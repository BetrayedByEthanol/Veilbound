"""B04/B07 twelve-Focus roster contract, not externally certified play."""
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.b04_b07_independent_progression_audit_v0 import (
    SOURCE_MODULES, audit,
)
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import (
    CANDIDATE_STATUS, FOCUS_TASKS, LEVELS, LEVEL_EVIDENCE, SOURCE_STATUS,
    blank_packet, preflight, roster,
)


class TwelveFocusProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roster = roster()
        cls.source_report = audit()

    @staticmethod
    def illustrative_candidate(pairing="Anointed/High"):
        """Synthetic reference strings ONLY to exercise the preflight."""
        packet = blank_packet(pairing)
        packet["report_author_ref"] = "sample-supplied-author"
        packet["independent_reviewer_ref"] = "sample-supplied-reviewer"
        packet["external_review_ref"] = "sample-supplied-review-file"
        for item in packet["levels"]:
            for key in LEVEL_EVIDENCE:
                item[key] = "UNVERIFIED-SAMPLE-%s-%s" % (item["level"], key)
        for item in packet["milestones"]:
            item["event_id"] = "SAMPLE-EVENT-%s" % item["to_level"]
            item["gm_declared_event_ref"] = "UNVERIFIED-GM-%s" % item["to_level"]
            item["reviewed_level_sheet_ref"] = "UNVERIFIED-SHEET-%s" % item["to_level"]
        return packet

    def test_01_exact_twelve_pairings_thirteen_variants_and_36_level_slots(self):
        self.assertEqual(len(self.roster), 12)
        self.assertEqual({x["pairing"] for x in self.roster},
                         set(self.source_report["pairings"]))
        self.assertEqual(set(FOCUS_TASKS), set(self.source_report["pairings"]))
        self.assertEqual(sum(x["structural_variants"] for x in self.roster), 13)
        self.assertEqual(sum(len(x["levels"]) for x in self.roster), 36)
        self.assertEqual((self.source_report["variants_checked"],
                          self.source_report["level_snapshots_checked"]), (13, 39))
        self.assertEqual({x.split("/")[0] for x in FOCUS_TASKS},
                         {"Priest", "Scholar", "Gifted", "Anointed"})
        self.assertEqual({x.split("/")[1] for x in FOCUS_TASKS},
                         {"Low", "Medium", "High"})
        self.assertEqual(len(SOURCE_MODULES), 11)

    def test_02_fingerprints_match_independent_actual_source_records(self):
        for row in self.roster:
            with self.subTest(pairing=row["pairing"]):
                pair = self.source_report["pairings"][row["pairing"]]
                expected = {pair["source"]: pair["source_sha256"]}
                if row["pairing"] == "Priest/Low":
                    expected[pair["build_record"]] = pair["build_record_sha256"]
                    self.assertEqual(row["structural_variants"], 2)
                else:
                    self.assertEqual(row["structural_variants"], 1)
                self.assertEqual(row["source_fingerprints"], expected)
                for path in expected:
                    self.assertTrue(Path(path).parts[0] in ("scripts", "docs"))
                    self.assertTrue((Path(__file__).resolve().parents[1] / path).is_file())
                self.assertEqual(row["source_issues"], pair["issues"])
                self.assertEqual(row["source_status"], SOURCE_STATUS)
                self.assertFalse(row["independently_full_certified"])

    def test_03_each_focus_has_distinct_combat_noncombat_and_countercase(self):
        for row in self.roster:
            with self.subTest(pairing=row["pairing"]):
                for field in ("identity", "combat_requirement",
                              "noncombat_requirement", "countercase_requirement"):
                    self.assertGreater(len(row[field]), 20)
                self.assertEqual(row["levels"], list(LEVELS))
        self.assertIn("Sword", FOCUS_TASKS["Anointed/Low"]["combat"])
        self.assertIn("Open Prayer", FOCUS_TASKS["Priest/High"]["combat"])
        self.assertIn("native Opportunity", FOCUS_TASKS["Scholar/Medium"]["combat"])

    def test_04_blank_packet_has_no_forged_sessions_or_certification(self):
        for row in self.roster:
            packet = blank_packet(row["pairing"])
            self.assertEqual(packet["source_fingerprints"],
                             row["source_fingerprints"])
            self.assertEqual([x["level"] for x in packet["levels"]], [1, 2, 3])
            self.assertEqual(len(packet["milestones"]), 2)
            self.assertTrue(all(not x[k] for x in packet["levels"]
                                for k in LEVEL_EVIDENCE))
            self.assertEqual(packet["status"], CANDIDATE_STATUS)
            self.assertFalse(packet["independently_full_certified"])
            self.assertEqual(packet["strict_mvp_exits_met"], 0)
            with self.assertRaises(ValueError):
                preflight(packet)
        with self.assertRaises(ValueError):
            blank_packet("Priest/Unrecognized")

    def test_05_populated_reference_fields_remain_unverified(self):
        for pairing in ("Priest/Low", "Gifted/Medium", "Anointed/High"):
            with self.subTest(pairing=pairing):
                result = preflight(self.illustrative_candidate(pairing))
                self.assertTrue(result["candidate_references_complete"])
                self.assertTrue(result["source_identity_matches"])
                self.assertEqual(result["externally_verified_sessions"], 0)
                self.assertFalse(result["independently_full_certified"])
                self.assertEqual(result["strict_mvp_exits_met"], 0)
                self.assertEqual(result["status"], CANDIDATE_STATUS)

    def test_06_forged_fingerprint_identity_and_certification_flags_rejected(self):
        good = self.illustrative_candidate()
        source = next(iter(good["source_fingerprints"]))
        for key, forged in (
            ("version", "unknown"),
            ("pairing", "Priest/High"),
            ("status", "CERTIFIED"),
            ("independently_full_certified", True),
            ("strict_mvp_exits_met", 1),
            ("source_fingerprints", {source: "0"*64}),
        ):
            with self.subTest(key=key):
                bad = deepcopy(good)
                bad[key] = forged
                with self.assertRaises(ValueError):
                    preflight(bad)
        for malformed_pairing in ([], {}, None, True):
            bad = deepcopy(good)
            bad["pairing"] = malformed_pairing
            with self.assertRaises(ValueError):
                preflight(bad)
        for key in ("full_focus_certified", "mvp_accepted",
                    "authenticated_gm", "independently_certified"):
            bad = deepcopy(good)
            bad[key] = True
            with self.assertRaises(ValueError):
                preflight(bad)

    def test_07_unearned_or_incomplete_level_references_rejected(self):
        good = self.illustrative_candidate()
        mutations = (
            lambda x: x["levels"].pop(),
            lambda x: x["levels"].reverse(),
            lambda x: x["levels"][0].update({"level": True}),
            lambda x: x["levels"][1].update({"level": 3}),
            lambda x: x["levels"][0].update({"combat_countercase_ref": ""}),
            lambda x: x["levels"][2].update({"noncombat_chosen_action_ref": None}),
            lambda x: x["levels"][1].update({"unsupported_spell": "yes"}),
        )
        for index, change in enumerate(mutations):
            with self.subTest(case=index):
                bad = deepcopy(good)
                change(bad)
                with self.assertRaises(ValueError):
                    preflight(bad)

    def test_08_milestone_order_id_and_gm_reference_are_not_automatic(self):
        good = self.illustrative_candidate()
        mutations = (
            lambda x: x["milestones"].pop(),
            lambda x: x["milestones"].reverse(),
            lambda x: x["milestones"][0].update({"to_level": 3}),
            lambda x: x["milestones"][1].update({"from_level": True}),
            lambda x: x["milestones"][1].update(
                {"event_id": x["milestones"][0]["event_id"]}),
            lambda x: x["milestones"][0].update({"gm_declared_event_ref": ""}),
            lambda x: x["milestones"][1].update({"xp": 100}),
        )
        for index, change in enumerate(mutations):
            with self.subTest(case=index):
                bad = deepcopy(good)
                change(bad)
                with self.assertRaises(ValueError):
                    preflight(bad)
        bad = deepcopy(good)
        bad["independent_reviewer_ref"] = bad["report_author_ref"]
        with self.assertRaises(ValueError):
            preflight(bad)

    def test_09_roster_and_templates_do_not_mutate_source_inventory(self):
        original = roster()
        changed = roster()
        changed[0]["source_fingerprints"]["forged"] = "f"*64
        changed[0]["source_issues"].append({"code": "fake"})
        self.assertEqual(original, roster())
        first = blank_packet("Priest/Low")
        first["source_fingerprints"]["forged"] = "f"*64
        self.assertNotIn("forged", blank_packet("Priest/Low")["source_fingerprints"])


if __name__ == "__main__":
    unittest.main()
