"""B05/B06 a continuous source-paid three-scene adventure, never GM certification."""
from collections import Counter
import unittest

from scripts.b05_b06_integrated_noncombat_adventure_v0 import (
    STATUS, DETOUR_SECONDS, play, roster,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision


class IntegratedNoncombatAdventureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=roster()
        cls.rows={(r["pairing"],r["level"],r["plan"]):r
                  for r in cls.result["rows"]}

    def row(self, pair, level, plan):
        return self.rows[pair,level,plan]

    def test_01_36_source_level_slots_and_80_connected_three_scene_forks(self):
        self.assertEqual((12,36,80,240),(
            self.result["structural_pairings"],
            self.result["pairing_level_slots"],
            self.result["connected_three_scene_author_forks"],
            self.result["fixture_scenes_count"]))
        self.assertEqual(len(self.rows),80)
        self.assertEqual(Counter(r["plan"] for r in self.result["rows"]),
                         {"evidence":36,"inspection":36,"special":8})
        for pair in ("Priest/High","Priest/Medium","Priest/Low",
                     "Scholar/High","Scholar/Medium","Scholar/Low",
                     "Gifted/High","Gifted/Medium","Gifted/Low",
                     "Anointed/High","Anointed/Medium","Anointed/Low"):
            for level in (1,2,3):
                self.assertIn((pair,level,"evidence"),self.rows)
                self.assertIn((pair,level,"inspection"),self.rows)

    def test_02_one_native_clock_sequential_scenes_and_single_source(self):
        for r in self.result["rows"]:
            with self.subTest(pair=r["pairing"],level=r["level"],plan=r["plan"]):
                scenes=r["scenes"]
                self.assertEqual([s["scene"] for s in scenes],[
                    "1-crossing","2-investigation","3-public-record"])
                self.assertEqual(scenes[0]["start_seconds"],0)
                self.assertEqual(scenes[0]["end_seconds"],scenes[1]["start_seconds"])
                self.assertEqual(scenes[1]["end_seconds"],scenes[2]["start_seconds"])
                self.assertEqual(scenes[-1]["end_seconds"],r["world_seconds_elapsed"])
                self.assertGreater(r["world_seconds_elapsed"],0)
                self.assertEqual(len(r["native_ledger_sha256"]),64)
                self.assertEqual(len(r["source_sha256"]),64)
                self.assertGreater(r["native_event_count"],0)
                self.assertIn("g42_exploration_advanced",r["native_event_kinds"])
                self.assertEqual(r["source_vp_initial"]-r["source_vp_available"],
                                 r["source_vp_spent"])
                self.assertEqual(r["source_vp_committed"],0)
                self.assertEqual(r["native_turns_taken"],
                                 len(r["source_paid_techniques"]))
                if r["native_turns_taken"]:
                    for k in ("action_committed","vp_transition",
                              "g42_initiative_entered","g42_initiative_exited"):
                        self.assertIn(k,r["native_event_kinds"])

    def test_03_evidence_vs_inspection_role_alternatives_change_information(self):
        e=self.row("Priest/High",1,"evidence")
        i=self.row("Priest/High",1,"inspection")
        self.assertTrue(e["shared_consequences"]["medical_diagnosis"])
        self.assertFalse(e["shared_consequences"]["observed_magic_signature"])
        self.assertEqual(e["scenes"][2]["medical_evidence_support"],2)
        self.assertFalse(i["shared_consequences"]["medical_diagnosis"])
        self.assertTrue(i["shared_consequences"]["observed_magic_signature"])
        self.assertEqual(i["scenes"][2]["medical_evidence_support"],0)
        self.assertEqual((e["source_vp_spent"],i["source_vp_spent"]),(0,2))
        self.assertEqual((e["world_seconds_elapsed"],i["world_seconds_elapsed"]),
                         (540,270))
        self.assertTrue(e["shared_consequences"]["public_log_access"])
        self.assertFalse(i["shared_consequences"]["public_log_access"])

    def test_04_real_failed_route_produces_physical_detour_and_elapsed_cost(self):
        normal=play("Scholar/Low",2,"evidence",faces=(12,12,12,12))
        failed=play("Scholar/Low",2,"evidence",faces=(1,12,12,12))
        self.assertEqual(normal["shared_consequences"]["route"],"direct")
        self.assertEqual(failed["shared_consequences"]["route"],"detour")
        self.assertEqual(failed["scenes"][0]["detour_seconds"],DETOUR_SECONDS)
        self.assertEqual(failed["world_seconds_elapsed"]-normal["world_seconds_elapsed"],
                         DETOUR_SECONDS)
        self.assertEqual(failed["source_vp_spent"],0)
        self.assertFalse(failed["scenes"][0]["choice"]["success"])

    def test_05_failed_diagnosis_removes_only_author_declared_evidence_support(self):
        original=play("Priest/High",1,"evidence",faces=(12,12,12,12))
        no_proof=play("Priest/High",1,"evidence",faces=(12,1,12,12))
        self.assertEqual((original["scenes"][2]["medical_evidence_support"],
                          no_proof["scenes"][2]["medical_evidence_support"]),(2,0))
        self.assertEqual(original["scenes"][2]["choice"]["total"]-
                         no_proof["scenes"][2]["choice"]["total"],2)
        self.assertFalse(no_proof["shared_consequences"]["medical_diagnosis"])
        self.assertEqual(no_proof["scenes"][2]["source_of_modifier"],None)

    def test_06_high_priest_rapport_is_paid_and_animal_still_uncompelled(self):
        for level in (1,2,3):
            r=self.row("Priest/High",level,"special")
            self.assertEqual((r["native_turns_taken"],r["source_vp_spent"]),(1,2))
            self.assertEqual(r["source_paid_techniques"],["Woodland Rapport"])
            self.assertEqual(r["scenes"][0]["animal_first_contact_check"]["situational"],2)
            self.assertEqual(r["scenes"][0]["technique_actions"][0]["ap_spent"],20)
            self.assertFalse(r["scenes"][0]["technique_actions"][0]
                             ["effect"]["animal_compelled"])
            self.assertIn(r["shared_consequences"]["route"],("direct","detour"))
        lost=play("Priest/High",1,"special",faces=(1,12,12,1))
        self.assertFalse(lost["scenes"][0]["animal_first_contact_check"]["success"])
        self.assertEqual(lost["scenes"][0]["animal_first_contact_check"]["situational"],2)
        self.assertFalse(lost["scenes"][0]["technique_actions"][0]["effect"]["animal_compelled"])

    def test_07_high_scholar_sound_and_telekinesis_coexist_without_free_persuasion(self):
        for level in (1,2,3):
            r=self.row("Scholar/High",level,"special")
            self.assertEqual(r["source_paid_techniques"],
                             ["Minor Telekinesis","Phantom Sound"])
            self.assertEqual(r["source_vp_spent"],3)
            self.assertEqual(r["native_turns_taken"],2)
            self.assertTrue(r["shared_consequences"]["loose_sample_retrieved"])
            self.assertTrue(r["shared_consequences"]["signal_emitted"])
            self.assertFalse(r["shared_consequences"]["medical_diagnosis"])
            self.assertEqual(r["scenes"][2]["medical_evidence_support"],0)
            self.assertFalse(r["scenes"][2]["technique_actions"][0]
                             ["effect"]["npc_attention_forced"])

    def test_08_medium_scholar_tk_route_and_sample_share_vp_across_two_turns(self):
        for level in (2,3):
            r=self.row("Scholar/Medium",level,"special")
            self.assertEqual(r["source_paid_techniques"],
                             ["Minor Telekinesis","Minor Telekinesis"])
            self.assertEqual(r["source_vp_spent"],4)
            self.assertEqual(r["native_turns_taken"],2)
            self.assertEqual(r["shared_consequences"]["route"],"direct")
            self.assertEqual(r["scenes"][0]["choice"]["approach"],
                             "recover_loose_annotated_map_marker")
            self.assertTrue(r["shared_consequences"]["loose_sample_retrieved"])
            self.assertFalse(r["shared_consequences"]["medical_diagnosis"])

    def test_09_cross_focus_invalid_special_and_fake_level_fail_closed(self):
        for pair in ("Gifted/High","Gifted/Medium","Gifted/Low","Priest/Low",
                     "Scholar/Low","Anointed/High","Anointed/Medium",
                     "Anointed/Low","Priest/Medium"):
            with self.subTest(pair=pair):
                with self.assertRaises(UnresolvedDecision):
                    play(pair,1,"special")
        with self.assertRaises(UnresolvedDecision):
            play("Scholar/Medium",1,"special")
        for level in (0,4,True,1.0,"2"):
            with self.subTest(level=level):
                with self.assertRaises(ValueError):
                    play("Scholar/High",level)
        for plan in ("invented",{"route":"success"},None):
            with self.subTest(plan=str(plan)):
                with self.assertRaises(ValueError):
                    play("Scholar/High",1,plan)

    def test_10_malformed_faces_and_low_priest_variants_are_checked(self):
        for faces in ((12,12,12), (12,12,12,0), (True,12,12,12),
                      (12,12,21,12),"12 12 12 12",None):
            with self.subTest(faces=str(faces)):
                with self.assertRaises(ValueError):
                    play("Scholar/High",1,faces=faces)
        with self.assertRaises(ValueError):
            play("Priest/High",1,low_variant="B")
        with self.assertRaises(ValueError):
            play("Priest/Low",1,low_variant="X")
        b=play("Priest/Low",1,low_variant="B")
        self.assertEqual(b["source_scope"],"LOW_PRIEST_G0_ABILITIES_ONLY")
        self.assertEqual(b["native_turns_taken"],0)
        self.assertFalse(b["independent_focus_certified"])

    def test_11_different_faces_change_social_consequence_no_magic_mental_effect(self):
        pass_case=play("Anointed/High",2,"inspection",faces=(12,12,20,12))
        fail_case=play("Anointed/High",2,"inspection",faces=(12,12,1,12))
        self.assertTrue(pass_case["shared_consequences"]["public_log_access"])
        self.assertFalse(fail_case["shared_consequences"]["public_log_access"])
        self.assertEqual(pass_case["source_vp_spent"],fail_case["source_vp_spent"])
        self.assertEqual(pass_case["source_vp_spent"],2)
        self.assertFalse(pass_case["scenes"][2]["choice"]["training"]=="Persuasion")
        self.assertTrue(pass_case["scenes"][2]["npc_disposition_not_compelled"])

    def test_12_no_real_human_gm_sessions_certificates_or_unearned_level_awards(self):
        for r in self.result["rows"]:
            self.assertEqual(r["status"],STATUS)
            self.assertEqual(r["externally_verified_gm_scenes"],0)
            self.assertEqual(r["human_choices_observed"],0)
            self.assertEqual(r["human_session_count"],0)
            self.assertEqual(r["strict_mvp_exits_met"],0)
            self.assertFalse(r["independent_focus_certified"])
            self.assertNotIn("level_awarded",r)
            self.assertNotIn("hunter_cr",r)
        self.assertEqual((self.result["externally_verified_gm_scenes"],
                          self.result["human_session_count"],
                          self.result["full_focus_certificates"],
                          self.result["strict_mvp_exits_met"]),(0,0,0,0))

    def test_13_determinism_and_native_receipt_replay(self):
        a=play("Scholar/High",1,"special")
        b=play("Scholar/High",1,"special")
        self.assertEqual(a["native_ledger_sha256"],b["native_ledger_sha256"])
        self.assertEqual(a["scenes"],b["scenes"])
        self.assertEqual(a["source_sha256"],b["source_sha256"])


if __name__ == "__main__":
    unittest.main()
