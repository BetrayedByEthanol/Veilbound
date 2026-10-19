"""Source-backed G0 state, timing, defense, ledger and conservation tests."""
import json
import unittest

from scripts.b06_encounter_state_v0 import (
    ENEMIES, Encounter, RegenerationChoice, Response, Trigger, UnresolvedDecision,
    Wound, enemy_actor, party_actor,
)


def soldier(name="soldier", team="enemy", at=((1, 0),)):
    return enemy_actor("B06-EN-02", name, team, occupied=at)


def sentry(start, name="sentry", at=((2, 0),)):
    return enemy_actor("B06-EN-01", name, "enemy",
                       start_state=start, occupied=at)


def hunter(name="hunter", at=((4, 0), (3, 0))):
    return enemy_actor("B06-EN-03", name, "enemy", occupied=at)


def party(role="R", level=3, name="hero", at=((0, 0),)):
    return party_actor(role, level, name, "party", occupied=at)


def scene(*actors, score=None):
    return Encounter(list(actors), score or {a.id: 10 + i for i, a in enumerate(actors)},
                     seed=123, tie_order=tuple(a.id for a in actors))


class G0SourceTests(unittest.TestCase):
    def test_enemy_id_state_snapshot_and_local_nonfocus_assumptions(self):
        a = soldier()
        h = hunter()
        c = sentry("cold_start")
        p = sentry("prepared_start", name="prepared", at=((6, 0),))
        self.assertEqual(set(ENEMIES), {"B06-EN-01", "B06-EN-02", "B06-EN-03"})
        self.assertEqual((a.hp_max, a.vigor_max, a.vp_max, a.ap_total,
                          a.physical_ap, a.projection_ap), (12, 36, 0, 42, 24, None))
        self.assertEqual((a.guard_value, a.guard_capacity, a.regen), (18, 2, 2))
        self.assertEqual((h.hp_max, h.vigor_max, h.vp_max, h.regen), (14, 42, 0, 4))
        self.assertEqual(h.source.source_id, "B06-EN-03")
        self.assertEqual(h.footprint, ("head", "rear"))
        self.assertEqual(len(h.occupied), 2)
        self.assertIsNone(h.guard_instrument)
        self.assertEqual(h.guard_capacity, 1)  # latent, not a Guard entitlement.
        self.assertEqual((c.vp_available, c.vp_committed, c.vp_spent), (6, 0, 0))
        self.assertEqual((p.vp_available, p.vp_committed, p.vp_spent), (3, 3, 0))
        self.assertEqual(p.maintained, ["B06-FIRE-RESERVE-01"])
        for x in (a, h, c, p):
            self.assertEqual(len(x.source.digest), 64)
            x.validate()
        with self.assertRaises(UnresolvedDecision):
            enemy_actor("B06-EN-01", "x", "enemy", occupied=((10, 0),))
        with self.assertRaises(ValueError):
            enemy_actor("B06-EN-01", "x", "enemy",
                        start_state="imaginary", occupied=((10, 0),))

    def test_party_structural_roles_and_physical_proxy_boundary(self):
        for lvl in (1, 2, 3):
            for role in ("A", "B", "R", "F"):
                a = party(role, lvl)
                self.assertEqual(a.level, lvl)
                self.assertEqual(a.ap_total, 30 + 6 * (lvl - 1))
                a.validate()
                if role in ("A", "B"):
                    self.assertEqual(a.source.status, "B05_UNBUFFED_PHYSICAL_PROXY")
                    self.assertEqual(a.vp_max, 2 * lvl)
                else:
                    self.assertEqual(a.source.status, "STRUCTURAL_B05_ONLY")
                    self.assertEqual(a.vp_max, (2 if role == "R" else 6) * lvl)
                    self.assertEqual(a.guard_instrument, None)
        r = party("R", 3)
        f = party("F", 3, at=((8, 0),))
        self.assertEqual((r.ammunition, r.guard_capacity, r.regen,
                          r.physical_ap, r.projection_ap), (20, 3, 6, 20, 30))
        self.assertEqual((f.ammunition, f.guard_capacity, f.regen,
                          f.physical_ap, f.projection_ap), (0, 1, 3, 30, 20))
        self.assertNotEqual(r.source.digest, f.source.digest)
        self.assertIn(("Bow", "wielded"), r.source.equipment)
        self.assertIn(("Dagger", "carried"), f.source.equipment)
        self.assertNotIn(("Dagger", "wielded"), f.source.equipment)
        a1 = party("A", 1)
        a2 = party("A", 2)
        b1 = party("B", 1)
        b2 = party("B", 2)
        self.assertEqual((a1.guard_capacity, a2.guard_capacity), (1, 2))
        self.assertEqual((b1.guard_capacity, b2.guard_capacity), (3, 3))
        self.assertEqual((b1.initiative_bonus, b2.initiative_bonus), (2, 4))
        self.assertEqual(dict(b1.source.abilities)["Veil Affinity"], 0)
        self.assertIn(("Mace", "wielded"), b1.source.equipment)
        self.assertIn(("Shield", "held"), b1.source.equipment)

    def test_no_overlap_and_unresolved_tie(self):
        with self.assertRaisesRegex(ValueError, "overlaps another actor"):
            scene(soldier(), party(at=((1, 0),)))
        with self.assertRaisesRegex(UnresolvedDecision, "Initiative tie"):
            Encounter([party(name="R1"), party(name="R2", at=((3, 0),))],
                      {"R1": 12, "R2": 12}, seed=123)
        e = scene(party(name="R1"), party(name="R2", at=((3, 0),)),
                  score={"R1": 12, "R2": 12})
        self.assertEqual(e.order, ("R1", "R2"))


class G0LedgerTests(unittest.TestCase):
    def test_one_round_refresh_own_turn_regeneration_and_deterministic_ledger(self):
        def execute():
            s = soldier(at=((3, 0),))
            r = party()
            e = scene(s, r, score={"soldier": 9, "hero": 14})
            e.begin_round()
            e.start_turn("hero")
            self.assertEqual(r.ap_remaining, 42)
            self.assertEqual((r.guard_remaining, r.dodge_pressure,
                              r.reaction_available), (3, 0, True))
            e.spend_ap("hero", "physical", label="readied physical attempt")
            e.end_turn()
            e.start_turn("soldier")
            self.assertEqual((s.ap_remaining, s.guard_remaining), (42, 2))
            e.end_turn()
            e.begin_round()
            self.assertEqual(e.round, 2)
            self.assertEqual((s.guard_remaining, r.guard_remaining), (2, 3))
            self.assertEqual(r.ap_remaining, 0)
            with self.assertRaises(ValueError):
                e.begin_round()
            return e.serialize()
        self.assertEqual(execute(), execute())
        events = json.loads(execute())
        self.assertEqual([e["index"] for e in events], list(range(len(events))))
        self.assertIn("round_begin", [e["kind"] for e in events])
        self.assertEqual(sum(e["kind"] == "round_end" for e in events), 1)
        # Round End must precede the *next* Round Begin, not wait for it.
        ends = [i for i, ev in enumerate(events) if ev["kind"] == "round_end"]
        begins = [i for i, ev in enumerate(events) if ev["kind"] == "round_begin"]
        self.assertLess(ends[0], begins[1])

    def test_vp_available_committed_spent_refund_not_spent(self):
        s = sentry("prepared_start")
        e = scene(s)
        e.spend_vp("sentry", 1, mode="spent", label="paid effect")
        self.assertEqual((s.vp_available, s.vp_committed, s.vp_spent), (2, 3, 1))
        e.release_vp("sentry", 3, label="prepared sword Reserve ended")
        self.assertEqual((s.vp_available, s.vp_committed, s.vp_spent), (5, 0, 1))
        with self.assertRaises(ValueError):
            e.release_vp("sentry", 1, label="illegal spent refund")
        with self.assertRaises(ValueError):
            e.spend_vp("sentry", 6, mode="spent", label="overdraw")
        s.vp_available += 1
        with self.assertRaisesRegex(ValueError, "Max VP"):
            e.check()

    def test_legal_guard_and_dodge_are_defenses_not_reactions(self):
        a = soldier()
        r = party()
        e = scene(a, r)
        e.begin_round()
        self.assertEqual(e.defense("soldier", "guard", attack_key="hit1"), 18)
        self.assertEqual(e.defense("soldier", "guard", attack_key="hit2"), 18)
        with self.assertRaises(ValueError):
            e.defense("soldier", "guard", attack_key="hit3")
        self.assertEqual([e.defense("soldier", "dodge", attack_key=f"d{i}")
                          for i in range(4)], [13, 11, 9, 7])
        self.assertEqual(a.dodge_pressure, 8)
        self.assertTrue(a.reaction_available)
        self.assertIsNone(e.defense("soldier", "take_hit", attack_key="hit4"))
        self.assertEqual(a.dodge_pressure, 8)
        with self.assertRaises(ValueError):
            e.defense("hero", "guard", attack_key="no bow guard")
        with self.assertRaises(UnresolvedDecision):
            e.defense("soldier", "guard", attack_key="arrow", projectile=True)
        with self.assertRaises(ValueError):
            e.begin_round()  # Mid-round refresh is forbidden.

    def test_dying_at_round_begin_keeps_reaction_for_own_turn_recovery(self):
        # Dying Sentry has an unfinished wound, then spends the real
        # survival + repair + HP natural-regeneration budget at its own Step 2.
        a = sentry("cold_start")
        a.hp = 0
        a.wounds = [Wound("serious", 10, 9)]
        e = scene(a)
        e.begin_round()
        self.assertTrue(a.reaction_available)  # refreshed, not currently usable
        for kind in ("reaction", "opportunity"):
            with self.subTest(kind=kind):
                with self.assertRaisesRegex(ValueError, "Dying/dead actor"):
                    e.response_window(
                        Trigger("before-" + kind, "sentry", "sentry"),
                        on_interception=lambda *_: None,
                        spontaneous=(Response("sentry", kind, "unauthorized while Dying"),),
                        on_spontaneous=lambda *_: self.fail("Dying response resolved"))
                self.assertTrue(a.reaction_available)
                self.assertFalse(a.opportunity_active)
                self.assertEqual(a.opportunity_used, 0)
        self.assertFalse(any(x["kind"] == "spontaneous_committed"
                             for x in e.ledger))
        e.start_turn("sentry", regen_choice=RegenerationChoice(
            hp=1, repair=1, cancel_dying_loss=True))
        self.assertEqual((a.hp, a.vigor, a.wounds[0].progress), (1, 33, 10))
        self.assertTrue(a.reaction_available)  # no extra refresh, same capacity
        self.assertTrue(e.response_window(
            Trigger("after-recovery", "sentry", "sentry"),
            on_interception=lambda *_: None,
            spontaneous=(Response("sentry", "reaction", "explicit legal reaction probe"),),
            on_spontaneous=lambda st, tr, c: st.log("test_authorized_response",
                                                      actor=c.actor_id)))
        self.assertFalse(a.reaction_available)
        with self.assertRaisesRegex(ValueError, "Reaction already used"):
            e.response_window(
                Trigger("second-in-round", "sentry", "sentry"),
                on_interception=lambda *_: None,
                spontaneous=(Response("sentry", "reaction", "second"),),
                on_spontaneous=lambda *_: self.fail("Double Reaction"))
        e.check()

    def test_recovered_actors_can_activate_opportunity_once_per_round(self):
        a = sentry("cold_start")
        a.hp = 0
        a.wounds = [Wound("wound", 10, 9)]
        e = scene(a)
        e.begin_round()
        e.start_turn("sentry", regen_choice=RegenerationChoice(
            hp=1, repair=1, cancel_dying_loss=True))
        for index in (1, 2):  # Physical Tempo 42//20 == 2
            self.assertTrue(e.response_window(
                Trigger(f"opportunity-{index}", "sentry", "sentry"),
                on_interception=lambda *_: None,
                spontaneous=(Response("sentry", "opportunity", "eligible test trigger"),),
                on_spontaneous=lambda *_: None))
        self.assertFalse(a.reaction_available)
        self.assertTrue(a.opportunity_active)
        self.assertEqual(a.opportunity_used, 2)
        with self.assertRaisesRegex(ValueError, "Opportunity capacity exhausted"):
            e.response_window(
                Trigger("third-opportunity", "sentry", "sentry"),
                on_interception=lambda *_: None,
                spontaneous=(Response("sentry", "opportunity", "third"),),
                on_spontaneous=lambda *_: self.fail("Excess Opportunity"))

    def test_recovery_does_not_replenish_already_spent_reaction(self):
        a = sentry("cold_start")
        e = scene(a)
        e.begin_round()
        e.response_window(
            Trigger("earlier", "sentry", "sentry"),
            on_interception=lambda *_: None,
            spontaneous=(Response("sentry", "reaction", "prior legal response"),),
            on_spontaneous=lambda *_: None)
        self.assertFalse(a.reaction_available)
        # Source-resolved damage/earlier wound state is an input; G0 does
        # not invent the damaging event or an external spell execution.
        a.hp = 0
        a.wounds = [Wound("wound", 10, 9)]
        e.start_turn("sentry", regen_choice=RegenerationChoice(
            hp=1, repair=1, cancel_dying_loss=True))
        self.assertEqual(a.hp, 1)
        self.assertFalse(a.reaction_available)
        e.end_turn()
        e.begin_round()
        self.assertTrue(a.reaction_available)

    def test_incapacitated_attacker_cannot_poison_sequence_lock_or_ap(self):
        a = soldier()
        target = sentry("cold_start")
        e = scene(a, target, score={"soldier": 20, "sentry": 10})
        e.begin_round()
        e.start_turn("soldier")
        self.assertEqual(a.ap_remaining, 42)
        # A separate previously legal event incapacitates the attacker
        # after AP was established; G0 does not adjudicate that event.
        a.hp = 0
        baseline = len(e.ledger)
        with self.assertRaisesRegex(ValueError, "Dying/dead attacker"):
            e.declare_sequence("soldier", "sentry", ("B06-AT-03",), ("guard",))
        self.assertEqual(a.ap_remaining, 42)
        self.assertEqual(target.guard_remaining, 3)
        self.assertFalse(e.seen_sequences)
        self.assertEqual(len(e.ledger), baseline)
        # A separately authored external recovery (G3/G4) restores HP
        # before this turn ends; the original target is still eligible.
        a.hp = 1
        e.declare_sequence("soldier", "sentry", ("B06-AT-03",), ("guard",))
        self.assertEqual(a.ap_remaining, 18)
        self.assertEqual(target.guard_remaining, 2)
        self.assertIn(("soldier", "sentry"), e.seen_sequences)
        with self.assertRaisesRegex(ValueError, "Second ordinary"):
            e.declare_sequence("soldier", "sentry", ("B06-AT-03",), ("take_hit",))
        e.check()

    def test_round_end_expires_opportunity_and_blocks_stale_reaction(self):
        # First Opportunity uses the one Reaction, leaving a second available
        # Opportunity Attack in Physical Tempo; Round End must expire it.
        a = sentry("cold_start")
        e = scene(a)
        e.begin_round()
        self.assertTrue(e.response_window(
            Trigger("first-opportunity", "sentry", "sentry"),
            on_interception=lambda *_: None,
            spontaneous=(Response("sentry", "opportunity", "one legal trigger"),),
            on_spontaneous=lambda *_: None))
        self.assertTrue(a.opportunity_active)
        self.assertFalse(a.reaction_available)
        self.assertEqual(a.opportunity_used, 1)
        self.assertEqual(a.ap_total // a.physical_ap, 2)  # 42//20 == 2
        e.start_turn("sentry")
        e.end_turn()
        self.assertEqual(e.ledger[-1]["kind"], "round_end")
        self.assertEqual(e.ledger[-1]["detail"]["expired_opportunity_response"],
                         ["sentry"])
        self.assertFalse(a.opportunity_active)
        old_length = len(e.ledger)
        with self.assertRaisesRegex(ValueError, "outside an active round"):
            e.response_window(
                Trigger("post-round-opportunity", "sentry", "sentry"),
                on_interception=lambda *_: None,
                spontaneous=(Response("sentry", "opportunity", "illegal stale"),),
                on_spontaneous=lambda *_: self.fail("Opportunity after Round End"))
        self.assertEqual(len(e.ledger), old_length)
        self.assertEqual(a.opportunity_used, 1)
        self.assertFalse(a.reaction_available)
        e.begin_round()
        self.assertTrue(a.reaction_available)
        self.assertFalse(a.opportunity_active)
        self.assertEqual(a.opportunity_used, 0)
        self.assertTrue(e.response_window(
            Trigger("new-round-opportunity", "sentry", "sentry"),
            on_interception=lambda *_: None,
            spontaneous=(Response("sentry", "opportunity", "new round"),),
            on_spontaneous=lambda *_: None))
        e.check()

    def test_response_windows_rejected_before_first_or_after_last_turn(self):
        a = sentry("cold_start")
        e = scene(a)
        with self.assertRaisesRegex(ValueError, "outside an active round"):
            e.response_window(Trigger("before-combat", "sentry", "sentry"),
                              on_interception=lambda *_: None)
        self.assertEqual(len(e.ledger), 1)  # Encounter creation only.
        e.begin_round()
        e.start_turn("sentry")
        # Responses stay legal on the final actor's live own turn.
        self.assertTrue(e.response_window(
            Trigger("inside-final-turn", "sentry", "sentry"),
            on_interception=lambda *_: None,
            spontaneous=(Response("sentry", "reaction", "live turn"),),
            on_spontaneous=lambda *_: None))
        self.assertFalse(a.reaction_available)
        e.end_turn()
        before = e.serialize()
        with self.assertRaisesRegex(ValueError, "outside an active round"):
            e.response_window(
                Trigger("after-round", "sentry", "sentry"),
                on_interception=lambda *_: None,
                spontaneous=(Response("sentry", "reaction", "illegal late"),),
                on_spontaneous=lambda *_: self.fail("No after-round reaction"))
        self.assertEqual(e.serialize(), before)
        e.begin_round()
        self.assertTrue(a.reaction_available)

    def test_attack_profile_active_and_inactive_predicates_are_precommitted(self):
        # Both source predicates are required, not just profile membership.
        for start, illegal, legal in (
                ("cold_start", "B06-AT-02", "B06-AT-01"),
                ("prepared_start", "B06-AT-01", "B06-AT-02")):
            with self.subTest(start=start):
                caster = sentry(start)
                defender = soldier(at=((5, 0),))
                e = scene(caster, defender,
                          score={"sentry": 20, "soldier": 10})
                e.begin_round()
                e.start_turn("sentry")
                before = caster.ap_remaining
                with self.assertRaisesRegex(ValueError, "requires.*effect"):
                    e.declare_sequence("sentry", "soldier",
                                       (illegal,), ("guard",))
                self.assertEqual(caster.ap_remaining, before)
                self.assertEqual(defender.guard_remaining, 2)
                self.assertNotIn(("sentry", "soldier"), e.seen_sequences)
                e.declare_sequence("sentry", "soldier",
                                   (legal,), ("guard",))
                self.assertEqual(caster.ap_remaining, before - 20)
                self.assertEqual(defender.guard_remaining, 1)

    def test_hunter_contact_and_dying_defense_preflight_are_atomic(self):
        hunter_actor = hunter()
        opponent = soldier(at=((1, 0),))
        e = scene(hunter_actor, opponent,
                  score={"hunter": 20, "soldier": 10})
        e.begin_round()
        e.start_turn("hunter")
        before = hunter_actor.ap_remaining
        with self.assertRaisesRegex(UnresolvedDecision, "Hunter attack"):
            e.declare_sequence("hunter", "soldier",
                               ("B06-AT-04",), ("guard",))
        self.assertEqual(hunter_actor.ap_remaining, before)
        self.assertEqual(opponent.guard_remaining, 2)
        self.assertNotIn(("hunter", "soldier"), e.seen_sequences)

        attacker = sentry("cold_start")
        dying = soldier(at=((5, 0),))
        dying.hp = 0
        e2 = scene(attacker, dying,
                   score={"sentry": 20, "soldier": 10})
        e2.begin_round()
        e2.start_turn("sentry")
        with self.assertRaisesRegex(ValueError, "Dying/dead target"):
            e2.declare_sequence("sentry", "soldier",
                                ("B06-AT-01",), ("dodge",))
        self.assertEqual(attacker.ap_remaining, 42)
        self.assertEqual(dying.dodge_pressure, 0)
        self.assertNotIn(("sentry", "soldier"), e2.seen_sequences)
        e2.declare_sequence("sentry", "soldier",
                            ("B06-AT-01",), ("take_hit",))
        self.assertEqual(attacker.ap_remaining, 22)

    def test_expiry_is_committed_once_when_regeneration_policy_is_pending(self):
        a = soldier()
        e = scene(a)
        e.begin_round()
        e.start_turn("soldier")
        e.reserve("soldier", "future", "expires on next own turn")
        e.end_turn()
        # The round must end *now*, without requiring another begin_round.
        self.assertEqual(e.ledger[-1]["kind"], "round_end")
        e.begin_round()
        a.hp = 10
        with self.assertRaisesRegex(UnresolvedDecision, "regeneration allocation"):
            e.start_turn("soldier")
        self.assertEqual(e.current, "soldier")
        self.assertEqual(e.pending_regeneration, "soldier")
        self.assertFalse(e.reservations)
        self.assertEqual(sum(x["kind"] == "turn_start_expiry"
                             for x in e.ledger), 2)  # once each own turn
        with self.assertRaises(UnresolvedDecision):
            e.response_window(Trigger("future", "soldier", "soldier"),
                              on_interception=lambda *_: None)
        with self.assertRaises(ValueError):
            e.end_turn()
        e.start_turn("soldier", regen_choice=RegenerationChoice(hp=1))
        self.assertEqual((a.hp, a.vigor), (11, 35))
        self.assertIsNone(e.pending_regeneration)
        self.assertEqual(sum(x["kind"] == "turn_start_expiry"
                             for x in e.ledger), 2)
        self.assertTrue(e.response_window(
            Trigger("future", "soldier", "soldier"),
            on_interception=lambda *_: self.fail("Expired reservation fired")))
        self.assertEqual(sum(x["kind"] == "interception_released"
                             for x in e.ledger), 0)
        e.end_turn()
        self.assertEqual(sum(x["kind"] == "round_end" for x in e.ledger), 2)

    def test_no_illegal_second_sequence_or_dice_after_defense(self):
        a = soldier()
        b = sentry("cold_start")
        e = scene(a, b, score={"soldier": 20, "sentry": 10})
        e.begin_round()
        e.start_turn("soldier")
        e.declare_sequence("soldier", "sentry", ("B06-AT-03",), ("guard",))
        self.assertEqual((a.ap_remaining, b.guard_remaining), (18, 2))
        kinds = [x["kind"] for x in e.ledger]
        self.assertLess(kinds.index("attack_sequence_committed"),
                        kinds.index("defense_assigned"))
        self.assertEqual(kinds[-1], "unresolved_attack_roll")
        with self.assertRaisesRegex(ValueError, "Second ordinary"):
            e.declare_sequence("soldier", "sentry", ("B06-AT-03",), ("take_hit",))
        e.end_turn()
        e.start_turn("sentry")
        with self.assertRaises(ValueError):
            e.spend_ap("sentry", "full", label="not ready") if b.ap_remaining < b.ap_total else (
                e.spend_ap("sentry", "physical", label="paid"),
                e.spend_ap("sentry", "full", label="not ready"))
        with self.assertRaises(UnresolvedDecision):
            e.declare_sequence("sentry", "soldier", ("invented",), ("take_hit",))

    def test_regeneration_allocation_and_dying_third_vigor_debit(self):
        s = soldier()
        s.hp = 7
        s.wounds = [Wound("w1", 10, 2), Wound("w2", 20, 0)]
        e = scene(s)
        e.begin_round()
        with self.assertRaises(UnresolvedDecision):
            e.start_turn("soldier")
        # Fresh scenario for the explicit allocation probe.
        s2 = soldier()
        s2.hp = 7
        s2.wounds = [Wound("w1", 10, 2)]
        e2 = scene(s2)
        e2.begin_round()
        e2.start_turn("soldier", regen_choice=RegenerationChoice(hp=1, repair=1))
        self.assertEqual((s2.hp, s2.vigor, s2.wounds[0].progress), (8, 34, 3))
        self.assertIn("turn_resources", [x["kind"] for x in e2.ledger])
        e2_kinds = [x["kind"] for x in e2.ledger]
        self.assertLess(e2_kinds.index("turn_start_expiry"),
                        e2_kinds.index("regeneration_step"))
        e2.end_turn()
        e2.begin_round()
        e2.start_turn("soldier", regen_choice=RegenerationChoice(hp=1, repair=1))
        self.assertEqual((s2.hp, s2.vigor, s2.wounds[0].progress), (9, 32, 4))
        e2.end_turn()
        d = soldier()
        d.hp = 0
        d.wounds = [Wound("serious", 10, 0)]
        e3 = scene(d)
        e3.begin_round()
        e3.start_turn("soldier", regen_choice=RegenerationChoice(cancel_dying_loss=True,
                                                                 repair=1))
        self.assertEqual((d.hp, d.vigor, d.wounds[0].progress), (0, 34, 1))
        regen_event = next(x for x in e3.ledger if x["kind"] == "regeneration_step")
        self.assertTrue(regen_event["detail"]["survival_cancelled"])
        self.assertEqual(regen_event["detail"]["throughput_spent"], 2)
        z = soldier()
        z.hp, z.vigor = 0, 0
        e4 = scene(z)
        e4.begin_round()
        e4.start_turn("soldier")
        self.assertEqual((z.hp, z.vigor), (-1, 0))
        with self.assertRaisesRegex(ValueError, "Unconscious/dead"):
            e4.defense("soldier", "dodge", attack_key="dying")
        with self.assertRaisesRegex(ValueError, "Unconscious/dead"):
            e4.defense("soldier", "guard", attack_key="dying")
        self.assertIsNone(e4.defense("soldier", "take_hit", attack_key="dying"))
        for x in (e2, e3, e4):
            x.check()

    def test_non_dying_multiple_wound_allocation_requires_policy(self):
        a = soldier()
        a.hp = 10
        a.wounds = [Wound("arm", 10, 1), Wound("leg", 20, 2)]
        e = scene(a)
        e.begin_round()
        with self.assertRaisesRegex(UnresolvedDecision, "non-Dying wound"):
            e.start_turn("soldier", regen_choice=RegenerationChoice(repair=1))
        self.assertEqual(e.current, "soldier")
        self.assertEqual(e.pending_regeneration, "soldier")
        self.assertEqual((a.hp, a.vigor, [w.progress for w in a.wounds]),
                         (10, 36, [1, 2]))
        self.assertIn("unresolved_decision", [x["kind"] for x in e.ledger])
        # It remains possible to choose HP instead, without repair targeting.
        e.start_turn("soldier", regen_choice=RegenerationChoice(hp=1))
        self.assertEqual((a.hp, a.vigor), (11, 35))
        e.end_turn()

    def test_reject_dying_bypass_and_no_implicit_healing(self):
        a = soldier()
        a.hp = 0
        a.wounds = [Wound("a", 10, 0)]
        e = scene(a)
        e.begin_round()
        with self.assertRaises(ValueError):
            e.start_turn("soldier", regen_choice=RegenerationChoice(
                hp=1, cancel_dying_loss=True))
        self.assertEqual((a.hp, a.vigor, a.wounds[0].progress), (0, 36, 0))
        with self.assertRaisesRegex(ValueError, "exceeds throughput"):
            # Fresh actor avoids partial turn after invalid declaration.
            b = soldier(name="b", at=((5, 0),))
            b.hp = 10
            f = scene(b)
            f.begin_round()
            f.start_turn("b", regen_choice=RegenerationChoice(hp=3))

    def test_cancelled_interception_does_not_consume_spontaneous_reaction(self):
        a = soldier()
        s = sentry("cold_start")
        e = scene(a, s, score={"soldier": 20, "sentry": 10})
        e.begin_round()
        e.start_turn("soldier")
        e.reserve("soldier", "original", "source-backed interruption")
        e.end_turn()
        trigger = Trigger("original", "sentry", "soldier")
        def authorized_cancel(state, original, reservation):
            state.log("authorized_test_resolution", source="explicit scripted policy")
            original.legal = False  # Not an automatic property of Interception.
        ok = e.response_window(
            trigger, on_interception=authorized_cancel,
            spontaneous=(Response("sentry", "reaction", "Reactive Blink"),),
            on_spontaneous=lambda *_: self.fail("Cancelled trigger consumed Reaction"))
        self.assertFalse(ok)
        self.assertTrue(s.reaction_available)
        self.assertEqual((s.vp_available, s.vp_committed, s.vp_spent), (6, 0, 0))
        self.assertNotIn("spontaneous_committed", [x["kind"] for x in e.ledger])

    def test_nested_response_order_no_free_interrupt(self):
        a = soldier()
        s = sentry("cold_start")
        e = scene(a, s, score={"soldier": 20, "sentry": 10})
        e.begin_round()
        e.start_turn("soldier")
        e.reserve("soldier", "main", "prepared")
        e.end_turn()
        def intercept(state, trigger, reservation):
            self.assertTrue(trigger.legal)
            nested = Trigger("nested", "soldier", "sentry")
            state.response_window(nested, on_interception=lambda *_: None)
        self.assertTrue(e.response_window(
            Trigger("main", "sentry", "soldier"), on_interception=intercept,
            spontaneous=(Response("sentry", "reaction", "legal reaction"),),
            on_spontaneous=lambda st, tr, ch: st.log("reaction_resolved", actor=ch.actor_id)))
        kinds = [x["kind"] for x in e.ledger]
        idx_nested = next(i for i, x in enumerate(e.ledger)
                          if x["kind"] == "response_window_open" and x["detail"]["trigger"] == "nested")
        original_recheck = next(i for i, x in enumerate(e.ledger)
                                if x["kind"] == "trigger_rechecked_after_interceptions"
                                and x["detail"]["trigger"] == "main")
        self.assertLess(idx_nested, original_recheck)
        self.assertFalse(s.reaction_available)
        self.assertEqual(kinds[-1], "trigger_ready_to_resolve")


if __name__ == "__main__":
    unittest.main()
