"""Source-bound High Gifted L1-3 native Conjure Flame bridge.

One real G0 actor, Emotion Window, G2 physical lane/defense, G3 AP/VP
commit and G4 injury receipt. No naturally Overwhelming state, reactive
casting, general Gifted spell repertoire or independent Focus certificate.
"""
from math import ceil

from scripts.b05_high_gifted_l1_l3_v0 import profile
from scripts.b05_high_gifted_amplification_v0 import PILOT_LINKS, thrown_flame, surge_surcharge
from scripts.b06_encounter_state_v0 import Actor, Source, UnresolvedDecision, _fingerprint

PATH = "scripts/b05_high_gifted_l1_l3_v0.py"
OPTIONS = frozenset(("Potency", "Reach", "Precision"))


def gifted_actor(level, actor_id, team, *, occupied):
    """Project the exact B05 pilot sheet, not a fabricated Phase-3 proxy."""
    p = profile(level)
    gear = tuple(sorted((name, "worn" if name == "Leather armor" else
                         "wielded" if name == "Dagger" else "carried")
                        for name in p["equipment_sp"]))
    src = Source(PATH, "G", _fingerprint(PATH), "STRUCTURAL_B05_ONLY",
                 tuple(sorted(p["abilities"].items())),
                 tuple(sorted(p["weapon_training"].items())),
                 gear, (), f"L{level}-high-gifted-structural")
    a = p["abilities"]
    actor = Actor(actor_id, team, src, level, "High", p["initiative"],
                  a["Awareness"], a["Agility"], p["hp_max"], p["vigor_max"],
                  p["vp_max"], p["hp_max"], p["vigor_max"], p["vp_max"], 0, 0,
                  p["normal_regen_throughput"], p["turn_ap"],
                  p["physical_action_ap"], p["projection_action_ap"],
                  "Dagger", p["dagger_guard_defense"], p["guard_capacity"],
                  occupied=tuple(tuple(c) for c in occupied))
    actor.validate()
    return actor


def _source(actor):
    """Reconstruct and compare every combat-relevant source authority."""
    if actor.source.source_id != "G" or actor.level not in (1, 2, 3):
        raise UnresolvedDecision("Only the authored High Gifted pilot")
    original = gifted_actor(actor.level, actor.id, actor.team, occupied=actor.occupied)
    expected, actual = original.source, actor.source
    if (actual != expected or actor.focus != "High" or
            (actor.awareness, actor.agility, actor.initiative_bonus) !=
            (original.awareness, original.agility, original.initiative_bonus) or
            (actor.hp_max, actor.vigor_max, actor.vp_max, actor.ap_total,
             actor.physical_ap, actor.projection_ap, actor.regen,
             actor.guard_instrument, actor.guard_value, actor.guard_capacity) !=
            (original.hp_max, original.vigor_max, original.vp_max,
             original.ap_total, original.physical_ap, original.projection_ap,
             original.regen, original.guard_instrument, original.guard_value,
             original.guard_capacity)):
        raise UnresolvedDecision("Gifted source sheet or combat values changed")
    return profile(actor.level)


class GiftedNative:
    """One G3-hosted, encounter-bound emotion state for the Gifted pilot."""

    def __init__(self, encounter, caster):
        if encounter.g1 is None or encounter.g2 is None or encounter.g3 is None or encounter.g4 is None:
            raise ValueError("Requires actual native G1/G2/G3/G4")
        if getattr(encounter.g3, "gifted", None) is not None:
            raise ValueError("Gifted G3 host already claimed")
        if caster not in encounter.actors:
            raise ValueError("Unknown Gifted")
        self.e, self.caster = encounter, caster
        _source(encounter.actors[caster])
        self.window = None
        self.turn_key = None
        self.surge_remaining = False
        self.safe_remaining = False
        encounter.g3.gifted = self
        encounter.log("b05_gifted_native_installed", caster=caster,
                      source_digest=encounter.actors[caster].source.digest)

    def establish(self, emotion, *, natural_heightening=False, rationale=None):
        """Call exactly once after actual G0 turn resources, never per cast."""
        a = self.e.actors[self.caster]
        _source(a)
        if self.e.current != self.caster or self.e.pending_regeneration is not None:
            raise ValueError("Emotion establishment requires ready own turn")
        resources = [v for v in self.e.ledger if v["kind"] == "turn_resources"
                     and v["detail"]["actor"] == self.caster]
        if not resources:
            raise ValueError("No live G0 Emotion Establishment Step")
        turn_key = resources[-1]["index"]
        if turn_key == self.turn_key:
            raise ValueError("An Emotion Window cannot be refreshed mid-turn")
        if any(v["kind"] in ("action_committed", "vp_transition")
               and v["detail"].get("actor") == self.caster
               and v["index"] > turn_key for v in self.e.ledger):
            raise ValueError("Emotion Establishment precedes normal actions")
        if emotion not in PILOT_LINKS and emotion is not None:
            raise ValueError("Emotion must be one of the eight permanent links")
        if type(natural_heightening) is not bool:
            raise ValueError("Natural Heightening needs explicit bool")
        if natural_heightening and (emotion is None or not isinstance(rationale, str)
                                   or not rationale.strip()):
            raise UnresolvedDecision("Heightening requires an explicit fictional basis")
        self.turn_key = turn_key
        self.window = {"emotion": emotion, "intensity": (
            "heightened" if natural_heightening else "evoked")}
        self.surge_remaining = True
        self.safe_remaining = natural_heightening
        self.e.log("b05_gifted_emotion_established", caster=self.caster,
                   window=turn_key, emotion=emotion,
                   intensity=self.window["intensity"],
                   natural_heightening=natural_heightening,
                   rationale=rationale if natural_heightening else None)

    def _ready(self):
        a = self.e.actors[self.caster]
        p = _source(a)
        if (self.e.current != self.caster or self.e.pending_regeneration is not None
                or self.window is None or
                next((v["index"] for v in reversed(self.e.ledger)
                      if v["kind"] == "turn_resources"
                      and v["detail"]["actor"] == self.caster), None)
                   != self.turn_key):
            raise ValueError("No active source-bound Gifted Emotion Window")
        if a.hp <= 0 or a.dead:
            raise ValueError("Incapacitated Gifted cannot cast")
        if self.window["emotion"] != "Joy":
            raise ValueError("Conjure Flame requires currently Active Joy")
        if set(self.e.g2.wielded[self.caster]) != {"Dagger"}:
            raise UnresolvedDecision("Authored wielded dagger/hand state changed")
        return a, p

    def cast_flame(self, target, *, tier, face, vigor_die, defense="take_hit",
                   aware=False, hand_available=False, safe=None, surge=None,
                   potency_die=None, confirmation_face=None, critical_dice=(),
                   exposures=(), target_cell=None, wound_location_roll=None,
                   prone_cover_policy=(), prone_dodge_feasible=False):
        """Commit a fully native G2/G3/G4 delivery, without synthetic rolls.

        The only permitted Amp categories on the exact Thrown Primary profile
        are Potency/Reach/Precision. Risky Overwhelming has no legal v0 entry.
        """
        a, p = self._ready()
        if (type(tier) is not int or tier not in (1, 2)
                or tier > p["max_used_tier"]):
            raise ValueError("Inaccessible Flame Used Tier")
        t = thrown_flame(tier)
        selected = tuple(x for x in (safe, surge) if x is not None)
        if (len(set(selected)) != len(selected) or
                any(x not in OPTIONS or x not in t.choices for x in selected)):
            raise ValueError("Duplicate/unsupported Amplification")
        if safe is not None and not self.safe_remaining:
            raise ValueError("No naturally Heightened safe Step available")
        if surge is not None and not self.surge_remaining:
            raise ValueError("One Surge per Emotion Window")
        if hand_available is not True:
            raise ValueError("Actual free hand required for Thrown Flame")
        if type(face) is not int or not 1 <= face <= 20:
            raise ValueError("Actual attack d20 required")
        if type(vigor_die) is not int or not 1 <= vigor_die <= 8:
            raise ValueError("Actual Vigor d8 required")
        if ("Potency" in selected) != (potency_die is not None):
            raise ValueError("One real extra d8 iff Potency selected")
        if potency_die is not None and (type(potency_die) is not int or not 1 <= potency_die <= 8):
            raise ValueError("Actual Potency d8 required")
        if defense not in ("take_hit", "dodge", "guard") or (defense != "take_hit" and not aware):
            raise ValueError("Actual aware legal projectile defense required")
        if type(critical_dice) not in (tuple, list):
            raise ValueError("Critical dice must be explicit")
        critical_dice = tuple(critical_dice)
        attack_bonus = p["thrown_flame_attack_bonus"] + int("Precision" in selected)
        if face == 20:
            if type(confirmation_face) is not int or not 1 <= confirmation_face <= 20:
                raise UnresolvedDecision("Natural-20 confirmation required for complete native hit")
        elif confirmation_face is not None:
            raise ValueError("Confirmation only on natural 20")
        max_range = t.max_range + int("Reach" in selected)
        lane = self.e.g2.lane(self.caster, target, target_cell=target_cell,
                              exposures=exposures, range_kind="flame",
                              max_flame_squares=max_range)
        if lane.screens:
            raise UnresolvedDecision("Living screen requires full physical projectile routing")
        if any(self.e.g1.threatens(enemy.id, square)
               for enemy in self.e.actors.values() if enemy.team != a.team
               for square in a.occupied):
            raise UnresolvedDecision("Threatened casting requires live Opportunity responses")
        victim = self.e.actors[target]
        position = self.e.g2._prone_position(
            victim, lane.distance, lane.cover, prone_cover_policy)
        _, declared_def = self.e.g2._defense_value(
            victim, defense, 0, lane.cover, position_bonus=position,
            prone_dodge_feasible=prone_dodge_feasible)
        critical = ("normal" if face != 20 else
                    self.e.g3._flame_confirmation_tier(
                        confirmation_face, defense, declared_def, attack_bonus=attack_bonus))
        count = {"normal": 0, "strong": 1, "critical": 2, "devastating": 2}[critical]
        if (len(critical_dice) != count or any(
                type(x) is not int or not 1 <= x <= 4 for x in critical_dice)):
            raise ValueError("Exact confirmed critical d4 allocation required")
        fire_hp = 2 + sum(critical_dice)
        if face == 20 or (face != 1 and face + attack_bonus > declared_def):
            self.e.g4.preflight_flame_wound(
                target, wound_location_roll, fire_hp=fire_hp,
                devastating=critical == "devastating")
        surcharge = surge_surcharge(t) if surge is not None else 0
        total_vp = t.spent_vp + surcharge
        if a.vp_available < total_vp or a.ap_remaining < a.projection_ap:
            raise ValueError("Combined AP/VP unavailable; no partial cast")
        self.e.spend_ap(self.caster, "projection", label="b05:gifted_thrown_flame:T"+str(tier))
        # No user callback is accepted between preflight, payment and impact.
        self.e.spend_vp(self.caster, t.spent_vp, mode="spent", label="b05:gifted_flame_base")
        if surcharge:
            self.e.spend_vp(self.caster, surcharge, mode="spent",
                            label="b05:gifted_projected_surge")
        base, effective_def = self.e.g2._defense_value(
            victim, defense, 0, lane.cover, commit=True,
            position_bonus=position, prone_dodge_feasible=prone_dodge_feasible)
        attack = face + attack_bonus
        if face == 1:
            outcome = "automatic_miss"
        elif face == 20 or attack > effective_def:
            outcome = "direct_hit_pending_G4"
        elif lane.cover and attack > base:
            outcome = "cover_impact"
        elif defense == "guard" and attack <= base:
            outcome = "guard_impact"
        else:
            outcome = "ordinary_miss"
        used_die = max(vigor_die, potency_die) if potency_die is not None else vigor_die
        packets = ({"fire_hp": fire_hp, "vigor": 2 + ceil(used_die*tier/3)}
                   if outcome == "direct_hit_pending_G4" else None)
        receipt = {"outcome": outcome, "attack_total": attack,
                   "base_defense": base, "final_defense": effective_def,
                   "vp_spent": total_vp, "packets_pending_g4": packets}
        self.e.log("g3_flame_launched", caster=self.caster, target=target,
                   source_id="G", source_digest=a.source.digest,
                   source_attack_bonus=attack_bonus, projection_ap=a.projection_ap,
                   tier=tier, primary_face=face, die=vigor_die,
                   critical=critical, critical_dice=list(critical_dice),
                   confirmation_face=confirmation_face,
                   gifted_emotion=self.window["emotion"], gifted_window=self.turn_key,
                   gifted_options=list(selected), gifted_surge_spent=surcharge,
                   potency_die=potency_die, effective_die=used_die,
                   physical_range=lane.distance, **receipt)
        if outcome == "direct_hit_pending_G4":
            receipt["g4_damage"] = self.e.g4.apply_flame(
                self.caster, target, ledger_index=self.e.ledger[-1]["index"],
                wound_location_roll=wound_location_roll)
            receipt["outcome"] = "direct_hit_resolved_G4"
        if safe is not None:
            self.safe_remaining = False
        if surge is not None:
            self.surge_remaining = False
        self.e.log("b05_gifted_window_debit", caster=self.caster, window=self.turn_key,
                   safe_remaining=self.safe_remaining,
                   surge_remaining=self.surge_remaining,
                   options=list(selected))
        self.e.check()
        return receipt
