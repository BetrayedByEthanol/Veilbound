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
from scripts.b06_mundane_toxins_v0 import MundaneToxins
from scripts.b06_hunter_venom_endurance_v0 import HunterVenomEndurance


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
        # An ordinary apply_damage caller cannot impersonate the synchronous
        # G3->G4 Flame delivery merely by guessing its event key/cause.
        # Only apply_flame opens this transient exact-packet authority.
        self._live_flame_delivery = None
        # Only a currently applying native G4 packet authorizes Medium L3
        # Intercession; direct G3 calls must never fabricate a packet.
        self._live_medium_vigor = None
        self._flame_consumptions = {}
        # Optional source-bound Medium Gifted Ward adapter; no implicit effects.
        self.medium_gifted = None
        self._live_ward_delivery = None
        self._live_ward_profile = None
        # Only G4.5's exact G0-paid source action can attest Ward G5 delivery.
        self._live_ward_action = None
        # Scoped G4.5 Opportunity receipt; detached rehearsal has its own marker.
        self._live_ward_opportunity = None
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
        self.toxins = MundaneToxins(self)
        self.venom = HunterVenomEndurance(self)
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

    def _preview_damage_packets(self, recipient, packets):
        """Pure native packet mitigation plus optional Chosen HP diversion.

        Both G5's preflight and G4's eventual application MUST compute the
        same HP/wound threshold from the same live source packets. The Low
        Life preview never consumes a host budget or a pending property.
        """
        victim=self._actor(recipient)
        resolved=tuple(
            self._mitigate_hp(victim,p) if p.resource=="hp" else p.raw
            for p in packets)
        low=(getattr(self.e.g3,"low_life",None)
             if self.e.g3 is not None else None)
        if low is None:
            after, low_proposal = resolved, None
        else:
            after, low_proposal = low.preview_hp(recipient, packets, resolved)
        if self.medium_gifted is not None:
            proposal = self.medium_gifted.preview(
                recipient, packets, after, low_proposal=low_proposal)
            after = proposal["remaining"]
        return after, low_proposal

    def apply_damage(self, recipient, packets, *, event_key, cause,
                     devastating=False, wound_location_roll=None,
                     wound_trauma=None, medium_intercessor=None):
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
        if (cause=="g3:thrown_flame"
                and self._live_flame_delivery!=(
                    recipient,event_key,packets,devastating)):
            raise UnresolvedDecision(
                "G3 Flame damage must be consumed through native G4.apply_flame")
        if a.dead:
            raise ValueError("Dead recipient cannot receive live encounter damage")
        if medium_intercessor is not None:
            if (self.e.g3 is None or
                    getattr(self.e.g3, "medium_life", None) is None or
                    not any(p.resource=="vigor" and p.raw>0 for p in packets)):
                raise ValueError("Medium Intercession requires native positive G4 Vigor packet")
            # Fail closed before any HP/Vigor or wound mutation.
            self.e.g3.medium_life.preflight_vigor(medium_intercessor,recipient)
        resolved,lp_proposal=self._preview_damage_packets(recipient,packets)
        ward=self.medium_gifted
        ward_proposal=None
        if ward is not None:
            base=tuple(self._mitigate_hp(a,p) if p.resource=="hp"
                       else p.raw for p in packets)
            low_for_preview=(getattr(self.e.g3,"low_life",None)
                             if self.e.g3 is not None else None)
            if low_for_preview is not None:
                base,_=low_for_preview.preview_hp(recipient,packets,base)
            ward_proposal=ward.preview(
                recipient,packets,base,low_proposal=lp_proposal)
            if ward_proposal["remaining"]!=resolved:
                raise UnresolvedDecision("Ward G4 preflight diverged from damage plan")
            if ward_proposal["prevention"] and medium_intercessor is not None:
                raise UnresolvedDecision(
                    "Ward and Medium Intercession finite prevention ordering unauthored")
        low=(getattr(self.e.g3,"low_life",None)
             if self.e.g3 is not None else None)
        hp_loss = sum(x for p, x in zip(packets, resolved) if p.resource == "hp")
        hp_after = max(-a.hp_max, a.hp - hp_loss)
        if medium_intercessor is not None and hp_after <= -a.hp_max:
            raise UnresolvedDecision("Cannot extend Consecration to a fatal recipient")
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
        # Intercession is a defensive Reaction to the already-confirmed
        # incoming packet. Resolve it AFTER the entire HP/wound preflight,
        # but BEFORE committing any HP loss: the recipient can also be the
        # priest, and the same mixed hit may incapacitate the priest.
        # Waiting for the later Vigor loop would recheck consciousness
        # after the wound was already written, then fail partially.
        interceded_packet = None
        if medium_intercessor is not None:
            # The Reaction must see the FULL eligible packet. The rule only
            # caps damage to Current Vigor AFTER finite-budget prevention.
            # A 10-point packet against Vigor 2 and B8 consumes all B8,
            # then applies the remaining 2 damage.
            first = next(((i,n)
                          for i,(p,n) in enumerate(zip(packets,resolved))
                          if p.resource == "vigor" and n > 0 and a.vigor > 0),
                         None)
            if first is None:
                raise ValueError("No positive native Vigor packet to Intercede")
            index, actual = first
            if self._live_medium_vigor is not None:
                raise UnresolvedDecision("Nested Medium packet intercession")
            # Exact caster, beneficiary and amount belong to this one live
            # G4 application, never a caller-owned fabricated spell packet.
            self._live_medium_vigor = (medium_intercessor,recipient,actual)
            try:
                residual = self.e.g3.prevent_vigor(
                    recipient,actual,medium_intercessor=medium_intercessor)
            finally:
                self._live_medium_vigor = None
            interceded_packet = (index,residual)
        if ward_proposal is not None and ward_proposal["prevention"]:
            if self._live_ward_delivery is not None:
                raise UnresolvedDecision("Nested native Ward delivery")
            self._live_ward_delivery=(recipient,event_key,cause,packets)
            try:
                ward.commit(recipient,packets,ward_proposal,
                            event_key=event_key,cause=cause)
            finally:
                self._live_ward_delivery=None
        if lp_proposal is not None:
            low.commit_hp(recipient,lp_proposal,event_key=event_key)
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
        for index, (p, n) in enumerate(zip(packets, resolved)):
            if p.resource != "vigor":
                continue
            # Preserve the full post-mitigation packet until protection has
            # consumed its finite budget. Even with Current Vigor 2, a
            # confirmed packet of 10 must consume B8 before the final 2
            # points are applied to Vigor. At Current Vigor 0, the shelter
            # itself prevents nothing (G3 owns that explicit rule).
            available = a.vigor
            if interceded_packet is not None and index == interceded_packet[0]:
                # Already paid/blocked in the live pre-damage Reaction window.
                # This is the same first positive packet, never a second
                # Intercession, even if the hit also caused Dying.
                residual = interceded_packet[1]
            else:
                residual = (self.e.g3.prevent_vigor(recipient,n)
                            if self.e.g3 is not None else n)
            applied = min(available,residual)
            a.vigor -= applied
            vigor_details.append({"raw": p.raw,
                                  "available": min(available,n),
                                  "prevented": n - residual,
                                  "applied": applied})
        a.dead = a.hp <= -a.hp_max
        if a.hp <= 0:
            a.ap_remaining = 0
            if self.e.g3 is not None:
                self.e.g3.sync_consciousness(recipient)
            if ward is not None:
                ward.sync_consciousness(recipient)
        self.used_events.add(event_key)
        self.e.log("g4_damage_applied", event_key=event_key, cause=cause,
                   recipient=recipient, hp_before=before_hp, hp_after=a.hp,
                   vigor_before=before_vigor, vigor_after=a.vigor,
                   packets=[{"resource":p.resource, "type":p.damage_type,
                             "raw":p.raw, "mitigated":n, "armor_rule":p.armor_rule}
                            for p,n in zip(packets,resolved)],
                   vigor_details=vigor_details, wound=severity, dead=a.dead,
                   medium_gifted_ward=(ward_proposal["receipt"]
                                      if ward_proposal is not None else None))
        # EX-LR-01 payout happens only after native HP loss, wound,
        # and Dying/death rules. The event ledger keeps the gross loss and
        # a separate paid post-hit Exaltation receipt.
        if low is not None:
            low.after_hp_loss(recipient,before_hp-a.hp,event_key=event_key)
        # Independently resolved G4 damage can incapacitate an attacker
        # *after* G0 has paid and declared a G5 multi-slot sword sequence.
        # Close every remaining paid slot at the real damage boundary,
        # before any subsequent G5 resolve/contact or native turn-end gate.
        if a.hp<=0 and getattr(self.e,"g5",None) is not None:
            self.e.g5.cancel_incapacitated_attacker(
                recipient,damage_event_key=event_key)
        if a.dead and before_hp > -a.hp_max:
            # Recipient death ends fixed Venom Endurance immediately, even
            # when there is no later toxin check or caster interaction.
            self.venom.on_recipient_death(recipient)
        self.e.check()
        return {"hp_loss": before_hp-a.hp, "vigor_loss": before_vigor-a.vigor,
                "wound": severity, "dead": a.dead,
                "hp_packets": [n for p,n in zip(packets,resolved) if p.resource=="hp"]}

    def preflight_flame_wound(self, recipient, wound_location_roll, *,
                             fire_hp=2, devastating=False):
        """Preflight the exact Fire primary *including* confirmed critical d4s.

        A Devastating direct Flame also requires a real location die even
        without crossing 0 HP. The future hit must consume the same value.
        """
        if type(fire_hp) is not int or fire_hp<2 or type(devastating) is not bool:
            raise ValueError("Source-confirmed Flame Fire HP/critical required")
        a=self._actor(recipient)
        # This is the same pure, live packet preview used by native G5
        # preflight and G4.apply_damage. An armed Low Priest Vital
        # Interposition may absorb a Flame's Fire HP *before* the wound
        # threshold is evaluated; preview neither spends budget nor VP.
        packets=(DamagePacket("hp","Fire",fire_hp),)
        resolved,_=self._preview_damage_packets(recipient,packets)
        hp_loss=resolved[0]
        after=max(-a.hp_max,a.hp-hp_loss)
        wound=((a.hp>0 and after<=0) or devastating) and after>-a.hp_max
        if wound and (type(wound_location_roll) is not int
                      or not 1<=wound_location_roll<=20):
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
        critical=d.get("critical","normal")
        extra=d.get("critical_dice",[])
        required={"normal":0,"strong":1,"critical":2,"devastating":2}.get(critical)
        if (required is None or not isinstance(extra,(tuple,list))
                or len(extra)!=required
                or any(type(x) is not int or not 1<=x<=4 for x in extra)
                or type(pending["fire_hp"]) is not int
                or pending["fire_hp"]!=2+sum(extra)
                or type(pending["vigor"]) is not int
                or pending["vigor"]<0):
            raise ValueError("G3 primary Fire packet/critical evidence mismatch")
        packets=(DamagePacket("hp","Fire",pending["fire_hp"]),
                 DamagePacket("vigor","Direct Vigor",pending["vigor"]))
        if self._live_flame_delivery is not None:
            raise UnresolvedDecision("Nested G3 Flame damage delivery not authorized")
        self._live_flame_delivery=(
            target,event_key,packets,critical=="devastating")
        start=len(self.e.ledger)
        try:
            result=self.apply_damage(
                target,packets,event_key=event_key,cause="g3:thrown_flame",
                devastating=critical=="devastating",
                wound_location_roll=wound_location_roll)
        finally:
            # An exception must never leak authorization to a later
            # generic delivery or to another turn.
            self._live_flame_delivery=None
        deliveries=[entry for entry in self.e.ledger[start:]
                    if entry["kind"]=="g4_damage_applied"
                    and entry["detail"].get("event_key")==event_key
                    and entry["detail"].get("recipient")==target]
        if len(deliveries)!=1:
            raise AssertionError("Native Flame consumption lacks one G4 packet")
        # Runtime source provenance, written ONLY by this dedicated G4
        # executor after real damage. No new ledger event or historical
        # G7-A hash is introduced by this additional authority check.
        self._flame_consumptions[ledger_index]=deliveries[0]["index"]
        return result

    def _profile_hit_packets(self, attacker, target, profile_id, *,
                             die_face, critical="normal",
                             critical_dice=(), vigor_die=None):
        """Source-derived packets and input validation only; never mutate G4."""
        source = self._actor(attacker)
        if source.source.source_id in ("A","B"):
            from scripts.b06_player_offense_g6b_v0 import party_weapon_profile
            profile,_=party_weapon_profile(source,profile_id)
            profs=[profile]
        elif source.source.source_id in ("S","T"):
            from scripts.b05_scholar_native_sword_v0 import scholar_sword_profile
            profile,_=scholar_sword_profile(
                source,profile_id,encounter=self.e)
            profs=[profile]
        elif source.source.source_id in ENEMIES:
            obj = json.loads((ROOT / source.source.path).read_text(encoding="utf-8"))
            profs = [p for p in obj["attack_profiles"] if p["id"] == profile_id]
        else:
            raise UnresolvedDecision("Only sourced enemy or explicitly audited player melee damage supported")
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
        return p,main,tuple(packets)

    def preflight_profile_hit(self, attacker, target, profile_id, *,
                              die_face, critical="normal",
                              critical_dice=(), vigor_die=None,
                              wound_location_roll=None):
        """Validate exact live G4 inputs before G5 commits any dice/result.

        Includes all source-specific extra packets and effective Armor/
        resistance, so 0-HP crossing and Devastating wound locations are
        checked against the SAME calculation used in actual application.
        """
        p,main,packets=self._profile_hit_packets(
            attacker,target,profile_id,die_face=die_face,
            critical=critical,critical_dice=critical_dice,
            vigor_die=vigor_die)
        victim=self._actor(target)
        if victim.dead:
            raise ValueError("Dead recipient cannot receive live encounter damage")
        resolved,_=self._preview_damage_packets(target,packets)
        hp_loss=sum(n for p,n in zip(packets,resolved) if p.resource=="hp")
        hp_after=max(-victim.hp_max,victim.hp-hp_loss)
        creates_wound=(victim.hp>0 and hp_after<=0
                       or critical=="devastating") and hp_after>-victim.hp_max
        if creates_wound and (type(wound_location_roll) is not int
                              or not 1<=wound_location_roll<=20):
            raise UnresolvedDecision(
                "Actual wound-location d20 required before G5 roll commit")
        return {"hp_after":hp_after,"wound_required":bool(creates_wound),
                "hp_packet_count":sum(x.resource=="hp" for x in packets),
                "vigor_packet_count":sum(x.resource=="vigor" for x in packets)}

    def apply_profile_hit(self, attacker, target, profile_id, *,
                          die_face, confirmed_hit, critical="normal",
                          critical_dice=(), vigor_die=None, wound_location_roll=None,
                          medium_intercessor=None):
        """Post-G5 attack-result adapter for exact B06 enemy JSON damage profiles.

        The caller must have independently adjudicated hit, legal contact,
        responses, and any critical confirmation. No AP or defense is added.
        """
        if confirmed_hit is not True:
            raise UnresolvedDecision("G5 must independently confirm hit/contact")
        self.preflight_profile_hit(
            attacker,target,profile_id,die_face=die_face,
            critical=critical,critical_dice=critical_dice,
            vigor_die=vigor_die,wound_location_roll=wound_location_roll)
        p,main,packets=self._profile_hit_packets(
            attacker,target,profile_id,die_face=die_face,
            critical=critical,critical_dice=critical_dice,
            vigor_die=vigor_die)
        if self._live_ward_profile is not None:
            raise UnresolvedDecision("Nested source profile delivery")
        self._live_ward_profile=(attacker,target,profile_id,packets)
        try:
            result = self.apply_damage(
                target, packets,
                event_key=f"g4:profile:{attacker}:{target}:{profile_id}:{len(self.e.ledger)}",
                cause=f"source-profile:{profile_id}",
                devastating=(critical=="devastating"),
                wound_location_roll=wound_location_roll,
                wound_trauma=main["damage_type"],
                medium_intercessor=medium_intercessor)
        finally:
            self._live_ward_profile=None
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
        caster_source=self._actor(caster).source.source_id
        ap_cost={"F":20,"R":30,"M":24,"A":30,"B":30}.get(caster_source)
        if ap_cost is None:
            raise UnresolvedDecision("Caster lacks verified Basic Heal repertoire")
        actor = g3._own(caster,ap_cost)
        if caster_source in ("A","B"):
            low=getattr(g3,"low_life",None)
            if low is None or low.caster!=caster:
                raise UnresolvedDecision("A/B physical proxy lacks prepared Life authority")
            low._source(caster)
            # The source-locked B mace+shield occupy both hands. The
            # existing physical proxy has no verified equipment-switch
            # executor, so a caller Boolean cannot grant a free hand.
            if caster_source=="B":
                raise UnresolvedDecision(
                    "B mace and shield occupy both hands; no native free-hand transition")
        if caster_source=="M":
            from scripts.b05_medium_priest_life_l1_l3_v0 import profile as medium_profile
            p=medium_profile(actor.level)
            if (dict(actor.source.abilities)!=p["abilities"]
                    or actor.vp_max!=p["vp_max"]
                    or "Basic Heal" not in p["prepared_prayers"]
                    or actor.focus!="Medium"):
                raise UnresolvedDecision("Caster lacks verified prepared Medium Life Basic Heal")
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
        throughput=max(0,a.regen
                       +(e.g3.regen_throughput(a.id) if e.g3 is not None else 0)
                       +self.toxins.modifier(a.id,"regen_throughput"))
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
        if a.dead and hp_before > -a.hp_max:
            # Native Step 2 Dying loss is another real death transition.
            self.venom.on_recipient_death(a.id)
        e.check()

    def schedule_hemotoxin(self, recipient, *, exposure_key,
                            actual_exposure, resistance_total=None,
                            wound_location_roll=None):
        """Legacy verified TX-HM: eligibility -> Ward -> natural result.

        A real preventive Ward stops delivery BEFORE the natural check and
        packet-specific wound-roll preflight. Without one, the old bounded
        source-attested resistance and wound-roll requirements still apply.
        """
        a=self._actor(recipient)
        if a.dead:
            raise ValueError("Dead recipient cannot receive mundane toxin")
        if actual_exposure is not True:
            raise UnresolvedDecision("No toxin without verified delivery")
        if not isinstance(exposure_key,str) or not exposure_key:
            raise ValueError("Stable exposure key required")
        if exposure_key in self.toxins.exposure_ids:
            raise ValueError("Toxin exposure key already processed")
        if any(t["key"]==exposure_key for t in self.short_toxins):
            raise ValueError("Duplicate toxin exposure")
        # Apply the shared printed-grade one-instance gate BEFORE any Ward
        # or natural resistance. This legacy profile is Moderate: an
        # existing Moderate (unified or legacy) wins an equal-grade tie.
        prior=self.toxins.active(recipient)
        legacy=next((t for t in self.short_toxins
                     if t["recipient"]==recipient and t["left"]>0),None)
        if (prior is not None and prior["grade"]=="Moderate") or legacy is not None:
            active_key=prior["key"] if prior is not None else legacy["key"]
            self.toxins.exposure_ids.add(exposure_key)
            self.e.log("g4_toxin_ignored",recipient=recipient,profile="TX-HM",
                       key=exposure_key,active=active_key,
                       reason="equal_or_lower_printed_grade")
            return {"outcome":"ignored","active":active_key}
        # A valid legacy Moderate exposure can replace a unified Minor
        # only AFTER Ward eligibility and an independent successful
        # natural-result/wound-roll preflight. A Ward instead consumes
        # this higher-grade candidate and preserves the original Minor.
        if self.venom.intercept(recipient,"Moderate"):
            self.toxins.exposure_ids.add(exposure_key)
            self.e.log("g4_toxin_prevented",recipient=recipient,
                       profile="TX-HM",key=exposure_key,
                       source="venom_endurance:ward")
            self.e.check()
            return {"outcome":"prevented"}
        if type(resistance_total) is not int:
            raise UnresolvedDecision("Explicit natural resistance result required")
        # Precommitted actual d20 is available if a later packet crosses 0.
        # This avoids silently consuming an overdue Step 3 packet while an
        # unresolved location choice interrupts an already-paid G0 Step 2.
        if type(wound_location_roll) is not int or not 1<=wound_location_roll<=20:
            raise UnresolvedDecision("Provide real possible-crossing wound-location d20")
        t={"key":exposure_key,"recipient":recipient,
           "left":3 if resistance_total>=12 else 5,
           "phase":0,"applied":0,"wound_location_roll":wound_location_roll}
        if prior is not None:
            self.toxins._expire(prior,"higher_printed_grade_replaced")
        self.short_toxins.append(t)
        self.e.log("g4_toxin_scheduled",recipient=recipient,profile="TX-HM",
                   key=exposure_key,ticks=t["left"],resistance_total=resistance_total)

    def _toxin_step(self,t):
        if t["left"]==0:
            return
        number=t["applied"]+1
        if not self._actor(t["recipient"]).dead:
            # The legacy clock owns this actual tick. Endurance may cover
            # its HP packet, never create a parallel unified TX-HM schedule.
            if not self.venom.prevent_legacy_hemotoxin(t):
                self.apply_damage(t["recipient"],(DamagePacket("hp","Toxin",1),),
                                  event_key=f"toxin:{t['key']}:{number}",
                                  cause="TX-HM:scheduled_hp_tick",
                                  wound_location_roll=t["wound_location_roll"])
        t["applied"]=number
        t["left"]-=1
        self.e.log("g4_toxin_tick",recipient=t["recipient"],
                   profile="TX-HM",key=t["key"],remaining=t["left"])
        if t["left"]==0:
            self.venom.on_legacy_hemotoxin_end(t)

    def on_turn_start(self,actor_id):
        """Step 3 after real G0 regeneration, before establishing turn AP."""
        for t in self.short_toxins:
            if t["recipient"]==actor_id and t["left"]:
                self._toxin_step(t)
        self.toxins.on_turn_step3(actor_id)
        self.venom.on_turn_step3(actor_id)

    def advance_exploration(self,seconds):
        """Advance the shared G4.2 chronology; never create a phantom turn."""
        return self.clock.advance_exploration(seconds)
