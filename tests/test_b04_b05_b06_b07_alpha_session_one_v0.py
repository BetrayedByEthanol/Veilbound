"""Session-one source GM cards, private worksheet and immutable intake boundaries."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.b04_b05_b06_b07_alpha_session_one_v0 import (
    brief,blank_worksheet,validate_worksheet,
    VERSION,STAGES,STAGE_FIELDS,GM_PREP_FIELDS,ROOT,
)
from scripts.b04_b05_b06_b07_first_cohort_pilot_v0 import (
    blank_packet as alpha_blank,validate as alpha_validate,
)
from scripts.b04_b05_b06_b07_alpha_pilot_handoff_v0 import handoff
from scripts.b04_b05_b06_alpha_l1_tactics_v0 import OPTIONS
from scripts.b05_b06_integrated_noncombat_adventure_v0 import DETOUR_SECONDS
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def selected(sheet):
    """Synthetic strings for schema tests ONLY, never participants or play."""
    p=deepcopy(sheet)
    for k in GM_PREP_FIELDS:
        p["gm_prep"][k]="synthetic:fixture:"+k
    for i,c in enumerate(p["characters"],1):
        c["selected_variant"]="A" if i==1 else "default"
        c["l1_selected_sheet_ref"]=f"synthetic:sheet:{i}:L1"
        c["player_ref"]=f"synthetic:player:{i}"
        c["starting_resources_ref"]=f"synthetic:resource:{i}"
    return p


def source_report(sheet,stage):
    row=next(x for x in sheet["stages"] if x["stage"]==stage)
    row["status"]="SOURCE_REPORTED"
    for k in STAGE_FIELDS[3:]:
        if k!="unsupported_action_ref":
            row[k]="synthetic:"+stage+":"+k
    return row


class AlphaSessionOneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.brief=brief()
        cls.blank=blank_worksheet()

    def test_01_matches_canonical_four_roster_and_real_source_hashes(self):
        b=self.brief
        p=alpha_blank()
        self.assertEqual(b["version"],VERSION)
        self.assertEqual(b["source_roster_digest"],p["source_roster_digest"])
        self.assertEqual(self.blank["source_roster_digest"],p["source_roster_digest"])
        self.assertEqual([x["pairing"] for x in self.blank["characters"]],
                         [x["pairing"] for x in p["characters"]])
        self.assertEqual([x["character_id"] for x in self.blank["characters"]],
                         ["PC-1","PC-2","PC-3","PC-4"])
        for key,value in b["mechanical_source_sha256"].items():
            path=handoff()["source_files"][key]["path"]
            self.assertEqual(value,sha256((ROOT/path).read_bytes()).hexdigest())

    def test_02_one_level_one_session_supply_gate_no_forced_advancement(self):
        b=self.brief
        self.assertEqual(b["session_number"],1)
        self.assertEqual(b["target_level"],1)
        self.assertEqual(b["beats"],["supply","gate"])
        self.assertEqual(self.blank["beats"],["supply","gate"])
        self.assertEqual([x["stage"] for x in b["gm_cards"]],list(STAGES))
        self.assertEqual([x["beat"] for x in b["gm_cards"]],
                         ["supply","supply","gate","gate"])
        self.assertEqual(self.blank["milestone_one"]["status"],"NOT_DECLARED")
        self.assertEqual(self.blank["level"],1)
        self.assertEqual(self.blank["session_number"],1)

    def test_03_noncombat_DC_and_time_author_example_never_free_cure(self):
        cards={x["stage"]:x for x in self.brief["gm_cards"]}
        self.assertEqual(cards["crossing"]["author_fixture"]["footbridge_target"],15)
        self.assertEqual(cards["crossing"]["author_fixture"]["ford_target"],12)
        self.assertEqual(cards["crossing"]["author_fixture"]["failure_detour_seconds"],
                         DETOUR_SECONDS)
        self.assertEqual(cards["cache"]["author_fixture"]["diagnose_target"],12)
        self.assertEqual(cards["gate_records"]["author_fixture"]["petition_target"],12)
        self.assertEqual(cards["gate_records"]["author_fixture"]["document_target"],12)
        self.assertEqual(cards["gate_records"]["author_fixture"][
            "diagnosis_conditional_situational_bonus"],2)
        self.assertIn("not a true cure",cards["cache"]["guardrail"])
        self.assertIn("not a universal",cards["gate_records"]["guardrail"])

    def test_04_native_gate_bounded_guard_dodge_and_original_soldier(self):
        gate=next(c for c in self.brief["gm_cards"] if c["stage"]=="gate_hostility")
        self.assertEqual(gate["author_fixture"]["original_opponent"],"B06-EN-02")
        self.assertEqual(gate["author_fixture"]["native_defenses"],
                         list(OPTIONS["priest_defense"]))
        self.assertTrue(any("24-AP" in x for x in gate["source_actions"]))
        self.assertTrue(any("full Low Priest" in x for x in gate["source_actions"]))
        self.assertIn("arbitrary tactical choices",gate["guardrail"])
        self.assertIn("Combat is optional",gate["prompt"])

    def test_05_blank_worksheet_and_original_packet_untouched_unobserved(self):
        p=alpha_blank()
        original=canonical_digest(p)
        report=validate_worksheet(self.blank)
        self.assertTrue(report["original_worksheet_unobserved"])
        self.assertEqual(report["source_reported_stage_refs"],0)
        self.assertEqual(report["source_blocked_stage_refs"],0)
        self.assertEqual(report["candidate_milestone_refs"],0)
        self.assertEqual(alpha_validate(p)["candidate_sessions_reported"],0)
        self.assertEqual(canonical_digest(p),original)
        self.assertTrue(all(x["status"]=="UNOBSERVED" for x in self.blank["stages"]))
        self.assertEqual(len(p["review_queue"]),84)

    def test_06_claimed_outcome_requires_real_source_reference_shapes(self):
        p=selected(self.blank)
        row=source_report(p,"crossing")
        self.assertEqual(validate_worksheet(p)["source_reported_stage_refs"],1)
        p["stages"][0]["resource_after_ref"]=""
        with self.assertRaises(ValueError):
            validate_worksheet(p)
        p=selected(self.blank)
        row=source_report(p,"crossing")
        row["unsupported_action_ref"]="synthetic:unresolved"
        with self.assertRaises(ValueError):
            validate_worksheet(p)

    def test_07_no_substituted_character_or_auto_selected_low_priest(self):
        for change in ("pairing","source","variant","borrowed","empty_player"):
            p=deepcopy(self.blank)
            c=p["characters"][0]
            if change=="pairing":
                c["pairing"]="Priest/High"
            elif change=="source":
                p["source_roster_digest"]="0"*64
            elif change=="variant":
                c["selected_variant"]="C"
            elif change=="borrowed":
                p=selected(p)
                p["characters"][1]["l1_selected_sheet_ref"]=p["characters"][0][
                    "l1_selected_sheet_ref"]
            else:
                c["selected_variant"]="B"
                c["l1_selected_sheet_ref"]="synthetic:selected"
            with self.subTest(change=change),self.assertRaises(ValueError):
                validate_worksheet(p)

    def test_08_unobserved_stage_cannot_claim_fake_evidence(self):
        for field in STAGE_FIELDS[3:]:
            p=deepcopy(self.blank)
            p["stages"][0][field]="synthetic:unseen"
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_worksheet(p)

    def test_09_blocked_action_requires_trace_and_leaves_milestone_unearned(self):
        p=deepcopy(self.blank)
        s=p["stages"][-1]
        s["status"]="SOURCE_BLOCKED"
        for k in ("scene_ref","unsupported_action_ref","gm_consequence_ref",
                  "resource_before_ref","clock_ref"):
            s[k]="synthetic:"+k
        report=validate_worksheet(p)
        self.assertEqual(report["source_blocked_stage_refs"],1)
        self.assertEqual(report["candidate_milestone_refs"],0)
        self.assertEqual(report["possible_current_level"],1)
        p["stages"][-1]["unsupported_action_ref"]=""
        with self.assertRaises(ValueError):
            validate_worksheet(p)

    def test_10_milestone_requires_actual_gate_ref_and_four_source_reviews(self):
        p=selected(self.blank)
        p["milestone_one"]["status"]="GM_EVENT_REPORTED_UNVERIFIED"
        p["milestone_one"]["gm_event_ref"]="synthetic:gm:declaration"
        p["milestone_one"]["group_story_achievement_ref"]="synthetic:story:meaning"
        p["milestone_one"]["l2_source_review_refs"]=[
            f"synthetic:L2:sheet:{i}" for i in range(4)]
        with self.assertRaises(ValueError):
            validate_worksheet(p)
        source_report(p,"gate_records")
        out=validate_worksheet(p)
        self.assertEqual(out["candidate_milestone_refs"],1)
        self.assertEqual(out["actual_milestones_authenticated"],0)
        self.assertEqual(out["possible_current_level"],1)
        p["milestone_one"]["l2_source_review_refs"][1]=p["milestone_one"][
            "l2_source_review_refs"][0]
        with self.assertRaises(ValueError):
            validate_worksheet(p)

    def test_11_reject_changed_gate_order_acceptance_and_false_flag(self):
        for change in ("beat","stage","level","cert","status","recorded_no_prep"):
            p=deepcopy(self.blank)
            if change=="beat":
                p["stages"][0]["beat"]="gate"
            elif change=="stage":
                p["stages"][0]["stage"]="gate_hostility"
            elif change=="level":
                p["level"]=2
            elif change=="cert":
                p["mvp_exits_accepted"]=1
            elif change=="status":
                p["status"]="PILOT_ACCEPTED"
            else:
                source_report(p,"gate_records")
            with self.subTest(change=change),self.assertRaises(ValueError):
                validate_worksheet(p)

    def test_12_no_raw_identifiers_echoed_and_no_certificate_from_filled_refs(self):
        p=selected(self.blank)
        source_report(p,"cache")
        out=validate_worksheet(p)
        encoded=json.dumps(out,sort_keys=True)
        self.assertNotIn("synthetic:fixture",encoded)
        self.assertNotIn("synthetic:player",encoded)
        self.assertFalse(out["original_worksheet_unobserved"])
        self.assertEqual(out["external_sessions_authenticated"],0)
        self.assertEqual(out["actual_milestones_authenticated"],0)
        self.assertEqual(out["independently_certified_focuses"],0)
        self.assertEqual(out["mvp_exits_accepted"],0)
        self.assertIn("source_action",out["reference_mapping"].values())

    def test_13_full_json_roundtrip_and_strict_field_types(self):
        p=json.loads(json.dumps(self.blank))
        self.assertEqual(validate_worksheet(p),validate_worksheet(self.blank))
        p["characters"][0]["selected_variant"]=None
        with self.assertRaises(ValueError):
            validate_worksheet(p)
        p=deepcopy(self.blank)
        p["stages"][0]["status"]=True
        with self.assertRaises(ValueError):
            validate_worksheet(p)
        p=deepcopy(self.blank)
        p["stages"][0]["new_fake_evidence"]="pretend"
        with self.assertRaises(ValueError):
            validate_worksheet(p)


if __name__=="__main__":
    unittest.main()
