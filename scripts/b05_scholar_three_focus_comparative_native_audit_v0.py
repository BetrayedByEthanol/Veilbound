"""B04/B05 Scholar three-Focus L1–3 source-native comparative audit v0.

Exact equal-source Soldier / HP resistance probes for F/S/T and bounded
individually certified M/L scene replays in separate evidence cohorts.
Never call a policy script's stale summary an independent simulation.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json

from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high_profile
from scripts.b05_medium_scholar_l1_l3_v0 import profile as medium_profile
from scripts.b05_low_scholar_l1_l3_v0 import profile as low_profile
from scripts.b05_medium_scholar_native_inward_v0 import MediumScholarInward
from scripts.b05_low_scholar_native_embodiment_v0 import LowScholarEmbodiment
from scripts.b05_medium_scholar_native_encounter_v0 import (
    run_policy as medium_scene, attest_policy as medium_attest,
)
from scripts.b05_low_scholar_native_encounter_v0 import (
    run_policy as low_scene, attest_policy as low_attest,
)
from scripts.b06_encounter_state_v0 import (
    ROOT, Encounter, RegenerationChoice, party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

LEVELS=(1,2,3)
FOCUSES=("High","Medium","Low")
ROLES={"High":"F","Medium":"S","Low":"T"}
PROFILES={"High":high_profile,"Medium":medium_profile,"Low":low_profile}
# Unlike the original M/L evidence sets (5 vs 6 d6), these exact face
# inputs, roster, turns and damage policy are identical for F, S and T.
MATCHED_POLICIES=("baseline","stone")
HORIZON=3
ATTACK_FACE=12
DAMAGE_FACE=5
WOUND_FACE=8
NATIVE_OTHER={"Medium":("baseline","stone","guided","reroute",
                         "overroute_body","overroute_guided"),
              "Low":("baseline","stone","guided","switch",
                     "stone_intensify","guided_intensify")}
SOURCE_PATHS=(
    "docs/rules/08-archetypes/scholar.md",
    "docs/rules/07-veil-magic/scholar-inward-embodiment-profiles-v0.md",
    "docs/rules/05-combat/action-categories-and-physical-tempo.md",
    "docs/rules/07-veil-magic/volition-points.md",
    "scripts/b05_high_scholar_fire_l1_l3_v0.py",
    "scripts/b05_medium_scholar_l1_l3_v0.py",
    "scripts/b05_low_scholar_l1_l3_v0.py",
    "scripts/b05_medium_scholar_native_inward_v0.py",
    "scripts/b05_low_scholar_native_embodiment_v0.py",
    "scripts/b05_medium_scholar_native_encounter_v0.py",
    "scripts/b05_low_scholar_native_encounter_v0.py",
    "scripts/b06_encounter_state_v0.py",
    "scripts/b06_spells_v0.py",
    "scripts/b06_damage_v0.py",
    "scripts/b06_soldier_sentry_g5_v0.py",
)
# These are price/authority declarations. Require exactly one match before
# publishing any fresh witness, and hash entire underlying bytes as well.
REQUIRED_BASIS={
    SOURCE_PATHS[0]:(
        "Low Scholar — Prepared Embodiment",
        "High Scholar — Projection through synthesis",
        "Medium Scholar — Routing and repertoire",
    ),
    SOURCE_PATHS[1]:(
        "**MS-STONE-BODY-T1**",
        "**MS-GUIDED-REGEN-T1**",
        "**LS-STONE-BODY-T1**",
        "**LS-GUIDED-REGEN-T1**",
    ),
    SOURCE_PATHS[2]:(
        "30 + 6 × (Level - 1)",
        "| **High — Projection** | 30 AP | 20 AP | 24 AP |",
        "| **Medium — Routing** | 24 AP | 24 AP | 24 AP |",
        "| **Low — Embodiment** | 20 AP | 30 AP | 24 AP |",
    ),
}
EXPECTED={
    "High":{"vp_rate":6,"physical_ap":30,"projection_ap":20,
            "regen":3,"known":(5,6,6),"guard_instrument":None},
    "Medium":{"vp_rate":4,"physical_ap":24,"projection_ap":24,
              "regen":3,"known":(4,5,5),"guard_instrument":"Sword"},
    "Low":{"vp_rate":2,"physical_ap":20,"projection_ap":30,
           "regen":5,"known":(3,4,4),"guard_instrument":"Sword"},
}


def verify_basis():
    """Bind actual rule and interpreter files, not incidental report labels."""
    basis={}
    for path in SOURCE_PATHS:
        raw=(ROOT/path).read_bytes()
        content=raw.decode("utf-8")
        for needle in REQUIRED_BASIS.get(path,()):
            if content.count(needle)!=1:
                raise AssertionError("Authored Scholar rule declaration drift: "
                                     +path+" => "+needle)
        basis[path]={"sha256":sha256(raw).hexdigest(),
                     "bytes":len(raw)}
    return basis


def row(focus,level):
    """Selected legal character, never normalized fictional Fighter/Scholar."""
    if focus not in FOCUSES or type(level) is not int or level not in LEVELS:
        raise ValueError("Only actual High/Medium/Low Scholar L1–3")
    p=PROFILES[focus](level)
    a=party_actor(ROLES[focus],level,"scholar","party",
                  occupied=((2,2),))
    ex=EXPECTED[focus]
    known=p["known_pillar_techniques"]
    expected={
        "hp_max":12,"vigor_max":12*level,"vp_max":ex["vp_rate"]*level,
        "ap_total":30+6*(level-1),
        "physical_ap":ex["physical_ap"],
        "projection_ap":ex["projection_ap"],
        "regen":ex["regen"],
        "guard_instrument":ex["guard_instrument"],
    }
    for key,value in expected.items():
        if getattr(a,key)!=value:
            raise AssertionError(f"{focus} L{level} G0 source mismatch: {key}")
    if (len(known)!=ex["known"][level-1]
            or dict(a.source.abilities)!=p["abilities"]
            or dict(a.source.training)!=p["weapon_training"]
            or a.hp_max!=p["hp_max"]
            or a.vigor_max!=p["vigor_max"]
            or a.vp_max!=p["vp_max"]
            or a.ap_total!=p["turn_ap"]
            or a.guard_instrument!=expected["guard_instrument"]
            or a.regen!=p["normal_regen_throughput"]
            or a.source.status!="STRUCTURAL_B05_ONLY"):
        raise AssertionError(f"{focus} structural sheet and native source mismatch")
    if focus=="High":
        if (p["guard_in_phase3"] is not None
                or "Dagger" not in p["starting_equipment_sp"]
                or any(n=="Dagger" and mode=="wielded"
                       for n,mode in a.source.equipment)):
            raise AssertionError("High F may not inherit a free active dagger Guard")
        prepared=None
        formulas=p["prepared_formula_capacity"]
        stone_reserve=p["stone_skin_committed_vp"]
        guided_prepared=False
        known_but_not_prepared=()
    elif focus=="Medium":
        prepared=None
        formulas=None
        stone_reserve=1
        guided_prepared=True   # individually known Inward; no preparation
        known_but_not_prepared=()
    else:
        prepared=list(p["prepared_techniques"])
        formulas=None
        stone_reserve=p["stone_committed_vp"]
        guided_prepared="Guided Regeneration" in prepared
        known_but_not_prepared=tuple(
            n for n in known if n not in prepared)
        if (p["prepared_capacity"]!=(2 if level==1 else 3)
                or len(prepared)!=p["prepared_capacity"]):
            raise AssertionError("Low prepared Arsenal not source-funded")
    vp=a.vp_max
    return {
        "focus":focus,"level":level,"actor_source_id":a.source.source_id,
        "actor_source_sha256":a.source.digest,
        "hp_max":a.hp_max,"vigor_max":a.vigor_max,"vp_max":vp,
        "vp_recovery_completed_six_hours":max(1,(vp+2)//4),
        "turn_ap":a.ap_total,"physical_ap":a.physical_ap,
        "projection_ap":a.projection_ap,
        "physical_tempo":a.ap_total//a.physical_ap,
        "projection_tempo":a.ap_total//a.projection_ap,
        "guard_capacity":a.guard_capacity,
        "guard_value":a.guard_value,
        "guard_instrument":a.guard_instrument,
        "dodge":p["first_dodge"],"initiative":a.initiative_bonus,
        "base_regen":a.regen,"movement_mp":p["movement_points"],
        "known_count":len(known),
        "individually_known":list(known),
        "prepared_arsenal":prepared,
        "unprepared_known":list(known_but_not_prepared),
        "prepared_formula_capacity":formulas,
        "stone_self_activation_ap":a.projection_ap,
        "stone_self_committed":stone_reserve,
        "guided_eligible_native":guided_prepared,
        "authoritative_native_outgoing_flame":
            focus=="High" and "Conjure Flame" in known,
        "physical_and_projection_same_turn":
            a.physical_ap+a.projection_ap<=a.ap_total,
        "only_structural_source_certified":True,
        "full_focus_certified":False,
    }


def matched_soldier(focus,level,policy,*,seed=0):
    """Identical native Soldier fixed melee and one legal self-defense mode.

    The High actor's G3 standalone Stone is usable; there is no authorized
    High Guided path or S/T outgoing offense in this matched v0. Compare
    the same attack packet, not the different old M/L authored dice.
    """
    if (focus not in FOCUSES or type(level) is not int or level not in LEVELS
            or policy not in MATCHED_POLICIES
            or type(seed) is not int or seed<0):
        raise ValueError("Non-authored Scholar matched-native cohort")
    source=row(focus,level)
    scholar=party_actor(ROLES[focus],level,"scholar","party",
                        occupied=((2,2),))
    soldier=enemy_actor("B06-EN-02","foe","enemy",
                        occupied=((3,2),))
    e=Encounter([scholar,soldier],{"scholar":40,"foe":30},
                seed=seed,scenario="B04-B05-Scholar-3Focus-matched-Soldier-v0",
                policy=policy,
                objective="matched_fixed_three_hit_defense_not_outgoing_CRs")
    GridMovement(e,width=7,height=7,scene_id="B05-scholar-comparable-clear")
    g3=SpellState(e)
    DamageState(e)
    adapter=(MediumScholarInward(e,"scholar") if focus=="Medium" else
             LowScholarEmbodiment(e,"scholar") if focus=="Low" else None)
    combat=SourceMelee(e)
    if e.order!=("scholar","foe"):
        raise AssertionError("Fixed common native Initiative order changed")
    e.begin_round()
    e.log("b05_scholar_matched_policy",focus=focus,level=level,policy=policy,
          source_digests={a.id:a.source.digest for a in e.actors.values()},
          attack_face=ATTACK_FACE,damage_face=DAMAGE_FACE,
          wound_location_roll=WOUND_FACE,defense="take_hit",
          horizon_rounds=HORIZON)
    for round_no in range(1,HORIZON+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for actor_id in e.order:
            a=e.actors[actor_id]
            throughput=max(0,a.regen+g3.regen_throughput(actor_id)
                           +e.g4.toxins.modifier(actor_id,"regen_throughput"))
            choice=RegenerationChoice(
                hp=min(max(0,a.hp_max-a.hp),a.vigor,throughput)
                    if a.hp>0 else 0,
                cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))
            combat.bridge.start_next_turn(choice)
            if actor_id=="scholar" and policy=="stone" and round_no==1:
                if focus=="High":
                    g3.cast_stone("scholar",tier=1)
                elif focus=="Medium":
                    adapter.activate("MS-STONE-BODY-T1")
                else:
                    adapter.activate("LS-STONE-BODY-T1")
            elif actor_id=="foe":
                if e.actors["scholar"].dead:
                    e.log("b05_scholar_matched_target_dead",round_no=round_no)
                else:
                    if not e.g1.melee_contact("foe","scholar"):
                        raise AssertionError("Original G1 melee contact lost")
                    attack=combat.declare("foe","scholar",
                        profiles=("B06-AT-03",),defenses=("take_hit",))
                    resolved=combat.resolve(attack,0,
                        attack_face=ATTACK_FACE,damage_face=DAMAGE_FACE,
                        wound_location_roll=WOUND_FACE)
                    if resolved["outcome"]!="hit":
                        raise AssertionError("Original fixed G5 expected legal sword hit")
            combat.bridge.end_current_turn()
    if e.current is not None or combat.pending_attack_slots():
        raise AssertionError("Unresolved source-native G5 or G0")
    e.check()
    def ev(kind):
        return [v for v in e.ledger if v["kind"]==kind]
    steps=[v for v in ev("regeneration_step")
           if v["detail"]["actor"]=="scholar"]
    actions=[v for v in ev("action_committed")
             if v["detail"]["actor"]=="scholar"]
    host=[v for v in g3.effects.values()
          if v.caster=="scholar" and v.kind=="Stone Skin"]
    if policy=="stone" and len(host)!=1:
        raise AssertionError("Expected one source-native retained Stone host")
    if policy=="baseline" and host:
        raise AssertionError("No free default Stone allowed")
    result={
        "version":"B04-B05-Scholar-Matched-Soldier-v0",
        "focus":focus,"level":level,"policy":policy,"seed":seed,
        "inputs":{"rounds":HORIZON,"enemy":"B06-EN-02",
                  "attack_face":ATTACK_FACE,"damage_face":DAMAGE_FACE,
                  "wound_location_roll":WOUND_FACE,"defense":"take_hit",
                  "source":source["actor_source_id"]},
        "sources":{"scholar":scholar.source.digest,
                   "foe":soldier.source.digest},
        "metrics":{
            "hp":scholar.hp,"vigor":scholar.vigor,
            "vp":[scholar.vp_available,scholar.vp_committed,scholar.vp_spent],
            "g5_hits":len(ev("g5_melee_resolved")),
            "g4_damage_receipts":len(ev("g4_damage_applied")),
            "true_self_steps":len(steps),
            "hp_restored":sum(v["detail"]["hp_restored"] for v in steps),
            "paid_projection_ap":sum(v["detail"]["ap_spent"] for v in actions),
            "paid_projection_actions":len(actions),
            "stone_r":host[0].resistance if host else 0,
            "stone_committed":host[0].committed if host else 0,
        },
        "ledger":deepcopy(e.ledger),
        "source_native_matched_defense_only":True,
        "no_outgoing_scholar_offense_certified":True,
        "full_focus_certified":False,
        "numerical_balance_tuning_authorized":False,
        "win_rate":None,
    }
    result["ledger_sha256"]=canonical_digest(result["ledger"])
    return result


def attest_matched(report,*,focus,level,policy,seed=0):
    expected=matched_soldier(focus,level,policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Matched Soldier native policy replay mismatch")
    return deepcopy(expected)


def _prior_cohort(focus,level,policy,seed):
    """Original M/L scene, not an apples-to-apples common damage result."""
    run,attest=(medium_scene,medium_attest) if focus=="Medium" else (
        low_scene,low_attest)
    source=run(level=level,policy=policy,seed=seed)
    attest(source,level=level,policy=policy,seed=seed)
    return {
        "focus":focus,"level":level,"policy":policy,
        "evidence_scope":"original_distinct_source_policy_not_matched",
        "original_face_damage":5 if focus=="Medium" else 6,
        "source_digests":source["source_digests"],
        "native_metrics":source["metrics"],
        "ledger_sha256":source["ledger_sha256"],
        "full_focus_certified":False,
    }


def run_audit(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative integer native-policy seed required")
    basis=verify_basis()
    rows=[row(focus,level) for level in LEVELS for focus in FOCUSES]
    matched=[matched_soldier(focus,level,policy,seed=seed)
             for level in LEVELS for policy in MATCHED_POLICIES
             for focus in FOCUSES]
    prior=[_prior_cohort(focus,level,policy,seed)
           for level in LEVELS for focus in ("Medium","Low")
           for policy in NATIVE_OTHER[focus]
           if not ((policy.startswith("overroute")
                    or policy.endswith("intensify")) and level<3)]
    matches=[{k:v for k,v in q.items()
              if k not in ("ledger",)}
             for q in matched]
    result={
        "version":"B04-B05-Scholar-Three-Focus-Comparative-Native-Audit-v0",
        "seed":seed,"source_basis":basis,"rows":rows,
        "native_matched":matches,"native_matched_count":len(matches),
        "prior_native_separate_cohorts":prior,"prior_cohort_count":len(prior),
        "caution":{
            "matched_attack_inputs_identical":True,
            "prior_medium_low_damage_faces_not_identical":True,
            "high_guide_vs_medium_low_no_equivalent_guided":True,
            "adaptive_attacker_policy":False,
            "native_three_focus_offense_matched":False,
            "ordinary_active_defense_scenarios_matched":False,
            "six_hour_restoration_native_encounter":False,
            "full_focus_certified":False,
            "numerical_balance_tuning_authorized":False,
            "statistical_win_rate":None,
        },
    }
    result["audit_sha256"]=canonical_digest(result)
    return result


def attest_audit(report,*,seed=0):
    expected=run_audit(seed=seed)
    if (not isinstance(report,dict) or report!=expected):
        raise AssertionError("Scholar comparative witness source or policy drift")
    return deepcopy(expected)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--focus",choices=FOCUSES)
    parser.add_argument("--level",type=int,choices=LEVELS)
    parser.add_argument("--policy",choices=MATCHED_POLICIES)
    args=parser.parse_args()
    if (args.focus is None)!=(args.level is None) or (
            args.focus is None)!=(args.policy is None):
        parser.error("Choose focus, level and policy together")
    result=(matched_soldier(args.focus,args.level,args.policy,seed=args.seed)
            if args.focus is not None else run_audit(seed=args.seed))
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
