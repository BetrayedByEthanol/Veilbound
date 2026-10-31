"""B04/B05/B06/B07 restricted L1-3, 3-5-session MVP adventure organiser v0.

Five connected GM story beats, explicitly conditional GM-declared milestone
windows, source-referenced combat/noncombat branches and FAIL-CLOSED,
untrusted human play intake. No rules engine, real session, GM decision,
level award, independent certification or MVP acceptance is synthesized.
"""
import argparse
from copy import deepcopy
import json

from scripts.b04_b07_twelve_focus_certification_protocol_v0 import (
    FOCUS_TASKS, LEVELS, roster,
)
from scripts.b05_b06_integrated_noncombat_adventure_v0 import PLANS as NONCOMBAT_PLANS
from scripts.b06_representative_gm_encounter_packs_v0 import PACKS, GM_BRIEFS
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION = "B04-B05-B06-B07-Integrated-Pilot-Adventure-v0"
STATUS = "CANDIDATE_UNVERIFIED"
SESSION_GROUPS = {
    3: (("supply", "gate"), ("forest", "shrine"), ("village",)),
    4: (("supply", "gate"), ("forest",), ("shrine",), ("village",)),
    5: (("supply",), ("gate",), ("forest",), ("shrine",), ("village",)),
}
BEATS = {
    "supply": {
        "level": 1, "chapter": "The spoiled herb shipment",
        "goal": "Reach the supply cache and trace contamination without presuming a magical cure",
        "fiction": "The village has suffered a supply shortage and spoiled herbs; some symptoms may have other GM-determined causes",
        "routes": ("ordinary survey/diagnosis", "held-ring Veil Inspection",
                   "source-accessible Priest/Scholar utility"),
        "origin": "B05/B06 Supply-Cache Ledger #188",
        "native_anchor": "scripts/b05_b06_integrated_noncombat_adventure_v0.py",
        "mechanical_scope": "L1 source-backed noncombat; authored choices, AP/VP/time, not external GM outcome",
        "failure_forward": "An unsuccessful check leaves causes uncertain and may add the authored 300-second route detour; clues need not vanish",
        "gm_open_questions": ("Which observations are true in this village?",
                              "Which real character holds the inspected ring?",
                              "Does the actual play scene require a roll?"),
    },
    "gate": {
        "level": 1, "chapter": "Road-gate passage and public supply records",
        "goal": "Secure access to the records or a credible alternative lead",
        "fiction": "A source Ordinary Soldier challenges passage; the neutral storekeeper has public supply records",
        "routes": ("social petition supported by actual medical diagnosis",
                   "physical record evidence", "retreat or another lawful route"),
        "origin": "B06 Soldier gate candidate #189, B05/B06 records #188",
        "native_anchor": "scripts/b06_representative_gm_encounter_packs_v0.py",
        "mechanical_scope": "L1 gate is nonhostile/social; G8 Soldier combat is L2/L3 only, NOT legal L1 replay",
        "failure_forward": "Refusal triggers a GM-chosen alternate witness or detour, not forced combat or guaranteed log access",
        "gm_open_questions": ("Does the Soldier choose combat after an actual player declaration?",
                              "If yes at L1, which separately source-legal L1 engine resolves it?",
                              "Is the group-story supply truth meaningful enough for Milestone One?"),
    },
    "forest": {
        "level": 2, "chapter": "The Hunter's forest corridor",
        "goal": "Reach the shrine safely through warning signs, alternative routes and predator territory",
        "fiction": "Hunter tracks reveal potential territorial danger; an encounter is avoidable by GM/player choice",
        "routes": ("follow clues and avoid contact", "warned party protection or retreat",
                   "original P3/P4 forest ordinary versus genuine Pounce"),
        "origin": "B06 Hunter GM candidate #189; G7F/G7H source natives",
        "native_anchor": "scripts/b06_representative_gm_encounter_packs_v0.py",
        "mechanical_scope": "L2 G7F P3/4 forest tactics and L2 G7H P4 terminals; separate source scenes",
        "failure_forward": "A scene-local exit leaves Hunter pursuit, venom onset, injuries and rest safety unresolved",
        "gm_open_questions": ("Does contact become hostile?", "Is the retreat actually safe beyond the border?",
                              "Can six-hour recovery be attempted without active pursuit?"),
    },
    "shrine": {
        "level": 2, "chapter": "Cold or prepared Firebound Sentry at the shrine",
        "goal": "Obtain access to the contaminated source or a usable alternative without assuming a magical ward is destroyed",
        "fiction": "The shrine's actual guardian may be unprepared or have already committed VP before the group arrives",
        "routes": ("observe/parley", "native G8 L2 cold_start fight or withdrawal",
                   "native G8 L2 prepared_start fight or withdrawal"),
        "origin": "B06 Sentry GM candidates #189",
        "native_anchor": "scripts/b06_representative_gm_encounter_packs_v0.py",
        "mechanical_scope": "L2 G8 P4 source-native cold/prepared Sentry; no invented shrine ward or automatic victory",
        "failure_forward": "Withdrawal/failed approach redirects to another shrine access route and leaves a living guardian possible",
        "gm_open_questions": ("Was preparation established in actual fiction?",
                              "What secures the dangerous supply route?",
                              "Is Milestone Two an actually completed significant group event?"),
    },
    "village": {
        "level": 3, "chapter": "Return, safeguard and help the village",
        "goal": "Resolve the supply threat and its consequences through actual PC decisions",
        "fiction": "The group returns with whichever documentary, herb or magical evidence they really obtained",
        "routes": ("social/technical follow-up and safe treatment", "source-legal L3 Focus role choice",
                   "conditional remaining L3 Soldier/Sentry/Hunter confrontation"),
        "origin": "B05/B06 source #188, B06 combat candidates #189, C1-C7 source roster #184",
        "native_anchor": "scripts/b05_b06_integrated_noncombat_adventure_v0.py",
        "mechanical_scope": "L3 ordinary decisions; L3 G8/G7H combat candidates only with separately reestablished legal source state",
        "failure_forward": "An incomplete cure/failed evacuation becomes an open GM resolution, not automatic healing or TPK",
        "gm_open_questions": ("What actually repairs a harmed person or contaminated supply?",
                              "What was accomplished without assuming the Anointed Mission is over?",
                              "Which resources/wounds persisted between earlier encounters?"),
    },
}
MILESTONE_BEATS = (
    {"beat": "gate", "from_level": 1, "to_level": 2,
     "candidate": "The group independently substantiates the supply problem and establishes a path forward"},
    {"beat": "shrine", "from_level": 2, "to_level": 3,
     "candidate": "The group secures a meaningful way to confront the dangerous supply source"},
)
SESSION_FIELDS = (
    "session_id", "played_at", "gm_observation_ref", "player_choice_refs",
    "start_resource_state_ref", "end_resource_state_ref",
    "incoming_handoff_ref", "reviewed_level_sheet_ref",
    "recovery_and_pursuit_decision_ref", "native_evidence_refs",
)
BEAT_FIELDS = ("choice_ref", "alternative_ref", "gm_consequence_ref",
               "world_clock_ref", "resource_state_ref", "source_action_ref")
LEVEL_FIELDS = ("sheet_ref", "combat_choice_ref", "noncombat_choice_ref",
                "alternative_ref", "countercase_ref", "independent_review_ref")
OUTCOMES = ("nonhostile", "partial", "resolved", "withdrawn", "defeat",
            "bypassed", "unresolved")


def _count(n):
    if type(n) is not int or n not in SESSION_GROUPS:
        raise ValueError("Pilot requires exactly 3, 4 or 5 sessions")
    return n


def _source_inventory():
    entries = roster()  # independently rechecked structural source paths/digests
    if len(entries) != 12 or set(x["pairing"] for x in entries) != set(FOCUS_TASKS):
        raise AssertionError("The independent canonical twelve-Focus roster changed")
    if any(x.get("source_issues") for x in entries):
        raise ValueError("Unresolved source authenticity in canonical roster")
    return [{"pairing": row["pairing"],
             "source_fingerprints": deepcopy(row["source_fingerprints"])}
            for row in entries]


def plan(session_count=4):
    """Draft schedule, not observed sessions or preapproved level changes."""
    _count(session_count)
    if (set(NONCOMBAT_PLANS) != {"evidence","inspection","special"}
            or any(v not in PACKS for v in
                   ("soldier_gate","sentry_shrine_cold",
                    "sentry_shrine_prepared","hunter_forest"))
            or len(GM_BRIEFS) != 4):
        raise AssertionError("Original noncombat/combat source anchors changed")
    sessions = []
    for idx, beat_ids in enumerate(SESSION_GROUPS[session_count], 1):
        levels = {BEATS[b]["level"] for b in beat_ids}
        if len(levels) != 1:
            raise AssertionError("A planned session crosses an undeclared milestone")
        sessions.append({
            "session_number": idx, "target_start_level": levels.pop(),
            "beats": list(beat_ids),
            "gm_candidate_scene_briefs": [deepcopy(BEATS[b]) for b in beat_ids],
            "milestone_window_after": next(
                (m["to_level"] for m in MILESTONE_BEATS
                 if m["beat"] == beat_ids[-1]), None),
        })
    milestones = [{
        **deepcopy(m),
        "after_session_number": next(s["session_number"] for s in sessions
                                     if m["beat"] in s["beats"]),
        "gm_declaration_required": True,
        "automatically_awarded": False,
    } for m in MILESTONE_BEATS]
    return {
        "version": VERSION, "session_count": session_count,
        "sessions": sessions, "milestone_candidates": milestones,
        "source_native_combat_level_floor": 2,
        "source_combat_L1_gap": "L1 Soldier/Hunter/Sentry pack combat not sourced in G8/G7H/G7F; do not reuse L2 actors",
        "source_roster": _source_inventory(),
        "structural_focus_pairings": 12,
        "supported_spotlight_slots": 36,
        "unobserved_human_sessions": session_count,
        "human_session_certifications": 0,
        "independently_full_certified_focuses": 0,
        "strict_mvp_exits_met": 0,
        "status": STATUS,
    }


def blank_packet(session_count=4):
    """Blank external human/GM record. All C1–C7 receipts are initially absent."""
    p=plan(session_count)
    return {
        "version": VERSION,
        "plan_digest": canonical_digest(p),
        "session_count": session_count,
        "source_roster": deepcopy(p["source_roster"]),
        "report_author_ref": "",
        "sessions": [{
            "session_number": s["session_number"],
            "target_start_level": s["target_start_level"],
            "beat_ids": deepcopy(s["beats"]),
            "status": "UNOBSERVED",
            **{field: [] if field.endswith("_refs") else ""
               for field in SESSION_FIELDS},
            "beats": [{
                "beat": beat, "status": "UNOBSERVED", "outcome": None,
                **{field: "" for field in BEAT_FIELDS},
            } for beat in s["beats"]],
        } for s in p["sessions"]],
        "milestones": [{
            "beat": m["beat"], "from_level": m["from_level"],
            "to_level": m["to_level"],
            "after_session_number": m["after_session_number"],
            "status": "UNDECLARED", "actual_event_id": "",
            "gm_declaration_ref": "", "reviewed_level_sheet_ref": "",
        } for m in p["milestone_candidates"]],
        "focus_level_evidence": [{
            "pairing": entry["pairing"], "level": level,
            "status": "UNOBSERVED",
            **{field: "" for field in LEVEL_FIELDS},
        } for entry in p["source_roster"] for level in LEVELS],
        "status": STATUS,
        "human_sessions_certified": 0,
        "independent_focus_certifications": 0,
        "strict_mvp_exits_met": 0,
    }


def preflight(packet):
    """Validate provenance and sequencing of UNTRUSTED human references.

    Matching strings/references NEVER authenticate a human GM, session,
    rules legality, milestone award, resource continuity or C1–C7 acceptance.
    """
    if (type(packet) is not dict or type(packet.get("session_count")) is not int):
        raise ValueError("A versioned pilot intake object is required")
    template=blank_packet(packet["session_count"])
    if set(packet) != set(template):
        raise ValueError("Unexpected intake keys; cannot inject acceptance flags")
    for key in ("version","plan_digest","session_count","source_roster",
                "status","human_sessions_certified",
                "independent_focus_certifications","strict_mvp_exits_met"):
        if type(packet[key]) != type(template[key]) or packet[key]!=template[key]:
            raise ValueError("Reserved source/planning status changed: "+key)
    if type(packet["report_author_ref"]) is not str:
        raise ValueError("Author reference must be text")
    sessions=packet["sessions"]
    if type(sessions) is not list or len(sessions)!=len(template["sessions"]):
        raise ValueError("Cannot add, drop or reorder preauthored sessions")
    reported=[]
    for index, (entry, expected) in enumerate(zip(sessions, template["sessions"])):
        if (type(entry) is not dict or set(entry)!=set(expected)
                or any(type(entry[k])!=type(expected[k]) or entry[k]!=expected[k]
                       for k in ("session_number","target_start_level","beat_ids"))
                or entry["status"] not in ("UNOBSERVED","REPORTED")):
            raise ValueError("Forged session chronology")
        if type(entry["beats"]) is not list or len(entry["beats"])!=len(expected["beats"]):
            raise ValueError("Missing beat observation")
        for record, baseline in zip(entry["beats"],expected["beats"]):
            if (type(record) is not dict or set(record)!=set(baseline)
                    or record["beat"]!=baseline["beat"]
                    or record["status"] not in ("UNOBSERVED","REPORTED")):
                raise ValueError("Beat observations must follow source plan order")
            for key in BEAT_FIELDS:
                if type(record[key]) is not str:
                    raise ValueError("Beat reference is not text")
            if record["status"]=="REPORTED":
                if (entry["status"]!="REPORTED"
                        or record["outcome"] not in OUTCOMES
                        or any(not record[k].strip() for k in BEAT_FIELDS)):
                    raise ValueError("A claimed played beat needs player/GM/source/time receipts")
            elif record["outcome"] is not None or any(record[k] for k in BEAT_FIELDS):
                raise ValueError("Unobserved beat cannot assert an outcome")
        for key in SESSION_FIELDS:
            if type(entry[key])!=type(expected[key]):
                raise ValueError("Malformed session evidence: "+key)
        if any(type(x) is not str or not x.strip() for key in (
                "player_choice_refs","native_evidence_refs") for x in entry[key]):
            raise ValueError("Empty session player/native evidence reference")
        if entry["status"]=="REPORTED":
            required=tuple(k for k in SESSION_FIELDS if not k.endswith("_refs"))
            if (not packet["report_author_ref"].strip()
                    or any(not entry[k].strip() for k in required)
                    or not entry["player_choice_refs"]
                    or not entry["native_evidence_refs"]
                    or any(b["status"]!="REPORTED" for b in entry["beats"])
                    or (index>0 and not entry["incoming_handoff_ref"].strip())):
                raise ValueError("Reported session lacks GM, players, native receipts or resource handoff")
            reported.append(index)
        else:
            if (any(entry[k] for k in SESSION_FIELDS)
                    or any(b["status"]=="REPORTED" for b in entry["beats"])):
                raise ValueError("Unobserved session cannot carry implied played evidence")
    if reported!=list(range(len(reported))):
        raise ValueError("Session reports cannot skip earlier unobserved sessions")
    milestones=packet["milestones"]
    if type(milestones) is not list or len(milestones)!=2:
        raise ValueError("Exactly two distinct prospective group milestones")
    ids=set()
    for i,(actual,expected) in enumerate(zip(milestones,template["milestones"])):
        if (type(actual) is not dict or set(actual)!=set(expected)
                or any(type(actual[k])!=type(expected[k]) or actual[k]!=expected[k]
                       for k in ("beat","from_level","to_level","after_session_number"))
                or actual["status"] not in ("UNDECLARED","REPORTED")
                or any(type(actual[k]) is not str for k in
                       ("actual_event_id","gm_declaration_ref","reviewed_level_sheet_ref"))):
            raise ValueError("Milestone source/level/event chronology forged")
        if actual["status"]=="REPORTED":
            if (actual["after_session_number"]-1 not in reported
                    or any(not actual[k].strip() for k in
                           ("actual_event_id","gm_declaration_ref",
                            "reviewed_level_sheet_ref"))
                    or actual["actual_event_id"] in ids
                    or (i and milestones[0]["status"]!="REPORTED")):
                raise ValueError("Claimed GM milestone needs distinct chronological session and review")
            ids.add(actual["actual_event_id"])
        elif any(actual[k] for k in ("actual_event_id","gm_declaration_ref",
                                     "reviewed_level_sheet_ref")):
            raise ValueError("Undeclared milestone cannot contain an award")
    for index in reported:
        level=sessions[index]["target_start_level"]
        if level>1 and milestones[level-2]["status"]!="REPORTED":
            raise ValueError("Cannot report L2/L3 play before its claimed actual GM milestone")
    focus=packet["focus_level_evidence"]
    expected=template["focus_level_evidence"]
    if type(focus) is not list or len(focus)!=36:
        raise ValueError("Exactly 36 twelve-Focus L1-3 review slots")
    seen=set()
    for actual,baseline in zip(focus,expected):
        if (type(actual) is not dict or set(actual)!=set(baseline)
                or any(type(actual[k])!=type(baseline[k]) or actual[k]!=baseline[k]
                       for k in ("pairing","level"))
                or actual["status"] not in ("UNOBSERVED","REPORTED")):
            raise ValueError("Focus/level source lineage or receipt field forged")
        pair=(actual["pairing"],actual["level"])
        if pair in seen:
            raise ValueError("Duplicate Focus/level record")
        seen.add(pair)
        if any(type(actual[k]) is not str for k in LEVEL_FIELDS):
            raise ValueError("Focus receipt reference must be text")
        if actual["status"]=="REPORTED":
            if (actual["level"] not in {sessions[i]["target_start_level"] for i in reported}
                    or any(not actual[k].strip() for k in LEVEL_FIELDS)):
                raise ValueError("Reported Focus evidence needs real session level and all C1-C6 refs")
        elif any(actual[k] for k in LEVEL_FIELDS):
            raise ValueError("Cannot supply certificates on an unobserved Focus/level")
    return {
        "candidate_references_well_formed": True,
        "reported_session_references": len(reported),
        "reported_milestone_references": len(ids),
        "reported_focus_level_references": sum(r["status"]=="REPORTED" for r in focus),
        "externally_authenticated_gm_sessions": 0,
        "independently_verified_milestones": 0,
        "independently_full_certified_focuses": 0,
        "strict_mvp_exits_met": 0, "status": STATUS,
        "caution": "All supplied refs are UNTRUSTED; no external identity, action, resources, award or reviewer authenticated",
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sessions",type=int,choices=tuple(SESSION_GROUPS),default=4)
    ap.add_argument("--blank-intake",action="store_true")
    ap.add_argument("--check",type=str,metavar="JSON_PATH")
    args=ap.parse_args()
    if args.blank_intake and args.check:
        ap.error("Choose blank template or check, not both")
    if args.check:
        with open(args.check,encoding="utf-8") as f:
            value=preflight(json.load(f))
    elif args.blank_intake:
        value=blank_packet(args.sessions)
    else:
        value=plan(args.sessions)
    print(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
