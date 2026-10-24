"""B04/B05 Medium Life: source-native encounter and finite-resource comparisons."""
from copy import deepcopy
import unittest

from scripts.b05_medium_life_encounter_balance_v0 import (
    OPPONENTS, _scene, _start, attest_policy, run_matrix, run_policy,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class MediumLifeEncounterIntegrationTests(unittest.TestCase):
    def test_01_full_source_matrix_levels_and_policies(self):
        matrix=run_matrix(seed=0)
        self.assertEqual(matrix["policy_count"],27)
        self.assertEqual(len(matrix["trials"]),27)
        self.assertFalse(matrix["independent_medium_focus_certified"])
        self.assertIsNone(matrix["observed_win_rate"])
        self.assertIsNone(matrix["confidence_interval"])
        self.assertFalse(matrix["intercession_cost_accepted"])
        for t in matrix["trials"]:
            self.assertEqual(t["source_digests"].keys(),
                             {"medium","foe","ally"})
            self.assertEqual(t["metrics"]["paid_foe_attacks"],2)
            self.assertTrue(t["ledger_sha256"])

    def test_02_source_paid_melee_and_g4_g45_each_round(self):
        for source in OPPONENTS:
            for level in (1,2,3):
                with self.subTest(opponent=source,level=level):
                    r=run_policy(opponent=source,level=level,policy="guided",seed=7)
                    ledger=r["ledger"]
                    def items(kind):
                        return [x for x in ledger if x["kind"]==kind]
                    self.assertEqual(r["rounds_completed"],2)
                    self.assertEqual(r["source_ids"]["medium"],"M")
                    self.assertEqual(r["source_ids"]["ally"],"F")
                    self.assertEqual(r["source_ids"]["foe"],OPPONENTS[source][0])
                    self.assertEqual(len(items("g5_melee_resolved")),2)
                    self.assertEqual(len(items("g45_attested_hit")),2)
                    self.assertEqual(len(items("g4_damage_applied")),2)
                    self.assertEqual(len(items("g5_melee_sequence_attested")),2)
                    self.assertEqual(len(items("regeneration_step")),6)
                    self.assertEqual(len(items("round_end")),2)
                    self.assertEqual(len(items("b05_consecration_applied")),1)
                    self.assertEqual(r["metrics"]["effect_establishments"],1)
                    self.assertEqual(r["ledger_sha256"],
                                     canonical_digest(ledger))
                    for hit in items("g45_attested_hit"):
                        self.assertEqual(hit["detail"]["attacker"],"foe")
                        self.assertEqual(hit["detail"]["target"],"ally")
                        self.assertEqual(hit["detail"]["target_source"],
                                         r["source_digests"]["ally"])
                        self.assertIsNone(hit["detail"]["medium_intercessor"])
                    self.assertFalse(r["full_encounter_certified"])
                    self.assertIsNone(r["sampled_win_rate"])
                    self.assertIsNone(r["policy_weighting"])

    def test_03_soldier_guided_restores_hp_shelter_does_not_prevent_hp(self):
        guided=run_policy(opponent="soldier",level=1,policy="guided")
        shelter=run_policy(opponent="soldier",level=1,policy="shelter")
        bare=run_policy(opponent="soldier",level=1,policy="no_magic")
        g,s,b=(x["metrics"] for x in (guided,shelter,bare))
        self.assertGreater(g["ally_hp"],s["ally_hp"])
        self.assertEqual(s["ally_hp"],b["ally_hp"])
        self.assertEqual(s["direct_vigor_prevented"],0)
        self.assertEqual(b["direct_vigor_prevented"],0)
        self.assertGreater(g["ally_hp_regenerated"],s["ally_hp_regenerated"])
        self.assertEqual(g["priest_vp"],[2,2,0])
        self.assertEqual(s["priest_vp"],[1,2,1])

    def test_04_sentry_guided_hp_vs_shelter_vigor_tradeoff(self):
        for level in (1,2,3):
            with self.subTest(level=level):
                guided=run_policy(opponent="sentry_prepared",level=level,
                                  policy="guided")["metrics"]
                shelter=run_policy(opponent="sentry_prepared",level=level,
                                   policy="shelter")["metrics"]
                bare=run_policy(opponent="sentry_prepared",level=level,
                                policy="no_magic")["metrics"]
                self.assertGreaterEqual(guided["ally_hp"],shelter["ally_hp"])
                self.assertGreater(shelter["ally_vigor"],guided["ally_vigor"])
                self.assertEqual(shelter["direct_vigor_prevented"],4)
                self.assertEqual(guided["direct_vigor_prevented"],0)
                self.assertEqual(bare["direct_vigor_prevented"],0)
                self.assertEqual(shelter["intercession_reactions"],0)
                self.assertEqual(shelter["effect_establishments"],1)

    def test_05_medium_native_basic_heal_source_paid_no_free_talent(self):
        for level in (1,2,3):
            with self.subTest(level=level):
                basic=run_policy(opponent="sentry_prepared",level=level,
                                 policy="basic_heal")
                b=basic["metrics"]
                self.assertGreater(b["basic_heal_hp"],0)
                self.assertGreater(b["basic_heal_vigor"],0)
                self.assertEqual(b["ap_committed_by_priest"],24)
                self.assertEqual(b["priest_vp"],[4*level-2,0,2])
                self.assertEqual(b["effect_establishments"],0)
                heals=[x for x in basic["ledger"]
                       if x["kind"]=="g4_basic_heal_applied"]
                self.assertEqual(len(heals),1)
                self.assertEqual(heals[0]["detail"]["source"],"g4:paid_primary")
                self.assertEqual(heals[0]["detail"]["recipient"],"ally")
                self.assertEqual(b["paid_foe_attacks"],2)

    def test_06_guided_intercession_from_self_on_genuine_ally_steps(self):
        for opponent in OPPONENTS:
            normal=run_policy(opponent=opponent,level=3,policy="guided")
            rescue=run_policy(opponent=opponent,level=3,
                              policy="guided_intercession")
            g,n=normal["metrics"],rescue["metrics"]
            self.assertEqual((n["ally_hp"],n["ally_vigor"]),
                             (g["ally_hp"],g["ally_vigor"]))
            self.assertEqual(n["intercession_reactions"],2)
            self.assertEqual(g["intercession_reactions"],0)
            self.assertEqual(n["priest_vp"],[6,2,4])
            self.assertEqual(g["priest_vp"],[10,2,0])
            armed=[x for x in rescue["ledger"]
                   if x["kind"]=="b05_guided_intercession_armed"]
            self.assertEqual(len(armed),2)
            self.assertEqual(len([x for x in rescue["ledger"]
                                  if x["kind"]=="b05_guided_intercession_finished"]),2)

    def test_07_shelter_intercession_from_self_uses_native_sentry_packets(self):
        protected=run_policy(opponent="sentry_prepared",level=3,
                             policy="shelter")["metrics"]
        rescue=run_policy(opponent="sentry_prepared",level=3,
                          policy="shelter_intercession")
        m=rescue["metrics"]
        self.assertEqual((m["ally_hp"],m["ally_vigor"]),
                         (protected["ally_hp"],protected["ally_vigor"]))
        self.assertEqual(m["direct_vigor_prevented"],4)
        self.assertEqual(m["intercession_reactions"],2)
        self.assertEqual(m["priest_vp"],[5,2,5])
        self.assertEqual(protected["priest_vp"],[9,2,1])
        self.assertEqual(len([x for x in rescue["ledger"]
                              if x["kind"]=="b05_vital_intercession_packet"]),2)
        hits=[x["detail"] for x in rescue["ledger"]
              if x["kind"]=="g45_attested_hit"]
        self.assertEqual(len(hits),2)
        self.assertTrue(all(x["medium_intercessor"]=="medium" for x in hits))
        self.assertEqual(len([x for x in rescue["ledger"]
                              if x["kind"]=="g5_melee_resolved"]),2)

    def test_08_report_tampering_fails_closed_even_after_rehash(self):
        original=run_policy(opponent="sentry_prepared",level=3,
                            policy="shelter_intercession",seed=11)
        self.assertEqual(attest_policy(
            original,opponent="sentry_prepared",level=3,
            policy="shelter_intercession",seed=11),original)
        fake=deepcopy(original)
        fake["metrics"]["direct_vigor_prevented"]=100
        with self.assertRaises(AssertionError):
            attest_policy(fake,opponent="sentry_prepared",level=3,
                          policy="shelter_intercession",seed=11)
        fake=deepcopy(original)
        entry=next(x for x in fake["ledger"]
                   if x["kind"]=="b05_vital_intercession_packet")
        entry["detail"]["prevented"]=999
        fake["ledger_sha256"]=canonical_digest(fake["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(fake,opponent="sentry_prepared",level=3,
                          policy="shelter_intercession",seed=11)
        with self.assertRaises(AssertionError):
            attest_policy(original,opponent="sentry_prepared",level=3,
                          policy="shelter_intercession",seed=12)

    def test_09_missing_native_vigor_source_rejected_pre_roll(self):
        combat,adapter=_scene("soldier",3,"shelter",0)
        e=combat.e
        _start(combat,adapter,"shelter","medium")
        adapter.cast("medium","Vital Shelter","medium")
        combat.bridge.end_current_turn()
        _start(combat,adapter,"shelter","foe")
        seq=combat.declare("foe","ally",profiles=("B06-AT-03",),
                           defenses=("take_hit",))
        before=e.actors["medium"].vp_available
        with self.assertRaisesRegex(UnresolvedDecision,"native Vigor damage"):
            combat.resolve(seq,0,attack_face=12,damage_face=1,
                           medium_intercessor="medium")
        self.assertEqual(e.actors["medium"].vp_available,before)
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="g5_melee_roll"]),0)
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="g4_damage_applied"]),0)

    def test_10_invalid_policy_and_seed_fail_closed(self):
        for args in (
            dict(opponent="hunter",level=3,policy="guided"),
            dict(opponent="soldier",level=0,policy="guided"),
            dict(opponent="soldier",level=3,policy="intrusion"),
            dict(opponent="soldier",level=2,policy="guided_intercession"),
            dict(opponent="soldier",level=3,policy="shelter_intercession"),
            dict(opponent="soldier",level=3,policy="guided",seed=-1),
        ):
            with self.subTest(args=args),self.assertRaises(ValueError):
                run_policy(**args)
        a=run_policy(opponent="soldier",level=2,policy="no_magic",seed=5)
        b=run_policy(opponent="soldier",level=2,policy="no_magic",seed=5)
        self.assertEqual(a,b)


if __name__=="__main__":
    unittest.main()
