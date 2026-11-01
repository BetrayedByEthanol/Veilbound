"""First Alpha L1 meaningful choices, native defensive costs and exits."""
from copy import deepcopy
import unittest

from scripts.b04_b05_b06_alpha_l1_tactics_v0 import (
    POLICIES,OPTIONS,run_policy,run_choice,attest,validate_choice,
)
from scripts.b04_b05_b06_alpha_mixed_native_v0 import scene,PARTY
from scripts.b06_encounter_state_v0 import RegenerationChoice,UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class AlphaL1TacticalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results={(v,p):run_policy(variant=v,policy=p)
                     for v in ("A","B") for p in POLICIES}

    def test_01_selected_original_Alpha_sources_and_unchanged_foe(self):
        for (variant,policy),r in self.results.items():
            with self.subTest(variant=variant,policy=policy):
                self.assertEqual(r["source_ids"]["priest"],variant)
                self.assertEqual(r["source_ids"]["anointed"],"AM")
                self.assertEqual(r["source_ids"]["gifted"],"G")
                self.assertEqual(r["source_ids"]["scholar"],"F")
                self.assertEqual(r["source_ids"]["foe"],"B06-EN-02")
                self.assertEqual(r["opponent_level"],3)
                self.assertEqual(r["rounds_completed"],2)
                self.assertEqual(r["native_g5_attack_slots"],2)
                self.assertEqual(r["human_play_sessions"],0)
                self.assertEqual(r["independent_focus_certifications"],0)
                self.assertEqual(r["strict_mvp_gates_accepted"],0)
                self.assertFalse(r["complete_Alpha_L1_tactical_choice_engine"])

    def test_02_guard_and_dodge_have_real_pre_roll_costs(self):
        for variant in ("A","B"):
            for policy,defense in (("protected_guard","guard"),
                                   ("evasive_dodge","dodge")):
                r=self.results[variant,policy]
                assigned=[x for x in r["ledger"]
                          if x["kind"]=="defense_assigned"
                          and x["detail"]["actor"]=="priest"]
                self.assertEqual(len(assigned),2)
                first=assigned[0]["detail"]
                self.assertEqual(first["defense"],defense)
                self.assertEqual(r["priest_round_one_defense"]["outcome"],"miss")
                if defense=="guard":
                    # B's selected L1 TAL-C05 + shield grants capacity 3;
                    # A has one ordinary source Guard. One pre-roll Guard
                    # consumes exactly one capacity, not AP or Dodge Pressure.
                    self.assertEqual(first["guard_remaining"],
                                     2 if variant=="B" else 0)
                    self.assertEqual(first["dodge_pressure"],0)
                else:
                    self.assertEqual(first["dodge_pressure"],2)
                    self.assertIsNotNone(first["defense_value"])
                self.assertEqual(assigned[1]["detail"]["defense"],"take_hit")
                self.assertFalse(r["medium_pulse_applied"])
                self.assertEqual(r["native_exit_receipts"],4)

    def test_03_g5_hit_only_causes_medium_pulse_when_actually_invested(self):
        for variant in ("A","B"):
            paid=self.results[variant,"wounded_with_step"]
            avoided=self.results[variant,"protected_guard"]
            omitted=self.results[variant,"wounded_no_investment"]
            self.assertEqual(paid["priest_round_one_defense"]["outcome"],"hit")
            self.assertTrue(paid["medium_pulse_applied"])
            self.assertFalse(avoided["medium_pulse_applied"])
            self.assertEqual(omitted["priest_round_one_defense"]["outcome"],"hit")
            self.assertFalse(omitted["medium_pulse_applied"])
            self.assertEqual(len([e for e in paid["ledger"]
                                  if e["kind"]=="g4_anointed_medium_returning_step_applied"]),1)
            self.assertEqual(len([e for e in omitted["ledger"]
                                  if e["kind"]=="b05_medium_anointed_investment_established"]),0)

    def test_04_real_actor_turn_action_choices_and_source_AP_VP(self):
        for (variant,policy),r in self.results.items():
            choices=POLICIES[policy]
            actual=r["player_actions"]
            self.assertEqual(actual,
                             {k:choices[k] for k in ("anointed","priest","gifted","scholar")})
            paid=[x for x in r["ledger"]
                  if x["kind"]=="action_committed"
                  and x["detail"]["actor"] in PARTY]
            for name,choice in actual.items():
                actor_paid=[x["detail"]["ap_spent"] for x in paid
                            if x["detail"]["actor"]==name]
                self.assertEqual(
                    actor_paid,
                    ([] if choice=="hold" else [
                         24 if name=="anointed" else 30 if name=="priest" else 20]))
            for name,t in r["vp_state"].items():
                self.assertEqual(t["available"]+t["committed"]+t["spent"],t["max"])
            flames=[x for x in r["ledger"] if x["kind"]=="g3_flame_launched"]
            self.assertEqual(len(flames),int(choices["gifted"]=="joy_flame")
                             +int(choices["scholar"]=="flame"))

    def test_05_different_outcomes_do_not_mint_false_victory_or_exit(self):
        for variant in ("A","B"):
            for policy in ("protected_guard","evasive_dodge",
                           "wounded_no_investment","wounded_with_step"):
                r=self.results[variant,policy]
                self.assertEqual(r["outcome"],"party_scene_withdrawal")
                self.assertEqual(r["native_exit_receipts"],4)
                self.assertFalse(r["final_state"]["foe"]["dead"])
            r=self.results[variant,"defend_position"]
            self.assertEqual(r["outcome"],"ongoing_engagement_not_terminal")
            self.assertEqual(r["native_exit_receipts"],0)
            self.assertEqual(len([x for x in r["ledger"]
                                  if x["kind"]=="g5_terminal_exit"]),0)

    def test_06_no_unlisted_choice_or_roll_confers_source_authority(self):
        valid=deepcopy(POLICIES["protected_guard"])
        for key,val in (("priest_defense","parry"),
                        ("scholar","fireball"),
                        ("anointed","free_pulse"),
                        ("round_two","victory"),
                        ("soldier_d20",20),
                        ("soldier_d20",True),
                        ("soldier_d20",0)):
            with self.subTest(key=key,val=val):
                q=deepcopy(valid)
                q[key]=val
                with self.assertRaises((ValueError,UnresolvedDecision)):
                    validate_choice(q)
        short=deepcopy(valid)
        del short["priest"]
        with self.assertRaises(ValueError):
            validate_choice(short)
        with self.assertRaises(ValueError):
            run_policy(policy="phantom")
        with self.assertRaises(ValueError):
            run_policy(policy="protected_guard",variant="Z")

    def test_07_exact_replay_checks_changes_even_with_reshashed_ledger(self):
        for variant in ("A","B"):
            for policy in POLICIES:
                record=self.results[variant,policy]
                self.assertEqual(attest(record,choices=POLICIES[policy],
                                        variant=variant)["ledger_sha256"],
                                 record["ledger_sha256"])
        r=deepcopy(self.results["A","evasive_dodge"])
        r["priest_round_one_defense"]["outcome"]="hit"
        with self.assertRaises(AssertionError):
            attest(r,choices=POLICIES["evasive_dodge"])
        r=deepcopy(self.results["A","protected_guard"])
        r["ledger"][0]["kind"]="forged_encounter"
        r["ledger_sha256"]=canonical_digest(r["ledger"])
        with self.assertRaises(AssertionError):
            attest(r,choices=POLICIES["protected_guard"])
        with self.assertRaises(AssertionError):
            attest(self.results["A","protected_guard"],
                   choices=POLICIES["evasive_dodge"])

    def test_08_failed_guard_preflight_spends_no_G0_AP_or_guard(self):
        c,_,_,_=scene(variant="A")
        e=c.e
        e.start_turn("anointed",regen_choice=RegenerationChoice())
        e.end_turn()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        victim=e.actors["priest"]
        victim.ready_guard=False
        ap=e.actors["foe"].ap_remaining
        guard=victim.guard_remaining
        with self.assertRaises(ValueError):
            c.declare("foe","priest",profiles=("B06-AT-03",),
                      defenses=("guard",))
        self.assertEqual(e.actors["foe"].ap_remaining,ap)
        self.assertEqual(victim.guard_remaining,guard)
        self.assertFalse(any(x["kind"]=="attack_sequence_committed"
                             for x in e.ledger))

    def test_09_prone_dodge_rejected_before_cost_and_pressure(self):
        c,_,_,_=scene(variant="B")
        e=c.e
        e.start_turn("anointed",regen_choice=RegenerationChoice())
        e.end_turn()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        victim=e.actors["priest"]
        victim.conditions.append("Prone")
        ap=e.actors["foe"].ap_remaining
        pressure=victim.dodge_pressure
        with self.assertRaises(UnresolvedDecision):
            c.declare("foe","priest",profiles=("B06-AT-03",),
                      defenses=("dodge",))
        self.assertEqual(victim.dodge_pressure,pressure)
        self.assertEqual(e.actors["foe"].ap_remaining,ap)

    def test_10_defense_outcome_tracks_native_pre_roll_value_not_caller_flag(self):
        for variant in ("A","B"):
            for policy in ("protected_guard","evasive_dodge","wounded_with_step"):
                r=self.results[variant,policy]
                pre=[x for x in r["ledger"] if x["kind"]=="defense_assigned"
                     and x["detail"]["actor"]=="priest"][0]
                attack=[x for x in r["ledger"] if x["kind"]=="g5_melee_roll"][0]
                self.assertEqual(pre["detail"]["defense"],
                                 attack["detail"]["declared_defense"])
                self.assertEqual(pre["detail"]["defense_value"],
                                 attack["detail"]["defense_value"])
                self.assertEqual(attack["detail"]["attack_face"],
                                 POLICIES[policy]["soldier_d20"])
                self.assertEqual(r["priest_round_one_defense"]["outcome"],
                                 "hit" if attack["detail"]["hit"] else "miss")


if __name__=="__main__":
    unittest.main()
