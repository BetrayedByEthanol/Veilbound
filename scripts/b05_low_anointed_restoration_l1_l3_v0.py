"""B04/B05 Low Anointed Restoration L1–3 source-limited structural character.

One Life/Restoration bond, actual Low Focus 0-VP Embodied Signature, and
bounded isolated rules-referee examples. Externally asserted step/Intrusion/
spell predicates are NOT G0/G4/G5 source-authenticated encounter receipts.
Run: python -m scripts.b05_low_anointed_restoration_l1_l3_v0
"""
from dataclasses import replace
import json

from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, guided_regeneration_l3, mission_event, recover_destiny,
    returning_step, set_bond, set_embodiment,
)

LEVELS = (1, 2, 3)
ABILITY_COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
ABILITIES = {
    "Strength": 0, "Agility": 1, "Precision": 0, "Intellect": 2,
    "Awareness": 2, "Presence": 0, "Vitality": 2,
    "Veil Affinity": 0, "Veil Control": 0,
}
DISCIPLINES_L1 = {
    "Pillar Lore (Life)": 2, "regional/era History": 2,
    "Medicine": 2, "Throwing": 2,
}
FAMILY_ALLOCATION_L1 = {
    "Scholarly": 4, "Professional and Technical": 2,
    "Physical and Fieldcraft": 2,
}
WEAPON_TRAINING = {"One-Handed Swords": 2}
EQUIPMENT_SP = {
    "Leather armor": 25, "Sword": 22,
    "Standard adventuring pack": 8, "Basic medical kit": 15,
}
BOND = {"pillar": "Life", "aspect": "Restoration"}
MISSION = "Make recovery possible where injury or illness has taken that possibility away."
IMPRINT = "The Returning Step"
SURGE = "The Returning Steps"
TALENTS = {
    1: "TAL-A01 Imprint Recall",
    2: "TAL-C02 Enhanced Regeneration",
    3: "TAL-C05 Guard Reserve",
}
AUTHORED_RESTORATION = ("Basic Heal", "Guided Regeneration")


def profile(level):
    """Fixed character across L1→L3: no Focus-swapped spells or free selections."""
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only sourced L1–3 Low Anointed build")
    a = dict(ABILITIES)
    learned = dict(DISCIPLINES_L1)
    if level >= 2:
        learned["Navigation"] = 1
    hp = 10 + a["Vitality"]
    ap = 30 + 6 * (level - 1)
    vp = max(1, 2 + a["Veil Affinity"]) * level
    physical = ap // 20
    guard_reserve = int(level >= 3)
    regen_talent = int(level >= 2)
    return {
        "identity": "Low Anointed Returning Steps Embodied Field-Guardian",
        "archetype": "Anointed", "focus": "Low", "level": level,
        "abilities": a, "ability_points": sum(ABILITY_COST[x] for x in a.values()),
        "resonance": 0, "priest_pillar_accord": None,
        "bond": dict(BOND), "mission": MISSION, "birth_imprint": IMPRINT,
        "origin_surge": SURGE, "mission_state": "Aligned", "bond_active": True,
        "aspect_intuition": "Restoration-relevant injury and failed recovery, without secret facts",
        "birth_imprint_is_additional_spell": False,
        "learned_disciplines": learned, "learned_points": sum(learned.values()),
        "learned_families_l1": dict(FAMILY_ALLOCATION_L1),
        "weapon_training": dict(WEAPON_TRAINING),
        "weapon_development_points": sum(WEAPON_TRAINING.values()),
        "background_familiarities": [
            "Collective rehabilitation practice", "Travelling healers and patient care",
        ],
        "talents": [TALENTS[n] for n in LEVELS if n <= level],
        "talent_selections_acquired": level,
        "imprint_recall_once_per_six_hours": True,
        "enhanced_regeneration_throughput_bonus": regen_talent,
        "guard_reserve_capacity_bonus": guard_reserve,
        "guard_reserve_opportunity_bonus": 0,
        "known_bonded_techniques": list(AUTHORED_RESTORATION),
        "known_other_aspect_techniques": [],
        "priest_prepared_prayers": None, "scholar_formulas": None,
        "gifted_emotion_links": None,
        "universal": ["Veil Inspection"] + (["Blink"] if level >= 3 else []),
        "max_used_tier": 2 if level == 3 else 1,
        "equipment_sp": dict(EQUIPMENT_SP),
        "starting_budget_sp": 150,
        "starting_spent_sp": sum(EQUIPMENT_SP.values()),
        "silver_remaining_sp": 150 - sum(EQUIPMENT_SP.values()),
        "armor": 3, "wielded_weapon": "Sword",
        "sword_attack_bonus": a["Strength"] + a["Agility"] + 2,
        "sword_guard_defense": 10 + a["Strength"] + a["Agility"] + 2,
        "sword_damage": "3+d6 Cut/Pierce (Light contribution +0)",
        "sword_penetration": 2,
        "hp_max": hp, "vigor_max": hp * level, "vp_max": vp,
        "turn_ap": ap, "physical_action_ap": 20,
        "projection_action_ap": 30, "general_action_ap": 24,
        "physical_tempo": physical, "projection_tempo": ap // 30,
        "normal_guard_capacity": physical,
        "guard_capacity": physical + guard_reserve,
        "opportunity_capacity": physical,
        "initiative": a["Agility"] + a["Awareness"],
        "first_dodge": 10 + min(a["Agility"], 4) + a["Awareness"],
        "movement_points": 12,
        "natural_regen_throughput_before_talents": max(0, a["Vitality"]) + 3,
        "normal_regen_throughput": max(0, a["Vitality"]) + 3 + regen_talent,
        "medicine_check_bonus": a["Intellect"] + learned["Medicine"],
        "life_pillar_lore_bonus": a["Intellect"] + learned["Pillar Lore (Life)"],
        "signature": "Returning Step", "signature_vp": 0,
        "signature_self_only": True, "embodied_initially": True,
        "signature_requires_existing_own_turn_regeneration_step": True,
        "signature_activation_ap": 0, "signature_hp_cap": 1,
        "signature_max_range_squares": 0,
        "signature_vigor_per_hp": 1,
        "l2_living_instrument_extra_pulse": False,
        "l2_living_instrument_step_retiming": False,
        "l2_living_instrument_reactive_guard_effect": False,
        "lesser_authority": "Spare the Reserve", "lesser_destiny_cost": 1,
        "max_destiny": 2, "destiny_initial_at_creation_only": 2,
        "destiny_on_level_up": "carry state; no automatic refill",
        "destiny_recovery_per_completed_six_hours": 1,
        "l3_guided_self_primary_lesser_eligible": level == 3,
        "l3_guided_single_target_lesser_eligible": False,
        "l3_basic_heal_lesser_eligible": False,
        "basic_heal_t1_spent_vp": 2,
        "basic_heal_t2_spent_vp": 4 if level == 3 else None,
        "guided_t1_fixed_spent_vp": 2,
        "guided_t1_maintained_committed_vp": 2,
        "guided_requires_normal_activation_ap": 30,
        "guided_grants_extra_regeneration_step": False,
        "two_paid_physical_attacks_fit": ap >= 40,
        "physical_attack_plus_projection_fit": ap >= 50,
        "two_projection_actions_fit": ap >= 60,
        "blink_affordable_from_full_vp": level >= 3 and vp >= 10,
        "structural_character_build_complete": True,
        "native_encounter_receipts": False,
        "independent_full_focus_certified": False,
    }


def isolated_witness(level):
    """Source-referee positive cases, with UNTRUSTED external Step flags."""
    s = profile(level)
    actor = Anointed(level, "Low", "Restoration")
    normal = returning_step(
        actor, receipt=f"L{level}:self:step-1", target_id="self",
        recipient_hp=5, recipient_max_hp=12, recipient_vigor=4,
        authenticated_regeneration_step=True, focus_turn_id="self:turn-1",
        distance=0,
    )
    lesser = returning_step(
        normal.actor, receipt=f"L{level}:self:step-2", target_id="self",
        recipient_hp=6, recipient_max_hp=12, recipient_vigor=0, lesser=True,
        authenticated_regeneration_step=True, focus_turn_id="self:turn-2",
        distance=0,
    )
    suppressed = set_embodiment(lesser.actor, manifested=False, at_own_turn_start=True)
    restored = set_embodiment(suppressed, manifested=True, at_own_turn_start=True)
    rewarded = mission_event(lesser.actor, "restoration-community-event", gm_recognized=True)
    repeat = mission_event(rewarded, "restoration-community-event", gm_recognized=True)
    recovered = recover_destiny(replace(lesser.actor, destiny=0), 360)
    guided = None
    if level == 3:
        x = guided_regeneration_l3(
            actor, receipt="L3:self:guided:step",
            recipient_missing_hp_after_ordinary=2,
            active_paid_guided_instance=True, mode="Maintained",
            profile="Self", recipient_self=True,
            authenticated_regeneration_step=True,
            guided_bonus_unsuppressed=True,
        )
        guided = {
            "incremental_hp_without_vigor": x.additional_hp_without_vigor,
            "destiny_remaining": x.actor.destiny,
            "ordinary_maintained_guided_vp_reservation_required": 2,
            "native_g4_step_authenticated": False,
        }
    return {
        "level": level,
        "signature_ap": normal.ap_spent,
        "normal_hp": normal.hp_restored,
        "normal_self_vigor_spent": normal.recipient_vigor_spent,
        "lesser_hp": lesser.hp_restored,
        "lesser_self_vigor_spent": lesser.recipient_vigor_spent,
        "lesser_destiny_remaining": lesser.actor.destiny,
        "suppress_then_resume": not suppressed.embodied and restored.embodied,
        "mission_reward_destiny": rewarded.destiny,
        "mission_repeat_awarded": repeat.destiny != rewarded.destiny,
        "six_hour_recovery_from_zero": recovered.destiny,
        "l3_guided": guided,
        "native_attestation": False,
        "full_focus_certified": False,
    }


def verify():
    if (len(ABILITIES) != 9
            or any(type(v) is not int or v not in ABILITY_COST for v in ABILITIES.values())
            or sum(ABILITY_COST[v] for v in ABILITIES.values()) != 28
            or sum(DISCIPLINES_L1.values()) != 8
            or max(DISCIPLINES_L1.values()) > 2
            or sum(FAMILY_ALLOCATION_L1.values()) != 8
            or sum(WEAPON_TRAINING.values()) != 2
            or sum(EQUIPMENT_SP.values()) != 70):
        raise AssertionError("Low Anointed point/Training/equipment budget drift")
    for lv in LEVELS:
        s = profile(lv)
        w = isolated_witness(lv)
        if (s["ability_points"] != 28
                or s["learned_points"] != 8 + int(lv >= 2)
                or s["talent_selections_acquired"] != lv
                or len(s["talents"]) != lv
                or s["weapon_development_points"] != 2
                or (s["starting_spent_sp"], s["silver_remaining_sp"]) != (70,80)
                or (s["hp_max"], s["vigor_max"], s["vp_max"]) != (12,12*lv,2*lv)
                or s["turn_ap"] != 30+6*(lv-1)
                or s["physical_tempo"] != (2 if lv == 3 else 1)
                or s["projection_tempo"] != 1
                or s["guard_capacity"] != (3 if lv == 3 else 1)
                or s["opportunity_capacity"] != (2 if lv == 3 else 1)
                or s["normal_regen_throughput"] != (5 if lv == 1 else 6)
                or s["max_used_tier"] != (2 if lv == 3 else 1)
                or s["universal"] != (["Veil Inspection"] + (["Blink"] if lv==3 else []))
                or s["two_paid_physical_attacks_fit"] != (lv == 3)
                or s["physical_attack_plus_projection_fit"]
                or s["known_other_aspect_techniques"]
                or s["l3_guided_self_primary_lesser_eligible"] != (lv == 3)
                or s["independent_full_focus_certified"]):
            raise AssertionError("Low Anointed source resource/progression drift")
        if ((w["signature_ap"],w["normal_hp"],w["normal_self_vigor_spent"],
             w["lesser_hp"],w["lesser_self_vigor_spent"],
             w["lesser_destiny_remaining"]) != (0,1,1,1,0,1)
            or not w["suppress_then_resume"]
            or w["mission_reward_destiny"] != 2
            or w["mission_repeat_awarded"]
            or w["six_hour_recovery_from_zero"] != 1
            or (w["l3_guided"] is None) != (lv < 3)
            or w["native_attestation"]):
            raise AssertionError("Low Anointed isolated source witness drift")
    return True


if __name__ == "__main__":
    verify()
    print(json.dumps({"build": "Low Anointed Restoration L1–3",
                      "levels": [profile(n) for n in LEVELS],
                      "witnesses": [isolated_witness(n) for n in LEVELS]},
                     sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False))
