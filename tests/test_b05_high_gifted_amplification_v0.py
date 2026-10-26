"""High Gifted isolated resource, power, and all 20 miscast outcomes."""
from dataclasses import replace
from pathlib import Path
import unittest

from scripts.b05_high_gifted_amplification_v0 import (
    CATEGORIES, PILOT_LINKS, EMOTIONS, HighGiftedWindow, Target, Technique,
    amplified_parameters, instability_dc, legal_target, miscast, potency_die,
    surge_surcharge, thrown_flame,
)

ROOT = Path(__file__).resolve().parents[1]


class HighGiftedAmplificationTests(unittest.TestCase):
    def setUp(self):
        self.flame = thrown_flame()
        self.soldier = Target("soldier", 3)

    def test_source_guard_approved_categories_and_pilot_eight(self):
        self.assertEqual(CATEGORIES, ("Potency", "Reach", "Extent", "Persistence", "Penetration", "Precision"))
        self.assertEqual(set(PILOT_LINKS), set(EMOTIONS))
        self.assertEqual(len({p for p, _, _ in PILOT_LINKS.values()}), 8)
        self.assertEqual(sum(r == "S" for _, _, r in PILOT_LINKS.values()), 6)
        self.assertEqual(sum(r == "P" for _, _, r in PILOT_LINKS.values()), 2)
        gifted = (ROOT / "docs/rules/08-archetypes/gifted.md").read_text()
        self.assertIn("high-gifted-amplification-and-miscasts-v0.md", gifted)
        flame_doc = (ROOT / "docs/rules/07-veil-magic/conjure-flame-v0.md").read_text()
        self.assertIn("**[Projection]**", flame_doc)
        self.assertIn("Potency", flame_doc)

    def test_projected_surge_positive_cost_and_exact_tag(self):
        for vp in range(1, 30):
            t = replace(self.flame, spent_vp=vp)
            self.assertEqual(surge_surcharge(t), (vp+3)//4)
        with self.assertRaises(ValueError):
            surge_surcharge(replace(self.flame, spent_vp=0))
        with self.assertRaises(ValueError):
            surge_surcharge(replace(self.flame, tags=frozenset()))
        self.assertEqual(surge_surcharge(thrown_flame(2)), 1)

    def test_basic_amplification_numeric_and_no_damage_type_swap(self):
        p = amplified_parameters(self.flame, ("Potency", "Reach", "Precision"))
        self.assertEqual(p["max_range"], 4)
        self.assertEqual(p["attack_bonus"], 1)
        self.assertTrue(p["roll_one_damage_die_twice_keep_higher"])
        self.assertEqual(p["direct_pressure_bonus"], 0)
        self.assertEqual(potency_die(3, 7, 8), 7)
        for options in (("Expression",), ("Reach", "Reach"), ("Extent",), ("Persistence",)):
            with self.assertRaises(ValueError):
                amplified_parameters(self.flame, options)
        with self.assertRaises(ValueError):
            potency_die(0, 8, 8)

    def test_full_six_category_preview(self):
        t = replace(self.flame, choices=CATEGORIES, radius=2,
                    duration_ticks=3, pressure=True)
        p = amplified_parameters(t, CATEGORIES)
        self.assertEqual((p["max_range"], p["radius"], p["duration_ticks"]), (4, 3, 6))
        self.assertEqual((p["attack_bonus"], p["direct_pressure_bonus"]), (1, 1))

    def test_tier_level_ap_vp_pilot_resource(self):
        for level, ap, vp in ((1, 30, 6), (2, 36, 12), (3, 42, 18)):
            w = HighGiftedWindow(level, "Joy", initial_intensity="heightened")
            self.assertEqual((w.ap, w.vp), (ap, vp))
            t = thrown_flame(2 if level == 3 else 1)
            receipt = w.cast(t, self.soldier, safe="Potency", surge="Reach")
            self.assertEqual(receipt["paid_vp"], t.spent_vp+1)
            self.assertEqual(receipt["ap_remaining"], ap-20)
            self.assertEqual(w.surge_allowance, 0)
            with self.assertRaises(ValueError):
                w.cast(t, self.soldier, surge="Precision")

    def test_access_preflight_no_mutation(self):
        w = HighGiftedWindow(1, "Joy")
        before = (w.ap, w.vp, w.surge_allowance, w.safe_step)
        with self.assertRaises(ValueError):
            w.cast(replace(self.flame, aspect="Warmth"), self.soldier)
        with self.assertRaises(ValueError):
            w.cast(thrown_flame(2), self.soldier)
        with self.assertRaises(ValueError):
            w.cast(self.flame, Target("blocked", 3, open_path=False))
        with self.assertRaises(ValueError):
            w.cast(self.flame, self.soldier, safe="Reach")
        with self.assertRaises(ValueError):
            w.cast(self.flame, self.soldier, surge="Expression")
        with self.assertRaises(ValueError):
            w.cast(self.flame, self.soldier, safe="Reach", surge="Reach")
        self.assertEqual((w.ap, w.vp, w.surge_allowance, w.safe_step), before)

    def test_deepen_and_overload_ap_cannot_combo_cast_levels_one_to_three(self):
        for level in (1, 2, 3):
            w = HighGiftedWindow(level, "Joy")
            self.assertTrue(w.deepen(12))
            self.assertEqual(w.safe_step, 1)
            with self.assertRaises(ValueError):
                w.cast(self.flame, self.soldier, safe="Potency")
            w2 = HighGiftedWindow(level, "Joy", initial_intensity="heightened")
            w2.overload()
            with self.assertRaises(ValueError):
                w2.cast(self.flame, self.soldier, safe="Potency", risky="Reach",
                        instability_roll=1, miscast_roll=4)
        w3 = HighGiftedWindow(1, "Joy")
        self.assertFalse(w3.deepen(1))
        self.assertFalse(w3.deepen_used is False)
        with self.assertRaises(ValueError):
            w3.deepen(20)
        with self.assertRaises(ValueError):
            HighGiftedWindow(1, "Joy", initial_intensity="overwhelming")

    def test_reach_fourth_square_only_if_spent_step(self):
        w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
        far = Target("far", 4)
        with self.assertRaises(ValueError):
            w.cast(self.flame, far, safe="Precision")
        self.assertEqual(w.cast(self.flame, far, safe="Reach")["ap_remaining"], 10)
        self.assertFalse(legal_target(far, self.flame))
        self.assertTrue(legal_target(far, self.flame, reach=True))


    def test_minimum_thrown_range_applies_before_costs_and_with_reach(self):
        self.assertEqual(self.flame.min_range, 1)
        self.assertFalse(legal_target(Target("same_square", 0), self.flame))
        self.assertFalse(legal_target(Target("same_square", 0), self.flame,
                                      reach=True))
        self.assertTrue(legal_target(Target("one_square", 1), self.flame))
        self.assertEqual(amplified_parameters(self.flame, ("Reach",))["min_range"], 1)
        w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
        before = (w.ap, w.vp, w.safe_step, w.surge_allowance)
        for options in ({}, {"safe": "Reach"}, {"surge": "Reach"}):
            with self.assertRaises(ValueError):
                w.cast(self.flame, Target("same_square", 0), **options)
        self.assertEqual((w.ap, w.vp, w.safe_step, w.surge_allowance), before)
        self.assertEqual(w.cast(self.flame, Target("one_square", 1),
                                safe="Reach")["paid_vp"], 2)

    def test_severe_miscast_retains_only_surviving_reach_for_range_and_targets(self):
        reaction = replace(self.flame, action_ap=0)  # isolated, not native
        def attempt(roll, *, safe="Reach", risky="Precision", surge=None,
                    target=None, others=(), choice=0):
            w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
            w.overload()
            return w.cast(reaction, target or self.soldier, safe=safe,
                          risky=risky, surge=surge, instability_roll=1,
                          miscast_roll=roll, other_targets=others,
                          choice_index=choice)["miscast"]
        # Base max 3; the surviving Reach makes it 4, reduced to 3.
        outcome = attempt(7)
        self.assertEqual(outcome["status"], "resolve")
        self.assertEqual(outcome["penalty"], "range -1 square")
        self.assertEqual(attempt(7, target=Target("far", 4))["status"], "fizzle")
        # A risky Reach is lost after severe failure and cannot save range.
        self.assertEqual(attempt(7, safe="Precision", risky="Reach")["status"],
                         "fizzle")
        distant_ally = Target("ally", 4)
        for roll in (4, 5):
            self.assertEqual(attempt(roll, others=(distant_ally,))["target"],
                             "ally")
            self.assertEqual(attempt(roll, safe="Precision", risky="Reach",
                                     others=(distant_ally,))["target"], "soldier")
        # Removing all Amplification also removes its reach, no illegal hit.
        self.assertEqual(attempt(3, target=Target("far", 4))["status"],
                         "fizzle")
        self.assertEqual(attempt(3)["status"], "resolve")

    def test_unexpected_amplification_excludes_all_selected_categories(self):
        reaction = replace(self.flame, action_ap=0)  # isolated, not native
        def attempt(extras, *, index=0):
            w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
            w.overload()
            return w.cast(reaction, self.soldier, safe="Reach",
                          risky="Precision", surge="Potency",
                          instability_roll=1, miscast_roll=20,
                          extra_choices=extras,
                          choice_index=index)["miscast"]
        self.assertIsNone(attempt(("Reach",))["bonus"])
        self.assertIsNone(attempt(("Potency", "Precision"))["bonus"])
        self.assertIsNone(attempt(("Expression",))["bonus"])
        self.assertEqual(attempt(("Reach", "Potency", "Precision"))["status"],
                         "resolve")
        # A remaining authored category works for a technique with more
        # choices; duplicating entries cannot bias the uniform draw.
        wide = replace(reaction, choices=CATEGORIES, radius=2,
                       duration_ticks=2, pressure=True)
        w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
        w.overload()
        result = w.cast(wide, self.soldier, safe="Reach", risky="Precision",
                        surge="Potency", instability_roll=1, miscast_roll=20,
                        extra_choices=("Reach", "Extent", "Extent", "Persistence"),
                        choice_index=1)["miscast"]
        self.assertEqual(result["bonus"], "Persistence")


    def test_failed_risky_reach_fizzles_after_legal_preflight_and_pays_costs(self):
        # Reaction is a pure zero-AP test fixture, not an authored off-turn
        # Conjure Flame permission. Base maximum is 3; risky Reach allows 4
        # only while that Step actually functions.
        reaction = replace(self.flame, action_ap=0)
        far = Target("far", 4)
        near = Target("near", 2)

        def attempt(instability, outcome=None, *, safe="Precision", risky="Reach",
                    surge=None, others=(), choice=0):
            w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
            w.overload()
            receipt = w.cast(
                reaction, far, safe=safe, risky=risky, surge=surge,
                instability_roll=instability, miscast_roll=outcome,
                other_targets=others, choice_index=choice,
                catalogue=(reaction,), extra_choices=("Potency",),
            )
            self.assertEqual(receipt["paid_vp"], 2 + int(surge is not None)
                             + (receipt["miscast"]["extra_spent_vp"]
                                if receipt["miscast"] else 0))
            self.assertEqual((w.ap, w.vp, w.safe_step, w.risky_step,
                              w.instability_used),
                             (6, 6-receipt["paid_vp"], 0, 0, True))
            return receipt

        # DC 13, roll 10 fails by 3, so NO miscast die is used.
        mild = attempt(10)
        self.assertIsNone(mild["miscast"])
        self.assertEqual(mild["status"], "fizzle")
        # Severe failure plus positive/negative backlash cannot certify an
        # out-of-range spell. The separately rolled backlash is preserved.
        for die in (3, 8, 14, 15, 16, 17, 19, 20):
            receipt = attempt(1, die)
            self.assertEqual(receipt["status"], "fizzle", die)
            self.assertEqual(receipt["miscast"]["status"], "fizzle", die)
        backlash = attempt(1, 14)
        self.assertEqual(backlash["miscast"]["self_damage"],
                         ("Vigor", "Vigor", 2))
        # Retargeting uses surviving base range. Alternative target rescues
        # the attack; fallback to original must fizzle if none is valid.
        for die in (4, 5):
            self.assertEqual(attempt(1, die)["status"], "fizzle")
            rescued = attempt(1, die, others=(near,))
            self.assertEqual(rescued["status"], "resolve")
            self.assertEqual(rescued["miscast"]["target"], "near")
            self.assertEqual(attempt(1, die, others=(Target("too_far", 4),))
                             ["status"], "fizzle")
        # On success risky Reach is retained and the same target is legal.
        self.assertEqual(attempt(13)["status"], "resolve")
        # A surviving safe or paid Surge Reach protects legal delivery.
        self.assertEqual(attempt(10, safe="Reach", risky="Precision")
                         ["status"], "resolve")
        self.assertEqual(attempt(10, safe="Precision", risky="Potency",
                                 surge="Reach")["status"], "resolve")

    def test_standalone_miscast_validates_final_delivery_not_original_preflight(self):
        t = self.flame
        far = Target("far", 4)
        for die in (3, 4, 5, 14, 17, 19, 20):
            result = miscast(die, t, far, selected_options=("Reach",),
                             extra_choices=("Precision",),
                             committed_cast_vp=2)
            self.assertEqual(result["status"], "fizzle", die)
        # A different legal replacement may resolve with its own range.
        longer = replace(t, name="Different Conflagration", max_range=4)
        replaced = miscast(18, t, far, catalogue=(longer,), choice_index=0,
                          selected_options=("Reach",))
        self.assertEqual(replaced["status"], "resolve")
        self.assertEqual(replaced["replacement"],
                         "Different Conflagration / Thrown Projectile")

    def test_instability_dc(self):
        self.assertEqual([instability_dc(t) for t in range(10)],
                         [12, 13, 13, 14, 14, 15, 15, 16, 16, 17])

    def test_twenty_outcomes_are_bounded_and_nonrecursive(self):
        for roll in range(1, 21):
            info = miscast(roll, self.flame, self.soldier,
                           committed_cast_vp=3, available_vp=1,
                           catalogue=(self.flame,), extra_choices=("Reach",))
            self.assertEqual(info["d20"], roll)
            self.assertIn(info["status"], ("resolve", "fizzle"))
            self.assertGreaterEqual(info["extra_spent_vp"], 0)
            self.assertLessEqual(info["extra_spent_vp"], 1)
        self.assertEqual(miscast(14, self.flame, self.soldier,
                                 committed_cast_vp=3)["self_damage"],
                         ("Vigor", "Vigor", 3))
        self.assertEqual(miscast(15, self.flame, self.soldier)["self_damage"],
                         ("HP", "Fire", 1))
        self.assertEqual(miscast(19, self.flame, self.soldier)["bonus"],
                         "one original damage die at maximum")
        self.assertEqual(miscast(20, self.flame, self.soldier,
                                 extra_choices=("Reach",))["bonus"], "Reach")

    def test_target_changes_include_allies_but_not_illegal_paths(self):
        pool = (Target("ally", 2), Target("foe", 2),
                Target("blocked", 2, open_path=False), Target("far", 5))
        choice = miscast(4, self.flame, self.soldier,
                         other_targets=pool, choice_index=0)
        self.assertEqual(choice["target"], "ally")
        self.assertEqual(miscast(5, self.flame, self.soldier,
                                 other_targets=pool, choice_index=1)["target"], "foe")
        self.assertEqual(miscast(4, self.flame, self.soldier,
                                 other_targets=())["target"], "soldier")
        with self.assertRaises(ValueError):
            miscast(4, self.flame, self.soldier,
                    other_targets=pool, choice_index=2)

    def test_inapplicable_penalties_not_made_worse_by_fizzle(self):
        nondamage = replace(self.flame, damage_die=0, damage_type="",
                            damage_resource="", attack=False, pressure=False,
                            min_range=0, max_range=0, radius=0, duration_ticks=0)
        subject = Target("self", 0)
        for x in (7, 8, 9, 10, 11, 12, 13, 19, 20):
            self.assertEqual(miscast(x, nondamage, subject)["status"], "resolve")
        self.assertEqual(miscast(15, nondamage, subject)["status"], "fizzle")
        self.assertEqual(miscast(16, self.flame, self.soldier,
                                 available_vp=0)["status"], "fizzle")
        self.assertEqual(miscast(16, self.flame, self.soldier,
                                 available_vp=1)["extra_spent_vp"], 1)
        self.assertEqual(miscast(6, self.flame, self.soldier)["status"], "resolve")
        self.assertEqual(miscast(6, self.flame, self.soldier,
                                 scatter_legal=True)["status"],
                         "scatter_pending_native_position_and_defenses")
        self.assertEqual(miscast(7, self.flame, self.soldier)["status"], "fizzle")

    def test_altered_manifestation_same_aspect_source_tier_profile_and_budget(self):
        another = replace(self.flame, name="Second Conflagration", spent_vp=2)
        different = replace(self.flame, name="Different", aspect="Warmth")
        higher = replace(self.flame, name="Higher", base_tier=3, used_tier=3)
        pool = (different, higher, self.flame, another)
        result = miscast(18, self.flame, self.soldier,
                         catalogue=pool, choice_index=1)
        self.assertEqual(result["replacement"], "Second Conflagration / Thrown Projectile")
        no = replace(another, spent_vp=20)
        self.assertEqual(miscast(18, self.flame, self.soldier,
                                 catalogue=(no,))["status"], "fizzle")
        self.assertEqual(miscast(18, self.flame, self.soldier,
                                 catalogue=())["status"], "fizzle")
        self.assertEqual(miscast(18, self.flame, self.soldier,
                                 catalogue=(self.flame,))["replacement"],
                         "Conjure Flame / Thrown Projectile")

    def test_miscast_is_only_severe_failure_and_uses_vp_paid(self):
        # Isolated ledger can test a severe check with a compatible zero-AP
        # reaction witness; no native playable spell is asserted by that fixture.
        reaction = replace(self.flame, action_ap=0)
        w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
        w.overload()  # 24 AP; leaves 6 AP for a hypothetical reaction
        a = w.cast(reaction, self.soldier, safe="Potency", risky="Reach",
                   surge="Precision", instability_roll=1, miscast_roll=14)
        self.assertEqual(a["paid_vp"], 3)
        self.assertEqual(a["miscast"]["self_damage"], ("Vigor", "Vigor", 3))
        self.assertEqual(a["instability_deficit"], 12)
        self.assertEqual(w.instability_used, True)
        self.assertEqual(w.surge_allowance, 0)
        with self.assertRaises(ValueError):
            w.cast(reaction, self.soldier, risky="Reach", instability_roll=1,
                   miscast_roll=1)

    def test_missing_dice_and_invalid_retargets_do_not_consume(self):
        w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
        with self.assertRaises(ValueError):
            w.cast(self.flame, self.soldier, safe="Potency", risky="Reach",
                   instability_roll=1, miscast_roll=1)
        self.assertEqual((w.ap, w.vp, w.safe_step), (30, 6, 1))


if __name__ == "__main__":
    unittest.main()
