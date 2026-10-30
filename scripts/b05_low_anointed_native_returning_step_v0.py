"""B04/B05 Low Anointed Restoration — authentic self-Embodied G0/G4 Step.

The optional self Returning Step is previewed only during its OWN existing
G0/G4 Regeneration Step. Natural allocations are validated against projected
HP/Vigor before G4 pays the actual pulse and finite Lesser Destiny. There is
no second Step, G5 on-hit trigger, out-of-initiative timer or L3 Guided host.
"""
from dataclasses import dataclass

from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, returning_step, set_embodiment,
)
from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint


@dataclass(frozen=True)
class LowPulse:
    round: int
    lesser: bool
    blocked_restoration: tuple
    restoration_check: object


class LowAnointedRestoration:
    """One SHA-bound Low Restoration actor with separate finite Destiny state."""

    def __init__(self, encounter, caster):
        if (encounter.g4 is None or caster not in encounter.actors
                or getattr(encounter.g4, "low_anointed", None) is not None):
            raise ValueError("Attach exactly one Low Anointed to native G4")
        a=encounter.actors[caster]
        path="scripts/b05_low_anointed_restoration_l1_l3_v0.py"
        p=profile(a.level)
        if (a.source.source_id!="AL" or a.source.path!=path
                or a.source.status!="STRUCTURAL_B05_ONLY"
                or a.source.digest!=_fingerprint(path)
                or a.focus!="Low" or a.physical_ap!=20
                or a.projection_ap!=30 or a.ap_total!=p["turn_ap"]
                or a.hp_max!=p["hp_max"] or a.vigor_max!=p["vigor_max"]
                or a.vp_max!=p["vp_max"]
                or a.regen!=p["normal_regen_throughput"]
                or a.guard_capacity!=p["guard_capacity"]
                or dict(a.source.abilities)!=p["abilities"]):
            raise ValueError("Requires exactly sourced Low Anointed Restoration actor")
        self.e=encounter
        self.caster=caster
        self.state=Anointed(a.level,"Low","Restoration")
        self.pending=None
        self.last_toggle_round=None
        encounter.g4.low_anointed=self
        encounter.log("b05_low_anointed_source_bound",caster=caster,
                      level=a.level,source_digest=a.source.digest,
                      destiny=self.state.destiny,embodied=self.state.embodied,
                      scope="native_existing_self_G4_step_only")

    def _turn_start(self):
        e=self.e
        return (e.round>=1 and e.current==self.caster
                and e.pending_regeneration==self.caster
                and e.cursor<len(e.order)
                and e.order[e.cursor]==self.caster
                and self.caster not in e.regen_done)

    def toggle_embodiment(self, *, manifested):
        """Only G0 own-turn Step-2-ready boundary, never mid-turn or off-turn."""
        if (type(manifested) is not bool or not self._turn_start()
                or getattr(self.e,"_live_regeneration_ready_callback",None)!=self.caster
                or self.last_toggle_round==self.e.round
                or self.pending is not None):
            raise ValueError("Embodiment toggles once at real own-turn start only")
        self.state=set_embodiment(self.state,manifested=manifested,
                                 at_own_turn_start=True)
        self.last_toggle_round=self.e.round
        self.e.log("b05_low_anointed_embodiment_set",
                   caster=self.caster,round=self.e.round,
                   manifested=self.state.embodied,activation_ap=0,vp_spent=0)
        return self.state.embodied

    def _upcoming_step(self):
        """Allow an authored next-turn choice or the true Step-ready callback."""
        e=self.e
        if (e.round<1 or e.cursor>=len(e.order)
                or e.order[e.cursor]!=self.caster
                or self.caster in e.regen_done):
            return False
        return e.current is None or self._turn_start()

    def declare_pulse(self, *, lesser=False,blocked_restoration=(),
                      restoration_check=None):
        """Optional one-HP own-Step pulse, not a free per-attack ability."""
        e=self.e
        if type(lesser) is not bool or not self._upcoming_step() or self.pending is not None:
            raise ValueError("Choose only one optional authentic upcoming self-Step pulse")
        a=e.actors[self.caster]
        if (not self.state.active_bond or not self.state.embodied
                or a.dead or a.hp<=0 or a.hp>=a.hp_max):
            raise ValueError("Low Signature requires embodied positive missing self HP")
        if lesser and self.state.destiny<1:
            raise ValueError("Insufficient source Destiny")
        if not lesser and a.vigor<=0:
            raise ValueError("Baseline self Signature requires own Vigor")
        if restoration_check is not None and not callable(restoration_check):
            raise ValueError("Native live restoration_check must be callable")
        blocks=e.g4.live_heal_blocks(e,self.caster,self.caster,
                                      blocked_restoration,restoration_check)
        if "hp" in blocks:
            raise ValueError("Self HP restoration currently blocked")
        # Keep only immutable authored blocks; re-run live checks at true Step.
        declaration=LowPulse(e.round,lesser,tuple(blocked_restoration),
                             restoration_check)
        self.pending=declaration
        e.log("b05_low_anointed_pulse_declared",caster=self.caster,
              round=e.round,lesser=lesser,embodied=True,
              native_self_step_pending=True)

    def cancel_pulse(self):
        """Escape invalid natural allocations without spending AP or Destiny."""
        e=self.e
        p=self.pending
        if (p is None or e.round!=p.round
                or self.caster in e.regen_done
                or (e.current is not None and not self._turn_start())):
            raise ValueError("No cancellable Low self-Step pulse")
        self.pending=None
        e.log("b05_low_anointed_pulse_cancelled",caster=self.caster,
              round=e.round,lesser=p.lesser,ap_spent=0,destiny_spent=0)

    def _on_dead_step(self,recipient):
        p=self.pending
        if p is None or recipient.id!=self.caster:
            return
        if (not self._turn_start() or self.e.round!=p.round or not recipient.dead):
            raise ValueError("Low queued pulse may expire only on real dead own Step")
        self.pending=None
        self.e.log("b05_low_anointed_pulse_expired_on_death",
                   caster=self.caster,round=self.e.round,
                   ap_spent=0,destiny_spent=0)

    def _preview_step(self,recipient):
        """Pure source referee preview invoked ONLY by actual G4 Step-2."""
        p=self.pending
        if p is None or recipient.id!=self.caster:
            return None
        e=self.e
        if (not self._turn_start() or e.round!=p.round
                or not self.state.embodied or not self.state.active_bond):
            raise ValueError("Low pulse cannot escape its live own embodied G0 Step")
        blocks=e.g4.live_heal_blocks(e,self.caster,self.caster,
                                      p.blocked_restoration,p.restoration_check)
        if "hp" in blocks:
            raise ValueError("Live G4 HP block prevents Low self Signature")
        outcome=returning_step(
            self.state,
            receipt=f"g0:{e.scenario}:r{e.round}:step:{self.caster}:low",
            target_id="self",recipient_hp=recipient.hp,
            recipient_max_hp=recipient.hp_max,recipient_vigor=recipient.vigor,
            lesser=p.lesser,distance=0,path_visible=True,
            beneficial_intrusion_legal=True,intrusion_succeeded=True,
            authenticated_regeneration_step=True,
            focus_turn_id=f"round:{e.round}:recipient:{self.caster}",
            recipient_living=not recipient.dead,
        )
        if outcome.ap_spent!=0 or outcome.hp_restored!=1:
            raise AssertionError("Low source Returning Step must be one 0-AP self HP")
        return outcome

    def _apply_step(self,recipient,outcome):
        """G4-only after full natural RegenerationChoice preflight."""
        e=self.e
        p=self.pending
        if (p is None or recipient.id!=self.caster
                or e.g4._live_low_anointed!=(self.caster,e.round)):
            raise ValueError("Only genuine native G4 own Step may apply Low pulse")
        if self._preview_step(recipient)!=outcome:
            raise ValueError("Low recipient changed between preflight and application")
        hp_before,vigor_before=recipient.hp,recipient.vigor
        recipient.hp+=outcome.hp_restored
        recipient.vigor-=outcome.recipient_vigor_spent
        self.state=outcome.actor
        self.pending=None
        e.log("g4_anointed_low_returning_step_applied",
              caster=self.caster,recipient=self.caster,
              source_digest=e.actors[self.caster].source.digest,
              native_step_round=e.round,embodied=self.state.embodied,
              lesser=p.lesser,hp_before=hp_before,hp_after=recipient.hp,
              vigor_before=vigor_before,vigor_after=recipient.vigor,
              hp_restored=outcome.hp_restored,
              recipient_vigor_spent=outcome.recipient_vigor_spent,
              destiny_cost=int(p.lesser),destiny_remaining=self.state.destiny,
              activation_ap=0,vp_spent=0)
        e.check()
