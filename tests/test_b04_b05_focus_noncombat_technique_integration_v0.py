"""B04/B05 source-paid noncombat technique contracts and fail-closed access."""
from collections import Counter
import unittest

from scripts.b04_b05_focus_noncombat_technique_integration_v0 import (
    OPTIONS, STATUS, run_scene, matrix,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision


class NoncombatTechniqueIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=matrix()
        cls.rows={(r["pairing"],r["level"],r["technique"]):r
                  for r in cls.report["rows"]}

    def test_01_twelve_focus_inspection_and_legally_authorized_specialties(self):
        self.assertEqual((12,3,47,36,11),(
            self.report["focus_pairings"],self.report["levels"],
            self.report["source_paid_noncombat_actions"],
            self.report["universal_inspection_coverage"],
            self.report["focus_specific_actions"]))
        self.assertEqual(len(self.rows),47)
        for pairing in ("Priest/High","Priest/Medium","Priest/Low",
                        "Scholar/High","Scholar/Medium","Scholar/Low",
                        "Gifted/High","Gifted/Medium","Gifted/Low",
                        "Anointed/High","Anointed/Medium","Anointed/Low"):
            for level in (1,2,3):
                self.assertIn((pairing,level,"Veil Inspection"),self.rows)
        self.assertEqual(Counter(r["technique"] for r in self.report["rows"]),
                         {"Veil Inspection":36,"Woodland Rapport":3,
                          "Phantom Sound":3,"Minor Telekinesis":5})

    def test_02_real_g0_full_action_and_vp_conservation_for_all_inspections(self):
        for row in self.report["rows"]:
            if row["technique"]!="Veil Inspection":
                continue
            with self.subTest(pairing=row["pairing"],level=row["level"]):
                self.assertEqual(row["action_class"],"full")
                self.assertEqual(row["ap_before"],row["ap_spent"])
                self.assertEqual(row["vp_spent"],2)
                self.assertEqual(row["vp_after"],row["vp_before"]-2)
                self.assertEqual(len(row["source_sha256"]),64)
                self.assertEqual(len(row["ledger_sha256"]),64)
                self.assertIn("action_committed",row["ledger_event_kinds"])
                self.assertIn("vp_transition",row["ledger_event_kinds"])
                self.assertTrue(row["effect_applied"])
                self.assertFalse(row["full_focus_certified"])

    def test_03_observable_pattern_not_full_magic_identification(self):
        for focus in ("Priest/High","Scholar/High","Gifted/Low","Anointed/Low"):
            row=run_scene(focus,1,"inspection")
            o=row["observation"]
            self.assertEqual((o["observable"],o["pillar"],o["aspect"]),
                             (True,"Life","Restoration"))
            self.assertFalse(o["function_identified"])
            self.assertFalse(o["concealed_revealed"])
        empty=run_scene("Scholar/High",1,"inspection",pattern="unobservable")
        self.assertFalse(empty["observation"]["observable"])
        self.assertIsNone(empty["interpretation"])
        self.assertEqual(empty["vp_spent"],2)

    def test_04_inspection_veil_theory_plus_two_on_one_relevant_check(self):
        high=run_scene("Priest/High",1,"inspection",face=7)
        self.assertEqual((high["interpretation"]["source_veil_theory_rank"],
                          high["interpretation"]["inspection_situational_modifier"]),
                         (2,2))
        self.assertEqual(high["interpretation"]["total"],11)
        self.assertFalse(high["interpretation"]["succeeds_on_authored_question"])
        other=run_scene("Anointed/Low",1,"inspection",face=12)
        self.assertEqual(other["interpretation"]["source_veil_theory_rank"],0)
        self.assertEqual(other["interpretation"]["total"],16)

    def test_05_medium_priest_l3_only_real_source_frugal_discount(self):
        row=run_scene("Priest/Medium",3,"inspection",discount=True)
        self.assertEqual((row["vp_spent"],row["vp_after"]), (1,row["vp_before"]-1))
        self.assertEqual(row["ap_spent"],row["ap_before"])
        for pair,level in (("Priest/Medium",2),("Priest/High",3),
                           ("Gifted/Low",3)):
            with self.subTest(pair=pair,level=level):
                with self.assertRaises(ValueError):
                    run_scene(pair,level,"inspection",discount=True)

    def test_06_interruption_spends_turn_ap_but_no_vp_or_information(self):
        for pair,tech in (("Priest/Medium","inspection"),
                          ("Priest/High","rapport"),
                          ("Scholar/High","sound"),
                          ("Scholar/Medium","telekinesis")):
            with self.subTest(pair=pair):
                row=run_scene(pair,2,tech,contact_lost_after_ap=True)
                self.assertFalse(row["effect_applied"])
                self.assertEqual(row["vp_spent"],0)
                self.assertIsNone(row["observation"])
                self.assertIsNone(row["interpretation"])
                self.assertGreater(row["ap_spent"],0)
                self.assertIn("b04_b05_noncombat_application_canceled",
                              row["ledger_event_kinds"])

    def test_07_priest_high_rapport_preserves_animal_choice_and_tier_limits(self):
        for level in (1,2,3):
            row=run_scene("Priest/High",level,"rapport")
            self.assertEqual((row["vp_spent"],row["ap_spent"]), (2,20))
            self.assertEqual(row["observation"]["initial_trust_bonus_pending"],2)
            self.assertFalse(row["observation"]["compulsion"])
            self.assertIn("GM",row["observation"]["animal_response"])
        high=run_scene("Priest/High",3,"rapport",tier=2,animal_mass_kg=90)
        self.assertEqual(high["vp_spent"],4)
        for kw in ({"tier":2,"animal_mass_kg":90},
                   {"animal_mass_kg":30},{"animal_state":"hostile"},
                   {"animal_visible":False},{"path_open":False},
                   {"sensory_route":False}):
            with self.subTest(kwargs=kw):
                with self.assertRaises(ValueError):
                    run_scene("Priest/High",1,"rapport",**kw)

    def test_08_scholar_high_phantom_sound_has_no_compulsion_or_damage(self):
        for level in (1,2,3):
            row=run_scene("Scholar/High",level,"sound")
            self.assertEqual((row["vp_spent"],row["ap_spent"]), (1,20))
            self.assertFalse(row["observation"]["forced_distraction"])
            self.assertEqual(row["observation"]["damage"],0)
            self.assertIn("GM",row["observation"]["listener_behavior"])
        for kw in ({"sound":"shouted_command"},{"sound_range_squares":13},
                   {"path_open":False}):
            with self.assertRaises(ValueError):
                run_scene("Scholar/High",1,"sound",**kw)

    def test_09_telekinesis_source_learning_object_limits_and_cost(self):
        with self.assertRaises(UnresolvedDecision):
            run_scene("Scholar/Medium",1,"telekinesis")
        for pair,level,ap in (("Scholar/High",1,20),
                              ("Scholar/Medium",2,24),
                              ("Scholar/Medium",3,24)):
            row=run_scene(pair,level,"telekinesis")
            self.assertEqual((row["vp_spent"],row["ap_spent"]),(2,ap))
            self.assertTrue(row["observation"]["unattended_object_moved"])
            self.assertFalse(row["observation"]["held_object_seized"])
            self.assertEqual(row["observation"]["damage"],0)
        for kw in ({"object_mass_kg":11},{"object_volume_dm3":11},
                   {"object_dimension_m":1.6},{"object_range_squares":21},
                   {"object_route_squares":7},{"object_unattended":False},
                   {"hand_available":False},{"path_open":False}):
            with self.subTest(kwargs=kw):
                with self.assertRaises(ValueError):
                    run_scene("Scholar/High",2,"telekinesis",**kw)

    def test_10_unauthored_cross_focus_access_rejected(self):
        for pair,tech in (("Priest/Medium","rapport"),("Priest/Low","rapport"),
                          ("Gifted/High","sound"),("Gifted/Medium","telekinesis"),
                          ("Gifted/Low","rapport"),("Anointed/High","telekinesis"),
                          ("Anointed/Medium","sound"),("Anointed/Low","rapport"),
                          ("Scholar/Low","telekinesis"),("Scholar/High","rapport")):
            with self.subTest(pair=pair,tech=tech):
                with self.assertRaises(UnresolvedDecision):
                    run_scene(pair,2,tech)
        for lvl in (0,4,True):
            with self.assertRaises(ValueError):
                run_scene("Priest/High",lvl,"inspection")
        with self.assertRaises(ValueError):
            run_scene("Priest/High",1,"unknown")

    def test_11_no_author_fixture_counts_as_actual_gm_or_independent_focus(self):
        self.assertEqual((self.report["externally_verified_gm_scenes"],
                          self.report["human_choices_observed"],
                          self.report["full_focus_certificates"],
                          self.report["strict_mvp_exits_met"]),(0,0,0,0))
        for row in self.report["rows"]:
            self.assertEqual(row["status"],STATUS)
            self.assertFalse(row["external_gm_verdict"])
            self.assertEqual(row["human_choices_observed"],0)
            self.assertFalse(row["full_focus_certified"])
            self.assertEqual(row["strict_mvp_exits_met"],0)


if __name__=="__main__":
    unittest.main()
