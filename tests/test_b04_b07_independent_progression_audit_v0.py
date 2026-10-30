"""Independent cross-source B04/B07 progression and deliberately bounded status."""
import unittest
from copy import deepcopy
from unittest.mock import patch

from scripts.b04_b07_independent_progression_audit_v0 import (
    audit, _sheet_issues, authored_priest_techniques,
    talent_minimums, talent_rules,
    validate_pilot_milestones,
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

    def test_12_catalogue_archetype_gates_are_source_derived(self):
        rules = talent_rules()
        self.assertEqual(32, len(rules))
        for prefix, expected in (
            ("TAL-P", "Priest"), ("TAL-S", "Scholar"),
            ("TAL-G", "Gifted"), ("TAL-A", "Anointed"),
        ):
            self.assertTrue(all(entry["archetypes"] == frozenset((expected,))
                                for name, entry in rules.items()
                                if name.startswith(prefix)))
        for name in ("TAL-C01", "TAL-M01", "TAL-U01"):
            self.assertEqual(frozenset(("Priest", "Scholar", "Gifted", "Anointed")),
                             rules[name]["archetypes"])

    def test_13_foreign_archetype_talent_is_rejected_at_valid_level(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as anointed
        from scripts.b05_high_priest_life_l1_l3_v0 import profile as priest
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as scholar
        from scripts.b05_high_gifted_l1_l3_v0 import profile as gifted
        gates = talent_minimums()
        for pairing, make, foreign in (
            ("Anointed/High", anointed, "TAL-P01 Expanded Liturgy"),
            ("Priest/High", priest, "TAL-G01 Emotional Poise"),
            ("Scholar/High", scholar, "TAL-A01 Imprint Recall"),
            ("Gifted/High", gifted, "TAL-S01 Expanded Repertoire"),
        ):
            with self.subTest(pairing=pairing, foreign=foreign):
                profile = make(1)
                profile["talents"] = [foreign]
                detected = {issue["code"] for issue in _sheet_issues(
                    pairing, 1, profile, make(1), None, gates)}
                self.assertIn("talent_archetype", detected)
                self.assertNotIn("talent_gate", detected)

    def test_14_malformed_l1_talent_preserves_audit_issue_registry(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        original = module.profile
        def malformed(level):
            sheet = original(level)
            if level == 1:
                sheet["talents"] = ["TAL-NOT-AN-ID"]
            return sheet
        with patch.object(module, "profile", side_effect=malformed):
            report = audit()
        observed = {(issue["pairing"], issue["level"], issue["code"])
                    for issue in report["issues"]}
        self.assertIn(("Anointed/High", 1, "talent_identity"), observed)
        self.assertIn(("Anointed/High", 2, "talent_retraining"), observed)
        self.assertEqual(39, report["level_snapshots_checked"])
        self.assertEqual(12, report["pairings_checked"])
        self.assertEqual(0, report["independently_certified_full_focuses"])

    def test_15_high_scholar_composite_requires_authored_pair_profile_and_mode(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile
        gates = talent_minimums()
        cases = (
            {"primary": "Conjure Flame", "secondary": "Phantom Sound",
             "profile": "Self", "delivery": "normal on-turn Projection",
             "mode": "illicit"},
            {"primary": "Basic Heal", "secondary": "Stone Skin",
             "profile": "Self", "delivery": "normal on-turn Projection",
             "mode": "Stone Skin maintained + Basic Heal instantaneous Secondary"},
            {"primary": "Stone Skin", "secondary": "Basic Heal",
             "profile": "Single Target"},
            {"primary": "Stone Skin", "secondary": "Basic Heal",
             "delivery": "reactive Projection"},
            {"primary": "Stone Skin", "secondary": "Basic Heal",
             "mode": "Stone Skin maintained + recurring Basic Heal Secondary"},
            {"primary": "Stone Skin", "secondary": "Phantom Sound",
             "profile": "Self"},
        )
        for level in (1, 2):
            original = profile(level)
            source_issues = {i["code"] for i in _sheet_issues(
                "Scholar/High", level, original, profile(1),
                profile(level-1) if level > 1 else None, gates)}
            self.assertNotIn("scholar_formula_legality", source_issues)
            for case in cases:
                with self.subTest(level=level, case=case):
                    forged = deepcopy(original)
                    forged["prepared_composite_formulas"][0].update(case)
                    problems = {i["code"] for i in _sheet_issues(
                        "Scholar/High", level, forged, profile(1),
                        profile(level-1) if level > 1 else None, gates)}
                    self.assertIn("scholar_formula_legality", problems)
            for malformed in (None, "Stone Skin", {"primary": "Stone Skin"}):
                with self.subTest(level=level, malformed=malformed):
                    forged = deepcopy(original)
                    forged["prepared_composite_formulas"][0] = malformed
                    problems = {i["code"] for i in _sheet_issues(
                        "Scholar/High", level, forged, profile(1),
                        profile(level-1) if level > 1 else None, gates)}
                    self.assertIn("scholar_formula_legality", problems)

    def test_16_saved_talents_reconcile_even_when_every_award_spent(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high
        from scripts.b05_low_scholar_l1_l3_v0 import profile as low
        gates = talent_minimums()
        genuine = high(1)
        self.assertNotIn("talent_unaccounted", {x["code"] for x in _sheet_issues(
            "Scholar/High", 1, genuine, genuine, None, gates)})
        for invalid in (99, 1, -1, True, 0.0, "0", None):
            with self.subTest(invalid=invalid):
                forged = deepcopy(genuine)
                forged["saved_talent_selections"] = invalid
                issues = {x["code"] for x in _sheet_issues(
                    "Scholar/High", 1, forged, genuine, None, gates)}
                self.assertIn("talent_unaccounted", issues)
        explicit_zero = deepcopy(genuine)
        explicit_zero["saved_talent_selections"] = 0
        issues = {x["code"] for x in _sheet_issues(
            "Scholar/High", 1, explicit_zero, genuine, None, gates)}
        self.assertNotIn("talent_unaccounted", issues)
        for level in (2, 3):
            with self.subTest(saved_low_scholar_level=level):
                original = low(level)
                # Existing authored snapshot omits this earned L2 award.
                issues = {x["code"] for x in _sheet_issues(
                    "Scholar/Low", level, original, low(1),
                    low(level-1), gates)}
                self.assertIn("talent_unaccounted", issues)
                original["saved_talent_selections"] = 1
                issues = {x["code"] for x in _sheet_issues(
                    "Scholar/Low", level, original, low(1),
                    low(level-1), gates)}
                self.assertNotIn("talent_unaccounted", issues)

    def test_17_priest_preparation_uses_canonical_life_catalogue(self):
        authored = authored_priest_techniques()
        self.assertEqual({"Basic Heal", "Guided Regeneration",
                          "Vital Shelter", "Woodland Rapport",
                          "Venom Endurance", "Gentle Growth"}, set(authored))
        self.assertEqual({"Life"}, {v["pillar"] for v in authored.values()})
        self.assertEqual({1}, {v["base_tier"] for v in authored.values()})
        self.assertEqual({"Restoration", "Preservation", "Nature"},
                         {v["aspect"] for v in authored.values()})
        self.assertTrue(all(v["source"].startswith("docs/rules/07-veil-magic/")
                            for v in authored.values()))

    def test_18_priest_rejects_out_of_pillar_and_invented_prepared_prayers(self):
        from scripts.b05_high_priest_life_l1_l3_v0 import profile as high
        from scripts.b05_medium_priest_life_l1_l3_v0 import profile as medium
        gates = talent_minimums()
        for focus, make in (("High", high), ("Medium", medium)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    original = make(level)
                    base = {x["code"] for x in _sheet_issues(
                        "Priest/" + focus, level, original, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertNotIn("priest_prepared_access", base)
                    self.assertNotIn("priest_pillar", base)
                    for foreign in ("Conjure Flame", "Phantom Sound",
                                    "Unpublished Life Miracle", "Veil Inspection"):
                        forged = deepcopy(original)
                        prayers = list(forged["prepared_prayers"])
                        prayers[0] = foreign
                        forged["prepared_prayers"] = tuple(prayers)
                        issues = {x["code"] for x in _sheet_issues(
                            "Priest/" + focus, level, forged, make(1),
                            make(level-1) if level > 1 else None, gates)}
                        self.assertIn("priest_prepared_access", issues)
                    forged = deepcopy(original)
                    forged["pillar"] = "Fire"
                    forged["prepared_prayers"] = ("Conjure Flame",) + tuple(
                        original["prepared_prayers"][1:])
                    issues = {x["code"] for x in _sheet_issues(
                        "Priest/" + focus, level, forged, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertTrue({"priest_pillar",
                                     "priest_prepared_access"} <= issues)

    def test_19_priest_preparation_enforces_base_tier_independent_of_sheet(self):
        from scripts.b05_medium_priest_life_l1_l3_v0 import profile
        gates = talent_minimums()
        original_catalogue = authored_priest_techniques()
        # Synthetic catalogue metadata exercises the tier gate without
        # claiming a real Tier-2-only Life technique has been authored.
        modified = deepcopy(original_catalogue)
        modified["Basic Heal"]["base_tier"] = 2
        with patch("scripts.b04_b07_independent_progression_audit_v0."
                   "authored_priest_techniques", return_value=modified):
            for level in (1, 2, 3):
                with self.subTest(level=level):
                    p = profile(level)
                    issues = {x["code"] for x in _sheet_issues(
                        "Priest/Medium", level, p, profile(1),
                        profile(level-1) if level > 1 else None, gates)}
                    self.assertEqual(level < 3,
                                     "priest_prepared_access" in issues)

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
