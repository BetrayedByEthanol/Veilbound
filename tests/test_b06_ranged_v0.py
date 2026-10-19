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
            aware_collateral=("screen",),secondary_face=14),))
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
            defense="guard",aware_target=True,primary_face=10),))[0]
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
                defense="guard",aware_target=True,primary_face=7),))
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
            primary_face=8,exposures=(("screen",4),),
            collateral=(("screen","guard"),),
            aware_collateral=("screen",),secondary_face=2),))[0]
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
            collateral=(("screen","guard"),),
            aware_collateral=("screen",)),))[0]
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

    def test_22_unaware_collateral_shield_cannot_be_predeclared(self):
        r=hero("R","archer",(1,2))
        screen=soldier("screen",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,screen,target)
        e.start_turn("archer")
        before=(r.ap_remaining,r.ammunition,screen.guard_remaining,len(e.ledger))
        with self.assertRaisesRegex(ValueError,"Unaware screen"):
            g2.bow_sequence("archer","target",(ShotChoice(
                primary_face=8,exposures=(("screen",4),),
                collateral=(("screen","guard"),),secondary_face=1),))
        self.assertEqual((r.ap_remaining,r.ammunition,
                          screen.guard_remaining,len(e.ledger)),before)

    def test_23_unaware_intended_defender_cannot_choose_dodge(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,target)
        e.start_turn("archer")
        with self.assertRaisesRegex(ValueError,"Unaware target"):
            g2.bow_sequence("archer","target",(
                ShotChoice(primary_face=12,defense="dodge"),))
        self.assertEqual(r.ammunition,20)
        self.assertEqual(r.ap_remaining,42)

    def test_24_secondary_natural_one_still_impacts_legal_shield(self):
        r=hero("R","archer",(1,2))
        screen=soldier("screen",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,screen,target)
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=8,exposures=(("screen",4),),
            collateral=(("screen","guard"),),
            aware_collateral=("screen",),secondary_face=1),))[0]
        self.assertEqual(out["outcome"],"collateral_guard_impact")
        self.assertEqual(screen.guard_remaining,1)
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_25_interception_moving_aimed_archer_no_stale_bonus(self):
        # Movement Interception after Aim already starts shot: its aimed
        # source is gone, but the underlying AP-paid Bow shot still flies.
        r=hero("R","archer",(1,2))
        target=hero("B","target",(16,2),"enemy")
        e,g1,g2=fixture(r,target)
        e.start_turn("archer")
        g2.aim("archer","target","range")
        # Shooter is never permitted to self-trigger a Movement Interception;
        # instead simulate an independently authored displacement response
        # through G1's on_position_change hook immediately after the Aim
        # is consumed, before firing (no phantom MP spend).
        r.occupied=((2,2),)
        out=g2.bow_sequence("archer","target",(
            ShotChoice(primary_face=7,aim_source="range"),))[0]
        self.assertEqual(out["base_defense"],12)  # Medium +2 remains
        self.assertEqual(out["outcome"],"ordinary_miss")
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_26_intended_guard_resources_preassigned_before_first_roll(self):
        threat=soldier("threat",(2,3))
        r=hero("R","archer",(1,2))
        target=soldier("target",(9,2))
        e,g1,g2=fixture(threat,r,target,
                         score={"threat":30,"archer":20,"target":10})
        e.start_turn("threat");e.end_turn();e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(
            ShotChoice(primary_face=10,defense="guard",aware_target=True),
            ShotChoice(primary_face=20,defense="guard",aware_target=True,
                       opportunities=(Response("threat","opportunity","hit"),),
                       on_opportunity=lambda c:True)))
        self.assertEqual(tuple(x["outcome"] for x in out),
                         ("intended_guard_impact","interrupted_before_launch"))
        self.assertEqual(target.guard_remaining,0)
        self.assertEqual(r.ammunition,19)
        self.assertEqual(r.ap_remaining,2)
        pre=[x["index"] for x in e.ledger
             if x["kind"]=="g2_projectile_defense_preassigned"]
        launch=[x["index"] for x in e.ledger if x["kind"]=="g2_bow_launched"]
        self.assertEqual(len(pre),2)
        self.assertTrue(max(pre)<min(launch))
        e.check()

    def test_27_multiple_preassigned_dodges_use_respective_pressure(self):
        r=hero("R","archer",(1,2))
        t=soldier("target",(9,2))
        e,g1,g2=fixture(r,t)
        e.start_turn("archer")
        shots=(ShotChoice(defense="dodge",aware_target=True,primary_face=9),
               ShotChoice(defense="dodge",aware_target=True,primary_face=9))
        out=g2.bow_sequence("archer","target",shots)
        self.assertEqual([x["base_defense"] for x in out],[13,11])
        self.assertEqual([x["outcome"] for x in out],
                         ["ordinary_miss","intended_hit_pending_G5"])
        self.assertEqual(t.dodge_pressure,4)
        self.assertEqual(r.ammunition,18)
        e.check()

    def test_28_neutral_screen_requires_declared_collateral_side(self):
        r=hero("R","archer",(1,2))
        third=hero("A","third",(3,2),team="neutral")
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,third,target)
        e.start_turn("archer")
        initial=(r.ammunition,r.ap_remaining,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"risk side"):
            g2.bow_sequence("archer","target",(
                ShotChoice(primary_face=2,exposures=(("third",2),),
                           collateral=(("third","take_hit"),),
                           secondary_face=19),))
        self.assertEqual((r.ammunition,r.ap_remaining,len(e.ledger)),initial)
        out=g2.bow_sequence("archer","target",(
            ShotChoice(primary_face=2,exposures=(("third",2),),
                       neutral_sides=(("third","ally"),),
                       collateral=(("third","take_hit"),),
                       secondary_face=19),))[0]
        self.assertEqual((out["outcome"],out["target"]),
                         ("collateral_hit_pending_G5","third"))
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_29_guard_instrument_lost_after_assignment_falls_back_to_dodge(self):
        threat=soldier("threat",(2,3))
        r=hero("R","archer",(1,2))
        target=soldier("target",(9,2))
        e,g1,g2=fixture(threat,r,target,
                         score={"threat":30,"archer":20,"target":10})
        e.start_turn("threat");e.end_turn();e.start_turn("archer")
        def disarm_guard(response):
            target.ready_guard=False
            return False  # independently resolved threat attack did not hit
        out=g2.bow_sequence("archer","target",(ShotChoice(
            defense="guard",aware_target=True,primary_face=12,
            opportunities=(Response("threat","opportunity","disarm-guard"),),
            on_opportunity=disarm_guard),))[0]
        self.assertEqual(out["outcome"],"intended_hit_pending_G5")
        self.assertEqual(target.guard_remaining,1)  # spent despite fallback
        self.assertEqual(target.dodge_pressure,2)
        fallbacks=[v for v in e.ledger
                   if v["kind"]=="g2_projectile_defense_fallback"]
        self.assertEqual(fallbacks[0]["detail"]["actual"],"dodge")
        e.check()

    def test_30_loss_of_wielded_bow_prelaunch_no_arrow_or_ap_refund(self):
        threat=soldier("threat",(2,3))
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(threat,r,target,
                         score={"threat":30,"archer":20,"target":10})
        e.start_turn("threat");e.end_turn();e.start_turn("archer")
        def disarm_bow(response):
            g2.wielded["archer"].discard("Bow")
            return False
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=16,
            opportunities=(Response("threat","opportunity","break-bow"),),
            on_opportunity=disarm_bow),))[0]
        self.assertEqual(out["outcome"],"illegal_after_commit")
        self.assertEqual(r.ap_remaining,22)
        self.assertEqual(r.ammunition,20)
        self.assertEqual(len(result(e)),0)
        e.check()

    def test_31_hunter_target_requires_explicit_stable_anatomical_cell(self):
        r=hero("R","archer",(1,2))
        h=hunter(at=((8,2),(7,2)))
        e,g1,g2=fixture(r,h)
        e.start_turn("archer")
        with self.assertRaisesRegex(UnresolvedDecision,"anatomy cell"):
            g2.bow_sequence("archer","hunter",(ShotChoice(primary_face=15),))
        self.assertEqual((r.ap_remaining,r.ammunition),(42,20))
        self.assertNotIn(("archer","hunter"),e.seen_sequences)
        out=g2.bow_sequence("archer","hunter",(ShotChoice(
            primary_face=15,target_cell=g1.body_cell("hunter","head")),))[0]
        self.assertEqual(out["outcome"],"intended_hit_pending_G5")
        self.assertEqual(r.ammunition,19)
        self.assertEqual(h.hp,h.hp_max) # injury is G4/G5; G2 logs delivery only
        e.check()

    def test_32_hunter_one_silhouette_and_nearest_cell_secondary_range(self):
        r=hero("R","archer",(1,2))
        h=hunter(at=((8,2),(7,2)))
        t=hero("B","target",(11,2),"enemy")
        e,g1,g2=fixture(r,h,t)
        e.start_turn("archer")
        lane=g2.lane("archer","target",exposures=(("hunter",6),))
        self.assertEqual(len(lane.screens),1)
        self.assertEqual(lane.screens[0],("hunter",6,6))
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=8,exposures=(("hunter",6),),
            collateral=(("hunter","take_hit"),),secondary_face=5),))[0]
        self.assertEqual((out["outcome"],out["target"]),
                         ("collateral_hit_pending_G5","hunter"))
        secondary=[v for v in e.ledger
                   if v["kind"]=="g2_conditional_secondary"]
        self.assertEqual(secondary[0]["detail"]["defense_value"],8)
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_33_paid_dagger_ready_updates_true_g1_melee_threat(self):
        r=hero("R","archer",(1,2))
        t=hero("B","target",(2,2),"enemy")
        e,g1,g2=fixture(r,t)
        e.start_turn("archer")
        self.assertFalse(g1.threatens("archer",(2,2)))
        self.assertFalse(g1.melee_contact("archer","target"))
        g2.ready_weapon("archer","Dagger")
        self.assertTrue(g1.threatens("archer",(2,2)))
        self.assertTrue(g1.melee_contact("archer","target"))
        self.assertEqual(r.ap_remaining,18)
        e.check()

    def test_34_aim_cannot_swap_hunter_anatomical_point_for_free(self):
        r=hero("R","archer",(1,2))
        h=hunter(at=((16,2),(15,2)))
        e,g1,g2=fixture(r,h)
        e.start_turn("archer")
        g2.aim("archer","hunter","range",target_cell=(16,2))
        self.assertEqual(r.ap_remaining,22)
        with self.assertRaisesRegex(ValueError,"exact point"):
            g2.bow_sequence("archer","hunter",(ShotChoice(
                primary_face=20,aim_source="range",target_cell=(15,2)),))
        self.assertEqual(r.ammunition,20)
        self.assertEqual(r.ap_remaining,22)
        self.assertIn("archer",g2.aims)
        e.check()

    def test_35_reject_nonpositive_aim_sources_before_spending_ap(self):
        r=hero("R","archer",(1,2))
        t=hero("B","target",(9,2),"enemy") # Short range +0
        e,g1,g2=fixture(r,t)
        e.start_turn("archer")
        initial=(r.ap_remaining,len(e.ledger))
        for objective in ("range","cover"):
            with self.subTest(objective=objective):
                with self.assertRaisesRegex(ValueError,"positive applicable"):
                    g2.aim("archer","target",objective)
                self.assertEqual((r.ap_remaining,len(e.ledger)),initial)
                self.assertNotIn("archer",g2.aims)
        e.check()

    def test_36_no_conditional_shield_overcommit_across_sequence(self):
        r=hero("R","archer",(1,2))
        screen=soldier("screen",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,screen,target)
        e.start_turn("archer")
        screen.guard_remaining=1 # prior legal Guard in this round
        spec=ShotChoice(primary_face=8,exposures=(("screen",4),),
                        collateral=(("screen","guard"),),
                        aware_collateral=("screen",),secondary_face=2)
        before=(r.ap_remaining,r.ammunition,screen.guard_remaining,len(e.ledger))
        with self.assertRaisesRegex(ValueError,"collateral Guard sequence"):
            g2.bow_sequence("archer","target",(spec,spec))
        self.assertEqual((r.ap_remaining,r.ammunition,
                          screen.guard_remaining,len(e.ledger)),before)
        self.assertNotIn(("archer","target"),e.seen_sequences)

    def test_37_two_selected_conditional_guards_legal_if_capacity_two(self):
        r=hero("R","archer",(1,2))
        screen=soldier("screen",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,screen,target)
        e.start_turn("archer")
        spec=ShotChoice(primary_face=8,exposures=(("screen",4),),
                        collateral=(("screen","guard"),),
                        aware_collateral=("screen",),secondary_face=2)
        out=g2.bow_sequence("archer","target",(spec,spec))
        self.assertEqual([x["outcome"] for x in out],
                         ["collateral_guard_impact","collateral_guard_impact"])
        self.assertEqual(screen.guard_remaining,0)
        self.assertEqual(r.ammunition,18)
        self.assertEqual(r.ap_remaining,2)
        self.assertEqual(len([x for x in e.ledger
                              if x["kind"]=="g2_conditional_secondary"]),2)
        e.check()

    def test_38_conditional_guard_lost_preimpact_falls_back_no_fake_guard_charge(self):
        threat=soldier("threat",(2,3))
        r=hero("R","archer",(1,2))
        screen=soldier("screen",(5,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(threat,r,screen,target,score={
            "threat":40,"archer":30,"screen":20,"target":10})
        e.start_turn("threat");e.end_turn();e.start_turn("archer")
        def change_shield(response):
            screen.ready_guard=False
            return False
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=8,exposures=(("screen",4),),
            collateral=(("screen","guard"),),aware_collateral=("screen",),
            secondary_face=2,
            opportunities=(Response("threat","opportunity","disarm-screen"),),
            on_opportunity=change_shield),))[0]
        self.assertEqual(out["outcome"],"collateral_miss")
        self.assertEqual(screen.guard_remaining,2) # not physically committed
        self.assertEqual(screen.dodge_pressure,2) # actual fallback
        self.assertEqual(len([x for x in e.ledger
                              if x["kind"]=="g2_collateral_defense_fallback"]),1)
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_39_screen_departing_lane_no_longer_blocks_valid_shot(self):
        screen=soldier("screen",(5,2))
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(screen,r,target,score={
            "screen":30,"archer":20,"target":10})
        e.start_turn("screen")
        key=g1.reserve_movement("screen","screen-steps-aside",2,label="step-aside")
        e.end_turn()
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=15,exposures=(("screen",4),),
            collateral=(("screen","take_hit"),),
            trigger_key="screen-steps-aside",
            interceptor_routes={key:((0,1),)}),))[0]
        self.assertEqual(screen.occupied,((5,3),))
        self.assertEqual(out["outcome"],"intended_hit_pending_G5")
        self.assertEqual(r.ammunition,19)
        self.assertEqual(r.ap_remaining,22)
        self.assertEqual(out["final_defense"],10)
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="g2_conditional_secondary"]),0)
        e.check()

    def test_40_hunter_head_moves_during_interception_stable_target_identity(self):
        h=hunter(at=((7,2),(6,2)))
        r=hero("R","archer",(1,2))
        e,g1,g2=fixture(h,r,score={"hunter":20,"archer":10})
        e.start_turn("hunter")
        key=g1.reserve_movement("hunter","hunter-moves",2,label="head-forward")
        e.end_turn()
        e.start_turn("archer")
        out=g2.bow_sequence("archer","hunter",(ShotChoice(
            primary_face=6,target_cell=(7,2),
            trigger_key="hunter-moves",
            interceptor_routes={key:((1,0),)}),))[0]
        self.assertEqual(h.occupied,((8,2),(7,2)))
        self.assertEqual(g1.body_cell("hunter","head"),(8,2))
        self.assertEqual(out["outcome"],"ordinary_miss")
        self.assertEqual(out["base_defense"],10) # head now Short, not Close
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_41_prone_static_ranged_position_plus_two_at_three_squares(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        target.conditions.append("Prone")
        e,g1,g2=fixture(r,target)
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            defense="take_hit",primary_face=8),))[0]
        self.assertEqual(out["outcome"],"ordinary_miss")
        self.assertEqual((out["base_defense"],out["final_defense"]),(12,12))
        self.assertEqual(out["scatter_margin"],0)
        e.check()

    def test_42_prone_incidental_defense_changes_same_arrow_accuracy(self):
        r=hero("R","archer",(1,2))
        screen=soldier("screen",(4,2))
        screen.conditions.append("Prone")
        target=hero("B","target",(9,2),"enemy")
        e,g1,g2=fixture(r,screen,target)
        e.start_turn("archer")
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=8,exposures=(("screen",4),),
            collateral=(("screen","take_hit"),),secondary_face=6),))[0]
        self.assertEqual(out["outcome"],"collateral_miss")
        incidental=[x for x in e.ledger
                    if x["kind"]=="g2_conditional_secondary"][0]["detail"]
        self.assertEqual(incidental["defense_value"],10) # 10-2 Close+2 Prone
        self.assertEqual(r.ammunition,19)
        e.check()

    def test_43_prone_with_cover_requires_explicit_nonduplicate_policy(self):
        r=hero("R","archer",(1,2))
        target=hero("B","target",(9,2),"enemy")
        target.conditions.append("Prone")
        e,g1,g2=fixture(r,target,cover=(CoverSurface((5,2),4,(1,0)),))
        e.start_turn("archer")
        before=(r.ap_remaining,r.ammunition,len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"Prone plus Cover"):
            g2.bow_sequence("archer","target",(ShotChoice(primary_face=8),))
        self.assertEqual((r.ap_remaining,r.ammunition,len(e.ledger)),before)
        self.assertNotIn(("archer","target"),e.seen_sequences)
        out=g2.bow_sequence("archer","target",(ShotChoice(
            primary_face=8,
            prone_cover_policy=(("target","absorbed"),)),))[0]
        self.assertEqual((out["base_defense"],out["final_defense"]),(10,14))
        self.assertEqual(out["outcome"],"cover_impact")
        e.check()

    def test_44_retained_aim_follows_same_hunter_head_across_own_turns(self):
        r=hero("R","archer",(1,2))
        h=hunter(at=((16,2),(15,2)))
        e,g1,g2=fixture(r,h,score={"archer":20,"hunter":10})
        e.start_turn("archer")
        g2.aim("archer","hunter","range",target_cell=(16,2))
        e.end_turn()
        e.start_turn("hunter")
        self.assertTrue(g1.step("hunter",(1,0)))
        self.assertEqual(g1.body_cell("hunter","head"),(17,2))
        e.end_turn()
        e.begin_round()
        e.start_turn("archer")
        self.assertIn("archer",g2.aims)
        out=g2.bow_sequence("archer","hunter",(ShotChoice(
            primary_face=7,aim_source="range",target_cell=(17,2)),))[0]
        self.assertEqual(out["outcome"],"intended_hit_pending_G5")
        self.assertEqual(out["base_defense"],10)
        self.assertEqual(r.ammunition,19)
        self.assertNotIn("archer",g2.aims)
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
