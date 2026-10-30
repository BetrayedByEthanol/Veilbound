"""B04/B05 L3 Anointed Guided Regeneration after authentic native G5 injury.

24 fixed-source High/Medium/Low × Soldier/prepared-Sentry ×
Fixed/Maintained × no-waiver/Lesser. One actual paid G5 hit, two real
recipient G0/G4 Steps, G0-paid G3 Guided host, finite shared Destiny.
This is not a representative encounter or independent Focus certificate.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_anointed_native_defensive_encounter_v0 import (
    FOCI, OPPONENTS, _one_enemy_hit, _metrics, scene,
)
from scripts.b05_anointed_native_guided_authority_v0 import AnointedGuidedAuthority
from scripts.b06_encounter_state_v0 import RegenerationChoice
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

FOCUSES=tuple(FOCI)
MODES=("fixed","maintained")
POLICIES=("ordinary_guided","lesser_guided")
LEVEL=3
ROUNDS=2
SECOND_STEP_NATURAL_HP=1


def _validate(focus,opponent,mode,policy,seed):
    if (focus not in FOCUSES or opponent not in OPPONENTS
            or mode not in MODES or policy not in POLICIES):
        raise ValueError("Use one exact L3 Restoration focus/opponent/Guided policy")
    if type(seed) is not int or seed<0:
        raise ValueError("Explicit nonnegative source policy seed required")


def _guide_cast(guide,recipient,mode):
    """Ordinary paid technique host, no Destiny consumed on activation."""
    return guide.cast(recipient,mode=mode,visible=True,unopposed=True)


def run_policy(*,focus,opponent="soldier",mode="maintained",
               policy="lesser_guided",seed=0):
    _validate(focus,opponent,mode,policy,seed)
    combat,native=scene(focus=focus,level=LEVEL,opponent=opponent,
                        policy="baseline",seed=seed)
    e=combat.e
    recipient="anointed" if focus=="Low" else "patient"
    guide=AnointedGuidedAuthority(e,"anointed")
    e.log("b05_anointed_guided_g5_policy",focus=focus,level=LEVEL,
          opponent=opponent,mode=mode,policy=policy,rounds=ROUNDS,
          enemy_hit_count=1,round1_natural_hp=0,
          round2_natural_hp=SECOND_STEP_NATURAL_HP,
          additional_guided_hp=1,ordinary_guided_waiver=policy=="lesser_guided",
          beneficial_healing="explicitly_unopposed",
          medium_vessel_consent=True,optional_responses="decline_all")

    for round_no in range(1,ROUNDS+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            # The only Authority decision is bound to the next real G0
            # recipient Step, not a synthetic timer or caller-created G4 tick.
            if (round_no==2 and who==recipient
                    and policy=="lesser_guided"):
                guide.declare_waiver(recipient,visible=True,unopposed=True)
            choice=(RegenerationChoice(
                hp=SECOND_STEP_NATURAL_HP if round_no==2 else 0)
                if who==recipient else RegenerationChoice())
            combat.bridge.start_next_turn(choice)
            if e.current!=who or e.pending_regeneration is not None:
                raise AssertionError("Expected completed actual G0 beneficiary Step")
            if who=="anointed":
                if focus=="High" and round_no==1:
                    _guide_cast(guide,recipient,mode)
                elif focus=="Medium" and round_no==1:
                    native.invest(recipient,consenting=True)
                elif focus=="Medium" and round_no==2:
                    _guide_cast(guide,recipient,mode)
                elif focus=="Low" and round_no==1:
                    # This legal Projection is only after Low's own
                    # first post-injury G0/G4 Step, for next round's Step.
                    _guide_cast(guide,recipient,mode)
            elif who=="foe" and round_no==1:
                _one_enemy_hit(combat,opponent,recipient)
            combat.bridge.end_current_turn()

    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots() or guide.pending is not None):
        raise AssertionError("G5 slot, G0 turn or Guided waiver remains pending")
    e.check()
    data=_metrics(e,native,focus)
    natural=[event for event in e.ledger if event["kind"]=="regeneration_step"
             and event["detail"]["actor"]==recipient]
    host_events=[event for event in e.ledger
                 if event["kind"]=="b05_anointed_guided_host_established"]
    waivers=[event for event in e.ledger
             if event["kind"]=="g4_anointed_guided_waiver_applied"]
    if (len(natural)!=2 or len(host_events)!=1
            or [x["detail"]["hp_restored"] for x in natural]!=[0,1]
            or [x["detail"]["throughput_spent"] for x in natural]!=[0,1]
            or len(waivers)!=int(policy=="lesser_guided")):
        raise AssertionError("Missing ordinary paid Guided host / natural G4 receipt")
    if not (natural[0]["index"]<natural[1]["index"]
            and (not waivers or natural[1]["index"]<waivers[0]["index"])):
        raise AssertionError("L3 Guided must apply after natural source Step")
    source_host=host_events[0]["detail"]
    data.update({
        "guided_host":source_host["host"],
        "guided_host_ap_index":source_host["ap_index"],
        "guided_host_vp_index":source_host["vp_index"],
        "guided_host_activation_ap":source_host["ap_spent"],
        "guided_host_spent_vp":source_host["vp_spent"],
        "guided_host_committed_vp":source_host["vp_committed"],
        "guided_waiver_count":len(waivers),
        "guided_additional_hp":sum(x["detail"]["hp_restored"] for x in waivers),
        "guided_destiny_spent":2-native.state.destiny,
        "ordinary_hp_restored":sum(x["detail"]["hp_restored"] for x in natural),
        "ordinary_regen_recipient_vigor_spent":sum(
            x["detail"]["throughput_spent"] for x in natural),
        "recipient_regen_step_rounds":[x["round"] for x in natural],
        "recipient_regen_step_indices":[x["index"] for x in natural],
        "g5_hit_index":next(x["index"] for x in e.ledger
                            if x["kind"]=="g5_melee_resolved"),
        "guided_authority_event_indices":[x["index"] for x in waivers],
    })
    report={
        "version":"B04-B05-Anointed-L3-G5-Guided-Pressure-v0",
        "focus":focus,"level":LEVEL,"opponent":opponent,"mode":mode,
        "policy":policy,"seed":seed,
        "metrics":data,
        "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "ledger":deepcopy(e.ledger),
        "independent_focus_certified":False,
        "representative_play_certified":False,
        "sampled_win_rate":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,focus,opponent="soldier",mode="maintained",
                  policy="lesser_guided",seed=0):
    """Full deterministic G0–G5 replay, not self-declared eligibility."""
    expected=run_policy(focus=focus,opponent=opponent,mode=mode,
                        policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("L3 native Guided under G5 pressure diverged")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    return [run_policy(focus=f,opponent=o,mode=m,policy=p,seed=seed)
            for f in FOCUSES for o in OPPONENTS for m in MODES for p in POLICIES]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--focus",choices=FOCUSES,default="High")
    parser.add_argument("--opponent",choices=tuple(OPPONENTS),default="soldier")
    parser.add_argument("--mode",choices=MODES,default="maintained")
    parser.add_argument("--policy",choices=POLICIES,default="lesser_guided")
    parser.add_argument("--matrix",action="store_true")
    args=parser.parse_args()
    if args.matrix:
        reports=run_matrix(seed=args.seed)
        print(json.dumps({"cases":len(reports),"metrics":[
            {k:r[k] for k in ("focus","level","opponent","mode","policy")}
            |r["metrics"] for r in reports]},indent=2))
    else:
        print(json.dumps(run_policy(focus=args.focus,opponent=args.opponent,
                mode=args.mode,policy=args.policy,seed=args.seed),indent=2))


if __name__=="__main__":
    main()
