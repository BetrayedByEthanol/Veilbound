"""Medium Anointed source budget, Invested recipient and negative-path checks."""
from dataclasses import replace
from pathlib import Path
import unittest

from scripts.b05_medium_anointed_restoration_l1_l3_v0 import (
    ABILITIES, BOND, LEVELS, MISSION, IMPRINT, profile, isolated_witness, verify,
)
from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, guided_regeneration_l3, invest, mission_event,
    returning_step, set_bond, kindled_flame,
)

ROOT = Path(__file__).resolve().parents[1]


class MediumAnointedL1L3Verification(unittest.TestCase):
    def test_01_one_bond_point_buy_training_equipment(self):
        self.assertTrue(verify())
        for lv in LEVELS:
            s = profile(lv)
            self.assertEqual(28, s["ability_points"])
            self.assertEqual((52,98), (s["starting_spent_sp"],s["silver_remaining_sp"]))
            self.assertEqual(8+int(lv>=2), s["learned_points"])
            self.assertEqual(2, s["weapon_development_points"])
            self.assertEqual((BOND,MISSION,IMPRINT), (s["bond"],s["mission"],s["birth_imprint"]))
            self.assertEqual(["Basic Heal", "Guided Regeneration"],s["known_bonded_techniques"])
            self.assertEqual([],s["known_other_aspect_techniques"])
            self.assertFalse(s["independent_full_focus_certified"])

    def test_02_medium_focus_progression_and_talent_schedule(self):
        for lv in LEVELS:
            s=profile(lv)
            self.assertEqual((12,12*lv,4*lv),(s["hp_max"],s["vigor_max"],s["vp_max"]))
            self.assertEqual(30+6*(lv-1),s["turn_ap"])
            self.assertEqual((24,24,24),(s["physical_action_ap"],s["projection_action_ap"],s["general_action_ap"]))
            self.assertEqual((1,1,1),(s["physical_tempo"],s["projection_tempo"],s["guard_capacity"]))
            self.assertEqual(1 if lv<3 else 2,len(s["talents"]))
            self.assertEqual(["TAL-A01 Imprint Recall"]+(["TAL-U03 Field Diagnosis"] if lv==3 else []),s["talents"])
            self.assertEqual(4,s["medicine_check_bonus"])
            self.assertEqual(4,s["normal_regen_throughput"])
            self.assertFalse(s["one_investment_plus_projection_same_turn"])
            self.assertFalse(s["two_projection_actions_same_turn"])
            self.assertEqual(3,s["signature_max_range_squares"])
            self.assertEqual(lv==3,s["l3_guided_single_target_vessel_lesser_eligible"])
            self.assertEqual(lv==3,s["blink_affordable_from_full_vp"])
        for illegal in (0,4,True,1.5):
            with self.subTest(illegal=illegal), self.assertRaises(ValueError):
                profile(illegal)

    def test_03_invest_setup_consent_one_vessel_and_no_free_turn(self):
        a=Anointed(1,"Medium","Restoration")
        for overrides in (
            {"ap_available":23},{"legal_vessel":False},
            {"consent_or_other_delivery_valid":False}, {"vessel_id":""},
        ):
            args={"vessel_id":"patient","ap_available":30,"legal_vessel":True,
                  "consent_or_other_delivery_valid":True}|overrides
            with self.subTest(overrides=overrides),self.assertRaises(ValueError):
                invest(a,**args)
        placed,ap=invest(a,"patient",ap_available=30,legal_vessel=True,
                         consent_or_other_delivery_valid=True)
        self.assertEqual((24,"patient"),(ap,placed.invested_vessel))
        moved,_=invest(placed,"other",ap_available=24,legal_vessel=True,
                       consent_or_other_delivery_valid=True)
        self.assertEqual("other",moved.invested_vessel)
        self.assertNotEqual("patient",moved.invested_vessel)
        self.assertIsNone(set_bond(moved,active=False).invested_vessel)

    def test_04_exact_patient_step_cadence_and_range(self):
        a,_=invest(Anointed(2,"Medium","Restoration"),"patient",
                   ap_available=36,legal_vessel=True,
                   consent_or_other_delivery_valid=True)
        args=dict(target_id="patient",recipient_hp=6,recipient_max_hp=12,
                  recipient_vigor=2,authenticated_regeneration_step=True,
                  focus_turn_id="patient:step1",distance=3)
        x=returning_step(a,receipt="pulse1",**args)
        self.assertEqual((1,1,0),(x.hp_restored,x.recipient_vigor_spent,x.ap_spent))
        for change in ({"target_id":"other"},{"authenticated_regeneration_step":False},
                       {"focus_turn_id":None},{"distance":4},{"path_visible":False},
                       {"recipient_hp":0},{"recipient_living":False}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                returning_step(a,receipt="illegal",**(args|change))
        with self.assertRaises(ValueError):
            returning_step(x.actor,receipt="second-on-same-step",**args)
        newstep=returning_step(x.actor,receipt="pulse2",**(args|{"focus_turn_id":"patient:step2"}))
        self.assertEqual(1,newstep.hp_restored)
        moved,_=invest(a,"other",ap_available=24,legal_vessel=True,
                       consent_or_other_delivery_valid=True)
        with self.assertRaises(ValueError):
            returning_step(moved,receipt="former",**args)

    def test_05_spare_reserve_no_vigor_and_resistance(self):
        a,_=invest(Anointed(1,"Medium","Restoration"),"patient",
                   ap_available=30,legal_vessel=True,
                   consent_or_other_delivery_valid=True)
        args=dict(target_id="patient",recipient_hp=5,recipient_max_hp=12,
                  recipient_vigor=0,authenticated_regeneration_step=True,
                  focus_turn_id="patient:step1")
        with self.assertRaises(ValueError):
            returning_step(a,receipt="no-vigor",**args)
        x=returning_step(a,receipt="free-one",lesser=True,**args)
        self.assertEqual((1,0,1),(x.hp_restored,x.recipient_vigor_spent,x.actor.destiny))
        with self.assertRaises(ValueError):
            returning_step(x.actor,receipt="same-step",lesser=True,**args)
        resisted=returning_step(a,receipt="refusal",lesser=True,
                     intrusion_succeeded=False,**args)
        self.assertEqual((0,1),(resisted.hp_restored,resisted.actor.destiny))
        for change in ({"recipient_hp":12},{"beneficial_intrusion_legal":False}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                returning_step(a,receipt="prelegal",lesser=True,**(args|change))
        self.assertEqual(a,mission_event(a,"routine",gm_recognized=False))

    def test_06_level3_guided_vessel_and_no_unapproved_authority(self):
        legal=dict(receipt="genuine-step",recipient_missing_hp_after_ordinary=2,
                   active_paid_guided_instance=True,mode="Maintained",
                   profile="Single Target",authenticated_regeneration_step=True,
                   guided_bonus_unsuppressed=True,vessel_matches=True)
        a,_=invest(Anointed(3,"Medium","Restoration"),"patient",
                   ap_available=42,legal_vessel=True,
                   consent_or_other_delivery_valid=True)
        x=guided_regeneration_l3(a,**legal)
        self.assertEqual((1,1),(x.additional_hp_without_vigor,x.actor.destiny))
        for change in ({"recipient_missing_hp_after_ordinary":0},
                       {"active_paid_guided_instance":False},
                       {"profile":"Self"},{"authenticated_regeneration_step":False},
                       {"guided_bonus_unsuppressed":False},
                       {"vessel_matches":False},{"recipient_dying":True}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                guided_regeneration_l3(a,**(legal|change))
        with self.assertRaises(ValueError):
            guided_regeneration_l3(Anointed(3,"Medium","Restoration"),**legal)
        with self.assertRaises(ValueError):
            guided_regeneration_l3(Anointed(2,"Medium","Restoration",invested_vessel="patient"),**legal)
        with self.assertRaises(ValueError):
            guided_regeneration_l3(x.actor,**legal)
        with self.assertRaises(ValueError):
            kindled_flame(a,receipt="illegal-fire",hit=True,target_vigor=7,target_hp=9,
                          carrier_attack_authentic=True,carrier_attack_on_own_turn=True,
                          invested_weapon_id="sword",active_wielded_weapon_id="sword",turn_id="R1")

    def test_07_native_limit_and_roadmap(self):
        for lv in LEVELS:
            w=isolated_witness(lv)
            self.assertFalse(w["native_attestation"])
            self.assertEqual((24,0,1,1,1,0,1),
                 (w["investment_ap"],w["signature_activation_ap"],w["normal_hp"],
                  w["normal_recipient_vigor_spent"],w["lesser_hp"],
                  w["lesser_recipient_vigor_spent"],w["lesser_destiny_remaining"]))
            self.assertEqual(lv==3,w["l3_guided"] is not None)
        doc=(ROOT/"docs/design/b04-b05-medium-anointed-restoration-l1-l3-character-build-verification-v0.md").read_text(encoding="utf-8")
        roadmap=(ROOT/"docs/design/veilbound-roadmap-and-mvp-readiness.md").read_text(encoding="utf-8")
        for phrase in ("28-point","24 AP","TAL-U03","one Vessel","0/12","0/6","Guided Regeneration"):
            self.assertIn(phrase,doc)
        self.assertIn("**11/12**",roadmap)
        self.assertIn("**0/12**",roadmap)
        self.assertIn("**0/6**",roadmap)
        self.assertIn("Low Anointed",roadmap)


if __name__ == "__main__":
    unittest.main()
