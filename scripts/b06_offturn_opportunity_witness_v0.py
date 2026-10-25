"""B06 G5 off-turn Opportunity acceptance: two native Soldiers vs Scholar F/S/T.

Nine exact, completed source-ledger responses, distinct from the historical
B05 v0 unresolved Opportunity boundary probes. Not a new Focus certificate.
"""
import argparse
from copy import deepcopy
import json

from scripts.b06_offturn_opportunity_v0 import OpportunityChoice
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,party_actor,enemy_actor,_fingerprint,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

FOCUSES={"High":"F","Medium":"S","Low":"T"}
LEVELS=(1,2,3)
BASIS=(
    "scripts/b06_offturn_opportunity_v0.py",
    "scripts/b06_movement_v0.py",
    "scripts/b06_encounter_state_v0.py",
    "scripts/b06_soldier_sentry_g5_v0.py",
    "scripts/b06_wound_continuation_v0.py",
    "scripts/b06_damage_v0.py",
    "scripts/b05_high_scholar_fire_l1_l3_v0.py",
    "scripts/b05_medium_scholar_l1_l3_v0.py",
    "scripts/b05_low_scholar_l1_l3_v0.py",
)


def run_case(*,focus,level,seed=0):
    if focus not in FOCUSES or type(level) is not int or level not in LEVELS:
        raise ValueError("Exact authored Scholar role and L1–3 required")
    if type(seed) is not int or seed<0:
        raise ValueError("Native witness seed must be nonnegative integer")
    scholar=party_actor(FOCUSES[focus],level,"scholar","party",
                        occupied=((2,2),))
    alpha=enemy_actor("B06-EN-02","alpha","enemy",occupied=((3,2),))
    beta=enemy_actor("B06-EN-02","beta","enemy",occupied=((3,3),))
    e=Encounter([scholar,alpha,beta],{"scholar":40,"alpha":30,"beta":20},
                seed=seed,scenario="B06-G5-native-offturn-Soldier-pair-v0",
                policy="two_paid_G0_responses_before_G1_step",
                objective="bounded_native_Opportunity_attestation_not_terminal_CR")
    GridMovement(e,width=8,height=7,scene_id="b06-offturn-native-contact")
    RangedCombat(e)
    SpellState(e)
    DamageState(e)
    g5=SourceMelee(e)
    e.begin_round()
    g5.bridge.start_next_turn(RegenerationChoice())
    e.log("g5_offturn_source_policy",focus=focus,level=level,
          sources={a.id:a.source.digest for a in e.actors.values()},
          decisions={"alpha":"B06-AT-03 d20=1 miss",
                     "beta":"B06-AT-03 d20=12 d6=1"},
          source_basis={p:_fingerprint(p) for p in BASIS})
    before=(scholar.hp,scholar.mp_remaining,scholar.ap_remaining)
    moved=g5.opportunity_step("scholar",(0,1),decisions={
        "alpha":OpportunityChoice("B06-AT-03",1),
        "beta":OpportunityChoice("B06-AT-03",12,
                                 damage_face=1,wound_location_roll=8),
    })
    if not moved or scholar.occupied!=((2,3),):
        raise AssertionError("Real native G1 movement must continue after surviving hit")
    if (scholar.ap_remaining!=before[2]
            or scholar.mp_remaining!=before[1]-2
            or not scholar.hp<before[0]):
        raise AssertionError("Off-turn HP damage may not invent own-turn AP")
    post_step_mp=scholar.mp_remaining
    post_step_ap=scholar.ap_remaining
    events=lambda kind:[x for x in e.ledger if x["kind"]==kind]
    if (len(events("spontaneous_committed"))!=2
            or len(events("g5_opportunity_resolved"))!=2
            or len(events("g45_opportunity_attested_hit"))!=1
            or len(events("g1_movement_step"))!=1):
        raise AssertionError("G0/G1/G4.5 off-turn response census inconsistent")
    g5.bridge.end_current_turn()
    for actor in ("alpha","beta"):
        g5.bridge.start_next_turn(RegenerationChoice())
        # The tested response costs Reaction/Opportunity, not its own-turn
        # Attack Sequence AP or a magic once-per-turn penalty.
        g5.bridge.end_current_turn()
    e.check()
    report={
        "version":"B06-Native-Offturn-Opportunity-v0",
        "focus":focus,"level":level,"seed":seed,
        "basis_sha256":{p:_fingerprint(p) for p in BASIS},
        "source_digests":{a.id:a.source.digest for a in e.actors.values()},
        "metrics":{
            "resolved_offturn_responses":len(events("g5_opportunity_resolved")),
            "hit_receipts":len(events("g45_opportunity_attested_hit")),
            "native_rounds_complete":len(events("round_end")),
            "scholar_hp":scholar.hp,"scholar_mp_after":post_step_mp,
            "scholar_ap_after_response":post_step_ap,
            "scholar_position":[list(x) for x in scholar.occupied],
            "alpha_opportunity":alpha.opportunity_used,
            "beta_opportunity":beta.opportunity_used,
            "invented_offturn_ap":len([x for x in events("action_committed")
                    if x["detail"].get("actor") in ("alpha","beta")]),
        },
        "ledger":deepcopy(e.ledger),
        "full_focus_certified":False,"numerical_tuning_authorized":False,
    }
    report=json.loads(json.dumps(report,sort_keys=True,allow_nan=False))
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    report["audit_sha256"]=canonical_digest(report)
    return report


def attest_case(report,*,focus,level,seed=0):
    expected=run_case(focus=focus,level=level,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report.get("audit_sha256")!=canonical_digest({
                k:v for k,v in report.items() if k!="audit_sha256"})
            or report!=expected):
        raise AssertionError("Actual G0 source Opportunity replay mismatch")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Native matrix seed must be nonnegative integer")
    rows=[run_case(focus=focus,level=level,seed=seed)
          for focus in FOCUSES for level in LEVELS]
    result={
        "version":"B06-Offturn-Native-Soldier-Scholar-Matrix-v0",
        "case_count":len(rows),"seed":seed,
        "cases":[{k:v for k,v in r.items() if k!="ledger"} for r in rows],
        "source_basis":{p:_fingerprint(p) for p in BASIS},
        "independent_focus_certified":False,
    }
    if len(rows)!=9:
        raise AssertionError("Expected nine actual source roles")
    result["audit_sha256"]=canonical_digest(result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--focus",choices=FOCUSES)
    p.add_argument("--level",type=int,choices=LEVELS)
    p.add_argument("--seed",type=int,default=0)
    args=p.parse_args()
    if (args.focus is None)!=(args.level is None):
        p.error("Focus and level required together")
    result=(run_matrix(seed=args.seed) if args.focus is None else
            run_case(focus=args.focus,level=args.level,seed=args.seed))
    print(json.dumps(result,sort_keys=True,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
