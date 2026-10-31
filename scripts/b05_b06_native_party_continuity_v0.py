"""B05/B06 v0: actual native G0/G2/G3/G4 state across discrete encounters.

NARROW live-instance transfer; not a general save format or character importer.
Fail closed on unhandled active poison/Veil effects, pending actions or clock
milestones. Never recreate full-resource source defaults during handoff.
"""
from copy import deepcopy
from dataclasses import asdict
import argparse
import json

from scripts.b06_encounter_state_v0 import (
    Encounter, UnresolvedDecision, party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat, ShotChoice
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_world_clock_v0 import SIX_HOURS
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_g8_soldier_sentry_full_pack_v0 import (
    PARTY, POSITIONS, OPPONENTS, MAX_ROUNDS, _inputs, _scene, _turn,
    _foe_turn, _player_turn, _terminal,
)

VERSION = "B05-B06-Native-Party-Cross-Encounter-v0"
ROLES = dict(zip(PARTY, ("A", "B", "R", "F")))
CARRY_FIELDS = (
    "hp", "vigor", "vp_available", "vp_committed", "vp_spent",
    "ammunition", "wounds", "conditions", "milestones",
    "maintained", "ready_guard", "blink_debt_due", "blink_debt_next",
)
HOLD_EFFECTS = frozenset(("Guided Regeneration",))


def party_state(e):
    """Exact resource witnesses, including wounds and live maintained hosts."""
    return {ident: {
        "role": ROLES[ident], "level": e.actors[ident].level,
        "source_id": e.actors[ident].source.source_id,
        "source_digest": e.actors[ident].source.digest,
        "source_path": e.actors[ident].source.path,
        **{field: deepcopy(getattr(e.actors[ident], field))
           for field in CARRY_FIELDS if field != "wounds"},
        "wounds": [asdict(w) for w in e.actors[ident].wounds],
        "wielded": sorted(e.g2.wielded[ident]),
        "effects": [asdict(v) for v in e.g3.effects.values()
                    if v.caster == ident or v.recipient == ident],
    } for ident in PARTY}


def _boundary(e, *, carry_effects=False):
    if (not e.round or e.current is not None or
            e.cursor != len(e.order) or e.pending_regeneration is not None
            or not any(v["kind"] == "round_end" and v["round"] == e.round
                       for v in e.ledger)
            or e.reservations
            or (getattr(e, "g5", None) is not None and
                e.g5.pending_attack_slots())
            or e.g1 is None or e.g2 is None or e.g3 is None or e.g4 is None
            or e.g1.pounce is not None
            or e.g4.clock.mode != "exploration"):
        raise UnresolvedDecision("Only settled, exited native encounter boundary")
    terminals = [v for v in e.ledger
                 if v["kind"] == "g8_bounded_terminal_attested"
                 and v["detail"].get("outcome") in
                     ("soldier_defeat", "sentry_defeat", "party_scene_withdrawal")
                 and v["round"] == e.round]
    if len(terminals) != 1:
        raise UnresolvedDecision("Original G8 source terminal required for scene handoff")
    if any(e.g2.aims.get(n) for n in PARTY):
        raise UnresolvedDecision("Unresolved Bow Aim cannot disappear between scenes")
    # B06 G4.3/G4.4 and delayed short toxin effects require their complete
    # event/phase interpreters. Do not copy just a misleading HP snapshot.
    if not carry_effects and (any(t.get("left", 0) for t in e.g4.short_toxins
            if t.get("recipient") in PARTY)
            or any(t.get("active") and t.get("recipient") in PARTY
                   for t in e.g4.toxins.instances.values())
            or any(t.get("active") and t.get("recipient") in PARTY
                   for t in e.g4.venom.effects.values())):
        raise UnresolvedDecision("Active poison/Endurance requires dedicated source handoff")
    if not carry_effects and any(v.kind != "recovery" and v.actor_id in PARTY
           and not v.consumed and not v.canceled
           for v in e.g4.clock.events.values()):
        raise UnresolvedDecision("Active non-recovery milestone cannot be dropped")
    if not carry_effects and any(getattr(e.actors[n], "toxin_modifiers", {}) for n in PARTY):
        raise UnresolvedDecision("Unhandled actor toxin modifiers")
    for ident in PARTY:
        a=e.actors[ident]
        effects=[v for v in e.g3.effects.values()
                 if v.caster==ident or v.recipient==ident]
        if (any(
                not (
                    (v.kind == "Guided Regeneration"
                     and a.source.source_id=="R" and v.committed==1
                     and v.chosen and v.resistance==0)
                    or
                    (carry_effects and v.kind=="Stone Skin"
                     and a.source.source_id=="F"
                     and v.committed==(a.vp_max+2)//3
                     and not v.chosen and v.resistance==2)
                )
                or v.caster != ident or v.recipient != ident
                or v.anchor is not None or v.parent is not None
                or v.expiry_round is not None
                for v in effects)
                or {v.ident for v in effects} != set(a.maintained)
                or sum(v.committed for v in effects) != a.vp_committed):
            raise UnresolvedDecision("Unreconstructible maintained VP/host state")
    # A hostile caster's maintained effect on a party recipient is not lost.
    if any(v.recipient in PARTY and v.caster not in PARTY
           for v in e.g3.effects.values()):
        raise UnresolvedDecision("Hostile ongoing effects require separate scene authority")
    if any(a.hp <= 0 or a.dead for n,a in e.actors.items() if n in PARTY):
        raise UnresolvedDecision("This pilot requires a living mobile party")
    e.check()
    if carry_effects:
        from scripts.b05_b06_cross_encounter_effect_continuity_v0 import validate_source
        validate_source(e)


def _preflight_destination(previous, following):
    """Validate the entire destination before G4.2 travel can change source.

    Party G0 actors, G2 equipment, G3 hosts and G4.2 event identities must
    still be their source-created defaults. A Sentry's preauthored foe-host
    remains legal; no destination party effect or edited clock does.
    """
    if (following.round != 0 or following.current is not None
            or following.pending_regeneration is not None
            or following.g4 is None or following.g3 is None
            or following.g2 is None or following.g1 is None
            or getattr(following, "g5", None) is not None
            or set(PARTY) - set(following.actors)):
        raise UnresolvedDecision("Fresh G0-G4 scene required; cannot overwrite live actions")

    for n in PARTY:
        candidate = following.actors[n]
        fresh = party_actor(ROLES[n], candidate.level, n, "party",
                            occupied=candidate.occupied)
        source_equipment = {
            item for item, state in candidate.source.equipment
            if state is True or state == "wielded"
        }
        if (candidate.source != previous.actors[n].source
                or candidate.level != previous.actors[n].level
                or candidate.team != "party"
                or candidate.source != fresh.source
                or any(getattr(candidate, f) != getattr(fresh, f)
                       for f in CARRY_FIELDS)
                or following.g2.wielded.get(n) != source_equipment
                or following.g2.aims.get(n) is not None
                or following.g2.own_turn_number.get(n) != 0):
            raise UnresolvedDecision("Following actor must be pristine SAME source")

    # Existing party-owned/targeted G3 effects cannot be overwritten. The
    # original enemy's prepared Reserve (if any) is separately preserved.
    if (following.g3.next_effect != 0
            or any(v.caster in PARTY or v.recipient in PARTY
                   for v in following.g3.effects.values())
            or any(key[0] in PARTY for key in following.g3.effects)):
        raise UnresolvedDecision("Destination already owns a party effect/host")

    # G4.3/G4.4 toxins, even rejected/expired exposure histories, are
    # live source-owned state. Unlike G3 effects, an active legacy TX-HM
    # can have NO actor modifier or clock milestone and so can pass every
    # other pristine-scene check. Never erase its remaining ticks, replay
    # keys or existing Endurance merely by importing a different party.
    d = following.g4
    if (d.short_toxins or d.toxins.instances or d.toxins.exposure_ids
            or d.venom.effects or d.venom.next_effect != 0
            or d.venom.hit_keys or d.venom.hunter_keys
            or d.used_events
            or getattr(d, "legacy_toxin_provenance", {})):
        raise UnresolvedDecision(
            "Destination G4 toxin, Endurance or exposure history is not pristine")
    if any(getattr(a, "toxin_modifiers", {})
           for a in following.actors.values()):
        raise UnresolvedDecision(
            "Destination has pre-existing G4 toxin penalties")

    # Only one original Recovery checkpoint per actor is permitted in the
    # new scene. Any caller-supplied milestone or colliding future Recovery
    # ID must be refused BEFORE the prior clock advances even one second.
    clock = following.g4.clock
    expected = {f"recovery:{ident}:1" for ident in following.actors}
    if (clock.mode != "exploration" or clock.world_seconds != 0
            or clock.entry_round is not None
            or set(clock.events) != expected
            or set(clock.recovery_serial) != set(following.actors)
            or clock.sequence != len(expected)):
        raise UnresolvedDecision("Destination clock is not a pristine source clock")
    for ident, actor in following.actors.items():
        ev = clock.events[f"recovery:{ident}:1"]
        if (ev.actor_id != ident
                or ev.actor_source != actor.source.source_id
                or ev.source_digest != actor.source.digest
                or ev.kind != "recovery"
                or ev.phase != "recovery"
                or ev.source != "canonical:6h-recovery"
                or ev.due_seconds != SIX_HOURS
                or ev.original_order != SIX_HOURS
                or ev.due_round is not None
                or ev.consumed or ev.canceled
                or clock.recovery_serial[ident] != 2):
            raise UnresolvedDecision("Destination recovery checkpoint was altered")
    if any(key in clock.events and clock.events[key].actor_id not in PARTY
           for key, ev in previous.g4.clock.events.items()
           if ev.actor_id in PARTY):
        raise UnresolvedDecision("Recovery/milestone ID collision")
    following.check()


def handoff(previous, following, *, elapsed_seconds, travel_ref,
            carry_effects=False):
    """Bind TWO live encounter objects; no caller-authored snapshot injection.

    previous: source-attested complete G5 terminal and exited G4.2 initiative
    following: fresh original sourced G0 actors, installed G1/G2/G3/G4;
               BEFORE its first Round Begin and any native action.
    """
    if type(elapsed_seconds) is not int or elapsed_seconds < 0:
        raise ValueError("Elapsed travel is source-paid whole seconds")
    if type(travel_ref) is not str or not travel_ref.strip():
        raise ValueError("A distinct authored between-scene route reference is required")
    if type(carry_effects) is not bool:
        raise ValueError("Effect continuation must be an explicit boolean")
    _boundary(previous, carry_effects=carry_effects)
    # Destination feasibility is a read-only precondition. A rejected actor,
    # item, G3 effect or ClockEvent must not consume source travel or Recovery;
    # correcting that destination and retrying the same interval is safe.
    _preflight_destination(previous, following)
    if carry_effects:
        # Genuine scheduled toxins can deliver fatal damage or expire through
        # recovery. Evaluate a DEEP native copy before spending the original
        # party's world time, so unsupported after-travel state cannot charge
        # the same route twice when a destination must be corrected.
        trial=deepcopy(previous)
        trial.g4.clock.advance_exploration(elapsed_seconds)
        _boundary(trial, carry_effects=True)
    # All authorizations are settled before actual source world time moves.
    previous.g4.clock.advance_exploration(elapsed_seconds)
    _boundary(previous, carry_effects=carry_effects)
    outgoing=party_state(previous)
    old_clock=previous.g4.clock
    next_clock=following.g4.clock
    carried_events={key:deepcopy(v) for key,v in old_clock.events.items()
                    if v.actor_id in PARTY}
    for n in PARTY:
        a=following.actors[n]
        source=previous.actors[n]
        for field in CARRY_FIELDS:
            setattr(a,field,deepcopy(getattr(source,field)))
        following.g2.wielded[n]=set(previous.g2.wielded[n])
    # Carry source-paid commitments WITHOUT calling _pay or creating a second
    # maintained instance. Source-authenticated G3 effect identities survive.
    for v in previous.g3.effects.values():
        if v.caster in PARTY:
            following.g3.effects[(v.caster,v.ident)]=deepcopy(v)
    following.g3.next_effect=max(
        (int(v.ident[3:]) for v in following.g3.effects.values()
         if v.ident.startswith("G3-") and v.ident[3:].isdigit()),default=0)
    # Retain the actual exact G4.2 Recovery checkpoint IDs + their original
    # due seconds. New adversaries start a NEW six-hour phase at arrival.
    for key,ev in list(next_clock.events.items()):
        if ev.actor_id in PARTY:
            del next_clock.events[key]
        else:
            ev.due_seconds += old_clock.world_seconds
            ev.original_order += old_clock.world_seconds
            ev.serial += old_clock.sequence
    next_clock.events.update(carried_events)
    for n in PARTY:
        next_clock.recovery_serial[n]=old_clock.recovery_serial[n]
    next_clock.sequence=old_clock.sequence+len(
        [v for v in next_clock.events.values() if v.actor_id not in PARTY])
    next_clock.world_seconds=old_clock.world_seconds
    if carry_effects:
        from scripts.b05_b06_cross_encounter_effect_continuity_v0 import restore
        restore(previous, following)
    following.check()
    incoming=party_state(following)
    # Positions intentionally belong to the independently authored new
    # scene; resources, held equipment and maintained magic MUST be identical.
    if incoming != outgoing:
        raise AssertionError("Actual G0/G2/G3 carried state changed on import")
    previous_digest=canonical_digest(previous.ledger)
    if carry_effects:
        from scripts.b05_b06_cross_encounter_effect_continuity_v0 import effect_state
        effect_digest=canonical_digest(effect_state(following))
    else:
        effect_digest=None
    receipt={
        "travel_ref":travel_ref,"elapsed_seconds":elapsed_seconds,
        "prior_scene":previous.scenario,"next_scene":following.scenario,
        "old_terminal_ledger_sha256":previous_digest,
        "prior_party_sha256":canonical_digest(outgoing),
        "incoming_party_sha256":canonical_digest(incoming),
        "world_seconds":old_clock.world_seconds,
        "pending_recovery":{
            n:[{"id":v.ident,"due_seconds":v.due_seconds}
               for v in old_clock._pending()
               if v.kind=="recovery" and v.actor_id==n]
            for n in PARTY},
        "no_free_restore":True,
        "native_effect_continuation_sha256":effect_digest,
        "effect_continuation_enabled":carry_effects,
        "new_scene_positions_author_declared_not_G1_teleport":True,
    }
    following.log("b05_b06_native_party_handoff",**receipt)
    return receipt


def _new_scene(opponent, level, seed, *, previous=None, elapsed_seconds=0,
               travel_ref="", prepared_only=False, carry_effects=False):
    _inputs(opponent,level,seed,"party_victory")
    source,state=OPPONENTS[opponent]
    actors=[enemy_actor(source,"foe","enemy",start_state=state,
                        occupied=((3,2),))]
    actors += [party_actor(ROLES[n],level,n,"party",
                           occupied=(POSITIONS[n],)) for n in PARTY]
    e=Encounter(actors,{"foe":30,"vanguard":24,"guardian":20,
                        "archer":16,"scholar":12},seed=seed,
                scenario=f"B06-G8:{opponent}:L{level}:P4",
                objective="authenticate_one_fixed_source_terminal_policy",
                policy="bounded_fixed_source_dice_and_declined_optional_responses")
    GridMovement(e,width=8,height=7,scene_id="G8-mixed-clear")
    RangedCombat(e)
    SpellState(e)
    DamageState(e)
    if prepared_only:
        if previous is not None:
            raise ValueError("Prepared-only scene cannot import yet")
        return e,None
    receipt=handoff(previous,e,elapsed_seconds=elapsed_seconds,
                    travel_ref=travel_ref,
                    carry_effects=carry_effects) if previous is not None else None
    e.g4.clock.enter_initiative()
    e.begin_round()
    combat=SourceMelee(e,player_benchmark_target="foe")
    return combat,receipt


def _resolve_victory(combat,opponent):
    e=combat.e
    result=None
    for round_no in range(1,MAX_ROUNDS+1):
        if e.round != round_no:
            combat.bridge.begin_next_round()
        for ident in ("foe",*PARTY):
            _turn(combat,ident)
            if ident=="foe":
                _foe_turn(combat,opponent,"party_victory",round_no)
            elif not (ident=="archer" and
                      any(v.caster=="archer" and v.kind=="Guided Regeneration"
                          for v in e.g3.effects.values())):
                _player_turn(combat,ident,"party_victory",round_no,opponent)
            combat.bridge.end_current_turn()
        result=_terminal(combat,"party_victory",opponent)
        if result is not None:
            break
    if result is None:
        raise UnresolvedDecision("No native source terminal at round ceiling")
    e.g4.clock.leave_initiative()
    return result


def _first_withdrawal(level, seed):
    """Original G8 terminal with actual native Soldier harm and spent arrow."""
    _inputs("soldier",level,seed,"opposed_withdrawal")
    first=_scene("soldier",level,seed,"opposed_withdrawal")
    first.e.g4.clock.enter_initiative()
    # Round 1: source-paid ordinary Bow launch deliberately misses; the
    # arrow is consumed by native G2, not decremented by the handoff code.
    # Other PCs hold this round while the original Soldier attacks A.
    for round_no in (1, 2):
        if round_no == 2:
            first.bridge.begin_next_round()
        for ident in ("foe",*PARTY):
            _turn(first,ident)
            if ident == "foe":
                _foe_turn(first,"soldier","opposed_withdrawal",round_no)
            elif round_no == 1 and ident == "archer":
                first.e.g2.bow_sequence(
                    "archer","foe",(ShotChoice(primary_face=1),))
            elif round_no == 2:
                _player_turn(first,ident,"opposed_withdrawal",round_no,"soldier")
            first.bridge.end_current_turn()
    if first.e.actors["archer"].ammunition != 19:
        raise AssertionError("G2 must actually consume the source Bow arrow")
    outcome1=_terminal(first,"opposed_withdrawal","soldier")
    if outcome1!="party_scene_withdrawal":
        raise AssertionError("First original G8 exit was not authenticated")
    first.e.g4.clock.leave_initiative()
    return first.e


def run_chain(*,level=3,seed=0,travel_seconds=300):
    """Opposed G8 withdrawal -> paid travel -> native Sentry victory.

    First encounter is an unmodified G8 pre-existing policy. Second one
    imports its live party rather than permitting G8 _scene() to reset.
    """
    if type(travel_seconds) is not int or travel_seconds < 0:
        raise ValueError("Nonnegative authored elapsed seconds required")
    first_e=_first_withdrawal(level,seed)
    outcome1="party_scene_withdrawal"
    combat,receipt=_new_scene(
        "sentry_cold",level,seed,previous=first_e,
        elapsed_seconds=travel_seconds,travel_ref="authored:gate-to-sentry:route")
    outcome2=_resolve_victory(combat,"sentry_cold")
    next_state=party_state(combat.e)
    return {
        "version":VERSION,"level":level,"seed":seed,
        "outcomes":(outcome1,outcome2),
        "handoff":receipt,
        "first_state":party_state(first_e),
        "second_final_state":next_state,
        "first_ledger_sha256":canonical_digest(first_e.ledger),
        "second_ledger_sha256":canonical_digest(combat.e.ledger),
        "same_party_source_all_scenes":True,
        "actual_enemy_contact":True,
        "no_new_recovery_or_ammunition":True,
        "source_bound_native_witnesses":2,
        "gm_human_sessions":0,"independently_certified_focuses":0,
        "strict_mvp_exits_met":0,"representative_balance":False,
        "hunter_cr":None,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level",type=int,default=3)
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--travel-seconds",type=int,default=300)
    args=parser.parse_args()
    print(json.dumps(run_chain(level=args.level,seed=args.seed,
                               travel_seconds=args.travel_seconds),
                     sort_keys=True,indent=2))


if __name__=="__main__":
    main()
