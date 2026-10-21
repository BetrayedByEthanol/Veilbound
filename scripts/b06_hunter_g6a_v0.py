"""B06 G6-A: source-attested Hunter natural melee, Pounce and Horn Drive.

The G5 adapter remains the owner of paid ordinary attacks. G1 owns the
Charge/footprint commitment; G4 owns packets and injuries; G4.4 owns venom.
Only an explicitly declined optional-response policy is executable here.
No general Grapple, AI policy, multi-square victim, or CR is implied.
"""
from copy import deepcopy

from scripts.b06_encounter_state_v0 import Trigger, UnresolvedDecision
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee, _face
from scripts.b06_wound_continuation_v0 import _actor_state


class HunterCombat(SourceMelee):
    """One encounter-wide G5/G6 adapter; install before any attack sequence."""

    def __init__(self, encounter, *, scene_exit=None):
        super().__init__(encounter, scene_exit=scene_exit)
        self._g6_pounce_authorized = False

    def _hunter(self, hunter_id, target_id):
        e = self.e
        if (hunter_id not in e.actors or target_id not in e.actors
                or hunter_id == target_id):
            raise ValueError("Distinct existing Hunter and prey required")
        h, t = e.actors[hunter_id], e.actors[target_id]
        if (h.source.source_id != "B06-EN-03" or h.team == t.team
                or h.dead or h.hp <= 0 or t.dead or len(t.occupied) != 1
                or t.source.source_id not in ("A", "B", "R", "F")):
            raise UnresolvedDecision("G6 requires living Hunter against eligible one-square PC")
        if e.current != hunter_id or e.pending_regeneration is not None:
            raise ValueError("Hunter action must occur on ready own turn")
        return h, t

    @staticmethod
    def _ability(actor, name):
        abilities = dict(actor.source.abilities)
        answer = abilities.get(name, abilities.get(name.lower()))
        if type(answer) is not int:
            raise UnresolvedDecision("Source-backed " + name + " modifier required")
        return answer

    def pending_attack_slots(self, actor_id=None):
        pending = list(super().pending_attack_slots(actor_id))
        for ev in self.e.ledger:
            if ev["kind"] != "g6_pounce_attested":
                continue
            detail = ev["detail"]
            if actor_id is not None and detail["attacker"] != actor_id:
                continue
            index = detail["action_index"]
            if not any(x["kind"] in ("g6_pounce_resolved", "g6_pounce_cancelled")
                       and x["detail"].get("action_index") == index
                       for x in self.e.ledger[ev["index"]+1:]):
                pending.append({"attacker": detail["attacker"],
                                "declaration_index": ev["index"],
                                "slot": 0, "action_index": index})
        return tuple(pending)

    def assert_movement_allowed(self, actor_id):
        super().assert_movement_allowed(actor_id)
        if (self.e.current == actor_id and
                any(x["attacker"] == actor_id and
                    self.e.ledger[x["declaration_index"]]["kind"] == "g6_pounce_attested"
                    for x in self.pending_attack_slots(actor_id))):
            raise UnresolvedDecision("Resolve source-paid Pounce before new movement")

    def begin_pounce(self, hunter_id, target_id, route, *, defense="take_hit",
                     final_target_id=None):
        """Execute exactly the caller's G1 route, then attest its paid Bite.

        Never manufacture a second Physical Action or defense assignment.
        A failed route remains a live G1 Pounce until explicitly aborted.
        """
        self._hunter(hunter_id, target_id)
        self.assert_sequence_declaration_allowed(hunter_id)
        e = self.e
        route = tuple(tuple(step) for step in route)
        if not route:
            raise ValueError("Pounce requires explicitly supplied translated steps")
        self._g6_pounce_authorized = True
        try:
            e.g1.start_pounce(hunter_id, target_id)
            for step in route:
                if not e.g1.step(hunter_id, step):
                    raise UnresolvedDecision("Hunter approach interrupted; explicitly abort Pounce")
            legal = e.g1.pounce_contact(defense=defense,
                                        final_target_id=final_target_id)
        finally:
            self._g6_pounce_authorized = False
        # G1 itself records committed but canceled contact; never roll Bite.
        if not legal:
            raise UnresolvedDecision("G1 Pounce attack response canceled; no Bite or Balance")
        target_id = final_target_id or target_id
        contact = next((x for x in reversed(e.ledger)
                        if x["kind"] == "g1_pounce_contact_result"
                        and x["detail"].get("hunter") == hunter_id
                        and x["detail"].get("target") == target_id), None)
        bite = next((x for x in reversed(e.ledger)
                     if x["kind"] == "g1_pounce_bite_committed"
                     and x["detail"].get("hunter") == hunter_id
                     and x["detail"].get("target") == target_id), None)
        if (contact is None or bite is None
                or contact["detail"]["legal_after_responses"] is not True
                or contact["index"] < bite["index"]):
            raise UnresolvedDecision("Missing G1 Pounce contact/commitment provenance")
        paid = [x for x in e.ledger[:bite["index"]]
                if x["kind"] == "action_committed"
                and x["round"] == e.round and x["turn"] == hunter_id
                and x["detail"].get("actor") == hunter_id
                and x["detail"].get("label") in ("g1:pounce:cutoff", "g1:pounce:bite")]
        guards = [x for x in e.ledger[bite["index"]+1:contact["index"]]
                  if x["kind"] == "defense_assigned"
                  and x["detail"].get("actor") == target_id
                  and x["detail"].get("attack_key") ==
                  f"G1-pounce:{hunter_id}:{target_id}"]
        if len(paid) != 1 or len(guards) != 1 or guards[0]["detail"]["defense"] != defense:
            raise UnresolvedDecision("Pounce must bind exactly one genuine AP/defense debit")
        action, guard = paid[0], guards[0]
        e.log("g6_pounce_attested", attacker=hunter_id, target=target_id,
              action_index=action["index"], defense_index=guard["index"],
              contact_index=contact["index"], bite_index=bite["index"],
              attacker_source=e.actors[hunter_id].source.digest,
              target_source=e.actors[target_id].source.digest)
        return {"attestation": len(e.ledger)-1,
                "action_index": action["index"],
                "defense_index": guard["index"],
                "contact_index": contact["index"],
                "attacker": hunter_id, "target": target_id}

    def resolve_pounce(self, receipt, *, attack_face, damage_face=None,
                       confirmation_face=None, critical_dice=(),
                       wound_location_roll=None, venom_resistance_die=None,
                       venom_resistance_modifier=0, balance_hunter_face=None,
                       balance_defender_face=None, balance_ability=None):
        """One original Bite response, then an independent post-damage Balance."""
        e = self.e
        if (type(receipt) is not dict or
                type(receipt.get("attestation")) is not int or
                not 0 <= receipt["attestation"] < len(e.ledger)):
            raise UnresolvedDecision("G6 authentic Pounce receipt required")
        att = e.ledger[receipt["attestation"]]
        if att["kind"] != "g6_pounce_attested":
            raise UnresolvedDecision("Not a G6 Pounce source attestation")
        d = att["detail"]
        hunter, target = d["attacker"], d["target"]
        if any(receipt.get(k) != d[k] for k in (
                "attacker", "target", "action_index", "defense_index", "contact_index")):
            raise UnresolvedDecision("Mutable Pounce receipt disagrees with authoritative ledger")
        h, t = self._hunter(hunter, target)
        if (att["round"] != e.round or att["turn"] != hunter
                or not self._contact(hunter, target)
                or any(str(x).lower() == "prone" for x in h.conditions)
                or any(str(x).lower() == "prone" for x in t.conditions)):
            raise UnresolvedDecision("Pounce Bite no longer legal at original frontal posture")
        action = e.ledger[d["action_index"]]
        contact = e.ledger[d["contact_index"]]
        guard = e.ledger[d["defense_index"]]
        bite = e.ledger[d["bite_index"]]
        if (action["kind"] != "action_committed"
                or action["round"] != e.round or action["turn"] != hunter
                or action["detail"].get("actor") != hunter
                or action["detail"].get("action_class") != "physical"
                or action["detail"].get("label") not in ("g1:pounce:cutoff", "g1:pounce:bite")
                or bite["kind"] != "g1_pounce_bite_committed"
                or bite["detail"].get("profile") != "B06-AT-06"
                or bite["detail"].get("ap_spent") != h.physical_ap
                or contact["kind"] != "g1_pounce_contact_result"
                or contact["detail"].get("legal_after_responses") is not True
                or guard["kind"] != "defense_assigned"
                or guard["detail"].get("attack_key") != f"G1-pounce:{hunter}:{target}"
                or guard["detail"].get("actor") != target):
            raise UnresolvedDecision("Pounce provenance invalid before roll")
        if any(x["kind"] in ("action_committed", "turn_end", "round_begin",
                              "g1_movement_step", "g6_pounce_resolved")
               and (x["kind"] != "g1_movement_step" or
                    x["detail"].get("actor") == hunter)
               for x in e.ledger[att["index"]+1:]):
            raise UnresolvedDecision("Pounce source action no longer live")
        if not any(x["declaration_index"] == att["index"]
                   for x in self.pending_attack_slots(hunter)):
            raise ValueError("Pounce has already resolved or canceled")
        defense = guard["detail"]["defense"]
        value = guard["detail"]["defense_value"]
        if t.hp <= 0 and defense != "take_hit":
            # Ordinary G5 retains a paid defense, falling back to Take Hit.
            defense, value = "take_hit", None
        elif (defense == "guard" and
              (not t.ready_guard or not t.guard_instrument)):
            # A Guard committed at contact is not proof that it remains
            # wielded/ready after intervening legal response effects.
            # Match G5: retain the paid slot until an authored fallback.
            raise UnresolvedDecision(
                "Changed Guard requires native defensive fallback")
        attack_face = _face(attack_face, 20, "Pounce Bite")
        bonus = 6
        total = attack_face + bonus
        hit = attack_face != 1 and (
            defense == "take_hit" or attack_face == 20 or total > value)
        if attack_face == 20:
            confirmation_face = _face(confirmation_face, 20, "Pounce confirmation")
        elif confirmation_face is not None:
            raise ValueError("Confirmation without natural 20")
        critical = "normal"
        if hit and attack_face == 20:
            critical = ("devastating" if confirmation_face == 20 else "critical"
                        if defense == "take_hit" or (
                            confirmation_face != 1 and
                            confirmation_face + bonus > value) else "strong")
        expected = {"normal": 0, "strong": 1,
                    "critical": 2, "devastating": 2}[critical]
        if type(critical_dice) not in (tuple, list) or len(critical_dice) != expected:
            raise ValueError("Pounce critical dice count mismatched")
        for face in critical_dice:
            _face(face, 4, "Pounce critical")
        venom_exposure_key=None
        if hit:
            _face(damage_face, 6, "Pounce Bite damage")
            predicted=e.g4.preflight_profile_hit(
                hunter, target, "B06-AT-06", die_face=damage_face,
                critical=critical, critical_dice=tuple(critical_dice),
                wound_location_roll=wound_location_roll)
            venom_exposure_key=f"g6:pounce:{e.seed}:{d['action_index']}"
            if predicted["hp_after"] > -t.hp_max:
                e.g4.venom.validate_exposure_key(venom_exposure_key)
            _, _, packets = e.g4._profile_hit_packets(
                hunter, target, "B06-AT-06", die_face=damage_face,
                critical=critical, critical_dice=tuple(critical_dice))
            if (e.g4._mitigate_hp(t, packets[0]) > 0 and
                    predicted["hp_after"] > -t.hp_max and
                    e.g4.venom.bite_resistance_required(target) and
                    venom_resistance_die is None):
                raise UnresolvedDecision("Potential puncture requires committed venom resistance d20")
        elif damage_face is not None:
            raise ValueError("A missed Pounce cannot roll Bite damage")
        if venom_resistance_die is not None:
            _face(venom_resistance_die, 20, "venom resistance")
        if type(venom_resistance_modifier) is not int:
            raise ValueError("Venom modifier must be source-attested integer")
        # Predict the post-Bite condition before the first irreversible
        # roll log. A Dying prey is knocked Prone without a contest, and a
        # dead prey cannot be subjected to one. Neither case should demand
        # invented Balance d20s or a never-used contest ability.
        post_bite_hp = predicted["hp_after"] if hit else t.hp
        contest_required = post_bite_hp > 0
        defender_modifier = None
        if contest_required:
            if balance_ability not in ("Strength", "Agility"):
                raise UnresolvedDecision("Precommitted eligible Balance method required")
            _face(balance_hunter_face, 20, "Pounce pressure")
            _face(balance_defender_face, 20, "Pounce resistance")
            defender_modifier = self._ability(t, balance_ability)
        e.log("g6_pounce_melee_roll", action_index=d["action_index"],
              attacker=hunter, target=target, attack_face=attack_face,
              source_bonus=bonus, attack_total=total, defense=defense,
              defense_value=value, confirmation_face=confirmation_face,
              critical=critical, hit=hit)
        damage = None
        if hit:
            damage = e.g4.apply_profile_hit(
                hunter, target, "B06-AT-06", die_face=damage_face,
                confirmed_hit=True, critical=critical,
                critical_dice=tuple(critical_dice),
                wound_location_roll=wound_location_roll)
            # This is still the latest G4 hit; append no intermediate
            # provenance event before G4.4 has adjudicated this one exposure.
            if not t.dead:
                damage["venom"] = e.g4.venom.apply_bite(
                    hunter, target, profile_hit_index=next(
                        x["index"] for x in reversed(e.ledger)
                        if x["kind"] == "g4_profile_hit"),
                    exposure_key=venom_exposure_key,
                    resistance_die=venom_resistance_die,
                    resistance_modifier=venom_resistance_modifier)
            self.bridge.seen_actions.add(d["action_index"])
            e.log("g45_attested_hit",
                  source_event=f"g6:pounce:source:{e.seed}:{d['action_index']}",
                  attacker=hunter, target=target, profile="B06-AT-06",
                  action_index=d["action_index"],
                  sequence_declaration_index=att["index"],
                  declared_profile_index=0,
                  contact_reference=f"g1:pounce:contact:{d['contact_index']}",
                  defense_reference=f"g0:defense:{d['defense_index']}",
                  attacker_source=h.source.digest,
                  target_source=t.source.digest,
                  critical=critical, actual_result=deepcopy(damage),
                  target_state=_actor_state(t))
        balance_result = "not_applicable"
        if (not t.dead and self._contact(hunter, target)
                and not any(str(x).lower() == "prone" for x in t.conditions)
                and h.hp > 0):
            if t.hp <= 0:
                balance_result = "automatic_unable_to_contest"
                t.conditions.append("Prone")
            else:
                pressure = balance_hunter_face + 4
                resistance = (balance_defender_face + defender_modifier +
                              e.g4.toxins.modifier(target, "muscular_strength")
                              if balance_ability == "Strength" else
                              balance_defender_face + defender_modifier)
                balance_result = "prone" if pressure > resistance else "held"
                e.log("g6_pounce_balance", attacker=hunter, target=target,
                      pressure_face=balance_hunter_face, pressure=pressure,
                      resistance_face=balance_defender_face,
                      resistance_ability=balance_ability,
                      resistance=resistance, outcome=balance_result)
                if pressure > resistance:
                    t.conditions.append("Prone")
            if balance_result in ("prone", "automatic_unable_to_contest"):
                e.log("g6_pounce_prone", target=target, attacker=hunter,
                      cause=balance_result)
        e.log("g6_pounce_resolved", action_index=d["action_index"],
              attacker=hunter, target=target, bite="hit" if hit else "miss",
              damage=deepcopy(damage), balance=balance_result,
              source_contact=d["contact_index"])
        e.check()
        return {"bite": "hit" if hit else "miss", "critical": critical,
                "damage": deepcopy(damage), "balance": balance_result,
                "action_index": d["action_index"]}

    def pounce(self, hunter_id, target_id, route, *, defense="take_hit", **dice):
        receipt = self.begin_pounce(hunter_id, target_id, route, defense=defense)
        return self.resolve_pounce(receipt, **dice)

    def horn_drive(self, hunter_id, target_id, *, pressure_face,
                   resistance_face, spontaneous_policy="decline_all"):
        """One paid non-damaging head-forward Shove; no free Horn Bash."""
        h, t = self._hunter(hunter_id, target_id)
        self.assert_sequence_declaration_allowed(hunter_id)
        e = self.e
        if (spontaneous_policy != "decline_all"
                or e.g1.pounce is not None):
            raise UnresolvedDecision("Only bounded declared Horn Drive response is supported")
        if (not self._contact(hunter_id, target_id)
                or any(str(x).lower() == "prone" for x in t.conditions)):
            raise ValueError("Horn Drive requires a standing front-adjacent prey")
        pressure_face = _face(pressure_face, 20, "Horn Drive pressure")
        resistance_face = _face(resistance_face, 20, "Horn Drive resistance")
        pressure = pressure_face + self._ability(h, "Strength")
        resist = (resistance_face + self._ability(t, "Strength") + 2 +
                  e.g4.toxins.modifier(target_id, "muscular_strength"))
        forward = (h.occupied[0][0]-h.occupied[1][0],
                   h.occupied[0][1]-h.occupied[1][1])
        destination = (t.occupied[0][0]+forward[0], t.occupied[0][1]+forward[1])
        if any(r.trigger_key == f"g6:horn_drive:{hunter_id}:{target_id}"
               for r in e.reservations):
            raise UnresolvedDecision("Prepared Close-Contact response requires separate executor")
        # A successful Shove advances the Hunter's entire rigid body.
        # That exit can provoke THIRD-PARTY Movement Opportunities even
        # though the victim's forced shift itself is not a G1 MP step.
        # G6-A has no source-attested Opportunity attack executor for that
        # compound movement. Refuse this contested advance BEFORE AP,
        # response windows or geometry mutate; never silently teleport
        # the Hunter past an opponent's live threat.
        if pressure > resist and e.g1.valid_footprint(t, (destination,)):
            old_target=t.occupied
            next_h=(old_target[0], h.occupied[0])
            t.occupied=(destination,)
            try:
                advance_legal=e.g1.valid_footprint(h, next_h)
            finally:
                t.occupied=old_target
            if advance_legal:
                departure=set(h.occupied)-set(next_h)
                # spend_ap() starts a fresh G1 movement segment. Inspect
                # all threats, even those marked provoked in the previous
                # segment: _threats() alone would use stale segment flags.
                third_party=tuple(
                    oid for oid in e.order
                    if oid not in (hunter_id, target_id)
                    and e.actors[oid].team != h.team
                    and any(e.g1.threatens(oid, square)
                            for square in departure))
                if third_party:
                    raise UnresolvedDecision(
                        "Third-party Movement Opportunities require a "
                        "source-attested Horn Drive advance executor: "
                        + ", ".join(third_party))
        e.spend_ap(hunter_id, "physical", label="g6:horn_drive")
        action_index = next(x["index"] for x in reversed(e.ledger)
                            if x["kind"] == "action_committed"
                            and x["detail"].get("actor") == hunter_id)
        e.log("g6_horn_drive_committed", action_index=action_index,
              hunter=hunter_id, target=target_id,
              pressure_face=pressure_face, resistance_face=resistance_face,
              policy=spontaneous_policy)
        tr = Trigger(f"g6:horn_drive:{hunter_id}:{target_id}", hunter_id, target_id)
        def recheck(encounter,trigger):
            trigger.legal=(h.hp>0 and not h.dead and not t.dead
                           and self._contact(hunter_id,target_id))
        valid = e.response_window(tr,on_interception=lambda *args: None,
                                  spontaneous=(),after_interceptions=recheck)
        if not valid:
            e.log("g6_horn_drive_resolved",action_index=action_index,
                  result="contact_lost",ap_refunded=False)
            return {"outcome": "contact_lost", "action_index": action_index}
        moved = False
        if pressure > resist and e.g1.valid_footprint(t, (destination,)):
            original_target = t.occupied
            t.occupied = (destination,)
            next_h = (original_target[0], h.occupied[0])
            if e.g1.valid_footprint(h, next_h):
                h.occupied = next_h
                moved = True
                if e.g2 is not None:
                    e.g2.on_position_change(hunter_id)
                    e.g2.on_position_change(target_id)
            else:
                t.occupied = original_target
        outcome = "shoved" if moved else (
            "blocked_destination" if pressure > resist else "resisted")
        e.log("g6_horn_drive_resolved", action_index=action_index,
              hunter=hunter_id, target=target_id, pressure=pressure,
              resistance=resist, outcome=outcome,
              target_position=t.occupied, hunter_body=h.occupied)
        e.check()
        return {"outcome": outcome, "action_index": action_index}


def run_i3(*, seed=606):
    """Two real rounds: sourced Hunter misses, bites, venom, then A retreats.

    One L3 Low Life Priest physical proxy, not a completed diverse-party pack.
    No unearned player offensive profiles or automatic Hunter CR.
    """
    from scripts.b06_encounter_state_v0 import (
        Encounter, RegenerationChoice, enemy_actor, party_actor)
    from scripts.b06_movement_v0 import GridMovement
    from scripts.b06_spells_v0 import SpellState
    from scripts.b06_damage_v0 import DamageState
    from scripts.b06_soldier_sentry_g5_v0 import SceneExit

    h=enemy_actor("B06-EN-03","hunter","enemy",
                  occupied=((3,2),(4,2)))
    front=party_actor("A",3,"front","party",occupied=((2,2),))
    e=Encounter([h,front],{"hunter":30,"front":20},seed=seed,
                scenario="B06-I3:frontal-pursuit",
                objective="front_reaches_verified_exit",
                policy="declared_hunter_two_round_bite_then_declined_opportunity")
    GridMovement(e,width=8,height=5,scene_id="G6-open-corridor")
    SpellState(e)
    DamageState(e)
    e.begin_round()
    exit_policy=SceneExit(e.scenario,e.g1.scene_id,e.objective,
                          "front",(0,2),"G6:open-corridor:front-exit")
    scene=HunterCombat(e,scene_exit=exit_policy)
    scene.bridge.start_next_turn(RegenerationChoice())
    first=scene.declare("hunter","front",
                        profiles=("B06-AT-04",),defenses=("guard",))
    first_result=scene.resolve(first,0,attack_face=1)
    scene.bridge.end_current_turn()
    scene.bridge.start_next_turn(RegenerationChoice())
    scene.bridge.end_current_turn()
    scene.bridge.begin_next_round()
    scene.bridge.start_next_turn(RegenerationChoice())
    second=scene.declare("hunter","front",
                         profiles=("B06-AT-04",),defenses=("take_hit",))
    second_result=scene.resolve(second,0,attack_face=10,damage_face=1,
                                venom_resistance_die=1)
    scene.bridge.end_current_turn()
    scene.bridge.start_next_turn(RegenerationChoice(hp=2))
    for _ in range(2):
        if not e.g1.step("front",(-1,0),responses=lambda eligible: ()):
            raise UnresolvedDecision("Source-declared retreat route was interrupted")
    scene.withdraw("front")
    scene.bridge.end_current_turn()
    report=scene.report()
    if report["ending"]!="withdrawal_attested":
        raise AssertionError("Source-authored I3 exit evidence did not complete")
    report["first_bite"]=first_result
    report["second_bite"]=second_result
    return report
