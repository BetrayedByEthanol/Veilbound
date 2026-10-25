"""B04/B05 Three-Focus Life: source-paid multi-recipient support stress v0.

Use native G0/G1/G3/G4/G4.5/G5 actions, real opposing Soldier or Sentry
attacks against two distinct source F/R allies (and optionally Priest), with
explicit target policy. Keep Low's Chosen Rite self-only, A's verified Basic
Heal legal, B's occupied-hands limitation, Medium's one-host and reaction
limits, and High's prepared access. Four rounds, no statistical win claims.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_high_priest_life_invocation_v0 import HighLifeLiturgy
from scripts.b05_medium_priest_consecrations_v0 import MediumLifeConsecrations
from scripts.b05_low_life_native_rites_v0 import LowLifeNativeRites
from scripts.b05_three_focus_life_comparison_v0 import OPPONENTS, FOCI
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

ROUNDS=4
PATTERNS={
    "alternating":("front","rear","front","rear"),
    "rotating":("front","rear","priest","front"),
}
DAMAGE_FACES={"light":1,"heavy":4}
POLICIES={
    "H":("baseline","guided_front","shelter_front",
         "triage","split_wards"),
    "M":("baseline","guided_front","guided_reassign",
         "guided_intercession","shelter_front","shelter_reassign",
         "shelter_intercession","triage"),
    "A":("baseline","chosen_self","triage","chosen_and_heal"),
    "B":("baseline","chosen_self","vital_exaltation"),
}
L3_ONLY={"H":frozenset(("split_wards",)),
         "M":frozenset(("guided_intercession","shelter_intercession")),
         "A":frozenset(),
         "B":frozenset(("vital_exaltation",))}
L2_ONLY={role:(frozenset(("chosen_and_heal",)) if role=="A" else frozenset())
         for role in POLICIES}
ATTACK_FACE=12
SENTRY_DIE=4
HEAL_DIE=3
WOUND_ROLL=8


def _validate(role,level,opponent,pattern,policy,pressure,seed):
    if role not in POLICIES or policy not in POLICIES[role]:
        raise ValueError("No such source Life focus/policy")
    if type(level) is not int or level not in (1,2,3):
        raise ValueError("Only original L1–3 characters")
    if policy in L3_ONLY[role] and level<3:
        raise ValueError("Requires original L3 Focus ability")
    if policy in L2_ONLY[role] and level<2:
        raise ValueError("Cannot fund chosen and paid Heal at L1")
    if opponent not in OPPONENTS or pattern not in PATTERNS:
        raise ValueError("Only source Soldier/Sentry and explicit authored targets")
    if pressure not in DAMAGE_FACES:
        raise ValueError("Only precommitted legal d6 pressure")
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative integral replay seed required")


def scene(*,role,level,opponent,pattern,policy,pressure,seed=0):
    _validate(role,level,opponent,pattern,policy,pressure,seed)
    source,start=OPPONENTS[opponent]
    priest=party_actor(role,level,"priest","party",occupied=((2,1),))
    front=party_actor("F",level,"front","party",occupied=((2,2),))
    rear=party_actor("R",level,"rear","party",occupied=((3,3),))
    foe=enemy_actor(source,"foe","enemy",start_state=start,
                    occupied=((3,2),))
    e=Encounter([priest,foe,front,rear],
                {"priest":40,"foe":30,"front":20,"rear":10},
                seed=seed,scenario="B04-B05-Life-three-focus-multi-recipient",
                policy="fixed_adversary_target_schedule_native_paid_attacks",
                objective="external_support_and_intercession_not_victory")
    GridMovement(e,width=8,height=7,scene_id="B05-life-4-actor-clear")
    SpellState(e)
    DamageState(e)
    adapter=(HighLifeLiturgy(e,"priest",preparation="standard")
             if role=="H" else
             MediumLifeConsecrations(e) if role=="M" else
             LowLifeNativeRites(e,"priest"))
    combat=SourceMelee(e)
    if e.order!=("priest","foe","front","rear"):
        raise AssertionError("Authored multi-recipient Initiative order changed")
    for recipient in ("priest","front","rear"):
        if not e.g1.melee_contact("foe",recipient):
            raise AssertionError("Source opponent must have original G1 contact")
    e.begin_round()
    e.log("b05_multi_support_policy",role=role,focus=FOCI[role],
          level=level,opponent=opponent,pattern=pattern,policy=policy,
          pressure=pressure,rounds=ROUNDS,
          target_schedule=list(PATTERNS[pattern]),
          die_face=DAMAGE_FACES[pressure],attack_face=ATTACK_FACE,
          sentry_vigor_die=SENTRY_DIE,heal_die=HEAL_DIE,
          wound_location=WOUND_ROLL,defenses="take_hit",
          optional_responses="decline_all",source_digests={
              who:a.source.digest for who,a in e.actors.items()})
    return combat,adapter


def _target_geometry(e,recipient):
    """Independent native clear-line confirmation for source A/G4 healing."""
    if recipient not in ("front","rear","priest"):
        raise UnresolvedDecision("No invented healing target")
    priest=e.actors["priest"]
    target=e.actors[recipient]
    if target.dead or len(priest.occupied)!=1 or len(target.occupied)!=1:
        raise UnresolvedDecision("Requires living genuine one-square recipient")
    src,dst=priest.occupied[0],target.occupied[0]
    dx,dy=sorted((abs(src[0]-dst[0]),abs(src[1]-dst[1])),reverse=True)
    if dx+0.5*dy>3:
        raise ValueError("Source Life delivery beyond three squares")
    cells,corners=RangedCombat._ray(src,dst)
    if (any(c in e.g1.walls for c in cells[1:-1])
            or any(x in e.g1.walls or y in e.g1.walls
                   for x,y in corners)):
        raise ValueError("Source Life delivery blocked")


def _step(combat,adapter,role,policy,who,round_no):
    e=combat.e
    a=e.actors[who]
    if a.hp<=0 and not a.dead:
        choice=RegenerationChoice(cancel_dying_loss=a.vigor>0)
    elif a.dead:
        choice=RegenerationChoice()
    else:
        throughput=max(0,a.regen+e.g3.regen_throughput(who)
                       +e.g4.toxins.modifier(who,"regen_throughput"))
        bonus=int(role=="M" and policy=="guided_intercession"
                  and who=="rear" and round_no==2
                  and a.hp<a.hp_max and a.vigor>0)
        # Intercession is not a free buff. The callback must pay it
        # inside that recipient's actual pending Step-2 response window.
        if bonus and not (e.actors["priest"].vp_available>=2
                          and e.actors["priest"].reaction_available
                          and adapter._host("priest") is not None
                          and adapter._host("priest").recipient!=who):
            bonus=0
        choice=RegenerationChoice(
            hp=min(a.hp_max-a.hp,a.vigor,throughput+bonus))
    callback=None
    if (role=="M" and policy=="guided_intercession"
            and who=="rear" and round_no==2 and a.hp>0 and a.vigor>0
            and choice.hp>max(0,a.regen+e.g3.regen_throughput(who)
                              +e.g4.toxins.modifier(who,"regen_throughput"))):
        def on_ready(enc,recipient):
            adapter.intercede_regeneration("priest",recipient)
        callback=on_ready
    combat.bridge.start_next_turn(choice,on_regeneration_ready=callback)
    if e.current!=who or e.pending_regeneration is not None:
        raise AssertionError("Authentic Step 2 and turn readiness required")


def _heal(combat,adapter,role,recipient):
    e=combat.e
    priest=e.actors["priest"]
    target=e.actors[recipient]
    if (priest.hp<=0 or target.dead or
            (target.hp>=target.hp_max and target.vigor>=target.vigor_max)
            or priest.vp_available<2):
        return False
    _target_geometry(e,recipient)
    if role=="H":
        result=adapter.cast("priest","Basic Heal",recipient,
                            access="prepared",mode="instant",
                            die=HEAL_DIE,hand_available=True)
    elif role in ("M","A"):
        result=e.g4.cast_basic_heal(
            "priest",recipient,tier=1,die=HEAL_DIE,
            hand_available=True,in_range=True,unobstructed=True,
            unopposed=True)
    else:
        raise UnresolvedDecision("Source B has no free hand for Basic Heal")
    if result is None:
        raise AssertionError("Paid Life Primary interrupted in clear scene")
    return True


def _priest(combat,adapter,role,policy,round_no):
    e=combat.e
    a=e.actors["priest"]
    if a.hp<=0:
        return
    if round_no==1 and policy not in ("baseline","triage"):
        if role=="H":
            if policy=="split_wards":
                result=adapter.cast("priest","Guided Regeneration","front",
                                     mode="maintained")
                result2=adapter.cast("priest","Vital Shelter","rear",
                                      mode="maintained")
                if result is None or result2 is None:
                    raise AssertionError("H L3 native double Projection failed")
            else:
                kind=("Guided Regeneration" if policy=="guided_front"
                      else "Vital Shelter")
                if adapter.cast("priest",kind,"front",mode="maintained") is None:
                    raise AssertionError("H prepared external Primary failed")
        elif role=="M":
            kind=("Guided Regeneration" if policy.startswith("guided")
                  else "Vital Shelter")
            recipient=("priest" if policy=="shelter_intercession"
                       else "front")
            if policy=="guided_intercession":
                recipient="front"
            if adapter.cast("priest",kind,recipient) is None:
                raise AssertionError("M one-host Consecration failed")
        else:
            if adapter.cast_chosen("priest") is None:
                raise AssertionError("Low's only verified Chosen self host missing")
    if (role=="M" and round_no==2
            and policy in ("guided_reassign","shelter_reassign")
            and adapter._host("priest") is not None):
        if adapter.reassign("priest","rear") is not True:
            raise AssertionError("Native paid Medium reassignment failed")
    if (role=="B" and policy=="vital_exaltation" and a.level==3
            and adapter.pending is None and adapter._host()
            and adapter._host()[0].budget>=2 and a.vp_available>=1):
        adapter.arm_vital("priest")
    if policy in ("triage","chosen_and_heal"):
        # On the first round no ally yet has source damage. Beginning R2,
        # choose the already injured living external ally with largest
        # actual deficit; ties resolve by authored front then rear order.
        if round_no>1:
            candidates=[name for name in ("front","rear")
                        if not e.actors[name].dead]
            candidates.sort(key=lambda name:(
                -(e.actors[name].hp_max-e.actors[name].hp),
                -(e.actors[name].vigor_max-e.actors[name].vigor),
                ("front","rear").index(name)))
            if candidates:
                _heal(combat,adapter,role,candidates[0])


def _foe(combat,opponent,recipient,pressure,role,policy,round_no):
    e=combat.e
    if e.actors[recipient].dead:
        # The policy never silently retargets its precommitted attack
        # onto a different character to improve an outcome.
        e.log("b05_multi_target_unavailable",recipient=recipient,
              reason="dead_prior_to_source_attack",
              original_round=round_no,policy=policy)
        return
    profile=("B06-AT-03" if opponent=="soldier"
             else e.g3.sentry_profile("foe"))
    if profile not in ("B06-AT-03","B06-AT-02"):
        raise UnresolvedDecision("Source enemy's original sword unavailable")
    if not e.g1.melee_contact("foe",recipient):
        raise UnresolvedDecision("Source-target contact changed")
    sequence=combat.declare("foe",recipient,profiles=(profile,),
                            defenses=("take_hit",))
    dice={"attack_face":ATTACK_FACE,"damage_face":DAMAGE_FACES[pressure],
          "wound_location_roll":WOUND_ROLL}
    if profile=="B06-AT-02":
        dice["vigor_die"]=SENTRY_DIE
    if (role=="M" and policy=="shelter_intercession"
            and recipient=="rear" and round_no==2
            and e.actors["priest"].reaction_available
            and e.actors["priest"].vp_available>=2
            and e.actors[recipient].vigor>0
            and adapter_host_shelter(e)):
        dice["medium_intercessor"]="priest"
    outcome=combat.resolve(sequence,0,**dice)
    if outcome["outcome"]!="hit" or outcome["damage"] is None:
        raise AssertionError("Expected source-paid Take Hit outcome")


def adapter_host_shelter(e):
    medium=getattr(e.g3,"medium_life",None)
    host=medium._host("priest") if medium is not None else None
    return bool(host is not None and host.kind=="Vital Shelter"
                and host.recipient!="rear" and host.budget)


def _metrics(e,role,pattern):
    priest=e.actors["priest"]
    def rows(kind):
        return [x for x in e.ledger if x["kind"]==kind]
    attacked=rows("g5_melee_resolved")
    damage=rows("g4_damage_applied")
    skipped=rows("b05_multi_target_unavailable")
    expected=PATTERNS[pattern]
    if (len(attacked)+len(skipped)!=ROUNDS
            or any(x["detail"]["target"]!=expected[x["round"]-1]
                   or x["detail"]["outcome"]!="hit" for x in attacked)
            or len(attacked)!=len(damage)):
        raise AssertionError("Only exact native target schedule may be attested")
    step_counts={who:len([x for x in rows("regeneration_step")
                          if x["detail"]["actor"]==who])
                 for who in ("priest","front","rear")}
    if any(v!=ROUNDS for v in step_counts.values()):
        raise AssertionError("One native regeneration per living/eligible turn required")
    return {
        "recipients":{
            who:{"hp":e.actors[who].hp,
                 "vigor":e.actors[who].vigor,
                 "wounds":len(e.actors[who].wounds),
                 "dead":e.actors[who].dead}
            for who in ("front","rear","priest")},
        "paid_enemy_hits":len(attacked),
        "skipped_dead_target":len(skipped),
        "received_by":{
            who:len([x for x in attacked if x["detail"]["target"]==who])
            for who in ("front","rear","priest")},
        "real_steps":step_counts,
        "natural_hp":{who:sum(x["detail"]["hp_restored"] for x
                in rows("regeneration_step") if x["detail"]["actor"]==who)
            for who in ("front","rear","priest")},
        "direct_vigor_prevented":sum(
            v["prevented"] for x in damage
            for v in x["detail"]["vigor_details"]),
        "direct_vigor_applied":sum(
            v["applied"] for x in damage
            for v in x["detail"]["vigor_details"]),
        "heal_receipts":[x["detail"] for x in rows("g4_basic_heal_applied")],
        "paid_heal_count":len(rows("g4_basic_heal_applied")),
        "consecration_reassignments":len(rows("b05_consecration_reassigned")),
        "intercession_payments":len(rows("b05_intercession_paid")),
        "guided_intercessions":len(rows("b05_guided_intercession_armed")),
        "vital_intercessions":len(rows("b05_vital_intercession_packet")),
        "high_open_prayer_fills":len(rows("b05_open_prayer_slot_filled")),
        "chosen_self_effects":len([
            x for x in rows("g3_effect_established")
            if x["detail"]["caster"]=="priest"
            and x["detail"]["recipient"]=="priest"]),
        "ally_effects":len([
            x for x in rows("g3_effect_established")
            if x["detail"]["caster"]=="priest"
            and x["detail"]["recipient"] in ("front","rear")]),
        "effect_refunds":sum(x["detail"]["returned"]
            for x in rows("g3_effect_ended")
            if x["detail"]["caster"]=="priest"),
        "exaltation_arms":len(rows("b05_exaltation_armed")),
        "vp":[priest.vp_available,priest.vp_committed,priest.vp_spent],
        "ap_paid":sum(x["detail"]["ap_spent"] for x
            in rows("action_committed") if x["detail"]["actor"]=="priest"),
        "reaction_available":priest.reaction_available,
    }


def run_policy(*,role,level,opponent,pattern,policy,pressure="light",seed=0):
    combat,adapter=scene(role=role,level=level,opponent=opponent,
                         pattern=pattern,policy=policy,
                         pressure=pressure,seed=seed)
    e=combat.e
    for round_no,recipient in enumerate(PATTERNS[pattern],start=1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            _step(combat,adapter,role,policy,who,round_no)
            if who=="priest":
                _priest(combat,adapter,role,policy,round_no)
            elif who=="foe":
                _foe(combat,opponent,recipient,pressure,role,policy,round_no)
            combat.bridge.end_current_turn()
    if e.current is not None or combat.pending_attack_slots():
        raise AssertionError("Unclosed native G0 turn/G5 source attack")
    e.check()
    report={
        "version":"B04-B05-Life-Multi-Recipient-Support-v0",
        "role":role,"focus":FOCI[role],"level":level,"opponent":opponent,
        "pattern":pattern,"policy":policy,"pressure":pressure,"seed":seed,
        "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "metrics":_metrics(e,role,pattern),"ledger":deepcopy(e.ledger),
        "multi_recipient_certified":True,
        "full_balance_certified":False,"numerical_tuning_approved":False,
        "sampled_win_rate":None,"focus_ranking":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,role,level,opponent,pattern,policy,
                  pressure="light",seed=0):
    expected=run_policy(role=role,level=level,opponent=opponent,
                        pattern=pattern,policy=policy,
                        pressure=pressure,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Multi-recipient source-native replay differs")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative source seed required")
    rows=[]
    for level in (1,2,3):
        for opponent in OPPONENTS:
            for pattern in PATTERNS:
                for pressure in DAMAGE_FACES:
                    for role,policies in POLICIES.items():
                        for policy in policies:
                            if (policy in L3_ONLY[role] and level<3
                                    or policy in L2_ONLY[role] and level<2):
                                continue
                            r=run_policy(role=role,level=level,
                                         opponent=opponent,pattern=pattern,
                                         pressure=pressure,policy=policy,seed=seed)
                            rows.append({
                                "role":role,"focus":FOCI[role],"level":level,
                                "opponent":opponent,"pattern":pattern,
                                "pressure":pressure,"policy":policy,
                                "metrics":r["metrics"],
                                "source_digests":r["source_digests"],
                                "ledger_sha256":r["ledger_sha256"]})
    key=lambda r:(r["role"],r["level"],r["opponent"],
                  r["pattern"],r["pressure"])
    bases={key(r):r for r in rows if r["policy"]=="baseline"}
    for r in rows:
        b=bases[key(r)]["metrics"]
        m=r["metrics"]
        r["delta_vs_same_source_baseline"]={
            "front_hp":m["recipients"]["front"]["hp"]-b["recipients"]["front"]["hp"],
            "front_vigor":m["recipients"]["front"]["vigor"]-b["recipients"]["front"]["vigor"],
            "rear_hp":m["recipients"]["rear"]["hp"]-b["recipients"]["rear"]["hp"],
            "rear_vigor":m["recipients"]["rear"]["vigor"]-b["recipients"]["rear"]["vigor"],
            "priest_hp":m["recipients"]["priest"]["hp"]-b["recipients"]["priest"]["hp"],
            "priest_vigor":m["recipients"]["priest"]["vigor"]-b["recipients"]["priest"]["vigor"],
            "direct_vigor_prevented":m["direct_vigor_prevented"]-b["direct_vigor_prevented"],
            "spent_vp":m["vp"][2]-b["vp"][2],
            "committed_vp":m["vp"][1]-b["vp"][1],
            "ap_paid":m["ap_paid"]-b["ap_paid"],
        }
    report={
        "version":"B04-B05-Life-Multi-Recipient-Stress-Matrix-v0",
        "seed":seed,"case_count":len(rows),"cases":rows,
        "four_round_target_schedules":list(PATTERNS),
        "low_A_external_basic_heal":True,
        "low_B_external_basic_heal":False,
        "low_chosen_external_targeting":False,
        "source_replay_required":True,
        "same_source_baseline_only":True,
        "focus_balance_certified":False,
        "numerical_tuning_approved":False,
        "statistical_win_rate":None,"focus_ranking":None}
    report["audit_sha256"]=canonical_digest(report)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--role",choices=tuple(POLICIES))
    p.add_argument("--level",type=int,choices=(1,2,3))
    p.add_argument("--opponent",choices=tuple(OPPONENTS))
    p.add_argument("--pattern",choices=tuple(PATTERNS))
    p.add_argument("--policy")
    p.add_argument("--pressure",choices=tuple(DAMAGE_FACES),default="light")
    p.add_argument("--seed",type=int,default=0)
    args=p.parse_args()
    selected=(args.role,args.level,args.opponent,args.pattern,args.policy)
    if any(x is not None for x in selected) and not all(
            x is not None for x in selected):
        p.error("Supply role, level, opponent, pattern, policy together")
    result=run_policy(role=args.role,level=args.level,
                      opponent=args.opponent,pattern=args.pattern,
                      policy=args.policy,pressure=args.pressure,
                      seed=args.seed) if all(x is not None for x in selected) else run_matrix(seed=args.seed)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
