"""G7-A native seeded combat and censored outcome census safety tests."""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from scripts import b06_g7a_native_terminal_census_v0 as g7a


class G7ANativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cohort=g7a.census(4,start_seed=20,include_trials=True)

    def test_01_only_four_ready_scenarios(self):
        self.assertEqual(len(g7a.ALLOWED),4)
        self.assertEqual(set(g7a.ALLOWED),
                         {(2,3),(2,4),(3,3),(3,4)})
        self.assertEqual(len(self.cohort["cases"]),4)

    def test_02_native_real_turns_source_roster_and_ledger_provenance(self):
        for case in self.cohort["cases"]:
            for trial in case["trials"]:
                with self.subTest(id=trial["scenario_id"],seed=trial["seed"]):
                    self.assertEqual(trial["round_limit"],3)
                    self.assertEqual(trial["party_size"],case["party_size"])
                    self.assertEqual(set(trial["initial_state"]),
                                     set(g7a.ACTORS[case["party_size"]]))
                    self.assertEqual(trial["initial_state"]["hunter"]["source_id"],
                                     "B06-EN-03")
                    self.assertTrue(all(x["source_digest"] for x
                                        in trial["initial_state"].values()))
                    self.assertLessEqual(trial["rounds_completed"],3)
                    self.assertLessEqual(trial["turns_completed"],
                                         3*(case["party_size"]+1))
                    self.assertEqual(len(trial["ledger_sha256"]),64)
                    self.assertEqual(trial["measures"]["round_ends"],
                                     trial["rounds_completed"])
                    self.assertEqual(trial["measures"]["turn_ends"],
                                     trial["turns_completed"])
                    self.assertEqual(trial["measures"]["g2_arrows_launched"],
                                     trial["measures"]["g6d_attested_bow"])
                    self.assertIsNone(trial["hunter_cr"])
                    self.assertFalse(trial["complete_party_pack_certified"])

    def test_03_every_seed_is_classified_exactly_once(self):
        for case in self.cohort["cases"]:
            self.assertEqual(case["seed_count"],4)
            self.assertEqual(sum(case["counts"].values()),4)
            self.assertEqual(set(case["counts"]),set(g7a.OUTCOMES))
            self.assertEqual(case["censored_or_unresolved"],
                             sum(case["counts"][kind] for kind in
                                 ("legal_window_cutoff",
                                  "unresolved_mechanical_branch")))
            self.assertEqual([x["seed"] for x in case["trials"]],
                             list(range(20,24)))
            self.assertEqual([x["seed"] for x in case["trial_digests"]],
                             list(range(20,24)))

    def test_04_never_promote_window_cutoffs_to_complete_wins(self):
        for case in self.cohort["cases"]:
            self.assertIsNone(case["complete_encounter_outcome_rate"])
            self.assertIsNone(case["confidence_interval"])
            self.assertIsNone(case["hunter_cr"])
            for t in case["trials"]:
                self.assertEqual(t["sample_is_complete_encounter"],
                                 t["outcome"]=="hunter_defeat_attested")
                if t["outcome"]=="legal_window_cutoff":
                    self.assertIsNone(t["native_terminal"])
                    self.assertIsNone(t["unresolved"])
                    self.assertEqual(t["rounds_completed"],3)
                if t["outcome"]=="unresolved_mechanical_branch":
                    self.assertIsNotNone(t["unresolved"])
                    self.assertTrue(t["unresolved"]["reason"])

    def test_05_hunter_death_needs_native_terminal_proof(self):
        for case in self.cohort["cases"]:
            for t in case["trials"]:
                if t["outcome"]=="hunter_defeat_attested":
                    self.assertTrue(t["final_state"]["hunter"]["dead"])
                    self.assertEqual(t["final_state"]["hunter"]["hp"],
                                     -t["final_state"]["hunter"]["hp_max"])
                    self.assertEqual(t["native_terminal"]["ending"],
                                     "hunter_defeat_attested")
                    self.assertEqual(t["measures"]["g6d_defeat_terminals"],1)
                else:
                    self.assertEqual(t["measures"]["g6d_defeat_terminals"],0)
                    self.assertIsNone(t["native_terminal"])

    def test_06_all_player_combat_is_from_native_G2_G3_G5_G4(self):
        for case in self.cohort["cases"]:
            for t in case["trials"]:
                self.assertGreaterEqual(t["measures"]["g5_melee_resolved"],0)
                self.assertGreaterEqual(t["measures"]["g4_damage_events"],0)
                self.assertGreaterEqual(t["measures"]["g2_projectile_results"],0)
                self.assertLessEqual(t["measures"]["g4_wounds_created"],
                                     t["measures"]["g4_damage_events"])
                # Resource counts are source-derived: no unlimited Bow ammo.
                self.assertEqual(
                    t["initial_state"]["archer"]["ammunition"]-
                    t["final_state"]["archer"]["ammunition"],
                    t["measures"]["g2_arrows_launched"])

    def test_07_seeded_native_replay_is_byte_stable(self):
        for pair in ((2,3,31),(2,4,32),(3,3,33),(3,4,34)):
            a=g7a.run_trial(*pair)
            b=g7a.run_trial(*pair)
            self.assertEqual(a,b)

    def test_08_paired_dice_do_not_depend_on_roster_or_executed_branch(self):
        # Draws from same actor/round/action/label reappear across level/P3/P4.
        self.assertEqual(g7a.roll(100,2,"hunter","melee:B06-AT-04",
                                   "primary_d20",20),
                         g7a.roll(100,2,"hunter","melee:B06-AT-04",
                                   "primary_d20",20))
        self.assertEqual(g7a.roll(100,1,"vanguard","melee:B06-PC-A-SWORD",
                                   "primary_d20",20),
                         g7a.roll(100,1,"vanguard","melee:B06-PC-A-SWORD",
                                   "primary_d20",20))
        self.assertNotEqual(g7a.roll(100,1,"vanguard","x","primary_d20",20,0),
                            g7a.roll(100,1,"vanguard","x","primary_d20",20,1))

    def test_09_precommitted_rolls_handle_natural_1_and_20(self):
        faces={g7a.roll(seed,1,"hunter","melee:B06-AT-04",
                        "primary_d20",20) for seed in range(200)}
        self.assertIn(1,faces)
        self.assertIn(20,faces)
        self.assertTrue(all(1<=v<=20 for v in faces))

    def test_10_roll_rejects_invalid_inputs_even_boolean_aliases(self):
        tests=((True,1,"a","b","c",20),
               (-1,1,"a","b","c",20),
               (1,0,"a","b","c",20),
               (1,1,"a","b","c",1),
               (1,1,"a","b","c",False),
               (1,1,"","b","c",20))
        for args in tests:
            with self.assertRaises(ValueError):
                g7a.roll(*args)

    def test_11_trial_rejects_unsupported_scenarios_and_invalid_ceiling(self):
        bad=((1,3,0,3),(2,2,0,3),(3,5,0,3),
             (2,3,-1,3),(2,3,True,3),
             (2,3,0,0),(2,3,0,4),(2,3,0,False))
        for level,size,seed,rounds in bad:
            with self.subTest(level=level,size=size,seed=seed,rounds=rounds):
                with self.assertRaises(ValueError):
                    g7a.run_trial(level,size,seed,max_rounds=rounds)

    def test_12_cohort_inputs_bounded_and_no_unreported_rerolls(self):
        for opts in ({"seeds":0},{"seeds":129},{"seeds":True},
                     {"start_seed":-1},{"max_rounds":0},
                     {"max_rounds":4},{"include_trials":0}):
            with self.subTest(opts=opts):
                with self.assertRaises(ValueError):
                    g7a.census(**opts)

    def test_13_census_counts_identical_with_or_without_embedded_evidence(self):
        small=g7a.census(3,start_seed=51,include_trials=True)
        lean=g7a.census(3,start_seed=51,include_trials=False)
        for original,compacted in zip(small["cases"],lean["cases"]):
            self.assertEqual(compacted,
                             {k:v for k,v in original.items() if k!="trials"})
        self.assertTrue(all("trials" not in x for x in lean["cases"]))
        self.assertTrue(all("trial_digests" in x for x in lean["cases"]))

    def test_14_bounded_census_deterministic(self):
        a=g7a.census(2,start_seed=77,include_trials=False)
        b=g7a.census(2,start_seed=77,include_trials=False)
        self.assertEqual(a,b)
        self.assertEqual(g7a.canonical_digest(a),g7a.canonical_digest(b))

    def test_15_incomplete_branches_explicit_no_reclassification(self):
        for case in self.cohort["cases"]:
            self.assertEqual(sum(case["unresolved_reasons"].values()),
                             case["counts"]["unresolved_mechanical_branch"])
            self.assertEqual(
                case["complete_hunter_defeat_terminal_count"],
                case["counts"]["hunter_defeat_attested"])
            for t in case["trials"]:
                self.assertIn(t["outcome"],g7a.OUTCOMES)
                self.assertNotIn("success_rate",t)
                self.assertFalse(t["complete_party_pack_certified"])

    def test_16_source_evidence_not_phased_out_or_cr_encoded(self):
        self.assertTrue(self.cohort["historical_phase3_not_recomputed"])
        self.assertEqual(
            self.cohort["historical_phase3_sha256"],
            "c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b")
        self.assertTrue(self.cohort["no_numeric_cr"])
        self.assertGreater(len(self.cohort["missing_certification_gates"]),0)

    def test_17_cli_json_digest_matches_exact_report(self):
        output=StringIO()
        with redirect_stdout(output):
            g7a.main(["--seeds","1","--start-seed","5"])
        parsed=json.loads(output.getvalue())
        digest=parsed.pop("census_sha256")
        self.assertEqual(digest,g7a.canonical_digest(parsed))
        self.assertEqual(len(parsed["cases"]),4)
        self.assertTrue(all(c["seed_count"]==1 for c in parsed["cases"]))

    def test_18_native_trial_ledger_optional_full_provenance(self):
        t=g7a.run_trial(2,3,8,include_ledger=True)
        self.assertEqual(t["ledger_sha256"],g7a.canonical_digest(t["ledger"]))
        self.assertEqual(len(t["ledger"]),t["ledger"][-1]["index"]+1)
        self.assertEqual(t["measures"]["round_ends"],
                         sum(v["kind"]=="round_end" for v in t["ledger"]))


    def test_19_seed_30_dying_vanguard_uses_native_take_hit(self):
        # Codex P1: the live Vanguard can be <=0 HP without being dead
        # when the Hunter takes its next own turn. Native G0 must assign
        # Take Hit, never precommit an illegal Guard/Dodge.
        for level in (2,3):
            for size in (3,4):
                with self.subTest(level=level,size=size):
                    trial=g7a.run_trial(level,size,30,include_ledger=True)
                    self.assertIn(trial["outcome"],g7a.OUTCOMES)
                    self.assertTrue(trial["ledger"])
                    defenses=[
                        ev for ev in trial["ledger"]
                        if ev["kind"]=="defense_assigned"
                        and ev["detail"]["actor"]=="vanguard"
                        and ev["detail"]["attack_key"].startswith("hunter:vanguard:")
                    ]
                    self.assertTrue(defenses)
                    self.assertTrue(all(
                        ev["detail"]["defense"] in ("guard","dodge","take_hit")
                        for ev in defenses))
                    self.assertTrue(any(
                        ev["detail"]["defense"]=="take_hit" for ev in defenses),
                        "Seed 30 must exercise a Dying Vanguard's Take Hit")
                    self.assertEqual(trial["measures"]["g5_melee_resolved"],
                                     sum(ev["kind"]=="g5_melee_resolved"
                                         for ev in trial["ledger"]))
                    self.assertEqual(trial["measures"]["round_ends"],
                                     trial["rounds_completed"])

    def test_20_full_128_seed_cohort_never_drops_a_trial(self):
        # A valid seed (formerly seed 30) must not raise ValueError and
        # abort a full 128-seed census halfway through. Retain every
        # terminal, cutoff and unresolved branch in the denominator.
        report=g7a.census(128,start_seed=0,include_trials=False)
        self.assertEqual(len(report["cases"]),4)
        self.assertTrue(report["no_numeric_cr"])
        for case in report["cases"]:
            with self.subTest(scenario=case["scenario_id"]):
                self.assertEqual(case["seed_count"],128)
                self.assertEqual(sum(case["counts"].values()),128)
                self.assertEqual(len(case["trial_digests"]),128)
                self.assertEqual([x["seed"] for x in case["trial_digests"]],
                                 list(range(128)))
                self.assertEqual(sum(case["unresolved_reasons"].values()),
                                 case["counts"]["unresolved_mechanical_branch"])
                self.assertEqual(case["complete_hunter_defeat_terminal_count"],
                                 case["counts"]["hunter_defeat_attested"])
                self.assertIsNone(case["complete_encounter_outcome_rate"])
                self.assertIsNone(case["confidence_interval"])
                self.assertIsNone(case["hunter_cr"])


if __name__=="__main__":
    unittest.main()
