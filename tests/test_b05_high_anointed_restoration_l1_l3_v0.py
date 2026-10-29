"""Source-constrained High Anointed L1–3 build and negative permission tests."""
from dataclasses import replace
from pathlib import Path
import unittest

from scripts.b05_high_anointed_restoration_l1_l3_v0 import (
    ABILITIES, BOND, LEVELS, MISSION, IMPRINT, profile, isolated_witness, verify,
)
from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, mission_event, set_bond, returning_step, kindled_flame,
    conjure_flame_l3, guided_regeneration_l3,
)

ROOT = Path(__file__).resolve().parents[1]


class HighAnointedStructuralL1L3(unittest.TestCase):
    def test_source_constrained_budget_training_equipment_talents(self):
        self.assertTrue(verify())
        for lv in LEVELS:
            s = profile(lv)
            self.assertEqual(28, s["ability_points"])
            self.assertEqual(8 + (lv >= 2), s["learned_points"])
            self.assertEqual(2, s["weapon_development_points"])
            self.assertEqual((52, 98), (s["starting_spent_sp"], s["silver_remaining_sp"]))
            self.assertEqual(["TAL-A01 Imprint Recall"], s["talents"])
            self.assertEqual(2, s["medicine_check_bonus"] - ABILITIES["Intellect"])
            self.assertEqual(["Basic Heal", "Guided Regeneration"], s["known_bonded_techniques"])
            self.assertEqual([], s["known_other_aspect_techniques"])
            self.assertEqual((BOND, MISSION, IMPRINT), (s["bond"], s["mission"], s["birth_imprint"]))
            self.assertEqual(0, s["resonance"])
            self.assertFalse(s["independent_full_focus_certified"])

    def test_level_progression_and_one_high_talent(self):
        for lv in LEVELS:
            s = profile(lv)
            self.assertEqual((12, 12*lv, 6*lv), (s["hp_max"], s["vigor_max"], s["vp_max"]))
            self.assertEqual(30 + 6*(lv-1), s["turn_ap"])
            self.assertEqual((1, 2 if lv == 3 else 1), (s["physical_tempo"], s["projection_tempo"]))
            self.assertEqual((1, 1), (s["guard_capacity"], s["opportunity_capacity"]))
            self.assertEqual(4 if lv >= 2 else 3, s["signature_range_squares"])
            self.assertEqual(lv >= 3, s["l3_guided_primary_lesser_eligible"])
            self.assertFalse(s["l3_basic_heal_lesser_eligible"])
            self.assertEqual(lv >= 3, s["two_signature_actions_fit"])
            self.assertFalse(s["signature_plus_general_fit"])
            self.assertEqual(lv >= 3, s["blink_affordable_at_full_vp"])
        with self.assertRaises(ValueError): profile(0)
        with self.assertRaises(ValueError): profile(4)
        with self.assertRaises(ValueError): profile(True)

    def test_restoration_signature_l1_l2_range_and_no_vigor_without_destiny(self):
        for lv in LEVELS:
            actor = Anointed(lv, "High", "Restoration")
            with self.assertRaises(ValueError):
                returning_step(actor, receipt="far", target_id="patient", recipient_hp=5,
                               recipient_max_hp=12, recipient_vigor=8, ap_available=20,
                               distance=5 if lv >= 2 else 4)
            with self.assertRaises(ValueError):
                returning_step(actor, receipt="no-vigor", target_id="patient", recipient_hp=5,
                               recipient_max_hp=12, recipient_vigor=0, ap_available=20)
            with self.assertRaises(ValueError):
                returning_step(actor, receipt="full", target_id="patient", recipient_hp=12,
                               recipient_max_hp=12, recipient_vigor=2, ap_available=20,
                               lesser=True)
            with self.assertRaises(ValueError):
                returning_step(actor, receipt="dying", target_id="patient", recipient_hp=0,
                               recipient_max_hp=12, recipient_vigor=6, ap_available=20,
                               lesser=True)
            self.assertEqual(2, returning_step(actor, receipt="at-range", target_id="patient",
                 recipient_hp=5, recipient_max_hp=12, recipient_vigor=8,
                 ap_available=20, distance=3 if lv == 1 else 4).hp_restored)

    def test_intrusion_cost_and_destiny_ledger(self):
        a = Anointed(1, "High", "Restoration")
        resisted = returning_step(a, receipt="resist", target_id="patient",
            recipient_hp=5, recipient_max_hp=12, recipient_vigor=0,
            ap_available=20, lesser=True, intrusion_succeeded=False)
        self.assertEqual((0, 1, 20), (resisted.hp_restored, resisted.actor.destiny, resisted.ap_spent))
        with self.assertRaises(ValueError):
            returning_step(resisted.actor, receipt="resist", target_id="patient",
                recipient_hp=5, recipient_max_hp=12, recipient_vigor=0,
                ap_available=20, lesser=True)
        with self.assertRaises(ValueError):
            returning_step(a, receipt="illegal", target_id="patient",
                recipient_hp=5, recipient_max_hp=12, recipient_vigor=0,
                ap_available=20, lesser=True, beneficial_intrusion_legal=False)
        dormant = set_bond(a, active=False)
        with self.assertRaises(ValueError):
            returning_step(dormant, receipt="dormant", target_id="patient",
                recipient_hp=5, recipient_max_hp=12, recipient_vigor=3, ap_available=20)
        self.assertEqual(dormant, mission_event(dormant, "event", gm_recognized=True))

    def test_l3_guided_is_one_increment_not_an_extra_step(self):
        a = Anointed(3, "High", "Restoration")
        legal = dict(receipt="own-existing-g4-step", recipient_missing_hp_after_ordinary=2,
                     active_paid_guided_instance=True, mode="Maintained",
                     profile="Single Target", authenticated_regeneration_step=True,
                     guided_bonus_unsuppressed=True)
        x = guided_regeneration_l3(a, **legal)
        self.assertEqual((1, 1), (x.additional_hp_without_vigor, x.actor.destiny))
        for changed in ({"active_paid_guided_instance": False},
                        {"recipient_missing_hp_after_ordinary": 0},
                        {"authenticated_regeneration_step": False},
                        {"guided_bonus_unsuppressed": False},
                        {"recipient_dying": True}, {"profile": "Self"}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                guided_regeneration_l3(a, **(legal | changed))
        with self.assertRaises(ValueError):
            guided_regeneration_l3(Anointed(2, "High", "Restoration"), **legal)
        with self.assertRaises(ValueError):
            guided_regeneration_l3(x.actor, **legal)

    def test_single_aspect_no_fire_access_or_unapproved_grades(self):
        a = Anointed(3, "High", "Restoration")
        with self.assertRaises(ValueError):
            kindled_flame(a, receipt="borrow-fire", hit=True, target_vigor=8,
                          target_hp=8, ap_available=20)
        with self.assertRaises(ValueError):
            conjure_flame_l3(a, receipt="borrow-spell", profile="Thrown Projectile",
                             used_tier=1, hit=True, target_vigor_after_base=5,
                             adequate_spent_vp=True, authentic_paid_attack=True)
        self.assertEqual(["Basic Heal", "Guided Regeneration"], profile(3)["known_bonded_techniques"])

    def test_isolated_witnesses_and_documentation_are_not_native_claims(self):
        for lv in LEVELS:
            x = isolated_witness(lv)
            self.assertEqual((2, 2, 0, 1), (x["normal_hp"], x["lesser_hp"],
                              x["lesser_recipient_vigor"], x["lesser_destiny_left"]))
            self.assertFalse(x["native_event_receipts"])
            self.assertEqual(lv == 3, x["guided_l3"] is not None)
        doc = (ROOT / "docs/design/b04-b05-high-anointed-restoration-l1-l3-character-build-verification-v0.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs/design/veilbound-roadmap-and-mvp-readiness.md").read_text(encoding="utf-8")
        index = (ROOT / "docs/design/README.md").read_text(encoding="utf-8")
        for needle in ("28", "The Returning Step", "Spare the Reserve", "TAL-A01",
                       "0/12", "native", "Basic Heal", "Guided Regeneration"):
            self.assertIn(needle, doc)
        self.assertIn("**10/12**", roadmap)
        self.assertIn("**0/12**", roadmap)
        self.assertIn("b04-b05-high-anointed-restoration-l1-l3-character-build-verification-v0.md", index)


if __name__ == "__main__":
    unittest.main()
