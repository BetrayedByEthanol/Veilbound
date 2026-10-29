"""B04/B05 Medium Anointed Restoration L1–3 structural character and isolated witnesses.

No native G0/G4/G5 event authentication: externally supplied consent, paid
actions, legal step, range, refusal and suppression predicates are NOT receipts.
Run: python -m scripts.b05_medium_anointed_restoration_l1_l3_v0
"""
from dataclasses import replace
import json

from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, guided_regeneration_l3, invest, mission_event, recover_destiny,
    returning_step, set_bond,
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
WEAPON_TRAINING = {"Small Blades": 2}
EQUIPMENT_SP = {
    "Leather armor": 25, "Dagger": 4,
    "Standard adventuring pack": 8, "Basic medical kit": 15,
}
BOND = {"pillar": "Life", "aspect": "Restoration"}
MISSION = "Make recovery possible where injury or illness has taken that possibility away."
IMPRINT = "The Returning Step"
SURGE = "The Returning Steps"
TALENTS = {1: "TAL-A01 Imprint Recall", 3: "TAL-U03 Field Diagnosis"}
RESTORATION_TECHNIQUES = ("Basic Heal", "Guided Regeneration")


def profile(level):
    """One fixed bonded person with two actually selected Medium Talent awards."""
    if type(level) is not int or level not in LEVELS:
        raise ValueError("L1–3 only")
    a = dict(ABILITIES)
    skills = dict(DISCIPLINES_L1)
    if level >= 2:
        skills["Navigation"] = 1
    hp = 10 + a["Vitality"]
    ap = 30 + 6 * (level - 1)
    vp = max(1, 4 + a["Veil Affinity"]) * level
    return {
        "identity": "Medium Anointed Returning Steps Invested Patient Practitioner",
        "archetype": "Anointed", "focus": "Medium", "level": level,
        "abilities": a, "ability_points": sum(ABILITY_COST[n] for n in a.values()),
        "resonance": 0, "priest_pillar_accord": None,
        "bond": dict(BOND), "mission": MISSION, "birth_imprint": IMPRINT,
        "origin_surge": SURGE, "mission_state": "Aligned", "bond_active": True,
        "birth_imprint_creates_extra_spell": False,
        "aspect_intuition": "Restoration patterns only; no automatic diagnosis",
        "learned_disciplines": skills, "learned_points": sum(skills.values()),
        "learned_families_l1": dict(FAMILY_ALLOCATION_L1),
        "weapon_training": dict(WEAPON_TRAINING), "weapon_development_points": 2,
        "background_familiarities": [
            "Communal rehabilitation traditions", "Travelling medical practitioners",
        ],
        "talents": [TALENTS[n] for n in (1, 3) if n <= level],
        "talent_selections_acquired": 1 + int(level >= 3),
        "field_diagnosis_requires_direct_medicine": True,
        "field_diagnosis_bounded_once_per_six_hours": level >= 3,
        "known_bonded_techniques": list(RESTORATION_TECHNIQUES),
        "known_other_aspect_techniques": [],
        "prepared_prayers": None, "scholar_formulae": None,
        "emotion_aspect_links": None,
        "universal": ["Veil Inspection"] + (["Blink"] if level == 3 else []),
        "max_used_tier": 2 if level == 3 else 1,
        "equipment_sp": dict(EQUIPMENT_SP), "starting_budget_sp": 150,
        "starting_spent_sp": sum(EQUIPMENT_SP.values()),
        "silver_remaining_sp": 150 - sum(EQUIPMENT_SP.values()),
        "armor": 3, "wielded_weapon": "Dagger",
        "dagger_attack_bonus": a["Agility"] + a["Precision"] + 2,
        "dagger_guard_defense": 10 + a["Agility"] + a["Precision"] + 2,
        "dagger_damage": "2+d4 Cut/Pierce (Light Strength contribution +0)",
        "hp_max": hp, "vigor_max": hp * level, "vp_max": vp,
        "turn_ap": ap, "physical_action_ap": 24,
        "projection_action_ap": 24, "general_action_ap": 24,
        "physical_tempo": ap // 24, "projection_tempo": ap // 24,
        "guard_capacity": ap // 24, "opportunity_capacity": ap // 24,
        "initiative": a["Agility"] + a["Awareness"],
        "first_dodge": 10 + min(a["Agility"], 4) + a["Awareness"],
        "movement_points": 12,
        "normal_regen_throughput": max(0, a["Vitality"]) + 2,
        "medicine_check_bonus": a["Intellect"] + skills["Medicine"],
        "life_pillar_lore_bonus": a["Intellect"] + skills["Pillar Lore (Life)"],
        "signature": "Returning Step", "signature_vp": 0,
        "signature_hp_per_genuine_patient_step": 1,
        "signature_pulse_activation_ap": 0,
        "signature_max_range_squares": 3,
        "signature_requires_real_patient_step": True,
        "signature_requires_current_visible_invested_patient": True,
        "investment_setup_ap": 24, "investment_setup_vp": 0,
        "investment_one_vessel_only": True,
        "investment_requires_patient_consent": True,
        "l2_channel_through_vessel_extra_action": False,
        "l2_channel_through_vessel_remote_cast": False,
        "lesser_authority": "Spare the Reserve", "lesser_destiny_cost": 1,
        "max_destiny": 2, "destiny_initial_at_creation_only": 2,
        "destiny_on_level_up": "carry state; no automatic refill",
        "destiny_recovery_per_completed_six_hours": 1,
        "l3_guided_single_target_vessel_lesser_eligible": level == 3,
        "l3_basic_heal_lesser_eligible": False,
        "basic_heal_t1_spent_vp": 2,
        "basic_heal_t2_spent_vp": 4 if level == 3 else None,
        "guided_t1_fixed_spent_vp": 2,
        "guided_t1_maintained_committed_vp": 2,
        "guided_grants_extra_regeneration_step": False,
        "one_investment_plus_projection_same_turn": ap >= 48,
        "two_projection_actions_same_turn": ap >= 48,
        "blink_affordable_from_full_vp": level == 3 and vp >= 10,
        "structural_character_build_complete": True,
        "independent_full_focus_certified": False,
        "native_encounter_receipts": False,
    }


def isolated_witness(level):
    """Only rule-referee outputs with caller-assumed legal source predicates."""
    s = profile(level)
    a, setup_ap = invest(
        Anointed(level, "Medium", "Restoration"), "patient-a",
        ap_available=s["turn_ap"], legal_vessel=True,
        consent_or_other_delivery_valid=True,
    )
    normal = returning_step(
        a, receipt=f"L{level}:pulse-a", target_id="patient-a",
        recipient_hp=5, recipient_max_hp=12, recipient_vigor=4,
        authenticated_regeneration_step=True, focus_turn_id="patient-a:turn-1",
        distance=3, path_visible=True,
    )
    # A second pulse requires the patient's NEXT genuine step, not another
    # action or the same step; witness flags DO NOT authenticate a native step.
    lesser = returning_step(
        normal.actor, receipt=f"L{level}:pulse-b", target_id="patient-a",
        recipient_hp=6, recipient_max_hp=12, recipient_vigor=0, lesser=True,
        authenticated_regeneration_step=True, focus_turn_id="patient-a:turn-2",
        distance=3,
    )
    reward = mission_event(lesser.actor, "community-recovery", gm_recognized=True)
    no_repeat = mission_event(reward, "community-recovery", gm_recognized=True)
    recovered = recover_destiny(replace(lesser.actor, destiny=0), 360)
    guided = None
    if level == 3:
        x = guided_regeneration_l3(
            a, receipt="L3:guided:patient-step", recipient_missing_hp_after_ordinary=2,
            active_paid_guided_instance=True, mode="Maintained",
            profile="Single Target", authenticated_regeneration_step=True,
            guided_bonus_unsuppressed=True, vessel_matches=True,
        )
        guided = {
            "one_incremental_vigor_free_hp": x.additional_hp_without_vigor,
            "destiny_remaining": x.actor.destiny,
            "requires_external_paid_guided_instance": True,
            "native_step_attested": False,
        }
    return {
        "level": level, "investment_ap": setup_ap,
        "signature_activation_ap": normal.ap_spent,
        "normal_hp": normal.hp_restored,
        "normal_recipient_vigor_spent": normal.recipient_vigor_spent,
        "lesser_hp": lesser.hp_restored,
        "lesser_recipient_vigor_spent": lesser.recipient_vigor_spent,
        "lesser_destiny_remaining": lesser.actor.destiny,
        "mission_reward_destiny": reward.destiny,
        "mission_repeat_awarded": no_repeat.destiny != reward.destiny,
        "six_hour_recovery_from_zero": recovered.destiny,
        "l3_guided": guided, "native_attestation": False,
    }


def verify():
    if (len(ABILITIES) != 9 or any(type(n) is not int or n not in ABILITY_COST for n in ABILITIES.values())
            or sum(ABILITY_COST[n] for n in ABILITIES.values()) != 28
            or sum(DISCIPLINES_L1.values()) != 8
            or max(DISCIPLINES_L1.values()) > 2
            or sum(FAMILY_ALLOCATION_L1.values()) != 8
            or sum(WEAPON_TRAINING.values()) != 2
            or sum(EQUIPMENT_SP.values()) != 52):
        raise AssertionError("Initial point/Training/equipment budget drift")
    for lv in LEVELS:
        p, w = profile(lv), isolated_witness(lv)
        if (p["ability_points"] != 28 or p["learned_points"] != 8+int(lv>=2)
            or p["talent_selections_acquired"] != (2 if lv==3 else 1)
            or len(p["talents"]) != p["talent_selections_acquired"]
            or p["max_used_tier"] != (2 if lv==3 else 1)
            or p["starting_spent_sp"] + p["silver_remaining_sp"] != 150
            or (p["hp_max"],p["vigor_max"],p["vp_max"]) != (12,12*lv,4*lv)
            or p["turn_ap"] != 30+6*(lv-1)
            or p["physical_tempo"] != 1 or p["projection_tempo"] != 1
            or p["guard_capacity"] != 1 or p["opportunity_capacity"] != 1
            or p["signature_max_range_squares"] != 3
            or p["one_investment_plus_projection_same_turn"]
            or p["two_projection_actions_same_turn"]
            or p["known_other_aspect_techniques"]
            or p["l3_guided_single_target_vessel_lesser_eligible"] != (lv == 3)
            or p["independent_full_focus_certified"]):
            raise AssertionError("Medium Anointed level/build drift")
        if ((w["investment_ap"],w["signature_activation_ap"],w["normal_hp"],
             w["normal_recipient_vigor_spent"],w["lesser_hp"],
             w["lesser_recipient_vigor_spent"],w["lesser_destiny_remaining"])
            != (24,0,1,1,1,0,1)
            or w["mission_reward_destiny"] != 2 or w["mission_repeat_awarded"]
            or w["six_hour_recovery_from_zero"] != 1
            or (w["l3_guided"] is None) != (lv < 3)
            or w["native_attestation"]):
            raise AssertionError("Medium invested legal-pulse witness drift")
    return True


if __name__ == "__main__":
    verify()
    print(json.dumps({"build": "Medium Anointed Restoration L1–3",
                      "levels": [profile(n) for n in LEVELS],
                      "witnesses": [isolated_witness(n) for n in LEVELS]},
                     sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False))
