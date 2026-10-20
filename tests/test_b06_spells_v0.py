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
                                    on_committed=suppress,
                                    hand_check=lambda _e,_c:True)
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
        with self.assertRaisesRegex(ValueError,"Unwielded sword"):
            g.sentry_profile("sentry")
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
        with self.assertRaisesRegex(ValueError,"Unwielded sword"):
            g.sentry_profile("sentry")
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
        # Validate duplicate Rite exclusion at the start of a fresh turn,
        # where AP is sufficient, instead of masking it with AP exhaustion.
        e.end_turn()
        e.begin_round()
        e.start_turn("caster")
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
        self.assertFalse(g.reactive_stone_claims)
        self.assertEqual(len(spell_events(e,"g3_reactive_claim_expired")),1)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(g.effects)
        e.check()

    def test_31_reactive_stone_cannot_be_cast_using_unguarded_direct_call(self):
        f=pc("F");e,g=game(f)
        trig=Trigger("false","attacker","caster")
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
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

    def test_36_held_renewal_has_real_chosen_host_only_at_l3(self):
        for level in (1,2,3):
            r=pc("R",level);e,g=game(r);e.start_turn("caster")
            self.assertFalse(g.exaltation_eligibility("caster","EX-LR-01"))
            g.cast_guided("caster",chosen=True)
            self.assertEqual(g.exaltation_eligibility("caster","EX-LR-01"),
                             level==3)
            self.assertFalse(g.exaltation_eligibility("caster","EX-LP-01"))
            g.release("caster","Guided Regeneration")
            self.assertFalse(g.exaltation_eligibility("caster","EX-LR-01"))
            e.check()

    def test_37_nonchosen_rite_and_fixed_spell_never_anchor_exaltation(self):
        for mode,chosen in (("maintained",False),("fixed",False)):
            r=pc("R",3);e,g=game(r);e.start_turn("caster")
            g.cast_guided("caster",mode=mode,chosen=chosen)
            self.assertFalse(g.exaltation_eligibility("caster","EX-LR-01"))
            self.assertFalse(g.exaltation_eligibility("caster","EX-LP-01"))
            self.assertEqual(len([x for x in e.ledger
                                  if x["kind"]=="vp_transition" and
                                  x["detail"]["label"].startswith("g3:exaltation")]),0)
            e.check()

    def test_38_maintained_guided_ends_on_actual_caster_death(self):
        r=pc("R",3);e,g=game(r);e.start_turn("caster")
        g.cast_guided("caster",chosen=True)
        r.hp=-r.hp_max
        r.dead=True
        g.sync_consciousness("caster")
        self.assertFalse(g.effects)
        self.assertEqual((r.vp_available,r.vp_committed,r.vp_spent),(6,0,0))
        e.check()

    def test_39_fixed_guided_expires_before_regen_step_at_round_eleven(self):
        r=pc("R",2);e,g=game(r);e.start_turn("caster")
        g.cast_guided("caster",mode="fixed")
        e.end_turn()
        for nr in range(2,12):
            e.begin_round()
            self.assertEqual(e.round,nr)
            self.assertEqual(bool(g.active("caster","Guided Regeneration")),nr<11)
            if nr<11:
                e.start_turn("caster")
                e.end_turn()
        self.assertEqual((r.vp_available,r.vp_committed,r.vp_spent),(2,0,2))
        self.assertEqual(g.regen_throughput("caster"),0)
        e.check()

    def test_40_stone_composite_not_recasteable_while_host_remains_active(self):
        f=pc("F",3);e,g=game(f);e.start_turn("caster")
        g.cast_scholar_composite("caster","Vital Shelter")
        before=(f.ap_remaining,f.vp_available,f.vp_committed,f.vp_spent,
                len(e.ledger))
        with self.assertRaisesRegex(ValueError,"one Stone Skin"):
            g.cast_scholar_composite("caster","Basic Heal",heal_die=3,
                                      hand_available=True)
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_committed,
                          f.vp_spent,len(e.ledger)),before)
        e.check()

    def test_41_successful_effect_and_end_logging_does_not_collide_with_event_kind(self):
        f=pc("F",2);e,g=game(f);e.start_turn("caster")
        host=g.cast_scholar_composite("caster","Vital Shelter")
        self.assertEqual(len(g.active("caster","Vital Shelter")),1)
        established=spell_events(e,"g3_effect_established")
        self.assertEqual([x["detail"]["effect_kind"] for x in established],
                         ["Stone Skin","Vital Shelter"])
        self.assertEqual(host.ident,established[0]["detail"]["effect"])
        g.release("caster","Stone Skin")
        ended=spell_events(e,"g3_effect_ended")
        self.assertEqual([x["detail"]["effect_kind"] for x in ended],
                         ["Vital Shelter","Stone Skin"])
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(11,0,1))
        e.check()

    def test_42_reactive_stone_forged_generic_response_rejected_even_after_real_g0_commit(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        tr=Trigger("forged","attacker","caster")
        forged=Response("caster","reaction","g3:reactive_stone")
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            e.response_window(
                tr,on_interception=lambda state,trigger,r:None,
                spontaneous=(forged,),
                on_spontaneous=lambda state,trigger,r:
                    g.resolve_reactive_stone("caster",trigger,r))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(g.effects)
        e.check()

    def test_43_reactive_stone_prepared_on_event_a_cannot_apply_to_event_b(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        a=Trigger("incoming-A","attacker","caster")
        b=Trigger("incoming-B","attacker","caster")
        prepared=g.prepare_reactive_stone("caster",a,perceptible=True)
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            e.response_window(
                b,on_interception=lambda state,trigger,r:None,
                spontaneous=(prepared,),
                on_spontaneous=lambda state,trigger,r:
                    g.resolve_reactive_stone("caster",trigger,r))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(g.effects)
        e.check()

    def test_44_reactive_stone_claim_binds_same_trigger_instance_not_just_key(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        original=Trigger("reused-key","attacker","caster")
        clone=Trigger("reused-key","attacker","caster")
        response=g.prepare_reactive_stone("caster",original,perceptible=True)
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            e.response_window(
                clone,on_interception=lambda state,trigger,r:None,
                spontaneous=(response,),
                on_spontaneous=lambda state,trigger,r:
                    g.resolve_reactive_stone("caster",trigger,r))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(g.effects)
        e.check()

    def test_45_reactive_stone_claim_cannot_be_created_twice(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        tr=Trigger("incoming-once","attacker","caster")
        g.prepare_reactive_stone("caster",tr,perceptible=True)
        with self.assertRaisesRegex(ValueError,"already preflighted"):
            g.prepare_reactive_stone("caster",tr,perceptible=True)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        e.check()

    def test_46_dodge_invalidated_after_ap_loses_no_flame_vp_or_dodge_pressure(self):
        f=pc("F")
        target=pc("R",3,"target",(4,2),"enemy")
        e,g=game(f,target);e.start_turn("caster")
        def target_incapacitated(state):
            state.actors["target"].hp=0
        result=g.cast_flame("caster","target",tier=1,face=18,
                            vigor_die=6,defense="dodge",aware=True,
                            hand_available=True,on_committed=target_incapacitated)
        self.assertEqual(result,{"outcome":"interrupted_before_launch","vp_spent":0})
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_spent),(22,18,0))
        self.assertEqual(target.dodge_pressure,0)
        self.assertFalse(spell_events(e,"g3_flame_launched"))
        self.assertEqual(spell_events(e,"g3_cast_interrupted")[-1]["detail"]["cause"],
                         "post_commit_defense_unusable")
        e.check()

    def test_47_guard_invalidated_after_ap_loses_no_flame_vp_or_guard_capacity(self):
        f=pc("F")
        target=enemy_actor("B06-EN-02","target","enemy",occupied=((4,2),))
        e,g=game(f,target);e.start_turn("caster")
        before=target.guard_remaining
        def lose_shield(state):
            state.actors["target"].ready_guard=False
        result=g.cast_flame("caster","target",tier=1,face=14,
                            vigor_die=4,defense="guard",aware=True,
                            hand_available=True,on_committed=lose_shield)
        self.assertEqual(result["outcome"],"interrupted_before_launch")
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_spent),(22,18,0))
        self.assertEqual(target.guard_remaining,before)
        self.assertFalse(spell_events(e,"g3_flame_launched"))
        e.check()

    def test_48_voluntary_release_rejects_out_of_turn_and_bypass_keyword(self):
        f=pc("F")
        other=pc("R",3,"other",(4,2),"enemy")
        e,g=game(f,other);e.start_turn("caster")
        g.cast_stone("caster")
        e.end_turn()
        e.start_turn("other")
        before=(f.vp_available,f.vp_committed,f.vp_spent,len(g.effects))
        with self.assertRaisesRegex(ValueError,"own-turn decision"):
            g.release("caster","Stone Skin")
        with self.assertRaises(TypeError):
            g.release("caster","Stone Skin",own_turn=False)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent,
                          len(g.effects)),before)
        # An actual loss-of-consciousness event can still trigger the
        # dedicated forced termination path outside the caster's turn.
        f.hp=0
        g.sync_consciousness("caster")
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        e.check()

    def test_49_flame_at_three_squares_uses_prone_plus_two_static_defense(self):
        f=pc("F")
        target=pc("R",3,"target",(4,2),"enemy")
        target.conditions.append("Prone")
        e,g=game(f,target);e.start_turn("caster")
        r=g.cast_flame("caster","target",tier=1,face=7,vigor_die=5,
                       hand_available=True)
        self.assertEqual((r["base_defense"],r["final_defense"]),(12,12))
        self.assertEqual(r["outcome"],"ordinary_miss")
        self.assertIsNone(r["packets_pending_g4"])
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_spent),(22,16,2))
        e.check()

    def test_50_flame_prone_with_cover_requires_profile_policy_before_ap(self):
        f=pc("F")
        target=pc("R",3,"target",(4,2),"enemy")
        target.conditions.append("Prone")
        e,g=game(f,target,cover=(CoverSurface((2,2),4,(1,0)),))
        e.start_turn("caster")
        before=(f.ap_remaining,f.vp_available,f.vp_spent)
        with self.assertRaisesRegex(UnresolvedDecision,"Prone plus Cover"):
            g.cast_flame("caster","target",tier=1,face=10,vigor_die=2,
                         hand_available=True)
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_spent),before)
        r=g.cast_flame("caster","target",tier=1,face=10,vigor_die=2,
                       hand_available=True,
                       prone_cover_policy=(("target","absorbed"),))
        self.assertEqual((r["base_defense"],r["final_defense"]),(10,14))
        self.assertEqual(r["outcome"],"direct_hit_pending_G4")
        e.check()

    def test_51_flame_explicit_prone_dodge_feasibility_not_implicitly_granted(self):
        f=pc("F")
        target=pc("R",3,"target",(4,2),"enemy")
        target.conditions.append("Prone")
        e,g=game(f,target);e.start_turn("caster")
        before=(f.ap_remaining,f.vp_available,f.vp_spent)
        with self.assertRaisesRegex(UnresolvedDecision,"Prone Dodge"):
            g.cast_flame("caster","target",tier=1,face=6,vigor_die=3,
                         defense="dodge",aware=True,hand_available=True)
        self.assertEqual((f.ap_remaining,f.vp_available,f.vp_spent),before)
        r=g.cast_flame("caster","target",tier=1,face=6,vigor_die=3,
                       defense="dodge",aware=True,hand_available=True,
                       prone_dodge_feasible=True)
        self.assertEqual(target.dodge_pressure,2)
        self.assertGreaterEqual(r["final_defense"],12)
        self.assertEqual(f.vp_spent,2)
        e.check()

    def test_52_reactive_stone_cannot_resolve_after_response_window_returns(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        trigger=Trigger("incoming-live-only","attacker","caster")
        response=g.prepare_reactive_stone("caster",trigger,perceptible=True)
        seen=[]
        self.assertTrue(e.response_window(
            trigger,on_interception=lambda state,tr,r:None,
            spontaneous=(response,),
            on_spontaneous=lambda state,tr,r:seen.append(r.label)))
        self.assertEqual(seen,[response.label])
        self.assertFalse(f.reaction_available)  # G0 really paid the Reaction
        self.assertTrue(spell_events(e,"trigger_ready_to_resolve"))
        self.assertFalse(e.is_live_spontaneous(trigger,response))
        self.assertFalse(g.reactive_stone_claims)
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            g.resolve_reactive_stone("caster",trigger,response)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(g.effects)
        self.assertFalse(spell_events(e,"g3_stone_reacted"))
        e.check()

    def test_53_earlier_initiative_response_incapacitates_committed_stone_caster(self):
        interruptor=pc("A",3,"interruptor",(4,3),"enemy")
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(interruptor,attacker,f)
        trigger=Trigger("incoming-precommitted","attacker","caster")
        stone=g.prepare_reactive_stone("caster",trigger,perceptible=True)
        other=Response("interruptor","reaction","earlier-hp-zero")
        results=[]
        def on_spontaneous(state,tr,response):
            if response is other:
                self.assertFalse(f.reaction_available)
                # Independently resolved earlier response; G4 will later
                # own the actual HP/damage engine.
                f.hp=0
                results.append("incapacitated_before_stone")
            else:
                results.append(g.resolve_reactive_stone("caster",tr,response))
        self.assertTrue(e.response_window(
            trigger,on_interception=lambda state,tr,res:None,
            spontaneous=(stone,other),on_spontaneous=on_spontaneous))
        self.assertEqual(results,["incapacitated_before_stone",None])
        self.assertFalse(f.reaction_available)
        self.assertFalse(interruptor.reaction_available)
        self.assertFalse(g.reactive_stone_claims)
        self.assertIn(("caster",stone.label),g.reactive_stone_claimed)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(g.effects)
        cancelled=spell_events(e,"g3_cast_interrupted")
        self.assertEqual(cancelled[-1]["detail"]["cause"],"post_commit_incapacitated")
        self.assertEqual(cancelled[-1]["detail"]["vp_spent"],0)
        self.assertEqual(len(spell_events(e,"trigger_rechecked_after_responses")),1)
        self.assertEqual(len(spell_events(e,"trigger_ready_to_resolve")),1)
        self.assertFalse(e.is_live_spontaneous(trigger,stone))
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            g.resolve_reactive_stone("caster",trigger,stone)
        e.check()

    def test_54_live_other_actor_callback_cannot_execute_precommitted_stone(self):
        interruptor=pc("A",3,"interruptor",(4,3),"enemy")
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(interruptor,attacker,f)
        trigger=Trigger("incoming-other-callback","attacker","caster")
        stone=g.prepare_reactive_stone("caster",trigger,perceptible=True)
        other=Response("interruptor","reaction","earlier-attempt")
        observed=[]
        def on_spontaneous(state,tr,response):
            if response is other:
                with self.assertRaisesRegex(ValueError,"requires its live response callback"):
                    g.resolve_reactive_stone("caster",tr,stone)
                self.assertEqual(f.vp_committed,0)
                observed.append("rejected_wrong_live_callback")
            else:
                self.assertIsNotNone(g.resolve_reactive_stone("caster",tr,response))
                observed.append("accepted_matching_callback")
        self.assertTrue(e.response_window(
            trigger,on_interception=lambda state,tr,r:None,
            spontaneous=(stone,other),on_spontaneous=on_spontaneous))
        self.assertEqual(observed,["rejected_wrong_live_callback",
                                   "accepted_matching_callback"])
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(12,6,0))
        self.assertFalse(e.is_live_spontaneous(trigger,stone))
        e.check()

    def test_55_nested_response_window_restores_parent_authorization(self):
        interruptor=pc("A",3,"interruptor",(4,3),"enemy")
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,interruptor,f)
        outer=Trigger("outer-incoming","attacker","caster")
        stone=g.prepare_reactive_stone("caster",outer,perceptible=True)
        inner=Trigger("nested-incoming","attacker","interruptor")
        inner_choice=Response("interruptor","reaction","nested-choice")
        def outer_callback(state,tr,response):
            self.assertTrue(state.is_live_spontaneous(outer,stone))
            def inner_callback(state_inner,tr_inner,response_inner):
                self.assertTrue(state_inner.is_live_spontaneous(inner,inner_choice))
                self.assertFalse(state_inner.is_live_spontaneous(outer,stone))
                with self.assertRaisesRegex(ValueError,"requires its live response callback"):
                    g.resolve_reactive_stone("caster",outer,stone)
            self.assertTrue(state.response_window(
                inner,on_interception=lambda st,trigger,res:None,
                spontaneous=(inner_choice,),on_spontaneous=inner_callback))
            self.assertTrue(state.is_live_spontaneous(outer,stone))
            self.assertIsNotNone(g.resolve_reactive_stone("caster",outer,stone))
        self.assertTrue(e.response_window(
            outer,on_interception=lambda state,tr,res:None,
            spontaneous=(stone,),on_spontaneous=outer_callback))
        self.assertFalse(e.is_live_spontaneous(outer,stone))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(12,6,0))
        e.check()

    def test_56_exception_in_callback_clears_live_response_authority(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        trigger=Trigger("raise-after-commit","attacker","caster")
        stone=g.prepare_reactive_stone("caster",trigger,perceptible=True)
        def broken_callback(state,tr,response):
            self.assertTrue(state.is_live_spontaneous(trigger,stone))
            raise RuntimeError("authored effect resolver failed")
        with self.assertRaisesRegex(RuntimeError,"authored effect resolver failed"):
            e.response_window(
                trigger,on_interception=lambda state,tr,r:None,
                spontaneous=(stone,),on_spontaneous=broken_callback)
        self.assertFalse(e.is_live_spontaneous(trigger,stone))
        self.assertFalse(g.reactive_stone_claims)
        self.assertFalse(f.reaction_available)
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            g.resolve_reactive_stone("caster",trigger,stone)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(g.effects)
        e.check()

    def test_57_prior_spontaneous_cancels_trigger_after_both_reactions_paid(self):
        interrupter=pc("A",3,"interrupter",(4,3),"enemy")
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(interrupter,attacker,f)
        trigger=Trigger("previous-response-cancel","attacker","caster")
        stone=g.prepare_reactive_stone("caster",trigger,perceptible=True)
        first=Response("interrupter","reaction","preempt-original-trigger")
        resolved=[]
        before=(f.vp_available,f.vp_committed,f.vp_spent,
                interrupter.reaction_available,f.reaction_available)
        def on_spontaneous(state,tr,response):
            # G0 reserves BOTH Reactions before resolving by initiative.
            self.assertFalse(f.reaction_available)
            self.assertFalse(interrupter.reaction_available)
            if response is first:
                tr.legal=False
                resolved.append("cancelled_by_earlier_response")
            else:
                self.assertTrue(state.is_live_spontaneous(trigger,stone))
                resolved.append(g.resolve_reactive_stone("caster",tr,response))
        self.assertFalse(e.response_window(
            trigger,on_interception=lambda state,tr,res:None,
            spontaneous=(stone,first),on_spontaneous=on_spontaneous))
        self.assertEqual(resolved,["cancelled_by_earlier_response",None])
        self.assertEqual(before[:3],(18,0,0))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        self.assertFalse(f.reaction_available)
        self.assertFalse(interrupter.reaction_available)
        self.assertEqual(g.reactive_stone_claims,{})
        self.assertIn(("caster",stone.label),g.reactive_stone_claimed)
        self.assertFalse(g.effects)
        self.assertFalse(spell_events(e,"g3_stone_reacted"))
        ended=spell_events(e,"g3_cast_interrupted")
        self.assertEqual(len(ended),1)
        self.assertEqual(ended[0]["detail"]["cause"],"post_commit_trigger_cancelled")
        self.assertEqual(ended[0]["detail"]["vp_spent"],0)
        self.assertEqual([x["detail"]["legal"] for x in
                          spell_events(e,"trigger_rechecked_after_responses")],[False])
        self.assertEqual(len(spell_events(e,"trigger_cancelled_after_spontaneous")),1)
        self.assertFalse(spell_events(e,"trigger_ready_to_resolve"))
        self.assertFalse(e.is_live_spontaneous(trigger,stone))
        # The cancelled claim cannot later be reused, including from
        # another allegedly current response window with the same key.
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            g.resolve_reactive_stone("caster",trigger,stone)
        e.check()

    def test_58_new_stone_reaction_reusing_previous_text_key_is_legal(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        first_trigger=Trigger("repeat-attacked-cell","attacker","caster")
        first=g.prepare_reactive_stone("caster",first_trigger,perceptible=True)
        self.assertTrue(e.response_window(
            first_trigger,on_interception=lambda state,tr,response:None,
            spontaneous=(first,),
            on_spontaneous=lambda state,tr,response:
                g.resolve_reactive_stone("caster",tr,response)))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(12,6,0))
        self.assertIn(("caster",first.label),g.reactive_stone_claimed)
        # The first Stone Skin must be released on its actual own turn.
        e.start_turn("attacker")
        e.end_turn()
        e.start_turn("caster")
        g.release("caster","Stone Skin")
        e.end_turn()
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(18,0,0))
        e.begin_round()
        # Fresh, source-valid attack reuses the same external text key.
        second_trigger=Trigger("repeat-attacked-cell","attacker","caster")
        second=g.prepare_reactive_stone("caster",second_trigger,perceptible=True)
        self.assertIsNot(first_trigger,second_trigger)
        self.assertNotEqual(first.label,second.label)
        self.assertTrue(e.response_window(
            second_trigger,on_interception=lambda state,tr,response:None,
            spontaneous=(second,),
            on_spontaneous=lambda state,tr,response:
                g.resolve_reactive_stone("caster",tr,response)))
        self.assertEqual(len(spell_events(e,"g3_stone_reacted")),2)
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(12,6,0))
        self.assertEqual(g.reactive_stone_claims,{})
        self.assertIn(("caster",first.label),g.reactive_stone_claimed)
        self.assertIn(("caster",second.label),g.reactive_stone_claimed)
        self.assertNotIn(("caster",first_trigger.key),g.reactive_stone_claimed)
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            g.resolve_reactive_stone("caster",first_trigger,first)
        e.check()

    def test_59_prepared_sentry_can_rewield_and_pay_to_recast_ended_reserve(self):
        s=sentry("prepared_start")
        e,g=game(s)
        e.start_turn("sentry")
        # Initial prepared source state loaded 3 Committed without recast.
        self.assertEqual((s.vp_available,s.vp_committed,s.vp_spent),(3,3,0))
        e.g2.wielded["sentry"].discard("Sword")
        g.sword_no_longer_wielded("sentry")
        self.assertEqual((s.vp_available,s.vp_committed,s.vp_spent),(6,0,0))
        self.assertFalse(g.active("sentry","Sentry Sword Reserve"))
        with self.assertRaisesRegex(ValueError,"Unwielded sword"):
            g.sentry_profile("sentry")
        # The equipment action is separately source-adjudicated; G3 does
        # not invent a free re-wielding action or refill spell resources.
        # This actor starts its later ready turn with a re-wielded sword.
        e.end_turn()
        e.begin_round()
        e.start_turn("sentry")
        e.g2.wielded["sentry"].add("Sword")
        self.assertEqual(g.sentry_profile("sentry"),"B06-AT-01")
        self.assertEqual((s.ap_remaining,s.vp_available,s.vp_committed),
                         (42,6,0))
        instance=g.cast_sentry_reserve("sentry")
        self.assertEqual(instance.ident,"B06-FIRE-RESERVE-01")
        self.assertEqual((s.ap_remaining,s.vp_available,s.vp_committed,
                          s.vp_spent),(12,3,3,0))
        self.assertEqual(g.sentry_profile("sentry"),"B06-AT-02")
        with self.assertRaisesRegex(ValueError,"Insufficient source-specific Projection AP"):
            g.cast_sentry_reserve("sentry")
        self.assertEqual(len(spell_events(e,"g3_effect_established")),1)
        self.assertEqual(len(spell_events(e,"vp_transition")),1)
        self.assertEqual(len(spell_events(e,"vp_release")),1)
        e.check()

    def test_60_prepared_sentry_cannot_recast_without_wielding_or_with_active_reserve(self):
        s=sentry("prepared_start")
        e,g=game(s)
        e.start_turn("sentry")
        initial=(s.ap_remaining,s.vp_available,s.vp_committed,s.vp_spent)
        with self.assertRaisesRegex(ValueError,"Already active"):
            g.cast_sentry_reserve("sentry")
        self.assertEqual((s.ap_remaining,s.vp_available,s.vp_committed,
                          s.vp_spent),initial)
        e.g2.wielded["sentry"].discard("Sword")
        g.sword_no_longer_wielded("sentry")
        before=(s.ap_remaining,s.vp_available,s.vp_committed,s.vp_spent)
        with self.assertRaisesRegex(ValueError,"must actually be wielded"):
            g.cast_sentry_reserve("sentry")
        self.assertEqual((s.ap_remaining,s.vp_available,s.vp_committed,
                          s.vp_spent),before)
        self.assertEqual((s.vp_available,s.vp_committed,s.vp_spent),(6,0,0))
        e.check()

    def test_61_composite_rechecks_reactive_stone_exclusivity_after_ap_commit(self):
        for secondary in ("Basic Heal","Vital Shelter"):
            with self.subTest(secondary=secondary):
                f=pc("F",3)
                f.hp-=2;f.vigor-=5
                e,g=game(f)
                e.start_turn("caster",regen_choice=RegenerationChoice())
                hp_before,vigor_before=f.hp,f.vigor
                def incoming_stone(event):
                    tr=Trigger("respond-during-composite","enemy","caster")
                    choice=g.prepare_reactive_stone("caster",tr,perceptible=True)
                    self.assertTrue(event.response_window(
                        tr,on_interception=lambda ev,t,r:None,
                        spontaneous=(choice,),
                        on_spontaneous=lambda ev,t,r:
                            g.resolve_reactive_stone("caster",t,r)))
                kwargs=({"heal_tier":1,"heal_die":4,"hand_available":True}
                        if secondary=="Basic Heal" else {})
                out=g.cast_scholar_composite(
                    "caster",secondary,on_committed=incoming_stone,**kwargs)
                self.assertIsNone(out)
                self.assertEqual((f.ap_remaining,f.vp_available,
                                  f.vp_committed,f.vp_spent),(22,12,6,0))
                self.assertEqual((f.hp,f.vigor),(hp_before,vigor_before))
                self.assertEqual(len(g.active("caster","Stone Skin")),1)
                self.assertFalse(g.active("caster","Vital Shelter"))
                self.assertFalse(spell_events(e,"g3_basic_heal_secondary_once"))
                self.assertEqual(len(spell_events(e,"g3_effect_established")),1)
                latest=spell_events(e,"g3_cast_interrupted")[-1]["detail"]
                self.assertEqual(latest["cause"],
                                 "stone_skin_activated_during_responses")
                self.assertEqual(latest["vp_spent"],0)
                g.release("caster","Stone Skin")
                self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),
                                 (18,0,0))
                e.check()

    def test_62_interception_cancellation_expires_claim_before_reused_key(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        e.start_turn("attacker")
        e.reserve("attacker","same-key-after-cancel","stop",
                  action_kind="physical")
        e.end_turn()
        original=Trigger("same-key-after-cancel","attacker","caster")
        first=g.prepare_reactive_stone("caster",original,perceptible=True)
        self.assertFalse(e.response_window(
            original,
            on_interception=lambda ev,tr,r:setattr(tr,"legal",False),
            spontaneous=(first,),
            on_spontaneous=lambda ev,tr,r:
                g.resolve_reactive_stone("caster",tr,r)))
        self.assertTrue(f.reaction_available)
        self.assertFalse(g.reactive_stone_claims)
        self.assertFalse(g.reactive_stone_claimed)
        self.assertEqual(len(spell_events(e,"g3_reactive_claim_expired")),1)
        with self.assertRaisesRegex(ValueError,"No matching preflight claim"):
            g.resolve_reactive_stone("caster",original,first)
        e.start_turn("caster")
        e.end_turn()
        e.begin_round()
        new=Trigger("same-key-after-cancel","attacker","caster")
        second=g.prepare_reactive_stone("caster",new,perceptible=True)
        self.assertNotEqual(first.label,second.label)
        self.assertTrue(e.response_window(
            new,on_interception=lambda ev,tr,r:None,
            spontaneous=(second,),
            on_spontaneous=lambda ev,tr,r:
                g.resolve_reactive_stone("caster",tr,r)))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(12,6,0))
        self.assertFalse(f.reaction_available)
        self.assertEqual(len(spell_events(e,"g3_stone_reacted")),1)
        self.assertIn(("caster",second.label),g.reactive_stone_claimed)
        self.assertNotIn(("caster",first.label),g.reactive_stone_claimed)
        self.assertFalse(g.reactive_stone_claims)
        self.assertEqual(len(spell_events(e,"trigger_cancelled_before_spontaneous")),1)
        e.check()

    def test_63_prepared_but_undeclared_response_claim_expires_on_normal_exit(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        old=Trigger("normal-window-omit","attacker","caster")
        response=g.prepare_reactive_stone("caster",old,perceptible=True)
        self.assertTrue(e.response_window(
            old,on_interception=lambda ev,tr,r:None,spontaneous=()))
        self.assertTrue(f.reaction_available)
        self.assertFalse(g.reactive_stone_claims)
        self.assertFalse(g.reactive_stone_claimed)
        self.assertEqual(len(spell_events(e,"g3_reactive_claim_expired")),1)
        new=Trigger("normal-window-omit","attacker","caster")
        accepted=g.prepare_reactive_stone("caster",new,perceptible=True)
        self.assertNotEqual(response.label,accepted.label)
        self.assertTrue(e.response_window(
            new,on_interception=lambda ev,tr,r:None,
            spontaneous=(accepted,),
            on_spontaneous=lambda ev,tr,r:
                g.resolve_reactive_stone("caster",tr,r)))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(12,6,0))
        e.check()

    def test_64_exception_exit_clears_only_exact_trigger_claim(self):
        attacker=pc("R",3,"attacker",(4,2),"enemy")
        f=pc("F")
        e,g=game(attacker,f)
        old=Trigger("exception-cancel","attacker","caster")
        first=g.prepare_reactive_stone("caster",old,perceptible=True)
        def fail_interception(ev,tr,res):
            raise RuntimeError("interception policy exception")
        e.start_turn("attacker")
        e.reserve("attacker",old.key,"deliberate-exception",
                  action_kind="physical")
        e.end_turn()
        with self.assertRaisesRegex(RuntimeError,"interception policy exception"):
            e.response_window(old,on_interception=fail_interception,
                              spontaneous=(first,),
                              on_spontaneous=lambda ev,tr,r:None)
        self.assertTrue(f.reaction_available)
        self.assertFalse(g.reactive_stone_claims)
        self.assertEqual(len(spell_events(e,"g3_reactive_claim_expired")),1)
        new=Trigger(old.key,"attacker","caster")
        response=g.prepare_reactive_stone("caster",new,perceptible=True)
        self.assertNotEqual(first.label,response.label)
        self.assertTrue(e.response_window(
            new,on_interception=lambda ev,tr,r:None,
            spontaneous=(response,),
            on_spontaneous=lambda ev,tr,r:
                g.resolve_reactive_stone("caster",tr,r)))
        self.assertEqual((f.vp_available,f.vp_committed,f.vp_spent),(12,6,0))
        e.check()

    def test_65_self_heal_requires_fresh_hand_check_if_responses_exist(self):
        f=pc("F",3)
        f.hp-=2
        e,g=game(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        before=(f.ap_remaining,f.vp_available,f.hp)
        with self.assertRaisesRegex(UnresolvedDecision,"live hand_check"):
            g.cast_self_basic_heal("caster",die=1,hand_available=True,
                                   on_committed=lambda _e:None)
        self.assertEqual((f.ap_remaining,f.vp_available,f.hp),before)
        e.check()

    def test_66_self_heal_disarmed_during_commit_spends_no_vp(self):
        f=pc("F",3);f.hp-=2;f.vigor-=10
        e,g=game(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        hand={"free":True}
        def take_hand(_e):
            hand["free"]=False
        result=g.cast_self_basic_heal(
            "caster",tier=1,die=8,hand_available=True,
            on_committed=take_hand,
            hand_check=lambda _e,_c:hand["free"])
        self.assertIsNone(result)
        self.assertEqual((f.ap_remaining,f.vp_spent,f.vp_committed),(22,0,0))
        self.assertEqual((f.hp,f.vigor),(f.hp_max-2,f.vigor_max-10))
        self.assertTrue(any(x["kind"]=="g3_cast_interrupted" for x in e.ledger))
        e.check()

    def test_67_composite_heal_disarmed_after_commit_has_no_host(self):
        f=pc("F",3);f.hp-=2;f.vigor-=9
        e,g=game(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        hand={"free":True}
        def lose_hand(_e):
            hand["free"]=False
        result=g.cast_scholar_composite(
            "caster","Basic Heal",heal_tier=2,heal_die=6,
            hand_available=True,on_committed=lose_hand,
            hand_check=lambda _e,_c:hand["free"])
        self.assertIsNone(result)
        self.assertEqual((f.ap_remaining,f.vp_spent,f.vp_committed),(22,0,0))
        self.assertFalse(g.effects)
        e.check()

    def test_68_unchanged_hand_after_commit_heals_once(self):
        f=pc("F",3);f.hp-=2;f.vigor-=9
        e,g=game(f);e.start_turn("caster",regen_choice=RegenerationChoice())
        host=g.cast_scholar_composite(
            "caster","Basic Heal",heal_die=6,hand_available=True,
            on_committed=lambda _e:None,hand_check=lambda _e,_c:True)
        self.assertIsNotNone(host)
        self.assertEqual((f.hp,f.vigor),(f.hp_max-1,f.vigor_max-6))
        self.assertEqual((f.vp_spent,f.vp_committed),(2,6))
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
