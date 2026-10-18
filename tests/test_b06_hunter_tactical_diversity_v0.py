"""B06 Phase 3 source-bound tactical/role diversity probes (not CR)."""
import json
import unittest
from unittest.mock import patch

from scripts.b06_hunter_tactical_diversity_v0 import (
    ROLE, CASES, SEEDS, HUNTER_FILE, attack, group, trial, census, die,
)


class HunterTacticalDiversityTests(unittest.TestCase):
    def test_role_profiles_are_bounded_by_authored_weapon_and_focus_math(self):
        self.assertEqual(ROLE["A"]["attack"], 7)  # STR2+AGI3+Sword2
        self.assertEqual(ROLE["B"]["attack"], 6)  # STR2+AGI2+Mace2
        self.assertEqual(ROLE["R"]["attack"], 4)  # STR2+Precision0+Bow2
        self.assertEqual(ROLE["F"]["attack"], 5)  # AGI3+Precision0+Throwing2
        self.assertEqual(ROLE["R"]["base"], 2)
        self.assertEqual(ROLE["R"]["die"], 4)
        self.assertEqual(ROLE["R"]["pen"], 3)
        self.assertIsNone(ROLE["R"]["guard"])
        self.assertIsNone(ROLE["F"]["guard"])
        self.assertEqual(ROLE["F"]["regen"], 3)  # VIT2 + High1
        self.assertEqual(ROLE["F"]["kind"], "flame")
        self.assertEqual(ROLE["F"]["action_ap"], 20)
        self.assertEqual(group(3, "mixed"), ("B1", "R1", "F1"))
        self.assertEqual(group(4, "mixed"), ("B1", "R1", "F1", "A1"))
        self.assertEqual(group(3, "original"), ("A1", "B1", "A2"))

    def test_native_crit_damage_once_bow_and_fire_vigor_separate(self):
        def scripted(_seed, sides, *key):
            if key[-1] == "attack": return 20
            if key[-1] == "confirm": return 14
            if key[-1] == "damage": return 3
            if "critical" in key: return 2
            if key[-1] == "burn": return 7
            self.fail(f"Unexpected roll key {key}")
        with patch("scripts.b06_hunter_tactical_diversity_v0.die",
                   side_effect=scripted):
            # critical +2d4(2+2) only on native bow's physical packet:
            bow = attack(0, ("R1", 0, "strike"), 4, 14,
                         packet_base=2, packet_sides=4, armor=3,
                         penetration=3)
            # Flame's primary Fire packet has its own critical dice and
            # Fire resistance 0; direct Vigor packet is untouched by critical.
            flame = attack(0, ("F1", 0, "strike"), 5, 14,
                           packet_base=2, packet_sides=None, armor=0,
                           penetration=0, burn=True)
        self.assertEqual(bow, (9, 0, "critical"))
        self.assertEqual(flame, (6, 5, "critical"))

    def test_terminals_stop_before_toxin_or_pounce(self):
        original_die = die
        def initiative_h_first(seed, sides, *key):
            if key == ("initiative", "H"): return 20
            if key[:1] == ("initiative",): return 1
            if "toxin" in key or "balance" in key:
                self.fail(f"Invalid post-terminal roll {key}")
            return original_die(seed, sides, *key)
        def lethal(seed, key, *args, **kwargs):
            if key[:2] == ("H", "bite"):
                return (99, 0, "ordinary")
            self.fail(f"Attack after terminal wound {key}")
        with patch("scripts.b06_hunter_tactical_diversity_v0.die",
                   side_effect=initiative_h_first), \
             patch("scripts.b06_hunter_tactical_diversity_v0.attack",
                   side_effect=lethal):
            result = trial(2, 3, "mixed", "ambush", "exposed", 0)
        self.assertEqual(result["terminal"], "frontline_first_zero")
        self.assertTrue(result["pounce_declared"])
        self.assertFalse(result["balance_resolved"])
        self.assertIsNone(result["toxin"])
        self.assertEqual(result["pc_attacks"], 0)

    def test_unsupported_combinations_fail_and_fixed_seed_replays(self):
        bad_cases = ((1, 3, "mixed", "warned", "armored", 0),
                     (2, 5, "mixed", "ambush", "exposed", 0),
                     (3, 3, "mixed", "surprised", "armored", 0),
                     (2, 3, "alien", "warned", "armored", 0),
                     (2, 3, "mixed", "warned", "armored", -1))
        for vals in bad_cases:
            with self.subTest(vals=vals), self.assertRaises(ValueError):
                trial(*vals)
        with self.assertRaises(ValueError):
            census(seeds=0)
        for seed in (0, 3, 31, 127):
            for roster in ("mixed", "original"):
                values = (3, 4, roster, "ambush", "exposed", seed)
                self.assertEqual(trial(*values), trial(*values))

    def test_seed_matrix_preserves_first_window_and_resource_invariants(self):
        hunter = json.loads(HUNTER_FILE.read_text(encoding="utf-8"))
        self.assertEqual(len(CASES), 32)
        self.assertEqual(SEEDS, 128)
        results = census(seeds=SEEDS, hunter=hunter)
        self.assertEqual(len(results), 32)
        for row in results:
            with self.subTest(case=row["scenario"]):
                self.assertEqual(sum(row["terminal"].values()), SEEDS)
                self.assertGreaterEqual(row["vp_spent"], 0)
                self.assertGreaterEqual(row["arrows_fired"], 0)
                self.assertLessEqual(row["balance_resolved"],
                                     row["pounce_declared"])
                self.assertLessEqual(row["full_toxin"] + row["reduced_toxin"],
                                     SEEDS)
                if "-warned-" in row["scenario"]:
                    self.assertEqual(row["pounce_declared"], 0)
                if "-original-" in row["scenario"]:
                    self.assertEqual(row["vp_spent"], 0)
                    self.assertEqual(row["arrows_fired"], 0)

    def test_one_round_vp_ammo_and_hunter_first_zero_semantics(self):
        for level in (2, 3):
            for seed in range(16):
                for party in ("mixed", "original"):
                    result = trial(level, 4, party, "warned", "armored", seed)
                    self.assertLessEqual(result["vp_spent"], 6 * level)
                    self.assertLessEqual(result["arrows_fired"], 2)
                    self.assertGreaterEqual(result["hunter_vigor"], 0)
                    self.assertIn(result["terminal"],
                                  ("round_one_complete", "hunter_first_zero",
                                   "frontline_first_zero", "wound_unresolved"))
                    if result["pounce_declared"]:
                        self.fail("Warned adjacency cannot create Pounce")

if __name__ == "__main__":
    unittest.main()
