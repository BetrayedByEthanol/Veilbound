"""B04/B05 all-twelve Focus source-native combat + honest noncombat boundaries."""
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.b04_b05_focus_combat_noncombat_evidence_v0 import (
    RUNS, STATUS_ANOINTED, STATUS_COMBAT, STATUS_NONCOMBAT,
    _combat, _noncombat, evidence, matrix,
)
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import roster

ROOT = Path(__file__).resolve().parents[1]


class FocusCombatNoncombatEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = matrix()
        cls.records = {(r["pairing"], r["level"]): r for r in cls.report["rows"]}

    def test_01_all_twelve_three_levels_72_native_policy_replays(self):
        report = self.report
        self.assertEqual((12, 36, 72),
                         (report["focus_pairings"], report["pairing_level_slots"],
                          report["native_combat_witnesses"]))
        self.assertEqual(set(RUNS), {row["pairing"] for row in report["rows"]})
        self.assertEqual(36, len(self.records))
        self.assertEqual({1, 2, 3}, {r["level"] for r in report["rows"]})
        self.assertEqual(len(roster()), 12)
        for pairing in RUNS:
            for level in (1, 2, 3):
                self.assertIn((pairing, level), self.records)

    def test_02_actual_native_ledger_digest_and_contrasting_policies(self):
        for row in self.report["rows"]:
            with self.subTest(pairing=row["pairing"], level=row["level"]):
                first, second = row["selected_combat"], row["alternative_combat"]
                for source in (first, second):
                    self.assertEqual(source["evidence_status"], STATUS_COMBAT)
                    self.assertGreater(source["event_count"], 0)
                    self.assertEqual(len(source["ledger_sha256"]), 64)
                    self.assertIn("action_committed", source["distinct_event_kinds"])
                    self.assertTrue((ROOT / (source["source_module"].replace(
                        ".", "/") + ".py")).is_file())
                self.assertNotEqual(first["policy"], second["policy"])
                self.assertNotEqual(first["ledger_sha256"],
                                    second["ledger_sha256"])

    def test_03_gifted_low_native_paid_guard_alters_real_g5_defense(self):
        for level in (1, 2, 3):
            row = self.records["Gifted/Low", level]
            positive = row["selected_combat"]["source_metrics"]
            counter = row["alternative_combat"]["source_metrics"]
            self.assertEqual((positive["defense_value"], positive["anchor_bonus"],
                              positive["combat_outcome"]), (18, 1, "miss"))
            self.assertEqual((counter["defense_value"], counter["anchor_bonus"],
                              counter["combat_outcome"]), (17, 0, "hit"))

    def test_04_gifted_high_native_paid_flame_vs_extra_surge(self):
        for level in (1, 2, 3):
            row = self.records["Gifted/High", level]
            boosted = row["selected_combat"]["source_metrics"]
            ordinary = row["alternative_combat"]["source_metrics"]
            self.assertEqual(boosted["cast_outcome"], "direct_hit_resolved_G4")
            self.assertEqual(ordinary["cast_outcome"], "direct_hit_resolved_G4")
            self.assertEqual(boosted["vp_spent"], ordinary["vp_spent"]+1)
            self.assertGreater(boosted["attack_total"], ordinary["attack_total"])

    def test_05_noncombat_trained_choices_are_real_but_never_gm_resolved(self):
        counts = self.report["noncombat_coverage"]
        self.assertEqual((24, 9, 3, 0),
                         (counts["source_training_only"],
                          counts["native_anointed_clock"],
                          counts["low_priest_proxy_only"],
                          counts["human_gm_utility_outcomes"]))
        for row in self.report["rows"]:
            with self.subTest(pairing=row["pairing"], level=row["level"]):
                x = row["noncombat"]
                self.assertFalse(x["gm_check_resolved"])
                self.assertFalse(x["human_choice_observed"])
                if row["pairing"] == "Priest/Low":
                    self.assertIsNone(x["chosen"])
                    self.assertIsNone(x["alternative"])
                else:
                    self.assertNotEqual(x["chosen"]["discipline"],
                                        x["alternative"]["discipline"])
                    self.assertGreater(x["chosen"]["rank"], 0)
                    self.assertGreater(x["alternative"]["rank"], 0)
                    self.assertTrue(x["untrained_forgery_rejected"])
                    self.assertIn("scripts/", x["source_path"])
                    self.assertEqual(len(x["source_sha256"]), 64)

    def test_06_anointed_real_clock_not_fabricated_gm_verdict(self):
        for focus in ("High", "Medium", "Low"):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    a = self.records["Anointed/"+focus, level]["noncombat"]
                    self.assertEqual(a["status"], STATUS_ANOINTED)
                    self.assertEqual(len(a["native_clock_ledger_sha256"]), 64)
                    self.assertGreater(a["native_clock_event_count"], 0)
                    self.assertIn("not independently authenticated", a["limits"])
        for row in self.report["rows"]:
            if not row["pairing"].startswith("Anointed/") and row["pairing"] != "Priest/Low":
                self.assertEqual(row["noncombat"]["status"], STATUS_NONCOMBAT)

    def test_07_no_synthetic_certificates_played_sessions_or_level_ups(self):
        self.assertEqual((0, 0), (
            self.report["independently_certified_focuses"],
            self.report["strict_mvp_exits_met"]))
        self.assertEqual(self.report["externally_verified_sessions"], 0)
        for row in self.report["rows"]:
            self.assertEqual(row["actual_human_choices"], 0)
            self.assertEqual(row["externally_verified_sessions"], 0)
            self.assertFalse(row["independent_focus_certified"])
            self.assertEqual(row["strict_mvp_exits_met"], 0)

    def test_08_unsupported_pairs_levels_and_policies_fail_closed(self):
        for bad in ("Priest/Unknown", "High", [], None, True):
            with self.subTest(bad=str(bad)):
                with self.assertRaises(ValueError):
                    evidence(bad, 1)
        for bad in (0, 4, True, 1.0, "2"):
            with self.subTest(level=bad):
                with self.assertRaises(ValueError):
                    evidence("Scholar/High", bad)
        for pairing in RUNS:
            with self.subTest(pairing=pairing):
                with self.assertRaises(ValueError):
                    _combat(pairing, 1, "invented_unpaid_outcome")

    def test_09_native_ledger_mutation_never_changes_published_source(self):
        row = self.records["Gifted/Low", 2]
        mutated = deepcopy(row)
        mutated["selected_combat"]["source_metrics"]["anchor_bonus"] = 999
        self.assertEqual(self.records["Gifted/Low", 2]
                         ["selected_combat"]["source_metrics"]["anchor_bonus"], 1)
        # A fresh authoritative native replay still reports the same digest.
        regenerated = _combat("Gifted/Low", 2, "chosen_guard")
        self.assertEqual(regenerated["ledger_sha256"],
                         row["selected_combat"]["ledger_sha256"])

    def test_10_coverage_does_not_pretend_12_noncombat_native_foci(self):
        self.assertEqual(3, self.report["noncombat_coverage"]["low_priest_proxy_only"])
        self.assertEqual(24, self.report["noncombat_coverage"]["source_training_only"])
        self.assertEqual(3, self.report["noncombat_coverage"]["native_anointed_clock"])
        self.assertNotIn("human_session_count", self.report)


if __name__ == "__main__":
    unittest.main()
