"""Source-backed pilot-roster inventory/readiness tests (not character certification)."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
TECHNIQUES = ROOT / "docs/rules/07-veil-magic"
SELECTION = ROOT / "docs/design/b05-eight-pillar-mvp-selection-and-coverage.md"
AUDIT = ROOT / "docs/design/b04-b05-archetype-access-and-starting-repertoire-audit.md"
DOC = ROOT / "docs/design/b04-b05-mvp-pilot-roster-gifted-anointed-readiness-v0.md"
INDEX = ROOT / "docs/design/README.md"
ROADMAP = ROOT / "docs/design/veilbound-roadmap-and-mvp-readiness.md"
IDENTITY = re.compile(r"^# (?P<name>.+?) v0 [—-] (?P<pillar>[A-Za-z]+) / (?P<aspect>[A-Za-z ]+)$")
ROSTER = re.compile(r"^\\| \\*\\*(\\w+)\\*\\* \\| (\\w+) \\| (\\w+) \\| (\\w+) \\|")
EMOTIONS = ("Joy", "Sadness", "Anger", "Fear", "Surprise", "Disgust", "Trust", "Anticipation")


def source_techniques():
    """Count named, individually authored source identities, never shared engines/modes."""
    inventory = {}
    for path in TECHNIQUES.glob("*.md"):
        heading = path.read_text(encoding="utf-8").splitlines()[0]
        match = IDENTITY.fullmatch(heading)
        if match:
            inventory[match.group("name")] = (
                match.group("pillar"), match.group("aspect").strip(), path.name
            )
    return inventory


def selected_roster():
    text = SELECTION.read_text(encoding="utf-8")
    section = text.split("## Selected roster —", 1)[1].split("### Capability coverage", 1)[0]
    rows = {}
    for line in section.splitlines():
        match = ROSTER.match(line)
        if match:
            rows[match.group(1)] = set(match.groups()[1:])
    return rows


class MvpPilotRosterReadinessTests(unittest.TestCase):
    def test_fresh_scoped_source_census(self):
        inventory = source_techniques()
        roster = selected_roster()
        self.assertEqual(8, len(roster))
        self.assertEqual(24, sum(map(len, roster.values())))
        self.assertEqual(13, len(inventory))
        authored = {(pillar, aspect) for pillar, aspect, _ in inventory.values()}
        expected = {(pillar, aspect) for pillar, aspects in roster.items()
                    for aspect in aspects}
        self.assertTrue(authored <= expected)
        self.assertEqual(10, len(authored))
        self.assertEqual(14, len(expected - authored))
        doc = DOC.read_text(encoding="utf-8")
        # Every actual named base-T1 source identity must have a grounded link.
        for name, (_, _, filename) in inventory.items():
            self.assertIn(f"[{name}](../rules/07-veil-magic/{filename})", doc)
        for literal in ("**13**", "**10 of the selected 24**", "**14/24",
                        "**10/24 covered; 14 missing**"):
            self.assertIn(literal, doc)

    def test_gifted_eight_authored_links_are_legal_not_new_permission(self):
        inventory = source_techniques()
        available = {(pillar, aspect) for pillar, aspect, _ in inventory.values()}
        doc = DOC.read_text(encoding="utf-8")
        section = doc.split("### Gifted pilot candidate —", 1)[1].split(
            "## Six unfinished Focus implementation contracts", 1
        )[0]
        found = {}
        for line in section.splitlines():
            parts = [part.strip() for part in line.split("|")]
            if len(parts) == 6 and parts[1] in EMOTIONS:
                emotion, aspect, rating = parts[1], parts[2], parts[3]
                self.assertIn(rating, {"S", "P"})
                pillar, aspect_name = (piece.strip() for piece in aspect.split("/", 1))
                self.assertIn((pillar, aspect_name), available)
                self.assertNotIn(emotion, found)
                found[emotion] = (pillar, aspect_name, rating)
        self.assertEqual(set(EMOTIONS), set(found))
        self.assertEqual(8, len({pillar for pillar, _, _ in found.values()}))
        self.assertEqual(6, sum(rate == "S" for _, _, rate in found.values()))
        self.assertEqual(2, sum(rate == "P" for _, _, rate in found.values()))
        # The historically verified 6S/2P values, not the all-Strong Insight sample.
        old = AUDIT.read_text(encoding="utf-8")
        for emotion, (pillar, aspect, rating) in found.items():
            self.assertIn(f"| {emotion} | **{pillar} / {aspect}** | **{rating}** |", old)
        self.assertNotIn(("Mind", "Insight"), available)

    def test_all_six_gaps_and_no_false_certification(self):
        doc = DOC.read_text(encoding="utf-8")
        for name in ("High Gifted (A08)", "Medium Gifted (A09)",
                     "Low Gifted (A10)", "High Anointed (A11/A12)",
                     "Medium Anointed (A11/A12)", "Low Anointed (A11/A12)"):
            self.assertIn(name, doc)
        for concept in ("**NEEDS CONTENT DESIGN / APPROVAL**",
                        "0-VP Signature", "ordinary conditional technique access",
                        "not yet executable for all twelve", "B04, B05, B06 or B07"):
            self.assertIn(concept.lower(), doc.lower())
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertEqual(6, sum(line.startswith("| [ ] **")
                                for line in roadmap.splitlines()))
        self.assertIn("**6/12**", roadmap)
        self.assertIn("**0/12**", roadmap)
        self.assertIn(DOC.name, INDEX.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
