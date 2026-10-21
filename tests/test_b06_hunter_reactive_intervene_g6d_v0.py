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


def prepared_on_guardian_turn(*,method="shield_guard"):
    """Live named MP promise while B's actual first own turn is open."""
    combat=mixed_scene(size=4,level=3,seed=655)
    e=combat.e
    protector=ReactiveHunterProtection(combat)
    combat.bridge.start_next_turn(RegenerationChoice())
    original=combat.declare(
        "hunter","vanguard",profiles=("B06-AT-04",),defenses=("guard",))
    combat.resolve(original,0,attack_face=1)
    combat.bridge.end_current_turn()
    combat.bridge.start_next_turn(RegenerationChoice())
    combat.bridge.end_current_turn()
    combat.bridge.start_next_turn(RegenerationChoice())
    assert e.current=="guardian"
    assert e.g1.step("guardian",(1,0),responses=())
    label=protector.prepare(
        "guardian","vanguard",method=method,delta=(-1,0),
        trigger_key="g6d:prepared:hunter:vanguard:next_bite")
    return combat,protector,label


def prepared_witness(*,method="shield_guard"):
    """One actually reserved B own-turn MP step, released next Hunter turn."""
    combat,protector,label=prepared_on_guardian_turn(method=method)
    e=combat.e
    combat.bridge.end_current_turn()
    for ident in ("archer","scholar"):
        combat.bridge.start_next_turn(RegenerationChoice())
        assert e.current==ident
        combat.bridge.end_current_turn()
    combat.bridge.begin_next_round()
    combat.bridge.start_next_turn(RegenerationChoice())
    assert e.current=="hunter"
    seq=combat.declare(
        "hunter","vanguard",profiles=("B06-AT-04",),defenses=("dodge",))
    return combat,protector,seq,label


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


    def test_11_prepared_shield_releases_real_mp_and_preserves_reaction(self):
        combat,protect,seq,label=prepared_witness()
        e=combat.e
        p=e.actors["guardian"]
        self.assertTrue(p.reaction_available)
        before_guard=p.guard_remaining
        before_mp=p.mp_remaining
        self.assertEqual(p.occupied,((4,3),))
        r=protect.resolve(seq,protector_id="guardian",
                          method="shield_guard",prepared_label=label,
                          attack_face=10)
        self.assertEqual(r["outcome"],"shield_stopped")
        self.assertIsNone(r["reaction_index"])
        self.assertIsNotNone(r["interception_index"])
        self.assertTrue(p.reaction_available)
        self.assertEqual(p.guard_remaining,before_guard-1)
        self.assertEqual(p.mp_remaining,before_mp)
        self.assertEqual(p.occupied,((3,3),))
        self.assertEqual(len(logged(e,"g1_movement_step")
                             ),2)
        self.assertEqual(len(logged(e,"interception_released")),1)
        att=logged(e,"g6d_protective_bite_attested")[-1]["detail"]
        self.assertEqual(att["activation"],"prepared")
        self.assertIsNone(att["reaction_index"])
        self.assertEqual(att["interception_index"],r["interception_index"])
        self.assertFalse(combat.pending_attack_slots("hunter"))
        e.check()

    def test_12_prepared_body_receives_real_bite_without_spending_reaction(self):
        combat,protect,seq,label=prepared_witness(method="body_take_hit")
        e=combat.e
        p=e.actors["guardian"]
        before=(e.actors["vanguard"].hp,p.hp,p.guard_remaining)
        r=protect.resolve(seq,protector_id="guardian",
                          method="body_take_hit",prepared_label=label,
                          attack_face=10,damage_face=6,
                          venom_resistance_die=20)
        self.assertEqual(r["outcome"],"body_hit")
        self.assertEqual(r["recipient"],"guardian")
        self.assertEqual((e.actors["vanguard"].hp,p.hp,p.guard_remaining),
                         (before[0],before[1]-5,before[2]))
        self.assertTrue(p.reaction_available)
        self.assertIsNotNone(r["interception_index"])
        self.assertIsNone(r["reaction_index"])
        self.assertEqual(len(logged(e,"g4_profile_hit")),1)
        e.check()

    def test_13_prepared_binding_rejects_wrong_method_before_mp_release(self):
        combat,protect,seq,label=prepared_witness()
        e=combat.e
        before=(len(e.ledger),e.actors["guardian"].occupied,
                len(e.reservations),e.actors["guardian"].reaction_available)
        with self.assertRaisesRegex(UnresolvedDecision,"changed ward/method"):
            protect.resolve(seq,protector_id="guardian",
                            method="body_take_hit",prepared_label=label,
                            attack_face=10,damage_face=6,
                            venom_resistance_die=20)
        self.assertEqual((len(e.ledger),e.actors["guardian"].occupied,
                          len(e.reservations),
                          e.actors["guardian"].reaction_available),before)
        self.assertFalse(logged(e,"interception_released"))
        e.check()

    def test_14_prepared_without_authentic_reservation_cannot_spend_mp(self):
        combat,protect,seq,label=prepared_witness()
        e=combat.e
        before=(len(e.ledger),e.actors["guardian"].occupied,
                len(e.reservations))
        with self.assertRaisesRegex(UnresolvedDecision,"genuine prior"):
            protect.resolve(seq,protector_id="guardian",
                            method="shield_guard",
                            prepared_label="G1-MP:999:forged",
                            attack_face=10)
        self.assertEqual((len(e.ledger),e.actors["guardian"].occupied,
                          len(e.reservations)),before)
        e.check()

    def test_15_illegal_prepared_route_rejected_before_reservation_spend(self):
        combat=mixed_scene(size=4,level=3,seed=656)
        e=combat.e
        protect=ReactiveHunterProtection(combat)
        for ident in ("hunter","vanguard"):
            combat.bridge.start_next_turn(RegenerationChoice())
            combat.bridge.end_current_turn()
        combat.bridge.start_next_turn(RegenerationChoice())
        p=e.actors["guardian"]
        before=(p.mp_remaining,len(e.reservations),len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"physically cover"):
            protect.prepare(
                "guardian","vanguard",method="shield_guard",
                delta=(1,0),
                trigger_key="g6d:prepared:hunter:vanguard:next_bite")
        self.assertEqual((p.mp_remaining,len(e.reservations),len(e.ledger)),
                         before)
        e.check()


    def test_16_expired_prepared_offer_rearms_same_trigger_with_fresh_mp(self):
        combat,protect,old_label=prepared_on_guardian_turn()
        e=combat.e
        trigger="g6d:prepared:hunter:vanguard:next_bite"
        p=e.actors["guardian"]
        self.assertIn(old_label,protect.prepared)
        self.assertIn(old_label,e.g1.motion)
        original=next(r for r in e.reservations if r.label==old_label)
        self.assertEqual(original.trigger_key,trigger)
        combat.bridge.end_current_turn()
        for ident in ("archer","scholar"):
            combat.bridge.start_next_turn(RegenerationChoice())
            combat.bridge.end_current_turn()
        combat.bridge.begin_next_round()
        # No intervening Bite: this MP reservation has *not* fired.
        for ident in ("hunter","vanguard"):
            combat.bridge.start_next_turn(RegenerationChoice())
            combat.bridge.end_current_turn()
        combat.bridge.start_next_turn(RegenerationChoice())
        self.assertEqual(e.current,"guardian")
        self.assertNotIn(old_label,e.g1.motion)
        self.assertFalse(any(r.label==old_label for r in e.reservations))
        self.assertEqual(len([v for v in logged(e,"g1_reserved_mp_expired")
                              if v["detail"]["label"]==old_label]),1)
        # G0/G1 expired native commitments, but only G6-D owns this
        # local offer registry. It must be pruned before the duplicate gate.
        self.assertIn(old_label,protect.prepared)
        previous_mp=p.mp_remaining
        new_label=protect.prepare(
            "guardian","vanguard",method="shield_guard",delta=(-1,0),
            trigger_key=trigger)
        self.assertNotEqual(old_label,new_label)
        self.assertNotIn(old_label,protect.prepared)
        self.assertEqual(set(protect.prepared),{new_label})
        self.assertIn(new_label,e.g1.motion)
        self.assertEqual(p.mp_remaining,previous_mp-2)
        self.assertEqual(len([r for r in e.reservations
                              if r.trigger_key==trigger]),1)
        e.check()

    def test_17_live_duplicate_remains_rejected_without_second_mp_commit(self):
        combat,protect,label=prepared_on_guardian_turn()
        e=combat.e
        p=e.actors["guardian"]
        before=(p.mp_remaining,len(e.ledger),tuple(e.reservations),
                tuple(e.g1.motion),tuple(protect.prepared))
        with self.assertRaisesRegex(ValueError,"One pending prepared"):
            protect.prepare(
                "guardian","vanguard",method="body_take_hit",delta=(-1,0),
                trigger_key="g6d:prepared:hunter:vanguard:next_bite")
        self.assertEqual((p.mp_remaining,len(e.ledger),tuple(e.reservations),
                          tuple(e.g1.motion),tuple(protect.prepared)),before)
        self.assertIn(label,e.g1.motion)
        e.check()

    def test_18_expired_label_cannot_replace_fresh_prepared_authority(self):
        combat,protect,old=prepared_on_guardian_turn()
        e=combat.e
        combat.bridge.end_current_turn()
        for ident in ("archer","scholar"):
            combat.bridge.start_next_turn(RegenerationChoice())
            combat.bridge.end_current_turn()
        combat.bridge.begin_next_round()
        for ident in ("hunter","vanguard"):
            combat.bridge.start_next_turn(RegenerationChoice())
            combat.bridge.end_current_turn()
        combat.bridge.start_next_turn(RegenerationChoice())
        new=protect.prepare("guardian","vanguard",method="shield_guard",
                             delta=(-1,0),
                             trigger_key="g6d:prepared:hunter:vanguard:next_bite")
        combat.bridge.end_current_turn()
        for ident in ("archer","scholar"):
            combat.bridge.start_next_turn(RegenerationChoice())
            combat.bridge.end_current_turn()
        combat.bridge.begin_next_round()
        combat.bridge.start_next_turn(RegenerationChoice())
        seq=combat.declare("hunter","vanguard",
                           profiles=("B06-AT-04",),defenses=("dodge",))
        snapshot=(len(e.ledger),e.actors["guardian"].occupied,
                  tuple(e.reservations),tuple(e.g1.motion))
        with self.assertRaisesRegex(UnresolvedDecision,"genuine prior"):
            protect.resolve(seq,protector_id="guardian",method="shield_guard",
                            prepared_label=old,attack_face=10)
        self.assertEqual((len(e.ledger),e.actors["guardian"].occupied,
                          tuple(e.reservations),tuple(e.g1.motion)),snapshot)
        self.assertIn(new,protect.prepared)
        actual=protect.resolve(seq,protector_id="guardian",
                               method="shield_guard",
                               prepared_label=new,attack_face=10)
        self.assertEqual(actual["outcome"],"shield_stopped")
        self.assertIsNotNone(actual["interception_index"])
        self.assertFalse(logged(e,"spontaneous_committed"))
        e.check()


if __name__=="__main__":
    unittest.main()
