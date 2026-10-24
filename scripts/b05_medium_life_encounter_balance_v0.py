"""B04/B05 Medium Life: two-round native Soldier/Sentry support comparisons.

Every opponent hit uses actual G5 declaration/roll, G4.5 action attribution,
source JSON HP/Vigor packets, G4 injury, G0 turn/Step 2 and G3 effects.
Fixed choices are *policies*, not a sampled player population, calibrated
difficulty, enemy AI, a game winner, or an independent Focus certificate.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_medium_priest_consecrations_v0 import MediumLifeConsecrations
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

OPPONENTS = {
    "soldier": ("B06-EN-02", None),
    "sentry_prepared": ("B06-EN-01", "prepared_start"),
}
POLICIES = (
    "no_magic", "guided", "shelter", "basic_heal",
    "guided_intercession", "shelter_intercession",
)
# The only intercedable source attack in this two-opponent pack is the
# Sentry's independently paid, reserved Fire/Vigor sword hit.
ROUNDS = 2
MELEE_FACE = 12
SWORD_DIE = 1
SENTRY_VIGOR_DIE = 4
HEAL_D8 = 3


def _validate(opponent, level, policy, seed):
    if opponent not in OPPONENTS or policy not in POLICIES:
        raise ValueError("Choose exact source opponent and supported policy")
    if type(level) is not int or level not in (1, 2, 3):
        raise ValueError("Only Medium Life levels 1-3 are sourced")
    if type(seed) is not int or seed < 0:
        raise ValueError("Explicit nonnegative source seed required")
    if policy.endswith("_intercession") and level < 3:
        raise ValueError("Intercession exists only at level 3")
    if policy == "shelter_intercession" and opponent != "sentry_prepared":
        raise ValueError("No native Soldier Vigor packet for Shelter Intercession")


def _scene(opponent, level, policy, seed):
    source_id, start = OPPONENTS[opponent]
    medium = party_actor("M",level,"medium","party",occupied=((1,2),))
    foe = enemy_actor(source_id,"foe","enemy",
                      start_state=start,occupied=((3,2),))
    ally = party_actor("F",level,"ally","party",occupied=((2,2),))
    e=Encounter([medium,foe,ally],
        {"medium":30,"foe":24,"ally":18},
        seed=seed,scenario="B04-B05-Medium-Life-native-encounter",
        policy="fixed_dice_decline_optional_responses",
        objective="compare_native_support_resourcetraces_not_a_terminal")
    GridMovement(e,width=8,height=7,scene_id="B05-medium-life-clear")
    SpellState(e)
    DamageState(e)
    medium_adapter=MediumLifeConsecrations(e)
    combat=SourceMelee(e)
    if e.order!=("medium","foe","ally"):
        raise AssertionError("Changed source Initiative order")
    e.begin_round()
    e.log("b05_balance_policy_selected",opponent=opponent,level=level,
          policy=policy,rounds=ROUNDS,attack_face=MELEE_FACE,
          sword_damage_die=SWORD_DIE,sentry_vigor_die=SENTRY_VIGOR_DIE,
          heal_die=HEAL_D8,optional_responses="decline_all",
          foe_source=foe.source.digest,medium_source=medium.source.digest,
          ally_source=ally.source.digest)
    return combat,medium_adapter


def _start(combat, medium_adapter, policy, actor):
    e=combat.e
    a=e.actors[actor]
    response=None
    if actor=="ally":
        bonus=e.g3.regen_throughput(actor)
        if policy=="guided_intercession" and a.hp<a.hp_max:
            bonus+=1
            def response(enc,recipient):
                medium_adapter.intercede_regeneration("medium",recipient)
        # Only use actual Current Vigor and missing HP; never revive
        # Dying HP or choose a wound target by silence.
        if a.hp<=0 and not a.dead:
            choice=RegenerationChoice(cancel_dying_loss=(a.vigor>0))
            response=None
        else:
            choice=RegenerationChoice(
                hp=min(max(0,a.hp_max-a.hp),a.vigor,a.regen+bonus))
    else:
        choice=RegenerationChoice(
            cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))
    combat.bridge.start_next_turn(choice,on_regeneration_ready=response)
    if e.current!=actor or e.pending_regeneration is not None:
        raise AssertionError("Native Initiative/Step 2 did not complete")


def _medium(combat,adapter,policy,round_no):
    e=combat.e
    if round_no==1:
        spell={
            "guided":"Guided Regeneration",
            "shelter":"Vital Shelter",
            "guided_intercession":"Guided Regeneration",
            "shelter_intercession":"Vital Shelter",
        }.get(policy)
        if spell is not None:
            recipient=("medium" if policy.endswith("_intercession") else "ally")
            effect=adapter.cast("medium",spell,recipient)
            if effect is None:
                raise AssertionError("Legal source Consecration did not establish")
    elif round_no==2 and policy=="basic_heal":
        # At Level 1 Medium starts with 4 VP and can pay the T1
        # two-Spent cost without an invented Frugal Technique discount.
        heal=e.g4.cast_basic_heal(
            "medium","ally",tier=1,die=HEAL_D8,
            hand_available=True,in_range=True,unobstructed=True,
            unopposed=True)
        if heal is None or heal["spent_vp"]!=2:
            raise AssertionError("Native source-paid Medium Basic Heal missing")


def _foe(combat,policy,opponent):
    e=combat.e
    profile=(
        "B06-AT-03" if opponent=="soldier"
        else e.g3.sentry_profile("foe"))
    if profile not in ("B06-AT-03","B06-AT-02"):
        raise UnresolvedDecision("Only prepared Sentry and Soldier source hits")
    if not e.g1.melee_contact("foe","ally"):
        raise UnresolvedDecision("Sourced enemy and ally lost G1 melee contact")
    sequence=combat.declare("foe","ally",profiles=(profile,),
                            defenses=("take_hit",))
    kwargs={
        "attack_face":MELEE_FACE,
        "damage_face":SWORD_DIE,
        "wound_location_roll":8,
    }
    if profile=="B06-AT-02":
        kwargs["vigor_die"]=SENTRY_VIGOR_DIE
    if policy=="shelter_intercession":
        kwargs["medium_intercessor"]="medium"
    result=combat.resolve(sequence,0,**kwargs)
    if result["outcome"]!="hit" or result["damage"] is None:
        raise AssertionError("Source-authorized hit not actually delivered")


def _metrics(e):
    ally=e.actors["ally"]
    medium=e.actors["medium"]
    events=e.ledger
    def rows(kind):
        return [x for x in events if x["kind"]==kind]
    attacks=rows("g5_melee_resolved")
    delivered=rows("g4_damage_applied")
    own_heals=rows("g4_basic_heal_applied")
    steps=[x for x in rows("regeneration_step")
           if x["detail"]["actor"]=="ally"]
    # Never sum a free-standing fabricated packet into the balance metrics.
    if (len(attacks)!=ROUNDS or
            any(x["detail"]["target"]!="ally"
                or x["detail"]["outcome"]!="hit" for x in attacks)
            or len(delivered)!=ROUNDS
            or len(steps)!=ROUNDS
            or any(x["detail"]["recipient"]!="ally" for x in delivered)):
        raise AssertionError("Balance requires exactly two paid native enemy hits")
    return {
        "ally_hp":ally.hp, "ally_vigor":ally.vigor,
        "ally_wounds":len(ally.wounds),
        "priest_hp":medium.hp,"priest_vigor":medium.vigor,
        "priest_vp":[medium.vp_available,medium.vp_committed,medium.vp_spent],
        "ally_hp_regenerated":sum(x["detail"]["hp_restored"] for x in steps),
        "ally_regen_vigor_spent":sum(x["detail"]["throughput_spent"] for x in steps),
        "basic_heal_hp":sum(x["detail"]["hp_restored"] for x in own_heals),
        "basic_heal_vigor":sum(x["detail"]["vigor_restored"] for x in own_heals),
        "direct_vigor_prevented":sum(
            d["prevented"] for x in delivered
            for d in x["detail"]["vigor_details"]),
        "direct_vigor_applied":sum(
            d["applied"] for x in delivered
            for d in x["detail"]["vigor_details"]),
        "intercession_reactions":len(rows("b05_intercession_paid")),
        "paid_foe_attacks":len(attacks),
        "effect_establishments":len([
            x for x in rows("g3_effect_established")
            if x["detail"]["caster"]=="medium"]),
        "ap_committed_by_priest":sum(
            x["detail"]["ap_spent"] for x in rows("action_committed")
            if x["detail"]["actor"]=="medium"),
    }


def run_policy(*,opponent,level=3,policy,seed=0):
    """One two-round bounded paired-policy witness; not a winner."""
    _validate(opponent,level,policy,seed)
    combat,adapter=_scene(opponent,level,policy,seed)
    e=combat.e
    for round_no in range(1,ROUNDS+1):
        if e.round!=round_no:
            combat.bridge.begin_next_round()
        for actor in e.order:
            _start(combat,adapter,policy,actor)
            if actor=="medium":
                _medium(combat,adapter,policy,round_no)
            elif actor=="foe":
                _foe(combat,policy,opponent)
            combat.bridge.end_current_turn()
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots()):
        raise AssertionError("All native turns, round and attacks must resolve")
    e.check()
    metrics=_metrics(e)
    report={
        "version":"B04-B05-Medium-Life-Encounter-v0",
        "opponent":opponent,"level":level,"policy":policy,"seed":seed,
        "rounds_completed":e.round,
        "metrics":metrics,
        "source_ids":{a:e.actors[a].source.source_id for a in e.order},
        "source_digests":{a:e.actors[a].source.digest for a in e.order},
        "ledger":deepcopy(e.ledger),
        "full_encounter_certified":False,
        "independent_medium_focus_certified":False,
        "sampled_win_rate":None,"confidence_interval":None,
        "relative_intercession_cost_balanced":None,
        "policy_weighting":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,opponent,level=3,policy,seed=0):
    """Never certify a user-mutated or merely rehashed fabricated report."""
    _validate(opponent,level,policy,seed)
    expected=run_policy(opponent=opponent,level=level,policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Medium encounter report differs from native replay")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    """Comparable authored support choices; no inferred probabilities."""
    if type(seed) is not int or seed<0:
        raise ValueError("Source seed must be nonnegative integer")
    trials=[]
    for level in (1,2,3):
        for opponent in OPPONENTS:
            policies=("no_magic","guided","shelter","basic_heal")
            if level==3:
                policies+=("guided_intercession",)
                if opponent=="sentry_prepared":
                    policies+=("shelter_intercession",)
            for policy in policies:
                report=run_policy(opponent=opponent,level=level,
                                  policy=policy,seed=seed)
                trials.append({
                    "level":level,"opponent":opponent,"policy":policy,
                    "metrics":report["metrics"],
                    "source_digests":report["source_digests"],
                    "ledger_sha256":report["ledger_sha256"],
                })
    return {
        "version":"B04-B05-Medium-Life-Encounter-v0",
        "seed":seed,"policy_count":len(trials),
        "trials":trials,"source_replay_required":True,
        "fixed_policy_comparison":True,
        "observed_win_rate":None,"confidence_interval":None,
        "intercession_cost_accepted":False,
        "independent_medium_focus_certified":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opponent",choices=tuple(OPPONENTS))
    parser.add_argument("--level",type=int,choices=(1,2,3),default=3)
    parser.add_argument("--policy",choices=POLICIES)
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args()
    if bool(args.opponent)!=bool(args.policy):
        parser.error("Supply both --opponent and --policy, or neither")
    result=(run_policy(opponent=args.opponent,level=args.level,
                       policy=args.policy,seed=args.seed)
            if args.opponent else run_matrix(seed=args.seed))
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
