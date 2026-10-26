"""B04/B05 source-constrained High Gifted L1–3 character build verification."""
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.b05_high_gifted_l1_l3_v0 import (
    LEVELS, ABILITIES, ABILITY_COST, WEAPON_TRAINING,
    DISCIPLINES_L1, DISCIPLINE_L2, FAMILIARITIES, GEAR_SP, TALENT,
    AUTHORED_ACCESS, AUTHORED_UPCAST_T2, PLAUSIBLE_EXPLANATIONS,
    profile, verify,
)
from scripts.b05_high_gifted_amplification_v0 import (
    EMOTIONS, PILOT_LINKS, HighGiftedWindow, Target, thrown_flame,
)

ROOT = Path(__file__).resolve().parents[1]


class HighGiftedBuildTests(unittest.TestCase):
    def test_01_source_guard_and_fixed_legal_creation(self):
        self.assertTrue(verify())
        self.assertEqual(sum(ABILITY_COST[x] for x in ABILITIES.values()), 28)
        self.assertEqual(sum(DISCIPLINES_L1.values()), 8)
        self.assertEqual(sum(WEAPON_TRAINING.values()), 2)
        self.assertEqual(sum(GEAR_SP.values()), 52)
        self.assertEqual((len(FAMILIARITIES), TALENT),
                         (2, "TAL-G01 Emotional Poise"))
        self.assertEqual(DISCIPLINES_L1, {
            "Emotional Discipline": 2, "Disguise": 2,
            "Throwing": 2, "Medicine": 2,
        })
        self.assertEqual(DISCIPLINE_L2, ("Veil Theory", 1))
        self.assertEqual(LEVELS, (1, 2, 3))
        self.assertEqual(set(PLAUSIBLE_EXPLANATIONS), {"Joy", "Anger"})
        self.assertTrue(all(PLAUSIBLE_EXPLANATIONS.values()))

    def test_02_eight_distinct_legal_links_and_no_free_repertoire(self):
        for lvl in LEVELS:
            sheet = profile(lvl)
            links = sheet["emotion_aspect_links"]
            self.assertEqual(list(links), list(EMOTIONS))
            self.assertEqual(len({x["pillar"] for x in links.values()}), 8)
            self.assertEqual(len({x["aspect"] for x in links.values()}), 8)
            self.assertEqual(sum(x["compatibility"] == "P" for x in links.values()), 2)
            self.assertEqual(sum(x["compatibility"] == "S" for x in links.values()), 6)
            for emotion in EMOTIONS:
                self.assertEqual((links[emotion]["pillar"],
                                  links[emotion]["aspect"],
                                  links[emotion]["compatibility"]), PILOT_LINKS[emotion])
                self.assertEqual(links[emotion]["creation_interpretation"],
                                 PLAUSIBLE_EXPLANATIONS.get(emotion))
                self.assertEqual(sheet["authored_linked_techniques"][emotion],
                                 list(AUTHORED_ACCESS[emotion]))
            self.assertEqual(sheet["prepared_techniques"], None)
            self.assertEqual(sheet["individually_learned_pillar_techniques"], None)
            self.assertEqual(sheet["active_emotion"], None)
            self.assertEqual(sheet["emotion_intensity"], None)
        self.assertEqual(sum(map(len, AUTHORED_ACCESS.values())), 9)

    def test_03_level_progression_and_unchanged_budgets(self):
        before = None
        for lvl in LEVELS:
            s = profile(lvl)
            self.assertEqual(s["level"], lvl)
            self.assertEqual((s["archetype"], s["focus"]), ("Gifted", "High"))
            self.assertEqual(s["abilities"], ABILITIES)
            self.assertEqual(s["talents"], [TALENT])
            self.assertEqual(s["talent_selections_available"], 1)
            self.assertEqual(s["learned_points"], 8 + (lvl >= 2))
            self.assertTrue(all(rank <= 2 for rank in s["learned_disciplines"].values()))
            self.assertEqual(s["learned_disciplines"].get("Veil Theory"),
                             (1 if lvl >= 2 else None))
            self.assertEqual(s["weapon_training"], WEAPON_TRAINING)
            self.assertEqual((s["hp_max"], s["vigor_max"], s["vp_max"]),
                             (12, 12 * lvl, 6 * lvl))
            self.assertEqual((s["turn_ap"], s["projection_tempo"],
                              s["physical_tempo"], s["guard_capacity"]),
                             (30 + 6*(lvl-1), 2 if lvl == 3 else 1, 1, 1))
            self.assertEqual(s["max_used_tier"], 2 if lvl == 3 else 1)
            self.assertEqual(s["universal"], ["Veil Inspection"]
                             + (["Blink"] if lvl == 3 else []))
            self.assertEqual(s["authored_upcast_t2"],
                             sorted(AUTHORED_UPCAST_T2) if lvl == 3 else [])
            self.assertEqual((s["initiative"], s["first_dodge"],
                              s["normal_regen_throughput"]), (4, 14, 3))
            if before is not None:
                self.assertEqual(s["abilities"], before["abilities"])
                self.assertEqual(s["emotion_aspect_links"], before["emotion_aspect_links"])
                self.assertEqual(s["talents"], before["talents"])
            before = s

    def test_04_equipment_weapon_and_actual_flame_accuracy(self):
        for lvl in LEVELS:
            s = profile(lvl)
            self.assertEqual(s["equipment_sp"], GEAR_SP)
            self.assertEqual(s["starting_budget_sp"], 150)
            self.assertEqual((s["starting_spent_sp"], s["silver_remaining_sp"]),
                             (52, 98))
            self.assertEqual((s["armor"], s["wielded_weapon"]), (3, "Dagger"))
            self.assertEqual((s["dagger_attack_bonus"], s["dagger_guard_defense"]),
                             (4, 14))
            self.assertEqual(s["thrown_flame_attack_bonus"], 4)
            self.assertEqual(s["thrown_flame_t1_precision_attack_bonus"], 5)
            self.assertEqual(s["thrown_flame_t1_reach_max_squares"], 4)
            self.assertEqual((s["thrown_flame_t1_vp"],
                              s["thrown_flame_t1_surge_spent_vp"]), (2, 1))
            self.assertEqual(s["thrown_flame_available_tier"], 2 if lvl == 3 else 1)
            self.assertEqual(s["thrown_flame_available_tier_vp"], 4 if lvl == 3 else 2)
            self.assertEqual(s["thrown_flame_available_tier_surge_spent_vp"], 1)

    def test_05_real_high_gifted_l1_heightened_surge_transaction(self):
        w = HighGiftedWindow(1, "Joy", initial_intensity="heightened")
        s = profile(1)
        first = w.cast(thrown_flame(), Target("enemy", 4),
                       safe="Reach", surge="Precision")
        self.assertEqual(first["status"], "resolve")
        self.assertEqual(first["action_ap"], 20)
        self.assertEqual(first["paid_vp"], 3)
        self.assertEqual(first["surge_vp"], 1)
        self.assertEqual((w.ap, w.vp, w.safe_step, w.surge_allowance),
                         (10, 3, 0, 0))
        with self.assertRaises(ValueError):
            w.cast(thrown_flame(), Target("enemy", 3), surge="Potency")
        self.assertEqual(s["emotional_discipline_check_bonus"], 4)
        self.assertEqual(s["instability_check_bonus"], 3)

    def test_06_evoked_surge_no_free_safe_step_and_emotion_bound_access(self):
        w = HighGiftedWindow(1, "Joy")
        with self.assertRaises(ValueError):
            w.cast(thrown_flame(), Target("enemy", 3), safe="Precision")
        result = w.cast(thrown_flame(), Target("enemy", 3), surge="Precision")
        self.assertEqual((result["paid_vp"], result["ap_remaining"]), (3, 10))
        wrong = HighGiftedWindow(1, "Sadness")
        with self.assertRaises(ValueError):
            wrong.cast(thrown_flame(), Target("enemy", 3))
        self.assertEqual((wrong.ap, wrong.vp, wrong.surge_allowance), (30, 6, 1))

    def test_07_level3_double_projection_is_not_double_surge(self):
        w = HighGiftedWindow(3, "Joy", initial_intensity="heightened")
        first = w.cast(thrown_flame(2), Target("enemy", 3),
                       safe="Potency", surge="Precision")
        self.assertEqual(first["paid_vp"], 5)
        self.assertEqual((first["ap_remaining"], first["vp_remaining"]), (22, 13))
        second = w.cast(thrown_flame(), Target("enemy", 3))
        self.assertEqual((second["ap_remaining"], second["vp_remaining"]), (2, 11))
        with self.assertRaises(ValueError):
            w.cast(thrown_flame(), Target("enemy", 3), surge="Reach")
        self.assertEqual(w.surge_allowance, 0)

    def test_08_paid_deepen_overload_cannot_bypass_ap_at_any_level(self):
        for lvl in LEVELS:
            s = profile(lvl)
            self.assertFalse(s["deepen_plus_flame_same_turn"])
            self.assertFalse(s["overload_plus_flame_same_turn"])
            w = HighGiftedWindow(lvl, "Joy")
            self.assertTrue(w.deepen(20, awareness=2, discipline=2))
            self.assertEqual(w.ap, s["turn_ap"]-24)
            with self.assertRaises(ValueError):
                w.cast(thrown_flame(), Target("enemy", 3), safe="Precision")
            h = HighGiftedWindow(lvl, "Joy", initial_intensity="heightened")
            h.overload()
            with self.assertRaises(ValueError):
                h.cast(thrown_flame(), Target("enemy", 3),
                       safe="Precision", risky="Reach", instability_roll=1,
                       miscast_roll=14)
            self.assertEqual(h.vp, 6 * lvl)
            self.assertFalse(h.instability_used)

    def test_09_l3_blink_affordability_not_free_casting(self):
        self.assertFalse(profile(1)["blink_affordable_from_full_vp"])
        self.assertFalse(profile(2)["blink_affordable_from_full_vp"])
        self.assertTrue(profile(3)["blink_affordable_from_full_vp"])
        for lvl in LEVELS:
            s = profile(lvl)
            self.assertEqual(s["general_action_ap"], 24)
            self.assertEqual(s["projection_action_ap"], 20)
            self.assertEqual(s["physical_action_ap"], 30)

    def test_10_isolation_and_invalid_level(self):
        a = profile(1)
        a["abilities"]["Awareness"] = -2
        a["emotion_aspect_links"]["Joy"]["pillar"] = "Lightning"
        a["learned_disciplines"]["Emotional Discipline"] = 99
        a["equipment_sp"]["Dagger"] = 0
        b = profile(1)
        self.assertEqual(b["abilities"]["Awareness"], 2)
        self.assertEqual(b["emotion_aspect_links"]["Joy"]["pillar"], "Fire")
        self.assertEqual(b["learned_disciplines"]["Emotional Discipline"], 2)
        self.assertEqual(b["equipment_sp"]["Dagger"], 4)
        for value in (0, 4, True, 2.0, "3", -1):
            with self.assertRaises(ValueError):
                profile(value)

    def test_11_canonical_sources_do_not_permit_free_actions_or_aspects(self):
        paths = {
            "gifted": "docs/rules/08-archetypes/gifted.md",
            "amplification": "docs/rules/07-veil-magic/high-gifted-amplification-and-miscasts-v0.md",
            "creation": "docs/rules/02-character-creation/character-creation-foundation.md",
            "talent": "docs/rules/10-advancement/talents-level-1-5-v0.md",
            "flame": "docs/rules/07-veil-magic/conjure-flame-v0.md",
            "training": "docs/rules/02-character-creation/abilities-and-training.md",
            "roster": "docs/design/b04-b05-mvp-pilot-roster-gifted-anointed-readiness-v0.md",
        }
        data = {}
        for name, relative in paths.items():
            path = ROOT / relative
            if not path.is_file():
                self.skipTest("Full repository canonical sources required for source audit")
            data[name] = path.read_text()
        self.assertIn("exactly **eight permanent emotion-to-Aspect links**", data["gifted"])
        self.assertIn("ceil(effective technique VP price / 4)", data["amplification"])
        self.assertIn("TAL-G01 — Emotional Poise", data["talent"])
        self.assertIn("**Once per Emotion Window**", data["talent"])
        self.assertIn("**28 ability points**", data["training"])
        self.assertIn("**8 Learned Discipline points**", data["training"])
        self.assertIn("**150 sp", data["creation"])
        self.assertIn("**[Projection]**", data["flame"])
        self.assertIn("6 Strong / 2 Plausible", data["roster"])
        self.assertIn("24+20=44", data["amplification"])


if __name__ == "__main__":
    unittest.main()