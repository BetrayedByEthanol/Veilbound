"""Native one-slot G6-D Reactive Intervene: Hunter Bite versus A with B protector."""
import unittest

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
from scripts.b06_hunter_reactive_intervene_g6d_v0 import ReactiveHunterProtection


def witness(defense="dodge"):
    combat=mixed_scene(size=4,level=3,seed=654)
    combat.bridge.start_next_turn(RegenerationChoice())
    assert combat.e.current=="hunter"
    sequence=combat.declare("hunter","vanguard",
                            profiles=("B06-AT-04",),defenses=(defense,))
    return combat,ReactiveHunterProtection(combat),sequence


def logged(e,kind):
    return [x for x in e.ledger if x["kind"]==kind]


class ReactiveHunterInterveneTests(unittest.TestCase):
    def test_01_reactive_shield_stops_would_hit_for_one_guard_and_reaction(self):
        combat,protection,seq=witness()
        e=combat.e
        p=e.actors["guardian"]
        guard=p.guard_remaining
        a_hp=e.actors["vanguard"].hp
        r=protection.resolve(seq,protector_id="guardian",method="shield_guard",
                             attack_face=10)
        self.assertEqual(r["outcome"],"shield_stopped")
        self.assertTrue(r["original_hit"])
        self.assertEqual(p.guard_remaining,guard-1)
        self.assertFalse(p.reaction_available)
        self.assertEqual(e.actors["vanguard"].hp,a_hp)
        self.assertFalse(logged(e,"g4_profile_hit"))
        self.assertEqual(len(logged(e,"g6d_protective_bite_attested")),1)
        self.assertEqual(len(logged(e,"g5_melee_resolved")),1)
        self.assertFalse(combat.pending_attack_slots("hunter"))
        e.check()

    def test_02_reactive_body_takes_one_genuine_source_piercing_hit(self):
        combat,protection,seq=witness()
        e=combat.e
        p=e.actors["guardian"]
        ward=e.actors["vanguard"]
        original=(ward.hp,p.hp,p.guard_remaining)
        r=protection.resolve(seq,protector_id="guardian",
                             method="body_take_hit",attack_face=10,
                             damage_face=6,venom_resistance_die=20)
        self.assertEqual(r["outcome"],"body_hit")
        self.assertEqual(r["recipient"],"guardian")
        self.assertEqual((ward.hp,p.hp,p.guard_remaining),
                         (original[0],original[1]-5,original[2]))
        self.assertEqual(r["damage"]["hp_loss"],5)
        self.assertFalse(p.reaction_available)
        self.assertEqual(logged(e,"g4_profile_hit")[0]["detail"]["target"],
                         "guardian")
        self.assertEqual(len(logged(e,"g5_melee_resolved")),1)
        e.check()

    def test_03_reactive_shield_fails_to_stop_higher_attack_total(self):
        combat,protection,seq=witness()
        e=combat.e
        r=protection.resolve(seq,protector_id="guardian",method="shield_guard",
                             attack_face=14,damage_face=4,
                             venom_resistance_die=20)
        self.assertEqual(r["outcome"],"ward_hit")
        self.assertEqual(r["recipient"],"vanguard")
        self.assertEqual(e.actors["vanguard"].hp,12-5)
        self.assertEqual(e.actors["guardian"].guard_remaining,
                         e.actors["guardian"].guard_capacity-1)
        self.assertFalse(e.actors["guardian"].reaction_available)
        e.check()

    def test_04_declared_reaction_spent_even_if_natural_one(self):
        combat,protection,seq=witness()
        e=combat.e
        previous=e.actors["guardian"].guard_remaining
        r=protection.resolve(seq,protector_id="guardian",method="shield_guard",
                             attack_face=1)
        self.assertEqual(r["outcome"],"miss")
        self.assertIsNone(r["damage"])
        self.assertFalse(e.actors["guardian"].reaction_available)
        self.assertEqual(e.actors["guardian"].guard_remaining,previous)
        self.assertEqual(e.actors["vanguard"].hp,12)
        self.assertFalse(logged(e,"g4_damage_applied"))
        e.check()

    def test_05_shield_nat20_single_confirmation_still_hits_ward(self):
        combat,protection,seq=witness()
        e=combat.e
        r=protection.resolve(seq,protector_id="guardian",method="shield_guard",
                             attack_face=20,confirmation_face=1,
                             critical_dice=(2,),damage_face=2,
                             venom_resistance_die=20)
        self.assertEqual(r["outcome"],"ward_hit")
        self.assertEqual(r["critical"],"strong")
        self.assertEqual(r["damage"]["hp_loss"],5)
        self.assertEqual(e.actors["guardian"].guard_remaining,
                         e.actors["guardian"].guard_capacity-1)
        self.assertEqual(len(logged(e,"g5_melee_roll")),1)
        e.check()

    def test_06_body_nat20_confirmation_uses_original_ward_defense(self):
        combat,protection,seq=witness()
        e=combat.e
        r=protection.resolve(seq,protector_id="guardian",method="body_take_hit",
                             attack_face=20,confirmation_face=10,
                             critical_dice=(1,1),damage_face=2,
                             venom_resistance_die=20)
        self.assertEqual(r["outcome"],"body_hit")
        self.assertEqual(r["critical"],"critical")
        self.assertEqual(r["recipient"],"guardian")
        self.assertEqual(r["damage"]["hp_loss"],3)
        self.assertEqual(e.actors["vanguard"].hp,12)
        e.check()

    def test_07_wound_preflight_rejects_before_spending_reaction(self):
        combat,protection,seq=witness()
        e=combat.e
        e.actors["guardian"].hp=2
        before=(len(e.ledger),e.actors["guardian"].reaction_available,
                e.actors["guardian"].guard_remaining)
        with self.assertRaisesRegex(UnresolvedDecision,"wound-location"):
            protection.resolve(seq,protector_id="guardian",
                               method="body_take_hit",attack_face=10,
                               damage_face=6,venom_resistance_die=20)
        self.assertEqual((len(e.ledger),e.actors["guardian"].reaction_available,
                          e.actors["guardian"].guard_remaining),before)
        self.assertFalse(logged(e,"spontaneous_committed"))
        e.check()

    def test_08_invalid_guard_no_reaction_spent_no_guard_debit(self):
        combat,protection,seq=witness()
        e=combat.e
        e.actors["guardian"].guard_remaining=0
        before=(len(e.ledger),e.actors["guardian"].reaction_available)
        with self.assertRaises(ValueError):
            protection.resolve(seq,protector_id="guardian",
                               method="shield_guard",attack_face=10)
        self.assertEqual((len(e.ledger),e.actors["guardian"].reaction_available),
                         before)
        e.check()

    def test_09_unreachable_guardian_may_not_react_across_map(self):
        combat,protection,seq=witness()
        e=combat.e
        e.actors["guardian"].occupied=((6,5),)
        before=len(e.ledger)
        with self.assertRaisesRegex(UnresolvedDecision,"physically cover"):
            protection.resolve(seq,protector_id="guardian",
                               method="body_take_hit",attack_face=10,
                               damage_face=6,venom_resistance_die=20)
        self.assertEqual(len(e.ledger),before)
        self.assertTrue(e.actors["guardian"].reaction_available)

    def test_10_cannot_reuse_original_paid_attack_after_protection(self):
        combat,protection,seq=witness()
        e=combat.e
        r=protection.resolve(seq,protector_id="guardian",
                             method="shield_guard",attack_face=10)
        self.assertEqual(r["outcome"],"shield_stopped")
        with self.assertRaises((ValueError,UnresolvedDecision)):
            combat.resolve(seq,0,attack_face=10,damage_face=2)
        with self.assertRaises((ValueError,UnresolvedDecision)):
            protection.resolve(seq,protector_id="guardian",
                               method="shield_guard",attack_face=10)
        self.assertEqual(len(logged(e,"g5_melee_resolved")),1)
        combat.bridge.end_current_turn()
        e.check()


if __name__=="__main__":
    unittest.main()
