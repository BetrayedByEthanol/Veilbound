"""Original Alpha Low Priest A/B + High Scholar/Gifted + Medium Anointed L1–3.

Test-only GM milestones and tactical author fixtures are never human play.
"""
from copy import deepcopy
import unittest

from scripts.b04_b05_b06_alpha_l2_l3_progression_v0 import (
    run,attest,award,candidate_awards,_scene,_l1,_carry,_state,
    PARTY,FOCUSES,VERSION,
)
from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
from scripts.b06_world_clock_v0 import SIX_HOURS,ROUND_SECONDS_SURROGATE
from scripts.b04_b05_b06_alpha_mixed_native_v0 import scene as l1_source_scene
from scripts.b05_low_priest_life_l1_l3_v0 import profile as low_priest_profile


class AlphaProgressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=run(variant="A")
        cls.b=run(variant="B")

    def test_01_full_four_original_selected_sources_at_each_level(self):
        for variant,report in (("A",self.a),("B",self.b)):
            with self.subTest(variant=variant):
                self.assertEqual(report["version"],VERSION)
                self.assertEqual(report["source_focuses"],FOCUSES)
                self.assertEqual(report["session_plan_levels"],[1,2,2,3])
                self.assertEqual(set(report["l1_end"]),set(PARTY))
                for stage,key in ((1,"l1_end"),(2,"l2_start"),(3,"l3_start")):
                    for pc in PARTY:
                        self.assertEqual(report[key][pc]["level"],stage)
                    self.assertEqual(report[key]["priest"]["source_id"],variant)
                    self.assertEqual(report[key]["anointed"]["source_id"],"AM")
                    self.assertEqual(report[key]["gifted"]["source_id"],"G")
                    self.assertEqual(report[key]["scholar"]["source_id"],"F")
                self.assertEqual(report["source_adversaries"],
                                 {"L1":"B06-EN-02","L2":"B06-EN-03",
                                  "L3":"B06-EN-01"})
                self.assertEqual(report["native_source_stage_terminals"],3)

    def test_02_milestone_never_refills_hp_vigor_or_available_VP(self):
        for r in (self.a,self.b):
            for before,after,milestone in (
                (r["l1_end"],r["l2_post_award"],r["milestone_one"]),
                (r["l2_end"],r["l3_post_award"],r["milestone_two"])):
                self.assertTrue(milestone["no_HP_Vigor_available_VP_refill"])
                self.assertFalse(milestone["real_GM_attested"])
                for name in PARTY:
                    for value in ("hp","vigor","vp_available",
                                  "vp_committed","wounds","ammunition","wielded"):
                        self.assertEqual(before[name][value],after[name][value])
                    diff=after[name]["vp_spent"]-before[name]["vp_spent"]
                    self.assertEqual(diff,milestone["new_capacity_staged_spent"][name])
                    self.assertGreaterEqual(diff,0)
                    self.assertEqual(after[name]["level"],before[name]["level"]+1)
                    self.assertEqual(
                        after[name]["vp_available"]+after[name]["vp_committed"]
                        +after[name]["vp_spent"],
                        self._max_vp(r,name,after[name]["level"]))

    @staticmethod
    def _max_vp(r,pc,level):
        # Exact individual staged VP capacity comes from the original source
        # and receipts, never estimated with a generic Focus formula.
        states={1:r["l1_end"],2:r["l2_post_award"],3:r["l3_post_award"]}
        s=states[level][pc]
        initial=states[1][pc]
        inc=sum((r["milestone_one"]["new_capacity_staged_spent"].get(pc,0),
                 r["milestone_two"]["new_capacity_staged_spent"].get(pc,0))
                if level==3 else (
                r["milestone_one"]["new_capacity_staged_spent"].get(pc,0),)
                if level==2 else ())
        return (initial["vp_available"]+initial["vp_committed"]
                +initial["vp_spent"]+inc)

    def test_03_native_handoffs_preserve_carried_state_and_clock(self):
        for r in (self.a,self.b):
            self.assertEqual(r["l2_start"],r["l2_post_award"])
            self.assertEqual(r["l3_start"],r["l3_post_award"])
            for key in ("first_handoff","second_handoff"):
                receipt=r[key]
                self.assertEqual(receipt["source_party_sha256"],
                                 receipt["imported_party_sha256"])
                self.assertTrue(receipt["no_free_refill"])
                self.assertTrue(receipt["no_imported_foe_status"])
                self.assertEqual(receipt["elapsed_seconds"],300)
                self.assertEqual(len(receipt["pending_recovery_sha256"]),64)
            self.assertEqual(r["world_seconds"][0],r["first_handoff"]["world_seconds"])
            self.assertEqual(r["world_seconds"][1],r["second_handoff"]["world_seconds"])
            self.assertEqual(r["world_seconds"][0],300)
            self.assertGreaterEqual(r["world_seconds"][1],600)


    def test_12_L1_clock_enters_before_first_round_and_exits_after_terminal(self):
        for variant in ("A","B"):
            with self.subTest(variant=variant):
                combat=_l1(variant,0)
                e=combat.e
                self.assertEqual(e.round,2)
                self.assertEqual(e.g4.clock.mode,"exploration")
                self.assertIsNone(e.g4.clock.entry_round)
                self.assertEqual(e.g4.clock.world_seconds,0)
                names=[x["kind"] for x in e.ledger]
                self.assertEqual(names.count("g42_initiative_entered"),1)
                self.assertEqual(names.count("g42_initiative_exited"),1)
                self.assertEqual(names.count("g5_terminal_exit"),4)
                self.assertLess(
                    names.index("g42_initiative_entered"),
                    names.index("round_begin"))
                self.assertLess(
                    max(x["index"] for x in e.ledger
                        if x["kind"]=="round_end"),
                    names.index("g42_initiative_exited"))
                self.assertLess(
                    max(x["index"] for x in e.ledger
                        if x["kind"]=="g5_terminal_exit"),
                    names.index("g42_initiative_exited"))
                # Native G4.2 exit of a two-Round-Begin stage shortens
                # the pending six-hour due instant by 18 seconds.
                for name in (*PARTY,"foe"):
                    recovery=e.g4.clock.events[f"recovery:{name}:1"]
                    self.assertEqual(
                        recovery.due_seconds,
                        SIX_HOURS-3*ROUND_SECONDS_SURROGATE)
                    self.assertIsNone(recovery.due_round)

    def test_13_three_stage_native_recovery_deadlines_not_refilled(self):
        stages=(
            ("L1_after_two_rounds",3),
            ("L2_entry",3),
            ("L2_after_two_rounds",6),
            ("L3_entry",6),
            ("L3_after_two_rounds",9),
        )
        for variant,r in (("A",self.a),("B",self.b)):
            with self.subTest(variant=variant):
                snapshots=r["native_recovery_deadlines"]
                self.assertEqual(set(snapshots),{name for name,_ in stages})
                for stage,elapsed_surrogates in stages:
                    expected=SIX_HOURS-elapsed_surrogates*ROUND_SECONDS_SURROGATE
                    self.assertEqual(set(snapshots[stage]),set(PARTY))
                    for actor,receipt in snapshots[stage].items():
                        self.assertEqual(receipt["id"],f"recovery:{actor}:1")
                        self.assertEqual(receipt["due_seconds"],expected)
                self.assertEqual(
                    snapshots["L1_after_two_rounds"],
                    snapshots["L2_entry"])
                self.assertEqual(
                    snapshots["L2_after_two_rounds"],
                    snapshots["L3_entry"])
                self.assertEqual(
                    r["milestone_one"]["world_seconds"],0)
                self.assertEqual(
                    r["milestone_two"]["world_seconds"],300)

    def test_14_L1_clock_opt_in_preserves_old_standalone_witness(self):
        default_scene,_,_,_=l1_source_scene(variant="A",seed=0)
        self.assertEqual(default_scene.e.g4.clock.mode,"exploration")
        self.assertFalse(any(x["kind"]=="g42_initiative_entered"
                             for x in default_scene.e.ledger))
        native_scene,_,_,_=l1_source_scene(
            variant="A",seed=0,native_initiative_clock=True)
        self.assertEqual(native_scene.e.g4.clock.mode,"initiative")
        kinds=[x["kind"] for x in native_scene.e.ledger]
        self.assertLess(kinds.index("g42_initiative_entered"),
                        kinds.index("round_begin"))
        with self.assertRaises(ValueError):
            l1_source_scene(native_initiative_clock=1)

    def test_15_zero_travel_still_counts_all_three_native_encounters(self):
        for variant in ("A","B"):
            with self.subTest(variant=variant):
                r=run(variant=variant,travel_seconds=0)
                self.assertEqual(r["world_seconds"],[0,0,0])
                snapshots=r["native_recovery_deadlines"]
                for stage,seconds in (
                    ("L1_after_two_rounds",18),
                    ("L2_after_two_rounds",36),
                    ("L3_after_two_rounds",54)):
                    for n in PARTY:
                        self.assertEqual(
                            snapshots[stage][n]["due_seconds"],
                            SIX_HOURS-seconds)

    def test_04_real_hunter_head_front_original_bite_and_four_exits(self):
        for r in (self.a,self.b):
            l=r["source_evidence"]["L2"]["ledger"]
            self.assertEqual(r["l2_outcome"],"party_scene_withdrawal")
            rolls=[x for x in l if x["kind"]=="g5_melee_roll"]
            self.assertEqual(len(rolls),2)
            self.assertTrue(all(x["detail"]["profile"]=="B06-AT-04"
                                and x["detail"]["attacker"]=="foe"
                                and x["detail"]["target"]=="priest"
                                and x["detail"]["attack_face"]==1
                                for x in rolls))
            self.assertEqual(
                sum(x["kind"]=="g5_terminal_exit" for x in l),4)
            self.assertFalse(any(x["kind"].startswith("g44_") for x in l))
            self.assertEqual(r["source_evidence"]["L2"]["source_ids"]["foe"],
                             "B06-EN-03")

    def test_05_original_cold_sentry_chosen_reserve_paid_and_native_step(self):
        for r in (self.a,self.b):
            l=r["source_evidence"]["L3"]["ledger"]
            self.assertEqual(r["l3_outcome"],"party_scene_withdrawal")
            reserve=[x for x in l if x["kind"]=="g3_effect_established"
                     and x["detail"].get("effect_kind")=="Sentry Sword Reserve"]
            self.assertEqual(len(reserve),1)
            attacks=[x for x in l if x["kind"]=="g5_melee_roll"]
            self.assertEqual(len(attacks),1)
            self.assertEqual(attacks[0]["detail"]["profile"],"B06-AT-02")
            self.assertEqual(attacks[0]["detail"]["attack_face"],1)
            self.assertEqual(sum(x["kind"]=="g4_anointed_medium_returning_step_applied"
                                 for x in l),1)
            self.assertEqual(sum(x["kind"]=="b05_low_rite_established" for x in l),1)
            self.assertEqual(sum(x["kind"]=="b05_gifted_emotion_established" for x in l),1)
            self.assertEqual(sum(x["kind"]=="g5_terminal_exit" for x in l),4)

    def test_06_actual_l1_attrition_survives_L2_and_L3(self):
        for variant,r in (("A",self.a),("B",self.b)):
            pc="priest"
            self.assertLess(r["l1_end"][pc]["hp"],
                            low_priest_profile(variant,1)["hp_max"])
            self.assertEqual(r["l1_end"][pc]["hp"],r["l2_start"][pc]["hp"])
            self.assertEqual(r["l2_end"][pc]["hp"],r["l3_start"][pc]["hp"])
            self.assertGreater(r["l3_final"][pc]["hp"],r["l3_start"][pc]["hp"])
            for pc in PARTY:
                self.assertEqual(r["l3_final"][pc]["level"],3)
            self.assertEqual(r["human_sessions"],0)
            self.assertEqual(r["actual_GM_milestones_authenticated"],0)
            self.assertEqual(r["independently_certified_focuses"],0)
            self.assertEqual(r["strict_mvp_exits_met"],0)
            self.assertFalse(r["generalized_mixed_party_engine"])
            self.assertFalse(r["live_cross_level_effect_rebinding_supported"])

    def test_07_reject_forged_or_reused_milestones_without_play(self):
        valid=candidate_awards()
        for changed in (
            [valid[0],valid[0]],
            [dict(valid[0],gm_declared=False),valid[1]],
            [dict(valid[0],automatic=True),valid[1]],
            [dict(valid[0],gm_source="actual_human_gm"),valid[1]],
            [dict(valid[0],to_level=3),valid[1]],
            [dict(valid[0],beat="shrine"),valid[1]],
            [valid[1],valid[0]],
            [valid[0]],
        ):
            with self.subTest(changed=changed):
                with self.assertRaises(UnresolvedDecision):
                    run(awards=changed)

    def test_08_no_milestone_while_live_turn_or_unsourced_effect(self):
        combat=_l1("A",0)
        original=combat.e
        original.begin_round()
        with self.assertRaises(UnresolvedDecision):
            award(original,candidate_awards()[0],variant="A")
        # A clean historical L1 witness can advance exactly once.
        c=_l1("A",0)
        awarded=award(c.e,candidate_awards()[0],variant="A")
        self.assertEqual(awarded["to_level"],2)
        with self.assertRaises(UnresolvedDecision):
            award(c.e,candidate_awards()[0],variant="A")

    def test_09_unverified_destination_preflight_and_incomplete_gear(self):
        old=_l1("A",0)
        award(old.e,candidate_awards()[0],variant="A")
        new,_,_,_=_scene(2,"A","hunter",1)
        new.e.actors["priest"].vp_spent=1
        new.e.actors["priest"].vp_available-=1
        with self.assertRaises(UnresolvedDecision):
            _carry(old.e,new.e,travel_seconds=0,reference="forged")
        with self.assertRaises(ValueError):
            _carry(old.e,new.e,travel_seconds=-1,reference="forged")
        fresh,_,_,_=_scene(2,"B","hunter",1)
        with self.assertRaises(UnresolvedDecision):
            _carry(old.e,fresh.e,travel_seconds=0,reference="variant-substitution")

    def test_10_attestation_rejects_tampered_or_reshashed_receipts(self):
        for variant,r in (("A",self.a),("B",self.b)):
            self.assertEqual(attest(r,variant=variant)["digest"],r["digest"])
        bad=deepcopy(self.a)
        bad["l2_outcome"]="hunter_defeat"
        with self.assertRaises(AssertionError):
            attest(bad)
        bad=deepcopy(self.a)
        bad["source_evidence"]["L2"]["ledger"][0]["kind"]="fabricated"
        bad["source_evidence"]["L2"]["ledger_sha256"]=canonical_digest(
            bad["source_evidence"]["L2"]["ledger"])
        bad["digest"]=canonical_digest({k:v for k,v in bad.items() if k!="digest"})
        with self.assertRaises(AssertionError):
            attest(bad)

    def test_11_no_unbounded_travel_seed_or_level(self):
        for kw in (
            {"variant":"C"},{"seed":-1},{"seed":True},
            {"travel_seconds":-1},{"travel_seconds":21600},
            {"travel_seconds":True},
        ):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):
                    run(**kw)
        with self.assertRaises(ValueError):
            _scene(1,"A","hunter",1)
        with self.assertRaises(ValueError):
            _scene(2,"A","sentry_invalid",1)


if __name__=="__main__":
    unittest.main()
