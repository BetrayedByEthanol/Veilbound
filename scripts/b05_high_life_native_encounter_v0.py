"""B04/B05 High Life L1-3: source-native G0/G3/G4/G4.5/G5 encounter policies.

Two authentic Soldier/Sentry hits against a source-backed F ally over two
rounds; High Priest H chooses independently authored preparation/prayer policy.
No enemy AI, sampled win rate, independently calibrated CR or Focus sign-off.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_high_priest_life_invocation_v0 import HighLifeLiturgy
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

OPPONENTS={
    "soldier":("B06-EN-02",None),
    "sentry_prepared":("B06-EN-01","prepared_start"),
}
POLICIES=(
    "baseline", "prepared_guided", "prepared_shelter", "prepared_heal",
    "invoked_heal", "invoked_shelter", "open_heal", "open_shelter",
    "dual_prepared",
)
L3_ONLY=frozenset(("open_heal","open_shelter","dual_prepared"))
PREPARATIONS={
    "baseline":"standard",
    "prepared_guided":"standard",
    "prepared_shelter":"standard",
    "prepared_heal":"standard",
    "invoked_heal":"invocation",
    "invoked_shelter":"ward_invocation",
    "open_heal":"invocation",
    "open_shelter":"ward_invocation",
    "dual_prepared":"standard",
}
ROUNDS=2
ATTACK_D20=12
SWORD_D6=1
SENTRY_VIGOR_D6=4
HEAL_D8=3
ALLY_R1_REGEN_HP=1  # fixed policy keeps a real wound-free deficit for R2


def _validate(level,opponent,policy,seed):
    if type(level) is not int or level not in (1,2,3):
        raise ValueError("Only source-built High Life levels 1-3")
    if opponent not in OPPONENTS or policy not in POLICIES:
        raise ValueError("Unknown exact Soldier/Sentry or High Life policy")
    if policy in L3_ONLY and level!=3:
        raise ValueError("Open Prayer and double Projection exist only at L3")
    if type(seed) is not int or seed<0:
        raise ValueError("Explicit nonnegative deterministic seed required")


def scene(*,level,opponent,policy,seed):
    """Bind source characters, G1/G3/G4, then High access and native G5."""
    _validate(level,opponent,policy,seed)
    source_id,start=OPPONENTS[opponent]
    high=party_actor("H",level,"high","party",occupied=((1,2),))
    foe=enemy_actor(source_id,"foe","enemy",
                    start_state=start,occupied=((3,2),))
    ally=party_actor("F",level,"ally","party",occupied=((2,2),))
    e=Encounter([high,foe,ally],{"high":30,"foe":24,"ally":18},
                seed=seed,scenario="B04-B05-High-Life-native",
                policy="declared_fixed_dice_decline_optional_responses",
                objective="two_round_support_receipts_not_a_victory")
    GridMovement(e,width=8,height=7,scene_id="B05-high-life-clear")
    SpellState(e)
    DamageState(e)
    liturgy=HighLifeLiturgy(e,"high",preparation=PREPARATIONS[policy])
    combat=SourceMelee(e)
    if e.order!=("high","foe","ally"):
        raise AssertionError("Source Initiative priority changed")
    e.begin_round()
    e.log("b05_high_native_policy",level=level,opponent=opponent,
          policy=policy,preparation=PREPARATIONS[policy],
          rounds=ROUNDS,attack_face=ATTACK_D20,
          sword_die=SWORD_D6,sentry_vigor_die=SENTRY_VIGOR_D6,
          heal_d8=HEAL_D8,ally_round1_regen_hp=ALLY_R1_REGEN_HP,
          optional_responses="decline_all",
          source_digests={ident:a.source.digest for ident,a in e.actors.items()})
    return combat,liturgy


def _start(combat,actor_id,round_no):
    e=combat.e
    a=e.actors[actor_id]
    if a.hp<=0 and not a.dead:
        choice=RegenerationChoice(cancel_dying_loss=a.vigor>0)
    elif actor_id=="ally":
        missing=max(0,a.hp_max-a.hp)
        throughput=max(0,a.regen+e.g3.regen_throughput(actor_id)
                       +e.g4.toxins.modifier(actor_id,"regen_throughput"))
        permitted=(ALLY_R1_REGEN_HP if round_no==1 else throughput)
        choice=RegenerationChoice(
            hp=min(missing,a.vigor,throughput,permitted))
    else:
        choice=RegenerationChoice()
    combat.bridge.start_next_turn(choice)
    if e.current!=actor_id or e.pending_regeneration is not None:
        raise AssertionError("One real own-turn Step 2 must complete")


def _high(combat,liturgy,policy,round_no):
    if policy=="baseline":
        return
    if round_no==1:
        actions={
            "prepared_guided":("Guided Regeneration","prepared"),
            "prepared_shelter":("Vital Shelter","prepared"),
            "invoked_shelter":("Vital Shelter","invocation"),
            "open_shelter":("Vital Shelter","open_prayer"),
        }
        if policy=="dual_prepared":
            for spell in ("Guided Regeneration","Vital Shelter"):
                result=liturgy.cast("high",spell,"ally",
                                    access="prepared",mode="maintained")
                if result is None:
                    raise AssertionError("Sourced dual Projection failed")
        elif policy in actions:
            spell,access=actions[policy]
            result=liturgy.cast("high",spell,"ally",
                                access=access,mode="maintained")
            if result is None:
                raise AssertionError("Sourced real High maintained Primary failed")
    elif round_no==2 and policy in ("prepared_heal","invoked_heal","open_heal"):
        access={"prepared_heal":"prepared",
                "invoked_heal":"invocation",
                "open_heal":"open_prayer"}[policy]
        result=liturgy.cast("high","Basic Heal","ally",access=access,
                            mode="instant",tier=1,die=HEAL_D8,
                            hand_available=True)
        if result is None:
            raise AssertionError("Native paid High Basic Heal interrupted")
    # No invented second action or free party attack on either policy.


def _foe(combat,opponent):
    e=combat.e
    profile=("B06-AT-03" if opponent=="soldier"
             else e.g3.sentry_profile("foe"))
    if profile not in ("B06-AT-03","B06-AT-02"):
        raise UnresolvedDecision("Expected source Soldier or prepared Sentry")
    if not e.g1.melee_contact("foe","ally"):
        raise UnresolvedDecision("Source-target G1 melee contact missing")
    sequence=combat.declare("foe","ally",profiles=(profile,),
                            defenses=("take_hit",))
    kwargs={"attack_face":ATTACK_D20,"damage_face":SWORD_D6,
            "wound_location_roll":8}
    if profile=="B06-AT-02":
        kwargs["vigor_die"]=SENTRY_VIGOR_D6
    result=combat.resolve(sequence,0,**kwargs)
    if result["outcome"]!="hit" or result["damage"] is None:
        raise AssertionError("Exactly one resolved native G5 source hit required")


def _metrics(e):
    high=e.actors["high"]
    ally=e.actors["ally"]
    def rows(kind):
        return [x for x in e.ledger if x["kind"]==kind]
    attacks=rows("g5_melee_resolved")
    damages=rows("g4_damage_applied")
    ally_steps=[x for x in rows("regeneration_step")
                if x["detail"]["actor"]=="ally"]
    high_steps=[x for x in rows("regeneration_step")
                if x["detail"]["actor"]=="high"]
    spells=[x for x in rows("b05_high_life_applied")
            if x["detail"]["caster"]=="high"]
    healing=rows("g4_basic_heal_applied")
    if (len(attacks)!=ROUNDS or len(damages)!=ROUNDS
            or len(ally_steps)!=ROUNDS or len(high_steps)!=ROUNDS
            or any(x["detail"]["attacker"]!="foe"
                   or x["detail"]["target"]!="ally"
                   or x["detail"]["outcome"]!="hit" for x in attacks)
            or any(x["detail"]["recipient"]!="ally" for x in damages)
            or any(x["detail"]["recipient"]!="ally" for x in healing)):
        raise AssertionError("Missing genuine source hits, steps or deliveries")
    return {
        "ally_hp":ally.hp,"ally_vigor":ally.vigor,
        "ally_wounds":len(ally.wounds),
        "high_hp":high.hp,"high_vigor":high.vigor,
        "high_vp":[high.vp_available,high.vp_committed,high.vp_spent],
        "paid_g5_hits":len(attacks),"native_g4_damage_events":len(damages),
        "ally_real_steps":len(ally_steps),"high_real_steps":len(high_steps),
        "ally_step_hp_restored":sum(x["detail"]["hp_restored"] for x in ally_steps),
        "ally_step_vigor_spent":sum(x["detail"]["throughput_spent"] for x in ally_steps),
        "primary_heal_hp":sum(x["detail"]["hp_restored"] for x in healing),
        "primary_heal_vigor":sum(x["detail"]["vigor_restored"] for x in healing),
        "vigor_prevented":sum(v["prevented"] for d in damages
                               for v in d["detail"]["vigor_details"]),
        "vigor_applied":sum(v["applied"] for d in damages
                             for v in d["detail"]["vigor_details"]),
        "high_casts":[{"technique":x["detail"]["technique"],
                       "access":x["detail"]["access"],
                       "action_ap":x["detail"]["action_ap"],
                       "spent":x["detail"]["spent"],
                       "surcharge":x["detail"]["surcharge"],
                       "committed":x["detail"]["committed"]}
                      for x in spells],
        "high_ap_paid":sum(x["detail"]["ap_spent"]
                            for x in rows("action_committed")
                            if x["detail"]["actor"]=="high"),
        "high_open_prayer_fills":len(rows("b05_open_prayer_slot_filled")),
        "active_high_effects":len([v for v in e.g3.effects.values()
                                   if v.caster=="high"]),
    }


def run_policy(*,level,opponent,policy,seed=0):
    _validate(level,opponent,policy,seed)
    combat,liturgy=scene(level=level,opponent=opponent,policy=policy,seed=seed)
    e=combat.e
    for round_no in range(1,ROUNDS+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for actor_id in e.order:
            _start(combat,actor_id,round_no)
            if actor_id=="high":
                _high(combat,liturgy,policy,round_no)
            elif actor_id=="foe":
                _foe(combat,opponent)
            combat.bridge.end_current_turn()
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots()):
        raise AssertionError("Source G5 slots or turn remain unresolved")
    e.check()
    report={
        "version":"B04-B05-High-Life-Native-Encounter-v0",
        "level":level,"opponent":opponent,"policy":policy,"seed":seed,
        "preparation":PREPARATIONS[policy],
        "metrics":_metrics(e),
        "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "ledger":deepcopy(e.ledger),
        "full_encounter_certified":False,
        "independent_high_focus_certified":False,
        "three_focus_balance_certified":False,
        "sampled_win_rate":None,"policy_weighting":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,level,opponent,policy,seed=0):
    """Fail closed even when a caller recomputes a forged report hash."""
    expected=run_policy(level=level,opponent=opponent,policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Native High report deviates from exact source replay")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative deterministic seed required")
    cells=[]
    for level in (1,2,3):
        for opponent in OPPONENTS:
            for policy in POLICIES:
                if policy not in L3_ONLY or level==3:
                    r=run_policy(level=level,opponent=opponent,policy=policy,seed=seed)
                    cells.append({
                        "level":level,"opponent":opponent,"policy":policy,
                        "preparation":r["preparation"],
                        "source_digests":r["source_digests"],
                        "metrics":r["metrics"],
                        "ledger_sha256":r["ledger_sha256"],
                    })
    report={"version":"B04-B05-High-Life-Native-Encounter-v0",
            "seed":seed,"cell_count":len(cells),"cells":cells,
            "fixed_policy_comparison":True,
            "source_replay_required":True,
            "independent_high_focus_certified":False,
            "three_focus_balance_certified":False,
            "sampled_win_rate":None,"policy_weighting":None}
    report["audit_sha256"]=canonical_digest(report)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level",type=int,choices=(1,2,3))
    parser.add_argument("--opponent",choices=tuple(OPPONENTS))
    parser.add_argument("--policy",choices=POLICIES)
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args()
    selected=(args.level is not None,args.opponent is not None,
              args.policy is not None)
    if any(selected) and not all(selected):
        parser.error("Supply --level, --opponent and --policy together")
    result=(run_policy(level=args.level,opponent=args.opponent,
                       policy=args.policy,seed=args.seed)
            if all(selected) else run_matrix(seed=args.seed))
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
