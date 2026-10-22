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




    def test_25_codex_p1_bow_natural_one_cannot_remain_lethal(self):
        """An edited G2 delivery plus edited G6-D summary still misses."""
        trial = self._case(POLICIES[0])
        ledger = trial["ledger"]
        bow = next(v for v in ledger if v["kind"] == "g6d_bow_adjudicated"
                   and (v["detail"].get("damage") or {}).get("dead"))
        shot = ledger[bow["detail"]["shot_index"]]
        for event in (shot,):
            event["detail"]["primary_face"] = 1
            event["detail"]["attack_total"] = 5
            event["detail"]["outcome"] = "automatic_miss"
        bow["detail"]["attack_face"] = 1
        bow["detail"]["attack_total"] = 5
        bow["detail"]["original_outcome"] = "automatic_miss"
        self.assertEqual(bow["detail"]["outcome"], "hit")
        trial["ledger_sha256"] = canonical_digest(ledger)
        with self.assertRaises(AssertionError):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_26_codex_p1_bow_bonus_defense_and_confirmation_provenance(self):
        for attack in ("wrong_bonus", "lowered_defense", "false_confirmation",
                       "false_delivery"):
            with self.subTest(attack=attack):
                trial = self._case(POLICIES[0])
                bow = next(v for v in trial["ledger"]
                           if v["kind"] == "g6d_bow_adjudicated"
                           and (v["detail"].get("damage") or {}).get("dead"))
                shot = trial["ledger"][bow["detail"]["shot_index"]]
                launch = trial["ledger"][bow["detail"]["launch_index"]]
                if attack == "wrong_bonus":
                    shot["detail"]["attack_total"] += 1
                    bow["detail"]["attack_total"] += 1
                elif attack == "lowered_defense":
                    shot["detail"]["final_defense"] -= 1
                elif attack == "false_confirmation":
                    bow["detail"]["confirmation_face"] = 1
                else:
                    shot["detail"]["outcome"] = "automatic_miss"
                    bow["detail"]["original_outcome"] = "automatic_miss"
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_27_codex_p1_hunter_natural_one_rejects_defeat_and_escape(self):
        for policy in POLICIES[1:]:
            with self.subTest(policy=policy):
                trial = self._case(policy)
                rolls = [v for v in trial["ledger"]
                         if v["kind"] == "g5_melee_roll"
                         and v["detail"].get("attacker") == "hunter"
                         and v["detail"].get("profile") == "B06-AT-04"
                         and v["detail"].get("hit") is True]
                self.assertGreater(len(rolls), 0)
                for roll in rolls:
                    roll["detail"]["attack_face"] = 1
                    roll["detail"]["attack_total"] = 7
                    # Leave the cached hit flag TRUE and all lethal G4 and
                    # G4.5/G5 records untouched, as in the Codex witness.
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=policy)

    def test_28_codex_p1_hunter_bonus_and_critical_math_cannot_be_relabelled(self):
        for policy in POLICIES[1:]:
            for kind in ("wrong_bonus", "wrong_critical"):
                with self.subTest(policy=policy, kind=kind):
                    trial = self._case(policy)
                    roll = next(v for v in trial["ledger"]
                                if v["kind"] == "g5_melee_roll"
                                and v["detail"].get("attacker") == "hunter")
                    if kind == "wrong_bonus":
                        roll["detail"]["attack_bonus"] = 7
                        roll["detail"]["attack_total"] = roll["detail"]["attack_face"] + 7
                    else:
                        roll["detail"]["critical"] = "strong"
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=policy)

    def test_29_codex_p1_chosen_rite_requires_native_vp_commitment(self):
        for kind in ("missing", "wrong_actor", "wrong_mode", "wrong_amount"):
            with self.subTest(kind=kind):
                trial = self._case(POLICIES[0])
                ledger = trial["ledger"]
                cost = next(v for v in ledger if v["kind"] == "vp_transition"
                            and v["detail"].get("actor") == "archer"
                            and v["detail"].get("label") == "g3:guided:maintained")
                if kind == "missing":
                    cost["kind"] = "cost_was_not_committed"
                elif kind == "wrong_actor":
                    cost["detail"]["actor"] = "scholar"
                elif kind == "wrong_mode":
                    cost["detail"]["mode"] = "spent"
                else:
                    cost["detail"]["points"] = 2
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_30_codex_p1_flame_needs_own_action_and_vp_for_each_launch(self):
        for choice in ("both", "one_ap", "one_vp", "wrong_round",
                       "wrong_spend", "wrong_label"):
            with self.subTest(choice=choice):
                trial = self._case(POLICIES[0])
                ledger = trial["ledger"]
                actions = [v for v in ledger if v["kind"] == "action_committed"
                           and v["detail"].get("actor") == "scholar"
                           and v["detail"].get("label") == "g3:thrown_flame:T1"]
                costs = [v for v in ledger if v["kind"] == "vp_transition"
                         and v["detail"].get("actor") == "scholar"
                         and v["detail"].get("label") == "g3:thrown_flame:T1"]
                self.assertEqual(len(actions), 2)
                self.assertEqual(len(costs), 2)
                if choice == "both":
                    for v in actions + costs:
                        v["kind"] = "relabeled_unpaid_action"
                elif choice == "one_ap":
                    actions[0]["kind"] = "relabeled_unpaid_action"
                elif choice == "one_vp":
                    costs[1]["kind"] = "relabeled_unpaid_action"
                elif choice == "wrong_round":
                    costs[1]["round"] = 1
                elif choice == "wrong_spend":
                    costs[0]["detail"]["points"] = 1
                else:
                    actions[0]["detail"]["label"] = "g3:unfunded_flame"
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])


    def test_31_codex_p1_player_melee_needs_native_roll_and_g45_hit(self):
        # Attack summaries and the recalculated hash are NOT enough to
        # claim either A or B landed a sourced hit.
        for actor in ("vanguard", "guardian"):
            for lost in ("g5_melee_roll", "g45_attested_hit"):
                with self.subTest(actor=actor, lost=lost):
                    trial = self._case(POLICIES[0])
                    evidence = [event for event in trial["ledger"]
                                if event["kind"] == lost
                                and event["detail"].get("attacker") == actor
                                and event["detail"].get("target") == "hunter"]
                    self.assertGreater(len(evidence), 0)
                    for event in evidence:
                        event["kind"] = "relabeled_native_receipt"
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    # Resolved G5 summaries remain untouched.
                    self.assertTrue(any(
                        ev["kind"] == "g5_melee_resolved"
                        and ev["detail"].get("attacker") == actor
                        for ev in trial["ledger"]))
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_32_codex_p1_player_melee_hit_must_bind_paid_action_and_G4(self):
        for actor in ("vanguard", "guardian"):
            for kind in ("action", "declaration", "damage", "profile"):
                with self.subTest(actor=actor, corruption=kind):
                    trial = self._case(POLICIES[0])
                    ledger = trial["ledger"]
                    hit = next(v for v in ledger
                               if v["kind"] == "g5_melee_resolved"
                               and v["detail"].get("attacker") == actor
                               and v["detail"].get("outcome") == "hit")
                    action_index = hit["detail"]["action_index"]
                    native = next(v for v in ledger if v["kind"] ==
                                  "g5_melee_sequence_attested"
                                  and action_index in
                                  v["detail"].get("action_indices", ()))
                    if kind == "action":
                        ledger[action_index]["detail"]["ap_spent"] = 0
                    elif kind == "declaration":
                        ledger[native["detail"]["declaration_index"]]["detail"][
                            "target"] = "archer"
                    elif kind == "damage":
                        receipts = [v for v in ledger if v["kind"] ==
                                    "g4_damage_applied" and v["turn"] == actor
                                    and v["detail"].get("recipient") == "hunter"]
                        self.assertGreater(len(receipts), 0)
                        for event in receipts:
                            event["kind"] = "relabeled_source_damage"
                    else:
                        receipt = next(v for v in ledger if v["kind"] ==
                                       "g45_attested_hit"
                                       and v["detail"].get("action_index") ==
                                       action_index)
                        receipt["detail"]["profile"] = "B06-AT-04"
                    trial["ledger_sha256"] = canonical_digest(ledger)
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_33_codex_p1_player_melee_natural_one_cannot_hit(self):
        for actor in ("vanguard", "guardian"):
            with self.subTest(actor=actor):
                trial = self._case(POLICIES[0])
                roll = next(v for v in trial["ledger"]
                            if v["kind"] == "g5_melee_roll"
                            and v["detail"].get("attacker") == actor
                            and v["detail"].get("hit") is True)
                roll["detail"]["attack_face"] = 1
                roll["detail"]["attack_total"] = 1 + roll["detail"]["attack_bonus"]
                # Keep false source result labels and G4/G4.5 delivery.
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_34_codex_p1_chosen_guided_rite_must_be_self_targeted(self):
        trial = self._case(POLICIES[0])
        rites = [v for v in trial["ledger"]
                 if v["kind"] == "g3_effect_established"
                 and v["detail"].get("caster") == "archer"
                 and v["detail"].get("effect_kind") == "Guided Regeneration"]
        self.assertEqual(len(rites), 1)
        self.assertEqual(rites[0]["detail"]["recipient"], "archer")
        rites[0]["detail"]["recipient"] = "hunter"
        trial["ledger_sha256"] = canonical_digest(trial["ledger"])
        with self.assertRaises(AssertionError):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_35_codex_p1_flame_hits_must_beat_recorded_defense(self):
        for corruption in ("both_false_hit_faces", "one_false_hit_face",
                           "false_defense", "natural_one"):
            with self.subTest(corruption=corruption):
                trial = self._case(POLICIES[0])
                flames = [v for v in trial["ledger"]
                          if v["kind"] == "g3_flame_launched"
                          and v["detail"].get("caster") == "scholar"]
                self.assertEqual(len(flames), 2)
                targets = flames if corruption == "both_false_hit_faces" else flames[:1]
                for flame in targets:
                    if corruption == "false_defense":
                        flame["detail"]["final_defense"] = 25
                    elif corruption == "natural_one":
                        flame["detail"]["primary_face"] = 1
                        flame["detail"]["attack_total"] = 6
                    else:
                        flame["detail"]["primary_face"] = 2
                        flame["detail"]["attack_total"] = 7
                    # Retain editable direct_hit_pending_G4 outcomes and
                    # actually paid G3/G4 packet/VP chains unchanged.
                    self.assertEqual(
                        flame["detail"]["outcome"], "direct_hit_pending_G4")
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])



    def test_36_p1_lethal_bow_rejects_ordinary_hit_with_devastating_packet(self):
        trial=self._case(POLICIES[0])
        ledger=trial["ledger"]
        bow=next(v for v in ledger if v["kind"]=="g6d_bow_adjudicated"
                 and (v["detail"].get("damage") or {}).get("dead"))
        shot=ledger[bow["detail"]["shot_index"]]
        # The 14-HP G4 packet is untouched, while both mutable G2/G6D
        # receipts agree on an otherwise legal normal (10+4) hit.
        for event in (shot,):
            event["detail"].update(primary_face=10,attack_total=14,
                                   outcome="intended_hit_pending_G5")
        bow["detail"].update(attack_face=10,attack_total=14,
                              confirmation_face=None,critical="normal",
                              original_outcome="intended_hit_pending_G5")
        trial["ledger_sha256"]=canonical_digest(ledger)
        with self.assertRaises(AssertionError):
            attest_trial(trial,level=3,seed=17,policy=POLICIES[0])

    def test_37_p1_bow_die_packet_raw_and_clipping_must_match_source(self):
        for variant in ("raw", "mitigated", "missing", "hp_packets"):
            with self.subTest(variant=variant):
                trial=self._case(POLICIES[0])
                ledger=trial["ledger"]
                bow=next(v for v in ledger if v["kind"]=="g6d_bow_adjudicated"
                         and (v["detail"].get("damage") or {}).get("dead"))
                terminal=next(v for v in ledger
                              if v["kind"]=="g6d_hunter_defeat_attested")
                damage=ledger[terminal["detail"]["lethal_damage_index"]]["detail"]
                if variant=="raw":
                    damage["packets"][0]["raw"]=2
                elif variant=="mitigated":
                    damage["packets"][0]["mitigated"]=2
                elif variant=="missing":
                    damage["packets"]=[]
                else:
                    bow["detail"]["damage"]["hp_packets"]=[2]
                trial["ledger_sha256"]=canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial,level=3,seed=17,policy=POLICIES[0])

    def test_38_p1_bow_paid_ap_and_remainder_required(self):
        for mutation in ("zero_cost", "wrong_cost", "wrong_remaining",
                         "resource_mismatch"):
            with self.subTest(mutation=mutation):
                trial=self._case(POLICIES[0])
                ledger=trial["ledger"]
                bow=next(v for v in ledger if v["kind"]=="g6d_bow_adjudicated"
                         and (v["detail"].get("damage") or {}).get("dead"))
                action=ledger[bow["detail"]["action_index"]]
                if mutation=="zero_cost":
                    action["detail"]["ap_spent"]=0
                elif mutation=="wrong_cost":
                    action["detail"]["ap_spent"]=24
                elif mutation=="wrong_remaining":
                    action["detail"]["ap_remaining"]+=20
                else:
                    resources=next(v for v in ledger
                                   if v["kind"]=="turn_resources"
                                   and v["round"]==action["round"]
                                   and v["turn"]=="archer")
                    resources["detail"]["ap"]+=20
                trial["ledger_sha256"]=canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial,level=3,seed=17,policy=POLICIES[0])

    def test_39_p1_fatal_bite_normal_hit_cannot_keep_17_point_packet(self):
        trial=self._case(POLICIES[1])
        ledger=trial["ledger"]
        roll=next(v for v in ledger if v["kind"]=="g5_melee_roll"
                  and v["detail"].get("attacker")=="hunter"
                  and v["detail"].get("critical")=="devastating")
        action=roll["detail"]["action_index"]
        resolved=next(v for v in ledger if v["kind"]=="g5_melee_resolved"
                      and v["detail"].get("action_index")==action)
        roll["detail"].update(attack_face=2,attack_total=8,
                              confirmation_face=None,critical="normal")
        resolved["detail"]["critical"]="normal"
        # Keep the former lethal G4 raw packet, G4.5 and fatal certificate.
        trial["ledger_sha256"]=canonical_digest(ledger)
        with self.assertRaises(AssertionError):
            attest_trial(trial,level=3,seed=17,policy=POLICIES[1])

    def test_40_p1_bite_raw_mitigation_and_source_receipt_required(self):
        for policy in POLICIES[1:]:
            for mutation in ("raw", "mitigated", "empty", "missing_profile"):
                with self.subTest(policy=policy,mutation=mutation):
                    trial=self._case(policy)
                    ledger=trial["ledger"]
                    bite=next(v for v in ledger if v["kind"]=="g5_melee_roll"
                              and v["detail"].get("attacker")=="hunter")
                    damage=next(v for v in ledger
                                if v["kind"]=="g4_damage_applied"
                                and v["round"]==bite["round"]
                                and v["turn"]=="hunter")
                    if mutation=="raw":
                        damage["detail"]["packets"][0]["raw"]=100
                    elif mutation=="mitigated":
                        damage["detail"]["packets"][0]["mitigated"]=100
                    elif mutation=="empty":
                        damage["detail"]["packets"]=[]
                    else:
                        profile=next(v for v in ledger
                                     if v["kind"]=="g4_profile_hit"
                                     and v["round"]==bite["round"]
                                     and v["turn"]=="hunter")
                        profile["detail"]["critical"]="normal" if (
                            profile["detail"]["critical"]!="normal") else "critical"
                    trial["ledger_sha256"]=canonical_digest(ledger)
                    with self.assertRaises(AssertionError):
                        attest_trial(trial,level=3,seed=17,policy=policy)

    def test_41_p1_victory_hunter_bite_must_have_real_paid_hit(self):
        for mutation in ("natural_one", "unpaid", "missing_profile_packet"):
            with self.subTest(mutation=mutation):
                trial=self._case(POLICIES[0])
                ledger=trial["ledger"]
                bite=next(v for v in ledger if v["kind"]=="g5_melee_roll"
                          and v["round"]==2
                          and v["detail"].get("attacker")=="hunter")
                action=ledger[bite["detail"]["action_index"]]
                if mutation=="natural_one":
                    bite["detail"]["attack_face"]=1
                    bite["detail"]["attack_total"]=7
                elif mutation=="unpaid":
                    action["detail"]["ap_spent"]=0
                else:
                    packet=next(v for v in ledger if v["kind"]=="g4_damage_applied"
                                and v["round"]==2 and v["turn"]=="hunter")
                    packet["detail"]["packets"]=[]
                trial["ledger_sha256"]=canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial,level=3,seed=17,policy=POLICIES[0])

    def test_42_p1_flame_must_have_two_exact_synchronous_packets(self):
        for mutation in ("cleared", "changed_cause", "wrong_fire",
                         "wrong_vigor", "wrong_armor", "changed_turn"):
            with self.subTest(mutation=mutation):
                trial=self._case(POLICIES[0])
                ledger=trial["ledger"]
                flame=next(v for v in ledger if v["kind"]=="g3_flame_launched")
                packet=next(v for v in ledger
                            if v["kind"]=="g4_damage_applied"
                            and v["detail"].get("event_key")==
                                f"g3-flame-ledger:{flame['index']}")
                if mutation=="cleared":
                    packet["detail"]["packets"]=[]
                elif mutation=="changed_cause":
                    packet["detail"]["cause"]="free_unsourced_fire"
                elif mutation=="wrong_fire":
                    packet["detail"]["packets"][0]["raw"]=20
                elif mutation=="wrong_vigor":
                    packet["detail"]["packets"][1]["raw"]=20
                elif mutation=="wrong_armor":
                    packet["detail"]["packets"][0]["armor_rule"]="weapon"
                else:
                    packet["turn"]="hunter"
                trial["ledger_sha256"]=canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial,level=3,seed=17,policy=POLICIES[0])

    def test_43_p2_round_and_turn_boundary_receipts_must_match_chronology(self):
        for policy in POLICIES:
            for mutation in ("round_999", "turn_actor", "turn_round",
                             "duplicate_round", "round_turn", "skipped_turn"):
                with self.subTest(policy=policy,mutation=mutation):
                    trial=self._case(policy)
                    ledger=trial["ledger"]
                    rounds=[v for v in ledger if v["kind"]=="round_end"]
                    turns=[v for v in ledger if v["kind"]=="turn_end"]
                    if mutation=="round_999":
                        rounds[0]["round"]=999
                    elif mutation=="turn_actor":
                        turns[0]["turn"]="archer"
                    elif mutation=="turn_round":
                        turns[0]["round"]+=1
                    elif mutation=="duplicate_round":
                        beginnings=[v for v in ledger if v["kind"]=="round_begin"]
                        beginnings[1]["round"]=1
                    elif mutation=="round_turn":
                        rounds[0]["turn"]="hunter"
                    else:
                        turn_starts=[v for v in ledger
                                     if v["kind"]=="turn_start_expiry"]
                        turn_starts[1]["detail"]["actor"]="scholar"
                    trial["ledger_sha256"]=canonical_digest(ledger)
                    with self.assertRaises(AssertionError):
                        attest_trial(trial,level=3,seed=17,policy=policy)


    def test_44_codex_p1_spell_AP_uses_real_turn_resource_receipt(self):
        # Rehashed spell chains cannot spend 20/30 AP from a source turn
        # whose Step-4 available AP was forged down to zero.
        for actor,label in (("archer", "g3:guided:maintained"),
                            ("scholar", "g3:thrown_flame:T1")):
            exemplar = self._case(POLICIES[0])
            actions = [x for x in exemplar["ledger"]
                       if x["kind"] == "action_committed"
                       and x["detail"].get("actor") == actor
                       and x["detail"].get("label") == label]
            self.assertEqual(len(actions), 1 if actor == "archer" else 2)
            for chosen in range(len(actions)):
                for mutate in ("zero_resources", "wrong_remainder",
                               "forged_surplus_with_matching_remainder"):
                    with self.subTest(actor=actor, turn=chosen, mutate=mutate):
                        trial = self._case(POLICIES[0])
                        ledger = trial["ledger"]
                        action = [x for x in ledger
                                  if x["kind"] == "action_committed"
                                  and x["detail"].get("actor") == actor
                                  and x["detail"].get("label") == label][chosen]
                        resources = next(x for x in ledger
                                         if x["kind"] == "turn_resources"
                                         and x["round"] == action["round"]
                                         and x["turn"] == actor)
                        if mutate == "zero_resources":
                            resources["detail"]["ap"] = 0
                        elif mutate == "wrong_remainder":
                            action["detail"]["ap_remaining"] = 0
                        else:
                            resources["detail"]["ap"] += 20
                            action["detail"]["ap_remaining"] += 20
                        trial["ledger_sha256"] = canonical_digest(ledger)
                        with self.assertRaises(AssertionError):
                            attest_trial(trial, level=3, seed=17,
                                         policy=POLICIES[0])

    def test_45_codex_p1_genesis_source_digest_must_match_fixture(self):
        # Mirroring a fake digest into both snapshots and mutable source
        # receipts does NOT recreate the authored creature/party fixtures.
        for actor in ("hunter", "vanguard", "guardian", "archer", "scholar"):
            with self.subTest(actor=actor):
                trial = self._case(POLICIES[0])
                forged = "a" * 64
                trial["ledger"][0]["detail"]["source_ids"][actor]["digest"] = forged
                trial["initial_state"][actor]["source_digest"] = forged
                trial["final_state"][actor]["source_digest"] = forged
                for entry in trial["ledger"]:
                    detail = entry["detail"]
                    if entry["kind"] == "g45_attested_hit":
                        if detail.get("attacker") == actor:
                            detail["attacker_source"] = forged
                        if detail.get("target") == actor:
                            detail["target_source"] = forged
                    if entry["kind"] == "g5_melee_sequence_attested" and (
                            detail.get("attacker") == actor):
                        detail["source_digest"] = forged
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17,
                                 policy=POLICIES[0])

    def test_46_codex_p1_AB_packets_must_match_weapon_source_and_G4(self):
        # Keep reported HP delta unchanged, corrupt raw and mitigated
        # together, and recompute the only hash. The packet is impossible.
        for actor, profile in (("vanguard", "B06-PC-A-SWORD"),
                               ("guardian", "B06-PC-B-MACE")):
            for mutation in ("raw_and_mitigated_999", "damage_type",
                             "armor_rule", "extra_packet",
                             "cached_hp_packets"):
                with self.subTest(actor=actor, mutation=mutation):
                    trial = self._case(POLICIES[0])
                    ledger = trial["ledger"]
                    packet = next(v for v in ledger
                                  if v["kind"] == "g4_damage_applied"
                                  and v["detail"].get("cause") ==
                                      f"source-profile:{profile}")
                    detail = packet["detail"]
                    if mutation == "raw_and_mitigated_999":
                        detail["packets"][0]["raw"] = 999
                        detail["packets"][0]["mitigated"] = 999
                    elif mutation == "damage_type":
                        detail["packets"][0]["type"] = "Fire"
                    elif mutation == "armor_rule":
                        detail["packets"][0]["armor_rule"] = "none"
                    elif mutation == "extra_packet":
                        detail["packets"].append(dict(detail["packets"][0]))
                    else:
                        bridge = next(v for v in ledger
                                      if v["kind"] == "g45_attested_hit"
                                      and v["detail"].get("attacker") == actor
                                      and v["detail"].get("profile") == profile)
                        bridge["detail"]["actual_result"]["hp_packets"] = [999]
                        resolved = next(v for v in ledger
                                        if v["kind"] == "g5_melee_resolved"
                                        and v["detail"].get("attacker") == actor
                                        and v["detail"].get("profile") == profile
                                        and v["detail"].get("outcome") == "hit"
                                        and v["detail"].get("damage") is not None)
                        resolved["detail"]["damage"]["hp_packets"] = [999]
                    trial["ledger_sha256"] = canonical_digest(ledger)
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17,
                                     policy=POLICIES[0])


    def test_47_codex_p1_AB_melee_replays_source_AP_and_remainder(self):
        # A/B have valid signed 20-AP melee hits, but a hash does NOT
        # authenticate forged Step-4 turn resources or a paid remainder.
        for actor in ("vanguard", "guardian"):
            for mutation in ("zero_turn_AP", "wrong_remainder",
                             "surplus_turn_AP", "overdrawn_prior_payment"):
                with self.subTest(actor=actor, mutation=mutation):
                    trial = self._case(POLICIES[0])
                    ledger = trial["ledger"]
                    action = next(v for v in ledger
                                  if v["kind"] == "action_committed"
                                  and v["turn"] == actor
                                  and v["detail"].get("label", "").startswith("sequence:"))
                    res = next(v for v in ledger
                               if v["kind"] == "turn_resources"
                               and v["round"] == action["round"]
                               and v["turn"] == actor)
                    if mutation == "zero_turn_AP":
                        res["detail"]["ap"] = 0
                    elif mutation == "wrong_remainder":
                        action["detail"]["ap_remaining"] = 0
                    elif mutation == "surplus_turn_AP":
                        res["detail"]["ap"] += 20
                        action["detail"]["ap_remaining"] += 20
                    else:
                        action["detail"]["ap_spent"] += 50
                        action["detail"]["ap_remaining"] -= 50
                    trial["ledger_sha256"] = canonical_digest(ledger)
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17,
                                     policy=POLICIES[0])

    def test_48_codex_p1_legal_wrong_hunter_move_breaks_real_contact(self):
        # A legal 2-MP sideways move is not a legal head-forward Bite.
        # Both moved footprints and the G7-G summary are self-consistent,
        # and the original editable contact=True assertion is left intact.
        trial = self._case(POLICIES[2])
        ledger = trial["ledger"]
        pursuit = next(v for v in ledger
                       if v["kind"] == "g7g_hunter_pursuit_executed"
                       and v["round"] == 2)
        moves = pursuit["detail"]["movement_indices"]
        self.assertEqual(len(moves), 1)
        step = ledger[moves[0]]
        self.assertEqual(step["detail"]["direction"], [-1, 0])
        self.assertEqual(step["detail"]["new"], [[2, 2], [3, 2]])
        step["detail"]["direction"] = [0, -1]
        step["detail"]["new"] = [[3, 1], [4, 1]]
        pursuit["detail"]["final_footprint"] = [[3, 1], [4, 1]]
        self.assertTrue(pursuit["detail"]["contact"])
        trial["ledger_sha256"] = canonical_digest(ledger)
        with self.assertRaisesRegex(AssertionError, "contact"):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[2])

    def test_49_codex_p1_regeneration_requires_HP_cap_and_source_spending(self):
        # Source Scholar starts at full HP. Editing the signed Step-2
        # transcript and final summary cannot conjure HP above Max HP.
        for mutation in ("over_max", "free_HP", "too_much_throughput",
                         "false_vigor", "wrong_hp_arithmetic", "repair_from_nothing"):
            with self.subTest(mutation=mutation):
                trial = self._case(POLICIES[2])
                ledger = trial["ledger"]
                steps = [v for v in ledger if v["kind"] == "regeneration_step"
                         and v["detail"].get("actor") == "scholar"]
                self.assertTrue(steps)
                regen = steps[-1]["detail"]
                if mutation == "over_max":
                    regen["hp_after"] = 999
                    regen["hp_restored"] = 999 - regen["hp_before"]
                    trial["final_state"]["scholar"]["hp"] = 999
                elif mutation == "free_HP":
                    regen["hp_restored"] = 1
                    regen["hp_after"] = regen["hp_before"] + 1
                    regen["throughput_spent"] = 0
                    trial["final_state"]["scholar"]["hp"] += 1
                elif mutation == "too_much_throughput":
                    regen["throughput_spent"] = 99
                elif mutation == "false_vigor":
                    regen["vigor_after"] += 1
                    trial["final_state"]["scholar"]["vigor"] += 1
                elif mutation == "wrong_hp_arithmetic":
                    regen["hp_after"] += 1
                    trial["final_state"]["scholar"]["hp"] += 1
                else:
                    regen["repair_points"] = 1
                    regen["wound_allocations"] = [["fake", 1]]
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[2])

    def test_50_codex_p1_all_victory_terminal_fields_source_derived(self):
        pristine = self._case(POLICIES[0])
        terminal = next(v for v in pristine["ledger"]
                        if v["kind"] == "g6d_hunter_defeat_attested")
        fields = ("hunter", "party", "hp", "source_digest",
                  "round", "outcome", "source_event_cause", "hunter_cr")
        self.assertTrue(all(field in terminal["detail"] for field in fields))
        for mutation in fields + ("all_forged_together",):
            with self.subTest(mutation=mutation):
                trial = self._case(POLICIES[0])
                signed = next(v for v in trial["ledger"]
                              if v["kind"] == "g6d_hunter_defeat_attested")
                fields_to_change = fields[:-1] if mutation == "all_forged_together" else (mutation,)
                for field in fields_to_change:
                    signed["detail"][field] = {
                        "hunter": "other", "party": ["scholar", "vanguard"],
                        "hp": 999, "source_digest": "not-source",
                        "round": 0, "outcome": "noncanonical",
                        "source_event_cause": "unsourced",
                        "hunter_cr": "fake-rating",
                    }[field]
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])


if __name__ == "__main__":
    unittest.main()
