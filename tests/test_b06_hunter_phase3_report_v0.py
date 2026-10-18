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


    def test_caster_only_counters_are_impossible_for_original_roster(self):
        # Each counter must be independently forbidden, not just VP/arrows.
        valid = build_report(seeds=3)
        original_index = next(i for i, row in enumerate(valid["cases"])
                              if "-original-" in row["scenario"])
        for key, value in (
                ("arrows_fired", 1),
                ("vp_spent", 2),
                ("vigor_burn", 1),
                ("front_caster_precontact_casts", 1),
                ("front_caster_approach_mp", 2)):
            with self.subTest(metric=key):
                rows = copy.deepcopy(valid["cases"])
                rows[original_index][key] = value
                with patch("scripts.b06_hunter_phase3_report_v0.census",
                           return_value=rows):
                    with self.assertRaisesRegex(
                            AssertionError, "Original roster received mixed resources"):
                        build_report(seeds=3)

    def test_front_only_metrics_rejected_when_no_front_ambush_flame(self):
        valid = build_report(seeds=3)
        # Mixed F can attack from the back, but it never moves into the
        # *front caster* range-entry lane unless both ambush and exposed.
        forbidden_cases = (
            "-mixed-warned-armored",
            "-mixed-warned-exposed",
            "-mixed-ambush-armored",
        )
        for suffix in forbidden_cases:
            index = next(i for i, row in enumerate(valid["cases"])
                         if row["scenario"].endswith(suffix))
            for metric, value in (
                    ("front_caster_precontact_casts", 1),
                    ("front_caster_approach_mp", 2)):
                with self.subTest(case=suffix, metric=metric):
                    rows = copy.deepcopy(valid["cases"])
                    rows[index][metric] = value
                    with patch("scripts.b06_hunter_phase3_report_v0.census",
                               return_value=rows):
                        with self.assertRaisesRegex(
                                AssertionError, "Impossible front-caster attribution"):
                            build_report(seeds=3)

    def test_precontact_casts_require_range_entry_mp(self):
        valid = build_report(seeds=3)
        rows = copy.deepcopy(valid["cases"])
        row = next(row for row in rows
                   if row["scenario"] == "L2-P3-mixed-ambush-exposed")
        row["front_caster_precontact_casts"] = 1
        row["front_caster_approach_mp"] = 0
        row["vp_spent"] = max(2, row["vp_spent"])
        with patch("scripts.b06_hunter_phase3_report_v0.census",
                   return_value=rows):
            with self.assertRaisesRegex(
                    AssertionError, "Precontact caster lacked paid range-entry"):
                build_report(seeds=3)

    def test_seed_range_is_derived_for_short_and_default_runs(self):
        for seeds, last in ((1, 0), (3, 2), (128, 127)):
            with self.subTest(seeds=seeds):
                report = build_report(seeds=seeds)
                markdown = render_markdown(report)
                self.assertIn(f"seeds `0..{last}` per cell", markdown)
                self.assertEqual(report["seed_count_per_cell"], seeds)
                self.assertEqual(report["totals"]["trials"], 32 * seeds)

    def test_workflow_pins_pr_head_and_verifies_attested_source_sha(self):
        from pathlib import Path
        workflow = (Path(__file__).resolve().parents[1] / ".github" /
                    "workflows" / "b06-phase3-verification.yml").read_text(
                        encoding="utf-8")
        ref = "${{ github.event_name == 'pull_request' && github.event.pull_request.head.sha || github.sha }}"
        self.assertEqual(workflow.count(ref), 2)
        self.assertIn('test "$ACTUAL_SHA" = "$EXPECTED_SHA"', workflow)
        self.assertIn("persist-credentials: false", workflow)

    def test_invalid_seed_count_is_rejected(self):
        for seeds in (0, -1, 1.1, None):
            with self.subTest(seeds=seeds):
                with self.assertRaises(ValueError):
                    build_report(seeds=seeds)


if __name__ == "__main__":
    unittest.main()
