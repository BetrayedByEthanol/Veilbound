"""B04/B05 source-native Medium/Low Scholar Sword offense and readiness v0.

G0 pays and declares an entire real G5 Sword Cut sequence, with G1/G2
wielded contact, G4 typed HP damage, G4.5 receipts and exact Soldier
retaliation. Medium Inward and Low Embodiment retain their independent
native G3 hosts and G0 Step2. This is a two-round bounded scene,
not a full fight verdict or generic equipment-enchantment API.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_scholar_native_sword_v0 import (
    SWORD_IDS,scholar_sword_profile,
)
from scripts.b05_medium_scholar_native_inward_v0 import MediumScholarInward
from scripts.b05_low_scholar_native_embodiment_v0 import LowScholarEmbodiment
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

FOCUSES={"Medium":"S","Low":"T"}
LEVELS=(1,2,3)
POLICIES=("baseline","stone","guided","double")
ROUNDS=2
ATTACK_FACE=12
DAMAGE_FACE=4
SOLDIER_FACE=12
SOLDIER_D6=4
WOUND_FACE=8


def _allocation(e,who):
    a=e.actors[who]
    # One author-declared regeneration allocation after the *real* previous
    # native G4 damage. Soldier elects to conserve Vigor in this probe.
    if who=="foe":
        return RegenerationChoice()
    rate=max(0,a.regen+e.g3.regen_throughput(who)+
             e.g4.toxins.modifier(who,"regen_throughput"))
    return RegenerationChoice(
        hp=min(max(0,a.hp_max-a.hp),a.vigor,rate) if a.hp>0 else 0,
        cancel_dying_loss=(a.hp<=0 and not a.dead and a.vigor>0))


def run_case(*,focus,level,policy,seed=0):
    if focus not in FOCUSES or type(level) is not int or level not in LEVELS:
        raise ValueError("Only selected Medium/Low Scholar L1–3")
    if policy not in POLICIES or (policy=="double"
                                and not (focus=="Low" and level==3)):
        raise ValueError("Only L3 Low can fund two actual Sword Physical Actions")
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative deterministic encounter seed required")
    role=FOCUSES[focus]
    scholar=party_actor(role,level,"scholar","party",occupied=((2,2),))
    foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    e=Encounter([scholar,foe],{"scholar":40,"foe":30},seed=seed,
        scenario="B04-B05-Scholar-Native-Sword-Soldier-v0",
        policy="fixed_two_round_sword_and_optional_self_inward",
        objective="native_physical_offense_and_readiness_not_terminal_CR")
    GridMovement(e,width=7,height=7,scene_id="b05-scholar-sword-contact")
    RangedCombat(e,scene_id="b05-scholar-live-wielding")
    SpellState(e)
    DamageState(e)
    adapter=(MediumScholarInward(e,"scholar") if focus=="Medium"
             else LowScholarEmbodiment(e,"scholar"))
    combat=SourceMelee(e)
    if e.order!=("scholar","foe"):
        raise AssertionError("Fixed source Initiative changed")
    native=scholar_sword_profile(scholar,SWORD_IDS[role],encounter=e)
    if native[1]!=7:
        raise AssertionError("Native Sword source bonus differs")
    e.begin_round()
    e.log("b05_scholar_sword_policy",focus=focus,level=level,policy=policy,
          seed=seed,horizon=ROUNDS,
          source_digests={a.id:a.source.digest for a in e.actors.values()},
          initial_attack_face=ATTACK_FACE,damage_die=DAMAGE_FACE,
          soldier_attack_face=SOLDIER_FACE,soldier_die=SOLDIER_D6,
          defense="take_hit",wound_location_roll=WOUND_FACE)
    for rnd in range(1,ROUNDS+1):
        if rnd>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            a=e.actors[who]
            combat.bridge.start_next_turn(_allocation(e,who))
            if who=="scholar" and a.hp>0:
                if rnd==1 and policy in ("stone","guided"):
                    ident=(
                        ("MS-STONE-BODY-T1" if policy=="stone" else
                         "MS-GUIDED-REGEN-T1") if focus=="Medium" else
                        ("LS-STONE-BODY-T1" if policy=="stone" else
                         "LS-GUIDED-REGEN-T1"))
                    adapter.activate(ident)
                else:
                    if not e.g1.melee_contact("scholar","foe"):
                        raise AssertionError("Ready Sword lacks G1 contact")
                    count=2 if rnd==1 and policy=="double" else 1
                    seq=combat.declare("scholar","foe",
                        profiles=(SWORD_IDS[role],)*count,
                        defenses=("take_hit",)*count)
                    for slot in range(count):
                        if foe.dead:
                            raise AssertionError("Authored full sequence overshoots dead target")
                        hit=combat.resolve(seq,slot,attack_face=ATTACK_FACE,
                            damage_face=DAMAGE_FACE,
                            wound_location_roll=WOUND_FACE)
                        if hit["outcome"]!="hit" or hit["damage"] is None:
                            raise AssertionError("Real sourced Scholar Sword did not hit")
            elif who=="foe" and not scholar.dead and foe.hp>0:
                if not e.g1.melee_contact("foe","scholar"):
                    raise AssertionError("Soldier sword lost native G1 contact")
                seq=combat.declare("foe","scholar",
                    profiles=("B06-AT-03",),defenses=("take_hit",))
                result=combat.resolve(seq,0,attack_face=SOLDIER_FACE,
                    damage_face=SOLDIER_D6,
                    wound_location_roll=WOUND_FACE)
                if result["outcome"]!="hit":
                    raise AssertionError("Original Soldier retaliation hit changed")
            combat.bridge.end_current_turn()
    if e.current is not None or combat.pending_attack_slots():
        raise AssertionError("G0/G5 pending sequence cannot count as finished")
    e.check()
    def ev(kind):
        return [x for x in e.ledger if x["kind"]==kind]
    attacks=[v for v in ev("g5_melee_resolved")
             if v["detail"]["attacker"]=="scholar"]
    g4s=[v for v in ev("g4_damage_applied")
         if v["detail"]["cause"]==f"source-profile:{SWORD_IDS[role]}"]
    foe_attacks=[v for v in ev("g5_melee_resolved")
                 if v["detail"]["attacker"]=="foe"]
    actions=[v for v in ev("action_committed")
             if v["detail"]["actor"]=="scholar"]
    steps=[v for v in ev("regeneration_step")
           if v["detail"]["actor"]=="scholar"]
    expected=3 if policy=="double" else 1 if policy in ("stone","guided") else 2
    if (len(attacks)!=expected or len(g4s)!=expected
            or any(x["detail"]["outcome"]!="hit" for x in attacks)):
        raise AssertionError("Incorrect native Scholar Sword outcome count")
    for x in g4s:
        if x["detail"]["recipient"]!="foe":
            raise AssertionError("Scholar G4 source hit has wrong recipient")
    report={
        "version":"B04-B05-Scholar-Native-Physical-Sword-v0",
        "focus":focus,"level":level,"policy":policy,"seed":seed,
        "source_digests":{k:a.source.digest for k,a in e.actors.items()},
        "inputs":{"rounds":ROUNDS,"foe":"B06-EN-02",
                  "scholar_attack_face":ATTACK_FACE,
                  "scholar_damage_face":DAMAGE_FACE,
                  "soldier_attack_face":SOLDIER_FACE,
                  "soldier_damage_face":SOLDIER_D6,
                  "defense":"take_hit"},
        "metrics":{
            "scholar_sword_hits":len(attacks),
            "scholar_sword_g4_receipts":len(g4s),
            "scholar_source_attack_bonus":native[1],
            "physical_ap_paid":sum(x["detail"]["ap_spent"] for x in actions
                if x["detail"]["action_class"]=="physical"),
            "projection_ap_paid":sum(x["detail"]["ap_spent"] for x in actions
                if x["detail"]["action_class"]=="projection"),
            "active_scholar_profile":(
                adapter._current_ident() if focus=="Medium"
                else adapter.current_profile()),
            "soldier_sword_hits":len(foe_attacks),
            "scholar_true_steps":len(steps),
            "scholar_hp_restored":sum(x["detail"]["hp_restored"]
                                      for x in steps),
            "scholar_hp":scholar.hp,"scholar_vigor":scholar.vigor,
            "scholar_vp":[scholar.vp_available,scholar.vp_committed,
                          scholar.vp_spent],
            "foe_hp":foe.hp,"foe_vigor":foe.vigor,
            "foe_dead":foe.dead,
        },
        "ledger":deepcopy(e.ledger),
        "native_source_sword_only":True,
        "wielding_checked_live":True,
        "no_weapon_enchantment":True,
        "full_focus_certified":False,
        "numerical_tuning_authorized":False,
        "win_rate":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_case(report,*,focus,level,policy,seed=0):
    expected=run_case(focus=focus,level=level,policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Native Sword source or completed G5 policy drift")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative case seed required")
    cases=[run_case(focus=focus,level=level,policy=policy,seed=seed)
           for level in LEVELS for focus in FOCUSES for policy in POLICIES
           if policy!="double" or (level==3 and focus=="Low")]
    summaries=[{k:v for k,v in c.items() if k!="ledger"} for c in cases]
    result={
        "version":"B04-B05-Medium-Low-Scholar-Native-Sword-Matrix-v0",
        "seed":seed,"cases":summaries,"count":len(summaries),
        "full_focus_certified":False,
        "numerical_tuning_authorized":False,
        "statistical_win_rate":None,
    }
    result["audit_sha256"]=canonical_digest(result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--focus",choices=FOCUSES)
    p.add_argument("--level",type=int,choices=LEVELS)
    p.add_argument("--policy",choices=POLICIES)
    p.add_argument("--seed",type=int,default=0)
    a=p.parse_args()
    if len([v for v in (a.focus,a.level,a.policy) if v is not None]) not in (0,3):
        p.error("Provide focus, level and policy as one group")
    report=(run_case(focus=a.focus,level=a.level,policy=a.policy,seed=a.seed)
            if a.focus is not None else run_matrix(seed=a.seed))
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))


if __name__=="__main__":
    main()
