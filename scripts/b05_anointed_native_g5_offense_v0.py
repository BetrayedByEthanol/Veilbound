"""B04/B05 source-native Anointed mundane melee G5 offensive witness v0.

AH/AM Dagger Pierce and AL Sword Cut, all L1–3, against one source Soldier
or prepared Sentry. Exactly one original G0-paid G5 ordinary weapon
hit and one source enemy reply; no spell-powered weapon, Opportunity,
retarget, full tactical combat or Focus certificate is implied.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_anointed_native_melee_v0 import MELEE_IDS,anointed_weapon_profile
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

FOCUSES={"High":"AH","Medium":"AM","Low":"AL"}
OPPONENTS={"soldier":("B06-EN-02",None,"B06-AT-03"),
           "sentry_prepared":("B06-EN-01","prepared_start","B06-AT-02")}
POLICIES=("hold","strike")
LEVELS=(1,2,3)
D20=12
PLAYER_DAMAGE=4  # one legal d4 Dagger face or d6 Sword face
ENEMY_SWORD_D6=2
SENTRY_VIGOR_D6=1
WOUND_LOCATION_D20=8


def _validate(focus,level,opponent,policy,seed):
    if focus not in FOCUSES or opponent not in OPPONENTS or policy not in POLICIES:
        raise ValueError("Only authored Anointed Focus / enemy / policy combinations")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only source-verified L1–3 builds")
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative deterministic source seed required")


def run_policy(*,focus,level,opponent="soldier",policy="strike",seed=0):
    _validate(focus,level,opponent,policy,seed)
    role=FOCUSES[focus]
    npc,state,npc_profile=OPPONENTS[opponent]
    hero=party_actor(role,level,"anointed","party",occupied=((2,2),))
    foe=enemy_actor(npc,"foe","enemy",start_state=state,occupied=((3,2),))
    e=Encounter([hero,foe],{"anointed":40,"foe":30},seed=seed,
                scenario=f"B04-B05-Anointed-Mundane-G5:{focus}:{opponent}",
                policy="single_sourced_ordinary_weapon_hit_then_one_enemy_reply",
                objective="genuine_ordinary_anointed_melee_not_focus_certificate")
    GridMovement(e,width=7,height=6,scene_id="b05-anointed-physical-contact")
    RangedCombat(e,scene_id="b05-anointed-real-weapon-readiness")
    SpellState(e)
    DamageState(e)
    combat=SourceMelee(e)
    attested_profile,bonus=anointed_weapon_profile(
        hero,MELEE_IDS[role],encounter=e)
    if (attested_profile["primary_hp_packet"]["die"]!=
            ("d6" if role=="AL" else "d4") or bonus!=3):
        raise AssertionError("Anointed sourced physical profile drift")
    e.begin_round()
    e.log("b05_anointed_melee_policy",focus=focus,level=level,
          opponent=opponent,policy=policy,seed=seed,
          attack_face=D20,player_damage_face=PLAYER_DAMAGE,
          enemy_damage_face=ENEMY_SWORD_D6,sentry_vigor_die=SENTRY_VIGOR_D6,
          defense="take_hit",source_profile=MELEE_IDS[role],
          source_digests={name:a.source.digest for name,a in e.actors.items()})
    for who in e.order:
        combat.bridge.start_next_turn(RegenerationChoice())
        if e.current!=who or e.pending_regeneration is not None:
            raise AssertionError("Authentic own-turn G0 Regeneration Step required")
        if who=="anointed" and policy=="strike":
            if not e.g1.melee_contact(who,"foe"):
                raise AssertionError("G1/G2 real wielded melee contact missing")
            seq=combat.declare(who,"foe",profiles=(MELEE_IDS[role],),
                               defenses=("take_hit",))
            outcome=combat.resolve(seq,0,attack_face=D20,
                                   damage_face=PLAYER_DAMAGE,
                                   wound_location_roll=WOUND_LOCATION_D20)
            if outcome["outcome"]!="hit" or outcome["damage"] is None:
                raise AssertionError("Anointed physical strike did not hit G4")
        elif who=="foe":
            if opponent=="sentry_prepared" and e.g3.sentry_profile(who)!=npc_profile:
                raise AssertionError("Actual Sentry prepared Reserve must be active")
            if not e.g1.melee_contact(who,"anointed"):
                raise AssertionError("Native Soldier/Sentry contact missing")
            seq=combat.declare(who,"anointed",profiles=(npc_profile,),
                               defenses=("take_hit",))
            extra={"vigor_die":SENTRY_VIGOR_D6} if opponent=="sentry_prepared" else {}
            outcome=combat.resolve(seq,0,attack_face=D20,
                                   damage_face=ENEMY_SWORD_D6,
                                   wound_location_roll=WOUND_LOCATION_D20,
                                   **extra)
            if outcome["outcome"]!="hit" or outcome["damage"] is None:
                raise AssertionError("G5 enemy reply did not resolve")
        combat.bridge.end_current_turn()
    if e.current is not None or e.cursor!=len(e.order) or combat.pending_attack_slots():
        raise AssertionError("No unresolved paid G0/G5 actions on complete round")
    e.check()
    player=[x for x in e.ledger if x["kind"]=="g5_melee_resolved"
            and x["detail"]["attacker"]=="anointed"]
    enemy=[x for x in e.ledger if x["kind"]=="g5_melee_resolved"
           and x["detail"]["attacker"]=="foe"]
    if (len(player)!=int(policy=="strike") or len(enemy)!=1
            or any(x["detail"]["outcome"]!="hit" for x in player+enemy)):
        raise AssertionError("Only one authored source strike and one enemy reply")
    reports={
        "version":"B04-B05-Anointed-Mundane-G5-Offense-v0",
        "focus":focus,"level":level,"opponent":opponent,"policy":policy,
        "seed":seed,
        "metrics":{
            "anointed_hp":hero.hp,"anointed_vigor":hero.vigor,
            "anointed_hp_max":hero.hp_max,"anointed_vigor_max":hero.vigor_max,
            "enemy_hp":foe.hp,"enemy_vigor":foe.vigor,
            "enemy_hp_max":foe.hp_max,
            "player_attack_profile":MELEE_IDS[role],
            "player_attack_bonus":bonus,
            "player_weapon_damage_die":attested_profile["primary_hp_packet"]["die"],
            "player_g0_paid_physical_actions":len(
                [v for v in e.ledger if v["kind"]=="action_committed"
                 and v["detail"]["actor"]=="anointed"]),
            "player_g5_hits":len(player),
            "enemy_g5_hits":len(enemy),
            "player_g4_damage_events":len(
                [x for x in e.ledger if x["kind"]=="g4_profile_hit"
                 and x["detail"]["attacker"]=="anointed"]),
            "enemy_g4_damage_events":len(
                [x for x in e.ledger if x["kind"]=="g4_profile_hit"
                 and x["detail"]["attacker"]=="foe"]),
            "recipient_regeneration_steps":len(
                [x for x in e.ledger if x["kind"]=="regeneration_step"
                 and x["detail"]["actor"]=="anointed"]),
            "source_weapon_still_wielded":attested_profile["id"]==MELEE_IDS[role],
            "native_signature_or_authority_spent":False,
        },
        "source_digests":{name:a.source.digest for name,a in e.actors.items()},
        "source_ids":{name:a.source.source_id for name,a in e.actors.items()},
        "ledger":deepcopy(e.ledger),
        "independent_focus_certified":False,
        "representative_play_certified":False,
        "sampled_win_rate":None,
    }
    reports["ledger_sha256"]=canonical_digest(reports["ledger"])
    return reports


def attest_policy(report,*,focus,level,opponent="soldier",policy="strike",seed=0):
    expected=run_policy(focus=focus,level=level,opponent=opponent,
                        policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Forged or incomplete native Anointed physical G5 receipt")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    return [run_policy(focus=f,level=lv,opponent=o,policy=p,seed=seed)
            for f in FOCUSES for lv in LEVELS for o in OPPONENTS for p in POLICIES]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--focus",choices=tuple(FOCUSES),default="Low")
    parser.add_argument("--level",type=int,choices=LEVELS,default=3)
    parser.add_argument("--opponent",choices=tuple(OPPONENTS),default="soldier")
    parser.add_argument("--policy",choices=POLICIES,default="strike")
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--matrix",action="store_true")
    args=parser.parse_args()
    if args.matrix:
        rows=run_matrix(seed=args.seed)
        print(json.dumps({"cases":len(rows),"metrics":[
            {k:r[k] for k in ("focus","level","opponent","policy")}
            |r["metrics"] for r in rows]},indent=2))
    else:
        print(json.dumps(run_policy(focus=args.focus,level=args.level,
                opponent=args.opponent,policy=args.policy,seed=args.seed),indent=2))


if __name__=="__main__":
    main()
