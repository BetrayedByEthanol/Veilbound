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


# Pinned Full/Reduced accepted toxin applications and genuinely resolved
# Pounce Balance checks, AFTER terminal Bite/Opportunity stop precedence.
EXPECTED_TOXIN_AND_BALANCE = {
    (2, 3, "warned", "guard"): (75, 101, 0),
    (2, 3, "warned", "dodge"): (94, 141, 0),
    (2, 3, "ambush", "guard"): (88, 107, 144),
    (2, 3, "ambush", "dodge"): (105, 147, 144),
    (2, 4, "warned", "guard"): (54, 74, 0),
    (2, 4, "warned", "dodge"): (72, 111, 0),
    (2, 4, "ambush", "guard"): (63, 78, 118),
    (2, 4, "ambush", "dodge"): (81, 115, 118),
    (3, 3, "warned", "guard"): (40, 62, 0),
    (3, 3, "warned", "dodge"): (56, 91, 0),
    (3, 3, "ambush", "guard"): (50, 65, 144),
    (3, 3, "ambush", "dodge"): (64, 95, 144),
    (3, 4, "warned", "guard"): (30, 48, 0),
    (3, 4, "warned", "dodge"): (45, 72, 0),
    (3, 4, "ambush", "guard"): (35, 50, 118),
    (3, 4, "ambush", "dodge"): (50, 74, 118),
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


    def test_terminal_bite_stops_before_toxin_or_pounce_roll(self):
        # Seed 386 creates a real above-zero Devastating Hunter Bite while
        # Hunter initiates a legal Pounce. Do not resolve post-wound effects.
        for policy in DEFENSE_POLICIES:
            with self.subTest(policy=policy):
                with patch("scripts.b06_hunter_repeated_exchanges_v0.die",
                           wraps=die) as rolled:
                    result = simulate_trial(2, 3, "ambush", policy, 386)
                self.assertTrue(result["hunter_first_initiative"])
                self.assertEqual(result["terminal"],
                                 "devastating_wound_unresolved")
                self.assertGreater(result["frontline_hp"], 0)
                self.assertTrue(result["pounce_used"])  # already declared
                self.assertFalse(result["pounce_balance_resolved"])
                self.assertFalse(result["pounce_prone"])
                self.assertIsNone(result["toxin"])
                keys = [call.args[2:] for call in rolled.call_args_list]
                self.assertFalse(any("toxin" in k or "pounce" in k or
                                     "balance" in k for k in keys))

        # Force terminal ordinary Bite damage before the linked rider.
        # No toxin resistance or unable-to-contest Trip can follow here.
        def lethal_bite(_seed, key, *_args, **_kwargs):
            if key[-1] == "bite":
                return (13, "ordinary")  # HP12 -> -1
            self.fail(f"A later attack illegally resolved: {key}")
        with patch("scripts.b06_hunter_repeated_exchanges_v0.strike",
                   side_effect=lethal_bite):
            fatal = simulate_trial(2, 3, "ambush", "guard", 386)
        self.assertEqual(fatal["terminal"], "frontline_first_zero")
        self.assertEqual(fatal["frontline_hp"], -1)
        self.assertTrue(fatal["pounce_used"])
        self.assertFalse(fatal["pounce_balance_resolved"])
        self.assertFalse(fatal["pounce_prone"])
        self.assertIsNone(fatal["toxin"])
        self.assertEqual(fatal["standing_opportunities"], 0)

    def test_terminal_standing_opportunity_stops_before_toxin_and_stand(self):
        # Bite misses but legal forceful Pounce knocks A1 Prone. A1 reaches
        # Stand, then an Opportunity first drops its HP <= 0. Its associated
        # venom must not roll and the Stand cannot finish.
        original_die = die
        def forced_die(seed, sides, *key):
            if key == ("initiative", "H"):
                return 20
            if key == ("initiative", "A1"):
                return 19  # A1 acts before other PCs and triggers Stand
            if key[:1] == ("initiative",):
                return 1
            if key[-1] == "pounce":
                return 20
            if key[-1] == "balance":
                return 1
            return original_die(seed, sides, *key)
        def forced_strike(_seed, key, *_args, **_kwargs):
            if key[-1] == "bite":
                return (0, "miss")
            if key[-1] == "standing_opportunity":
                return (13, "ordinary")
            self.fail(f"Unexpected attack after terminal Opportunity: {key}")
        with patch("scripts.b06_hunter_repeated_exchanges_v0.die",
                   side_effect=forced_die):
            with patch("scripts.b06_hunter_repeated_exchanges_v0.strike",
                       side_effect=forced_strike):
                result = simulate_trial(2, 3, "ambush", "guard", 386)
        self.assertEqual(result["terminal"], "frontline_first_zero")
        self.assertEqual(result["frontline_hp"], -1)
        self.assertTrue(result["pounce_balance_resolved"])
        self.assertTrue(result["pounce_prone"])
        self.assertEqual(result["standing_opportunities"], 1)
        self.assertIsNone(result["toxin"])
        self.assertEqual(result["pc_attack_attempts"], 0)


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
                self.assertEqual(
                    (cell["full_toxin"], cell["reduced_toxin"],
                     cell["pounce_balance_resolutions"]),
                    EXPECTED_TOXIN_AND_BALANCE[key],
                )
                self.assertLessEqual(cell["pounce_balance_resolutions"],
                                     cell["pounce_attempts"])
                self.assertLessEqual(cell["pounce_prone"],
                                     cell["pounce_balance_resolutions"])

if __name__ == "__main__":
    unittest.main()
