"""B04/B05 Low Scholar L1–3 source-legal structural candidate (T).

Only the two individually authored Earth/Life Embodiments are native here;
ordinary known spells do not become equipment enchantments or free reactions.
"""
from copy import deepcopy
import json

from scripts.b05_high_scholar_fire_l1_l3_v0 import ABILITY_COST
from scripts.b05_scholar_inward_embodiment_profiles_v0 import (
    PROFILES, LOW, KNOWN_CAP, PREPARED_CAP, committed_cost,
)

ABILITIES = {
    "Strength": 2, "Agility": 3, "Precision": 0, "Intellect": 0,
    "Awareness": 1, "Presence": -2, "Vitality": 2,
    "Veil Affinity": 0, "Veil Control": 0,
}
WEAPON_TRAINING = {"One-Handed Swords": 2}
DISCIPLINES_L1 = {
    "Veil Theory": 2, "Pillar Lore (Earth)": 2,
    "Medicine": 2, "Acrobatics": 2,
}
EQUIPMENT_SP = {
    "Leather armor": 25, "Sword": 22,
    "Standard adventuring pack": 8, "General artisan's toolkit": 12,
}
KNOWN_L1 = ("Stone Skin", "Guided Regeneration", "Conjure Flame")
KNOWN_L2 = "Basic Heal"
PREPARED_L1 = ("Stone Skin", "Guided Regeneration")
PREPARED_L2 = PREPARED_L1 + ("Conjure Flame",)
TALENT_L1 = "TAL-U01 Veil Insight"
TALENT_L3 = "TAL-C01 Combat Awareness"


def profile(level):
    if type(level) is not int or level not in (1, 2, 3):
        raise ValueError("Only source-authored Low Scholar L1-3")
    if (sum(ABILITY_COST[v] for v in ABILITIES.values()) != 28
            or sum(WEAPON_TRAINING.values()) != 2
            or sum(DISCIPLINES_L1.values()) != 8
            or sum(EQUIPMENT_SP.values()) > 150):
        raise AssertionError("Unlawful independent ability/Training/gear budget")
    known = KNOWN_L1 + ((KNOWN_L2,) if level >= 2 else ())
    prepared = PREPARED_L1 if level == 1 else PREPARED_L2
    if (len(known) != KNOWN_CAP["Low"][level-1]
            or len(prepared) != PREPARED_CAP[level-1]
            or len(set(known)) != len(known)
            or len(set(prepared)) != len(prepared)
            or not set(prepared).issubset(known)):
        raise AssertionError("Known or Prepared Arsenal exceeds source cap")
    if any(PROFILES[x].technique not in prepared for x in LOW):
        raise AssertionError("Chosen Embodiment not genuinely prepared")
    hp = 10 + ABILITIES["Vitality"]
    ap = 30 + 6*(level-1)
    vp = 2*level
    return deepcopy({
        "identity": "Low Scholar Earth/Life Prepared Embodiment Vanguard v0",
        "archetype": "Scholar", "focus": "Low", "level": level,
        "abilities": ABILITIES, "ability_points": 28,
        "weapon_training": WEAPON_TRAINING, "weapon_development_points": 2,
        "learned_disciplines": {
            **DISCIPLINES_L1, **({"Navigation": 1} if level >= 2 else {})},
        "background_familiarities": (
            "Technical guild study", "Local professional trades network"),
        "talents": ((TALENT_L1,) if level < 3 else
                    (TALENT_L1, TALENT_L3)),
        "known_pillar_techniques": known,
        "known_capacity": KNOWN_CAP["Low"][level-1],
        "prepared_techniques": prepared,
        "prepared_capacity": PREPARED_CAP[level-1],
        "preparation_basis": (
            "initial free technical preparation" if level == 1 else
            "level-2+ snapshot after eligible ten-minute six-hour preparation"),
        "known_embodiment_profiles": LOW, "active_embodiment_cap": 1,
        "universals": (("Veil Inspection",) if level < 3 else
                       ("Veil Inspection", "Blink")),
        "max_used_tier": 1 if level < 3 else 2,
        "equipment_sp": EQUIPMENT_SP, "starting_budget_sp": 150,
        "starting_spent_sp": sum(EQUIPMENT_SP.values()),
        "silver_remaining_sp": 150 - sum(EQUIPMENT_SP.values()),
        "equipped_armor": "Leather armor", "wielded_weapon": "Sword",
        "guard_instrument": "Sword",
        "guard_value": 10+ABILITIES["Strength"]+ABILITIES["Agility"]+2,
        "hp_max": hp, "vigor_max": hp*level, "vp_max": vp,
        "turn_ap": ap, "physical_action_ap": 20,
        "projection_action_ap": 30, "physical_tempo": ap//20,
        "projection_tempo": ap//30, "normal_guard_capacity": ap//20,
        "normal_regen_throughput": max(0, ABILITIES["Vitality"])+3,
        "initiative": ABILITIES["Agility"]+ABILITIES["Awareness"]+
                      (2 if level>=3 else 0),
        "first_dodge": 10+min(4,ABILITIES["Agility"])+ABILITIES["Awareness"],
        "movement_points": 12,
        "stone_committed_vp": committed_cost(PROFILES[LOW[0]],vp),
        "guided_committed_vp": committed_cost(PROFILES[LOW[1]],vp),
        "intensification_spent_vp": 1 if level>=3 else None,
        "blink_known": level>=3,
        "independent_full_focus_certified": False,
        "native_outgoing_spell_attack_certified": False,
        "native_weapon_embodiment_authored": False,
    })


def verify():
    previous = None
    for level in (1,2,3):
        p=profile(level)
        assert (p["hp_max"], p["vigor_max"], p["vp_max"])==(12,12*level,2*level)
        assert p["stone_committed_vp"]==(1 if level==1 else 2)
        assert p["guided_committed_vp"]==2
        assert p["silver_remaining_sp"]==83
        assert p["normal_regen_throughput"]==5
        assert p["guard_value"]==17
        assert p["normal_guard_capacity"]==(1 if level<3 else 2)
        assert p["prepared_capacity"]==(2 if level==1 else 3)
        assert p["known_capacity"]==(3 if level==1 else 4)
        assert p["physical_action_ap"]==20 and p["projection_action_ap"]==30
        assert p["movement_points"]==12
        if previous:
            assert set(previous["known_pillar_techniques"]).issubset(
                p["known_pillar_techniques"])
        previous=p
    return {"levels":3,"structural_low_scholar_source_verified":True,
            "native_embodiment_modes_only":True,
            "independent_full_focus_certified":False}


if __name__ == "__main__":
    print(json.dumps({"verification":verify(),
        "levels":[profile(lv) for lv in (1,2,3)]},indent=2,sort_keys=True))
