"""Scripted, non-critical Hunter vs Level-2/3 Low Life Priest party exchanges.

Intentionally bounded: fixed declared dice, predetermined legal open-lane contacts,
all allies choose martial actions; no generic surprise package, spell tactics,
critical confirmations, wound resolution after the first 0-HP crossing, or CR.
Run: python -m scripts.b06_hunter_party_exchanges_v0
"""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HUNTER_FILE = ROOT / "content/creatures/b06-hunter-of-the-woods.v0.json"
SHEET_AUTHORITY = ROOT / "docs/design/b05-life-low-priest-l3-build-exaltation-verification-v0.md"

# A = Restorative Vanguard; B = Preservation Guardian. Both are the audited
# Low Life Priest sheets; L2 is their L2 progression, not a certified new class.
# Do not substitute a generic adventurer archetype or invent new equipment.
BUILD = {
    "A": {"hp": 12, "vit": 2, "agi": 3, "armor": 3, "guard": 17,
          "guard_extra": 1, "attack": 7, "weapon_base": 4,
          "penetration": 2, "regen": 6, "initiative": 4},
    "B": {"hp": 13, "vit": 3, "agi": 2, "armor": 5, "guard": 18,
          "guard_extra": 2, "attack": 6, "weapon_base": 6,
          "penetration": 3, "regen": 6, "initiative": 4},
}
# Dice are declared before resolution and *none* is a natural 1 or 20.
# Test of full critical confirmation belongs in a subsequent calibration pass.
PC_DICE = {
    1: {"A1": (6, 6), "B1": (5, 5), "A2": (12, 12), "B2": (12, 12)},
    2: {"A1": (13, 13), "B1": (12, 12), "A2": (12, 12), "B2": (12, 12)},
}
DAMAGE_DIE = {1: 2, 2: 4}
SCENARIOS = tuple(
    (level, size, setup)
    for level in (2, 3) for size in (3, 4)
    for setup in ("warned", "ambush")
)


def actor(kind, index, level):
    spec = BUILD[kind]
    return {
        "id": f"{kind}{index}", "kind": kind, "level": level,
        "hp": spec["hp"], "max_hp": spec["hp"],
        "vigor": spec["hp"] * level, "max_vigor": spec["hp"] * level,
        "guard_remaining": 0, "prone": False, "toxin": None,
    }


def simulate(level, size, setup, hunter=None):
    """Execute a deliberately fixed open-lane, two-round maximum exchange.

    All combatants roll legitimate (predeclared) initiative: Hunter 16+4=20,
    A1 12+4=16, B1 11+4=15, A2 9+4=13, B2 7+4=11.
    Hunter has the first turn in BOTH setups, with no surprise statistic.
    Warned: immediate head contact, not three steps of free charge lane.
    Ambush: an unblocked three-step cardinal front lane permits one Pounce;
    target is standing, supported and one square, and first contact is legal.
    These are different *declared terrain/position* cases, not a claim that
    'ambush' guarantees winning initiative under the rules.
    """
    if (level, size, setup) not in SCENARIOS:
        raise ValueError("Unsupported benchmark matrix cell")
    if hunter is None:
        hunter = json.loads(HUNTER_FILE.read_text(encoding="utf-8"))
    defense = hunter["defenses"]
    resource = hunter["resources"]
    modes = {a["id"]: a for a in hunter["attack_profiles"]}
    bite = modes["B06-AT-04"]
    pounce = modes["B06-AT-06"]
    assert bite["attack_roll"]["total_bonus"] == 6
    assert pounce["linked_contest"]["total_pressure_bonus"] == 4
    assert defense["guard_instrument"] is None
    assert resource["turn_ap"] == 42 and resource["physical_action_ap"] == 24
    assert resource["natural_regeneration_throughput"] == 4
    assert resource["movement_points"] == 12
    members = [actor("A" if i % 2 == 0 else "B", 1 + i // 2, level)
               for i in range(size)]
    hhp, hvig = defense["hp_max"], defense["vigor_max"]
    pounce_prone = False
    opportunity_used = False
    toxin_applications = 0
    attacks = 0
    hits = 0
    log = []
    rounds = 0
    first_round_hunter_hp = None
    for rnd in (1, 2):
        if hhp <= 0:
            break
        rounds = rnd
        dodge_pressure = 0
        opportunity_available = True
        for pc in members:
            physical_tempo = (30 + 6 * (level - 1)) // 20
            pc["guard_remaining"] = physical_tempo + BUILD[pc["kind"]]["guard_extra"]
        # Regeneration Step on Hunter's actual own turn, before its Bite.
        if rnd > 1 and hhp > 0:
            restored = min(resource["natural_regeneration_throughput"],
                           defense["hp_max"] - hhp, hvig)
            hhp += restored
            hvig -= restored
            log.append(f"R{rnd} Hunter Step2 +{restored} HP, -{restored} Vigor")
        target = members[0]
        if target["hp"] > 0:
            bite_die = 14 if setup == "ambush" and rnd == 1 else 11 if rnd == 1 else 12
            attack_total = bite_die + bite["attack_roll"]["total_bonus"]
            assert target["guard_remaining"] > 0
            target["guard_remaining"] -= 1
            hit = attack_total > BUILD["A"]["guard"]  # strict >; ties block
            if hit:
                die = 4 if rnd == 1 else 3
                packet = bite["primary_hp_packet"]
                damage = max(0, packet["fixed_base"] + die -
                             max(0, BUILD["A"]["armor"] - packet["armor_penetration"]))
                target["hp"] -= damage
                if damage > 0:
                    if target["toxin"] is None:  # one active toxin, no stacking
                        resist = 8 + BUILD["A"]["vit"]
                        assert resist < 12
                        target["toxin"] = "Full (delayed; no instant penalty)"
                        toxin_applications += 1
                    else:
                        log.append(f"R{rnd} repeat puncture; venom does not stack")
                log.append(f"R{rnd} Hunter Bite {attack_total}>{BUILD['A']['guard']}, "
                           f"{damage} HP after Armor; A1 HP={target['hp']}")
            else:
                log.append(f"R{rnd} Hunter Bite {attack_total}<={BUILD['A']['guard']} Guard: 0 HP")
            if rnd == 1 and setup == "ambush":
                # Legal three-step head-forward Pounce; independent of Bite.
                # A1 selects AGI3 rather than STR2 for Balance Resistance.
                pressure = 14 + pounce["linked_contest"]["total_pressure_bonus"]
                balance = 12 + BUILD["A"]["agi"]
                pounce_prone = pressure > balance
                target["prone"] = pounce_prone
                log.append(f"R1 Pounce Balance {pressure}>{balance}: "
                           f"{'Prone' if pounce_prone else 'stands'}")
        if target["hp"] <= 0:
            # Non-acting unconscious character omitted by limited script.
            # No automatic arbitrary re-target or win from party down.
            log.append(f"R{rnd} frontline Dying; stop scripted exchange")
            break
        for pc in members:
            if hhp <= 0:
                break
            # Each actual own-turn Step2 restores missing HP, consuming Vigor.
            recovered = min(BUILD[pc["kind"]]["regen"],
                            pc["max_hp"] - pc["hp"], pc["vigor"])
            pc["hp"] += recovered
            pc["vigor"] -= recovered
            if recovered:
                log.append(f"R{rnd} {pc['id']} Step2 +{recovered} HP, "
                           f"-{recovered} Vigor")
            if pc["prone"]:
                # 4 MP Stand, followed by one legal head-reach Standing
                # Opportunity by the Hunter (not a free Pounce Bite).
                assert resource["movement_points"] >= 4
                pc["prone"] = False
                if opportunity_available and pc["id"] == "A1":
                    opportunity_available = False
                    opportunity_used = True
                    pc["guard_remaining"] -= 1
                    assert pc["guard_remaining"] >= 0
                    opp_total = 12 + bite["attack_roll"]["total_bonus"]
                    if opp_total > BUILD["A"]["guard"]:
                        packet = bite["primary_hp_packet"]
                        opp_damage = max(
                            0, packet["fixed_base"] + 4 -
                            max(0, BUILD["A"]["armor"] -
                                packet["armor_penetration"]))
                        pc["hp"] -= opp_damage
                        # Re-exposure cannot stack with initial accepted toxin.
                        if pc["toxin"] is None and opp_damage > 0:
                            pc["toxin"] = "Full (delayed; no instant penalty)"
                            toxin_applications += 1
                        log.append(f"R{rnd} A1 Stand 4 MP; Hunter Opportunity "
                                   f"{opp_total} vs Guard17: {opp_damage} HP")
            if pc["hp"] <= 0:
                continue
            ap = 30 + 6 * (level - 1)
            count = ap // 20  # L2 one, L3 two; no paid spell this exchange
            for die in PC_DICE[rnd][pc["id"]][:count]:
                if hhp <= 0:
                    break
                attempts = attacks + 1
                attacks += 1
                defense_now = defense["dodge_base"] - dodge_pressure
                dodge_pressure += 2  # increment on choice, including a miss
                roll = die + BUILD[pc["kind"]]["attack"]
                if die == 1 or roll <= defense_now:
                    log.append(f"R{rnd} {pc['id']} attack{attempts} "
                               f"{roll}<={defense_now} Dodge: miss")
                    continue
                assert die != 20  # no critical opportunities in this slice
                hits += 1
                dmg = max(0, BUILD[pc["kind"]]["weapon_base"] +
                          DAMAGE_DIE[rnd] -
                          max(0, defense["armor"] -
                              BUILD[pc["kind"]]["penetration"]))
                hhp -= dmg
                log.append(f"R{rnd} {pc['id']} attack{attempts} "
                           f"{roll}>{defense_now}: {dmg} HP; Hunter HP={hhp}")
        if rnd == 1:
            first_round_hunter_hp = hhp
    a1 = members[0]
    return {
        "scenario": f"L{level}-P{size}-{setup}",
        "level": level, "party_size": size, "setup": setup,
        "rounds_observed": rounds,
        "hunter_hp_at_end_r1": first_round_hunter_hp,
        "hunter_final_hp": hhp, "hunter_vigor": hvig,
        "hunter_first_zero_hp": hhp <= 0,
        "frontline_final_hp": a1["hp"],
        "frontline_vigor_remaining": a1["vigor"],
        "frontline_delayed_toxin": a1["toxin"],
        "accepted_toxin_applications": toxin_applications,
        "pounce_prone": pounce_prone,
        "standing_opportunity_used": opportunity_used,
        "pc_attacks": attacks, "pc_hits": hits,
        "log": log,
    }


def main():
    results = [simulate(level, count, setup) for level, count, setup in SCENARIOS]
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return results


if __name__ == "__main__":
    main()
