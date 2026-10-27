"""Review-only assertions for the proposed Anointed Restoration Signature baseline.

This file checks design/document consistency and candidate conservation arithmetic.
It does not adjudicate native actions, approve numeric rules, or certify a Focus.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/design/b04-b05-anointed-restoration-birth-mission-signature-baseline-v0.md"
INDEX = ROOT / "docs/design/README.md"
RULE = ROOT / "docs/rules/08-archetypes/anointed.md"
HP = ROOT / "docs/rules/06-vigor-wounds-death/hp-and-vigor.md"


def pulse(hp, max_hp, vigor, cap, authority=False):
    """Isolated numeric candidate, deliberately not a runtime feature."""
    if hp <= 0 or hp >= max_hp:
        return None
    if not (0 <= vigor and 0 < cap and hp <= max_hp):
        raise ValueError("invalid state")
    restored = min(cap, max_hp - hp, vigor if not authority else max_hp - hp)
    return hp + restored, vigor if authority else vigor - restored


class AnointedRestorationSignatureDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.canon = RULE.read_text(encoding="utf-8")

    def test_01_design_only_and_index(self):
        self.assertIn("NOT an executable rule", self.doc)
        self.assertIn(DOC.name, INDEX.read_text(encoding="utf-8"))
        self.assertIn("9/12 structural", self.doc)
        self.assertIn("0/12 independently certified", self.doc)

    def test_02_positive_surge_mission_and_imprint(self):
        for phrase in ("The Returning Steps", "The Returning Step",
                       "extraordinary public celebration", "collective",
                       "Life / Restoration", "Make recovery possible where injury",
                       "not a Pillar-issued order", "not required"):
            self.assertIn(phrase.lower(), self.doc.lower())
        self.assertIn("Conflicted", self.canon)
        self.assertIn("Forsaken", self.canon)

    def test_03_one_signature_three_action_patterns(self):
        for phrase in ("one Signature", "High — Project", "Medium — Invest",
                       "Low — Embody", "20 AP", "24 AP",
                       "Regeneration Step", "once per", "0 VP"):
            self.assertIn(phrase.lower(), self.doc.lower())
        self.assertIn("**0 VP** baseline", self.canon)

    def test_04_conserves_vigor_normal_pulse(self):
        for hp, vigor, cap in ((5, 20, 2), (5, 1, 2), (5, 0, 2),
                               (11, 5, 2), (3, 24, 1)):
            new_hp, new_vigor = pulse(hp, 12, vigor, cap)
            self.assertEqual(new_hp + new_vigor, hp + vigor)
            self.assertTrue(0 <= new_vigor <= vigor)
            self.assertTrue(hp <= new_hp <= 12)
            self.assertLessEqual(new_hp - hp, cap)
        self.assertIn("restoring 1 HP consumes 1 Vigor", HP.read_text(encoding="utf-8"))

    def test_05_fighter_followup_step(self):
        healed_hp, healed_vigor = pulse(5, 12, 20, 2)
        self.assertEqual((7, 18), (healed_hp, healed_vigor))
        regen = min(3, 12 - healed_hp, healed_vigor)
        self.assertEqual((10, 15), (healed_hp + regen, healed_vigor - regen))

    def test_06_authority_cost_is_a_distinct_exception(self):
        self.assertEqual((7, 20), pulse(5, 12, 20, 2, authority=True))
        self.assertEqual((7, 0), pulse(5, 12, 0, 2, authority=True))
        for phrase in ("1 Destiny", "no new action", "Spare the Reserve",
                       "not automatically compatible"):
            self.assertIn(phrase.lower(), self.doc.lower())

    def test_07_refusals_and_dying(self):
        self.assertIsNone(pulse(0, 12, 10, 2))
        self.assertIsNone(pulse(-1, 12, 10, 2, authority=True))
        self.assertIsNone(pulse(12, 12, 10, 2, authority=True))
        for phrase in ("+8 barrier", "zero direct Vigor",
                       "Repair Progress", "unobstructed", "no pulse"):
            self.assertIn(phrase.lower(), self.doc.lower())

    def test_08_no_unearned_implementation(self):
        for phrase in ("not an extra natural Regeneration Step",
                       "no extra regeneration step",
                       "medium/low event-driven pulses",
                       "out-of-initiative recovery clock",
                       "zero completed Anointed L1–3 sheets"):
            self.assertIn(phrase.lower(), self.doc.lower())


if __name__ == "__main__":
    unittest.main()
