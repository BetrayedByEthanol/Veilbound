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
        # Derive structural progress from the roadmap's authoritative
        # four-archetype × three-Focus grid, not a frozen #138-era 4/12.
        # A newly merged source build may increase this number without
        # certifying its combat/noncombat Focus or changing blocker IDs.
        focus_rows = [line for line in text.splitlines()
                      if any(line.startswith("| **" + name + "** |")
                             for name in ("Priest", "Scholar", "Gifted",
                                          "Anointed"))]
        self.assertEqual(len(focus_rows), 4)
        cells = [cell.strip() for line in focus_rows
                 for cell in line.split("|")[2:5]]
        self.assertEqual(len(cells), 12)
        # Both fully native and source-verified structural-only builds
        # count as structural pairings, but not as independent MVP
        # certification. Do not silently exclude non-native High Gifted.
        delivered = sum(cell.startswith("**Structural") for cell in cells)
        status_row = next(line for line in text.splitlines()
                          if line.startswith("| Structural L1→3 Focus pairings |"))
        self.assertIn("**%d/12**" % delivered, status_row)
        self.assertIn("**0/12**", text)
        self.assertIn("**3/7**", text)
        # Preserve the original B06 milestone taxonomy even when new
        # native work is delivered inside existing G1/G5 components.
        b06_section = text.split("## B06 fixed milestone register", 1)[1].split(
            "## Level 1–3 tabletop MVP", 1)[0]
        self.assertEqual(9, sum(line.startswith("| **G")
                                for line in b06_section.splitlines()))
        for token in ("[formal assessment #137]", "PR #148", "G8",
                      "b04-b05-eight-combat-playstyles-evaluation-framework-v0.md"):
            self.assertIn(token, text)

    def test_index_links_protocol(self):
        self.assertIn("b04-b05-eight-combat-playstyles-evaluation-framework-v0.md",
                      INDEX.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
