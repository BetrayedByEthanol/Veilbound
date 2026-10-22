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
                or receipt.get("lethal_damage_indices") !=
                   terminals[0]["detail"].get("lethal_damage_indices")
                or len(receipt.get("lethal_damage_indices", ())) != 4):
            raise AssertionError("Hunter wipe requires four unique G4 lethal Bites")
    else:
        if (any(deaths.values())
                or receipt.get("member_exits") !=
                   terminals[0]["detail"].get("member_exits")
                or len(receipt.get("member_exits", ())) != 4):
            raise AssertionError("Disengagement requires all living original party exits")
    return terminals[0]



def _lethal_bow_terminal_chain(ledger, terminal, adjudication):
    """Bind G6-D's victory receipt to the unique paid *lethal* Bow shot.

    Rehashing an edited ledger cannot make a prior nonlethal G4 packet the
    finishing shot. Check the original G0 payment, G2 launch/shot, native G4
    cause+event key, G6-D summary and signed G6-D terminal as ONE chain.
    """
    td = terminal["detail"]
    lethal_index = td.get("lethal_damage_index")
    if type(lethal_index) is not int or not 0 <= lethal_index < terminal["index"]:
        raise AssertionError("G6-D terminal must identify a prior native lethal damage index")
    lethal = ledger[lethal_index]
    if (lethal["kind"] != "g4_damage_applied"
            or lethal["detail"].get("recipient") != "hunter"
            or lethal["detail"].get("dead") is not True
            or lethal["detail"].get("hp_after", 0) >= 0
            or lethal["turn"] != "archer"
            or lethal["round"] != adjudication["round"]):
        raise AssertionError("Victory terminal points at nonlethal/non-Bow Hunter damage")
    if len([x for x in ledger if x["kind"] == "g4_damage_applied"
            and x["detail"].get("recipient") == "hunter"
            and x["detail"].get("dead") is True]) != 1:
        raise AssertionError("Victory requires one unique genuine Hunter death packet")
    d = adjudication["detail"]
    action_index, launch_index, shot_index = (
        d.get("action_index"), d.get("launch_index"), d.get("shot_index"))
    if (any(type(v) is not int for v in
            (action_index, launch_index, shot_index))
            or not 0 <= action_index < launch_index < shot_index
                < lethal_index < adjudication["index"] < terminal["index"]
            or any(ledger[i]["round"] != lethal["round"]
                   or ledger[i]["turn"] != "archer" for i in
                   (action_index, launch_index, shot_index))
            or adjudication["turn"] != "archer"
            or d.get("shooter") != "archer"
            or d.get("target") != "hunter"
            or d.get("outcome") != "hit"):
        raise AssertionError("G6-D Bow completion is not one current native Archer turn")
    action, launch, shot = (ledger[action_index], ledger[launch_index],
                            ledger[shot_index])
    if (action["kind"] != "action_committed"
            or action["detail"].get("actor") != "archer"
            or action["detail"].get("action_class") != "physical"
            or action["detail"].get("label") != "g2:bow:hunter:0"
            or launch["kind"] != "g2_bow_launched"
            or launch["detail"].get("shooter") != "archer"
            or launch["detail"].get("target") != "hunter"
            or shot["kind"] != "g2_bow_shot_resolved"
            or shot["detail"].get("shooter") != "archer"
            or shot["detail"].get("intended") != "hunter"
            or shot["detail"].get("target") != "hunter"
            or shot["detail"].get("primary_face") != d.get("attack_face")
            or shot["detail"].get("outcome") != d.get("original_outcome")):
        raise AssertionError("Victory Bow lacks original G0/G2 paid shot and launch")
    declarations = [x for x in ledger[action_index+1:launch_index]
                    if x["kind"] == "g2_bow_sequence_committed"
                    and x["round"] == lethal["round"]
                    and x["turn"] == "archer"]
    if (len(declarations) != 1
            or declarations[0]["detail"].get("shooter") != "archer"
            or declarations[0]["detail"].get("target") != "hunter"
            or declarations[0]["detail"].get("profiles") != ["Bow"]
            or declarations[0]["detail"].get("defenses") != ["take_hit"]):
        raise AssertionError("Victory Bow missing its original one-shot G2 declaration")
    seed = ledger[0]["detail"].get("seed")
    if (lethal["detail"].get("cause") != f"g6d:source_bow:archer:{shot_index}"
            or lethal["detail"].get("event_key") !=
               f"g6d:bow:{seed}:{action_index}:{shot_index}"
            or td.get("source_event_cause") != lethal["detail"]["cause"]
            or d.get("shot_index") != shot_index
            or d.get("launch_index") != launch_index
            or (d.get("damage") or {}).get("dead") is not True
            or d["damage"].get("hp_loss") != (
                lethal["detail"]["hp_before"] - lethal["detail"]["hp_after"])):
        raise AssertionError("Terminal, G4 lethal packet and G6-D Bow summary diverge")
    return lethal


# These four border destinations are fixed by the G6-C scene constructor,
# NOT supplied by a terminal report or an editable exit-policy event.
G7C_BORDER_SQUARES = {
    "vanguard": [0, 2], "guardian": [3, 6],
    "archer": [0, 4], "scholar": [0, 0],
}


def _hunter_bite_hits(ledger, target):
    """Reconstruct each *resolved* Hunter Bite from its source-paid G0 chain.

    A cancelled paid slot is NOT a hit, even if an earlier G4 packet and a
    G7-C terminal are left in a tampered ledger. All five stages are bound
    to the same paid action, target, source profile and native actor turn.
    """
    hits = []
    seed = ledger[0]["detail"].get("seed")
    for resolved in ledger:
        if (resolved["kind"] != "g5_melee_resolved"
                or resolved["detail"].get("attacker") != "hunter"
                or resolved["detail"].get("target") != target
                or resolved["detail"].get("profile") != "B06-AT-04"
                or resolved["detail"].get("outcome") != "hit"):
            continue
        d = resolved["detail"]
        action_index = d.get("action_index")
        if (type(action_index) is not int
                or not 0 <= action_index < resolved["index"]):
            raise AssertionError("Bite resolution needs its exact paid action")
        action = ledger[action_index]
        if (action["kind"] != "action_committed"
                or action["round"] != resolved["round"]
                or action["turn"] != resolved["turn"]
                or resolved["turn"] != "hunter"
                or action["detail"].get("actor") != "hunter"
                or action["detail"].get("action_class") != "physical"
                or any(x["kind"] == "g5_melee_cancelled"
                       and x["detail"].get("action_index") == action_index
                       for x in ledger)):
            raise AssertionError("Bite must consume one genuine uncancelled G0 payment")
        attestations = [x for x in ledger
                        if x["kind"] == "g5_melee_sequence_attested"
                        and action_index in x["detail"].get("action_indices", ())
                        and action_index < x["index"] < resolved["index"]]
        if len(attestations) != 1:
            raise AssertionError("Bite lacks one source-authenticated G5 sequence")
        attested = attestations[0]
        seq = attested["detail"]
        position = seq["action_indices"].index(action_index)
        declaration_index = seq.get("declaration_index")
        if (seq.get("attacker") != "hunter" or seq.get("target") != target
                or len(seq.get("profiles", ())) <= position
                or seq["profiles"][position] != "B06-AT-04"
                or type(declaration_index) is not int
                or not action_index < declaration_index < attested["index"]
                or attested["round"] != resolved["round"]
                or attested["turn"] != "hunter"):
            raise AssertionError("Bite sequence changed its source profile or prey")
        declaration = ledger[declaration_index]
        if (declaration["kind"] != "attack_sequence_committed"
                or declaration["detail"].get("attacker") != "hunter"
                or declaration["detail"].get("target") != target
                or len(declaration["detail"].get("profiles", ())) <= position
                or declaration["detail"]["profiles"][position] != "B06-AT-04"
                or action["detail"].get("label") !=
                   f"sequence:B06-AT-04:{position}"):
            raise AssertionError("Paid Bite does not match original G0 declaration")
        rolls = [x for x in ledger
                 if x["kind"] == "g5_melee_roll"
                 and x["detail"].get("action_index") == action_index]
        bridges = [x for x in ledger
                   if x["kind"] == "g45_attested_hit"
                   and x["detail"].get("action_index") == action_index]
        if len(rolls) != 1 or len(bridges) != 1:
            raise AssertionError("Resolved Bite requires unique G5 roll and G4.5 hit")
        roll, bridge = rolls[0], bridges[0]
        native = (roll, bridge, resolved)
        if (not attested["index"] < roll["index"] < bridge["index"]
                < resolved["index"]
                or any(x["round"] != resolved["round"] or x["turn"] != "hunter"
                       for x in native)
                or any(x["detail"].get("attacker") != "hunter"
                       or x["detail"].get("target") != target
                       or x["detail"].get("profile") != "B06-AT-04"
                       for x in native)
                or roll["detail"].get("hit") is not True
                or roll["detail"].get("declaration_index") != declaration_index
                or roll["detail"].get("slot") != position
                or bridge["detail"].get("sequence_declaration_index") != declaration_index
                or bridge["detail"].get("declared_profile_index") != position
                or bridge["detail"].get("source_event") !=
                   f"g5:source:{seed}:{action_index}"
                or not isinstance(bridge["detail"].get("actual_result"), dict)
                or d.get("damage") != bridge["detail"]["actual_result"]):
            raise AssertionError("Hunter Bite roll, G4.5 and G5 outcome are not one hit")
        damages = [x for x in ledger
                   if x["kind"] == "g4_damage_applied"
                   and roll["index"] < x["index"] < bridge["index"]
                   and x["detail"].get("recipient") == target
                   and x["detail"].get("cause") == "source-profile:B06-AT-04"]
        if len(damages) != 1:
            raise AssertionError("Hunter Bite has no single synchronous G4 packet")
        damage = damages[0]
        result = bridge["detail"]["actual_result"]
        if (damage["round"] != resolved["round"] or damage["turn"] != "hunter"
                or result.get("dead") is not damage["detail"].get("dead")
                or result.get("hp_loss") != (
                    damage["detail"].get("hp_before", 0) -
                    damage["detail"].get("hp_after", 0))):
            raise AssertionError("Bite's G4 damage does not match attested G5 outcome")
        hits.append({"resolved": resolved, "roll": roll,
                     "bridge": bridge, "damage": damage,
                     "action": action, "sequence": attested})
    return hits


def _replay_native_exit_geometry(ledger):
    """Replay EVERY G7-G G1 move against a freshly sourced G6-C grid.

    The movement receipts and even their recalculated SHA are input evidence,
    not authority for positions. Derive the initial footprints, walls and
    movement rules from the independently constructed authored source scene;
    recheck legality, exact movement cost/shape, continuous position and
    remaining MP before allowing any of its border exits to certify.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene

    genesis = ledger[0]["detail"]
    seed = genesis.get("seed")
    origin = genesis.get("source_ids")
    if (type(seed) is not int or seed < 0
            or not isinstance(origin, dict) or set(origin) != set(ROSTER)
            or type(origin["vanguard"].get("level")) is not int
            or origin["vanguard"]["level"] not in (2, 3)):
        raise AssertionError("G7-H withdrawal needs original source start geometry")
    scene = mixed_scene(size=4, level=origin["vanguard"]["level"],
                        seed=seed, party_exits=True)
    expected = scene.e
    grid = expected.g1
    actual_maps = [x for x in ledger if x["kind"] == "g1_map_installed"]
    reference_map = next(x for x in expected.ledger
                         if x["kind"] == "g1_map_installed")
    if (len(actual_maps) != 1
            or actual_maps[0]["detail"] != reference_map["detail"]):
        raise AssertionError("G7-H G1 map must be the original authored 8x7 grid")
    for actor in ROSTER:
        if (origin[actor].get("source_id") !=
                expected.actors[actor].source.source_id
                or origin[actor].get("digest") !=
                   expected.actors[actor].source.digest
                or origin[actor].get("occupied") !=
                   [list(cell) for cell in expected.actors[actor].occupied]):
            raise AssertionError("G7-H original actor footprint altered")
    remaining = {}
    resource_round = {}
    exited = set()
    for event in ledger:
        kind, d = event["kind"], event["detail"]
        if kind == "turn_resources":
            actor = d.get("actor")
            if (actor not in ROSTER or event["turn"] != actor
                    or type(d.get("mp")) is not int
                    or not 0 <= d["mp"] <= 12):
                raise AssertionError("G7-H native source MP cannot be fabricated")
            remaining[actor] = d["mp"]
            resource_round[actor] = event["round"]
        elif kind in ("g1_allied_transit_step", "g1_allied_transit_finished",
                      "g1_movement_interception_resolved"):
            # No alternate MP path or sourced allied transits in this
            # bounded G7-G cautious scene. Do not skip unknown geometry.
            raise AssertionError("Unreplayable movement cannot fund G7-H exit")
        elif kind == "g1_movement_step":
            actor = d.get("actor")
            if (actor not in ROSTER or actor in exited
                    or event["turn"] != actor
                    or resource_round.get(actor) != event["round"]
                    or actor not in remaining
                    or d.get("cautious") is not True
                    or d.get("crawl") is not False
                    or d.get("reserved") is not False
                    or d.get("opportunity_sources") != []):
                raise AssertionError("Unsupported or unfunded G7-H G1 move")
            source = expected.actors[actor]
            before = [list(cell) for cell in source.occupied]
            if d.get("old") != before:
                raise AssertionError("G7-H G1 old coordinate breaks source movement continuity")
            kind_step = d.get("step_kind")
            try:
                if kind_step in ("orthogonal", "diagonal"):
                    direction = d.get("direction")
                    if (not isinstance(direction, list) or len(direction) != 2
                            or any(type(x) is not int or x not in (-1, 0, 1)
                                   for x in direction)
                            or direction == [0, 0]
                            or d.get("pivot_anchor") is not None
                            or d.get("clockwise") is not None):
                        raise ValueError("Malformed G1 translation")
                    destination, price, parsed_kind, allies = grid.preview(
                        actor, delta=tuple(direction), cautious=True)
                elif kind_step == "pivot":
                    anchor = d.get("pivot_anchor")
                    clockwise = d.get("clockwise")
                    if (actor != "hunter" or anchor not in ("head", "rear")
                            or type(clockwise) is not bool
                            or d.get("direction") is not None):
                        raise ValueError("Unfunded or malformed Hunter pivot")
                    destination, price, parsed_kind, allies = grid.preview(
                        actor, pivot=anchor, clockwise=clockwise, cautious=True)
                else:
                    raise ValueError("Unsupported G1 movement geometry")
            except (ValueError, UnresolvedDecision) as error:
                raise AssertionError("G7-H G1 source preview rejects movement") from error
            if (allies or parsed_kind != kind_step
                    or d.get("new") != [list(cell) for cell in destination]
                    or type(d.get("cost")) is not int or d["cost"] != price
                    or price > remaining[actor]
                    or type(d.get("mp_remaining")) is not int
                    or d["mp_remaining"] != remaining[actor] - price):
                raise AssertionError("G7-H G1 move geometry, MP or destination altered")
            remaining[actor] -= price
            source.occupied = destination
        elif kind == "g5_terminal_exit":
            actor = d.get("actor")
            if (actor not in ROSTER[1:] or actor in exited
                    or event["turn"] != actor):
                raise AssertionError("G7-H cannot move a departed or wrong actor")
            exited.add(actor)
        elif kind == "turn_end":
            actor = d.get("actor")
            if (actor not in remaining
                    or resource_round.get(actor) != event["round"]
                    or d.get("unused_mp") != remaining[actor]):
                raise AssertionError("G7-H G1 MP does not reconcile at native Turn End")
    return {actor: [list(cell) for cell in expected.actors[actor].occupied]
            for actor in ROSTER}


def _authored_exit_chains(ledger, terminal):
    """Validate all original G7-C G1 -> G4.5 -> G5 source-backed exits."""
    proven_positions = _replay_native_exit_geometry(ledger)
    e0 = ledger[0]["detail"]
    maps = [x for x in ledger if x["kind"] == "g1_map_installed"]
    if len(maps) != 1:
        raise AssertionError("Missing native G1 authored exit map")
    grid = maps[0]["detail"]
    if grid.get("scene") != "G6C-clear-mixed-front":
        raise AssertionError("G7-H exit policy must use original G6-C grid")
    authors = [x for x in ledger if x["kind"] == "g5_scene_exit_authored"]
    exits = [x for x in ledger if x["kind"] == "g5_terminal_exit"]
    bridges = [x for x in ledger if x["kind"] == "g45_withdrawal_attested"]
    party = ROSTER[1:]
    if (len(authors) != 4 or len(exits) != 4 or len(bridges) != 4
            or {x["detail"].get("actor") for x in authors} != set(party)
            or {x["detail"].get("actor") for x in exits} != set(party)
            or {x["detail"].get("actor") for x in bridges} != set(party)):
        raise AssertionError("Each PC needs unique authored/G4.5/G5 exit receipts")
    receipts = []
    for actor in party:
        auth = next(x for x in authors if x["detail"]["actor"] == actor)
        exit_event = next(x for x in exits if x["detail"]["actor"] == actor)
        signed = next(x for x in bridges if x["detail"]["actor"] == actor)
        square = G7C_BORDER_SQUARES[actor]
        policy = f"G7C:party:{actor}:border"
        at = exit_event["detail"]
        step_index = at.get("movement_index")
        if (auth["detail"].get("encounter_scene") != e0.get("scenario")
                or auth["detail"].get("grid_scene") != grid["scene"]
                or auth["detail"].get("objective") != e0.get("objective")
                or auth["detail"].get("policy") != policy
                or auth["detail"].get("square") != square
                or auth["round"] != 1 or auth["turn"] is not None
                or at.get("policy") != policy or at.get("at") != square
                or type(step_index) is not int
                or not auth["index"] < step_index < signed["index"]
                < exit_event["index"] < terminal["index"]
                or signed["detail"].get("status") != "withdrawal_attested"
                or signed["detail"].get("exit_policy_reference") != policy
                or signed["detail"].get("movement_event_index") != step_index
                or signed["detail"].get("round") != exit_event["round"]
                or signed["round"] != exit_event["round"]
                or signed["turn"] != exit_event["turn"]
                or exit_event["turn"] != actor):
            raise AssertionError("G7-H actor's authored border or signed exit mismatched")
        step = ledger[step_index]
        mv = step["detail"]
        if (step["kind"] != "g1_movement_step"
                or step["turn"] != actor or step["round"] != exit_event["round"]
                or mv.get("actor") != actor
                or mv.get("step_kind") not in ("orthogonal", "diagonal")
                or mv.get("old") == mv.get("new")
                or mv.get("new") != [square]
                or mv.get("cautious") is not True
                or type(mv.get("cost")) is not int or mv["cost"] <= 0):
            raise AssertionError("Exit requires paid final G1 cautious translation")
        # Once G5 has signed an exit, that actor has no more source turns,
        # harm or movement, even if later geometry would return to border.
        if any(v["index"] > exit_event["index"] and (
                (v["kind"] == "g4_damage_applied"
                 and v["detail"].get("recipient") == actor)
                or (v["kind"] in ("action_committed", "turn_start_expiry",
                                    "turn_resources")
                    and v["detail"].get("actor") == actor)
                or (v["kind"].startswith("g1_")
                    and (v["detail"].get("actor") == actor
                         or v["detail"].get("mover") == actor)))
               for v in ledger):
            raise AssertionError("Exited actor continued native scene activity")
        receipts.append({"actor": actor, "policy": policy,
                         "movement": step_index, "g45": signed["index"],
                         "g5": exit_event["index"]})
    if (terminal["detail"].get("member_exits") != receipts
            or terminal["detail"].get("party") != list(party)):
        raise AssertionError("G7-C terminal exits disagree with four native receipt chains")
    return receipts

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
        _lethal_bow_terminal_chain(ledger, terminal, bows[0])
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
        lethal_indices = terminal["detail"].get("lethal_damage_indices")
        if (not isinstance(lethal_indices, list)
                or len(lethal_indices) != len(ROSTER[1:])
                or len(set(lethal_indices)) != len(lethal_indices)
                or terminal["detail"].get("party") != list(ROSTER[1:])):
            raise AssertionError("G7-C lethal indices must bind all original PCs")
        proven = []
        for victim in ROSTER[1:]:
            deaths = [e for e in events["g4_damage_applied"]
                      if e["detail"].get("recipient") == victim
                      and e["detail"].get("dead") is True
                      and e["detail"].get("cause") == "source-profile:B06-AT-04"]
            if len(deaths) != 1:
                raise AssertionError("Every source PC needs one actual lethal Bite")
            death = deaths[0]
            hits = [hit for hit in _hunter_bite_hits(ledger, victim)
                    if hit["damage"]["index"] == death["index"]
                    and hit["bridge"]["detail"]["actual_result"].get("dead") is True
                    and hit["resolved"]["detail"]["damage"].get("dead") is True]
            if len(hits) != 1:
                raise AssertionError("Lethal G4 event lacks paid G5 roll/G4.5/resolved Bite")
            proven.append(death["index"])
        if proven != lethal_indices:
            raise AssertionError("G7-C death indices differ from independently resolved Bites")
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
        pursuit = p[0]
        if (pursuit["round"] != 2 or pursuit["turn"] != "hunter"
                or items[0]["detail"].get("pursuit_index") != pursuit["index"]):
            raise AssertionError("Authenticated pursuit must bind the actual second Hunter turn")
        move_indices = pursuit["detail"]["movement_indices"]
        if len(set(move_indices)) != len(move_indices):
            raise AssertionError("Repeated Hunter movement index in pursuit")
        for step_index in move_indices:
            if (type(step_index) is not int
                    or not 0 <= step_index < pursuit["index"]):
                raise AssertionError("Invalid G1 pursuit movement index")
            step = ledger[step_index]
            if (step["kind"] != "g1_movement_step"
                    or step["round"] != 2 or step["turn"] != "hunter"
                    or step["detail"].get("actor") != "hunter"
                    or step["detail"].get("cautious") is not True
                    or type(step["detail"].get("cost")) is not int
                    or step["detail"]["cost"] <= 0):
                raise AssertionError("Hunter pursuit requires source-paid Round-2 G1 MP")
        bite_hits = _hunter_bite_hits(ledger, "vanguard")
        if (len(bite_hits) != 2 or
                [h["resolved"]["round"] for h in bite_hits] != [1, 2]
                or bite_hits[0]["resolved"]["index"] >= pursuit["index"]
                or bite_hits[1]["roll"]["index"] <= pursuit["index"]
                or bite_hits[1]["resolved"]["index"] >= terminal["index"]
                or items[0]["detail"].get("hunter_paid_bite_indices") !=
                   [h["resolved"]["index"] for h in bite_hits]):
            raise AssertionError(
                "G7-G opposed withdrawal needs two real paid Bites, including post-pursuit")
        receipts = _authored_exit_chains(ledger, terminal)
        if items[0]["detail"].get("border_exit_indices") != [
                receipt["g5"] for receipt in receipts]:
            raise AssertionError("G7-G verification's exit indices diverged from native receipts")
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
