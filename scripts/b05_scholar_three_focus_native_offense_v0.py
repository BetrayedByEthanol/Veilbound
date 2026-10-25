"""B04/B05 source-native three-Focus Thrown Flame versus one Soldier v0.

Same G0/G1/G2/G3/G4/G5 fixed scene, deliberate one ranged attack in
round 1, followed by physical Soldier advance/retaliation. Low L1 is
explicitly NOT prepared; no fabricated native player Sword substitute.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_scholar_thrown_flame_access_v0 import flame_access
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

FOCUSES={"High":"F","Medium":"S","Low":"T"}
LEVELS=(1,2,3)
POLICIES=("no_spell","flame_t1","flame_t2")
ROUNDS=2
FLAME_FACE=12
VIGOR_FACE=3
SWORD_FACE=12
SWORD_DAMAGE_FACE=4


def _choice(e,actor_id):
    a=e.actors[actor_id]
    # A deliberately fixed, legal allocation policy, not enemy AI.
    if actor_id=="foe":
        return RegenerationChoice()
    rate=max(0,a.regen+e.g3.regen_throughput(actor_id)+
             e.g4.toxins.modifier(actor_id,"regen_throughput"))
    return RegenerationChoice(
        hp=min(max(0,a.hp_max-a.hp),a.vigor,rate) if a.hp>0 else 0,
        cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))


def run_case(*,focus,level,policy,seed=0):
    if focus not in FOCUSES or type(level) is not int or level not in LEVELS:
        raise ValueError("Only source F/S/T levels 1–3")
    if policy not in POLICIES or (policy=="flame_t2" and level!=3):
        raise ValueError("T2 requires an actually eligible L3")
    if type(seed) is not int or seed<0:
        raise ValueError("Explicit nonnegative scene seed required")
    source=party_actor(FOCUSES[focus],level,"scholar","party",
                       occupied=((2,2),))
    foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((4,2),))
    e=Encounter([source,foe],{"scholar":40,"foe":30},seed=seed,
        scenario="B04-B05-Scholar-Three-Focus-Native-Flame-v0",
        policy="fixed_opening-and-one-G5-Soldier-retaliation-per-round",
        objective="bounded_native_offense_and_retaliation_not_terminal_CR")
    GridMovement(e,width=8,height=7,scene_id="b05-scholar-flame-lane")
    RangedCombat(e,scene_id="b05-scholar-flame-clear")
    g3=SpellState(e)
    DamageState(e)
    g5=SourceMelee(e)
    if e.order!=("scholar","foe"):
        raise AssertionError("Matched native initiative order changed")
    e.begin_round()
    e.log("b05_scholar_offense_policy",focus=focus,level=level,policy=policy,
          seed=seed,rounds=ROUNDS,flame_attack_face=FLAME_FACE,
          flame_vigor_die=VIGOR_FACE,sword_attack_face=SWORD_FACE,
          sword_damage_face=SWORD_DAMAGE_FACE,
          source_digests={a.id:a.source.digest for a in e.actors.values()})
    inaccessible=False
    for rnd in (1,2):
        if rnd>1:
            g5.bridge.begin_next_round()
        for actor_id in e.order:
            a=e.actors[actor_id]
            g5.bridge.start_next_turn(_choice(e,actor_id))
            if actor_id=="scholar" and rnd==1 and policy!="no_spell":
                if focus=="Low" and level==1:
                    # The chosen starting T sheet knows but DID NOT prepare
                    # Flame. Verify that *both* physical G2 preview and
                    # native G3 reject it without a turn/VP debit.
                    before=(a.ap_remaining,a.vp_available,len(e.ledger))
                    try:
                        g3.cast_flame("scholar","foe",tier=1,face=FLAME_FACE,
                                      vigor_die=VIGOR_FACE,
                                      hand_available=True)
                    except UnresolvedDecision:
                        inaccessible=True
                    else:
                        raise AssertionError("Unprepared L1 Low Flame was executed")
                    if (a.ap_remaining,a.vp_available,len(e.ledger))!=before:
                        raise AssertionError("Unprepared outward attempt charged resources")
                    e.log("b05_scholar_flame_unprepared",actor="scholar",
                          source_id="T",technique="Conjure Flame")
                else:
                    access=flame_access(a,wielded=e.g2.wielded["scholar"])
                    used=2 if policy=="flame_t2" else 1
                    result=g3.cast_flame("scholar","foe",tier=used,
                        face=FLAME_FACE,vigor_die=VIGOR_FACE,
                        defense="take_hit",hand_available=True)
                    if result["outcome"]!="direct_hit_resolved_G4":
                        raise AssertionError("Fixed source-legal G3 Flame not resolved")
                    if (result["attack_total"]!=FLAME_FACE+access["attack_bonus"]
                            or result["vp_spent"]!=2*used):
                        raise AssertionError("Flame attack or VP differed from source")
            elif actor_id=="foe":
                if rnd==1 and foe.hp>0:
                    e.g1.step("foe",(-1,0),responses=())
                if source.dead:
                    e.log("b05_scholar_offense_dead_target",round_no=rnd)
                elif foe.hp>0:
                    if not e.g1.melee_contact("foe","scholar"):
                        raise AssertionError("Soldier retaliation lost G1 contact")
                    seq=g5.declare("foe","scholar",profiles=("B06-AT-03",),
                                   defenses=("take_hit",))
                    resolved=g5.resolve(seq,0,attack_face=SWORD_FACE,
                        damage_face=SWORD_DAMAGE_FACE,
                        wound_location_roll=8)
                    if resolved["outcome"]!="hit":
                        raise AssertionError("Source Soldier fixed sword did not hit")
            g5.bridge.end_current_turn()
    e.check()
    if e.current is not None or g5.pending_attack_slots():
        raise AssertionError("Unresolved native scene obligations")
    def ev(kind):
        return [v for v in e.ledger if v["kind"]==kind]
    launched=ev("g3_flame_launched")
    damage=[v for v in ev("g4_damage_applied")
            if v["detail"]["cause"]=="g3:thrown_flame"]
    receipts=[v for v in ev("regeneration_step")
              if v["detail"]["actor"]=="scholar"]
    castable=policy!="no_spell" and not inaccessible
    if len(launched)!=int(castable) or len(damage)!=int(castable):
        raise AssertionError("Exact paid Flame/G4 count differs from source permission")
    spent=sum(v["detail"]["points"] for v in ev("vp_transition")
              if v["detail"]["actor"]=="scholar"
              and v["detail"]["mode"]=="spent")
    if spent!=(2*(2 if policy=="flame_t2" else 1) if castable else 0):
        raise AssertionError("Unexpected native Spent VP")
    report={
        "version":"B04-B05-Scholar-Three-Focus-Native-Offense-v0",
        "level":level,"focus":focus,"policy":policy,"seed":seed,
        "scope":"bounded_opening_cast_and_native_melee_retaliation",
        "inputs":{"rounds":ROUNDS,"enemy":"B06-EN-02",
                  "range_squares_at_cast":2,
                  "flame_face":FLAME_FACE,"flame_die":VIGOR_FACE,
                  "soldier_face":SWORD_FACE,"soldier_damage_face":SWORD_DAMAGE_FACE,
                  "soldier_defense":"take_hit"},
        "source_digests":{a.id:a.source.digest for a in e.actors.values()},
        "metrics":{
            "legal_flame_cast":castable,
            "blocked_unprepared_flame":inaccessible,
            "flame_launches":len(launched),
            "flame_g4_receipts":len(damage),
            "flame_source_bonus":(
                launched[0]["detail"]["source_attack_bonus"] if launched else None),
            "flame_ap_paid":sum(v["detail"]["ap_spent"]
                for v in ev("action_committed")
                if v["detail"]["actor"]=="scholar"),
            "flame_vp_spent":spent,
            "foe_hp_final":foe.hp,"foe_vigor_final":foe.vigor,
            "scholar_hp_final":source.hp,"scholar_vigor_final":source.vigor,
            "scholar_vp":[source.vp_available,source.vp_committed,source.vp_spent],
            "soldier_sword_hits":len([v for v in ev("g5_melee_resolved")
                                    if v["detail"]["attacker"]=="foe"]),
            "scholar_true_steps":len(receipts),
            "scholar_native_hp_restored":sum(v["detail"]["hp_restored"]
                                             for v in receipts),
        },
        "ledger":deepcopy(e.ledger),"full_focus_certified":False,
        "matched_source_offense_for_all_L1":False,
        "general_melee_attack_authorized_for_S_T":False,
        "numerical_tuning_authorized":False,"win_rate":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_case(report,*,focus,level,policy,seed=0):
    expected=run_case(focus=focus,level=level,policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Scholar native offensive policy replay mismatch")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Invalid matrix seed")
    cells=[run_case(focus=focus,level=level,policy=policy,seed=seed)
           for level in LEVELS for policy in POLICIES
           if policy!="flame_t2" or level==3
           for focus in FOCUSES]
    summaries=[{k:v for k,v in c.items() if k!="ledger"} for c in cells]
    out={"version":"B04-B05-Scholar-Offense-Matrix-v0","seed":seed,
         "cells":summaries,"count":len(summaries),
         "legal_cast_cells":sum(c["metrics"]["legal_flame_cast"] for c in cells),
         "l1_low_unprepared_blocked":sum(
             c["metrics"]["blocked_unprepared_flame"] for c in cells),
         "full_focus_certified":False,"numerical_tuning_authorized":False}
    out["audit_sha256"]=canonical_digest(out)
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--focus",choices=FOCUSES)
    p.add_argument("--level",type=int,choices=LEVELS)
    p.add_argument("--policy",choices=POLICIES)
    p.add_argument("--seed",type=int,default=0)
    args=p.parse_args()
    if len([x for x in (args.focus,args.level,args.policy) if x is not None]) not in (0,3):
        p.error("Select focus, level, policy together")
    result=(run_case(focus=args.focus,level=args.level,
                     policy=args.policy,seed=args.seed)
            if args.focus is not None else run_matrix(seed=args.seed))
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))


if __name__=="__main__":
    main()
