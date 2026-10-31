"""B04/B05 Medium Gifted L1–3 eight-link structural build and Ward budget witness.

Source-backed character choices and provisional Ward v0; the Ward witness
models proposed L1–3 rules but DOES NOT resolve native G4 damage/response.
No unrelated Focus Surge, Embodiment, prepared techniques, or extra casting.
Run: python -m scripts.b05_medium_gifted_l1_l3_v0
"""
from copy import deepcopy
import json

from scripts.b05_high_gifted_amplification_v0 import EMOTIONS, PILOT_LINKS
from scripts.b05_medium_gifted_conduit_design_v0 import (
    EXPRESSION, MediumGiftedWardDesign,
)

LEVELS = (1, 2, 3)
ABILITY_COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
ABILITIES = {
    "Strength": 0, "Agility": 1, "Precision": 0, "Intellect": 0,
    "Awareness": 2, "Presence": 0, "Vitality": 2,
    "Veil Affinity": 0, "Veil Control": 2,
}
LEARNED_L1 = {
    "Emotional Discipline": 2, "Disguise": 2,
    "Throwing": 2, "Medicine": 2,
}
L2_LEARNED = ("Veil Theory", 1)
WEAPONS = {"Small Blades": 2}
GEAR = {
    "Leather armor": 25, "Dagger": 4,
    "Standard adventuring pack": 8, "Basic medical kit": 15,
}
TALENT = "TAL-G01 Emotional Poise"
PLAUSIBLE = {
    "Joy": "Shared light and festival hearth-fire express joy",
    "Anger": "Focused anger pushes against a material obstacle",
}
ORDINARY_TECHNIQUES = {
    "Joy": ("Conjure Flame",),
    "Sadness": ("Basic Heal", "Guided Regeneration"),
    "Anger": ("Minor Telekinesis",),
    "Fear": ("Stone Skin",),
    "Surprise": ("Phantom Sound",),
    "Disgust": ("Weaken Restraints",),
    "Trust": ("Protective Ward",),
    "Anticipation": ("Spark of Inspiration",),
}
UPCAST_T2 = frozenset(("Conjure Flame", "Basic Heal", "Minor Telekinesis"))


def profile(level):
    """Return a fresh full starting/progression sheet, no free Conduit setup."""
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only authored L1–3 Medium Gifted pilot")
    ability = deepcopy(ABILITIES)
    learned = deepcopy(LEARNED_L1)
    if level >= 2:
        learned[L2_LEARNED[0]] = L2_LEARNED[1]
    hp = 10 + ability["Vitality"]
    ap = 30 + 6 * (level - 1)
    vp = max(1, 4 + ability["Veil Affinity"]) * level
    action_ap = 24
    return {
        "identity": "Medium Gifted Conduit Ward and travelling medic — restricted pilot",
        "archetype": "Gifted", "focus": "Medium", "level": level,
        "abilities": ability,
        "ability_points": sum(ABILITY_COST[x] for x in ability.values()),
        "resonance": 0,
        "learned_disciplines": learned,
        "learned_points": sum(learned.values()),
        "learned_family_allocation_l1": {
            "Cultural and Specialized": 4,
            "Physical and Fieldcraft": 2,
            "Professional and Technical": 2,
        },
        "weapon_training": deepcopy(WEAPONS),
        "weapon_development_points": sum(WEAPONS.values()),
        # Medium Focus gains its second selection at L3; this pilot
        # deliberately saves it rather than inventing a new paid effect.
        "talents": [TALENT],
        "talent_selections_available": 1 + int(level >= 3),
        "saved_talent_selections": int(level >= 3),
        "background_familiarities": ["Village festival work", "Field medical practice"],
        "emotion_aspect_links": {emotion: {
            "pillar": PILOT_LINKS[emotion][0],
            "aspect": PILOT_LINKS[emotion][1],
            "compatibility": PILOT_LINKS[emotion][2],
            "creation_interpretation": PLAUSIBLE.get(emotion),
        } for emotion in EMOTIONS},
        "authored_linked_techniques": {
            emotion: list(ORDINARY_TECHNIQUES[emotion]) for emotion in EMOTIONS
        },
        "authored_upcast_t2": sorted(UPCAST_T2) if level == 3 else [],
        "max_used_tier": 2 if level == 3 else 1,
        "active_emotion": None, "emotion_intensity": None,
        "individually_learned_pillar_techniques": None,
        "prepared_techniques": None,
        "universal": ["Veil Inspection"] + (["Blink"] if level == 3 else []),
        "equipment_sp": deepcopy(GEAR),
        "starting_budget_sp": 150,
        "starting_spent_sp": sum(GEAR.values()),
        "silver_remaining_sp": 150 - sum(GEAR.values()),
        "armor": 3, "wielded_weapon": "Dagger",
        "dagger_attack_bonus": ability["Agility"] + ability["Precision"] + 2,
        "dagger_guard_defense": 10 + ability["Agility"] + ability["Precision"] + 2,
        "dagger_damage": "2+d4 Cut/Pierce (Light contribution +0)",
        "thrown_flame_attack_bonus": ability["Agility"] + ability["Precision"] + learned["Throwing"],
        "hp_max": hp, "vigor_max": hp * level, "vp_max": vp,
        "turn_ap": ap, "physical_action_ap": action_ap,
        "projection_action_ap": action_ap, "general_action_ap": action_ap,
        "physical_tempo": ap // action_ap,
        "projection_tempo": ap // action_ap,
        "guard_capacity": ap // action_ap,
        "opportunity_capacity": ap // action_ap,
        "movement_points": 12,
        "initiative": ability["Agility"] + ability["Awareness"],
        "first_dodge": 10 + min(ability["Agility"], 4) + ability["Awareness"],
        "normal_regen_throughput": max(0, ability["Vitality"]) + 1,
        "emotional_discipline_check_bonus": ability["Awareness"] + learned["Emotional Discipline"],
        "instability_check_bonus": ability["Veil Control"] + learned["Emotional Discipline"],
        "conduit_form": "Ward", "conduit_anchor": "self",
        "conduit_slots": 1 if level < 3 else 2,
        "conduit_grades": {"I": 1, "II": 2, "III": 3},
        "conduit_initial_general_ap": 24,
        "reconduction_general_ap": 24,
        "reconduction_spent_vp": 3,
        "conduit_emotion_expressions": {
            "Fear": "Holdfast (self Physical HP, one Grade-sized Pulse/Window)",
            "Trust": "Shared Reserve (orthogonally adjacent other ally Direct Vigor, one Grade-sized Pulse/Window)",
        },
        "conduit_initially_established": False,
        "two_initial_conduits_same_turn": 2 * action_ap <= ap,
        "normal_t1_flame_vp": 2,
        "normal_t2_flame_vp": 4 if level == 3 else None,
        "deepening_plus_t1_flame_same_turn": 24 + action_ap <= ap,
        "blink_affordable_without_commitment": level == 3 and vp >= 10,
        "blink_affordable_with_two_grade_ii_conduits": level == 3 and vp - 4 >= 10,
    }


def ward_budget(level, *, grade=2, emotion="Fear"):
    """Isolated source-matched AP/VP witness; no actual combat mitigation."""
    if type(grade) is not int or grade not in (1, 2, 3):
        raise ValueError("Only Grade I–III")
    model = MediumGiftedWardDesign(level, veil_affinity=ABILITIES["Veil Affinity"])
    model.begin_turn(emotion)
    conduit = model.establish(grade=grade)
    return {
        "level": level, "emotion": emotion, "grade": grade,
        "window": model.window, "status": conduit.status,
        "ap_remaining": model.ap, "available_vp": model.available,
        "committed_vp": model.committed, "spent_vp": model.spent,
        "slots_used": len(model.conduits), "slots_max": model.slot_cap,
    }


def verify():
    """Verify canonical creation constraints and the restricted Ward budget."""
    assert sum(ABILITY_COST[x] for x in ABILITIES.values()) == 28
    assert all(-2 <= x <= 4 for x in ABILITIES.values())
    assert sum(LEARNED_L1.values()) == 8
    assert all(0 <= x <= 2 for x in LEARNED_L1.values())
    assert sum(WEAPONS.values()) == 2
    assert sum(GEAR.values()) == 52
    assert len(EMOTIONS) == len(PILOT_LINKS) == len(ORDINARY_TECHNIQUES) == 8
    assert len({x[0] for x in PILOT_LINKS.values()}) == 8
    assert len({x[1] for x in PILOT_LINKS.values()}) == 8
    assert set(PLAUSIBLE) == {e for e in EMOTIONS if PILOT_LINKS[e][2] == "P"}
    for emotion, (pillar, aspect, _, _) in EXPRESSION.items():
        assert PILOT_LINKS[emotion][:2] == (pillar, aspect)
    for level in LEVELS:
        s = profile(level)
        assert s["ability_points"] == 28
        assert s["learned_points"] == 8 + int(level >= 2)
        assert s["starting_spent_sp"] + s["silver_remaining_sp"] == 150
        assert (s["hp_max"], s["vigor_max"], s["vp_max"]) == (12, 12 * level, 4 * level)
        assert s["talents"] == [TALENT]
        assert (s["talent_selections_available"], s["saved_talent_selections"]) == (
            1 + int(level >= 3), int(level >= 3))
        assert s["physical_tempo"] == s["projection_tempo"] == s["guard_capacity"] == 1
        assert not s["two_initial_conduits_same_turn"]
        assert not s["deepening_plus_t1_flame_same_turn"]
        assert s["conduit_slots"] == (1 if level < 3 else 2)
        assert (s["first_dodge"], s["dagger_guard_defense"]) == (13, 13)
        assert len(s["talents"]) == 1
        assert ward_budget(level)["committed_vp"] == 2
    return True


if __name__ == "__main__":
    verify()
    print(json.dumps({"build": "Medium Gifted L1–3 structural Ward pilot",
                      "levels": [profile(level) for level in LEVELS]},
                     indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False))
