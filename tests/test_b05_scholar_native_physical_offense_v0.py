"""B04/B05 source-native S/T Sword, real AP/Guard/HP and host interactions."""
from copy import deepcopy
from dataclasses import replace
import json
import unittest

from scripts.b05_scholar_native_sword_v0 import (
    SWORD_IDS,SWORD_ITEM,scholar_sword_profile,
)
from scripts.b05_scholar_native_physical_offense_v0 import (
    FOCUSES,LEVELS,POLICIES,run_case,run_matrix,attest_case,
)
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def game(focus,level=3):
    source=party_actor(FOCUSES[focus],level,"scholar","party",
                       occupied=((2,2),))
    soldier=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    e=Encounter([source,soldier],{"scholar":40,"foe":30},
        seed=0,scenario="scholar-sword-test",policy="source")
    GridMovement(e,width=7,height=7,scene_id="source-sword")
    RangedCombat(e)
    SpellState(e)
    DamageState(e)
    combat=SourceMelee(e)
    e.begin_round()
    e.start_turn("scholar",regen_choice=RegenerationChoice())
    return e,source,soldier,combat


class ScholarNativeSwordTests(unittest.TestCase):
    def test_01_six_exact_original_sheets_and_one_source_cut_profile(self):
        for focus,role in FOCUSES.items():
            for lv in LEVELS:
                with self.subTest(focus=focus,level=lv):
                    e,a,foe,combat=game(focus,lv)
                    self.assertEqual(a.source.attack_profiles,(SWORD_IDS[role],))
                    p,bonus=scholar_sword_profile(
                        a,SWORD_IDS[role],encounter=e)
                    self.assertEqual(bonus,7)
                    self.assertEqual(p["primary_hp_packet"],SWORD_ITEM)
                    self.assertEqual(p["additional_packets"],[])
                    self.assertEqual(p["toxin_delivery"],None)
                    self.assertEqual(dict(a.source.training)["One-Handed Swords"],2)
                    self.assertEqual(a.physical_ap,24 if role=="S" else 20)
                    self.assertEqual(a.guard_value,17)
                    self.assertTrue(e.g1.melee_contact("scholar","foe"))

    def test_02_all_ordinary_baselines_pay_one_real_sword_each_round(self):
        for focus in FOCUSES:
            for level in LEVELS:
                with self.subTest(focus=focus,level=level):
                    r=run_case(focus=focus,level=level,policy="baseline")
                    m=r["metrics"]
                    self.assertEqual(m["scholar_sword_hits"],2)
                    self.assertEqual(m["scholar_sword_g4_receipts"],2)
                    self.assertEqual(m["scholar_source_attack_bonus"],7)
                    self.assertEqual(m["physical_ap_paid"],
                        2*(24 if focus=="Medium" else 20))
                    self.assertEqual(m["projection_ap_paid"],0)
                    self.assertEqual(m["soldier_sword_hits"],2)
                    self.assertEqual(m["foe_hp"],2)
                    self.assertFalse(m["foe_dead"])
                    self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))
                    self.assertFalse(r["full_focus_certified"])

    def test_03_source_physical_damage_has_real_cut_armor_penetration(self):
        r=run_case(focus="Medium",level=2,policy="baseline")
        hits=[x for x in r["ledger"] if x["kind"]=="g4_damage_applied"
              and x["detail"]["cause"]=="source-profile:B05-PC-S-SWORD-CUT"]
        self.assertEqual(len(hits),2)
        for h in hits:
            d=h["detail"]
            self.assertEqual(d["hp_before"]-d["hp_after"],5)
            self.assertEqual(d["packets"][0]["resource"],"hp")
            self.assertEqual(d["packets"][0]["type"],"Cut")
            self.assertEqual(d["packets"][0]["raw"],8)
            self.assertEqual(d["packets"][0]["mitigated"],5)
            self.assertEqual(d["vigor_before"],d["vigor_after"])
            self.assertEqual(d["wound"],None)

    def test_04_L3_low_declares_pays_and_resolves_two_ordered_slots(self):
        r=run_case(focus="Low",level=3,policy="double")
        m=r["metrics"]
        self.assertEqual(m["scholar_sword_hits"],3)
        self.assertEqual(m["scholar_sword_g4_receipts"],3)
        self.assertEqual(m["physical_ap_paid"],60)
        self.assertTrue(m["foe_hp"]<=0)
        declared=[x for x in r["ledger"]
                  if x["kind"]=="attack_sequence_committed"
                  and x["detail"]["attacker"]=="scholar"]
        self.assertEqual([len(x["detail"]["profiles"]) for x in declared],[2,1])
        paid=[x for x in r["ledger"]
              if x["kind"]=="action_committed"
              and x["detail"]["actor"]=="scholar"]
        self.assertEqual([x["detail"]["ap_spent"] for x in paid],[20,20,20])

    def test_05_medium_and_low_L1_L2_cannot_create_second_unpaid_slot(self):
        for focus in FOCUSES:
            for lv in (1,2):
                e,a,foe,g5=game(focus,lv)
                before=(a.ap_remaining,len(e.ledger),foe.guard_remaining)
                with self.assertRaisesRegex(ValueError,"Not enough AP"):
                    g5.declare("scholar","foe",
                        profiles=(SWORD_IDS[FOCUSES[focus]],)*2,
                        defenses=("take_hit",)*2)
                self.assertEqual((a.ap_remaining,len(e.ledger),
                                  foe.guard_remaining),before)
                self.assertFalse(g5.pending_attack_slots())

    def test_06_stone_and_guided_are_paid_instead_of_extra_sword(self):
        for focus in FOCUSES:
            for lv in LEVELS:
                for policy in ("stone","guided"):
                    with self.subTest(focus=focus,level=lv,policy=policy):
                        r=run_case(focus=focus,level=lv,policy=policy)
                        m=r["metrics"]
                        self.assertEqual(m["scholar_sword_hits"],1)
                        self.assertEqual(m["physical_ap_paid"],
                                         24 if focus=="Medium" else 20)
                        self.assertEqual(m["projection_ap_paid"],
                                         24 if focus=="Medium" else 30)
                        self.assertEqual(m["soldier_sword_hits"],2)
                        self.assertEqual(m["scholar_true_steps"],2)
                        self.assertGreater(m["scholar_vp"][1],0)
                        self.assertEqual(m["scholar_vp"][2],0)
                        self.assertIsNotNone(m["active_scholar_profile"])

    def test_07_live_wielding_loss_prevents_melee_and_guard(self):
        for focus in FOCUSES:
            e,a,foe,g5=game(focus)
            e.g2.wielded["scholar"].remove("Sword")
            before=(a.ap_remaining,a.guard_remaining,len(e.ledger))
            self.assertFalse(e.g1.melee_contact("scholar","foe"))
            self.assertFalse(e.g1.threatens("scholar",foe.occupied[0]))
            with self.assertRaises(UnresolvedDecision):
                scholar_sword_profile(a,SWORD_IDS[FOCUSES[focus]],encounter=e)
            with self.assertRaises(UnresolvedDecision):
                g5.declare("scholar","foe",
                    profiles=(SWORD_IDS[FOCUSES[focus]],),
                    defenses=("take_hit",))
            with self.assertRaisesRegex(ValueError,"Sword Guard"):
                e.defense("scholar","guard",attack_key="unready")
            self.assertEqual((a.ap_remaining,a.guard_remaining,len(e.ledger)),
                             before)

    def test_08_defender_guard_preflight_blocks_foe_payment_when_unwielded(self):
        e,a,foe,g5=game("Medium",2)
        e.end_turn()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        e.g2.wielded["scholar"].clear()
        before=(foe.ap_remaining,a.guard_remaining,len(e.ledger))
        with self.assertRaisesRegex(ValueError,"Insufficient legal Guard"):
            g5.declare("foe","scholar",profiles=("B06-AT-03",),
                       defenses=("guard",))
        self.assertEqual((foe.ap_remaining,a.guard_remaining,len(e.ledger)),before)
        self.assertFalse(g5.pending_attack_slots())

    def test_09_guard_loss_after_paid_declaration_blocks_ghost_guard_damage(self):
        e,a,foe,g5=game("Low",2)
        e.end_turn()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        seq=g5.declare("foe","scholar",
                       profiles=("B06-AT-03",),defenses=("guard",))
        self.assertEqual(a.guard_remaining,0)
        e.g2.wielded["scholar"].clear()
        before=(a.hp,foe.ap_remaining,len([
            x for x in e.ledger if x["kind"]=="g4_damage_applied"]))
        with self.assertRaisesRegex(UnresolvedDecision,"Changed Guard"):
            g5.resolve(seq,0,attack_face=12,damage_face=4,
                       wound_location_roll=8)
        self.assertEqual((a.hp,foe.ap_remaining,len([
            x for x in e.ledger if x["kind"]=="g4_damage_applied"])),before)
        self.assertEqual(len(g5.pending_attack_slots()),1)

    def test_10_weapon_loss_after_paid_sword_sequence_blocks_resolution(self):
        e,a,foe,g5=game("Low",3)
        seq=g5.declare("scholar","foe",profiles=(SWORD_IDS["T"],)*2,
                       defenses=("take_hit",)*2)
        self.assertEqual(a.ap_remaining,2)
        e.g2.wielded["scholar"].clear()
        hp=foe.hp
        with self.assertRaises(UnresolvedDecision):
            g5.resolve(seq,0,attack_face=12,damage_face=4,
                       wound_location_roll=8)
        self.assertEqual(foe.hp,hp)
        self.assertEqual(len(g5.pending_attack_slots()),2)

    def test_11_forged_native_source_or_wrong_profile_rejected_before_AP(self):
        for focus in FOCUSES:
            e,a,foe,g5=game(focus)
            original=a.source
            bad=[
                replace(original,digest="bad"),
                replace(original,attack_profiles=("B05-PC-F-INVALID",)),
                replace(original,training=(("One-Handed Swords",8),)),
                replace(original,equipment=(("Sword","wielded"),)),
                replace(original,status="G5_TEST_PROXY"),
            ]
            for fake in bad:
                a.source=fake
                before=(a.ap_remaining,len(e.ledger))
                with self.assertRaises(UnresolvedDecision):
                    g5.declare("scholar","foe",
                        profiles=(SWORD_IDS[FOCUSES[focus]],),
                        defenses=("take_hit",))
                self.assertEqual((a.ap_remaining,len(e.ledger)),before)
            a.source=original
            self.assertEqual(scholar_sword_profile(
                a,SWORD_IDS[FOCUSES[focus]],encounter=e)[1],7)
            with self.assertRaises(UnresolvedDecision):
                g5.declare("scholar","foe",
                    profiles=("B06-PC-A-SWORD",),defenses=("take_hit",))

    def test_12_G5_sword_miss_cannot_fabricate_G4_damage(self):
        e,a,foe,g5=game("Medium",2)
        seq=g5.declare("scholar","foe",
                       profiles=(SWORD_IDS["S"],),defenses=("dodge",))
        hp=foe.hp
        result=g5.resolve(seq,0,attack_face=1)
        self.assertEqual(result["outcome"],"miss")
        self.assertEqual(foe.hp,hp)
        self.assertFalse(any(x["kind"]=="g4_profile_hit"
                             for x in e.ledger))

    def test_13_unbound_other_roles_and_non_cut_profiles_never_authorized(self):
        for role in ("F","A","B"):
            a=party_actor(role,3,"scholar","party",occupied=((2,2),))
            with self.assertRaises(UnresolvedDecision):
                scholar_sword_profile(a,"B05-PC-S-SWORD-CUT",encounter=None)
        e,a,foe,g5=game("Medium")
        with self.assertRaises(UnresolvedDecision):
            scholar_sword_profile(a,"B05-PC-T-SWORD-CUT",encounter=e)

    def test_14_full_matrix_has_19_source_authorized_cases(self):
        report=run_matrix()
        self.assertEqual(report["count"],19)
        self.assertEqual(len(report["cases"]),19)
        self.assertEqual(len({(r["focus"],r["level"],r["policy"])
                              for r in report["cases"]}),19)
        self.assertEqual(report["audit_sha256"],canonical_digest(
            {k:v for k,v in report.items() if k!="audit_sha256"}))
        self.assertFalse(report["full_focus_certified"])
        self.assertIsNone(report["statistical_win_rate"])

    def test_15_exact_native_replay_rejects_rehashed_tampering(self):
        args={"focus":"Low","level":3,"policy":"double","seed":0}
        r=run_case(**args)
        self.assertEqual(attest_case(r,**args),r)
        forged=deepcopy(r)
        forged["metrics"]["scholar_sword_hits"]-=1
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_case(forged,**args)
        forged=deepcopy(r)
        forged["ledger"][0]["kind"]="invented_source"
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_case(forged,**args)

    def test_16_JSON_roundtrip_preserves_case_and_matrix_attestation(self):
        args={"focus":"Medium","level":1,"policy":"stone","seed":0}
        original=run_case(**args)
        reloaded=json.loads(json.dumps(original))
        self.assertEqual(reloaded,original)
        self.assertEqual(attest_case(reloaded,**args),original)
        matrix=run_matrix()
        self.assertEqual(json.loads(json.dumps(matrix)),matrix)

    def test_17_regen_is_authentic_not_a_fake_paid_extra_attack(self):
        r=run_case(focus="Low",level=2,policy="guided")
        steps=[x for x in r["ledger"] if x["kind"]=="regeneration_step"
               and x["detail"]["actor"]=="scholar"]
        actions=[x for x in r["ledger"] if x["kind"]=="action_committed"
                 and x["detail"]["actor"]=="scholar"]
        self.assertEqual(len(steps),2)
        self.assertEqual(len(actions),2)
        self.assertEqual([x["detail"]["action_class"] for x in actions],
                         ["projection","physical"])
        self.assertEqual(r["metrics"]["scholar_sword_hits"],1)

    def test_18_wrong_level_policy_or_seed_rejected(self):
        for args in (
            {"focus":"High","level":2,"policy":"baseline"},
            {"focus":"Low","level":0,"policy":"stone"},
            {"focus":"Low","level":True,"policy":"guided"},
            {"focus":"Low","level":2,"policy":"double"},
            {"focus":"Medium","level":3,"policy":"double"},
            {"focus":"Medium","level":3,"policy":"illegal"},
            {"focus":"Low","level":3,"policy":"baseline","seed":-1},
        ):
            with self.assertRaises(ValueError):
                run_case(**args)
        with self.assertRaises(ValueError):
            run_matrix(seed=True)


if __name__=="__main__":
    unittest.main()
