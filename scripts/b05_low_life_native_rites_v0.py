"""B04/B05 Low Life A/B: native G0/G3/G4 Chosen Rites and L3 Exaltation.

A/B's G0 physical proxies remain unchanged; this is a separate explicitly
source-authenticated authority for their already-audited Life repertoires.
No generic GM-created damage or extra regeneration/Reaction is authorized.
"""
from hashlib import sha256

from scripts.b06_encounter_state_v0 import ROOT, UnresolvedDecision, party_actor
from scripts.b06_ranged_v0 import RangedCombat

SOURCE="scripts/b06_hunter_party_exchanges_v0.py"
DESIGN="docs/design/b05-life-low-priest-l3-build-exaltation-verification-v0.md"
RULE="docs/rules/07-veil-magic/life-exaltation-properties-v0.md"
RULE_PINS=(
    "## EX-LR-01 — Held Renewal",
    "## EX-LP-01 — Vital Interposition",
    "**1 Spent VP**",
    "P = min(2, event_HP, floor(actual remaining host Vigor-prevention budget / 2))",
)
CHOICES={"A":"Guided Regeneration","B":"Vital Shelter"}


class LowLifeNativeRites:
    def __init__(self,encounter,caster):
        if encounter.g3 is None or encounter.g4 is None or encounter.g1 is None:
            raise ValueError("Requires native G1/G3/G4")
        if encounter.round or encounter.current is not None:
            raise ValueError("Bind audited Low Life source before initiative")
        if getattr(encounter.g3,"low_life",None) is not None:
            raise ValueError("Exactly one selected Low Priest in this bounded scene")
        if caster not in encounter.actors:
            raise ValueError("Missing chosen Priest")
        a=encounter.actors[caster]
        expected=party_actor(a.source.source_id,a.level,"source-proof","party",
                             occupied=a.occupied) if a.source.source_id in CHOICES else None
        design=(ROOT/DESIGN).read_text(encoding="utf-8")
        rules=(ROOT/RULE).read_text(encoding="utf-8")
        if any(pin not in rules for pin in RULE_PINS):
            raise AssertionError("Canonical Low Exaltation price/identity changed")
        if (expected is None or a.source!=expected.source
                or a.hp_max!=expected.hp_max
                or a.vigor_max!=expected.vigor_max
                or a.ap_total!=expected.ap_total
                or a.physical_ap!=expected.physical_ap
                or a.focus!="Low" or a.source.path!=SOURCE
                or a.source.digest!=sha256((ROOT/SOURCE).read_bytes()).hexdigest()
                or a.source.status!="B05_UNBUFFED_PHYSICAL_PROXY"
                or a.vp_max!=2*a.level or a.projection_ap!=30
                or a.level not in (1,2,3)
                or a.regen!=6
                or "Level-1 Prepared / Chosen" not in design):
            raise UnresolvedDecision("Exact audited A/B Low Life build required")
        self.e=encounter
        self.g3=encounter.g3
        self.caster=caster
        self.role=a.source.source_id
        self.chosen_name=CHOICES[self.role]
        self.pending=None
        self.armed_vital_turns=set()
        self.last_held_step=None
        self.g3.low_life=self
        encounter.log("b05_low_life_bound",caster=caster,role=a.source.source_id,
                      chosen=self.chosen_name,source_sha256=a.source.digest,
                      design_sha256=sha256((ROOT/DESIGN).read_bytes()).hexdigest(),
                      rules_sha256=sha256((ROOT/RULE).read_bytes()).hexdigest())

    def _source(self,caster):
        if caster!=self.caster:
            raise UnresolvedDecision("Wrong Low Life caster")
        a=self.e.actors[caster]
        expected=party_actor(self.role,a.level,"source-proof","party",
                             occupied=a.occupied)
        if (a.source!=expected.source
                or a.hp_max!=expected.hp_max
                or a.vigor_max!=expected.vigor_max
                or a.ap_total!=expected.ap_total
                or a.physical_ap!=expected.physical_ap
                or a.source.source_id!=self.role or a.source.path!=SOURCE
                or a.source.status!="B05_UNBUFFED_PHYSICAL_PROXY"
                or a.source.digest!=sha256((ROOT/SOURCE).read_bytes()).hexdigest()
                or a.focus!="Low" or a.vp_max!=2*a.level
                or a.projection_ap!=30 or a.regen!=6):
            raise UnresolvedDecision("Low source identity/resources changed")
        return a

    def _host(self):
        return [v for v in self.g3.effects.values()
                if v.caster==self.caster and v.kind==self.chosen_name
                and v.recipient==self.caster and v.committed>0]

    def _chosen_host(self):
        host=self._host()
        if len(host)!=1 or not host[0].chosen or host[0].committed!=1:
            raise ValueError("One real, funded, self Chosen Rite required")
        if host[0].ident not in self.e.actors[self.caster].maintained:
            raise ValueError("Chosen Rite missing native G3 maintenance")
        return host[0]

    def cast_chosen(self,caster,*,chosen=True,on_committed=None):
        a=self._source(caster)
        if self.e.current!=caster or self.e.pending_regeneration is not None:
            raise ValueError("Requires a ready own turn")
        if a.hp<=0:
            raise ValueError("Dying caster cannot cast")
        if self._host() or any(
                v.caster==caster and v.committed>0 and
                v.kind in ("Guided Regeneration","Vital Shelter")
                for v in self.g3.effects.values()):
            raise ValueError("Only one active Low L1–3 Rite")
        if type(chosen) is not bool:
            raise ValueError("Explicit chosen status required")
        committed=1 if chosen else 2
        spent=int(self.chosen_name=="Vital Shelter")
        self.g3._funds(a,spent,committed)
        if on_committed is not None and not callable(on_committed):
            raise ValueError("Callback required")
        if a.ap_remaining<30:
            raise ValueError("Source Projection AP required")
        self.e.spend_ap(caster,"projection",label="b05:low:chosen_rite")
        if on_committed is not None:
            on_committed(self.e)
        source_ok=True
        try:
            self._source(caster)
        except (ValueError,UnresolvedDecision):
            source_ok=False
        if (not source_ok or a.hp<=0 or a.vp_available<spent+committed
                or self._host()
                or any(v.caster==caster and v.committed>0 and
                       v.kind in ("Guided Regeneration","Vital Shelter")
                       for v in self.g3.effects.values())):
            self.e.log("b05_low_rite_interrupted",caster=caster,spent_vp=0)
            return None
        self.g3._pay(caster,spent,committed,label="b05:low:rite")
        host=self.g3._new_effect(
            caster,self.chosen_name,caster,committed,chosen=chosen,
            budget=8 if self.chosen_name=="Vital Shelter" else None)
        self.e.log("b05_low_rite_established",caster=caster,
                   effect=host.ident,technique=host.kind,chosen=chosen,
                   spent=spent,committed=committed,budget=host.budget)
        self.e.check()
        return host

    def arm_vital(self,caster):
        a=self._source(caster)
        if (a.level<3 or self.chosen_name!="Vital Shelter"
                or self.e.current!=caster or self.e.pending_regeneration is not None
                or a.ap_remaining<0 or a.hp<=0):
            raise ValueError("L3 own-turn Preservation activation only")
        host=self._chosen_host()
        if (host.budget is None or host.budget<2 or self.pending is not None
                or (self.e.round,caster) in self.armed_vital_turns):
            raise ValueError("Need finite Chosen budget and unused own-turn property")
        if a.vp_available<1:
            raise ValueError("Vital Interposition requires 1 Spent VP")
        self.e.spend_vp(caster,1,mode="spent",label="b05:EX-LP-01")
        self.pending={"id":"EX-LP-01","host":host.ident,
                      "armed_round":self.e.round}
        self.armed_vital_turns.add((self.e.round,caster))
        self.e.log("b05_exaltation_armed",caster=caster,property="EX-LP-01",
                   host=host.ident,spent=1,budget=host.budget)

    def on_host_end(self,effect):
        if (self.pending is not None and effect.caster==self.caster
                and effect.ident==self.pending["host"]):
            pending=self.pending
            self.pending=None
            self.e.log("b05_exaltation_expired",caster=self.caster,
                       property=pending["id"],reason="exact_host_ended",
                       host=effect.ident)

    def on_step_start(self,actor_id):
        if actor_id==self.caster and self.pending is not None:
            self.e.log("b05_exaltation_expired",caster=actor_id,
                       property=self.pending["id"],reason="next_own_step")
            self.pending=None
        if actor_id==self.caster:
            self.last_held_step=None

    def arm_held(self,caster,points):
        """Only callable at the actual just-completed G0 Step-2 boundary."""
        a=self._source(caster)
        if (a.level<3 or self.chosen_name!="Guided Regeneration"
                or self.e.current!=caster or self.e.pending_regeneration!=caster
                or a.hp<=0 or self.pending is not None):
            raise ValueError("Held Renewal needs an actual conscious L3 Step 2")
        host=self._chosen_host()
        if (type(points) is not int or points not in (1,2)
                or not self.e.ledger
                or self.e.ledger[-1]["kind"]!="regeneration_step"
                or self.e.ledger[-1]["detail"]["actor"]!=caster):
            raise ValueError("Only 1 or 2 genuinely unused Step points may be held")
        step=self.e.ledger[-1]
        if self.last_held_step==step["index"]:
            raise ValueError("Step cannot arm Held Renewal twice")
        # Use exactly G4's live suppressed throughput, not an unsuppressed
        # build constant: toxin/regeneration suppression must not become
        # imaginary unused points available for Exaltation.
        available_throughput=max(
            0,a.regen+self.g3.regen_throughput(caster)
            +self.e.g4.toxins.modifier(caster,"regen_throughput"))
        remaining=available_throughput-step["detail"]["throughput_spent"]
        if (remaining<points or a.vp_available<1):
            raise ValueError("Cannot hold spent/suppressed throughput or unavailable VP")
        self.e.spend_vp(caster,1,mode="spent",label="b05:EX-LR-01")
        self.last_held_step=step["index"]
        self.pending={"id":"EX-LR-01","host":host.ident,
                      "points":points,"step":step["index"]}
        self.e.log("b05_exaltation_armed",caster=caster,property="EX-LR-01",
                   host=host.ident,points=points,step_index=step["index"],
                   spent=1)

    def preview_hp(self,recipient,packets,resolved):
        """Pure pre-wound HP proposal; never mutate budget on G5 preflight."""
        if recipient!=self.caster or self.pending is None or self.pending["id"]!="EX-LP-01":
            return tuple(resolved),None
        host=next((h for h in self._host()
                   if h.ident==self.pending["host"] and h.chosen),None)
        if host is None or host.budget is None or host.budget<=0:
            return tuple(resolved),None
        total=sum(n for p,n in zip(packets,resolved) if p.resource=="hp")
        if total<=0:
            return tuple(resolved),None
        prevent=min(2,total,host.budget//2)
        amounts=list(resolved)
        remaining=prevent
        # G4's G5 source profile emits primary first; no user rerouting.
        allocation=[]
        for i,(p,n) in enumerate(zip(packets,amounts)):
            if p.resource!="hp":
                continue
            used=min(n,remaining)
            amounts[i]-=used
            allocation.append({"index":i,"type":p.damage_type,
                               "mitigated":n,"prevented":used,
                               "residual":amounts[i]})
            remaining-=used
        return tuple(amounts),{"host":host.ident,"points":prevent,
                                "budget_cost":2*prevent,"allocation":allocation}

    def commit_hp(self,recipient,proposal,*,event_key):
        if proposal is None:
            return
        if recipient!=self.caster or self.pending is None or self.pending["id"]!="EX-LP-01":
            raise ValueError("Vital property not live at packet application")
        host=self._chosen_host()
        if host.ident!=proposal["host"] or host.budget<proposal["budget_cost"]:
            raise ValueError("Live host budget changed after native preflight")
        host.budget-=proposal["budget_cost"]
        self.pending=None
        self.e.log("b05_vital_interposition_applied",caster=recipient,
                   event_key=event_key,effect=host.ident,
                   prevented_hp=proposal["points"],
                   allocation=proposal["allocation"],
                   consumed_budget=proposal["budget_cost"],
                   budget_remaining=host.budget)
        if host.budget==0:
            self.g3._end(host,reason="budget_exhausted")

    def after_hp_loss(self,recipient,loss,*,event_key):
        if recipient!=self.caster or loss<=0 or self.pending is None:
            return
        if self.pending["id"]!="EX-LR-01":
            return
        arm=self.pending
        self.pending=None
        a=self.e.actors[recipient]
        host=next((h for h in self._host()
                   if h.ident==arm["host"] and h.chosen),None)
        healed=0
        if host is not None and a.hp>0 and not a.dead and a.vigor>0:
            healed=min(arm["points"],a.hp_max-a.hp,a.vigor)
            a.hp+=healed
            a.vigor-=healed
        self.e.log("b05_held_renewal_resolved",caster=recipient,
                   event_key=event_key,step_index=arm["step"],
                   incoming_hp_loss=loss,healed=healed,vigor_spent=healed,
                   no_extra_regeneration_step=True)
        self.e.check()
