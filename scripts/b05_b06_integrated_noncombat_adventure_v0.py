"""B05/B06 three linked GM-fixture noncombat scenes with one native G0/G4.2 history.

A bounded pilot adventure *segment* rather than a full 3-5-session campaign.
Unlike disconnected earlier witnesses, all checks, action payments, evidence
and delays use ONE sourced character, ONE WorldClock and ONE G0 event ledger.
Narrative conditions are explicit author-authored GM premises, not real GM
verdicts or source-authorized universal bonuses or advance awards.
"""
import argparse
import json

from scripts.b04_b05_noncombat_scene_resolution_v0 import (
    SCENES, DIFFICULTY, ROLES, _character,
)
from scripts.b04_b05_focus_noncombat_technique_integration_v0 import (
    _authorized, TECHNIQUES,
)
from scripts.b06_damage_v0 import DamageState
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

PLANS = ("evidence", "inspection", "special")
SPECIAL = {"Priest/High": ("rapport",),
           "Scholar/High": ("telekinesis", "sound"),
           "Scholar/Medium": ("telekinesis",)}
DETOUR_SECONDS = 300  # GM-fixture consequence, NOT a universal failure rule
STATUS = "INTEGRATED_AUTHOR_GM_FIXTURE_NOT_HUMAN_PILOT"


def _roll(e, abilities, disciplines, *, scene, domain, approach, face,
          situational=0, training_override=None, target_override=None):
    """Same canonical d20/Ability/narrow Training arithmetic as #186.

    Do not create Turn AP costs for exploration checks or NPC influence rules.
    """
    if type(face) is not int or not 1 <= face <= 20:
        raise ValueError("Explicit d20 face must be integer 1..20")
    if type(situational) is not int or situational not in (0, 1, 2):
        raise ValueError("Only named author-fixture situational advantages")
    if training_override is not None:
        ability_name, training = training_override
        target = target_override
    else:
        spec = SCENES[domain][approach]
        ability_name, training = spec["ability"], spec["training"]
        target = DIFFICULTY[spec["target_modifier"]]
    if target not in DIFFICULTY.values():
        raise ValueError("Only original canonical core-check difficulty ladder")
    rank = disciplines.get(training, 0) if training is not None else 0
    if type(rank) is not int or not 0 <= rank <= 2:
        raise ValueError("Learned Discipline rank must be sourced and legal")
    total = face + abilities[ability_name] + rank + situational
    success = total >= target
    receipt = {
        "scene": scene, "approach": approach, "ability": ability_name,
        "ability_modifier": abilities[ability_name],
        "training": training if rank else None, "training_rank": rank,
        "face": face, "situational": situational,
        "total": total, "target": target, "success": success,
        "gm_fixture_only": True,
    }
    e.log("b05_b06_adventure_core_check", **receipt)
    return receipt


def _time(e, seconds, *, cause):
    if type(seconds) is not int or not 0 <= seconds < 21600:
        raise ValueError("No unauthored six-hour scene time")
    if e.g4.clock.mode != "exploration":
        raise AssertionError("Only native exploration can advance actual seconds")
    start = e.g4.clock.world_seconds
    e.g4.advance_exploration(seconds)
    e.log("b05_b06_adventure_elapsed", cause=cause, start=start,
          end=e.g4.clock.world_seconds, seconds=seconds)


def _cast(e, pairing, level, technique, *, discount=False):
    """Only the exact four pre-vetted #187 fixture targets and effects.

    Native G0 AP/VP is retained in the same encounter and G4.2 crosses a
    genuine initiative/exploration boundary. Does not manufacture seconds
    from turns or a real listener/animal/guard response.
    """
    _authorized(pairing, level, technique)
    if discount:
        raise ValueError("No arbitrary or repeatable Talent discount in this adventure")
    a = e.actors["pilot"]
    cost = 1 if technique == "sound" else 2
    if a.vp_available < cost:
        raise ValueError("Source actor lacks enough Available VP")
    if e.g4.clock.mode != "exploration" or e.current is not None:
        raise ValueError("Not at a valid between-scenes exploration boundary")
    e.g4.clock.enter_initiative()
    e.begin_round()
    e.start_turn("pilot", regen_choice=RegenerationChoice())
    action = "full" if technique == "inspection" else "projection"
    ap = e.spend_ap("pilot", action, label="b05_b06_adventure_" + technique)
    e.spend_vp("pilot", cost, mode="spent",
               label="b05_b06_adventure_" + technique)
    # Exact source-limited observation for a fully eligible fixture target.
    if technique == "inspection":
        effect = {
            "held_item": "supply_cache_ring",
            "observable_pillar": "Life", "observable_aspect": "Restoration",
            "effect_function_disclosed": False, "concealed_read": False,
        }
    elif technique == "telekinesis":
        effect = {
            "loose_mundane_object_kg": 3, "occupied_volume_dm3": 3,
            "max_dimension_m": 0.4, "initial_direct_range_squares": 4,
            "declared_clear_route_squares": 2, "object_retrieved": True,
            "unwilling_holder_resisted": False, "damage": 0,
        }
    elif technique == "sound":
        effect = {
            "fixed_source_square_visible": True,
            "nonverbal_single_knock": True, "duration_at_most_seconds": 2,
            "npc_attention_forced": False, "npc_cooperation": "GM_UNRESOLVED",
        }
    elif technique == "rapport":
        effect = {
            "animal_ordinary_wary_kg": 12,
            "external_peaceful_cues": True,
            "first_qualifying_check_bonus_pending": 2,
            "vc0_duration_minutes": 10,
            "animal_compelled": False,
            "animal_decision": "GM_UNRESOLVED",
        }
    else:
        raise AssertionError("Only source-authorized named techniques")
    e.log("b05_b06_adventure_technique_application", actor="pilot",
          technique=TECHNIQUES[technique], cost_vp=cost, ap_spent=ap,
          action=action, observed=effect, author_fixture=True)
    e.end_turn()
    e.g4.clock.leave_initiative()
    e.check()
    return {"technique": TECHNIQUES[technique], "ap_spent": ap,
            "vp_spent": cost, "effect": effect,
            "world_seconds_at_application": e.g4.clock.world_seconds}


def play(pairing, level, plan="evidence", *, faces=(12, 12, 12, 12),
         low_variant="A"):
    if type(pairing) is not str or pairing not in ROLES:
        raise ValueError("Only original twelve Focus pairings")
    if type(level) is not int or level not in (1, 2, 3):
        raise ValueError("Only authenticated L1-3 characters")
    if type(plan) is not str or plan not in PLANS:
        raise ValueError("Only named original adventure decision plans")
    if type(faces) not in (tuple, list) or len(faces) != 4 or any(
            type(f) is not int or not 1 <= f <= 20 for f in faces):
        raise ValueError("Four separately declared d20 faces are required")
    if pairing != "Priest/Low" and low_variant != "A":
        raise ValueError("Low Priest physical proxy variant is only an A/B selection")
    if pairing == "Priest/Low" and low_variant not in ("A", "B"):
        raise ValueError("Only audited Low Priest A or B proxy")
    if plan == "special":
        if pairing not in SPECIAL:
            raise UnresolvedDecision("No selected accessible special technique scenario")
        if pairing == "Scholar/Medium" and level < 2:
            raise UnresolvedDecision("Medium Scholar lacks Minor Telekinesis at L1")
        for technique in SPECIAL[pairing]:
            _authorized(pairing, level, technique)
    elif plan == "inspection":
        _authorized(pairing, level, "inspection")

    actor, abilities, disciplines, scope = _character(
        pairing, level, low_variant=low_variant if pairing == "Priest/Low" else None)
    e = Encounter([actor], {"pilot": 40}, seed=6,
                  scenario="B05-B06-Supply-Cache-Three-Scene-Pilot-v0",
                  policy=pairing + ":" + plan,
                  objective="one continuous source-paid noncombat route, investigation and record request")
    DamageState(e)
    vp_start = actor.vp_available
    report = []
    evidence = {"route": None, "medical_diagnosis": False,
                "visible_stains": False, "observed_magic_signature": False,
                "loose_sample_retrieved": False, "public_log_access": False,
                "signal_emitted": False}

    # 1 — Approach the remote supply cache. Failure is a declared detour,
    # never an automatically imposed wound or universal exploration penalty.
    route_start = e.g4.clock.world_seconds
    tech = []
    if plan == "special" and pairing == "Priest/High":
        tech.append(_cast(e, pairing, level, "rapport"))
        # Separate, one-time qualifying initial-approach check. It does not
        # let the animal provide directions, automatically become friendly
        # or compel compliance; the ordinary route check remains necessary.
        animal = _roll(e, abilities, disciplines,
                       scene="crossing", domain="exploration",
                       approach="approach_wary_animal", face=faces[3],
                       situational=2, training_override=("Presence", None),
                       target_override=10)
        e.log("b05_b06_rapport_first_trust_consumed", actor="pilot",
              one_use_bonus=2, outcome=animal["success"],
              animal_behavior_not_compelled=True)
    else:
        animal = None
    if plan == "special" and pairing == "Scholar/Medium":
        tech.append(_cast(e, pairing, level, "telekinesis"))
        # The fixture's loose map marker carries a plainly visible route
        # label. Moving that physical object does not provide psychic clues.
        crossing = {"approach": "recover_loose_annotated_map_marker",
                    "success": True, "physical_object_retrieval_only": True}
        e.log("b05_b06_adventure_route_marker_seen", actor="pilot",
              route_accessible=True, gm_authored_label=True)
    else:
        approach = "balance" if plan == "inspection" else "survey"
        crossing = _roll(e, abilities, disciplines, scene="crossing",
                         domain="exploration", approach=approach, face=faces[0])
        _time(e, SCENES["exploration"][approach]["time_seconds"],
              cause="physical_route_attempt")
    route_direct = crossing["success"]
    evidence["route"] = "direct" if route_direct else "detour"
    if not route_direct:
        _time(e, DETOUR_SECONDS, cause="authored_long_footpath_after_route_failure")
    report.append({
        "scene": "1-crossing", "start_seconds": route_start,
        "end_seconds": e.g4.clock.world_seconds, "choice": crossing,
        "animal_first_contact_check": animal, "technique_actions": tech,
        "outcome": "direct_cache_approach" if route_direct else "long_detour_to_cache",
        "detour_seconds": 0 if route_direct else DETOUR_SECONDS,
    })

    # 2 — Distinguish ordinary contaminated-herb proof from observable Veil
    # patterns and telekinetic retrieval. No magic branch invents diagnosis.
    investigate_start = e.g4.clock.world_seconds
    tech = []
    if plan == "inspection":
        tech.append(_cast(e, pairing, level, "inspection"))
        evidence["observed_magic_signature"] = True
        investigation = {"approach": "inspect_held_cache_ring",
                         "success": True, "magical_signature_not_function": True,
                         "medical_cause_identified": False}
        _time(e, 120, cause="author_fixture_examining_source_ring_after_cast")
    elif plan == "special" and pairing in ("Scholar/High", "Scholar/Medium"):
        tech.append(_cast(e, pairing, level, "telekinesis"))
        evidence["loose_sample_retrieved"] = True
        investigation = {"approach": "retrieve_loose_unattended_sample",
                         "success": True, "ordinary_retrieval_only": True,
                         "medical_cause_identified": False}
        _time(e, 120, cause="author_fixture_sorting_retrieved_sample")
    else:
        investigation = _roll(
            e, abilities, disciplines, scene="cache-investigation",
            domain="investigation", approach="diagnose", face=faces[1])
        evidence["medical_diagnosis"] = investigation["success"]
        _time(e, SCENES["investigation"]["diagnose"]["time_seconds"],
              cause="authored_herb_batch_diagnosis")
    report.append({
        "scene": "2-investigation", "start_seconds": investigate_start,
        "end_seconds": e.g4.clock.world_seconds, "choice": investigation,
        "technique_actions": tech,
        "medical_cause_identified": evidence["medical_diagnosis"],
        "observable_magic_only": evidence["observed_magic_signature"],
        "object_retrieved_only": evidence["loose_sample_retrieved"],
    })

    # 3 — Specific GM fixture: a documented ordinary spoiled-batch
    # diagnosis justifies +2 contextual support to the actual request.
    # It is NOT a universal Medicine->Persuasion bonus or NPC compulsion.
    social_start = e.g4.clock.world_seconds
    tech = []
    if plan == "special" and pairing == "Scholar/High":
        tech.append(_cast(e, pairing, level, "sound"))
        evidence["signal_emitted"] = True
    approach = "document" if plan == "evidence" else "petition"
    support = 2 if evidence["medical_diagnosis"] else 0
    social = _roll(e, abilities, disciplines, scene="public-record-request",
                   domain="social", approach=approach, face=faces[2],
                   situational=support)
    _time(e, SCENES["social"][approach]["time_seconds"],
          cause="authored_storekeeper_discussion")
    evidence["public_log_access"] = social["success"]
    report.append({
        "scene": "3-public-record", "start_seconds": social_start,
        "end_seconds": e.g4.clock.world_seconds, "choice": social,
        "technique_actions": tech, "medical_evidence_support": support,
        "outcome": "public_log_shown" if social["success"] else "request_declined",
        "source_of_modifier": ("specific_authored_storekeeper_receives_actual_diagnosis"
                               if support else None),
        "npc_disposition_not_compelled": True,
    })
    e.check()
    if len(report) != 3 or any(
            report[i]["end_seconds"] > report[i+1]["start_seconds"]
            for i in range(2)):
        raise AssertionError("Scenes must share one monotonic world chronology")
    magic = [t for s in report for t in s["technique_actions"]]
    return {
        "pairing": pairing, "level": level, "plan": plan,
        "source_scope": scope, "source_path": actor.source.path,
        "source_sha256": actor.source.digest,
        "scenes": report, "shared_consequences": evidence,
        "world_seconds_elapsed": e.g4.clock.world_seconds,
        "source_vp_initial": vp_start, "source_vp_spent": vp_start-actor.vp_available,
        "source_vp_available": actor.vp_available,
        "source_vp_committed": actor.vp_committed,
        "native_turns_taken": len(magic),
        "source_paid_techniques": [t["technique"] for t in magic],
        "native_ledger_sha256": canonical_digest(e.ledger),
        "native_event_count": len(e.ledger),
        "native_event_kinds": sorted({v["kind"] for v in e.ledger}),
        "externally_verified_gm_scenes": 0, "human_choices_observed": 0,
        "human_session_count": 0, "independent_focus_certified": False,
        "strict_mvp_exits_met": 0, "status": STATUS,
    }


def roster():
    rows = []
    for pairing in sorted(ROLES):
        for level in (1, 2, 3):
            rows.append(play(pairing,level,"evidence"))
            rows.append(play(pairing,level,"inspection"))
            if pairing in SPECIAL and not (pairing=="Scholar/Medium" and level==1):
                rows.append(play(pairing,level,"special"))
    expected=36*2+3+3+2
    if len(rows)!=expected:
        raise AssertionError("Bounded 80-fork fixture census changed")
    return {
        "structural_pairings": 12, "pairing_level_slots": 36,
        "connected_three_scene_author_forks": len(rows),
        "fixture_scenes_count": len(rows)*3,
        "externally_verified_gm_scenes": 0, "human_session_count": 0,
        "full_focus_certificates": 0, "strict_mvp_exits_met": 0,
        "rows": rows,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairing",choices=sorted(ROLES))
    parser.add_argument("--level",type=int)
    parser.add_argument("--plan",choices=PLANS,default="evidence")
    parser.add_argument("--low-variant",choices=("A","B"),default="A")
    parser.add_argument("--faces",nargs=4,type=int,metavar=("ROUTE","INVESTIGATION","SOCIAL","ANIMAL"),
                        default=(12,12,12,12))
    args=parser.parse_args()
    if args.pairing is None and args.level is None and args.plan=="evidence" and args.low_variant=="A" and args.faces==(12,12,12,12):
        result=roster()
    else:
        if args.pairing is None or args.level is None:
            parser.error("Single adventure needs --pairing and --level")
        result=play(args.pairing,args.level,args.plan,faces=args.faces,
                    low_variant=args.low_variant)
    print(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
