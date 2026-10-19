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
        self.assertIsNone(e.current)
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
