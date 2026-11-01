"""First real-table Alpha cohort evidence intake and independent REVIEW QUEUE.

All submitted records and reviewer labels are untrusted. A valid receipt means
source/chronology/file integrity *preflight*, NOT an independently certified
person, GM milestone, play session, Focus or MVP exit gate.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re

from scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 import (
    COHORTS, CRITERIA, GATES,
)
from scripts.b04_b07_pilot_evidence_cohorts_v0 import (
    blank_packet as cohort_blank, preflight as cohort_preflight,
)
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import roster
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION = "B04-B05-B06-B07-First-Cohort-Execution-Evidence-v0"
COHORT_ID = "COHORT-ALPHA"
PAIRINGS = COHORTS[COHORT_ID]
STATUS = "CANDIDATE_UNVERIFIED"
CODES = tuple(CRITERIA)
DOC_KINDS = frozenset((
    "selected_sheet", "source_action", "resource_snapshot", "clock_trace",
    "player_choice", "gm_adjudication", "milestone_declaration",
    "review_notes", "countercase", "session_notes",
))
REVIEW_STATES = frozenset((
    "UNOBSERVED", "SUBMITTED", "REVIEWED_NEEDS_FIX",
    "REVIEWED_EVIDENCE_PRESENT",
))
ALLOWED_VARIANTS = {"Priest/Low": ("A", "B")}
# Source-scoped claims, NOT permissions to use these modules as a universal
# four-PC mixed-party adventure resolver.
CAPABILITIES = {
    "Priest/Low": {
        "selected_source": "scripts/b05_low_priest_life_l1_l3_v0.py",
        "bounded_anchor": "scripts/b04_b05_low_priest_complete_noncombat_v0.py",
        "constraint": "G8 A/B are physical proxies; separately source and pay Rite/Exaltation",
    },
    "Scholar/High": {
        "selected_source": "scripts/b05_high_scholar_fire_l1_l3_v0.py",
        "bounded_anchor": "scripts/b05_high_scholar_fire_l1_l3_v0.py",
        "constraint": "G8 Fire witness is authored policy, not chosen Alpha combat",
    },
    "Gifted/High": {
        "selected_source": "scripts/b05_high_gifted_l1_l3_v0.py",
        "bounded_anchor": "scripts/b05_high_gifted_native_encounter_v0.py",
        "constraint": "Emotion, paid Flame amplification and Instability require live source windows",
    },
    "Anointed/Medium": {
        "selected_source": "scripts/b05_medium_anointed_restoration_l1_l3_v0.py",
        "bounded_anchor": "scripts/b05_medium_anointed_native_returning_step_v0.py",
        "constraint": "Consent, one Vessel and recipient Step must be source-attested",
    },
}
# Named possible sessions, not human session IDs, outcomes or GM milestones.
SESSION_NOTES = (
    ("supply","gate"),
    ("forest",),
    ("shrine",),
    ("village",),
)
SOURCE_GAPS = (
    "L1 Alpha combat: no single native G8 L1 four-Focus encounter; select another proven source-legal scene",
    "L2 forest/Hunter: verify actual Alpha defenders, off-turn decisions, venom, escape and pursuit",
    "L2 shrine: verify source-legal cold/prepared Sentry response for the chosen Alpha members",
    "L3 village: obtain original GM and player choices; no scripted party victory substitutes",
    "Advancement with active poison/host: #196 rejects cross-level effect translation; settle naturally or implement source legal rebind",
)
REF_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
HEX_RE = re.compile(r"^[0-9a-f]{64}$")
MAX_BYTES = 128 * 1024 * 1024


def _shape(value, expected, label):
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError("Invalid " + label + " structure")


def _text(value, label):
    if type(value) is not str or not value.strip():
        raise ValueError("Missing " + label)
    return value


def _source_roster():
    rows = roster()
    if len(rows) != 12 or any(r["source_issues"] for r in rows):
        raise ValueError("Independent source audit has an unresolved issue")
    return {r["pairing"]: deepcopy(r["source_fingerprints"]) for r in rows}


def blank_packet():
    """Unreported first cohort, exact canonical source fingerprint snapshot."""
    src = _source_roster()
    if len(PAIRINGS) != 4 or set(PAIRINGS) != set(CAPABILITIES):
        raise AssertionError("First cohort roster drifted")
    example = cohort_blank(COHORT_ID, PAIRINGS)
    return {
        "version": VERSION,
        "cohort_id": COHORT_ID,
        "source_roster_digest": canonical_digest(src),
        "cohort_packet": example,
        "characters": [
            {"character_id": f"PC-{i}", "pairing": pairing,
             "source_fingerprints": deepcopy(src[pairing]),
             "selected_variant": "", "sheet_refs": {"1": "", "2": "", "3": ""},
             "independent_sheet_reviewer_ref": ""}
            for i, pairing in enumerate(PAIRINGS, 1)],
        "evidence_files": [],
        "review_queue": [
            {"character_id": f"PC-{i}", "level": level,
             "criterion": code, "status": "UNOBSERVED",
             "evidence_refs": [], "reviewer_identity_ref": "",
             "reviewer_ref": "", "finding_ref": ""}
            for i in range(1, 5) for level in (1, 2, 3) for code in CODES],
        "source_capabilities": deepcopy(CAPABILITIES),
        "scenario_gaps": list(SOURCE_GAPS),
        "session_plan": [{"number": i, "beats": list(beats)}
                         for i, beats in enumerate(SESSION_NOTES, 1)],
        "status": STATUS,
        "human_sessions_authenticated": 0,
        "actual_milestones_authenticated": 0,
        "independently_certified_focuses": 0,
        "strict_mvp_exits_met": 0,
    }


def _relative_path(value):
    _text(value,"evidence path")
    if ("\\" in value or any(ord(c) < 32 for c in value)
            or value.startswith("/") or value.endswith("/")):
        raise ValueError("Evidence path must be normalized and relative")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in (".","..") for part in value.split("/")):
        raise ValueError("Evidence path escapes reviewer evidence root")
    if str(p) != value:
        raise ValueError("Evidence path is noncanonical")
    return p


def _validate_files(entries, root):
    if type(entries) is not list:
        raise ValueError("Evidence manifest must be a list")
    found={}
    paths=set()
    base = None
    if root is not None:
        base=Path(root).resolve(strict=True)
        if not base.is_dir():
            raise ValueError("Reviewer evidence root must be a directory")
    for entry in entries:
        _shape(entry, ("ref_id","kind","path","sha256"),"evidence file")
        ref=entry["ref_id"]
        if type(ref) is not str or not REF_RE.fullmatch(ref) or ref in found:
            raise ValueError("Duplicate or invalid evidence reference")
        kind=entry["kind"]
        if type(kind) is not str or kind not in DOC_KINDS:
            raise ValueError("Unknown evidence document category")
        p=_relative_path(entry["path"])
        if str(p) in paths:
            raise ValueError("One evidence path cannot impersonate two document IDs")
        paths.add(str(p))
        digest=entry["sha256"]
        if type(digest) is not str or not HEX_RE.fullmatch(digest):
            raise ValueError("Evidence SHA256 must be exact lowercase hex")
        if base is not None:
            target=(base / str(p)).resolve(strict=True)
            if not target.is_relative_to(base) or not target.is_file():
                raise ValueError("Evidence file escaped root or is not a regular file")
            check=sha256()
            size=0
            with target.open("rb") as stream:
                for block in iter(lambda: stream.read(65536),b""):
                    size+=len(block)
                    if size>MAX_BYTES:
                        raise ValueError("Evidence file exceeds verifier read limit")
                    check.update(block)
            if check.hexdigest()!=digest:
                raise ValueError("Evidence bytes differ from manifest SHA256: "+ref)
        found[ref]=kind
    return found


def _reference(ref, found, allowed, label):
    if type(ref) is not str or ref not in found:
        raise ValueError("Unregistered evidence reference: "+label)
    if found[ref] not in allowed:
        raise ValueError("Wrong evidence document category: "+label)


def _cohort_crossbind(cohort, found):
    """Bind real claimed scenes/levels to registered primary evidence files."""
    c=cohort["cohorts"][0]
    if c["cohort_id"]!=COHORT_ID or tuple(
            x["pairing"] for x in c["characters"])!=PAIRINGS:
        raise ValueError("Nested cohort identity changed")
    for session in c["sessions"]:
        for key,allowed in (
                ("start_resource_state_ref",{"resource_snapshot"}),
                ("end_resource_state_ref",{"resource_snapshot"})):
            _reference(session[key],found,allowed,key)
        if session["inter_session_transition_ref"]:
            _reference(session["inter_session_transition_ref"],found,
                       {"source_action","clock_trace"},"transition")
        for scene in session["scenes"]:
            for key,allowed in (
                    ("choice_ref",{"player_choice"}),
                    ("alternative_ref",{"player_choice"}),
                    ("gm_consequence_ref",{"gm_adjudication"}),
                    ("source_action_ref",{"source_action"}),
                    ("resource_before_ref",{"resource_snapshot"}),
                    ("resource_after_ref",{"resource_snapshot"}),
                    ("world_clock_ref",{"clock_trace"})):
                _reference(scene[key],found,allowed,key)
    for milestone in c["milestones"]:
        for key,allowed in (
                ("gm_declaration_ref",{"milestone_declaration"}),
                ("story_achievement_ref",{"gm_adjudication"})):
            _reference(milestone[key],found,allowed,key)
        for sheet in milestone["reviewed_sheets"]:
            _reference(sheet["sheet_ref"],found,{"selected_sheet"},"milestone sheet")
            _reference(sheet["reviewer_ref"],found,{"review_notes"},"milestone review")
    for row in c["focus_level_evidence"]:
        for key,allowed in (
                ("sheet_ref",{"selected_sheet"}),
                ("combat_choice_ref",{"player_choice"}),
                ("noncombat_choice_ref",{"player_choice"}),
                ("alternative_ref",{"player_choice"}),
                ("countercase_ref",{"countercase"}),
                ("reviewer_ref",{"review_notes"})):
            _reference(row[key],found,allowed,key)


def validate(packet, *, evidence_root=None):
    """Check source, chronology and optional local bytes; no external authority."""
    template=blank_packet()
    _shape(packet,template,"first cohort packet")
    for field in ("version","cohort_id","source_roster_digest",
                  "source_capabilities","scenario_gaps","session_plan",
                  "status","human_sessions_authenticated",
                  "actual_milestones_authenticated",
                  "independently_certified_focuses","strict_mvp_exits_met"):
        if type(packet[field])!=type(template[field]) or packet[field]!=template[field]:
            raise ValueError("Reserved scope, source or certification flag altered: "+field)
    candidate=cohort_preflight(packet["cohort_packet"])
    if len(packet["cohort_packet"]["cohorts"])!=1:
        raise ValueError("Only the first Alpha cohort belongs in this packet")
    c=packet["cohort_packet"]["cohorts"][0]
    if c["cohort_id"]!=COHORT_ID:
        raise ValueError("Foreign cohort")
    expected_chars=template["characters"]
    actual_chars=packet["characters"]
    if type(actual_chars) is not list or len(actual_chars)!=4:
        raise ValueError("Exactly four original Alpha characters")
    found=_validate_files(packet["evidence_files"],evidence_root)
    for i,(record,baseline) in enumerate(zip(actual_chars,expected_chars)):
        _shape(record,baseline,"character source preflight")
        for k in ("character_id","pairing","source_fingerprints"):
            if record[k]!=baseline[k]:
                raise ValueError("Forged selected character source identity")
        if record["character_id"]!=c["characters"][i]["character_id"]:
            raise ValueError("Nested and selected character IDs disagree")
        if record["source_fingerprints"]!=c["characters"][i]["source_fingerprints"]:
            raise ValueError("Nested cohort source hash changed")
        variant=record["selected_variant"]
        if type(variant) is not str or variant not in (
                ("",)+ALLOWED_VARIANTS.get(record["pairing"],("default",))):
            raise ValueError("Illegal or implicit character variant")
        sheets=record["sheet_refs"]
        if type(sheets) is not dict or set(sheets)!=set(baseline["sheet_refs"]):
            raise ValueError("Invalid level-sheet selection")
        reviewer=record["independent_sheet_reviewer_ref"]
        if type(reviewer) is not str:
            raise ValueError("Invalid independent sheet reviewer reference")
        has_sheets=any(sheets.values())
        if has_sheets:
            if not variant:
                raise ValueError("Selected sheet needs explicit source variant")
            selected=[ref for ref in sheets.values() if ref]
            if len(selected)!=len(set(selected)):
                raise ValueError("Level sheet cannot be reused for a different level")
            for level,ref in sheets.items():
                if ref:
                    _reference(ref,found,{"selected_sheet"},"L"+level+" sheet")
            if not reviewer:
                raise ValueError("Selected sheet requires candidate independent review")
            _reference(reviewer,found,{"review_notes"},"sheet reviewer")
    _cohort_crossbind(packet["cohort_packet"],found)
    expected_queue=template["review_queue"]
    queue=packet["review_queue"]
    if type(queue) is not list or len(queue)!=len(expected_queue):
        raise ValueError("All 84 C1-C7 review slots must be present")
    reviewed=0
    submitted=0
    for value,original in zip(queue,expected_queue):
        _shape(value,original,"criterion review")
        if any(type(value[k])!=type(original[k]) or value[k]!=original[k]
               for k in ("character_id","level","criterion")):
            raise ValueError("Changed or reordered C1-C7 review owner")
        state=value["status"]
        if type(state) is not str or state not in REVIEW_STATES:
            raise ValueError("Invalid review state")
        refs=value["evidence_refs"]
        if type(refs) is not list or len(set(map(str,refs)))!=len(refs):
            raise ValueError("Duplicate or invalid review evidence list")
        if state=="UNOBSERVED":
            if (refs or value["reviewer_ref"] or value["finding_ref"]
                    or value["reviewer_identity_ref"]):
                raise ValueError("Unobserved criteria cannot claim evidence")
            continue
        if not refs:
            raise ValueError("Submitted review requires primary evidence")
        for ref in refs:
            _reference(ref,found,DOC_KINDS-{"review_notes"},"criterion primary evidence")
        reported_levels={scene["level"]
                         for session in c["sessions"] for scene in session["scenes"]}
        code=value["criterion"]
        level=value["level"]
        if code in ("C3","C4","C5","C6") and level not in reported_levels:
            raise ValueError("Cannot submit gameplay evidence for an unplayed level")
        if code=="C2" and level>1 and len(c["milestones"])<level-1:
            raise ValueError("Advancement review requires declared preceding GM event")
        if code=="C7" and len(c["milestones"])<min(level,2):
            raise ValueError("Milestone review requires actual declared source events")
        submitted+=1
        if state=="SUBMITTED":
            if (value["reviewer_ref"] or value["finding_ref"]
                    or value["reviewer_identity_ref"]):
                raise ValueError("Unreviewed submission cannot claim a referee")
            continue
        reviewer=_text(value["reviewer_identity_ref"],"reviewer pseudonymous ID")
        known_authors={c["gm_ref"],c["report_author_ref"]}
        known_authors.update(x["player_ref"] for x in c["characters"])
        if reviewer in known_authors or reviewer==value["character_id"]:
            raise ValueError("Reviewer cannot be the participant, author or GM")
        _reference(value["reviewer_ref"],found,{"review_notes"},"independent review")
        _reference(value["finding_ref"],found,{"review_notes"},"independent finding")
        if (value["reviewer_ref"] == value["finding_ref"]
                and value["reviewer_ref"] in refs):
            raise ValueError("Review note must not substitute for primary source")
        reviewed+=1
    return {
        "version":VERSION,"cohort":COHORT_ID,"status":STATUS,
        "candidate_sessions_reported":candidate["reported_session_references"],
        "candidate_milestones_reported":candidate["reported_milestone_references"],
        "candidate_focus_level_slots":candidate["candidate_unique_focus_level_slots"],
        "candidate_review_submissions":submitted,
        "candidate_review_notes_present":reviewed,
        "evidence_files_listed":len(found),
        "evidence_bytes_sha256_checked":evidence_root is not None,
        "external_human_identity_authenticated":False,
        "actual_gm_story_milestones_authenticated":0,
        "independently_certified_focuses":0,
        "strict_mvp_exits_met":0,
        "remaining_gates":[name for name,_ in GATES],
        "caution":"Hash, reference and reviewer-name consistency cannot authenticate actual play or independent reviewer identity",
    }


def run():
    """Machine-generated empty packet plus explicit first-cohort scenario gaps."""
    p=blank_packet()
    return {
        "version":VERSION,"status":STATUS,
        "cohort_id":COHORT_ID,"source_roster_digest":p["source_roster_digest"],
        "character_pairings":[x["pairing"] for x in p["characters"]],
        "level_review_slots":len(p["review_queue"]),
        "blank_packet_preflight":validate(p),
        "first_cohort_source_boundaries":deepcopy(CAPABILITIES),
        "blocking_scenes":list(SOURCE_GAPS),
        "recommended_schedule":deepcopy(p["session_plan"]),
        "pilot_sheets_need_real_player_selection":True,
        "individual_C1_C7_certification":False,
        "strict_mvp_exits_met":0,
    }


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    group=cli.add_mutually_exclusive_group()
    group.add_argument("--blank",action="store_true")
    group.add_argument("--check",metavar="JSON")
    cli.add_argument("--evidence-root",metavar="DIR")
    args=cli.parse_args()
    if args.evidence_root and not args.check:
        cli.error("--evidence-root requires --check")
    if args.check:
        with open(args.check,encoding="utf-8") as stream:
            value=validate(json.load(stream),evidence_root=args.evidence_root)
    else:
        value=blank_packet() if args.blank else run()
    print(json.dumps(value,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
