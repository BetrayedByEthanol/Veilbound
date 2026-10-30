"""B05 actual Low Gifted Rooted Guard / Unbound Step G0/G1/G2/G5 bridge."""
import unittest

from scripts.b05_low_gifted_native_anchor_v0 import (
    LowGiftedNativeAnchor,actual_sword_ready,SOURCE_ROLE,
)
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,party_actor,enemy_actor,UnresolvedDecision,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee


def scene(level,*,anchor="Fear",first="foe",terrain=None,attached=True):
    actor=party_actor("GL",level,"gifted","party",occupied=((2,2),))
    foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    e=Encounter([actor,foe],{
        first:40,("gifted" if first=="foe" else "foe"):30
    },seed=17,scenario="B05-Low-Gifted-Native-Anchor-Policy",
      policy="explicit_choice",objective="one_legitimate_defense_or_paid_step")
    GridMovement(e,width=8,height=8,terrain=terrain or {},
                 scene_id="b05-low-gifted-one-square")
    RangedCombat(e,scene_id="b05-low-gifted-g2-wielded")
    SpellState(e)
    DamageState(e)
    native=(LowGiftedNativeAnchor(e,"gifted",anchor=anchor)
            if attached else None)
    combat=SourceMelee(e)
    e.begin_round()
    return e,native,combat


def enemy_attack(e,combat,*,choice="guard",face=12):
    seq=combat.declare("foe","gifted",profiles=("B06-AT-03",),
                       defenses=(choice,))
    r=combat.resolve(seq,0,attack_face=face,
                     damage_face=2 if choice=="take_hit" else None,
                     wound_location_roll=8 if choice=="take_hit" else None)
    return r,seq


class NativeLowGiftedAnchorTests(unittest.TestCase):
    def test_01_source_actor_exact_and_native_source_attached_precombat(self):
        for level in (1,2,3):
            e,native,_=scene(level)
            a=e.actors["gifted"]
            self.assertEqual((a.source.source_id,a.level,a.focus),
                             (SOURCE_ROLE,level,"Low"))
            self.assertEqual(a.guard_value,17)
            self.assertEqual(a.guard_capacity,(1,2,3)[level-1])
            self.assertEqual(a.source.digest,native._source().source.digest)
            self.assertTrue(actual_sword_ready(e,"gifted"))
            self.assertEqual((native.model.anchor,native.model.active,
                              native.model.window),("Fear","Fear",1))
            self.assertFalse(any(x["kind"]=="b05_low_gifted_unbound_step_applied"
                                 for x in e.ledger))

    def test_02_genuine_g0_guard_plus_one_changes_source_g5_hit_to_miss(self):
        for level in (1,2,3):
            with self.subTest(level=level):
                e,native,combat=scene(level)
                combat.bridge.start_next_turn(RegenerationChoice())
                native.choose_defense("foe:gifted:0","guard")
                result,_=enemy_attack(e,combat,choice="guard",face=12)
                defense=next(x for x in e.ledger if x["kind"]=="defense_assigned")
                self.assertEqual((17,1,18),(
                    e.actors["gifted"].guard_value,
                    defense["detail"]["anchor_bonus"],
                    defense["detail"]["defense_value"]))
                self.assertEqual("miss",result["outcome"])
                self.assertEqual((1,level==1),(
                    native.model.pulse_window,
                    e.actors["gifted"].guard_remaining==0))
                self.assertEqual(1,len([x for x in e.ledger
                    if x["kind"]=="g5_melee_resolved"]))
                self.assertNotIn("g4_damage_applied",[x["kind"] for x in e.ledger])

    def test_03_unselected_guard_keeps_normal_17_and_hit(self):
        e,native,combat=scene(2)
        combat.bridge.start_next_turn(RegenerationChoice())
        # Without an explicitly precommitted Anchor choice, ordinary Guard.
        seq=combat.declare("foe","gifted",profiles=("B06-AT-03",),
                           defenses=("guard",))
        result=combat.resolve(seq,0,attack_face=12,damage_face=2,
                              wound_location_roll=8)
        defense=next(x for x in e.ledger if x["kind"]=="defense_assigned")
        self.assertEqual(17,defense["detail"]["defense_value"])
        self.assertNotIn("anchor_bonus",defense["detail"])
        self.assertEqual("hit",result["outcome"])
        self.assertIsNone(native.model.pulse_window)

    def test_04_dodge_only_receives_one_plus_one_from_l2(self):
        for level in (1,2,3):
            e,native,combat=scene(level)
            combat.bridge.start_next_turn(RegenerationChoice())
            if level==1:
                with self.assertRaises(ValueError):
                    native.choose_defense("foe:gifted:0","dodge")
                continue
            native.choose_defense("foe:gifted:0","dodge")
            seq=combat.declare("foe","gifted",profiles=("B06-AT-03",),
                               defenses=("dodge",))
            event=next(x for x in e.ledger if x["kind"]=="defense_assigned")
            self.assertEqual(15,event["detail"]["defense_value"])
            self.assertEqual(2,event["detail"]["dodge_pressure"])
            result=combat.resolve(seq,0,attack_face=9)
            self.assertEqual("miss",result["outcome"])
            self.assertEqual(1,native.model.pulse_window)

    def test_05_wrong_key_or_wrong_defense_never_mints_bonus(self):
        e,native,combat=scene(2)
        combat.bridge.start_next_turn(RegenerationChoice())
        native.choose_defense("foe:gifted:OTHER","guard")
        seq=combat.declare("foe","gifted",profiles=("B06-AT-03",),
                           defenses=("guard",))
        self.assertEqual(17,next(x for x in e.ledger
            if x["kind"]=="defense_assigned")["detail"]["defense_value"])
        self.assertIsNone(native.model.pulse_window)
        combat.resolve(seq,0,attack_face=1)
        self.assertIsNone(native.model.pulse_window)

    def test_06_missing_g2_or_wrong_source_does_not_grant_guard(self):
        e,native,combat=scene(2)
        combat.bridge.start_next_turn(RegenerationChoice())
        native.choose_defense("foe:gifted:0","guard")
        e.g2.wielded["gifted"].clear()
        with self.assertRaises(ValueError):
            combat.declare("foe","gifted",profiles=("B06-AT-03",),
                           defenses=("guard",))
        self.assertIsNone(native.model.pulse_window)
        self.assertEqual(2,e.actors["gifted"].guard_remaining)
        self.assertEqual(0,len([x for x in e.ledger if x["kind"]=="action_committed"
                                 and x["detail"].get("actor")=="foe"]))

    def test_07_actual_paid_difficult_step_cost_saves_one_mp(self):
        for level in (1,2,3):
            e,native,combat=scene(level,first="gifted",anchor="Disgust",
                                  terrain={(2,3):"difficult",(2,4):"difficult"})
            combat.bridge.start_next_turn(RegenerationChoice())
            before=e.actors["gifted"].mp_remaining
            native.choose_step((0,1))
            self.assertTrue(e.g1.step("gifted",(0,1)))
            steps=[x for x in e.ledger if x["kind"]=="g1_movement_step"]
            self.assertEqual(1,len(steps))
            self.assertEqual((4,3,1),(
                steps[0]["detail"]["source_cost"],steps[0]["detail"]["cost"],
                steps[0]["detail"]["anchor_mp_saved"]))
            self.assertEqual(before-3,e.actors["gifted"].mp_remaining)
            effects=[x for x in e.ledger if x["kind"]==
                     "b05_low_gifted_unbound_step_applied"]
            self.assertEqual(1,len(effects))
            self.assertEqual(steps[0]["index"],effects[0]["detail"]["g1_movement_index"])
            self.assertEqual(1,native.model.pulse_window)
            self.assertTrue(e.g1.step("gifted",(0,1)))
            self.assertEqual(4,steps[0]["detail"]["source_cost"])
            self.assertEqual(5,e.actors["gifted"].mp_remaining) # 12-3-4
            self.assertEqual(1,len([x for x in e.ledger if x["kind"]==
                                    "b05_low_gifted_unbound_step_applied"]))

    def test_08_l2_cautious_widening_and_l1_rejection(self):
        for level in (1,2,3):
            e,native,combat=scene(level,first="gifted",anchor="Disgust")
            combat.bridge.start_next_turn(RegenerationChoice())
            if level==1:
                with self.assertRaises(ValueError):
                    native.choose_step((0,1),cautious=True)
                continue
            native.choose_step((0,1),cautious=True)
            self.assertTrue(e.g1.step("gifted",(0,1),cautious=True))
            step=[x for x in e.ledger if x["kind"]=="g1_movement_step"][0]
            self.assertEqual((4,3,1),(step["detail"]["source_cost"],
                                      step["detail"]["cost"],
                                      step["detail"]["anchor_mp_saved"]))
            self.assertEqual(9,e.actors["gifted"].mp_remaining)

    def test_09_nonpaying_ordinary_step_does_not_spend_pulse(self):
        e,native,combat=scene(1,first="gifted",anchor="Disgust")
        combat.bridge.start_next_turn(RegenerationChoice())
        native.choose_step((0,1))
        self.assertTrue(e.g1.step("gifted",(0,1)))
        self.assertIsNone(native.model.pulse_window)
        self.assertIsNone(native.step_choice)
        self.assertEqual(10,e.actors["gifted"].mp_remaining)
        self.assertFalse(any(x["kind"]=="b05_low_gifted_unbound_step_applied"
                             for x in e.ledger))

    def test_10_false_player_authority_and_duplicate_pulse_rejected(self):
        e,native,combat=scene(2,first="gifted",anchor="Disgust",
                              terrain={(2,3):"difficult"})
        combat.bridge.start_next_turn(RegenerationChoice())
        with self.assertRaises(ValueError):native.choose_step((0,0))
        with self.assertRaises(ValueError):native.choose_defense("", "guard")
        native.choose_step((0,1))
        with self.assertRaises(ValueError):native.choose_step((0,1))
        self.assertTrue(e.g1.step("gifted",(0,1)))
        self.assertEqual(1,native.model.pulse_window)
        with self.assertRaises(ValueError):native.choose_step((0,1))
        self.assertFalse(native.model._ready("Disgust"))
        with self.assertRaises(UnresolvedDecision):
            LowGiftedNativeAnchor(e,"gifted",anchor="Fear")

    def test_11_g0_subsequent_step_refreshes_only_new_real_emotion_window(self):
        e,native,combat=scene(3,first="gifted",anchor="Disgust",
                              terrain={(2,3):"difficult"})
        combat.bridge.start_next_turn(RegenerationChoice())
        native.choose_step((0,1))
        self.assertTrue(e.g1.step("gifted",(0,1)))
        self.assertEqual((1,1),(native.model.window,native.model.pulse_window))
        combat.bridge.end_current_turn()
        combat.bridge.start_next_turn(RegenerationChoice())
        combat.bridge.end_current_turn()
        combat.bridge.begin_next_round()
        combat.bridge.start_next_turn(RegenerationChoice())
        self.assertEqual((2,1),(native.model.window,native.model.pulse_window))
        self.assertTrue(native.model._ready("Disgust"))
        self.assertFalse(native.model.disrupted)
        self.assertEqual(2,native.own_steps)


    def test_12_public_preview_cannot_forge_a_second_native_pulse_or_step(self):
        e,native,combat=scene(3,first="gifted",anchor="Disgust",
                              terrain={(2,3):"difficult",(2,4):"difficult"})
        combat.bridge.start_next_turn(RegenerationChoice())
        native.choose_step((0,1))
        self.assertTrue(e.g1.step("gifted",(0,1)))
        self.assertEqual(1,len([x for x in e.ledger if x["kind"]==
                                 "b05_low_gifted_unbound_step_applied"]))
        # The old isolated design object is mutable and must not be
        # accepted as a new G0 Emotion Establishment or a cleared receipt.
        native.model.pulse_window=None
        with self.assertRaises(ValueError):
            native.choose_step((0,1))
        native.model.begin_window()
        with self.assertRaises(ValueError):
            native.choose_step((0,1))
        # Even corrupting the adapter's public counter cannot impersonate
        # an absent second G0 Step: native ledger receipts are authoritative.
        native.own_steps=2
        with self.assertRaises(ValueError):
            native.choose_step((0,1))
        native.own_steps=1
        with self.assertRaises(UnresolvedDecision):
            native.on_own_step_completed()
        self.assertTrue(e.g1.step("gifted",(0,1)))
        self.assertEqual(1,len([x for x in e.ledger if x["kind"]==
                                 "b05_low_gifted_unbound_step_applied"]))


if __name__=="__main__":
    unittest.main()
