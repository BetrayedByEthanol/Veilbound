"""B06-EN-03 physiology-slice arithmetic and provenance (not encounter balance).

No external dependencies and no claim that the full Hunter enemy is executable.
"""
import copy
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHYSIOLOGY = ROOT / "content/creatures/b06-hunter-physiology.v0.json"
SCHEMA = ROOT / "schemas/b06-hunter-physiology-v0.schema.json"
BESTIARY = ROOT / "content/creatures/b06-initial-bestiary-v0.json"
DESIGN = ROOT / "docs/design/b06-hunter-physiology-v0.md"
POUNCE = ROOT / "docs/rules/05-combat/hunter-pounce-and-prey-takedown-v0.md"
BITE = ROOT / "docs/rules/05-combat/hunter-bite-venom-and-horn-v0.md"
HP_VIGOR = ROOT / "docs/rules/06-vigor-wounds-death/hp-and-vigor.md"
DODGE = ROOT / "docs/rules/05-combat/defensive-responses-and-criticals.md"


def round_half_up_positive(amount):
    return math.floor(amount + 0.5)


def damage_after_armor(rolled, penetration, armor):
    return max(0, rolled - max(0, armor - penetration))


def regenerate(hp, vigor, hp_max, throughput):
    """A legitimate non-Dying own-turn HP-only allocation, not free exploration healing."""
    amount = min(throughput, hp_max - hp, vigor)
    return hp + amount, vigor - amount


class HunterPhysiologyV0Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads(PHYSIOLOGY.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.bestiary = json.loads(BESTIARY.read_text(encoding="utf-8"))
        cls.hunter = next(x for x in cls.bestiary["entries"]
                          if x["id"] == "B06-EN-03")
        cls.design = DESIGN.read_text(encoding="utf-8")
        cls.pounce = POUNCE.read_text(encoding="utf-8")
        cls.bite = BITE.read_text(encoding="utf-8")
        cls.hp_vigor = HP_VIGOR.read_text(encoding="utf-8")
        cls.dodge = DODGE.read_text(encoding="utf-8")

    def test_snapshot_has_dedicated_strict_draft202012_schema(self):
        root = self.schema
        self.assertEqual(root["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(root["additionalProperties"])
        self.assertEqual(root["properties"]["schema_version"]["const"],
                         self.profile["schema_version"])
        self.assertIn("creature_profile", root["required"])
        profile_schema = root["properties"]["creature_profile"]
        self.assertIn("footprint_cell_ids", profile_schema["required"])
        self.assertIn("reference_cell_id", profile_schema["required"])
        self.assertEqual(profile_schema["properties"]["reference_cell_id"]["const"], "head")
        self.assertEqual(profile_schema["properties"]["footprint_cell_ids"]["const"],
                         ["head", "rear"])

    def test_snapshot_draft202012_schema_validation_when_available(self):
        # This repository's required tests remain stdlib-only; schema execution
        # is additionally exercised when a Draft 2020-12 validator is installed.
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("optional jsonschema package not installed")
        Draft202012Validator.check_schema(self.schema)
        validator = Draft202012Validator(self.schema)
        self.assertEqual(list(validator.iter_errors(self.profile)), [])
        invalid = copy.deepcopy(self.profile)
        invalid["creature_profile"]["reference_cell_id"] = "wing"
        self.assertTrue(list(validator.iter_errors(invalid)))
        invalid = copy.deepcopy(self.profile)
        invalid["creature_profile"]["footprint_cell_ids"] = ["head", "head"]
        self.assertTrue(list(validator.iter_errors(invalid)))
        invalid = copy.deepcopy(self.profile)
        invalid["record_status"] = "EXECUTABLE_TEST_FIXTURE"
        self.assertTrue(list(validator.iter_errors(invalid)))

    def test_slice_record_explicitly_not_an_executable_enemy(self):
        self.assertEqual(self.profile["record_status"], "PHYSIOLOGY_ONLY_NOT_EXECUTABLE")
        self.assertIsNone(self.profile["full_enemy_fixture_path"])
        self.assertEqual(self.hunter["entry_status"], "EXECUTABLE_FIXTURE_EXISTS")
        self.assertEqual(self.hunter["fixture_path"],
                         "content/creatures/b06-hunter-of-the-woods.v0.json")
        self.assertEqual(self.hunter["encounter_guidance"]["challenge_rating"]["status"], "unrated")
        self.assertIn("docs/design/b06-hunter-physiology-v0.md", self.hunter["rules_basis"])

    def test_source_and_species_not_magical_caster_or_second_creature(self):
        p = self.profile
        self.assertEqual(p["creature_id"], "B06-EN-03")
        self.assertEqual(p["creature_profile"]["family"], "natural_beast")
        self.assertEqual(p["creature_profile"]["footprint_cell_ids"], ["head", "rear"])
        self.assertEqual(p["creature_profile"]["reference_cell_id"], "head")
        self.assertEqual(p["creature_profile"]["hp_vigor_pool_count"], 1)
        self.assertFalse(p["creature_profile"]["has_personal_veil_invocation"])
        self.assertEqual(p["personal_vp"]["max"], 0)

    def test_ability_anchors_are_local_not_character_point_buy(self):
        a = self.profile["abilities"]
        self.assertEqual((a["vitality"], a["agility"], a["awareness"]), (4, 2, 2))
        self.assertEqual(self.profile["benchmark_rank"], 3)
        self.assertIn("not actual PC Level", self.design)

    def test_hp_not_multiplied_by_rank_or_footprint(self):
        p = self.profile
        self.assertIn("Max HP = 10 + Vitality", self.hp_vigor)
        self.assertEqual(p["hp"]["max"], 10 + p["abilities"]["vitality"])
        self.assertEqual(p["hp"]["max"], 14)
        self.assertEqual(p["hp"]["size_or_footprint_multiplier"], 1)

    def test_natural_armor_uniform_nonstacking_and_no_dodge_cap(self):
        armor = self.profile["natural_armor"]
        self.assertEqual(armor["rating"], 3)
        self.assertIsNone(armor["dodge_agility_cap"])
        self.assertFalse(armor["worn_armor_stacking"])
        self.assertIn("One uniform hide/dermis Armor rating", self.design)

    def test_dodge_base_and_pressure_sequence(self):
        p = self.profile
        a = p["abilities"]
        base = 10 + a["agility"] + a["awareness"]
        self.assertEqual(base, p["dodge"]["base"])
        self.assertEqual([base - 2 * i for i in range(4)],
                         p["dodge"]["first_four_defenses"])
        self.assertIn("Dodge Pressure", self.dodge)

    def test_guard_capacity_exists_but_no_instrument_authorized(self):
        g = self.profile["guard"]
        self.assertIsNone(g["instrument"])
        self.assertEqual(g["capacity"], 1)
        self.assertFalse(g["usable_with_current_natural_sources"])
        self.assertFalse(g["natural_horn_or_jaws_grant_guard"])
        self.assertIn("Physical Tempo1", self.design)
        self.assertIn("not a Guard", self.bite)

    def test_max_vigor_nonfocus_regen_and_six_hour_recovery(self):
        p = self.profile
        v = p["vigor"]
        self.assertEqual(v["max"], p["hp"]["max"] * p["benchmark_rank"])
        self.assertEqual(v["max"], 42)
        self.assertEqual(v["non_focus_rate"], 0)
        self.assertEqual(v["regeneration_throughput"],
                         max(p["abilities"]["vitality"], 0) + v["non_focus_rate"])
        self.assertEqual(v["regeneration_throughput"], 4)
        self.assertEqual(v["six_hour_recovery"], round_half_up_positive(v["max"] * 0.25))
        self.assertEqual(v["six_hour_recovery"], 11)

    def test_soldier_sword_damage_hits_hunter_once(self):
        # Existing ordinary soldier profile: raw 4+d6 Piercing, Pen2.
        raw, pen, armor = 4 + 4, 2, self.profile["natural_armor"]["rating"]
        hp_damage = damage_after_armor(raw, pen, armor)
        self.assertEqual(hp_damage, 7)
        self.assertEqual(self.profile["hp"]["max"] - hp_damage, 7)

    def test_regeneration_one_real_step_spends_vigor(self):
        p = self.profile
        self.assertEqual(regenerate(7, 42, 14, 4), (11, 38))
        self.assertEqual(regenerate(13, 42, 14, 4), (14, 41))
        self.assertEqual(regenerate(7, 0, 14, 4), (7, 0))
        self.assertIn("Regeneration Step", self.hp_vigor)
        self.assertIn("general exploration-time natural HP regeneration is not authored", self.design)

    def test_six_hour_recovery_capped_and_not_hp_heal(self):
        p = self.profile
        restored = min(p["vigor"]["max"], 38 + p["vigor"]["six_hour_recovery"])
        self.assertEqual(restored, 42)
        self.assertIn("completed 6-hour interval", self.hp_vigor)
        self.assertIn("no corresponding free HP repair", self.design)

    def test_pounce_bite_and_horn_remain_independent_and_uncalibrated(self):
        self.assertIn("d20+6 Bite", self.design)
        self.assertIn("d20+5 Horn", self.design)
        self.assertIn("full B06-EN-03 executable test fixture", self.design)
        self.assertIn("Pounce/Drive contest authority", self.design)
        self.assertIn("PHYSIOLOGY_ONLY_NOT_EXECUTABLE", self.design)
        self.assertIn("24 AP", self.pounce)


if __name__ == "__main__":
    unittest.main()
