"""B06 G2: deterministic authored firing-lane, response and resource traces."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, Response, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat, CoverSurface, ShotChoice


def hero(kind, ident, at, team="party"):
    return party_actor(kind, 3, ident, team, occupied=(at,))


def soldier(ident, at, team="enemy"):
    return enemy_actor("B06-EN-02", ident, team, occupied=(at,))


def hunter(at=((6, 2), (5, 2))):
    return enemy_actor("B06-EN-03", "hunter", "enemy", occupied=at)


def fixture(*actors, cover=(), walls=(), terrain=None, width=24, score=None):
    scores = score or {a.id: 100-i for i,a in enumerate(actors)}
    e = Encounter(list(actors), scores, seed=4402,
                  tie_order=tuple(a.id for a in actors), scenario="G2-authored",
                  policy="explicit_G2_shot_dice")
    g1 = GridMovement(e, width=width, height=7, walls=walls, terrain=terrain)
    g2 = RangedCombat(e, cover=cover)
    e.begin_round()
    return e,g1,g2


def result(e):
    return [v for v in e.ledger if v["kind"] == "g2_bow_shot_resolved"]


class G2RangedAcceptance(unittest.TestCase):
    def test_01_mixed_lane_cover_ally_enemy_one_highest_penalty(self):
        r=hero("R","archer",(1,2))
        ally=hero("A","ally",(3,2))
        guard=soldier("screen",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,ally,guard,target,cover=(CoverSurface((7,2),4,(1,0)),))
        lane=g2.lane("archer","target",exposures=(("ally",2),("screen",6)))
        self.assertEqual((lane.cover,lane.effective_obstruction,lane.range_difficulty),(4,6,0))
        self.assertEqual(tuple(x[0] for x in lane.screens),("ally","screen"))
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=3,exposures=(("ally",2),("screen",6)),
            collateral=(("ally","take_hit"),("screen","guard")),
            secondary_face=14),))
        self.assertEqual(out[0]["outcome"],"collateral_hit_pending_G5")
        self.assertEqual(out[0]["target"],"ally")
        self.assertEqual(r.ammunition,19)
        self.assertEqual(r.ap_remaining,22)
        self.assertEqual(guard.guard_remaining,guard.guard_capacity)
        log=[v for v in e.ledger if v["kind"]=="g2_miss_faces_preallocated"][0]
        faces={int(k):tuple(v) for k,v in log["detail"]["faces"].items()}
        self.assertEqual(faces[2],("creature","ally"))
        self.assertEqual(faces[3],("creature","ally"))
        self.assertEqual(faces[9],("cover",None))
        self.assertEqual(faces[12],("cover",None))
        self.assertEqual(faces[8],("creature","screen"))
        self.assertEqual(len([x for x in e.ledger
                              if x["kind"]=="g2_conditional_secondary"]),1)
        e.check()

    def test_02_cover_only_one_roll_strikes_surface_no_secondary(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,target,cover=(CoverSurface((5,2),4,(1,0)),))
        e.start_turn("archer")
        shots=(ShotChoice(primary_face=8),ShotChoice(primary_face=6))
        out=g2.bow_sequence("archer","target",shots)
        self.assertEqual(tuple(x["outcome"] for x in out),
                         ("cover_impact","ordinary_miss"))
        self.assertEqual(r.ammunition,18)
        self.assertEqual(r.ap_remaining,2)
        self.assertEqual((out[0]["base_defense"],out[0]["final_defense"]),(10,14))
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="g2_conditional_secondary"]),0)
        e.check()

    def test_03_full_wall_illegal_no_ap_ammo_or_defense(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,target,walls=((5,2),))
        e.start_turn("archer")
        before=(r.ap_remaining,r.ammunition,target.guard_remaining,len(e.ledger))
        with self.assertRaisesRegex(ValueError,"physically usable"):
            g2.bow_sequence("archer","target",(ShotChoice(primary_face=20),))
        self.assertEqual((r.ap_remaining,r.ammunition,
                          target.guard_remaining,len(e.ledger)),before)
        self.assertNotIn(("archer","target"),e.seen_sequences)

    def test_04_projectile_shield_guard_spends_capacity(self):
        r=hero("R","archer",(1,2))
        target=soldier("target",(8,2))
        e,g1,g2=fixture(r,target)
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            defense="guard",primary_face=10),))[0]
        self.assertEqual(out["outcome"],"intended_guard_impact")
        self.assertEqual(target.guard_remaining,1)
        self.assertEqual(target.dodge_pressure,0)
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_05_bow_cannot_guard_despite_guard_reserve_talent(self):
        r=hero("R","archer",(1,2))
        other=hero("R","bow_target",(8,2),"enemy")
        e,g1,g2=fixture(r,other)
        e.start_turn("archer")
        before=(r.ap_remaining,r.ammunition,other.guard_remaining)
        with self.assertRaisesRegex(ValueError,"projectile-capable shield"):
            g2.bow_sequence("archer","bow_target",(ShotChoice(
                defense="guard",primary_face=7),))
        self.assertEqual((r.ap_remaining,r.ammunition,other.guard_remaining),before)

    def test_06_threatened_bow_hit_interrupts_prelaunch_only_ap_spent(self):
        threat=soldier("threat",(2,3))
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(threat,r,target,score={"threat":30,"archer":20,"target":10})
        e.start_turn("threat")
        e.end_turn()
        e.start_turn("archer")
        self.assertTrue(g1.threatens("threat",(1,2)))
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=20,trigger_key="threat-shot",
            opportunities=(Response("threat","opportunity","blade-counter"),),
            on_opportunity=lambda response:True),))[0]
        self.assertEqual(out["outcome"],"interrupted_before_launch")
        self.assertEqual(r.ammunition,20)
        self.assertEqual(r.ap_remaining,22)
        self.assertEqual(target.guard_remaining,target.guard_capacity)
        self.assertEqual(threat.opportunity_used,1)
        self.assertFalse(threat.reaction_available)
        self.assertEqual(len(result(e)),0)
        e.check()

    def test_07_threatened_bow_nonhit_launches_single_arrow(self):
        threat=soldier("threat",(2,3))
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(threat,r,target,score={"threat":30,"archer":20,"target":10})
        e.start_turn("threat");e.end_turn();e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=14,opportunities=(Response("threat","opportunity","miss"),),
            on_opportunity=lambda response:False),))[0]
        self.assertEqual(out["outcome"],"intended_hit_pending_G5")
        self.assertEqual(r.ammunition,19)
        self.assertEqual(threat.opportunity_used,1)
        e.check()

    def test_08_precommitted_interception_blocking_lane_no_launch(self):
        interceptor=soldier("interceptor",(5,3))
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(interceptor,r,target,
                         score={"interceptor":30,"archer":20,"target":10})
        e.start_turn("interceptor")
        key=g1.reserve_movement("interceptor","arrow-trigger",2,label="step_into_lane")
        e.end_turn()
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=20,trigger_key="arrow-trigger",
            interceptor_routes={key:((0,-1),)}),))[0]
        self.assertEqual(out["outcome"],"interrupted_before_launch")
        self.assertEqual(interceptor.occupied,((5,2),))
        self.assertEqual(r.ammunition,20)
        self.assertEqual(r.ap_remaining,22)
        self.assertEqual(interceptor.opportunity_used,0)
        e.check()

    def test_09_explicit_aim_range_reduces_one_source_not_attack_bonus(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(16,2),"enemy")
        e,g1,g2=fixture(r,target)
        e.start_turn("archer")
        g2.aim("archer","target","range")
        self.assertEqual(r.ap_remaining,22)
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=7,aim_source="range"),))[0]
        self.assertEqual((out["base_defense"],out["final_defense"]),(10,10))
        self.assertEqual(out["outcome"],"intended_hit_pending_G5")
        self.assertEqual(r.ap_remaining,2)
        self.assertEqual(r.ammunition,19)
        self.assertNotIn("archer",g2.aims)
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="g2_aim_consumed"]),1)
        e.check()

    def test_10_aim_expires_on_start_of_second_subsequent_turn(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(16,2),"enemy")
        e,g1,g2=fixture(r,target)
        e.start_turn("archer")
        g2.aim("archer","target","range")
        e.end_turn();e.start_turn("target");e.end_turn();e.begin_round()
        e.start_turn("archer")
        self.assertIn("archer",g2.aims)
        e.end_turn();e.start_turn("target");e.end_turn();e.begin_round()
        e.start_turn("archer")
        self.assertNotIn("archer",g2.aims)
        e.check()

    def test_11_aim_breaks_only_after_successful_position_change(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(16,2),"enemy")
        e,g1,g2=fixture(r,target)
        e.start_turn("archer")
        g2.aim("archer","target","range")
        self.assertTrue(g1.step("archer",(0,1)))
        self.assertNotIn("archer",g2.aims)
        e.check()

    def test_12_aim_on_living_screen_narrows_only_that_band(self):
        r=hero("R","archer",(1,2))
        ally=hero("A","ally",(3,2))
        enemy=soldier("enemy",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,ally,enemy,target,cover=(CoverSurface((7,2),4,(1,0)),))
        e.start_turn("archer")
        g2.aim("archer","target","screen:ally",
               exposures=(("ally",2),("enemy",6)))
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=2,aim_source="screen:ally",
            exposures=(("ally",2),("enemy",6)),
            collateral=(("ally","take_hit"),("enemy","take_hit"))),))[0]
        self.assertNotEqual(out["outcome"],"collateral_hit_pending_G5")
        allocation=[v for v in e.ledger if v["kind"]=="g2_miss_faces_preallocated"][0]
        self.assertNotIn("2",allocation["detail"]["faces"] if False else {
            k for k,v in allocation["detail"]["faces"].items()
            if v[0]=="creature" and v[1]=="ally"})
        self.assertEqual(out["ammunition_spent"],1)
        e.check()

    def test_13_only_selected_incidental_guard_uses_capacity(self):
        r=hero("R","archer",(1,2))
        enemy=soldier("screen",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,enemy,target)
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=4,exposures=(("screen",4),),
            collateral=(("screen","guard"),),secondary_face=2),))[0]
        self.assertEqual(out["outcome"],"collateral_guard_impact")
        self.assertEqual(enemy.guard_remaining,1)
        self.assertEqual(r.ammunition,19)
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="g2_conditional_secondary"]),1)
        e.check()

    def test_14_conditional_defender_does_not_spend_on_direct_hit(self):
        r=hero("R","archer",(1,2))
        enemy=soldier("screen",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,enemy,target)
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=20,exposures=(("screen",4),),
            collateral=(("screen","guard"),)),))[0]
        self.assertEqual(out["outcome"],"critical_confirmation_pending_G5")
        self.assertEqual(enemy.guard_remaining,2)
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_15_flame_3_square_physical_only_no_cast_or_vp_spent(self):
        f=hero("F","scholar",(1,2))
        prey=hero("A","prey",(4,2),"enemy")
        e,g1,g2=fixture(f,prey)
        before=(f.ap_remaining,f.vp_available,f.vp_spent,f.ammunition)
        lane=g2.preview_thrown_flame("scholar","prey")
        self.assertEqual((lane.distance,lane.range_difficulty),(3,0))
        self.assertEqual((f.ap_remaining,f.vp_available,
                          f.vp_spent,f.ammunition),before)
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="g2_flame_lane_preview"]),1)
        e.check()

    def test_16_flame_cannot_assume_cast_through_unmodelled_screen(self):
        f=hero("F","scholar",(1,2))
        screen=hero("B","screen",(3,2))
        prey=hero("A","prey",(4,2),"enemy")
        e,g1,g2=fixture(f,screen,prey)
        with self.assertRaisesRegex(UnresolvedDecision,"Living Screen"):
            g2.preview_thrown_flame("scholar","prey")
        lane=g2.preview_thrown_flame("scholar","prey",
                                    exposures=(("screen",4),))
        self.assertEqual(lane.effective_obstruction,4)
        self.assertFalse(any(v["kind"]=="vp_transition" for v in e.ledger))
        e.check()

    def test_17_aim_consumes_on_interrupted_attack(self):
        threat=soldier("threat",(2,3))
        r=hero("R","archer",(1,2))
        target=hero("B","target",(16,2),"enemy")
        e,g1,g2=fixture(threat,r,target,score={"threat":30,"archer":20,"target":10})
        e.start_turn("threat");e.end_turn();e.start_turn("archer")
        g2.aim("archer","target","range")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=20,aim_source="range",
            opportunities=(Response("threat","opportunity","hit"),),
            on_opportunity=lambda _:True),))[0]
        self.assertEqual(out["outcome"],"interrupted_before_launch")
        self.assertNotIn("archer",g2.aims)
        self.assertEqual(r.ammunition,20)
        self.assertEqual(r.ap_remaining,2)
        e.check()

    def test_18_invalid_fully_blocked_shot_does_not_spend_aim_or_ap(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(16,2),"enemy")
        e,g1,g2=fixture(r,target,walls=((9,2),))
        e.start_turn("archer")
        before=(r.ap_remaining,r.ammunition)
        with self.assertRaisesRegex(ValueError,"physically usable"):
            g2.bow_sequence("archer","target",(ShotChoice(primary_face=20),))
        self.assertEqual((r.ap_remaining,r.ammunition),before)
        e.check()

    def test_19_second_attack_sequence_same_target_rejected(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,target)
        e.start_turn("archer")
        g2.bow_sequence("archer","target",(ShotChoice(primary_face=6),))
        self.assertEqual(r.ap_remaining,22)
        with self.assertRaisesRegex(ValueError,"second Attack Sequence"):
            g2.bow_sequence("archer","target",(ShotChoice(primary_face=20),))
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_20_second_conditional_accuracy_never_another_arrow(self):
        r=hero("R","archer",(1,2))
        ally=hero("A","ally",(3,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,ally,target)
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=2,exposures=(("ally",2),),
            collateral=(("ally","take_hit"),),secondary_face=19),))[0]
        self.assertEqual(out["outcome"],"collateral_hit_pending_G5")
        self.assertEqual(r.ammunition,19)
        self.assertEqual(r.ap_remaining,22)
        self.assertEqual(len([v for v in e.ledger if v["kind"]=="g2_conditional_secondary"]),1)
        e.check()

    def test_21_ready_dagger_is_paid_and_bow_shot_no_longer_legal(self):
        r=hero("R","archer",(1,2))
        t=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,t)
        e.start_turn("archer")
        g2.ready_weapon("archer","Dagger")
        self.assertEqual(r.ap_remaining,18)
        with self.assertRaisesRegex(ValueError,"wielded Bow"):
            g2.bow_sequence("archer","target",(ShotChoice(primary_face=12),))
        self.assertEqual(r.ammunition,20)
        e.check()


if __name__ == "__main__":
    unittest.main()
