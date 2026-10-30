"""B04/B05 L3 Anointed Restoration: paid native Guided host and one-Step Authority.

Separate from 0-VP Returning Step. The exact G0/G3-paid Fixed/Maintained
Guided Regeneration primary must be active; at its beneficiary's genuine
G4 Step the authored +1 Guided throughput can restore exactly one extra
HP without beneficiary Vigor for one finite Destiny. No G5/Intrusion proof.
"""
from dataclasses import dataclass

from scripts.b05_anointed_authority_l1_l3_v0 import guided_regeneration_l3
from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as high_profile
from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile as medium_profile
from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile as low_profile
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint
from scripts.b06_ranged_v0 import RangedCombat


SOURCE = {
    "AH": ("High", high_profile, "scripts/b05_high_anointed_restoration_l1_l3_v0.py"),
    "AM": ("Medium", medium_profile, "scripts/b05_medium_anointed_restoration_l1_l3_v0.py"),
    "AL": ("Low", low_profile, "scripts/b05_low_anointed_restoration_l1_l3_v0.py"),
}


@dataclass(frozen=True)
class GuidedDeclaration:
    recipient: str
    round: int
    host_id: str
    visible: bool
    unopposed: bool
    blocked_restoration: tuple
    restoration_check: object


class AnointedGuidedAuthority:
    """One source-bound L3 focus; Destiny is shared with its Signature adapter."""

    def __init__(self, encounter, caster):
        if (encounter.g1 is None or encounter.g3 is None or encounter.g4 is None
                or caster not in encounter.actors):
            raise ValueError("Native G1, G3, G4 and source caster required")
        a = encounter.actors[caster]
        if a.source.source_id not in SOURCE or a.level != 3:
            raise ValueError("Only authored L3 Anointed Restoration")
        focus, make, path = SOURCE[a.source.source_id]
        p = make(3)
        if (a.source.path != path or a.source.digest != _fingerprint(path)
                or a.source.status != "STRUCTURAL_B05_ONLY"
                or a.focus != focus or a.projection_ap != p["projection_action_ap"]
                or a.vp_max != p["vp_max"] or a.hp_max != p["hp_max"]
                or dict(a.source.abilities) != p["abilities"]):
            raise ValueError("Unverified source-specific L3 Anointed Guided profile")
        native = {"High": encounter.g4.high_anointed,
                  "Medium": encounter.g4.medium_anointed,
                  "Low": encounter.g4.low_anointed}[focus]
        if native is None or native.caster != caster or native.state.focus != focus:
            raise ValueError("Attach matching source-authentic Returning Step first")
        if caster in encounter.g4.anointed_guided:
            raise ValueError("One L3 Guided Authority source adapter per caster")
        self.e, self.caster, self.focus, self.native = encounter, caster, focus, native
        self.host = None
        self.host_action = None
        self.host_payment = None
        self.pending = None
        encounter.g4.anointed_guided[caster] = self
        encounter.log("b05_anointed_guided_source_bound", caster=caster,
                      focus=focus, source_digest=a.source.digest,
                      shared_destiny=native.state.destiny, level=3)

    def _delivery(self, recipient, *, visible):
        e = self.e
        if type(visible) is not bool or not visible:
            raise UnresolvedDecision("Guided single-target visibility requires explicit scene ruling")
        if recipient not in e.actors:
            raise ValueError("Unknown Guided beneficiary")
        a,b = e.actors[self.caster], e.actors[recipient]
        if self.focus == "Low":
            if recipient != self.caster or not self.native.state.embodied:
                raise ValueError("Low Guided must be actual manifested Self Primary")
            return 0
        if self.focus == "Medium":
            self.native._investment_authentic()
            if self.native.state.invested_vessel != recipient:
                raise ValueError("Medium Guided requires current invested Vessel")
        if len(a.occupied) != 1 or len(b.occupied) != 1:
            raise UnresolvedDecision("Multicell Guided magical path not authored")
        origin,dest=a.occupied[0],b.occupied[0]
        # Guided Regeneration has a technique-local 3D metric, NOT G1's
        # Chebyshev movement/range metric. The bounded G1 map is 2D, so
        # dz=0; preserve the exact half-square increments (e.g. 3,1 -> 3.5).
        a_offset,b_offset,c_offset=sorted((
            abs(origin[0]-dest[0]),abs(origin[1]-dest[1]),0),
            reverse=True)
        distance=a_offset+0.5*b_offset+0.5*c_offset
        if distance > 3:
            raise ValueError("Guided Primary exceeds 3 weighted square-equivalents")
        if distance and self.caster != recipient:
            cells,corners=RangedCombat._ray(origin,dest)
            walls=e.g1.walls
            if any(x in walls or y in walls for x,y in corners):
                raise UnresolvedDecision("Guided ray corner needs GM adjudication")
            if any(cell in walls for cell in cells[1:-1]):
                raise ValueError("Solid wall blocks Guided Single Target")
            if any(other.id not in (self.caster,recipient)
                   and any(cell in cells[1:-1] for cell in other.occupied)
                   for other in e.actors.values()):
                raise UnresolvedDecision("Guided intervening creature requires adjudication")
        return distance

    def cast(self, recipient, *, mode, visible, unopposed):
        """Real 20/24/30 Projection + two Spent or Committed VP, no Destiny."""
        e=self.e
        if mode not in ("fixed","maintained") or type(unopposed) is not bool:
            raise ValueError("Choose a source-guided mode and opposition policy")
        a=e.actors[self.caster]
        if (e.current != self.caster or e.pending_regeneration is not None
                or a.hp <= 0 or a.dead or a.ap_remaining < a.projection_ap
                or not self.native.state.active_bond):
            raise ValueError("Only ready own-turn paid Guided Projection")
        if not unopposed:
            raise UnresolvedDecision("Contested beneficial +8 Intrusion not native here")
        self._delivery(recipient,visible=visible)
        b=e.actors[recipient]
        if b.dead or b.hp <= 0:
            raise ValueError("Bounded Guided recipient must be living")
        if (self.pending is not None or self.host is not None
                and (self.caster,self.host.ident) in e.g3.effects):
            raise ValueError("Release previous Guided host and pending Step first")
        if any(x.kind == "Guided Regeneration" and x.recipient == recipient
               for x in e.g3.effects.values()):
            raise UnresolvedDecision("Competing Guided hosts need authored stacking policy")
        if a.vp_available < 2:
            raise ValueError("Guided requires two real Available VP")
        index=len(e.ledger)
        cost=e.spend_ap(self.caster,"projection",label="anointed:guided:"+mode)
        if cost != a.projection_ap:
            raise AssertionError("Native Guided Projection AP mismatch")
        vp_index=len(e.ledger)
        e.spend_vp(self.caster,2,mode=("spent" if mode=="fixed" else "committed"),
                   label="anointed:guided:"+mode)
        host=e.g3._new_effect(self.caster,"Guided Regeneration",recipient,
                             0 if mode=="fixed" else 2,
                             expiry_round=(e.round+10 if mode=="fixed" else None))
        self.host,self.host_action,self.host_payment=host,index,vp_index
        e.log("b05_anointed_guided_host_established",caster=self.caster,
              recipient=recipient,focus=self.focus,mode=mode,host=host.ident,
              ap_index=index,vp_index=vp_index,source_digest=a.source.digest,
              ap_spent=cost,vp_spent=(2 if mode=="fixed" else 0),
              vp_committed=(2 if mode=="maintained" else 0))
        e.check()
        return host

    def _host_live(self, recipient):
        e=self.e
        h=self.host
        i,j=self.host_action,self.host_payment
        if (h is None or type(i) is not int or type(j) is not int
                or not 0<=i<j<len(e.ledger)
                or e.g3.effects.get((self.caster,h.ident)) is not h
                or h.kind!="Guided Regeneration" or h.caster!=self.caster
                or h.recipient!=recipient or h.ident not in e.actors[self.caster].maintained):
            raise ValueError("No genuine active source-paid Guided host")
        action,payment=e.ledger[i],e.ledger[j]
        mode="fixed" if h.committed==0 else "maintained"
        if (action["kind"]!="action_committed" or action["detail"].get("actor")!=self.caster
                or action["detail"].get("action_class")!="projection"
                or action["detail"].get("ap_spent")!=e.actors[self.caster].projection_ap
                or action["detail"].get("label")!="anointed:guided:"+mode
                or payment["kind"]!="vp_transition"
                or payment["detail"].get("actor")!=self.caster
                or payment["detail"].get("mode")!=("spent" if mode=="fixed" else "committed")
                or payment["detail"].get("points")!=2
                or payment["detail"].get("label")!="anointed:guided:"+mode
                or not any(v["kind"]=="b05_anointed_guided_host_established"
                           and v["detail"].get("host")==h.ident
                           and v["detail"].get("ap_index")==i
                           and v["detail"].get("vp_index")==j
                           for v in e.ledger[j+1:])):
            raise ValueError("Unattested Guided AP/VP/host receipts")
        # G3's generic throughput intentionally coalesces multiple Guided
        # effects to one slot. A native Authority must never attribute that
        # shared slot to one arbitrarily chosen paid host.
        if sum(v.kind=="Guided Regeneration" and v.recipient==recipient
               for v in e.g3.effects.values())!=1:
            raise UnresolvedDecision("Competing Guided instances cannot share one Authority waiver")
        return mode

    def declare_waiver(self, recipient, *, visible, unopposed,
                       blocked_restoration=(), restoration_check=None):
        """Commit to a proposed next genuine beneficiary Step, no Destiny yet."""
        e=self.e
        if type(unopposed) is not bool or self.pending is not None:
            raise ValueError("Explicit one-Step Authority decision required")
        if (e.round < 1 or e.current is not None or
                e.cursor >= len(e.order) or e.order[e.cursor]!=recipient
                or recipient in e.regen_done):
            raise ValueError("Only the next genuine G0 recipient Step qualifies")
        if not unopposed:
            raise UnresolvedDecision("Refused beneficial Guided needs +8 Intrusion")
        mode=self._host_live(recipient)
        self._delivery(recipient,visible=visible)
        b=e.actors[recipient]
        if b.dead or b.hp<=0 or b.hp>=b.hp_max:
            raise ValueError("Only living positive missing-HP Guided beneficiary")
        if (not self.native.state.active_bond or self.native.state.destiny<1):
            raise ValueError("Finite Destiny required for Guided Lesser")
        if restoration_check is not None and not callable(restoration_check):
            raise ValueError("Live restoration callback must be callable")
        blocks=e.g4.live_heal_blocks(e,self.caster,recipient,
                                      blocked_restoration,restoration_check)
        if "hp" in blocks:
            raise ValueError("Current HP restoration blocked")
        self.pending=GuidedDeclaration(recipient,e.round,self.host.ident,
                                       visible,unopposed,tuple(blocked_restoration),
                                       restoration_check)
        e.log("b05_anointed_guided_waiver_declared",caster=self.caster,
              recipient=recipient,round=e.round,host=self.host.ident,
              mode=mode,destiny_pending=1)

    def cancel_waiver(self):
        e=self.e
        p=self.pending
        if (p is None or p.recipient in e.regen_done or e.round!=p.round
                or (e.current is not None and
                    (e.current!=p.recipient or e.pending_regeneration!=p.recipient))):
            raise ValueError("No cancellable native Guided Step waiver")
        self.pending=None
        e.log("b05_anointed_guided_waiver_cancelled",caster=self.caster,
              recipient=p.recipient,round=p.round,destiny_spent=0)

    def _on_dead_step(self,recipient):
        p=self.pending
        if p is None or p.recipient!=recipient.id:
            return
        e=self.e
        if (e.current!=recipient.id or e.pending_regeneration!=recipient.id
                or not recipient.dead or e.round!=p.round):
            raise ValueError("Only genuine dead Step may expire Guided waiver")
        self.pending=None
        e.log("b05_anointed_guided_waiver_expired_on_death",
              caster=self.caster,recipient=recipient.id,destiny_spent=0)

    def _preview_step(self,recipient):
        e=self.e
        p=self.pending
        if p is None or p.recipient!=recipient.id:
            return None
        if (e.current!=recipient.id or e.pending_regeneration!=recipient.id
                or e.order[e.cursor]!=recipient.id or recipient.id in e.regen_done
                or e.round!=p.round):
            raise ValueError("No real current Guided recipient Step")
        mode=self._host_live(recipient.id)
        self._delivery(recipient.id,visible=p.visible)
        blocks=e.g4.live_heal_blocks(e,self.caster,recipient.id,
                                      p.blocked_restoration,p.restoration_check)
        if "hp" in blocks:
            raise ValueError("Live Guided HP block")
        if (recipient.dead or recipient.hp<=0 or not p.unopposed
                or not self.native.state.active_bond or self.native.state.destiny<1):
            raise ValueError("Guided authority requires living unopposed bond and Destiny")
        return mode

    def _preview_payout(self, recipient, *, missing_after_ordinary):
        """G4-only pure calculation after the natural choice passes validation."""
        mode=self._preview_step(recipient)
        if mode is None:
            return None
        source=self.native.state
        return guided_regeneration_l3(
            source,receipt=(f"g0:{self.e.scenario}:r{self.e.round}:"
                            f"guided:{self.caster}:{recipient.id}:{self.host.ident}"),
            recipient_missing_hp_after_ordinary=missing_after_ordinary,
            active_paid_guided_instance=True,
            mode=("Fixed" if mode=="fixed" else "Maintained"),
            profile=("Self" if self.focus=="Low" else "Single Target"),
            authenticated_regeneration_step=True,
            guided_bonus_unsuppressed=True,
            vessel_matches=(self.focus=="Medium" and source.invested_vessel==recipient.id),
            recipient_self=(recipient.id==self.caster),
            recipient_dying=recipient.hp<=0)

    def _apply_step(self, recipient, outcome):
        e=self.e
        p=self.pending
        if (p is None or p.recipient!=recipient.id
                or e.g4._live_anointed_guided!=(self.caster,recipient.id,e.round)
                or recipient.id not in e.regen_done):
            raise ValueError("Guided +1 payout requires completed real G4 Step")
        if (recipient.dead or recipient.hp<=0 or recipient.hp>=recipient.hp_max
                or self._preview_step_completed_check(recipient) is False):
            raise ValueError("No living missing-HP source Guided increment")
        # At application the G4 natural Step is already resolved. Do not
        # re-preview the unfinished Step; outcome was preflighted before it.
        if outcome.additional_hp_without_vigor!=1 or outcome.actor.destiny!=self.native.state.destiny-1:
            raise ValueError("Source Guided one-Destiny packet mismatch")
        hp_before,vigor_before=recipient.hp,recipient.vigor
        recipient.hp+=1
        self.native.state=outcome.actor
        self.pending=None
        e.log("g4_anointed_guided_waiver_applied",
              caster=self.caster,recipient=recipient.id,focus=self.focus,
              host=self.host.ident,host_action_index=self.host_action,
              host_vp_index=self.host_payment,source_digest=e.actors[self.caster].source.digest,
              mode=("Fixed" if self.host.committed==0 else "Maintained"),
              native_step_round=e.round,hp_before=hp_before,hp_after=recipient.hp,
              vigor_before=vigor_before,vigor_after=recipient.vigor,
              hp_restored=1,recipient_vigor_spent=0,destiny_cost=1,
              destiny_remaining=self.native.state.destiny,
              activation_ap=0,additional_throughput=0)
        e.check()

    def _preview_step_completed_check(self, recipient):
        """The source host must still be active at native G4 payout time."""
        return (self.host is not None
                and self.e.g3.effects.get((self.caster,self.host.ident)) is self.host
                and self.native.state.active_bond)
