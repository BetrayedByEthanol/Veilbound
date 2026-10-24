"""B06 G4.2: world/encounter chronology, not an effect or toxin rules engine.

Exploration advances actual seconds. Initiative uses Round Begin labels with
source-specific conservative conversions: no global physical combat seconds,
virtual turns, regeneration, or invented wound/poison effects.
"""
from dataclasses import dataclass

from scripts.b06_encounter_state_v0 import UnresolvedDecision, _integer


SIX_HOURS = 21600
ROUND_SECONDS_SURROGATE = 6  # conversion only; NOT a duration of a combat round
PHASE_ORDER = {"before_toxin": -1, "before_recovery": 0,
               "recovery": 1, "after_recovery": 2}


@dataclass
class ClockEvent:
    ident: str
    actor_id: str
    actor_source: str
    source_digest: str
    source: str
    kind: str
    phase: str
    serial: int
    original_order: int
    due_seconds: int | None = None
    due_round: int | None = None
    consumed: bool = False
    canceled: bool = False


class WorldClock:
    """One canonical pending-event ledger shared by exploration and initiative.

    Marker events only attest that a source-owned milestone has become due.
    G4.3/G4.4 must provide the separately authored effect interpreter.
    """

    def __init__(self, damage_state, *, recovery_phase_seconds=None):
        self.g4 = damage_state
        self.e = damage_state.e
        self.mode = "exploration"
        self.world_seconds = 0
        self.entry_round = None
        self.events = {}
        self.sequence = 0
        self.recovery_serial = {a: 1 for a in self.e.actors}
        if recovery_phase_seconds is None:
            recovery_phase_seconds = {}
        if not isinstance(recovery_phase_seconds, dict):
            raise ValueError("Recovery phases must be an actor-to-seconds mapping")
        if set(recovery_phase_seconds) - set(self.e.actors):
            raise ValueError("Recovery phase references unknown actor")
        for actor_id in self.e.actors:
            remaining = recovery_phase_seconds.get(actor_id, SIX_HOURS)
            _integer(remaining, "remaining recovery seconds", 1)
            if remaining > SIX_HOURS:
                raise ValueError("Recovery phase must be within one six-hour interval")
            self._schedule_recovery(actor_id, remaining)

    def _next_serial(self):
        self.sequence += 1
        return self.sequence

    def _round_label(self):
        # If last round has ended, the next Round Begin is the next initiative
        # label. Otherwise the still-unplayed current round is the entry label.
        if self.e.round and self.e.cursor == len(self.e.order):
            return self.e.round + 1
        return max(1, self.e.round)

    def _schedule_recovery(self, actor_id, delay, *, completed_round=None):
        a = self.e.actors[actor_id]
        number = self.recovery_serial[actor_id]
        ident = f"recovery:{actor_id}:{number}"
        # Recovery IDs are clock-owned across the ENTIRE checkpoint series,
        # including checkpoints which have not yet been constructed.
        # Never replace an existing event or advance the serial on collision.
        if ident in self.events:
            raise ValueError("Recovery checkpoint ID collision")
        self.recovery_serial[actor_id] += 1
        if self.mode == "exploration":
            deadline = self.world_seconds + delay
            due_seconds, due_round = deadline, None
            original_order = deadline
        else:
            # Recurrence after a genuinely completed Recovery is exactly
            # 3600 Round Begin boundaries, not a newly earned time interval.
            if delay % ROUND_SECONDS_SURROGATE:
                raise ValueError("Initiative Recovery extension requires whole boundaries")
            # Entry with q=0 may precede begin_round(): use its mapped
            # boundary, not the previous e.round, when scheduling recurrence.
            anchor = completed_round if completed_round is not None else self._round_label()
            deadline = anchor + delay // ROUND_SECONDS_SURROGATE
            due_seconds, due_round = None, deadline
            original_order = (self.world_seconds
                              + (deadline - self.entry_round) * ROUND_SECONDS_SURROGATE)
        event = ClockEvent(ident,actor_id,a.source.source_id,a.source.digest,
                           "canonical:6h-recovery","recovery","recovery",
                           self._next_serial(),original_order,
                           due_seconds,due_round)
        self.events[ident] = event
        return event

    def schedule_milestone(self, actor_id, *, event_id, source,
                           delay_seconds, phase="after_recovery"):
        """Schedule one externally authored *marker*, without applying effects."""
        if actor_id not in self.e.actors:
            raise ValueError("Unknown milestone actor")
        if not isinstance(event_id,str) or not event_id:
            raise ValueError("Stable nonempty milestone ID required")
        if event_id.startswith("recovery:"):
            raise ValueError("Recovery checkpoint ID namespace is reserved")
        if not isinstance(source,str) or not source:
            raise ValueError("Milestone must identify its source")
        if phase not in ("before_toxin","before_recovery","after_recovery"):
            raise ValueError("Marker must specify an authored tie phase")
        _integer(delay_seconds,"milestone delay",1)
        if event_id in self.events:
            raise ValueError("Milestone ID already used; consumed IDs cannot be reused")
        a = self.e.actors[actor_id]
        if self.mode == "exploration":
            due_s = self.world_seconds + delay_seconds
            due_r = None
            original_order = due_s
        else:
            if delay_seconds % ROUND_SECONDS_SURROGATE:
                raise UnresolvedDecision(
                    "New initiative milestone requires authored whole-round surrogate")
            current_round = self._round_label()
            due_r = current_round + delay_seconds // ROUND_SECONDS_SURROGATE
            due_s = None
            original_order = (self.world_seconds
                              + (due_r - self.entry_round) * ROUND_SECONDS_SURROGATE)
        ev = ClockEvent(event_id,actor_id,a.source.source_id,a.source.digest,
                        source,"milestone",phase,self._next_serial(),
                        original_order,due_s,due_r)
        self.events[event_id] = ev
        self.e.log("g42_milestone_scheduled",event_id=event_id,actor=actor_id,
                   actor_source=ev.actor_source,source=source,phase=phase,
                   due_seconds=due_s,due_round=due_r)
        return ev

    def cancel_milestone(self, event_id, *, source):
        ev = self.events.get(event_id)
        if ev is None or ev.kind != "milestone" or ev.consumed or ev.canceled:
            raise ValueError("No pending cancellable milestone")
        if source != ev.source:
            raise ValueError("Only matching source can cancel its marker")
        ev.canceled = True
        self.e.log("g42_milestone_canceled",event_id=event_id,source=source)

    def _pending(self):
        return [ev for ev in self.events.values()
                if not ev.consumed and not ev.canceled]

    @staticmethod
    def _sort_key(ev):
        due = ev.due_seconds if ev.due_seconds is not None else ev.due_round
        # Coalesced Round Begin deadlines must first honor fixed Endurance
        # 'before_toxin' expiry, even when its original instant was later
        # than a toxin pulse. Preserve the original chronological ordering
        # of all OTHER events (including Recovery and ordinary milestones).
        expiry_first = 0 if ev.phase == "before_toxin" else 1
        return due, expiry_first, ev.original_order, PHASE_ORDER[ev.phase], ev.serial

    def _complete(self, ev, *, boundary_round=None):
        if ev.consumed or ev.canceled:
            raise ValueError("Clock event is already processed")
        ev.consumed = True
        if ev.kind == "milestone":
            self.e.log("g42_milestone_due",event_id=ev.ident,actor=ev.actor_id,
                       actor_source=ev.actor_source,source=ev.source,
                       phase=ev.phase,original_order=ev.original_order,
                       world_seconds=self.world_seconds,
                       round_begin=boundary_round)
            # G4.3 consumes source-owned markers, not arbitrary story markers.
            self.g4.venom.on_milestone(ev)
            self.g4.toxins.on_milestone(ev)
            return
        a = self.e.actors[ev.actor_id]
        vigor = max(1,(a.vigor_max+2)//4) if a.vigor_max else 0
        vp = max(1,(a.vp_max+2)//4) if a.vp_max else 0
        # Hepatotoxin can intercept THIS already-earned checkpoint, never
        # schedule a second one or decrease VP Recovery.
        reduction=self.g4.toxins.recovery_penalty(ev)
        actual_vigor = 0 if a.dead else min(max(0,vigor-reduction),
                                           a.vigor_max-a.vigor)
        actual_vp = 0 if a.dead else min(vp,a.vp_spent)
        a.vigor += actual_vigor
        a.vp_spent -= actual_vp
        a.vp_available += actual_vp
        self.e.log("g4_six_hour_recovery",actor=a.id,
                   checkpoint_id=ev.ident,actor_source=ev.actor_source,
                   world_seconds=self.world_seconds,
                   round_begin=boundary_round,
                   vigor=actual_vigor,spent_vp_recovered=actual_vp,
                   toxin_recovery_reduction=reduction)
        # A consumed checkpoint remains forever; only its successor can
        # award a subsequent quarter-max amount.
        if not a.dead:
            self._schedule_recovery(ev.actor_id,SIX_HOURS,
                                    completed_round=boundary_round)

    def _due_exploration(self):
        due = [ev for ev in self._pending()
               if ev.due_seconds is not None
               and ev.due_seconds <= self.world_seconds]
        for ev in sorted(due,key=self._sort_key):
            # A real Recovery may end TX-HE and cancel its same-instant
            # maximum-expiry marker while processing this due snapshot.
            if not ev.consumed and not ev.canceled:
                self._complete(ev)

    def _due_round(self, round_number):
        due = [ev for ev in self._pending()
               if ev.due_round is not None and ev.due_round <= round_number]
        for ev in sorted(due,key=self._sort_key):
            if not ev.consumed and not ev.canceled:
                self._complete(ev,boundary_round=round_number)

    def advance_exploration(self, seconds):
        """Advance actual seconds in chronological pieces, including TX-HM."""
        _integer(seconds,"exploration seconds")
        if self.mode != "exploration":
            raise ValueError("Cannot advance physical exploration seconds in initiative")
        if self.e.current is not None or (
                self.e.round and self.e.cursor not in (0,len(self.e.order))):
            raise ValueError("Enter exploration only between full initiative rounds")
        start = self.world_seconds
        remaining = seconds
        # Event-driven stepping, not one lumped 6-hour recovery after toxins.
        while remaining:
            next_seconds = remaining
            pending = [ev.due_seconds-self.world_seconds for ev in self._pending()
                       if ev.due_seconds is not None]
            if pending:
                next_seconds = min(next_seconds,max(0,min(pending)))
            for toxin in self.g4.short_toxins:
                if toxin["left"]:
                    next_seconds = min(next_seconds,6-toxin["phase"])
            g43_limit=self.g4.toxins.exploration_step_limit()
            if g43_limit is not None:
                next_seconds=min(next_seconds,g43_limit)
            g44_limit=self.g4.venom.long_step_limit()
            if g44_limit is not None:
                next_seconds=min(next_seconds,g44_limit)
            if next_seconds:
                self.world_seconds += next_seconds
                remaining -= next_seconds
                for toxin in self.g4.short_toxins:
                    if toxin["left"]:
                        toxin["phase"] += next_seconds
                self.g4.toxins.exploration_advance(next_seconds)
                self.g4.venom.exploration_advance(next_seconds)
            # Native short-toxin intervals are hazard-only; never fake Step 2.
            for toxin in self.g4.short_toxins:
                if toxin["left"] and toxin["phase"] >= 6:
                    toxin["phase"] -= 6
                    self.g4._toxin_step(toxin)
            self.g4.toxins.exploration_resolve()
            # A newly due Hunter stage/expiry is resolved before deciding
            # whether to fund the NEXT six-second suppression interval.
            self._due_exploration()
            self.g4.venom.after_exploration_boundary()
        self.e.log("g42_exploration_advanced",from_seconds=start,
                   to_seconds=self.world_seconds,seconds=seconds)
        self.e.check()

    def enter_initiative(self):
        """Convert each pending deadline using its own remaining seconds."""
        if self.mode != "exploration" or self.e.current is not None or (
                self.e.round and self.e.cursor not in (0,len(self.e.order))):
            raise ValueError("Initiative entry requires an exploration boundary")
        entry = self._round_label()
        self.mode = "initiative"
        self.entry_round = entry
        for ev in self._pending():
            seconds = max(0,ev.due_seconds-self.world_seconds)
            ev.due_round = entry + seconds // ROUND_SECONDS_SURROGATE
            ev.due_seconds = None
            # Keep preconversion absolute deadline for original order if
            # multiple distinct source instants collapse on one Round Begin.
        self.e.log("g42_initiative_entered",round_begin=entry,
                   world_seconds=self.world_seconds)
        self._due_round(entry)  # q=0: due at transition before actions.
        self.e.check()

    def on_round_begin(self, round_number):
        if self.mode != "initiative":
            return
        self._due_round(round_number)
        self.e.check()

    def leave_initiative(self):
        """Convert every unconsumed Round Begin deadline independently."""
        if self.mode != "initiative" or self.e.current is not None or (
                self.e.round and self.e.cursor not in (0,len(self.e.order))):
            raise ValueError("Initiative exit requires a round boundary")
        # At a completed round boundary Encounter.round still names the
        # completed round until begin_round() is called. _round_label()
        # consistently advances to the *next* label, whether initiative
        # was just entered or remained active throughout that round.
        current = self._round_label()
        self.mode = "exploration"
        self.entry_round = None
        for ev in self._pending():
            # Incomplete current round gets no real-time credit. At most one
            # six-second surrogate per completed future Round Begin boundary.
            seconds = ROUND_SECONDS_SURROGATE * max(0,ev.due_round-current-1)
            ev.due_seconds = self.world_seconds + seconds
            ev.due_round = None
        # Combat-only Exaltations end at the initiative-to-exploration
        # boundary, BEFORE due exploration events can deliver new damage.
        # The Chosen Rite itself and its Committed VP remain unaffected.
        low=(getattr(self.e.g3,"low_life",None)
             if self.e.g3 is not None else None)
        if low is not None:
            low.on_initiative_exit()
        self.e.log("g42_initiative_exited",round_label=current,
                   world_seconds=self.world_seconds)
        self._due_exploration()  # E<=C+1: resolve at mode transition.
        self.e.check()
