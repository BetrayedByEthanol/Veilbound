"""B06 G3: executable deterministic spell-state / VP / host acceptance tests."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, Response, Trigger, UnresolvedDecision,
    party_actor, enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat, CoverSurface
from scripts.b06_spells_v0 import SpellState


def pc(role,level=3,ident="caster",point=(1,2),team="party"):
    return party_actor(role,level,ident,team,occupied=(point,))


def sentry(state="cold_start",ident="sentry",point=(4,2),team="enemy"):
    return enemy_actor("B06-EN-01",ident,team,start_state=state,
                       occupied=(point,))


def game(*actors,cover=(),walls=(),width=16):
    e=Encounter(list(actors),{a.id:100-i for i,a in enumerate(actors)},
                seed=303,scenario="B06-G3",policy="authored_cast")
    GridMovement(e,width=width,height=7,walls=walls)
    RangedCombat(e,cover=cover)
    g=SpellState(e)
    e.begin_round()
    return e,g


def spell_events(e,kind):
    return [v for v in e.ledger if v["kind"]==kind]


class B06G3Test(unittest.TestCase):
    def test_01_scholar_l1_l3_cast_budgets_and_standalone_t1_flame(self):
        for level in (1,2,3):
            with self.subTest(level=level):
                f=pc("F",level)
                t=pc("R",level,"target",(3,2),"enemy")
                e,g=game(f,t)
                e.start_turn("caster")
                before=f.ap_remaining
                shot=g.cast_flame("caster","target",tier=1,face=12,
                                  vigor_die=5,hand_available=True)
                self.assertEqual(shot["outcome"],"direct_hit_pending_G4")
                self.assertEqual(shot["packets_pending_g4"],
                                 {"fire_hp":2,"vigor":4})
                self.assertEqual((f.ap_remaining,f.vp_available,f.vp_spent),
                                 (before-20,6*level-2,2))
                self.assertEqual((t.hp,t.vigor),(t.hp_max,t.vigor_max))
                e.check()

    def test_02_level_three_tier_two_flame_spends_four_and_separate_packets(self):
        f=pc("F");t=pc("R",3,"target",(4,2),"enemy")
        e,g=game(f,t);e.start_turn("caster")
        shot=g.cast_flame("caster","target",tier=2,face=12,vigor_die=8,
                          hand_available=True)
        self.assertEqual(shot["packets_pending_g4"],
                         {"fire_hp":2,"vigor":2+6})
        self.assertEqual((f.vp_available,f.vp_spent,f.ap_remaining),(14,4,22))
        e.check()

    def test_03_level_one_cannot_upcast_before_any_commitment(self):
        f=pc("F",1);t=pc("R",1,"target",(3,2),"enemy")
        e,g=game(f,t);e.start_turn("caster")
        before=(f.ap_remaining,f.vp_available,len(e.ledger))
        with self.assertRaisesRegex(ValueError,"Used Tier"):
            g.cast_flame("caster","target",tier=2,face=15,vigor_die=4,
                          hand_available=True)
        self.assertEqual((f.ap_remaining,f.vp_available,len(e.ledger)),before)

    def test_04_flame_miss_spends_full_vp_but_no_damage(self):
        f=pc("F",2);t=pc("R",2,"target",(3,2),"enemy")
        e,g=game(f,t);e.start_turn("caster")
        r=g.cast_flame("caster","target",tier=1,face=1,vigor_die=8,
                       hand_available=True)
        self.assertEqual(r["outcome"],"automatic_miss")
        self.assertIsNone(r["packets_pending_g4"])
        self.assertEqual((f.ap_remaining,f.vp_spent),(16,2))
        e.check()

    def test_05_blocked_flame_refused_no_ap_or_vp(self):
        f=pc("F");t=pc("R",3,"target",(3,2),"enemy")
        e,g=game(f,t,walls=((2,2),));e.start_turn("caster")
        before=(f.ap_remaining,f.vp_spent)
        with self.assertRaisesRegex(ValueError,"physically usable"):
            g.cast_flame("caster","target",tier=1,face=20,vigor_die=1,
                          hand_available=True)
        self.assertEqual((f.ap_remaining,f.vp_spent),before)

    def test_06_flame_cover_hit_uses_own_zero_range_not_bow_close(self):
        f=pc("F");t=pc("R",3,"target",(4,2),"enemy")
        e,g=game(f,t,cover=(CoverSurface((2,2),4,(1,0)),))
        e.start_turn("caster")
        r=g.cast_flame("caster","target",tier=1,face=8,vigor_die=6,
                       hand_available=True)
        self.assertEqual((r["base_defense"],r["final_defense"]),(10,14))
        self.assertEqual(r["outcome"],"cover_impact")
        self.assertIsNone(r["packets_pending_g4"])

    def test_07_threatened_flame_no_undeclared_opportunity_shortcut(self):
        f=pc("F",3);t=pc("R",3,"target",(3,2),"enemy")
        guard=pc("A",3,"threat",(2,3),"enemy")
        e,g=game(f,t,guard);e.start_turn("caster")
        # The A melee sword is wielded; a projected cast must not get
        # an assumed free Opportunity policy.
        with self.assertRaisesRegex(UnresolvedDecision,"Threatened F casting"):
            g.cast_flame("caster","target",tier=1,face=15,vigor_die=8,
                          hand_available=True)
        self.assertEqual((f.ap_remaining,f.vp_spent),(42,0))

    def test_08_scholar_stone_heal_composite_all_levels(self):
        for level in (1,2,3):
            f=pc("F",level)
            f.hp-=2;f.vigor-=6
            e,g=game(f)
            e.start_turn("caster",regen_choice=RegenerationChoice())
            host=g.cast_scholar_composite("caster","Basic Heal",heal_tier=1,
                                          heal_die=6,hand_available=True)
            reserve=2*level
            self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),
                             (6*level-reserve-2,reserve,2))
            self.assertEqual((f.hp,f.vigor),(11,f.vigor_max-3))
            self.assertEqual(host.resistance,2)
            self.assertEqual(len(g.active("caster","Stone Skin")),1)
            self.assertEqual(spell_events(e,"g3_basic_heal_secondary_once")[0]
                             ["detail"]["vigor"],3)
            g.release("caster","Stone Skin")
            self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),
                             (6*level-2,0,2))
            e.check()

    def test_09_scholar_tier_two_healing_independent_at_l3(self):
        f=pc("F");f.hp=10;f.vigor=30
        e,g=game(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        g.cast_scholar_composite("caster","Basic Heal",heal_tier=2,
                                 heal_die=6,hand_available=True)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(8,6,4))
        self.assertEqual((f.hp,f.vigor),(11,34))
        e.check()

    def test_10_l1_does_not_prepare_stone_shelter_pair(self):
        f=pc("F",1);e,g=game(f);e.start_turn("caster")
        with self.assertRaisesRegex(ValueError,"Formula not prepared"):
            g.cast_scholar_composite("caster","Vital Shelter")
        self.assertEqual((f.ap_remaining,f.vp_available),(30,6))

    def test_11_l2_stone_shelter_subordinate_s4_and_refunds(self):
        f=pc("F",2);e,g=game(f);e.start_turn("caster")
        host=g.cast_scholar_composite("caster","Vital Shelter")
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_committed,f.vp_spent),
                         (16,5,6,1))
        self.assertEqual(g.resistance("caster","Fire"),2)
        self.assertEqual(g.prevent_vigor("caster",3),0)
        self.assertEqual(g.active("caster","Vital Shelter")[0].budget,1)
        self.assertEqual(g.prevent_vigor("caster",5),4)
        self.assertEqual(len(g.active("caster","Vital Shelter")),0)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(7,4,1))
        self.assertEqual(g.resistance("caster","Physical",other=(3,)),3)
        g.release("caster","Stone Skin")
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(11,0,1))
        e.check()

    def test_12_host_end_releases_undepleted_child_not_spent(self):
        f=pc("F",3);e,g=game(f);e.start_turn("caster")
        g.cast_scholar_composite("caster","Vital Shelter")
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(9,8,1))
        g.release("caster","Stone Skin")
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(17,0,1))
        self.assertFalse(g.effects)
        e.check()

    def test_13_stone_skin_unconscious_terminates_full_host_and_child(self):
        f=pc("F",2);e,g=game(f);e.start_turn("caster")
        g.cast_scholar_composite("caster","Vital Shelter")
        f.hp=0
        g.sync_consciousness("caster")
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(11,0,1))
        self.assertFalse(g.effects)
        e.check()

    def test_14_composite_interrupted_after_ap_no_vp_or_host(self):
        f=pc("F",1);e,g=game(f);e.start_turn("caster")
        def suppress(event):
            event.actors["caster"].hp=0
        out=g.cast_scholar_composite("caster","Basic Heal",heal_tier=1,
                                    heal_die=1,hand_available=True,
                                    on_committed=suppress)
        self.assertIsNone(out)
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_committed,f.vp_spent),
                         (10,6,0,0))
        self.assertFalse(g.effects)
        e.check()

    def test_15_unauthorized_composite_and_reverse_banned(self):
        f=pc("F");e,g=game(f);e.start_turn("caster")
        for partner in ("Conjure Flame","Phantom Sound","Minor Telekinesis"):
            with self.subTest(partner=partner):
                with self.assertRaises(UnresolvedDecision):
                    g.cast_scholar_composite("caster",partner)
        self.assertEqual((f.ap_remaining,f.vp_available),(42,18))

    def test_16_sentry_cold_cast_cost_and_normal_sword_next_turn(self):
        s=sentry();e,g=game(s);e.start_turn("sentry")
        self.assertEqual(g.sentry_profile("sentry"),"B06-AT-01")
        v=g.cast_sentry_reserve("sentry")
        self.assertIsNotNone(v)
        self.assertEqual((s.ap_remaining,s.vp_available,s.vp_committed,
                          s.vp_spent),(12,3,3,0))
        self.assertEqual(g.sentry_profile("sentry"),"B06-AT-02")
        with self.assertRaisesRegex(ValueError,"Not enough AP"):
            e.declare_sequence("sentry","sentry",("B06-AT-02",),("take_hit",))
        e.check()

    def test_17_prepared_sentry_loads_exact_reserve_without_second_debit(self):
        s=sentry("prepared_start");e,g=game(s);e.start_turn("sentry")
        self.assertEqual(g.sentry_profile("sentry"),"B06-AT-02")
        self.assertEqual((s.vp_available,s.vp_committed,s.vp_spent),(3,3,0))
        self.assertEqual(list(g.effects)[0],("sentry","B06-FIRE-RESERVE-01"))
        self.assertEqual(spell_events(e,"vp_transition"),[])
        e.check()

    def test_18_sentry_disarm_releases_three_no_refund_of_four(self):
        s=sentry("prepared_start");e,g=game(s);e.start_turn("sentry")
        e.g2.wielded["sentry"].discard("Sword")
        g.sword_no_longer_wielded("sentry")
        self.assertEqual(g.sentry_profile("sentry"),"B06-AT-01")
        self.assertEqual((s.vp_available,s.vp_committed,s.vp_spent),(6,0,0))
        self.assertNotIn("B06-FIRE-RESERVE-01",s.maintained)
        e.check()

    def test_19_sentry_interrupted_cold_cast_keeps_ap_no_vp(self):
        s=sentry();e,g=game(s);e.start_turn("sentry")
        def disarm(event):
            event.g2.wielded["sentry"].discard("Sword")
        self.assertIsNone(g.cast_sentry_reserve("sentry",on_committed=disarm))
        self.assertEqual((s.ap_remaining,s.vp_available,s.vp_committed),
                         (12,6,0))
        self.assertEqual(g.sentry_profile("sentry"),"B06-AT-01")
        e.check()

    def test_20_guided_low_priest_chosen_and_nonchosen_cost(self):
        for chosen in (True,False):
            r=pc("R",3);e,g=game(r);e.start_turn("caster")
            v=g.cast_guided("caster",chosen=chosen)
            cost=1 if chosen else 2
            self.assertEqual((r.vp_available,r.vp_committed,r.vp_spent),
                             (6-cost,cost,0))
            self.assertEqual(v.chosen,chosen)
            self.assertEqual(g.regen_throughput("caster"),1)
            g.release("caster","Guided Regeneration")
            self.assertEqual((r.vp_available,r.vp_committed,r.vp_spent),(6,0,0))
            e.check()

    def test_21_guided_fixed_spends_two_without_active_rite(self):
        r=pc("R",2);e,g=game(r);e.start_turn("caster")
        v=g.cast_guided("caster",mode="fixed")
        self.assertEqual((r.vp_available,r.vp_committed,r.vp_spent),(2,0,2))
        self.assertFalse(v.chosen)
        self.assertEqual(v.expiry_round,11)
        self.assertEqual(g.regen_throughput("caster"),1)
        e.check()

    def test_22_guided_cannot_be_fully_duplicated_without_break(self):
        r=pc("R",3);e,g=game(r);e.start_turn("caster")
        g.cast_guided("caster",chosen=True)
        before=(r.ap_remaining,r.vp_available,r.vp_committed)
        with self.assertRaisesRegex(ValueError,"Cannot stack"):
            g.cast_guided("caster",chosen=True)
        self.assertEqual((r.ap_remaining,r.vp_available,r.vp_committed),before)

    def test_23_guided_integrates_with_one_genuine_g0_regen_step(self):
        r=pc("R",3);e,g=game(r);e.start_turn("caster")
        g.cast_guided("caster",chosen=True);e.end_turn()
        r.hp=4
        e.begin_round()
        e.start_turn("caster",regen_choice=RegenerationChoice(hp=7))
        self.assertEqual(r.hp,11)
        self.assertEqual(r.vigor,r.vigor_max-7)
        self.assertEqual(g.regen_throughput("caster"),1)
        self.assertEqual(len([x for x in e.ledger
                              if x["kind"]=="regeneration_step"]),2)
        e.check()

    def test_24_guided_unconscious_maintained_does_not_end(self):
        r=pc("R",3);e,g=game(r);e.start_turn("caster")
        g.cast_guided("caster",chosen=True)
        r.hp=0
        g.sync_consciousness("caster")
        self.assertEqual((r.vp_committed,len(g.active("caster","Guided Regeneration"))),(1,1))
        e.check()

    def test_25_a_b_proxy_cannot_gain_unrecorded_prepared_repertoire(self):
        a=pc("A",3);e,g=game(a);e.start_turn("caster")
        with self.assertRaises(UnresolvedDecision):
            g.cast_guided("caster")
        self.assertEqual((a.ap_remaining,a.vp_available),(42,6))

    def test_26_shelter_zero_current_vigor_does_not_spend_budget(self):
        f=pc("F",2);e,g=game(f);e.start_turn("caster")
        g.cast_scholar_composite("caster","Vital Shelter")
        f.vigor=0
        self.assertEqual(g.prevent_vigor("caster",8),8)
        self.assertEqual(g.active("caster","Vital Shelter")[0].budget,4)
        e.check()

    def test_28_standalone_stone_skin_l1_to_l3_reserves_one_third(self):
        for level in (1,2,3):
            with self.subTest(level=level):
                f=pc("F",level)
                e,g=game(f);e.start_turn("caster")
                effect=g.cast_stone("caster")
                self.assertEqual(effect.resistance,2)
                self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),
                                 (4*level,2*level,0))
                self.assertEqual(f.ap_remaining,f.ap_total-20)
                g.release("caster","Stone Skin")
                self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),
                                 (6*level,0,0))
                e.check()

    def test_29_stone_skin_reaction_only_after_actual_g0_commit(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        trigger=Trigger("incoming-stone","attacker","caster")
        response=g.prepare_reactive_stone("caster",trigger,perceptible=True)
        before_ap=f.ap_remaining
        ok=e.response_window(
            trigger,on_interception=lambda event,tr,r:None,
            spontaneous=(response,),
            on_spontaneous=lambda event,tr,r:g.resolve_reactive_stone(
                "caster",tr,r))
        self.assertTrue(ok)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(12,6,0))
        self.assertEqual(f.ap_remaining,before_ap)
        self.assertFalse(f.reaction_available)
        self.assertEqual(g.resistance("caster","Fire"),2)
        self.assertEqual(spell_events(e,"g3_stone_reacted")[0]["detail"]["ap_debt"],0)
        with self.assertRaisesRegex(ValueError,"Reaction not available"):
            g.prepare_reactive_stone(
                "caster",Trigger("next-threat","attacker","caster"),
                perceptible=True)
        e.check()

    def test_30_stone_reaction_preempted_by_interception_no_vp_reaction(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        e.start_turn("attacker")
        e.reserve("attacker","incoming-stone","cancel",action_kind="physical")
        e.end_turn()
        trigger=Trigger("incoming-stone","attacker","caster")
        response=g.prepare_reactive_stone("caster",trigger,perceptible=True)
        on_spontaneous=lambda event,tr,r:g.resolve_reactive_stone("caster",tr,r)
        result=e.response_window(
            trigger,on_interception=lambda event,tr,r:setattr(tr,"legal",False),
            spontaneous=(response,),on_spontaneous=on_spontaneous)
        self.assertFalse(result)
        self.assertTrue(f.reaction_available)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(g.effects)
        e.check()

    def test_31_reactive_stone_cannot_be_cast_using_unguarded_direct_call(self):
        f=pc("F");e,g=game(f)
        trig=Trigger("false","attacker","caster")
        with self.assertRaisesRegex(ValueError,"No unused G0-committed"):
            g.resolve_reactive_stone(
                "caster",trig,Response("caster","reaction","g3:reactive_stone"))
        self.assertEqual(f.vp_committed,0)
        e.check()

    def test_32_primary_basic_heal_self_does_not_debit_vigor_throughput(self):
        f=pc("F",3)
        f.hp=7;f.vigor=20
        e,g=game(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        result=g.cast_self_basic_heal("caster",tier=2,die=7,
                                      hand_available=True)
        self.assertEqual(result,{"hp_restored":2,"vigor_restored":9,"spent_vp":4})
        self.assertEqual((f.hp,f.vigor),(9,29))
        self.assertEqual((f.vp_available,f.vp_spent,f.ap_remaining),(14,4,22))
        e.check()

    def test_33_low_priest_bow_does_not_automatically_free_heal_hand(self):
        r=pc("R",3)
        r.hp=10
        e,g=game(r);e.start_turn("caster",regen_choice=RegenerationChoice())
        before=(r.ap_remaining,r.vp_available)
        with self.assertRaisesRegex(ValueError,"available hand"):
            g.cast_self_basic_heal("caster",tier=1,die=6)
        self.assertEqual((r.ap_remaining,r.vp_available),before)
        heal=g.cast_self_basic_heal("caster",tier=1,die=6,
                                    hand_available=True)
        self.assertEqual(heal["hp_restored"],2)
        self.assertEqual((r.ap_remaining,r.vp_available,r.vp_spent),(12,4,2))
        e.check()

    def test_34_one_active_stone_skin_instance_cannot_recast(self):
        f=pc("F");e,g=game(f);e.start_turn("caster")
        g.cast_stone("caster")
        before=(f.ap_remaining,f.vp_available,f.vp_committed,len(e.ledger))
        with self.assertRaisesRegex(ValueError,"One Stone Skin"):
            g.cast_stone("caster")
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_committed,
                          len(e.ledger)),before)
        e.check()

    def test_35_standalone_stone_aborted_after_commit_preserves_vp(self):
        f=pc("F");e,g=game(f);e.start_turn("caster")
        def lose_consciousness(event):event.actors["caster"].hp=0
        outcome=g.cast_stone("caster",on_committed=lose_consciousness)
        self.assertIsNone(outcome)
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_committed),(22,18,0))
        self.assertFalse(g.effects)
        e.check()

    def test_27_only_legal_flame_vp_after_activation_not_rejected_line(self):
        f=pc("F");t=pc("R",3,"target",(3,2),"enemy")
        e,g=game(f,t);e.start_turn("caster")
        def block_after_commit(event):
            event.g1.walls=frozenset({(2,2)})
        r=g.cast_flame("caster","target",tier=1,face=12,vigor_die=4,
                       hand_available=True,on_committed=block_after_commit)
        self.assertEqual(r["outcome"],"interrupted_before_launch")
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_spent),(22,18,0))
        e.check()


if __name__=="__main__":
    unittest.main()
