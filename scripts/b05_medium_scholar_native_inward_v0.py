"""B04/B05 native Medium Scholar Inward profiles, one verified S source.

Binds source-approved MS Stone/Guided to G0 AP/VP, G1 genuine MP,
G3 maintained effects, G4 typed mitigation and one actual G0 Step2.
No self-Projection-to-Inward inference, fabricated bonus steps or combat AI.
"""
from scripts.b05_medium_scholar_l1_l3_v0 import profile
from scripts.b05_scholar_inward_embodiment_profiles_v0 import (
    PROFILES, MEDIUM, BASE_MOVEMENT_MP,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint


class MediumScholarInward:
    def __init__(self, encounter, caster):
        if encounter.g3 is None or encounter.g1 is None or encounter.g4 is None:
            raise ValueError("G0/G1/G3/G4 source engines required")
        if encounter.g3.medium_scholar is not None:
            raise ValueError("Only one native Medium Scholar adapter per scene v0")
        self.e = encounter
        self.g3 = encounter.g3
        self.caster = caster
        self.effect_id = None
        self.steps = 0
        self.charged_mp = 0
        self.mp_turn_round = None
        self._scholar()
        self.g3.medium_scholar = self
        self.e.log("b05_medium_scholar_inward_installed", caster=caster,
                   source_digest=self.e.actors[caster].source.digest)

    def _scholar(self):
        a = self.e.actors.get(self.caster)
        if a is None or a.source.source_id != "S" or a.focus != "Medium":
            raise UnresolvedDecision("Only authored S Medium Scholar can use Inward")
        p = profile(a.level)
        path = "scripts/b05_medium_scholar_l1_l3_v0.py"
        equipment = tuple(sorted((name,
            "worn" if name == "Leather armor" else
            "wielded" if name == "Sword" else "carried")
            for name in p["equipment_sp"]))
        if (a.source.path != path
                or a.source.digest != _fingerprint(path)
                or a.source.start_state != f"L{a.level}-medium-scholar-inward"
                or a.source.status != "STRUCTURAL_B05_ONLY"
                or a.source.attack_profiles != ("B05-PC-S-SWORD-CUT",)
                or a.source.equipment != equipment
                or dict(a.source.abilities) != p["abilities"]
                or dict(a.source.training) != p["weapon_training"]
                or a.vp_max != p["vp_max"]
                or a.hp_max != p["hp_max"]
                or a.vigor_max != p["vigor_max"]
                or a.initiative_bonus != p["initiative"]
                or a.projection_ap != 24
                or a.physical_ap != 24
                or a.guard_instrument != p["guard_instrument"]
                or a.guard_value != p["guard_value"]
                or a.guard_capacity != p["normal_guard_capacity"]
                or a.regen != p["normal_regen_throughput"]):
            raise UnresolvedDecision("Medium Scholar live source sheet mismatch")
        return a,p

    def _own(self):
        a,p=self._scholar()
        if (self.e.current != self.caster or
                self.e.pending_regeneration is not None):
            raise ValueError("Inward decision requires ready own turn")
        if a.dead or a.hp<=0:
            raise ValueError("Incapacitated Medium Scholar")
        if (getattr(self.e,"g5",None) is not None and
                self.e.g5.pending_attack_slots(self.caster)):
            raise UnresolvedDecision("Cannot alter Inward before resolving G5 slots")
        return a,p

    def _target_profile(self, ident, p):
        if ident not in MEDIUM or type(ident) is not str:
            raise UnresolvedDecision("No compatible authored Medium Inward profile")
        candidate=PROFILES[ident]
        if candidate.technique not in p["known_pillar_techniques"]:
            raise UnresolvedDecision("Technique not individually learned")
        return candidate

    def _has_named_effect_conflict(self, kind):
        """No duplicate named spell from this caster *or* on this recipient.

        G3.active(caster, kind) only checks the original caster. A distinct
        Priest may already maintain Guided Regeneration on the Scholar;
        both activation and free-AP rerouting must reject that recipient
        collision before committing any AP, VP, MP or existing host.
        """
        return bool(self.g3.active(self.caster, kind)) or any(
            effect.kind == kind and effect.recipient == self.caster
            for effect in self.g3.effects.values())

    def _host(self):
        if self.effect_id is None:
            return None
        host=self.g3.effects.get((self.caster,self.effect_id))
        if host is None or host.caster!=self.caster or host.committed!=1 or (
                host.kind not in ("Stone Skin","Guided Regeneration")):
            raise AssertionError("Live G3 Inward host no longer matches reserved ID")
        return host

    def _current_ident(self):
        host=self._host()
        if host is None:
            return None
        ident=("MS-STONE-BODY-T1" if host.kind=="Stone Skin"
               else "MS-GUIDED-REGEN-T1")
        return ident

    def _reconcile_mp(self, steps):
        """Preflight the real remaining MP before a paid configuration change."""
        if type(steps) is not int or steps<0 or steps>2:
            raise ValueError("Authored Overroute range is 0-2")
        a,_=self._scholar()
        if self.mp_turn_round != self.e.round:
            raise UnresolvedDecision("G0 has not established this own turn's MP")
        needed=2*steps
        delta=needed-self.charged_mp
        if delta>0 and a.mp_remaining<delta:
            raise ValueError("Already-spent ordinary MP cannot fund stronger Overroute")
        # Adding back *withheld, unspent* MP on a drop is legal;
        # no G1 movement receipt is reversed or refunded.
        return delta

    def _apply_mp(self,delta):
        a,_=self._scholar()
        a.mp_remaining-=delta
        self.charged_mp+=delta
        if a.mp_remaining<0 or self.charged_mp<0 or self.charged_mp>4:
            raise AssertionError("Unreconciled native MP forfeiture")
        self.e.log("b05_medium_scholar_mp_reconciled",caster=self.caster,
                   withheld=self.charged_mp,delta=delta,
                   mp_remaining=a.mp_remaining)

    def on_turn_resources(self, actor_id):
        """Native G0 Step4 hook: apply sustained Overroute once after MP refresh."""
        if actor_id!=self.caster:
            return
        a,_=self._scholar()
        if self.mp_turn_round == self.e.round:
            raise ValueError("Medium Scholar own-turn MP already established")
        needed=2*self.steps if self._host() else 0
        if a.mp_remaining<needed:
            raise UnresolvedDecision("Cannot sustain stronger Overroute with source MP impairment")
        a.mp_remaining-=needed
        self.charged_mp=needed
        self.mp_turn_round=self.e.round
        self.e.log("b05_medium_scholar_turn_mp",caster=self.caster,
                   overroute_steps=self.steps, withheld=needed,
                   native_allowance=a.mp_remaining)
        self.e.check()

    def _establish(self,ident,steps=0):
        p=PROFILES[ident]
        effect=self.g3._new_effect(
            self.caster,p.technique,self.caster,1,
            resistance=(1+steps if p.channel=="Body" else 0))
        self.effect_id=effect.ident
        self.steps=steps
        self.e.log("b05_medium_scholar_inward_active",
                   caster=self.caster, profile=ident, effect=effect.ident,
                   channel=p.channel, committed=1, overroute_steps=steps)
        return effect

    def activate(self, ident):
        a,p=self._own()
        self._target_profile(ident,p)
        if self._host() is not None:
            raise ValueError("One active Inward at levels 1-3")
        kind=PROFILES[ident].technique
        if self._has_named_effect_conflict(kind):
            raise ValueError("Cannot stack same named G3 spell on recipient")
        if a.ap_remaining<24 or a.vp_available<1:
            raise ValueError("Inward activation requires 24 AP and 1 Available VP")
        self.e.spend_ap(self.caster,"projection",label="b05:scholar:activate:"+ident)
        if a.hp<=0 or a.vp_available<1 or self._has_named_effect_conflict(kind):
            self.e.log("b05_medium_scholar_activation_interrupted",
                       caster=self.caster,profile=ident)
            return None
        self.e.spend_vp(self.caster,1,mode="committed",label="b05:scholar:"+ident)
        host=self._establish(ident)
        self.e.check()
        return host

    def regen_bonus(self,actor_id):
        """Only G3's real G0/G4 Step-2 calculation consumes this value."""
        if actor_id != self.caster:
            return None
        host=self._host()
        if host is None:
            return None
        return 1+self.steps if host.kind=="Guided Regeneration" else None

    def on_host_end(self,effect):
        if effect.caster==self.caster and effect.ident==self.effect_id:
            self.e.log("b05_medium_scholar_inward_ended",
                       caster=self.caster,effect=effect.ident,
                       profile=("MS-STONE-BODY-T1" if effect.kind=="Stone Skin"
                                else "MS-GUIDED-REGEN-T1"))
            self.effect_id=None
            self.steps=0
            # Withheld MP expires with this turn; ending a spell from
            # damage/death never creates free MP out of turn.

    def release(self):
        self._own()
        host=self._host()
        if host is None:
            raise ValueError("No active Medium Inward to release")
        self._reconcile_mp(0)
        delta=-self.charged_mp
        self.g3._end(host,reason="medium_scholar_voluntary_release")
        self._apply_mp(delta)
        self.e.check()

    def reroute(self,ident,*,overroute_steps=0):
        a,p=self._own()
        candidate=self._target_profile(ident,p)
        old=self._host()
        if old is None:
            raise ValueError("Rerouting requires active original Inward")
        old_id=self._current_ident()
        if old_id==ident:
            raise ValueError("No same-host free refresh via rerouting")
        if PROFILES[old_id].channel==candidate.channel:
            raise UnresolvedDecision("No distinct same-channel compatible mode")
        if (type(overroute_steps) is not int or
                not 0<=overroute_steps<=2 or
                (overroute_steps and a.level<3)):
            raise ValueError("Only L3 may reroute into authored Overroute")
        fee=(3 if a.level<3 else 2)+overroute_steps
        if a.vp_available+old.committed<fee+1:
            raise ValueError("Reroute cannot afford full Spent plus Committed")
        if self._has_named_effect_conflict(candidate.technique):
            raise ValueError("Replacement would duplicate named G3 effect on recipient")
        delta=self._reconcile_mp(overroute_steps)
        self.g3._end(old,reason="medium_scholar_reroute")
        self.e.spend_vp(self.caster,fee,mode="spent",
                        label="b05:scholar:reroute")
        self.e.spend_vp(self.caster,1,mode="committed",
                        label="b05:scholar:replacement")
        new=self._establish(ident,overroute_steps)
        self._apply_mp(delta)
        self.e.log("b05_medium_scholar_rerouted",
                   caster=self.caster,from_profile=old_id,to_profile=ident,
                   spent=fee,overroute_steps=overroute_steps,ap=0)
        self.e.check()
        return new

    def overroute(self,steps):
        a,p=self._own()
        host=self._host()
        if host is None or a.level<3:
            raise ValueError("Active Level-3 Inward host required")
        if type(steps) is not int or not 0<=steps<=2:
            raise ValueError("Overroute supports 0-2 authored steps")
        old=self.steps
        if old==steps:
            return host
        if old and steps<old and steps!=0:
            raise ValueError("Free Overroute drop is only to normal mode")
        cost=max(0,steps-old)
        if a.vp_available<cost:
            raise ValueError("Additional Overroute step must be paid")
        delta=self._reconcile_mp(steps)
        if cost:
            self.e.spend_vp(self.caster,cost,mode="spent",
                            label="b05:scholar:overroute")
        self.steps=steps
        host.resistance=(1+steps if host.kind=="Stone Skin" else 0)
        self._apply_mp(delta)
        self.e.log("b05_medium_scholar_overroute",
                   caster=self.caster,from_steps=old,to_steps=steps,
                   spent=cost,effective_mp_cap=BASE_MOVEMENT_MP-2*steps)
        self.e.check()
        return host
