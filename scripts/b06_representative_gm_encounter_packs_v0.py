"""B06 source-native Soldier, Sentry and Hunter candidate GM encounter packs v0.

Three enemy families with actual G8/G7H terminal branches, Hunter forest
geometry and protected/warned tactical countercases. This is an actionable
GM scenario menu and replayable source evidence, NOT representative GM sample
data, measured challenge rating, or newly authored combat effects.
"""
import argparse
from collections import Counter
from copy import deepcopy
import json

from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_g8_soldier_sentry_full_pack_v0 import (
    MODES as G8_MODES, OPPONENTS as G8_OPPONENTS,
    run_policy as g8_run, attest_policy as g8_attest,
)
from scripts.b06_g7h_mixed_encounter_certification_v0 import (
    POLICIES as HUNTER_TERMINALS, run_pack as hunter_pack,
)
from scripts.b06_g7f_representative_calibration_v0 import (
    run_case as hunter_tactical_case,
)

LEVELS = (2, 3)
SEED = 17
HUNTER_FIELD = ("forest_ordinary", "forest_pounce")
HUNTER_WATCH = ("warned_party_exit", "protected_control",
                "reactive_shield", "prepared_body")
# These are GM-prep encounter names, NOT a change to the original source
# scenes, enemy statblocks, source geometry or policy selectors.
GM_BRIEFS = {
    "soldier_gate": {
        "source_enemy": "B06-EN-02", "enemy_role": "ordinary_human",
        "fiction": "A road gate patrol challenging a party near the supply route",
        "approach": "Question the soldier or show credentials; combat is optional",
        "tactical_terrain": "Open 8x7 G8 melee lane; no authored cover or reinforcements",
        "player_objective": "Protect companions and proceed, hold position or withdraw",
        "gm_question": "When do negotiations fail, and is retreat physically safe beyond the scene?",
        "potential_hazards": "Reinforcements and gate crowds are NOT included in native evidence",
    },
    "sentry_shrine_cold": {
        "source_enemy": "B06-EN-01", "enemy_role": "magical_specialist",
        "fiction": "An unprepared Firebound Sentry watching the shrine doorway",
        "approach": "Choose parley, observation, bypass or direct opposition",
        "tactical_terrain": "G8 8x7 source lane; cold Sentry must spend 30 AP and commit 3 VP to Reserve",
        "player_objective": "Escape the doorway or withstand the first preparation window",
        "gm_question": "Is the sentry alerted early enough to pre-prepare, or still cold?",
        "potential_hazards": "Shrine seals/wards are fiction only unless separate rules are sourced",
    },
    "sentry_shrine_prepared": {
        "source_enemy": "B06-EN-01", "enemy_role": "magical_specialist",
        "fiction": "The same source Sentry after its source-authorized prepared start",
        "approach": "Observe its active state, de-escalate or break contact",
        "tactical_terrain": "Same source G8 open geometry; 3 VP already committed in starting state",
        "player_objective": "Deal with the genuinely enhanced sword and possible direct Vigor harm",
        "gm_question": "Was a preparation action actually available before the party arrived?",
        "potential_hazards": "Do not grant free additional ward, spell, movement or preparation",
    },
    "hunter_forest": {
        "source_enemy": "B06-EN-03", "enemy_role": "elite_predator_unrated",
        "fiction": "A 1x2 apex forest Hunter defending a travel corridor near its territory",
        "approach": "Read tracks and signs, keep distance or choose lawful engagement",
        "tactical_terrain": "G7H source contact lane; G7F separate forest 1x2 Pounce versus ordinary approach",
        "player_objective": "Survive, drive it off, defeat it or genuinely leave contact",
        "gm_question": "Is the party warned? Can it avoid hostility or withdraw safely from pursuit?",
        "potential_hazards": "Bite venom and wounds require actual native receipts, not inferred ticks",
    },
}
PACKS = {
    "soldier_gate": ("g8", "soldier"),
    "sentry_shrine_cold": ("g8", "sentry_cold"),
    "sentry_shrine_prepared": ("g8", "sentry_prepared"),
    "hunter_forest": ("g7h", "hunter"),
}


def _level(level, seed):
    if type(level) is not int or level not in LEVELS:
        raise ValueError("GM source encounters require authored L2/L3")
    if type(seed) is not int or seed < 0:
        raise ValueError("Predeclared nonnegative source seed required")


def _authentic_native(report):
    ledger = report.get("ledger")
    if (not isinstance(ledger, list) or not ledger
            or canonical_digest(ledger) != report.get("ledger_sha256")
            or any(e.get("index") != i for i, e in enumerate(ledger))):
        raise AssertionError("Cannot use nonnative or resequenced encounter ledger")


def _aftermath(final_state, *, opponent_alive, exit_count,
               outcome, outcome_certified):
    if not isinstance(final_state, dict):
        raise AssertionError("Native final source state required")
    party = {k: v for k, v in final_state.items() if k not in ("foe", "hunter")}
    if not party or any(not isinstance(v.get("wounds"), list)
                        for v in party.values()):
        raise AssertionError("Native party wounds must be available")
    return {
        "party_dead": sorted(k for k, v in party.items() if v["dead"]),
        "party_dying": sorted(k for k, v in party.items() if v["dying"]),
        "party_wounds": {k: deepcopy(v["wounds"]) for k, v in party.items()},
        "party_hp": {k: v["hp"] for k, v in party.items()},
        "party_vigor": {k: v["vigor"] for k, v in party.items()},
        "party_vp_available": {k: v["vp_available"] for k, v in party.items()},
        "party_vp_committed": {k: v["vp_committed"] for k, v in party.items()},
        "party_ammunition": {k: v["ammunition"] for k, v in party.items()},
        "source_digests": {k: v["source_digest"] for k, v in final_state.items()},
        "enemy_alive_at_terminal_or_cutoff": opponent_alive,
        "source_exit_event_count": exit_count,
        "scene_local_outcome": outcome,
        "native_outcome_certified": outcome_certified,
        "safe_for_six_hour_rest": None,
        "long_term_pursuit_resolved": None,
        "next_gm_gate": (
            "Terminal defeat; GM must resolve aftermath, casualties and continuation"
            if outcome in ("party_defeat", "party_defeat_attested")
            else "Opposed departure only; living foe pursuit, venom and safe distance unresolved"
            if exit_count
            else "Encounter ends/cuts off locally; GM must decide tracking, treatment, recovery and next threat"
        ),
    }


def run_g8(name, level, *, mode, seed=SEED):
    if name not in PACKS or PACKS[name][0] != "g8":
        raise ValueError("Choose a source G8 Soldier/Sentry GM brief")
    _level(level, seed)
    if type(mode) is not str or mode not in G8_MODES:
        raise ValueError("G8 requires one authored outcome policy")
    source = PACKS[name][1]
    result = g8_run(opponent=source, level=level, seed=seed, mode=mode)
    _authentic_native(result)
    g8_attest(result, opponent=source, level=level, seed=seed, mode=mode)
    if result["source_ids"]["foe"] != GM_BRIEFS[name]["source_enemy"]:
        raise AssertionError("Wrong enemy source for GM brief")
    ledger = result["ledger"]
    exits = sum(e["kind"] == "g5_terminal_exit" for e in ledger)
    final = result["final_state"]
    return {
        "gm_pack": name, "level": level, "party_size": 4, "seed": seed,
        "source_executor": "B06_G8", "policy": mode,
        "source_opponent": source,
        "source_enemy_id": result["source_ids"]["foe"],
        "outcome": result["outcome"],
        "bounded_native_terminal_attested": result["bounded_source_terminal_certified"],
        "censored_or_unresolved": not result["bounded_source_terminal_certified"],
        "rounds_completed": result["rounds_completed"],
        "native_ledger_sha256": result["ledger_sha256"],
        "native_event_count": len(ledger),
        "real_damage_packets": sum(e["kind"] == "g4_damage_applied" for e in ledger),
        "real_vp_transitions": sum(e["kind"] == "vp_transition" for e in ledger),
        "real_movement_steps": sum(e["kind"] == "g1_movement_step" for e in ledger),
        "native_exit_events": exits,
        "initial_source_state": ledger[0]["detail"]["source_ids"],
        "aftermath": _aftermath(
            final, opponent_alive=not final["foe"]["dead"],
            exit_count=exits, outcome=result["outcome"],
            outcome_certified=result["bounded_source_terminal_certified"]),
        "human_gm_observed": False, "sampled_win_rate": None, "hunter_cr": None,
    }


def run_hunter_terminals(level, *, seed=SEED):
    _level(level, seed)
    pack = hunter_pack(level, seed, include_trials=True)
    if (not pack["bounded_terminal_matrix_certified"]
            or pack["party_size"] != 4
            or set(pack["policies"]) != set(HUNTER_TERMINALS)):
        raise AssertionError("G7H original three-terminal pack is incomplete")
    rows = []
    for proof in pack["cases"]:
        policy = proof["policy"]
        native = pack["native_trials"][policy]
        _authentic_native(native)
        if proof["ledger_sha256"] != native["ledger_sha256"]:
            raise AssertionError("G7H native result and independently authenticated proof disagree")
        if native["initial_state"]["hunter"]["source_id"] != GM_BRIEFS["hunter_forest"]["source_enemy"]:
            raise AssertionError("Wrong Hunter source fixture")
        ledger = native["ledger"]
        exit_count = sum(e["kind"] == "g5_terminal_exit" for e in ledger)
        final = native["final_state"]
        rows.append({
            "gm_pack": "hunter_forest", "level": level, "party_size": 4,
            "seed": seed, "source_executor": "B06_G7H", "policy": policy,
            "source_enemy_id": "B06-EN-03",
            "outcome": proof["outcome"],
            "bounded_native_terminal_attested": True,
            "censored_or_unresolved": False,
            "rounds_completed": proof["rounds_completed"],
            "native_ledger_sha256": proof["ledger_sha256"],
            "native_event_count": len(ledger),
            "real_damage_packets": sum(e["kind"] == "g4_damage_applied" for e in ledger),
            "real_vp_transitions": sum(e["kind"] == "vp_transition" for e in ledger),
            "real_movement_steps": sum(e["kind"] == "g1_movement_step" for e in ledger),
            "native_exit_events": exit_count,
            "source_decisions": deepcopy(proof["source_decisions"]),
            "aftermath": _aftermath(
                final, opponent_alive=not final["hunter"]["dead"],
                exit_count=exit_count, outcome=proof["outcome"],
                outcome_certified=True),
            "human_gm_observed": False, "sampled_win_rate": None, "hunter_cr": None,
        })
    if len(rows) != 3:
        raise AssertionError("Original G7H three independently witnessed terminals required")
    return rows


def run_hunter_tactic(level, size, policy, *, seed=SEED):
    _level(level, seed)
    if (type(size) is not int or size not in (3, 4) or
            type(policy) is not str or
            policy not in HUNTER_FIELD + HUNTER_WATCH or
            (policy in HUNTER_WATCH and (level, size) != (3, 4))):
        raise ValueError("Only original G7F authored forest/defense policy cells")
    proof = hunter_tactical_case(level, size, seed, policy=policy)
    # The original G7F attestor has already checked the native source
    # roster, ledger, outcome, HP changes and genuine terminal receipts.
    if (proof["policy"] != policy or proof["level"] != level or
            proof["party_size"] != size or proof["seed"] != seed
            or len(proof["ledger_sha256"]) != 64):
        raise AssertionError("Foreign G7F source policy result")
    return {
        "gm_pack": "hunter_forest", "level": level, "party_size": size,
        "seed": seed, "source_executor": "B06_G7F", "policy": policy,
        "source_enemy_id": "B06-EN-03",
        "opening_source": ("forest_geometry_pounce_vs_ordinary" if policy in HUNTER_FIELD
                           else "warned_protection_or_source_exit"),
        "outcome": proof["outcome"],
        "bounded_native_terminal_attested": proof["certified_terminal"],
        "censored_or_unresolved": proof["censored"],
        "unresolved_reason": proof["unresolved_reason"],
        "rounds_completed": proof["rounds_completed"],
        "native_ledger_sha256": proof["ledger_sha256"],
        "hunter_hp_change": proof["hunter_hp_change"],
        "party_hp_change": proof["party_hp_change"],
        "native_pounces": proof["genuine_pounces"],
        "native_protections": proof["genuine_protections"],
        "native_exit_events": proof["real_party_exit_events"],
        "aftermath": {
            "native_hp_changes_only": True,
            "party_hp_change": proof["party_hp_change"],
            "hunter_hp_change": proof["hunter_hp_change"],
            "source_exit_event_count": proof["real_party_exit_events"],
            "safe_for_six_hour_rest": None,
            "long_term_pursuit_resolved": None,
            "next_gm_gate": "Native short-window/cutoff evidence; check real wounds, venoms and threats before moving time",
        },
        "human_gm_observed": False, "sampled_win_rate": None, "hunter_cr": None,
    }


def encounter_pack(*, seed=SEED):
    """Predeclared source policies; no post-outcome filtering or GM weights."""
    if type(seed) is not int or seed < 0:
        raise ValueError("Only a fixed nonnegative reproducible seed")
    rows = []
    for level in LEVELS:
        for gm_pack in ("soldier_gate", "sentry_shrine_cold",
                        "sentry_shrine_prepared"):
            for mode in G8_MODES:
                rows.append(run_g8(gm_pack, level, mode=mode, seed=seed))
        rows.extend(run_hunter_terminals(level, seed=seed))
        for size in (3, 4):
            for policy in HUNTER_FIELD:
                rows.append(run_hunter_tactic(level, size, policy, seed=seed))
    for policy in HUNTER_WATCH:
        rows.append(run_hunter_tactic(3, 4, policy, seed=seed))
    if len(rows) != 36:
        raise AssertionError("Exact 18 G8 + 6 G7H + 12 G7F candidate source cells required")
    grades = Counter(("bounded_terminal" if r["bounded_native_terminal_attested"]
                      else "censored_or_unresolved") for r in rows)
    observed = Counter(r["outcome"] for r in rows)
    return {
        "version": "B06-Representative-GM-Candidate-Packs-v0",
        "seed_predeclared": seed, "gm_briefs": deepcopy(GM_BRIEFS),
        "enemy_families": 3, "authored_gm_scenarios": len(GM_BRIEFS),
        "source_native_policy_observations": len(rows),
        "g8_soldier_sentry_terminal_cases": 18,
        "g7h_hunter_terminal_cases": 6,
        "g7f_hunter_field_and_protective_cases": 12,
        "terminal_or_censor_denominator": len(rows),
        "source_evidence_grade_counts": dict(sorted(grades.items())),
        "outcome_counts_including_censored": dict(sorted(observed.items())),
        "native_source_sha256": sorted({r["native_ledger_sha256"] for r in rows}),
        "human_sessions_observed": 0,
        "representative_player_gm_samples": 0,
        "representative_difficulty_accepted": False,
        "source_bounded_terminal_certification_is_full_gm_pack": False,
        "hunter_challenge_rating": None, "sampled_win_rate": None,
        "independent_focus_certifications": 0,
        "strict_mvp_exit_gates_met": 0,
        "rows": rows,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--gm-pack", choices=tuple(PACKS))
    p.add_argument("--level", type=int, choices=LEVELS)
    p.add_argument("--policy", type=str)
    p.add_argument("--party-size", type=int, choices=(3,4), default=4)
    a = p.parse_args()
    if any(x is not None for x in (a.gm_pack,a.level,a.policy)):
        if not all(x is not None for x in (a.gm_pack,a.level,a.policy)):
            p.error("Specify --gm-pack, --level and --policy together")
        if a.gm_pack=="hunter_forest":
            if a.policy in HUNTER_TERMINALS:
                if a.party_size != 4:
                    p.error("G7H native terminal has four original players")
                result=next(r for r in run_hunter_terminals(a.level, seed=a.seed)
                            if r["policy"]==a.policy)
            else:
                result=run_hunter_tactic(a.level,a.party_size,a.policy,seed=a.seed)
        else:
            if a.party_size != 4:
                p.error("G8 native Soldier/Sentry policy has four original players")
            result=run_g8(a.gm_pack,a.level,mode=a.policy,seed=a.seed)
    else:
        if a.party_size != 4:
            p.error("Party size needs a named Hunter G7F candidate")
        result=encounter_pack(seed=a.seed)
    print(json.dumps(result,sort_keys=True,indent=2,allow_nan=False))


if __name__ == "__main__":
    main()
