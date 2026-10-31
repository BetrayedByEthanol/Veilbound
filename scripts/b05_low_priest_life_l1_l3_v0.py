"""B04/B05 original Low Life Priest A/B selected FULL L1-3 source sheets.

These preserve the two existing B06 G0 *physical* actor projections. They add
the independently auditable choices that projection cannot represent:
Learned Disciplines, preparation, Chosen Rite, talents and hand constraints.
Structural selected sheets, not GM play or complete Focus certificates.
"""
from copy import deepcopy

LEVELS = (1, 2, 3)
CREATION_COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
LIFE_PRAYERS = frozenset((
    "Guided Regeneration", "Vital Shelter", "Basic Heal",
    "Woodland Rapport", "Venom Endurance",
))
BUILD = {
    "A": {
        "abilities": {
            "Strength": 2, "Agility": 3, "Precision": 0, "Intellect": 0,
            "Awareness": 1, "Presence": -2, "Vitality": 2,
            "Veil Affinity": 0, "Veil Control": 0,
        },
        "weapon_training": {"One-Handed Swords": 2},
        "learned": {
            "Veil Theory": 2, "Life Pillar Lore": 2,
            "Medicine": 2, "Acrobatics": 2,
        },
        "level_two_discipline": ("Survival", 1),
        "talents": ("TAL-C02", "TAL-C05", "TAL-C10"),
        "prayers": ("Guided Regeneration", "Basic Heal", "Woodland Rapport"),
        "chosen": "Guided Regeneration",
        "equipment": {
            "Leather armor": 25, "Sword": 22,
            "Medical kit": 15, "Adventuring pack": 8,
        },
        "wielded": ("Sword",),
        "free_hands": 1,
        "background": ("Home community", "Prior rural medical practice"),
        "guard_instrument": "Sword", "guard_value": 17,
        "exaltation": "EX-LR-01 Held Renewal",
    },
    "B": {
        "abilities": {
            "Strength": 2, "Agility": 2, "Precision": 0, "Intellect": 1,
            "Awareness": 0, "Presence": -2, "Vitality": 3,
            "Veil Affinity": 0, "Veil Control": 0,
        },
        "weapon_training": {"Blunt Weapons": 2},
        "learned": {
            "Medicine": 2, "Herbalism": 2, "Survival": 2,
            "Life Pillar Lore": 2,
        },
        "level_two_discipline": ("Veil Theory", 1),
        "talents": ("TAL-C05", "TAL-C01", "TAL-C09"),
        "prayers": ("Vital Shelter", "Basic Heal", "Venom Endurance"),
        "chosen": "Vital Shelter",
        "equipment": {
            "Brigandine": 95, "Mace": 16, "Shield": 16,
            "Medical kit": 15, "Adventuring pack": 8,
        },
        "wielded": ("Mace", "Shield"),
        "free_hands": 0,
        "background": ("Town watch", "Temple infirmary"),
        "guard_instrument": "Shield", "guard_value": 18,
        "exaltation": "EX-LP-01 Vital Interposition",
    },
}


def profile(role, level):
    """Return one purchased, explicitly prepared A or B character at L1-3."""
    if role not in BUILD or type(level) is not int or level not in LEVELS:
        raise ValueError("Only sourced Low Life A/B at levels 1-3")
    spec = BUILD[role]
    a = spec["abilities"]
    if sum(CREATION_COST[v] for v in a.values()) != 28:
        raise AssertionError("Nine starting Abilities must spend exactly 28")
    if sum(spec["learned"].values()) != 8 or sum(spec["weapon_training"].values()) != 2:
        raise AssertionError("Original Training budget changed")
    if sum(spec["equipment"].values()) > 150:
        raise AssertionError("Original starter purchases exceed 150 sp")
    prayers = spec["prayers"][:2 if level == 1 else 3]
    if (len(prayers) != len(set(prayers)) or
            not set(prayers) <= LIFE_PRAYERS or
            spec["chosen"] not in prayers):
        raise AssertionError("Chosen must occupy an actual prepared Life prayer")
    learned = dict(spec["learned"])
    if level >= 2:
        name, ranks = spec["level_two_discipline"]
        learned[name] = ranks
    hp = 10 + a["Vitality"]
    ap = 30 + 6 * (level-1)
    base_guard = ap // 20
    guard_bonus = int("TAL-C05" in spec["talents"][:level])
    shield_bonus = int(role == "B")
    return deepcopy({
        "archetype": "Priest", "focus": "Low", "pillar": "Life",
        "variant": role, "level": level, "abilities": a,
        "weapon_training": spec["weapon_training"],
        "learned_disciplines": learned,
        "saved_weapon_development_points": 0,
        "saved_learned_discipline_points": 0,
        "saved_talent_selections": 0,
        "equipment_sp": spec["equipment"],
        "silver_remaining": 150 - sum(spec["equipment"].values()),
        "wielded_items": spec["wielded"], "free_hands": spec["free_hands"],
        "background_familiarities": spec["background"],
        "accord": 1, "resonance": 0, "miracle_debt": 0,
        "prepared_prayers": prayers, "prepared_capacity": 2 if level == 1 else 3,
        "chosen_devotion": spec["chosen"],
        "active_devotional_rite_cap": 1,
        "selected_talents_by_level": spec["talents"][:level],
        "talents": spec["talents"][:level],
        "hp_max": hp, "vigor_max": hp*level,
        "vp_max": (2 + a["Veil Affinity"])*level,
        "turn_ap": ap, "physical_action_ap": 20, "projection_action_ap": 30,
        "general_action_ap": 24, "movement_points": 12,
        "physical_tempo": ap // 20, "projection_tempo": ap // 30,
        "normal_regen_throughput": max(a["Vitality"], 0)+3+int(
            "TAL-C02" in spec["talents"][:level]),
        "normal_guard_capacity": base_guard+guard_bonus+shield_bonus,
        "guard_instrument": spec["guard_instrument"],
        "guard_value": spec["guard_value"],
        "dodge_value": 10+a["Agility"]+a["Awareness"],
        "initiative": a["Agility"]+a["Awareness"]+(
            2 if "TAL-C01" in spec["talents"][:level] else 0),
        "tier_ceiling": 1 if level < 3 else 2,
        "universals": ("Veil Inspection",) if level < 3 else
                      ("Veil Inspection", "Blink"),
        "inspection_spent_vp": 2,
        "blink_spent_vp": 10,
        "blink_affordable_at_initial_full_vp": 10 <= (2+a["Veil Affinity"])*level,
        "basic_heal_hand_available_in_authored_loadout": spec["free_hands"] >= 1,
        "exaltation_property": spec["exaltation"] if level == 3 else None,
        "full_magic_sheet_selected": True,
        "independently_full_focus_certified": False,
    })


def verify():
    """Local invariant convenience, never a substitute for independent audit."""
    result = {}
    for role in BUILD:
        for level in LEVELS:
            p = profile(role, level)
            if (p["prepared_capacity"] != len(p["prepared_prayers"])
                    or p["vp_max"] != 2*level
                    or p["normal_regen_throughput"] != 6
                    or p["talents"] != BUILD[role]["talents"][:level]):
                raise AssertionError("Author's original Low Priest build drifted")
        result[role] = {"levels": 3, "chosen": BUILD[role]["chosen"]}
    return {"variants": result, "levels": 6, "source_selected": True,
            "external_gm_verified": False, "full_focus_certified": False}


if __name__ == "__main__":
    print(verify())
