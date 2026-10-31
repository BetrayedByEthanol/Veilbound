"""Integrated MVP adventure: source lineage, milestone windows, untrusted intake."""
from copy import deepcopy
from unittest.mock import patch
import unittest

from scripts.b04_b05_b06_b07_integrated_pilot_adventure_v0 import (
    BEATS, MILESTONE_BEATS, SESSION_GROUPS, STATUS,
    blank_packet, plan, preflight,
)
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import FOCUS_TASKS


def reported_template(n=3):
    """Explicitly synthetic references for validation tests, NEVER human play."""
    p=blank_packet(n)
    p["report_author_ref"]="SYNTHETIC_TEST_NOT_A_HUMAN_AUTHOR"
    for index, session in enumerate(p["sessions"]):
        session["status"]="REPORTED"
        for key in ("session_id","played_at","gm_observation_ref",
                    "start_resource_state_ref","end_resource_state_ref",
                    "reviewed_level_sheet_ref","recovery_and_pursuit_decision_ref"):
            session[key]=f"SYNTHETIC_{key}_S{index+1}"
        session["player_choice_refs"]=[f"SYNTHETIC_chosen_{index+1}"]
        session["native_evidence_refs"]=[f"SYNTHETIC_source_log_{index+1}"]
        if index:
            session["incoming_handoff_ref"]=f"SYNTHETIC_handoff_{index+1}"
        for beat in session["beats"]:
            beat["status"]="REPORTED"
            beat["outcome"]="partial"
            for field in ("choice_ref","alternative_ref","gm_consequence_ref",
                          "world_clock_ref","resource_state_ref","source_action_ref"):
                beat[field]=f"SYNTHETIC_{field}_{beat['beat']}"
    for i,m in enumerate(p["milestones"]):
        m["status"]="REPORTED"
        m["actual_event_id"]=f"SYNTHETIC_UNVERIFIED_GM_GROUP_BEAT_{i+1}"
        m["gm_declaration_ref"]=f"SYNTHETIC_GM_REF_{i+1}"
        m["reviewed_level_sheet_ref"]=f"SYNTHETIC_GM_SHEET_{i+1}"
    return p


class IntegratedPilotAdventureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plans={n:plan(n) for n in SESSION_GROUPS}
        cls.blank={n:blank_packet(n) for n in SESSION_GROUPS}

    def test_01_five_beats_each_fits_l1_l2_l3_and_three_to_five_sessions(self):
        expected={
            3: ([1,2,3], [["supply","gate"],["forest","shrine"],["village"]], [1,2]),
            4: ([1,2,2,3], [["supply","gate"],["forest"],["shrine"],["village"]], [1,3]),
            5: ([1,1,2,2,3], [["supply"],["gate"],["forest"],["shrine"],["village"]], [2,4]),
        }
        for n,p in self.plans.items():
            with self.subTest(sessions=n):
                levels,beats,after=expected[n]
                self.assertEqual([x["target_start_level"] for x in p["sessions"]],levels)
                self.assertEqual([x["beats"] for x in p["sessions"]],beats)
                self.assertEqual([m["after_session_number"] for m in
                                  p["milestone_candidates"]],after)
                self.assertEqual(p["unobserved_human_sessions"],n)
                self.assertEqual(p["status"],STATUS)
                self.assertEqual(len(p["source_roster"]),12)
                self.assertEqual(p["supported_spotlight_slots"],36)

    def test_02_all_live_sources_source_fingerprinted_and_focus_slots_unique(self):
        for n,p in self.plans.items():
            self.assertEqual({x["pairing"] for x in p["source_roster"]},
                             set(FOCUS_TASKS))
            for x in p["source_roster"]:
                self.assertTrue(x["source_fingerprints"])
                for path,digest in x["source_fingerprints"].items():
                    self.assertTrue(path.startswith(("scripts/","docs/")))
                    self.assertEqual(len(digest),64)
            slots=self.blank[n]["focus_level_evidence"]
            self.assertEqual(len(slots),36)
            self.assertEqual(len({(x["pairing"],x["level"]) for x in slots}),36)
            self.assertTrue(all(x["status"]=="UNOBSERVED" for x in slots))

    def test_03_existing_native_scene_anchors_never_claim_l1_g8_combat(self):
        self.assertEqual(set(BEATS),{"supply","gate","forest","shrine","village"})
        self.assertEqual(tuple(BEATS[x]["level"] for x in
                               ("supply","gate","forest","shrine","village")),
                         (1,1,2,2,3))
        self.assertIn("L2/L3 only",BEATS["gate"]["mechanical_scope"])
        self.assertIn("nonhostile",BEATS["gate"]["mechanical_scope"])
        for b in BEATS.values():
            self.assertTrue(b["native_anchor"].startswith("scripts/"))
            self.assertGreaterEqual(len(b["routes"]),3)
            self.assertTrue(b["failure_forward"])
            self.assertTrue(b["gm_open_questions"])
        self.assertEqual([m["from_level"] for m in MILESTONE_BEATS],[1,2])
        self.assertEqual([m["to_level"] for m in MILESTONE_BEATS],[2,3])

    def test_04_blank_intake_preflight_is_unverified_with_no_real_awards(self):
        for n,template in self.blank.items():
            with self.subTest(n=n):
                r=preflight(template)
                self.assertTrue(r["candidate_references_well_formed"])
                for k in ("reported_session_references",
                          "reported_milestone_references",
                          "reported_focus_level_references",
                          "externally_authenticated_gm_sessions",
                          "independently_verified_milestones",
                          "independently_full_certified_focuses",
                          "strict_mvp_exits_met"):
                    self.assertEqual(r[k],0)
                self.assertEqual(r["status"],STATUS)
                self.assertEqual(template["human_sessions_certified"],0)

    def test_05_synthetic_refs_can_be_wellformed_but_never_certified(self):
        p=reported_template(3)
        for slot in p["focus_level_evidence"][:3]:
            slot["status"]="REPORTED"
            for k in ("sheet_ref","combat_choice_ref","noncombat_choice_ref",
                      "alternative_ref","countercase_ref","independent_review_ref"):
                slot[k]=f"SYNTHETIC_{k}_{slot['pairing']}_{slot['level']}"
        r=preflight(p)
        self.assertEqual(r["reported_session_references"],3)
        self.assertEqual(r["reported_milestone_references"],2)
        self.assertEqual(r["reported_focus_level_references"],3)
        self.assertEqual(r["externally_authenticated_gm_sessions"],0)
        self.assertEqual(r["independently_verified_milestones"],0)
        self.assertEqual(r["independently_full_certified_focuses"],0)
        self.assertEqual(r["strict_mvp_exits_met"],0)

    def test_06_level_two_play_cannot_be_reported_without_real_milestone_reference(self):
        p=reported_template(3)
        p["milestones"][0]=deepcopy(self.blank[3]["milestones"][0])
        with self.assertRaisesRegex(ValueError,"milestone"):
            preflight(p)

    def test_07_reused_or_out_of_order_milestones_rejected(self):
        for key,value in (("actual_event_id","SYNTHETIC_UNVERIFIED_GM_GROUP_BEAT_1"),
                          ("after_session_number",1),
                          ("from_level",1),("to_level",2)):
            p=reported_template()
            p["milestones"][1][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                preflight(p)
        p=reported_template()
        p["milestones"][0]["status"]="UNDECLARED"
        with self.assertRaises(ValueError):
            preflight(p)

    def test_08_skipped_session_or_forged_play_status_is_rejected(self):
        p=reported_template()
        p["sessions"][0]=deepcopy(self.blank[3]["sessions"][0])
        with self.assertRaises(ValueError):
            preflight(p)
        p=reported_template()
        p["sessions"][1]["status"]="UNOBSERVED"
        with self.assertRaises(ValueError):
            preflight(p)
        p=reported_template()
        p["sessions"][1]["incoming_handoff_ref"]=""
        with self.assertRaises(ValueError):
            preflight(p)

    def test_09_negative_beat_consequence_and_claimed_forged_outcome(self):
        p=reported_template()
        p["sessions"][0]["beats"][0]["gm_consequence_ref"]=""
        with self.assertRaises(ValueError):
            preflight(p)
        p=reported_template()
        p["sessions"][0]["beats"][0]["outcome"]="guaranteed_free_level"
        with self.assertRaises(ValueError):
            preflight(p)
        p=reported_template()
        p["sessions"][0]["beats"][1]["status"]="UNOBSERVED"
        with self.assertRaises(ValueError):
            preflight(p)

    def test_10_falsified_source_hash_plan_or_certification_flags_fail(self):
        for tamper in ("source","digest","certified","extra","roster_order"):
            p=deepcopy(self.blank[4])
            if tamper=="source":
                p["source_roster"][0]["source_fingerprints"]["scripts/fake.py"]="0"*64
            elif tamper=="digest":
                p["plan_digest"]="0"*64
            elif tamper=="certified":
                p["strict_mvp_exits_met"]=6
            elif tamper=="extra":
                p["real_gm_said_ok"]=True
            else:
                p["source_roster"]=list(reversed(p["source_roster"]))
            with self.subTest(tamper=tamper),self.assertRaises(ValueError):
                preflight(p)

    def test_11_focus_coverage_cannot_be_duplicated_or_claimed_without_sessions(self):
        p=deepcopy(self.blank[4])
        p["focus_level_evidence"][1]=deepcopy(p["focus_level_evidence"][0])
        with self.assertRaises(ValueError):
            preflight(p)
        p=deepcopy(self.blank[4])
        slot=p["focus_level_evidence"][0]
        slot["status"]="REPORTED"
        for k in ("sheet_ref","combat_choice_ref","noncombat_choice_ref",
                  "alternative_ref","countercase_ref","independent_review_ref"):
            slot[k]="untrusted_only"
        with self.assertRaises(ValueError):
            preflight(p)

    def test_12_invalid_session_counts_and_mutable_plan_arbitrary_attributes(self):
        for n in (2,6,True,3.0,"4",None):
            with self.subTest(n=str(n)),self.assertRaises(ValueError):
                plan(n)
        p=deepcopy(self.blank[3])
        p["sessions"][0]["target_start_level"]=3
        with self.assertRaises(ValueError):
            preflight(p)

    def test_13_no_combat_fixture_is_a_pilot_session_or_real_CR(self):
        for p in self.plans.values():
            self.assertEqual(p["human_session_certifications"],0)
            self.assertEqual(p["independently_full_certified_focuses"],0)
            self.assertEqual(p["strict_mvp_exits_met"],0)
            self.assertIn("not sourced",p["source_combat_L1_gap"])
            for m in p["milestone_candidates"]:
                self.assertTrue(m["gm_declaration_required"])
                self.assertFalse(m["automatically_awarded"])
                self.assertNotIn("xp_awarded",m)
                self.assertNotIn("destiny_awarded",m)


if __name__=="__main__":
    unittest.main()
