"""B06 G4.3: one-instance mundane toxin application and authored effects.

No exposure is inferred from a hit: caller must attest the actual delivered
material and route. Hunter's named venom and Venom Endurance are G4.4.
"""
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _integer

# (grade, delivery, Full count, Reduced count, clock)
PROFILES = {
    "TX-HM": ("Moderate","injection",5,3,"short"),
    "TX-NE": ("Moderate","injection",5,3,"short"),
    "TX-CY": ("Moderate","contact",3,3,"short"),
    "TX-NC": ("Moderate","injection",5,4,"short"),
    "TX-MY": ("Minor","injection",6,3,"short"),
    "TX-CA": ("Moderate","ingestion",4,2,"short"),
    "TX-HE": ("Minor","ingestion",21600,21600,"long"),
    "TX-NP": ("Moderate","ingestion",4,2,"long"),
    "TX-PN": ("Minor","inhalation",5,3,"short"),
    "TX-EN": ("Minor","ingestion",10800,7200,"long"),
    "TX-DE": ("Minor","contact",6,3,"short"),
}
GRADE = {"Minor":0, "Moderate":1}
DC = {"Minor":10, "Moderate":12}
# Values are modifiers to exact eligible uses; no generic poisoned condition.
PENALTIES = {
    "TX-NE": {"dodge":-2},
    "TX-MY": {"mp":-2,"muscular_strength":-1},
    "TX-CA": {"regen_throughput":-1},
    "TX-PN": {"mp":-2,"breathing_endurance":-1},
    "TX-EN": {"physical_exertion":-1},
    "TX-DE": {"contact_precision":-1},
}


class MundaneToxins:
    def __init__(self, damage_state):
        self.d = damage_state
        self.e = damage_state.e
        self.clock = damage_state.clock
        self.instances = {}
        self.exposure_ids = set()

    def active(self, actor_id):
        t = self.instances.get(actor_id)
        return t if t is not None and t["active"] else None

    def modifier(self, actor_id, use):
        t = self.active(actor_id)
        return PENALTIES.get(t["profile"],{}).get(use,0) if t else 0

    def _synchronize(self, actor_id):
        actor = self.e.actors[actor_id]
        previous = getattr(actor,"toxin_modifiers",{})
        t = self.active(actor_id)
        current = dict(PENALTIES.get(t["profile"],{})) if t else {}
        actor.toxin_modifiers = current
        # An effect becoming active during an already established turn may
        # consume currently remaining ordinary movement; ending never refunds
        # MP already committed/spent or generates a new MP allowance.
        if self.e.current == actor_id and current.get("mp",0)<previous.get("mp",0):
            actor.mp_remaining = max(0,actor.mp_remaining
                                     + current["mp"]-previous.get("mp",0))

    def _expire(self,t,reason):
        if not t["active"]:
            return
        t["active"] = False
        marker = t.get("marker")
        if marker is not None:
            ev = self.clock.events.get(marker)
            if ev is not None and not ev.consumed and not ev.canceled:
                self.clock.cancel_milestone(marker,source=t["source_tag"])
        self.e.log("g43_toxin_ended",recipient=t["recipient"],
                   exposure_key=t["key"],profile=t["profile"],reason=reason)
        self._synchronize(t["recipient"])

    def stop_authorized(self,actor_id,*,reason,authorized):
        """A separately established cure/suppression outcome; no free medicine."""
        if authorized is not True or not isinstance(reason,str) or not reason:
            raise UnresolvedDecision("Independent authored ending authority required")
        t=self.active(actor_id)
        if t is None:
            raise ValueError("No active toxin to end")
        self._expire(t,reason)

    def _future_event(self,t,*,delay,kind,phase="before_recovery"):
        t["serial"] += 1
        ident=f"toxin:{t['key']}:{kind}:{t['serial']}"
        self.clock.schedule_milestone(t["recipient"],event_id=ident,
                                      source=t["source_tag"],
                                      delay_seconds=delay,phase=phase)
        t["marker"]=ident

    def _hit(self,t,resource,amount):
        from scripts.b06_damage_v0 import DamagePacket
        if self.e.actors[t["recipient"]].dead:
            return
        t["applied"] += 1
        self.d.apply_damage(t["recipient"],
                 (DamagePacket(resource,"Toxin",amount),),
                 event_key=f"toxin:{t['key']}:packet:{t['applied']}",
                 cause=t["profile"]+":scheduled_"+resource,
                 wound_location_roll=t["wound_roll"])

    def apply(self,recipient,profile,*,exposure_key,source,route,
              delivery_verified,breach_verified=False,residual_piercing_hp=0,
              resistance_die=None,resistance_modifier=0,
              preventive_ward=None,wound_location_roll=None):
        """Delivery -> one-instance gate -> independently valid ward -> save.

        No roll or ward is consumed on failed exposure or an ignored grade.
        A prevented higher grade leaves the earlier active toxin untouched.
        """
        if recipient not in self.e.actors or self.e.actors[recipient].dead:
            raise ValueError("Living known toxin recipient required")
        if profile not in PROFILES:
            raise UnresolvedDecision("Uncatalogued mundane toxin profile")
        grade,required,full,reduced,clock_type=PROFILES[profile]
        if not isinstance(exposure_key,str) or not exposure_key:
            raise ValueError("Stable toxin exposure key required")
        if exposure_key in self.exposure_ids:
            raise ValueError("Toxin exposure key already processed")
        if not isinstance(source,str) or not source:
            raise ValueError("Independent toxin source must be identified")
        if route != required:
            raise ValueError("Profile does not authorize exposure route")
        if type(delivery_verified) is not bool or type(breach_verified) is not bool:
            raise ValueError("Actual delivery and breach testimony must be booleans")
        _integer(residual_piercing_hp,"residual Piercing HP")
        if not delivery_verified or (route=="injection" and not
                (residual_piercing_hp>0 or breach_verified)):
            self.exposure_ids.add(exposure_key)
            self.e.log("g43_exposure_rejected",recipient=recipient,
                       profile=profile,key=exposure_key,reason="no_valid_delivery")
            return {"outcome":"not_delivered"}
        prior=self.active(recipient)
        if prior is None and any(t["recipient"]==recipient and t["left"]
                  for t in self.d.short_toxins):
            raise UnresolvedDecision("Resolve legacy TX-HM before unified toxin application")
        if prior is not None and GRADE[grade]<=GRADE[prior["grade"]]:
            self.exposure_ids.add(exposure_key)
            self.e.log("g43_exposure_ignored",recipient=recipient,
                       profile=profile,key=exposure_key,
                       active=prior["key"],reason="equal_or_lower_printed_grade")
            return {"outcome":"ignored","active":prior["key"]}
        if preventive_ward is not None:
            if not callable(preventive_ward):
                raise ValueError("Preventive ward must be an attested callback")
            stopped=preventive_ward(self.e,recipient,profile,grade)
            if type(stopped) is not bool:
                raise ValueError("Preventive ward adjudication must return bool")
            if stopped:
                self.exposure_ids.add(exposure_key)
                self.e.log("g43_exposure_prevented",recipient=recipient,
                           profile=profile,key=exposure_key,source=source)
                return {"outcome":"prevented"}
        if type(resistance_die) is not int or not 1<=resistance_die<=20:
            raise UnresolvedDecision("One actual d20 Vitality resistance required")
        if type(resistance_modifier) is not int:
            raise ValueError("Explicit resistance modifier must be integer")
        if profile in ("TX-HM","TX-NC","TX-CY") and (
                type(wound_location_roll) is not int
                or not 1<=wound_location_roll<=20):
            raise UnresolvedDecision("Future HP crossing requires actual wound-location d20")
        vitality=dict(self.e.actors[recipient].source.abilities).get("Vitality")
        if type(vitality) is not int:
            raise UnresolvedDecision("Recipient has no sourced Vitality")
        total=resistance_die+vitality+resistance_modifier
        mode="Reduced" if total>=DC[grade] else "Full"
        units=reduced if mode=="Reduced" else full
        tag="mundane:"+profile+":"+exposure_key
        t={"recipient":recipient,"key":exposure_key,"profile":profile,
           "grade":grade,"source":source,"source_tag":tag,
           "result":mode,"resistance_total":total,
           "phase":0,"left":units if clock_type=="short" else 0,
           "remaining":units if clock_type=="long" else 0,
           "wound_roll":wound_location_roll,"applied":0,
           "active":True,"marker":None,"serial":0,
           "clock":clock_type,"recovery_id":None}
        if prior is not None:
            self._expire(prior,"higher_printed_grade_replaced")
        self.instances[recipient]=t
        self.exposure_ids.add(exposure_key)
        self._synchronize(recipient)
        self.e.log("g43_toxin_accepted",recipient=recipient,profile=profile,
                   exposure_key=exposure_key,source=source,grade=grade,
                   resistance_die=resistance_die,resistance_total=total,
                   resolution=mode,units=units,route=route)
        if profile=="TX-CY":
            self._hit(t,"hp",2 if mode=="Reduced" else 4)
        elif profile=="TX-NP":
            self._future_event(t,delay=3600,kind="pulse")
        elif profile=="TX-EN":
            self._future_event(t,delay=units,kind="expiry")
        elif profile=="TX-HE":
            pending=next((ev for ev in self.clock._pending()
                          if ev.kind=="recovery" and ev.actor_id==recipient),None)
            if pending is None:
                raise UnresolvedDecision("No independently pending Recovery checkpoint")
            t["recovery_id"]=pending.ident
            self._future_event(t,delay=21600,kind="expiry",phase="after_recovery")
        self.e.check()
        return {"outcome":"accepted","resolution":mode,"active":exposure_key,
                "resistance_total":total}

    def _short_interval(self,t):
        if not t["active"] or t["clock"]!="short":
            return
        profile=t["profile"]
        # TX-NC's first two local intervals are deliberately onset delays.
        if profile=="TX-HM" or (profile=="TX-NC" and
                                    t["left"] <= (3 if t["result"]=="Full" else 2)):
            self._hit(t,"hp",1)
        t["left"]-=1
        self.e.log("g43_short_interval",recipient=t["recipient"],
                   key=t["key"],profile=profile,remaining=t["left"])
        if t["left"]==0:
            self._expire(t,"short_duration_completed")

    def on_turn_step3(self,actor_id):
        t=self.active(actor_id)
        if t is not None and t["clock"]=="short":
            self._short_interval(t)

    def on_milestone(self,ev):
        if not ev.source.startswith("mundane:"):
            return
        t=self.active(ev.actor_id)
        if t is None or ev.ident!=t.get("marker") or ev.source!=t["source_tag"]:
            return
        t["marker"]=None
        if t["profile"]=="TX-NP":
            self._hit(t,"vigor",1)
            t["remaining"]-=1
            if t["remaining"]:
                self._future_event(t,delay=3600,kind="pulse")
            else:
                self._expire(t,"last_hourly_pulse")
        elif t["profile"] in ("TX-EN","TX-HE"):
            self._expire(t,"long_duration_expiry")

    def recovery_penalty(self,ev):
        """Consume one authentic existing Recovery only, never reschedule it."""
        t=self.active(ev.actor_id)
        if t is None or t["profile"]!="TX-HE" or t["recovery_id"]!=ev.ident:
            return 0
        reduction=2 if t["result"]=="Full" else 1
        self.e.log("g43_hepatotoxin_recovery",recipient=t["recipient"],
                   exposure_key=t["key"],checkpoint_id=ev.ident,
                   reduction=reduction)
        self._expire(t,"recovery_intercepted")
        return reduction

    def exploration_step_limit(self):
        limits=[6-t["phase"] for t in self.instances.values()
                if t["active"] and t["clock"]=="short"]
        return min(limits) if limits else None

    def exploration_advance(self,seconds):
        for t in self.instances.values():
            if t["active"] and t["clock"]=="short":
                t["phase"]+=seconds

    def exploration_resolve(self):
        for t in list(self.instances.values()):
            if t["active"] and t["clock"]=="short" and t["phase"]>=6:
                t["phase"]-=6
                self._short_interval(t)
