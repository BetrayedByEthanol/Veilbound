"""B04/B05 Anointed three-Focus native G5 weapon plus Returning Step witness.

Two genuine G0 rounds; one sourced ordinary Anointed G5 melee and one
sourced enemy melee, plus one optional, source-native Returning Step.
The legal timing differs by Focus. These are bounded fixed policies,
not measured win rates or independently certified combat roles.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_anointed_native_melee_v0 import MELEE_IDS,anointed_weapon_profile
from scripts.b05_anointed_native_defensive_encounter_v0 import _one_enemy_hit
from scripts.b05_high_anointed_native_returning_step_v0 import HighAnointedRestoration
from scripts.b05_medium_anointed_native_returning_step_v0 import MediumAnointedRestoration
from scripts.b05_low_anointed_native_returning_step_v0 import LowAnointedRestoration
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

FOCUSES={"High":("AH",HighAnointedRestoration),
         "Medium":("AM",MediumAnointedRestoration),
         "Low":("AL",LowAnointedRestoration)}
OPPONENTS={"soldier":("B06-EN-02",None),
           "sentry_prepared":("B06-EN-01","prepared_start")}
LEVELS=(1,2,3)
POLICIES=("weapon_only","weapon_signature","weapon_lesser")
ROUNDS=2
D20=12
PLAYER_DAMAGE=4
WOUND_FACE=8
SIGNATURE_KIND={"High":"g4_anointed_returning_step_applied",
                "Medium":"g4_anointed_medium_returning_step_applied",
                "Low":"g4_anointed_low_returning_step_applied"}


def _validate(focus,level,opponent,policy,seed):
    if focus not in FOCUSES or opponent not in OPPONENTS or policy not in POLICIES:
        raise ValueError("Only source-backed Anointed weapon/Restoration policies")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only authored L1–3 Focus characters")
    if type(seed) is not int or seed<0:
        raise ValueError("Deterministic nonnegative seed required")


def run_policy(*,focus,level,opponent="soldier",policy="weapon_signature",seed=0):
    """One actual sourced weapon attack and one real recipient healing window."""
    _validate(focus,level,opponent,policy,seed)
    role,adapter=FOCUSES[focus]
    enemy_source,start=OPPONENTS[opponent]
    low=focus=="Low"
    caster=party_actor(role,level,"anointed","party",occupied=((2,2),))
    foe=enemy_actor(enemy_source,"foe","enemy",start_state=start,
                    occupied=((3,2),))
    actors=[caster,foe]
    if not low:
        # Adjacent to BOTH the actual G5 opponent and the source caster;
        # no hidden movement, remote Medium Vessel or manufactured G4 Step.
        actors.append(party_actor("F",level,"patient","party",
                                  occupied=((2,3),)))
    order=({"foe":40,"anointed":30} if low
           else {"anointed":40,"foe":30,"patient":20})
    e=Encounter(actors,order,seed=seed,
                scenario=f"B04-B05-Anointed-G5-Role-Choice:{focus}:{opponent}",
                objective="one_paid_weapon_one_real_enemy_hit_one_optional_signature",
                policy="two_round_source_declined_response_and_explicit_unopposed_restoration")
    GridMovement(e,width=7,height=7,scene_id="b05-anointed-weapon-and-beneficial-contact")
    RangedCombat(e,scene_id="b05-anointed-live-source-wielding")
    SpellState(e)
    DamageState(e)
    native=adapter(e,"anointed")
    combat=SourceMelee(e)
    recipient="anointed" if low else "patient"
    profile,bonus=anointed_weapon_profile(
        caster,MELEE_IDS[role],encounter=e)
    if bonus!=3:
        raise AssertionError("Source native mundane attack bonus drift")
    e.begin_round()
    e.log("b05_anointed_g5_role_policy",focus=focus,level=level,
          opponent=opponent,policy=policy,seed=seed,rounds=ROUNDS,
          weapon=MELEE_IDS[role],weapon_die=profile["primary_hp_packet"]["die"],
          attack_face=D20,damage_face=PLAYER_DAMAGE,
          enemy_attack_face=12,enemy_damage_face=2,sentry_vigor_die=1,
          spontaneous_responses="decline_all",
          healing="unopposed",medium_consent=True,
          natural_hp_regeneration=0,
          source_digests={name:a.source.digest for name,a in e.actors.items()})

    for rnd in range(1,ROUNDS+1):
        if rnd>1:
            combat.bridge.begin_next_round()
        for who in e.order:
            # Only real upcoming recipient G4 Steps may host the 0-AP
            # Medium/Low expressions, with declaration before start_turn.
            if (policy!="weapon_only" and rnd==1 and
                    who==recipient and focus in ("Medium","Low")):
                lesser=policy=="weapon_lesser"
                if focus=="Medium":
                    native.declare_pulse(recipient,lesser=lesser,
                                         visible=True,unopposed=True)
                else:
                    native.declare_pulse(lesser=lesser)
            combat.bridge.start_next_turn(RegenerationChoice())
            if e.current!=who or e.pending_regeneration is not None:
                raise AssertionError("Expected exact real G0 recipient Step")
            if who=="anointed":
                if (focus=="Medium" and rnd==1 and
                        policy!="weapon_only"):
                    # Medium L1 has 30 AP, so Investment (24) and
                    # physical weapon (24) CANNOT both be done here.
                    native.invest(recipient,consenting=True)
                if (focus=="High" and rnd==2 and
                        policy!="weapon_only"):
                    # Source High Projection is a paid 20-AP action,
                    # in a later turn than its Round-1 physical attack.
                    native.project(recipient,lesser=policy=="weapon_lesser",
                                   visible=True,unopposed=True)
                # High + Low attack Round 1, Medium baseline Round 1;
                # Medium Investment instead attacks Round 2. Never a
                # synthetic same-turn 48-AP Medium action combination.
                attack=(rnd==1 and (focus!="Medium" or
                        policy=="weapon_only")
                        or rnd==2 and focus=="Medium" and
                        policy!="weapon_only")
                if attack:
                    if not e.g1.melee_contact(who,"foe"):
                        raise AssertionError("G1/G2 real source weapon lost contact")
                    seq=combat.declare(who,"foe",profiles=(MELEE_IDS[role],),
                                       defenses=("take_hit",))
                    result=combat.resolve(seq,0,attack_face=D20,
                                          damage_face=PLAYER_DAMAGE,
                                          wound_location_roll=WOUND_FACE)
                    if result["outcome"]!="hit" or result["damage"] is None:
                        raise AssertionError("One source G5 weapon attack must resolve")
            elif who=="foe" and rnd==1:
                _one_enemy_hit(combat,opponent,recipient)
            combat.bridge.end_current_turn()
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots() or getattr(native,"pending",None) is not None):
        raise AssertionError("No pending G0/G5 or Signature claim at scene end")
    e.check()

    def ev(kind):
        return [x for x in e.ledger if x["kind"]==kind]
    player_hits=[x for x in ev("g5_melee_resolved")
                 if x["detail"]["attacker"]=="anointed"]
    enemy_hits=[x for x in ev("g5_melee_resolved")
                if x["detail"]["attacker"]=="foe"]
    signatures=ev(SIGNATURE_KIND[focus])
    recipient_steps=[x for x in ev("regeneration_step")
                     if x["detail"]["actor"]==recipient]
    all_signatures=[x for k in SIGNATURE_KIND.values() for x in ev(k)]
    if (len(player_hits)!=1 or len(enemy_hits)!=1
            or len(recipient_steps)!=2
            or len(all_signatures)!=int(policy!="weapon_only")
            or len(signatures)!=int(policy!="weapon_only")
            or [x["detail"]["hp_restored"] for x in recipient_steps]!=[0,0]
            or any(x["detail"]["outcome"]!="hit" for x in player_hits+enemy_hits)):
        raise AssertionError("Incorrect exact native weapon, injury or G4 Step provenance")
    cost=sum(x["detail"]["destiny_cost"] for x in signatures)
    if cost!=int(policy=="weapon_lesser") or cost!=2-native.state.destiny:
        raise AssertionError("Finite shared Destiny must only pay for sourced Signature")
    restored=sum(x["detail"]["hp_restored"] for x in signatures)
    if restored!=((2 if focus=="High" else 1) if policy!="weapon_only" else 0):
        raise AssertionError("Restoration must obey exact native Focus expression")
    signature_vigor=sum(x["detail"]["recipient_vigor_spent"] for x in signatures)
    if signature_vigor != (restored if policy=="weapon_signature" else 0):
        raise AssertionError("Lesser does not waive ordinary source VP or mint Vigor")
    report={
        "version":"B04-B05-Anointed-Native-Weapon-Signature-Choice-v0",
        "focus":focus,"level":level,"opponent":opponent,
        "policy":policy,"seed":seed,
        "metrics":{
            "recipient":recipient,
            "recipient_hp":e.actors[recipient].hp,
            "recipient_vigor":e.actors[recipient].vigor,
            "recipient_hp_max":e.actors[recipient].hp_max,
            "enemy_hp":foe.hp,"enemy_hp_max":foe.hp_max,
            "one_paid_g5_player_hit":len(player_hits),
            "one_paid_g5_enemy_hit":len(enemy_hits),
            "player_attack_round":player_hits[0]["round"],
            "player_source_profile":MELEE_IDS[role],
            "player_source_attack_bonus":bonus,
            "player_damage_die":profile["primary_hp_packet"]["die"],
            "source_signature_kind":SIGNATURE_KIND[focus],
            "signature_receipts":len(signatures),
            "signature_hp_restored":restored,
            "signature_recipient_vigor_spent":signature_vigor,
            "signature_destiny_spent":cost,
            "shared_destiny_remaining":native.state.destiny,
            "natural_hp_restored":sum(x["detail"]["hp_restored"] for x in recipient_steps),
            "recipient_regeneration_step_count":len(recipient_steps),
            "recipient_regeneration_rounds":[x["round"] for x in recipient_steps],
            "medium_investment_count":len(ev("b05_medium_anointed_investment_established")),
            "high_paid_projection_count":sum(1 for x in ev("action_committed")
                if x["detail"].get("label")=="anointed:high:returning_step"),
            "caster_vp_spent":caster.vp_spent,
            "caster_vp_committed":caster.vp_committed,
        },
        "source_ids":{name:a.source.source_id for name,a in e.actors.items()},
        "source_digests":{name:a.source.digest for name,a in e.actors.items()},
        "ledger":deepcopy(e.ledger),
        "independent_focus_certified":False,
        "representative_play_certified":False,
        "sampled_win_rate":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest_policy(report,*,focus,level,opponent="soldier",
                  policy="weapon_signature",seed=0):
    expected=run_policy(focus=focus,level=level,opponent=opponent,
                        policy=policy,seed=seed)
    if (not isinstance(report,dict)
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Unverified native G5 weapon or G4 Signature choice")
    return deepcopy(expected)


def run_matrix(*,seed=0):
    return [run_policy(focus=f,level=lv,opponent=o,policy=p,seed=seed)
            for f in FOCUSES for lv in LEVELS for o in OPPONENTS
            for p in POLICIES]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--focus",choices=tuple(FOCUSES),default="Low")
    parser.add_argument("--level",type=int,choices=LEVELS,default=3)
    parser.add_argument("--opponent",choices=tuple(OPPONENTS),default="soldier")
    parser.add_argument("--policy",choices=POLICIES,default="weapon_signature")
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--matrix",action="store_true")
    args=parser.parse_args()
    if args.matrix:
        cases=run_matrix(seed=args.seed)
        print(json.dumps({"cases":len(cases),"metrics":[
            {k:r[k] for k in ("focus","level","opponent","policy")}
            |r["metrics"] for r in cases]},indent=2))
    else:
        print(json.dumps(run_policy(focus=args.focus,level=args.level,
             opponent=args.opponent,policy=args.policy,seed=args.seed),indent=2))


if __name__=="__main__":
    main()
