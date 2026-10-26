"""Bounded native High Gifted L1-3 G0/G2/G3/G4/G5 verification."""
import unittest
from dataclasses import replace

from scripts.b05_high_gifted_native_encounter_v0 import gifted_actor, GiftedNative
from scripts.b06_encounter_state_v0 import Encounter, enemy_actor, UnresolvedDecision
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee


def scene(level=1, distance=2):
    g = gifted_actor(level, "gifted", "party", occupied=((2, 2),))
    foe = enemy_actor("B06-EN-02", "soldier", "enemy",
                      occupied=((2+distance, 2),))
    e = Encounter([g, foe], {"gifted": 40, "soldier": 30}, seed=7,
                  scenario="B04-B05-High-Gifted-Native-v0",
                  policy="authored_cast_and_one_soldier_response",
                  objective="bounded_native_flame_not_hero_certification")
    GridMovement(e, width=10, height=6, scene_id="gifted-native-grid")
    RangedCombat(e, scene_id="gifted-native-projectile")
    SpellState(e)
    DamageState(e)
    melee = SourceMelee(e)
    witness = GiftedNative(e, "gifted")
    e.begin_round()
    e.start_turn("gifted")
    return e, witness, melee


def cast(w, **kwargs):
    values = {"tier": 1, "face": 14, "vigor_die": 5,
              "hand_available": True}
    values.update(kwargs)
    return w.cast_flame("soldier", **values)


def events(e, kind):
    return [x for x in e.ledger if x["kind"] == kind]


class HighGiftedNativeTests(unittest.TestCase):
    def test_source_actors_all_levels_real_resources(self):
        for level in (1, 2, 3):
            e, w, _ = scene(level)
            a = e.actors["gifted"]
            self.assertEqual((a.source.source_id, a.source.status, a.focus),
                             ("G", "STRUCTURAL_B05_ONLY", "High"))
            self.assertEqual((a.hp_max, a.vigor_max, a.vp_max, a.ap_total),
                             (12, 12*level, 6*level, 30+6*(level-1)))
            self.assertEqual(e.order, ("gifted", "soldier"))
            w.establish("Joy")
            r = cast(w)
            self.assertEqual(r["outcome"], "direct_hit_resolved_G4")
            self.assertEqual(r["attack_total"], 18)
            self.assertEqual(r["vp_spent"], 2)
            self.assertEqual(a.ap_remaining, a.ap_total-20)
            self.assertEqual(a.vp_spent, 2)
            self.assertEqual(len(events(e, "g4_damage_applied")), 1)
            self.assertEqual(events(e, "g3_flame_launched")[-1]["detail"]["source_id"], "G")
            e.check()

    def test_natural_heightened_reach_and_paid_surge_at_four_squares(self):
        e, w, _ = scene(2, 4)
        w.establish("Joy", natural_heightening=True,
                    rationale="An explicitly established joyful reunion")
        r = cast(w, face=12, safe="Reach", surge="Precision")
        self.assertEqual((r["outcome"], r["attack_total"], r["vp_spent"]),
                         ("direct_hit_resolved_G4", 17, 3))
        d = events(e, "g3_flame_launched")[-1]["detail"]
        self.assertEqual((d["physical_range"], d["gifted_options"],
                          d["gifted_surge_spent"]), (4, ["Reach", "Precision"], 1))
        self.assertEqual(e.actors["gifted"].vp_spent, 3)
        self.assertFalse(w.safe_remaining)
        self.assertFalse(w.surge_remaining)

    def test_evoked_surge_is_independent_of_natural_heightening(self):
        e, w, _ = scene()
        w.establish("Joy")
        r = cast(w, surge="Precision")
        self.assertEqual((r["attack_total"], r["vp_spent"]), (19, 3))
        self.assertFalse(w.surge_remaining)
        self.assertFalse(w.safe_remaining)
        with self.assertRaises(ValueError):
            cast(w, surge="Reach")
        self.assertEqual(len(events(e, "action_committed")), 1)

    def test_potency_uses_exact_original_vigor_die(self):
        e, w, _ = scene(1)
        w.establish("Joy", natural_heightening=True, rationale="Source-authorized")
        r = cast(w, vigor_die=2, potency_die=8, safe="Potency")
        d = events(e, "g3_flame_launched")[-1]["detail"]
        self.assertEqual((d["die"], d["potency_die"], d["effective_die"],
                          d["packets_pending_g4"]["vigor"]), (2, 8, 8, 5))

    def test_level_three_two_projection_actions_no_step_refresh(self):
        e, w, _ = scene(3)
        w.establish("Joy", natural_heightening=True, rationale="Joyful")
        first = cast(w, face=1, safe="Precision", surge="Reach")
        self.assertEqual(first["outcome"], "automatic_miss")
        second = cast(w, face=14, tier=2)
        self.assertEqual(second["outcome"], "direct_hit_resolved_G4")
        a = e.actors["gifted"]
        self.assertEqual((a.ap_remaining, a.vp_spent), (2, 3+4))
        self.assertEqual(len(events(e, "g3_flame_launched")), 2)
        with self.assertRaises(ValueError):
            cast(w, surge="Potency")
        with self.assertRaises(ValueError):
            w.establish("Joy", natural_heightening=True, rationale="no second window")

    def test_late_establishment_cannot_refresh_after_paid_action(self):
        e, w, _ = scene()
        e.spend_ap("gifted", "general", label="legal_prior_general_action")
        with self.assertRaises(ValueError):
            w.establish("Joy")
        self.assertFalse(events(e, "b05_gifted_emotion_established"))

    def test_next_turn_without_new_emotion_window_cannot_reuse_surge(self):
        e, w, _ = scene()
        w.establish("Joy")
        cast(w, face=1, surge="Precision")
        e.end_turn()
        e.start_turn("soldier")
        e.end_turn()
        e.begin_round()
        e.start_turn("gifted")
        with self.assertRaises(ValueError):
            cast(w)
        w.establish("Joy")
        self.assertTrue(w.surge_remaining)

    def test_wrong_emotion_and_no_initial_window_cost_nothing(self):
        e, w, _ = scene()
        initial = (e.actors["gifted"].ap_remaining, e.actors["gifted"].vp_spent)
        with self.assertRaises(ValueError):
            cast(w)
        w.establish("Sadness")
        with self.assertRaises(ValueError):
            cast(w)
        self.assertEqual((e.actors["gifted"].ap_remaining,
                          e.actors["gifted"].vp_spent), initial)

    def test_missing_fiction_cannot_heighten_or_overwhelm(self):
        e, w, _ = scene()
        with self.assertRaises(UnresolvedDecision):
            w.establish("Joy", natural_heightening=True)
        with self.assertRaises(ValueError):
            w.establish("Joy", natural_heightening="overwhelming")
        w.establish("Joy")
        with self.assertRaises(ValueError):
            cast(w, safe="Reach")
        with self.assertRaises(TypeError):
            cast(w, risky="Reach")
        self.assertFalse(events(e, "action_committed"))

    def test_no_fourth_square_without_live_reach(self):
        e, w, _ = scene(1, 4)
        w.establish("Joy")
        with self.assertRaises(ValueError):
            cast(w)
        self.assertFalse(events(e, "action_committed"))
        result = cast(w, surge="Reach")
        self.assertEqual(result["outcome"], "direct_hit_resolved_G4")

    def test_preflight_rejects_duplicate_or_illegal_options_and_dice(self):
        e, w, _ = scene(1)
        w.establish("Joy", natural_heightening=True, rationale="Joyful")
        for opts in ({"safe": "Reach", "surge": "Reach"},
                     {"safe": "Extent"},
                     {"safe": "Precision", "potency_die": 4},
                     {"safe": "Potency"},
                     {"safe": "Potency", "potency_die": 9}):
            with self.subTest(opts=opts):
                with self.assertRaises(ValueError):
                    cast(w, **opts)
        self.assertEqual((e.actors["gifted"].ap_remaining,
                          e.actors["gifted"].vp_spent), (30, 0))

    def test_insufficient_ap_vp_and_wrong_tier_do_not_pay(self):
        e, w, _ = scene(1)
        w.establish("Joy")
        with self.assertRaises(ValueError):
            cast(w, tier=2)
        e.actors["gifted"].ap_remaining = 19
        with self.assertRaises(ValueError):
            cast(w)
        e.actors["gifted"].ap_remaining = 30
        e.actors["gifted"].vp_available = 1
        e.actors["gifted"].vp_spent = 5
        e.check()
        with self.assertRaises(ValueError):
            cast(w)
        self.assertEqual((e.actors["gifted"].ap_remaining,
                          len(events(e, "action_committed"))), (30, 0))

    def test_fake_source_or_hand_state_preflight_cannot_spend(self):
        e, w, _ = scene()
        w.establish("Joy")
        a = e.actors["gifted"]
        a.source = replace(a.source, digest="forged")
        with self.assertRaises(UnresolvedDecision):
            cast(w)
        a.source = replace(a.source, digest=w.e.ledger[0]["detail"]["source_ids"]["gifted"]["digest"])
        e.g2.wielded["gifted"].clear()
        with self.assertRaises(UnresolvedDecision):
            cast(w)
        self.assertFalse(events(e, "action_committed"))

    def test_live_dodge_and_no_unsourced_shield_guard(self):
        e, w, _ = scene()
        w.establish("Joy")
        with self.assertRaises(ValueError):
            cast(w, defense="dodge")
        before = e.actors["soldier"].dodge_pressure
        cast(w, defense="dodge", aware=True, face=19)
        self.assertEqual(e.actors["soldier"].dodge_pressure, before+2)
        self.assertEqual(len(events(e, "g4_damage_applied")), 1)

    def test_real_soldier_melee_retaliation(self):
        e, w, melee = scene()
        w.establish("Joy")
        cast(w, face=1)
        e.end_turn()
        e.start_turn("soldier")
        e.g1.step("soldier", (-1, 0), responses=())
        self.assertTrue(e.g1.melee_contact("soldier", "gifted"))
        seq = melee.declare("soldier", "gifted", profiles=("B06-AT-03",),
                            defenses=("take_hit",))
        r = melee.resolve(seq, 0, attack_face=16, damage_face=3,
                          wound_location_roll=8)
        self.assertEqual(r["outcome"], "hit")
        self.assertEqual(len(events(e, "g5_melee_resolved")), 1)
        self.assertLess(e.actors["gifted"].hp, 12)
        e.end_turn()
        e.check()

    def test_no_unconditional_window_reuse_after_turn_end(self):
        e, w, _ = scene()
        w.establish("Joy")
        cast(w, surge="Precision")
        e.end_turn()
        with self.assertRaises(ValueError):
            cast(w)
        self.assertEqual(len(events(e, "g3_flame_launched")), 1)


if __name__ == "__main__":
    unittest.main()
