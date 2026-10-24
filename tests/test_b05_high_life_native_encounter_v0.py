"""Native High Priest Life Soldier/Sentry encounters and access receipts."""
from copy import deepcopy
import unittest

from scripts.b05_high_life_native_encounter_v0 import (
    OPPONENTS,POLICIES,PREPARATIONS,L3_ONLY,scene,
    run_policy,run_matrix,attest_policy,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision


def rows(report,kind):
    return [x for x in report["ledger"] if x["kind"]==kind]


class HighLifeNativeEncounterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix=run_matrix(seed=0)
        cls.index={(c["level"],c["opponent"],c["policy"]):c
                   for c in cls.matrix["cells"]}

    def cell(self,level,opponent,policy):
        return self.index[level,opponent,policy]

    def test_01_exact_42_native_policy_cases_with_live_source_hashes(self):
        matrix=self.matrix
        expected={(l,o,p) for l in (1,2,3) for o in OPPONENTS
                  for p in POLICIES if l==3 or p not in L3_ONLY}
        self.assertEqual(matrix["cell_count"],42)
        self.assertEqual(set(self.index),expected)
        self.assertEqual(matrix["audit_sha256"],canonical_digest(
            {k:v for k,v in matrix.items() if k!="audit_sha256"}))
        self.assertTrue(matrix["source_replay_required"])
        self.assertFalse(matrix["independent_high_focus_certified"])
        self.assertFalse(matrix["three_focus_balance_certified"])
        self.assertIsNone(matrix["sampled_win_rate"])
        for cell in matrix["cells"]:
            with self.subTest(level=cell["level"],opponent=cell["opponent"],
                              policy=cell["policy"]):
                self.assertEqual(cell["preparation"],PREPARATIONS[cell["policy"]])
                self.assertEqual(cell["source_digests"].keys(),
                                 {"high","foe","ally"})
                self.assertTrue(all(len(v)==64 for v in cell["source_digests"].values()))
                m=cell["metrics"]
                self.assertEqual((m["paid_g5_hits"],m["native_g4_damage_events"],
                                  m["ally_real_steps"],m["high_real_steps"]),
                                 (2,2,2,2))
                self.assertEqual(sum(m["high_vp"]),6*cell["level"])
                self.assertEqual(m["high_hp"],12)
                self.assertGreater(m["ally_hp"],0)
                self.assertLessEqual(m["ally_hp"],12)
                self.assertGreaterEqual(m["ally_vigor"],0)
                self.assertEqual(m["ally_wounds"],0)

    def test_02_source_native_two_hits_without_auto_attacks_or_extra_steps(self):
        for opponent in OPPONENTS:
            report=run_policy(level=3,opponent=opponent,policy="prepared_shelter")
            attacks=rows(report,"g5_melee_resolved")
            damages=rows(report,"g4_damage_applied")
            self.assertEqual([v["round"] for v in attacks],[1,2])
            self.assertEqual([x["round"] for x in damages],[1,2])
            expected_profile="B06-AT-03" if opponent=="soldier" else "B06-AT-02"
            self.assertEqual([v["detail"]["profile"] for v in attacks],
                             [expected_profile]*2)
            self.assertTrue(all(x["detail"]["recipient"]=="ally" for x in damages))
            self.assertEqual([x["detail"]["actor"] for x in
                              rows(report,"regeneration_step")],
                             ["high","foe","ally","high","foe","ally"])
            self.assertEqual(report["source_ids"]["high"],"H")
            self.assertEqual(report["source_ids"]["ally"],"F")
            self.assertEqual(report["source_ids"]["foe"],OPPONENTS[opponent][0])
            self.assertEqual(report["ledger_sha256"],
                             canonical_digest(report["ledger"]))

    def test_03_baseline_never_creates_free_spells_or_vp(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                m=self.cell(level,opponent,"baseline")["metrics"]
                self.assertEqual(m["high_casts"],[])
                self.assertEqual(m["high_vp"],[6*level,0,0])
                self.assertEqual(m["high_ap_paid"],0)
                self.assertEqual(m["high_open_prayer_fills"],0)
                self.assertEqual(m["active_high_effects"],0)
                self.assertEqual(m["primary_heal_hp"],0)
                self.assertEqual(m["vigor_prevented"],0)

    def test_04_prepared_maintained_cost_and_ally_regen(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                with self.subTest(level=level,opponent=opponent):
                    m=self.cell(level,opponent,"prepared_guided")["metrics"]
                    cast=m["high_casts"]
                    self.assertEqual(cast,[{"technique":"Guided Regeneration",
                        "access":"prepared","action_ap":20,"spent":0,
                        "surcharge":0,"committed":2}])
                    self.assertEqual(m["high_vp"],[6*level-2,2,0])
                    self.assertEqual(m["high_ap_paid"],20)
                    self.assertEqual(m["active_high_effects"],1)
                    self.assertGreaterEqual(m["ally_step_hp_restored"],
                         self.cell(level,opponent,"baseline")["metrics"]["ally_step_hp_restored"])

    def test_05_prepared_shelter_uses_real_sentry_vigor_packets(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                m=self.cell(level,opponent,"prepared_shelter")["metrics"]
                self.assertEqual(m["high_casts"],[{
                    "technique":"Vital Shelter","access":"prepared",
                    "action_ap":20,"spent":1,"surcharge":0,"committed":2}])
                self.assertEqual(m["high_vp"],[6*level-3,2,1])
                self.assertEqual(m["high_ap_paid"],20)
                self.assertEqual(m["active_high_effects"],1)
                baseline=self.cell(level,opponent,"baseline")["metrics"]
                if opponent=="sentry_prepared":
                    self.assertGreater(m["vigor_prevented"],0)
                    self.assertLess(m["vigor_applied"],baseline["vigor_applied"])
                else:
                    self.assertEqual(m["vigor_prevented"],0)

    def test_06_prepared_heal_is_real_paid_primary_not_step_two(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                c=self.cell(level,opponent,"prepared_heal")["metrics"]
                self.assertEqual(c["high_casts"],[{"technique":"Basic Heal",
                    "access":"prepared","action_ap":20,"spent":2,
                    "surcharge":0,"committed":0}])
                self.assertEqual(c["high_vp"],[6*level-2,0,2])
                self.assertEqual(c["high_ap_paid"],20)
                self.assertEqual(c["primary_heal_hp"],2)
                self.assertGreater(c["primary_heal_vigor"],0)
                self.assertEqual(c["active_high_effects"],0)

    def test_07_unprepared_invocation_uses_true_full_turn_and_surcharge(self):
        for level in (1,2,3):
            for opponent in OPPONENTS:
                base_ap=30+6*(level-1)
                h=self.cell(level,opponent,"invoked_heal")["metrics"]
                self.assertEqual(h["high_casts"],[{"technique":"Basic Heal",
                    "access":"invocation","action_ap":base_ap,
                    "spent":2,"surcharge":1,"committed":0}])
                self.assertEqual(h["high_ap_paid"],base_ap)
                self.assertEqual(h["high_vp"],[6*level-3,0,3])
                self.assertEqual(h["high_open_prayer_fills"],0)
                self.assertEqual(h["primary_heal_hp"],2)
                w=self.cell(level,opponent,"invoked_shelter")["metrics"]
                self.assertEqual(w["high_casts"],[{"technique":"Vital Shelter",
                    "access":"invocation","action_ap":base_ap,
                    "spent":1,"surcharge":1,"committed":2}])
                self.assertEqual(w["high_vp"],[6*level-4,2,2])
                self.assertEqual(w["high_ap_paid"],base_ap)
                self.assertEqual(w["active_high_effects"],1)

    def test_08_l3_open_prayer_is_filled_once_at_prepared_price(self):
        for opponent in OPPONENTS:
            for policy,spell,spent,committed in (
                ("open_heal","Basic Heal",2,0),
                ("open_shelter","Vital Shelter",1,2),
            ):
                m=self.cell(3,opponent,policy)["metrics"]
                self.assertEqual(m["high_open_prayer_fills"],1)
                self.assertEqual(m["high_casts"],[{
                    "technique":spell,"access":"open_prayer",
                    "action_ap":20,"spent":spent,
                    "surcharge":0,"committed":committed}])
                self.assertEqual(m["high_ap_paid"],20)
                self.assertEqual(m["high_vp"],[18-spent-committed,
                                               committed,spent])
                self.assertEqual(m["active_high_effects"],int(committed>0))

    def test_09_l3_double_prepared_projection_is_40_of_42_not_free(self):
        for opponent in OPPONENTS:
            m=self.cell(3,opponent,"dual_prepared")["metrics"]
            self.assertEqual([v["technique"] for v in m["high_casts"]],
                             ["Guided Regeneration","Vital Shelter"])
            self.assertEqual([v["action_ap"] for v in m["high_casts"]],[20,20])
            self.assertEqual(m["high_ap_paid"],40)
            self.assertEqual(m["high_vp"],[13,4,1])
            self.assertEqual(m["active_high_effects"],2)
            self.assertEqual(m["high_open_prayer_fills"],0)

    def test_10_source_g5_payments_and_prayer_receipts_are_native_ordered(self):
        r=run_policy(level=3,opponent="sentry_prepared",policy="invoked_shelter")
        full=[v for v in rows(r,"action_committed")
              if v["detail"]["actor"]=="high"]
        self.assertEqual(len(full),1)
        self.assertEqual(full[0]["detail"]["action_class"],"full")
        self.assertEqual(full[0]["detail"]["ap_spent"],42)
        cast=rows(r,"b05_high_life_applied")
        self.assertEqual(len(cast),1)
        self.assertGreater(cast[0]["index"],full[0]["index"])
        self.assertLess(cast[0]["index"],rows(r,"g5_melee_resolved")[0]["index"])
        self.assertEqual(len(rows(r,"g45_attested_hit")),2)
        self.assertEqual(len(rows(r,"g3_effect_established")),1)

    def test_11_mutated_or_rehashed_metrics_cannot_attest(self):
        baseline=run_policy(level=3,opponent="soldier",policy="prepared_heal")
        self.assertEqual(attest_policy(
            baseline,level=3,opponent="soldier",policy="prepared_heal"),
            baseline)
        forged=deepcopy(baseline)
        forged["metrics"]["high_ap_paid"]=0
        with self.assertRaises(AssertionError):
            attest_policy(forged,level=3,opponent="soldier",
                          policy="prepared_heal")
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(forged,level=3,opponent="soldier",
                          policy="prepared_heal")
        with self.assertRaises(AssertionError):
            attest_policy(baseline,level=3,opponent="soldier",
                          policy="prepared_heal",seed=1)

    def test_12_illegal_levels_policies_and_seeds_fail_closed(self):
        cases=((True,"soldier","baseline",0),
               (4,"soldier","baseline",0),
               (0,"soldier","baseline",0),
               (2,"bogus","baseline",0),
               (2,"soldier","bogus",0),
               (2,"soldier","dual_prepared",0),
               (1,"soldier","open_heal",0),
               (2,"sentry_prepared","open_shelter",0),
               (3,"soldier","baseline",-1))
        for level,opponent,policy,seed in cases:
            with self.subTest(level=level,opponent=opponent,
                              policy=policy,seed=seed):
                with self.assertRaises(ValueError):
                    run_policy(level=level,opponent=opponent,
                               policy=policy,seed=seed)
        with self.assertRaises(ValueError):
            run_matrix(seed=True)

    def test_13_same_source_cannot_claim_prepared_invocation_or_second_open_slot(self):
        combat,x=scene(level=3,opponent="soldier",policy="open_heal",seed=0)
        e=combat.e
        e.start_turn("high")
        a=e.actors["high"]
        with self.assertRaises(UnresolvedDecision):
            x.cast("high","Basic Heal","ally",access="prepared",
                   mode="instant",die=3,hand_available=True)
        with self.assertRaises(UnresolvedDecision):
            x.cast("high","Guided Regeneration","ally",
                   access="invocation")
        self.assertEqual(a.ap_remaining,a.ap_total)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(18,0,0))
        # Live slot belongs to one unique unprepared name, no hindsight
        # switching to a different name once it is legally used.
        result=x.cast("high","Basic Heal","ally",access="open_prayer",
                      mode="instant",die=3,hand_available=True)
        self.assertIsNotNone(result)
        self.assertEqual(x.open_filled,"Basic Heal")
        self.assertFalse(x.open_slot)
        with self.assertRaises(UnresolvedDecision):
            x.cast("high","Vital Shelter","ally",access="open_prayer")
        self.assertEqual(a.vp_spent,2)

    def test_14_no_unsourced_opponent_or_unsupported_life_access(self):
        combat,x=scene(level=3,opponent="soldier",policy="baseline",seed=0)
        e=combat.e
        e.start_turn("high")
        a=e.actors["high"]
        initial=(a.ap_remaining,a.vp_available,len(e.ledger))
        with self.assertRaises(UnresolvedDecision):
            x.cast("high","Gentle Growth","ally")
        self.assertEqual((a.ap_remaining,a.vp_available,len(e.ledger)),initial)
        with self.assertRaises(ValueError):
            x.cast("high","Basic Heal","ally",mode="instant",
                   die=3,hand_available=False)
        self.assertEqual((a.ap_remaining,a.vp_available,len(e.ledger)),initial)

    def test_15_no_certification_from_any_witness(self):
        r=run_policy(level=1,opponent="sentry_prepared",policy="prepared_guided")
        self.assertFalse(r["independent_high_focus_certified"])
        self.assertFalse(r["full_encounter_certified"])
        self.assertFalse(r["three_focus_balance_certified"])
        self.assertIsNone(r["sampled_win_rate"])
        self.assertIsNone(r["policy_weighting"])


if __name__=="__main__":
    unittest.main()
