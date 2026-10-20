"""G4.3 mundane toxin source/clock/one-instance acceptance probes."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor,
    enemy_actor,
)
from scripts.b06_damage_v0 import DamageState
from scripts.b06_mundane_toxins_v0 import PROFILES


def scene(*,phase=None):
    a=party_actor("F",3,"hero","party",occupied=((1,1),))
    e=Encounter([a],{"hero":100},seed=431,scenario="G4.3",
                policy="explicit_delivery_and_resistance")
    d=DamageState(e,recovery_phase_seconds=(
        {"hero":phase} if phase is not None else None))
    e.begin_round()
    return e,a,d,d.toxins,d.clock


def exposure(t,profile,key,*,die=1,ward=None,delivery=True,
             piercing=1,breach=False,route=None,rolls=None):
    required=PROFILES[profile][1]
    if profile in ("TX-HM","TX-NC"):
        # Independent precommitted d20 per FUTURE damaging packet, not a
        # single exposure die replayed on a second HP=0 wound crossing.
        vit=dict(t.e.actors["hero"].source.abilities)["Vitality"]
        # A missing resistance die is rejected before these matter.
        count=PROFILES[profile][3 if (type(die) is int and
                  die+vit>=(12 if PROFILES[profile][0]=="Moderate" else 10))
                                else 2]-(2 if profile=="TX-NC" else 0)
        rolls=(tuple(range(10,10+count)) if rolls is None else rolls)
    return t.apply("hero",profile,exposure_key=key,source="fiction:verified:"+key,
                   route=required if route is None else route,
                   delivery_verified=delivery,breach_verified=breach,
                   residual_piercing_hp=(piercing if required=="injection" else 0),
                   resistance_die=die,preventive_ward=ward,
                   wound_location_roll=10 if profile=="TX-CY" else None,
                   wound_location_rolls=rolls)


def events(e,kind):
    return [x["detail"] for x in e.ledger if x["kind"]==kind]


def take_turn(e):
    e.start_turn("hero",regen_choice=RegenerationChoice())
    e.end_turn()
    e.begin_round()


class G43Toxins(unittest.TestCase):
    def test_01_profile_coverage_and_no_automatic_delivery(self):
        self.assertEqual(set(PROFILES),
                         {"TX-HM","TX-NE","TX-CY","TX-NC","TX-MY","TX-CA",
                          "TX-HE","TX-NP","TX-PN","TX-EN","TX-DE"})
        e,a,d,t,c=scene()
        o=exposure(t,"TX-HM","miss",delivery=False)
        self.assertEqual(o["outcome"],"not_delivered")
        self.assertIsNone(t.active("hero"))
        self.assertFalse(events(e,"g43_toxin_accepted"))
        with self.assertRaises(ValueError):
            exposure(t,"TX-MY","wrong",route="contact")
        self.assertIsNone(t.active("hero"))
        e.check()

    def test_02_injection_requires_actual_piercing_or_separate_breach(self):
        e,a,d,t,c=scene()
        self.assertEqual(exposure(t,"TX-HM","stopped",piercing=0)["outcome"],
                         "not_delivered")
        self.assertIsNone(t.active("hero"))
        x=exposure(t,"TX-HM","breach",piercing=0,breach=True)
        self.assertEqual(x["outcome"],"accepted")
        self.assertEqual(t.active("hero")["result"],"Full")
        e.check()

    def test_03_nonstack_equal_minor_ignored_without_ward_or_save(self):
        e,a,d,t,c=scene()
        exposure(t,"TX-MY","first")
        fired=[]
        o=t.apply("hero","TX-DE",exposure_key="ignored",source="fiction:test",
                  route="contact",delivery_verified=True,
                  preventive_ward=lambda *_:fired.append(True),
                  resistance_die=None)
        self.assertEqual(o["outcome"],"ignored")
        self.assertFalse(fired)
        self.assertEqual(t.active("hero")["key"],"first")
        self.assertEqual(len(events(e,"g43_toxin_accepted")),1)
        e.check()

    def test_04_higher_grade_ward_preserves_old_instance(self):
        e,a,d,t,c=scene()
        exposure(t,"TX-MY","minor")
        inspected=[]
        o=exposure(t,"TX-HM","blocked",die=None,
                   ward=lambda ev,who,p,g:inspected.append((who,p,g)) or True)
        self.assertEqual(o["outcome"],"prevented")
        self.assertEqual(inspected,[("hero","TX-HM","Moderate")])
        self.assertEqual(t.active("hero")["key"],"minor")
        self.assertEqual(len(events(e,"g43_toxin_accepted")),1)
        e.check()

    def test_05_higher_grade_valid_replacement_and_no_refund(self):
        e,a,d,t,c=scene()
        a.hp-=1
        exposure(t,"TX-MY","minor")
        o=exposure(t,"TX-HM","moderate")
        self.assertEqual(o["outcome"],"accepted")
        self.assertEqual(t.active("hero")["profile"],"TX-HM")
        self.assertEqual(t.modifier("hero","mp"),0)
        self.assertEqual(a.hp,a.hp_max-1)
        self.assertEqual(events(e,"g43_toxin_ended")[-1]["reason"],
                         "higher_printed_grade_replaced")
        with self.assertRaises(ValueError):
            exposure(t,"TX-HM","moderate")
        e.check()

    def test_06_natural_tie_reduced_not_immune(self):
        e,a,d,t,c=scene()
        vit=dict(a.source.abilities)["Vitality"]
        die=12-vit
        self.assertTrue(1<=die<=20)
        o=exposure(t,"TX-HM","tie",die=die)
        self.assertEqual(o["resistance_total"],12)
        self.assertEqual(o["resolution"],"Reduced")
        d.advance_exploration(18)
        self.assertEqual(a.hp,a.hp_max-3)
        self.assertIsNone(t.active("hero"))
        self.assertEqual(len(events(e,"g4_damage_applied")),3)
        e.check()

    def test_07_neurotoxin_dodge_only_and_five_interval_expiry(self):
        e,a,d,t,c=scene()
        exposure(t,"TX-NE","neuro")
        self.assertEqual(t.modifier("hero","dodge"),-2)
        self.assertEqual(t.modifier("hero","muscular_strength"),0)
        base=10+min(a.agility,4)+a.awareness
        self.assertEqual(e.defense("hero","dodge",attack_key="one"),base-2)
        self.assertEqual(a.dodge_pressure,2)
        d.advance_exploration(30)
        self.assertEqual(t.modifier("hero","dodge"),0)
        self.assertIsNone(t.active("hero"))
        e.check()

    def test_08_cytotoxin_immediate_and_three_interval_residual(self):
        e,a,d,t,c=scene()
        o=exposure(t,"TX-CY","contact",die=20)
        self.assertEqual(o["resolution"],"Reduced")
        self.assertEqual(a.hp,a.hp_max-2)
        self.assertEqual(len(events(e,"g4_damage_applied")),1)
        self.assertIsNotNone(t.active("hero"))
        d.advance_exploration(17)
        self.assertIsNotNone(t.active("hero"))
        d.advance_exploration(1)
        self.assertIsNone(t.active("hero"))
        self.assertEqual(a.hp,a.hp_max-2)
        self.assertFalse(events(e,"regeneration_step"))
        e.check()

    def test_09_necrotoxin_two_delays_then_three_actual_packets(self):
        e,a,d,t,c=scene()
        exposure(t,"TX-NC","necrosis")
        d.advance_exploration(12)
        self.assertEqual(a.hp,a.hp_max)
        self.assertEqual(t.active("hero")["left"],3)
        d.advance_exploration(18)
        self.assertEqual(a.hp,a.hp_max-3)
        self.assertEqual(len(events(e,"g4_damage_applied")),3)
        self.assertIsNone(t.active("hero"))
        e.check()

    def test_10_myo_mp_strength_scope_and_short_duration(self):
        e,a,d,t,c=scene()
        exposure(t,"TX-MY","muscle")
        self.assertEqual((t.modifier("hero","mp"),
                          t.modifier("hero","muscular_strength")),(-2,-1))
        self.assertEqual(t.modifier("hero","physical_exertion"),0)
        e.start_turn("hero",regen_choice=RegenerationChoice())
        self.assertEqual(a.mp_remaining,10)
        e.end_turn()
        d.advance_exploration(36)
        self.assertIsNone(t.active("hero"))
        e.check()

    def test_11_cardiotoxin_penalizes_real_step2_not_exploration_regen(self):
        e,a,d,t,c=scene()
        a.hp-=4;a.vigor-=4
        exposure(t,"TX-CA","cardiac")
        before=(a.hp,a.vigor)
        d.advance_exploration(6)
        self.assertEqual((a.hp,a.vigor),before)
        self.assertEqual(t.modifier("hero","regen_throughput"),-1)
        e.start_turn("hero",regen_choice=RegenerationChoice(hp=1))
        self.assertEqual(a.hp,before[0]+1)
        self.assertEqual(a.vigor,before[1]-1)
        e.end_turn()
        d.advance_exploration(18)
        self.assertIsNone(t.active("hero"))
        self.assertFalse(any(x["kind"]=="regeneration_step" and
                   x["detail"]["actor"]=="fake" for x in e.ledger))
        e.check()

    def test_12_pneumo_dermato_and_entero_named_penalties(self):
        for profile,use,expected in (
            ("TX-PN","breathing_endurance",-1),
            ("TX-DE","contact_precision",-1),
            ("TX-EN","physical_exertion",-1)):
            with self.subTest(profile=profile):
                e,a,d,t,c=scene()
                exposure(t,profile,"p-"+profile)
                self.assertEqual(t.modifier("hero",use),expected)
                self.assertEqual(t.modifier("hero","dodge"),0)
                self.assertEqual(t.modifier("hero","regen_throughput"),0)
                e.check()

    def test_13_nephrotoxin_hourly_vigor_packets_not_hp(self):
        e,a,d,t,c=scene()
        before=(a.hp,a.vigor)
        exposure(t,"TX-NP","kidney")
        d.advance_exploration(3599)
        self.assertEqual((a.hp,a.vigor),before)
        d.advance_exploration(1)
        self.assertEqual((a.hp,a.vigor),(before[0],before[1]-1))
        d.advance_exploration(10800)
        self.assertEqual(a.vigor,before[1]-4)
        self.assertEqual(a.hp,before[0])
        self.assertIsNone(t.active("hero"))
        self.assertEqual(len(events(e,"g4_damage_applied")),4)
        e.check()

    def test_14_enterotoxin_two_vs_three_hours(self):
        for die,hours in ((20,2),(1,3)):
            with self.subTest(hours=hours):
                e,a,d,t,c=scene()
                exposure(t,"TX-EN","meal",die=die)
                d.advance_exploration(hours*3600-1)
                self.assertIsNotNone(t.active("hero"))
                d.advance_exploration(1)
                self.assertIsNone(t.active("hero"))
                self.assertEqual(t.modifier("hero","physical_exertion"),0)
                e.check()

    def test_15_hepato_penalizes_existing_recovery_once_spent_vp_unchanged(self):
        a_due=5
        e,a,d,t,c=scene(phase=a_due)
        a.vigor-=10;a.vp_spent=4;a.vp_available-=4
        original=c.events["recovery:hero:1"]
        exposure(t,"TX-HE","liver")
        self.assertEqual(t.active("hero")["recovery_id"],original.ident)
        d.advance_exploration(5)
        self.assertIsNone(t.active("hero"))
        self.assertTrue(original.consumed)
        recovered=events(e,"g4_six_hour_recovery")
        self.assertEqual(len(recovered),1)
        expected=max(1,(a.vigor_max+2)//4)-2
        self.assertEqual(recovered[0]["vigor"],expected)
        self.assertEqual(recovered[0]["spent_vp_recovered"],
                         min(4,max(1,(a.vp_max+2)//4)))
        self.assertEqual(recovered[0]["toxin_recovery_reduction"],2)
        self.assertTrue(any(v["reason"]=="recovery_intercepted"
                            for v in events(e,"g43_toxin_ended")))
        d.advance_exploration(21600)
        self.assertEqual(len(events(e,"g43_hepatotoxin_recovery")),1)
        e.check()

    def test_16_hepato_expiry_before_recovery_does_not_steal_it(self):
        e,a,d,t,c=scene(phase=21600)
        a.vigor-=10
        # Consume 100 seconds so Recovery is 21,500 away; expose
        # afterward: it will intercept before its own 21,600s expiry.
        d.advance_exploration(100)
        exposure(t,"TX-HE","earlier")
        d.advance_exploration(21500)
        self.assertEqual(len(events(e,"g43_hepatotoxin_recovery")),1)
        self.assertIsNone(t.active("hero"))
        e.check()

    def test_17_hepato_true_tie_recovery_before_expiry(self):
        e,a,d,t,c=scene(phase=21600)
        a.vigor-=10
        exposure(t,"TX-HE","tie")
        d.advance_exploration(21600)
        self.assertTrue(c.events["recovery:hero:1"].consumed)
        self.assertEqual(len(events(e,"g43_hepatotoxin_recovery")),1)
        self.assertIsNone(t.active("hero"))
        self.assertEqual(len(events(e,"g4_six_hour_recovery")),1)
        e.check()

    def test_18_hourly_milestone_across_initiative_exit(self):
        e,a,d,t,c=scene()
        exposure(t,"TX-NP","round-kidney")
        d.advance_exploration(3563)
        c.enter_initiative()
        self.assertEqual(t.active("hero")["remaining"],4)
        self.assertEqual(c.events[t.active("hero")["marker"]].due_round,7)
        e.start_turn("hero",regen_choice=RegenerationChoice());e.end_turn()
        c.leave_initiative()
        d.advance_exploration(24)
        self.assertEqual(t.active("hero")["remaining"],3)
        self.assertEqual(a.vigor,a.vigor_max-1)
        self.assertFalse(events(e,"regeneration_step") == [])
        e.check()

    def test_19_short_phase_5_5_5_5_5_survives_mode_switch(self):
        e,a,d,t,c=scene()
        exposure(t,"TX-HM","short-phase")
        for _ in range(5):
            d.advance_exploration(5)
            c.enter_initiative();c.leave_initiative()
        self.assertEqual(t.active("hero")["phase"],1)
        self.assertEqual(t.active("hero")["left"],1)
        self.assertEqual(a.hp,a.hp_max-4)
        e.check()

    def test_20_legacy_hemotoxin_cannot_coexist_with_new_instance(self):
        e,a,d,t,c=scene()
        exposure(t,"TX-NE","new-neuro")
        original=t.active("hero")
        self.assertEqual(original["grade"],"Moderate")
        ignored=d.schedule_hemotoxin("hero",exposure_key="old-thorn",
                  actual_exposure=True,resistance_total=None,
                  wound_location_roll=None)
        self.assertEqual(ignored,{"outcome":"ignored","active":"new-neuro"})
        self.assertIs(t.active("hero"),original)
        self.assertFalse(d.short_toxins)
        self.assertIn("old-thorn",t.exposure_ids)
        t.stop_authorized("hero",reason="external_independent_cure",
                          authorized=True)
        # A previously ignored exposure key cannot be replayed even
        # after the first instance ends; a NEW real exposure is legal.
        with self.assertRaisesRegex(ValueError,"already processed"):
            d.schedule_hemotoxin("hero",exposure_key="old-thorn",
                 actual_exposure=True,resistance_total=9,wound_location_roll=10)
        d.schedule_hemotoxin("hero",exposure_key="fresh-thorn",
             actual_exposure=True,resistance_total=9,wound_location_roll=10)
        self.assertEqual(len(d.short_toxins),1)
        self.assertIsNone(t.active("hero"))
        with self.assertRaises(UnresolvedDecision):
            exposure(t,"TX-MY","another")
        e.check()

    def test_21_no_extra_step2_and_same_packet_wound_crossing(self):
        e,a,d,t,c=scene()
        a.hp=2;a.vigor=4
        exposure(t,"TX-HM","cross")
        d.advance_exploration(12)
        self.assertEqual(a.hp,0)
        self.assertEqual(len(a.wounds),1)
        self.assertEqual(len(events(e,"regeneration_step")),0)
        self.assertEqual(len(events(e,"g4_damage_applied")),2)
        e.check()

    def test_22_missing_roll_and_unauthorized_end_do_not_mutate(self):
        e,a,d,t,c=scene()
        with self.assertRaises(UnresolvedDecision):
            exposure(t,"TX-HM","unrolled",die=None)
        self.assertIsNone(t.active("hero"))
        exposure(t,"TX-MY","valid")
        with self.assertRaises(UnresolvedDecision):
            t.stop_authorized("hero",reason="free_cure",authorized=False)
        self.assertEqual(t.active("hero")["key"],"valid")
        e.check()


    def test_23_enemy_json_lowercase_vitality_on_all_three_fixtures(self):
        for source_id,state,occupied in (
            ("B06-EN-01","cold_start",((1,1),)),
            ("B06-EN-02",None,((1,1),)),
            ("B06-EN-03",None,((1,1),(2,1)))):
            with self.subTest(source_id=source_id):
                enemy=enemy_actor(source_id,"foe","enemy",
                                  start_state=state,occupied=occupied)
                attributes=dict(enemy.source.abilities)
                self.assertIn("vitality",attributes)
                self.assertNotIn("Vitality",attributes)
                e=Encounter([enemy],{"foe":100},seed=437,
                            scenario="G4.3-enemy-resistance",policy="explicit")
                d=DamageState(e);e.begin_round()
                result=d.toxins.apply("foe","TX-NE",
                      exposure_key="foe-neuro",source="attested:sting",
                      route="injection",delivery_verified=True,
                      residual_piercing_hp=1,resistance_die=11)
                expected=11+attributes["vitality"]
                self.assertEqual(result["resistance_total"],expected)
                self.assertEqual(result["resolution"],
                     "Reduced" if expected>=12 else "Full")
                self.assertEqual(d.toxins.active("foe")["profile"],"TX-NE")
                self.assertEqual(len(events(e,"g43_toxin_accepted")),1)
                e.check()

    def test_24_expired_legacy_key_cannot_be_reused_by_unified_path(self):
        e,a,d,t,c=scene()
        d.schedule_hemotoxin("hero",exposure_key="old-finished",
                             actual_exposure=True,resistance_total=12,
                             wound_location_roll=10)
        d.advance_exploration(18)
        self.assertEqual(d.short_toxins[0]["left"],0)
        self.assertIsNone(t.active("hero"))
        before=(len(t.exposure_ids),len(events(e,"g43_toxin_accepted")),
                len(events(e,"g43_exposure_rejected")))
        with self.assertRaisesRegex(ValueError,"Toxin exposure key already processed"):
            exposure(t,"TX-MY","old-finished")
        self.assertEqual((len(t.exposure_ids),
                          len(events(e,"g43_toxin_accepted")),
                          len(events(e,"g43_exposure_rejected"))),before)
        self.assertIsNone(t.active("hero"))
        self.assertEqual(len(d.short_toxins),1)
        # Fresh identity is still valid after the previous toxin has ended.
        outcome=exposure(t,"TX-MY","fresh")
        self.assertEqual(outcome["outcome"],"accepted")
        e.check()

    def test_25_crossing_uses_distinct_packet_rolls_after_real_repair(self):
        for profile in ("TX-HM","TX-NC"):
            with self.subTest(profile=profile):
                e,a,d,t,c=scene()
                a.hp=1
                rolls=(1,20,14,16,18) if profile=="TX-HM" else (1,20,14)
                exposure(t,profile,"repeat",rolls=rolls)
                if profile=="TX-NC":
                    # The two non-damaging intervals do not consume rolls.
                    d.advance_exploration(12)
                    self.assertEqual(a.hp,1)
                    self.assertEqual(t.active("hero")["applied"],0)
                d.advance_exploration(6)
                first=a.wounds[-1]
                self.assertEqual((a.hp,first.location),(0,"Head / neck"))
                self.assertEqual(first.source_event,"toxin:repeat:packet:1")
                # Exactly five independently paid and successfully delivered
                # Primary heals can repair this Serious wound at 2 each.
                # One paid Secondary then returns 1 HP above the threshold.
                for _ in range(5):
                    d.resolve_heal("hero",contribution="Primary",
                                   vigor_amount=0,source="test:paid_external_heal")
                self.assertEqual((first.progress,a.hp),(10,0))
                d.resolve_heal("hero",contribution="Secondary",vigor_amount=0,
                               source="test:paid_external_heal")
                self.assertEqual(a.hp,1)
                d.advance_exploration(6)
                self.assertEqual(a.hp,0)
                self.assertEqual(len(a.wounds),2)
                second=a.wounds[1]
                self.assertEqual(second.location,"Hand / extremity")
                self.assertEqual(second.source_event,"toxin:repeat:packet:2")
                self.assertNotEqual(first.source_event,second.source_event)
                self.assertEqual(t.active("hero")["applied"],2)
                e.check()

    def test_26_recurring_hp_requires_independent_precommitted_rolls(self):
        for profile in ("TX-HM","TX-NC"):
            with self.subTest(profile=profile):
                e,a,d,t,c=scene()
                required=5 if profile=="TX-HM" else 3
                baseline=(len(t.exposure_ids),len(events(e,"g43_toxin_accepted")),
                          len(c.events))
                for supplied in (None,(10,),tuple([10]*(required-1)),
                                 tuple([10]*(required-1)+[0]),
                                 tuple([10]*(required-1)+[True])):
                    with self.subTest(rolls=supplied):
                        with self.assertRaisesRegex(
                                UnresolvedDecision,
                                "independent wound-location d20 per future HP packet"):
                            t.apply("hero",profile,exposure_key="bad-rolls",
                                    source="attested:source",route="injection",
                                    delivery_verified=True,
                                    residual_piercing_hp=1,resistance_die=1,
                                    wound_location_rolls=supplied)
                        self.assertIsNone(t.active("hero"))
                        self.assertEqual((len(t.exposure_ids),
                                          len(events(e,"g43_toxin_accepted")),
                                          len(c.events)),baseline)
                with self.assertRaisesRegex(
                        UnresolvedDecision,"independent wound-location d20"):
                    t.apply("hero",profile,exposure_key="scalar-only",
                            source="attested:source",route="injection",
                            delivery_verified=True,residual_piercing_hp=1,
                            resistance_die=1,wound_location_roll=10)
                e.check()

if __name__=="__main__":
    unittest.main()
