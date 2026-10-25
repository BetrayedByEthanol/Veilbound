"""Formal Priest Life Focus balance: preserve source truth and no-tune gate."""
from copy import deepcopy
import json
import unittest

from scripts.b05_priest_life_formal_balance_assessment_v0 import (
    COUNTS,DECISION,GAPS,ROLES,ROWS,KEYS,BASE_KEYS,
    _key,assess_matrices,run_assessment,attest_assessment,
)
from scripts.b05_three_focus_life_comparison_v0 import run_matrix as self_matrix
from scripts.b05_three_focus_life_extended_attrition_v0 import run_matrix as attrition_matrix
from scripts.b05_priest_life_multi_recipient_stress_v0 import run_matrix as multi_matrix
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def stat(report,stratum,role,policy):
    cells=[c for c in report["cohort_observations"][stratum]
           if c["role"]==role and c["policy"]==policy]
    if len(cells)!=1:
        raise AssertionError("Exactly one named Focus-policy cohort")
    return cells[0]


class FormalPriestLifeFocusAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence={
            "matched_self":self_matrix(seed=0),
            "extended_attrition":attrition_matrix(seed=0),
            "multi_recipient":multi_matrix(seed=0),
        }
        cls.report=assess_matrices(cls.evidence)

    def test_01_all_three_native_audits_and_primary_case_count(self):
        r=self.report
        self.assertEqual(r["scenario_counts"],COUNTS)
        self.assertEqual(r["primary_scenario_total"],1384)
        self.assertEqual(r["historical_H_M_ally_context_only"],36)
        self.assertEqual(r["assessment_sha256"],canonical_digest(
            {k:v for k,v in r.items() if k!="assessment_sha256"}))
        for item in r["source_evidence"]:
            self.assertEqual(item["native_matrix_sha256"],
                             self.evidence[item["stratum"]]["audit_sha256"])
            self.assertEqual(item["cases"],COUNTS[item["stratum"]])
        self.assertEqual(r["formal_mechanical_audit"],
                         "complete_for_bounded_source_scenes")

    def test_02_every_witness_counted_once_and_source_policy_not_reweighted(self):
        cohort_counts={"matched_self":12,"extended_attrition":14,
                       "multi_recipient":20}
        for name,expected in cohort_counts.items():
            cells=self.report["cohort_observations"][name]
            self.assertEqual(len(cells),expected)
            self.assertEqual(sum(c["witness_cells"] for c in cells),COUNTS[name])
            self.assertEqual(len({(x["role"],x["policy"]) for x in cells}),
                             len(cells))
            for c in cells:
                self.assertGreater(c["witness_cells"],0)
                self.assertEqual(c["witness_cells"],
                                 c["same_exposure_cells"]+
                                 c["changed_exposure_cells"])
                for field in (
                    "higher_terminal_hp_cells","lower_terminal_hp_cells",
                    "higher_terminal_vigor_cells","lower_terminal_vigor_cells"):
                    self.assertLessEqual(c[field],c["same_exposure_cells"])
        self.assertEqual(len(self.report["verified_focus_capabilities"]),4)

    def test_03_same_source_baselines_per_authored_scene_not_all_Focus_weights(self):
        for name,mat in self.evidence.items():
            cells=mat[ROWS[name]]
            base={_key(x,BASE_KEYS[name]):x for x in cells
                  if x["policy"]=="baseline"}
            self.assertTrue(base)
            self.assertEqual(len({tuple(x[k] for k in KEYS[name])
                                  for x in cells}),len(cells))
            for c in cells:
                b=base[_key(c,BASE_KEYS[name])]
                self.assertEqual(c["source_digests"],b["source_digests"])
                if c["policy"]=="baseline":
                    self.assertTrue(all(v==0 for v in
                                        c["delta_vs_same_source_baseline"].values()))

    def test_04_no_magic_baseline_cannot_create_an_effectiveness_win(self):
        for name in COUNTS:
            for role in ROLES:
                baseline=stat(self.report,name,role,"baseline")
                self.assertEqual(baseline["witness_cells"],
                                 baseline["same_exposure_cells"])
                self.assertEqual(baseline["higher_terminal_hp_cells"],0)
                self.assertEqual(baseline["higher_terminal_vigor_cells"],0)
                self.assertEqual(baseline["lower_terminal_hp_cells"],0)
                self.assertEqual(baseline["lower_terminal_vigor_cells"],0)
                self.assertEqual(baseline["nonzero_spent_vp_cells"],0)
                self.assertEqual(baseline["nonzero_ap_paid_cells"],0)

    def test_05_attrition_mismatched_rounds_are_not_HP_deltas(self):
        name="extended_attrition"
        rows=self.evidence[name][ROWS[name]]
        baselines={_key(c,BASE_KEYS[name]):c for c in rows
                   if c["policy"]=="baseline"}
        for role in ROLES:
            for cohort in (x for x in self.report["cohort_observations"][name]
                           if x["role"]==role):
                chosen=[c for c in rows if c["role"]==role
                        and c["policy"]==cohort["policy"]]
                mismatched=sum(c["metrics"]["rounds_completed"]!=
                               baselines[_key(c,BASE_KEYS[name])]
                               ["metrics"]["rounds_completed"]
                               for c in chosen)
                self.assertEqual(cohort["changed_exposure_cells"],mismatched)
                self.assertEqual(cohort["longer_survival_windows"],
                                 sum(c["round_completion_delta"]>0
                                     for c in chosen))
                self.assertEqual(cohort["shorter_survival_windows"],
                                 sum(c["round_completion_delta"]<0
                                     for c in chosen))

    def test_06_multi_target_missing_source_attacks_excluded_from_like_exposure(self):
        name="multi_recipient"
        rows=self.evidence[name][ROWS[name]]
        baselines={_key(c,BASE_KEYS[name]):c for c in rows
                   if c["policy"]=="baseline"}
        for cohort in self.report["cohort_observations"][name]:
            chosen=[c for c in rows if c["role"]==cohort["role"]
                    and c["policy"]==cohort["policy"]]
            diffs=sum(c["metrics"]["paid_enemy_hits"]!=
                      baselines[_key(c,BASE_KEYS[name])]
                      ["metrics"]["paid_enemy_hits"]
                      for c in chosen)
            self.assertEqual(cohort["changed_exposure_cells"],diffs)
            self.assertEqual(cohort["skipped_dead_target_cells"],
                             sum(c["metrics"]["skipped_dead_target"]>0
                                 for c in chosen))

    def test_07_medium_intercession_evidence_is_limited_to_true_native_receipts(self):
        guided=stat(self.report,"multi_recipient","M","guided_intercession")
        vital=stat(self.report,"multi_recipient","M","shelter_intercession")
        self.assertGreater(guided["guided_intercession_receipts"],0)
        self.assertEqual(guided["vital_intercession_receipts"],0)
        self.assertGreater(vital["vital_intercession_receipts"],0)
        self.assertEqual(vital["guided_intercession_receipts"],0)
        self.assertGreater(guided["nonzero_spent_vp_cells"],0)
        self.assertGreater(vital["nonzero_spent_vp_cells"],0)
        self.assertGreater(stat(self.report,"multi_recipient","M",
                                "guided_reassign")["reassignment_receipts"],0)

    def test_08_low_A_can_paid_heal_but_low_B_does_not_gain_a_free_hand(self):
        triage=stat(self.report,"multi_recipient","A","triage")
        combination=stat(self.report,"multi_recipient","A","chosen_and_heal")
        self.assertGreater(triage["paid_heal_receipts"],0)
        self.assertGreater(combination["paid_heal_receipts"],0)
        for c in self.report["cohort_observations"]["multi_recipient"]:
            if c["role"]=="B":
                self.assertEqual(c["paid_heal_receipts"],0)
                self.assertEqual(c["guided_intercession_receipts"],0)
                self.assertEqual(c["vital_intercession_receipts"],0)

    def test_09_high_two_ally_projections_are_separate_paid_source_actions(self):
        split=stat(self.report,"multi_recipient","H","split_wards")
        self.assertGreater(split["nonzero_ap_paid_cells"],0)
        self.assertGreater(split["nonzero_committed_vp_cells"],0)
        self.assertEqual(split["guided_intercession_receipts"],0)
        self.assertEqual(split["vital_intercession_receipts"],0)
        self.assertGreater(stat(self.report,"multi_recipient","H",
                                "triage")["paid_heal_receipts"],0)

    def test_10_low_self_exaltation_not_elevated_to_external_party_buff(self):
        for role in ("A","B"):
            self.assertGreater(
                stat(self.report,"extended_attrition",role,"exaltation")
                    ["witness_cells"],0)
        self.assertNotIn(
            ("B","triage"),
            {(c["role"],c["policy"]) for c in
             self.report["cohort_observations"]["multi_recipient"]})
        self.assertFalse(self.evidence["matched_self"]
                         ["low_ally_comparison_supported"])
        self.assertFalse(self.evidence["multi_recipient"]
                         ["low_chosen_external_targeting"])

    def test_11_explicit_decision_hold_prices_and_nonstatistical_classification(self):
        r=self.report
        self.assertEqual(r["decision"],DECISION)
        self.assertFalse(r["global_balance_certified"])
        self.assertFalse(r["numerical_tuning_authorized"])
        for field in ("focus_ranking","sampled_win_rate",
                      "confidence_interval","cross_focus_utility_weights"):
            self.assertIsNone(r[field])
        self.assertTrue(r["different_policy_cells_not_equal_resource_prices"])
        self.assertTrue(r["early_stop_and_dead_target_exposure_excluded_from_terminal_deltas"])
        self.assertGreaterEqual(len(r["unresolved_gates"]),6)
        self.assertEqual({x["id"] for x in r["unresolved_gates"]},
                         {g[0] for g in GAPS})

    def test_12_reject_tampered_or_partial_native_input(self):
        altered=deepcopy(self.evidence)
        altered["matched_self"]["matched_self"][0]["metrics"]["final_hp"]=999
        with self.assertRaises(AssertionError):
            assess_matrices(altered)
        altered=deepcopy(self.evidence)
        altered["multi_recipient"]["cases"].pop()
        altered["multi_recipient"]["audit_sha256"]=canonical_digest(
            {k:v for k,v in altered["multi_recipient"].items()
             if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            assess_matrices(altered)
        altered=deepcopy(self.evidence)
        altered["extended_attrition"]["only_actual_rounds_counted"]=False
        altered["extended_attrition"]["audit_sha256"]=canonical_digest(
            {k:v for k,v in altered["extended_attrition"].items()
             if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            assess_matrices(altered)

    def test_13_conflicting_source_ids_and_missing_baseline_fail_closed(self):
        altered=deepcopy(self.evidence)
        altered["multi_recipient"]["cases"][0]["source_digests"]["priest"]="f"*64
        altered["multi_recipient"]["audit_sha256"]=canonical_digest(
            {k:v for k,v in altered["multi_recipient"].items()
             if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            assess_matrices(altered)
        altered=deepcopy(self.evidence)
        altered["matched_self"]["matched_self"][0]["policy"]="phantom"
        altered["matched_self"]["audit_sha256"]=canonical_digest(
            {k:v for k,v in altered["matched_self"].items()
             if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            assess_matrices(altered)

    def test_14_independent_source_replay_rejects_rehashed_assessment(self):
        expected=run_assessment(seed=0)
        self.assertEqual(expected,self.report)
        forged=deepcopy(expected)
        forged["cohort_observations"]["matched_self"][0]["higher_terminal_hp_cells"]=999
        forged["assessment_sha256"]=canonical_digest(
            {k:v for k,v in forged.items() if k!="assessment_sha256"})
        with self.assertRaises(AssertionError):
            attest_assessment(forged,seed=0)
        with self.assertRaises(ValueError):
            run_assessment(seed=True)
        with self.assertRaises(ValueError):
            run_assessment(seed=-1)

    def test_15_emit_bounded_reproducible_evidence_summary(self):
        r=self.report
        selected=[
            (name,role,policy,stat(r,name,role,policy))
            for name,role,policy in (
                ("matched_self","B","exaltation"),
                ("extended_attrition","H","heal_cycle"),
                ("extended_attrition","B","exaltation"),
                ("multi_recipient","H","split_wards"),
                ("multi_recipient","M","guided_intercession"),
                ("multi_recipient","M","shelter_intercession"),
                ("multi_recipient","A","triage"),
                ("multi_recipient","B","chosen_self"),
            )]
        condensed={f"{name}:{role}:{policy}":{
            "n":s["witness_cells"],"same_exposure":s["same_exposure_cells"],
            "more_HP":s["higher_terminal_hp_cells"],
            "more_Vigor":s["higher_terminal_vigor_cells"],
            **({"heals":s["paid_heal_receipts"],
                "guided_intercessions":s["guided_intercession_receipts"],
                "vital_intercessions":s["vital_intercession_receipts"]}
               if name=="multi_recipient" else {})}
            for name,role,policy,s in selected}
        print("B05_FORMAL_SOURCE_COUNTS "+json.dumps(
            {"assessment_sha256":r["assessment_sha256"],
             "scenario_counts":r["scenario_counts"],
             "witnesses":condensed},sort_keys=True))


if __name__=="__main__":
    unittest.main()
