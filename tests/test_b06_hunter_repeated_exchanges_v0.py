"""Repeated Hunter first-zero/first-wound simulation: stable, bounded evidence."""
import json
import unittest
from unittest.mock import patch

from scripts.b06_hunter_repeated_exchanges_v0 import (
    SEED_COUNT, DEFENSE_POLICIES, SCENARIOS, HUNTER_FILE,
    die, strike, simulate_trial, run_matrix,
)

# Pinned outcome counts over a small, explicitly selected seed census.
# NOT an empirical estimate or a certified challenge rating.
EXPECTED_HUNTER_FIRST_ZERO = {
    (2, 3, "warned", "guard"): 503,
    (2, 3, "warned", "dodge"): 503,
    (2, 3, "ambush", "guard"): 499,
    (2, 3, "ambush", "dodge"): 498,
    (2, 4, "warned", "guard"): 509,
    (2, 4, "warned", "dodge"): 509,
    (2, 4, "ambush", "guard"): 507,
    (2, 4, "ambush", "dodge"): 506,
    (3, 3, "warned", "guard"): 508,
    (3, 3, "warned", "dodge"): 508,
    (3, 3, "ambush", "guard"): 507,
    (3, 3, "ambush", "dodge"): 507,
    (3, 4, "warned", "guard"): 509,
    (3, 4, "warned", "dodge"): 509,
    (3, 4, "ambush", "guard"): 508,
    (3, 4, "ambush", "dodge"): 508,
}


class HunterRepeatedExchangeTests(unittest.TestCase):
    def test_replayable_branch_independent_keyed_rolls(self):
        for seed in (0, 1, 19, 511):
            self.assertEqual(die(seed, 20, "initiative", "H"),
                             die(seed, 20, "initiative", "H"))
            self.assertTrue(1 <= die(seed, 6, 1, "H", "damage") <= 6)
            self.assertEqual(
                simulate_trial(2, 3, "ambush", "guard", seed),
                simulate_trial(2, 3, "ambush", "guard", seed),
            )

    def test_natural_1_misses_and_nat20_confirmation_bonus_is_once(self):
        def pick(face, confirm, d6=3, d4=2):
            def roll(_seed, sides, *_key):
                if _key[-1] == "attack": return face
                if _key[-1] == "confirm": return confirm
                if _key[-1] == "damage": return d6
                if "bonus" in _key: return d4
                self.fail(f"Unexpected roll key {_key}")
            return roll
        packet = dict(base=3, penetration=1, target_armor=3)
        with patch("scripts.b06_hunter_repeated_exchanges_v0.die", side_effect=pick(1, 20)):
            self.assertEqual(strike(0, (1, "A"), 6, "guard", 17, **packet), (0, "miss"))
        with patch("scripts.b06_hunter_repeated_exchanges_v0.die", side_effect=pick(20, 1)):
            self.assertEqual(strike(0, (1, "A"), 6, "guard", 17, **packet), (6, "strong"))
        with patch("scripts.b06_hunter_repeated_exchanges_v0.die", side_effect=pick(20, 14)):
            self.assertEqual(strike(0, (1, "A"), 6, "guard", 17, **packet), (8, "critical"))
        with patch("scripts.b06_hunter_repeated_exchanges_v0.die", side_effect=pick(20, 20)):
            self.assertEqual(strike(0, (1, "A"), 6, "guard", 17, **packet), (8, "devastating"))
        with patch("scripts.b06_hunter_repeated_exchanges_v0.die", side_effect=pick(20, 1)):
            self.assertEqual(strike(0, (1, "A"), 6, "take_hit", 0, **packet), (8, "critical"))

    def test_unsupported_situations_are_not_fabricated(self):
        for bad in ((1, 3, "warned", "guard", 0),
                    (3, 5, "ambush", "guard", 0),
                    (2, 3, "surprised", "guard", 0),
                    (2, 3, "ambush", "auto_crit", 0),
                    (2, 3, "warned", "guard", -1)):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                simulate_trial(*bad)
        with self.assertRaises(ValueError):
            run_matrix(0)

    def test_critical_wound_is_not_played_through_unmodeled(self):
        results = [simulate_trial(2, 3, "warned", "guard", i) for i in range(512)]
        unresolved = [r for r in results if r["terminal"] == "devastating_wound_unresolved"]
        self.assertEqual(len(unresolved), 4)
        self.assertTrue(all(r["critical_events"] > 0 for r in unresolved))

    def test_matrix_exact_counts_and_category_conservation(self):
        self.assertEqual(len(SCENARIOS), 8)
        self.assertEqual(DEFENSE_POLICIES, ("guard", "dodge"))
        hunter = json.loads(HUNTER_FILE.read_text(encoding="utf-8"))
        self.assertEqual(hunter["defenses"]["hp_max"], 14)
        self.assertIsNone(hunter["defenses"]["guard_instrument"])
        observed = run_matrix(SEED_COUNT, hunter=hunter)
        self.assertEqual(len(observed), 16)
        for cell in observed:
            key = (cell["level"], cell["party_size"], cell["setup"], cell["defense"])
            with self.subTest(key=key):
                self.assertEqual(cell["terminal_counts"].get("hunter_first_zero", 0),
                                 EXPECTED_HUNTER_FIRST_ZERO[key])
                self.assertEqual(sum(cell["terminal_counts"].values()), SEED_COUNT)
                self.assertLessEqual(cell["pounce_attempts"],
                                     cell["hunter_initiative_first"])
                if cell["setup"] == "warned":
                    self.assertEqual(cell["pounce_attempts"], 0)
                self.assertLessEqual(cell["full_toxin"] + cell["reduced_toxin"], SEED_COUNT)
                self.assertLessEqual(cell["pounce_prone"], cell["pounce_attempts"])

if __name__ == "__main__":
    unittest.main()
