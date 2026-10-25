"""L1–3 three Scholar Focuses: source-checked Thrown Flame and Soldier retaliation."""
from copy import deepcopy
from dataclasses import replace
import json
import unittest

from scripts.b05_scholar_thrown_flame_access_v0 import flame_access
from scripts.b05_scholar_three_focus_native_offense_v0 import (
    run_case,attest_case,run_matrix,FOCUSES,LEVELS,
)
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def fixture(focus,level=3):
    a=party_actor(FOCUSES[focus],level,"scholar","party",
                  occupied=((2,2),))
    foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((4,2),))
    e=Encounter([a,foe],{"scholar":40,"foe":30},seed=0)
    GridMovement(e,width=8,height=7)
    RangedCombat(e)
    g3=SpellState(e)
    DamageState(e)
    e.begin_round()
    e.start_turn("scholar",regen_choice=RegenerationChoice())
    return e,g3,a


class ScholarNativeOffenseTests(unittest.TestCase):
    def test_01_real_source_identity_and_access_3x3(self):
        for level in LEVELS:
            for focus in FOCUSES:
                with self.subTest(focus=focus,level=level):
                    a=party_actor(FOCUSES[focus],level,"scholar","party",
                                  occupied=((2,2),))
                    if focus=="Low" and level==1:
                        with self.assertRaises(UnresolvedDecision):
                            flame_access(a)
                        continue
                    p=flame_access(a)
                    self.assertEqual(p["focus"],focus)
                    self.assertEqual(p["action_ap"],
                        {"High":20,"Medium":24,"Low":30}[focus])
                    self.assertEqual(p["attack_bonus"],5 if focus=="High" else 3)
                    self.assertEqual(p["throwing"],2 if focus=="High" else 0)
                    self.assertEqual(p["source_digest"],a.source.digest)
                    self.assertEqual(p["max_tier"],1 if level<3 else 2)

    def test_02_all_source_profiles_one_real_t1_hit_and_native_g4(self):
        for focus in FOCUSES:
            for level in LEVELS:
                with self.subTest(focus=focus,level=level):
                    r=run_case(focus=focus,level=level,policy="flame_t1")
                    m=r["metrics"]
                    self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))
                    if focus=="Low" and level==1:
                        self.assertFalse(m["legal_flame_cast"])
                        self.assertTrue(m["blocked_unprepared_flame"])
                        self.assertEqual(m["flame_launches"],0)
                        self.assertEqual(m["flame_vp_spent"],0)
                    else:
                        self.assertTrue(m["legal_flame_cast"])
                        self.assertEqual((m["flame_launches"],
                                          m["flame_g4_receipts"]),(1,1))
                        self.assertEqual(m["flame_vp_spent"],2)
                        self.assertEqual(m["flame_ap_paid"],
                                         {"High":20,"Medium":24,"Low":30}[focus])
                        self.assertEqual(m["flame_source_bonus"],
                                         5 if focus=="High" else 3)
                        hits=[x for x in r["ledger"]
                              if x["kind"]=="g4_damage_applied"
                              and x["detail"]["cause"]=="g3:thrown_flame"]
                        self.assertEqual(len(hits),1)
                        self.assertEqual(hits[0]["detail"]["recipient"],"foe")
                    self.assertEqual(m["soldier_sword_hits"],2)
                    self.assertEqual(m["scholar_true_steps"],2)
                    self.assertFalse(r["general_melee_attack_authorized_for_S_T"])
                    self.assertFalse(r["full_focus_certified"])

    def test_03_t2_at_l3_costs_four_vp_without_second_free_attack(self):
        for focus in FOCUSES:
            with self.subTest(focus=focus):
                r=run_case(focus=focus,level=3,policy="flame_t2")
                m=r["metrics"]
                self.assertEqual(m["flame_launches"],1)
                self.assertEqual(m["flame_g4_receipts"],1)
                self.assertEqual(m["flame_vp_spent"],4)
                self.assertEqual(m["flame_ap_paid"],
                                 {"High":20,"Medium":24,"Low":30}[focus])
                self.assertEqual(m["scholar_vp"][2],4)

    def test_04_baselines_have_no_free_player_damage(self):
        for focus in FOCUSES:
            for level in LEVELS:
                with self.subTest(focus=focus,level=level):
                    r=run_case(focus=focus,level=level,policy="no_spell")
                    m=r["metrics"]
                    self.assertEqual((m["flame_launches"],m["flame_g4_receipts"],
                                      m["flame_vp_spent"],m["flame_ap_paid"]),
                                     (0,0,0,0))
                    self.assertEqual(m["foe_hp_final"],12)
                    self.assertEqual(m["soldier_sword_hits"],2)
                    self.assertEqual(m["scholar_true_steps"],2)

    def test_05_threatened_second_round_cast_never_gets_free_opportunity(self):
        e,g,a=fixture("Medium",2)
        # Actual G1 movement by a foe from 2 squares away into adjacent
        # contact is done here without inventing enemy attack evidence.
        e.end_turn()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        e.g1.step("foe",(-1,0),responses=())
        e.end_turn()
        e.begin_round()
        e.start_turn("scholar",regen_choice=RegenerationChoice())
        before=(a.ap_remaining,a.vp_available,a.vp_spent)
        with self.assertRaisesRegex(UnresolvedDecision,"Threatened Scholar casting"):
            g.cast_flame("scholar","foe",tier=1,face=12,
                          vigor_die=3,hand_available=True)
        self.assertEqual((a.ap_remaining,a.vp_available,a.vp_spent),before)

    def test_06_unprepared_low_l1_preflight_never_pays_AP_VP(self):
        e,g,a=fixture("Low",1)
        before=(a.ap_remaining,a.vp_available,a.vp_spent,len(e.ledger))
        with self.assertRaises(UnresolvedDecision):
            e.g2.preview_thrown_flame("scholar","foe")
        with self.assertRaises(UnresolvedDecision):
            g.cast_flame("scholar","foe",tier=1,face=12,
                         vigor_die=3,hand_available=True)
        self.assertEqual(before,(a.ap_remaining,a.vp_available,
                                 a.vp_spent,len(e.ledger)))

    def test_07_hand_eligibility_and_current_wielded_item_preflight(self):
        for focus in FOCUSES:
            e,g,a=fixture(focus,2)
            before=(a.ap_remaining,a.vp_available,a.vp_spent,len(e.ledger))
            with self.assertRaisesRegex(ValueError,"functioning hand"):
                g.cast_flame("scholar","foe",tier=1,face=12,
                             vigor_die=3,hand_available=False)
            self.assertEqual(before,(a.ap_remaining,a.vp_available,
                                     a.vp_spent,len(e.ledger)))
            e.g2.wielded["scholar"].add("Shield")
            with self.assertRaises(UnresolvedDecision):
                g.cast_flame("scholar","foe",tier=1,face=12,
                             vigor_die=3,hand_available=True)
            self.assertEqual(before,(a.ap_remaining,a.vp_available,
                                     a.vp_spent,len(e.ledger)))

    def test_08_source_forgery_cannot_gain_flame_access(self):
        for focus in FOCUSES:
            a=party_actor(FOCUSES[focus],3,"scholar","party",
                          occupied=((2,2),))
            original=a.source
            for fake in (replace(original,digest="0"*64),
                         replace(original,status="EXECUTABLE_TEST_FIXTURE"),
                         replace(original,attack_profiles=("fake",)),
                         replace(original,training=(("Throwing",10),)),
                         replace(original,equipment=(("Sword","wielded"),))):
                a.source=fake
                with self.assertRaises(UnresolvedDecision):
                    flame_access(a)
            a.source=original
            self.assertEqual(flame_access(a)["role"],FOCUSES[focus])

    def test_09_known_vs_prepared_and_wrong_used_tier(self):
        for focus in FOCUSES:
            e,g,a=fixture(focus,2)
            before=(a.ap_remaining,a.vp_available,len(e.ledger))
            with self.assertRaises(ValueError):
                g.cast_flame("scholar","foe",tier=2,face=12,
                             vigor_die=3,hand_available=True)
            self.assertEqual(before,(a.ap_remaining,a.vp_available,len(e.ledger)))
            with self.assertRaises(ValueError):
                g.cast_flame("scholar","foe",tier=True,face=12,
                             vigor_die=3,hand_available=True)

    def test_10_only_native_S_T_sword_cut_no_extra_profiles(self):
        for focus,ident in (("Medium","B05-PC-S-SWORD-CUT"),
                            ("Low","B05-PC-T-SWORD-CUT")):
            a=party_actor(FOCUSES[focus],3,"scholar","party",
                          occupied=((2,2),))
            self.assertEqual(a.source.attack_profiles,(ident,))
            self.assertEqual(dict(a.source.equipment)["Sword"],"wielded")
            self.assertEqual(dict(a.source.training)["One-Handed Swords"],2)

    def test_11_matrix_counts_and_honest_low_L1_blocker(self):
        r=run_matrix()
        self.assertEqual(r["count"],21)
        self.assertEqual(len(r["cells"]),21)
        self.assertEqual(r["legal_cast_cells"],11)
        self.assertEqual(r["l1_low_unprepared_blocked"],1)
        self.assertEqual(r["audit_sha256"],canonical_digest(
            {k:v for k,v in r.items() if k!="audit_sha256"}))
        self.assertFalse(r["full_focus_certified"])
        self.assertFalse(r["numerical_tuning_authorized"])

    def test_12_native_report_forgery_rejected_after_rehash(self):
        arguments={"focus":"Medium","level":2,"policy":"flame_t1","seed":0}
        original=run_case(**arguments)
        self.assertEqual(attest_case(original,**arguments),original)
        forged=deepcopy(original)
        forged["metrics"]["flame_vp_spent"]=0
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_case(forged,**arguments)
        forged=deepcopy(original)
        forged["ledger"][0]["kind"]="fake"
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_case(forged,**arguments)

    def test_13_reject_bad_roles_policies_levels_and_seeds(self):
        for args in (
            {"focus":"Priest","level":2,"policy":"flame_t1"},
            {"focus":"Low","level":True,"policy":"flame_t1"},
            {"focus":"Low","level":4,"policy":"flame_t1"},
            {"focus":"High","level":1,"policy":"flame_t2"},
            {"focus":"Medium","level":2,"policy":"flame_t2"},
            {"focus":"High","level":2,"policy":"invalid"},
            {"focus":"High","level":2,"policy":"flame_t1","seed":-1},
        ):
            with self.assertRaises(ValueError):
                run_case(**args)
        with self.assertRaises(ValueError):
            run_matrix(seed=True)

    def test_14_json_roundtrip_canonical_case_and_matrix(self):
        case=run_case(focus="High",level=2,policy="flame_t1")
        self.assertEqual(json.loads(json.dumps(case)),case)
        self.assertEqual(attest_case(json.loads(json.dumps(case)),
                                     focus="High",level=2,policy="flame_t1"),case)
        matrix=run_matrix()
        self.assertEqual(json.loads(json.dumps(matrix)),matrix)

    def test_15_executable_evidence_distinguishes_damage_and_enemy_recovery(self):
        r=run_case(focus="Low",level=2,policy="flame_t1")
        launched=[x for x in r["ledger"] if x["kind"]=="g3_flame_launched"]
        native=[x for x in r["ledger"] if x["kind"]=="g4_damage_applied"
                and x["detail"]["cause"]=="g3:thrown_flame"]
        self.assertEqual((len(launched),len(native)),(1,1))
        self.assertEqual(launched[0]["detail"]["source_id"],"T")
        self.assertEqual(launched[0]["detail"]["source_attack_bonus"],3)
        self.assertEqual(launched[0]["detail"]["projection_ap"],30)
        self.assertGreater(native[0]["detail"]["hp_before"],
                           native[0]["detail"]["hp_after"])
        self.assertEqual(r["metrics"]["foe_hp_final"],10)


if __name__=="__main__":
    unittest.main()
