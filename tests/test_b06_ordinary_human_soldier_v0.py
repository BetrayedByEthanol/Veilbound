"""B06-EN-02 ordinary non-Archetype human benchmark tests (stdlib only).

These pin one proposed neutral 24-AP non-Focus physical action and +0 Focus
regeneration offset; they do not silently promote them to universal combat law.
"""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "content" / "creatures" / "b06-ordinary-human-soldier.v0.json"
BESTIARY = ROOT / "content" / "creatures" / "b06-initial-bestiary-v0.json"
SCHEMA = ROOT / "schemas" / "b06-enemy-benchmark-v0.schema.json"


class OrdinaryHumanSoldierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foe = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.index = json.loads(BESTIARY.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.entry = next(e for e in cls.index["entries"] if e["id"] == "B06-EN-02")

    def test_no_archetype_focus_or_invocation(self):
        f = self.foe
        self.assertEqual(f["id"], "B06-EN-02")
        self.assertEqual(f["status"], "EXECUTABLE_TEST_FIXTURE")
        self.assertEqual(f["identity"]["type"], "ordinary_non_archetype_humanoid")
        for name in ("archetype", "focus", "pillar"):
            self.assertIsNone(f["identity"][name])
        self.assertNotIn("progression", f)
        self.assertEqual(f["resources"]["max_vp"], 0)
        self.assertIsNone(f["resources"]["projection_action_ap"])
        self.assertFalse(f["effects"])
        self.assertTrue(all(a["source_class"] == "mundane_weapon"
                            for a in f["attack_profiles"]))

    def test_all_nine_abilities_and_benchmark_points(self):
        a = self.foe["abilities"]
        costs = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
        self.assertEqual(set(a), {"strength", "agility", "precision", "intelligence",
                                   "awareness", "presence", "vitality", "veil_affinity",
                                   "veil_control"})
        self.assertEqual(sum(costs[v] for v in a.values()), 28)
        self.assertEqual((a["strength"], a["agility"], a["awareness"], a["vitality"]),
                         (2, 2, 1, 2))

    def test_resources_follow_benchmark_without_focus(self):
        f = self.foe
        a, d, r = f["abilities"], f["defenses"], f["resources"]
        self.assertEqual(f["benchmark_level"], 3)
        self.assertEqual(d["hp_max"], 10 + a["vitality"])
        self.assertEqual(d["vigor_max"], (10 + a["vitality"]) * f["benchmark_level"])
        self.assertEqual(r["turn_ap"], 30 + 6 * (f["benchmark_level"] - 1))
        self.assertEqual(r["natural_regeneration_throughput"], max(0, a["vitality"]) + 0)
        self.assertEqual(r["movement_points"], 12)
        self.assertEqual(r["reaction_capacity"], 1)
        self.assertEqual(r["max_vp"], 0)

    def test_neutral_physical_cost_is_explicit_not_a_focus(self):
        f = self.foe
        r = f["resources"]
        self.assertEqual(r["physical_action_ap"], 24)
        self.assertEqual(r["turn_ap"] // r["physical_action_ap"], 1)
        self.assertLess(r["turn_ap"] - r["physical_action_ap"], r["physical_action_ap"])
        self.assertEqual(len(f["attack_profiles"]), 1)
        self.assertEqual(f["attack_profiles"][0]["ap"], r["physical_action_ap"])
        self.assertTrue(any("proposed" in s.lower() or "provisional" in s.lower()
                            for s in f["validation"]["known_exclusions"]))

    def test_single_real_sword_attack_roll_and_damage(self):
        f, p = self.foe, self.foe["attack_profiles"][0]
        a = f["abilities"]
        self.assertEqual(p["id"], "B06-AT-03")
        self.assertEqual(p["source_class"], "mundane_weapon")
        self.assertEqual(p["resolution_kind"], "ordinary_weapon_attack")
        self.assertEqual(p["action_class"], "physical")
        self.assertEqual((p["attack_roll"]["ability_a"], p["attack_roll"]["ability_b"]),
                         ("Strength", "Agility"))
        self.assertEqual(p["attack_roll"]["training_family"], "One-Handed Swords")
        self.assertEqual(p["attack_roll"]["total_bonus"],
                         a["strength"] + a["agility"] + p["attack_roll"]["effective_training"])
        packet = p["primary_hp_packet"]
        self.assertEqual((packet["fixed_base"], packet["die"]), (3, "d6"))
        self.assertEqual(packet["strength_contribution"], "light")
        self.assertEqual(packet["armor_penetration"], 2)
        self.assertEqual(packet["damage_type"], "Piercing")
        self.assertEqual(packet["mitigation"], "physical_armor_after_penetration")

    def test_no_magical_toxin_or_extra_packets(self):
        p = self.foe["attack_profiles"][0]
        self.assertEqual(p["additional_packets"], [])
        self.assertIsNone(p["toxin_delivery"])
        self.assertIsNone(p["required_active_effect"])
        self.assertIsNone(p["requires_effect_inactive"])
        self.assertEqual(p["source_authority_ref"],
                         "docs/rules/05-combat/weapons-and-armor.md")
        self.assertFalse(self.foe["resources"]["start_states"][0]["active_effects"])

    def test_sword_and_shield_guard_not_stacked_training(self):
        f, a, d = self.foe, self.foe["abilities"], self.foe["defenses"]
        training = f["attack_profiles"][0]["attack_roll"]["effective_training"]
        sword_guard = 10 + a["strength"] + a["agility"] + training
        self.assertEqual(sword_guard, 16)
        self.assertEqual(d["guard_base"], sword_guard + 2)  # Shield bonus +2.
        self.assertIn("Shield", d["guard_instrument"])
        tempo = f["resources"]["turn_ap"] // f["resources"]["physical_action_ap"]
        self.assertEqual(d["guard_capacity"], tempo + 1)  # Shield +1 Guard.
        self.assertEqual(d["guard_capacity"], 2)

    def test_brigan_dodge_and_initiative(self):
        f, a, d = self.foe, self.foe["abilities"], self.foe["defenses"]
        self.assertEqual(d["armor"], 5)
        self.assertEqual(d["armor_name"], "Brigandine")
        self.assertEqual(d["dodge_agility_cap"], 2)
        self.assertEqual(d["dodge_base"], 10 + min(a["agility"], d["dodge_agility_cap"])
                         + a["awareness"])
        self.assertEqual(d["dodge_base"], 13)
        self.assertEqual(d["initiative_bonus"], a["agility"] + a["awareness"])

    def test_optional_starter_gear_price(self):
        gear = self.foe["equipment"]
        costs = {g["name"]: g["cost_sp"] for g in gear}
        self.assertEqual(costs, {"Brigandine": 95, "Sword": 22, "Shield": 16,
                                 "Standard adventuring pack": 8})
        self.assertEqual(sum(costs.values()), 141)
        self.assertLessEqual(sum(costs.values()), 150)

    def test_cold_start_vp_accounting(self):
        f, r = self.foe, self.foe["resources"]
        self.assertEqual(len(r["start_states"]), 1)
        s = r["start_states"][0]
        self.assertEqual(s["available_vp"] + s["committed_vp"] + s["spent_vp"], 0)
        self.assertEqual(s["hp"], f["defenses"]["hp_max"])
        self.assertEqual(s["vigor"], f["defenses"]["vigor_max"])

    def test_two_defender_damage_examples_are_post_hit_only(self):
        # Attack roll/defenses/critical and opponent effects still resolve separately.
        d6 = 4
        raw = 3 + d6 + self.foe["abilities"]["strength"] // 2
        self.assertEqual(raw, 8)
        self.assertEqual(max(0, raw - max(3 - 2, 0)), 7)
        self.assertEqual(max(0, raw - max(5 - 2, 0)), 5)

    def test_bestiary_status_and_physical_profile_link(self):
        f, entry = self.foe, self.entry
        self.assertEqual(f["bestiary_ref"], entry["id"])
        self.assertEqual(entry["entry_status"], "EXECUTABLE_FIXTURE_EXISTS")
        self.assertEqual(entry["fixture_path"], "content/creatures/b06-ordinary-human-soldier.v0.json")
        self.assertEqual(f["creature_profile"], entry["creature_profile"])
        self.assertEqual(entry["creature_profile"]["family"], "ordinary_humanoid")
        self.assertEqual(entry["creature_profile"]["veil_relationship"],
                         ["ordinary_no_independent_invocation"])
        self.assertEqual(set(self.schema["$defs"]["attack"]["required"])
                         .issubset(f["attack_profiles"][0].keys()), True)


if __name__ == "__main__":
    unittest.main()
