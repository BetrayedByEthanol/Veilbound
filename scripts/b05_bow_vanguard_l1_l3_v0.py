"""B05/B07: source-bound L1-3 Low Life Priest Bow Vanguard character fixture.

A variant of audited Restorative Vanguard A: the two starting Sword
Training points go to Bows instead; all underlying Talent, Discipline,
Prayer, Ability, and regeneration choices remain intact. This is a legal
*structural sheet*, not a new Archetype or encounter/CR certification.
No combat algorithm, movement pathfinding, or free bow Guard is provided.

Run: python -m scripts.b05_bow_vanguard_l1_l3_v0
"""
import json

LEVELS = (1, 2, 3)
ABILITY_ORDER = ("Strength", "Agility", "Precision", "Intellect", "Awareness",
                 "Presence", "Vitality", "Veil Affinity", "Veil Control")
ABILITIES = dict(zip(ABILITY_ORDER, (2, 3, 0, 0, 1, -2, 2, 0, 0)))
ABILITY_COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
START_DISCIPLINES = {
    "Veil Theory": 2, "Life Pillar Lore": 2,
    "Medicine": 2, "Acrobatics": 2,
}
GEAR_SP = {
    "Leather armor": 25, "Bow": 26, "20 arrows": 5,
    "Dagger": 4, "Adventuring pack": 8,
}
TALENTS = {
    1: "TAL-C02 Enhanced Regeneration",
    2: "TAL-C05 Guard Reserve",
    3: "TAL-C10 Emergency Regeneration",
}
PRAYERS = {
    1: ("Guided Regeneration", "Basic Heal"),
    2: ("Guided Regeneration", "Basic Heal", "Woodland Rapport"),
    3: ("Guided Regeneration", "Basic Heal", "Woodland Rapport"),
}
SOURCE_PROFILE = "R"  # scripts.b06_hunter_tactical_diversity_v0.ROLE
STARTING_SILVER = 150
STARTING_ARROWS = 20
BOW_TRAINING = 2
SMALL_BLADES_TRAINING = 0


def profile(level):
    """Return an independently inspectable, complete chosen v0 ledger."""
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only integer character levels 1, 2, 3 are authored")
    ab = ABILITIES
    strength, agility, precision = (ab[k] for k in
                                    ("Strength", "Agility", "Precision"))
    vitality, awareness, va = (ab[k] for k in
                               ("Vitality", "Awareness", "Veil Affinity"))
    turn_ap = 30 + 6 * (level - 1)
    physical_cost, projection_cost, general_cost = 20, 30, 24
    physical_tempo, projection_tempo = (
        turn_ap // physical_cost, turn_ap // projection_cost)
    max_hp = 10 + vitality
    return {
        "identity": "Bow Vanguard — Restorative Vanguard A training/equipment variant",
        "level": level, "archetype": "Priest", "focus": "Low",
        "pillar": "Life", "pillar_accord": 1, "resonance": 0,
        "abilities": dict(ab),
        "ability_points": sum(ABILITY_COST[k] for k in ab.values()),
        "weapon_training": {"Bows": BOW_TRAINING},
        "weapon_development_points": 2,
        "learned_disciplines": {
            **START_DISCIPLINES, **({"Survival": 1} if level >= 2 else {})
        },
        "learned_points": 8 + (level >= 2),
        "background_familiarities": [
            "Home community", "Prior rural medical practice"],
        "talents": [v for k, v in TALENTS.items() if k <= level],
        "prepared_prayers": list(PRAYERS[level]),
        "chosen_devotion": "Guided Regeneration",
        "max_prepared_prayers": (1 if level == 1 else 2) + 1,
        "universal": (["Veil Inspection", "Blink"] if level >= 3
                      else ["Veil Inspection"]),
        "silver_budget": STARTING_SILVER,
        "equipment_sp": dict(GEAR_SP),
        "silver_spent": sum(GEAR_SP.values()),
        "silver_remaining": STARTING_SILVER - sum(GEAR_SP.values()),
        "initial_arrows": STARTING_ARROWS,
        "hp_max": max_hp,
        "vigor_max": max_hp * level,
        "vp_max": max(1, 2 + va) * level,
        "turn_ap": turn_ap, "physical_action_ap": physical_cost,
        "projection_action_ap": projection_cost,
        "general_action_ap": general_cost,
        "physical_tempo": physical_tempo,
        "projection_tempo": projection_tempo,
        "normal_guard_capacity": physical_tempo + (1 if level >= 2 else 0),
        "bow_guard": None,  # not Guard-capable, even with Guard Reserve
        "dagger_guard_if_wielded": 10 + agility + precision +
                                  SMALL_BLADES_TRAINING,
        "first_dodge": 10 + min(agility, 4) + awareness,
        "ranged_evasion_bonus": physical_tempo - 1,
        "initiative": agility + awareness,
        "movement_points": 12,
        "bow_attack_bonus": strength + precision + BOW_TRAINING,
        "bow_damage": "2+d4 Piercing",
        "bow_penetration": 3,
        "bow_shots_per_pure_physical_turn": physical_tempo,
        "dagger_attack_bonus": agility + precision + SMALL_BLADES_TRAINING,
        "dagger_damage": f"{2 + max(0, strength) // 2}+d4 Cut/Pierce",
        "dagger_penetration": 0,
        "normal_regen_throughput": max(0, vitality) + 3 + 1,
        "regen_with_active_chosen_guided": max(0, vitality) + 3 + 1 + 1,
        "chosen_maintained_guided_committed_vp": 1,
        "ordinary_basic_heal_t1_spent_vp": 2,
        "ordinary_woodland_rapport_t1_spent_vp": 2,
        "full_normal_bow_turn_shots": turn_ap // physical_cost,
        "aim_then_shoot_same_turn": physical_cost * 2 <= turn_ap,
        "shot_then_project_same_turn": physical_cost + projection_cost <= turn_ap,
        "blink_usable_from_fresh_full_vp": level >= 3 and
                                            max(1, 2 + va) * level >= 10,
    }


def verify():
    """Check local ledger conservation and B06 R-role compatibility."""
    from scripts.b06_hunter_tactical_diversity_v0 import ROLE

    assert sum(ABILITY_COST[v] for v in ABILITIES.values()) == 28
    assert sum(START_DISCIPLINES.values()) == 8
    assert sum(GEAR_SP.values()) == 68
    for level in LEVELS:
        p = profile(level)
        assert p["ability_points"] == 28
        assert p["learned_points"] == sum(p["learned_disciplines"].values())
        assert all(0 <= v <= 2 for v in p["learned_disciplines"].values())
        assert p["weapon_development_points"] == sum(
            p["weapon_training"].values())
        assert p["silver_spent"] + p["silver_remaining"] == STARTING_SILVER
        assert len(p["talents"]) == level
        assert len(p["prepared_prayers"]) == p["max_prepared_prayers"]
        assert p["bow_guard"] is None
        assert p["physical_tempo"] == p["turn_ap"] // 20
        assert p["projection_tempo"] == p["turn_ap"] // 30
        assert p["vp_max"] == 2 * level
        assert p["vigor_max"] == 12 * level
        assert not p["shot_then_project_same_turn"]
        if level == 3:
            assert p["blink_usable_from_fresh_full_vp"] is False
        if level in (2, 3):
            role = ROLE[SOURCE_PROFILE]
            for sheet_key, source_key in (
                    ("hp_max", "hp"), ("bow_attack_bonus", "attack"),
                    ("bow_penetration", "pen"),
                    ("normal_regen_throughput", "regen"),
                    ("initiative", "init")):
                assert p[sheet_key] == role[source_key], sheet_key
            assert p["first_dodge"] == 14
            assert (role["armor"], role["base"], role["die"],
                    role["kind"], role["action_ap"], role["guard"]) == (
                        3, 2, 4, "bow", 20, None)
    return True


if __name__ == "__main__":
    verify()
    print(json.dumps({"build": "Bow Vanguard v0",
                      "levels": [profile(level) for level in LEVELS]},
                     indent=2, sort_keys=True, ensure_ascii=False))
