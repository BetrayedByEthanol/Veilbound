"""Bounded Low Gifted Anchor design assertions; NEVER native combat claims."""
import unittest
from scripts.b05_low_gifted_anchor_design_v0 import (
    starting_access, LowGiftedAnchorDesign, ordinary_cast_budget, CANDIDATE,
)


class LowGiftedAnchorDesignTests(unittest.TestCase):
    def test_01_eight_distinct_source_links_and_no_extra_forms(self):
        for level in (1,2,3):
            p=starting_access(level)
            self.assertEqual(len(p["links"]),8)
            self.assertEqual(len({v["pillar"] for v in p["links"].values()}),8)
            self.assertEqual(len({v["aspect"] for v in p["links"].values()}),8)
            self.assertEqual([e for e in p["links"] if p["links"][e]["compatibility"]=="P"],["Joy","Anger"])
            self.assertEqual([e for e in p["links"] if p["links"][e]["anchor_expression_candidate"]],["Fear","Disgust"])
            self.assertFalse(p["structural_character_build_complete"])
            self.assertFalse(p["canonical_anchor_expression_authored"])
            self.assertEqual(p["universal_known"], ["Veil Inspection"]+(["Blink"] if level==3 else []))

    def test_02_vp_action_tempo_and_blink_stay_low(self):
        for lv,vp,ap,guard in ((1,2,30,1),(2,4,36,1),(3,6,42,2)):
            p=starting_access(lv)
            self.assertEqual((p["vp_max"],p["turn_ap"],p["guard_capacity"]),(vp,ap,guard))
            self.assertEqual((p["physical_action_ap"],p["projection_action_ap"],p["general_action_ap"]),(20,30,24))
            self.assertFalse(p["blink_affordable_at_full_vp"])
            self.assertEqual(p["anchor_extra_vp_cost_candidate"],0)
        self.assertEqual(starting_access(3,veil_affinity=2)["vp_max"],12)
        self.assertTrue(starting_access(3,veil_affinity=2)["blink_affordable_at_full_vp"])

    def test_03_anchor_persists_without_pulse_refresh_during_window(self):
        m=LowGiftedAnchorDesign(1)
        m.begin_window()
        m.establish_anchor("Fear")
        first=m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True)
        self.assertEqual(first.bonus,1)
        self.assertFalse(m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True).applicable)
        m.begin_window()
        self.assertEqual(m.active,"Fear")
        self.assertTrue(m.persisted_from_previous)
        self.assertEqual(m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True).bonus,1)

    def test_04_no_free_guard_dodge_or_l1_instinctive(self):
        m=LowGiftedAnchorDesign(1);m.begin_window();m.establish_anchor("Fear")
        for kw in ({"kind":"guard","paid":False,"self_target":True,"source_legal":True},
                   {"kind":"guard","paid":True,"self_target":False,"source_legal":True},
                   {"kind":"guard","paid":True,"self_target":True,"source_legal":False},
                   {"kind":"dodge","paid":True,"self_target":True,"source_legal":True}):
            self.assertEqual(m.guarded_defense(**kw).bonus,0)
        self.assertEqual(m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True).bonus,1)
        m2=LowGiftedAnchorDesign(2);m2.begin_window();m2.establish_anchor("Fear")
        self.assertEqual(m2.guarded_defense(kind="dodge",paid=True,self_target=True,source_legal=True).bonus,1)
        self.assertEqual(m2.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True).bonus,0)

    def test_05_break_anchor_pays_24_and_does_not_refresh_pulse(self):
        m=LowGiftedAnchorDesign(2);m.begin_window();m.establish_anchor("Fear")
        m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True)
        m.break_anchor("Disgust")
        self.assertEqual((m.ap_remaining,m.anchor,m.active),(12,"Disgust","Disgust"))
        self.assertFalse(m.movement_step(kind="normal_difficult",paid=True,source_legal=True,base_mp=1,surcharge_mp=2).applicable)
        with self.assertRaises(ValueError):m.break_anchor("Fear")
        m.begin_window()
        self.assertTrue(m.movement_step(kind="normal_difficult",paid=True,source_legal=True,base_mp=1,surcharge_mp=2).applicable)
        m.break_anchor("Fear")
        self.assertEqual(m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True).bonus,0)
        self.assertEqual(m.pulse_window,m.window)

    def test_06_disgust_step_only_reduces_paid_surcharge(self):
        m=LowGiftedAnchorDesign(1);m.begin_window();m.establish_anchor("Disgust")
        self.assertEqual(m.movement_step(kind="normal_difficult",paid=True,source_legal=True,base_mp=1,surcharge_mp=0).mp_reduction,0)
        self.assertEqual(m.movement_step(kind="cautious",paid=True,source_legal=True,base_mp=1,surcharge_mp=1).mp_reduction,0)
        self.assertEqual(m.movement_step(kind="normal_difficult",paid=False,source_legal=True,base_mp=1,surcharge_mp=2).mp_reduction,0)
        p=m.movement_step(kind="normal_difficult",paid=True,source_legal=True,base_mp=1,surcharge_mp=2)
        self.assertEqual((p.mp_reduction,p.remaining_mp_cost),(1,2))
        self.assertEqual(m.movement_step(kind="normal_difficult",paid=True,source_legal=True,base_mp=1,surcharge_mp=2).remaining_mp_cost,3)
        m2=LowGiftedAnchorDesign(2);m2.begin_window();m2.establish_anchor("Disgust")
        self.assertEqual(m2.movement_step(kind="cautious",paid=True,source_legal=True,base_mp=1,surcharge_mp=1).remaining_mp_cost,1)

    def test_07_external_emotion_disrupts_and_requires_paid_reassertion(self):
        m=LowGiftedAnchorDesign(2);m.begin_window();m.establish_anchor("Fear");m.force_disruption("Joy")
        self.assertEqual(m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True).bonus,0)
        m.begin_window();self.assertNotEqual(m.active,"Fear")
        self.assertTrue(m.disrupted)
        self.assertFalse(m.reassert(die=1,awareness=0,discipline=0))
        self.assertEqual((m.ap_remaining,m.active),(12,None))
        with self.assertRaises(ValueError):m.reassert(die=20,awareness=0,discipline=0)
        m.begin_window();self.assertTrue(m.reassert(die=12,awareness=0,discipline=0))
        self.assertEqual(m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True).bonus,1)

    def test_08_settled_l3_requires_uninterrupted_previous_window(self):
        m=LowGiftedAnchorDesign(3);m.begin_window();m.establish_anchor("Fear")
        first=m.deepen(die=1,awareness=0,discipline=0)
        self.assertEqual((first["ap_spent"],first["settled"]),(24,False))
        m.begin_window()
        after=m.deepen(die=12,awareness=0,discipline=0)
        self.assertEqual((after["ap_spent"],after["settled"],m.ap_remaining),(0,True,42))
        self.assertTrue(m.heightened)
        with self.assertRaises(ValueError):m.deepen(die=12,awareness=0,discipline=0)
        m.begin_window()
        self.assertTrue(m.heightened)  # Settled persists; no repeat Deepen needed
        with self.assertRaises(ValueError):m.deepen(die=15,awareness=0,discipline=0)

    def test_09_reanchoring_or_disruption_loses_settled(self):
        m=LowGiftedAnchorDesign(3);m.begin_window();m.establish_anchor("Disgust");m.begin_window()
        m.break_anchor("Fear")
        # Break 24 AP plus paid Deepen 24 AP exceeds actual L3 42 AP.
        with self.assertRaises(ValueError):m.deepen(die=12,awareness=0,discipline=0)
        n=LowGiftedAnchorDesign(3);n.begin_window();n.establish_anchor("Fear");n.begin_window();n.force_disruption("Joy")
        with self.assertRaises(ValueError):n.deepen(die=20,awareness=2,discipline=2)

    def test_10_paid_cast_splits_emotion_and_vp_and_ap(self):
        self.assertEqual(ordinary_cast_budget(1,"Joy","Conjure Flame"),{
            "affordable":True,"ap_required":30,"vp_required":2,"vp_mode":"spent",
            "emotion_required":"Joy","profile_resolution_certified":False})
        self.assertEqual(ordinary_cast_budget(1,"Fear","Stone Skin")["vp_required"],1)
        self.assertEqual(ordinary_cast_budget(3,"Fear","Stone Skin")["vp_required"],2)
        self.assertTrue(ordinary_cast_budget(3,"Sadness","Basic Heal",used_tier=2)["affordable"])
        self.assertFalse(ordinary_cast_budget(3,"Joy","Conjure Flame",available_vp=1)["affordable"])
        self.assertFalse(ordinary_cast_budget(3,"Joy","Conjure Flame",available_ap=24)["affordable"])

    def test_11_no_free_upcast_or_unverified_mode_price(self):
        for args in ((1,"Joy","Conjure Flame",2), (2,"Fear","Stone Skin",2),
                     (3,"Fear","Stone Skin",2), (3,"Disgust","Weaken Restraints",1),
                     (3,"Trust","Protective Ward",1)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                ordinary_cast_budget(args[0],args[1],args[2],used_tier=args[3])
        with self.assertRaises(ValueError):ordinary_cast_budget(1,"Fear","Conjure Flame")

    def test_12_strict_invalid_inputs_no_hidden_window(self):
        with self.assertRaises(ValueError):starting_access(True)
        with self.assertRaises(ValueError):starting_access(4)
        with self.assertRaises(ValueError):starting_access(1,veil_affinity=1.5)
        m=LowGiftedAnchorDesign(1)
        with self.assertRaises(ValueError):m.establish_anchor("Fear")
        m.begin_window();m.establish_anchor("Fear")
        with self.assertRaises(ValueError):m.establish_anchor("Joy")
        with self.assertRaises(ValueError):m.break_anchor("Fear")
        with self.assertRaises(ValueError):m.movement_step(kind="normal_difficult",paid=True,source_legal=True,base_mp=0,surcharge_mp=1)
        with self.assertRaises(ValueError):m.guarded_defense(kind="guard",paid=1,self_target=True,source_legal=True)

    def test_13_false_check_and_no_unearned_heightening(self):
        m=LowGiftedAnchorDesign(3);m.begin_window();m.establish_anchor("Fear");m.begin_window()
        result=m.deepen(die=1,awareness=1,discipline=2)
        self.assertFalse(result["success"])
        self.assertFalse(m.heightened)
        self.assertEqual(result["ap_spent"],0)
        m.begin_window()
        self.assertFalse(m.heightened)
        self.assertIsNone(m.guarded_defense(kind="guard",paid=False,self_target=True,source_legal=True).expression)

    def test_15_matching_dominant_preserves_settled_and_free_deepen(self):
        m=LowGiftedAnchorDesign(3)
        m.begin_window(dominant="Fear")
        m.establish_anchor("Fear")
        self.assertEqual((m.anchor,m.active,m.disrupted),("Fear","Fear",False))
        self.assertFalse(m.persisted_from_previous)  # combat start, not L3 settled
        self.assertEqual(m.deepen(die=1,awareness=0,discipline=0)["ap_spent"],24)
        m.begin_window(dominant="Fear")
        self.assertTrue(m.persisted_from_previous)
        self.assertFalse(m.disrupted)
        first=m.deepen(die=12,awareness=0,discipline=0)
        self.assertEqual((first["ap_spent"],first["settled"],m.ap_remaining),(0,True,42))
        self.assertTrue(m.heightened)
        m.begin_window(dominant="Fear")
        self.assertTrue(m.persisted_from_previous)
        self.assertEqual((m.active,m.disrupted,m.heightened),("Fear",False,True))
        with self.assertRaises(ValueError):
            m.deepen(die=12,awareness=0,discipline=0)

    def test_16_initial_matching_dominant_allows_first_anchor(self):
        for level in (1,2,3):
            m=LowGiftedAnchorDesign(level)
            m.begin_window(dominant="Disgust")
            self.assertIsNone(m.anchor)
            self.assertFalse(m.disrupted)
            m.establish_anchor("Disgust")
            self.assertEqual((m.anchor,m.active,m.disrupted),("Disgust","Disgust",False))
            self.assertFalse(m.persisted_from_previous)
            self.assertEqual(m.ap_remaining,starting_access(level)["turn_ap"])
            step=m.movement_step(kind="normal_difficult",paid=True,
                                 source_legal=True,base_mp=1,surcharge_mp=2)
            self.assertEqual(step.mp_reduction,1)
            with self.assertRaises(ValueError):m.establish_anchor("Fear")

    def test_17_initial_competing_dominant_requires_paid_reassert(self):
        for level in (1,2,3):
            m=LowGiftedAnchorDesign(level)
            m.begin_window(dominant="Joy")
            m.establish_anchor("Fear")
            self.assertEqual((m.anchor,m.active,m.disrupted),("Fear","Joy",True))
            self.assertFalse(m.guarded_defense(kind="guard",paid=True,
                             self_target=True,source_legal=True).applicable)
            before=m.ap_remaining
            self.assertFalse(m.reassert(die=1,awareness=0,discipline=0))
            self.assertEqual((m.anchor,m.active,m.disrupted),("Fear","Joy",True))
            self.assertEqual(m.ap_remaining,before-24)
        m=LowGiftedAnchorDesign(3)
        m.begin_window(dominant="Joy")
        m.establish_anchor("Fear")
        self.assertTrue(m.reassert(die=12,awareness=0,discipline=0))
        self.assertEqual((m.anchor,m.active,m.disrupted),("Fear","Fear",False))
        self.assertFalse(m.persisted_from_previous)
        self.assertTrue(m.guarded_defense(kind="guard",paid=True,self_target=True,
                                        source_legal=True).applicable)
        # First-turn recovery cannot claim settled status or another 24 AP.
        with self.assertRaises(ValueError):m.deepen(die=12,awareness=0,discipline=0)
        m.begin_window(dominant="Fear")
        self.assertTrue(m.persisted_from_previous)
        self.assertEqual(m.deepen(die=12,awareness=0,discipline=0)["ap_spent"],0)

    def test_18_existing_disruption_not_cleared_by_matching_dominant(self):
        m=LowGiftedAnchorDesign(3)
        m.begin_window()
        m.establish_anchor("Fear")
        m.begin_window()
        m.deepen(die=12,awareness=0,discipline=0)
        self.assertTrue(m.heightened)
        m.force_disruption("Joy")
        m.begin_window(dominant="Fear")
        self.assertEqual((m.anchor,m.active,m.disrupted),("Fear","Fear",True))
        self.assertFalse(m.persisted_from_previous)
        self.assertFalse(m.heightened)
        self.assertFalse(m.guarded_defense(kind="guard",paid=True,
                         self_target=True,source_legal=True).applicable)
        self.assertTrue(m.reassert(die=12,awareness=0,discipline=0))
        # Transition actually consumed the 24 AP; no free Settled use and
        # not enough remaining L3 AP for a second paid 24 AP Deepen.
        with self.assertRaises(ValueError):
            m.deepen(die=12,awareness=0,discipline=0)
        m.begin_window(dominant="Fear")
        self.assertTrue(m.persisted_from_previous)
        self.assertEqual(m.deepen(die=12,awareness=0,discipline=0)["ap_spent"],0)

    def test_19_no_skipping_initial_anchor_choice(self):
        for dominant in (None,"Fear"):
            m=LowGiftedAnchorDesign(3)
            m.begin_window(dominant=dominant)
            with self.assertRaises(ValueError):m.begin_window()
            m.establish_anchor("Fear")
            self.assertEqual(m.window,1)
        m=LowGiftedAnchorDesign(2)
        with self.assertRaises(ValueError):m.begin_window(dominant="NotLinked")
        self.assertEqual(m.window,0)

    def test_14_two_candidates_are_aspect_specific_not_spell_copies(self):
        self.assertEqual(CANDIDATE["Fear"]["pillar"],"Earth")
        self.assertEqual(CANDIDATE["Disgust"]["aspect"],"Defiance")
        self.assertEqual(CANDIDATE["Fear"]["bonus"],1)
        self.assertEqual(CANDIDATE["Disgust"]["mp_surcharge_reduction"],1)
        self.assertFalse(starting_access(3)["canonical_anchor_expression_authored"])


if __name__ == "__main__":
    unittest.main()
