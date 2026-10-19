"""B06 G1: seven deterministic physical/contact/response acceptance traces."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, Response, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement


def soldier(actor_id, team="enemy", at=((4, 4),)):
    return enemy_actor("B06-EN-02", actor_id, team, occupied=at)


def sentry(actor_id, team="enemy", at=((4, 4),)):
    return enemy_actor("B06-EN-01", actor_id, team,
                       start_state="cold_start", occupied=at)


def hunter(actor_id="hunter", team="enemy", at=((2, 2), (1, 2))):
    return enemy_actor("B06-EN-03", actor_id, team, occupied=at)


def hero(actor_id, at, role="A", level=3, team="party"):
    return party_actor(role, level, actor_id, team, occupied=(at,))


def scenario(*actors, walls=(), terrain=None, scores=None, w=12, h=9):
    totals = scores or {a.id: 20-i for i, a in enumerate(actors)}
    e = Encounter(list(actors), totals, seed=1919, tie_order=tuple(a.id for a in actors),
                  scenario="G1-deterministic-fixture", policy="declared-route")
    m = GridMovement(e, width=w, height=h, walls=walls, terrain=terrain)
    return e, m


class G1PhysicalAcceptance(unittest.TestCase):
    def test_trace_01_hunter_three_head_forward_steps_one_bite_conditional_balance(self):
        h = hunter()
        prey = hero("prey", (6, 2))
        e, g = scenario(h, prey)
        e.begin_round()
        e.start_turn("hunter")
        self.assertEqual(g.start_pounce("hunter", "prey"), (1, 0))
        for _ in range(3):
            self.assertTrue(g.step("hunter", (1, 0)))
        self.assertEqual(h.occupied, ((5, 2), (4, 2)))
        self.assertEqual(g.front("hunter"), (6, 2))
        self.assertEqual((h.mp_remaining, h.ap_remaining), (18, 42))
        self.assertTrue(g.pounce_contact(defense="take_hit"))
        self.assertEqual((h.ap_remaining, h.mp_remaining), (18, 0))
        self.assertEqual((prey.hp, prey.vigor), (prey.hp_max, prey.vigor_max))
        self.assertIn(("hunter", "prey"), e.seen_sequences)
        actions = [ev for ev in e.ledger if ev["kind"] == "g1_pounce_bite_committed"]
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["detail"]["profile"], "B06-AT-06")
        self.assertEqual(actions[0]["detail"]["translated_steps"], 3)
        last = [ev for ev in e.ledger if ev["kind"] == "g1_pounce_contact_result"]
        self.assertEqual(len(last), 1)
        self.assertEqual(last[0]["detail"]["balance"],
                         "conditional_after_Bite_resolution_G5")
        self.assertFalse(any(ev["kind"] == "damage_applied" for ev in e.ledger))
        e.check()

    def test_trace_02_scholar_pays_precontact_movement_not_unearned_flame(self):
        f = hero("F", (0, 2), role="F")
        h = hunter(at=((4, 2), (5, 2)))
        e, g = scenario(f, h)
        e.begin_round()
        e.start_turn("F")
        prior_vp = (f.vp_available, f.vp_committed, f.vp_spent)
        self.assertTrue(g.step("F", (1, 0)))
        self.assertEqual(f.occupied, ((1, 2),))
        self.assertEqual(f.mp_remaining, 10)
        self.assertFalse(g.melee_contact("F", "hunter"))
        # Direct head is 3 squares away: potential T1/2/3 thrown Flame
        # geometry only. No G2 lane and no G3 spell or VP spent.
        self.assertEqual(abs(f.occupied[0][0]-h.occupied[0][0]), 3)
        self.assertEqual((f.vp_available, f.vp_committed, f.vp_spent), prior_vp)
        self.assertEqual(f.ap_remaining, 42)
        self.assertNotIn("spell_committed", [ev["kind"] for ev in e.ledger])
        e.check()

    def test_trace_03_nonfront_melee_blocker_forces_explicit_alt_route(self):
        a = hero("A", (0, 2))
        block = soldier("block", at=((2, 2),))
        h = hunter(at=((5, 2), (6, 2)))
        e, g = scenario(a, block, h)
        e.begin_round()
        e.start_turn("A")
        self.assertTrue(g.step("A", (1, 0)))
        before = (a.occupied, a.mp_remaining)
        with self.assertRaisesRegex(ValueError, "blocked|occupied"):
            g.step("A", (1, 0))  # Direct line's soldier cannot be passed.
        self.assertEqual((a.occupied, a.mp_remaining), before)
        # Alternate normal approach explicitly chosen: one diagonal,
        # then one east, all cells legal. Not an AI shortest-path guess.
        self.assertTrue(g.step("A", (1, -1)))
        self.assertTrue(g.step("A", (1, 0)))
        self.assertEqual(a.occupied, ((3, 1),))
        self.assertEqual(a.mp_remaining, 5)  # 2+3+2 MP
        self.assertNotEqual(a.occupied[0], block.occupied[0])
        e.check()

    def test_trace_04_allies_require_continuous_paid_transit_no_overlap(self):
        a = hero("A", (0, 1))
        b = hero("B", (1, 1), role="B")
        e, g = scenario(a, b)
        e.begin_round()
        e.start_turn("A")
        with self.assertRaisesRegex(ValueError, "occupied|blocked"):
            # Plain entry requires a full transit route, not a free merge.
            g.step("A", (1, 0))
        self.assertEqual((a.occupied, a.mp_remaining), (((0, 1),), 12))
        with self.assertRaisesRegex(ValueError, "Cannot end movement on ally"):
            g.move_route("A", ((1, 0),))
        self.assertTrue(g.move_route("A", ((1, 0), (1, 0))))
        self.assertEqual(a.occupied, ((2, 1),))
        self.assertEqual(a.mp_remaining, 6)  # 4 transit +2 exit
        self.assertEqual(b.occupied, ((1, 1),))
        self.assertEqual(len(set(a.occupied+b.occupied)), 2)
        e.check()

    def test_trace_05_hunter_pivot_cost_sweep_identity_and_charge_ban(self):
        h = hunter()
        e, g = scenario(h)
        e.begin_round()
        e.start_turn("hunter")
        self.assertTrue(g.pivot("hunter", "rear", clockwise=True))
        self.assertEqual(g.body_cell("hunter", "rear"), (1, 2))
        self.assertEqual(g.body_cell("hunter", "head"), (1, 1))
        self.assertEqual(h.mp_remaining, 9)  # 3 MP clockwise pivot
        self.assertTrue(g.pivot("hunter", "rear", clockwise=False, cautious=True))
        self.assertEqual(h.occupied, ((2, 2), (1, 2)))
        self.assertEqual(h.mp_remaining, 3)  # Cautious pivot 6 MP
        e.check()
        x = hunter()
        ex, gx = scenario(x, walls=((2, 1),))
        ex.begin_round()
        ex.start_turn("hunter")
        with self.assertRaisesRegex(ValueError, "swept corner"):
            gx.pivot("hunter", "rear", clockwise=True)
        self.assertEqual(x.occupied, ((2, 2), (1, 2)))
        self.assertEqual(x.mp_remaining, 12)
        hx = hunter()
        target = hero("prey", (6, 2))
        ey, gy = scenario(hx, target)
        ey.begin_round()
        ey.start_turn("hunter")
        gy.start_pounce("hunter", "prey")
        with self.assertRaisesRegex(ValueError, "fixed-head-forward"):
            gy.pivot("hunter", "rear", clockwise=True)
        with self.assertRaisesRegex(ValueError, "fixed-head-forward"):
            gy.step("hunter", (0, -1))
        self.assertEqual(hx.mp_remaining, 24)
        self.assertEqual(hx.ap_remaining, 42)
        gy.pounce_abort()

    def test_trace_06_threatened_departure_one_reaction_not_auto_interrupt(self):
        mover = hero("mover", (2, 2))
        threat = sentry("threat", at=((3, 2),))
        e, g = scenario(mover, threat)
        e.begin_round()
        e.start_turn("mover")
        self.assertTrue(g.step("mover", (0, -1),
                      responses=(Response("threat", "opportunity", "ordinary pre-step attack"),)))
        self.assertEqual(mover.occupied, ((2, 1),))
        self.assertEqual(mover.mp_remaining, 10)
        self.assertEqual(threat.opportunity_used, 1)
        self.assertTrue(threat.opportunity_active)
        self.assertFalse(threat.reaction_available)
        self.assertEqual(len([ev for ev in e.ledger
                              if ev["kind"] == "g1_movement_opportunity_pending"]), 1)
        # Step 2 in same movement segment may not take a second general
        # Opportunity from the same sentry even while it has Tempo capacity.
        self.assertTrue(g.step("mover", (0, 1)))
        self.assertEqual(len([ev for ev in e.ledger
                              if ev["kind"] == "g1_movement_opportunity_pending"]), 1)
        with self.assertRaisesRegex(ValueError, "not eligible"):
            g.step("mover", (0, -1),
                   responses=(Response("threat", "opportunity", "duplicate segment"),))
        # A real own action ends segment; opportunity timing resets, but the
        # already-active Opportunity still consumes capacity normally.
        e.spend_ap("mover", "physical", label="new own action")
        self.assertTrue(g.step("mover", (0, -1),
                      responses=(Response("threat", "opportunity", "after own action"),)))
        self.assertEqual(threat.opportunity_used, 2)
        self.assertFalse(threat.reaction_available)
        e.check()
        # Contrast Cautious departure: cost doubled, no general opportunity.
        m = hero("cautious", (2, 2))
        t = sentry("sentry", at=((3, 2),))
        ec, gc = scenario(m, t)
        ec.begin_round()
        ec.start_turn("cautious")
        self.assertTrue(gc.step("cautious", (0, -1), cautious=True))
        self.assertEqual(m.mp_remaining, 8)
        self.assertTrue(t.reaction_available)

    def test_trace_07_mp_interception_blocks_destination_without_leaking_resources(self):
        sentinel = soldier("sentinel", at=((2, 1),))
        mover = hero("mover", (0, 1))
        e, g = scenario(sentinel, mover)
        e.begin_round()
        e.start_turn("sentinel")
        label = g.reserve_movement("sentinel", "mover-step", 2,
                                   label="step-into-lane")
        self.assertEqual(sentinel.mp_remaining, 10)
        e.end_turn()
        e.start_turn("mover")
        original = (mover.mp_remaining, mover.ap_remaining,
                    mover.vp_available, mover.vigor, mover.hp,
                    sentinel.vigor, sentinel.hp, sentinel.reaction_available)
        self.assertFalse(g.step(
            "mover", (1, 0), trigger_key="mover-step",
            interceptor_routes={label: ((-1, 0),)}))
        self.assertEqual(sentinel.occupied, ((1, 1),))
        self.assertEqual(mover.occupied, ((0, 1),))
        self.assertEqual(original, (mover.mp_remaining, mover.ap_remaining,
                                   mover.vp_available, mover.vigor, mover.hp,
                                   sentinel.vigor, sentinel.hp, sentinel.reaction_available))
        self.assertNotIn(label, g.motion)
        released = [ev for ev in e.ledger
                    if ev["kind"] == "g1_movement_interception_resolved"]
        self.assertEqual(len(released), 1)
        self.assertEqual(released[0]["detail"]["consumed_mp"], 2)
        self.assertEqual(released[0]["detail"]["completed_steps"], 1)
        self.assertIn("trigger_cancelled_before_spontaneous",
                      [ev["kind"] for ev in e.ledger])
        self.assertTrue(g.step("mover", (0, 1), trigger_key="alternate-route"))
        self.assertEqual(mover.mp_remaining, 10)
        e.check()

    def test_profiled_terrain_and_cautious_footprint_average(self):
        h = hunter()
        e, g = scenario(h, terrain={(3, 2): "difficult"})
        e.begin_round()
        e.start_turn("hunter")
        self.assertTrue(g.step("hunter", (1, 0)))
        self.assertEqual(h.mp_remaining, 9)  # avg(4 front,2 rear) =3
        self.assertEqual(h.occupied, ((3, 2), (2, 2)))
        self.assertTrue(g.step("hunter", (1, 0), cautious=True))
        # cautious base4+ destination head normal4/rear difficult6 ->5
        self.assertEqual(h.mp_remaining, 4)
        e.check()

    def test_pounce_cutoff_commits_ap_on_first_step_past_eighteen_mp(self):
        h = hunter(at=((2, 2), (1, 2)))
        prey = hero("prey", (7, 2))
        # Four severe 6-MP steps reach frontal contact within the actual
        # 24-MP Charge allowance; the fourth crosses the 18-MP cutoff.
        ground = {(x, 2): "severe" for x in range(1, 9)}
        e, g = scenario(h, prey, terrain=ground)
        e.begin_round()
        e.start_turn("hunter")
        g.start_pounce("hunter", "prey")
        for _ in range(3):
            self.assertTrue(g.step("hunter", (1, 0)))
        self.assertEqual((g.pounce.spent_mp, h.ap_remaining), (18, 42))
        self.assertTrue(g.step("hunter", (1, 0)))
        self.assertEqual((g.pounce.spent_mp, h.ap_remaining), (24, 18))
        self.assertTrue(g.pounce.committed)
        self.assertEqual(sum(ev["kind"] == "action_committed" for ev in e.ledger), 1)
        g.pounce_abort()
        self.assertEqual(h.mp_remaining, 0)

    def test_g1_validates_rigid_body_and_unwielded_melee_capability(self):
        h = hunter(at=((2, 2), (1, 1)))
        e = Encounter([h], {"hunter": 20}, seed=919)
        with self.assertRaisesRegex(ValueError, "cardinally adjacent"):
            GridMovement(e, width=9, height=9)
        f = hero("F", (1, 1), role="F")
        e2, g2 = scenario(f)
        self.assertFalse(g2.threatens("F", (2, 1)))
        r = hero("R", (3, 1), role="R")
        e3, g3 = scenario(f, r)
        self.assertFalse(g3.threatens("R", (4, 1)))
        self.assertFalse(g3.threatens("F", (2, 1)))

    def test_mp_interception_cannot_self_trigger_or_be_reserved_while_dying(self):
        a = sentry("a", at=((1, 1),))
        e, g = scenario(a)
        e.begin_round()
        e.start_turn("a")
        key = g.reserve_movement("a", "self-attack-response", 2,
                                 label="cannot-react-to-my-step")
        baseline = (a.occupied, a.mp_remaining, len(e.reservations),
                    len(g.motion), len(e.ledger))
        with self.assertRaisesRegex(ValueError, "self-trigger"):
            g.step("a", (1, 0), trigger_key="self-attack-response")
        self.assertEqual((a.occupied, a.mp_remaining, len(e.reservations),
                          len(g.motion), len(e.ledger)), baseline)
        self.assertIn(key, g.motion)
        a.hp = 0
        with self.assertRaisesRegex(ValueError, "Dying/dead"):
            g.reserve_movement("a", "future", 2, label="unable")
        self.assertEqual(a.mp_remaining, 10)

    def test_illegal_released_interception_path_spends_no_extra_mp(self):
        a = soldier("a", at=((2, 1),))
        b = hero("b", (0, 1))
        e, g = scenario(a, b, walls=((1, 1),))
        e.begin_round()
        e.start_turn("a")
        key = g.reserve_movement("a", "b-movement", 3, label="blocked-route")
        e.end_turn()
        e.start_turn("b")
        self.assertTrue(g.step("b", (0, 1), trigger_key="b-movement",
                       interceptor_routes={key: ((-1, 0),)}))
        self.assertEqual(a.occupied, ((2, 1),))
        rejected = [v for v in e.ledger if v["kind"] == "g1_interception_route_rejected"]
        self.assertEqual(len(rejected), 1)
        self.assertEqual(rejected[0]["detail"]["spent_mp"], 0)
        self.assertFalse(any(v["kind"] == "g1_movement_step"
                             and v["detail"]["actor"] == "a" for v in e.ledger))
        self.assertNotIn(key, g.motion)
        e.check()

    def test_aborted_tentative_pounce_keeps_rapid_heading_and_action_budget(self):
        h = hunter(at=((2, 2), (1, 2)))
        prey = hero("prey", (8, 2))
        e, g = scenario(h, prey)
        e.begin_round()
        e.start_turn("hunter")
        g.start_pounce("hunter", "prey")
        self.assertTrue(g.step("hunter", (1, 0)))
        self.assertEqual((h.mp_remaining, h.ap_remaining), (22, 42))
        with self.assertRaisesRegex(ValueError, "Complete or abort active Pounce"):
            e.spend_ap("hunter", "physical", label="unrelated attack mid-run")
        self.assertEqual(h.ap_remaining, 42)
        g.pounce_abort()
        self.assertEqual(h.mp_remaining, 16)  # Remaining 18-MP Rapid allowance.
        self.assertEqual(g.rapid_heading["hunter"], (1, 0))
        with self.assertRaisesRegex(ValueError, "fixed Rapid Advance heading"):
            g.step("hunter", (0, 1))
        with self.assertRaisesRegex(ValueError, "fixed Rapid Advance heading"):
            g.pivot("hunter", "rear", clockwise=True)
        with self.assertRaisesRegex(ValueError, "prohibits new MP reservations"):
            g.reserve_movement("hunter", "future", 2, label="invalid")
        with self.assertRaisesRegex(ValueError, "already active or this turn"):
            g.start_pounce("hunter", "prey")
        self.assertTrue(g.step("hunter", (1, 0)))
        self.assertEqual(h.mp_remaining, 14)
        e.spend_ap("hunter", "physical", label="separate legal action")
        self.assertEqual(h.ap_remaining, 18)
        e.end_turn()
        e.start_turn("prey")
        e.end_turn()
        e.begin_round()
        e.start_turn("hunter")
        self.assertNotIn("hunter", g.rapid_heading)
        self.assertEqual(h.mp_remaining, 12)

    def test_allied_transit_cannot_bypass_earlier_threatened_step(self):
        mover = hero("mover", (0, 1))
        ally = hero("ally", (2, 1), role="B")
        hostile = sentry("hostile", at=((1, 2),))
        e, g = scenario(mover, ally, hostile)
        e.begin_round()
        e.start_turn("mover")
        baseline = (mover.occupied, mover.mp_remaining, len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision, "transit|responses"):
            g.move_route("mover", ((1, 0), (1, 0), (1, 0)))
        self.assertEqual((mover.occupied, mover.mp_remaining, len(e.ledger)), baseline)

    def test_review_p1_opportunity_source_moves_away_step_still_commits(self):
        # Threat is initially a legal responder, then its own saved MP
        # Interception escapes the mover's pre-step reach. That only drops
        # its spontaneous Opportunity; the mover's unblocked step proceeds.
        threat = sentry("threat", at=((3, 2),))
        mover = hero("mover", (2, 2))
        e, g = scenario(threat, mover, scores={"threat": 20, "mover": 10})
        e.begin_round()
        e.start_turn("threat")
        key = g.reserve_movement("threat", "mover-leaves", 4, label="withdraw")
        e.end_turn()
        e.start_turn("mover")
        assert g.threatens("threat", (2, 2))
        self.assertTrue(g.step(
            "mover", (0, -1), trigger_key="mover-leaves",
            responses=(Response("threat", "opportunity", "preplanned-offer"),),
            interceptor_routes={key: ((1, 0), (1, 0))}))
        self.assertEqual(threat.occupied, ((5, 2),))
        self.assertEqual(mover.occupied, ((2, 1),))
        self.assertEqual(mover.mp_remaining, 10)
        self.assertTrue(threat.reaction_available)
        self.assertEqual(threat.opportunity_used, 0)
        kinds = [item["kind"] for item in e.ledger]
        self.assertIn("g1_opportunity_no_longer_eligible", kinds)
        self.assertNotIn("g1_movement_opportunity_pending", kinds)
        self.assertEqual(kinds.count("g1_step_cancelled"), 0)
        e.check()

    def test_review_p1_post_interception_dynamic_opportunity_selection(self):
        # A second enemy moves INTO threat position while the original
        # triggering step remains clear. Post-Interception policy chooses it.
        scout = hero("scout", (2, 2))
        approach = sentry("approach", at=((4, 2),))
        e, g = scenario(approach, scout, scores={"approach": 20, "scout": 10})
        e.begin_round()
        e.start_turn("approach")
        key = g.reserve_movement("approach", "scout-goes", 2,
                                 label="close-gap")
        e.end_turn()
        e.start_turn("scout")
        # Initial source is 2 squares away and cannot declare an Opportunity.
        self.assertFalse(g.threatens("approach", (2, 2)))
        selected_from = []
        def choose(eligible):
            selected_from.append(tuple(eligible))
            return (Response("approach", "opportunity", "post-interception"),
                    ) if "approach" in eligible else ()
        self.assertTrue(g.step(
            "scout", (0, -1), trigger_key="scout-goes", responses=choose,
            interceptor_routes={key: ((-1, 0),)}))
        self.assertEqual(selected_from, [("approach",)])
        self.assertFalse(approach.reaction_available)
        self.assertEqual(approach.opportunity_used, 1)
        self.assertEqual(scout.occupied, ((2, 1),))
        self.assertEqual([x["kind"] for x in e.ledger].count(
            "g1_movement_opportunity_pending"), 1)
        e.check()

    def test_review_p1_rejected_bite_reservation_route_completes_paid_window(self):
        for route, expected, spent in (
                (((0, -1),), True, 0),
                (((1, 0), (0, -1)), False, 2)):
            with self.subTest(route=route):
                prey = hero("prey", (6, 2))
                h = hunter()
                # Illegal first step is the blocked north cell; illegal
                # second step follows one valid displacement east.
                walls = ((6, 1), (7, 1))
                e, g = scenario(prey, h, scores={"prey": 20, "hunter": 10},
                                walls=walls)
                e.begin_round()
                e.start_turn("prey")
                key = g.reserve_movement("prey", "bite-commit", 4,
                                         label="attempt-escape")
                e.end_turn()
                e.start_turn("hunter")
                g.start_pounce("hunter", "prey")
                for _ in range(3):
                    self.assertTrue(g.step("hunter", (1, 0)))
                self.assertEqual(h.ap_remaining, 42)
                self.assertEqual(g.pounce.steps, 3)
                self.assertEqual(g.pounce.committed, False)
                result = g.pounce_contact(
                    defense="take_hit", trigger_key="bite-commit",
                    interceptor_routes={key: route})
                self.assertIs(result, expected)
                self.assertEqual(h.ap_remaining, 18)
                self.assertIsNone(g.pounce)
                self.assertNotIn(key, g.motion)
                self.assertIn(("hunter", "prey"), e.seen_sequences)
                self.assertEqual(sum(ev["kind"] == "g1_pounce_bite_committed"
                                     for ev in e.ledger), 1)
                rejected = [ev for ev in e.ledger
                            if ev["kind"] == "g1_interception_route_rejected"]
                self.assertEqual(len(rejected), 1)
                self.assertEqual(rejected[0]["detail"]["spent_mp"], spent)
                self.assertEqual([ev["kind"] for ev in e.ledger].count(
                    "g1_pounce_contact_result"), 1)
                self.assertEqual(prey.vp_available, prey.vp_max)
                e.check()

    def test_review_p2_internal_pounce_ap_cannot_be_label_spoofed(self):
        h = hunter()
        prey = hero("prey", (6, 2))
        e, g = scenario(h, prey)
        e.begin_round()
        e.start_turn("hunter")
        g.start_pounce("hunter", "prey")
        before = (h.ap_remaining, len(e.ledger), g.segment["hunter"])
        for label in ("g1:pounce:anything", "g1:pounce:cutoff",
                      "g1:pounce:bite"):
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, "Complete or abort active Pounce"):
                    e.spend_ap("hunter", "physical", label=label)
                self.assertEqual((h.ap_remaining, len(e.ledger),
                                  g.segment["hunter"]), before)
        for _ in range(3):
            self.assertTrue(g.step("hunter", (1, 0)))
        self.assertTrue(g.pounce_contact())
        self.assertEqual(h.ap_remaining, 18)
        self.assertFalse(g._internal_pounce_spend)
        e.check()

    def test_review_p2_invalid_initial_pounce_approaches_atomic(self):
        layouts = (
            ((0, 2), ()),          # target behind body
            ((6, 3), ()),          # off fixed heading
            ((11, 2), ()),         # beyond map/24 MP? outside 24 normal not;
            ((6, 2), ((4, 2),)),   # solid wall in the body's exact lane
            ((6, 2), ((3, 1),)),   # harmless adjacent wall is not a blocker
        )
        for prey_at, walls in layouts:
            if prey_at == (6, 2) and walls == ((3, 1),):
                continue
            with self.subTest(prey=prey_at, walls=walls):
                h = hunter()
                prey = hero("prey", prey_at)
                e, g = scenario(h, prey, walls=walls, w=16)
                e.begin_round()
                e.start_turn("hunter")
                initial = (h.occupied, h.mp_remaining, h.ap_remaining,
                           len(e.ledger))
                with self.assertRaisesRegex(ValueError, "Pounce"):
                    g.start_pounce("hunter", "prey")
                self.assertEqual((h.occupied, h.mp_remaining, h.ap_remaining,
                                  len(e.ledger)), initial)
                self.assertIsNone(g.pounce)
        # Within width but >24 orthogonal MP, cannot borrow unlimited
        # Charge allowance or count inaccessible squares as a run-up.
        h = hunter()
        prey = hero("prey", (15, 2))
        e, g = scenario(h, prey, w=20)
        e.begin_round()
        e.start_turn("hunter")
        with self.assertRaisesRegex(ValueError, "24-MP"):
            g.start_pounce("hunter", "prey")
        self.assertEqual(h.mp_remaining, 12)
        self.assertIsNone(g.pounce)

    def test_review_p2_retarg_to_other_front_pc_before_defense(self):
        original = hero("original", (6, 2))
        replacement = hero("replacement", (6, 3), role="B")
        h = hunter()
        e, g = scenario(original, replacement, h,
                        scores={"original": 30, "replacement": 20, "hunter": 10})
        e.begin_round()
        e.start_turn("original")
        old_key = g.reserve_movement("original", "front-shift", 2,
                                     label="retreat-east")
        e.end_turn()
        e.start_turn("replacement")
        new_key = g.reserve_movement("replacement", "front-shift", 2,
                                     label="fill-front")
        e.end_turn()
        e.start_turn("hunter")
        self.assertEqual(g.start_pounce("hunter", "original"), (1, 0))
        self.assertTrue(g.step("hunter", (1, 0)))
        self.assertTrue(g.step("hunter", (1, 0)))
        self.assertTrue(g.step("hunter", (1, 0), trigger_key="front-shift",
                    interceptor_routes={
                        old_key: ((1, 0),),
                        new_key: ((0, -1),),
                    }))
        self.assertEqual(original.occupied, ((7, 2),))
        self.assertEqual(replacement.occupied, ((6, 2),))
        self.assertTrue(g.melee_contact("hunter", "replacement", hunter_front=True))
        self.assertFalse(g.melee_contact("hunter", "original", hunter_front=True))
        self.assertTrue(g.pounce_contact(
            final_target_id="replacement", defense="guard"))
        self.assertIn(("hunter", "replacement"), e.seen_sequences)
        self.assertNotIn(("hunter", "original"), e.seen_sequences)
        changed = [ev for ev in e.ledger if ev["kind"] == "g1_pounce_retargeted"]
        self.assertEqual(len(changed), 1)
        self.assertEqual(changed[0]["detail"]["final_target"], "replacement")
        self.assertEqual(h.ap_remaining, 18)
        e.check()

    def test_expired_mp_reservation_never_releases_next_turn(self):
        a = sentry("a", at=((1, 1),))
        b = hero("b", (6, 1))
        e, g = scenario(a, b)
        e.begin_round()
        e.start_turn("a")
        label = g.reserve_movement("a", "unlikely-trigger", 4, label="guard-approach")
        self.assertEqual(a.mp_remaining, 8)
        e.end_turn()
        e.start_turn("b")
        e.end_turn()
        e.begin_round()
        e.start_turn("a")
        self.assertNotIn(label, g.motion)
        self.assertFalse(any(r.label == label for r in e.reservations))
        self.assertEqual(a.mp_remaining, 12)
        self.assertTrue(any(ev["kind"] == "g1_reserved_mp_expired" for ev in e.ledger))
        e.check()


if __name__ == "__main__":
    unittest.main()
