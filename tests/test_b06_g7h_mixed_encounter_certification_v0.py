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


    def test_13_native_paid_slot_cannot_vanish_from_source_ledger(self):
        policy=POLICIES[0]
        trial=self._case(policy)
        resolutions=[v for v in trial["ledger"] if v["kind"]=="g5_melee_resolved"]
        self.assertTrue(resolutions)
        resolutions[0]["kind"]="missing_paid_slot_resolution"
        trial["ledger_sha256"]=canonical_digest(trial["ledger"])
        with self.assertRaises(AssertionError):
            attest_trial(trial,level=3,seed=17,policy=policy)

    def test_14_uninstrumented_legacy_g6d_victory_unchanged(self):
        from scripts.b06_hunter_completion_g6d_v0 import run_i3_defeat
        original=run_i3_defeat(level=3,seed=640)
        self.assertEqual(original["terminal"]["ending"],"hunter_defeat_attested")
        self.assertTrue(original["hunter_dead"])
        self.assertEqual(original["rounds"],3)
        self.assertFalse(any(v["kind"]=="g7h_pack_policy_selected"
                             for v in original["ledger"]))
        self.assertFalse(original["complete_party_pack_certified"])


    def test_15_codex_p1_defeat_cannot_cancel_all_four_lethal_bites(self):
        """A real G4 death does not survive removal of its G5 resolve."""
        trial = self._case(POLICIES[1])
        lethal = [x for x in trial["ledger"]
                  if x["kind"] == "g5_melee_resolved"
                  and x["detail"].get("attacker") == "hunter"
                  and (x["detail"].get("damage") or {}).get("dead") is True]
        self.assertEqual(len(lethal), 4)
        for event in lethal:
            event["kind"] = "g5_melee_cancelled"
        trial["ledger_sha256"] = canonical_digest(trial["ledger"])
        with self.assertRaises(AssertionError):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[1])

    def test_16_codex_p1_lone_lethal_bite_needs_roll_and_g45(self):
        for missing_kind in ("g5_melee_roll", "g45_attested_hit",
                             "g5_melee_resolved", "action_committed"):
            with self.subTest(missing_kind=missing_kind):
                trial = self._case(POLICIES[1])
                ledger = trial["ledger"]
                fatal = next(x for x in ledger if x["kind"] == "g5_melee_resolved"
                             and x["detail"].get("attacker") == "hunter"
                             and (x["detail"].get("damage") or {}).get("dead") is True)
                action_index = fatal["detail"]["action_index"]
                if missing_kind == "action_committed":
                    ledger[action_index]["kind"] = "missing_paid_action"
                elif missing_kind == "g5_melee_resolved":
                    fatal["kind"] = "g5_melee_cancelled"
                else:
                    hit = next(x for x in ledger if x["kind"] == missing_kind
                               and x["detail"].get("action_index") == action_index)
                    hit["kind"] = "missing_source_proof"
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[1])

    def test_17_codex_p1_withdrawal_requires_two_resolved_hunter_bites(self):
        for removed in ("both", "round2", "roll2", "bridge2"):
            with self.subTest(removed=removed):
                trial = self._case(POLICIES[2])
                ledger = trial["ledger"]
                bites = [x for x in ledger if x["kind"] == "g5_melee_resolved"
                         and x["detail"].get("attacker") == "hunter"
                         and x["detail"].get("target") == "vanguard"]
                self.assertEqual([x["round"] for x in bites], [1, 2])
                if removed == "both":
                    for event in bites:
                        event["kind"] = "g5_melee_cancelled"
                elif removed == "round2":
                    bites[1]["kind"] = "g5_melee_cancelled"
                else:
                    action_index = bites[1]["detail"]["action_index"]
                    kind = ("g5_melee_roll" if removed == "roll2"
                            else "g45_attested_hit")
                    event = next(x for x in ledger if x["kind"] == kind
                                 and x["detail"].get("action_index") == action_index)
                    event["kind"] = "source_bite_evidence_missing"
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[2])

    def test_18_codex_p1_withdrawal_requires_four_g45_exits(self):
        for removed in ("all", "one"):
            with self.subTest(removed=removed):
                trial = self._case(POLICIES[2])
                bridge = [x for x in trial["ledger"]
                          if x["kind"] == "g45_withdrawal_attested"]
                self.assertEqual(len(bridge), 4)
                for event in bridge if removed == "all" else bridge[:1]:
                    event["kind"] = "g45_source_attestation_missing"
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[2])

    def test_19_exit_chain_policy_move_and_round_tampering(self):
        for broken in ("auth_policy", "auth_square", "g5_policy", "g45_policy",
                       "move_kind", "move_cell", "move_actor", "move_round",
                       "exit_round", "terminal_receipt", "missing_move"):
            with self.subTest(broken=broken):
                trial = self._case(POLICIES[2])
                ledger = trial["ledger"]
                actor = "guardian"
                auth = next(e for e in ledger if e["kind"] ==
                            "g5_scene_exit_authored"
                            and e["detail"].get("actor") == actor)
                g5 = next(e for e in ledger if e["kind"] == "g5_terminal_exit"
                          and e["detail"].get("actor") == actor)
                g45 = next(e for e in ledger if e["kind"] ==
                           "g45_withdrawal_attested"
                           and e["detail"].get("actor") == actor)
                move = ledger[g5["detail"]["movement_index"]]
                end = next(e for e in ledger
                           if e["kind"] == "g7c_party_withdrawal_attested")
                if broken == "auth_policy":
                    auth["detail"]["policy"] = "unauthorized_exit"
                elif broken == "auth_square":
                    auth["detail"]["square"] = [0, 0]
                elif broken == "g5_policy":
                    g5["detail"]["policy"] = "unauthorized_exit"
                elif broken == "g45_policy":
                    g45["detail"]["exit_policy_reference"] = "unauthorized_exit"
                elif broken == "move_kind":
                    move["detail"]["step_kind"] = "pivot"
                elif broken == "move_cell":
                    move["detail"]["new"] = [[0, 0]]
                elif broken == "move_actor":
                    move["detail"]["actor"] = "vanguard"
                elif broken == "move_round":
                    move["round"] = 1
                elif broken == "exit_round":
                    g5["round"] = 1
                elif broken == "terminal_receipt":
                    end["detail"]["member_exits"][1]["g45"] = 0
                else:
                    move["kind"] = "g1_step_cancelled"
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[2])

    def test_20_exit_after_source_departure_cannot_resume_movement(self):
        trial = self._case(POLICIES[2])
        ledger = trial["ledger"]
        exiting = next(e for e in ledger if e["kind"] == "g5_terminal_exit"
                       and e["detail"].get("actor") == "vanguard")
        # Reinterpret a harmless later event as an illicit G1 step by the
        # already-exited Vanguard. Do not alter any original event indices.
        candidate = next(e for e in ledger if e["index"] > exiting["index"]
                         and e["kind"] == "g45_native_turn_started"
                         and e["turn"] == "guardian")
        candidate["kind"] = "g1_movement_step"
        candidate["detail"]["actor"] = "vanguard"
        trial["ledger_sha256"] = canonical_digest(ledger)
        with self.assertRaises(AssertionError):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[2])

    def test_21_codex_p1_victory_lethal_index_must_point_to_real_bow_death(self):
        for corruption in ("nonlethal_g4", "wrong_source_cause",
                           "wrong_action", "wrong_shot", "wrong_launch",
                           "fabricated_summary", "wrong_event_key"):
            with self.subTest(corruption=corruption):
                r = self._case(POLICIES[0])
                ledger = r["ledger"]
                terminal = next(v for v in ledger
                                if v["kind"] == "g6d_hunter_defeat_attested")
                bow = next(v for v in ledger
                           if v["kind"] == "g6d_bow_adjudicated"
                           and (v["detail"].get("damage") or {}).get("dead"))
                fatal = ledger[terminal["detail"]["lethal_damage_index"]]
                if corruption == "nonlethal_g4":
                    nonlethal = next(v for v in ledger
                                    if v["kind"] == "g4_damage_applied"
                                    and v["detail"].get("recipient") == "hunter"
                                    and v["detail"].get("dead") is False)
                    terminal["detail"]["lethal_damage_index"] = nonlethal["index"]
                elif corruption == "wrong_source_cause":
                    fatal["detail"]["cause"] = "g6d:source_bow:archer:0"
                elif corruption == "wrong_action":
                    bow["detail"]["action_index"] = 0
                elif corruption == "wrong_shot":
                    bow["detail"]["shot_index"] = 0
                elif corruption == "wrong_launch":
                    bow["detail"]["launch_index"] = 0
                elif corruption == "fabricated_summary":
                    bow["detail"]["damage"]["hp_loss"] += 1
                else:
                    fatal["detail"]["event_key"] = "fake-bow-event"
                r["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(r, level=3, seed=17, policy=POLICIES[0])

    def test_22_codex_p1_withdrawal_rejects_teleport_and_movement_cost(self):
        for corruption in ("outside_old", "broken_previous", "changed_direction",
                           "discounted_cost", "false_mp_remaining",
                           "extra_destination", "wrong_step_kind"):
            with self.subTest(corruption=corruption):
                r = self._case(POLICIES[2])
                ledger = r["ledger"]
                exit_event = next(x for x in ledger if x["kind"] ==
                                  "g5_terminal_exit"
                                  and x["detail"].get("actor") == "guardian")
                move = ledger[exit_event["detail"]["movement_index"]]
                d = move["detail"]
                if corruption == "outside_old":
                    d["old"] = [[100, 100]]
                elif corruption == "broken_previous":
                    d["old"] = [[2, 2]]
                elif corruption == "changed_direction":
                    d["direction"] = [1, 0]
                elif corruption == "discounted_cost":
                    d["cost"] = 1
                elif corruption == "false_mp_remaining":
                    d["mp_remaining"] += 1
                elif corruption == "extra_destination":
                    d["new"] = [[100, 100]]
                else:
                    d["step_kind"] = "diagonal"
                r["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(r, level=3, seed=17, policy=POLICIES[2])

    def test_23_codex_p1_replay_all_moves_not_just_final_exit(self):
        for corruption in ("initial_footprint", "authored_map",
                           "midpath_position", "midpath_cost"):
            with self.subTest(corruption=corruption):
                r = self._case(POLICIES[2])
                ledger = r["ledger"]
                if corruption == "initial_footprint":
                    ledger[0]["detail"]["source_ids"]["guardian"]["occupied"] = [[100, 100]]
                elif corruption == "authored_map":
                    grid = next(v for v in ledger if v["kind"] == "g1_map_installed")
                    grid["detail"]["width"] = 100
                else:
                    intermediate = next(v for v in ledger
                                        if v["kind"] == "g1_movement_step"
                                        and v["round"] == 1
                                        and v["detail"].get("actor") == "guardian")
                    if corruption == "midpath_position":
                        intermediate["detail"]["old"] = [[100, 100]]
                    else:
                        intermediate["detail"]["cost"] = 1
                r["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(r, level=3, seed=17, policy=POLICIES[2])

    def test_24_legitimate_P4_exits_replay_across_L2_and_L3(self):
        for level in (2, 3):
            with self.subTest(level=level):
                r = run_pack(level, 17, include_trials=True)
                trial = r["native_trials"][POLICIES[2]]
                result = attest_trial(trial, level=level, seed=17,
                                      policy=POLICIES[2])
                self.assertEqual(result["outcome"], "party_withdrawal_attested")
                self.assertEqual(result["source_decisions"]["native_exit_receipts"], 4)




if __name__ == "__main__":
    unittest.main()
