"""G7-G: source-native Hunter pursuit/retarget, defeat and opposed escape."""
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_g7c_party_terminals_v0 import PartyTerminal
from scripts.b06_g7g_hunter_pursuit_terminals_v0 import (
    HISTORICAL_SHA, MAX_ROUNDS, MODES, _bite, _pursue, _route_to_contact,
    main, run_trial,
)
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene


class G7GNativeTests(unittest.TestCase):
    def test_01_fixed_native_multitarget_defeat_for_three_and_four(self):
        for level in (2, 3):
            for size in (3, 4):
                with self.subTest(level=level, size=size):
                    r = run_trial(level, size, 7, include_ledger=True)
                    self.assertEqual(r["outcome"], "party_defeat_attested")
                    self.assertTrue(r["hunter_alive"])
                    self.assertEqual(r["unique_hunter_bite_victims"],
                                     sorted(r["final_state"].keys() - {"hunter"}))
                    self.assertEqual(len(r["native_terminal"]["lethal_damage_indices"]), size)
                    self.assertLessEqual(r["rounds_completed"], MAX_ROUNDS)
                    self.assertEqual(r["turns_completed"],
                                     r["rounds_completed"] * (size + 1))
                    self.assertTrue(all(r["final_state"][p]["dead"]
                                        for p in r["final_state"] if p != "hunter"))
                    self.assertEqual(r["ledger_sha256"], canonical_digest(r["ledger"]))
                    self.assertEqual(sum(v["kind"] == "g7c_party_defeat_attested"
                                         for v in r["ledger"]), 1)
                    self.assertEqual(sum(v["kind"] == "g7g_multitarget_defeat_verified"
                                         for v in r["ledger"]), 1)
                    self.assertFalse(r["complete_party_pack_certified"])
                    self.assertFalse(r["representative_encounter_calibration_accepted"])
                    self.assertIsNone(r["hunter_cr"])
                    self.assertIsNone(r["sampled_win_rate"])

    def test_02_each_death_is_hunter_paid_bite_and_not_dying_attrition(self):
        r = run_trial(2, 4, 0, include_ledger=True)
        ledger = r["ledger"]
        for member in ("vanguard", "guardian", "archer", "scholar"):
            deaths = [v for v in ledger if v["kind"] == "g4_damage_applied"
                      and v["detail"].get("recipient") == member
                      and v["detail"].get("dead") is True]
            self.assertEqual(len(deaths), 1)
            self.assertEqual(deaths[0]["detail"]["cause"],
                             "source-profile:B06-AT-04")
            bridge = [v for v in ledger if v["kind"] == "g45_attested_hit"
                      and v["detail"].get("attacker") == "hunter"
                      and v["detail"].get("target") == member
                      and (v["detail"].get("actual_result") or {}).get("dead")]
            resolved = [v for v in ledger if v["kind"] == "g5_melee_resolved"
                        and v["detail"].get("attacker") == "hunter"
                        and v["detail"].get("target") == member
                        and (v["detail"].get("damage") or {}).get("dead")]
            self.assertEqual(len(bridge), 1)
            self.assertEqual(len(resolved), 1)
            self.assertEqual(bridge[0]["detail"]["action_index"],
                             resolved[0]["detail"]["action_index"])
            self.assertLess(deaths[0]["index"], bridge[0]["index"])
            self.assertLess(bridge[0]["index"], resolved[0]["index"])

    def test_03_living_hunter_escapes_are_real_second_round_exits(self):
        for level in (2, 3):
            for size in (3, 4):
                with self.subTest(level=level, size=size):
                    r = run_trial(level, size, 9, mode="opposed_disengagement",
                                  include_ledger=True)
                    self.assertEqual(r["outcome"], "party_withdrawal_attested")
                    self.assertTrue(r["hunter_alive"])
                    self.assertEqual(r["rounds_completed"], 2)
                    self.assertEqual(len(r["native_terminal"]["member_exits"]), size)
                    self.assertEqual(sum(v["kind"] ==
                                         "g7g_living_hunter_disengagement_verified"
                                         for v in r["ledger"]), 1)
                    proof = next(v["detail"] for v in r["ledger"]
                                 if v["kind"] == "g7g_living_hunter_disengagement_verified")
                    self.assertTrue(proof["ongoing_world_pursuit_not_adjudicated"])
                    self.assertTrue(proof["hunter_paid_bite_indices"])
                    self.assertEqual(len(proof["hunter_paid_bite_indices"]), 2)
                    self.assertEqual(len(proof["border_exit_indices"]), size)
                    self.assertEqual(r["ledger_sha256"], canonical_digest(r["ledger"]))
                    self.assertFalse(r["complete_party_pack_certified"])

    def test_04_native_pursuit_uses_real_mp_and_anatomical_front(self):
        r = run_trial(2, 3, 2, mode="opposed_disengagement",
                      include_ledger=True)
        ledger = r["ledger"]
        pursuing = [v for v in ledger if v["kind"] == "g7g_hunter_pursuit_executed"]
        self.assertEqual(len(pursuing), 1)
        witness = pursuing[0]
        self.assertEqual(witness["round"], 2)
        self.assertTrue(witness["detail"]["contact"])
        self.assertGreater(len(witness["detail"]["movement_indices"]), 0)
        for ix in witness["detail"]["movement_indices"]:
            step = ledger[ix]
            self.assertEqual(step["turn"], "hunter")
            self.assertEqual(step["round"], 2)
            self.assertEqual(step["kind"], "g1_movement_step")
            self.assertTrue(step["detail"]["cautious"])
            self.assertGreater(step["detail"]["cost"], 0)
        move = [v for v in ledger if v["kind"] == "g1_movement_step"
                and v["detail"]["actor"] == "vanguard"]
        self.assertEqual([v["round"] for v in move], [1, 2])

    def test_05_no_defeat_by_dying_or_fake_damage_and_no_early_exit(self):
        c = mixed_scene(level=2, size=3, seed=0, party_exits=True)
        for actor in c.e.order:
            c.bridge.start_next_turn(RegenerationChoice())
            c.bridge.end_current_turn()
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_defeat()
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_withdrawal()

    def test_06_no_attack_on_corpse_or_without_head_contact(self):
        c = mixed_scene(level=2, size=3, seed=0)
        c.bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(c.e.g1.melee_contact("hunter", "vanguard",
                                             hunter_front=True))
        with self.assertRaises(UnresolvedDecision):
            _bite(c, "archer", devastating=True)
        self.assertEqual(sum(v["kind"] == "action_committed"
                             for v in c.e.ledger), 0)

    def test_07_pursuit_preview_does_not_move_or_pay_hunter(self):
        c = mixed_scene(level=3, size=4, seed=2)
        c.bridge.start_next_turn(RegenerationChoice())
        e = c.e
        first = e.actors["hunter"].occupied
        ledger = len(e.ledger)
        path = _route_to_contact(e, "guardian")
        self.assertTrue(path)
        self.assertEqual(first, e.actors["hunter"].occupied)
        self.assertEqual(len(e.ledger), ledger)
        self.assertEqual(e.actors["hunter"].mp_remaining, 12)
        # The only real relocation must use G1 and appear in the ledger.
        _pursue(c, "guardian")
        self.assertGreater(sum(v["kind"] == "g1_movement_step"
                               and v["detail"].get("actor") == "hunter"
                               for v in e.ledger), 0)

    def test_08_parameter_rejection_and_seed_reproducibility(self):
        for wrong in ({"level": 1}, {"size": 2}, {"seed": -1},
                      {"mode": "invented"}, {"include_ledger": 1}):
            with self.subTest(wrong=wrong), self.assertRaises(ValueError):
                run_trial(**wrong)
        a = run_trial(3, 3, 11, mode="opposed_disengagement")
        b = run_trial(3, 3, 11, mode="opposed_disengagement")
        self.assertEqual(a, b)
        self.assertEqual(a["historical_phase3_sha256"], HISTORICAL_SHA)
        self.assertEqual(a["rounds_completed"], 2)

    def test_09_cli_emits_standalone_numerically_unrated_witness(self):
        stream = StringIO()
        with redirect_stdout(stream):
            main(["--mode", "opposed_disengagement", "--level", "2",
                  "--party-size", "3", "--seed", "1"])
        report = json.loads(stream.getvalue())
        self.assertIn(report["mode"], MODES)
        self.assertEqual(report["outcome"], "party_withdrawal_attested")
        self.assertFalse(report["complete_party_pack_certified"])
        self.assertIsNone(report["sampled_win_rate"])
        self.assertIsNone(report["hunter_cr"])


if __name__ == "__main__":
    unittest.main()
