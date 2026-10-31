"""B04/B07 twelve-Focus pilot roster and non-certifying evidence intake v0.

This inventories the actual #181/#182 independent structural source audit.
It neither validates third-party identity nor certifies human play, legal
combat, GM adjudication, two actual milestone awards, or any MVP exit.
"""
import argparse
from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path

from scripts.b04_b07_independent_progression_audit_v0 import audit

ROOT = Path(__file__).resolve().parents[1]
VERSION = "B04-B07-Twelve-Focus-Candidate-Intake-v0"
LEVELS = (1, 2, 3)
SOURCE_STATUS = "STRUCTURAL_SOURCE_ONLY"
CANDIDATE_STATUS = "CANDIDATE_UNVERIFIED"
LEVEL_EVIDENCE = (
    "character_sheet_ref", "independent_build_ledger_ref",
    "combat_chosen_action_ref", "combat_alternative_ref",
    "combat_consequence_ref", "combat_countercase_ref",
    "noncombat_chosen_action_ref", "noncombat_alternative_ref",
    "noncombat_consequence_ref", "noncombat_countercase_ref",
    "source_action_ledger_ref", "gm_observation_ref",
)
# An acceptance protocol is not itself a new set of Focus mechanics.
FOCUS_TASKS = {
    "Priest/High": {
        "identity": "Life preparation, Open Invocation and Open Prayer",
        "combat": "Prepared vs unprepared Full Action paid support, L3 Open Prayer; Ward/recovery under enemy pressure",
        "noncombat": "Preparation choice under exploration, poison/animal/plant constraints and real rest clock",
        "countercase": "Unprepared spell, exhausted VP, interruption or no legal target",
    },
    "Priest/Medium": {
        "identity": "Life Consecration, Reassign and L3 Intercession",
        "combat": "Guided Regeneration vs Vital Shelter host and ally protection; competing Reaction/Spent VP",
        "noncombat": "Prearranged single Consecration, lawful recipient/reassignment and real preparation time",
        "countercase": "Two simultaneous Consecrations, refilled finite shelter or unaffordable Intercession",
    },
    "Priest/Low": {
        "identity": "Life Chosen Devotion, one Rite and L3 Exaltation",
        "combat": "Actual self-Rite protection vs regeneration, held weapon/hand cost and paid attack",
        "noncombat": "Preparation and release/recast across exploration, toxin or recovery with host expiry",
        "countercase": "Second L1-3 Rite, wrong Exaltation host, unauthorized ally-target Chosen status",
    },
    "Scholar/High": {
        "identity": "Fire-led prepared Composite and legal native offense",
        "combat": "Source-priced ranged Flame vs legal Composite/defensive tradeoffs and responses",
        "noncombat": "Known/prepared repertoire and authored field utility, not phantom Formula authorization",
        "countercase": "Illegal composition mode or unavailable preparation/VP",
    },
    "Scholar/Medium": {
        "identity": "Earth-Life Inward boost and ordinary Sword offense",
        "combat": "Paid Inward utility/defense vs physical strike and native Opportunity/Guard window",
        "noncombat": "Technical known/prepared choice, genuine task check and resource tradeoff",
        "countercase": "Out-of-preparation technique, duplicated Inward or unearned off-turn action",
    },
    "Scholar/Low": {
        "identity": "Earth-Life prepared self Embodiment and L3 Initiative Talent",
        "combat": "Stone Body vs Guided self Embodiment, source Sword/Guard and lost reserve",
        "noncombat": "Prepared technical field action and eligible ten-minute/six-hour preparation",
        "countercase": "Two active Embodiments, free host-switch or Basic Heal cast while unprepared",
    },
    "Gifted/High": {
        "identity": "Joy Conjure Flame Projected Surge, Amplification and Instability",
        "combat": "Safe/risky legal Amplification, real paid Flame and lost Reach/target legality",
        "noncombat": "Emotion/Aspect link and a paid authored noncombat choice under a genuine window",
        "countercase": "Deepen plus Projection over AP, forged Emotion window, free/incorrect miscast",
    },
    "Gifted/Medium": {
        "identity": "Fear/Trust Ward Conduit Grade and retuning",
        "combat": "Committed Ward pulse, dormancy/reconduction vs real competing paid attack",
        "noncombat": "Link/Emotion routing and materially different field utility choice",
        "countercase": "Free second pulse, unsupported active Emotion, phantom VP refund",
    },
    "Gifted/Low": {
        "identity": "Anchored Emotion Rooted Guard and Unbound Step",
        "combat": "Native paid +1 self Guard/Dodge, one shared window Pulse and physical response",
        "noncombat": "Real difficult/cautious MP surcharge reduction and competing field choice",
        "countercase": "Free Guard, uncharged movement, duplicate pulse or illicit Break rearm",
    },
    "Anointed/High": {
        "identity": "Restoration Returning Step paid AP Projection, Destiny and Mission",
        "combat": "Source-paid Dagger vs 20-AP Projection to consenting other at legal Step",
        "noncombat": "Observed GM-recognized-or-denied Mission event with real six-hour clock",
        "countercase": "Invented free AP, automatic milestone Destiny or unconsented Intrusion success",
    },
    "Anointed/Medium": {
        "identity": "Restoration willing one-Vessel Investment and beneficiary Step",
        "combat": "24-AP Investment vs own paid Dagger, true recipient G4 Step",
        "noncombat": "Consent, Vessel reassignment and externally GM-judged Mission choices",
        "countercase": "Two Vessels, fabricated remote casting or same-turn 48 AP at L1",
    },
    "Anointed/Low": {
        "identity": "Restoration self Embodiment and own regeneration Step",
        "combat": "Own source 20-AP Sword strike vs genuine own-Step Returning Step",
        "noncombat": "Active/dormant bond, own six-hour clock and GM Mission alternatives",
        "countercase": "Remote ally heal, synthetic G0 Step, unearned Destiny/Authority",
    },
}


@lru_cache(maxsize=1)
def _source_roster():
    """Read independent live source findings once per process, not a self-cert."""
    report = audit()
    if (report["pairings_checked"], report["variants_checked"],
            report["level_snapshots_checked"]) != (12, 13, 39):
        raise ValueError("Unexpected structural source audit scope")
    if set(report["pairings"]) != set(FOCUS_TASKS):
        raise ValueError("Missing/extra canonical Archetype x Focus pairing")
    entries = []
    for pairing in sorted(FOCUS_TASKS):
        item = report["pairings"][pairing]
        paths = {item["source"]: item["source_sha256"]}
        if "build_record" in item:
            paths[item["build_record"]] = item["build_record_sha256"]
        if item["variants"] != (2 if pairing == "Priest/Low" else 1):
            raise ValueError("Unexpected Low Priest A/B variant accounting")
        for path, digest in paths.items():
            if (not (ROOT / path).is_file() or type(digest) is not str
                    or len(digest) != 64):
                raise ValueError("Unverifiable structural provenance: " + path)
        entries.append({
            "pairing": pairing, "levels": list(LEVELS),
            "structural_variants": item["variants"],
            "source_fingerprints": paths,
            "source_issues": deepcopy(item["issues"]),
            "identity": FOCUS_TASKS[pairing]["identity"],
            "combat_requirement": FOCUS_TASKS[pairing]["combat"],
            "noncombat_requirement": FOCUS_TASKS[pairing]["noncombat"],
            "countercase_requirement": FOCUS_TASKS[pairing]["countercase"],
            "source_status": SOURCE_STATUS,
            "independently_full_certified": False,
        })
    return entries


def roster():
    return deepcopy(_source_roster())


def blank_packet(pairing):
    row = next((r for r in _source_roster() if r["pairing"] == pairing), None)
    if row is None:
        raise ValueError("Unknown twelve-Focus pairing")
    return {
        "version": VERSION,
        "pairing": pairing,
        "source_fingerprints": deepcopy(row["source_fingerprints"]),
        "report_author_ref": "",
        "independent_reviewer_ref": "",
        "external_review_ref": "",
        "levels": [
            {"level": level, **{key: "" for key in LEVEL_EVIDENCE}}
            for level in LEVELS
        ],
        "milestones": [
            {"event_id": "", "from_level": level, "to_level": level+1,
             "gm_declared_event_ref": "", "reviewed_level_sheet_ref": ""}
            for level in (1, 2)
        ],
        "status": CANDIDATE_STATUS,
        "independently_full_certified": False,
        "strict_mvp_exits_met": 0,
    }


def preflight(packet):
    """Check candidate source/schema/references; NEVER authenticate evidence.

    Even valid strings, a different reviewer name, matching hashes and
    purported GM milestone refs may be entirely fabricated by a submitter.
    """
    if type(packet) is not dict or packet.get("pairing") not in FOCUS_TASKS:
        raise ValueError("Unknown pairing or packet")
    expected = blank_packet(packet["pairing"])
    if set(packet) != set(expected):
        raise ValueError("Unexpected packet fields or certification flags")
    for field in ("version", "pairing", "source_fingerprints", "status",
                  "independently_full_certified", "strict_mvp_exits_met"):
        if type(packet[field]) != type(expected[field]) or packet[field] != expected[field]:
            raise ValueError("Source or reserved non-certification field altered: " + field)
    for key in ("report_author_ref", "independent_reviewer_ref", "external_review_ref"):
        if type(packet[key]) is not str or not packet[key].strip():
            raise ValueError("Missing candidate reference: " + key)
    if packet["report_author_ref"] == packet["independent_reviewer_ref"]:
        raise ValueError("Reviewer must be distinct from reported author")
    levels = packet["levels"]
    if type(levels) is not list or len(levels) != 3:
        raise ValueError("Exactly three level receipts required")
    for index, entry in enumerate(levels):
        if type(entry) is not dict or set(entry) != set(expected["levels"][index]):
            raise ValueError("Missing or extra level evidence field")
        if type(entry["level"]) is not int or entry["level"] != LEVELS[index]:
            raise ValueError("Level must be 1, 2, then 3")
        for field in LEVEL_EVIDENCE:
            if type(entry[field]) is not str or not entry[field].strip():
                raise ValueError("Missing candidate L%d evidence: %s" % (index+1, field))
    milestones = packet["milestones"]
    if type(milestones) is not list or len(milestones) != 2:
        raise ValueError("Exactly two separate claimed GM milestones required")
    seen = set()
    for index, entry in enumerate(milestones):
        if type(entry) is not dict or set(entry) != set(expected["milestones"][index]):
            raise ValueError("Missing/extra milestone fields")
        for field in ("from_level", "to_level"):
            if type(entry[field]) is not int or entry[field] != expected["milestones"][index][field]:
                raise ValueError("Wrong milestone chronology")
        for field in ("event_id", "gm_declared_event_ref", "reviewed_level_sheet_ref"):
            if type(entry[field]) is not str or not entry[field].strip():
                raise ValueError("Missing candidate milestone evidence")
        if entry["event_id"] in seen:
            raise ValueError("Reused milestone event ID")
        seen.add(entry["event_id"])
    return {
        "pairing": packet["pairing"], "candidate_references_complete": True,
        "source_identity_matches": True,
        "externally_verified_sessions": 0,
        "independently_full_certified": False,
        "strict_mvp_exits_met": 0,
        "status": CANDIDATE_STATUS,
        "limitations": "Untrusted references; external reviewer/GM identity and native event legality not authenticated",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--roster", action="store_true")
    choice.add_argument("--template", choices=sorted(FOCUS_TASKS))
    choice.add_argument("--check", type=Path)
    args = parser.parse_args()
    if args.roster:
        out = {"version": VERSION, "focus_pairings": 12,
               "structural_variants": 13, "level_snapshots": 39,
               "independent_full_focus_certificates": 0,
               "strict_mvp_exits": 0, "roster": roster()}
    elif args.template:
        out = blank_packet(args.template)
    else:
        out = preflight(json.loads(args.check.read_text(encoding="utf-8")))
    print(json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
