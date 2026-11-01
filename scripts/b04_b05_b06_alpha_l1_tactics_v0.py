"""Alpha L1 tactical-choice bridge over native G0/G1/G2/G3/G4/G5.

Source-paid, predeclared player policies, real pre-roll G5 Guard/Dodge or
Take Hit, independent actor decisions and both withdrawal and unresolved
endings. This is NOT general tactical AI or independent human play.
"""
import argparse
from copy import deepcopy
import json

from scripts.b04_b05_b06_alpha_mixed_native_v0 import (
    scene, PARTY, FOCUSES, EXIT_STEPS, _validate as validate_source,
)
from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import _snapshot,canonical_digest

VERSION="B04-B05-B06-Alpha-L1-Tactical-Defenses-v0"
FIELDS=("priest_defense","soldier_d20","anointed","priest","gifted",
        "scholar","round_two")
OPTIONS={
    "priest_defense":("take_hit","guard","dodge"),
    "anointed":("invest","hold"),
    "priest":("chosen_rite","hold"),
    "gifted":("joy_flame","hold"),
    "scholar":("flame","hold"),
    "round_two":("withdraw","hold_position"),
}
# Author-identified branches are demonstrations, not a scripted assertion
# about actual player behavior or representative Soldier difficulty.
POLICIES={
    "protected_guard":{
        "priest_defense":"guard","soldier_d20":2,
        "anointed":"invest","priest":"chosen_rite",
        "gifted":"joy_flame","scholar":"flame","round_two":"withdraw"},
    "evasive_dodge":{
        "priest_defense":"dodge","soldier_d20":2,
        "anointed":"invest","priest":"chosen_rite",
        "gifted":"joy_flame","scholar":"hold","round_two":"withdraw"},
    "wounded_no_investment":{
        "priest_defense":"take_hit","soldier_d20":12,
        "anointed":"hold","priest":"chosen_rite",
        "gifted":"hold","scholar":"flame","round_two":"withdraw"},
    "wounded_with_step":{
        "priest_defense":"take_hit","soldier_d20":12,
        "anointed":"invest","priest":"chosen_rite",
        "gifted":"joy_flame","scholar":"flame","round_two":"withdraw"},
    "defend_position":{
        "priest_defense":"take_hit","soldier_d20":12,
        "anointed":"invest","priest":"hold",
        "gifted":"joy_flame","scholar":"hold","round_two":"hold_position"},
}


def validate_choice(choice):
    """Exact explicit choices, no silent defaults or unbounded reaction paths."""
    if type(choice) is not dict or set(choice)!=set(FIELDS):
        raise ValueError("Complete source-bound Alpha tactical declaration required")
    for key, options in OPTIONS.items():
        if type(choice[key]) is not str or choice[key] not in options:
            raise UnresolvedDecision("Unsupported Alpha player choice: "+key)
    die=choice["soldier_d20"]
    if type(die) is not int or not 1<=die<=19:
        raise UnresolvedDecision("Natural-20 confirmation not authored by Alpha v0")
    return deepcopy(choice)


def _soldier(combat, defense, face):
    """Native G5 defense assigned BEFORE face; dice paid only if actual hit."""
    e=combat.e
    if not e.g1.melee_contact("foe","priest"):
        raise UnresolvedDecision("Soldier requires actual source Priest contact")
    seq=combat.declare("foe","priest",profiles=("B06-AT-03",),
                       defenses=(defense,))
    assigned=e.ledger[seq["defenses"][0]]
    value=assigned["detail"]["defense_value"]
    bonus=combat._profile("foe","B06-AT-03")
    predicted=(face!=1 and (defense=="take_hit" or face+bonus>value))
    kwargs={"attack_face":face}
    if predicted:
        kwargs.update(damage_face=2,wound_location_roll=8)
    outcome=combat.resolve(seq,0,**kwargs)
    if outcome["outcome"]!=("hit" if predicted else "miss"):
        raise AssertionError("G5 resolution changed after defense commitment")
    return {"choice":defense,"face":face,"source_bonus":bonus,
            "assigned_defense":value,"guard_remaining":e.actors["priest"].guard_remaining,
            "dodge_pressure":e.actors["priest"].dodge_pressure,
            "outcome":outcome["outcome"],"action_index":outcome["action_index"]}


def run_choice(*,variant="A",seed=0,choices):
    """One bounded author-declared decision set, including incomplete battle."""
    validate_source(variant,seed)
    c=validate_choice(choices)
    combat,low,gifted,medium=scene(variant=variant,seed=seed)
    e=combat.e
    e.log("b04_b05_b06_alpha_tactical_predeclared",
          variant=variant,decisions=c,actor_source_digests={
              name:e.actors[name].source.digest for name in PARTY},
          externally_observed=False,party_author_fixed=True)
    before_hp=e.actors["priest"].hp
    fighter=None
    chosen_action={}
    pulse=False
    e_order=tuple(e.order)
    for actor in e_order:
        if actor=="priest" and medium.invest_action_index is not None:
            # The source only permits a beneficial pulse at an authentic
            # recipient Step after actual G5 harm, with living Vigor.
            target=e.actors["priest"]
            if target.hp>0 and target.hp<target.hp_max and target.vigor>0:
                medium.declare_pulse("priest",lesser=False,
                                     visible=True,unopposed=True)
        combat.bridge.start_next_turn(RegenerationChoice())
        if actor=="foe":
            fighter=_soldier(combat,c["priest_defense"],c["soldier_d20"])
        elif actor=="anointed":
            if c[actor]=="invest":
                result=medium.invest("priest",consenting=True)
                if result["ap_spent"]!=24:
                    raise AssertionError("Native medium General AP not paid")
                chosen_action[actor]="invest"
            else:
                chosen_action[actor]="hold"
        elif actor=="priest":
            if c[actor]=="chosen_rite":
                if low.cast_chosen("priest",chosen=True) is None:
                    raise AssertionError("Low Life G3 source Chosen Rite unavailable")
                chosen_action[actor]="chosen_rite"
            else:
                chosen_action[actor]="hold"
        elif actor=="gifted":
            if c[actor]=="joy_flame":
                gifted.establish("Joy")
                result=gifted.cast_flame("foe",tier=1,face=1,vigor_die=3,
                                         hand_available=True)
                if result["outcome"]!="automatic_miss":
                    raise AssertionError("High Gifted source paid miss not delivered")
                chosen_action[actor]="joy_flame"
            else:
                chosen_action[actor]="hold"
        elif actor=="scholar":
            if c[actor]=="flame":
                result=e.g3.cast_flame("scholar","foe",tier=1,face=1,
                                       vigor_die=3,defense="take_hit",
                                       hand_available=True)
                if result["outcome"]!="automatic_miss":
                    raise AssertionError("High Scholar source paid miss not delivered")
                chosen_action[actor]="flame"
            else:
                chosen_action[actor]="hold"
        combat.bridge.end_current_turn()
    if fighter is None:
        raise AssertionError("No native G5 Soldier attack")
    received_damage=e.actors["priest"].hp<before_hp
    pulse=any(x["kind"]=="g4_anointed_medium_returning_step_applied"
              for x in e.ledger)
    if pulse!=(c["anointed"]=="invest" and fighter["outcome"]=="hit"):
        raise AssertionError("Medium pulse must match paid Vessel and actual injury")
    # The first-round Priest's HP may be one higher due to the correctly
    # debited recipient-Vigor pulse; the G5 hit receipt is authoritative.
    round_one=_snapshot(e)
    e.log("b04_b05_b06_alpha_tactical_round_one",
          defense=fighter,source_actions=chosen_action,
          pulse_applied=pulse,actual_g5_injury=fighter["outcome"]=="hit")
    combat.bridge.begin_next_round()
    for actor in e_order:
        combat.bridge.start_next_turn(RegenerationChoice())
        if actor=="foe":
            # Natural-1 paid source miss, same live defender, each Round
            # reassigns its own defense; no reused previous Guard/Dodge.
            _soldier(combat,"take_hit",1)
        elif c["round_two"]=="withdraw":
            for delta in EXIT_STEPS[actor]:
                if not e.g1.step(actor,delta,cautious=True,
                                 responses=lambda eligible: ()):
                    raise UnresolvedDecision("Native source exit route was cancelled")
            combat.withdraw(actor)
        combat.bridge.end_current_turn()
    e.check()
    exits=[x for x in e.ledger if x["kind"]=="g5_terminal_exit"]
    if c["round_two"]=="withdraw":
        if (len(exits)!=len(PARTY) or
                {x["detail"]["actor"] for x in exits}!=set(PARTY) or
                any(e.actors[n].hp<=0 or e.actors[n].dead for n in PARTY)):
            raise AssertionError("Cannot attest all-Alpha tactical withdrawal")
        outcome="party_scene_withdrawal"
    else:
        if exits:
            raise AssertionError("Unresolved battle must not mint exit receipts")
        outcome="ongoing_engagement_not_terminal"
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots()
            or len([x for x in e.ledger if x["kind"]=="g5_melee_resolved"])!=2):
        raise AssertionError("No pending paid G0/G5 attacks at round end")
    def count(kind):
        return sum(x["kind"]==kind for x in e.ledger)
    if (count("b05_low_rite_established")!=int(c["priest"]=="chosen_rite")
            or count("b05_medium_anointed_investment_established")!=int(c["anointed"]=="invest")
            or count("b05_gifted_emotion_established")!=int(c["gifted"]=="joy_flame")
            or count("g3_flame_launched")!=(
                int(c["gifted"]=="joy_flame")+int(c["scholar"]=="flame"))
            or count("g4_anointed_medium_returning_step_applied")!=int(pulse)
            or count("g5_terminal_exit")!=(
                4 if outcome=="party_scene_withdrawal" else 0)):
        raise AssertionError("Alpha tactical source costs or action choices drifted")
    report={
        "version":VERSION,"variant":variant,"seed":seed,"choices":c,
        "party_focuses":dict(FOCUSES),
        "opponent":"B06-EN-02","opponent_level":3,
        "source_ids":{n:e.actors[n].source.source_id for n in e.actors},
        "source_digests":{n:e.actors[n].source.digest for n in e.actors},
        "priest_round_one_defense":fighter,"player_actions":chosen_action,
        "priest_injured_by_source_G5":fighter["outcome"]=="hit",
        "medium_pulse_applied":pulse,
        "round_one_state":round_one,"final_state":_snapshot(e),
        "vp_state":{n:{"max":e.actors[n].vp_max,
                       "available":e.actors[n].vp_available,
                       "committed":e.actors[n].vp_committed,
                       "spent":e.actors[n].vp_spent} for n in PARTY},
        "native_g5_attack_slots":count("g5_melee_resolved"),
        "native_exit_receipts":count("g5_terminal_exit"),
        "outcome":outcome,"rounds_completed":e.round,
        "ledger":deepcopy(e.ledger),
        "human_play_sessions":0,"independent_focus_certifications":0,
        "strict_mvp_gates_accepted":0,"sampled_win_rate":None,
        "complete_Alpha_L1_tactical_choice_engine":False,
        "representative_balance_calibrated":False,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def run_policy(*,policy,variant="A",seed=0):
    if type(policy) is not str or policy not in POLICIES:
        raise ValueError("Unknown author-verified Alpha L1 tactical policy")
    return run_choice(variant=variant,seed=seed,choices=POLICIES[policy])


def attest(report,*,choices,variant="A",seed=0):
    """Exact re-run rejects altered choices, defense pressure and endings."""
    expected=run_choice(variant=variant,seed=seed,choices=choices)
    if (type(report) is not dict or
            report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Alpha tactical witness diverges from native source")
    return deepcopy(expected)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--policy",choices=tuple(POLICIES),default="protected_guard")
    cli.add_argument("--variant",choices=("A","B"),default="A")
    cli.add_argument("--seed",type=int,default=0)
    a=cli.parse_args()
    report=run_policy(policy=a.policy,variant=a.variant,seed=a.seed)
    print(json.dumps({k:v for k,v in report.items() if k!="ledger"},
                     sort_keys=True,indent=2))


if __name__=="__main__":
    main()
