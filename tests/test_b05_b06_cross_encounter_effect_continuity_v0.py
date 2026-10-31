"""B05/B06 genuine G4.2/G4.3/G4.4/maintained G3 cross-scene receipts."""
import unittest
from copy import deepcopy

from scripts.b05_b06_native_party_continuity_v0 import (
    _first_withdrawal, _new_scene, handoff, party_state,
)
from scripts.b05_b06_cross_encounter_effect_continuity_v0 import effect_state
from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_g8_soldier_sentry_full_pack_v0 import (
    _scene, _turn, _foe_turn, _player_turn, _terminal, PARTY,
)
from scripts.b06_ranged_v0 import ShotChoice


def paid_first_scene(*, stone=False, endurance=False):
    """Original G8 native Soldier terminal with source-paid alternate R1 spell."""
    combat=_scene("soldier",3,0,"opposed_withdrawal")
    e=combat.e
    e.g4.clock.enter_initiative()
    if endurance:
        answer=e.g4.toxins.apply(
            "guardian","TX-EN",exposure_key="native:travel:en",
            source="authored:contaminated-ration",route="ingestion",
            delivery_verified=True,resistance_die=1)
        assert answer["outcome"]=="accepted"
    for round_no in (1,2):
        if round_no==2:
            combat.bridge.begin_next_round()
        for ident in ("foe",*PARTY):
            _turn(combat,ident)
            if ident=="foe":
                _foe_turn(combat,"soldier","opposed_withdrawal",round_no)
            elif round_no==1 and ident=="archer":
                e.g2.bow_sequence("archer","foe",(ShotChoice(primary_face=1),))
            elif round_no==1 and ident=="guardian" and endurance:
                result=e.g4.venom.cast_endurance(
                    "guardian","guardian",profile="Self",mode="suppression",
                    source_authorized=True,
                    source_reference="Low Priest B L3 prepared Venom Endurance",
                    ordinary_cost=2)
                assert result is not None
            elif round_no==1 and ident=="scholar" and stone:
                assert e.g3.cast_stone("scholar") is not None
            elif round_no==2:
                _player_turn(combat,ident,"opposed_withdrawal",round_no,"soldier")
            combat.bridge.end_current_turn()
    assert _terminal(combat,"opposed_withdrawal","soldier")=="party_scene_withdrawal"
    e.g4.clock.leave_initiative()
    return e


def fresh():
    return _new_scene("sentry_cold",3,0,prepared_only=True)[0]


class CrossEncounterEffectContinuationTests(unittest.TestCase):
    def test_01_unified_hourly_toxin_has_same_deadline_and_native_pulse(self):
        first=_first_withdrawal(3,0)
        accepted=first.g4.toxins.apply(
            "guardian","TX-NP",exposure_key="native:np:before-gate",
            source="GM:inhaled-dust",route="ingestion",
            delivery_verified=True,resistance_die=1)
        # TX-NP is ingestion, source exposure is independently authenticated.
        self.assertEqual(accepted["outcome"],"accepted")
        original=first.g4.toxins.active("guardian")
        self.assertEqual(original["marker"],"toxin:native:np:before-gate:pulse:1")
        next_scene=fresh()
        receipt=handoff(first,next_scene,elapsed_seconds=100,
                        travel_ref="GM:to-next-gate",carry_effects=True)
        self.assertEqual(receipt["effect_continuation_enabled"],True)
        self.assertEqual(receipt["native_effect_continuation_sha256"],
                         canonical_digest(effect_state(next_scene)))
        self.assertEqual(effect_state(first),effect_state(next_scene))
        self.assertEqual(next_scene.g4.toxins.active("guardian")["key"],
                         "native:np:before-gate")
        marker=next_scene.g4.toxins.active("guardian")["marker"]
        remain=next_scene.g4.clock.events[marker].due_seconds-100
        self.assertGreater(remain,0)
        self.assertLess(remain,3600)
        before=next_scene.actors["guardian"].vigor
        next_scene.g4.clock.advance_exploration(remain)
        self.assertEqual(next_scene.actors["guardian"].vigor,before-1)
        self.assertEqual(next_scene.g4.toxins.active("guardian")["applied"],1)
        self.assertEqual(next_scene.g4.toxins.active("guardian")["remaining"],3)

    def test_02_source_paid_endurance_suppression_retains_units_phase_and_expiry(self):
        first=paid_first_scene(endurance=True)
        effect=first.g4.venom.for_recipient("guardian")
        self.assertEqual((effect["mode"],effect["cost"]),("suppression",2))
        self.assertTrue(effect["covered"])
        self.assertEqual(first.actors["guardian"].vp_spent,2)
        self.assertEqual(first.g4.toxins.active("guardian")["profile"],"TX-EN")
        next_scene=fresh()
        receipt=handoff(first,next_scene,elapsed_seconds=1,
                        travel_ref="GM:still-toxic",carry_effects=True)
        self.assertTrue(receipt["native_effect_continuation_sha256"])
        self.assertEqual(effect_state(first),effect_state(next_scene))
        self.assertEqual(next_scene.actors["guardian"].vp_spent,2)
        self.assertEqual(next_scene.g4.venom.for_recipient("guardian")["id"],
                         effect["id"])
        self.assertEqual(next_scene.g4.venom.for_recipient("guardian")["phase"],1)
        self.assertEqual(next_scene.g4.toxins.modifier("guardian","physical_exertion"),0)
        next_scene.g4.clock.advance_exploration(5)
        v=next_scene.g4.venom.for_recipient("guardian")
        self.assertEqual(v["units"],effect["units"]-1)
        self.assertEqual(v["phase"],0)
        self.assertTrue(v["covered"])
        self.assertEqual(next_scene.actors["guardian"].vp_spent,2)
        due=next_scene.g4.clock.events[v["expiry"]].due_seconds
        next_scene.g4.clock.advance_exploration(due-next_scene.g4.clock.world_seconds)
        self.assertIsNone(next_scene.g4.venom.for_recipient("guardian"))
        self.assertIsNotNone(next_scene.g4.toxins.active("guardian"))
        self.assertEqual(next_scene.g4.toxins.modifier("guardian","physical_exertion"),-1)

    def test_03_maintained_stone_skin_host_keeps_original_reserve_no_recast(self):
        first=paid_first_scene(stone=True)
        skin=first.g3.active("scholar","Stone Skin")
        self.assertEqual(len(skin),1)
        old=skin[0]
        before=first.actors["scholar"].vp_committed
        self.assertEqual(old.committed,before)
        next_scene=fresh()
        handoff(first,next_scene,elapsed_seconds=120,
                travel_ref="GM:known-route",carry_effects=True)
        new=next_scene.g3.active("scholar","Stone Skin")
        self.assertEqual(len(new),1)
        self.assertEqual(vars(old),vars(new[0]))
        self.assertIsNot(old,new[0])
        self.assertEqual(next_scene.actors["scholar"].vp_committed,before)
        self.assertEqual(next_scene.actors["scholar"].vp_spent,0)
        self.assertEqual(next_scene.g3.resistance("scholar","Physical"),2)

    def test_04_legacy_toxin_preserves_local_six_second_phase(self):
        first=_first_withdrawal(3,0)
        first.g4.schedule_hemotoxin(
            "guardian",exposure_key="native:legacy-hm",
            actual_exposure=True,resistance_total=12,
            wound_location_roll=8)
        next_scene=fresh()
        handoff(first,next_scene,elapsed_seconds=2,
                travel_ref="GM:short-travel",carry_effects=True)
        self.assertEqual(next_scene.g4.short_toxins[0]["phase"],2)
        self.assertEqual(next_scene.g4.short_toxins[0]["left"],3)
        hp=next_scene.actors["guardian"].hp
        next_scene.g4.clock.advance_exploration(4)
        self.assertEqual(next_scene.g4.short_toxins[0]["left"],2)
        self.assertEqual(next_scene.actors["guardian"].hp,hp-1)

    def test_05_recovery_during_long_toxin_keeps_original_checkpoint(self):
        first=_first_withdrawal(3,0)
        first.g4.toxins.apply(
            "guardian","TX-HE",exposure_key="native:he:01",
            source="GM:ingested-alkaloid",route="ingestion",
            delivery_verified=True,resistance_die=1)
        before=first.g4.clock.events[
            first.g4.toxins.active("guardian")["recovery_id"]].ident
        next_scene=fresh()
        handoff(first,next_scene,elapsed_seconds=100,
                travel_ref="GM:after-ration",carry_effects=True)
        self.assertEqual(next_scene.g4.toxins.active("guardian")["recovery_id"],before)
        checkpoint=next_scene.g4.clock.events[before]
        remaining=checkpoint.due_seconds-next_scene.g4.clock.world_seconds
        next_scene.g4.clock.advance_exploration(remaining)
        self.assertIsNone(next_scene.g4.toxins.active("guardian"))
        self.assertEqual(len([e for e in next_scene.ledger
                              if e["kind"]=="g43_hepatotoxin_recovery"]),1)
        self.assertEqual(len([e for e in next_scene.ledger
                              if e["kind"]=="g4_six_hour_recovery"
                              and e["detail"]["actor"]=="guardian"]),1)

    def test_06_rejected_destination_and_failed_future_hazard_do_not_charge_time(self):
        first=_first_withdrawal(3,0)
        first.g4.toxins.apply(
            "guardian","TX-NP",exposure_key="native:np:retry",
            source="GM:inhaled-dust",route="ingestion",
            delivery_verified=True,resistance_die=1)
        next_scene=fresh()
        next_scene.actors["archer"].ammunition=999
        digest=canonical_digest(first.ledger)
        state=effect_state(first)
        with self.assertRaises(UnresolvedDecision):
            handoff(first,next_scene,elapsed_seconds=10800,
                    travel_ref="GM:three-hour-route",carry_effects=True)
        self.assertEqual(first.g4.clock.world_seconds,0)
        self.assertEqual(effect_state(first),state)
        self.assertEqual(canonical_digest(first.ledger),digest)
        next_scene.actors["archer"].ammunition=20
        handoff(first,next_scene,elapsed_seconds=1,
                travel_ref="GM:one-second-route",carry_effects=True)
        self.assertEqual(first.g4.clock.world_seconds,1)

    def test_07_bad_toxin_marker_and_unsupported_spell_duration_fail_before_travel(self):
        first=_first_withdrawal(3,0)
        first.g4.toxins.apply(
            "guardian","TX-EN",exposure_key="native:en:missing",
            source="GM:ingestion",route="ingestion",
            delivery_verified=True,resistance_die=1)
        marker=first.g4.toxins.active("guardian")["marker"]
        first.g4.clock.events[marker].canceled=True
        next_scene=fresh()
        with self.assertRaises(UnresolvedDecision):
            handoff(first,next_scene,elapsed_seconds=100,
                    travel_ref="GM:invalid-marker",carry_effects=True)
        self.assertEqual(first.g4.clock.world_seconds,0)
        first.g4.clock.events[marker].canceled=False
        first.actors["scholar"].maintained.append("unsourced-round-duration")
        with self.assertRaises(UnresolvedDecision):
            handoff(first,next_scene,elapsed_seconds=100,
                    travel_ref="GM:unsupported-round-effect",carry_effects=True)

    def test_08_old_path_stays_fail_closed_without_explicit_effect_opt_in(self):
        first=_first_withdrawal(3,0)
        first.g4.toxins.apply(
            "guardian","TX-EN",exposure_key="native:en:old-boundary",
            source="GM:ingested",route="ingestion",
            delivery_verified=True,resistance_die=1)
        with self.assertRaises(UnresolvedDecision):
            handoff(first,fresh(),elapsed_seconds=0,
                    travel_ref="GM:unsupported",carry_effects=False)
        self.assertEqual(first.g4.clock.world_seconds,0)

    def test_09_replay_keys_survive_cross_encounter(self):
        first=_first_withdrawal(3,0)
        first.g4.toxins.apply(
            "guardian","TX-NP",exposure_key="native:np:dedup",
            source="GM:inhaled-dust",route="ingestion",
            delivery_verified=True,resistance_die=1)
        next_scene=fresh()
        handoff(first,next_scene,elapsed_seconds=1,
                travel_ref="GM:dedup",carry_effects=True)
        with self.assertRaises(ValueError):
            next_scene.g4.toxins.apply(
                "vanguard","TX-EN",exposure_key="native:np:dedup",
                source="GM:new-contamination",route="ingestion",
                delivery_verified=True,resistance_die=1)

    def test_10_still_no_human_certification(self):
        first=_first_withdrawal(3,0)
        next_scene=fresh()
        receipt=handoff(first,next_scene,elapsed_seconds=0,
                        travel_ref="GM:zero-safe-route",carry_effects=True)
        self.assertTrue(receipt["effect_continuation_enabled"])
        self.assertIsNotNone(receipt["native_effect_continuation_sha256"])
        self.assertEqual(receipt["prior_party_sha256"],receipt["incoming_party_sha256"])


if __name__=="__main__":
    unittest.main()
