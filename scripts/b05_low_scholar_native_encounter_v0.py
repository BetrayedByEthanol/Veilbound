"""B04/B05 bounded native Low Scholar Embodiment Soldier encounters v0.

G0 turns, G1 map, G3 host, G4 typed hit and genuine Step2, G5 sword;
not full tactical offense, balance tuning, noncombat or PS-03 certificate.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_low_scholar_native_embodiment_v0 import LowScholarEmbodiment
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

POLICIES=("baseline","stone","guided","switch",
          "stone_intensify","guided_intensify")
HORIZON=3


def run_policy(*,level,policy,seed=0):
    if type(level) is not int or level not in (1,2,3):
        raise ValueError("Original Low Scholar L1-3 only")
    if policy not in POLICIES or (
            policy.endswith("intensify") and level!=3):
        raise ValueError("Only level-authorized Low Scholar policies")
    if type(seed) is not int or seed<0:
        raise ValueError("Explicit nonnegative integer scene seed")
    scholar=party_actor("T",level,"scholar","party",occupied=((2,2),))
    foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    e=Encounter([scholar,foe],{"scholar":40,"foe":30},
                seed=seed,scenario="B04-B05-Low-Scholar-Embodiment-Soldier",
                policy="3-round-fixed-sword-and-explicit-step-allocation",
                objective="native-self-embodiment-vs-fixed-soldier-not-full-CR")
    GridMovement(e,width=7,height=7,scene_id="B05-low-scholar-clear")
    SpellState(e)
    DamageState(e)
    ls=LowScholarEmbodiment(e,"scholar")
    combat=SourceMelee(e)
    if e.order!=("scholar","foe"):
        raise AssertionError("Source-native fixed Initiative order not honored")
    e.begin_round()
    e.log("b05_low_scholar_policy",policy=policy,seed=seed,level=level,
          rounds=HORIZON,source_digests={
              k:a.source.digest for k,a in e.actors.items()},
          attack_face=12,damage_face=6,wound_location_roll=8,
          defense="take_hit")
    for round_no in range(1,HORIZON+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            a=e.actors[who]
            # The policy declares how many native Step2 points to allocate,
            # including a separately paid pending Deep Guided point. Only
            # actual G0/G4 Step2 can accept and realize this declaration.
            throughput=max(0,a.regen+e.g3.regen_throughput(who)+
                           e.g4.toxins.modifier(who,"regen_throughput"))
            if (who=="scholar" and ls.current_profile()=="LS-GUIDED-REGEN-T1"
                    and ls.intensified):
                throughput+=1
            choice=RegenerationChoice(
                hp=min(max(0,a.hp_max-a.hp),a.vigor,throughput)
                   if a.hp>0 else 0,
                cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))
            combat.bridge.start_next_turn(choice)
            if who=="scholar" and a.hp>0:
                if round_no==1:
                    if policy in ("stone","switch","stone_intensify"):
                        ls.activate("LS-STONE-BODY-T1")
                    elif policy in ("guided","guided_intensify"):
                        ls.activate("LS-GUIDED-REGEN-T1")
                    if policy.endswith("intensify"):
                        ls.intensify()
                if round_no==2 and policy=="switch":
                    # 0-AP release then a *second*, independently paid
                    # 30-AP Projection on the next eligible own turn.
                    ls.release()
                    ls.activate("LS-GUIDED-REGEN-T1")
            elif who=="foe":
                if e.actors["scholar"].dead:
                    e.log("b05_low_scholar_target_dead",round_no=round_no)
                else:
                    if not e.g1.melee_contact("foe","scholar"):
                        raise AssertionError("Authored sword lost G1 contact")
                    seq=combat.declare("foe","scholar",
                                       profiles=("B06-AT-03",),
                                       defenses=("take_hit",))
                    outcome=combat.resolve(seq,0,attack_face=12,
                                           damage_face=6,
                                           wound_location_roll=8)
                    if outcome["outcome"]!="hit" or outcome["damage"] is None:
                        raise AssertionError("Expected genuine confirmed G5 sword hit")
            combat.bridge.end_current_turn()
    if e.current is not None or combat.pending_attack_slots():
        raise AssertionError("Unresolved source G5 slot or G0 turn")
    e.check()
    def ev(kind):
        return [v for v in e.ledger if v["kind"]==kind]
    r={
        "version":"B04-B05-Low-Scholar-Native-Embodiment-v0",
        "level":level,"policy":policy,"seed":seed,
        "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "metrics":{
            "hp":scholar.hp,"vigor":scholar.vigor,
            "vp":(scholar.vp_available,scholar.vp_committed,scholar.vp_spent),
            "confirmed_attacks":len(ev("g5_melee_resolved")),
            "damage_receipts":len(ev("g4_damage_applied")),
            "actual_self_steps":len([
                v for v in ev("regeneration_step")
                if v["detail"]["actor"]=="scholar"]),
            "hp_restored":sum(v["detail"]["hp_restored"] for v in
                ev("regeneration_step") if v["detail"]["actor"]=="scholar"),
            "paid_projection_ap":sum(v["detail"]["ap_spent"] for v in
                ev("action_committed") if v["detail"]["actor"]=="scholar"),
            "activations":len(ev("b05_low_scholar_embodiment_active")),
            "releases":len([v for v in ev("g3_effect_ended")
                            if v["detail"]["caster"]=="scholar"]),
            "intensifications":len(ev("b05_low_scholar_intensified")),
            "stone_intensity_expirations":len(
                ev("b05_low_scholar_stone_intensity_expired")),
            "guided_intensity_consumptions":len(
                ev("b05_low_scholar_guided_intensity_consumed")),
            "active_profile":ls.current_profile(),
            "intensified":ls.intensified,
            "last_mp":scholar.mp_remaining,
        },
        "ledger":deepcopy(e.ledger),
        "native_bounded_embodiment_verified":True,
        "full_focus_certified":False,
        "complete_opposed_encounter_certified":False,
        "numerical_tuning_authorized":False,"win_rate":None,
    }
    r["ledger_sha256"]=canonical_digest(r["ledger"])
    return r


def attest_policy(report,*,level,policy,seed=0):
    expected=run_policy(level=level,policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Low Scholar report disagrees with native policy replay")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    rows=[]
    for level in (1,2,3):
        for policy in POLICIES:
            if policy.endswith("intensify") and level!=3:
                continue
            r=run_policy(level=level,policy=policy,seed=seed)
            rows.append({k:r[k] for k in
                         ("level","policy","source_digests",
                          "metrics","ledger_sha256")})
    report={"version":"B04-B05-Low-Scholar-Native-Matrix-v0",
            "seed":seed,"cases":rows,"case_count":len(rows),
            "full_focus_certified":False,"numerical_tuning_authorized":False}
    report["audit_sha256"]=canonical_digest(report)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level",type=int,choices=(1,2,3))
    parser.add_argument("--policy",choices=POLICIES)
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args()
    if (args.level is None)!=(args.policy is None):
        parser.error("Provide both level and policy")
    obj=(run_policy(level=args.level,policy=args.policy,seed=args.seed)
         if args.level is not None else run_matrix(seed=args.seed))
    print(json.dumps(obj,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
