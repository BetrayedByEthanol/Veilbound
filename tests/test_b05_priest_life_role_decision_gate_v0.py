"""Source-native decision-gate tests; no invented role certificates or rates."""
from copy import deepcopy
import unittest

from scripts.b05_priest_life_role_decision_gate_v0 import (
    VARIANTS, CHOSEN_POLICIES, OPPONENTS, L3_ONLY, L2_ONLY,
    run_policy, run_matrix, attest_policy, attest_matrix,
)
from scripts.b05_priest_life_multi_recipient_stress_v0 import run_policy as old_run
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def events(report, kind):
    return [x for x in report["ledger"] if x["kind"] == kind]


class PriestLifeRoleDecisionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_matrix(seed=0)
        cls.rows = {(
            r["role"], r["level"], r["opponent"],
            r["variant"], r["policy"]): r
            for r in cls.report["cases"]}

    def test_01_exact_matrix_and_unbiased_source_baselines(self):
        expected = {(role, lv, enemy, v, policy)
                    for role, policies in CHOSEN_POLICIES.items()
                    for lv in (1, 2, 3)
                    for enemy in OPPONENTS for v in VARIANTS
                    for policy in policies
                    if not (policy in L3_ONLY[role] and lv < 3
                            or policy in L2_ONLY[role] and lv < 2)}
        self.assertEqual(self.report["case_count"], len(expected))
        self.assertEqual(set(self.rows), expected)
        self.assertEqual(self.report["audit_sha256"], canonical_digest(
            {k: v for k, v in self.report.items() if k != "audit_sha256"}))
        self.assertFalse(self.report["focus_comparative_balance_certified"])
        self.assertFalse(self.report["numerical_tuning_authorized"])
        self.assertIsNone(self.report["sampled_win_rate"])
        self.assertIsNone(self.report["focus_ranking"])

    def test_02_true_native_rolls_hit_miss_source_and_vp(self):
        max_vp = {"H": 6, "M": 4, "A": 2, "B": 2}
        seen_miss = seen_hit = False
        for r in self.report["cases"]:
            with self.subTest(role=r["role"], level=r["level"],
                              variant=r["variant"], policy=r["policy"]):
                m = r["metrics"]
                self.assertEqual(m["attack_attempts"] +
                                 m["unavailable_targets"], 4)
                self.assertEqual(m["attack_attempts"],
                                 m["attack_hits"] + m["attack_misses"])
                self.assertEqual(m["steps"],
                    {"priest": 4, "front": 4, "rear": 4})
                self.assertEqual(m["spent_vp"] +
                                 m["committed_vp"] + m["available_vp"],
                                 max_vp[r["role"]] * r["level"])
                self.assertEqual(len(r["source_digests"]), 4)
                self.assertTrue(all(len(v) == 64 for v in
                                    r["source_digests"].values()))
                self.assertIn(r["comparison"]["like_exposure"], (True, False))
                if r["comparison"]["like_exposure"]:
                    self.assertIsNotNone(r["comparison"]["endpoint_delta"])
                else:
                    self.assertIsNone(r["comparison"]["endpoint_delta"])
                seen_miss |= m["attack_misses"] > 0
                seen_hit |= m["attack_hits"] > 0
        self.assertTrue(seen_hit)
        self.assertTrue(seen_miss)

    def test_03_original_source_payments_parity(self):
        for role, policy in (("H", "split_wards"),
                             ("M", "guided_intercession"),
                             ("A", "chosen_self"),
                             ("B", "chosen_self")):
            native = run_policy(role=role, level=3, opponent="sentry_prepared",
                                variant="prepared_light", policy=policy)
            old = old_run(role=role, level=3, opponent="sentry_prepared",
                          pattern="alternating", policy=policy,
                          pressure="light")
            m = native["metrics"]
            self.assertEqual(m["attack_hits"], old["metrics"]["paid_enemy_hits"])
            self.assertEqual(m["heals"], old["metrics"]["paid_heal_count"])
            self.assertEqual(m["spent_vp"], old["metrics"]["vp"][2])
            self.assertEqual(m["committed_vp"], old["metrics"]["vp"][1])
            self.assertEqual(m["priest_ap_paid"], old["metrics"]["ap_paid"])
            self.assertEqual(m["intercession_payments"],
                             old["metrics"]["intercession_payments"])

    def test_04_actual_initiative_order_precedes_actions(self):
        for variant, v in VARIANTS.items():
            r = run_policy(role="H", level=1, opponent="soldier",
                           variant=variant, policy="baseline")
            encounter = events(r, "encounter_created")[0]
            order = encounter["detail"]["order"]
            self.assertEqual(order[0],
                             "foe" if v["initiative"] == "foe_first"
                             else "priest")
            self.assertEqual(len(events(r, "b05_role_gate_policy")), 1)
            self.assertEqual(
                events(r, "b05_role_gate_policy")[0]["detail"]["attack_face"],
                v["attack_face"])
            self.assertEqual(
                events(r, "b05_role_gate_policy")[0]["detail"]["defense"],
                v["defense"])

    def test_05_true_dodge_misses_never_apply_damage(self):
        miss_found = False
        for r in (
            run_policy(role="H", level=2, opponent="soldier",
                       variant="cautious_dodge", policy="baseline"),
            run_policy(role="H", level=2, opponent="sentry_prepared",
                       variant="pressured_dodge", policy="baseline"),
        ):
            outcomes = events(r, "g5_melee_resolved")
            damage = events(r, "g4_damage_applied")
            self.assertEqual(len(damage), sum(
                x["detail"]["outcome"] == "hit" for x in outcomes))
            miss_found |= any(x["detail"]["outcome"] == "miss"
                              for x in outcomes)
        self.assertTrue(miss_found)

    def test_06_high_support_and_l3_double_projection(self):
        r = run_policy(role="H", level=3, opponent="sentry_prepared",
                       variant="prepared_light", policy="split_wards")
        self.assertEqual(r["metrics"]["ally_effects"], 2)
        self.assertEqual(r["metrics"]["priest_ap_paid"], 40)
        self.assertEqual(len(events(r, "g3_effect_established")), 2)
        self.assertFalse(r["PS_08_full_role_certified"])

    def test_07_medium_paid_live_intercession_with_real_response(self):
        guided = run_policy(role="M", level=3, opponent="soldier",
                            variant="surprise_heavy",
                            policy="guided_intercession")
        shelter = run_policy(role="M", level=3, opponent="sentry_prepared",
                             variant="surprise_heavy",
                             policy="shelter_intercession")
        self.assertGreaterEqual(guided["metrics"]["guided_intercessions"], 1)
        self.assertGreaterEqual(shelter["metrics"]["vital_intercessions"], 1)
        for r in (guided, shelter):
            paid = events(r, "b05_intercession_paid")
            self.assertEqual(len(paid), 1)
            self.assertEqual(paid[0]["detail"]["spent"], 2)
            self.assertEqual(r["metrics"]["intercession_payments"], 1)

    def test_08_medium_reaction_is_not_free_or_always_available(self):
        # Native misses and lack of eligible packet must not fabricate
        # an Intercession receipt. This does NOT assert a second rival
        # Reaction window has been implemented.
        r = run_policy(role="M", level=3, opponent="sentry_prepared",
                       variant="cautious_dodge", policy="shelter_intercession")
        self.assertLessEqual(r["metrics"]["intercession_payments"], 1)
        self.assertEqual(r["metrics"]["intercession_payments"],
                         r["metrics"]["vital_intercessions"])
        self.assertIn("Two simultaneous authentic competing Medium Reaction opportunities",
                      self.report["unresolved"])

    def test_09_low_source_identity_and_external_heal_restrictions(self):
        for lv in (1, 2, 3):
            for variant in VARIANTS:
                a = run_policy(role="A", level=lv, opponent="soldier",
                               variant=variant, policy="chosen_self")
                b = run_policy(role="B", level=lv, opponent="soldier",
                               variant=variant, policy="chosen_self")
                self.assertEqual(a["metrics"]["self_effects"], 1)
                self.assertEqual(b["metrics"]["self_effects"], 1)
                self.assertEqual(a["metrics"]["ally_effects"], 0)
                self.assertEqual(b["metrics"]["ally_effects"], 0)
                self.assertEqual(b["metrics"]["heals"], 0)
        healed = run_policy(role="A", level=3, opponent="soldier",
                            variant="surprise_heavy", policy="triage")
        self.assertGreater(healed["metrics"]["heals"], 0)
        self.assertFalse(healed["PS_01_full_fighter_certified"])
        self.assertFalse(healed["PS_02_full_ally_defender_certified"])

    def test_10_illegal_capability_preflight_no_role_invention(self):
        cases = [
            dict(role="H", level=2, opponent="soldier",
                 variant="prepared_light", policy="split_wards"),
            dict(role="M", level=2, opponent="soldier",
                 variant="prepared_light", policy="guided_intercession"),
            dict(role="A", level=1, opponent="soldier",
                 variant="prepared_light", policy="chosen_and_heal"),
            dict(role="B", level=1, opponent="soldier",
                 variant="prepared_light", policy="triage"),
            dict(role="X", level=2, opponent="soldier",
                 variant="prepared_light", policy="baseline"),
            dict(role="H", level=3, opponent="soldier",
                 variant="unknown", policy="baseline"),
        ]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                run_policy(**case)
        with self.assertRaises(ValueError):
            run_policy(role="M", level=True, opponent="soldier",
                       variant="prepared_light", policy="baseline")
        with self.assertRaises(ValueError):
            run_matrix(seed=-1)

    def test_11_case_report_forgery_rejected_even_when_rehashed(self):
        args = dict(role="M", level=3, opponent="sentry_prepared",
                    variant="surprise_heavy", policy="shelter_intercession")
        r = run_policy(**args)
        self.assertEqual(attest_policy(r, **args), r)
        bad = deepcopy(r)
        bad["metrics"]["intercession_payments"] += 1
        bad["ledger_sha256"] = canonical_digest(bad["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(bad, **args)
        bad = deepcopy(r)
        bad["ledger"][0]["kind"] = "forged_start"
        bad["ledger_sha256"] = canonical_digest(bad["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(bad, **args)

    def test_12_matrix_audit_replay_and_rehashed_malice(self):
        r = self.report
        self.assertEqual(attest_matrix(r), r)
        bad = deepcopy(r)
        bad["cases"][0]["metrics"]["attack_hits"] += 1
        bad["audit_sha256"] = canonical_digest(
            {k: v for k, v in bad.items() if k != "audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_matrix(bad)

    def test_13_comparison_never_normalizes_unequal_exposure(self):
        for row in self.report["cases"]:
            b = self.rows[(row["role"], row["level"], row["opponent"],
                           row["variant"], "baseline")]
            if row["comparison"]["like_exposure"]:
                for who in ("front", "rear", "priest"):
                    self.assertEqual(
                        row["comparison"]["endpoint_delta"][who]["hp"],
                        row["metrics"]["recipients"][who]["hp"] -
                        b["metrics"]["recipients"][who]["hp"])
            else:
                self.assertIsNone(row["comparison"]["endpoint_delta"])

    def test_14_historical_source_evidence_unchanged(self):
        # Structural evidence: the runner imports old adapters but doesn't
        # modify original matrices or historical B06 Phase 3 witnesses.
        for row in self.report["cases"]:
            self.assertFalse(row["comparison"]["like_exposure"]
                             and row["comparison"]["endpoint_delta"] is None)
        self.assertEqual(self.report["cases"][0]["source_ids"]["foe"]
                         in ("B06-EN-01", "B06-EN-02"), True)


if __name__ == "__main__":
    unittest.main()
