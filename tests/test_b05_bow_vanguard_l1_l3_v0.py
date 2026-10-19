"""Executable B05/B07 v0 Bow Vanguard creation/progression legality tests.

Tests a derived character ledger, not a probabilistic encounter outcome.
"""
from pathlib import Path
import json
import unittest

from scripts.b05_bow_vanguard_l1_l3_v0 import (
    ABILITIES, ABILITY_COST, GEAR_SP, LEVELS, PRAYERS,
    START_DISCIPLINES, TALENTS, profile, verify,
)
from scripts.b06_hunter_tactical_diversity_v0 import ROLE


ROOT = Path(__file__).resolve().parents[1]


class BowVanguardBuildTests(unittest.TestCase):
    def test_exact_source_validation(self):
        self.assertTrue(verify())
        self.assertEqual(LEVELS, (1, 2, 3))

    def test_creation_ability_points_and_identity(self):
        sheet = profile(1)
        self.assertEqual(sum(ABILITY_COST[x] for x in ABILITIES.values()), 28)
        self.assertEqual(sheet["ability_points"], 28)
        self.assertEqual(sheet["abilities"], {
            "Strength": 2, "Agility": 3, "Precision": 0,
            "Intellect": 0, "Awareness": 1, "Presence": -2,
            "Vitality": 2, "Veil Affinity": 0, "Veil Control": 0,
        })
        self.assertEqual((sheet["archetype"], sheet["focus"], sheet["pillar"]),
                         ("Priest", "Low", "Life"))
        self.assertEqual(sheet["pillar_accord"], 1)
        self.assertEqual(sheet["resonance"], 0)

    def test_bow_training_is_independent_and_no_melee_transfer(self):
        for level in LEVELS:
            sheet = profile(level)
            self.assertEqual(sheet["weapon_training"], {"Bows": 2})
            self.assertEqual(sheet["weapon_development_points"], 2)
            self.assertEqual(sheet["bow_attack_bonus"], 2 + 0 + 2)
            self.assertEqual(sheet["dagger_attack_bonus"], 3 + 0 + 0)
            self.assertEqual(sheet["dagger_damage"], "3+d4 Cut/Pierce")
            self.assertEqual(sheet["dagger_penetration"], 0)
            self.assertEqual(sheet["dagger_guard_if_wielded"], 13)
        source = (ROOT / "docs/rules/05-combat" /
                  "weapon-training-and-refinements-v0.md").read_text()
        self.assertIn("Bows and Crossbows are trained **independently**", source)

    def test_starting_gear_cost_and_arrows(self):
        for level in LEVELS:
            sheet = profile(level)
            self.assertEqual(sheet["equipment_sp"], GEAR_SP)
            self.assertEqual(sheet["silver_spent"], 68)
            self.assertEqual(sheet["silver_remaining"], 82)
            self.assertEqual(sheet["silver_budget"], 150)
            self.assertEqual(sheet["initial_arrows"], 20)
            self.assertEqual(sum(sheet["equipment_sp"].values()), 68)
            self.assertNotIn("Medical kit", sheet["equipment_sp"])

    def test_training_budget_and_level_two_progression(self):
        for level in LEVELS:
            sheet = profile(level)
            self.assertEqual(sheet["learned_points"], 8 + (level >= 2))
            self.assertEqual(sum(sheet["learned_disciplines"].values()),
                             sheet["learned_points"])
            self.assertTrue(all(v <= 2 for v in
                                sheet["learned_disciplines"].values()))
            self.assertEqual(
                sheet["learned_disciplines"],
                {**START_DISCIPLINES, **({"Survival": 1} if level >= 2 else {})})
            self.assertEqual(len(sheet["background_familiarities"]), 2)
            self.assertEqual(sheet["abilities"], profile(1)["abilities"])

    def test_talents_prayers_and_universal_unlocks(self):
        for level in LEVELS:
            sheet = profile(level)
            self.assertEqual(sheet["talents"],
                             [TALENTS[x] for x in LEVELS if x <= level])
            self.assertEqual(sheet["prepared_prayers"], list(PRAYERS[level]))
            self.assertEqual(len(sheet["prepared_prayers"]),
                             sheet["max_prepared_prayers"])
            self.assertEqual(sheet["chosen_devotion"], "Guided Regeneration")
            self.assertEqual(sheet["universal"],
                             (["Veil Inspection"] if level < 3
                              else ["Veil Inspection", "Blink"]))
            self.assertEqual(sheet["max_prepared_prayers"],
                             2 if level == 1 else 3)

    def test_level_one_two_three_resource_and_regen_table(self):
        expected = (
            (1, 12, 12, 2, 30, 1, 1, 1),
            (2, 12, 24, 4, 36, 1, 1, 2),
            (3, 12, 36, 6, 42, 2, 1, 3),
        )
        for level, hp, vig, vp, ap, phys, proj, guard in expected:
            with self.subTest(level=level):
                sheet = profile(level)
                self.assertEqual((sheet["hp_max"], sheet["vigor_max"],
                                  sheet["vp_max"], sheet["turn_ap"],
                                  sheet["physical_tempo"],
                                  sheet["projection_tempo"],
                                  sheet["normal_guard_capacity"]),
                                 (hp, vig, vp, ap, phys, proj, guard))
                self.assertEqual(sheet["normal_regen_throughput"], 6)
                self.assertEqual(sheet["regen_with_active_chosen_guided"], 7)
                self.assertEqual(sheet["chosen_maintained_guided_committed_vp"],
                                 1)
                self.assertEqual(sheet["movement_points"], 12)

    def test_bow_damage_defense_and_phase3_role_stay_unchanged(self):
        r = ROLE["R"]
        self.assertEqual((r["attack"], r["base"], r["die"], r["pen"],
                          r["kind"], r["guard"], r["action_ap"],
                          r["regen"]), (4, 2, 4, 3, "bow", None, 20, 6))
        for level in (2, 3):
            sheet = profile(level)
            self.assertEqual(sheet["bow_attack_bonus"], r["attack"])
            self.assertEqual(sheet["bow_damage"], "2+d4 Piercing")
            self.assertEqual(sheet["bow_penetration"], r["pen"])
            self.assertEqual(sheet["hp_max"], r["hp"])
            self.assertEqual(sheet["initiative"], r["init"])
            self.assertEqual(sheet["first_dodge"], 14)
            self.assertIsNone(sheet["bow_guard"])
            self.assertEqual(sheet["ranged_evasion_bonus"], level - 2)

    def test_ap_tradeoffs_aim_and_heal_do_not_create_shots(self):
        for level in LEVELS:
            sheet = profile(level)
            self.assertEqual(sheet["physical_action_ap"], 20)
            self.assertEqual(sheet["projection_action_ap"], 30)
            self.assertEqual(sheet["general_action_ap"], 24)
            self.assertEqual(sheet["bow_shots_per_pure_physical_turn"],
                             1 if level <= 2 else 2)
            self.assertEqual(sheet["aim_then_shoot_same_turn"], level == 3)
            self.assertFalse(sheet["shot_then_project_same_turn"])
            self.assertGreater(20 + 30, sheet["turn_ap"])

    def test_vp_affordability_and_missing_components_are_not_waived(self):
        for level in LEVELS:
            sheet = profile(level)
            available_after_chosen = sheet["vp_max"] - 1
            self.assertEqual(sheet["ordinary_basic_heal_t1_spent_vp"], 2)
            self.assertEqual(sheet["ordinary_woodland_rapport_t1_spent_vp"], 2)
            self.assertEqual(available_after_chosen >= 2, level >= 2)
            self.assertEqual(sheet["blink_usable_from_fresh_full_vp"], False)
        self.assertGreater(10, profile(3)["vp_max"])
        heal = (ROOT / "docs/rules/07-veil-magic" /
                "basic-heal-v0.md").read_text()
        self.assertIn("at least one functioning available hand", heal)

    def test_bow_guard_is_not_rescued_by_guard_reserve(self):
        for level in LEVELS:
            self.assertIsNone(profile(level)["bow_guard"])
        self.assertEqual(profile(2)["normal_guard_capacity"], 2)
        self.assertEqual(profile(3)["normal_guard_capacity"], 3)
        source = (ROOT / "docs/rules/05-combat" /
                  "off-hand-and-ranged-combat.md").read_text()
        self.assertIn("bows and heavy crossbows are not Guard-capable", source)

    def test_threatened_shot_and_ammo_are_not_free(self):
        combat = (ROOT / "docs/rules/05-combat" /
                  "off-hand-and-ranged-combat.md").read_text()
        gear = (ROOT / "docs/rules/11-equipment" /
                "economy-and-starter-equipment-v0.md").read_text()
        self.assertIn("A bow or crossbow may be fired while the wielder is "
                      "threatened in melee", combat)
        self.assertIn("one arrow or bolt expended per shot fired", gear)

    def test_reject_out_of_scope_levels_and_bool(self):
        for level in (0, 4, -1, 1.0, True, "3"):
            with self.subTest(level=level):
                with self.assertRaises(ValueError):
                    profile(level)

    def test_json_fixture_roundtrip(self):
        for level in LEVELS:
            sheet = profile(level)
            self.assertEqual(json.loads(json.dumps(sheet)), sheet)


if __name__ == "__main__":
    unittest.main()
