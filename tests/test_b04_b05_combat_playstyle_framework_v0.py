"""Static consistency gates for the B04/B05 role framework (not combat certification)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/design/b04-b05-eight-combat-playstyles-evaluation-framework-v0.md"
ROADMAP = ROOT / "docs/design/veilbound-roadmap-and-mvp-readiness.md"
INDEX = ROOT / "docs/design/README.md"
ROLES = ("Fighter", "Defender", "Spellblade", "Assassin", "Archer",
         "Combat Caster", "Battlemage", "Healer / Support")

class CombatPlaystyleFrameworkTests(unittest.TestCase):
    def test_exactly_eight_role_rows_and_scenarios(self):
        text = DOC.read_text(encoding="utf-8")
        for role in ROLES:
            self.assertEqual(1, sum(line.startswith("| **" + role + "** |")
                for line in text.splitlines()), role)
        for case in range(1, 9):
            self.assertIn("**PS-%02d**" % case, text)
        self.assertIn("not canonical game rules", text)
        self.assertIn("15–20%", text)
        self.assertIn("changes no B01–B07 blocker status", text)

    def test_roadmap_remains_uncertified(self):
        text = ROADMAP.read_text(encoding="utf-8")
        self.assertEqual(6, sum(line.startswith("| [ ] **") for line in text.splitlines()))
        for n in range(1, 8):
            self.assertEqual(1, sum(line.startswith("| **B%02d**" % n)
                for line in text.splitlines()))
        for token in ("**4/12**", "**0/12**", "**3/7**", "PR #137", "G8",
                      "b04-b05-eight-combat-playstyles-evaluation-framework-v0.md"):
            self.assertIn(token, text)

    def test_index_links_protocol(self):
        self.assertIn("b04-b05-eight-combat-playstyles-evaluation-framework-v0.md",
                      INDEX.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
