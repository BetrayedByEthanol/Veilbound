"""B06 scoped eight-cell opposed Hunter/Low Life party exchange regression."""
import json
import unittest

from scripts.b06_hunter_party_exchanges_v0 import (
    BUILD, HUNTER_FILE, PRONE_TARGET_MELEE_ATTACK_BONUS, SCENARIOS,
    SHEET_AUTHORITY, simulate, standing_opportunity_attack_total,
)


# Precomputed from the authored fixed d20/d6 sample, not CR probabilities.
# (rounds, Hunter HP at R1 end, final HP, A1 HP, A1 Vigor,
#  accepted toxin count, Pounce Prone, Standing Opportunity, attacks, hits)
EXPECTED = {
    "L2-P3-warned": (2, 9, -4, 12, 20, 1, False, False, 5, 3),
    "L2-P3-ambush": (2, 9, -4, 9, 13, 1, True, True, 5, 3),
    "L2-P4-warned": (2, 1, -2, 12, 20, 1, False, False, 5, 3),
    "L2-P4-ambush": (2, 1, -2, 9, 13, 1, True, True, 5, 3),
    "L3-P3-warned": (1, -7, -7, 12, 36, 0, False, False, 4, 3),
    "L3-P3-ambush": (1, -7, -7, 7, 31, 1, True, True, 4, 3),
    "L3-P4-warned": (1, -7, -7, 12, 36, 0, False, False, 4, 3),
    "L3-P4-ambush": (1, -7, -7, 7, 31, 1, True, True, 4, 3),
}


class HunterPartyExchangesTests(unittest.TestCase):
    def test_all_eight_matrix_cells_and_outcomes(self):
        self.assertEqual(len(SCENARIOS), 8)
        self.assertEqual(
            {f"L{lv}-P{n}-{setup}" for lv, n, setup in SCENARIOS},
            set(EXPECTED),
        )
        for lv, n, setup in SCENARIOS:
            with self.subTest(level=lv, size=n, setup=setup):
                result = simulate(lv, n, setup)
                actual = (
                    result["rounds_observed"],
                    result["hunter_hp_at_end_r1"],
                    result["hunter_final_hp"],
                    result["frontline_final_hp"],
                    result["frontline_vigor_remaining"],
                    result["accepted_toxin_applications"],
                    result["pounce_prone"],
                    result["standing_opportunity_used"],
                    result["pc_attacks"],
                    result["pc_hits"],
                )
                self.assertEqual(actual, EXPECTED[result["scenario"]])
                self.assertTrue(result["hunter_first_zero_hp"])
                self.assertTrue(result["hunter_final_hp"] > -14)
                self.assertEqual(result["frontline_delayed_toxin"] is not None,
                                 result["accepted_toxin_applications"] == 1)

    def test_build_provenance_and_progression_without_fake_pcs(self):
        text = SHEET_AUTHORITY.read_text(encoding="utf-8")
        self.assertIn("Restorative Vanguard", text)
        self.assertIn("Preservation Guardian", text)
        self.assertIn("12 → 24 → 36", text)
        self.assertIn("13 → 26 → 39", text)
        self.assertEqual(BUILD["A"]["weapon_base"], 4)  # sword:3 + STR2//2
        self.assertEqual(BUILD["B"]["weapon_base"], 6)  # mace:4 + STR2
        self.assertEqual(BUILD["A"]["attack"], 7)
        self.assertEqual(BUILD["B"]["attack"], 6)
        self.assertEqual(BUILD["A"]["guard"], 17)
        self.assertEqual(BUILD["B"]["guard"], 18)
        self.assertEqual(BUILD["A"]["regen"], 6)  # no Guided Rite activated
        self.assertEqual(BUILD["B"]["regen"], 6)
        for level in (2, 3):
            self.assertEqual(30 + 6 * (level - 1), 36 if level == 2 else 42)
            self.assertEqual((30 + 6 * (level - 1)) // 20,
                             1 if level == 2 else 2)

    def test_all_attacks_use_actual_hunter_source_and_dodge_pressure(self):
        hunter = json.loads(HUNTER_FILE.read_text(encoding="utf-8"))
        bite = next(a for a in hunter["attack_profiles"] if a["id"] == "B06-AT-04")
        pounce = next(a for a in hunter["attack_profiles"] if a["id"] == "B06-AT-06")
        self.assertEqual(hunter["defenses"]["hp_max"], 14)
        self.assertEqual(hunter["defenses"]["armor"], 3)
        self.assertEqual(hunter["defenses"]["dodge_base"], 14)
        self.assertIsNone(hunter["defenses"]["guard_instrument"])
        self.assertEqual(bite["attack_roll"]["total_bonus"], 6)
        self.assertEqual(bite["primary_hp_packet"]["armor_penetration"], 1)
        self.assertEqual(pounce["linked_contest"]["total_pressure_bonus"], 4)
        result = simulate(2, 4, "warned")
        self.assertTrue(any("13<=14 Dodge: miss" in s for s in result["log"]))
        self.assertTrue(any("11<=12 Dodge: miss" in s for s in result["log"]))
        self.assertTrue(any("19>10" in s for s in result["log"]))
        self.assertTrue(any("18>8" in s for s in result["log"]))

    def test_ambush_is_geometry_not_free_surprise_attack(self):
        ambush = simulate(2, 3, "ambush")
        warned = simulate(2, 3, "warned")
        self.assertEqual(ambush["hunter_hp_at_end_r1"],
                         warned["hunter_hp_at_end_r1"])
        self.assertTrue(ambush["pounce_prone"])
        self.assertTrue(ambush["standing_opportunity_used"])
        self.assertFalse(warned["pounce_prone"])
        self.assertFalse(warned["standing_opportunity_used"])
        self.assertIn("R1 Pounce Balance 18>15: Prone", ambush["log"])
        self.assertEqual(ambush["accepted_toxin_applications"], 1)
        self.assertEqual(warned["accepted_toxin_applications"], 1)
        self.assertIn("R2 repeat puncture; venom does not stack", ambush["log"])
        self.assertNotIn("R2 repeat puncture; venom does not stack", warned["log"])

    def test_standing_opportunity_resolves_before_prone_state_clears(self):
        self.assertEqual(PRONE_TARGET_MELEE_ATTACK_BONUS, 2)
        # Regression for Prone melee modifier: a 19 Guard would stop the
        # erroneous standing-target total 18, but cannot stop the legal 20.
        total = standing_opportunity_attack_total(
            12, 6, target_prone=True)
        self.assertEqual(total, 20)
        self.assertGreater(total, 19)
        self.assertLessEqual(12 + 6, 19)
        with self.assertRaises(ValueError):
            standing_opportunity_attack_total(12, 6, target_prone=False)

        for level in (2, 3):
            for size in (3, 4):
                with self.subTest(level=level, size=size):
                    events = simulate(level, size, "ambush")["log"]
                    begin = next(i for i, x in enumerate(events)
                                 if "A1 begins Stand (4 MP; still Prone)" in x)
                    opportunity = next(i for i, x in enumerate(events)
                                       if ("Standing Opportunity "
                                           "12+6+2(Prone)=20>17" in x))
                    complete = next(i for i, x in enumerate(events)
                                    if "A1 completes Stand; no longer Prone" in x)
                    self.assertLess(begin, opportunity)
                    self.assertLess(opportunity, complete)
                    self.assertIn("target still Prone", events[opportunity])
                    self.assertIn(": 5 HP;", events[opportunity])
        self.assertFalse(
            any("Standing Opportunity" in event
                for event in simulate(2, 3, "warned")["log"]))

    def test_hunter_regeneration_is_real_step_not_free_between_strikes(self):
        for size, expected in ((3, 13), (4, 5)):
            result = simulate(2, size, "warned")
            self.assertEqual(result["hunter_vigor"], 38)
            self.assertIn("R2 Hunter Step2 +4 HP, -4 Vigor", result["log"])
            # R1 ends at 9/1, and R2 starts from 13/5 before PC attacks.
            self.assertEqual(result["hunter_hp_at_end_r1"] + 4, expected)
        for size in (3, 4):
            result = simulate(3, size, "ambush")
            self.assertEqual(result["hunter_vigor"], 42)
            self.assertEqual(result["rounds_observed"], 1)

    def test_calibration_does_not_invent_variants_or_numeric_cr(self):
        for invalid in ((1, 3, "warned"), (3, 5, "ambush"),
                        (2, 2, "ambush"), (2, 3, "surprised")):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    simulate(*invalid)


if __name__ == "__main__":
    unittest.main()
