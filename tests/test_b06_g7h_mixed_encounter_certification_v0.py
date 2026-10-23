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
        with self.assertRaisesRegex(AssertionError, "contact|pursuit"):
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


    def test_51_codex_p1_G7C_every_signed_terminal_field_is_canonical(self):
        """A self-consistent recomputed SHA must not certify forged G7-C."""
        for policy in POLICIES[1:]:
            terminal_kind = TERMINALS[policy][1]
            proof_key = ("lethal_damage_indices"
                         if policy == POLICIES[1] else "member_exits")
            for mutation in ("detail_round_999", "detail_round_earlier",
                             "detail_hunter_cr", "detail_party",
                             "detail_missing_field", "detail_extra_field",
                             "detail_evidence", "event_round",
                             "event_turn", "receipt_extra_field",
                             "receipt_missing_rating"):
                with self.subTest(policy=policy, mutation=mutation):
                    trial = self._case(policy)
                    signed = next(ev for ev in trial["ledger"]
                                  if ev["kind"] == terminal_kind)
                    if mutation == "detail_round_999":
                        signed["detail"]["round"] = 999
                    elif mutation == "detail_round_earlier":
                        signed["detail"]["round"] = 1
                    elif mutation == "detail_hunter_cr":
                        signed["detail"]["hunter_cr"] = "fabricated-CR"
                    elif mutation == "detail_party":
                        signed["detail"]["party"] = ["vanguard"]
                    elif mutation == "detail_missing_field":
                        signed["detail"].pop("hunter_cr")
                    elif mutation == "detail_extra_field":
                        signed["detail"]["certified"] = True
                    elif mutation == "detail_evidence":
                        signed["detail"][proof_key] = []
                    elif mutation == "event_round":
                        signed["round"] = 999
                    elif mutation == "event_turn":
                        signed["turn"] = "archer"
                    elif mutation == "receipt_extra_field":
                        trial["native_terminal"]["invented"] = "accepted"
                    else:
                        trial["native_terminal"].pop("hunter_cr")
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=policy)

    def test_52_codex_p2_closing_snapshot_matches_replayed_all_actor_positions(self):
        """Submitted snapshots are untrusted even with a genuine ledger hash."""
        for actor in ("hunter", "vanguard", "guardian", "archer", "scholar"):
            for mutation in ("outside_grid", "different_inside_grid",
                             "malformed_footprint"):
                with self.subTest(actor=actor, mutation=mutation):
                    trial = self._case(POLICIES[2])
                    original = deepcopy(trial["final_state"][actor]["occupied"])
                    if mutation == "outside_grid":
                        position = [[99, 99]]
                    elif mutation == "different_inside_grid":
                        position = [[(original[0][0] + 1) % 8, original[0][1]]]
                    else:
                        position = [[0, 0], [0, 0], [0, 0]]
                    trial["final_state"][actor]["occupied"] = position
                    # final_state is not inside the native ledger digest.
                    self.assertEqual(
                        trial["ledger_sha256"], canonical_digest(trial["ledger"]))
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=POLICIES[2])

    def test_53_codex_p2_legitimate_L2_L3_footprints_remain_certified(self):
        for level in (2, 3):
            with self.subTest(level=level):
                trial = run_pack(level, 17, include_trials=True)[
                    "native_trials"][POLICIES[2]]
                proof = attest_trial(trial, level=level, seed=17,
                                     policy=POLICIES[2])
                self.assertEqual(proof["outcome"],
                                 "party_withdrawal_attested")
                self.assertEqual(
                    set(trial["final_state"]),
                    {"hunter", "vanguard", "guardian", "archer", "scholar"})


    def test_54_codex_p1_coordinated_zero_arrow_lethal_bow_rejected(self):
        """A rehashed declaration/launch/resolution/final-state counterfeit.

        AP and the lethal 20/20 roll remain valid; only native ammunition
        provenance is forged across all affected receipts.
        """
        trial = self._case(POLICIES[0])
        ledger = trial["ledger"]
        bow = next(ev for ev in ledger
                   if ev["kind"] == "g6d_bow_adjudicated"
                   and (ev["detail"].get("damage") or {}).get("dead"))
        launch = ledger[bow["detail"]["launch_index"]]
        shot = ledger[bow["detail"]["shot_index"]]
        declaration = next(ev for ev in ledger[:launch["index"]]
                           if ev["kind"] == "g2_bow_sequence_committed"
                           and ev["round"] == bow["round"])
        self.assertEqual(declaration["detail"]["ammunition_selected"], 1)
        self.assertEqual(shot["detail"]["ammunition_spent"], 1)
        declaration["detail"]["ammunition_selected"] = 0
        launch["detail"]["ammo_remaining"] += 1
        shot["detail"]["ammunition_spent"] = 0
        trial["final_state"]["archer"]["ammunition"] += 1
        trial["ledger_sha256"] = canonical_digest(ledger)
        with self.assertRaisesRegex(AssertionError, "arrow"):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_55_codex_p1_bow_chain_debit_and_source_closing_inventory(self):
        for round_no in (2, 3):
            for variant in ("selected", "launch", "spent", "missing_launch",
                            "missing_resolution", "wrong_shot_face"):
                with self.subTest(round=round_no, variant=variant):
                    trial = self._case(POLICIES[0])
                    ledger = trial["ledger"]
                    declaration = next(v for v in ledger
                                       if v["kind"] == "g2_bow_sequence_committed"
                                       and v["round"] == round_no)
                    launch = next(v for v in ledger
                                  if v["kind"] == "g2_bow_launched"
                                  and v["round"] == round_no)
                    resolution = next(v for v in ledger
                                      if v["kind"] == "g2_bow_shot_resolved"
                                      and v["round"] == round_no)
                    if variant == "selected":
                        declaration["detail"]["ammunition_selected"] = 0
                    elif variant == "launch":
                        launch["detail"]["ammo_remaining"] += 1
                    elif variant == "spent":
                        resolution["detail"]["ammunition_spent"] = 0
                    elif variant == "missing_launch":
                        launch["kind"] = "unsigned_bow_launch"
                    elif variant == "missing_resolution":
                        resolution["kind"] = "unsigned_bow_resolution"
                    else:
                        resolution["detail"]["primary_face"] = 10
                        resolution["detail"]["attack_total"] = 14
                    trial["ledger_sha256"] = canonical_digest(ledger)
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=POLICIES[0])
        for variant in ("source_start", "final_inventory"):
            with self.subTest(variant=variant):
                trial = self._case(POLICIES[0])
                if variant == "source_start":
                    trial["initial_state"]["archer"]["ammunition"] += 1
                else:
                    trial["final_state"]["archer"]["ammunition"] += 1
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_56_codex_p1_flame_authored_d20_and_d8_cannot_be_substituted(self):
        """Both original G6-C (12, 3) casts must survive digest rewrites."""
        for round_no in (1, 2):
            for variant in ("legal_alternative_hit", "legal_alternative_vigor_die"):
                with self.subTest(round=round_no, variant=variant):
                    trial = self._case(POLICIES[0])
                    ledger = trial["ledger"]
                    flame = next(ev for ev in ledger
                                 if ev["kind"] == "g3_flame_launched"
                                 and ev["round"] == round_no)
                    detail = flame["detail"]
                    self.assertEqual((detail["primary_face"], detail["die"]),
                                     (12, 3))
                    if variant == "legal_alternative_hit":
                        detail["primary_face"] = 10
                        detail["attack_total"] = 15
                    else:
                        # 2 and 3 yield identical ceil(d8 / 3) packet,
                        # so the native G4 damage remains coherent.
                        detail["die"] = 2
                    trial["ledger_sha256"] = canonical_digest(ledger)
                    with self.assertRaisesRegex(AssertionError, "fixed G6-C Scholar roll"):
                        attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_57_legitimate_fixed_Bow_and_Flame_receipts_L2_and_L3(self):
        from scripts.b05_bow_vanguard_l1_l3_v0 import profile as bow_sheet
        for level in (2, 3):
            with self.subTest(level=level):
                bundle = run_pack(level, 17, include_trials=True)
                native = bundle["native_trials"][POLICIES[0]]
                events = native["ledger"]
                declarations = [ev for ev in events
                                if ev["kind"] == "g2_bow_sequence_committed"]
                launches = [ev for ev in events
                            if ev["kind"] == "g2_bow_launched"]
                shots = [ev for ev in events
                         if ev["kind"] == "g2_bow_shot_resolved"]
                flames = [ev for ev in events
                          if ev["kind"] == "g3_flame_launched"]
                start = bow_sheet(level)["initial_arrows"]
                self.assertEqual(native["initial_state"]["archer"]["ammunition"], start)
                self.assertEqual([x["detail"]["ammunition_selected"]
                                  for x in declarations], [1, 1])
                self.assertEqual([x["detail"]["ammo_remaining"] for x in launches],
                                 [start - 1, start - 2])
                self.assertEqual([x["detail"]["ammunition_spent"] for x in shots],
                                 [1, 1])
                self.assertEqual(native["final_state"]["archer"]["ammunition"],
                                 start - 2)
                self.assertEqual([(x["round"], x["detail"]["primary_face"],
                                   x["detail"]["die"]) for x in flames],
                                 [(1, 12, 3), (2, 12, 3)])
                self.assertEqual(
                    attest_trial(native, level=level, seed=17,
                                 policy=POLICIES[0])["outcome"],
                    "hunter_defeat_attested")


    def test_58_codex_p1_every_hunter_bite_requires_original_declared_defense(self):
        for policy in POLICIES:
            native = self._case(policy)
            bites = [v for v in native["ledger"]
                     if v["kind"] == "g5_melee_resolved"
                     and v["detail"].get("attacker") == "hunter"
                     and v["detail"].get("profile") == "B06-AT-04"
                     and v["detail"].get("outcome") == "hit"]
            self.assertTrue(bites)
            for bite in bites:
                for variant in ("declaration_defense", "assigned_attack_key"):
                    with self.subTest(policy=policy, action=bite["detail"]["action_index"],
                                      variant=variant):
                        trial = deepcopy(native)
                        ledger = trial["ledger"]
                        paid = bite["detail"]["action_index"]
                        native_seq = next(
                            v for v in ledger
                            if v["kind"] == "g5_melee_sequence_attested"
                            and paid in v["detail"].get("action_indices", ()))
                        position = native_seq["detail"]["action_indices"].index(paid)
                        declaration = ledger[
                            native_seq["detail"]["declaration_index"]]
                        assigned = ledger[
                            native_seq["detail"]["defense_indices"][position]]
                        self.assertEqual(
                            declaration["detail"]["defenses"][position], "take_hit")
                        self.assertEqual(
                            assigned["detail"]["attack_key"],
                            f"hunter:{bite['detail']['target']}:{position}")
                        if variant == "declaration_defense":
                            declaration["detail"]["defenses"][position] = "guard"
                        else:
                            assigned["detail"]["attack_key"] = "hunter:forged:0"
                        trial["ledger_sha256"] = canonical_digest(ledger)
                        with self.assertRaisesRegex(
                                AssertionError, "Native Hunter Bite defense was altered"):
                            attest_trial(trial, level=3, seed=17, policy=policy)

    def test_59_codex_p2_victory_must_be_signed_after_last_round_end(self):
        trial = self._case(POLICIES[0])
        ledger = trial["ledger"]
        last_round = max(v["index"] for v in ledger
                         if v["kind"] == "round_end")
        terminal = next(v for v in ledger
                        if v["kind"] == "g6d_hunter_defeat_attested")
        self.assertGreater(terminal["index"], last_round)
        ledger.pop(terminal["index"])
        ledger.insert(last_round, terminal)
        for index, event in enumerate(ledger):
            event["index"] = index
        trial["native_terminal"]["terminal_event"] = terminal["index"]
        trial["ledger_sha256"] = canonical_digest(ledger)
        with self.assertRaisesRegex(
                AssertionError, "G6-D victory terminal is not the complete canonical"):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_60_codex_p2_wipe_receipt_reconstructs_every_native_field(self):
        policy = POLICIES[1]
        original = self._case(policy)
        proof = next(v for v in original["ledger"]
                     if v["kind"] == "g7g_multitarget_defeat_verified")
        self.assertEqual(proof["detail"]["party"],
                         ["vanguard", "guardian", "archer", "scholar"])
        self.assertEqual(proof["detail"]["distinct_targets"],
                         ["vanguard", "guardian", "archer", "scholar"])
        self.assertTrue(proof["detail"]["hunter_alive"])
        for field, fake in (
                ("party", []),
                ("distinct_targets", []),
                ("lethal_damage_indices", []),
                ("hunter_alive", False)):
            with self.subTest(field=field):
                trial = deepcopy(original)
                receipt = next(v for v in trial["ledger"]
                               if v["kind"] == "g7g_multitarget_defeat_verified")
                receipt["detail"][field] = fake
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaisesRegex(
                        AssertionError, "G7-G full defeat verification"):
                    attest_trial(trial, level=3, seed=17, policy=policy)

    def test_61_codex_p2_wipe_targets_cannot_be_rewritten_with_receipt(self):
        policy = POLICIES[1]
        trial = self._case(policy)
        ledger = trial["ledger"]
        chosen = next(v for v in ledger
                      if v["kind"] == "g7g_hunter_target_selected")
        pursuit = next(v for v in ledger
                       if v["kind"] == "g7g_hunter_pursuit_executed")
        verified = next(v for v in ledger
                        if v["kind"] == "g7g_multitarget_defeat_verified")
        self.assertEqual(chosen["detail"]["target"], "vanguard")
        self.assertEqual(pursuit["detail"]["target"], "vanguard")
        chosen["detail"]["target"] = "guardian"
        chosen["detail"]["target_source"] = "B"
        pursuit["detail"]["target"] = "guardian"
        verified["detail"]["distinct_targets"] = [
            "guardian", "vanguard", "archer", "scholar"]
        trial["ledger_sha256"] = canonical_digest(ledger)
        with self.assertRaisesRegex(
                AssertionError, "target choices contradict original Hunter turns"):
            attest_trial(trial, level=3, seed=17, policy=policy)


    def test_62_p1_first_round_hunter_miss_requires_original_24_AP(self):
        """An unpaid natural-1 attack must never disappear behind hit-only auditing."""
        original = self._case(POLICIES[0])
        payments = [v for v in original["ledger"]
                    if v["kind"] == "action_committed"
                    and v["round"] == 1
                    and v["detail"].get("actor") == "hunter"
                    and v["detail"].get("label") ==
                       "sequence:B06-AT-04:0"]
        self.assertEqual(len(payments), 1)
        self.assertEqual(payments[0]["detail"]["ap_spent"], 24)
        self.assertEqual(payments[0]["detail"]["ap_remaining"], 18)
        for variant in ("no_debit", "wrong_balance", "miss_disappears"):
            with self.subTest(variant=variant):
                trial = deepcopy(original)
                ledger = trial["ledger"]
                receipt = ledger[payments[0]["index"]]
                if variant == "no_debit":
                    receipt["detail"]["ap_spent"] = 0
                    receipt["detail"]["ap_remaining"] = 42
                elif variant == "wrong_balance":
                    receipt["detail"]["ap_remaining"] = 42
                else:
                    outcome = next(v for v in ledger
                                   if v["kind"] == "g5_melee_resolved"
                                   and v["round"] == 1
                                   and v["detail"].get("attacker") == "hunter")
                    outcome["kind"] = "g5_melee_unresolved_forged"
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_63_p2_every_branch_rejects_inconsistent_complete_snapshots(self):
        for policy in POLICIES:
            source = self._case(policy)
            for variant in ("source_id", "hp_max", "dying",
                            "wounds", "extra_key", "initial_dying",
                            "initial_hp_max"):
                with self.subTest(policy=policy, variant=variant):
                    trial = deepcopy(source)
                    target = trial["final_state"]["guardian"]
                    if variant == "source_id":
                        target["source_id"] = "forged:B"
                    elif variant == "hp_max":
                        target["hp_max"] += 3
                    elif variant == "dying":
                        target["dying"] = not target["dying"]
                    elif variant == "wounds":
                        # The full-wipe branch carries an actual G4 wound.
                        # Other branches must still reject arbitrary
                        # invented wound history.
                        if target["wounds"]:
                            target["wounds"].pop()
                        else:
                            target["wounds"].append(
                                {"id": "G4-W9999", "severity": "Critical",
                                 "progress": 0, "requirement": 30})
                    elif variant == "extra_key":
                        target["unlogged_condition"] = True
                    elif variant == "initial_dying":
                        trial["initial_state"]["guardian"]["dying"] = True
                    elif variant == "initial_hp_max":
                        trial["initial_state"]["guardian"]["hp_max"] += 1
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=policy)

    def test_64_p2_full_wound_identity_requirement_and_progress_replay(self):
        original = self._case(POLICIES[1])
        victims = [name for name in ("vanguard", "guardian", "archer", "scholar")
                   if original["final_state"][name]["wounds"]]
        self.assertTrue(victims, "G7-G loss should carry at least one G4 wound")
        victim = victims[0]
        for variant in ("delete", "id", "severity", "requirement", "progress"):
            with self.subTest(victim=victim, variant=variant):
                trial = deepcopy(original)
                wound = trial["final_state"][victim]["wounds"][0]
                if variant == "delete":
                    trial["final_state"][victim]["wounds"].clear()
                elif variant == "id":
                    wound["id"] = "G4-W4444"
                elif variant == "severity":
                    wound["severity"] = "Serious" if wound["severity"] != "Serious" else "Critical"
                elif variant == "requirement":
                    wound["requirement"] += 1
                else:
                    wound["progress"] += 1
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17,
                                 policy=POLICIES[1])


    def test_65_p2_bite_wound_location_and_trauma_follow_source_d20(self):
        original = self._case(POLICIES[1])
        created = [v for v in original["ledger"]
                   if v["kind"] == "g4_wound_created"]
        self.assertTrue(created)
        for field, replacement in (
                ("location", "Invented anatomical location"),
                ("location", "Head / neck"),
                ("trauma", "Fire"),
                ("trauma", "Cut")):
            with self.subTest(field=field, replacement=replacement):
                trial = deepcopy(original)
                witness = next(v for v in trial["ledger"]
                               if v["kind"] == "g4_wound_created")
                self.assertEqual(witness["detail"]["location"], "Chest")
                self.assertEqual(witness["detail"]["trauma"], "Piercing")
                witness["detail"][field] = replacement
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[1])

    def test_66_p2_coordinated_valid_severity_downgrade_cannot_certify(self):
        trial = self._case(POLICIES[1])
        wound = next(v for v in trial["ledger"] if v["kind"] == "g4_wound_created")
        wd = wound["detail"]
        self.assertEqual(wd["severity"], "Critical")
        actor, key = wd["recipient"], wd["event_key"]
        matching = [v for v in trial["ledger"]
                    if v["kind"] == "g4_damage_applied"
                    and v["detail"].get("recipient") == actor
                    and v["detail"].get("event_key") == key]
        self.assertEqual(len(matching), 1)
        damage = matching[0]
        wd["severity"] = "Serious"
        wd["requirement"] = 10
        damage["detail"]["wound"] = "Serious"
        # Reconcile every *editable* G4.5/G5 summary and closing wound
        # snapshot, so simple consistency checks cannot identify the edit.
        for ev in trial["ledger"]:
            if (ev["kind"] == "g45_attested_hit"
                    and ev["detail"].get("attacker") == "hunter"
                    and ev["detail"].get("target") == actor
                    and damage["index"] < ev["index"]
                    and (ev["detail"].get("actual_result") or {}).get("wound")
                    == "Critical"):
                ev["detail"]["actual_result"]["wound"] = "Serious"
            if (ev["kind"] == "g5_melee_resolved"
                    and ev["detail"].get("attacker") == "hunter"
                    and ev["detail"].get("target") == actor
                    and damage["index"] < ev["index"]
                    and (ev["detail"].get("damage") or {}).get("wound")
                    == "Critical"):
                ev["detail"]["damage"]["wound"] = "Serious"
        carried = next(w for w in trial["final_state"][actor]["wounds"]
                       if w["id"] == wd["wound"])
        carried["severity"] = "Serious"
        carried["requirement"] = 10
        trial["ledger_sha256"] = canonical_digest(trial["ledger"])
        with self.assertRaises(AssertionError):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[1])

    def test_67_p2_global_wound_id_reconstruction_rejects_coordinated_alias(self):
        trial = self._case(POLICIES[1])
        wound = next(v for v in trial["ledger"] if v["kind"] == "g4_wound_created")
        actor, old = wound["detail"]["recipient"], wound["detail"]["wound"]
        assert old.startswith("G4-W")
        forged = "G4-W9999"
        wound["detail"]["wound"] = forged
        for existing in trial["final_state"][actor]["wounds"]:
            if existing["id"] == old:
                existing["id"] = forged
        trial["ledger_sha256"] = canonical_digest(trial["ledger"])
        with self.assertRaises(AssertionError):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[1])

    def test_68_p2_opposed_withdrawal_reconstructs_entire_g7g_receipt(self):
        original = self._case(POLICIES[2])
        receipts = [v for v in original["ledger"]
                    if v["kind"] == "g7g_living_hunter_disengagement_verified"]
        self.assertEqual(len(receipts), 1)
        original_details = receipts[0]["detail"]
        self.assertEqual(original_details["hunter_alive"], True)
        self.assertEqual(original_details["boundary"],
                         "authored_G7C_scene_exits_only")
        changes = (
            ("hunter_alive", False),
            ("boundary", "unverified_world_safe_escape"),
            ("ongoing_world_pursuit_not_adjudicated", False),
            ("native_terminal_index", 0),
            ("pursuit_index", 0),
            ("hunter_paid_bite_indices", []),
            ("border_exit_indices", []),
            ("unexpected_receipt_field", "forged"),
        )
        for field, changed in changes:
            with self.subTest(field=field):
                trial = deepcopy(original)
                witness = next(v for v in trial["ledger"]
                               if v["kind"] ==
                               "g7g_living_hunter_disengagement_verified")
                witness["detail"][field] = changed
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[2])
        trial = deepcopy(original)
        witness = next(v for v in trial["ledger"]
                       if v["kind"] == "g7g_living_hunter_disengagement_verified")
        del witness["detail"]["boundary"]
        trial["ledger_sha256"] = canonical_digest(trial["ledger"])
        with self.assertRaises(AssertionError):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[2])

    def test_69_p2_authentic_L2_L3_wounds_and_withdrawal_receipts(self):
        for level in (2, 3):
            with self.subTest(level=level):
                pack = run_pack(level, 17, include_trials=True)
                for policy in (POLICIES[1], POLICIES[2]):
                    attested = attest_trial(
                        deepcopy(pack["native_trials"][policy]),
                        level=level, seed=17, policy=policy)
                    self.assertEqual(
                        attested["outcome"], TERMINALS[policy][0])


    def test_70_p1_every_bite_requires_true_final_response_recheck(self):
        for policy in POLICIES:
            # Include the original first-round Hunter miss in the victory
            # branch and the final lethal/pursued Bite in the other branches.
            native = run_pack(3, 0, include_trials=True)["native_trials"][policy]
            hunter_rolls = [v for v in native["ledger"]
                            if v["kind"] == "g5_melee_roll"
                            and v["detail"].get("attacker") == "hunter"]
            self.assertTrue(hunter_rolls)
            for roll in (hunter_rolls[0], hunter_rolls[-1]):
                paid = roll["detail"]["action_index"]
                trigger = f"g5:melee:{paid}"
                for stage in ("trigger_rechecked_after_interceptions",
                              "trigger_rechecked_after_responses"):
                    with self.subTest(policy=policy, paid=paid, stage=stage):
                        trial = deepcopy(native)
                        recheck = next(x for x in trial["ledger"]
                                       if x["kind"] == stage
                                       and x["detail"].get("trigger") == trigger)
                        self.assertIs(recheck["detail"]["legal"], True)
                        recheck["detail"]["legal"] = False
                        trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                        with self.assertRaisesRegex(
                                AssertionError, "response-window ready chain"):
                            attest_trial(trial, level=3, seed=0, policy=policy)

    def test_71_p1_cancelled_ready_marker_cannot_underwrite_bite(self):
        for policy in POLICIES:
            native = self._case(policy)
            roll = next(v for v in reversed(native["ledger"])
                        if v["kind"] == "g5_melee_roll"
                        and v["detail"].get("attacker") == "hunter")
            trigger = f"g5:melee:{roll['detail']['action_index']}"
            ready = next(v for v in native["ledger"]
                         if v["kind"] == "trigger_ready_to_resolve"
                         and v["detail"].get("trigger") == trigger)
            ready["kind"] = "trigger_cancelled_after_spontaneous"
            native["ledger_sha256"] = canonical_digest(native["ledger"])
            with self.subTest(policy=policy), self.assertRaisesRegex(
                    AssertionError, "response-window ready chain"):
                attest_trial(native, level=3, seed=17, policy=policy)

    def test_72_p2_turn_end_unused_AP_must_match_source_paid_actions(self):
        for policy in POLICIES:
            native = run_pack(3, 0, include_trials=True)["native_trials"][policy]
            hunter_end = next(v for v in native["ledger"]
                              if v["kind"] == "turn_end"
                              and v["detail"].get("actor") == "hunter")
            self.assertEqual(hunter_end["detail"]["unused_ap"], 18)
            for bad in (999, 19, -1, None, True):
                with self.subTest(policy=policy, unused_ap=bad):
                    trial = deepcopy(native)
                    receipt = next(v for v in trial["ledger"]
                                   if v["kind"] == "turn_end"
                                   and v["detail"].get("actor") == "hunter")
                    receipt["detail"]["unused_ap"] = bad
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaisesRegex(
                            AssertionError, "Turn End unused AP"):
                        attest_trial(trial, level=3, seed=0, policy=policy)

    def test_73_p2_no_forged_AP_payment_remainder_or_allowance(self):
        for policy in POLICIES:
            native = self._case(policy)
            for kind, field, replacement in (
                    ("turn_resources", "ap", 999),
                    ("action_committed", "ap_spent", 1),
                    ("action_committed", "ap_remaining", 777)):
                with self.subTest(policy=policy, kind=kind, field=field):
                    trial = deepcopy(native)
                    event = next(x for x in trial["ledger"]
                                 if x["kind"] == kind
                                 and x["detail"].get("actor") == "hunter")
                    event["detail"][field] = replacement
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=policy)

    def test_74_p2_profile_injection_must_match_real_bite_receipt(self):
        for policy in POLICIES:
            native = run_pack(3, 0, include_trials=True)["native_trials"][policy]
            profiles = [v for v in native["ledger"]
                        if v["kind"] == "g4_profile_hit"
                        and v["detail"].get("attacker") == "hunter"
                        and v["detail"].get("profile") == "B06-AT-04"]
            self.assertTrue(profiles)
            for original in (profiles[0], profiles[-1]):
                with self.subTest(policy=policy, index=original["index"]):
                    trial = deepcopy(native)
                    profile = trial["ledger"][original["index"]]
                    self.assertIs(profile["detail"]["injection_eligible"], True)
                    profile["detail"]["injection_eligible"] = False
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaisesRegex(
                            AssertionError, "G4 profile injection eligibility"):
                        attest_trial(trial, level=3, seed=0, policy=policy)

    def test_75_p2_nonfatal_bite_venom_outcome_needs_source_receipt(self):
        for policy in POLICIES:
            native = self._case(policy)
            result = next(v for v in native["ledger"]
                          if v["kind"] == "g5_melee_resolved"
                          and v["detail"].get("attacker") == "hunter"
                          and v["detail"].get("outcome") == "hit"
                          and (v["detail"].get("damage") or {}).get("venom"))
            paid = result["detail"]["action_index"]
            exposure = f"g6:bite:17:{paid}"
            recorded = [v for v in native["ledger"]
                        if v["kind"] in (
                            "g44_hunter_accepted", "g44_hunter_ignored",
                            "g44_hunter_prevented", "g44_hunter_not_delivered")
                        and (v["detail"].get("key") == exposure
                             or v["detail"].get("exposure_key") == exposure)]
            self.assertEqual(len(recorded), 1)
            receipt = recorded[0]
            receipt["kind"] = "g44_hunter_prevented" if (
                receipt["kind"] != "g44_hunter_prevented"
            ) else "g44_hunter_accepted"
            native["ledger_sha256"] = canonical_digest(native["ledger"])
            with self.subTest(policy=policy), self.assertRaisesRegex(
                    AssertionError, "venom outcome|exposure receipt"):
                attest_trial(native, level=3, seed=17, policy=policy)

    def test_76_positive_L2_L3_seed0_and_17_all_terminal_paths(self):
        for level in (2, 3):
            for seed in (0, 17):
                with self.subTest(level=level, seed=seed):
                    bundle = run_pack(level, seed, include_trials=True)
                    for policy in POLICIES:
                        native = bundle["native_trials"][policy]
                        attested = attest_trial(
                            native, level=level, seed=seed, policy=policy)
                        self.assertEqual(attested["outcome"],
                                         TERMINALS[policy][0])



    def test_77_p1_lethal_bow_must_have_two_true_legal_response_rechecks(self):
        # Codex P1: cancelling the final G0 Bow trigger used to leave an
        # otherwise well-formed lethal G4 packet accepted after rehash.
        for level in (2, 3):
            original = run_pack(level, 0, include_trials=True)["native_trials"][POLICIES[0]]
            bow = next(v for v in original["ledger"]
                       if v["kind"] == "g6d_bow_adjudicated")
            trigger = bow["detail"]["shot_trigger"]
            for stage in ("trigger_rechecked_after_interceptions",
                          "trigger_rechecked_after_responses"):
                with self.subTest(level=level, stage=stage):
                    trial = deepcopy(original)
                    item = next(v for v in trial["ledger"]
                                if v["kind"] == stage
                                and v["detail"].get("trigger") == trigger)
                    self.assertIs(item["detail"]["legal"], True)
                    item["detail"]["legal"] = False
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaisesRegex(
                            AssertionError, "legal G0 response-window ready chain"):
                        attest_trial(trial, level=level, seed=0, policy=POLICIES[0])

    def test_78_p1_lethal_bow_cannot_use_cancelled_or_foreign_window(self):
        original = run_pack(3, 0, include_trials=True)["native_trials"][POLICIES[0]]
        bow = next(v for v in original["ledger"]
                   if v["kind"] == "g6d_bow_adjudicated")
        trigger = bow["detail"]["shot_trigger"]
        for variant in ("cancel_ready", "duplicate_ready", "wrong_trigger",
                        "unmodelled_spontaneous"):
            with self.subTest(variant=variant):
                trial = deepcopy(original)
                ledger = trial["ledger"]
                if variant == "cancel_ready":
                    ready = next(v for v in ledger
                                 if v["kind"] == "trigger_ready_to_resolve"
                                 and v["detail"].get("trigger") == trigger)
                    ready["kind"] = "trigger_cancelled_after_spontaneous"
                elif variant == "duplicate_ready":
                    # A foreign second 'ready' cannot sign another shot.
                    ready = next(v for v in ledger
                                 if v["kind"] == "trigger_ready_to_resolve"
                                 and v["detail"].get("trigger") == trigger)
                    other = next(v for v in ledger
                                 if v["kind"] == "g2_projectile_defense_rechecked")
                    other["kind"] = "trigger_ready_to_resolve"
                    other["detail"] = deepcopy(ready["detail"])
                elif variant == "wrong_trigger":
                    bow_record = next(v for v in ledger
                                      if v["kind"] == "g6d_bow_adjudicated")
                    bow_record["detail"]["shot_trigger"] = "g6d:bow:fake"
                else:
                    other = next(v for v in ledger
                                 if v["kind"] == "g2_projectile_defense_rechecked")
                    other["kind"] = "spontaneous_committed"
                    other["detail"] = {"trigger": trigger, "actor": "hunter"}
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=0, policy=POLICIES[0])

    def test_79_p1_every_replayed_g1_step_requires_legal_response_window(self):
        # Codex P1: tamper all four final border steps, not only their
        # coordinates/MP; failed trigger must invalidate their G5 exits.
        for level in (2, 3):
            original = run_pack(level, 0, include_trials=True)["native_trials"][POLICIES[2]]
            moves = []
            for exit_event in (v for v in original["ledger"]
                               if v["kind"] == "g5_terminal_exit"):
                moves.append(original["ledger"][
                    exit_event["detail"]["movement_index"]])
            self.assertEqual(len(moves), 4)
            for stage in ("trigger_rechecked_after_interceptions",
                          "trigger_rechecked_after_responses"):
                with self.subTest(level=level, stage=stage):
                    trial = deepcopy(original)
                    for move in moves:
                        ready = trial["ledger"][move["index"] - 1]
                        self.assertEqual(ready["kind"], "trigger_ready_to_resolve")
                        matching = next(v for v in trial["ledger"]
                                        if v["kind"] == stage
                                        and v["detail"].get("trigger") ==
                                            ready["detail"]["trigger"])
                        self.assertIs(matching["detail"]["legal"], True)
                        matching["detail"]["legal"] = False
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaisesRegex(
                            AssertionError, "legal G0 response-window ready chain"):
                        attest_trial(trial, level=level, seed=0, policy=POLICIES[2])

    def test_80_p1_cancelled_or_reused_g1_window_cannot_fund_border_exit(self):
        original = run_pack(3, 0, include_trials=True)["native_trials"][POLICIES[2]]
        exit_event = next(v for v in original["ledger"]
                          if v["kind"] == "g5_terminal_exit")
        index = exit_event["detail"]["movement_index"]
        for variant in ("cancel_ready", "foreign_ready", "missing_open",
                        "duplicate_ready"):
            with self.subTest(variant=variant):
                trial = deepcopy(original)
                ledger = trial["ledger"]
                ready = ledger[index - 1]
                trigger = ready["detail"]["trigger"]
                window = next(v for v in ledger
                              if v["kind"] == "response_window_open"
                              and v["detail"].get("trigger") == trigger)
                if variant == "cancel_ready":
                    ready["kind"] = "trigger_cancelled_after_spontaneous"
                elif variant == "foreign_ready":
                    ready["detail"]["trigger"] = "g1:archer:step:0"
                elif variant == "missing_open":
                    window["kind"] = "missing_response_window"
                else:
                    other = next(v for v in ledger
                                 if v["kind"] == "trigger_rechecked_after_interceptions"
                                 and v["detail"].get("trigger") == trigger)
                    other["kind"] = "trigger_ready_to_resolve"
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=0, policy=POLICIES[2])

    def test_81_p1_valid_bow_and_movement_windows_continue_to_certify(self):
        for level in (2, 3):
            for seed in (0, 17):
                with self.subTest(level=level, seed=seed):
                    bundle = run_pack(level, seed, include_trials=True)
                    self.assertTrue(bundle["bounded_terminal_matrix_certified"])
                    for policy in POLICIES:
                        result = attest_trial(bundle["native_trials"][policy],
                                             level=level, seed=seed, policy=policy)
                        self.assertEqual(result["outcome"], TERMINALS[policy][0])


    def test_82_p2_no_move_turn_cannot_lower_source_MP_and_turn_end(self):
        # Codex P2: two mutually consistent signed balances still contradict
        # the independent G6-C/G0 base 12-MP grant for every original actor.
        for level in (2, 3):
            native = run_pack(level, 17, include_trials=True)["native_trials"]
            for policy in POLICIES:
                src = native[policy]
                no_move = next(
                    (event for event in src["ledger"]
                     if event["kind"] == "turn_resources"
                     and event["detail"]["mp"] == 12
                     and not any(v["kind"] == "g1_movement_step"
                                 and v["round"] == event["round"]
                                 and v["detail"].get("actor") == event["detail"]["actor"]
                                 for v in src["ledger"])),
                    None)
                self.assertIsNotNone(no_move)
                for lowered in (0, 11):
                    with self.subTest(level=level, policy=policy, mp=lowered):
                        trial = deepcopy(src)
                        start = trial["ledger"][no_move["index"]]
                        start["detail"]["mp"] = lowered
                        ends = [e for e in trial["ledger"]
                                if e["kind"] == "turn_end"
                                and e["round"] == start["round"]
                                and e["detail"].get("actor") == start["detail"]["actor"]]
                        self.assertEqual(len(ends), 1)
                        ends[0]["detail"]["unused_mp"] = lowered
                        trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                        with self.assertRaisesRegex(
                                AssertionError, "source allowance"):
                            attest_trial(trial, level=level, seed=17,
                                         policy=policy)

    def test_83_p2_every_native_MP_grant_is_exactly_source_authorized(self):
        for level in (2, 3):
            pack = run_pack(level, 0, include_trials=True)["native_trials"]
            for policy in POLICIES:
                receipt = pack[policy]
                grants = [v for v in receipt["ledger"]
                          if v["kind"] == "turn_resources"]
                self.assertEqual(len(grants),
                                 receipt["rounds_completed"] * 5)
                self.assertEqual({v["detail"]["mp"] for v in grants}, {12})
                attest_trial(receipt, level=level, seed=0, policy=policy)

    def test_84_p2_forged_full_to_reduced_venom_with_rehashed_G45_G5(self):
        # This reproduces the specific coordinated P2 injection: changing
        # the original Full/3 resistance to a fictitious Reduced/999 and
        # clearing marker identities in the accepted G4.4 event and BOTH
        # mirrored G4.5/G5 receipts is still forbidden.
        policy = POLICIES[0]
        trial = self._case(policy)
        ledger = trial["ledger"]
        result = next(v for v in ledger if
                      v["kind"] == "g5_melee_resolved"
                      and v["detail"].get("attacker") == "hunter"
                      and ((v["detail"].get("damage") or {}).get("venom") or {}).get(
                          "outcome") == "accepted")
        action = result["detail"]["action_index"]
        bridge = next(v for v in ledger
                      if v["kind"] == "g45_attested_hit"
                      and v["detail"].get("action_index") == action)
        accepted = next(v for v in ledger if v["kind"] == "g44_hunter_accepted"
                        and v["detail"].get("key") == f"g6:bite:17:{action}")
        self.assertEqual(accepted["detail"]["resolution"], "Full")
        self.assertEqual(accepted["detail"]["resistance_total"], 3)
        self.assertEqual(len(accepted["detail"]["marker_ids"]), 3)
        accepted["detail"].update(
            resolution="Reduced", resistance_total=999, marker_ids=[])
        altered = {"outcome": "accepted", "resolution": "Reduced",
                   "resistance_total": 999}
        bridge["detail"]["actual_result"]["venom"] = deepcopy(altered)
        result["detail"]["damage"]["venom"] = deepcopy(altered)
        trial["ledger_sha256"] = canonical_digest(ledger)
        with self.assertRaisesRegex(
                AssertionError, "authored resistance roll/Vitality"):
            attest_trial(trial, level=3, seed=17, policy=policy)

    def test_85_p2_resistance_total_cannot_change_even_with_same_result(self):
        for policy in (POLICIES[0], POLICIES[2]):
            with self.subTest(policy=policy):
                trial = self._case(policy)
                ledger = trial["ledger"]
                accepted = next(v for v in ledger
                                if v["kind"] == "g44_hunter_accepted")
                key = accepted["detail"]["key"]
                actor_resolved = next(v for v in ledger
                        if v["kind"] == "g5_melee_resolved"
                        and ((v["detail"].get("damage") or {}).get("venom") or {}).get(
                            "resistance_total") ==
                               accepted["detail"]["resistance_total"]
                        and f"g6:bite:17:{v['detail'].get('action_index')}" == key)
                action = actor_resolved["detail"]["action_index"]
                bridge = next(v for v in ledger
                              if v["kind"] == "g45_attested_hit"
                              and v["detail"].get("action_index") == action)
                altered = accepted["detail"]["resistance_total"] + 1
                accepted["detail"]["resistance_total"] = altered
                bridge["detail"]["actual_result"]["venom"]["resistance_total"] = altered
                actor_resolved["detail"]["damage"]["venom"]["resistance_total"] = altered
                trial["ledger_sha256"] = canonical_digest(ledger)
                with self.assertRaisesRegex(
                        AssertionError, "authored resistance roll/Vitality"):
                    attest_trial(trial, level=3, seed=17, policy=policy)

    def test_86_p2_real_venom_requires_exact_source_timed_milestones(self):
        for policy in (POLICIES[0], POLICIES[2]):
            for mutation in ("due", "phase", "marker", "recipient"):
                with self.subTest(policy=policy, mutation=mutation):
                    trial = self._case(policy)
                    ledger = trial["ledger"]
                    accepted = next(v for v in ledger
                                    if v["kind"] == "g44_hunter_accepted")
                    key = accepted["detail"]["key"]
                    marker = next(v for v in ledger
                                  if v["kind"] == "g42_milestone_scheduled"
                                  and v["detail"]["source"] == f"hunter:{key}")
                    # G6-C's fixed witness never calls enter_initiative:
                    # its WorldClock schedules the 600s/1800s/7200s or
                    # 600s/3600s markers in exploration seconds (not a
                    # fabricated Round-Begin conversion).
                    self.assertIsNone(marker["detail"]["due_round"])
                    self.assertIsInstance(marker["detail"]["due_seconds"], int)
                    if mutation == "due":
                        marker["detail"]["due_seconds"] += 6
                    elif mutation == "phase":
                        marker["detail"]["phase"] = "after_recovery"
                    elif mutation == "recipient":
                        marker["detail"]["actor"] = "scholar"
                    else:
                        accepted["detail"]["marker_ids"].pop()
                    trial["ledger_sha256"] = canonical_digest(ledger)
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=policy)

    def test_87_p2_original_L2_L3_source_venom_and_MP_still_certify(self):
        for level in (2, 3):
            for seed in (0, 17):
                pack = run_pack(level, seed, include_trials=True)
                self.assertTrue(pack["bounded_terminal_matrix_certified"])
                for policy in POLICIES:
                    with self.subTest(level=level, seed=seed, policy=policy):
                        trial = pack["native_trials"][policy]
                        self.assertEqual(
                            attest_trial(trial, level=level, seed=seed,
                                         policy=policy)["outcome"],
                            TERMINALS[policy][0])



    def test_88_p1_AB_every_hit_requires_both_legal_G0_response_rechecks(self):
        # G5 cannot roll an A/B hit after a cancelled G0 original trigger.
        # Recomputing the SHA cannot authorize the unchanged G4 and G4.5.
        for level in (2, 3):
            for seed in (0, 17):
                native = run_pack(level, seed, include_trials=True)[
                    "native_trials"][POLICIES[0]]
                hits = [v for v in native["ledger"]
                        if v["kind"] == "g5_melee_roll"
                        and v["detail"].get("attacker") in ("vanguard", "guardian")
                        and v["detail"].get("hit") is True]
                self.assertTrue(any(v["detail"]["attacker"] == "vanguard"
                                    for v in hits))
                self.assertTrue(any(v["detail"]["attacker"] == "guardian"
                                    for v in hits))
                for roll in hits:
                    trigger = f"g5:melee:{roll['detail']['action_index']}"
                    for stage in ("trigger_rechecked_after_interceptions",
                                  "trigger_rechecked_after_responses"):
                        with self.subTest(level=level, seed=seed,
                                          attacker=roll["detail"]["attacker"],
                                          action=roll["detail"]["action_index"],
                                          stage=stage):
                            trial = deepcopy(native)
                            recheck = next(
                                v for v in trial["ledger"]
                                if v["kind"] == stage
                                and v["detail"].get("trigger") == trigger)
                            self.assertIs(recheck["detail"]["legal"], True)
                            recheck["detail"]["legal"] = False
                            trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                            with self.assertRaisesRegex(
                                    AssertionError,
                                    "legal G0 response-window ready chain"):
                                attest_trial(trial, level=level, seed=seed,
                                             policy=POLICIES[0])

    def test_89_p1_AB_hit_cannot_borrow_cancelled_or_foreign_G0_window(self):
        source = run_pack(3, 0, include_trials=True)[
            "native_trials"][POLICIES[0]]
        rolls = [v for v in source["ledger"]
                 if v["kind"] == "g5_melee_roll"
                 and v["detail"].get("attacker") in ("vanguard", "guardian")
                 and v["detail"].get("hit") is True]
        self.assertGreaterEqual(len(rolls), 2)
        for roll in rolls:
            trigger = f"g5:melee:{roll['detail']['action_index']}"
            for mutation in ("cancel_ready", "missing_open", "wrong_actor_turn",
                             "borrow_other_paid_action", "foreign_response"):
                with self.subTest(actor=roll["detail"]["attacker"],
                                  action=roll["detail"]["action_index"],
                                  mutation=mutation):
                    trial = deepcopy(source)
                    ledger = trial["ledger"]
                    windows = [v for v in ledger
                               if v["detail"].get("trigger") == trigger]
                    self.assertEqual(
                        [v["kind"] for v in windows],
                        ["response_window_open",
                         "trigger_rechecked_after_interceptions",
                         "trigger_rechecked_after_responses",
                         "trigger_ready_to_resolve"])
                    if mutation == "cancel_ready":
                        windows[-1]["kind"] = "trigger_cancelled_after_spontaneous"
                    elif mutation == "missing_open":
                        windows[0]["kind"] = "window_open_fabricated"
                    elif mutation == "wrong_actor_turn":
                        windows[1]["turn"] = "hunter"
                    elif mutation == "borrow_other_paid_action":
                        windows[2]["detail"]["trigger"] = "g5:melee:other"
                    else:
                        windows[1]["kind"] = "spontaneous_committed"
                        windows[1]["detail"] = {
                            "trigger": trigger, "actor": "hunter",
                            "response_kind": "reaction"}
                    trial["ledger_sha256"] = canonical_digest(ledger)
                    # Native chronology may reject a foreign actor turn
                    # even before the dedicated response-chain validator.
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=0,
                                     policy=POLICIES[0])

    def test_90_p1_chosen_rite_requires_entire_native_G3_effect_receipt(self):
        # _new_effect on the original G6-D/G7-H source scene must establish
        # first-effect G3-0001, maintained without expiry/parent/budget,
        # exactly 1 committed VP and no invented extra fields.
        for level in (2, 3):
            native = run_pack(level, 0, include_trials=True)[
                "native_trials"][POLICIES[0]]
            established = [v for v in native["ledger"]
                           if v["kind"] == "g3_effect_established"]
            self.assertEqual(len(established), 1)
            for key, bad in (
                    ("effect", "G3-fabricated"),
                    ("expiry_round", 1),
                    ("anchor", "Arrow"),
                    ("parent", "G3-0099"),
                    ("budget", 999),
                    ("resistance", 4),
                    ("chosen", False),
                    ("committed", 2),
                    ("effect_kind", "Vital Shelter"),
                    ("caster", "guardian"),
                    ("recipient", "vanguard")):
                with self.subTest(level=level, field=key):
                    trial = deepcopy(native)
                    rite = next(v for v in trial["ledger"]
                                if v["kind"] == "g3_effect_established")
                    rite["detail"][key] = bad
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaisesRegex(
                            AssertionError, "exact native G3 establishment receipt"):
                        attest_trial(trial, level=level, seed=0,
                                     policy=POLICIES[0])
            for mutation in ("extra_field", "deleted_field", "wrong_round"):
                with self.subTest(level=level, mutation=mutation):
                    trial = deepcopy(native)
                    rite = next(v for v in trial["ledger"]
                                if v["kind"] == "g3_effect_established")
                    if mutation == "extra_field":
                        rite["detail"]["invented_ward"] = True
                    elif mutation == "deleted_field":
                        del rite["detail"]["parent"]
                    else:
                        rite["round"] = 2
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    expected = ("G0 non-boundary event"
                                if mutation == "wrong_round"
                                else "exact native G3 establishment receipt")
                    with self.assertRaisesRegex(AssertionError, expected):
                        attest_trial(trial, level=level, seed=0,
                                     policy=POLICIES[0])



    def test_91_p1_bow_lethal_range_rebuilt_from_authored_g2_lane(self):
        for level in (2, 3):
            native = run_pack(level, 0, include_trials=True)[
                "native_trials"][POLICIES[0]]
            launches = [v for v in native["ledger"]
                        if v["kind"] == "g2_bow_launched"]
            self.assertEqual(len(launches), 2)
            for round_no in (2, 3):
                with self.subTest(level=level, round=round_no):
                    trial = deepcopy(native)
                    launch = next(v for v in trial["ledger"]
                                  if v["kind"] == "g2_bow_launched"
                                  and v["round"] == round_no)
                    self.assertEqual(launch["detail"]["range_difficulty"], -2)
                    launch["detail"]["range_difficulty"] = 999
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaisesRegex(
                            AssertionError, "G2 launch range, cover, obstruction"):
                        attest_trial(trial, level=level, seed=0,
                                     policy=POLICIES[0])

    def test_92_p1_bow_cover_obstruction_and_defense_recheck_from_lane(self):
        native = self._case(POLICIES[0])
        for target, field, replacement in (
                ("g2_bow_launched", "cover", 2),
                ("g2_bow_launched", "screens", {"guardian": 4}),
                ("g2_bow_launched", "effective_obstruction", 6),
                ("g2_bow_launched", "aim_mitigation", 4),
                ("g2_projectile_defense_rechecked", "base", 90),
                ("g2_projectile_defense_rechecked", "final", 90),
                ("g2_projectile_defense_rechecked", "actual", "dodge"),
                ("g2_bow_shot_resolved", "base_defense", 90),
                ("g2_bow_shot_resolved", "final_defense", 90),
                ("g2_miss_faces_preallocated", "final_defense", 90)):
            with self.subTest(kind=target, field=field):
                trial = deepcopy(native)
                event = next(v for v in trial["ledger"]
                             if v["kind"] == target and v["round"] == 3)
                event["detail"][field] = replacement
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaises(AssertionError):
                    attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_93_p1_g45_post_hit_full_state_source_replayed_all_terminals(self):
        for policy in POLICIES:
            native = self._case(policy)
            source_bridges = [v for v in native["ledger"]
                              if v["kind"] == "g45_attested_hit"
                              and v["detail"]["attacker"] == "hunter"]
            self.assertTrue(source_bridges)
            for field, bogus in (
                    ("dead", True), ("dying", True),
                    ("hp", 999), ("hp_max", 999),
                    ("vigor", 999), ("vigor_max", 999),
                    ("vp_available", 999), ("vp_committed", 999),
                    ("vp_spent", 999), ("id", "different-actor"),
                    ("source_id", "F"), ("source_digest", "forged"),
                    ("wounds", [{"id": "synthetic"}])):
                with self.subTest(policy=policy, field=field):
                    trial = deepcopy(native)
                    event = next(v for v in trial["ledger"]
                                 if v["kind"] == "g45_attested_hit"
                                 and v["detail"]["attacker"] == "hunter")
                    original = event["detail"]["target_state"][field]
                    event["detail"]["target_state"][field] = (
                        not original if field in ("dead", "dying") else bogus)
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=policy)

    def test_94_p2_g45_bridge_source_digests_and_binding_authenticated(self):
        for policy in POLICIES:
            native = self._case(policy)
            for key, bogus in (
                    ("attacker_source", "rehashed-forgery"),
                    ("target_source", "rehashed-forgery"),
                    ("contact_reference", "g5:melee:other"),
                    ("defense_reference", "g0:defense:other"),
                    ("source_event", "g5:source:synthetic"),
                    ("sequence_declaration_index", -1),
                    ("declared_profile_index", 999)):
                with self.subTest(policy=policy, key=key):
                    trial = deepcopy(native)
                    event = next(v for v in trial["ledger"]
                                 if v["kind"] == "g45_attested_hit"
                                 and v["detail"]["attacker"] == "hunter")
                    event["detail"][key] = bogus
                    trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                    with self.assertRaises(AssertionError):
                        attest_trial(trial, level=3, seed=17, policy=policy)

    def test_95_p2_g45_non_hunter_bridge_state_also_source_bound(self):
        trial = self._case(POLICIES[0])
        bridge = next(v for v in trial["ledger"]
                      if v["kind"] == "g45_attested_hit"
                      and v["detail"]["attacker"] == "vanguard")
        bridge["detail"]["target_state"]["dead"] = True
        trial["ledger_sha256"] = canonical_digest(trial["ledger"])
        with self.assertRaises(AssertionError):
            attest_trial(trial, level=3, seed=17, policy=POLICIES[0])

    def test_96_p1_positive_all_native_g2_g45_chains_level2_level3(self):
        for level in (2, 3):
            with self.subTest(level=level):
                run = run_pack(level, 0)
                self.assertTrue(run["bounded_terminal_matrix_certified"])
                self.assertEqual(run["distinct_native_terminal_outcomes"], 3)
                self.assertFalse(run["complete_party_pack_certified"])



    def test_97_p1_every_AB_defense_is_exact_source_policy_and_pressure(self):
        # Coordinated changes to declaration, assignment, roll and the
        # subsequent pressure receipt still cannot substitute another
        # legal Hunter defense for the G6-C authored choice.
        for round_no in (1, 2):
            for actor in ("vanguard", "guardian"):
                with self.subTest(round_no=round_no, actor=actor):
                    trial=self._case(POLICIES[0])
                    events=trial["ledger"]
                    declaration=next(v for v in events
                                     if v["kind"]=="attack_sequence_committed"
                                     and v["round"]==round_no
                                     and v["detail"].get("attacker")==actor
                                     and v["detail"].get("target")=="hunter")
                    chosen="take_hit" if actor=="vanguard" else "dodge"
                    declaration["detail"]["defenses"]=[chosen]
                    key=f"{actor}:hunter:0"
                    assigned=next(v for v in events
                                  if v["kind"]=="defense_assigned"
                                  and v["round"]==round_no
                                  and v["detail"].get("attack_key")==key)
                    defense_value=(None if chosen=="take_hit" else 12)
                    assigned["detail"]["defense"]=chosen
                    assigned["detail"]["defense_value"]=defense_value
                    assigned["detail"]["dodge_pressure"]=(
                        0 if chosen=="take_hit" else 4)
                    seq=next(v for v in events
                             if v["kind"]=="g5_melee_sequence_attested"
                             and v["detail"].get("attacker")==actor
                             and v["round"]==round_no)
                    action=seq["detail"]["action_indices"][0]
                    roll=next(v for v in events
                              if v["kind"]=="g5_melee_roll"
                              and v["detail"].get("action_index")==action)
                    roll["detail"]["defense"]=chosen
                    roll["detail"]["declared_defense"]=chosen
                    roll["detail"]["defense_value"]=defense_value
                    if actor=="vanguard":
                        # Also amend the *next* G0 pressure receipt, so all
                        # changed local resource metadata appears coherent.
                        guardian=next(v for v in events
                                      if v["kind"]=="defense_assigned"
                                      and v["round"]==round_no
                                      and v["detail"].get("attack_key")==
                                      "guardian:hunter:0")
                        guardian["detail"]["dodge_pressure"]=0
                    trial["ledger_sha256"]=canonical_digest(events)
                    with self.assertRaises(AssertionError):
                        attest_trial(trial,level=3,seed=17,policy=POLICIES[0])

    def test_98_p1_guardian_round1_miss_requires_true_legal_window(self):
        # Round-1 B face=1 misses and has no G4.5 hit; it STILL needs
        # both legal source rechecks and one authentic G5 roll/resolution.
        for level in (2, 3):
            source=run_pack(level, 17, include_trials=True)[
                "native_trials"][POLICIES[0]]
            events=source["ledger"]
            miss=next(v for v in events if
                      v["kind"]=="g5_melee_resolved"
                      and v["round"]==1
                      and v["detail"].get("attacker")=="guardian")
            self.assertEqual(miss["detail"]["outcome"],"miss")
            action=miss["detail"]["action_index"]
            trigger=f"g5:melee:{action}"
            for stage in ("trigger_rechecked_after_interceptions",
                          "trigger_rechecked_after_responses"):
                with self.subTest(level=level,stage=stage):
                    trial=deepcopy(source)
                    recheck=next(v for v in trial["ledger"]
                                 if v["kind"]==stage
                                 and v["detail"].get("trigger")==trigger)
                    self.assertIs(recheck["detail"]["legal"],True)
                    recheck["detail"]["legal"]=False
                    trial["ledger_sha256"]=canonical_digest(trial["ledger"])
                    with self.assertRaises(AssertionError):
                        attest_trial(trial,level=level,seed=17,policy=POLICIES[0])

    def test_99_p1_guardian_round1_miss_cannot_be_cancelled_or_omitted(self):
        source=self._case(POLICIES[0])
        for corruption in ("fake_cancel", "omit_original_roll",
                           "replace_original_roll", "change_miss_to_hit"):
            with self.subTest(corruption=corruption):
                trial=deepcopy(source)
                events=trial["ledger"]
                resolved=next(v for v in events if
                              v["kind"]=="g5_melee_resolved"
                              and v["round"]==1
                              and v["detail"].get("attacker")=="guardian")
                action=resolved["detail"]["action_index"]
                original_roll=next(v for v in events
                                   if v["kind"]=="g5_melee_roll"
                                   and v["detail"].get("action_index")==action)
                if corruption=="fake_cancel":
                    resolved["kind"]="g5_melee_cancelled"
                    resolved["detail"]={
                        "action_index":action, "trigger":f"g5:melee:{action}"}
                elif corruption=="omit_original_roll":
                    original_roll["kind"]="declined_melee_roll"
                elif corruption=="replace_original_roll":
                    original_roll["detail"]["attack_face"]=2
                    original_roll["detail"]["attack_total"]+=1
                else:
                    original_roll["detail"]["hit"]=True
                    resolved["detail"]["outcome"]="hit"
                trial["ledger_sha256"]=canonical_digest(events)
                with self.assertRaises(AssertionError):
                    attest_trial(trial,level=3,seed=17,policy=POLICIES[0])

    def test_100_p2_genesis_policy_is_original_source_for_all_outcomes(self):
        for policy in POLICIES:
            with self.subTest(policy=policy):
                source=self._case(policy)
                native=source["ledger"][0]["detail"]
                self.assertEqual(
                    native["policy"],
                    "fixed_source_declared_dice_and_declined_optional_responses")
                for changed in ("policy", "objective"):
                    with self.subTest(field=changed):
                        trial=deepcopy(source)
                        trial["ledger"][0]["detail"][changed]="unrelated_authored_policy"
                        trial["ledger_sha256"]=canonical_digest(trial["ledger"])
                        with self.assertRaises(AssertionError):
                            attest_trial(trial,level=3,seed=17,policy=policy)

    def test_101_valid_all_AB_slots_and_original_genesis_remain_accepted(self):
        for level in (2,3):
            for seed in (0,17):
                with self.subTest(level=level,seed=seed):
                    pack=run_pack(level,seed,include_trials=True)
                    trial=pack["native_trials"][POLICIES[0]]
                    original=trial["ledger"]
                    ab=[v for v in original if v["kind"]=="g5_melee_resolved"
                        and v["detail"].get("attacker") in ("vanguard","guardian")]
                    self.assertEqual(len(ab),4)
                    self.assertEqual([(v["detail"]["attacker"],
                                       v["round"],v["detail"]["outcome"])
                                      for v in ab],
                                     [("vanguard",1,"hit"),("guardian",1,"miss"),
                                      ("vanguard",2,"hit"),("guardian",2,"hit")])
                    proof=attest_trial(trial,level=level,seed=seed,
                                       policy=POLICIES[0])
                    self.assertEqual(proof["outcome"],"hunter_defeat_attested")


    def test_102_p2_fixed_g7g_player_cannot_commit_valid_but_unauthored_ap(self):
        # Replay legitimate actor/source AP exactly as the current accounting
        # validator would accept. The *policy*, not budget, must reject it.
        for policy in POLICIES[1:]:
            with self.subTest(policy=policy):
                trial = self._case(policy)
                events = trial["ledger"]
                # An otherwise non-Action source in the Scholar's first
                # turn, replaced with a self-consistent affordable 24 AP
                # general action. The same technique can target any member.
                unused = next(v for v in events
                              if v["kind"] == "regeneration_step"
                              and v["round"] == 1 and v["turn"] == "scholar")
                scholar_resources = next(v for v in events
                                         if v["kind"] == "turn_resources"
                                         and v["round"] == 1
                                         and v["turn"] == "scholar")
                self.assertGreaterEqual(scholar_resources["detail"]["ap"], 24)
                # Preserve an otherwise source-legal Step-4 receipt
                # ahead of the new Action. The renamed regeneration receipt
                # is deliberately NOT a legal source continuation; the AP
                # verifier must still accept the forged debit itself, while
                # the fixed policy gate must reject it independently.
                self.assertLess(unused["index"], scholar_resources["index"])
                allowance = scholar_resources["detail"]["ap"]
                unused["kind"] = "turn_resources"
                unused["detail"] = deepcopy(scholar_resources["detail"])
                scholar_resources["kind"] = "action_committed"
                scholar_resources["detail"] = {
                    "actor": "scholar", "action_class": "general",
                    "label": "g7h:unapproved:general",
                    "ap_spent": 24, "ap_remaining": allowance - 24,
                }
                end = next(v for v in events if v["kind"] == "turn_end"
                           and v["round"] == 1 and v["turn"] == "scholar")
                end["detail"]["unused_ap"] -= 24
                trial["ledger_sha256"] = canonical_digest(events)
                from scripts.b06_g7h_mixed_encounter_certification_v0 import (
                    _reconcile_all_turn_end_ap,
                )
                self.assertEqual(
                    _reconcile_all_turn_end_ap(events, level=3, seed=17),
                    trial["rounds_completed"] * 5)
                with self.assertRaisesRegex(
                        AssertionError, "Fixed G7-G action policy"):
                    attest_trial(trial, level=3, seed=17, policy=policy)

    def test_103_p2_defeat_bite_wound_must_match_synchronous_G4(self):
        trial = self._case("hunter_multitarget_defeat")
        events = trial["ledger"]
        damage = next(e for e in events if e["kind"] == "g4_damage_applied"
                      and e["detail"].get("cause") == "source-profile:B06-AT-04"
                      and e["detail"].get("wound") == "Critical"
                      and e["detail"].get("dead") is not True)
        bridge = next(e for e in events if
                      e["kind"] == "g45_attested_hit"
                      and e["detail"].get("target") == damage["detail"]["recipient"]
                      and e["index"] > damage["index"]
                      and e["detail"].get("actual_result", {}).get("wound") ==
                          "Critical")
        action = bridge["detail"]["action_index"]
        resolved = next(e for e in events
                        if e["kind"] == "g5_melee_resolved"
                        and e["detail"].get("action_index") == action)
        self.assertEqual(resolved["detail"]["damage"]["wound"],
                         bridge["detail"]["actual_result"]["wound"])
        bridge["detail"]["actual_result"]["wound"] = None
        resolved["detail"]["damage"]["wound"] = None
        trial["ledger_sha256"] = canonical_digest(events)
        with self.assertRaisesRegex(
                AssertionError, "Bite's G4 damage"):
            attest_trial(trial, level=3, seed=17,
                         policy="hunter_multitarget_defeat")

    def test_104_p2_defeat_source_pursuit_receipt_reconstructs_entire_route(self):
        source = self._case("hunter_multitarget_defeat")
        selected = next(v for v in source["ledger"] if
                        v["kind"] == "g7g_hunter_target_selected"
                        and v["detail"]["declared_cautious_route"])
        pursued = next(v for v in source["ledger"] if
                       v["kind"] == "g7g_hunter_pursuit_executed"
                       and v["round"] == selected["round"])
        for variant in ("selection_start", "selection_route",
                        "pursuit_start", "pursuit_indices",
                        "pursuit_mp", "pursuit_extra_index"):
            with self.subTest(variant=variant):
                trial = deepcopy(source)
                a = trial["ledger"][selected["index"]]["detail"]
                b = trial["ledger"][pursued["index"]]["detail"]
                if variant == "selection_start":
                    a["initial_footprint"] = [[7, 6], [7, 5]]
                elif variant == "selection_route":
                    a["declared_cautious_route"] = [["step", [0, 1], None, 2]]
                elif variant == "pursuit_start":
                    b["initial_footprint"] = [[7, 6], [7, 5]]
                elif variant == "pursuit_indices":
                    b["movement_indices"] = []
                elif variant == "pursuit_mp":
                    b["mp_remaining"] = 999
                else:
                    b["movement_indices"].append(pursued["index"])
                trial["ledger_sha256"] = canonical_digest(trial["ledger"])
                with self.assertRaisesRegex(AssertionError, "G7-H.*pursuit"):
                    attest_trial(trial, level=3, seed=17,
                                 policy="hunter_multitarget_defeat")

    def test_105_p2_positive_exact_G7G_action_and_pursuit_receipts(self):
        for level in (2, 3):
            report = run_pack(level, 17, include_trials=True)
            for policy in POLICIES[1:]:
                with self.subTest(level=level, policy=policy):
                    trial = report["native_trials"][policy]
                    actions = [v for v in trial["ledger"]
                               if v["kind"] == "action_committed"]
                    self.assertTrue(actions)
                    self.assertEqual({v["detail"]["actor"] for v in actions},
                                     {"hunter"})
                    self.assertEqual({v["detail"]["label"] for v in actions},
                                     {"sequence:B06-AT-04:0"})
                    accepted = attest_trial(trial, level=level, seed=17,
                                            policy=policy)
                    self.assertEqual(accepted["outcome"], TERMINALS[policy][0])


if __name__ == "__main__":
    unittest.main()
