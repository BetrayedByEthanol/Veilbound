"""B04/B05 Low Gifted L1–3 restricted Anchor preview and pilot authority.

The original #158 +1 defense / -1 MP outputs are approved *provisionally*
for the restricted L1–3 pilot. Still not a native G0/G1/G4 effect.
Untrusted caller declarations must be independently source-attested before
this preview becomes a resolved defense or movement. No full certificate.
"""
from dataclasses import dataclass

from scripts.b05_high_gifted_amplification_v0 import PILOT_LINKS
from scripts.b05_high_gifted_l1_l3_v0 import AUTHORED_ACCESS, AUTHORED_UPCAST_T2

EMOTIONS = tuple(PILOT_LINKS)
LEVELS = (1, 2, 3)
# Exact restricted-pilot provisional numbers; no native action authorization.
CANDIDATE = {
    "Fear": {"pillar": "Earth", "aspect": "Fortification",
             "name": "Rooted Guard", "cadence": "one paid-defense Pulse/window",
             "bonus": 1},
    "Disgust": {"pillar": "Liberty", "aspect": "Defiance",
                "name": "Unbound Step", "cadence": "one paid-movement Pulse/window",
                "mp_surcharge_reduction": 1},
}


def starting_access(level, *, veil_affinity=0):
    """Pilot starting *access*, not a complete or certified character sheet.

    Ordinary techniques retain source action/VP/target/mode constraints.
    No blanket free Embodiment, tier upcast, Surge, Conduit or preparation.
    """
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only restricted L1–3 starting access")
    if type(veil_affinity) is not int:
        raise ValueError("Veil Affinity must be the actual integer Ability")
    links = {e: {"pillar": p, "aspect": a, "compatibility": rating,
                 "ordinary_techniques": list(AUTHORED_ACCESS[e]),
                 "anchor_expression_candidate":
                     CANDIDATE[e]["name"] if e in CANDIDATE else None,
                 "anchor_expression_pilot":
                     CANDIDATE[e]["name"] if e in CANDIDATE else None}
             for e, (p, a, rating) in PILOT_LINKS.items()}
    assert len(links) == 8 and len({v["pillar"] for v in links.values()}) == 8
    ap = 30 + 6 * (level-1)
    vp = max(1, 2 + veil_affinity) * level
    return {"archetype": "Gifted", "focus": "Low", "level": level,
            "links": links, "vp_max": vp, "turn_ap": ap,
            "physical_action_ap": 20, "projection_action_ap": 30,
            "general_action_ap": 24, "physical_tempo": ap // 20,
            "projection_tempo": ap // 30, "guard_capacity": ap // 20,
            "opportunity_capacity": ap // 20,
            "max_used_tier": 1 if level < 3 else 2,
            "explicit_t2_upcasts": sorted(AUTHORED_UPCAST_T2) if level == 3 else [],
            "universal_known": ["Veil Inspection"] + (["Blink"] if level == 3 else []),
            "blink_base_spent_vp": 10 if level == 3 else None,
            "blink_affordable_at_full_vp": level == 3 and vp >= 10,
            "anchor_at_start": None,
            "anchor_extra_vp_cost_candidate": 0,
            "break_anchor_general_ap": 24,
            "canonical_anchor_expression_authored": True,
            "anchor_native_effect_certified": False,
            "structural_character_build_complete": False}


@dataclass(frozen=True)
class Proposal:
    expression: str | None
    applicable: bool
    actual_action_required: bool
    bonus: int = 0
    mp_reduction: int = 0
    remaining_mp_cost: int | None = None


class LowGiftedAnchorDesign:
    """Isolated window and expense witness; NEVER commits native G0/G4.

    'actual_*' inputs are declarations supplied by an external resolution
    witness. This model neither pays real Guard/MP nor adjudicates a hit.
    """
    def __init__(self, level, *, veil_affinity=0):
        self.source = starting_access(level, veil_affinity=veil_affinity)
        self.level = level
        self.anchor = None
        self.active = None
        self.window = 0
        self.ap_remaining = 0
        self.pulse_window = None
        self.disrupted = False
        self.persisted_from_previous = False
        self.heightened = False
        # Only a successful *Settled* (0-AP) Deepen carries Heightening
        # into later unbroken Emotion Windows. A paid success is local.
        self.settled_heightening = False
        self.deepen_window = None
        self.history = []

    def _eligible_emotion(self, emotion):
        if emotion not in self.source["links"]:
            raise ValueError("Only one of the original eight linked emotions")

    def begin_window(self, *, dominant=None):
        if dominant is not None:
            self._eligible_emotion(dominant)
        if self.window > 0 and self.anchor is None:
            raise ValueError("Choose the initial Anchor in the combat-start window")
        prior = self.anchor is not None and not self.disrupted and self.active == self.anchor
        # A matching dominant emotion is not interference. In particular it
        # must not erase L3 Settled Heightening or make the next Deepen paid.
        competes = self.anchor is not None and dominant is not None and dominant != self.anchor
        self.window += 1
        self.ap_remaining = self.source["turn_ap"]
        self.persisted_from_previous = prior and not competes
        carry_settled = bool(self.level == 3 and self.persisted_from_previous
                             and self.heightened and self.settled_heightening)
        self.heightened = carry_settled
        self.settled_heightening = carry_settled
        if self.anchor is None:
            # Combat-start dominance is observed BEFORE the player chooses an
            # Anchor. The choice below, not this observation, decides whether
            # a real competing-emotion transition is required.
            self.active = dominant
            self.disrupted = False
        elif competes:
            self.disrupted = True
            self.active = dominant
            self.persisted_from_previous = False
        elif not self.disrupted:
            self.active = self.anchor
        else:
            self.active = dominant  # no free recovery of a disrupted Anchor
        self.history.append(("window", self.window, self.anchor, self.active))

    def establish_anchor(self, emotion):
        """Combat-start choice: record an Anchor even under interference.

        If a different emotion dominates, it stays Active and the chosen
        Anchor is disrupted until an independently paid, successful reassert.
        """
        self._eligible_emotion(emotion)
        if self.window != 1 or self.anchor is not None:
            raise ValueError("Initial Anchor exists only at combat start")
        dominant = self.active
        self.anchor = emotion
        self.disrupted = dominant is not None and dominant != emotion
        self.active = dominant if self.disrupted else emotion
        self.persisted_from_previous = False
        self.heightened = False
        self.settled_heightening = False
        self.history.append(("initial_anchor", self.window, emotion))
        if self.disrupted:
            self.history.append(("disruption", self.window, dominant))

    def break_anchor(self, new_emotion):
        self._eligible_emotion(new_emotion)
        if self.anchor is None or self.active != self.anchor or self.disrupted:
            raise ValueError("Cannot voluntarily break disrupted Anchor")
        if new_emotion == self.anchor:
            raise ValueError("Breaking Anchor must actually change emotion")
        if self.ap_remaining < 24:
            raise ValueError("24 General AP required before changing Anchor")
        self.ap_remaining -= 24
        self.anchor = self.active = new_emotion
        self.disrupted = False
        self.persisted_from_previous = False
        self.heightened = False
        self.settled_heightening = False
        # Do not reset pulse_window: a Break cannot mint a fresh window.
        self.history.append(("break_anchor", self.window, new_emotion, 24))

    def force_disruption(self, emotion):
        self._eligible_emotion(emotion)
        if self.anchor is None or emotion == self.anchor:
            raise ValueError("Disruption requires competing emotion")
        self.active = emotion
        self.disrupted = True
        self.persisted_from_previous = False
        self.heightened = False
        self.settled_heightening = False
        self.history.append(("disruption", self.window, emotion))

    def reassert(self, *, die, awareness, discipline, resonance=0, overwhelming=False):
        """Only a proposed paid transition; caller supplies real d20/Ability values."""
        if not self.disrupted or self.anchor is None:
            raise ValueError("No disrupted Anchor to reassert")
        if any(type(x) is not int for x in (die, awareness, discipline, resonance)) or not 1 <= die <= 20:
            raise ValueError("Exact d20 and integer source bonuses required")
        if type(overwhelming) is not bool or self.ap_remaining < 24:
            raise ValueError("Actual 24 AP transition required")
        self.ap_remaining -= 24
        success = die + awareness + discipline + resonance >= (15 if overwhelming else 12)
        if success:
            self.disrupted = False
            self.active = self.anchor
        self.history.append(("reassert", self.window, success, 24))
        return success

    def _ready(self, emotion):
        return (self.window > 0 and self.anchor == self.active == emotion
                and not self.disrupted and self.pulse_window != self.window)

    def guarded_defense(self, *, kind, paid, self_target, source_legal, physical=True):
        """Source should commit Guard/Dodge BEFORE applying proposed +1."""
        if kind not in ("guard", "dodge") or any(type(x) is not bool for x in (paid, self_target, source_legal, physical)):
            raise ValueError("Explicit boolean physical Guard/Dodge proof required")
        eligible = (self._ready("Fear") and paid and self_target and source_legal
                    and physical and (kind == "guard" or self.level >= 2))
        if eligible:
            self.pulse_window = self.window
        return Proposal("Rooted Guard" if eligible else None, eligible, True,
                        bonus=1 if eligible else 0)

    def movement_step(self, *, kind, paid, source_legal, base_mp, surcharge_mp):
        """Reduce *existing* eligible surcharge only. No movement is performed."""
        if kind not in ("normal_difficult", "cautious") or any(type(x) is not bool for x in (paid, source_legal)):
            raise ValueError("Exact normal difficult/cautious source declaration required")
        if (type(base_mp) is not int or type(surcharge_mp) is not int
                or base_mp < 1 or surcharge_mp < 0):
            raise ValueError("Finite paid MP cost and nonnegative surcharge required")
        eligible = (self._ready("Disgust") and paid and source_legal
                    and surcharge_mp > 0 and
                    (kind == "normal_difficult" or self.level >= 2))
        reduced = 1 if eligible else 0
        if eligible:
            self.pulse_window = self.window
        return Proposal("Unbound Step" if eligible else None, eligible, True,
                        mp_reduction=reduced,
                        remaining_mp_cost=base_mp + surcharge_mp - reduced)

    def deepen(self, *, die, awareness, discipline, resonance=0):
        """L3 Settled candidate uses the canonical DC12 formula; no native roll."""
        if any(type(x) is not int for x in (die, awareness, discipline, resonance)) or not 1 <= die <= 20:
            raise ValueError("Explicit d20 and integer emotional bonuses required")
        if self.anchor is None or self.active != self.anchor or self.disrupted:
            raise ValueError("Actual uninterrupted Active Anchor required")
        if self.deepen_window == self.window or self.heightened:
            raise ValueError("Deepen requires Evoked and one attempt per Emotion Window")
        cost = 0 if self.level == 3 and self.persisted_from_previous else 24
        if self.ap_remaining < cost:
            raise ValueError("Insufficient AP for canonical Deepen")
        self.ap_remaining -= cost
        self.deepen_window = self.window
        success = die + awareness + discipline + resonance >= 12
        self.heightened = success
        # A successful ordinary paid Deepen lasts in THIS window only;
        # permanent Settled persistence is earned on a successful free
        # Deepen after the same Anchor actually survived a prior window.
        self.settled_heightening = success and cost == 0
        self.history.append(("deepen", self.window, success, cost))
        return {"success": success, "ap_spent": cost,
                "settled": cost == 0}


def ordinary_cast_budget(level, emotion, technique, *, used_tier=1,
                         veil_affinity=0, available_vp=None, available_ap=None):
    """Price ONLY three source-authored profile identities, never execute them.

    External actual Active Emotion/target, Source mode and reaction checks
    remain necessary. A valid price is NOT a spell-resolution certificate.
    """
    source=starting_access(level,veil_affinity=veil_affinity)
    if emotion not in source["links"] or technique not in source["links"][emotion]["ordinary_techniques"]:
        raise ValueError("Technique requires its exact linked emotion and Aspect")
    if type(used_tier) is not int or used_tier < 1 or used_tier > source["max_used_tier"]:
        raise ValueError("Used Tier exceeds level ceiling")
    if used_tier == 2 and technique not in source["explicit_t2_upcasts"]:
        raise ValueError("Tier-2 mode was not individually authored")
    if technique in ("Conjure Flame", "Basic Heal"):
        vp, mode = 2 * used_tier, "spent"
    elif technique == "Stone Skin" and used_tier == 1:
        vp, mode = (source["vp_max"] + 2) // 3, "committed"
    else:
        raise ValueError("This witness does not authorize other technique mode prices")
    ap=source["projection_action_ap"]
    available_vp=source["vp_max"] if available_vp is None else available_vp
    available_ap=source["turn_ap"] if available_ap is None else available_ap
    if type(available_vp) is not int or type(available_ap) is not int or min(available_vp,available_ap)<0:
        raise ValueError("Finite exact AP/Available VP budget required")
    return {"affordable": available_ap>=ap and available_vp>=vp,
            "ap_required":ap,"vp_required":vp,"vp_mode":mode,
            "emotion_required":emotion,"profile_resolution_certified":False}
