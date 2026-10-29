"""NONCANONICAL B04/B05 Authority/Destiny source-parameterized balance model.

Isolated comparison only. No native G0/G4/G5 combat, no player permission,
no automatic Anointed spell acquisition or creature-difficulty certification.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
CREATURES = ROOT / "content" / "creatures"
CONJURE = ROOT / "docs/rules/07-veil-magic/conjure-flame-v0.md"
SOURCE_NAMES = (
    "b06-ordinary-human-soldier.v0.json",
    "b06-firebound-sentry.v0.json",
    "b06-hunter-of-the-woods.v0.json",
)
INTENSITIES = {"baseline": (0, 0), "lesser": (1, 3), "greater": (2, 6), "supreme": (3, 9)}
UNLOCK = {"baseline": 1, "lesser": 1, "greater": 5, "supreme": 10}
FOCUS = {
    "High": {"signature_ap": 20, "physical_ap": 30, "setup_ap": 0},
    "Medium": {"signature_ap": 24, "physical_ap": 24, "setup_ap": 24},
    "Low": {"signature_ap": 20, "physical_ap": 20, "setup_ap": 0},
}


@dataclass(frozen=True)
class Target:
    name: str
    hp_max: int
    vigor_max: int
    throughput: int
    fire_resistance: int = 0


def load_targets(root: Path = ROOT) -> tuple[Target, ...]:
    """Require actual B06 fixture values and explicit absence of Fire Resistance."""
    result = []
    for filename in SOURCE_NAMES:
        src = json.loads((root / "content/creatures" / filename).read_text(encoding="utf-8"))
        assert src["status"] == "EXECUTABLE_TEST_FIXTURE", filename
        d, r = src["defenses"], src["resources"]
        notes = d["resistance_notes"]
        assert ("No Fire Resistance" in notes
                or "No special resistance" in notes
                or "No generic toxin immunity, Fire resistance" in notes), filename
        hp, vigor, throughput = d["hp_max"], d["vigor_max"], r["natural_regeneration_throughput"]
        assert all(type(v) is int and v > 0 for v in (hp, vigor, throughput))
        assert all(s["hp"] == hp and s["vigor"] == vigor for s in r["start_states"])
        result.append(Target(src["id"], hp, vigor, throughput))
    return tuple(result)


def verify_conjure_source(root: Path = ROOT) -> None:
    doc = (root / "docs/rules/07-veil-magic/conjure-flame-v0.md").read_text(encoding="utf-8")
    for literal in ("F 2; V 2 + ceil(d8×T/3) + VC", "2 × T Spent VP",
                    "One Projection Action", "Fire Resistance"):
        assert literal in doc, literal


def paid_conjure(tier: int, vc: int = 0) -> dict:
    if type(tier) is not int or not 1 <= tier <= 9 or type(vc) is not int:
        raise ValueError("invalid tier/VC")
    rolls = [2 + math.ceil(face * tier / 3) + max(0, vc) for face in range(1, 9)]
    return {"fire_hp": 2, "vigor_mean_on_hit": sum(rolls) / 8,
            "vigor_min": min(rolls), "vigor_max": max(rolls), "vp_cost": 2 * tier}


def max_normal_tier(level: int) -> int:
    if not 1 <= level <= 20:
        raise ValueError("level")
    return min(9, (level + 1) // 2)


def max_destiny(level: int, high_l4_bonus: bool = False) -> int:
    if not 1 <= level <= 20:
        raise ValueError("level")
    # Excludes separately unapproved High L4 bonus by default.
    return 2 + level // 5 + (int(high_l4_bonus) if level >= 4 else 0)


def destiny_recovery(level: int, high_l4_bonus: bool = False) -> int:
    # 25% rounded half up (integer arithmetic), minimum 1.
    return max(1, (max_destiny(level, high_l4_bonus) + 2) // 4)


def recovery_after_elapsed(level: int, current: int, completed_hours: int,
                           high_l4_bonus: bool = False) -> int:
    maximum = max_destiny(level, high_l4_bonus)
    if not 0 <= current <= maximum or completed_hours < 0:
        raise ValueError("invalid Destiny state")
    return min(maximum, current + completed_hours // 6 * destiny_recovery(level, high_l4_bonus))


def significant_mission_event(level: int, current: int, recognized: bool,
                              event_id: str, previous_ids: frozenset[str]):
    """GM-recognized single meaningful story event, not a Mission milestone."""
    maximum = max_destiny(level)
    if not event_id or not event_id.strip() or not 0 <= current <= maximum:
        raise ValueError("invalid mission event")
    if not recognized or event_id in previous_ids:
        return current, previous_ids
    return min(maximum, current + 1), previous_ids | {event_id}


def authority_cost(level: int, intensity: str, current_destiny: int) -> int:
    if intensity not in INTENSITIES or level < UNLOCK[intensity] or level > 20:
        raise ValueError("unknown or locked intensity")
    if not 0 <= current_destiny <= max_destiny(level):
        raise ValueError("invalid Destiny")
    cost = INTENSITIES[intensity][0]
    if current_destiny < cost:
        raise ValueError("insufficient Destiny")
    return cost


def spend_for_authority_attempt(level: int, intensity: str, current_destiny: int,
                                *, legal_application: bool) -> int:
    """Actual eligible attempt spends even when it misses, not on early interruption."""
    cost = authority_cost(level, intensity, current_destiny)
    return current_destiny - cost if legal_application else current_destiny


def one_hit(target: Target, intensity: str, model: str, vigor_before: int,
            *, hp_before: int | None = None, hit: bool = True) -> dict:
    """One assumed attempt and the target's next existing regeneration Step.

    Burn: Fire HP1, Vigor 1+3*n. Interference: Fire HP1, Vigor1, and
    one-time next-step throughput reduction n. No native attacker/defender
    response, crit, wound, death or full encounter replay. Stop at HP<=0.
    """
    if intensity not in INTENSITIES or model not in ("burn", "interference"):
        raise ValueError("unknown model")
    if not 0 <= vigor_before <= target.vigor_max:
        raise ValueError("invalid Vigor")
    if hp_before is None:
        hp_before = target.hp_max - 5
    if not 1 <= hp_before <= target.hp_max:
        raise ValueError("positive-HP witness only")
    n = INTENSITIES[intensity][0]
    fire_hp = max(0, 1 - target.fire_resistance) if hit else 0
    vigor_packet = (1 + 3 * n) if model == "burn" else 1
    burned = min(vigor_before, vigor_packet) if hit else 0
    after_hp = hp_before - fire_hp
    after_vigor = vigor_before - burned
    base = {"hp_after_hit": after_hp, "vigor_after_hit": after_vigor,
            "vigor_burned": burned, "hp_fire_packet": fire_hp}
    if after_hp <= 0:
        return {**base, "needs_native_dying_wound_resolution": True}
    throughput = max(0, target.throughput - (n if model == "interference" and hit else 0))
    regenerated = min(throughput, target.hp_max - after_hp, after_vigor)
    return {**base, "regeneration_restored": regenerated,
            "hp_after_step": after_hp + regenerated,
            "vigor_after_step": after_vigor - regenerated,
            "effective_throughput": throughput,
            "needs_native_dying_wound_resolution": False}


def focus_three_rounds(level: int, focus: str, starting_destiny: int | None = None) -> dict:
    """Illustrative AP opportunity envelope, not a legal Anointed combat build."""
    if focus not in FOCUS or not 1 <= level <= 20:
        raise ValueError("invalid level/Focus")
    ap = min(120, 30 + 6 * (level - 1))
    cfg = FOCUS[focus]
    opportunities, spent_ap = [], []
    for rnd in range(1, 4):
        setup = cfg["setup_ap"] if focus == "Medium" and rnd == 1 else 0
        remain = ap - setup
        count = remain // cfg["signature_ap"] if focus == "High" else int(remain >= cfg["physical_ap"])
        opportunities.append(count)
        spent_ap.append(setup + count * cfg["signature_ap"])
    maximum = max_destiny(level)
    points = maximum if starting_destiny is None else starting_destiny
    if not 0 <= points <= maximum:
        raise ValueError("invalid available Destiny")
    return {"focus": focus, "level": level, "turn_ap": ap,
            "opportunities_per_round": opportunities,
            "ap_committed_for_signature_opportunities": spent_ap,
            "max_burn_authority_attempts_at_1_destiny": min(sum(opportunities), points),
            "vessel_count": int(focus == "Medium"),
            "additional_physical_attacks_granted": 0,
            "note": "No authored Anointed attack, delivery or full native character implied"}


def compare(hit_chance: float = 0.65, root: Path = ROOT) -> dict:
    if not 0 <= hit_chance <= 1:
        raise ValueError("invalid assumed hit probability")
    verify_conjure_source(root)
    targets = load_targets(root)
    paid = []
    for level in (1, 3, 5, 10, 20):
        tier = max_normal_tier(level)
        row = paid_conjure(tier)
        paid.append({**row, "level": level, "tier": tier,
                     "expected_vigor_dmg_per_attack": row["vigor_mean_on_hit"] * hit_chance,
                     "expected_fire_hp_per_attack": 2 * hit_chance})
    focus = [focus_three_rounds(level, name) for level in (1, 3, 5, 10, 20)
             for name in ("High", "Medium", "Low")]
    scenarios = []
    for target in targets:
        for vigor in (0, 1, 4, target.vigor_max):
            for intensity in INTENSITIES:
                for model in ("burn", "interference"):
                    scenarios.append({"target": target.name, "vigor_before": vigor,
                                      "intensity": intensity, "model": model,
                                      **one_hit(target, intensity, model, vigor)})
    return {"status": "DESIGN_ONLY_NOT_NATIVE_NOT_CANONICAL",
            "candidate_signature": {"fire_hp_on_hit": 1, "vigor_on_hit": 1, "vp": 0,
                                    "authority_additional_vigor": [3, 6, 9],
                                    "destiny_costs": [1, 2, 3], "unlocks": [1, 5, 10],
                                    "authority_declared_and_charged_on_legal_attempt_even_if_miss": True},
            "hit_probability_assumption": hit_chance,
            "source_target_profiles": [t.__dict__ for t in targets],
            "conjure_flame_reference": paid, "focus_opportunities": focus,
            "single_hit_next_regeneration_step": scenarios,
            "boundaries": ["not native", "no real attack/response rolls",
                           "no native wound/Dying adjudication", "no L1–3 Anointed build",
                           "no Medium/Low extra attacks", "no automatic ordinary-technique Authority"]}


if __name__ == "__main__":
    print(json.dumps(compare(), indent=2, sort_keys=True))
