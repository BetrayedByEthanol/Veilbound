"""B04/B05: one selected Medium Priest Life L1–3 structural character.

All numbers and choices come from the existing B04/B05 Priest/Medium rules,
TAL-C02/TAL-M03, and the audited Life Low Vanguard's legal mundane allocation.
A source sheet is not an opposed encounter or an independent MVP certificate.
"""
from copy import deepcopy

ABILITIES = {
    "Strength": 2, "Agility": 3, "Precision": 0, "Intellect": 0,
    "Awareness": 1, "Presence": -2, "Vitality": 2,
    "Veil Affinity": 0, "Veil Control": 0,
}
CREATION_COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
TRAINING = {"Veil Theory": 2, "Life Pillar Lore": 2,
            "Medicine": 2, "Acrobatics": 2}
EQUIPMENT_SP = {"Leather armor": 25, "Sword": 22,
                "Medical kit": 15, "Adventuring pack": 8}
L1_PRAYERS = ("Guided Regeneration", "Vital Shelter", "Basic Heal")
L2_PRAYERS = L1_PRAYERS + ("Woodland Rapport",)
LIFE_T1 = frozenset(("Basic Heal", "Guided Regeneration",
    "Vital Shelter", "Venom Endurance", "Gentle Growth", "Woodland Rapport"))


def profile(level):
    if type(level) is not int or level not in (1, 2, 3):
        raise ValueError("Only authored Medium Life levels 1–3")
    if sum(CREATION_COST[v] for v in ABILITIES.values()) != 28:
        raise AssertionError("Ability budget must be exactly 28")
    if sum(TRAINING.values()) != 8 or sum(EQUIPMENT_SP.values()) > 150:
        raise AssertionError("Illegal starting allocation")
    prayers = L1_PRAYERS if level == 1 else L2_PRAYERS
    if len(set(prayers)) != len(prayers) or not set(prayers) <= LIFE_T1:
        raise AssertionError("Only unique authored Life prayers permitted")
    if len(prayers) != (3 if level == 1 else 4):
        raise AssertionError("Accord +1 Medium prayer capacity violated")
    vit = ABILITIES["Vitality"]
    return deepcopy({
        "archetype": "Priest", "focus": "Medium", "pillar": "Life",
        "level": level, "abilities": ABILITIES, "weapon_training": {"One-Handed Swords": 2},
        "learned_disciplines": {**TRAINING, **({"Survival": 1} if level >= 2 else {})},
        "equipment_sp": EQUIPMENT_SP, "silver_remaining": 150-sum(EQUIPMENT_SP.values()),
        "background_familiarities": ("Home community", "Prior rural medical practice"),
        "accord": 1, "resonance": 0, "miracle_debt": 0,
        "prepared_prayers": prayers, "prepared_capacity": len(prayers),
        "talents": (("TAL-C02",) if level < 3 else ("TAL-C02", "TAL-M03")),
        "hp_max": 10+vit, "vigor_max": (10+vit)*level,
        "vp_max": (4+ABILITIES["Veil Affinity"])*level,
        "turn_ap": 30 + 6*(level-1),
        "physical_action_ap": 24, "projection_action_ap": 24,
        "normal_regen_throughput": max(vit,0)+2+1,  # TAL-C02 is already owned at L1
        "normal_guard_capacity": 1,
        "guard_value": 10 + ABILITIES["Strength"]+ABILITIES["Agility"]+2,
        "dodge_value": 10+ABILITIES["Agility"]+ABILITIES["Awareness"],
        "initiative": ABILITIES["Agility"]+ABILITIES["Awareness"],
        "tier_ceiling": 1 if level < 3 else 2,
        "active_consecration_cap": 1,
        "universals": ("Veil Inspection",) if level < 3 else ("Veil Inspection", "Blink"),
    })


def verify():
    previous = None
    for level in (1,2,3):
        p = profile(level)
        assert p["prepared_capacity"] == (3 if level == 1 else 4)
        assert p["vigor_max"] == 12*level and p["vp_max"] == 4*level
        assert p["turn_ap"] == 30 + 6*(level-1)
        assert p["normal_regen_throughput"] == 5
        assert p["normal_guard_capacity"] == 1
        assert p["silver_remaining"] == 80
        if previous is not None:
            assert set(previous["prepared_prayers"]) <= set(p["prepared_prayers"])
        previous = p
    return {"levels": 3, "source_legal_structural": True,
            "native_focus_scene_certified": False,
            "independent_mvp_focus_certified": False}


if __name__ == "__main__":
    print(verify())
