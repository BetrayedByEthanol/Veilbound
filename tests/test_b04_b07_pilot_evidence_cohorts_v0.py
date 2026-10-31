"""Independent fail-closed milestone chronology and multi-cohort intake tests."""
from copy import deepcopy
import unittest

from scripts.b04_b07_pilot_evidence_cohorts_v0 import (
    BEAT_ORDER, VERSION, STATUS, blank_packet, preflight,
)


def scene(sid, beat, level):
    return {"scene_id": sid, "beat": beat, "level": level, "outcome": "partial",
            **{k: f"SYNTHETIC-{sid}-{k}" for k in (
                "choice_ref", "alternative_ref", "gm_consequence_ref",
                "source_action_ref", "resource_before_ref", "resource_after_ref", "world_clock_ref")}}


def reported(cohort="C1", pairings=("Priest/High", "Scholar/Low"), award_after=("supply", "forest")):
    """Entirely fabricated references; never play or certification evidence."""
    packet = blank_packet(cohort, pairings)
    c = packet["cohorts"][0]
    c["gm_ref"] = f"SYNTHETIC-GM-{cohort}"
    c["report_author_ref"] = f"SYNTHETIC-AUTHOR-{cohort}"
    for actor in c["characters"]:
        actor["player_ref"] = f"SYNTHETIC-PLAYER-{cohort}-{actor['character_id']}"
    current_level = 1
    # Each beat is its own session (5 sessions); awards may happen after any beat.
    for i, beat in enumerate(BEAT_ORDER):
        sid = f"{cohort}-S{i+1}"
        before = f"{cohort}-state-{i}"
        after = f"{cohort}-state-{i+1}"
        c["sessions"].append({
            "session_id": sid, "played_at": f"SYNTHETIC-DAY-{i+1}",
            "incoming_handoff_ref": "" if i == 0 else before,
            "start_resource_state_ref": before,
            "end_resource_state_ref": after, "inter_session_transition_ref": "",
            "scenes": [scene(f"{cohort}-{beat}", beat, current_level)]})
        if beat in award_after:
            event_no = len(c["milestones"]) + 1
            c["milestones"].append({
                "event_id": f"{cohort}-GM-AWARD-{event_no}",
                "after_scene_id": f"{cohort}-{beat}",
                "from_level": event_no, "to_level": event_no+1,
                "gm_declaration_ref": f"SYNTHETIC-GM-DECLARATION-{cohort}-{event_no}",
                "story_achievement_ref": f"SYNTHETIC-STORY-{cohort}-{event_no}",
                "reviewed_sheets": [
                    {"character_id": actor["character_id"],
                     "sheet_ref": f"SYNTHETIC-LEVEL-SHEET-{cohort}-{event_no}-{actor['character_id']}",
                     "reviewer_ref": f"SYNTHETIC-REVIEWER-{cohort}-{event_no}-{actor['character_id']}"}
                    for actor in c["characters"]]})
            current_level += 1
    for actor in c["characters"]:
        for level in (1, 2, 3):
            possible = [s for session in c["sessions"] for s in session["scenes"]
                        if s["level"] == level]
            if not possible:
                continue
            c["focus_level_evidence"].append({
                "character_id": actor["character_id"], "level": level,
                "sheet_ref": f"SYNTHETIC-SHEET-{cohort}-{level}",
                "combat_scene_id": possible[0]["scene_id"],
                "combat_choice_ref": f"SYNTHETIC-COMBAT-{cohort}-{level}",
                "noncombat_scene_id": possible[0]["scene_id"],
                "noncombat_choice_ref": f"SYNTHETIC-NONCOMBAT-{cohort}-{level}",
                "alternative_ref": f"SYNTHETIC-ALTERNATIVE-{cohort}-{level}",
                "countercase_scene_id": possible[0]["scene_id"],
                "countercase_ref": f"SYNTHETIC-COUNTERCASE-{cohort}-{level}",
                "reviewer_ref": f"SYNTHETIC-REVIEW-{cohort}-{level}"})
    return packet


class CohortEvidenceTests(unittest.TestCase):
    def test_blank_packet_no_awards_or_certificates(self):
        packet = blank_packet("C1", ("Priest/High",))
        out = preflight(packet)
        self.assertEqual(out["candidate_unique_focus_level_slots"], 0)
        self.assertEqual(out["reported_milestone_references"], 0)
        self.assertEqual(out["strict_mvp_exits_met"], 0)
        self.assertEqual(packet["version"], VERSION)
        self.assertEqual(out["status"], STATUS)

    def test_actual_milestone_windows_can_move_to_different_beats(self):
        # L2 after supply, L3 after forest (not fixed road-gate / shrine).
        p = reported()
        out = preflight(p)
        self.assertEqual(out["reported_milestone_references"], 2)
        self.assertEqual(out["candidate_unique_focus_level_slots"], 6)
        self.assertEqual(out["externally_authenticated_gm_sessions"], 0)
        self.assertEqual(out["independently_full_certified_focuses"], 0)

    def test_delayed_milestones_and_unadvanced_sessions_allowed(self):
        # Delayed L2 at shrine, no L3; final village stays L2.
        p = reported(award_after=("shrine",))
        preflight(p)
        c = p["cohorts"][0]
        self.assertEqual([s["scenes"][0]["level"] for s in c["sessions"]], [1,1,1,1,2])
        self.assertEqual(len(c["milestones"]), 1)

    def test_cohorts_can_have_same_pairing_without_doubling_unique_coverage(self):
        p = reported("C1")
        q = reported("C2", ("Priest/High",))
        p["cohorts"].extend(q["cohorts"])
        summary = preflight(p)
        self.assertEqual(summary["reported_cohorts"], 2)
        self.assertEqual(summary["reported_session_references"], 10)
        self.assertEqual(summary["candidate_unique_focus_level_slots"], 6)
        priest = next(r for r in summary["candidate_focus_level_slots"]
                      if r["pairing"] == "Priest/High" and r["level"] == 2)
        self.assertEqual({r["cohort_id"] for r in priest["participants"]}, {"C1", "C2"})

    def test_no_foreign_or_duplicate_ids(self):
        for tamper in ("cohort", "session", "scene", "award"):
            p = reported("C1")
            q = reported("C2", ("Gifted/High",))
            p["cohorts"].extend(q["cohorts"])
            other = p["cohorts"][1]
            if tamper == "cohort":
                other["cohort_id"] = "C1"
            elif tamper == "session":
                other["sessions"][0]["session_id"] = "C1-S1"
            elif tamper == "scene":
                other["sessions"][0]["scenes"][0]["scene_id"] = "C1-supply"
            else:
                other["milestones"][0]["event_id"] = "C1-GM-AWARD-1"
            with self.subTest(tamper=tamper), self.assertRaises(ValueError):
                preflight(p)

    def test_no_gm_award_without_real_scene_or_complete_sheets(self):
        for tamper in ("foreign_scene", "duplicate_scene", "missing_sheet", "level_skipping", "out_of_order"):
            p = reported()
            c = p["cohorts"][0]
            if tamper == "foreign_scene":
                c["milestones"][0]["after_scene_id"] = "SOME-OTHER-COHORT-SCENE"
            elif tamper == "duplicate_scene":
                c["milestones"][1]["after_scene_id"] = c["milestones"][0]["after_scene_id"]
            elif tamper == "missing_sheet":
                c["milestones"][0]["reviewed_sheets"].pop()
            elif tamper == "level_skipping":
                c["milestones"][0]["to_level"] = 3
            else:
                c["milestones"].reverse()
            with self.subTest(tamper=tamper), self.assertRaises(ValueError):
                preflight(p)

    def test_wrong_level_before_or_after_milestone_rejected(self):
        for beat, level in (("supply",2), ("gate",1), ("village",2)):
            p = reported()
            scene_row = next(s for session in p["cohorts"][0]["sessions"]
                             for s in session["scenes"] if s["beat"] == beat)
            scene_row["level"] = level
            with self.subTest(beat=beat), self.assertRaises(ValueError):
                preflight(p)

    def test_cross_cohort_evidence_cannot_borrow_scene(self):
        p = reported()
        p["cohorts"][0]["focus_level_evidence"][0]["combat_scene_id"] = "C2-supply"
        with self.assertRaises(ValueError):
            preflight(p)

    def test_modified_source_and_certification_claims_rejected(self):
        for tamper in ("digest", "source", "flag", "unexpected"):
            p = reported()
            if tamper == "digest":
                p["source_roster_digest"] = "bad"
            elif tamper == "source":
                p["cohorts"][0]["characters"][0]["source_fingerprints"] = {}
            elif tamper == "flag":
                p["strict_mvp_exits_met"] = 6
            else:
                p["externally_verified_by_script"] = True
            with self.subTest(tamper=tamper), self.assertRaises(ValueError):
                preflight(p)

    def test_resource_handoffs_and_paid_inter_session_changes(self):
        p = reported()
        c = p["cohorts"][0]
        c["sessions"][1]["start_resource_state_ref"] = "SYNTHETIC-UPDATED-STATE"
        with self.assertRaises(ValueError):
            preflight(p)
        c["sessions"][1]["inter_session_transition_ref"] = "SYNTHETIC-SOURCE-TIMELINE"
        preflight(p)
        c["sessions"][1]["incoming_handoff_ref"] = "WRONG"
        with self.assertRaises(ValueError):
            preflight(p)

    def test_higher_level_evidence_requires_real_scene_at_exact_level(self):
        p = reported(award_after=("shrine",))
        c = p["cohorts"][0]
        c["focus_level_evidence"][0]["level"] = 3
        with self.assertRaises(ValueError):
            preflight(p)
        p = reported()
        c = p["cohorts"][0]
        c["focus_level_evidence"][0]["noncombat_scene_id"] = "C1-forest"
        with self.assertRaises(ValueError):
            preflight(p)

    def test_no_twelve_player_party_or_duplicate_pc_identity(self):
        with self.assertRaises(ValueError):
            blank_packet("C1", list(("Priest/High",))*6)
        p = reported()
        p["cohorts"][0]["characters"][1]["character_id"] = "PC-1"
        with self.assertRaises(ValueError):
            preflight(p)


if __name__ == "__main__":
    unittest.main()
