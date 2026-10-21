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

from scripts.b06_encounter_state_v0 import Response, Trigger, UnresolvedDecision
from scripts.b06_soldier_sentry_g5_v0 import _face


class ReactiveHunterProtection:
    def __init__(self,combat):
        e=combat.e
        if e.g1 is None or e.g3 is None or e.g4 is None or e.g5 is not combat:
            raise UnresolvedDecision("Protective Hunter Bite requires live G1/G4/G5")
        self.c,self.e=combat,e

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

    def resolve(self,sequence,*,protector_id,method,attack_face,
                damage_face=None,confirmation_face=None,critical_dice=(),
                wound_location_roll=None,venom_resistance_die=None,
                venom_resistance_modifier=0):
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
        key=f"g5:melee:{action_index}"
        if any(r.trigger_key==key for r in e.reservations):
            raise UnresolvedDecision("Prepared Intervene needs native MP movement executor")
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
        choice=Response(protector_id,"reaction",
                        f"g6d:reactive:{method}:{action_index}")
        live=[]
        def recheck(encounter,tr):
            tr.legal=(encounter.current==attacker and
                      c._contact(attacker,ward) and
                      encounter.actors[attacker].hp>0 and
                      not encounter.actors[ward].dead)
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
        valid=e.response_window(trigger,on_interception=lambda *args: None,
                                spontaneous=(choice,),on_spontaneous=on_response,
                                after_interceptions=recheck)
        if not valid or len(live)!=1:
            raise UnresolvedDecision("Protective response did not reach live original Bite")
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
              hit=hit,spontaneous_policy="g6d:reactive_intervene")
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
              reaction_index=live[0],shield_defense_index=shield_event,
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
                "reaction_index":live[0],"shield_defense_index":shield_event,
                "action_index":action_index}
