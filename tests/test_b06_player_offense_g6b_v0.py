"""G6-B: native audited player physical offense and G1/G0 reactive Opportunities."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_player_offense_g6b_v0 import (
    PlayerHunterCombat, PARTY_MELEE, party_weapon_profile,
)


def scene(*,with_b=False,head=(4,2),rear=(3,2),a_pos=(5,2),
          b_pos=(4,3)):
    actors=[enemy_actor("B06-EN-03","hunter","enemy",occupied=(head,rear)),
            party_actor("A",3,"a","party",occupied=(a_pos,))]
    if with_b:
        actors.append(party_actor("B",3,"b","party",occupied=(b_pos,)))
    e=Encounter(actors,{"hunter":30,"a":20,"b":10} if with_b else
                {"hunter":30,"a":20},seed=967,scenario="G6-B-authored",
                objective="bounded_party_offense_and_response")
    GridMovement(e,width=12,height=8)
    SpellState(e)
    DamageState(e)
    e.begin_round()
    c=PlayerHunterCombat(e)
    c.bridge.start_next_turn(RegenerationChoice())
    return e,c


def go_to(e,c,actor_id):
    while e.current!=actor_id:
        if e.current is not None:
            c.bridge.end_current_turn()
        if e.current is None:
            c.bridge.start_next_turn(RegenerationChoice())


def events(e,kind):
    return [x for x in e.ledger if x["kind"]==kind]


class G6BTests(unittest.TestCase):
    def test_01_player_profiles_match_verified_attack_and_damage(self):
        e,c=scene(with_b=True)
        for role,who in (("A","a"),("B","b")):
            src=e.actors[who]
            profile,bonus=party_weapon_profile(src,PARTY_MELEE[role][0])
            self.assertEqual(bonus,7 if role=="A" else 6)
            self.assertEqual(profile["primary_hp_packet"]["armor_penetration"],
                             2 if role=="A" else 3)
            self.assertEqual(src.source.attack_profiles,(PARTY_MELEE[role][0],))
        self.assertIsNone(e.actors["hunter"].guard_instrument)
        e.check()

    def test_02_a_sword_own_turn_pays_native_g0_and_attests_g45(self):
        e,c=scene()
        go_to(e,c,"a")
        s=c.declare("a","hunter",profiles=("B06-PC-A-SWORD",),
                    defenses=("take_hit",))
        self.assertEqual(e.actors["a"].ap_remaining,22)
        outcome=c.resolve(s,0,attack_face=10,damage_face=2)
        self.assertEqual(outcome["outcome"],"hit")
        self.assertEqual(outcome["damage"]["hp_loss"],5)
        self.assertEqual(e.actors["hunter"].hp,9)
        self.assertEqual(len(events(e,"g5_melee_resolved")),1)
        self.assertEqual(len(events(e,"g45_attested_hit")),1)
        self.assertEqual(events(e,"g4_profile_hit")[-1]["detail"]["profile"],
                         "B06-PC-A-SWORD")
        c.bridge.end_current_turn()
        e.check()

    def test_03_b_mace_own_turn_penetration_and_crush(self):
        e,c=scene(with_b=True)
        go_to(e,c,"b")
        s=c.declare("b","hunter",profiles=("B06-PC-B-MACE",),
                    defenses=("dodge",))
        # Hunter: first source Dodge 14. Attack 10+6=16 exceeds it.
        result=c.resolve(s,0,attack_face=10,damage_face=2)
        self.assertEqual(result["outcome"],"hit")
        self.assertEqual(result["damage"]["hp_loss"],8)
        self.assertEqual(e.actors["hunter"].hp,6)
        self.assertEqual(e.actors["hunter"].dodge_pressure,2)
        self.assertEqual(events(e,"g4_damage_applied")[-1]["detail"]["cause"],
                         "source-profile:B06-PC-B-MACE")
        e.check()

    def test_04_two_real_player_slots_preserve_precommitted_dodge_pressure(self):
        e,c=scene()
        go_to(e,c,"a")
        s=c.declare("a","hunter",profiles=("B06-PC-A-SWORD",)*2,
                    defenses=("dodge","dodge"))
        self.assertEqual(e.actors["a"].ap_remaining,2)
        self.assertEqual(e.actors["hunter"].dodge_pressure,4)
        with self.assertRaises(UnresolvedDecision):
            c.resolve(s,1,attack_face=7,damage_face=1)
        first=c.resolve(s,0,attack_face=7)
        second=c.resolve(s,1,attack_face=7,damage_face=1)
        self.assertEqual((first["outcome"],second["outcome"]),("miss","hit"))
        self.assertEqual((first["defense_value"],second["defense_value"]),(14,12))
        self.assertEqual(e.actors["hunter"].hp,10)
        self.assertEqual(len(events(e,"g5_melee_resolved")),2)
        e.check()

    def test_05_invalid_player_sources_and_hunter_guard_rejected_before_ap(self):
        e,c=scene(with_b=True)
        go_to(e,c,"a")
        ap=e.actors["a"].ap_remaining
        with self.assertRaises(UnresolvedDecision):
            e.declare_sequence("a","hunter",("B06-PC-A-SWORD",),("take_hit",))
        with self.assertRaises(UnresolvedDecision):
            c.declare("a","hunter",profiles=("B06-PC-B-MACE",),
                      defenses=("take_hit",))
        with self.assertRaises(ValueError):
            c.declare("a","hunter",profiles=("B06-PC-A-SWORD",),
                      defenses=("guard",))
        self.assertEqual(e.actors["a"].ap_remaining,ap)
        self.assertFalse(events(e,"attack_sequence_committed"))
        self.assertEqual(e.actors["hunter"].guard_remaining,1)
        self.assertIsNone(e.actors["hunter"].guard_instrument)
        e.check()

    def test_06_player_wound_requires_precommitted_location_before_roll(self):
        e,c=scene()
        go_to(e,c,"a")
        e.actors["hunter"].hp=5
        s=c.declare("a","hunter",profiles=("B06-PC-A-SWORD",),
                    defenses=("take_hit",))
        before=len(e.ledger)
        with self.assertRaises(UnresolvedDecision):
            c.resolve(s,0,attack_face=10,damage_face=4)
        self.assertEqual(len(e.ledger),before)
        self.assertEqual(e.actors["hunter"].hp,5)
        result=c.resolve(s,0,attack_face=10,damage_face=4,
                         wound_location_roll=8)
        self.assertEqual(result["outcome"],"hit")
        self.assertEqual(result["damage"]["hp_loss"],7)
        self.assertEqual(e.actors["hunter"].hp,-2)
        self.assertEqual(len(e.actors["hunter"].wounds),1)
        self.assertEqual(len(events(e,"g45_attested_hit")),1)
        e.check()

    def test_07_natural_one_player_attack_never_mints_damage(self):
        e,c=scene()
        go_to(e,c,"a")
        s=c.declare("a","hunter",profiles=("B06-PC-A-SWORD",),
                    defenses=("take_hit",))
        hit=c.resolve(s,0,attack_face=1)
        self.assertEqual(hit["outcome"],"miss")
        self.assertEqual(e.actors["hunter"].hp,14)
        self.assertFalse(events(e,"g4_profile_hit"))
        e.check()

    def test_08_missed_opportunity_spends_reaction_and_allows_hunter_step(self):
        e,c=scene()
        ap=e.actors["a"].ap_remaining
        before=e.actors["hunter"].hp
        out=c.step_with_opportunity("hunter",(-1,0),"a",
                                    attack_face=1)
        self.assertTrue(out["movement_completed"])
        self.assertEqual(out["opportunity"]["outcome"],"miss")
        self.assertEqual(e.actors["hunter"].occupied,((3,2),(2,2)))
        self.assertEqual(e.actors["hunter"].hp,before)
        self.assertFalse(e.actors["a"].reaction_available)
        self.assertEqual(e.actors["a"].opportunity_used,1)
        self.assertEqual(e.actors["a"].ap_remaining,ap)
        self.assertEqual(len(events(e,"g6b_opportunity_resolved")),1)
        self.assertFalse(events(e,"g4_profile_hit"))
        e.check()

    def test_09_real_opportunity_hit_precedes_hunter_movement(self):
        e,c=scene()
        out=c.step_with_opportunity("hunter",(-1,0),"a",
                                    defense="dodge",attack_face=10,
                                    damage_face=2)
        # First Hunter dodge is 14; A's 10+7=17 hits. A's Sword is 5 HP.
        self.assertTrue(out["movement_completed"])
        self.assertEqual(out["opportunity"]["outcome"],"hit")
        self.assertEqual(e.actors["hunter"].hp,9)
        self.assertEqual(e.actors["hunter"].dodge_pressure,2)
        self.assertEqual(len(events(e,"g4_profile_hit")),1)
        step=events(e,"g1_movement_step")[-1]
        self.assertLess(events(e,"g6b_opportunity_resolved")[-1]["index"],
                        step["index"])
        self.assertEqual(out["opportunity"]["damage"]["hp_loss"],5)
        e.check()

    def test_10_opportunity_incapacitation_interrupts_step_with_real_wound(self):
        e,c=scene()
        e.actors["hunter"].hp=3
        out=c.step_with_opportunity("hunter",(-1,0),"a",
                                    attack_face=10,damage_face=4,
                                    wound_location_roll=9)
        self.assertFalse(out["movement_completed"])
        self.assertEqual(out["opportunity"]["outcome"],"hit")
        self.assertEqual(e.actors["hunter"].occupied,((4,2),(3,2)))
        self.assertTrue(e.actors["hunter"].hp<=0)
        self.assertEqual(len(e.actors["hunter"].wounds),1)
        self.assertTrue(events(e,"g1_step_cancelled"))
        self.assertEqual(len(events(e,"g6b_opportunity_resolved")),1)
        e.check()

    def test_11_invalid_opportunity_rejected_before_reaction_or_movement(self):
        # The PC is deliberately too far away to threaten *any* Hunter
        # departure cell. A sidestep that leaves a threatened cell can
        # legitimately provoke even when the mover stays adjacent.
        e,c=scene(a_pos=(7,2))
        original=(e.actors["hunter"].occupied,
                  e.actors["a"].reaction_available,
                  e.actors["a"].opportunity_used,len(e.ledger))
        with self.assertRaises(UnresolvedDecision):
            c.step_with_opportunity("hunter",(-1,0),"a",attack_face=12,
                                    damage_face=2)
        self.assertEqual((e.actors["hunter"].occupied,
                          e.actors["a"].reaction_available,
                          e.actors["a"].opportunity_used,len(e.ledger)),original)
        e.check()

        normal,combat=scene()
        with self.assertRaises(UnresolvedDecision):
            combat.step_with_opportunity("hunter",(-1,0),"a",
                                         defense="guard",attack_face=10,
                                         damage_face=2)
        self.assertEqual(normal.actors["a"].opportunity_used,0)
        self.assertTrue(normal.actors["a"].reaction_available)
        normal.check()

    def test_12_missing_wound_roll_blocks_response_before_reaction_spend(self):
        e,c=scene()
        e.actors["hunter"].hp=3
        original=(e.actors["hunter"].occupied,
                  e.actors["a"].reaction_available,len(e.ledger))
        with self.assertRaises(UnresolvedDecision):
            c.step_with_opportunity("hunter",(-1,0),"a",
                                    attack_face=10,damage_face=4)
        self.assertEqual((e.actors["hunter"].occupied,
                          e.actors["a"].reaction_available,len(e.ledger)),original)
        self.assertFalse(events(e,"spontaneous_committed"))
        e.check()

    def test_13_source_response_cannot_claim_unpaid_attack_twice(self):
        e,c=scene()
        out=c.step_with_opportunity("hunter",(-1,0),"a",
                                    attack_face=11,damage_face=1)
        proof=events(e,"g6b_opportunity_resolved")[-1]["detail"]
        commit=e.ledger[proof["response_index"]]
        self.assertEqual(commit["kind"],"spontaneous_committed")
        self.assertEqual(commit["detail"]["response_kind"],"opportunity")
        self.assertFalse(e.is_live_spontaneous(None,None))
        self.assertEqual(e.actors["a"].opportunity_used,1)
        with self.assertRaises(UnresolvedDecision):
            c.step_with_opportunity("hunter",(-1,0),"a",
                                    attack_face=10,damage_face=1)
        self.assertEqual(len(events(e,"g6b_opportunity_resolved")),1)
        e.check()


if __name__=="__main__":
    unittest.main()
