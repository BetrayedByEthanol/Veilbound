"""Isolated B04/B05 Medium Gifted Ward Conduit *design candidate*.

NOT canonical/conferred character access, not a B06 combat executor and not a
Medium Gifted L1-3 structural build. Numerical expressions await approval.
Only the existing Gifted Foundation's resources and costs are treated as canon.
"""
from dataclasses import dataclass

from scripts.b05_high_gifted_amplification_v0 import PILOT_LINKS

LEVELS = (1, 2, 3)
FORM = "Ward"
ANCHOR = "self"
EXPRESSION = {
    "Fear": ("Earth", "Fortification", "caster", "hp"),
    "Trust": ("Kinship", "Guardian", "other_ally", "vigor"),
}
PHYSICAL_HP = frozenset(("Physical", "Piercing", "Cut", "Crush"))


@dataclass
class Conduit:
    serial: int
    form: str
    anchor: str
    grade: int
    status: str = "Dormant"
    pulse_window: int = -1


class MediumGiftedWardDesign:
    """Pure proposed resource and event contract; NEVER G4 damage authority.

    An event's post-mitigation amount and actual actor identity must come
    from a future real native executor, NOT this isolated candidate model.
    """

    def __init__(self, level, *, veil_affinity=0, links=PILOT_LINKS):
        if type(level) is not int or level not in LEVELS:
            raise ValueError("Only design pilot L1-3")
        if type(veil_affinity) is not int:
            raise ValueError("Veil Affinity must be an integer")
        if links != PILOT_LINKS:
            raise ValueError("Only exact eight-link pilot authoring fixture")
        self.level = level
        self.max_vp = max(1, 4 + veil_affinity) * level
        self.available = self.max_vp
        self.committed = 0
        self.spent = 0
        self.turn_ap = 30 + 6 * (level - 1)
        self.ap = 0
        self.turn = 0
        self.window = 0
        self.emotion = None
        self.conduits = []
        self.seen_events = set()

    @property
    def slot_cap(self):
        return 1 if self.level < 3 else 2

    def check(self):
        if not ((self.ap is None or
                 (type(self.ap) is int and 0 <= self.ap <= self.turn_ap)) and
                self.available >= 0 and self.committed >= 0 and
                self.spent >= 0 and
                self.available + self.committed + self.spent == self.max_vp):
            raise AssertionError("Conduit proposal AP/VP conservation failed")
        if len(self.conduits) > self.slot_cap or any(
            c.form != FORM or c.anchor != ANCHOR or c.grade not in (1, 2, 3)
            for c in self.conduits
        ):
            raise AssertionError("Conduit proposal slot/Grade invalid")
        if sum(c.grade for c in self.conduits) != self.committed:
            raise AssertionError("Conduit proposal reservation mismatch")

    def begin_turn(self, emotion):
        """One *modeled* Step-5 window, not a general Emotion Transition rule."""
        if self.turn and self.ap is not None:
            raise ValueError("End existing modeled turn first")
        if emotion is not None and emotion not in PILOT_LINKS:
            raise ValueError("Not one of the eight authored links")
        self.turn += 1
        self.window += 1
        self.ap = self.turn_ap
        self.emotion = emotion
        self._retune()
        self.check()

    def end_turn(self):
        if self.ap is None:
            raise ValueError("No modeled turn")
        self.ap = None
        self.check()

    def first_link(self, emotion):
        """A linked-Aspect establishment within an already-open window."""
        if self.ap is None or self.turn == 0 or self.emotion is not None:
            raise ValueError("First link requires an unset live Emotion Window")
        if emotion not in PILOT_LINKS:
            raise ValueError("First link requires an authored emotion")
        self.emotion = emotion
        self._retune()  # No new window, Pulse or VP refresh.
        self.check()

    def _retune(self):
        for c in self.conduits:
            e = EXPRESSION.get(self.emotion)
            c.status = "Active" if e is not None and PILOT_LINKS[self.emotion][:2] == e[:2] else "Dormant"

    def _ready(self, ap_cost=24):
        if type(ap_cost) is not int or ap_cost <= 0:
            raise ValueError("Positive actual action AP cost required")
        if self.ap is None or self.turn == 0:
            raise ValueError("Only a live modeled own turn can commit an action")
        if self.ap < ap_cost:
            raise ValueError("Insufficient Turn AP")

    def establish(self, *, form=FORM, anchor=ANCHOR, grade):
        """PROPOSED 24-AP establishment price, plus canonical Grade VP."""
        self._ready()
        if form != FORM or anchor != ANCHOR:
            raise ValueError("No other executable Form/anchor is proposed")
        if type(grade) is not int or grade not in (1, 2, 3):
            raise ValueError("Grade I-III only")
        if len(self.conduits) >= self.slot_cap or self.available < grade:
            raise ValueError("Slot or Grade VP unavailable")
        self.ap -= 24
        self.available -= grade
        self.committed += grade
        conduit = Conduit(len(self.conduits) + 1, form, anchor, grade)
        self.conduits.append(conduit)
        self._retune()
        self.check()
        return conduit

    def reconduct_grade(self, serial, new_grade):
        """Canonical 24 AP + 3 Spent VP and grade-commitment delta.

        No refund from a downgrade can fund the *preceding* 3 Spent VP.
        Changing Grade in-window never grants a second Pulse.
        """
        self._ready()
        if type(serial) is not int or serial < 1 or serial > len(self.conduits):
            raise ValueError("Only an existing owned Conduit can be reconducted")
        if type(new_grade) is not int or new_grade not in (1, 2, 3):
            raise ValueError("Grade I-III only")
        c = self.conduits[serial - 1]
        if new_grade == c.grade:
            raise ValueError("No reconfiguration is requested")
        delta = new_grade - c.grade
        if self.available < 3 + max(0, delta):
            raise ValueError("Cannot pay the Spent surcharge and increased Grade")
        self.ap -= 24
        self.available -= 3 + delta
        self.spent += 3
        self.committed += delta
        c.grade = new_grade
        self.check()
        return c

    def spend_other_action(self, *, ap_cost=24, spent_vp=0):
        """Budget countercase only; NEVER authorizes a real magic technique."""
        self._ready(ap_cost)
        if type(spent_vp) is not int or spent_vp < 0 or self.available < spent_vp:
            raise ValueError("Unaffordable unrelated action")
        self.ap -= ap_cost
        self.available -= spent_vp
        self.spent += spent_vp
        self.check()

    def pulse(self, key, *, recipient, resource, damage_type,
              post_mitigation, adjacent=False):
        """PROPOSED first eligible post-mitigation packet, once per window.

        No attack/Guard/Dodge, free Reaction, new HP/Vigor packet, or re-roll.
        An event cannot trigger more than ONE Conduit, even at L3.
        """
        if not isinstance(key, str) or not key or key in self.seen_events:
            raise ValueError("Fresh external damage event key required")
        if (self.window == 0 or type(post_mitigation) is not int or
                post_mitigation < 0 or recipient not in ("caster", "other_ally") or
                resource not in ("hp", "vigor") or type(adjacent) is not bool):
            raise ValueError("Malformed external post-mitigation event")
        self.seen_events.add(key)
        if post_mitigation == 0:
            return 0
        for c in self.conduits:
            if c.status != "Active" or c.pulse_window == self.window:
                continue
            if self.emotion == "Fear":
                legal = (recipient == "caster" and resource == "hp"
                         and damage_type in PHYSICAL_HP)
            elif self.emotion == "Trust":
                legal = (recipient == "other_ally" and adjacent
                         and resource == "vigor" and
                         damage_type == "Direct Vigor")
            else:
                legal = False
            if legal:
                c.pulse_window = self.window
                return min(c.grade, post_mitigation)
        return 0
