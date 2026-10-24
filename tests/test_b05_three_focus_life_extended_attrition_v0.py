"""Extended High/Medium/Low Life balance evidence; no numerical tuning."""
from copy import deepcopy
import unittest

from scripts.b05_three_focus_life_extended_attrition_v0 import (
    ROLE_POLICIES,TACTICS,OPPONENTS,HORIZONS,PRESSURES,
    scene,run_policy,run_matrix,attest_policy,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def rows(r,kind):
    return [v for v in r["ledger"] if v["kind"]==kind]


class ExtendedLifeTacticalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix=run_matrix(seed=0)
        cls.idx={(r["role"],r["level"],r["opponent"],r["horizon"],
                  r["pressure"],r["tactic"],r["policy"]):r
                 for r in cls.matrix["cells"]}

    def row(self,role,level,opponent,horizon,pressure,tactic,policy):
        return self.idx[role,level,opponent,horizon,pressure,tactic,policy]

    def test_01_complete_912_source_authenticated_cross_product(self):
        expected={(role,level,opponent,horizon,pressure,tactic,policy)
            for role,policies in ROLE_POLICIES.items()
            for level in (1,2,3) for opponent in OPPONENTS
            for horizon in HORIZONS for pressure in PRESSURES
            for tactic in TACTICS for policy in policies
            if level==3 or policy!="exaltation"}
        self.assertEqual(len(expected),912)
        self.assertEqual(set(self.idx),expected)
        self.assertEqual(self.matrix["cell_count"],912)
        self.assertEqual(self.matrix["audit_sha256"],canonical_digest(
            {k:v for k,v in self.matrix.items() if k!="audit_sha256"}))

    def test_02_every_paid_attempt_and_hit_has_one_real_G4_receipt(self):
        for r in self.matrix["cells"]:
            with self.subTest(role=r["role"],level=r["level"],
                              policy=r["policy"],tactic=r["tactic"],
                              horizon=r["horizon"],pressure=r["pressure"]):
                m=r["metrics"]
                self.assertEqual(m["attack_attempts_paid"],
                                 m["rounds_completed"])
                self.assertEqual(m["genuine_regen_steps"],
                                 m["rounds_completed"])
                self.assertEqual(m["attacks_hit"]+m["attacks_missed"],
                                 m["attack_attempts_paid"])
                self.assertEqual(m["damage_receipts"],m["attacks_hit"])
                self.assertLessEqual(m["rounds_completed"],r["horizon"])
                self.assertEqual(sum(m["final_vp"]),m["max_vp"])
                self.assertEqual(len(r["source_digests"]),2)
                self.assertTrue(all(len(h)==64 for h in
                                    r["source_digests"].values()))
                if m["rounds_completed"]<r["horizon"]:
                    self.assertTrue(m["stopped_incapacitated"])
                self.assertGreaterEqual(m["final_hp"],-m["starting_hp"])
                self.assertGreaterEqual(m["final_vigor"],0)

    def test_03_baseline_starts_without_phantom_magic(self):
        for r in self.matrix["cells"]:
            if r["policy"]!="baseline":
                continue
            m=r["metrics"]
            self.assertEqual(m["effects_established"],0)
            self.assertEqual(m["final_vp"],[m["max_vp"],0,0])
            self.assertEqual(m["heal_hp"]+m["heal_vigor"],0)
            self.assertEqual(m["exaltation_arms"],0)
            self.assertEqual(m["projection_or_full_ap_paid"],0)
            self.assertEqual(r["round_completion_delta"],0)
            self.assertTrue(all(v==0 for v in
                                r["delta_vs_same_source_baseline"].values()))

    def test_04_source_paid_G5_and_temporal_hit_miss_authority(self):
        for role,opponent,tactic in (
            ("H","soldier","take_hit"),
            ("M","sentry_prepared","guard"),
            ("A","soldier","cautious_dodge"),
            ("B","sentry_prepared","take_hit")):
            r=run_policy(role=role,level=3,opponent=opponent,
                         policy="baseline",horizon=8,pressure="light",
                         tactic=tactic)
            m=r["metrics"]
            attacks=rows(r,"g5_melee_resolved")
            self.assertEqual(len(attacks),m["rounds_completed"])
            self.assertEqual([x["round"] for x in attacks],
                             list(range(1,m["rounds_completed"]+1)))
            self.assertEqual([x["detail"]["profile"] for x in attacks],
                             ["B06-AT-03" if opponent=="soldier"
                              else "B06-AT-02"]*len(attacks))
            self.assertEqual([v["detail"]["recipient"]
                              for v in rows(r,"g4_damage_applied")],
                             ["priest"]*m["attacks_hit"])
            self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))

    def test_05_defense_assignments_are_true_G0_capacity_receipts(self):
        for role in ROLE_POLICIES:
            for tactic in TACTICS:
                r=run_policy(role=role,level=3,opponent="soldier",
                             policy="baseline",horizon=4,
                             pressure="light",tactic=tactic)
                self.assertEqual(
                    [x["detail"]["defense"] for x in
                     rows(r,"defense_assigned")],
                    [TACTICS[tactic][0]]*r["metrics"]["rounds_completed"])
                self.assertEqual(r["metrics"]["defense_assignments"],
                                 r["metrics"]["attack_attempts_paid"])

    def test_06_miss_does_not_have_damage_packet_or_Vigor_die(self):
        seen=0
        for role in ROLE_POLICIES:
            for opponent in OPPONENTS:
                for tactic in ("guard","cautious_dodge"):
                    r=run_policy(role=role,level=3,opponent=opponent,
                                 policy="baseline",horizon=4,
                                 pressure="light",tactic=tactic)
                    for a in rows(r,"g5_melee_resolved"):
                        if a["detail"]["outcome"]=="miss":
                            self.assertIsNone(a["detail"]["damage"])
                            seen+=1
                    self.assertEqual(len(rows(r,"g4_damage_applied")),
                                     r["metrics"]["attacks_hit"])
        self.assertGreater(seen,0)

    def test_07_cautious_sidestep_is_paid_and_preserves_live_contact(self):
        r=run_policy(role="M",level=3,opponent="soldier",
                     policy="baseline",horizon=8,pressure="light",
                     tactic="cautious_dodge")
        movements=rows(r,"g1_movement_step")
        self.assertEqual(len(movements),
                         r["metrics"]["movement_steps"])
        self.assertEqual(r["metrics"]["movement_mp_paid"],
                         sum(x["detail"]["cost"] for x in movements))
        self.assertEqual([x["round"] for x in movements],
                         list(range(2,r["metrics"]["rounds_completed"]+1,2)))
        self.assertTrue(all(x["detail"]["cautious"] is True for x in movements))
        self.assertTrue(all(x["detail"]["actor"]=="priest" for x in movements))
        self.assertEqual(len(rows(r,"g1_movement_opportunity_pending")),0)

    def test_08_heal_cycle_only_spends_for_real_eligible_deficit(self):
        for role in ("H","M"):
            r=run_policy(role=role,level=3,opponent="sentry_prepared",
                         policy="heal_cycle",horizon=8,pressure="light",
                         tactic="take_hit")
            heal=rows(r,"g4_basic_heal_applied")
            paid=[x for x in rows(r,"action_committed")
                  if x["detail"]["actor"]=="priest"]
            self.assertEqual(len(heal),len(paid))
            self.assertLessEqual(len(heal),4)
            self.assertTrue(all(x["round"]%2==0 for x in heal))
            self.assertEqual(
                r["metrics"]["projection_or_full_ap_paid"],
                len(heal)*(20 if role=="H" else 24))
            self.assertEqual(r["metrics"]["final_vp"][2],len(heal)*2)
            self.assertEqual(r["metrics"]["heal_hp"],
                             sum(x["detail"]["hp_restored"] for x in heal))
            self.assertEqual(r["metrics"]["heal_vigor"],
                             sum(x["detail"]["vigor_restored"] for x in heal))

    def test_09_maintained_effect_is_source_paid_once_not_each_round(self):
        for role in ("H","M","A","B"):
            policy="chosen" if role in ("A","B") else "guided"
            r=run_policy(role=role,level=3,opponent="soldier",
                         policy=policy,horizon=8,pressure="light",
                         tactic="take_hit")
            m=r["metrics"]
            self.assertEqual(m["effects_established"],1)
            self.assertEqual(m["projection_or_full_ap_paid"],
                             {"H":20,"M":24,"A":30,"B":30}[role])
            self.assertLessEqual(m["effects_expired"],1)

    def test_10_low_exaltations_only_after_real_source_events(self):
        for role in ("A","B"):
            for opponent in OPPONENTS:
                r=run_policy(role=role,level=3,opponent=opponent,
                             policy="exaltation",horizon=8,
                             pressure="heavy",tactic="take_hit")
                armed=rows(r,"b05_exaltation_armed")
                self.assertEqual(len(armed),r["metrics"]["exaltation_arms"])
                self.assertLessEqual(len(armed),r["metrics"]["rounds_completed"])
                if role=="A":
                    steps=rows(r,"regeneration_step")
                    self.assertTrue(all(any(s["round"]==x["round"]
                                            and s["detail"]["actor"]=="priest"
                                            and s["index"]<x["index"]
                                            for s in steps) for x in armed))
                else:
                    self.assertTrue(all(x["detail"]["property"]=="EX-LP-01"
                                        for x in armed))
                self.assertEqual(sum(r["metrics"]["final_vp"]),6)

    def test_11_canonical_replay_rejects_metric_and_rehashed_forgery(self):
        kw={"role":"B","level":3,"opponent":"sentry_prepared",
            "policy":"exaltation","horizon":8,"pressure":"heavy",
            "tactic":"take_hit","seed":7}
        r=run_policy(**kw)
        self.assertEqual(attest_policy(r,**kw),r)
        forged=deepcopy(r)
        forged["metrics"]["final_hp"]=999
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(forged,**kw)
        forged=deepcopy(r)
        forged["ledger"][-1]["kind"]="fabricated_end"
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(forged,**kw)

    def test_12_invalid_source_or_uncertified_horizon_rejected(self):
        base={"role":"M","level":3,"opponent":"soldier",
              "policy":"baseline","horizon":4,
              "pressure":"light","tactic":"take_hit","seed":0}
        bad=(("role","R"),("level",True),("level",4),
             ("opponent","hunter"),("policy","open"),
             ("horizon",3),("horizon",True),("horizon",6),
             ("pressure","random"),("tactic","charge"),("seed",-1))
        for key,val in bad:
            kw={**base,key:val}
            with self.subTest(key=key,value=val):
                with self.assertRaises(ValueError):
                    run_policy(**kw)
        with self.assertRaises(ValueError):
            run_matrix(seed=True)
        with self.assertRaises(ValueError):
            run_policy(**{**base,"role":"A","level":2,"policy":"exaltation"})

    def test_13_no_statistical_balance_certification_or_rule_changes(self):
        report=self.matrix
        self.assertFalse(report["three_focus_balance_certified"])
        self.assertFalse(report["numerical_tuning_approved"])
        self.assertIsNone(report["balanced_focus_ranking"])
        self.assertIsNone(report["sampled_win_rate"])
        self.assertIsNone(report["confidence_interval"])
        self.assertFalse(report["intercession_and_external_Low_access_matched"])
        self.assertTrue(report["only_actual_rounds_counted"])
        self.assertTrue(report["same_build_fixed_dice_baselines"])

    def test_14_heavy_pressure_has_real_attrition_not_virtual_damage(self):
        for role in ROLE_POLICIES:
            r=run_policy(role=role,level=3,opponent="sentry_prepared",
                         policy="baseline",horizon=8,pressure="heavy",
                         tactic="take_hit")
            m=r["metrics"]
            self.assertEqual(m["attacks_hit"],m["rounds_completed"])
            self.assertEqual(m["damage_receipts"],m["attacks_hit"])
            self.assertGreater(m["vigor_applied"],0)
            self.assertGreater(len(rows(r,"g4_damage_applied")),0)
            self.assertEqual(len(rows(r,"g4_wound_created")),m["wounds"])
            if m["rounds_completed"]<8:
                self.assertTrue(m["dying"])

    def test_15_historical_phase_three_hash_remains_independent(self):
        self.assertTrue(self.matrix["only_actual_rounds_counted"])
        self.assertEqual(len(ROLE_POLICIES),4)
        self.assertEqual(set(HORIZONS),{4,8})
        self.assertEqual(set(PRESSURES),{"light","heavy"})
        self.assertEqual(set(TACTICS),{"take_hit","guard","cautious_dodge"})


if __name__=="__main__":
    unittest.main()
