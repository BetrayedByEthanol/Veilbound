"""B04/B05 Low Anointed Restoration level, Embodiment and Authority regressions."""
from pathlib import Path
import unittest

from scripts.b05_low_anointed_restoration_l1_l3_v0 import (
    ABILITIES, BOND, LEVELS, MISSION, IMPRINT, profile, isolated_witness, verify,
)
from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, guided_regeneration_l3, invest, kindled_flame,
    mission_event, returning_step, set_bond, set_embodiment,
)

ROOT = Path(__file__).resolve().parents[1]


class LowAnointedRestorationL1L3Tests(unittest.TestCase):
    def test_01_l1_budgets_one_bond_and_actual_equipment(self):
        self.assertTrue(verify())
        for lv in LEVELS:
            s = profile(lv)
            self.assertEqual(28,s["ability_points"])
            self.assertEqual((70,80),(s["starting_spent_sp"],s["silver_remaining_sp"]))
            self.assertEqual(2,s["weapon_development_points"])
            self.assertEqual(8+int(lv>=2),s["learned_points"])
            self.assertEqual((BOND,MISSION,IMPRINT),(s["bond"],s["mission"],s["birth_imprint"]))
            self.assertEqual(["Basic Heal","Guided Regeneration"],s["known_bonded_techniques"])
            self.assertEqual([],s["known_other_aspect_techniques"])
            self.assertEqual((3,13),(s["sword_attack_bonus"],s["sword_guard_defense"]))
            self.assertFalse(s["independent_full_focus_certified"])
            self.assertEqual(0,s["resonance"])

    def test_02_low_focus_ap_vp_talents_guard_and_regeneration(self):
        names=["TAL-A01 Imprint Recall","TAL-C02 Enhanced Regeneration","TAL-C05 Guard Reserve"]
        for lv in LEVELS:
            s=profile(lv)
            self.assertEqual((12,12*lv,2*lv),(s["hp_max"],s["vigor_max"],s["vp_max"]))
            self.assertEqual(30+6*(lv-1),s["turn_ap"])
            self.assertEqual((20,30,24),(s["physical_action_ap"],s["projection_action_ap"],s["general_action_ap"]))
            self.assertEqual((2 if lv==3 else 1,1),(s["physical_tempo"],s["projection_tempo"]))
            self.assertEqual((3 if lv==3 else 1,2 if lv==3 else 1),
                             (s["guard_capacity"],s["opportunity_capacity"]))
            self.assertEqual(0,s["guard_reserve_opportunity_bonus"])
            self.assertEqual(5 if lv==1 else 6,s["normal_regen_throughput"])
            self.assertEqual(names[:lv],s["talents"])
            self.assertEqual(lv==3,s["two_paid_physical_attacks_fit"])
            self.assertFalse(s["physical_attack_plus_projection_fit"])
            self.assertFalse(s["two_projection_actions_fit"])
            self.assertFalse(s["blink_affordable_from_full_vp"])
            self.assertEqual(lv==3,s["l3_guided_self_primary_lesser_eligible"])
            self.assertFalse(s["l3_guided_single_target_lesser_eligible"])
            self.assertFalse(s["l3_basic_heal_lesser_eligible"])
        for bad in (0,4,True,1.5):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                profile(bad)

    def test_03_self_only_existing_step_and_no_repeat_or_retiming(self):
        a=Anointed(2,"Low","Restoration")
        base=dict(target_id="self",recipient_hp=5,recipient_max_hp=12,
                  recipient_vigor=4,authenticated_regeneration_step=True,
                  focus_turn_id="self:turn1",distance=0)
        first=returning_step(a,receipt="self-pulse",**base)
        self.assertEqual((0,1,1),(first.ap_spent,first.hp_restored,first.recipient_vigor_spent))
        for changed in (
            {"target_id":"ally"},{"distance":1},
            {"authenticated_regeneration_step":False},{"focus_turn_id":None},
            {"recipient_hp":0},{"recipient_living":False},
            {"recipient_hp":12},{"path_visible":False},
        ):
            with self.subTest(changed=changed),self.assertRaises(ValueError):
                returning_step(a,receipt="invalid",**(base|changed))
        with self.assertRaises(ValueError):
            returning_step(first.actor,receipt="second-same-turn",**base)
        with self.assertRaises(ValueError):
            returning_step(first.actor,receipt="self-pulse",
                           **(base|{"focus_turn_id":"self:turn2"}))
        fresh=returning_step(first.actor,receipt="next-step",**(base|{"focus_turn_id":"self:turn2"}))
        self.assertEqual(1,fresh.hp_restored)

    def test_04_embodiment_suppression_resume_and_dormancy(self):
        a=Anointed(1,"Low","Restoration")
        for flags in ({"manifested":False,"at_own_turn_start":False},):
            with self.assertRaises(ValueError):
                set_embodiment(a,**flags)
        off=set_embodiment(a,manifested=False,at_own_turn_start=True)
        args=dict(receipt="disabled",target_id="self",recipient_hp=5,
                  recipient_max_hp=12,recipient_vigor=4,
                  authenticated_regeneration_step=True,focus_turn_id="R1")
        with self.assertRaises(ValueError):
            returning_step(off,**args)
        with self.assertRaises(ValueError):
            guided_regeneration_l3(off,receipt="l3-not-even-level",active_paid_guided_instance=True,
                                   mode="Fixed",profile="Self",recipient_self=True,
                                   authenticated_regeneration_step=True,
                                   recipient_missing_hp_after_ordinary=2,
                                   guided_bonus_unsuppressed=True)
        on=set_embodiment(off,manifested=True,at_own_turn_start=True)
        self.assertEqual(1,returning_step(on,**args).hp_restored)
        dormant=set_bond(a,active=False)
        self.assertFalse(dormant.embodied)
        with self.assertRaises(ValueError):
            returning_step(dormant,**args)
        self.assertEqual(dormant,mission_event(dormant,"gm-event",gm_recognized=True))
        with self.assertRaises(ValueError):
            invest(a,"patient",ap_available=24,legal_vessel=True,
                   consent_or_other_delivery_valid=True)

    def test_05_one_destiny_no_vigor_and_legitimate_resistance(self):
        a=Anointed(1,"Low","Restoration")
        args=dict(target_id="self",recipient_hp=6,recipient_max_hp=12,
                  recipient_vigor=0,authenticated_regeneration_step=True,
                  focus_turn_id="step1")
        with self.assertRaises(ValueError):
            returning_step(a,receipt="without-vigor",**args)
        lesser=returning_step(a,receipt="waiver",lesser=True,**args)
        self.assertEqual((1,0,1),(lesser.hp_restored,lesser.recipient_vigor_spent,lesser.actor.destiny))
        with self.assertRaises(ValueError):
            returning_step(lesser.actor,receipt="replay-other",lesser=True,**args)
        refused=returning_step(a,receipt="resisted",lesser=True,
                 intrusion_succeeded=False,**args)
        self.assertEqual((0,0,1),(refused.hp_restored,refused.recipient_vigor_spent,
                                   refused.actor.destiny))
        for change in ({"recipient_hp":12},{"beneficial_intrusion_legal":False}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                returning_step(a,receipt="unlawful",lesser=True,**(args|change))
        with self.assertRaises(ValueError):
            returning_step(Anointed(1,"Low","Restoration",destiny=0),
                           receipt="no-destiny",lesser=True,**args)

    def test_06_l3_guided_requires_real_self_primary_paid_instance(self):
        a=Anointed(3,"Low","Restoration")
        args=dict(receipt="self-guided-step",recipient_missing_hp_after_ordinary=2,
                  active_paid_guided_instance=True,mode="Maintained",profile="Self",
                  authenticated_regeneration_step=True,recipient_self=True,
                  guided_bonus_unsuppressed=True)
        x=guided_regeneration_l3(a,**args)
        self.assertEqual((1,1),(x.additional_hp_without_vigor,x.actor.destiny))
        for change in ({"profile":"Single Target"},{"recipient_self":False},
                       {"recipient_missing_hp_after_ordinary":0},
                       {"active_paid_guided_instance":False},
                       {"authenticated_regeneration_step":False},
                       {"guided_bonus_unsuppressed":False},
                       {"recipient_dying":True},{"mode":"Invalid"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                guided_regeneration_l3(a,**(args|change))
        with self.assertRaises(ValueError):
            guided_regeneration_l3(set_embodiment(a,manifested=False,at_own_turn_start=True),**args)
        with self.assertRaises(ValueError):
            guided_regeneration_l3(Anointed(2,"Low","Restoration"),**args)
        with self.assertRaises(ValueError):
            guided_regeneration_l3(x.actor,**args)
        with self.assertRaises(ValueError):
            kindled_flame(a,receipt="borrow-fire",hit=True,target_vigor=8,target_hp=6,
                          carrier_attack_authentic=True,carrier_attack_on_own_turn=True,
                          active_wielded_weapon_id="Sword",turn_id="R1")

    def test_07_talents_do_not_mint_signature_or_extra_step(self):
        for lv in LEVELS:
            s=profile(lv)
            self.assertEqual(1,s["signature_hp_cap"])
            self.assertTrue(s["signature_requires_existing_own_turn_regeneration_step"])
            self.assertFalse(s["l2_living_instrument_extra_pulse"])
            self.assertFalse(s["l2_living_instrument_step_retiming"])
            self.assertFalse(s["l2_living_instrument_reactive_guard_effect"])
            self.assertEqual(s["physical_tempo"],s["opportunity_capacity"])
            self.assertEqual(int(lv>=2),s["enhanced_regeneration_throughput_bonus"])
            self.assertEqual(int(lv>=3),s["guard_reserve_capacity_bonus"])
            self.assertFalse(s["guided_grants_extra_regeneration_step"])
            self.assertEqual(30,s["guided_requires_normal_activation_ap"])

    def test_08_isolated_regressions_and_roadmap_are_not_certification(self):
        for lv in LEVELS:
            w=isolated_witness(lv)
            self.assertEqual((0,1,1,1,0,1),(w["signature_ap"],w["normal_hp"],
                w["normal_self_vigor_spent"],w["lesser_hp"],
                w["lesser_self_vigor_spent"],w["lesser_destiny_remaining"]))
            self.assertTrue(w["suppress_then_resume"])
            self.assertFalse(w["native_attestation"])
            self.assertFalse(w["full_focus_certified"])
            self.assertEqual(lv==3,w["l3_guided"] is not None)
        doc=(ROOT/"docs/design/b04-b05-low-anointed-restoration-l1-l3-character-build-verification-v0.md").read_text(encoding="utf-8")
        roadmap=(ROOT/"docs/design/veilbound-roadmap-and-mvp-readiness.md").read_text(encoding="utf-8")
        index=(ROOT/"docs/design/README.md").read_text(encoding="utf-8")
        for phrase in ("28-point","TAL-C02","TAL-C05","Living Instrument",
                       "12/12","0/12","0/6","Guided Regeneration"):
            self.assertIn(phrase,doc)
        self.assertIn("**12/12**",roadmap)
        self.assertIn("**0/12**",roadmap)
        self.assertIn("**0/6**",roadmap)
        self.assertIn("b04-b05-low-anointed-restoration-l1-l3-character-build-verification-v0.md",index)


if __name__ == "__main__":
    unittest.main()
