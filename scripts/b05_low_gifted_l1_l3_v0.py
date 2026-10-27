"""B04/B05 — source-constrained Low Gifted L1–3 structural sheet.

Anchor benefits remain PR #158 PROVISIONAL candidates. No native G0/G1/G5
receipt, automatic player-granted effect or independent Focus certification.
"""
from copy import deepcopy
import json

from scripts.b05_high_gifted_l1_l3_v0 import ABILITY_COST
from scripts.b05_high_gifted_amplification_v0 import PILOT_LINKS
from scripts.b05_low_gifted_anchor_design_v0 import (
    CANDIDATE, LowGiftedAnchorDesign, starting_access, ordinary_cast_budget,
)

LEVELS = (1, 2, 3)
ABILITIES = {
    "Strength": 2, "Agility": 3, "Precision": 0, "Intellect": 0,
    "Awareness": 1, "Presence": -2, "Vitality": 2,
    "Veil Affinity": 0, "Veil Control": 0,
}
LEARNED_L1 = {
    "Emotional Discipline": 2, "Disguise": 2,
    "Acrobatics": 2, "Medicine": 2,
}
FAMILIES = {
    "Cultural and Specialized": 4, "Physical and Fieldcraft": 2,
    "Professional and Technical": 2,
}
WEAPON_TRAINING = {"One-Handed Swords": 2}
EQUIPMENT_SP = {
    "Leather armor": 25, "Sword": 22,
    "Standard adventuring pack": 8, "Basic medical kit": 15,
}
TALENTS = {
    1: "TAL-G01 Emotional Poise",
    2: "TAL-C05 Guard Reserve",
    3: "TAL-C01 Combat Awareness",
}
PLAUSIBLE = {
    "Joy": "Celebrating around shared watchfires evokes protective hearth-flame",
    "Anger": "Resisting a blocked path channels forceful psionic movement",
}


def profile(level):
    """One fully budgeted, persistent character across the three level steps."""
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only sourced Low Gifted L1–3")
    a = deepcopy(ABILITIES)
    source = starting_access(level, veil_affinity=a["Veil Affinity"])
    ap, vp = source["turn_ap"], source["vp_max"]
    learned = dict(LEARNED_L1)
    if level >= 2:
        learned["Navigation"] = 1
    hp = 10 + a["Vitality"]
    chosen = [TALENTS[n] for n in LEVELS if n <= level]
    guard_reserve = int(level >= 2)
    initiative_talent = 2 if level >= 3 else 0
    return deepcopy({
        "identity": "Low Gifted Border-Watch Anchor Defender — pilot",
        "archetype": "Gifted", "focus": "Low", "level": level,
        "abilities": a,
        "ability_points": sum(ABILITY_COST[n] for n in a.values()),
        "resonance": 0, "priest_pillar_accord": None,
        "learned_disciplines": learned, "learned_points": sum(learned.values()),
        "learned_family_allocation_l1": FAMILIES,
        "weapon_training": WEAPON_TRAINING,
        "weapon_development_points": sum(WEAPON_TRAINING.values()),
        "background_familiarities": [
            "Border-watch patrol routes", "Roadside healer and caravan community",
        ],
        "talents": chosen, "talent_selections_acquired": len(chosen),
        "talent_selection_levels": list(range(1, level + 1)),
        "talent_emotional_poise_bonus_once_per_window": 2,
        "talent_guard_reserve_capacity": guard_reserve,
        "talent_combat_awareness_initiative": initiative_talent,
        "emotion_aspect_links": {
            e: {
                "pillar": PILOT_LINKS[e][0], "aspect": PILOT_LINKS[e][1],
                "compatibility": PILOT_LINKS[e][2],
                "creation_interpretation": PLAUSIBLE.get(e),
            } for e in PILOT_LINKS
        },
        "authored_linked_techniques": {
            e: list(source["links"][e]["ordinary_techniques"]) for e in PILOT_LINKS
        },
        "authored_upcast_t2": list(source["explicit_t2_upcasts"]),
        "max_used_tier": source["max_used_tier"],
        "universal": list(source["universal_known"]),
        "active_emotion": None, "anchored_emotion": None,
        "emotion_intensity": None, "prepared_techniques": None,
        "individually_learned_pillar_techniques": None,
        "anchor_expressions": {
            e: {**CANDIDATE[e], "status": "PROVISIONAL_UNAPPROVED"}
            for e in CANDIDATE
        },
        "anchor_host": "own body", "anchor_candidate_pulse_per_window": 1,
        "break_anchor_general_ap": 24,
        "anchor_extra_spent_vp": 0, "anchor_extra_committed_vp": 0,
        "anchor_native_effect_certified": False,
        "equipment_sp": EQUIPMENT_SP,
        "starting_budget_sp": 150,
        "starting_spent_sp": sum(EQUIPMENT_SP.values()),
        "silver_remaining_sp": 150 - sum(EQUIPMENT_SP.values()),
        "armor": 3, "wielded_weapon": "Sword",
        "sword_attack_bonus": a["Strength"]+a["Agility"]+2,
        "sword_guard_defense": 10+a["Strength"]+a["Agility"]+2,
        "sword_damage": "3+d6 Cut/Pierce (Light contribution +1)",
        "sword_penetration": 2,
        "hp_max": hp, "vigor_max": hp*level, "vp_max": vp,
        "turn_ap": ap, "physical_action_ap": 20,
        "projection_action_ap": 30, "general_action_ap": 24,
        "physical_tempo": ap//20, "projection_tempo": ap//30,
        "normal_guard_capacity": ap//20,
        "guard_capacity": ap//20+guard_reserve,
        "opportunity_capacity": ap//20,
        "movement_points": 12,
        "initiative": a["Agility"]+a["Awareness"]+initiative_talent,
        "first_dodge": 10+min(a["Agility"], 4)+a["Awareness"],
        "normal_regen_throughput": max(0,a["Vitality"])+3,
        "emotional_discipline_check_bonus": a["Awareness"]+learned["Emotional Discipline"],
        "instability_check_bonus": a["Veil Control"]+learned["Emotional Discipline"],
        "thrown_flame_attack_bonus": a["Agility"]+a["Precision"],  # Throwing untrained
        "thrown_flame_t1_ap": 30, "thrown_flame_t1_spent_vp": 2,
        "stone_skin_t1_committed_vp": (vp+2)//3,
        "blink_known": level>=3, "blink_base_spent_vp": 10 if level>=3 else None,
        "blink_affordable_from_full_vp": level>=3 and vp>=10,
        "two_physical_actions_fit": 40<=ap,
        "paid_break_plus_projection_fit": 54<=ap,
        "paid_deepen_plus_projection_fit": 54<=ap,
        "paid_break_plus_paid_deepen_fit": 48<=ap,
        "settled_deepen_then_projection_fit": level==3 and 30<=ap,
        "structural_character_build_complete": True,
        "independent_full_focus_certified": False,
        "native_combat_or_noncombat_certified": False,
    })


def anchor_witness(level):
    """Only isolated candidate previews. paid/source_legal are UNTRUSTED inputs."""
    s = profile(level)
    m = LowGiftedAnchorDesign(level, veil_affinity=s["abilities"]["Veil Affinity"])
    m.begin_window(dominant="Fear")
    m.establish_anchor("Fear")
    first=m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True)
    again=m.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True)
    m.begin_window(dominant="Fear")
    renewed=m.guarded_defense(kind="dodge" if level>=2 else "guard",
                              paid=True,self_target=True,source_legal=True)
    m.break_anchor("Disgust")
    no_refresh=m.movement_step(kind="normal_difficult",paid=True,source_legal=True,
                                base_mp=1,surcharge_mp=2)
    m.begin_window(dominant="Disgust")
    move=m.movement_step(kind="normal_difficult",paid=True,source_legal=True,
                         base_mp=1,surcharge_mp=2)
    repeated=m.movement_step(kind="normal_difficult",paid=True,source_legal=True,
                             base_mp=1,surcharge_mp=2)
    n=LowGiftedAnchorDesign(level)
    n.begin_window(dominant="Joy")
    n.establish_anchor("Fear")
    inactive=n.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True)
    transition=n.reassert(die=9,awareness=s["abilities"]["Awareness"],
                          discipline=s["learned_disciplines"]["Emotional Discipline"],
                          resonance=s["resonance"])
    active=n.guarded_defense(kind="guard",paid=True,self_target=True,source_legal=True)
    settled=None
    if level==3:
        x=LowGiftedAnchorDesign(level)
        x.begin_window(dominant="Fear")
        x.establish_anchor("Fear")
        paid=x.deepen(die=9,awareness=1,discipline=2)
        x.begin_window(dominant="Fear")
        paid_expired=not x.heightened
        free=x.deepen(die=9,awareness=1,discipline=2)
        x.begin_window(dominant="Fear")
        settled={"paid":paid,"ordinary_expired":paid_expired,
                 "free":free,"persistent":x.heightened and x.settled_heightening}
    return {"level":level,"first_defense":first.bonus,"repeated_defense":again.bonus,
            "new_window_defense":renewed.bonus,"break_no_refresh":no_refresh.mp_reduction,
            "fresh_movement_mp":move.remaining_mp_cost,
            "repeated_movement_mp":repeated.remaining_mp_cost,
            "competing_inactive":not inactive.applicable,"paid_transition":transition,
            "transition_ap_remaining":n.ap_remaining,"reasserted_defense":active.bonus,
            "level3_settled":settled,
            "native_receipt":False,"canonical_anchor_approved":False}


def verify():
    """Fail closed on point-budget, Talent, source access and witness drift."""
    if (len(ABILITIES)!=9 or
            any(type(v) is not int or v not in ABILITY_COST for v in ABILITIES.values()) or
            sum(ABILITY_COST[x] for x in ABILITIES.values())!=28):
        raise AssertionError("Unlawful nine-Ability starting budget")
    if (sum(LEARNED_L1.values())!=8 or max(LEARNED_L1.values())>2
            or sum(FAMILIES.values())!=8
            or WEAPON_TRAINING!={"One-Handed Swords":2}
            or sum(EQUIPMENT_SP.values())>150
            or sorted(TALENTS)!=[1,2,3]
            or {e for e in PILOT_LINKS if PILOT_LINKS[e][2]=="P"}!=set(PLAUSIBLE)):
        raise AssertionError("Unlawful Trainings, Talents, equipment or links")
    for level in LEVELS:
        s=profile(level)
        if (s["ability_points"]!=28 or s["learned_points"]!=8+int(level>=2)
                or s["talent_selections_acquired"]!=level
                or s["vp_max"]!=2*level or s["guard_capacity"]!=ap_guards(level)
                or s["opportunity_capacity"]!=s["physical_tempo"]
                or s["starting_spent_sp"]+s["silver_remaining_sp"]!=150
                or not s["structural_character_build_complete"]
                or s["anchor_native_effect_certified"]):
            raise AssertionError("Source-derived L1–3 build drift")
        w=anchor_witness(level)
        if (w["first_defense"],w["repeated_defense"],w["new_window_defense"])!=(1,0,1):
            raise AssertionError("Invalid isolated Fear one-pulse cadence")
        if (w["break_no_refresh"],w["fresh_movement_mp"],w["repeated_movement_mp"])!=(0,2,3):
            raise AssertionError("Invalid isolated Disgust MP/no-refresh")
        if (not w["competing_inactive"] or not w["paid_transition"]
                or w["reasserted_defense"]!=1
                or w["transition_ap_remaining"]!=s["turn_ap"]-24):
            raise AssertionError("Invalid source-based paid Anchor transition")
        if level==3:
            z=w["level3_settled"]
            if (not z["paid"]["success"] or z["paid"]["settled"]
                    or z["paid"]["ap_spent"]!=24 or not z["ordinary_expired"]
                    or z["free"]["ap_spent"]!=0 or not z["free"]["success"]
                    or not z["persistent"]):
                raise AssertionError("L3 Settled provenance failure")
    return True


def ap_guards(level):
    return (30+6*(level-1))//20+int(level>=2)


if __name__ == "__main__":
    verify()
    print(json.dumps({"build":"Low Gifted structural L1–3",
                      "levels":[profile(n) for n in LEVELS],
                      "anchor_witnesses":[anchor_witness(n) for n in LEVELS]},
                     sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False))
