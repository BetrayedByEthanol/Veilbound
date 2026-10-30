"""B04/B05 — source G5 injury vs ordinary G4 regeneration and Anointed Signature.

Extend the merged #172 fixed Soldier/Sentry witness with two real
player-chosen 1-HP natural allocations; compare no Signature, ordinary
recipient-Vigor Signature and finite 1-Destiny Lesser. Authentic G0/G4/G5
only; not an optimal tactical policy, new offensive profile, GM pilot
or independently certified Archetype × Focus pairing.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_anointed_native_defensive_encounter_v0 import (
    FOCI, LEVELS, OPPONENTS, _one_enemy_hit, _pulse, _metrics, scene,
)
from scripts.b06_encounter_state_v0 import RegenerationChoice
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

POLICIES=("natural_only","natural_plus_signature","natural_plus_lesser")
SOURCE_POLICY={"natural_only":"baseline",
               "natural_plus_signature":"signature",
               "natural_plus_lesser":"lesser"}
ROUNDS=2
NATURAL_HP_EACH_STEP=1


def _validate(focus,level,opponent,policy,seed):
    if focus not in FOCI or opponent not in OPPONENTS or policy not in POLICIES:
        raise ValueError("Only three sourced Anointed Focuses and ordinary policies")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only source-backed L1–3 Anointed")
    if type(seed) is not int or seed<0:
        raise ValueError("Explicit nonnegative deterministic seed required")


def run_policy(*,focus,level,opponent="soldier",policy="natural_plus_signature",seed=0):
    _validate(focus,level,opponent,policy,seed)
    base_policy=SOURCE_POLICY[policy]
    combat,native=scene(focus=focus,level=level,opponent=opponent,
                        policy=base_policy,seed=seed)
    e=combat.e
    recipient="anointed" if focus=="Low" else "patient"
    e.log("b05_anointed_natural_recovery_policy",focus=focus,level=level,
          opponent=opponent,policy=policy,source_policy=base_policy,
          rounds=ROUNDS,natural_hp_each_genuine_recipient_step=1,
          wound_repair=0,optional_responses="decline_all",
          beneficial_healing="explicit_unopposed")

    for round_no in range(1,ROUNDS+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            if round_no==1 and who==recipient and focus!="High":
                _pulse(combat,native,focus,base_policy)
            choice=(RegenerationChoice(hp=NATURAL_HP_EACH_STEP)
                    if who==recipient else RegenerationChoice())
            combat.bridge.start_next_turn(choice)
            if e.current!=who or e.pending_regeneration is not None:
                raise AssertionError("Source G0 Step must complete before next action")
            if who=="anointed":
                if focus=="Medium" and round_no==1 and base_policy!="baseline":
                    native.invest(recipient,consenting=True)
                if focus=="High" and round_no==2:
                    _pulse(combat,native,focus,base_policy)
            elif who=="foe" and round_no==1:
                _one_enemy_hit(combat,opponent,recipient)
            combat.bridge.end_current_turn()

    if e.current is not None or e.cursor!=len(e.order) or combat.pending_attack_slots():
        raise AssertionError("Incomplete native G5 sequence or G0 round")
    e.check()
    result=_metrics(e,native,focus)
    natural=[v for v in e.ledger if v["kind"]=="regeneration_step"
             and v["detail"]["actor"]==recipient]
    hit=[v for v in e.ledger if v["kind"]=="g5_melee_resolved"]
    if (len(natural)!=2 or len(hit)!=1
            or any(step["detail"]["hp_restored"]!=NATURAL_HP_EACH_STEP
                   or step["detail"]["repair_points"]!=0
                   or step["detail"]["throughput_spent"]!=NATURAL_HP_EACH_STEP
                   for step in natural)
            or not hit[0]["detail"]["outcome"]=="hit"
            or natural[0]["index"]<=hit[0]["index"]):
        raise AssertionError("Natural HP allocations must follow source hit on both real Steps")
    result.update({
        "natural_hp_restored":sum(x["detail"]["hp_restored"] for x in natural),
        "natural_recipient_vigor_spent":sum(x["detail"]["throughput_spent"] for x in natural),
        "natural_step_rounds":[x["round"] for x in natural],
        "natural_step_indices":[x["index"] for x in natural],
        "g5_hit_index":hit[0]["index"],
    })
    report={
        "version":"B04-B05-Anointed-G5-Natural-Recovery-v0",
        "focus":focus,"level":level,"opponent":opponent,"policy":policy,
        "seed":seed,"metrics":result,
        "source_ids":{name:a.source.source_id for name,a in e.actors.items()},
        "source_digests":{name:a.source.digest for name,a in e.actors.items()},
        "ledger":deepcopy(e.ledger),
        "independent_focus_certified":False,
        "representative_play_certified":False,
        "sampled_win_rate":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,focus,level,opponent="soldier",
                  policy="natural_plus_signature",seed=0):
    expected=run_policy(focus=focus,level=level,opponent=opponent,
                        policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Natural allocation/Signature report is not native source replay")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    return [
        run_policy(focus=focus,level=lv,opponent=foe,policy=policy,seed=seed)
        for focus in FOCI for lv in LEVELS for foe in OPPONENTS
        for policy in POLICIES
    ]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--focus",choices=tuple(FOCI),default="High")
    parser.add_argument("--level",type=int,choices=LEVELS,default=3)
    parser.add_argument("--opponent",choices=tuple(OPPONENTS),default="soldier")
    parser.add_argument("--policy",choices=POLICIES,default="natural_plus_signature")
    parser.add_argument("--matrix",action="store_true")
    args=parser.parse_args()
    if args.matrix:
        reports=run_matrix(seed=args.seed)
        print(json.dumps({"policies":len(reports),"metrics":[
            {k:r[k] for k in ("focus","level","opponent","policy")}
            |r["metrics"] for r in reports]},indent=2))
    else:
        print(json.dumps(run_policy(focus=args.focus,level=args.level,
            opponent=args.opponent,policy=args.policy,seed=args.seed),indent=2))


if __name__=="__main__":
    main()
