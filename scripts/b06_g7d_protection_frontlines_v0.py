"""B06 G7-D: native protective Bite policies and B-frontline alternatives.

Seven bounded two-round cohorts: three A-front L3/P4 (control, Reactive
Shield and Prepared Body Intervene), plus four source-backed B-front
L2/L3 x P3/P4. All attacks, protection, resource payments, venom,
real G0 turns and G4 HP changes use native encounter APIs. Not CR.
"""
from collections import Counter
import json

from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import (
    roll, _regen_choice, _melee, _bow, _flame, _snapshot,
    _validate_native_ledger, canonical_digest,
)
from scripts.b06_g7_calibration_readiness_v0 import _ledger_measures
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
from scripts.b06_hunter_reactive_intervene_g6d_v0 import ReactiveHunterProtection
from scripts.b06_hunter_completion_g6d_v0 import HunterCompletion

MAX_ROUNDS=2
POLICIES=("control","reactive_shield","prepared_body","b_front")
OUTCOMES=("hunter_defeat_attested","party_defeat_observed",
          "legal_window_cutoff","unresolved_mechanical_branch")
PHASE3_SHA="c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b"
CELLS=tuple(
    [(3,4,policy) for policy in POLICIES[:3]]
    +[(level,size,"b_front") for level in (2,3) for size in (3,4)]
)


def _protected_bite(combat,executor,seed,round_no,*,method,prepared_label=None):
    """One real paid G5 Hunter Bite, intercepted before its source attack roll.

    The original predeclared ward defense is authenticated by the G6-D
    adapter; its single confirmation differs by Shield Guard versus Body.
    All dice come from fixed independent SHA-256 keys, not recycled rolls.
    """
    e=combat.e
    action="melee:B06-AT-04"
    ward=e.actors["vanguard"]
    pick=roll(seed,round_no,"hunter","bite","defense_choice",2)
    defense=("take_hit" if ward.hp<=0 else
             "guard" if pick==2 and ward.guard_remaining>0 else "dodge")
    seq=combat.declare("hunter","vanguard",
                       profiles=("B06-AT-04",),defenses=(defense,))
    source_bonus=combat._profile("hunter","B06-AT-04")
    face=roll(seed,round_no,"hunter",action,"primary_d20",20)
    assigned=e.ledger[seq["defenses"][0]]["detail"]
    original=assigned["defense"]
    value=assigned["defense_value"]
    original_hit=face!=1 and (
        original=="take_hit" or face==20 or face+source_bonus>value)
    shield=e.actors["guardian"].guard_value if method=="shield_guard" else None
    stopped=(method=="shield_guard" and original_hit and face!=20
             and face+source_bonus<=shield)
    hit=original_hit and not stopped
    confirm=(roll(seed,round_no,"hunter",action,"confirmation",20)
             if face==20 else None)
    critical="normal"
    if hit and face==20:
        if confirm==20:
            critical="devastating"
        elif method=="body_take_hit" and original=="take_hit":
            critical="critical"
        elif confirm!=1 and confirm+source_bonus > (
                shield if method=="shield_guard" else value):
            critical="critical"
        else:
            critical="strong"
    n={"normal":0,"strong":1,"critical":2,"devastating":2}[critical]
    kwargs={
        "protector_id":"guardian","method":method,"attack_face":face,
        "confirmation_face":confirm,
        "critical_dice":tuple(
            roll(seed,round_no,"hunter",action,"critical_d4",4,i)
            for i in range(n)),
    }
    if prepared_label is not None:
        kwargs["prepared_label"]=prepared_label
    if hit:
        kwargs.update(
            damage_face=roll(seed,round_no,"hunter",action,"damage_d6",6),
            wound_location_roll=roll(
                seed,round_no,"hunter",action,"wound_d20",20),
            venom_resistance_die=roll(
                seed,round_no,
                "guardian" if method=="body_take_hit" else "vanguard",
                action,"venom_resistance_d20",20))
    outcome=executor.resolve(seq,**kwargs)
    if (outcome["original_hit"]!=original_hit
            or outcome["recipient"]!=(
                "guardian" if hit and method=="body_take_hit" else
                "vanguard" if hit else None)):
        raise AssertionError("G7-D misclassified native protective source hit")
    return outcome


def _prepare_body(combat,executor):
    """Only the original B Guardian can reserve one real safe G1 return."""
    e=combat.e
    if e.current!="guardian" or e.actors["guardian"].hp<=0:
        raise UnresolvedDecision("G7-D Prepared Body needs living Guardian turn")
    dest,_,_,allies=e.g1.preview("guardian",delta=(1,0))
    if allies or e.g1._threats("guardian",dest,False):
        raise UnresolvedDecision("G7-D Guardian preparation needs legal unthreatened step")
    if e.g1.step("guardian",(1,0),responses=()) is not True:
        raise UnresolvedDecision("G7-D Guardian source reposition interrupted")
    return executor.prepare(
        "guardian","vanguard",method="body_take_hit",delta=(-1,0),
        trigger_key="g6d:prepared:hunter:vanguard:next_bite")


def _validate_protection(e,policy):
    """Do not count protected hits from flags or fabricated transfer claims."""
    facts=[x for x in e.ledger if x["kind"]=="g6d_protective_bite_attested"]
    expected_method={"reactive_shield":"shield_guard",
                     "prepared_body":"body_take_hit"}.get(policy)
    for ev in facts:
        d=ev["detail"]
        if (expected_method is None or
                d.get("method")!=expected_method
                or d.get("attacker")!="hunter"
                or d.get("ward")!="vanguard"
                or d.get("protector")!="guardian"):
            raise AssertionError("Unexpected protection source or method")
        slot=d.get("action_index")
        attest=[x for x in e.ledger if x["kind"]=="g5_melee_resolved"
                and x["detail"].get("action_index")==slot
                and x["index"]>ev["index"]]
        if len(attest)!=1 or e.g5.pending_attack_slots("hunter"):
            raise AssertionError("Protective Bite must consume its paid G5 slot")
        proof=(d.get("reaction_index") if policy=="reactive_shield"
               else d.get("interception_index"))
        if type(proof) is not int or not 0<=proof<ev["index"]:
            raise AssertionError("No native paid protection event index")
        item=e.ledger[proof]
        if (item["kind"]!=(
                "spontaneous_committed" if policy=="reactive_shield"
                else "interception_released")
                or item["detail"].get("actor")!="guardian"):
            raise AssertionError("Protected hit missing authentic G0 resource")
        if policy=="reactive_shield" and d.get("interception_index") is not None:
            raise AssertionError("Reactive cannot borrow prepared movement")
        if policy=="prepared_body":
            if d.get("reaction_index") is not None:
                raise AssertionError("Prepared cannot spend guardian Reaction")
            moves=[x for x in e.ledger if x["kind"]=="g1_movement_step"
                   and x["detail"].get("actor")=="guardian"
                   and x["index"]>proof and x["index"]<ev["index"]]
            if len(moves)!=1 or moves[0]["detail"].get("new")!=[[3,3]]:
                raise AssertionError("Prepared Bite requires real return to head lane")
    return {"attested_protections":len(facts),
            "reactive_uses":sum(x["detail"]["activation"]=="reactive" for x in facts),
            "prepared_uses":sum(x["detail"]["activation"]=="prepared" for x in facts)}


def run_trial(level,size,seed,*,policy,round_limit=MAX_ROUNDS,
              include_ledger=False):
    """Execute authored tactical choices; classify all censored branches."""
    if (type(level) is not int or type(size) is not int
            or type(seed) is not int or seed<0
            or type(round_limit) is not int
            or not 1<=round_limit<=MAX_ROUNDS
            or type(include_ledger) is not bool
            or (level,size,policy) not in CELLS):
        raise ValueError("G7-D only supports seven source-authored pilot cells")
    frontline=("B_head_forward" if policy=="b_front" else "A_head_forward")
    combat=mixed_scene(level=level,size=size,seed=seed,frontline=frontline)
    e=combat.e
    protection=(ReactiveHunterProtection(combat)
                if policy in ("reactive_shield","prepared_body") else None)
    start=_snapshot(e)
    unresolved=None
    stored_label=None
    for round_no in range(1,round_limit+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for actor in e.order:
            try:
                combat.bridge.start_next_turn(
                    _regen_choice(e,actor,seed,round_no))
                a=e.actors[actor]
                hunter=e.actors["hunter"]
                front=("guardian" if policy=="b_front" else "vanguard")
                ward=e.actors[front]
                if hunter.dead or a.dead or a.hp<=0:
                    pass
                elif actor=="hunter":
                    if not ward.dead:
                        if (protection is not None
                                and e.actors["guardian"].hp>0
                                and (policy=="reactive_shield" or
                                     policy=="prepared_body" and round_no>1
                                     and stored_label is not None)):
                            method=("shield_guard" if policy=="reactive_shield"
                                    else "body_take_hit")
                            _protected_bite(
                                combat,protection,seed,round_no,
                                method=method,
                                prepared_label=(
                                    stored_label if policy=="prepared_body" else None))
                            stored_label=None
                        else:
                            defense=("take_hit" if ward.hp<=0 else
                                     "guard" if roll(
                                         seed,round_no,"hunter","bite",
                                         "defense_choice",2)==2
                                         and ward.guard_remaining>0
                                     else "dodge")
                            _melee(combat,"hunter",front,"B06-AT-04",
                                   defense,seed,round_no)
                elif actor in ("vanguard","guardian"):
                    if policy=="prepared_body" and actor=="guardian" and round_no==1:
                        if ward.dead or e.actors["vanguard"].dead:
                            pass
                        else:
                            stored_label=_prepare_body(combat,protection)
                    else:
                        choice=roll(seed,round_no,actor,"melee",
                                    "hunter_defense_choice",2)
                        defense=("dodge" if choice==2 and hunter.hp>0
                                 else "take_hit")
                        profile=("B06-PC-A-SWORD" if actor=="vanguard"
                                 else "B06-PC-B-MACE")
                        _melee(combat,actor,"hunter",profile,defense,seed,round_no)
                elif actor=="archer":
                    _bow(combat,seed,round_no)
                elif actor=="scholar":
                    _flame(combat,seed,round_no,resolve_critical=True)
                else:
                    raise AssertionError("No fictional party actor")
                combat.bridge.end_current_turn()
            except UnresolvedDecision as exc:
                unresolved={"actor":actor,"round":round_no,"reason":str(exc)}
                break
        if unresolved is not None:
            break
        if e.current is not None or e.cursor!=len(e.order):
            raise AssertionError("G7-D needs genuine native Round End")
        if hunter.dead or all(e.actors[x].dead for x in e.order if x!="hunter"):
            break
    if unresolved is not None:
        status="unresolved_mechanical_branch"
        terminal=None
    elif e.actors["hunter"].dead:
        try:
            terminal=HunterCompletion(combat).attest_hunter_defeat(
                "hunter",party_ids=tuple(x for x in e.order if x!="hunter"))
            status="hunter_defeat_attested"
        except UnresolvedDecision as exc:
            status="unresolved_mechanical_branch"
            unresolved={"actor":"hunter","round":e.round,
                        "reason":"hunter_terminal:"+str(exc)}
            terminal=None
    elif all(e.actors[x].dead for x in e.order if x!="hunter"):
        status="party_defeat_observed"
        terminal=None
    else:
        status="legal_window_cutoff"
        terminal=None
    turns,ends=_validate_native_ledger(e)
    if status!="unresolved_mechanical_branch" and (
            e.current is not None or ends!=e.round):
        raise AssertionError("Terminal needs full real G0 turns")
    proof=_validate_protection(e,policy)
    measures=_ledger_measures(e.ledger)
    summary={
        "version":"B06-G7D-native-protection-frontline-v0",
        "scenario_id":f"G7D-L{level}-P{size}-warned_clear-{frontline}-{policy}",
        "level":level,"party_size":size,"seed":seed,"policy_id":policy,
        "opening":"warned_clear","frontline":frontline,
        "round_limit":round_limit,"outcome":status,
        "native_terminal":terminal,"unresolved":unresolved,
        "rounds_completed":ends,"turns_completed":turns,
        "initial_state":start,"final_state":_snapshot(e),
        "protection":proof,"measures":measures,
        "ledger_sha256":canonical_digest(e.ledger),
        "complete_party_pack_certified":False,"hunter_cr":None,
    }
    if include_ledger:
        summary["ledger"]=e.ledger
    return summary


def census(seeds=8,*,start_seed=0,round_limit=MAX_ROUNDS,include_trials=False):
    if (type(seeds) is not int or not 1<=seeds<=128
            or type(start_seed) is not int or start_seed<0
            or type(round_limit) is not int or not 1<=round_limit<=MAX_ROUNDS
            or type(include_trials) is not bool):
        raise ValueError("G7-D requires 1–128 seeds and 1–2 native rounds")
    cells=[]
    for level,size,policy in CELLS:
        trials=[run_trial(level,size,start_seed+i,policy=policy,
                          round_limit=round_limit) for i in range(seeds)]
        count=Counter(x["outcome"] for x in trials)
        if sum(count.values())!=seeds or set(count)-set(OUTCOMES):
            raise AssertionError("G7-D denominator mismatch")
        unresolved=Counter(x["unresolved"]["reason"] for x in trials
                           if x["unresolved"])
        protections=sum(x["protection"]["attested_protections"] for x in trials)
        cells.append({
            "scenario_id":trials[0]["scenario_id"],
            "level":level,"party_size":size,"policy":policy,
            "seed_start":start_seed,"seed_count":seeds,
            "counts":{key:count[key] for key in OUTCOMES},
            "unresolved_reasons":dict(sorted(unresolved.items())),
            "native_protective_bites":protections,
            "complete_party_packs_certified":0,
            "sampled_win_rate":None,"ci95":None,"hunter_cr":None,
            "trial_digests":[{"seed":x["seed"],"outcome":x["outcome"],
                              "ledger_sha256":x["ledger_sha256"]}
                             for x in trials],
            **({"trials":trials} if include_trials else {}),
        })
    return {
        "version":"B06-G7D-protection-and-alternate-frontline-v0",
        "evidence_grade":"seven_bounded_source_policy_cohorts_not_CR",
        "round_limit":round_limit,
        "historical_phase3_not_recomputed":True,
        "historical_phase3_sha256":PHASE3_SHA,
        "complete_party_packs_certified":0,"creature_challenge_rating":None,
        "remaining_gates":[
            "protective_B_front_with_A_guard_capability_unverified",
            "native_multi_target_Hunter_party_wipe",
            "genuine_forest_ambush_and_pounce_contact",
            "long_toxin_and_postcombat_recovery",
            "representative_GM_policy_sampling_and_CR_calibration",
        ],
        "cells":cells,
    }


def main(argv=None):
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seeds",type=int,default=8)
    p.add_argument("--start-seed",type=int,default=0)
    p.add_argument("--rounds",type=int,default=MAX_ROUNDS)
    p.add_argument("--full-trials",action="store_true")
    args=p.parse_args(argv)
    report=census(args.seeds,start_seed=args.start_seed,
                  round_limit=args.rounds,include_trials=args.full_trials)
    print(json.dumps({"census_sha256":canonical_digest(report),**report},
                     sort_keys=True,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
