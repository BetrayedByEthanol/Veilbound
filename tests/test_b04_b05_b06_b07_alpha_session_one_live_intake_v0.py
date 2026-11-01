"""Alpha Session 1 source/GM preflight and read-only local evidence intake tests.

Every "played" reference is an explicitly synthetic local unit-test fixture.
Never an observed session or independent signoff.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.b04_b05_b06_b07_alpha_session_one_live_intake_v0 import (
    preflight,intake,VERSION,CROSSWALK,
)
from scripts.b04_b05_b06_b07_alpha_session_one_v0 import (
    blank_worksheet,GM_PREP_FIELDS,validate_worksheet,
)
from scripts.b04_b05_b06_b07_first_cohort_pilot_v0 import (
    blank_packet,validate as validate_alpha,DOC_KINDS,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def register(p,root,kind,name):
    assert kind in DOC_KINDS
    b=("SYNTHETIC UNIT TEST PRIMARY EVIDENCE, NOT HUMAN PLAY: "+name).encode()
    path="records/"+name+".txt"
    f=Path(root)/path
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_bytes(b)
    p["evidence_files"].append({
        "ref_id":name,"path":path,"kind":kind,
        "sha256":sha256(b).hexdigest()})
    return name


def fixture(root,*,stages=("crossing","gate_records"),blocked=(),milestone=False):
    """Two original source-shaped records and an unmodified review queue."""
    w=blank_worksheet()
    p=blank_packet()
    nested=p["cohort_packet"]["cohorts"][0]
    nested["gm_ref"]="SYNTHETIC-GM"
    nested["report_author_ref"]="SYNTHETIC-REPORTER"
    for k in GM_PREP_FIELDS:
        w["gm_prep"][k]="SYNTHETIC-PREPARATION-"+k
    w["gm_prep"]["gm_ref"]=nested["gm_ref"]
    w["gm_prep"]["session_ref"]="SYNTHETIC-SESSION-1"
    get=lambda kind,ref:register(p,root,kind,ref)
    for i,(sc,c,actor) in enumerate(zip(w["characters"],p["characters"],
                                       nested["characters"]),1):
        v="B" if i==1 else "default"
        sheet=get("selected_sheet",f"SYNTHETIC-L1-SHEET-{i}")
        source=get("resource_snapshot",f"SYNTHETIC-L1-INITIAL-{i}")
        review=get("review_notes",f"SYNTHETIC-L1-REVIEW-{i}")
        player=f"SYNTHETIC-PLAYER-{i}"
        sc.update(selected_variant=v,l1_selected_sheet_ref=sheet,
                  starting_resources_ref=source,player_ref=player)
        c["selected_variant"]=v
        c["sheet_refs"]["1"]=sheet
        c["independent_sheet_reviewer_ref"]=review
        actor["player_ref"]=player
    played=[]
    for stage in w["stages"]:
        if stage["stage"] in stages:
            name=stage["stage"]
            stage["status"]="SOURCE_REPORTED"
            stage["scene_ref"]="SYNTHETIC-SCENE-"+name
            mapping={}
            for local,(canonical,kind) in CROSSWALK.items():
                ref=get(kind,f"SYNTHETIC-{name}-{local}")
                stage[local]=ref
                mapping[canonical]=ref
            stage["outcome_ref"]=get(
                "gm_adjudication",f"SYNTHETIC-{name}-outcome")
            played.append(dict(scene_id=stage["scene_ref"],beat=stage["beat"],
                               level=1,outcome="partial",**mapping))
        elif stage["stage"] in blocked:
            stage["status"]="SOURCE_BLOCKED"
            stage["scene_ref"]="SYNTHETIC-BLOCKED-"+stage["stage"]
            for kind,key in (("countercase","unsupported_action_ref"),
                             ("gm_adjudication","gm_consequence_ref"),
                             ("resource_snapshot","resource_before_ref"),
                             ("clock_trace","clock_ref")):
                stage[key]=get(kind,"SYNTHETIC-BLOCKED-"+stage["stage"]+"-"+key)
    begin=get("resource_snapshot","SYNTHETIC-PARTY-START")
    end=get("resource_snapshot","SYNTHETIC-PARTY-END")
    clock=get("clock_trace","SYNTHETIC-PARTY-END-CLOCK")
    w["end_session"]["final_resource_ref"]=end
    w["end_session"]["world_clock_ref"]=clock
    if blocked:
        w["end_session"]["unresolved_source_issue_ref"]=get(
            "countercase","SYNTHETIC-UNRESOLVED-SOURCE")
    nested["sessions"].append(dict(
        session_id=w["gm_prep"]["session_ref"],played_at="SYNTHETIC-DATE",
        incoming_handoff_ref="",inter_session_transition_ref="",
        start_resource_state_ref=begin,end_resource_state_ref=end,
        scenes=played))
    if milestone:
        if not any(s["beat"]=="gate" for s in played):
            raise ValueError("Milestone fixture needs a real gate scene")
        declaration=get("milestone_declaration","SYNTHETIC-GM-DECLARATION")
        story=get("gm_adjudication","SYNTHETIC-STORY-BEAT")
        sheets=[]
        for i,c in enumerate(p["characters"],1):
            target=get("selected_sheet",f"SYNTHETIC-L2-SHEET-{i}")
            c["sheet_refs"]["2"]=target
            sheets.append({
                "character_id":c["character_id"],"sheet_ref":target,
                "reviewer_ref":c["independent_sheet_reviewer_ref"]})
        nested["milestones"].append(dict(
            event_id="SYNTHETIC-GROUP-MILESTONE-1",
            after_scene_id=next(s["scene_id"] for s in played
                                if s["beat"]=="gate"),
            from_level=1,to_level=2,gm_declaration_ref=declaration,
            story_achievement_ref=story,reviewed_sheets=sheets))
        w["milestone_one"].update(
            status="GM_EVENT_REPORTED_UNVERIFIED",gm_event_ref=declaration,
            group_story_achievement_ref=story,
            l2_source_review_refs=[x["sheet_ref"] for x in sheets])
    assert validate_worksheet(w)
    assert validate_alpha(p,evidence_root=root)["evidence_bytes_sha256_checked"]
    return w,p


class AlphaLiveIntakeTests(unittest.TestCase):
    def test_01_blank_no_go_does_not_create_play(self):
        w=blank_worksheet()
        before=canonical_digest(w)
        r=preflight(w)
        self.assertEqual(r["status"],"NO_GO_FOR_LIVE_INTAKE")
        self.assertEqual(r["source_reported_stages"],0)
        self.assertEqual(r["source_blocked_stages"],0)
        self.assertFalse(r["canonical_manifest_bytes_checked"])
        self.assertGreaterEqual(len(r["missing_preparation_field_names"]),8)
        self.assertEqual(r["unselected_character_ids"],
                         ["PC-1","PC-2","PC-3","PC-4"])
        self.assertEqual(canonical_digest(w),before)

    def test_02_filled_prep_is_not_a_session_or_actual_reviewer(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            p0=canonical_digest(p)
            w0=canonical_digest(w)
            r=preflight(w)
            self.assertEqual(r["status"],"REFERENCE_ONLY_POSSIBLE_INTAKE")
            self.assertEqual(r["source_reported_stages"],2)
            self.assertEqual(r["candidate_GM_milestone_reported"],0)
            self.assertEqual(r["external_session_authenticated"],False)
            self.assertEqual(canonical_digest(p),p0)
            self.assertEqual(canonical_digest(w),w0)

    def test_03_original_bytes_and_exact_scene_refs_successfully_crossbind(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            wp,pp=canonical_digest(w),canonical_digest(p)
            r=intake(w,p,evidence_root=root)
            self.assertEqual(r["version"],VERSION)
            self.assertEqual(
                r["status"],
                "REFERENCES_AND_LOCAL_BYTES_VERIFIED_PENDING_INDEPENDENT_REVIEW")
            self.assertEqual(r["candidate_session_references"],1)
            self.assertEqual(r["source_reported_stages"],2)
            self.assertEqual(r["source_blocked_stages"],0)
            self.assertEqual(r["candidate_milestone_declarations"],0)
            self.assertEqual(r["canonical_manifest_files_checked"],len(p["evidence_files"]))
            self.assertEqual(r["canonical_manifest_sha256"],
                             canonical_digest(p["evidence_files"]))
            self.assertEqual(canonical_digest(p),pp)
            self.assertEqual(canonical_digest(w),wp)

    def test_04_prevent_missing_or_bypassed_local_sha256_verification(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=None)
            first=p["evidence_files"][0]
            (Path(root)/first["path"]).write_bytes(b"modified without updating hash")
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)

    def test_05_worksheet_cannot_change_original_canonical_decision(self):
        for local in CROSSWALK:
            with self.subTest(field=local),TemporaryDirectory() as root:
                w,p=fixture(root)
                stage=w["stages"][0]
                stage[local]="SYNTHETIC-FORGED-"+local
                with self.assertRaises(ValueError):
                    intake(w,p,evidence_root=root)

    def test_06_cannot_export_unobserved_or_unsourced_play(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            w["stages"][0]["status"]="UNOBSERVED"
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            p["cohort_packet"]["cohorts"][0]["sessions"][0]["scenes"][0][
                "scene_id"]="SYNTHETIC-ANOTHER-SCENE"
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)

    def test_07_cannot_borrow_a_historical_alpha_sheet_or_actor(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            w["characters"][0]["l1_selected_sheet_ref"]=w["characters"][1][
                "l1_selected_sheet_ref"]
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            w["characters"][0]["selected_variant"]="A"
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)

    def test_08_blocked_tactic_held_not_claimed_as_resolved_or_c3(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root,stages=("crossing",),blocked=("gate_hostility",))
            r=intake(w,p,evidence_root=root)
            self.assertEqual(r["status"],"HOLD_FOR_SOURCE_ADJUDICATION")
            self.assertEqual(r["source_blocked_stages"],1)
            self.assertEqual(r["source_reported_stages"],1)
            self.assertEqual(r["independently_certified_focuses"],0)
            self.assertEqual(r["strict_mvp_exits_met"],0)
            # Fabricating a canonical "played" scene from the blocked stage
            # must not convert it into verified source action evidence.
            additional=dict(p["cohort_packet"]["cohorts"][0]["sessions"][0][
                "scenes"][0])
            additional["scene_id"]=w["stages"][3]["scene_ref"]
            additional["beat"]="gate"
            p["cohort_packet"]["cohorts"][0]["sessions"][0]["scenes"].append(
                additional)
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)

    def test_09_cannot_skip_original_real_end_state_and_clock(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            w["end_session"]["final_resource_ref"]="SYNTHETIC-PARTY-START"
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            w["end_session"]["world_clock_ref"]=""
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)

    def test_10_distinct_GM_milestone_is_candidate_not_automatic_Level2(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root,milestone=True)
            r=intake(w,p,evidence_root=root)
            self.assertEqual(r["candidate_milestone_declarations"],1)
            self.assertEqual(r["actual_GM_milestones_authenticated"],0)
            self.assertEqual(r["external_session_authenticated"],False)
        with TemporaryDirectory() as root:
            w,p=fixture(root,milestone=True)
            w["milestone_one"]["gm_event_ref"]="SYNTHETIC-FAKE-GM"
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            w["milestone_one"]["status"]="NOT_DECLARED"
            # extra original GM award is rejected by original validator or
            # our worksheet/canonical explicit symmetry check.
            p["cohort_packet"]["cohorts"][0]["milestones"]=[{
                "event_id":"SYNTHETIC-FORGED","after_scene_id":"SYNTHETIC-SCENE-gate_records",
                "from_level":1,"to_level":2,"gm_declaration_ref":"MISSING",
                "story_achievement_ref":"MISSING","reviewed_sheets":[]}]
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)

    def test_11_reject_multiple_sessions_or_unmatched_GM_identity(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            p["cohort_packet"]["cohorts"][0]["gm_ref"]="ANOTHER"
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            s=deepcopy(p["cohort_packet"]["cohorts"][0]["sessions"][0])
            s["session_id"]="SYNTHETIC-SECOND"
            s["incoming_handoff_ref"]=s["start_resource_state_ref"]
            s["inter_session_transition_ref"]="SYNTHETIC-FORGED"
            p["cohort_packet"]["cohorts"][0]["sessions"].append(s)
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)

    def test_12_no_private_identifiers_or_session_certification_in_output(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            r=intake(w,p,evidence_root=root)
            text=json.dumps(r,sort_keys=True)
            self.assertNotIn("SYNTHETIC-PLAYER",text)
            self.assertNotIn("SYNTHETIC-GM",text)
            self.assertNotIn(str(root),text)
            self.assertTrue(r["source_evidence_packet_read_only"])
            self.assertFalse(r["human_GM_or_reviewer_identity_authenticated"])
            self.assertEqual(r["actual_GM_milestones_authenticated"],0)
            self.assertEqual(r["independently_certified_focuses"],0)
            self.assertEqual(r["strict_mvp_exits_met"],0)

    def test_13_wrong_category_or_symlink_cannot_impersonate_source(self):
        with TemporaryDirectory() as root:
            w,p=fixture(root)
            entry=next(e for e in p["evidence_files"]
                       if e["ref_id"]==w["characters"][0]["l1_selected_sheet_ref"])
            entry["kind"]="clock_trace"
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)
        with TemporaryDirectory() as root,TemporaryDirectory() as other:
            w,p=fixture(root)
            first=p["evidence_files"][0]
            inside=Path(root)/first["path"]
            outside=Path(other)/"record"
            outside.write_bytes(inside.read_bytes())
            inside.unlink()
            inside.symlink_to(outside)
            with self.assertRaises(ValueError):
                intake(w,p,evidence_root=root)


if __name__=="__main__":
    unittest.main()
