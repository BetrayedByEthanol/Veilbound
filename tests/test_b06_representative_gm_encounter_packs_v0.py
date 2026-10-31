"""B06 GM pack source-native terminals, tactical countercases and aftermath gates."""
from collections import Counter
import unittest

from scripts.b06_representative_gm_encounter_packs_v0 import (
    GM_BRIEFS, HUNTER_FIELD, HUNTER_WATCH,
    encounter_pack, run_g8, run_hunter_terminals, run_hunter_tactic,
)


class RepresentativeGMEncounterPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=encounter_pack(seed=17)
        cls.rows=cls.report["rows"]

    def _cell(self, gm_pack, level, policy, *, size=4):
        matches=[r for r in self.rows
                 if (r["gm_pack"],r["level"],r["policy"],r["party_size"])
                 ==(gm_pack,level,policy,size)]
        self.assertEqual(len(matches),1)
        return matches[0]

    def test_01_four_gm_briefs_three_original_enemies_36_policy_cases(self):
        r=self.report
        self.assertEqual((3,4,36,18,6,12),(
            r["enemy_families"],r["authored_gm_scenarios"],
            r["source_native_policy_observations"],
            r["g8_soldier_sentry_terminal_cases"],
            r["g7h_hunter_terminal_cases"],
            r["g7f_hunter_field_and_protective_cases"]))
        self.assertEqual(r["terminal_or_censor_denominator"],36)
        self.assertEqual(len(self.rows),36)
        self.assertEqual(set(GM_BRIEFS),{
            "soldier_gate","sentry_shrine_cold","sentry_shrine_prepared",
            "hunter_forest"})
        self.assertEqual(Counter(x["source_executor"] for x in self.rows),
                         {"B06_G8":18,"B06_G7H":6,"B06_G7F":12})
        self.assertEqual(sum(r["source_evidence_grade_counts"].values()),36)
        self.assertEqual(sum(r["outcome_counts_including_censored"].values()),36)

    def test_02_each_soldier_sentry_state_has_three_authentic_L2_L3_terminals(self):
        for gm_pack in ("soldier_gate","sentry_shrine_cold",
                        "sentry_shrine_prepared"):
            for level in (2,3):
                for policy in ("party_victory","party_defeat",
                               "opposed_withdrawal"):
                    with self.subTest(gm_pack=gm_pack,level=level,policy=policy):
                        cell=self._cell(gm_pack,level,policy)
                        self.assertEqual(cell["source_enemy_id"],
                                         GM_BRIEFS[gm_pack]["source_enemy"])
                        self.assertTrue(cell["bounded_native_terminal_attested"])
                        self.assertFalse(cell["censored_or_unresolved"])
                        self.assertEqual(len(cell["native_ledger_sha256"]),64)
                        self.assertGreater(cell["rounds_completed"],0)
                        self.assertGreater(cell["native_event_count"],0)
                        self.assertIn("foe",cell["initial_source_state"])
                        self.assertEqual(len(cell["aftermath"]["source_digests"]),5)
                        if policy=="party_victory":
                            self.assertFalse(cell["aftermath"]["enemy_alive_at_terminal_or_cutoff"])
                        elif policy=="party_defeat":
                            self.assertEqual(len(cell["aftermath"]["party_dead"]),4)
                        else:
                            self.assertTrue(cell["aftermath"]["enemy_alive_at_terminal_or_cutoff"])
                            self.assertEqual(cell["native_exit_events"],4)

    def test_03_sentry_cold_and_prepared_retain_real_source_start_state(self):
        for level in (2,3):
            cold=self._cell("sentry_shrine_cold",level,"party_victory")
            ready=self._cell("sentry_shrine_prepared",level,"party_victory")
            self.assertNotEqual(cold["native_ledger_sha256"],
                                ready["native_ledger_sha256"])
            self.assertEqual(cold["source_enemy_id"],ready["source_enemy_id"])
            self.assertNotEqual(cold["initial_source_state"]["foe"]["vp"],
                                ready["initial_source_state"]["foe"]["vp"])
            self.assertGreater(cold["real_vp_transitions"],0)

    def test_04_hunter_three_native_L2_L3_terminal_proofs(self):
        for level in (2,3):
            win=self._cell("hunter_forest",level,"mixed_victory_rite")
            loss=self._cell("hunter_forest",level,"hunter_multitarget_defeat")
            exit=self._cell("hunter_forest",level,
                            "opposed_living_hunter_withdrawal")
            self.assertEqual({win["outcome"],loss["outcome"],exit["outcome"]},
                             {"hunter_defeat_attested","party_defeat_attested",
                              "party_withdrawal_attested"})
            for r in (win,loss,exit):
                self.assertTrue(r["bounded_native_terminal_attested"])
                self.assertFalse(r["censored_or_unresolved"])
                self.assertEqual(r["source_enemy_id"],"B06-EN-03")
                self.assertEqual(len(r["aftermath"]["source_digests"]),5)
                self.assertGreater(r["real_damage_packets"],0)
            self.assertFalse(win["aftermath"]["enemy_alive_at_terminal_or_cutoff"])
            self.assertEqual(len(loss["aftermath"]["party_dead"]),4)
            self.assertEqual(exit["native_exit_events"],4)
            self.assertTrue(exit["aftermath"]["enemy_alive_at_terminal_or_cutoff"])
            self.assertEqual(win["source_decisions"]["chosen_R_rites"],1)
            self.assertGreater(exit["source_decisions"]
                               ["genuine_hunter_pursuit_steps"],0)

    def test_05_hunter_forest_two_geometry_policies_and_P3_P4_L2_L3(self):
        for level in (2,3):
            for size in (3,4):
                a=self._cell("hunter_forest",level,"forest_ordinary",size=size)
                b=self._cell("hunter_forest",level,"forest_pounce",size=size)
                self.assertEqual(a["opening_source"],
                                 "forest_geometry_pounce_vs_ordinary")
                self.assertEqual(b["opening_source"],
                                 "forest_geometry_pounce_vs_ordinary")
                self.assertNotEqual(a["native_ledger_sha256"],
                                    b["native_ledger_sha256"])
                self.assertEqual(a["native_pounces"],0)
                self.assertGreater(b["native_pounces"],0)
                self.assertEqual(a["party_size"],size)
                self.assertEqual(b["party_size"],size)

    def test_06_hunter_warned_and_protective_tactics_not_generalized(self):
        self.assertEqual(set(HUNTER_WATCH),
                         {"warned_party_exit","protected_control",
                          "reactive_shield","prepared_body"})
        for policy in HUNTER_WATCH:
            r=self._cell("hunter_forest",3,policy)
            self.assertEqual((r["level"],r["party_size"]),(3,4))
            self.assertEqual(r["opening_source"],
                             "warned_protection_or_source_exit")
            self.assertEqual(len(r["native_ledger_sha256"]),64)
        for r in self.rows:
            if r["source_executor"]=="B06_G7F":
                self.assertEqual(r["censored_or_unresolved"],
                                 not r["bounded_native_terminal_attested"])
                self.assertEqual(r["aftermath"]["native_hp_changes_only"],True)
                self.assertIsNone(r["aftermath"]["safe_for_six_hour_rest"])

    def test_07_attrition_and_aftermath_are_real_not_invented_recovery(self):
        for r in self.rows:
            with self.subTest(pack=r["gm_pack"],policy=r["policy"],level=r["level"]):
                self.assertIsNone(r["hunter_cr"])
                self.assertIsNone(r["sampled_win_rate"])
                self.assertFalse(r["human_gm_observed"])
                self.assertIsNone(r["aftermath"]["safe_for_six_hour_rest"])
                self.assertIsNone(r["aftermath"]["long_term_pursuit_resolved"])
                self.assertTrue(r["aftermath"]["next_gm_gate"])
                if r["source_executor"]!="B06_G7F":
                    a=r["aftermath"]
                    self.assertEqual(set(a["party_hp"]),set(a["party_vigor"]))
                    self.assertEqual(set(a["party_hp"]),set(a["party_wounds"]))
                    self.assertEqual(set(a["party_hp"]),set(a["party_vp_available"]))
                    self.assertEqual(set(a["party_hp"]),set(a["party_ammunition"]))

    def test_08_unsupported_cross_source_cells_and_levels_fail_closed(self):
        for func,args in (
            (run_g8,("hunter_forest",2)),
            (run_g8,("soldier_gate",1)),
            (run_g8,("soldier_gate",True)),
            (run_g8,("unknown",2)),
            (run_hunter_tactic,(2,3,"reactive_shield")),
            (run_hunter_tactic,(3,3,"prepared_body")),
            (run_hunter_tactic,(2,4,"fake_hunter_stealth")),
            (run_hunter_tactic,(3,2,"forest_pounce")),
            (run_hunter_tactic,(True,4,"forest_ordinary")),
            (run_hunter_terminals,(1,)),
        ):
            with self.subTest(func=func.__name__,args=str(args)):
                with self.assertRaises(ValueError):
                    if func is run_g8:
                        func(*args,mode="party_victory")
                    else:
                        func(*args)
        with self.assertRaises(ValueError):
            run_g8("soldier_gate",2,mode="fake_victory")
        with self.assertRaises(ValueError):
            encounter_pack(seed=-1)
        with self.assertRaises(ValueError):
            encounter_pack(seed=True)

    def test_09_deterministic_single_source_replay_g8(self):
        original=self._cell("soldier_gate",2,"party_victory")
        replay=run_g8("soldier_gate",2,mode="party_victory",seed=17)
        self.assertEqual(original["native_ledger_sha256"],
                         replay["native_ledger_sha256"])
        self.assertEqual(original["aftermath"],replay["aftermath"])

    def test_10_no_human_GM_sampling_CR_or_full_pack_certification(self):
        r=self.report
        self.assertEqual((r["human_sessions_observed"],
                          r["representative_player_gm_samples"],
                          r["independent_focus_certifications"],
                          r["strict_mvp_exit_gates_met"]),(0,0,0,0))
        self.assertFalse(r["representative_difficulty_accepted"])
        self.assertFalse(r["source_bounded_terminal_certification_is_full_gm_pack"])
        self.assertIsNone(r["hunter_challenge_rating"])
        self.assertIsNone(r["sampled_win_rate"])
        self.assertEqual(len(r["native_source_sha256"]),
                         len(set(x["native_ledger_sha256"] for x in self.rows)))


if __name__=="__main__":
    unittest.main()
