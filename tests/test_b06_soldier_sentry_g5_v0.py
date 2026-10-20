"""Deterministic G5 I1/I2 source-bound melee and exit integration gates."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision,
    enemy_actor, party_actor)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import (
    SourceMelee, fixed_scene, run_i1, run_i2)


def crossed_scene(*,state="prepared_start"):
    sentry=enemy_actor("B06-EN-01","sentry","party",
                       start_state=state,occupied=((3,2),))
    soldier=enemy_actor("B06-EN-02","soldier","enemy",
                        occupied=((4,2),))
    e=Encounter([sentry,soldier],{"sentry":30,"soldier":20},
                seed=905,scenario="G5-source-cross-benchmark",
                objective="bounded_opposed_witness",policy="declared_dice")
    GridMovement(e,width=8,height=5)
    SpellState(e)
    DamageState(e)
    e.begin_round()
    return e,SourceMelee(e)


class G5SoldierSentryTests(unittest.TestCase):
    def test_01_i1_soldier_guard_and_genuine_exit_terminal(self):
        report=run_i1(seed=7001)
        self.assertEqual(report["seed"],7001)
        self.assertEqual(report["ending"],"withdrawal_attested")
        self.assertEqual(report["i1_first_attack"]["outcome"],"miss")
        self.assertEqual(report["i1_first_attack"]["defense"],"guard")
        self.assertEqual(report["attacks"][0]["profile"],"B06-AT-03")
        self.assertEqual(report["attacks"][0]["outcome"],"miss")
        self.assertEqual(report["current"]["actors"]["front"]["hp"],12)
        self.assertEqual(report["current"]["actors"]["front"]["wounds"],[])
        self.assertEqual(report["current"]["actors"]["front"]["vigor"],36)
        self.assertEqual(report["current"]["actors"]["front"]["source_id"],"A")
        self.assertEqual(report["outcomes"][0]["status"],"withdrawal_attested")
        self.assertFalse(report["complete_party_pack_certified"])
        self.assertIsNone(report["hunter_cr"])
        self.assertEqual(report,run_i1(seed=7001))

    def test_02_i2_cold_pays_projection_then_genuine_enchanted_hit(self):
        report=run_i2(state="cold_start",seed=7002)
        self.assertEqual(report["ending"],"withdrawal_attested")
        self.assertEqual(report["start_state"],"cold_start")
        self.assertEqual(report["i2_first_hit"]["outcome"],"hit")
        self.assertEqual(report["attacks"][0]["profile"],"B06-AT-02")
        self.assertEqual(report["i2_first_hit"]["damage"]["hp_packets"],[7,2])
        self.assertEqual(report["i2_first_hit"]["damage"]["vigor_loss"],2)
        self.assertEqual(report["current"]["actors"]["front"]["hp"],3)
        self.assertEqual(report["current"]["actors"]["front"]["vigor"],34)
        foe=report["current"]["actors"]["foe"]
        self.assertEqual((foe["vp_available"],foe["vp_committed"],
                          foe["vp_spent"]),(3,3,0))
        self.assertEqual(report["current"]["round"],2)
        self.assertEqual(report,run_i2(state="cold_start",seed=7002))

    def test_03_i2_prepared_begins_precommitted_and_attacks_round_one(self):
        report=run_i2(state="prepared_start",seed=7003)
        self.assertEqual(report["start_state"],"prepared_start")
        self.assertEqual(report["ending"],"withdrawal_attested")
        self.assertEqual(report["current"]["round"],1)
        self.assertEqual(report["attacks"][0]["profile"],"B06-AT-02")
        self.assertEqual(report["i2_first_hit"]["damage"]["hp_loss"],9)
        foe=report["current"]["actors"]["foe"]
        self.assertEqual((foe["vp_available"],foe["vp_committed"],
                          foe["vp_spent"]),(3,3,0))
        self.assertEqual(report,run_i2(state="prepared_start",seed=7003))

    def test_04_guard_stops_sentry_sword_without_free_damage(self):
        e,g=crossed_scene()
        g.bridge.start_next_turn(RegenerationChoice())
        seq=g.declare("sentry","soldier",profiles=("B06-AT-02",),
                      defenses=("guard",))
        soldier=e.actors["soldier"]
        self.assertEqual(soldier.guard_remaining,soldier.guard_capacity-1)
        result=g.resolve(seq,0,attack_face=10)
        self.assertEqual(result["outcome"],"miss")
        self.assertEqual(result["defense_value"],18)
        self.assertEqual(result["attack_total"],17)
        self.assertEqual(soldier.hp,12)
        self.assertEqual(soldier.vigor,36)
        self.assertFalse(g.bridge.report()["verified_hits"])
        self.assertEqual(len(g.report()["attacks"]),1)
        e.check()

    def test_05_two_dodges_use_one_sequence_and_real_pressure(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("dodge","dodge"))
        defense_values=[e.ledger[i]["detail"]["defense_value"]
                        for i in seq["defenses"]]
        self.assertEqual(defense_values,[14,12])
        self.assertEqual(e.actors["front"].dodge_pressure,4)
        self.assertEqual(e.actors["foe"].ap_remaining,2)
        first=scene.resolve(seq,0,attack_face=7)
        second=scene.resolve(seq,1,attack_face=7,damage_face=1,vigor_die=4)
        self.assertEqual(first["outcome"],"miss")
        self.assertEqual(second["outcome"],"hit")
        self.assertEqual(second["damage"]["hp_loss"],6)
        self.assertEqual(second["damage"]["vigor_loss"],2)
        self.assertEqual(len(scene.report()["attacks"]),2)
        self.assertEqual(len(scene.bridge.report()["verified_hits"]),1)
        self.assertEqual(e.actors["front"].guard_remaining,
                         e.actors["front"].guard_capacity)
        e.check()

    def test_06_critical_take_hit_confirmed_and_devastating_wound(self):
        for confirmation,expect in ((7,"critical"),(20,"devastating")):
            with self.subTest(confirmation=confirmation):
                scene=fixed_scene("I2",sentry_state="prepared_start")
                e=scene.e
                scene.bridge.start_next_turn(RegenerationChoice())
                seq=scene.declare("foe","front",
                                  profiles=("B06-AT-02",),
                                  defenses=("take_hit",))
                result=scene.resolve(seq,0,attack_face=20,
                                     confirmation_face=confirmation,
                                     critical_dice=(2,3),damage_face=1,
                                     vigor_die=4,
                                     wound_location_roll=14 if confirmation==20
                                     else None)
                self.assertEqual(result["critical"],expect)
                self.assertEqual(result["damage"]["hp_loss"],11)
                self.assertEqual(e.actors["front"].hp,1)
                self.assertEqual(len(e.actors["front"].wounds),
                                 1 if confirmation==20 else 0)
                if confirmation==20:
                    self.assertEqual(e.actors["front"].wounds[0].severity,
                                     "Critical")
                e.check()

    def test_07_natural20_failed_guard_confirmation_is_strong(self):
        scene=fixed_scene("I1")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-03",),defenses=("guard",))
        outcome=scene.resolve(seq,0,attack_face=20,confirmation_face=1,
                              critical_dice=(3,),damage_face=1)
        self.assertEqual(outcome["critical"],"strong")
        self.assertEqual(outcome["damage"]["hp_loss"],7)
        self.assertFalse(e.actors["front"].wounds)
        e.check()

    def test_08_cold_cannot_claim_prepared_damage_or_same_turn_strike(self):
        scene=fixed_scene("I2",sentry_state="cold_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        with self.assertRaisesRegex(ValueError,"Sentry profile"):
            scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        self.assertEqual(e.actors["foe"].ap_remaining,42)
        e.g3.cast_sentry_reserve("foe")
        before=(e.actors["foe"].ap_remaining,
                e.actors["front"].hp,e.actors["foe"].vp_committed)
        with self.assertRaisesRegex(ValueError,"Not enough AP"):
            scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        self.assertEqual((e.actors["foe"].ap_remaining,
                          e.actors["front"].hp,e.actors["foe"].vp_committed),
                         before)
        self.assertEqual(before,(12,12,3))
        self.assertFalse(scene.report()["attacks"])
        e.check()

    def test_09_reserved_interception_blocks_unsupported_resolution(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        e.reserve("foe",f"g5:melee:{seq['actions'][0]}","deferred",
                  action_kind="physical")
        before=(e.actors["front"].hp,len(e.reservations))
        with self.assertRaisesRegex(UnresolvedDecision,"Reserved Interception"):
            scene.resolve(seq,0,attack_face=11,damage_face=4,vigor_die=4)
        self.assertEqual((e.actors["front"].hp,len(e.reservations)),before)
        self.assertEqual(len(scene.report()["attacks"]),0)
        e.check()

    def test_10_attack_contact_preflight_blocks_out_of_reach_without_ap(self):
        scene=fixed_scene("I1")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        # A legally moved distant target cannot be attacked as if adjacent.
        e.actors["front"].occupied=((0,2),)
        before=e.actors["foe"].ap_remaining
        with self.assertRaisesRegex(UnresolvedDecision,"G1 current actual melee contact"):
            scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("take_hit",))
        self.assertEqual(e.actors["foe"].ap_remaining,before)
        self.assertFalse(scene.report()["attacks"])
        e.check()

    def test_11_dying_does_not_implicitly_end_encounter(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        e.actors["front"].hp=9
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        r=scene.resolve(seq,0,attack_face=11,damage_face=4,vigor_die=4,
                        wound_location_roll=9)
        self.assertEqual(r["outcome"],"hit")
        self.assertEqual(e.actors["front"].hp,0)
        self.assertFalse(e.actors["front"].dead)
        self.assertEqual(scene.report()["ending"],"unresolved")
        self.assertEqual(len(e.actors["front"].wounds),1)
        self.assertFalse(scene.report()["complete_party_pack_certified"])
        e.check()

    def test_12_missing_confirm_roll_is_unresolved_before_damage(self):
        scene=fixed_scene("I1")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("take_hit",))
        before=(e.actors["front"].hp,e.actors["foe"].ap_remaining)
        with self.assertRaisesRegex(UnresolvedDecision,"critical confirmation"):
            scene.resolve(seq,0,attack_face=20,damage_face=4,
                          critical_dice=(1,1))
        self.assertEqual((e.actors["front"].hp,
                          e.actors["foe"].ap_remaining),before)
        self.assertFalse(scene.report()["attacks"])
        after=scene.resolve(seq,0,attack_face=20,confirmation_face=7,
                            critical_dice=(1,1),damage_face=4)
        self.assertEqual(after["critical"],"critical")
        e.check()

    def test_13_resolving_same_paid_slot_twice_never_duplicates_damage(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        scene.resolve(seq,0,attack_face=11,damage_face=1,vigor_die=4)
        hp=e.actors["front"].hp
        with self.assertRaisesRegex(ValueError,"already resolved"):
            scene.resolve(seq,0,attack_face=11,damage_face=1,vigor_die=4)
        self.assertEqual(e.actors["front"].hp,hp)
        self.assertEqual(len(scene.report()["attacks"]),1)
        e.check()

    def test_14_guard_instrument_loss_requires_real_fallback_not_implicit_hit(self):
        scene=fixed_scene("I1")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("guard",))
        e.actors["front"].ready_guard=False
        with self.assertRaisesRegex(UnresolvedDecision,"defensive fallback"):
            scene.resolve(seq,0,attack_face=10)
        self.assertEqual(e.actors["front"].hp,12)
        self.assertEqual(len(scene.report()["attacks"]),0)
        e.check()

if __name__=="__main__":
    unittest.main()
