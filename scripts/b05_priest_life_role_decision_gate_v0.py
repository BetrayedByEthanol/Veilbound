"""B04/B05 Priest Life role decision-gate: varied native source scenes.

PS-08 ally support and bounded PS-01/02 self-survival evidence, not a
full role certificate, probability experiment, adaptive GM, or tuning.
Reuse existing audited H/M/Low adapters, G0 Step2 and G5/G4 attack paths.
"""
import argparse
from copy import deepcopy
import json

from scripts.b05_priest_life_multi_recipient_stress_v0 import (
    FOCI, OPPONENTS, POLICIES, L3_ONLY, L2_ONLY, PATTERNS,
    _step, _priest,
)
from scripts.b05_high_priest_life_invocation_v0 import HighLifeLiturgy
from scripts.b05_medium_priest_consecrations_v0 import MediumLifeConsecrations
from scripts.b05_low_life_native_rites_v0 import LowLifeNativeRites
from scripts.b06_encounter_state_v0 import (
    Encounter, party_actor, enemy_actor, UnresolvedDecision,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

# Authored decisions; no "random sample" interpretation.
VARIANTS = {
    "prepared_light": dict(initiative="priest_first", pattern="alternating",
                           attack_face=12, sword_die=1, defense="take_hit"),
    "surprise_heavy": dict(initiative="foe_first", pattern="rotating",
                           attack_face=16, sword_die=4, defense="take_hit"),
    "cautious_dodge": dict(initiative="priest_first", pattern="alternating",
                          attack_face=8, sword_die=1, defense="dodge"),
    "pressured_dodge": dict(initiative="foe_first", pattern="alternating",
                           attack_face=16, sword_die=4, defense="dodge"),
}
SENTRY_DIE = 4
WOUND_DIE = 8
ROUNDS = 4
CHOSEN_POLICIES = {
    "H": ("baseline", "triage", "guided_front", "split_wards"),
    "M": ("baseline", "triage", "guided_front", "guided_intercession",
          "shelter_intercession"),
    "A": ("baseline", "chosen_self", "triage", "chosen_and_heal"),
    "B": ("baseline", "chosen_self", "vital_exaltation"),
}
ROLE_NAMES = {
    "H": "Healer / Support", "M": "Healer / Support",
    "A": "Fighter (self-sustain candidate)", "B": "Defender (self-protection candidate)",
}


def _validate(role, level, opponent, variant, policy, seed):
    if (type(level) is not int or level not in (1, 2, 3)
            or type(seed) is not int or seed < 0):
        raise ValueError("Exact L1–3, nonnegative integral seed required")
    if (role not in CHOSEN_POLICIES
            or policy not in CHOSEN_POLICIES[role]
            or policy not in POLICIES[role]
            or opponent not in OPPONENTS or variant not in VARIANTS):
        raise ValueError("Only authored source role / foe / variant / policy")
    if policy in L3_ONLY[role] and level < 3:
        raise ValueError("L3 feature not available at this level")
    if policy in L2_ONLY[role] and level < 2:
        raise ValueError("L1 Low cannot fund Chosen plus external Basic Heal")


def _scene(role, level, opponent, variant, policy, seed):
    v = VARIANTS[variant]
    source, start = OPPONENTS[opponent]
    priest = party_actor(role, level, "priest", "party", occupied=((2, 1),))
    front = party_actor("F", level, "front", "party", occupied=((2, 2),))
    rear = party_actor("R", level, "rear", "party", occupied=((3, 3),))
    foe = enemy_actor(source, "foe", "enemy", start_state=start,
                      occupied=((3, 2),))
    initiative = ({"foe": 50, "priest": 40, "front": 20, "rear": 10}
                  if v["initiative"] == "foe_first" else
                  {"priest": 40, "foe": 30, "front": 20, "rear": 10})
    e = Encounter([priest, foe, front, rear], initiative, seed=seed,
                  scenario="B04-B05-Priest-Life-role-decision-gate-v0",
                  policy="authored_varied_initiative_damage_defenses_targets",
                  objective="PS-08_ally_support_and_self_survival_not_victory")
    GridMovement(e, width=8, height=7, scene_id="B05-priest-role-clear")
    SpellState(e)
    DamageState(e)
    adapter = (HighLifeLiturgy(e, "priest", preparation="standard")
               if role == "H" else
               MediumLifeConsecrations(e) if role == "M" else
               LowLifeNativeRites(e, "priest"))
    combat = SourceMelee(e)
    expected = (("foe", "priest", "front", "rear")
                if v["initiative"] == "foe_first" else
                ("priest", "foe", "front", "rear"))
    if e.order != expected:
        raise AssertionError("Native rolled Initiative differs from authored order")
    for recipient in ("priest", "front", "rear"):
        if not e.g1.melee_contact("foe", recipient):
            raise AssertionError("Original source melee contact was lost")
    e.begin_round()
    e.log("b05_role_gate_policy", role=role, focus=FOCI[role], level=level,
          opponent=opponent, variant=variant, policy=policy,
          initiative=initiative.copy(), attack_face=v["attack_face"],
          sword_die=v["sword_die"], defense=v["defense"],
          target_schedule=list(PATTERNS[v["pattern"]]),
          sentry_die=SENTRY_DIE, wound_roll=WOUND_DIE, seed=seed,
          source_digests={k: a.source.digest for k, a in e.actors.items()})
    return combat, adapter


def _foe(combat, opponent, target, v, round_no):
    e = combat.e
    if e.actors[target].dead:
        e.log("b05_role_target_unavailable", recipient=target,
              round=round_no, reason="source_target_already_dead")
        return
    profile = ("B06-AT-03" if opponent == "soldier"
               else e.g3.sentry_profile("foe"))
    if profile not in ("B06-AT-03", "B06-AT-02"):
        raise UnresolvedDecision("Genuine source sword unavailable")
    if not e.g1.melee_contact("foe", target):
        raise UnresolvedDecision("Authored target outside genuine melee contact")
    defense = v["defense"]
    seq = combat.declare("foe", target, profiles=(profile,),
                         defenses=(defense,))
    assigned = e.ledger[seq["defenses"][0]]
    if (assigned["kind"] != "defense_assigned"
            or assigned["detail"]["actor"] != target
            or assigned["detail"]["defense"] != defense):
        raise AssertionError("Cannot replace native G0 defense receipt")
    value = assigned["detail"]["defense_value"]
    landed = (defense == "take_hit"
              or v["attack_face"] + combat._profile("foe", profile) > value)
    dice = {"attack_face": v["attack_face"]}
    if landed:
        dice["damage_face"] = v["sword_die"]
        dice["wound_location_roll"] = WOUND_DIE
        if profile == "B06-AT-02":
            dice["vigor_die"] = SENTRY_DIE
    # L3 M shelter Intercession: only one specific living source attack
    # on a distinct R beneficiary during R2; G4 itself owns the live
    # positive packet and paid Reaction/VP. Never invoke the adapter
    # from an attacker miss or a synthetic damage packet.
    medium = getattr(e.g3, "medium_life", None)
    host = medium._host("priest") if medium is not None else None
    if (landed and e.actors["priest"].level == 3 and
            host is not None and host.kind == "Vital Shelter" and
            host.recipient != target and host.budget and
            opponent == "sentry_prepared" and profile == "B06-AT-02"
            and target == "rear" and round_no == 2 and
            e.actors["priest"].reaction_available and
            e.actors["priest"].vp_available >= 2 and
            e.actors[target].vigor > 0):
        dice["medium_intercessor"] = "priest"
    outcome = combat.resolve(seq, 0, **dice)
    if outcome["outcome"] != ("hit" if landed else "miss"):
        raise AssertionError("Native G5 outcome differs from the real preflight")
    if not landed and outcome["damage"] is not None:
        raise AssertionError("G5 miss cannot deliver phantom G4 packet")


def _metrics(e, v):
    def events(kind):
        return [x for x in e.ledger if x["kind"] == kind]
    attacks = events("g5_melee_resolved")
    skipped = events("b05_role_target_unavailable")
    damage = events("g4_damage_applied")
    if len(attacks) + len(skipped) != ROUNDS:
        raise AssertionError("Opponent actions must match four authored rounds")
    for x in attacks:
        round_no = x["round"]
        expected = PATTERNS[v["pattern"]][round_no - 1]
        if x["detail"]["target"] != expected:
            raise AssertionError("Native target differs from authored target")
    if sum(x["detail"]["outcome"] == "hit" for x in attacks) != len(damage):
        raise AssertionError("Native hit/damage receipt mismatch")
    steps = {who: sum(x["detail"]["actor"] == who
                      for x in events("regeneration_step"))
             for who in ("priest", "front", "rear")}
    if any(n != ROUNDS for n in steps.values()):
        raise AssertionError("One actual G0 Step2 per source recipient/round")
    priest = e.actors["priest"]
    return {
        "attack_attempts": len(attacks), "attack_hits": len(damage),
        "attack_misses": len(attacks) - len(damage),
        "unavailable_targets": len(skipped),
        "target_hits": {who: sum(x["detail"]["target"] == who
                        and x["detail"]["outcome"] == "hit" for x in attacks)
                        for who in ("front", "rear", "priest")},
        "steps": steps,
        "recipients": {who: {"hp": e.actors[who].hp,
                             "vigor": e.actors[who].vigor,
                             "dead": e.actors[who].dead,
                             "wounds": len(e.actors[who].wounds)}
                       for who in ("front", "rear", "priest")},
        "heals": len(events("g4_basic_heal_applied")),
        "heal_receipts": [x["detail"] for x in events("g4_basic_heal_applied")],
        "guided_intercessions": len(events("b05_guided_intercession_armed")),
        "vital_intercessions": len(events("b05_vital_intercession_packet")),
        "intercession_payments": len(events("b05_intercession_paid")),
        "ally_effects": sum(
            x["detail"].get("caster") == "priest"
            and x["detail"].get("recipient") in ("front", "rear")
            for x in events("g3_effect_established")),
        "self_effects": sum(
            x["detail"].get("caster") == "priest"
            and x["detail"].get("recipient") == "priest"
            for x in events("g3_effect_established")),
        "spent_vp": priest.vp_spent, "committed_vp": priest.vp_committed,
        "available_vp": priest.vp_available,
        "priest_ap_paid": sum(x["detail"]["ap_spent"] for x in
            events("action_committed") if x["detail"]["actor"] == "priest"),
        "priest_reaction_available": priest.reaction_available,
        "vigor_prevented": sum(vv["prevented"] for x in damage
                          for vv in x["detail"]["vigor_details"]),
        "natural_hp_restored": {who: sum(x["detail"]["hp_restored"]
             for x in events("regeneration_step") if x["detail"]["actor"] == who)
             for who in ("front", "rear", "priest")},
    }


def run_policy(*, role, level, opponent, variant, policy, seed=0):
    _validate(role, level, opponent, variant, policy, seed)
    v = VARIANTS[variant]
    combat, adapter = _scene(role, level, opponent, variant, policy, seed)
    e = combat.e
    for round_no, target in enumerate(PATTERNS[v["pattern"]], start=1):
        if round_no > 1:
            combat.bridge.begin_next_round()
        for who in e.order:
            _step(combat, adapter, role, policy, who, round_no)
            if who == "priest":
                _priest(combat, adapter, role, policy, round_no)
            elif who == "foe":
                _foe(combat, opponent, target, v, round_no)
            combat.bridge.end_current_turn()
    if e.current is not None or combat.pending_attack_slots():
        raise AssertionError("Unresolved native G0/G5 state")
    e.check()
    result = {
        "version": "B04-B05-Priest-Life-Role-Decision-Gate-v0",
        "role": role, "focus": FOCI[role], "playstyle": ROLE_NAMES[role],
        "level": level, "opponent": opponent, "variant": variant,
        "policy": policy, "seed": seed,
        "source_ids": {k: a.source.source_id for k, a in e.actors.items()},
        "source_digests": {k: a.source.digest for k, a in e.actors.items()},
        "metrics": _metrics(e, v), "ledger": deepcopy(e.ledger),
        "bounded_role_evidence": True, "PS_08_full_role_certified": False,
        "PS_02_full_ally_defender_certified": False,
        "PS_01_full_fighter_certified": False,
        "global_balance_certified": False, "numerical_tuning_authorized": False,
        "sampled_win_rate": None, "focus_ranking": None,
    }
    result["ledger_sha256"] = canonical_digest(result["ledger"])
    return result


def attest_policy(report, *, role, level, opponent, variant, policy, seed=0):
    expected = run_policy(role=role, level=level, opponent=opponent,
                          variant=variant, policy=policy, seed=seed)
    if (not isinstance(report, dict)
            or report.get("ledger_sha256") != canonical_digest(report.get("ledger"))
            or report != expected):
        raise AssertionError("Source-native role gate must replay fully")
    return deepcopy(expected)


def _key(row):
    return (row["role"], row["level"], row["opponent"], row["variant"])


def _delta(row, base):
    m, b = row["metrics"], base["metrics"]
    # Preserve changes in real enemy exposure; cannot score a canceled
    # attack after death as free healing or compare differing hit counts.
    matched = (m["attack_attempts"], m["attack_hits"],
               m["unavailable_targets"]) == (
               b["attack_attempts"], b["attack_hits"],
               b["unavailable_targets"])
    return {"like_exposure": matched,
            "exposure_diff": {k: m[k] - b[k] for k in
                ("attack_attempts", "attack_hits", "unavailable_targets")},
            "priest_ap_paid_delta": m["priest_ap_paid"] - b["priest_ap_paid"],
            "spent_vp_delta": m["spent_vp"] - b["spent_vp"],
            "committed_vp_delta": m["committed_vp"] - b["committed_vp"],
            "endpoint_delta": ({who: {
                "hp": m["recipients"][who]["hp"] - b["recipients"][who]["hp"],
                "vigor": m["recipients"][who]["vigor"] -
                         b["recipients"][who]["vigor"]}
                for who in ("front", "rear", "priest")} if matched else None)}


def run_matrix(*, seed=0):
    if type(seed) is not int or seed < 0:
        raise ValueError("Nonnegative integral seed required")
    rows = []
    for role, policies in CHOSEN_POLICIES.items():
        for level in (1, 2, 3):
            for opponent in OPPONENTS:
                for variant in VARIANTS:
                    for policy in policies:
                        if (policy in L3_ONLY[role] and level < 3
                                or policy in L2_ONLY[role] and level < 2):
                            continue
                        r = run_policy(role=role, level=level, opponent=opponent,
                                       variant=variant, policy=policy, seed=seed)
                        rows.append({k: r[k] for k in ("role", "focus",
                            "playstyle", "level", "opponent", "variant", "policy",
                            "source_digests", "source_ids", "metrics",
                            "ledger_sha256")})
    bases = {_key(r): r for r in rows if r["policy"] == "baseline"}
    if len(bases) != 4 * 3 * len(OPPONENTS) * len(VARIANTS):
        raise AssertionError("Missing matched native role baselines")
    for row in rows:
        row["comparison"] = _delta(row, bases[_key(row)])
    result = {
        "version": "B04-B05-Priest-Life-Role-Decision-Matrix-v0",
        "seed": seed, "cases": rows, "case_count": len(rows),
        "variants": deepcopy(VARIANTS),
        "PS_08_bounded_support_evidence": True,
        "PS_01_complete_fighter_certified": False,
        "PS_02_complete_defender_certified": False,
        "PS_08_complete_healer_certified": False,
        "focus_comparative_balance_certified": False,
        "numerical_tuning_authorized": False,
        "sampled_win_rate": None, "focus_ranking": None,
        "unresolved": [
            "PS-01 genuine paid Low Priest outgoing physical offense",
            "PS-02 source-backed protector intervention on ally-targeted attack",
            "Two simultaneous authentic competing Medium Reaction opportunities",
            "Variable natural dice distributions, independent GM tactics and human role utility",
            "Full encounter terminal/aftermath and noncombat Focus evidence",
        ],
    }
    result["audit_sha256"] = canonical_digest(result)
    return result


def attest_matrix(report, *, seed=0):
    expected = run_matrix(seed=seed)
    if (not isinstance(report, dict)
            or report.get("audit_sha256") !=
                canonical_digest({k: v for k, v in report.items()
                                  if k != "audit_sha256"})
            or report != expected):
        raise AssertionError("Rehashed caller role report differs from native matrix")
    return deepcopy(expected)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--role", choices=tuple(CHOSEN_POLICIES))
    p.add_argument("--level", type=int, choices=(1, 2, 3))
    p.add_argument("--opponent", choices=tuple(OPPONENTS))
    p.add_argument("--variant", choices=tuple(VARIANTS))
    p.add_argument("--policy")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    selected = (args.role, args.level, args.opponent, args.variant, args.policy)
    if any(x is not None for x in selected) and not all(x is not None for x in selected):
        p.error("Specify role, level, opponent, variant and policy together")
    result = (run_policy(role=args.role, level=args.level,
                         opponent=args.opponent, variant=args.variant,
                         policy=args.policy, seed=args.seed)
              if all(x is not None for x in selected)
              else run_matrix(seed=args.seed))
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
