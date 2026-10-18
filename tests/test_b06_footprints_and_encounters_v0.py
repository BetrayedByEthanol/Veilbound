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
WARD = ROOT / "docs/rules/07-veil-magic/protective-ward-v0.md"
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
        cls.ward_rules = WARD.read_text(encoding="utf-8")
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
        self.assertEqual(shape["cell_ids"], ["head", "rear"])
        self.assertEqual(shape["reference_cell_id"], "head")
        self.assertIn("head", shape["reference_rule"])
        self.assertIn("multi-square-creature-footprints-v0.md",
                      shape["movement_rule_ref"])
        self.assertEqual(shape["movement_rule_ref"], shape["rotation_rule_ref"])

    def test_pivots_preserve_anatomical_cell_index_even_if_coordinate_sort_flips(self):
        """A committed head hit must never move to rear after a 90-degree pivot."""
        ids = self.hunter["creature_profile"]["footprint"]["cell_ids"]
        self.assertEqual(ids, ["head", "rear"])
        before = {"head": (1, 0, 0), "rear": (0, 0, 0)}
        after = {"head": (0, -1, 0), "rear": (0, 0, 0)}
        # Existing Ward implementation used world-coordinate sorting before/after.
        before_by_coordinates = sorted(before, key=lambda k: before[k])
        after_by_coordinates = sorted(after, key=lambda k: after[k])
        self.assertEqual(before_by_coordinates, ["rear", "head"])
        self.assertEqual(after_by_coordinates, ["head", "rear"])
        # A previous x/y/z rank of head=2 would now incorrectly land on rear.
        head_old_rank = before_by_coordinates.index("head")
        self.assertEqual(after_by_coordinates[head_old_rank], "rear")
        head_id = ids[0]  # permanent body-local cell 1
        self.assertEqual(before[head_id], (1, 0, 0))
        self.assertEqual(after[head_id], (0, -1, 0))
        self.assertNotEqual(after[head_id], after["rear"])
        self.assertIn("head (0,-1)", self.ward_rules)
        self.assertIn("same original cell ID/index", self.ward_rules)

    def test_reference_cell_tracks_head_through_pivot_and_relocation(self):
        shape = self.hunter["creature_profile"]["footprint"]
        ref = shape["reference_cell_id"]
        self.assertEqual(ref, "head")
        original = {"head": (1, 0, 0), "rear": (0, 0, 0)}
        pivoted = {"head": (0, -1, 0), "rear": (0, 0, 0)}
        translated = {cell: (x + 4, y + 2, z + 1)
                      for cell, (x, y, z) in pivoted.items()}
        self.assertEqual(original[ref], (1, 0, 0))
        self.assertEqual(pivoted[ref], (0, -1, 0))
        self.assertEqual(translated[ref], (4, 1, 1))
        self.assertIn("same identity", self.ward_rules)
        self.assertIn("never re-sort world coordinates", self.ward_rules)

    def test_precommitted_rear_cell_and_removed_cell_fallback(self):
        # Repeated coordinate sorting also corrupts precommitted rear impacts.
        ids = self.hunter["creature_profile"]["footprint"]["cell_ids"]
        rear_id = ids[1]
        pivoted = {"head": (0, -1, 0), "rear": (0, 0, 0)}
        self.assertEqual(pivoted[rear_id], (0, 0, 0))
        self.assertIn("lowest remaining original body-local cell index", self.rules)
        self.assertIn("lowest surviving **original body-local index**",
                      self.ward_rules)
        self.assertIn("only if original attack/Ward legality survives",
                      self.ward_rules)

    def test_body_local_ids_are_schema_required_and_unique(self):
        footprint = self.index_schema["$defs"]["creatureProfile"]["properties"]["footprint"]
        self.assertIn("cell_ids", footprint["required"])
        self.assertIn("reference_cell_id", footprint["required"])
        self.assertTrue(footprint["properties"]["cell_ids"]["uniqueItems"])
        ids = self.hunter["creature_profile"]["footprint"]["cell_ids"]
        self.assertEqual(len(ids), 2)
        self.assertEqual(len(set(ids)), len(ids))
        self.assertIn(self.hunter["creature_profile"]["footprint"]["reference_cell_id"], ids)
        self.assertEqual(self.enemy_schema["$defs"]["creatureProfile"]["properties"]
                         ["footprint"], footprint)

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
        self.assertIn("full Hunter test fixture", self.encounter_docs)

    def test_hunter_now_has_source_backed_full_fixture_but_no_certified_cr(self):
        self.assertEqual(self.hunter["entry_status"], "EXECUTABLE_FIXTURE_EXISTS")
        self.assertEqual(self.hunter["fixture_path"],
                         "content/creatures/b06-hunter-of-the-woods.v0.json")
        self.assertEqual(self.hunter["encounter_guidance"]["challenge_rating"]["status"], "unrated")
        self.assertTrue(self.hunter["open_mechanics"])

    def test_hunter_pounce_bite_independent_takedown(self):
        cap = {c["id"]: c for c in self.hunter["planned_capabilities"]}
        for name in ("B06-CAP-HUNTER-POUNCE", "B06-CAP-HUNTER-BITE",
                     "B06-CAP-HUNTER-HORN", "B06-CAP-HUNTER-TRACK"):
            self.assertIn(name, cap)
        for name in ("B06-CAP-HUNTER-POUNCE", "B06-CAP-HUNTER-BITE",
                     "B06-CAP-HUNTER-HORN"):
            self.assertEqual(cap[name]["state"], "existing_authority_only")
            self.assertTrue(cap[name]["missing_authority"])
        self.assertEqual(cap["B06-CAP-HUNTER-TRACK"]["state"], "narrative_only")
        self.assertIn("irrespective of whether pounce/takedown succeeded",
                      cap["B06-CAP-HUNTER-BITE"]["concept"])

    def test_hunter_venom_resistance_and_timing_still_requires_source(self):
        bite = next(c for c in self.hunter["planned_capabilities"]
                    if c["name"] == "Venomous bite")
        self.assertTrue(any("calibration" in x.lower() for x in bite["missing_authority"]))
        self.assertIn("slow-acting", bite["concept"])
        self.assertIn("short TX-HM", bite["concept"])
        self.assertIn("not already a long-term pursuit venom", self.encounter_docs)

    def test_horn_ecological_roles_not_optimized_weapon(self):
        profile = self.hunter["creature_profile"]
        anatomy = " ".join(profile["physiology_notes"]).casefold()
        behavior = " ".join(profile["behavior_notes"]).casefold()
        self.assertIn("rutting", anatomy)
        self.assertIn("intimidation", anatomy)
        self.assertIn("excavat", anatomy)
        self.assertIn("predator", behavior)

    def test_hunter_vigor_sourced_only_by_full_fixture_not_bestiary_top_level(self):
        self.assertTrue(any("Vigor" in x for x in self.hunter["open_mechanics"]) or
                        any("HP" in x for x in self.hunter["open_mechanics"]))
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
