"""B04/B05/B06 L1 source-native hostile Soldier contact and opposed withdrawal.

The Soldier is the UNCHANGED L3-equivalent B06-EN-02 source benchmark,
not an L1-scaled enemy. S/T/F are genuine selected L1 Scholar source sheets,
not historical A/B physical-only Low Priest proxies. These are deliberately
favorable/dangerous FIXED policies, never representative difficulty or play.
"""
import argparse
from copy import deepcopy
import json

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SceneExit, SourceMelee
from scripts.b05_scholar_native_sword_v0 import SWORD_IDS, scholar_sword_profile
from scripts.b06_g7a_native_terminal_census_v0 import _snapshot, canonical_digest

VERSION = "B04-B05-B06-Level-One-Soldier-Combat-v0"
LEVEL = 1
ENEMY_SOURCE = "B06-EN-02"
POLICIES = ("favorable_offense", "opposed_withdrawal")
PARTY = ("fire", "medium", "low")
ROLES = {"fire": "F", "medium": "S", "low": "T"}
POSITIONS = {"fire": (1, 0), "medium": (2, 2), "low": (3, 3)}
EXIT_SQUARES = {"fire": (0, 0), "medium": (0, 2), "low": (3, 6)}
EXIT_STEPS = {"fire": ((-1, 0),),
              "medium": ((-1, 0), (-1, 0)),
              "low": ((0, 1), (0, 1), (0, 1))}
MAX_ROUNDS = 12


def _validate(policy, seed):
    if policy not in POLICIES:
        raise ValueError("Choose one of the two authored L1 Soldier policies")
    if type(seed) is not int or seed < 0:
        raise ValueError("Explicit nonnegative integer source seed required")


def _scene(policy, seed):
    foe = enemy_actor(ENEMY_SOURCE, "foe", "enemy",
                      occupied=((3, 2),))
    actors = [foe] + [
        party_actor(ROLES[ident], LEVEL, ident, "party",
                    occupied=(POSITIONS[ident],))
        for ident in PARTY
    ]
    e = Encounter(actors, {"foe": 40, "fire": 32, "medium": 28, "low": 24},
                  seed=seed, scenario="B04-B05-B06-L1-Soldier-Gate-v0",
                  policy="source-paid-fixed-dice-and-declined-optional-responses",
                  objective="authenticate_L1_hostile_contact_or_opposed_exit")
    GridMovement(e, width=8, height=7, scene_id="L1-soldier-open-gate")
    RangedCombat(e, scene_id="L1-soldier-original-ready-equipment")
    SpellState(e)
    DamageState(e)
    exits = tuple(SceneExit(
        e.scenario, e.g1.scene_id, e.objective, ident,
        EXIT_SQUARES[ident], "L1:gate:" + ident + ":cautious-border"
    ) for ident in PARTY) if policy == "opposed_withdrawal" else ()
    combat = SourceMelee(e, scene_exits=exits)
    if e.order != ("foe", *PARTY):
        raise AssertionError("Original L1 source initiative order changed")
    if (foe.level != 3 or foe.source.source_id != ENEMY_SOURCE or
            any(e.actors[n].level != LEVEL or
                e.actors[n].source.source_id != ROLES[n]
                for n in PARTY)):
        raise AssertionError("Original enemy or selected player L1 source changed")
    for name in ("medium", "low"):
        scholar_sword_profile(e.actors[name], SWORD_IDS[ROLES[name]],
                              encounter=e)
    e.begin_round()
    e.log("b04_b05_b06_l1_policy_selected", policy=policy, level=LEVEL,
          opponent_benchmark_level=foe.level, seed=seed,
          fixed_source_start=foe.source.start_state,
          source_digests={name: a.source.digest for name, a in e.actors.items()},
          no_enemy_downlevel=True, no_low_priest_proxy=True)
    return combat


def _start(combat, ident):
    a = combat.e.actors[ident]
    # No automatic refill. A Dying actor spends its own Vigor to prevent
    # Dying loss only when the authored choice and actual source permit it.
    choice = RegenerationChoice(
        cancel_dying_loss=(a.hp <= 0 and not a.dead and
                           a.vigor > 0 and a.regen > 0))
    combat.bridge.start_next_turn(choice)
    if combat.e.current != ident:
        raise AssertionError("Turn must follow source native Initiative")


def _sword(combat, attacker, target, profile, attack_face, damage_face=None):
    e = combat.e
    if not e.g1.melee_contact(attacker, target):
        raise UnresolvedDecision("Actual G1 contact required before sourced sword")
    sequence = combat.declare(attacker, target, profiles=(profile,),
                              defenses=("take_hit",))
    kwargs = {"attack_face": attack_face}
    if attack_face != 1:
        kwargs.update(damage_face=damage_face, wound_location_roll=8)
    outcome = combat.resolve(sequence, 0, **kwargs)
    if outcome["outcome"] != ("miss" if attack_face == 1 else "hit"):
        raise AssertionError("Fixed native Soldier/Scholar roll was not delivered")
    return outcome


def _enemy_turn(combat, policy):
    e = combat.e
    if e.actors["foe"].hp <= 0 or e.actors["foe"].dead:
        return
    target = next((name for name in ("medium", "low")
                   if e.actors[name].hp > 0 and not e.actors[name].dead), None)
    if target is not None:
        _sword(combat, "foe", target, "B06-AT-03",
               1 if policy == "favorable_offense" else 12,
               None if policy == "favorable_offense" else 1)


def _player_turn(combat, ident, policy, round_no):
    e = combat.e
    a = e.actors[ident]
    if a.dead or a.hp <= 0:
        return
    if policy == "opposed_withdrawal":
        for delta in EXIT_STEPS[ident]:
            if not e.g1.step(ident, delta, cautious=True,
                             responses=lambda eligible: ()):
                raise UnresolvedDecision("Native L1 cautious exit canceled")
        combat.withdraw(ident)
        return
    if e.actors["foe"].dead:
        return
    if ident == "fire":
        if round_no == 1:
            result = e.g3.cast_flame(
                "fire", "foe", tier=1, face=12, vigor_die=3,
                defense="take_hit", hand_available=True,
                wound_location_roll=8)
            if result["outcome"] != "direct_hit_resolved_G4":
                raise AssertionError("Selected L1 High Scholar failed genuine paid Flame")
    else:
        _sword(combat, ident, "foe", SWORD_IDS[ROLES[ident]], 12, 4)


def _outcome(e, policy):
    if e.current is not None or e.cursor != len(e.order):
        raise AssertionError("L1 terminal assessment requires completed Round End")
    if e.g5.pending_attack_slots():
        raise AssertionError("G5 paid actions remain unresolved")
    if not any(x["kind"] == "round_end" and x["round"] == e.round
               for x in e.ledger):
        raise AssertionError("Missing original native Round End")
    if policy == "favorable_offense":
        if not e.actors["foe"].dead:
            return None
        if not any(x["kind"] == "g4_damage_applied" and
                   x["detail"].get("recipient") == "foe" and
                   x["detail"].get("dead") is True for x in e.ledger):
            raise AssertionError("Enemy death must be an actual G4 terminal")
        return "soldier_defeat"
    exits = [ev for ev in e.ledger if ev["kind"] == "g5_terminal_exit"]
    if (len(exits) == len(PARTY) and
            {ev["detail"]["actor"] for ev in exits} == set(PARTY) and
            not e.actors["foe"].dead and
            all(e.actors[n].hp > 0 and not e.actors[n].dead for n in PARTY)):
        return "party_scene_withdrawal"
    return None


def run_policy(*, policy, seed=0):
    """One native L1 policy. Unresolved rounds remain censored, never wins."""
    _validate(policy, seed)
    combat = _scene(policy, seed)
    e = combat.e
    outcome = None
    for round_no in range(1, MAX_ROUNDS + 1):
        if round_no > 1:
            combat.bridge.begin_next_round()
        for ident in e.order:
            _start(combat, ident)
            if ident == "foe":
                _enemy_turn(combat, policy)
            else:
                _player_turn(combat, ident, policy, round_no)
            combat.bridge.end_current_turn()
        outcome = _outcome(e, policy)
        if outcome is not None:
            break
    e.check()
    original_damage = [ev for ev in e.ledger if ev["kind"] == "g4_damage_applied"]
    source_hits = [ev for ev in e.ledger if ev["kind"] == "g5_melee_resolved"]
    if not source_hits or (policy == "favorable_offense" and
                           not any(ev["detail"]["attacker"] in ("medium", "low")
                                   for ev in source_hits)):
        raise AssertionError("Must perform actual source-paid melee combat")
    report = {
        "version": VERSION, "level": LEVEL, "policy": policy, "seed": seed,
        "opponent_source": ENEMY_SOURCE,
        "opponent_source_level": e.actors["foe"].level,
        "party_roles": dict(ROLES),
        "rounds_completed": e.round,
        "outcome": outcome or "unresolved_round_ceiling",
        "final_state": _snapshot(e),
        "final_vp_spent": {n: e.actors[n].vp_spent for n in e.actors},
        "source_digests": {n: e.actors[n].source.digest for n in e.actors},
        "native_melee_results": len(source_hits),
        "native_g4_damage_receipts": len(original_damage),
        "native_flame_launches": sum(ev["kind"] == "g3_flame_launched"
                                     for ev in e.ledger),
        "native_scene_exits": sum(ev["kind"] == "g5_terminal_exit"
                                  for ev in e.ledger),
        "source_paid_l1_hostile_combat": True,
        "bounded_source_terminal_certified": outcome is not None,
        "externally_observed_player_decisions": False,
        "complete_twelve_focus_l1_coverage": False,
        "independently_full_focus_certified": False,
        "representative_difficulty_calibrated": False,
        "statistical_win_rate": None,
        "hunter_cr": None,
        "ledger": deepcopy(e.ledger),
    }
    report["ledger_sha256"] = canonical_digest(report["ledger"])
    return report


def attest_policy(report, *, policy, seed=0):
    """Reject a forged/rehashed outcome against an independently rerun policy."""
    _validate(policy, seed)
    expected = run_policy(policy=policy, seed=seed)
    if (type(report) is not dict or
            report.get("ledger_sha256") != canonical_digest(report.get("ledger")) or
            report != expected or not expected["bounded_source_terminal_certified"]):
        raise AssertionError("L1 source terminal fails independent native replay")
    return deepcopy(expected)


def run_pack(*, seed=0):
    rows = []
    for policy in POLICIES:
        original = run_policy(policy=policy, seed=seed)
        if original["bounded_source_terminal_certified"]:
            attest_policy(original, policy=policy, seed=seed)
        rows.append({k: deepcopy(v) for k, v in original.items() if k != "ledger"})
    outcomes = {r["policy"]: r["outcome"] for r in rows}
    return {
        "version": VERSION, "seed": seed, "observations": rows,
        "terminal_count": sum(r["bounded_source_terminal_certified"] for r in rows),
        "total_policies": len(rows),
        "all_terminal": all(r["bounded_source_terminal_certified"] for r in rows),
        "outcomes": outcomes,
        "external_human_sessions": 0, "independent_focus_certificates": 0,
        "strict_mvp_exits_met": 0, "win_rate": None, "hunter_cr": None,
    }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--policy", choices=POLICIES)
    cli.add_argument("--seed", type=int, default=0)
    args = cli.parse_args()
    result = (run_policy(policy=args.policy, seed=args.seed)
              if args.policy else run_pack(seed=args.seed))
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
