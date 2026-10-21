"""B06 G6-D: one source-bound Reactive Intervene on paid Hunter Bite.

Bounded to the audited A ward/B Guardian pair, the *original* one-slot
Hunter B06-AT-04 sequence and actual 1x2 head-forward geometry.
Reuses G0's Reaction response window and already charged G0 defense/AP,
and G4's actual physical damage/wounds/venom. Prepared Intervene and
general G5 active protections require a separate window executor.

This path logs distinct protected-hit provenance, NOT a fictional G4.5
ordinary-target proof: Body Take Hit intentionally changes recipient.
"""
from copy import deepcopy
from dataclasses import dataclass

from scripts.b06_encounter_state_v0 import Response, Trigger, UnresolvedDecision
from scripts.b06_soldier_sentry_g5_v0 import _face


@dataclass(frozen=True)
class PreparedBite:
    actor_id: str
    ward_id: str
    hunter_id: str
    method: str
    trigger_key: str
    label: str
    delta: tuple
    final_cell: tuple
    reserved_mp: int
    source_digest: str


class ReactiveHunterProtection:
    def __init__(self,combat):
        e=combat.e
        if e.g1 is None or e.g3 is None or e.g4 is None or e.g5 is not combat:
            raise UnresolvedDecision("Protective Hunter Bite requires live G1/G4/G5")
        self.c,self.e=combat,e
        self.prepared={}

    def _eligibility(self,attacker,ward,protector,method):
        e=self.e
        h,w,p=(e.actors[x] for x in (attacker,ward,protector))
        if (h.source.source_id!="B06-EN-03"
                or w.source.source_id!="A"
                or p.source.source_id!="B"
                or len(w.occupied)!=1 or len(p.occupied)!=1
                or w.team!=p.team or h.team==w.team
                or h.hp<=0 or h.dead or w.dead or p.hp<=0 or p.dead
                or method not in ("shield_guard","body_take_hit")):
            raise UnresolvedDecision("G6-D Reactive Intervene needs Hunter/A/B live sources")
        if (h.footprint!=("head","rear") or len(h.occupied)!=2
                or not e.g1.melee_contact(attacker,ward,hunter_front=True)):
            raise UnresolvedDecision("Only genuine Hunter head-forward Bite")
        head=h.occupied[0]
        wp,pp=w.occupied[0],p.occupied[0]
        # Reachable shielding/body contact: the B Guardian must stand
        # adjacent to the ward and to the Hunter's actual head cell.
        # There is no gratis step, cross-room rescue or 1x2 rear reach.
        if (max(abs(pp[0]-wp[0]),abs(pp[1]-wp[1]))!=1
                or max(abs(pp[0]-head[0]),abs(pp[1]-head[1]))!=1):
            raise UnresolvedDecision("Protector cannot physically cover this Bite lane")
        if method=="shield_guard" and (
                (p.guard_instrument or "").lower() not in ("shield","buckler")
                or not p.ready_guard or p.guard_value is None
                or p.guard_remaining<1):
            raise ValueError("Ready Shield and normal Guard capacity required")
        return h,w,p

    def prepare(self,protector_id,ward_id,*,method,delta,trigger_key):
        """Precommit one actual G1 MP Interception and protective choice.

        The route is frozen on the Guardian's own turn, before the future
        Bite action ID exists. This scenario uses exactly one unthreatened
        cardinal movement step. The future response MUST release this
        exact G0 reservation; no free spontaneous Reaction substitutes it.
        """
        e=self.e
        hunters=[a.id for a in e.actors.values()
                 if a.source.source_id=="B06-EN-03"]
        if len(hunters)!=1 or protector_id not in e.actors or ward_id not in e.actors:
            raise UnresolvedDecision("One sourced Hunter and two PCs required")
        hunter_id=hunters[0]
        p=e.actors[protector_id]
        if (e.current!=protector_id or e.pending_regeneration is not None
                or p.source.source_id!="B"
                or method not in ("shield_guard","body_take_hit")):
            raise UnresolvedDecision("Only source Guardian on own ready turn may prepare")
        if (type(trigger_key) is not str or
                trigger_key!=f"g6d:prepared:{hunter_id}:{ward_id}:next_bite"):
            raise UnresolvedDecision("Prepared trigger must name next Hunter Bite against ward")
        if any(v.trigger_key==trigger_key for v in self.prepared.values()):
            raise ValueError("One pending prepared protection per named incoming Bite")
        delta=tuple(delta)
        if delta not in ((1,0),(-1,0),(0,1),(0,-1)):
            raise UnresolvedDecision("Bounded Prepared Intervene needs one cardinal step")
        destination,cost,kind,allies=e.g1.preview(protector_id,delta=delta)
        if (kind!="orthogonal" or allies
                or e.g1._threats(protector_id,destination,False)):
            raise UnresolvedDecision("Prepared route needs safe legal unthreatened step")
        before=p.occupied
        try:
            p.occupied=destination
            self._eligibility(hunter_id,ward_id,protector_id,method)
        finally:
            p.occupied=before
        if p.mp_remaining<cost:
            raise ValueError("Insufficient MP to precommit prepared route")
        label=e.g1.reserve_movement(protector_id,trigger_key,cost,
                                    label=f"protect:{ward_id}:{method}")
        self.prepared[label]=PreparedBite(
            protector_id,ward_id,hunter_id,method,trigger_key,label,
            delta,destination[0],cost,p.source.digest)
        e.log("g6d_prepared_protection_reserved",
              actor=protector_id,ward=ward_id,hunter=hunter_id,
              method=method,trigger=trigger_key,
              label=label,delta=delta,final_cell=destination[0],
              mp_reserved=cost,source_digest=p.source.digest)
        return label

    def resolve(self,sequence,*,protector_id,method,attack_face,
                damage_face=None,confirmation_face=None,critical_dice=(),
                wound_location_roll=None,venom_resistance_die=None,
                venom_resistance_modifier=0,prepared_label=None):
        e,c=self.e,self.c
        if (type(sequence) is not dict or sequence.get("profiles")!=("B06-AT-04",)
                or len(sequence.get("actions",()))!=1
                or len(sequence.get("defenses",()))!=1):
            raise UnresolvedDecision("One actual paid G5 Bite slot required")
        attacker,ward=sequence["attacker"],sequence["target"]
        if (attacker not in e.actors or ward not in e.actors
                or protector_id not in e.actors or
                len({attacker,ward,protector_id})!=3):
            raise ValueError("Distinct source actors required")
        if e.current!=attacker or e.pending_regeneration is not None:
            raise ValueError("Protector resolves during current Hunter attack only")
        prepared=None
        if prepared_label is not None:
            if type(prepared_label) is not str or prepared_label not in self.prepared:
                raise UnresolvedDecision("No genuine prior Prepared Intervene reservation")
            prepared=self.prepared[prepared_label]
            if (prepared.actor_id!=protector_id or prepared.ward_id!=ward
                    or prepared.hunter_id!=attacker or prepared.method!=method
                    or prepared.source_digest!=e.actors[protector_id].source.digest):
                raise UnresolvedDecision("Prepared reservation changed ward/method/source")
            p=e.actors[protector_id]
            before=p.occupied
            try:
                p.occupied=(prepared.final_cell,)
                h,w,p=self._eligibility(attacker,ward,protector_id,method)
            finally:
                p.occupied=before
            matching=[r for r in e.reservations
                      if r.label==prepared.label
                      and r.trigger_key==prepared.trigger_key
                      and r.actor_id==protector_id]
            reservation=e.g1.motion.get(prepared.label)
            if (len(matching)!=1 or reservation is None
                    or reservation.reserved_mp!=prepared.reserved_mp
                    or reservation.steps!=0 or reservation.spent_mp!=0
                    or any(r.trigger_key==prepared.trigger_key
                           and r.label!=prepared.label for r in e.reservations)):
                raise UnresolvedDecision("Prepared G1 saved MP or trigger provenance invalid")
        else:
            h,w,p=self._eligibility(attacker,ward,protector_id,method)
            if not p.reaction_available:
                raise ValueError("Guardian Reaction unavailable")
        if type(venom_resistance_modifier) is not int:
            raise ValueError("Venom resistance modifier must be integer")
        if venom_resistance_die is not None:
            _face(venom_resistance_die,20,"venom resistance")
        action_index,defense_index=sequence["actions"][0],sequence["defenses"][0]
        declaration=sequence["declaration"]
        if any(type(x) is not int or x<0 or x>=len(e.ledger)
               for x in (action_index,defense_index,declaration)):
            raise UnresolvedDecision("Invalid native attack/defense indices")
        native=e.ledger[declaration]
        if (native["kind"]!="attack_sequence_committed" or
                native["round"]!=e.round or native["turn"]!=attacker or
                native["detail"].get("attacker")!=attacker or
                native["detail"].get("target")!=ward or
                native["detail"].get("profiles")!=["B06-AT-04"] or
                not any(x["kind"]=="g5_melee_sequence_attested"
                        and x["detail"].get("declaration_index")==declaration
                        and x["detail"].get("action_indices")==[action_index]
                        and x["detail"].get("defense_indices")==[defense_index]
                        for x in e.ledger[declaration+1:])):
            raise UnresolvedDecision("Original paid G5 Bite declaration not attested")
        action=e.ledger[action_index]
        d=e.ledger[defense_index]
        if (action["kind"]!="action_committed" or
                action["round"]!=e.round or action["turn"]!=attacker or
                action["detail"].get("actor")!=attacker or
                action["detail"].get("action_class")!="physical" or
                action["detail"].get("label")!="sequence:B06-AT-04:0"
                or d["kind"]!="defense_assigned" or
                d["round"]!=e.round or d["turn"]!=attacker or
                d["detail"].get("actor")!=ward or
                d["detail"].get("attack_key")!=f"{attacker}:{ward}:0" or
                d["detail"].get("defense")!=native["detail"]["defenses"][0]):
            raise UnresolvedDecision("Bite paid action/ward defense provenance invalid")
        if c.bridge._bound_attack_declaration(attacker,ward,"B06-AT-04",action_index)!=(declaration,0):
            raise UnresolvedDecision("G4.5 could not bind original paid Bite")
        if (len(c.pending_attack_slots(attacker))!=1
                or c.pending_attack_slots(attacker)[0]["action_index"]!=action_index
                or any(x["kind"] in ("g5_melee_resolved","g5_melee_cancelled")
                       and x["detail"].get("action_index")==action_index
                       for x in e.ledger)):
            raise UnresolvedDecision("Bite slot already used or another pending attack")
        key=(prepared.trigger_key if prepared is not None
             else f"g5:melee:{action_index}")
        if prepared is None and any(r.trigger_key==key for r in e.reservations):
            raise UnresolvedDecision("Reserved Interception needs explicit executor")
        declared=d["detail"]["defense"]
        original_defense="take_hit" if w.hp<=0 else declared
        original_value=(None if original_defense=="take_hit"
                        else d["detail"]["defense_value"])
        if original_defense=="guard" and (
                not w.ready_guard or not w.guard_instrument):
            raise UnresolvedDecision("Original ward lost legal personal Guard")
        if any(str(x).lower()=="prone" for x in h.conditions+w.conditions):
            raise UnresolvedDecision("Prone protective Bite requires separate feasibility")
        source_bonus=c._profile(attacker,"B06-AT-04")
        face=_face(attack_face,20,"original Bite")
        total=face+source_bonus
        original_hit=face!=1 and (
            original_defense=="take_hit" or face==20 or total>original_value)
        if face==20:
            confirm=_face(confirmation_face,20,"single Bite confirmation")
        else:
            if confirmation_face is not None:
                raise ValueError("No confirmation without natural 20")
            confirm=None
        shield_value=p.guard_value if method=="shield_guard" else None
        stopped=bool(method=="shield_guard" and original_hit and face!=20
                     and total<=shield_value)
        hit=original_hit and not stopped
        recipient=(protector_id if hit and method=="body_take_hit" else ward)
        confirmation_defense=(shield_value if method=="shield_guard"
                              else original_value)
        critical="normal"
        if hit and face==20:
            if confirm==20:
                critical="devastating"
            elif method=="body_take_hit" and original_defense=="take_hit":
                critical="critical"
            elif confirm!=1 and confirm+source_bonus>confirmation_defense:
                critical="critical"
            else:
                critical="strong"
        required={"normal":0,"strong":1,"critical":2,"devastating":2}[critical]
        if (type(critical_dice) not in (tuple,list)
                or len(critical_dice)!=(required if hit else 0)
                or any(type(x) is not int or not 1<=x<=4 for x in critical_dice)):
            raise ValueError("Exactly sourced critical d4 faces required")
        venom_key=f"g6d:protective-bite:{e.seed}:{action_index}"
        if hit:
            _face(damage_face,6,"source Bite damage")
            prediction=e.g4.preflight_profile_hit(
                attacker,recipient,"B06-AT-04",die_face=damage_face,
                critical=critical,critical_dice=tuple(critical_dice),
                wound_location_roll=wound_location_roll)
            if prediction["hp_after"]>-e.actors[recipient].hp_max:
                e.g4.venom.validate_exposure_key(venom_key)
            _,_,packets=e.g4._profile_hit_packets(
                attacker,recipient,"B06-AT-04",die_face=damage_face,
                critical=critical,critical_dice=tuple(critical_dice))
            if (e.g4._mitigate_hp(e.actors[recipient],packets[0])>0
                    and prediction["hp_after"]>-e.actors[recipient].hp_max
                    and e.g4.venom.bite_resistance_required(recipient)
                    and venom_resistance_die is None):
                raise UnresolvedDecision("Potential puncturing Bite needs venom resistance d20")
        elif damage_face is not None or wound_location_roll is not None:
            raise ValueError("Stopped/missed Bite cannot invent damage or a wound")
        trigger=Trigger(key,attacker,ward)
        choice=(None if prepared is not None else
                Response(protector_id,"reaction",
                         f"g6d:reactive:{method}:{action_index}"))
        live=[]
        def recheck(encounter,tr):
            tr.legal=(encounter.current==attacker and
                      c._contact(attacker,ward) and
                      encounter.actors[attacker].hp>0 and
                      not encounter.actors[ward].dead)
            if tr.legal and prepared is not None:
                # A prepared movement is the ONLY conditional protection
                # authority after it really reaches the original attack.
                self._eligibility(attacker,ward,protector_id,method)
        def on_interception(encounter,tr,res):
            if (prepared is None or res.label!=prepared.label
                    or res.actor_id!=protector_id
                    or tr.key!=prepared.trigger_key):
                raise UnresolvedDecision("Unrecognized source MP Interception")
            entry=e.g1.motion.pop(res.label,None)
            if entry is None or entry.steps!=0 or entry.spent_mp!=0:
                raise UnresolvedDecision("Prepared MP already consumed")
            released=next((x for x in reversed(e.ledger)
                           if x["kind"]=="interception_released"
                           and x["detail"].get("actor")==protector_id
                           and x["detail"].get("trigger")==key
                           and x["detail"].get("label")==res.label),None)
            if released is None:
                raise UnresolvedDecision("G0 never released promised MP reservation")
            moved=e.g1._movement(
                protector_id,delta=prepared.delta,reserved=entry,
                trigger_key=f"{key}:saved_mp_step",responses=())
            if (moved is not True or entry.steps!=1
                    or entry.spent_mp!=prepared.reserved_mp
                    or e.actors[protector_id].occupied!=(prepared.final_cell,)):
                raise UnresolvedDecision("Prepared protector failed original G1 move")
            self._eligibility(attacker,ward,protector_id,method)
            e.log("g6d_prepared_protection_arrived",
                  actor=protector_id,ward=ward,trigger=key,
                  release_index=released["index"],
                  mp_spent=entry.spent_mp,steps=entry.steps)
            live.append(released["index"])
        def on_response(encounter,tr,response):
            if not encounter.is_live_spontaneous(tr,response) or response!=choice:
                raise UnresolvedDecision("Protection requires live G0 Reaction")
            self._eligibility(attacker,ward,protector_id,method)
            receipt=next((x for x in reversed(encounter.ledger)
                          if x["kind"]=="spontaneous_committed" and
                          x["detail"].get("trigger")==key
                          and x["detail"].get("actor")==protector_id
                          and x["detail"].get("label")==choice.label),None)
            if receipt is None:
                raise UnresolvedDecision("No native Reaction payment evidence")
            live.append(receipt["index"])
        valid=e.response_window(
            trigger,on_interception=on_interception,
            spontaneous=() if prepared is not None else (choice,),
            on_spontaneous=None if prepared is not None else on_response,
            after_interceptions=recheck)
        if not valid or len(live)!=1:
            raise UnresolvedDecision("Protection did not reach live original Bite")
        if prepared is not None:
            del self.prepared[prepared.label]
        shield_event=None
        if method=="shield_guard" and original_hit:
            defense_before=len(e.ledger)
            val=e.defense(protector_id,"guard",
                          attack_key=f"g6d:shield:{action_index}")
            if val!=shield_value:
                raise UnresolvedDecision("Shield Guard changed after preflight")
            shield_event=defense_before
        e.log("g5_melee_roll",action_index=action_index,
              declaration_index=declaration,slot=0,
              attacker=attacker,target=ward,profile="B06-AT-04",
              defense=original_defense,defense_value=original_value,
              attack_face=face,source_attack_bonus=source_bonus,
              attack_bonus=source_bonus,attack_total=total,
              confirmation_face=confirm,critical=critical,
              hit=hit,spontaneous_policy=("g6d:prepared_intervene"
                    if prepared is not None else "g6d:reactive_intervene"))
        damage=None
        if hit:
            damage=e.g4.apply_profile_hit(
                attacker,recipient,"B06-AT-04",die_face=damage_face,
                confirmed_hit=True,critical=critical,
                critical_dice=tuple(critical_dice),
                wound_location_roll=wound_location_roll)
            if not e.actors[recipient].dead:
                damage["venom"]=e.g4.venom.apply_bite(
                    attacker,recipient,profile_hit_index=len(e.ledger)-1,
                    exposure_key=venom_key,
                    resistance_die=venom_resistance_die,
                    resistance_modifier=venom_resistance_modifier)
        e.log("g6d_protective_bite_attested",
              action_index=action_index,declaration_index=declaration,
              ward_defense_index=defense_index,
              reaction_index=live[0] if prepared is None else None,
              interception_index=live[0] if prepared is not None else None,
              activation="prepared" if prepared is not None else "reactive",
              shield_defense_index=shield_event,
              attacker=attacker,ward=ward,protector=protector_id,
              method=method,original_hit=original_hit,
              original_defense=original_defense,
              original_defense_value=original_value,
              attack_total=total,shield_value=shield_value,
              shield_stopped=stopped,recipient=recipient if hit else None,
              critical=critical,source_digest=h.source.digest,
              protector_source_digest=p.source.digest,damage=deepcopy(damage))
        e.log("g5_melee_resolved",action_index=action_index,
              attacker=attacker,target=ward,profile="B06-AT-04",
              outcome="hit" if hit else "miss",damage=deepcopy(damage),
              protective_recipient=recipient if hit else None,
              critical=critical)
        e.check()
        return {"outcome":"shield_stopped" if stopped else
                "body_hit" if hit and method=="body_take_hit" else
                "ward_hit" if hit else "miss",
                "original_hit":original_hit,"critical":critical,
                "recipient":recipient if hit else None,
                "damage":deepcopy(damage),
                "reaction_index":live[0] if prepared is None else None,
                "interception_index":live[0] if prepared is not None else None,
                "shield_defense_index":shield_event,
                "action_index":action_index}
