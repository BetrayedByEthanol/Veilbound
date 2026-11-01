"""Alpha real-table handoff: audit source gaps, no fake acceptance or play."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.b04_b05_b06_b07_alpha_pilot_handoff_v0 import (
    handoff, _sources, _stages, _triage, ROOT, VERSION,
    MECHANICAL_SOURCES, CAPABILITIES, LEGACY_GAP_REASSESSMENT,
)
from scripts.b04_b05_b06_b07_first_cohort_pilot_v0 import (
    blank_packet, validate, SOURCE_GAPS,
)
from scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 import (
    GATES, COHORTS,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class AlphaGMExecutionHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet=blank_packet()
        cls.report=handoff()

    def test_01_sources_are_current_real_bytes_not_opaque_assertions(self):
        r=self.report
        self.assertEqual(r["version"],VERSION)
        self.assertEqual(set(r["source_files"]),set(MECHANICAL_SOURCES))
        for kind,entry in r["source_files"].items():
            self.assertEqual(entry["path"],MECHANICAL_SOURCES[kind])
            self.assertTrue((ROOT/entry["path"]).is_file())
            self.assertEqual(entry["sha256"],sha256(
                (ROOT/entry["path"]).read_bytes()).hexdigest())
        self.assertEqual(r["source_snapshot_sha256"],
                         canonical_digest(r["source_files"]))

    def test_02_no_global_gameplay_capability_claimed_from_bounded_proofs(self):
        r=self.report
        byid={x["id"]:x for x in r["native_reference_scope"]}
        self.assertEqual(set(byid),{c[0] for c in CAPABILITIES})
        self.assertEqual(byid["alpha_L1_mixed"]["state"],"BOUNDED_SOURCE_LEGAL")
        self.assertEqual(byid["alpha_L1_tactical"]["state"],"BOUNDED_SOURCE_LEGAL")
        self.assertEqual(byid["alpha_L1_L3_progression"]["state"],"AUTHOR_CANDIDATE_ONLY")
        self.assertEqual(byid["alpha_L2_venom_sentry"]["state"],"BOUNDED_SOURCE_LEGAL")
        self.assertEqual(r["automatic_mixed_party_gameplay"],
                         "NO_GO_UNSUPPORTED_PLAYER_CHOICES")
        self.assertTrue(r["source_legal_alternatives_require_human_choice"])

    def test_03_five_real_story_beats_order_and_levels_not_forced_sessions(self):
        stages=self.report["scene_handoff"]
        self.assertEqual([x["beat"] for x in stages],
                         ["supply","gate","forest","shrine","village"])
        self.assertEqual([x["target_level"] for x in stages],[1,1,2,2,3])
        self.assertTrue(all(x["automatically_playable"] is False
                            and x["human_scene_observed"] is False
                            for x in stages))
        self.assertEqual(_stages(),stages)

    def test_04_legacy_source_gaps_remain_frozen_and_reassessed_separately(self):
        before=deepcopy(SOURCE_GAPS)
        r=handoff()
        self.assertEqual(tuple(SOURCE_GAPS),tuple(before))
        self.assertEqual(r["legacy_packet_source_gaps_preserved"],len(before))
        self.assertEqual(len(r["legacy_gap_reassessment"]),
                         len(LEGACY_GAP_REASSESSMENT))
        self.assertIn("PARTIALLY_ADDRESSED",
                      {x["state"] for x in r["legacy_gap_reassessment"]})
        self.assertIn("UNSUPPORTED_UNTIL_ADJUDICATED",
                      {x["state"] for x in r["legacy_gap_reassessment"]})

    def test_05_eight_dependencies_distinguish_gm_external_and_implementation(self):
        entries=self.report["prerequisite_register"]
        self.assertEqual(len(entries),8)
        self.assertEqual(len({x["id"] for x in entries}),8)
        self.assertEqual(entries,_triage())
        owners={x["dependency"]:x["owner_class"] for x in entries}
        self.assertEqual(owners["ARBITRARY_MIXED_ALPHA_COMBAT"],
                         "CONDITIONAL_IMPLEMENTATION")
        self.assertEqual(owners["L2_L3_REAL_MILESTONES"],
                         "EXTERNAL_GM_EVIDENCE")
        self.assertEqual(owners["GM_SCENE_FACTS_AND_TACTICAL_POLICY"],
                         "GM_PREPLAY")
        self.assertEqual(owners["ADVANCEMENT_RESOURCE_POLICY"],
                         "GM_AND_SOURCE_REVIEW")

    def test_06_original_blank_packet_preserved_eighty_four_unobserved_rows(self):
        packet=deepcopy(self.packet)
        before=canonical_digest(packet)
        actual=handoff(packet)
        self.assertEqual(canonical_digest(packet),before)
        self.assertEqual(len(packet["review_queue"]),84)
        self.assertTrue(all(x["status"]=="UNOBSERVED"
                            for x in packet["review_queue"]))
        self.assertEqual(
            actual["original_intake_shape_preflight"]["candidate_review_submissions"],0)
        self.assertEqual(
            actual["original_intake_shape_preflight"]["candidate_sessions_reported"],0)
        self.assertEqual(actual["source_intake_version"],packet["version"])
        self.assertTrue(actual["pilot_packet_unmodified_by_audit"])

    def test_07_a_variant_choice_is_not_an_approved_sheet_or_session(self):
        p=deepcopy(self.packet)
        p["characters"][0]["selected_variant"]="B"
        validated=handoff(p)
        self.assertTrue(validated["selected_character_preflight"][0]["variant_declared"])
        self.assertEqual(validated["selected_character_preflight"][0]["level_sheet_selected"],
                         [False,False,False])
        self.assertEqual(validated["original_player_pilot_sessions_verified"],0)
        self.assertEqual(validated["external_gm_milestones_authenticated"],0)
        self.assertEqual(validated["independent_full_focus_certificates"],0)
        self.assertEqual(validated["strict_mvp_exits_met"],0)

    def test_08_invalid_source_or_acceptance_payload_fails_closed(self):
        for change in ("digest","source_gap","certification","queue"):
            p=deepcopy(self.packet)
            if change=="digest":
                p["source_roster_digest"]="0"*64
            elif change=="source_gap":
                p["scenario_gaps"]=[]
            elif change=="certification":
                p["independently_certified_focuses"]=1
            else:
                p["review_queue"].pop()
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    handoff(p)

    def test_09_cannot_claim_external_file_integrity_without_primary_bytes(self):
        with self.assertRaises(ValueError):
            handoff(evidence_root="/tmp/nonexistent")
        with TemporaryDirectory() as path:
            checked=handoff(deepcopy(self.packet),evidence_root=path)
            self.assertTrue(checked["original_intake_shape_preflight"][
                "evidence_bytes_sha256_checked"])
            self.assertEqual(checked["evidence_files_listed"]
                             if "evidence_files_listed" in checked else
                             checked["original_intake_shape_preflight"]["evidence_files_listed"],0)

    def test_10_all_gates_stay_open_and_beta_gamma_are_not_credited(self):
        r=self.report
        self.assertEqual({x["gate"] for x in r["independent_gate_register"]},
                         {g[0] for g in GATES})
        self.assertTrue(all(x["status"]=="OPEN"
                            and x["automatically_accepted"] is False
                            for x in r["independent_gate_register"]))
        self.assertEqual(r["structural_focus_pairings"],12)
        self.assertEqual(r["original_mvp_blockers_closed"],3)
        self.assertEqual(r["independent_full_focus_certificates"],0)
        self.assertEqual(r["strict_mvp_exits_met"],0)
        self.assertTrue(r["full_twelve_focus_cohort_execution_not_complete"])
        self.assertEqual(len(COHORTS),3)
        self.assertEqual(r["table_execution_decision"],
                         "CONDITIONAL_GO_ONLY_AFTER_GM_SOURCE_AND_SAFETY_REVIEW")
        self.assertEqual(r["level_up_with_live_unsupported_effects"],
                         "NO_GO_UNTIL_SOURCE_LEGAL_RESOLUTION")
        self.assertEqual(r["independent_certification_decision"],
                         "NO_GO_UNTIL_AUTHENTIC_HUMAN_REVIEW")

    def test_11_handoff_is_deterministic_and_non_private(self):
        r=handoff()
        self.assertEqual(r,self.report)
        encoded=json.dumps(r,sort_keys=True)
        self.assertNotIn("GM-TEST",encoded)
        self.assertNotIn("PLAYER-TEST",encoded)
        self.assertNotIn("actual_person_name",encoded)
        self.assertIn("private",r["privacy"].lower())
        self.assertEqual(len(r["selected_character_preflight"]),4)


if __name__=="__main__":
    unittest.main()
