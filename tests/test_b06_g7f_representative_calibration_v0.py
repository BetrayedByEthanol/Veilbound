"""G7-F: strict pilot denominator, provenance and no-false-calibration proofs."""
from contextlib import redirect_stdout
from copy import deepcopy
from hashlib import sha256
from io import StringIO
import json
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from scripts import b06_g7f_representative_calibration_v0 as g7f


def fake_source_trial(level, size, seed, policy, outcome="legal_window_cutoff"):
    """Non-gameplay fixture used ONLY for verifier corruption tests."""
    roster = ("hunter", "vanguard", "guardian", "archer") + (
        ("scholar",) if size == 4 else ())
    sources = ("B06-EN-03", "A", "B", "R") + (("F",) if size == 4 else ())
    initial = {name: {"source_id": src, "source_digest": "hash:" + src,
                      "hp": 24, "dead": False}
               for name, src in zip(roster, sources)}
    final = deepcopy(initial)
    ledger = [{"index": idx, "round": 1, "kind": "turn_end",
               "detail": {"actor": name}} for idx, name in enumerate(roster)]
    ledger.append({"index": len(ledger), "round": 1,
                   "kind": "round_end", "detail": {}})
    if outcome == "hunter_defeat_attested":
        final["hunter"]["hp"] = -24
        final["hunter"]["dead"] = True
        ledger.append({"index": len(ledger), "round": 1,
                       "kind": "g6d_hunter_defeat_attested", "detail": {}})
    if outcome == "party_withdrawal_attested":
        ledger.append({"index": len(ledger), "round": 1,
                       "kind": "g7c_party_withdrawal_attested", "detail": {}})
    if outcome == "party_defeat_attested":
        ledger.append({"index": len(ledger), "round": 1,
                       "kind": "g7c_party_defeat_attested", "detail": {}})
    return {
        "level": level, "party_size": size, "seed": seed, "policy_id": policy,
        "scenario_id": "unit-test-only:" + policy,
        "initial_state": initial, "final_state": final,
        "outcome": outcome, "native_terminal": (
            {"ending": outcome} if outcome in g7f.CERTIFIED_TERMINALS else None),
        "unresolved": ({"reason": "mechanical_gap"}
                       if outcome == "unresolved_mechanical_branch" else None),
        "hunter_cr": None, "complete_party_pack_certified": False,
        "turns_completed": len(roster), "rounds_completed": 1,
        "ledger": ledger, "ledger_sha256": g7f._digest(ledger),
        "clock_handoff": {"not_a_combat_terminal": True, "elapsed_seconds": 0}
        if policy.startswith("forest_") else None,
    }


class PureG7FTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Avoid requiring full repository native engines for these isolated
        # verifier and denominator tests. CI runs real-engine tests below.
        cls._patch = patch.dict(sys.modules, {
            "scripts.b06_g7a_native_terminal_census_v0": SimpleNamespace(
                canonical_digest=g7f._digest)})
        cls._patch.start()

    @classmethod
    def tearDownClass(cls):
        cls._patch.stop()

    def attested(self, *, level=3, size=4, seed=0,
                 policy="warned_control", outcome="legal_window_cutoff"):
        value = fake_source_trial(level, size, seed, policy, outcome)
        return g7f.attest_native(value, level=level, size=size,
                                 seed=seed, policy=policy)

    def test_01_exact_31_preauthored_cohorts(self):
        self.assertEqual(len(g7f.COHORTS), 31)
        self.assertEqual(len(set(g7f.COHORTS)), 31)
        self.assertEqual(len(g7f.POLICIES), 10)
        self.assertEqual({p for _, _, p in g7f.COHORTS}, set(g7f.POLICIES))

    def test_02_refuses_fictional_party_or_protection(self):
        for values in [(1, 4, 0, "forest_pounce"),
                       (3, 5, 0, "warned_control"),
                       (2, 3, 0, "reactive_shield"),
                       (2, 4, 0, "prepared_body"),
                       (3, 4, -1, "warned_control")]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                g7f._validate_cell(*values)

    def test_03_validates_before_native_execution(self):
        with patch.object(g7f, "_native_case", side_effect=AssertionError("called")):
            with self.assertRaises(ValueError):
                g7f.run_case(2, 3, 0, policy="reactive_shield")

    def test_04_rejects_bool_seed_and_level(self):
        for level, seed in [(True, 0), (3, True), (3, 1.0)]:
            with self.subTest(level=level, seed=seed), self.assertRaises(ValueError):
                g7f._validate_cell(level, 4, seed, "warned_control")

    def test_05_attests_legitimate_source_shape_without_minting_terminal(self):
        result = self.attested()
        self.assertTrue(result["censored"])
        self.assertFalse(result["certified_terminal"])
        self.assertEqual(result["turns_completed"], 5)
        self.assertEqual(result["party_hp_change"], 0)

    def test_06_rejects_ledger_hash_tamper(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["ledger"][0]["detail"]["actor"] = "guardian"
        with self.assertRaisesRegex(AssertionError, "hash"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_07_rejects_missing_or_reindexed_source_events(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["ledger"][0]["index"] = 30
        report["ledger_sha256"] = g7f._digest(report["ledger"])
        with self.assertRaisesRegex(AssertionError, "resequenced"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_08_rejects_reordered_turns_even_with_rehashed_ledger(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["ledger"][0]["detail"]["actor"] = "vanguard"
        report["ledger_sha256"] = g7f._digest(report["ledger"])
        with self.assertRaisesRegex(AssertionError, "chronology"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_09_rejects_mutated_source_identity(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["final_state"]["archer"]["source_id"] = "B"
        with self.assertRaisesRegex(AssertionError, "roster"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_10_rejects_terminal_label_without_native_event(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["outcome"] = "hunter_defeat_attested"
        report["native_terminal"] = {"ending": "hunter_defeat_attested"}
        with self.assertRaisesRegex(AssertionError, "terminal"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_11_rejects_demoting_real_terminal_to_cutoff(self):
        report = fake_source_trial(3, 4, 0, "warned_control", "hunter_defeat_attested")
        report["outcome"] = "legal_window_cutoff"
        with self.assertRaisesRegex(AssertionError, "mislabeled"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_12_rejects_false_party_wipe_from_only_dying_or_observed(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["outcome"] = "party_defeat_attested"
        report["native_terminal"] = {"ending": "party_defeat_attested"}
        with self.assertRaisesRegex(AssertionError, "terminal"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_13_retains_reason_for_each_unresolved_branch(self):
        x = self.attested(outcome="unresolved_mechanical_branch")
        self.assertTrue(x["censored"])
        self.assertEqual(x["unresolved_reason"], "mechanical_gap")

    def test_14_refuses_clock_handoff_as_forest_escape(self):
        report = fake_source_trial(3, 4, 0, "forest_pounce")
        report["clock_handoff"]["not_a_combat_terminal"] = False
        with self.assertRaisesRegex(AssertionError, "clock"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="forest_pounce")

    def test_15_refuses_any_embedded_false_CR_or_pack_certificate(self):
        for field, value in (("hunter_cr", 3), ("complete_party_pack_certified", True)):
            report = fake_source_trial(3, 4, 0, "warned_control")
            report[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, "inflated"):
                g7f.attest_native(report, level=3, size=4, seed=0,
                                 policy="warned_control")

    def test_16_all_31_denominators_and_ten_pairwise_seed_sets(self):
        def fake(level, size, seed, policy):
            outcome = "hunter_defeat_attested" if seed % 2 else "legal_window_cutoff"
            return fake_source_trial(level, size, seed, policy, outcome)
        with patch.object(g7f, "_native_case", side_effect=fake):
            report = g7f.census(seeds=2)
        self.assertEqual(report["cohort_count"], 31)
        self.assertEqual(report["observation_count"], 62)
        self.assertEqual(report["paired_comparison_count"], 10)
        self.assertEqual(report["certified_native_terminal_observations"], 31)
        self.assertEqual(report["censored_or_unresolved_observations"], 31)
        self.assertEqual(sum(x["native_terminals"] for x in report["cohorts"]), 31)
        self.assertTrue(all(x["paired_seed_count"] == 2 and
                            x["censored_pairs"] == 1 for x in report["paired_comparisons"]))
        self.assertIsNone(report["creature_challenge_rating"])
        self.assertFalse(report["representative_encounter_calibration_accepted"])

    def test_17_paired_delta_preserves_each_separate_source_digest(self):
        def fake(level, size, seed, policy):
            trial = fake_source_trial(level, size, seed, policy)
            trial["final_state"]["hunter"]["hp"] = 10 if policy == "forest_pounce" else 20
            return trial
        with patch.object(g7f, "_native_case", side_effect=fake):
            report = g7f.census(seeds=1)
        forest = [x for x in report["paired_comparisons"] if x["comparison"] ==
                  "forest_ordinary__vs__forest_pounce"]
        self.assertEqual(len(forest), 4)
        self.assertTrue(all(x["observations"][0]["delta_hunter_hp_change"] == -10
                            for x in forest))
        self.assertTrue(all(x["statistical_effect_estimate"] is None for x in forest))

    def test_18_pilot_report_and_hash_reproducible(self):
        with patch.object(g7f, "_native_case", side_effect=fake_source_trial):
            r1 = g7f.census(seeds=1, include_trials=True)
            r2 = g7f.census(seeds=1, include_trials=True)
        self.assertEqual(r1, r2)
        self.assertEqual(g7f._digest(r1), g7f._digest(r2))
        self.assertEqual(r1["historical_phase3_sha256"], g7f.PHASE3_SHA)

    def test_19_bad_census_inputs_fail_before_any_native_call(self):
        with patch.object(g7f, "_native_case", side_effect=AssertionError("called")):
            for kwargs in ({"seeds": 0}, {"seeds": 129}, {"seeds": True},
                           {"seeds": 1, "start_seed": -1},
                           {"seeds": 1, "include_trials": 1}):
                with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                    g7f.census(**kwargs)


class NativeG7FTests(unittest.TestCase):
    """CI exercises real G0–G7 native adapters; no synthetic combat mocks."""
    def test_20_run_each_real_policy_and_validate_true_native_provenance(self):
        for level, size, policy in g7f.COHORTS:
            with self.subTest(level=level, size=size, policy=policy):
                result = g7f.run_case(level, size, 0, policy=policy)
                self.assertEqual(result["policy"], policy)
                self.assertEqual(len(result["ledger_sha256"]), 64)
                self.assertIsInstance(result["hunter_hp_change"], int)

    def test_21_native_seeded_denominator_and_no_fake_CR(self):
        report = g7f.census(seeds=2)
        self.assertEqual(report["observation_count"], 62)
        self.assertEqual(report["cohort_count"], 31)
        self.assertEqual(report["paired_comparison_count"], 10)
        self.assertEqual(sum(x["seed_count"] for x in report["cohorts"]), 62)
        self.assertEqual(report["complete_party_packs_certified"], 0)
        self.assertIsNone(report["creature_challenge_rating"])
        self.assertTrue(all(x["sampled_win_rate"] is None and
                            x["confidence_interval"] is None
                            for x in report["cohorts"]))

    def test_22_native_terminal_escapes_separate_from_forest_clock(self):
        t = g7f.run_case(3, 4, 0, policy="warned_party_exit")
        f = g7f.run_case(3, 4, 0, policy="forest_pounce")
        self.assertEqual(t["policy"], "warned_party_exit")
        self.assertEqual(f["policy"], "forest_pounce")
        self.assertEqual(f["real_party_exit_events"], 0)
        self.assertNotEqual(t["source_policy_id"], f["source_policy_id"])

    def test_23_native_pounce_control_share_authored_comparable_source(self):
        o = g7f.run_case(3, 4, 1, policy="forest_ordinary")
        p = g7f.run_case(3, 4, 1, policy="forest_pounce")
        self.assertEqual(o["genuine_pounces"], 0)
        self.assertEqual(p["genuine_pounces"], 1)
        self.assertEqual(o["level"], p["level"])
        self.assertEqual(o["seed"], p["seed"])

    def test_24_cli_result_is_deterministic_json_with_no_CR(self):
        with redirect_stdout(StringIO()) as sink:
            g7f.main(["--seeds", "1"])
        report = json.loads(sink.getvalue())
        digest = report.pop("pilot_sha256")
        self.assertEqual(digest, g7f._digest(report))
        self.assertEqual(report["observation_count"], 31)
        self.assertIsNone(report["creature_challenge_rating"])


if __name__ == "__main__":
    unittest.main()
