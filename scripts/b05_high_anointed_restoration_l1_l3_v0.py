"""B04/B05 — source-limited High Anointed Restoration L1–3 structural build.

A single bonded Life/Restoration character across three levels, with isolated
canonical Signature/Authority examples. Caller-asserted legal receipts are
NOT source-authenticated G0/G4/G5 encounter proof or a full Focus certificate.
Run: python -m scripts.b05_high_anointed_restoration_l1_l3_v0
"""
from copy import deepcopy
import json

from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, mission_event, recover_destiny, returning_step,
    guided_regeneration_l3,
)

LEVELS = (1, 2, 3)
COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
ABILITIES = {
    "Strength": 0, "Agility": 1, "Precision": 0, "Intellect": 2,
    "Awareness": 2, "Presence": 0, "Vitality": 2,
    "Veil Affinity": 0, "Veil Control": 0,
}
DISCIPLINES_L1 = {
    "Pillar Lore (Life)": 2, "regional/era History": 2,
    "Medicine": 2, "Throwing": 2,
}
DISCIPLINE_L2 = ("Navigation", 1)
FAMILIES = {"Scholarly": 4, "Professional and Technical": 2,
            "Physical and Fieldcraft": 2}
WEAPON_TRAINING = {"Small Blades": 2}
EQUIPMENT_SP = {
    "Leather armor": 25, "Dagger": 4,
    "Standard adventuring pack": 8, "Basic medical kit": 15,
}
BOND = {"pillar": "Life", "aspect": "Restoration"}
MISSION = "Make recovery possible where injury or illness has taken that possibility away."
IMPRINT = "The Returning Step"
SURGE = "The Returning Steps"
TALENT = "TAL-A01 Imprint Recall"
AUTHORED_RESTORATION = ("Basic Heal", "Guided Regeneration")
# The selected pilot is Life / Restoration only. Fire / Conflagration is an
# ALTERNATIVE, separately bonded pilot, never a second known catalogue.


def profile(level):
    """One character, no free extra technique, Talent or second Aspect."""
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only source-defined levels 1–3")
    a = deepcopy(ABILITIES)
    learned = dict(DISCIPLINES_L1)
    if level >= 2:
        learned[DISCIPLINE_L2[0]] = DISCIPLINE_L2[1]
    hp = 10 + a["Vitality"]
    ap = 30 + 6 * (level - 1)
    vp = max(1, 6 + a["Veil Affinity"]) * level
    return {
        "identity": "High Anointed Returning Step Restoration Practitioner — pilot",
        "archetype": "Anointed", "focus": "High", "level": level,
        "abilities": a, "ability_points": sum(COST[v] for v in a.values()),
        "resonance": 0, "priest_pillar_accord": None,
        "bond": dict(BOND), "mission": MISSION, "birth_imprint": IMPRINT,
        "origin_surge": SURGE, "mission_state": "Aligned", "bond_active": True,
        "aspect_intuition": "Restoration: injury, disease and failed healing patterns; no automatic reveal",
        "birth_imprint_is_additional_technique": False,
        "learned_disciplines": learned, "learned_points": sum(learned.values()),
        "learned_families_l1": dict(FAMILIES),
        "weapon_training": dict(WEAPON_TRAINING),
        "weapon_development_points": 2,
        "background_familiarities": [
            "Communal rehabilitation traditions", "Travelling medical practitioners",
        ],
        "talents": [TALENT], "talent_selections_acquired": 1,
        "talent_recall_interval_hours": 6,
        "talent_recall_scope": "Failed legitimate bonded-Pillar Lore or context-related History check only",
        "known_bonded_techniques": list(AUTHORED_RESTORATION),
        "ordinary_technique_access": "Full authored bonded Aspect catalogue, subject to actual profile and tier limits",
        "known_other_aspect_techniques": [],
        "prepared_prayers": None, "scholar_formulae": None,
        "emotion_aspect_links": None,
        "universal": ["Veil Inspection"] + (["Blink"] if level >= 3 else []),
        "max_used_tier": 1 if level < 3 else 2,
        "basic_heal_t1_spent_vp": 2, "basic_heal_t2_spent_vp": 4 if level >= 3 else None,
        "guided_regeneration_t1_fixed_spent_vp": 2,
        "guided_regeneration_t1_maintained_committed_vp": 2,
        "ordinary_guided_grants_regeneration_step": False,
        "equipment_sp": dict(EQUIPMENT_SP),
        "starting_budget_sp": 150, "starting_spent_sp": sum(EQUIPMENT_SP.values()),
        "silver_remaining_sp": 150 - sum(EQUIPMENT_SP.values()),
        "armor": 3, "wielded_weapon": "Dagger",
        "dagger_attack_bonus": a["Agility"] + a["Precision"] + 2,
        "dagger_guard_defense": 10 + a["Agility"] + a["Precision"] + 2,
        "dagger_damage": "2+d4 Cut/Pierce (Light Strength contribution +0)",
        "hp_max": hp, "vigor_max": hp * level, "vp_max": vp,
        "turn_ap": ap, "physical_action_ap": 30,
        "projection_action_ap": 20, "general_action_ap": 24,
        "physical_tempo": ap // 30, "projection_tempo": ap // 20,
        "guard_capacity": ap // 30, "opportunity_capacity": ap // 30,
        "initiative": a["Agility"] + a["Awareness"],
        "first_dodge": 10 + min(a["Agility"], 4) + a["Awareness"],
        "movement_points": 12,
        "normal_regen_throughput": max(0, a["Vitality"]) + 1,
        "medicine_check_bonus": a["Intellect"] + learned["Medicine"],
        "pillar_lore_check_bonus": a["Intellect"] + learned["Pillar Lore (Life)"],
        "signature": "Returning Step", "signature_vp": 0,
        "signature_projection_ap": 20, "signature_hp_cap": 2,
        "signature_range_squares": 4 if level >= 2 else 3,
        "signature_vigor_per_hp": 1,
        "lesser_authority": "Spare the Reserve", "lesser_destiny_cost": 1,
        "max_destiny": 2, "destiny_initial_at_creation_only": 2,
        "destiny_on_level_up": "carry existing account; no automatic refill",
        "destiny_recovery_per_completed_six_hours": 1,
        "l3_guided_primary_lesser_eligible": level >= 3,
        "l3_basic_heal_lesser_eligible": False,
        "two_signature_actions_fit": ap >= 40,
        "signature_plus_basic_heal_fit": ap >= 40,
        "signature_plus_general_fit": ap >= 44,
        "blink_affordable_at_full_vp": level >= 3 and vp >= 10,
        "structural_character_build_complete": True,
        "independent_full_focus_certified": False,
        "native_combat_or_noncombat_certified": False,
    }


def isolated_witness(level):
    """Resources/eligibility only: simulated source flags are NOT native receipts."""
    s = profile(level)
    actor = Anointed(level=level, focus="High", aspect="Restoration")
    baseline = returning_step(
        actor, receipt=f"L{level}-baseline", target_id="patient",
        recipient_hp=5, recipient_max_hp=12, recipient_vigor=6,
        ap_available=s["turn_ap"], distance=3,
    )
    lesser = returning_step(
        baseline.actor, receipt=f"L{level}-lesser", target_id="patient",
        recipient_hp=7, recipient_max_hp=12, recipient_vigor=0,
        lesser=True, ap_available=s["turn_ap"], distance=s["signature_range_squares"],
    )
    # GM recognition is an independent, once-only story beat.
    rewarded = mission_event(lesser.actor, f"village-recovery-L{level}", gm_recognized=True)
    repeat = mission_event(rewarded, f"village-recovery-L{level}", gm_recognized=True)
    rec = recover_destiny(replace_destiny(rewarded, 0), 360)
    guided = None
    if level == 3:
        # All flags are asserted by this isolated fixture, NOT authenticated.
        out = guided_regeneration_l3(
            actor, receipt="L3-guided-step-1", recipient_missing_hp_after_ordinary=2,
            active_paid_guided_instance=True, mode="Maintained",
            profile="Single Target", authenticated_regeneration_step=True,
            guided_bonus_unsuppressed=True,
        )
        guided = {"extra_hp_without_vigor": out.additional_hp_without_vigor,
                  "destiny_left": out.actor.destiny, "native_step_authenticated": False}
    return {
        "level": level,
        "normal_hp": baseline.hp_restored, "normal_recipient_vigor": baseline.recipient_vigor_spent,
        "normal_ap": baseline.ap_spent,
        "lesser_hp": lesser.hp_restored, "lesser_recipient_vigor": lesser.recipient_vigor_spent,
        "lesser_destiny_left": lesser.actor.destiny,
        "mission_destiny_after_award": rewarded.destiny,
        "mission_repeat_awarded": repeat.destiny != rewarded.destiny,
        "six_hour_recovery_from_zero": rec.destiny,
        "guided_l3": guided,
        "native_event_receipts": False, "full_focus_certified": False,
    }


def replace_destiny(actor, value):
    from dataclasses import replace
    return replace(actor, destiny=value)


def verify():
    if (len(ABILITIES) != 9 or any(type(x) is not int or x not in COST for x in ABILITIES.values())
            or sum(COST[x] for x in ABILITIES.values()) != 28):
        raise AssertionError("Nine-Ability point-buy drift")
    if (sum(DISCIPLINES_L1.values()) != 8 or max(DISCIPLINES_L1.values()) > 2
            or sum(FAMILIES.values()) != 8 or sum(WEAPON_TRAINING.values()) != 2
            or sum(EQUIPMENT_SP.values()) != 52):
        raise AssertionError("Training/equipment drift")
    for level in LEVELS:
        s = profile(level)
        w = isolated_witness(level)
        if (s["ability_points"] != 28 or s["learned_points"] != 8 + int(level >= 2)
                or s["weapon_development_points"] != 2 or s["starting_spent_sp"] != 52
                or s["silver_remaining_sp"] != 98 or len(s["talents"]) != 1
                or len(s["known_bonded_techniques"]) != 2
                or s["known_other_aspect_techniques"] or s["known_bonded_techniques"] != list(AUTHORED_RESTORATION)
                or s["turn_ap"] != 30 + 6*(level-1)
                or s["vp_max"] != 6*level or s["vigor_max"] != 12*level
                or s["physical_tempo"] != 1 or s["projection_tempo"] != (2 if level == 3 else 1)
                or s["guard_capacity"] != 1
                or s["universal"] != (["Veil Inspection"] + (["Blink"] if level >= 3 else []))
                or s["max_used_tier"] != (2 if level >= 3 else 1)
                or s["signature_range_squares"] != (4 if level >= 2 else 3)
                or s["two_signature_actions_fit"] != (level == 3)
                or s["signature_plus_general_fit"]
                or s["independent_full_focus_certified"]):
            raise AssertionError("High Anointed level ledger drift")
        if ((w["normal_hp"], w["normal_recipient_vigor"], w["normal_ap"]) != (2, 2, 20)
                or (w["lesser_hp"], w["lesser_recipient_vigor"], w["lesser_destiny_left"]) != (2, 0, 1)
                or w["mission_destiny_after_award"] != 2 or w["mission_repeat_awarded"]
                or w["six_hour_recovery_from_zero"] != 1
                or (w["guided_l3"] is None) != (level < 3)):
            raise AssertionError("Canonical isolated Signature/Authority witness drift")
    return True


if __name__ == "__main__":
    verify()
    print(json.dumps({"build": "High Anointed Restoration structural L1–3",
                      "levels": [profile(n) for n in LEVELS],
                      "isolated_witnesses": [isolated_witness(n) for n in LEVELS]},
                     indent=2, ensure_ascii=False, sort_keys=True, allow_nan=False))
