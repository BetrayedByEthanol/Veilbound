"""Real 4-round Scholar tactical/VP/Guard/cover/Step2 acceptance witnesses."""
from copy import deepcopy
import json
import unittest

from scripts.b05_scholar_three_focus_tactical_attrition_v0 import (
    ROLES,LEVELS,POLICIES,COMMON_POLICIES,PHYSICAL_POLICIES,
    ROUNDS,SOURCE_BASIS,run_case,run_matrix,attest_case,attest_matrix,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def events(case,kind,*,actor=None):
    return [x for x in case["ledger"] if x["kind"]==kind and
            (actor is None or x["detail"].get("actor")==actor)]


class ScholarTacticalAttritionV0Tests(unittest.TestCase):
    def test_01_complete_48_native_four_round_source_matrix(self):
        rows=run_matrix()
        self.assertEqual(rows["case_count"],48)
        self.assertEqual(len(rows["cases"]),48)
        self.assertEqual(len({
            (c["focus"],c["level"],c["policy"]) for c in rows["cases"]}),48)
        self.assertEqual(set(rows["source_basis"]),set(SOURCE_BASIS))
        self.assertEqual(rows["audit_sha256"],canonical_digest({
            k:v for k,v in rows.items() if k!="audit_sha256"}))
        self.assertFalse(rows["full_focus_certified"])
        self.assertIsNone(rows["statistical_win_rate"])

    def test_02_each_common_focus_level_has_real_four_round_turns(self):
        for focus in ROLES:
            for level in LEVELS:
                for policy in COMMON_POLICIES:
                    with self.subTest(focus=focus,level=level,policy=policy):
                        r=run_case(focus=focus,level=level,policy=policy)
                        m=r["metrics"]
                        self.assertEqual(m["native_soldier_attacks"],ROUNDS)
                        self.assertEqual(m["regen_steps"],ROUNDS)
                        self.assertEqual(len(events(r,"round_end")),ROUNDS)
                        self.assertEqual(len(events(r,"turn_end")),2*ROUNDS)
                        self.assertEqual(len(events(r,"regeneration_step")),2*ROUNDS)
                        self.assertEqual(m["native_sword_hits"],
                                         0 if focus=="High" else 2)
                        self.assertFalse(m["scholar_dead"])
                        self.assertFalse(m["foe_dead"])
                        self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))
                        self.assertEqual(r["audit_sha256"],canonical_digest({
                            k:v for k,v in r.items() if k!="audit_sha256"}))

    def test_03_high_fire_pressure_native_launch_vp_g4_and_range(self):
        for level in LEVELS:
            r=run_case(focus="High",level=level,policy="pressure")
            m=r["metrics"]
            self.assertEqual(m["native_flame_launches"],1)
            self.assertEqual(m["native_flame_g4"],1)
            self.assertEqual(m["flame_cover_impacts"],0)
            self.assertEqual(m["source_ap_projection"],20)
            self.assertEqual(m["source_ap_physical"],0)
            self.assertEqual(m["source_vp_spent"],2)
            self.assertEqual(m["foe_hp"],10)
            self.assertEqual(m["native_soldier_hits"],4)
            self.assertEqual(m["native_soldier_g4"],4)
            launched=events(r,"g3_flame_launched")
            self.assertEqual(launched[0]["detail"]["source_attack_bonus"],5)
            self.assertEqual(launched[0]["detail"]["attack_total"],17)

    def test_04_source_cover_eight_changes_only_legal_flame_outcome(self):
        for level in LEVELS:
            r=run_case(focus="High",level=level,policy="cover")
            m=r["metrics"]
            self.assertEqual(m["native_flame_launches"],1)
            self.assertEqual(m["flame_cover_impacts"],1)
            self.assertEqual(m["native_flame_g4"],0)
            self.assertEqual(m["source_vp_spent"],2)
            self.assertEqual(m["foe_hp"],12)
            self.assertEqual(r["inputs"]["cover_tier"],8)
            lane=events(r,"g2_flame_lane_preview")
            self.assertTrue(lane)
            self.assertEqual(lane[0]["detail"]["obstruction"],8)
            self.assertEqual(events(r,"g3_flame_launched")[0]["detail"]["outcome"],
                             "cover_impact")

    def test_05_sword_approach_and_unchanged_cut_armor_penetration(self):
        for focus in ("Medium","Low"):
            for level in LEVELS:
                r=run_case(focus=focus,level=level,policy="cover")
                m=r["metrics"]
                self.assertEqual(m["native_sword_attacks"],2)
                self.assertEqual(m["native_sword_g4"],2)
                self.assertEqual(m["foe_hp"],2)
                self.assertEqual(m["native_flame_launches"],0)
                self.assertEqual(m["source_ap_physical"],
                                 2*(24 if focus=="Medium" else 20))
                self.assertEqual(m["final_scholar_position"],[[3,2]])
                step=events(r,"g1_movement_step")
                self.assertEqual(
                    len([v for v in step if v["detail"].get("actor")=="scholar"]),1)
                self.assertEqual(
                    [v["detail"]["cost"] for v in step
                     if v["detail"].get("actor")=="scholar"],[1])
                source_damage=[v for v in events(r,"g4_damage_applied")
                               if v["detail"]["recipient"]=="foe"]
                self.assertEqual(len(source_damage),2)
                self.assertEqual(source_damage[0]["detail"]["packets"][0]["type"],
                                 "Cut")
                self.assertEqual(source_damage[0]["detail"]["packets"][0]["raw"],8)
                self.assertEqual(source_damage[0]["detail"]["packets"][0]["mitigated"],5)

    def test_06_same_input_soldier_dodge_vs_take_hit_is_actual_native_choice(self):
        for focus in ROLES:
            r=run_case(focus=focus,level=2,policy="dodge")
            base=run_case(focus=focus,level=2,policy="pressure")
            m=r["metrics"]
            self.assertEqual(m["native_soldier_hits"],0)
            self.assertEqual(m["native_soldier_g4"],0)
            self.assertEqual(base["metrics"]["native_soldier_hits"],4)
            self.assertEqual(m["scholar_hp"],12)
            self.assertEqual(m["hp_restored"],0)
            assigned=[v for v in events(r,"defense_assigned")
                      if v["detail"]["actor"]=="scholar"]
            self.assertEqual([x["detail"]["defense"] for x in assigned],
                             ["dodge"]*4)
            self.assertTrue(all(x["detail"]["defense_value"]==14
                                for x in assigned))

    def test_07_sword_guard_is_available_only_to_medium_low(self):
        for focus in ("Medium","Low"):
            for level in LEVELS:
                r=run_case(focus=focus,level=level,policy="guard")
                m=r["metrics"]
                self.assertEqual(m["native_soldier_hits"],0)
                self.assertEqual(m["native_soldier_g4"],0)
                self.assertEqual(m["scholar_hp"],12)
                assigned=[x for x in events(r,"defense_assigned")
                          if x["detail"]["actor"]=="scholar"]
                self.assertEqual([a["detail"]["defense"] for a in assigned],
                                 ["guard"]*4)
                self.assertTrue(all(a["detail"]["defense_value"]==17
                                    for a in assigned))
        for lv in LEVELS:
            with self.assertRaises(ValueError):
                run_case(focus="High",level=lv,policy="guard")

    def test_08_genuine_stone_commitment_protects_four_real_soldier_hits(self):
        for focus in ROLES:
            for level in LEVELS:
                exposed=run_case(focus=focus,level=level,policy="pressure")
                r=run_case(focus=focus,level=level,policy="stone")
                m=r["metrics"]
                self.assertEqual(m["native_soldier_hits"],4)
                self.assertEqual(m["effect_receipts"],1)
                self.assertGreater(m["effect_source_committed"],0)
                self.assertEqual(m["source_vp_spent"],0)
                self.assertGreater(m["source_vp_state"][1],0)
                self.assertEqual(m["source_ap_projection"],
                                 {"High":20,"Medium":24,"Low":30}[focus])
                self.assertGreaterEqual(m["scholar_hp"],
                                        exposed["metrics"]["scholar_hp"])
                self.assertEqual(m["native_sword_hits"],
                                 0 if focus=="High" else 2)
                self.assertTrue(any(v["detail"]["effect_kind"]=="Stone Skin"
                                    for v in events(r,"g3_effect_established")))

    def test_09_guided_medium_low_uses_only_real_step_two(self):
        for focus in ("Medium","Low"):
            for level in LEVELS:
                r=run_case(focus=focus,level=level,policy="guided")
                m=r["metrics"]
                self.assertEqual(m["effect_receipts"],1)
                self.assertEqual(m["native_sword_hits"],2)
                self.assertEqual(m["regen_steps"],4)
                self.assertGreaterEqual(m["hp_restored"],4)
                self.assertLess(m["scholar_vigor"],12*level)
                self.assertEqual(m["source_ap_projection"],
                                 24 if focus=="Medium" else 30)
                self.assertEqual(m["source_ap_physical"],
                                 48 if focus=="Medium" else 40)
                self.assertEqual(m["source_vp_spent"],0)
                self.assertGreater(m["source_vp_state"][1],0)
        for lv in LEVELS:
            with self.assertRaises(ValueError):
                run_case(focus="High",level=lv,policy="guided")

    def test_10_no_free_second_cast_while_threatened_or_unprepared(self):
        for focus in ROLES:
            for level in LEVELS:
                for policy in COMMON_POLICIES:
                    r=run_case(focus=focus,level=level,policy=policy)
                    refused=events(r,"b05_scholar_tactical_cast_rejected")
                    self.assertEqual(len(refused),1)
                    self.assertTrue(refused[0]["detail"]["ap_vp_unchanged"])
                    reason=refused[0]["detail"]["reason"]
                    self.assertTrue(reason)
                    if focus=="Low" and level==1:
                        self.assertIn("Prepared Arsenal",reason)
                    else:
                        self.assertIn("Threatened",reason)

    def test_11_attributed_hp_damage_only_once_per_native_paid_g5(self):
        r=run_case(focus="Low",level=3,policy="pressure")
        hits=[x for x in events(r,"g45_attested_hit")
              if x["detail"]["attacker"]=="scholar"]
        damages=[x for x in events(r,"g4_damage_applied")
                 if x["detail"]["recipient"]=="foe"]
        self.assertEqual(len(hits),2)
        self.assertEqual(len(damages),2)
        self.assertEqual(len(set(x["detail"]["action_index"] for x in hits)),2)
        self.assertEqual(r["metrics"]["foe_hp"],2)

    def test_12_vp_spent_commit_and_available_conserve_exact_source_totals(self):
        for focus in ROLES:
            for level in LEVELS:
                for policy in COMMON_POLICIES:
                    r=run_case(focus=focus,level=level,policy=policy)
                    state=r["metrics"]["source_vp_state"]
                    max_vp={"High":6,"Medium":4,"Low":2}[focus]*level
                    self.assertEqual(sum(state),max_vp)
                    self.assertEqual(state[2],r["metrics"]["source_vp_spent"])
                    self.assertEqual(r["metrics"]["effect_receipts"],
                                     1 if policy=="stone" else 0)

    def test_13_vigor_consumes_recovery_budget_not_free_hp(self):
        for focus in ROLES:
            for lv in LEVELS:
                base=run_case(focus=focus,level=lv,policy="pressure")
                guarded=(run_case(focus=focus,level=lv,
                                  policy="dodge"))
                self.assertGreater(base["metrics"]["hp_restored"],0)
                self.assertLess(base["metrics"]["scholar_vigor"],
                                guarded["metrics"]["scholar_vigor"])
                self.assertEqual(guarded["metrics"]["hp_restored"],0)
                self.assertEqual(guarded["metrics"]["scholar_vigor"],12*lv)

    def test_14_reattest_saved_native_case_and_detect_tamper_even_rehashed(self):
        kwargs={"focus":"Medium","level":2,"policy":"stone","seed":8}
        original=run_case(**kwargs)
        loaded=json.loads(json.dumps(original,sort_keys=True,allow_nan=False))
        self.assertEqual(loaded,original)
        self.assertEqual(attest_case(loaded,**kwargs),original)
        forged=deepcopy(original)
        forged["metrics"]["native_soldier_hits"]=0
        forged["audit_sha256"]=canonical_digest({
            k:v for k,v in forged.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_case(forged,**kwargs)
        forged=deepcopy(original)
        forged["ledger"][0]["kind"]="faked_action"
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        forged["audit_sha256"]=canonical_digest({
            k:v for k,v in forged.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_case(forged,**kwargs)

    def test_15_matrix_json_roundtrip_source_replay_and_rehash_detection(self):
        original=run_matrix(seed=0)
        loaded=json.loads(json.dumps(original))
        self.assertEqual(loaded,original)
        self.assertEqual(attest_matrix(loaded),original)
        fake=deepcopy(original)
        fake["cases"][0]["metrics"]["native_soldier_hits"]=99
        fake["audit_sha256"]=canonical_digest({
            k:v for k,v in fake.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_matrix(fake)

    def test_16_fail_closed_on_unauthorized_roles_policies_levels_and_seeds(self):
        for kwargs in (
            {"focus":"Priest","level":1,"policy":"pressure"},
            {"focus":"Low","level":True,"policy":"pressure"},
            {"focus":"Low","level":4,"policy":"stone"},
            {"focus":"High","level":1,"policy":"guided"},
            {"focus":"High","level":1,"policy":"guard"},
            {"focus":"Medium","level":2,"policy":"unknown"},
            {"focus":"Low","level":1,"policy":"pressure","seed":-1},
            {"focus":"High","level":2,"policy":"pressure","seed":True},
        ):
            with self.assertRaises(ValueError):
                run_case(**kwargs)
        with self.assertRaises(ValueError):
            run_matrix(seed=True)

    def test_17_numerical_balancing_and_terminal_claims_stay_provisional(self):
        for r in run_matrix()["cases"]:
            self.assertTrue(r["bounded_policy_only"])
            self.assertTrue(r["no_hypothetical_responses"])
            self.assertFalse(r["full_focus_certified"])
            self.assertFalse(r["numerical_tuning_authorized"])
            self.assertIsNone(r["win_rate"])
            self.assertTrue(all(len(s)==64 for s in r["basis_sha256"].values()))

    def test_18_source_spellbook_is_not_augmented_by_tactics(self):
        for focus in ROLES:
            r=run_case(focus=focus,level=1,policy="stone")
            self.assertEqual(r["metrics"]["effect_receipts"],1)
            self.assertEqual(r["metrics"]["source_vp_spent"],0)
            self.assertEqual(r["metrics"]["native_flame_launches"],0)
            if focus=="High":
                self.assertEqual(r["metrics"]["source_ap_physical"],0)


if __name__=="__main__":
    unittest.main()
