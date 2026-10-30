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

    def test_06_focus_ap_prices_reject_self_consistent_forged_tempos(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as high
        from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile as medium
        from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile as low
        gates = talent_minimums()
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    genuine = make(level)
                    baseline = {x["code"] for x in _sheet_issues(
                        "Anointed/"+focus, level, genuine, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertFalse({"focus_action_cost", "general_action_cost",
                                      "physical_tempo", "projection_tempo"} & baseline)
                    forged = deepcopy(genuine)
                    forged["physical_action_ap"] = forged["projection_action_ap"] = 1
                    forged["general_action_ap"] = 1
                    forged["physical_tempo"] = forged["projection_tempo"] = forged["turn_ap"]
                    detected = {x["code"] for x in _sheet_issues(
                        "Anointed/"+focus, level, forged, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertTrue({"focus_action_cost", "general_action_cost",
                                     "physical_tempo", "projection_tempo"} <= detected)

    def test_07_scholar_known_capacity_rejects_coupled_source_inflation(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high
        from scripts.b05_medium_scholar_l1_l3_v0 import profile as medium
        from scripts.b05_low_scholar_l1_l3_v0 import profile as low
        gates = talent_minimums()
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    original = make(level)
                    forged = deepcopy(original)
                    forged["known_pillar_techniques"] = list(forged["known_pillar_techniques"])
                    forged["known_pillar_techniques"].append("Guided Regeneration" if
                        "Guided Regeneration" not in forged["known_pillar_techniques"]
                        else "Phantom Sound")
                    forged["known_capacity"] += 1
                    found = {x["code"] for x in _sheet_issues(
                        "Scholar/"+focus, level, forged, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertIn("scholar_known_capacity", found)

    def test_08_derived_prepared_and_formula_caps_reject_coupled_changes(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high
        from scripts.b05_low_scholar_l1_l3_v0 import profile as low
        from scripts.b05_high_priest_life_l1_l3_v0 import profile as priest_high
        from scripts.b05_medium_priest_life_l1_l3_v0 import profile as priest_medium
        gates = talent_minimums()
        for level in (1, 2):
            forged = high(level)
            forged["prepared_composite_formulas"].append(
                dict(forged["prepared_composite_formulas"][0], mode="invented"))
            forged["prepared_formula_capacity"] += 1
            codes = {x["code"] for x in _sheet_issues(
                "Scholar/High", level, forged, high(1),
                high(level-1) if level > 1 else None, gates)}
            self.assertIn("scholar_formula_capacity", codes)
        for level in (1, 2, 3):
            with self.subTest(level=level):
                forged = low(level)
                forged["prepared_techniques"] = list(forged["prepared_techniques"])
                forged["prepared_techniques"].append(
                    "Conjure Flame" if level == 1 else "Basic Heal")
                forged["prepared_capacity"] += 1
                codes = {x["code"] for x in _sheet_issues(
                    "Scholar/Low", level, forged, low(1),
                    low(level-1) if level > 1 else None, gates)}
                self.assertIn("scholar_preparation_capacity", codes)
        for focus, make in (("High", priest_high), ("Medium", priest_medium)):
            for level in (1, 2, 3):
                with self.subTest(priest=focus, level=level):
                    forged = make(level)
                    forged["prepared_prayers"] = list(forged["prepared_prayers"])
                    forged["prepared_prayers"].append("Bonus unearned prayer")
                    forged["prepared_capacity"] += 1
                    codes = {x["code"] for x in _sheet_issues(
                        "Priest/"+focus, level, forged, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertIn("priest_capacity", codes)

    def test_09_legitimately_earned_repertoire_talents_adjust_only_own_caps(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as scholar
        from scripts.b05_high_priest_life_l1_l3_v0 import profile as priest
        gates = talent_minimums()
        expanded = scholar(1)
        expanded["talents"] = ["TAL-S01 Expanded Repertoire"]
        expanded["known_pillar_techniques"].append("Guided Regeneration")
        expanded["known_capacity"] += 1
        # Already known? Use a new distinct authored Technique for this source.
        self.assertEqual(6, len(set(expanded["known_pillar_techniques"])))
        found = {x["code"] for x in _sheet_issues(
            "Scholar/High", 1, expanded, scholar(1), None, gates)}
        self.assertNotIn("scholar_known_capacity", found)
        expanded["talents"].append("TAL-U01 Veil Insight")  # no earned second choice
        found = {x["code"] for x in _sheet_issues(
            "Scholar/High", 1, expanded, scholar(1), None, gates)}
        self.assertTrue({"talent_overaward","scholar_known_capacity"} <= found)
        liturgy = priest(1)
        liturgy["talents"] = ("TAL-P01 Expanded Liturgy",)
        liturgy["prepared_prayers"] = tuple(liturgy["prepared_prayers"]) + ("Venom Endurance",)
        liturgy["prepared_capacity"] += 1
        found = {x["code"] for x in _sheet_issues(
            "Priest/High", 1, liturgy, priest(1), None, gates)}
        self.assertNotIn("priest_capacity", found)
        liturgy["accord"] = 2
        liturgy["prepared_capacity"] += 1
        found = {x["code"] for x in _sheet_issues(
            "Priest/High", 1, liturgy, priest(1), None, gates)}
        self.assertIn("priest_accord_provenance", found)

    def test_10_high_l3_fluency_and_medium_preparation_cannot_mint_caps(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high
        from scripts.b05_medium_scholar_l1_l3_v0 import profile as medium
        gates=talent_minimums()
        high_forged=high(3)
        high_forged["prepared_formula_capacity"]=12
        high_forged["prepared_composite_formulas"].append({
            "primary":"Stone Skin","secondary":"Basic Heal",
            "profile":"Self","mode":"invented"})
        codes={x["code"] for x in _sheet_issues(
            "Scholar/High",3,high_forged,high(1),high(2),gates)}
        self.assertIn("scholar_formula_capacity",codes)
        medium_forged=medium(2)
        medium_forged["prepared_capacity"]=99
        medium_forged["prepared_technique_subset"]=("Stone Skin",)
        codes={x["code"] for x in _sheet_issues(
            "Scholar/Medium",2,medium_forged,medium(1),medium(1),gates)}
        self.assertIn("scholar_medium_preparation",codes)

    def test_11_no_new_capacity_or_focus_cost_findings_on_authored_builds(self):
        prohibited={"focus_action_cost", "general_action_cost",
                    "physical_tempo", "projection_tempo",
                    "scholar_known_capacity", "scholar_preparation_capacity",
                    "scholar_formula_capacity", "scholar_formula_legality",
                    "scholar_medium_preparation", "priest_capacity",
                    "priest_accord_provenance"}
        new=[(x["pairing"],x["level"],x["code"]) for x in self.report["issues"]
             if x["code"] in prohibited]
        self.assertEqual([],new)

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
