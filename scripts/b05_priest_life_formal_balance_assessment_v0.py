"""B04/B05 Formal Priest Life Focus Balance Assessment v0.

Consolidate the three independently source-native matrix runners, preserve
local baselines and endpoint exposure differences, and record deterministic
observations rather than invented cross-Focus weights or win probabilities.
No AP/VP/damage tuning. Full assessed reports can be replay-attested.
"""
import argparse
from collections import defaultdict
from copy import deepcopy
import json

from scripts.b05_three_focus_life_comparison_v0 import run_matrix as self_matrix
from scripts.b05_three_focus_life_extended_attrition_v0 import run_matrix as attrition_matrix
from scripts.b05_priest_life_multi_recipient_stress_v0 import run_matrix as support_matrix
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

COUNTS={"matched_self":64,"extended_attrition":912,"multi_recipient":408}
HISTORICAL_ALLY_COUNT=36
ROLES=("H","M","A","B")
FOCI={"H":"High","M":"Medium","A":"Low","B":"Low"}
SOURCES={
    "matched_self":"scripts/b05_three_focus_life_comparison_v0.py",
    "extended_attrition":"scripts/b05_three_focus_life_extended_attrition_v0.py",
    "multi_recipient":"scripts/b05_priest_life_multi_recipient_stress_v0.py",
}
KEYS={
    "matched_self":("role","level","opponent","policy"),
    "extended_attrition":(
        "role","level","opponent","horizon","pressure","tactic","policy"),
    "multi_recipient":(
        "role","level","opponent","pattern","pressure","policy"),
}
BASE_KEYS={
    "matched_self":("role","level","opponent"),
    "extended_attrition":(
        "role","level","opponent","horizon","pressure","tactic"),
    "multi_recipient":(
        "role","level","opponent","pattern","pressure"),
}
ROWS={"matched_self":"matched_self","extended_attrition":"cells",
      "multi_recipient":"cases"}
DIGEST_LABELS={"matched_self":"audit_sha256",
               "extended_attrition":"audit_sha256",
               "multi_recipient":"audit_sha256"}
POLICIES={
    "H":{
        "identity":"High Priest Life",
        "supported":"20-AP prepared Prayers; two distinct maintained effects at L3; real paid Basic Heal",
        "limitation":"prepared/invocation choice and available VP, not a free universal spell pool",
        "next_gate":"Compare different preparation loadouts and recurring healer opportunity costs"},
    "M":{
        "identity":"Medium Priest Life",
        "supported":"24-AP maintained Consecration and 24-AP paid reassignment; L3 2-Spent-VP Reaction Intercessions",
        "limitation":"one live host; other-beneficiary, packet/Step-2, line, VP and Reaction gates",
        "next_gate":"Vary Initiative and simultaneous threats to measure intercession opportunity cost"},
    "A":{
        "identity":"Low Priest Guided A",
        "supported":"self Chosen Guided, L3 Held Renewal, legal hand-free 30-AP external Basic Heal",
        "limitation":"Chosen host is self-only and shares limited VP with separately paid healing",
        "next_gate":"Test mixed self attrition and ally healing under genuinely scarce VP"},
    "B":{
        "identity":"Low Priest Shelter B",
        "supported":"self Chosen Shelter and L3 own-packet Vital Interposition with finite budget",
        "limitation":"mace and shield occupy both hands; no verified external Basic Heal transition",
        "next_gate":"Author and verify an actual equipment-switch path before assessing external Heal access"},
}
GAPS=(
    ("G1","HIGH","stochastic_and_threat_coverage",
     "Only authored fixed attack/damage dice, one source foe and limited horizons",
     "Vary attack/defense rolls, enemy count, attack targets, wounds and policy distribution before probabilistic claims"),
    ("G2","HIGH","focus_access_asymmetry",
     "H/M and A/B do not share legal spell targeting, host counts or equipment states",
     "Compare legal party objectives rather than normalize all Focuses to identical spell repertoires"),
    ("G3","HIGH","dynamic_opponent_and_turn_order",
     "Fixed Initiative, Take Hit or bounded Guard/Dodge, no adaptive enemy AI or contested magic",
     "Verify alternating initiative, active foe tactics and contested delivery under true native authorities"),
    ("G4","MEDIUM","medium_reaction_opportunity",
     "Native Intercession receipts certify legality but not the value of foregone other Reactions",
     "Measure simultaneously eligible reaction windows and real alternatives under the same source scene"),
    ("G5","MEDIUM","low_B_equipment_transition",
     "Source B lacks a legal free hand while wielding shield and mace",
     "Test a source-authored action-priced equipment transition, if designed, before considering repertoire changes"),
    ("G6","MEDIUM","long_horizon_recovery",
     "The 4/8-round scenes do not simulate a representative adventuring day or six-hour recovery",
     "Test multiple encounters, VP recovery, wound maintenance and sustained resource costs"),
)
DECISION="retain_existing_numbers_pending_targeted_evidence"


def _seal(value):
    if not isinstance(value,dict) or "audit_sha256" not in value:
        raise AssertionError("Missing native source matrix and audit digest")
    expected=canonical_digest({k:v for k,v in value.items()
                               if k!="audit_sha256"})
    if value["audit_sha256"]!=expected:
        raise AssertionError("Native matrix digest does not match contents")


def _key(row,names):
    return tuple(row[k] for k in names)


def _validate_evidence(evidence):
    """Fail closed against incomplete/conflicting matrices and local baselines.

    This is a *structural* check of supplied matrices, not proof of their
    origin; final attestation must replay native runners independently.
    """
    if not isinstance(evidence,dict) or set(evidence)!=set(COUNTS):
        raise AssertionError("Need exactly the three native evidence strata")
    roles_sources={}
    opponents_sources={}
    for stratum,expected_count in COUNTS.items():
        matrix=evidence[stratum]
        _seal(matrix)
        if matrix.get("seed") is None or type(matrix["seed"]) is not int:
            raise AssertionError("Signed native integer seed needed")
        cells=matrix[ROWS[stratum]]
        if len(cells)!=expected_count:
            raise AssertionError("Missing or duplicate native evidence cells")
        n_field={"matched_self":"matched_self_cells",
                 "extended_attrition":"cell_count",
                 "multi_recipient":"case_count"}[stratum]
        if matrix[n_field]!=expected_count:
            raise AssertionError("Source matrix count mismatch")
        if matrix.get("focus_ranking","absent") is not None and (
                "focus_ranking" in matrix):
            raise AssertionError("Native matrix must never rank Focuses")
        identity=set()
        baselines={}
        for row in cells:
            key=_key(row,KEYS[stratum])
            if key in identity:
                raise AssertionError("Duplicate native policy/scene identity")
            identity.add(key)
            role=row["role"]
            if role not in ROLES or row["focus"]!=FOCI[role]:
                raise AssertionError("Incorrect source Focus role")
            if type(row["level"]) is not int or row["level"] not in (1,2,3):
                raise AssertionError("Invalid source level")
            if (type(row["ledger_sha256"]) is not str
                    or len(row["ledger_sha256"])!=64):
                raise AssertionError("Missing source ledger receipt digest")
            src=row["source_digests"]
            priest_key="priest"
            if priest_key not in src or "foe" not in src:
                raise AssertionError("No genuine Priest or foe source digest")
            k=(role,row["level"])
            if k in roles_sources and roles_sources[k]!=src[priest_key]:
                raise AssertionError("Priest build digest differs across strata")
            roles_sources[k]=src[priest_key]
            enemy=(row["opponent"],src["foe"])
            if enemy[0] in opponents_sources and opponents_sources[enemy[0]]!=enemy[1]:
                raise AssertionError("Enemy identity differs across strata")
            opponents_sources[enemy[0]]=enemy[1]
            if row["policy"]=="baseline":
                bk=_key(row,BASE_KEYS[stratum])
                if bk in baselines:
                    raise AssertionError("Duplicate baseline for scenario")
                baselines[bk]=row
            if not isinstance(row.get("delta_vs_same_source_baseline"),dict):
                raise AssertionError("Native local baseline delta missing")
        for row in cells:
            bk=_key(row,BASE_KEYS[stratum])
            if bk not in baselines:
                raise AssertionError("Missing same-source baseline")
            base=baselines[bk]
            if row["source_digests"]!=base["source_digests"]:
                raise AssertionError("Source mismatch inside local comparison")
            if row["policy"]=="baseline" and any(
                    value!=0 for value in row["delta_vs_same_source_baseline"].values()):
                raise AssertionError("Baseline is not zero")
        if stratum=="matched_self":
            if (matrix["existing_same_F_ally_cells"]!=HISTORICAL_ALLY_COUNT
                    or len(matrix["high_medium_same_ally"])!=HISTORICAL_ALLY_COUNT
                    or matrix["low_ally_comparison_supported"] is not False):
                raise AssertionError("Historical ally context cannot become matched Low evidence")
        if stratum=="extended_attrition" and (
                matrix["only_actual_rounds_counted"] is not True
                or matrix["intercession_and_external_Low_access_matched"] is not False):
            raise AssertionError("Attrition exposure boundary changed")
        if stratum=="multi_recipient" and (
                matrix["low_A_external_basic_heal"] is not True
                or matrix["low_B_external_basic_heal"] is not False
                or matrix["low_chosen_external_targeting"] is not False):
            raise AssertionError("Source legal Life repertoire boundary changed")
    if len({e["seed"] for e in evidence.values()})!=1:
        raise AssertionError("Do not silently combine different deterministic seeds")
    if len(roles_sources)!=12 or len(opponents_sources)!=2:
        raise AssertionError("Missing a source level or opponent witness")
    return roles_sources,opponents_sources


def _cohort(stratum,rows):
    """Count deterministic observations using exact same-scene baseline.

    A policy that changes delivered enemy attack count or realized round
    count has a meaningful survival/target result, but its terminal HP/Vigor
    is not the same-exposure contrast. Do not score it as a free benefit.
    """
    baseline={_key(row,BASE_KEYS[stratum]):row for row in rows
              if row["policy"]=="baseline"}
    groups=defaultdict(list)
    for row in rows:
        groups[row["role"],row["policy"]].append(row)
    result=[]
    for (role,policy),cells in sorted(groups.items()):
        stats={
            "role":role,"focus":FOCI[role],"policy":policy,
            "witness_cells":len(cells),"same_exposure_cells":0,
            "changed_exposure_cells":0,
            "higher_terminal_hp_cells":0,"lower_terminal_hp_cells":0,
            "higher_terminal_vigor_cells":0,"lower_terminal_vigor_cells":0,
            "nonzero_spent_vp_cells":0,"nonzero_committed_vp_cells":0,
            "nonzero_ap_paid_cells":0,
        }
        if stratum=="extended_attrition":
            stats.update({"longer_survival_windows":0,
                          "shorter_survival_windows":0,
                          "native_heal_deliveries":0,
                          "exaltation_arms":0})
        if stratum=="multi_recipient":
            stats.update({"ally_front_hp_improved_cells":0,
                          "ally_rear_hp_improved_cells":0,
                          "paid_heal_receipts":0,
                          "reassignment_receipts":0,
                          "guided_intercession_receipts":0,
                          "vital_intercession_receipts":0,
                          "skipped_dead_target_cells":0})
        for row in cells:
            d=row["delta_vs_same_source_baseline"]
            m=row["metrics"]
            base=baseline[_key(row,BASE_KEYS[stratum])]["metrics"]
            if stratum=="matched_self":
                hp,vigor=d["hp_delta"],d["vigor_delta"]
                same=True
                vp=m["final_vp"]
                ap=m["projection_or_full_ap_paid"]
            elif stratum=="extended_attrition":
                hp,vigor=d["hp_delta"],d["vigor_delta"]
                same=(m["rounds_completed"]==base["rounds_completed"])
                if row["round_completion_delta"]!=(
                        m["rounds_completed"]-base["rounds_completed"]):
                    raise AssertionError("Unattested attrition exposure delta")
                stats["longer_survival_windows"]+=(
                    m["rounds_completed"]>base["rounds_completed"])
                stats["shorter_survival_windows"]+=(
                    m["rounds_completed"]<base["rounds_completed"])
                stats["native_heal_deliveries"]+=(
                    m["heal_hp"]>0 or m["heal_vigor"]>0)
                stats["exaltation_arms"]+=m["exaltation_arms"]
                vp=m["final_vp"]
                ap=m["projection_or_full_ap_paid"]
            else:
                hp=sum(d[k] for k in ("front_hp","rear_hp","priest_hp"))
                vigor=sum(d[k] for k in (
                    "front_vigor","rear_vigor","priest_vigor"))
                same=(m["paid_enemy_hits"]==base["paid_enemy_hits"])
                vp=m["vp"]
                ap=m["ap_paid"]
                stats["ally_front_hp_improved_cells"]+=(d["front_hp"]>0 and same)
                stats["ally_rear_hp_improved_cells"]+=(d["rear_hp"]>0 and same)
                stats["paid_heal_receipts"]+=m["paid_heal_count"]
                stats["reassignment_receipts"]+=m["consecration_reassignments"]
                stats["guided_intercession_receipts"]+=m["guided_intercessions"]
                stats["vital_intercession_receipts"]+=m["vital_intercessions"]
                stats["skipped_dead_target_cells"]+=m["skipped_dead_target"]>0
            if same:
                stats["same_exposure_cells"]+=1
                stats["higher_terminal_hp_cells"]+=hp>0
                stats["lower_terminal_hp_cells"]+=hp<0
                stats["higher_terminal_vigor_cells"]+=vigor>0
                stats["lower_terminal_vigor_cells"]+=vigor<0
            else:
                stats["changed_exposure_cells"]+=1
            stats["nonzero_spent_vp_cells"]+=vp[2]>0
            stats["nonzero_committed_vp_cells"]+=vp[1]>0
            stats["nonzero_ap_paid_cells"]+=ap>0
        result.append(stats)
    return result


def assess_matrices(evidence):
    """Analyze native matrices; raw imported input is not origin-attested."""
    _validate_evidence(evidence)
    counts={name:len(evidence[name][ROWS[name]]) for name in COUNTS}
    observations={
        name:_cohort(name,evidence[name][ROWS[name]]) for name in COUNTS
    }
    if any(sum(x["witness_cells"] for x in observations[name])!=counts[name]
           for name in COUNTS):
        raise AssertionError("Summaries must cover every source witness once")
    assessment={
        "version":"B04-B05-Priest-Life-Formal-Balance-Assessment-v0",
        "seed":evidence["matched_self"]["seed"],
        "decision":DECISION,
        "formal_mechanical_audit":"complete_for_bounded_source_scenes",
        "global_balance_certified":False,
        "numerical_tuning_authorized":False,
        "sampled_win_rate":None,"confidence_interval":None,
        "focus_ranking":None,"cross_focus_utility_weights":None,
        "scenario_counts":counts,
        "primary_scenario_total":sum(counts.values()),
        "historical_H_M_ally_context_only":HISTORICAL_ALLY_COUNT,
        "different_policy_cells_not_equal_resource_prices":True,
        "early_stop_and_dead_target_exposure_excluded_from_terminal_deltas":True,
        "source_evidence":[
            {"stratum":name,"source":SOURCES[name],
             "cases":counts[name],
             "native_matrix_sha256":evidence[name]["audit_sha256"],
             "purpose":{
                 "matched_self":"two true hits, self-defense vs same-build baseline",
                 "extended_attrition":"real 4/8-round horizons, defense/cautious movement and early exits",
                 "multi_recipient":"two allies, alternating/rotating target pressure and legal support"
             }[name]} for name in COUNTS],
        "cohort_observations":observations,
        "verified_focus_capabilities":[{"role":k,**POLICIES[k]}
                                      for k in ROLES],
        "unresolved_gates":[{"id":id,"priority":priority,"kind":kind,
                             "basis":basis,"required_evidence":required}
                             for id,priority,kind,basis,required in GAPS],
        "interpretation_rules":[
            "Counts are deterministic witness frequencies, not probabilities, balance scores or outcomes of independent trials.",
            "Only same-source, same-level, same-opponent and same-authored pressure policy receives a local baseline delta.",
            "Terminal resource comparisons exclude differences in actual realized attack exposure or attrition rounds.",
            "Self and external-support strata remain distinct. Low Chosen self Rites cannot be silently retargeted.",
            "A source host reservation is Committed, not Spent; ending a finite effect can refund Committed VP only.",
            "Historical 36 High/Medium F-ally cases are context, never included in the 1384 primary total.",
        ],
    }
    assessment["assessment_sha256"]=canonical_digest(assessment)
    return assessment


def run_assessment(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative source seed required")
    evidence={
        "matched_self":self_matrix(seed=seed),
        "extended_attrition":attrition_matrix(seed=seed),
        "multi_recipient":support_matrix(seed=seed),
    }
    return assess_matrices(evidence)


def attest_assessment(report,*,seed=0):
    """Independently reconstruct all three authoritative native matrices."""
    expected=run_assessment(seed=seed)
    if (not isinstance(report,dict)
            or report.get("assessment_sha256")!=canonical_digest(
                {k:v for k,v in report.items() if k!="assessment_sha256"})
            or report!=expected):
        raise AssertionError("Formal Focus assessment differs from source replay")
    return deepcopy(expected)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args()
    print(json.dumps(run_assessment(seed=args.seed),
                     sort_keys=True,indent=2))


if __name__=="__main__":
    main()
