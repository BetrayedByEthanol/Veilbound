"""Native cross-encounter party-resource chain, no phantom refresh."""
import unittest
from copy import deepcopy
from dataclasses import replace

from scripts.b05_b06_native_party_continuity_v0 import (
    PARTY, _first_withdrawal, _new_scene, _resolve_victory, _boundary,
    handoff, party_state, run_chain,
)
from scripts.b06_encounter_state_v0 import Wound, UnresolvedDecision
from scripts.b06_damage_v0 import DamagePacket
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_g8_soldier_sentry_full_pack_v0 import _scene


class NativePartyContinuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run_chain(level=3,seed=0,travel_seconds=300)

    def test_01_two_genuine_hostile_terminals_and_separate_ledgers(self):
        r=self.report
        self.assertEqual(tuple(r["outcomes"]),
                         ("party_scene_withdrawal","sentry_defeat"))
        self.assertNotEqual(r["first_ledger_sha256"],r["second_ledger_sha256"])
        self.assertTrue(r["same_party_source_all_scenes"])
        self.assertEqual(r["source_bound_native_witnesses"],2)
        self.assertEqual(r["gm_human_sessions"],0)
        self.assertEqual(r["independently_certified_focuses"],0)
        self.assertEqual(r["strict_mvp_exits_met"],0)

    def test_02_real_soldier_injury_and_bow_ammunition_carried_without_refill(self):
        r=self.report
        old=r["first_state"]
        new=r["handoff"]
        self.assertLess(old["vanguard"]["hp"],12)
        self.assertEqual(old["archer"]["ammunition"],19)
        self.assertEqual(new["prior_party_sha256"],new["incoming_party_sha256"])
        self.assertTrue(new["no_free_restore"])
        self.assertEqual(new["elapsed_seconds"],300)
        self.assertEqual(new["world_seconds"],300)
        self.assertTrue(new["old_terminal_ledger_sha256"])
        self.assertEqual(new["prior_party_sha256"],canonical_digest(old))
        self.assertEqual(r["second_final_state"]["archer"]["ammunition"],19)
        self.assertEqual(r["second_final_state"]["vanguard"]["hp"],old["vanguard"]["hp"])

    def test_03_preserves_purchased_vp_and_new_chosen_rite_at_next_handoff(self):
        old=_first_withdrawal(3,0)
        c,_=_new_scene("sentry_cold",3,0,previous=old,travel_ref="test:gate-to-sentry")
        self.assertEqual(_resolve_victory(c,"sentry_cold"),"sentry_defeat")
        r=c.e.actors["archer"]
        self.assertEqual((r.vp_committed, r.vp_spent), (1,0))
        self.assertEqual(len(c.e.g3.active("archer","Guided Regeneration")),1)
        third,receipt=_new_scene("soldier",3,0,previous=c.e,
                                 travel_ref="test:sentry-to-road",elapsed_seconds=60)
        new=third.e.actors["archer"]
        self.assertEqual(new.vp_committed,1)
        self.assertEqual(new.vp_available,r.vp_available)
        self.assertEqual(new.ammunition,19)
        self.assertEqual(new.maintained,r.maintained)
        self.assertEqual(len(third.e.g3.active("archer","Guided Regeneration")),1)
        self.assertEqual(receipt["prior_party_sha256"],receipt["incoming_party_sha256"])
        self.assertGreater(third.e.g3.next_effect,0)

    def test_04_authored_six_hour_clock_is_earned_and_preserves_phase(self):
        first=_first_withdrawal(3,0)
        first.g4.apply_damage(
            "guardian",(DamagePacket("vigor","Toxin",9),),
            event_key="fixture:independent_vigor_loss",
            cause="author-fixture:source-hazard")
        before=first.actors["guardian"].vigor
        next_scene,_=_new_scene("sentry_cold",3,0,previous=first,
                                elapsed_seconds=21600,
                                travel_ref="test:actually-six-hours")
        after=next_scene.e.actors["guardian"].vigor
        self.assertGreater(after,before)
        self.assertLessEqual(after,next_scene.e.actors["guardian"].vigor_max)
        self.assertEqual(next_scene.e.g4.clock.world_seconds,21600)
        pending=[x for x in next_scene.e.g4.clock.events.values()
                 if x.actor_id=="guardian" and x.kind=="recovery"
                 and not x.consumed]
        self.assertEqual(len(pending),1)
        # G4.2 credits the already completed combat boundaries before the
        # source's first six-hour event; do not restart a fresh 3600-round
        # interval on import. Its exact native conversion is 3598 here.
        self.assertEqual(pending[0].due_round,3598)
        self.assertTrue(any(x["kind"]=="g4_six_hour_recovery"
                            and x["detail"]["actor"]=="guardian"
                            for x in first.ledger))

    def test_05_carried_wound_objects_are_deep_copied_with_source_metadata(self):
        first=_first_withdrawal(3,0)
        # An independently supplied pre-existing Wound is an API transport
        # fixture, not a fabricated G4 wound-generation proof.
        first.actors["guardian"].wounds.append(
            Wound("historical:chest",requirement=10,progress=2,
                  severity="Serious",location="Chest",source_event="GM:old-hit"))
        first.check()
        follow,_=_new_scene("sentry_cold",3,0,previous=first,
                            travel_ref="test:wound-carry")
        old=first.actors["guardian"].wounds[0]
        fresh=follow.e.actors["guardian"].wounds[0]
        self.assertEqual(vars(old),vars(fresh))
        self.assertIsNot(old,fresh)
        self.assertEqual(party_state(first)["guardian"]["wounds"],
                         party_state(follow.e)["guardian"]["wounds"])

    def test_06_pending_turn_blocks_handoff_before_mutation(self):
        first=_scene("soldier",3,0,"opposed_withdrawal").e
        following,_=_new_scene("sentry_cold",3,0,prepared_only=True)
        digest=canonical_digest(party_state(following))
        with self.assertRaises(UnresolvedDecision):
            handoff(first,following,elapsed_seconds=10,travel_ref="test:unsettled")
        self.assertEqual(digest,canonical_digest(party_state(following)))

    def test_07_changed_source_and_not_pristine_next_state_rejected(self):
        first=_first_withdrawal(3,0)
        following,_=_new_scene("sentry_cold",3,0,prepared_only=True)
        following.actors["archer"].source=replace(
            following.actors["archer"].source,digest="0"*64)
        with self.assertRaises(UnresolvedDecision):
            handoff(first,following,elapsed_seconds=0,travel_ref="test:tamper")
        following,_=_new_scene("sentry_cold",3,0,prepared_only=True)
        following.actors["archer"].ammunition=999
        # Carry-in must not silently accept a pre-modified character.
        with self.assertRaises(UnresolvedDecision):
            handoff(first,following,elapsed_seconds=0,travel_ref="test:not-pristine")

    def test_07b_rejected_three_hour_destination_cannot_double_charge_travel(self):
        # Codex P2: source must be byte-for-byte/clock-for-clock untouched
        # when a destination's ammunition was altered before the handoff.
        first = _first_withdrawal(3, 0)
        next_scene, _ = _new_scene("sentry_cold", 3, 0, prepared_only=True)
        next_scene.actors["archer"].ammunition = 999
        source_digest = canonical_digest(first.ledger)
        source_party = party_state(first)
        source_events = deepcopy(first.g4.clock.events)
        source_serial = deepcopy(first.g4.clock.recovery_serial)
        with self.assertRaises(UnresolvedDecision):
            handoff(first, next_scene, elapsed_seconds=10800,
                    travel_ref="source:three-hour-route")
        self.assertEqual(first.g4.clock.world_seconds, 0)
        self.assertEqual(first.g4.clock.events, source_events)
        self.assertEqual(first.g4.clock.recovery_serial, source_serial)
        self.assertEqual(party_state(first), source_party)
        self.assertEqual(canonical_digest(first.ledger), source_digest)
        self.assertFalse(any(ev["kind"] == "g4_six_hour_recovery"
                             for ev in first.ledger))

        # Correct only the destination; the original three hours are paid
        # exactly once. Otherwise a second 10800 would spuriously award 6h.
        next_scene.actors["archer"].ammunition = 20
        receipt = handoff(first, next_scene, elapsed_seconds=10800,
                          travel_ref="source:three-hour-route")
        self.assertEqual(first.g4.clock.world_seconds, 10800)
        self.assertEqual(next_scene.g4.clock.world_seconds, 10800)
        self.assertEqual(receipt["world_seconds"], 10800)
        self.assertTrue(receipt["no_free_restore"])
        self.assertFalse(any(ev["kind"] == "g4_six_hour_recovery"
                             for ev in first.ledger))
        self.assertEqual(receipt["prior_party_sha256"],
                         receipt["incoming_party_sha256"])

    def test_07c_destination_host_clock_and_gear_collisions_preflight(self):
        from scripts.b06_spells_v0 import SpellEffect
        first = _first_withdrawal(3, 0)
        source_digest = canonical_digest(first.ledger)
        clock_events = deepcopy(first.g4.clock.events)
        for fault in ("party_effect", "future_recovery_collision", "wielded"):
            with self.subTest(fault=fault):
                next_scene, _ = _new_scene("sentry_cold", 3, 0,
                                           prepared_only=True)
                if fault == "party_effect":
                    next_scene.g3.effects[("archer", "G3-0001")] = SpellEffect(
                        "G3-0001", "archer", "Guided Regeneration",
                        "archer", 1, chosen=True)
                elif fault == "future_recovery_collision":
                    next_scene.g4.clock.events["recovery:archer:2"] = replace(
                        next_scene.g4.clock.events["recovery:foe:1"],
                        ident="recovery:archer:2")
                else:
                    next_scene.g2.wielded["archer"].clear()
                with self.assertRaises(UnresolvedDecision):
                    handoff(first, next_scene, elapsed_seconds=10800,
                            travel_ref="source:rejected-transition")
                self.assertEqual(first.g4.clock.world_seconds, 0)
                self.assertEqual(first.g4.clock.events, clock_events)
                self.assertEqual(canonical_digest(first.ledger), source_digest)

    def test_08_unhandled_poison_or_live_nonrecovery_clock_rejected(self):
        first=_first_withdrawal(3,0)
        new,_=_new_scene("sentry_cold",3,0,prepared_only=True)
        first.g4.short_toxins.append({"recipient":"vanguard","left":2})
        with self.assertRaises(UnresolvedDecision):
            handoff(first,new,elapsed_seconds=0,travel_ref="test:poison")
        first.g4.short_toxins.clear()
        first.g4.clock.schedule_milestone(
            "vanguard",event_id="GM:unresolved-continuation",
            source="source-owned:unknown",delay_seconds=200)
        with self.assertRaises(UnresolvedDecision):
            handoff(first,new,elapsed_seconds=0,travel_ref="test:marker")

    def test_09_unmodeled_maintained_effects_are_not_dropped(self):
        from scripts.b06_spells_v0 import SpellEffect
        first=_first_withdrawal(3,0)
        first.actors["archer"].maintained.append("forged:host")
        first.g3.effects[("archer","forged:host")]=SpellEffect(
            "forged:host","archer","Vital Shelter","archer",1)
        first.actors["archer"].vp_available-=1
        first.actors["archer"].vp_committed+=1
        new,_=_new_scene("sentry_cold",3,0,prepared_only=True)
        with self.assertRaises(UnresolvedDecision):
            handoff(first,new,elapsed_seconds=0,travel_ref="test:unsupported-host")

    def test_10_refuse_false_travel_or_out_of_scope_profile(self):
        for sec in (-1,True,1.2):
            with self.subTest(sec=sec),self.assertRaises(ValueError):
                run_chain(level=3,seed=0,travel_seconds=sec)
        first=_first_withdrawal(3,0)
        next_scene,_=_new_scene("sentry_cold",3,0,prepared_only=True)
        for travel in ("",None,0):
            with self.subTest(travel=travel),self.assertRaises(ValueError):
                handoff(first,next_scene,elapsed_seconds=0,travel_ref=travel)

    def test_11_source_and_round_counts_do_not_become_certification(self):
        report=run_chain(level=2,seed=0,travel_seconds=0)
        self.assertEqual(report["source_bound_native_witnesses"],2)
        self.assertEqual(report["gm_human_sessions"],0)
        self.assertEqual(report["independently_certified_focuses"],0)
        self.assertEqual(report["strict_mvp_exits_met"],0)
        self.assertFalse(report["representative_balance"])
        self.assertIsNone(report["hunter_cr"])


if __name__ == "__main__":
    unittest.main()
