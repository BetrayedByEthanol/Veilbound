"""B06 G7: source-attested Hunter calibration readiness and scenario matrix v0.

A *readiness* manifest, not a Monte Carlo combat simulator or a CR rating.
The 48 candidate cells distinguish a fully executable G6-C fixed-choice
window from source-tested-but-unintegrated G6-D protection and unsupported
starts/targets. Six original native witnesses are audited separately;
fixed dice/seeds MUST NEVER become win probabilities or Wilson samples.
"""
from collections import Counter
from hashlib import sha256
from itertools import product
import json
import math

from scripts.b06_hunter_mixed_party_g6c_v0 import run_i3_mixed
from scripts.b06_hunter_completion_g6d_v0 import run_i3_defeat

LEVELS = (2, 3)
PARTY_SIZES = (3, 4)
OPENINGS = ("warned_clear", "forest_ambush")
FRONTS = ("A_head_forward", "B_head_forward")
POLICIES = ("decline_all", "reactive_shield", "prepared_body")
SOURCES = {3: ("A", "B", "R"), 4: ("A", "B", "R", "F")}
ACTORS = {3: ("hunter", "vanguard", "guardian", "archer"),
          4: ("hunter", "vanguard", "guardian", "archer", "scholar")}
SOURCE_FILES = (
    "content/creatures/b06-hunter-of-the-woods.v0.json",
    "scripts/b06_encounter_state_v0.py",
    "scripts/b06_hunter_mixed_party_g6c_v0.py",
    "scripts/b06_hunter_completion_g6d_v0.py",
    "scripts/b06_hunter_reactive_intervene_g6d_v0.py",
)
BASE_GATES = (
    "vary_source_legal_dice_and_tactics_with_independent_declared_policy",
    "attest_all_terminal_and_unresolved_outcomes_in_full_encounter",
    "record_party_losses_retreat_healing_and_postcombat_toxin_recovery",
    "define_paired_seed_cohort_and_comparable_starting_resources",
)


def scenario_matrix():
    """Complete, ordered 48-cell G7 *plan*; never guessed difficulty."""
    result=[]
    for level,size,opening,front,policy in product(
            LEVELS,PARTY_SIZES,OPENINGS,FRONTS,POLICIES):
        gaps=[]
        if opening=="forest_ambush":
            gaps.append("native_ambush_1x2_pounce_contact_and_response_policy")
        if front=="B_head_forward":
            gaps.append("alternate_frontline_source_defense_and_1x2_geometry")
        if policy=="reactive_shield":
            gaps.append("integrate_native_G6D_reactive_shield_into_party_run")
        if policy=="prepared_body":
            gaps.append("integrate_native_G6D_prepared_MP_route_into_party_run")
        witnessed=not gaps
        component=(opening=="warned_clear" and front=="A_head_forward"
                   and policy!="decline_all")
        status=("fixed_native_window" if witnessed else
                "component_verified_only" if component else
                "blocked_not_executable")
        result.append({
            "scenario_id":(
                f"G7-L{level}-P{size}-{opening}-{front}-{policy}"),
            "level":level,"party_size":size,
            "roster_source_ids":list(SOURCES[size]),
            "enemy_source_id":"B06-EN-03",
            "enemy_count":1,
            "opening":opening,"frontline":front,"policy":policy,
            "status":status,
            "native_fixed_window_executable":witnessed,
            "complete_encounter_certified":False,
            "component_only":component,
            "known_missing_authority":gaps,
            "frozen_historical_phase3_not_a_comparator":True,
            "calibration_samples":0,
            "terminal_count":None,
            "success_rate":None,
            "ci95":None,
            "creature_cr":None,
        })
    return result


def wilson_95(successes, trials):
    """Confidence-interval helper for *future* independent completed trials.

    Never called on fixed-face witnesses, truncated runs or unresolved
    denominators. Integer-only validation deliberately rejects bools.
    """
    if (type(successes) is not int or type(trials) is not int
            or trials<1 or not 0<=successes<=trials):
        raise ValueError("Wilson needs 0 <= integer successes <= positive trials")
    z=1.959963984540054
    p=successes/trials
    z2=z*z
    den=1+z2/trials
    center=(p+z2/(2*trials))/den
    spread=(z/den)*math.sqrt(
        (p*(1-p)+z2/(4*trials))/trials)
    return (round(max(0.0,center-spread),6),
            round(min(1.0,center+spread),6))


def _ledger_measures(ledger):
    """Observe authenticated event *counts*, not inferred result labels."""
    if not isinstance(ledger,list):
        raise AssertionError("Native witness ledger required")
    for i,ev in enumerate(ledger):
        if (ev.get("index")!=i or
                type(ev.get("round")) is not int or
                type(ev.get("kind")) is not str or
                not isinstance(ev.get("detail"),dict)):
            raise AssertionError("Invalid native G0 event sequence")
    counts=Counter(ev["kind"] for ev in ledger)
    return {
        "turn_ends":counts["turn_end"],
        "round_ends":counts["round_end"],
        "g5_melee_resolved":counts["g5_melee_resolved"],
        "g2_arrows_launched":counts["g2_bow_launched"],
        "g2_projectile_results":counts["g2_bow_shot_resolved"],
        "g4_damage_events":counts["g4_damage_applied"],
        "g4_wounds_created":counts["g4_wound_created"],
        "g3_flame_launches":counts["g3_flame_launched"],
        "g6d_attested_bow":counts["g6d_bow_adjudicated"],
        "g6d_defeat_terminals":counts["g6d_hunter_defeat_attested"],
        "reactive_protections":sum(
            ev["detail"].get("activation")=="reactive"
            for ev in ledger if ev["kind"]=="g6d_protective_bite_attested"),
        "prepared_protections":sum(
            ev["detail"].get("activation")=="prepared"
            for ev in ledger if ev["kind"]=="g6d_protective_bite_attested"),
    }


def _verify_turns(ledger,actors,rounds):
    turn_ends=[ev["detail"]["actor"] for ev in ledger
               if ev["kind"]=="turn_end"]
    if (turn_ends!=list(actors)*rounds or
            len([ev for ev in ledger if ev["kind"]=="round_end"])!=rounds):
        raise AssertionError("Native G0 turn order or Round End incomplete")


def replay_native_witnesses():
    """Six source-backed, fixed-dice witnesses; explicitly not trial samples."""
    witnesses=[]
    for level,size in product(LEVELS,PARTY_SIZES):
        seed=7100+100*level+size
        report=run_i3_mixed(size=size,level=level,seed=seed)
        roster=report["roster"]
        if ([(a["id"],a["source"]) for a in roster]
                !=list(zip(ACTORS[size],("B06-EN-03",*SOURCES[size])))
                or any(not a["source_digest"] for a in roster)):
            raise AssertionError("G6-C native source roster/digest mismatch")
        if (report["rounds"]!=2 or report["round_ends"]!=2
                or report["window_status"]!="two_real_rounds_observed"
                or report["ending"]!="not_attested_full_encounter"
                or report["complete_party_pack_certified"] is not False
                or report["hunter_cr"] is not None):
            raise AssertionError("G6-C fixed window falsely certified")
        _verify_turns(report["ledger"],ACTORS[size],2)
        measure=_ledger_measures(report["ledger"])
        if (measure["g2_arrows_launched"]!=2 or
                measure["g6d_defeat_terminals"]!=0 or
                measure["g6d_attested_bow"]!=0):
            raise AssertionError("G6-C fixed window evidence unexpectedly changed")
        witnesses.append({
            "witness_id":f"G6C-L{level}-P{size}-fixed",
            "scenario_id":f"G7-L{level}-P{size}-warned_clear-A_head_forward-decline_all",
            "executor":"scripts.b06_hunter_mixed_party_g6c_v0.run_i3_mixed",
            "kind":"two_round_fixed_choice_window",
            "level":level,"party_size":size,"seed":seed,
            "seed_is_random_trial":False,
            "roster":roster,
            "rounds":2,
            "hunter_hp_at_stop":report["hunter_hp"],
            "hunter_dying_at_stop":report["hunter_dying"],
            "hunter_dead_at_stop":report["hunter_dead"],
            "ending":"not_attested_full_encounter",
            "measures":measure,
        })
    for level in LEVELS:
        seed=8100+100*level
        report=run_i3_defeat(level=level,seed=seed)
        terminal=report["terminal"]
        if (report["rounds"]!=3 or not report["hunter_dead"]
                or terminal["ending"]!="hunter_defeat_attested"
                or report["complete_party_pack_certified"] is not False
                or report["hunter_cr"] is not None):
            raise AssertionError("G6-D witnessed defeat or boundary changed")
        _verify_turns(report["ledger"],ACTORS[4],3)
        measure=_ledger_measures(report["ledger"])
        if (measure["g6d_defeat_terminals"]!=1
                or measure["g6d_attested_bow"]!=1):
            raise AssertionError("One genuinely attested G6-D Bow defeat required")
        original=next(x for x in witnesses
                      if x["level"]==level and x["party_size"]==4)
        witnesses.append({
            "witness_id":f"G6D-L{level}-P4-scripted-defeat",
            "scenario_id":original["scenario_id"],
            "executor":"scripts.b06_hunter_completion_g6d_v0.run_i3_defeat",
            "kind":"three_round_scripted_terminal_overlay",
            "level":level,"party_size":4,"seed":seed,
            "seed_is_random_trial":False,
            "roster":original["roster"],
            "rounds":3,
            "hunter_hp_at_stop":report["hunter_hp"],
            "hunter_dying_at_stop":False,
            "hunter_dead_at_stop":True,
            "ending":"hunter_defeat_attested",
            "measures":measure,
        })
    return witnesses


def build_readiness_report(*,replay=True):
    """Reproducible readiness report; never derives a sampled success rate."""
    if type(replay) is not bool:
        raise ValueError("Replay flag must be explicit boolean")
    matrix=scenario_matrix()
    witnesses=replay_native_witnesses() if replay else []
    census=Counter(x["status"] for x in matrix)
    summary={
        "planned_cells":len(matrix),
        "native_fixed_window_cells":census["fixed_native_window"],
        "component_only_cells":census["component_verified_only"],
        "blocked_cells":census["blocked_not_executable"],
        "replayed_native_witnesses":len(witnesses),
        "calibration_samples":0,
        "certified_party_pack_count":0,
        "hunter_challenge_rating":None,
    }
    if (summary["planned_cells"]!=48 or
            (summary["native_fixed_window_cells"],
             summary["component_only_cells"],summary["blocked_cells"])
            !=(4,8,36)):
        raise AssertionError("G7 scenario coverage unexpectedly changed")
    return {
        "version":"B06-G7-calibration-readiness-v0",
        "evidence_grade":"planning_with_fixed_native_witnesses",
        "historical_phase3_seeds":128,
        "historical_phase3_cells":32,
        "historical_phase3_windows":4096,
        "historical_phase3_audit_sha256":
            "c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b",
        "historical_phase3_recomputed":False,
        "historical_phase3_is_not_current_native_cohort":True,
        "native_source_paths":list(SOURCE_FILES),
        "summary":summary,
        "matrix":matrix,
        "native_witnesses":witnesses,
        "next_gate_before_distributional_sampling":list(BASE_GATES),
        "future_inference_policy":{
            "source_build_parity_required":True,
            "paired_seeds_without_rerolling_selected_failures":True,
            "report_unresolved_as_own_denominator_category":True,
            "do_not_condition_win_rate_on_resolved_subset":True,
            "candidate_pilot_seeds_per_cell":128,
            "confidence_interval":"Wilson95 only for future completed unbiased binary trials",
            "current_win_probability":None,
            "current_cr":None,
        },
    }


def canonical_digest(report):
    """Content fingerprint; not the frozen Phase 3 report's audit hash."""
    return sha256(json.dumps(report,sort_keys=True,
                             separators=(",",":"),ensure_ascii=True,
                             allow_nan=False).encode("utf-8")).hexdigest()


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-only",action="store_true",
                        help="List all gates without rerunning six fixed witnesses")
    args=parser.parse_args(argv)
    report=build_readiness_report(replay=not args.manifest_only)
    result={"readiness_sha256":canonical_digest(report),**report}
    print(json.dumps(result,sort_keys=True,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
