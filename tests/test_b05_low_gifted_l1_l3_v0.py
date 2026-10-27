"""Low Gifted L1–3 structural legality and PR #158 isolated Anchor checks."""
from pathlib import Path
import unittest

from scripts.b05_high_gifted_amplification_v0 import PILOT_LINKS
from scripts.b05_high_gifted_l1_l3_v0 import AUTHORED_ACCESS, AUTHORED_UPCAST_T2
from scripts.b05_low_gifted_anchor_design_v0 import (
    LowGiftedAnchorDesign, ordinary_cast_budget,
)
from scripts.b05_low_gifted_l1_l3_v0 import (
    ABILITIES, EQUIPMENT_SP, LEARNED_L1, FAMILIES, TALENTS, LEVELS,
    anchor_witness, profile, verify,
)

ROOT=Path(__file__).resolve().parents[1]


class LowGiftedBuildTests(unittest.TestCase):
    def test_01_all_three_structural_levels(self):
        self.assertTrue(verify())
        for level in LEVELS:
            s=profile(level)
            self.assertEqual((s["archetype"],s["focus"],s["level"]),("Gifted","Low",level))
            self.assertEqual(s["ability_points"],28)
            self.assertEqual(s["abilities"],ABILITIES)
            self.assertEqual(s["resonance"],0)
            self.assertTrue(s["structural_character_build_complete"])
            self.assertFalse(s["independent_full_focus_certified"])

    def test_02_independent_ability_training_and_progression_budgets(self):
        self.assertEqual(len(ABILITIES),9)
        self.assertEqual(sum(LEARNED_L1.values()),8)
        self.assertEqual(FAMILIES,{"Cultural and Specialized":4,
                                  "Physical and Fieldcraft":2,
                                  "Professional and Technical":2})
        for level in LEVELS:
            s=profile(level)
            self.assertEqual(s["weapon_training"],{"One-Handed Swords":2})
            self.assertEqual(s["weapon_development_points"],2)
            self.assertEqual(s["learned_points"],8+int(level>=2))
            self.assertEqual(s["learned_disciplines"]["Emotional Discipline"],2)
            self.assertEqual(s["learned_disciplines"].get("Navigation"),
                             1 if level>=2 else None)
            self.assertTrue(all(0<=value<=2
                                for value in s["learned_disciplines"].values()))
            self.assertEqual(len(s["background_familiarities"]),2)
        self.assertEqual(profile(1)["abilities"],profile(3)["abilities"])
        self.assertEqual(profile(2)["learned_disciplines"],profile(3)["learned_disciplines"])

    def test_03_three_separate_low_talent_awards(self):
        self.assertEqual(TALENTS,{1:"TAL-G01 Emotional Poise",
                                  2:"TAL-C05 Guard Reserve",
                                  3:"TAL-C01 Combat Awareness"})
        for level in LEVELS:
            s=profile(level)
            self.assertEqual(s["talents"],[TALENTS[n] for n in range(1,level+1)])
            self.assertEqual(s["talent_selections_acquired"],level)
            self.assertEqual(s["talent_selection_levels"],list(range(1,level+1)))
            self.assertEqual(s["talent_guard_reserve_capacity"],int(level>=2))
            self.assertEqual(s["talent_emotional_poise_bonus_once_per_window"],2)
            self.assertEqual(s["talent_combat_awareness_initiative"],
                             2 if level==3 else 0)

    def test_04_weapon_armor_equipment_and_coin_conservation(self):
        self.assertEqual(EQUIPMENT_SP,{"Leather armor":25,"Sword":22,
                          "Standard adventuring pack":8,"Basic medical kit":15})
        for level in LEVELS:
            s=profile(level)
            self.assertEqual((s["starting_budget_sp"],s["starting_spent_sp"],
                              s["silver_remaining_sp"]),(150,70,80))
            self.assertEqual((s["armor"],s["wielded_weapon"]),(3,"Sword"))
            self.assertEqual((s["sword_attack_bonus"],s["sword_guard_defense"]),(7,17))
            self.assertEqual(s["sword_penetration"],2)
            self.assertEqual(s["sword_damage"],"3+d6 Cut/Pierce (Light contribution +1)")

    def test_05_focus_action_vp_and_talent_guard_vs_opportunity(self):
        for level,ap,vp,guard,opp,initiative in (
                (1,30,2,1,1,4),(2,36,4,2,1,4),(3,42,6,3,2,6)):
            s=profile(level)
            self.assertEqual((s["hp_max"],s["vigor_max"],s["vp_max"]),(12,12*level,vp))
            self.assertEqual((s["turn_ap"],s["physical_action_ap"],
                              s["projection_action_ap"],s["general_action_ap"]),
                             (ap,20,30,24))
            self.assertEqual(s["physical_tempo"],ap//20)
            self.assertEqual(s["projection_tempo"],1)
            self.assertEqual((s["guard_capacity"],s["opportunity_capacity"]),(guard,opp))
            self.assertEqual((s["first_dodge"],s["initiative"]),(14,initiative))
            self.assertEqual((s["movement_points"],s["normal_regen_throughput"]),(12,5))
            self.assertEqual(s["emotional_discipline_check_bonus"],3)
            self.assertEqual(s["instability_check_bonus"],2)
            self.assertEqual(s["stone_skin_t1_committed_vp"],(vp+2)//3)
            self.assertFalse(s["paid_break_plus_projection_fit"])
            self.assertFalse(s["paid_deepen_plus_projection_fit"])
            self.assertFalse(s["paid_break_plus_paid_deepen_fit"])
            self.assertEqual(s["two_physical_actions_fit"],level==3)

    def test_06_eight_unchanged_links_with_explicit_plausible_interpretation(self):
        for level in LEVELS:
            s=profile(level)
            links=s["emotion_aspect_links"]
            self.assertEqual(set(links),set(PILOT_LINKS))
            self.assertEqual(len({v["pillar"] for v in links.values()}),8)
            self.assertEqual(len({v["aspect"] for v in links.values()}),8)
            self.assertEqual({e for e in links if links[e]["compatibility"]=="P"},
                             {"Joy","Anger"})
            for e in ("Joy","Anger"):
                self.assertTrue(links[e]["creation_interpretation"])
            self.assertEqual(s["authored_linked_techniques"],
                             {e:list(AUTHORED_ACCESS[e]) for e in PILOT_LINKS})
            self.assertEqual(s["authored_upcast_t2"],
                             sorted(AUTHORED_UPCAST_T2) if level==3 else [])
            self.assertIsNone(s["prepared_techniques"])
            self.assertIsNone(s["individually_learned_pillar_techniques"])
            self.assertIsNone(s["active_emotion"])
            self.assertIsNone(s["anchored_emotion"])

    def test_07_candidate_anchor_not_canon_or_native_authority(self):
        for level in LEVELS:
            s=profile(level)
            self.assertEqual(set(s["anchor_expressions"]),{"Fear","Disgust"})
            self.assertTrue(all(e["status"]=="PROVISIONAL_UNAPPROVED"
                                for e in s["anchor_expressions"].values()))
            self.assertEqual(s["anchor_candidate_pulse_per_window"],1)
            self.assertEqual((s["anchor_extra_spent_vp"],s["anchor_extra_committed_vp"]),(0,0))
            self.assertFalse(s["anchor_native_effect_certified"])
            self.assertFalse(s["native_combat_or_noncombat_certified"])
            for absent in ("projected_surge","conduit_slots","exaltation",
                           "extra_reaction","free_guard"):
                self.assertNotIn(absent,s)

    def test_08_real_source_budget_and_unauthored_modes_refused(self):
        for level in LEVELS:
            s=profile(level)
            self.assertTrue(ordinary_cast_budget(level,"Joy","Conjure Flame")["affordable"])
            self.assertEqual(ordinary_cast_budget(level,"Fear","Stone Skin")["vp_required"],
                             s["stone_skin_t1_committed_vp"])
            self.assertFalse(ordinary_cast_budget(level,"Joy","Conjure Flame",
                                                  available_ap=24)["affordable"])
            with self.assertRaises(ValueError):
                ordinary_cast_budget(level,"Fear","Conjure Flame")
            with self.assertRaises(ValueError):
                ordinary_cast_budget(level,"Trust","Protective Ward")
            with self.assertRaises(ValueError):
                ordinary_cast_budget(level,"Fear","Stone Skin",used_tier=2)
        self.assertFalse(ordinary_cast_budget(1,"Joy","Conjure Flame",
                                             available_vp=1)["affordable"])
        self.assertTrue(ordinary_cast_budget(3,"Joy","Conjure Flame",
                                            used_tier=2)["affordable"])

    def test_09_commitment_and_blink_cannot_be_paid_twice(self):
        for level in LEVELS:
            s=profile(level)
            left=s["vp_max"]-s["stone_skin_t1_committed_vp"]
            self.assertEqual(ordinary_cast_budget(level,"Sadness","Basic Heal",
                              available_vp=left)["affordable"],left>=2)
            self.assertFalse(s["blink_affordable_from_full_vp"])
            self.assertEqual(s["universal"],
                             ["Veil Inspection"]+(["Blink"] if level==3 else []))
            self.assertEqual(s["blink_known"],level==3)
        self.assertEqual(profile(1)["vp_max"]-profile(1)["stone_skin_t1_committed_vp"],1)
        self.assertEqual(profile(3)["blink_base_spent_vp"],10)

    def test_10_finite_candidate_pulses_and_paid_reassertion(self):
        for level in LEVELS:
            w=anchor_witness(level)
            self.assertEqual((w["first_defense"],w["repeated_defense"],
                              w["new_window_defense"]),(1,0,1))
            self.assertEqual((w["break_no_refresh"],w["fresh_movement_mp"],
                              w["repeated_movement_mp"]),(0,2,3))
            self.assertTrue(w["competing_inactive"])
            self.assertTrue(w["paid_transition"])
            self.assertEqual(w["transition_ap_remaining"],profile(level)["turn_ap"]-24)
            self.assertEqual(w["reasserted_defense"],1)
            self.assertFalse(w["native_receipt"])
            self.assertFalse(w["canonical_anchor_approved"])

    def test_11_initial_paid_deepen_does_not_permanently_heighten_l3(self):
        z=anchor_witness(3)["level3_settled"]
        self.assertEqual((z["paid"]["success"],z["paid"]["ap_spent"],
                          z["paid"]["settled"]),(True,24,False))
        self.assertTrue(z["ordinary_expired"])
        self.assertEqual((z["free"]["success"],z["free"]["ap_spent"],
                          z["free"]["settled"]),(True,0,True))
        self.assertTrue(z["persistent"])
        self.assertIsNone(anchor_witness(1)["level3_settled"])
        self.assertIsNone(anchor_witness(2)["level3_settled"])

    def test_12_actual_l2_candidate_dodge_not_l1_dodge(self):
        a=LowGiftedAnchorDesign(1)
        a.begin_window();a.establish_anchor("Fear")
        self.assertFalse(a.guarded_defense(kind="dodge",paid=True,
                         self_target=True,source_legal=True).applicable)
        b=LowGiftedAnchorDesign(2)
        b.begin_window();b.establish_anchor("Fear")
        self.assertTrue(b.guarded_defense(kind="dodge",paid=True,
                        self_target=True,source_legal=True).applicable)
        c=LowGiftedAnchorDesign(1)
        c.begin_window();c.establish_anchor("Disgust")
        self.assertFalse(c.movement_step(kind="cautious",paid=True,
                         source_legal=True,base_mp=1,surcharge_mp=1).applicable)

    def test_13_false_unpaid_or_wrong_target_cannot_grant_benefit(self):
        x=LowGiftedAnchorDesign(3)
        x.begin_window();x.establish_anchor("Fear")
        for kwargs in ({"paid":False,"self_target":True,"source_legal":True},
                       {"paid":True,"self_target":False,"source_legal":True},
                       {"paid":True,"self_target":True,"source_legal":False}):
            self.assertFalse(x.guarded_defense(kind="guard",**kwargs).applicable)
        self.assertEqual(x.guarded_defense(kind="guard",paid=True,
                         self_target=True,source_legal=True).bonus,1)
        x.break_anchor("Joy")
        self.assertFalse(x.guarded_defense(kind="guard",paid=True,
                         self_target=True,source_legal=True).applicable)

    def test_14_profile_isolation_and_strict_level_types(self):
        x=profile(1)
        x["abilities"]["Strength"]=-2
        x["equipment_sp"]["Sword"]=0
        x["talents"].append("UNSOURCED")
        x["anchor_expressions"]["Fear"]["bonus"]=99
        x["emotion_aspect_links"]["Joy"]["pillar"]="Unknown"
        y=profile(1)
        self.assertEqual(y["abilities"]["Strength"],2)
        self.assertEqual(y["equipment_sp"]["Sword"],22)
        self.assertEqual(y["talents"],[TALENTS[1]])
        self.assertEqual(y["anchor_expressions"]["Fear"]["bonus"],1)
        self.assertEqual(y["emotion_aspect_links"]["Joy"]["pillar"],"Fire")
        for invalid in (0,4,True,False,-1,2.0,"3",None):
            with self.assertRaises(ValueError):
                profile(invalid)
            with self.assertRaises(ValueError):
                anchor_witness(invalid)

    def test_15_repository_sources_and_genuine_low_talent_timing(self):
        paths={
            "creation":"docs/rules/02-character-creation/character-creation-foundation.md",
            "training":"docs/rules/02-character-creation/abilities-and-training.md",
            "talents":"docs/rules/10-advancement/talents-framework-v0.md",
            "catalogue":"docs/rules/10-advancement/talents-level-1-5-v0.md",
            "gifted":"docs/rules/08-archetypes/gifted.md",
            "proposal":"docs/design/b04-b05-low-gifted-l1-l3-focus-design-starting-access-v0.md",
        }
        if not all((ROOT/p).is_file() for p in paths.values()):
            self.skipTest("Full repository source documents required")
        data={k:(ROOT/p).read_text() for k,p in paths.items()}
        self.assertIn("28 ability points",data["creation"])
        self.assertIn("receive **8 points**",data["creation"])
        self.assertIn("| 2 | — | — | +1 |",data["talents"])
        self.assertIn("| 3 | — | +1 | +1 |",data["talents"])
        for t in ("TAL-G01 — Emotional Poise","TAL-C05 — Guard Reserve",
                  "TAL-C01 — Combat Awareness"):
            self.assertIn(t,data["catalogue"])
        self.assertIn("Low Gifted — Anchored Embodiment",data["gifted"])
        self.assertIn("L3 Settled Emotion",data["proposal"])


if __name__=="__main__":
    unittest.main()
