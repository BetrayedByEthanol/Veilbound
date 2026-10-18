"""Regression gates for B06 Phase 3 census/report (only bounded stops)."""
import copy
import json
import math
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

    def test_warned_exposed_front_flame_never_spends_vp_or_burns_vigor(self):
        valid = build_report(seeds=3)
        index = next(i for i, row in enumerate(valid["cases"])
                     if row["scenario"] == "L2-P3-mixed-warned-exposed")
        row = valid["cases"][index]
        self.assertEqual(row["vp_spent"], 0)
        self.assertEqual(row["vigor_burn"], 0)
        # Codex counterexample: 2 VP and 3 Vigor burn can be individually
        # plausible aggregates, but are impossible with a threatened F.
        for bogus in ({"vp_spent": 2}, {"vigor_burn": 3},
                      {"vp_spent": 2, "vigor_burn": 3}):
            with self.subTest(bogus=bogus):
                rows = copy.deepcopy(valid["cases"])
                rows[index].update(bogus)
                with patch("scripts.b06_hunter_phase3_report_v0.census",
                           return_value=rows):
                    with self.assertRaisesRegex(
                            AssertionError, "Threatened front Flame spent resources"):
                        build_report(seeds=3)

    def test_bool_aggregate_cannot_exceed_per_cell_seed_count(self):
        valid = build_report(seeds=3)
        index = next(i for i, row in enumerate(valid["cases"])
                     if row["scenario"] == "L2-P3-mixed-ambush-armored")
        self.assertEqual(valid["cases"][index]["trials"], 3)
        for bogus in (
                {"pounce_declared": 4},
                {"pounce_declared": 4, "balance_resolved": 4},
                {"lane_disrupted_trials": 4}):
            with self.subTest(bogus=bogus):
                rows = copy.deepcopy(valid["cases"])
                rows[index].update(bogus)
                with patch("scripts.b06_hunter_phase3_report_v0.census",
                           return_value=rows):
                    with self.assertRaisesRegex(
                            AssertionError,
                            "Per-trial Boolean count exceeds trial count"):
                        build_report(seeds=3)

    def test_pounce_and_disrupted_lane_cannot_overlap(self):
        valid = build_report(seeds=3)
        rows = copy.deepcopy(valid["cases"])
        row = next(r for r in rows
                   if r["scenario"] == "L2-P3-mixed-ambush-armored")
        # Each isolated Boolean count is <=3; their sum is impossible.
        row["pounce_declared"] = 3
        row["balance_resolved"] = 3  # Keep Pounce/Balance valid; isolate lane overlap.
        row["lane_disrupted_trials"] = 3
        with patch("scripts.b06_hunter_phase3_report_v0.census",
                   return_value=rows):
            with self.assertRaisesRegex(
                    AssertionError, "Inconsistent Pounce/lane/path attribution"):
                build_report(seeds=3)

    def test_unresolved_path_requires_disrupted_lane(self):
        valid = build_report(seeds=3)
        rows = copy.deepcopy(valid["cases"])
        # Move exactly one terminal to unresolved, preserving all three
        # trial stops; arrange an impossible zero prior lane disruptions.
        row = next(r for r in rows if "-ambush-" in r["scenario"]
                   and any(v > 0 for k, v in r["terminal"].items()
                           if k != "contact_path_unresolved"))
        donor = next(k for k, v in row["terminal"].items()
                     if k != "contact_path_unresolved" and v > 0)
        row["terminal"][donor] -= 1
        row["terminal"]["contact_path_unresolved"] = (
            row["terminal"].get("contact_path_unresolved", 0) + 1)
        row["contact_path_unresolved"] = row["terminal"]["contact_path_unresolved"]
        row["lane_disrupted_trials"] = 0
        with patch("scripts.b06_hunter_phase3_report_v0.census",
                   return_value=rows):
            with self.assertRaisesRegex(
                    AssertionError, "Inconsistent Pounce/lane/path attribution"):
                build_report(seeds=3)

    def test_warned_opening_forbids_lane_disruption_and_unresolved_path(self):
        valid = build_report(seeds=3)
        idx = next(i for i, r in enumerate(valid["cases"])
                   if r["scenario"] == "L2-P3-original-warned-armored")
        for kind in ("lane", "path"):
            with self.subTest(kind=kind):
                rows = copy.deepcopy(valid["cases"])
                row = rows[idx]
                if kind == "lane":
                    row["lane_disrupted_trials"] = 1
                else:
                    donor = next(k for k, v in row["terminal"].items()
                                 if k != "contact_path_unresolved" and v > 0)
                    row["terminal"][donor] -= 1
                    row["terminal"]["contact_path_unresolved"] = 1
                    row["contact_path_unresolved"] = 1
                    row["lane_disrupted_trials"] = 1
                with patch("scripts.b06_hunter_phase3_report_v0.census",
                           return_value=rows):
                    with self.assertRaisesRegex(
                            AssertionError, "Warned opening has ambush-only counters"):
                        build_report(seeds=3)

    def test_flame_vigor_burn_cannot_exceed_paid_launches(self):
        valid = build_report(seeds=3)
        for scenario in ("L2-P3-mixed-warned-armored",
                         "L2-P3-mixed-ambush-exposed"):
            with self.subTest(scenario=scenario):
                rows = copy.deepcopy(valid["cases"])
                row = next(r for r in rows if r["scenario"] == scenario)
                row["vigor_burn"] = (row["vp_spent"] // 2) * 5 + 1
                with patch("scripts.b06_hunter_phase3_report_v0.census",
                           return_value=rows):
                    with self.assertRaisesRegex(
                            AssertionError, "Vigor burn exceeds paid Flame launches"):
                        build_report(seeds=3)

    def test_every_front_caster_approach_requires_flame_launch(self):
        valid = build_report(seeds=3)
        rows = copy.deepcopy(valid["cases"])
        row = next(r for r in rows
                   if r["scenario"] == "L2-P3-mixed-ambush-exposed")
        row["front_caster_approach_mp"] = 2
        row["front_caster_precontact_casts"] = 0
        # It is impossible to pay movement without reaching this launch,
        # even if the reported VP also says zero.
        with patch("scripts.b06_hunter_phase3_report_v0.census",
                   return_value=rows):
            with self.assertRaisesRegex(
                    AssertionError, "Front caster moved without launching Flame"):
                build_report(seeds=3)

    def test_exposed_front_all_vp_is_paid_precontact_casts(self):
        valid = build_report(seeds=128)
        rows = copy.deepcopy(valid["cases"])
        row = next(r for r in rows
                   if r["scenario"] == "L2-P3-mixed-ambush-exposed")
        self.assertLess(row["vp_spent"] + 2, 128 * 2)
        self.assertEqual(row["vp_spent"],
                         row["front_caster_precontact_casts"] * 2)
        row["vp_spent"] += 2
        with patch("scripts.b06_hunter_phase3_report_v0.census",
                   return_value=rows):
            with self.assertRaisesRegex(
                    AssertionError, "Exposed-front VP does not match Flame casts"):
                build_report(seeds=128)

    def test_unresolved_pounce_requires_terminal_bite_stop(self):
        valid = build_report(seeds=128)
        rows = copy.deepcopy(valid["cases"])
        row = next(r for r in rows
                   if r["scenario"] == "L2-P3-mixed-ambush-armored")
        self.assertGreater(row["pounce_declared"],
                           row["terminal"].get("wound_unresolved", 0) +
                           row["terminal"].get("frontline_first_zero", 0))
        row["balance_resolved"] = 0
        with patch("scripts.b06_hunter_phase3_report_v0.census",
                   return_value=rows):
            with self.assertRaisesRegex(
                    AssertionError, "Unresolved Pounce lacks terminal Bite stop"):
                build_report(seeds=128)

    def test_toxin_cannot_overlap_unresolved_contact_path(self):
        valid = build_report(seeds=128)
        rows = copy.deepcopy(valid["cases"])
        row = next(r for r in rows
                   if r["scenario"] == "L2-P3-original-ambush-armored")
        self.assertGreater(row["contact_path_unresolved"], 0)
        row["full_toxin"] = 128 - row["contact_path_unresolved"] + 1
        row["reduced_toxin"] = 0
        self.assertLessEqual(row["full_toxin"] + row["reduced_toxin"], 128)
        with patch("scripts.b06_hunter_phase3_report_v0.census",
                   return_value=rows):
            with self.assertRaisesRegex(
                    AssertionError, "Toxin overlaps unresolved contact path"):
                build_report(seeds=128)

    def test_flame_vigor_aggregate_never_equals_one_or_two(self):
        valid = build_report(seeds=128)
        for burn in (1, 2):
            with self.subTest(burn=burn):
                rows = copy.deepcopy(valid["cases"])
                row = next(r for r in rows
                           if r["scenario"] == "L2-P3-mixed-warned-armored")
                self.assertGreater(row["vp_spent"], 0)
                row["vigor_burn"] = burn
                with patch("scripts.b06_hunter_phase3_report_v0.census",
                           return_value=rows):
                    with self.assertRaisesRegex(
                            AssertionError, "Impossible sub-three Vigor burn"):
                        build_report(seeds=128)

    def test_mean_hunter_hp_must_be_finite_and_physically_bounded(self):
        valid = build_report(seeds=3)
        for bad_mean in (float("nan"), float("inf"), -float("inf"),
                         -19.001, -20, 14.001, 15, "3", True):
            with self.subTest(mean=repr(bad_mean)):
                rows = copy.deepcopy(valid["cases"])
                rows[0]["mean_hunter_hp"] = bad_mean
                with patch("scripts.b06_hunter_phase3_report_v0.census",
                           return_value=rows):
                    with self.assertRaisesRegex(
                            AssertionError, "Invalid mean Hunter HP"):
                        build_report(seeds=3)

    def test_replay_rejects_plausible_counter_and_mean_tampering(self):
        valid = build_report(seeds=128)
        for metric in ("arrows_fired", "mean_hunter_hp"):
            with self.subTest(metric=metric):
                rows = copy.deepcopy(valid["cases"])
                row = next(r for r in rows
                           if r["scenario"] == "L2-P3-mixed-warned-armored")
                row[metric] += 1 if metric == "arrows_fired" else 0.001
                # All explicit coarse bounds remain satisfied, so the
                # independent per-seed replay must catch this corruption.
                with patch("scripts.b06_hunter_phase3_report_v0.census",
                           return_value=rows):
                    with self.assertRaisesRegex(
                            AssertionError, "Census differs from source trial replay"):
                        build_report(seeds=128)

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
