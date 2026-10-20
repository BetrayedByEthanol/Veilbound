"""B06 G4.4: Hunter's source-bound delayed venom and fixed Venom Endurance.

No new attack/ward is authorized: Bite must exist in G4's actual hit ledger;
Venom Endurance requires an independently attested legal prepared Prayer.
"""
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _integer

HUNTER="B06-TX-HUNTER-SLOW-MY"
BITES=frozenset(("B06-AT-04","B06-AT-06"))
COVERED=frozenset(("TX-HM","TX-NE","TX-CY","TX-NC","TX-MY","TX-CA",
                   "TX-HE","TX-NP","TX-PN","TX-EN","TX-DE",HUNTER))
CONTINUOUS_SHORT=frozenset(("TX-NE","TX-MY","TX-CA","TX-PN","TX-DE"))
CONTINUOUS_LONG=frozenset(("TX-EN",HUNTER))
DISCRETE=frozenset(("TX-HM","TX-NC","TX-NP","TX-HE"))

class HunterVenomEndurance:
    HUNTER=HUNTER

    def __init__(self,damage_state):
        self.d=damage_state
        self.e=damage_state.e
        self.clock=damage_state.clock
        self.toxins=damage_state.toxins
        self.effects={}
        self.next_effect=0
        self.hit_keys=set()
        self.hunter_keys=set()

    def hunter_penalties(self,t):
        if t["profile"]!=HUNTER or not t["active"]:
            return {}
        stage=t.get("stage",0)
        return ({"mp":-4,"muscular_strength":-2} if stage==2 else
                {"mp":-2,"muscular_strength":-1} if stage==1 else {})

    def for_recipient(self,recipient):
        for v in list(self.effects.values()):
            if v["active"] and v["recipient"]==recipient:
                if self.e.actors[recipient].dead:
                    self._end(v,"recipient_dead")
                    return None
                return v
        return None

    def on_recipient_death(self,recipient):
        """End all fixed protection on the actual G4 death transition.

        This is invoked at damage/Dying commit, not deferred until a caller
        happens to query the expired recipient or the caster's next cast.
        """
        for v in list(self.effects.values()):
            if v["active"] and v["recipient"]==recipient:
                self._end(v,"recipient_dead")

    def covering(self,t):
        v=self.for_recipient(t["recipient"])
        return bool(v is not None and v["mode"]=="suppression"
                    and v["bound_key"]==t["key"] and v["covered"])

    def _end(self,v,reason):
        if not v["active"]:
            return
        v["active"]=False
        marker=v["expiry"]
        if marker is not None:
            ev=self.clock.events.get(marker)
            if ev and not ev.consumed and not ev.canceled:
                self.clock.cancel_milestone(marker,source=v["source"])
        self.e.log("g44_endurance_ended",effect=v["id"],caster=v["caster"],
                   recipient=v["recipient"],reason=reason,unused_units=v["units"])
        self.toxins._synchronize(v["recipient"])

    def _spend(self,v,kind,*,phase=0):
        if not v["active"] or v["units"]<=0:
            return False
        v["units"]-=1
        v["covered"]=True
        # On a genuine Step 3, preserve the actual exploration remainder
        # that belongs to the newly funded long suppression interval.
        # Initial and wholly exploration-funded intervals begin at zero.
        v["phase"]=phase
        self.e.log("g44_suppression_unit",effect=v["id"],recipient=v["recipient"],
                   source_toxin=v["bound_key"],unit_kind=kind,remaining=v["units"])
        self.toxins._synchronize(v["recipient"])
        return True

    def on_toxin_end(self,t):
        v=self.for_recipient(t["recipient"])
        if v and v["mode"]=="suppression" and v["bound_key"]==t["key"]:
            self._end(v,"bound_toxin_ended")

    def intercept(self,recipient,grade):
        v=self.for_recipient(recipient)
        if v is None or v["mode"]!="ward" or grade not in ("Minor","Moderate"):
            return False
        self.e.log("g44_ward_intercepted",effect=v["id"],recipient=recipient,
                   grade=grade)
        self._end(v,"interception_consumed")
        return True

    def prevent_discrete(self,t,resource,amount):
        v=self.for_recipient(t["recipient"])
        if v is None or v["mode"]!="suppression" or v["bound_key"]!=t["key"]:
            return False
        if t["profile"] not in DISCRETE:
            return False
        if resource=="vigor" and self.e.actors[t["recipient"]].vigor<=0:
            return False
        if not self._spend(v,"discrete_"+resource):
            return False
        # One unit covers one packet only; depletion has no lingering interval.
        v["covered"]=False
        if v["units"]==0:
            self._end(v,"units_exhausted")
        return True

    def prevent_legacy_hemotoxin(self,t):
        """Protect the still-supported G4 TX-HM adapter's real pending tick.

        Legacy entries are deliberately not copied into G4.3 instances:
        their local elapsed phase, consumed packet count and source key
        remain owned by DamageState.short_toxins.
        """
        if t["left"]<=0 or self.e.actors[t["recipient"]].dead:
            return False
        v=self.for_recipient(t["recipient"])
        if (v is None or v["mode"]!="suppression"
                or v["bound_key"]!=t["key"] or not v["bound_legacy"]):
            return False
        if not self._spend(v,"legacy_TX_HM_hp"):
            return False
        v["covered"]=False
        self.e.log("g44_toxin_packet_prevented",recipient=t["recipient"],
                   key=t["key"],packet=t["applied"]+1,
                   resource="hp",legacy=True)
        if v["units"]==0:
            self._end(v,"units_exhausted")
        return True

    def on_legacy_hemotoxin_end(self,t):
        if t["left"]:
            return
        v=self.for_recipient(t["recipient"])
        if (v is not None and v["mode"]=="suppression"
                and v["bound_legacy"] and v["bound_key"]==t["key"]):
            self._end(v,"bound_toxin_ended")

    def prevent_recovery(self,t):
        v=self.for_recipient(t["recipient"])
        if v is None or v["mode"]!="suppression" or v["bound_key"]!=t["key"]:
            return False
        if t["profile"]!="TX-HE" or not self._spend(v,"genuine_recovery"):
            return False
        v["covered"]=False
        if v["units"]==0:
            self._end(v,"units_exhausted")
        return True

    def after_short_interval(self,t):
        v=self.for_recipient(t["recipient"])
        if v is None or v["mode"]!="suppression" or v["bound_key"]!=t["key"]:
            return
        if t["profile"] not in CONTINUOUS_SHORT:
            return
        v["covered"]=False
        if t["active"] and v["units"]>0:
            self._spend(v,"next_short_interval")
        else:
            self._end(v,"units_exhausted" if t["active"] else "bound_toxin_ended")
        self.toxins._synchronize(t["recipient"])

    def _long_stage(self,t):
        # Starts protection at delayed Hunter onset; never at T+0 silence.
        v=self.for_recipient(t["recipient"])
        if (v and v["mode"]=="suppression" and v["bound_key"]==t["key"]
                and t["profile"]==HUNTER and t["stage"]==1
                and not v["covered"] and v["units"]):
            self._spend(v,"long_onset")

    def long_step_limit(self):
        limits=[6-v["phase"] for v in self.effects.values()
                if v["active"] and v["mode"]=="suppression"
                and v["covered"] and v["long"]]
        return min(limits) if limits else None

    def exploration_advance(self,seconds):
        for v in self.effects.values():
            if v["active"] and v["mode"]=="suppression" and v["covered"] and v["long"]:
                v["phase"]+=seconds

    def _long_boundary(self,v,*,from_step3=False):
        if not v["active"] or not v["covered"] or not v["long"]:
            return
        # Completing a six-second EXPLORATION interval consumes its entire
        # elapsed clock. A genuine Step 3 closes the current interval without
        # creating elapsed seconds: carry 1..5 already elapsed exploration
        # seconds into the next paid local interval instead of losing them.
        next_phase=v["phase"] if from_step3 else 0
        v["phase"]=0
        v["covered"]=False
        t=self.toxins.active(v["recipient"])
        if t is None or t["key"]!=v["bound_key"]:
            self._end(v,"bound_toxin_ended")
        elif t["profile"]!=HUNTER or self.hunter_penalties(t):
            if v["units"] and v["active"]:
                self._spend(v,"next_long_interval",phase=next_phase)
            else:
                self._end(v,"units_exhausted")
        self.toxins._synchronize(v["recipient"])

    def after_exploration_boundary(self):
        for v in list(self.effects.values()):
            if v["active"] and v["mode"]=="suppression" and v["long"] and v["covered"] and v["phase"]>=6:
                self._long_boundary(v)

    def on_turn_step3(self,recipient):
        for v in list(self.effects.values()):
            if v["active"] and v["recipient"]==recipient and v["mode"]=="suppression" and v["long"] and v["covered"]:
                self._long_boundary(v,from_step3=True)

    def on_milestone(self,ev):
        if ev.source.startswith("endurance:"):
            v=next((x for x in self.effects.values() if x["expiry"]==ev.ident
                    and x["active"] and x["source"]==ev.source),None)
            if v:self._end(v,"fixed_duration_expired")
            return
        if not ev.source.startswith("hunter:"):
            return
        t=self.toxins.active(ev.actor_id)
        if t is None or t["profile"]!=HUNTER or ev.ident not in t["markers"] or ev.source!=t["source_tag"]:
            return
        if ev.ident.endswith(":onset"):
            t["stage"]=1
            self._long_stage(t)
        elif ev.ident.endswith(":escalate"):
            if t["result"]=="Full":
                t["stage"]=2
        elif ev.ident.endswith(":expiry"):
            self.toxins._expire(t,"hunter_original_expiry")
        self.e.log("g44_hunter_milestone",recipient=ev.actor_id,
                   key=t["key"],stage=t["stage"],marker=ev.ident,
                   active=t["active"],original_order=ev.original_order)
        self.toxins._synchronize(ev.actor_id)

    def apply_bite(self,attacker,recipient,*,profile_hit_index,exposure_key,
                   resistance_die=None,resistance_modifier=0,breach_verified=False):
        """Use one actual G4 Hunter Bite/Pounce ledger, never a claimed hit."""
        if attacker not in self.e.actors or recipient not in self.e.actors:
            raise ValueError("Known Hunter and victim required")
        source=self.e.actors[attacker]
        if source.source.source_id!="B06-EN-03":
            raise ValueError("Only sourced Hunter can deliver Hunter venom")
        if type(profile_hit_index) is not int or not 0<=profile_hit_index<len(self.e.ledger):
            raise UnresolvedDecision("Exact resolved G4 Hunter hit ledger index required")
        hit=self.e.ledger[profile_hit_index]
        facts=hit["detail"]
        if (hit["kind"]!="g4_profile_hit" or facts.get("attacker")!=attacker
                or facts.get("target")!=recipient or facts.get("profile") not in BITES):
            raise UnresolvedDecision("Only genuine resolved Hunter Bite/Pounce source qualifies")
        if profile_hit_index in self.hit_keys:
            raise ValueError("One venom application per actual Hunter Bite event")
        # Exposure is a synchronous part of this physical Bite's resolution.
        # Once any intervening encounter/clock event is recorded, historical
        # Bite results cannot be re-used under a later Ward/nonstack state or
        # restart their original 10/30/60/120-minute clock.
        if profile_hit_index != len(self.e.ledger)-1:
            raise UnresolvedDecision(
                "Hunter venom must consume the latest Bite event synchronously")
        if type(breach_verified) is not bool:
            raise ValueError("Breach adjudication must be bool")
        if self.e.actors[recipient].dead:
            raise ValueError("Dead recipient cannot receive Hunter venom")
        if (not isinstance(exposure_key,str) or not exposure_key
                or exposure_key in self.toxins.exposure_ids
                or exposure_key in self.hunter_keys
                or any(x["key"]==exposure_key for x in self.d.short_toxins)):
            raise ValueError("New stable unused toxin exposure key required")
        # An independent non-puncture route cannot be inferred merely
        # because some other HP packet of the Bite caused injury.
        valid=bool(facts["injection_eligible"] or breach_verified)
        if not valid:
            self.hit_keys.add(profile_hit_index)
            self.hunter_keys.add(exposure_key)
            self.toxins.exposure_ids.add(exposure_key)
            self.e.log("g44_hunter_not_delivered",attacker=attacker,recipient=recipient,
                       exposure_key=exposure_key,hit_index=profile_hit_index)
            return {"outcome":"not_delivered"}
        old=self.toxins.active(recipient)
        if old is not None and old["grade"]=="Moderate":
            self.hit_keys.add(profile_hit_index)
            self.hunter_keys.add(exposure_key)
            self.toxins.exposure_ids.add(exposure_key)
            self.e.log("g44_hunter_ignored",recipient=recipient,
                       key=exposure_key,active=old["key"])
            return {"outcome":"ignored","active":old["key"]}
        if old is None and any(x["recipient"]==recipient and x["left"]
                               for x in self.d.short_toxins):
            raise UnresolvedDecision("Legacy toxin active; no parallel Hunter instance")
        if self.intercept(recipient,"Moderate"):
            self.hit_keys.add(profile_hit_index)
            self.hunter_keys.add(exposure_key)
            self.toxins.exposure_ids.add(exposure_key)
            self.e.log("g44_hunter_prevented",recipient=recipient,key=exposure_key)
            return {"outcome":"prevented"}
        if type(resistance_die) is not int or not 1<=resistance_die<=20:
            raise UnresolvedDecision("One actual d20 natural resistance required")
        if type(resistance_modifier) is not int:
            raise ValueError("Natural resistance modifier must be integer")
        abilities=dict(self.e.actors[recipient].source.abilities)
        vit=abilities.get("Vitality",abilities.get("vitality"))
        if type(vit) is not int:
            raise UnresolvedDecision("Recipient requires source Vitality")
        total=resistance_die+vit+resistance_modifier
        mode="Reduced" if total>=12 else "Full"
        tag="hunter:"+exposure_key
        self.hit_keys.add(profile_hit_index)
        self.hunter_keys.add(exposure_key)
        t={"recipient":recipient,"key":exposure_key,"profile":HUNTER,
           "grade":"Moderate","result":mode,"resistance_total":total,
           "source_tag":tag,"active":True,"clock":"hunter","stage":0,
           "markers":[],"source":"B06-SRC-HUNTER-GROOVED-CANINES"}
        if old is not None:
            self.toxins._expire(old,"higher_printed_grade_replaced")
        self.toxins.instances[recipient]=t
        self.toxins.exposure_ids.add(exposure_key)
        for label,seconds in ((("onset",600),("escalate",1800),("expiry",7200))
                              if mode=="Full" else (("onset",600),("expiry",3600))):
            ident=f"hunter:{exposure_key}:{label}"
            self.clock.schedule_milestone(recipient,event_id=ident,source=tag,
                                           delay_seconds=seconds,
                                           phase="before_recovery")
            t["markers"].append(ident)
        self.toxins._synchronize(recipient)
        self.e.log("g44_hunter_accepted",recipient=recipient,key=exposure_key,
                   resolution=mode,resistance_total=total,hit_index=profile_hit_index,
                   marker_ids=list(t["markers"]))
        return {"outcome":"accepted","resolution":mode,"resistance_total":total}

    def cast_endurance(self,caster,recipient,*,profile,mode,
                       source_authorized,source_reference,
                       ordinary_cost=2,discount_authorized=False,
                       discount_commit=None,open_invocation=False,
                       high_priest_authorized=False,unopposed=True,
                       intrusion_totals=None,visible=True,unobstructed=True,
                       delivery_check=None,on_committed=None):
        """Actual own-turn AP+VP casting; source legality attested externally."""
        if caster not in self.e.actors or recipient not in self.e.actors:
            raise ValueError("Known caster and recipient required")
        a,b=self.e.actors[caster],self.e.actors[recipient]
        if mode not in ("ward","suppression") or profile not in ("Self","Single Target"):
            raise ValueError("Exact Venom Endurance profile and mode required")
        if profile=="Self" and caster!=recipient:
            raise ValueError("Self mode must target caster")
        if source_authorized is not True or not isinstance(source_reference,str) or not source_reference:
            raise UnresolvedDecision("Independently proven known/prepared Life Prayer access required")
        if a.hp<=0 or a.dead or b.dead or b.hp<=-b.hp_max:
            raise ValueError("Living caster and recipient required")
        if self.e.current!=caster or self.e.pending_regeneration is not None:
            raise ValueError("Venom Endurance is an ordinary own-turn cast, not Reaction")
        if (type(ordinary_cost) is not int or ordinary_cost not in (1,2)
                or (ordinary_cost==1 and discount_authorized is not True)):
            raise ValueError("Only legally declared ordinary 2/discounted 1 Spent VP")
        if open_invocation and high_priest_authorized is not True:
            raise UnresolvedDecision("Open Invocation requires authorized High Priest")
        if discount_authorized and ordinary_cost==1 and not callable(discount_commit):
            raise UnresolvedDecision("Discount must consume independently legal declared use")
        if any(v["active"] and (v["recipient"]==recipient or v["caster"]==caster)
               for v in self.effects.values()):
            raise ValueError("Only one active Endurance per caster and recipient")
        def legal_delivery():
            if profile=="Self":
                return True
            if visible is not True or unobstructed is not True:
                return False
            if not a.occupied or not b.occupied:
                raise UnresolvedDecision("Explicit source occupied reference cells required")
            # The reference is a permanent body-local ID, not the current
            # lexicographically smallest world cell. In particular Hunter's
            # head stays the reference even when rear sorts before head.
            p=a.reference_square()
            q=b.reference_square()
            axes=sorted([abs(x-y) for x,y in zip(
                tuple(p)+(0,)*(3-len(p)),tuple(q)+(0,)*(3-len(q)))],reverse=True)
            if axes[0]+axes[1]/2+axes[2]/2>3:
                return False
            if delivery_check is not None:
                if not callable(delivery_check):
                    raise ValueError("Current target/path callback required")
                valid=delivery_check(self.e,caster,recipient)
                if type(valid) is not bool:
                    raise ValueError("Target/path callback must return bool")
                return valid
            return True
        if not legal_delivery():
            raise ValueError("Invalid declaration-time Venom Endurance delivery")
        if unopposed is not True and (
                not isinstance(intrusion_totals,(tuple,list)) or
                len(intrusion_totals)!=2 or
                any(type(x) is not int for x in intrusion_totals)):
            raise UnresolvedDecision(
                "Resisted +8 Intrusion contest must be independently attested")
        raw_vc=None
        if mode=="suppression":
            abilities=dict(a.source.abilities)
            raw_vc=abilities.get("Veil Control",abilities.get("veil_control"))
            if type(raw_vc) is not int:
                raise UnresolvedDecision(
                    "Caster raw Veil Control required before AP/VP commit")
        price=ordinary_cost+int(open_invocation)
        if a.vp_available<price:
            raise ValueError("Insufficient Available VP for locked effective price")
        action="full" if open_invocation else "projection"
        if action=="projection" and a.projection_ap not in (20,24,30):
            raise UnresolvedDecision("No legal Focus Projection Action")
        # Verify AP availability before discount use is committed.
        needed=a.ap_total if open_invocation else a.projection_ap
        if (a.ap_remaining<needed or
                (open_invocation and a.ap_remaining!=a.ap_total)):
            raise ValueError("Insufficient own-turn AP to declare")
        if ordinary_cost==1 and discount_commit(self.e,caster) is not True:
            raise UnresolvedDecision("Ordinary discount could not be legally committed")
        self.e.spend_ap(caster,action,label="venom_endurance:"+mode)
        if on_committed is not None:
            on_committed(self.e)
        if (a.hp<=0 or a.dead or b.dead or a.vp_available<price
                or any(x["active"] and (x["caster"]==caster or
                                       x["recipient"]==recipient)
                       for x in self.effects.values())
                or not legal_delivery()):
            self.e.log("g44_endurance_interrupted",caster=caster,recipient=recipient,
                       mode=mode,ap_spent=needed,vp_spent=0)
            return None
        self.e.spend_vp(caster,price,mode="spent",label="venom_endurance:"+mode)
        if unopposed is not True:
            if intrusion_totals[0]<=intrusion_totals[1]:
                self.e.log("g44_endurance_resisted",caster=caster,recipient=recipient,
                           attack=intrusion_totals[0],defense=intrusion_totals[1])
                return None
        self.next_effect+=1
        ident=f"G44-VE-{self.next_effect:04d}"
        event=f"endurance:{ident}:expiry"
        source="endurance:"+ident
        v={"id":ident,"caster":caster,"recipient":recipient,"mode":mode,
           "source_reference":source_reference,"source":source,"active":True,
           "expiry":event,"bound_key":None,"bound_legacy":False,
           "units":0,"covered":False,
           "phase":0,"long":False,"cost":price}
        if mode=="suppression":
            t=self.toxins.active(recipient)
            # Older verified TX-HM schedules are still legal and use a
            # separate retained hazard record. They are exclusively bound
            # only when there is no live unified instance.
            legacy=(next((x for x in self.d.short_toxins
                         if x["recipient"]==recipient and x["left"]>0),None)
                    if t is None else None)
            viable=(t is not None and t["profile"] in COVERED
                    and t["profile"]!="TX-CY") or legacy is not None
            if viable:
                v["bound_key"]=t["key"] if t is not None else legacy["key"]
                v["bound_legacy"]=legacy is not None
                v["units"]=min(5,3+max(0,raw_vc)//2)
                v["long"]=t is not None and t["profile"] in CONTINUOUS_LONG
                if t is not None and (t["profile"] in CONTINUOUS_SHORT or (
                        t["profile"] in CONTINUOUS_LONG and (
                            t["profile"]!=HUNTER or t["stage"]>0))):
                    self.effects[ident]=v
                    self._spend(v,"initial_continuous_interval")
        self.effects[ident]=v
        self.clock.schedule_milestone(recipient,event_id=event,source=source,
                                       delay_seconds=60,phase="before_toxin")
        self.e.log("g44_endurance_applied",effect=ident,caster=caster,
                   recipient=recipient,mode=mode,cost=price,
                   bound_key=v["bound_key"],units=v["units"])
        if mode=="suppression" and v["bound_key"] is None:
            self._end(v,"no_suppressible_instance")
        self.e.check()
        return ident

    def dismiss(self,caster,effect_id):
        v=self.effects.get(effect_id)
        if v is None or not v["active"] or v["caster"]!=caster:
            raise ValueError("No active caster-owned Endurance to dismiss")
        if self.e.current!=caster or self.e.pending_regeneration is not None:
            raise ValueError("Voluntary dismissal requires own-turn timing")
        self._end(v,"voluntary_dismissal")
