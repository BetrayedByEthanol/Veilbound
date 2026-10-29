"""Executable isolated L1-3 Anointed Signature/Destiny authority referee.

This is a first-class *bounded* rules implementation, not a native G0 action or
G4 wound bridge. Caller supplies authenticated legal action/turn/step, defense,
Intrusion and active-technique receipts; this module MUST NOT certify those.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Literal

Focus = Literal["High", "Medium", "Low"]
Aspect = Literal["Restoration", "Conflagration"]


@dataclass(frozen=True)
class Anointed:
    level: int
    focus: Focus
    aspect: Aspect
    destiny: int = 2
    six_hour_remainder_minutes: int = 0
    mission_awards: frozenset[str] = frozenset()
    used_receipts: frozenset[str] = frozenset()
    used_focus_turns: frozenset[str] = frozenset()
    invested_vessel: str | None = None
    active_bond: bool = True
    embodied: bool = True

    def __post_init__(self):
        if type(self.level) is not int or not 1 <= self.level <= 3:
            raise ValueError("L1-3 only; no automatic higher-level mechanics")
        if self.focus not in ("High", "Medium", "Low") or self.aspect not in ("Restoration", "Conflagration"):
            raise ValueError("only the two explicitly authored pilot Aspects/Focuses")
        if type(self.destiny) is not int or not 0 <= self.destiny <= 2:
            raise ValueError("Destiny out of L1-3 range")
        if not 0 <= self.six_hour_remainder_minutes < 360:
            raise ValueError("elapsed remainder")
        if self.focus != "Medium" and self.invested_vessel is not None:
            raise ValueError("only Medium may invest")


def recover_destiny(actor: Anointed, elapsed_minutes: int) -> Anointed:
    """Completed 6-hour in-world intervals only, retaining partial time."""
    if type(elapsed_minutes) is not int or elapsed_minutes < 0:
        raise ValueError("elapsed time must be a nonnegative integer minute count")
    if not actor.active_bond:
        return actor  # Dormant time does not accumulate toward Destiny recovery.
    total = actor.six_hour_remainder_minutes + elapsed_minutes
    return replace(actor, destiny=min(2, actor.destiny + total // 360),
                   six_hour_remainder_minutes=total % 360)


def mission_event(actor: Anointed, event_id: str, *, gm_recognized: bool) -> Anointed:
    """One GM-recognized significant event, not routine actions or quest milestones."""
    if not event_id or not event_id.strip():
        raise ValueError("unique significant story event identifier required")
    if not gm_recognized or not actor.active_bond or event_id in actor.mission_awards:
        return actor
    return replace(actor, destiny=min(2, actor.destiny + 1),
                   mission_awards=actor.mission_awards | {event_id})


def set_bond(actor: Anointed, *, active: bool) -> Anointed:
    """External mission-state adjudication is authoritative; no automated morality."""
    return replace(actor, active_bond=bool(active),
                   invested_vessel=actor.invested_vessel if active else None,
                   embodied=actor.embodied if active else False)


def set_embodiment(actor: Anointed, *, manifested: bool, at_own_turn_start: bool) -> Anointed:
    """Low Anointed suppress/resume only at normal start-of-own-turn timing."""
    if actor.focus != "Low" or not actor.active_bond or not at_own_turn_start:
        raise ValueError("illegal Embodiment toggle")
    return replace(actor, embodied=bool(manifested))


def invest(actor: Anointed, vessel_id: str, *, ap_available: int,
           legal_vessel: bool, consent_or_other_delivery_valid: bool) -> tuple[Anointed, int]:
    if (not actor.active_bond or actor.focus != "Medium" or not vessel_id
            or not legal_vessel or not consent_or_other_delivery_valid
            or type(ap_available) is not int or ap_available < 24):
        raise ValueError("illegal Medium Investment")
    return replace(actor, invested_vessel=vessel_id), 24


def _commit(actor: Anointed, receipt: str, *, lesser: bool,
            focus_turn_id: str | None = None) -> Anointed:
    if not actor.active_bond:
        raise ValueError("Forsaken/Dormant bond cannot use Signature or Authority")
    if not receipt or receipt in actor.used_receipts:
        raise ValueError("missing or replayed application receipt")
    if focus_turn_id is not None and (not focus_turn_id or focus_turn_id in actor.used_focus_turns):
        raise ValueError("only one invested/embodied Signature pulse per own turn")
    if lesser and actor.destiny < 1:
        raise ValueError("insufficient Destiny")
    return replace(actor, destiny=actor.destiny - int(lesser),
                   used_receipts=actor.used_receipts | {receipt},
                   used_focus_turns=actor.used_focus_turns | ({focus_turn_id} if focus_turn_id else set()))


@dataclass(frozen=True)
class SignatureOutcome:
    actor: Anointed
    ap_spent: int
    hp_restored: int = 0
    recipient_vigor_spent: int = 0
    fire_hp_packet: int = 0
    vigor_damage_packet: int = 0
    requires_native_dying_bridge: bool = False


def returning_step(actor: Anointed, *, receipt: str, target_id: str,
                   recipient_hp: int, recipient_max_hp: int, recipient_vigor: int,
                   lesser: bool = False, ap_available: int = 0,
                   distance: int = 0, path_visible: bool = True,
                   beneficial_intrusion_legal: bool = True,
                   intrusion_succeeded: bool = True,
                   authenticated_regeneration_step: bool = False,
                   focus_turn_id: str | None = None,
                   recipient_living: bool = True) -> SignatureOutcome:
    """One positive-HP living-target conversion; never Dying or wound repair."""
    if actor.aspect != "Restoration" or not target_id or not actor.active_bond:
        raise ValueError("invalid bonded Aspect/target")
    if (not recipient_living or type(recipient_hp) is not int or
            type(recipient_max_hp) is not int or type(recipient_vigor) is not int or
            recipient_hp <= 0 or recipient_max_hp < recipient_hp or recipient_vigor < 0 or
            recipient_hp == recipient_max_hp or not beneficial_intrusion_legal):
        raise ValueError("requires positive HP, missing HP, resolved Intrusion legality")
    if (type(distance) is not int or distance < 0 or
            distance > (4 if actor.focus == "High" and actor.level >= 2 else 3) or
            (actor.focus == "Low" and distance != 0) or not path_visible):
        raise ValueError("illegal path/range")
    if actor.focus == "High":
        if type(ap_available) is not int or ap_available < 20:
            raise ValueError("High Projection requires 20 AP")
        cap, cost, one_turn = 2, 20, None
    elif actor.focus == "Medium":
        if actor.invested_vessel != target_id or not authenticated_regeneration_step or not focus_turn_id:
            raise ValueError("requires valid invested patient's existing Regeneration Step")
        cap, cost, one_turn = 1, 0, "restoration-medium:"+focus_turn_id
    else:
        if not actor.embodied or target_id != "self" or not authenticated_regeneration_step or not focus_turn_id:
            raise ValueError("Low self Signature requires own existing Regeneration Step")
        cap, cost, one_turn = 1, 0, "restoration-low:"+focus_turn_id
    amount = min(cap, recipient_max_hp-recipient_hp,
                 recipient_max_hp if lesser else recipient_vigor)
    if amount == 0:
        raise ValueError("normal Signature cannot restore HP without Vigor")
    new_actor = _commit(actor, receipt, lesser=lesser, focus_turn_id=one_turn)
    # A genuinely legal beneficial Intrusion with a valid target may still be
    # consciously resisted. Such an application spends Destiny on the attempt;
    # an externally resolved successful contest is needed to apply HP/Vigor.
    if not intrusion_succeeded:
        return SignatureOutcome(actor=new_actor, ap_spent=cost)
    return SignatureOutcome(actor=new_actor, ap_spent=cost, hp_restored=amount,
                            recipient_vigor_spent=0 if lesser else amount)


def kindled_flame(actor: Anointed, *, receipt: str, hit: bool,
                  target_vigor: int, target_hp: int, fire_resistance: int = 0,
                  lesser: bool = False, ap_available: int = 0,
                  distance: int = 1, path_visible: bool = True,
                  carrier_attack_authentic: bool = False,
                  target_legal: bool = True, turn_id: str | None = None,
                  invested_weapon_id: str | None = None,
                  active_wielded_weapon_id: str | None = None) -> SignatureOutcome:
    """One separately defended on-hit packet; externally authenticated hit.

    Carries no implicit weapon damage, critical dice, second attack, Ignite,
    environmental accumulation, or extra G0 event. Caller resolves wound/Dying.
    """
    if actor.aspect != "Conflagration" or not actor.active_bond or not target_legal:
        raise ValueError("invalid target or bonded Aspect")
    if any(type(v) is not int or v < 0 for v in (target_vigor, fire_resistance)) or type(target_hp) is not int:
        raise ValueError("invalid resource inputs")
    if actor.focus == "High":
        if (type(ap_available) is not int or ap_available < 20 or type(distance) is not int
                or not 1 <= distance <= (4 if actor.level >= 2 else 3) or not path_visible):
            raise ValueError("High projectile requires paid 20-AP legal path/range")
        cost, turn_slot = 20, None
    elif actor.focus == "Medium":
        if (not carrier_attack_authentic or not turn_id or not invested_weapon_id
                or actor.invested_vessel != invested_weapon_id
                or active_wielded_weapon_id != invested_weapon_id):
            raise ValueError("Medium needs one actually paid invested-weapon attack")
        cost, turn_slot = 0, "conflagration-medium:"+turn_id
    else:
        if (not actor.embodied or not carrier_attack_authentic or not turn_id
                or not active_wielded_weapon_id):
            raise ValueError("Low needs one paid own-turn wielded-weapon attack")
        cost, turn_slot = 0, "conflagration-low:"+turn_id
    updated = _commit(actor, receipt, lesser=lesser, focus_turn_id=turn_slot)
    # 1 Fire HP and 1 Vigor on legal hit. L1-3 scaling is fixed: the L5
    # candidate level-scaling formula is not yet canonical.
    fire = max(0, 1-fire_resistance) if hit else 0
    vigor = min(target_vigor, 1 + (3 if lesser else 0)) if hit else 0
    return SignatureOutcome(actor=updated, ap_spent=cost,
                            fire_hp_packet=fire, vigor_damage_packet=vigor,
                            requires_native_dying_bridge=bool(hit and target_hp - fire <= 0))


@dataclass(frozen=True)
class TechniqueAuthorityOutcome:
    actor: Anointed
    additional_vigor_damage: int = 0
    additional_hp_without_vigor: int = 0
    spent_vp_this_attempt: int = 0
    required_existing_committed_vp: int = 0


def conjure_flame_l3(actor: Anointed, *, receipt: str, profile: str,
                     used_tier: int, hit: bool, target_vigor_after_base: int,
                     adequate_spent_vp: bool = False,
                     active_reserve: bool = False, reserved_vp: int = 0,
                     vessel_weapon_matches: bool = False, weapon_wielded: bool = False,
                     authentic_paid_attack: bool = False) -> TechniqueAuthorityOutcome:
    """L3 Lesser attachment to an independently paid/committed legal Primary.

    The native technique resolves its own HP/Vigor; this returns only extra
    Vigor and preserves its once-per-attempt Destiny charge on a miss.
    """
    if actor.level < 3 or actor.aspect != "Conflagration" or not actor.active_bond:
        raise ValueError("not an eligible L3 Fire Anointed")
    if type(used_tier) is not int or not 1 <= used_tier <= 2 or target_vigor_after_base < 0:
        raise ValueError("L3 tier/resource restriction")
    if actor.focus == "High":
        if profile != "Thrown Projectile" or not adequate_spent_vp or not authentic_paid_attack:
            raise ValueError("High requires legal paid Primary projectile")
        required_vp, committed = 2*used_tier, 0
    else:
        if (profile != "Weapon Enchantment" or not authentic_paid_attack
                or not active_reserve or not weapon_wielded or reserved_vp < 4*used_tier
                or (actor.focus == "Medium" and (actor.invested_vessel is None or not vessel_weapon_matches))):
            raise ValueError("Medium/Low require one legal paid active Reserved Weapon hit")
        required_vp, committed = 0, 4*used_tier
    updated = _commit(actor, receipt, lesser=True)
    return TechniqueAuthorityOutcome(updated,
        additional_vigor_damage=min(target_vigor_after_base, 3) if hit else 0,
        spent_vp_this_attempt=required_vp, required_existing_committed_vp=committed)


def guided_regeneration_l3(actor: Anointed, *, receipt: str,
                           recipient_missing_hp_after_ordinary: int,
                           active_paid_guided_instance: bool,
                           mode: str, profile: str,
                           authenticated_regeneration_step: bool,
                           vessel_matches: bool = False,
                           recipient_self: bool = False,
                           recipient_dying: bool = False) -> TechniqueAuthorityOutcome:
    """Only the already-authored +1 Guided HP increment can be Vigor-free.

    External G4 resolves all normal HP/Repair Progress allocations *first*;
    the Guided +1 must actually remain eligible to restore one HP.
    """
    if actor.level < 3 or actor.aspect != "Restoration" or not actor.active_bond:
        raise ValueError("not an eligible L3 Restoration Anointed")
    if (not active_paid_guided_instance or mode not in ("Fixed", "Maintained")
            or not authenticated_regeneration_step or recipient_dying
            or type(recipient_missing_hp_after_ordinary) is not int
            or recipient_missing_hp_after_ordinary < 1):
        raise ValueError("missing eligible +1 HP Guided incremental restoration")
    if actor.focus == "Low":
        if profile != "Self" or not recipient_self:
            raise ValueError("Low requires actual self [Embodiment] Guided")
    else:
        if profile != "Single Target" or (actor.focus == "Medium" and (actor.invested_vessel is None or not vessel_matches)):
            raise ValueError("High/Medium require exact Single Target and Vessel when Medium")
    updated = _commit(actor, receipt, lesser=True)
    return TechniqueAuthorityOutcome(updated, additional_hp_without_vigor=1)
