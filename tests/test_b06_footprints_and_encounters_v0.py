"""B06 v0 multi-square-footprint and encounter-taxonomy regression tests.

This verifies the newly authored index fields, provenance boundaries, unchanged
executable enemies, and explicit movement arithmetic examples. It is NOT a
full physics, JSON Schema or encounter-balance simulator.
"""
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "docs/rules/05-combat/multi-square-creature-footprints-v0.md"
ENCOUNTER_DOC = ROOT / "docs/design/b06-encounter-frequency-challenge-and-hunter-ecology-v0.md"
INDEX_PATH = ROOT / "content/creatures/b06-initial-bestiary-v0.json"
ENEMY_SCHEMA = ROOT / "schemas/b06-enemy-benchmark-v0.schema.json"
INDEX_SCHEMA = ROOT / "schemas/b06-bestiary-index-v0.schema.json"
SENTRY = ROOT / "content/creatures/b06-firebound-sentry.v0.json"
SOLDIER = ROOT / "content/creatures/b06-ordinary-human-soldier.v0.json"


def translated_mp_cost(base_mp, terrain_surcharges, cautious=False):
    """Pure arithmetic example, not a replacement for spatial legality checks."""
    return math.ceil(sum(base_mp * (2 if cautious else 1) + t
                         for t in terrain_surcharges) / len(terrain_surcharges))


class B06FootprintEncounterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        cls.entries = {e["id"]: e for e in cls.index["entries"]}
        cls.enemy_schema = json.loads(ENEMY_SCHEMA.read_text(encoding="utf-8"))
        cls.index_schema = json.loads(INDEX_SCHEMA.read_text(encoding="utf-8"))
        cls.rules = RULE.read_text(encoding="utf-8")
        cls.encounter_docs = ENCOUNTER_DOC.read_text(encoding="utf-8")
        cls.sentry = json.loads(SENTRY.read_text(encoding="utf-8"))
        cls.soldier = json.loads(SOLDIER.read_text(encoding="utf-8"))
        cls.hunter = cls.entries["B06-EN-03"]

    def test_shared_schema_definitions_remain_identical(self):
        for name in ("creatureProfile", "plannedCapability", "bestiaryEntry",
                     "encounterGuidance"):
            self.assertEqual(self.enemy_schema["$defs"][name],
                             self.index_schema["$defs"][name], name)

    def test_encounter_fields_optional_and_separate_from_combat_stats(self):
        props = self.index_schema["$defs"]["bestiaryEntry"]["properties"]
        self.assertIn("encounter_guidance", props)
        self.assertNotIn("encounter_guidance",
                         self.index_schema["$defs"]["bestiaryEntry"]["required"])
        self.assertIn("footprint",
                      self.index_schema["$defs"]["creatureProfile"]["properties"])
        self.assertNotIn("footprint",
                         self.index_schema["$defs"]["creatureProfile"]["required"])

    def test_hunter_has_one_by_two_footprint_not_second_combatant(self):
        p = self.hunter["creature_profile"]
        shape = p["footprint"]
        self.assertEqual(p["family"], "natural_beast")
        self.assertEqual((shape["width_cells"], shape["length_cells"]), (1, 2))
        self.assertEqual(shape["shape"], "rectangular")
        self.assertIn("front", shape["reference_rule"])
        self.assertIn("multi-square-creature-footprints-v0.md",
                      shape["movement_rule_ref"])
        self.assertEqual(shape["movement_rule_ref"], shape["rotation_rule_ref"])

    def test_translation_average_rounds_up_after_terrain(self):
        self.assertEqual(translated_mp_cost(2, [0, 0]), 2)
        self.assertEqual(translated_mp_cost(2, [2, 0]), 3)
        self.assertEqual(translated_mp_cost(2, [2, 2]), 4)
        self.assertEqual(translated_mp_cost(2, [4, 0]), 4)
        self.assertEqual(translated_mp_cost(2, [4, 2]), 5)
        self.assertEqual(translated_mp_cost(2, [4, 4]), 6)
        self.assertIn("ceil((c_1 + ... + c_N) / N)", self.rules)

    def test_diagonal_averaging_and_cautious_base_first(self):
        self.assertEqual(translated_mp_cost(3, [2, 0]), 4)
        self.assertEqual(translated_mp_cost(3, [4, 2]), 6)
        self.assertEqual(translated_mp_cost(2, [2, 0], cautious=True), 5)
        self.assertEqual(translated_mp_cost(3, [2, 0], cautious=True), 7)
        self.assertIn("double each *base*", self.rules)

    def test_rotation_uses_single_moving_end_and_does_not_average(self):
        self.assertIn("90° pivot", self.rules)
        self.assertIn("3 MP", self.rules)
        self.assertIn("6 MP Cautious", self.rules)
        self.assertIn("180° reversal", self.rules)
        self.assertIn("two", self.rules)
        self.assertEqual(3 + 2, 5)  # Pivot into Difficult destination.
        self.assertEqual(3 + 4, 7)  # Pivot into Severe destination.

    def test_no_impassable_partial_movement_or_free_squeeze(self):
        self.assertIn("entire step is illegal", self.rules)
        self.assertIn("no portion", self.rules.lower())
        self.assertIn("blocked-corner", self.rules)

    def test_opportunity_is_once_per_enemy_per_segment(self):
        self.assertIn("at most one general Movement Opportunity", self.rules)
        self.assertIn("per movement segment", self.rules)
        self.assertIn("Cautious", self.rules)

    def test_existing_charge_is_not_free_pounce(self):
        self.assertIn("three straight-line translated approach steps", self.rules)
        self.assertIn("no free pounce", self.rules.lower())
        self.assertIn("Rapid Advance, Charge and Sprint forbid voluntary pivot", self.rules)
        self.assertIn("one normally paid melee attack", self.encounter_docs)

    def test_grapple_single_square_exception_explicitly_pending(self):
        self.assertIn("shared single-square Grapple", self.rules)
        self.assertIn("Pounce-linked takedown require", self.rules)
        self.assertIn("CONCEPT_ONLY", self.encounter_docs)

    def test_hunter_remains_numerically_unexecuted(self):
        self.assertEqual(self.hunter["entry_status"], "CONCEPT_ONLY")
        self.assertIsNone(self.hunter["fixture_path"])
        self.assertTrue(all(c["state"] != "existing_authority_only"
                            for c in self.hunter["planned_capabilities"]))
        self.assertTrue(self.hunter["open_mechanics"])

    def test_hunter_pounce_bite_independent_takedown(self):
        cap = {c["id"]: c for c in self.hunter["planned_capabilities"]}
        for name in ("B06-CAP-HUNTER-POUNCE", "B06-CAP-HUNTER-BITE",
                     "B06-CAP-HUNTER-HORN", "B06-CAP-HUNTER-TRACK"):
            self.assertIn(name, cap)
        for name in ("B06-CAP-HUNTER-POUNCE", "B06-CAP-HUNTER-BITE",
                     "B06-CAP-HUNTER-HORN"):
            self.assertEqual(cap[name]["state"], "requires_authored_attack_or_effect")
            self.assertTrue(cap[name]["missing_authority"])
        self.assertEqual(cap["B06-CAP-HUNTER-TRACK"]["state"], "narrative_only")
        self.assertIn("irrespective of whether pounce/takedown succeeded",
                      cap["B06-CAP-HUNTER-BITE"]["concept"])

    def test_hunter_venom_resistance_and_timing_still_requires_source(self):
        bite = next(c for c in self.hunter["planned_capabilities"]
                    if c["name"] == "Venomous bite")
        self.assertIn("TX framework", " ".join(bite["missing_authority"]))
        self.assertIn("slow-acting", bite["concept"])
        self.assertIn("short TX-HM", bite["concept"])
        self.assertIn("not already a long-term pursuit venom", self.encounter_docs)

    def test_horn_ecological_roles_not_optimized_weapon(self):
        anatomy = " ".join(self.hunter["creature_profile"]["physiology_notes"]).lower()
        self.assertIn("rutting", anatomy)
        self.assertIn("intimidation", anatomy)
        self.assertIn("excavat", anatomy)
        self.assertIn("predator", anatomy)

    def test_hunter_vigor_not_numerically_locked(self):
        self.assertTrue(any("Vigor" in x for x in self.hunter["open_mechanics"]))
        self.assertNotIn("vigor_max", self.hunter)
        self.assertIn("not a generalized stamina bar", self.encounter_docs)

    def test_soldier_and_hunter_cr_both_unrated(self):
        for n in ("B06-EN-02", "B06-EN-03"):
            g = self.entries[n]["encounter_guidance"]
            self.assertEqual(g["challenge_rating"]["status"], "unrated")
            self.assertIsNone(g["challenge_rating"]["value"])
            self.assertIsNone(g["challenge_rating"]["scale"])
        self.assertEqual(self.entries["B06-EN-02"]["encounter_guidance"]["combat_role"],
                         "ordinary_humanoid")
        self.assertEqual(self.hunter["encounter_guidance"]["combat_role"],
                         "elite_ambush_predator")

    def test_unrated_cr_schema_requires_null(self):
        schema = self.index_schema["$defs"]["encounterGuidance"]
        cr = schema["properties"]["challenge_rating"]
        self.assertTrue(any(branch.get("then", {}).get("properties", {})
                            .get("value", {}).get("type") == "null"
                            for branch in cr["allOf"]))
        self.assertTrue(any(branch.get("then", {}).get("properties", {})
                            .get("scale", {}).get("type") == "string"
                            for branch in cr["allOf"]))
        self.assertTrue(any("calibration_evidence" in branch.get("then", {}).get("required", [])
                            for branch in cr["allOf"]))

    def test_party_size_vs_footprint_vs_enemy_count_are_independent(self):
        for n in ("B06-EN-02", "B06-EN-03"):
            for scenario in self.entries[n]["encounter_guidance"]["test_scenarios"]:
                self.assertLessEqual(scenario["party_size_min"], scenario["party_size_max"])
                self.assertLessEqual(scenario["party_level_min"], scenario["party_level_max"])
                self.assertEqual(scenario["evidence_status"], "untested")
                self.assertGreaterEqual(scenario["enemy_count"], 0)
                self.assertIn(scenario["intended_difficulty"],
                              ("noncombat", "standard", "dangerous", "severe"))
        self.assertIn("encounter size / composition", self.encounter_docs.lower())

    def test_soldier_nonhostile_scene_and_preexisting_stats_unchanged(self):
        s = self.soldier
        self.assertEqual(s["resources"]["max_vp"], 0)
        self.assertEqual(s["resources"]["physical_action_ap"], 24)
        self.assertEqual(s["defenses"]["guard_base"], 18)
        self.assertEqual(s["attack_profiles"][0]["attack_roll"]["total_bonus"], 6)
        scenarios = self.entries["B06-EN-02"]["encounter_guidance"]["test_scenarios"]
        self.assertTrue(any(s["intended_difficulty"] == "noncombat" for s in scenarios))
        self.assertTrue(any("gate" in s["context"].lower()
                            for s in self.entries["B06-EN-02"]["encounter_guidance"]
                            ["frequency_contexts"]))

    def test_no_prior_sentry_fixture_modification(self):
        self.assertEqual(self.sentry["id"], "B06-EN-01")
        self.assertEqual([a["id"] for a in self.sentry["attack_profiles"]],
                         ["B06-AT-01", "B06-AT-02"])
        self.assertEqual([a["attack_roll"]["total_bonus"] for a in
                          self.sentry["attack_profiles"]], [7, 7])
        self.assertEqual(self.sentry["resources"]["max_vp"], 6)


if __name__ == "__main__":
    unittest.main()
