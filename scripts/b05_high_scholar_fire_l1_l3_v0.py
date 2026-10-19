"""B05/B07: High Scholar Fire L1-3 structural character ledger (v0).

This is a *candidate sheet* for Phase 3's unchanged F numeric role,
not a new Archetype or an independently certified Focus/encounter.
Only explicit authored High Scholar composite pairings are represented.
Run: python -m scripts.b05_high_scholar_fire_l1_l3_v0
"""
import json

LEVELS = (1, 2, 3)
ABILITIES = {
    "Strength": 2, "Agility": 3, "Precision": 0,
    "Intellect": 0, "Awareness": 1, "Presence": -2,
    "Vitality": 2, "Veil Affinity": 0, "Veil Control": 0,
}
ABILITY_COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
L1_DISCIPLINES = {
    "Veil Theory": 2, "Pillar Lore (Fire)": 2,
    "Throwing": 2, "Medicine": 2,
}
L2_DISCIPLINE = ("Alchemy", 1)
WEAPON_TRAINING = {"Small Blades": 2}
STARTING_GEAR_SP = {
    "Leather armor": 25, "Dagger": 4, "Standard adventuring pack": 8,
}
KNOWN_L1 = (
    "Conjure Flame", "Stone Skin", "Basic Heal",
    "Minor Telekinesis", "Phantom Sound",
)
KNOWN_L2_ADD = "Vital Shelter"
TALENT_L1 = "TAL-U01 Veil Insight"
# These are exact, ordered, technique-specific authorized composites.
# No automatic Thrown Projectile partner for Conjure Flame exists here.
FORMULAS = (
    {"primary": "Stone Skin", "secondary": "Basic Heal",
     "profile": "Self", "delivery": "normal on-turn Projection",
     "mode": "Stone Skin maintained + Basic Heal instantaneous Secondary"},
    {"primary": "Stone Skin", "secondary": "Vital Shelter",
     "profile": "Self", "delivery": "normal on-turn Projection",
     "mode": "Stone Skin maintained + Vital Shelter subordinate maintained Secondary"},
)
B06_ROLE = "F"


def formula_cost(formula, level):
    """Legal T1 composite example with VA=0; separate Spent/Committed."""
    if formula not in FORMULAS or type(level) is not int or level not in LEVELS:
        raise ValueError("Only the authored Self formulae at levels 1-3 are supported")
    # Stone Skin commits ceil(Max VP / 3) = 2 * level at VA=0.
    reserve = 2 * level
    if formula["secondary"] == "Basic Heal":
        return {"action_ap": 20, "committed_vp": reserve,
                "spent_vp": 2, "vp_required": reserve + 2,
                "secondary_effect": "Basic Heal Self Secondary: 1 HP and 3 Vigor at T1, VC0"}
    # Vital Shelter subordinate maintained Self Secondary: 2 committed
    # and 1 spent, with S4 one-time Vigor protection budget at VC0.
    return {"action_ap": 20, "committed_vp": reserve + 2,
            "spent_vp": 1, "vp_required": reserve + 3,
            "secondary_effect": "Vital Shelter Self Secondary: Vigor budget 4 at VC0"}


def profile(level):
    """Return source-grounded, explicitly selected L1->L3 character values."""
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only character levels 1, 2, 3 are authored")
    a = ABILITIES
    hp = 10 + a["Vitality"]
    max_vp = max(1, 6 + a["Veil Affinity"]) * level
    ap = 30 + 6 * (level - 1)
    known = list(KNOWN_L1) + ([KNOWN_L2_ADD] if level >= 2 else [])
    learned = dict(L1_DISCIPLINES)
    if level >= 2:
        learned[L2_DISCIPLINE[0]] = L2_DISCIPLINE[1]
    formulas = [dict(f) for f in FORMULAS[:1 if level == 1 else 2]] if level < 3 else []
    return {
        "identity": "High Scholar Fire Thrower — Phase 3 F structural candidate",
        "archetype": "Scholar", "focus": "High", "level": level,
        "resonance": 0, "priest_pillar_accord": None,
        "abilities": dict(a),
        "ability_points": sum(ABILITY_COST[v] for v in a.values()),
        "weapon_development_points": sum(WEAPON_TRAINING.values()),
        "weapon_training": dict(WEAPON_TRAINING),
        "learned_disciplines": learned,
        "learned_points": sum(learned.values()),
        "background_familiarities": [
            "Arcane study community", "Local practical herbal and medical work"
        ],
        "talents": [TALENT_L1],
        "known_pillar_techniques": known,
        "known_capacity": 5 if level == 1 else 6,
        "prepared_composite_formulas": formulas,
        "prepared_formula_capacity": 1 if level == 1 else 2 if level == 2 else 0,
        "formula_fluency": level >= 3,
        "universal": ["Veil Inspection"] + (["Blink"] if level >= 3 else []),
        "max_used_tier": 1 if level < 3 else 2,
        "starting_silver_budget": 150,
        "starting_equipment_sp": dict(STARTING_GEAR_SP),
        "starting_silver_spent": sum(STARTING_GEAR_SP.values()),
        "starting_silver_left": 150 - sum(STARTING_GEAR_SP.values()),
        "leather_armor": 3,
        "dagger_held_in_phase3": False,
        "guard_in_phase3": None,
        "dagger_guard_if_legally_wielded": (
            10 + a["Agility"] + a["Precision"] + WEAPON_TRAINING["Small Blades"]
        ),
        "dagger_attack_if_wielded": (
            a["Agility"] + a["Precision"] + WEAPON_TRAINING["Small Blades"]
        ),
        "dagger_damage_if_wielded": "3+d4 Cut/Pierce",
        "hp_max": hp, "vigor_max": hp * level, "vp_max": max_vp,
        "turn_ap": ap, "physical_action_ap": 30,
        "projection_action_ap": 20, "general_action_ap": 24,
        "physical_tempo": ap // 30, "projection_tempo": ap // 20,
        "guard_capacity": ap // 30,
        "initiative": a["Agility"] + a["Awareness"],
        "first_dodge": 10 + min(a["Agility"], 4) + a["Awareness"],
        "movement_points": 12,
        "normal_regen_throughput": max(0, a["Vitality"]) + 1,
        "thrown_flame_attack": (
            a["Agility"] + a["Precision"] + learned["Throwing"]
        ),
        "thrown_flame_t1": "Fire 2 HP + Vigor (2+ceil(d8/3))",
        "thrown_flame_range_squares": [1, 3],
        "thrown_flame_t1_spent_vp": 2,
        "thrown_flame_activation_ap": 20,
        "t1_flame_casts_at_full_vp": min(ap // 20, max_vp // 2),
        "t2_flame_casts_at_full_vp": min(ap // 20, max_vp // 4) if level >= 3 else 0,
        "stone_skin_committed_vp": (max_vp + 2) // 3,
        "stone_skin_resistance_vc0": 2,
        "l1_stone_heal_formula_cost": formula_cost(FORMULAS[0], level),
        "stone_shelter_formula_cost": (
            formula_cost(FORMULAS[1], level) if level >= 2 else None
        ),
        "blink_affordable_from_full_vp": level >= 3 and max_vp >= 10,
        "t1_flame_and_physical_action_same_turn": 20 + 30 <= ap,
    }


def verify():
    """Reconcile *all* currently simulated F input fields and legal ledgers."""
    from scripts.b06_hunter_tactical_diversity_v0 import ROLE

    assert sum(ABILITY_COST[v] for v in ABILITIES.values()) == 28
    assert sum(L1_DISCIPLINES.values()) == 8
    assert sum(WEAPON_TRAINING.values()) == 2
    assert sum(STARTING_GEAR_SP.values()) == 37
    role = ROLE[B06_ROLE]
    for level in LEVELS:
        s = profile(level)
        assert s["ability_points"] == 28
        assert s["weapon_development_points"] == 2
        assert s["learned_points"] == 8 + (level >= 2)
        assert max(s["learned_disciplines"].values()) <= 2
        assert len(s["known_pillar_techniques"]) == s["known_capacity"]
        assert len(set(s["known_pillar_techniques"])) == len(s["known_pillar_techniques"])
        assert len(s["prepared_composite_formulas"]) == (
            s["prepared_formula_capacity"] if level < 3 else 0
        )
        assert s["starting_silver_spent"] + s["starting_silver_left"] == 150
        assert s["projection_tempo"] == s["turn_ap"] // 20
        assert s["guard_capacity"] == s["physical_tempo"]
        assert not s["t1_flame_and_physical_action_same_turn"]
        for field, source in (
            ("hp_max", "hp"), ("leather_armor", "armor"),
            ("normal_regen_throughput", "regen"), ("initiative", "init"),
            ("thrown_flame_attack", "attack"),
            ("thrown_flame_activation_ap", "action_ap"),
        ):
            assert s[field] == role[source], (field, source)
        assert role["focus"] == "High"
        assert (role["vit"], role["agi"], role["awa"]) == (2, 3, 1)
        assert (role["kind"], role["base"], role["die"], role["pen"],
                role["guard"], role["guard_extra"]) == (
                    "flame", 2, None, 0, None, 0)
        assert s["guard_in_phase3"] is None
        assert s["first_dodge"] == 14
    return True


if __name__ == "__main__":
    verify()
    print(json.dumps({"build": "High Scholar Fire L1-3 v0",
                      "levels": [profile(level) for level in LEVELS]},
                     indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False))
