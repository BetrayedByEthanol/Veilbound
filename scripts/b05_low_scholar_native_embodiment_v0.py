"""B04/B05 source T Low Scholar G0/G3/G4 native Embodiment adapter.

Only two authored prepared Self modes. G3 effect hosts own VP/typed
resistance; native G0/G4 Step2 owns healing, no self-issued Step receipt.
"""
from scripts.b05_low_scholar_l1_l3_v0 import profile
from scripts.b05_scholar_inward_embodiment_profiles_v0 import (
    PROFILES, LOW, committed_cost,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint


class LowScholarEmbodiment:
    def __init__(self, encounter, caster):
        if any(getattr(encounter,part,None) is None for part in ("g1","g3","g4")):
            raise ValueError("Install source G1/G3/G4 before Low Embodiment")
        if encounter.g3.low_scholar is not None:
            raise ValueError("One bounded native Low Scholar adapter per scene")
        self.e=encounter
        self.g3=encounter.g3
        self.caster=caster
        self.effect_id=None
        self.intensified=False
        self._stone_intensified_on_round=None
        self._step_open_at=None
        self._step_live=False
        self._scholar()
        self.g3.low_scholar=self
        self.e.log("b05_low_scholar_embodiment_installed",
                   caster=caster,source_digest=self.e.actors[caster].source.digest)

    def _scholar(self):
        a=self.e.actors.get(self.caster)
        if a is None or a.source.source_id!="T" or a.focus!="Low":
            raise UnresolvedDecision("Only source T Low Scholar supports Embodiment")
        p=profile(a.level)
        path="scripts/b05_low_scholar_l1_l3_v0.py"
        equipment=tuple(sorted((name,
            "worn" if name=="Leather armor" else
            "wielded" if name=="Sword" else "carried")
            for name in p["equipment_sp"]))
        if (a.source.path!=path
                or a.source.digest!=_fingerprint(path)
                or a.source.status!="STRUCTURAL_B05_ONLY"
                or a.source.start_state!=f"L{a.level}-low-scholar-prepared"
                or a.source.attack_profiles!=()
                or a.source.equipment!=equipment
                or dict(a.source.abilities)!=p["abilities"]
                or dict(a.source.training)!=p["weapon_training"]
                or a.hp_max!=p["hp_max"] or a.vigor_max!=p["vigor_max"]
                or a.vp_max!=p["vp_max"]
                or a.initiative_bonus!=p["initiative"]
                or a.physical_ap!=20 or a.projection_ap!=30
                or a.guard_instrument!=p["guard_instrument"]
                or a.guard_value!=p["guard_value"]
                or a.guard_capacity!=p["normal_guard_capacity"]
                or a.regen!=p["normal_regen_throughput"]):
            raise UnresolvedDecision("Low Scholar live source sheet mismatch")
        return a,p

    def _own(self):
        a,p=self._scholar()
        if self.e.current!=self.caster or self.e.pending_regeneration is not None:
            raise ValueError("Embodiment requires ready own turn")
        if a.hp<=0 or a.dead:
            raise ValueError("Dying or dead Scholar cannot activate")
        if (getattr(self.e,"g5",None) is not None
                and self.e.g5.pending_attack_slots(self.caster)):
            raise UnresolvedDecision("Pending G5 sequence forbids Embodiment change")
        return a,p

    def _candidate(self,ident,p):
        if type(ident) is not str or ident not in LOW:
            raise UnresolvedDecision("Only two authored Low Embodiment IDs")
        candidate=PROFILES[ident]
        if (candidate.technique not in p["known_pillar_techniques"]
                or candidate.technique not in p["prepared_techniques"]):
            raise UnresolvedDecision("Low Scholar did not individually prepare technique")
        return candidate

    def _host(self):
        if self.effect_id is None:
            return None
        host=self.g3.effects.get((self.caster,self.effect_id))
        if (host is None or host.caster!=self.caster
                or host.recipient!=self.caster
                or host.kind not in ("Stone Skin","Guided Regeneration")
                or host.committed!=committed_cost(
                    PROFILES[self._profile_id(host.kind)],
                    self.e.actors[self.caster].vp_max)):
            raise AssertionError("G3 Low Scholar host/commitment mismatch")
        return host

    @staticmethod
    def _profile_id(kind):
        return ("LS-STONE-BODY-T1" if kind=="Stone Skin"
                else "LS-GUIDED-REGEN-T1" if kind=="Guided Regeneration"
                else None)

    def current_profile(self):
        host=self._host()
        return self._profile_id(host.kind) if host is not None else None

    def _named_conflict(self,kind):
        # active(caster, kind) is not sufficient: another Priest or Scholar
        # may already maintain the same named spell on this beneficiary.
        return bool(self.g3.active(self.caster,kind)) or any(
            v.kind==kind and v.recipient==self.caster
            for v in self.g3.effects.values())

    def _stone_base(self):
        # Snapshot live sourced Veil Control on activation, not an AP bonus.
        a,_=self._scholar()
        vc=dict(a.source.abilities)["Veil Control"]
        if type(vc) is not int:
            raise UnresolvedDecision("No source Veil Control")
        return 2+max(0,vc)//4

    def activate(self,ident):
        a,p=self._own()
        candidate=self._candidate(ident,p)
        if self._host() is not None:
            raise ValueError("Low L1-3 has one Active Embodiment; release first")
        if self._named_conflict(candidate.technique):
            raise ValueError("Named Embodiment already exists on caster/recipient")
        cost=committed_cost(candidate,a.vp_max)
        if a.ap_remaining<30 or a.vp_available<cost:
            raise ValueError("Low Embodiment needs fresh 30 AP and full VP reserve")
        self.e.spend_ap(self.caster,"projection",
                        label="b05:low_scholar:activate:"+ident)
        # Post-commit recheck: interrupted cast loses paid AP, no VP/host.
        if (a.hp<=0 or a.dead or a.vp_available<cost
                or self._host() is not None
                or self._named_conflict(candidate.technique)):
            self.e.log("b05_low_scholar_activation_interrupted",
                       caster=self.caster,profile=ident)
            return None
        resistance=(self._stone_base() if candidate.channel=="Body" else 0)
        self.e.spend_vp(self.caster,cost,mode="committed",
                        label="b05:low_scholar:"+ident)
        host=self.g3._new_effect(self.caster,candidate.technique,self.caster,
                                 cost,resistance=resistance)
        self.effect_id=host.ident
        self.intensified=False
        self._stone_intensified_on_round=None
        self.e.log("b05_low_scholar_embodiment_active",
                   caster=self.caster,effect=host.ident,profile=ident,
                   committed=cost,resistance=resistance)
        self.e.check()
        return host

    def on_host_end(self,effect):
        if effect.caster==self.caster and effect.ident==self.effect_id:
            self.e.log("b05_low_scholar_embodiment_ended",caster=self.caster,
                       effect=effect.ident,profile=self._profile_id(effect.kind),
                       intensified_lost=self.intensified)
            self.effect_id=None
            self.intensified=False
            self._stone_intensified_on_round=None
            self._step_live=False
            self._step_open_at=None

    def release(self):
        self._own()
        host=self._host()
        if host is None:
            raise ValueError("No Low Embodiment host to release")
        self.g3._end(host,reason="low_scholar_voluntary_release")
        self.e.check()

    def intensify(self):
        a,p=self._own()
        if a.level<3:
            raise ValueError("Deep Embodiment requires Level 3")
        host=self._host()
        if host is None:
            raise ValueError("Only a live prepared Embodiment may Intensify")
        self._candidate(self._profile_id(host.kind),p)
        if self.intensified:
            raise ValueError("Unexpired Intensification cannot be purchased twice")
        if a.vp_available<1:
            raise ValueError("No Available VP for 1 Spent Intensification")
        self.e.spend_vp(self.caster,1,mode="spent",
                        label="b05:low_scholar:intensify")
        self.intensified=True
        if host.kind=="Stone Skin":
            host.resistance+=1
            self._stone_intensified_on_round=self.e.round
        self.e.log("b05_low_scholar_intensified",caster=self.caster,
                   effect=host.ident,effect_kind=host.kind,spent=1,
                   window=("next_own_turn_begin" if host.kind=="Stone Skin"
                           else "next_actual_G0_Step2"))
        self.e.check()
        return host

    def on_step_start(self,actor_id):
        """Only G0's current Step2 transition may open this marker."""
        if actor_id!=self.caster:
            return
        a,_=self._scholar()
        if (self.e.current!=actor_id or self.e.pending_regeneration!=actor_id
                or actor_id in self.e.regen_done):
            raise UnresolvedDecision("Only actual pending G0 Step2 may arm Embodiment")
        host=self._host()
        if host is not None and host.kind=="Stone Skin" and self.intensified:
            # Own next turn begins: original Stone host remains, plus-one ends.
            if self._stone_intensified_on_round is None or (
                    self.e.round<=self._stone_intensified_on_round):
                raise AssertionError("Stone intensity cannot expire on activation turn")
            host.resistance-=1
            self.intensified=False
            self._stone_intensified_on_round=None
            self.e.log("b05_low_scholar_stone_intensity_expired",
                       caster=self.caster,effect=host.ident,
                       resistance=host.resistance)
        if not self._step_live:
            self._step_open_at=len(self.e.ledger)
            self._step_live=True

    def regen_bonus(self,actor_id):
        """Returns pending intensity only inside a live G0 Step2 boundary."""
        if actor_id!=self.caster:
            return None
        host=self._host()
        if host is None or host.kind!="Guided Regeneration":
            return None
        return 1+int(self.intensified and self._step_live and
                     self.e.pending_regeneration==actor_id and
                     actor_id not in self.e.regen_done)

    def on_step_complete(self,actor_id):
        if actor_id!=self.caster:
            return
        if not self._step_live or self._step_open_at is None or (
                actor_id not in self.e.regen_done):
            raise AssertionError("No authenticated completed Low Scholar Step2")
        receipts=[v for v in self.e.ledger[self._step_open_at:]
                  if v["kind"] in ("regeneration_step","regeneration_dead")
                  and v["detail"]["actor"]==actor_id]
        if len(receipts)!=1:
            raise AssertionError("One native Step2 receipt needed to consume intensity")
        host=self._host()
        if (host is not None and host.kind=="Guided Regeneration"
                and self.intensified):
            self.intensified=False
            self.e.log("b05_low_scholar_guided_intensity_consumed",
                       caster=self.caster,effect=host.ident,
                       step2_index=receipts[0]["index"],
                       hp_restored=receipts[0]["detail"].get("hp_restored",0))
        self._step_live=False
        self._step_open_at=None
        self.e.check()
