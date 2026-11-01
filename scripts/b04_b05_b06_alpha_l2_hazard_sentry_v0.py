"""Alpha L2 Hunter venom/Endurance -> live same-level Sentry damage and hazard carry.

This supplements, but does NOT replace, the clean L1->L3 milestone chain:
real unresolved live venom/Endurance prohibits an automatic L2->L3 award.
No source authority for Low Priest A to cast the B-only Venom Endurance.
"""
from copy import deepcopy
import json

from scripts.b04_b05_b06_alpha_l2_l3_progression_v0 import (
    PARTY, _scene, _begin, _start, _exit, _terminal, _carry, _state,
    award, candidate_awards,
)
from scripts.b05_low_priest_life_l1_l3_v0 import profile as priest_profile
from scripts.b05_b06_cross_encounter_effect_continuity_v0 import (
    effect_state, validate_source,
)
from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION="B04-B05-B06-Alpha-L2-Hunter-Venom-Endurance-Sentry-Handoff-v0"


def _hunter_contact(combat):
    e=combat.e
    if not e.g1.melee_contact("foe","priest",hunter_front=True):
        raise UnresolvedDecision("Original Hunter head-to-priest contact required")
    seq=combat.declare("foe","priest",profiles=("B06-AT-04",),
                       defenses=("take_hit",))
    # Source damage: 3+d6 Piercing Pen1. The G5/G4.4 adapter decides
    # whether actual HP penetration delivers native venom, not caller flags.
    return combat.resolve(seq,0,attack_face=12,damage_face=6,
                          venom_resistance_die=1,wound_location_roll=8)


def _priest_endurance(combat,variant):
    """Only actual L2 B has prepared the independently sourced Life Prayer."""
    e=combat.e
    p=priest_profile(variant,2)
    if "Venom Endurance" not in p["prepared_prayers"]:
        raise UnresolvedDecision("Selected A does not know/prep Venom Endurance at L2")
    caster=e.actors["priest"]
    if (caster.source.source_id!=variant
            or caster.level!=2 or caster.source.path!=
            "scripts/b05_low_priest_life_l1_l3_v0.py"
            or e.g4.toxins.active("priest") is None):
        raise UnresolvedDecision("Only genuine native selected B source after verified Bite")
    ident=e.g4.venom.cast_endurance(
        "priest","priest",profile="Self",mode="suppression",
        source_authorized=True,
        source_reference="selected-B-L2:"+caster.source.digest+
                         ":prepared:Venom Endurance",
        ordinary_cost=2,discount_authorized=False,unopposed=True)
    if ident is None:
        raise AssertionError("Selected B must fund one native Endurance suppression")
    return ident


def _hunter_scene(variant,seed):
    combat,_,_,_=_scene(2,variant,"hunter",seed)
    e=combat.e
    _begin(combat)
    before_hp=e.actors["priest"].hp
    endurance=None
    for round_no in (1,2):
        if round_no==2:
            combat.bridge.begin_next_round()
        for who in e.order:
            _start(combat,who)
            if who=="foe":
                if round_no==1:
                    result=_hunter_contact(combat)
                    if result["outcome"]!="hit":
                        raise AssertionError("Native Hunter Bite required")
                else:
                    seq=combat.declare("foe","priest",
                                       profiles=("B06-AT-04",),
                                       defenses=("take_hit",))
                    result=combat.resolve(seq,0,attack_face=1)
                    if result["outcome"]!="miss":
                        raise AssertionError("Second native Bite must miss")
            elif who=="priest" and round_no==1 and variant=="B":
                endurance=_priest_endurance(combat,variant)
            elif round_no==2 and who in PARTY:
                _exit(combat,who)
            combat.bridge.end_current_turn()
    outcome=_terminal(combat,"hunter")
    if (outcome!="party_scene_withdrawal"
            or e.actors["priest"].hp>=before_hp
            or len([x for x in e.ledger
                    if x["kind"]=="g44_hunter_accepted"])!=1):
        raise AssertionError("G4 source HP breach and accepted Hunter venom required")
    current=e.g4.toxins.active("priest")
    if (current is None or current["profile"]!="B06-TX-HUNTER-SLOW-MY"
            or current["result"]!="Full" or current["stage"]!=0):
        raise AssertionError("Original Hunter toxin stage not instantiated")
    if variant=="B" and endurance not in e.g4.venom.effects:
        raise AssertionError("Selected B's paid suppression has no native identity")
    if variant=="A" and e.g4.venom.effects:
        raise AssertionError("Selected A has no Venom Endurance preparation")
    validate_source(e,party=PARTY)
    return combat,endurance


def _sentry_scene(combat):
    """L2 source Sentry: real paid Reserve -> real weapon+Fire+Vigor hit."""
    e=combat.e
    _begin(combat)
    prior=e.actors["priest"].hp
    for round_no in (1,2):
        if round_no==2:
            combat.bridge.begin_next_round()
        for who in e.order:
            choice=RegenerationChoice()
            # The Priest can elect native source regeneration at Step 2
            # to protect against real incoming sword+Fire; this is a
            # declared HP allocation, never a free cross-scene refill.
            if who=="priest" and round_no==1:
                a=e.actors["priest"]
                choice=RegenerationChoice(
                    hp=min(3,max(0,a.hp_max-a.hp),a.vigor))
            combat.bridge.start_next_turn(choice)
            if who=="foe":
                if round_no==1:
                    if e.g3.cast_sentry_reserve("foe") is None:
                        raise AssertionError("Sentry original Chosen Reserve not paid")
                else:
                    if e.g3.sentry_profile("foe")!="B06-AT-02":
                        raise AssertionError("Actual sword Reserve absent")
                    seq=combat.declare("foe","priest",
                                       profiles=("B06-AT-02",),
                                       defenses=("take_hit",))
                    result=combat.resolve(seq,0,attack_face=12,
                                          damage_face=1,vigor_die=1,
                                          wound_location_roll=8)
                    if result["outcome"]!="hit":
                        raise AssertionError("Sentry must resolve original G4 Fire/Vigor hit")
            elif round_no==2 and who in PARTY:
                _exit(combat,who)
            combat.bridge.end_current_turn()
    outcome=_terminal(combat,"sentry_cold")
    if (outcome!="party_scene_withdrawal"
            or not any(x["kind"]=="g5_melee_resolved"
                       and x["detail"].get("profile")=="B06-AT-02"
                       and x["detail"].get("outcome")=="hit" for x in e.ledger)):
        raise AssertionError("Native paid enhanced Sentry hit/party exit absent")
    validate_source(e,party=PARTY)
    return prior


def run(*,variant="B",seed=0,travel_seconds=12):
    if variant not in ("A","B") or type(seed) is not int or seed<0:
        raise ValueError("Only genuine selected Alpha A/B sources")
    if type(travel_seconds) is not int or not 0<=travel_seconds<=30:
        raise ValueError("Same-level live Venom/Endurance handoff limited to 0–30s")
    hunter,effect_id=_hunter_scene(variant,seed)
    source=hunter.e
    origin=effect_state(source,party=PARTY)
    prior=_state(source)
    next_combat,_,_,_=_scene(2,variant,"sentry_cold",seed+1)
    # Same exact level and source, no milestone. Genuine recovery/timed
    # toxin/Endurance clocks survive instead of silently dropping host.
    handoff=_carry(source,next_combat.e,travel_seconds=travel_seconds,
                   reference="ALPHA-VERIFIED-HUNTER-BITE:forest-to-watch",
                   carry_hazards=True)
    imported=effect_state(next_combat.e,party=PARTY)
    if (origin["unified_instances"]["priest"]["key"]!=
            imported["unified_instances"]["priest"]["key"]
            or origin["hunter_keys"]!=imported["hunter_keys"]
            or origin["exposure_ids"]!=imported["exposure_ids"]
            or origin["endurance_effects"]!=imported["endurance_effects"]
            or handoff["before_hazard_sha256"]!=canonical_digest(origin)
            or handoff["after_hazard_sha256"]!=canonical_digest(imported)):
        raise AssertionError("Original Bite/Endurance source not preserved")
    at_start=_state(next_combat.e)
    if prior["priest"]["hp"]!=at_start["priest"]["hp"]:
        raise AssertionError("Poison handoff cannot refill source HP")
    prior_hp=_sentry_scene(next_combat)
    post=effect_state(next_combat.e,party=PARTY)
    after_sentry=_state(next_combat.e)
    if not next_combat.e.g4.toxins.active("priest"):
        raise AssertionError("Hunter venom disappeared during native Sentry")
    # This stage cannot grant the shrine award with unresolved live toxin.
    attempted=False
    try:
        award(next_combat.e,candidate_awards()[1],variant=variant)
    except UnresolvedDecision:
        attempted=True
    if not attempted:
        raise AssertionError("Active venom incorrectly permitted cross-level award")
    # Native G4.2 exploration time drives both Endurance expiry and Hunter
    # long-stage onset. No synthetic player turn or rewritten timer.
    timeline=next_combat.e.g4.clock
    # Native venom onset is anchored to original Bite's source-clock time.
    marker=next_combat.e.g4.clock.events[
        next_combat.e.g4.toxins.active("priest")["markers"][0]]
    remaining=marker.due_seconds-timeline.world_seconds
    if remaining<1:
        raise AssertionError("Venom native onset expected in source future")
    timeline.advance_exploration(remaining)
    after_onset=effect_state(next_combat.e,party=PARTY)
    toxin=next_combat.e.g4.toxins.active("priest")
    if (toxin is None or toxin["stage"]!=1
            or after_onset["modifiers"]["priest"].get("mp")!=-2):
        raise AssertionError("Original Hunter onset must apply native -2 MP")
    expected_event=next_combat.e.g4.clock.events[toxin["markers"][-1]]
    expiry_delta=expected_event.due_seconds-timeline.world_seconds
    if expiry_delta<1:
        raise AssertionError("Original expiry remains due")
    timeline.advance_exploration(expiry_delta)
    expired=effect_state(next_combat.e,party=PARTY)
    if (next_combat.e.g4.toxins.active("priest") is not None
            or expired["modifiers"]["priest"]
            or any(x["active"] for x in expired["endurance_effects"].values())):
        raise AssertionError("Native Hunter expiry must remove penalties and support")
    def ledger(e):
        return {"sha256":canonical_digest(e.ledger),"events":deepcopy(e.ledger)}
    report={
        "version":VERSION,"variant":variant,"seed":seed,
        "source_roster":{n:source.actors[n].source.source_id for n in PARTY},
        "hunter_profile":"B06-AT-04","sentry_profile":"B06-AT-02",
        "hunter_victim_HP_after":prior["priest"]["hp"],
        "endurance_effect":effect_id,
        "hunter_native_hazard":origin,
        "hazard_imported":imported,
        "sentry_initial_HP":prior_hp,
        "sentry_native_hazard":post,
        "sentry_exit_party":after_sentry,
        "onset_hazard":after_onset,
        "expiry_hazard":expired,
        "handoff":handoff,
        "milestone_blocked":attempted,
        "source_ledgers":{"hunter":ledger(source),"sentry":ledger(next_combat.e)},
        "native_mixed_level":2,
        "human_sessions":0,"actual_GM_milestones_authenticated":0,
        "independently_certified_focuses":0,"strict_mvp_exits_met":0,
        "cross_level_live_effect_rebind":False,
        "representative_Hunter_Sentry_balance":False,
    }
    report["digest"]=canonical_digest({k:v for k,v in report.items() if k!="digest"})
    return report


def attest(report,*,variant="B",seed=0,travel_seconds=12):
    expected=run(variant=variant,seed=seed,travel_seconds=travel_seconds)
    if (type(report) is not dict or
        report.get("digest")!=canonical_digest(
            {k:v for k,v in report.items() if k!="digest"}) or
        expected!=report):
        raise AssertionError("Authentic source native Hunter/Sentry replay changed")
    return deepcopy(expected)


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--variant",choices=("A","B"),default="B")
    p.add_argument("--seed",type=int,default=0)
    p.add_argument("--travel-seconds",type=int,default=12)
    args=p.parse_args()
    report=run(variant=args.variant,seed=args.seed,
               travel_seconds=args.travel_seconds)
    print(json.dumps({k:v for k,v in report.items() if k!="source_ledgers"},
                     indent=2,sort_keys=True))


if __name__=="__main__":
    main()
