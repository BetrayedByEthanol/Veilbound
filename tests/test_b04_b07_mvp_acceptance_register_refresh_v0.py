"""Regression guards for the live B04/B07 MVP acceptance register.

This is a planning and canonical-technique inventory check, NOT a Focus
certificate or a claim to have witnessed a real GM/player session.
"""
from pathlib import Path
import re
import unittest

from scripts.b04_b07_independent_progression_audit_v0 import (
    SOURCE_MODULES, authored_scholar_techniques,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs/design"
MAGIC = ROOT / "docs/rules/07-veil-magic"

# Complete individually authored Pillar/Aspect Tier-1 registry as of #182.
INDIVIDUAL_T1 = {
    "Conjure Flame": ("Fire", "Conflagration", "conjure-flame-v0.md"),
    "Basic Heal": ("Life", "Restoration", "basic-heal-v0.md"),
    "Guided Regeneration": ("Life", "Restoration",
                            "guided-regeneration-v0.md"),
    "Gentle Growth": ("Life", "Nature", "gentle-growth-v0.md"),
    "Woodland Rapport": ("Life", "Nature", "woodland-rapport-v0.md"),
    "Vital Shelter": ("Life", "Preservation", "vital-shelter-v0.md"),
    "Venom Endurance": ("Life", "Preservation", "venom-endurance-v0.md"),
    "Stone Skin": ("Earth", "Fortification", "stone-skin-v0.md"),
    "Weaken Restraints": ("Liberty", "Defiance",
                          "weaken-restraints-v0.md"),
    "Minor Telekinesis": ("Mind", "Psionics", "minor-telekinesis-v0.md"),
    "Protective Ward": ("Kinship", "Guardian", "protective-ward-v0.md"),
    "Phantom Sound": ("Secrets", "Hallucination", "phantom-sound-v0.md"),
    "Spark of Inspiration": ("Arts", "Inspiration",
                             "spark-of-inspiration-v0.md"),
}
# Separate procedures, core math, Focus modes, Universals and capabilities
# must NOT be counted as individual Tier-1 Pillar techniques.
NON_INDIVIDUAL = {
    "blink-v0.md", "elemental-damage-resistance-v0.md",
    "high-gifted-amplification-and-miscasts-v0.md",
    "life-exaltation-properties-v0.md", "manifestation-resolution.md",
    "medium-gifted-ward-conduit-v0.md", "metaphysical-foundation.md",
    "resonance-and-intrusion.md",
    "scholar-inward-embodiment-profiles-v0.md",
    "technique-structure-v0.md", "technique-tiers-and-expression.md",
    "universal-veil-fundamentals.md", "veil-inspection-v0.md",
    "veil-translocation-foundation.md", "volition-points.md",
}


class MvpAcceptanceRegisterRefreshTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roadmap = (DESIGN / "veilbound-roadmap-and-mvp-readiness.md"
                       ).read_text(encoding="utf-8")
        cls.acceptance = (
            DESIGN / "b04-b07-mvp-acceptance-register-refresh-v0.md"
        ).read_text(encoding="utf-8")
        cls.approvals = (
            DESIGN / "b04-b05-b07-mvp-pilot-approvals-and-watches-v0.md"
        ).read_text(encoding="utf-8")

    def test_01_source_census_rechecks_all_individual_technique_pages(self):
        source_files = {p.name for p in MAGIC.glob("*.md")}
        individually_authored = {t[2] for t in INDIVIDUAL_T1.values()}
        self.assertFalse(individually_authored & NON_INDIVIDUAL)
        # A new page triggers an explicit source-census decision instead of
        # keeping the 13/10 label after catalogue changes.
        self.assertEqual(source_files, individually_authored | NON_INDIVIDUAL)
        registered = authored_scholar_techniques()
        self.assertEqual(set(registered), set(INDIVIDUAL_T1))
        self.assertEqual(len(registered), 13)
        for name, (pillar, aspect, filename) in INDIVIDUAL_T1.items():
            with self.subTest(technique=name):
                rule = (MAGIC / filename).read_text(encoding="utf-8")
                self.assertTrue(rule.startswith("# " + name + " v0"))
                self.assertIn(pillar + " / " + aspect, rule)
                self.assertEqual(registered[name]["pillar"], pillar)
                self.assertEqual(registered[name]["aspect"], aspect)
                self.assertEqual(registered[name]["base_tier"], 1)
        aspects = {(p, a) for p, a, _ in INDIVIDUAL_T1.values()}
        self.assertEqual((13, 10, 8), (
            len(INDIVIDUAL_T1), len(aspects),
            len({p for p, _ in aspects})))

    def test_02_six_exit_gates_remain_open_without_double_counting(self):
        table = self.roadmap.split(
            "## Level 1–3 tabletop MVP — objective and six exit requirements"
        )[1].split("### B01–B07 MVP blocker register")[0]
        self.assertEqual(6, sum(line.startswith("| [ ] **")
                                for line in table.splitlines()))
        for name in ("Create", "Act", "Resolve", "Advance",
                     "Challenge", "Observe"):
            self.assertIn("**" + name, table)
            self.assertIn("**" + name, self.acceptance)
        for marker in ("12/12", "0/12", "0/6", "3/7", "G0–G8"):
            self.assertIn(marker, self.roadmap)
            self.assertIn(marker, self.acceptance)
        self.assertIn("39", self.roadmap)
        self.assertIn("39", self.acceptance)
        self.assertIn("13 variants", self.roadmap)
        self.assertIn("13 variants", self.acceptance)
        self.assertIn("SOURCE_MODULES", "SOURCE_MODULES")  # source-backed input
        self.assertEqual(11, len(SOURCE_MODULES))  # 12th is Low Priest A/B
        self.assertIn("0/12 independently", self.acceptance)

    def test_03_original_blocker_identity_and_no_new_b06_stage(self):
        table = self.roadmap.split(
            "### B01–B07 MVP blocker register"
        )[1].split("## Next MVP work — after merged PR #182")[0]
        self.assertEqual([f"B0{i}" for i in range(1, 8)],
                         re.findall(r"^\| \*\*(B0[1-7])\*\*",
                                    table, flags=re.MULTILINE))
        self.assertEqual(3, table.count("**CLOSED"))
        self.assertEqual(4, table.count("**PARTIAL") +
                         table.count("**G0–G8 bounded"))
        self.assertIn("No new B06 G-stage", self.acceptance)
        self.assertNotIn("G9 implementation milestone", self.roadmap)

    def test_04_merged_deliveries_and_approved_decisions_are_current(self):
        for marker in ("merged **#180**", "**#181**", "**#182**",
                       "Rooted Guard", "Unbound Step"):
            self.assertIn(marker, self.roadmap)
        for marker in ("#180", "#181", "#182",
                       "13", "10 of 24", "14", "watch",
                       "two GM-declared", "0/12", "0/6"):
            self.assertIn(marker.lower(), self.approvals.lower())
        self.assertIn("native source binding merged **#180**",
                      self.approvals)
        self.assertNotIn("Implementation gate still open — not native",
                         self.approvals)
        self.assertNotIn("this corrective branch proposes",
                         self.roadmap)
        self.assertNotIn("reconciliation in review", self.roadmap)

    def test_05_all_acceptance_artifacts_and_source_links_exist(self):
        related = (
            "veilbound-roadmap-and-mvp-readiness.md",
            "b04-b07-independent-l1-l3-build-progression-audit-v0.md",
            "b04-b07-mvp-acceptance-register-refresh-v0.md",
            "b04-b05-b07-mvp-pilot-approvals-and-watches-v0.md",
            "b04-b05-anointed-field-pilot-evidence-v0.md",
            "b04-b05-mvp-pilot-roster-gifted-anointed-readiness-v0.md",
        )
        for name in related:
            with self.subTest(document=name):
                self.assertTrue((DESIGN / name).is_file())
        self.assertTrue((DESIGN / "README.md").is_file())
        self.assertIn("b04-b07-mvp-acceptance-register-refresh-v0.md",
                      (DESIGN / "README.md").read_text(encoding="utf-8"))

    def test_06_pr_changes_to_register_trigger_independent_ci(self):
        flow = (ROOT / ".github/workflows/b04-b07-independent-progression-audit.yml"
                ).read_text(encoding="utf-8")
        for source in (
            "docs/design/veilbound-roadmap-and-mvp-readiness.md",
            "docs/design/b04-b07-mvp-acceptance-register-refresh-v0.md",
            "docs/design/b04-b05-b07-mvp-pilot-approvals-and-watches-v0.md",
            "docs/design/README.md",
            "tests/test_b04_b07_mvp_acceptance_register_refresh_v0.py",
        ):
            self.assertIn("'" + source + "'", flow)


if __name__ == "__main__":
    unittest.main()
