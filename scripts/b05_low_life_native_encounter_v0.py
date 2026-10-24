"""B04/B05 Low Life A/B bounded source-native two-round Soldier/Sentry encounters.

Authentic G5 paid attacks, G4 packet mitigation, G0 Step 2, G3 chosen host,
and optional native L3 Exaltation. Fixed dice/policy != general balance score.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_low_life_native_rites_v0 import LowLifeNativeRites
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,enemy_actor,party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

OPPONENTS={"soldier":("B06-EN-02",None),
           "sentry_prepared":("B06-EN-01","prepared_start")}
ROLES=("A","B")
LEVELS=(1,2,3)
ATTACK_D20=12
SWORD_D6={"A":1,"B":4}
VIGOR_D6=4


def scene(role,level,opponent,seed):
    if role not in ROLES or opponent not in OPPONENTS:
        raise ValueError("Only audited A/B and real Soldier/Sentry")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only original Low Life L1–3")
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative deterministic seed required")
    low=party_actor(role,level,"low","party",occupied=((2,2),))
    source,start=OPPONENTS[opponent]
    foe=enemy_actor(source,"foe","enemy",start_state=start,
                    occupied=((3,2),))
    e=Encounter([low,foe],{"low":30,"foe":20},seed=seed,
                scenario="B04-B05-Low-Life-native-"+role,
                objective="bounded_source_damage_and_low_exaltation",
                policy="fixed_source_dice_decline_optional_responses")
    GridMovement(e,width=8,height=7,scene_id="B05-low-clear-lane")
    SpellState(e)
    DamageState(e)
    adapter=LowLifeNativeRites(e,"low")
    combat=SourceMelee(e)
    if e.order!=("low","foe"):
        raise AssertionError("Initial initiative source order changed")
    e.begin_round()
    e.log("b05_low_native_policy",role=role,level=level,
          opponent=opponent,rounds=2,attack_face=ATTACK_D20,
          damage_die=SWORD_D6[role],vigor_die=VIGOR_D6,
          native_source_digests={k:v.source.digest for k,v in e.actors.items()})
    return combat,adapter


def _start(combat,adapter,actor,round_no):
    e=combat.e
    a=e.actors[actor]
    hp_choice=0
    if a.hp>0:
        hp_choice=min(max(0,a.hp_max-a.hp),a.vigor,
                      a.regen+e.g3.regen_throughput(actor))
    choice=RegenerationChoice(
        hp=hp_choice,
        cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))
    arm=None
    if actor=="low" and round_no==2 and a.level==3 and adapter.chosen_name=="Guided Regeneration":
        # User explicitly chooses two of *genuinely unspent* points only
        # after G0/G4 resolves actual Step 2, before start-of-turn hazards.
        def arm(enc,who):
            step=enc.ledger[-1]["detail"]
            unused=(enc.actors[who].regen+enc.g3.regen_throughput(who)
                    -step["throughput_spent"])
            if unused>0:
                adapter.arm_held(who,min(2,unused))
    combat.bridge.start_next_turn(choice,on_regeneration_complete=arm)


def _foe(combat,opponent):
    e=combat.e
    profile=("B06-AT-03" if opponent=="soldier"
             else e.g3.sentry_profile("foe"))
    if profile not in ("B06-AT-03","B06-AT-02"):
        raise AssertionError("Only native paid Soldier or prepared Sentry attacks")
    if not e.g1.melee_contact("foe","low"):
        raise AssertionError("No native G1 contact")
    declaration=combat.declare("foe","low",profiles=(profile,),
                               defenses=("take_hit",))
    kwargs={"attack_face":ATTACK_D20,"damage_face":SWORD_D6[e.g3.low_life.e.actors["low"].source.source_id],
            "wound_location_roll":8}
    if profile=="B06-AT-02":
        kwargs["vigor_die"]=VIGOR_D6
    outcome=combat.resolve(declaration,0,**kwargs)
    if outcome["outcome"]!="hit" or outcome["damage"] is None:
        raise AssertionError("Expected actually delivered native source hit")


def _metrics(e,role):
    low=e.actors["low"]
    log=e.ledger
    def events(kind):
        return [x for x in log if x["kind"]==kind]
    hit=events("g5_melee_resolved")
    damaged=events("g4_damage_applied")
    if len(hit)!=2 or len(damaged)!=2 or any(
        x["detail"]["target"]!="low" or x["detail"]["outcome"]!="hit"
        for x in hit):
        raise AssertionError("Exactly two genuine native attacks required")
    steps=[x for x in events("regeneration_step")
           if x["detail"]["actor"]=="low"]
    if len(steps)!=2:
        raise AssertionError("Exactly two actual Low Priest Step 2 receipts")
    arming=events("b05_exaltation_armed")
    vitals=events("b05_vital_interposition_applied")
    held=events("b05_held_renewal_resolved")
    return {
        "hp":low.hp,"vigor":low.vigor,
        "vp":[low.vp_available,low.vp_committed,low.vp_spent],
        "pending":getattr(e.g3.low_life,"pending",None),
        "wounds":len(low.wounds),
        "native_g5_paid_hits":len(hit),"native_g4_events":len(damaged),
        "own_real_regen_steps":len(steps),
        "natural_hp_restored":sum(x["detail"]["hp_restored"] for x in steps),
        "natural_vigor_spent":sum(x["detail"]["throughput_spent"] for x in steps),
        "exaltation_paid_arms":len(arming),
        "vital_hp_prevented":sum(x["detail"]["prevented_hp"] for x in vitals),
        "vital_budget_spent":sum(x["detail"]["consumed_budget"] for x in vitals),
        "held_hp_restored":sum(x["detail"]["healed"] for x in held),
        "held_vigor_spent":sum(x["detail"]["vigor_spent"] for x in held),
        "direct_vigor_prevented":sum(d["prevented"] for x in damaged
                                    for d in x["detail"]["vigor_details"]),
        "priest_ap_paid":sum(x["detail"]["ap_spent"] for x in events("action_committed")
                              if x["detail"]["actor"]=="low"),
    }


def run_policy(*,role,level,opponent="soldier",seed=0):
    combat,adapter=scene(role,level,opponent,seed)
    e=combat.e
    for round_no in (1,2):
        if e.round!=round_no:
            combat.bridge.begin_next_round()
        for actor_id in e.order:
            _start(combat,adapter,actor_id,round_no)
            if actor_id=="low" and round_no==1:
                host=adapter.cast_chosen("low")
                if host is None:
                    raise AssertionError("Source Chosen Rite failed to establish")
                if role=="B" and level==3:
                    adapter.arm_vital("low")
            elif actor_id=="foe":
                _foe(combat,opponent)
            combat.bridge.end_current_turn()
    if e.current is not None or e.cursor!=len(e.order) or combat.pending_attack_slots():
        raise AssertionError("No unresolved source attacks or turns allowed")
    e.check()
    report={"version":"B04-B05-Low-Life-Native-Exaltation-v0",
            "role":role,"level":level,"opponent":opponent,"seed":seed,
            "source_ids":{k:a.source.source_id for k,a in e.actors.items()},
            "source_digests":{k:a.source.digest for k,a in e.actors.items()},
            "metrics":_metrics(e,role),
            "ledger":deepcopy(e.ledger),
            "full_encounter_certified":False,
            "independent_focus_certified":False,
            "sampled_win_rate":None,"balance_approval":None}
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,role,level,opponent="soldier",seed=0):
    expected=run_policy(role=role,level=level,opponent=opponent,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Low native policy report fails source replay")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    cells=[run_policy(role=role,level=level,opponent=opponent,seed=seed)
           for role in ROLES for level in LEVELS for opponent in OPPONENTS]
    report={"seed":seed,"cells":cells,"cell_count":len(cells),
            "independent_focus_certified":False}
    report["audit_sha256"]=canonical_digest(report)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args()
    print(json.dumps(run_matrix(seed=args.seed),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
