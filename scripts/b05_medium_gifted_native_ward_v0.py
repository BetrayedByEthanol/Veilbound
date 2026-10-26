"""B04/B05 Medium Gifted source-bound Ward conduit native G0/G1/G4 adapter.

Only actual G4 post-mitigation packets may consume a Pulse. This is bounded
L1-3 native protection, not a general Conduit catalogue or Focus certificate.
"""
from scripts.b05_medium_gifted_l1_l3_v0 import profile
from scripts.b05_high_gifted_amplification_v0 import PILOT_LINKS
from scripts.b05_medium_gifted_conduit_design_v0 import (
    Conduit, EXPRESSION, PHYSICAL_HP,
)
from scripts.b06_encounter_state_v0 import (
    Actor, Source, UnresolvedDecision, _fingerprint,
)

PATH = "scripts/b05_medium_gifted_l1_l3_v0.py"


def gifted_actor(level, actor_id, team, *, occupied):
    """Build the exact Medium source sheet, not a proxy with invented VP."""
    p = profile(level)
    gear = tuple(sorted((name, "worn" if name == "Leather armor" else
                         "wielded" if name == "Dagger" else "carried")
                        for name in p["equipment_sp"]))
    src = Source(PATH, "MG", _fingerprint(PATH), "STRUCTURAL_B05_ONLY",
                 tuple(sorted(p["abilities"].items())),
                 tuple(sorted(p["weapon_training"].items())),
                 gear, (), f"L{level}-medium-gifted-ward")
    a = p["abilities"]
    actor = Actor(actor_id, team, src, level, "Medium", p["initiative"],
                  a["Awareness"], a["Agility"], p["hp_max"], p["vigor_max"],
                  p["vp_max"], p["hp_max"], p["vigor_max"], p["vp_max"], 0, 0,
                  p["normal_regen_throughput"], p["turn_ap"],
                  p["physical_action_ap"], p["projection_action_ap"],
                  "Dagger", p["dagger_guard_defense"], p["guard_capacity"],
                  occupied=tuple(tuple(c) for c in occupied))
    actor.validate()
    return actor


def _source(actor):
    if actor.source.source_id != "MG" or actor.level not in (1, 2, 3):
        raise UnresolvedDecision("Only authored L1-3 Medium Gifted")
    expected = gifted_actor(actor.level, actor.id, actor.team,
                            occupied=actor.occupied)
    if (actor.source != expected.source or actor.focus != "Medium" or
            (actor.initiative_bonus, actor.awareness, actor.agility,
             actor.hp_max, actor.vigor_max, actor.vp_max, actor.ap_total,
             actor.physical_ap, actor.projection_ap, actor.regen,
             actor.guard_instrument, actor.guard_value, actor.guard_capacity) !=
            (expected.initiative_bonus, expected.awareness, expected.agility,
             expected.hp_max, expected.vigor_max, expected.vp_max,
             expected.ap_total, expected.physical_ap, expected.projection_ap,
             expected.regen, expected.guard_instrument, expected.guard_value,
             expected.guard_capacity)):
        raise UnresolvedDecision("Medium Gifted native source sheet changed")
    return profile(actor.level)


class MediumGiftedWardNative:
    """Single pilot caster's real committed VP, state and G4 Ward pulses.

    Preview is pure for G5 preflight and G4. Commit is restricted to the
    exact applying G4 event and logs the prevention before HP/Vigor loss.
    """

    def __init__(self, encounter, caster):
        if (encounter.g1 is None or encounter.g3 is None or
                encounter.g4 is None or encounter.g4.medium_gifted is not None):
            raise ValueError("Requires unclaimed native G1/G3/G4")
        if caster not in encounter.actors:
            raise ValueError("Unknown Ward caster")
        _source(encounter.actors[caster])
        self.e, self.caster = encounter, caster
        self.conduits = []
        self.next_serial = 0
        self.window = None
        self.emotion = None
        self.released_window = None
        self.used_original_events = set()
        encounter.g4.medium_gifted = self
        encounter.log("b05_medium_ward_installed", caster=caster,
                      source_digest=encounter.actors[caster].source.digest)

    def _actor(self):
        actor = self.e.actors[self.caster]
        _source(actor)
        return actor

    def _latest_turn_key(self):
        return next((v["index"] for v in reversed(self.e.ledger)
                     if v["kind"] == "turn_resources" and
                     v["detail"].get("actor") == self.caster), None)

    def _live_window(self):
        return (self.window is not None and self._latest_turn_key() == self.window)

    def _retune(self):
        expr = EXPRESSION.get(self.emotion)
        for c in self.conduits:
            c.status = ("Active" if expr is not None and
                        PILOT_LINKS[self.emotion][:2] == expr[:2]
                        else "Dormant")

    def establish_emotion(self, emotion):
        """Actual G0 Step 5; changing an active emotion is not free."""
        a = self._actor()
        key = self._latest_turn_key()
        if (self.e.current != self.caster or
                self.e.pending_regeneration is not None or key is None or
                key == self.window or a.hp <= 0 or a.dead):
            raise ValueError("One new Step-5 emotion establishment per live turn")
        if emotion is not None and emotion not in PILOT_LINKS:
            raise ValueError("Unknown permanent emotion link")
        forbidden = ("action_committed", "vp_transition", "g1_movement_step",
                     "g1_allied_transit_step", "g6_stand_started",
                     "g1_movement_mp_reserved")
        if any(v["index"] > key and v["kind"] in forbidden and
               v["detail"].get("actor") == self.caster
               for v in self.e.ledger):
            raise ValueError("Emotion establishment precedes movement and actions")
        self.window, self.emotion = key, emotion
        self._retune()
        self.e.log("b05_medium_emotion_established", caster=self.caster,
                   window=key, emotion=emotion)

    def _on_turn(self, *, require_ap=True):
        a = self._actor()
        if (self.e.current != self.caster or
                self.e.pending_regeneration is not None or
                not self._live_window() or a.hp <= 0 or a.dead):
            raise ValueError("Conduit changes require conscious own-turn Emotion Window")
        if (self.e.g5 is not None and
                self.e.g5.pending_attack_slots(self.caster)):
            raise UnresolvedDecision("Finish pending G5 attack before Conduit changes")
        if require_ap and a.ap_remaining < 24:
            raise ValueError("Insufficient native General Tempo AP")
        return a

    def place(self, grade):
        a = self._on_turn()
        if type(grade) is not int or grade not in (1, 2, 3):
            raise ValueError("Only Grade I-III")
        if (len(self.conduits) >= (2 if a.level == 3 else 1) or
                self.released_window == self.window or
                a.vp_available < grade):
            raise ValueError("Slot, lockout or committed VP unavailable")
        self.e.spend_ap(self.caster, "general", label="b05:medium_ward_place")
        self.e.spend_vp(self.caster, grade, mode="committed",
                        label="b05:medium_ward_place")
        self.next_serial += 1
        c = Conduit(self.next_serial, "Ward", "self", grade)
        self.conduits.append(c)
        self._retune()
        self.e.log("b05_medium_ward_placed", caster=self.caster,
                   serial=c.serial, grade=grade, window=self.window,
                   status=c.status)
        return c.serial

    def reconduct(self, serial, grade):
        a = self._on_turn()
        if type(serial) is not int or type(grade) is not int or grade not in (1, 2, 3):
            raise ValueError("Exact serial and new Grade required")
        c = next((c for c in self.conduits if c.serial == serial), None)
        if c is None or c.grade == grade:
            raise ValueError("No eligible Conduit grade change")
        delta = grade - c.grade
        if a.vp_available < 3 + max(0, delta):
            raise ValueError("Spent VP surcharge cannot use future Grade release")
        self.e.spend_ap(self.caster, "general", label="b05:medium_ward_reconduct")
        self.e.spend_vp(self.caster, 3, mode="spent",
                        label="b05:medium_ward_reconduct")
        old = c.grade
        if delta > 0:
            self.e.spend_vp(self.caster, delta, mode="committed",
                            label="b05:medium_ward_upgrade")
        c.grade = grade
        if delta < 0:
            self.e.release_vp(self.caster, -delta,
                              label="b05:medium_ward_downgrade")
        self.e.log("b05_medium_ward_reconducted", caster=self.caster,
                   serial=serial, old_grade=old, grade=grade,
                   window=self.window, pulse_window=c.pulse_window)

    def release(self, serial):
        self._on_turn(require_ap=False)  # Free voluntary release.
        if type(serial) is not int:
            raise ValueError("Owned serial required")
        c = next((c for c in self.conduits if c.serial == serial), None)
        if c is None:
            raise ValueError("No owned Ward to release")
        self.conduits.remove(c)
        self.released_window = self.window
        self.e.release_vp(self.caster, c.grade,
                          label="b05:medium_ward_voluntary_release")
        self.e.log("b05_medium_ward_ended", caster=self.caster,
                   serial=serial, reason="voluntary", returned=c.grade)

    def sync_consciousness(self, actor_id):
        if actor_id != self.caster:
            return
        a = self._actor()
        if a.hp > 0 and not a.dead:
            return
        for c in list(self.conduits):
            self.conduits.remove(c)
            self.e.release_vp(self.caster, c.grade,
                              label="b05:medium_ward_unconscious")
            self.e.log("b05_medium_ward_ended", caster=self.caster,
                       serial=c.serial, reason="unconscious_or_dead",
                       returned=c.grade)

    def _recipient(self, recipient):
        caster = self._actor()
        if recipient not in self.e.actors:
            raise ValueError("Unknown native Ward recipient")
        victim = self.e.actors[recipient]
        if len(caster.occupied) != 1 or len(victim.occupied) != 1:
            raise UnresolvedDecision("Ward native v0 cannot resolve multi-cell geometry")
        if victim.team != caster.team or recipient == self.caster:
            return False
        x, y = caster.occupied[0]
        u, v = victim.occupied[0]
        return abs(x-u) + abs(y-v) == 1

    def preview(self, recipient, packets, resolved, *, low_proposal=None):
        """Pure same-packet native G4/G5 preview, never consume a Pulse."""
        a = self._actor()
        packets, resolved = tuple(packets), tuple(resolved)
        if len(packets) != len(resolved):
            raise ValueError("Mismatched post-mitigation packets")
        result = {"remaining": resolved, "prevention": 0, "receipt": None,
                  "serial": None, "index": None}
        if (not self._live_window() or self.emotion not in EXPRESSION or
                a.hp <= 0 or a.dead):
            return result
        available = [c for c in self.conduits
                     if c.status == "Active" and c.pulse_window != self.window]
        if not available:
            return result
        victim = self.e.actors[recipient]
        for i, (p, amount) in enumerate(zip(packets, resolved)):
            if type(amount) is not int or amount < 0:
                raise ValueError("Native G4 must provide nonnegative post-mitigation")
            if not amount:
                continue
            if self.emotion == "Fear":
                eligible = (recipient == self.caster and p.resource == "hp"
                            and p.damage_type in PHYSICAL_HP
                            and p.armor_rule == "weapon")
            else:
                eligible = (p.resource == "vigor" and
                            p.damage_type == "Direct Vigor" and
                            victim.vigor > 0 and self._recipient(recipient))
            if not eligible:
                continue
            if low_proposal is not None:
                raise UnresolvedDecision("Ward/Low Life finite HP prevention ordering unauthored")
            if self.emotion == "Trust" and self.e.g3 is not None and any(
                    e.kind == "Vital Shelter" and e.recipient == recipient
                    for e in self.e.g3.effects.values()):
                raise UnresolvedDecision("Ward/Vital Shelter finite Vigor ordering unauthored")
            c = available[0]
            blocked = min(c.grade, amount)
            after = list(resolved)
            after[i] -= blocked
            return {"remaining": tuple(after), "prevention": blocked,
                    "serial": c.serial, "index": i,
                    "receipt": {"caster": self.caster,
                                "source_digest": a.source.digest,
                                "window": self.window, "emotion": self.emotion,
                                "conduit_serial": c.serial, "grade": c.grade,
                                "recipient": recipient, "packet_index": i,
                                "original_post_mitigation": amount,
                                "prevented": blocked, "remaining": after[i]}}
        return result

    def commit(self, recipient, packets, proposal, *, event_key, cause):
        """Only G4 applying its actual typed original packet may use a Pulse."""
        if (not isinstance(event_key, str) or not event_key or
                event_key in self.used_original_events or
                event_key in self.e.g4.used_events):
            raise ValueError("Ward original damage event already consumed")
        if self.e.g4._live_ward_delivery != (recipient,event_key,cause,tuple(packets)):
            raise UnresolvedDecision("Ward pulse may only commit inside exact G4 event")
        if cause.startswith("source-profile:"):
            profile_id = cause.removeprefix("source-profile:")
            source = self.e.g4._live_ward_profile
            if (source is None or source[1:] !=
                    (recipient,profile_id,tuple(packets))):
                raise UnresolvedDecision("Ward needs G4's exact native profile hit")
            attacker = source[0]
            paid = self.e.g4._live_ward_action
            if (paid is None or paid[:3] != (attacker,recipient,profile_id)
                    or type(paid[3]) is not int):
                raise UnresolvedDecision("Ward needs exact live G4.5 paid action")
            action_index = paid[3]
            if not any(ev["kind"] == "g5_melee_roll" and
                       ev["round"] == self.e.round and
                       ev["turn"] == self.e.current and
                       ev["detail"].get("attacker") == attacker and
                       ev["detail"].get("target") == recipient and
                       ev["detail"].get("profile") == profile_id and
                       ev["detail"].get("action_index") == action_index and
                       ev["detail"].get("hit") is True
                       for ev in self.e.ledger):
                raise UnresolvedDecision("Ward G5 roll disagrees with exact paid slot")
            if any(ev["kind"] in ("g45_attested_hit","g5_melee_resolved") and
                   ev["detail"].get("action_index") == action_index
                   for ev in self.e.ledger):
                raise UnresolvedDecision("Ward cannot reuse already completed G5 slot")
        elif cause == "g3:thrown_flame":
            if self.e.g4._live_flame_delivery is None:
                raise UnresolvedDecision("Ward needs a confirmed live G3 Flame")
        else:
            raise UnresolvedDecision("Ward requires an authored native delivery")
        if proposal["prevention"] <= 0 or proposal["receipt"]["recipient"] != recipient:
            raise ValueError("No eligible preflighted Ward packet")
        serial = proposal["serial"]
        c = next((x for x in self.conduits if x.serial == serial), None)
        if (c is None or c.pulse_window == self.window or
                not self._live_window() or c.status != "Active"):
            raise UnresolvedDecision("Ward state changed since native preflight")
        c.pulse_window = self.window
        self.used_original_events.add(event_key)
        self.e.log("b05_medium_ward_pulse", event_key=event_key,
                   cause=cause, **proposal["receipt"])
