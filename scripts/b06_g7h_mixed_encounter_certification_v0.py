"""B06 G7-H: provenance-checked, bounded mixed-party terminal matrix.

One exact L2/L3 Hunter + A/B/R/F source scene, three separately authored
native policies. A real R Chosen Rite, A/B melee, F Flame and R Bow reach
G6-D victory; G7-G supplies genuine lethal pursuit and opposed withdrawal.
This is terminal-path *coverage*, not representative play or Hunter CR.
"""
from copy import deepcopy
import json

from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import (
    _validate_native_ledger, canonical_digest,
)
from scripts.b06_g7f_representative_calibration_v0 import _reconcile_hp_snapshots
from scripts.b06_hunter_completion_g6d_v0 import run_i3_defeat
from scripts.b06_g7g_hunter_pursuit_terminals_v0 import (
    run_trial as g7g_trial, HISTORICAL_SHA,
)

POLICIES = ("mixed_victory_rite", "hunter_multitarget_defeat",
            "opposed_living_hunter_withdrawal")
TERMINALS = {
    "mixed_victory_rite": ("hunter_defeat_attested", "g6d_hunter_defeat_attested"),
    "hunter_multitarget_defeat": ("party_defeat_attested", "g7c_party_defeat_attested"),
    "opposed_living_hunter_withdrawal": (
        "party_withdrawal_attested", "g7c_party_withdrawal_attested"),
}
ROSTER = ("hunter", "vanguard", "guardian", "archer", "scholar")
SOURCES = ("B06-EN-03", "A", "B", "R", "F")


def _origin(report, ledger, *, policy, level, seed):
    """Bind identity and tactical policy to the *native G0 ledger*."""
    genesis = ledger[0]
    scene = f"B06-I3-G6C:party-4:L{level}"
    if (genesis["kind"] != "encounter_created"
            or genesis["round"] != 0 or genesis["turn"] is not None
            or genesis["detail"].get("scenario") != scene
            or genesis["detail"].get("seed") != seed
            or genesis["detail"].get("order") != list(ROSTER)
            or report.get("scenario_id") != scene
            or report.get("level") != level or report.get("party_size") != 4
            or report.get("seed") != seed):
        raise AssertionError("G7-H source scene, original roster or seed mismatch")
    expected = ("g7h_pack_policy_selected" if policy == "mixed_victory_rite"
                else "g7g_policy_selected")
    chosen = [ev for ev in ledger if ev["kind"] in (
        "g7h_pack_policy_selected", "g7g_policy_selected")]
    if len(chosen) != 1 or chosen[0]["kind"] != expected:
        raise AssertionError("Missing, duplicated or foreign native policy binding")
    v = chosen[0]
    d = v["detail"]
    mode = {"mixed_victory_rite": "mixed_victory_rite",
            "hunter_multitarget_defeat": "multitarget_defeat",
            "opposed_living_hunter_withdrawal": "opposed_disengagement"}[policy]
    runner = "g6d" if policy == "mixed_victory_rite" else None
    if (d.get("policy" if runner else "mode") != mode
            or (runner is not None and d.get("runner") != runner)
            or d.get("scenario") != scene or d.get("seed") != seed
            or d.get("level") != level or d.get("party_size") != 4
            or v["turn"] is not None
            or v["round"] != 1
            or v["index"] <= genesis["index"]
            or any(ev["kind"] in ("turn_start_expiry", "action_committed",
                                 "turn_resources", "g1_movement_step")
                   for ev in ledger[:v["index"]])):
        raise AssertionError("G7-H policy not native-bound before first decision")
    return scene


def _terminal_proof(report, ledger, *, policy, deaths):
    outcome, terminal_kind = TERMINALS[policy]
    terminals = [ev for ev in ledger if ev["kind"] in (
        "g6d_hunter_defeat_attested", "g7c_party_defeat_attested",
        "g7c_party_withdrawal_attested")]
    receipt = report.get("native_terminal") or report.get("terminal")
    if (report.get("outcome") != outcome or len(terminals) != 1
            or terminals[0]["kind"] != terminal_kind
            or not isinstance(receipt, dict)
            or receipt.get("ending") != outcome
            or receipt.get("terminal_event") != terminals[0]["index"]
            or receipt.get("hunter_cr") is not None
            or receipt.get("complete_party_pack_certified") is not False
            or report.get("complete_party_pack_certified") is not False
            or report.get("hunter_cr") is not None
            or report.get("rounds_completed", report.get("rounds")) is None):
        raise AssertionError("G7-H requires unique authentic signed terminal")
    if policy == "mixed_victory_rite":
        if (not deaths["hunter"] or
                any(deaths[p] for p in ROSTER[1:]) or
                terminals[0]["detail"].get("lethal_damage_index") is None):
            raise AssertionError("Hunter victory requires actual Hunter death")
    elif policy == "hunter_multitarget_defeat":
        if (deaths["hunter"] or not all(deaths[p] for p in ROSTER[1:])
                or len(receipt.get("lethal_damage_indices", ())) != 4):
            raise AssertionError("Hunter wipe requires four unique G4 lethal Bites")
    else:
        if (any(deaths.values()) or
                len(receipt.get("member_exits", ())) != 4):
            raise AssertionError("Disengagement requires all living original party exits")
    return terminals[0]


def _source_decisions(ledger, *, policy, terminal):
    events = {}
    for kind in ("g5_melee_resolved", "g6d_bow_adjudicated",
                 "g3_flame_launched", "g3_effect_established",
                 "g7g_hunter_pursuit_executed", "g5_terminal_exit",
                 "g7g_multitarget_defeat_verified",
                 "g7g_living_hunter_disengagement_verified",
                 "g4_damage_applied", "g4_basic_heal_applied",
                 "regeneration_step", "g1_movement_step"):
        events[kind] = [x for x in ledger if x["kind"] == kind]
    melee = events["g5_melee_resolved"]
    if policy == "mixed_victory_rite":
        # Four distinct source actors *actually* contribute in combat:
        # Hunter has real Bite; A/B have paid G5 attacks; R has a Chosen
        # (VP-committed) Rite and lethal authenticated G2/G6-D Bow; F
        # launches independently paid G3 Fire through G4 damage.
        if not any(e["detail"].get("attacker") == "hunter"
                   and e["detail"].get("profile") == "B06-AT-04"
                   for e in melee):
            raise AssertionError("Source Hunter had no genuine physical attack")
        for who, attack in (("vanguard", "B06-PC-A-SWORD"),
                            ("guardian", "B06-PC-B-MACE")):
            if not any(e["detail"].get("attacker") == who
                       and e["detail"].get("profile") == attack for e in melee):
                raise AssertionError("Mixed victory omitted native A/B melee")
        rites = [x for x in events["g3_effect_established"]
                 if x["detail"].get("caster") == "archer"
                 and x["detail"].get("effect_kind") == "Guided Regeneration"
                 and x["detail"].get("chosen") is True
                 and x["detail"].get("committed") == 1]
        if len(rites) != 1 or not any(
                v["kind"] == "action_committed"
                and v["detail"].get("actor") == "archer"
                and v["detail"].get("label") == "g3:guided:maintained"
                and v["index"] < rites[0]["index"] for v in ledger):
            raise AssertionError("No source-paid and chosen R Devotional Rite")
        bows = [x for x in events["g6d_bow_adjudicated"]
                if x["detail"].get("shooter") == "archer"
                and x["detail"].get("target") == "hunter"
                and (x["detail"].get("damage") or {}).get("dead") is True]
        if len(bows) != 1 or bows[0]["index"] >= terminal["index"]:
            raise AssertionError("No genuinely lethal G6-D Bow adjudication")
        flames = [x for x in events["g3_flame_launched"]
                  if x["detail"].get("caster") == "scholar"
                  and x["detail"].get("target") == "hunter"
                  and x["detail"].get("outcome") == "direct_hit_pending_G4"]
        if len(flames) != 2 or not all(any(
                d["detail"].get("event_key") == f"g3-flame-ledger:{flame['index']}"
                and d["detail"].get("recipient") == "hunter"
                for d in events["g4_damage_applied"]) for flame in flames):
            raise AssertionError("F did not deliver two genuine paid Fire packets")
    elif policy == "hunter_multitarget_defeat":
        items = events["g7g_multitarget_defeat_verified"]
        if (len(items) != 1 or items[0]["index"] <= terminal["index"]
                or items[0]["detail"].get("native_terminal_index") !=
                   terminal["index"]):
            raise AssertionError("Missing source-bound positive G7-G party wipe")
        for victim in ROSTER[1:]:
            deaths = [e for e in events["g4_damage_applied"]
                      if e["detail"].get("recipient") == victim
                      and e["detail"].get("dead") is True
                      and e["detail"].get("cause") == "source-profile:B06-AT-04"]
            if len(deaths) != 1 or deaths[0]["index"] not in (
                    terminal["detail"].get("lethal_damage_indices") or ()):
                raise AssertionError("Non-native/deferred Hunter death in G7-H wipe")
    else:
        items = events["g7g_living_hunter_disengagement_verified"]
        exits = events["g5_terminal_exit"]
        p = events["g7g_hunter_pursuit_executed"]
        if (len(items) != 1 or len(exits) != 4 or len(p) != 1
                or items[0]["detail"].get("native_terminal_index") !=
                   terminal["index"] or items[0]["index"] <= terminal["index"]
                or items[0]["detail"].get("ongoing_world_pursuit_not_adjudicated") is not True
                or not p[0]["detail"].get("movement_indices")
                or p[0]["detail"].get("contact") is not True):
            raise AssertionError("G7-H opposed withdrawal lacks living pursuit/exit proof")
        for step in p[0]["detail"]["movement_indices"]:
            if (type(step) is not int or not 0 <= step < len(ledger)
                    or ledger[step]["kind"] != "g1_movement_step"
                    or ledger[step]["detail"].get("actor") != "hunter"):
                raise AssertionError("Non-native Hunter pursuit displacement")
        if {e["detail"].get("actor") for e in exits} != set(ROSTER[1:]):
            raise AssertionError("Missing/duplicated authenticated player exits")
    return {
        "paid_melee_resolutions": len(melee),
        "bow_hit_adjudications": len(events["g6d_bow_adjudicated"]),
        "flame_launches": len(events["g3_flame_launched"]),
        "chosen_R_rites": sum(
            x["detail"].get("caster") == "archer"
            and x["detail"].get("chosen") is True
            for x in events["g3_effect_established"]),
        "genuine_hunter_pursuit_steps": sum(
            x["detail"].get("actor") == "hunter" for x in events["g1_movement_step"]),
        "native_damage_events": len(events["g4_damage_applied"]),
        "native_regeneration_steps": len(events["regeneration_step"]),
        "native_exit_receipts": len(events["g5_terminal_exit"]),
    }


def attest_trial(report, *, level, seed, policy):
    """Independent evidence validation. Never trust mutable report metadata."""
    if (type(level) is not int or level not in (2, 3)
            or type(seed) is not int or seed < 0 or policy not in POLICIES):
        raise ValueError("G7-H supports only L2/L3, P4 and three fixed policies")
    if not isinstance(report, dict):
        raise AssertionError("Source report object required")
    ledger = report.get("ledger")
    if not isinstance(ledger, list) or not ledger:
        raise AssertionError("Full source-native ledger required")
    if any(not isinstance(ev, dict) or ev.get("index") != i
           or type(ev.get("round")) is not int
           or not isinstance(ev.get("detail"), dict)
           for i, ev in enumerate(ledger)):
        raise AssertionError("Original sequential G0 event indices required")
    if canonical_digest(ledger) != report.get("ledger_sha256"):
        raise AssertionError("G7-H source report and original ledger hash disagree")
    _origin(report, ledger, policy=policy, level=level, seed=seed)
    turns = [v["detail"].get("actor") for v in ledger if v["kind"] == "turn_end"]
    ends = [v for v in ledger if v["kind"] == "round_end"]
    last_round_end = ends[-1]["index"] if ends else -1
    open_native = any(
        ev["kind"] in ("round_begin", "turn_start_expiry", "turn_resources",
                       "action_committed", "attack_sequence_committed",
                       "g5_melee_sequence_attested", "g1_movement_step")
        and ev["index"] > last_round_end for ev in ledger)
    if (not ends or turns != list(ROSTER) * len(ends)
            or open_native
            or report.get("turns_completed") != len(turns)
            or report.get("rounds_completed") != len(ends)
            or len([v for v in ledger if v["kind"] == "round_begin"]) != len(ends)
            or any(v["kind"] == "g5_melee_sequence_attested"
                   and (not v["detail"].get("action_indices")
                        or any(not any(
                            x["kind"] in ("g5_melee_resolved", "g5_melee_cancelled")
                            and x["detail"].get("action_index") == action
                            and x["index"] > v["index"]
                            for x in ledger)
                            for action in v["detail"]["action_indices"]))
                   for v in ledger)):
        raise AssertionError("G7-H terminal needs completed G0 rounds and funded G5 slots")
    initial, final = report.get("initial_state"), report.get("final_state")
    if (not isinstance(initial, dict) or not isinstance(final, dict)
            or set(initial) != set(ROSTER) or set(final) != set(ROSTER)):
        raise AssertionError("Missing original/closing actor snapshots")
    _, deaths = _reconcile_hp_snapshots(
        ledger, initial, final, ROSTER, SOURCES)
    terminal = _terminal_proof(report, ledger, policy=policy, deaths=deaths)
    facts = _source_decisions(ledger, policy=policy, terminal=terminal)
    return {"policy": policy, "outcome": TERMINALS[policy][0],
            "source_scenario_id": report["scenario_id"],
            "native_terminal_event": terminal["index"],
            "native_terminal_kind": terminal["kind"],
            "rounds_completed": len(ends), "turns_completed": len(turns),
            "ledger_sha256": report["ledger_sha256"],
            "hunter_dead": deaths["hunter"],
            "party_deaths": [p for p in ROSTER[1:] if deaths[p]],
            "source_decisions": facts}


def _native(policy, level, seed):
    if policy == "mixed_victory_rite":
        return run_i3_defeat(level=level, seed=seed, g7h_priest_rite=True)
    return g7g_trial(
        level=level, size=4, seed=seed,
        mode="multitarget_defeat" if policy == "hunter_multitarget_defeat"
        else "opposed_disengagement", include_ledger=True)


def run_pack(level=3, seed=0, *, include_trials=False):
    """Certify only source-bound terminal-path coverage, not representativeness."""
    if (type(level) is not int or level not in (2, 3)
            or type(seed) is not int or seed < 0
            or type(include_trials) is not bool):
        raise ValueError("G7-H authored terminal pack is L2/L3 four-PC only")
    traces = {}
    cases = []
    for policy in POLICIES:
        native = _native(policy, level, seed)
        proof = attest_trial(native, level=level, seed=seed, policy=policy)
        cases.append(proof)
        if include_trials:
            traces[policy] = native
    if ({c["outcome"] for c in cases} !=
            {v[0] for v in TERMINALS.values()}
            or len({c["ledger_sha256"] for c in cases}) != len(POLICIES)
            or any(c["source_scenario_id"] !=
                   f"B06-I3-G6C:party-4:L{level}" for c in cases)):
        raise AssertionError("Mixed-party source terminal coverage incomplete")
    result = {
        "version": "B06-G7H-source-mixed-terminal-pack-v0",
        "scene": f"B06-I3-G6C:party-4:L{level}",
        "level": level, "party_size": 4, "seed": seed,
        "policies": list(POLICIES),
        "cases": cases,
        "distinct_native_terminal_outcomes": len(cases),
        "bounded_terminal_matrix_certified": True,
        "certification_scope": "one_source_P4_scene_three_authored_terminal_policies",
        "full_representative_encounter_pack_certified": False,
        "complete_party_pack_certified": False,
        "representative_encounter_calibration_accepted": False,
        "sampled_win_rate": None, "confidence_interval": None,
        "hunter_cr": None,
        "human_GM_policy_weights": None,
        "historical_phase3_not_recomputed": True,
        "historical_phase3_sha256": HISTORICAL_SHA,
        "remaining_gates": [
            "native_integrated_protective_response_and_real_healing_in_terminal_path",
            "expanded_P3_and_alternate_frontline_terminal_scenes",
            "unbiased_seeded_rolling_and_policy_decisions_with_uncensored_outcomes",
            "independent_representative_player_GM_and_enemy_baselines",
        ],
    }
    if include_trials:
        result["native_trials"] = traces
    return result


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--include-trials", action="store_true")
    args = parser.parse_args(argv)
    print(json.dumps(run_pack(args.level, args.seed,
                              include_trials=args.include_trials),
                     sort_keys=True, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
