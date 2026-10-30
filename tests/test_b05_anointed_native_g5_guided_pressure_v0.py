"""Bounded Anointed L3 source-paid Guided + true Soldier/Sentry G5 pressure."""
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.b05_anointed_native_g5_guided_pressure_v0 import (
    FOCUSES, MODES, OPPONENTS, POLICIES, attest_policy, run_matrix, run_policy,
)
from scripts.b05_anointed_native_defensive_encounter_v0 import (
    run_policy as source_g5_baseline, scene,
)
from scripts.b05_anointed_native_guided_authority_v0 import AnointedGuidedAuthority
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def rows(r,kind):
    return [e for e in r["ledger"] if e["kind"]==kind]


class GuidedG5PressureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports=run_matrix(seed=0)
        cls.by_case={(r["focus"],r["opponent"],r["mode"],r["policy"]):r
                     for r in cls.reports}

    def test_01_exact_twenty_four_source_policies_without_focus_certification(self):
        self.assertEqual(24,len(self.reports))
        self.assertEqual(24,len(self.by_case))
        self.assertEqual(24,len(FOCUSES)*len(OPPONENTS)*len(MODES)*len(POLICIES))
        for r in self.reports:
            self.assertEqual(3,r["level"])
            self.assertIs(r["independent_focus_certified"],False)
            self.assertIs(r["representative_play_certified"],False)
            self.assertIsNone(r["sampled_win_rate"])

    def test_02_one_paid_source_g5_attack_and_true_damage_for_every_policy(self):
        for r in self.reports:
            with self.subTest(r=(r["focus"],r["opponent"],r["mode"],r["policy"])):
                m=r["metrics"]
                self.assertEqual((1,1,1,2),
                    (m["g0_enemy_paid_actions"],m["g5_hit_events"],
                     m["g4_damage_events"],m["g0_recipient_regeneration_steps"]))
                seq=rows(r,"g5_melee_sequence_attested")
                hit=rows(r,"g5_melee_resolved")
                dmg=rows(r,"g4_damage_applied")
                self.assertEqual((1,1,1),(len(seq),len(hit),len(dmg)))
                self.assertEqual("hit",hit[0]["detail"]["outcome"])
                self.assertEqual("foe",hit[0]["detail"]["attacker"])
                self.assertEqual({"soldier":"B06-EN-02",
                                  "sentry_prepared":"B06-EN-01"}[r["opponent"]],
                                 r["source_ids"]["foe"])
                self.assertEqual({"High":"AH","Medium":"AM","Low":"AL"}[r["focus"]],
                                 r["source_ids"]["anointed"])
                self.assertFalse(m["recipient_dead"])
                self.assertEqual(0,m["recipient_wound_count"])

    def test_03_g0_projection_and_real_g3_host_payment_per_focus_and_mode(self):
        for r in self.reports:
            with self.subTest(r=(r["focus"],r["opponent"],r["mode"],r["policy"])):
                m=r["metrics"]
                host=rows(r,"b05_anointed_guided_host_established")
                self.assertEqual(1,len(host))
                h=host[0]["detail"]
                ap={"High":20,"Medium":24,"Low":30}[r["focus"]]
                self.assertEqual(ap,m["guided_host_activation_ap"])
                self.assertEqual(ap,h["ap_spent"])
                self.assertEqual(r["mode"],h["mode"])
                self.assertEqual(r["source_digests"]["anointed"],h["source_digest"])
                self.assertEqual(h["host"],m["guided_host"])
                self.assertEqual(h["ap_index"],m["guided_host_ap_index"])
                self.assertEqual(h["vp_index"],m["guided_host_vp_index"])
                action=r["ledger"][h["ap_index"]]
                payment=r["ledger"][h["vp_index"]]
                self.assertEqual("action_committed",action["kind"])
                self.assertEqual("vp_transition",payment["kind"])
                self.assertEqual("projection",action["detail"]["action_class"])
                self.assertEqual(ap,action["detail"]["ap_spent"])
                self.assertEqual(2,payment["detail"]["points"])
                self.assertEqual("spent" if r["mode"]=="fixed" else "committed",
                                 payment["detail"]["mode"])
                self.assertEqual(2 if r["mode"]=="fixed" else 0,
                                 m["guided_host_spent_vp"])
                self.assertEqual(2 if r["mode"]=="maintained" else 0,
                                 m["guided_host_committed_vp"])
                self.assertEqual(m["guided_host_spent_vp"],
                                 m["anointed_vp_spent"])
                self.assertEqual(m["guided_host_committed_vp"],
                                 m["anointed_vp_committed"])

    def test_04_warranted_focus_turn_timing_and_medium_vessel_action(self):
        for r in self.reports:
            focus=r["focus"]
            events=rows(r,"b05_anointed_guided_host_established")
            self.assertEqual(1,len(events))
            host=events[0]
            hit=rows(r,"g5_melee_resolved")[0]
            if focus=="High":
                self.assertEqual(1,host["round"])
                self.assertLess(host["index"],hit["index"])
            else:
                self.assertGreater(host["index"],hit["index"])
                self.assertEqual(2 if focus=="Medium" else 1,host["round"])
            if focus=="Medium":
                invests=[v for v in rows(r,"action_committed")
                         if v["detail"].get("label")=="anointed:medium:investment"]
                self.assertEqual(1,len(invests))
                self.assertEqual(24,invests[0]["detail"]["ap_spent"])
                self.assertEqual(1,invests[0]["round"])
                self.assertLess(invests[0]["index"],host["index"])
            else:
                self.assertFalse(any(v["detail"].get("label")=="anointed:medium:investment"
                                     for v in rows(r,"action_committed")))

    def test_05_real_natural_g4_regen_cost_is_not_waived_by_guided_lesser(self):
        for r in self.reports:
            m=r["metrics"]
            self.assertEqual([1,2],m["recipient_regen_step_rounds"])
            self.assertEqual((1,1),(m["ordinary_hp_restored"],
                                    m["ordinary_regen_recipient_vigor_spent"]))
            natural=[v for v in rows(r,"regeneration_step")
                     if v["detail"]["actor"]==m["recipient"]]
            self.assertEqual([0,1],[v["detail"]["hp_restored"] for v in natural])
            self.assertEqual([0,1],[v["detail"]["throughput_spent"] for v in natural])
            self.assertEqual([0,0],[v["detail"]["repair_points"] for v in natural])
            hit=rows(r,"g5_melee_resolved")[0]
            self.assertLess(hit["index"],natural[0]["index"])
            self.assertLess(natural[0]["index"],natural[1]["index"])
            self.assertFalse(rows(r,"g4_anointed_returning_step_applied"))
            self.assertFalse(rows(r,"g4_anointed_medium_returning_step_applied"))
            self.assertFalse(rows(r,"g4_anointed_low_returning_step_applied"))

    def test_06_only_lesser_grants_one_post_step_hp_from_finite_destiny(self):
        for focus in FOCUSES:
            for opponent in OPPONENTS:
                for mode in MODES:
                    base=self.by_case[focus,opponent,mode,"ordinary_guided"]
                    lesser=self.by_case[focus,opponent,mode,"lesser_guided"]
                    a,b=base["metrics"],lesser["metrics"]
                    with self.subTest(focus=focus,opponent=opponent,mode=mode):
                        self.assertEqual((0,0,2),(a["guided_waiver_count"],
                                                 a["guided_additional_hp"],
                                                 a["anointed_destiny_remaining"]))
                        self.assertEqual((1,1,1),(b["guided_waiver_count"],
                                                 b["guided_additional_hp"],
                                                 b["anointed_destiny_remaining"]))
                        self.assertEqual(1,b["guided_destiny_spent"])
                        self.assertEqual(0,a["guided_destiny_spent"])
                        self.assertEqual(a["recipient_hp"]+1,b["recipient_hp"])
                        self.assertEqual(a["recipient_vigor"],b["recipient_vigor"])
                        self.assertEqual(a["anointed_vp_spent"],b["anointed_vp_spent"])
                        self.assertEqual(a["anointed_vp_committed"],b["anointed_vp_committed"])
                        self.assertEqual(a["ordinary_regen_recipient_vigor_spent"],
                                         b["ordinary_regen_recipient_vigor_spent"])
                        waiver=rows(lesser,"g4_anointed_guided_waiver_applied")
                        self.assertEqual(1,len(waiver))
                        self.assertEqual(2,waiver[0]["round"])
                        self.assertEqual(0,waiver[0]["detail"]["recipient_vigor_spent"])
                        self.assertEqual(1,waiver[0]["detail"]["destiny_cost"])
                        self.assertEqual(b["guided_host"],waiver[0]["detail"]["host"])
                        self.assertLess(b["recipient_regen_step_indices"][1],
                                        waiver[0]["index"])

    def test_07_source_g5_baseline_has_same_hit_and_no_guided_for_free(self):
        for opponent in OPPONENTS:
            for focus in FOCUSES:
                r=self.by_case[focus,opponent,"maintained","ordinary_guided"]
                base=source_g5_baseline(focus=focus,level=3,opponent=opponent,
                                        policy="baseline",seed=0)
                self.assertEqual(base["metrics"]["recipient_hp"]+1,
                                 r["metrics"]["recipient_hp"])
                self.assertEqual(base["metrics"]["recipient_vigor"]-1,
                                 r["metrics"]["recipient_vigor"])
                self.assertEqual(base["metrics"]["recipient_hp_max"],
                                 r["metrics"]["recipient_hp_max"])
                self.assertEqual(base["metrics"]["g5_hit_events"],
                                 r["metrics"]["g5_hit_events"])
                self.assertEqual(2,r["metrics"]["anointed_destiny_remaining"])

    def test_08_policy_report_replays_full_ledger_and_rejects_rehashed_forgery(self):
        for focus in FOCUSES:
            r=self.by_case[focus,"sentry_prepared","fixed","lesser_guided"]
            self.assertEqual(r,attest_policy(r,focus=focus,opponent="sentry_prepared",
                                             mode="fixed",policy="lesser_guided",seed=0))
        forged=deepcopy(self.by_case["Low","soldier","maintained","lesser_guided"])
        forged["metrics"]["recipient_hp"]+=1
        with self.assertRaises(AssertionError):
            attest_policy(forged,focus="Low",opponent="soldier",
                          mode="maintained",policy="lesser_guided")
        forged=deepcopy(self.by_case["Medium","soldier","fixed","lesser_guided"])
        event=rows(forged,"g4_anointed_guided_waiver_applied")[0]
        event["detail"]["destiny_cost"]=0
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(forged,focus="Medium",opponent="soldier",
                          mode="fixed",policy="lesser_guided")

    def test_09_reject_unsourced_level_and_unknown_inputs_before_scene(self):
        for args in (
            {"focus":"none","opponent":"soldier","mode":"fixed","policy":"lesser_guided"},
            {"focus":"Low","opponent":"hunter","mode":"fixed","policy":"ordinary_guided"},
            {"focus":"Medium","opponent":"soldier","mode":"none","policy":"lesser_guided"},
            {"focus":"High","opponent":"soldier","mode":"maintained","policy":"free_host"},
            {"focus":"High","opponent":"soldier","mode":"fixed","policy":"ordinary_guided","seed":-1},
        ):
            with self.subTest(args=args),self.assertRaises(ValueError):
                run_policy(**args)
        combat,native=scene(focus="High",level=2,opponent="soldier",
                            policy="baseline",seed=0)
        with self.assertRaises(ValueError):
            AnointedGuidedAuthority(combat.e,"anointed")
        self.assertEqual(2,native.state.destiny)

    def test_10_documented_scope_and_mvp_exits_stay_uncertified(self):
        path=Path(__file__).resolve().parents[1]/"docs/design/b04-b05-anointed-g5-guided-pressure-v0.md"
        doc=path.read_text().lower()
        for word in ("24","12/12","0/12","0/6","g0","g3","g4","g5",
                     "unopposed","contested","fixed","maintained",
                     "soldier","sentry","ordinary","destiny",
                     "not certified","noncombat"):
            self.assertIn(word,doc)


if __name__=="__main__":
    unittest.main()
