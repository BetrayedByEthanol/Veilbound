"""G6-A native Hunter source actions, venom, posture and multi-turn I3."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_hunter_g6a_v0 import HunterCombat, run_i3


def setup(*, front=(6,2), head=(2,2), rear=(1,2), walls=(), role="A"):
    hunter=enemy_actor("B06-EN-03","hunter","enemy",
                       occupied=(head,rear))
    prey=party_actor(role,3,"prey","party",occupied=(front,))
    e=Encounter([hunter,prey],{"hunter":30,"prey":20},
                seed=606,scenario="G6A-source-check",
                objective="bounded_hunter_source_action",
                policy="all_optional_reactions_declined")
    GridMovement(e,width=12,height=6,walls=walls)
    SpellState(e)
    DamageState(e)
    e.begin_round()
    combat=HunterCombat(e)
    combat.bridge.start_next_turn(RegenerationChoice())
    return e,combat


def events(e,kind):
    return [x for x in e.ledger if x["kind"]==kind]


class HunterG6ATests(unittest.TestCase):
    def test_01_normal_bite_g0_g4_g44_g45_once(self):
        e,c=setup(front=(3,2))
        s=c.declare("hunter","prey",profiles=("B06-AT-04",),
                    defenses=("take_hit",))
        self.assertEqual(e.actors["hunter"].ap_remaining,18)
        result=c.resolve(s,0,attack_face=10,damage_face=1,
                         venom_resistance_die=1)
        self.assertEqual(result["outcome"],"hit")
        self.assertEqual(result["damage"]["hp_loss"],2)
        self.assertEqual(result["damage"]["venom"]["outcome"],"accepted")
        self.assertEqual(len(events(e,"g4_profile_hit")),1)
        self.assertEqual(len(events(e,"g44_hunter_accepted")),1)
        self.assertEqual(len(events(e,"g45_attested_hit")),1)
        self.assertEqual(len(events(e,"g5_melee_resolved")),1)
        with self.assertRaises(ValueError):
            c.resolve(s,0,attack_face=10,damage_face=1,
                      venom_resistance_die=1)
        e.check()

    def test_02_natural_one_does_not_create_venom_or_damage(self):
        e,c=setup(front=(3,2))
        s=c.declare("hunter","prey",profiles=("B06-AT-04",),
                    defenses=("guard",))
        p=e.actors["prey"]
        first=(p.hp,p.vigor)
        result=c.resolve(s,0,attack_face=1)
        self.assertEqual(result["outcome"],"miss")
        self.assertEqual((p.hp,p.vigor),first)
        self.assertFalse(events(e,"g4_profile_hit"))
        self.assertFalse(events(e,"g44_hunter_accepted"))
        e.check()

    def test_03_no_puncture_means_no_resistance_roll(self):
        e,c=setup(front=(3,2),role="B")
        s=c.declare("hunter","prey",profiles=("B06-AT-04",),
                    defenses=("take_hit",))
        # B wears brigandine Armor5, Pen1: 3+d6=4 causes zero HP.
        out=c.resolve(s,0,attack_face=10,damage_face=1)
        self.assertEqual(out["damage"]["hp_loss"],0)
        self.assertEqual(out["damage"]["venom"]["outcome"],"not_delivered")
        self.assertFalse(events(e,"g44_hunter_accepted"))
        e.check()

    def test_04_missing_venom_resistance_blocks_before_roll_damage(self):
        e,c=setup(front=(3,2))
        s=c.declare("hunter","prey",profiles=("B06-AT-04",),
                    defenses=("take_hit",))
        original_hp=e.actors["prey"].hp
        with self.assertRaises(UnresolvedDecision):
            c.resolve(s,0,attack_face=10,damage_face=1)
        self.assertEqual(e.actors["prey"].hp,original_hp)
        self.assertFalse(events(e,"g5_melee_roll"))
        self.assertEqual(len(c.pending_attack_slots("hunter")),1)
        e.check()

    def test_05_horn_bash_has_damage_but_never_poison(self):
        e,c=setup(front=(3,2))
        s=c.declare("hunter","prey",profiles=("B06-AT-05",),
                    defenses=("take_hit",))
        out=c.resolve(s,0,attack_face=10,damage_face=3)
        self.assertEqual(out["outcome"],"hit")
        self.assertEqual(out["damage"]["hp_loss"],2)
        self.assertFalse(events(e,"g44_hunter_accepted"))
        e.check()

    def test_06_hunter_anatomical_front_required_before_payment(self):
        e,c=setup(front=(2,3))
        before=e.actors["hunter"].ap_remaining
        with self.assertRaises(UnresolvedDecision):
            c.declare("hunter","prey",profiles=("B06-AT-04",),
                      defenses=("take_hit",))
        self.assertEqual(e.actors["hunter"].ap_remaining,before)
        self.assertFalse(events(e,"attack_sequence_committed"))

    def test_07_g0_direct_hunter_sequence_rejected(self):
        e,c=setup(front=(3,2))
        with self.assertRaises(UnresolvedDecision):
            e.declare_sequence("hunter","prey",
                               ("B06-AT-04",),("take_hit",))
        self.assertEqual(e.actors["hunter"].ap_remaining,42)
        self.assertFalse(events(e,"action_committed"))

    def test_08_pounce_missed_bite_still_knocks_down(self):
        e,c=setup()
        receipt=c.begin_pounce("hunter","prey",((1,0),)*3,
                               defense="take_hit")
        self.assertEqual(e.actors["hunter"].ap_remaining,18)
        self.assertEqual(len(c.pending_attack_slots("hunter")),1)
        with self.assertRaises(UnresolvedDecision):
            e.end_turn()
        with self.assertRaises(UnresolvedDecision):
            e.g1.step("hunter",(0,1))
        out=c.resolve_pounce(receipt,attack_face=1,
                             balance_hunter_face=20,
                             balance_defender_face=1,balance_ability="Strength")
        self.assertEqual(out["bite"],"miss")
        self.assertEqual(out["balance"],"prone")
        self.assertIn("Prone",e.actors["prey"].conditions)
        self.assertFalse(events(e,"g4_profile_hit"))
        self.assertFalse(c.pending_attack_slots("hunter"))
        e.check()

    def test_09_pounce_hit_delivers_venom_but_balance_held(self):
        e,c=setup()
        out=c.pounce("hunter","prey",((1,0),)*3,
                     attack_face=10,damage_face=1,
                     venom_resistance_die=1,
                     balance_hunter_face=1,balance_defender_face=20,
                     balance_ability="Strength")
        self.assertEqual(out["bite"],"hit")
        self.assertEqual(out["balance"],"held")
        self.assertEqual(out["damage"]["venom"]["outcome"],"accepted")
        self.assertNotIn("Prone",e.actors["prey"].conditions)
        self.assertEqual(len(events(e,"g6_pounce_melee_roll")),1)
        self.assertEqual(len(events(e,"g6_pounce_balance")),1)
        self.assertEqual(len(events(e,"g45_attested_hit")),1)
        e.check()

    def test_10_pounce_bite_can_make_dying_preys_balance_automatic(self):
        e,c=setup()
        e.actors["prey"].hp=2
        out=c.pounce("hunter","prey",((1,0),)*3,
                     attack_face=10,damage_face=1,
                     wound_location_roll=8,
                     venom_resistance_die=1)
        self.assertTrue(e.actors["prey"].hp<=0)
        self.assertEqual(out["balance"],"automatic_unable_to_contest")
        self.assertIn("Prone",e.actors["prey"].conditions)
        self.assertEqual(len(events(e,"g6_pounce_balance")),0)
        e.check()

    def test_11_pounce_receipts_are_not_spendable_twice(self):
        e,c=setup()
        receipt=c.begin_pounce("hunter","prey",((1,0),)*3)
        self.assertEqual(c.resolve_pounce(receipt,attack_face=1,
                           balance_hunter_face=1,balance_defender_face=20,
                           balance_ability="Strength")["bite"],"miss")
        with self.assertRaises(ValueError):
            c.resolve_pounce(receipt,attack_face=1,
                             balance_hunter_face=1,
                             balance_defender_face=20,balance_ability="Strength")
        e.check()

    def test_12_pounce_requires_g6_approved_entry(self):
        e,c=setup()
        with self.assertRaises(UnresolvedDecision):
            e.g1.start_pounce("hunter","prey")
        self.assertFalse(events(e,"g1_pounce_declared"))
        self.assertEqual(e.actors["hunter"].ap_remaining,42)

    def test_13_prone_crawl_and_stand_are_paid_and_genuine(self):
        e,c=setup()
        out=c.pounce("hunter","prey",((1,0),)*3,
                     attack_face=1,balance_hunter_face=20,
                     balance_defender_face=1,balance_ability="Strength")
        self.assertEqual(out["balance"],"prone")
        c.bridge.end_current_turn()
        c.bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(e.g1.crawl_step("prey",(0,1)))
        self.assertEqual(e.actors["prey"].mp_remaining,8)
        self.assertTrue(e.g1.stand("prey"))
        self.assertEqual(e.actors["prey"].mp_remaining,4)
        self.assertNotIn("Prone",e.actors["prey"].conditions)
        self.assertEqual(len(events(e,"g6_stand_completed")),1)
        e.check()

    def test_14_horn_drive_displaces_one_whole_body_step(self):
        e,c=setup(front=(3,2))
        out=c.horn_drive("hunter","prey",pressure_face=18,
                         resistance_face=1)
        self.assertEqual(out["outcome"],"shoved")
        self.assertEqual(e.actors["prey"].occupied,((4,2),))
        self.assertEqual(e.actors["hunter"].occupied,((3,2),(2,2)))
        self.assertEqual(e.actors["hunter"].ap_remaining,18)
        self.assertFalse(events(e,"g4_profile_hit"))
        e.check()

    def test_15_horn_drive_can_be_resisted_or_blocked(self):
        e,c=setup(front=(3,2))
        out=c.horn_drive("hunter","prey",pressure_face=1,
                         resistance_face=20)
        self.assertEqual(out["outcome"],"resisted")
        self.assertEqual(e.actors["prey"].occupied,((3,2),))
        e2,c2=setup(front=(3,2),walls=((4,2),))
        out2=c2.horn_drive("hunter","prey",pressure_face=18,
                           resistance_face=1)
        self.assertEqual(out2["outcome"],"blocked_destination")
        self.assertEqual(e2.actors["hunter"].occupied,((2,2),(1,2)))
        e2.check()

    def test_16_i3_genuine_two_round_retreat_and_venom(self):
        report=run_i3(seed=791)
        self.assertEqual(report["ending"],"withdrawal_attested")
        self.assertEqual(report["current"]["round"],2)
        self.assertEqual(report["first_bite"]["outcome"],"miss")
        self.assertEqual(report["second_bite"]["outcome"],"hit")
        self.assertEqual(report["second_bite"]["damage"]["venom"]["outcome"],
                         "accepted")
        self.assertEqual(report,run_i3(seed=791))
        self.assertFalse(report["complete_party_pack_certified"])
        self.assertIsNone(report["hunter_cr"])


    def test_17_repeated_normal_bite_ignores_moderate_without_second_save(self):
        e,c=setup(front=(3,2))
        first=c.declare("hunter","prey",profiles=("B06-AT-04",),
                        defenses=("take_hit",))
        accepted=c.resolve(first,0,attack_face=10,damage_face=1,
                           venom_resistance_die=1)
        self.assertEqual(accepted["damage"]["venom"]["outcome"],"accepted")
        old=e.g4.toxins.active("prey")
        original_key,original_markers=old["key"],tuple(old["markers"])
        c.bridge.end_current_turn()
        c.bridge.start_next_turn(RegenerationChoice(hp=2))
        c.bridge.end_current_turn()
        c.bridge.begin_next_round()
        c.bridge.start_next_turn(RegenerationChoice())
        second=c.declare("hunter","prey",profiles=("B06-AT-04",),
                         defenses=("take_hit",))
        # The second bite punctures, but the first Moderate poison owns
        # the one-instance slot. A second resistance d20 is not rolled.
        repeated=c.resolve(second,0,attack_face=10,damage_face=1)
        self.assertEqual(repeated["outcome"],"hit")
        self.assertEqual(repeated["damage"]["venom"],
                         {"outcome":"ignored","active":original_key})
        self.assertEqual(len(events(e,"g44_hunter_accepted")),1)
        self.assertEqual(len(events(e,"g44_hunter_ignored")),1)
        self.assertEqual(tuple(e.g4.toxins.active("prey")["markers"]),
                         original_markers)
        self.assertFalse(c.pending_attack_slots("hunter"))
        e.check()

    def test_18_pounce_ignores_legacy_moderate_hemotoxin_without_save(self):
        e,c=setup()
        e.g4.schedule_hemotoxin(
            "prey",exposure_key="existing-hm",actual_exposure=True,
            resistance_total=10,wound_location_roll=8)
        self.assertEqual(e.g4.short_toxins[0]["key"],"existing-hm")
        result=c.pounce("hunter","prey",((1,0),)*3,
                        attack_face=10,damage_face=1,
                        balance_hunter_face=1,balance_defender_face=20,
                        balance_ability="Strength")
        self.assertEqual(result["bite"],"hit")
        self.assertEqual(result["damage"]["venom"],
                         {"outcome":"ignored","active":"existing-hm"})
        self.assertEqual(result["balance"],"held")
        self.assertEqual(len(events(e,"g44_hunter_accepted")),0)
        self.assertEqual(len(events(e,"g44_hunter_ignored")),1)
        self.assertEqual(len(e.g4.short_toxins),1)
        e.check()

    def test_19_prepared_ward_prevents_bite_without_unused_save(self):
        e,c=setup(front=(3,2))
        c.bridge.end_current_turn()
        c.bridge.start_next_turn(RegenerationChoice())
        ward=e.g4.venom.cast_endurance(
            "prey","prey",profile="Self",mode="ward",
            source_authorized=True,
            source_reference="test:independently_attested_life_prayer")
        self.assertIsNotNone(ward)
        c.bridge.end_current_turn()
        c.bridge.begin_next_round()
        c.bridge.start_next_turn(RegenerationChoice())
        s=c.declare("hunter","prey",profiles=("B06-AT-04",),
                    defenses=("take_hit",))
        result=c.resolve(s,0,attack_face=10,damage_face=1)
        self.assertEqual(result["damage"]["venom"]["outcome"],"prevented")
        self.assertEqual(len(events(e,"g44_ward_intercepted")),1)
        self.assertEqual(len(events(e,"g44_hunter_accepted")),0)
        self.assertFalse(e.g4.venom.effects[ward]["active"])
        e.check()

    def test_20_active_pounce_prone_suspends_crawl_and_requires_stand(self):
        from scripts.b06_encounter_state_v0 import RegenerationChoice
        h=enemy_actor("B06-EN-03","hunter","enemy",
                      occupied=((2,2),(1,2)))
        prey=party_actor("A",3,"prey","party",occupied=((6,2),))
        e=Encounter([h,prey],{"hunter":30,"prey":20},
                    seed=880,scenario="G6-prone-pounce")
        g=GridMovement(e,width=12,height=6)
        e.begin_round()
        e.start_turn("hunter",regen_choice=RegenerationChoice())
        g.start_pounce("hunter","prey")
        for _ in range(3):
            self.assertTrue(g.step("hunter",(1,0)))
        self.assertEqual(g.pounce.steps,3)
        h.conditions.append("Prone")
        before=(h.occupied,h.mp_remaining,h.ap_remaining,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"Standing, not Crawl"):
            g.crawl_step("hunter",(1,0))
        self.assertEqual((h.occupied,h.mp_remaining,h.ap_remaining,len(e.ledger)),
                         before)
        with self.assertRaisesRegex(ValueError,"must Stand"):
            g.pounce_contact()
        self.assertTrue(g.stand("hunter"))
        self.assertEqual(g.pounce.steps,0)
        self.assertEqual(g.pounce.spent_mp,10)  # 6 old + 4 Stand
        self.assertEqual((h.mp_remaining,h.ap_remaining),(14,42))
        self.assertEqual(len(events(e,"g1_pounce_runup_reset")),1)
        with self.assertRaisesRegex(ValueError,"three translated"):
            g.pounce_contact()
        self.assertEqual(h.ap_remaining,42)
        g.pounce_abort()
        self.assertEqual(h.mp_remaining,8)  # Remaining 18-MP Rapid allowance
        e.check()

    def test_21_aborted_pounce_prone_cannot_crawl_using_rapid_pool(self):
        h=enemy_actor("B06-EN-03","hunter","enemy",
                      occupied=((2,2),(1,2)))
        prey=party_actor("A",3,"prey","party",occupied=((6,2),))
        e=Encounter([h,prey],{"hunter":30,"prey":20},
                    seed=881,scenario="G6-prone-rapid")
        g=GridMovement(e,width=12,height=6)
        e.begin_round()
        e.start_turn("hunter",regen_choice=RegenerationChoice())
        g.start_pounce("hunter","prey")
        self.assertTrue(g.step("hunter",(1,0)))
        g.pounce_abort()
        self.assertEqual(h.mp_remaining,16)
        self.assertIn("hunter",g.rapid_heading)
        h.conditions.append("Prone")
        before=(h.occupied,h.mp_remaining,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"Standing, not Crawl"):
            g.crawl_step("hunter",(1,0))
        self.assertEqual((h.occupied,h.mp_remaining,len(e.ledger)),before)
        self.assertTrue(g.stand("hunter"))
        self.assertEqual(h.mp_remaining,12)
        self.assertIn("hunter",g.rapid_heading)
        self.assertTrue(g.step("hunter",(1,0)))
        self.assertEqual(h.mp_remaining,10)
        e.check()

    def test_22_three_new_charge_steps_after_stand_preserve_ap_and_mp(self):
        h=enemy_actor("B06-EN-03","hunter","enemy",
                      occupied=((2,2),(1,2)))
        prey=party_actor("A",3,"prey","party",occupied=((9,2),))
        e=Encounter([h,prey],{"hunter":30,"prey":20},
                    seed=882,scenario="G6-restarted-runup")
        g=GridMovement(e,width=12,height=6)
        e.begin_round()
        e.start_turn("hunter",regen_choice=RegenerationChoice())
        g.start_pounce("hunter","prey")
        for _ in range(3):
            self.assertTrue(g.step("hunter",(1,0)))
        h.conditions.append("Prone")
        self.assertTrue(g.stand("hunter"))
        self.assertEqual((g.pounce.steps,g.pounce.spent_mp),(0,10))
        for i in range(3):
            self.assertTrue(g.step("hunter",(1,0)))
            self.assertEqual(g.pounce.steps,i+1)
        self.assertEqual(g.pounce.spent_mp,16)
        self.assertEqual(h.ap_remaining,42)
        self.assertTrue(g.pounce_contact(defense="take_hit"))
        self.assertEqual(h.ap_remaining,18)
        self.assertEqual(h.mp_remaining,0)
        self.assertEqual(len(events(e,"action_committed")),1)
        self.assertEqual(len(events(e,"g1_pounce_bite_committed")),1)
        e.check()


    def test_23_hunter_rear_and_side_departs_do_not_offer_opportunities(self):
        from scripts.b06_encounter_state_v0 import Response
        # The generic multi-cell reach set contains rear and side cells,
        # but only the anatomical head-forward square has Bite/Horn authority.
        head,rear=(4,2),(3,2)
        for start,direction,eligible in (
                ((2,2),(0,-1),False),  # rear-facing square
                ((4,3),(0,1),False),   # adjacent to Hunter's head side
                ((3,3),(0,1),False),   # adjacent to Hunter's rear side
                ((5,2),(1,0),True)):  # exactly head-forward
            with self.subTest(departure=start):
                h=enemy_actor("B06-EN-03","hunter","enemy",
                              occupied=(head,rear))
                prey=party_actor("A",3,"prey","party",occupied=(start,))
                e=Encounter([h,prey],{"prey":30,"hunter":20},
                            seed=607,scenario="G6-anatomical-threat")
                g=GridMovement(e,width=10,height=6)
                e.begin_round()
                e.start_turn("prey",regen_choice=RegenerationChoice())
                new=((start[0]+direction[0],start[1]+direction[1]),)
                self.assertEqual(start in g.reach("hunter"),True)
                self.assertEqual(g.threatens("hunter",start),eligible)
                self.assertEqual(g._threats("prey",new,False),
                                 ("hunter",) if eligible else ())
                source=Response("hunter","opportunity","real natural attack")
                if eligible:
                    self.assertTrue(g.step("prey",direction,
                                           responses=(source,)))
                    self.assertEqual(h.opportunity_used,1)
                    self.assertFalse(h.reaction_available)
                    self.assertEqual(len(events(e,"g1_movement_opportunity_pending")),1)
                else:
                    before=(prey.occupied,prey.mp_remaining,
                            h.reaction_available,h.opportunity_used,len(e.ledger))
                    with self.assertRaisesRegex(ValueError,"not eligible"):
                        g.step("prey",direction,responses=(source,))
                    self.assertEqual((prey.occupied,prey.mp_remaining,
                                      h.reaction_available,h.opportunity_used,len(e.ledger)),
                                     before)
                    self.assertTrue(g.step("prey",direction))
                    self.assertEqual(h.opportunity_used,0)
                    self.assertTrue(h.reaction_available)
                    self.assertFalse(events(e,"g1_movement_opportunity_pending"))
                e.check()

    def test_24_lethal_pounce_bite_skips_unused_balance_choices(self):
        e,c=setup()
        victim=e.actors["prey"]
        # An already-Dying but not Dead victim remains a legal Take Hit
        # target. This real puncturing Bite reaches the death threshold.
        victim.hp=-victim.hp_max+1
        out=c.pounce("hunter","prey",((1,0),)*3,
                     attack_face=10,damage_face=1)
        self.assertEqual(out["bite"],"hit")
        self.assertTrue(out["damage"]["dead"])
        self.assertTrue(victim.dead)
        self.assertEqual(out["balance"],"not_applicable")
        self.assertFalse(events(e,"g6_pounce_balance"))
        self.assertFalse(events(e,"g6_pounce_prone"))
        self.assertFalse(events(e,"g44_hunter_accepted"))
        self.assertEqual(len(events(e,"g6_pounce_resolved")),1)
        self.assertFalse(c.pending_attack_slots("hunter"))
        e.check()

    def test_25_healthy_pounce_requires_real_balance_dice_before_roll(self):
        e,c=setup()
        receipt=c.begin_pounce("hunter","prey",((1,0),)*3)
        before=(e.actors["prey"].hp,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"Pounce pressure"):
            c.resolve_pounce(receipt,attack_face=1,
                             balance_ability="Strength")
        with self.assertRaisesRegex(UnresolvedDecision,"Pounce resistance"):
            c.resolve_pounce(receipt,attack_face=1,
                             balance_ability="Strength",
                             balance_hunter_face=2)
        self.assertEqual((e.actors["prey"].hp,len(e.ledger)),before)
        self.assertFalse(events(e,"g6_pounce_melee_roll"))
        self.assertEqual(len(c.pending_attack_slots("hunter")),1)
        out=c.resolve_pounce(receipt,attack_face=1,
                             balance_ability="Strength",
                             balance_hunter_face=2,
                             balance_defender_face=20)
        self.assertEqual(out["bite"],"miss")
        self.assertEqual(out["balance"],"held")
        self.assertEqual(len(events(e,"g6_pounce_balance")),1)
        e.check()


    def test_26_horn_drive_third_party_threat_is_unresolved_before_ap(self):
        hunter=enemy_actor("B06-EN-03","hunter","enemy",
                           occupied=((2,2),(1,2)))
        prey=party_actor("A",3,"prey","party",occupied=((3,2),))
        witness=party_actor("B",3,"witness","party",occupied=((0,2),))
        e=Encounter([hunter,prey,witness],
                    {"hunter":30,"prey":20,"witness":10},
                    seed=909,scenario="G6-Horn-Drive-third-party")
        g=GridMovement(e,width=8,height=5)
        SpellState(e)
        DamageState(e)
        e.begin_round()
        c=HunterCombat(e)
        c.bridge.start_next_turn(RegenerationChoice())
        # Hunter head would enter (3,2), rear (2,2), abandoning (1,2).
        # An opposing armed PC can legally threaten that departed rear cell.
        self.assertEqual(g._threats("hunter",((3,2),(2,2)),False),
                         ("witness",))
        before=(hunter.occupied,prey.occupied,witness.occupied,
                hunter.ap_remaining,prey.hp,len(e.ledger),
                witness.reaction_available,witness.opportunity_used)
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "Third-party Movement Opportunities"):
            c.horn_drive("hunter","prey",
                         pressure_face=18,resistance_face=1)
        self.assertEqual((hunter.occupied,prey.occupied,witness.occupied,
                          hunter.ap_remaining,prey.hp,len(e.ledger),
                          witness.reaction_available,witness.opportunity_used),
                         before)
        self.assertFalse(events(e,"g6_horn_drive_committed"))
        self.assertFalse(events(e,"g6_horn_drive_resolved"))
        e.check()

    def test_27_no_horn_drive_advance_does_not_create_phantom_opportunity(self):
        def scenario(*,wall=False):
            hunter=enemy_actor("B06-EN-03","hunter","enemy",
                               occupied=((2,2),(1,2)))
            prey=party_actor("A",3,"prey","party",occupied=((3,2),))
            witness=party_actor("B",3,"witness","party",
                                occupied=((0,2),))
            e=Encounter([hunter,prey,witness],
                        {"hunter":30,"prey":20,"witness":10},
                        seed=910,scenario="G6-Horn-Drive-no-advance")
            GridMovement(e,width=8,height=5,
                         walls=((4,2),) if wall else ())
            SpellState(e)
            DamageState(e)
            e.begin_round()
            c=HunterCombat(e)
            c.bridge.start_next_turn(RegenerationChoice())
            return e,c
        for wall,pressure,resistance,expected in (
                (False,1,20,"resisted"),
                (True,18,1,"blocked_destination")):
            with self.subTest(expected=expected):
                e,c=scenario(wall=wall)
                out=c.horn_drive("hunter","prey",
                                 pressure_face=pressure,
                                 resistance_face=resistance)
                self.assertEqual(out["outcome"],expected)
                self.assertEqual(e.actors["prey"].occupied,((3,2),))
                self.assertEqual(e.actors["hunter"].occupied,
                                 ((2,2),(1,2)))
                self.assertEqual(e.actors["hunter"].ap_remaining,18)
                self.assertTrue(e.actors["witness"].reaction_available)
                self.assertEqual(e.actors["witness"].opportunity_used,0)
                self.assertFalse(events(e,"g1_movement_opportunity_pending"))
                e.check()

    def test_28_pounce_stale_guard_must_not_block_bite(self):
        # Match ordinary G5's post-commit Guard preflight for both
        # removing a readied stance and losing the actual instrument.
        for change in ("ready_guard","guard_instrument"):
            with self.subTest(change=change):
                e,c=setup()
                receipt=c.begin_pounce("hunter","prey",
                                       ((1,0),)*3,defense="guard")
                t=e.actors["prey"]
                original=getattr(t,change)
                self.assertTrue(t.ready_guard)
                self.assertIsNotNone(t.guard_instrument)
                setattr(t,change,False if change=="ready_guard" else None)
                before=(len(e.ledger),t.hp,t.vigor,
                        e.actors["hunter"].ap_remaining,
                        t.guard_remaining)
                with self.assertRaisesRegex(
                        UnresolvedDecision,
                        "Changed Guard requires native defensive fallback"):
                    c.resolve_pounce(
                        receipt,attack_face=2,
                        balance_hunter_face=1,
                        balance_defender_face=20,balance_ability="Strength")
                self.assertEqual((len(e.ledger),t.hp,t.vigor,
                                  e.actors["hunter"].ap_remaining,
                                  t.guard_remaining),before)
                self.assertFalse(events(e,"g6_pounce_melee_roll"))
                self.assertEqual(len(c.pending_attack_slots("hunter")),1)
                setattr(t,change,original)
                result=c.resolve_pounce(
                    receipt,attack_face=1,balance_hunter_face=1,
                    balance_defender_face=20,balance_ability="Strength")
                self.assertEqual(result["bite"],"miss")
                self.assertFalse(c.pending_attack_slots("hunter"))
                e.check()



    def test_29_normal_bite_duplicate_legitimate_toxin_key_preflight_is_atomic(self):
        e,c=setup(front=(3,2))
        sequence=c.declare("hunter","prey",profiles=("B06-AT-04",),
                           defenses=("take_hit",))
        action_index=sequence["actions"][0]
        poison_key=f"g6:bite:{e.seed}:{action_index}"
        # A different genuine TX-HM exposure previously claimed precisely
        # the generated Bite key. G4.4 must reject it BEFORE G4 damages prey.
        e.g4.schedule_hemotoxin(
            "prey",exposure_key=poison_key,actual_exposure=True,
            resistance_total=10,wound_location_roll=8)
        before=(e.actors["prey"].hp,e.actors["prey"].vigor,
                e.actors["hunter"].ap_remaining,len(e.ledger))
        for _ in range(2):
            with self.assertRaisesRegex(ValueError,"unused toxin exposure key"):
                c.resolve(sequence,0,attack_face=10,damage_face=1)
            self.assertEqual((e.actors["prey"].hp,e.actors["prey"].vigor,
                              e.actors["hunter"].ap_remaining,len(e.ledger)),before)
        self.assertEqual(len(c.pending_attack_slots("hunter")),1)
        self.assertFalse(events(e,"g4_profile_hit"))
        self.assertFalse(events(e,"g5_melee_roll"))
        self.assertFalse(events(e,"g45_attested_hit"))
        self.assertFalse(c.bridge.seen_actions)
        self.assertEqual(e.g4.short_toxins[0]["key"],poison_key)
        e.check()

    def test_30_pounce_duplicate_legitimate_toxin_key_preflight_is_atomic(self):
        e,c=setup()
        receipt=c.begin_pounce("hunter","prey",((1,0),)*3)
        action_index=receipt["action_index"]
        poison_key=f"g6:pounce:{e.seed}:{action_index}"
        e.g4.schedule_hemotoxin(
            "prey",exposure_key=poison_key,actual_exposure=True,
            resistance_total=10,wound_location_roll=8)
        before=(e.actors["prey"].hp,e.actors["prey"].vigor,
                e.actors["hunter"].ap_remaining,len(e.ledger))
        for _ in range(2):
            with self.assertRaisesRegex(ValueError,"unused toxin exposure key"):
                c.resolve_pounce(receipt,attack_face=10,damage_face=1,
                                 balance_hunter_face=1,balance_defender_face=20,
                                 balance_ability="Strength")
            self.assertEqual((e.actors["prey"].hp,e.actors["prey"].vigor,
                              e.actors["hunter"].ap_remaining,len(e.ledger)),before)
        self.assertEqual(len(c.pending_attack_slots("hunter")),1)
        self.assertFalse(events(e,"g6_pounce_melee_roll"))
        self.assertFalse(events(e,"g4_profile_hit"))
        self.assertFalse(events(e,"g45_attested_hit"))
        self.assertNotIn(action_index,c.bridge.seen_actions)
        e.check()

    def test_31_stand_checks_rear_and_all_occupied_hunter_cells(self):
        # Each source only needs to threaten ONE cell; sources threatening
        # both are still recorded exactly once and in stable sorted order.
        for positions,expected in (
                ({"rear":(1,2)},("rear",)),
                ({"both":(2,3)},("both",)),
                ({"rear":(1,2),"front":(4,2)},("front","rear"))):
            with self.subTest(positions=positions):
                hunter=enemy_actor("B06-EN-03","hunter","enemy",
                                   occupied=((3,2),(2,2)))
                others=[party_actor("A",3,ident,"party",occupied=(square,))
                        for ident,square in positions.items()]
                ranks={"hunter":30}
                ranks.update({ident:20-i for i,ident in enumerate(positions)})
                e=Encounter([hunter,*others],ranks,seed=901,
                            scenario="G6-Stand-full-footprint-threat")
                g=GridMovement(e,width=8,height=6)
                e.begin_round()
                e.start_turn("hunter",regen_choice=RegenerationChoice())
                hunter.conditions.append("Prone")
                for ident,square in positions.items():
                    self.assertTrue(any(g.threatens(ident,cell)
                                        for cell in hunter.occupied))
                if "rear" in positions:
                    self.assertTrue(g.threatens("rear",hunter.occupied[1]))
                    self.assertFalse(g.threatens("rear",hunter.occupied[0]))
                self.assertTrue(g.stand("hunter"))
                self.assertEqual(events(e,"g6_stand_started")[-1]["detail"]
                                 ["opportunity_sources"],list(expected))
                self.assertEqual(hunter.mp_remaining,8)
                self.assertEqual(len(events(e,"g6_stand_completed")),1)
                e.check()


    def test_32_pounce_strength_pressure_respects_hunter_muscle_toxin(self):
        # A's Strength +2: 11+2=13. Clean Hunter 10+4=14 wins;
        # a real TX-MY -1 makes it 13 vs 13, which holds standing.
        clean,clean_combat=setup()
        clean_result=clean_combat.pounce(
            "hunter","prey",((1,0),)*3,
            attack_face=1,balance_hunter_face=10,
            balance_defender_face=11,balance_ability="Strength")
        self.assertEqual(clean_result["balance"],"prone")
        self.assertEqual(events(clean,"g6_pounce_balance")[-1]["detail"]["pressure"],14)
        clean.check()

        poisoned,combat=setup()
        receipt=combat.begin_pounce("hunter","prey",((1,0),)*3)
        applied=poisoned.g4.toxins.apply(
            "hunter","TX-MY",exposure_key="hunter-muscle-pounce",
            source="test:independently_verified_injection",
            route="injection",delivery_verified=True,
            residual_piercing_hp=1,resistance_die=1)
        self.assertEqual(applied["outcome"],"accepted")
        self.assertEqual(poisoned.g4.toxins.modifier(
            "hunter","muscular_strength"),-1)
        outcome=combat.resolve_pounce(
            receipt,attack_face=1,balance_hunter_face=10,
            balance_defender_face=11,balance_ability="Strength")
        self.assertEqual(outcome["balance"],"held")
        self.assertEqual(events(poisoned,"g6_pounce_balance")[-1]["detail"]["pressure"],13)
        self.assertNotIn("Prone",poisoned.actors["prey"].conditions)
        poisoned.check()

    def test_33_horn_drive_strength_pressure_respects_hunter_muscle_toxin(self):
        # Hunter Strength +4, prey Strength +2 plus Hold Ground +2:
        # clean 10+4=14 beats 9+2+2=13; TX-MY -1 makes a tie.
        clean,clean_combat=setup(front=(3,2))
        first=clean_combat.horn_drive(
            "hunter","prey",pressure_face=10,resistance_face=9)
        self.assertEqual(first["outcome"],"shoved")
        self.assertEqual(events(clean,"g6_horn_drive_resolved")[-1]["detail"]["pressure"],14)
        clean.check()

        poisoned,combat=setup(front=(3,2))
        applied=poisoned.g4.toxins.apply(
            "hunter","TX-MY",exposure_key="hunter-muscle-horn",
            source="test:independently_verified_injection",
            route="injection",delivery_verified=True,
            residual_piercing_hp=1,resistance_die=1)
        self.assertEqual(applied["outcome"],"accepted")
        self.assertEqual(poisoned.g4.toxins.modifier(
            "hunter","muscular_strength"),-1)
        outcome=combat.horn_drive(
            "hunter","prey",pressure_face=10,resistance_face=9)
        self.assertEqual(outcome["outcome"],"resisted")
        self.assertEqual(events(poisoned,"g6_horn_drive_resolved")[-1]["detail"]["pressure"],13)
        self.assertEqual(poisoned.actors["prey"].occupied,((3,2),))
        self.assertEqual(poisoned.actors["hunter"].occupied,((2,2),(1,2)))
        poisoned.check()


if __name__=="__main__":
    unittest.main()
