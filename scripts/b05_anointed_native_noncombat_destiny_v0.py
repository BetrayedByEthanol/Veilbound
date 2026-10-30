"""B04/B05 real noncombat Anointed Destiny and GM Mission witness.

One source-paid Lesser Returning Step in an authentic two-round G5 scene,
then actual G4.2 initiative exit and exploration time / optional GM
story event. 72 bounded AH/AM/AL L1–3 source policies. An explicit GM
verdict is an external adjudication, never inferred from quest labels.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_anointed_native_defensive_encounter_v0 import (
    FOCI, OPPONENTS, _one_enemy_hit, _pulse, scene,
)
from scripts.b05_anointed_native_destiny_exploration_v0 import (
    AnointedDestinyExploration,
)
from scripts.b06_encounter_state_v0 import RegenerationChoice,UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

FOCUSES=tuple(FOCI)
LEVELS=(1,2,3)
POLICIES=("clock_partial","gm_recognized","gm_unrecognized","dormant_pause")
SIX_HOURS_SECONDS=21600
FIRST_SEGMENT_SECONDS=21540
LAST_SEGMENT_SECONDS=60
STORY_EVENT_ID="gm:restoration:healed_village"
ROUNDS=2


def _validate(focus,level,opponent,policy,seed):
    if focus not in FOCUSES or opponent not in OPPONENTS or policy not in POLICIES:
        raise ValueError("Only authored source focus/opponent/noncombat policies")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only exact sourced L1–3 Anointed")
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative deterministic policy seed required")


def _spent_lesser_scene(focus,level,opponent,seed):
    """Real source-paid G0/G4 Lesser and true G5 hit before exploration."""
    combat,native=scene(focus=focus,level=level,opponent=opponent,
                        policy="lesser",seed=seed)
    e=combat.e
    clock=e.g4.clock
    # The scene was authored at Round Begin; entering initiative at
    # cursor=0 is a genuine G4.2 boundary, no fabricated world seconds.
    clock.enter_initiative()
    patient="anointed" if focus=="Low" else "patient"
    for round_no in range(1,ROUNDS+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            if round_no==1 and who==patient and focus!="High":
                _pulse(combat,native,focus,"lesser")
            combat.bridge.start_next_turn(RegenerationChoice())
            if e.current!=who or e.pending_regeneration is not None:
                raise AssertionError("Every actor needs its authentic G0 Step")
            if who=="anointed":
                if focus=="Medium" and round_no==1:
                    native.invest(patient,consenting=True)
                if focus=="High" and round_no==2:
                    _pulse(combat,native,focus,"lesser")
            elif who=="foe" and round_no==1:
                _one_enemy_hit(combat,opponent,patient)
            combat.bridge.end_current_turn()
    if e.current is not None or e.cursor!=len(e.order) or combat.pending_attack_slots():
        raise AssertionError("No pending native G0/G5 action at initiative exit")
    clock.leave_initiative()
    if (clock.mode!="exploration" or native.state.destiny!=1
            or sum(x["kind"]=="g5_melee_resolved" for x in e.ledger)!=1):
        raise AssertionError("Only true source Lesser and finished G5 initiative")
    return e,native


def run_policy(*,focus,level,opponent="soldier",
               policy="clock_partial",seed=0):
    _validate(focus,level,opponent,policy,seed)
    e,native=_spent_lesser_scene(focus,level,opponent,seed)
    before_destiny=native.state.destiny
    bridge=AnointedDestinyExploration(e,native)
    clock=e.g4.clock
    e.log("b05_anointed_noncombat_policy",focus=focus,level=level,
          opponent=opponent,policy=policy,seed=seed,
          true_lesser_destiny_before_exploration=before_destiny,
          story_event_id=STORY_EVENT_ID,gm_authority="external_only",
          six_hour_source="g42_world_clock_not_G0_regeneration")
    blocked_unrecognized=False
    blocked_replay=False
    interim_destiny=None
    interim_remainder=None
    dormant_destiny=None
    if policy=="clock_partial":
        clock.advance_exploration(FIRST_SEGMENT_SECONDS)
        self_award=bridge.sync_world_time()
        if self_award!=0:raise AssertionError("359 min must not award a six-hour point")
        interim_destiny=native.state.destiny
        interim_remainder=native.state.six_hour_remainder_minutes
        clock.advance_exploration(LAST_SEGMENT_SECONDS)
        if bridge.sync_world_time()!=1:
            raise AssertionError("360 completed minutes must restore exactly one Destiny")
    elif policy=="gm_recognized":
        if bridge.record_mission_event(STORY_EVENT_ID,gm_recognized=True)!=1:
            raise AssertionError("Unique GM story beat must award one capped Destiny")
        try:
            bridge.record_mission_event(STORY_EVENT_ID,gm_recognized=True)
        except ValueError:
            blocked_replay=True
        if not blocked_replay:
            raise AssertionError("Replayed story event must not farm Destiny")
        clock.advance_exploration(SIX_HOURS_SECONDS)
        if bridge.sync_world_time()!=0:
            raise AssertionError("Six-hour source must not exceed Destiny cap")
    elif policy=="gm_unrecognized":
        try:
            bridge.record_mission_event(STORY_EVENT_ID,gm_recognized=False)
        except UnresolvedDecision:
            blocked_unrecognized=True
        if not blocked_unrecognized:
            raise AssertionError("No auto-Mission from an unrecognized quest beat")
        clock.advance_exploration(SIX_HOURS_SECONDS)
        if bridge.sync_world_time()!=1:
            raise AssertionError("Only real six-hour world clock earned this point")
    else:
        if bridge.apply_bond_verdict(active=False,gm_recognized=True):
            raise AssertionError("GM source explicitly made Mission bond dormant")
        clock.advance_exploration(SIX_HOURS_SECONDS)
        if bridge.sync_world_time()!=0:
            raise AssertionError("Dormant 6h can never recover Destiny")
        dormant_destiny=native.state.destiny
        if bridge.apply_bond_verdict(active=True,gm_recognized=True) is not True:
            raise AssertionError("Only a new external GM bond verdict reactivates")
        clock.advance_exploration(SIX_HOURS_SECONDS)
        if bridge.sync_world_time()!=1:
            raise AssertionError("One active genuine six-hour period must restore")
    e.check()

    time_events=[x for x in e.ledger
                 if x["kind"]=="b05_anointed_destiny_time_reconciled"]
    story_events=[x for x in e.ledger
                  if x["kind"]=="b05_anointed_destiny_mission_recognized"]
    source_heals=[x for x in e.ledger
                  if x["kind"] in ("g4_anointed_returning_step_applied",
                                  "g4_anointed_medium_returning_step_applied",
                                  "g4_anointed_low_returning_step_applied")]
    source_destiny_cost=sum(x["detail"]["destiny_cost"] for x in source_heals)
    earned_story=sum(x["detail"]["destiny_awarded"] for x in story_events)
    earned_time=sum(x["detail"]["destiny_recovered"] for x in time_events)
    if (len(source_heals)!=1 or source_destiny_cost!=1
            or before_destiny!=1 or native.state.destiny!=2
            or earned_story!=(1 if policy=="gm_recognized" else 0)
            or earned_time!=(0 if policy=="gm_recognized" else 1)):
        raise AssertionError("Exact source Lesser, story and clock Destiny must balance")
    if (policy=="gm_recognized" and not blocked_replay or
            policy=="gm_unrecognized" and not blocked_unrecognized):
        raise AssertionError("One source GM replay/recognition refusal required")
    if clock.mode!="exploration" or any(
            x["kind"]=="regeneration_step" and x["round"]>2
            for x in e.ledger):
        raise AssertionError("No synthetic regeneration or initiative after exit")

    report={
        "version":"B04-B05-Anointed-Native-Noncombat-Destiny-v0",
        "focus":focus,"level":level,"opponent":opponent,
        "policy":policy,"seed":seed,
        "metrics":{
            "destiny_initial":2,
            "destiny_after_real_lesser":before_destiny,
            "destiny_after_noncombat":native.state.destiny,
            "lesser_source_destiny_spent":source_destiny_cost,
            "gm_story_destiny_awarded":earned_story,
            "world_clock_destiny_recovered":earned_time,
            "world_seconds":clock.world_seconds,
            "six_hour_remainder_minutes":native.state.six_hour_remainder_minutes,
            "partial_minute_seconds":bridge.partial_minute_seconds,
            "interim_destiny":interim_destiny,
            "interim_remainder_minutes":interim_remainder,
            "dormant_destiny_after_6h":dormant_destiny,
            "blocked_unrecognized_story":blocked_unrecognized,
            "blocked_duplicate_gm_award":blocked_replay,
            "gm_mission_awards":sorted(native.state.mission_awards),
            "active_bond":native.state.active_bond,
            "embodied":native.state.embodied,
            "source_signature_receipts":len(source_heals),
            "source_g5_enemy_hits":sum(
                x["kind"]=="g5_melee_resolved" for x in e.ledger),
            "authentic_exploration_recovery_events":sum(
                x["kind"]=="g4_six_hour_recovery" for x in e.ledger),
            "synthetic_post_exit_regeneration_steps":0,
        },
        "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "ledger":deepcopy(e.ledger),
        "independent_focus_certified":False,
        "noncombat_mission_gm_certified":False,
        "representative_play_certified":False,
        "sampled_win_rate":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,focus,level,opponent="soldier",
                  policy="clock_partial",seed=0):
    expected=run_policy(focus=focus,level=level,opponent=opponent,
                        policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Native noncombat Destiny report does not source-replay")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    return [run_policy(focus=f,level=lv,opponent=o,policy=p,seed=seed)
            for f in FOCUSES for lv in LEVELS for o in OPPONENTS
            for p in POLICIES]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--focus",choices=FOCUSES,default="Low")
    parser.add_argument("--level",type=int,choices=LEVELS,default=3)
    parser.add_argument("--opponent",choices=tuple(OPPONENTS),default="soldier")
    parser.add_argument("--policy",choices=POLICIES,default="gm_recognized")
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--matrix",action="store_true")
    args=parser.parse_args()
    if args.matrix:
        reports=run_matrix(seed=args.seed)
        print(json.dumps({"cases":len(reports),"metrics":[
            {k:r[k] for k in ("focus","level","opponent","policy")}
            |r["metrics"] for r in reports]},indent=2))
    else:
        print(json.dumps(run_policy(
            focus=args.focus,level=args.level,opponent=args.opponent,
            policy=args.policy,seed=args.seed),indent=2))


if __name__=="__main__":
    main()
