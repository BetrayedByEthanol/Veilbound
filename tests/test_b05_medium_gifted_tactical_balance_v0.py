"""Source-native, fixed-policy Medium Gifted tactical/attrition checks."""
import json
import unittest
from copy import deepcopy

from scripts.b05_medium_gifted_tactical_balance_v0 import (
    LEVELS, SCENARIOS, run_case, run_matrix, attest_case, attest_matrix,
)


def rows(report,kind):
    return [x for x in report["ledger"] if x["kind"]==kind]


class MediumGiftedTacticalBalanceV0Tests(unittest.TestCase):
    def test_01_matrix_exact_21_cases_without_creeping_certification(self):
        report=run_matrix(seed=161)
        self.assertEqual(len(report["cases"]),21)
        self.assertEqual(report["summary"]["cases"],21)
        self.assertEqual(report["summary"]["levels"],[1,2,3])
        self.assertIsNone(report["summary"]["win_rate"])
        self.assertFalse(report["summary"]["full_focus_certified"])
        self.assertFalse(report["summary"]["representative_encounter"])
        self.assertFalse(report["summary"]["numerical_tuning_authorized"])
        self.assertEqual({(r["opponent"],r["level"],r["policy"])
                          for r in report["cases"]},
                         {(o,lv,p) for o,spec in SCENARIOS.items()
                          for lv in LEVELS for p in spec["policies"]})

    def test_02_fear_vs_dormant_real_soldier_hp_across_four_rounds(self):
        for level in LEVELS:
            with self.subTest(level=level):
                fear=run_case(opponent="soldier",level=level,policy="fear")
                dormant=run_case(opponent="soldier",level=level,policy="dormant")
                a,b=fear["metrics"],dormant["metrics"]
                self.assertEqual(a["g5_attacks"],b["g5_attacks"])
                self.assertEqual(a["g5_attacks"],4)
                self.assertEqual(a["g5_hits"],4)
                self.assertEqual(a["g45_attested_hits"],4)
                self.assertEqual((a["pulse_count"],a["hp_prevented"]),(4,8))
                self.assertEqual((b["pulse_count"],b["hp_prevented"]),(0,0))
                self.assertGreaterEqual(a["recipient_hp"],b["recipient_hp"])
                self.assertEqual(a["gifted_vp_state"],[4*level-2,2,0])
                self.assertEqual(a["gifted_ap_ward"],24)
                self.assertEqual(a["regen_steps"],8)
                self.assertEqual(a["emotion_windows"],4)
                self.assertFalse(a["recipient_dead"])

    def test_03_dodge_is_real_g5_miss_not_free_ward(self):
        for level in LEVELS:
            r=run_case(opponent="soldier",level=level,policy="dodge")
            m=r["metrics"]
            self.assertEqual((m["g5_attacks"],m["g5_hits"]),(4,0))
            self.assertEqual((m["g4_source_packets"],m["pulse_count"]),(0,0))
            self.assertEqual(m["attack_defenses"],["dodge"]*4)
            self.assertEqual(m["recipient_hp"],12)
            self.assertEqual(len(rows(r,"g5_melee_roll")),4)
            self.assertFalse(rows(r,"g4_damage_applied"))

    def test_04_retune_keeps_grade_but_dormant_after_first_round(self):
        for level in LEVELS:
            m=run_case(opponent="soldier",level=level,policy="retune")["metrics"]
            self.assertEqual((m["pulse_count"],m["hp_prevented"]),(1,2))
            self.assertEqual(m["active_ward"],"Dormant")
            self.assertEqual(m["ward_instances"],1)
            self.assertEqual(m["gifted_vp_state"],[4*level-2,2,0])
            self.assertEqual(m["g5_hits"],4)

    def test_05_native_trust_compared_with_dormant_sentry(self):
        for level in LEVELS:
            t=run_case(opponent="sentry",level=level,policy="trust")
            d=run_case(opponent="sentry",level=level,policy="dormant")
            a,b=t["metrics"],d["metrics"]
            self.assertEqual((a["g5_attacks"],a["g5_hits"]),(2,2))
            self.assertEqual(a["g45_attested_hits"],2)
            self.assertEqual((a["pulse_count"],a["vigor_prevented"]),(2,4))
            self.assertEqual((b["pulse_count"],b["vigor_prevented"]),(0,0))
            self.assertGreaterEqual(a["recipient_vigor"],b["recipient_vigor"])
            self.assertEqual(a["gifted_position"],[[2,2]])
            self.assertEqual(a["gifted_ap_ward"],24)
            self.assertEqual(a["regen_steps"],6)
            self.assertEqual(a["emotion_windows"],2)
            self.assertEqual(a["gifted_vp_state"],[4*level-2,2,0])
            self.assertEqual(len(rows(t,"g5_melee_resolved")),2)

    def test_06_native_g1_reposition_removes_trust_range(self):
        for level in LEVELS:
            r=run_case(opponent="sentry",level=level,policy="diagonal")
            m=r["metrics"]
            self.assertEqual((m["pulse_count"],m["vigor_prevented"]),(1,2))
            self.assertEqual(m["gifted_position"],[[2,1]])
            self.assertEqual(m["recipient_position"],[[3,2]])
            self.assertEqual(m["movement_steps"],1)
            self.assertEqual(m["g45_attested_hits"],2)
            self.assertEqual(m["active_ward"],"Active")
            pulse=rows(r,"b05_medium_ward_pulse")
            self.assertEqual(len(pulse),1)
            self.assertEqual(pulse[0]["detail"]["recipient"],"ally")

    def test_07_each_source_packet_has_one_native_damage_and_wound_preflight(self):
        for opponent,spec in SCENARIOS.items():
            for level in LEVELS:
                for policy in spec["policies"]:
                    r=run_case(opponent=opponent,level=level,policy=policy)
                    m=r["metrics"]
                    self.assertEqual(m["g4_source_packets"],m["g5_hits"])
                    self.assertEqual(m["g45_attested_hits"],m["g5_hits"])
                    self.assertEqual(len(rows(r,"b05_medium_ward_placed")),1)
                    self.assertEqual(len(rows(r,"regeneration_step")),m["regen_steps"])
                    self.assertEqual(len(rows(r,"b05_medium_emotion_established")),
                                     spec["rounds"])
                    self.assertEqual(sum(x["detail"]["prevented"] for x in
                                         rows(r,"b05_medium_ward_pulse")),
                                     m["hp_prevented"]+m["vigor_prevented"])
                    self.assertEqual(m["gifted_ap_physical"],0)
                    self.assertEqual(len(rows(r,"action_committed")),
                                     spec["rounds"]+1)  # Paid Ward + every G5 sword.

    def test_08_source_and_ledger_digests_replay_and_tamper(self):
        r=run_case(opponent="sentry",level=2,policy="diagonal",seed=44)
        self.assertTrue(attest_case(r,opponent="sentry",level=2,
                                    policy="diagonal",seed=44))
        self.assertEqual(r,run_case(opponent="sentry",level=2,
                                    policy="diagonal",seed=44))
        self.assertFalse(attest_case(r,opponent="sentry",level=2,
                                     policy="diagonal",seed=45))
        changed=deepcopy(r)
        changed["metrics"]["vigor_prevented"]=99
        self.assertFalse(attest_case(changed,opponent="sentry",level=2,
                                     policy="diagonal",seed=44))
        changed=deepcopy(r)
        changed["ledger"][0]["detail"]["seed"]="forged"
        self.assertFalse(attest_case(changed,opponent="sentry",level=2,
                                     policy="diagonal",seed=44))

    def test_09_reject_invalid_policy_source_level_seed_without_commit(self):
        for kw in ({"opponent":"dragon","level":2,"policy":"fear"},
                   {"opponent":"soldier","level":0,"policy":"fear"},
                   {"opponent":"sentry","level":2,"policy":"fear"},
                   {"opponent":"soldier","level":2,"policy":"trust"},
                   {"opponent":"soldier","level":True,"policy":"fear"},
                   {"opponent":"soldier","level":2,"policy":"fear","seed":-1}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):
                run_case(**kw)
        with self.assertRaises(ValueError):
            run_matrix(seed=-1)

    def test_10_matrix_replay_rejects_rehashed_false_claim(self):
        r=run_matrix(seed=91)
        self.assertTrue(attest_matrix(r,seed=91))
        self.assertEqual(r,json.loads(json.dumps(r,allow_nan=False)))
        self.assertEqual(r,run_matrix(seed=91))
        forged=deepcopy(r)
        forged["summary"]["full_focus_certified"]=True
        self.assertFalse(attest_matrix(forged,seed=91))
        forged=deepcopy(r)
        forged["cases"][0]["metrics"]["g5_hits"]=-1
        self.assertFalse(attest_matrix(forged,seed=91))


if __name__=="__main__":
    unittest.main()
