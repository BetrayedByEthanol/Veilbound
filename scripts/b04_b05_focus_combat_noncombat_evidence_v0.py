"""B04/B05 L1-3 Focus-specific bounded native combat and noncombat access v0.

Replay genuine existing authored G0-G5 combat policies for every pairing/level,
and native G4.2 Anointed exploration. For the other nine Focuses, noncombat
evidence is ONLY independent source Training access with unresolved GM checks.
No actor/GM observations, Focus certificate, representative win rate or MVP
exit is fabricated. Pairing/level records are distinct from source variants.
"""
from copy import deepcopy
from hashlib import sha256
from importlib import import_module
import argparse
import json

from scripts.b04_b07_twelve_focus_certification_protocol_v0 import roster
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

LEVELS = (1, 2, 3)
RUNS = {
    "Priest/High": ("scripts.b05_high_life_native_encounter_v0",
                    "run_policy", "prepared_guided", "baseline"),
    "Priest/Medium": ("scripts.b05_priest_life_role_decision_gate_v0",
                      "run_policy", "triage", "baseline"),
    "Priest/Low": ("scripts.b05_low_life_native_encounter_v0",
                   "run_policy", "A", "B"),
    "Scholar/High": ("scripts.b05_scholar_three_focus_native_offense_v0",
                     "run_case", "flame_t1", "no_spell"),
    "Scholar/Medium": ("scripts.b05_medium_scholar_native_encounter_v0",
                       "run_policy", "stone", "baseline"),
    "Scholar/Low": ("scripts.b05_low_scholar_native_encounter_v0",
                    "run_policy", "stone", "baseline"),
    "Gifted/High": ("scripts.b05_high_gifted_native_encounter_v0",
                    "GiftedNative.cast_flame", "flame", "no_surge"),
    "Gifted/Medium": ("scripts.b05_medium_gifted_tactical_balance_v0",
                      "run_case", "fear", "dormant"),
    "Gifted/Low": ("scripts.b05_low_gifted_native_anchor_v0",
                   "LowGiftedNativeAnchor", "chosen_guard", "ordinary_guard"),
    "Anointed/High": ("scripts.b05_anointed_native_g5_weapon_signature_choice_v0",
                      "run_policy", "weapon_signature", "weapon_only"),
    "Anointed/Medium": ("scripts.b05_anointed_native_g5_weapon_signature_choice_v0",
                        "run_policy", "weapon_signature", "weapon_only"),
    "Anointed/Low": ("scripts.b05_anointed_native_g5_weapon_signature_choice_v0",
                     "run_policy", "weapon_signature", "weapon_only"),
}
STATUS_COMBAT = "BOUNDED_NATIVE_POLICY_REPLAY_NOT_HUMAN_PLAY"
STATUS_NONCOMBAT = "SOURCE_TRAINING_ACCESS_ONLY_GM_UNRESOLVED"
STATUS_ANOINTED = "BOUNDED_NATIVE_G42_CLOCK_NOT_EXTERNAL_GM_VERDICT"


def _native_high_gifted(level, *, amplify):
    from scripts.b05_high_gifted_native_encounter_v0 import gifted_actor, GiftedNative
    from scripts.b06_encounter_state_v0 import Encounter, enemy_actor
    from scripts.b06_movement_v0 import GridMovement
    from scripts.b06_ranged_v0 import RangedCombat
    from scripts.b06_spells_v0 import SpellState
    from scripts.b06_damage_v0 import DamageState
    g = gifted_actor(level, "gifted", "party", occupied=((2, 2),))
    foe = enemy_actor("B06-EN-02", "soldier", "enemy", occupied=((4, 2),))
    e = Encounter([g, foe], {"gifted": 40, "soldier": 30}, seed=7,
                  scenario="B04-B05-High-Gifted-Bounded-Role-Choice-v0",
                  policy="source_flame_surge_vs_ordinary",
                  objective="one_authored_cast_not_full_role_certification")
    GridMovement(e, width=10, height=6, scene_id="gifted-evidence-grid")
    RangedCombat(e, scene_id="gifted-evidence-projectile")
    SpellState(e)
    DamageState(e)
    witness = GiftedNative(e, "gifted")
    e.begin_round()
    e.start_turn("gifted")
    witness.establish("Joy")
    result = witness.cast_flame("soldier", tier=1, face=14, vigor_die=5,
                                hand_available=True,
                                **({"surge": "Precision"} if amplify else {}))
    if result["outcome"] != "direct_hit_resolved_G4":
        raise AssertionError("High Gifted intended fixed live hit did not resolve")
    e.check()
    return {"ledger": deepcopy(e.ledger), "ledger_sha256": canonical_digest(e.ledger),
            "metrics": {"cast_outcome": result["outcome"],
                        "attack_total": result["attack_total"],
                        "vp_spent": result["vp_spent"]}}


def _native_low_gifted(level, *, boosted):
    from scripts.b05_low_gifted_native_anchor_v0 import LowGiftedNativeAnchor
    from scripts.b06_encounter_state_v0 import (
        Encounter, RegenerationChoice, party_actor, enemy_actor,
    )
    from scripts.b06_movement_v0 import GridMovement
    from scripts.b06_ranged_v0 import RangedCombat
    from scripts.b06_spells_v0 import SpellState
    from scripts.b06_damage_v0 import DamageState
    from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
    actor = party_actor("GL", level, "gifted", "party", occupied=((2, 2),))
    foe = enemy_actor("B06-EN-02", "foe", "enemy", occupied=((3, 2),))
    e = Encounter([actor, foe], {"foe": 40, "gifted": 30}, seed=17,
                  scenario="B04-B05-Low-Gifted-Bounded-Role-Choice-v0",
                  policy="paid_guard_pulse_vs_ordinary",
                  objective="one_native_response_not_full_certification")
    GridMovement(e, width=8, height=8, scene_id="low-gifted-evidence-grid")
    RangedCombat(e, scene_id="low-gifted-evidence-wielded")
    SpellState(e)
    DamageState(e)
    anchor = LowGiftedNativeAnchor(e, "gifted", anchor="Fear")
    combat = SourceMelee(e)
    e.begin_round()
    combat.bridge.start_next_turn(RegenerationChoice())
    if boosted:
        anchor.choose_defense("foe:gifted:0", "guard")
    attack = combat.declare("foe", "gifted", profiles=("B06-AT-03",),
                            defenses=("guard",))
    outcome = combat.resolve(attack, 0, attack_face=12,
                             **({} if boosted else
                                {"damage_face": 2, "wound_location_roll": 8}))
    assigned = next(x for x in e.ledger if x["kind"] == "defense_assigned")
    if (boosted and (outcome["outcome"], assigned["detail"]["defense_value"]) !=
            ("miss", 18)):
        raise AssertionError("Native Rooted Guard did not provide paid +1")
    if not boosted and (outcome["outcome"], assigned["detail"]["defense_value"]) != ("hit", 17):
        raise AssertionError("Normal Guard comparison did not resolve original hit")
    e.check()
    return {"ledger": deepcopy(e.ledger), "ledger_sha256": canonical_digest(e.ledger),
            "metrics": {"combat_outcome": outcome["outcome"],
                        "defense_value": assigned["detail"]["defense_value"],
                        "anchor_bonus": assigned["detail"].get("anchor_bonus", 0)}}


def _combat(pairing, level, policy):
    module, method, primary, alternative = RUNS[pairing]
    if policy not in (primary, alternative):
        raise ValueError("Only fixed source-vetted combat policy choices")
    if pairing == "Gifted/High":
        result = _native_high_gifted(level, amplify=policy == primary)
    elif pairing == "Gifted/Low":
        result = _native_low_gifted(level, boosted=policy == primary)
    else:
        run = getattr(import_module(module), method)
        if pairing == "Priest/High":
            result = run(level=level, opponent="soldier", policy=policy)
        elif pairing == "Priest/Medium":
            result = run(role="M", level=level, opponent="soldier",
                         variant="prepared_light", policy=policy)
        elif pairing == "Priest/Low":
            result = run(role=policy, level=level, opponent="soldier")
        elif pairing.startswith("Scholar/") and pairing == "Scholar/High":
            result = run(focus="High", level=level, policy=policy)
        elif pairing.startswith("Scholar/"):
            result = run(level=level, policy=policy)
        elif pairing == "Gifted/Medium":
            result = run(level=level, opponent="soldier", policy=policy)
        else:
            result = run(focus=pairing.split("/")[1], level=level,
                         opponent="soldier", policy=policy)
    if not isinstance(result, dict) or not isinstance(result.get("ledger"), list):
        raise AssertionError("No actual native G0 ledger in bounded policy")
    if not result["ledger"] or result.get("ledger_sha256") != canonical_digest(result["ledger"]):
        raise AssertionError("Native combat result has invalid ledger checksum")
    kinds = [e["kind"] for e in result["ledger"]]
    if "action_committed" not in kinds:
        raise AssertionError("Combat policy did not commit a native G0 action")
    return {"policy": policy, "source_module": module,
            "ledger_sha256": result["ledger_sha256"],
            "event_count": len(kinds), "distinct_event_kinds": sorted(set(kinds)),
            "source_metrics": deepcopy(result.get("metrics", {})),
            "evidence_status": STATUS_COMBAT}


def _noncombat(pairing, level):
    """Independently verify actual learned training; do NOT roll a GM scene."""
    if pairing == "Priest/Low":
        return {"status": "LOW_PRIEST_A_B_PROXY_NO_COMPLETE_NONCOMBAT_SHEET",
                "chosen": None, "alternative": None,
                "gm_check_resolved": False, "human_choice_observed": False,
                "blocker": "Independently reviewed complete Low Priest skill/rite sheet"}
    source = next(row for row in roster() if row["pairing"] == pairing)
    if source["source_issues"]:
        raise AssertionError("Cannot derive noncombat choices from structurally failing source")
    path = next(p for p in source["source_fingerprints"] if p.startswith("scripts/"))
    profile = getattr(import_module("scripts." + path.split("/")[-1][:-3]), "profile")(level)
    skills = profile["learned_disciplines"]
    if not isinstance(skills, dict):
        raise AssertionError("No authored trained skills for source pairing")
    trained = sorted((n, v) for n, v in skills.items() if type(v) is int and v > 0)
    if len(trained) < 2:
        raise AssertionError("Source sheet lacks two actual trained candidate alternatives")
    chosen, alternative = trained[:2]
    result = {
        "status": STATUS_NONCOMBAT, "chosen": {"discipline": chosen[0], "rank": chosen[1]},
        "alternative": {"discipline": alternative[0], "rank": alternative[1]},
        "source_path": path, "source_sha256": source["source_fingerprints"][path],
        "untrained_forgery_rejected": "Unauthored Noncombat Skill" not in skills,
        "gm_check_resolved": False, "human_choice_observed": False,
        "limits": "Source training alternatives only; no real skill roll, declared DC, GM adjudication or level-specific lived choice",
    }
    if pairing.startswith("Anointed/"):
        mod = import_module("scripts.b05_anointed_native_noncombat_destiny_v0")
        clock = mod.run_policy(focus=pairing.split("/")[1], level=level,
                               opponent="soldier", policy="clock_partial", seed=0)
        if (not isinstance(clock.get("ledger"), list) or
                clock.get("ledger_sha256") != canonical_digest(clock["ledger"])):
            raise AssertionError("Anointed G4.2 native clock provenance mismatch")
        result["status"] = STATUS_ANOINTED
        result["native_clock_ledger_sha256"] = clock["ledger_sha256"]
        result["native_clock_event_count"] = len(clock["ledger"])
        result["limits"] = ("Real source G4.2 elapsed clock only; GM verdict was not supplied "
                            "or independently authenticated; no human agency claimed")
    return result


def evidence(pairing, level):
    if type(pairing) is not str or pairing not in RUNS:
        raise ValueError("Only original twelve Focus pairings")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only exact L1-3 level")
    module, method, primary, alternative = RUNS[pairing]
    selected = _combat(pairing, level, primary)
    comparison = _combat(pairing, level, alternative)
    if selected["ledger_sha256"] == comparison["ledger_sha256"]:
        raise AssertionError("Chosen and alternative native policies collapsed")
    return {
        "pairing": pairing, "level": level,
        "selected_combat": selected, "alternative_combat": comparison,
        "noncombat": _noncombat(pairing, level),
        "native_combat_witnesses": 2, "actual_human_choices": 0,
        "externally_verified_sessions": 0, "independent_focus_certified": False,
        "strict_mvp_exits_met": 0,
        "evidence_scope": "two deterministic source-paid native policies + source skill access (G4.2 for Anointed); not human-play role certification",
    }


def matrix():
    rows = [evidence(pairing, level) for pairing in sorted(RUNS) for level in LEVELS]
    return {
        "focus_pairings": 12, "pairing_level_slots": len(rows),
        "native_combat_witnesses": sum(x["native_combat_witnesses"] for x in rows),
        "externally_verified_sessions": 0,
        "independently_certified_focuses": 0, "strict_mvp_exits_met": 0,
        "noncombat_coverage": {
            "source_training_only": sum(x["noncombat"]["status"] == STATUS_NONCOMBAT for x in rows),
            "native_anointed_clock": sum(x["noncombat"]["status"] == STATUS_ANOINTED for x in rows),
            "low_priest_proxy_only": sum(x["noncombat"]["chosen"] is None for x in rows),
            "human_gm_utility_outcomes": 0,
        },
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairing", choices=sorted(RUNS))
    parser.add_argument("--level", type=int)
    args = parser.parse_args()
    if (args.pairing is None) != (args.level is None):
        parser.error("--pairing and --level must be combined")
    payload = (evidence(args.pairing, args.level) if args.pairing else matrix())
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
