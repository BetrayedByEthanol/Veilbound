"""B04/B05 High Gifted isolated L1–3 Amp/Surge/miscast rules witness.

No G0 actor, live attack window, real grid, resistance, healing or wound
application is claimed. The returned disposition is a declaration/receipt for
those engines, NOT damage/target certification. No random draws are hidden.
"""
from dataclasses import dataclass

CATEGORIES = ("Potency", "Reach", "Extent", "Persistence", "Penetration", "Precision")
EMOTIONS = ("Joy", "Sadness", "Anger", "Fear", "Surprise", "Disgust", "Trust", "Anticipation")
PILOT_LINKS = {
    "Joy": ("Fire", "Conflagration", "P"),
    "Sadness": ("Life", "Restoration", "S"),
    "Anger": ("Mind", "Psionics", "P"),
    "Fear": ("Earth", "Fortification", "S"),
    "Surprise": ("Secrets", "Hallucination", "S"),
    "Disgust": ("Liberty", "Defiance", "S"),
    "Trust": ("Kinship", "Guardian", "S"),
    "Anticipation": ("Arts", "Inspiration", "S"),
}


@dataclass(frozen=True)
class Technique:
    name: str
    pillar: str
    aspect: str
    base_tier: int
    used_tier: int
    spent_vp: int
    action_ap: int
    tags: frozenset
    choices: tuple = ()
    min_range: int = 0
    max_range: int = 0
    radius: int = 0
    duration_ticks: int = 0
    attack: bool = False
    pressure: bool = False
    damage_die: int = 0
    damage_type: str = ""
    damage_resource: str = ""
    profile: str = "Primary"


@dataclass(frozen=True)
class Target:
    name: str
    distance: int
    open_path: bool = True
    eligible: bool = True


def thrown_flame(tier=1):
    """Only newly tagged Gifted Thrown Projectile Primary, not weapon modes."""
    if type(tier) is not int or tier not in (1, 2):
        raise ValueError("Only authored T1/T2 Thrown Flame")
    return Technique("Conjure Flame", "Fire", "Conflagration", 1, tier,
                     2 * tier, 20, frozenset({"Projection"}),
                     ("Potency", "Reach", "Precision"), min_range=1, max_range=3,
                     attack=True, damage_die=8, damage_type="Fire",
                     damage_resource="HP+Vigor", profile="Thrown Projectile")


def surge_surcharge(technique):
    """ceil(actual positive VP price / 4); no implicit zero-VP eligibility."""
    if type(technique.spent_vp) is not int or technique.spent_vp <= 0:
        raise ValueError("Projected Surge requires a positive authored VP price")
    if "Projection" not in technique.tags:
        raise ValueError("The exact profile lacks the [Projection] tag")
    return (technique.spent_vp + 3) // 4


def instability_dc(tier):
    if type(tier) is not int or not 0 <= tier <= 9:
        raise ValueError("Invalid Used Tier")
    return 12 + (tier + 1) // 2


def legal_target(target, technique, *, reach=False):
    return (target.eligible and target.open_path and
            technique.min_range <= target.distance <= technique.max_range + int(reach))


def choose_replacement(original, catalogue, choice_index):
    """Catalogue must be a fixed source-authored order, including original.

    A selected incompatible profile does not provoke another draw: fizzle.
    Affordability is capped by the already paid original VP and AP budgets.
    """
    eligible = tuple(p for p in catalogue
                     if p.pillar == original.pillar and p.aspect == original.aspect
                     and p.base_tier <= original.used_tier)
    if not eligible:
        return None
    if type(choice_index) is not int or not 0 <= choice_index < len(eligible):
        raise ValueError("Provide a valid recorded uniform draw for catalogue")
    return eligible[choice_index]


def miscast(roll, technique, original_target, *, other_targets=(),
            choice_index=0, catalogue=(), available_vp=0,
            committed_cast_vp=0, scatter_legal=False, extra_choices=(),
            surviving_options=(), selected_options=()):
    """Resolve one recorded d20 miscast (no rerolls/GM-created replacement).

    Returns instructions rather than applying combat packets. An independent
    native adapter must bind pre-roll targeting, cover and defenses, paid costs,
    and actual HP/Vigor on the live actor before certifying an encounter.
    """
    if type(roll) is not int or not 1 <= roll <= 20:
        raise ValueError("Miscast d20 must be 1..20")
    if type(available_vp) is not int or available_vp < 0:
        raise ValueError("Invalid unspent available VP")
    if type(committed_cast_vp) is not int or committed_cast_vp < 0:
        raise ValueError("Invalid VP-spent receipt")
    # The risky Step was attempted (and lost). Its category still counts as
    # selected for the no-duplicate-on-this-cast constraint; safe and paid
    # Surge categories survive until a specific outcome removes them.
    if (len(set(selected_options)) != len(selected_options)
            or len(set(surviving_options)) != len(surviving_options)
            or any(x not in technique.choices for x in selected_options)
            or not set(surviving_options).issubset(selected_options)):
        raise ValueError("Invalid recorded Amplification choices")
    retained_reach = "Reach" in surviving_options
    r = {"d20": roll, "status": "resolve", "target": original_target.name,
         "bonus": None, "penalty": None, "replacement": None,
         "self_damage": None, "extra_spent_vp": 0}
    def fizzle():
        r.update(status="fizzle", target=None, bonus=None, penalty=None)
    delivery_target = original_target
    delivery_technique = technique
    alternatives = tuple(t for t in other_targets if
                         t.name != original_target.name and
                         legal_target(t, technique, reach=retained_reach))
    if roll in (1, 2):
        fizzle()
        if roll == 2:
            r["bonus"] = "harmless visible same-Aspect dissipation"
    elif roll == 3:
        r["penalty"] = "remove all Amplifications (including Surge)"
        # Any previously legal distance 4 allowed solely by Reach is now
        # out of range. The miscast must not attest an impossible hit.
        if not legal_target(original_target, technique):
            fizzle()
    elif roll in (4, 5):
        if alternatives:
            if roll == 5:
                nearest = min(x.distance for x in alternatives)
                alternatives = tuple(x for x in alternatives if x.distance == nearest)
            if type(choice_index) is not int or not 0 <= choice_index < len(alternatives):
                raise ValueError("Invalid recorded target-selection die")
            delivery_target = alternatives[choice_index]
            r["target"] = delivery_target.name
    elif roll == 6:
        if scatter_legal:
            r["status"] = "scatter_pending_native_position_and_defenses"
            r["target"] = None
        # No applicable positional scatter: original effect resolves.
    elif roll == 7:
        if technique.max_range > 0:
            if original_target.distance > max(0, technique.max_range + int(retained_reach) - 1):
                fizzle()
            else:
                r["penalty"] = "range -1 square"
    elif roll == 8:
        if technique.radius > 0:
            r["penalty"] = "radius -1 square (minimum zero)"
    elif roll == 9:
        if technique.duration_ticks > 0:
            r["penalty"] = "duration halved, ceil to actual source tick"
    elif roll == 10:
        if technique.attack:
            r["penalty"] = "-2 attack roll"
    elif roll == 11:
        if technique.pressure:
            r["penalty"] = "-2 Direct Veil Pressure"
    elif roll in (12, 13):
        if technique.damage_die:
            r["penalty"] = ("one damage die minimum" if roll == 12
                            else "one damage die roll twice, take lower")
    elif roll == 14:
        r["self_damage"] = ("Vigor", "Vigor", committed_cast_vp)
    elif roll == 15:
        if not technique.damage_type:
            fizzle()
        else:
            # For a mixed HP/Vigor technique its actual primary typed HP packet.
            resource = "HP" if "HP" in technique.damage_resource else "Vigor"
            r["self_damage"] = (resource, technique.damage_type, 1)
    elif roll == 16:
        if available_vp < 1:
            fizzle()
        else:
            r["extra_spent_vp"] = 1
    elif roll == 17:
        r["bonus"] = "noticeable same-Aspect manifestation (no extra hit)"
    elif roll == 18:
        replacement = choose_replacement(technique, catalogue, choice_index)
        if (replacement is None or replacement.spent_vp > technique.spent_vp
                or replacement.action_ap > technique.action_ap
                or replacement.used_tier > technique.used_tier
                or not legal_target(
                    original_target, replacement,
                    reach=(retained_reach and replacement == technique))):
            fizzle()
        else:
            delivery_technique = replacement
            r["replacement"] = replacement.name + " / " + replacement.profile
    elif roll == 19:
        if technique.damage_die:
            r["bonus"] = "one original damage die at maximum"
    elif roll == 20:
        available = tuple(dict.fromkeys(
            x for x in extra_choices
            if x in technique.choices and x not in selected_options
        ))
        if available:
            if type(choice_index) is not int or not 0 <= choice_index < len(available):
                raise ValueError("Invalid recorded bonus-Option selection")
            r["bonus"] = available[choice_index]
    # A lost risky Reach cannot keep an illegal delivery alive. Check the
    # ACTUAL final target/profile, not just the original preflight (which
    # quite rightly allowed the attempted risky Reach). Retargeting can
    # legitimately rescue the spell if the new target is within range.
    # A Scatter still awaits native position/path/defense resolution and
    # must never claim a successful hit here.
    if r["status"] == "resolve":
        effective_reach = (retained_reach and roll != 3
                           and delivery_technique == technique)
        if not legal_target(delivery_target, delivery_technique,
                            reach=effective_reach):
            fizzle()
    return r


class HighGiftedWindow:
    """One High Gifted Emotion Window; isolated transactional resource model."""

    def __init__(self, level, emotion, *, affinity=0, initial_intensity="evoked"):
        if type(level) is not int or level not in (1, 2, 3):
            raise ValueError("L1–3 only")
        if emotion not in PILOT_LINKS:
            raise ValueError("No authored pilot emotion link")
        if initial_intensity not in ("evoked", "heightened"):
            raise ValueError("Naturally Overwhelming is not authored")
        self.level = level
        self.emotion = emotion
        self.ap = 30 + 6 * (level - 1)
        self.vp = max(1, 6 + affinity) * level
        self.spent = 0
        self.intensity = initial_intensity
        self.safe_step = int(initial_intensity == "heightened")
        self.risky_step = 0
        self.surge_allowance = 1
        self.instability_used = False
        self.deepen_used = False
        self.overload_used = False

    def deepen(self, roll, *, awareness=0, discipline=0, resonance=0):
        if self.deepen_used or self.intensity != "evoked" or self.ap < 24:
            raise ValueError("Deepen unavailable")
        if type(roll) is not int or not 1 <= roll <= 20:
            raise ValueError("Invalid check die")
        self.ap -= 24
        self.deepen_used = True
        success = roll + awareness + discipline + resonance >= 12
        if success:
            self.intensity = "heightened"
            self.safe_step = 1
        return success

    def overload(self):
        if self.overload_used or self.intensity != "heightened" or self.ap < 24:
            raise ValueError("Overload unavailable")
        self.ap -= 24
        self.overload_used = True
        self.intensity = "overwhelming"
        self.risky_step = 1

    def cast(self, technique, target, *, safe=None, risky=None, surge=None,
             instability_roll=None, control=0, discipline=0, resonance=0,
             miscast_roll=None, other_targets=(), choice_index=0,
             catalogue=(), extra_choices=(), scatter_legal=False):
        """Preflight first, then pay once and return an immutable-ish receipt.

        No action or resource rollback is possible after a severe fizzle.
        The table is called only if the rolled Instability total misses DC by 5+.
        """
        if (technique.pillar, technique.aspect) != PILOT_LINKS[self.emotion][:2]:
            raise ValueError("Active Emotion has no linked Aspect access")
        if technique.base_tier > technique.used_tier or technique.used_tier > (1 if self.level < 3 else 2):
            raise ValueError("Technique tier inaccessible")
        options = tuple(x for x in (safe, risky, surge) if x is not None)
        if len(set(options)) != len(options) or any(x not in technique.choices for x in options):
            raise ValueError("Duplicate or unauthorized Amplification")
        if safe is not None and not self.safe_step:
            raise ValueError("No Heightened Step remains")
        if risky is not None and (not self.risky_step or self.instability_used):
            raise ValueError("No Overwhelming Step or Instability check remains")
        if surge is not None and not self.surge_allowance:
            raise ValueError("Projected Surge allowance spent")
        surcharge = surge_surcharge(technique) if surge is not None else 0
        if self.ap < technique.action_ap or self.vp < technique.spent_vp + surcharge:
            raise ValueError("Unaffordable activation; no resources changed")
        if not legal_target(target, technique, reach="Reach" in options):
            raise ValueError("Original declared target illegal")
        if risky is not None:
            if type(instability_roll) is not int or not 1 <= instability_roll <= 20:
                raise ValueError("A recorded Instability d20 is required")
            deficit = instability_dc(technique.used_tier) - (instability_roll + control + discipline + resonance)
            if (deficit >= 5) != (miscast_roll is not None):
                raise ValueError("Exactly one d20 Miscast roll on severe failure")
            if miscast_roll is not None and (type(miscast_roll) is not int or not 1 <= miscast_roll <= 20):
                raise ValueError("Invalid miscast roll")
        else:
            if instability_roll is not None or miscast_roll is not None:
                raise ValueError("Instability only when risky Step is used")
            deficit = None
        # A failing optional Miscast-selection roll does not cost an action.
        # The original technique's paid resources are validated before any mutation.
        outcome = None
        if deficit is not None and deficit >= 5:
            outcome = miscast(miscast_roll, technique, target,
                              other_targets=other_targets, choice_index=choice_index,
                              catalogue=catalogue,
                              available_vp=self.vp-technique.spent_vp-surcharge,
                              committed_cast_vp=technique.spent_vp+surcharge,
                              extra_choices=extra_choices,
                              scatter_legal=scatter_legal,
                              surviving_options=tuple(x for x in (safe, surge)
                                                      if x is not None),
                              selected_options=options)
        # Mild failure loses its risky category but does not roll a miscast.
        # Resolve cannot be attested if the remaining safe/Surge categories
        # no longer support the original target's lawful delivery.
        surviving = tuple(x for x in (safe, surge) if x is not None)
        mild_fizzle = (deficit is not None and 1 <= deficit <= 4
                       and not legal_target(target, technique,
                                            reach="Reach" in surviving))
        delivery_status = (outcome["status"] if outcome is not None else
                           "fizzle" if mild_fizzle else "resolve")
        additional = outcome["extra_spent_vp"] if outcome else 0
        if additional > self.vp-technique.spent_vp-surcharge:
            raise AssertionError("Post-preflight leakage mismatch")
        self.ap -= technique.action_ap
        self.vp -= technique.spent_vp + surcharge + additional
        self.spent += technique.spent_vp + surcharge + additional
        if safe is not None:
            self.safe_step = 0
        if risky is not None:
            self.risky_step = 0
            self.instability_used = True
        if surge is not None:
            self.surge_allowance = 0
        return {"status": delivery_status, "action_ap": technique.action_ap,
                "paid_vp": technique.spent_vp+surcharge+additional,
                "surge_vp": surcharge, "options": options,
                "instability_deficit": deficit,
                "risky_step_functioned": deficit is not None and deficit <= 0,
                "miscast": outcome, "vp_remaining": self.vp,
                "ap_remaining": self.ap}


def amplified_parameters(technique, selected):
    """Provisional authored modifier preview; not a native damage application."""
    if len(set(selected)) != len(selected) or any(x not in technique.choices for x in selected):
        raise ValueError("Duplicate or unauthorized Amplification")
    if "Potency" in selected and not technique.damage_die:
        raise ValueError("Potency needs an actual damage die")
    if "Reach" in selected and not technique.max_range:
        raise ValueError("Reach needs an actual ranged delivery")
    if "Extent" in selected and not technique.radius:
        raise ValueError("Extent needs a radius")
    if "Persistence" in selected and not technique.duration_ticks:
        raise ValueError("Persistence needs a finite duration")
    if "Penetration" in selected and not technique.pressure:
        raise ValueError("Penetration needs a Direct Veil Pressure roll")
    if "Precision" in selected and not technique.attack:
        raise ValueError("Precision needs an actual attack roll")
    return {"roll_one_damage_die_twice_keep_higher": "Potency" in selected,
            "min_range": technique.min_range,
            "max_range": technique.max_range + int("Reach" in selected),
            "radius": technique.radius + int("Extent" in selected),
            "duration_ticks": technique.duration_ticks * (2 if "Persistence" in selected else 1),
            "direct_pressure_bonus": int("Penetration" in selected),
            "attack_bonus": int("Precision" in selected)}


def potency_die(first, second, sides):
    if any(type(x) is not int for x in (first, second, sides)) or sides < 1:
        raise ValueError("Invalid damage dice")
    if not (1 <= first <= sides and 1 <= second <= sides):
        raise ValueError("Die result out of bounds")
    return max(first, second)
