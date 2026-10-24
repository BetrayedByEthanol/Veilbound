"""B04/B05 Life Focus: extended native-source attrition and tactical evidence.

Four/eight scheduled rounds with genuine G0 turns, G1 cautious movement,
G5 paid sword actions, assigned Guard/Dodge, G4 packet effects, and G3 rites.
Stop at source incapacitation; never fabricate later attacks or completions.
Role-local baseline deltas, no inferred win probabilities or balance tuning.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_three_focus_life_comparison_v0 import (
    FOCI, OPPONENTS, CHOSEN, _baseline_delta,
)
from scripts.b05_high_priest_life_invocation_v0 import HighLifeLiturgy
from scripts.b05_medium_priest_consecrations_v0 import MediumLifeConsecrations
from scripts.b05_low_life_native_rites_v0 import LowLifeNativeRites
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

ROLE_POLICIES={
    "H":("baseline","guided","shelter","heal_cycle"),
    "M":("baseline","guided","shelter","heal_cycle"),
    "A":("baseline","chosen","exaltation"),
    "B":("baseline","chosen","exaltation"),
}
HORIZONS=(4,8)
PRESSURES={"light":1,"heavy":4}
TACTICS={
    "take_hit":("take_hit",False),
    "guard":("guard",False),
    "cautious_dodge":("dodge",True),
}
ATTACK_FACE=12
SENTRY_VIGOR_DIE=4
HEAL_DIE=3
WOUND_DIE=8


def _validate(role,level,opponent,policy,horizon,pressure,tactic,seed):
    if role not in ROLE_POLICIES or policy not in ROLE_POLICIES[role]:
        raise ValueError("Only source-bound Life policies are supported")
    if type(level) is not int or level not in (1,2,3):
        raise ValueError("Only sourced Priest L1-3")
    if policy=="exaltation" and level!=3:
        raise ValueError("Low Priest Exaltation only at L3")
    if opponent not in OPPONENTS:
        raise ValueError("Only Soldier or prepared Sentry source pressure")
    if type(horizon) is not int or horizon not in HORIZONS:
        raise ValueError("Only 4/8-round requested horizons")
    if pressure not in PRESSURES or tactic not in TACTICS:
        raise ValueError("Exact fixed dice pressure/tactic required")
    if type(seed) is not int or seed<0:
        raise ValueError("Explicit nonnegative replay seed")


def scene(*,role,level,opponent,policy,horizon,pressure,tactic,seed=0):
    _validate(role,level,opponent,policy,horizon,pressure,tactic,seed)
    source,start=OPPONENTS[opponent]
    priest=party_actor(role,level,"priest","party",occupied=((2,2),))
    foe=enemy_actor(source,"foe","enemy",start_state=start,
                    occupied=((3,2),))
    e=Encounter([priest,foe],{"priest":30,"foe":20},seed=seed,
                scenario="B04-B05-Life-extended-native-tactics",
                policy="fixed_source_paid_melee_and_declined_opportunities",
                objective="attrition_receipts_not_win_rate")
    GridMovement(e,width=8,height=7,scene_id="B05-life-tactical-clear")
    SpellState(e)
    DamageState(e)
    if role=="H":
        adapter=HighLifeLiturgy(e,"priest",preparation="standard")
    elif role=="M":
        adapter=MediumLifeConsecrations(e)
    else:
        adapter=LowLifeNativeRites(e,"priest")
    combat=SourceMelee(e)
    if e.order!=("priest","foe"):
        raise AssertionError("Source Initiative changed")
    e.begin_round()
    e.log("b05_extended_life_policy",role=role,level=level,
          opponent=opponent,policy=policy,horizon=horizon,
          pressure=pressure,tactic=tactic,seed=seed,
          attack_d20=ATTACK_FACE,sword_d6=PRESSURES[pressure],
          sentry_vigor_d6=SENTRY_VIGOR_DIE,
          healing_d8=HEAL_DIE,wound_d20=WOUND_DIE,
          opponent_choice="one_attested_native_attempt_each_live_round",
          optional_responses="decline_all",
          no_ghost_turn_after_incapacitation=True,
          source_digests={k:v.source.digest for k,v in e.actors.items()})
    return combat,adapter


def _start(combat,adapter,role,policy,round_no,who):
    e=combat.e
    a=e.actors[who]
    if a.hp<=0 and not a.dead:
        regen=RegenerationChoice(cancel_dying_loss=a.vigor>0)
    elif who=="priest":
        available=max(0,a.regen+e.g3.regen_throughput(who)
                      +e.g4.toxins.modifier(who,"regen_throughput"))
        regen=RegenerationChoice(
            hp=min(max(0,a.hp_max-a.hp),a.vigor,available))
    else:
        regen=RegenerationChoice()
    callback=None
    if (role=="A" and policy=="exaltation"
            and who=="priest" and round_no>1):
        def on_step(enc,recipient):
            step=enc.ledger[-1]
            if (step["kind"]!="regeneration_step"
                    or step["detail"]["actor"]!=recipient):
                raise AssertionError("Actual post-Step2 Held Renewal required")
            a=enc.actors[recipient]
            throughput=max(0,a.regen+enc.g3.regen_throughput(recipient)
                           +enc.g4.toxins.modifier(recipient,"regen_throughput"))
            unused=throughput-step["detail"]["throughput_spent"]
            if (a.hp>0 and a.vp_available>=1 and unused>0
                    and adapter.pending is None and adapter._host()):
                adapter.arm_held(recipient,min(2,unused))
        callback=on_step
    combat.bridge.start_next_turn(regen,on_regeneration_complete=callback)
    if e.current!=who or e.pending_regeneration is not None:
        raise AssertionError("Native Step2/turn did not finish")


def _priest_action(combat,adapter,role,policy,round_no,tactic):
    e=combat.e
    a=e.actors["priest"]
    if a.hp<=0:
        return
    defense,move=TACTICS[tactic]
    if move and round_no%2==0:
        step=(0,1) if a.occupied[0]==(2,2) else (0,-1)
        if not e.g1.step("priest",step,cautious=True):
            raise AssertionError("Declared legal cautious contact step failed")
        if not e.g1.melee_contact("foe","priest"):
            raise AssertionError("Cautious movement may not invent enemy pursuit")
    if round_no==1 and policy not in ("baseline","heal_cycle"):
        spell=(policy if policy in ("guided","shelter")
               else CHOSEN[role])
        kind=("Guided Regeneration" if spell=="guided"
              else "Vital Shelter")
        if role=="H":
            effect=adapter.cast("priest",kind,"priest",
                                access="prepared",mode="maintained")
        elif role=="M":
            effect=adapter.cast("priest",kind,"priest")
        else:
            effect=adapter.cast_chosen("priest")
        if effect is None or effect.kind!=kind or effect.recipient!="priest":
            raise AssertionError("No authentic initial maintained Life effect")
    if (role=="B" and policy=="exaltation"
            and adapter.pending is None and a.vp_available>=1
            and adapter._host() and adapter._host()[0].budget>=2):
        # Each live own-turn arm must pass original once-per-turn, actual
        # B8 budget and available VP rules; do not replay a free arm.
        adapter.arm_vital("priest")
    if (policy=="heal_cycle" and round_no%2==0
            and a.vp_available>=2
            and (a.hp<a.hp_max or a.vigor<a.vigor_max)):
        if role=="H":
            result=adapter.cast("priest","Basic Heal","priest",
                                mode="instant",tier=1,die=HEAL_DIE,
                                hand_available=True)
        elif role=="M":
            result=e.g4.cast_basic_heal(
                "priest","priest",tier=1,die=HEAL_DIE,
                hand_available=True,in_range=True,unobstructed=True,
                unopposed=True)
        else:
            raise AssertionError("Low has no authored heal_cycle")
        if result is None:
            raise AssertionError("Native source-paid recovery interrupted")


def _foe(combat,opponent,pressure,tactic):
    e=combat.e
    profile=("B06-AT-03" if opponent=="soldier"
             else e.g3.sentry_profile("foe"))
    if profile not in ("B06-AT-03","B06-AT-02"):
        raise UnresolvedDecision("Only the original Soldier/Sentry attack")
    if not e.g1.melee_contact("foe","priest"):
        raise UnresolvedDecision("Source foe did not have live G1 contact")
    defense=TACTICS[tactic][0]
    sequence=combat.declare("foe","priest",profiles=(profile,),
                            defenses=(defense,))
    # Once the original G0 defense is actually assigned, consult that
    # canonical ledger receipt and sourced attack bonus. A G5 miss is
    # still PAID but must not supply damage/Vigor dice to resolve().
    assigned=e.ledger[sequence["defenses"][0]]
    if (assigned["kind"]!="defense_assigned"
            or assigned["detail"]["actor"]!="priest"
            or assigned["detail"]["defense"]!=defense):
        raise AssertionError("No exact G0 defense receipt for native attack")
    value=assigned["detail"]["defense_value"]
    landed=(defense=="take_hit"
            or ATTACK_FACE+combat._profile("foe",profile)>value)
    dice={"attack_face":ATTACK_FACE}
    if landed:
        dice.update(damage_face=PRESSURES[pressure],
                    wound_location_roll=WOUND_DIE)
        if profile=="B06-AT-02":
            dice["vigor_die"]=SENTRY_VIGOR_DIE
    result=combat.resolve(sequence,0,**dice)
    if (result["outcome"]=="hit")!=landed:
        raise AssertionError("Precommitted source dice differ from native G5 outcome")
    if result["outcome"] not in ("hit","miss"):
        raise AssertionError("Paid source G5 must resolve hit or miss")
    return result


def _metrics(e,*,horizon):
    priest=e.actors["priest"]
    def rows(kind):
        return [x for x in e.ledger if x["kind"]==kind]
    attacks=rows("g5_melee_resolved")
    delivered=rows("g4_damage_applied")
    steps=[x for x in rows("regeneration_step")
           if x["detail"]["actor"]=="priest"]
    movements=[x for x in rows("g1_movement_step")
               if x["detail"]["actor"]=="priest"]
    if (len(steps)!=e.round or len(attacks)!=e.round
            or any(x["detail"]["target"]!="priest" for x in attacks)
            or len(delivered)!=sum(
                x["detail"]["outcome"]=="hit" for x in attacks)
            or len(movements)>e.round//2):
        raise AssertionError("Attrition cannot use phantom attacks or Step2")
    vigor=[d for x in delivered for d in x["detail"]["vigor_details"]]
    return {
        "rounds_completed":e.round,"horizon":horizon,
        "stopped_incapacitated":priest.hp<=0 or priest.dead,
        "attack_attempts_paid":len(attacks),
        "attacks_hit":sum(x["detail"]["outcome"]=="hit" for x in attacks),
        "attacks_missed":sum(x["detail"]["outcome"]=="miss" for x in attacks),
        "damage_receipts":len(delivered),
        "genuine_regen_steps":len(steps),
        "source_armor":e.g4._armor(priest),
        "starting_hp":priest.hp_max,"starting_vigor":priest.vigor_max,
        "max_vp":priest.vp_max,
        "final_hp":priest.hp,"final_vigor":priest.vigor,
        "wounds":len(priest.wounds),
        "dying":priest.hp<=0,"dead":priest.dead,
        "final_vp":[priest.vp_available,priest.vp_committed,priest.vp_spent],
        "step_hp_restored":sum(x["detail"]["hp_restored"] for x in steps),
        "step_vigor_paid":sum(x["detail"]["throughput_spent"] for x in steps),
        "vigor_prevented":sum(x["prevented"] for x in vigor),
        "vigor_applied":sum(x["applied"] for x in vigor),
        "vital_hp_prevented":sum(x["detail"]["prevented_hp"]
            for x in rows("b05_vital_interposition_applied")),
        "held_hp_restored":sum(x["detail"]["healed"]
            for x in rows("b05_held_renewal_resolved")),
        "projection_or_full_ap_paid":sum(
            x["detail"]["ap_spent"] for x in rows("action_committed")
            if x["detail"]["actor"]=="priest"),
        "movement_steps":len(movements),
        "movement_mp_paid":sum(x["detail"]["cost"] for x in movements),
        "defense_assignments":len([x for x in rows("defense_assigned")
                                   if x["detail"]["actor"]=="priest"]),
        "heal_hp":sum(x["detail"]["hp_restored"]
                      for x in rows("g4_basic_heal_applied")),
        "heal_vigor":sum(x["detail"]["vigor_restored"]
                         for x in rows("g4_basic_heal_applied")),
        "effects_established":len([x for x in rows("g3_effect_established")
                                   if x["detail"]["caster"]=="priest"]),
        "effects_expired":len([x for x in rows("g3_effect_ended")
                               if x["detail"]["caster"]=="priest"]),
        "committed_vp_refunded":sum(x["detail"]["returned"]
            for x in rows("g3_effect_ended")
            if x["detail"]["caster"]=="priest"),
        "exaltation_arms":len(rows("b05_exaltation_armed")),
        "outstanding_exaltation":bool(getattr(
            getattr(e.g3,"low_life",None),"pending",None)),
    }


def run_policy(*,role,level,opponent,policy,horizon,pressure,tactic,
               seed=0):
    combat,adapter=scene(role=role,level=level,opponent=opponent,
                         policy=policy,horizon=horizon,pressure=pressure,
                         tactic=tactic,seed=seed)
    e=combat.e
    for r in range(1,horizon+1):
        if r>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            _start(combat,adapter,role,policy,r,who)
            if who=="priest":
                _priest_action(combat,adapter,role,policy,r,tactic)
            else:
                _foe(combat,opponent,pressure,tactic)
            combat.bridge.end_current_turn()
        if e.actors["priest"].hp<=0:
            break
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots()):
        raise AssertionError("Unresolved G0 turn or paid G5 sequence at terminal")
    e.check()
    report={
        "version":"B04-B05-Life-Extended-Attrition-v0",
        "role":role,"focus":FOCI[role],"level":level,
        "opponent":opponent,"policy":policy,
        "horizon":horizon,"pressure":pressure,"tactic":tactic,
        "seed":seed,
        "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "metrics":_metrics(e,horizon=horizon),
        "ledger":deepcopy(e.ledger),
        "same_actor_baseline_only":True,
        "sampled_win_rate":None,"confidence_interval":None,
        "three_focus_balance_certified":False,
        "numerical_tuning_approved":False,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,role,level,opponent,policy,horizon,pressure,tactic,seed=0):
    expected=run_policy(role=role,level=level,opponent=opponent,
                        policy=policy,horizon=horizon,pressure=pressure,
                        tactic=tactic,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Altered/rehashed attrition report cannot attest")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative seed required")
    cases=[]
    for role,policies in ROLE_POLICIES.items():
        for level in (1,2,3):
            for opponent in OPPONENTS:
                for horizon in HORIZONS:
                    for pressure in PRESSURES:
                        for tactic in TACTICS:
                            for policy in policies:
                                if policy=="exaltation" and level!=3:
                                    continue
                                r=run_policy(
                                    role=role,level=level,opponent=opponent,
                                    policy=policy,horizon=horizon,
                                    pressure=pressure,tactic=tactic,seed=seed)
                                cases.append({
                                    "role":role,"focus":FOCI[role],
                                    "level":level,"opponent":opponent,
                                    "horizon":horizon,"pressure":pressure,
                                    "tactic":tactic,"policy":policy,
                                    "metrics":r["metrics"],
                                    "source_digests":r["source_digests"],
                                    "ledger_sha256":r["ledger_sha256"]})
    keys=lambda c:(c["role"],c["level"],c["opponent"],
                   c["horizon"],c["pressure"],c["tactic"])
    baseline={keys(c):c for c in cases if c["policy"]=="baseline"}
    for c in cases:
        b=baseline[keys(c)]
        # Both deltas keep original source Armor/HP/Vigor. When defensive
        # outcomes stop one policy early, no normalization by fake rounds.
        c["delta_vs_same_source_baseline"]=_baseline_delta(
            c["metrics"],b["metrics"])
        c["round_completion_delta"]=(
            c["metrics"]["rounds_completed"]
            -b["metrics"]["rounds_completed"])
    report={"version":"B04-B05-Life-Extended-Tactical-Balance-v0",
            "seed":seed,"cell_count":len(cases),"cells":cases,
            "long_horizons_requested":list(HORIZONS),
            "only_actual_rounds_counted":True,
            "same_build_fixed_dice_baselines":True,
            "tactical_move_has_declined_opportunities":True,
            "intercession_and_external_Low_access_matched":False,
            "unobserved_actor_action_imputed":False,
            "balanced_focus_ranking":None,
            "sampled_win_rate":None,"confidence_interval":None,
            "three_focus_balance_certified":False,
            "numerical_tuning_approved":False}
    report["audit_sha256"]=canonical_digest(report)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--role",choices=tuple(ROLE_POLICIES))
    p.add_argument("--level",type=int,choices=(1,2,3))
    p.add_argument("--opponent",choices=tuple(OPPONENTS))
    p.add_argument("--policy")
    p.add_argument("--horizon",type=int,choices=HORIZONS)
    p.add_argument("--pressure",choices=tuple(PRESSURES))
    p.add_argument("--tactic",choices=tuple(TACTICS))
    p.add_argument("--seed",type=int,default=0)
    a=p.parse_args()
    args=(a.role,a.level,a.opponent,a.policy,a.horizon,a.pressure,a.tactic)
    if any(x is not None for x in args) and not all(x is not None for x in args):
        p.error("Supply all seven scenario flags, or none for the matrix")
    result=(run_policy(role=a.role,level=a.level,opponent=a.opponent,
                       policy=a.policy,horizon=a.horizon,
                       pressure=a.pressure,tactic=a.tactic,seed=a.seed)
            if all(x is not None for x in args) else run_matrix(seed=a.seed))
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
