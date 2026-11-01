"""B04/B06/B07: source-linked, NON-CERTIFYING human pilot readiness register.

A bounded G0/G8 author fixture and structural roster are inputs, not human
session testimony. This creates repeatable C1-C7 obligations, evidence
assignments and gate gaps; no populated string can award a certificate.
"""
import argparse
from copy import deepcopy
import json

from scripts.b04_b07_twelve_focus_certification_protocol_v0 import (
    FOCUS_TASKS, LEVELS, roster, blank_packet as focus_blank,
)
from scripts.b04_b07_independent_progression_audit_v0 import audit
from scripts.b04_b07_pilot_evidence_cohorts_v0 import (
    blank_packet as cohort_blank,
)
from scripts.b04_b05_b06_b07_integrated_pilot_adventure_v0 import (
    BEATS, plan, SESSION_GROUPS,
)
from scripts.b04_b06_b07_integrated_milestone_persistent_party_v0 import run
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION = "B04-B06-B07-Persistent-Adventure-Acceptance-Readiness-v0"
STATUS = "EXTERNAL_PLAY_AND_INDEPENDENT_REVIEW_REQUIRED"
GATES = (
    ("Create", "12 independently reviewed complete L1-L3 Focus lines"),
    ("Act", "meaningful source-legal combat AND noncombat player choices at each level"),
    ("Resolve", "complete representative native/GM combat, defenses, wounds and aftermath"),
    ("Advance", "two distinct actual GM story awards and reviewed sheet/resource changes"),
    ("Challenge", "one runnable 3-5-session exploration, social and varied challenge arc"),
    ("Observe", "attributable human play, independent review, calibrated outcomes/denominators"),
)
CRITERIA = {
    "C1": "Exact source legal complete character sheet and purchase/knowledge ledger",
    "C2": "Reviewed advancement, earned vs saved awards and conserved resources",
    "C3": "Human-selected legal combat action, alternative, cost and outcome",
    "C4": "Human-selected legal noncombat choice, alternative, GM time/consequence",
    "C5": "Source countercase or genuine weakness, limits and adverse consequence",
    "C6": "Independent reviewer, raw session/GM receipts and provenance",
    "C7": "Two distinct actual GM-declared group-story L2 and L3 awards",
}
# Three separate playable cohorts, four characters each, instead of 12 PCs
# in one illegal or artificially easy combat. These are *scheduling proposals*.
COHORTS = {
    "COHORT-ALPHA": (
        "Priest/Low", "Scholar/High", "Gifted/High", "Anointed/Medium"),
    "COHORT-BETA": (
        "Priest/High", "Scholar/Medium", "Gifted/Low", "Anointed/High"),
    "COHORT-GAMMA": (
        "Priest/Medium", "Scholar/Low", "Gifted/Medium", "Anointed/Low"),
}
# These are the only ORIGINAL #196 fixture characters. A/B are two
# *physical proxy builds of ONE Low Priest Focus*, not a full selected Priest.
FIXTURE = {
    "Priest/Low": {
        1: {"noncombat": ("vanguard: source ordinary Medicine diagnosis",),
            "combat": (), "advancement": ("authored Gate L1-L2 candidate",)},
        2: {"noncombat": (),
            "combat": ("vanguard/guardian: G8 Soldier withdrawal and source harm; physical A/B proxy",),
            "advancement": ("authored Shrine L2-L3 candidate",)},
        3: {"noncombat": (),
            "combat": ("vanguard/guardian: G8 cold Sentry source actions; physical A/B proxy",),
            "advancement": ()},
    },
    "Scholar/High": {
        1: {"noncombat": ("scholar: source survey and public record checks",),
            "combat": (), "advancement": ("authored Gate L1-L2 candidate",)},
        2: {"noncombat": (),
            "combat": ("scholar: native G8 Soldier withdrawal; no player-selected Fire role action",),
            "advancement": ("authored Shrine L2-L3 candidate",)},
        3: {"noncombat": (),
            "combat": ("scholar: native G8 Sentry Flame action",),
            "advancement": ()},
    },
}
REVIEW_STEPS = (
    "Before play: GM and independent reviewer agree selected complete legal L1 sheet, source SHA and countercases; record actual roster IDs",
    "During play: record player's chosen and rejected actions, exact AP/VP/MP/Guard/target/roll, G4.2 time, observed GM rulings and alternative",
    "After each scene: preserve native action and independent GM notes, end HP/Vigor/VP/wounds/arrows, toxins, pursuit and any lawful inter-session transition",
    "At each GM milestone: record actual distinct group-story event, before/after source sheet, earned/saved Talents/Training, no phantom refill or automatic Destiny",
    "For each L1, L2, L3 Focus: capture combat and noncombat player decisions, source-bound countercase, independent reviewer verdict and reason for any unavailable action",
    "After 3-5 sessions: independently reconcile identities, sessions, wound/clock history, negative paths, repeated encounters and balance denominators; adjudicate gates separately",
)
TASK_IDS = ("C1","C2","C3","C4","C5","C6","C7")
INTAKE = {
    "cohorts": "scripts/b04_b07_pilot_evidence_cohorts_v0.py",
    "individual_focus": "scripts/b04_b07_twelve_focus_certification_protocol_v0.py",
    "adventure": "scripts/b04_b05_b06_b07_integrated_pilot_adventure_v0.py",
    "structural_audit": "scripts/b04_b07_independent_progression_audit_v0.py",
    "bounded_native_chain": "scripts/b04_b06_b07_integrated_milestone_persistent_party_v0.py",
}


def cohort_templates():
    """Blank source-derived cohort forms; no claimed human choices or awards."""
    return [cohort_blank(cid, pairings)
            for cid,pairings in COHORTS.items()]


def _task(pairing, level, code, fixture):
    source=FOCUS_TASKS[pairing]
    base={
        "C1": f"Independently check full {pairing} L{level} source sheet; selected/saved Talents, training, repertoire, gear and AP/HP/Vigor/VP",
        "C2": (f"Verify L{level} starting ledger and previous GM award (if L2/3); no free recovery or illicit source benefit"),
        "C3": f"Observe L{level} real player combat decision: {source['combat']}; record alternative, paid native action and opposition",
        "C4": f"Observe L{level} real exploration/social decision: {source['noncombat']}; record source time, alternative and actual GM consequence",
        "C5": f"Reproduce or observe L{level} defining weakness: {source['countercase']}; link a source-legal negative receipt",
        "C6": f"Independent reviewer checks L{level} raw event, GM/player testimony, source hash, reviewer separation and session continuity",
        "C7": ("Record actual independent GM L1->L2 story milestone after a played scene"
               if level==1 else
               "Record actual independent GM L2->L3 story milestone after a later played scene"
               if level==2 else "Match both prior distinct real GM awards to the L3 sheet"),
    }
    available={
        "C3": list(fixture["combat"]), "C4": list(fixture["noncombat"]),
        "C7": list(fixture["advancement"]),
    }.get(code, [])
    return {
        "criterion":code, "requirement":CRITERIA[code],
        "gm_reviewer_action":base[code],
        "existing_machine_fixture":available,
        "machine_fixture_is_human_play":False,
        "independently_accepted":False,
        "status":"MISSING_AUTHENTICATED_EVIDENCE",
    }


def report():
    """Rebuild from current source files; never infer acceptance from a run."""
    source_audit=audit()
    rows=roster()
    if (source_audit["issues"] or len(rows)!=12
            or source_audit["variants_checked"]!=13
            or source_audit["level_snapshots_checked"]!=39
            or {r["pairing"] for r in rows}!=set(FOCUS_TASKS)
            or set(CRITERIA)!=set(TASK_IDS)):
        raise ValueError("Cannot issue a readiness register from unsound source roster")
    agenda=plan(4)
    if (set(BEATS)!=set(("supply","gate","forest","shrine","village"))
            or tuple(x["target_start_level"] for x in agenda["sessions"])
               != (1,2,2,3)
            or set(p for v in COHORTS.values() for p in v)!=set(FOCUS_TASKS)
            or sum(map(len,COHORTS.values()))!=12
            or any(not 1<=len(p)<=5 or len(set(p))!=len(p)
                   for p in COHORTS.values())):
        raise ValueError("Invalid authored pilot beat or cohort constraints")
    # Verify actual merged G0->G8 chain on each independent CI run. The
    # result is a fixture and deliberately cannot authenticate any human play.
    native=run()
    if (native["l2_outcome"],native["l3_outcome"],
            native["original_source_g8_terminals"])!=(
                "party_scene_withdrawal","sentry_defeat",2):
        raise ValueError("Merged native chain no longer authenticates original scenes")
    if (native["human_sessions"] or native["independently_certified_focuses"]
            or native["strict_mvp_exits_met"]):
        raise ValueError("Native author fixture must not invent certification")
    matrix=[]
    for row in rows:
        pairing=row["pairing"]
        fixture=FIXTURE.get(pairing,{})
        for level in LEVELS:
            bounded=fixture.get(level,{
                "combat":(),"noncombat":(),"advancement":()})
            matrix.append({
                "pairing":pairing, "level":level,
                "cohort_id":next(k for k,v in COHORTS.items() if pairing in v),
                "source_fingerprints":deepcopy(row["source_fingerprints"]),
                "structural_issues":deepcopy(row["source_issues"]),
                "structural_variants":row["structural_variants"],
                "focus_identity":row["identity"],
                "bounded_fixture_present":bool(any(bounded.values())),
                "complete_focus_native_play_verified":False,
                "tasks":[_task(pairing,level,code,bounded)
                         for code in TASK_IDS],
                "independent_reviewer_assigned":False,
                "genuine_gm_and_player_sessions_recorded":False,
                "certified":False,
            })
    if len(matrix)!=36 or any(len(m["tasks"])!=7 for m in matrix):
        raise AssertionError("Lost one of 36 level slots or C1-C7 obligations")
    return {
        "version":VERSION,"status":STATUS,
        "source_roster_digest":canonical_digest({
            x["pairing"]:x["source_fingerprints"] for x in rows}),
        "source_pairings":12,"structural_variants":13,
        "structural_level_snapshots":39,
        "focus_level_review_slots":36,
        "criteria_per_level":list(TASK_IDS),
        "unmet_independent_criterion_slots":252,
        "cohort_allocation":{k:list(v) for k,v in COHORTS.items()},
        "session_options":sorted(SESSION_GROUPS),
        "four_session_beats":[{"session":s["session_number"],
             "level":s["target_start_level"],"beats":s["beats"]}
            for s in agenda["sessions"]],
        "native_fixture":{
            "scope":"four source roles including two Low Priest physical proxies",
            "real_player_session":False,
            "l1_observed_by_fixture":["vanguard:source diagnosis",
                                      "scholar:survey and records"],
            "l2_combat":"G8 source Soldier withdrawal",
            "l3_combat":"G8 source cold Sentry victory",
            "l1_evidence_sha256":native["l1_ledger_sha256"],
            "l2_evidence_sha256":native["l2_ledger_sha256"],
            "l3_evidence_sha256":native["l3_ledger_sha256"],
            "authored_milestone_ids":[native["milestone_one"]["event_id"],
                                      native["milestone_two"]["event_id"]],
            "authored_awards_are_real_gm_declarations":False,
        },
        "review_matrix":matrix,
        "gate_status":[{"gate":name,"needed":description,"status":"OPEN",
             "independent_signoff":False} for name,description in GATES],
        "procedure":list(REVIEW_STEPS),
        "existing_input_tools":deepcopy(INTAKE),
        "full_focus_certificates":0,"human_sessions_verified":0,
        "actual_gm_milestones_verified":0,"mvp_exit_gates_closed":0,
        "original_blockers_closed":3,
        "warning":"Author fixtures, self-filled form references and hashes never authenticate people or confer acceptance",
    }


def focus_field_sheet(pairing):
    """Use original, separately versioned packet instead of another format."""
    if pairing not in FOCUS_TASKS:
        raise ValueError("Unknown source pairing")
    r=report()
    return {
        "version":VERSION,
        "status":STATUS,
        "pairing":pairing,
        "source_intake_template":focus_blank(pairing),
        "gm_and_reviewer_procedure":list(REVIEW_STEPS),
        "level_tasks":[row for row in r["review_matrix"]
                       if row["pairing"]==pairing],
        "independently_full_certified":False,
        "strict_mvp_exits_met":0,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument("--cohort-templates",action="store_true")
    mode.add_argument("--field-sheet",choices=sorted(FOCUS_TASKS))
    args=parser.parse_args()
    result=(cohort_templates() if args.cohort_templates else
            focus_field_sheet(args.field_sheet) if args.field_sheet else report())
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
