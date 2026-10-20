"""Deterministic B06 G4.2: actual world chronology and native round mapping."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_damage_v0 import DamageState
from scripts.b06_world_clock_v0 import SIX_HOURS, WorldClock


def pc(ident="hero",point=(1,1)):
    return party_actor("F",3,ident,"party",occupied=(point,))


def soldier(ident="soldier",point=(2,1)):
    return enemy_actor("B06-EN-02",ident,"enemy",occupied=(point,))


def scene(*actors, phases=None):
    e=Encounter(list(actors),{a.id:100-i for i,a in enumerate(actors)},
                seed=422,scenario="B06-G4.2",policy="explicit_clock")
    g4=DamageState(e,recovery_phase_seconds=phases)
    e.begin_round()
    return e,g4,g4.clock


def events(e,kind):
    return [x["detail"] for x in e.ledger if x["kind"]==kind]


def next_round(e):
    for actor_id in e.order:
        e.start_turn(actor_id,regen_choice=RegenerationChoice())
        e.end_turn()
    e.begin_round()


class G42ClockTests(unittest.TestCase):
    def test_01_exact_six_hour_phase_and_spent_only(self):
        a=pc();a.vigor-=10;a.vp_spent=7;a.vp_available-=7
        e,d,c=scene(a)
        d.advance_exploration(SIX_HOURS-1)
        self.assertEqual((a.vigor,a.vp_spent),(a.vigor_max-10,7))
        d.advance_exploration(1)
        self.assertEqual((a.vigor,a.vp_spent),(a.vigor_max-1,2))
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertEqual(events(e,"g4_six_hour_recovery")[0]["checkpoint_id"],
                         "recovery:hero:1")
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        self.assertEqual(c.events["recovery:hero:2"].due_seconds,2*SIX_HOURS)
        self.assertEqual(a.vp_available+a.vp_committed+a.vp_spent,a.vp_max)
        e.check()

    def test_02_independent_recipient_phase_no_scene_reset(self):
        a=pc("first");b=pc("second",(3,1))
        a.vigor-=4;b.vigor-=4
        e,d,c=scene(a,b,phases={"first":5,"second":13})
        d.advance_exploration(5)
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertEqual(events(e,"g4_six_hour_recovery")[0]["actor"],"first")
        self.assertEqual((a.vigor,b.vigor),(a.vigor_max,b.vigor_max-4))
        d.advance_exploration(7)
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        d.advance_exploration(1)
        self.assertEqual([x["actor"] for x in events(e,"g4_six_hour_recovery")],
                         ["first","second"])
        self.assertEqual(c.events["recovery:first:2"].due_seconds,SIX_HOURS+5)
        self.assertEqual(c.events["recovery:second:2"].due_seconds,SIX_HOURS+13)
        e.check()

    def test_03_milestones_and_recovery_interleave_in_one_long_advance(self):
        a=pc();a.vigor-=8
        e,d,c=scene(a,phases={"hero":38})
        c.schedule_milestone("hero",event_id="clock:first",source="authored:A",
                             delay_seconds=37)
        c.schedule_milestone("hero",event_id="clock:last",source="authored:B",
                             delay_seconds=40)
        d.advance_exploration(41)
        due=[x for x in e.ledger
             if x["kind"] in ("g42_milestone_due","g4_six_hour_recovery")]
        self.assertEqual([x["detail"].get("event_id",x["detail"].get("checkpoint_id"))
                          for x in due],
                         ["clock:first","recovery:hero:1","clock:last"])
        self.assertEqual([x["detail"]["world_seconds"] for x in due],[37,38,40])
        self.assertEqual(c.world_seconds,41)
        e.check()

    def test_04_short_toxin_phase_5_plus_5_plus_5_plus_5_plus_5(self):
        a=soldier();a.hp=10
        e,d,c=scene(a)
        d.schedule_hemotoxin("soldier",exposure_key="phase-25",
             actual_exposure=True,resistance_total=11,wound_location_roll=10)
        for n in range(5):
            d.advance_exploration(5)
            c.enter_initiative()
            c.leave_initiative()
        self.assertEqual(d.short_toxins[0]["applied"],4)
        self.assertEqual(d.short_toxins[0]["phase"],1)
        self.assertEqual(a.hp,6)
        self.assertFalse(events(e,"regeneration_step"))
        self.assertEqual(c.world_seconds,25)
        e.check()

    def test_05_genuine_step_two_then_three_plus_exploration_phase(self):
        a=soldier();a.hp=10
        e,d,c=scene(a)
        d.schedule_hemotoxin("soldier",exposure_key="mix-5-1",
             actual_exposure=True,resistance_total=11,wound_location_roll=10)
        d.advance_exploration(5)
        c.enter_initiative()
        e.start_turn("soldier",regen_choice=RegenerationChoice())
        self.assertEqual((a.hp,d.short_toxins[0]["applied"]),(9,1))
        e.end_turn()
        c.leave_initiative()
        d.advance_exploration(1)
        self.assertEqual((a.hp,d.short_toxins[0]["applied"]),(8,2))
        self.assertEqual(len(events(e,"regeneration_step")),1)
        self.assertEqual(d.short_toxins[0]["phase"],0)
        e.check()

    def test_06_enter_with_one_second_applies_milestone_and_recovery(self):
        a=pc();a.vigor-=6
        e,d,c=scene(a,phases={"hero":1})
        c.schedule_milestone("hero",event_id="clock:urgent",source="authored:urgent",
                             delay_seconds=1)
        c.enter_initiative()
        self.assertEqual(e.round,1)
        self.assertTrue(c.events["clock:urgent"].consumed)
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertEqual(events(e,"g42_milestone_due")[0]["round_begin"],1)
        self.assertEqual(c.events["recovery:hero:2"].due_round,3601)
        e.check()

    def test_07_conservative_37_seconds_to_round_begin_r_plus_six(self):
        a=pc();e,d,c=scene(a,phases={"hero":39})
        c.schedule_milestone("hero",event_id="clock:37",source="authored:37",
                             delay_seconds=37)
        c.enter_initiative()
        self.assertEqual(c.events["clock:37"].due_round,7)
        self.assertEqual(c.events["recovery:hero:1"].due_round,7)
        for _ in range(5):
            next_round(e)
        self.assertFalse(c.events["clock:37"].consumed)
        next_round(e)
        self.assertTrue(c.events["clock:37"].consumed)
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        self.assertEqual(events(e,"g42_milestone_due")[0]["round_begin"],7)
        e.check()

    def test_08_rounding_coalescence_keeps_original_instant_order(self):
        a=pc();a.vigor-=4
        e,d,c=scene(a,phases={"hero":39})
        c.schedule_milestone("hero",event_id="m:late",source="authored:L",
                             delay_seconds=41)
        c.schedule_milestone("hero",event_id="m:early",source="authored:E",
                             delay_seconds=37)
        c.enter_initiative()
        for _ in range(6):
            next_round(e)
        occurred=[x["detail"].get("event_id",x["detail"].get("checkpoint_id"))
                  for x in e.ledger if x["kind"] in
                  ("g42_milestone_due","g4_six_hour_recovery")]
        self.assertEqual(occurred,["m:early","recovery:hero:1","m:late"])
        e.check()

    def test_09_exit_uses_e_minus_c_minus_one_and_no_replay(self):
        a=pc();e,d,c=scene(a)
        c.schedule_milestone("hero",event_id="out:37",source="authored:out",
                             delay_seconds=37)
        c.enter_initiative()
        e.start_turn("hero",regen_choice=RegenerationChoice());e.end_turn()
        c.leave_initiative()
        self.assertEqual(c.events["out:37"].due_seconds,30)
        d.advance_exploration(29)
        self.assertFalse(c.events["out:37"].consumed)
        d.advance_exploration(1)
        self.assertEqual(len(events(e,"g42_milestone_due")),1)
        c.enter_initiative();c.leave_initiative()
        self.assertEqual(len(events(e,"g42_milestone_due")),1)
        e.check()

    def test_10_recovery_earned_inside_initiative_cannot_be_repaid_on_exit(self):
        a=pc();a.vigor-=5;a.vp_spent=4;a.vp_available-=4
        e,d,c=scene(a,phases={"hero":13})
        c.enter_initiative()  # q=floor(13/6)=2, due Round Begin 3.
        next_round(e)
        self.assertFalse(c.events["recovery:hero:1"].consumed)
        next_round(e)
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        paid=(a.vigor,a.vp_spent)
        e.start_turn("hero",regen_choice=RegenerationChoice());e.end_turn()
        c.leave_initiative()
        d.advance_exploration(0)
        self.assertEqual((a.vigor,a.vp_spent),paid)
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertTrue(c.events["recovery:hero:2"].due_seconds>c.world_seconds)
        e.check()

    def test_11_exit_immediate_q_one_and_reentry_no_double_credit(self):
        a=pc();a.vigor-=5
        e,d,c=scene(a,phases={"hero":8})
        c.enter_initiative()  # event R+1.
        e.start_turn("hero",regen_choice=RegenerationChoice());e.end_turn()
        c.leave_initiative()  # E=C+1 => due now.
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        c.enter_initiative();c.leave_initiative()
        d.advance_exploration(0)
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertEqual(c.recovery_serial["hero"],3)
        e.check()

    def test_12_new_milestone_in_initiative_requires_authorized_unit(self):
        a=pc();e,d,c=scene(a);c.enter_initiative()
        with self.assertRaises(UnresolvedDecision):
            c.schedule_milestone("hero",event_id="illegal",source="fiction",
                                 delay_seconds=37)
        c.schedule_milestone("hero",event_id="future",source="authored:R",
                             delay_seconds=600)
        self.assertEqual(c.events["future"].due_round,101)
        self.assertFalse(c.events["future"].consumed)
        e.start_turn("hero",regen_choice=RegenerationChoice());e.end_turn()
        c.leave_initiative()
        self.assertEqual(c.events["future"].due_seconds,594)
        e.check()

    def test_13_source_identity_cancellation_and_no_id_reuse(self):
        a=pc();e,d,c=scene(a)
        ev=c.schedule_milestone("hero",event_id="source:marker",
                                source="authored:source",delay_seconds=5)
        self.assertEqual((ev.actor_source,ev.source_digest),
                         (a.source.source_id,a.source.digest))
        with self.assertRaises(ValueError):
            c.cancel_milestone("source:marker",source="wrong:source")
        c.cancel_milestone("source:marker",source="authored:source")
        d.advance_exploration(7)
        self.assertTrue(c.events["source:marker"].canceled)
        self.assertFalse(events(e,"g42_milestone_due"))
        with self.assertRaises(ValueError):
            c.schedule_milestone("hero",event_id="source:marker",
                                 source="authored:source",delay_seconds=1)
        e.check()

    def test_14_failed_transition_or_bad_phase_is_side_effect_free(self):
        a=pc();e,d,c=scene(a)
        with self.assertRaises(ValueError):
            c.schedule_milestone("hero",event_id="bad",source="source",
                                 delay_seconds=6,phase="unknown")
        self.assertNotIn("bad",c.events)
        c.enter_initiative()
        with self.assertRaises(ValueError):
            d.advance_exploration(6)
        with self.assertRaises(ValueError):
            c.enter_initiative()
        e.start_turn("hero",regen_choice=RegenerationChoice())
        with self.assertRaises(ValueError):
            c.leave_initiative()
        e.end_turn()
        c.leave_initiative()
        self.assertEqual(c.world_seconds,0)
        e.check()

    def test_15_full_vigor_vp_still_consumes_real_checkpoint(self):
        a=pc();e,d,c=scene(a,phases={"hero":2})
        d.advance_exploration(2)
        self.assertEqual((a.vigor,a.vp_available,a.vp_spent),
                         (a.vigor_max,a.vp_max,0))
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertEqual(events(e,"g4_six_hour_recovery")[0]["vigor"],0)
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        e.check()

    def test_16_clock_never_grants_turn_regeneration_or_dying(self):
        a=soldier();a.hp=0;a.vigor=0
        e,d,c=scene(a,phases={"soldier":12})
        d.advance_exploration(25)
        self.assertEqual(a.hp,0)
        self.assertFalse(events(e,"regeneration_step"))
        self.assertEqual(c.world_seconds,25)
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertFalse(a.dead)
        e.check()


    def test_17_exit_before_entry_round_begins_uses_entry_label(self):
        a=pc();a.vigor-=5
        e,d,c=scene(a,phases={"hero":8})
        c.schedule_milestone("hero",event_id="next:14",
                             source="authored:future",delay_seconds=14)
        # Complete round 1, then enter round-label 2 without begin_round(2).
        e.start_turn("hero",regen_choice=RegenerationChoice())
        e.end_turn()
        self.assertEqual((e.round,e.cursor),(1,len(e.order)))
        c.enter_initiative()
        self.assertEqual(c.entry_round,2)
        self.assertEqual((c.events["recovery:hero:1"].due_round,
                          c.events["next:14"].due_round),(3,4))
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),0)
        c.leave_initiative()
        # For E=3 and active C=2, E-C-1=0: Recovery due immediately.
        # E=4 instead retains 6 seconds, not 12.
        self.assertEqual(events(e,"g42_initiative_exited")[-1]["round_label"],2)
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertEqual(events(e,"g4_six_hour_recovery")[0]["checkpoint_id"],
                         "recovery:hero:1")
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        self.assertEqual(c.events["next:14"].due_seconds,6)
        self.assertFalse(c.events["next:14"].consumed)
        d.advance_exploration(5)
        self.assertFalse(c.events["next:14"].consumed)
        d.advance_exploration(1)
        self.assertEqual(len(events(e,"g42_milestone_due")),1)
        self.assertEqual(events(e,"g42_milestone_due")[0]["event_id"],
                         "next:14")
        # Consumed IDs cannot replay on any later zero-time mode switch.
        c.enter_initiative()
        c.leave_initiative()
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertEqual(len(events(e,"g42_milestone_due")),1)
        e.check()

    def test_18_future_recovery_namespace_is_not_available_to_milestones(self):
        a=pc();a.vigor-=5
        e,d,c=scene(a,phases={"hero":2})
        self.assertIn("recovery:hero:1",c.events)
        self.assertNotIn("recovery:hero:2",c.events)
        before=(len(c.events),c.sequence,c.recovery_serial["hero"],
                len(e.ledger))
        for reserved in ("recovery:hero:2","recovery:hero:999",
                         "recovery:other:2","recovery:"):
            with self.subTest(event_id=reserved):
                with self.assertRaisesRegex(ValueError,
                                            "Recovery checkpoint ID namespace"):
                    c.schedule_milestone("hero",event_id=reserved,
                                         source="authored:forged",delay_seconds=2)
                self.assertNotIn(reserved,c.events)
                self.assertEqual((len(c.events),c.sequence,
                                  c.recovery_serial["hero"],len(e.ledger)),before)
        marker=c.schedule_milestone("hero",event_id="story:marker",
                                     source="authored:story",delay_seconds=2)
        d.advance_exploration(2)
        self.assertTrue(marker.consumed)
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        self.assertIn("recovery:hero:2",c.events)
        self.assertEqual(c.events["recovery:hero:2"].kind,"recovery")
        self.assertEqual(c.events["recovery:hero:2"].ident,"recovery:hero:2")
        self.assertFalse(c.events["recovery:hero:2"].consumed)
        self.assertEqual(c.events["recovery:hero:2"].due_seconds,SIX_HOURS+2)
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        self.assertEqual(len(events(e,"g42_milestone_due")),1)
        self.assertEqual(events(e,"g42_milestone_due")[0]["event_id"],
                         "story:marker")
        e.check()

    def test_19_recovery_namespace_rejected_inside_initiative_as_well(self):
        a=pc();e,d,c=scene(a,phases={"hero":1})
        c.enter_initiative()
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        self.assertEqual(c.events["recovery:hero:2"].due_round,3601)
        before=(len(c.events),c.sequence,c.recovery_serial["hero"])
        with self.assertRaisesRegex(ValueError,"Recovery checkpoint ID namespace"):
            c.schedule_milestone("hero",event_id="recovery:hero:3",
                                 source="authored:poison",delay_seconds=600)
        self.assertEqual((len(c.events),c.sequence,
                          c.recovery_serial["hero"]),before)
        self.assertNotIn("recovery:hero:3",c.events)
        c.schedule_milestone("hero",event_id="tox:milestone",
                             source="authored:poison",delay_seconds=600)
        self.assertEqual(c.events["tox:milestone"].due_round,101)
        self.assertEqual(c.events["recovery:hero:2"].due_round,3601)
        e.check()


if __name__=="__main__":
    unittest.main()
