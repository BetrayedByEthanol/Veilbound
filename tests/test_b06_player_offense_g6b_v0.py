"""G6-B: native audited player physical offense and G1/G0 reactive Opportunities."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState, DamagePacket
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



def suffix_scene(*,role="A",alternate_hunter=False):
    """Genuine native sequence with one adjacent non-Hunter redirect decoy."""
    actors=[
        enemy_actor("B06-EN-03","hunter","enemy",
                    occupied=((4,2),(3,2))),
        enemy_actor("B06-EN-02","soldier","enemy",
                    occupied=((5,3),)),
        party_actor(role,3,"hero","party",occupied=((5,2),)),
    ]
    scores={"hunter":40,"soldier":10,"hero":20}
    if alternate_hunter:
        actors.append(enemy_actor("B06-EN-03","second_hunter","enemy",
                                  occupied=((6,2),(7,2))))
        scores["second_hunter"]=30
    e=Encounter(actors,scores,seed=968,
                scenario="G6-B-paid-suffix",
                objective="source_bound_hunter_suffix")
    GridMovement(e,width=12,height=8)
    SpellState(e)
    DamageState(e)
    e.begin_round()
    combat=PlayerHunterCombat(e)
    combat.bridge.start_next_turn(RegenerationChoice())
    go_to(e,combat,"hero")
    return e,combat



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


    def test_14_live_two_cell_hunter_keeps_paid_a_sword_suffix(self):
        e,c=suffix_scene()
        seq=c.declare("hero","hunter",profiles=("B06-PC-A-SWORD",)*2,
                      defenses=("take_hit","take_hit"))
        first=c.resolve(seq,0,attack_face=1)
        self.assertEqual(first["outcome"],"miss")
        self.assertFalse(c._paid_target_unavailable("hero","hunter"))
        before=(len(e.ledger),e.actors["soldier"].dodge_pressure,
                e.actors["hero"].ap_remaining,
                tuple(c.pending_attack_slots("hero")))
        with self.assertRaisesRegex(UnresolvedDecision,"remains legal"):
            c.retarget_remaining(seq,"soldier",defenses=("dodge",))
        with self.assertRaisesRegex(UnresolvedDecision,"unavailable target"):
            c.decline_remaining(seq)
        self.assertEqual((len(e.ledger),e.actors["soldier"].dodge_pressure,
                          e.actors["hero"].ap_remaining,
                          tuple(c.pending_attack_slots("hero"))),before)
        second=c.resolve(seq,1,attack_face=10,damage_face=1)
        self.assertEqual(second["outcome"],"hit")
        self.assertEqual(second["damage"]["hp_loss"],4)
        self.assertEqual(e.actors["hunter"].hp,10)
        self.assertFalse(events(e,"g5_melee_retarget_committed"))
        self.assertFalse(events(e,"g5_melee_cancelled"))
        e.check()

    def test_15_dying_two_cell_hunter_keeps_paid_b_mace_suffix(self):
        e,c=suffix_scene(role="B")
        e.actors["hunter"].hp=1
        seq=c.declare("hero","hunter",profiles=("B06-PC-B-MACE",)*2,
                      defenses=("take_hit","take_hit"))
        first=c.resolve(seq,0,attack_face=10,damage_face=1,
                        wound_location_roll=8)
        self.assertEqual(first["damage"]["hp_loss"],7)
        self.assertLessEqual(e.actors["hunter"].hp,0)
        self.assertFalse(e.actors["hunter"].dead)
        self.assertFalse(c._paid_target_unavailable("hero","hunter"))
        before=(len(e.ledger),e.actors["soldier"].dodge_pressure,
                e.actors["hero"].ap_remaining)
        with self.assertRaisesRegex(UnresolvedDecision,"remains legal"):
            c.retarget_remaining(seq,"soldier",defenses=("dodge",))
        with self.assertRaisesRegex(UnresolvedDecision,"unavailable target"):
            c.decline_remaining(seq)
        self.assertEqual((len(e.ledger),e.actors["soldier"].dodge_pressure,
                          e.actors["hero"].ap_remaining),before)
        second=c.resolve(seq,1,attack_face=1)
        self.assertEqual(second["outcome"],"miss")
        self.assertFalse(c.pending_attack_slots("hero"))
        e.check()

    def test_16_dead_hunter_cannot_redirect_paid_a_slot_to_soldier(self):
        e,c=suffix_scene()
        e.actors["hunter"].hp=1
        seq=c.declare("hero","hunter",profiles=("B06-PC-A-SWORD",)*2,
                      defenses=("take_hit","take_hit"))
        c.resolve(seq,0,attack_face=10,damage_face=1,
                  wound_location_roll=8)
        # An independently confirmed lethal G4 event now makes the
        # originally declared Hunter genuinely unavailable.
        e.g4.apply_damage(
            "hunter",(DamagePacket("hp","Toxin",20),),
            event_key="g6b:test:separate_lethal_toxin",
            cause="test:independently_confirmed_toxin")
        self.assertTrue(e.actors["hunter"].dead)
        self.assertTrue(c._paid_target_unavailable("hero","hunter"))
        before=(len(e.ledger),e.actors["soldier"].dodge_pressure,
                e.actors["soldier"].guard_remaining,
                tuple(c.pending_attack_slots("hero")))
        with self.assertRaisesRegex(UnresolvedDecision,"source-authorized"):
            c.retarget_remaining(seq,"soldier",defenses=("dodge",))
        self.assertEqual((len(e.ledger),e.actors["soldier"].dodge_pressure,
                          e.actors["soldier"].guard_remaining,
                          tuple(c.pending_attack_slots("hero"))),before)
        self.assertFalse(events(e,"g5_melee_retarget_committed"))
        # An explicitly declined, already-paid suffix is still legal
        # against a genuinely unavailable/dead Hunter, without AP refund.
        ap=e.actors["hero"].ap_remaining
        self.assertEqual(c.decline_remaining(seq),
                         (seq["actions"][1],))
        self.assertEqual(e.actors["hero"].ap_remaining,ap)
        self.assertFalse(c.pending_attack_slots("hero"))
        e.check()

    def test_17_unavailable_hunter_retargets_only_another_live_hunter(self):
        e,c=suffix_scene(role="B",alternate_hunter=True)
        e.actors["hunter"].hp=1
        seq=c.declare("hero","hunter",profiles=("B06-PC-B-MACE",)*2,
                      defenses=("take_hit","take_hit"))
        c.resolve(seq,0,attack_face=10,damage_face=1,
                  wound_location_roll=8)
        e.g4.apply_damage(
            "hunter",(DamagePacket("hp","Toxin",20),),
            event_key="g6b:test:second_lethal_toxin",
            cause="test:independently_confirmed_toxin")
        self.assertTrue(e.actors["hunter"].dead)
        before_ap=e.actors["hero"].ap_remaining
        reassigned=c.retarget_remaining(
            seq,"second_hunter",defenses=("take_hit",))
        self.assertEqual(reassigned["action_indices"],(seq["actions"][1],))
        self.assertEqual(e.actors["hero"].ap_remaining,before_ap)
        second=c.resolve(seq,1,attack_face=10,damage_face=1)
        self.assertEqual(second["outcome"],"hit")
        self.assertEqual(second["damage"]["hp_loss"],7)
        self.assertEqual(e.actors["second_hunter"].hp,7)
        self.assertFalse(c.pending_attack_slots("hero"))
        self.assertEqual(events(e,"g5_melee_resolved")[-1]["detail"]["target"],
                         "second_hunter")
        self.assertEqual(len(events(e,"g5_melee_retarget_committed")),1)
        e.check()


if __name__=="__main__":
    unittest.main()
