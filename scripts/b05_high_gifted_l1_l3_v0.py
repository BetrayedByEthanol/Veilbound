"""B04/B05 source-constrained High Gifted L1–3 structural character candidate.

A legal eight-link example with explicit choices and ordinary spell access;
this is not a native G0/G2/G3/G4/G5 encounter, a miscast action authorization,
or independent full MVP certification.
Run: python -m scripts.b05_high_gifted_l1_l3_v0
"""
from copy import deepcopy
import json

from scripts.b05_high_gifted_amplification_v0 import (
    EMOTIONS, PILOT_LINKS, HighGiftedWindow, amplified_parameters,
    surge_surcharge, thrown_flame,
)

LEVELS = (1, 2, 3)
ABILITY_COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
ABILITIES = {
    "Strength": 0, "Agility": 2, "Precision": 0, "Intellect": 0,
    "Awareness": 2, "Presence": 0, "Vitality": 2,
    "Veil Affinity": 0, "Veil Control": 1,
}
WEAPON_TRAINING = {"Small Blades": 2}
DISCIPLINES_L1 = {
    "Emotional Discipline": 2, "Disguise": 2,
    "Throwing": 2, "Medicine": 2,
}
DISCIPLINE_L2 = ("Veil Theory", 1)
TALENT = "TAL-G01 Emotional Poise"
GEAR_SP = {
    "Leather armor": 25, "Dagger": 4,
    "Standard adventuring pack": 8, "Basic medical kit": 15,
}
FAMILIARITIES = (
    "Village market and festivals", "Travelling healers and their patients",
)
# Fixed, documented 6 Strong + 2 Plausible pilot. The two Plausible
# connections require a coherent interpretation ONCE at creation.
PLAUSIBLE_EXPLANATIONS = {
    "Joy": "Joy in bright communal hearth-fire, lanterns and celebratory flame",
    "Anger": "Anger expressed as a forceful impulse to move an obstacle",
}
# Individually authored Tier-1 spell identities, not a universal ability to
# amplify these profiles or to cast them while a different emotion is active.
AUTHORED_ACCESS = {
    "Joy": ("Conjure Flame",),
    "Sadness": ("Basic Heal", "Guided Regeneration"),
    "Anger": ("Minor Telekinesis",),
    "Fear": ("Stone Skin",),
    "Surprise": ("Phantom Sound",),
    "Disgust": ("Weaken Restraints",),
    "Trust": ("Protective Ward",),
    "Anticipation": ("Spark of Inspiration",),
}
# A Tier-2 ceiling is NOT a Tier-2 version of every known Tier-1 spell.
AUTHORED_UPCAST_T2 = frozenset({
    "Conjure Flame", "Basic Heal", "Minor Telekinesis",
})


def profile(level):
    """One explicit persistent build; no reroll, free talent or preparation."""
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only levels 1, 2, 3 have an authored witness")
    ability = deepcopy(ABILITIES)
    learned = deepcopy(DISCIPLINES_L1)
    if level >= 2:
        learned[DISCIPLINE_L2[0]] = DISCIPLINE_L2[1]
    hp = 10 + ability["Vitality"]
    ap = 30 + 6 * (level - 1)
    vp = max(1, 6 + ability["Veil Affinity"]) * level
    flame_tier = 2 if level >= 3 else 1
    flame = thrown_flame(flame_tier)
    result = {
        "identity": "High Gifted Eight-Emotion Fire-Linked Explorer — pilot candidate",
        "archetype": "Gifted", "focus": "High", "level": level,
        "abilities": ability,
        "ability_points": sum(ABILITY_COST[x] for x in ability.values()),
        "resonance": 0, "priest_pillar_accord": None,
        "talents": [TALENT], "talent_selections_available": 1,
        "learned_disciplines": learned,
        "learned_points": sum(learned.values()),
        "learned_family_allocation_l1": {
            "Cultural and Specialized": 4,
            "Physical and Fieldcraft": 2,
            "Professional and Technical": 2,
        },
        "weapon_training": deepcopy(WEAPON_TRAINING),
        "weapon_development_points": sum(WEAPON_TRAINING.values()),
        "background_familiarities": list(FAMILIARITIES),
        "emotion_aspect_links": {emotion: {
            "pillar": PILOT_LINKS[emotion][0],
            "aspect": PILOT_LINKS[emotion][1],
            "compatibility": PILOT_LINKS[emotion][2],
            "creation_interpretation": PLAUSIBLE_EXPLANATIONS.get(emotion),
        } for emotion in EMOTIONS},
        "authored_linked_techniques": {
            emotion: list(AUTHORED_ACCESS[emotion]) for emotion in EMOTIONS
        },
        "authored_upcast_t2": (sorted(AUTHORED_UPCAST_T2) if level >= 3 else []),
        "active_emotion": None,  # chosen at an actual Emotion Establishment Step
        "emotion_intensity": None,  # cannot assume natural Heightening
        "prepared_techniques": None,
        "individually_learned_pillar_techniques": None,
        "universal": ["Veil Inspection"] + (["Blink"] if level >= 3 else []),
        "max_used_tier": 1 if level < 3 else 2,
        "equipment_sp": deepcopy(GEAR_SP),
        "starting_budget_sp": 150,
        "starting_spent_sp": sum(GEAR_SP.values()),
        "silver_remaining_sp": 150 - sum(GEAR_SP.values()),
        "armor": 3,
        "wielded_weapon": "Dagger",
        "dagger_attack_bonus": ability["Agility"] + ability["Precision"] + 2,
        "dagger_guard_defense": 10 + ability["Agility"] + ability["Precision"] + 2,
        "dagger_damage": "2+d4 Cut/Pierce (Light contribution +0)",
        "hp_max": hp, "vigor_max": hp * level, "vp_max": vp,
        "turn_ap": ap, "physical_action_ap": 30,
        "projection_action_ap": 20, "general_action_ap": 24,
        "physical_tempo": ap // 30,
        "projection_tempo": ap // 20,
        "guard_capacity": ap // 30,
        "movement_points": 12,
        "initiative": ability["Agility"] + ability["Awareness"],
        "first_dodge": 10 + min(ability["Agility"], 4) + ability["Awareness"],
        "normal_regen_throughput": max(0, ability["Vitality"]) + 1,
        "emotional_discipline_check_bonus": (
            ability["Awareness"] + learned["Emotional Discipline"]
        ),
        "instability_check_bonus": (
            ability["Veil Control"] + learned["Emotional Discipline"]
        ),
        "thrown_flame_attack_bonus": (
            ability["Agility"] + ability["Precision"] + learned["Throwing"]
        ),
        "thrown_flame_t1_ap": 20,
        "thrown_flame_t1_vp": 2,
        "thrown_flame_t1_surge_spent_vp": surge_surcharge(thrown_flame(1)),
        "thrown_flame_t1_reach_max_squares": amplified_parameters(
            thrown_flame(1), ("Reach",)
        )["max_range"],
        "thrown_flame_t1_precision_attack_bonus": (
            ability["Agility"] + ability["Precision"] + learned["Throwing"] + 1
        ),
        "thrown_flame_available_tier": flame_tier,
        "thrown_flame_available_tier_vp": flame.spent_vp,
        "thrown_flame_available_tier_surge_spent_vp": surge_surcharge(flame),
        "two_regular_flame_actions_fit": 2 * 20 <= ap,
        "deepen_plus_flame_same_turn": 24 + 20 <= ap,
        "overload_plus_flame_same_turn": 24 + 20 <= ap,
        "blink_affordable_from_full_vp": level >= 3 and vp >= 10,
    }
    return result


def verify():
    """Fail closed if this candidate ceases to be a legal source-backed build."""
    assert sum(ABILITY_COST[x] for x in ABILITIES.values()) == 28
    assert all(-2 <= x <= 4 for x in ABILITIES.values())
    assert sum(DISCIPLINES_L1.values()) == 8
    assert max(DISCIPLINES_L1.values()) <= 2
    assert sum(WEAPON_TRAINING.values()) == 2
    assert sum(GEAR_SP.values()) == 52
    assert len(EMOTIONS) == len(PILOT_LINKS) == len(AUTHORED_ACCESS) == 8
    assert len({v[0] for v in PILOT_LINKS.values()}) == 8
    assert len({v[1] for v in PILOT_LINKS.values()}) == 8
    assert sum(v[2] == "P" for v in PILOT_LINKS.values()) == 2
    assert set(PLAUSIBLE_EXPLANATIONS) == {
        e for e in EMOTIONS if PILOT_LINKS[e][2] == "P"
    }
    for level in LEVELS:
        s = profile(level)
        assert s["ability_points"] == 28
        assert s["learned_points"] == 8 + int(level >= 2)
        assert s["weapon_development_points"] == 2
        assert s["starting_spent_sp"] + s["silver_remaining_sp"] == 150
        assert (s["hp_max"], s["vigor_max"], s["vp_max"]) == (12, 12*level, 6*level)
        assert s["guard_capacity"] == s["physical_tempo"]
        assert s["first_dodge"] == 14
        assert not s["deepen_plus_flame_same_turn"]
        assert not s["overload_plus_flame_same_turn"]
        assert s["two_regular_flame_actions_fit"] == (level >= 3)
        assert s["thrown_flame_t1_surge_spent_vp"] == 1
        assert s["thrown_flame_available_tier_surge_spent_vp"] == 1
        assert len(s["talents"]) == 1
    return True


if __name__ == "__main__":
    verify()
    print(json.dumps({"build": "High Gifted L1-3 structural candidate",
                      "levels": [profile(level) for level in LEVELS]},
                     indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False))