"""L1 real source-party combat against the unchanged B06 Soldier."""
from copy import deepcopy
import unittest

from scripts.b04_b05_b06_l1_source_native_combat_v0 import (
    ENEMY_SOURCE, LEVEL, MAX_ROUNDS, PARTY, POLICIES, ROLES,
    _scene, attest_policy, run_pack, run_policy,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision


class LevelOneSourceNativeCombatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports = {policy: run_policy(policy=policy, seed=0)
                       for policy in POLICIES}

    def test_source_roles_are_actual_l1_not_l2_g8_proxies(self):
        self.assertEqual(LEVEL, 1)
        self.assertEqual(ROLES, {"fire": "F", "medium": "S", "low": "T"})
        c = _scene("favorable_offense", 0)
        self.assertEqual(c.e.actors["foe"].source.source_id, ENEMY_SOURCE)
        self.assertEqual(c.e.actors["foe"].level, 3)
        self.assertEqual({n: c.e.actors[n].level for n in PARTY},
                         {n: 1 for n in PARTY})
        self.assertEqual({n: c.e.actors[n].source.source_id for n in PARTY},
                         ROLES)
        self.assertTrue(all(c.e.actors[n].source.digest for n in PARTY))
        self.assertNotIn("A", ROLES.values())
        self.assertNotIn("B", ROLES.values())

    def test_favorable_policy_paid_swords_flame_and_actual_g4_terminal(self):
        r = self.reports["favorable_offense"]
        self.assertEqual(r["outcome"], "soldier_defeat")
        self.assertTrue(r["bounded_source_terminal_certified"])
        self.assertTrue(r["final_state"]["foe"]["dead"])
        self.assertGreater(r["native_melee_results"], 1)
        self.assertGreater(r["native_g4_damage_receipts"], 0)
        self.assertEqual(r["native_flame_launches"], 1)
        self.assertEqual(r["final_vp_spent"]["fire"], 2)
        self.assertLessEqual(r["rounds_completed"], MAX_ROUNDS)
        self.assertTrue(any(ev["kind"] == "g4_damage_applied" and
                            ev["detail"].get("recipient") == "foe" and
                            ev["detail"].get("dead") is True
                            for ev in r["ledger"]))

    def test_withdrawal_uses_g1_border_g5_and_live_enemy_attacks(self):
        r = self.reports["opposed_withdrawal"]
        self.assertEqual(r["outcome"], "party_scene_withdrawal")
        self.assertTrue(r["bounded_source_terminal_certified"])
        self.assertEqual(r["native_scene_exits"], len(PARTY))
        self.assertFalse(r["final_state"]["foe"]["dead"])
        self.assertEqual(r["native_flame_launches"], 0)
        self.assertTrue(all(not r["final_state"][n]["dead"] for n in PARTY))
        self.assertTrue(any(ev["kind"] == "g5_melee_resolved" and
                            ev["detail"]["attacker"] == "foe" and
                            ev["detail"]["outcome"] == "hit"
                            for ev in r["ledger"]))
        self.assertTrue(any(ev["kind"] == "g1_movement_step" for ev in r["ledger"]))

    def test_each_attack_source_ap_and_ledger_sha_attested(self):
        for policy, r in self.reports.items():
            with self.subTest(policy=policy):
                self.assertEqual(attest_policy(r, policy=policy), r)
                actions = [x for x in r["ledger"]
                           if x["kind"] == "action_committed"]
                self.assertTrue(actions)
                self.assertTrue(any(x["detail"]["actor"] == "foe"
                                    for x in actions))
                self.assertTrue(any(x["kind"] == "round_end"
                                    for x in r["ledger"]))
                self.assertGreater(r["source_digests"]["foe"], "")

    def test_no_automatic_refill_or_absent_level_awards(self):
        for r in self.reports.values():
            self.assertFalse(r["externally_observed_player_decisions"])
            self.assertFalse(r["complete_twelve_focus_l1_coverage"])
            self.assertFalse(r["independently_full_focus_certified"])
            self.assertFalse(r["representative_difficulty_calibrated"])
            self.assertIsNone(r["statistical_win_rate"])
            self.assertIsNone(r["hunter_cr"])
            self.assertEqual(r["opponent_source_level"], 3)
            self.assertFalse(any(x["kind"] in ("gm_milestone_awarded",
                                              "xp_awarded", "recovery_six_hours")
                                 for x in r["ledger"]))

    def test_bad_policy_seed_and_bool_seed_rejected(self):
        for kwargs in ({"policy": "L2_G8_victory", "seed": 0},
                       {"policy": "favorable_offense", "seed": -1},
                       {"policy": "favorable_offense", "seed": True},
                       {"policy": "opposed_withdrawal", "seed": 1.2}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_policy(**kwargs)

    def test_tampered_report_even_rehashed_rejected(self):
        r = deepcopy(self.reports["favorable_offense"])
        r["outcome"] = "party_defeat"
        with self.assertRaises(AssertionError):
            attest_policy(r, policy="favorable_offense")
        r = deepcopy(self.reports["opposed_withdrawal"])
        r["source_digests"]["medium"] = "0" * 64
        with self.assertRaises(AssertionError):
            attest_policy(r, policy="opposed_withdrawal")

    def test_original_g8_stays_l2_l3_only(self):
        from scripts.b06_g8_soldier_sentry_full_pack_v0 import run_policy as g8
        with self.assertRaisesRegex(ValueError, "L2/L3"):
            g8(opponent="soldier", level=1, seed=0, mode="party_victory")

    def test_pack_has_two_source_terminals_not_a_win_rate(self):
        p = run_pack(seed=0)
        self.assertEqual(p["total_policies"], 2)
        self.assertEqual(p["terminal_count"], 2)
        self.assertTrue(p["all_terminal"])
        self.assertEqual(p["outcomes"], {
            "favorable_offense": "soldier_defeat",
            "opposed_withdrawal": "party_scene_withdrawal"})
        self.assertEqual(p["external_human_sessions"], 0)
        self.assertEqual(p["independent_focus_certificates"], 0)
        self.assertEqual(p["strict_mvp_exits_met"], 0)

    def test_live_original_sword_source_wielding_required(self):
        c = _scene("favorable_offense", 0)
        # Source equipment ownership alone must not enable an unwielded sword.
        c.e.g2.wielded["medium"].clear()
        with self.assertRaises(UnresolvedDecision):
            from scripts.b05_scholar_native_sword_v0 import (
                SWORD_IDS, scholar_sword_profile)
            scholar_sword_profile(c.e.actors["medium"], SWORD_IDS["S"],
                                  encounter=c.e)


if __name__ == "__main__":
    unittest.main()
