"""B06 native G0/G1/G4/G4.5/G5 off-turn Opportunity acceptance."""
from copy import deepcopy
import json
import unittest

from scripts.b06_offturn_opportunity_v0 import OpportunityChoice
from scripts.b06_offturn_opportunity_witness_v0 import (
    run_case,run_matrix,attest_case,
)
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,Response,Trigger,UnresolvedDecision,
    enemy_actor,party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def scene(*,role="F",two=False,enemy_mover=False,level=3):
    if enemy_mover:
        mover=enemy_actor("B06-EN-02","mover","enemy",occupied=((2,2),))
        first=party_actor("S",level,"alpha","party",occupied=((3,2),))
    else:
        mover=party_actor(role,level,"mover","party",occupied=((2,2),))
        first=enemy_actor("B06-EN-02","alpha","enemy",occupied=((3,2),))
    roster=[mover,first]
    if two:
        roster.append(enemy_actor("B06-EN-02","beta","enemy",
                                  occupied=((3,3),)))
    scores={"mover":40,"alpha":30}
    if two:
        scores["beta"]=20
    e=Encounter(roster,scores,seed=0,scenario="offturn-source-test",
                policy="explicit",objective="native_opportunity")
    GridMovement(e,width=7,height=7,scene_id="offturn-test")
    RangedCombat(e)
    SpellState(e)
    DamageState(e)
    g5=SourceMelee(e)
    e.begin_round()
    g5.bridge.start_next_turn(RegenerationChoice())
    return e,g5,mover,first


def events(e,kind):
    return [v for v in e.ledger if v["kind"]==kind]


class NativeOpportunityV0Tests(unittest.TestCase):
    def test_01_real_soldier_hit_consumes_G0_reaction_and_native_G4(self):
        e,g,m,t=scene()
        hp,ap,mp=m.hp,m.ap_remaining,m.mp_remaining
        self.assertTrue(g.opportunity_step("mover",(0,-1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",12,damage_face=4,
                                      wound_location_roll=8)}))
        self.assertLess(m.hp,hp)
        self.assertEqual(m.ap_remaining,ap)
        self.assertEqual(m.mp_remaining,mp-2)
        self.assertEqual(m.occupied,((2,1),))
        self.assertEqual((t.opportunity_used,t.reaction_available),(1,False))
        self.assertEqual(len(events(e,"spontaneous_committed")),1)
        self.assertEqual(len(events(e,"g5_opportunity_resolved")),1)
        self.assertEqual(len(events(e,"g4_damage_applied")),1)
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),1)
        self.assertEqual(len(events(e,"action_committed")),0)

    def test_02_miss_spends_response_but_no_G4_damage_or_defense_roll(self):
        e,g,m,t=scene()
        hp=m.hp
        self.assertTrue(g.opportunity_step("mover",(0,-1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",1)}))
        self.assertEqual(m.hp,hp)
        self.assertEqual(t.opportunity_used,1)
        self.assertEqual(len(events(e,"g5_opportunity_resolved")),1)
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),0)
        self.assertEqual(len(events(e,"g4_damage_applied")),0)

    def test_03_canonical_two_enemy_response_window_in_initiative_order(self):
        e,g,m,a=scene(two=True,role="T")
        b=e.actors["beta"]
        start=m.hp
        self.assertTrue(g.opportunity_step("mover",(0,1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",1),
            "beta":OpportunityChoice("B06-AT-03",12,damage_face=1,
                                     wound_location_roll=8)}))
        self.assertLess(m.hp,start)
        self.assertEqual(
            [x["detail"]["actor"] for x in events(e,"spontaneous_committed")],
            ["alpha","beta"])
        self.assertEqual(
            [x["detail"]["outcome"] for x in events(e,"g5_opportunity_resolved")],
            ["miss","hit"])
        self.assertEqual((a.opportunity_used,b.opportunity_used),(1,1))
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),1)
        self.assertEqual(len(events(e,"g1_movement_step")),1)

    def test_04_real_guard_preserves_HP_and_spends_instrument(self):
        e,g,m,a=scene(role="S")
        guard=m.guard_remaining
        self.assertTrue(g.opportunity_step("mover",(0,-1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",2,"guard")}))
        self.assertEqual(m.guard_remaining,guard-1)
        self.assertEqual(m.hp,m.hp_max)
        self.assertEqual(
            events(e,"defense_assigned")[-1]["detail"]["defense"],"guard")
        self.assertEqual(len(events(e,"g4_damage_applied")),0)

    def test_05_dodge_uses_real_G0_pressure_with_two_responses(self):
        e,g,m,a=scene(role="S",two=True)
        self.assertTrue(g.opportunity_step("mover",(0,1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",2,"dodge"),
            "beta":OpportunityChoice("B06-AT-03",2,"dodge")}))
        self.assertEqual(m.dodge_pressure,4)
        self.assertEqual([x["detail"]["defense"] for x in
                          events(e,"defense_assigned")],["dodge","dodge"])
        self.assertEqual(len(events(e,"g4_damage_applied")),0)

    def test_06_sword_ready_source_bound_medium_scholar_is_real_responder(self):
        e,g,m,a=scene(enemy_mover=True)
        self.assertTrue(g.opportunity_step("mover",(0,-1),decisions={
            "alpha":OpportunityChoice("B05-PC-S-SWORD-CUT",12,
                                      damage_face=4,wound_location_roll=8)}))
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),1)
        self.assertEqual(events(e,"g5_opportunity_roll")[0]
                         ["detail"]["profile"],"B05-PC-S-SWORD-CUT")
        self.assertEqual(a.opportunity_used,1)

    def test_07_unwielded_scholar_cannot_claim_threat_or_G0_response(self):
        e,g,m,a=scene(enemy_mover=True)
        e.g2.wielded["alpha"].remove("Sword")
        before=(len(e.ledger),m.mp_remaining,a.reaction_available)
        with self.assertRaises(UnresolvedDecision):
            g.opportunity_step("mover",(0,-1),decisions={
                "alpha":OpportunityChoice("B05-PC-S-SWORD-CUT",12,
                                          damage_face=4)})
        self.assertEqual((len(e.ledger),m.mp_remaining,
                          a.reaction_available),before)
        self.assertEqual(a.opportunity_used,0)

    def test_08_unwielded_soldier_does_not_gain_a_ghost_sword_attack(self):
        e,g,m,a=scene()
        e.g2.wielded["alpha"].remove("Sword")
        with self.assertRaises(UnresolvedDecision):
            g.opportunity_step("mover",(0,-1),decisions={
                "alpha":OpportunityChoice("B06-AT-03",12,damage_face=4)})
        self.assertEqual(a.opportunity_used,0)
        self.assertEqual(m.occupied,((2,2),))

    def test_09_declared_ineligible_profile_fails_before_any_capacity(self):
        e,g,m,a=scene()
        old=(a.opportunity_used,m.mp_remaining,len(e.ledger))
        with self.assertRaises((ValueError,UnresolvedDecision)):
            g.opportunity_step("mover",(0,-1),decisions={
                "alpha":OpportunityChoice("B06-AT-02",12,damage_face=4)})
        self.assertEqual((a.opportunity_used,m.mp_remaining,len(e.ledger)),old)

    def test_10_missing_damage_die_cannot_commit_G0_response_or_movement(self):
        e,g,m,a=scene()
        old=(a.opportunity_used,m.mp_remaining,len(e.ledger),m.hp)
        with self.assertRaises((ValueError,UnresolvedDecision)):
            g.opportunity_step("mover",(0,-1),decisions={
                "alpha":OpportunityChoice("B06-AT-03",12)})
        self.assertEqual((a.opportunity_used,m.mp_remaining,
                          len(e.ledger),m.hp),old)

    def test_11_invalid_critical_faces_and_wound_requirements_fail_closed(self):
        for candidate in (
            OpportunityChoice("B06-AT-03",20,damage_face=4),
            OpportunityChoice("B06-AT-03",20,damage_face=4,
                              confirmation_face=20,critical_dice=(4,)),
            OpportunityChoice("B06-AT-03",12,damage_face=7),
            OpportunityChoice("B06-AT-03",1,damage_face=4),
        ):
            e,g,m,a=scene()
            before=(len(e.ledger),a.opportunity_used,m.mp_remaining)
            with self.assertRaises((ValueError,UnresolvedDecision)):
                g.opportunity_step("mover",(0,-1),decisions={
                    "alpha":candidate})
            self.assertEqual((len(e.ledger),a.opportunity_used,
                              m.mp_remaining),before)

    def test_12_live_critical_damage_creates_exact_G4_wound(self):
        e,g,m,a=scene()
        start=m.hp
        result=g.opportunity_step("mover",(0,-1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",20,damage_face=6,
                confirmation_face=20,critical_dice=(4,4),
                wound_location_roll=8)})
        self.assertFalse(result)
        self.assertLess(m.hp,start)
        self.assertTrue(m.wounds)
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),1)
        self.assertEqual(len(events(e,"g5_opportunity_resolved")),1)
        self.assertEqual(m.occupied,((2,2),))
        self.assertEqual(m.mp_remaining,12)

    def test_13_two_paid_opportunities_second_cancelled_after_incapacitation(self):
        e,g,m,a=scene(two=True)
        b=e.actors["beta"]
        result=g.opportunity_step("mover",(0,1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",20,damage_face=6,
                confirmation_face=20,critical_dice=(4,4),
                wound_location_roll=8),
            "beta":OpportunityChoice("B06-AT-03",12,damage_face=1,
                                     wound_location_roll=8)})
        self.assertFalse(result)
        self.assertEqual((a.opportunity_used,b.opportunity_used),(1,1))
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),1)
        self.assertEqual(len(events(e,"g5_opportunity_cancelled")),1)
        self.assertEqual(len(events(e,"g1_movement_step")),0)
        self.assertEqual(m.occupied,((2,2),))

    def test_14_explicit_decline_does_not_cost_reaction_and_still_pays_MP(self):
        e,g,m,a=scene()
        self.assertTrue(g.opportunity_step("mover",(0,-1),decisions={"alpha":None}))
        self.assertTrue(a.reaction_available)
        self.assertEqual(a.opportunity_used,0)
        self.assertEqual(len(events(e,"g5_opportunity_resolved")),0)
        self.assertEqual(m.mp_remaining,10)

    def test_15_missing_enemy_or_extra_noneligible_actor_rejected_precommit(self):
        for choices in ({},{"alpha":None,"mover":None}):
            e,g,m,a=scene()
            before=(m.occupied,m.mp_remaining,len(e.ledger),a.opportunity_used)
            with self.assertRaises(UnresolvedDecision):
                g.opportunity_step("mover",(0,-1),decisions=choices)
            self.assertEqual((m.occupied,m.mp_remaining,
                              len(e.ledger),a.opportunity_used),before)

    def test_16_next_step_same_segment_does_not_grant_duplicated_Opportunity(self):
        e,g,m,a=scene()
        self.assertTrue(g.opportunity_step("mover",(0,-1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",1)}))
        self.assertTrue(g.opportunity_step("mover",(0,1),decisions={}))
        self.assertTrue(g.opportunity_step("mover",(0,-1),decisions={}))
        self.assertEqual(a.opportunity_used,1)
        self.assertEqual(len(events(e,"spontaneous_committed")),1)
        self.assertEqual(len(events(e,"g5_opportunity_resolved")),1)

    def test_17_cautious_step_requires_no_OA_and_costs_double_MP(self):
        e,g,m,a=scene()
        self.assertTrue(g.opportunity_step("mover",(0,-1),decisions={},
                                           cautious=True))
        self.assertEqual(m.mp_remaining,8)
        self.assertEqual(a.opportunity_used,0)

    def test_18_no_direct_replay_without_live_G0_spontaneous_callback(self):
        e,g,m,a=scene()
        tr=Trigger("fabricated","mover","mover")
        resp=Response("alpha","opportunity","g5:ordinary_sword_offturn")
        before=(len(e.ledger),m.hp,a.opportunity_used)
        with self.assertRaises(UnresolvedDecision):
            g.resolve_opportunity(tr,resp,
                OpportunityChoice("B06-AT-03",12,damage_face=4))
        self.assertEqual((len(e.ledger),m.hp,a.opportunity_used),before)

    def test_19_source_witness_matrix_nine_replay_exact_S_T_F(self):
        m=run_matrix()
        self.assertEqual(m["case_count"],9)
        for focus in ("High","Medium","Low"):
            for level in (1,2,3):
                with self.subTest(focus=focus,level=level):
                    r=run_case(focus=focus,level=level)
                    self.assertEqual(r["metrics"]["resolved_offturn_responses"],2)
                    self.assertEqual(r["metrics"]["hit_receipts"],1)
                    self.assertEqual(r["metrics"]["invented_offturn_ap"],0)
                    self.assertEqual(r["metrics"]["native_rounds_complete"],1)
                    self.assertEqual(attest_case(json.loads(json.dumps(r)),
                                                 focus=focus,level=level),r)
                    self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))

    def test_20_rehashed_report_forgery_does_not_pass_source_native_replay(self):
        original=run_case(focus="Medium",level=2,seed=0)
        fake=deepcopy(original)
        fake["metrics"]["hit_receipts"]=0
        fake["audit_sha256"]=canonical_digest({
            k:v for k,v in fake.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_case(fake,focus="Medium",level=2,seed=0)
        fake=deepcopy(original)
        fake["ledger"][0]["kind"]="ghost"
        fake["ledger_sha256"]=canonical_digest(fake["ledger"])
        fake["audit_sha256"]=canonical_digest({
            k:v for k,v in fake.items() if k!="audit_sha256"})
        with self.assertRaises(AssertionError):
            attest_case(fake,focus="Medium",level=2,seed=0)


    def test_21_sentry_cold_source_normal_sword_is_live_offturn(self):
        mover=party_actor("F",2,"mover","party",occupied=((2,2),))
        sentry=enemy_actor("B06-EN-01","sentry","enemy",
                           start_state="cold_start",occupied=((3,2),))
        e=Encounter([mover,sentry],{"mover":40,"sentry":30},
                    seed=0,scenario="offturn-native-sentry-cold",
                    policy="cold_source",objective="ordinary_sword")
        GridMovement(e,width=7,height=7)
        RangedCombat(e)
        SpellState(e)
        DamageState(e)
        g5=SourceMelee(e)
        e.begin_round()
        g5.bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(g5.opportunity_step("mover",(0,-1),decisions={
            "sentry":OpportunityChoice("B06-AT-01",12,
                                       damage_face=1,wound_location_roll=8)}))
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),1)
        self.assertEqual(events(e,"g5_opportunity_roll")[0]
                         ["detail"]["profile"],"B06-AT-01")
        self.assertEqual(sentry.opportunity_used,1)

    def test_22_sentry_cold_cannot_smuggle_enhanced_reserved_profile(self):
        mover=party_actor("F",2,"mover","party",occupied=((2,2),))
        sentry=enemy_actor("B06-EN-01","sentry","enemy",
                           start_state="cold_start",occupied=((3,2),))
        e=Encounter([mover,sentry],{"mover":40,"sentry":30},
                    seed=0,scenario="offturn-native-sentry-not-prepared",
                    policy="cold_source",objective="reserved_profile_rejected")
        GridMovement(e,width=7,height=7)
        RangedCombat(e)
        SpellState(e)
        DamageState(e)
        g5=SourceMelee(e)
        e.begin_round()
        g5.bridge.start_next_turn(RegenerationChoice())
        before=(sentry.opportunity_used,mover.mp_remaining,len(e.ledger))
        with self.assertRaises((ValueError,UnresolvedDecision)):
            g5.opportunity_step("mover",(0,-1),decisions={
                "sentry":OpportunityChoice("B06-AT-02",12,damage_face=4,
                                            vigor_die=4,wound_location_roll=8)})
        self.assertEqual((sentry.opportunity_used,mover.mp_remaining,
                          len(e.ledger)),before)


    def test_23_high_carried_dagger_cannot_guard_real_offturn_attack(self):
        e,g,m,a=scene(role="F")
        original=(m.guard_remaining,a.opportunity_used,
                  m.mp_remaining,len(e.ledger))
        with self.assertRaises((ValueError,UnresolvedDecision)):
            g.opportunity_step("mover",(0,-1),decisions={
                "alpha":OpportunityChoice("B06-AT-03",2,"guard")})
        self.assertEqual((m.guard_remaining,a.opportunity_used,
                          m.mp_remaining,len(e.ledger)),original)


    def test_24_second_dodge_uses_pressure_from_first_response(self):
        e,g,m,a=scene(role="S",two=True)
        hp=m.hp
        self.assertTrue(g.opportunity_step("mover",(0,1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",2,"dodge"),
            # 8+6=14 misses the ORIGINAL 14, but hits the REAL next
            # Dodge value 12 after alpha's paid Dodge pressure.
            "beta":OpportunityChoice("B06-AT-03",8,"dodge",
                                     damage_face=1,wound_location_roll=8)}))
        self.assertLess(m.hp,hp)
        self.assertEqual(m.dodge_pressure,4)
        self.assertEqual([v["detail"]["defense_value"]
                          for v in events(e,"defense_assigned")],[14,12])
        self.assertEqual([v["detail"]["outcome"]
                          for v in events(e,"g5_opportunity_resolved")],
                         ["miss","hit"])
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),1)

    def test_25_second_dodge_new_hit_missing_die_fails_before_any_payment(self):
        e,g,m,a=scene(role="S",two=True)
        beta=e.actors["beta"]
        before=(m.hp,m.mp_remaining,m.dodge_pressure,m.guard_remaining,
                m.occupied,len(e.ledger),a.opportunity_used,beta.opportunity_used,
                a.reaction_available,beta.reaction_available)
        with self.assertRaises((ValueError,UnresolvedDecision)):
            g.opportunity_step("mover",(0,1),decisions={
                "alpha":OpportunityChoice("B06-AT-03",2,"dodge"),
                "beta":OpportunityChoice("B06-AT-03",8,"dodge")})
        self.assertEqual((m.hp,m.mp_remaining,m.dodge_pressure,m.guard_remaining,
                          m.occupied,len(e.ledger),a.opportunity_used,
                          beta.opportunity_used,a.reaction_available,
                          beta.reaction_available),before)
        self.assertEqual(len(events(e,"g5_opportunity_resolved")),0)

    def test_26_two_guards_with_one_capacity_fail_atomically(self):
        e,g,m,a=scene(role="S",two=True,level=1)
        beta=e.actors["beta"]
        self.assertEqual(m.guard_remaining,1)
        before=(m.hp,m.guard_remaining,m.mp_remaining,m.occupied,
                len(e.ledger),a.opportunity_used,beta.opportunity_used,
                a.reaction_available,beta.reaction_available)
        with self.assertRaises((ValueError,UnresolvedDecision)):
            g.opportunity_step("mover",(0,1),decisions={
                "alpha":OpportunityChoice("B06-AT-03",2,"guard"),
                "beta":OpportunityChoice("B06-AT-03",2,"guard")})
        self.assertEqual((m.hp,m.guard_remaining,m.mp_remaining,m.occupied,
                          len(e.ledger),a.opportunity_used,beta.opportunity_used,
                          a.reaction_available,beta.reaction_available),before)

    def test_27_second_hit_cumulative_wound_requirement_precommitted(self):
        e,g,m,a=scene(role="F",two=True,level=1)
        beta=e.actors["beta"]
        before=(m.hp,m.occupied,m.mp_remaining,len(e.ledger),
                a.opportunity_used,beta.opportunity_used)
        # Both noncritical source Sword hits individually leave a fresh
        # 12-HP target alive. In sequence they cross zero only on hit two.
        with self.assertRaises((ValueError,UnresolvedDecision)):
            g.opportunity_step("mover",(0,1),decisions={
                "alpha":OpportunityChoice("B06-AT-03",12,damage_face=6),
                "beta":OpportunityChoice("B06-AT-03",12,damage_face=6)})
        self.assertEqual((m.hp,m.occupied,m.mp_remaining,len(e.ledger),
                          a.opportunity_used,beta.opportunity_used),before)
        self.assertEqual(len(events(e,"g4_damage_applied")),0)
        self.assertFalse(g.opportunity_step("mover",(0,1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",12,damage_face=6),
            "beta":OpportunityChoice("B06-AT-03",12,damage_face=6,
                                     wound_location_roll=8)}))
        self.assertLessEqual(m.hp,0)
        self.assertEqual(m.occupied,((2,2),))
        self.assertEqual(len(events(e,"g4_damage_applied")),2)
        self.assertEqual(len(events(e,"g4_wound_created")),1)
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),2)

    def test_28_second_dodge_confirmation_changes_critical_tier(self):
        e,g,m,a=scene(role="S",two=True)
        beta=e.actors["beta"]
        before=(m.hp,m.dodge_pressure,m.mp_remaining,len(e.ledger),
                a.opportunity_used,beta.opportunity_used)
        with self.assertRaises((ValueError,UnresolvedDecision)):
            g.opportunity_step("mover",(0,1),decisions={
                "alpha":OpportunityChoice("B06-AT-03",2,"dodge"),
                # 7+6=13 confirms only after Dodge falls 14 -> 12:
                # real Critical requires TWO d4, not the stale Strong one.
                "beta":OpportunityChoice("B06-AT-03",20,"dodge",
                    damage_face=1,confirmation_face=7,
                    critical_dice=(4,),wound_location_roll=8)})
        self.assertEqual((m.hp,m.dodge_pressure,m.mp_remaining,len(e.ledger),
                          a.opportunity_used,beta.opportunity_used),before)
        self.assertFalse(g.opportunity_step("mover",(0,1),decisions={
            "alpha":OpportunityChoice("B06-AT-03",2,"dodge"),
            "beta":OpportunityChoice("B06-AT-03",20,"dodge",
                damage_face=1,confirmation_face=7,
                critical_dice=(4,4),wound_location_roll=8)}))
        rolls=events(e,"g5_opportunity_roll")
        self.assertEqual([r["detail"]["critical"] for r in rolls],
                         ["normal","critical"])
        self.assertEqual(len(events(e,"g45_opportunity_attested_hit")),1)


if __name__=="__main__":
    unittest.main()
