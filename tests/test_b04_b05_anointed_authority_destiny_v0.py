"""Isolated design probes, source-loaded. NOT native or canonical rule approval."""
from pathlib import Path
import unittest

from scripts.b04_b05_anointed_authority_destiny_v0 import (
    INTENSITIES, authority_cost, compare, destiny_recovery, focus_three_rounds,
    load_targets, max_destiny, max_normal_tier, one_hit, paid_conjure,
    recovery_after_elapsed, significant_mission_event, spend_for_authority_attempt,
    verify_conjure_source,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/design/b04-b05-anointed-authority-destiny-cross-aspect-balance-v0.md"
INDEX = ROOT / "docs/design/README.md"
ROADMAP = ROOT / "docs/design/veilbound-roadmap-and-mvp-readiness.md"


class AnointedAuthorityDestinyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.targets = load_targets()
        cls.doc = DOC.read_text(encoding="utf-8")

    def test_01_source_bound_three_enemy_profiles_and_paid_technique(self):
        verify_conjure_source()
        self.assertEqual((("B06-EN-02", 12, 36, 2),
                          ("B06-EN-01", 12, 36, 6),
                          ("B06-EN-03", 14, 42, 4)),
                         tuple((t.name, t.hp_max, t.vigor_max, t.throughput)
                               for t in self.targets))
        self.assertEqual((1, 2, 3, 5, 9),
                         tuple(max_normal_tier(x) for x in (1, 3, 5, 10, 20)))
        self.assertEqual((3.875, 5.375, 6.5, 9.875, 15.5),
                         tuple(paid_conjure(i)["vigor_mean_on_hit"] for i in (1, 2, 3, 5, 9)))
        self.assertEqual((2, 4, 6, 10, 18),
                         tuple(paid_conjure(i)["vp_cost"] for i in (1, 2, 3, 5, 9)))

    def test_02_destiny_pool_and_six_hour_boundaries(self):
        levels = (1, 3, 4, 5, 10, 15, 20)
        self.assertEqual((2, 2, 2, 3, 4, 5, 6), tuple(map(max_destiny, levels)))
        self.assertEqual((1, 1, 1, 1, 1, 1, 2), tuple(map(destiny_recovery, levels)))
        for level in levels:
            self.assertEqual(0, recovery_after_elapsed(level, 0, 5))
            self.assertEqual(destiny_recovery(level), recovery_after_elapsed(level, 0, 6))
            self.assertEqual(destiny_recovery(level), recovery_after_elapsed(level, 0, 11))
            self.assertEqual(min(max_destiny(level), 2 * destiny_recovery(level)),
                             recovery_after_elapsed(level, 0, 12))
            self.assertEqual(max_destiny(level),
                             recovery_after_elapsed(level, max_destiny(level), 36))
        self.assertEqual(3, max_destiny(4, high_l4_bonus=True))
        self.assertEqual(2, max_destiny(3, high_l4_bonus=True))
        with self.assertRaises(ValueError):
            recovery_after_elapsed(1, 3, 6)

    def test_03_intensity_level_and_resource_gates(self):
        for level, unlocked in (
            (1, {"baseline", "lesser"}),
            (4, {"baseline", "lesser"}),
            (5, {"baseline", "lesser", "greater"}),
            (10, set(INTENSITIES)),
        ):
            for intensity in INTENSITIES:
                if intensity in unlocked:
                    self.assertEqual(INTENSITIES[intensity][0],
                                     authority_cost(level, intensity, max_destiny(level)))
                else:
                    with self.assertRaises(ValueError):
                        authority_cost(level, intensity, max_destiny(level))
        with self.assertRaises(ValueError):
            authority_cost(10, "supreme", 2)
        with self.assertRaises(ValueError):
            authority_cost(1, "unknown", 2)

    def test_04_no_destiny_on_interrupted_attempt_but_spend_on_miss(self):
        self.assertEqual(1, spend_for_authority_attempt(1, "lesser", 2,
                                                         legal_application=True))
        self.assertEqual(2, spend_for_authority_attempt(1, "lesser", 2,
                                                         legal_application=False))
        self.assertEqual(2, spend_for_authority_attempt(5, "greater", 2,
                                                         legal_application=False))
        self.assertEqual(0, spend_for_authority_attempt(5, "greater", 2,
                                                         legal_application=True))
        with self.assertRaises(ValueError):
            spend_for_authority_attempt(5, "greater", 1, legal_application=True)

    def test_05_gm_story_event_not_mission_completion_or_farm(self):
        value, seen = significant_mission_event(1, 0, True, "village-cured", frozenset())
        self.assertEqual(1, value)
        self.assertEqual((value, seen), significant_mission_event(1, value, True, "village-cured", seen))
        self.assertEqual((value, seen), significant_mission_event(1, value, False, "routine-heal", seen))
        self.assertEqual((2, seen | {"another-consequential-event"}),
                         significant_mission_event(1, 1, True, "another-consequential-event", seen))
        self.assertEqual(2, significant_mission_event(1, 2, True, "third", seen)[0])

    def test_06_burn_vs_throughput_interference_on_source_sentry(self):
        sentry = self.targets[1]
        burn = one_hit(sentry, "supreme", "burn", 36)
        interference = one_hit(sentry, "supreme", "interference", 36)
        self.assertEqual((6, 12, 20, 6),
                         (burn["hp_after_hit"], burn["hp_after_step"],
                          burn["vigor_after_step"], burn["regeneration_restored"]))
        self.assertEqual((6, 9, 32, 3),
                         (interference["hp_after_hit"], interference["hp_after_step"],
                          interference["vigor_after_step"], interference["regeneration_restored"]))
        self.assertEqual(0, one_hit(sentry, "supreme", "burn", 0)["regeneration_restored"])
        self.assertEqual(0, one_hit(sentry, "supreme", "interference", 0)["regeneration_restored"])

    def test_07_all_states_no_overdraft_or_illicit_dying_resolution(self):
        for target in self.targets:
            for vigor in (0, 1, 4, target.vigor_max):
                for intensity in INTENSITIES:
                    for model in ("burn", "interference"):
                        x = one_hit(target, intensity, model, vigor)
                        self.assertFalse(x["needs_native_dying_wound_resolution"])
                        self.assertTrue(0 <= x["vigor_after_step"] <= vigor)
                        self.assertTrue(0 <= x["hp_after_step"] <= target.hp_max)
                        miss = one_hit(target, intensity, model, vigor, hit=False)
                        self.assertEqual(0, miss["vigor_burned"])
                        self.assertEqual(0, miss["hp_fire_packet"])
        dying = one_hit(self.targets[0], "supreme", "burn", 36, hp_before=1)
        self.assertTrue(dying["needs_native_dying_wound_resolution"])
        self.assertNotIn("hp_after_step", dying)

    def test_08_three_focus_source_ap_and_once_per_turn_bound(self):
        self.assertEqual([1, 1, 1], focus_three_rounds(1, "High")["opportunities_per_round"])
        self.assertEqual([2, 2, 2], focus_three_rounds(3, "High")["opportunities_per_round"])
        self.assertEqual([6, 6, 6], focus_three_rounds(20, "High")["opportunities_per_round"])
        self.assertEqual([0, 1, 1], focus_three_rounds(1, "Medium")["opportunities_per_round"])
        self.assertEqual([0, 1, 1], focus_three_rounds(3, "Medium")["opportunities_per_round"])
        self.assertEqual([1, 1, 1], focus_three_rounds(1, "Low")["opportunities_per_round"])
        for level in (1, 3, 5, 10, 20):
            for focus in ("High", "Medium", "Low"):
                x = focus_three_rounds(level, focus)
                self.assertTrue(all(spent <= x["turn_ap"]
                                    for spent in x["ap_committed_for_signature_opportunities"]))
                self.assertEqual(0, x["additional_physical_attacks_granted"])
                if focus != "High":
                    self.assertLessEqual(max(x["opportunities_per_round"]), 1)

    def test_09_report_census_and_source_scope(self):
        x = compare()
        self.assertEqual("DESIGN_ONLY_NOT_NATIVE_NOT_CANONICAL", x["status"])
        self.assertEqual(96, len(x["single_hit_next_regeneration_step"]))
        self.assertEqual(15, len(x["focus_opportunities"]))
        self.assertEqual(5, len(x["conjure_flame_reference"]))
        self.assertEqual(0.65, x["hit_probability_assumption"])
        self.assertTrue(x["candidate_signature"]
                        ["authority_declared_and_charged_on_legal_attempt_even_if_miss"])

    def test_10_design_only_and_readiness_not_mutated(self):
        for term in ("DESIGN ONLY", "Meaningful Mission Event", "Searing Interference",
                     "3/6/9", "High", "Medium", "Low", "Firebound Sentry",
                     "Hunter", "Ordinary Human Soldier", "9/12", "0/12",
                     "not native", "Sovereign Projection", "Level 3"):
            self.assertIn(term.lower(), self.doc.lower())
        self.assertIn(DOC.name, INDEX.read_text(encoding="utf-8"))
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn(DOC.name, roadmap)
        self.assertIn("**0/12**", roadmap)
        self.assertIn("**9/12**", roadmap)


if __name__ == "__main__":
    unittest.main()
