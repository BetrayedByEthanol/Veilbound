"""B04/B05 actual G5 damage plus genuine natural and Anointed recovery."""
from copy import deepcopy
import unittest

from scripts.b05_anointed_native_natural_recovery_v0 import (
    FOCI, LEVELS, OPPONENTS, POLICIES, run_policy, run_matrix, attest_policy,
)
from scripts.b05_anointed_native_defensive_encounter_v0 import (
    run_policy as zero_natural_policy,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def events(report,kind):
    return [x for x in report["ledger"] if x["kind"]==kind]


SIG={"High":("g4_anointed_returning_step_applied",2),
     "Medium":("g4_anointed_medium_returning_step_applied",1),
     "Low":("g4_anointed_low_returning_step_applied",1)}


class NativeNaturalRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix=run_matrix(seed=0)
        cls.lookup={(r["focus"],r["level"],r["opponent"],r["policy"]):r
                    for r in cls.matrix}

    def test_01_exact_fifty_four_real_policy_witnesses_no_certification(self):
        self.assertEqual(54,len(self.matrix))
        self.assertEqual(54,len(self.lookup))
        self.assertEqual(54,len(FOCI)*len(LEVELS)*len(OPPONENTS)*len(POLICIES))
        for r in self.matrix:
            self.assertIs(r["independent_focus_certified"],False)
            self.assertIs(r["representative_play_certified"],False)
            self.assertIsNone(r["sampled_win_rate"])

    def test_02_one_real_source_hit_two_real_player_paid_hp_allocations(self):
        for r in self.matrix:
            with self.subTest(focus=r["focus"],level=r["level"],
                              opponent=r["opponent"],policy=r["policy"]):
                m=r["metrics"]
                self.assertEqual(1,m["g5_hit_events"])
                self.assertEqual(1,m["g4_damage_events"])
                self.assertEqual(1,m["g0_enemy_paid_actions"])
                self.assertEqual(2,m["g0_recipient_regeneration_steps"])
                self.assertEqual((2,2),(m["natural_hp_restored"],
                                         m["natural_recipient_vigor_spent"]))
                self.assertEqual([1,2],m["natural_step_rounds"])
                self.assertLess(m["g5_hit_index"],m["natural_step_indices"][0])
                natural=[x for x in events(r,"regeneration_step")
                         if x["detail"]["actor"]==m["recipient"]]
                self.assertEqual(2,len(natural))
                self.assertEqual([1,1],[x["detail"]["hp_restored"] for x in natural])
                self.assertEqual([1,1],[x["detail"]["throughput_spent"] for x in natural])
                self.assertEqual([0,0],[x["detail"]["repair_points"] for x in natural])
                self.assertEqual(1,len(events(r,"g5_melee_sequence_attested")))
                self.assertEqual(1,len(events(r,"g5_melee_resolved")))
                self.assertEqual(1,len(events(r,"g4_damage_applied")))

    def test_03_two_natural_hp_costs_are_distinct_from_signature_vigor(self):
        for focus in FOCI:
            pulse_kind,cap=SIG[focus]
            for level in LEVELS:
                for opponent in OPPONENTS:
                    base=self.lookup[focus,level,opponent,"natural_only"]
                    zero=zero_natural_policy(
                        focus=focus,level=level,opponent=opponent,
                        policy="baseline",seed=0)
                    self.assertEqual(zero["metrics"]["recipient_hp"]+2,
                                     base["metrics"]["recipient_hp"])
                    self.assertEqual(zero["metrics"]["recipient_vigor"]-2,
                                     base["metrics"]["recipient_vigor"])
                    self.assertEqual(2,base["metrics"]["anointed_destiny_remaining"])
                    self.assertEqual(0,base["metrics"]["signature_receipts"])
                    for policy,expected_vigor,expected_destiny in (
                        ("natural_plus_signature",cap,0),
                        ("natural_plus_lesser",0,1),
                    ):
                        with self.subTest(focus=focus,level=level,
                                          opponent=opponent,policy=policy):
                            r=self.lookup[focus,level,opponent,policy]
                            m=r["metrics"]
                            self.assertEqual(1,m["signature_receipts"])
                            self.assertEqual(cap,m["signature_hp_restored"])
                            self.assertEqual(base["metrics"]["recipient_hp"]+cap,
                                             m["recipient_hp"])
                            self.assertEqual(base["metrics"]["recipient_vigor"]-expected_vigor,
                                             m["recipient_vigor"])
                            self.assertEqual(expected_vigor,
                                             m["signature_recipient_vigor_spent"])
                            self.assertEqual(expected_destiny,m["signature_destiny_spent"])
                            self.assertEqual(2-expected_destiny,m["anointed_destiny_remaining"])
                            self.assertEqual(1,len(events(r,pulse_kind)))

    def test_04_source_hit_and_signature_causality_is_preserved(self):
        for r in self.matrix:
            hit=events(r,"g5_melee_resolved")[0]
            natural=[x for x in events(r,"regeneration_step")
                     if x["detail"]["actor"]==r["metrics"]["recipient"]]
            self.assertLess(hit["index"],natural[0]["index"])
            self.assertLess(natural[0]["index"],natural[1]["index"])
            src=events(r,"b05_anointed_natural_recovery_policy")
            self.assertEqual(1,len(src))
            self.assertEqual(r["policy"],src[0]["detail"]["policy"])
            self.assertEqual("explicit_unopposed",
                             src[0]["detail"]["beneficial_healing"])
            self.assertEqual(1,src[0]["detail"]["natural_hp_each_genuine_recipient_step"])
            self.assertEqual(0,src[0]["detail"]["wound_repair"])
            self.assertFalse(events(r,"g4_anointed_guided_waiver_applied"))
            pulses=sum(len(events(r,SIG[f][0])) for f in FOCI)
            if r["policy"]=="natural_only":
                self.assertEqual(0,pulses)
            else:
                self.assertEqual(1,pulses)
                pulse=next(x for f in FOCI for x in events(r,SIG[f][0]))
                self.assertGreater(pulse["index"],hit["index"])
                self.assertEqual(2 if r["focus"]=="High" else 1,pulse["round"])

    def test_05_medium_investment_and_high_projection_actually_cost_ap(self):
        for r in self.matrix:
            paid=[x for x in events(r,"action_committed")
                  if x["detail"].get("actor")=="anointed"]
            if r["focus"]=="Medium" and r["policy"]!="natural_only":
                self.assertEqual(1,len(paid))
                self.assertEqual("anointed:medium:investment",paid[0]["detail"]["label"])
                self.assertEqual(24,paid[0]["detail"]["ap_spent"])
            elif r["focus"]=="High" and r["policy"]!="natural_only":
                self.assertEqual(1,len(paid))
                self.assertEqual("anointed:high:returning_step",paid[0]["detail"]["label"])
                self.assertEqual(20,paid[0]["detail"]["ap_spent"])
            else:
                self.assertEqual(0,len(paid))
            self.assertEqual(0,r["metrics"]["anointed_vp_spent"])
            self.assertEqual(0,r["metrics"]["anointed_vp_committed"])

    def test_06_source_identity_and_prepared_sentry_remain_real(self):
        for r in self.matrix:
            self.assertEqual({"soldier":"B06-EN-02",
                              "sentry_prepared":"B06-EN-01"}[r["opponent"]],
                             r["source_ids"]["foe"])
            self.assertEqual({"High":"AH","Medium":"AM","Low":"AL"}[r["focus"]],
                             r["source_ids"]["anointed"])
            source=events(r,"b05_anointed_defensive_policy")[0]["detail"]
            self.assertEqual(r["source_digests"],source["source_digests"])
            if r["opponent"]=="sentry_prepared":
                self.assertEqual("B06-AT-02",
                    events(r,"g5_melee_sequence_attested")[0]["detail"]["profiles"][0])
            else:
                self.assertEqual("B06-AT-03",
                    events(r,"g5_melee_sequence_attested")[0]["detail"]["profiles"][0])

    def test_07_exact_full_replay_not_only_a_self_consistent_digest(self):
        for focus in FOCI:
            r=self.lookup[focus,3,"sentry_prepared","natural_plus_lesser"]
            self.assertEqual(r,attest_policy(
                r,focus=focus,level=3,opponent="sentry_prepared",
                policy="natural_plus_lesser",seed=0))
        tampered=deepcopy(self.lookup["Medium",2,"soldier","natural_plus_lesser"])
        tampered["metrics"]["natural_recipient_vigor_spent"]=1
        with self.assertRaises(AssertionError):
            attest_policy(tampered,focus="Medium",level=2,opponent="soldier",
                          policy="natural_plus_lesser",seed=0)
        tampered=deepcopy(self.lookup["Low",2,"soldier","natural_plus_signature"])
        evt=events(tampered,"b05_anointed_natural_recovery_policy")[0]
        evt["detail"]["natural_hp_each_genuine_recipient_step"]=2
        tampered["ledger_sha256"]=canonical_digest(tampered["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(tampered,focus="Low",level=2,opponent="soldier",
                          policy="natural_plus_signature",seed=0)

    def test_08_reject_unsupported_focus_level_policy_opponent_seed(self):
        cases=(
            {"focus":"wrong","level":1,"opponent":"soldier","policy":"natural_only"},
            {"focus":"High","level":4,"opponent":"soldier","policy":"natural_only"},
            {"focus":"Low","level":3,"opponent":"hunter","policy":"natural_plus_signature"},
            {"focus":"Medium","level":2,"opponent":"soldier","policy":"free_all"},
            {"focus":"High","level":2,"opponent":"soldier","policy":"natural_only","seed":-1},
        )
        for args in cases:
            with self.subTest(args=args),self.assertRaises(ValueError):
                run_policy(**args)

    def test_09_documented_scope_never_grants_native_offense_or_certification(self):
        from pathlib import Path
        doc=(Path(__file__).resolve().parents[1]/
             "docs/design/b04-b05-anointed-natural-regeneration-g5-attrition-v0.md").read_text().lower()
        for token in ("54","12/12","0/12","0/6","natural","signature",
                      "unopposed","contested","G0","G4","G5",
                      "Vigor","not certified"):
            self.assertIn(token.lower(),doc)


if __name__=="__main__":
    unittest.main()
