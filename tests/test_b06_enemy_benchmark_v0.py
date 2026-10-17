"""B06 first enemy/attack fixture checks. Standard library only.

The JSON Schema is the machine contract; these tests validate the authored
example's current rules arithmetic and prohibit implicit new poison powers.
A full Draft 2020-12 schema-validator pass remains separately recommended.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "schemas" / "b06-enemy-benchmark-v0.schema.json"
F = ROOT / "content" / "creatures" / "b06-firebound-sentry.v0.json"


class FireboundSentryFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(S.read_text(encoding="utf-8"))
        cls.foe = json.loads(F.read_text(encoding="utf-8"))

    def test_contract_shape_and_ids(self):
        f = self.foe
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertTrue(set(self.schema["required"]).issubset(f.keys()))
        self.assertEqual(f["schema_version"], "b06-enemy-v0")
        self.assertEqual(f["id"], "B06-EN-01")
        self.assertEqual([p["id"] for p in f["attack_profiles"]], ["B06-AT-01", "B06-AT-02"])
        self.assertEqual(f["status"], "EXECUTABLE_TEST_FIXTURE")

    def test_complete_ability_budget(self):
        cost = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
        a = self.foe["abilities"]
        self.assertEqual(set(a.keys()), {"strength", "agility", "precision", "intelligence",
                          "awareness", "presence", "vitality", "veil_affinity", "veil_control"})
        self.assertEqual(sum(cost[v] for v in a.values()), 28)

    def test_derived_resources_and_defenses(self):
        f = self.foe
        a, d, r = f["abilities"], f["defenses"], f["resources"]
        training = f["progression"]["weapon_training"]["One-Handed Swords"]
        self.assertEqual(d["hp_max"], 10 + a["vitality"])
        self.assertEqual(d["vigor_max"], (10 + a["vitality"]) * f["benchmark_level"])
        self.assertEqual(r["max_vp"], (2 + a["veil_affinity"]) * f["benchmark_level"])
        self.assertEqual(d["initiative_bonus"], a["agility"] + a["awareness"])
        self.assertEqual(d["dodge_base"], 10 + min(a["agility"], d["dodge_agility_cap"]) + a["awareness"])
        self.assertEqual(d["guard_base"], 10 + a["strength"] + a["agility"] + training)
        self.assertEqual(d["guard_capacity"], 3)
        self.assertEqual(r["natural_regeneration_throughput"], a["vitality"] + 3 + 1)
        self.assertEqual((r["turn_ap"], r["physical_action_ap"], r["projection_action_ap"]), (42, 20, 30))

    def test_gear_and_training(self):
        f = self.foe
        self.assertEqual(sum(g["cost_sp"] for g in f["equipment"]), 70)
        self.assertLessEqual(sum(g["cost_sp"] for g in f["equipment"]), 150)
        self.assertEqual(f["progression"]["weapon_training"], {"One-Handed Swords": 2})
        self.assertEqual(len(f["progression"]["talents"]), 3)

    def test_only_real_eligible_chosen_reserve(self):
        f, r = self.foe, self.foe["resources"]
        e = f["effects"][0]
        self.assertEqual(e["source_technique"], "Conjure Flame — Fire/Conflagration")
        self.assertEqual(e["used_tier"], 1)
        self.assertEqual(e["effective_committed_vp"], 4 * e["used_tier"] - 1)
        self.assertEqual(e["establishment_spent_vp"], 0)
        self.assertEqual(e["activation_ap"], 30)
        states = {s["id"]: s for s in r["start_states"]}
        for s in states.values():
            self.assertEqual(s["available_vp"] + s["committed_vp"] + s["spent_vp"], r["max_vp"])
            self.assertEqual(s["hp"], f["defenses"]["hp_max"])
            self.assertEqual(s["vigor"], f["defenses"]["vigor_max"])
        self.assertEqual(states["cold_start"]["committed_vp"], 0)
        self.assertEqual(states["prepared_start"]["committed_vp"], 3)
        self.assertIn(e["id"], states["prepared_start"]["active_effects"])
        self.assertNotIn(e["id"], states["cold_start"]["active_effects"])

    def test_no_free_spell_and_weapon_attack_same_turn(self):
        r = self.foe["resources"]
        ap_left = r["turn_ap"] - self.foe["effects"][0]["activation_ap"]
        self.assertEqual(ap_left, 12)
        self.assertLess(ap_left, r["physical_action_ap"])
        self.assertLessEqual(2 * r["physical_action_ap"], r["turn_ap"])
        self.assertGreater(3 * r["physical_action_ap"], r["turn_ap"])

    def test_exclusive_attack_state_and_roll(self):
        f = self.foe
        plain, flame = f["attack_profiles"]
        self.assertEqual(plain["requires_effect_inactive"], flame["required_active_effect"])
        self.assertIsNone(plain["required_active_effect"])
        self.assertIsNone(flame["requires_effect_inactive"])
        for attack in (plain, flame):
            self.assertEqual(attack["ap"], 20)
            roll = attack["attack_roll"]
            self.assertEqual(roll["total_bonus"],
                             f["abilities"]["strength"] + f["abilities"]["agility"]
                             + roll["effective_training"] + roll["situational_bonus"])
            self.assertEqual((roll["ability_a"], roll["ability_b"]), ("Strength", "Agility"))

    def test_typed_packets_and_critical_provenance(self):
        plain, flame = self.foe["attack_profiles"]
        self.assertEqual(plain["additional_packets"], [])
        self.assertEqual([p["kind"] for p in flame["additional_packets"]], ["hp", "vigor"])
        self.assertEqual(flame["additional_packets"][0]["damage_type"], "Fire")
        self.assertEqual(flame["additional_packets"][0]["mitigation"], "fire_resistance")
        self.assertEqual(flame["additional_packets"][0]["fixed_base"], 2)
        self.assertEqual(flame["additional_packets"][1]["mitigation"], "none")
        self.assertEqual(flame["additional_packets"][1]["fixed_base"], 1)
        expr = flame["additional_packets"][1]["extra_formula"]
        self.assertEqual((expr["die"], expr["multiplier"], expr["divisor"], expr["vc_bonus"]), ("d6", 1, 4, 0))
        self.assertEqual([1 + (i + 3) // 4 for i in range(1, 7)], [2, 2, 2, 2, 3, 3])
        for attack in (plain, flame):
            p = attack["primary_hp_packet"]
            self.assertEqual(p["damage_type"], "Piercing")
            self.assertEqual((p["fixed_base"], p["die"], p["armor_penetration"]), (3, "d6", 2))
            self.assertEqual(p["strength_contribution"], "light")

    def test_defender_armor_math_is_post_hit_only(self):
        raw_piercing = 3 + 4 + (self.foe["abilities"]["strength"] // 2)
        self.assertEqual(raw_piercing, 8)
        self.assertEqual(raw_piercing - max(3 - 2, 0), 7)  # Restorative Vanguard
        self.assertEqual(raw_piercing - max(5 - 2, 0), 5)  # Preservation Guardian

    def test_no_invented_toxin_or_fire_exaltation(self):
        f = self.foe
        self.assertTrue(all(p["toxin_delivery"] is None for p in f["attack_profiles"]))
        self.assertTrue(any("No Fire Exaltation" in s for s in f["validation"]["known_exclusions"]))
        self.assertTrue(any("does not authorize" in s for s in f["validation"]["known_exclusions"]
                            if "Neither toxin" in s))


if __name__ == "__main__":
    unittest.main()
