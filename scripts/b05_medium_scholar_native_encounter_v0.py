"""B04/B05 bounded source-native Medium Scholar Soldier verification.

Original Soldier G5 sword, G4 packets, G0 Step2, G1 grid and G3 Inward.
Fixed attack faces/choices, not opponent AI, sampled rates or full role proof.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_medium_scholar_native_inward_v0 import MediumScholarInward
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

POLICIES=("baseline","stone","guided","reroute",
          "overroute_body","overroute_guided")
HORIZON=3


def run_policy(*,level,policy,seed=0):
    if type(level) is not int or level not in (1,2,3):
        raise ValueError("Original Medium Scholar L1-3 only")
    if policy not in POLICIES or (policy.startswith("overroute") and level!=3):
        raise ValueError("Only authored profile/level policies")
    if type(seed) is not int or seed<0:
        raise ValueError("Deterministic nonnegative seed required")
    scholar=party_actor("S",level,"scholar","party",occupied=((2,2),))
    foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    e=Encounter([scholar,foe],{"scholar":40,"foe":30},
                seed=seed,scenario="B04-B05-Medium-Scholar-native-Inward",
                policy="three_fixed_soldier_sword_hits",
                objective="bounded_native_self_resistance_and_step_not_win_rate")
    GridMovement(e,width=7,height=7,scene_id="B05-medium-scholar-clear")
    SpellState(e)
    DamageState(e)
    adapter=MediumScholarInward(e,"scholar")
    combat=SourceMelee(e)
    if e.order!=("scholar","foe"):
        raise AssertionError("Authored fixed Initiative must be honored")
    e.begin_round()
    e.log("b05_medium_scholar_native_policy",level=level,policy=policy,
          seed=seed,rounds=HORIZON,source_digests={
              k:a.source.digest for k,a in e.actors.items()},
          damage_face=5,attack_face=12,wound_location_roll=8,
          target="scholar",defense="take_hit")
    for round_no in range(1,HORIZON+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            a=e.actors[who]
            # Exactly one authentic Step2 allocation per actor, after
            # real previous G4 damage, no fabricated bonus steps.
            throughput=max(0,a.regen+e.g3.regen_throughput(who)+
                           e.g4.toxins.modifier(who,"regen_throughput"))
            choice=RegenerationChoice(
                hp=min(max(0,a.hp_max-a.hp),a.vigor,throughput) if a.hp>0 else 0,
                cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))
            combat.bridge.start_next_turn(choice)
            if who=="scholar" and a.hp>0:
                if round_no==1:
                    if policy in ("stone","reroute","overroute_body"):
                        adapter.activate("MS-STONE-BODY-T1")
                    elif policy in ("guided","overroute_guided"):
                        adapter.activate("MS-GUIDED-REGEN-T1")
                    if policy=="overroute_body":
                        adapter.overroute(2)
                    elif policy=="overroute_guided":
                        adapter.overroute(2)
                if round_no==2 and policy=="reroute":
                    adapter.reroute("MS-GUIDED-REGEN-T1")
            elif who=="foe":
                if e.actors["scholar"].dead:
                    e.log("b05_scholar_target_dead",round_no=round_no)
                else:
                    if not e.g1.melee_contact("foe","scholar"):
                        raise AssertionError("Authored source sword lost contact")
                    seq=combat.declare("foe","scholar",
                                       profiles=("B06-AT-03",),
                                       defenses=("take_hit",))
                    outcome=combat.resolve(seq,0,attack_face=12,
                                           damage_face=5,
                                           wound_location_roll=8)
                    if outcome["outcome"]!="hit" or outcome["damage"] is None:
                        raise AssertionError("Genuine soldier expected confirmed hit")
            combat.bridge.end_current_turn()
    if e.current is not None or combat.pending_attack_slots():
        raise AssertionError("Unresolved paid G5 action or G0 turn")
    e.check()
    def events(kind):
        return [v for v in e.ledger if v["kind"]==kind]
    r={
        "version":"B04-B05-Medium-Scholar-Native-Inward-v0",
        "level":level,"policy":policy,"seed":seed,
        "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "metrics":{
            "scholar_hp":e.actors["scholar"].hp,
            "scholar_vigor":e.actors["scholar"].vigor,
            "vp":(scholar.vp_available,scholar.vp_committed,scholar.vp_spent),
            "attack_hits":len(events("g5_melee_resolved")),
            "damage_receipts":len(events("g4_damage_applied")),
            "regeneration_steps":len([v for v in events("regeneration_step")
                                     if v["detail"]["actor"]=="scholar"]),
            "native_hp_restored":sum(v["detail"]["hp_restored"] for v in
                events("regeneration_step") if v["detail"]["actor"]=="scholar"),
            "paid_projection_ap":sum(v["detail"]["ap_spent"] for v in
                events("action_committed") if v["detail"]["actor"]=="scholar"),
            "reroutes":len(events("b05_medium_scholar_rerouted")),
            "overroutes":len(events("b05_medium_scholar_overroute")),
            "active_effect":adapter._current_ident(),
            "active_steps":adapter.steps,
            "last_mp":scholar.mp_remaining,
        },
        "ledger":deepcopy(e.ledger),
        "native_self_profile_verified":True,
        "complete_opposed_encounter_certified":False,
        "full_focus_certified":False,"numerical_tuning_authorized":False,
        "statistical_win_rate":None,
    }
    r["ledger_sha256"]=canonical_digest(r["ledger"])
    return r


def attest_policy(report, *,level,policy,seed=0):
    expected=run_policy(level=level,policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Authenticated Medium Scholar native policy replay mismatch")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    rows=[]
    for level in (1,2,3):
        for policy in POLICIES:
            if policy.startswith("overroute") and level!=3:
                continue
            r=run_policy(level=level,policy=policy,seed=seed)
            rows.append({k:r[k] for k in ("level","policy","metrics",
                                         "source_digests","ledger_sha256")})
    report={"version":"B04-B05-Medium-Scholar-Native-Matrix-v0",
            "cases":rows,"case_count":len(rows),"seed":seed,
            "full_focus_certified":False,"numerical_tuning_authorized":False}
    report["audit_sha256"]=canonical_digest(report)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--level",type=int,choices=(1,2,3))
    p.add_argument("--policy",choices=POLICIES)
    p.add_argument("--seed",type=int,default=0)
    args=p.parse_args()
    if (args.level is None)!=(args.policy is None):
        p.error("Supply level and policy together")
    r=(run_policy(level=args.level,policy=args.policy,seed=args.seed)
       if args.level is not None else run_matrix(seed=args.seed))
    print(json.dumps(r,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
