"""B04/B06/B07 live L1->L3 source party, GM-fixture milestones and encounters.

An executable author/GM *fixture*, not a human session, real milestone
attestation, certified twelve-Focus character or new canonical refill rule.
The original G8 engine remains strictly L2/L3; L1 is source-backed G0/G4.2
noncombat with its own genuine ledger and clock.
"""
from copy import deepcopy
from dataclasses import asdict
import json
from scripts.b06_encounter_state_v0 import (
    Encounter, UnresolvedDecision, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat, ShotChoice
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SceneExit, SourceMelee
from scripts.b06_g8_soldier_sentry_full_pack_v0 import (
    PARTY, POSITIONS, EXITS, _turn, _foe_turn, _player_turn, _terminal,
)
from scripts.b05_b06_native_party_continuity_v0 import (
    CARRY_FIELDS, ROLES, _new_scene, _preflight_destination,
    _boundary, _resolve_victory, handoff, party_state,
)
from scripts.b05_b06_integrated_noncombat_adventure_v0 import _roll, _time
from scripts.b04_b05_noncombat_scene_resolution_v0 import SCENES
from scripts.b04_b07_independent_progression_audit_v0 import (
    validate_pilot_milestones, audit,
)
from scripts.b04_b05_b06_b07_integrated_pilot_adventure_v0 import (
    MILESTONE_BEATS, plan,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION="B04-B06-B07-Integrated-Milestone-Persistent-Party-v0"
FIELDS=("source","level","focus","initiative_bonus","awareness","agility",
        "hp_max","vigor_max","vp_max","regen","ap_total","physical_ap",
        "projection_ap","guard_instrument","guard_value","guard_capacity")
SCORES={"vanguard":24,"guardian":20,"archer":16,"scholar":12}
SOURCE_PROFILES={
    "vanguard":lambda level: __import__(
        "scripts.b05_low_priest_life_l1_l3_v0",fromlist=["profile"]).profile("A",level),
    "guardian":lambda level: __import__(
        "scripts.b05_low_priest_life_l1_l3_v0",fromlist=["profile"]).profile("B",level),
    "archer":lambda level: __import__(
        "scripts.b05_bow_vanguard_l1_l3_v0",fromlist=["profile"]).profile(level),
    "scholar":lambda level: __import__(
        "scripts.b05_high_scholar_fire_l1_l3_v0",fromlist=["profile"]).profile(level),
}


def fixture_awards():
    """Author-declared candidate records, never authenticated human GM awards."""
    return [
        {"event_id":"GM-FIXTURE:gate:level2","kind":"adventure_milestone",
         "beat":"gate","from_level":1,"to_level":2,
         "gm_declared":True,"automatic":False,
         "gm_source":"authored_candidate_only_no_human_observation"},
        {"event_id":"GM-FIXTURE:shrine:level3","kind":"adventure_milestone",
         "beat":"shrine","from_level":2,"to_level":3,
         "gm_declared":True,"automatic":False,
         "gm_source":"authored_candidate_only_no_human_observation"},
    ]


def _check_awards(awards):
    if type(awards) not in (list,tuple) or len(awards)!=2:
        raise UnresolvedDecision("Two separate explicit GM fixture decisions are required")
    if any(type(m) is not dict or
           m.get("beat")!=canonical["beat"] or
           m.get("from_level")!=canonical["from_level"] or
           m.get("to_level")!=canonical["to_level"] or
           m.get("gm_source")!="authored_candidate_only_no_human_observation"
           for m,canonical in zip(awards,MILESTONE_BEATS)):
        raise UnresolvedDecision("Advancement must follow authored gate and shrine beats")
    for n in PARTY:
        validate_pilot_milestones(n,[dict(entry,character_id=n) for entry in awards])
    if len({m["event_id"] for m in awards})!=2:
        raise UnresolvedDecision("A single story milestone cannot be reused")
    return deepcopy(awards)


def _l1():
    """Four ORIGINAL source L1 PC identities, no unlawful L1 G8 opponent."""
    actors=[party_actor(ROLES[n],1,n,"party",occupied=(POSITIONS[n],))
            for n in PARTY]
    e=Encounter(actors,SCORES,seed=0,
                scenario="B04-B06-B07:L1:source-supply-and-gate",
                policy="fixture_author_gm_noncombat_explicit_d20",
                objective="find spoilage and request public supply records")
    GridMovement(e,width=8,height=7,scene_id="G8-mixed-clear")
    RangedCombat(e)
    SpellState(e)
    DamageState(e)
    # Reuse the already-authored core-check targets/training and G4.2 time
    # prices, but take the actor's REAL source abilities and audited sheet.
    scripted=(
        ("scholar","crossing","exploration","survey",12),
        ("vanguard","cache-investigation","investigation","diagnose",12),
        ("scholar","public-record-request","social","document",20),
    )
    checks=[]
    for ident,scene,domain,approach,face in scripted:
        a=e.actors[ident]
        p=SOURCE_PROFILES[ident](1)
        if (p["abilities"]!=dict(a.source.abilities)
                or p["level"]!=1 or a.source.start_state!=
                "L1-physical-proxy" and ident in ("vanguard","guardian")):
            raise UnresolvedDecision("L1 sheet does not match original G0 source")
        e.log("b07_milestone_pilot_core_check_declared",
              actor=ident,actor_source=a.source.source_id,
              actor_source_sha256=a.source.digest,
              approach=approach,face=face,
              author_gm_fixture_only=True)
        receipt=_roll(e,p["abilities"],p["learned_disciplines"],
                      scene=scene,domain=domain,approach=approach,
                      face=face)
        _time(e,SCENES[domain][approach]["time_seconds"],
              cause="GM-fixture:"+scene+":"+approach)
        checks.append({"actor":ident,**receipt})
    e.log("b07_l1_noncombat_fixture_gate_completed",
          checks=[v["success"] for v in checks],
          candidate_story_only=True,not_a_gm_level_award=True)
    e.check()
    return e,checks


def _safe_award_boundary(e, current):
    if (e.g4 is None or e.g4.clock.mode!="exploration" or
            e.current is not None or e.pending_regeneration is not None or
            e.reservations or (e.g5 is not None and e.g5.pending_attack_slots())):
        raise UnresolvedDecision("Advancement requires completed exploration boundary")
    if current==1:
        if (e.round!=0 or
                not any(x["kind"]=="b07_l1_noncombat_fixture_gate_completed"
                        for x in e.ledger)):
            raise UnresolvedDecision("No authenticated L1 source noncombat fixture")
    elif current==2:
        _boundary(e)  # Original G8 terminal, no injected source kill/withdrawal.
    else:
        raise UnresolvedDecision("Only two source-audited pilot awards")
    if (e.g4.short_toxins or e.g4.toxins.instances or
            e.g4.venom.effects or e.g3.effects or
            any(v.kind!="recovery" and not v.consumed and not v.canceled
                for v in e.g4.clock.events.values())
            or any(e.actors[n].maintained for n in PARTY)):
        raise UnresolvedDecision("No v0 milestone while live hazards/hosts need rebinding")
    if any(e.actors[n].hp<=0 or e.actors[n].dead for n in PARTY):
        raise UnresolvedDecision("Pilot cannot silently advance a dying member")


def award(e, event):
    """Apply ONE explicit, distinct author-GM pilot award to same live actors.

    New VP capacity is initially Spent, never automatically Available:
    this is a conservative fixture rule and NOT a canonical generic level-up
    refresh policy. Future normal G4.2 Recovery can reimburse it.
    """
    if type(event) is not dict:
        raise ValueError("Explicit milestone record required")
    current=event.get("from_level")
    if (type(current) is not int or current not in (1,2)
            or event.get("to_level")!=current+1
            or event.get("beat")!=MILESTONE_BEATS[current-1]["beat"]
            or type(event.get("event_id")) is not str
            or not event["event_id"] or event.get("gm_declared") is not True
            or event.get("automatic") is not False
            or event.get("kind")!="adventure_milestone"
            or event.get("gm_source")!="authored_candidate_only_no_human_observation"
            or any(event["event_id"] in e.actors[n].milestones for n in PARTY)):
        raise UnresolvedDecision("Only separately declared source pilot milestone applies")
    _safe_award_boundary(e,current)
    proposals={}
    for n in PARTY:
        a=e.actors[n]
        if a.level!=current or a.source!=party_actor(
                ROLES[n],current,n,"party",occupied=a.occupied).source:
            raise UnresolvedDecision("Old level or original build source mismatch")
        new=party_actor(ROLES[n],current+1,n,"party",occupied=a.occupied)
        if (a.source.source_id!=new.source.source_id
                or a.source.digest!=new.source.digest
                or a.source.equipment!=new.source.equipment
                or a.hp>new.hp_max or a.vigor>new.vigor_max
                or new.vp_max<a.vp_max
                or a.vp_available+a.vp_committed+a.vp_spent!=a.vp_max):
            raise UnresolvedDecision("Cannot carry source resources over this level transition")
        delta=new.vp_max-a.vp_max
        trial=deepcopy(a)
        for field in FIELDS:
            setattr(trial,field,deepcopy(getattr(new,field)))
        trial.vp_spent+=delta
        trial.milestones.append(event["event_id"])
        trial.validate()
        proposals[n]=(trial,delta)
    before=party_state(e)
    original_clock={
        key:asdict(ev) for key,ev in e.g4.clock.events.items()
        if ev.actor_id in PARTY
    }
    for n in PARTY:
        target=e.actors[n]
        updated,delta=proposals[n]
        for field in FIELDS:
            setattr(target,field,deepcopy(getattr(updated,field)))
        target.vp_spent+=delta
        target.milestones.append(event["event_id"])
    e.check()
    after=party_state(e)
    for n in PARTY:
        x,y=before[n],after[n]
        if (x["hp"]!=y["hp"] or x["vigor"]!=y["vigor"]
                or x["vp_available"]!=y["vp_available"]
                or x["vp_committed"]!=y["vp_committed"]
                or x["ammunition"]!=y["ammunition"]
                or y["vp_spent"]-x["vp_spent"]!=proposals[n][1]):
            raise AssertionError("Award must not grant HP/Vigor/VP/ammunition refresh")
    if original_clock!={key:asdict(ev) for key,ev in e.g4.clock.events.items()
                       if ev.actor_id in PARTY}:
        raise AssertionError("Award cannot restart, rewrite or shorten old Recovery")
    receipt={
        "event_id":event["event_id"],"beat":event["beat"],
        "from_level":current,"to_level":current+1,
        "prior_party_sha256":canonical_digest(before),
        "advanced_party_sha256":canonical_digest(after),
        "new_vp_capacity_staged_as_spent":{
            n:proposals[n][1] for n in PARTY},
        "world_seconds":e.g4.clock.world_seconds,
        "recovery_deadlines_preserved":True,
        "hp_vigor_available_vp_unchanged":True,
        "author_gm_fixture_only":True,
        "human_milestone_certified":False,
    }
    e.log("b07_milestone_candidate_level_applied",**receipt)
    return receipt


def _entry_l2(source):
    """L1 G0 narrative -> first original G8 L2 encounter without inventing G8 L1.

    This is a distinct, restricted first-entry bridge, NOT a G8 terminal
    handoff. It transfers already level-awarded source snapshots/clock and
    refuses any unresolved poison, host or new G2 shot history.
    """
    if (source.round!=0 or source.g4.clock.mode!="exploration"
            or not any(x["kind"]=="b07_milestone_candidate_level_applied"
                       and x["detail"]["to_level"]==2 for x in source.ledger)
            or source.g4.short_toxins or source.g4.toxins.instances
            or source.g4.toxins.exposure_ids or source.g3.effects
            or source.g4.used_events):
        raise UnresolvedDecision("First G8 entry requires completed clean L1 fixture")
    e,_=_new_scene("soldier",2,0,prepared_only=True)
    _preflight_destination(source,e)
    old,new=source.g4.clock,e.g4.clock
    if any(v.kind!="recovery" and not v.consumed and not v.canceled
           for v in old.events.values()):
        raise UnresolvedDecision("Unsupported old G0 event cannot enter G8")
    prior=party_state(source)
    for n in PARTY:
        a=e.actors[n]
        for field in CARRY_FIELDS:
            setattr(a,field,deepcopy(getattr(source.actors[n],field)))
        e.g2.wielded[n]=set(source.g2.wielded[n])
    for key,ev in list(new.events.items()):
        if ev.actor_id in PARTY:
            del new.events[key]
        else:
            ev.due_seconds+=old.world_seconds
            ev.original_order+=old.world_seconds
            ev.serial+=old.sequence
    new.events.update({key:deepcopy(ev) for key,ev in old.events.items()
                       if ev.actor_id in PARTY})
    for n in PARTY:
        new.recovery_serial[n]=old.recovery_serial[n]
    new.sequence=old.sequence+sum(ev.actor_id not in PARTY
                                 for ev in new.events.values())
    new.world_seconds=old.world_seconds
    e.check()
    if prior!=party_state(e):
        raise AssertionError("First G8 entry altered source-level party resources")
    e.log("b07_l1_noncombat_party_entered_l2_g8",
          L1_ledger_sha256=canonical_digest(source.ledger),
          L2_party_sha256=canonical_digest(prior),
          inherited_world_seconds=new.world_seconds,
          no_L1_G8_terminal_claim=True,
          no_free_restoration=True)
    e.g4.clock.enter_initiative()
    e.begin_round()
    exits=tuple(SceneExit(
        e.scenario,e.g1.scene_id,e.objective,n,EXITS[n],
        f"G8:soldier:{n}:border") for n in PARTY)
    combat=SourceMelee(e,scene_exits=exits,
                       player_benchmark_target="foe")
    return combat


def _l2_withdrawal(combat):
    """Original fixed Soldier opposition, native G0/G2/G4/G5 and border exits."""
    e=combat.e
    for round_no in (1,2):
        if round_no==2:
            combat.bridge.begin_next_round()
        for ident in ("foe",*PARTY):
            _turn(combat,ident)
            if ident=="foe":
                _foe_turn(combat,"soldier","opposed_withdrawal",round_no)
            elif round_no==1 and ident=="archer":
                e.g2.bow_sequence("archer","foe",
                                  (ShotChoice(primary_face=1),))
            elif round_no==2:
                _player_turn(combat,ident,"opposed_withdrawal",round_no,"soldier")
            combat.bridge.end_current_turn()
    result=_terminal(combat,"opposed_withdrawal","soldier")
    if result!="party_scene_withdrawal":
        raise AssertionError("No authenticated original G8 withdrawal terminal")
    e.g4.clock.leave_initiative()
    return result


def run(*,awards=None,travel_seconds=300):
    """Source-bound 3-level cohort candidate; GM milestones are fixture inputs."""
    if type(travel_seconds) is not int or not 0<=travel_seconds<21600:
        raise ValueError("Explicit bounded nonnegative route time required")
    awards=_check_awards(fixture_awards() if awards is None else awards)
    if audit()["issues"]:
        raise UnresolvedDecision("Independent source build audit must be issue-free")
    # Four sessions from original integrated pilot; not reported human play.
    agenda=plan(4)
    if [s["target_start_level"] for s in agenda["sessions"]] != [1,2,2,3]:
        raise AssertionError("Original authored four-session level plan changed")
    l1,checks=_l1()
    l1_state=party_state(l1)
    l1_ledger_sha=canonical_digest(l1.ledger)
    first=award(l1,awards[0])
    combat=_entry_l2(l1)
    l2_entry=party_state(combat.e)
    exit_status=_l2_withdrawal(combat)
    l2_exit=party_state(combat.e)
    l2_ledger_sha=canonical_digest(combat.e.ledger)
    # Deliberate author-declared shrine Milestone Two *candidate*; the L2
    # Soldier witness does NOT prove any actual shrine/GM story outcome.
    second=award(combat.e,awards[1])
    l3,_= _new_scene("sentry_cold",3,0,previous=combat.e,
                    elapsed_seconds=travel_seconds,
                    travel_ref="GM-fixture:shrine-to-village-l3")
    l3_entry=party_state(l3.e)
    result=_resolve_victory(l3,"sentry_cold")
    if result!="sentry_defeat":
        raise AssertionError("Original L3 G8 Sentry terminal missing")
    if (l3.e.actors["archer"].ammunition!=19
            or l3_entry["archer"]["ammunition"]!=19
            or any(a.level!=3 for n,a in l3.e.actors.items() if n in PARTY)):
        raise AssertionError("L3 party or spent Bow arrow reset")
    return {
        "version":VERSION,"source_scope":"author_gm_fixture_not_human_pilot",
        "session_plan_levels":[s["target_start_level"] for s in agenda["sessions"]],
        "actual_g8_combat_levels":[2,3],
        "l1_checks":checks,"l1_state":l1_state,
        "l1_ledger_sha256":l1_ledger_sha,
        "milestone_one":first,
        "l2_entry":l2_entry,"l2_outcome":exit_status,"l2_exit":l2_exit,
        "l2_ledger_sha256":l2_ledger_sha,
        "milestone_two":second,
        "l3_handoff":next(x["detail"] for x in l3.e.ledger
                           if x["kind"]=="b05_b06_native_party_handoff"),
        "l3_entry":l3_entry,"l3_outcome":result,
        "l3_final":party_state(l3.e),
        "l3_ledger_sha256":canonical_digest(l3.e.ledger),
        "actual_source_g0_g4_narrative_ledger":True,
        "original_source_g8_terminals":2,
        "no_L1_G8_replay":True,
        "no_automatic_award":True,
        "no_levelup_resource_refill":True,
        "human_sessions":0,"independently_certified_focuses":0,
        "strict_mvp_exits_met":0,
    }


if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
