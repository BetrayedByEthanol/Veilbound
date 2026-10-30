"""Native G4.2 noncombat Destiny from real Anointed Lesser G5 scenes."""
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.b05_anointed_native_noncombat_destiny_v0 import (
    FOCUSES,LEVELS,OPPONENTS,POLICIES,STORY_EVENT_ID,
    run_matrix,run_policy,attest_policy,_spent_lesser_scene,
)
from scripts.b05_anointed_native_destiny_exploration_v0 import (
    AnointedDestinyExploration,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def entries(report,kind):
    return [ev for ev in report["ledger"] if ev["kind"]==kind]


class NativeAnointedNoncombatDestinyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports=run_matrix(seed=0)
        cls.by_key={(r["focus"],r["level"],r["opponent"],r["policy"]):r
                    for r in cls.reports}

    def test_01_all_72_source_bound_policies_are_bounded_not_focus_certificates(self):
        self.assertEqual(72,len(self.reports))
        self.assertEqual(72,len(self.by_key))
        self.assertEqual(72,len(FOCUSES)*len(LEVELS)*len(OPPONENTS)*len(POLICIES))
        for r in self.reports:
            self.assertFalse(r["independent_focus_certified"])
            self.assertFalse(r["noncombat_mission_gm_certified"])
            self.assertFalse(r["representative_play_certified"])
            self.assertIsNone(r["sampled_win_rate"])

    def test_02_every_noncombat_ledger_starts_with_one_real_paid_lesser_and_hit(self):
        for r in self.reports:
            with self.subTest(case=(r["focus"],r["level"],r["opponent"],r["policy"])):
                m=r["metrics"]
                self.assertEqual((2,1,2,1,1),(
                    m["destiny_initial"],m["destiny_after_real_lesser"],
                    m["destiny_after_noncombat"],m["lesser_source_destiny_spent"],
                    m["source_signature_receipts"]))
                self.assertEqual(1,m["source_g5_enemy_hits"])
                self.assertEqual(1,len(entries(r,"g5_melee_sequence_attested")))
                self.assertEqual(1,len(entries(r,"g5_melee_resolved")))
                self.assertEqual(1,len(entries(r,"g4_damage_applied")))
                self.assertEqual(1,len(entries(r,"g42_initiative_entered")))
                self.assertEqual(1,len(entries(r,"g42_initiative_exited")))
                self.assertEqual(1,len(entries(r,"b05_anointed_destiny_clock_bound")))
                self.assertEqual({"High":"AH","Medium":"AM","Low":"AL"}[r["focus"]],
                                 r["source_ids"]["anointed"])
                self.assertEqual({"soldier":"B06-EN-02","sentry_prepared":"B06-EN-01"}[
                    r["opponent"]],r["source_ids"]["foe"])
                self.assertEqual(0,m["synthetic_post_exit_regeneration_steps"])

    def test_03_clock_partial_retains_359_min_and_awards_at_exact_360(self):
        for focus in FOCUSES:
            for level in LEVELS:
                for foe in OPPONENTS:
                    m=self.by_key[focus,level,foe,"clock_partial"]["metrics"]
                    with self.subTest(focus=focus,level=level,foe=foe):
                        self.assertEqual((1,359),(m["interim_destiny"],
                                                  m["interim_remainder_minutes"]))
                        self.assertEqual(21600,m["world_seconds"])
                        self.assertEqual(1,m["world_clock_destiny_recovered"])
                        self.assertEqual(0,m["gm_story_destiny_awarded"])
                        self.assertEqual((0,0),(m["six_hour_remainder_minutes"],
                                               m["partial_minute_seconds"]))
                        self.assertEqual([],m["gm_mission_awards"])

    def test_04_story_beat_is_external_gm_recognized_unique_and_capped(self):
        for focus in FOCUSES:
            for level in LEVELS:
                r=self.by_key[focus,level,"soldier","gm_recognized"]
                m=r["metrics"]
                self.assertEqual([STORY_EVENT_ID],m["gm_mission_awards"])
                self.assertTrue(m["blocked_duplicate_gm_award"])
                self.assertEqual((1,0),(m["gm_story_destiny_awarded"],
                                       m["world_clock_destiny_recovered"]))
                self.assertEqual(21600,m["world_seconds"])
                recognized=entries(r,"b05_anointed_destiny_mission_recognized")
                self.assertEqual(1,len(recognized))
                self.assertEqual(1,recognized[0]["detail"]["destiny_awarded"])
                self.assertEqual("external_explicit",
                                 recognized[0]["detail"]["gm_verdict"])
                self.assertTrue(recognized[0]["detail"]["quest_not_ended"])

    def test_05_unrecognized_quest_cannot_automatically_mint_destiny(self):
        for r in self.reports:
            m=r["metrics"]
            if r["policy"]!="gm_unrecognized":
                continue
            self.assertTrue(m["blocked_unrecognized_story"])
            self.assertEqual((0,1),(m["gm_story_destiny_awarded"],
                                   m["world_clock_destiny_recovered"]))
            self.assertEqual([],entries(r,"b05_anointed_destiny_mission_recognized"))
            self.assertEqual([],m["gm_mission_awards"])
            self.assertEqual(21600,m["world_seconds"])

    def test_06_dormant_elapsed_six_hours_does_not_restore_destiny(self):
        for focus in FOCUSES:
            for level in LEVELS:
                r=self.by_key[focus,level,"sentry_prepared","dormant_pause"]
                m=r["metrics"]
                self.assertEqual(1,m["dormant_destiny_after_6h"])
                self.assertEqual(43200,m["world_seconds"])
                self.assertEqual(1,m["world_clock_destiny_recovered"])
                self.assertEqual(0,m["gm_story_destiny_awarded"])
                self.assertTrue(m["active_bond"])
                if focus=="Low":
                    self.assertFalse(m["embodied"])
                verdicts=entries(r,"b05_anointed_destiny_bond_verdict")
                self.assertEqual(2,len(verdicts))
                self.assertEqual([False,True],[v["detail"]["active_after"]
                                               for v in verdicts])
                self.assertTrue(all(v["detail"]["no_automatic_morality"]
                                    for v in verdicts))

    def test_07_real_g4_world_time_and_separate_vp_vigor_recovery_not_new_steps(self):
        for r in self.reports:
            m=r["metrics"]
            self.assertGreaterEqual(m["authentic_exploration_recovery_events"],1)
            self.assertEqual(2,len([x for x in entries(r,"regeneration_step")
                                    if x["detail"]["actor"]==
                                    ("anointed" if r["focus"]=="Low" else "patient")]))
            time_events=entries(r,"b05_anointed_destiny_time_reconciled")
            self.assertTrue(time_events)
            self.assertTrue(all(t["detail"]["no_synthetic_g0_step"]
                                for t in time_events))
            self.assertTrue(all(t["detail"]["world_seconds"]>=0
                                for t in time_events))
            self.assertEqual(
                m["world_clock_destiny_recovered"],
                sum(t["detail"]["destiny_recovered"] for t in time_events))

    def test_08_native_clock_bridge_rejects_external_unrecognized_duplicate_or_reentry(self):
        for role in ("High","Medium","Low"):
            e,native=_spent_lesser_scene(role,2,"soldier",seed=0)
            bridge=AnointedDestinyExploration(e,native)
            with self.assertRaises(ValueError):
                AnointedDestinyExploration(e,native)
            before=(native.state.destiny,len(entries({"ledger":e.ledger},
                                    "b05_anointed_destiny_mission_recognized")))
            with self.assertRaises(UnresolvedDecision):
                bridge.record_mission_event("quest:label",gm_recognized=False)
            with self.assertRaises(UnresolvedDecision):
                bridge.apply_bond_verdict(active=False,gm_recognized=False)
            self.assertEqual(before,(native.state.destiny,0))
            self.assertEqual(1,bridge.record_mission_event("story:one",gm_recognized=True))
            with self.assertRaises(ValueError):
                bridge.record_mission_event("story:one",gm_recognized=True)
            self.assertEqual(2,native.state.destiny)

    def test_09_ledger_forgery_rejected_even_after_canonical_digest_rehash(self):
        for focus in FOCUSES:
            r=self.by_key[focus,3,"sentry_prepared","gm_recognized"]
            self.assertEqual(r,attest_policy(r,focus=focus,level=3,
                opponent="sentry_prepared",policy="gm_recognized",seed=0))
        report=deepcopy(self.by_key["Medium",2,"soldier","clock_partial"])
        report["metrics"]["world_clock_destiny_recovered"]=2
        with self.assertRaises(AssertionError):
            attest_policy(report,focus="Medium",level=2,
                          opponent="soldier",policy="clock_partial")
        report=deepcopy(self.by_key["High",3,"soldier","gm_recognized"])
        entry=entries(report,"b05_anointed_destiny_mission_recognized")[0]
        entry["detail"]["gm_verdict"]="forged_automatic"
        report["ledger_sha256"]=canonical_digest(report["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(report,focus="High",level=3,
                          opponent="soldier",policy="gm_recognized")

    def test_10_bad_policy_level_seed_and_documented_mvp_boundaries(self):
        for args in (
            {"focus":"Wrong","level":1,"opponent":"soldier","policy":"clock_partial"},
            {"focus":"Medium","level":4,"opponent":"soldier","policy":"gm_recognized"},
            {"focus":"Low","level":3,"opponent":"hunter","policy":"gm_unrecognized"},
            {"focus":"High","level":2,"opponent":"soldier","policy":"free_destiny"},
            {"focus":"High","level":2,"opponent":"soldier","policy":"clock_partial","seed":-1},
        ):
            with self.subTest(args=args),self.assertRaises(ValueError):
                run_policy(**args)
        doc=(Path(__file__).resolve().parents[1]/
             "docs/design/b04-b05-anointed-native-noncombat-destiny-v0.md").read_text().lower()
        for word in ("72","12/12","0/12","0/6","six-hour","gm",
                     "story beat","mission","g0","g4","g5","worldclock",
                     "unopposed","not certified","noncombat"):
            self.assertIn(word,doc)


if __name__=="__main__":
    unittest.main()
