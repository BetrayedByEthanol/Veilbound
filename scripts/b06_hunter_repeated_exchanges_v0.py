"""Repeatable, *bounded* Hunter party combat; stop before unresolved wound play.

Run python -m scripts.b06_hunter_repeated_exchanges_v0 in a repository checkout.
No inferred surprise statistics, CR, magic actions, creature AI or wound recovery.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import random

from scripts.b06_hunter_party_exchanges_v0 import (
    BUILD, HUNTER_FILE, SCENARIOS, PRONE_TARGET_MELEE_ATTACK_BONUS,
)

SEED_COUNT = 512
ROUNDS_CAP = 3
DEFENSE_POLICIES = ("guard", "dodge")


def die(seed, sides, *key):
    """Stable independent keyed die: comparisons reuse rolls across branches."""
    data = json.dumps([seed, *key], separators=(",", ":")).encode()
    number = int.from_bytes(sha256(data).digest()[:8], "big")
    return random.Random(number).randint(1, sides)


def strike(seed, key, attacker_bonus, defense_kind, defense_value, *,
           base, penetration, target_armor):
    """Native ordinary or natural-20 confirmed direct-HP attack, no wounds."""
    face = die(seed, 20, *key, "attack")
    if face == 1:
        return (0, "miss")
    if face == 20:
        confirm = die(seed, 20, *key, "confirm")
        if defense_kind == "take_hit":
            tier = "devastating" if confirm == 20 else "critical"
        elif confirm == 20:
            tier = "devastating"
        elif confirm == 1 or confirm + attacker_bonus <= defense_value:
            tier = "strong"
        else:
            tier = "critical"
    elif defense_kind == "take_hit" or face + attacker_bonus > defense_value:
        tier = "ordinary"
    else:
        return (0, "miss")
    extra = 1 if tier == "strong" else 2 if tier in ("critical", "devastating") else 0
    bonus = sum(die(seed, 4, *key, "bonus", j) for j in range(extra))
    rolled = base + die(seed, 6, *key, "damage") + bonus
    return max(0, rolled - max(0, target_armor - penetration)), tier


def simulate_trial(level, party_size, setup, defense_policy, seed, *, hunter=None):
    """Stop at first Hunter/A1 nonpositive HP or *unresolved* Devastating wound.

    Initial terrain grants a legal Pounce *only* on Hunter's first turn when
    no PC has acted beforehand and the scenario starts with the three-step lane.
    Other cases use a legal ordinary Bite following open approach. Initiative
    is real d20+4 for all actors, tie-breaking by authored Awareness/Agility.
    The first A1 zero-HP crossing ends this controlled focus-fire scenario;
    other PCs are not magically defeated. No right to claim a party wipe.
    """
    if (level, party_size, setup) not in SCENARIOS:
        raise ValueError("Unsupported party/level/setup")
    if defense_policy not in DEFENSE_POLICIES:
        raise ValueError("Unknown player defense policy")
    if not isinstance(seed, int) or seed < 0:
        raise ValueError("Seed must be a nonnegative integer")
    if hunter is None:
        hunter = json.loads(HUNTER_FILE.read_text(encoding="utf-8"))
    profiles = {a["id"]: a for a in hunter["attack_profiles"]}
    bite = profiles["B06-AT-04"]
    pounce = profiles["B06-AT-06"]
    hd = hunter["defenses"]
    hr = hunter["resources"]
    assert (hd["hp_max"], hd["armor"], hd["dodge_base"]) == (14, 3, 14)
    assert hr["natural_regeneration_throughput"] == 4
    assert bite["attack_roll"]["total_bonus"] == 6
    assert bite["primary_hp_packet"]["fixed_base"] == 3
    assert bite["primary_hp_packet"]["armor_penetration"] == 1
    assert pounce["linked_contest"]["total_pressure_bonus"] == 4
    assert hd["guard_instrument"] is None

    members = [
        {"id": ("A" if i % 2 == 0 else "B") + str(1 + i // 2),
         "kind": "A" if i % 2 == 0 else "B"}
        for i in range(party_size)
    ]
    a1 = BUILD["A"]
    ahp, avig = a1["hp"], a1["hp"] * level
    hhp, hvig = hd["hp_max"], hd["vigor_max"]
    prone = False
    toxin = None
    pounce_used = False
    pounce_success = False
    pounce_balance_resolved = False
    stand_opportunities = 0
    criticals = 0
    attacks = 0
    h_first = False
    first_round = 0
    rounds = 0
    terminal = "window_end"
    # At identical initiative totals: Hunter AWA2 > Vanguard AWA1 > Guardian AWA0;
    # surviving equal scores can be resolved by AGI or the tie-breaker stream.
    initiative = {"H": (die(seed, 20, "initiative", "H") + 4, 2, 2)}
    for pc in members:
        awareness, agility = (1, 3) if pc["kind"] == "A" else (0, 2)
        initiative[pc["id"]] = (
            die(seed, 20, "initiative", pc["id"]) + 4,
            awareness, agility,
        )
    order = sorted(initiative, key=lambda ident: (
        -initiative[ident][0], -initiative[ident][1],
        -initiative[ident][2], die(seed, 20, "tiebreak", ident)))
    h_first = order[0] == "H"

    def finish_zero(target, tier):
        # No continuation through the first 0-HP wound; devastating wound
        # effects (even above 0 HP) also require a separate authored trace.
        if target == "H" and hhp <= 0:
            return "hunter_first_zero"
        if target == "A1" and ahp <= 0:
            return "frontline_first_zero"
        if tier == "devastating":
            return "devastating_wound_unresolved"
        return None

    for rnd in range(1, ROUNDS_CAP + 1):
        rounds = rnd
        h_dodge = 0
        a_dodge = 0
        guard_remaining = (30 + 6 * (level - 1)) // 20 + a1["guard_extra"]
        opportunity = 1
        for who in order:
            if who == "H":
                # Real own-turn regeneration even if PCs acted earlier.
                restored = min(4, 14 - hhp, hvig)
                hhp += restored
                hvig -= restored
                # If Hunter is first overall in the ambush lane it can make a
                # straight 3-step Pounce. Earlier PC approach disrupts lane.
                legal_pounce = (rnd == 1 and setup == "ambush" and h_first)
                if legal_pounce:
                    pounce_used = True
                defkind = defense_policy
                if defkind == "guard" and guard_remaining:
                    guard_remaining -= 1
                    defense_value = a1["guard"]
                else:
                    defkind = "dodge"
                    defense_value = 10 + a1["agi"] + 1 - a_dodge
                    a_dodge += 2
                damage, tier = strike(
                    seed, (rnd, "H", "bite"), 6, defkind, defense_value,
                    base=3, penetration=1, target_armor=a1["armor"])
                criticals += tier in ("strong", "critical", "devastating")
                ahp -= damage
                # Stop at the *damage/wound boundary*, before injecting toxin
                # or resolving the linked Pounce balance rider. A Dying or
                # Devastating result cannot be followed by invented effects.
                terminal = finish_zero("A1", tier) or terminal
                if terminal != "window_end":
                    break
                if damage > 0 and toxin is None:
                    resist = die(seed, 20, rnd, "H", "toxin") + a1["vit"]
                    toxin = "reduced" if resist >= 12 else "full"
                if legal_pounce:
                    # Independent Balance, not gated on Bite *success*, but
                    # reached only when Bite has not triggered the declared
                    # 0-HP or Devastating-wound simulation stop.
                    pounce_balance_resolved = True
                    pressure = die(seed, 20, rnd, "H", "pounce") + 4
                    balance = die(seed, 20, rnd, "A1", "balance") + a1["agi"]
                    pounce_success = pressure > balance
                    prone = pounce_success
            else:
                member = next(x for x in members if x["id"] == who)
                if who == "A1":
                    # Only A1 is the targeted defender in this scoped policy.
                    # Actual Step 2 before voluntary movement/actions.
                    rec = min(a1["regen"], a1["hp"] - ahp, avig)
                    ahp += rec
                    avig -= rec
                    if prone:
                        # Standing costs 4 MP. The target stays Prone for
                        # opportunity resolution; non-Prone Hunter gets +2.
                        if opportunity:
                            opportunity = 0
                            stand_opportunities += 1
                            defkind = defense_policy
                            if defkind == "guard" and guard_remaining:
                                guard_remaining -= 1
                                defense_value = a1["guard"]
                            else:
                                defkind = "dodge"
                                defense_value = 14 - a_dodge
                                a_dodge += 2
                            damage, tier = strike(
                                seed, (rnd, "H", "standing_opportunity"),
                                6 + PRONE_TARGET_MELEE_ATTACK_BONUS,
                                defkind, defense_value, base=3,
                                penetration=1, target_armor=a1["armor"])
                            criticals += tier in ("strong", "critical", "devastating")
                            ahp -= damage
                            # An Opportunity can also create an unresolved
                            # wound. Stop before its toxin resistance or Stand.
                            terminal = finish_zero("A1", tier) or terminal
                            if terminal != "window_end":
                                break
                            if damage > 0 and toxin is None:
                                resist = die(seed, 20, rnd, "H", "opp_toxin") + a1["vit"]
                                toxin = "reduced" if resist >= 12 else "full"
                        prone = False  # Stand only after all Opportunity responses
                # Phase 2 policy: each character spends all legal AP on
                # ordinary martial strikes; no optional magic/Talent use.
                count = (30 + 6 * (level - 1)) // 20
                spec = BUILD[member["kind"]]
                for j in range(count):
                    attacks += 1
                    defense_value = hd["dodge_base"] - h_dodge
                    h_dodge += 2  # Dodge Pressure even when attack misses
                    damage, tier = strike(
                        seed, (rnd, who, "attack", j), spec["attack"],
                        "dodge", defense_value, base=spec["weapon_base"],
                        penetration=spec["penetration"], target_armor=hd["armor"])
                    criticals += tier in ("strong", "critical", "devastating")
                    hhp -= damage
                    terminal = finish_zero("H", tier) or terminal
                    if terminal != "window_end":
                        break
                if terminal != "window_end":
                    break
        if rnd == 1:
            first_round = hhp
        if terminal != "window_end":
            break
    return {
        "seed": seed, "level": level, "party_size": party_size, "setup": setup,
        "defense": defense_policy, "terminal": terminal, "rounds": rounds,
        "hunter_first_initiative": h_first, "hunter_hp": hhp,
        "frontline_hp": ahp, "hunter_vigor": hvig, "frontline_vigor": avig,
        "first_round_hunter_hp": first_round, "pounce_used": pounce_used,
        "pounce_balance_resolved": pounce_balance_resolved,
        "pounce_prone": pounce_success, "standing_opportunities": stand_opportunities,
        "toxin": toxin, "critical_events": criticals, "pc_attack_attempts": attacks,
    }


def run_matrix(seeds=SEED_COUNT, *, hunter=None):
    if not isinstance(seeds, int) or seeds <= 0:
        raise ValueError("Positive seed count required")
    cases = []
    for level, size, setup in SCENARIOS:
        for policy in DEFENSE_POLICIES:
            trials = [simulate_trial(level, size, setup, policy, seed, hunter=hunter)
                      for seed in range(seeds)]
            t = Counter(x["terminal"] for x in trials)
            cases.append({
                "level": level, "party_size": size, "setup": setup,
                "defense": policy, "trials": seeds, "terminal_counts": dict(t),
                "hunter_initiative_first": sum(x["hunter_first_initiative"] for x in trials),
                "pounce_attempts": sum(x["pounce_used"] for x in trials),
                "pounce_balance_resolutions": sum(x["pounce_balance_resolved"] for x in trials),
                "pounce_prone": sum(x["pounce_prone"] for x in trials),
                "standing_opportunities": sum(x["standing_opportunities"] for x in trials),
                "full_toxin": sum(x["toxin"] == "full" for x in trials),
                "reduced_toxin": sum(x["toxin"] == "reduced" for x in trials),
                "critical_events": sum(x["critical_events"] for x in trials),
                "mean_first_round_hunter_hp": round(sum(x["first_round_hunter_hp"] for x in trials) / seeds, 3),
            })
    return cases


def main():
    print(json.dumps({"method": "paired keyed seeds, wound-bounded first-zero",
                      "seed_count": SEED_COUNT, "cases": run_matrix()}, indent=2))


if __name__ == "__main__":
    main()
