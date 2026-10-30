"""B04/B05 actual Anointed melee and Returning Step in one native G5 scene."""
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.b05_anointed_native_g5_weapon_signature_choice_v0 import (
    FOCUSES,LEVELS,OPPONENTS,POLICIES,SIGNATURE_KIND,
    run_matrix,run_policy,attest_policy,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def events(report,kind):
    return [event for event in report["ledger"] if event["kind"]==kind]


class AnointedG5WeaponSignatureChoiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports=run_matrix(seed=0)
        cls.by_key={(r["focus"],r["level"],r["opponent"],r["policy"]):r
                    for r in cls.reports}

    def test_01_exact_54_fixed_source_cases_never_certify_focus(self):
        self.assertEqual(54,len(self.reports))
        self.assertEqual(54,len(self.by_key))
        self.assertEqual(54,len(FOCUSES)*len(LEVELS)*len(OPPONENTS)*len(POLICIES))
        for r in self.reports:
            self.assertEqual(1,r["metrics"]["one_paid_g5_player_hit"])
            self.assertEqual(1,r["metrics"]["one_paid_g5_enemy_hit"])
            self.assertFalse(r["independent_focus_certified"])
            self.assertFalse(r["representative_play_certified"])
            self.assertIsNone(r["sampled_win_rate"])

    def test_02_exact_one_native_paid_weapon_and_one_g5_enemy_hit(self):
        for r in self.reports:
            with self.subTest(focus=r["focus"],level=r["level"],
                              opponent=r["opponent"],policy=r["policy"]):
                seq=events(r,"g5_melee_sequence_attested")
                hits=events(r,"g5_melee_resolved")
                native=events(r,"g45_attested_hit")
                g4=events(r,"g4_profile_hit")
                self.assertEqual((2,2,2,2),(len(seq),len(hits),len(native),len(g4)))
                self.assertEqual(["anointed","foe"],
                    sorted(x["detail"]["attacker"] for x in hits))
                self.assertTrue(all(x["detail"]["outcome"]=="hit" for x in hits))
                for hit in native:
                    self.assertEqual(r["source_digests"][hit["detail"]["attacker"]],
                                     hit["detail"]["attacker_source"])
                physical=[x for x in events(r,"action_committed")
                          if x["detail"].get("actor")=="anointed"
                          and x["detail"].get("action_class")=="physical"]
                self.assertEqual(1,len(physical))
                self.assertEqual(
                    {"High":30,"Medium":24,"Low":20}[r["focus"]],
                    physical[0]["detail"]["ap_spent"])
                self.assertEqual(physical[0]["index"],
                    next(x for x in native
                         if x["detail"]["attacker"]=="anointed")["detail"]["action_index"])
                self.assertEqual(1,len([x for x in events(r,"action_committed")
                    if x["detail"].get("actor")=="foe"]))
                self.assertEqual({"High":"AH","Medium":"AM","Low":"AL"}[r["focus"]],
                                 r["source_ids"]["anointed"])

    def test_03_weapon_source_stats_and_same_enemy_hp_under_each_policy(self):
        for focus in FOCUSES:
            for lv in LEVELS:
                for opponent in OPPONENTS:
                    baseline=self.by_key[focus,lv,opponent,"weapon_only"]
                    expected_base=baseline["metrics"]
                    for policy in POLICIES:
                        m=self.by_key[focus,lv,opponent,policy]["metrics"]
                        with self.subTest(focus=focus,level=lv,
                                          opponent=opponent,policy=policy):
                            self.assertEqual(expected_base["enemy_hp"],m["enemy_hp"])
                            self.assertEqual(3,m["player_source_attack_bonus"])
                            self.assertEqual("d6" if focus=="Low" else "d4",
                                             m["player_damage_die"])
                            self.assertEqual(
                                {"High":"B05-PC-AH-DAGGER-PIERCE",
                                 "Medium":"B05-PC-AM-DAGGER-PIERCE",
                                 "Low":"B05-PC-AL-SWORD-CUT"}[focus],
                                m["player_source_profile"])
                            self.assertEqual(0,m["caster_vp_spent"])
                            self.assertEqual(0,m["caster_vp_committed"])

    def test_04_signature_deltas_from_identical_real_damage_and_same_foe(self):
        for focus in FOCUSES:
            cap=2 if focus=="High" else 1
            for level in LEVELS:
                for opponent in OPPONENTS:
                    control=self.by_key[focus,level,opponent,"weapon_only"]["metrics"]
                    self.assertEqual(0,control["signature_receipts"])
                    self.assertEqual(2,control["shared_destiny_remaining"])
                    for policy in ("weapon_signature","weapon_lesser"):
                        r=self.by_key[focus,level,opponent,policy]
                        m=r["metrics"]
                        with self.subTest(focus=focus,level=level,foe=opponent,
                                          policy=policy):
                            self.assertEqual(1,m["signature_receipts"])
                            self.assertEqual(cap,m["signature_hp_restored"])
                            self.assertEqual(control["recipient_hp"]+cap,
                                             m["recipient_hp"])
                            self.assertEqual(
                                control["recipient_vigor"]-(cap if policy=="weapon_signature" else 0),
                                m["recipient_vigor"])
                            self.assertEqual(cap if policy=="weapon_signature" else 0,
                                             m["signature_recipient_vigor_spent"])
                            self.assertEqual(int(policy=="weapon_lesser"),
                                             m["signature_destiny_spent"])
                            self.assertEqual(2-m["signature_destiny_spent"],
                                             m["shared_destiny_remaining"])
                            self.assertEqual(control["enemy_hp"],m["enemy_hp"])
                            self.assertEqual(1,len(events(r,SIGNATURE_KIND[focus])))

    def test_05_focus_distinct_g0_timing_and_no_illegal_same_turn_medium_ap(self):
        for focus in FOCUSES:
            r=self.by_key[focus,1,"sentry_prepared","weapon_lesser"]
            m=r["metrics"]
            player_hit=next(x for x in events(r,"g5_melee_resolved")
                            if x["detail"]["attacker"]=="anointed")
            enemy_hit=next(x for x in events(r,"g5_melee_resolved")
                           if x["detail"]["attacker"]=="foe")
            sig=events(r,SIGNATURE_KIND[focus])[0]
            self.assertEqual([1,2],m["recipient_regeneration_rounds"])
            self.assertEqual(2,m["recipient_regeneration_step_count"])
            self.assertEqual(0,m["natural_hp_restored"])
            if focus=="High":
                self.assertEqual((1,2), (m["player_attack_round"],sig["round"]))
                self.assertLess(player_hit["index"],enemy_hit["index"])
                self.assertGreater(sig["index"],enemy_hit["index"])
                self.assertEqual(1,m["high_paid_projection_count"])
                self.assertEqual(0,m["medium_investment_count"])
            elif focus=="Medium":
                self.assertEqual((2,1), (m["player_attack_round"],sig["round"]))
                invests=events(r,"b05_medium_anointed_investment_established")
                self.assertEqual(1,len(invests))
                self.assertEqual(1,m["medium_investment_count"])
                self.assertLess(invests[0]["index"],enemy_hit["index"])
                self.assertLess(enemy_hit["index"],sig["index"])
                self.assertLess(sig["index"],player_hit["index"])
                spent=[x for x in events(r,"action_committed")
                       if x["detail"].get("actor")=="anointed"]
                self.assertEqual([1,2],[x["round"] for x in spent])
                self.assertEqual(["general","physical"],
                                 [x["detail"]["action_class"] for x in spent])
                self.assertEqual([24,24],
                                 [x["detail"]["ap_spent"] for x in spent])
            else:
                self.assertEqual((1,1), (m["player_attack_round"],sig["round"]))
                self.assertLess(enemy_hit["index"],sig["index"])
                self.assertLess(sig["index"],player_hit["index"])
                self.assertEqual(0,m["medium_investment_count"])
                self.assertEqual(0,m["high_paid_projection_count"])

    def test_06_no_duplicate_step_extra_weapon_or_secondary_magic(self):
        for r in self.reports:
            m=r["metrics"]
            self.assertEqual((1,1),(m["one_paid_g5_player_hit"],
                                    m["one_paid_g5_enemy_hit"]))
            self.assertEqual(2,m["recipient_regeneration_step_count"])
            self.assertFalse(events(r,"g4_anointed_guided_waiver_applied"))
            self.assertFalse(events(r,"b05_anointed_guided_host_established"))
            self.assertFalse(events(r,"g5_melee_cancelled"))
            self.assertFalse(any(x["kind"]=="g5_melee_resolved"
                                 and x["detail"]["attacker"] not in ("anointed","foe")
                                 for x in r["ledger"]))
            self.assertEqual({"soldier":"B06-EN-02",
                              "sentry_prepared":"B06-EN-01"}[r["opponent"]],
                             r["source_ids"]["foe"])
            self.assertEqual(1,len(events(r,"b05_anointed_g5_role_policy")))
            self.assertEqual(r["source_digests"],
                events(r,"b05_anointed_g5_role_policy")[0]["detail"]["source_digests"])

    def test_07_full_exact_replay_not_ledger_hash_trust(self):
        for focus in FOCUSES:
            r=self.by_key[focus,3,"sentry_prepared","weapon_lesser"]
            self.assertEqual(r,attest_policy(r,focus=focus,level=3,
                 opponent="sentry_prepared",policy="weapon_lesser",seed=0))
        forged=deepcopy(self.by_key["Low",2,"soldier","weapon_lesser"])
        forged["metrics"]["recipient_hp"]+=1
        with self.assertRaises(AssertionError):
            attest_policy(forged,focus="Low",level=2,opponent="soldier",
                          policy="weapon_lesser")
        forged=deepcopy(self.by_key["Medium",2,"soldier","weapon_signature"])
        paid=next(x for x in events(forged,"action_committed")
                  if x["detail"].get("actor")=="anointed"
                  and x["detail"].get("action_class")=="physical")
        paid["detail"]["ap_spent"]=0
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(forged,focus="Medium",level=2,opponent="soldier",
                          policy="weapon_signature")

    def test_08_invalid_focus_levels_opponents_policies_seeds_fail_closed(self):
        for args in (
            {"focus":"Gifted","level":1,"opponent":"soldier","policy":"weapon_only"},
            {"focus":"Medium","level":4,"opponent":"soldier","policy":"weapon_signature"},
            {"focus":"Low","level":2,"opponent":"hunter","policy":"weapon_lesser"},
            {"focus":"High","level":3,"opponent":"soldier","policy":"free_magic"},
            {"focus":"High","level":3,"opponent":"soldier","policy":"weapon_only","seed":-1},
        ):
            with self.subTest(args=args),self.assertRaises(ValueError):
                run_policy(**args)

    def test_09_scope_documented_without_independent_focus_certification(self):
        doc=(Path(__file__).resolve().parents[1]/
             "docs/design/b04-b05-anointed-native-weapon-signature-role-choice-v0.md").read_text().lower()
        for token in ("54","12/12","0/12","0/6","g0","g1","g2","g4","g5",
                      "dagger","sword","medium","investment","20 ap","24 ap",
                      "unopposed","contested","noncombat","not certified"):
            self.assertIn(token,doc)


if __name__=="__main__":
    unittest.main()
