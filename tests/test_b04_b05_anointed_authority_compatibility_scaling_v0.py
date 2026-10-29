"""Isolated candidate evidence, not native combat or canonical authorization."""
from pathlib import Path
import unittest

from scripts.b04_b05_anointed_authority_compatibility_scaling_v0 import (
    CANDIDATE_PROFILES, LEVELS, candidate_compatibility, conjure_authority_l3,
    guided_regeneration_authority_l3, kindled_vigor, scaling_comparison,
    scope_check, signature_vigor, single_grade, target_vigor_ceiling,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/design/b04-b05-anointed-authority-compatibility-signature-scaling-v0.md"


class AuthorityCompatibilityScalingTests(unittest.TestCase):
    def test_01_cross_level_baseline_and_grades(self):
        self.assertEqual((1, 1, 2, 3, 4, 5),
                         tuple(signature_vigor(x) for x in LEVELS))
        self.assertEqual((4, 4, 8, 12, 13, 14),
                         tuple(kindled_vigor(l, g) for l, g in zip(
                             LEVELS, ("lesser", "lesser", "greater", "supreme", "supreme", "supreme"))))
        for level in range(1, 21):
            self.assertGreaterEqual(signature_vigor(level), 1)
            self.assertEqual(1, signature_vigor(level, scaled=False))
        with self.assertRaises(ValueError):
            kindled_vigor(4, "greater")
        with self.assertRaises(ValueError):
            kindled_vigor(9, "supreme")
        with self.assertRaises(ValueError):
            signature_vigor(21)

    def test_02_one_grade_no_sovereign_same_authority_stack(self):
        self.assertEqual(1, single_grade(("lesser",), 3, 2))
        self.assertEqual(2, single_grade(("greater",), 5, 3))
        for levels in (("lesser", "lesser"), ("lesser", "greater"),
                       ("lesser", "supreme"), (), ("greater", "supreme")):
            with self.assertRaises(ValueError):
                single_grade(levels, 20, 6)
        with self.assertRaises(ValueError):
            single_grade(("greater",), 3, 2)
        with self.assertRaises(ValueError):
            single_grade(("lesser",), 3, 0)

    def test_03_exact_mode_allowlist_and_l3_gate(self):
        self.assertEqual(9, len(CANDIDATE_PROFILES))
        self.assertTrue(candidate_compatibility("High", "Conflagration", "Conjure Flame",
                                               "Thrown Projectile", "Primary", level=3))
        self.assertFalse(candidate_compatibility("High", "Conflagration", "Conjure Flame",
                                                "Thrown Projectile", "Primary", level=2))
        for focus in ("Medium", "Low"):
            self.assertTrue(candidate_compatibility(
                focus, "Conflagration", "Conjure Flame", "Weapon Enchantment", "Primary",
                level=3, weapon_wielded=True, vessel_matches=focus == "Medium"))
            self.assertFalse(candidate_compatibility(
                focus, "Conflagration", "Conjure Flame", "Weapon Enchantment", "Primary",
                level=3, weapon_wielded=False, vessel_matches=True))
        self.assertFalse(candidate_compatibility("High", "Restoration", "Basic Heal",
                                                "Single Target", "Primary", level=3))
        self.assertFalse(candidate_compatibility("High", "Conflagration", "Conjure Flame",
                                                "Ammunition Shot", "Primary", level=3))
        self.assertFalse(candidate_compatibility("High", "Conflagration", "Conjure Flame",
                                                "Thrown Projectile", "Primary", level=3,
                                                has_bond_access=False))
        self.assertFalse(candidate_compatibility("Medium", "Restoration", "Guided Regeneration",
                                                "Single Target", "Maintained", level=3))
        self.assertFalse(candidate_compatibility("Low", "Restoration", "Guided Regeneration",
                                                "Self", "Maintained", level=3))
        self.assertTrue(candidate_compatibility("Low", "Restoration", "Guided Regeneration",
                                               "Self", "Maintained", level=3, recipient_self=True))

    def test_04_high_thrown_source_pricing_and_l3_lesser(self):
        paid = conjure_authority_l3(focus="High", level=3, tier=2, destiny=2,
                                    receipt="attack-1", used_receipts=frozenset(),
                                    roll=8, vc=0, hit=True)
        self.assertEqual((2, 11, 4, 0, 1),
                         (paid.hp_packet, paid.vigor_packet, paid.spent_vp_this_attempt,
                          paid.required_existing_committed_vp, paid.spent_destiny))
        self.assertIn("attack-1", paid.used_receipts)
        with self.assertRaises(ValueError):
            conjure_authority_l3(focus="High", level=3, tier=2, destiny=1,
                                 receipt="attack-1", used_receipts=paid.used_receipts,
                                 roll=8, hit=True)
        with self.assertRaises(ValueError):
            conjure_authority_l3(focus="High", level=3, tier=3, destiny=2,
                                 receipt="attack-2", used_receipts=frozenset(),
                                 roll=8, hit=True)

    def test_05_reserved_hit_no_free_rider_or_refund(self):
        for focus in ("Medium", "Low"):
            kwargs = dict(focus=focus, level=3, tier=1, destiny=2,
                          receipt="hit-1", used_receipts=frozenset(),
                          roll=6, vc=0, hit=True, weapon_wielded=True,
                          vessel_matches=focus == "Medium")
            with self.assertRaises(ValueError):
                conjure_authority_l3(**kwargs)
            x = conjure_authority_l3(**kwargs, active_reserve=True, committed_vp=4)
            self.assertEqual((2, 6, 0, 4, 1),
                             (x.hp_packet, x.vigor_packet, x.spent_vp_this_attempt,
                              x.required_existing_committed_vp, x.spent_destiny))
            with self.assertRaises(ValueError):
                conjure_authority_l3(**{**kwargs, "used_receipts": x.used_receipts},
                                     active_reserve=True, committed_vp=4)
            miss = conjure_authority_l3(**{**kwargs, "hit": False, "receipt": "miss"},
                                        active_reserve=True, committed_vp=4)
            self.assertEqual((0, 0, 1), (miss.hp_packet, miss.vigor_packet, miss.spent_destiny))
            with self.assertRaises(ValueError):
                conjure_authority_l3(**kwargs, active_reserve=True, committed_vp=3)

    def test_06_guided_increment_waiver_consumes_only_natural_vigor(self):
        for focus in ("High", "Medium", "Low"):
            x = guided_regeneration_authority_l3(
                focus=focus, level=3, destiny=2, missing_hp=5,
                recipient_vigor=3, natural_throughput=2,
                receipt="step-1", used_receipts=frozenset(),
                vessel_matches=focus == "Medium", recipient_self=focus == "Low")
            self.assertEqual((2, 1, 2, 1, 3, 1),
                             (x.ordinary_hp, x.extra_guided_hp, x.spent_recipient_vigor,
                              x.remaining_vigor, x.healed_hp, x.spent_destiny))
            with self.assertRaises(ValueError):
                guided_regeneration_authority_l3(
                    focus=focus, level=3, destiny=2, missing_hp=5, recipient_vigor=3,
                    natural_throughput=2, receipt="step-1", used_receipts=x.used_receipts,
                    vessel_matches=focus == "Medium", recipient_self=focus == "Low")

    def test_07_guided_zero_vigor_and_no_loops_or_wound_bypass(self):
        common = dict(focus="High", level=3, destiny=2,
                      receipt="step-0", used_receipts=frozenset())
        z = guided_regeneration_authority_l3(**common, missing_hp=5,
                                              recipient_vigor=0, natural_throughput=2)
        self.assertEqual((0, 1, 0, 0, 1),
                         (z.ordinary_hp, z.extra_guided_hp, z.spent_recipient_vigor,
                          z.remaining_vigor, z.healed_hp))
        for override in ({"missing_hp": 0}, {"missing_hp": 1, "recipient_vigor": 10},
                         {"dying": True}, {"active_effect": False},
                         {"mode": "Nonexistent"}, {"destiny": 0}):
            values = {**common, "missing_hp": 5, "recipient_vigor": 5,
                      "natural_throughput": 2, **override}
            with self.assertRaises(ValueError):
                guided_regeneration_authority_l3(**values)

    def test_08_resource_ceiling_and_assumed_hit_rates(self):
        for level in LEVELS:
            for vigor in (0, 1, 4, 12, 36, 42):
                for grade in ("baseline", "lesser"):
                    value = target_vigor_ceiling(level, grade, vigor)
                    self.assertTrue(0 <= value <= vigor)
                    self.assertEqual(0, target_vigor_ceiling(level, grade, vigor, hit=False))
        for probability in (0, .65, 1):
            rows = scaling_comparison(probability)
            self.assertEqual(6, len(rows))
            for x in rows:
                self.assertAlmostEqual(probability * x["empowered_scaled"],
                                       x["candidate_expected_vigor"], places=5)
        with self.assertRaises(ValueError):
            scaling_comparison(1.2)

    def test_09_paid_technique_and_six_level_census(self):
        rows = scaling_comparison()
        self.assertEqual(LEVELS, tuple(x["level"] for x in rows))
        self.assertEqual((4, 4, 8, 12, 13, 14), tuple(x["empowered_scaled"] for x in rows))
        self.assertEqual((3.875, 5.375, 6.5, 9.875, 14.375, 15.5),
                         tuple(x["paid_vigor_mean_hit_vc0"] for x in rows))
        self.assertEqual([6, 6, 6], rows[-1]["focus_envelope"]["High"])
        self.assertEqual([1, 1, 1], rows[-1]["focus_envelope"]["Low"])
        self.assertEqual([1, 1, 1], rows[-1]["focus_envelope"]["Medium"])

    def test_10_source_and_scope(self):
        scope_check()
        doc = DOC.read_text(encoding="utf-8")
        for word in ("DESIGN ONLY", "Sovereign Projection", "one grade", "Conjure Flame",
                     "Guided Regeneration", "Restoration", "Conflagration", "L3",
                     "9/12", "0/12", "1 + floor(Level / 5)", "L20"):
            self.assertIn(word.lower(), doc.lower())
        self.assertIn(DOC.name, (ROOT / "docs/design/README.md").read_text(encoding="utf-8"))
        roadmap = (ROOT / "docs/design/veilbound-roadmap-and-mvp-readiness.md").read_text(encoding="utf-8")
        self.assertIn(DOC.name, roadmap)
        self.assertIn("**9/12**", roadmap)
        self.assertIn("**0/12**", roadmap)


if __name__ == "__main__":
    unittest.main()
