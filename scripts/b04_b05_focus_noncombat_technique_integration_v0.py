"""B04/B05 legal noncombat Veil technique actions on genuine G0 source actors.

One bounded, fully paid native Turn AP/VP action per authored fixture.
The surrounding item/animal/object facts are explicit author-authored mock
GM premises, not independently authenticated real-world GM decisions.
No new magic catalogue, universal technique access or MVP certification.
"""
import argparse
import json
from importlib import import_module

from scripts.b04_b05_noncombat_scene_resolution_v0 import _character
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import FOCUS_TASKS
from scripts.b06_damage_v0 import DamageState
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

LEVELS = (1, 2, 3)
TECHNIQUES = {
    "inspection": "Veil Inspection",
    "rapport": "Woodland Rapport",
    "sound": "Phantom Sound",
    "telekinesis": "Minor Telekinesis",
}
STATUS = "SOURCE_PAID_AUTHOR_FIXTURE_NOT_EXTERNAL_GM_PLAY"
UNRESOLVED = "NPC/reaction/consequence requires independent GM adjudication"
OPTIONS = {
    "Priest/High": ("inspection", "rapport"),
    "Scholar/High": ("inspection", "sound", "telekinesis"),
    "Scholar/Medium": ("inspection", "telekinesis"),
}


def _authorized(pairing, level, technique):
    if type(pairing) is not str or pairing not in FOCUS_TASKS:
        raise ValueError("Unknown canonical Focus")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only original L1-3 source levels")
    if type(technique) is not str or technique not in TECHNIQUES:
        raise ValueError("Unknown authored technique")
    if technique == "inspection":
        return
    if technique not in OPTIONS.get(pairing, ()):
        raise UnresolvedDecision("No individually accessed noncombat technique on this Focus")
    if technique == "telekinesis" and pairing == "Scholar/Medium" and level == 1:
        raise UnresolvedDecision("Medium Scholar acquires Minor Telekinesis at L2")
    # Validate actual technique selection, not merely a named Focus permission.
    from scripts.b04_b05_noncombat_scene_resolution_v0 import _sources
    source = _sources()[pairing]
    script = next(p for p in source["source_fingerprints"] if p.startswith("scripts/"))
    profile = import_module("scripts." + script.split("/")[-1][:-3]).profile(level)
    name = TECHNIQUES[technique]
    if pairing == "Priest/High":
        eligible = profile["prepared_prayers"]    # source standard list
    else:
        eligible = profile["known_pillar_techniques"]
    if name not in eligible:
        raise UnresolvedDecision("Technique is not actually prepared/known on this source sheet")


def _source_actor(pairing, level):
    actor, abilities, disciplines, scope = _character(
        pairing, level, low_variant="A" if pairing == "Priest/Low" else None)
    return actor, abilities, disciplines, scope


def run_scene(pairing, level, technique, *,
              tier=1, item="held_ring", pattern="Life/Restoration",
              held=True, contact_lost_after_ap=False,
              observe_interpretation=True, face=12,
              animal_mass_kg=12, animal_state="wary",
              animal_visible=True, path_open=True, sensory_route=True,
              object_mass_kg=3, object_volume_dm3=3, object_dimension_m=0.4,
              object_range_squares=4, object_route_squares=2,
              object_unattended=True, hand_available=True,
              sound="single_knock", sound_range_squares=3,
              discount=False):
    _authorized(pairing, level, technique)
    if type(tier) is not int or tier not in (1, 2):
        raise ValueError("Only T1 or explicitly L3 T2 example")
    if type(contact_lost_after_ap) is not bool or type(discount) is not bool:
        raise ValueError("Source interruption/discount declarations must be bool")
    if type(face) is not int or not 1 <= face <= 20:
        raise ValueError("One explicitly rolled interpretation d20 is 1..20")
    actor, abilities, disciplines, scope = _source_actor(pairing, level)
    if technique != "rapport" and tier != 1:
        raise ValueError("No source-authored alternate Used Tier in this fixture")
    if technique == "rapport" and tier == 2 and level != 3:
        raise ValueError("T2 Woodland Rapport is L3+")
    if discount and not (technique == "inspection" and
                         pairing == "Priest/Medium" and level == 3):
        raise ValueError("Only source-owned TAL-M03 at L3 may discount this Inspection")
    effective = (1 if discount else 2) if technique == "inspection" else (
        2 * tier if technique in ("rapport", "telekinesis") else 1)
    # Preflight before AP commitment. All target predicates are mock GM
    # observations; callers cannot use them to certify a real scene.
    if technique == "inspection":
        if item != "held_ring" or type(held) is not bool or not held:
            raise ValueError("Inspection requires the selected actually held item")
        if pattern not in ("Life/Restoration", "unobservable"):
            raise ValueError("Cannot invent hidden enchantment properties")
    elif technique == "rapport":
        if (type(animal_mass_kg) not in (int, float) or
                not 0 < animal_mass_kg <= (25 if tier == 1 else 125)
                or animal_state not in ("wary", "indifferent")
                or not all(type(x) is bool and x for x in
                           (animal_visible, path_open, sensory_route))):
            raise ValueError("Only eligible nonhostile visible sensing animal")
    elif technique == "telekinesis":
        values=(object_mass_kg, object_volume_dm3, object_dimension_m,
                object_range_squares, object_route_squares)
        if (not all(type(x) in (int, float) for x in values)
                or not (0 < object_mass_kg <= 10)
                or not (0 < object_volume_dm3 <= 10)
                or not (0 < object_dimension_m <= 1.5)
                or not (0 <= object_range_squares <= 20)
                or not (0 <= object_route_squares <= 6)
                or type(object_unattended) is not bool or not object_unattended
                or type(hand_available) is not bool or not hand_available
                or not (animal_visible and path_open)):
            raise ValueError("Single loose mundane object, direct sight and free hand required")
    elif technique == "sound":
        if (sound not in ("single_knock", "short_whistle")
                or type(sound_range_squares) not in (int, float)
                or not 0 <= sound_range_squares <= 12
                or not (animal_visible and path_open)):
            raise ValueError("Only visible unblocked localized nonverbal sound")
    if actor.vp_available < effective:
        raise ValueError("Insufficient source Available VP")
    e = Encounter([actor], {"pilot": 40}, seed=0,
                  scenario="B04-B05-Native-Noncombat-Technique-v0",
                  policy=f"{pairing}:{technique}:T{tier}",
                  objective="one source-paid action; no GM/Focus signoff")
    DamageState(e)
    e.begin_round()
    e.start_turn("pilot", regen_choice=RegenerationChoice())
    ap_before, vp_before = actor.ap_remaining, actor.vp_available
    action_class = "full" if technique == "inspection" else "projection"
    ap_spent = e.spend_ap("pilot", action_class,
                         label="b04_b05_" + technique)
    if contact_lost_after_ap:
        e.log("b04_b05_noncombat_application_canceled", actor="pilot",
              technique=TECHNIQUES[technique],
              reason="authored fixture interruption after native AP commit",
              vp_spent=0)
        observation = None
        interpretation = None
        applied = False
    else:
        e.spend_vp("pilot", effective, mode="spent",
                   label="b04_b05_" + technique)
        applied = True
        interpretation = None
        if technique == "inspection":
            observation = (
                {"observable": True, "pillar": "Life", "aspect": "Restoration",
                 "function_identified": False, "concealed_revealed": False}
                if pattern == "Life/Restoration" else
                {"observable": False, "pillar": None, "aspect": None,
                 "function_identified": False, "concealed_revealed": False})
            if observe_interpretation and observation["observable"]:
                rank=disciplines.get("Veil Theory", 0)
                total=face+abilities["Intellect"]+rank+2
                interpretation={
                    "source_veil_theory_rank": rank, "intellect": abilities["Intellect"],
                    "inspection_situational_modifier": 2,
                    "face": face, "total": total, "target": 12,
                    "succeeds_on_authored_question": total >= 12,
                    "limited_to_observed_pattern": True,
                }
        elif technique == "rapport":
            observation = {
                "external_peaceful_cues": True,
                "target_animal_kg": animal_mass_kg,
                "initial_trust_bonus_pending": 2,
                "cue_duration_minutes": min(30,10+5*max(0,abilities["Veil Control"])),
                "animal_response": UNRESOLVED, "compulsion": False,
                "extra_targets": 0,
            }
        elif technique == "telekinesis":
            observation = {
                "unattended_object_moved": True, "mass_kg": object_mass_kg,
                "volume_dm3": object_volume_dm3,
                "distance_squares": object_route_squares,
                "damage": 0, "held_object_seized": False,
                "sustained_levitation": False,
            }
        else:
            observation = {
                "short_nonverbal_event": sound, "localized_source": True,
                "sound_event_seconds_at_most": 2,
                "listener_behavior": UNRESOLVED,
                "forced_distraction": False, "damage": 0,
            }
        e.log("b04_b05_noncombat_technique_applied",
              actor="pilot", technique=TECHNIQUES[technique],
              source_path=actor.source.path, source_sha256=actor.source.digest,
              spent_vp=effective, observation=observation,
              interpretation=interpretation, no_human_gm_certification=True)
    e.end_turn()
    e.check()
    return {
        "pairing": pairing, "level": level, "technique": TECHNIQUES[technique],
        "tier": tier, "source_path": actor.source.path,
        "source_sha256": actor.source.digest, "source_scope": scope,
        "action_class": action_class, "ap_before": ap_before, "ap_spent": ap_spent,
        "vp_before": vp_before, "vp_spent": vp_before-actor.vp_available,
        "vp_after": actor.vp_available, "effect_applied": applied,
        "observation": observation, "interpretation": interpretation,
        "ledger_sha256": canonical_digest(e.ledger),
        "ledger_event_kinds": sorted(set(x["kind"] for x in e.ledger)),
        "status": STATUS, "human_choices_observed": 0,
        "external_gm_verdict": False, "full_focus_certified": False,
        "strict_mvp_exits_met": 0,
    }


def matrix():
    rows = []
    for pairing in sorted(FOCUS_TASKS):
        for level in LEVELS:
            rows.append(run_scene(pairing,level,"inspection"))
            for technique in OPTIONS.get(pairing, ()):
                if technique == "inspection":
                    continue
                if technique == "telekinesis" and pairing == "Scholar/Medium" and level == 1:
                    continue
                rows.append(run_scene(pairing,level,technique))
    return {
        "focus_pairings": 12, "levels": 3, "source_paid_noncombat_actions": len(rows),
        "universal_inspection_coverage": sum(r["technique"]=="Veil Inspection" for r in rows),
        "focus_specific_actions": sum(r["technique"]!="Veil Inspection" for r in rows),
        "externally_verified_gm_scenes": 0, "human_choices_observed": 0,
        "full_focus_certificates": 0, "strict_mvp_exits_met": 0,
        "rows": rows,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairing",choices=sorted(FOCUS_TASKS))
    parser.add_argument("--level",type=int)
    parser.add_argument("--technique",choices=sorted(TECHNIQUES))
    args=parser.parse_args()
    if any(x is not None for x in (args.pairing,args.level,args.technique)):
        if not all(x is not None for x in (args.pairing,args.level,args.technique)):
            parser.error("Specify all of --pairing, --level and --technique")
        result=run_scene(args.pairing,args.level,args.technique)
    else:
        result=matrix()
    print(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
