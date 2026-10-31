"""B04/B05 source-derived canonical noncombat scenes: no invented GM authority."""
from copy import deepcopy
from unittest.mock import patch
import unittest

from scripts.b04_b05_noncombat_scene_resolution_v0 import (
    DIFFICULTY, DOMAIN_POLICIES, NO_CERTIFICATION, ROLES,
    SCENES, SOURCE_ONLY, _character, _sources, matrix, resolve_scene,
)
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import roster


class NoncombatSceneResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all = matrix()
        cls.by = {
            (r["pairing"], r["level"], r["domain"], r["policy"]): r
            for r in cls.all["rows"]
        }

    def case(self, pairing, level, domain, policy):
        return self.by[pairing, level, domain, policy]

    def test_01_12_focus_36_level_slots_three_domains_two_approaches(self):
        self.assertEqual(set(ROLES), {r["pairing"] for r in roster()})
        self.assertEqual((12, 36, 216), (
            self.all["focus_pairings"], self.all["pairing_level_slots"],
            self.all["mechanically_resolved_fixed_fixtures"]))
        self.assertEqual(len(self.all["rows"]), len(self.by))
        self.assertEqual(self.all["domains"], ["exploration", "investigation", "social"])
        for pairing in sorted(ROLES):
            for level in (1, 2, 3):
                for domain, approaches in DOMAIN_POLICIES.items():
                    for policy in approaches:
                        self.assertIn((pairing, level, domain, policy), self.by)
        self.assertEqual(self.all["low_priest_ability_only_fixtures"], 18)

    def test_02_native_source_receipts_and_real_elapsed_g42_seconds(self):
        for r in self.all["rows"]:
            with self.subTest(pairing=r["pairing"], level=r["level"],
                              domain=r["domain"], policy=r["policy"]):
                self.assertEqual(len(r["source_sha256"]), 64)
                self.assertEqual(len(r["native_ledger_sha256"]), 64)
                self.assertGreater(r["native_g42_event_count"], 0)
                self.assertEqual(r["elapsed_seconds"],
                                 SCENES[r["domain"]][r["policy"]]["time_seconds"])
                self.assertEqual(r["status"], SOURCE_ONLY)
                self.assertEqual(r["target"],
                                 DIFFICULTY[r["difficulty_modifier"]])
                self.assertEqual(r["total"], r["check_base"] +
                                 r["ability_modifier"] + r["trained_rank"] +
                                 r["situational_modifier"])
                self.assertEqual(r["success"], r["total"] >= r["target"])
                self.assertEqual(r["d20_face"], 12)

    def test_03_training_only_when_specific_authored_practice_applies(self):
        for r in self.all["rows"]:
            if r["training"] is not None:
                with self.subTest(r=r["pairing"], lvl=r["level"], task=r["policy"]):
                    self.assertIn(r["training"],
                                  ("Acrobatics", "Navigation", "Medicine",
                                   "regional/era History"))
                    self.assertGreater(r["trained_rank"], 0)
        hp = self.case("Priest/High", 1, "investigation", "diagnose")
        self.assertEqual((hp["ability"], hp["training"], hp["trained_rank"]),
                         ("Intellect", "Medicine", 2))
        untrained = self.case("Scholar/High", 1, "exploration", "survey")
        self.assertIsNone(untrained["training"])
        self.assertEqual(untrained["trained_rank"], 0)
        for pairing in ROLES:
            for level in (1, 2, 3):
                direct = self.case(pairing, level, "social", "petition")
                self.assertEqual((direct["ability"], direct["training"],
                                  direct["trained_rank"]), ("Presence", None, 0))
                factual = self.case(pairing, level, "social", "document")
                self.assertEqual(factual["ability"], "Intellect")
                self.assertNotIn(factual["training"],
                                 ("Disguise", "Emotional Discipline",
                                  "Negotiation", "Oratory", "Command"))

    def test_04_low_priest_a_b_are_source_proxies_without_trainings(self):
        for level in (1, 2, 3):
            a = resolve_scene("Priest/Low", level, "investigation", "diagnose",
                              low_variant="A")
            b = resolve_scene("Priest/Low", level, "investigation", "diagnose",
                              low_variant="B")
            for row in (a, b):
                self.assertEqual(row["source_scope"], "LOW_PRIEST_G0_ABILITIES_ONLY")
                self.assertIsNone(row["training"])
                self.assertEqual(row["trained_rank"], 0)
                self.assertFalse(row["independent_focus_certified"])
            self.assertNotEqual(a["ability_modifier"], b["ability_modifier"])
        self.assertEqual(self.all["full_low_priest_noncombat_certificates"], 0)

    def test_05_roll_natural_one_twenty_have_no_special_noncombat_rule(self):
        low = resolve_scene("Priest/High", 1, "exploration", "balance", face=1)
        high = resolve_scene("Priest/High", 1, "exploration", "balance", face=20)
        self.assertEqual((low["d20_face"], low["success"]), (1, False))
        self.assertEqual((high["d20_face"], high["success"]), (20, True))
        # Even a natural 20 is not an unconditional success against an
        # explicitly poorer situational premise: the arithmetic decides.
        extreme = resolve_scene("Priest/High", 1, "exploration", "balance",
                                face=20, situational_modifier=-10)
        self.assertEqual(extreme["total"], extreme["target"])
        self.assertTrue(extreme["success"])
        # High-numbered d20 under a legitimate harder check still may fail.
        failed = resolve_scene("Priest/High", 1, "exploration", "survey",
                               face=20, situational_modifier=-10)
        self.assertFalse(failed["success"])

    def test_06_safe_effort_passive_take10_take20_exact_canonical_base(self):
        opts = ("passive", "take10", "take20", "safe_roll")
        for mode in opts:
            result = resolve_scene(
                "Scholar/Medium", 2, "investigation", "observe",
                mode=mode, face=(14 if mode == "safe_roll" else None))
            expected = {"passive": 10, "take10": 10,
                        "take20": 20, "safe_roll": 14}[mode]
            self.assertEqual(result["check_base"], expected)
            self.assertEqual(result["elapsed_seconds"],
                             0 if mode == "passive" else 900 if mode == "take20" else 90)
        with self.assertRaises(ValueError):
            resolve_scene("Scholar/Medium", 2, "social", "petition",
                          mode="take20", face=None)
        with self.assertRaises(ValueError):
            resolve_scene("Scholar/Medium", 2, "social", "petition",
                          mode="passive", face=None)
        with self.assertRaises(ValueError):
            resolve_scene("Scholar/Medium", 2, "exploration", "balance",
                          mode="take20", face=None)
        with self.assertRaises(ValueError):
            resolve_scene("Scholar/Medium", 2, "investigation", "diagnose",
                          mode="take10", face=None)
        incidental = resolve_scene("Scholar/Medium", 2, "exploration", "survey",
                                   mode="passive", face=None)
        self.assertEqual(incidental["elapsed_seconds"], 0)

    def test_07_consequence_and_approach_change_without_free_bonuses(self):
        a = resolve_scene("Priest/High", 1, "exploration", "balance", face=8)
        b = resolve_scene("Priest/High", 1, "exploration", "survey", face=8)
        self.assertEqual((a["ability"], a["training"]), ("Agility", "Acrobatics"))
        self.assertEqual(b["ability"], "Awareness")
        self.assertNotEqual((a["target"], a["elapsed_seconds"]),
                            (b["target"], b["elapsed_seconds"]))
        self.assertEqual(a["consequence"],
                         SCENES["exploration"]["balance"]["failure"])
        success = resolve_scene("Priest/High", 1, "exploration", "balance",
                                face=14)
        self.assertEqual(success["consequence"],
                         SCENES["exploration"]["balance"]["success"])
        self.assertNotEqual(success["consequence"], a["consequence"])

    def test_08_unsupported_or_malformed_modes_fail_before_any_native_pay(self):
        bad_cases = (
            ("Priest/High", 1, "stealth", "balance", 12, "pressure", None, 0),
            ("Priest/High", 1, "exploration", "fly", 12, "pressure", None, 0),
            ("Priest/High", 4, "exploration", "balance", 12, "pressure", None, 0),
            ("Priest/High", True, "exploration", "balance", 12, "pressure", None, 0),
            ([], 1, "exploration", "balance", 12, "pressure", None, 0),
            ("Priest/High", 1, "exploration", "balance", 0, "pressure", None, 0),
            ("Priest/High", 1, "exploration", "balance", 21, "pressure", None, 0),
            ("Priest/High", 1, "exploration", "balance", True, "pressure", None, 0),
            ("Priest/High", 1, "exploration", "balance", None, "pressure", None, 0),
            ("Priest/High", 1, "exploration", "balance", 12, "take10", None, 0),
            ("Priest/High", 1, "exploration", "balance", None, "bogus", None, 0),
            ("Priest/High", 1, "exploration", "balance", 12, "pressure", None, 12),
            ("Priest/High", 1, "exploration", "balance", 12, "pressure", "A", 0),
            ("Priest/Low", 1, "exploration", "balance", 12, "pressure", None, 0),
            ("Priest/Low", 1, "exploration", "balance", 12, "pressure", "C", 0),
        )
        for i, (p,l,d,a,f,m,v,s) in enumerate(bad_cases):
            with self.subTest(case=i):
                with self.assertRaises(ValueError):
                    resolve_scene(p,l,d,a,face=f,mode=m,
                                  low_variant=v,situational_modifier=s)

    def test_09_structural_source_tampering_rejected_including_missing_training(self):
        ref = _sources()
        row = deepcopy(ref)
        row["Priest/High"]["source_fingerprints"] = {"not/a/real/file.py": "0"*64}
        with patch("scripts.b04_b05_noncombat_scene_resolution_v0._sources",
                   return_value=row):
            with self.assertRaises(ValueError):
                resolve_scene("Priest/High", 1, "investigation", "diagnose")
        modified = deepcopy(ref)
        modified["Scholar/Low"]["source_issues"].append({"issue": "fake"})
        with patch("scripts.b04_b05_noncombat_scene_resolution_v0._sources",
                   return_value=modified):
            with self.assertRaises(ValueError):
                resolve_scene("Scholar/Low", 1, "social", "petition")

    def test_10_fixture_outcomes_never_claim_gm_or_focus_certification(self):
        for r in self.all["rows"]:
            self.assertFalse(r["external_gm_adjudicated"])
            self.assertFalse(r["human_choice_observed"])
            self.assertFalse(r["independent_focus_certified"])
            self.assertEqual(r["strict_mvp_exits_met"], 0)
            self.assertNotIn("combat_damage", r)
            self.assertNotIn("xp_awarded", r)
            self.assertNotIn("destiny", r)
        for flag, expected in NO_CERTIFICATION.items():
            self.assertEqual(self.all[flag], expected)

    def test_11_cross_scene_replay_digest_reproducible_from_source(self):
        expected = self.case("Anointed/Medium", 3, "social", "petition")
        reproduced = resolve_scene("Anointed/Medium", 3, "social", "petition")
        self.assertEqual(reproduced["native_ledger_sha256"],
                         expected["native_ledger_sha256"])
        self.assertEqual(reproduced["source_sha256"], expected["source_sha256"])
        self.assertEqual(reproduced["elapsed_seconds"], 60)


if __name__ == "__main__":
    unittest.main()
