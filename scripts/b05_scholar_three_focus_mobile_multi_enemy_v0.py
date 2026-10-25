"""B04/B05 Scholar three-Focus mobile multi-enemy native integration v0.

Complete three-round witnesses reuse sourced G0–G5 melee and Fire, while a
separate actual double-Opportunity G0 probe expressly STOPS at missing G5
off-turn attack delivery. Committed capacity is not fictitious HP damage.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_scholar_native_sword_v0 import SWORD_IDS
from scripts.b05_scholar_thrown_flame_access_v0 import flame_access
from scripts.b05_medium_scholar_native_inward_v0 import MediumScholarInward
from scripts.b05_low_scholar_native_embodiment_v0 import LowScholarEmbodiment
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,Response,UnresolvedDecision,
    _fingerprint,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat,CoverSurface
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

ROLES={"High":"F","Medium":"S","Low":"T"}
LEVELS=(1,2,3)
POLICIES=("pursuit","cover_shift","stone_weave","opportunity_probe")
ROUNDS=3
SOLDIER_FACE={"alpha":(1,12,1),"beta":(12,1,12)}
SOLDIER_DIE=1
SCHOLAR_FACE=12
SCHOLAR_SWORD_DIE=4
SCHOLAR_FLAME_DIE=3
COVER_TIER=8
RULE_BASIS=(
    "scripts/b05_high_scholar_fire_l1_l3_v0.py",
    "scripts/b05_medium_scholar_l1_l3_v0.py",
    "scripts/b05_low_scholar_l1_l3_v0.py",
    "scripts/b05_scholar_native_sword_v0.py",
    "scripts/b05_scholar_thrown_flame_access_v0.py",
    "scripts/b05_medium_scholar_native_inward_v0.py",
    "scripts/b05_low_scholar_native_embodiment_v0.py",
    "scripts/b06_encounter_state_v0.py",
    "scripts/b06_movement_v0.py",
    "scripts/b06_ranged_v0.py",
    "scripts/b06_spells_v0.py",
    "scripts/b06_damage_v0.py",
    "scripts/b06_soldier_sentry_g5_v0.py",
    "scripts/b06_wound_continuation_v0.py",
)


def _validate(focus,level,policy,seed):
    if focus not in ROLES or type(level) is not int or level not in LEVELS:
        raise ValueError("Only original F/S/T Scholar L1–3")
    if policy not in POLICIES:
        raise ValueError("Unsupported authored three-Focus mobile policy")
    if type(seed) is not int or seed<0:
        raise ValueError("Source scene seed must be nonnegative integer")


def _setup(focus,level,policy,seed,*,probe=False):
    role=ROLES[focus]
    scholar=party_actor(role,level,"scholar","party",occupied=((2,2),))
    alpha_pos=(3,2) if probe else (4,2)
    beta_pos=(3,3) if probe else (4,4)
    alpha=enemy_actor("B06-EN-02","alpha","enemy",occupied=(alpha_pos,))
    beta=enemy_actor("B06-EN-02","beta","enemy",occupied=(beta_pos,))
    e=Encounter([scholar,alpha,beta],
                {"scholar":40,"alpha":30,"beta":20},
                seed=seed,scenario="B04-B05-Scholar-Mobile-Two-Soldier-v0",
                policy=policy,
                objective="source_native_mobile_evidence_not_terminal_certificate")
    GridMovement(e,width=8,height=7,scene_id="b05-mobile-two-soldiers")
    cover=((CoverSurface((2,3),COVER_TIER,(1,0)),)
           if policy=="cover_shift" else ())
    RangedCombat(e,cover=cover,scene_id="b05-changing-shooter-origin")
    SpellState(e)
    DamageState(e)
    adapter=(MediumScholarInward(e,"scholar") if focus=="Medium" else
             LowScholarEmbodiment(e,"scholar") if focus=="Low" else None)
    g5=SourceMelee(e)
    if e.order!=("scholar","alpha","beta"):
        raise AssertionError("Chosen source-native initiative reordered")
    e.begin_round()
    e.log("b05_mobile_policy",focus=focus,level=level,policy=policy,seed=seed,
          horizon=(1 if probe else ROUNDS),
          soldier_faces=SOLDIER_FACE,
          scholar_face=SCHOLAR_FACE,
          cover_tier=COVER_TIER if cover else 0,
          source_digests={name:a.source.digest for name,a in e.actors.items()})
    return e,g5,adapter


def _regen(e,who):
    a=e.actors[who]
    if who!="scholar":
        return RegenerationChoice()
    rate=max(0,a.regen+e.g3.regen_throughput(who)
             +e.g4.toxins.modifier(who,"regen_throughput"))
    return RegenerationChoice(
        hp=min(max(0,a.hp_max-a.hp),a.vigor,rate) if a.hp>0 else 0,
        cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))


def _move(e,who,delta,*,cautious=True):
    # Exact source-priced native G1 steps, including explicit Opportunity
    # decline under Cautious; no unsourced teleport or free MP.
    start=e.actors[who].occupied
    mp=e.actors[who].mp_remaining
    if not e.g1.step(who,delta,cautious=cautious,
                      responses=lambda eligible: ()):
        raise AssertionError("Authored G1 move was canceled")
    if e.actors[who].occupied==start or e.actors[who].mp_remaining>=mp:
        raise AssertionError("Native position or MP payment absent")


def _melee(g5,who,target,face,*,source_profile):
    e=g5.e
    if not e.g1.melee_contact(who,target):
        raise AssertionError("G1 native contact required for selected target")
    seq=g5.declare(who,target,profiles=(source_profile,),
                   defenses=("take_hit",))
    kwargs={"attack_face":face}
    if face!=1:
        kwargs.update(damage_face=(SCHOLAR_SWORD_DIE if who=="scholar"
                                   else SOLDIER_DIE),
                      wound_location_roll=8)
    hit=g5.resolve(seq,0,**kwargs)
    if hit["outcome"]!=("miss" if face==1 else "hit"):
        raise AssertionError("Declared G5 attack contradicted authored face")
    return hit


def _flame(e,target,*,expected):
    a=e.actors["scholar"]
    source=flame_access(a,wielded=e.g2.wielded["scholar"])
    before=(a.ap_remaining,a.vp_available,a.vp_spent)
    result=e.g3.cast_flame("scholar",target,tier=1,face=SCHOLAR_FACE,
                    vigor_die=SCHOLAR_FLAME_DIE,defense="take_hit",
                    hand_available=True,wound_location_roll=8)
    if (result["outcome"]!=expected
            or result["attack_total"]!=SCHOLAR_FACE+source["attack_bonus"]
            or result["vp_spent"]!=2
            or before[0]-a.ap_remaining!=source["action_ap"]
            or before[1]-a.vp_available!=2
            or a.vp_spent-before[2]!=2):
        raise AssertionError("Source-paid, genuinely delivered Flame mismatched")
    return result


def _report(e,focus,level,policy,seed,*,complete,blocker=None):
    if e.current is not None and complete:
        raise AssertionError("Full native case has an open turn")
    e.check()
    def ev(kind):
        return [v for v in e.ledger if v["kind"]==kind]
    steps=[v for v in ev("regeneration_step")
           if v["detail"].get("actor")=="scholar"]
    sword=[v for v in ev("g5_melee_resolved")
           if v["detail"].get("attacker")=="scholar"]
    foe_attacks=[v for v in ev("g5_melee_resolved")
                 if v["detail"].get("attacker") in ("alpha","beta")]
    flames=ev("g3_flame_launched")
    commitment=[v for v in ev("spontaneous_committed")
                if v["detail"].get("response_kind")=="opportunity"]
    paid=[v for v in ev("action_committed")
          if v["detail"].get("actor")=="scholar"]
    a=e.actors["scholar"]
    out={
        "version":"B04-B05-Scholar-Mobile-Multi-Enemy-v0",
        "focus":focus,"level":level,"policy":policy,"seed":seed,
        "native_complete_rounds":complete,
        "rule_basis":{p:_fingerprint(p) for p in RULE_BASIS},
        "actor_sources":{name:v.source.digest for name,v in e.actors.items()},
        "inputs":{"initial_scholar":[2,2],
                  "initial_alpha":[3,2] if blocker else [4,2],
                  "initial_beta":[3,3] if blocker else [4,4],
                  "roll_soldiers":SOLDIER_FACE,
                  "soldier_damage_die":SOLDIER_DIE,
                  "scholar_sword_die":SCHOLAR_SWORD_DIE,
                  "scholar_flame_die":SCHOLAR_FLAME_DIE,
                  "cover_tier":COVER_TIER if policy=="cover_shift" else 0},
        "metrics":{
            "rounds_finished":len(ev("round_end")),
            "scholar_step2":len(steps),
            "soldier_attacks":len(foe_attacks),
            "scholar_sword_attacks":len(sword),
            "flame_launches":len(flames),
            "flame_cover_impacts":sum(v["detail"]["outcome"]=="cover_impact"
                                      for v in flames),
            "flame_direct_g4":len([v for v in ev("g4_damage_applied")
                                     if v["detail"].get("cause")==
                                        "g3:thrown_flame"]),
            "vp": [a.vp_available,a.vp_committed,a.vp_spent],
            "physical_ap_paid":sum(v["detail"]["ap_spent"] for v in paid
                                    if v["detail"]["action_class"]=="physical"),
            "projection_ap_paid":sum(v["detail"]["ap_spent"] for v in paid
                                      if v["detail"]["action_class"]=="projection"),
            "scholar_hp":a.hp,"scholar_vigor":a.vigor,
            "hp_restored":sum(v["detail"]["hp_restored"] for v in steps),
            "positions":{name:[list(c) for c in actor.occupied]
                         for name,actor in e.actors.items()},
            "remaining_enemy_hp":{name:e.actors[name].hp
                                  for name in ("alpha","beta")},
            "enemy_target_orders":[v["detail"]["target"] for v in sword],
            "flame_target_orders":[v["detail"]["target"] for v in flames],
            "g1_move_receipts":len(ev("g1_movement_step")),
            "g1_opportunity_committed":len(commitment),
            "g1_opportunity_pending":len(ev("g1_movement_opportunity_pending")),
            "unresolved_g5_opportunities":len([v for v in ev("g45_unresolved_stop")
                     if v["detail"].get("category")=="unresolved_response"]),
        },
        "blocker":blocker,
        "ledger":deepcopy(e.ledger),
        "full_focus_certified":False,
        "completed_opportunity_damage_certified":False,
        "numerical_tuning_authorized":False,
        "win_rate":None,
    }
    out=json.loads(json.dumps(out,sort_keys=True,allow_nan=False))
    out["ledger_sha256"]=canonical_digest(out["ledger"])
    out["audit_sha256"]=canonical_digest(out)
    return out


def run_case(*,focus,level,policy,seed=0):
    _validate(focus,level,policy,seed)
    if policy=="opportunity_probe":
        # A live G1 departure with two genuine source-enemy Opportunity
        # responders. G0 pays both Responses in initiative order; the G1
        # callback correctly reports G5 damage delivery as unresolved.
        # Deliberately STOP; do not claim an ordinary turn or combat finish.
        e,g5,_=_setup(focus,level,policy,seed,probe=True)
        g5.bridge.start_next_turn(_regen(e,"scholar"))
        pre_hp={k:e.actors[k].hp for k in e.actors}
        selected=[]
        def choices(eligible):
            selected.extend(eligible)
            return tuple(Response(who,"opportunity",
                                  "B06-AT-03:offturn-unresolved")
                         for who in eligible)
        moved=e.g1.step("scholar",(0,1),responses=choices)
        if not moved or tuple(selected)!=("alpha","beta"):
            raise AssertionError("Exact two-source native Opportunity eligibility")
        committed=[v for v in e.ledger
                   if v["kind"]=="spontaneous_committed"]
        pending=[v for v in e.ledger
                 if v["kind"]=="g1_movement_opportunity_pending"]
        if (len(committed)!=2 or len(pending)!=2
                or any(e.actors[who].reaction_available
                       for who in ("alpha","beta"))
                or any(e.actors[who].opportunity_used!=1
                       for who in ("alpha","beta"))
                or pre_hp!={k:e.actors[k].hp for k in e.actors}):
            raise AssertionError("Native off-turn response capacity or HP forged")
        blocker=g5.bridge.mark_unresolved(
            "unresolved_response",
            source_reference="scripts/b06_movement_v0.py:G1-on_spontaneous",
            detail="G0 committed both Soldier Opportunity responses; G1 logs pending G5 attack, but no source-bound off-turn G5 attack/damage delivery exists")
        return _report(e,focus,level,policy,seed,
                       complete=False,blocker=blocker)

    e,g5,adapter=_setup(focus,level,policy,seed)
    for rnd in range(1,ROUNDS+1):
        if rnd>1:
            g5.bridge.begin_next_round()
        for who in e.order:
            actor=e.actors[who]
            g5.bridge.start_next_turn(_regen(e,who))
            if actor.hp>0 and not actor.dead:
                if who=="scholar":
                    if rnd==1:
                        if policy=="stone_weave":
                            if focus=="High":
                                host=e.g3.cast_stone("scholar",tier=1)
                            else:
                                ident=("MS-STONE-BODY-T1" if focus=="Medium"
                                       else "LS-STONE-BODY-T1")
                                host=adapter.activate(ident)
                            if host is None:
                                raise AssertionError("Authored paid Stone not established")
                        elif focus=="High":
                            _flame(e,"alpha",expected="direct_hit_resolved_G4")
                        else:
                            _move(e,"scholar",(1,0))
                            _melee(g5,"scholar","alpha",SCHOLAR_FACE,
                                   source_profile=SWORD_IDS[ROLES[focus]])
                    elif focus=="High":
                        if rnd==2:
                            _move(e,"scholar",(0,1))
                            _move(e,"scholar",(-1,0))
                        else:
                            _move(e,"scholar",(-1,0))
                        cover_hit=(policy=="cover_shift" and rnd==2)
                        _flame(e,"beta",expected=(
                            "cover_impact" if cover_hit else
                            "direct_hit_resolved_G4"))
                    else:
                        target=("alpha" if policy=="stone_weave" and rnd==2
                                else "beta" if rnd==2 or policy=="stone_weave"
                                else "alpha")
                        _melee(g5,"scholar",target,SCHOLAR_FACE,
                               source_profile=SWORD_IDS[ROLES[focus]])
                else:
                    if focus=="High":
                        _move(e,who,((-1,0) if who=="alpha" or rnd>1
                                     else (-1,-1)))
                    elif (policy=="stone_weave" and who=="alpha"
                          and rnd==1):
                        # S/T spent round one projecting Stone at (2,2).
                        # Alpha at (4,2) is two squares out: it must pay
                        # the actual G1 one-square approach to (3,2)
                        # BEFORE declaring its ordinary G5 melee hit.
                        _move(e,"alpha",(-1,0))
                    elif who=="beta" and rnd==1:
                        _move(e,"beta",(-1,-1))
                    # Two enemies make one independently funded native
                    # G5 attack per turn with source-chosen hit/miss dice.
                    face=SOLDIER_FACE[who][rnd-1]
                    _melee(g5,who,"scholar",face,source_profile="B06-AT-03")
            g5.bridge.end_current_turn()
    if (e.current is not None or g5.pending_attack_slots()
            or e.cursor!=len(e.order)):
        raise AssertionError("Unresolved G0/G5 after complete mobile scene")
    report=_report(e,focus,level,policy,seed,complete=True)
    m=report["metrics"]
    if (m["rounds_finished"]!=ROUNDS or m["scholar_step2"]!=ROUNDS
            or m["soldier_attacks"]!=2*ROUNDS
            or m["g1_opportunity_committed"]!=0
            or m["g1_opportunity_pending"]!=0):
        raise AssertionError("Invented opportunities or missing genuine three-round actors")
    return report


def attest_case(report,*,focus,level,policy,seed=0):
    expected=run_case(focus=focus,level=level,policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report.get("audit_sha256")!=canonical_digest({
                k:v for k,v in report.items() if k!="audit_sha256"})
            or report!=expected):
        raise AssertionError("Source-native multi-enemy replay mismatch")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative native matrix seed")
    rows=[run_case(focus=focus,level=level,policy=policy,seed=seed)
          for focus in ROLES for level in LEVELS for policy in POLICIES]
    result={
        "version":"B04-B05-Scholar-Mobile-Multi-Enemy-Matrix-v0",
        "seed":seed,"case_count":len(rows),
        "complete_cases":sum(r["native_complete_rounds"] for r in rows),
        "opportunity_boundary_probes":sum(
            r["policy"]=="opportunity_probe" for r in rows),
        "cases":[{k:v for k,v in r.items() if k!="ledger"} for r in rows],
        "rule_basis":{p:_fingerprint(p) for p in RULE_BASIS},
        "full_focus_certified":False,
        "opportunity_damage_certified":False,
        "numerical_tuning_authorized":False,
        "win_rate":None,
    }
    if (result["case_count"]!=36 or result["complete_cases"]!=27
            or result["opportunity_boundary_probes"]!=9):
        raise AssertionError("Unexpected source-native three-Focus cohort census")
    result=json.loads(json.dumps(result,sort_keys=True,allow_nan=False))
    result["audit_sha256"]=canonical_digest(result)
    return result


def attest_matrix(report,*,seed=0):
    expected=run_matrix(seed=seed)
    if (not isinstance(report,dict)
            or report.get("audit_sha256")!=canonical_digest({
                k:v for k,v in report.items() if k!="audit_sha256"})
            or report!=expected):
        raise AssertionError("Mobile multi-enemy matrix evidence/source drift")
    return deepcopy(expected)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--focus",choices=ROLES)
    p.add_argument("--level",type=int,choices=LEVELS)
    p.add_argument("--policy",choices=POLICIES)
    p.add_argument("--seed",type=int,default=0)
    args=p.parse_args()
    if sum(v is not None for v in (args.focus,args.level,args.policy)) not in (0,3):
        p.error("Provide focus, level, policy together")
    out=(run_case(focus=args.focus,level=args.level,
                  policy=args.policy,seed=args.seed)
         if args.focus is not None else run_matrix(seed=args.seed))
    print(json.dumps(out,sort_keys=True,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
