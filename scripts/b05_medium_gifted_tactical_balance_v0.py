"""B04/B05 Medium Gifted bounded native Soldier/Sentry tactical comparisons.

Every hit/defense, Ward placement/retune, adjacency, VP change, HP packet,
Step-2 recovery and G5 response is emitted by actual G0–G5 state.
These deliberately fixed choices are not simulated player behavior or CR.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_medium_gifted_native_ward_v0 import gifted_actor, MediumGiftedWardNative
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, _fingerprint,
    enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

LEVELS=(1,2,3)
SCENARIOS={
    "soldier": {"source":"B06-EN-02", "profile":"B06-AT-03", "rounds":4,
                "policies":("fear","dormant","dodge","retune")},
    "sentry": {"source":"B06-EN-01", "profile":"B06-AT-02", "rounds":2,
               "policies":("trust","dormant","diagonal")},
}
SWORD_ATTACK_FACE=4
SWORD_DAMAGE_D6=1
SENTRY_VIGOR_D6=4
WOUND_D20=8
WARD_GRADE=2
SOURCE_BASIS=(
    "scripts/b05_medium_gifted_l1_l3_v0.py",
    "scripts/b05_medium_gifted_native_ward_v0.py",
    "scripts/b06_encounter_state_v0.py",
    "scripts/b06_movement_v0.py",
    "scripts/b06_ranged_v0.py",
    "scripts/b06_spells_v0.py",
    "scripts/b06_damage_v0.py",
    "scripts/b06_wound_continuation_v0.py",
    "scripts/b06_offturn_opportunity_v0.py",
    "scripts/b06_soldier_sentry_g5_v0.py",
)


def _validate(opponent,level,policy,seed):
    if opponent not in SCENARIOS:
        raise ValueError("Only authored Soldier/Sentry tactical scenes")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only source-attested Medium Gifted L1–3")
    if policy not in SCENARIOS[opponent]["policies"]:
        raise ValueError("Policy unavailable for this opponent")
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative deterministic scene seed required")


def _recovery(e,who):
    a=e.actors[who]
    if who=="foe":
        # Opponent does not choose recovery in the bounded policy.
        return RegenerationChoice()
    if a.hp<=0:
        return RegenerationChoice(cancel_dying_loss=(not a.dead and a.vigor>0))
    rate=max(0,a.regen+e.g3.regen_throughput(who)
             +e.g4.toxins.modifier(who,"regen_throughput"))
    return RegenerationChoice(hp=min(max(0,a.hp_max-a.hp),a.vigor,rate))


def _events(e,kind):
    return [v for v in e.ledger if v["kind"]==kind]


def run_case(*,opponent,level,policy,seed=0):
    """Run the fully authored combat/positioning policy in actual G0 time.

    Soldier: four separate source Sword attempts at Medium Gifted.
    Sentry: two prepared Sword attempts at an allied R, while Medium Gifted
    either remains orthogonally adjacent or deliberately leaves that radius.
    Neither policy makes unauthored player offense or declares victory.
    """
    _validate(opponent,level,policy,seed)
    spec=SCENARIOS[opponent]
    gifted=gifted_actor(level,"gifted","party",occupied=((2,2),))
    actors=[gifted]
    if opponent=="sentry":
        ally=party_actor("R",level,"ally","party",occupied=((3,2),))
        actors.append(ally)
        foe=enemy_actor(spec["source"],"foe","enemy",
                        start_state="prepared_start",occupied=((4,2),))
        initiative={"gifted":50,"ally":40,"foe":20}
    else:
        foe=enemy_actor(spec["source"],"foe","enemy",occupied=((3,2),))
        initiative={"gifted":50,"foe":20}
    actors.append(foe)
    e=Encounter(actors,initiative,seed=seed,
                scenario="B04-B05-Medium-Gifted-Ward-tactical-balance-v0",
                policy=f"{opponent}:{policy}",
                objective="fixed_policy_multiround_native_receipts_not_terminal_CR")
    GridMovement(e,width=8,height=7,scene_id="medium-gifted-tactical-grid")
    RangedCombat(e,scene_id="medium-gifted-tactical-lane")
    SpellState(e)
    DamageState(e)
    g5=SourceMelee(e)
    ward=MediumGiftedWardNative(e,"gifted")
    if e.order!=tuple(initiative):
        raise AssertionError("Tactical witness initiative changed")
    e.begin_round()
    e.log("b05_medium_gifted_tactical_authored",
          opponent=opponent,policy=policy,level=level,rounds=spec["rounds"],
          seed=seed,grade=WARD_GRADE,source_profile=spec["profile"],
          attack_face=SWORD_ATTACK_FACE,damage_face=SWORD_DAMAGE_D6,
          vigor_die=SENTRY_VIGOR_D6 if opponent=="sentry" else None,
          wound_location=WOUND_D20,
          source_digests={x.id:x.source.digest for x in actors})
    for round_no in range(1,spec["rounds"]+1):
        if round_no>1:
            g5.bridge.begin_next_round()
        for who in e.order:
            a=e.actors[who]
            g5.bridge.start_next_turn(_recovery(e,who))
            if who=="gifted" and a.hp>0 and not a.dead:
                if round_no==1:
                    emotion=("Fear" if opponent=="soldier" and policy!="dormant"
                             else "Trust" if opponent=="sentry" and policy!="dormant"
                             else "Joy")
                    ward.establish_emotion(emotion)
                    serial=ward.place(WARD_GRADE)
                    if (len(ward.conduits)!=1 or ward.conduits[0].serial!=serial):
                        raise AssertionError("Actual source Ward placement missing")
                else:
                    emotion=("Joy" if policy=="retune" else
                             "Joy" if policy=="dormant" else
                             "Fear" if opponent=="soldier" else "Trust")
                    ward.establish_emotion(emotion)
                    # Position changes must affect the *live* G1 radius,
                    # never a caller-supplied ally-distance flag.
                    if policy=="diagonal" and round_no==2:
                        if not e.g1.step("gifted",(0,-1),responses=()):
                            raise AssertionError("Source-funded diagonal reposition failed")
            elif who=="foe" and a.hp>0 and not a.dead:
                target="ally" if opponent=="sentry" else "gifted"
                victim=e.actors[target]
                if victim.dead:
                    # No authorized alternate target, don't create a ghost hit.
                    e.log("b05_medium_tactical_attack_skipped",round_no=round_no,
                          reason="authored_target_dead",target=target)
                else:
                    if not e.g1.melee_contact("foe",target):
                        raise AssertionError("Source Sword target no longer in G1 contact")
                    defense="dodge" if policy=="dodge" else "take_hit"
                    seq=g5.declare("foe",target,profiles=(spec["profile"],),
                                   defenses=(defense,))
                    args={"attack_face":SWORD_ATTACK_FACE}
                    # An unconfirmed hit may not smuggle dice into G4.
                    if defense!="dodge":
                        args.update(damage_face=SWORD_DAMAGE_D6,
                                    wound_location_roll=WOUND_D20)
                        if opponent=="sentry":
                            args["vigor_die"]=SENTRY_VIGOR_D6
                    actual=g5.resolve(seq,0,**args)
                    expected="miss" if defense=="dodge" else "hit"
                    if actual["outcome"]!=expected:
                        raise AssertionError("Fixed native G5 attack result drifted")
            g5.bridge.end_current_turn()
    if e.current is not None or g5.pending_attack_slots():
        raise AssertionError("Committed native attack slots/turn left open")
    e.check()
    pulses=_events(e,"b05_medium_ward_pulse")
    hits=[v for v in _events(e,"g5_melee_resolved")
          if v["detail"].get("attacker")=="foe"]
    attacks=[v for v in hits if v["detail"].get("outcome")=="hit"]
    damage=[v for v in _events(e,"g4_damage_applied")
            if v["detail"].get("cause")=="source-profile:"+spec["profile"]]
    defense=[v for v in _events(e,"defense_assigned")
             if v["detail"].get("actor")==
                  ("ally" if opponent=="sentry" else "gifted")]
    placement=[v for v in _events(e,"b05_medium_ward_placed")]
    ap=[v for v in _events(e,"action_committed")
        if v["detail"].get("actor")=="gifted"]
    vps=[v for v in _events(e,"vp_transition")
         if v["detail"].get("actor")=="gifted"]
    ally=e.actors.get("ally")
    expected_pulses=(0 if policy in ("dormant","dodge") else
                     1 if policy in ("retune","diagonal") else spec["rounds"])
    if (len(placement)!=1 or len(hits)!=spec["rounds"] or
            len(damage)!=len(attacks) or len(pulses)!=expected_pulses or
            len(defense)!=len(hits)):
        raise AssertionError("Native encounter attacks, Pulse cadence or receipts drifted")
    if any(p["detail"].get("prevented")!=WARD_GRADE for p in pulses):
        raise AssertionError("Unexpected Grade II native prevention")
    if (len([v for v in vps if v["detail"]["mode"]=="committed"])!=1 or
            len([v for v in vps if v["detail"]["mode"]=="spent"])!=0 or
            sum(v["detail"]["ap_spent"] for v in ap)!=24 or
            gifted.vp_committed!=WARD_GRADE or gifted.vp_spent!=0):
        raise AssertionError("Ward reservation/AP did not follow native G0")
    recipient=ally if ally is not None else gifted
    metrics={
        "rounds":spec["rounds"],
        "g5_attacks":len(hits),"g5_hits":len(attacks),
        "g4_source_packets":len(damage),
        "g45_attested_hits":len(_events(e,"g45_attested_hit")),
        "pulse_count":len(pulses),
        "hp_prevented":sum(p["detail"]["prevented"] for p in pulses
                            if p["detail"]["emotion"]=="Fear"),
        "vigor_prevented":sum(p["detail"]["prevented"] for p in pulses
                               if p["detail"]["emotion"]=="Trust"),
        "recipient_hp":recipient.hp,"recipient_vigor":recipient.vigor,
        "recipient_dying":recipient.hp<=0 and not recipient.dead,
        "recipient_dead":recipient.dead,
        "recipient_regen_hp":sum(v["detail"].get("hp_restored",0)
                                  for v in _events(e,"regeneration_step")
                                  if v["detail"].get("actor")==recipient.id),
        "gifted_ap_ward":sum(v["detail"]["ap_spent"] for v in ap),
        "gifted_vp_state":[gifted.vp_available,gifted.vp_committed,gifted.vp_spent],
        "gifted_ap_physical":sum(v["detail"]["ap_spent"] for v in ap
                                  if v["detail"].get("action_class")=="physical"),
        "gifted_position":[list(v) for v in gifted.occupied],
        "recipient_position":[list(v) for v in recipient.occupied],
        "attack_defenses":[v["detail"].get("defense") for v in defense],
        "emotion_windows":len(_events(e,"b05_medium_emotion_established")),
        "ward_instances":len(ward.conduits),
        "active_ward":ward.conduits[0].status if ward.conduits else None,
        "regen_steps":len(_events(e,"regeneration_step")),
        "movement_steps":len(_events(e,"g1_movement_step")),
        "wounds_created":len(_events(e,"g4_wound_created")),
    }
    result={
        "version":"B04-B05-Medium-Gifted-Tactical-Balance-v0",
        "opponent":opponent,"level":level,"policy":policy,"seed":seed,
        "basis_sha256":{p:_fingerprint(p) for p in SOURCE_BASIS},
        "source_digests":{a.id:a.source.digest for a in e.actors.values()},
        "inputs":{"grade":WARD_GRADE,"attack_face":SWORD_ATTACK_FACE,
                  "damage_d6":SWORD_DAMAGE_D6,"sentry_vigor_d6":
                      SENTRY_VIGOR_D6 if opponent=="sentry" else None,
                  "wound_d20":WOUND_D20,"initial_gifted":[2,2],
                  "initial_foe":[4,2] if opponent=="sentry" else [3,2],
                  "initial_ally":[3,2] if opponent=="sentry" else None},
        "metrics":metrics,"ledger":deepcopy(e.ledger),
        "fixed_policy_only":True,"representative_encounter":False,
        "full_focus_certified":False,"numerical_tuning_authorized":False,
        "win_rate":None,
    }
    result=json.loads(json.dumps(result,sort_keys=True,allow_nan=False))
    result["ledger_sha256"]=canonical_digest(result["ledger"])
    result["audit_sha256"]=canonical_digest(result)
    return result


def attest_case(report,*,opponent,level,policy,seed=0):
    """Use a fresh source replay; hashes of mutable incoming JSON do not suffice."""
    try:
        return report==run_case(opponent=opponent,level=level,
                                policy=policy,seed=seed)
    except (ValueError,UnresolvedDecision,AssertionError,TypeError,KeyError):
        return False


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative matrix seed required")
    cases=[run_case(opponent=opponent,level=level,policy=policy,seed=seed)
           for opponent,spec in SCENARIOS.items()
           for level in LEVELS for policy in spec["policies"]]
    summary={
        "cases":len(cases),"levels":list(LEVELS),
        "opponents":list(SCENARIOS),
        "policies":{k:list(v["policies"]) for k,v in SCENARIOS.items()},
        "holdfast_compared":True,"shared_reserve_compared":True,
        "full_focus_certified":False,"representative_encounter":False,
        "numerical_tuning_authorized":False,"win_rate":None,
    }
    data={"version":"B04-B05-Medium-Gifted-Tactical-Balance-v0",
          "seed":seed,"summary":summary,"cases":cases}
    data=json.loads(json.dumps(data,sort_keys=True,allow_nan=False))
    data["audit_sha256"]=canonical_digest(data)
    return data


def attest_matrix(report,*,seed=0):
    try:
        return report==run_matrix(seed=seed)
    except (ValueError,UnresolvedDecision,AssertionError,TypeError,KeyError):
        return False


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--summary",action="store_true")
    args=parser.parse_args()
    r=run_matrix(seed=args.seed)
    print(json.dumps(r["summary"] if args.summary else r,
                     indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False))


if __name__=="__main__":
    main()
