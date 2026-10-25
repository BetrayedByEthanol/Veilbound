"""B04/B05 Scholar three-Focus tactical and attrition verification v0.

Actual G0/G1/G2/G3/G4/G4.5/G5 four-round Soldier witnesses, not a new
combat executor, AI, win-rate model or independent Focus certificate.
All dice, resource allocations and policies are authored explicitly here.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_scholar_native_sword_v0 import SWORD_IDS
from scripts.b05_scholar_thrown_flame_access_v0 import flame_access
from scripts.b05_medium_scholar_native_inward_v0 import MediumScholarInward
from scripts.b05_low_scholar_native_embodiment_v0 import LowScholarEmbodiment
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, _fingerprint,
    party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat, CoverSurface
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

ROLES = {"High":"F", "Medium":"S", "Low":"T"}
LEVELS = (1,2,3)
COMMON_POLICIES = ("pressure","dodge","cover","stone")
PHYSICAL_POLICIES = ("guard","guided")
POLICIES = COMMON_POLICIES + PHYSICAL_POLICIES
ROUNDS = 4
# Fixed dice are input policy, not inferred GM tactics or Monte Carlo draws.
FLAME_FACE, FLAME_VIGOR_D8 = 12,3
SWORD_FACE, SWORD_D6 = 12,4
SOLDIER_FACE, SOLDIER_D6 = 8,1
WOUND_FACE, COVER_TIER = 8,8
SOURCE_BASIS = (
    "scripts/b05_high_scholar_fire_l1_l3_v0.py",
    "scripts/b05_medium_scholar_l1_l3_v0.py",
    "scripts/b05_low_scholar_l1_l3_v0.py",
    "scripts/b05_scholar_thrown_flame_access_v0.py",
    "scripts/b05_scholar_native_sword_v0.py",
    "scripts/b05_medium_scholar_native_inward_v0.py",
    "scripts/b05_low_scholar_native_embodiment_v0.py",
    "scripts/b06_encounter_state_v0.py",
    "scripts/b06_movement_v0.py",
    "scripts/b06_ranged_v0.py",
    "scripts/b06_spells_v0.py",
    "scripts/b06_damage_v0.py",
    "scripts/b06_wound_continuation_v0.py",
    "scripts/b06_soldier_sentry_g5_v0.py",
)


def _validate(focus,level,policy,seed):
    if focus not in ROLES or type(level) is not int or level not in LEVELS:
        raise ValueError("Exact source-selected Scholar Focus/level required")
    if (policy not in POLICIES
            or (policy in PHYSICAL_POLICIES and focus=="High")):
        raise ValueError("Guard/Guided is not authorized for this High sheet")
    if type(seed) is not int or seed<0:
        raise ValueError("Explicit nonnegative native scene seed required")


def _allocation(e,who):
    if who=="foe":
        # Soldier conserves Vigor in this exact non-optimal benchmark policy.
        return RegenerationChoice()
    a=e.actors[who]
    throughput=max(0,a.regen+e.g3.regen_throughput(who)
                   +e.g4.toxins.modifier(who,"regen_throughput"))
    return RegenerationChoice(
        hp=min(max(0,a.hp_max-a.hp),a.vigor,throughput)
           if a.hp>0 else 0,
        cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))


def _activate(e,focus,policy,adapter):
    if policy=="stone":
        if focus=="High":
            return e.g3.cast_stone("scholar",tier=1)
        return adapter.activate(
            "MS-STONE-BODY-T1" if focus=="Medium" else "LS-STONE-BODY-T1")
    if policy=="guided" and focus!="High":
        return adapter.activate(
            "MS-GUIDED-REGEN-T1" if focus=="Medium" else "LS-GUIDED-REGEN-T1")
    raise AssertionError("Activation must be source-authorized and scheduled")


def run_case(*,focus,level,policy,seed=0):
    """Replay a bounded real 4-round fight with choices fixed before rolls.

    Scholar uses only one eligible opening cast or sourced Sword; G5 handles
    each legal Soldier attack. Later Scholar physical attacks stop after the
    second hit to keep the same nonterminal Soldier alive for attrition.
    """
    _validate(focus,level,policy,seed)
    role=ROLES[focus]
    scholar=party_actor(role,level,"scholar","party",occupied=((2,2),))
    foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((4,2),))
    e=Encounter([scholar,foe],{"scholar":40,"foe":30},seed=seed,
        scenario="B04-B05-Scholar-Three-Focus-Tactical-Attrition-v0",
        policy=policy,
        objective="four_round_tactical_resource_witness_not_terminal_CR")
    GridMovement(e,width=8,height=7,scene_id="b05-scholar-four-round-tactics")
    cover=((CoverSurface((3,2),COVER_TIER,(1,0)),)
           if policy=="cover" else ())
    RangedCombat(e,cover=cover,scene_id="b05-scholar-tactical-lane")
    g3=SpellState(e)
    DamageState(e)
    adapter=(MediumScholarInward(e,"scholar") if focus=="Medium" else
             LowScholarEmbodiment(e,"scholar") if focus=="Low" else None)
    g5=SourceMelee(e)
    if e.order!=("scholar","foe"):
        raise AssertionError("Actual Scholar-first initiative changed")
    e.begin_round()
    e.log("b05_scholar_tactical_policy",focus=focus,level=level,
          policy=policy,seed=seed,rounds=ROUNDS,
          cover_tier=COVER_TIER if cover else 0,
          input_flame_face=FLAME_FACE,input_flame_vigor=FLAME_VIGOR_D8,
          input_sword_face=SWORD_FACE,input_sword_damage=SWORD_D6,
          input_soldier_face=SOLDIER_FACE,input_soldier_damage=SOLDIER_D6,
          source_digests={a.id:a.source.digest for a in e.actors.values()})
    rejected_cast=None
    for round_no in range(1,ROUNDS+1):
        if round_no>1:
            g5.bridge.begin_next_round()
        for who in e.order:
            actor=e.actors[who]
            g5.bridge.start_next_turn(_allocation(e,who))
            if who=="scholar" and actor.hp>0 and not actor.dead:
                if round_no==1:
                    if policy in ("stone","guided"):
                        host=_activate(e,focus,policy,adapter)
                        if host is None:
                            raise AssertionError("Required source-paid host interrupted")
                    elif focus=="High":
                        access=flame_access(scholar,wielded=e.g2.wielded["scholar"])
                        shot=g3.cast_flame("scholar","foe",tier=1,
                            face=FLAME_FACE,vigor_die=FLAME_VIGOR_D8,
                            defense="take_hit",hand_available=True)
                        expected=("cover_impact" if policy=="cover"
                                  else "direct_hit_resolved_G4")
                        if (shot["outcome"]!=expected or shot["vp_spent"]!=2
                                or shot["attack_total"]!=
                                   FLAME_FACE+access["attack_bonus"]):
                            raise AssertionError("Native G2 cover/G3 Flame evidence mismatch")
                    else:
                        # Only this one source-legal one-square approach.
                        e.g1.step("scholar",(1,0),responses=())
                        if not e.g1.melee_contact("scholar","foe"):
                            raise AssertionError("Moved Scholar lost G1 Sword contact")
                        seq=g5.declare("scholar","foe",
                            profiles=(SWORD_IDS[role],),defenses=("take_hit",))
                        hit=g5.resolve(seq,0,attack_face=SWORD_FACE,
                                       damage_face=SWORD_D6,
                                       wound_location_roll=WOUND_FACE)
                        if hit["outcome"]!="hit":
                            raise AssertionError("Fixed source Sword opening missed")
                else:
                    if round_no==2:
                        # Source preflight may emit a physical G2 preview but
                        # must never debit AP or VP for a threatened cast.
                        before=(actor.ap_remaining,actor.vp_available,
                                actor.vp_spent,actor.vp_committed)
                        try:
                            g3.cast_flame("scholar","foe",tier=1,
                                face=FLAME_FACE,vigor_die=FLAME_VIGOR_D8,
                                defense="take_hit",hand_available=True)
                        except UnresolvedDecision as issue:
                            rejected_cast=str(issue)
                        else:
                            raise AssertionError("No free threatened or unprepared Flame")
                        if before!=(actor.ap_remaining,actor.vp_available,
                                   actor.vp_spent,actor.vp_committed):
                            raise AssertionError("Illegal secondary Flame paid AP/VP")
                        e.log("b05_scholar_tactical_cast_rejected",caster="scholar",
                              round_no=round_no,reason=rejected_cast,
                              ap_vp_unchanged=True)
                    # Preserve Soldier as an actual conscious source across
                    # all four rounds: at most two normal Sword receipts.
                    sword_rounds=((2,3) if policy in ("stone","guided")
                                  else (2,))
                    if (focus!="High" and round_no in sword_rounds
                            and foe.hp>0 and not foe.dead):
                        if not e.g1.melee_contact("scholar","foe"):
                            raise AssertionError("Sword lost actual G1 contact")
                        seq=g5.declare("scholar","foe",
                            profiles=(SWORD_IDS[role],),defenses=("take_hit",))
                        hit=g5.resolve(seq,0,attack_face=SWORD_FACE,
                                       damage_face=SWORD_D6,
                                       wound_location_roll=WOUND_FACE)
                        if hit["outcome"]!="hit":
                            raise AssertionError("G5 Sword attrition hit not resolved")
            elif who=="foe" and foe.hp>0 and not scholar.dead:
                # Legal one-square approach only if native G1 contact absent.
                if not e.g1.melee_contact("foe","scholar"):
                    if round_no!=1:
                        raise AssertionError("Missing later-round contact")
                    e.g1.step("foe",(-1,0),responses=())
                if not e.g1.melee_contact("foe","scholar"):
                    raise AssertionError("Soldier did not achieve real melee contact")
                defense=("dodge" if policy=="dodge" else
                         "guard" if policy=="guard" else "take_hit")
                seq=g5.declare("foe","scholar",
                    profiles=("B06-AT-03",),defenses=(defense,))
                # A miss must not smuggle a damage die or fabricate G4 HP.
                miss=policy in ("dodge","guard")
                result=g5.resolve(seq,0,attack_face=SOLDIER_FACE,
                    **({} if miss else {"damage_face":SOLDIER_D6,
                                       "wound_location_roll":WOUND_FACE}))
                if result["outcome"]!=("miss" if miss else "hit"):
                    raise AssertionError("Source-defense outcome changed")
            g5.bridge.end_current_turn()
    if e.current is not None or g5.pending_attack_slots():
        raise AssertionError("Unresolved paid action or turn boundary")
    e.check()

    def ev(kind):
        return [x for x in e.ledger if x["kind"]==kind]

    soldier_rolls=[x for x in ev("g5_melee_resolved")
                   if x["detail"]["attacker"]=="foe"]
    sword_rolls=[x for x in ev("g5_melee_resolved")
                 if x["detail"]["attacker"]=="scholar"]
    flame=ev("g3_flame_launched")
    scholar_steps=[x for x in ev("regeneration_step")
                   if x["detail"]["actor"]=="scholar"]
    foe_steps=[x for x in ev("regeneration_step")
               if x["detail"]["actor"]=="foe"]
    soldier_hits=sum(x["detail"]["outcome"]=="hit" for x in soldier_rolls)
    sword_hits=sum(x["detail"]["outcome"]=="hit" for x in sword_rolls)
    expected_sword=(0 if focus=="High" else
                    2 if policy not in ("stone","guided") else 2)
    if (len(soldier_rolls)!=ROUNDS or len(scholar_steps)!=ROUNDS
            or len(foe_steps)!=ROUNDS or sword_hits!=expected_sword
            or len(flame)!=(1 if focus=="High" and
                           policy not in ("stone","guided") else 0)):
        raise AssertionError("Incomplete or fabricated four-round source receipts")
    if policy in ("dodge","guard") and soldier_hits:
        raise AssertionError("Protected native Scholar must evade fixed sword roll")
    if policy not in ("dodge","guard") and soldier_hits!=ROUNDS:
        raise AssertionError("Fixed Soldier native retaliation count changed")
    if rejected_cast is None:
        raise AssertionError("Missing round-two source-preflight refusal")

    effect=[x for x in ev("g3_effect_established")
            if x["detail"].get("caster")=="scholar"]
    endings=[x for x in ev("g3_effect_ended")
             if x["detail"].get("caster")=="scholar"]
    vp_spends=[x for x in ev("vp_transition")
               if x["detail"].get("actor")=="scholar"
               and x["detail"].get("mode")=="spent"]
    ap=[x for x in ev("action_committed")
        if x["detail"].get("actor")=="scholar"]
    g4_flame=[x for x in ev("g4_damage_applied")
              if x["detail"].get("cause")=="g3:thrown_flame"]
    g4_sword=[x for x in ev("g4_damage_applied")
              if x["detail"].get("cause")==
                 "source-profile:"+SWORD_IDS.get(role,"")]
    g4_soldier=[x for x in ev("g4_damage_applied")
                if x["detail"].get("cause")=="source-profile:B06-AT-03"]
    report={
        "version":"B04-B05-Scholar-Three-Focus-Tactical-Attrition-v0",
        "focus":focus,"level":level,"policy":policy,"seed":seed,
        "basis_sha256":{p:_fingerprint(p) for p in SOURCE_BASIS},
        "source_digests":{a.id:a.source.digest for a in e.actors.values()},
        "inputs":{"rounds":ROUNDS,"foe":"B06-EN-02",
                  "initial_scholar":[2,2],"initial_foe":[4,2],
                  "cover_tier":COVER_TIER if cover else 0,
                  "flame_face":FLAME_FACE,"flame_d8":FLAME_VIGOR_D8,
                  "sword_face":SWORD_FACE,"sword_d6":SWORD_D6,
                  "soldier_face":SOLDIER_FACE,"soldier_d6":SOLDIER_D6,
                  "wound_location":WOUND_FACE},
        "metrics":{
            "native_soldier_attacks":len(soldier_rolls),
            "native_soldier_hits":soldier_hits,
            "native_sword_attacks":len(sword_rolls),
            "native_sword_hits":sword_hits,
            "native_flame_launches":len(flame),
            "flame_cover_impacts":sum(x["detail"]["outcome"]=="cover_impact"
                                     for x in flame),
            "native_flame_g4":len(g4_flame),
            "native_sword_g4":len(g4_sword),
            "native_soldier_g4":len(g4_soldier),
            "source_ap_physical":sum(x["detail"]["ap_spent"] for x in ap
                                     if x["detail"]["action_class"]=="physical"),
            "source_ap_projection":sum(x["detail"]["ap_spent"] for x in ap
                                       if x["detail"]["action_class"]=="projection"),
            "source_vp_spent":sum(x["detail"]["points"] for x in vp_spends),
            "source_vp_state":[scholar.vp_available,scholar.vp_committed,
                               scholar.vp_spent],
            "effect_receipts":len(effect),"effect_ended_receipts":len(endings),
            "effect_source_committed":sum(x["detail"]["committed"]
                                          for x in effect),
            "regen_steps":len(scholar_steps),
            "hp_restored":sum(x["detail"]["hp_restored"] for x in scholar_steps),
            "scholar_hp":scholar.hp,"scholar_vigor":scholar.vigor,
            "scholar_dead":scholar.dead,
            "foe_hp":foe.hp,"foe_vigor":foe.vigor,"foe_dead":foe.dead,
            "r2_blocked_cast_reason":rejected_cast,
            "final_scholar_position":[list(v) for v in scholar.occupied],
            "final_foe_position":[list(v) for v in foe.occupied],
            "chosen_soldier_defense":(
                "dodge" if policy=="dodge" else
                "guard" if policy=="guard" else "take_hit"),
        },
        "ledger":deepcopy(e.ledger),
        "bounded_policy_only":True,
        "no_hypothetical_responses":True,
        "full_focus_certified":False,
        "numerical_tuning_authorized":False,
        "win_rate":None,
    }
    # Normalize ALL tuple/list containers before signing a persistent JSON.
    report=json.loads(json.dumps(report,sort_keys=True,allow_nan=False))
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    report["audit_sha256"]=canonical_digest(report)
    return report


def attest_case(report,*,focus,level,policy,seed=0):
    """Reject changed saved JSON even when a caller recomputes both hashes."""
    expected=run_case(focus=focus,level=level,policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report.get("audit_sha256")!=canonical_digest({
                k:v for k,v in report.items() if k!="audit_sha256"})
            or report!=expected):
        raise AssertionError("Native Scholar tactical resource witness mismatch")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Native matrix seed must be nonnegative integer")
    rows=[run_case(focus=focus,level=level,policy=policy,seed=seed)
          for focus in ROLES for level in LEVELS for policy in POLICIES
          if focus!="High" or policy in COMMON_POLICIES]
    result={
        "version":"B04-B05-Scholar-Tactical-Attrition-Matrix-v0",
        "seed":seed,"case_count":len(rows),
        "cases":[{k:v for k,v in case.items() if k!="ledger"} for case in rows],
        "source_basis":{p:_fingerprint(p) for p in SOURCE_BASIS},
        "full_focus_certified":False,"numerical_tuning_authorized":False,
        "statistical_win_rate":None,
    }
    if len(rows)!=48:
        raise AssertionError("Expected 9 common cohorts + 6 restricted policies")
    result=json.loads(json.dumps(result,sort_keys=True,allow_nan=False))
    result["audit_sha256"]=canonical_digest(result)
    return result


def attest_matrix(report,*,seed=0):
    expected=run_matrix(seed=seed)
    if (not isinstance(report,dict)
            or report.get("audit_sha256")!=canonical_digest({
                k:v for k,v in report.items() if k!="audit_sha256"})
            or report!=expected):
        raise AssertionError("Persisted Scholar tactical matrix source drift")
    return deepcopy(expected)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--focus",choices=ROLES)
    p.add_argument("--level",type=int,choices=LEVELS)
    p.add_argument("--policy",choices=POLICIES)
    p.add_argument("--seed",type=int,default=0)
    args=p.parse_args()
    if sum(x is not None for x in (args.focus,args.level,args.policy)) not in (0,3):
        p.error("Pass focus, level and policy together")
    out=(run_matrix(seed=args.seed) if args.focus is None
         else run_case(focus=args.focus,level=args.level,
                       policy=args.policy,seed=args.seed))
    print(json.dumps(out,indent=2,sort_keys=True,allow_nan=False))


if __name__=="__main__":
    main()
