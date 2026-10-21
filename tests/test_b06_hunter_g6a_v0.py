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
                     venom_resistance_die=1,
                     balance_hunter_face=1,balance_defender_face=20,
                     balance_ability="Agility")
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


if __name__=="__main__":
    unittest.main()
