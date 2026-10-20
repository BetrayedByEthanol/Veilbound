"""Deterministic acceptance for B06 G4 injury and recovery integration."""
import unittest
from dataclasses import replace
from math import ceil

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


def scene(*actors,spatial=False,walls=()):
    e=Encounter(list(actors),{a.id:100-i for i,a in enumerate(actors)},
                seed=404,scenario="B06-G4",policy="explicit_verified_delivery")
    if spatial:
        GridMovement(e,width=16,height=7,walls=walls)
        RangedCombat(e)
    g3=SpellState(e)
    g4=DamageState(e)
    e.begin_round()
    return e,g3,g4


def synthetic_vc(actor, raw):
    """Test-only formula witness; NOT an authored alternative F/R build."""
    fields=dict(actor.source.abilities)
    fields["Veil Control"]=raw
    actor.source=replace(actor.source,abilities=tuple(sorted(fields.items())))


class G4IntegrationTests(unittest.TestCase):
    def test_physical_armor_and_critical_dice_on_primary_only(self):
        s=soldier(); t=sentry(point=(4,2))
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

    def test_real_g3_flame_hit_is_applied_synchronously_and_once(self):
        f=pc();t=pc("R","target",(3,2),"enemy")
        e,g,d=scene(f,t,spatial=True)
        e.start_turn("caster")
        shot=g.cast_flame("caster","target",tier=1,face=12,
                          vigor_die=5,hand_available=True)
        self.assertEqual(shot["outcome"],"direct_hit_resolved_G4")
        self.assertEqual((shot["g4_damage"]["hp_loss"],
                          shot["g4_damage"]["vigor_loss"]),(2,4))
        self.assertEqual((t.hp,t.vigor),(t.hp_max-2,t.vigor_max-4))
        launch=next(v for v in e.ledger if v["kind"]=="g3_flame_launched")
        impact=next(v for v in e.ledger if v["kind"]=="g4_damage_applied")
        # The actual Vigor packet's G3 Shelter accounting is logged
        # within synchronous damage resolution, never a separate turn/step.
        intervening=[v["kind"] for v in e.ledger[
            launch["index"]+1:impact["index"]]]
        self.assertEqual(intervening,["g3_shelter_packet"])
        with self.assertRaisesRegex(ValueError,"consumed"):
            d.apply_flame("caster","target",ledger_index=launch["index"])
        e.end_turn()
        e.start_turn("target",regen_choice=RegenerationChoice(hp=2))
        self.assertEqual(t.hp,t.hp_max)
        self.assertEqual(t.vigor,t.vigor_max-6)
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


    def test_flame_cannot_consume_a_historical_g3_only_launch(self):
        f=pc();t=pc("R","target",(3,2),"enemy")
        e=Encounter([f,t],{"caster":100,"target":99},
                    seed=405,scenario="late-G4-install",policy="source")
        GridMovement(e,width=16,height=7)
        RangedCombat(e)
        g=SpellState(e)
        e.begin_round()
        e.start_turn("caster")
        shot=g.cast_flame("caster","target",tier=1,face=12,
                          vigor_die=5,hand_available=True)
        self.assertEqual(shot["outcome"],"direct_hit_pending_G4")
        launch=e.ledger[-1]["index"]
        e.end_turn()
        d=DamageState(e)
        with self.assertRaisesRegex(ValueError,"original launch"):
            d.apply_flame("caster","target",ledger_index=launch)
        self.assertEqual((t.hp,t.vigor),(t.hp_max,t.vigor_max))
        e.check()

    def test_flame_wound_is_preflighted_then_resolved_before_next_step(self):
        f=pc();t=pc("R","target",(3,2),"enemy")
        t.hp=1
        e,g,d=scene(f,t,spatial=True)
        e.start_turn("caster")
        with self.assertRaisesRegex(UnresolvedDecision,"wound-location"):
            g.cast_flame("caster","target",tier=1,face=12,
                         vigor_die=5,hand_available=True)
        self.assertEqual((t.hp,f.vp_spent),(1,0))
        # An already-committed attempt lost AP but neither launched nor paid
        # VP. Supply the actual d20 for a fresh legal declared cast.
        shot=g.cast_flame("caster","target",tier=1,face=12,
                          vigor_die=5,hand_available=True,wound_location_roll=13)
        self.assertEqual(shot["outcome"],"direct_hit_resolved_G4")
        self.assertEqual((t.hp,t.wounds[0].location),(-1,"Arm"))
        self.assertEqual(len(t.wounds),1)
        self.assertTrue(any(v["kind"]=="g4_wound_created" for v in e.ledger))
        e.check()

    def test_carried_g4_wound_ids_remain_unique_with_new_encounter_damage(self):
        t=sentry();t.hp=1
        t.wounds=[Wound("G4-W0001",10,9),Wound("G4-W0007",20,0)]
        other=pc("F","other",(1,2))
        other.wounds=[Wound("G4-W0020",10,0)]
        e,g,d=scene(t,other)
        d.apply_damage("sentry",(DamagePacket("hp","Fire",2),),
                       event_key="new-hit",cause="confirmed",
                       wound_location_roll=16)
        self.assertEqual(t.wounds[-1].ident,"G4-W0021")
        self.assertEqual(len({w.ident for w in t.wounds}),3)
        restored=d.resolve_heal("sentry",contribution="Primary",
                                vigor_amount=0,wound_id="G4-W0021")
        self.assertEqual(restored["repair_progress"],2)
        self.assertEqual([w.progress for w in t.wounds],[9,0,2])
        e.start_turn("sentry",regen_choice=RegenerationChoice(
            cancel_dying_loss=True,repair=3))
        self.assertEqual([w.progress for w in t.wounds],[10,2,2])
        e.check()

    def test_heal_committed_response_requires_live_delivery_policy(self):
        r=pc("R");t=pc("F","patient",(2,2))
        e,g,d=scene(r,t)
        e.start_turn("caster")
        with self.assertRaisesRegex(UnresolvedDecision,"live Basic Heal delivery_check"):
            d.cast_basic_heal("caster","patient",die=1,
                              hand_available=True,in_range=True,
                              unobstructed=True,on_committed=lambda x:None)
        self.assertEqual((r.ap_remaining,r.vp_spent),(42,0))
        e.check()

    def test_heal_committed_response_removes_caster_hand_before_vp(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp-=2;t.vigor-=8
        e,g,d=scene(r,t)
        e.start_turn("caster")
        hand={"free":True}
        def disarm(_encounter):
            hand["free"]=False
        check=lambda _e,_c,_r:(hand["free"],True,True)
        result=d.cast_basic_heal("caster","patient",die=8,
                                 hand_available=True,in_range=True,unobstructed=True,
                                 on_committed=disarm,delivery_check=check,
                                 restoration_check=lambda _e,_c,_r:())
        self.assertIsNone(result)
        self.assertEqual((r.ap_remaining,r.vp_spent),(12,0))
        self.assertEqual((t.hp,t.vigor),(t.hp_max-2,t.vigor_max-8))
        self.assertEqual(
            [ev["detail"]["cause"] for ev in e.ledger
             if ev["kind"]=="g4_heal_interrupted"],["hand_unavailable"])
        e.check()

    def test_heal_committed_response_moving_target_out_of_range_cancels(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp-=2;t.vigor-=8
        e,g,d=scene(r,t,spatial=True)
        e.start_turn("caster")
        def move_after_commit(_encounter):
            t.occupied=((7,2),)
        result=d.cast_basic_heal(
            "caster","patient",die=1,hand_available=True,in_range=True,
            unobstructed=True,on_committed=move_after_commit,
            delivery_check=lambda _e,_c,_r:(True,True,True),
            restoration_check=lambda _e,_c,_r:())
        self.assertIsNone(result)
        self.assertEqual((r.ap_remaining,r.vp_spent,t.hp),
                         (12,0,t.hp_max-2))
        self.assertTrue(any(v["kind"]=="g4_heal_interrupted" and
                            v["detail"]["cause"]=="delivery_out_of_range"
                            for v in e.ledger))
        e.check()

    def test_heal_committed_response_new_wall_obstruction_cancels(self):
        r=pc("R");t=pc("F","patient",(1,4))
        t.hp-=2
        e,g,d=scene(r,t,spatial=True,walls=((2,3),))
        e.start_turn("caster")
        def redirect(_encounter):
            t.occupied=((3,3),)
        out=d.cast_basic_heal(
            "caster","patient",die=1,hand_available=True,in_range=True,
            unobstructed=True,on_committed=redirect,
            delivery_check=lambda _e,_c,_r:(True,True,True),
            restoration_check=lambda _e,_c,_r:())
        self.assertIsNone(out)
        self.assertEqual((r.ap_remaining,r.vp_spent,t.hp),(12,0,t.hp_max-2))
        self.assertTrue(any(v["kind"]=="g4_heal_interrupted" and
                            v["detail"]["cause"]=="delivery_obstructed"
                            for v in e.ledger))
        e.check()

    def test_heal_unchanged_delivery_after_response_still_applies_once(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp-=2;t.vigor-=8
        e,g,d=scene(r,t,spatial=True)
        e.start_turn("caster")
        out=d.cast_basic_heal(
            "caster","patient",die=1,hand_available=True,in_range=True,
            unobstructed=True,on_committed=lambda _e:None,
            delivery_check=lambda _e,_c,_r:(True,True,True),
            restoration_check=lambda _e,_c,_r:())
        self.assertEqual((out["hp_restored"],out["spent_vp"]),(2,2))
        self.assertEqual((r.ap_remaining,r.vp_spent,t.hp),
                         (12,2,t.hp_max))
        e.check()



    def test_g41_survival_only_debits_one_throughput_and_one_vigor(self):
        t=sentry();t.hp=0;t.vigor=1;t.regen=1
        t.wounds=[Wound("carried",10,2)]
        e,g,d=scene(t)
        e.start_turn("sentry",regen_choice=RegenerationChoice(
            cancel_dying_loss=True))
        self.assertEqual((t.hp,t.vigor,t.wounds[0].progress),(0,0,2))
        log=next(v for v in e.ledger if v["kind"]=="regeneration_step")
        self.assertEqual((log["detail"]["throughput_spent"],
                          log["detail"]["repair_points"],
                          log["detail"]["hp_restored"]),(1,0,0))
        self.assertEqual(len(e.regen_done),1)
        e.check()
        z=sentry();z.hp=0;z.vigor=0;z.regen=1
        e2,g2,d2=scene(z)
        e2.start_turn("sentry")
        self.assertEqual((z.hp,z.vigor),(-1,0))
        e2.check()

    def test_g41_primary_vc_source_formula_tier_two_and_caps(self):
        r=pc("R");synthetic_vc(r,3)
        t=pc("F","patient",(2,2));t.hp-=2;t.vigor=0
        e,g,d=scene(r,t)
        e.start_turn("caster")
        out=d.cast_basic_heal("caster","patient",tier=2,die=8,
                              hand_available=True,in_range=True,unobstructed=True)
        self.assertEqual((out["hp_restored"],out["vigor_restored"],out["spent_vp"]),
                         (2,4+ceil(8*2/3)+3,4))
        self.assertEqual((t.hp,t.vigor),(t.hp_max,13))
        self.assertEqual((r.ap_remaining,r.vp_spent),(12,4))
        self.assertEqual(e.regen_done,{"caster"})
        e.check()

    def test_g41_negative_vc_contributes_zero_to_self_primary(self):
        f=pc();synthetic_vc(f,-4);f.hp-=3;f.vigor=0
        e,g,d=scene(f)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        out=g.cast_self_basic_heal("caster",tier=1,die=8,hand_available=True)
        self.assertEqual(out["vigor_restored"],4+ceil(8/3))
        self.assertEqual((f.vp_spent,f.hp),(2,f.hp_max-1))
        e.check()

    def test_g41_self_primary_and_composite_secondary_use_nonzero_vc(self):
        f=pc();synthetic_vc(f,4);f.hp-=4;f.vigor=0
        e,g,d=scene(f)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        primary=g.cast_self_basic_heal("caster",tier=1,die=8,
                                      hand_available=True)
        self.assertEqual(primary["vigor_restored"],4+ceil(8/3)+4)
        secondary=g.cast_scholar_composite("caster","Basic Heal",
                         heal_tier=1,heal_die=6,hand_available=True)
        self.assertEqual((f.vigor,f.hp),(4+ceil(8/3)+4+2+ceil(6/6)+4,
                                         f.hp_max-1))
        self.assertEqual((f.vp_spent,f.vp_committed),(4,6))
        self.assertEqual(sum(v["kind"]=="g4_basic_heal_applied" for v in e.ledger),2)
        e.check()

    def test_g41_vigor_only_healing_block_preserves_direct_hp(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp-=2;t.vigor=0
        e,g,d=scene(r,t);e.start_turn("caster")
        out=d.cast_basic_heal("caster","patient",die=8,hand_available=True,
                              in_range=True,unobstructed=True,
                              blocked_restoration=("vigor",))
        self.assertEqual((out["hp_restored"],out["vigor_restored"]),(2,0))
        self.assertEqual((r.vp_spent,t.hp,t.vigor),(2,t.hp_max,0))
        self.assertEqual(e.regen_done,{"caster"})
        e.check()

    def test_g41_direct_hp_block_does_not_prevent_dying_repair(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp=0;t.vigor=0;t.wounds=[Wound("only",10,9)]
        e,g,d=scene(r,t);e.start_turn("caster")
        out=d.cast_basic_heal("caster","patient",die=1,hand_available=True,
                              in_range=True,unobstructed=True,
                              blocked_restoration=("hp",))
        self.assertEqual((out["repair_progress"],out["hp_restored"]),(1,0))
        self.assertEqual(t.hp,0)
        self.assertEqual(t.wounds[0].progress,10)
        self.assertGreater(t.vigor,0)
        e.check()

    def test_g41_repair_block_does_not_prevent_external_vigor(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp=0;t.vigor=0;t.wounds=[Wound("only",10,9)]
        e,g,d=scene(r,t);e.start_turn("caster")
        out=d.cast_basic_heal("caster","patient",die=1,hand_available=True,
                              in_range=True,unobstructed=True,
                              blocked_restoration=("repair",))
        self.assertEqual((out["repair_progress"],out["hp_restored"]),(0,0))
        self.assertEqual(t.wounds[0].progress,9)
        self.assertGreater(t.vigor,0)
        self.assertEqual(r.vp_spent,2)
        e.check()

    def test_g41_g3_self_and_composite_respect_vigor_only_block(self):
        f=pc();f.hp-=4;f.vigor=0
        e,g,d=scene(f)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        first=g.cast_self_basic_heal("caster",die=8,hand_available=True,
                                    blocked_restoration=("vigor",))
        self.assertEqual((first["hp_restored"],first["vigor_restored"]),(2,0))
        host=g.cast_scholar_composite("caster","Basic Heal",heal_die=6,
                hand_available=True,blocked_restoration=("vigor",))
        self.assertIsNotNone(host)
        self.assertEqual((f.hp,f.vigor),(f.hp_max-1,0))
        self.assertEqual((f.vp_spent,f.vp_committed),(4,6))
        e.check()

    def test_g41_g3_rejects_unknown_blocks_before_composite_host(self):
        f=pc();f.hp-=2;f.vigor-=8
        e,g,d=scene(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        before=(f.ap_remaining,f.vp_available)
        with self.assertRaisesRegex(UnresolvedDecision,"Unknown or repeated"):
            g.cast_scholar_composite("caster","Basic Heal",heal_die=1,
                hand_available=True,blocked_restoration=("unresolved_magic",))
        self.assertEqual((f.ap_remaining,f.vp_available),before)
        self.assertFalse(g.effects)
        e.check()

    def test_g41_unknown_healing_restriction_rejects_before_ap(self):
        r=pc("R");t=pc("F","patient",(2,2))
        e,g,d=scene(r,t);e.start_turn("caster")
        with self.assertRaisesRegex(UnresolvedDecision,"Unknown or repeated"):
            d.cast_basic_heal("caster","patient",die=1,hand_available=True,
                              in_range=True,unobstructed=True,
                              blocked_restoration=("all_healing",))
        self.assertEqual((r.ap_remaining,r.vp_spent),(42,0))
        with self.assertRaisesRegex(UnresolvedDecision,"live restoration_check"):
            d.cast_basic_heal("caster","patient",die=1,hand_available=True,
                              in_range=True,unobstructed=True,
                              blocked_restoration=("vigor",),
                              on_committed=lambda _e:None,
                              delivery_check=lambda _e,_c,_r:(True,True,True))
        self.assertEqual((r.ap_remaining,r.vp_spent),(42,0))
        e.check()

    def test_g41_committed_caster_moves_beyond_healing_range(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp-=2
        e,g,d=scene(r,t,spatial=True);e.start_turn("caster")
        def reposition(_e):
            r.occupied=((8,2),)
        out=d.cast_basic_heal("caster","patient",die=1,hand_available=True,
                     in_range=True,unobstructed=True,
                     on_committed=reposition,
                     delivery_check=lambda _e,_c,_r:(True,True,True),
            restoration_check=lambda _e,_c,_r:())
        self.assertIsNone(out)
        self.assertEqual((r.ap_remaining,r.vp_spent,t.hp),(12,0,t.hp_max-2))
        self.assertTrue(any(v["kind"]=="g4_heal_interrupted" and
                            v["detail"]["cause"]=="delivery_out_of_range"
                            for v in e.ledger))
        e.check()

    def test_g41_new_ward_after_ap_blocks_only_current_vigor_component(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp-=2;t.vigor=0
        e,g,d=scene(r,t,spatial=True);e.start_turn("caster")
        calls=[]
        def ward_created(event):
            event.actors["patient"].conditions.append("vigor")
        def live_blocks(event,_caster,recipient):
            current=tuple(event.actors[recipient].conditions)
            calls.append(current)
            return current
        out=d.cast_basic_heal(
            "caster","patient",die=8,hand_available=True,in_range=True,
            unobstructed=True,on_committed=ward_created,
            delivery_check=lambda _e,_c,_r:(True,True,True),
            restoration_check=live_blocks)
        self.assertEqual(calls,[(),("vigor",)])
        self.assertEqual((out["hp_restored"],out["vigor_restored"],
                          out["spent_vp"]),(2,0,2))
        self.assertEqual((t.hp,t.vigor,r.ap_remaining,r.vp_spent),
                         (t.hp_max,0,12,2))
        applied=[v["detail"] for v in e.ledger
                 if v["kind"]=="g4_basic_heal_applied"]
        self.assertEqual(applied[-1]["blocked_components"],["vigor"])
        e.check()

    def test_g41_empty_declaration_without_live_ward_checker_is_unresolved(self):
        r=pc("R");t=pc("F","patient",(2,2))
        e,g,d=scene(r,t);e.start_turn("caster")
        before=(r.ap_remaining,r.vp_spent,t.hp,t.vigor)
        with self.assertRaisesRegex(UnresolvedDecision,"live restoration_check"):
            d.cast_basic_heal(
                "caster","patient",die=1,hand_available=True,in_range=True,
                unobstructed=True,on_committed=lambda ev:
                    ev.actors["patient"].conditions.append("vigor"),
                delivery_check=lambda _e,_c,_r:(True,True,True))
        self.assertEqual((r.ap_remaining,r.vp_spent,t.hp,t.vigor),before)
        self.assertFalse(t.conditions)
        e.check()

    def test_g41_self_new_ward_after_ap_blocks_vigor_only(self):
        f=pc();f.hp-=2;f.vigor=0
        e,g,d=scene(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        checks=[]
        def ward_created(ev):
            ev.actors["caster"].conditions.append("vigor")
        def check(ev,_c,_r):
            v=tuple(ev.actors["caster"].conditions)
            checks.append(v)
            return v
        out=g.cast_self_basic_heal(
            "caster",die=8,hand_available=True,
            on_committed=ward_created,
            hand_check=lambda _e,_c:True,
            restoration_check=check)
        self.assertEqual(checks,[(),("vigor",)])
        self.assertEqual((out["hp_restored"],out["vigor_restored"],
                          out["spent_vp"]),(2,0,2))
        self.assertEqual((f.hp,f.vigor,f.vp_spent),
                         (f.hp_max,0,2))
        e.check()

    def test_g41_composite_new_ward_after_ap_blocks_secondary_vigor(self):
        f=pc();f.hp-=2;f.vigor=0
        e,g,d=scene(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        checks=[]
        def ward_created(ev):
            ev.actors["caster"].conditions.append("vigor")
        def check(ev,_c,_r):
            v=tuple(ev.actors["caster"].conditions)
            checks.append(v)
            return v
        host=g.cast_scholar_composite(
            "caster","Basic Heal",heal_die=6,hand_available=True,
            on_committed=ward_created,hand_check=lambda _e,_c:True,
            restoration_check=check)
        self.assertIsNotNone(host)
        self.assertEqual(checks,[(),("vigor",)])
        self.assertEqual((f.hp,f.vigor,f.vp_spent,f.vp_committed),
                         (f.hp_max-1,0,2,6))
        applied=[v["detail"] for v in e.ledger
                 if v["kind"]=="g4_basic_heal_applied"]
        self.assertEqual(applied[-1]["blocked_components"],["vigor"])
        e.check()

    def test_g41_response_removing_dynamic_block_restores_now_eligible_vigor(self):
        r=pc("R");t=pc("F","patient",(2,2))
        t.hp-=2;t.vigor=0;t.conditions.append("vigor")
        e,g,d=scene(r,t);e.start_turn("caster")
        seen=[]
        def clear_ward(ev):
            ev.actors["patient"].conditions.remove("vigor")
        def check(ev,_c,_r):
            v=tuple(ev.actors["patient"].conditions)
            seen.append(v)
            return v
        out=d.cast_basic_heal(
            "caster","patient",die=8,hand_available=True,in_range=True,
            unobstructed=True,on_committed=clear_ward,
            delivery_check=lambda _e,_c,_r:(True,True,True),
            restoration_check=check)
        self.assertEqual(seen,[("vigor",),()])
        self.assertEqual((out["hp_restored"],out["vigor_restored"]),(2,7))
        self.assertEqual(t.vigor,7)
        e.check()

    def test_g41_non_dying_named_wound_allocations_and_no_double_regen(self):
        t=sentry();t.hp=t.hp_max-3;t.vigor=6
        t.wounds=[Wound("first",10,1),Wound("second",20,1)]
        e,g,d=scene(t)
        e.start_turn("sentry",regen_choice=RegenerationChoice(
            hp=1,repair=2,wound_allocations=(("second",1),("first",1))))
        self.assertEqual((t.hp,t.vigor),(t.hp_max-2,3))
        self.assertEqual([w.progress for w in t.wounds],[2,2])
        with self.assertRaisesRegex(ValueError,"No resolved open turn|already"):
            e.start_turn("sentry",regen_choice=RegenerationChoice(hp=1))
        self.assertEqual(len([v for v in e.ledger if v["kind"]=="regeneration_step"]),1)
        e.check()



if __name__=="__main__":
    unittest.main()
