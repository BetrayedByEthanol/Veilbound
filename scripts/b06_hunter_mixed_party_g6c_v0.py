"""B06 G6-C v0: native 3/4-character mixed-party Hunter encounter witnesses.

These are source-attested TWO-ROUND integration windows, not adjudicated
victory/defeat, threat/CR calibration or complete I3 fight certification.
A/B source melee (G5/G6B), R missed arrows (G2), F direct Flame (G3/G4),
Hunter Bite/venom (G6A/G4.4) and regeneration use their own native costs.
The script never turns a G2 Bow 'hit_pending_G5' into phantom HP damage.
"""
from copy import deepcopy

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat, ShotChoice
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_player_offense_g6b_v0 import PlayerHunterCombat
from scripts.b06_soldier_sentry_g5_v0 import SceneExit

HUNTER_HEAD = (3, 2)
HUNTER_REAR = (4, 2)
ROSTER = ("vanguard", "guardian", "archer", "scholar")
SOURCES = {"vanguard": "A", "guardian": "B", "archer": "R", "scholar": "F"}
LOCATIONS = {"vanguard": (2, 2), "guardian": (3, 3),
             "archer": (1, 4), "scholar": (1, 0)}
SCORES = {"hunter": 30, "vanguard": 24, "guardian": 20,
          "archer": 16, "scholar": 12}
# Independently preauthored face choices. A natural-1 R arrow is a real
# miss, not a suppressed successful projectile waiting for G5 damage.
POLICY = {
    1: {"hunter": (1, None, None),
        "vanguard": (10, 1), "guardian": (1, None),
        "archer": 1, "scholar": (12, 3)},
    2: {"hunter": (10, 1, 1),
        "vanguard": (10, 1), "guardian": (10, 1),
        "archer": 1, "scholar": (12, 3)},
}


def mixed_scene(*,size,level=3,seed=630,archer_exit=False,party_exits=False,
                frontline="A_head_forward"):
    """Create the authored clear-lane Hunter + A/B/R[/F] fixture.

    Strict scope before Encounter/G1 mutation: one Hunter and exactly
    three or four source-backed PCs at L2/3; no virtual replacements.
    """
    if type(size) is not int or size not in (3,4):
        raise ValueError("G6-C accepts exactly 3 or 4 real party members")
    if type(level) is not int or level not in (2,3):
        raise ValueError("G6-C fixture has L2 and L3 character sheets")
    if type(seed) is not int or seed < 0:
        raise ValueError("G6-C requires a nonnegative encounter seed")
    if (type(archer_exit) is not bool or type(party_exits) is not bool
            or (archer_exit and party_exits)):
        raise ValueError("Choose only one authored G7-B/C exit mode")
    if frontline not in ("A_head_forward","B_head_forward"):
        raise ValueError("Only authored A/B Hunter head-forward contact")
    if frontline=="B_head_forward" and (archer_exit or party_exits):
        raise ValueError("G7-D B-front has no independently authored exit routes")
    present=ROSTER[:size]
    positions=dict(LOCATIONS)
    if frontline=="B_head_forward":
        # A/B exchange the front and side positions before scene setup.
        # The Hunter's 1x2 head and anatomical Bite direction remain real.
        positions["vanguard"],positions["guardian"]=(
            positions["guardian"],positions["vanguard"])
    actors=[enemy_actor("B06-EN-03", "hunter", "enemy",
                        occupied=(HUNTER_HEAD,HUNTER_REAR))]
    actors += [party_actor(SOURCES[name],level,name,"party",
                          occupied=(positions[name],)) for name in present]
    e=Encounter(actors,{k:SCORES[k] for k in ("hunter",*present)},
                seed=seed,scenario=(f"B06-I3-G6C:party-{size}:L{level}"
                    if frontline=="A_head_forward" else
                    f"B06-I3-G7D:B-front:party-{size}:L{level}"),
                objective="observe_two_real_rounds_without_inferred_victory",
                policy="fixed_source_declared_dice_and_declined_optional_responses")
    GridMovement(e,width=8,height=7,scene_id=(
        "G6C-clear-mixed-front" if frontline=="A_head_forward"
        else "G7D-clear-B-head-forward"))
    RangedCombat(e)
    SpellState(e)
    DamageState(e)
    e.begin_round()
    exit_policy=(SceneExit(e.scenario,e.g1.scene_id,e.objective,
                           "archer",(0,4),"G7B:archer-west-border")
                 if archer_exit else None)
    # G7-C authorizes distinct, before-play exits for each source PC,
    # not a retroactive withdrawal square selected by the caller.
    exits=(
        tuple(SceneExit(e.scenario,e.g1.scene_id,e.objective,ident,square,
                        f"G7C:party:{ident}:border")
              for ident,square in (
                  ("vanguard",(0,2)),("guardian",(3,6)),
                  ("archer",(0,4)),("scholar",(0,0))) if ident in present)
        if party_exits else ())
    combat=PlayerHunterCombat(e,scene_exit=exit_policy,scene_exits=exits)
    if e.order != ("hunter",*present):
        raise AssertionError("G6-C authored Initiative positions altered")
    # This invariant matters especially to the 1x2 Hunter: the Priest A is
    # in its only threatened forward square; Priest B is adjacent to its
    # side, but cannot intercept the Bite for free.
    frontline_actor=("vanguard" if frontline=="A_head_forward"
                     else "guardian")
    side_actor=("guardian" if frontline=="A_head_forward"
                else "vanguard")
    if (e.g1.front("hunter")!=positions[frontline_actor]
            or not e.g1.melee_contact(side_actor,"hunter")
            or e.g1.threatens("hunter",positions[side_actor])
            or not e.g1.melee_contact("hunter",frontline_actor,
                                      hunter_front=True)):
        raise AssertionError("Hunter anatomical mixed-party contact invalid")
    for caster in ("archer", "scholar"):
        if caster not in e.actors:
            continue
        lane=e.g2.lane(caster,"hunter",target_cell=HUNTER_HEAD,
                       range_kind=("bow" if caster=="archer" else "flame"))
        if lane.screens or lane.cover:
            raise AssertionError("G6-C never silently elides living screens/cover")
    return combat


def _next_turn(combat,ident,choice):
    e=combat.e
    combat.bridge.start_next_turn(choice)
    if e.current!=ident:
        raise AssertionError("Real G0 Initiative turn not as authored")
    return e.actors[ident]


def _hunter_turn(combat,round_no):
    e=combat.e
    _next_turn(combat,"hunter",
               RegenerationChoice(hp=4 if round_no==2 else 0))
    if e.actors["hunter"].hp<=0:
        raise UnresolvedDecision("Hunter lacks conscious Bite in authored round")
    face,damage,resistance=POLICY[round_no]["hunter"]
    seq=combat.declare("hunter","vanguard",
                       profiles=("B06-AT-04",),
                       defenses=("guard" if round_no==1 else "take_hit",))
    dice={"attack_face":face}
    if damage is not None:
        dice.update(damage_face=damage,venom_resistance_die=resistance)
    resolved=combat.resolve(seq,0,**dice)
    combat.bridge.end_current_turn()
    return resolved


def _priest_turn(combat,ident,round_no):
    e=combat.e
    # The injured Vanguard can choose its exact natural HP allocation at
    # its real subsequent Regeneration Step. No mid-round free healing.
    candidate=e.actors[ident]
    recovery=(min(2,candidate.hp_max-candidate.hp,candidate.vigor)
              if ident=="vanguard" and round_no==2 else 0)
    _next_turn(combat,ident,RegenerationChoice(hp=recovery))
    if e.actors["hunter"].dead:
        raise UnresolvedDecision("Source scene cannot attack a corpse")
    profile=("B06-PC-A-SWORD" if ident=="vanguard"
             else "B06-PC-B-MACE")
    seq=combat.declare(ident,"hunter",profiles=(profile,),
                       defenses=("dodge" if ident=="vanguard" else "take_hit",))
    face,damage=POLICY[round_no][ident]
    dice={"attack_face":face}
    if damage is not None:
        # Only legitimate wound crosses consume their own actual die;
        # the 4-PC round-two Scholar Flame supplies its own later wound.
        dice["damage_face"]=damage
    resolved=combat.resolve(seq,0,**dice)
    combat.bridge.end_current_turn()
    return resolved


def _archer_turn(combat,round_no):
    e=combat.e
    _next_turn(combat,"archer",RegenerationChoice())
    prior=e.actors["archer"].ammunition
    fired=e.g2.bow_sequence("archer","hunter",(
        ShotChoice(defense="take_hit",primary_face=POLICY[round_no]["archer"],
                   target_cell=HUNTER_HEAD),
    ))
    if (len(fired)!=1 or fired[0]["outcome"]!="automatic_miss"
            or e.actors["archer"].ammunition!=prior-1):
        raise AssertionError("G6-C requires one legitimate missed launched arrow")
    combat.bridge.end_current_turn()
    return fired[0]


def _scholar_turn(combat,round_no):
    e=combat.e
    _next_turn(combat,"scholar",RegenerationChoice())
    face,vigor_die=POLICY[round_no]["scholar"]
    hit=e.g3.cast_flame("scholar","hunter",tier=1,face=face,
                        vigor_die=vigor_die,hand_available=True,
                        target_cell=HUNTER_HEAD,
                        wound_location_roll=8 if round_no==2 else None)
    if hit["outcome"]!="direct_hit_resolved_G4":
        raise AssertionError("G6-C Scholar requires a genuine G3+G4 direct Flame")
    combat.bridge.end_current_turn()
    return hit


def _report(combat,*,size,level,observed):
    e=combat.e
    if e.current is not None or e.cursor!=len(e.order):
        raise AssertionError("G6-C requires a complete natural Round End")
    if combat.pending_attack_slots():
        raise AssertionError("G6-C may not hide pre-paid unresolved melee slots")
    # Native ledger is a source of truth; observations are cached copies,
    # never mutable references that could change the encounter.
    turns=[v["detail"]["actor"] for v in e.ledger if v["kind"]=="turn_end"]
    expected=list(e.order)*2
    if turns!=expected:
        raise AssertionError("All mixed-party turns must actually be completed")
    bow=[v for v in e.ledger if v["kind"]=="g2_bow_shot_resolved"]
    if (len(bow)!=2 or any(v["detail"]["outcome"]!="automatic_miss"
                          for v in bow)):
        raise AssertionError("Unresolved G2 projectile hit must not be certified")
    report=combat.report()
    hunter=e.actors["hunter"]
    facts={
        "name":f"G6-C-I3-mixed-{size}-L{level}",
        "roster":[{"id":a,"source":e.actors[a].source.source_id,
                   "source_digest":e.actors[a].source.digest}
                  for a in e.order],
        "size":size,"level":level,"seed":e.seed,"rounds":e.round,
        "initiative":list(e.order),
        "turns":turns,
        "round_ends":len([v for v in e.ledger if v["kind"]=="round_end"]),
        "attack_observations":deepcopy(observed),
        "arrow_launches":len([v for v in e.ledger if v["kind"]=="g2_bow_launched"]),
        "actual_g4_damage_events":len([v for v in e.ledger
                                       if v["kind"]=="g4_damage_applied"]),
        "g45_melee_attestations":len([v for v in e.ledger
                                      if v["kind"]=="g45_attested_hit"]),
        "scholar_flame_hits":len([v for v in e.ledger
                                  if v["kind"]=="g3_flame_launched"
                                  and v["detail"]["outcome"]=="direct_hit_pending_G4"]),
        "hunter_hp":hunter.hp,"hunter_dying":hunter.hp<=0 and not hunter.dead,
        "hunter_dead":hunter.dead,
        "original_report":report,
        "window_status":"two_real_rounds_observed",
        "ending":"not_attested_full_encounter",
        "complete_party_pack_certified":False,
        "hunter_cr":None,
        "missing_mechanics":(
            "G2 landed-bow-hit-to-G4 physical damage and critical proof",
            "G6 reactive/prepared Protective Intervene and chosen counterattacks",
            "complete mixed-party encounter terminal and calibrated CR"),
        "ledger":deepcopy(e.ledger),
    }
    e.check()
    return facts


def run_i3_mixed(*,size,level=3,seed=630):
    """Two real rounds with every member of an authored 3/4-PC party acting.

    This reports an honest *integration witness*, not a narrated win or a
    numeric encounter balance finding. Author only fixed dice, never
    unstated tactics, infinite ammo, implicit player Guard or fake spell HP.
    """
    combat=mixed_scene(size=size,level=level,seed=seed)
    e=combat.e
    observed=[]
    for round_no in (1,2):
        if round_no==2:
            if e.cursor!=len(e.order):
                raise AssertionError("G6-C cannot refresh mid-round")
            combat.bridge.begin_next_round()
        results={
            "hunter":_hunter_turn(combat,round_no),
            "vanguard":_priest_turn(combat,"vanguard",round_no),
            "guardian":_priest_turn(combat,"guardian",round_no),
            "archer":_archer_turn(combat,round_no),
        }
        if size==4:
            results["scholar"]=_scholar_turn(combat,round_no)
        observed.append({"round":round_no,"results":deepcopy(results),
                         "hunter_hp_after":e.actors["hunter"].hp})
        if e.current is not None or e.cursor!=len(e.order):
            raise AssertionError("G6-C must end each real round")
    return _report(combat,size=size,level=level,observed=observed)
