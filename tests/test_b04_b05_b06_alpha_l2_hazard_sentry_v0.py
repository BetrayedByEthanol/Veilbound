"""Selected Alpha A/B L2 Hunter Bite/Endurance and Sentry live hazard regression."""
from copy import deepcopy
import unittest

from scripts.b04_b05_b06_alpha_l2_hazard_sentry_v0 import (
    run,attest,_hunter_scene,_priest_endurance,
)
from scripts.b04_b05_b06_alpha_l2_l3_progression_v0 import (
    _scene,_carry,award,candidate_awards,PARTY,
)
from scripts.b05_b06_cross_encounter_effect_continuity_v0 import (
    effect_state,validate_source,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class AlphaHunterSentryHazardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=run(variant="A")
        cls.b=run(variant="B")

    def test_01_native_source_bite_and_actual_injected_venom(self):
        for variant,r in (("A",self.a),("B",self.b)):
            with self.subTest(variant=variant):
                self.assertEqual(r["source_roster"]["priest"],variant)
                self.assertEqual(r["source_roster"]["anointed"],"AM")
                self.assertEqual(r["source_roster"]["gifted"],"G")
                self.assertEqual(r["source_roster"]["scholar"],"F")
                hunter=r["source_ledgers"]["hunter"]["events"]
                self.assertEqual(
                    [ev["detail"]["profile"] for ev in hunter
                     if ev["kind"]=="g5_melee_roll"],
                    ["B06-AT-04","B06-AT-04"])
                self.assertEqual(
                    [ev["detail"]["outcome"] for ev in hunter
                     if ev["kind"]=="g5_melee_resolved"],
                    ["hit","miss"])
                self.assertEqual(
                    sum(ev["kind"]=="g44_hunter_accepted" for ev in hunter),1)
                self.assertEqual(
                    sum(ev["kind"]=="g5_terminal_exit" for ev in hunter),4)
                self.assertEqual(
                    r["hunter_native_hazard"]["unified_instances"]["priest"]["result"],
                    "Full")
                self.assertEqual(
                    r["hunter_native_hazard"]["unified_instances"]["priest"]["stage"],
                    0)

    def test_02_only_source_prepared_B_can_cast_endurance(self):
        self.assertIsNone(self.a["endurance_effect"])
        self.assertIsNotNone(self.b["endurance_effect"])
        for variant,r in (("A",self.a),("B",self.b)):
            events=r["source_ledgers"]["hunter"]["events"]
            paid=[e for e in events if e["kind"]=="g44_endurance_applied"]
            self.assertEqual(len(paid),int(variant=="B"))
            if paid:
                self.assertEqual(paid[0]["detail"]["caster"],"priest")
                self.assertEqual(paid[0]["detail"]["recipient"],"priest")
                self.assertEqual(paid[0]["detail"]["mode"],"suppression")
                self.assertEqual(paid[0]["detail"]["cost"],2)
                self.assertEqual(len(r["hunter_native_hazard"]["endurance_effects"]),1)
        scene,_=_hunter_scene("A",0)
        with self.assertRaises(UnresolvedDecision):
            _priest_endurance(scene,"A")

    def test_03_actual_G4_hazard_ids_and_pending_deadlines_migrate(self):
        for r in (self.a,self.b):
            before=r["hunter_native_hazard"]
            after=r["hazard_imported"]
            self.assertEqual(before["exposure_ids"],after["exposure_ids"])
            self.assertEqual(before["hunter_keys"],after["hunter_keys"])
            self.assertEqual(before["unified_instances"],after["unified_instances"])
            self.assertEqual(before["endurance_effects"],after["endurance_effects"])
            self.assertEqual(before["recovery_serial"],after["recovery_serial"])
            for event_id,ev in before["clock_events"].items():
                self.assertEqual(after["clock_events"][event_id]["ident"],ev["ident"])
                self.assertEqual(after["clock_events"][event_id]["due_seconds"],
                                 ev["due_seconds"])
            self.assertEqual(r["handoff"]["before_hazard_sha256"],
                             canonical_digest(before))
            self.assertEqual(r["handoff"]["after_hazard_sha256"],
                             canonical_digest(after))
            self.assertTrue(r["handoff"]["carry_source_hazards"])
            self.assertTrue(r["handoff"]["no_free_refill"])
            self.assertEqual(r["handoff"]["elapsed_seconds"],12)

    def test_04_original_cold_Sentry_delivers_HP_Fire_and_Vigor_damage(self):
        for r in (self.a,self.b):
            sentry=r["source_ledgers"]["sentry"]["events"]
            reserve=[e for e in sentry
                     if e["kind"]=="g3_effect_established"
                     and e["detail"]["effect_kind"]=="Sentry Sword Reserve"]
            self.assertEqual(len(reserve),1)
            resolved=[e for e in sentry
                      if e["kind"]=="g5_melee_resolved"
                      and e["detail"]["profile"]=="B06-AT-02"]
            self.assertEqual(len(resolved),1)
            self.assertEqual(resolved[0]["detail"]["outcome"],"hit")
            self.assertEqual(
                sum(e["kind"]=="g5_terminal_exit" for e in sentry),4)
            self.assertTrue(any(
                e["kind"]=="g4_damage_applied"
                and e["detail"].get("recipient")=="priest"
                for e in sentry))
            self.assertGreater(
                r["sentry_exit_party"]["priest"]["hp"],0)

    def test_05_venom_stage_and_endurance_expiry_use_original_clock(self):
        for r in (self.a,self.b):
            start=r["hazard_imported"]["unified_instances"]["priest"]
            self.assertEqual(start["stage"],0)
            onset=r["onset_hazard"]["unified_instances"]["priest"]
            self.assertEqual(onset["stage"],1)
            self.assertEqual(r["onset_hazard"]["modifiers"]["priest"]["mp"],-2)
            self.assertEqual(r["expiry_hazard"]["modifiers"]["priest"],{})
            self.assertFalse(
                r["expiry_hazard"]["unified_instances"]["priest"]["active"])
            self.assertTrue(r["milestone_blocked"])
            self.assertEqual(r["independently_certified_focuses"],0)
            self.assertEqual(r["strict_mvp_exits_met"],0)

    def test_06_preflight_rejects_cross_level_live_hazards(self):
        hunter,_=_hunter_scene("B",0)
        next_combat,_,_,_=_scene(3,"B","sentry_cold",1)
        before=canonical_digest(effect_state(hunter.e,party=PARTY))
        with self.assertRaises(UnresolvedDecision):
            _carry(hunter.e,next_combat.e,travel_seconds=0,
                   reference="forbidden-cross-level",
                   carry_hazards=True)
        self.assertEqual(before,
                         canonical_digest(effect_state(hunter.e,party=PARTY)))
        with self.assertRaises(UnresolvedDecision):
            award(hunter.e,candidate_awards()[1],variant="B")

    def test_07_hazard_source_validation_rejects_tampered_identity(self):
        hunter,_=_hunter_scene("B",0)
        v=hunter.e.g4.toxins.instances["priest"]
        v["stage"]=3
        with self.assertRaises(UnresolvedDecision):
            validate_source(hunter.e,party=PARTY)
        next_combat,_,_,_=_scene(2,"B","sentry_cold",1)
        with self.assertRaises(UnresolvedDecision):
            _carry(hunter.e,next_combat.e,travel_seconds=0,
                   reference="tampered-venom",carry_hazards=True)

    def test_08_old_hazard_bridge_default_not_changed_by_alpha_roster(self):
        hunter,_=_hunter_scene("A",0)
        next_combat,_,_,_=_scene(2,"A","sentry_cold",1)
        with self.assertRaises(UnresolvedDecision):
            _carry(hunter.e,next_combat.e,travel_seconds=0,
                   reference="omitted-opt-in")

    def test_09_exact_replay_rejects_reshashed_source_ledger(self):
        for variant,r in (("A",self.a),("B",self.b)):
            self.assertEqual(attest(r,variant=variant)["digest"],r["digest"])
        fake=deepcopy(self.b)
        fake["source_ledgers"]["hunter"]["events"][0]["kind"]="fabrication"
        fake["source_ledgers"]["hunter"]["sha256"]=canonical_digest(
            fake["source_ledgers"]["hunter"]["events"])
        fake["digest"]=canonical_digest({k:v for k,v in fake.items() if k!="digest"})
        with self.assertRaises(AssertionError):
            attest(fake,variant="B")

    def test_10_strict_variant_and_travel_inputs(self):
        for kw in ({"variant":"Z"},{"seed":-1},
                   {"travel_seconds":31},{"travel_seconds":-1},
                   {"travel_seconds":True}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):
                    run(**kw)


if __name__=="__main__":
    unittest.main()
