"""Source-paid Low Life A/B native G5/G4 and timed L3 Exaltation gates."""
from copy import deepcopy
import unittest

from scripts.b05_low_life_native_encounter_v0 import (
    OPPONENTS, LEVELS, ROLES, run_policy, attest_policy, run_matrix, scene,
)
from scripts.b05_low_life_native_rites_v0 import LowLifeNativeRites
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,enemy_actor,party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState,DamagePacket
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def events(e,kind):
    return [v["detail"] for v in e.ledger if v["kind"]==kind]


def attached_scene(*args):
    combat,adapter=scene(*args)
    return combat.e,adapter


class LowLifeNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run_matrix(seed=0)

    def test_01_twelve_genuine_policies_and_source_evidence(self):
        data=self.report
        self.assertEqual(data["cell_count"],12)
        self.assertEqual({(v["role"],v["level"],v["opponent"])
                          for v in data["cells"]},
                         {(r,l,o) for r in ROLES for l in LEVELS for o in OPPONENTS})
        self.assertEqual(data["audit_sha256"],
                         canonical_digest({k:v for k,v in data.items()
                                           if k!="audit_sha256"}))
        for report in data["cells"]:
            self.assertEqual(report["source_ids"]["low"],report["role"])
            self.assertIn(report["source_ids"]["foe"],("B06-EN-01","B06-EN-02"))
            self.assertEqual(report["ledger_sha256"],
                             canonical_digest(report["ledger"]))
            m=report["metrics"]
            self.assertEqual(m["native_g5_paid_hits"],2)
            self.assertEqual(m["native_g4_events"],2)
            self.assertEqual(m["own_real_regen_steps"],2)
            self.assertLessEqual(m["hp"],13)
            self.assertEqual(sum(m["vp"]),2*report["level"])
            self.assertFalse(report["full_encounter_certified"])
            self.assertFalse(report["independent_focus_certified"])
            self.assertIsNone(report["sampled_win_rate"])

    def test_02_l3_a_held_only_after_real_later_step_and_hit(self):
        for opponent in OPPONENTS:
            with self.subTest(opponent=opponent):
                r=next(v for v in self.report["cells"]
                       if (v["role"],v["level"],v["opponent"])==("A",3,opponent))
                logs=r["ledger"]
                arms=[v for v in logs if v["kind"]=="b05_exaltation_armed"]
                held=[v for v in logs if v["kind"]=="b05_held_renewal_resolved"]
                self.assertEqual(len(arms),1)
                self.assertEqual(len(held),1)
                self.assertEqual(arms[0]["detail"]["property"],"EX-LR-01")
                self.assertEqual(arms[0]["round"],2)
                self.assertEqual(arms[0]["turn"],"low")
                self.assertEqual(held[0]["round"],2)
                self.assertGreater(arms[0]["index"],arms[0]["detail"]["step_index"])
                self.assertGreater(held[0]["index"],arms[0]["index"])
                self.assertEqual(r["metrics"]["held_hp_restored"],
                                 held[0]["detail"]["healed"])
                self.assertEqual(r["metrics"]["held_vigor_spent"],
                                 r["metrics"]["held_hp_restored"])
                self.assertEqual(len([v for v in logs
                                      if v["kind"]=="regeneration_step" and
                                         v["detail"]["actor"]=="low"]),2)
                self.assertEqual(held[0]["detail"]["no_extra_regeneration_step"],True)

    def test_03_l3_b_vital_precedes_native_hp_and_uses_host_budget(self):
        for opponent in OPPONENTS:
            r=next(v for v in self.report["cells"]
                   if (v["role"],v["level"],v["opponent"])==("B",3,opponent))
            logs=r["ledger"]
            paid=[x for x in logs if x["kind"]=="b05_exaltation_armed"]
            used=[x for x in logs if x["kind"]=="b05_vital_interposition_applied"]
            self.assertEqual(len(paid),1)
            self.assertEqual(len(used),1)
            self.assertEqual(paid[0]["detail"]["property"],"EX-LP-01")
            self.assertEqual(used[0]["detail"]["prevented_hp"],2)
            self.assertEqual(used[0]["detail"]["consumed_budget"],4)
            self.assertGreater(used[0]["index"],paid[0]["index"])
            self.assertEqual(r["metrics"]["vital_hp_prevented"],2)
            self.assertEqual(r["metrics"]["vital_budget_spent"],4)
            self.assertEqual(sum(r["metrics"]["vp"]),6)

    def test_04_sentry_packet_allocation_preserves_type_and_vigor_priority(self):
        r=next(v for v in self.report["cells"]
               if (v["role"],v["level"],v["opponent"])==
               ("B",3,"sentry_prepared"))
        ledger=r["ledger"]
        use=next(x["detail"] for x in ledger
                 if x["kind"]=="b05_vital_interposition_applied")
        self.assertEqual(use["allocation"][0]["type"],"Piercing")
        self.assertEqual(use["allocation"][1]["type"],"Fire")
        self.assertEqual(use["allocation"][0]["prevented"],2)
        self.assertEqual(use["allocation"][1]["prevented"],0)
        applied=[x["detail"] for x in ledger
                 if x["kind"]=="g4_damage_applied"]
        self.assertEqual(applied[0]["packets"][0]["mitigated"],
                         use["allocation"][0]["residual"])
        self.assertEqual(applied[0]["packets"][1]["mitigated"],
                         use["allocation"][1]["residual"])
        self.assertEqual(applied[0]["vigor_details"][0]["prevented"],
                         r["metrics"]["direct_vigor_prevented"]
                         -applied[1]["vigor_details"][0]["prevented"]
                         if applied[1]["vigor_details"] else
                         r["metrics"]["direct_vigor_prevented"])
        self.assertGreaterEqual(use["budget_remaining"],0)

    def test_05_level_gate_no_exaltations_at_l1_l2(self):
        for r in self.report["cells"]:
            if r["level"]<3:
                self.assertEqual(r["metrics"]["exaltation_paid_arms"],0)
                self.assertEqual(r["metrics"]["held_hp_restored"],0)
                self.assertEqual(r["metrics"]["vital_hp_prevented"],0)
                self.assertIsNone(r["metrics"]["pending"])

    def test_06_source_authentication_rejects_other_roles_and_stale_actor(self):
        e,c=attached_scene("A",3,"soldier",0)
        with self.assertRaises((UnresolvedDecision,ValueError)):
            c.cast_chosen("foe")
        with self.assertRaises(ValueError):
            c.arm_vital("low")
        with self.assertRaises(ValueError):
            c.arm_held("low",2)
        with self.assertRaises(ValueError):
            LowLifeNativeRites(e,"low")
        a=e.actors["low"]
        a.source=party_actor("B",3,"x","party",occupied=((2,2),)).source
        with self.assertRaises(UnresolvedDecision):
            c.cast_chosen("low")
        self.assertEqual(len(events(e,"b05_low_rite_established")),0)

    def test_07_low_chosen_rite_cost_and_reaction_independence(self):
        for role in ROLES:
            e,c=attached_scene(role,3,"soldier",0)
            e.start_turn("low")
            initial=e.actors["low"].reaction_available
            host=c.cast_chosen("low")
            self.assertTrue(host.chosen)
            self.assertEqual(host.committed,1)
            self.assertEqual(e.actors["low"].vp_committed,1)
            self.assertEqual(e.actors["low"].vp_spent,1 if role=="B" else 0)
            self.assertEqual(e.actors["low"].ap_remaining,12)
            self.assertEqual(e.actors["low"].reaction_available,initial)
            with self.assertRaises(ValueError):
                c.cast_chosen("low")
            e.check()

    def test_08_nonchosen_host_cannot_anchor_and_no_reroute(self):
        e,c=attached_scene("B",3,"soldier",0)
        e.start_turn("low")
        host=c.cast_chosen("low",chosen=False)
        self.assertFalse(host.chosen)
        before=(e.actors["low"].vp_available,e.actors["low"].vp_spent)
        with self.assertRaises(ValueError):
            c.arm_vital("low")
        self.assertIsNone(c.pending)
        self.assertEqual((e.actors["low"].vp_available,
                          e.actors["low"].vp_spent),before)
        e.check()

    def test_09_low_a_native_basic_heal_and_b_hand_boundary(self):
        for role in ROLES:
            e,c=attached_scene(role,3,"soldier",0)
            e.start_turn("low")
            target=e.actors["low"]
            target.hp-=4
            target.vigor-=8
            before=(e.actors["low"].ap_remaining,e.actors["low"].vp_available)
            if role=="B":
                with self.assertRaises(UnresolvedDecision):
                    e.g4.cast_basic_heal("low","low",die=2,
                                         hand_available=True,
                                         in_range=True,unobstructed=True)
                self.assertEqual((target.ap_remaining,target.vp_available),before)
            else:
                receipt=e.g4.cast_basic_heal(
                    "low","low",die=3,hand_available=True,
                    in_range=True,unobstructed=True)
                self.assertEqual(receipt["spent_vp"],2)
                self.assertEqual((target.ap_remaining,target.vp_available),
                                 (before[0]-30,before[1]-2))
                self.assertEqual(len(events(e,"g4_basic_heal_applied")),1)

    def test_10_replay_rejects_rehashed_policy_and_unrelated_seed(self):
        r=run_policy(role="A",level=3,opponent="soldier",seed=0)
        self.assertEqual(attest_policy(r,role="A",level=3,seed=0),r)
        edited=deepcopy(r)
        edited["metrics"]["held_hp_restored"]=99
        with self.assertRaises(AssertionError):
            attest_policy(edited,role="A",level=3,seed=0)
        edited["ledger_sha256"]=canonical_digest(edited["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(edited,role="A",level=3,seed=0)
        with self.assertRaises(AssertionError):
            attest_policy(r,role="A",level=3,seed=1)

    def test_11_invalid_matrix_arguments_fail_before_source_actor(self):
        for args in (("F",3,"soldier",0),("A",4,"soldier",0),
                     ("B",True,"soldier",0),("A",3,"invented",0),
                     ("B",1,"soldier",-1)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                run_policy(role=args[0],level=args[1],
                           opponent=args[2],seed=args[3])

    def test_12_vigor_only_does_not_consume_pending_vital(self):
        e,c=attached_scene("B",3,"soldier",0)
        e.start_turn("low")
        c.cast_chosen("low")
        c.arm_vital("low")
        pending=deepcopy(c.pending)
        result=e.g4.apply_damage(
            "low",(DamagePacket("vigor","Direct Vigor",2),),
            event_key="independently-confirmed-vigor-test",
            cause="isolated_confirmed_G4_packet_fixture")
        self.assertEqual(result["hp_loss"],0)
        self.assertEqual(c.pending,pending)
        self.assertEqual(len(events(e,"b05_vital_interposition_applied")),0)
        self.assertEqual(len(events(e,"g4_damage_applied")),1)

    def test_13_no_held_arm_before_real_step_or_without_chosen(self):
        e,c=attached_scene("A",3,"soldier",0)
        e.start_turn("low")
        c.cast_chosen("low")
        with self.assertRaises(ValueError):
            c.arm_held("low",2)
        e.end_turn()
        e.start_turn("foe")
        with self.assertRaises(ValueError):
            c.arm_held("low",1)

    def test_14_host_termination_keeps_spent_property_price(self):
        e,c=attached_scene("B",3,"soldier",0)
        e.start_turn("low")
        c.cast_chosen("low")
        c.arm_vital("low")
        a=e.actors["low"]
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,1,2))
        e.g3.release("low","Vital Shelter")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(4,0,2))
        self.assertIsNone(c.pending)
        self.assertEqual(len(events(e,"b05_exaltation_expired")),1)
        with self.assertRaises(ValueError):
            c.arm_vital("low")
        self.assertEqual(a.vp_spent,2)

    def test_15_no_unrelated_chosen_or_extra_full_focus_certificate(self):
        self.assertFalse(self.report["independent_focus_certified"])
        for r in self.report["cells"]:
            self.assertEqual(r["metrics"]["native_g4_events"],2)
            self.assertEqual(r["source_ids"]["low"],r["role"])
            self.assertIsNone(r["balance_approval"])


    def test_16_held_first_dying_crossing_never_resurrects(self):
        e,c=attached_scene("A",3,"soldier",0)
        e.start_turn("low")
        c.cast_chosen("low")
        e.end_turn()
        e.start_turn("foe")
        e.end_turn()
        e.begin_round()
        def arm(enc,who):
            c.arm_held(who,2)
        e.start_turn("low",regen_choice=RegenerationChoice(),
                     on_regeneration_complete=arm)
        self.assertEqual(c.pending["points"],2)
        a=e.actors["low"]
        result=e.g4.apply_damage(
            "low",(DamagePacket("hp","Piercing",16,
                                penetration=0,armor_rule="weapon"),),
            event_key="separate-lethal-Held-fixture",
            cause="independently-confirmed-single-G4-event",
            wound_location_roll=8)
        self.assertTrue(a.hp<=0)
        self.assertIsNone(c.pending)
        self.assertEqual(result["wound"],"Serious")
        payout=events(e,"b05_held_renewal_resolved")
        self.assertEqual(len(payout),1)
        self.assertEqual(payout[0]["healed"],0)
        self.assertFalse(a.dead)

    def test_17_vital_pending_budget_one_consumes_without_hp_protection(self):
        e,c=attached_scene("B",3,"soldier",0)
        e.start_turn("low")
        host=c.cast_chosen("low")
        c.arm_vital("low")
        e.g4.apply_damage("low",(DamagePacket("vigor","Direct Vigor",7),),
                          event_key="finite-budget-7",
                          cause="separate-confirmed-G4-packet")
        self.assertEqual(host.budget,1)
        self.assertIsNotNone(c.pending)
        before=e.actors["low"].hp
        e.g4.apply_damage(
            "low",(DamagePacket("hp","Piercing",8,
                                penetration=2,armor_rule="weapon"),),
            event_key="finite-budget-1-then-hp",
            cause="separate-confirmed-G4-packet")
        self.assertIsNone(c.pending)
        self.assertEqual(e.actors["low"].hp,before-5)
        event=events(e,"b05_vital_interposition_applied")[0]
        self.assertEqual((event["prevented_hp"],event["budget_remaining"]),(0,1))
        self.assertEqual(host.budget,1)


if __name__=="__main__":
    unittest.main()
