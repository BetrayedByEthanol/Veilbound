"""B06 G4: bounded, source-backed damage and wound/recovery state.

G4 never decides whether an attack hits, rolls an attack, or invents a spell.
Callers supply confirmed deliveries or the exact pending G3 projectile ledger
entry. Canonical rules remain in docs/rules/05, 06 and 07.
"""
from dataclasses import dataclass
from math import ceil
import json

from scripts.b06_encounter_state_v0 import (
    ENEMIES, ROOT, RegenerationChoice, UnresolvedDecision, Wound, _integer,
)
from scripts.b06_world_clock_v0 import WorldClock


ARMOR = {
    "Leather armor": 3, "Brigandine": 5,
}
WOUND_BANDS = {"Serious": 10, "Severe": 20, "Critical": 30}
LOCATIONS = ((2, "Head / neck"), (8, "Chest"), (12, "Abdomen"),
             (15, "Arm"), (19, "Leg"), (20, "Hand / extremity"))


@dataclass(frozen=True)
class DamagePacket:
    """Already-rolled component; Armor only for a native physical HP packet."""
    resource: str
    damage_type: str
    raw: int
    penetration: int = 0
    armor_rule: str = "none"

    def __post_init__(self):
        if self.resource not in ("hp", "vigor"):
            raise ValueError("Only authored HP/Vigor packets may be applied")
        if not isinstance(self.damage_type, str) or not self.damage_type:
            raise ValueError("Explicit packet damage type required")
        _integer(self.raw, "raw packet")
        _integer(self.penetration, "penetration")
        if self.armor_rule not in ("none", "weapon"):
            raise UnresolvedDecision("Unimplemented physical mitigation source")
        if self.armor_rule == "weapon" and (
                self.resource != "hp" or
                self.damage_type not in ("Piercing", "Cut", "Crush", "Physical")):
            raise ValueError("Weapon Armor applies only to physical HP")
        if self.armor_rule == "none" and self.penetration:
            raise ValueError("Penetration without authored physical Armor rule")
        if (self.resource == "hp"
                and self.damage_type in ("Piercing", "Cut", "Crush", "Physical")
                and self.armor_rule == "none"):
            raise UnresolvedDecision("Physical HP packet requires source-authored mitigation")


class DamageState:
    def __init__(self, encounter, *, recovery_phase_seconds=None):
        if getattr(encounter, "g4", None) is not None:
            raise ValueError("G4 already installed")
        self.e = encounter
        self.used_events = set()
        # Actors may carry wounds across encounters. Resume beyond *all*
        # recorded G4 identifiers, including wounds belonging to other actors.
        existing = [w.ident for a in encounter.actors.values() for w in a.wounds]
        if any(len({w.ident for w in a.wounds}) != len(a.wounds)
               for a in encounter.actors.values()):
            raise ValueError("Carried wound IDs must be unique per actor")
        self.next_wound = max(
            (int(s[4:]) for s in existing
             if s.startswith("G4-W") and s[4:].isdigit()), default=0)
        self.short_toxins = []
        # The independent six-hour phase exists for each actor even without
        # a toxin, including when initiative starts or ends.
        self.clock = WorldClock(self,recovery_phase_seconds=recovery_phase_seconds)
        encounter.g4 = self
        encounter.log("g4_damage_state_installed")
        encounter.check()

    def _actor(self, actor_id):
        if actor_id not in self.e.actors:
            raise ValueError("Unknown damage recipient")
        return self.e.actors[actor_id]

    def _heal_delivery_issue(self,caster,recipient,*,hand_available,in_range,
                             unobstructed,delivery_check):
        """Live Basic Heal hand/path check; re-run after paid AP responses."""
        if delivery_check is not None:
            if not callable(delivery_check):
                raise ValueError("Basic Heal delivery_check must be callable")
            state=delivery_check(self.e,caster,recipient)
            if (not isinstance(state,(tuple,list)) or len(state)!=3
                    or any(type(v) is not bool for v in state)):
                raise ValueError("Basic Heal delivery_check must return three booleans")
            hand_available=hand_available and state[0]
            in_range=in_range and state[1]
            unobstructed=unobstructed and state[2]
        if hand_available is not True:
            return "hand_unavailable"
        if recipient==caster:
            return None
        if in_range is not True:
            return "delivery_out_of_range"
        if unobstructed is not True:
            return "delivery_obstructed"
        # Also independently recheck current G1 geometry if installed.
        if self.e.g1 is not None:
            a,b=self._actor(caster),self._actor(recipient)
            if len(a.occupied)!=1 or len(b.occupied)!=1:
                raise UnresolvedDecision("Basic Heal multicell air path needs explicit adjudication")
            origin,dest=a.occupied[0],b.occupied[0]
            dist=max(abs(origin[0]-dest[0]),abs(origin[1]-dest[1]))
            if dist>3:
                return "delivery_out_of_range"
            if dist==0:
                return "delivery_overlap_invalid"
            from scripts.b06_ranged_v0 import RangedCombat
            cells,corners=RangedCombat._ray(origin,dest)
            walls=self.e.g1.walls
            if (any(c in walls for c in cells[1:-1])
                    or any(u in walls or v in walls for u,v in corners)):
                return "delivery_obstructed"
        return None

    def _armor(self, a):
        if a.source.source_id in ENEMIES:
            obj = json.loads((ROOT / a.source.path).read_text(encoding="utf-8"))
            return _integer(obj["defenses"]["armor"], "source Armor")
        worn = [(name, state) for name, state in a.source.equipment
                if state == "worn" and name in ARMOR]
        if len(worn) != 1:
            raise UnresolvedDecision("No single verified current party Armor configuration")
        return ARMOR[worn[0][0]]

    def _mitigate_hp(self, a, packet):
        amount = packet.raw
        if packet.armor_rule == "weapon":
            amount = max(0, amount - max(0, self._armor(a) - packet.penetration))
        if self.e.g3 is not None:
            resistance = self.e.g3.resistance(a.id, packet.damage_type)
            amount = max(0, amount - resistance)
        return amount

    def apply_damage(self, recipient, packets, *, event_key, cause,
                     devastating=False, wound_location_roll=None,
                     wound_trauma=None):
        """Apply an independently *confirmed* damaging event exactly once.

        A delivered event may contain multiple HP and direct Vigor packets.
        Physical Hit/critical qualification and geometry are G2/G5 inputs.
        """
        a = self._actor(recipient)
        if not isinstance(event_key, str) or not event_key:
            raise ValueError("Event needs a stable unique key")
        if event_key in self.used_events:
            raise ValueError("Damaging event already consumed")
        if not isinstance(cause, str) or not cause:
            raise ValueError("Explicit source cause required")
        if type(devastating) is not bool:
            raise ValueError("Devastating must be independently adjudicated")
        packets = tuple(packets)
        if not packets or any(not isinstance(p, DamagePacket) for p in packets):
            raise ValueError("A delivered event requires typed packets")
        if a.dead:
            raise ValueError("Dead recipient cannot receive live encounter damage")
        resolved = [self._mitigate_hp(a, p) if p.resource == "hp" else p.raw
                    for p in packets]
        hp_loss = sum(x for p, x in zip(packets, resolved) if p.resource == "hp")
        hp_after = max(-a.hp_max, a.hp - hp_loss)
        crosses = a.hp > 0 and hp_after <= 0
        creates_wound = (crosses or devastating) and hp_after > -a.hp_max
        severity = None
        location = None
        if creates_wound:
            if type(wound_location_roll) is not int or not 1 <= wound_location_roll <= 20:
                raise UnresolvedDecision("Actual wound-location d20 required before damage commit")
            location = next(label for bound, label in LOCATIONS
                            if wound_location_roll <= bound)
            overkill = max(0, -hp_after)
            if overkill < ceil(a.hp_max / 3):
                severity = "Serious"
            elif overkill < ceil(2 * a.hp_max / 3):
                severity = "Severe"
            else:
                severity = "Critical"
            if devastating:
                severity = "Critical" if severity in ("Serious", "Severe") else severity
            if wound_trauma is None:
                wound_trauma = next((p.damage_type for p, n in zip(packets, resolved)
                                     if p.resource == "hp" and n > 0), "Unresolved")
        before_hp, before_vigor = a.hp, a.vigor
        a.hp = hp_after
        # Set the threshold flag before any VP-release hook can validate G0.
        a.dead = a.hp <= -a.hp_max
        if creates_wound:
            # Reserve a stable ID that cannot alias any carried or previously
            # issued wound, even after a second encounter / new DamageState.
            used_ids = {w.ident for actor in self.e.actors.values()
                        for w in actor.wounds}
            while True:
                self.next_wound += 1
                wound_id = f"G4-W{self.next_wound:04d}"
                if wound_id not in used_ids:
                    break
            a.wounds.append(Wound(wound_id,
                                  WOUND_BANDS[severity], severity=severity,
                                  location=location, trauma=wound_trauma,
                                  source_event=event_key))
            self.e.log("g4_wound_created", recipient=recipient,
                       wound=a.wounds[-1].ident, severity=severity,
                       requirement=WOUND_BANDS[severity],
                       location=location, trauma=wound_trauma,
                       event_key=event_key)
        vigor_details = []
        for p, n in zip(packets, resolved):
            if p.resource != "vigor":
                continue
            # Never consume Shelter budget for reserve the actor does not have.
            actual = min(a.vigor, n)
            residual = (self.e.g3.prevent_vigor(recipient, actual)
                        if self.e.g3 is not None else actual)
            a.vigor -= residual
            vigor_details.append({"raw": p.raw, "available": actual,
                                  "prevented": actual - residual,
                                  "applied": residual})
        a.dead = a.hp <= -a.hp_max
        if a.hp <= 0:
            a.ap_remaining = 0
            if self.e.g3 is not None:
                self.e.g3.sync_consciousness(recipient)
        self.used_events.add(event_key)
        self.e.log("g4_damage_applied", event_key=event_key, cause=cause,
                   recipient=recipient, hp_before=before_hp, hp_after=a.hp,
                   vigor_before=before_vigor, vigor_after=a.vigor,
                   packets=[{"resource":p.resource, "type":p.damage_type,
                             "raw":p.raw, "mitigated":n, "armor_rule":p.armor_rule}
                            for p,n in zip(packets,resolved)],
                   vigor_details=vigor_details, wound=severity, dead=a.dead)
        self.e.check()
        return {"hp_loss": before_hp-a.hp, "vigor_loss": before_vigor-a.vigor,
                "wound": severity, "dead": a.dead,
                "hp_packets": [n for p,n in zip(packets,resolved) if p.resource=="hp"]}

    def preflight_flame_wound(self, recipient, wound_location_roll):
        """Require a wound die before paying for a G3 Flame that will cross 0."""
        a=self._actor(recipient)
        hp_loss=self._mitigate_hp(a,DamagePacket("hp","Fire",2))
        after=max(-a.hp_max,a.hp-hp_loss)
        if a.hp>0 and after<=0 and after>-a.hp_max:
            if type(wound_location_roll) is not int or not 1<=wound_location_roll<=20:
                raise UnresolvedDecision("Actual wound-location d20 required before Flame VP payment")

    def apply_flame(self, caster, target, *, ledger_index, wound_location_roll=None):
        """Consume *only* the just-launched G3 direct hit synchronously."""
        if self.e.g3 is None:
            raise ValueError("G3 needed for Thrown Flame")
        _integer(ledger_index, "G3 ledger index")
        event_key=f"g3-flame-ledger:{ledger_index}"
        if event_key in self.used_events:
            raise ValueError("Damaging event already consumed")
        if ledger_index!=len(self.e.ledger)-1 or self.e.current!=caster:
            raise ValueError("Flame damage must resolve at its original launch")
        ev = self.e.ledger[ledger_index]
        if ev["round"]!=self.e.round or ev["turn"]!=caster:
            raise ValueError("Flame launch no longer belongs to current turn")
        d = ev["detail"]
        if (ev["kind"] != "g3_flame_launched" or d.get("caster") != caster
                or d.get("target") != target
                or d.get("outcome") != "direct_hit_pending_G4"):
            raise ValueError("No confirmed ordinary direct G3 Flame at this event")
        pending = d.get("packets_pending_g4")
        if not isinstance(pending, dict) or set(pending) != {"fire_hp", "vigor"}:
            raise ValueError("Missing G3 authorized packet pair")
        return self.apply_damage(target, (
            DamagePacket("hp", "Fire", pending["fire_hp"]),
            DamagePacket("vigor", "Direct Vigor", pending["vigor"])),
            event_key=event_key, cause="g3:thrown_flame",
            wound_location_roll=wound_location_roll)

    def apply_profile_hit(self, attacker, target, profile_id, *,
                          die_face, confirmed_hit, critical="normal",
                          critical_dice=(), vigor_die=None, wound_location_roll=None):
        """Post-G5 attack-result adapter for exact B06 enemy JSON damage profiles.

        The caller must have independently adjudicated hit, legal contact,
        responses, and any critical confirmation. No AP or defense is added.
        """
        source = self._actor(attacker)
        if source.source.source_id not in ENEMIES:
            raise UnresolvedDecision("Only exact B06 enemy attack profiles supported")
        if confirmed_hit is not True:
            raise UnresolvedDecision("G5 must independently confirm hit/contact")
        obj = json.loads((ROOT / source.source.path).read_text(encoding="utf-8"))
        profs = [p for p in obj["attack_profiles"] if p["id"] == profile_id]
        if len(profs) != 1 or profs[0]["primary_hp_packet"] is None:
            raise ValueError("Unknown or non-damaging source attack")
        if source.hp <= 0 or source.dead:
            raise ValueError("Incapacitated attacker cannot deliver normal hit")
        if source.source.source_id == "B06-EN-01":
            if self.e.g3 is None or self.e.g3.sentry_profile(attacker) != profile_id:
                raise ValueError("Sentry attack disagrees with actual wielded reserve")
        p = profs[0]
        main = p["primary_hp_packet"]
        die = main["die"]
        sides = {"d4":4, "d6":6, "d8":8}.get(die)
        if sides is None or type(die_face) is not int or not 1<=die_face<=sides:
            raise ValueError("Explicit legal native damage die required")
        if critical not in ("normal", "strong", "critical", "devastating"):
            raise ValueError("Unsupported critical classification")
        expected = {"normal":0,"strong":1,"critical":2,"devastating":2}[critical]
        if len(critical_dice) != expected or any(
                type(x) is not int or not 1<=x<=4 for x in critical_dice):
            raise ValueError("Canonical critical d4 faces required once")
        abilities = dict(source.source.abilities)
        strength = abilities.get("strength", abilities.get("Strength", 0))
        contribution = main["strength_contribution"]
        bonus = (0 if contribution=="none" else strength if contribution=="full"
                 else max(strength, 0)//2 if contribution=="light" else None)
        if bonus is None:
            raise UnresolvedDecision("Unsupported physical contribution formula")
        packets = [DamagePacket("hp", main["damage_type"],
                                main["fixed_base"]+die_face+bonus+sum(critical_dice),
                                main["armor_penetration"], "weapon")]
        for extra in p["additional_packets"]:
            raw = extra["fixed_base"]
            if extra["kind"] == "vigor":
                formula = extra.get("extra_formula")
                if formula:
                    if formula["operator"]!="ceil_div_dice" or (
                            type(vigor_die) is not int or not 1<=vigor_die<=6):
                        raise ValueError("Explicit enchanted-sword d6 required")
                    raw += ceil(vigor_die*formula["multiplier"]/formula["divisor"])
                    raw += formula["vc_bonus"]
            elif extra["kind"] != "hp":
                raise UnresolvedDecision("Unsupported extra damage resource")
            packets.append(DamagePacket(extra["kind"],extra["damage_type"],raw))
        result = self.apply_damage(
            target, packets,
            event_key=f"g4:profile:{attacker}:{target}:{profile_id}:{len(self.e.ledger)}",
            cause=f"source-profile:{profile_id}",
            devastating=(critical=="devastating"),
            wound_location_roll=wound_location_roll,
            wound_trauma=main["damage_type"])
        result["injection_eligible"] = bool(p.get("toxin_delivery")
                                            and result["hp_packets"][0] > 0)
        # Qualification only: the Hunter's toxin still requires real
        # resistance/ward adjudication and its own long clock.
        self.e.log("g4_profile_hit", attacker=attacker,target=target,
                   profile=profile_id, critical=critical,
                   injection_eligible=result["injection_eligible"])
        return result

    @staticmethod
    def _validate_heal_blocks(blocked_components):
        """Require explicit per-component adjudication, never infer a blanket block."""
        if not isinstance(blocked_components,(tuple,list,frozenset)):
            raise ValueError("Healing blocks must be an explicit component collection")
        blocks=tuple(blocked_components)
        if (any(type(x) is not str for x in blocks)
                or len(set(blocks))!=len(blocks)
                or any(x not in ("vigor","hp","repair") for x in blocks)):
            raise UnresolvedDecision("Unknown or repeated healing component prohibition")
        return frozenset(blocks)

    @staticmethod
    def live_heal_blocks(encounter,caster,recipient,declared,restoration_check):
        """Re-read independently attested active blocks at the real application.

        Always run this *after* committed responses, even if the initial
        declaration had zero blocks. A static declared prohibition remains
        in force; a live check can add newly established prohibitions.
        """
        blocks=DamageState._validate_heal_blocks(declared)
        if restoration_check is not None:
            if not callable(restoration_check):
                raise ValueError("Basic Heal restoration_check must be callable")
            blocks |= DamageState._validate_heal_blocks(
                restoration_check(encounter,caster,recipient))
        return blocks

    def resolve_heal(self, recipient, *, contribution, vigor_amount,
                     wound_id=None, source="Basic Heal",blocked_components=()):
        """One already paid and successfully delivered Basic Heal contribution."""
        a = self._actor(recipient)
        if a.dead:
            raise ValueError("Basic Heal cannot resurrect")
        if a.hp>0 and wound_id is not None:
            raise ValueError("Non-Dying Basic Heal does not target wound progress")
        if contribution not in ("Primary", "Secondary"):
            raise ValueError("Only actually authored Basic Heal contributions")
        _integer(vigor_amount, "heal Vigor packet")
        blocks=self._validate_heal_blocks(blocked_components)
        amount = 2 if contribution=="Primary" else 1
        old_hp, old_vigor = a.hp, a.vigor
        progress = 0
        if a.hp<=0:
            repairable = [w for w in a.wounds if w.repairable and
                          w.progress < w.requirement]
            if wound_id is not None:
                chosen = next((w for w in repairable if w.ident==wound_id),None)
                if chosen is None:
                    raise ValueError("Selected wound is not an unfinished repairable wound")
            else:
                chosen = repairable[0] if repairable else None
            if chosen is not None and "repair" not in blocks:
                progress = min(amount, chosen.requirement - chosen.progress)
                chosen.progress += progress
                amount -= progress
            if any(w.progress < w.requirement for w in a.wounds):
                amount = 0
        # A ward may independently prohibit direct HP, direct external Repair,
        # or external Vigor. Do not let blocked repair points spill into HP.
        # Non-Dying Heal never adds Repair Progress even when wounded.
        if "hp" in blocks:
            amount=0
        if "vigor" in blocks:
            vigor_amount=0
        a.hp = min(a.hp_max, a.hp + amount)
        a.vigor = min(a.vigor_max, a.vigor + vigor_amount)
        self.e.log("g4_basic_heal_applied", recipient=recipient, source=source,
                   contribution=contribution, wound_id=(chosen.ident if old_hp<=0 and chosen else None),
                   direct_repair=progress, hp_restored=a.hp-old_hp,
                   vigor_restored=a.vigor-old_vigor, regen_debit=0,
                   blocked_components=sorted(blocks))
        self.e.check()
        return {"hp_restored":a.hp-old_hp,"vigor_restored":a.vigor-old_vigor,
                "repair_progress":progress}

    def cast_basic_heal(self, caster, recipient, *, tier=1, die,
                        hand_available=False, unobstructed=False,
                        in_range=False, unopposed=True, wound_id=None,
                        on_committed=None, delivery_check=None,
                        blocked_restoration=(),restoration_check=None):
        """Authorised F/R Primary, including Dying allies; no invented contest."""
        g3 = self.e.g3
        if g3 is None:
            raise ValueError("Source-backed G3 required for casting")
        actor = g3._own(caster,20 if self._actor(caster).source.source_id=="F" else 30)
        if actor.source.source_id not in ("F","R"):
            raise UnresolvedDecision("Caster lacks verified Basic Heal repertoire")
        if type(tier) is not int or tier<1 or tier>(1 if actor.level<3 else 2):
            raise ValueError("Invalid Heal Used Tier")
        if type(die) is not int or not 1<=die<=8:
            raise ValueError("Explicit legal d8 required")
        if on_committed is not None and delivery_check is None:
            raise UnresolvedDecision(
                "Committed responses require live Basic Heal delivery_check")
        if on_committed is not None and restoration_check is None:
            raise UnresolvedDecision(
                "Committed Basic Heal requires live restoration_check")
        # Neither an empty declaration snapshot nor a guessed absence of wards
        # is sufficient when responses can establish new protections.
        self.live_heal_blocks(self.e,caster,recipient,blocked_restoration,
                              restoration_check)
        preflight=self._heal_delivery_issue(
            caster,recipient,hand_available=hand_available,
            in_range=in_range,unobstructed=unobstructed,
            delivery_check=delivery_check)
        if preflight=="hand_unavailable":
            raise ValueError("Available functioning hand required")
        if preflight is not None:
            raise UnresolvedDecision(
                "Single Target needs current visible 3-square unobstructed air path: "+preflight)
        if unopposed is not True:
            raise UnresolvedDecision("Intrusion +8 resistance outcome requires separate valid contest")
        target = self._actor(recipient)
        if target.dead:
            raise ValueError("Dead target is ineligible")
        if target.hp<=0 and wound_id is not None and not any(
                w.ident==wound_id and w.repairable and w.progress<w.requirement
                for w in target.wounds):
            raise ValueError("No selected incomplete repairable wound")
        cost=2*tier
        g3._funds(actor,cost,0)
        g3._commit(caster,on_committed=on_committed,label="g4:basic_heal_primary")
        selected_invalid = wound_id is not None and (
            target.hp > 0 or not any(
                w.ident == wound_id and w.repairable and w.progress < w.requirement
                for w in target.wounds))
        # A committed response can change the hand or magical delivery
        # geometry. A stale initial assertion cannot spend healing VP.
        postflight=self._heal_delivery_issue(
            caster,recipient,hand_available=hand_available,
            in_range=in_range,unobstructed=unobstructed,
            delivery_check=delivery_check)
        # The live check is unconditional: a new prohibition might have been
        # created by committed responses even when no initial block existed.
        blocks=self.live_heal_blocks(self.e,caster,recipient,
                                      blocked_restoration,restoration_check)
        if (actor.hp<=0 or actor.vp_available<cost or target.dead
                or selected_invalid or postflight is not None):
            self.e.log("g4_heal_interrupted",caster=caster,recipient=recipient,
                       cause=postflight or "post_commit_source_or_resources",
                       spent_vp=0)
            return None
        g3._pay(caster,cost,0,label="g4:basic_heal_primary")
        result=self.resolve_heal(recipient,contribution="Primary",
                                 vigor_amount=4+ceil(die*tier/3)+g3.heal_vc(actor),
                                 wound_id=wound_id,
                                 blocked_components=blocks,
                                 source="g4:paid_primary")
        result["spent_vp"]=cost
        return result

    def regenerate(self, a, choice):
        """Actual existing G0 Step 2; more precise multi-wound choice, no new tick."""
        e=self.e
        if a.id in e.regen_done:
            raise ValueError("Regeneration Step already resolved this round")
        if a.dead:
            e.regen_done.add(a.id)
            e.log("regeneration_dead",actor=a.id)
            return
        throughput=a.regen+(e.g3.regen_throughput(a.id) if e.g3 is not None else 0)
        incomplete=[w for w in a.wounds if w.progress < w.requirement]
        repairable=[w for w in incomplete if w.repairable]
        missing=(a.hp<a.hp_max or bool(repairable))
        if missing and a.vigor>0 and throughput>0 and choice is None:
            e.log("unresolved_decision",actor=a.id,choice="regeneration_allocation")
            raise UnresolvedDecision("Explicit regeneration allocation required")
        choice=choice or RegenerationChoice()
        if not isinstance(choice,RegenerationChoice):
            raise ValueError("Invalid regeneration choice")
        for n in (choice.hp,choice.repair):
            _integer(n,"regeneration points")
        if type(choice.cancel_dying_loss) is not bool:
            raise ValueError("Cancellation needs an explicit Boolean")
        dying=a.hp<=0
        if choice.cancel_dying_loss and not dying:
            raise ValueError("Cannot cancel Dying loss above 0 HP")
        survival=int(dying and choice.cancel_dying_loss)
        debit=survival+choice.hp+choice.repair
        if debit>throughput or debit>a.vigor:
            raise ValueError("Natural regeneration exceeds throughput or available Vigor")
        if choice.hp>a.hp_max-a.hp:
            raise ValueError("Natural HP regeneration exceeds missing HP")
        allocation=()
        if dying:
            if choice.wound_allocations:
                raise ValueError("Dying repair is always oldest unfinished first")
            remaining=choice.repair
            tmp=[]
            for w in repairable:
                n=min(remaining,w.requirement-w.progress)
                if n:
                    tmp.append((w.ident,n))
                    remaining-=n
            if remaining:
                raise ValueError("Repair would exceed unfinished wounds")
            allocation=tuple(tmp)
        elif choice.repair:
            if choice.wound_allocations:
                allocation=tuple(choice.wound_allocations)
            elif len(repairable)==1:
                allocation=((repairable[0].ident,choice.repair),)
            else:
                raise UnresolvedDecision("Select non-Dying wound allocation explicitly in G4")
        elif choice.wound_allocations:
            raise ValueError("Unexpected per-wound allocation with zero repair")
        if any(not isinstance(x,(tuple,list)) or len(x)!=2 for x in allocation):
            raise ValueError("Malformed wound allocation")
        if sum(n for _,n in allocation)!=choice.repair:
            raise ValueError("Repair sum does not match requested throughput")
        if len(set(w for w,_ in allocation))!=len(allocation):
            raise ValueError("Repeated wound allocation target")
        for ident,n in allocation:
            _integer(n,"wound repair",1)
            wound=next((w for w in repairable if w.ident==ident),None)
            if wound is None or n>wound.requirement-wound.progress:
                raise ValueError("Invalid wound progress recipient or overrepair")
        if dying and choice.hp and (
                any(not w.repairable for w in incomplete) or
                choice.repair<sum(w.requirement-w.progress for w in repairable)):
            raise ValueError("Dying HP blocked by incomplete wound repair")
        if dying and not survival and a.hp-1<=-a.hp_max and debit:
            raise ValueError("Cannot spend regeneration after lethal Dying loss")
        # All checks above are preflight; no partial Vigor/wound mutations.
        e.regen_done.add(a.id)
        hp_before, vigor_before=a.hp,a.vigor
        if dying and not survival:
            a.hp=max(-a.hp_max,a.hp-1)
            a.dead=a.hp<=-a.hp_max
        if not a.dead:
            for ident,n in allocation:
                next(w for w in a.wounds if w.ident==ident).progress+=n
            a.hp+=choice.hp
            a.vigor-=debit
        if a.hp<=0 and e.g3 is not None:
            e.g3.sync_consciousness(a.id)
        e.log("regeneration_step",actor=a.id,hp_before=hp_before,
              hp_after=a.hp,vigor_before=vigor_before,vigor_after=a.vigor,
              survival_cancelled=bool(survival),hp_restored=choice.hp if not a.dead else 0,
              repair_points=choice.repair if not a.dead else 0,
              throughput_spent=debit if not a.dead else 0,
              wound_allocations=list(allocation),dead=a.dead)
        e.check()

    def schedule_hemotoxin(self, recipient, *, exposure_key,
                            actual_exposure, resistance_total,
                            wound_location_roll):
        """TX-HM after independently verified actual exposure and natural check."""
        self._actor(recipient)
        if actual_exposure is not True:
            raise UnresolvedDecision("No toxin without verified delivery")
        if type(resistance_total) is not int:
            raise UnresolvedDecision("Explicit natural resistance result required")
        if not isinstance(exposure_key,str) or not exposure_key:
            raise ValueError("Stable exposure key required")
        # Precommitted actual d20 is available if a later packet crosses 0.
        # This avoids silently consuming an overdue Step 3 packet while an
        # unresolved location choice interrupts an already-paid G0 Step 2.
        if type(wound_location_roll) is not int or not 1<=wound_location_roll<=20:
            raise UnresolvedDecision("Provide real possible-crossing wound-location d20")
        if any(t["key"]==exposure_key for t in self.short_toxins):
            raise ValueError("Duplicate toxin exposure")
        # This bounded primitive does not decide stacking with already-live
        # other toxin families or Venom Endurance: refuse duplicate active TX-HM.
        if any(t["recipient"]==recipient and t["left"] for t in self.short_toxins):
            raise UnresolvedDecision("Source-specific toxin nonstack/ward resolution needed")
        t={"key":exposure_key,"recipient":recipient,
           "left":3 if resistance_total>=12 else 5,
           "phase":0,"applied":0,"wound_location_roll":wound_location_roll}
        self.short_toxins.append(t)
        self.e.log("g4_toxin_scheduled",recipient=recipient,profile="TX-HM",
                   key=exposure_key,ticks=t["left"],resistance_total=resistance_total)

    def _toxin_step(self,t):
        if t["left"]==0:
            return
        number=t["applied"]+1
        if not self._actor(t["recipient"]).dead:
            self.apply_damage(t["recipient"],(DamagePacket("hp","Toxin",1),),
                              event_key=f"toxin:{t['key']}:{number}",
                              cause="TX-HM:scheduled_hp_tick",
                              wound_location_roll=t["wound_location_roll"])
        t["applied"]=number
        t["left"]-=1
        self.e.log("g4_toxin_tick",recipient=t["recipient"],
                   profile="TX-HM",key=t["key"],remaining=t["left"])

    def on_turn_start(self,actor_id):
        """Step 3 after real G0 regeneration, before establishing turn AP."""
        for t in self.short_toxins:
            if t["recipient"]==actor_id and t["left"]:
                self._toxin_step(t)

    def advance_exploration(self,seconds):
        """Advance the shared G4.2 chronology; never create a phantom turn."""
        return self.clock.advance_exploration(seconds)
