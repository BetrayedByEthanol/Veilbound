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
        # A genuine pre-existing G0 reservation is legal. Its 20-AP
        # payment logs action_committed, G1 segment_break, then
        # interception_reserved BEFORE the separately paid attack.
        # A NEW reservation after declare() is rejected by G5's AP gate.
        expected_action_index=len(e.ledger)+3
        e.reserve("foe",f"g5:melee:{expected_action_index}","deferred",
                  action_kind="physical")
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        self.assertEqual(seq["actions"][0],expected_action_index)
        self.assertEqual(e.actors["foe"].ap_remaining,2)
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
        # Round rollover is illegal until this paid first-round attack has
        # genuinely resolved or its trigger has been explicitly cancelled.
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "committed G5 attack slot"):
            scene.bridge.end_current_turn()
        self.assertEqual(scene.resolve(stale,0,attack_face=1)["outcome"],"miss")
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
        self.assertEqual(
            len([x for x in e.ledger if x["kind"]=="g5_melee_resolved"]),1)
        self.assertEqual(
            len([x for x in e.ledger if x["kind"]=="g5_melee_roll"]),1)
        # Failure must not consume this round's real AP. A newly declared
        # sequence CAN legally produce the same natural-one miss now.
        fresh=scene.declare("foe","front",profiles=("B06-AT-03",),
                            defenses=("guard",))
        r=scene.resolve(fresh,0,attack_face=1)
        self.assertEqual(r["outcome"],"miss")
        self.assertEqual(e.ledger[fresh["declaration"]]["round"],2)
        self.assertEqual(len(scene.report()["attacks"]),2)
        self.assertEqual([a["outcome"] for a in scene.report()["attacks"]],
                         ["miss","miss"])
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
                                  profiles=("B06-AT-02",),defenses=("guard",),
                                  prone_guard_feasible=target_prone,
                                  prone_attack_feasible=attacker_prone)
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
                          profiles=("B06-AT-02",),defenses=("guard",),
                          prone_guard_feasible=target_prone,
                          prone_attack_feasible=attacker_prone)
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


    def test_37_i1_paid_unresolved_attack_blocks_native_turn_end_and_exit(self):
        scene=fixed_scene("I1",seed=9137)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-03",),defenses=("guard",))
        before=(e.current,e.cursor,e.round,
                e.actors["foe"].ap_remaining,
                e.actors["front"].guard_remaining,len(e.ledger))
        # This is the exact prior false terminal: caller attempts to
        # silently end the paid but unrolled Soldier turn, then escape.
        for end in (scene.bridge.end_current_turn,e.end_turn):
            with self.assertRaisesRegex(UnresolvedDecision,
                                        "committed G5 attack slot"):
                end()
            self.assertEqual((e.current,e.cursor,e.round,
                              e.actors["foe"].ap_remaining,
                              e.actors["front"].guard_remaining,
                              len(e.ledger)),before)
        outstanding=scene.pending_attack_slots()
        self.assertEqual(len(outstanding),1)
        self.assertEqual(outstanding[0]["action_index"],seq["actions"][0])
        self.assertEqual(scene.report()["ending"],"unresolved")
        self.assertEqual(len(scene.report()["unresolved_attack_slots"]),1)
        self.assertFalse(scene.report()["attacks"])
        self.assertFalse(any(x["kind"]=="turn_end" and
                             x["detail"].get("actor")=="foe" for x in e.ledger))
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertFalse(scene.pending_attack_slots())
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        for _ in range(2):
            self.assertTrue(e.g1.step("front",(-1,0),
                                     responses=lambda eligible:()))
        withdrawal=scene.withdraw("front")
        self.assertEqual(withdrawal["status"],"withdrawal_attested")
        self.assertEqual(scene.report()["ending"],"withdrawal_attested")
        self.assertEqual(len(scene.report()["attacks"]),1)
        self.assertFalse(scene.report()["unresolved_attack_slots"])
        scene.bridge.end_current_turn()
        e.check()

    def test_38_terminal_withdrawal_checks_pending_enemy_slots_globally(self):
        front=party_actor("A",3,"front","party",occupied=((0,1),))
        foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((1,2),))
        e=Encounter([front,foe],{"front":30,"foe":20},
                    seed=9138,scenario="G5-withdrawal-pending",
                    objective="front_verified_border_exit",
                    policy="explicit_no_automatic_interruption")
        GridMovement(e,width=8,height=5,scene_id="G5-pending-exit-map")
        SpellState(e)
        DamageState(e)
        e.begin_round()
        exit_policy=SceneExit(e.scenario,e.g1.scene_id,e.objective,
                              "front",(0,2),"G5:independently_authored_exit")
        scene=SourceMelee(e,scene_exit=exit_policy)
        scene.bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(e.g1.step("front",(0,1),
                                  responses=lambda eligible:()))
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("take_hit",))
        before=(len(e.ledger),front.hp,foe.ap_remaining)
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "terminal withdrawal with unresolved"):
            scene.withdraw("front")
        self.assertEqual((len(e.ledger),front.hp,foe.ap_remaining),before)
        self.assertEqual(scene.report()["ending"],"unresolved")
        self.assertEqual(len(scene.report()["unresolved_attack_slots"]),1)
        self.assertFalse(any(x["kind"] in ("g45_withdrawal_attested",
                                           "g5_terminal_exit") for x in e.ledger))
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        scene.bridge.end_current_turn()
        self.assertFalse(scene.pending_attack_slots())
        result=scene.withdraw("front")
        self.assertEqual(result["status"],"withdrawal_attested")
        self.assertEqual(scene.report()["ending"],"withdrawal_attested")
        self.assertEqual(len(scene.report()["attacks"]),1)
        e.check()

    def test_39_multi_attack_turn_cannot_end_between_resolved_slots(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9139)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        self.assertEqual(len(scene.pending_attack_slots()),2)
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        self.assertEqual(scene.pending_attack_slots()[0]["slot"],1)
        held=(e.current,e.cursor,e.actors["foe"].ap_remaining,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "committed G5 attack slot"):
            e.end_turn()
        self.assertEqual((e.current,e.cursor,
                          e.actors["foe"].ap_remaining,len(e.ledger)),held)
        self.assertEqual(scene.resolve(seq,1,attack_face=1)["outcome"],"miss")
        self.assertFalse(scene.pending_attack_slots("foe"))
        scene.bridge.end_current_turn()
        self.assertEqual(e.current,None)
        self.assertEqual(e.cursor,1)
        self.assertEqual([a["outcome"] for a in scene.report()["attacks"]],
                         ["miss","miss"])
        e.check()


    def test_40_open_sequence_blocks_second_target_before_any_payment(self):
        sentry=enemy_actor("B06-EN-01","sentry","party",
                           start_state="prepared_start",occupied=((3,2),))
        first=enemy_actor("B06-EN-02","first","enemy",occupied=((4,2),))
        second=enemy_actor("B06-EN-02","second","enemy",occupied=((3,3),))
        e=Encounter([sentry,first,second],
                    {"sentry":60,"first":40,"second":20},
                    seed=9240,scenario="G5-two-targets",
                    policy="declarations_must_finish")
        GridMovement(e,width=8,height=5)
        SpellState(e)
        DamageState(e)
        e.begin_round()
        g=SourceMelee(e)
        g.bridge.start_next_turn(RegenerationChoice())
        older=g.declare("sentry","first",profiles=("B06-AT-02",),
                        defenses=("take_hit",))
        self.assertEqual(sentry.ap_remaining,22)
        before=e.serialize()
        state=(sentry.ap_remaining,second.guard_remaining,
               second.dodge_pressure,set(e.seen_sequences))
        # SourceMelee and direct native G0 must both reject BEFORE payment.
        for declare in (
            lambda:g.declare("sentry","second",profiles=("B06-AT-02",),
                             defenses=("guard",)),
            lambda:e.declare_sequence("sentry","second",
                                      ("B06-AT-02",),("guard",)),
        ):
            with self.assertRaisesRegex(
                UnresolvedDecision,"Complete pending G5 Attack Sequence"):
                declare()
            self.assertEqual(e.serialize(),before)
            self.assertEqual(
                (sentry.ap_remaining,second.guard_remaining,
                 second.dodge_pressure,set(e.seen_sequences)),state)
        self.assertEqual(len(g.pending_attack_slots("sentry")),1)
        self.assertEqual(g.resolve(older,0,attack_face=1)["outcome"],"miss")
        self.assertFalse(g.pending_attack_slots("sentry"))
        newer=g.declare("sentry","second",profiles=("B06-AT-02",),
                        defenses=("guard",))
        self.assertEqual(sentry.ap_remaining,2)
        self.assertEqual(second.guard_remaining,second.guard_capacity-1)
        self.assertEqual(g.resolve(newer,0,attack_face=1)["outcome"],"miss")
        self.assertEqual([x["target"] for x in g.report()["attacks"]],
                         ["first","second"])
        g.bridge.end_current_turn()
        self.assertFalse(g.pending_attack_slots())
        e.check()

    def test_41_partially_resolved_multi_slot_blocks_other_target(self):
        sentry=enemy_actor("B06-EN-01","sentry","party",
                           start_state="prepared_start",occupied=((3,2),))
        one=enemy_actor("B06-EN-02","one","enemy",occupied=((4,2),))
        two=enemy_actor("B06-EN-02","two","enemy",occupied=((3,3),))
        e=Encounter([sentry,one,two],
                    {"sentry":60,"one":40,"two":20},
                    seed=9241,scenario="G5-partial-sequence",
                    policy="no_overlap")
        GridMovement(e,width=8,height=5)
        SpellState(e)
        DamageState(e)
        e.begin_round()
        g=SourceMelee(e)
        g.bridge.start_next_turn(RegenerationChoice())
        seq=g.declare("sentry","one",
                      profiles=("B06-AT-02","B06-AT-02"),
                      defenses=("take_hit","take_hit"))
        self.assertEqual(g.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(len(g.pending_attack_slots("sentry")),1)
        before=e.serialize()
        with self.assertRaisesRegex(
            UnresolvedDecision,"Complete pending G5 Attack Sequence"):
            g.declare("sentry","two",profiles=("B06-AT-02",),
                      defenses=("take_hit",))
        self.assertEqual(e.serialize(),before)
        self.assertEqual(g.pending_attack_slots("sentry")[0]["slot"],1)
        self.assertEqual(g.resolve(seq,1,attack_face=1)["outcome"],"miss")
        self.assertFalse(g.pending_attack_slots("sentry"))
        g.bridge.end_current_turn()
        e.check()

    def test_42_fatal_first_hit_retains_paid_followup_until_declined(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9242)
        e=scene.e
        front=e.actors["front"]
        front.hp=1
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","guard"))
        remaining_ap=e.actors["foe"].ap_remaining
        remaining_guard=front.guard_remaining
        self.assertEqual((remaining_ap,remaining_guard),
                         (2,front.guard_capacity-1))
        first=scene.resolve(seq,0,attack_face=20,confirmation_face=20,
                            critical_dice=(4,4),damage_face=6,vigor_die=4)
        self.assertTrue(first["damage"]["dead"])
        self.assertTrue(front.dead)
        self.assertEqual(front.hp,-front.hp_max)
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        self.assertEqual(scene.pending_attack_slots("foe")[0]["action_index"],
                         seq["actions"][1])
        self.assertFalse(any(x["kind"]=="g5_melee_cancelled" for x in e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"committed G5 attack slot"):
            scene.bridge.end_current_turn()
        self.assertEqual(scene.report()["ending"],"unresolved")
        before=(front.hp,e.actors["foe"].ap_remaining,
                front.guard_remaining)
        declined=scene.decline_remaining(seq)
        self.assertEqual(declined,(seq["actions"][1],))
        self.assertFalse(scene.pending_attack_slots())
        self.assertEqual((front.hp,e.actors["foe"].ap_remaining,
                          front.guard_remaining),before)
        cancelled=[x for x in e.ledger if x["kind"]=="g5_melee_cancelled"]
        self.assertEqual(len(cancelled),1)
        self.assertEqual(cancelled[0]["detail"]["reason"],
                         "explicit_decline_target_unavailable")
        self.assertEqual(cancelled[0]["detail"]["ap_refunded"],0)
        self.assertFalse(cancelled[0]["detail"]["defense_commitments_refunded"])
        with self.assertRaisesRegex(ValueError,"already cancelled"):
            scene.resolve(seq,1,attack_face=1)
        self.assertEqual(scene.report()["ending"],"death_attested")
        scene.bridge.end_current_turn()
        e.check()


    def test_43_direct_g0_declaration_does_not_strand_paid_g5_attack(self):
        scene=fixed_scene("I1",seed=9243)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        foe,front=e.actors["foe"],e.actors["front"]
        before=(foe.ap_remaining,front.guard_remaining,
                front.dodge_pressure,len(e.ledger),set(e.seen_sequences))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "G5 requires SourceMelee.declare"):
            e.declare_sequence("foe","front",("B06-AT-03",),("guard",))
        self.assertEqual((foe.ap_remaining,front.guard_remaining,
                          front.dodge_pressure,len(e.ledger),
                          set(e.seen_sequences)),before)
        self.assertFalse(scene.pending_attack_slots())
        self.assertEqual(scene.report()["ending"],"unresolved")
        self.assertEqual(scene.report()["attacks"],[])
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("guard",))
        self.assertEqual(len(scene.pending_attack_slots()),1)
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "committed G5 attack slot"):
            e.end_turn()
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertFalse(scene.pending_attack_slots())
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        for _ in range(2):
            self.assertTrue(e.g1.step("front",(-1,0),
                                     responses=lambda eligible:()))
        self.assertEqual(scene.withdraw("front")["status"],
                         "withdrawal_attested")
        self.assertEqual(scene.report()["ending"],"withdrawal_attested")
        self.assertEqual(len(scene.report()["attacks"]),1)
        e.check()

    def test_44_prone_guard_requires_feasible_instrument_before_payment(self):
        scene=fixed_scene("I1",seed=9244)
        e=scene.e
        front=e.actors["front"]
        front.conditions.append("Prone")
        scene.bridge.start_next_turn(RegenerationChoice())
        foe=e.actors["foe"]
        before=(foe.ap_remaining,front.guard_remaining,
                front.dodge_pressure,len(e.ledger),
                set(e.seen_sequences))
        for feasible in (None,False):
            with self.subTest(feasible=feasible):
                with self.assertRaisesRegex(UnresolvedDecision,
                    "Prone Guard requires explicit instrument feasibility"):
                    scene.declare("foe","front",
                                  profiles=("B06-AT-03",),defenses=("guard",),
                                  prone_guard_feasible=feasible)
                self.assertEqual(
                    (foe.ap_remaining,front.guard_remaining,
                     front.dodge_pressure,len(e.ledger),
                     set(e.seen_sequences)),before)
        self.assertFalse(scene.pending_attack_slots())
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("guard",),prone_guard_feasible=True)
        self.assertEqual(foe.ap_remaining,before[0]-foe.physical_ap)
        self.assertEqual(front.guard_remaining,before[1]-1)
        attested=next(x["detail"] for x in e.ledger
                      if x["kind"]=="g5_melee_sequence_attested")
        self.assertTrue(attested["prone_guard_feasible"])
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(front.hp,front.hp_max)
        e.check()

    def test_45_newly_prone_guard_requires_precommitted_feasibility(self):
        scene=fixed_scene("I1",seed=9245)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-03",),
                          defenses=("guard",))
        front,foe=e.actors["front"],e.actors["foe"]
        front.conditions.append("Prone")
        before=(front.hp,front.guard_remaining,foe.ap_remaining,
                len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                        "Prone Guard requires explicit instrument feasibility"):
            scene.resolve(seq,0,attack_face=14,damage_face=4)
        self.assertEqual((front.hp,front.guard_remaining,
                          foe.ap_remaining,len(e.ledger)),before)
        self.assertFalse(any(x["kind"] in ("g5_melee_roll","g5_melee_resolved")
                             for x in e.ledger))
        self.assertEqual(len(scene.pending_attack_slots()),1)
        self.assertEqual(scene.report()["ending"],"unresolved")
        e.check()

    def test_46_failed_adapter_declaration_resets_native_gate(self):
        scene=fixed_scene("I2",sentry_state="cold_start",seed=9246)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        with self.assertRaisesRegex(ValueError,"Sentry profile"):
            scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("guard",))
        self.assertFalse(scene._native_sequence_authorized)
        before=(e.actors["foe"].ap_remaining,
                e.actors["front"].guard_remaining,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "G5 requires SourceMelee.declare"):
            e.declare_sequence("foe","front",("B06-AT-01",),("guard",))
        self.assertEqual((e.actors["foe"].ap_remaining,
                          e.actors["front"].guard_remaining,len(e.ledger)),
                         before)
        seq=scene.declare("foe","front",profiles=("B06-AT-01",),
                          defenses=("guard",))
        self.assertFalse(scene._native_sequence_authorized)
        self.assertEqual(len(scene.pending_attack_slots()),1)
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        e.check()



    def test_47_pending_sentry_slot_blocks_physical_reservation_before_commit(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9247)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        foe=e.actors["foe"]
        self.assertEqual(foe.ap_remaining,22)
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        original=e.serialize()
        reserved=list(e.reservations)
        state=(foe.ap_remaining,foe.mp_remaining,
               e.actors["front"].guard_remaining,
               e.actors["front"].dodge_pressure,
               set(e.seen_sequences))
        with self.assertRaisesRegex(
            UnresolvedDecision,
            "Complete pending G5 Attack Sequence before committing Turn AP"):
            e.reserve("foe","future-interception","later-defense",
                      action_kind="physical")
        self.assertEqual(e.serialize(),original)
        self.assertEqual(e.reservations,reserved)
        self.assertEqual(
            (foe.ap_remaining,foe.mp_remaining,
             e.actors["front"].guard_remaining,
             e.actors["front"].dodge_pressure,
             set(e.seen_sequences)),state)
        self.assertFalse(any(x["kind"]=="interception_reserved"
                             for x in e.ledger))
        # An invalid reservation must not make the original attack stale.
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertFalse(scene.pending_attack_slots("foe"))
        # The remaining 22 AP may now fund an actual separate reservation.
        e.reserve("foe","later-window","later-defense",
                  action_kind="physical")
        self.assertEqual(foe.ap_remaining,2)
        self.assertEqual(len(e.reservations),1)
        scene.bridge.end_current_turn()
        self.assertEqual(e.cursor,1)
        e.check()

    def test_48_every_own_turn_ap_class_and_reserve_kind_are_blocked(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9248)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        foe=e.actors["foe"]
        before=e.serialize()
        before_state=(foe.ap_remaining,foe.mp_remaining,
                      len(e.reservations),len(scene.pending_attack_slots("foe")))
        attempts=[
            lambda:e.spend_ap("foe","physical",label="other-sword"),
            lambda:e.spend_ap("foe","projection",label="other-spell"),
            lambda:e.spend_ap("foe","general",label="other-action"),
            lambda:e.spend_ap("foe","full",label="other-full-action"),
            lambda:e.reserve("foe","other-window","physical-guard",
                             action_kind="physical"),
            lambda:e.reserve("foe","other-window","general-guard",
                             action_kind="general"),
            lambda:e.g3._commit("foe",label="g3:unexpected_projection"),
        ]
        for attempt in attempts:
            with self.subTest(attempt=attempt):
                with self.assertRaisesRegex(
                    UnresolvedDecision,
                    "Complete pending G5 Attack Sequence before committing Turn AP"):
                    attempt()
                self.assertEqual(e.serialize(),before)
                self.assertEqual((foe.ap_remaining,foe.mp_remaining,
                                  len(e.reservations),
                                  len(scene.pending_attack_slots("foe"))),
                                 before_state)
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        scene.bridge.end_current_turn()
        e.check()

    def test_49_partially_resolved_multi_slot_blocks_ap_until_last_hit(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9249)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        self.assertEqual(e.actors["foe"].ap_remaining,2)
        self.assertEqual(len(scene.pending_attack_slots("foe")),2)
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        before=e.serialize()
        with self.assertRaisesRegex(
            UnresolvedDecision,
            "Complete pending G5 Attack Sequence before committing Turn AP"):
            e.reserve("foe","interrupt-other","reserve-second-attack")
        self.assertEqual(e.serialize(),before)
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        self.assertEqual(scene.resolve(seq,1,attack_face=1)["outcome"],"miss")
        self.assertFalse(scene.pending_attack_slots())
        scene.bridge.end_current_turn()
        self.assertEqual(e.cursor,1)
        self.assertEqual(
            [x["detail"]["outcome"] for x in e.ledger
             if x["kind"]=="g5_melee_resolved"],["miss","miss"])
        e.check()



    def test_50_prone_soldier_and_sentry_require_feasible_sword_before_ap(self):
        for pack,state,profile in (
            ("I1",None,"B06-AT-03"),
            ("I2","prepared_start","B06-AT-02"),
        ):
            with self.subTest(pack=pack,state=state):
                scene=fixed_scene(pack,sentry_state=state)
                e=scene.e
                foe,front=e.actors["foe"],e.actors["front"]
                foe.conditions.append("Prone")
                scene.bridge.start_next_turn(RegenerationChoice())
                before=(foe.ap_remaining,front.guard_remaining,
                        front.dodge_pressure,len(e.ledger),
                        set(e.seen_sequences))
                for feasible in (None,False):
                    with self.subTest(feasible=feasible):
                        with self.assertRaisesRegex(UnresolvedDecision,
                                "Prone sword attack requires explicit physical feasibility"):
                            scene.declare("foe","front",
                                profiles=(profile,),defenses=("guard",),
                                prone_attack_feasible=feasible)
                        self.assertEqual(
                            (foe.ap_remaining,front.guard_remaining,
                             front.dodge_pressure,len(e.ledger),
                             set(e.seen_sequences)),before)
                        self.assertFalse(scene.pending_attack_slots())
                self.assertFalse(any(x["kind"]=="g5_melee_sequence_attested"
                                     for x in e.ledger))
                e.check()

    def test_51_attested_prone_sword_uses_real_minus_two_on_hit(self):
        e,scene=crossed_scene()
        sentry,soldier=e.actors["sentry"],e.actors["soldier"]
        sentry.conditions.append("Prone")
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("sentry","soldier",
                          profiles=("B06-AT-02",),defenses=("guard",),
                          prone_attack_feasible=True)
        attestation=next(x["detail"] for x in e.ledger
                         if x["kind"]=="g5_melee_sequence_attested")
        self.assertTrue(attestation["prone_attack_feasible"])
        self.assertEqual(sentry.ap_remaining,22)
        self.assertEqual(soldier.guard_remaining,soldier.guard_capacity-1)
        result=scene.resolve(seq,0,attack_face=14,damage_face=1,
                             vigor_die=4)
        self.assertEqual(result["outcome"],"hit")
        self.assertEqual(result["prone_modifier"],-2)
        self.assertEqual(result["attack_total"],14+7-2)
        self.assertLess(soldier.hp,soldier.hp_max)
        roll=next(x["detail"] for x in e.ledger
                  if x["kind"]=="g5_melee_roll")
        self.assertEqual(roll["source_attack_bonus"],7)
        self.assertEqual(roll["prone_modifier"],-2)
        self.assertEqual(len(scene.report()["attacks"]),1)
        e.check()

    def test_52_newly_prone_attacker_needs_precommitted_feasibility(self):
        for predeclared in (None,True):
            with self.subTest(predeclared=predeclared):
                e,scene=crossed_scene()
                scene.bridge.start_next_turn(RegenerationChoice())
                seq=scene.declare("sentry","soldier",
                     profiles=("B06-AT-02",),defenses=("guard",),
                     prone_attack_feasible=predeclared)
                sentry,soldier=e.actors["sentry"],e.actors["soldier"]
                sentry.conditions.append("Prone")
                before=(sentry.ap_remaining,soldier.guard_remaining,
                        soldier.hp,soldier.vigor,len(e.ledger))
                if predeclared is None:
                    with self.assertRaisesRegex(UnresolvedDecision,
                              "Prone sword attack requires explicit physical feasibility"):
                        scene.resolve(seq,0,attack_face=14,damage_face=1,
                                      vigor_die=4)
                    self.assertEqual(
                        (sentry.ap_remaining,soldier.guard_remaining,
                         soldier.hp,soldier.vigor,len(e.ledger)),before)
                    self.assertFalse(any(x["kind"] in
                        ("g5_melee_roll","g5_melee_resolved") for x in e.ledger))
                    self.assertEqual(len(scene.pending_attack_slots()),1)
                else:
                    resolved=scene.resolve(seq,0,attack_face=14,
                                           damage_face=1,vigor_die=4)
                    self.assertEqual(resolved["outcome"],"hit")
                    self.assertEqual(resolved["prone_modifier"],-2)
                    self.assertFalse(scene.pending_attack_slots())
                e.check()



    def test_53_attach_g5_rejects_already_paid_untracked_g0_sequence(self):
        foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
        front=party_actor("A",3,"front","party",occupied=((2,2),))
        e=Encounter([foe,front],{"foe":30,"front":20},
                    seed=9353,scenario="G5-late-attach-native-sequence",
                    objective="source_bound_only",
                    policy="no_untracked_attack_payment")
        GridMovement(e,width=8,height=5)
        SpellState(e)
        DamageState(e)
        e.begin_round()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        e.declare_sequence("foe","front",("B06-AT-03",),("guard",))
        self.assertEqual(foe.ap_remaining,18)
        self.assertEqual(front.guard_remaining,front.guard_capacity-1)
        before=e.serialize()
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "Attach G5 before any untracked native Attack Sequence"):
            SourceMelee(e)
        self.assertEqual(e.serialize(),before)
        self.assertIsNone(getattr(e,"g5",None))
        self.assertFalse(any(x["kind"]=="g45_continuation_opened"
                             for x in e.ledger))
        self.assertEqual(foe.ap_remaining,18)
        self.assertEqual(front.guard_remaining,front.guard_capacity-1)
        e.check()

    def test_54_attach_after_prior_native_sequence_round_still_rejected(self):
        foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
        front=party_actor("A",3,"front","party",occupied=((2,2),))
        e=Encounter([foe,front],{"foe":30,"front":20},
                    seed=9354,scenario="G5-late-attach-prior-round",
                    policy="no_unverified_historical_attack")
        GridMovement(e,width=8,height=5)
        SpellState(e)
        DamageState(e)
        e.begin_round()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        e.declare_sequence("foe","front",("B06-AT-03",),("take_hit",))
        e.end_turn()  # Untracked native G0 cannot prove attack resolution.
        e.start_turn("front",regen_choice=RegenerationChoice())
        e.end_turn()
        e.begin_round()
        before=e.serialize()
        with self.assertRaisesRegex(UnresolvedDecision,"untracked native Attack Sequence"):
            SourceMelee(e)
        self.assertEqual(e.serialize(),before)
        self.assertIsNone(getattr(e,"g5",None))
        e.check()

    def test_55_voluntary_sentry_release_blocked_until_paid_attack_resolves(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9355)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        a=e.actors["foe"]
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,3,0))
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        before=e.serialize()
        resources=(a.ap_remaining,a.vp_available,a.vp_committed,a.vp_spent,
                   tuple(a.maintained))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "Complete pending G5 Attack Sequence"):
            e.g3.release("foe","Sentry Sword Reserve")
        self.assertEqual(e.serialize(),before)
        self.assertEqual((a.ap_remaining,a.vp_available,a.vp_committed,
                          a.vp_spent,tuple(a.maintained)),resources)
        self.assertEqual(len(e.g3.active("foe","Sentry Sword Reserve")),1)
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertFalse(scene.pending_attack_slots("foe"))
        e.g3.release("foe","Sentry Sword Reserve")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(6,0,0))
        self.assertFalse(e.g3.active("foe","Sentry Sword Reserve"))
        self.assertEqual(e.g3.sentry_profile("foe"),"B06-AT-01")
        self.assertEqual(sum(x["kind"]=="g3_effect_ended" for x in e.ledger),1)
        scene.bridge.end_current_turn()
        e.check()

    def test_56_mid_sequence_release_rejected_until_all_slots_resolved(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9356)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        a=e.actors["foe"]
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        self.assertEqual(len(scene.pending_attack_slots("foe")),2)
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        before=e.serialize()
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "Complete pending G5 Attack Sequence"):
            e.g3.release("foe","Sentry Sword Reserve")
        self.assertEqual(e.serialize(),before)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,3,0))
        self.assertEqual(scene.resolve(seq,1,attack_face=1)["outcome"],"miss")
        self.assertFalse(scene.pending_attack_slots("foe"))
        e.g3.release("foe","Sentry Sword Reserve")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(6,0,0))
        scene.bridge.end_current_turn()
        e.check()


    def test_57_raw_vp_release_cannot_unfund_pending_enhanced_sword(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9357)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        a=e.actors["foe"]
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        before=e.serialize()
        original=(a.ap_remaining,a.vp_available,a.vp_committed,a.vp_spent,
                  tuple(a.maintained),len(scene.pending_attack_slots("foe")))
        with self.assertRaisesRegex(ValueError,
                                    "Cannot refund VP owned by active G3 effects"):
            e.release_vp("foe",3,label="bypass:prepared-reserve")
        self.assertEqual(e.serialize(),before)
        self.assertEqual(
            (a.ap_remaining,a.vp_available,a.vp_committed,a.vp_spent,
             tuple(a.maintained),len(scene.pending_attack_slots("foe"))),
            original)
        self.assertEqual(e.g3.sentry_profile("foe"),"B06-AT-02")
        result=scene.resolve(seq,0,attack_face=11,damage_face=4,vigor_die=4)
        self.assertEqual(result["outcome"],"hit")
        self.assertEqual(result["damage"]["hp_loss"],9)
        self.assertEqual(result["damage"]["vigor_loss"],2)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,3,0))
        # Legitimate G3 release still refunds the originally committed
        # three points, now that the declared attack has been resolved.
        e.g3.release("foe","Sentry Sword Reserve")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(6,0,0))
        self.assertEqual(e.g3.sentry_profile("foe"),"B06-AT-01")
        e.check()

    def test_58_cold_cast_raw_release_rejected_but_real_release_succeeds(self):
        scene=fixed_scene("I2",sentry_state="cold_start",seed=9358)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        a=e.actors["foe"]
        effect=e.g3.cast_sentry_reserve("foe")
        self.assertIsNotNone(effect)
        self.assertEqual(e.g3.sentry_profile("foe"),"B06-AT-02")
        original=e.serialize()
        before=(a.ap_remaining,a.vp_available,a.vp_committed,a.vp_spent)
        with self.assertRaisesRegex(ValueError,
                                    "Cannot refund VP owned by active G3 effects"):
            e.release_vp("foe",3,label="bypass:cold-cast")
        self.assertEqual(e.serialize(),original)
        self.assertEqual((a.ap_remaining,a.vp_available,a.vp_committed,
                          a.vp_spent),before)
        self.assertEqual(before,(12,3,3,0))
        e.g3.release("foe","Sentry Sword Reserve")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(6,0,0))
        self.assertEqual(e.g3.sentry_profile("foe"),"B06-AT-01")
        self.assertEqual(len(e.g3.active("foe","Sentry Sword Reserve")),0)
        e.check()

    def test_59_enhanced_profile_requires_live_funded_effect(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9359)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        a=e.actors["foe"]
        original=(a.vp_available,a.vp_committed)
        # Simulate a corrupted actor snapshot that still conserves VP
        # while retaining the old SpellEffect. Even without a direct
        # release_vp call, G5 must never use an unfunded Fire profile.
        a.vp_available,a.vp_committed=(6,0)
        self.assertEqual(a.vp_available+a.vp_committed+a.vp_spent,a.vp_max)
        before=(a.ap_remaining,e.actors["front"].hp,len(e.ledger))
        with self.assertRaisesRegex(ValueError,
                                    "Sentry Sword Reserve lacks funded Committed VP"):
            e.g3.sentry_profile("foe")
        with self.assertRaisesRegex(ValueError,
                                    "Sentry Sword Reserve lacks funded Committed VP"):
            scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        self.assertEqual((a.ap_remaining,e.actors["front"].hp,len(e.ledger)),
                         before)
        a.vp_available,a.vp_committed=original
        self.assertEqual(e.g3.sentry_profile("foe"),"B06-AT-02")
        seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                          defenses=("take_hit",))
        self.assertEqual(scene.resolve(seq,0,attack_face=1)["outcome"],"miss")
        e.check()


    def test_60_independent_g4_death_cancels_every_paid_sentry_slot(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9460)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("dodge","dodge"))
        self.assertEqual(len(scene.pending_attack_slots("foe")),2)
        self.assertEqual(e.actors["front"].dodge_pressure,4)
        # An independently sourced Fire packet interrupts the sentry
        # after both Physical20 actions have already been paid.
        e.g4.apply_damage("foe",(DamagePacket("hp","Fire",24),),
                          event_key="G5:independent:fatal-sentry",
                          cause="independently_confirmed_fire")
        foe=e.actors["foe"]
        self.assertTrue(foe.dead)
        self.assertEqual(foe.hp,-foe.hp_max)
        self.assertEqual(foe.ap_remaining,0)
        self.assertEqual(e.actors["front"].dodge_pressure,4)
        self.assertFalse(scene.pending_attack_slots())
        cancellations=[x for x in e.ledger if x["kind"]=="g5_melee_cancelled"
                        and x["detail"].get("attacker")=="foe"]
        self.assertEqual([x["detail"]["action_index"] for x in cancellations],
                         list(seq["actions"]))
        self.assertTrue(all(x["detail"]["reason"]==
                            "attacker_dead_before_resolution"
                            and x["detail"]["damage_event_key"]==
                            "G5:independent:fatal-sentry"
                            and x["detail"]["ap_refunded"]==0
                            and x["detail"]["defense_commitments_refunded"] is False
                            for x in cancellations))
        self.assertEqual(scene.report()["ending"],"death_attested")
        self.assertFalse(scene.report()["unresolved_attack_slots"])
        before=len(e.ledger)
        with self.assertRaisesRegex(UnresolvedDecision,"Attacker incapacitated"):
            scene.resolve(seq,0,attack_face=11,damage_face=4,vigor_die=4)
        self.assertEqual(len(e.ledger),before)
        self.assertEqual(e.actors["front"].hp,12)
        self.assertFalse(any(x["kind"]=="g5_melee_roll" for x in e.ledger))
        scene.bridge.end_current_turn()
        self.assertEqual(e.current,None)
        e.check()

    def test_61_independent_g4_dying_cancels_soldier_without_fake_death(self):
        scene=fixed_scene("I1",seed=9461)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-03",),defenses=("guard",))
        front=e.actors["front"]
        committed_guard=front.guard_remaining
        e.g4.apply_damage("foe",(DamagePacket("hp","Fire",12),),
                          event_key="G5:independent:dying-soldier",
                          cause="independently_confirmed_fire",
                          wound_location_roll=11)
        foe=e.actors["foe"]
        self.assertEqual(foe.hp,0)
        self.assertFalse(foe.dead)
        self.assertFalse(scene.pending_attack_slots())
        self.assertEqual(front.guard_remaining,committed_guard)
        cancels=[x for x in e.ledger if x["kind"]=="g5_melee_cancelled"]
        self.assertEqual(len(cancels),1)
        self.assertEqual(cancels[0]["detail"]["action_index"],seq["actions"][0])
        self.assertEqual(cancels[0]["detail"]["reason"],
                         "attacker_dying_before_resolution")
        self.assertEqual(scene.report()["ending"],"unresolved")
        before=len(e.ledger)
        self.assertEqual(scene.cancel_incapacitated_attacker("foe"),())
        self.assertEqual(len(e.ledger),before)
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        self.assertEqual(front.hp,12)
        e.check()

    def test_62_allied_transit_finish_is_legal_authored_exit_evidence(self):
        front=party_actor("A",3,"front","party",occupied=((1,2),))
        ally=party_actor("B",3,"ally","party",occupied=((2,2),))
        foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((0,4),))
        e=Encounter([front,ally,foe],
                    {"front":30,"ally":20,"foe":10},
                    seed=9462,scenario="G5-allied-exit",
                    objective="front_exits_authorized_border",
                    policy="G1:clear_atomic_ally_transit")
        GridMovement(e,width=4,height=5,scene_id="G5-allied-route-map")
        SpellState(e)
        DamageState(e)
        e.begin_round()
        policy=SceneExit(e.scenario,e.g1.scene_id,e.objective,
                         "front",(3,2),"G5:author-approved-allied-exit")
        scene=SourceMelee(e,scene_exit=policy)
        scene.bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(e.g1.move_route("front",((1,0),(1,0))))
        self.assertEqual(front.occupied,((3,2),))
        self.assertFalse(any(x["kind"]=="g1_movement_step"
                             and x["detail"].get("actor")=="front"
                             for x in e.ledger))
        finished=[x for x in e.ledger if
                  x["kind"]=="g1_allied_transit_finished"]
        self.assertEqual(len(finished),1)
        result=scene.withdraw("front")
        self.assertEqual(result["status"],"withdrawal_attested")
        self.assertEqual(result["movement_event_index"],finished[0]["index"])
        self.assertEqual(scene.report()["ending"],"withdrawal_attested")
        self.assertFalse(scene.report()["unresolved_attack_slots"])
        self.assertEqual([x["detail"]["movement_index"] for x in e.ledger
                          if x["kind"]=="g5_terminal_exit"],
                         [finished[0]["index"]])
        e.check()

    def test_63_allied_transit_requires_last_completed_proof_at_exit(self):
        front=party_actor("A",3,"front","party",occupied=((1,2),))
        ally=party_actor("B",3,"ally","party",occupied=((2,2),))
        foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((0,4),))
        e=Encounter([front,ally,foe],
                    {"front":30,"ally":20,"foe":10},
                    seed=9463,scenario="G5-allied-exit-control",
                    objective="front_exits_authorized_border")
        GridMovement(e,width=4,height=5,scene_id="G5-allied-route-control")
        SpellState(e)
        DamageState(e)
        e.begin_round()
        policy=SceneExit(e.scenario,e.g1.scene_id,e.objective,
                         "front",(3,2),"G5:author-approved-allied-exit")
        scene=SourceMelee(e,scene_exit=policy)
        scene.bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(e.g1.move_route("front",((1,0),(1,0))))
        self.assertTrue(e.g1.step("front",(0,1),responses=lambda eligible:()))
        self.assertEqual(front.occupied,((3,3),))
        # Even a previously completed route to the exit cannot establish
        # an exit after the actor has moved back into the interior.
        before=e.serialize()
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "has not reached scene-authored exit square"):
            scene.withdraw("front")
        self.assertEqual(e.serialize(),before)
        self.assertEqual(scene.report()["ending"],"unresolved")
        e.check()



    def test_64_fatal_first_sentry_hit_retargets_funded_second_to_new_foe(self):
        sentry=enemy_actor("B06-EN-01","sentry","enemy",
                           start_state="prepared_start",occupied=((3,2),))
        first=party_actor("A",3,"first","party",occupied=((2,2),))
        second=party_actor("A",3,"second","party",occupied=((3,3),))
        e=Encounter([sentry,first,second],
                    {"sentry":30,"first":20,"second":10},
                    seed=9264,scenario="G5-paid-suffix-retarget",
                    objective="source_retarg_proof",policy="precommitted_dice")
        GridMovement(e,width=8,height=5)
        SpellState(e)
        DamageState(e)
        e.begin_round()
        scene=SourceMelee(e)
        first.hp=1
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("sentry","first",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","guard"))
        ap_after_payment=sentry.ap_remaining
        guard_after_payment=first.guard_remaining
        self.assertEqual(ap_after_payment,2)
        fatal=scene.resolve(seq,0,attack_face=20,confirmation_face=20,
                            critical_dice=(4,4),damage_face=6,vigor_die=4)
        self.assertTrue(fatal["damage"]["dead"])
        self.assertTrue(first.dead)
        self.assertEqual(len(scene.pending_attack_slots("sentry")),1)
        with self.assertRaisesRegex(UnresolvedDecision,"contact"):
            scene.resolve(seq,1,attack_face=11,damage_face=4,vigor_die=4)
        retarget=scene.retarget_remaining(
            seq,"second",defenses=("take_hit",))
        self.assertEqual(retarget["action_indices"],(seq["actions"][1],))
        self.assertEqual(sentry.ap_remaining,ap_after_payment)
        self.assertEqual(first.guard_remaining,guard_after_payment)
        self.assertEqual(e.actors["second"].guard_remaining,
                         e.actors["second"].guard_capacity)
        follow=scene.resolve(seq,1,attack_face=11,damage_face=4,vigor_die=4)
        self.assertEqual(follow["outcome"],"hit")
        self.assertEqual(follow["action_index"],seq["actions"][1])
        self.assertEqual(follow["damage"]["hp_loss"],9)
        self.assertEqual(second.hp,second.hp_max-9)
        self.assertEqual(second.vigor,second.vigor_max-2)
        self.assertFalse(scene.pending_attack_slots())
        self.assertEqual(sentry.ap_remaining,ap_after_payment)
        redirect=[x for x in e.ledger if x["kind"]=="g5_melee_retarget_committed"]
        self.assertEqual(len(redirect),1)
        self.assertEqual(redirect[0]["detail"]["profiles"],["B06-AT-02"])
        self.assertEqual(redirect[0]["detail"]["ap_spent"],0)
        self.assertFalse(redirect[0]["detail"]["old_defense_commitments_refunded"])
        self.assertEqual([x["detail"]["target"] for x in e.ledger
                          if x["kind"]=="g5_melee_resolved"],
                         ["first","second"])
        scene.bridge.end_current_turn()
        e.check()

    def test_65_illegal_retarget_rejected_before_new_defense_spend(self):
        sentry=enemy_actor("B06-EN-01","sentry","enemy",
                           start_state="prepared_start",occupied=((3,2),))
        first=party_actor("A",3,"first","party",occupied=((2,2),))
        distant=party_actor("A",3,"distant","party",occupied=((7,3),))
        e=Encounter([sentry,first,distant],
                    {"sentry":30,"first":20,"distant":10},
                    seed=9265,scenario="G5-no-free-redirection")
        GridMovement(e,width=8,height=5)
        SpellState(e)
        DamageState(e)
        e.begin_round()
        scene=SourceMelee(e)
        first.hp=1
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("sentry","first",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        scene.resolve(seq,0,attack_face=20,confirmation_face=20,
                      critical_dice=(4,4),damage_face=6,vigor_die=4)
        before=e.serialize()
        with self.assertRaisesRegex(UnresolvedDecision,"genuine live 1x1 G1 contact"):
            scene.retarget_remaining(seq,"distant",defenses=("dodge",))
        self.assertEqual(e.serialize(),before)
        self.assertEqual(len(scene.pending_attack_slots()),1)
        scene.decline_remaining(seq)
        scene.bridge.end_current_turn()
        e.check()

    def test_66_decline_disallowed_while_original_target_is_legal(self):
        scene=fixed_scene("I2",sentry_state="prepared_start")
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        miss=scene.resolve(seq,0,attack_face=1)
        self.assertEqual(miss["outcome"],"miss")
        before=e.serialize()
        with self.assertRaisesRegex(UnresolvedDecision,"unavailable target"):
            scene.decline_remaining(seq)
        self.assertEqual(e.serialize(),before)
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        scene.resolve(seq,1,attack_face=1)
        scene.bridge.end_current_turn()
        e.check()



    def test_67_lost_guard_instrument_preflight_preserves_paid_sequence(self):
        e,g=crossed_scene()
        g.bridge.start_next_turn(RegenerationChoice())
        attacker=e.actors["sentry"]
        defender=e.actors["soldier"]
        self.assertTrue(defender.ready_guard)
        self.assertIsNotNone(defender.guard_value)
        instrument=defender.guard_instrument
        self.assertTrue(instrument)
        # The Guard is still marked ready, but the actual instrument has
        # been lost independently before the sequence is declared.
        defender.guard_instrument=None
        before=e.serialize()
        resources=(attacker.ap_remaining,defender.guard_remaining,
                   defender.dodge_pressure,set(e.seen_sequences))
        with self.assertRaisesRegex(
            ValueError,"Cannot Guard without ready legal instrument"):
            g.declare("sentry","soldier",
                      profiles=("B06-AT-02","B06-AT-02"),
                      defenses=("take_hit","guard"))
        self.assertEqual(e.serialize(),before)
        self.assertEqual((attacker.ap_remaining,defender.guard_remaining,
                          defender.dodge_pressure,set(e.seen_sequences)),
                         resources)
        self.assertFalse(g.pending_attack_slots())
        self.assertFalse(g.report()["attacks"])
        self.assertFalse(any(x["kind"] in (
            "action_committed","attack_sequence_committed",
            "defense_assigned","g5_melee_sequence_attested")
            for x in e.ledger))
        # Restoration permits precisely one normally paid, fully tracked
        # two-slot sequence against the same target on the same own turn.
        defender.guard_instrument=instrument
        sequence=g.declare("sentry","soldier",
                            profiles=("B06-AT-02","B06-AT-02"),
                            defenses=("take_hit","guard"))
        self.assertEqual(attacker.ap_remaining,resources[0]-40)
        self.assertEqual(defender.guard_remaining,resources[1]-1)
        self.assertEqual(len(g.pending_attack_slots()),2)
        self.assertEqual(g.resolve(sequence,0,attack_face=1)["outcome"],"miss")
        self.assertEqual(g.resolve(sequence,1,attack_face=1)["outcome"],"miss")
        self.assertFalse(g.pending_attack_slots())
        g.bridge.end_current_turn()
        e.check()

    def test_68_lost_guard_in_first_slot_also_rejects_without_payment(self):
        e,g=crossed_scene()
        g.bridge.start_next_turn(RegenerationChoice())
        attacker=e.actors["sentry"]
        defender=e.actors["soldier"]
        saved=defender.guard_instrument
        self.assertTrue(defender.ready_guard)
        defender.guard_instrument=None
        before=(e.serialize(),attacker.ap_remaining,
                defender.guard_remaining,set(e.seen_sequences))
        with self.assertRaisesRegex(
            ValueError,"Cannot Guard without ready legal instrument"):
            g.declare("sentry","soldier",
                      profiles=("B06-AT-02",),defenses=("guard",))
        self.assertEqual((e.serialize(),attacker.ap_remaining,
                          defender.guard_remaining,set(e.seen_sequences)),before)
        self.assertFalse(g.pending_attack_slots())
        defender.guard_instrument=saved
        seq=g.declare("sentry","soldier",
                      profiles=("B06-AT-02",),defenses=("guard",))
        self.assertEqual(g.resolve(seq,0,attack_face=1)["outcome"],"miss")
        g.bridge.end_current_turn()
        e.check()


    def test_69_mp_reservation_waits_for_every_paid_g5_sequence_slot(self):
        scene=fixed_scene("I2",sentry_state="prepared_start",seed=9069)
        e=scene.e
        scene.bridge.start_next_turn(RegenerationChoice())
        attacker=e.actors["foe"]
        seq=scene.declare("foe","front",
                          profiles=("B06-AT-02","B06-AT-02"),
                          defenses=("take_hit","take_hit"))
        self.assertEqual(len(scene.pending_attack_slots("foe")),2)
        self.assertEqual(attacker.ap_remaining,2)

        def prove_reservation_rejected():
            # Snapshot all native and G1 bookkeeping before the attempt.
            before=(attacker.mp_remaining,attacker.ap_remaining,
                    attacker.occupied,e.serialize(),len(e.reservations),
                    dict(e.g1.motion),e.g1.next_reservation,
                    tuple(scene.pending_attack_slots("foe")))
            with self.assertRaisesRegex(
                    UnresolvedDecision,
                    "Complete committed G5 Attack Sequence before movement"):
                e.g1.reserve_movement("foe","later-movement-trigger",4,
                                      label="delayed-interception")
            self.assertEqual(
                (attacker.mp_remaining,attacker.ap_remaining,
                 attacker.occupied,e.serialize(),len(e.reservations),
                 dict(e.g1.motion),e.g1.next_reservation,
                 tuple(scene.pending_attack_slots("foe"))),before)
            self.assertFalse(any(x["kind"]=="g1_movement_mp_reserved"
                                 for x in e.ledger))

        # Cannot reserve immediately after the declaration...
        prove_reservation_rejected()
        # ...or after observing a first attack result while its pre-paid
        # second profile/defense is still committed and unresolved.
        first=scene.resolve(seq,0,attack_face=1)
        self.assertEqual(first["outcome"],"miss")
        self.assertEqual(len(scene.pending_attack_slots("foe")),1)
        prove_reservation_rejected()

        # The same valid reservation becomes legal as soon as the ordered
        # sequence is fully resolved. Only this call may mutate MP/registry.
        second=scene.resolve(seq,1,attack_face=1)
        self.assertEqual(second["outcome"],"miss")
        self.assertFalse(scene.pending_attack_slots("foe"))
        before_mp=attacker.mp_remaining
        before_ledger=len(e.ledger)
        token=e.g1.reserve_movement("foe","later-movement-trigger",4,
                                     label="delayed-interception")
        self.assertEqual(attacker.mp_remaining,before_mp-4)
        self.assertEqual(e.g1.next_reservation,1)
        self.assertIn(token,e.g1.motion)
        self.assertEqual(e.g1.motion[token].reserved_mp,4)
        self.assertEqual(len(e.reservations),1)
        self.assertEqual(e.reservations[0].trigger_key,"later-movement-trigger")
        self.assertEqual(e.ledger[before_ledger]["kind"],
                         "g1_movement_mp_reserved")
        scene.bridge.end_current_turn()
        e.check()

    def test_70_ordinary_g1_mp_reservation_remains_legal_without_g5(self):
        soldier=enemy_actor("B06-EN-02","soldier","enemy",
                            occupied=((3,2),))
        e=Encounter([soldier],{"soldier":30},seed=9070,
                    scenario="G1-no-G5-regression")
        movement=GridMovement(e,width=8,height=5)
        e.begin_round()
        e.start_turn("soldier",regen_choice=RegenerationChoice())
        self.assertIsNone(getattr(e,"g5",None))
        before=soldier.mp_remaining
        token=movement.reserve_movement("soldier","G1:independent",3,
                                        label="standalone-reserve")
        self.assertEqual(soldier.mp_remaining,before-3)
        self.assertEqual(len(e.reservations),1)
        self.assertIn(token,movement.motion)
        self.assertEqual(movement.motion[token].reserved_mp,3)
        self.assertEqual(movement.next_reservation,1)
        e.check()


    def test_71_dying_contact_blocks_paid_suffix_retarget_and_decline(self):
        """A first nonfatal HP crossing changes defense, NOT target legality.

        Test both 0 and negative HP and both precommitted active defenses.
        The eligible adjacent second opponent must not receive paid attacks
        until genuine original-target illegality occurs.
        """
        for original_hp in (6,5):
            for defense in ("guard","dodge"):
                with self.subTest(original_hp=original_hp,defense=defense):
                    sentry=enemy_actor("B06-EN-01","sentry","enemy",
                        start_state="prepared_start",occupied=((3,2),))
                    original=party_actor("A",3,"original","party",
                                         occupied=((2,2),))
                    replacement=party_actor("A",3,"replacement","party",
                                            occupied=((3,3),))
                    e=Encounter([sentry,original,replacement],
                        {"sentry":30,"original":20,"replacement":10},
                        seed=9271,scenario="G5-dying-still-legal-target",
                        objective="paid_suffix_stays_on_dying_target",
                        policy="fixed_dice_declared_defense")
                    GridMovement(e,width=8,height=5)
                    SpellState(e)
                    DamageState(e)
                    e.begin_round()
                    scene=SourceMelee(e)
                    original.hp=original_hp
                    scene.bridge.start_next_turn(RegenerationChoice())
                    seq=scene.declare("sentry","original",
                        profiles=("B06-AT-02","B06-AT-02"),
                        defenses=("take_hit",defense))
                    ap_paid=sentry.ap_remaining
                    guard_paid=original.guard_remaining
                    dodge_paid=original.dodge_pressure
                    first=scene.resolve(seq,0,attack_face=11,
                        damage_face=1,vigor_die=4,wound_location_roll=10)
                    self.assertEqual(first["outcome"],"hit")
                    self.assertEqual(first["damage"]["hp_loss"],6)
                    self.assertEqual(original.hp,original_hp-6)
                    self.assertLessEqual(original.hp,0)
                    self.assertFalse(original.dead)
                    self.assertTrue(e.g1.melee_contact("sentry","original"))
                    self.assertTrue(e.g1.melee_contact("sentry","replacement"))
                    self.assertEqual(len(scene.pending_attack_slots("sentry")),1)
                    before=e.serialize()
                    replacement_before=(replacement.guard_remaining,
                                        replacement.dodge_pressure,
                                        replacement.hp)
                    with self.assertRaisesRegex(UnresolvedDecision,
                                                "Original target remains legal"):
                        scene.retarget_remaining(seq,"replacement",
                                                 defenses=("take_hit",))
                    self.assertEqual(e.serialize(),before)
                    with self.assertRaisesRegex(UnresolvedDecision,
                                                "unavailable target"):
                        scene.decline_remaining(seq)
                    self.assertEqual(e.serialize(),before)
                    self.assertEqual(
                        (replacement.guard_remaining,
                         replacement.dodge_pressure,replacement.hp),
                         replacement_before)
                    self.assertEqual(len(scene.pending_attack_slots("sentry")),1)
                    self.assertFalse(any(x["kind"]=="g5_melee_retarget_committed"
                                         for x in e.ledger))
                    second=scene.resolve(seq,1,attack_face=2,
                                         damage_face=1,vigor_die=4)
                    self.assertEqual(second["outcome"],"hit")
                    self.assertEqual(second["defense"],"take_hit")
                    self.assertEqual(second["declared_defense"],defense)
                    self.assertEqual(second["damage"]["hp_loss"],6)
                    self.assertEqual(original.hp,original_hp-12)
                    self.assertEqual(replacement.hp,replacement.hp_max)
                    self.assertEqual(sentry.ap_remaining,ap_paid)
                    self.assertEqual(original.guard_remaining,guard_paid)
                    self.assertEqual(original.dodge_pressure,dodge_paid)
                    self.assertFalse(scene.pending_attack_slots("sentry"))
                    self.assertEqual([x["detail"]["target"] for x in e.ledger
                        if x["kind"]=="g5_melee_resolved"],
                        ["original","original"])
                    scene.bridge.end_current_turn()
                    e.check()


if __name__=="__main__":
    unittest.main()
