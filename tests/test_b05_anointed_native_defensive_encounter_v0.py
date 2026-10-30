"""Bounded High/Medium/Low Anointed L1–3 native G5 defensive receipts."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import unittest

from scripts.b05_anointed_native_defensive_encounter_v0 import (
    FOCI, LEVELS, OPPONENTS, POLICIES,
    attest_policy, run_matrix, run_policy, scene,
)
from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision

ROOT=Path(__file__).resolve().parents[1]
SIGNATURE={"High":("g4_anointed_returning_step_applied",2),
           "Medium":("g4_anointed_medium_returning_step_applied",1),
           "Low":("g4_anointed_low_returning_step_applied",1)}


def rows(report,kind):
    return [x for x in report["ledger"] if x["kind"]==kind]


class AnointedRestorationNativeDefenseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports=run_matrix(seed=0)
        cls.lookup={(r["focus"],r["level"],r["opponent"],r["policy"]):r
                    for r in cls.reports}

    def test_01_matrix_is_exact_source_fifty_four_policy_witnesses(self):
        self.assertEqual(54,len(self.reports))
        self.assertEqual(54,len(self.lookup))
        self.assertEqual(3*3*2*3,len(FOCI)*len(LEVELS)*len(OPPONENTS)*len(POLICIES))
        self.assertTrue(all(r["independent_focus_certified"] is False
                            and r["representative_play_certified"] is False
                            and r["sampled_win_rate"] is None
                            for r in self.reports))

    def test_02_real_source_soldier_sentry_one_paid_g5_hit_and_g4_damage(self):
        for r in self.reports:
            with self.subTest(focus=r["focus"],level=r["level"],
                              foe=r["opponent"],policy=r["policy"]):
                m=r["metrics"]
                self.assertEqual((1,1,1,2),
                    (m["g0_enemy_paid_actions"],m["g5_hit_events"],
                     m["g4_damage_events"],m["g0_recipient_regeneration_steps"]))
                self.assertEqual(1,len(rows(r,"g5_melee_sequence_attested")))
                self.assertEqual(1,len(rows(r,"g5_melee_resolved")))
                self.assertEqual(1,len(rows(r,"g4_damage_applied")))
                self.assertFalse(m["recipient_dead"])
                self.assertGreater(m["recipient_hp"],0)
                self.assertLess(m["recipient_hp"],m["recipient_hp_max"])
                self.assertEqual(0,m["recipient_wound_count"])
                self.assertEqual("foe",rows(r,"g5_melee_resolved")[0]["detail"]["attacker"])
                self.assertEqual({"soldier":"B06-EN-02",
                                  "sentry_prepared":"B06-EN-01"}[r["opponent"]],
                                 r["source_ids"]["foe"])
                self.assertEqual({"High":"AH","Medium":"AM","Low":"AL"}[r["focus"]],
                                 r["source_ids"]["anointed"])

    def test_03_source_sha_and_paid_g5_action_bind_the_exact_attack(self):
        for r in self.reports:
            with self.subTest(focus=r["focus"],level=r["level"],
                              foe=r["opponent"],policy=r["policy"]):
                for actor_id,sha in r["source_digests"].items():
                    path=next(x["detail"]["source_digests"] for x in r["ledger"]
                              if x["kind"]=="b05_anointed_defensive_policy")
                    self.assertEqual(sha,path[actor_id])
                source_actions=[e for e in rows(r,"action_committed")
                                if e["detail"].get("actor")=="foe"]
                self.assertEqual(1,len(source_actions))
                g5=rows(r,"g5_melee_sequence_attested")[0]
                self.assertEqual([source_actions[0]["index"]],
                                 g5["detail"]["action_indices"])
                self.assertEqual(r["source_digests"]["foe"],
                                 g5["detail"]["source_digest"])

    def test_04_signature_heals_only_source_capped_positive_hp_with_destiny(self):
        for focus in FOCI:
            kind,cap=SIGNATURE[focus]
            for level in LEVELS:
                for opponent in OPPONENTS:
                    base=self.lookup[focus,level,opponent,"baseline"]
                    for policy in ("signature","lesser"):
                        r=self.lookup[focus,level,opponent,policy]
                        with self.subTest(focus=focus,level=level,foe=opponent,
                                          policy=policy):
                            m=r["metrics"]
                            b=base["metrics"]
                            self.assertEqual(1,m["signature_receipts"])
                            self.assertEqual(cap,m["signature_hp_restored"])
                            self.assertEqual(b["recipient_hp"]+cap,m["recipient_hp"])
                            self.assertEqual(
                                b["recipient_vigor"]-(0 if policy=="lesser" else cap),
                                m["recipient_vigor"])
                            self.assertEqual(
                                (1 if policy=="lesser" else 0),
                                m["signature_destiny_spent"])
                            self.assertEqual(2-m["signature_destiny_spent"],
                                             m["anointed_destiny_remaining"])
                            self.assertEqual(1,len(rows(r,kind)))
                    self.assertEqual(0,base["metrics"]["signature_receipts"])
                    self.assertEqual(2,base["metrics"]["anointed_destiny_remaining"])

    def test_05_g0_high_projection_medium_invest_low_self_step_provenance(self):
        for focus in FOCI:
            r=self.lookup[focus,3,"soldier","signature"]
            kind,_=SIGNATURE[focus]
            pulse=rows(r,kind)[0]
            foe=rows(r,"g5_melee_resolved")[0]
            self.assertGreater(pulse["index"],foe["index"])
            if focus=="High":
                proj=[e for e in rows(r,"action_committed") if
                      e["detail"].get("label")=="anointed:high:returning_step"]
                self.assertEqual(1,len(proj))
                self.assertEqual(20,proj[0]["detail"]["ap_spent"])
                self.assertEqual(proj[0]["index"],pulse["detail"]["action_index"])
                self.assertEqual(2,pulse["round"])
            elif focus=="Medium":
                setup=[e for e in rows(r,"action_committed") if
                       e["detail"].get("label")=="anointed:medium:investment"]
                self.assertEqual(1,len(setup))
                self.assertEqual(24,setup[0]["detail"]["ap_spent"])
                self.assertEqual(0,pulse["detail"]["activation_ap"])
                self.assertEqual(1,pulse["round"])
                self.assertLess(setup[0]["index"],pulse["index"])
            else:
                self.assertEqual(0,pulse["detail"]["activation_ap"])
                self.assertEqual(1,pulse["round"])
                self.assertEqual("anointed",pulse["detail"]["recipient"])
            self.assertEqual(0,r["metrics"]["anointed_vp_spent"])
            self.assertEqual(0,r["metrics"]["anointed_vp_committed"])

    def test_06_ordinary_natural_step_does_not_hide_source_hit_or_create_hp(self):
        for r in self.reports:
            recipient=r["metrics"]["recipient"]
            steps=[e for e in rows(r,"regeneration_step")
                   if e["detail"]["actor"]==recipient]
            self.assertEqual(2,len(steps))
            self.assertTrue(all(x["detail"]["hp_restored"]==0
                                and x["detail"]["throughput_spent"]==0
                                for x in steps))
            self.assertEqual(0,len(rows(r,"g4_anointed_guided_waiver_applied")))
            self.assertFalse(rows(r,"g5_melee_cancelled"))
            self.assertFalse(rows(r,"g5_melee_resolved") and
                             r["metrics"]["g5_hit_events"]!=1)

    def test_07_forged_report_even_with_recomputed_digest_rejected(self):
        from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
        r=deepcopy(self.lookup["Medium",2,"sentry_prepared","lesser"])
        r["metrics"]["recipient_hp"]+=1
        with self.assertRaises(AssertionError):
            attest_policy(r,focus="Medium",level=2,
                          opponent="sentry_prepared",policy="lesser",seed=0)
        r=deepcopy(self.lookup["High",1,"soldier","signature"])
        policy_event=next(x for x in r["ledger"]
                          if x["kind"]=="b05_anointed_defensive_policy")
        policy_event["detail"]["source_digests"]["anointed"]="forged"
        r["ledger_sha256"]=canonical_digest(r["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(r,focus="High",level=1,opponent="soldier",
                          policy="signature",seed=0)

    def test_08_real_report_replays_byte_equal_without_recency_flag(self):
        for focus in FOCI:
            r=self.lookup[focus,3,"sentry_prepared","lesser"]
            self.assertEqual(r,attest_policy(r,focus=focus,level=3,
                                            opponent="sentry_prepared",
                                            policy="lesser",seed=0))

    def test_09_invalid_levels_focus_opponent_policy_and_seed_fail_closed(self):
        for args in (
            {"focus":"none","level":1,"opponent":"soldier","policy":"baseline"},
            {"focus":"Low","level":4,"opponent":"soldier","policy":"signature"},
            {"focus":"Medium","level":3,"opponent":"hunter","policy":"lesser"},
            {"focus":"High","level":2,"opponent":"soldier","policy":"hostile"},
            {"focus":"High","level":2,"opponent":"soldier","policy":"signature","seed":-1},
        ):
            with self.subTest(args=args),self.assertRaises(ValueError):
                run_policy(**args)

    def test_10_no_unsupported_anointed_offense_intrusion_or_noncombat_clock(self):
        combat,native=scene(focus="Low",level=3,opponent="soldier",
                            policy="signature",seed=0)
        e=combat.e
        self.assertEqual((),e.actors["anointed"].source.attack_profiles)
        self.assertEqual(0,len(rows({"ledger":e.ledger},"g5_melee_resolved")))
        self.assertFalse(hasattr(e.actors["anointed"],"destiny"))
        self.assertFalse(e.g4.anointed_guided)
        self.assertEqual(2,native.state.destiny)
        doc=(ROOT/"docs/design/b04-b05-anointed-three-focus-native-g5-defensive-witness-v0.md").read_text()
        for token in ("12/12","0/12","0/6","G0","G4","G5","Soldier",
                      "Sentry","unopposed","noncombat","not certified"):
            self.assertIn(token.lower(),doc.lower())


if __name__=="__main__":
    unittest.main()
