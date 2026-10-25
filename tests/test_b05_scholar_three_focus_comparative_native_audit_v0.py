"""B04/B05 genuine three-Focus Scholar source / matched-native audit tests."""
from copy import deepcopy
from unittest import TestCase, main

from scripts.b05_scholar_three_focus_comparative_native_audit_v0 import (
    FOCUSES, LEVELS, ROLES, EXPECTED, SOURCE_PATHS, verify_basis,
    row, matched_soldier, attest_matched, run_audit, attest_audit,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_encounter_state_v0 import ROOT, party_actor


class ThreeFocusScholarAuditTests(TestCase):
    def test_01_verifies_actual_source_bytes_and_exact_declarations(self):
        basis=verify_basis()
        self.assertEqual(set(basis),set(SOURCE_PATHS))
        self.assertGreaterEqual(len(basis),15)
        self.assertTrue(all(len(x["sha256"])==64 and x["bytes"]>0
                            for x in basis.values()))
        self.assertEqual(len(FOCUSES),3)
        self.assertEqual(tuple(ROLES.values()),("F","S","T"))
        self.assertTrue((ROOT/SOURCE_PATHS[0]).is_file())

    def test_02_nine_selected_sheets_are_source_native(self):
        for level in LEVELS:
            for focus in FOCUSES:
                with self.subTest(level=level,focus=focus):
                    a=row(focus,level)
                    e=EXPECTED[focus]
                    self.assertEqual(a["actor_source_id"],ROLES[focus])
                    self.assertEqual(a["hp_max"],12)
                    self.assertEqual(a["vigor_max"],12*level)
                    self.assertEqual(a["vp_max"],e["vp_rate"]*level)
                    self.assertEqual(a["turn_ap"],30+6*(level-1))
                    self.assertEqual(a["physical_ap"],e["physical_ap"])
                    self.assertEqual(a["projection_ap"],e["projection_ap"])
                    self.assertEqual(a["base_regen"],e["regen"])
                    self.assertEqual(a["movement_mp"],12)
                    self.assertEqual(a["known_count"],e["known"][level-1])
                    self.assertFalse(a["physical_and_projection_same_turn"])
                    self.assertTrue(a["only_structural_source_certified"])
                    self.assertFalse(a["full_focus_certified"])
                    self.assertEqual(len(a["actor_source_sha256"]),64)

    def test_03_high_no_free_guard_and_real_prep_formula_capacity(self):
        for lv,cp in ((1,1),(2,2),(3,0)):
            r=row("High",lv)
            self.assertIsNone(r["guard_value"])
            self.assertIsNone(r["guard_instrument"])
            self.assertIsNone(r["prepared_arsenal"])
            self.assertEqual(r["prepared_formula_capacity"],cp)
            self.assertTrue(r["authoritative_native_outgoing_flame"])
            self.assertEqual(r["stone_self_committed"],2*lv)

    def test_04_medium_has_not_gained_low_prepared_or_priest_reroute(self):
        for lv in LEVELS:
            r=row("Medium",lv)
            self.assertIsNone(r["prepared_arsenal"])
            self.assertIsNone(r["prepared_formula_capacity"])
            self.assertEqual(r["stone_self_committed"],1)
            self.assertTrue(r["guided_eligible_native"])
            self.assertEqual(r["physical_tempo"],1)
            self.assertEqual(r["projection_tempo"],1)
            self.assertEqual(r["guard_value"],17)

    def test_05_low_prepared_subset_not_all_known_or_high_composite(self):
        for lv in LEVELS:
            r=row("Low",lv)
            self.assertEqual(len(r["prepared_arsenal"]),2 if lv==1 else 3)
            self.assertEqual(r["unprepared_known"],
                             ["Conjure Flame"] if lv==1 else ["Basic Heal"])
            self.assertTrue(r["guided_eligible_native"])
            self.assertEqual(r["stone_self_committed"],1 if lv==1 else 2)
            self.assertEqual(r["physical_tempo"],2 if lv==3 else 1)
            self.assertEqual(r["projection_tempo"],1)
            self.assertIsNone(r["prepared_formula_capacity"])

    def test_06_six_hour_vp_model_is_not_instant_native_recovery(self):
        recovery={"High":(2,3,5),"Medium":(1,2,3),"Low":(1,1,2)}
        for focus,expected in recovery.items():
            self.assertEqual(tuple(row(focus,lv)[
                "vp_recovery_completed_six_hours"] for lv in LEVELS),expected)

    def test_07_same_original_soldier_receipts_in_all_matched_scenes(self):
        for lv in LEVELS:
            for focus in FOCUSES:
                for policy in ("baseline","stone"):
                    with self.subTest(level=lv,focus=focus,policy=policy):
                        r=matched_soldier(focus,lv,policy)
                        self.assertEqual(r["inputs"],{
                            "rounds":3,"enemy":"B06-EN-02",
                            "attack_face":12,"damage_face":5,
                            "wound_location_roll":8,"defense":"take_hit",
                            "source":ROLES[focus]})
                        self.assertEqual(r["metrics"]["g5_hits"],3)
                        self.assertEqual(r["metrics"]["g4_damage_receipts"],3)
                        self.assertEqual(r["metrics"]["true_self_steps"],3)
                        self.assertEqual(r["ledger_sha256"],
                                         canonical_digest(r["ledger"]))
                        self.assertFalse(r["full_focus_certified"])
                        self.assertIsNone(r["win_rate"])

    def test_08_matched_stone_is_paid_and_reduces_real_hp_loss(self):
        for lv in LEVELS:
            outcomes={focus:{
                policy:matched_soldier(focus,lv,policy)["metrics"]
                for policy in ("baseline","stone")} for focus in FOCUSES}
            for focus in FOCUSES:
                with self.subTest(level=lv,focus=focus):
                    base=outcomes[focus]["baseline"]
                    stone=outcomes[focus]["stone"]
                    self.assertEqual(base["paid_projection_ap"],0)
                    self.assertEqual(stone["paid_projection_ap"],
                                     EXPECTED[focus]["projection_ap"])
                    self.assertEqual(stone["paid_projection_actions"],1)
                    self.assertEqual(base["stone_committed"],0)
                    self.assertEqual(stone["stone_committed"],
                                     row(focus,lv)["stone_self_committed"])
                    self.assertEqual(stone["vp"][1],
                                     stone["stone_committed"])
                    self.assertEqual(stone["vp"][2],0)
                    self.assertGreater(stone["hp"],base["hp"])
            self.assertEqual(outcomes["High"]["stone"]["stone_r"],2)
            self.assertEqual(outcomes["Medium"]["stone"]["stone_r"],1)
            self.assertEqual(outcomes["Low"]["stone"]["stone_r"],2)

    def test_09_matched_baseline_same_guardless_take_hit_input(self):
        for lv in LEVELS:
            a=[matched_soldier(focus,lv,"baseline") for focus in FOCUSES]
            self.assertTrue(all(q["metrics"]["g5_hits"]==3 for q in a))
            self.assertTrue(all(x["metrics"]["stone_r"]==0 for x in a))
            self.assertEqual(len({q["sources"]["foe"] for q in a}),1)
            self.assertEqual(len({q["inputs"]["damage_face"] for q in a}),1)

    def test_10_matched_replay_rejects_changed_report_with_refreshed_hash(self):
        args={"focus":"Medium","level":2,"policy":"stone","seed":0}
        original=matched_soldier(**args)
        self.assertEqual(attest_matched(original,**args),original)
        fake=deepcopy(original)
        fake["metrics"]["hp"]+=1
        with self.assertRaises(AssertionError):
            attest_matched(fake,**args)
        fake=deepcopy(original)
        fake["ledger"][0]["kind"]="forged"
        fake["ledger_sha256"]=canonical_digest(fake["ledger"])
        with self.assertRaises(AssertionError):
            attest_matched(fake,**args)

    def test_11_full_audit_witnesses_have_separate_cohorts(self):
        a=run_audit()
        self.assertEqual(len(a["rows"]),9)
        self.assertEqual(a["native_matched_count"],18)
        self.assertEqual(a["prior_cohort_count"],28)
        self.assertEqual(len(a["prior_native_separate_cohorts"]),28)
        self.assertEqual(a["audit_sha256"],canonical_digest(
            {k:v for k,v in a.items() if k!="audit_sha256"}))
        self.assertTrue(a["caution"]["matched_attack_inputs_identical"])
        self.assertTrue(a["caution"]["prior_medium_low_damage_faces_not_identical"])
        self.assertFalse(a["caution"]["native_three_focus_offense_matched"])
        self.assertFalse(a["caution"]["adaptive_attacker_policy"])
        self.assertFalse(a["caution"]["full_focus_certified"])
        self.assertFalse(a["caution"]["numerical_balance_tuning_authorized"])
        self.assertIsNone(a["caution"]["statistical_win_rate"])

    def test_12_unduplicated_per_focus_prior_native_provenance(self):
        a=run_audit()
        cells=a["prior_native_separate_cohorts"]
        self.assertEqual(len({(c["focus"],c["level"],c["policy"])
                              for c in cells}),28)
        self.assertEqual(sum(c["focus"]=="Medium" for c in cells),14)
        self.assertEqual(sum(c["focus"]=="Low" for c in cells),14)
        self.assertEqual({c["original_face_damage"]
                          for c in cells if c["focus"]=="Medium"},{5})
        self.assertEqual({c["original_face_damage"]
                          for c in cells if c["focus"]=="Low"},{6})
        self.assertTrue(all(c["evidence_scope"]==
            "original_distinct_source_policy_not_matched" for c in cells))
        self.assertNotIn("High",{c["focus"] for c in cells})

    def test_13_full_audit_attestation_rejects_forged_metrics(self):
        report=run_audit()
        self.assertEqual(attest_audit(report),report)
        forged=deepcopy(report)
        forged["rows"][0]["vp_max"]=999
        forged["audit_sha256"]=canonical_digest({
            k:v for k,v in forged.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_audit(forged)

    def test_14_reject_unauthorized_rates_levels_policies_and_seed(self):
        for focus,lv in (("Low",4),("Medium",0),("High",True),
                         ("Priest",1),("low",2)):
            with self.assertRaises(ValueError):
                row(focus,lv)
        for args in (
            {"focus":"High","level":3,"policy":"guided"},
            {"focus":"Medium","level":2,"policy":"reroute"},
            {"focus":"Low","level":2,"policy":"stone_intensify"},
            {"focus":"Low","level":True,"policy":"stone"},
            {"focus":"High","level":1,"policy":"stone","seed":-1},
        ):
            with self.assertRaises(ValueError):
                matched_soldier(**args)
        with self.assertRaises(ValueError):
            run_audit(seed=True)

    def test_15_source_digest_matches_actual_native_actor(self):
        for focus in FOCUSES:
            for lv in LEVELS:
                a=party_actor(ROLES[focus],lv,"scholar","party",
                              occupied=((2,2),))
                self.assertEqual(row(focus,lv)["actor_source_sha256"],
                                 a.source.digest)

    def test_16_report_claims_no_three_focus_win_rate_or_tuning(self):
        r=run_audit()
        self.assertTrue(all(not x["full_focus_certified"]
                            for x in r["rows"]))
        self.assertTrue(all(not x["full_focus_certified"]
                            for x in r["native_matched"]))
        self.assertTrue(all(x["win_rate"] is None
                            for x in r["native_matched"]))
        self.assertTrue(all(not x["full_focus_certified"]
                            for x in r["prior_native_separate_cohorts"]))


if __name__=="__main__":
    main()
