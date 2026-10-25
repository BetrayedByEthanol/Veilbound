"""B04/B05 Medium Scholar L1–3 source-legal structural sheet v0.

A single explicit example, not universal Scholar access or completed MVP role.
"""
from copy import deepcopy
import json
from scripts.b05_high_scholar_fire_l1_l3_v0 import ABILITY_COST

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
GEAR = {"Leather armor": 25, "Sword": 22,
        "Standard adventuring pack": 8, "General artisan's toolkit": 12}
KNOWN_L1 = ("Stone Skin", "Guided Regeneration", "Conjure Flame", "Basic Heal")
KNOWN_L2 = "Minor Telekinesis"
TALENT_L1 = "TAL-U01 Veil Insight"
TALENT_L3 = "TAL-C01 Combat Awareness"
PROFILE_IDS = ("MS-STONE-BODY-T1", "MS-GUIDED-REGEN-T1")


def profile(level):
    if type(level) is not int or level not in (1, 2, 3):
        raise ValueError("Medium Scholar character supports only L1-3")
    from scripts.b05_scholar_inward_embodiment_profiles_v0 import (
        KNOWN_CAP, PROFILES,
    )
    if sum(ABILITY_COST[v] for v in ABILITIES.values()) != 28:
        raise AssertionError("Invalid source ability budget")
    if sum(WEAPON_TRAINING.values()) != 2 or sum(DISCIPLINES_L1.values()) != 8:
        raise AssertionError("Invalid independent Training budgets")
    if sum(GEAR.values()) > 150:
        raise AssertionError("Illegal level-one equipment allocation")
    known = KNOWN_L1 + ((KNOWN_L2,) if level >= 2 else ())
    if len(known) != KNOWN_CAP["Medium"][level-1] or len(set(known)) != len(known):
        raise AssertionError("Medium individually learned counts")
    if any(PROFILES[i].technique not in known for i in PROFILE_IDS):
        raise AssertionError("Missing individually learned Inward candidate")
    vit = ABILITIES["Vitality"]
    ap = 30 + 6*(level-1)
    return deepcopy({
        "identity": "Medium Scholar Earth/Life Inward Technical Vanguard v0",
        "archetype": "Scholar", "focus": "Medium", "level": level,
        "abilities": ABILITIES,
        "ability_points": 28, "weapon_training": WEAPON_TRAINING,
        "weapon_development_points": 2,
        "learned_disciplines": {
            **DISCIPLINES_L1, **({"Navigation": 1} if level >= 2 else {})},
        "background_familiarities": (
            "Technical guild study", "Local professional trades network"),
        "talents": ((TALENT_L1,) if level < 3 else
                    (TALENT_L1,TALENT_L3)),
        "known_pillar_techniques": known, "known_capacity": len(known),
        "known_inward_profiles": PROFILE_IDS, "active_inward_cap": 1,
        "prepared_technique_subset": None,
        "universals": (("Veil Inspection",) if level < 3 else
                       ("Veil Inspection","Blink")),
        "max_used_tier": 1 if level < 3 else 2,
        "equipment_sp": GEAR, "starting_budget_sp": 150,
        "starting_spent_sp": sum(GEAR.values()),
        "silver_remaining_sp": 150-sum(GEAR.values()),
        "equipped_armor": "Leather armor", "wielded_weapon": "Sword",
        "guard_instrument": "Sword",
        "guard_value": 10+ABILITIES["Strength"]+ABILITIES["Agility"]+2,
        "resonance": 0, "hp_max": 10+vit,
        "vigor_max": (10+vit)*level,
        "vp_max": (4+ABILITIES["Veil Affinity"])*level,
        "turn_ap": ap, "physical_action_ap": 24,
        "projection_action_ap": 24,
        "physical_tempo": ap//24, "projection_tempo": ap//24,
        "normal_guard_capacity": ap//24,
        "normal_regen_throughput": max(0,vit)+1,
        "initiative": ABILITIES["Agility"]+ABILITIES["Awareness"]+
                      (2 if level>=3 else 0),
        "first_dodge": 10+min(ABILITIES["Agility"],4)+ABILITIES["Awareness"],
        "movement_points": 12, "reroute_spent_vp": 3 if level<3 else 2,
        "overroute_max_steps": 0 if level<3 else 2,
        "blink_affordable_from_full_vp": level>=3 and 12>=10,
        "native_physical_attack_verified": False,
        "complete_focus_certified": False,
    })


def verify():
    previous = None
    from scripts.b05_scholar_inward_embodiment_profiles_v0 import PROFILES
    for level in (1,2,3):
        p=profile(level)
        assert p["hp_max"] == 12
        assert p["vigor_max"] == 12*level
        assert p["vp_max"] == 4*level
        assert p["normal_guard_capacity"] == (1 if level<3 else 1)
        assert p["known_capacity"] == (4 if level==1 else 5)
        assert p["silver_remaining_sp"] == 83
        assert p["movement_points"] == 12
        assert p["guard_value"] == 17
        assert p["normal_regen_throughput"] == 3
        assert all(PROFILES[ident].technique in
                   p["known_pillar_techniques"] for ident in PROFILE_IDS)
        if previous:
            assert set(previous["known_pillar_techniques"]) <= set(p["known_pillar_techniques"])
        previous = p
    return {"levels":3, "structural_build_source_verified":True,
            "native_inward_profile_only":True,
            "full_mvp_focus_certified":False}


if __name__=="__main__":
    print(json.dumps({"verification":verify(),
                      "sheets":[profile(level) for level in (1,2,3)]},
                     indent=2,sort_keys=True))
