"""Deterministic acceptance for B06 G4 injury and recovery integration."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, Wound,
    enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamagePacket, DamageState


def soldier(ident="soldier",point=(5,2),team="enemy"):
    return enemy_actor("B06-EN-02",ident,team,occupied=(point,))


def sentry(ident="sentry",state="cold_start",point=(5,2),team="enemy"):
    return enemy_actor("B06-EN-01",ident,team,start_state=state,occupied=(point,))


def pc(role="F",ident="caster",point=(1,2),team="party",level=3):
    return party_actor(role,level,ident,team,occupied=(point,))


def scene(*actors,spatial=False):
    e=Encounter(list(actors),{a.id:100-i for i,a in enumerate(actors)},
                seed=404,scenario="B06-G4",policy="explicit_verified_delivery")
    if spatial:
        GridMovement(e,width=16,height=7)
        RangedCombat(e)
    g3=SpellState(e)
    g4=DamageState(e)
    e.begin_round()
    return e,g3,g4


class G4IntegrationTests(unittest.TestCase):
    def test_physical_armor_and_critical_dice_on_primary_only(self):
        s=soldier(); t=sentry()
        e,g,d=scene(s,t)
        r=d.apply_profile_hit("soldier","sentry","B06-AT-03",
                              die_face=6,confirmed_hit=True)
        # Sword =4+d6; Leather Armor3, Pen2 leaves 1 Armor.
        self.assertEqual((r["hp_loss"],t.hp), (9,3))
        self.assertFalse(t.wounds)
        self.assertEqual(t.vigor,t.vigor_max)
        e.check()

    def test_one_crossing_wound_is_calculated_after_full_event(self):
        t=sentry();t.hp=1
        e,g,d=scene(t)
        r=d.apply_damage("sentry",(
            DamagePacket("hp","Piercing",8,2,"weapon"),
            DamagePacket("hp","Fire",2),
            DamagePacket("vigor","Direct Vigor",3)),
            event_key="impact-1",cause="confirmed_mixed_hit",
            devastating=True,wound_location_roll=14)
        self.assertEqual(t.hp,-8)
        self.assertEqual(r["wound"],"Critical")
        self.assertEqual(len(t.wounds),1)
        w=t.wounds[0]
        self.assertEqual((w.requirement,w.location,w.trauma),(30,"Arm","Piercing"))
        self.assertEqual(t.vigor,t.vigor_max-3)
        with self.assertRaisesRegex(ValueError,"consumed"):
            d.apply_damage("sentry",(DamagePacket("hp","Fire",2),),
                           event_key="impact-1",cause="repeat")
        e.check()

    def test_threshold_death_does_not_create_repairable_wound(self):
        t=soldier();t.hp=1
        e,g,d=scene(t)
        r=d.apply_damage("soldier",(DamagePacket("hp","Fire",13),),
                         event_key="lethal",cause="confirmed_direct_effect")
        self.assertTrue(r["dead"])
        self.assertEqual(t.hp,-t.hp_max)
        self.assertEqual(t.wounds,[])
        with self.assertRaises(ValueError):
            d.apply_damage("soldier",(DamagePacket("hp","Fire",1),),
                           event_key="extra",cause="illegal")
        e.check()

    def test_explicit_location_is_preflighted_before_mutating_damage(self):
        t=soldier();t.hp=1
        e,g,d=scene(t)
        before=(t.hp,t.vigor,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"location"):
            d.apply_damage("soldier",(DamagePacket("hp","Fire",2),),
                           event_key="missing-roll",cause="hit")
        self.assertEqual((t.hp,t.vigor,len(e.ledger)),before)
        d.apply_damage("soldier",(DamagePacket("hp","Fire",2),),
                       event_key="missing-roll",cause="hit",wound_location_roll=3)
        self.assertEqual((t.hp,t.wounds[0].location),(-1,"Chest"))

    def test_oldest_first_dying_survival_consumes_actual_vigor(self):
        t=sentry();t.hp=0;t.wounds=[Wound("old",10,9),Wound("new",20,0)]
        e,g,d=scene(t)
        before=t.vigor
        e.start_turn("sentry",regen_choice=RegenerationChoice(
            repair=2,cancel_dying_loss=True))
        self.assertEqual((t.hp,t.vigor),(0,before-3))
        self.assertEqual((t.wounds[0].progress,t.wounds[1].progress),(10,1))
        self.assertEqual(e.ledger[-2]["kind"],"regeneration_step")
        self.assertEqual(t.ap_remaining,0)
        e.check()

    def test_non_dying_repair_distribution_needs_explicit_wounds(self):
        t=sentry();t.hp=9;t.wounds=[Wound("arm",10,0),Wound("leg",20,0)]
        e,g,d=scene(t)
        with self.assertRaisesRegex(UnresolvedDecision,"Select non-Dying"):
            e.start_turn("sentry",regen_choice=RegenerationChoice(repair=2))
        self.assertEqual((t.vigor,[w.progress for w in t.wounds]),
                         (t.vigor_max,[0,0]))
        e.start_turn("sentry",regen_choice=RegenerationChoice(
            hp=1,repair=2,wound_allocations=(("leg",1),("arm",1))))
        self.assertEqual((t.hp,t.vigor,[w.progress for w in t.wounds]),
                         (10,t.vigor_max-3,[1,1]))
        self.assertEqual(sum(x["kind"]=="regeneration_step" for x in e.ledger),1)
        e.check()

    def test_zero_vigor_dying_tick_has_no_free_cancellation(self):
        t=soldier();t.hp=0;t.vigor=0
        e,g,d=scene(t)
        e.start_turn("soldier")
        self.assertEqual(t.hp,-1)
        self.assertEqual(t.vigor,0)
        self.assertTrue(any(x["kind"]=="regeneration_step" for x in e.ledger))
        e.check()

    def test_natural_death_ends_maintained_effects(self):
        t=pc();t.hp=1
        e,g,d=scene(t)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        g.cast_stone("caster")
        e.end_turn()
        t.hp=-t.hp_max+1;t.vigor=0
        e.begin_round()
        e.start_turn("caster")
        self.assertTrue(t.dead)
        self.assertEqual(t.hp,-t.hp_max)
        self.assertFalse(g.effects)
        self.assertEqual(t.vp_committed,0)
        e.check()

    def test_shelter_and_typed_stone_resistance_with_unconscious_end(self):
        t=pc()
        e,g,d=scene(t)
        e.start_turn("caster")
        g.cast_scholar_composite("caster","Vital Shelter")
        hp=t.hp
        d.apply_damage("caster",(DamagePacket("hp","Fire",5),
                                   DamagePacket("vigor","Direct Vigor",5)),
                       event_key="fire-hit",cause="verified_flame")
        self.assertEqual((t.hp,hp-t.hp),(hp-3,3))
        self.assertEqual(t.vigor,t.vigor_max-1)
        self.assertFalse(g.active("caster","Vital Shelter"))
        self.assertEqual(t.vp_committed,6)
        d.apply_damage("caster",(DamagePacket("hp","Fire",20),),
                       event_key="knockout",cause="verified_flame",
                       wound_location_roll=3)
        self.assertLessEqual(t.hp,0)
        self.assertEqual(t.vp_committed,0)
        self.assertFalse(g.active("caster","Stone Skin"))
        e.check()

    def test_real_g3_flame_pending_event_consumed_once(self):
        f=pc();t=pc("R","target",(3,2),"enemy")
        e,g,d=scene(f,t,spatial=True)
        e.start_turn("caster")
        shot=g.cast_flame("caster","target",tier=1,face=12,
                          vigor_die=5,hand_available=True)
        self.assertEqual(shot["outcome"],"direct_hit_pending_G4")
        index=e.ledger[-1]["index"]
        result=d.apply_flame("caster","target",ledger_index=index)
        self.assertEqual((result["hp_loss"],result["vigor_loss"]),(2,4))
        with self.assertRaisesRegex(ValueError,"consumed"):
            d.apply_flame("caster","target",ledger_index=index)
        e.check()

    def test_g4_primary_heal_of_dying_target_uses_repair_not_regen(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp=0;t.vigor=0;t.wounds=[Wound("first",10,9),Wound("second",20,0)]
        e,g,d=scene(r,t)
        e.start_turn("caster")
        result=d.cast_basic_heal("caster","patient",tier=1,die=8,
                                 hand_available=True,unobstructed=True,
                                 in_range=True,wound_id="first")
        self.assertEqual(result["repair_progress"],1)
        self.assertEqual(result["hp_restored"],0)
        self.assertEqual(t.hp,0)
        self.assertEqual((t.wounds[0].progress,t.wounds[1].progress),(10,0))
        self.assertGreater(t.vigor,0)
        self.assertEqual(r.vp_spent,2)
        self.assertEqual(len(e.regen_done),1)
        e.check()

    def test_g4_heal_completing_only_wound_allows_hp_surplus(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp=0;t.vigor=0;t.wounds=[Wound("only",10,9)]
        e,g,d=scene(r,t)
        e.start_turn("caster")
        out=d.cast_basic_heal("caster","patient",die=1,
                              hand_available=True,unobstructed=True,in_range=True)
        self.assertEqual((out["hp_restored"],out["repair_progress"]),(1,1))
        self.assertEqual(t.hp,1)
        self.assertEqual(t.wounds[0].progress,10)
        e.check()

    def test_g3_composite_secondary_can_heal_non_dying_wounded(self):
        t=pc();t.hp=t.hp_max-2;t.vigor-=8
        t.wounds=[Wound("open",10,0)]
        e,g,d=scene(t)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        host=g.cast_scholar_composite("caster","Basic Heal",
                                      heal_die=6,hand_available=True)
        self.assertIsNotNone(host)
        self.assertEqual(t.hp,t.hp_max-1)
        self.assertEqual(t.wounds[0].progress,0)
        self.assertTrue(any(x["kind"]=="g4_basic_heal_applied" for x in e.ledger))
        e.check()

    def test_sentry_prepared_reserve_source_selects_correct_packets(self):
        s=sentry(state="prepared_start")
        t=pc("F","target",(2,2))
        e,g,d=scene(s,t)
        r=d.apply_profile_hit("sentry","target","B06-AT-02",
                               die_face=4,vigor_die=6,confirmed_hit=True)
        self.assertEqual(r["hp_packets"],[7,2])
        self.assertEqual(r["vigor_loss"],3)
        with self.assertRaises(ValueError):
            d.apply_profile_hit("sentry","target","B06-AT-01",
                                 die_face=2,confirmed_hit=True)
        e.check()

    def test_hunter_bite_injection_requires_surviving_puncture(self):
        h=enemy_actor("B06-EN-03","hunter","enemy",
                      occupied=((4,2),(3,2)))
        t=pc("F","target",(2,2))
        e,g,d=scene(h,t)
        low=d.apply_profile_hit("hunter","target","B06-AT-04",
                                die_face=1,confirmed_hit=True)
        self.assertTrue(low["injection_eligible"])
        armored=soldier("armored",(6,2))
        # An independent legal scene of the same bite against Armor5/Pen1.
        e2,g2,d2=scene(h,armored)
        stopped=d2.apply_profile_hit("hunter","armored","B06-AT-04",
                                     die_face=1,confirmed_hit=True)
        self.assertFalse(stopped["injection_eligible"])
        e.check();e2.check()

    def test_hemotoxin_short_ticks_and_exploration_no_virtual_regen(self):
        t=soldier();t.hp=10
        e,g,d=scene(t)
        d.schedule_hemotoxin("soldier",exposure_key="thorn",actual_exposure=True,
                             resistance_total=11,wound_location_roll=3)
        d.advance_exploration(30)
        self.assertEqual((t.hp,t.vigor),(5,t.vigor_max))
        self.assertEqual(d.short_toxins[0]["left"],0)
        self.assertFalse(any(x["kind"]=="regeneration_step" for x in e.ledger))
        e.check()

    def test_six_hour_recovery_half_up_and_spent_only(self):
        t=pc();t.vigor-=10;t.vp_spent=7;t.vp_available-=7
        e,g,d=scene(t)
        d.advance_exploration(21599)
        self.assertEqual((t.vigor,t.vp_spent),(t.vigor_max-10,7))
        d.advance_exploration(1)
        self.assertEqual((t.vigor,t.vp_spent),(t.vigor_max-1,2))
        self.assertEqual(t.vp_available+t.vp_committed+t.vp_spent,t.vp_max)
        e.check()


if __name__=="__main__":
    unittest.main()
