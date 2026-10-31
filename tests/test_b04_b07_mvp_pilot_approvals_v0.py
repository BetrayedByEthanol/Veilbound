"""Restricted L1–3 pilot approvals: real source values, no fabricated native play."""
from pathlib import Path
import unittest

from scripts.b05_low_gifted_anchor_design_v0 import (
    CANDIDATE, LowGiftedAnchorDesign, starting_access,
)
from scripts.b05_low_gifted_l1_l3_v0 import profile, verify


ROOT=Path(__file__).resolve().parents[1]


class MvpPilotApprovalsTests(unittest.TestCase):
    def test_01_exact_approved_low_gifted_numbers_at_all_three_levels(self):
        self.assertEqual(set(CANDIDATE),{"Fear","Disgust"})
        self.assertEqual((CANDIDATE["Fear"]["name"],CANDIDATE["Fear"]["bonus"]),
                         ("Rooted Guard",1))
        self.assertEqual((CANDIDATE["Disgust"]["name"],
                          CANDIDATE["Disgust"]["mp_surcharge_reduction"]),
                         ("Unbound Step",1))
        self.assertTrue(verify())
        for level in (1,2,3):
            s=profile(level)
            a=starting_access(level)
            self.assertEqual(
                {k:a["links"][k]["anchor_expression_pilot"] for k in CANDIDATE},
                {"Fear":"Rooted Guard","Disgust":"Unbound Step"})
            self.assertEqual(
                {k:a["links"][k]["anchor_expression_candidate"] for k in CANDIDATE},
                {"Fear":"Rooted Guard","Disgust":"Unbound Step"})
            self.assertTrue(a["canonical_anchor_expression_authored"])
            self.assertFalse(a["anchor_native_effect_certified"])
            self.assertTrue(all(
                e["status"]=="PILOT_PROVISIONAL_APPROVED_NOT_NATIVE"
                for e in s["anchor_expressions"].values()))
            self.assertFalse(s["anchor_native_effect_certified"])
            self.assertFalse(s["independent_full_focus_certified"])

    def test_02_guard_bonus_only_on_paid_legal_self_defense_once_per_window(self):
        for level in (1,2,3):
            w=LowGiftedAnchorDesign(level)
            w.begin_window()
            w.establish_anchor("Fear")
            self.assertFalse(w.guarded_defense(
                kind="guard",paid=False,self_target=True,
                source_legal=True).applicable)
            self.assertEqual(1,w.guarded_defense(
                kind="guard",paid=True,self_target=True,
                source_legal=True).bonus)
            self.assertEqual(0,w.guarded_defense(
                kind="guard",paid=True,self_target=True,
                source_legal=True).bonus)
            w.begin_window()
            dodge=w.guarded_defense(kind="dodge",paid=True,
                                    self_target=True,source_legal=True)
            self.assertEqual(int(level>=2),dodge.bonus)
            if level==1:
                self.assertEqual(1,w.guarded_defense(
                    kind="guard",paid=True,self_target=True,
                    source_legal=True).bonus)
            else:
                self.assertEqual(0,w.guarded_defense(
                    kind="guard",paid=True,self_target=True,
                    source_legal=True).bonus)

    def test_03_movement_reduces_only_surcharge_not_base_or_opportunity(self):
        for level in (1,2,3):
            w=LowGiftedAnchorDesign(level)
            w.begin_window()
            w.establish_anchor("Disgust")
            unavailable=w.movement_step(kind="normal_difficult",paid=True,
                source_legal=True,base_mp=2,surcharge_mp=0)
            self.assertEqual((0,2),(unavailable.mp_reduction,
                                     unavailable.remaining_mp_cost))
            legal=w.movement_step(kind="normal_difficult",paid=True,
                source_legal=True,base_mp=2,surcharge_mp=1)
            self.assertEqual((1,2),(legal.mp_reduction,
                                     legal.remaining_mp_cost))
            repeated=w.movement_step(kind="normal_difficult",paid=True,
                source_legal=True,base_mp=2,surcharge_mp=1)
            self.assertEqual((0,3),(repeated.mp_reduction,
                                     repeated.remaining_mp_cost))
            w.begin_window()
            cautious=w.movement_step(kind="cautious",paid=True,
                source_legal=True,base_mp=2,surcharge_mp=1)
            self.assertEqual(int(level>=2),cautious.mp_reduction)
            self.assertGreaterEqual(cautious.remaining_mp_cost,2)

    def test_04_no_fake_refresh_after_same_window_break(self):
        w=LowGiftedAnchorDesign(3)
        w.begin_window()
        w.establish_anchor("Fear")
        self.assertEqual(1,w.guarded_defense(
            kind="guard",paid=True,self_target=True,
            source_legal=True).bonus)
        w.break_anchor("Disgust")
        self.assertEqual(0,w.movement_step(
            kind="normal_difficult",paid=True,source_legal=True,
            base_mp=1,surcharge_mp=2).mp_reduction)
        self.assertEqual(18,w.ap_remaining)
        w.begin_window()
        self.assertEqual(1,w.movement_step(
            kind="normal_difficult",paid=True,source_legal=True,
            base_mp=1,surcharge_mp=2).mp_reduction)

    def test_05_milestones_are_restricted_to_pilot_and_no_xp_benefits(self):
        text=(ROOT/"docs/rules/10-advancement/progression-architecture.md").read_text()
        section=text.split("## Restricted L1–3 MVP pilot — milestone awards")[1].split(
            "## Not yet canonical")[0]
        for phrase in ("Level 1","Level 2","Level 3","two distinct",
                       "GM-declared","not a general level-award rule",
                       "no automatic", "pilot"):
            self.assertIn(phrase.lower(),section.lower())
        self.assertIn("outside the restricted L1–3 MVP pilot",text)
        self.assertIn("automatically grants a character level",section.lower())
        self.assertIn("not a general level-award rule",section.lower())

    def test_06_watch_count_and_mvp_gates_are_not_falsely_closed(self):
        doc=(ROOT/"docs/design/b04-b05-b07-mvp-pilot-approvals-and-watches-v0.md").read_text()
        source=(ROOT/"docs/rules/08-archetypes/low-gifted-anchored-expressions-l1-3-v0.md").read_text()
        roadmap=(ROOT/"docs/design/veilbound-roadmap-and-mvp-readiness.md").read_text()
        for marker in ("13","10 of 24","14","watch","D1","D2","D4",
                       "milestone","12/12","0/12","0/6"):
            self.assertIn(marker.lower(),doc.lower())
        self.assertIn("0/12",source)
        self.assertIn("0/6",roadmap)
        self.assertEqual(6,sum(s.startswith("| [ ] **") for s in roadmap.splitlines()))
        self.assertIn("#178",roadmap)
        self.assertIn("bounded native",doc.lower())
        self.assertIn("not itself",doc.lower())
        self.assertIn("merged #180",doc.lower())
        self.assertIn("0/12",doc)


if __name__=="__main__":
    unittest.main()
