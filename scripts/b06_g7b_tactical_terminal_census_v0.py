"""B06 G7-B: source-attested direct Flame critical and one-PC exit policies.

Runs eight scoped, reproducible G7-A-geometry cells: four L2/L3 ×
P3/P4 each with native Flame confirmation and either normal ongoing
attack policy or a preauthored R-Archer west-border withdrawal option.
Neither an archer's exit nor a three-round cutoff is a party victory.
"""
from collections import Counter
import json
from scripts.b06_g7a_native_terminal_census_v0 import (
    ALLOWED, MAX_ROUNDS, canonical_digest, run_trial,
)

POLICIES=("g7b_flame","g7b_archer_exit")
OUTCOMES=("hunter_defeat_attested","party_defeat_observed",
          "archer_withdrawal_attested","legal_window_cutoff",
          "unresolved_mechanical_branch")
FROZEN_PHASE3_SHA256=(
    "c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b")


def native_case(level,size,seed,*,policy="g7b_flame",max_rounds=MAX_ROUNDS,
                include_ledger=False):
    if type(policy) is not str or policy not in POLICIES:
        raise ValueError("G7-B requires one of two preauthored policy choices")
    report=run_trial(level,size,seed,max_rounds=max_rounds,
                     include_ledger=include_ledger,policy_mode=policy)
    if report["outcome"] not in OUTCOMES or report["complete_party_pack_certified"]:
        raise AssertionError("G7-B result exceeds source-supported outcome")
    if (report["outcome"]=="archer_withdrawal_attested")!=bool(
            report["one_party_member_exit_only"]):
        raise AssertionError("Archer withdrawal cannot assert a party terminal")
    if report["outcome"]=="archer_withdrawal_attested":
        t=report["native_terminal"]
        if (policy!="g7b_archer_exit"
                or t is None or not t["not_whole_party_withdrawal"]
                or report["final_state"]["archer"]["occupied"]!=[[0,4]]
                or report["measures"]["g2_arrows_launched"]>
                   report["rounds_completed"]):
            raise AssertionError("Not a source-bound R actor exit")
    return report


def census(seeds=8,*,start_seed=0,max_rounds=MAX_ROUNDS,
           include_trials=False):
    if (type(seeds) is not int or not 1<=seeds<=128
            or type(start_seed) is not int or start_seed<0
            or type(max_rounds) is not int or not 1<=max_rounds<=MAX_ROUNDS
            or type(include_trials) is not bool):
        raise ValueError("G7-B bounded census requires 1–128 keyed seeds")
    cases=[]
    for level,size in sorted(ALLOWED):
        for policy in POLICIES:
            trials=[native_case(level,size,start_seed+i,policy=policy,
                               max_rounds=max_rounds)
                    for i in range(seeds)]
            categories=Counter(x["outcome"] for x in trials)
            if sum(categories.values())!=seeds or set(categories)-set(OUTCOMES):
                raise AssertionError("Every G7-B seed needs exactly one outcome")
            issues=Counter(x["unresolved"]["reason"] for x in trials
                           if x["unresolved"] is not None)
            if sum(issues.values())!=categories["unresolved_mechanical_branch"]:
                raise AssertionError("Mechanical blocker denominator mismatch")
            cases.append({
                "scenario_id":ALLOWED[(level,size)],
                "policy":policy,"level":level,"party_size":size,
                "seed_start":start_seed,"seed_count":seeds,
                "counts":{x:categories[x] for x in OUTCOMES},
                "unresolved_reasons":dict(sorted(issues.items())),
                "incomplete_or_single_exit":(
                    categories["legal_window_cutoff"]+
                    categories["unresolved_mechanical_branch"]+
                    categories["archer_withdrawal_attested"]),
                "native_hunter_death_count":categories["hunter_defeat_attested"],
                "actual_party_withdrawals":0,
                "sampled_win_rate":None,"ci95":None,"hunter_cr":None,
                "trials_digest":[{"seed":x["seed"],"outcome":x["outcome"],
                                  "ledger_sha256":x["ledger_sha256"]}
                                 for x in trials],
                **({"trials":trials} if include_trials else {}),
            })
    return {
        "version":"B06-G7B-native-flame-and-archer-exit-v0",
        "evidence_grade":"eight_bounded_policy_cells_not_complete_party_calibration",
        "policies":list(POLICIES),
        "max_rounds":max_rounds,
        "historical_phase3_not_recomputed":True,
        "historical_phase3_sha256":FROZEN_PHASE3_SHA256,
        "complete_party_packs_certified":0,
        "creature_challenge_rating":None,
        "unresolved_next_gates":[
            "full_party_retreat_and_reinforcement_authority",
            "source_attested_party_wipe_terminal",
            "native_reactive_prepared_protection_in_mixed_party_loop",
            "alternative_frontline_and_forest_ambush_pounce",
            "genuine_long_toxin_and_six_hour_postcombat_recovery",
        ],
        "cases":cases,
    }


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds",type=int,default=8)
    parser.add_argument("--start-seed",type=int,default=0)
    parser.add_argument("--rounds",type=int,default=MAX_ROUNDS)
    parser.add_argument("--full-trials",action="store_true")
    args=parser.parse_args(argv)
    answer=census(args.seeds,start_seed=args.start_seed,
                  max_rounds=args.rounds,include_trials=args.full_trials)
    print(json.dumps({"census_sha256":canonical_digest(answer),**answer},
                     sort_keys=True,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
