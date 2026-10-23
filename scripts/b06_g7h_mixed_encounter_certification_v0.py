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



# Authored G7-H input dice, independent of editable trial/roll summaries.
# G6-D run_i3_defeat's finishing R shot uses 20/20, (4, 4), damage d4=4.
# G7-G _bite uses 20/20, (4, 4), damage d6=6 for defeat; 12,
# no confirmation or critical dice, damage d6=1 for withdrawal.
# G6-C's round-two Hunter attack is face=10, damage d6=1.
BOW_FINISH_DICE = (20, 20, (4, 4), 4)
BITE_AUTHORED_DICE = {
    "mixed_victory_rite": (10, None, (), 1),
    "hunter_multitarget_defeat": (20, 20, (4, 4), 6),
    "opposed_living_hunter_withdrawal": (12, None, (), 1),
}
BITE_TARGET_ARMOR = {
    "vanguard": 3, "guardian": 5, "archer": 3, "scholar": 3,
}


def _paid_action_ap(ledger, action, *, actor, cost, kind, label):
    """Reconcile native current-turn AP from Step 4 through the payment."""
    d = action["detail"]
    if (action["kind"] != "action_committed"
            or action["turn"] != actor or action["round"] < 1
            or d.get("actor") != actor or d.get("action_class") != kind
            or d.get("label") != label
            or type(d.get("ap_spent")) is not int or d["ap_spent"] != cost
            or type(d.get("ap_remaining")) is not int):
        raise AssertionError("Source action's exact AP debit is invalid")
    resources = [v for v in ledger[:action["index"]]
                 if v["kind"] == "turn_resources"
                 and v["round"] == action["round"] and v["turn"] == actor
                 and v["detail"].get("actor") == actor]
    if len(resources) != 1 or type(resources[0]["detail"].get("ap")) is not int:
        raise AssertionError("Source AP payment missing genuine own-turn resources")
    start = resources[0]
    # This authored pack never grants extra Turn AP from equipment, spells
    # or Blink. The turn's initial allowance is the canonical source sheet,
    # not an editable turn_resources amount that can fund forged actions.
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
    genesis = ledger[0]["detail"]
    level = genesis["source_ids"]["vanguard"]["level"]
    expected = mixed_scene(size=4, level=level, seed=genesis["seed"])
    if (start["detail"]["ap"] != expected.e.actors[actor].ap_total
            or start["detail"]["ap"] <= 0):
        raise AssertionError("Paid G7-H action lacks source-authored Turn AP")
    earlier = [v for v in ledger[start["index"]+1:action["index"]]
               if v["kind"] == "action_committed" and v["turn"] == actor
               and v["round"] == action["round"]]
    if any(type(v["detail"].get("ap_spent")) is not int
           or v["detail"]["ap_spent"] <= 0 for v in earlier):
        raise AssertionError("Unfunded earlier source action")
    remaining = start["detail"]["ap"] - sum(
        v["detail"]["ap_spent"] for v in earlier) - cost
    if remaining < 0 or d["ap_remaining"] != remaining:
        raise AssertionError("Native AP remainder does not follow paid actions")
    return remaining


def _native_round_turn_chronology(ledger):
    """Replay every authoritative G0 Round Begin/End and Initiative boundary."""
    current_round, slot, active, completed = 0, 0, None, 0
    for event in ledger:
        kind, round_no, turn, detail = (
            event["kind"], event["round"], event["turn"], event["detail"])
        if kind == "round_begin":
            if (active is not None or slot != 0 or current_round != completed
                    or round_no != completed + 1 or turn is not None
                    or detail.get("refreshed") != list(ROSTER)):
                raise AssertionError("G0 Round Begin out of chronological order")
            current_round = round_no
        elif kind == "turn_start_expiry":
            if (current_round == 0 or active is not None
                    or slot >= len(ROSTER) or round_no != current_round
                    or turn != ROSTER[slot]
                    or detail.get("actor") != ROSTER[slot]):
                raise AssertionError("Native Initiative turn opened for wrong actor")
            active = turn
        elif kind == "turn_end":
            if (active != turn or round_no != current_round
                    or detail.get("actor") != ROSTER[slot]
                    or turn != ROSTER[slot]):
                raise AssertionError("Native Initiative turn ended out of order")
            active = None
            slot += 1
        elif kind == "round_end":
            if (active is not None or slot != len(ROSTER)
                    or round_no != current_round or turn is not None
                    or current_round != completed + 1):
                raise AssertionError("Native Round End does not close five paid turns")
            completed += 1
            slot = 0
        elif event["index"] == 0:
            if kind != "encounter_created" or round_no != 0 or turn is not None:
                raise AssertionError("Native genesis is not round zero")
        elif (round_no != current_round or turn != active):
            raise AssertionError("G0 non-boundary event is outside its actual turn/round")
    if active is not None or completed < 1 or slot != 0 or current_round != completed:
        raise AssertionError("G0 certified trace ended with open native turn or round")
    return completed



def _attest_unopposed_response_window(ledger, *, trigger, actor, round_no,
                                      before_index, after_index):
    """Require the full legal G0 window authorizing one subsequent source action.

    The G7-H Bow and Cautious G1 steps predeclare no Interceptions or
    spontaneous responses. A recomputed digest cannot authorize an action
    after either recheck failed, after a cancellation, or via a duplicated
    ready receipt. Bind all four events to this exact trigger and actor turn.
    """
    required = ("response_window_open", "trigger_rechecked_after_interceptions",
                "trigger_rechecked_after_responses", "trigger_ready_to_resolve")
    scoped = [v for v in ledger if v["detail"].get("trigger") == trigger]
    if (type(trigger) is not str or not trigger
            or [v["kind"] for v in scoped] != list(required)
            or not before_index < scoped[0]["index"]
                   < scoped[1]["index"] < scoped[2]["index"]
                   < scoped[3]["index"] < after_index
            or any(v["round"] != round_no or v["turn"] != actor for v in scoped)
            or scoped[1]["detail"].get("legal") is not True
            or scoped[2]["detail"].get("legal") is not True):
        raise AssertionError(
            "Source action lacks a complete legal G0 response-window ready chain")
    return scoped[0], scoped[3]


def _attest_g1_step_response_window(ledger, step):
    """Bind a G1 movement receipt to its own immediately preceding ready.

    G7-G calls one source G1 step/pivot without explicit trigger override.
    G1 builds its key from the *opening ledger index*. That construction,
    exact same-turn G0 rechecks, and adjacency of ready -> committed step
    prevent borrowing another step's valid window.
    """
    idx = step["index"]
    if idx < 1 or ledger[idx - 1]["kind"] != "trigger_ready_to_resolve":
        raise AssertionError("G1 step lacks its own legal response-window ready chain")
    ready = ledger[idx - 1]
    actor = step["detail"].get("actor")
    trigger = ready["detail"].get("trigger")
    openings = [v for v in ledger[:idx] if
                v["kind"] == "response_window_open"
                and v["detail"].get("trigger") == trigger]
    if (actor not in ROSTER or len(openings) != 1
            or trigger != f"g1:{actor}:step:{openings[0]['index']}"):
        raise AssertionError("G1 step has no uniquely source-bound response-window trigger")
    opening, signed = _attest_unopposed_response_window(
        ledger, trigger=trigger, actor=actor, round_no=step["round"],
        before_index=-1, after_index=idx)
    if (signed["index"] != idx - 1 or
            any(v["kind"] == "response_window_open"
                for v in ledger[opening["index"] + 1:idx])):
        raise AssertionError("G1 step cannot borrow another movement response window")
    return signed["index"]


def _attest_bite_response_window(ledger, *, action_index, attested_index, roll):
    """Bind one Bite roll to G0's real, legal, *ready* response trigger.

    G5 cannot resolve after either failed recheck. The event digest alone is
    not a witness of this legality: all four G0 receipts must precede the
    original G5 roll, with no cancellation or unmodelled responses.
    """
    trigger = f"g5:melee:{action_index}"
    required = ("response_window_open", "trigger_rechecked_after_interceptions",
                "trigger_rechecked_after_responses", "trigger_ready_to_resolve")
    events = [v for v in ledger
              if v["detail"].get("trigger") == trigger
              and v["kind"] in (*required, "trigger_cancelled_before_spontaneous",
                                "trigger_cancelled_after_spontaneous",
                                "interception_released", "spontaneous_committed",
                                "g5_melee_cancelled")]
    if ([v["kind"] for v in events] != list(required)
            or any(v["round"] != roll["round"] or v["turn"] != "hunter"
                   for v in events)
            or not attested_index < events[0]["index"]
                   < events[1]["index"] < events[2]["index"]
                   < events[3]["index"] < roll["index"]
            or any(v["detail"].get("legal") is not True for v in events[1:3])
            or roll["detail"].get("spontaneous_policy") != "decline_all"):
        raise AssertionError("Hunter Bite lacks one legal G0 response-window ready chain")
    return events[3]["index"]


def _reconcile_all_turn_end_ap(ledger, *, level, seed):
    """Replay Step-4 resources, every native AP debit and exact Turn-End AP.

    Compare first against genuine L2/L3 source turn budgets (not a mutable
    receipt); a Dying actor receives zero, including when it merely holds.
    These policies do not use Blink debt or action-grant mechanics.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
    baseline = mixed_scene(size=4, level=level, seed=seed).e
    hp = {actor: ledger[0]["detail"]["source_ids"][actor]["hp"]
          for actor in ROSTER}
    active, balance, turn_no = None, None, None
    seen_resources = False
    closed = 0
    for ev in ledger:
        kind, d = ev["kind"], ev["detail"]
        if kind == "regeneration_step":
            actor = d.get("actor")
            if actor in hp:
                hp[actor] = d["hp_after"]
        elif kind == "g4_damage_applied":
            actor = d.get("recipient")
            if actor in hp:
                hp[actor] = d["hp_after"]
        elif kind == "g4_basic_heal_applied":
            actor = d.get("recipient")
            if actor in hp:
                hp[actor] += d["hp_restored"]
        if kind == "turn_start_expiry":
            if active is not None or d.get("actor") not in ROSTER:
                raise AssertionError("Unexpected overlapping native turn AP budgets")
            active, balance, turn_no = d["actor"], None, ev["round"]
            seen_resources = False
        elif kind == "turn_resources":
            actor = d.get("actor")
            if (actor != active or turn_no != ev["round"]
                    or ev["turn"] != active or seen_resources
                    or type(d.get("ap")) is not int):
                raise AssertionError("Native Turn AP allowance lacks original Step 4")
            expected = baseline.actors[actor].ap_total if hp[actor] > 0 else 0
            if d["ap"] != expected:
                raise AssertionError("Native Step-4 AP differs from source living/Dying budget")
            balance = d["ap"]
            seen_resources = True
        elif kind == "action_committed":
            actor = d.get("actor")
            if (actor != active or ev["turn"] != active
                    or ev["round"] != turn_no or not seen_resources):
                raise AssertionError("AP action was not on a funded native turn")
            a = baseline.actors[actor]
            costs = {"physical": a.physical_ap, "projection": a.projection_ap,
                     "general": 24, "full": a.ap_total}
            cost = costs.get(d.get("action_class"))
            if (type(cost) is not int or cost <= 0
                    or type(d.get("ap_spent")) is not int
                    or d["ap_spent"] != cost or cost > balance
                    or type(d.get("ap_remaining")) is not int
                    or d["ap_remaining"] != balance - cost):
                raise AssertionError("Native source Turn AP action debit is inconsistent")
            balance -= cost
        elif kind == "turn_end":
            if (d.get("actor") != active or ev["turn"] != active
                    or ev["round"] != turn_no or not seen_resources
                    or type(d.get("unused_ap")) is not int
                    or d["unused_ap"] != balance):
                raise AssertionError("Turn End unused AP is not the source-paid remainder")
            active, balance, turn_no = None, None, None
            closed += 1
    if active is not None or closed == 0:
        raise AssertionError("Incomplete AP replay at native Round End")
    return closed


def _hp_damage_packet(ledger, damage, *, target, raw, mitigated,
                      cause, damage_type, armor_rule):
    """Recompute typed native G4 HP loss, including lethal floor clipping."""
    d = damage["detail"]
    genesis = ledger[0]["detail"]["source_ids"]
    hpmax = genesis[target]["hp"]
    packet = {"resource": "hp", "type": damage_type, "raw": raw,
              "mitigated": mitigated, "armor_rule": armor_rule}
    if (damage["kind"] != "g4_damage_applied"
            or d.get("recipient") != target or d.get("cause") != cause
            or d.get("packets") != [packet]
            or type(hpmax) is not int or hpmax <= 0
            or type(d.get("hp_before")) is not int
            or type(d.get("hp_after")) is not int
            or d["hp_after"] != max(-hpmax, d["hp_before"] - mitigated)
            or d.get("vigor_after") != d.get("vigor_before")
            or d.get("vigor_details") != []):
        raise AssertionError("G4 typed damage packet cannot follow source damage dice")
    return d["hp_before"] - d["hp_after"]

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
    # Reconstruct every fixture independently of the attacker/target,
    # mutable genesis digests, snapshot strings and G4.5 target_source.
    # Merely making those ledger entries agree is not authentication.
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
    source_scene = mixed_scene(
        size=4, level=level, seed=seed,
        party_exits=(policy == "opposed_living_hunter_withdrawal"))
    authored_genesis = source_scene.e.ledger[0]["detail"]
    # The branch-specific G7-H/G7-G marker is not authority to replace
    # G0's original scenario contract. Reconstruct it from the native
    # G6-C factory rather than trusting a rehashed genesis policy string.
    if (genesis["detail"].get("policy") != authored_genesis["policy"]
            or genesis["detail"].get("objective") != authored_genesis["objective"]):
        raise AssertionError("G7-H G0 genesis policy/objective differs from source scene")
    source_genesis = authored_genesis["source_ids"]
    original_sources = genesis["detail"].get("source_ids")
    if (not isinstance(original_sources, dict)
            or set(original_sources) != set(ROSTER)
            or original_sources != source_genesis
            or any(original_sources[actor].get("digest") !=
                   source_scene.e.actors[actor].source.digest
                   for actor in ROSTER)):
        raise AssertionError("G7-H original source digests diverge from authored fixtures")
    return scene


def _spell_payment_chain(ledger, event, *, actor, label, ap, vp_mode, vp_points):
    """Reconstruct one legal G0 action -> VP debit -> G3 effect/launch.

    Authoritative slots are (round, native turn, caster) and the original
    chronological indices, not an event label copied into the result.
    """
    if (event["turn"] != actor or type(event["round"]) is not int
            or event["round"] < 1):
        raise AssertionError("G3 source delivery must be on caster's own turn")
    chain = [v for v in ledger[:event["index"]]
             if v["round"] == event["round"] and v["turn"] == actor]
    actions = [v for v in chain if v["kind"] == "action_committed"
               and v["detail"].get("actor") == actor
               and v["detail"].get("label") == label]
    transitions = [v for v in chain if v["kind"] == "vp_transition"
                   and v["detail"].get("actor") == actor
                   and v["detail"].get("label") == label]
    if len(actions) != 1 or len(transitions) != 1:
        raise AssertionError("G3 source action or unique VP payment missing")
    action, payment = actions[0], transitions[0]
    if (not action["index"] < payment["index"] < event["index"]
            or action["detail"].get("action_class") != "projection"
            or type(action["detail"].get("ap_spent")) is not int
            or action["detail"]["ap_spent"] != ap
            or payment["detail"].get("mode") != vp_mode
            or type(payment["detail"].get("points")) is not int
            or payment["detail"]["points"] != vp_points
            or any(v["kind"] == "action_committed"
                   and v["detail"].get("actor") == actor
                   for v in ledger[action["index"]+1:event["index"]])
            or any(v["kind"] in ("vp_transition", "vp_release")
                   and v["detail"].get("actor") == actor
                   and v["index"] != payment["index"]
                   for v in ledger[action["index"]+1:event["index"]])):
        raise AssertionError("G3 spell must consume its exact ordered AP/VP chain")
    _paid_action_ap(ledger, action, actor=actor, cost=ap,
                    kind="projection", label=label)
    return action, payment


def _reconcile_source_vp(ledger, final):
    """Independent G0 VP accounting; an edited/omitted payment never funds a cast."""
    origin = ledger[0]["detail"].get("source_ids")
    if not isinstance(origin, dict) or set(origin) != set(ROSTER):
        raise AssertionError("G0 source VP genesis missing")
    accounts = {}
    for actor in ROSTER:
        start = origin[actor].get("vp")
        if (not isinstance(start, list) or len(start) != 3
                or any(type(x) is not int or x < 0 for x in start)):
            raise AssertionError("G0 initial VP state invalid")
        accounts[actor] = list(start)
    for ev in ledger[1:]:
        d = ev["detail"]
        if ev["kind"] == "vp_transition":
            actor, mode, points = d.get("actor"), d.get("mode"), d.get("points")
            if (actor not in accounts or ev["turn"] != actor
                    or mode not in ("spent", "committed")
                    or type(points) is not int or points <= 0
                    or points > accounts[actor][0]):
                raise AssertionError("Invalid source G0 VP debit")
            accounts[actor][0] -= points
            accounts[actor][1 if mode == "committed" else 2] += points
        elif ev["kind"] == "vp_release":
            actor, points = d.get("actor"), d.get("points")
            if (actor not in accounts or type(points) is not int or points <= 0
                    or points > accounts[actor][1]):
                raise AssertionError("Invalid source G0 VP release")
            accounts[actor][0] += points
            accounts[actor][1] -= points
    if any(final[actor].get("vp_available") != accounts[actor][0]
           or final[actor].get("vp_committed") != accounts[actor][1]
           for actor in ROSTER):
        raise AssertionError("Final source VP state disagrees with paid ledger")
    return accounts



def _reconcile_source_regeneration(ledger, final, *, policy, level, seed):
    """Audit G4 Step 2 against source HP, Vigor and throughput, not hash alone.

    These three *fixed* authored policies use natural HP recovery and
    Dying-loss cancellation, but NEVER voluntary wound repair or external
    Basic Heal. Explicitly reject an unmodelled repair/heal here rather
    than certify it by replaying untrusted transition amounts.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene

    reference = mixed_scene(
        size=4, level=level, seed=seed,
        party_exits=(policy == "opposed_living_hunter_withdrawal")).e
    genesis = ledger[0]["detail"]["source_ids"]
    hp = {actor: genesis[actor]["hp"] for actor in ROSTER}
    vigor = {actor: genesis[actor]["vigor"] for actor in ROSTER}
    hp_limits = {actor: reference.actors[actor].hp_max for actor in ROSTER}
    vigor_limits = {actor: reference.actors[actor].vigor_max for actor in ROSTER}
    regenerated = set()
    rites = set()
    for ev in ledger:
        d, kind = ev["detail"], ev["kind"]
        if kind == "g3_effect_established" and (
                d.get("effect_kind") == "Guided Regeneration"
                and d.get("caster") == "archer"
                and d.get("recipient") == "archer"):
            if policy != "mixed_victory_rite":
                raise AssertionError("Other authored packs have no Guided Rite")
            rites.add("archer")
        elif kind == "g3_effect_ended" and d.get("caster") == "archer":
            rites.discard("archer")
        elif kind == "g4_damage_applied":
            actor = d.get("recipient")
            if (actor not in hp or
                    any(type(d.get(key)) is not int for key in (
                        "hp_before", "hp_after", "vigor_before", "vigor_after"))
                    or (d["hp_before"], d["vigor_before"]) !=
                       (hp[actor], vigor[actor])
                    or not -hp_limits[actor] <= d["hp_after"] <= hp_limits[actor]
                    or not 0 <= d["vigor_after"] <= vigor_limits[actor]):
                raise AssertionError("G4 damage violates source HP/Vigor continuity")
            hp[actor], vigor[actor] = d["hp_after"], d["vigor_after"]
        elif kind == "g4_basic_heal_applied":
            raise AssertionError(
                "Fixed G7-H policies have no source-authored external Basic Heal")
        elif kind in ("regeneration_step", "regeneration_dead"):
            actor = d.get("actor")
            key = (ev["round"], actor)
            if (actor not in hp or ev["turn"] != actor
                    or ev["round"] < 1 or key in regenerated):
                raise AssertionError("G4 regeneration must occur once on its own turn")
            regenerated.add(key)
            # Every Step 2 must occur after Step 1 and before the one
            # Step 4 source resource grant for the same native turn.
            before = [x for x in ledger[:ev["index"]]
                      if x["round"] == ev["round"]
                      and x["turn"] == actor and
                      x["kind"] == "turn_start_expiry"]
            after = [x for x in ledger[ev["index"] + 1:]
                     if x["round"] == ev["round"]
                     and x["turn"] == actor and
                     x["kind"] == "turn_resources"]
            if len(before) != 1 or len(after) != 1:
                raise AssertionError("Regeneration not between native Step 1 and Step 4")
            hpmax, vmax = hp_limits[actor], vigor_limits[actor]
            if kind == "regeneration_dead":
                if hp[actor] != -hpmax:
                    raise AssertionError("Living source actor cannot skip Step 2 as dead")
                continue
            fields = ("hp_before", "hp_after", "hp_restored",
                      "vigor_before", "vigor_after", "repair_points",
                      "throughput_spent")
            if (any(type(d.get(k)) is not int for k in fields)
                    or type(d.get("survival_cancelled")) is not bool
                    or type(d.get("dead")) is not bool
                    or d.get("wound_allocations") != []
                    or d["repair_points"] != 0
                    or (d["hp_before"], d["vigor_before"]) !=
                       (hp[actor], vigor[actor])):
                raise AssertionError("Regeneration receipt lacks authentic allocation")
            survival = int(d["survival_cancelled"])
            restored, spent = d["hp_restored"], d["throughput_spent"]
            available = reference.actors[actor].regen + int(actor in rites)
            dying = hp[actor] <= 0
            pre_heal = max(-hpmax, hp[actor] - int(dying and not survival))
            died = pre_heal == -hpmax
            if (restored < 0 or spent < 0
                    or (survival and not dying)
                    or (dying and restored != 0)
                    or spent != (0 if died else restored + survival)
                    or spent > available or spent > vigor[actor]
                    or d["dead"] is not died
                    or d["hp_after"] != pre_heal + (0 if died else restored)
                    or not -hpmax <= d["hp_after"] <= hpmax
                    or d["vigor_after"] != vigor[actor] - spent
                    or not 0 <= d["vigor_after"] <= vmax):
                raise AssertionError(
                    "G4 regeneration exceeds source HP/Vigor/throughput or Dying law")
            hp[actor], vigor[actor] = d["hp_after"], d["vigor_after"]
    # No Step-2 gaps: even dead characters have exactly one actual
    # regeneration_dead acknowledgement on every completed native turn.
    every_turn = {(v["round"], v["detail"]["actor"]) for v in ledger
                  if v["kind"] == "turn_start_expiry"}
    if regenerated != every_turn:
        raise AssertionError("G4 Step 2 absent or duplicated on source Initiative")
    if any(hp[actor] != final[actor]["hp"]
           or vigor[actor] != final[actor]["vigor"]
           for actor in ROSTER):
        raise AssertionError("Source regeneration/Vigor replay differs from final snapshot")
    return True


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
    if policy != "mixed_victory_rite":
        # A fresh SHA over externally supplied bytes cannot authenticate
        # *meaning* of a signed G7-C terminal. Reconstruct its entire native
        # event and returned receipt schema from the finished G0 round and
        # independently checked underlying fatal/exit evidence. Reject
        # omitted, additional or altered fields rather than cherry-picking
        # the event's lethal/exit list.
        signed = terminals[0]
        evidence = ("lethal_damage_indices"
                    if policy == "hunter_multitarget_defeat"
                    else "member_exits")
        native_detail = {
            "party": list(ROSTER[1:]),
            evidence: receipt.get(evidence),
            "round": report["rounds_completed"],
            "hunter_cr": None,
        }
        native_receipt = {
            "ending": outcome,
            "terminal_event": signed["index"],
            evidence: receipt.get(evidence),
            "hunter_cr": None,
            "complete_party_pack_certified": False,
        }
        last_end = max(x["index"] for x in ledger if x["kind"] == "round_end")
        if (signed["detail"] != native_detail
                or receipt != native_receipt
                or signed["round"] != report["rounds_completed"]
                or signed["turn"] is not None
                or signed["index"] <= last_end):
            raise AssertionError(
                "G7-C signed terminal differs from canonical party/round/"
                "rating/evidence and exact source receipt")
    if policy == "mixed_victory_rite":
        terminal = terminals[0]
        fatal_index = terminal["detail"].get("lethal_damage_index")
        source_hunter = ledger[0]["detail"]["source_ids"]["hunter"]
        lethal = (ledger[fatal_index] if type(fatal_index) is int
                  and 0 <= fatal_index < terminal["index"] else None)
        expected_detail = {
            "hunter": "hunter",
            "party": list(ROSTER[1:]),
            "lethal_damage_index": fatal_index,
            "hp": -source_hunter["hp"],
            "source_digest": source_hunter["digest"],
            "source_event_cause": (
                lethal["detail"].get("cause") if lethal is not None else None),
            "round": terminal["round"],
            "outcome": "hunter_dead_after_actual_native_combat",
            "hunter_cr": None,
        }
        if (not deaths["hunter"]
                or any(deaths[p] for p in ROSTER[1:])
                or lethal is None or lethal["kind"] != "g4_damage_applied"
                or lethal["detail"].get("recipient") != "hunter"
                or lethal["detail"].get("dead") is not True
                or terminal["turn"] is not None
                or terminal["round"] != report["rounds_completed"]
                or terminal["index"] <= max(
                    event["index"] for event in ledger if event["kind"] == "round_end")
                or terminal["detail"] != expected_detail
                or receipt.get("round") != terminal["round"]):
            raise AssertionError(
                "G6-D victory terminal is not the complete canonical source receipt")
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




def _authored_bow_lane_receipts(ledger, launch, shot, *, level, seed):
    """Derive G2 Bow firing geometry and defense from the original fixture.

    The three authored G7-H victory rounds do not move any actor. Rebuild
    the original G2 grid and Bow lane independently of mutable G2 receipts;
    an invented range, cover, obstruction or rechecked defense cannot
    become true merely by rehashing a matching Bow outcome.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene

    if any(v["kind"] in ("g1_movement_step", "g1_allied_transit_step")
           for v in ledger):
        raise AssertionError("Source G6-D victory never repositions its Bow lane")
    scene = mixed_scene(size=4, level=level, seed=seed)
    e = scene.e
    hunter_cell = e.g1.body_cell("hunter", "head")
    lane = e.g2.lane("archer", "hunter", target_cell=hunter_cell)
    if (lane.origin != e.actors["archer"].occupied[0]
            or lane.destination != hunter_cell
            or lane.screens or lane.cover or lane.effective_obstruction):
        raise AssertionError("G7-H lethal Bow requires authored clear head lane")
    base, final = e.g2._defense_value(
        e.actors["hunter"], "take_hit", lane.range_difficulty,
        lane.effective_obstruction)
    # G2 rechecks after the legal G0 response window and logs this receipt
    # immediately before spending the real arrow in g2_bow_launched.
    index = launch["index"]
    if index < 1 or shot["index"] != index + 2:
        raise AssertionError("G7-H Bow has no synchronous G2 lane/shot chain")
    recheck, faces = ledger[index - 1], ledger[index + 1]
    if (recheck["kind"] != "g2_projectile_defense_rechecked"
            or faces["kind"] != "g2_miss_faces_preallocated"
            or any(event["round"] != launch["round"]
                   or event["turn"] != "archer"
                   for event in (recheck, launch, faces, shot))
            or any(ev["detail"].get("actor") != "hunter"
                   for ev in (recheck,))
            or any(recheck["detail"].get(key) != value for key, value in {
                "declared": "take_hit", "actual": "take_hit",
                "base": base, "final": final}.items())
            or any(launch["detail"].get(key) != value for key, value in {
                "shooter": "archer", "target": "hunter",
                "attack_bonus": 4, "aim_mitigation": 0,
                "range_difficulty": lane.range_difficulty,
                "cover": lane.cover, "screens": {},
                "effective_obstruction": final - base}.items())
            or any(faces["detail"].get(key) != value for key, value in {
                "shooter": "archer", "target": "hunter",
                "faces": {}, "primary_face": shot["detail"].get("primary_face"),
                "base_defense": base, "final_defense": final}.items())
            or shot["detail"].get("base_defense") != base
            or shot["detail"].get("final_defense") != final):
        raise AssertionError(
            "G2 launch range, cover, obstruction or defense disagrees with authored lane")
    return base, final


def _reconcile_victory_bow_ammunition(ledger, initial, final, *, level):
    """Replay *every* source R Bow round from its independent B05 arrow count.

    G0 genesis does not serialize arrow inventory, so the pre-action
    snapshot must match the actual source sheet rather than being trusted
    as an arbitrary caller-supplied starting balance. Round 1 consumes
    no arrow (R casts its Chosen Rite); Round 2 launches one missed arrow
    from G6-C; Round 3 launches the G6-D lethal arrow. Each declaration,
    G2 launch and G2 resolution must agree with the same decrement, and
    the reconciled balance must equal the final original-R snapshot.
    """
    from scripts.b05_bow_vanguard_l1_l3_v0 import profile as bow_sheet
    from scripts.b06_hunter_mixed_party_g6c_v0 import POLICY

    source_ammo = bow_sheet(level)["initial_arrows"]
    if (type(source_ammo) is not int or source_ammo < 2
            or type(initial["archer"].get("ammunition")) is not int
            or initial["archer"]["ammunition"] != source_ammo):
        raise AssertionError("G7-H R opening arrows must match source B05 sheet")
    expected_faces = {2: POLICY[2]["archer"], 3: BOW_FINISH_DICE[0]}
    stages = (
        "action_committed", "g2_bow_sequence_committed",
        "g2_bow_launched", "g2_bow_shot_resolved",
    )
    timeline = {stage: [ev for ev in ledger if ev["kind"] == stage
                        and (stage != "action_committed" or
                             ev["detail"].get("label") == "g2:bow:hunter:0")]
                for stage in stages}
    # These are the only ranged G2 arrow events for this fixed victory
    # policy. A hidden launch, selected extra shot or missing resolution
    # cannot be made legitimate by modifying the final ammunition.
    if any(len(timeline[stage]) != 2 for stage in stages):
        raise AssertionError("G7-H victory requires exactly two Bow arrow chains")

    ammo = source_ammo
    for round_no, expected_face in expected_faces.items():
        items = []
        for stage in stages:
            found = [ev for ev in timeline[stage]
                     if ev["round"] == round_no and ev["turn"] == "archer"]
            if len(found) != 1:
                raise AssertionError("Source Bow arrow has missing/duplicate own-turn stage")
            items.append(found[0])
        action, declaration, launch, shot = items
        if not (action["index"] < declaration["index"]
                < launch["index"] < shot["index"]):
            raise AssertionError("G2 arrow was not declared, launched and resolved in order")
        ad, dd, ld, sd = (ev["detail"] for ev in items)
        _paid_action_ap(
            ledger, action, actor="archer", cost=20,
            kind="physical", label="g2:bow:hunter:0")
        if (ad.get("actor") != "archer"
                or dd.get("shooter") != "archer"
                or dd.get("target") != "hunter"
                or dd.get("profiles") != ["Bow"]
                or dd.get("defenses") != ["take_hit"]
                or type(dd.get("ammunition_selected")) is not int
                or dd["ammunition_selected"] != 1
                or ld.get("shooter") != "archer"
                or ld.get("target") != "hunter"
                or type(ld.get("ammo_remaining")) is not int
                or ld["ammo_remaining"] != ammo - 1
                or sd.get("shooter") != "archer"
                or sd.get("intended") != "hunter"
                or type(sd.get("ammunition_spent")) is not int
                or sd["ammunition_spent"] != 1
                or sd.get("primary_face") != expected_face
                or sd.get("outcome") != (
                    "automatic_miss" if round_no == 2
                    else "critical_confirmation_pending_G5")
                or sd.get("target") != (
                    None if round_no == 2 else "hunter")):
            raise AssertionError("G7-H G2 declared/paid/launched arrow balance changed")
        _authored_bow_lane_receipts(
            ledger, launch, shot, level=level,
            seed=ledger[0]["detail"]["seed"])
        ammo -= 1
    if (type(final["archer"].get("ammunition")) is not int
            or final["archer"]["ammunition"] != ammo):
        raise AssertionError("Closing R arrow inventory disagrees with G2 paid launches")
    return ammo


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
    _paid_action_ap(ledger, action, actor="archer", cost=20,
                    kind="physical", label="g2:bow:hunter:0")
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
    # G2 owns the projectile natural-1 auto-miss, original target and
    # ranged defense. G6-D may only resolve a confirmed *G2 hit*; comparing
    # two mutable outcome strings does not prove the actual d20 result.
    shot_d, launch_d = shot["detail"], launch["detail"]
    face = shot_d.get("primary_face")
    defense = shot_d.get("final_defense")
    confirmation = d.get("confirmation_face")
    if (type(face) is not int or not 1 <= face <= 20
            or type(defense) is not int
            or type(shot_d.get("base_defense")) is not int
            or type(shot_d.get("attack_total")) is not int
            or type(d.get("attack_total")) is not int
            or shot_d["attack_total"] != face + 4
            or d["attack_total"] != shot_d["attack_total"]
            or type(d.get("attack_face")) is not int
            or d["attack_face"] != face
            or d.get("defense_value") != defense
            or launch_d.get("attack_bonus") != 4
            or launch_d.get("cover") != 0
            or launch_d.get("range_difficulty") is None
            or shot_d["base_defense"] > defense
            or face == 1):
        raise AssertionError("Lethal Bow cannot certify false G2 roll/defense math")
    if face == 20:
        if type(confirmation) is not int or not 1 <= confirmation <= 20:
            raise AssertionError("Natural-20 Bow requires source confirmation")
        tier = ("devastating" if confirmation == 20 else
                "critical" if confirmation != 1 and confirmation + 4 > defense
                else "strong")
        delivery = "critical_confirmation_pending_G5"
    else:
        if confirmation is not None or face + 4 <= defense:
            raise AssertionError("Ordinary Bow must actually beat ranged defense")
        tier, delivery = "normal", "intended_hit_pending_G5"
    # G7-H is one preauthored *fixed-dice* witness, not a generic Bow
    # damage referee. Bind its original 20/20 + two d4 + d4 faces to the
    # typed G4 event; a rewritten ordinary d20 cannot retain a 14 HP hit.
    authored_face, authored_confirm, extras, damage_die = BOW_FINISH_DICE
    if (face != authored_face or confirmation != authored_confirm
            or tier != "devastating"):
        raise AssertionError("G7-H Bow finishing dice differ from source-authored shot")
    if (shot_d.get("outcome") != delivery
            or d.get("original_outcome") != delivery
            or d.get("critical") != tier
            or shot_d.get("target") != "hunter"
            or launch_d.get("shooter") != "archer"
            or launch_d.get("target") != "hunter"):
        raise AssertionError("Fatal G6-D Bow result must derive from native G2 d20")
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
    # A paid and launched shot must first survive its own *complete*
    # source G0 response window, not merely cite a valid G2 action index.
    # Neither a failed recheck nor a cancelled trigger may fund lethal G4.
    seed = ledger[0]["detail"].get("seed")
    expected_trigger = (
        f"g6d:bow:{seed}:{lethal['round']}:archer:hunter:one_shot")
    if d.get("shot_trigger") != expected_trigger:
        raise AssertionError("Lethal Bow response trigger differs from source shot")
    _attest_unopposed_response_window(
        ledger, trigger=expected_trigger, actor="archer",
        round_no=lethal["round"], before_index=declarations[0]["index"],
        after_index=launch_index)
    raw = 2 + damage_die + sum(extras)
    # Hunter natural hide Armor 3 is exactly bypassed by Bow Penetration 3.
    hp_loss = _hp_damage_packet(
        ledger, lethal, target="hunter", raw=raw, mitigated=raw,
        cause=f"g6d:source_bow:archer:{shot_index}",
        damage_type="Piercing", armor_rule="weapon")
    source_result = d.get("damage")
    if (not isinstance(source_result, dict)
            or source_result.get("hp_packets") != [raw]
            or source_result.get("hp_loss") != hp_loss
            or source_result.get("vigor_loss") != 0
            or source_result.get("dead") is not True
            or source_result.get("wound") != lethal["detail"].get("wound")):
        raise AssertionError("G6-D lethal Bow result cannot follow its d4 damage dice")
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



def _attest_source_bite_venom(ledger, *, policy, target, profile, bridge,
                              resolved, source_mitigated, seed, action_index):
    """Rebuild G4.4 venom from the authored die and original target Vitality.

    Merely repeating a forged resistance total/mode in G4.4, G4.5 and G5
    does not make that total legal. These fixed policies have no Ward,
    suppression, prior source toxin or elapsed Hunter-onset milestone.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene

    result = bridge["detail"]["actual_result"]
    exposure = f"g6:bite:{seed}:{action_index}"
    outcome = result.get("venom")
    profile_index = profile["index"]
    delivered = [event for event in ledger[profile_index + 1:bridge["index"]]
                 if event["kind"] in (
                     "g44_hunter_accepted", "g44_hunter_ignored",
                     "g44_hunter_prevented", "g44_hunter_not_delivered")]
    if result.get("dead") is True:
        if outcome is not None or delivered:
            raise AssertionError("Lethal Bite cannot deliver venom postmortem")
        return
    if len(delivered) != 1 or not isinstance(outcome, dict):
        raise AssertionError("Nonfatal Bite lacks one native G4.4 venom outcome")
    event = delivered[0]
    d = event["detail"]
    if (event["round"] != resolved["round"]
            or event["turn"] != "hunter"
            or event["index"] <= profile_index):
        raise AssertionError("Venom outcome is not synchronous with sourced Bite")

    existing = [v for v in ledger[:profile_index]
                if v["kind"] == "g44_hunter_accepted"
                and v["detail"].get("recipient") == target]
    # The authored encounters terminate before T+600 s/100 Round Begins,
    # without any authorized ward or other toxin application. A previous
    # accepted Moderate Hunter toxin therefore occupies this target's
    # nonstacking slot until a genuine death; an equal-grade Bite is ignored.
    if any(v["kind"] in ("g44_ward_intercepted", "g44_endurance_ended",
                        "g44_hunter_milestone")
           for v in ledger):
        raise AssertionError("G7-H fixed Bite has unsupported ward/onset effect")
    expected_type = ("g44_hunter_not_delivered" if source_mitigated <= 0
                     else "g44_hunter_ignored" if existing
                     else "g44_hunter_accepted")
    if event["kind"] != expected_type:
        raise AssertionError(
            "Hunter venom outcome contradicts puncture and source nonstacking")
    if expected_type == "g44_hunter_not_delivered":
        if (d != {"attacker": "hunter", "recipient": target,
                  "exposure_key": exposure, "hit_index": profile_index}
                or outcome != {"outcome": "not_delivered"}):
            raise AssertionError("Hunter nonpuncture venom exposure receipt mismatched")
        expected_markers = []
    elif expected_type == "g44_hunter_ignored":
        previous = existing[-1]["detail"]["key"]
        if (d != {"recipient": target, "key": exposure, "active": previous}
                or outcome != {"outcome": "ignored", "active": previous}):
            raise AssertionError("Hunter equal-grade venom exposure receipt mismatched")
        expected_markers = []
    else:
        # Fixed authored die, NOT a mutable attack/venom receipt. G6-C's
        # L2/L3 Round-2 Hunter uses natural 1; the two G7-G policies use 20.
        die = 1 if policy == "mixed_victory_rite" else 20
        reference = mixed_scene(
            size=4, level=ledger[0]["detail"]["source_ids"]["vanguard"]["level"],
            seed=seed).e
        source = reference.actors[target].source
        # The current authored G6-C scenarios begin native G0 combat rounds
        # WITHOUT a WorldClock.enter_initiative() handoff. Consequently
        # G4.4 schedules deadlines in exploration seconds, despite active
        # Initiative turn labels. A rehashed source trace cannot invent an
        # initiative conversion or elapse that clock in this fixed pack.
        if (reference.g4.clock.mode != "exploration"
                or reference.g4.clock.world_seconds != 0
                or any(v["kind"] in (
                    "g42_initiative_entered", "g42_initiative_exited",
                    "g42_exploration_advanced") for v in ledger)):
            raise AssertionError(
                "G7-H Hunter venom requires original G6-C exploration clock basis")
        vit = dict(source.abilities).get("Vitality")
        if type(vit) is not int:
            raise AssertionError("Hunter Bite target has no sourced Vitality")
        total = die + vit  # Both fixed policies use modifier=0.
        mode = "Reduced" if total >= 12 else "Full"
        tag = f"hunter:{exposure}"
        plan = ([("onset", 600), ("escalate", 1800), ("expiry", 7200)]
                if mode == "Full" else
                [("onset", 600), ("expiry", 3600)])
        expected_markers = [f"{tag}:{label}" for label, _ in plan]
        receipt = {"recipient": target, "key": exposure,
                   "resolution": mode, "resistance_total": total,
                   "hit_index": profile_index,
                   "marker_ids": expected_markers}
        if (d != receipt or
                outcome != {"outcome": "accepted", "resolution": mode,
                            "resistance_total": total}):
            raise AssertionError(
                "Hunter accepted venom does not follow authored resistance roll/Vitality")
        # All delayed stages are source-scheduled at the actual Bite, not
        # optional mutable annotations; require the exact identity, order,
        # due-round conversion and clock phase of each scheduled milestone.
        markers = [v for v in ledger
                   if v["kind"] == "g42_milestone_scheduled"
                   and (v["detail"].get("source") == tag or
                        v["detail"].get("event_id", "").startswith(tag + ":"))]
        if (len(markers) != len(plan)
                or any(v["index"] <= profile_index or v["index"] >= event["index"]
                       or v["round"] != resolved["round"]
                       or v["turn"] != "hunter"
                       or v["detail"] != {
                           "event_id": f"{tag}:{label}",
                           "actor": target, "actor_source": source.source_id,
                           "source": tag, "phase": "before_recovery",
                           "due_seconds": seconds,
                           "due_round": None,
                       }
                       for v, (label, seconds) in zip(markers, plan))):
            raise AssertionError(
                "Hunter source venom needs original scheduled milestone set")
    # An ignored/blocked puncture cannot fabricate a future Hunter timer.
    if expected_type != "g44_hunter_accepted" and any(
            v["kind"] == "g42_milestone_scheduled"
            and (v["detail"].get("source") == f"hunter:{exposure}" or
                 v["detail"].get("event_id", "").startswith(
                     f"hunter:{exposure}:"))
            for v in ledger):
        raise AssertionError("Unsourced Hunter venom milestones on nonacceptance")
    if any(v["kind"] in ("g42_milestone_due", "g42_milestone_canceled")
           and v["detail"].get("source") == f"hunter:{exposure}"
           for v in ledger):
        raise AssertionError("Hunter onset cannot occur in bounded G7-H turns")


def _hunter_bite_hits(ledger, target, *, policy):
    """Reconstruct each *resolved* Hunter Bite from its source-paid G0 chain.

    A cancelled paid slot is NOT a hit, even if an earlier G4 packet and a
    G7-C terminal are left in a tampered ledger. All five stages are bound
    to the same paid action, target, source profile and native actor turn.
    """
    if policy not in BITE_AUTHORED_DICE:
        raise AssertionError("Only source-authored G7-H Bite policies are certified")
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
                or declaration["round"] != resolved["round"]
                or declaration["turn"] != "hunter"
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
        _attest_bite_response_window(
            ledger, action_index=action_index,
            attested_index=attested["index"], roll=roll)
        # Hunter source B06-AT-04 is +6, and these two G7-G policies
        # predeclare a standing one-square Take Hit target. Recompute the
        # attack and critical legality from its actual d20 and native G0
        # defense receipt: a natural 1 must NEVER certify a hit.
        rd = roll["detail"]
        defense_positions = seq.get("defense_indices")
        if (not isinstance(defense_positions, list)
                or len(defense_positions) <= position
                or type(defense_positions[position]) is not int
                or not 0 <= defense_positions[position] < roll["index"]):
            raise AssertionError("Hunter Bite requires native assigned defense")
        assigned = ledger[defense_positions[position]]
        declared_defenses = declaration["detail"].get("defenses")
        if (not isinstance(declared_defenses, list)
                or len(declared_defenses) != len(seq["action_indices"])
                or declared_defenses[position] != "take_hit"
                or not declaration_index < assigned["index"] < attested["index"]
                or len(set(defense_positions)) != len(defense_positions)
                or assigned["kind"] != "defense_assigned"
                or assigned["round"] != roll["round"]
                or assigned["turn"] != "hunter"
                or assigned["detail"].get("actor") != target
                or assigned["detail"].get("attack_key") !=
                   f"hunter:{target}:{position}"
                or assigned["detail"].get("defense") !=
                   declared_defenses[position]
                or assigned["detail"].get("defense") != "take_hit"
                or assigned["detail"].get("defense_value") is not None
                or rd.get("defense") != "take_hit"
                or rd.get("declared_defense") != "take_hit"
                or rd.get("defense_value") is not None):
            raise AssertionError("Native Hunter Bite defense was altered")
        face = rd.get("attack_face")
        confirm = rd.get("confirmation_face")
        if (type(face) is not int or not 1 <= face <= 20
                or face == 1
                or type(rd.get("source_attack_bonus")) is not int
                or rd["source_attack_bonus"] != 6
                or type(rd.get("prone_modifier")) is not int
                or rd["prone_modifier"] != 0
                or type(rd.get("attack_bonus")) is not int
                or rd["attack_bonus"] != 6
                or type(rd.get("attack_total")) is not int
                or rd["attack_total"] != face + 6
                or rd.get("hit") is not True
                or type(action["detail"].get("ap_spent")) is not int
                or action["detail"]["ap_spent"] != 24):
            raise AssertionError("Lethal/withdrawal Bite is not a legal paid G5 d20 hit")
        if face == 20:
            if type(confirm) is not int or not 1 <= confirm <= 20:
                raise AssertionError("Hunter natural-20 must be confirmed")
            expected_critical = ("devastating" if confirm == 20 else "critical")
        else:
            if confirm is not None:
                raise AssertionError("Ordinary Hunter Bite cannot confirm critical")
            expected_critical = "normal"
        authored_face, authored_confirmation, authored_extras, authored_damage = (
            BITE_AUTHORED_DICE[policy])
        if (policy == "mixed_victory_rite" and resolved["round"] != 2
                or face != authored_face or confirm != authored_confirmation
                or len(authored_extras) !=
                    {"normal": 0, "strong": 1,
                     "critical": 2, "devastating": 2}[expected_critical]):
            raise AssertionError("Hunter Bite differs from fixed source-authored damage dice")
        _paid_action_ap(ledger, action, actor="hunter", cost=24,
                        kind="physical", label=f"sequence:B06-AT-04:{position}")
        if (rd.get("critical") != expected_critical
                or d.get("critical") != expected_critical):
            raise AssertionError("Hunter Bite critical tier is not source-derived")
        damages = [x for x in ledger
                   if x["kind"] == "g4_damage_applied"
                   and roll["index"] < x["index"] < bridge["index"]
                   and x["detail"].get("recipient") == target
                   and x["detail"].get("cause") == "source-profile:B06-AT-04"]
        if len(damages) != 1:
            raise AssertionError("Hunter Bite has no single synchronous G4 packet")
        damage = damages[0]
        result = bridge["detail"]["actual_result"]
        source_raw = 3 + authored_damage + sum(authored_extras)
        mitigation = max(0, BITE_TARGET_ARMOR[target] - 1)
        source_mitigated = max(0, source_raw - mitigation)
        loss = _hp_damage_packet(
            ledger, damage, target=target,
            raw=source_raw, mitigated=source_mitigated,
            cause="source-profile:B06-AT-04",
            damage_type="Piercing", armor_rule="weapon")
        profiles = [x for x in ledger[damage["index"]+1:bridge["index"]]
                    if x["kind"] == "g4_profile_hit"
                    and x["detail"].get("attacker") == "hunter"
                    and x["detail"].get("target") == target
                    and x["detail"].get("profile") == "B06-AT-04"]
        if (len(profiles) != 1 or
                profiles[0]["detail"].get("critical") != expected_critical
                or profiles[0]["round"] != resolved["round"]
                or profiles[0]["turn"] != "hunter"
                or result.get("hp_packets") != [source_mitigated]
                or result.get("hp_loss") != loss or
                result.get("vigor_loss") != 0):
            raise AssertionError("Native G4 Bite packet and profile result not source-derived")
        # G4 computes puncture eligibility from this *specific* source
        # Piercing HP packet. Never allow a rehashed G4 eligibility flag
        # to contradict the G4.5/G5 result or synchronous G4.4 venom.
        profile = profiles[0]
        eligible = source_mitigated > 0
        if (profile["index"] <= damage["index"]
                or profile["index"] >= bridge["index"]
                or profile["detail"].get("injection_eligible") is not eligible
                or result.get("injection_eligible") is not eligible):
            raise AssertionError("Bite G4 profile injection eligibility contradicts attested G4.5 result")
        exposure = f"g6:bite:{seed}:{action_index}"
        _attest_source_bite_venom(
            ledger, policy=policy, target=target, profile=profile,
            bridge=bridge, resolved=resolved, source_mitigated=source_mitigated,
            seed=seed, action_index=action_index)
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


def _replay_native_exit_geometry(ledger, *, party_exits=True):
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
                        seed=seed, party_exits=party_exits)
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
            # G0 Step 4 grants a fixed 12 base MP plus genuinely live
            # source penalties. None of these <100-round fixed policies can
            # reach Hunter venom onset; the independently constructed G6-C
            # source actor therefore has exactly 12 MP on every turn.
            # The receipt cannot invent a smaller opening allowance and
            # then make its own movement/Turn End arithmetic self-consistent.
            source_mp = max(
                0, 12 + expected.g4.toxins.modifier(actor, "mp")
            ) if actor in ROSTER else None
            if (actor not in ROSTER or event["turn"] != actor
                    or type(d.get("mp")) is not int
                    or d["mp"] != source_mp):
                raise AssertionError(
                    "G7-H native Step-4 MP differs from source allowance")
            remaining[actor] = source_mp
            resource_round[actor] = event["round"]
        elif kind in ("g1_allied_transit_step", "g1_allied_transit_finished",
                      "g1_movement_interception_resolved"):
            # No alternate MP path or sourced allied transits in this
            # bounded G7-G cautious scene. Do not skip unknown geometry.
            raise AssertionError("Unreplayable movement cannot fund G7-H exit")
        elif kind == "g1_movement_step":
            # Independently authenticate the actual trigger that permitted
            # THIS movement before accepting source geometry or MP.
            _attest_g1_step_response_window(ledger, event)
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
        elif kind == "g7g_hunter_pursuit_executed":
            # Independently derive Hunter front-line contact from its
            # replayed anatomical footprint, even for multi-round defeat.
            target = d.get("target")
            hunter = expected.actors["hunter"]
            if (event["turn"] != "hunter"
                    or target not in ROSTER[1:]
                    or d.get("final_footprint") !=
                       [list(cell) for cell in hunter.occupied]
                    or type(d.get("contact")) is not bool
                    or d["contact"] != (
                        grid.front("hunter") == expected.actors[target].occupied[0])
                    or (party_exits and (event["round"] != 2
                                         or target != "vanguard"
                                         or d["contact"] is not True))):
                raise AssertionError(
                    "G7-H Hunter pursuit receipt lost actual head-forward contact")
        elif kind == "g5_melee_roll" and d.get("attacker") == "hunter":
            target = d.get("target")
            if (target not in ROSTER[1:] or event["turn"] != "hunter"
                    or grid.front("hunter") != expected.actors[target].occupied[0]):
                raise AssertionError(
                    "G7-H paid Hunter Bite rolled outside replayed melee contact")
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


def _authored_exit_chains(ledger, terminal, final_state):
    """Validate G7-C exits and bind native G1 replay to closing positions."""
    proven_positions = _replay_native_exit_geometry(ledger)
    # The caller's final_state is an untrusted summary, not a source of
    # geometry. G1 replay reconstructs positions for *every* sourced actor,
    # including Hunter and any player who did not move in the final round.
    if (not isinstance(final_state, dict)
            or set(final_state) != set(ROSTER)
            or any(not isinstance(final_state[actor], dict)
                   or final_state[actor].get("occupied") != proven_positions[actor]
                   for actor in ROSTER)):
        raise AssertionError(
            "Closing source footprints disagree with fully replayed native G1 moves")
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

def _reconcile_victory_all_ab_sequences(ledger):
    """Bind EVERY A/B paid slot to the G6-C policy, including B's R1 miss.

    Native consistency of a declaration, assignment and roll cannot prove
    which *legal* Dodge/Take Hit the authored Hunter originally chose.
    Reconstruct both rounds and the defender's pressured Dodge resource
    from the independent source scene, not a mutable report or roll.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import POLICY, mixed_scene
    from scripts.b06_hunter_party_exchanges_v0 import BUILD

    genesis = ledger[0]["detail"]
    level, seed = genesis["source_ids"]["vanguard"]["level"], genesis["seed"]
    authored = mixed_scene(size=4, level=level, seed=seed)
    hunter = authored.e.actors["hunter"]
    base_dodge = 10 + min(hunter.agility, 4) + hunter.awareness
    guard = hunter.guard_capacity
    actors = (("vanguard", "A", "B06-PC-A-SWORD", "dodge"),
              ("guardian", "B", "B06-PC-B-MACE", "take_hit"))
    paid = [v for v in ledger if v["kind"] == "action_committed"
            and v["detail"].get("actor") in ("vanguard", "guardian")
            and v["detail"].get("label", "").startswith("sequence:")]
    assigned_to_hunter = [v for v in ledger
                          if v["kind"] == "defense_assigned"
                          and v["detail"].get("actor") == "hunter"]
    ab_rolls = [v for v in ledger if v["kind"] == "g5_melee_roll"
                and v["detail"].get("attacker") in ("vanguard", "guardian")]
    ab_results = [v for v in ledger
                  if v["kind"] in ("g5_melee_resolved", "g5_melee_cancelled")
                  and (v["detail"].get("attacker") in ("vanguard", "guardian")
                       or v["detail"].get("action_index") in
                          {action["index"] for action in paid})]
    if (len(paid) != 4 or len(assigned_to_hunter) != 4
            or len(ab_rolls) != 4 or len(ab_results) != 4):
        raise AssertionError("Every authored A/B slot needs one paid roll and resolution")

    seen_actions, checked = set(), []
    for round_no in (1, 2):
        pressure = 0  # G0 begin_round resets Dodge Pressure on Hunter.
        for actor, role, profile, defense_choice in actors:
            face, damage_die = POLICY[round_no][actor]
            action_set = [v for v in paid
                          if v["round"] == round_no and v["turn"] == actor
                          and v["detail"].get("label") == f"sequence:{profile}:0"]
            if len(action_set) != 1:
                raise AssertionError("A/B authored round lacks exact source payment")
            action = action_set[0]
            idx = action["index"]
            if idx in seen_actions:
                raise AssertionError("A/B native action index was reused")
            seen_actions.add(idx)
            expected_value = (base_dodge - pressure
                              if defense_choice == "dodge" else None)
            if defense_choice == "dodge":
                pressure += 2
            seqs = [v for v in ledger if v["kind"] == "g5_melee_sequence_attested"
                    and idx in v["detail"].get("action_indices", ())]
            if len(seqs) != 1:
                raise AssertionError("A/B paid slot has no unique original G5 sequence")
            seq = seqs[0]
            q = seq["detail"]
            declaration_index = q.get("declaration_index")
            defense_indices = q.get("defense_indices")
            if (q.get("attacker") != actor or q.get("target") != "hunter"
                    or q.get("profiles") != [profile]
                    or q.get("action_indices") != [idx]
                    or q.get("source_bonuses") != [BUILD[role]["attack"]]
                    or q.get("source_digest") !=
                       genesis["source_ids"][actor]["digest"]
                    or type(declaration_index) is not int
                    or not idx < declaration_index < seq["index"]
                    or not isinstance(defense_indices, list)
                    or len(defense_indices) != 1
                    or type(defense_indices[0]) is not int
                    or not declaration_index < defense_indices[0] < seq["index"]
                    or seq["round"] != round_no or seq["turn"] != actor):
                raise AssertionError("A/B paid sequence diverges from authored source")
            declaration, defense = ledger[declaration_index], ledger[defense_indices[0]]
            if (declaration["kind"] != "attack_sequence_committed"
                    or declaration["round"] != round_no
                    or declaration["turn"] != actor
                    or declaration["detail"].get("attacker") != actor
                    or declaration["detail"].get("target") != "hunter"
                    or declaration["detail"].get("profiles") != [profile]
                    or declaration["detail"].get("defenses") != [defense_choice]
                    or defense["kind"] != "defense_assigned"
                    or defense["round"] != round_no
                    or defense["turn"] != actor
                    or defense["detail"].get("actor") != "hunter"
                    or defense["detail"].get("attack_key") !=
                       f"{actor}:hunter:0"
                    or defense["detail"].get("defense") != defense_choice
                    or defense["detail"].get("defense_value") != expected_value
                    or defense["detail"].get("dodge_pressure") != pressure
                    or defense["detail"].get("guard_remaining") != guard):
                raise AssertionError("A/B authored Dodge/Take Hit or resource state changed")
            rolls = [v for v in ab_rolls
                     if v["detail"].get("action_index") == idx]
            results = [v for v in ab_results
                       if v["detail"].get("action_index") == idx]
            if len(rolls) != 1 or len(results) != 1:
                raise AssertionError("Every paid A/B melee slot must roll and resolve")
            roll, result = rolls[0], results[0]
            rd, d = roll["detail"], result["detail"]
            if (result["kind"] != "g5_melee_resolved"
                    or not seq["index"] < roll["index"] < result["index"]
                    or roll["round"] != round_no or roll["turn"] != actor
                    or result["round"] != round_no or result["turn"] != actor
                    or rd.get("action_index") != idx
                    or rd.get("declaration_index") != declaration_index
                    or rd.get("slot") != 0
                    or rd.get("attacker") != actor or rd.get("target") != "hunter"
                    or rd.get("profile") != profile
                    or rd.get("declared_defense") != defense_choice
                    or rd.get("defense") != defense_choice
                    or rd.get("defense_value") != expected_value
                    or rd.get("attack_face") != face
                    or rd.get("source_attack_bonus") != BUILD[role]["attack"]
                    or rd.get("prone_modifier") != 0
                    or rd.get("attack_bonus") != BUILD[role]["attack"]
                    or rd.get("attack_total") != face + BUILD[role]["attack"]
                    or rd.get("confirmation_face") is not None
                    or rd.get("critical") != "normal"
                    or rd.get("spontaneous_policy") != "decline_all"
                    or d.get("attacker") != actor or d.get("target") != "hunter"
                    or d.get("profile") != profile
                    or d.get("critical") != "normal"):
                raise AssertionError("A/B authored melee roll or native result altered")
            opening, ready = _attest_unopposed_response_window(
                ledger, trigger=f"g5:melee:{idx}", actor=actor,
                round_no=round_no, before_index=seq["index"],
                after_index=roll["index"])
            if (ready["index"] != roll["index"] - 1
                    or ready["index"] != opening["index"] + 3):
                raise AssertionError("A/B paid roll lacks contiguous legal G0 response chain")
            hit = (face != 1 and (defense_choice == "take_hit"
                   or face == 20 or face + BUILD[role]["attack"] > expected_value))
            if (rd.get("hit") is not hit
                    or d.get("outcome") != ("hit" if hit else "miss")
                    or (not hit and d.get("damage") is not None)
                    or (not hit and any(
                        v["kind"] == "g45_attested_hit"
                        and v["detail"].get("action_index") == idx for v in ledger))):
                raise AssertionError("A/B authored miss/hit must match source roll")
            checked.append((actor, round_no, hit))
        if pressure != 2:
            raise AssertionError("Authored Vanguard Dodge must commit Hunter pressure")
    if (len(seen_actions) != 4
            or [v["detail"]["attack_key"] for v in assigned_to_hunter] !=
               [f"{actor}:hunter:0" for _ in (1, 2) for actor in
                ("vanguard", "guardian")]
            or checked != [("vanguard", 1, True), ("guardian", 1, False),
                           ("vanguard", 2, True), ("guardian", 2, True)]):
        raise AssertionError("Victory lacks exact four source A/B outcomes")
    return checked


def _player_melee_hit_chains(ledger, actor, profile):
    """Prove G6-B A/B participation from real paid G0 -> G5 -> G4 -> G4.5.

    A G5 resolved summary is insufficient: source G0 declaration/defense,
    G5 hit-producing roll, G4 damage and G4.5 verified receipt must share
    the original physical action index and actual own-turn chronology.
    """
    from scripts.b06_hunter_party_exchanges_v0 import BUILD
    from scripts.b06_hunter_mixed_party_g6c_v0 import POLICY, mixed_scene

    role = {"vanguard": "A", "guardian": "B"}.get(actor)
    expected_profile = {"A": "B06-PC-A-SWORD", "B": "B06-PC-B-MACE"}.get(role)
    if role is None or profile != expected_profile:
        raise AssertionError("Only the exact sourced A/B profile may certify melee")
    seed = ledger[0]["detail"].get("seed")
    sources = ledger[0]["detail"].get("source_ids", {})
    attacker_source = sources.get(actor, {})
    hunter_source = sources.get("hunter", {})
    bonus = BUILD[role]["attack"]
    if (attacker_source.get("source_id") != role
            or hunter_source.get("source_id") != "B06-EN-03"
            or type(seed) is not int):
        raise AssertionError("A/B melee needs original source fixture identities")
    candidates = [v for v in ledger if v["kind"] == "g5_melee_resolved"
                  and v["detail"].get("attacker") == actor
                  and v["detail"].get("target") == "hunter"
                  and v["detail"].get("profile") == profile
                  and v["detail"].get("outcome") == "hit"]
    if not candidates:
        raise AssertionError("A/B martial contribution needs a genuine hit")
    # Native G4 is the sole packet/mitigation authority. Load the original
    # source fixtures and derive each authored dice roll through G4 rather
    # than trusting G4 event raw/mitigated fields or a cached HP delta.
    authored = mixed_scene(
        size=4, level=sources["vanguard"]["level"], seed=seed)
    g4 = authored.e.g4
    hunter = authored.e.actors["hunter"]
    proven = []
    used_actions = set()
    for resolved in candidates:
        d = resolved["detail"]
        index = d.get("action_index")
        if (type(index) is not int or not 0 <= index < resolved["index"]
                or index in used_actions):
            raise AssertionError("A/B source hit has missing/reused paid action")
        used_actions.add(index)
        action = ledger[index]
        if (action["kind"] != "action_committed"
                or action["turn"] != actor
                or action["round"] != resolved["round"]
                or resolved["turn"] != actor
                or action["detail"].get("actor") != actor
                or action["detail"].get("action_class") != "physical"
                or action["detail"].get("label") != f"sequence:{profile}:0"
                or type(action["detail"].get("ap_spent")) is not int
                or action["detail"]["ap_spent"] != 20
                or any(x["kind"] == "g5_melee_cancelled"
                       and x["detail"].get("action_index") == index
                       for x in ledger)):
            raise AssertionError("A/B hit did not consume its legal physical action")
        # A genuine action index and a 20-AP debit are insufficient:
        # reconstruct the actor's SOURCE-sized own-turn allowance and
        # every preceding paid action, including the claimed remainder.
        _paid_action_ap(
            ledger, action, actor=actor, cost=20, kind="physical",
            label=f"sequence:{profile}:0")
        attestations = [v for v in ledger
                        if v["kind"] == "g5_melee_sequence_attested"
                        and index in v["detail"].get("action_indices", ())]
        if len(attestations) != 1:
            raise AssertionError("A/B hit requires one authoritative G5 sequence")
        seq = attestations[0]
        q = seq["detail"]
        dec_index = q.get("declaration_index")
        defense_indices = q.get("defense_indices")
        if (q.get("attacker") != actor or q.get("target") != "hunter"
                or q.get("profiles") != [profile]
                or q.get("action_indices") != [index]
                or q.get("source_bonuses") != [bonus]
                or q.get("source_digest") != attacker_source.get("digest")
                or type(dec_index) is not int
                or not index < dec_index < seq["index"] < resolved["index"]
                or not isinstance(defense_indices, list)
                or len(defense_indices) != 1
                or type(defense_indices[0]) is not int
                or not dec_index < defense_indices[0] < seq["index"]
                or seq["round"] != resolved["round"] or seq["turn"] != actor):
            raise AssertionError("A/B G5 sequence not bound to native payment/declaration")
        declaration = ledger[dec_index]
        defense = ledger[defense_indices[0]]
        if (declaration["kind"] != "attack_sequence_committed"
                or declaration["round"] != resolved["round"]
                or declaration["turn"] != actor
                or declaration["detail"].get("attacker") != actor
                or declaration["detail"].get("target") != "hunter"
                or declaration["detail"].get("profiles") != [profile]
                or defense["kind"] != "defense_assigned"
                or defense["round"] != resolved["round"]
                or defense["turn"] != actor
                or defense["detail"].get("actor") != "hunter"
                or defense["detail"].get("attack_key") !=
                   f"{actor}:hunter:0"
                or defense["detail"].get("defense") not in ("take_hit", "dodge")
                or declaration["detail"].get("defenses") !=
                   [defense["detail"]["defense"]]):
            raise AssertionError("A/B original G0 target, profile or defense altered")
        rolls = [v for v in ledger if v["kind"] == "g5_melee_roll"
                 and v["detail"].get("action_index") == index]
        bridges = [v for v in ledger if v["kind"] == "g45_attested_hit"
                   and v["detail"].get("action_index") == index]
        if len(rolls) != 1 or len(bridges) != 1:
            raise AssertionError("A/B paid hit must have exactly one roll and G4.5 receipt")
        roll, bridge = rolls[0], bridges[0]
        rd, bd = roll["detail"], bridge["detail"]
        if (not seq["index"] < roll["index"] < bridge["index"] < resolved["index"]
                or any(v["round"] != resolved["round"] or v["turn"] != actor
                       for v in (roll, bridge))
                or any(v["detail"].get("attacker") != actor
                       or v["detail"].get("target") != "hunter"
                       or v["detail"].get("profile") != profile
                       for v in (roll, bridge))
                or rd.get("declaration_index") != dec_index
                or rd.get("slot") != 0
                or rd.get("declared_defense") != defense["detail"]["defense"]
                or rd.get("hit") is not True
                or rd.get("spontaneous_policy") != "decline_all"
                or bd.get("sequence_declaration_index") != dec_index
                or bd.get("declared_profile_index") != 0
                or bd.get("source_event") != f"g5:source:{seed}:{index}"
                or bd.get("contact_reference") != f"g5:melee:{index}"
                or bd.get("defense_reference") !=
                   f"g0:defense:{defense_indices[0]}"
                or bd.get("attacker_source") != attacker_source.get("digest")
                or bd.get("target_source") != hunter_source.get("digest")
                or not isinstance(bd.get("actual_result"), dict)
                or bd["actual_result"] != d.get("damage")):
            raise AssertionError("A/B G5 roll and G4.5 receipt do not bind the same hit")
        # A genuine G5 roll may exist only after G0's original response
        # window has passed BOTH legality rechecks and emitted its unique
        # ready receipt. A rehashed G4/G4.5 hit cannot turn a canceled
        # Vanguard/Guardian trigger into a legal melee contribution.
        opening, ready = _attest_unopposed_response_window(
            ledger, trigger=f"g5:melee:{index}", actor=actor,
            round_no=resolved["round"], before_index=seq["index"],
            after_index=roll["index"])
        # G5's sourced decline-all policy has no intervening interception,
        # spontaneous or nested response events: the native G0 rechecks
        # occur back-to-back, and G5 rolls immediately after ready.
        if (ready["index"] != roll["index"] - 1
                or tuple(x["index"] for x in (
                    opening,
                    ledger[opening["index"] + 1],
                    ledger[opening["index"] + 2],
                    ready)) != tuple(range(opening["index"], ready["index"] + 1))
                or ready["index"] != opening["index"] + 3):
            raise AssertionError(
                "A/B hit lacks contiguous legal G0 response-window ready chain")
        face = rd.get("attack_face")
        value = rd.get("defense_value")
        chosen = rd.get("defense")
        assigned = defense["detail"]["defense"]
        if (type(face) is not int or not 1 <= face <= 20 or face == 1
                or type(rd.get("source_attack_bonus")) is not int
                or rd["source_attack_bonus"] != bonus
                or type(rd.get("prone_modifier")) is not int
                or rd["prone_modifier"] != 0
                or type(rd.get("attack_bonus")) is not int
                or rd["attack_bonus"] != bonus
                or type(rd.get("attack_total")) is not int
                or rd["attack_total"] != face + bonus
                or chosen not in ("take_hit", "dodge")
                or (chosen == assigned and value !=
                    defense["detail"].get("defense_value"))
                or (chosen != assigned and (
                    chosen != "take_hit"
                    or not any(v["kind"] == "g5_defense_unavailable_fallback"
                               and v["detail"].get("attacker") == actor
                               and v["detail"].get("target") == "hunter"
                               and v["detail"].get("action_index") == index
                               and v["detail"].get("declared") == assigned
                               and v["detail"].get("resolved") == "take_hit"
                               and dec_index < v["index"] < roll["index"]
                               for v in ledger)))
                or (chosen == "take_hit" and value is not None)
                or (chosen == "dodge"
                    and (type(value) is not int
                         or (face != 20 and face + bonus <= value)))):
            raise AssertionError("A/B recorded d20 cannot produce its claimed melee hit")
        confirm = rd.get("confirmation_face")
        if face == 20:
            if type(confirm) is not int or not 1 <= confirm <= 20:
                raise AssertionError("A/B natural-20 needs source confirmation")
            critical = ("devastating" if confirm == 20
                        else "critical" if chosen == "take_hit"
                        or (confirm != 1 and confirm + bonus > value)
                        else "strong")
        else:
            if confirm is not None:
                raise AssertionError("Ordinary A/B hit cannot have confirmation")
            critical = "normal"
        if (rd.get("critical") != critical or d.get("critical") != critical
                or bd.get("critical") != critical):
            raise AssertionError("A/B critical tier cannot be relabeled")
        # G7-H certifies only G6-C's fixed two-round physical witness,
        # never an unsourced damage d6 inferred from the reported HP loss.
        faces = POLICY.get(resolved["round"], {}).get(actor)
        if (not isinstance(faces, tuple) or len(faces) != 2
                or face != faces[0]
                or type(faces[1]) is not int or critical != "normal"):
            raise AssertionError("A/B authored melee face or damage die is invalid")
        _, profile_packet, packets = g4._profile_hit_packets(
            actor, "hunter", profile, die_face=faces[1],
            critical=critical, critical_dice=())
        if (len(packets) != 1 or packets[0].resource != "hp"
                or packets[0].armor_rule != "weapon"
                or packets[0].damage_type !=
                   profile_packet["damage_type"]):
            raise AssertionError("A/B fixture must produce one source weapon packet")
        source_raw = packets[0].raw
        source_mitigated = g4._mitigate_hp(hunter, packets[0])
        damage_events = [v for v in ledger
                         if v["kind"] == "g4_damage_applied"
                         and roll["index"] < v["index"] < bridge["index"]
                         and v["detail"].get("recipient") == "hunter"
                         and v["detail"].get("cause") ==
                             f"source-profile:{profile}"]
        source_events = [v for v in ledger
                         if v["kind"] == "g4_profile_hit"
                         and roll["index"] < v["index"] < bridge["index"]
                         and v["detail"].get("attacker") == actor
                         and v["detail"].get("target") == "hunter"
                         and v["detail"].get("profile") == profile]
        if len(damage_events) != 1 or len(source_events) != 1:
            raise AssertionError("A/B hit requires one actual native G4 source damage")
        dmg = damage_events[0]
        actual = bd["actual_result"]
        if (dmg["round"] != resolved["round"] or dmg["turn"] != actor
                or source_events[0]["round"] != resolved["round"]
                or source_events[0]["turn"] != actor
                or source_events[0]["detail"].get("critical") != critical
                or not dmg["index"] < source_events[0]["index"] < bridge["index"]
                or actual.get("hp_loss") != (
                    dmg["detail"].get("hp_before") -
                    dmg["detail"].get("hp_after"))
                or actual.get("dead") is not dmg["detail"].get("dead")
                or actual.get("vigor_loss") != 0
                or actual.get("hp_packets") != [source_mitigated]
                or actual.get("injection_eligible") is not False):
            raise AssertionError("A/B paid G4 damage not in attested hit chain")
        _hp_damage_packet(
            ledger, dmg, target="hunter", raw=source_raw,
            mitigated=source_mitigated, cause=f"source-profile:{profile}",
            damage_type=packets[0].damage_type, armor_rule="weapon")
        proven.append({"action": index, "roll": roll["index"],
                       "damage": dmg["index"], "bridge": bridge["index"],
                       "resolved": resolved["index"]})
    return proven


def _flame_hit_from_defense(flame):
    """Re-derive the certified F direct hit from the native d20 and defense.

    This fixed G6-C scene has a clear Take Hit lane (G2 base/final 10).
    A launch's editable hit-outcome string cannot turn an actual miss into
    G4 Fire, including natural-1 auto misses and unresolved natural-20s.
    """
    d = flame["detail"]
    face, base, defense = (d.get("primary_face"),
                           d.get("base_defense"), d.get("final_defense"))
    total = d.get("attack_total")
    if (type(face) is not int or not 1 <= face <= 20
            or type(base) is not int or type(defense) is not int
            or base != 10 or defense != 10
            or type(total) is not int or total != face + 5
            or face == 1
            or d.get("outcome") != "direct_hit_pending_G4"):
        raise AssertionError("G7-H Flame lacks native clear-lane d20/defense proof")
    if face == 20:
        confirm = d.get("confirmation_face")
        if type(confirm) is not int or not 1 <= confirm <= 20:
            raise AssertionError("G7-H Flame natural-20 needs resolved confirmation")
        tier = "devastating" if confirm == 20 else "critical"
    else:
        if d.get("confirmation_face") is not None or total <= defense:
            raise AssertionError("G7-H Flame cannot deliver Fire after a source miss")
        tier = "normal"
    dice = d.get("critical_dice", [])
    required = {"normal": 0, "strong": 1,
                "critical": 2, "devastating": 2}[tier]
    if (d.get("critical", "normal") != tier
            or not isinstance(dice, list) or len(dice) != required
            or any(type(v) is not int or not 1 <= v <= 4 for v in dice)
            or type(d.get("die")) is not int or not 1 <= d["die"] <= 8):
        raise AssertionError("G7-H Flame critical or damage faces mismatch")
    # This certificate is a *fixed* G6-C scene. Re-derive the exact
    # independently preauthored Scholar input pair by its original round,
    # not from an editable launch/attack-total pair. An otherwise legal
    # substituted hit is a different policy and must not certify.
    from scripts.b06_hunter_mixed_party_g6c_v0 import POLICY
    authored = POLICY.get(flame["round"], {}).get("scholar")
    if (flame["round"] not in (1, 2)
            or flame["turn"] != "scholar"
            or authored is None
            or (face, d.get("die")) != tuple(authored)):
        raise AssertionError("G7-H Flame diverged from fixed G6-C Scholar roll")
    from math import ceil
    if d.get("packets_pending_g4") != {
            "fire_hp": 2 + sum(dice), "vigor": 2 + ceil(d["die"] / 3)}:
        raise AssertionError("G7-H Flame damage packets not derived from native cast")



def _flame_delivery_packet(ledger, flame):
    """Bind source Thrown Flame's Fire and Direct Vigor to its one native G4."""
    d = flame["detail"]
    pending = d.get("packets_pending_g4")
    if not isinstance(pending, dict) or set(pending) != {"fire_hp", "vigor"}:
        raise AssertionError("Source Flame must declare two typed G3 packets")
    hp_raw, vigor_raw = pending["fire_hp"], pending["vigor"]
    key = f"g3-flame-ledger:{flame['index']}"
    hits = [x for x in ledger
            if x["kind"] == "g4_damage_applied"
            and x["detail"].get("event_key") == key]
    if len(hits) != 1:
        raise AssertionError("One Thrown Flame must have exactly one G4 delivery")
    hit = hits[0]
    record = hit["detail"]
    expected = [
        {"resource": "hp", "type": "Fire", "raw": hp_raw,
         "mitigated": hp_raw, "armor_rule": "none"},
        {"resource": "vigor", "type": "Direct Vigor", "raw": vigor_raw,
         "mitigated": vigor_raw, "armor_rule": "none"},
    ]
    if (hit["index"] <= flame["index"]
            or hit["round"] != flame["round"]
            or hit["turn"] != "scholar"
            or record.get("recipient") != "hunter"
            or record.get("cause") != "g3:thrown_flame"
            or record.get("packets") != expected
            or type(record.get("hp_before")) is not int
            or type(record.get("hp_after")) is not int
            or record["hp_after"] != max(
                -ledger[0]["detail"]["source_ids"]["hunter"]["hp"],
                record["hp_before"] - hp_raw)
            or type(record.get("vigor_before")) is not int
            or type(record.get("vigor_after")) is not int
            or record["vigor_before"] < vigor_raw
            or record["vigor_after"] != record["vigor_before"] - vigor_raw
            or record.get("vigor_details") != [
                {"raw": vigor_raw, "available": vigor_raw,
                 "prevented": 0, "applied": vigor_raw}]):
        raise AssertionError("Flame G4 packet/cause/HP/Vigor do not match source dice")
    # No later action or turn transition can intervene before a synchronous
    # native G3 -> G4 Fire launch; only G4's wound bookkeeping may precede it.
    if any(v["kind"] in ("turn_end", "turn_start_expiry",
                          "action_committed", "g3_flame_launched")
           for v in ledger[flame["index"]+1:hit["index"]]):
        raise AssertionError("Flame damage was not synchronous with its original G3")
    return hit



def _reconcile_victory_hunter_sequences(ledger):
    """Audit BOTH G6-C Hunter actions, including the Round-1 natural-1 miss.

    A source-native sequence still costs 24 AP when its attack misses;
    hit-only G4/G4.5 traversals cannot vouch for that G0 payment.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import POLICY

    label = "sequence:B06-AT-04:0"
    payments = [v for v in ledger
                if v["kind"] == "action_committed"
                and v["detail"].get("actor") == "hunter"
                and v["detail"].get("label") == label]
    sequences = [v for v in ledger if
                 v["kind"] == "g5_melee_sequence_attested"
                 and v["detail"].get("attacker") == "hunter"]
    resolved = [v for v in ledger if
                v["kind"] == "g5_melee_resolved"
                and v["detail"].get("attacker") == "hunter"]
    rolls = [v for v in ledger if v["kind"] == "g5_melee_roll"
             and v["detail"].get("attacker") == "hunter"]
    if (len(payments) != 2 or len(sequences) != 2
            or len(resolved) != 2 or len(rolls) != 2
            or {v["round"] for v in payments} != {1, 2}):
        raise AssertionError("Victory requires both original paid Hunter Bite sequences")
    for action in payments:
        round_no = action["round"]
        face, damage_face, _ = POLICY[round_no]["hunter"]
        _paid_action_ap(ledger, action, actor="hunter", cost=24,
                        kind="physical", label=label)
        matches = [v for v in sequences if
                   v["round"] == round_no
                   and v["turn"] == "hunter"
                   and v["detail"].get("action_indices") == [action["index"]]
                   and v["detail"].get("profiles") == ["B06-AT-04"]
                   and v["detail"].get("attacker") == "hunter"
                   and v["detail"].get("target") == "vanguard"]
        if len(matches) != 1:
            raise AssertionError("Hunter Bite payment lacks its original G5 sequence")
        seq = matches[0]
        declaration_index = seq["detail"].get("declaration_index")
        defense_indices = seq["detail"].get("defense_indices")
        if (type(declaration_index) is not int
                or not action["index"] < declaration_index < seq["index"]
                or not isinstance(defense_indices, list)
                or len(defense_indices) != 1
                or type(defense_indices[0]) is not int
                or not declaration_index < defense_indices[0] < seq["index"]):
            raise AssertionError("Paid Hunter sequence has no actual source declaration")
        declared = ledger[declaration_index]
        defense = ledger[defense_indices[0]]
        expected_defense = "guard" if round_no == 1 else "take_hit"
        if (declared["kind"] != "attack_sequence_committed"
                or declared["round"] != round_no
                or declared["turn"] != "hunter"
                or declared["detail"].get("attacker") != "hunter"
                or declared["detail"].get("target") != "vanguard"
                or declared["detail"].get("profiles") != ["B06-AT-04"]
                or declared["detail"].get("defenses") != [expected_defense]
                or defense["kind"] != "defense_assigned"
                or defense["round"] != round_no
                or defense["turn"] != "hunter"
                or defense["detail"].get("actor") != "vanguard"
                or defense["detail"].get("attack_key") !=
                   "hunter:vanguard:0"
                or defense["detail"].get("defense") != expected_defense):
            raise AssertionError("Victory Hunter declaration/defense was replaced")
        hits = [v for v in resolved if
                v["detail"].get("action_index") == action["index"]]
        faces = [v for v in rolls if
                 v["detail"].get("action_index") == action["index"]]
        if len(hits) != 1 or len(faces) != 1:
            raise AssertionError("Each paid Hunter action needs one source G5 roll/result")
        result, roll = hits[0], faces[0]
        _attest_bite_response_window(
            ledger, action_index=action["index"],
            attested_index=seq["index"], roll=roll)
        expected_hit = round_no == 2
        if (not seq["index"] < roll["index"] < result["index"]
                or any(v["round"] != round_no or v["turn"] != "hunter"
                       for v in (roll, result))
                or roll["detail"].get("declaration_index") != declaration_index
                or roll["detail"].get("slot") != 0
                or roll["detail"].get("attacker") != "hunter"
                or roll["detail"].get("target") != "vanguard"
                or roll["detail"].get("profile") != "B06-AT-04"
                or roll["detail"].get("attack_face") != face
                or roll["detail"].get("source_attack_bonus") != 6
                or roll["detail"].get("prone_modifier") != 0
                or roll["detail"].get("attack_bonus") != 6
                or roll["detail"].get("attack_total") != face + 6
                or roll["detail"].get("hit") is not expected_hit
                or roll["detail"].get("critical") != "normal"
                or roll["detail"].get("confirmation_face") is not None
                or roll["detail"].get("declared_defense") != expected_defense
                or roll["detail"].get("defense") != expected_defense
                or result["detail"].get("attacker") != "hunter"
                or result["detail"].get("target") != "vanguard"
                or result["detail"].get("profile") != "B06-AT-04"
                or result["detail"].get("outcome") !=
                   ("hit" if expected_hit else "miss")
                or result["detail"].get("critical") != "normal"):
            raise AssertionError("Hunter source-authored miss/hit not paid and resolved")
        if not expected_hit:
            if (damage_face is not None
                    or result["detail"].get("damage") is not None
                    or any(v["kind"] == "g45_attested_hit"
                           and v["detail"].get("action_index") == action["index"]
                           for v in ledger)):
                raise AssertionError("Round-1 Hunter miss cannot create G4/G4.5 hit")
        elif damage_face is None:
            raise AssertionError("Round-2 source Bite requires genuine damage")
    return True


def _authored_wound_basis(ledger, damage, *, policy):
    """Recover wound inputs from the source's *independently verified* attack.

    A G4 wound_created event is an OUTPUT, never the source of its own
    severity, location, trauma, or identifier. Every damage cause in these
    three fixed-policy scenes must have a known, authenticated native origin.
    The original wound-location d20 is not serialized in G5's roll receipt;
    use the immutable G6-C/G7-G authored input, not a replacement d20 from
    the mutable wound record.
    """
    d = damage["detail"]
    cause, actor, key = (
        d.get("cause"), d.get("recipient"), d.get("event_key"))
    if cause == "source-profile:B06-AT-04":
        hits = [h for h in _hunter_bite_hits(ledger, actor, policy=policy)
                if h["damage"]["index"] == damage["index"]]
        if len(hits) != 1:
            raise AssertionError("Wound must trace to an authenticated Hunter Bite")
        tier = hits[0]["roll"]["detail"]["critical"]
        # G7-G commits d20=8 for every wound-qualifying Hunter Bite.
        # G6-C's single landed Bite does not supply a wound d20, and
        # cannot legitimately generate a wound in the original scene.
        location_roll = (8 if policy != "mixed_victory_rite" else None)
        expected_key = (
            f"g4:profile:hunter:{actor}:B06-AT-04:"
            f"{damage['index'] - 1}" if d.get("wound") is not None else None)
        trauma = "Piercing"
    elif cause == "g3:thrown_flame":
        flames = [ev for ev in ledger if ev["kind"] == "g3_flame_launched"
                  and f"g3-flame-ledger:{ev['index']}" == key]
        if len(flames) != 1 or _flame_delivery_packet(
                ledger, flames[0])["index"] != damage["index"]:
            raise AssertionError("Wound must trace to the native G3/G4 Flame packet")
        _flame_hit_from_defense(flames[0])
        tier = flames[0]["detail"].get("critical", "normal")
        location_roll = 8 if flames[0]["round"] == 2 else None
        expected_key = f"g3-flame-ledger:{flames[0]['index']}"
        trauma = "Fire"
    elif cause in ("source-profile:B06-PC-A-SWORD",
                   "source-profile:B06-PC-B-MACE"):
        attacker, profile = (
            ("vanguard", "B06-PC-A-SWORD")
            if cause.endswith("B06-PC-A-SWORD")
            else ("guardian", "B06-PC-B-MACE"))
        rolls = [ev for ev in ledger if ev["kind"] == "g5_melee_roll"
                 and ev["detail"].get("attacker") == attacker
                 and ev["detail"].get("target") == "hunter"
                 and ev["detail"].get("profile") == profile
                 and ev["detail"].get("hit") is True
                 and ev["index"] < damage["index"]]
        bridges = [ev for ev in ledger if ev["kind"] == "g45_attested_hit"
                   and ev["detail"].get("attacker") == attacker
                   and ev["detail"].get("target") == "hunter"
                   and damage["index"] < ev["index"]]
        pairs = [(roll, bridge) for roll in rolls for bridge in bridges
                 if roll["detail"].get("action_index") ==
                    bridge["detail"].get("action_index")
                 and roll["index"] < damage["index"] < bridge["index"]]
        if len(pairs) != 1:
            raise AssertionError("G4 melee wound lacks unique native A/B paid hit")
        tier = pairs[0][0]["detail"]["critical"]
        location_roll = None   # G6-C A/B rolls supply no wound d20
        expected_key = None
        trauma = "Cut" if attacker == "vanguard" else "Crush"
    elif isinstance(cause, str) and cause.startswith("g6d:source_bow:"):
        if policy != "mixed_victory_rite":
            raise AssertionError("Only mixed victory uses source R Bow damage")
        # G6-D's 20/20 finishing shot hits the existing Dying Hunter's
        # *lethal* threshold; no G4 wound can be minted after death.
        terminal_bows = [ev for ev in ledger
                         if ev["kind"] == "g6d_bow_adjudicated"
                         and (ev["detail"].get("damage") or {}).get("dead") is True]
        if (len(terminal_bows) != 1
                or terminal_bows[0]["detail"].get("damage", {}).get("wound") is not None):
            raise AssertionError("Source Bow fatal packet is not the authored finishing hit")
        tier = "devastating"
        location_roll = None
        expected_key = None
        trauma = "Piercing"
    else:
        raise AssertionError("Unrecognized damage source cannot certify G7-H wound history")
    if tier not in ("normal", "strong", "critical", "devastating"):
        raise AssertionError("Unsupported critical tier in native wound basis")
    # The first positive, typed HP packet determines G4 wound trauma.
    packets = d.get("packets")
    if (not isinstance(packets, list)
            or not any(p.get("resource") == "hp"
                       and p.get("mitigated", 0) > 0
                       and p.get("type") == trauma for p in packets)):
        raise AssertionError("G4 trauma does not follow the authenticated attack type")
    return {"devastating": tier == "devastating",
            "location_roll": location_roll, "trauma": trauma,
            "event_key": expected_key}



def _reconcile_every_g45_target_snapshot(ledger, *, policy, level, seed):
    """Replay each G4.5 target's COMPLETE *immediate post-hit* actor state.

    A G4.5 target_state is not an authority about death, VP, wounds or
    Vigor: reconstruct it from a fresh source fixture and earlier G0/G3/G4
    transactions. Global HP/regeneration/VP/wound checks elsewhere audit
    those transitions against real costs and wound dice. Compare all G4.5
    fields (including wound source identity), not only actual_result.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
    from scripts.b06_wound_continuation_v0 import _actor_state

    source = mixed_scene(
        size=4, level=level, seed=seed,
        party_exits=(policy == "opposed_living_hunter_withdrawal")).e
    state = {actor: _actor_state(source.actors[actor]) for actor in ROSTER}
    bridges = 0
    for event in ledger:
        kind, d = event["kind"], event["detail"]
        if kind == "g4_wound_created":
            actor = d.get("recipient")
            if actor not in state:
                raise AssertionError("Wound recipient is not in original source scene")
            requirement = d.get("requirement")
            if type(requirement) is not int or requirement < 1:
                raise AssertionError("G4 wound must have a genuine repair requirement")
            state[actor]["wounds"].append({
                "id": d.get("wound"), "source_event": d.get("event_key"),
                "severity": d.get("severity"), "location": d.get("location"),
                "trauma": d.get("trauma"), "requirement": requirement,
                "progress": 0, "repairable": True, "completed": False,
            })
        elif kind in ("g4_damage_applied", "regeneration_step"):
            actor = (d.get("recipient") if kind == "g4_damage_applied"
                     else d.get("actor"))
            if actor not in state:
                raise AssertionError("G4 HP/Vigor transition has foreign actor")
            current = state[actor]
            if (d.get("hp_before") != current["hp"]
                    or d.get("vigor_before") != current["vigor"]
                    or type(d.get("hp_after")) is not int
                    or type(d.get("vigor_after")) is not int):
                raise AssertionError("G4.5 source prefix HP/Vigor is not chronological")
            current["hp"], current["vigor"] = d["hp_after"], d["vigor_after"]
            current["dead"] = current["hp"] <= -current["hp_max"]
            current["dying"] = current["hp"] <= 0 and not current["dead"]
        elif kind == "vp_transition":
            actor, points, mode = (
                d.get("actor"), d.get("points"), d.get("mode"))
            if actor not in state or type(points) is not int or points <= 0:
                raise AssertionError("G4.5 source prefix has invalid VP debit")
            if mode not in ("committed", "spent"):
                raise AssertionError("G4.5 source prefix has unknown VP mode")
            current = state[actor]
            current["vp_available"] -= points
            current["vp_committed" if mode == "committed" else "vp_spent"] += points
        elif kind == "vp_release":
            actor, points = d.get("actor"), d.get("points")
            if actor not in state or type(points) is not int or points <= 0:
                raise AssertionError("G4.5 source prefix has invalid VP release")
            current = state[actor]
            current["vp_available"] += points
            current["vp_committed"] -= points
        elif kind == "g45_attested_hit":
            actor, target = d.get("attacker"), d.get("target")
            idx = d.get("action_index")
            if (actor not in state or target not in state
                    or actor == target or type(idx) is not int
                    or not 0 <= idx < event["index"]):
                raise AssertionError("G4.5 receipt has foreign source/paid action")
            sequences = [v for v in ledger[:event["index"]]
                         if v["kind"] == "g5_melee_sequence_attested"
                         and idx in v["detail"].get("action_indices", ())]
            if len(sequences) != 1:
                raise AssertionError("G4.5 receipt cannot borrow a different G5 sequence")
            sequence = sequences[0]["detail"]
            slot = sequence["action_indices"].index(idx)
            indices = sequence.get("defense_indices")
            if (not isinstance(indices, list) or slot >= len(indices)
                    or type(indices[slot]) is not int
                    or not 0 <= indices[slot] < event["index"]
                    or sequence.get("attacker") != actor
                    or sequence.get("target") != target
                    or d.get("source_event") != f"g5:source:{seed}:{idx}"
                    or d.get("contact_reference") != f"g5:melee:{idx}"
                    or d.get("defense_reference") != f"g0:defense:{indices[slot]}"
                    or d.get("sequence_declaration_index") !=
                       sequence.get("declaration_index")
                    or d.get("declared_profile_index") != slot
                    or d.get("attacker_source") !=
                       source.actors[actor].source.digest
                    or d.get("target_source") !=
                       source.actors[target].source.digest
                    or d.get("target_state") != state[target]):
                raise AssertionError(
                    "G4.5 complete target snapshot or bridge source provenance "
                    "contradicts native G4 state at the hit")
            bridges += 1
    if bridges < 1:
        raise AssertionError("No native G4.5 physical hit certified")
    return bridges


def _reconcile_complete_snapshots(ledger, initial, final, *,
                                  policy, level, seed):
    """Reconstruct every serialized actor field from fixture and native events.

    No voluntary wound repair/Basic Heal is authored in these three packs.
    G4 wound creation and source Step-2 receipts therefore determine the
    complete carried wound list, in native chronological order.
    """
    from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
    from scripts.b06_g7a_native_terminal_census_v0 import _snapshot
    from scripts.b06_damage_v0 import WOUND_BANDS, LOCATIONS
    from math import ceil

    reference = mixed_scene(
        size=4, level=level, seed=seed,
        party_exits=(policy == "opposed_living_hunter_withdrawal")).e
    source_initial = _snapshot(reference)
    if initial != source_initial:
        raise AssertionError("Initial actor snapshot differs from exact G6-C source fixture")
    if (set(final) != set(ROSTER)
            or any(not isinstance(final[actor], dict)
                   or set(final[actor]) != set(source_initial[actor])
                   for actor in ROSTER)):
        raise AssertionError("Final actor snapshot has missing/extra source fields")

    wounds = {actor: deepcopy(source_initial[actor]["wounds"]) for actor in ROSTER}
    created = [ev for ev in ledger if ev["kind"] == "g4_wound_created"]
    damages = [ev for ev in ledger if ev["kind"] == "g4_damage_applied"]
    # DamageState uses a *global* next_wound sequence, not an actor-local
    # sequence or a freely chosen identifier from the event being checked.
    carried = [w["id"] for actor in ROSTER
               for w in source_initial[actor]["wounds"]]
    next_wound = max((int(name[4:]) for name in carried
                      if isinstance(name, str) and name.startswith("G4-W")
                      and name[4:].isdigit()), default=0)
    used = set(carried)
    used_keys = set()
    expected_created = []
    # Iterate the *actual ordered G4 damage history*, computing necessity
    # and severity without taking a declared wound or summary as authority.
    for damage in damages:
        record = damage["detail"]
        actor, key = record.get("recipient"), record.get("event_key")
        if (actor not in wounds or not isinstance(key, str) or not key
                or key in used_keys):
            raise AssertionError("G4 damage needs unique source event identity")
        used_keys.add(key)
        source = _authored_wound_basis(ledger, damage, policy=policy)
        hp_max = source_initial[actor]["hp_max"]
        before, after = record.get("hp_before"), record.get("hp_after")
        if (type(before) is not int or type(after) is not int
                or type(hp_max) is not int or hp_max <= 0):
            raise AssertionError("Wound severity needs native integer G4 HP")
        crosses = before > 0 and after <= 0
        needed = (crosses or source["devastating"]) and after > -hp_max
        matched = [ev for ev in created
                   if ev["detail"].get("recipient") == actor
                   and ev["detail"].get("event_key") == key]
        if needed:
            roll = source["location_roll"]
            if type(roll) is not int or not 1 <= roll <= 20:
                raise AssertionError("Source never supplied an authentic wound d20")
            if len(matched) != 1 or matched[0]["index"] >= damage["index"]:
                raise AssertionError("Missing/duplicated native wound before damage")
            wound = matched[0]
            # G4 establishes its event_key from the pre-creation ledger index
            # for a physical profile. The original F Flame source key is
            # independently fixed by its G3 launch index.
            if source["event_key"] is not None and (
                    key != source["event_key"]
                    if record["cause"] == "g3:thrown_flame" else
                    key != f"g4:profile:hunter:{actor}:B06-AT-04:{wound['index']}"):
                raise AssertionError("Wound event key not bound to source delivery")
            overkill = max(0, -after)
            if overkill < ceil(hp_max / 3):
                severity = "Serious"
            elif overkill < ceil(2 * hp_max / 3):
                severity = "Severe"
            else:
                severity = "Critical"
            if source["devastating"]:
                severity = "Critical"
            next_wound += 1
            name = f"G4-W{next_wound:04d}"
            if name in used:
                raise AssertionError("Global G4 wound ID reused")
            used.add(name)
            location = next(label for bound, label in LOCATIONS if roll <= bound)
            expected_detail = {
                "recipient": actor, "wound": name, "severity": severity,
                "requirement": WOUND_BANDS[severity],
                "location": location, "trauma": source["trauma"],
                "event_key": key,
            }
            if (wound["detail"] != expected_detail
                    or wound["round"] != damage["round"]
                    or wound["turn"] != damage["turn"]
                    or record.get("wound") != severity):
                raise AssertionError(
                    "Wound does not follow original damage, d20, critical and global ID")
            wounds[actor].append({
                "id": name, "severity": severity, "progress": 0,
                "requirement": WOUND_BANDS[severity]})
            expected_created.append(wound["index"])
        elif matched or record.get("wound") is not None:
            raise AssertionError("Unqualified G4 packet invented a wound")
    if sorted(expected_created) != [ev["index"] for ev in created]:
        raise AssertionError("Unpaired or reordered wound creation event")
    if any(ev["kind"] in ("g4_basic_heal_applied", "g4_wound_repaired")
           for ev in ledger):
        raise AssertionError("No external healing/wound repair in authored pack")
    # Geometry is replayed from the source grid, not accepted from its
    # editable closing snapshot, for both battle and exit policies.
    positions = _replay_native_exit_geometry(
        ledger, party_exits=(policy == "opposed_living_hunter_withdrawal"))
    for actor in ROSTER:
        state, start = final[actor], source_initial[actor]
        expected_dying = state["hp"] <= 0 and not state["dead"]
        arrows = (state["ammunition"] if actor == "archer"
                  and policy == "mixed_victory_rite"
                  else start["ammunition"])
        expected = {
            "source_id": start["source_id"],
            "source_digest": start["source_digest"],
            "hp": state["hp"], "hp_max": start["hp_max"],
            "vigor": state["vigor"],
            "vp_available": state["vp_available"],
            "vp_committed": state["vp_committed"],
            "ammunition": arrows,
            "occupied": positions[actor],
            "wounds": wounds[actor],
            "dying": expected_dying,
            "dead": state["dead"],
        }
        if state != expected:
            raise AssertionError(
                f"Closing {actor} actor snapshot contradicts source/ledger state")
    return True


def _source_decisions(ledger, *, policy, terminal, final_state):
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
        actual_hunter_hits = _hunter_bite_hits(
            ledger, "vanguard", policy="mixed_victory_rite")
        if (len(actual_hunter_hits) != 1
                or actual_hunter_hits[0]["resolved"]["round"] != 2):
            raise AssertionError("Victory Hunter must land one actual paid Round-2 Bite")
        # Bind all four A/B paid actions to the original G6-C defense
        # policy, Hunter Dodge Pressure and BOTH hit/miss response windows.
        # The hit-specific G4/G4.5 audit below remains independent.
        _reconcile_victory_all_ab_sequences(ledger)
        _reconcile_victory_hunter_sequences(ledger)
        for who, attack in (("vanguard", "B06-PC-A-SWORD"),
                            ("guardian", "B06-PC-B-MACE")):
            # Verify every original paid sequence action, not just hits.
            # B's Round-1 miss is still a 20-AP commitment and cannot
            # disappear from the Turn AP budget merely because no G4
            # damage event was produced.
            label = f"sequence:{attack}:0"
            all_paid = [v for v in ledger
                        if v["kind"] == "action_committed"
                        and v["detail"].get("actor") == who
                        and v["detail"].get("label") == label]
            if (len(all_paid) != 2
                    or {v["round"] for v in all_paid} != {1, 2}):
                raise AssertionError("A/B require both original melee AP payments")
            for action in all_paid:
                _paid_action_ap(ledger, action, actor=who, cost=20,
                                kind="physical", label=label)
            _player_melee_hit_chains(ledger, who, attack)
        # The G6-D G7-H opt-in branch casts exactly one G3 effect, the
        # first effect allocated on its source scene. Reconstruct the FULL
        # _new_effect() receipt from the authorized Chosen Maintained Self
        # Guided spell; an editable receipt's ID, parent, expiry, budget,
        # resistance or extra field cannot redefine the original Rite.
        expected_rite = {
            "caster": "archer",
            "recipient": "archer",
            "effect": "G3-0001",
            "effect_kind": "Guided Regeneration",
            "committed": 1,
            "chosen": True,
            "anchor": None,
            "parent": None,
            "budget": None,
            "resistance": 0,
            "expiry_round": None,
        }
        rites = events["g3_effect_established"]
        if (len(rites) != 1
                or rites[0]["round"] != 1
                or rites[0]["turn"] != "archer"
                or rites[0]["detail"] != expected_rite
                or not any(
                    v["kind"] == "action_committed"
                    and v["detail"].get("actor") == "archer"
                    and v["detail"].get("label") == "g3:guided:maintained"
                    and v["index"] < rites[0]["index"] for v in ledger)):
            raise AssertionError(
                "Chosen R Rite requires the exact native G3 establishment receipt")
        _spell_payment_chain(
            ledger, rites[0], actor="archer", label="g3:guided:maintained",
            ap=30, vp_mode="committed", vp_points=1)
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
        if len(flames) != 2 or not all(
                flame["detail"].get("tier") == 1
                and flame["detail"].get("vp_spent") == 2
                and flame["detail"].get("primary_face") in range(2, 21)
                and flame["detail"].get("attack_total") ==
                    flame["detail"].get("primary_face") + 5
                for flame in flames):
            raise AssertionError("G7-H Flame source/tier/attack receipts invalid")
        for flame in flames:
            _flame_hit_from_defense(flame)
            _spell_payment_chain(
                ledger, flame, actor="scholar",
                label="g3:thrown_flame:T1", ap=20,
                vp_mode="spent", vp_points=2)
        deliveries = [_flame_delivery_packet(ledger, flame) for flame in flames]
        if len({hit["index"] for hit in deliveries}) != 2:
            raise AssertionError("Two source Flames cannot reuse one G4 delivery")
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
            hits = [hit for hit in _hunter_bite_hits(
                    ledger, victim, policy="hunter_multitarget_defeat")
                    if hit["damage"]["index"] == death["index"]
                    and hit["bridge"]["detail"]["actual_result"].get("dead") is True
                    and hit["resolved"]["detail"]["damage"].get("dead") is True]
            if len(hits) != 1:
                raise AssertionError("Lethal G4 event lacks paid G5 roll/G4.5/resolved Bite")
            proven.append(death["index"])
        if proven != lethal_indices:
            raise AssertionError("G7-C death indices differ from independently resolved Bites")

        # G7-G logs a Hunter-selected victim on each actual Hunter turn.
        # Reconstruct that history from the original native G4 death
        # transitions and the ordered source party, not from the editable
        # verification receipt's distinct_targets or party assertions.
        selections = [v for v in ledger if
                      v["kind"] == "g7g_hunter_target_selected"]
        pursuits = [v for v in ledger if
                    v["kind"] == "g7g_hunter_pursuit_executed"]
        round_ends = [v for v in ledger if v["kind"] == "round_end"]
        if (len(selections) != len(round_ends)
                or len(pursuits) != len(selections)
                or not all(selections[i]["round"] == i + 1
                           for i in range(len(selections)))):
            raise AssertionError("Defeat source Hunter must select one target each round")
        history = []
        sources = ledger[0]["detail"]["source_ids"]
        for selected, pursued in zip(selections, pursuits):
            alive = [actor for actor in ROSTER[1:]
                     if not any(e["detail"].get("recipient") == actor
                                and e["detail"].get("dead") is True
                                and e["index"] < selected["index"]
                                for e in events["g4_damage_applied"])]
            expected = alive[0] if alive else None
            if (expected is None
                    or selected["round"] != pursued["round"]
                    or selected["turn"] != "hunter" or pursued["turn"] != "hunter"
                    or selected["index"] >= pursued["index"]
                    or selected["detail"].get("hunter") != "hunter"
                    or selected["detail"].get("target") != expected
                    or selected["detail"].get("target_source") !=
                       sources[expected]["source_id"]
                    or pursued["detail"].get("hunter") != "hunter"
                    or pursued["detail"].get("target") != expected):
                raise AssertionError(
                    "G7-G target choices contradict original Hunter turns and deaths")
            history.append(expected)
        expected_receipt = {
            "party": list(ROSTER[1:]),
            "native_terminal_index": terminal["index"],
            "lethal_damage_indices": proven,
            "distinct_targets": list(dict.fromkeys(history)),
            "hunter_alive": True,
        }
        verified = items[0]
        if (verified["detail"] != expected_receipt
                or verified["round"] != terminal["round"]
                or verified["turn"] is not None
                or verified["index"] <= terminal["index"]
                or final_state["hunter"]["dead"] is not False
                or set(expected_receipt["distinct_targets"]) != set(ROSTER[1:])):
            raise AssertionError(
                "G7-G full defeat verification must exactly match source Bite/death chains")
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
        bite_hits = _hunter_bite_hits(
            ledger, "vanguard", policy="opposed_living_hunter_withdrawal")
        if (len(bite_hits) != 2 or
                [h["resolved"]["round"] for h in bite_hits] != [1, 2]
                or bite_hits[0]["resolved"]["index"] >= pursuit["index"]
                or bite_hits[1]["roll"]["index"] <= pursuit["index"]
                or bite_hits[1]["resolved"]["index"] >= terminal["index"]
                or items[0]["detail"].get("hunter_paid_bite_indices") !=
                   [h["resolved"]["index"] for h in bite_hits]):
            raise AssertionError(
                "G7-G opposed withdrawal needs two real paid Bites, including post-pursuit")
        receipts = _authored_exit_chains(ledger, terminal, final_state)
        # Rebuild the *whole* G7-G certificate from its authenticated
        # G7-C terminal, real G1 pursuit, two paid G5 Bites, distinct
        # G1/G4.5/G5 border exits and source Hunter's closing HP/death.
        # No free-form fields, stale pointers or contradictory claims may
        # be accepted merely because the ledger digest was recomputed.
        expected_receipt = {
            "native_terminal_index": terminal["index"],
            "hunter_alive": True,
            "pursuit_index": pursuit["index"],
            "hunter_paid_bite_indices": [
                hit["resolved"]["index"] for hit in bite_hits],
            "border_exit_indices": [receipt["g5"] for receipt in receipts],
            "boundary": "authored_G7C_scene_exits_only",
            "ongoing_world_pursuit_not_adjudicated": True,
        }
        verified = items[0]
        if (verified["detail"] != expected_receipt
                or verified["round"] != terminal["round"]
                or verified["turn"] is not None
                or verified["index"] <= terminal["index"]
                or final_state["hunter"]["dead"] is not False
                or final_state["hunter"]["hp"] <= 0):
            raise AssertionError(
                "G7-G opposed withdrawal receipt must exactly follow the native evidence")
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
    completed_rounds = _native_round_turn_chronology(ledger)
    _origin(report, ledger, policy=policy, level=level, seed=seed)
    _reconcile_all_turn_end_ap(ledger, level=level, seed=seed)
    turns = [v["detail"].get("actor") for v in ledger if v["kind"] == "turn_end"]
    ends = [v for v in ledger if v["kind"] == "round_end"]
    last_round_end = ends[-1]["index"] if ends else -1
    open_native = any(
        ev["kind"] in ("round_begin", "turn_start_expiry", "turn_resources",
                       "action_committed", "attack_sequence_committed",
                       "g5_melee_sequence_attested", "g1_movement_step")
        and ev["index"] > last_round_end for ev in ledger)
    if (not ends or turns != list(ROSTER) * len(ends)
            or len(ends) != completed_rounds
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
    _reconcile_source_vp(ledger, final)
    _reconcile_source_regeneration(
        ledger, final, policy=policy, level=level, seed=seed)
    if policy == "mixed_victory_rite":
        _reconcile_victory_bow_ammunition(ledger, initial, final, level=level)
    terminal = _terminal_proof(report, ledger, policy=policy, deaths=deaths)
    facts = _source_decisions(
        ledger, policy=policy, terminal=terminal, final_state=final)
    _reconcile_complete_snapshots(
        ledger, initial, final, policy=policy, level=level, seed=seed)
    _reconcile_every_g45_target_snapshot(
        ledger, policy=policy, level=level, seed=seed)
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
