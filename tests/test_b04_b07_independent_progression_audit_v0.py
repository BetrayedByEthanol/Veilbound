"""Independent cross-source B04/B07 progression and deliberately bounded status."""
import unittest
from copy import deepcopy
from unittest.mock import patch

from scripts.b04_b07_independent_progression_audit_v0 import (
    audit, _sheet_issues, authored_priest_techniques,
    authored_scholar_techniques, anointed_signature_bonds,
    canonical_aspect_pairs, gifted_core_emotions, talent_minimums, talent_rules,
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
        # Medicine 2->3 is an invalid rank: do not sum it merely to
        # manufacture a learned-budget result after numeric preflight.
        self.assertTrue({"vp_formula","learned_ranks","learned_progression",
                         "universal_award","talent_overaward",
                         "talent_gate"} <= found)
        # A separately forged allocation with all legal numeric ranks still
        # proves over-budget learned points are rejected independently.
        overspent = deepcopy(good)
        overspent["learned_disciplines"]["Unawarded Training"] = 1
        overspent_found = {x["code"] for x in _sheet_issues(
            "Anointed/High", 2, overspent, base, base, gates)}
        self.assertIn("learned_budget", overspent_found)
        self.assertIn("learned_progression", overspent_found)
        self.assertNotIn("learned_ranks", overspent_found)

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
                    "anointed_technique_access",
                    "gifted_technique_access",
                    "scholar_known_access", "gifted_link_identity",
                    "scholar_knowledge_grant",
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

    def test_20_scholar_repertoire_uses_authored_pillar_techniques(self):
        rules = authored_scholar_techniques()
        self.assertEqual(13, len(rules))
        self.assertEqual({1}, {r["base_tier"] for r in rules.values()})
        self.assertTrue(all((r["pillar"], r["aspect"]) in
                            canonical_aspect_pairs() for r in rules.values()))
        for name in ("Blink", "Veil Inspection", "Phantom Image"):
            self.assertNotIn(name, rules)
        self.assertTrue({"Protective Ward", "Weaken Restraints",
                         "Spark of Inspiration", "Gentle Growth",
                         "Venom Endurance", "Woodland Rapport"} <= set(rules))

    def test_21_scholar_rejects_universal_unauthored_and_early_tier_techniques(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high
        from scripts.b05_medium_scholar_l1_l3_v0 import profile as medium
        from scripts.b05_low_scholar_l1_l3_v0 import profile as low
        gates = talent_minimums()
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    original = make(level)
                    baseline = {x["code"] for x in _sheet_issues(
                        "Scholar/"+focus, level, original, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertNotIn("scholar_known_access", baseline)
                    for bad in ("Blink", "Veil Inspection",
                                "Phantom Image", "Unauthored Tier-1 Spell"):
                        forged = deepcopy(original)
                        known = list(forged["known_pillar_techniques"])
                        known[0] = bad
                        forged["known_pillar_techniques"] = known
                        errors = {x["code"] for x in _sheet_issues(
                            "Scholar/"+focus, level, forged, make(1),
                            make(level-1) if level > 1 else None, gates)}
                        self.assertIn("scholar_known_access", errors)
        legal = high(1)
        legal["known_pillar_techniques"][0] = "Spark of Inspiration"
        codes = {x["code"] for x in _sheet_issues(
            "Scholar/High", 1, legal, high(1), None, gates)}
        self.assertNotIn("scholar_known_access", codes)
        # No Tier-2-only technique exists in this bounded source census.
        # Simulate future authored metadata to prove L1-2 reject before L3.
        canonical = authored_scholar_techniques()
        modified = deepcopy(canonical)
        modified["Stone Skin"]["base_tier"] = 2
        with patch("scripts.b04_b07_independent_progression_audit_v0."
                   "authored_scholar_techniques", return_value=modified):
            for level in (1, 2, 3):
                p = high(level)
                codes = {x["code"] for x in _sheet_issues(
                    "Scholar/High", level, p, high(1),
                    high(level-1) if level > 1 else None, gates)}
                self.assertEqual(level < 3, "scholar_known_access" in codes)

    def test_22_gifted_links_require_distinct_valid_canonical_pillars_and_aspects(self):
        from scripts.b05_high_gifted_l1_l3_v0 import profile as high
        from scripts.b05_medium_gifted_l1_l3_v0 import profile as medium
        from scripts.b05_low_gifted_l1_l3_v0 import profile as low
        gates = talent_minimums()
        self.assertEqual(48, len(canonical_aspect_pairs()))
        self.assertEqual({"Joy", "Sadness", "Anger", "Fear", "Surprise",
                          "Disgust", "Trust", "Anticipation"}, gifted_core_emotions())
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    original = make(level)
                    baseline = {x["code"] for x in _sheet_issues(
                        "Gifted/"+focus, level, original, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertNotIn("gifted_link_identity", baseline)
                    for kind in ("duplicate", "mismatched", "invented",
                                 "missing_emotion", "foreign_emotion"):
                        forged = deepcopy(original)
                        links = forged["emotion_aspect_links"]
                        if kind == "duplicate":
                            links["Joy"] = deepcopy(links["Fear"])
                        elif kind == "mismatched":
                            links["Joy"]["pillar"] = "Earth"  # wrong Fire Aspect
                        elif kind == "invented":
                            links["Joy"]["aspect"] = "Never-Authored Aspect"
                        elif kind == "missing_emotion":
                            links["Extra"] = links.pop("Joy")
                        else:
                            links["Anger"] = links.pop("Joy")  # loses Joy
                        errors = {x["code"] for x in _sheet_issues(
                            "Gifted/"+focus, level, forged, make(1),
                            make(level-1) if level > 1 else None, gates)}
                        self.assertTrue({"gifted_links"} <= errors if kind in
                                        ("missing_emotion", "foreign_emotion") else
                                        {"gifted_link_identity"} <= errors)

    def test_23_gifted_bad_birth_links_fail_even_if_persisted_at_all_levels(self):
        from scripts import b05_high_gifted_l1_l3_v0 as module
        original = module.profile

        def forged_at_creation_and_carried(level):
            sheet = original(level)
            sheet["emotion_aspect_links"]["Joy"] = deepcopy(
                sheet["emotion_aspect_links"]["Fear"])
            return sheet

        with patch.object(module, "profile",
                          side_effect=forged_at_creation_and_carried):
            report = audit()
        issues = {(x["pairing"], x["level"], x["code"])
                  for x in report["issues"]}
        self.assertTrue({("Gifted/High", level, "gifted_link_identity")
                         for level in (1, 2, 3)} <= issues)
        self.assertNotIn(("Gifted/High", 2, "gifted_link_mutation"), issues)
        self.assertNotIn(("Gifted/High", 3, "gifted_link_mutation"), issues)

    def test_24_anointed_signature_is_tied_to_authored_initial_bond(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as high
        from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile as medium
        from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile as low
        gates = talent_minimums()
        self.assertEqual({
            "Returning Step": {"pillar": "Life", "aspect": "Restoration"},
            "Kindled Flame": {"pillar": "Fire", "aspect": "Conflagration"},
        }, anointed_signature_bonds())
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    original = make(level)
                    baseline = {x["code"] for x in _sheet_issues(
                        "Anointed/"+focus, level, original, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertNotIn("anointed_bond", baseline)
                    for forged_bond in (
                        {"pillar": "Fire", "aspect": "Conflagration"},
                        {"pillar": "Life", "aspect": "Preservation"},
                        {"pillar": "Life", "aspect": "Invented"},
                        {"pillar": "Life", "aspect": "Restoration", "extra": 1},
                        None,
                    ):
                        forged = deepcopy(original)
                        forged["bond"] = forged_bond
                        findings = {x["code"] for x in _sheet_issues(
                            "Anointed/"+focus, level, forged, make(1),
                            make(level-1) if level > 1 else None, gates)}
                        self.assertIn("anointed_bond", findings)

    def test_25_consistently_wrong_anointed_bond_is_found_across_full_audit(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        original = module.profile
        def bad_bond(level):
            sheet = original(level)
            sheet["bond"] = {"pillar": "Fire", "aspect": "Conflagration"}
            return sheet
        with patch.object(module, "profile", side_effect=bad_bond):
            report = audit()
        issues = {(x["pairing"], x["level"], x["code"])
                  for x in report["issues"]}
        self.assertTrue({("Anointed/High", n, "anointed_bond")
                         for n in (1, 2, 3)} <= issues)
        self.assertNotIn(("Anointed/High", 2, "anointed_bond_mutation"), issues)
        self.assertNotIn(("Anointed/High", 3, "anointed_bond_mutation"), issues)
        self.assertEqual(39, report["level_snapshots_checked"])

    def test_26_malformed_learned_ranks_never_abort_multi_focus_audit(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        original = module.profile
        gates = talent_minimums()
        for invalid in ("2", None, 2.0, True, -1, 3):
            with self.subTest(invalid=invalid):
                forged = original(1)
                forged["learned_disciplines"]["Medicine"] = invalid
                issues = {x["code"] for x in _sheet_issues(
                    "Anointed/High", 1, forged, forged, None, gates)}
                self.assertIn("learned_ranks", issues)
        # L1 malformed but L2 otherwise valid: reject the transition and
        # preserve the full report rather than attempting invalid subtraction.
        def malformed_first(level):
            sheet = original(level)
            if level == 1:
                sheet["learned_disciplines"]["Medicine"] = "2"
            return sheet
        with patch.object(module, "profile", side_effect=malformed_first):
            report = audit()
        issues = {(x["pairing"], x["level"], x["code"])
                  for x in report["issues"]}
        self.assertIn(("Anointed/High", 1, "learned_ranks"), issues)
        self.assertIn(("Anointed/High", 2, "learned_progression"), issues)
        self.assertEqual(12, report["pairings_checked"])
        self.assertEqual(39, report["level_snapshots_checked"])
        self.assertEqual(0, report["independently_certified_full_focuses"])

    def test_27_gifted_techniques_match_each_emotion_aspect_and_tier(self):
        from scripts.b05_high_gifted_l1_l3_v0 import profile as high
        from scripts.b05_medium_gifted_l1_l3_v0 import profile as medium
        from scripts.b05_low_gifted_l1_l3_v0 import profile as low
        gates = talent_minimums()
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    genuine = make(level)
                    original = {issue["code"] for issue in _sheet_issues(
                        "Gifted/"+focus, level, genuine, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertNotIn("gifted_technique_access", original)
                    for emotion, name in (
                        ("Fear", "Conjure Flame"),  # Earth -> Fire
                        ("Joy", "Stone Skin"),      # Fire -> Earth
                        ("Sadness", "Venom Endurance"),  # Life, wrong Aspect
                        ("Trust", "Blink"),          # Universal procedure
                        ("Surprise", "Phantom Image"),  # unauthored
                        ("Joy", "Unknown Magic"),    # invented
                    ):
                        tampered = deepcopy(genuine)
                        tampered["authored_linked_techniques"][emotion] = [name]
                        findings = {issue["code"] for issue in _sheet_issues(
                            "Gifted/"+focus, level, tampered, make(1),
                            make(level-1) if level > 1 else None, gates)}
                        self.assertIn("gifted_technique_access", findings)
                    invalid_shape = deepcopy(genuine)
                    invalid_shape["authored_linked_techniques"]["Fear"] = "Stone Skin"
                    findings = {issue["code"] for issue in _sheet_issues(
                        "Gifted/"+focus, level, invalid_shape, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertIn("gifted_links", findings)
                    self.assertIn("gifted_technique_access", findings)
                    duplicate = deepcopy(genuine)
                    duplicate["authored_linked_techniques"]["Fear"] = [
                        "Stone Skin", "Stone Skin"]
                    findings = {issue["code"] for issue in _sheet_issues(
                        "Gifted/"+focus, level, duplicate, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertIn("gifted_technique_access", findings)
        # A legitimately authored T2-only entry is unavailable until L3.
        authored = authored_scholar_techniques()
        future = deepcopy(authored)
        future["Stone Skin"]["base_tier"] = 2
        with patch("scripts.b04_b07_independent_progression_audit_v0."
                   "authored_scholar_techniques", return_value=future):
            for level in (1, 2, 3):
                with self.subTest(level=level, base_tier=2):
                    profile = high(level)
                    codes = {i["code"] for i in _sheet_issues(
                        "Gifted/High", level, profile, high(1),
                        high(level-1) if level > 1 else None, gates)}
                    self.assertEqual(level < 3, "gifted_technique_access" in codes)

    def test_28_out_of_aspect_technique_carried_through_levels_is_detected(self):
        from scripts import b05_high_gifted_l1_l3_v0 as module
        original = module.profile
        def forged(level):
            sheet = original(level)
            sheet["authored_linked_techniques"]["Fear"] = ["Conjure Flame"]
            return sheet
        with patch.object(module, "profile", side_effect=forged):
            report = audit()
        issues = {(x["pairing"], x["level"], x["code"])
                  for x in report["issues"]}
        self.assertTrue({("Gifted/High", n, "gifted_technique_access")
                         for n in (1, 2, 3)} <= issues)
        self.assertEqual(39, report["level_snapshots_checked"])
        self.assertEqual(12, report["pairings_checked"])

    def test_29_invalid_weapon_ranks_do_not_abort_the_audit(self):
        from scripts import b05_high_gifted_l1_l3_v0 as module
        original = module.profile
        gates = talent_minimums()
        for invalid in ("2", None, 2.0, True, -1, 3):
            with self.subTest(invalid=invalid):
                sheet = original(1)
                sheet["weapon_training"]["Small Blades"] = invalid
                findings = {i["code"] for i in _sheet_issues(
                    "Gifted/High", 1, sheet, sheet, None, gates)}
                self.assertIn("weapon_budget", findings)
        # A valid integer with the wrong total is still a budget violation.
        sheet = original(1)
        sheet["weapon_training"]["Small Blades"] = 1
        findings = {i["code"] for i in _sheet_issues(
            "Gifted/High", 1, sheet, sheet, None, gates)}
        self.assertIn("weapon_budget", findings)
        for changed_level in (1, 2):
            with self.subTest(changed_level=changed_level):
                def forged(level):
                    sheet = original(level)
                    if level == changed_level:
                        sheet["weapon_training"]["Small Blades"] = "2"
                    return sheet
                with patch.object(module, "profile", side_effect=forged):
                    report = audit()
                issues = {(x["pairing"], x["level"], x["code"])
                          for x in report["issues"]}
                self.assertIn(("Gifted/High", changed_level, "weapon_budget"),
                              issues)
                self.assertEqual(39, report["level_snapshots_checked"])
                self.assertEqual(12, report["pairings_checked"])

    def test_30_anointed_bonded_techniques_require_authored_matching_aspect(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as high
        from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile as medium
        from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile as low
        gates = talent_minimums()
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    original = make(level)
                    baseline = {i["code"] for i in _sheet_issues(
                        "Anointed/"+focus, level, original, make(1),
                        make(level-1) if level > 1 else None, gates)}
                    self.assertNotIn("anointed_technique_access", baseline)
                    for foreign in ("Conjure Flame", "Stone Skin",
                                    "Vital Shelter", "Blink",
                                    "Veil Inspection", "Unknown Technique"):
                        forged = deepcopy(original)
                        forged["known_bonded_techniques"] = [foreign]
                        findings = {i["code"] for i in _sheet_issues(
                            "Anointed/"+focus, level, forged, make(1),
                            make(level-1) if level > 1 else None, gates)}
                        self.assertIn("anointed_technique_access", findings)
                    for nonbonded in (["Stone Skin"], ["Conjure Flame"],
                                      ["Basic Heal"], None, "Stone Skin"):
                        forged = deepcopy(original)
                        forged["known_other_aspect_techniques"] = nonbonded
                        findings = {i["code"] for i in _sheet_issues(
                            "Anointed/"+focus, level, forged, make(1),
                            make(level-1) if level > 1 else None, gates)}
                        self.assertIn("anointed_technique_access", findings)
                    for bad in (["Basic Heal", "Basic Heal"],
                                "Basic Heal", [None], [42]):
                        forged = deepcopy(original)
                        forged["known_bonded_techniques"] = bad
                        findings = {i["code"] for i in _sheet_issues(
                            "Anointed/"+focus, level, forged, make(1),
                            make(level-1) if level > 1 else None, gates)}
                        self.assertIn("anointed_technique_access", findings)
        # Higher-base-tier technique can appear only at a legal tier.
        catalogue = authored_scholar_techniques()
        future = deepcopy(catalogue)
        future["Basic Heal"]["base_tier"] = 2
        with patch("scripts.b04_b07_independent_progression_audit_v0."
                   "authored_scholar_techniques", return_value=future):
            for level in (1, 2, 3):
                original = high(level)
                codes = {i["code"] for i in _sheet_issues(
                    "Anointed/High", level, original, high(1),
                    high(level-1) if level > 1 else None, gates)}
                self.assertEqual(level < 3, "anointed_technique_access" in codes)

    def test_31_anointed_out_of_aspect_list_persists_and_fails_full_audit(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        original = module.profile
        def forged(level):
            sheet = original(level)
            sheet["known_bonded_techniques"] = ["Conjure Flame"]
            sheet["known_other_aspect_techniques"] = ["Stone Skin"]
            return sheet
        with patch.object(module, "profile", side_effect=forged):
            report = audit()
        issues = {(x["pairing"], x["level"], x["code"])
                  for x in report["issues"]}
        self.assertTrue({("Anointed/High", n, "anointed_technique_access")
                         for n in (1, 2, 3)} <= issues)
        self.assertEqual(12, report["pairings_checked"])
        self.assertEqual(39, report["level_snapshots_checked"])
        self.assertEqual(0, report["independently_certified_full_focuses"])

    def test_32_malformed_equipment_prices_preserve_audit_register(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        original = module.profile
        gates = talent_minimums()
        for invalid in ("4", None, True, 4.0, -1):
            with self.subTest(invalid=invalid):
                sheet = original(1)
                sheet["equipment_sp"]["Dagger"] = invalid
                findings = {i["code"] for i in _sheet_issues(
                    "Anointed/High", 1, sheet, sheet, None, gates)}
                self.assertIn("equipment_budget", findings)
        # Valid integer but inconsistent sum/remainder is still rejected.
        sheet = original(1)
        sheet["equipment_sp"]["Dagger"] = 5
        findings = {i["code"] for i in _sheet_issues(
            "Anointed/High", 1, sheet, sheet, None, gates)}
        self.assertIn("equipment_budget", findings)
        for changed in (1, 2):
            with self.subTest(changed_level=changed):
                def forged(level):
                    sheet = original(level)
                    if level == changed:
                        sheet["equipment_sp"]["Dagger"] = "4"
                    return sheet
                with patch.object(module, "profile", side_effect=forged):
                    report = audit()
                found = {(x["pairing"], x["level"], x["code"])
                         for x in report["issues"]}
                self.assertIn(("Anointed/High", changed, "equipment_budget"), found)
                self.assertEqual(39, report["level_snapshots_checked"])
                self.assertEqual(12, report["pairings_checked"])

    def test_33_scholar_l3_cannot_claim_unused_l2_knowledge_grant(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high
        from scripts.b05_medium_scholar_l1_l3_v0 import profile as medium
        from scripts.b05_low_scholar_l1_l3_v0 import profile as low
        gates = talent_minimums()
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            with self.subTest(focus=focus):
                l1, l2, l3 = (make(n) for n in (1, 2, 3))
                l2["known_pillar_techniques"] = deepcopy(
                    l1["known_pillar_techniques"])
                # L2 leaves its newly awarded slot empty; this does not
                # itself mint a new L3 acquisition entitlement.
                l2_findings = {x["code"] for x in _sheet_issues(
                    "Scholar/"+focus, 2, l2, l1, l1, gates)}
                self.assertNotIn("scholar_knowledge_grant", l2_findings)
                # The L3 source still contains the genuine L2-added name.
                l3_findings = {x["code"] for x in _sheet_issues(
                    "Scholar/"+focus, 3, l3, l1, l2, gates)}
                self.assertIn("scholar_knowledge_grant", l3_findings)
                self.assertNotIn("scholar_known_capacity", l3_findings)

    def test_34_legally_new_talent_grants_one_not_retroactive_technique(self):
        from scripts.b05_medium_scholar_l1_l3_v0 import profile as medium
        from scripts.b05_low_scholar_l1_l3_v0 import profile as low
        gates = talent_minimums()
        for focus, make in (("Medium", medium), ("Low", low)):
            with self.subTest(focus=focus):
                l1, l2, l3 = (make(n) for n in (1, 2, 3))
                # Legitimate L3 TAL-S01 purchase authorizes one more
                # individual technique even though base L3 awards none.
                l3["talents"] = (l3["talents"][0],
                                 "TAL-S01 Expanded Repertoire")
                l3["known_pillar_techniques"] = tuple(
                    l3["known_pillar_techniques"]) + ("Phantom Sound",)
                l3["known_capacity"] += 1
                # Low has three earned Talent awards by L3 but this
                # published pilot leaves one selection explicitly unspent.
                # Account for it rather than granting a free third Talent.
                if focus == "Low":
                    l3["saved_talent_selections"] = 1
                findings = {x["code"] for x in _sheet_issues(
                    "Scholar/"+focus, 3, l3, l1, l2, gates)}
                self.assertNotIn("scholar_knowledge_grant", findings)
                self.assertNotIn("scholar_known_capacity", findings)
                self.assertNotIn("talent_gate", findings)
                self.assertNotIn("talent_unaccounted", findings)
                # The exact same Talent still owned at L3 cannot be used
                # to add a further late technique after it was acquired.
                prior = deepcopy(l2)
                prior["talents"] = ("TAL-S01 Expanded Repertoire",)
                prior["known_capacity"] += 1
                # This fabricated prior snapshot only tests the grant
                # comparison: it has a valid level-2 Talent allowance.
                findings = {x["code"] for x in _sheet_issues(
                    "Scholar/"+focus, 3, l3, l1, prior, gates)}
                self.assertIn("scholar_knowledge_grant", findings)

    def test_35_l2_one_grant_does_not_fill_multiple_empty_slots(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high
        gates = talent_minimums()
        l1, l2 = high(1), high(2)
        # Start with three known techniques and two empty L1 slots.
        l1["known_pillar_techniques"] = list(
            l1["known_pillar_techniques"])[:3]
        l2["known_pillar_techniques"] = list(
            l1["known_pillar_techniques"]) + ["Vital Shelter", "Phantom Sound"]
        self.assertEqual(5, len(l2["known_pillar_techniques"]))
        findings = {x["code"] for x in _sheet_issues(
            "Scholar/High", 2, l2, l1, l1, gates)}
        self.assertIn("scholar_knowledge_grant", findings)
        # Only one new actual technique is allowed by the L2 grant.
        l2["known_pillar_techniques"].pop()
        findings = {x["code"] for x in _sheet_issues(
            "Scholar/High", 2, l2, l1, l1, gates)}
        self.assertNotIn("scholar_knowledge_grant", findings)

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
