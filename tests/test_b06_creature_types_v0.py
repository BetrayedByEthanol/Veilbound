"""B06 creature taxonomy/index regression checks (Python standard library only).

These tests enforce design-status honesty and source boundaries. JSON Schema
Draft 2020-12 validation should additionally be run with a standards-compliant
validator; this suite does not implement a JSON Schema engine.
"""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CREATURE_SCHEMA = ROOT / "schemas/b06-enemy-benchmark-v0.schema.json"
INDEX_SCHEMA = ROOT / "schemas/b06-bestiary-index-v0.schema.json"
BESTIARY = ROOT / "content/creatures/b06-initial-bestiary-v0.json"
SENTRY = ROOT / "content/creatures/b06-firebound-sentry.v0.json"
HUNTER_FIXTURE = ROOT / "content/creatures/b06-hunter-of-the-woods.v0.json"


class B06CreatureTaxonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.creature_schema = json.loads(CREATURE_SCHEMA.read_text(encoding="utf-8"))
        cls.index_schema = json.loads(INDEX_SCHEMA.read_text(encoding="utf-8"))
        cls.index = json.loads(BESTIARY.read_text(encoding="utf-8"))
        cls.sentry = json.loads(SENTRY.read_text(encoding="utf-8"))
        cls.hunter_fixture = json.loads(HUNTER_FIXTURE.read_text(encoding="utf-8"))
        cls.entries = {e["id"]: e for e in cls.index["entries"]}

    def test_schema_versions_and_collection_contract(self):
        self.assertEqual(self.creature_schema["properties"]["schema_version"]["const"], "b06-enemy-v0")
        self.assertEqual(self.index_schema["properties"]["schema_version"]["const"], "b06-bestiary-index-v0")
        self.assertEqual(self.index["schema_version"], "b06-bestiary-index-v0")
        self.assertEqual(self.index["status"], "DESIGN_ONLY_NOT_CANONICAL_BESTIARY")
        self.assertEqual(self.index_schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_shared_schema_definitions_do_not_drift(self):
        for name in ("creatureProfile", "plannedCapability", "bestiaryEntry", "encounterGuidance"):
            self.assertEqual(self.creature_schema["$defs"][name],
                             self.index_schema["$defs"][name], name)

    def test_all_fourteen_ids_unique_and_contiguous(self):
        ids = [e["id"] for e in self.index["entries"]]
        self.assertEqual(len(ids), 14)
        self.assertEqual(len(set(ids)), 14)
        self.assertEqual(ids, [f"B06-EN-{n:02d}" for n in range(1, 15)])
        self.assertTrue(all(e["entry_status"] in
                            {"EXECUTABLE_FIXTURE_EXISTS", "CONCEPT_ONLY", "DEFERRED"}
                            for e in self.index["entries"]))

    def test_three_executable_benchmarks_linked_without_altering_sentry(self):
        executable = [e for e in self.index["entries"]
                      if e["entry_status"] == "EXECUTABLE_FIXTURE_EXISTS"]
        self.assertEqual([e["id"] for e in executable], ["B06-EN-01", "B06-EN-02", "B06-EN-03"])
        self.assertEqual(executable[0]["fixture_path"],
                         "content/creatures/b06-firebound-sentry.v0.json")
        self.assertEqual(executable[1]["fixture_path"],
                         "content/creatures/b06-ordinary-human-soldier.v0.json")
        self.assertEqual(executable[2]["fixture_path"],
                         "content/creatures/b06-hunter-of-the-woods.v0.json")
        self.assertEqual(self.hunter_fixture["creature_profile"], executable[2]["creature_profile"])
        self.assertEqual(self.hunter_fixture["bestiary_ref"], "B06-EN-03")
        self.assertEqual(self.sentry["bestiary_ref"], "B06-EN-01")
        self.assertEqual(self.sentry["creature_profile"],
                         executable[0]["creature_profile"])
        self.assertEqual([a["id"] for a in self.sentry["attack_profiles"]],
                         ["B06-AT-01", "B06-AT-02"])

    def test_sentry_attack_math_and_resources_unchanged(self):
        s = self.sentry
        self.assertEqual(s["identity"]["type"], "player_rules_derived_opponent")
        self.assertEqual(s["defenses"]["hp_max"], 12)
        self.assertEqual(s["defenses"]["vigor_max"], 36)
        self.assertEqual(s["defenses"]["dodge_base"], 14)
        self.assertEqual(s["defenses"]["guard_base"], 17)
        self.assertEqual(s["resources"]["max_vp"], 6)
        self.assertEqual((s["resources"]["turn_ap"], s["resources"]["physical_action_ap"],
                          s["resources"]["projection_action_ap"]), (42, 20, 30))
        self.assertEqual([p["attack_roll"]["total_bonus"] for p in s["attack_profiles"]], [7, 7])
        self.assertEqual(s["attack_profiles"][1]["additional_packets"][0]["fixed_base"], 2)
        self.assertEqual(s["attack_profiles"][1]["additional_packets"][1]["fixed_base"], 1)
        self.assertEqual(s["effects"][0]["effective_committed_vp"], 3)

    def test_all_concept_entries_have_no_fake_combat_fixture(self):
        for e in self.index["entries"]:
            if e["entry_status"] != "EXECUTABLE_FIXTURE_EXISTS":
                self.assertIsNone(e["fixture_path"], e["id"])
                self.assertTrue(e["open_mechanics"], e["id"])
                self.assertFalse(any(c["state"] == "existing_authority_only"
                                     for c in e["planned_capabilities"]), e["id"])
                for c in e["planned_capabilities"]:
                    if c["state"] == "requires_authored_attack_or_effect":
                        self.assertTrue(c["missing_authority"], (e["id"], c["id"]))

    def test_player_species_human_only_for_mvp(self):
        for e in self.index["entries"]:
            p = e["creature_profile"]
            self.assertIn(p["mvp_player_option"],
                          {"human_only", "not_playable_mvp", "not_applicable"})
            if p["mvp_player_option"] == "human_only":
                self.assertEqual(p["species_or_kind"], "Human")

    def test_untrained_human_not_auto_veil_caster(self):
        soldier = self.entries["B06-EN-02"]["creature_profile"]
        self.assertIn("ordinary_no_independent_invocation", soldier["veil_relationship"])
        self.assertEqual(soldier["family"], "ordinary_humanoid")
        self.assertTrue(any(
            "non-focus" in note.casefold() or "non-archetype" in note.casefold()
            for note in self.entries["B06-EN-02"]["open_mechanics"]
        ))

    def test_inward_and_outward_species_do_not_inherit_focus(self):
        for n in (5, 6):
            p = self.entries[f"B06-EN-{n:02d}"]["creature_profile"]
            self.assertIn("inward_dominant", p["veil_relationship"])
            self.assertEqual(p["mvp_player_option"], "not_playable_mvp")
        elf = self.entries["B06-EN-07"]["creature_profile"]
        self.assertIn("outward_dominant", elf["veil_relationship"])
        self.assertTrue(any("Vigor" in note for note in elf["physiology_notes"]))
        self.assertEqual(elf["mvp_player_option"], "not_playable_mvp")

    def test_dwarf_has_no_invented_species_attributes(self):
        dwarf = self.entries["B06-EN-08"]
        self.assertEqual(dwarf["entry_status"], "DEFERRED")
        self.assertEqual(dwarf["creature_profile"]["veil_relationship"], ["undetermined"])
        self.assertEqual(dwarf["planned_capabilities"], [])

    def test_hunter_venom_delivery_is_sourced_but_uncalibrated(self):
        hunter = self.entries["B06-EN-03"]
        self.assertEqual(hunter["creature_profile"]["family"], "natural_beast")
        self.assertTrue(any("horn" in s.lower() for s in hunter["creature_profile"]["physiology_notes"]))
        self.assertTrue(any("venomous" in s.lower() for s in hunter["creature_profile"]["physiology_notes"]))
        bite = next(c for c in hunter["planned_capabilities"] if c["name"] == "Venomous bite")
        self.assertEqual(bite["state"], "existing_authority_only")
        self.assertTrue(any("calibration" in x.lower() for x in bite["missing_authority"]))
        self.assertEqual(self.hunter_fixture["attack_profiles"][0]["toxin_delivery"]["profile_id"],
                         "B06-TX-HUNTER-SLOW-MY")

    def test_spider_veil_touch_needs_authored_alteration(self):
        spider = self.entries["B06-EN-04"]
        self.assertEqual(spider["creature_profile"]["family"], "veil_touched_beast")
        innate = [c for c in spider["planned_capabilities"] if c["source_class"] == "innate_veil"]
        self.assertEqual(len(innate), 1)
        self.assertEqual(innate[0]["state"], "requires_authored_attack_or_effect")

    def test_dragon_has_no_spellcasting_and_flight_is_deferred(self):
        dragon = self.entries["B06-EN-09"]
        self.assertEqual(dragon["creature_profile"]["cognition"], "animal_like")
        self.assertIn("innate_pillar_affinity", dragon["creature_profile"]["veil_relationship"])
        self.assertTrue(any(c["name"] == "Flight" and c["state"] == "deferred"
                            for c in dragon["planned_capabilities"]))
        self.assertFalse(any(c["source_class"] == "learned_veil"
                             for c in dragon["planned_capabilities"]))

    def test_raised_turned_and_spirit_remain_distinct(self):
        self.assertEqual(self.entries["B06-EN-10"]["creature_profile"]["body_state"], "corporeal_raised")
        for n in (11, 12):
            self.assertEqual(self.entries[f"B06-EN-{n:02d}"]["creature_profile"]["body_state"],
                             "corporeal_turned")
        spirit = self.entries["B06-EN-14"]["creature_profile"]
        self.assertEqual(spirit["body_state"], "nonphysical_spirit")
        self.assertEqual(spirit["physical_presence"], "nonphysical_no_ordinary_interaction")

    def test_manifestation_is_nonsentient_and_not_anointed(self):
        e = self.entries["B06-EN-13"]
        p = e["creature_profile"]
        self.assertEqual(p["family"], "pillar_manifestation")
        self.assertEqual(p["cognition"], "non_sentient_pattern")
        self.assertIn("surge_manifestation", p["veil_relationship"])
        self.assertEqual(e["entry_status"], "DEFERRED")
        self.assertTrue(any("Not an Anointed" in c["concept"] for c in e["planned_capabilities"]))

    def test_future_toxin_attack_requires_separate_delivery_source(self):
        toxin = self.creature_schema["$defs"]["attack"]["properties"]["toxin_delivery"]
        self.assertIn("source_ref", toxin["properties"])
        self.assertTrue(any("source_ref" in part.get("then", {}).get("required", [])
                            for part in toxin["allOf"]))

    def test_non_archetype_progression_optional_but_player_progression_required(self):
        root = self.creature_schema
        self.assertNotIn("progression", root["required"])
        conditional = root["allOf"][0]
        self.assertIn("progression", conditional["then"]["required"])
        self.assertIn("creature_profile", conditional["else"]["required"])


    def test_nonprojectors_and_innate_attacks_require_explicit_authority(self):
        resources = self.creature_schema["properties"]["resources"]["properties"]
        self.assertIn("null", resources["projection_action_ap"]["type"])
        self.assertIn("null", resources["natural_regeneration_throughput"]["type"])
        attack = self.creature_schema["$defs"]["attack"]
        self.assertIn("null", attack["properties"]["attack_roll"]["type"])
        self.assertIn("source_class", attack["required"])
        self.assertTrue(any(
            {"source_authority_ref", "resolution_rule_ref"}.issubset(set(branch["then"]["required"]))
            and "natural_weapon" in branch["if"].get("properties", {}).get("source_class", {}).get("enum", [])
            for branch in attack["allOf"]
        ))


    def test_attack_requires_source_class_even_when_rolled_and_hp_damaging(self):
        """A rolled, non-null-HP natural attack must not evade its source contract."""
        attack = self.creature_schema["$defs"]["attack"]
        self.assertIn("source_class", attack["required"])
        self.assertIn("natural_weapon", attack["properties"]["source_class"]["enum"])
        self.assertTrue(any(
            {"source_authority_ref", "resolution_rule_ref"}.issubset(
                set(branch["then"]["required"])
            )
            and "natural_weapon" in branch["if"].get("properties", {})
                .get("source_class", {}).get("enum", [])
            for branch in attack["allOf"]
        ))
        self.assertTrue(all("source_class" in p for p in self.sentry["attack_profiles"]))



if __name__ == "__main__":
    unittest.main()
