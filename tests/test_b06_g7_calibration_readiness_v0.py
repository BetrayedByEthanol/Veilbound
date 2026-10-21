"""B06 G7: scenario-space and native fixed-witness readiness regression."""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import json
import math
import unittest
from unittest.mock import patch

from scripts import b06_g7_calibration_readiness_v0 as g7


class G7MatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix=g7.scenario_matrix()
        cls.report=g7.build_readiness_report(replay=True)

    def test_01_complete_48_cell_cartesian_matrix_no_duplicates(self):
        self.assertEqual(len(self.matrix),48)
        self.assertEqual(len({x["scenario_id"] for x in self.matrix}),48)
        self.assertEqual({(x["level"],x["party_size"],x["opening"],
                           x["frontline"],x["policy"]) for x in self.matrix},
                         {(l,n,o,f,p) for l in (2,3) for n in (3,4)
                          for o in g7.OPENINGS for f in g7.FRONTS
                          for p in g7.POLICIES})
        self.assertEqual(self.matrix,g7.scenario_matrix())

    def test_02_explicit_native_component_and_blocked_evidence(self):
        counts=Counter(x["status"] for x in self.matrix)
        self.assertEqual(counts,{"fixed_native_window":4,
                                 "component_verified_only":2,
                                 "blocked_not_executable":42})
        for row in self.matrix:
            self.assertEqual(row["native_fixed_window_executable"],
                             row["status"]=="fixed_native_window")
            self.assertEqual(row["component_only"],
                             row["status"]=="component_verified_only")
            self.assertEqual(row["component_evidence_ref"],
                             g7.PROTECTION_EVIDENCE if row["component_only"] else None)
            self.assertIs(row["component_evidence_replayed"],False)
            self.assertEqual(row["known_missing_authority"]==[],
                             row["status"]=="fixed_native_window")
            self.assertIsNone(row["success_rate"])
            self.assertIsNone(row["ci95"])
            self.assertIsNone(row["creature_cr"])
            self.assertIsNone(row["terminal_count"])
            self.assertEqual(row["calibration_samples"],0)
            self.assertIs(row["complete_encounter_certified"],False)
            self.assertTrue(row["frozen_historical_phase3_not_a_comparator"])

    def test_03_actual_sourced_roster_ids_and_enemy_count(self):
        for row in self.matrix:
            self.assertEqual(row["roster_source_ids"],
                             list(g7.SOURCES[row["party_size"]]))
            self.assertEqual(row["enemy_source_id"],"B06-EN-03")
            self.assertEqual(row["enemy_count"],1)
            self.assertIn(row["party_size"],(3,4))
            self.assertIn(row["level"],(2,3))

    def test_04_ambush_cannot_be_mislabeled_native(self):
        blocked=[x for x in self.matrix if x["opening"]=="forest_ambush"]
        self.assertEqual(len(blocked),24)
        self.assertTrue(all(
            "native_ambush_1x2_pounce_contact_and_response_policy" in
            x["known_missing_authority"] and
            x["status"]=="blocked_not_executable" for x in blocked))

    def test_05_guardian_head_forward_needs_real_source_scene(self):
        candidates=[x for x in self.matrix
                    if x["frontline"]=="B_head_forward"]
        self.assertEqual(len(candidates),24)
        self.assertTrue(all(
            "alternate_frontline_source_defense_and_1x2_geometry" in
            x["known_missing_authority"] for x in candidates))
        self.assertFalse(any(x["native_fixed_window_executable"] for x in candidates))

    def test_06_shield_and_prepared_body_are_components_not_party_trials(self):
        protected=[x for x in self.matrix if x["policy"]!="decline_all"]
        self.assertEqual(len(protected),32)
        self.assertEqual(sum(x["component_only"] for x in protected),2)
        self.assertFalse(any(x["native_fixed_window_executable"] for x in protected))
        for x in protected:
            self.assertTrue(any("integrate_native_G6D_" in g
                                for g in x["known_missing_authority"]))

    def test_07_four_native_two_round_witnesses_are_source_bound(self):
        witnesses=[x for x in self.report["native_witnesses"]
                   if x["kind"]=="two_round_fixed_choice_window"]
        self.assertEqual(len(witnesses),4)
        for w in witnesses:
            self.assertEqual(w["rounds"],2)
            self.assertFalse(w["seed_is_random_trial"])
            self.assertEqual(w["ending"],"not_attested_full_encounter")
            self.assertEqual(w["roster"][0]["source"],"B06-EN-03")
            self.assertTrue(all(x["source_digest"] for x in w["roster"]))
            self.assertEqual(w["measures"]["round_ends"],2)
            self.assertEqual(w["measures"]["turn_ends"],
                             2*(w["party_size"]+1))
            self.assertEqual(w["measures"]["g2_arrows_launched"],2)
            self.assertEqual(w["measures"]["g6d_attested_bow"],0)
            self.assertEqual(w["measures"]["g6d_defeat_terminals"],0)
            self.assertEqual(w["measures"]["reactive_protections"],0)
            self.assertEqual(w["measures"]["prepared_protections"],0)
            self.assertIn(w["scenario_id"],
                          {r["scenario_id"] for r in self.matrix
                           if r["status"]=="fixed_native_window"})

    def test_08_scripted_death_overlays_not_added_as_fresh_sample_cells(self):
        terminal=[x for x in self.report["native_witnesses"]
                  if x["kind"]=="three_round_scripted_terminal_overlay"]
        self.assertEqual(len(terminal),2)
        for w in terminal:
            self.assertEqual(w["party_size"],4)
            self.assertEqual(w["rounds"],3)
            self.assertEqual(w["ending"],"hunter_defeat_attested")
            self.assertTrue(w["hunter_dead_at_stop"])
            self.assertFalse(w["hunter_dying_at_stop"])
            self.assertFalse(w["seed_is_random_trial"])
            self.assertEqual(w["measures"]["round_ends"],3)
            self.assertEqual(w["measures"]["turn_ends"],15)
            self.assertEqual(w["measures"]["g6d_attested_bow"],1)
            self.assertEqual(w["measures"]["g6d_defeat_terminals"],1)
            self.assertEqual(w["measures"]["g2_arrows_launched"],3)
            self.assertIn(w["scenario_id"],
                          {x["scenario_id"] for x in self.matrix})
        self.assertEqual(self.report["summary"]["replayed_native_witnesses"],6)
        self.assertEqual(self.report["summary"]["calibration_samples"],0)

    def test_09_report_deterministic_without_new_random_trials(self):
        twin=g7.build_readiness_report()
        self.assertEqual(self.report,twin)
        self.assertEqual(g7.canonical_digest(self.report),
                         g7.canonical_digest(twin))
        self.assertEqual(len(g7.canonical_digest(self.report)),64)

    def test_10_manifest_only_is_explicitly_not_witness_execution(self):
        light=g7.build_readiness_report(replay=False)
        self.assertEqual(light["matrix"],self.matrix)
        self.assertEqual(light["native_witnesses"],[])
        self.assertEqual(light["summary"]["replayed_native_witnesses"],0)
        self.assertEqual(light["summary"]["calibration_samples"],0)
        self.assertNotEqual(g7.canonical_digest(light),
                            g7.canonical_digest(self.report))

    def test_11_calibration_wilson_rejects_invalid_or_empty_samples(self):
        for success,n in ((0,0),(-1,10),(11,10),(1,-1),
                          (True,20),(1,False),(0,1.0),(1.0,4),
                          (2,1)):
            with self.subTest(success=success,n=n):
                with self.assertRaises(ValueError):
                    g7.wilson_95(success,n)

    def test_12_wilson_sane_limits_do_not_publish_current_rate(self):
        a=g7.wilson_95(0,100)
        b=g7.wilson_95(100,100)
        middle=g7.wilson_95(50,100)
        self.assertEqual(a[0],0.0)
        self.assertEqual(b[1],1.0)
        self.assertGreater(a[1],0)
        self.assertLess(b[0],1)
        self.assertTrue(middle[0]<0.5<middle[1])
        self.assertTrue(all(math.isfinite(z) and 0<=z<=1
                            for z in (*a,*b,*middle)))
        self.assertIsNone(self.report["future_inference_policy"]["current_win_probability"])

    def test_13_phase3_referenced_but_unmodified_and_not_replayed(self):
        self.assertEqual(self.report["historical_phase3_windows"],4096)
        self.assertEqual(self.report["historical_phase3_seeds"],128)
        self.assertEqual(self.report["historical_phase3_cells"],32)
        self.assertFalse(self.report["historical_phase3_recomputed"])
        self.assertTrue(self.report["historical_phase3_is_not_current_native_cohort"])
        self.assertEqual(self.report["historical_phase3_audit_sha256"],
                         "c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b")

    def test_14_frozen_fixed_witnesses_do_not_create_cr_or_certification(self):
        self.assertEqual(self.report["summary"]["certified_party_pack_count"],0)
        self.assertIsNone(self.report["summary"]["hunter_challenge_rating"])
        self.assertIsNone(self.report["future_inference_policy"]["current_cr"])
        self.assertEqual(self.report["future_inference_policy"]["candidate_pilot_seeds_per_cell"],128)
        self.assertTrue(self.report["future_inference_policy"]["report_unresolved_as_own_denominator_category"])
        self.assertTrue(self.report["future_inference_policy"]["do_not_condition_win_rate_on_resolved_subset"])
        self.assertEqual(self.report["evidence_grade"],
                         "planning_with_fixed_native_witnesses")

    def test_15_ledger_validator_rejects_reordered_or_spoofed_events(self):
        fake=[{"index":1,"round":1,"kind":"round_end","detail":{}}]
        with self.assertRaisesRegex(AssertionError,"native G0"):
            g7._ledger_measures(fake)
        fake[0]["index"]=0
        fake[0]["round"]=True
        with self.assertRaisesRegex(AssertionError,"native G0"):
            g7._ledger_measures(fake)

    def test_16_ledger_measures_no_guess_from_empty_events(self):
        value=g7._ledger_measures([])
        self.assertTrue(all(type(x) is int and x==0 for x in value.values()))

    def test_17_seed_replay_is_not_counted_as_independent_outcome(self):
        for w in self.report["native_witnesses"]:
            self.assertFalse(w["seed_is_random_trial"])
            self.assertIsInstance(w["seed"],int)
            self.assertIn(w["level"],(2,3))
        self.assertTrue(all(x["calibration_samples"]==0 for x in self.matrix))

    def test_18_source_provenance_paths_are_actual_native_boundaries(self):
        self.assertIn("scripts/b06_hunter_mixed_party_g6c_v0.py",
                      self.report["native_source_paths"])
        self.assertIn("scripts/b06_hunter_completion_g6d_v0.py",
                      self.report["native_source_paths"])
        self.assertIn("scripts/b06_hunter_reactive_intervene_g6d_v0.py",
                      self.report["native_source_paths"])
        self.assertIn("content/creatures/b06-hunter-of-the-woods.v0.json",
                      self.report["native_source_paths"])

    def test_19_banned_boolean_replay_input(self):
        for bad in (None,0,1,[],{},"false"):
            with self.assertRaises(ValueError):
                g7.build_readiness_report(replay=bad)

    def test_20_cli_returns_verifiable_machine_readable_digest(self):
        target=StringIO()
        with redirect_stdout(target):
            g7.main(["--manifest-only"])
        parsed=json.loads(target.getvalue())
        digest=parsed.pop("readiness_sha256")
        self.assertEqual(digest,g7.canonical_digest(parsed))
        self.assertEqual(parsed["summary"]["planned_cells"],48)
        self.assertFalse(parsed["native_witnesses"])
        self.assertTrue(parsed["historical_phase3_is_not_current_native_cohort"])

    def test_21_digest_changes_when_scoping_or_sample_claim_changes(self):
        light=g7.build_readiness_report(replay=False)
        original=g7.canonical_digest(light)
        light["summary"]["calibration_samples"]=1
        self.assertNotEqual(original,g7.canonical_digest(light))

    def test_22_no_misleading_win_probability_on_scripted_lethal_witness(self):
        defeats=[w for w in self.report["native_witnesses"]
                 if w["ending"]=="hunter_defeat_attested"]
        self.assertEqual(len(defeats),2)
        self.assertIsNone(self.report["future_inference_policy"]["current_win_probability"])
        self.assertTrue(all(row["success_rate"] is None
                            for row in self.report["matrix"]))


    def test_23_protection_evidence_is_exactly_native_p4_l3_fixture(self):
        verified=[x for x in self.matrix if x["component_only"]]
        self.assertEqual(len(verified),2)
        self.assertEqual(
            {(x["level"],x["party_size"],x["opening"],
              x["frontline"],x["policy"]) for x in verified},
            {(3,4,"warned_clear","A_head_forward","reactive_shield"),
             (3,4,"warned_clear","A_head_forward","prepared_body")})
        self.assertEqual(
            g7.PROTECTION_WITNESSED,
            frozenset({(3,4,"reactive_shield"),(3,4,"prepared_body")}))
        self.assertEqual(
            {x["component_evidence_ref"] for x in verified},
            {"tests/test_b06_hunter_reactive_intervene_g6d_v0.py"})
        self.assertTrue(all(x["component_evidence_replayed"] is False
                            for x in verified))

    def test_24_other_six_clear_a_front_protective_cases_are_unverified(self):
        requested=[x for x in self.matrix
                   if x["opening"]=="warned_clear"
                   and x["frontline"]=="A_head_forward"
                   and x["policy"]!="decline_all"]
        self.assertEqual(len(requested),8)
        unverified=[x for x in requested if not x["component_only"]]
        self.assertEqual(len(unverified),6)
        self.assertEqual(
            {(x["level"],x["party_size"],x["policy"])
             for x in unverified},
            {(2,3,"reactive_shield"),(2,3,"prepared_body"),
             (2,4,"reactive_shield"),(2,4,"prepared_body"),
             (3,3,"reactive_shield"),(3,3,"prepared_body")})
        for row in unverified:
            self.assertEqual(row["status"],"blocked_not_executable")
            self.assertIn(
                "G6D_protection_component_not_verified_at_level_party_size",
                row["known_missing_authority"])
            self.assertIsNone(row["component_evidence_ref"])
            self.assertFalse(row["component_evidence_replayed"])
        summary=self.report["summary"]
        self.assertEqual(
            (summary["planned_cells"],summary["native_fixed_window_cells"],
             summary["component_only_cells"],summary["blocked_cells"]),
            (48,4,2,42))
        self.assertEqual(
            sum(x["component_only"] for x in self.report["matrix"]),
            summary["component_only_cells"])


if __name__=="__main__":
    unittest.main()
