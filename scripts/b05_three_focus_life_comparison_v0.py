"""B04/B05 Life Focus v0: matched native self-defense and honest delta audit.

H/M/A/B original source-bound actors face identical paid Soldier/Sentry
profile/dice/contact/round policies. Treat A and B as distinct Low builds;
role-local baselines prevent false equivalence of armor/HP/Vigor. Existing
H/M F-ally support reports are separate evidence, not low-self comparisons.
No sampled wins, benchmark equivalence, automatic tuning or Focus approval.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_high_priest_life_invocation_v0 import HighLifeLiturgy
from scripts.b05_medium_priest_consecrations_v0 import MediumLifeConsecrations
from scripts.b05_low_life_native_rites_v0 import LowLifeNativeRites
from scripts.b05_high_life_native_encounter_v0 import run_policy as high_ally_policy
from scripts.b05_medium_life_encounter_balance_v0 import run_policy as medium_ally_policy
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

OPPONENTS={"soldier":("B06-EN-02",None),
           "sentry_prepared":("B06-EN-01","prepared_start")}
ROLE_POLICIES={
    "H":("baseline","guided","shelter"),
    "M":("baseline","guided","shelter"),
    "A":("baseline","guided","exaltation"),
    "B":("baseline","shelter","exaltation"),
}
FOCI={"H":"High","M":"Medium","A":"Low","B":"Low"}
CHOSEN={"A":"Guided Regeneration","B":"Vital Shelter"}
ROLLS={"attack_d20":12,"damage_d6":1,"sentry_vigor_d6":4,
       "wound_location_d20":8}
ROUNDS=2
PHASE="self_defense_two_paid_hits"


def _validate(role,level,opponent,policy,seed):
    if role not in ROLE_POLICIES or policy not in ROLE_POLICIES[role]:
        raise ValueError("Choose authentic H/M/A/B and authored support policy")
    if type(level) is not int or level not in (1,2,3):
        raise ValueError("Only sourced Life L1–3")
    if policy=="exaltation" and level!=3:
        raise ValueError("Low Exaltation requires actual L3")
    if opponent not in OPPONENTS:
        raise ValueError("Choose genuine Soldier or prepared Sentry")
    if type(seed) is not int or seed<0:
        raise ValueError("Seed must be a nonnegative integer")


def scene(*,role,level,opponent,policy,seed=0):
    _validate(role,level,opponent,policy,seed)
    priest=party_actor(role,level,"priest","party",occupied=((2,2),))
    source,start=OPPONENTS[opponent]
    foe=enemy_actor(source,"foe","enemy",start_state=start,
                    occupied=((3,2),))
    e=Encounter([priest,foe],{"priest":30,"foe":20},
                seed=seed,scenario="B04-B05-three-Focus-Life-matched-self",
                policy="one_paid_source_hit_per_round_fixed_same_dice",
                objective="support_survival_evidence_not_victory")
    GridMovement(e,width=8,height=7,scene_id="B05-3focus-self-clear")
    SpellState(e)
    DamageState(e)
    if role=="H":
        support=HighLifeLiturgy(e,"priest",preparation="standard")
    elif role=="M":
        support=MediumLifeConsecrations(e)
    else:
        support=LowLifeNativeRites(e,"priest")
    combat=SourceMelee(e)
    if e.order!=("priest","foe"):
        raise AssertionError("Authored source Initiative order changed")
    e.begin_round()
    e.log("b05_three_focus_policy",focus=FOCI[role],role=role,
          policy=policy,opponent=opponent,level=level,rolls=ROLLS,
          rounds=ROUNDS,recipient="priest",
          mitigation="actor_original_source_armor",
          regen="legal_maximum_current_HP_Vigor_actual_Step2",
          responses="take_hit_no_spontaneous")
    return combat,support


def _start(combat,role,policy,support,round_no,actor_id):
    e=combat.e
    a=e.actors[actor_id]
    if a.hp<=0 and not a.dead:
        choice=RegenerationChoice(cancel_dying_loss=a.vigor>0)
    elif actor_id=="priest":
        throughput=max(0,a.regen+e.g3.regen_throughput(actor_id)
                       +e.g4.toxins.modifier(actor_id,"regen_throughput"))
        choice=RegenerationChoice(
            hp=min(max(0,a.hp_max-a.hp),a.vigor,throughput))
    else:
        choice=RegenerationChoice()
    on_complete=None
    if (role=="A" and policy=="exaltation" and round_no==2
            and actor_id=="priest"):
        def after_step(enc,who):
            step=enc.ledger[-1]
            if (step["kind"]!="regeneration_step"
                    or step["detail"]["actor"]!=who):
                raise AssertionError("No genuine Step2 for Held Renewal")
            a=enc.actors[who]
            throughput=max(0,a.regen+enc.g3.regen_throughput(who)
                           +enc.g4.toxins.modifier(who,"regen_throughput"))
            unused=throughput-step["detail"]["throughput_spent"]
            if unused>0 and a.hp>0 and a.vp_available>0:
                support.arm_held(who,min(2,unused))
        on_complete=after_step
    combat.bridge.start_next_turn(choice,on_regeneration_complete=on_complete)
    if e.current!=actor_id or e.pending_regeneration is not None:
        raise AssertionError("Native turn and Step2 did not finish")


def _priest_action(combat,role,policy,support,round_no):
    if round_no!=1 or policy=="baseline":
        return
    kind=("Guided Regeneration" if policy=="guided" else
          "Vital Shelter" if policy=="shelter" else CHOSEN[role])
    if role=="H":
        effect=support.cast("priest",kind,"priest",
                            access="prepared",mode="maintained")
    elif role=="M":
        effect=support.cast("priest",kind,"priest")
    else:
        effect=support.cast_chosen("priest")
    if effect is None or effect.kind!=kind or effect.recipient!="priest":
        raise AssertionError("Actual source-bound maintained rite not established")
    if role=="B" and policy=="exaltation":
        support.arm_vital("priest")


def _foe(combat,opponent):
    e=combat.e
    profile=("B06-AT-03" if opponent=="soldier"
             else e.g3.sentry_profile("foe"))
    if profile not in ("B06-AT-03","B06-AT-02"):
        raise UnresolvedDecision("Not the exact source Soldier/Sentry profile")
    if not e.g1.melee_contact("foe","priest"):
        raise UnresolvedDecision("Genuine one-square source contact missing")
    declaration=combat.declare("foe","priest",profiles=(profile,),
                               defenses=("take_hit",))
    dice={"attack_face":ROLLS["attack_d20"],
          "damage_face":ROLLS["damage_d6"],
          "wound_location_roll":ROLLS["wound_location_d20"]}
    if profile=="B06-AT-02":
        dice["vigor_die"]=ROLLS["sentry_vigor_d6"]
    result=combat.resolve(declaration,0,**dice)
    if result["outcome"]!="hit" or result["damage"] is None:
        raise AssertionError("Matched scene must deliver one source G5 paid hit")


def _metrics(e):
    a=e.actors["priest"]
    def rows(kind):
        return [x for x in e.ledger if x["kind"]==kind]
    hits=rows("g5_melee_resolved")
    damage=rows("g4_damage_applied")
    steps=[x for x in rows("regeneration_step")
           if x["detail"]["actor"]=="priest"]
    if (len(hits)!=2 or len(damage)!=2 or len(steps)!=2
            or any(x["detail"]["attacker"]!="foe"
                   or x["detail"]["target"]!="priest"
                   or x["detail"]["outcome"]!="hit" for x in hits)
            or any(x["detail"]["recipient"]!="priest" for x in damage)):
        raise AssertionError("Comparison requires exactly two paid attacks and Steps")
    native_vigor=[v for x in damage for v in x["detail"]["vigor_details"]]
    return {
        "starting_hp":a.hp_max,"starting_vigor":a.vigor_max,
        "max_vp":a.vp_max,"source_armor":e.g4._armor(a),
        "final_hp":a.hp,"final_vigor":a.vigor,
        "final_vp":[a.vp_available,a.vp_committed,a.vp_spent],
        "wounds":len(a.wounds),"dying":a.hp<=0,"dead":a.dead,
        "g5_paid_attacks":len(hits),"g4_delivered_hits":len(damage),
        "actual_regen_steps":len(steps),
        "step_hp_restored":sum(x["detail"]["hp_restored"] for x in steps),
        "step_vigor_paid":sum(x["detail"]["throughput_spent"] for x in steps),
        "g4_incoming_hp_after_protection":sum(
            x["detail"]["hp_before"]-x["detail"]["hp_after"] for x in damage),
        "vigor_prevented":sum(v["prevented"] for v in native_vigor),
        "vigor_applied":sum(v["applied"] for v in native_vigor),
        "vital_hp_prevented":sum(x["detail"]["prevented_hp"]
            for x in rows("b05_vital_interposition_applied")),
        "held_hp_restored":sum(x["detail"]["healed"]
            for x in rows("b05_held_renewal_resolved")),
        "exaltation_arms":len(rows("b05_exaltation_armed")),
        "projection_or_full_ap_paid":sum(
            x["detail"]["ap_spent"] for x in rows("action_committed")
            if x["detail"]["actor"]=="priest"),
        "effects_established":len([x for x in rows("g3_effect_established")
                                   if x["detail"]["caster"]=="priest"]),
        "outstanding_exaltation":bool(getattr(
            getattr(e.g3,"low_life",None),"pending",None)),
    }


def run_policy(*,role,level,opponent,policy,seed=0):
    combat,support=scene(role=role,level=level,opponent=opponent,
                         policy=policy,seed=seed)
    e=combat.e
    for round_no in (1,2):
        if round_no>1:
            combat.bridge.begin_next_round()
        for actor_id in e.order:
            _start(combat,role,policy,support,round_no,actor_id)
            if actor_id=="priest":
                _priest_action(combat,role,policy,support,round_no)
            else:
                _foe(combat,opponent)
            combat.bridge.end_current_turn()
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots()):
        raise AssertionError("Unresolved native G0 turn or paid source G5 slot")
    e.check()
    report={"version":"B04-B05-Three-Focus-Life-Matched-Self-v0",
            "focus":FOCI[role],"role":role,"level":level,
            "opponent":opponent,"policy":policy,"seed":seed,
            "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
            "source_digests":{k:a.source.digest for k,a in e.actors.items()},
            "metrics":_metrics(e),"ledger":deepcopy(e.ledger),
            "matched_target_type":"priest_self",
            "full_encounter_certified":False,
            "three_focus_balance_certified":False,
            "sampled_win_rate":None,"effectiveness_weighting":None}
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,role,level,opponent,policy,seed=0):
    """Replay from exact sources; rehashed forged receipts never authenticate."""
    expected=run_policy(role=role,level=level,opponent=opponent,
                        policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Comparative report differs from native source replay")
    return deepcopy(expected)


def _baseline_delta(actual,baseline):
    """Compare *only* to this very same role/level/opponent's no-magic run."""
    return {
        "hp_delta":actual["final_hp"]-baseline["final_hp"],
        "vigor_delta":actual["final_vigor"]-baseline["final_vigor"],
        "wound_delta":actual["wounds"]-baseline["wounds"],
        "vigor_prevented_delta":
            actual["vigor_prevented"]-baseline["vigor_prevented"],
        "native_hp_prevented_delta":
            actual["vital_hp_prevented"]-baseline["vital_hp_prevented"],
        "spent_vp_delta":actual["final_vp"][2]-baseline["final_vp"][2],
        "committed_vp_delta":actual["final_vp"][1]-baseline["final_vp"][1],
        "ap_paid_delta":actual["projection_or_full_ap_paid"]
                        -baseline["projection_or_full_ap_paid"],
    }


def _ally_bridge(level,opponent,seed):
    """Native existing H/M scholar-ally policies; NEVER label Low as ally."""
    choices=(
        ("H","baseline",high_ally_policy(level=level,opponent=opponent,
                                       policy="baseline",seed=seed)),
        ("H","guided",high_ally_policy(level=level,opponent=opponent,
                                     policy="prepared_guided",seed=seed)),
        ("H","shelter",high_ally_policy(level=level,opponent=opponent,
                                      policy="prepared_shelter",seed=seed)),
        ("M","baseline",medium_ally_policy(level=level,opponent=opponent,
                                         policy="no_magic",seed=seed)),
        ("M","guided",medium_ally_policy(level=level,opponent=opponent,
                                       policy="guided",seed=seed)),
        ("M","shelter",medium_ally_policy(level=level,opponent=opponent,
                                        policy="shelter",seed=seed)),
    )
    out=[]
    for role,policy,r in choices:
        m=r["metrics"]
        out.append({
            "role":role,"focus":FOCI[role],"level":level,
            "opponent":opponent,"policy":policy,
            "recipient":"source_F_scholar_ally",
            "source_digests":r["source_digests"],
            "ledger_sha256":r["ledger_sha256"],
            "ally_final_hp":m["ally_hp"],"ally_final_vigor":m["ally_vigor"],
            "ally_wounds":m["ally_wounds"],
            "priest_final_vp":m["high_vp"] if role=="H" else m["priest_vp"],
            "priest_ap_paid":m["high_ap_paid"] if role=="H"
                             else m["ap_committed_by_priest"],
            "vigor_prevented":m["vigor_prevented"] if role=="H"
                              else m["direct_vigor_prevented"],
        })
    return out


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative source seed required")
    runs=[]
    for level in (1,2,3):
        for opponent in OPPONENTS:
            for role,policies in ROLE_POLICIES.items():
                for policy in policies:
                    if policy=="exaltation" and level!=3:
                        continue
                    r=run_policy(role=role,level=level,opponent=opponent,
                                 policy=policy,seed=seed)
                    runs.append({k:r[k] for k in (
                        "focus","role","level","opponent","policy",
                        "metrics","source_digests","ledger_sha256")})
    index={(r["role"],r["level"],r["opponent"],r["policy"]):r
           for r in runs}
    for r in runs:
        baseline=index[r["role"],r["level"],r["opponent"],"baseline"]
        r["delta_vs_same_source_baseline"]=_baseline_delta(
            r["metrics"],baseline["metrics"])
    ally=[]
    for level in (1,2,3):
        for opponent in OPPONENTS:
            ally+=_ally_bridge(level,opponent,seed)
    report={"version":"B04-B05-Three-Focus-Life-Comparison-v0",
            "seed":seed,"matched_self_cells":len(runs),
            "matched_self":runs,"existing_same_F_ally_cells":len(ally),
            "high_medium_same_ally":ally,
            "low_ally_comparison_supported":False,
            "self_armor_hp_vigor_normalized_across_focuses":False,
            "local_baseline_delta_only":True,
            "fixed_dice_not_probability_sample":True,
            "no_automatic_tuning":True,
            "balance_candidates_require_followup":True,
            "three_focus_balance_certified":False,
            "sampled_win_rate":None,"confidence_interval":None,
            "focus_ranking":None}
    report["audit_sha256"]=canonical_digest(report)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role",choices=tuple(ROLE_POLICIES))
    parser.add_argument("--level",type=int,choices=(1,2,3))
    parser.add_argument("--opponent",choices=tuple(OPPONENTS))
    parser.add_argument("--policy")
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args()
    selected=(args.role is not None,args.level is not None,
              args.opponent is not None,args.policy is not None)
    if any(selected) and not all(selected):
        parser.error("Provide role, level, opponent and policy together")
    value=(run_policy(role=args.role,level=args.level,
                      opponent=args.opponent,policy=args.policy,seed=args.seed)
           if all(selected) else run_matrix(seed=args.seed))
    print(json.dumps(value,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
