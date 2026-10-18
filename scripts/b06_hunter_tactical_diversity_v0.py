"""B06 Phase 3: bounded, seeded *one-round* Hunter tactics/party role probes.

Uses a stable three- or four-person party: audited Low Life sword/guardian
profiles, a re-equipped/trained Low Life bow candidate, and a HIGH Scholar
Conjure Flame candidate. The latter two are NOT independently certified
complete builds. No simulated map/pathfinder, full encounter, CR or surprise.
Run: python -m scripts.b06_hunter_tactical_diversity_v0
"""
from collections import Counter
import json

from scripts.b06_hunter_party_exchanges_v0 import BUILD, HUNTER_FILE
from scripts.b06_hunter_repeated_exchanges_v0 import die

SEEDS = 128
# Four party-size/level pairs × two rosters × two encounter setups ×
# two separately staged frontline target identities = 32 cells.
CASES = tuple((level, size, roster, opening, front)
              for level in (2, 3) for size in (3, 4)
              for roster in ("original", "mixed")
              for opening in ("warned", "ambush")
              for front in ("armored", "exposed"))

# These are sourced combat *probes*, not automatically awarded player builds.
# R: A's L2/3 statistics, Talents and Low Focus retained, but L1 Sword +2
# becomes Bow +2 and gear is leather/bow/20 arrows/pack. No Guard with bow.
# F: provisional High Scholar Fire, A's 28-point Ability array, Throwing +2
# of its L1 discipline points, Conjure Flame individually known. Other known
# spells / disciplines / talents not asserted; incomplete sheet by design.
ROLE = {
    "A": {"hp": 12, "armor": 3, "vit": 2, "agi": 3, "awa": 1,
          "init": 4, "guard": 17, "guard_extra": 1, "regen": 6,
          "focus": "Low", "attack": 7, "base": 4, "die": 6, "pen": 2,
          "kind": "melee", "action_ap": 20},
    "B": {"hp": 13, "armor": 5, "vit": 3, "agi": 2, "awa": 0,
          "init": 4, "guard": 18, "guard_extra": 2, "regen": 6,
          "focus": "Low", "attack": 6, "base": 6, "die": 6, "pen": 3,
          "kind": "melee", "action_ap": 20},
    "R": {"hp": 12, "armor": 3, "vit": 2, "agi": 3, "awa": 1,
          "init": 4, "guard": None, "guard_extra": 0, "regen": 6,
          "focus": "Low", "attack": 4, "base": 2, "die": 4, "pen": 3,
          "kind": "bow", "action_ap": 20},
    "F": {"hp": 12, "armor": 3, "vit": 2, "agi": 3, "awa": 1,
          "init": 4, "guard": None, "guard_extra": 0, "regen": 3,
          "focus": "High", "attack": 5, "base": 2, "die": None,
          "pen": 0, "kind": "flame", "action_ap": 20},
}


def attack(seed, key, attacker_bonus, defense, *, packet_base,
           packet_sides, armor, penetration, burn=False):
    """One opposed direct attack; returns (HP, Vigor, hit tier).

    Bow uses d4, melee Bite/sword/mace use d6, Conjure Flame has fixed Fire2
    plus a separate Vigor packet. A hit with HP fully mitigated still triggers
    Conjure Flame's independent Vigor burn. No critical dice on Vigor.
    """
    face = die(seed, 20, *key, "attack")
    if face == 1:
        return 0, 0, "miss"
    if face == 20:
        confirm = die(seed, 20, *key, "confirm")
        tier = ("devastating" if confirm == 20 else
                "critical" if confirm != 1 and confirm + attacker_bonus > defense
                else "strong")
    elif face + attacker_bonus > defense:
        tier = "ordinary"
    else:
        return 0, 0, "miss"
    dice = 1 if tier == "strong" else 2 if tier in ("critical", "devastating") else 0
    extra = sum(die(seed, 4, *key, "critical", j) for j in range(dice))
    normal = die(seed, packet_sides, *key, "damage") if packet_sides else 0
    hp = max(0, packet_base + normal + extra - max(0, armor - penetration))
    vigor = 2 + (die(seed, 8, *key, "burn") + 2) // 3 if burn else 0
    return hp, vigor, tier


def group(size, roster):
    if (size, roster) not in ((3, "original"), (4, "original"),
                              (3, "mixed"), (4, "mixed")):
        raise ValueError("Unsupported roster")
    # ID stability means identical member rolls across paired options.
    return (("A1", "B1", "A2", "B2") if roster == "original"
            else ("B1", "R1", "F1", "A1"))[:size]


def trial(level, size, roster, opening, front, seed, hunter=None):
    if (level, size, roster, opening, front) not in CASES:
        raise ValueError("Unsupported Phase 3 tactical scenario")
    if not isinstance(seed, int) or seed < 0:
        raise ValueError("Seed must be nonnegative integer")
    hunter = hunter or json.loads(HUNTER_FILE.read_text(encoding="utf-8"))
    # Catch any later changes to the two actually audited Low Life inputs.
    for name in ("A", "B"):
        source = BUILD[name]
        for field in ("hp", "vit", "agi", "armor", "guard",
                      "guard_extra", "attack", "weapon_base",
                      "penetration", "regen", "initiative"):
            alias = {"weapon_base": "base", "penetration": "pen",
                     "initiative": "init"}.get(field, field)
            assert ROLE[name][alias] == source[field], (name, field)
    hd = hunter["defenses"]
    modes = {m["id"]: m for m in hunter["attack_profiles"]}
    assert (hd["hp_max"], hd["armor"], hd["dodge_base"]) == (14, 3, 14)
    assert modes["B06-AT-04"]["attack_roll"]["total_bonus"] == 6
    assert modes["B06-AT-06"]["linked_contest"]["total_pressure_bonus"] == 4
    assert hd["guard_instrument"] is None
    party = group(size, roster)
    front_id = ("B1" if front == "armored" else
                "A1" if roster == "original" else "F1")
    assert front_id in party
    front_stat = ROLE[front_id[0]]
    h_hp, h_vigor = 14, 42
    t_hp = front_stat["hp"]
    t_vigor = t_hp * level
    t_prone = False
    toxin = None
    vp_spent = 0
    burn_received = 0
    arrows_fired = 0
    pounce_declared = False
    balance_resolved = False
    standing_opportunities = 0
    pc_attacks = 0
    skipped_threatened_flame = 0
    front_caster_precontact_casts = 0
    front_caster_approach_mp = 0
    lane_disrupted_by = []
    # Warned begins head-adjacent. Ambush begins three legal straight
    # translations from head-forward contact; no one is threatened by the
    # Hunter until it actually completes a legal approach.
    frontal_contact = opening == "warned"
    # Contact is only sufficient to resolve Bite if a reachable head/target
    # geometry has actually been established. A non-front melee body in the
    # approach corridor requires real path/Opportunity resolution instead.
    contact_route = "warned_adjacent" if frontal_contact else None
    hunter_attack_resolution = None
    outcome = "round_one_complete"
    h_dodge = 0
    t_dodge = 0
    guard_remaining = (30 + 6 * (level - 1)) // 20 + front_stat["guard_extra"]
    participants = ("H",) + party
    initiative = {}
    for ident in participants:
        if ident == "H":
            stat = {"init": 4, "awa": 2, "agi": 2}
        else:
            stat = ROLE[ident[0]]
        initiative[ident] = (die(seed, 20, "initiative", ident) + stat["init"],
                             stat["awa"], stat["agi"])
    order = sorted(participants, key=lambda x: (
        -initiative[x][0], -initiative[x][1], -initiative[x][2],
        die(seed, 20, "tie", x)))
    hunter_first = order[0] == "H"
    # Conditional map sketch: ambush starts Hunter head=(0,0), rear=(-1,0),
    # facing east, with its standing target=(4,0); three translations put
    # head=(3,0), adjacent to target. An earlier frontal F at (4,0) is OUT
    # of Thrown Flame's 3-square range. It can use one ordinary cardinal
    # step to (3,0) (2 MP), cast back three squares at the Hunter's original
    # head, and disrupt the three-step Pounce run-up. The Hunter can still
    # approach two steps to head=(2,0) and ordinary Bite the moved F at
    # (3,0). R shoots from a separate unobstructed 7-12-square lane without
    # moving, so R's earlier attack never disrupts the Pounce corridor.
    # Melee actors' already-declared within-budget approach is modeled as
    # entering (1,0), next to the Hunter's original head. If this is the
    # front target itself, Bite can resolve in place with no Hunter movement.
    # If this is a DIFFERENT character while the front stays at (4,0),
    # the straight route is occupied and a possible detour would provoke a
    # Movement Opportunity or require a concrete Cautious route. STOP the
    # bounded trial before Hunter attacks in that case. These are explicit
    # staging contracts, NOT a general-purpose map/pathfinder.
    for ident in order:
        if ident == "H":
            # Hunter may have taken damage from higher-Initiative PCs:
            # restore only at its genuine Step 2, paying equal Vigor.
            restoration = min(4, 14 - h_hp, h_vigor)
            h_hp += restoration
            h_vigor -= restoration
            # An earlier NON-front melee attacker occupies (1,0), adjacent
            # to Hunter's head, while its declared front target stays at
            # (4,0). The Hunter cannot simply translate its 1x2 footprint
            # through the attacker and Bite the distant target. A detour's
            # legal cells, MP and possible Movement Opportunity have not
            # been authored for this bounded test: do not roll that Bite.
            nonfront_melee_blockers = [
                ident for ident in lane_disrupted_by
                if ident != front_id and ROLE[ident[0]]["kind"] == "melee"
            ]
            if opening == "ambush" and nonfront_melee_blockers:
                contact_route = "unresolved_nonfront_melee_block"
                hunter_attack_resolution = "contact_path_unresolved"
                outcome = "contact_path_unresolved"
                break
            # The lane can survive an earlier stationary bow/Flame shot:
            # initiative order alone cannot cancel Charge.
            pounce_declared = (opening == "ambush" and
                               not lane_disrupted_by)
            if pounce_declared:
                contact_route = "three_step_pounce"
                hunter_attack_resolution = "pounce"
            elif opening == "ambush":
                if front_id in lane_disrupted_by and ROLE[front_id[0]]["kind"] == "melee":
                    # The target itself approached Hunter head to (1,0):
                    # Hunter stays in place and can Bite it without exiting
                    # the original threatened square.
                    contact_route = "front_melee_adjacent"
                elif front_id in lane_disrupted_by and ROLE[front_id[0]]["kind"] == "flame":
                    # Front F moved (4,0)->(3,0); Hunter can translate
                    # head 0->1->2 with no intervening occupied cells,
                    # reaching a legal Bite at F (3,0).
                    contact_route = "two_step_front_caster"
                else:
                    # There must be a concrete route for every fallback.
                    contact_route = "unresolved_other_approach"
                    hunter_attack_resolution = "contact_path_unresolved"
                    outcome = "contact_path_unresolved"
                    break
                hunter_attack_resolution = "bite"
            else:
                contact_route = "warned_adjacent"
                hunter_attack_resolution = "bite"
            frontal_contact = True
            defense_kind = ("guard" if front_stat["guard"] is not None
                            and guard_remaining > 0 else "dodge")
            if defense_kind == "guard":
                guard_remaining -= 1
                defense = front_stat["guard"]
            else:
                defense = 10 + front_stat["agi"] + front_stat["awa"] - t_dodge
                t_dodge += 2
            dmg, _, tier = attack(seed, ("H", "bite", front_id), 6, defense,
                                   packet_base=3, packet_sides=6,
                                   armor=front_stat["armor"], penetration=1)
            t_hp -= dmg
            # Stop on damage/wound before dependent toxin and Balance.
            if t_hp <= 0:
                outcome = "frontline_first_zero"
                break
            if tier == "devastating":
                outcome = "wound_unresolved"
                break
            if dmg > 0 and toxin is None:
                resist = die(seed, 20, "H", "toxin", front_id) + front_stat["vit"]
                toxin = "reduced" if resist >= 12 else "full"
            if pounce_declared:
                balance_resolved = True
                pressure = die(seed, 20, "H", "balance_pressure") + 4
                response = (die(seed, 20, "H", "balance_defense") +
                            front_stat["agi"])
                t_prone = pressure > response
        else:
            member = ROLE[ident[0]]
            if opening == "ambush" and not frontal_contact:
                if member["kind"] == "melee":
                    # This model's side-melee action requires an ordinary
                    # forward approach into the disputed Charge corridor.
                    # A ranged R never needs that movement. Do not mark
                    # disruption if the model stops before this actor acts.
                    lane_disrupted_by.append(ident)
                    if ident == front_id:
                        # Front target walks from (4,0) into (1,0) to
                        # attack Hunter head=(0,0). No Hunter movement will
                        # be needed to Bite this target later. Keep the
                        # pre-Hunter action window open so a second moving
                        # melee actor is not silently ignored.
                        contact_route = "front_melee_adjacent"
                elif member["kind"] == "flame" and ident == front_id:
                    # Before Hunter's approach, F's initially head-forward
                    # target square is four squares away: out of Flame range.
                    # F may move one cardinal step toward the Hunter (2 MP)
                    # from (4,0) to (3,0), now at legal range 3. This
                    # occupies the last prospective Charge-head square and
                    # thus prevents the Hunter's three-step Pounce later.
                    front_caster_approach_mp += 2
                    lane_disrupted_by.append(ident)
            if ident == front_id:
                healed = min(member["regen"], member["hp"] - t_hp, t_vigor)
                t_hp += healed
                t_vigor -= healed
                if t_prone:
                    # Stand spends 4 MP; one legal Hunter Standing Opportunity
                    # resolves against STILL Prone target (+2 Bite), before
                    # the Prone state may end. Guard remains legal if held.
                    standing_opportunities += 1
                    if front_stat["guard"] is not None and guard_remaining:
                        guard_remaining -= 1
                        response_def = front_stat["guard"]
                    else:
                        response_def = (10 + front_stat["agi"] +
                                        front_stat["awa"] - t_dodge)
                        t_dodge += 2
                    dmg, _, tier = attack(
                        seed, ("H", "stand", front_id), 8, response_def,
                        packet_base=3, packet_sides=6,
                        armor=front_stat["armor"], penetration=1)
                    t_hp -= dmg
                    if t_hp <= 0:
                        outcome = "frontline_first_zero"
                        break
                    if tier == "devastating":
                        outcome = "wound_unresolved"
                        break
                    if dmg > 0 and toxin is None:
                        resist = (die(seed, 20, "H", "stand_toxin", front_id) +
                                  front_stat["vit"])
                        toxin = "reduced" if resist >= 12 else "full"
                    t_prone = False
            if ident[0] == "F" and ident == front_id and frontal_contact:
                # Already-threatened caster: this model does not grant free
                # Withdrawal or silently ignore nested Opportunities.
                # A front F who acted *before* Hunter contact instead moved
                # 2 MP to a legal 3-square range and casts normally below.
                skipped_threatened_flame += 1
                continue
            action_count = (30 + 6 * (level - 1)) // member["action_ap"]
            if member["kind"] == "flame":
                action_count = min(action_count, (6 * level - vp_spent) // 2)
            for j in range(action_count):
                pc_attacks += 1
                if member["kind"] == "bow":
                    arrows_fired += 1
                if member["kind"] == "flame":
                    vp_spent += 2  # spent on launch, including misses
                    if ident == front_id and not frontal_contact:
                        front_caster_precontact_casts += 1
                # No natural Guard for Hunter. Melee and ranged Dodge both
                # happen to start at 14 here (ranged Evasion=Tempo1−1=0).
                d = hd["dodge_base"] - h_dodge
                h_dodge += 2   # on chosen Dodge, INCLUDING misses
                dmg, burn, tier = attack(
                    seed, (ident, j, "strike"), member["attack"], d,
                    packet_base=member["base"], packet_sides=member["die"],
                    armor=(0 if member["kind"] == "flame" else hd["armor"]),
                    penetration=member["pen"], burn=member["kind"] == "flame")
                h_hp -= dmg
                h_vigor = max(0, h_vigor - burn)
                burn_received += burn
                # All HP/Vigor packets in the same hit resolve together;
                # nothing *after* the hit/wound may occur when terminal.
                if h_hp <= 0:
                    outcome = "hunter_first_zero"
                    break
                if tier == "devastating":
                    outcome = "wound_unresolved"
                    break
            if outcome != "round_one_complete":
                break
    return {
        "level": level, "size": size, "roster": roster, "opening": opening,
        "front": front, "seed": seed, "terminal": outcome,
        "hunter_first": hunter_first, "hunter_hp": h_hp, "hunter_vigor": h_vigor,
        "front_hp": t_hp, "front_vigor": t_vigor,
        "pounce_declared": pounce_declared,
        "balance_resolved": balance_resolved,
        "standing_opportunities": standing_opportunities,
        "toxin": toxin, "pc_attacks": pc_attacks,
        "arrows_fired": arrows_fired, "vp_spent": vp_spent,
        "burn_received": burn_received,
        "skipped_threatened_flame": skipped_threatened_flame,
        "frontal_contact_established": frontal_contact,
        "front_caster_precontact_casts": front_caster_precontact_casts,
        "front_caster_approach_mp": front_caster_approach_mp,
        "lane_disrupted_by": lane_disrupted_by,
        "contact_route": contact_route,
        "hunter_attack_resolution": hunter_attack_resolution,
    }


def census(seeds=SEEDS, hunter=None):
    if not isinstance(seeds, int) or seeds <= 0:
        raise ValueError("Positive seed count required")
    results = []
    for level, size, roster, opening, front in CASES:
        trials = [trial(level, size, roster, opening, front, seed, hunter=hunter)
                  for seed in range(seeds)]
        results.append({
            "scenario": (f"L{level}-P{size}-{roster}-{opening}-{front}"),
            "trials": seeds, "terminal": dict(Counter(x["terminal"] for x in trials)),
            "pounce_declared": sum(x["pounce_declared"] for x in trials),
            "balance_resolved": sum(x["balance_resolved"] for x in trials),
            "full_toxin": sum(x["toxin"] == "full" for x in trials),
            "reduced_toxin": sum(x["toxin"] == "reduced" for x in trials),
            "vp_spent": sum(x["vp_spent"] for x in trials),
            "arrows_fired": sum(x["arrows_fired"] for x in trials),
            "vigor_burn": sum(x["burn_received"] for x in trials),
            "front_caster_precontact_casts": sum(
                x["front_caster_precontact_casts"] for x in trials),
            "front_caster_approach_mp": sum(
                x["front_caster_approach_mp"] for x in trials),
            "lane_disrupted_trials": sum(
                bool(x["lane_disrupted_by"]) for x in trials),
            "contact_path_unresolved": sum(
                x["terminal"] == "contact_path_unresolved" for x in trials),
            "mean_hunter_hp": round(sum(x["hunter_hp"] for x in trials) / seeds, 3),
        })
    return results


if __name__ == "__main__":
    print(json.dumps({"seeds": SEEDS, "cases": census()}, indent=2))
