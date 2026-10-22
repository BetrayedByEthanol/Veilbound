"""B06 G7-G — source-native Hunter pursuit and opposed terminal witnesses.

Two deliberately authored policies, not general Hunter AI or representative
combat sampling. Every Bite is a G0-paid G5/G4.5/G4 action; every relocation
is actual G1 translation/pivot. Dying, dead and exited actors are distinct.
No CR, universal Hunter escape rules or fictitious post-fight safety.
"""
from collections import Counter
from heapq import heappop, heappush
import json

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import (
    _snapshot, _validate_native_ledger, canonical_digest,
)
from scripts.b06_g7c_party_terminals_v0 import PartyTerminal
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene

MODES = ("multitarget_defeat", "opposed_disengagement")
HISTORICAL_SHA = "c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b"
MAX_ROUNDS = 32
# Stable tie order for route planning only. Every committed move is still
# checked, paid, and source-logged by G1 before any subsequent attack.
TRANSLATIONS = ((-1, 0), (0, 1), (0, -1), (1, 0),
                (-1, 1), (-1, -1), (1, 1), (1, -1))
PIVOTS = (("head", False), ("head", True),
          ("rear", False), ("rear", True))
OPENING_ROUTES = {
    "vanguard": ((-1, 0),),
    "guardian": ((0, 1), (0, 1)),
    "archer": (),
    "scholar": (),
}
FINAL_ROUTES = {
    "vanguard": ((-1, 0),),
    "guardian": ((0, 1),),
    "archer": ((-1, 0),),
    "scholar": ((-1, 0),),
}


def _next(combat, actor):
    e = combat.e
    a = e.actors[actor]
    # A conscious actor explicitly forgoes discretionary regeneration;
    # a Dying actor pays real Vigor to stop mandatory Dying loss when able.
    # This fixed witness does not let a PC die from a fabricated timeout.
    choice = RegenerationChoice(
        cancel_dying_loss=(a.hp <= 0 and not a.dead and a.vigor > 0))
    combat.bridge.start_next_turn(choice)
    if e.current != actor:
        raise AssertionError("G7-G must consume actual native Initiative")
    return a


def _bite(combat, target, *, devastating):
    """Single genuine G5 attack; extremal faces are a *fixed-dice witness*."""
    e = combat.e
    if e.current != "hunter" or not e.g1.melee_contact(
            "hunter", target, hunter_front=True):
        raise UnresolvedDecision("Hunter Bite requires real head-forward G1 contact")
    t = e.actors[target]
    if t.dead:
        raise UnresolvedDecision("Hunter cannot Bite a corpse")
    sequence = combat.declare(
        "hunter", target, profiles=("B06-AT-04",), defenses=("take_hit",))
    if devastating:
        dice = {"attack_face": 20, "confirmation_face": 20,
                "critical_dice": (4, 4), "damage_face": 6,
                "wound_location_roll": 8, "venom_resistance_die": 20}
    else:
        dice = {"attack_face": 12, "damage_face": 1,
                "wound_location_roll": 8, "venom_resistance_die": 20}
    result = combat.resolve(sequence, 0, **dice)
    if result["outcome"] != "hit":
        raise UnresolvedDecision("Authored native Hunter Bite did not hit")
    return result


def _route_to_contact(e, target):
    """Dijkstra over G1 previews, not invented displacement.

    Temporarily substitute a *hypothetical* rigid Hunter footprint only
    while asking the existing G1 preview for legality and exact Cautious
    MP prices. Restore the real footprint before every actual G1 move.
    Cautious costs explicitly suppress paid Opportunity ambiguity; this
    is an authored policy choice, not blanket immunity to all responses.
    """
    h = e.actors["hunter"]
    g = e.g1
    destination = e.actors[target].occupied
    if len(destination) != 1 or e.actors[target].dead:
        raise UnresolvedDecision("Pursuit requires one actual living/Dying PC")
    start = h.occupied
    best = {start: 0}
    queue = [(0, 0, start, ())]
    ordinal = 0
    try:
        while queue:
            cost, _, state, path = heappop(queue)
            if best[state] != cost:
                continue
            h.occupied = state
            if g.front("hunter") == destination[0]:
                return path
            for kind, argument, second in (
                    [("step", d, None) for d in TRANSLATIONS] +
                    [("pivot", anchor, clockwise)
                     for anchor, clockwise in PIVOTS]):
                try:
                    if kind == "step":
                        next_state, mp, _, allies = g.preview(
                            "hunter", delta=argument, cautious=True)
                    else:
                        next_state, mp, _, allies = g.preview(
                            "hunter", pivot=argument, clockwise=second,
                            cautious=True)
                    if allies:
                        continue
                except (ValueError, UnresolvedDecision):
                    continue
                new_cost = cost + mp
                if new_cost < best.get(next_state, 10**9):
                    best[next_state] = new_cost
                    ordinal += 1
                    heappush(queue, (new_cost, ordinal, next_state,
                                     path + ((kind, argument, second, mp),)))
    finally:
        h.occupied = start
    raise UnresolvedDecision("No G1 legal Hunter route to living target")


def _pursue(combat, target):
    e = combat.e
    h = e.actors["hunter"]
    start = h.occupied
    route = _route_to_contact(e, target)
    steps = []
    e.log("g7g_hunter_target_selected", hunter="hunter", target=target,
          target_source=e.actors[target].source.source_id,
          initial_footprint=start, declared_cautious_route=tuple(
              (kind, argument, clockwise, cost)
              for kind, argument, clockwise, cost in route))
    for kind, argument, clockwise, expected in route:
        if expected > h.mp_remaining:
            break
        if kind == "step":
            before = len(e.ledger)
            moved = e.g1.step("hunter", argument, cautious=True, responses=())
        else:
            before = len(e.ledger)
            moved = e.g1.pivot("hunter", argument, clockwise=clockwise,
                               cautious=True, responses=())
        if not moved:
            raise UnresolvedDecision("Native G1 pursuit move cancelled")
        events = [v for v in e.ledger[before:]
                  if v["kind"] == "g1_movement_step"
                  and v["detail"].get("actor") == "hunter"]
        if len(events) != 1 or events[0]["detail"]["cost"] != expected:
            raise AssertionError("G7-G pursuit step not sourced from paid G1 MP")
        steps.append(events[0]["index"])
    contact = e.g1.melee_contact("hunter", target, hunter_front=True)
    e.log("g7g_hunter_pursuit_executed", hunter="hunter", target=target,
          initial_footprint=start, final_footprint=h.occupied,
          movement_indices=steps, mp_remaining=h.mp_remaining,
          contact=contact)
    return contact


def _native_deaths(e, party):
    deaths = []
    for actor in party:
        a = e.actors[actor]
        if a.dead and a.hp == -a.hp_max:
            found = [v for v in e.ledger if v["kind"] == "g4_damage_applied"
                     and v["detail"].get("recipient") == actor
                     and v["detail"].get("dead") is True
                     and v["detail"].get("cause") == "source-profile:B06-AT-04"]
            if len(found) != 1:
                raise UnresolvedDecision("G7-G death must be unique actual Hunter Bite")
            deaths.append({"actor": actor, "lethal_index": found[0]["index"]})
    return deaths


def _defeat(level, size, seed):
    c = mixed_scene(level=level, size=size, seed=seed)
    e = c.e
    party = e.order[1:]
    e.log("g7g_policy_selected", mode="multitarget_defeat",
          level=level, party_size=size, seed=seed, scenario=e.scenario)
    initial = _snapshot(e)
    outcome = None
    terminal = None
    target_history = []
    rounds = 0
    for round_no in range(1, MAX_ROUNDS + 1):
        if round_no > 1:
            c.bridge.begin_next_round()
        target = next((p for p in party if not e.actors[p].dead), None)
        for actor in e.order:
            _next(c, actor)
            if actor == "hunter" and target is not None:
                target_history.append(target)
                if _pursue(c, target):
                    _bite(c, target, devastating=True)
            # All other characters explicitly hold actions, retain their
            # real turn, and do not magically heal or teleport into contact.
            c.bridge.end_current_turn()
        rounds += 1
        if all(e.actors[p].dead for p in party):
            terminal = PartyTerminal(c).attest_defeat()
            outcome = "party_defeat_attested"
            break
    if outcome is None:
        outcome = "legal_window_cutoff"
    if terminal:
        sources = _native_deaths(e, party)
        if (len(sources) != size or len(set(target_history)) != size
                or terminal["lethal_damage_indices"] !=
                   [x["lethal_index"] for x in sources]):
            raise AssertionError("G7-G defeat lacks distinct native Hunter victims")
        e.log("g7g_multitarget_defeat_verified",
              party=party, native_terminal_index=terminal["terminal_event"],
              lethal_damage_indices=terminal["lethal_damage_indices"],
              distinct_targets=tuple(dict.fromkeys(target_history)),
              hunter_alive=not e.actors["hunter"].dead)
    return c, initial, terminal, outcome, rounds


def _withdraw(level, size, seed):
    c = mixed_scene(level=level, size=size, seed=seed, party_exits=True)
    e = c.e
    party = e.order[1:]
    e.log("g7g_policy_selected", mode="opposed_disengagement",
          level=level, party_size=size, seed=seed, scenario=e.scenario)
    initial = _snapshot(e)
    # Round 1: Hunter pays an ordinary Bite, while the source PCs make
    # preparatory *real* G1 Cautious steps. None claims an early terminal.
    _next(c, "hunter")
    _bite(c, "vanguard", devastating=False)
    c.bridge.end_current_turn()
    for actor in party:
        _next(c, actor)
        for delta in OPENING_ROUTES[actor]:
            if not e.g1.step(actor, delta, cautious=True, responses=()):
                raise UnresolvedDecision("Preparation step interrupted")
        c.bridge.end_current_turn()
    # Round 2: Hunter reacts to the *actual changed map*, pursues the
    # Vanguard and delivers a paid Bite. Only then can the party reach
    # their G7-C exits, each with its own current-round G1/G4.5/G5 receipt.
    c.bridge.begin_next_round()
    _next(c, "hunter")
    if not _pursue(c, "vanguard"):
        raise UnresolvedDecision("Hunter did not establish opposed retreat contact")
    _bite(c, "vanguard", devastating=False)
    c.bridge.end_current_turn()
    for actor in party:
        _next(c, actor)
        for delta in FINAL_ROUTES[actor]:
            if not e.g1.step(actor, delta, cautious=True, responses=()):
                raise UnresolvedDecision("Actual border step interrupted")
        c.withdraw(actor)
        c.bridge.end_current_turn()
    if e.actors["hunter"].dead or any(e.actors[p].hp <= 0
                                       or e.actors[p].dead for p in party):
        raise UnresolvedDecision("Disengagement witnesses require living participants")
    # More than a mere G7-C border certificate: source Hunter pursuit
    # actually follows initial PC translation, has a paid G1 step, and
    # reaches the still-in-scene Vanguard before its Round 2 withdrawal.
    pursuit = [v for v in e.ledger if v["kind"] ==
               "g7g_hunter_pursuit_executed" and v["round"] == 2]
    if len(pursuit) != 1 or not pursuit[0]["detail"]["movement_indices"]:
        raise UnresolvedDecision("No actual second-round Hunter pursuit")
    for index in pursuit[0]["detail"]["movement_indices"]:
        step = e.ledger[index]
        if (step["kind"] != "g1_movement_step"
                or step["detail"].get("actor") != "hunter"
                or not step["detail"].get("cautious")
                or step["round"] != 2 or step["turn"] != "hunter"):
            raise UnresolvedDecision("Source Hunter pursuit MP not authenticated")
    hunter_bites = [v for v in e.ledger if v["kind"] == "g5_melee_resolved"
                    and v["detail"].get("attacker") == "hunter"
                    and v["detail"].get("target") == "vanguard"]
    if (len(hunter_bites) != 2
            or not all(v["detail"]["outcome"] == "hit" for v in hunter_bites)
            or hunter_bites[-1]["round"] != 2
            or hunter_bites[-1]["index"] <= pursuit[0]["index"]):
        raise UnresolvedDecision("Hunter did not source-pay an opposed Bite after pursuit")
    terminal = PartyTerminal(c).attest_withdrawal()
    e.log("g7g_living_hunter_disengagement_verified",
          native_terminal_index=terminal["terminal_event"],
          hunter_alive=True, pursuit_index=pursuit[0]["index"],
          hunter_paid_bite_indices=[v["index"] for v in hunter_bites],
          border_exit_indices=[x["g5"] for x in terminal["member_exits"]],
          boundary="authored_G7C_scene_exits_only",
          ongoing_world_pursuit_not_adjudicated=True)
    return c, initial, terminal, "party_withdrawal_attested", 2


def run_trial(level=2, size=3, seed=0, *, mode="multitarget_defeat",
              include_ledger=False):
    if (type(level) is not int or level not in (2, 3)
            or type(size) is not int or size not in (3, 4)
            or type(seed) is not int or seed < 0
            or mode not in MODES or type(mode) is not str
            or type(include_ledger) is not bool):
        raise ValueError("G7-G supports sourced L2/3 P3/4 and two fixed policies")
    c, before, terminal, outcome, rounds = (
        _defeat(level, size, seed) if mode == "multitarget_defeat"
        else _withdraw(level, size, seed))
    e = c.e
    turns, ends = _validate_native_ledger(e)
    if (e.current is not None or e.cursor != len(e.order)
            or rounds != ends or turns != ends * len(e.order)
            or c.pending_attack_slots()):
        raise AssertionError("No G7-G acceptance without complete native rounds")
    summary = {
        "version": "B06-G7G-native-pursuit-terminals-v0",
        "mode": mode, "level": level, "party_size": size, "seed": seed,
        "scenario_id": e.scenario, "round_limit": MAX_ROUNDS if
            mode == "multitarget_defeat" else 2,
        "policy_grade": "authored_extremal_dice" if
            mode == "multitarget_defeat" else "authored_two_round_pursuit",
        "outcome": outcome, "native_terminal": terminal,
        "initial_state": before, "final_state": _snapshot(e),
        "rounds_completed": ends, "turns_completed": turns,
        "hunter_alive": not e.actors["hunter"].dead,
        "unique_hunter_bite_victims": sorted({
            v["detail"]["target"] for v in e.ledger
            if v["kind"] == "g5_melee_resolved"
            and v["detail"].get("attacker") == "hunter"
            and v["detail"].get("outcome") == "hit"}),
        "ledger_sha256": canonical_digest(e.ledger),
        "complete_party_pack_certified": False,
        "representative_encounter_calibration_accepted": False,
        "sampled_win_rate": None, "hunter_cr": None,
        "historical_phase3_sha256": HISTORICAL_SHA,
    }
    if include_ledger:
        summary["ledger"] = e.ledger
    return summary


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=MODES, default="multitarget_defeat")
    parser.add_argument("--level", type=int, default=2)
    parser.add_argument("--party-size", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--include-ledger", action="store_true")
    args = parser.parse_args(argv)
    report = run_trial(args.level, args.party_size, args.seed,
                       mode=args.mode, include_ledger=args.include_ledger)
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
