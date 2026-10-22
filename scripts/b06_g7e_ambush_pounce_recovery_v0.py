"""B06 G7-E: source-native forest approach, Pounce and long clock handoff.

The forest opening is an authored 1x2 charge lane, NOT an invented
surprise/stealth modifier. A paired ordinary approach+Bite control uses
the same original source dice. Native G0/G1/G4/G4.2/G4.4/G5/G6A
resolve the consequences; exploration continuation never fabricates
combat turns, a full-party victory or Hunter challenge rating.
"""
from collections import Counter
import json

from scripts.b06_encounter_state_v0 import (
    Encounter, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_player_offense_g6b_v0 import PlayerHunterCombat
from scripts.b06_hunter_mixed_party_g6c_v0 import ROSTER, SOURCES, SCORES
from scripts.b06_g7a_native_terminal_census_v0 import (
    roll, _regen_choice, _critical_faces, _melee, _bow, _flame,
    _snapshot, _validate_native_ledger, canonical_digest,
)
from scripts.b06_hunter_completion_g6d_v0 import HunterCompletion
from scripts.b06_g7_calibration_readiness_v0 import _ledger_measures

PHASE3_SHA="c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b"
POSITIONS={"hunter":((2,2),(1,2)),"vanguard":((6,2),),
           "guardian":((5,3),),"archer":((2,4),),"scholar":((3,0),)}
POLICIES=("ordinary_approach","pounce")
OUTCOMES=("hunter_defeat_attested","party_defeat_observed",
          "legal_window_cutoff","unresolved_mechanical_branch")
MAX_ROUNDS=2
MAX_EXPLORATION=21600
CELLS=tuple((level,size,policy) for level in (2,3)
            for size in (3,4) for policy in POLICIES)


def forest_scene(*,level,size,seed):
    """Immutable per-scene starting coordinates and native G0 initiative.

    No generalized ambush surprise advantage is asserted: the canonical
    Initiative rules have no universal surprise-action package yet.
    """
    if (type(level) is not int or level not in (2,3)
            or type(size) is not int or size not in (3,4)
            or type(seed) is not int or seed<0):
        raise ValueError("Only L2/L3 A/B/R[/F] sourced forest approach")
    present=ROSTER[:size]
    actors=[enemy_actor("B06-EN-03","hunter","enemy",
                        occupied=POSITIONS["hunter"])]
    actors.extend(party_actor(SOURCES[p],level,p,"party",
                              occupied=POSITIONS[p]) for p in present)
    e=Encounter(actors,{x:SCORES[x] for x in ("hunter",*present)},
                seed=seed,scenario=f"B06-G7E-forest-lane:L{level}:P{size}",
                objective="bounded_approach_and_clock_observation",
                policy="authored_visible_initiative_no_surprise_bonus")
    GridMovement(e,width=10,height=7,scene_id="G7E-forest-three-step-corridor")
    RangedCombat(e)
    SpellState(e)
    DamageState(e)
    e.begin_round()
    # Before the first genuine Initiative turn, map the preexisting
    # six-hour recovery deadlines onto G4.2 Round Begin labels.
    e.g4.clock.enter_initiative()
    combat=PlayerHunterCombat(e)
    if e.order!=("hunter",*present) or e.g1.front("hunter")!=(3,2):
        raise AssertionError("Forest Pounce lacks actual head-forward geometry")
    if e.g1._pounce_approach("hunter","vanguard",(1,0))!=(3,6):
        raise AssertionError("Source Hunter Pounce cannot traverse legal 1x2 run-up")
    for ident in ("archer","scholar"):
        if ident not in e.actors:continue
        lane=e.g2.lane(
            ident,"hunter",target_cell=e.g1.body_cell("hunter","head"),
            range_kind="bow" if ident=="archer" else "flame")
        # A forest *description* is not a fabricated concealment or cover
        # modifier. The authored fixed lane is clear at scene entry.
        if lane.screens or lane.cover:
            raise AssertionError("G7-E forest entry lane must be explicitly clear")
    return combat


def _opening_bite(combat,seed,*,pounce):
    """Same source attack/critical/damage faces for paired policy comparison."""
    e=combat.e
    target="vanguard"
    prey=e.actors[target]
    if e.current!="hunter" or prey.dead:
        raise UnresolvedDecision("Opening Hunter attack needs living prey on Hunter turn")
    route=((1,0),)*3
    action="opening_bite"
    pick=roll(seed,1,"hunter",action,"defense_choice",2)
    defense=("take_hit" if prey.hp<=0 else
             "guard" if pick==2 and prey.guard_remaining>0 else "dodge")
    if pounce:
        paid=combat.begin_pounce("hunter",target,route,defense=defense)
        assigned=e.ledger[paid["defense_index"]]["detail"]
        profile="B06-AT-06"
    else:
        for delta in route:
            dest,_,_,allies=e.g1.preview("hunter",delta=delta)
            if allies or e.g1._threats("hunter",dest,False):
                raise UnresolvedDecision("Ordinary approach needs genuine Opportunity resolution")
            if e.g1.step("hunter",delta,responses=()) is not True:
                raise UnresolvedDecision("Ordinary Hunter approach interrupted")
        seq=combat.declare("hunter",target,
                           profiles=("B06-AT-04",),defenses=(defense,))
        assigned=e.ledger[seq["defenses"][0]]["detail"]
        profile="B06-AT-04"
    face=roll(seed,1,"hunter",action,"primary_d20",20)
    value=assigned["defense_value"]
    actual="take_hit" if prey.hp<=0 else assigned["defense"]
    if actual=="take_hit":value=None
    confirm,critdice=_critical_faces(
        seed,1,"hunter",action,face,6,actual,value)
    hit=face!=1 and (actual=="take_hit" or face==20 or face+6>value)
    damage_face=roll(seed,1,"hunter",action,"damage_d6",6)
    wound_face=roll(seed,1,"hunter",action,"wound_d20",20)
    predicted_hp=prey.hp
    if hit:
        _,_,packets=e.g4._profile_hit_packets(
            "hunter",target,profile,die_face=damage_face,
            critical=("devastating" if face==20 and confirm==20
                      else "critical" if face==20 and
                        (actual=="take_hit" or
                         confirm!=1 and confirm+6>value)
                      else "strong" if face==20 else "normal"),
            critical_dice=critdice)
        predicted_hp=max(
            -prey.hp_max,prey.hp-sum(
                e.g4._mitigate_hp(prey,p) for p in packets if p.resource=="hp"))
    params={"attack_face":face,"confirmation_face":confirm,
            "critical_dice":critdice if hit else ()}
    if hit:
        params.update(
            damage_face=damage_face,wound_location_roll=wound_face,
            venom_resistance_die=roll(
                seed,1,target,action,"venom_resistance_d20",20))
    if pounce:
        # The G6-A rider independently requires a declared real source
        # ability and contest d20s only while the post-Bite prey is able.
        if predicted_hp>0:
            params.update(
                balance_ability="Strength",
                balance_hunter_face=roll(
                    seed,1,"hunter",action,"balance_hunter_d20",20),
                balance_defender_face=roll(
                    seed,1,target,action,"balance_defender_d20",20))
        outcome=combat.resolve_pounce(paid,**params)
        if (outcome["bite"]!=("hit" if hit else "miss")
                or outcome["action_index"]!=paid["action_index"]):
            raise AssertionError("Pounce result differs from paid G6A source")
    else:
        outcome=combat.resolve(seq,0,**params)
        if outcome["outcome"]!=("hit" if hit else "miss"):
            raise AssertionError("Ordinary Bite result diverged from paid G5")
    return {"kind":"native_pounce" if pounce else "native_ordinary_bite",
            "attack_face":face,"hit":hit,
            "source_damage_face":damage_face if hit else None,
            "source_confirmation_face":confirm,
            "source_critical_dice":list(critdice if hit else ()),
            "outcome":outcome}


def _continuation(combat,seed,round_no):
    """Real native follow-up attacks where sources permit; no free stand."""
    e=combat.e
    for actor in e.order:
        try:
            combat.bridge.start_next_turn(
                _regen_choice(e,actor,seed,round_no))
            a=e.actors[actor]
            hunter=e.actors["hunter"]
            if a.dead or a.hp<=0 or (hunter.dead and actor!="hunter"):
                pass
            elif actor=="hunter":
                target=e.actors["vanguard"]
                if not target.dead and e.g1.melee_contact(
                        "hunter","vanguard",hunter_front=True):
                    defense=("take_hit" if target.hp<=0 else
                             "guard" if roll(seed,round_no,"hunter","bite",
                                "defense_choice",2)==2
                             and target.guard_remaining>0 else "dodge")
                    _melee(combat,"hunter","vanguard","B06-AT-04",
                           defense,seed,round_no)
            elif actor in ("vanguard","guardian"):
                if not any(str(x).lower()=="prone" for x in a.conditions):
                    profile=("B06-PC-A-SWORD" if actor=="vanguard"
                             else "B06-PC-B-MACE")
                    if e.g1.melee_contact(actor,"hunter"):
                        pick=roll(seed,round_no,actor,"melee",
                                  "hunter_defense_choice",2)
                        _melee(combat,actor,"hunter",profile,
                               "dodge" if pick==2 and hunter.hp>0
                               else "take_hit",seed,round_no)
            elif actor=="archer":
                _bow(combat,seed,round_no)
            elif actor=="scholar":
                _flame(combat,seed,round_no,resolve_critical=True)
            combat.bridge.end_current_turn()
        except UnresolvedDecision as exc:
            return {"actor":actor,"round":round_no,"reason":str(exc)}
    return None


def _clock_handoff(combat,seconds):
    """Authoritative Round End -> exploration, not an invented combat exit."""
    e=combat.e
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots()
            or e.g1.pounce is not None
            or e.g4.clock.mode!="initiative"):
        raise UnresolvedDecision("Cannot time-jump an unfinished Hunter encounter")
    e.g4.clock.leave_initiative()
    start=e.g4.clock.world_seconds
    before=len(e.ledger)
    e.g4.advance_exploration(seconds)
    events=e.ledger[before:]
    milestones=[x for x in events if x["kind"]=="g44_hunter_milestone"]
    recoveries=[x for x in events if x["kind"]=="g4_six_hour_recovery"]
    if any(x["detail"].get("world_seconds")>e.g4.clock.world_seconds
           for x in events if x["kind"]=="g4_six_hour_recovery"):
        raise AssertionError("G4 invented future six-hour recovery")
    # WorldClock's conservative initiative/exploration conversion can
    # map an earned 6h checkpoint slightly before 21600 new exploration
    # seconds; its own source-owned due instant is authoritative.
    return {
        "mode":"exploration","elapsed_seconds":seconds,
        "world_seconds_before":start,
        "world_seconds_after":e.g4.clock.world_seconds,
        "hunter_milestone_indices":[x["index"] for x in milestones],
        "recovery_indices":[x["index"] for x in recoveries],
        "recovered_vigor":sum(x["detail"]["vigor"] for x in recoveries),
        "recovered_spent_vp":sum(x["detail"]["spent_vp_recovered"]
                                 for x in recoveries),
        "not_a_combat_terminal":True,
    }


def run_trial(level,size,seed,*,policy="pounce",round_limit=2,
              exploration_seconds=7200,include_ledger=False,
              calibration_policy=None):
    if (type(level) is not int or level not in (2,3)
            or type(size) is not int or size not in (3,4)
            or type(seed) is not int or seed<0
            or policy not in POLICIES or type(policy) is not str
            or type(round_limit) is not int or not 1<=round_limit<=2
            or type(exploration_seconds) is not int
            or not 0<=exploration_seconds<=MAX_EXPLORATION
            or type(include_ledger) is not bool):
        raise ValueError("G7-E accepts four L2/3 P3/4 cells x two authored approaches")
    cohort="forest_pounce" if policy=="pounce" else "forest_ordinary"
    if calibration_policy is not None and calibration_policy!=cohort:
        raise ValueError("G7-F cohort does not match native G7-E approach")
    c=forest_scene(level=level,size=size,seed=seed)
    e=c.e
    if calibration_policy is not None:
        e.log("g7f_policy_selected", cohort=cohort, runner="g7e",
              mode=policy, scenario=e.scenario,
              level=level, party_size=size, seed=seed)
    start=_snapshot(e)
    opening=None
    unresolved=None
    rounds=0
    for round_no in range(1,round_limit+1):
        if round_no>1:c.bridge.begin_next_round()
        if round_no==1:
            try:
                c.bridge.start_next_turn(_regen_choice(e,"hunter",seed,round_no))
                opening=_opening_bite(c,seed,pounce=policy=="pounce")
                c.bridge.end_current_turn()
            except UnresolvedDecision as exc:
                unresolved={"actor":"hunter","round":1,"reason":str(exc)}
            if unresolved is None:
                # Subsequent real Round 1 actor turns, without an
                # invented second Hunter turn.
                for actor in e.order[1:]:
                    try:
                        c.bridge.start_next_turn(_regen_choice(e,actor,seed,1))
                        a=e.actors[actor]
                        h=e.actors["hunter"]
                        if a.hp>0 and not a.dead and not h.dead:
                            if actor in ("vanguard","guardian"):
                                if not any(str(x).lower()=="prone"
                                           for x in a.conditions):
                                    if e.g1.melee_contact(actor,"hunter"):
                                        _melee(c,actor,"hunter",
                                               "B06-PC-A-SWORD" if actor=="vanguard"
                                               else "B06-PC-B-MACE",
                                               "take_hit",seed,1)
                            elif actor=="archer":
                                _bow(c,seed,1)
                            elif actor=="scholar":
                                _flame(c,seed,1,resolve_critical=True)
                        c.bridge.end_current_turn()
                    except UnresolvedDecision as exc:
                        unresolved={"actor":actor,"round":1,"reason":str(exc)}
                        break
        else:
            unresolved=_continuation(c,seed,round_no)
        if unresolved:break
        if e.current is not None or e.cursor!=len(e.order):
            raise AssertionError("G7-E cannot invent a completed Round End")
        rounds+=1
        if e.actors["hunter"].dead:
            break
    terminal=None
    if unresolved:
        outcome="unresolved_mechanical_branch"
    elif e.actors["hunter"].dead:
        try:
            terminal=HunterCompletion(c).attest_hunter_defeat(
                "hunter",party_ids=tuple(x for x in e.order if x!="hunter"))
            outcome="hunter_defeat_attested"
        except UnresolvedDecision as exc:
            unresolved={"actor":"hunter","round":e.round,
                        "reason":"terminal_authority:"+str(exc)}
            outcome="unresolved_mechanical_branch"
    elif all(e.actors[x].dead for x in e.order if x!="hunter"):
        outcome="party_defeat_observed"
    else:
        outcome="legal_window_cutoff"
    clock=None
    if not unresolved and rounds:
        clock=_clock_handoff(c,exploration_seconds)
    turns,ends=_validate_native_ledger(e)
    if not unresolved and (rounds!=ends or turns!=ends*len(e.order)):
        raise AssertionError("G7-E time handoff requires true full rounds")
    pounce=[x for x in e.ledger if x["kind"]=="g6_pounce_resolved"]
    if (policy=="pounce" and opening is not None)!=bool(pounce):
        raise AssertionError("G7-E native Pounce receipt parity lost")
    if policy=="ordinary_approach" and pounce:
        raise AssertionError("Ordinary opening acquired free Pounce")
    result={
        "version":"B06-G7E-native-forest-pounce-clock-v0",
        "scenario_id":f"G7E-L{level}-P{size}-forest-lane-{policy}",
        "level":level,"party_size":size,"seed":seed,
        "opening":"forest_ambush_geometry_only",
        "universal_surprise_benefit_applied":False,
        "policy_id":policy,"round_limit":round_limit,
        "exploration_seconds_requested":exploration_seconds,
        "opening_bite":opening,"outcome":outcome,"unresolved":unresolved,
        "native_terminal":terminal,"clock_handoff":clock,
        "rounds_completed":ends,"turns_completed":turns,
        "initial_state":start,"final_state":_snapshot(e),
        "native_pounce_count":len(pounce),
        "measures":_ledger_measures(e.ledger),
        "ledger_sha256":canonical_digest(e.ledger),
        "complete_party_pack_certified":False,"hunter_cr":None,
    }
    if include_ledger:result["ledger"]=e.ledger
    return result


def census(seeds=8,*,start_seed=0,round_limit=2,exploration_seconds=7200,
           include_trials=False):
    if (type(seeds) is not int or not 1<=seeds<=128
            or type(start_seed) is not int or start_seed<0
            or type(round_limit) is not int or not 1<=round_limit<=2
            or type(exploration_seconds) is not int
            or not 0<=exploration_seconds<=MAX_EXPLORATION
            or type(include_trials) is not bool):
        raise ValueError("G7-E bounded census takes 1–128 deterministic seeds")
    cells=[]
    for level,size,policy in CELLS:
        trials=[run_trial(level,size,start_seed+i,policy=policy,
                          round_limit=round_limit,
                          exploration_seconds=exploration_seconds)
                for i in range(seeds)]
        counts=Counter(x["outcome"] for x in trials)
        if sum(counts.values())!=seeds or set(counts)-set(OUTCOMES):
            raise AssertionError("Every forest trial must have exactly one outcome")
        reasons=Counter(x["unresolved"]["reason"] for x in trials
                        if x["unresolved"])
        cells.append({
            "scenario_id":trials[0]["scenario_id"],
            "level":level,"party_size":size,"policy":policy,
            "seed_start":start_seed,"seed_count":seeds,
            "counts":{key:counts[key] for key in OUTCOMES},
            "unresolved_reasons":dict(sorted(reasons.items())),
            "native_pounces":sum(x["native_pounce_count"] for x in trials),
            "completed_exploration_handoffs":sum(
                x["clock_handoff"] is not None for x in trials),
            "genuine_hunter_milestones":sum(
                len(x["clock_handoff"]["hunter_milestone_indices"])
                for x in trials if x["clock_handoff"] is not None),
            "genuine_six_hour_recoveries":sum(
                len(x["clock_handoff"]["recovery_indices"])
                for x in trials if x["clock_handoff"] is not None),
            "sampled_win_rate":None,"ci95":None,"hunter_cr":None,
            "trial_digests":[{"seed":x["seed"],"outcome":x["outcome"],
                              "ledger_sha256":x["ledger_sha256"]}
                             for x in trials],
            **({"trials":trials} if include_trials else {}),
        })
    return {"version":"B06-G7E-forest-pounce-extended-clock-v0",
            "evidence_grade":"eight_bounded_forest_geometry_policies_not_surprise_or_CR",
            "historical_phase3_not_recomputed":True,
            "historical_phase3_sha256":PHASE3_SHA,
            "round_limit":round_limit,
            "exploration_seconds_requested":exploration_seconds,
            "complete_party_packs_certified":0,
            "creature_challenge_rating":None,
            "remaining_gates":[
                "universal_surprise_awareness_rules_not_authored",
                "full_source_scenario_retreat_or_true_combat_disengagement",
                "positive_native_all_party_death_witness",
                "representative_GM_player_strategy_balance",
            ],
            "cells":cells}


def main(argv=None):
    import argparse
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seeds",type=int,default=8)
    ap.add_argument("--start-seed",type=int,default=0)
    ap.add_argument("--rounds",type=int,default=2)
    ap.add_argument("--exploration-seconds",type=int,default=7200)
    ap.add_argument("--full-trials",action="store_true")
    args=ap.parse_args(argv)
    report=census(args.seeds,start_seed=args.start_seed,
                  round_limit=args.rounds,
                  exploration_seconds=args.exploration_seconds,
                  include_trials=args.full_trials)
    print(json.dumps({"census_sha256":canonical_digest(report),**report},
                     sort_keys=True,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
