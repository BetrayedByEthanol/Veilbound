"""B05/B07 High Scholar Fire L1–3 creation and F compatibility tests."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.b05_high_scholar_fire_l1_l3_v0 import (
    ABILITIES, ABILITY_COST, FORMULAS, KNOWN_L1, KNOWN_L2_ADD,
    L1_DISCIPLINES, LEVELS, STARTING_GEAR_SP, TALENT_L1,
    WEAPON_TRAINING, formula_cost, profile, verify,
)
from scripts.b06_hunter_tactical_diversity_v0 import ROLE

ROOT = Path(__file__).resolve().parents[1]


class HighScholarFireBuildTests(unittest.TestCase):
    def test_source_bound_verifier(self):
        self.assertTrue(verify())
        self.assertEqual(LEVELS, (1, 2, 3))

    def test_level_one_ability_points_and_focus(self):
        sheet = profile(1)
        self.assertEqual(sheet["abilities"], {
            "Strength": 2, "Agility": 3, "Precision": 0,
            "Intellect": 0, "Awareness": 1, "Presence": -2,
            "Vitality": 2, "Veil Affinity": 0, "Veil Control": 0,
        })
        self.assertEqual(sum(ABILITY_COST[x] for x in ABILITIES.values()), 28)
        self.assertEqual(sheet["ability_points"], 28)
        self.assertEqual((sheet["archetype"], sheet["focus"]),
                         ("Scholar", "High"))
        self.assertIsNone(sheet["priest_pillar_accord"])
        self.assertEqual(sheet["resonance"], 0)

    def test_training_point_and_family_conservation(self):
        self.assertEqual(L1_DISCIPLINES, {
            "Veil Theory": 2, "Pillar Lore (Fire)": 2,
            "Throwing": 2, "Medicine": 2,
        })
        self.assertEqual(sum(L1_DISCIPLINES.values()), 8)
        for level in LEVELS:
            s = profile(level)
            self.assertEqual(s["learned_points"], 8 + (level >= 2))
            self.assertTrue(all(0 <= x <= 2 for x in
                                s["learned_disciplines"].values()))
            self.assertEqual(sum(s["learned_disciplines"].values()),
                             s["learned_points"])
            self.assertEqual(s["learned_disciplines"].get("Alchemy"),
                             1 if level >= 2 else None)
            self.assertEqual(s["weapon_training"], {"Small Blades": 2})
            self.assertEqual(s["weapon_development_points"], 2)

    def test_talent_prerequisite_and_levels(self):
        self.assertEqual(TALENT_L1, "TAL-U01 Veil Insight")
        for level in LEVELS:
            s = profile(level)
            self.assertEqual(s["talents"], [TALENT_L1])
            self.assertGreaterEqual(s["learned_disciplines"]["Veil Theory"], 1)
            self.assertEqual(s["abilities"], profile(1)["abilities"])
        text = (ROOT / "docs/rules/10-advancement" /
                "talents-level-1-5-v0.md").read_text()
        self.assertIn("### TAL-U01 — Veil Insight", text)

    def test_starting_gear_and_carried_dagger(self):
        self.assertEqual(STARTING_GEAR_SP, {
            "Leather armor": 25, "Dagger": 4,
            "Standard adventuring pack": 8,
        })
        for level in LEVELS:
            s = profile(level)
            self.assertEqual(s["starting_silver_spent"], 37)
            self.assertEqual(s["starting_silver_left"], 113)
            self.assertEqual(s["starting_silver_budget"], 150)
            self.assertEqual(sum(s["starting_equipment_sp"].values()), 37)
            self.assertFalse(s["dagger_held_in_phase3"])
            self.assertIsNone(s["guard_in_phase3"])
            self.assertEqual(s["dagger_guard_if_legally_wielded"], 15)
            self.assertEqual(s["dagger_attack_if_wielded"], 5)

    def test_known_repertoire_and_level_two_acquisition(self):
        self.assertEqual(KNOWN_L1, (
            "Conjure Flame", "Stone Skin", "Basic Heal",
            "Minor Telekinesis", "Phantom Sound",
        ))
        self.assertEqual(KNOWN_L2_ADD, "Vital Shelter")
        for level in LEVELS:
            s = profile(level)
            self.assertEqual(len(s["known_pillar_techniques"]), 5 if level == 1 else 6)
            self.assertEqual(len(set(s["known_pillar_techniques"])),
                             s["known_capacity"])
            self.assertEqual(s["known_pillar_techniques"][:5], list(KNOWN_L1))
            self.assertEqual("Vital Shelter" in s["known_pillar_techniques"],
                             level >= 2)

    def test_formula_preparation_and_fluency(self):
        for level in LEVELS:
            s = profile(level)
            self.assertEqual(s["prepared_formula_capacity"],
                             (1, 2, 0)[level - 1])
            self.assertEqual(s["formula_fluency"], level == 3)
            self.assertEqual(s["prepared_composite_formulas"],
                             [dict(FORMULAS[0])] if level == 1 else
                             [dict(FORMULAS[0]), dict(FORMULAS[1])]
                             if level == 2 else [])
            for f in s["prepared_composite_formulas"]:
                self.assertIn(f["primary"], s["known_pillar_techniques"])
                self.assertIn(f["secondary"], s["known_pillar_techniques"])
                self.assertEqual(f["profile"], "Self")
        self.assertNotIn("Conjure Flame", str(FORMULAS))

    def test_composite_cost_ledger_and_no_free_activation(self):
        for level in LEVELS:
            sh = profile(level)
            self.assertEqual(formula_cost(FORMULAS[0], level), {
                "action_ap": 20, "committed_vp": 2 * level,
                "spent_vp": 2, "vp_required": 2 * level + 2,
                "secondary_effect": "Basic Heal Self Secondary: 1 HP and 3 Vigor at T1, VC0"
            })
            self.assertLessEqual(formula_cost(FORMULAS[0], level)["vp_required"],
                                 sh["vp_max"])
            if level >= 2:
                cost = formula_cost(FORMULAS[1], level)
                self.assertEqual((cost["committed_vp"], cost["spent_vp"],
                                  cost["vp_required"]), (2*level + 2, 1, 2*level + 3))
                self.assertLessEqual(cost["vp_required"], sh["vp_max"])

    def test_source_f_bounded_combat_profile(self):
        r = ROLE["F"]
        self.assertEqual(
            (r["hp"], r["armor"], r["vit"], r["agi"], r["awa"], r["init"],
             r["guard"], r["guard_extra"], r["regen"], r["focus"], r["attack"],
             r["base"], r["die"], r["pen"], r["kind"], r["action_ap"]),
            (12, 3, 2, 3, 1, 4, None, 0, 3, "High", 5, 2, None, 0, "flame", 20))
        for level in (2, 3):
            s = profile(level)
            self.assertEqual(s["thrown_flame_attack"], r["attack"])
            self.assertEqual(s["normal_regen_throughput"], r["regen"])
            self.assertEqual(s["initiative"], r["init"])
            self.assertEqual(s["hp_max"], r["hp"])
            self.assertEqual(s["leather_armor"], r["armor"])
            self.assertIsNone(s["guard_in_phase3"])

    def test_reject_source_F_stat_mutation(self):
        with patch.dict(ROLE["F"], {"attack": 6}):
            with self.assertRaises(AssertionError):
                verify()
        with patch.dict(ROLE["F"], {"guard": 15}):
            with self.assertRaises(AssertionError):
                verify()

    def test_resources_and_action_economy(self):
        expected = (
            (1, 12, 12, 6, 30, 1, 1, 1, 1),
            (2, 12, 24, 12, 36, 1, 1, 1, 1),
            (3, 12, 36, 18, 42, 1, 2, 1, 2),
        )
        for level, hp, vigor, vp, ap, physical, projection, guard, flame in expected:
            s = profile(level)
            self.assertEqual(
                (s["hp_max"], s["vigor_max"], s["vp_max"],
                 s["turn_ap"], s["physical_tempo"], s["projection_tempo"],
                 s["guard_capacity"], s["t1_flame_casts_at_full_vp"]),
                (hp, vigor, vp, ap, physical, projection, guard, flame))
            self.assertEqual(s["projection_action_ap"], 20)
            self.assertEqual(s["physical_action_ap"], 30)
            self.assertFalse(s["t1_flame_and_physical_action_same_turn"])
            self.assertEqual(s["normal_regen_throughput"], 3)

    def test_flame_tier_and_full_VP_shots(self):
        for level in LEVELS:
            s = profile(level)
            self.assertEqual(s["max_used_tier"], 1 if level <= 2 else 2)
            self.assertEqual(s["thrown_flame_range_squares"], [1, 3])
            self.assertEqual(s["thrown_flame_activation_ap"], 20)
            self.assertEqual(s["thrown_flame_t1_spent_vp"], 2)
            self.assertEqual(s["t2_flame_casts_at_full_vp"], 2 if level == 3 else 0)
            self.assertEqual(s["first_dodge"], 14)
            self.assertEqual(s["movement_points"], 12)

    def test_universal_access_not_known_spell_slots(self):
        for level in LEVELS:
            s = profile(level)
            self.assertEqual(s["universal"],
                             ["Veil Inspection"] + (["Blink"] if level >= 3 else []))
            self.assertEqual(s["known_capacity"], 5 if level == 1 else 6)
            self.assertEqual(s["blink_affordable_from_full_vp"], level == 3)

    def test_reject_invalid_level_and_unlisted_formula(self):
        for level in (0, -1, 4, 3.0, True, "2"):
            with self.subTest(level=level):
                with self.assertRaises(ValueError):
                    profile(level)
        with self.assertRaises(ValueError):
            formula_cost({"primary": "Conjure Flame"}, 2)
        with self.assertRaises(ValueError):
            formula_cost(FORMULAS[0], True)

    def test_machine_readable_sheet_roundtrip(self):
        for level in LEVELS:
            s = profile(level)
            self.assertEqual(json.loads(json.dumps(s, allow_nan=False)), s)


if __name__ == "__main__":
    unittest.main()
