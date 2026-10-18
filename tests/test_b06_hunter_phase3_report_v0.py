"""Regression gates for B06 Phase 3 census/report (only bounded stops)."""
import copy
import json
import unittest
from unittest.mock import patch

from scripts.b06_hunter_phase3_report_v0 import (
    METRICS, TERMINAL_ORDER, build_report, render_markdown,
)


class Phase3ReportTests(unittest.TestCase):
    def test_reproducible_small_census_and_sha(self):
        a = build_report(seeds=3)
        b = build_report(seeds=3)
        self.assertEqual(a, b)
        self.assertEqual(a["scenario_count"], 32)
        self.assertEqual(a["totals"]["trials"], 96)
        self.assertEqual(len(a["cases"]), 32)
        self.assertEqual(len(a["audit_sha256"]), 64)
        self.assertEqual(sum(a["totals"]["terminal"].values()), 96)
        for dimensions in a["by"].values():
            self.assertEqual(sum(g["trials"] for g in dimensions.values()), 96)
        for group in a["by"]["roster"].values():
            self.assertEqual(sum(group["terminal"].values()), group["trials"])
        self.assertEqual(a["by"]["roster"]["original"]["vp_spent"], 0)
        self.assertEqual(a["by"]["roster"]["original"]["arrows_fired"], 0)

    def test_markdown_contains_all_cells_without_victory_claim(self):
        report = build_report(seeds=1)
        text = render_markdown(report)
        self.assertEqual(text.count("| L2-P"), 16)
        self.assertEqual(text.count("| L3-P"), 16)
        for stop in TERMINAL_ORDER:
            self.assertIn(stop, text)
        self.assertIn("not party victory", text)
        self.assertIn("Audit SHA-256", text)
        self.assertIn(report["audit_sha256"], text)

    def test_terminal_count_corruption_detected(self):
        valid = build_report(seeds=1)
        rows = copy.deepcopy(valid["cases"])
        rows[0]["terminal"]["round_one_complete"] = 99
        with patch("scripts.b06_hunter_phase3_report_v0.census", return_value=rows):
            with self.assertRaisesRegex(AssertionError, "Terminal conservation"):
                build_report(seeds=1)

    def test_unresolved_contact_cannot_disappear_from_totals(self):
        valid = build_report(seeds=1)
        rows = copy.deepcopy(valid["cases"])
        rows[0]["contact_path_unresolved"] += 1
        with patch("scripts.b06_hunter_phase3_report_v0.census", return_value=rows):
            with self.assertRaisesRegex(AssertionError, "Bad unresolved count"):
                build_report(seeds=1)

    def test_original_roster_never_gets_casting_or_arrows(self):
        valid = build_report(seeds=1)
        rows = copy.deepcopy(valid["cases"])
        rows[0]["arrows_fired"] = 1
        with patch("scripts.b06_hunter_phase3_report_v0.census", return_value=rows):
            with self.assertRaisesRegex(AssertionError, "Original roster"):
                build_report(seeds=1)

    def test_invalid_seed_count_is_rejected(self):
        for seeds in (0, -1, 1.1, None):
            with self.subTest(seeds=seeds):
                with self.assertRaises(ValueError):
                    build_report(seeds=seeds)


if __name__ == "__main__":
    unittest.main()
