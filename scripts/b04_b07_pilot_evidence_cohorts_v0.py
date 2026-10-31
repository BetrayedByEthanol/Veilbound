"""Flexible, multi-cohort L1-3 pilot evidence intake. All external refs are UNTRUSTED.

This is an alternative to the fixed schedule in the merged #190 illustrative
planner, not an importer of its session reports or an automatic certification.
"""
import argparse
from collections import defaultdict
from copy import deepcopy
import json

from scripts.b04_b07_twelve_focus_certification_protocol_v0 import FOCUS_TASKS, LEVELS, roster
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b04_b05_b06_b07_integrated_pilot_adventure_v0 import BEATS, OUTCOMES

VERSION = "B04-B07-Pilot-Cohort-Evidence-v0"
STATUS = "CANDIDATE_UNVERIFIED"
MAX_PLAYERS = 5
BEAT_ORDER = tuple(BEATS)
SCENE_FIELDS = ("scene_id", "beat", "level", "outcome", "choice_ref",
                "alternative_ref", "gm_consequence_ref", "source_action_ref",
                "resource_before_ref", "resource_after_ref", "world_clock_ref")
EVIDENCE_FIELDS = ("sheet_ref", "combat_scene_id", "combat_choice_ref",
                   "noncombat_scene_id", "noncombat_choice_ref", "alternative_ref",
                   "countercase_scene_id", "countercase_ref", "reviewer_ref")


def _text(value, label):
    if type(value) is not str or not value.strip():
        raise ValueError(f"Missing or invalid {label}")
    return value


def _shape(value, keys, label):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError(f"Invalid {label} fields")


def _sources():
    rows = roster()
    if len(rows) != 12 or {r["pairing"] for r in rows} != set(FOCUS_TASKS):
        raise AssertionError("Canonical Focus roster changed")
    if any(r.get("source_issues") for r in rows):
        raise ValueError("Unresolved original source issues")
    return {r["pairing"]: deepcopy(r["source_fingerprints"]) for r in rows}


def blank_packet(cohort_id="COHORT-1", pairings=("Priest/High",)):
    """Create a blank candidate; one source pairing is not one certified character."""
    _text(cohort_id, "cohort ID")
    src = _sources()
    if (type(pairings) not in (list, tuple) or not 1 <= len(pairings) <= MAX_PLAYERS
            or len(set(pairings)) != len(pairings) or any(p not in src for p in pairings)):
        raise ValueError("Provide 1-5 distinct real roster pairings")
    return {
        "version": VERSION, "source_roster_digest": canonical_digest(src),
        "cohorts": [{"cohort_id": cohort_id, "gm_ref": "", "report_author_ref": "",
                     "characters": [
                         {"character_id": f"PC-{i}", "pairing": p,
                          "source_fingerprints": src[p], "player_ref": ""}
                         for i, p in enumerate(pairings, 1)],
                     "sessions": [], "milestones": [], "focus_level_evidence": []}],
        "status": STATUS, "externally_authenticated_sessions": 0,
        "independently_verified_milestones": 0,
        "independently_certified_focuses": 0, "strict_mvp_exits_met": 0,
    }


def preflight(packet):
    """Check shape, source lineage, cross-cohort identity and event chronology.

    Source/GM/player/reviewer references are untrusted external assertions.
    Passing this function never checks human identity, legal rolls or awards.
    """
    src = _sources()
    _shape(packet, ("version", "source_roster_digest", "cohorts", "status",
                    "externally_authenticated_sessions", "independently_verified_milestones",
                    "independently_certified_focuses", "strict_mvp_exits_met"), "packet")
    expected = (VERSION, canonical_digest(src), STATUS, 0, 0, 0, 0)
    actual = tuple(packet[k] for k in ("version", "source_roster_digest", "status",
                                      "externally_authenticated_sessions",
                                      "independently_verified_milestones",
                                      "independently_certified_focuses", "strict_mvp_exits_met"))
    if any(type(a) != type(e) or a != e for a, e in zip(actual, expected)):
        raise ValueError("Cannot tamper with canonical source or certification status")
    if type(packet["cohorts"]) is not list or not packet["cohorts"]:
        raise ValueError("Supply at least one cohort")
    seen_cohorts, global_sessions, global_scenes, global_awards = set(), set(), set(), set()
    coverage = defaultdict(list)
    reported_sessions = reported_awards = 0
    for cohort in packet["cohorts"]:
        _shape(cohort, ("cohort_id", "gm_ref", "report_author_ref", "characters",
                        "sessions", "milestones", "focus_level_evidence"), "cohort")
        cid = _text(cohort["cohort_id"], "cohort ID")
        if cid in seen_cohorts:
            raise ValueError("Duplicate cohort ID")
        seen_cohorts.add(cid)
        if type(cohort["characters"]) is not list or not 1 <= len(cohort["characters"]) <= MAX_PLAYERS:
            raise ValueError("Cohort must contain 1-5 characters, not a 12-PC party")
        characters = {}
        for actor in cohort["characters"]:
            _shape(actor, ("character_id", "pairing", "source_fingerprints", "player_ref"), "character")
            actor_id = _text(actor["character_id"], "character ID")
            if actor_id in characters or actor["pairing"] not in src or actor["source_fingerprints"] != src[actor["pairing"]]:
                raise ValueError("Duplicate character or forged source fingerprints")
            if type(actor["player_ref"]) is not str:
                raise ValueError("Player reference must be text")
            characters[actor_id] = actor
        sessions = cohort["sessions"]
        if type(sessions) is not list or len(sessions) > 5:
            raise ValueError("At most five reported sessions per cohort")
        if sessions and (not _text(cohort["gm_ref"], "GM") or
                         not _text(cohort["report_author_ref"], "report author") or
                         any(not _text(a["player_ref"], "player") for a in characters.values())):
            raise ValueError("Reported sessions require cohort GM, author and players")
        elif type(cohort["gm_ref"]) is not str or type(cohort["report_author_ref"]) is not str:
            raise ValueError("GM/author reference must be text")
        scenes, scene_sequence, scene_levels = {}, [], {}
        previous_end = None
        last_beat = -1
        for session_index, session in enumerate(sessions):
            _shape(session, ("session_id", "played_at", "incoming_handoff_ref",
                             "start_resource_state_ref", "end_resource_state_ref",
                             "inter_session_transition_ref", "scenes"), "session")
            sid = _text(session["session_id"], "session ID")
            if sid in global_sessions:
                raise ValueError("Session ID reused across cohorts")
            global_sessions.add(sid)
            _text(session["played_at"], "played_at")
            for key in ("start_resource_state_ref", "end_resource_state_ref"):
                _text(session[key], key)
            if type(session["incoming_handoff_ref"]) is not str:
                raise ValueError("Malformed handoff")
            if type(session["inter_session_transition_ref"]) is not str:
                raise ValueError("Transition reference must be text")
            if session_index == 0:
                if session["inter_session_transition_ref"]:
                    raise ValueError("First session cannot claim inter-session transitions")
                if session["incoming_handoff_ref"]:
                    raise ValueError("First session cannot have prior cohort handoff")
            elif session["incoming_handoff_ref"] != previous_end:
                raise ValueError("Resource handoff must bind the previous session ending")
            elif session["start_resource_state_ref"] != previous_end and not session["inter_session_transition_ref"].strip():
                raise ValueError("Changed inter-session state needs a source-paid transition receipt")
            previous_end = session["end_resource_state_ref"]
            if type(session["scenes"]) is not list or not session["scenes"]:
                raise ValueError("Reported session needs at least one scene")
            for scene in session["scenes"]:
                _shape(scene, SCENE_FIELDS, "scene")
                scene_id = _text(scene["scene_id"], "scene ID")
                if scene_id in global_scenes:
                    raise ValueError("Scene ID reused across cohorts")
                global_scenes.add(scene_id)
                beat = scene["beat"]
                if beat not in BEAT_ORDER or BEAT_ORDER.index(beat) < last_beat:
                    raise ValueError("Scenes must preserve the authored story-beat order")
                last_beat = BEAT_ORDER.index(beat)
                if type(scene["level"]) is not int or scene["level"] not in LEVELS:
                    raise ValueError("Invalid scene level")
                if scene["outcome"] not in OUTCOMES:
                    raise ValueError("Unrecognized GM scene outcome")
                for key in SCENE_FIELDS[4:]:
                    _text(scene[key], key)
                scenes[scene_id] = (session_index, len(scene_sequence))
                scene_sequence.append(scene_id)
                scene_levels[scene_id] = scene["level"]
            reported_sessions += 1
        if type(cohort["milestones"]) is not list or len(cohort["milestones"]) > 2:
            raise ValueError("At most two genuine GM events per cohort")
        awards = {}
        prior_position = -1
        for i, event in enumerate(cohort["milestones"]):
            _shape(event, ("event_id", "after_scene_id", "from_level", "to_level",
                           "gm_declaration_ref", "story_achievement_ref", "reviewed_sheets"), "milestone")
            eid = _text(event["event_id"], "GM event ID")
            anchor = _text(event["after_scene_id"], "event scene anchor")
            if eid in global_awards or anchor not in scenes:
                raise ValueError("Duplicate award or nonexistent cohort scene")
            global_awards.add(eid)
            pos = scenes[anchor][1]
            if (pos <= prior_position or type(event["from_level"]) is not int
                    or type(event["to_level"]) is not int or
                    (event["from_level"], event["to_level"]) != (i+1, i+2)):
                raise ValueError("Awards must be distinct, sequential L1->L2->L3 events")
            prior_position = pos
            _text(event["gm_declaration_ref"], "GM declaration")
            _text(event["story_achievement_ref"], "group-story significance")
            if type(event["reviewed_sheets"]) is not list or len(event["reviewed_sheets"]) != len(characters):
                raise ValueError("Each actual participant requires a reviewed level sheet")
            reviewed = set()
            for sheet in event["reviewed_sheets"]:
                _shape(sheet, ("character_id", "sheet_ref", "reviewer_ref"), "award level sheet")
                char = _text(sheet["character_id"], "award character")
                if char not in characters or char in reviewed:
                    raise ValueError("Missing, reused, or foreign level sheet")
                reviewed.add(char)
                _text(sheet["sheet_ref"], "new level sheet")
                _text(sheet["reviewer_ref"], "independent level reviewer")
            awards[anchor] = i+1
            reported_awards += 1
        current_level = 1
        for scene_id in scene_sequence:
            if scene_levels[scene_id] != current_level:
                raise ValueError("Scene level skips or precedes a GM-declared award")
            if scene_id in awards:
                current_level += 1
        evidence = cohort["focus_level_evidence"]
        if type(evidence) is not list:
            raise ValueError("Focus-level evidence must be a list")
        seen_slots = set()
        for row in evidence:
            _shape(row, ("character_id", "level", *EVIDENCE_FIELDS), "Focus-level evidence")
            char_id = _text(row["character_id"], "evidence character")
            if char_id not in characters or type(row["level"]) is not int or row["level"] not in LEVELS:
                raise ValueError("Foreign character or invalid evidence level")
            key = (char_id, row["level"])
            if key in seen_slots:
                raise ValueError("Duplicate evidence level within character")
            seen_slots.add(key)
            for field in EVIDENCE_FIELDS:
                _text(row[field], field)
            for field in ("combat_scene_id", "noncombat_scene_id", "countercase_scene_id"):
                if row[field] not in scene_levels or scene_levels[row[field]] != row["level"]:
                    raise ValueError("Evidence refers to foreign scene or wrong level")
            pair = characters[char_id]["pairing"]
            coverage[(pair, row["level"])].append({"cohort_id": cid, "character_id": char_id})
    return {
        "candidate_references_well_formed": True,
        "reported_cohorts": len(seen_cohorts), "reported_session_references": reported_sessions,
        "reported_milestone_references": reported_awards,
        "candidate_unique_focus_level_slots": len(coverage),
        "candidate_focus_level_slots": [
            {"pairing": pair, "level": level, "participants": participants}
            for (pair, level), participants in sorted(coverage.items())],
        "externally_authenticated_gm_sessions": 0,
        "independently_verified_milestones": 0,
        "independently_full_certified_focuses": 0, "strict_mvp_exits_met": 0,
        "status": STATUS,
        "caution": "Cross-cohort references are only syntactically linked; no person, action, source resource or GM event was independently authenticated",
    }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--blank-cohort", metavar="ID")
    cli.add_argument("--pairing", action="append", default=[])
    cli.add_argument("--check", metavar="PATH")
    args = cli.parse_args()
    if bool(args.blank_cohort) == bool(args.check):
        cli.error("Choose exactly one of --blank-cohort and --check")
    if args.check:
        with open(args.check, encoding="utf-8") as stream:
            result = preflight(json.load(stream))
    else:
        result = blank_packet(args.blank_cohort, args.pairing or ("Priest/High",))
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
