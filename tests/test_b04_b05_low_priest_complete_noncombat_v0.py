"""B04/B05 Low Life A/B full source-sheets and noncombat source receipts."""
from copy import deepcopy
from unittest.mock import patch
import unittest

from scripts.b05_low_priest_life_l1_l3_v0 import BUILD, profile, verify
from scripts.b04_b05_low_priest_complete_noncombat_v0 import (
    STATUS, matrix, native_utility, verify_level,
)
from scripts.b04_b05_noncombat_scene_resolution_v0 import (
    _character, resolve_scene,
)
from scripts.b04_b07_independent_progression_audit_v0 import (
    LOW_FULL_SOURCE, _low_full_issues, audit, talent_minimums,
)
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import roster
from scripts.b06_encounter_state_v0 import UnresolvedDecision, party_actor
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class LowPriestFullNoncombatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = matrix()
        cls.independent = audit()

    def test_01_a_b_six_structural_purchased_sheet_snapshots(self):
        self.assertEqual(verify()["levels"], 6)
        self.assertEqual((self.rows["low_priest_variants"],
                          self.rows["level_snapshots"]), (2, 6))
        self.assertEqual(self.independent["pairings_checked"], 12)
        self.assertEqual(self.independent["variants_checked"], 13)
        self.assertEqual(self.independent["level_snapshots_checked"], 39)
        self.assertFalse(self.independent["pairings"]["Priest/Low"]["issues"])
        for role in ("A", "B"):
            prev = None
            for level in (1, 2, 3):
                p = profile(role, level)
                self.assertEqual(p["level"], level)
                self.assertEqual(p["variant"], role)
                self.assertEqual(p["pillar"], "Life")
                self.assertEqual(p["prepared_capacity"], 2 if level == 1 else 3)
                self.assertEqual(len(p["prepared_prayers"]), p["prepared_capacity"])
                self.assertEqual(len(p["talents"]), level)
                self.assertEqual(sum(p["learned_disciplines"].values()),
                                 8 + (level >= 2))
                self.assertEqual(p["vp_max"], 2 * level)
                self.assertEqual(p["normal_regen_throughput"], 6)
                self.assertEqual(p["active_devotional_rite_cap"], 1)
                self.assertFalse(p["blink_affordable_at_initial_full_vp"])
                if prev is not None:
                    self.assertTrue(set(prev["prepared_prayers"]) <=
                                    set(p["prepared_prayers"]))
                prev = p

    def test_02_a_b_hands_preparation_training_and_resource_differences(self):
        for level in (1, 2, 3):
            a, b = profile("A", level), profile("B", level)
            self.assertEqual(a["chosen_devotion"], "Guided Regeneration")
            self.assertEqual(b["chosen_devotion"], "Vital Shelter")
            self.assertEqual(a["equipment_sp"]["Leather armor"], 25)
            self.assertEqual(b["equipment_sp"]["Shield"], 16)
            self.assertEqual((a["silver_remaining"], b["silver_remaining"]), (80, 0))
            self.assertEqual((a["free_hands"], b["free_hands"]), (1, 0))
            self.assertTrue(a["basic_heal_hand_available_in_authored_loadout"])
            self.assertFalse(b["basic_heal_hand_available_in_authored_loadout"])
            self.assertEqual(a["learned_disciplines"]["Medicine"], 2)
            self.assertEqual(b["learned_disciplines"]["Herbalism"], 2)
            self.assertEqual(a["learned_disciplines"]["Acrobatics"], 2)
            self.assertEqual(b["learned_disciplines"].get("Acrobatics", 0), 0)
            self.assertNotIn("Woodland Rapport", b["prepared_prayers"])
            self.assertNotIn("Venom Endurance", a["prepared_prayers"])

    def test_03_independent_audit_reconciles_live_physical_proxies(self):
        gates = talent_minimums()
        for role in ("A", "B"):
            for level in (1, 2, 3):
                actor = party_actor(role, level, "low", "party", occupied=((1,1),))
                p = profile(role, level)
                self.assertEqual(_low_full_issues(
                    role, level, p, actor, profile(role, 1),
                    profile(role, level-1) if level>1 else None, gates), [])
                self.assertEqual(actor.source.source_id, role)
                self.assertEqual(actor.source.status, "B05_UNBUFFED_PHYSICAL_PROXY")
                self.assertEqual(actor.hp_max, p["hp_max"])
                self.assertEqual(actor.vp_max, p["vp_max"])

    def test_04_roster_adds_full_sheet_provenance_not_extra_focus(self):
        low = next(x for x in roster() if x["pairing"] == "Priest/Low")
        self.assertEqual(low["structural_variants"], 2)
        self.assertEqual(len(low["source_fingerprints"]), 3)
        self.assertIn(LOW_FULL_SOURCE, low["source_fingerprints"])
        self.assertEqual(len(low["source_fingerprints"][LOW_FULL_SOURCE]), 64)
        self.assertEqual(low["source_issues"], [])
        self.assertFalse(low["independently_full_certified"])

    def test_05_both_variants_get_real_trained_noncombat_core_checks(self):
        for role in ("A", "B"):
            for level in (1,2,3):
                actor, abilities, learned, scope = _character(
                    "Priest/Low", level, low_variant=role)
                self.assertEqual(learned, profile(role, level)["learned_disciplines"])
                self.assertEqual(scope, "LOW_PRIEST_FULL_SELECTED_SHEET_NATIVE_G0_PHYSICAL_ONLY")
                diagnosis = resolve_scene(
                    "Priest/Low", level, "investigation", "diagnose", low_variant=role)
                self.assertEqual(diagnosis["trained_rank"], 2)
                self.assertEqual(diagnosis["training"], "Medicine")
                balance = resolve_scene(
                    "Priest/Low", level, "exploration", "balance", low_variant=role)
                self.assertEqual(balance["trained_rank"], 2 if role == "A" else 0)
                self.assertGreater(diagnosis["elapsed_seconds"], 0)
                self.assertFalse(diagnosis["external_gm_adjudicated"])

    def test_06_genuine_native_paid_inspection_for_six_sources(self):
        for role in ("A", "B"):
            for level in (1,2,3):
                r = native_utility(role, level, "inspection")
                self.assertEqual(r["ap_paid"], profile(role, level)["turn_ap"])
                self.assertEqual(r["vp_spent"], 2)
                self.assertEqual(r["vp_before"], 2*level)
                self.assertEqual(r["vp_after"], 2*level-2)
                self.assertEqual(r["ledger_sha256"], canonical_digest(r["ledger"]))
                self.assertFalse(r["focus_certified"])
                self.assertTrue(any(e["kind"]=="action_committed" for e in r["ledger"]))

    def test_07_only_prepared_a_l2_l3_has_native_woodland_rapport(self):
        for level in (2,3):
            r = native_utility("A", level, "rapport")
            self.assertEqual((r["ap_paid"],r["vp_spent"]), (30,2))
            self.assertEqual(r["observation"]["animal_response"], "UNRESOLVED_GM")
            self.assertFalse(r["observation"]["forced_compliance"])
        for role,level in (("A",1),("B",1),("B",2),("B",3)):
            with self.subTest(role=role,level=level), self.assertRaises(UnresolvedDecision):
                native_utility(role,level,"rapport")
        for kwargs in ({"animal_mass_kg":26}, {"animal_visible":False},
                       {"animal_wary":False}, {"animal_mass_kg":True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                native_utility("A",2,"rapport",**kwargs)

    def test_08_source_forgery_prayer_training_gear_and_talent_fail_independent_audit(self):
        gates=talent_minimums()
        for kind in ("training", "chosen", "equipment", "talent", "hand",
                     "prepared", "regeneration"):
            p=deepcopy(profile("B",3))
            if kind=="training":
                p["learned_disciplines"]["Herbalism"]=3
            elif kind=="chosen":
                p["chosen_devotion"]="Guided Regeneration"
            elif kind=="equipment":
                p["equipment_sp"]["Shield"]=0
            elif kind=="talent":
                p["talents"]=("TAL-C05","TAL-C01","TAL-C01")
            elif kind=="hand":
                p["free_hands"]=1
            elif kind=="prepared":
                p["prepared_prayers"] += ("Conjure Flame",)
            else:
                p["normal_regen_throughput"]=10
            actor=party_actor("B",3,"low","party",occupied=((1,1),))
            with self.subTest(kind=kind):
                found=_low_full_issues("B",3,p,actor,profile("B",1),
                                       profile("B",2),gates)
                self.assertTrue(found, kind)

    def test_09_legal_l3_talent_substitution_rejected_by_full_audit_and_roster(self):
        # Codex P2: C10 -> C09 for A (and C09 -> C10 for B) is
        # individually legal. Neither is the original source-selected build.
        from scripts.b04_b07_twelve_focus_certification_protocol_v0 import _source_roster
        original_profile = profile
        for role, legal_replacement in (("A", "TAL-C09"), ("B", "TAL-C10")):
            with self.subTest(role=role):
                def substitute(selected_role, level):
                    sheet = original_profile(selected_role, level)
                    if selected_role == role and level == 3:
                        forged = tuple(sheet["talents"][:2]) + (legal_replacement,)
                        sheet["talents"] = forged
                        sheet["selected_talents_by_level"] = forged
                    return sheet

                # The ordinary checks already accept these level-legal
                # Talent replacements. Exact source identity must not.
                with patch("scripts.b05_low_priest_life_l1_l3_v0.profile",
                           side_effect=substitute):
                    result = audit()
                findings = [issue for issue in result["pairings"]["Priest/Low"]["issues"]
                            if issue["variant"] == role and issue["level"] == 3]
                self.assertIn("low_talent_source", {x["code"] for x in findings})
                with patch("scripts.b04_b07_twelve_focus_certification_protocol_v0.audit",
                           return_value=result):
                    low = next(x for x in _source_roster.__wrapped__()
                               if x["pairing"] == "Priest/Low")
                self.assertIn("low_talent_source",
                              {x["code"] for x in low["source_issues"]})
                self.assertFalse(low["independently_full_certified"])

    def test_09b_talent_selected_ledger_cannot_disagree_with_talents(self):
        gates = talent_minimums()
        for role in ("A", "B"):
            for field in ("talents", "selected_talents_by_level"):
                with self.subTest(role=role, field=field):
                    sheet = deepcopy(profile(role, 3))
                    sheet[field] = tuple(sheet[field][:2]) + (
                        "TAL-C09" if role == "A" else "TAL-C10",)
                    actor = party_actor(role, 3, "low", "party", occupied=((1, 1),))
                    issues = _low_full_issues(role, 3, sheet, actor,
                                              profile(role, 1), profile(role, 2), gates)
                    self.assertIn("low_talent_source", {i["code"] for i in issues})

    def test_09_source_tampering_cannot_upgrade_noncombat_training(self):
        original=profile("A",1)
        forged=deepcopy(original)
        forged["learned_disciplines"]["Acrobatics"]=0
        with patch("scripts.b05_low_priest_life_l1_l3_v0.profile",
                   return_value=forged):
            with self.assertRaises(ValueError):
                _character("Priest/Low",1,low_variant="A")

    def test_10_reject_unearned_levels_sources_and_unsourced_options(self):
        for role,level in (("C",1),("A",0),("A",4),("B",True)):
            with self.subTest(role=role,level=level),self.assertRaises(ValueError):
                profile(role,level)
        with self.assertRaises(UnresolvedDecision):
            native_utility("A",2,"mass_cure")
        with self.assertRaises(ValueError):
            resolve_scene("Priest/Low",2,"social","petition",low_variant="C")

    def test_11_immutable_noncertification_and_counts(self):
        self.assertEqual(self.rows["core_check_scenarios"],18)
        self.assertEqual(self.rows["native_paid_utility_actions"],8)
        self.assertEqual(self.rows["independent_full_focus_certificates"],0)
        self.assertEqual(self.rows["human_sessions"],0)
        self.assertEqual(self.rows["strict_mvp_exits_met"],0)
        for row in self.rows["rows"]:
            self.assertEqual(row["status"], STATUS)
            self.assertEqual(row["authentic_human_choices"],0)
            self.assertFalse(row["full_focus_certified"])


if __name__ == "__main__":
    unittest.main()
