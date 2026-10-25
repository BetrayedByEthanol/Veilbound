"""B05 Scholar Inward/Embodiment profile and VP-contract verification v0.

Executable planning-level source profile constraints, *not* a source-backed
L1-3 Medium/Low Scholar build, G0 combat action, or new permission granted
to another Archetype. See the paired technique-specific design record.
"""
from dataclasses import dataclass, replace
from math import ceil

# Both existing Pillar techniques require individual Scholar learning.
# These are explicitly new Scholar Focus profiles; Projection versions retain
# their own costs/targets/timing without retroactive conversion.
@dataclass(frozen=True)
class ConfigurationProfile:
    ident: str
    technique: str
    pillar: str
    aspect: str
    focus: str
    mode: str
    channel: str
    committed: int | None
    output: str

PROFILES = {
    "MS-STONE-BODY-T1": ConfigurationProfile(
        "MS-STONE-BODY-T1", "Stone Skin", "Earth", "Fortification",
        "Medium", "Inward", "Body", 1,
        "Physical/Fire/Electrical HP resistance 1; no Armor or Guard"),
    "MS-GUIDED-REGEN-T1": ConfigurationProfile(
        "MS-GUIDED-REGEN-T1", "Guided Regeneration", "Life", "Restoration",
        "Medium", "Inward", "Regeneration", 1,
        "+1 throughput only at actual own G0 Regeneration Step"),
    "LS-STONE-BODY-T1": ConfigurationProfile(
        "LS-STONE-BODY-T1", "Stone Skin", "Earth", "Fortification",
        "Low", "Embodiment", "Body", None,
        "Original Stone Skin resistance, no other activation channel"),
    "LS-GUIDED-REGEN-T1": ConfigurationProfile(
        "LS-GUIDED-REGEN-T1", "Guided Regeneration", "Life",
        "Restoration", "Low", "Embodiment", "Regeneration", 2,
        "+1 throughput only at actual own G0 Regeneration Step"),
}
TECHNIQUE_NAMES = frozenset(p.technique for p in PROFILES.values())
MEDIUM = ("MS-STONE-BODY-T1", "MS-GUIDED-REGEN-T1")
LOW = ("LS-STONE-BODY-T1", "LS-GUIDED-REGEN-T1")
KNOWN_CAP = {"Medium": (4, 5, 5), "Low": (3, 4, 4)}
PREPARED_CAP = (2, 3, 3)


def committed_cost(profile, max_vp):
    if profile.committed is not None:
        return profile.committed
    if profile.ident == "LS-STONE-BODY-T1":
        return ceil(max_vp / 3)
    raise ValueError("Unpublished commitment cost")


@dataclass(frozen=True)
class ActiveConfiguration:
    profile_id: str
    committed: int
    overroute_steps: int = 0
    intensified: bool = False


class ScholarConfigurationLedger:
    """Fail-closed *planning model* of lawful profile choices and VP/AP.

    A later source-authored M/L build must bind the original sheet, equipment,
    native G0 times and G3/G4 application. This isolated verifier cannot
    simulate actual damage, healing, movement, enemy actions or response
    windows and never declares a full executable character certificate.
    """

    def __init__(self, *, focus, level, veil_affinity, known, prepared=()):
        if focus not in KNOWN_CAP or type(level) is not int or level not in (1, 2, 3):
            raise ValueError("Only Medium/Low Scholar Level 1-3")
        if type(veil_affinity) is not int or not -2 <= veil_affinity <= 4:
            raise ValueError("Require real provisional creation-range Veil Affinity")
        if not isinstance(known, (tuple, list)) or any(
                not isinstance(x, str) for x in known):
            raise ValueError("Known Pillar techniques must be an explicit list")
        if len(set(known)) != len(known) or len(known) > KNOWN_CAP[focus][level - 1]:
            raise ValueError("Individually known repertoire over source cap")
        if any(x not in TECHNIQUE_NAMES for x in known):
            raise ValueError("Only exact authored profile-technique identities")
        if not isinstance(prepared, (tuple, list)) or any(
                not isinstance(x, str) for x in prepared):
            raise ValueError("Prepared technique identities must be explicit")
        if focus == "Medium" and prepared:
            raise ValueError("Medium ordinary repertoire has no Low prepared subset")
        if focus == "Low" and (len(set(prepared)) != len(prepared) or
                              len(prepared) > PREPARED_CAP[level - 1] or
                              not set(prepared).issubset(known)):
            raise ValueError("Low Prepared Arsenal cannot duplicate or create techniques")
        self.focus = focus
        self.level = level
        self.veil_affinity = veil_affinity
        self.known = tuple(known)
        self.prepared = tuple(prepared)
        self.max_vp = level * max(1, (4 if focus == "Medium" else 2) + veil_affinity)
        self.vp_available = self.max_vp
        self.vp_committed = 0
        self.vp_spent = 0
        self.active = None
        self.ap_remaining = 0
        self.turn_open = False
        self.round_index = 0
        self.events = []

    def _log(self, kind, **details):
        self.events.append({"kind": kind, "detail": details})

    def check(self):
        if (self.vp_available < 0 or self.vp_committed < 0 or
                self.vp_spent < 0 or
                self.vp_available + self.vp_committed + self.vp_spent != self.max_vp):
            raise AssertionError("Available + Committed + Spent VP must equal Max VP")
        if self.vp_committed != (self.active.committed if self.active else 0):
            raise AssertionError("Model commitment must be owned by active configuration")
        if self.ap_remaining < 0 or self.ap_remaining > 30 + 6 * (self.level - 1):
            raise AssertionError("Turn AP conservation failed")
        return True

    def begin_turn(self):
        if self.turn_open:
            raise ValueError("Complete previous model turn first")
        self.turn_open = True
        self.ap_remaining = 30 + 6 * (self.level - 1)
        self.round_index += 1
        # Low Stone intensification lasts only until next own turn.
        if self.active and self.focus == "Low" and self.active.intensified and (
                self.active.profile_id == "LS-STONE-BODY-T1"):
            self.active = replace(self.active, intensified=False)
            self._log("stone_intensification_expired", round=self.round_index)
        self._log("turn_started", round=self.round_index, ap=self.ap_remaining)
        self.check()

    def end_turn(self):
        self._own()
        self.turn_open = False
        self._log("turn_ended", ap_remaining=self.ap_remaining)
        self.check()

    def _own(self):
        if not self.turn_open:
            raise ValueError("Only ready own-turn configuration decisions")

    def _profile(self, ident):
        p = PROFILES.get(ident)
        if p is None or p.focus != self.focus or p.technique not in self.known:
            raise ValueError("No individually learned and compatible Focus profile")
        if self.focus == "Low" and p.technique not in self.prepared:
            raise ValueError("Low cannot activate an unprepared Embodiment")
        return p

    def _pay_spent(self, points, label):
        if type(points) is not int or points < 0 or points > self.vp_available:
            raise ValueError("Cannot pay Spent VP")
        self.vp_available -= points
        self.vp_spent += points
        if points:
            self._log("spent_vp", amount=points, label=label)

    def _commit(self, points, label):
        if type(points) is not int or points < 1 or points > self.vp_available:
            raise ValueError("Cannot commit unavailable VP")
        self.vp_available -= points
        self.vp_committed += points
        self._log("committed_vp", amount=points, label=label)

    def activate(self, ident):
        self._own()
        p = self._profile(ident)
        if self.active is not None:
            raise ValueError("One active Inward/Embodiment at L1-3")
        cost = committed_cost(p, self.max_vp)
        ap_cost = 24 if self.focus == "Medium" else 30
        if self.ap_remaining < ap_cost or self.vp_available < cost:
            raise ValueError("Insufficient Projection AP or Available VP")
        self.ap_remaining -= ap_cost
        self._log("projection_action", amount=ap_cost, technique=p.technique)
        self._commit(cost, ident)
        self.active = ActiveConfiguration(ident, cost)
        self._log("configuration_started", profile=ident, channel=p.channel)
        self.check()
        return self.active

    def _release(self, reason):
        old = self.active
        if old is None:
            raise ValueError("No active configuration")
        self.active = None
        self.vp_committed -= old.committed
        self.vp_available += old.committed
        self._log("configuration_ended", profile=old.profile_id,
                  returned=old.committed, reason=reason)
        return old

    def release(self):
        self._own()
        self._release("voluntary_release")
        self.check()

    def reroute(self, ident, *, overroute_steps=0):
        self._own()
        if self.focus != "Medium" or self.active is None:
            raise ValueError("Only Medium with a live Inward can reroute")
        p = self._profile(ident)
        old = PROFILES[self.active.profile_id]
        if ident == old.ident:
            raise ValueError("No same-profile zero-cost refresh")
        if p.channel == old.channel:
            raise ValueError("Same channel replacement needs an authored compatible distinct mode")
        if (type(overroute_steps) is not int or overroute_steps < 0 or
                overroute_steps > 2 or (overroute_steps and self.level < 3)):
            raise ValueError("Overrouting requires authored L3 capability")
        fee = (3 if self.level < 3 else 2) + overroute_steps
        cost = committed_cost(p, self.max_vp)
        if self.vp_available + self.active.committed < fee + cost:
            raise ValueError("Do not release original reservation if reroute cannot be funded")
        self._release("medium_reroute")
        self._pay_spent(fee, "medium_reroute_and_overroute")
        self._commit(cost, ident)
        self.active = ActiveConfiguration(ident, cost, overroute_steps)
        self._log("rerouted", original=old.ident, replacement=ident,
                  spent=fee, steps=overroute_steps, ap=0)
        self.check()
        return self.active

    def overroute(self, steps):
        self._own()
        if self.focus != "Medium" or self.level < 3 or self.active is None:
            raise ValueError("Only L3 Medium active Inward can Overroute")
        if type(steps) is not int or not 0 <= steps <= 2:
            raise ValueError("Maximum two Overroute steps")
        current = self.active.overroute_steps
        if steps == current:
            return self.active
        if steps < current:
            if steps != 0:
                raise ValueError("Free reduction is only to the normal Boost")
            self.active = replace(self.active, overroute_steps=0)
            self._log("overroute_dropped", from_steps=current)
        else:
            cost = steps - current
            if self.vp_available < cost:
                raise ValueError("Insufficient VP for each additional Overroute step")
            self._pay_spent(cost, "medium_overroute")
            self.active = replace(self.active, overroute_steps=steps)
            self._log("overrouted", from_steps=current, to_steps=steps)
        self.check()
        return self.active

    def intensify(self):
        self._own()
        if self.focus != "Low" or self.level < 3 or self.active is None:
            raise ValueError("Only L3 Low with an authored Embodiment can Intensify")
        if self.active.intensified:
            raise ValueError("Cannot repeatedly pay for the same active Intensification")
        if self.vp_available < 1:
            raise ValueError("Intensification requires 1 Spent VP")
        self._pay_spent(1, "low_embodiment_intensify")
        self.active = replace(self.active, intensified=True)
        self._log("intensified", profile=self.active.profile_id,
                  timing=("until_next_own_turn" if self.active.profile_id ==
                          "LS-STONE-BODY-T1" else "next_actual_self_step"))
        self.check()
        return self.active

    def model_effect(self, *, veil_control=0):
        """Prospective profile numbers only, never a delivered G4 packet."""
        if not self.active:
            return None
        if type(veil_control) is not int:
            raise ValueError("Raw VC must be independently sourced")
        p = PROFILES[self.active.profile_id]
        steps = self.active.overroute_steps
        effective_mp_cap = 6 - 2 * steps
        if steps and effective_mp_cap < 0:
            raise AssertionError("Overroute must sacrifice actual locomotion")
        if p.channel == "Body":
            resistance = (1 + steps if self.focus == "Medium" else
                          2 + max(0, veil_control)//4 +
                          int(self.active.intensified))
            return {"resistance": resistance, "regen_bonus": 0,
                    "movement_cap": effective_mp_cap}
        return {"resistance": 0,
                "regen_bonus": (1 + steps if self.focus == "Medium"
                                else 1 + int(self.active.intensified)),
                "movement_cap": effective_mp_cap}

    def consume_next_guided_step_marker(self):
        """Model-only marker: no HP gained without future actual G0 Step2."""
        if self.focus != "Low" or self.active is None or (
                self.active.profile_id != "LS-GUIDED-REGEN-T1"):
            return False
        if not self.active.intensified:
            return False
        self.active = replace(self.active, intensified=False)
        self._log("guided_intensity_marker_consumed",
                  note="Requires an independently authenticated native self Regeneration Step")
        self.check()
        return True

    def snapshot(self):
        self.check()
        return {"focus": self.focus, "level": self.level, "max_vp": self.max_vp,
                "available": self.vp_available, "committed": self.vp_committed,
                "spent": self.vp_spent, "ap_remaining": self.ap_remaining,
                "turn_open": self.turn_open,
                "active": self.active.profile_id if self.active else None,
                "overroute_steps": self.active.overroute_steps if self.active else 0,
                "intensified": self.active.intensified if self.active else False}
