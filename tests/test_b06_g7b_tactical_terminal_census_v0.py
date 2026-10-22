"""B06 G7-B: sourced Flame critical and R exit terminal regression suite."""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
from scripts import b06_g7a_native_terminal_census_v0 as g7a
from scripts import b06_g7b_tactical_terminal_census_v0 as g7b


def scholar_turn():
    c=mixed_scene(level=3,size=4,seed=9901)
    for _ in range(4):
        c.bridge.start_next_turn(RegenerationChoice())
        c.bridge.end_current_turn()
    c.bridge.start_next_turn(RegenerationChoice())
    assert c.e.current=="scholar"
    return c


class G7BTests(unittest.TestCase):
    def test_01_critical_direct_flame_is_one_paid_fire_hit_and_one_vigor_packet(self):
        c=scholar_turn()
        e=c.e
        before=e.actors["hunter"]
        hp,vigor,vp=before.hp,before.vigor,e.actors["scholar"].vp_available
        result=e.g3.cast_flame(
            "scholar","hunter",tier=1,face=20,vigor_die=3,
            confirmation_face=10,critical_dice=(2,3),
            hand_available=True,target_cell=e.g1.body_cell("hunter","head"),
            wound_location_roll=8)
        self.assertEqual(result["outcome"],"direct_hit_resolved_G4")
        self.assertEqual(result["packets_pending_g4"]["fire_hp"],7)
        self.assertEqual(result["g4_damage"]["hp_loss"],7)
        self.assertEqual(e.actors["hunter"].hp,hp-7)
        self.assertEqual(e.actors["hunter"].vigor,vigor-3)
        self.assertEqual(e.actors["scholar"].vp_available,vp-2)
        sources=[x for x in e.ledger if x["kind"]=="g3_flame_launched"]
        self.assertEqual(len(sources),1)
        self.assertEqual(sources[0]["detail"]["critical"],"critical")
        self.assertEqual(sources[0]["detail"]["critical_dice"],[2,3])
        damages=[x for x in e.ledger if x["kind"]=="g4_damage_applied"]
        self.assertEqual(len(damages),1)
        self.assertEqual(damages[0]["detail"]["event_key"],
                         f"g3-flame-ledger:{sources[0]['index']}")
        self.assertEqual(len(damages[0]["detail"]["packets"]),2)
        self.assertEqual(damages[0]["detail"]["packets"][0]["raw"],7)
        self.assertEqual(damages[0]["detail"]["packets"][1]["raw"],3)

    def test_02_devastating_direct_flame_creates_above_zero_wound(self):
        c=scholar_turn()
        e=c.e
        result=e.g3.cast_flame(
            "scholar","hunter",tier=1,face=20,vigor_die=2,
            confirmation_face=20,critical_dice=(1,1),
            hand_available=True,target_cell=e.g1.body_cell("hunter","head"),
            wound_location_roll=8)
        self.assertEqual(result["outcome"],"direct_hit_resolved_G4")
        self.assertEqual(result["g4_damage"]["wound"],"Critical")
        self.assertGreater(e.actors["hunter"].hp,0)
        self.assertEqual(len(e.actors["hunter"].wounds),1)
        self.assertEqual(e.actors["hunter"].wounds[0].severity,"Critical")

    def test_03_failed_nat20_confirmation_is_strong_against_dodge(self):
        c=scholar_turn()
        e=c.e
        out=e.g3.cast_flame(
            "scholar","hunter",tier=1,face=20,vigor_die=2,
            defense="dodge",aware=True,confirmation_face=1,
            critical_dice=(3,),hand_available=True,
            target_cell=e.g1.body_cell("hunter","head"),
            wound_location_roll=7)
        self.assertEqual(out["outcome"],"direct_hit_resolved_G4")
        self.assertEqual(out["packets_pending_g4"]["fire_hp"],5)
        self.assertEqual([v["detail"]["critical"] for v in e.ledger
                          if v["kind"]=="g3_flame_launched"],["strong"])

    def test_04_legacy_nat20_remains_pending_and_does_not_deal_damage(self):
        c=scholar_turn()
        e=c.e
        prior=e.actors["hunter"].hp
        result=e.g3.cast_flame(
            "scholar","hunter",tier=1,face=20,vigor_die=3,
            hand_available=True,target_cell=e.g1.body_cell("hunter","head"))
        self.assertEqual(result["outcome"],"critical_confirmation_pending_G5")
        self.assertEqual(e.actors["hunter"].hp,prior)
        self.assertFalse(any(v["kind"]=="g4_damage_applied" for v in e.ledger))

    def test_05_bad_confirmation_or_critical_dice_precommit_no_payment(self):
        args=[
            {"face":20,"confirmation_face":21,"critical_dice":(2,3)},
            {"face":20,"confirmation_face":1,"critical_dice":(2,3)},
            {"face":20,"confirmation_face":10,"critical_dice":(0,3)},
            {"face":12,"confirmation_face":10,"critical_dice":(2,3)},
            {"face":12,"critical_dice":(1,)},
        ]
        for kwargs in args:
            with self.subTest(args=kwargs):
                c=scholar_turn()
                e=c.e
                ap=e.actors["scholar"].ap_remaining
                vp=e.actors["scholar"].vp_available
                with self.assertRaises(ValueError):
                    e.g3.cast_flame(
                        "scholar","hunter",tier=1,vigor_die=3,
                        hand_available=True,
                        target_cell=e.g1.body_cell("hunter","head"),
                        **kwargs)
                self.assertEqual(e.actors["scholar"].ap_remaining,ap)
                self.assertEqual(e.actors["scholar"].vp_available,vp)
                self.assertFalse(any(x["kind"]=="g3_flame_launched"
                                     for x in e.ledger))

    def test_06_devastating_requires_real_wound_location_before_payment(self):
        c=scholar_turn()
        e=c.e
        ap=e.actors["scholar"].ap_remaining
        vp=e.actors["scholar"].vp_available
        with self.assertRaises(UnresolvedDecision):
            e.g3.cast_flame(
                "scholar","hunter",tier=1,face=20,vigor_die=1,
                confirmation_face=20,critical_dice=(2,2),
                hand_available=True,target_cell=e.g1.body_cell("hunter","head"))
        self.assertEqual(e.actors["scholar"].ap_remaining,ap)
        self.assertEqual(e.actors["scholar"].vp_available,vp)

    def test_07_no_extra_fire_critical_on_vigor_and_one_g4_event(self):
        t=g7b.native_case(2,4,35,policy="g7b_flame",include_ledger=True)
        ledger=t["ledger"]
        self.assertEqual(t["ledger_sha256"],g7b.canonical_digest(ledger))
        for i,ev in enumerate(ledger):
            if ev["kind"]!="g3_flame_launched" or not ev["detail"].get("critical"):
                continue
            d=ev["detail"]
            self.assertEqual(d["packets_pending_g4"]["fire_hp"],
                             2+sum(d["critical_dice"]))
            pairs=[x for x in ledger
                   if x["kind"]=="g4_damage_applied" and
                   x["detail"]["event_key"]==f"g3-flame-ledger:{i}"]
            self.assertEqual(len(pairs),1)
            self.assertEqual(pairs[0]["detail"]["packets"][0]["raw"],
                             d["packets_pending_g4"]["fire_hp"])
            self.assertEqual(pairs[0]["detail"]["packets"][1]["raw"],
                             d["packets_pending_g4"]["vigor"])

    def test_08_policy_modes_leave_old_g7a_fixed_census_intact(self):
        a=g7a.run_trial(2,4,30)
        b=g7a.run_trial(2,4,30,policy_mode="g7a")
        self.assertEqual(a,b)
        self.assertTrue(a["policy_id"].startswith("G7A-"))
        self.assertNotIn("archer_withdrawal_attested",g7a.OUTCOMES)

    def test_09_actual_archer_exit_attested_after_native_paid_grid_step(self):
        for level,size in g7a.ALLOWED:
            with self.subTest(level=level,size=size):
                result=g7b.native_case(
                    level,size,0,policy="g7b_archer_exit",include_ledger=True)
                self.assertEqual(result["outcome"],"archer_withdrawal_attested")
                self.assertFalse(result["sample_is_complete_encounter"])
                self.assertTrue(result["one_party_member_exit_only"])
                self.assertEqual(result["final_state"]["archer"]["occupied"],[[0,4]])
                events=result["ledger"]
                g1=[x for x in events if x["kind"]=="g1_movement_step"
                    and x["detail"].get("actor")=="archer"]
                g45=[x for x in events if x["kind"]=="g45_withdrawal_attested"
                     and x["detail"].get("actor")=="archer"]
                g5=[x for x in events if x["kind"]=="g5_terminal_exit"
                    and x["detail"].get("actor")=="archer"]
                self.assertEqual(len(g1),1)
                self.assertEqual(len(g45),1)
                self.assertEqual(len(g5),1)
                self.assertEqual(g1[0]["index"],g5[0]["detail"]["movement_index"])
                self.assertEqual(g1[0]["index"],g45[0]["detail"]["movement_event_index"])
                self.assertEqual(g1[0]["detail"]["new"],[[0,4]])
                self.assertEqual(result["rounds_completed"],1)
                self.assertEqual(result["turns_completed"],size+1)

    def test_10_no_exit_without_original_scene_policy(self):
        c=mixed_scene(size=3,level=2,seed=0)
        with self.assertRaises(UnresolvedDecision):
            c.withdraw("archer")

    def test_11_no_exit_for_wrong_actor_even_in_authored_scene(self):
        c=mixed_scene(size=3,level=2,seed=0,archer_exit=True)
        with self.assertRaises(UnresolvedDecision):
            c.withdraw("vanguard")

    def test_12_no_exit_without_actual_grid_movement(self):
        c=mixed_scene(size=3,level=2,seed=0,archer_exit=True)
        with self.assertRaises(UnresolvedDecision):
            c.withdraw("archer")

    def test_13_g7b_flame_only_never_claims_archer_exit(self):
        for level,size in g7a.ALLOWED:
            t=g7b.native_case(level,size,0,policy="g7b_flame")
            self.assertNotEqual(t["outcome"],"archer_withdrawal_attested")
            self.assertFalse(t["one_party_member_exit_only"])

    def test_14_g7b_census_all_eight_cells_and_exclusive_counts(self):
        report=g7b.census(8,start_seed=0,include_trials=False)
        self.assertEqual(len(report["cases"]),8)
        self.assertEqual(len({(x["scenario_id"],x["policy"])
                              for x in report["cases"]}),8)
        self.assertEqual(report["complete_party_packs_certified"],0)
        self.assertIsNone(report["creature_challenge_rating"])
        for case in report["cases"]:
            self.assertEqual(sum(case["counts"].values()),8)
            self.assertEqual(set(case["counts"]),set(g7b.OUTCOMES))
            self.assertEqual(len(case["trials_digest"]),8)
            self.assertEqual(case["actual_party_withdrawals"],0)
            self.assertIsNone(case["sampled_win_rate"])
            self.assertIsNone(case["ci95"])
            self.assertIsNone(case["hunter_cr"])
            self.assertEqual(
                sum(case["unresolved_reasons"].values()),
                case["counts"]["unresolved_mechanical_branch"])

    def test_15_128_seed_fully_accounted_without_promotion_to_win_rates(self):
        report=g7b.census(128,include_trials=False)
        self.assertEqual(len(report["cases"]),8)
        for case in report["cases"]:
            self.assertEqual(case["seed_count"],128)
            self.assertEqual(sum(case["counts"].values()),128)
            self.assertEqual(len(case["trials_digest"]),128)
            self.assertEqual([x["seed"] for x in case["trials_digest"]],
                             list(range(128)))
            self.assertEqual(
                case["incomplete_or_single_exit"],
                case["counts"]["legal_window_cutoff"]+
                case["counts"]["unresolved_mechanical_branch"]+
                case["counts"]["archer_withdrawal_attested"])
            self.assertIsNone(case["sampled_win_rate"])

    def test_16_invalid_policy_and_sample_bounds_fail_before_execution(self):
        for policy in ("g7a","g7b_prepared","g7b_body",None,""):
            with self.subTest(policy=policy):
                with self.assertRaises(ValueError):
                    g7b.native_case(2,3,0,policy=policy)
        for values in ({"seeds":0},{"seeds":True},{"seeds":129},
                       {"start_seed":-1},{"max_rounds":4},
                       {"include_trials":0}):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    g7b.census(**values)

    def test_17_G7B_report_digest_deterministic_and_phase3_frozen(self):
        first=g7b.census(2,start_seed=4,include_trials=False)
        second=g7b.census(2,start_seed=4,include_trials=False)
        self.assertEqual(first,second)
        self.assertEqual(g7b.canonical_digest(first),g7b.canonical_digest(second))
        self.assertEqual(first["historical_phase3_sha256"],
                         g7b.FROZEN_PHASE3_SHA256)
        self.assertTrue(first["historical_phase3_not_recomputed"])

    def test_18_G7B_cli_json_has_correct_digest_and_no_CI_claim(self):
        output=StringIO()
        with redirect_stdout(output):
            g7b.main(["--seeds","1"])
        parsed=json.loads(output.getvalue())
        key=parsed.pop("census_sha256")
        self.assertEqual(key,g7b.canonical_digest(parsed))
        self.assertIsNone(parsed["creature_challenge_rating"])


if __name__=="__main__":
    unittest.main()
