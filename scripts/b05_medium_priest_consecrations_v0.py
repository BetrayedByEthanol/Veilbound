"""B04/B05 Life Medium Priest: bounded native G0/G3/G4 Consecration adapter.

Only the source-authored M build, maintained Guided Regeneration and maintained
Vital Shelter are supported. No automatic tactical choice or invented effect
cadence. G3 owns effect reservation, G4 owns real damage and regeneration.
"""
from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_ranged_v0 import RangedCombat


class MediumLifeConsecrations:
    def __init__(self, encounter):
        if encounter.g3 is None:
            raise ValueError("Install native G3 before Medium Priest adapter")
        if getattr(encounter.g3, "medium_life", None) is not None:
            raise ValueError("Medium Priest adapter already installed")
        self.e = encounter
        self.g3 = encounter.g3
        self._regen_beneficiary = None
        self.g3.medium_life = self
        encounter.log("b05_medium_life_consecrations_installed")

    def _priest(self, caster):
        if caster not in self.e.actors:
            raise ValueError("Unknown Medium Priest")
        a = self.e.actors[caster]
        if a.source.source_id != "M" or a.focus != "Medium":
            raise UnresolvedDecision("Only verified M Medium Life source can use this adapter")
        from scripts.b05_medium_priest_life_l1_l3_v0 import profile
        p = profile(a.level)
        if (dict(a.source.abilities) != p["abilities"] or a.vp_max != p["vp_max"]
                or a.projection_ap != 24):
            raise UnresolvedDecision("Medium Life source mismatch")
        return a, p

    def _host(self, caster):
        hosted = [v for v in self.g3.effects.values() if v.caster == caster
                  and v.kind in ("Guided Regeneration", "Vital Shelter")
                  and v.committed > 0]
        if len(hosted) > 1:
            raise ValueError("Medium Consecration active-cap violation")
        return hosted[0] if hosted else None

    def _target(self, caster, recipient):
        if recipient not in self.e.actors:
            raise ValueError("Unknown Consecration recipient")
        c = self.e.actors[caster]
        r = self.e.actors[recipient]
        if r.dead:
            raise ValueError("Living recipient required")
        if recipient == caster:
            return
        if self.e.g1 is None:
            raise UnresolvedDecision("Non-self magic requires live G1 geometry")
        if len(c.occupied) != 1 or len(r.occupied) != 1:
            raise UnresolvedDecision("Only sourced one-square 2D geometry verified")
        x,y = c.occupied[0][:2]
        u,v = r.occupied[0][:2]
        if len(c.occupied[0]) != 2 or len(r.occupied[0]) != 2:
            raise UnresolvedDecision("No fabricated 3D delivery line")
        a,b = sorted((abs(u-x),abs(v-y)),reverse=True)
        if a + 0.5*b > 3:
            raise ValueError("Consecration target beyond three-square range")
        cells,corners = RangedCombat._ray((x,y),(u,v))
        walls = self.e.g1.walls
        if any(p in walls for p in cells[1:-1]) or any(
                m in walls or n in walls for m,n in corners):
            raise ValueError("Consecration obstructed delivery path")

    def _available(self, caster):
        a,_ = self._priest(caster)
        if a.hp <= 0 or a.dead:
            raise ValueError("Incapacitated Medium Priest")
        return a

    def cast(self, caster, kind, recipient, *, on_committed=None):
        """Prepared maintained Primary; excludes fixed and unspecified modes."""
        a,p = self._priest(caster)
        if kind not in ("Guided Regeneration","Vital Shelter") or kind not in p["prepared_prayers"]:
            raise UnresolvedDecision("Not an authored prepared Life Consecration")
        if self.e.current != caster or self.e.pending_regeneration is not None:
            raise ValueError("Activation requires a ready own turn")
        self._available(caster)
        self._target(caster,recipient)
        if self._host(caster) is not None or self.g3.active(caster,kind):
            raise ValueError("Only one active maintained Consecration at L1–3")
        if any(v.kind == kind and v.recipient == recipient for v in self.g3.effects.values()):
            raise ValueError("Duplicate named effect on recipient")
        spent = int(kind == "Vital Shelter")
        cost = spent + 2
        if on_committed is not None and not callable(on_committed):
            raise ValueError("Invalid response callback")
        if a.ap_remaining < 24 or a.vp_available < cost:
            raise ValueError("Insufficient AP or Available VP")
        self.e.spend_ap(caster,"projection",label="b05:medium:"+kind)
        if on_committed is not None:
            on_committed(self.e)
        # At post-commit application no full priced invocation or new target.
        if (a.hp <= 0 or a.vp_available < cost or
                self._host(caster) is not None or
                any(v.kind == kind and v.recipient == recipient
                    for v in self.g3.effects.values())):
            self.e.log("b05_medium_cast_interrupted",caster=caster,technique=kind)
            return None
        try:
            self._target(caster,recipient)
        except (ValueError,UnresolvedDecision):
            self.e.log("b05_medium_cast_interrupted",caster=caster,technique=kind,
                       cause="recipient_or_path_changed")
            return None
        self.g3._pay(caster,spent,2,label="b05:medium:"+kind)
        effect = self.g3._new_effect(
            caster,kind,recipient,2,budget=(8+max(0,p["abilities"]["Veil Control"])
                                             if kind == "Vital Shelter" else None))
        self.e.log("b05_consecration_applied",caster=caster,recipient=recipient,
                   effect=effect.ident,technique=kind,spent=spent,committed=2,
                   budget=effect.budget)
        return effect

    def reassign(self, caster, recipient):
        a,_ = self._priest(caster)
        if self.e.current != caster or self.e.pending_regeneration is not None:
            raise ValueError("Reassign requires a ready own turn")
        self._available(caster)
        host = self._host(caster)
        if host is None:
            raise ValueError("No active Consecration")
        if host.recipient == recipient:
            raise ValueError("Must choose another recipient")
        if any(v.kind == host.kind and v.recipient == recipient
               for v in self.g3.effects.values()):
            raise ValueError("Identical blessing cannot stack on recipient")
        if a.ap_remaining < 24:
            raise ValueError("Insufficient General Tempo AP")
        self._target(caster,recipient)
        self.e.spend_ap(caster,"general",label="b05:medium:reassign")
        # Failed delivery after paid AP retains old beneficiary and budget.
        try:
            self._target(caster,recipient)
        except (ValueError,UnresolvedDecision):
            self.e.log("b05_reassign_failed",caster=caster,effect=host.ident)
            return False
        old = host.recipient
        host.recipient = recipient
        self.e.log("b05_consecration_reassigned",caster=caster,effect=host.ident,
                   previous=old,recipient=recipient,budget=host.budget,
                   committed=host.committed)
        return True

    def _intercession(self, caster, recipient, kind):
        a,_ = self._priest(caster)
        host = self._host(caster)
        if a.level < 3 or host is None or host.kind != kind:
            raise ValueError("L3 matching active Consecration required")
        if host.recipient == recipient or not a.reaction_available:
            raise ValueError("Another recipient and unused Reaction required")
        self._available(caster)
        if a.vp_available < 2:
            raise ValueError("Intercession requires two Available VP")
        self._target(caster,recipient)
        a.reaction_available = False
        self.e.spend_vp(caster,2,mode="spent",label="b05:medium:intercession")
        self.e.log("b05_intercession_paid",caster=caster,recipient=recipient,
                   effect=host.ident,technique=kind,reaction=True,spent=2)
        return host

    def intercede_regeneration(self, caster, recipient):
        """Call only inside target's actual G0 start_turn Step-2 window."""
        if (self.e.pending_regeneration != recipient or self.e.current != recipient
                or recipient in self.e.regen_done or self._regen_beneficiary is not None):
            raise ValueError("No single imminent real Regeneration Step")
        if any(v.kind == "Guided Regeneration" and v.recipient == recipient
               for v in self.g3.effects.values()):
            raise ValueError("Guided Regeneration never stacks")
        host = self._intercession(caster,recipient,"Guided Regeneration")
        self._regen_beneficiary = recipient
        self.e.log("b05_guided_intercession_armed",caster=caster,
                   recipient=recipient,effect=host.ident)

    def bonus_for_regen(self, recipient):
        return int(self._regen_beneficiary == recipient)

    def finish_regen(self, recipient):
        if self._regen_beneficiary == recipient:
            self._regen_beneficiary = None
            self.e.log("b05_guided_intercession_finished",recipient=recipient)

    def preflight_vigor(self, caster, recipient):
        """Check the selected beneficiary and funded Reaction before G4 mutates."""
        a,_ = self._priest(caster)
        host = self._host(caster)
        if (self.e.g4 is None or a.level < 3 or host is None
                or host.kind != "Vital Shelter" or not host.budget):
            raise ValueError("An active L3 Vital Shelter and native G4 required")
        if host.recipient == recipient or not a.reaction_available:
            raise ValueError("Intercession needs other recipient and live Reaction")
        if any(v.kind == "Vital Shelter" and v.recipient == recipient
               for v in self.g3.effects.values()):
            raise ValueError("Cannot stack recipient Vital Shelter")
        self._available(caster)
        if a.vp_available < 2:
            raise ValueError("Intercession cannot spend unavailable VP")
        self._target(caster,recipient)
        return host

    def intercede_vigor(self, caster, recipient, amount):
        """Called synchronously from one genuinely applying G4 Vigor packet."""
        if type(amount) is not int or amount <= 0:
            raise ValueError("Positive native direct Vigor packet required")
        self.preflight_vigor(caster,recipient)
        host = self._intercession(caster,recipient,"Vital Shelter")
        target = self.e.actors[recipient]
        absorbed = min(amount,host.budget) if target.vigor > 0 else 0
        host.budget -= absorbed
        self.e.log("b05_vital_intercession_packet",caster=caster,recipient=recipient,
                   effect=host.ident,original=amount,prevented=absorbed,
                   residual=amount-absorbed,budget=host.budget)
        if host.budget == 0:
            self.g3._end(host,reason="budget_exhausted")
        return amount-absorbed
