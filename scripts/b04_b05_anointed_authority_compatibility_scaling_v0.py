"""DESIGN ONLY: Anointed Authority compatibility/scaling candidates, not runtime rules.

Follows exact existing authored technique modes for comparison, but does not
create player-facing Authority permission or native encounter receipts.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from pathlib import Path

from scripts.b04_b05_anointed_authority_destiny_v0 import (
    INTENSITIES, max_normal_tier, paid_conjure, focus_three_rounds,
    max_destiny, authority_cost, load_targets,
)

ROOT = Path(__file__).resolve().parents[1]
LEVELS = (1, 3, 5, 10, 15, 20)
# Focus, Aspect, authored technique, exact profile, precise mode.
CANDIDATE_PROFILES = frozenset({
    ("High", "Conflagration", "Conjure Flame", "Thrown Projectile", "Primary"),
    ("Medium", "Conflagration", "Conjure Flame", "Weapon Enchantment", "Primary"),
    ("Low", "Conflagration", "Conjure Flame", "Weapon Enchantment", "Primary"),
    ("High", "Restoration", "Guided Regeneration", "Single Target", "Fixed"),
    ("High", "Restoration", "Guided Regeneration", "Single Target", "Maintained"),
    ("Medium", "Restoration", "Guided Regeneration", "Single Target", "Fixed"),
    ("Medium", "Restoration", "Guided Regeneration", "Single Target", "Maintained"),
    ("Low", "Restoration", "Guided Regeneration", "Self", "Fixed"),
    ("Low", "Restoration", "Guided Regeneration", "Self", "Maintained"),
})


def signature_vigor(level: int, *, scaled: bool = True) -> int:
    if type(level) is not int or not 1 <= level <= 20:
        raise ValueError("level must be 1..20")
    return 1 + level // 5 if scaled else 1


def kindled_vigor(level: int, intensity: str, *, scaled: bool = True) -> int:
    if intensity not in INTENSITIES:
        raise ValueError("unknown Authority intensity")
    # validate level unlock independently of current Destiny reserve
    authority_cost(level, intensity, max_destiny(level))
    return signature_vigor(level, scaled=scaled) + INTENSITIES[intensity][1]


def single_grade(intensities: tuple[str, ...], level: int, destiny: int) -> int:
    """Never combine Lesser+Greater to bypass Supreme, including High L5.

    High Sovereign Projection remains canonical as written, so this isolated
    no-*same-Authority-grade*-stacking proposal does not replace that feature.
    """
    if len(intensities) != 1:
        raise ValueError("only one grade of one Authority per application")
    return authority_cost(level, intensities[0], destiny)


def candidate_compatibility(focus: str, aspect: str, technique: str,
                            profile: str, mode: str, *, level: int,
                            has_bond_access: bool = True,
                            vessel_matches: bool = False,
                            weapon_wielded: bool = False,
                            recipient_self: bool = False) -> bool:
    """Design eligibility only; exact profiles and carriers, no real permission."""
    if level < 3 or level > 20 or not has_bond_access:
        return False
    key = (focus, aspect, technique, profile, mode)
    if key not in CANDIDATE_PROFILES:
        return False
    if focus == "Medium" and not vessel_matches:
        return False
    if aspect == "Conflagration" and focus in ("Low", "Medium") and not weapon_wielded:
        return False
    if focus == "Low" and aspect == "Restoration" and not recipient_self:
        return False
    return True


@dataclass(frozen=True)
class CandidateResult:
    hp_packet: int
    vigor_packet: int
    spent_vp_this_attempt: int
    required_existing_committed_vp: int
    spent_destiny: int
    used_receipts: frozenset[str]


def conjure_authority_l3(*, focus: str, level: int, tier: int,
                         destiny: int, receipt: str, used_receipts: frozenset[str],
                         roll: int, vc: int = 0, hit: bool,
                         vessel_matches: bool = False,
                         weapon_wielded: bool = False,
                         active_reserve: bool = False, committed_vp: int = 0,
                         has_bond_access: bool = True) -> CandidateResult:
    """One chosen eligible Primary hit attempt, not a persistent per-hit buff.

    T1/T2/etc obey source tier ceiling. Thrown VP is spent per cast;
    Reserved Weapon VP is precommitted at establishment, not per hit.
    Destiny is charged at the legal attempt even if it misses.
    """
    if not receipt or receipt in used_receipts:
        raise ValueError("one Authority application per distinct event receipt")
    if not 1 <= tier <= max_normal_tier(level) or not 1 <= roll <= (8 if focus == "High" else 6):
        raise ValueError("illegal tier or damage die")
    if type(vc) is not int:
        raise ValueError("invalid VC")
    profile = "Thrown Projectile" if focus == "High" else "Weapon Enchantment"
    if not candidate_compatibility(
        focus, "Conflagration", "Conjure Flame", profile, "Primary", level=level,
        vessel_matches=vessel_matches, weapon_wielded=weapon_wielded,
        has_bond_access=has_bond_access,
    ):
        raise ValueError("unapproved/unavailable candidate profile")
    if focus != "High" and (not active_reserve or committed_vp < 4 * tier):
        raise ValueError("reserved weapon must be active and fully funded")
    spent = single_grade(("lesser",), level, destiny)
    if focus == "High":
        source_vigor = 2 + math.ceil(roll * tier / 3) + max(0, vc)
        per_attempt_vp, existing_reserve = 2 * tier, 0
    else:
        source_vigor = 1 + math.ceil(roll * tier / 4) + max(0, vc)
        per_attempt_vp, existing_reserve = 0, 4 * tier
    return CandidateResult(
        hp_packet=2 if hit else 0,
        vigor_packet=(source_vigor + 3) if hit else 0,
        spent_vp_this_attempt=per_attempt_vp,
        required_existing_committed_vp=existing_reserve,
        spent_destiny=spent,
        used_receipts=used_receipts | {receipt},
    )


@dataclass(frozen=True)
class RegenerationResult:
    ordinary_hp: int
    extra_guided_hp: int
    spent_recipient_vigor: int
    remaining_vigor: int
    healed_hp: int
    spent_destiny: int
    used_receipts: frozenset[str]


def guided_regeneration_authority_l3(*, focus: str, level: int, destiny: int,
                                    missing_hp: int, recipient_vigor: int,
                                    natural_throughput: int, receipt: str,
                                    used_receipts: frozenset[str],
                                    mode: str = "Maintained", active_effect: bool = True,
                                    vessel_matches: bool = False,
                                    recipient_self: bool = False,
                                    dying: bool = False, has_bond_access: bool = True) -> RegenerationResult:
    """Pilot-only: one +1 Guided Regeneration HP step becomes Vigor-free.

    Considers only non-Dying HP regeneration, not wound allocations, other
    competing effects or a real native G4 event. Does not invent a Step.
    """
    profile = "Self" if focus == "Low" else "Single Target"
    if not candidate_compatibility(
        focus, "Restoration", "Guided Regeneration", profile, mode,
        level=level, vessel_matches=vessel_matches,
        recipient_self=recipient_self, has_bond_access=has_bond_access,
    ) or not active_effect or dying:
        raise ValueError("invalid active Guided/Focus/recipient eligibility")
    if not receipt or receipt in used_receipts:
        raise ValueError("duplicate or missing Regeneration Step receipt")
    if type(missing_hp) is not int or type(recipient_vigor) is not int or type(natural_throughput) is not int:
        raise ValueError("invalid HP/Vigor/throughput")
    if missing_hp <= 0 or recipient_vigor < 0 or natural_throughput < 0:
        raise ValueError("invalid resource state")
    # The incremental +1 throughput is eligible only if HP remains missing
    # AFTER an explicitly allocated ordinary non-Dying HP regeneration.
    ordinary = min(missing_hp, recipient_vigor, natural_throughput)
    extra = min(1, missing_hp - ordinary)
    if extra != 1:
        raise ValueError("no incremental Guided HP for Destiny to spare")
    spent = single_grade(("lesser",), level, destiny)
    return RegenerationResult(
        ordinary_hp=ordinary, extra_guided_hp=1,
        spent_recipient_vigor=ordinary,
        remaining_vigor=recipient_vigor - ordinary,
        healed_hp=ordinary + 1, spent_destiny=spent,
        used_receipts=used_receipts | {receipt},
    )


def scaling_comparison(hit_probability: float = 0.65) -> list[dict]:
    if not 0 <= hit_probability <= 1:
        raise ValueError("assumed hit probability")
    result = []
    for level in LEVELS:
        tier = max_normal_tier(level)
        paid = paid_conjure(tier)
        strength = "supreme" if level >= 10 else ("greater" if level >= 5 else "lesser")
        result.append({
            "level": level, "used_tier": tier, "vp_cost": paid["vp_cost"],
            "paid_vigor_mean_hit_vc0": paid["vigor_mean_on_hit"],
            "baseline_fixed": signature_vigor(level, scaled=False),
            "baseline_scaled": signature_vigor(level),
            "authority_strength": strength,
            "empowered_fixed": kindled_vigor(level, strength, scaled=False),
            "empowered_scaled": kindled_vigor(level, strength),
            "paid_expected_vigor": round(hit_probability * paid["vigor_mean_on_hit"], 5),
            "candidate_expected_vigor": round(hit_probability * kindled_vigor(level, strength), 5),
            "focus_envelope": {focus: focus_three_rounds(level, focus)["opportunities_per_round"]
                               for focus in ("High", "Medium", "Low")},
        })
    return result


def target_vigor_ceiling(level: int, intensity: str, target_current_vigor: int,
                         *, hit: bool = True) -> int:
    if type(target_current_vigor) is not int or target_current_vigor < 0:
        raise ValueError("target Vigor")
    return min(target_current_vigor, kindled_vigor(level, intensity)) if hit else 0


def scope_check(root: Path = ROOT) -> None:
    """Assert source-tag and mode facts; does not grant Anointed permission."""
    def read(path: str) -> str:
        return (root / path).read_text(encoding="utf-8")
    anointed = read("docs/rules/08-archetypes/anointed.md")
    fire = read("docs/rules/07-veil-magic/conjure-flame-v0.md")
    guided = read("docs/rules/07-veil-magic/guided-regeneration-v0.md")
    basic = read("docs/rules/07-veil-magic/basic-heal-v0.md")
    for expected in ("### Level 3 — Manifest Authority", "### Level 3 — Deep Channeling",
                     "### Level 3 — Incarnate Authority", "### Level 5 — Sovereign Projection"):
        assert expected in anointed, expected
    for expected in ("Thrown Projectile", "Weapon Enchantment", "F 2; V 2 + ceil(d8×T/3) + VC",
                     "F 2; V 1 + ceil(d6×T/4) + VC", "4 × T Committed VP"):
        assert expected in fire, expected
    for expected in ("Single Target", "Self", "**2 Committed VP**", "**2 ordinary Spent VP**",
                     "**+1 throughput**", "[Embodiment]"):
        assert expected in guided, expected
    assert "2 × T Spent VP" in basic


if __name__ == "__main__":
    import json
    scope_check()
    print(json.dumps({"status": "DESIGN_ONLY_NOT_NATIVE_NOT_CANONICAL",
                      "scaling": scaling_comparison(),
                      "enemy_profiles": [t.__dict__ for t in load_targets()],
                      "compatibility_candidate_count": len(CANDIDATE_PROFILES)}, indent=2))
