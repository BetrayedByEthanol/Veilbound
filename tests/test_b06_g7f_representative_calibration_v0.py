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
    """Isolated G0/G4-compatible verifier fixture; never gameplay evidence."""
    roster = ("hunter", "vanguard", "guardian", "archer") + (
        ("scholar",) if size == 4 else ())
    sources = ("B06-EN-03", "A", "B", "R") + (("F",) if size == 4 else ())
    initial = {n: {"source_id": src, "source_digest": "hash:" + src,
                   "hp": 24, "dead": False} for n, src in zip(roster, sources)}
    final = deepcopy(initial)
    scenario_id, policy_id, opening, frontline = g7f._policy_origin(
        level, size, policy)
    genesis = {n: {"source_id": src, "digest": "hash:" + src, "hp": 24}
               for n, src in zip(roster, sources)}
    g0_scene = (f"B06-G7E-forest-lane:L{level}:P{size}"
                if policy.startswith("forest_") else
                f"B06-I3-G7D:B-front:party-{size}:L{level}"
                if policy == "b_front" else
                f"B06-I3-G6C:party-{size}:L{level}")
    ledger = [{"index": 0, "round": 0, "kind": "encounter_created",
               "detail": {"scenario": g0_scene, "seed": seed,
                          "source_ids": genesis}}]
    # Pre-turn G0 selection from the native runner is covered by the ledger hash.
    runner, mode = g7f._policy_binding(policy)
    ledger.append({"index": 1, "round": 0, "turn": None,
                   "kind": "g7f_policy_selected",
                   "detail": {"cohort": policy, "runner": runner, "mode": mode,
                              "scenario": g0_scene, "level": level,
                              "party_size": size, "seed": seed}})
    if outcome == "hunter_defeat_attested":
        ledger.append({"index": len(ledger), "round": 1,
                       "kind": "g4_damage_applied",
                       "detail": {"recipient": "hunter", "hp_before": 24,
                                  "hp_after": -24, "dead": True}})
        final["hunter"].update(hp=-24, dead=True)
    offset = len(ledger)
    ledger.extend({"index": offset + i, "round": 1, "kind": "turn_end",
                   "detail": {"actor": n}} for i, n in enumerate(roster))
    ledger.append({"index": len(ledger), "round": 1,
                   "kind": "round_end", "detail": {}})
    if outcome in g7f.CERTIFIED_TERMINALS:
        ledger.append({"index": len(ledger), "round": 1,
                       "kind": g7f.CERTIFIED_TERMINALS[outcome], "detail": {}})
    if outcome == "unresolved_mechanical_branch":
        # A genuine opened Round Begin cannot become a completed cutoff
        # by deleting the mutable exception summary.
        ledger.append({"index": len(ledger), "round": 2,
                       "kind": "round_begin", "detail": {}})
    report = {
        "level": level, "party_size": size, "seed": seed,
        "policy_id": policy_id, "scenario_id": scenario_id,
        "opening": opening, "initial_state": initial, "final_state": final,
        "outcome": outcome,
        "native_terminal": ({"ending": outcome} if outcome
                            in g7f.CERTIFIED_TERMINALS else None),
        "unresolved": ({"reason": "mechanical_gap"}
                       if outcome == "unresolved_mechanical_branch" else None),
        "hunter_cr": None, "complete_party_pack_certified": False,
        "turns_completed": len(roster), "rounds_completed": 1,
        "ledger": ledger, "ledger_sha256": g7f._digest(ledger),
    }
    if frontline is not None:
        report["frontline"] = frontline
    if policy.startswith("forest_"):
        report.update(clock_handoff={"not_a_combat_terminal": True,
                                     "elapsed_seconds": 0},
                      exploration_seconds_requested=0,
                      universal_surprise_benefit_applied=False,
                      native_pounce_count=0, opening_bite=None)
    if policy in ("b_front", *g7f.PROTECTIVE_POLICIES):
        report["protection"] = {"attested_protections": 0}
    return report


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
        report["ledger"][2]["detail"]["actor"] = "guardian"
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
        report["ledger"][2]["detail"]["actor"] = "vanguard"
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
        self.assertEqual(x["unresolved_reason"], "native_turn_or_round_incomplete")

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
            after = 10 if policy == "forest_pounce" else 20
            trial["ledger"].insert(2, {"index": 1, "round": 1,
                "kind": "g4_damage_applied",
                "detail": {"recipient": "hunter", "hp_before": 24,
                           "hp_after": after, "dead": False}})
            for i, event in enumerate(trial["ledger"]):
                event["index"] = i
            trial["ledger_sha256"] = g7f._digest(trial["ledger"])
            trial["final_state"]["hunter"]["hp"] = after
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

    def test_25_rejects_wrong_requested_policy_metadata(self):
        pairs = (("warned_flame", "warned_control"),
                 ("forest_pounce", "forest_ordinary"),
                 ("reactive_shield", "prepared_body"),
                 ("warned_party_exit", "warned_control"))
        for requested, substituted in pairs:
            report = fake_source_trial(3, 4, 11, substituted)
            with self.subTest(requested=requested), self.assertRaisesRegex(
                    AssertionError, "scenario/policy"):
                g7f.attest_native(report, level=3, size=4, seed=11,
                                 policy=requested)
        for key in ("scenario_id", "policy_id", "opening", "frontline"):
            report = fake_source_trial(3, 4, 0, "reactive_shield")
            report[key] = "other"
            with self.subTest(key=key), self.assertRaisesRegex(
                    AssertionError, "scenario/policy"):
                g7f.attest_native(report, level=3, size=4, seed=0,
                                 policy="reactive_shield")

    def test_26_rejects_wrong_pounce_receipt(self):
        report = fake_source_trial(3, 4, 0, "forest_pounce")
        report["opening_bite"] = {"kind": "native_pounce"}
        with self.assertRaisesRegex(AssertionError, "Pounce"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="forest_pounce")
        report = fake_source_trial(3, 4, 0, "forest_ordinary")
        report["native_pounce_count"] = 1
        with self.assertRaisesRegex(AssertionError, "Pounce"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="forest_ordinary")

    def test_27_rejects_snapshot_hp_tamper_with_unchanged_ledger_hash(self):
        for phase, actor in (("initial_state", "vanguard"),
                             ("final_state", "hunter")):
            report = fake_source_trial(3, 4, 0, "warned_control")
            signed = report["ledger_sha256"]
            report[phase][actor]["hp"] += 8
            with self.subTest(phase=phase), self.assertRaisesRegex(
                    AssertionError, "HP"):
                g7f.attest_native(report, level=3, size=4, seed=0,
                                 policy="warned_control")
            self.assertEqual(report["ledger_sha256"], signed)

    def test_28_rejects_false_dead_flag_and_inconsistent_damage_chain(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["final_state"]["hunter"]["dead"] = True
        with self.assertRaisesRegex(AssertionError, "HP/death"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["ledger"].insert(2, {"index": 0, "round": 1,
            "kind": "g4_damage_applied",
            "detail": {"recipient": "hunter", "hp_before": 12,
                       "hp_after": 10, "dead": False}})
        for i, ev in enumerate(report["ledger"]): ev["index"] = i
        report["ledger_sha256"] = g7f._digest(report["ledger"])
        with self.assertRaisesRegex(AssertionError, "transition"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_29_reconciles_damage_regeneration_and_healing(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        transitions = (
            {"kind": "g4_damage_applied", "detail": {
                "recipient": "guardian", "hp_before": 24,
                "hp_after": 15, "dead": False}},
            {"kind": "regeneration_step", "detail": {
                "actor": "guardian", "hp_before": 15,
                "hp_after": 17, "dead": False}},
            {"kind": "g4_basic_heal_applied", "detail": {
                "recipient": "guardian", "hp_restored": 3}},
        )
        for ev in reversed(transitions):
            report["ledger"].insert(2, {"index": 0, "round": 1, **ev})
        for i, ev in enumerate(report["ledger"]): ev["index"] = i
        report["ledger_sha256"] = g7f._digest(report["ledger"])
        report["final_state"]["guardian"]["hp"] = 20
        verified = g7f.attest_native(report, level=3, size=4, seed=0,
                                     policy="warned_control")
        self.assertEqual(verified["party_hp_change"], -4)
        report["final_state"]["guardian"]["hp"] = 21
        with self.assertRaisesRegex(AssertionError, "HP/death"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_30_rejects_forged_snapshot_fingerprints(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        for phase in ("initial_state", "final_state"):
            report[phase]["archer"]["source_digest"] = "forged"
        with self.assertRaisesRegex(AssertionError, "source"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_31_rejects_wrong_policy_exit_terminal(self):
        report = fake_source_trial(3, 4, 0, "warned_archer_exit")
        report["outcome"] = "archer_withdrawal_attested"
        with self.assertRaisesRegex(AssertionError, "Archer exit"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_archer_exit")
        report = fake_source_trial(3, 4, 0, "warned_control",
                                   "party_withdrawal_attested")
        with self.assertRaisesRegex(AssertionError, "Party withdrawal"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")




    def test_32_rejects_real_unresolved_window_hidden_as_cutoff(self):
        report = fake_source_trial(3, 4, 0, "warned_control",
                                   "unresolved_mechanical_branch")
        original_hash = report["ledger_sha256"]
        report["outcome"] = "legal_window_cutoff"
        report["unresolved"] = None
        with self.assertRaisesRegex(AssertionError, "Censored outcome"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")
        self.assertEqual(report["ledger_sha256"], original_hash)

    def test_33_reasons_are_from_ledger_not_mutable_exception(self):
        report = fake_source_trial(3, 4, 0, "warned_control",
                                   "unresolved_mechanical_branch")
        report["unresolved"]["reason"] = "invented_non_source_reason"
        verified = g7f.attest_native(report, level=3, size=4, seed=0,
                                     policy="warned_control")
        self.assertEqual(verified["unresolved_reason"],
                         "native_turn_or_round_incomplete")
        report["outcome"] = "party_defeat_observed"
        report["unresolved"] = None
        with self.assertRaisesRegex(AssertionError, "Censored outcome"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_34_rejects_native_archer_exit_demoted_to_cutoff(self):
        report = fake_source_trial(3, 4, 0, "warned_archer_exit")
        ledger = report["ledger"]
        ledger.insert(-1, {"index": 0, "round": 1,
                           "kind": "g45_withdrawal_attested",
                           "detail": {"actor": "archer", "movement_event_index": 13}})
        ledger.insert(-1, {"index": 0, "round": 1,
                           "kind": "g5_terminal_exit",
                           "detail": {"actor": "archer", "movement_index": 13}})
        for i, event in enumerate(ledger):
            event["index"] = i
        report["ledger_sha256"] = g7f._digest(ledger)
        with self.assertRaisesRegex(AssertionError, "Censored outcome"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_archer_exit")

    def test_35_rejects_fabricated_observed_party_defeat(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["outcome"] = "party_defeat_observed"
        with self.assertRaisesRegex(AssertionError, "Censored outcome"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")
        report["final_state"]["vanguard"]["dead"] = True
        with self.assertRaisesRegex(AssertionError, "HP/death"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")

    def test_36_actual_observed_defeat_requires_each_g4_death(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        ledger = report["ledger"]
        for actor in ("vanguard", "guardian", "archer", "scholar"):
            ledger.insert(-1, {"index": 0, "round": 1,
                               "kind": "g4_damage_applied",
                               "detail": {"recipient": actor, "hp_before": 24,
                                          "hp_after": -24, "dead": True}})
            report["final_state"][actor].update(hp=-24, dead=True)
        for i, event in enumerate(ledger):
            event["index"] = i
        report["ledger_sha256"] = g7f._digest(ledger)
        report["outcome"] = "party_defeat_observed"
        verified = g7f.attest_native(report, level=3, size=4, seed=0,
                                     policy="warned_control")
        self.assertFalse(verified["certified_terminal"])
        self.assertEqual(verified["outcome"], "party_defeat_observed")
        report["outcome"] = "legal_window_cutoff"
        with self.assertRaisesRegex(AssertionError, "Censored outcome"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")



    def test_37_hashed_policy_rejects_control_to_flame_relabel(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        preserved = report["ledger_sha256"]
        report["policy_id"] = g7f._policy_origin(3, 4, "warned_flame")[1]
        with self.assertRaisesRegex(AssertionError, "Hashed native policy binding"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_flame")
        self.assertEqual(report["ledger_sha256"], preserved)

    def test_38_hashed_policy_rejects_unprotected_as_reactive(self):
        report = fake_source_trial(3, 4, 0, "protected_control")
        scenario, label, _, _ = g7f._policy_origin(3, 4, "reactive_shield")
        report["scenario_id"], report["policy_id"] = scenario, label
        report["protection"] = {"attested_protections": 0, "reactive_uses": 99}
        with self.assertRaisesRegex(AssertionError, "Hashed native policy binding"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="reactive_shield")

    def test_39_policy_receipt_must_be_unique_and_pre_turn(self):
        for alteration in ("missing", "late", "duplicate"):
            with self.subTest(alteration=alteration):
                report = fake_source_trial(3, 4, 0, "warned_control")
                ledger = report["ledger"]
                receipt = ledger.pop(1)
                if alteration == "late":
                    ledger.append(receipt)
                elif alteration == "duplicate":
                    ledger.insert(1, receipt)
                    ledger.insert(2, deepcopy(receipt))
                for i, event in enumerate(ledger):
                    event["index"] = i
                report["ledger_sha256"] = g7f._digest(ledger)
                with self.assertRaisesRegex(AssertionError, "Hashed native policy binding"):
                    g7f.attest_native(report, level=3, size=4, seed=0,
                                     policy="warned_control")

    def test_40_policy_or_native_mode_mutation_is_rejected(self):
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["ledger"][1]["detail"]["cohort"] = "warned_flame"
        with self.assertRaisesRegex(AssertionError, "ledger.*hash"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")
        report["ledger_sha256"] = g7f._digest(report["ledger"])
        with self.assertRaisesRegex(AssertionError, "Hashed native policy binding"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")
        report = fake_source_trial(3, 4, 0, "warned_control")
        report["ledger"][1]["detail"]["mode"] = "g7b_flame"
        report["ledger_sha256"] = g7f._digest(report["ledger"])
        with self.assertRaisesRegex(AssertionError, "Hashed native policy binding"):
            g7f.attest_native(report, level=3, size=4, seed=0,
                             policy="warned_control")


class NativeG7FTests(unittest.TestCase):
    """CI exercises real G0–G7 native adapters; no synthetic combat mocks."""
    def test_41_native_runners_prebind_all_four_source_policy_families(self):
        for policy in ("warned_flame", "warned_party_exit",
                       "reactive_shield", "forest_pounce"):
            with self.subTest(policy=policy):
                case = g7f._native_case(3, 4, 0, policy)
                ledger = case["ledger"]
                runner, mode = g7f._policy_binding(policy)
                selection = ledger[1]
                self.assertEqual(selection["kind"], "g7f_policy_selected")
                self.assertEqual(selection["round"], ledger[0]["round"])
                self.assertIsNone(selection["turn"])
                self.assertEqual(selection["detail"]["cohort"], policy)
                self.assertEqual(selection["detail"]["runner"], runner)
                self.assertEqual(selection["detail"]["mode"], mode)
                self.assertEqual(case["ledger_sha256"], g7f._digest(ledger))
                self.assertEqual(g7f.attest_native(
                    case, level=3, size=4, seed=0, policy=policy)["policy"], policy)

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
