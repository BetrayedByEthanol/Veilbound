"""Hunter B06-EN-03 full sourced enemy fixture arithmetic and contract tests.

Fixture execution means deterministic attack/contest data and authoritative
rules exist. These checks are NOT Monte Carlo fights or a certified CR.
"""
import copy
import json
import math
import unittest
from pathlib import Path

from scripts.validate_b06_footprints import validate_b06_document

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "content/creatures/b06-hunter-of-the-woods.v0.json"
PARTIAL = ROOT / "content/creatures/b06-hunter-physiology.v0.json"
INDEX = ROOT / "content/creatures/b06-initial-bestiary-v0.json"
SCHEMA = ROOT / "schemas/b06-enemy-benchmark-v0.schema.json"
CONTENT_README = ROOT / "content/README.md"
SOURCE = ROOT / "docs/design/b06-hunter-full-statblock-v0.md"
POUNCE = ROOT / "docs/rules/05-combat/hunter-pounce-and-prey-takedown-v0.md"
BITE = ROOT / "docs/rules/05-combat/hunter-bite-venom-and-horn-v0.md"


def hp_damage(raw, penetration, armor):
    return max(raw - max(armor - penetration, 0), 0)


class B06HunterFullFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hunter = json.loads(FULL.read_text(encoding="utf-8"))
        cls.partial = json.loads(PARTIAL.read_text(encoding="utf-8"))
        cls.index = json.loads(INDEX.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.entry = next(x for x in cls.index["entries"] if x["id"] == "B06-EN-03")
        cls.profiles = {a["id"]: a for a in cls.hunter["attack_profiles"]}
        cls.doc = SOURCE.read_text(encoding="utf-8")
        cls.pounce_source = POUNCE.read_text(encoding="utf-8")
        cls.bite_source = BITE.read_text(encoding="utf-8")

    def test_complete_fixture_promoted_but_challenge_unrated(self):
        h, e = self.hunter, self.entry
        self.assertEqual(h["schema_version"], "b06-enemy-v0")
        self.assertEqual(h["id"], "B06-EN-03")
        self.assertEqual(h["status"], "EXECUTABLE_TEST_FIXTURE")
        self.assertEqual(e["entry_status"], "EXECUTABLE_FIXTURE_EXISTS")
        self.assertEqual(e["fixture_path"], "content/creatures/b06-hunter-of-the-woods.v0.json")
        self.assertEqual(h["bestiary_ref"], e["id"])
        self.assertEqual(e["encounter_guidance"]["challenge_rating"]["status"], "unrated")
        self.assertIsNone(e["encounter_guidance"]["challenge_rating"]["value"])
        self.assertTrue(all(s["evidence_status"] == "untested" for s in
                            e["encounter_guidance"]["test_scenarios"]))

    def test_content_index_tracks_three_executable_and_eleven_other_entries(self):
        contents = CONTENT_README.read_text(encoding="utf-8")
        entries = self.index["entries"]
        executable = [e for e in entries
                      if e["entry_status"] == "EXECUTABLE_FIXTURE_EXISTS"]
        nonexec = [e for e in entries
                   if e["entry_status"] != "EXECUTABLE_FIXTURE_EXISTS"]
        self.assertEqual(len(entries), 14)
        self.assertEqual(len(executable), 3)
        self.assertEqual(len(nonexec), 11)
        self.assertIn("three executable benchmark fixtures", contents)
        self.assertIn("eleven remaining non-executable entries", contents)
        for entry in executable:
            self.assertIn(entry["fixture_path"].replace("content/", ""), contents)
        self.assertIn("unrated contextual encounter guidance", contents)

    def test_fixture_matches_bestiary_creature_metadata(self):
        self.assertEqual(self.hunter["creature_profile"], self.entry["creature_profile"])
        self.assertEqual(self.hunter["creature_profile"]["family"], "natural_beast")
        self.assertEqual(self.hunter["identity"]["type"], "authored_creature")
        self.assertIsNone(self.hunter["identity"]["focus"])
        self.assertIsNone(self.hunter["identity"]["archetype"])

    def test_physio_snapshot_remains_a_separate_nonexecutable_record(self):
        p = self.partial
        self.assertEqual(p["record_status"], "PHYSIOLOGY_ONLY_NOT_EXECUTABLE")
        self.assertEqual(p["calibration_status"], "PROVISIONAL_B06")
        self.assertIsNone(p["full_enemy_fixture_path"])
        self.assertEqual(p["creature_id"], self.hunter["id"])
        for key in ("vitality", "agility", "awareness"):
            self.assertEqual(p["abilities"][key], self.hunter["abilities"][key])

    def test_nine_authored_ability_fields_and_nonprojector(self):
        a = self.hunter["abilities"]
        self.assertEqual((a["strength"], a["agility"], a["precision"],
                          a["intelligence"], a["awareness"], a["presence"],
                          a["vitality"], a["veil_affinity"], a["veil_control"]),
                         (4, 2, 1, -2, 2, -1, 4, 0, 0))
        self.assertEqual(self.hunter["resources"]["max_vp"], 0)
        self.assertIsNone(self.hunter["resources"]["projection_action_ap"])
        self.assertFalse(self.hunter["creature_profile"]["veil_relationship"][0]
                         != "ordinary_no_independent_invocation")

    def test_hp_armor_dodge_and_vigor_derive_from_physio(self):
        h, p = self.hunter, self.partial
        a, d = h["abilities"], h["defenses"]
        self.assertEqual(d["hp_max"], p["hp"]["max"])
        self.assertEqual(d["hp_max"], 10 + a["vitality"])
        self.assertEqual(d["vigor_max"], d["hp_max"] * h["benchmark_level"])
        self.assertEqual((d["vigor_max"], d["armor"]), (42, 3))
        self.assertIsNone(d["dodge_agility_cap"])
        self.assertEqual(d["dodge_base"], 10 + a["agility"] + a["awareness"])

    def test_initiative_has_no_bonus_for_being_predator(self):
        h = self.hunter
        self.assertEqual(h["defenses"]["initiative_bonus"],
                         h["abilities"]["agility"] + h["abilities"]["awareness"])
        self.assertEqual(h["defenses"]["initiative_bonus"], 4)

    def test_turn_ap_action_count_and_round_capacities(self):
        h = self.hunter
        r, d = h["resources"], h["defenses"]
        self.assertEqual(r["turn_ap"], min(120, 30 + 6 * (h["benchmark_level"] - 1)))
        self.assertEqual((r["turn_ap"], r["physical_action_ap"]), (42, 24))
        self.assertEqual(r["turn_ap"] // r["physical_action_ap"], 1)
        self.assertEqual((d["guard_capacity"], r["reaction_capacity"]), (1, 1))
        self.assertEqual(r["turn_ap"] - r["physical_action_ap"], 18)

    def test_guard_not_legal_without_instrument(self):
        d = self.hunter["defenses"]
        self.assertIsNone(d["guard_instrument"])
        self.assertIsNone(d["guard_base"])
        self.assertEqual(d["guard_capacity"], 1)
        self.assertIn("no legal natural Guard instrument", self.doc)

    def test_dodge_pressure_round_sequence(self):
        b = self.hunter["defenses"]["dodge_base"]
        self.assertEqual([b - 2 * n for n in range(4)], [14, 12, 10, 8])

    def test_regeneration_and_recovery_derive_without_free_stamina(self):
        h = self.hunter
        r = h["resources"]
        self.assertEqual(r["natural_regeneration_throughput"], 4)
        self.assertEqual(r["natural_regeneration_throughput"], max(h["abilities"]["vitality"], 0))
        self.assertEqual(math.floor(0.25 * h["defenses"]["vigor_max"] + 0.5), 11)
        self.assertEqual(hp_damage(8, 2, 3), 7)
        self.assertEqual((14 - 7 + 4, 42 - 4), (11, 38))

    def test_footprint_reference_and_single_pool(self):
        h = self.hunter
        f = h["creature_profile"]["footprint"]
        self.assertEqual((f["width_cells"], f["length_cells"]), (1, 2))
        self.assertEqual(f["cell_ids"], ["head", "rear"])
        self.assertEqual(f["reference_cell_id"], "head")
        self.assertEqual(validate_b06_document(h, "hunter"), [])

    def test_ordinary_move_and_pounce_budget(self):
        self.assertEqual(self.hunter["resources"]["movement_points"], 12)
        self.assertEqual(2 * 12, 24)
        self.assertEqual((3 * 12) // 2, 18)
        self.assertIn("three translated steps", self.pounce_source)

    def test_source_authored_four_modes_and_unique_ids(self):
        self.assertEqual(list(self.profiles), ["B06-AT-04", "B06-AT-05", "B06-AT-06", "B06-AT-07"])
        for attack in self.profiles.values():
            self.assertEqual(attack["action_class"], "physical")
            self.assertEqual(attack["ap"], 24)
            self.assertEqual(attack["source_class"], "natural_weapon")
            self.assertTrue((ROOT / attack["source_authority_ref"]).exists())
            self.assertTrue((ROOT / attack["resolution_rule_ref"]).exists())

    def test_bite_decomposes_attack_no_physical_damage_double_count(self):
        bite = self.profiles["B06-AT-04"]
        roll = bite["attack_roll"]
        self.assertEqual((roll["ability_a"], roll["ability_b"]), ("Strength", "Agility"))
        self.assertEqual(roll["total_bonus"], 4 + 2 + 0 + 0)
        self.assertEqual(roll["effective_training"], 0)
        packet = bite["primary_hp_packet"]
        self.assertEqual((packet["fixed_base"], packet["die"], packet["armor_penetration"]),
                         (3, "d6", 1))
        self.assertEqual(packet["strength_contribution"], "none")
        self.assertEqual(hp_damage(3 + 4, 1, 5), 3)
        self.assertEqual(hp_damage(3 + 1, 1, 5), 0)

    def test_horn_bash_decomposes_attack_not_an_automatic_shove(self):
        horn = self.profiles["B06-AT-05"]
        roll = horn["attack_roll"]
        self.assertEqual((roll["ability_a"], roll["ability_b"]), ("Strength", "Precision"))
        self.assertEqual(roll["total_bonus"], 4 + 1 + 0 + 0)
        packet = horn["primary_hp_packet"]
        self.assertEqual((packet["fixed_base"], packet["damage_type"],
                          packet["armor_penetration"]), (2, "Crush", 0))
        self.assertEqual(packet["strength_contribution"], "none")
        self.assertIsNone(horn["toxin_delivery"])
        self.assertNotIn("linked_contest", horn)
        self.assertEqual(hp_damage(2 + 4, 0, 5), 1)

    def test_pounce_one_bite_and_separate_force_contest(self):
        bite, pounce = self.profiles["B06-AT-04"], self.profiles["B06-AT-06"]
        self.assertEqual(pounce["attack_roll"], bite["attack_roll"])
        self.assertEqual(pounce["primary_hp_packet"], bite["primary_hp_packet"])
        self.assertEqual(pounce["toxin_delivery"], bite["toxin_delivery"])
        self.assertEqual(pounce["linked_contest"]["kind"], "pounce_balance")
        self.assertEqual(pounce["linked_contest"]["total_pressure_bonus"], 4)
        self.assertEqual(pounce["linked_contest"]["extra_ap_cost"], 0)
        self.assertEqual(pounce["linked_contest"]["result_on_strict_win"], "prone_in_place")
        self.assertEqual(9 + 4, 13)
        self.assertLess(9 + 4, 12 + 3)

    def test_horn_drive_contest_has_no_fabricated_attack_or_damage(self):
        drive = self.profiles["B06-AT-07"]
        self.assertIsNone(drive["attack_roll"])
        self.assertIsNone(drive["primary_hp_packet"])
        self.assertIsNone(drive["toxin_delivery"])
        self.assertEqual(drive["linked_contest"]["kind"], "horn_drive_shove")
        self.assertEqual(drive["linked_contest"]["total_pressure_bonus"], 4)
        self.assertEqual(drive["linked_contest"]["extra_ap_cost"], 0)
        self.assertEqual(13 + 4, 17)
        self.assertGreater(17, 8 + 2 + 2)

    def test_contest_components_and_authority_crossrefs(self):
        for id in ("B06-AT-06", "B06-AT-07"):
            contest = self.profiles[id]["linked_contest"]
            self.assertEqual(contest["total_pressure_bonus"],
                             contest["attacker_modifier"] + contest["training_modifier"]
                             + contest["other_modifier"])
            for ref in ("defender_rule_ref", "resolution_rule_ref"):
                self.assertTrue((ROOT / contest[ref]).exists())

    def test_injection_gated_to_bite_not_horn(self):
        bite, horn, pounce, drive = (self.profiles[k] for k in self.profiles)
        for attack in (bite, pounce):
            delivery = attack["toxin_delivery"]
            self.assertEqual(delivery["profile_id"], "B06-TX-HUNTER-SLOW-MY")
            self.assertEqual(delivery["route"], "injection")
            self.assertTrue(delivery["requires_surviving_puncture"])
            self.assertEqual(delivery["source_ref"], "B06-SRC-HUNTER-GROOVED-CANINES")
        self.assertIsNone(horn["toxin_delivery"])
        self.assertIsNone(drive["toxin_delivery"])

    def test_vp_start_state_no_veil_and_no_pregame_poison(self):
        r = self.hunter["resources"]
        self.assertEqual(len(r["start_states"]), 1)
        st = r["start_states"][0]
        self.assertEqual((st["hp"], st["vigor"]), (14, 42))
        self.assertEqual((st["available_vp"], st["committed_vp"], st["spent_vp"]), (0, 0, 0))
        self.assertEqual(st["active_effects"], [])
        self.assertEqual(self.hunter["effects"], [])

    def test_enemy_schema_linked_contest_option_is_nonbreaking(self):
        schema = self.schema["$defs"]["attack"]
        self.assertNotIn("linked_contest", schema["required"])
        self.assertIn("linked_contest", schema["properties"])
        self.assertEqual(schema["properties"]["linked_contest"]["properties"]
                         ["extra_ap_cost"]["const"], 0)

    def test_linked_contest_kinds_are_structurally_bound_in_schema(self):
        """Always-on stdlib guard: ensure conditionals cannot disappear unnoticed."""
        attack = self.schema["$defs"]["attack"]
        linked = attack["properties"]["linked_contest"]

        def nested_rule(kind):
            return next(branch["then"] for branch in linked["allOf"]
                        if branch["if"]["properties"]["kind"]["const"] == kind)

        def parent_rule(kind):
            # Earlier attack.allOf clauses cover ordinary attack_roll,
            # primary_hp_packet and source_class; they are not contests.
            # A missing linked_contest discriminant is not an error.
            return next(
                branch["then"] for branch in attack["allOf"]
                if "linked_contest" in branch.get("if", {}).get("properties", {})
                and branch["if"]["properties"]["linked_contest"]
                ["properties"]["kind"]["const"] == kind
            )

        self.assertEqual(nested_rule("pounce_balance")["properties"]
                         ["result_on_strict_win"]["const"], "prone_in_place")
        self.assertEqual(nested_rule("horn_drive_shove")["properties"]
                         ["result_on_strict_win"]["const"],
                         "straight_head_forward_shove_and_whole_body_advance")

        pounce = parent_rule("pounce_balance")["properties"]
        self.assertEqual(pounce["attack_roll"]["type"], "object")
        self.assertEqual(pounce["primary_hp_packet"]["type"], "object")
        self.assertEqual(pounce["primary_hp_packet"]["properties"]["damage_type"]["const"],
                         "Piercing")
        self.assertEqual(pounce["toxin_delivery"]["type"], "object")
        self.assertTrue(pounce["toxin_delivery"]["properties"]
                        ["requires_surviving_puncture"]["const"])
        self.assertEqual(pounce["additional_packets"]["maxItems"], 0)
        self.assertEqual(pounce["resolution_kind"]["const"], "authored_natural_attack")
        pounce_profile = self.profiles["B06-AT-06"]
        bite_profile = self.profiles["B06-AT-04"]
        for key in ("weapon_or_source", "source_authority_ref", "resolution_rule_ref"):
            self.assertEqual(pounce[key]["const"], pounce_profile[key])
        self.assertEqual(pounce["attack_roll"]["properties"]["ability_a"]["const"],
                         bite_profile["attack_roll"]["ability_a"])
        self.assertEqual(pounce["attack_roll"]["properties"]["ability_b"]["const"],
                         bite_profile["attack_roll"]["ability_b"])
        self.assertEqual(pounce["primary_hp_packet"]["properties"]["source"]["const"],
                         bite_profile["primary_hp_packet"]["source"])
        self.assertEqual(pounce["toxin_delivery"]["properties"]["source_ref"]["const"],
                         "B06-SRC-HUNTER-GROOVED-CANINES")
        self.assertEqual(pounce["toxin_delivery"]["properties"]["profile_id"]["const"],
                         "B06-TX-HUNTER-SLOW-MY")

        drive = parent_rule("horn_drive_shove")["properties"]
        for field in ("attack_roll", "primary_hp_packet", "toxin_delivery"):
            with self.subTest(field=field):
                self.assertEqual(drive[field]["type"], "null")
        self.assertEqual(drive["additional_packets"]["maxItems"], 0)
        self.assertEqual(drive["resolution_kind"]["const"], "authored_non_damage_effect")
        drive_profile = self.profiles["B06-AT-07"]
        for key in ("weapon_or_source", "source_authority_ref", "resolution_rule_ref"):
            self.assertEqual(drive[key]["const"], drive_profile[key])
        self.assertIn("B06-SRC-HUNTER-FRONTAL-HORN", drive["weapon_or_source"]["const"])
        for props in (pounce, drive):
            self.assertEqual(props["action_class"]["const"], "physical")
            self.assertEqual(props["ap"]["const"], 24)

    def test_linked_contest_invalid_mutations_rejected_by_draft202012(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("optional jsonschema dependency unavailable")
        Draft202012Validator.check_schema(self.schema)
        validator = Draft202012Validator(self.schema)
        self.assertTrue(validator.is_valid(self.hunter))

        bite = self.profiles["B06-AT-04"]
        horn = self.profiles["B06-AT-05"]
        drive = self.profiles["B06-AT-07"]
        cases = [
            ("pounce uses shove win result", "B06-AT-06",
             ("linked_contest", "result_on_strict_win"),
             "straight_head_forward_shove_and_whole_body_advance"),
            ("drive uses prone win result", "B06-AT-07",
             ("linked_contest", "result_on_strict_win"), "prone_in_place"),
            ("pounce missing rolled Bite", "B06-AT-06", ("attack_roll",), None),
            ("pounce missing Bite HP packet", "B06-AT-06",
             ("primary_hp_packet",), None),
            ("pounce missing injection", "B06-AT-06",
             ("toxin_delivery",), None),
            ("pounce uses Crush not Bite Piercing", "B06-AT-06",
             ("primary_hp_packet", "damage_type"), "Crush"),
            ("pounce adds extra HP packet", "B06-AT-06",
             ("additional_packets",), [bite["primary_hp_packet"]]),
            ("drive retains rolled Horn attack", "B06-AT-07",
             ("attack_roll",), bite["attack_roll"]),
            ("drive retains HP damage packet", "B06-AT-07",
             ("primary_hp_packet",), bite["primary_hp_packet"]),
            ("drive retains venom", "B06-AT-07",
             ("toxin_delivery",), bite["toxin_delivery"]),
            ("drive retains additional packets", "B06-AT-07",
             ("additional_packets",), [bite["primary_hp_packet"]]),
            ("drive mislabeled damaging attack", "B06-AT-07",
             ("resolution_kind",), "authored_natural_attack"),
            ("pounce switches to frontal horn", "B06-AT-06",
             ("weapon_or_source",), horn["weapon_or_source"]),
            ("pounce switches to Horn roll", "B06-AT-06",
             ("attack_roll",), horn["attack_roll"]),
            ("pounce replaces canine toxin source", "B06-AT-06",
             ("toxin_delivery", "source_ref"), "B06-SRC-HUNTER-FRONTAL-HORN"),
            ("pounce uses foreign HP packet source", "B06-AT-06",
             ("primary_hp_packet", "source"), horn["primary_hp_packet"]["source"]),
            ("pounce replaces authority with Horn source", "B06-AT-06",
             ("source_authority_ref",), "docs/rules/05-combat/weapon-attack-and-guard-math.md"),
            ("drive switches to canines", "B06-AT-07",
             ("weapon_or_source",), bite["weapon_or_source"]),
            ("drive changes source authority", "B06-AT-07",
             ("source_authority_ref",), "docs/rules/05-combat/hunter-pounce-and-prey-takedown-v0.md"),
            ("drive changes resolution source", "B06-AT-07",
             ("resolution_rule_ref",), "docs/rules/05-combat/hunter-pounce-and-prey-takedown-v0.md"),
        ]
        for label, attack_id, key_path, bad_value in cases:
            with self.subTest(case=label):
                mutated = copy.deepcopy(self.hunter)
                profile = next(a for a in mutated["attack_profiles"]
                               if a["id"] == attack_id)
                owner = profile
                for key in key_path[:-1]:
                    owner = owner[key]
                owner[key_path[-1]] = bad_value
                self.assertFalse(validator.is_valid(mutated), label)

        # A malicious replacement of BOTH the declared natural source AND roll
        # must not turn Pounce into a Horn attack while preserving Prone metadata.
        compound = copy.deepcopy(self.hunter)
        pounce = next(a for a in compound["attack_profiles"] if a["id"] == "B06-AT-06")
        pounce["weapon_or_source"] = horn["weapon_or_source"]
        pounce["attack_roll"] = copy.deepcopy(horn["attack_roll"])
        self.assertFalse(validator.is_valid(compound),
                         "Pounce must not validate after simultaneous Horn source/roll swap")

    def test_schema_validation_when_jsonschema_installed(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("optional jsonschema dependency unavailable; stdlib checks still run")
        Draft202012Validator.check_schema(self.schema)
        validator = Draft202012Validator(self.schema)
        errors = list(validator.iter_errors(self.hunter))
        self.assertEqual([(list(e.path), e.message) for e in errors], [])


if __name__ == "__main__":
    unittest.main()
