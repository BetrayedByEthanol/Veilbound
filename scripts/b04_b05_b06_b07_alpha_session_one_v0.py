"""Alpha Session 1 L1 supply/gate GM preparation and PRIVATE worksheet scaffold.

A useful authored session brief and local reference worksheet, NOT an alternate
Alpha evidence intake, a source combat resolver, an observed session or an
automatically accepted milestone. All personal evidence belongs in the
original first-cohort intake plus independently reviewed private primary files.
"""
import argparse
from copy import deepcopy
import json
import re

from scripts.b04_b05_b06_b07_alpha_pilot_handoff_v0 import (
    handoff, MECHANICAL_SOURCES,
)
from scripts.b04_b05_b06_b07_first_cohort_pilot_v0 import (
    blank_packet, COHORT_ID, PAIRINGS,
)
from scripts.b04_b05_b06_b07_integrated_pilot_adventure_v0 import (
    BEATS, SESSION_GROUPS,
)
from scripts.b04_b05_b06_alpha_l1_tactics_v0 import OPTIONS
from scripts.b04_b05_noncombat_scene_resolution_v0 import SCENES, DIFFICULTY
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION="B04-B05-B06-B07-Alpha-Session-1-GM-Execution-Packet-v0"
STAGES=("crossing","cache","gate_records","gate_hostility")
BEAT_OF={"crossing":"supply","cache":"supply",
         "gate_records":"gate","gate_hostility":"gate"}
STATE=("UNOBSERVED","SOURCE_REPORTED","SOURCE_BLOCKED")
MILESTONE_STATES=("NOT_DECLARED","GM_EVENT_REPORTED_UNVERIFIED")
REF_RE=re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
STAGE_FIELDS=("stage","beat","status","scene_ref","chosen_ref",
              "declined_alternative_ref","gm_consequence_ref",
              "source_action_ref","resource_before_ref",
              "resource_after_ref","clock_ref","outcome_ref",
              "unsupported_action_ref")
GM_PREP_FIELDS=(
    "gm_ref","session_ref","session_date_ref",
    "independent_reviewer_ref","table_safety_ref",
    "spoilage_truth_ref","ring_and_cache_truth_ref",
    "supply_route_map_ref","soldier_motive_and_terrain_ref",
    "log_keeper_truth_ref","source_legal_adjudication_plan_ref",
    "private_evidence_root_ref",
)
SOURCE_CARD=(
    {"stage":"crossing","beat":"supply",
     "prompt":"The herbal cache lies across a slick footbridge or a ford; ask who scouts, tests and crosses, and which slower route remains.",
     "source_actions":(
         "Agility plus genuinely trained Acrobatics at the narrow footbridge",
         "Awareness plus genuinely trained Navigation to survey the ford",
     ),
     "author_fixture":{"footbridge_target":DIFFICULTY[5],
                       "ford_target":DIFFICULTY[2],
                       "footbridge_seconds":SCENES["exploration"]["balance"]["time_seconds"],
                       "ford_seconds":SCENES["exploration"]["survey"]["time_seconds"],
                       "failure_detour_seconds":300},
     "guardrail":"Targets and seconds belong to the declared source example, not a universal terrain penalty. Failed approach can cost the authored detour; no automatic HP loss."},
    {"stage":"cache","beat":"supply",
     "prompt":"The cache contains a sample and an actually held-or-unattended marked ring. Ask what evidence players seek and what they deliberately leave untested.",
     "source_actions":(
         "Intellect plus actually learned Medicine to diagnose an ordinary spoiled herb sample",
         "Awareness observation of visible stains without automatically diagnosing their cause",
         "Known Universal Veil Inspection only on an eligible actually held item; 2 VP and a full action",
         "Scholar/High known Phantom Sound or Minor Telekinesis only after actual L1 source repertoire and target check",
     ),
     "author_fixture":{"diagnose_target":DIFFICULTY[2],
                       "diagnose_seconds":SCENES["investigation"]["diagnose"]["time_seconds"],
                       "observe_seconds":SCENES["investigation"]["observe"]["time_seconds"]},
     "guardrail":"A visible Life/Restoration Veil signature is not a true cure, function, causal link or consent. GM establishes actual spoilage and item truth before any check."},
    {"stage":"gate_records","beat":"gate",
     "prompt":"An ordinary Soldier questions passage; a neutral storekeeper holds the public supply log. Offer negotiation, proof, another witness or withdrawal.",
     "source_actions":(
         "Presence petition to the actual neutral storekeeper",
         "Intellect plus source-learned regional/era History to present a real local record precedent",
         "Medical-evidence argument only if the diagnosis actually succeeded and the GM prepared that contextual premise",
         "Source-legal Scholar Phantom Sound is a cue, never automatic persuasion or Soldier distraction",
     ),
     "author_fixture":{"petition_target":DIFFICULTY[2],
                       "petition_seconds":SCENES["social"]["petition"]["time_seconds"],
                       "document_target":DIFFICULTY[2],
                       "document_seconds":SCENES["social"]["document"]["time_seconds"],
                       "diagnosis_conditional_situational_bonus":2},
     "guardrail":"The +2 is a conditional authored neutral-NPC circumstance, not a universal Medicine-to-social rule. Refused access must leave a real alternative or consequence."},
    {"stage":"gate_hostility","beat":"gate",
     "prompt":"Combat is optional. If a real declaration turns the Soldier hostile, record positions, defense assignment, actual action and costs before rolling.",
     "source_actions":(
         "Genuine full Low Priest A/B source with chosen Rite or hold",
         "High Scholar source-paid Thrown Flame or hold",
         "High Gifted linked Joy/Flame or hold with real Instability if chosen",
         "Medium Anointed legal 24-AP Investment on one consenting recipient, or hold",
         "Original B06-EN-02 Soldier and native pre-roll Take Hit/Guard/Dodge if legal",
         "Original G1 cautious withdrawal only if the actual scene and movement support it",
     ),
     "author_fixture":{"native_defenses":list(OPTIONS["priest_defense"]),
                       "source_l1_reference":"scripts/b04_b05_b06_alpha_l1_tactics_v0.py",
                       "original_opponent":"B06-EN-02"},
     "guardrail":"The five scripted L1 policies do not implement arbitrary tactical choices, natural-20 confirmations, off-turn answers or custom layouts. Source-adjudicate the human choice or STOP; no compulsory fight, fictional hit or guaranteed exit."},
)
REVIEW_REF_MAP={
    "scene_ref":"scene_id (canonical nested first-cohort session scene)",
    "chosen_ref":"player_choice",
    "declined_alternative_ref":"player_choice",
    "gm_consequence_ref":"gm_adjudication",
    "source_action_ref":"source_action",
    "resource_before_ref":"resource_snapshot",
    "resource_after_ref":"resource_snapshot",
    "clock_ref":"clock_trace",
    "outcome_ref":"gm_adjudication (original observed outcome)",
    "unsupported_action_ref":"countercase or source action issue, independently assessed",
}


def brief():
    """Source-anchored printable GM cards, never a performed scene."""
    readiness=handoff()
    if tuple(SESSION_GROUPS[4][0])!=("supply","gate"):
        raise AssertionError("Source four-session opening beat drift")
    if tuple(BEATS)!=("supply","gate","forest","shrine","village"):
        raise AssertionError("Pilot adventure order changed")
    source=readiness["source_files"]
    return {
        "version":VERSION,"scope":"GM authored briefing, not real play",
        "cohort_id":COHORT_ID,"session_number":1,"target_level":1,
        "beats":["supply","gate"],
        "source_roster_digest":blank_packet()["source_roster_digest"],
        "mechanical_source_sha256":{
            n:source[n]["sha256"] for n in (
                "full_selected_low_priest","high_scholar",
                "high_gifted","medium_anointed","alpha_L1_tactical",
                "original_noncombat","gm_three_enemy_reference")},
        "role_spotlights":{
            "Priest/Low":"Select complete A/B with actual prepared Rite/hand/gear; Medicine if genuinely trained, held-item Inspection only if legal; G8 physical proxy alone is insufficient.",
            "Scholar/High":"Use actual prepared formula and legal ordinary History/observation; source-paid Flame or available repertoire only, no invented manipulation or automatic cue success.",
            "Gifted/High":"Declare linked Emotion/Aspect and paid source Flame or support; no free Instability bypass and no gifted scouting spell by implication.",
            "Anointed/Medium":"Confirm actual Restoration bond and single consenting Investment/Vessel; pay source AP and trigger benefit only at genuine recipient G4 Step; Mission is not automatic group Milestone.",
        },
        "gm_cards":deepcopy(SOURCE_CARD),
        "candidate_outcomes":[
            "Evidence established; gate log access negotiated",
            "Uncertain cause; documented alternative witness, route or delay",
            "Denied log access; record consequence and optional safe withdrawal",
            "Hostile source-legal scene resolved or blocked by unimplemented chosen action",
        ],
        "minimum_clock_and_resource_capture":[
            "actual scene start/end G4.2 world time and Recovery deadline",
            "actual L1 four-character source sheets, purchased/saved Talent and Training",
            "HP/Vigor, VP Available/Committed/Spent, weapons/ammunition, wounds, conditions",
            "every actual check face/Ability/Training/DC, conditional bonus and GM reason",
            "original AP/MP/Guard/Dodge/Reaction assignments, targets and G5/G4 receipts only if combat occurs",
            "choice, legal declined alternative, raw GM ruling and observed failure/aftermath",
            "no unexplained refill between cache and gate or automatically safe long rest",
        ],
        "gm_trust_questions":[
            "What actually spoiled the herbs, and which facts can the party discover?",
            "Is the marked ring held and is its Life/Restoration mark relevant or coincidental?",
            "Who holds the public log, what would persuade them and what survives refusal?",
            "Is the Soldier hostile, and if so what original geometry and source-legal responses exist?",
            "What alternative route remains after a failed bridge/cache/gate choice?",
            "Did the GM actually declare a meaningful group-story milestone? If not, L2 is unawarded.",
        ],
        "milestone_one":"possible genuine group story beat after supply/gate; GM verdict only, never auto-awarded",
        "privacy":"Store completed worksheet and raw material privately. Transfer actual refs to existing Alpha first-cohort intake with original manifest/hash validator.",
        "external_sessions_authenticated":0,
        "actual_milestones_authenticated":0,
        "independently_certified_focuses":0,"mvp_exits_accepted":0,
    }


def blank_worksheet():
    """Unobserved local planning aid. Not the first-cohort intake schema."""
    p=blank_packet()
    return {
        "version":VERSION,"cohort_id":COHORT_ID,
        "source_roster_digest":p["source_roster_digest"],
        "session_number":1,"level":1,"beats":["supply","gate"],
        "gm_prep":{k:"" for k in GM_PREP_FIELDS},
        "characters":[{"character_id":c["character_id"],
                       "pairing":c["pairing"],"selected_variant":"",
                       "l1_selected_sheet_ref":"","player_ref":"",
                       "starting_resources_ref":""}
                      for c in p["characters"]],
        "stages":[{"stage":s,"beat":BEAT_OF[s],
                   "status":"UNOBSERVED",
                   **{k:"" for k in STAGE_FIELDS[3:]}}
                  for s in STAGES],
        "end_session":{"final_resource_ref":"","world_clock_ref":"",
                       "outstanding_effects_ref":"","actual_next_session_handoff_ref":"",
                       "unresolved_source_issue_ref":""},
        "milestone_one":{"status":"NOT_DECLARED","gm_event_ref":"",
                         "group_story_achievement_ref":"",
                         "l2_source_review_refs":[]},
        "status":"UNOBSERVED_PRIVATE_WORKSHEET",
        "external_sessions_authenticated":0,
        "actual_milestones_authenticated":0,
        "independently_certified_focuses":0,"mvp_exits_accepted":0,
    }


def _ref(s,label,*,allow_empty=True):
    if type(s) is not str or (s and not REF_RE.fullmatch(s)) or (not allow_empty and not s):
        raise ValueError("Invalid private reference "+label)
    return s


def validate_worksheet(value):
    """Strict structural cross-check. Noncertifying EVEN if every ref is filled."""
    model=blank_worksheet()
    if type(value) is not dict or set(value)!=set(model):
        raise ValueError("Session 1 worksheet schema changed")
    for k in ("version","cohort_id","source_roster_digest","session_number",
              "level","beats","status","external_sessions_authenticated",
              "actual_milestones_authenticated","independently_certified_focuses",
              "mvp_exits_accepted"):
        if type(value[k])!=type(model[k]) or value[k]!=model[k]:
            raise ValueError("Cannot alter source, L1 chronology or acceptance flag: "+k)
    if type(value["gm_prep"]) is not dict or set(value["gm_prep"])!=set(GM_PREP_FIELDS):
        raise ValueError("Missing GM preparatory truth and safety fields")
    for k,v in value["gm_prep"].items():
        _ref(v,k)
    if type(value["characters"]) is not list or len(value["characters"])!=4:
        raise ValueError("Exactly original four Alpha characters")
    selected=set()
    for c,template in zip(value["characters"],model["characters"]):
        if type(c) is not dict or set(c)!=set(template) or any(
                c[k]!=template[k] for k in ("character_id","pairing")):
            raise ValueError("Cannot substitute historical G8 proxies or another cohort")
        variant=_ref(c["selected_variant"],"selected variant")
        # The unobserved first-cohort worksheet intentionally leaves A/B
        # unselected until the actual player decides. A reported L1 source
        # sheet still requires an explicit nonblank legal variant below.
        if variant not in (("","A","B") if c["pairing"]=="Priest/Low" else ("","default")):
            raise ValueError("Only original Low Priest A/B or other unchanged Focus")
        for key in ("l1_selected_sheet_ref","player_ref","starting_resources_ref"):
            _ref(c[key],key)
        if c["l1_selected_sheet_ref"] and (not variant or not c["player_ref"] or
                                           not c["starting_resources_ref"]):
            raise ValueError("Reported selected sheet needs actual selection/player/start state")
        if c["l1_selected_sheet_ref"]:
            if c["l1_selected_sheet_ref"] in selected:
                raise ValueError("Cannot reuse one sheet for two PCs")
            selected.add(c["l1_selected_sheet_ref"])
    if type(value["stages"]) is not list or len(value["stages"])!=len(STAGES):
        raise ValueError("Original crossing/cache/records/hostility cards required")
    seen=set()
    recorded=blocked=0
    for s,template in zip(value["stages"],model["stages"]):
        if type(s) is not dict or set(s)!=set(STAGE_FIELDS) or any(
                s[k]!=template[k] for k in ("stage","beat")):
            raise ValueError("Changed authored scene order or beat")
        state=s["status"]
        if state not in STATE or type(state) is not str:
            raise ValueError("Unrecognized source-observation state")
        for k in STAGE_FIELDS[3:]:
            _ref(s[k],k)
        if state=="UNOBSERVED":
            if any(s[k] for k in STAGE_FIELDS[3:]):
                raise ValueError("Unobserved stage cannot claim evidence")
        else:
            if not s["scene_ref"] or s["scene_ref"] in seen:
                raise ValueError("Real source scene needs unique original reference")
            required=("chosen_ref","declined_alternative_ref","gm_consequence_ref",
                      "source_action_ref","resource_before_ref","resource_after_ref",
                      "clock_ref","outcome_ref") if state=="SOURCE_REPORTED" else (
                          "unsupported_action_ref","gm_consequence_ref",
                          "resource_before_ref","clock_ref")
            if any(not s[k] for k in required):
                raise ValueError("Reported/blocked source stage missing primary references")
            if state=="SOURCE_REPORTED" and s["unsupported_action_ref"]:
                raise ValueError("Unresolved source action cannot be silently resolved")
            if state=="SOURCE_BLOCKED":
                blocked+=1
            else:
                recorded+=1
            seen.add(s["scene_ref"])
    if recorded:
        essential=("gm_ref","session_ref","session_date_ref",
                   "independent_reviewer_ref","table_safety_ref",
                   "source_legal_adjudication_plan_ref",
                   "private_evidence_root_ref")
        if any(not value["gm_prep"][key] for key in essential):
            raise ValueError("Reported Session 1 stages require real GM, safety, reviewer and private-evidence references")
        if any(not c["l1_selected_sheet_ref"] for c in value["characters"]):
            raise ValueError("Reported Session 1 stages require four actual reviewed L1 selections")
    end=value["end_session"]
    if type(end) is not dict or set(end)!=set(model["end_session"]):
        raise ValueError("Session end/handoff structure changed")
    for k,v in end.items():
        _ref(v,k)
    m=value["milestone_one"]
    if type(m) is not dict or set(m)!=set(model["milestone_one"]):
        raise ValueError("Milestone field shape changed")
    if m["status"] not in MILESTONE_STATES or type(m["status"]) is not str:
        raise ValueError("Unknown GM milestone status")
    for k in ("gm_event_ref","group_story_achievement_ref"):
        _ref(m[k],k)
    if type(m["l2_source_review_refs"]) is not list or any(
            not _ref(x,"L2 reviewed sheet",allow_empty=False)
            for x in m["l2_source_review_refs"]):
        raise ValueError("Invalid L2 source sheet review refs")
    if len(set(m["l2_source_review_refs"]))!=len(m["l2_source_review_refs"]):
        raise ValueError("Duplicate L2 source sheet review")
    if m["status"]=="NOT_DECLARED":
        if (m["gm_event_ref"] or m["group_story_achievement_ref"]
                or m["l2_source_review_refs"]):
            raise ValueError("Undeclared milestone cannot claim level sheets or award")
    elif (not m["gm_event_ref"] or not m["group_story_achievement_ref"]
          or len(m["l2_source_review_refs"])!=4 or not any(
              s["status"]=="SOURCE_REPORTED" and s["beat"]=="gate"
              for s in value["stages"])):
        raise ValueError("Claimed GM gate milestone lacks evidence or four new sheet reviews")
    return {
        "version":VERSION,"cohort_id":COHORT_ID,
        "status":"UNTRUSTED_CANDIDATE_REFERENCE_PREFLIGHT_ONLY",
        "original_worksheet_unobserved":not(recorded or blocked or
                                            any(value["gm_prep"].values()) or
                                            any(x["l1_selected_sheet_ref"]
                                                for x in value["characters"])),
        "source_reported_stage_refs":recorded,
        "source_blocked_stage_refs":blocked,
        "candidate_milestone_refs":int(m["status"]!="NOT_DECLARED"),
        "possible_current_level":1,
        "can_export_to_canonical_alpha_intake_only_after_external_review":True,
        "reference_mapping":deepcopy(REVIEW_REF_MAP),
        "external_sessions_authenticated":0,
        "actual_milestones_authenticated":0,
        "independently_certified_focuses":0,
        "mvp_exits_accepted":0,
        "warning":"References and source-legal examples do not authenticate participants, rolls, GM decisions, level-up or reviewer findings.",
    }


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    group=cli.add_mutually_exclusive_group()
    group.add_argument("--blank",action="store_true")
    group.add_argument("--check",metavar="WORKSHEET")
    args=cli.parse_args()
    if args.blank:
        result=blank_worksheet()
    elif args.check:
        with open(args.check,encoding="utf-8") as stream:
            result=validate_worksheet(json.load(stream))
    else:
        result=brief()
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
