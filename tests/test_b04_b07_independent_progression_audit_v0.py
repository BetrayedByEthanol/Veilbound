"""Independent cross-source B04/B07 progression and deliberately bounded status."""
import unittest
from fnmatch import fnmatchcase
from pathlib import Path
import re
from copy import deepcopy
from unittest.mock import patch

from scripts.b04_b07_independent_progression_audit_v0 import (
    audit, _sheet_issues, authored_priest_techniques,
    SOURCE_MODULES, PRIEST_LIFE_RULE_SOURCES, SCHOLAR_RULE_SOURCES,
    CANONICAL_ASPECTS, GIFTED_FOUNDATION, ANOINTED_SIGNATURE_AUTHORITY,
    EQUIPMENT_CATALOGUE, WEAPON_TRAINING_CATALOGUE, CATALOGUE, LOW_RECORD,
    canonical_weapon_families, canonical_starter_item_prices,
    authored_scholar_techniques, anointed_signature_bonds,
    canonical_aspect_pairs, gifted_core_emotions, talent_minimums, talent_rules,
    utility_talent_requirements, _has_direct_utility_training,
    deep_volition_reserve_bonus,
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

    def test_02_reconciled_talent_ledgers_do_not_fake_certification(self):
        issues = {(x["pairing"], x["level"], x["code"])
                  for x in self.report["issues"]}
        for pairing, level, original_code in (
                ("Priest/High", 3, "talent_overaward"),
                ("Scholar/Low", 2, "talent_unaccounted"),
                ("Scholar/Low", 3, "talent_unaccounted"),
                ("Gifted/Medium", 3, "talent_unaccounted")):
            self.assertNotIn((pairing, level, original_code), issues)
        # Audit receipt closure is not a full-played Focus certificate.
        self.assertEqual((0, 0), (
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
                    "scholar_knowledge_grant", "talent_prerequisite",
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
                # After the source correction, the L2 award is genuinely
                # retained at both L2 and L3. The negative case must
                # deliberately erase that saved balance instead.
                issues = {x["code"] for x in _sheet_issues(
                    "Scholar/Low", level, original, low(1),
                    low(level-1), gates)}
                self.assertNotIn("talent_unaccounted", issues)
                original["saved_talent_selections"] = 0
                issues = {x["code"] for x in _sheet_issues(
                    "Scholar/Low", level, original, low(1),
                    low(level-1), gates)}
                self.assertIn("talent_unaccounted", issues)

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
                    # L2 already earned two awards; only one was spent.
                    # A legitimate deferred L3 purchase must be backed
                    # by that saved L2 selection, not just the L3 ledger.
                    l2["saved_talent_selections"] = 1
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

    def test_36_full_audit_rejects_delayed_medium_scholar_acquisition(self):
        from scripts import b05_medium_scholar_l1_l3_v0 as module
        original = module.profile

        def with_unfilled_l2_slot(level):
            result = original(level)
            if level == 2:
                result["known_pillar_techniques"] = (
                    original(1)["known_pillar_techniques"])
            return result

        with patch.object(module, "profile",
                          side_effect=with_unfilled_l2_slot):
            report = audit()
        issues = {(x["pairing"], x["level"], x["code"])
                  for x in report["issues"]}
        self.assertIn(("Scholar/Medium", 3, "scholar_knowledge_grant"), issues)
        self.assertNotIn(("Scholar/Medium", 2, "scholar_knowledge_grant"), issues)
        self.assertNotIn(("Scholar/Medium", 3, "scholar_known_capacity"), issues)
        self.assertEqual((12, 39),
                         (report["pairings_checked"],
                          report["level_snapshots_checked"]))
        self.assertEqual(0, report["independently_certified_full_focuses"])

    def test_37_saved_high_scholar_award_grants_later_knowledge(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile
        gates = talent_minimums()
        for acquired_at in (2, 3):
            with self.subTest(acquired_at=acquired_at):
                sheets = [profile(n) for n in (1, 2, 3)]
                # Save High's only L1 Talent instead of spending it.
                sheets[0]["talents"] = []
                sheets[0]["saved_talent_selections"] = 1
                sheets[1]["talents"] = []
                sheets[1]["saved_talent_selections"] = 1
                bought = sheets[acquired_at-1]
                bought["talents"] = ["TAL-S01 Expanded Repertoire"]
                bought["saved_talent_selections"] = 0
                bought["known_pillar_techniques"].append("Guided Regeneration")
                bought["known_capacity"] += 1
                if acquired_at == 2:
                    sheets[2]["talents"] = list(bought["talents"])
                    sheets[2]["known_pillar_techniques"].append("Guided Regeneration")
                    sheets[2]["known_capacity"] += 1
                for i, sheet in enumerate(sheets):
                    codes = {issue["code"] for issue in _sheet_issues(
                        "Scholar/High", i+1, sheet, sheets[0],
                        sheets[i-1] if i else None, gates)}
                    for code in ("scholar_knowledge_grant",
                                 "scholar_known_capacity",
                                 "talent_unaccounted", "talent_retraining"):
                        self.assertNotIn(code, codes)

    def test_38_spent_or_fake_saved_selection_does_not_mint_knowledge(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile
        gates = talent_minimums()
        original = profile(1)
        forged = profile(2)
        forged["talents"] = ["TAL-S01 Expanded Repertoire"]
        forged["known_capacity"] += 1
        forged["known_pillar_techniques"].append("Guided Regeneration")
        # L1 was already spent on Veil Insight, not saved.
        findings = {issue["code"] for issue in _sheet_issues(
            "Scholar/High", 2, forged, original, original, gates)}
        self.assertIn("scholar_knowledge_grant", findings)
        self.assertIn("talent_retraining", findings)
        # Falsely claim the saved L1 award was zero despite 0 selected.
        fake = deepcopy(original)
        fake["talents"] = []
        fake["saved_talent_selections"] = 0
        findings = {issue["code"] for issue in _sheet_issues(
            "Scholar/High", 2, forged, fake, fake, gates)}
        self.assertIn("scholar_knowledge_grant", findings)

    def test_39_utility_talents_require_direct_investment(self):
        from scripts.b05_high_scholar_fire_l1_l3_v0 import profile
        gates = talent_minimums()
        rules = utility_talent_requirements()
        self.assertEqual(set(rules), {"TAL-U01", "TAL-U02", "TAL-U03",
                                      "TAL-U04", "TAL-U05"})
        choices = {
            "TAL-U01": ("Veil Theory", "Pillar Lore (Life)"),
            "TAL-U02": ("Smithing", "Engineering", "Trade (Glassblowing)"),
            "TAL-U03": ("Medicine",),
            "TAL-U04": ("Navigation", "Tracking"),
        }
        for talent_id, disciplines in choices.items():
            for discipline in disciplines:
                with self.subTest(talent=talent_id, discipline=discipline):
                    sheet = profile(1)
                    sheet["talents"] = [talent_id+" candidate"]
                    sheet["learned_disciplines"] = {
                        discipline: 1, "Other": 2, "Culture": 2,
                        "Fieldcraft": 2, "Background": 1,
                    }
                    self.assertEqual(8, sum(sheet["learned_disciplines"].values()))
                    codes = {issue["code"] for issue in _sheet_issues(
                        "Scholar/High", 1, sheet, sheet, None, gates)}
                    self.assertNotIn("talent_prerequisite", codes)
            with self.subTest(talent=talent_id, missing=True):
                sheet = profile(1)
                sheet["talents"] = [talent_id+" candidate"]
                sheet["learned_disciplines"] = {
                    "Veil Theory": 0, "Pillar Lore (Life)": 0,
                    "Smithing": 0, "Trade (Glassblowing)": 0,
                    "Medicine": 0, "Navigation": 0, "Tracking": 0,
                    "Other": 2, "Culture": 2, "Fieldcraft": 2,
                    "Background": 2,
                }
                codes = {issue["code"] for issue in _sheet_issues(
                    "Scholar/High", 1, sheet, sheet, None, gates)}
                self.assertIn("talent_prerequisite", codes)
        self.assertTrue(_has_direct_utility_training({"Medicine": 2}, *rules["TAL-U05"]))
        for invalid in ({"Medicine": 1}, {"Medicine": "2"},
                        {"Medicine": True}, {"Medicine": None}):
            self.assertFalse(_has_direct_utility_training(invalid, *rules["TAL-U05"]))

    def test_40_ineligible_route_familiarity_fails_full_audit(self):
        from scripts import b05_high_scholar_fire_l1_l3_v0 as module
        original = module.profile
        def invalid(level):
            sheet = original(level)
            sheet["talents"] = ["TAL-U04 Route Familiarity"]
            return sheet
        with patch.object(module, "profile", side_effect=invalid):
            report = audit()
        seen = {(issue["pairing"], issue["level"], issue["code"])
                for issue in report["issues"]}
        self.assertTrue({("Scholar/High", n, "talent_prerequisite")
                         for n in (1, 2, 3)} <= seen)
        self.assertEqual((12, 39), (report["pairings_checked"],
                                    report["level_snapshots_checked"]))

    def test_41_deep_volition_reserve_is_flat_and_earned(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as high
        from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile as medium
        from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile as low
        gates = talent_minimums()
        self.assertEqual(2, deep_volition_reserve_bonus())
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            for level in (1, 2, 3):
                with self.subTest(focus=focus, level=level):
                    baseline = make(level)
                    earned = deepcopy(baseline)
                    earned["talents"] = ["TAL-M01 Deep Volition Reserve"]
                    earned["vp_max"] += 2
                    # Low/Medium L3 have multiple awards; conserve the
                    # remaining earned selection rather than fabricating it.
                    existing = len(baseline["talents"])
                    if existing > 1:
                        earned["talents"] += list(baseline["talents"])[1:]
                    codes = {x["code"] for x in _sheet_issues(
                        "Anointed/"+focus, level, earned, earned, None, gates)}
                    self.assertNotIn("vp_formula", codes)
                    self.assertNotIn("talent_unaccounted", codes)
                    self.assertNotIn("talent_gate", codes)
                    # Owning the Talent without its +2 bonus is also invalid.
                    missing_bonus = deepcopy(earned)
                    missing_bonus["vp_max"] -= 2
                    codes = {x["code"] for x in _sheet_issues(
                        "Anointed/"+focus, level, missing_bonus,
                        earned, None, gates)}
                    self.assertIn("vp_formula", codes)
                    # The flat +2 does not scale with character level.
                    if level > 1:
                        inflated = deepcopy(earned)
                        inflated["vp_max"] += 2 * (level - 1)
                        codes = {x["code"] for x in _sheet_issues(
                            "Anointed/"+focus, level, inflated,
                            earned, None, gates)}
                        self.assertIn("vp_formula", codes)
                    unauthorized = deepcopy(baseline)
                    unauthorized["vp_max"] += 2
                    codes = {x["code"] for x in _sheet_issues(
                        "Anointed/"+focus, level, unauthorized,
                        baseline, None, gates)}
                    self.assertIn("vp_formula", codes)

    def test_42_saved_l2_learned_discipline_point_can_be_spent_at_l3(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as high
        from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile as medium
        from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile as low
        gates = talent_minimums()
        for focus, make in (("High", high), ("Medium", medium), ("Low", low)):
            with self.subTest(focus=focus):
                sheets = [make(n) for n in (1, 2, 3)]
                sheets[1]["learned_disciplines"] = deepcopy(
                    sheets[0]["learned_disciplines"])
                sheets[1]["learned_points"] = 8
                sheets[1]["saved_learned_discipline_points"] = 1
                sheets[2]["saved_learned_discipline_points"] = 0
                for index, sheet in enumerate(sheets):
                    codes = {x["code"] for x in _sheet_issues(
                        "Anointed/"+focus, index+1, sheet, sheets[0],
                        sheets[index-1] if index else None, gates)}
                    self.assertNotIn("learned_budget", codes)
                    self.assertNotIn("learned_progression", codes)
                    self.assertNotIn("learned_total", codes)
                    self.assertNotIn("learned_ranks", codes)

    def test_43_invalid_saved_learned_balances_and_false_spending_fail(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile
        gates = talent_minimums()
        for malformed in ("1", None, 1.0, True, -1, 2):
            with self.subTest(saved=malformed):
                forged = profile(2)
                forged["saved_learned_discipline_points"] = malformed
                codes = {x["code"] for x in _sheet_issues(
                    "Anointed/High", 2, forged, profile(1),
                    profile(1), gates)}
                self.assertIn("learned_budget", codes)
                if type(malformed) is not int or malformed < 0:
                    self.assertIn("learned_progression", codes)
        # A valid-looking L3 extra +1 without a saved point is not earned.
        forged = profile(3)
        forged["learned_disciplines"]["Unawarded Lore"] = 1
        forged["learned_points"] += 1
        codes = {x["code"] for x in _sheet_issues(
            "Anointed/High", 3, forged, profile(1), profile(2), gates)}
        self.assertIn("learned_budget", codes)
        self.assertIn("learned_progression", codes)
        # An L3 rank decrease does not become a free refund to saved points.
        forged = profile(3)
        forged["learned_disciplines"]["Medicine"] -= 1
        forged["learned_points"] -= 1
        forged["saved_learned_discipline_points"] = 1
        codes = {x["code"] for x in _sheet_issues(
            "Anointed/High", 3, forged, profile(1), profile(2), gates)}
        self.assertIn("learned_progression", codes)
        self.assertNotIn("learned_budget", codes)

    def test_44_cross_source_audit_accepts_deferred_learned_point(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        original = module.profile
        def saved_at_l2(level):
            sheet = original(level)
            if level == 2:
                initial = original(1)
                sheet["learned_disciplines"] = initial["learned_disciplines"]
                sheet["learned_points"] = 8
                sheet["saved_learned_discipline_points"] = 1
            return sheet
        with patch.object(module, "profile", side_effect=saved_at_l2):
            report = audit()
        found = {(x["pairing"], x["level"], x["code"])
                 for x in report["issues"]}
        for level in (2, 3):
            self.assertNotIn(("Anointed/High", level, "learned_budget"), found)
            self.assertNotIn(("Anointed/High", level, "learned_progression"), found)
        self.assertEqual((12, 39), (report["pairings_checked"],
                                    report["level_snapshots_checked"]))

    def test_45_cross_source_audit_accepts_flat_talent_vp(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        original = module.profile
        def reserve_at_creation(level):
            sheet = original(level)
            sheet["talents"] = ["TAL-M01 Deep Volition Reserve"]
            sheet["vp_max"] += 2
            return sheet
        with patch.object(module, "profile", side_effect=reserve_at_creation):
            report = audit()
        found = {(x["pairing"], x["level"], x["code"])
                 for x in report["issues"]}
        for level in (1, 2, 3):
            self.assertNotIn(("Anointed/High", level, "vp_formula"), found)
        self.assertEqual((12, 39), (report["pairings_checked"],
                                    report["level_snapshots_checked"]))

    def test_46_canonical_starter_item_prices_and_weapon_families(self):
        catalogue = canonical_starter_item_prices()
        self.assertEqual(4, catalogue["Dagger"])
        self.assertEqual(25, catalogue["Leather"])
        self.assertEqual(25, catalogue["Leather armor"])
        self.assertEqual(15, catalogue["Medical kit"])
        self.assertEqual(15, catalogue["Basic medical kit"])
        self.assertEqual(8, catalogue["Adventuring pack"])
        self.assertEqual(8, catalogue["Standard adventuring pack"])
        self.assertEqual(55, catalogue["Heavy crossbow"])
        self.assertEqual(5, catalogue["20 arrows"])
        self.assertNotIn("Ordinary clothing / light robes", catalogue)
        self.assertNotIn("Heavy padded / battle robes", catalogue)
        self.assertNotIn("Made-up discount", catalogue)
        self.assertEqual(30, len(catalogue))  # 29 rows - 2 banned + 3 aliases
        self.assertEqual({
            "Small Blades", "One-Handed Swords", "Two-Handed Swords",
            "Polearms", "Axes", "Blunt Weapons", "Bows", "Crossbows",
        }, canonical_weapon_families())

    def test_47_discount_forgery_with_matching_silver_still_fails(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile
        gates = talent_minimums()
        base = profile(1)
        baseline = {i["code"] for i in _sheet_issues(
            "Anointed/High", 1, base, base, None, gates)}
        self.assertNotIn("equipment_budget", baseline)
        for forged_name, forged_price in (
                ("Dagger", 0), ("Dagger", 3),
                ("Leather armor", 0), ("Basic medical kit", 1),
                ("Standard adventuring pack", 0)):
            with self.subTest(item=forged_name, price=forged_price):
                sheet = deepcopy(base)
                original_price = sheet["equipment_sp"][forged_name]
                sheet["equipment_sp"][forged_name] = forged_price
                sheet["silver_remaining_sp"] += original_price-forged_price
                codes = {i["code"] for i in _sheet_issues(
                    "Anointed/High", 1, sheet, base, None, gates)}
                self.assertIn("equipment_budget", codes)
        for item in ("Nonexistent equipment", "Heavy padded / battle robes",
                     "Ordinary clothing / light robes"):
            with self.subTest(unauthored=item):
                sheet = deepcopy(base)
                sheet["equipment_sp"][item] = 1
                sheet["silver_remaining_sp"] -= 1
                codes = {i["code"] for i in _sheet_issues(
                    "Anointed/High", 1, sheet, base, None, gates)}
                self.assertIn("equipment_budget", codes)
        original = deepcopy(base)
        original["equipment_sp"]["Dagger"] = 4
        codes = {i["code"] for i in _sheet_issues(
            "Anointed/High", 1, original, base, None, gates)}
        self.assertNotIn("equipment_budget", codes)

    def test_48_weapon_training_requires_exact_authored_family(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile
        gates = talent_minimums()
        base = profile(1)
        for invalid in ("Shields", "Shield Training", "Throwing",
                        "Daggers", "Unknown Family", 7, None):
            with self.subTest(family=invalid):
                sheet = deepcopy(base)
                sheet["weapon_training"] = {invalid: 2}
                codes = {i["code"] for i in _sheet_issues(
                    "Anointed/High", 1, sheet, base, None, gates)}
                self.assertIn("weapon_budget", codes)
        for legal in canonical_weapon_families():
            with self.subTest(family=legal):
                sheet = deepcopy(base)
                sheet["weapon_training"] = {legal: 2}
                codes = {i["code"] for i in _sheet_issues(
                    "Anointed/High", 1, sheet, base, None, gates)}
                self.assertNotIn("weapon_budget", codes)
        split = deepcopy(base)
        split["weapon_training"] = {"Small Blades": 1, "Bows": 1}
        codes = {i["code"] for i in _sheet_issues(
            "Anointed/High", 1, split, base, None, gates)}
        self.assertNotIn("weapon_budget", codes)

    def test_49_full_audit_detects_persistently_forged_prices_and_shields(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        make = module.profile
        def forged(level):
            sheet = make(level)
            sheet["weapon_training"] = {"Shields": 2}
            sheet["equipment_sp"]["Dagger"] = 0
            sheet["silver_remaining_sp"] += 4
            return sheet
        with patch.object(module, "profile", side_effect=forged):
            report = audit()
        found = {(i["pairing"], i["level"], i["code"])
                 for i in report["issues"]}
        self.assertTrue({
            ("Anointed/High", n, code)
            for n in (1, 2, 3)
            for code in ("weapon_budget", "equipment_budget")
        } <= found)
        self.assertEqual(12, report["pairings_checked"])
        self.assertEqual(39, report["level_snapshots_checked"])
        self.assertEqual(0, report["independently_certified_full_focuses"])

    def test_50_saved_weapon_points_are_spendable_after_creation(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile
        gates = talent_minimums()
        for focus_profile in (1, 0):
            with self.subTest(initial_invested=focus_profile):
                sheets = [profile(n) for n in (1, 2, 3)]
                sheets[0]["weapon_training"] = {"Small Blades": focus_profile}
                sheets[0]["saved_weapon_development_points"] = 2-focus_profile
                # An unused L1 point can remain unspent at L2.
                sheets[1]["weapon_training"] = {"Small Blades": focus_profile}
                sheets[1]["saved_weapon_development_points"] = 2-focus_profile
                # L3 spends all earlier saved points; there is no L3 award.
                sheets[2]["weapon_training"] = {"Small Blades": 2}
                sheets[2]["saved_weapon_development_points"] = 0
                for i, sheet in enumerate(sheets):
                    issues = {x["code"] for x in _sheet_issues(
                        "Anointed/High", i+1, sheet, sheets[0],
                        sheets[i-1] if i else None, gates)}
                    self.assertNotIn("weapon_budget", issues)
                    self.assertNotIn("weapon_progression", issues)
                    self.assertNotIn("weapon_total", issues)
        # Spend exactly one point at L2 and keep the remaining point.
        l1, l2 = profile(1), profile(2)
        l1["weapon_training"] = {"Small Blades": 0}
        l1["saved_weapon_development_points"] = 2
        l2["weapon_training"] = {"Small Blades": 1}
        l2["saved_weapon_development_points"] = 1
        issues = {x["code"] for x in _sheet_issues(
            "Anointed/High", 2, l2, l1, l1, gates)}
        self.assertNotIn("weapon_progression", issues)
        self.assertNotIn("weapon_budget", issues)

    def test_51_weapon_saved_balances_do_not_allow_unearned_or_refunded_ranks(self):
        from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile
        gates = talent_minimums()
        for invalid in ("1", 1.0, None, True, -1, 2):
            with self.subTest(saved=invalid):
                sheet = profile(1)
                sheet["weapon_training"] = {"Small Blades": 1}
                sheet["saved_weapon_development_points"] = invalid
                codes = {x["code"] for x in _sheet_issues(
                    "Anointed/High", 1, sheet, sheet, None, gates)}
                if invalid != 1 or type(invalid) is not int:
                    self.assertIn("weapon_budget", codes)
        l1, l2 = profile(1), profile(2)
        # Inverting ranks into a fictitious saved point is a refund.
        l2["weapon_training"] = {"Small Blades": 1}
        l2["saved_weapon_development_points"] = 1
        codes = {x["code"] for x in _sheet_issues(
            "Anointed/High", 2, l2, l1, l1, gates)}
        self.assertNotIn("weapon_budget", codes)
        self.assertIn("weapon_progression", codes)
        # Two ranks cannot be purchased with no available saved balance.
        l1["weapon_training"] = {"Small Blades": 1}
        l1["saved_weapon_development_points"] = 1
        l2["weapon_training"] = {"Small Blades": 2, "Bows": 1}
        l2["saved_weapon_development_points"] = 0
        codes = {x["code"] for x in _sheet_issues(
            "Anointed/High", 2, l2, l1, l1, gates)}
        self.assertIn("weapon_budget", codes)
        self.assertIn("weapon_progression", codes)
        # A malformed prior balance must not satisfy an authentic delta.
        bad_prior = profile(1)
        bad_prior["saved_weapon_development_points"] = "0"
        codes = {x["code"] for x in _sheet_issues(
            "Anointed/High", 2, profile(2), bad_prior, bad_prior, gates)}
        self.assertIn("weapon_progression", codes)

    def test_52_full_audit_allows_late_saved_weapon_spending(self):
        from scripts import b05_high_anointed_restoration_l1_l3_v0 as module
        original = module.profile
        def saved_at_creation(level):
            sheet = original(level)
            if level in (1, 2):
                sheet["weapon_training"] = {"Small Blades": 1}
                sheet["saved_weapon_development_points"] = 1
            return sheet
        with patch.object(module, "profile", side_effect=saved_at_creation):
            report = audit()
        found = {(x["pairing"], x["level"], x["code"])
                 for x in report["issues"]}
        for level in (1, 2, 3):
            self.assertNotIn(("Anointed/High", level, "weapon_budget"), found)
            self.assertNotIn(("Anointed/High", level, "weapon_progression"), found)
        self.assertEqual((12, 39), (report["pairings_checked"],
                                    report["level_snapshots_checked"]))

    def test_53_workflow_triggers_for_every_audited_source_and_ruleset(self):
        # Missing a PR path prevents the independently audited source from
        # ever reaching these tests, regardless of how correct the audit is.
        workflow = (Path(__file__).resolve().parents[1] /
                    ".github/workflows/b04-b07-independent-progression-audit.yml"
                    ).read_text(encoding="utf-8")
        match = re.search(
            r"(?ms)^  pull_request:\n    paths:\n(?P<paths>.*?)(?=^  workflow_dispatch:)",
            workflow)
        self.assertIsNotNone(match)
        patterns = re.findall(r"^      - '([^']+)'$",
                              match.group("paths"), flags=re.MULTILINE)
        self.assertGreater(len(patterns), 0)
        def covered(path):
            return any(fnmatchcase(path, pattern) for pattern in patterns)
        required = {
            "scripts/b04_b07_independent_progression_audit_v0.py",
            "tests/test_b04_b07_independent_progression_audit_v0.py",
            ".github/workflows/b04-b07-independent-progression-audit.yml",
            "scripts/b06_hunter_party_exchanges_v0.py",
            "scripts/b06_encounter_state_v0.py",
            LOW_RECORD, CATALOGUE, WEAPON_TRAINING_CATALOGUE,
            EQUIPMENT_CATALOGUE, CANONICAL_ASPECTS, GIFTED_FOUNDATION,
            ANOINTED_SIGNATURE_AUTHORITY,
            "docs/rules/08-archetypes/scholar.md",
            "docs/rules/08-archetypes/priest.md",
            "docs/rules/05-combat/action-categories-and-physical-tempo.md",
        }
        required.update("scripts/" + name + ".py" for name in SOURCE_MODULES.values())
        required.update("docs/rules/07-veil-magic/" + entry[-1]
                        for entry in PRIEST_LIFE_RULE_SOURCES)
        required.update("docs/rules/07-veil-magic/" + entry[-1]
                        for entry in SCHOLAR_RULE_SOURCES)
        missing = sorted(path for path in required if not covered(path))
        self.assertEqual([], missing)

    def test_54_reconciled_talent_source_ledgers_preserve_focus_awards(self):
        from scripts.b05_high_priest_life_l1_l3_v0 import profile as priest
        from scripts.b05_medium_gifted_l1_l3_v0 import profile as gifted
        from scripts.b05_low_scholar_l1_l3_v0 import profile as scholar
        from scripts.b04_b07_independent_progression_audit_v0 import TALENT_AWARDS
        cases = (
            ("Priest/High", "High", priest,
             (("TAL-C02",), ("TAL-C02",), ("TAL-C02",)), (0, 0, 0)),
            ("Gifted/Medium", "Medium", gifted,
             (("TAL-G01",), ("TAL-G01",), ("TAL-G01",)), (0, 0, 1)),
            ("Scholar/Low", "Low", scholar,
             (("TAL-U01",), ("TAL-U01",),
              ("TAL-U01", "TAL-C01")), (0, 1, 1)),
        )
        gates = talent_minimums()
        for pairing, focus, make, ids, saved in cases:
            sheets = [make(level) for level in (1, 2, 3)]
            for index, sheet in enumerate(sheets):
                level = index+1
                with self.subTest(pairing=pairing, level=level):
                    actual = tuple(t.split()[0] for t in sheet["talents"])
                    self.assertEqual(ids[index], actual)
                    self.assertEqual(
                        sheet.get("saved_talent_selections", 0), saved[index])
                    self.assertEqual(len(actual)+saved[index], sum(
                        award <= level for award in TALENT_AWARDS[focus]))
                    codes = {x["code"] for x in _sheet_issues(
                        pairing, level, sheet, sheets[0],
                        sheets[index-1] if index else None, gates)}
                    self.assertFalse({
                        "talent_identity", "talent_overaward",
                        "talent_unaccounted", "talent_gate",
                        "talent_archetype", "talent_retraining",
                    } & codes)

        self.assertEqual([priest(n)["normal_regen_throughput"]
                          for n in (1, 2, 3)], [4, 4, 4])
        self.assertEqual([scholar(n)["initiative"] for n in (1, 2, 3)],
                         [4, 4, 6])
        self.assertEqual(gifted(3)["talent_selections_available"], 2)

    def test_55_ledger_tampering_reopens_independently_reported_findings(self):
        from scripts import b05_high_priest_life_l1_l3_v0 as pmod
        from scripts import b05_medium_gifted_l1_l3_v0 as gmod
        from scripts import b05_low_scholar_l1_l3_v0 as smod
        original = {m: m.profile for m in (pmod, gmod, smod)}
        def forbidden_high(level):
            sheet = original[pmod](level)
            if level == 3:
                sheet["talents"] = ("TAL-C02", "TAL-M03")
            return sheet
        def missing_medium(level):
            sheet = original[gmod](level)
            if level == 3:
                sheet.pop("saved_talent_selections")
            return sheet
        def missing_low(level):
            sheet = original[smod](level)
            if level >= 2:
                sheet["saved_talent_selections"] = 0
            return sheet
        for module, replacement, expected in (
                (pmod, forbidden_high,
                 {("Priest/High", 3, "talent_overaward")}),
                (gmod, missing_medium,
                 {("Gifted/Medium", 3, "talent_unaccounted")}),
                (smod, missing_low,
                 {("Scholar/Low", 2, "talent_unaccounted"),
                  ("Scholar/Low", 3, "talent_unaccounted")}),
        ):
            with self.subTest(module=module.__name__):
                with patch.object(module, "profile", side_effect=replacement):
                    report = audit()
                found = {(x["pairing"], x["level"], x["code"])
                         for x in report["issues"]}
                self.assertTrue(expected <= found)
                self.assertEqual((12, 39), (report["pairings_checked"],
                                            report["level_snapshots_checked"]))
                self.assertEqual(0, report["independently_certified_full_focuses"])

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
