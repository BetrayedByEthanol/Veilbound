"""B04/B05 High Priest Life L1–3 source-selected build, no Focus certification.

Two explicitly legal initial prayer lists allow distinct prepared-vs-invoked
receipts without retroactively swapping prayers mid-encounter. L3 may leave
exactly one slot UNSPECIFIED for High Open Prayer.
"""
from copy import deepcopy

LEVELS=(1,2,3)
ABILITIES={
    "Strength":2,"Agility":3,"Precision":0,"Intellect":0,
    "Awareness":1,"Presence":-2,"Vitality":2,
    "Veil Affinity":0,"Veil Control":0,
}
CREATION_COST={-2:0,-1:1,0:2,1:3,2:5,3:7,4:10}
TRAINING={"Veil Theory":2,"Life Pillar Lore":2,
          "Medicine":2,"Acrobatics":2}
EQUIPMENT_SP={"Leather armor":25,"Sword":22,
              "Medical kit":15,"Adventuring pack":8}
LIFE_T1=frozenset(("Basic Heal","Guided Regeneration","Vital Shelter",
                    "Woodland Rapport","Venom Endurance","Gentle Growth"))
PREPARATION={
    "standard":{
        1:("Basic Heal","Guided Regeneration","Vital Shelter","Woodland Rapport"),
        2:("Basic Heal","Guided Regeneration","Vital Shelter","Woodland Rapport",
           "Venom Endurance"),
        3:("Basic Heal","Guided Regeneration","Vital Shelter","Woodland Rapport"),
    },
    "invocation":{
        1:("Guided Regeneration","Vital Shelter","Woodland Rapport",
           "Venom Endurance"),
        2:("Guided Regeneration","Vital Shelter","Woodland Rapport",
           "Venom Endurance","Gentle Growth"),
        3:("Guided Regeneration","Vital Shelter","Woodland Rapport",
           "Venom Endurance"),
    },
    "ward_invocation":{
        1:("Basic Heal","Guided Regeneration","Woodland Rapport",
           "Venom Endurance"),
        2:("Basic Heal","Guided Regeneration","Woodland Rapport",
           "Venom Endurance","Gentle Growth"),
        3:("Basic Heal","Guided Regeneration","Woodland Rapport",
           "Venom Endurance"),
    },
}


def profile(level,*,preparation="standard"):
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only sourced High Life levels 1–3")
    if preparation not in PREPARATION:
        raise ValueError("Only authored character-creation preparations")
    if sum(CREATION_COST[v] for v in ABILITIES.values())!=28:
        raise AssertionError("Nine abilities must spend 28 creation points")
    if sum(TRAINING.values())!=8 or sum(EQUIPMENT_SP.values())>150:
        raise AssertionError("Invalid L1 trained disciplines or gear")
    prayers=PREPARATION[preparation][level]
    capacity=(4 if level==1 else 5)
    open_slot=int(level==3)
    if (len(prayers)+open_slot!=capacity or len(prayers)!=len(set(prayers))
            or not set(prayers)<=LIFE_T1):
        raise AssertionError("Only authored unique Life prayers fill capacity")
    a=ABILITIES
    hp=10+a["Vitality"]
    return deepcopy({
        "archetype":"Priest","focus":"High","pillar":"Life",
        "level":level,"preparation_policy":preparation,
        "abilities":a,
        "weapon_training":{"One-Handed Swords":2},
        "learned_disciplines":{**TRAINING,**({"Survival":1} if level>=2 else {})},
        "equipment_sp":EQUIPMENT_SP,"silver_remaining":150-sum(EQUIPMENT_SP.values()),
        "accord":1,"resonance":0,"miracle_debt":0,
        "prepared_prayers":prayers,
        "prepared_capacity":capacity,"open_prayer_slots":open_slot,
        "talents":(("TAL-C02",) if level<3 else ("TAL-C02","TAL-M03")),
        "hp_max":hp,"vigor_max":hp*level,
        "vp_max":(6+a["Veil Affinity"])*level,
        "turn_ap":30+6*(level-1),
        "physical_action_ap":30,"projection_action_ap":20,
        "normal_regen_throughput":max(a["Vitality"],0)+1+1,
        "normal_guard_capacity":1,
        "guard_value":10+a["Strength"]+a["Agility"]+2,
        "dodge_value":10+a["Agility"]+a["Awareness"],
        "initiative":a["Agility"]+a["Awareness"],
        "tier_ceiling":1 if level<3 else 2,
        "universals":("Veil Inspection",) if level<3 else
                     ("Veil Inspection","Blink"),
        "high_open_invocation_surcharge":1,
        "open_invocation_action":"Full Action",
    })


def verify():
    for policy in PREPARATION:
        for level in LEVELS:
            p=profile(level,preparation=policy)
            assert p["vp_max"]==6*level
            assert p["normal_regen_throughput"]==4
            assert p["physical_action_ap"]==30
            assert p["projection_action_ap"]==20
            assert len(p["prepared_prayers"])+p["open_prayer_slots"]==p["prepared_capacity"]
            assert p["silver_remaining"]==80
    return {"source_legal_structural":True,"profiles":9,
            "full_encounter_certified":False,
            "independent_mvp_focus_certified":False}


if __name__=="__main__":
    print(verify())
