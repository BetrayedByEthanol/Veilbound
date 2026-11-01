"""Bounded, source-native Alpha L1->L2->L3 Soldier/Hunter/Sentry pilot chain.

Four ORIGINAL Priest/Low A|B, Scholar/High, Gifted/High, Anointed/Medium
characters, not the A/B/R/F G8 cohort. One GM-AUTHOR CANDIDATE award at
each clean scene boundary; never a real GM attestation or implicit refill.
Native source actor, G0/G1/G2/G3/G4/G5 attacks, HP, Vigor, Spent/Committed
VP, original recovery deadlines and source-ledger provenance are retained.
"""
from copy import deepcopy
from dataclasses import asdict
import json

from scripts.b04_b05_b06_alpha_mixed_native_v0 import (
    scene as l1_scene, PARTY, FOCUSES, EXIT_STEPS, EXIT_SQUARES,
)
from scripts.b05_low_life_native_rites_v0 import (
    LowLifeNativeRites,full_low_priest_actor,
)
from scripts.b05_high_gifted_native_encounter_v0 import GiftedNative,gifted_actor
from scripts.b05_medium_anointed_native_returning_step_v0 import MediumAnointedRestoration
from scripts.b05_b06_native_party_continuity_v0 import CARRY_FIELDS
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee,SceneExit
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION="B04-B05-B06-Alpha-L2-L3-Persistent-Mixed-Progression-v0"
LEVEL_FIELDS=(
    "source","level","focus","initiative_bonus","awareness","agility",
    "hp_max","vigor_max","vp_max","regen","ap_total","physical_ap",
    "projection_ap","guard_instrument","guard_value","guard_capacity",
)
POSITIONS={"anointed":(1,3),"priest":(3,2),
           "gifted":(3,5),"scholar":(1,5)}
ACTORS={"anointed":"AM","priest":"selected-full-low","gifted":"G","scholar":"F"}
SCORES={"anointed":50,"foe":40,"priest":30,"gifted":20,"scholar":10}
OPPONENTS={"hunter":("B06-EN-03",None,((4,2),(5,2))),
           "sentry_cold":("B06-EN-01","cold_start",((4,2),))}
BEATS=("gate","shrine")


def _source_actor(name,level,variant):
    if name=="priest":
        return full_low_priest_actor(
            variant,level,name,"party",occupied=(POSITIONS[name],))
    if name=="gifted":
        return gifted_actor(level,name,"party",occupied=(POSITIONS[name],))
    if name in ("anointed","scholar"):
        return party_actor(ACTORS[name],level,name,"party",
                           occupied=(POSITIONS[name],))
    raise ValueError("No non-Alpha actor allowed in source progression")


def _recovery_due(e):
    """Read authentic party six-hour Recovery deadlines at exploration boundary."""
    if e.g4.clock.mode!="exploration":
        raise UnresolvedDecision("Recovery deadline witness needs exploration clock")
    result={}
    for n in PARTY:
        live=[event for event in e.g4.clock.events.values()
              if event.kind=="recovery" and event.actor_id==n
              and not event.consumed and not event.canceled]
        if len(live)!=1 or type(live[0].due_seconds) is not int:
            raise UnresolvedDecision("Exactly one live source Recovery deadline per Alpha PC")
        result[n]={"id":live[0].ident,"due_seconds":live[0].due_seconds}
    return result


def _state(e):
    """Source and all persistent G0/G2 parts; no fake full-resource projection."""
    return {n:{
        "source_id":e.actors[n].source.source_id,
        "source_digest":e.actors[n].source.digest,
        "source_path":e.actors[n].source.path,
        "level":e.actors[n].level,
        **{field:deepcopy(getattr(e.actors[n],field))
           if field!="wounds" else [asdict(w) for w in e.actors[n].wounds]
           for field in CARRY_FIELDS},
        "wielded":sorted(e.g2.wielded[n]),
    } for n in PARTY}


def _clean_boundary(e,*,terminal=True):
    if (e.current is not None or e.pending_regeneration is not None
            or not e.round or e.cursor!=len(e.order)
            or not any(x["kind"]=="round_end" and x["round"]==e.round
                       for x in e.ledger)
            or e.reservations or e.g5.pending_attack_slots()
            or e.g4.clock.mode!="exploration" or e.g1.pounce is not None
            or any(e.g2.aims.get(n) for n in PARTY)
            or e.g3.effects
            or e.g4.short_toxins or e.g4.toxins.instances
            or e.g4.toxins.exposure_ids or e.g4.venom.effects
            or any(v.kind!="recovery" and not v.consumed and not v.canceled
                   for v in e.g4.clock.events.values())
            or any(e.actors[n].maintained or e.actors[n].hp<=0
                   or e.actors[n].dead for n in PARTY)):
        raise UnresolvedDecision("Alpha level handoff needs settled living party, no active effects or pending actions")
    if terminal:
        exits=[x for x in e.ledger if x["kind"]=="g5_terminal_exit"]
        if (len(exits)!=len(PARTY)
                or {x["detail"]["actor"] for x in exits}!=set(PARTY)
                or any(tuple(e.actors[n].occupied[0])!=EXIT_SQUARES[n]
                       for n in PARTY)):
            raise UnresolvedDecision("All four source-attested exit receipts required before advancement")
    e.check()


def candidate_awards():
    return [
        {"event_id":"ALPHA-AUTHOR-CANDIDATE:GATE:L2",
         "beat":"gate","from_level":1,"to_level":2,
         "kind":"adventure_milestone","gm_declared":True,
         "automatic":False,"gm_source":"authored_candidate_only_no_human_observation"},
        {"event_id":"ALPHA-AUTHOR-CANDIDATE:SHRINE:L3",
         "beat":"shrine","from_level":2,"to_level":3,
         "kind":"adventure_milestone","gm_declared":True,
         "automatic":False,"gm_source":"authored_candidate_only_no_human_observation"},
    ]


def _awards(events):
    expected=candidate_awards()
    if (type(events) not in (list,tuple) or len(events)!=2
            or any(type(x) is not dict or x!=y for x,y in zip(events,expected))):
        raise UnresolvedDecision("Two separately authored GM *candidate* milestones; no automatic/forged awards")
    return deepcopy(events)


def award(e,event,*,variant):
    """Reproject same four source actors after real source-settled GM fixture beat.

    Incremented Max VP is staged Spent (a conservative PILOT FIXTURE policy,
    not a canonical levelling refill entitlement), never made Available.
    """
    if type(event) is not dict or event not in candidate_awards():
        raise UnresolvedDecision("Unauthenticated or non-Alpha advancement source")
    level=event["from_level"]
    if event["beat"]!=BEATS[level-1] or event["to_level"]!=level+1:
        raise UnresolvedDecision("Actual story/level progression order required")
    _clean_boundary(e)
    witnessed=[x for x in e.ledger
               if x["kind"]=="b04_b05_b06_alpha_story_beat_candidate"
               and x["detail"].get("beat")==event["beat"]
               and x["detail"].get("from_level")==level
               and x["detail"].get("to_level")==level+1]
    if len(witnessed)!=1:
        raise UnresolvedDecision("Author candidate beat must follow an authentic native stage terminal")
    old=_state(e)
    proposed={}
    for n in PARTY:
        actor=e.actors[n]
        fresh=_source_actor(n,level,variant)
        later=_source_actor(n,level+1,variant)
        if (actor.level!=level or actor.source!=fresh.source
                or actor.source.equipment!=later.source.equipment
                or actor.hp>later.hp_max or actor.vigor>later.vigor_max
                or later.vp_max<actor.vp_max
                or event["event_id"] in actor.milestones):
            raise UnresolvedDecision("Selected Alpha build, level, gear or current resources changed")
        delta=later.vp_max-actor.vp_max
        if (actor.vp_available+actor.vp_committed+actor.vp_spent
                !=actor.vp_max):
            raise UnresolvedDecision("Cannot level with invalid available/committed/spent VP")
        trial=deepcopy(actor)
        for field in LEVEL_FIELDS:
            setattr(trial,field,deepcopy(getattr(later,field)))
        trial.vp_spent+=delta
        trial.milestones.append(event["event_id"])
        trial.validate()
        proposed[n]=(trial,delta)
    deadlines={key:asdict(value) for key,value in e.g4.clock.events.items()}
    for n,(trial,delta) in proposed.items():
        a=e.actors[n]
        for field in LEVEL_FIELDS:
            setattr(a,field,deepcopy(getattr(trial,field)))
        a.vp_spent+=delta
        a.milestones.append(event["event_id"])
    e.check()
    after=_state(e)
    for n in PARTY:
        previous,new=old[n],after[n]
        if any(previous[k]!=new[k] for k in
               ("hp","vigor","vp_available","vp_committed","ammunition",
                "wounds","conditions","maintained","wielded")):
            raise AssertionError("GM candidate level-up silently replenished party")
        if new["vp_spent"]-previous["vp_spent"]!=proposed[n][1]:
            raise AssertionError("Only changed source Max VP staged Spent")
    if deadlines!={key:asdict(value) for key,value in e.g4.clock.events.items()}:
        raise AssertionError("Old recovery clock altered by author milestone")
    receipt={
        "event_id":event["event_id"],"beat":event["beat"],
        "from_level":level,"to_level":level+1,
        "old_party_sha256":canonical_digest(old),
        "new_party_sha256":canonical_digest(after),
        "new_capacity_staged_spent":{n:proposed[n][1] for n in PARTY},
        "world_seconds":e.g4.clock.world_seconds,
        "recovery_event_sha256":canonical_digest(deadlines),
        "no_HP_Vigor_available_VP_refill":True,
        "author_candidate_only":True,"real_GM_attested":False,
    }
    e.log("b04_b05_b06_alpha_level_candidate_applied",**receipt)
    return receipt


def _scene(level,variant,kind,seed):
    if kind not in OPPONENTS or level not in (2,3) or type(seed) is not int or seed<0:
        raise ValueError("Exactly L2 Hunter or L3 cold Sentry scene with source seed")
    source,start,footprint=OPPONENTS[kind]
    actors=[_source_actor(n,level,variant) for n in PARTY]
    actors.append(enemy_actor(source,"foe","enemy",start_state=start,
                              occupied=footprint))
    e=Encounter(actors,SCORES,seed=seed,
                scenario="Alpha:L"+str(level)+":"+kind+":native",
                policy="author_fixed_source_mixed_and_opposed_exit",
                objective="original_source_mixed_party_native_stage")
    GridMovement(e,width=8,height=7,scene_id="Alpha-L"+str(level)+"-open")
    RangedCombat(e,scene_id="Alpha-L"+str(level)+"-original-ready-weapons")
    SpellState(e)
    DamageState(e)
    low=LowLifeNativeRites(e,"priest")
    joy=GiftedNative(e,"gifted")
    am=MediumAnointedRestoration(e,"anointed")
    exits=tuple(SceneExit(
        e.scenario,e.g1.scene_id,e.objective,n,EXIT_SQUARES[n],
        "Alpha:L"+str(level)+":"+n+":source-cautious") for n in PARTY)
    combat=SourceMelee(e,scene_exits=exits,player_benchmark_target=None)
    if e.order!=("anointed","foe","priest","gifted","scholar"):
        raise AssertionError("Stage source initiative drifted")
    if kind=="hunter" and not e.g1.melee_contact("foe","priest",hunter_front=True):
        raise UnresolvedDecision("Actual 1x2 Hunter head-forward Priest contact missing")
    return combat,low,joy,am


def _carry(previous,following,*,travel_seconds,reference):
    """Strict source-identity and clock transfer, no new state or free rest."""
    if (type(travel_seconds) is not int or not 0<=travel_seconds<=600
            or type(reference) is not str or not reference):
        raise ValueError("Exactly bounded explicit route time/reference needed")
    _clean_boundary(previous)
    if (following.round or following.current is not None
            or following.g4.clock.mode!="exploration"
            or following.g4.clock.world_seconds!=0
            or following.g3.effects
            or any(a.hp!=a.hp_max or a.vigor!=a.vigor_max
                   or a.vp_available!=a.vp_max or a.vp_committed or a.vp_spent
                   for n,a in following.actors.items() if n in PARTY)):
        raise UnresolvedDecision("Target must be pristine sourced G0/G4 scene")
    for n in PARTY:
        old,new=previous.actors[n],following.actors[n]
        pristine=_source_actor(n,new.level,
               "A" if old.source.source_id=="A" else
               "B" if old.source.source_id=="B" else "A")
        if (old.source!=new.source or new.source!=pristine.source
                or old.level!=new.level or old.team!="party"
                or old.occupied==() or
                any(getattr(new,k)!=getattr(pristine,k) for k in
                    ("hp","vigor","vp_available","vp_committed","vp_spent",
                     "ammunition","wounds","conditions","maintained"))
                or set(following.g2.wielded[n])!=
                   {item for item,state in pristine.source.equipment if state=="wielded"}):
            raise UnresolvedDecision("Source-ledger/pristine destination character mismatch")
    old_clock=previous.g4.clock
    if (old_clock.world_seconds+travel_seconds>=21600
            or any(v.kind!="recovery" and not v.consumed and not v.canceled
                   for v in old_clock.events.values())):
        raise UnresolvedDecision("Long Recovery/hazard boundary needs separate source handoff")
    # Advance genuine G4.2 time and only THEN copy the resulting native
    # source events, not forged absolute event fields from caller JSON.
    old_clock.advance_exploration(travel_seconds)
    earlier=_state(previous)
    old_events={key:deepcopy(value) for key,value in old_clock.events.items()
                if value.actor_id in PARTY}
    next_clock=following.g4.clock
    if (set(next_clock.events)!={f"recovery:{n}:1" for n in (*PARTY,"foe")}
            or any(next_clock.recovery_serial[n]!=2 for n in (*PARTY,"foe"))):
        raise UnresolvedDecision("Fresh destination Recovery state changed")
    for n in PARTY:
        source=previous.actors[n]
        target=following.actors[n]
        for field in CARRY_FIELDS:
            setattr(target,field,deepcopy(getattr(source,field)))
        following.g2.wielded[n]=set(previous.g2.wielded[n])
    for key in tuple(next_clock.events):
        if next_clock.events[key].actor_id in PARTY:
            del next_clock.events[key]
    for key,ev in old_events.items():
        if key in next_clock.events:
            raise UnresolvedDecision("Old source recovery ID overlaps new enemy event")
        next_clock.events[key]=ev
    enemy=next_clock.events["recovery:foe:1"]
    enemy.due_seconds+=old_clock.world_seconds
    enemy.original_order+=old_clock.world_seconds
    enemy.serial=old_clock.sequence+1
    for n in PARTY:
        next_clock.recovery_serial[n]=old_clock.recovery_serial[n]
    next_clock.sequence=old_clock.sequence+1
    next_clock.world_seconds=old_clock.world_seconds
    following.check()
    if earlier!=_state(following):
        raise AssertionError("Cross-scene Alpha resources or legal wielding refilled")
    receipt={
        "from":previous.scenario,"to":following.scenario,"travel_ref":reference,
        "elapsed_seconds":travel_seconds,
        "source_party_sha256":canonical_digest(earlier),
        "imported_party_sha256":canonical_digest(_state(following)),
        "old_ledger_sha256":canonical_digest(previous.ledger),
        "pending_recovery_sha256":canonical_digest(
            {k:asdict(v) for k,v in old_events.items()}),
        "world_seconds":old_clock.world_seconds,
        "no_free_refill":True,"no_imported_foe_status":True,
    }
    following.log("b04_b05_b06_alpha_party_handoff",**receipt)
    return receipt


def _begin(combat):
    e=combat.e
    e.g4.clock.enter_initiative()
    e.begin_round()


def _start(combat,who):
    combat.bridge.start_next_turn(RegenerationChoice())
    if combat.e.current!=who:
        raise AssertionError("Native source turn not next")


def _foe(combat,kind,*,face):
    e=combat.e
    profile=("B06-AT-03" if kind=="soldier" else
             "B06-AT-04" if kind=="hunter" else e.g3.sentry_profile("foe"))
    if kind=="hunter" and not e.g1.melee_contact("foe","priest",hunter_front=True):
        raise UnresolvedDecision("Hunter moved off the exact source head-forward contact")
    seq=combat.declare("foe","priest",profiles=(profile,),defenses=("take_hit",))
    dice={"attack_face":face}
    if face!=1:
        dice.update(damage_face=2,wound_location_roll=8)
        if kind=="hunter":
            dice.update(venom_resistance_die=12)
        if profile=="B06-AT-02":
            dice.update(vigor_die=1)
    result=combat.resolve(seq,0,**dice)
    if result["outcome"]!=("miss" if face==1 else "hit"):
        raise AssertionError("Native source enemy G5 hit/defense contradicted")
    return result


def _exit(combat,who):
    e=combat.e
    for delta in EXIT_STEPS[who]:
        if not e.g1.step(who,delta,cautious=True,
                         responses=lambda offered: ()):
            raise UnresolvedDecision("Original authenticated G1 exit interrupted")
    combat.withdraw(who)


def _terminal(combat,kind):
    e=combat.e
    if (e.current is not None or e.cursor!=len(e.order)
            or combat.pending_attack_slots()
            or not any(x["kind"]=="round_end" and x["round"]==e.round
                       for x in e.ledger)):
        raise UnresolvedDecision("Original source G5 round boundary is unsettled")
    events=[x for x in e.ledger if x["kind"]=="g5_terminal_exit"]
    if (len(events)!=4 or {x["detail"]["actor"] for x in events}!=set(PARTY)
            or any(e.actors[n].hp<=0 or e.actors[n].dead for n in PARTY)
            or e.actors["foe"].dead):
        raise UnresolvedDecision("No source-attested four-PC contested exit")
    e.log("b04_b05_b06_alpha_stage_withdrawal_attested",
          opponent=kind,level=e.actors["priest"].level,round=e.round,
          exit_indices=[x["index"] for x in events],
          outcome="party_scene_withdrawal",native_source_only=True,
          human_GM_observed=False)
    e.g4.clock.leave_initiative()
    e.check()
    return "party_scene_withdrawal"


def _l1(variant,seed):
    """Old source Alpha gate; no maintained Rite/Investment to silently drop."""
    combat,low,joy,am=l1_scene(
        variant=variant,seed=seed,native_initiative_clock=True)
    e=combat.e
    # The native G4.2 initiative clock must already be active BEFORE the
    # L1 scene's first Round Begin, not switched on after that boundary.
    if (e.g4.clock.mode!="initiative" or e.g4.clock.entry_round!=1):
        raise AssertionError("L1 Recovery clock did not enter before first Round Begin")
    for round_no in (1,2):
        if round_no==2:
            combat.bridge.begin_next_round()
        for who in e.order:
            _start(combat,who)
            if who=="foe":
                _foe(combat,"soldier",face=12 if round_no==1 else 1)
            elif round_no==1 and who=="gifted":
                joy.establish("Joy")
                joy.cast_flame("foe",tier=1,face=1,vigor_die=3,
                               hand_available=True)
            elif round_no==1 and who=="scholar":
                e.g3.cast_flame("scholar","foe",tier=1,face=1,
                                vigor_die=3,hand_available=True)
            elif round_no==2 and who in PARTY:
                _exit(combat,who)
            combat.bridge.end_current_turn()
    # Authenticate the full four-PC terminal BEFORE exiting G4.2 initiative.
    # _terminal uses the same source G5 exit checks and clock conversion as
    # L2/L3, then _clean_boundary asserts the exploration handoff is settled.
    if _terminal(combat,"soldier")!="party_scene_withdrawal":
        raise AssertionError("L1 source Soldier stage lacks actual four-PC exit")
    _clean_boundary(e)
    if not any(x["kind"]=="g4_damage_applied" and
               x["detail"].get("recipient")=="priest" for x in e.ledger):
        raise AssertionError("Original source hostile L1 resource attrition required")
    e.log("b04_b05_b06_alpha_story_beat_candidate",
          beat="gate",from_level=1,to_level=2,
          original_source_terminal_exits=4,
          external_GM_story_attested=False,
          candidate_only_not_automatically_awarded=True)
    return combat


def _l2(combat,joy):
    """Two genuine Hunter head-forward Bite attempts; no false venom or kill."""
    e=combat.e
    _begin(combat)
    if e.actors["priest"].hp>=e.actors["priest"].hp_max:
        raise AssertionError("Original L1 HP attrition vanished at L2 entry")
    for round_no in (1,2):
        if round_no==2:
            combat.bridge.begin_next_round()
        for who in e.order:
            _start(combat,who)
            if who=="foe":
                _foe(combat,"hunter",face=1)
            elif round_no==1 and who=="gifted":
                joy.establish("Joy")
                joy.cast_flame("foe",tier=1,face=1,vigor_die=3,
                               hand_available=True,target_cell=(4,2))
            elif round_no==2 and who in PARTY:
                _exit(combat,who)
            combat.bridge.end_current_turn()
    result=_terminal(combat,"hunter")
    e.log("b04_b05_b06_alpha_story_beat_candidate",
          beat="shrine",from_level=2,to_level=3,
          original_source_terminal_exits=4,
          external_GM_story_attested=False,
          candidate_only_not_automatically_awarded=True)
    return result


def _l3(combat,low,joy,am):
    """Cold Sentry prepares its paid sword; AM uses actual invested Priest Step."""
    e=combat.e
    _begin(combat)
    applied=0
    for round_no in (1,2):
        if round_no==2:
            combat.bridge.begin_next_round()
        for who in e.order:
            if who=="priest" and round_no==1:
                a=e.actors[who]
                if a.hp>0 and a.hp<a.hp_max and a.vigor>0:
                    am.declare_pulse("priest",lesser=False,
                                     visible=True,unopposed=True)
            _start(combat,who)
            if round_no==1:
                if who=="anointed":
                    am.invest("priest",consenting=True)
                elif who=="foe":
                    if e.g3.cast_sentry_reserve("foe") is None:
                        raise UnresolvedDecision("Cold Sentry missing real G3 Reserve")
                elif who=="priest":
                    if low.cast_chosen("priest",chosen=True) is None:
                        raise AssertionError("Selected complete Low Priest Rite missing")
                elif who=="gifted":
                    joy.establish("Joy")
                    joy.cast_flame("foe",tier=1,face=1,vigor_die=3,
                                   hand_available=True)
                elif who=="scholar":
                    e.g3.cast_flame("scholar","foe",tier=1,face=1,
                                    vigor_die=3,hand_available=True)
            else:
                if who=="foe":
                    if e.g3.sentry_profile("foe")!="B06-AT-02":
                        raise AssertionError("Sentry source Reserve not paid/maintained")
                    _foe(combat,"sentry_cold",face=1)
                elif who in PARTY:
                    _exit(combat,who)
            combat.bridge.end_current_turn()
    if not any(x["kind"]=="g4_anointed_medium_returning_step_applied"
               for x in e.ledger):
        raise AssertionError("Actual source Priest Step did not receive AM pulse")
    return _terminal(combat,"sentry_cold")


def run(*,variant="A",seed=0,awards=None,travel_seconds=300):
    if variant not in ("A","B") or type(seed) is not int or seed<0:
        raise ValueError("Only sourced full Low Priest A/B, nonnegative seed")
    if type(travel_seconds) is not int or not 0<=travel_seconds<=600:
        raise ValueError("Bounded genuine per-scene travel seconds required")
    author=_awards(candidate_awards() if awards is None else awards)
    first=_l1(variant,seed)
    e1=first.e
    l1_end=_state(e1)
    l1_recovery=_recovery_due(e1)
    receipt1=award(e1,author[0],variant=variant)
    upgraded_l2=_state(e1)
    l2_combat,_,l2_joy,_=_scene(2,variant,"hunter",seed+1)
    transfer1=_carry(e1,l2_combat.e,travel_seconds=travel_seconds,
                     reference="ALPHA-FIXTURE:gate-to-forest")
    l2_begin=_state(l2_combat.e)
    l2_entry_recovery=_recovery_due(l2_combat.e) if l2_combat.e.g4.clock.mode=="exploration" else None
    outcome_l2=_l2(l2_combat,l2_joy)
    l2_end=_state(l2_combat.e)
    l2_recovery=_recovery_due(l2_combat.e)
    receipt2=award(l2_combat.e,author[1],variant=variant)
    upgraded_l3=_state(l2_combat.e)
    l3_combat,l3_low,l3_joy,l3_am=_scene(3,variant,"sentry_cold",seed+2)
    transfer2=_carry(l2_combat.e,l3_combat.e,travel_seconds=travel_seconds,
                     reference="ALPHA-FIXTURE:shrine-to-village")
    l3_begin=_state(l3_combat.e)
    l3_entry_recovery=_recovery_due(l3_combat.e) if l3_combat.e.g4.clock.mode=="exploration" else None
    outcome_l3=_l3(l3_combat,l3_low,l3_joy,l3_am)
    final=_state(l3_combat.e)
    l3_recovery=_recovery_due(l3_combat.e)
    if (l2_begin!=upgraded_l2 or l3_begin!=upgraded_l3
            or any(l1_end[n]["source_id"]!=final[n]["source_id"] for n in PARTY)
            or any(final[n]["level"]!=3 for n in PARTY)):
        raise AssertionError("Original selected Alpha character progression drift")
    if (len([x for x in l2_combat.e.ledger if x["kind"]=="g5_melee_resolved"])!=2
            or len([x for x in l3_combat.e.ledger if x["kind"]=="g5_melee_resolved"])!=1
            or l3_combat.e.g3.sentry_profile("foe")!="B06-AT-02"):
        raise AssertionError("Original native Hunter/Sentry opposition not retained")
    def evidence(e):
        return {"source_digests":{n:a.source.digest for n,a in e.actors.items()},
                "source_ids":{n:a.source.source_id for n,a in e.actors.items()},
                "ledger_sha256":canonical_digest(e.ledger),
                "ledger":deepcopy(e.ledger)}
    report={
        "version":VERSION,"variant":variant,"seed":seed,
        "session_plan_levels":[1,2,2,3],
        "source_focuses":dict(FOCUSES),
        "source_adversaries":{"L1":"B06-EN-02","L2":"B06-EN-03",
                             "L3":"B06-EN-01"},
        "l1_end":l1_end,"milestone_one":receipt1,
        "l2_post_award":upgraded_l2,"first_handoff":transfer1,
        "l2_start":l2_begin,"l2_end":l2_end,"l2_outcome":outcome_l2,
        "milestone_two":receipt2,"l3_post_award":upgraded_l3,
        "second_handoff":transfer2,"l3_start":l3_begin,
        "l3_outcome":outcome_l3,"l3_final":final,
        "source_evidence":{"L1":evidence(e1),"L2":evidence(l2_combat.e),
                           "L3":evidence(l3_combat.e)},
        "world_seconds":[e1.g4.clock.world_seconds,
                         l2_combat.e.g4.clock.world_seconds,
                         l3_combat.e.g4.clock.world_seconds],
        "native_recovery_deadlines":{
            "L1_after_two_rounds":l1_recovery,
            "L2_entry":l2_entry_recovery,
            "L2_after_two_rounds":l2_recovery,
            "L3_entry":l3_entry_recovery,
            "L3_after_two_rounds":l3_recovery,
        },
        "native_source_stage_terminals":3,
        "human_sessions":0,"actual_GM_milestones_authenticated":0,
        "independently_certified_focuses":0,"strict_mvp_exits_met":0,
        "representative_difficulty_calibrated":False,
        "generalized_mixed_party_engine":False,
        "live_cross_level_effect_rebinding_supported":False,
    }
    report["digest"]=canonical_digest({k:v for k,v in report.items()
                                       if k!="digest"})
    return report


def attest(report,*,variant="A",seed=0,awards=None,travel_seconds=300):
    expected=run(variant=variant,seed=seed,awards=awards,
                 travel_seconds=travel_seconds)
    if (type(report) is not dict or
            report.get("digest")!=canonical_digest(
                {k:v for k,v in report.items() if k!="digest"})
            or report!=expected):
        raise AssertionError("L1-L3 source-native Alpha party replay differs")
    return deepcopy(expected)


def main():
    import argparse
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--variant",choices=("A","B"),default="A")
    cli.add_argument("--seed",type=int,default=0)
    cli.add_argument("--travel-seconds",type=int,default=300)
    args=cli.parse_args()
    out=run(variant=args.variant,seed=args.seed,travel_seconds=args.travel_seconds)
    print(json.dumps({k:v for k,v in out.items() if k!="source_evidence"},
                     sort_keys=True,indent=2))


if __name__=="__main__":
    main()
