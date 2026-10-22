"""B06 G7-F: stratified, source-audited *candidate* encounter-calibration pilot.

Replays G7-A/C/D/E real encounters with predeclared seed/policy cells.
These are selected bounded tactics, not representative GM/player samples:
unknown encounter endings stay in every denominator, and no win rate,
confidence interval or Hunter CR is inferred from them.
"""
from collections import Counter
from hashlib import sha256
import json

PHASE3_SHA = "c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b"
LEVELS = (2, 3)
SIZES = (3, 4)
BASE_POLICIES = (
    "warned_control", "warned_flame", "warned_archer_exit",
    "warned_party_exit", "b_front", "forest_ordinary", "forest_pounce",
)
PROTECTIVE_POLICIES = ("protected_control", "reactive_shield", "prepared_body")
COHORTS = tuple((level, size, policy) for level in LEVELS for size in SIZES
                for policy in BASE_POLICIES) + tuple(
                    (3, 4, policy) for policy in PROTECTIVE_POLICIES)
POLICIES = BASE_POLICIES + PROTECTIVE_POLICIES
NATIVE_OUTCOMES = frozenset((
    "hunter_defeat_attested", "party_defeat_attested",
    "party_withdrawal_attested", "party_defeat_observed",
    "archer_withdrawal_attested", "legal_window_cutoff",
    "unresolved_mechanical_branch",
))
CERTIFIED_TERMINALS = {
    "hunter_defeat_attested": "g6d_hunter_defeat_attested",
    "party_defeat_attested": "g7c_party_defeat_attested",
    "party_withdrawal_attested": "g7c_party_withdrawal_attested",
}
# Match only within the *same* source roster, level and start geometry.
# This compares observed policy effects, not general treatment effects.
PAIRS = (
    ("forest_ordinary", "forest_pounce", "paired_forest_opening_faces"),
    ("warned_control", "warned_archer_exit", "predeclared_archer_exit_choice"),
    ("protected_control", "reactive_shield", "paired_L3P4_protection"),
    ("protected_control", "prepared_body", "paired_L3P4_protection"),
)


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False)


def _digest(value):
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _validate_cell(level, size, seed, policy):
    if (type(level) is not int or type(size) is not int or
            type(seed) is not int or seed < 0 or type(policy) is not str or
            (level, size, policy) not in COHORTS):
        raise ValueError("G7-F requires one of the 31 preauthored L2/3 P3/4 policies")


def _native_case(level, size, seed, policy):
    """Dispatch before observing results; no re-roll or policy switching."""
    if policy in ("warned_control", "warned_flame", "warned_archer_exit"):
        from scripts.b06_g7a_native_terminal_census_v0 import run_trial
        mode = {"warned_control": "g7a", "warned_flame": "g7b_flame",
                "warned_archer_exit": "g7b_archer_exit"}[policy]
        return run_trial(level, size, seed, policy_mode=mode, max_rounds=3,
                         include_ledger=True)
    if policy == "warned_party_exit":
        from scripts.b06_g7c_party_terminals_v0 import run_trial
        return run_trial(level, size, seed, include_ledger=True)
    if policy in ("b_front", *PROTECTIVE_POLICIES):
        from scripts.b06_g7d_protection_frontlines_v0 import run_trial
        mode = "control" if policy == "protected_control" else policy
        return run_trial(level, size, seed, policy=mode, round_limit=2,
                         include_ledger=True)
    from scripts.b06_g7e_ambush_pounce_recovery_v0 import run_trial
    return run_trial(level, size, seed,
                     policy="pounce" if policy == "forest_pounce"
                     else "ordinary_approach", round_limit=2,
                     exploration_seconds=0, include_ledger=True)


def attest_native(report, *, level, size, seed, policy):
    """Validate a native execution rather than trusting its summary label.

    Attests G0 event ordering/rounds, source roster, hash and terminal
    event. Does not reimplement the G4/G5 legality checks performed by
    each native source executor.
    """
    _validate_cell(level, size, seed, policy)
    if (not isinstance(report, dict) or report.get("level") != level or
            report.get("party_size") != size or report.get("seed") != seed or
            report.get("outcome") not in NATIVE_OUTCOMES or
            report.get("hunter_cr") is not None or
            report.get("complete_party_pack_certified") is not False):
        raise AssertionError("Foreign, inflated or malformed source trial")
    ledger = report.get("ledger")
    if not isinstance(ledger, list) or not ledger:
        raise AssertionError("Full actual native G0 ledger required")
    for index, event in enumerate(ledger):
        if (not isinstance(event, dict) or event.get("index") != index or
                type(event.get("round")) is not int or
                not isinstance(event.get("kind"), str) or
                not isinstance(event.get("detail"), dict)):
            raise AssertionError("Malformed or resequenced native event ledger")
    # Use the repository's original canonical digest, not a new digest
    # format which could quietly validate a different event history.
    from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
    if canonical_digest(ledger) != report.get("ledger_sha256"):
        raise AssertionError("Native ledger diverges from original attested hash")
    names = ("hunter", "vanguard", "guardian", "archer") + (
        ("scholar",) if size == 4 else ())
    expected_sources = ("B06-EN-03", "A", "B", "R") + (
        ("F",) if size == 4 else ())
    initial = report.get("initial_state")
    final = report.get("final_state")
    if (not isinstance(initial, dict) or not isinstance(final, dict) or
            set(initial) != set(names) or set(final) != set(names) or
            any(initial[n].get("source_id") != src or
                final[n].get("source_id") != src or
                not initial[n].get("source_digest") or
                initial[n].get("source_digest") != final[n].get("source_digest")
                for n, src in zip(names, expected_sources))):
        raise AssertionError("Native roster or source fingerprints changed")
    turns = [e["detail"].get("actor") for e in ledger if e["kind"] == "turn_end"]
    round_ends = sum(e["kind"] == "round_end" for e in ledger)
    if (turns != list(names) * (len(turns) // len(names)) +
            list(names)[:len(turns) % len(names)] or
            round_ends != len(turns) // len(names) or
            report.get("turns_completed") != len(turns) or
            report.get("rounds_completed") != round_ends):
        raise AssertionError("Native G0 round/turn chronology is not genuine")
    outcome = report["outcome"]
    found = [e for e in ledger if e["kind"] in CERTIFIED_TERMINALS.values()]
    if outcome in CERTIFIED_TERMINALS:
        if (len(found) != 1 or found[0]["kind"] != CERTIFIED_TERMINALS[outcome] or
                not isinstance(report.get("native_terminal"), dict) or
                len(turns) != round_ends * len(names) or
                report.get("unresolved") is not None):
            raise AssertionError("Certified terminal lacks source and final Round End")
    elif found:
        raise AssertionError("A real native terminal is mislabeled or discarded")
    if (outcome == "unresolved_mechanical_branch") != (report.get("unresolved") is not None):
        raise AssertionError("Unresolved mechanics must be retained explicitly")
    if policy in ("forest_ordinary", "forest_pounce"):
        clock = report.get("clock_handoff")
        if clock is not None and (clock.get("not_a_combat_terminal") is not True or
                                   clock.get("elapsed_seconds") != 0):
            raise AssertionError("Forest observation clock is not a legal departure")
    return {
        "level": level, "party_size": size, "seed": seed,
        "policy": policy, "source_scenario_id": report["scenario_id"],
        "source_policy_id": report["policy_id"],
        "outcome": outcome, "certified_terminal": outcome in CERTIFIED_TERMINALS,
        "censored": outcome not in CERTIFIED_TERMINALS,
        "unresolved_reason": (report["unresolved"]["reason"]
                              if report.get("unresolved") else None),
        "ledger_sha256": report["ledger_sha256"],
        "rounds_completed": round_ends, "turns_completed": len(turns),
        "hunter_hp_change": final["hunter"]["hp"] - initial["hunter"]["hp"],
        "party_hp_change": sum(final[n]["hp"] - initial[n]["hp"]
                               for n in names[1:]),
        "hunter_genuinely_dead": bool(final["hunter"].get("dead")),
        "genuine_pounces": sum(e["kind"] == "g6_pounce_resolved" for e in ledger),
        "genuine_protections": sum(e["kind"] == "g6d_protective_bite_attested"
                                   for e in ledger),
        "real_party_exit_events": sum(e["kind"] == "g5_terminal_exit" for e in ledger),
    }


def run_case(level, size, seed, *, policy):
    """Source-run and audit an exact declared scenario/policy/seed."""
    _validate_cell(level, size, seed, policy)
    return attest_native(_native_case(level, size, seed, policy), level=level,
                         size=size, seed=seed, policy=policy)


def _pairs(by_key, start_seed, seeds):
    result = []
    for level, size in ((l, s) for l in LEVELS for s in SIZES):
        for left, right, basis in PAIRS:
            if ((level, size, left) not in COHORTS or
                    (level, size, right) not in COHORTS):
                continue
            observations = []
            for seed in range(start_seed, start_seed + seeds):
                a = by_key[(level, size, left, seed)]
                b = by_key[(level, size, right, seed)]
                observations.append({
                    "seed": seed, "left_ledger_sha256": a["ledger_sha256"],
                    "right_ledger_sha256": b["ledger_sha256"],
                    "left_outcome": a["outcome"], "right_outcome": b["outcome"],
                    "delta_hunter_hp_change": b["hunter_hp_change"] - a["hunter_hp_change"],
                    "delta_party_hp_change": b["party_hp_change"] - a["party_hp_change"],
                    "both_terminal": a["certified_terminal"] and b["certified_terminal"],
                })
            result.append({
                "level": level, "party_size": size, "comparison": f"{left}__vs__{right}",
                "paired_source_scope": basis, "paired_seed_count": seeds,
                "both_terminal": sum(x["both_terminal"] for x in observations),
                "censored_pairs": sum(not x["both_terminal"] for x in observations),
                "observations": observations, "causal_effect_established": False,
                "statistical_effect_estimate": None,
            })
    return result


def census(seeds=4, *, start_seed=0, include_trials=False):
    """31 separate source-native pilot strata; never pool to a Hunter CR."""
    if (type(seeds) is not int or not 1 <= seeds <= 128 or
            type(start_seed) is not int or start_seed < 0 or
            type(include_trials) is not bool):
        raise ValueError("G7-F requires 1..128 seeds, nonnegative start and bool trials")
    all_trials = {}
    cohorts = []
    for level, size, policy in COHORTS:
        trials = [run_case(level, size, start_seed + i, policy=policy)
                  for i in range(seeds)]
        for t in trials:
            key = (level, size, policy, t["seed"])
            if key in all_trials:
                raise AssertionError("A native trial cannot be counted twice")
            all_trials[key] = t
        counts = Counter(t["outcome"] for t in trials)
        if sum(counts.values()) != seeds:
            raise AssertionError("Every trial outcome must remain in denominator")
        unresolved = Counter(t["unresolved_reason"] for t in trials
                             if t["unresolved_reason"])
        cohorts.append({
            "cohort_id": f"G7F-L{level}-P{size}-{policy}",
            "level": level, "party_size": size, "policy": policy,
            "seed_start": start_seed, "seed_count": seeds,
            "counts": {k: counts[k] for k in sorted(NATIVE_OUTCOMES)},
            "native_terminals": sum(t["certified_terminal"] for t in trials),
            "censored_observations": sum(t["censored"] for t in trials),
            "unresolved_reasons": dict(sorted(unresolved.items())),
            "native_pounces": sum(t["genuine_pounces"] for t in trials),
            "native_protections": sum(t["genuine_protections"] for t in trials),
            "source_ledger_sha256": [t["ledger_sha256"] for t in trials],
            "sampled_win_rate": None, "confidence_interval": None,
            "hunter_cr": None, "representative_policy_validated": False,
            **({"trials": trials} if include_trials else {}),
        })
    comparisons = _pairs(all_trials, start_seed, seeds)
    return {
        "version": "B06-G7F-native-stratified-calibration-pilot-v0",
        "study_design": "predeclared_source_policy_pilot_not_representative_player_sampling",
        "observation_count": len(all_trials),
        "cohort_count": len(cohorts), "paired_comparison_count": len(comparisons),
        "seed_count_per_cohort": seeds, "historical_phase3_sha256": PHASE3_SHA,
        "historical_phase3_not_recomputed": True,
        "certified_native_terminal_observations": sum(t["certified_terminal"]
                                                       for t in all_trials.values()),
        "censored_or_unresolved_observations": sum(t["censored"]
                                                    for t in all_trials.values()),
        "representative_encounter_calibration_accepted": False,
        "complete_party_packs_certified": 0,
        "creature_challenge_rating": None, "sampled_win_rate": None,
        "confidence_interval": None,
        "blocking_gates": [
            "positive_native_multitarget_hunter_party_defeat_witness",
            "fictionally_safe_disengagement_before_long_exploration_when_hunter_alive",
            "independently_observed_GM_player_tactics_and_policy_weights",
            "broad_legal_cover_reactions_healing_and_Rite_focus_usage",
            "complete_outcomes_without_fixed_round_censoring",
            "independent_difficulty_benchmarks_before_numeric_hunter_CR",
        ],
        "cohorts": cohorts, "paired_comparisons": comparisons,
    }


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--full-trials", action="store_true")
    args = ap.parse_args(argv)
    result = census(args.seeds, start_seed=args.start_seed,
                    include_trials=args.full_trials)
    print(json.dumps({"pilot_sha256": _digest(result), **result},
                     sort_keys=True, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
