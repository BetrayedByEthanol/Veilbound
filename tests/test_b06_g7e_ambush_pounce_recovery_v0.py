"""B06 G7-E genuine source Hunter forest Pounce and long-clock continuity."""
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
from scripts.b06_g7d_protection_frontlines_v0 import run_trial as g7d_trial
from scripts import b06_g7e_ambush_pounce_recovery_v0 as g7e


class G7ETests(unittest.TestCase):
    def test_01_only_source_authorized_paired_forest_cells(self):
        self.assertEqual(len(g7e.CELLS),8)
        self.assertEqual(set(g7e.CELLS),
            {(level,size,mode) for level in (2,3)
             for size in (3,4) for mode in g7e.POLICIES})

    def test_02_forest_is_physical_pounce_approach_not_free_surprise(self):
        for level in (2,3):
            for size in (3,4):
                with self.subTest(level=level,size=size):
                    c=g7e.forest_scene(level=level,size=size,seed=3)
                    e=c.e
                    self.assertEqual(e.order,("hunter","vanguard","guardian",
                                               "archer")+
                                     (("scholar",) if size==4 else ()))
                    self.assertEqual(e.actors["hunter"].occupied,((2,2),(1,2)))
                    self.assertEqual(e.g1.front("hunter"),(3,2))
                    self.assertEqual(e.g1._pounce_approach(
                        "hunter","vanguard",(1,0)),(3,6))
                    self.assertEqual(e.g4.clock.mode,"initiative")
                    self.assertFalse(any(x["kind"]=="action_committed"
                                         for x in e.ledger))
                    self.assertEqual(e.actors["vanguard"].occupied,((6,2),))
                    self.assertIn("no_surprise_bonus",e.policy)
                    e.check()

    def test_03_pounce_uses_exactly_three_native_rigid_steps_and_one_ap(self):
        result=g7e.run_trial(3,4,0,policy="pounce",round_limit=1,
                             exploration_seconds=0,include_ledger=True)
        self.assertIsNotNone(result["opening_bite"])
        self.assertEqual(result["native_pounce_count"],1)
        ls=result["ledger"]
        steps=[x for x in ls if x["kind"]=="g1_movement_step"
               and x["detail"].get("actor")=="hunter"]
        self.assertEqual(len(steps),3)
        self.assertEqual([x["detail"]["new"] for x in steps],
                         [[[3,2],[2,2]],[[4,2],[3,2]],[[5,2],[4,2]]])
        att=[x for x in ls if x["kind"]=="g6_pounce_attested"]
        done=[x for x in ls if x["kind"]=="g6_pounce_resolved"]
        self.assertEqual((len(att),len(done)),(1,1))
        self.assertEqual(done[0]["detail"]["action_index"],
                         att[0]["detail"]["action_index"])
        self.assertFalse(result["universal_surprise_benefit_applied"])

    def test_04_ordinary_approach_has_no_free_pounce_or_balance(self):
        r=g7e.run_trial(3,4,0,policy="ordinary_approach",
                        round_limit=1,exploration_seconds=0,
                        include_ledger=True)
        self.assertEqual(r["native_pounce_count"],0)
        self.assertFalse(any(x["kind"].startswith("g6_pounce")
                             for x in r["ledger"]))
        self.assertEqual(sum(x["kind"]=="g1_movement_step" and
                            x["detail"].get("actor")=="hunter"
                            for x in r["ledger"]),3)
        self.assertTrue(any(x["kind"]=="g5_melee_resolved"
                            and x["detail"].get("attacker")=="hunter"
                            for x in r["ledger"]))

    def test_05_paired_opening_bite_original_attack_dice(self):
        for seed in range(16):
            with self.subTest(seed=seed):
                a=g7e.run_trial(3,3,seed,policy="pounce",round_limit=1,
                                exploration_seconds=0)
                b=g7e.run_trial(3,3,seed,policy="ordinary_approach",
                                round_limit=1,exploration_seconds=0)
                self.assertIsNotNone(a["opening_bite"])
                self.assertIsNotNone(b["opening_bite"])
                for key in ("attack_face","hit","source_damage_face",
                            "source_confirmation_face","source_critical_dice"):
                    self.assertEqual(a["opening_bite"][key],
                                     b["opening_bite"][key])

    def test_06_missed_bite_can_still_genuinely_knock_down(self):
        matched=False
        for seed in range(128):
            r=g7e.run_trial(3,3,seed,policy="pounce",round_limit=1,
                            exploration_seconds=0,include_ledger=True)
            opening=r["opening_bite"]
            if (opening is not None and opening["hit"] is False
                    and opening["outcome"]["balance"]=="prone"):
                matched=True
                self.assertTrue(any(x["kind"]=="g6_pounce_prone"
                                    for x in r["ledger"]))
                self.assertFalse(any(x["kind"]=="g4_profile_hit"
                                     and x["detail"].get("attacker")=="hunter"
                                     for x in r["ledger"]))
                self.assertTrue(any(
                    x["kind"]=="g6_pounce_balance"
                    and x["detail"]["outcome"]=="prone"
                    for x in r["ledger"]))
                break
        self.assertTrue(matched,"Expected a real missed-Bite force win")

    def test_07_hit_causes_only_native_G4_injury_and_G44_toxin(self):
        found=False
        for seed in range(64):
            r=g7e.run_trial(3,4,seed,policy="pounce",round_limit=1,
                            exploration_seconds=0,include_ledger=True)
            if (r["opening_bite"] is not None and
                    r["opening_bite"]["hit"]):
                found=True
                self.assertTrue(any(x["kind"]=="g4_profile_hit" and
                                    x["detail"].get("attacker")=="hunter"
                                    for x in r["ledger"]))
                self.assertEqual(sum(x["kind"]=="g6_pounce_resolved"
                                     for x in r["ledger"]),1)
                self.assertTrue(any(x["kind"]=="g45_attested_hit" and
                                    x["detail"].get("profile")=="B06-AT-06"
                                    for x in r["ledger"]))
                self.assertLessEqual(sum(
                    x["kind"]=="g44_hunter_accepted"
                    and x["detail"].get("recipient")=="vanguard"
                    for x in r["ledger"]),1)
                break
        self.assertTrue(found,"Expected a native Pounce hit")

    def test_08_native_round2_regeneration_and_no_ghost_turn(self):
        r=g7e.run_trial(3,4,5,policy="pounce",round_limit=2,
                        exploration_seconds=0,include_ledger=True)
        self.assertIsNone(r["unresolved"])
        self.assertLessEqual(r["rounds_completed"],2)
        self.assertEqual(r["turns_completed"],
                         r["rounds_completed"]*5)
        self.assertEqual(sum(x["kind"]=="round_end" for x in r["ledger"]),
                         r["rounds_completed"])
        self.assertEqual(sum(x["kind"]=="round_begin" for x in r["ledger"]),
                         r["rounds_completed"])
        self.assertEqual(sum(x["kind"]=="regeneration_step" and
                             x["detail"].get("actor")=="vanguard"
                             for x in r["ledger"]),r["rounds_completed"])

    def test_09_cannot_time_jump_with_an_unresolved_native_pounce(self):
        c=g7e.forest_scene(level=3,size=3,seed=7)
        e=c.e
        c.bridge.start_next_turn(RegenerationChoice())
        c.begin_pounce("hunter","vanguard",((1,0),)*3,
                       defense="take_hit")
        with self.assertRaises(UnresolvedDecision):
            g7e._clock_handoff(c,21600)
        self.assertEqual(e.g4.clock.mode,"initiative")
        self.assertEqual(e.g4.clock.world_seconds,0)
        self.assertFalse(any(x["kind"]=="g4_six_hour_recovery"
                             for x in e.ledger))

    def test_10_real_10min_and_30min_hunter_stages_after_handoff(self):
        found=False
        for seed in range(64):
            r=g7e.run_trial(3,3,seed,policy="pounce",
                            round_limit=1,exploration_seconds=7200,
                            include_ledger=True)
            if any(x["kind"]=="g44_hunter_accepted" for x in r["ledger"]):
                found=True
                self.assertIsNotNone(r["clock_handoff"])
                self.assertEqual(r["clock_handoff"]["world_seconds_after"],7200)
                milestones=[x for x in r["ledger"] if
                            x["kind"]=="g44_hunter_milestone"]
                self.assertTrue(milestones)
                self.assertTrue(all(x["detail"]["round_begin"] is None
                                    for x in milestones))
                self.assertFalse(any(x["kind"]=="g4_six_hour_recovery"
                                     for x in r["ledger"]))
                self.assertEqual(r["clock_handoff"]["mode"],"exploration")
                break
        self.assertTrue(found,"Native poison case should reach long milestones")

    def test_11_exact_six_hour_recovery_only_at_earned_checkpoint(self):
        witness=g7e.run_trial(3,4,0,policy="pounce",round_limit=1,
                              exploration_seconds=21600,include_ledger=True)
        self.assertIsNotNone(witness["clock_handoff"])
        events=[x for x in witness["ledger"]
                if x["kind"]=="g4_six_hour_recovery"]
        self.assertEqual(len(events),5)
        self.assertTrue(all(0 < x["detail"]["world_seconds"]<=21600
                            for x in events))
        self.assertEqual(len({x["detail"]["checkpoint_id"] for x in events}),5)
        self.assertEqual(witness["clock_handoff"]["world_seconds_after"],21600)
        self.assertTrue(witness["clock_handoff"]["not_a_combat_terminal"])
        self.assertFalse(witness["complete_party_pack_certified"])

    def test_12_early_7200s_handoff_never_grants_six_hour_rewards(self):
        r=g7e.run_trial(2,3,1,policy="ordinary_approach",
                        round_limit=1,exploration_seconds=7200)
        self.assertIsNotNone(r["clock_handoff"])
        self.assertEqual(r["clock_handoff"]["recovery_indices"],[])
        self.assertIsNone(r["hunter_cr"])

    def test_13_no_noncompleted_round_is_promoted_to_exploration(self):
        # Every failed mechanical branch must stop before clock transfer.
        for seed in range(16):
            r=g7e.run_trial(3,4,seed,policy="pounce",
                            round_limit=2,exploration_seconds=7200)
            if r["unresolved"] is not None:
                self.assertIsNone(r["clock_handoff"])
                self.assertEqual(r["outcome"],"unresolved_mechanical_branch")

    def test_14_census_all_eight_128_seed_cells_exclusive_and_no_CR(self):
        c=g7e.census(128,exploration_seconds=0)
        self.assertEqual(len(c["cells"]),8)
        for row in c["cells"]:
            self.assertEqual(sum(row["counts"].values()),128)
            self.assertEqual(len(row["trial_digests"]),128)
            self.assertEqual([x["seed"] for x in row["trial_digests"]],
                             list(range(128)))
            self.assertIsNone(row["sampled_win_rate"])
            self.assertIsNone(row["ci95"])
            self.assertIsNone(row["hunter_cr"])
        self.assertIsNone(c["creature_challenge_rating"])
        self.assertEqual(c["historical_phase3_sha256"],g7e.PHASE3_SHA)

    def test_15_hash_determinism_and_inherited_G7D_fixture(self):
        self.assertEqual(g7e.census(2,start_seed=10),
                         g7e.census(2,start_seed=10))
        self.assertEqual(g7d_trial(3,4,0,policy="control"),
                         g7d_trial(3,4,0,policy="control"))
        a=mixed_scene(level=3,size=4,seed=1)
        self.assertEqual(a.e.actors["hunter"].occupied,((3,2),(4,2)))

    def test_16_unknown_ambush_bonuses_never_silently_applied(self):
        for seed in (0,1,2):
            for mode in g7e.POLICIES:
                r=g7e.run_trial(3,4,seed,policy=mode,
                                round_limit=1,exploration_seconds=0)
                self.assertEqual(r["opening"],"forest_ambush_geometry_only")
                self.assertFalse(r["universal_surprise_benefit_applied"])
                self.assertEqual(r["native_pounce_count"],int(mode=="pounce"))

    def test_17_bounds_enforced_before_native_scene(self):
        for kwargs in ({"level":1},{"size":5},{"seed":-1},{"seed":True},
                       {"policy":"surprise_action"},{"round_limit":3},
                       {"exploration_seconds":21601},
                       {"exploration_seconds":-1},{"include_ledger":1}):
            with self.subTest(kwargs=kwargs):
                args={"level":3,"size":4,"seed":0}
                args.update(kwargs)
                with self.assertRaises(ValueError):
                    g7e.run_trial(**args)
        for kwargs in ({"seeds":0},{"seeds":True},{"seeds":129},
                       {"start_seed":-1},{"round_limit":3},
                       {"exploration_seconds":21601},{"include_trials":0}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    g7e.census(**kwargs)

    def test_18_cli_digest_json_and_no_sampled_win_rate(self):
        buf=StringIO()
        with redirect_stdout(buf):
            g7e.main(["--seeds","1","--exploration-seconds","0"])
        result=json.loads(buf.getvalue())
        digest=result.pop("census_sha256")
        self.assertEqual(digest,canonical_digest(result))
        self.assertEqual(result["complete_party_packs_certified"],0)

    def test_19_source_ledger_digest_includes_long_clock(self):
        r=g7e.run_trial(3,4,1,policy="pounce",round_limit=1,
                        exploration_seconds=21600,include_ledger=True)
        self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))
        self.assertTrue(any(x["kind"]=="g42_initiative_exited"
                            for x in r["ledger"]))
        self.assertTrue(any(x["kind"]=="g42_exploration_advanced"
                            for x in r["ledger"]))

    def test_20_observation_handoff_not_full_party_terminal(self):
        for mode in g7e.POLICIES:
            r=g7e.run_trial(3,4,0,policy=mode,round_limit=1,
                            exploration_seconds=21600)
            self.assertIsNone(r["hunter_cr"])
            self.assertFalse(r["complete_party_pack_certified"])
            self.assertTrue(r["clock_handoff"]["not_a_combat_terminal"])
            self.assertIn(r["outcome"],g7e.OUTCOMES)


if __name__=="__main__":
    unittest.main()
