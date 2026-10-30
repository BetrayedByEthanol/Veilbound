"""B04/B05: source-bound noncombat Anointed Destiny on real G4.2 time.

This bridge observes existing WorldClock exploration seconds and accepts
externally GM-recognized, unique significant Mission story events.
It neither advances the clock itself nor manufactures a GM verdict.
"""
from scripts.b05_anointed_authority_l1_l3_v0 import (
    recover_destiny, mission_event, set_bond,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint

SOURCE_PATHS={
    "AH":("High","scripts/b05_high_anointed_restoration_l1_l3_v0.py"),
    "AM":("Medium","scripts/b05_medium_anointed_restoration_l1_l3_v0.py"),
    "AL":("Low","scripts/b05_low_anointed_restoration_l1_l3_v0.py"),
}


class AnointedDestinyExploration:
    """One native Anointed state's separate capped Destiny accounting."""

    def __init__(self,encounter,native):
        if (getattr(encounter,"g4",None) is None
                or getattr(encounter.g4,"clock",None) is None
                or getattr(encounter.g4,"anointed_destiny_exploration",None) is not None
                or getattr(native,"e",None) is not encounter
                or not isinstance(getattr(native,"caster",None),str)
                or native.caster not in encounter.actors):
            raise ValueError("One native G4.2 clock and source Anointed required")
        self.e=encounter
        self.native=native
        self.caster=native.caster
        actor=encounter.actors[self.caster]
        if actor.source.source_id not in SOURCE_PATHS:
            raise ValueError("Only sourced AH/AM/AL Restoration")
        focus,path=SOURCE_PATHS[actor.source.source_id]
        state=native.state
        if (actor.source.path!=path or actor.source.digest!=_fingerprint(path)
                or actor.source.status!="STRUCTURAL_B05_ONLY"
                or state.aspect!="Restoration" or state.focus!=focus
                or state.level!=actor.level):
            raise ValueError("Native state and source sheet must match")
        self.last_world_seconds=encounter.g4.clock.world_seconds
        self.partial_minute_seconds=0
        self._require_boundary()
        encounter.g4.anointed_destiny_exploration=self
        encounter.log("b05_anointed_destiny_clock_bound",
                      caster=self.caster,focus=focus,level=actor.level,
                      source_digest=actor.source.digest,
                      world_seconds=self.last_world_seconds,
                      initial_destiny=state.destiny,
                      noncombat_only=True,independent_focus_certified=False)

    def _require_boundary(self):
        e=self.e
        if (e.g4.clock.mode!="exploration" or e.current is not None
                or (e.round and e.cursor not in (0,len(e.order)))):
            raise UnresolvedDecision(
                "Destiny exploration accounting only at a real G4.2 noncombat boundary")
        if getattr(e.g4,"anointed_destiny_exploration",None) not in (None,self):
            raise ValueError("Anointed Destiny owner mismatch")

    def sync_world_time(self):
        """Only count real G4.2 exploration seconds; preserve subminute scraps."""
        self._require_boundary()
        clock=self.e.g4.clock
        elapsed=clock.world_seconds-self.last_world_seconds
        if elapsed<0:
            raise AssertionError("Authoritative G4.2 world time cannot move backwards")
        before=self.native.state
        if before.active_bond:
            total=self.partial_minute_seconds+elapsed
            minutes,left=divmod(total,60)
            next_state=recover_destiny(before,minutes)
            self.partial_minute_seconds=left
        else:
            # No time earned during Dormancy; pre-existing active-time
            # progress remains, but idle Dormant seconds do not roll forward.
            minutes=0
            next_state=before
        self.native.state=next_state
        self.last_world_seconds=clock.world_seconds
        self.e.log("b05_anointed_destiny_time_reconciled",
                   caster=self.caster,source_digest=self.e.actors[self.caster].source.digest,
                   world_seconds=clock.world_seconds,actual_elapsed_seconds=elapsed,
                   eligible_minutes=minutes,partial_minute_seconds=self.partial_minute_seconds,
                   active_bond=before.active_bond,
                   six_hour_remainder_before=before.six_hour_remainder_minutes,
                   six_hour_remainder_after=next_state.six_hour_remainder_minutes,
                   destiny_before=before.destiny,destiny_after=next_state.destiny,
                   destiny_recovered=next_state.destiny-before.destiny,
                   no_synthetic_g0_step=True)
        self.e.check()
        return next_state.destiny-before.destiny

    def record_mission_event(self,event_id,*,gm_recognized):
        """External GM verdict, NOT internally inferred quest completion."""
        self._require_boundary()
        if gm_recognized is not True:
            raise UnresolvedDecision("Only an explicit GM-recognized significant story beat")
        if not isinstance(event_id,str) or not event_id.strip():
            raise ValueError("Distinct nonempty GM significant-event identifier required")
        # Preserve chronology: credit already-elapsed real time before
        # the separately GM-recognized event reaches the Destiny pool.
        self.sync_world_time()
        old=self.native.state
        if not old.active_bond or event_id in old.mission_awards:
            raise ValueError("Dormant or already recognized Mission beat cannot award again")
        new=mission_event(old,event_id,gm_recognized=True)
        if event_id not in new.mission_awards:
            raise AssertionError("Source Mission event was not consumed")
        self.native.state=new
        self.e.log("b05_anointed_destiny_mission_recognized",
                   caster=self.caster,event_id=event_id,
                   source_digest=self.e.actors[self.caster].source.digest,
                   gm_verdict="external_explicit",
                   world_seconds=self.e.g4.clock.world_seconds,
                   destiny_before=old.destiny,destiny_after=new.destiny,
                   destiny_awarded=new.destiny-old.destiny,
                   event_unique=True,quest_not_ended=True)
        self.e.check()
        return new.destiny-old.destiny

    def apply_bond_verdict(self,*,active,gm_recognized):
        """Only apply explicitly GM-adjudicated bond status, never detect morality."""
        self._require_boundary()
        if type(active) is not bool or gm_recognized is not True:
            raise UnresolvedDecision("GM must separately adjudicate active Mission bond")
        # Credit eligible elapsed time BEFORE changing the GM's bond state.
        self.sync_world_time()
        old=self.native.state
        new=set_bond(old,active=active)
        self.native.state=new
        self.e.log("b05_anointed_destiny_bond_verdict",
                   caster=self.caster,source_digest=self.e.actors[self.caster].source.digest,
                   gm_verdict="external_explicit",active_before=old.active_bond,
                   active_after=new.active_bond,
                   vessel_after=new.invested_vessel,embodied_after=new.embodied,
                   world_seconds=self.e.g4.clock.world_seconds,
                   no_automatic_morality=True)
        self.e.check()
        return new.active_bond
