"""B04/B05 native Scholar mobile two-enemy evidence and G0 response limits."""
from copy import deepcopy
import json
import unittest

from scripts.b05_scholar_three_focus_mobile_multi_enemy_v0 import (
    ROLES,LEVELS,POLICIES,ROUNDS,SOLDIER_FACE,RULE_BASIS,
    run_case,run_matrix,attest_case,attest_matrix,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def ev(case,kind,*,actor=None):
    return [v for v in case["ledger"] if v["kind"]==kind
            and (actor is None or v["detail"].get("actor")==actor)]


class ScholarMobileMultiEnemyV0Tests(unittest.TestCase):
    def test_01_36_explicit_source_native_cohorts_27_complete_9_unresolved(self):
        r=run_matrix()
        self.assertEqual(r["case_count"],36)
        self.assertEqual(r["complete_cases"],27)
        self.assertEqual(r["opportunity_boundary_probes"],9)
        self.assertEqual(len({(x["focus"],x["level"],x["policy"])
                              for x in r["cases"]}),36)
        self.assertEqual(set(r["rule_basis"]),set(RULE_BASIS))
        self.assertFalse(r["full_focus_certified"])
        self.assertFalse(r["opportunity_damage_certified"])

    def test_02_complete_scenes_have_all_three_g0_turns_and_six_soldier_actions(self):
        for focus in ROLES:
            for lv in LEVELS:
                for policy in POLICIES[:-1]:
                    with self.subTest(focus=focus,level=lv,policy=policy):
                        r=run_case(focus=focus,level=lv,policy=policy)
                        m=r["metrics"]
                        self.assertTrue(r["native_complete_rounds"])
                        self.assertIsNone(r["blocker"])
                        self.assertEqual(m["rounds_finished"],ROUNDS)
                        self.assertEqual(m["scholar_step2"],ROUNDS)
                        self.assertEqual(m["soldier_attacks"],6)
                        self.assertEqual(len(ev(r,"turn_end")),9)
                        self.assertEqual(len(ev(r,"regeneration_step")),9)
                        self.assertEqual(m["g1_opportunity_committed"],0)
                        self.assertEqual(m["g1_opportunity_pending"],0)
                        self.assertEqual(r["ledger_sha256"],
                                         canonical_digest(r["ledger"]))

    def test_03_two_soldiers_each_really_attacks_source_player_by_own_g5(self):
        r=run_case(focus="Low",level=2,policy="pursuit")
        choices=[(x["round"],x["detail"]["attacker"],
                  x["detail"]["target"],x["detail"]["outcome"])
                 for x in ev(r,"g5_melee_resolved")
                 if x["detail"]["attacker"] in ("alpha","beta")]
        self.assertEqual(len(choices),6)
        self.assertEqual([x[1] for x in choices],
                         ["alpha","beta"]*3)
        self.assertEqual([x[2] for x in choices],["scholar"]*6)
        self.assertEqual([x[3] for x in choices],
                         ["miss","hit","hit","miss","miss","hit"])
        paid=[x for x in ev(r,"action_committed")
              if x["detail"].get("actor") in ("alpha","beta")]
        self.assertEqual(len(paid),6)
        self.assertEqual(len(ev(r,"g45_attested_hit")),6)

    def test_04_high_g1_repositioning_changes_native_projectile_origin(self):
        r=run_case(focus="High",level=2,policy="pursuit")
        m=r["metrics"]
        self.assertEqual(m["flame_launches"],3)
        self.assertEqual(m["flame_cover_impacts"],0)
        self.assertEqual(m["flame_direct_g4"],3)
        self.assertEqual(m["flame_target_orders"],["alpha","beta","beta"])
        self.assertEqual(m["projection_ap_paid"],60)
        self.assertEqual(m["vp"][2],6)
        self.assertEqual(m["positions"]["scholar"],[[0,3]])
        origins=[(x["detail"]["squares"],x["detail"]["obstruction"])
                 for x in ev(r,"g2_flame_lane_preview")]
        self.assertGreaterEqual(len(origins),3)
        steps=ev(r,"g1_movement_step",actor="scholar")
        self.assertEqual([x["detail"]["new"] for x in steps],
                         [[[2,3]],[[1,3]],[[0,3]]])
        self.assertTrue(all(x["detail"]["cost"]>0 for x in steps))

    def test_05_live_directional_cover_deflects_only_middle_flame(self):
        for lv in LEVELS:
            open_case=run_case(focus="High",level=lv,policy="pursuit")
            covered=run_case(focus="High",level=lv,policy="cover_shift")
            m=covered["metrics"]
            self.assertEqual(m["flame_launches"],3)
            self.assertEqual(m["flame_cover_impacts"],1)
            self.assertEqual(m["flame_direct_g4"],2)
            self.assertEqual(m["vp"][2],6)
            self.assertEqual(
                [x["detail"]["outcome"] for x in ev(covered,"g3_flame_launched")],
                ["direct_hit_pending_G4","cover_impact","direct_hit_pending_G4"])
            self.assertEqual(covered["inputs"]["cover_tier"],8)
            self.assertEqual(open_case["metrics"]["flame_direct_g4"],3)
            self.assertGreater(covered["metrics"]["remaining_enemy_hp"]["beta"],
                               open_case["metrics"]["remaining_enemy_hp"]["beta"])

    def test_06_native_S_T_swords_switch_actual_source_targets(self):
        for focus in ("Medium","Low"):
            for lv in LEVELS:
                r=run_case(focus=focus,level=lv,policy="pursuit")
                m=r["metrics"]
                self.assertEqual(m["scholar_sword_attacks"],3)
                self.assertEqual(m["enemy_target_orders"],
                                 ["alpha","beta","alpha"])
                self.assertEqual(m["flame_launches"],0)
                self.assertEqual(m["physical_ap_paid"],
                                 (24 if focus=="Medium" else 20)*3)
                self.assertEqual(m["positions"]["scholar"],[[3,2]])
                self.assertEqual(m["remaining_enemy_hp"],
                                 {"alpha":2,"beta":7})
                damage=[x for x in ev(r,"g4_damage_applied")
                        if x["detail"]["recipient"] in ("alpha","beta")]
                self.assertEqual(len(damage),3)
                self.assertTrue(all(x["detail"]["packets"][0]["type"]=="Cut"
                                    for x in damage))

    def test_07_two_enemies_reach_real_contact_without_teleport(self):
        for focus in ROLES:
            r=run_case(focus=focus,level=2,policy="pursuit")
            steps=ev(r,"g1_movement_step")
            moved={who:len([x for x in steps if x["detail"]["actor"]==who])
                   for who in ("scholar","alpha","beta")}
            self.assertGreaterEqual(moved["alpha"],0 if focus!="High" else 3)
            self.assertGreaterEqual(moved["beta"],1)
            self.assertEqual(moved["scholar"],3 if focus=="High" else 1)
            self.assertEqual(len(ev(r,"g5_melee_resolved")),
                             6 if focus=="High" else 9)

    def test_08_cover_does_not_create_fictitious_melee_sword_penalty(self):
        for focus in ("Medium","Low"):
            for lv in LEVELS:
                normal=run_case(focus=focus,level=lv,policy="pursuit")
                covered=run_case(focus=focus,level=lv,policy="cover_shift")
                self.assertEqual(normal["metrics"]["remaining_enemy_hp"],
                                 covered["metrics"]["remaining_enemy_hp"])
                self.assertEqual(normal["metrics"]["scholar_sword_attacks"],3)
                self.assertEqual(covered["metrics"]["scholar_sword_attacks"],3)
                self.assertEqual(covered["metrics"]["flame_launches"],0)

    def test_09_paid_stone_to_later_physical_or_projected_actions(self):
        for focus in ROLES:
            for lv in LEVELS:
                r=run_case(focus=focus,level=lv,policy="stone_weave")
                m=r["metrics"]
                effects=[x for x in ev(r,"g3_effect_established")
                         if x["detail"].get("caster")=="scholar"]
                self.assertEqual(len(effects),1)
                self.assertEqual(effects[0]["detail"]["effect_kind"],"Stone Skin")
                self.assertGreater(effects[0]["detail"]["committed"],0)
                self.assertGreater(m["projection_ap_paid"],0)
                if focus=="High":
                    self.assertEqual(m["flame_launches"],2)
                    self.assertEqual(m["physical_ap_paid"],0)
                else:
                    self.assertEqual(m["scholar_sword_attacks"],2)
                    self.assertEqual(m["flame_launches"],0)
                    self.assertGreater(m["physical_ap_paid"],0)
                    self.assertEqual(m["enemy_target_orders"],["alpha","beta"])
                self.assertTrue(all(x["detail"]["actor"]=="scholar"
                                    for x in ev(r,"regeneration_step",
                                                actor="scholar")))

    def test_10_actual_S_T_preparation_does_not_grant_free_new_weapon_spell(self):
        for focus in ("Medium","Low"):
            r=run_case(focus=focus,level=1,policy="stone_weave")
            self.assertEqual(r["metrics"]["flame_launches"],0)
            self.assertEqual(r["metrics"]["scholar_sword_attacks"],2)
            self.assertEqual(r["metrics"]["vp"][2],0)
            self.assertFalse(r["full_focus_certified"])

    def test_11_opportunity_two_real_G0_commits_without_fabricated_G5_damage(self):
        for focus in ROLES:
            for lv in LEVELS:
                r=run_case(focus=focus,level=lv,policy="opportunity_probe")
                m=r["metrics"]
                self.assertFalse(r["native_complete_rounds"])
                self.assertEqual(m["g1_opportunity_committed"],2)
                self.assertEqual(m["g1_opportunity_pending"],2)
                self.assertEqual(m["unresolved_g5_opportunities"],1)
                self.assertEqual(m["soldier_attacks"],0)
                self.assertEqual(m["rounds_finished"],0)
                self.assertEqual(m["scholar_step2"],1)
                self.assertEqual(m["positions"]["scholar"],[[2,3]])
                self.assertIsNotNone(r["blocker"])
                self.assertEqual(r["blocker"]["category"],"unresolved_response")
                self.assertFalse(r["completed_opportunity_damage_certified"])
                self.assertEqual(len(ev(r,"g4_damage_applied")),0)
                commits=ev(r,"spontaneous_committed")
                self.assertEqual(
                    [v["detail"]["actor"] for v in commits],
                    ["alpha","beta"])
                self.assertEqual(
                    [v["detail"]["response_kind"] for v in commits],
                    ["opportunity","opportunity"])

    def test_12_every_pending_oa_is_source_named_but_no_offturn_G5_slot(self):
        r=run_case(focus="Low",level=3,policy="opportunity_probe")
        pending=ev(r,"g1_movement_opportunity_pending")
        self.assertEqual(
            [v["detail"]["attacker"] for v in pending],["alpha","beta"])
        self.assertEqual({v["detail"]["outcome"] for v in pending},
                         {"G5_attack_unresolved"})
        self.assertEqual(len(ev(r,"g5_melee_resolved")),0)
        self.assertEqual(len(ev(r,"g45_attested_hit")),0)
        self.assertEqual(len(ev(r,"g45_unresolved_stop")),1)
        self.assertTrue(all(r["metrics"]["remaining_enemy_hp"][a]==12
                            for a in ("alpha","beta")))

    def test_13_only_declined_opportunities_in_completed_cases(self):
        for focus in ROLES:
            r=run_case(focus=focus,level=3,policy="cover_shift")
            self.assertTrue(r["native_complete_rounds"])
            self.assertEqual(len(ev(r,"spontaneous_committed")),0)
            self.assertEqual(len(ev(r,"g1_movement_opportunity_pending")),0)
            self.assertEqual(len(ev(r,"g45_unresolved_stop")),0)

    def test_14_two_enemy_hp_vigor_and_regeneration_are_native_receipts(self):
        for focus in ROLES:
            for lv in LEVELS:
                r=run_case(focus=focus,level=lv,policy="pursuit")
                self.assertEqual(len(ev(r,"regeneration_step")),9)
                m=r["metrics"]
                self.assertEqual(m["scholar_step2"],3)
                self.assertGreaterEqual(m["hp_restored"],0)
                self.assertLessEqual(m["scholar_hp"],12)
                self.assertLessEqual(m["scholar_vigor"],12*lv)
                self.assertTrue(all(h>0 for h in m["remaining_enemy_hp"].values()))

    def test_15_replay_saved_json_case_rejects_metric_and_ledger_forgery(self):
        args={"focus":"Medium","level":2,"policy":"cover_shift","seed":1}
        original=run_case(**args)
        saved=json.loads(json.dumps(original))
        self.assertEqual(saved,original)
        self.assertEqual(attest_case(saved,**args),original)
        fake=deepcopy(original)
        fake["metrics"]["remaining_enemy_hp"]["beta"]=12
        fake["audit_sha256"]=canonical_digest({
            k:v for k,v in fake.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_case(fake,**args)
        fake=deepcopy(original)
        fake["ledger"][0]["kind"]="invented"
        fake["ledger_sha256"]=canonical_digest(fake["ledger"])
        fake["audit_sha256"]=canonical_digest({
            k:v for k,v in fake.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_case(fake,**args)

    def test_16_OA_probe_cannot_be_relabelled_as_complete_even_with_rehash(self):
        args={"focus":"High","level":3,"policy":"opportunity_probe"}
        original=run_case(**args)
        self.assertEqual(attest_case(original,**args),original)
        fake=deepcopy(original)
        fake["native_complete_rounds"]=True
        fake["completed_opportunity_damage_certified"]=True
        fake["audit_sha256"]=canonical_digest({
            k:v for k,v in fake.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_case(fake,**args)

    def test_17_matrix_json_replay_rejects_rehashed_case_substitution(self):
        orig=run_matrix()
        self.assertEqual(json.loads(json.dumps(orig)),orig)
        self.assertEqual(attest_matrix(json.loads(json.dumps(orig))),orig)
        fake=deepcopy(orig)
        fake["cases"][0]["policy"]="opportunity_probe"
        fake["audit_sha256"]=canonical_digest({
            k:v for k,v in fake.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_matrix(fake)

    def test_18_invalid_level_focus_seed_and_policy_fail_before_any_fixture(self):
        for args in (
            {"focus":"Priest","level":1,"policy":"pursuit"},
            {"focus":"High","level":True,"policy":"pursuit"},
            {"focus":"Low","level":4,"policy":"stone_weave"},
            {"focus":"Medium","level":0,"policy":"cover_shift"},
            {"focus":"Low","level":2,"policy":"invalid"},
            {"focus":"Low","level":2,"policy":"pursuit","seed":-1},
            {"focus":"High","level":3,"policy":"pursuit","seed":True},
        ):
            with self.assertRaises(ValueError):
                run_case(**args)
        with self.assertRaises(ValueError):
            run_matrix(seed=True)


if __name__=="__main__":
    unittest.main()
