"""B04/B06/B07 noncertifying acceptance triage and human test readiness."""
import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 import (
    report, cohort_templates, focus_field_sheet, FOCUS_TASKS,
    CRITERIA, GATES, COHORTS,
)
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import (
    blank_packet as focus_blank,
)
from scripts.b04_b07_pilot_evidence_cohorts_v0 import (
    preflight as cohort_preflight,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class AcceptanceReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=report()

    def test_01_current_roster_counts_and_36_explicit_level_slots(self):
        r=self.r
        self.assertEqual((r["source_pairings"],r["structural_variants"],
                          r["structural_level_snapshots"],
                          r["focus_level_review_slots"]),(12,13,39,36))
        self.assertEqual({x["pairing"] for x in r["review_matrix"]},
                         set(FOCUS_TASKS))
        self.assertEqual(
            {(x["pairing"],x["level"]) for x in r["review_matrix"]},
            {(p,l) for p in FOCUS_TASKS for l in (1,2,3)})
        self.assertEqual(len(r["review_matrix"]),36)

    def test_02_all_seven_criteria_per_level_remain_unverified(self):
        for row in self.r["review_matrix"]:
            self.assertEqual(
                [x["criterion"] for x in row["tasks"]],list(CRITERIA))
            self.assertTrue(all(not x["independently_accepted"]
                                for x in row["tasks"]))
            self.assertTrue(all(not x["machine_fixture_is_human_play"]
                                for x in row["tasks"]))
            self.assertTrue(all(x["status"]=="MISSING_AUTHENTICATED_EVIDENCE"
                                for x in row["tasks"]))
            self.assertFalse(row["certified"])
            self.assertFalse(row["genuine_gm_and_player_sessions_recorded"])
        self.assertEqual(self.r["unmet_independent_criterion_slots"],252)

    def test_03_canonical_mvp_six_gates_unchanged(self):
        r=self.r
        self.assertEqual([g["gate"] for g in r["gate_status"]],
                         [name for name,_ in GATES])
        self.assertTrue(all(g["status"]=="OPEN"
                            and not g["independent_signoff"]
                            for g in r["gate_status"]))
        self.assertEqual((r["full_focus_certificates"],
                          r["human_sessions_verified"],
                          r["actual_gm_milestones_verified"],
                          r["mvp_exit_gates_closed"],
                          r["original_blockers_closed"]),(0,0,0,0,3))

    def test_04_fixture_scope_does_not_claim_twelve_focus_coverage(self):
        r=self.r
        machine={(row["pairing"],row["level"]) for row in r["review_matrix"]
                 if row["bounded_fixture_present"]}
        self.assertEqual(machine,{
            ("Priest/Low",1),("Priest/Low",2),("Priest/Low",3),
            ("Scholar/High",1),("Scholar/High",2),("Scholar/High",3)})
        self.assertTrue(all(not row["complete_focus_native_play_verified"]
                            for row in r["review_matrix"]))
        for row in r["review_matrix"]:
            if row["pairing"] not in ("Priest/Low","Scholar/High"):
                self.assertTrue(all(not t["existing_machine_fixture"]
                                    for t in row["tasks"]))
        fixture=r["native_fixture"]
        self.assertFalse(fixture["real_player_session"])
        self.assertFalse(fixture["authored_awards_are_real_gm_declarations"])
        self.assertNotEqual(fixture["l1_evidence_sha256"],
                            fixture["l2_evidence_sha256"])
        self.assertNotEqual(fixture["l2_evidence_sha256"],
                            fixture["l3_evidence_sha256"])
        self.assertEqual(len(set(fixture["authored_milestone_ids"])),2)

    def test_05_low_priest_ab_physical_proxy_is_one_pairing(self):
        priest=[x for x in self.r["review_matrix"]
                if x["pairing"]=="Priest/Low"]
        self.assertEqual(len(priest),3)
        self.assertEqual({x["structural_variants"] for x in priest},{2})
        self.assertIn("physical A/B proxy",
                      next(x for x in priest
                           if x["level"]==2)["tasks"][2]["existing_machine_fixture"][0])

    def test_06_human_play_runbook_and_constrained_cohort_allocation(self):
        r=self.r
        self.assertEqual([x["level"] for x in r["four_session_beats"]],
                         [1,2,2,3])
        self.assertEqual([x["beats"] for x in r["four_session_beats"]],
                         [["supply","gate"],["forest"],["shrine"],["village"]])
        self.assertEqual(r["session_options"],[3,4,5])
        self.assertEqual(len(r["procedure"]),6)
        self.assertEqual(set.union(*(set(x) for x in COHORTS.values())),
                         set(FOCUS_TASKS))
        self.assertEqual(sum(len(x) for x in COHORTS.values()),12)
        self.assertTrue(all(len(x)==4 for x in COHORTS.values()))

    def test_07_existing_flexible_intake_templates_are_blank_and_valid(self):
        templates=cohort_templates()
        self.assertEqual(len(templates),3)
        for form in templates:
            self.assertEqual(form["status"],"CANDIDATE_UNVERIFIED")
            self.assertEqual((form["cohorts"][0]["sessions"],
                              form["cohorts"][0]["milestones"],
                              form["cohorts"][0]["focus_level_evidence"]),
                             ([],[],[]))
            self.assertEqual(form["independently_certified_focuses"],0)
            self.assertEqual(form["strict_mvp_exits_met"],0)
            self.assertEqual(
                cohort_preflight(deepcopy(form))["strict_mvp_exits_met"],0)
        self.assertEqual(len(set(x["cohorts"][0]["cohort_id"]
                                 for x in templates)),3)

    def test_08_source_fingerprints_are_derived_not_guessed(self):
        templates=cohort_templates()
        for row in self.r["review_matrix"]:
            baseline=focus_blank(row["pairing"])
            self.assertEqual(row["source_fingerprints"],
                             baseline["source_fingerprints"])
            self.assertEqual(row["structural_issues"],[])
            self.assertEqual(len(row["source_fingerprints"])>=1,True)
        source_map={r["pairing"]:r["source_fingerprints"]
                    for r in self.r["review_matrix"] if r["level"]==1}
        self.assertEqual(self.r["source_roster_digest"],
                         canonical_digest(source_map))
        for form in templates:
            self.assertEqual(form["source_roster_digest"],
                             self.r["source_roster_digest"])

    def test_09_field_sheet_reuses_existing_protocol_blank_form(self):
        for pair in FOCUS_TASKS:
            sheet=focus_field_sheet(pair)
            self.assertEqual(sheet["source_intake_template"],
                             focus_blank(pair))
            self.assertEqual([x["level"] for x in sheet["level_tasks"]],
                             [1,2,3])
            self.assertFalse(sheet["independently_full_certified"])
            self.assertEqual(sheet["strict_mvp_exits_met"],0)
            self.assertEqual(sheet["source_intake_template"]["report_author_ref"],"")

    def test_10_unsupported_scope_and_fabricated_run_claims_fail(self):
        with self.assertRaises(ValueError):
            focus_field_sheet("Priest/Ultra")
        forged=deepcopy(self.r)
        forged["full_focus_certificates"]=12
        # The report is generated afresh; downstream caller changes have
        # no effect on independently calculated source state.
        self.assertEqual(report()["full_focus_certificates"],0)
        with patch(
            "scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0.run",
            return_value={"l2_outcome":"party_scene_withdrawal",
                          "l3_outcome":"sentry_defeat",
                          "original_source_g8_terminals":2,
                          "human_sessions":1,
                          "independently_certified_focuses":0,
                          "strict_mvp_exits_met":0}):
            with self.assertRaises(ValueError):
                report()

    def test_11_machine_readable_register_and_templates_stay_json_safe(self):
        self.assertEqual(json.loads(json.dumps(self.r)),self.r)
        self.assertEqual(json.loads(json.dumps(cohort_templates())),
                         cohort_templates())


if __name__=="__main__":
    unittest.main()
