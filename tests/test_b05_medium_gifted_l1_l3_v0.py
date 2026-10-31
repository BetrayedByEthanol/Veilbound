"""Structural source checks; Ward events remain isolated, never native G4."""
from pathlib import Path
import unittest

from scripts.b05_high_gifted_amplification_v0 import PILOT_LINKS
from scripts.b05_medium_gifted_conduit_design_v0 import MediumGiftedWardDesign
from scripts.b05_medium_gifted_l1_l3_v0 import (
    ABILITIES, GEAR, LEARNED_L1, LEVELS, ORDINARY_TECHNIQUES,
    PLAUSIBLE, TALENT, UPCAST_T2, profile, verify, ward_budget,
)

ROOT = Path(__file__).resolve().parents[1]


class MediumGiftedBuildTests(unittest.TestCase):
    def test_creation_ability_budget_and_medium_focus_identity(self):
        self.assertTrue(verify())
        self.assertEqual(ABILITIES["Agility"], 1)
        self.assertEqual(ABILITIES["Veil Control"], 2)
        for level in LEVELS:
            s = profile(level)
            self.assertEqual((s["archetype"], s["focus"], s["ability_points"]),
                             ("Gifted", "Medium", 28))
            self.assertEqual(s["abilities"], ABILITIES)
            self.assertEqual(s["resonance"], 0)
            self.assertEqual(s["talents"], [TALENT])
            self.assertEqual(
                (s["talent_selections_available"],
                 s["saved_talent_selections"]),
                (1 + int(level == 3), int(level == 3)))
            self.assertEqual(s["learned_family_allocation_l1"],
                             {"Cultural and Specialized": 4,
                              "Physical and Fieldcraft": 2,
                              "Professional and Technical": 2})
            self.assertEqual(s["learned_points"], 8 + int(level >= 2))
            self.assertTrue(all(x <= 2 for x in s["learned_disciplines"].values()))
            self.assertEqual(s["weapon_training"], {"Small Blades": 2})
            self.assertEqual(s["weapon_development_points"], 2)

    def test_level_progression_derivatives_not_high_focus(self):
        for level, ap, vp, slots in ((1, 30, 4, 1), (2, 36, 8, 1),
                                     (3, 42, 12, 2)):
            with self.subTest(level=level):
                s = profile(level)
                self.assertEqual((s["turn_ap"], s["vp_max"], s["conduit_slots"]),
                                 (ap, vp, slots))
                self.assertEqual((s["physical_action_ap"], s["projection_action_ap"],
                                  s["general_action_ap"]), (24, 24, 24))
                self.assertEqual((s["physical_tempo"], s["projection_tempo"],
                                  s["guard_capacity"], s["opportunity_capacity"]),
                                 (1, 1, 1, 1))
                self.assertEqual((s["hp_max"], s["vigor_max"], s["normal_regen_throughput"]),
                                 (12, 12*level, 3))
                self.assertEqual((s["initiative"], s["first_dodge"],
                                  s["dagger_attack_bonus"], s["dagger_guard_defense"],
                                  s["thrown_flame_attack_bonus"]), (3, 13, 3, 13, 3))
                self.assertEqual((s["emotional_discipline_check_bonus"],
                                  s["instability_check_bonus"]), (4, 4))
                self.assertEqual(s["max_used_tier"], 2 if level == 3 else 1)
                self.assertEqual(s["universal"], ["Veil Inspection"] +
                                 (["Blink"] if level == 3 else []))
                self.assertEqual(s["authored_upcast_t2"], sorted(UPCAST_T2)
                                 if level == 3 else [])

    def test_budget_equipment_and_actual_fictional_choices(self):
        for level in LEVELS:
            s = profile(level)
            self.assertEqual((s["starting_budget_sp"], s["starting_spent_sp"],
                              s["silver_remaining_sp"]), (150, 52, 98))
            self.assertEqual(s["equipment_sp"], GEAR)
            self.assertEqual(s["armor"], 3)
            self.assertEqual(s["wielded_weapon"], "Dagger")
            self.assertEqual(s["learned_disciplines"]["Disguise"], 2)
            self.assertEqual(s["learned_disciplines"]["Medicine"], 2)
            self.assertEqual(s["learned_disciplines"].get("Veil Theory"),
                             1 if level >= 2 else None)

    def test_exact_fixed_eight_links_and_unprepared_catalogue(self):
        for level in LEVELS:
            s = profile(level)
            links = s["emotion_aspect_links"]
            self.assertEqual(set(links), set(PILOT_LINKS))
            self.assertEqual(len({x["pillar"] for x in links.values()}), 8)
            self.assertEqual(len({x["aspect"] for x in links.values()}), 8)
            self.assertEqual({e for e in links if links[e]["compatibility"] == "P"},
                             set(PLAUSIBLE))
            self.assertEqual(s["authored_linked_techniques"],
                             {e: list(t) for e, t in ORDINARY_TECHNIQUES.items()})
            self.assertIsNone(s["prepared_techniques"])
            self.assertIsNone(s["individually_learned_pillar_techniques"])
            self.assertIsNone(s["active_emotion"])
            self.assertIsNone(s["emotion_intensity"])

    def test_ward_initially_unplaced_and_authorized_two_outputs_only(self):
        for level in LEVELS:
            s = profile(level)
            self.assertFalse(s["conduit_initially_established"])
            self.assertEqual((s["conduit_form"], s["conduit_anchor"]),
                             ("Ward", "self"))
            self.assertEqual(set(s["conduit_emotion_expressions"]), {"Fear", "Trust"})
            self.assertEqual(s["conduit_grades"], {"I": 1, "II": 2, "III": 3})
            self.assertEqual((s["conduit_initial_general_ap"],
                              s["reconduction_general_ap"],
                              s["reconduction_spent_vp"]), (24, 24, 3))
            self.assertFalse(s["two_initial_conduits_same_turn"])
            self.assertFalse(s["deepening_plus_t1_flame_same_turn"])

    def test_each_grade_each_level_conserves_real_medium_vp(self):
        for level in LEVELS:
            for grade in (1, 2, 3):
                with self.subTest(level=level, grade=grade):
                    w = ward_budget(level, grade=grade)
                    self.assertEqual((w["available_vp"], w["committed_vp"],
                                      w["spent_vp"]), (4*level-grade, grade, 0))
                    self.assertEqual(w["ap_remaining"], 6 * level)
                    self.assertEqual((w["slots_used"], w["slots_max"]),
                                     (1, 1 if level < 3 else 2))
                    self.assertEqual(w["status"], "Active")
                    self.assertEqual(sum(w[k] for k in
                                         ("available_vp", "committed_vp", "spent_vp")),
                                     4*level)

    def test_grade_three_l1_blocks_paid_ordinary_spell(self):
        m = MediumGiftedWardDesign(1)
        m.begin_turn("Fear")
        m.establish(grade=3)
        m.end_turn()
        m.begin_turn("Joy")
        self.assertEqual(m.conduits[0].status, "Dormant")
        before = (m.ap, m.available, m.committed, m.spent)
        with self.assertRaises(ValueError):
            m.spend_other_action(ap_cost=24, spent_vp=2)
        self.assertEqual((m.ap, m.available, m.committed, m.spent), before)
        self.assertNotIn("projected_surge", profile(1))

    def test_grade_one_l1_allows_exact_single_ordinary_spell(self):
        m = MediumGiftedWardDesign(1)
        m.begin_turn("Fear")
        m.establish(grade=1)
        m.end_turn()
        m.begin_turn("Joy")
        m.spend_other_action(ap_cost=24, spent_vp=2)  # Conjure Flame T1 budget ONLY
        self.assertEqual((m.ap, m.available, m.committed, m.spent),
                         (6, 1, 1, 2))
        with self.assertRaises(ValueError):
            m.spend_other_action(ap_cost=24, spent_vp=2)
        m.check()

    def test_level_three_two_wards_use_two_turns_no_double_pulse(self):
        m = MediumGiftedWardDesign(3)
        m.begin_turn("Fear")
        m.establish(grade=3)
        with self.assertRaises(ValueError):
            m.establish(grade=3)
        m.end_turn()
        m.begin_turn("Fear")
        m.establish(grade=3)
        self.assertEqual((m.available, m.committed, m.spent), (6, 6, 0))
        self.assertEqual(m.pulse("one", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=6), 3)
        self.assertEqual(m.pulse("two", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=6), 3)
        self.assertEqual(m.pulse("three", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=6), 0)

    def test_reconduction_not_fundable_with_pending_grade_refund(self):
        m = MediumGiftedWardDesign(1)
        m.begin_turn("Fear")
        c = m.establish(grade=2)
        m.end_turn()
        m.begin_turn("Fear")
        before = (m.available, m.committed, m.spent, m.ap)
        with self.assertRaises(ValueError):
            m.reconduct_grade(c.serial, 1)
        self.assertEqual((m.available, m.committed, m.spent, m.ap), before)

    def test_level_three_blink_and_commitment_compete(self):
        self.assertFalse(profile(1)["blink_affordable_without_commitment"])
        self.assertFalse(profile(2)["blink_affordable_without_commitment"])
        s = profile(3)
        self.assertTrue(s["blink_affordable_without_commitment"])
        self.assertFalse(s["blink_affordable_with_two_grade_ii_conduits"])
        self.assertEqual(s["normal_t2_flame_vp"], 4)

    def test_no_inheritance_of_high_surge_or_low_anchor(self):
        for level in LEVELS:
            s = profile(level)
            for forbidden in ("projected_surge", "safe_step", "anchored_emotion",
                              "deep_embodiment", "inward_boost", "consecration"):
                self.assertNotIn(forbidden, s)

    def test_defensive_copy_and_invalid_input(self):
        a = profile(1)
        a["abilities"]["Agility"] = -2
        a["emotion_aspect_links"]["Joy"]["pillar"] = "Lightning"
        a["equipment_sp"]["Dagger"] = 0
        a["learned_disciplines"]["Medicine"] = 99
        b = profile(1)
        self.assertEqual(b["abilities"]["Agility"], 1)
        self.assertEqual(b["emotion_aspect_links"]["Joy"]["pillar"], "Fire")
        self.assertEqual(b["equipment_sp"]["Dagger"], 4)
        self.assertEqual(b["learned_disciplines"]["Medicine"], 2)
        for level in (-1, 0, True, 2.0, "3", 4):
            with self.assertRaises(ValueError):
                profile(level)
                ward_budget(level)
        for grade in (0, 4, True, 2.0, "II"):
            with self.assertRaises(ValueError):
                ward_budget(1, grade=grade)

    def test_repository_sources_bind_candidate_as_rule_and_structure(self):
        sources = {
            "gifted": "docs/rules/08-archetypes/gifted.md",
            "ward": "docs/rules/07-veil-magic/medium-gifted-ward-conduit-v0.md",
            "talents": "docs/rules/10-advancement/talents-level-1-5-v0.md",
            "creation": "docs/rules/02-character-creation/character-creation-foundation.md",
            "high": "scripts/b05_high_gifted_l1_l3_v0.py",
        }
        if not all((ROOT / name).is_file() for name in sources.values()):
            self.skipTest("Full repo source documents unavailable locally")
        data = {name: (ROOT / path).read_text(encoding="utf-8")
                for name, path in sources.items()}
        self.assertIn("Medium Gifted — Conduits and retuning", data["gifted"])
        self.assertIn("medium-gifted-ward-conduit-v0.md", data["gifted"])
        for phrase in ("Holdfast", "Shared Reserve", "24 AP", "1/2/3",
                       "Direct Vigor", "one Pulse", "self-anchored"):
            self.assertIn(phrase, data["ward"])
        self.assertIn("TAL-G01 — Emotional Poise", data["talents"])
        self.assertIn("28 ability points", data["creation"])
        self.assertIn("PILOT_LINKS", data["high"])


if __name__ == "__main__":
    unittest.main()

class ConduitReleasePolicyTests(unittest.TestCase):
    def test_paid_reestablishment_after_window_and_distinct_serial(self):
        m = MediumGiftedWardDesign(2)
        m.begin_turn("Fear")
        c = m.establish(grade=2)
        self.assertEqual(m.release(c.serial).grade, 2)
        self.assertEqual((m.available, m.committed, m.spent), (8, 0, 0))
        with self.assertRaises(ValueError):
            m.establish(grade=3)
        m.end_turn()
        m.begin_turn("Trust")
        again = m.establish(grade=3)
        self.assertGreater(again.serial, c.serial)
        self.assertEqual((m.available, m.committed, m.spent), (5, 3, 0))
        self.assertEqual(again.status, "Active")

    def test_release_cannot_replay_event_or_reuse_serial(self):
        m = MediumGiftedWardDesign(3)
        m.begin_turn("Fear")
        old = m.establish(grade=2)
        self.assertEqual(m.pulse("hit", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=4), 2)
        m.release(old.serial)
        with self.assertRaises(ValueError):
            m.reconduct_grade(old.serial, 3)
        with self.assertRaises(ValueError):
            m.release(old.serial)
        with self.assertRaises(ValueError):
            m.pulse("hit", recipient="caster", resource="hp",
                    damage_type="Piercing", post_mitigation=4)
        m.check()
