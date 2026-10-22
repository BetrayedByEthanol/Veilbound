"""B06 G7-H — independently bind three complete source-native terminal paths."""
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
import unittest

from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_g7h_mixed_encounter_certification_v0 import (
    POLICIES, TERMINALS, HISTORICAL_SHA, attest_trial, main, run_pack,
)


class G7HMixedNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = run_pack(3, 17, include_trials=True)

    def _case(self, policy):
        return deepcopy(self.bundle["native_trials"][policy])

    def test_01_authenticates_all_three_terminals_with_actual_native_rounds(self):
        for level in (2, 3):
            with self.subTest(level=level):
                report = run_pack(level, 17)
                self.assertTrue(report["bounded_terminal_matrix_certified"])
                self.assertEqual(report["distinct_native_terminal_outcomes"], 3)
                self.assertEqual(report["policies"], list(POLICIES))
                self.assertEqual(report["party_size"], 4)
                self.assertEqual({c["outcome"] for c in report["cases"]},
                                 {entry[0] for entry in TERMINALS.values()})
                self.assertEqual({c["native_terminal_kind"] for c in report["cases"]},
                                 {entry[1] for entry in TERMINALS.values()})
                for c in report["cases"]:
                    self.assertEqual(c["turns_completed"],
                                     c["rounds_completed"] * 5)
                    self.assertGreater(c["rounds_completed"], 0)
                    self.assertEqual(c["source_scenario_id"],
                                     f"B06-I3-G6C:party-4:L{level}")
                self.assertFalse(report["complete_party_pack_certified"])
                self.assertFalse(report["full_representative_encounter_pack_certified"])
                self.assertFalse(report["representative_encounter_calibration_accepted"])
                self.assertIsNone(report["hunter_cr"])
                self.assertIsNone(report["confidence_interval"])
                self.assertIsNone(report["sampled_win_rate"])

    def test_02_victory_has_four_active_native_roles_and_priest_rite(self):
        policy = POLICIES[0]
        result = attest_trial(self._case(policy), level=3, seed=17,
                              policy=policy)
        facts = result["source_decisions"]
        self.assertTrue(result["hunter_dead"])
        self.assertEqual(result["party_deaths"], [])
        self.assertEqual(facts["chosen_R_rites"], 1)
        self.assertEqual(facts["flame_launches"], 2)
        self.assertGreater(facts["paid_melee_resolutions"], 2)
        self.assertGreater(facts["bow_hit_adjudications"], 0)
        ledger = self._case(policy)["ledger"]
        chosen = [v for v in ledger if v["kind"] == "g7h_pack_policy_selected"]
        self.assertEqual(len(chosen), 1)
        self.assertEqual(chosen[0]["detail"]["policy"], policy)
        self.assertLess(chosen[0]["index"],
                        next(v["index"] for v in ledger
                             if v["kind"] == "turn_start_expiry"))

    def test_03_loss_contains_unique_sourced_hunter_deaths(self):
        r = attest_trial(self._case(POLICIES[1]), level=3, seed=17,
                         policy=POLICIES[1])
        self.assertFalse(r["hunter_dead"])
        self.assertEqual(r["party_deaths"], list(("vanguard", "guardian",
                                                 "archer", "scholar")))
        self.assertEqual(r["native_terminal_kind"], "g7c_party_defeat_attested")
        self.assertGreater(r["rounds_completed"], 2)

    def test_04_escape_uses_living_hunter_and_four_source_exits(self):
        r = attest_trial(self._case(POLICIES[2]), level=3, seed=17,
                         policy=POLICIES[2])
        self.assertFalse(r["hunter_dead"])
        self.assertEqual(r["party_deaths"], [])
        self.assertEqual(r["rounds_completed"], 2)
        self.assertEqual(r["source_decisions"]["native_exit_receipts"], 4)
        self.assertGreater(r["source_decisions"]["genuine_hunter_pursuit_steps"], 0)

    def test_05_no_policy_relabel_from_wipe_to_escape(self):
        r = self._case(POLICIES[1])
        with self.assertRaises(AssertionError):
            attest_trial(r, level=3, seed=17, policy=POLICIES[2])

    def test_06_forged_report_outcome_or_terminal_is_rejected(self):
        source = self._case(POLICIES[0])
        for corruption in ("outcome", "terminal", "digest"):
            with self.subTest(corruption=corruption):
                r = deepcopy(source)
                if corruption == "outcome":
                    r["outcome"] = "party_withdrawal_attested"
                elif corruption == "terminal":
                    r["native_terminal"]["terminal_event"] = 0
                else:
                    r["ledger_sha256"] = "0" * 64
                with self.assertRaises(AssertionError):
                    attest_trial(r, level=3, seed=17, policy=POLICIES[0])

    def test_07_missing_or_late_native_policy_marker_rejected(self):
        for variant in ("missing", "late", "duplicate", "swapped"):
            with self.subTest(variant=variant):
                r = self._case(POLICIES[0])
                ledger = r["ledger"]
                originals = [x for x in ledger if x["kind"] ==
                             "g7h_pack_policy_selected"]
                self.assertEqual(len(originals), 1)
                selected = originals[0]
                if variant == "missing":
                    selected["kind"] = "other"
                elif variant == "late":
                    selected["round"] = 3
                elif variant == "duplicate":
                    ledger.append(deepcopy(selected))
                    ledger[-1]["index"] = len(ledger)-1
                else:
                    selected["detail"]["policy"] = "opposed_disengagement"
                r["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(r, level=3, seed=17, policy=POLICIES[0])

    def test_08_snapshot_tampering_without_hash_change_is_rejected(self):
        for variant in ("hp", "dead", "digest"):
            with self.subTest(variant=variant):
                r = self._case(POLICIES[1])
                final = r["final_state"]["guardian"]
                if variant == "hp":
                    final["hp"] += 1
                elif variant == "dead":
                    final["dead"] = False
                else:
                    final["source_digest"] = "fake"
                with self.assertRaises(AssertionError):
                    attest_trial(r, level=3, seed=17, policy=POLICIES[1])

    def test_09_signed_but_missing_terminal_is_not_certified(self):
        for policy in POLICIES:
            with self.subTest(policy=policy):
                r = self._case(policy)
                terminal = TERMINALS[policy][1]
                assert sum(e["kind"] == terminal for e in r["ledger"]) == 1
                for event in r["ledger"]:
                    if event["kind"] == terminal:
                        event["kind"] = "nonterminal_observation"
                r["ledger_sha256"] = canonical_digest(r["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(r, level=3, seed=17, policy=policy)

    def test_10_no_open_round_or_pending_action_can_certify(self):
        policy = POLICIES[0]
        r = self._case(policy)
        r["ledger"].append({
            "index": len(r["ledger"]), "round": r["rounds_completed"] + 1,
            "turn": "hunter", "kind": "turn_start_expiry",
            "detail": {"actor": "hunter"}})
        r["ledger_sha256"] = canonical_digest(r["ledger"])
        with self.assertRaises(AssertionError):
            attest_trial(r, level=3, seed=17, policy=policy)

    def test_11_strict_unsupported_P3_and_invalid_inputs(self):
        for kwargs in ({"level": 1}, {"level": True}, {"seed": -1},
                       {"seed": True}, {"include_trials": 2}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_pack(**kwargs)
        for kwargs in ({"level": 4}, {"seed": -1}, {"policy": "not_authored"}):
            opts={"level": 3, "seed": 17, "policy": POLICIES[0]}
            opts.update(kwargs)
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                attest_trial(self._case(POLICIES[0]), **opts)

    def test_12_reproducible_unrated_nonprobabilistic_report_and_cli(self):
        a=run_pack(2, 17)
        b=run_pack(2, 17)
        self.assertEqual(a, b)
        self.assertEqual(a["historical_phase3_sha256"], HISTORICAL_SHA)
        self.assertTrue(a["historical_phase3_not_recomputed"])
        self.assertIsNone(a["human_GM_policy_weights"])
        stream=StringIO()
        with redirect_stdout(stream):
            main(["--level", "2", "--seed", "17"])
        result=json.loads(stream.getvalue())
        self.assertEqual(result, a)
        self.assertNotIn("native_trials", a)


if __name__ == "__main__":
    unittest.main()
