"""B04/B05 — Anointed Restoration three-Focus native G5 defensive witness v0.

One genuine source Soldier/Sentry paid melee hit, then one legal
High/Medium/Low Returning Step healing policy. No unsourced Anointed
offensive G5 profile, AI, combat victory, unrestricted Intrusion,
noncombat step cadence or independent Focus-role certificate.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_high_anointed_native_returning_step_v0 import HighAnointedRestoration
from scripts.b05_medium_anointed_native_returning_step_v0 import MediumAnointedRestoration
from scripts.b05_low_anointed_native_returning_step_v0 import LowAnointedRestoration
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

FOCI={"High":("AH",HighAnointedRestoration),
      "Medium":("AM",MediumAnointedRestoration),
      "Low":("AL",LowAnointedRestoration)}
OPPONENTS={"soldier":("B06-EN-02",None,"B06-AT-03"),
           "sentry_prepared":("B06-EN-01","prepared_start","B06-AT-02")}
POLICIES=("baseline","signature","lesser")
LEVELS=(1,2,3)
ATTACK_FACE=12
SWORD_D6=2
SENTRY_VIGOR_D6=1
ROUNDS=2


def _validate(focus,level,opponent,policy,seed):
    if focus not in FOCI or opponent not in OPPONENTS or policy not in POLICIES:
        raise ValueError("Unknown exact sourced Focus/opponent/policy")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only independently sourced L1–3 Anointed structural actors")
    if type(seed) is not int or seed<0:
        raise ValueError("Deterministic nonnegative seed required")


def scene(*,focus,level,opponent,policy,seed=0):
    _validate(focus,level,opponent,policy,seed)
    role,adapter=FOCI[focus]
    source_id,start,_=OPPONENTS[opponent]
    low=focus=="Low"
    caster=party_actor(role,level,"anointed","party",
                       occupied=((2,2),) if low else ((1,2),))
    foe=enemy_actor(source_id,"foe","enemy",start_state=start,occupied=((3,2),))
    actors=[caster,foe]
    if not low:
        actors.append(party_actor("F",level,"patient","party",occupied=((2,2),)))
    # High/Medium take an earlier setup turn. Low is the first actor
    # attacked in Round 1, so its genuine own Step follows the hit.
    scores=({"foe":30,"anointed":20} if low else
            {"anointed":30,"foe":24,"patient":18})
    e=Encounter(actors,scores,seed=seed,
                scenario=f"B04-B05-Anointed-Restoration-G5:{focus}:{opponent}",
                objective="one_paid_enemy_melee_and_one_existing_signature_step",
                policy="declared_attack_faces_declined_optional_responses")
    GridMovement(e,width=8,height=7,scene_id="B05-Anointed-clear-one-square")
    SpellState(e)
    DamageState(e)
    native=adapter(e,"anointed")
    combat=SourceMelee(e)
    e.begin_round()
    e.log("b05_anointed_defensive_policy",focus=focus,level=level,
          opponent=opponent,policy=policy,rounds=ROUNDS,
          attacker="foe",target="anointed" if low else "patient",
          attack_d20=ATTACK_FACE,sword_d6=SWORD_D6,
          sentry_vigor_d6=SENTRY_VIGOR_D6,optional_responses="decline_all",
          source_digests={ident:a.source.digest for ident,a in e.actors.items()})
    return combat,native


def _start(combat,actor):
    e=combat.e
    combat.bridge.start_next_turn(RegenerationChoice())
    if e.current!=actor or e.pending_regeneration is not None:
        raise AssertionError("G0 authentic Step / Initiative source mismatch")


def _one_enemy_hit(combat,opponent,recipient):
    e=combat.e
    _,_,profile=OPPONENTS[opponent]
    if profile!=("B06-AT-03" if opponent=="soldier" else e.g3.sentry_profile("foe")):
        raise AssertionError("Enemy must retain correct source attack state")
    if not e.g1.melee_contact("foe",recipient):
        raise UnresolvedDecision("Authentic G1 contact needed before enemy G5 sequence")
    seq=combat.declare("foe",recipient,profiles=(profile,),defenses=("take_hit",))
    params={"attack_face":ATTACK_FACE,"damage_face":SWORD_D6,
            "wound_location_roll":8}
    if opponent=="sentry_prepared":
        params["vigor_die"]=SENTRY_VIGOR_D6
    result=combat.resolve(seq,0,**params)
    if result["outcome"]!="hit" or result["damage"] is None:
        raise AssertionError("Expected one actual paid G5 HP/Vigor hit")
    return result


def _pulse(combat,native,focus,policy):
    if policy=="baseline":
        return
    lesser=policy=="lesser"
    if focus=="High":
        native.project("patient",lesser=lesser,visible=True,unopposed=True)
    elif focus=="Medium":
        native.declare_pulse("patient",lesser=lesser,visible=True,unopposed=True)
    else:
        native.declare_pulse(lesser=lesser)


def _metrics(e,native,focus):
    def events(kind):
        return [v for v in e.ledger if v["kind"]==kind]
    patient="anointed" if focus=="Low" else "patient"
    a=e.actors[patient]
    damage=events("g4_damage_applied")
    hit=events("g5_melee_resolved")
    if len(hit)!=1 or len(damage)!=1:
        raise AssertionError("Exactly one source G5 attack/G4 damage event expected")
    if hit[0]["detail"]["outcome"]!="hit" or not damage[0]["detail"]:
        raise AssertionError("Native G5 hit or G4 damaged patient not attested")
    signature_kind={"High":"g4_anointed_returning_step_applied",
                    "Medium":"g4_anointed_medium_returning_step_applied",
                    "Low":"g4_anointed_low_returning_step_applied"}[focus]
    sign=events(signature_kind)
    if len(sign)>1:
        raise AssertionError("Only one source Signature packet is eligible")
    regen=[v for v in events("regeneration_step")
           if v["detail"]["actor"]==patient]
    if len(regen)!=2:
        raise AssertionError("Exactly two genuine patient own Steps required")
    action=[v for v in events("action_committed")
            if v["detail"].get("actor")=="foe"]
    return {
        "recipient":patient,
        "recipient_hp":a.hp,
        "recipient_vigor":a.vigor,
        "recipient_hp_max":a.hp_max,
        "recipient_vigor_max":a.vigor_max,
        "recipient_dead":a.dead,
        "recipient_wound_count":len(a.wounds),
        "g5_hit_events":len(hit),
        "g4_damage_events":len(damage),
        "g0_enemy_paid_actions":len(action),
        "g0_recipient_regeneration_steps":len(regen),
        "signature_receipts":len(sign),
        "signature_hp_restored":sum(v["detail"]["hp_restored"] for v in sign),
        "signature_recipient_vigor_spent":sum(
            v["detail"]["recipient_vigor_spent"] for v in sign),
        "signature_destiny_spent":2-native.state.destiny,
        "anointed_destiny_remaining":native.state.destiny,
        "anointed_vp_available":e.actors["anointed"].vp_available,
        "anointed_vp_committed":e.actors["anointed"].vp_committed,
        "anointed_vp_spent":e.actors["anointed"].vp_spent,
        "anointed_ap_total":e.actors["anointed"].ap_total,
    }


def run_policy(*,focus,level,opponent="soldier",policy="signature",seed=0):
    """Two complete G0 rounds; no terminal win-rate or unsourced actions."""
    _validate(focus,level,opponent,policy,seed)
    combat,native=scene(focus=focus,level=level,opponent=opponent,
                        policy=policy,seed=seed)
    e=combat.e
    patient="anointed" if focus=="Low" else "patient"
    for round_no in range(1,ROUNDS+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            # The pulse must be declared for exactly the imminent native
            # recipient G0 Step after the actual enemy hit (not before).
            if round_no==1 and who==patient and focus!="High":
                _pulse(combat,native,focus,policy)
            _start(combat,who)
            if who=="anointed":
                if focus=="Medium" and round_no==1 and policy!="baseline":
                    native.invest(patient,consenting=True)
                if focus=="High" and round_no==2:
                    _pulse(combat,native,focus,policy)
            elif who=="foe" and round_no==1:
                _one_enemy_hit(combat,opponent,patient)
            combat.bridge.end_current_turn()
    if e.current is not None or e.cursor!=len(e.order) or combat.pending_attack_slots():
        raise AssertionError("Pending G0 turn or paid G5 attack at the end of witness")
    e.check()
    report={
        "version":"B04-B05-Anointed-G5-Defensive-Witness-v0",
        "focus":focus,"level":level,"opponent":opponent,
        "policy":policy,"seed":seed,
        "metrics":_metrics(e,native,focus),
        "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "ledger":deepcopy(e.ledger),
        "independent_focus_certified":False,
        "representative_play_certified":False,
        "sampled_win_rate":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,focus,level,opponent="soldier",policy="signature",seed=0):
    """Recompute the entire deterministic native timeline, not only its digest."""
    expected=run_policy(focus=focus,level=level,opponent=opponent,
                        policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Altered or unauthentic Anointed G0/G5 receipt/policy")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    reports=[]
    for focus in FOCI:
        for level in LEVELS:
            for opponent in OPPONENTS:
                for policy in POLICIES:
                    reports.append(run_policy(
                        focus=focus,level=level,opponent=opponent,
                        policy=policy,seed=seed))
    return reports


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--focus",choices=tuple(FOCI))
    parser.add_argument("--level",type=int,choices=LEVELS,default=3)
    parser.add_argument("--opponent",choices=tuple(OPPONENTS),default="soldier")
    parser.add_argument("--policy",choices=POLICIES,default="signature")
    parser.add_argument("--matrix",action="store_true")
    args=parser.parse_args()
    if args.matrix:
        reports=run_matrix(seed=args.seed)
        print(json.dumps({"witnesses":len(reports),"metrics":[
            {k:r[k] for k in ("focus","level","opponent","policy")}
            |r["metrics"] for r in reports]},indent=2))
    else:
        print(json.dumps(run_policy(focus=args.focus or "High",
                   level=args.level,opponent=args.opponent,policy=args.policy,
                   seed=args.seed),indent=2))


if __name__=="__main__":
    main()
