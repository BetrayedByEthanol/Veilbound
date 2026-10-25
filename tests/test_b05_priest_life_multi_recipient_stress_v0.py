"""Multi-target Priest Life Stress: source G5 attacks and legal Life access."""
from copy import deepcopy
import unittest

from scripts.b05_priest_life_multi_recipient_stress_v0 import (
    POLICIES,L3_ONLY,L2_ONLY,PATTERNS,DAMAGE_FACES,OPPONENTS,
    run_policy,run_matrix,attest_policy,scene,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_encounter_state_v0 import UnresolvedDecision


def events(report,kind):
    return [x for x in report["ledger"] if x["kind"]==kind]


class ThreeFocusMultiRecipientStressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix=run_matrix(seed=0)
        cls.lookup={(r["role"],r["level"],r["opponent"],
                     r["pattern"],r["pressure"],r["policy"]):r
                    for r in cls.matrix["cases"]}

    def row(self,role,level,opponent,pattern,pressure,policy):
        return self.lookup[role,level,opponent,pattern,pressure,policy]

    def test_01_source_policy_cross_product_and_audit_authentication(self):
        expected={(role,level,opponent,pattern,pressure,policy)
                  for role,policies in POLICIES.items()
                  for level in (1,2,3)
                  for opponent in OPPONENTS
                  for pattern in PATTERNS
                  for pressure in DAMAGE_FACES
                  for policy in policies
                  if (policy not in L3_ONLY[role] or level>=3)
                  and (policy not in L2_ONLY[role] or level>=2)}
        self.assertEqual(len(expected),408)
        self.assertEqual(self.matrix["case_count"],408)
        self.assertEqual(set(self.lookup),expected)
        self.assertEqual(self.matrix["audit_sha256"],
                         canonical_digest({k:v for k,v in self.matrix.items()
                                           if k!="audit_sha256"}))
        self.assertFalse(self.matrix["focus_balance_certified"])
        self.assertFalse(self.matrix["numerical_tuning_approved"])

    def test_02_every_cell_uses_real_native_attacks_and_three_steps(self):
        for r in self.matrix["cases"]:
            with self.subTest(role=r["role"],level=r["level"],
                              pattern=r["pattern"],policy=r["policy"],
                              opponent=r["opponent"],pressure=r["pressure"]):
                m=r["metrics"]
                self.assertEqual(m["paid_enemy_hits"]+m["skipped_dead_target"],4)
                self.assertEqual(m["received_by"]["front"]
                                 +m["received_by"]["rear"]
                                 +m["received_by"]["priest"],
                                 m["paid_enemy_hits"])
                self.assertEqual(m["real_steps"],{
                    "priest":4,"front":4,"rear":4})
                self.assertEqual(sum(m["vp"]),{"H":6,"M":4,"A":2,"B":2}[r["role"]]*r["level"])
                self.assertEqual(len(r["source_digests"]),4)
                self.assertTrue(all(len(v)==64 for v in
                                    r["source_digests"].values()))
                self.assertGreaterEqual(m["direct_vigor_prevented"],0)
                self.assertGreaterEqual(m["direct_vigor_applied"],0)

    def test_03_true_distinct_F_R_and_optional_priest_targets(self):
        for pattern,target in (
            ("alternating",["front","rear","front","rear"]),
            ("rotating",["front","rear","priest","front"])):
            r=run_policy(role="H",level=3,opponent="sentry_prepared",
                         pattern=pattern,policy="baseline",pressure="light")
            self.assertEqual([x["detail"]["target"] for x in
                              events(r,"g5_melee_resolved")],target)
            self.assertEqual([x["detail"]["recipient"] for x in
                              events(r,"g4_damage_applied")],target)
            self.assertEqual(r["source_ids"]["front"],"F")
            self.assertEqual(r["source_ids"]["rear"],"R")
            self.assertEqual(r["source_ids"]["priest"],"H")
            self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))

    def test_04_no_spell_baseline_has_no_virtual_support_or_reactions(self):
        for r in self.matrix["cases"]:
            if r["policy"]!="baseline":
                continue
            m=r["metrics"]
            self.assertEqual(m["ap_paid"],0)
            self.assertEqual(m["paid_heal_count"],0)
            self.assertEqual(m["ally_effects"]+m["chosen_self_effects"],0)
            self.assertEqual(m["intercession_payments"],0)
            self.assertEqual(m["consecration_reassignments"],0)
            self.assertEqual(m["vp"],[{"H":6,"M":4,"A":2,"B":2}[r["role"]]*r["level"],0,0])
            self.assertTrue(all(v==0 for v in
                                r["delta_vs_same_source_baseline"].values()))

    def test_05_high_prepared_front_blessings_and_two_L3_effects(self):
        for opponent in OPPONENTS:
            for pattern in PATTERNS:
                for policy,kind in (
                    ("guided_front","Guided Regeneration"),
                    ("shelter_front","Vital Shelter")):
                    r=run_policy(role="H",level=2,opponent=opponent,
                                 pattern=pattern,policy=policy,
                                 pressure="light")
                    m=r["metrics"]
                    self.assertEqual(m["ap_paid"],20)
                    self.assertEqual(m["ally_effects"],1)
                    self.assertEqual(m["chosen_self_effects"],0)
                    effects=events(r,"g3_effect_established")
                    self.assertEqual((effects[0]["detail"]["effect_kind"],
                                      effects[0]["detail"]["recipient"]),
                                     (kind,"front"))
                split=run_policy(role="H",level=3,opponent=opponent,
                                 pattern=pattern,policy="split_wards",
                                 pressure="light")
                self.assertEqual(split["metrics"]["ap_paid"],40)
                self.assertEqual(split["metrics"]["ally_effects"],2)
                self.assertEqual([(e["detail"]["effect_kind"],
                                   e["detail"]["recipient"])
                                  for e in events(split,"g3_effect_established")
                                  if e["detail"]["caster"]=="priest"],
                                  [("Guided Regeneration","front"),
                                   ("Vital Shelter","rear")])
                self.assertEqual(split["metrics"]["vp"][2],1)

    def test_06_medium_reassignment_is_paid_and_preserves_source_host(self):
        for kind,policy in (
            ("Guided Regeneration","guided_reassign"),
            ("Vital Shelter","shelter_reassign")):
            r=run_policy(role="M",level=3,opponent="sentry_prepared",
                         pattern="alternating",policy=policy,pressure="light")
            applied=events(r,"b05_consecration_applied")
            moved=events(r,"b05_consecration_reassigned")
            self.assertEqual((len(applied),len(moved)),(1,1))
            self.assertEqual(moved[0]["detail"]["previous"],"front")
            self.assertEqual(moved[0]["detail"]["recipient"],"rear")
            self.assertEqual(applied[0]["detail"]["effect"],
                             moved[0]["detail"]["effect"])
            self.assertEqual(applied[0]["detail"]["committed"],2)
            self.assertEqual(moved[0]["detail"]["committed"],2)
            self.assertEqual(r["metrics"]["ap_paid"],48)
            self.assertEqual(r["metrics"]["consecration_reassignments"],1)

    def test_07_guided_intercession_requires_live_R_step_and_reaction(self):
        r=run_policy(role="M",level=3,opponent="soldier",
                     pattern="alternating",policy="guided_intercession",
                     pressure="heavy")
        payments=events(r,"b05_intercession_paid")
        arms=events(r,"b05_guided_intercession_armed")
        self.assertEqual((len(payments),len(arms)),(1,1))
        self.assertEqual(payments[0]["detail"]["recipient"],"rear")
        self.assertEqual(payments[0]["detail"]["spent"],2)
        self.assertEqual(arms[0]["round"],2)
        steps=[x for x in events(r,"regeneration_step")
               if x["detail"]["actor"]=="rear" and x["round"]==2]
        self.assertEqual(len(steps),1)
        self.assertLess(arms[0]["index"],steps[0]["index"])
        self.assertEqual(r["metrics"]["guided_intercessions"],1)
        self.assertEqual(r["metrics"]["vp"][2],2)

    def test_08_vital_intercession_consumes_real_R_sentry_vigor_packet(self):
        r=run_policy(role="M",level=3,opponent="sentry_prepared",
                     pattern="alternating",policy="shelter_intercession",
                     pressure="heavy")
        paid=events(r,"b05_intercession_paid")
        applied=events(r,"b05_vital_intercession_packet")
        self.assertEqual((len(paid),len(applied)),(1,1))
        self.assertEqual((applied[0]["detail"]["recipient"],
                          applied[0]["detail"]["effect"]),
                         ("rear",paid[0]["detail"]["effect"]))
        self.assertGreater(applied[0]["detail"]["prevented"],0)
        self.assertEqual(applied[0]["detail"]["original"],
                         applied[0]["detail"]["prevented"]
                         +applied[0]["detail"]["residual"])
        self.assertEqual(paid[0]["detail"]["spent"],2)
        self.assertEqual(r["metrics"]["vital_intercessions"],1)
        self.assertEqual(r["metrics"]["ap_paid"],24)

    def test_09_heal_triage_source_paid_for_H_M_and_low_A(self):
        for role in ("H","M","A"):
            for level in (1,2,3):
                r=run_policy(role=role,level=level,opponent="soldier",
                             pattern="alternating",policy="triage",
                             pressure="heavy")
                heals=events(r,"g4_basic_heal_applied")
                self.assertGreaterEqual(len(heals),1)
                self.assertEqual(len(heals),r["metrics"]["paid_heal_count"])
                self.assertTrue(all(x["detail"]["recipient"] in ("front","rear")
                                    for x in heals))
                self.assertTrue(all(x["round"] in (2,3,4) for x in heals))
                self.assertEqual(r["metrics"]["vp"][2],2*len(heals))
                self.assertEqual(r["metrics"]["ap_paid"],
                                 len(heals)*{"H":20,"M":24,"A":30}[role])

    def test_10_low_Chosens_only_protect_themselves_not_allies(self):
        for role in ("A","B"):
            for pattern in PATTERNS:
                r=run_policy(role=role,level=3,opponent="sentry_prepared",
                             pattern=pattern,policy="chosen_self",
                             pressure="heavy")
                m=r["metrics"]
                self.assertEqual(m["chosen_self_effects"],1)
                self.assertEqual(m["ally_effects"],0)
                self.assertEqual(m["paid_heal_count"],0)
                effects=[x for x in events(r,"g3_effect_established")
                         if x["detail"]["caster"]=="priest"]
                self.assertEqual([x["detail"]["recipient"] for x in effects],
                                 ["priest"])
                self.assertEqual(m["intercession_payments"],0)

    def test_11_low_A_constrained_chosen_plus_external_heal(self):
        for level in (2,3):
            r=run_policy(role="A",level=level,opponent="soldier",
                         pattern="alternating",policy="chosen_and_heal",
                         pressure="heavy")
            self.assertEqual(r["metrics"]["chosen_self_effects"],1)
            self.assertEqual(r["metrics"]["ally_effects"],0)
            self.assertGreaterEqual(r["metrics"]["paid_heal_count"],1)
            self.assertEqual(r["metrics"]["vp"][1],1)
            self.assertEqual(r["metrics"]["ap_paid"],
                             30*(1+r["metrics"]["paid_heal_count"]))

    def test_12_low_B_cannot_gain_unsourced_free_hand_or_external_host(self):
        combat,adapter=scene(role="B",level=3,opponent="soldier",
                             pattern="alternating",policy="chosen_self",
                             pressure="light")
        e=combat.e
        e.start_turn("priest")
        with self.assertRaises(UnresolvedDecision):
            e.g4.cast_basic_heal("priest","front",tier=1,die=3,
                                 hand_available=True,in_range=True,
                                 unobstructed=True,unopposed=True)
        with self.assertRaises((ValueError,UnresolvedDecision)):
            adapter.cast_chosen("front")
        self.assertEqual(e.actors["priest"].vp_spent,0)
        self.assertEqual(e.actors["priest"].ap_remaining,
                         e.actors["priest"].ap_total)

    def test_13_low_L3_vital_property_only_own_native_HP_packet(self):
        r=run_policy(role="B",level=3,opponent="sentry_prepared",
                     pattern="rotating",policy="vital_exaltation",
                     pressure="heavy")
        diverted=events(r,"b05_vital_interposition_applied")
        self.assertLessEqual(len(diverted),1)
        self.assertTrue(all(x["detail"]["caster"]=="priest" for x in diverted))
        self.assertTrue(all(x["round"]==3 for x in diverted))
        self.assertGreaterEqual(r["metrics"]["exaltation_arms"],1)
        self.assertEqual(r["metrics"]["ally_effects"],0)

    def test_14_forged_rehashed_report_and_wrong_seed_fail_closed(self):
        args={"role":"M","level":3,"opponent":"sentry_prepared",
              "pattern":"alternating","policy":"shelter_intercession",
              "pressure":"heavy","seed":3}
        report=run_policy(**args)
        self.assertEqual(attest_policy(report,**args),report)
        altered=deepcopy(report)
        altered["metrics"]["intercession_payments"]=0
        altered["ledger_sha256"]=canonical_digest(altered["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(altered,**args)
        with self.assertRaises(AssertionError):
            attest_policy(report,**{**args,"seed":4})

    def test_15_invalid_levels_policies_and_routed_targets_fail_closed(self):
        a={"role":"M","level":3,"opponent":"soldier",
           "pattern":"alternating","policy":"baseline",
           "pressure":"light","seed":0}
        wrong=(("role","X"),("level",True),("level",4),
               ("opponent","hunter"),("pattern","random"),
               ("policy","phantom"),("pressure","random"),("seed",-1))
        for key,val in wrong:
            with self.subTest(field=key,value=val):
                with self.assertRaises(ValueError):
                    run_policy(**{**a,key:val})
        for role,level,policy in (("M",2,"guided_intercession"),
                                  ("M",1,"shelter_intercession"),
                                  ("H",2,"split_wards"),("A",1,"chosen_and_heal"),
                                  ("B",2,"vital_exaltation"),
                                  ("B",3,"triage")):
            with self.assertRaises(ValueError):
                run_policy(**{**a,"role":role,"level":level,"policy":policy})
        with self.assertRaises(ValueError):
            run_matrix(seed=True)


if __name__=="__main__":
    unittest.main()
