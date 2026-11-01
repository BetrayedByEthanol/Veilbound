"""Session 1 Alpha live-intake preflight and read-only canonical evidence crossbind.

Reads PRIVATE worksheet + canonical first-cohort packet + original evidence
bytes. Does not create fake play, alter files, certify a referee, apply game
effects or award a milestone. Keep all real inputs outside public CI/repo.
"""
import argparse
from copy import deepcopy
import json

from scripts.b04_b05_b06_b07_alpha_session_one_v0 import (
    blank_worksheet, validate_worksheet, GM_PREP_FIELDS, STAGES,
)
from scripts.b04_b05_b06_b07_first_cohort_pilot_v0 import (
    blank_packet, validate as validate_alpha, DOC_KINDS,
    COHORT_ID,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION="B04-B05-B06-B07-Alpha-Session1-Live-Intake-v0"
CROSSWALK={
    "chosen_ref":("choice_ref","player_choice"),
    "declined_alternative_ref":("alternative_ref","player_choice"),
    "gm_consequence_ref":("gm_consequence_ref","gm_adjudication"),
    "source_action_ref":("source_action_ref","source_action"),
    "resource_before_ref":("resource_before_ref","resource_snapshot"),
    "resource_after_ref":("resource_after_ref","resource_snapshot"),
    "clock_ref":("world_clock_ref","clock_trace"),
}
EXTRAS={
    "outcome_ref":"gm_adjudication",
    "starting_resources_ref":"resource_snapshot",
    "l1_selected_sheet_ref":"selected_sheet",
    "final_resource_ref":"resource_snapshot",
    "world_clock_ref":"clock_trace",
    "outstanding_effects_ref":"resource_snapshot",
    "actual_next_session_handoff_ref":("source_action","clock_trace"),
    "unresolved_source_issue_ref":"countercase",
    "unsupported_action_ref":"countercase",
}
STOP_REASONS={
    "missing_actual_GM_source_prep":"Complete required GM truth, session, safety and independent reviewer references.",
    "missing_selected_Alpha_L1_sheets":"Obtain four full source-legal L1 selected sheets, player refs, starting resource snapshots and explicit Low Priest A/B.",
    "blocked_source_actions":"Resolve or separately referee the declared action; do not convert a blocked tactic into a success or G5 exit.",
    "missing_observed_stage":"No original player/GM scene decision has been submitted; template is unobserved.",
}


def preflight(worksheet=None):
    """Non-invasive checklist. A fully filled fixture is STILL not live play."""
    w=deepcopy(blank_worksheet() if worksheet is None else worksheet)
    shape=validate_worksheet(w)
    incomplete=[key for key in GM_PREP_FIELDS if not w["gm_prep"][key]]
    sheets=[c["character_id"] for c in w["characters"] if not(
        c["selected_variant"] and c["l1_selected_sheet_ref"]
        and c["player_ref"] and c["starting_resources_ref"])]
    blocked=[s["stage"] for s in w["stages"] if s["status"]=="SOURCE_BLOCKED"]
    observed=[s["stage"] for s in w["stages"] if s["status"]=="SOURCE_REPORTED"]
    pending=[]
    if incomplete:
        pending.append("missing_actual_GM_source_prep")
    if sheets:
        pending.append("missing_selected_Alpha_L1_sheets")
    if blocked:
        pending.append("blocked_source_actions")
    if not observed:
        pending.append("missing_observed_stage")
    return {
        "version":VERSION,"scope":"Session 1 L1 supply/gate, original Alpha",
        "status":("REFERENCE_ONLY_POSSIBLE_INTAKE" if not pending
                  else "NO_GO_FOR_LIVE_INTAKE"),
        "pre_session_GM_reference_fields_complete":not incomplete,
        "selected_four_L1_sheets_declared":not sheets,
        "missing_preparation_field_names":incomplete,
        "unselected_character_ids":sheets,
        "source_reported_stages":len(observed),
        "source_blocked_stages":len(blocked),
        "missing_or_blocked_conditions":[{"id":p,"action":STOP_REASONS[p]} for p in pending],
        "candidate_GM_milestone_reported":shape["candidate_milestone_refs"],
        "canonical_manifest_bytes_checked":False,
        "external_session_authenticated":False,
        "human_GM_or_reviewer_identity_authenticated":False,
        "actual_GM_milestones_authenticated":0,
        "independently_certified_focuses":0,
        "strict_mvp_exits_met":0,
        "caution":"Preflight only checks reference structure. No observed play, independently reviewed legal action or milestone is authenticated.",
    }


def _registered(ref,kind,manifest):
    allowed=(kind,) if type(kind) is str else tuple(kind)
    if (type(ref) is not str or not ref or ref not in manifest
            or manifest[ref] not in allowed):
        raise ValueError("Missing or wrong category source evidence reference: "+
                         "/".join(allowed))


def _crossbind(worksheet, packet):
    """Assert the private worksheet refers to EXACT original canonical evidence.

    Not a second ingestion format: submitted original packet and its 84 C1-C7
    rows remain authoritative. This routine only checks that no local
    worksheet source report silently contradicts that original packet.
    """
    w=worksheet
    c=packet["cohort_packet"]["cohorts"][0]
    if len(c["sessions"])!=1:
        raise ValueError("Session 1 intake accepts exactly one actual session, not later/merged records")
    session=c["sessions"][0]
    if (session["session_id"]!=w["gm_prep"]["session_ref"]
            or c["gm_ref"]!=w["gm_prep"]["gm_ref"]):
        raise ValueError("Session or GM source identity differs between worksheet and Alpha intake")
    if not all(w["gm_prep"][key] for key in GM_PREP_FIELDS):
        raise ValueError("GM, safety, source, terrain, keeper and private evidence preparation incomplete")
    # The baseline validator also ensures all source fingerprints and the
    # nested character roster exactly match original Alpha PAIRINGS.
    manifest={x["ref_id"]:x["kind"] for x in packet["evidence_files"]}
    for index,actor in enumerate(w["characters"]):
        pc=packet["characters"][index]
        nested=c["characters"][index]
        if (actor["character_id"]!=pc["character_id"]
                or actor["pairing"]!=pc["pairing"]
                or actor["selected_variant"]!=pc["selected_variant"]
                or actor["l1_selected_sheet_ref"]!=pc["sheet_refs"]["1"]
                or actor["player_ref"]!=nested["player_ref"]):
            raise ValueError("Original selected character or L1 source sheet mismatch")
        for attr in ("l1_selected_sheet_ref","starting_resources_ref"):
            _registered(actor[attr], EXTRAS[attr], manifest)
        if not actor["selected_variant"]:
            raise ValueError("Explicit actual selection required for all four original Alpha PCs")
    scenes=session["scenes"]
    reported=[s for s in w["stages"] if s["status"]=="SOURCE_REPORTED"]
    blocked=[s for s in w["stages"] if s["status"]=="SOURCE_BLOCKED"]
    if not reported or len(scenes)!=len(reported):
        raise ValueError("Canonical played scenes must equal source-reported worksheet stages")
    for stage,scene in zip(reported,scenes):
        if (stage["scene_ref"]!=scene["scene_id"] or
                scene["beat"]!=stage["beat"] or scene["level"]!=1):
            raise ValueError("Source stage/chronology differs from original played scene")
        for worksheet_field,(scene_field,kind) in CROSSWALK.items():
            ref=stage[worksheet_field]
            if ref!=scene[scene_field]:
                raise ValueError("Played scene does not bind original "+worksheet_field)
            _registered(ref,kind,manifest)
        _registered(stage["outcome_ref"],EXTRAS["outcome_ref"],manifest)
    canonical_ids={s["scene_id"] for s in scenes}
    for stage in blocked:
        if stage["scene_ref"] in canonical_ids:
            raise ValueError("Blocked action improperly exported as source-resolved scene")
        _registered(stage["unsupported_action_ref"],"countercase",manifest)
        _registered(stage["gm_consequence_ref"],"gm_adjudication",manifest)
        _registered(stage["resource_before_ref"],"resource_snapshot",manifest)
        _registered(stage["clock_ref"],"clock_trace",manifest)
    end=w["end_session"]
    for field in ("final_resource_ref","world_clock_ref"):
        _registered(end[field],EXTRAS[field],manifest)
    if end["final_resource_ref"]!=session["end_resource_state_ref"]:
        raise ValueError("Session exit resource snapshot not original canonical ending")
    for field in ("outstanding_effects_ref","actual_next_session_handoff_ref",
                  "unresolved_source_issue_ref"):
        if end[field]:
            _registered(end[field],EXTRAS[field],manifest)
    if blocked and not end["unresolved_source_issue_ref"]:
        raise ValueError("Blocked action requires an unresolved source handoff")
    if not blocked and end["unresolved_source_issue_ref"]:
        raise ValueError("Unresolved issue declared without a blocked source stage")
    if w["milestone_one"]["status"]=="NOT_DECLARED":
        if c["milestones"]:
            raise ValueError("Canonical evidence cannot invent an unreported group milestone")
    else:
        if len(c["milestones"])!=1:
            raise ValueError("Exactly one reported GM source milestone required")
        m=c["milestones"][0]
        local=w["milestone_one"]
        if (m["gm_declaration_ref"]!=local["gm_event_ref"]
                or m["story_achievement_ref"]!=local["group_story_achievement_ref"]
                or m["from_level"]!=1 or m["to_level"]!=2
                or m["after_scene_id"] not in
                    {s["scene_ref"] for s in reported if s["beat"]=="gate"}
                or {x["character_id"]:x["sheet_ref"] for x in m["reviewed_sheets"]}
                   !={w["characters"][i]["character_id"]:ref
                      for i,ref in enumerate(local["l2_source_review_refs"])}):
            raise ValueError("Real group milestone does not match original gate and four L2 sheet reviews")
        _registered(local["gm_event_ref"],"milestone_declaration",manifest)
        _registered(local["group_story_achievement_ref"],"gm_adjudication",manifest)
    return len(reported),len(blocked)


def intake(worksheet, packet, *, evidence_root):
    """Read-only crosscheck verified original bytes; output no private ref IDs.

    A valid SHA can be computed over invented data. All authentic human play,
    legal action decisions, GM rulings and independent review remain external.
    """
    if evidence_root is None:
        raise ValueError("Real intake must check private primary bytes; evidence_root is required")
    worksheet=deepcopy(worksheet)
    packet=deepcopy(packet)
    status=preflight(worksheet)
    # Always invoke existing authoritative Alpha validator (source, 84 rows,
    # chronology, selected sheet/reviewer, and local file hash/path security).
    original=validate_alpha(packet,evidence_root=evidence_root)
    if original["evidence_bytes_sha256_checked"] is not True:
        raise AssertionError("Canonical evidence bytes must be verified before intake")
    reported,blocked=_crossbind(worksheet,packet)
    if not status["selected_four_L1_sheets_declared"]:
        raise ValueError("Actual selected full L1 source sheets missing")
    if blocked and not status["source_blocked_stages"]:
        raise AssertionError("Blocked action inconsistent")
    return {
        "version":VERSION,"cohort_id":COHORT_ID,
        "status":("HOLD_FOR_SOURCE_ADJUDICATION" if blocked else
                  "REFERENCES_AND_LOCAL_BYTES_VERIFIED_PENDING_INDEPENDENT_REVIEW"),
        "source_evidence_packet_read_only":True,
        "canonical_first_cohort_version":packet["version"],
        "canonical_manifest_sha256":canonical_digest(packet["evidence_files"]),
        "canonical_manifest_local_bytes_verified":True,
        "canonical_manifest_files_checked":original["evidence_files_listed"],
        "candidate_session_references":original["candidate_sessions_reported"],
        "source_reported_stages":reported,"source_blocked_stages":blocked,
        "candidate_milestone_declarations":original["candidate_milestones_reported"],
        "review_notes_claimed":original["candidate_review_notes_present"],
        "original_C1_C7_review_submissions":original["candidate_review_submissions"],
        "next_steps":(
            ["Resolve the real source-blocked choices and recheck original evidence."]
            if blocked else
            ["Independent reviewer verifies actual participants, legal rolls, choices, GM rulings, countercases and milestone; no automatic acceptance."]
        ),
        "external_session_authenticated":False,
        "human_GM_or_reviewer_identity_authenticated":False,
        "actual_GM_milestones_authenticated":0,
        "independently_certified_focuses":0,"strict_mvp_exits_met":0,
        "caution":"Local SHA256 and exact source references do NOT authenticate human activity or independent review.",
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument("--preflight",metavar="WORKSHEET")
    group.add_argument("--intake",metavar="WORKSHEET")
    parser.add_argument("--packet",metavar="ALPHA_JSON")
    parser.add_argument("--evidence-root",metavar="PRIVATE_DIR")
    args=parser.parse_args()
    if args.intake:
        if not args.packet or not args.evidence_root:
            parser.error("--intake requires --packet and --evidence-root")
        with open(args.intake,encoding="utf-8") as stream:
            worksheet=json.load(stream)
        with open(args.packet,encoding="utf-8") as stream:
            packet=json.load(stream)
        result=intake(worksheet,packet,evidence_root=args.evidence_root)
    else:
        if args.packet or args.evidence_root:
            parser.error("--packet/--evidence-root are only valid with --intake")
        if args.preflight:
            with open(args.preflight,encoding="utf-8") as stream:
                worksheet=json.load(stream)
        else:
            worksheet=None
        result=preflight(worksheet)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
