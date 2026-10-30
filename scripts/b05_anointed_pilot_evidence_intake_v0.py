"""B04/B05 Anointed human-pilot evidence intake v0.

Capture *reported* GM/player decisions for a restricted Restoration pilot.
This is an untrusted intake validator and source-identity inventory, not a
native combat replay, GM authentication or independent Focus certificate.
"""
import argparse
from datetime import date
from hashlib import sha256
import json
from pathlib import Path

from scripts.b06_encounter_state_v0 import party_actor

VERSION="B04-B05-Anointed-Field-Pilot-Intake-v0"
FOCUSES={"High":"AH","Medium":"AM","Low":"AL"}
LEVELS=(1,2,3)
DOMAINS=("combat","exploration","mission","advancement")
ALLOWED_EVIDENCE=("human_notes","table_log","native_trace_reference")
UNRESOLVED=(
    "Independent character-sheet reviewer and level-step approval",
    "Genuine player-selected alternatives and GM-observed outcome review",
    "Contested beneficial +8 Intrusion, consent and response decisions",
    "Representative encounter and noncombat objective diversity",
    "Three-to-five-session continuity and defensible calibration",
    "Externally authenticated GM adjudication and Mission-event context",
)


def canonical_digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(",",":"),
                              ensure_ascii=False).encode("utf-8")).hexdigest()


def source_actor(focus,level):
    if focus not in FOCUSES or type(level) is not int or level not in LEVELS:
        raise ValueError("Only authored L1–3 AH/AM/AL Restoration pilot")
    return party_actor(FOCUSES[focus],level,"anointed","party",occupied=((0,0),))


def pilot_slots():
    """Nine real source identities; each still needs separate human review."""
    return [{
        "focus":focus,"level":level,"source_role":FOCUSES[focus],
        "source_digest":source_actor(focus,level).source.digest,
        "status":"SOURCE_STRUCTURAL_ONLY",
        "human_play_certified":False,
        "independent_focus_certified":False,
    } for focus in FOCUSES for level in LEVELS]


def blank_template(*,focus,level):
    """An explicitly empty capture form, not a simulated human session."""
    actor=source_actor(focus,level)
    return {
        "version":VERSION,
        "session_id":"","session_date":"",
        "scenario_id":"","focus":focus,"level":level,
        "source_role":actor.source.source_id,
        "source_digest":actor.source.digest,
        "session_sequence":None,
        "evidence_kind":"human_notes",
        "gm_observation_reference":"",
        "player_decisions":[],
        "independent_review_reference":"",
        "notes_on_unresolved_rules":[],
    }


def validate_intake(packet):
    """Only validate structure/source provenance. Never attest played events.

    Even a matching hash or complete intake cannot independently prove
    live consent, a GM verdict, action legality or a meaningful choice.
    Those remain subject to external review, regardless of input claims.
    """
    if type(packet) is not dict or set(packet)!=set(blank_template(focus="High",level=1)):
        raise ValueError("Exact versioned intake fields required; no extra certification flags")
    if packet["version"]!=VERSION:
        raise ValueError("Unsupported pilot evidence version")
    actor=source_actor(packet["focus"],packet["level"])
    if (packet["source_role"]!=actor.source.source_id
            or packet["source_digest"]!=actor.source.digest):
        raise ValueError("Source actor identity/digest cannot be caller-invented")
    for key in ("session_id","scenario_id","gm_observation_reference"):
        v=packet[key]
        if not isinstance(v,str) or not v.strip() or len(v)>256:
            raise ValueError(f"External nonempty {key} required")
    try:
        if (not isinstance(packet["session_date"],str)
                or date.fromisoformat(packet["session_date"]).isoformat() !=
                packet["session_date"]):
            raise ValueError("Explicit ISO session date required")
    except (TypeError, ValueError) as exc:
        raise ValueError("Explicit ISO session date required") from exc
    if type(packet["session_sequence"]) is not int or packet["session_sequence"]<1:
        raise ValueError("Real positive session sequence required")
    if packet["evidence_kind"] not in ALLOWED_EVIDENCE:
        raise ValueError("Unknown external evidence kind")
    if (not isinstance(packet["player_decisions"],list)
            or len(packet["player_decisions"])>100):
        raise ValueError("List of at most 100 actual player decisions required")
    if (not isinstance(packet["independent_review_reference"],str)
            or len(packet["independent_review_reference"])>256):
        raise ValueError("Reviewer reference must be text, not a self-certified flag")
    if (not isinstance(packet["notes_on_unresolved_rules"],list)
            or any(not isinstance(v,str) or not v.strip() or len(v)>500
                   for v in packet["notes_on_unresolved_rules"])):
        raise ValueError("Unresolved rule notes must be nonempty strings")
    domains=[]
    for d in packet["player_decisions"]:
        if type(d) is not dict or set(d)!={
                "domain","decision_id","chosen_action","alternative_considered",
                "observed_consequence","source_event_reference"}:
            raise ValueError("Each decision needs a complete source-referenced choice record")
        if d["domain"] not in DOMAINS:
            raise ValueError("Only combat/exploration/mission/advancement domains")
        for field in ("decision_id","chosen_action","alternative_considered",
                      "observed_consequence","source_event_reference"):
            v=d[field]
            if not isinstance(v,str) or not v.strip() or len(v)>500:
                raise ValueError("Explicit human decision, alternative, outcome and ref required")
        if d["chosen_action"].strip()==d["alternative_considered"].strip():
            raise ValueError("Alternative must differ from chosen action")
        domains.append(d["domain"])
    if len({d["decision_id"] for d in packet["player_decisions"]})!=len(domains):
        raise ValueError("Decision IDs must be unique within a session")
    # Reporting counts is not proving agency. Never convert intake alone
    # into a gate exit, independently certified Focus or GM-verdict proof.
    normalized=json.loads(json.dumps(packet,ensure_ascii=False))
    return {
        "version":VERSION,
        "session_id":packet["session_id"],
        "focus":packet["focus"],"level":packet["level"],
        "source_role":packet["source_role"],
        "source_digest":packet["source_digest"],
        "reported_domains":sorted(set(domains)),
        "reported_choices":len(domains),
        "claimed_gm_reference":packet["gm_observation_reference"],
        "claimed_independent_review_reference":packet["independent_review_reference"],
        "intake_sha256":canonical_digest(normalized),
        "structural_intake_valid":True,
        "actual_human_play_verified":False,
        "gm_identity_authenticated":False,
        "native_receipts_verified":False,
        "independent_focus_certified":False,
        "mvp_exit_certified":False,
        "unresolved":list(UNRESOLVED),
    }


def aggregate_intakes(packets):
    """Group candidate forms by source role/level without certifying them."""
    if not isinstance(packets,list):
        raise ValueError("Expected list of independently supplied session intakes")
    if len(packets)>1000:
        raise ValueError("Limit intake assessment to 1000 submitted records")
    reviewed=[validate_intake(p) for p in packets]
    ids=[(p["session_id"],p["focus"],p["level"]) for p in reviewed]
    if len(ids)!=len(set(ids)):
        raise ValueError("Duplicate session/source pilot identity")
    slots=pilot_slots()
    index={(s["focus"],s["level"]):s for s in slots}
    for p in reviewed:
        key=p["focus"],p["level"]
        slot=index[key]
        slot.setdefault("reported_sessions",0)
        slot.setdefault("reported_domains",set())
        slot["reported_sessions"]+=1
        slot["reported_domains"].update(p["reported_domains"])
    for slot in slots:
        slot.setdefault("reported_sessions",0)
        slot.setdefault("reported_domains",set())
        slot["reported_domains"]=sorted(slot["reported_domains"])
    return {
        "version":VERSION,
        "slots":slots,
        "submitted_sessions":len(reviewed),
        "reported_complete_domain_sets":sum(
            set(x["reported_domains"])==set(DOMAINS) for x in slots),
        "independently_certified_focuses":0,
        "strict_mvp_exits":0,
        "externally_verified_sessions":0,
        "all_12_structural_builds_unaffected":True,
        "all_unresolved":list(UNRESOLVED),
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--template",action="store_true")
    group.add_argument("--check",type=Path)
    group.add_argument("--aggregate",type=Path)
    group.add_argument("--slots",action="store_true")
    parser.add_argument("--focus",choices=tuple(FOCUSES),default="High")
    parser.add_argument("--level",type=int,choices=LEVELS,default=1)
    args=parser.parse_args()
    if args.template: result=blank_template(focus=args.focus,level=args.level)
    elif args.slots:result=pilot_slots()
    else:
        source=json.loads((args.check or args.aggregate).read_text(encoding="utf-8"))
        result=validate_intake(source) if args.check else aggregate_intakes(source)
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
