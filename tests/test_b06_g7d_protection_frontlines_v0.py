"""B06 G7-D: native G6-D protection inside multi-round mixed-party play."""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from scripts.b06_encounter_state_v0 import RegenerationChoice,UnresolvedDecision
from scripts.b06_hunter_mixed_party_g6c_v0 import (
    mixed_scene, HUNTER_HEAD, LOCATIONS,
)
from scripts.b06_hunter_reactive_intervene_g6d_v0 import ReactiveHunterProtection
from scripts.b06_g7a_native_terminal_census_v0 import (
    run_trial as g7a_case, canonical_digest,
)
from scripts.b06_g7b_tactical_terminal_census_v0 import native_case as g7b_case
from scripts.b06_g7c_party_terminals_v0 import run_trial as g7c_case
from scripts import b06_g7d_protection_frontlines_v0 as g7d


class G7DTests(unittest.TestCase):
    def test_01_seven_strictly_scoped_policy_cells(self):
        self.assertEqual(len(g7d.CELLS),7)
        self.assertEqual(set(g7d.CELLS),{
            (3,4,"control"),(3,4,"reactive_shield"),
            (3,4,"prepared_body"),(2,3,"b_front"),
            (2,4,"b_front"),(3,3,"b_front"),(3,4,"b_front")})

    def test_02_B_front_is_actual_source_B_at_hunter_head(self):
        for size in (3,4):
            for level in (2,3):
                with self.subTest(size=size,level=level):
                    c=mixed_scene(size=size,level=level,seed=41,
                                  frontline="B_head_forward")
                    e=c.e
                    self.assertEqual(e.g1.front("hunter"),
                                     e.actors["guardian"].occupied[0])
                    self.assertEqual(e.actors["vanguard"].occupied,
                                     (LOCATIONS["guardian"],))
                    self.assertEqual(e.actors["guardian"].occupied,
                                     (LOCATIONS["vanguard"],))
                    self.assertTrue(e.g1.melee_contact(
                        "hunter","guardian",hunter_front=True))
                    self.assertTrue(e.g1.melee_contact("vanguard","hunter"))
                    self.assertFalse(e.g1.melee_contact(
                        "hunter","vanguard",hunter_front=True))
                    self.assertEqual(e.order,
                        ("hunter","vanguard","guardian","archer")+
                        (("scholar",) if size==4 else ()))
                    e.check()

    def test_03_alternate_front_attack_targets_B_with_real_source_hit(self):
        for level,size,_ in g7d.CELLS[3:]:
            with self.subTest(level=level,size=size):
                r=g7d.run_trial(level,size,0,policy="b_front",
                                include_ledger=True)
                self.assertEqual(r["frontline"],"B_head_forward")
                sources=[x for x in r["ledger"]
                         if x["kind"]=="g5_melee_roll"
                         and x["detail"].get("attacker")=="hunter"]
                self.assertTrue(sources)
                self.assertEqual({x["detail"]["target"] for x in sources},
                                 {"guardian"})
                self.assertEqual(r["protection"]["attested_protections"],0)
                self.assertFalse(r["complete_party_pack_certified"])
                self.assertIsNone(r["hunter_cr"])

    def test_04_reactive_shield_has_a_real_g0_reaction_and_G5_source(self):
        found=False
        for seed in range(32):
            r=g7d.run_trial(3,4,seed,policy="reactive_shield",
                            include_ledger=True)
            for event in r["ledger"]:
                if event["kind"]!="g6d_protective_bite_attested":
                    continue
                found=True
                d=event["detail"]
                self.assertEqual(d["method"],"shield_guard")
                self.assertEqual(d["activation"],"reactive")
                self.assertIsNotNone(d["reaction_index"])
                self.assertIsNone(d["interception_index"])
                receipt=r["ledger"][d["reaction_index"]]
                self.assertEqual(receipt["kind"],"spontaneous_committed")
                self.assertEqual(receipt["detail"]["actor"],"guardian")
                if d["original_hit"]:
                    self.assertIsNotNone(d["shield_defense_index"])
                    self.assertEqual(
                        r["ledger"][d["shield_defense_index"]]["kind"],
                        "defense_assigned")
                self.assertFalse(r["complete_party_pack_certified"])
            if found:
                break
        self.assertTrue(found,"G7-D requires a positive native Reactive witness")

    def test_05_prepared_body_uses_reserved_MP_and_not_reaction(self):
        found=False
        for seed in range(64):
            r=g7d.run_trial(3,4,seed,policy="prepared_body",
                            include_ledger=True)
            for event in r["ledger"]:
                if event["kind"]!="g6d_protective_bite_attested":
                    continue
                found=True
                d=event["detail"]
                self.assertEqual(d["activation"],"prepared")
                self.assertEqual(d["method"],"body_take_hit")
                self.assertIsNone(d["reaction_index"])
                self.assertIsNotNone(d["interception_index"])
                self.assertEqual(event["round"],2)
                release=r["ledger"][d["interception_index"]]
                self.assertEqual(release["kind"],"interception_released")
                self.assertEqual(release["detail"]["actor"],"guardian")
                prep=[v for v in r["ledger"]
                      if v["kind"]=="g6d_prepared_protection_reserved"]
                arrived=[v for v in r["ledger"]
                         if v["kind"]=="g6d_prepared_protection_arrived"]
                self.assertEqual(len(prep),1)
                self.assertEqual(len(arrived),1)
                self.assertLess(prep[0]["index"],release["index"])
                self.assertLess(release["index"],arrived[0]["index"])
                self.assertEqual(arrived[0]["detail"]["mp_spent"],2)
                self.assertEqual(r["protection"]["prepared_uses"],1)
            if found:
                break
        self.assertTrue(found,"G7-D requires a positive native Prepared witness")

    def test_06_preserves_original_A_front_source_geometry(self):
        c=mixed_scene(level=3,size=4,seed=22)
        self.assertEqual(c.e.g1.front("hunter"),LOCATIONS["vanguard"])
        self.assertEqual(c.e.actors["guardian"].occupied,(LOCATIONS["guardian"],))
        self.assertEqual(c.e.g1.scene_id,"G6C-clear-mixed-front")
        self.assertEqual(c.e.scenario,"B06-I3-G6C:party-4:L3")

    def test_07_B_front_protection_cannot_impersonate_A_ward_B_guardian(self):
        c=mixed_scene(level=3,size=4,seed=23,
                      frontline="B_head_forward")
        e=c.e
        c.bridge.start_next_turn(RegenerationChoice())
        seq=c.declare("hunter","guardian",
                      profiles=("B06-AT-04",),defenses=("dodge",))
        with self.assertRaises(UnresolvedDecision):
            ReactiveHunterProtection(c).resolve(
                seq,protector_id="vanguard",method="shield_guard",
                attack_face=12)
        self.assertEqual(sum(x["kind"]=="g6d_protective_bite_attested"
                             for x in e.ledger),0)

    def test_08_B_front_withdrawal_modes_are_not_retroactively_enabled(self):
        for params in ({"party_exits":True},{"archer_exit":True}):
            with self.subTest(params=params):
                with self.assertRaises(ValueError):
                    mixed_scene(size=4,level=3,seed=22,
                                frontline="B_head_forward",**params)

    def test_09_no_new_roles_or_unsupported_protection_on_other_sources(self):
        for level,size,policy in (
                (2,3,"reactive_shield"),(2,4,"prepared_body"),
                (3,3,"reactive_shield"),(2,3,"control"),
                (3,4,"body_protect_B"),(3,4,"ambush")):
            with self.subTest(level=level,size=size,policy=policy):
                with self.assertRaises(ValueError):
                    g7d.run_trial(level,size,0,policy=policy)

    def test_10_all_native_tactical_evidence_has_replay_digest(self):
        for level,size,policy in g7d.CELLS:
            with self.subTest(cell=(level,size,policy)):
                r=g7d.run_trial(level,size,3,policy=policy,
                                include_ledger=True)
                self.assertEqual(r["ledger_sha256"],
                                 canonical_digest(r["ledger"]))
                self.assertIn(r["outcome"],g7d.OUTCOMES)
                self.assertLessEqual(r["rounds_completed"],2)
                self.assertEqual(r["initial_state"]["hunter"]["occupied"],
                                 [[3,2],[4,2]])
                self.assertIsNone(r["hunter_cr"])

    def test_11_g7a_baseline_is_still_deterministic(self):
        self.assertEqual(g7a_case(2,4,30),g7a_case(2,4,30))
        self.assertTrue(g7a_case(2,4,30)["policy_id"].startswith("G7A-"))

    def test_12_g7b_archer_individual_exit_remains_only_one_exit(self):
        old=g7b_case(2,3,0,policy="g7b_archer_exit")
        self.assertEqual(old["outcome"],"archer_withdrawal_attested")
        self.assertTrue(old["one_party_member_exit_only"])

    def test_13_g7c_party_withdrawal_remains_separately_certified(self):
        r=g7c_case(2,3,0)
        self.assertEqual(r["outcome"],"party_withdrawal_attested")
        self.assertIsNotNone(r["native_terminal"])

    def test_14_128_seed_census_counts_all_seven_policy_cohorts(self):
        report=g7d.census(128)
        self.assertEqual(len(report["cells"]),7)
        for cell in report["cells"]:
            self.assertEqual(sum(cell["counts"].values()),128)
            self.assertEqual(len(cell["trial_digests"]),128)
            self.assertEqual([x["seed"] for x in cell["trial_digests"]],
                             list(range(128)))
            self.assertIsNone(cell["sampled_win_rate"])
            self.assertIsNone(cell["hunter_cr"])
            self.assertEqual(cell["complete_party_packs_certified"],0)
        self.assertEqual(report["complete_party_packs_certified"],0)
        self.assertIsNone(report["creature_challenge_rating"])
        self.assertEqual(report["historical_phase3_sha256"],g7d.PHASE3_SHA)
        self.assertTrue(report["historical_phase3_not_recomputed"])

    def test_15_ledger_replay_and_report_hash_deterministic(self):
        first=g7d.census(2,start_seed=31,include_trials=True)
        again=g7d.census(2,start_seed=31,include_trials=True)
        self.assertEqual(first,again)
        self.assertEqual(canonical_digest(first),canonical_digest(again))

    def test_16_cli_json_digest_is_valid(self):
        out=StringIO()
        with redirect_stdout(out):
            g7d.main(["--seeds","1","--rounds","1"])
        raw=json.loads(out.getvalue())
        digest=raw.pop("census_sha256")
        self.assertEqual(digest,canonical_digest(raw))

    def test_17_input_bounds_fail_before_constructing_any_encounter(self):
        for options in ({"seeds":True},{"seeds":0},{"seeds":129},
                        {"start_seed":-1},{"round_limit":3},
                        {"include_trials":None}):
            with self.subTest(options=options):
                with self.assertRaises(ValueError):
                    g7d.census(**options)
        for kwargs in ({"seed":-1},{"seed":True},{"round_limit":0},
                       {"round_limit":3},{"include_ledger":1}):
            with self.subTest(kwargs=kwargs):
                valid={"level":3,"size":4,"seed":0,
                       "policy":"reactive_shield"}
                valid.update(kwargs)
                with self.assertRaises(ValueError):
                    g7d.run_trial(**valid)

    def test_18_control_and_protection_share_hunter_primary_roll(self):
        a=g7d.run_trial(3,4,30,policy="control",include_ledger=True)
        b=g7d.run_trial(3,4,30,policy="reactive_shield",include_ledger=True)
        def faces(report):
            return [(x["round"],x["detail"]["attack_face"])
                    for x in report["ledger"]
                    if x["kind"]=="g5_melee_roll"
                    and x["detail"].get("attacker")=="hunter"]
        self.assertTrue(faces(a))
        self.assertEqual(faces(a),faces(b))

    def test_19_outcomes_never_imply_party_defeat_or_full_withdrawal(self):
        report=g7d.census(8)
        self.assertNotIn("party_withdrawal_attested",g7d.OUTCOMES)
        for cell in report["cells"]:
            self.assertNotIn("party_withdrawal_attested",cell["counts"])
            self.assertEqual(cell["counts"]["party_defeat_observed"],0)
            self.assertIsNone(cell["sampled_win_rate"])

    def test_20_no_implicit_ambush_geometry_or_hunter_CR(self):
        for cell in g7d.census(2)["cells"]:
            self.assertIn("warned_clear",cell["scenario_id"])
            self.assertIsNone(cell["hunter_cr"])
        self.assertEqual(g7d.MAX_ROUNDS,2)


if __name__=="__main__":
    unittest.main()
