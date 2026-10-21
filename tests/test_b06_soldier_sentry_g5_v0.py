"""Deterministic G5 I1/I2 source-bound melee and exit integration gates."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision,
    enemy_actor, party_actor)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState, DamagePacket
from scripts.b06_soldier_sentry_g5_v0 import (
    SourceMelee, SceneExit, fixed_scene, run_i1, run_i2)


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

    def test_15_confirmation_natural_one_fails_with_dodge_below_attack_bonus(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        # A fifth native Dodge has Defense 6, below the Sentry's +7.
        for i in range(4):
            e.defense("front","dodge",attack_key=f"pressure:{i}")
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("dodge",))
        self.assertEqual(e.ledger[seq["defenses"][0]]["detail"]["defense_value"],6)
        r=scene.resolve(seq,0,attack_face=20,confirmation_face=1,
                        critical_dice=(3,),damage_face=1,vigor_die=4)
        self.assertEqual(r["outcome"],"hit")
        self.assertEqual(r["critical"],"strong")
        self.assertEqual(r["damage"]["hp_loss"],9)
        self.assertFalse(e.actors["front"].wounds)
        self.assertEqual(scene.report()["attacks"][0]["critical"],"strong")
        e.check()

    def test_16_confirmation_two_still_succeeds_above_low_dodge(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        for i in range(4):
            e.defense("front","dodge",attack_key=f"pressure:{i}")
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("dodge",))
        self.assertEqual(e.ledger[seq["defenses"][0]]["detail"]["defense_value"],6)
        r=scene.resolve(seq,0,attack_face=20,confirmation_face=2,
                        critical_dice=(3,4),damage_face=1,vigor_die=4,
                        wound_location_roll=14)
        self.assertEqual(r["outcome"],"hit")
        self.assertEqual(r["critical"],"critical")
        self.assertEqual(r["damage"]["hp_loss"],13)
        self.assertEqual(len(e.actors["front"].wounds),1)
        e.check()

    def test_17_cannot_relabel_interior_step_as_withdrawal(self):
        scene=fixed_scene("I1")
        e=scene.e
        self.assertEqual(scene.scene_exit.square,(0,2))
        self.assertEqual(scene.scene_exit.policy_id,
                         "G5:open-corridor:exit-front")
        scene.bridge.start_next_turn(RegenerationChoice())
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(e.g1.step("front",(-1,0),responses=lambda _:()))
        self.assertEqual(e.actors["front"].occupied,((1,2),))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "has not reached scene-authored exit"):
            scene.withdraw("front")
        with self.assertRaises(TypeError):
            scene.withdraw("front",exit_square=(1,2),
                           policy_id="fabricated-exit")
        self.assertEqual(scene.report()["ending"],"unresolved")
        self.assertTrue(e.g1.step("front",(-1,0),responses=lambda _:()))
        with self.assertRaisesRegex(UnresolvedDecision,"Actor does not match"):
            scene.withdraw("foe")
        outcome=scene.withdraw("front")
        self.assertEqual(outcome["status"],"withdrawal_attested")
        self.assertEqual(scene.report()["ending"],"withdrawal_attested")
        terminal=[x["detail"] for x in e.ledger if x["kind"]=="g5_terminal_exit"]
        self.assertEqual(len(terminal),1)
        self.assertEqual(terminal[0]["at"],[0,2])
        self.assertEqual(terminal[0]["policy"],scene.scene_exit.policy_id)
        with self.assertRaisesRegex(ValueError,"already attested"):
            scene.withdraw("front")
        e.check()

    def test_18_generic_scene_without_authored_exit_cannot_withdraw(self):
        e,scene=crossed_scene()
        scene.bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(e.g1.step("sentry",(-1,0),responses=lambda _:()))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "No scene-authored exit policy"):
            scene.withdraw("sentry")
        self.assertEqual(scene.report()["ending"],"unresolved")
        self.assertFalse([x for x in e.ledger if x["kind"]=="g5_terminal_exit"])
        e.check()

    def test_19_reject_malformed_or_interior_scene_exit_contract(self):
        e,scene=crossed_scene()
        before=len(e.ledger)
        wrongs=(
            SceneExit(e.scenario,e.g1.scene_id,e.objective,
                      "sentry",(2,2),"G5:pretend"),
            SceneExit("different",e.g1.scene_id,e.objective,
                      "sentry",(0,2),"G5:pretend"),
            SceneExit(e.scenario,e.g1.scene_id,"other-objective",
                      "sentry",(0,2),"G5:pretend"),
            SceneExit(e.scenario,e.g1.scene_id,e.objective,
                      "unknown",(0,2),"G5:pretend"),
        )
        for entry in wrongs:
            with self.subTest(entry=entry):
                with self.assertRaisesRegex(ValueError,
                                            "Scene exit must match source scene"):
                    SourceMelee(e,scene_exit=entry)
        self.assertEqual(len(e.ledger),before)
        self.assertIsNone(scene.scene_exit)
        e.check()


    def test_20_stale_sequence_miss_rejected_after_turn_and_round_refresh(self):
        scene=fixed_scene("I1")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        stale=scene.declare("foe","front",profiles=("B06-AT-03",),
                            defenses=("guard",))
        self.assertEqual(e.ledger[stale["declaration"]]["round"],1)
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        scene.bridge.end_current_turn()
        scene.bridge.begin_next_round()
        scene.bridge.start_next_turn(RegenerationChoice())
        self.assertEqual((e.round,e.current),(2,"foe"))
        before=(e.actors["front"].hp,e.actors["front"].guard_remaining,
                e.actors["foe"].ap_remaining,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "must belong to current round and turn"):
            scene.resolve(stale,0,attack_face=1)
        self.assertEqual(
            (e.actors["front"].hp,e.actors["front"].guard_remaining,
             e.actors["foe"].ap_remaining,len(e.ledger)),before)
        self.assertFalse([x for x in e.ledger if x["kind"]=="g5_melee_resolved"])
        self.assertFalse([x for x in e.ledger if x["kind"]=="g5_melee_roll"])
        # Failure must not consume this round's real AP. A newly declared
        # sequence CAN legally produce the same natural-one miss now.
        fresh=scene.declare("foe","front",profiles=("B06-AT-03",),
                            defenses=("guard",))
        r=scene.resolve(fresh,0,attack_face=1)
        self.assertEqual(r["outcome"],"miss")
        self.assertEqual(e.ledger[fresh["declaration"]]["round"],2)
        self.assertEqual(len(scene.report()["attacks"]),1)
        self.assertEqual(e.actors["front"].hp,12)
        e.check()

    def test_21_swapped_dodges_cannot_reverse_precommitted_pressure(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("dodge","dodge"))
        original_indices=seq["defenses"]
        self.assertEqual(
            [e.ledger[i]["detail"]["defense_value"] for i in original_indices],
            [14,12])
        self.assertEqual(
            [e.ledger[i]["detail"]["attack_key"] for i in original_indices],
            ["foe:front:0","foe:front:1"])
        tampered=dict(seq)
        tampered["defenses"]=tuple(reversed(original_indices))
        before=(e.actors["front"].hp,e.actors["front"].vigor,
                e.actors["front"].dodge_pressure,
                e.actors["foe"].ap_remaining,len(e.ledger))
        # Face 6 + Sentry bonus 7 = 13: legitimate slot 0 MISSES
        # Dodge14, while wrong swapped Dodge12 would falsely deal damage.
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "assigned defense event does not match declared slot"):
            scene.resolve(tampered,0,attack_face=6,damage_face=1,vigor_die=4)
        # Slot 1 is not yet legal even before validating its swapped
        # defense: declared order requires slot 0 to be final first.
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "Resolve or lose earlier declared attack slots first"):
            scene.resolve(tampered,1,attack_face=6,damage_face=1,vigor_die=4)
        self.assertEqual(
            (e.actors["front"].hp,e.actors["front"].vigor,
             e.actors["front"].dodge_pressure,
             e.actors["foe"].ap_remaining,len(e.ledger)),before)
        self.assertFalse(scene.report()["attacks"])
        first=scene.resolve(seq,0,attack_face=6)
        second=scene.resolve(seq,1,attack_face=6,damage_face=1,vigor_die=4)
        self.assertEqual(first["outcome"],"miss")
        self.assertEqual(first["defense_value"],14)
        self.assertEqual(second["outcome"],"hit")
        self.assertEqual(second["defense_value"],12)
        self.assertEqual(second["attack_total"],13)
        self.assertEqual(len(scene.report()["attacks"]),2)
        e.check()

    def test_22_swapped_paid_slots_cannot_alias_matching_profiles(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        swapped=dict(seq)
        swapped["actions"]=tuple(reversed(seq["actions"]))
        before=(e.actors["front"].hp,e.actors["front"].vigor,
                e.actors["foe"].ap_remaining,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "action index does not match declared attack slot"):
            scene.resolve(swapped,0,attack_face=1)
        self.assertEqual(
            (e.actors["front"].hp,e.actors["front"].vigor,
             e.actors["foe"].ap_remaining,len(e.ledger)),before)
        self.assertFalse(scene.report()["attacks"])
        # Ordinary misses must each consume ONLY their own source slot.
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(scene.resolve(seq,1,attack_face=1)["outcome"],"miss")
        self.assertEqual(
            [x["action_index"] for x in scene.report()["attacks"]],
            list(seq["actions"]))
        e.check()


    def test_23_sequence_must_resolve_slots_in_declared_order(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        before=(e.actors["front"].hp,e.actors["front"].vigor,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "Resolve or lose earlier declared attack slots first"):
            scene.resolve(seq,1,attack_face=1)
        self.assertEqual((e.actors["front"].hp,e.actors["front"].vigor,
                          len(e.ledger)),before)
        self.assertFalse(scene.report()["attacks"])
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(scene.resolve(seq,1,attack_face=1)["outcome"],"miss")
        self.assertEqual([a["action_index"] for a in scene.report()["attacks"]],
                         list(seq["actions"]))
        e.check()

    def test_24_dying_disables_later_precommitted_guard_and_dodge(self):
        for second_defense in ("guard","dodge"):
            with self.subTest(second_defense=second_defense):
                scene=fixed_scene("I2",sentry_state="prepared_start")
                e=scene.e
                e.actors["front"].hp=6
                scene.bridge.start_next_turn(RegenerationChoice())
                seq=scene.declare("foe","front",
                        profiles=("B06-AT-02","B06-AT-02"),
                        defenses=("take_hit",second_defense))
                guard=e.actors["front"].guard_remaining
                pressure=e.actors["front"].dodge_pressure
                first=scene.resolve(seq,0,attack_face=11,damage_face=1,
                                    vigor_die=4,wound_location_roll=10)
                self.assertEqual(first["damage"]["hp_loss"],6)
                self.assertEqual(e.actors["front"].hp,0)
                self.assertFalse(e.actors["front"].dead)
                # Attack 2+7=9 cannot beat the precommitted active defense,
                # but an unconscious defender can only Take Hit.
                second=scene.resolve(seq,1,attack_face=2,damage_face=1,
                                     vigor_die=4)
                self.assertEqual(second["outcome"],"hit")
                self.assertEqual(second["defense"],"take_hit")
                self.assertEqual(second["declared_defense"],second_defense)
                self.assertIsNone(second["defense_value"])
                self.assertEqual(e.actors["front"].hp,-6)
                self.assertEqual(e.actors["front"].guard_remaining,guard)
                self.assertEqual(e.actors["front"].dodge_pressure,pressure)
                fallback=[x for x in e.ledger
                          if x["kind"]=="g5_defense_unavailable_fallback"]
                self.assertEqual(len(fallback),1)
                self.assertEqual(fallback[0]["detail"]["declared"],second_defense)
                self.assertEqual(fallback[0]["detail"]["resolved"],"take_hit")
                self.assertEqual(len(e.actors["front"].wounds),1)
                e.check()

    def test_25_missing_enchanted_vigor_die_does_not_commit_roll_or_response(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02",),defenses=("take_hit",))
        before=(e.actors["front"].hp,e.actors["front"].vigor,len(e.ledger))
        for die in (None,0,7,"4"):
            with self.subTest(vigor_die=die):
                with self.assertRaisesRegex(ValueError,
                                            "enchanted-sword d6"):
                    scene.resolve(seq,0,attack_face=11,damage_face=4,
                                  vigor_die=die)
                self.assertEqual((e.actors["front"].hp,
                                  e.actors["front"].vigor,len(e.ledger)),before)
        self.assertFalse([x for x in e.ledger if x["kind"] in (
            "g5_melee_roll","g5_melee_resolved","response_window_open")])
        # An invalid, unrecorded dice proposal does not spend the committed
        # attack: a genuine legal miss may still be resolved exactly once.
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(len(scene.report()["attacks"]),1)
        e.check()

    def test_26_missing_wound_location_preflight_keeps_attack_unrolled(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        e.actors["front"].hp=9
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02",),defenses=("take_hit",))
        prior=(e.actors["front"].hp,len(e.actors["front"].wounds),
               len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "wound-location d20 required"):
            scene.resolve(seq,0,attack_face=11,damage_face=4,vigor_die=4)
        self.assertEqual((e.actors["front"].hp,
                          len(e.actors["front"].wounds),
                          len(e.ledger)),prior)
        self.assertFalse([x for x in e.ledger if x["kind"]=="g5_melee_roll"])
        result=scene.resolve(seq,0,attack_face=11,damage_face=4,
                             vigor_die=4,wound_location_roll=14)
        self.assertEqual(result["damage"]["hp_loss"],9)
        self.assertEqual(e.actors["front"].hp,0)
        self.assertEqual(len(e.actors["front"].wounds),1)
        self.assertEqual(sum(x["kind"]=="g5_melee_roll" for x in e.ledger),1)
        e.check()

    def test_27_live_prone_bonus_and_penalty_control_melee_and_confirmation(self):
        for attacker_prone,target_prone,expected_modifier,face,expected in (
            (False,True,2,10,"hit"),
            (True,False,-2,12,"miss"),
            (True,True,-2,12,"miss"),
            (False,False,0,12,"hit"),
        ):
            with self.subTest(attacker_prone=attacker_prone,
                              target_prone=target_prone):
                e,scene=crossed_scene()
                if attacker_prone:
                    e.actors["sentry"].conditions.append("Prone")
                if target_prone:
                    e.actors["soldier"].conditions.append("Prone")
                scene.bridge.start_next_turn(RegenerationChoice())
                seq=scene.declare("sentry","soldier",
                                  profiles=("B06-AT-02",),defenses=("guard",))
                result=scene.resolve(seq,0,attack_face=face,
                   damage_face=1 if expected=="hit" else None,
                   vigor_die=4 if expected=="hit" else None)
                self.assertEqual(result["prone_modifier"],expected_modifier)
                self.assertEqual(result["outcome"],expected)
                self.assertEqual(result["attack_total"],face+7+expected_modifier)
                roll=next(x["detail"] for x in e.ledger
                          if x["kind"]=="g5_melee_roll")
                self.assertEqual(roll["source_attack_bonus"],7)
                self.assertEqual(roll["prone_modifier"],expected_modifier)
                e.check()

    def test_28_prone_applies_to_natural20_guard_confirmation_too(self):
        for attacker_prone,target_prone,confirmation,expected in (
            (False,True,10,"critical"),
            (True,False,10,"strong"),
            (True,True,10,"strong"),
        ):
            with self.subTest(attacker_prone=attacker_prone,
                              target_prone=target_prone):
                e,scene=crossed_scene()
                if attacker_prone:
                    e.actors["sentry"].conditions.append("Prone")
                if target_prone:
                    e.actors["soldier"].conditions.append("Prone")
                scene.bridge.start_next_turn(RegenerationChoice())
                seq=scene.declare("sentry","soldier",
                          profiles=("B06-AT-02",),defenses=("guard",))
                critical_dice=(1,1) if expected=="critical" else (1,)
                result=scene.resolve(seq,0,attack_face=20,
                          confirmation_face=confirmation,
                          critical_dice=critical_dice,damage_face=1,
                          vigor_die=4,wound_location_roll=None)
                self.assertEqual(result["critical"],expected)
                self.assertEqual(e.actors["soldier"].wounds,[])
                e.check()


    def test_29_dying_at_authored_exit_cannot_be_attested_as_withdrawal(self):
        for damage,expected_hp in ((12,0),(13,-1)):
            with self.subTest(hp_after=expected_hp):
                scene=fixed_scene("I1",seed=7029+damage)
                e=scene.e
                scene.bridge.start_next_turn(RegenerationChoice())
                scene.bridge.end_current_turn()
                scene.bridge.start_next_turn(RegenerationChoice())
                # These are real G1 movements; the actor initially reaches
                # the policy-authorized edge while still conscious.
                for _ in range(2):
                    self.assertTrue(e.g1.step("front",(-1,0),
                                              responses=lambda _:()))
                a=e.actors["front"]
                self.assertEqual(a.occupied,(scene.scene_exit.square,))
                self.assertEqual(a.hp,12)
                step=next(x for x in reversed(e.ledger)
                          if x["kind"]=="g1_movement_step")
                self.assertEqual(step["detail"]["actor"],"front")
                # The source-confirmed harm is later than the actual
                # movement step, but BEFORE the terminal attestation.
                result=e.g4.apply_damage(
                    "front",(DamagePacket("hp","Fire",damage),),
                    event_key=f"g5:exit-post-step-harm:{damage}",
                    cause="independently_confirmed_exit_harm",
                    wound_location_roll=11)
                self.assertEqual(result["hp_loss"],damage)
                self.assertEqual(a.hp,expected_hp)
                self.assertFalse(a.dead)
                self.assertEqual(len(a.wounds),1)
                before=e.serialize()
                with self.assertRaisesRegex(ValueError,
                                             "Dying/dead actor cannot withdraw"):
                    scene.withdraw("front")
                self.assertEqual(e.serialize(),before)
                self.assertEqual(scene.report()["ending"],"unresolved")
                self.assertEqual(scene.report()["outcomes"],[])
                self.assertFalse(any(x["kind"] in
                    ("g45_withdrawal_attested","g5_terminal_exit")
                    for x in e.ledger))
                self.assertFalse(scene.report()["complete_party_pack_certified"])
                e.check()


    def test_30_prior_round_resolved_action_does_not_unlock_new_dodge_slot(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        old=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        historical=old["actions"][0]
        self.assertEqual(scene.resolve(old,0,attack_face=1)["outcome"],"miss")
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        scene.bridge.end_current_turn()
        scene.bridge.begin_next_round()
        scene.bridge.start_next_turn(RegenerationChoice())
        current=scene.declare("foe","front",
                              profiles=("B06-AT-02","B06-AT-02"),
                              defenses=("dodge","dodge"))
        self.assertEqual([e.ledger[i]["detail"]["defense_value"]
                          for i in current["defenses"]],[14,12])
        self.assertNotEqual(historical,current["actions"][0])
        forged=dict(current)
        forged["actions"]=(historical,current["actions"][1])
        before=(e.actors["front"].hp,e.actors["front"].vigor,
                e.actors["front"].dodge_pressure,
                e.actors["foe"].ap_remaining,len(e.ledger))
        # 6+7=13 misses first Dodge14 and beats second Dodge12.
        # Replacing the first index with an old completed slot must not
        # allow resolution at the artificially favorable later defense.
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "action index does not match declared attack slot"):
            scene.resolve(forged,1,attack_face=6,damage_face=1,vigor_die=4)
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "Resolve or lose earlier declared attack slots first"):
            scene.resolve(current,1,attack_face=6,damage_face=1,vigor_die=4)
        self.assertEqual((e.actors["front"].hp,e.actors["front"].vigor,
                          e.actors["front"].dodge_pressure,
                          e.actors["foe"].ap_remaining,len(e.ledger)),before)
        self.assertFalse(any(x["kind"]=="g5_melee_resolved" and
                             x["detail"]["action_index"]==current["actions"][1]
                             for x in e.ledger))
        first=scene.resolve(current,0,attack_face=6)
        second=scene.resolve(current,1,attack_face=6,damage_face=1,vigor_die=4)
        self.assertEqual((first["outcome"],first["defense_value"]),("miss",14))
        self.assertEqual((second["outcome"],second["defense_value"]),("hit",12))
        self.assertEqual(second["attack_total"],13)
        self.assertEqual((e.actors["front"].hp,e.actors["front"].vigor),(6,34))
        e.check()

    def test_31_tampered_prior_slot_rejected_even_after_current_slot_resolves(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        old=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        self.assertEqual(scene.resolve(old,0,attack_face=1)["outcome"],"miss")
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        scene.bridge.end_current_turn()
        scene.bridge.begin_next_round()
        scene.bridge.start_next_turn(RegenerationChoice())
        current=scene.declare("foe","front",
                              profiles=("B06-AT-02","B06-AT-02"),
                              defenses=("take_hit","take_hit"))
        self.assertEqual(scene.resolve(current,0,attack_face=1)["outcome"],"miss")
        forged=dict(current)
        forged["actions"]=(old["actions"][0],current["actions"][1])
        before=(e.actors["front"].hp,e.actors["front"].vigor,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "action index does not match declared attack slot"):
            scene.resolve(forged,1,attack_face=1)
        self.assertEqual((e.actors["front"].hp,e.actors["front"].vigor,
                          len(e.ledger)),before)
        self.assertEqual(scene.resolve(current,1,attack_face=1)["outcome"],"miss")
        self.assertEqual([x["action_index"] for x in scene.report()["attacks"]][-2:],
                         list(current["actions"]))
        e.check()


    def test_32_g5_precommitted_attack_blocks_g1_movement_until_resolved(self):
        scene=fixed_scene("I1",seed=9032)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("take_hit",))
        foe=e.actors["foe"]
        before=(foe.occupied,foe.mp_remaining,len(e.ledger))
        for attempt in (
            lambda:e.g1.step("foe",(0,-1),responses=lambda eligible:()),
            lambda:e.g1.move_route("foe",((0,-1),)),
        ):
            with self.subTest(attempt=attempt):
                with self.assertRaisesRegex(
                        UnresolvedDecision,"Complete committed G5 Attack Sequence"):
                    attempt()
                self.assertEqual(
                    (foe.occupied,foe.mp_remaining,len(e.ledger)),before)
        self.assertTrue(e.g1.melee_contact("foe","front"))
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertTrue(e.g1.step("foe",(0,-1),
                                   responses=lambda eligible:()))
        self.assertEqual(foe.occupied,((3,1),))
        self.assertEqual(foe.mp_remaining,before[1]-2)
        e.check()

    def test_33_g5_multi_slot_movement_block_persists_between_hits(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9033)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        foe=e.actors["foe"]
        before=(foe.occupied,foe.mp_remaining,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "Complete committed G5 Attack Sequence"):
            e.g1.step("foe",(0,-1),responses=lambda eligible:())
        self.assertEqual((foe.occupied,foe.mp_remaining,len(e.ledger)),before)
        self.assertEqual(scene.resolve(seq,1,attack_face=1)["outcome"],"miss")
        self.assertTrue(e.g1.step("foe",(0,-1),
                                  responses=lambda eligible:()))
        self.assertEqual(foe.occupied,((3,1),))
        e.check()

    def test_34_g5_resolution_rejects_unauthorized_post_declaration_movement(self):
        scene=fixed_scene("I1",seed=9034)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("take_hit",))
        before=(e.actors["front"].hp,len(scene.report()["attacks"]))
        # Defense in depth if another integration bypasses G1's proactive
        # preflight and commits translation directly to the source ledger.
        e.log("g1_movement_step",actor="foe",old=((3,2),),new=((3,1),),
              step_kind="orthogonal",cost=2)
        with self.assertRaisesRegex(
                UnresolvedDecision,
                "Committed G5 Attack Sequence cannot interleave movement"):
            scene.resolve(seq,0,attack_face=1)
        self.assertEqual((e.actors["front"].hp,
                          len(scene.report()["attacks"])),before)
        self.assertFalse(any(x["kind"]=="g5_melee_roll" for x in e.ledger))
        e.check()

    def test_35_prone_dodge_needs_feasibility_before_g0_commit(self):
        scene=fixed_scene("I1",seed=9035)
        e=scene.e
        e.actors["front"].conditions.append("Prone")
        scene.bridge.start_next_turn(RegenerationChoice())
        foe=e.actors["foe"]
        front=e.actors["front"]
        before=(foe.ap_remaining,front.dodge_pressure,
                front.guard_remaining,len(e.ledger))
        for feasible in (None,False):
            with self.subTest(feasible=feasible):
                with self.assertRaisesRegex(
                        UnresolvedDecision,
                        "Prone Dodge requires explicit physical capability"):
                    scene.declare("foe","front",profiles=("B06-AT-03",),
                                  defenses=("dodge",),
                                  prone_dodge_feasible=feasible)
                self.assertEqual(
                    (foe.ap_remaining,front.dodge_pressure,
                     front.guard_remaining,len(e.ledger)),before)
        self.assertFalse(e.seen_sequences)
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("dodge",),prone_dodge_feasible=True)
        self.assertEqual(front.dodge_pressure,2)
        self.assertEqual(foe.ap_remaining,before[0]-foe.physical_ap)
        self.assertTrue(any(x["kind"]=="g5_melee_sequence_attested"
                            and x["detail"]["prone_dodge_feasible"]
                            for x in e.ledger))
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        e.check()

    def test_36_newly_prone_dodge_requires_capability_at_resolution(self):
        scene=fixed_scene("I1",seed=9036)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("dodge",))
        pre=(e.actors["front"].hp,
             e.actors["foe"].ap_remaining,
             e.actors["front"].dodge_pressure)
        e.actors["front"].conditions.append("Prone")
        ledger_before=len(e.ledger)
        with self.assertRaisesRegex(
                UnresolvedDecision,
                "Prone Dodge requires explicit physical capability"):
            scene.resolve(seq,0,attack_face=1)
        self.assertEqual(len(e.ledger),ledger_before)
        self.assertEqual((e.actors["front"].hp,e.actors["foe"].ap_remaining,
                          e.actors["front"].dodge_pressure),pre)
        self.assertFalse(any(x["kind"]=="g5_melee_roll" for x in e.ledger))
        e.check()

if __name__=="__main__":
    unittest.main()
