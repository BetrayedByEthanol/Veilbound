"""B04/B05 — source-backed L1–3 Anointed Restoration actors for native G0.

This is an ACTOR-STATE bridge, not a native Signature/Destiny/Authority engine.
The real G0/Step-2 actor ledger is available for future integration. The
structural source has no authored mundane G5 attack profile or established
G3 technique instance, and Actor has no Anointed Destiny or Vessel ledger.
"""
from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as high_profile
from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile as medium_profile
from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile as low_profile
from scripts.b06_encounter_state_v0 import Actor, Source, _fingerprint

ROLES = {
    "AH": ("High", high_profile, "scripts/b05_high_anointed_restoration_l1_l3_v0.py"),
    "AM": ("Medium", medium_profile, "scripts/b05_medium_anointed_restoration_l1_l3_v0.py"),
    "AL": ("Low", low_profile, "scripts/b05_low_anointed_restoration_l1_l3_v0.py"),
}


def anointed_party_actor(role, level, actor_id, team, *, occupied):
    """Adapt ONE complete canon-bound character into ordinary native G0 state.

    No new technique, turn, Destiny reservoir, Invested Vessel, or free
    Signature pulse is created. Only the source's real AP/VP/HP/regen/Guard
    quantities and currently wielded physical instrument enter G0.
    """
    if role not in ROLES or type(level) is not int or level not in (1, 2, 3):
        raise ValueError("Only sourced Anointed Restoration AH/AM/AL L1–3")
    if not isinstance(actor_id, str) or not actor_id or not isinstance(team, str) or not team:
        raise ValueError("Explicit native actor and team identifiers required")
    focus, build, path = ROLES[role]
    p = build(level)
    a = p["abilities"]
    weapon = p["wielded_weapon"]
    guard_key = "sword_guard_defense" if weapon == "Sword" else "dagger_guard_defense"
    if (p["archetype"] != "Anointed" or p["focus"] != focus
            or p["bond"] != {"pillar": "Life", "aspect": "Restoration"}
            or p["resonance"] != 0 or p["known_other_aspect_techniques"]
            or p["hp_max"] != 10 + a["Vitality"]
            or p["vigor_max"] != p["hp_max"] * level
            or p["guard_capacity"] < p["physical_tempo"]
            or weapon not in ("Sword", "Dagger")
            or weapon not in p["equipment_sp"]):
        raise ValueError("Anointed G0 source profile inconsistent")
    gear = tuple(sorted(
        (name, "worn" if name == "Leather armor" else
         "wielded" if name == weapon else "carried")
        for name in p["equipment_sp"]
    ))
    source = Source(
        path, role, _fingerprint(path), "STRUCTURAL_B05_ONLY",
        tuple(sorted(a.items())), tuple(sorted(p["weapon_training"].items())),
        gear, (), f"L{level}-{focus.lower()}-anointed-restoration-structural",
    )
    actor = Actor(
        id=actor_id, team=team, source=source, level=level, focus=focus,
        initiative_bonus=p["initiative"],
        awareness=a["Awareness"], agility=a["Agility"],
        hp_max=p["hp_max"], vigor_max=p["vigor_max"], vp_max=p["vp_max"],
        hp=p["hp_max"], vigor=p["vigor_max"],
        vp_available=p["vp_max"], vp_committed=0, vp_spent=0,
        regen=p["normal_regen_throughput"],
        ap_total=p["turn_ap"], physical_ap=p["physical_action_ap"],
        projection_ap=p["projection_action_ap"],
        guard_instrument=weapon, guard_value=p[guard_key],
        guard_capacity=p["guard_capacity"],
        occupied=tuple(tuple(square) for square in occupied),
    )
    actor.validate()
    return actor
