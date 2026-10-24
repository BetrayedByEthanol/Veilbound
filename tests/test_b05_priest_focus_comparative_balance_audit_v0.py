"""Fail-closed comparative Priest Focus audit, not full three-Focus certification."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts.b05_priest_focus_comparative_balance_audit_v0 import (
    FOCUSES, LEVELS, REQUIRED_RULES, SOURCE_PATHS, ROOT,
    _half_up_quarter, _crosscheck_real_characters, attest, audit,
    row, verify_basis,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class PriestFocusComparativeBalanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=audit(seed=0)

    def test_01_source_basis_exact_existing_rules(self):
        source=verify_basis()
        self.assertEqual(set(source),set(SOURCE_PATHS))
        self.assertTrue(all(v["present"] and v["chars"]>100
                            for v in source.values()))
        for path,details in source.items():
            self.assertEqual(len(details["sha256"]),64)
            self.assertEqual(details["sha256"],
                             sha256((ROOT/path).read_bytes()).hexdigest())
        self.assertIn("High",self.report["focus_progression"])
        self.assertIn("Low",self.report["focus_progression"])

    def test_02_audit_references_all_three_levels_and_one_chassis(self):
        r=self.report
        self.assertEqual(set(r["focus_progression"]),set(FOCUSES))
        for focus in FOCUSES:
            self.assertEqual([x["level"] for x in r["focus_progression"][focus]],
                             list(LEVELS))
            for entry in r["focus_progression"][focus]:
                self.assertEqual(entry["hp_max"],12)
                self.assertEqual(entry["vigor_max"],12*entry["level"])
                self.assertEqual(entry["accord"],1)
                self.assertFalse(entry["independent_full_focus_certified"])
        self.assertEqual(r["reference"]["veil_affinity"],0)
        self.assertEqual(r["reference"]["vitality"],2)

    def test_03_prepared_capacity_and_accord_variations(self):
        expected={"High":[4,5,5],"Medium":[3,4,4],"Low":[2,3,3]}
        for focus,values in expected.items():
            self.assertEqual(
                [r["effective_prepared_capacity"]
                 for r in self.report["focus_progression"][focus]],values)
            for level in LEVELS:
                self.assertEqual(row(focus,level,accord=-3)["effective_prepared_capacity"],
                                 max(1,row(focus,level)["base_prepared_capacity"]-3))
                self.assertEqual(row(focus,level,talent_bonus=1)["effective_prepared_capacity"],
                                 values[level-1]+1)
        self.assertEqual(row("High",1,accord=3)["effective_prepared_capacity"],6)
        self.assertEqual(row("Low",1,accord=-3)["effective_prepared_capacity"],1)

    def test_04_focus_vp_regen_recovery_and_tempo(self):
        expected={
            "High":{"vp":[6,12,18],"regen":3,"physical":[1,1,1],
                    "projection":[1,1,2],"recover":[2,3,5]},
            "Medium":{"vp":[4,8,12],"regen":4,"physical":[1,1,1],
                      "projection":[1,1,1],"recover":[1,2,3]},
            "Low":{"vp":[2,4,6],"regen":5,"physical":[1,1,2],
                   "projection":[1,1,1],"recover":[1,1,2]},
        }
        for focus,want in expected.items():
            rows=self.report["focus_progression"][focus]
            self.assertEqual([x["vp_max"] for x in rows],want["vp"])
            self.assertEqual([x["six_hour_vp_recovery"] for x in rows],
                             want["recover"])
            self.assertEqual([x["physical_tempo"] for x in rows],
                             want["physical"])
            self.assertEqual([x["projection_tempo"] for x in rows],
                             want["projection"])
            self.assertTrue(all(x["base_regen"]==want["regen"] for x in rows))
            self.assertTrue(all(x["normal_guard_capacity"]==x["physical_tempo"]
                                for x in rows))
            self.assertTrue(all(not x["mixed_physical_projection_in_one_turn"]
                                for x in rows))
        self.assertEqual(_half_up_quarter(6),2)
        self.assertEqual(_half_up_quarter(18),5)
        self.assertEqual([x["turn_ap"] for x in self.report["focus_progression"]["High"]],
                         [30,36,42])

    def test_05_selected_low_and_medium_add_talent_not_focus_rate(self):
        chosen=self.report["selected_source_witnesses"]
        self.assertEqual(set(chosen),{"Medium","Low"})
        self.assertEqual([chosen["Medium"][level]["total_regen"] for level in LEVELS],
                         [5,5,5])
        self.assertEqual([chosen["Low"][level]["total_regen"] for level in LEVELS],
                         [6,6,6])
        for level in LEVELS:
            self.assertEqual(chosen["Medium"][level]["selected_talent_regen_bonus"],1)
            self.assertEqual(chosen["Low"][level]["selected_talent_regen_bonus"],1)
            self.assertEqual(chosen["Low"][level]["chosen_guided_commitment"],1)
            self.assertEqual(chosen["Low"][level]["source_status"],
                             "B05_UNBUFFED_PHYSICAL_PROXY")
            self.assertFalse(chosen["Low"][level]["full_priest_spell_runtime_certified"])
        self.assertIsNone(self.report["high_priest_life_complete_character"])

    def test_06_basic_heal_action_cost_vs_chosen_rite(self):
        payments={(x["focus"],x["level"]):x
                  for x in self.report["priced_actions"]}
        self.assertEqual(len(payments),9)
        self.assertEqual([payments[(f,3)]["prepared_basic_heal"]["projection_ap"]
                          for f in FOCUSES],[20,24,30])
        for level in LEVELS:
            high=payments["High",level]
            self.assertEqual(high["unprepared_life_basic_heal_open_invocation"][
                "total_spent_vp"],3)
            self.assertEqual(high["unprepared_life_basic_heal_open_invocation"][
                "full_action_ap"],30+6*(level-1))
            self.assertEqual(payments["Low",level]["maintained_guided_on_self"][
                "committed_vp"],1)
            self.assertEqual(payments["Medium",level]["maintained_guided_on_self"][
                "committed_vp"],2)
            self.assertIsNone(payments["Low",level][
                "unprepared_life_basic_heal_open_invocation"])
            self.assertIsNone(payments["Medium",level][
                "unprepared_life_basic_heal_open_invocation"])

    def test_07_fixed_native_medium_evidence_and_paired_cost(self):
        r=self.report["native_medium_encounter"]
        self.assertTrue(r["native_medium_only"])
        self.assertEqual(r["policy_count"],27)
        self.assertEqual(len(r["native_policy_cells"]),27)
        self.assertEqual(len(r["l3_direct_vs_intercession_pairs"]),3)
        for pair in r["l3_direct_vs_intercession_pairs"]:
            self.assertEqual(pair["extra_spent_vp"],4)
            self.assertEqual(pair["extra_reactions"],2)
            self.assertNotEqual(pair["ledger_sha256_direct"],
                                pair["ledger_sha256_interceded"])
            self.assertFalse(pair["provisional_cost_accepted"])
        self.assertIsNone(r["low_and_high_opposed_cohorts"])
        self.assertIsNone(r["sampled_win_rate"])
        self.assertFalse(r["balance_price_approved"])

    def test_08_replay_and_report_integrity(self):
        r=self.report
        self.assertEqual(r["audit_sha256"],
                         canonical_digest({k:v for k,v in r.items()
                                           if k!="audit_sha256"}))
        self.assertEqual(attest(r,seed=0),r)
        self.assertEqual(audit(seed=0),r)
        fake=deepcopy(r)
        fake["focus_progression"]["High"][0]["vp_max"]=999
        with self.assertRaises(AssertionError):
            attest(fake,seed=0)
        fake["audit_sha256"]=canonical_digest(
            {k:v for k,v in fake.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest(fake,seed=0)
        with self.assertRaises(AssertionError):
            attest(r,seed=1)

    def test_09_rule_drift_detected_without_updating_canonical_source(self):
        replacement=dict(REQUIRED_RULES)
        replacement[SOURCE_PATHS[2]]=("invented action rule",)
        with patch("scripts.b05_priest_focus_comparative_balance_audit_v0.REQUIRED_RULES",
                   replacement):
            with self.assertRaisesRegex(AssertionError,"Rule changed"):
                verify_basis()

    @staticmethod
    def _mutate_source(path, before, after):
        """In-memory same-length edit; do not change canonical disk files."""
        before,after=before.encode("utf-8"),after.encode("utf-8")
        if len(before)!=len(after):
            raise AssertionError("Mutation test must preserve byte length")
        original=Path.read_bytes
        selected=ROOT/path
        def reader(self):
            raw=original(self)
            if self==selected:
                if raw.count(before)!=1:
                    raise AssertionError("Expected one source declaration")
                return raw.replace(before,after,1)
            return raw
        return reader

    def test_12_same_length_payment_edits_fail_before_attestation(self):
        examples=(
            ("docs/rules/08-archetypes/priest.md",
             "**1 additional Spent VP Invocation Surcharge**",
             "**2 additional Spent VP Invocation Surcharge**"),
            ("docs/rules/08-archetypes/priest.md",
             "This **+1 surcharge is a provisional",
             "This **+2 surcharge is a provisional"),
            ("docs/rules/08-archetypes/priest.md",
             "Intercession = 2 Spent VP",
             "Intercession = 3 Spent VP"),
            ("docs/rules/08-archetypes/priest.md",
             "**2→1 Committed VP**",
             "**2→2 Committed VP**"),
            ("docs/rules/07-veil-magic/basic-heal-v0.md",
             "| Primary VP | **2 × T Spent VP**",
             "| Primary VP | **3 × T Spent VP**"),
            ("docs/rules/07-veil-magic/guided-regeneration-v0.md",
             "| Maintained mode | **2 Committed VP**",
             "| Maintained mode | **3 Committed VP**"),
            ("docs/rules/07-veil-magic/vital-shelter-v0.md",
             "| Maintained mode — Primary | **2 Committed VP",
             "| Maintained mode — Primary | **3 Committed VP"),
            ("docs/rules/07-veil-magic/vital-shelter-v0.md",
             "| Primary initial prevention budget | **B = 8 +",
             "| Primary initial prevention budget | **B = 9 +"),
            ("docs/rules/10-advancement/talents-level-1-5-v0.md",
             "costs **1 fewer Spent VP**",
             "costs **2 fewer Spent VP**"),
        )
        for path,before,after in examples:
            with self.subTest(path=path,from_value=before):
                with patch.object(Path,"read_bytes",
                                  new=self._mutate_source(path,before,after)):
                    with self.assertRaisesRegex(AssertionError,
                                                "Rule changed or duplicate"):
                        verify_basis()
                    with self.assertRaisesRegex(AssertionError,
                                                "Rule changed or duplicate"):
                        attest(self.report,seed=0)

    def test_13_equal_length_nonprice_change_invalidates_previous_report(self):
        path="docs/design/b05-life-low-priest-l3-build-exaltation-verification-v0.md"
        baseline=verify_basis()
        with patch.object(Path,"read_bytes",new=self._mutate_source(
                path,"Verification record","Verification Record")):
            changed=verify_basis()
            self.assertEqual(changed[path]["chars"],baseline[path]["chars"])
            self.assertNotEqual(changed[path]["sha256"],
                                baseline[path]["sha256"])
            changed_report=audit(seed=0)
            self.assertNotEqual(changed_report["audit_sha256"],
                                self.report["audit_sha256"])
            self.assertEqual(changed_report["source_files"][path]["sha256"],
                             changed[path]["sha256"])
            with self.assertRaisesRegex(AssertionError,
                                        "independent source replay"):
                attest(self.report,seed=0)

    def test_10_invalid_inputs_fail_without_partial_report(self):
        for args in (
            ("Anointed",1,1,0),
            ("High",0,1,0),
            ("Low",4,1,0),
            ("Medium",True,1,0),
            ("High",2,-4,0),
            ("High",2,4,0),
            ("Low",3,1,-1),
            ("Medium",3,1,2),
        ):
            with self.subTest(args=args),self.assertRaises(ValueError):
                row(args[0],args[1],accord=args[2],talent_bonus=args[3])
        for invalid in (-1,True,0.1):
            with self.subTest(seed=invalid),self.assertRaises(ValueError):
                audit(seed=invalid)

    def test_11_explicit_acceptance_boundaries_are_not_gamed(self):
        r=self.report
        self.assertFalse(r["comparison_is_measured_three_focus_balance"])
        self.assertFalse(r["certify_representative_priest_encounter"])
        self.assertEqual(r["mvp_focus_certifications_added"],0)
        self.assertIsNone(r["high_priest_life_native_encounter"])
        self.assertIsNone(r["low_priest_life_full_spell_encounter"])
        self.assertIsNone(r["sampled_win_rate"])
        self.assertGreaterEqual(len(r["open_numerical_decisions"]),4)


if __name__=="__main__":
    unittest.main()
