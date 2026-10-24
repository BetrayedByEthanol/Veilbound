"""Three-Focus Life comparison: same source-native hits, honest local baselines."""
from copy import deepcopy
import unittest

from scripts.b05_three_focus_life_comparison_v0 import (
    FOCI,OPPONENTS,ROLE_POLICIES,ROLLS,
    run_policy,attest_policy,run_matrix,scene,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_encounter_state_v0 import UnresolvedDecision, RegenerationChoice


def rows(report,kind):
    return [v for v in report["ledger"] if v["kind"]==kind]


class ThreeFocusLifeComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run_matrix(seed=0)
        cls.index={(x["role"],x["level"],x["opponent"],x["policy"]):x
                   for x in cls.report["matched_self"]}
        cls.ally={(x["role"],x["level"],x["opponent"],x["policy"]):x
                  for x in cls.report["high_medium_same_ally"]}

    def test_01_complete_64_self_and_36_source_F_ally_cells(self):
        r=self.report
        self.assertEqual((r["matched_self_cells"],
                          r["existing_same_F_ally_cells"]),(64,36))
        expected={(role,level,opponent,policy)
                  for role,policies in ROLE_POLICIES.items()
                  for level in (1,2,3) for opponent in OPPONENTS
                  for policy in policies
                  if policy!="exaltation" or level==3}
        self.assertEqual(set(self.index),expected)
        self.assertEqual(len(self.ally),36)
        self.assertEqual(r["audit_sha256"],canonical_digest(
            {k:v for k,v in r.items() if k!="audit_sha256"}))
        self.assertFalse(r["low_ally_comparison_supported"])
        self.assertFalse(r["self_armor_hp_vigor_normalized_across_focuses"])
        self.assertTrue(r["local_baseline_delta_only"])
        self.assertFalse(r["three_focus_balance_certified"])
        self.assertIsNone(r["focus_ranking"])
        self.assertIsNone(r["sampled_win_rate"])

    def test_02_all_native_self_cells_conserve_VP_and_deliver_two_hits(self):
        for row in self.report["matched_self"]:
            with self.subTest(role=row["role"],level=row["level"],
                              opponent=row["opponent"],policy=row["policy"]):
                m=row["metrics"]
                self.assertEqual((m["g5_paid_attacks"],
                                  m["g4_delivered_hits"],
                                  m["actual_regen_steps"]),(2,2,2))
                self.assertEqual(sum(m["final_vp"]),m["max_vp"])
                self.assertTrue(all(len(d)==64 for d in
                                    row["source_digests"].values()))
                self.assertGreaterEqual(m["final_vigor"],0)
                self.assertLessEqual(m["final_vigor"],m["starting_vigor"])
                self.assertGreaterEqual(m["final_hp"],-m["starting_hp"])
                self.assertLessEqual(m["final_hp"],m["starting_hp"])
                self.assertEqual(m["max_vp"],{"H":6,"M":4,"A":2,"B":2}[row["role"]]*row["level"])
                self.assertEqual(m["wounds"],0)
                self.assertFalse(m["dead"])
                self.assertFalse(m["dying"])

    def test_03_no_magic_baselines_have_no_extra_magic_or_ap(self):
        for role in ROLE_POLICIES:
            for level in (1,2,3):
                for opponent in OPPONENTS:
                    row=self.index[role,level,opponent,"baseline"]
                    m=row["metrics"]
                    self.assertEqual(m["final_vp"],[m["max_vp"],0,0])
                    self.assertEqual(m["projection_or_full_ap_paid"],0)
                    self.assertEqual(m["effects_established"],0)
                    self.assertEqual(m["exaltation_arms"],0)
                    self.assertEqual(m["held_hp_restored"],0)
                    self.assertEqual(m["vital_hp_prevented"],0)
                    self.assertEqual(row["delta_vs_same_source_baseline"],{
                        "hp_delta":0,"vigor_delta":0,"wound_delta":0,
                        "vigor_prevented_delta":0,
                        "native_hp_prevented_delta":0,
                        "spent_vp_delta":0,"committed_vp_delta":0,
                        "ap_paid_delta":0})

    def test_04_high_prepared_projection_and_source_cost(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                for policy,spent,committed in (("guided",0,2),("shelter",1,2)):
                    m=self.index["H",level,opponent,policy]["metrics"]
                    self.assertEqual(m["projection_or_full_ap_paid"],20)
                    self.assertEqual(m["final_vp"],[6*level-spent-committed,
                                                    committed,spent])
                    self.assertEqual(m["effects_established"],1)
                    self.assertEqual(m["exaltation_arms"],0)

    def test_05_medium_real_consecration_cost(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                for policy,spent in (("guided",0),("shelter",1)):
                    m=self.index["M",level,opponent,policy]["metrics"]
                    self.assertEqual(m["projection_or_full_ap_paid"],24)
                    self.assertEqual(m["final_vp"],[4*level-2-spent,2,spent])
                    self.assertEqual(m["effects_established"],1)
                    self.assertEqual(m["exaltation_arms"],0)

    def test_06_low_source_Chosens_and_attached_Exaltation_prices(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                for role,spell,spent in (("A","guided",0),("B","shelter",1)):
                    m=self.index[role,level,opponent,spell]["metrics"]
                    self.assertEqual(m["projection_or_full_ap_paid"],30)
                    self.assertEqual(m["final_vp"],[2*level-1-spent,1,spent])
                    self.assertEqual(m["effects_established"],1)
                    self.assertEqual(m["exaltation_arms"],0)
                for role in ("A","B"):
                    if level!=3:
                        self.assertNotIn((role,level,opponent,"exaltation"),
                                         self.index)
                        continue
                    exalt=self.index[role,3,opponent,"exaltation"]["metrics"]
                    self.assertEqual(exalt["projection_or_full_ap_paid"],30)
                    self.assertEqual(exalt["effects_established"],1)
                    # A held host remains reserved. B's finite B8 may
                    # be exhausted by real L3 Vital HP diversion followed
                    # by a prepared Sentry Vigor packet; G3 MUST refund
                    # its one effective Committed VP, never Spent VP.
                    self.assertLessEqual(exalt["exaltation_arms"],1)
                    self.assertEqual(exalt["final_vp"][1],
                                     1-exalt["committed_vp_refunded"])
                    self.assertIn(exalt["committed_vp_refunded"],(0,1))
                    self.assertEqual(exalt["finite_host_exhaustions"],
                                     exalt["committed_vp_refunded"])
                    if role=="A":
                        self.assertEqual(exalt["final_vp"][1],1)
                    elif exalt["committed_vp_refunded"]:
                        actual=run_policy(
                            role=role,level=3,opponent=opponent,
                            policy="exaltation")
                        ends=rows(actual,"g3_effect_ended")
                        self.assertEqual(len(ends),1)
                        self.assertEqual(
                            (ends[0]["detail"]["reason"],
                             ends[0]["detail"]["returned"]),
                            ("budget_exhausted",1))
                    self.assertEqual(exalt["final_vp"][2],
                                     (1 if role=="B" else 0)
                                     +exalt["exaltation_arms"])

    def test_07_G5_source_profiles_and_all_native_rounds(self):
        for role in ROLE_POLICIES:
            for opponent in OPPONENTS:
                r=run_policy(role=role,level=3,opponent=opponent,
                             policy="baseline")
                attacks=rows(r,"g5_melee_resolved")
                damaging=rows(r,"g4_damage_applied")
                steps=[v for v in rows(r,"regeneration_step")
                       if v["detail"]["actor"]=="priest"]
                self.assertEqual([v["round"] for v in attacks],[1,2])
                self.assertEqual([v["round"] for v in damaging],[1,2])
                self.assertEqual([v["round"] for v in steps],[1,2])
                profile="B06-AT-03" if opponent=="soldier" else "B06-AT-02"
                self.assertEqual([v["detail"]["profile"] for v in attacks],
                                 [profile,profile])
                self.assertEqual([v["detail"]["recipient"] for v in damaging],
                                 ["priest","priest"])
                self.assertEqual((r["source_ids"]["priest"],
                                  r["source_ids"]["foe"]),
                                 (role,OPPONENTS[opponent][0]))
                self.assertEqual(r["ledger_sha256"],
                                 canonical_digest(r["ledger"]))

    def test_08_protection_is_actual_damage_not_imputed_packet(self):
        for role in ("H","M","B"):
            for level in (1,2,3):
                for opponent in OPPONENTS:
                    policy="shelter"
                    m=self.index[role,level,opponent,policy]["metrics"]
                    base=self.index[role,level,opponent,"baseline"]["metrics"]
                    if opponent=="soldier":
                        self.assertEqual(m["vigor_prevented"],0)
                        self.assertEqual(base["vigor_prevented"],0)
                    else:
                        self.assertGreater(m["vigor_prevented"],0)
                        self.assertLess(m["vigor_applied"],base["vigor_applied"])
                    self.assertEqual(
                        self.index[role,level,opponent,policy]
                        ["delta_vs_same_source_baseline"]["vigor_prevented_delta"],
                        m["vigor_prevented"])

    def test_09_guided_only_real_step_no_extra_fake_healing(self):
        for role in ("H","M","A"):
            for level in (1,2,3):
                for opponent in OPPONENTS:
                    m=self.index[role,level,opponent,"guided"]["metrics"]
                    self.assertEqual(m["actual_regen_steps"],2)
                    self.assertEqual(m["held_hp_restored"],0)
                    self.assertEqual(m["vital_hp_prevented"],0)
                    self.assertLessEqual(m["step_hp_restored"],
                                         m["step_vigor_paid"])

    def test_10_self_B_is_not_same_ally_F_and_is_not_source_normalized(self):
        self.assertNotIn(("B",1,"soldier","shelter"),self.ally)
        self.assertNotIn(("A",3,"sentry_prepared","guided"),self.ally)
        self.assertEqual(self.ally["H",1,"soldier","baseline"]
                         ["recipient"],"source_F_scholar_ally")
        self.assertEqual(self.ally["M",1,"soldier","baseline"]
                         ["recipient"],"source_F_scholar_ally")
        for level in (1,2,3):
            for opponent in OPPONENTS:
                for policy in ("baseline","guided","shelter"):
                    h=self.ally["H",level,opponent,policy]
                    m=self.ally["M",level,opponent,policy]
                    self.assertEqual(h["source_digests"]["ally"],
                                     m["source_digests"]["ally"])
                    self.assertEqual(h["source_digests"]["foe"],
                                     m["source_digests"]["foe"])

    def test_11_rehashed_forgery_and_different_seed_fail_replay(self):
        r=run_policy(role="B",level=3,opponent="sentry_prepared",
                     policy="exaltation",seed=2)
        self.assertEqual(attest_policy(
            r,role="B",level=3,opponent="sentry_prepared",
            policy="exaltation",seed=2),r)
        forged=deepcopy(r)
        forged["metrics"]["vigor_prevented"]=120
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(forged,role="B",level=3,
                          opponent="sentry_prepared",policy="exaltation",seed=2)
        with self.assertRaises(AssertionError):
            attest_policy(r,role="B",level=3,opponent="sentry_prepared",
                          policy="exaltation",seed=1)

    def test_12_invalid_role_level_policy_opponent_and_seed_fail_closed(self):
        cases=(("T",1,"soldier","baseline",0),
               ("H",True,"soldier","baseline",0),
               ("B",4,"soldier","shelter",0),
               ("A",2,"soldier","shelter",0),
               ("M",3,"soldier","exaltation",0),
               ("A",2,"soldier","exaltation",0),
               ("B",1,"bogus","baseline",0),
               ("H",1,"sentry_prepared","none",0),
               ("M",1,"soldier","baseline",-1))
        for role,level,opponent,policy,seed in cases:
            with self.subTest(role=role,level=level,policy=policy,
                              opponent=opponent,seed=seed):
                with self.assertRaises(ValueError):
                    run_policy(role=role,level=level,opponent=opponent,
                               policy=policy,seed=seed)
        for seed in (-1,True,1.5):
            with self.assertRaises(ValueError):
                run_matrix(seed=seed)

    def test_13_compatibility_no_cross_source_prayer_access(self):
        combat,adapter=scene(role="A",level=3,opponent="soldier",
                             policy="guided")
        e=combat.e
        e.start_turn("priest")
        with self.assertRaises((ValueError,UnresolvedDecision)):
            adapter.cast_chosen("foe")
        self.assertEqual(e.actors["priest"].vp_spent,0)
        self.assertEqual(e.actors["priest"].ap_remaining,
                         e.actors["priest"].ap_total)

    def test_14_unchanged_native_high_medium_ally_evidence(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                h=self.ally["H",level,opponent,"guided"]
                m=self.ally["M",level,opponent,"guided"]
                self.assertEqual(h["recipient"],m["recipient"])
                self.assertGreaterEqual(h["ally_final_vigor"],0)
                self.assertGreaterEqual(m["ally_final_vigor"],0)
                self.assertEqual(sum(h["priest_final_vp"]),6*level)
                self.assertEqual(sum(m["priest_final_vp"]),4*level)

    def test_15_no_world_skill_balance_approval_from_fixed_dice(self):
        r=self.report
        self.assertTrue(r["no_automatic_tuning"])
        self.assertTrue(r["balance_candidates_require_followup"])
        self.assertTrue(r["fixed_dice_not_probability_sample"])
        self.assertIsNone(r["confidence_interval"])
        self.assertFalse(r["three_focus_balance_certified"])
        self.assertFalse(r["self_armor_hp_vigor_normalized_across_focuses"])


if __name__=="__main__":
    unittest.main()
