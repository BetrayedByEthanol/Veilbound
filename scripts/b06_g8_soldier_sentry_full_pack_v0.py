"""B06 G8: Soldier/Sentry source-native four-PC terminal matrix.

Fixed tactical witness, NOT representative difficulty, general encounter AI,
Hunter CR, arbitrary Bow adjudication, or independent Focus certification.
Every step, attack, spell and exit runs through the existing native G0-G5
adapters. No direct HP assignment or invented terminal damage is permitted.
"""
from copy import deepcopy
from heapq import heappop, heappush
import argparse
import json

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SceneExit, SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import _snapshot, canonical_digest

HISTORICAL_PHASE3_SHA = (
    "c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b"
)
MODES = ("party_victory", "party_defeat", "opposed_withdrawal")
OPPONENTS = {"soldier": ("B06-EN-02", None),
             "sentry_cold": ("B06-EN-01", "cold_start"),
             "sentry_prepared": ("B06-EN-01", "prepared_start")}
PARTY = ("vanguard", "guardian", "archer", "scholar")
PROFILES = {"vanguard": "B06-PC-A-SWORD",
            "guardian": "B06-PC-B-MACE"}
POSITIONS = {"vanguard": (2, 2), "guardian": (3, 3),
             "archer": (1, 4), "scholar": (1, 0)}
EXITS = {"vanguard": (0, 2), "guardian": (3, 6),
         "archer": (0, 4), "scholar": (0, 0)}
EXIT_ROUTES = {"vanguard": ((-1, 0), (-1, 0)),
               "guardian": ((0, 1), (0, 1), (0, 1)),
               "archer": ((-1, 0),), "scholar": ((-1, 0),)}
DELTAS = ((0, -1), (-1, 0), (1, 0), (0, 1),
          (-1, -1), (-1, 1), (1, -1), (1, 1))
MAX_ROUNDS = 48


def _inputs(opponent, level, seed, mode):
    if opponent not in OPPONENTS or mode not in MODES:
        raise ValueError("Select a source Soldier/Sentry and authored G8 terminal policy")
    if type(level) is not int or level not in (2, 3):
        raise ValueError("G8 supports actual L2/L3 A/B/R/F sheets only")
    if type(seed) is not int or seed < 0:
        raise ValueError("G8 requires an exact nonnegative source seed")


def _scene(opponent, level, seed, mode):
    source, state = OPPONENTS[opponent]
    actors = [enemy_actor(source, "foe", "enemy",
                          start_state=state, occupied=((3, 2),))]
    actors.extend(party_actor(role, level, name, "party",
                              occupied=(POSITIONS[name],))
                  for name, role in zip(PARTY, ("A", "B", "R", "F")))
    encounter = Encounter(
        actors, {"foe": 30, "vanguard": 24, "guardian": 20,
                 "archer": 16, "scholar": 12},
        seed=seed, scenario=f"B06-G8:{opponent}:L{level}:P4",
        objective="authenticate_one_fixed_source_terminal_policy",
        policy="bounded_fixed_source_dice_and_declined_optional_responses",
    )
    GridMovement(encounter, width=8, height=7, scene_id="G8-mixed-clear")
    RangedCombat(encounter)
    SpellState(encounter)
    DamageState(encounter)
    encounter.begin_round()
    exits = tuple(SceneExit(encounter.scenario, encounter.g1.scene_id,
                            encounter.objective, name, EXITS[name],
                            f"G8:{opponent}:{name}:border")
                  for name in PARTY) if mode == "opposed_withdrawal" else ()
    combat = SourceMelee(encounter, scene_exits=exits,
                         player_benchmark_target="foe")
    if encounter.order != ("foe", *PARTY):
        raise AssertionError("Wrong source initiative")
    encounter.log("g8_policy_selected", opponent=opponent, level=level,
                  mode=mode, party=list(PARTY), source_id=source,
                  source_digest=encounter.actors["foe"].source.digest)
    return combat


def _turn(combat, actor):
    e = combat.e
    a = e.actors[actor]
    # Genuine mandatory Dying protection when available. No discretionary
    # HP/repair regeneration and no transfer to an unsourced healing policy.
    choice = RegenerationChoice(
        cancel_dying_loss=(a.hp <= 0 and not a.dead and a.vigor > 0))
    combat.bridge.start_next_turn(choice)
    if e.current != actor:
        raise AssertionError("G8 must follow genuine Initiative")
    return e.actors[actor]


def _attack(combat, attacker, target, *, face, die=None, extreme=False):
    e = combat.e
    a = e.actors[attacker]
    profile = (PROFILES[attacker] if attacker in PROFILES else
               "B06-AT-03" if a.source.source_id == "B06-EN-02" else
               e.g3.sentry_profile("foe"))
    if a.hp <= 0 or a.dead or e.actors[target].dead:
        raise UnresolvedDecision("Cannot perform an incapacitated or corpse attack")
    if not e.g1.melee_contact(attacker, target):
        raise UnresolvedDecision("G8 paid attack requires genuine G1 contact")
    sequence = combat.declare(attacker, target, profiles=(profile,),
                              defenses=("take_hit",))
    kwargs = {"attack_face": face}
    if face == 20:
        kwargs.update(confirmation_face=20,
                      critical_dice=(4, 4) if extreme else (1, 1))
    if face != 1:
        kwargs.update(damage_face=die,
                      wound_location_roll=8)
        if profile == "B06-AT-02":
            kwargs["vigor_die"] = 4
    result = combat.resolve(sequence, 0, **kwargs)
    if result["outcome"] != ("miss" if face == 1 else "hit"):
        raise AssertionError("G8 native attack contradicted the authored dice")
    return result


def _route(e, target):
    """Bounded shortest legal cautious G1 path for 1x1 foe, not a teleport."""
    mover = e.actors["foe"]
    start = mover.occupied
    queue = [(0, 0, start, ())]
    best = {start: 0}
    serial = 0
    try:
        while queue:
            cost, _, cell, steps = heappop(queue)
            if cost != best[cell]:
                continue
            mover.occupied = cell
            if e.g1.melee_contact("foe", target):
                return steps
            for delta in DELTAS:
                try:
                    next_cells, mp, _, allies = e.g1.preview(
                        "foe", delta=delta, cautious=True)
                except (UnresolvedDecision, ValueError):
                    continue
                if allies:
                    continue
                new_cost = cost + mp
                if new_cost < best.get(next_cells, 10**9):
                    best[next_cells] = new_cost
                    serial += 1
                    heappush(queue, (new_cost, serial, next_cells,
                                     steps + ((delta, mp),)))
    finally:
        mover.occupied = start
    raise UnresolvedDecision("No legal G1 cautious path to living party target")


def _pursue(combat, target):
    e = combat.e
    route = _route(e, target)
    e.log("g8_source_target_selected", attacker="foe", target=target,
          target_digest=e.actors[target].source.digest,
          authored_cautious_path=[list(delta) for delta, _ in route])
    for delta, quoted_mp in route:
        if e.actors["foe"].mp_remaining < quoted_mp:
            break
        before = e.actors["foe"].mp_remaining
        if not e.g1.step("foe", delta, cautious=True,
                         responses=lambda eligible: ()):
            raise UnresolvedDecision("Actual G8 pursuing step was canceled")
        if e.actors["foe"].mp_remaining != before - quoted_mp:
            raise AssertionError("G1 MP receipt and planned path disagree")
    return e.g1.melee_contact("foe", target)


def _foe_turn(combat, opponent, mode, round_no):
    e = combat.e
    foe = e.actors["foe"]
    if foe.hp <= 0 or foe.dead:
        return
    if opponent == "sentry_cold" and round_no == 1:
        if e.g3.cast_sentry_reserve("foe") is None:
            raise UnresolvedDecision("Cold Sentry must pay its real Reserve")
        return
    if mode == "party_defeat":
        target = next((name for name in PARTY if not e.actors[name].dead), None)
        if target is None:
            return
        if _pursue(combat, target):
            _attack(combat, "foe", target, face=20, die=6, extreme=True)
        return
    # An actual enemy action even in the deliberately favorable victory
    # policy; the natural-1 face still spends one G0 Physical Action.
    target = "vanguard"
    if not e.g1.melee_contact("foe", target) or e.actors[target].dead:
        raise UnresolvedDecision("Fixed G8 opposition lost its source contact")
    if mode == "party_victory":
        _attack(combat, "foe", target, face=1)
    else:
        _attack(combat, "foe", target, face=12, die=1)


def _player_turn(combat, actor, mode, round_no, opponent):
    e = combat.e
    a = e.actors[actor]
    if a.dead or a.hp <= 0 or mode == "party_defeat":
        return
    if mode == "opposed_withdrawal":
        # Cold Sentry must first spend its separate Round-1 Projection and
        # make a genuinely paid enhanced attack on Round 2 before withdrawal.
        if opponent == "sentry_cold" and round_no == 1:
            return
        for delta in EXIT_ROUTES[actor]:
            if not e.g1.step(actor, delta, cautious=True,
                             responses=lambda eligible: ()):
                raise UnresolvedDecision("G8 authored party exit canceled")
        combat.withdraw(actor)
        return
    if e.actors["foe"].dead:
        return
    if actor in PROFILES:
        _attack(combat, actor, "foe", face=12, die=4)
    elif actor == "archer" and round_no == 1:
        # Real R Chosen maintained Self Guided Rite; not a fictional Bow
        # damage resolver against enemies (G6-D Bow lethal is Hunter-only).
        if e.g3.cast_guided("archer", mode="maintained", chosen=True) is None:
            raise UnresolvedDecision("G8 R Chosen Rite did not establish")
    elif actor == "scholar" and round_no <= 2:
        result = e.g3.cast_flame(
            "scholar", "foe", tier=1, face=12, vigor_die=3,
            defense="take_hit", hand_available=True, wound_location_roll=8)
        if result["outcome"] != "direct_hit_resolved_G4":
            raise UnresolvedDecision("G8 F Flame must be genuinely delivered")


def _terminal(combat, mode, opponent):
    e = combat.e
    if e.current is not None or e.cursor != len(e.order):
        raise AssertionError("G8 terminal requires finished genuine Round End")
    if combat.pending_attack_slots():
        raise AssertionError("Cannot certify G8 with unpaid-resolution G5 slots")
    events = e.ledger
    if mode == "party_victory":
        if not e.actors["foe"].dead or not any(
                x["kind"] == "g4_damage_applied"
                and x["detail"].get("recipient") == "foe"
                and x["detail"].get("dead") is True for x in events):
            return None
        outcome = "soldier_defeat" if opponent == "soldier" else "sentry_defeat"
    elif mode == "party_defeat":
        if not all(e.actors[name].dead for name in PARTY):
            return None
        if len({x["detail"].get("recipient") for x in events
                if x["kind"] == "g4_damage_applied"
                and x["detail"].get("dead") is True}) < 4:
            raise AssertionError("G8 defeat needs four independent fatal transitions")
        outcome = "party_defeat"
    else:
        exits = [x for x in events if x["kind"] == "g5_terminal_exit"]
        if (len(exits) != len(PARTY)
                or {x["detail"]["actor"] for x in exits} != set(PARTY)
                or e.actors["foe"].dead
                or any(e.actors[name].dead or e.actors[name].hp <= 0
                       for name in PARTY)):
            return None
        outcome = "party_scene_withdrawal"
    if not any(x["kind"] == "round_end" and x["round"] == e.round
               for x in events):
        raise AssertionError("G8 needs actual native Round End")
    e.log("g8_bounded_terminal_attested", opponent=opponent, mode=mode,
          outcome=outcome, round=e.round, party=list(PARTY),
          opponent_source=e.actors["foe"].source.digest,
          original_evidence_indices=[
              x["index"] for x in events if x["kind"] in
              ("g5_melee_resolved", "g45_attested_hit", "g5_terminal_exit",
               "g3_flame_launched", "g3_effect_established")],
          representative=False, hunter_cr=None)
    return outcome


def run_policy(*, opponent, level=3, seed=0, mode):
    """Run exactly one original source policy; no winner injected on timeout."""
    _inputs(opponent, level, seed, mode)
    combat = _scene(opponent, level, seed, mode)
    e = combat.e
    outcome = None
    for round_no in range(1, MAX_ROUNDS + 1):
        if e.round != round_no:
            combat.bridge.begin_next_round()
        for actor in ("foe", *PARTY):
            _turn(combat, actor)
            if actor == "foe":
                _foe_turn(combat, opponent, mode, round_no)
            else:
                _player_turn(combat, actor, mode, round_no, opponent)
            combat.bridge.end_current_turn()
        outcome = _terminal(combat, mode, opponent)
        if outcome is not None:
            break
    e.check()
    result = {
        "version": "B06-G8-v0", "opponent": opponent, "level": level,
        "seed": seed, "mode": mode, "rounds_completed": e.round,
        "outcome": outcome if outcome is not None else "unresolved_round_ceiling",
        "final_state": _snapshot(e), "ledger": deepcopy(e.ledger),
        "source_ids": {a: e.actors[a].source.source_id
                       for a in ("foe", *PARTY)},
        "bounded_source_terminal_certified": outcome is not None,
        "complete_representative_party_pack_certified": False,
        "representative_encounter_calibration_accepted": False,
        "sampled_win_rate": None, "confidence_interval": None,
        "hunter_cr": None, "historical_phase3_sha256": HISTORICAL_PHASE3_SHA,
    }
    result["ledger_sha256"] = canonical_digest(result["ledger"])
    return result


def attest_policy(report, *, opponent, level=3, seed=0, mode):
    """Fail closed against any rehashed/altered report: replay trusted source."""
    _inputs(opponent, level, seed, mode)
    if not isinstance(report, dict):
        raise AssertionError("G8 attestation requires complete native report")
    trusted = run_policy(opponent=opponent, level=level, seed=seed, mode=mode)
    if (canonical_digest(report.get("ledger")) != report.get("ledger_sha256")
            or report != trusted):
        raise AssertionError("G8 source-native report differs from independent replay")
    if not trusted["bounded_source_terminal_certified"]:
        raise AssertionError("Unresolved G8 branch has no native terminal")
    return deepcopy(trusted)


def run_pack(*, opponent, level=3, seed=0):
    """Three independently replayed source outcomes; strictly fixed policies."""
    if opponent not in OPPONENTS:
        raise ValueError("Unknown G8 opponent")
    paths = {mode: run_policy(opponent=opponent, level=level,
                              seed=seed, mode=mode) for mode in MODES}
    for mode, report in paths.items():
        attest_policy(report, opponent=opponent, level=level,
                      seed=seed, mode=mode)
    if (paths["party_victory"]["outcome"] not in
            ("soldier_defeat", "sentry_defeat")
            or paths["party_defeat"]["outcome"] != "party_defeat"
            or paths["opposed_withdrawal"]["outcome"] != "party_scene_withdrawal"):
        raise AssertionError("G8 authored terminal matrix is incomplete")
    digests = {mode: paths[mode]["ledger_sha256"] for mode in MODES}
    if len(set(digests.values())) != len(MODES):
        raise AssertionError("G8 distinct policies must have distinct native evidence")
    return {"version": "B06-G8-v0", "opponent": opponent, "level": level,
            "seed": seed, "terminals": {m: p["outcome"] for m,p in paths.items()},
            "source_ledger_sha256": digests,
            "bounded_three_terminal_matrix_certified": True,
            "complete_representative_party_pack_certified": False,
            "human_policy_weights": None, "sampled_win_rate": None,
            "hunter_cr": None, "historical_phase3_sha256": HISTORICAL_PHASE3_SHA}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opponent", choices=tuple(OPPONENTS), required=True)
    parser.add_argument("--level", type=int, choices=(2, 3), default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--mode", choices=MODES, default=None)
    args = parser.parse_args()
    result = (run_policy(opponent=args.opponent, level=args.level,
                         seed=args.seed, mode=args.mode)
              if args.mode else run_pack(opponent=args.opponent,
                                         level=args.level, seed=args.seed))
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
