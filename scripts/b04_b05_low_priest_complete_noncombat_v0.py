"""B04/B05 source-verified Low Priest A/B noncombat choices at L1-3.

Native G0 source A/B remains a physical proxy, but the selected full sheet
supplies REAL paid Learned Discipline, preparation, hand and VP constraints.
Fixed illustrative GM premises, no observed players or full Focus certificate.
"""
import argparse
from copy import deepcopy
import json

from scripts.b04_b05_noncombat_scene_resolution_v0 import (
    _character, resolve_scene,
)
from scripts.b05_low_priest_life_l1_l3_v0 import profile
from scripts.b06_damage_v0 import DamageState
from scripts.b06_encounter_state_v0 import Encounter, RegenerationChoice, UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

ROLES = ("A", "B")
LEVELS = (1, 2, 3)
STATUS = "BOUNDED_NATIVE_SOURCE_PAID_NOT_EXTERNAL_GM_PLAY"


def _actual_source(role, level):
    if role not in ROLES or type(level) is not int or level not in LEVELS:
        raise ValueError("Only original Low Priest A/B at L1-3")
    actor, abilities, learned, scope = _character(
        "Priest/Low", level, low_variant=role)
    sheet = profile(role, level)
    if (sheet["abilities"] != abilities
            or sheet["learned_disciplines"] != learned
            or sheet["chosen_devotion"] not in sheet["prepared_prayers"]
            or scope != "LOW_PRIEST_FULL_SELECTED_SHEET_NATIVE_G0_PHYSICAL_ONLY"):
        raise UnresolvedDecision("Audited full source sheet does not match G0")
    return actor, sheet


def native_utility(role, level, technique, *, animal_mass_kg=12,
                   animal_visible=True, animal_wary=True):
    """G0 paid Inspection for A/B or prepared L2+ A Woodland Rapport.

    Only independently preauthored observations. Rapport does not decide an
    animal's actual behavior, permit a reaction or cause automatic compliance.
    """
    actor, sheet = _actual_source(role, level)
    if technique not in ("inspection", "rapport"):
        raise UnresolvedDecision("No unlisted Low Life noncombat technique")
    if technique == "rapport":
        if (role != "A" or level < 2
                or "Woodland Rapport" not in sheet["prepared_prayers"]):
            raise UnresolvedDecision("This Low Priest did not prepare Rapport")
        if (type(animal_mass_kg) not in (int, float) or
                type(animal_mass_kg) is bool or
                not 0 < animal_mass_kg <= 25
                or type(animal_visible) is not bool or not animal_visible
                or type(animal_wary) is not bool or not animal_wary):
            raise ValueError("Requires a visible nonhostile animal up to 25 kg")
    else:
        if "Veil Inspection" not in sheet["universals"]:
            raise UnresolvedDecision("Universal procedure was not earned")
    e = Encounter([actor], {"pilot": 40}, seed=0,
                  scenario="B04-B05-Low-Priest-Full-Sheet-Noncombat-v0",
                  policy=f"{role}:L{level}:{technique}",
                  objective="one real G0 cost, no GM verdict")
    DamageState(e)
    e.begin_round()
    e.start_turn("pilot", regen_choice=RegenerationChoice())
    ap_before, vp_before = actor.ap_remaining, actor.vp_available
    e.spend_ap("pilot", "full" if technique == "inspection" else "projection",
               label="b04_b05_low_priest_" + technique)
    e.spend_vp("pilot", 2, mode="spent",
               label="b04_b05_low_priest_" + technique)
    observation = (
        {"observable_pillar": "Life", "observable_aspect": "Restoration",
         "hidden_effect_exposed": False, "actual_item_held_by_fixture": True}
        if technique == "inspection" else
        {"animal_mass_kg": animal_mass_kg, "peaceful_cues": True,
         "first_contact_bonus": 2, "animal_response": "UNRESOLVED_GM",
         "forced_compliance": False})
    e.log("b04_b05_low_priest_utility_authored", role=role, level=level,
          technique="Veil Inspection" if technique == "inspection"
          else "Woodland Rapport", observation=observation,
          full_sheet_source=sheet["chosen_devotion"],
          source_sha256=actor.source.digest, player_gm_observed=False)
    e.end_turn()
    e.check()
    spent = vp_before - actor.vp_available
    if (spent != 2 or actor.vp_spent != 2
            or ap_before-actor.ap_remaining !=
                (sheet["turn_ap"] if technique == "inspection" else 30)):
        raise AssertionError("Source G0 AP/VP utility cost missing")
    return {
        "role": role, "level": level, "technique": technique,
        "source_path": actor.source.path, "source_sha256": actor.source.digest,
        "full_source_prepared": tuple(sheet["prepared_prayers"]),
        "ap_before": ap_before, "ap_paid": ap_before-actor.ap_remaining,
        "vp_before": vp_before, "vp_spent": spent,
        "vp_after": actor.vp_available,
        "observation": observation, "ledger": deepcopy(e.ledger),
        "ledger_sha256": canonical_digest(e.ledger),
        "human_gm_sessions": 0, "focus_certified": False,
    }


def verify_level(role, level):
    actor, sheet = _actual_source(role, level)
    forks = {
        "field_balance": resolve_scene("Priest/Low", level, "exploration",
                                      "balance", low_variant=role),
        "medical_diagnosis": resolve_scene("Priest/Low", level, "investigation",
                                          "diagnose", low_variant=role),
        "social_petition": resolve_scene("Priest/Low", level, "social",
                                        "petition", low_variant=role),
    }
    if (forks["medical_diagnosis"]["trained_rank"] != 2
            or forks["social_petition"]["trained_rank"] != 0
            or forks["field_balance"]["trained_rank"] != (2 if role == "A" else 0)):
        raise AssertionError("Exact original A/B purchased Training missing")
    utilities = {"inspection": native_utility(role, level, "inspection")}
    if role == "A" and level >= 2:
        utilities["rapport"] = native_utility(role, level, "rapport")
    if (sheet["basic_heal_hand_available_in_authored_loadout"] != (role == "A")
            or sheet["chosen_devotion"] != ("Guided Regeneration" if role == "A"
                                          else "Vital Shelter")):
        raise AssertionError("Actual equipped hand/Chosen source mismatch")
    return {
        "variant": role, "level": level,
        "source_identity": actor.source.source_id,
        "source_digest": actor.source.digest,
        "selected_full_sheet": True,
        "learned_disciplines": deepcopy(sheet["learned_disciplines"]),
        "prepared_prayers": deepcopy(sheet["prepared_prayers"]),
        "chosen_devotion": sheet["chosen_devotion"],
        "talents": deepcopy(sheet["talents"]),
        "silver_remaining": sheet["silver_remaining"],
        "free_hands_in_start_loadout": sheet["free_hands"],
        "basic_heal_currently_usable_with_hands":
            sheet["basic_heal_hand_available_in_authored_loadout"],
        "natural_rite_count_cap": sheet["active_devotional_rite_cap"],
        "exaltation_property": sheet["exaltation_property"],
        "noncombat": forks,
        "native_paid_utility": {
            key: {k: v for k, v in value.items() if k != "ledger"}
            for key, value in utilities.items()},
        "status": STATUS,
        "authentic_human_choices": 0, "full_focus_certified": False,
    }


def matrix():
    rows = [verify_level(role, level) for role in ROLES for level in LEVELS]
    return {
        "version": "B04-B05-Low-Priest-Full-Noncombat-v0",
        "low_priest_variants": 2, "level_snapshots": 6,
        "core_check_scenarios": 18,
        "native_paid_utility_actions": sum(len(x["native_paid_utility"]) for x in rows),
        "rows": rows, "independent_full_focus_certificates": 0,
        "human_sessions": 0, "strict_mvp_exits_met": 0,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--role", choices=ROLES)
    p.add_argument("--level", type=int, choices=LEVELS)
    args = p.parse_args()
    if (args.role is None) != (args.level is None):
        p.error("Choose role and level together")
    report = verify_level(args.role, args.level) if args.role else matrix()
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
