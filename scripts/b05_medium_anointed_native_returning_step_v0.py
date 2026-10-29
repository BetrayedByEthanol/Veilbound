"""B04/B05 Medium Anointed Restoration v0: native Investment and once-per-Step pulse.

Investment is one real 24-AP G0 General Action, with explicitly declared living
recipient consent. A queued legal pulse is resolved only INSIDE the matching
recipient's actual G4 Regeneration Step, before normal allocation, after G4
allocation preflight. The source referee's authenticated_step flag is derived
from active G0 state, never an input from the caller.

This is NOT L3 Guided Authority, contested +8 Intrusion, hostile Investment,
authentic consent/perception adjudication or a full independent Focus certificate.
"""
from dataclasses import dataclass

from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, invest as source_invest, returning_step,
)
from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint
from scripts.b06_ranged_v0 import RangedCombat


@dataclass(frozen=True)
class PulseDeclaration:
    recipient: str
    round: int
    lesser: bool
    visible: bool
    unopposed: bool
    blocked_restoration: tuple
    restoration_check: object


class MediumAnointedRestoration:
    """Native G0/G1/G4 only; never accepts caller-claimed Regeneration receipts."""

    def __init__(self, encounter, caster):
        if (encounter.g1 is None or encounter.g4 is None
                or caster not in encounter.actors
                or getattr(encounter.g4, "medium_anointed", None) is not None):
            raise ValueError("Attach exactly one Medium Anointed to native G1/G4")
        a=encounter.actors[caster]
        path="scripts/b05_medium_anointed_restoration_l1_l3_v0.py"
        p=profile(a.level)
        if (a.source.source_id!="AM" or a.source.path!=path
                or a.source.status!="STRUCTURAL_B05_ONLY"
                or a.source.digest!=_fingerprint(path)
                or a.focus!="Medium" or a.physical_ap!=24
                or a.projection_ap!=24 or a.ap_total!=p["turn_ap"]
                or a.hp_max!=p["hp_max"] or a.vigor_max!=p["vigor_max"]
                or a.vp_max!=p["vp_max"]
                or dict(a.source.abilities)!=p["abilities"]):
            raise ValueError("Requires exactly sourced Medium Anointed Restoration actor")
        self.e=encounter
        self.caster=caster
        self.state=Anointed(a.level,"Medium","Restoration")
        self.invest_action_index=None
        self.pending=None
        encounter.g4.medium_anointed=self
        encounter.log("b05_medium_anointed_source_bound",caster=caster,
                      level=a.level,source_digest=a.source.digest,
                      destiny=self.state.destiny,
                      scope="native_paid_investment_and_existing_G4_step_only")

    def invest(self, recipient, *, consenting):
        """Actual 24-AP General G0 action: only one currently consenting living Vessel."""
        e=self.e
        if recipient not in e.actors or type(consenting) is not bool or not consenting:
            raise UnresolvedDecision("One explicitly consenting living Vessel required")
        a,b=e.actors[self.caster],e.actors[recipient]
        if (e.current!=self.caster or e.pending_regeneration is not None
                or a.dead or a.hp<=0 or a.ap_remaining<24
                or b.dead or b.hp<=0 or not self.state.active_bond):
            raise ValueError("Only a ready Medium own turn can establish one living Investment")
        if self.pending is not None:
            raise ValueError("Finish or abandon a queued recipient Step before re-Investment")
        source,ap=source_invest(self.state,recipient,
               ap_available=a.ap_remaining,legal_vessel=True,
               consent_or_other_delivery_valid=True)
        if ap!=24 or source.invested_vessel!=recipient:
            raise AssertionError("Source Investment is exactly one 24-AP Vessel")
        event_index=len(e.ledger)
        paid=e.spend_ap(self.caster,"general",label="anointed:medium:investment")
        if paid!=24 or e.ledger[event_index]["kind"]!="action_committed":
            raise AssertionError("Native General AP payment missing")
        self.state=source
        self.invest_action_index=event_index
        e.log("b05_medium_anointed_investment_established",
              caster=self.caster,vessel=recipient,action_index=event_index,
              source_digest=a.source.digest,ap_spent=24,vp_spent=0)
        e.check()
        return {"action_index":event_index,"vessel":recipient,
                "ap_spent":24,"vp_spent":0}

    def _investment_authentic(self):
        i=self.invest_action_index
        e=self.e
        if (type(i) is not int or not 0<=i<len(e.ledger)
                or not self.state.active_bond
                or self.state.invested_vessel not in e.actors):
            raise ValueError("Missing live one-Vessel Investment")
        v=e.ledger[i]
        d=v["detail"]
        if (v["kind"]!="action_committed" or v["turn"]!=self.caster
                or d.get("actor")!=self.caster
                or d.get("action_class")!="general"
                or d.get("label")!="anointed:medium:investment"
                or d.get("ap_spent")!=24
                or not any(ev["kind"]=="b05_medium_anointed_investment_established"
                           and ev["detail"].get("action_index")==i
                           and ev["detail"].get("vessel")==self.state.invested_vessel
                           for ev in e.ledger[i+1:])):
            raise ValueError("Forged or stale G0 Investment source receipt")

    def _delivery(self,recipient,*,visible):
        if type(visible) is not bool or not visible:
            raise UnresolvedDecision("Current target visibility must be independently declared")
        e=self.e
        a,b=e.actors[self.caster],e.actors[recipient]
        if len(a.occupied)!=1 or len(b.occupied)!=1:
            raise UnresolvedDecision("No authored multicell Medium Restoration magical path")
        origin,dest=a.occupied[0],b.occupied[0]
        distance=max(abs(origin[0]-dest[0]),abs(origin[1]-dest[1]))
        if distance>3:
            raise ValueError("Medium Investment does not extend 0–3 pulse range")
        if distance and self.caster!=recipient:
            ray,corners=RangedCombat._ray(origin,dest)
            walls=e.g1.walls
            if any(x in walls or y in walls for x,y in corners):
                raise UnresolvedDecision("Medium pulse grazes unresolved solid corner")
            if any(c in walls for c in ray[1:-1]):
                raise ValueError("Medium pulse blocked by solid wall")
            if any(other.id not in (self.caster,recipient)
                   and any(c in ray[1:-1] for c in other.occupied)
                   for other in e.actors.values()):
                raise UnresolvedDecision("Intervening living screen needs separate magical adjudication")
        return distance

    def declare_pulse(self,recipient,*,lesser=False,visible,unopposed,
                      blocked_restoration=(),restoration_check=None):
        """Opt into ONE upcoming true recipient Step; never declare a fake Step."""
        e=self.e
        if (recipient not in e.actors or type(lesser) is not bool
                or type(unopposed) is not bool):
            raise ValueError("Explicit positive-HP recipient and Lesser decision required")
        self._investment_authentic()
        if (self.pending is not None or recipient!=self.state.invested_vessel
                or e.round<1 or e.current is not None
                or e.pending_regeneration is not None or e.cursor>=len(e.order)
                or e.order[e.cursor]!=recipient or recipient in e.regen_done):
            raise ValueError("One pulse may be declared only for the next real invested Step")
        if not unopposed:
            raise UnresolvedDecision("Beneficial refusal requires the unresolved +8 Intrusion contest")
        b=e.actors[recipient]
        if b.dead or b.hp<=0 or b.hp==b.hp_max:
            raise ValueError("Target must be positive-HP living with missing HP")
        if lesser and self.state.destiny<1:
            raise ValueError("Insufficient finite Destiny")
        if not lesser and b.vigor==0:
            raise ValueError("Baseline pulse needs existing recipient Vigor")
        self._delivery(recipient,visible=visible)
        if restoration_check is not None and not callable(restoration_check):
            raise ValueError("Live restoration check must be callable")
        blocks=e.g4.live_heal_blocks(e,self.caster,recipient,
                                      blocked_restoration,restoration_check)
        if "hp" in blocks:
            raise ValueError("Live HP restoration blocked")
        # Keep the declared static blocks, NOT a live snapshot that could
        # mask a new response/ward before the recipient's actual Step.
        self.pending=PulseDeclaration(recipient,e.round,lesser,visible,
                                      unopposed,tuple(blocked_restoration),
                                      restoration_check)
        e.log("b05_medium_anointed_pulse_declared",caster=self.caster,
              vessel=recipient,round=e.round,lesser=lesser,
              investment_action_index=self.invest_action_index,
              native_step_pending=True)

    def cancel_pulse(self):
        """Abandon an unstarted/suspended Step declaration without extra effects.

        A target that moved, refused or became Dying must never strand the
        real G0 turn; cancel and resume ordinary G4 regeneration instead.
        """
        e=self.e
        p=self.pending
        if (p is None or e.round!=p.round
                or p.recipient in e.regen_done
                or (e.current is not None and (
                    e.current!=p.recipient
                    or e.pending_regeneration!=p.recipient))):
            raise ValueError("No cancellable pending native recipient pulse")
        self.pending=None
        e.log("b05_medium_anointed_pulse_cancelled",
              caster=self.caster,recipient=p.recipient,
              round=e.round,lesser=p.lesser,destiny_spent=0,ap_spent=0)

    def _on_dead_step(self,recipient):
        """A truly dead recipient's native Step expires a queued pulse safely."""
        p=self.pending
        if p is None or p.recipient!=recipient.id:
            return
        e=self.e
        if (e.current!=recipient.id or e.pending_regeneration!=recipient.id
                or e.round!=p.round or not recipient.dead):
            raise ValueError("Only a genuine dead-recipient G0 Step can expire pulse")
        self.pending=None
        e.log("b05_medium_anointed_pulse_expired_on_death",
              caster=self.caster,recipient=recipient.id,round=e.round,
              destiny_spent=0,ap_spent=0)

    def _preview_step(self,recipient):
        """G4-only pure preflight at the actual live G0 Step-2 boundary."""
        e=self.e
        p=self.pending
        if p is None or p.recipient!=recipient.id:
            return None
        if (e.current!=recipient.id or e.pending_regeneration!=recipient.id
                or e.order[e.cursor]!=recipient.id
                or recipient.id in e.regen_done or e.round!=p.round):
            raise ValueError("Not the genuine unfinished recipient G0 Regeneration Step")
        self._investment_authentic()
        if self.state.invested_vessel!=recipient.id or not p.unopposed:
            raise ValueError("Vessel mismatch or refused pulse")
        distance=self._delivery(recipient.id,visible=p.visible)
        blocks=e.g4.live_heal_blocks(e,self.caster,recipient.id,
                                      p.blocked_restoration,p.restoration_check)
        if "hp" in blocks:
            raise ValueError("Native HP block prevents Medium pulse")
        receipt=f"g0:{e.scenario}:r{e.round}:step:{recipient.id}:med:{self.invest_action_index}"
        turn=f"round:{e.round}:recipient:{recipient.id}"
        outcome=returning_step(
            self.state,receipt=receipt,target_id=recipient.id,
            recipient_hp=recipient.hp,recipient_max_hp=recipient.hp_max,
            recipient_vigor=recipient.vigor,lesser=p.lesser,distance=distance,
            path_visible=True,beneficial_intrusion_legal=True,
            intrusion_succeeded=True,
            authenticated_regeneration_step=True,focus_turn_id=turn)
        if outcome.ap_spent!=0 or outcome.hp_restored!=1:
            raise AssertionError("Medium once-per-Step packet must be 1 HP, 0 activation AP")
        return outcome

    def _apply_step(self,recipient,outcome):
        """Called by G4 only after all ordinary RegenerationChoice checks pass."""
        e=self.e
        p=self.pending
        if p is None or p.recipient!=recipient.id:
            raise ValueError("No pending Medium source Step")
        if self.e.g4._live_medium_anointed!=(recipient.id,self.e.round):
            raise ValueError("Only native G4 Regeneration Step may apply Medium Signature")
        check=self._preview_step(recipient)
        if check!=outcome:
            raise ValueError("Recipient source resources changed after preflight")
        old_hp,old_vigor=recipient.hp,recipient.vigor
        recipient.hp+=outcome.hp_restored
        recipient.vigor-=outcome.recipient_vigor_spent
        self.state=outcome.actor
        self.pending=None
        e.log("g4_anointed_medium_returning_step_applied",
              caster=self.caster,recipient=recipient.id,
              investment_action_index=self.invest_action_index,
              source_digest=e.actors[self.caster].source.digest,
              native_step_round=e.round,lesser=p.lesser,
              hp_before=old_hp,hp_after=recipient.hp,
              vigor_before=old_vigor,vigor_after=recipient.vigor,
              hp_restored=outcome.hp_restored,
              recipient_vigor_spent=outcome.recipient_vigor_spent,
              destiny_cost=int(p.lesser),destiny_remaining=self.state.destiny,
              activation_ap=0,vp_spent=0)
        e.check()

