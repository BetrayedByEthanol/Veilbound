"""Native G8 Soldier/Sentry four-party terminal evidence and tamper rejection."""
from copy import deepcopy
import unittest

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_soldier_sentry_g5_v0 import fixed_scene
from scripts.b06_g8_soldier_sentry_full_pack_v0 import (
    HISTORICAL_PHASE3_SHA, MODES, OPPONENTS, PARTY,
    _scene, attest_policy, run_pack, run_policy,
)


class SoldierSentryG8Tests(unittest.TestCase):
    def test_01_all_three_opponents_have_real_three_terminal_l3_matrix(self):
        for opponent in OPPONENTS:
            with self.subTest(opponent=opponent):
                report = run_pack(opponent=opponent, level=3, seed=0)
                self.assertTrue(report["bounded_three_terminal_matrix_certified"])
                self.assertEqual(set(report["terminals"]), set(MODES))
                self.assertEqual(report["terminals"]["party_defeat"],
                                 "party_defeat")
                self.assertEqual(report["terminals"]["opposed_withdrawal"],
                                 "party_scene_withdrawal")
                self.assertFalse(report["complete_representative_party_pack_certified"])
                self.assertIsNone(report["sampled_win_rate"])
                self.assertIsNone(report["hunter_cr"])

    def test_02_l2_authentic_source_roles_and_fixed_terminal_matrix(self):
        for opponent in OPPONENTS:
            with self.subTest(opponent=opponent):
                report = run_pack(opponent=opponent, level=2, seed=17)
                self.assertTrue(report["bounded_three_terminal_matrix_certified"])
                self.assertEqual(report["historical_phase3_sha256"],
                                 HISTORICAL_PHASE3_SHA)

    def test_03_four_fatal_party_victims_are_not_hp_assigned(self):
        for opponent in ("soldier", "sentry_prepared"):
            with self.subTest(opponent=opponent):
                report = run_policy(opponent=opponent, level=3,
                                    seed=1, mode="party_defeat")
                ledger = report["ledger"]
                fatalities = [x for x in ledger
                              if x["kind"] == "g4_damage_applied"
                              and x["detail"].get("dead") is True
                              and x["detail"].get("recipient") in PARTY]
                self.assertEqual({x["detail"]["recipient"] for x in fatalities},
                                 set(PARTY))
                self.assertTrue(all(report["final_state"][a]["dead"] for a in PARTY))
                self.assertFalse(report["final_state"]["foe"]["dead"])
                self.assertGreaterEqual(len(
                    [x for x in ledger if x["kind"]=="g5_melee_resolved"
                     and x["detail"].get("attacker")=="foe"]), 8)
                self.assertTrue(report["bounded_source_terminal_certified"])

    def test_04_withdrawal_requires_four_real_source_border_arrivals(self):
        for opponent in OPPONENTS:
            with self.subTest(opponent=opponent):
                report = run_policy(opponent=opponent, level=3,
                                    mode="opposed_withdrawal")
                ledger = report["ledger"]
                exits = [x for x in ledger if x["kind"]=="g5_terminal_exit"]
                self.assertEqual({x["detail"]["actor"] for x in exits},
                                 set(PARTY))
                for exit in exits:
                    person = exit["detail"]["actor"]
                    self.assertTrue(any(x["kind"]=="g1_movement_step"
                                        and x["detail"].get("actor")==person
                                        and x["index"]<exit["index"]
                                        for x in ledger))
                self.assertTrue(any(x["kind"]=="g5_melee_resolved"
                                    and x["detail"].get("attacker")=="foe"
                                    for x in ledger))
                self.assertFalse(report["final_state"]["foe"]["dead"])
                self.assertFalse(any(report["final_state"][a]["dead"]
                                     for a in PARTY))

    def test_05_cold_sentry_uses_projection_and_not_free_enchantment(self):
        cold = run_policy(opponent="sentry_cold", level=3,
                          mode="opposed_withdrawal")
        prepared = run_policy(opponent="sentry_prepared", level=3,
                              mode="opposed_withdrawal")
        self.assertGreater(cold["rounds_completed"], prepared["rounds_completed"])
        self.assertTrue(any(x["kind"]=="g3_effect_established"
                            and x["detail"].get("caster")=="foe"
                            for x in cold["ledger"]))
        self.assertTrue(any(x["kind"]=="vp_transition"
                            and x["detail"].get("actor")=="foe"
                            and x["detail"].get("mode")=="committed"
                            for x in cold["ledger"]))
        self.assertEqual(cold["final_state"]["foe"]["vp_committed"], 3)
        self.assertEqual(prepared["final_state"]["foe"]["vp_committed"], 3)

    def test_06_opt_in_preserves_hunter_only_default(self):
        legacy = fixed_scene("I1")
        legacy.bridge.start_next_turn(RegenerationChoice())
        legacy.bridge.end_current_turn()
        legacy.bridge.start_next_turn(RegenerationChoice())
        with self.assertRaisesRegex(UnresolvedDecision, "Hunter"):
            legacy.declare("front", "foe", profiles=("B06-PC-A-SWORD",),
                           defenses=("take_hit",))
        scoped = _scene("soldier", 3, 0, "party_victory")
        scoped.bridge.start_next_turn(RegenerationChoice())
        scoped.bridge.end_current_turn()
        scoped.bridge.start_next_turn(RegenerationChoice())
        sequence = scoped.declare("vanguard", "foe",
                                  profiles=("B06-PC-A-SWORD",),
                                  defenses=("take_hit",))
        result = scoped.resolve(sequence, 0, attack_face=12, damage_face=4,
                                wound_location_roll=8)
        self.assertEqual(result["outcome"], "hit")
        self.assertEqual(scoped.pending_attack_slots(), ())

    def test_07_public_report_tampering_rehash_and_terminal_claim_rejected(self):
        result = run_policy(opponent="soldier", level=3,
                            seed=0, mode="party_victory")
        self.assertEqual(attest_policy(result, opponent="soldier", level=3,
                                       seed=0, mode="party_victory"), result)
        variants = []
        public = deepcopy(result)
        public["outcome"] = "party_defeat"
        variants.append(public)
        public = deepcopy(result)
        public["ledger"][0]["detail"]["policy"] = "forged_policy"
        public["ledger_sha256"] = canonical_digest(public["ledger"])
        variants.append(public)
        public = deepcopy(result)
        event = next(x for x in public["ledger"] if x["kind"]=="g5_melee_roll")
        event["detail"]["attack_face"] = 20
        public["ledger_sha256"] = canonical_digest(public["ledger"])
        variants.append(public)
        public = deepcopy(result)
        public["bounded_source_terminal_certified"] = False
        variants.append(public)
        public = deepcopy(result)
        public["final_state"]["foe"]["hp"] = 12
        variants.append(public)
        for variant in variants:
            with self.subTest(change=variants.index(variant)):
                with self.assertRaises(AssertionError):
                    attest_policy(variant, opponent="soldier",
                                  level=3, seed=0, mode="party_victory")

    def test_08_invalid_source_scope_rejected(self):
        for kwargs in (
            dict(opponent="hunter", level=3, seed=0, mode="party_victory"),
            dict(opponent="soldier", level=1, seed=0, mode="party_victory"),
            dict(opponent="soldier", level=3, seed=-1, mode="party_victory"),
            dict(opponent="soldier", level=3, seed=0, mode="fake"),
            dict(opponent="soldier", level=True, seed=0, mode="party_victory"),
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_policy(**kwargs)

    def test_09_repeatable_native_digest_and_no_representative_claim(self):
        first = run_policy(opponent="sentry_prepared", level=3,
                           seed=17, mode="party_victory")
        second = run_policy(opponent="sentry_prepared", level=3,
                            seed=17, mode="party_victory")
        self.assertEqual(first, second)
        self.assertEqual(first["ledger_sha256"], canonical_digest(first["ledger"]))
        self.assertTrue(first["bounded_source_terminal_certified"])
        self.assertFalse(first["complete_representative_party_pack_certified"])
        self.assertFalse(first["representative_encounter_calibration_accepted"])
        self.assertIsNone(first["sampled_win_rate"])


if __name__ == "__main__":
    unittest.main()
