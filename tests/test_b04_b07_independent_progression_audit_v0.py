"""Independent cross-source B04/B07 progression and deliberately bounded status."""
import unittest
from copy import deepcopy

from scripts.b04_b07_independent_progression_audit_v0 import (
    audit, _sheet_issues, talent_minimums, validate_pilot_milestones,
)


class IndependentProgressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = audit()

    def test_01_all_twelve_pairings_and_thirty_nine_source_snapshots(self):
        report = self.report
        self.assertEqual((12, 13, 39),
                         (report["pairings_checked"], report["variants_checked"],
                          report["level_snapshots_checked"]))
        self.assertEqual({"High", "Medium", "Low"}, {p.split("/")[1]
                         for p in report["pairings"]})
        self.assertEqual({"Priest", "Scholar", "Gifted", "Anointed"},
                         {p.split("/")[0] for p in report["pairings"]})
        self.assertTrue(all(len(x["source_sha256"]) == 64
                            for x in report["pairings"].values()))

    def test_02_report_real_talent_gaps_not_false_full_certificates(self):
        issues={(x["pairing"], x["level"], x["code"])
                for x in self.report["issues"]}
        self.assertIn(("Priest/High", 3, "talent_overaward"), issues)
        self.assertIn(("Scholar/Low", 2, "talent_unaccounted"), issues)
        self.assertIn(("Scholar/Low", 3, "talent_unaccounted"), issues)
        self.assertIn(("Gifted/Medium", 3, "talent_unaccounted"), issues)
        self.assertEqual((0,0),(
            self.report["independently_certified_full_focuses"],
            self.report["strict_mvp_exits_met"]))
        self.assertFalse(any(p["full_focus_certified"]
                             for p in self.report["pairings"].values()))

    def test_03_independent_calculation_fails_tampered_legal_sheet(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile
        gates=talent_minimums()
        base=profile(1)
        good=profile(2)
        self.assertFalse(_sheet_issues("Anointed/High",2,good,base,base,gates))
        forged=deepcopy(good)
        forged["vp_max"]+=6
        forged["learned_disciplines"]["Medicine"]+=1
        forged["universals"]=("Veil Inspection","Blink")
        forged["talents"].append("TAL-C07 Reactive Aim")
        found={x["code"] for x in _sheet_issues(
            "Anointed/High",2,forged,base,base,gates)}
        self.assertTrue({"vp_formula","learned_budget","universal_award",
                         "talent_overaward","talent_gate"} <= found)

    def test_04_award_chronology_requires_two_distinct_gm_events(self):
        good=[
            {"event_id":"bridge", "character_id":"pilot-1",
             "kind":"adventure_milestone","gm_declared":True,
             "from_level":1,"to_level":2,"automatic":False},
            {"event_id":"village", "character_id":"pilot-1",
             "kind":"adventure_milestone","gm_declared":True,
             "from_level":2,"to_level":3,"automatic":False}]
        proof=validate_pilot_milestones("pilot-1",good)
        self.assertEqual((3,2,False),
                         (proof["level"],proof["unique_milestones"],
                          proof["resources_refreshed"]))
        for i, changes in enumerate((
            {1:{"event_id":"bridge"}},
            {1:{"from_level":1}},
            {1:{"to_level":4}},
            {1:{"gm_declared":False}},
            {1:{"kind":"personal_destiny_event"}},
            {1:{"xp":500}},
            {1:{"automatic":True}},
            {1:{"vp_refill":True}},
            {1:{"character_id":"other"}})):
            with self.subTest(case=i):
                wrong=deepcopy(good)
                wrong[1].update(changes[1])
                with self.assertRaises(ValueError):
                    validate_pilot_milestones("pilot-1",wrong)
        with self.assertRaises(ValueError):
            validate_pilot_milestones("pilot-1",good[:1])

    def test_05_low_priest_a_b_are_one_pairing_and_two_distinct_proxies(self):
        record=self.report["pairings"]["Priest/Low"]
        self.assertEqual((2,3),(record["variants"],record["levels_checked"]))
        self.assertIn("physical A/B proxy",record["boundary"])
        self.assertEqual([],record["issues"])
        self.assertEqual(64,len(record["build_record_sha256"]))


if __name__ == "__main__":
    unittest.main()
