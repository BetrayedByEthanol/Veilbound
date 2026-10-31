"""B04/B06/B07 milestone + persistent native G0/G8 party continuity."""
import unittest
from copy import deepcopy

from scripts.b04_b06_b07_integrated_milestone_persistent_party_v0 import (
    run, _l1, award, fixture_awards, _entry_l2, _l2_withdrawal,
)
from scripts.b05_b06_native_party_continuity_v0 import party_state
from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class MilestonePartyAdventureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run()

    def test_01_source_narrative_then_exact_native_g8_l2_l3(self):
        r=self.report
        self.assertEqual(r["session_plan_levels"],[1,2,2,3])
        self.assertEqual(r["actual_g8_combat_levels"],[2,3])
        self.assertEqual(r["original_source_g8_terminals"],2)
        self.assertEqual(r["l2_outcome"],"party_scene_withdrawal")
        self.assertEqual(r["l3_outcome"],"sentry_defeat")
        self.assertTrue(r["no_L1_G8_replay"])
        self.assertEqual(len(r["l1_checks"]),3)
        self.assertTrue(all(x["gm_fixture_only"] for x in r["l1_checks"]))
        self.assertEqual({x["actor"] for x in r["l1_checks"]},
                         {"scholar","vanguard"})

    def test_02_two_distinct_milestones_in_source_order(self):
        r=self.report
        one,two=r["milestone_one"],r["milestone_two"]
        self.assertEqual((one["from_level"],one["to_level"]),(1,2))
        self.assertEqual((two["from_level"],two["to_level"]),(2,3))
        self.assertNotEqual(one["event_id"],two["event_id"])
        self.assertEqual((one["beat"],two["beat"]),("gate","shrine"))
        self.assertTrue(one["author_gm_fixture_only"])
        self.assertTrue(two["author_gm_fixture_only"])
        self.assertFalse(one["human_milestone_certified"])
        self.assertFalse(two["human_milestone_certified"])
        for name in ("vanguard","guardian","archer","scholar"):
            self.assertEqual(
                r["l3_final"][name]["milestones"],
                [one["event_id"],two["event_id"]])

    def test_03_award_never_refills_hp_vigor_ammunition_or_available_vp(self):
        r=self.report
        for before,after,receipt in (
                (r["l1_state"],r["l2_entry"],r["milestone_one"]),
                (r["l2_exit"],r["l3_entry"],r["milestone_two"])):
            self.assertTrue(receipt["recovery_deadlines_preserved"])
            for ident in before:
                for field in ("hp","vigor","vp_available","ammunition"):
                    self.assertEqual(after[ident][field],before[ident][field])
                self.assertEqual(
                    after[ident]["vp_spent"]-before[ident]["vp_spent"],
                    receipt["new_vp_capacity_staged_as_spent"][ident])
                self.assertEqual(after[ident]["vp_committed"],
                                 before[ident]["vp_committed"])

    def test_04_l1_noncombat_is_one_real_clock_without_combat_invention(self):
        r=self.report
        self.assertTrue(r["actual_source_g0_g4_narrative_ledger"])
        self.assertTrue(all(x["success"] for x in r["l1_checks"]))
        for ident in r["l1_state"]:
            self.assertEqual(r["l1_state"][ident]["level"],1)
        self.assertGreater(r["milestone_one"]["world_seconds"],0)
        self.assertEqual(r["l3_handoff"]["world_seconds"],
                         r["milestone_two"]["world_seconds"]+300)

    def test_05_actual_bow_arrow_and_prior_injury_survive_milestone(self):
        r=self.report
        self.assertEqual(r["l2_entry"]["archer"]["ammunition"],20)
        self.assertEqual(r["l2_exit"]["archer"]["ammunition"],19)
        self.assertEqual(r["l3_entry"]["archer"]["ammunition"],19)
        self.assertEqual(r["l3_final"]["archer"]["ammunition"],19)
        self.assertLess(r["l2_exit"]["vanguard"]["hp"],
                        r["l2_entry"]["vanguard"]["hp"])
        self.assertEqual(r["l3_entry"]["vanguard"]["hp"],
                         r["l2_exit"]["vanguard"]["hp"])

    def test_06_duplicate_or_skipped_milestones_rejected_atomically(self):
        for bad in ("not_gm","skips","repeat","wrong_beat"):
            with self.subTest(bad=bad):
                e,_=_l1()
                before=party_state(e)
                clock=deepcopy(e.g4.clock.events)
                ledger=canonical_digest(e.ledger)
                m=fixture_awards()[0]
                if bad=="not_gm": m["gm_declared"]=False
                if bad=="skips": m["to_level"]=3
                if bad=="repeat": e.actors["archer"].milestones.append(m["event_id"])
                if bad=="wrong_beat": m["beat"]="forest"
                with self.assertRaises(UnresolvedDecision):
                    award(e,m)
                self.assertEqual(e.g4.clock.events,clock)
                self.assertEqual(canonical_digest(e.ledger),ledger)
                if bad!="repeat":
                    self.assertEqual(party_state(e),before)

    def test_07_no_milestone_while_unresolved_poison_exists(self):
        e,_=_l1()
        e.g4.schedule_hemotoxin(
            "guardian",exposure_key="fixture:l1:legacy:poison",
            actual_exposure=True,resistance_total=1,wound_location_roll=9)
        before=party_state(e)
        t=deepcopy(e.g4.short_toxins)
        world=e.g4.clock.world_seconds
        with self.assertRaises(UnresolvedDecision):
            award(e,fixture_awards()[0])
        self.assertEqual(world,e.g4.clock.world_seconds)
        self.assertEqual(t,e.g4.short_toxins)
        self.assertEqual(before,party_state(e))

    def test_08_first_entry_rejects_unsourced_or_poisoned_narrative(self):
        e,_=_l1()
        with self.assertRaises(UnresolvedDecision):
            _entry_l2(e)  # No level-two GM award yet.
        award(e,fixture_awards()[0])
        e.g4.toxins.exposure_ids.add("GM:rejected-elsewhere")
        with self.assertRaises(UnresolvedDecision):
            _entry_l2(e)

    def test_09_second_award_needs_settled_original_g8_terminal(self):
        e,_=_l1()
        award(e,fixture_awards()[0])
        combat=_entry_l2(e)
        before=party_state(combat.e)
        with self.assertRaises(UnresolvedDecision):
            award(combat.e,fixture_awards()[1])
        self.assertEqual(party_state(combat.e),before)
        self.assertEqual(_l2_withdrawal(combat),"party_scene_withdrawal")
        m=award(combat.e,fixture_awards()[1])
        self.assertEqual(m["to_level"],3)

    def test_10_rejected_caller_milestone_cannot_claim_human_cert(self):
        m=fixture_awards()
        for key,value in (("gm_source","real_human_gm"),
                          ("automatic",True)):
            forged=deepcopy(m)
            forged[0][key]=value
            with self.subTest(field=key),self.assertRaises(
                    (UnresolvedDecision,ValueError)):
                run(awards=forged)

    def test_11_no_human_play_or_focus_exit_claims(self):
        r=self.report
        self.assertEqual((r["human_sessions"],
                          r["independently_certified_focuses"],
                          r["strict_mvp_exits_met"]),(0,0,0))
        self.assertEqual(r["source_scope"],
                         "author_gm_fixture_not_human_pilot")
        self.assertTrue(r["no_automatic_award"])


if __name__=="__main__":
    unittest.main()
