"""B04/B05/B06 Alpha mixed L1 Soldier contact and source-paid withdrawal.

One AUTHORED GM policy, not generic player-choice AI or actual external play.
Four genuine full selected Focus source identities (including A/B Low Life),
one original unchanged Soldier and native G0/G1/G2/G3/G4/G5 state.
"""
from copy import deepcopy
import json

from scripts.b05_low_life_native_rites_v0 import (
    LowLifeNativeRites,full_low_priest_actor,FULL_SOURCE,FULL_STATUS,
)
from scripts.b05_high_gifted_native_encounter_v0 import (
    GiftedNative,gifted_actor,
)
from scripts.b05_medium_anointed_native_returning_step_v0 import MediumAnointedRestoration
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee,SceneExit
from scripts.b06_g7a_native_terminal_census_v0 import _snapshot,canonical_digest

VERSION="B04-B05-B06-Alpha-Four-Focus-L1-Soldier-v0"
PARTY=("anointed","priest","gifted","scholar")
FOCUSES={"anointed":"Anointed/Medium","priest":"Priest/Low",
         "gifted":"Gifted/High","scholar":"Scholar/High"}
POSITIONS={"anointed":(1,3),"priest":(3,2),
           "gifted":(3,5),"scholar":(1,5)}
EXIT_STEPS={"anointed":((-1,0),),
            "priest":((0,-1),(0,-1)),
            "gifted":((0,1),),
            "scholar":((-1,0),)}
EXIT_SQUARES={"anointed":(0,3),"priest":(3,0),
              "gifted":(3,6),"scholar":(0,5)}
FOE=(4,2)
MAX_ROUNDS=2


def _validate(variant,seed):
    if variant not in ("A","B"):
        raise ValueError("Choose one actual full Low Life Priest A/B sheet")
    if type(seed) is not int or seed<0:
        raise ValueError("Explicit nonnegative integer native seed required")


def scene(*,variant="A",seed=0,native_initiative_clock=False):
    """Build true source actors; optional G4.2 entry precedes first Round Begin.

    The opt-in keeps existing standalone #199/#200 source witnesses unchanged.
    Persistent L1->L3 progression must use this real clock mode so each
    completed L1 round debits its native Recovery deadline.
    """
    _validate(variant,seed)
    if type(native_initiative_clock) is not bool:
        raise ValueError("Explicit native initiative-clock option required")
    actors=[
        anointed:=party_actor("AM",1,"anointed","party",
                             occupied=(POSITIONS["anointed"],)),
        priest:=full_low_priest_actor(variant,1,"priest","party",
                                     occupied=(POSITIONS["priest"],)),
        gifted:=gifted_actor(1,"gifted","party",
                            occupied=(POSITIONS["gifted"],)),
        scholar:=party_actor("F",1,"scholar","party",
                            occupied=(POSITIONS["scholar"],)),
        enemy_actor("B06-EN-02","foe","enemy",occupied=(FOE,)),
    ]
    # These are explicit authored rolled initiative inputs, NOT an automatic
    # universal initiative bonus or a deterministic-player choice engine.
    scores={"anointed":50,"foe":40,"priest":30,"gifted":20,"scholar":10}
    e=Encounter(actors,scores,seed=seed,scenario="Alpha-L1-Soldier-Gate",
                policy="author_fixture_support_then_opposed_native_withdrawal",
                objective="source_bounded_actual_L1_mixed_party_contact_and_exit")
    GridMovement(e,width=8,height=7,scene_id="Alpha-L1-open-gate")
    RangedCombat(e,scene_id="Alpha-L1-sourced-weapons-and-flame-lanes")
    SpellState(e)
    DamageState(e)
    low=LowLifeNativeRites(e,"priest")
    joy=GiftedNative(e,"gifted")
    investment=MediumAnointedRestoration(e,"anointed")
    exits=tuple(SceneExit(
        e.scenario,e.g1.scene_id,e.objective,n,EXIT_SQUARES[n],
        "Alpha:L1:"+n+":cautious") for n in PARTY)
    combat=SourceMelee(e,scene_exits=exits,
                       player_benchmark_target="foe")
    if e.order!=("anointed","foe","priest","gifted","scholar"):
        raise AssertionError("Alpha turn/recipient Step order changed")
    if (priest.source.path!=FULL_SOURCE or priest.source.status!=FULL_STATUS
            or priest.source.attack_profiles or
            any(e.actors[n].level!=1 for n in PARTY)
            or e.actors["foe"].level!=3 or
            e.actors["foe"].source.source_id!="B06-EN-02"
            or gifted.source.source_id!="G"
            or anointed.source.source_id!="AM"):
        raise AssertionError("Selected full Focus source or enemy benchmark drift")
    if native_initiative_clock:
        e.g4.clock.enter_initiative()
    e.begin_round()
    e.log("b04_b05_b06_alpha_native_source_policy",
          variant=variant,level=1,opponent_level=3,
          selected_focuses=dict(FOCUSES),
          real_L1_source={n:{"source_id":e.actors[n].source.source_id,
                            "path":e.actors[n].source.path,
                            "digest":e.actors[n].source.digest}
                          for n in PARTY},
          author_fixture_only=True,no_human_play=True,
          no_proxy_priest=True,no_downleveled_enemy=True)
    return combat,low,joy,investment


def _enemy(combat,face):
    e=combat.e
    if not e.g1.melee_contact("foe","priest"):
        raise UnresolvedDecision("Soldier must threaten genuine source Priest")
    declaration=combat.declare("foe","priest",profiles=("B06-AT-03",),
                               defenses=("take_hit",))
    kwargs={"attack_face":face}
    if face!=1:
        kwargs.update(damage_face=2,wound_location_roll=8)
    result=combat.resolve(declaration,0,**kwargs)
    if result["outcome"]!=("miss" if face==1 else "hit"):
        raise AssertionError("Soldier actual G5 hit/miss policy contradicted source")
    return result


def _round_one(combat,low,joy,investment):
    e=combat.e
    first_hp=e.actors["priest"].hp
    hits=[]
    for who in e.order:
        if who=="priest":
            # Medium's one-Vessel declaration is allowed only immediately
            # before the real upcoming Priest Step, never manufactured.
            investment.declare_pulse("priest",lesser=False,
                                      visible=True,unopposed=True)
        combat.bridge.start_next_turn(RegenerationChoice())
        if who=="anointed":
            receipt=investment.invest("priest",consenting=True)
            if receipt["ap_spent"]!=24:
                raise AssertionError("L1 Medium Anointed must pay true General AP")
        elif who=="foe":
            hits.append(_enemy(combat,12))
        elif who=="priest":
            if low.cast_chosen("priest",chosen=True) is None:
                raise AssertionError("Chosen Low Priest native G3 host missing")
        elif who=="gifted":
            joy.establish("Joy")
            result=joy.cast_flame("foe",tier=1,face=1,vigor_die=3,
                                  hand_available=True)
            if result["outcome"]!="automatic_miss" or result["vp_spent"]<=0:
                raise AssertionError("Gifted failed source-paid native Thrown Flame")
        elif who=="scholar":
            result=e.g3.cast_flame("scholar","foe",tier=1,face=1,vigor_die=3,
                                   defense="take_hit",hand_available=True)
            if result["outcome"]!="automatic_miss":
                raise AssertionError("Scholar must pay native Flame miss")
        combat.bridge.end_current_turn()
    if (len(hits)!=1 or e.actors["priest"].hp>=first_hp
            or not any(x["kind"]=="g4_anointed_medium_returning_step_applied"
                       for x in e.ledger)):
        raise AssertionError("G5 real wound and native recipient Step both required")


def _round_two(combat):
    e=combat.e
    combat.bridge.begin_next_round()
    for who in e.order:
        combat.bridge.start_next_turn(RegenerationChoice())
        if who=="foe":
            _enemy(combat,1)
        else:
            for delta in EXIT_STEPS[who]:
                if not e.g1.step(who,delta,cautious=True,
                                 responses=lambda eligible: ()):
                    raise UnresolvedDecision("Alpha sourced cautious withdrawal canceled")
            combat.withdraw(who)
        combat.bridge.end_current_turn()
    exits=[x for x in e.ledger if x["kind"]=="g5_terminal_exit"]
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots() or len(exits)!=4
            or {x["detail"]["actor"] for x in exits}!=set(PARTY)
            or any(e.actors[n].hp<=0 or e.actors[n].dead for n in PARTY)
            or e.actors["foe"].dead):
        raise AssertionError("No authenticated mixed-party opposed scene exit")
    return "party_scene_withdrawal"


def run(*,variant="A",seed=0):
    combat,low,joy,investment=scene(variant=variant,seed=seed)
    e=combat.e
    _round_one(combat,low,joy,investment)
    after_round_one=_snapshot(e)
    terminal=_round_two(combat)
    e.check()
    def events(kind):
        return [x for x in e.ledger if x["kind"]==kind]
    if (len(events("b05_low_rite_established"))!=1
            or len(events("b05_medium_anointed_investment_established"))!=1
            or len(events("g4_anointed_medium_returning_step_applied"))!=1
            or len(events("b05_gifted_emotion_established"))!=1
            or len(events("g3_flame_launched"))!=2
            or len(events("g5_melee_resolved"))!=2
            or len(events("g5_terminal_exit"))!=4):
        raise AssertionError("Every Alpha Focus, enemy contact and scene exit must be paid")
    report={
        "version":VERSION,"variant":variant,"seed":seed,"level":1,
        "opponent_source":"B06-EN-02","opponent_level":3,
        "party_focuses":dict(FOCUSES),
        "source_digests":{n:e.actors[n].source.digest for n in e.actors},
        "source_paths":{n:e.actors[n].source.path for n in e.actors},
        "actual_full_low_priest_source":True,
        "native_low_chosen_hosts":1,
        "native_anointed_investments":1,
        "native_anointed_recipient_steps":1,
        "native_gifted_emotion_windows":1,
        "native_paid_flame_launches":2,
        "native_enemy_melee_resolutions":2,
        "native_party_exits":4,
        "rounds":e.round,
        "end_of_round_one":after_round_one,
        "final_state":_snapshot(e),
        "final_vp_totals":{n:{"max":a.vp_max,"available":a.vp_available,
                               "committed":a.vp_committed,"spent":a.vp_spent}
                           for n,a in e.actors.items() if n in PARTY},
        "terminal":terminal,
        "ledger":deepcopy(e.ledger),
        "human_sessions":0,
        "independent_full_focus_certificates":0,
        "strict_mvp_exits_met":0,
        "representative_encounter_calibrated":False,
        "universal_alpha_encounter_engine":False,
        "hunter_cr":None,
    }
    report["ledger_sha256"]=canonical_digest(report["ledger"])
    return report


def attest(report,*,variant="A",seed=0):
    """Exact native replay: no caller-defined terminal, costs or new opponent."""
    _validate(variant,seed)
    expected=run(variant=variant,seed=seed)
    if (type(report) is not dict
            or report.get("ledger_sha256")!=canonical_digest(report.get("ledger"))
            or report!=expected):
        raise AssertionError("Alpha source-native witness differs from current replay")
    return deepcopy(expected)


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--variant",choices=("A","B"),default="A")
    p.add_argument("--seed",type=int,default=0)
    a=p.parse_args()
    print(json.dumps({k:v for k,v in run(variant=a.variant,seed=a.seed).items()
                      if k!="ledger"},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
