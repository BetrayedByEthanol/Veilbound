"""G4.5: bounded real-turn injury continuation + frozen wound-witness register."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, Wound,
    enemy_actor, party_actor)
from scripts.b06_damage_v0 import DamageState, DamagePacket
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_wound_continuation_v0 import (
    WoundContinuation, historical_phase3_wound_witnesses)


def scene(*,soldier=True,sentry=True):
    actors=[]
    if soldier:
        actors.append(enemy_actor("B06-EN-02","soldier","enemy",
                                  occupied=((3,2),)))
    if sentry:
        actors.append(enemy_actor("B06-EN-01","sentry","party",
                                  start_state="cold_start",occupied=((4,2),)))
    e=Encounter(actors,{a.id:100-i for i,a in enumerate(actors)},
                seed=451,scenario="G45-I1-source-bounded",
                policy="external_G5_attested_actions_and_choices")
    SpellState(e)
    d=DamageState(e)
    e.begin_round()
    return e,d,WoundContinuation(e)


def begin_attack(e,bridge,*,target="sentry"):
    bridge.start_next_turn(RegenerationChoice())
    idx=len(e.ledger)
    # G0's actual declaration locks the attacker, target, profile, AP and
    # pre-roll defense. A free-form spend_ap label is NOT an attack.
    e.declare_sequence("soldier",target,("B06-AT-03",),("take_hit",))
    return idx


def hit(e,bridge,idx,**kw):
    return bridge.verified_profile_hit(
        "soldier","sentry","B06-AT-03",
        action_index=idx,source_event=kw.pop("source_event","hit-1"),
        contact_reference="G5:test:independent_sword_contact",
        defense_reference="G5:test:resolved_sentry_defense",
        contact_verified=kw.pop("contact_verified",True),
        defense_verified=kw.pop("defense_verified",True),
        die_face=kw.pop("die_face",1),
        critical=kw.pop("critical","devastating"),
        critical_dice=kw.pop("critical_dice",(1,1)),
        wound_location_roll=kw.pop("wound_location_roll",14),**kw)


class WoundContinuationTests(unittest.TestCase):
    def test_01_legal_source_hit_creates_wound_then_five_genuine_repairs(self):
        e,d,b=scene()
        idx=begin_attack(e,b)
        result=hit(e,b,idx)
        target=e.actors["sentry"]
        self.assertEqual(result["wound"],"Critical")
        self.assertEqual(target.hp,6)
        self.assertEqual(len(target.wounds),1)
        w=target.wounds[0]
        self.assertEqual((w.requirement,w.location,w.progress),
                         (30,"Arm",0))
        self.assertEqual(len(b.report()["verified_hits"]),1)
        b.end_current_turn()
        for round_no in range(5):
            b.start_next_turn(RegenerationChoice(repair=6))
            self.assertEqual(w.progress,6*(round_no+1))
            self.assertEqual(target.vigor,36-6*(round_no+1))
            self.assertEqual(target.hp,6)
            b.end_current_turn()
            if round_no<4:
                b.begin_next_round()
                b.start_next_turn(RegenerationChoice())
                b.end_current_turn()
        report=b.report()
        self.assertEqual(report["native_step2_count"],10)
        self.assertEqual(len(report["wound_creation_events"]),1)
        self.assertEqual(report["current"]["actors"]["sentry"]["wounds"][0]["progress"],30)
        self.assertTrue(report["current"]["actors"]["sentry"]["wounds"][0]["completed"])
        self.assertEqual(report["g4_damage_events"][0],w.source_event)
        self.assertIsNone(report["winner"])
        self.assertFalse(report["complete_encounter_certified"])
        self.assertFalse(report["recorded_dead"])
        e.check()

    def test_02_dying_survival_plus_oldest_wound_repair_is_real_step2(self):
        e,d,b=scene(soldier=False)
        actor=e.actors["sentry"]
        actor.hp=-1
        actor.wounds=[Wound("old",10,8),Wound("new",20,0)]
        b.start_next_turn(RegenerationChoice(cancel_dying_loss=True,repair=5))
        self.assertEqual(actor.hp,-1)
        self.assertEqual(actor.vigor,30)
        self.assertEqual([w.progress for w in actor.wounds],[10,3])
        self.assertEqual(b.report()["native_step2_count"],1)
        self.assertEqual([x["kind"] for x in e.ledger
                          if x["kind"]=="regeneration_step"],["regeneration_step"])
        self.assertEqual(actor.ap_remaining,0)
        b.end_current_turn()
        self.assertEqual(b.report()["current"]["actors"]["sentry"]["dying"],True)
        e.check()

    def test_03_unselected_dying_step_and_zero_vigor_do_not_free_heal(self):
        e,d,b=scene(soldier=False)
        actor=e.actors["sentry"]
        actor.hp=0
        actor.vigor=1
        actor.wounds=[Wound("w",10,0)]
        with self.assertRaises(UnresolvedDecision):
            b.start_next_turn()  # No specified survival/repair allocation.
        self.assertEqual(actor.hp,0)
        self.assertEqual(actor.vigor,1)
        self.assertEqual(b.report()["native_step2_count"],0)
        self.assertEqual(e.pending_regeneration,"sentry")
        b.start_next_turn(RegenerationChoice(cancel_dying_loss=True))
        self.assertEqual((actor.hp,actor.vigor), (0,0))
        b.end_current_turn()
        b.begin_next_round()
        b.start_next_turn(RegenerationChoice())  # No Vigor = real Dying loss.
        self.assertEqual(actor.hp,-1)
        self.assertEqual(actor.vigor,0)
        b.end_current_turn()
        self.assertEqual(b.report()["native_step2_count"],2)
        e.check()

    def test_04_duplicated_or_unattested_contact_cannot_invent_wound(self):
        e,d,b=scene()
        idx=begin_attack(e,b)
        before=(e.actors["sentry"].hp,len(e.actors["sentry"].wounds))
        with self.assertRaises(UnresolvedDecision):
            hit(e,b,idx,contact_verified=False)
        self.assertEqual((e.actors["sentry"].hp,
                          len(e.actors["sentry"].wounds)),before)
        with self.assertRaises(UnresolvedDecision):
            hit(e,b,idx,wound_location_roll=None)
        self.assertEqual((e.actors["sentry"].hp,
                          len(e.actors["sentry"].wounds)),before)
        hit(e,b,idx)
        with self.assertRaises(ValueError):
            hit(e,b,idx,source_event="hit-2")
        with self.assertRaises(ValueError):
            hit(e,b,idx)
        self.assertEqual(len(e.actors["sentry"].wounds),1)
        self.assertEqual(len(b.report()["verified_hits"]),1)
        e.check()

    def test_05_death_threshold_not_a_victory_or_extra_repairable_wound(self):
        e,d,b=scene()
        e.actors["sentry"].hp=1
        idx=begin_attack(e,b)
        result=hit(e,b,idx,source_event="fatal-1",
                   die_face=6,critical_dice=(4,4))
        a=e.actors["sentry"]
        self.assertTrue(result["dead"])
        self.assertEqual(a.hp,-a.hp_max)
        self.assertEqual(a.wounds,[])
        report=b.report()
        self.assertEqual(report["recorded_dead"],["sentry"])
        self.assertEqual(report["wound_creation_events"],[])
        self.assertFalse(report["complete_encounter_certified"])
        self.assertIsNone(report["winner"])
        with self.assertRaisesRegex(ValueError,"Dead recipient"):
            d.apply_damage("sentry",(DamagePacket("hp","Fire",1),),
                           event_key="after-death",cause="illegal")
        e.check()

    def test_06_unresolved_policy_not_backfilled_as_withdrawal(self):
        e,d,b=scene()
        outcome=b.mark_unresolved("g5_retreat_geometry",
                   source_reference="G5:unresolved_exit",
                   detail="No legal G1 path and Opportunity proof for escape")
        self.assertEqual(outcome["status"],"unresolved")
        with self.assertRaises(UnresolvedDecision):
            b.attest_withdrawal("sentry",movement_event_index=0,
                exit_policy_reference="G6:retreat-claimed",
                independently_verified=True)
        with self.assertRaises(ValueError):
            b.mark_unresolved("invented_blessed_exit",
                    source_reference="GM",detail="fabricated")
        report=b.report()
        self.assertEqual(report["explicit_outcomes"],[outcome])
        self.assertIsNone(report["winner"])
        e.check()

    def test_07_no_instant_resurrection_or_virtual_regen_in_exploration(self):
        e,d,b=scene(soldier=False)
        a=e.actors["sentry"]
        a.hp=1
        d.apply_damage("sentry",(DamagePacket("hp","Fire",2),),
                       event_key="observed_fire",cause="confirmed_fire",
                       wound_location_roll=2)
        self.assertEqual(a.hp,-1)
        self.assertEqual(len(a.wounds),1)
        b.d.clock.advance_exploration(60)
        self.assertEqual(a.hp,-1)
        self.assertEqual(a.wounds[0].progress,0)
        self.assertEqual(b.report()["native_step2_count"],0)
        self.assertTrue(b.report()["current"]["actors"]["sentry"]["dying"])
        e.check()

    def test_08_phase3_wound_witnesses_classified_not_claimed_completed(self):
        rows=historical_phase3_wound_witnesses()
        self.assertEqual(len(rows),22)
        self.assertEqual(len({r["witness_key"] for r in rows}),22)
        self.assertEqual(len({tuple(r["source_tuple"]) for r in rows}),22)
        self.assertTrue(all(r["source_terminal"]=="wound_unresolved"
                            and r["classification"].startswith("unresolved_")
                            and not r["g4_damage_replayed"]
                            and not r["historical_census_mutated"]
                            and not r["encounter_certified"]
                            and len(r["source_trial_sha256"])==64 for r in rows))
        from scripts.b06_hunter_tactical_diversity_v0 import trial
        for r in rows[::5]:
            self.assertEqual(trial(*r["source_tuple"])["terminal"],
                             "wound_unresolved")

    def test_09_g45_source_digest_and_event_ledger_provenance(self):
        e,d,b=scene()
        idx=begin_attack(e,b)
        result=hit(e,b,idx,source_event="melee-proof-3",
                   critical="normal",critical_dice=(),die_face=3,
                   wound_location_roll=None)
        self.assertEqual(result["hp_loss"],6)
        record=b.report()["verified_hits"][0]
        self.assertEqual(record["source_event"],"melee-proof-3")
        self.assertEqual(record["action_index"],idx)
        self.assertEqual(record["attacker_source"],
                         e.actors["soldier"].source.digest)
        self.assertEqual(record["target_source"],
                         e.actors["sentry"].source.digest)
        self.assertEqual(len(e.actors["sentry"].wounds),0)
        self.assertEqual(b.report()["wound_creation_events"],[])
        e.check()


    def test_10_i1_soldier_against_low_life_priest_wound_to_repair(self):
        soldier=enemy_actor("B06-EN-02","soldier","enemy",
                            occupied=((3,2),))
        front=party_actor("A",3,"front","party",occupied=((4,2),))
        e=Encounter([soldier,front],{"soldier":100,"front":90},
                    seed=451,scenario="G45-I1-soldier-vs-low-life",
                    policy="G5_contact_and_defense_independently_attested")
        SpellState(e)
        DamageState(e)
        e.begin_round()
        b=WoundContinuation(e)
        b.start_next_turn(RegenerationChoice())
        action_index=len(e.ledger)
        e.declare_sequence("soldier","front",("B06-AT-03",),("take_hit",))
        attack=b.verified_profile_hit("soldier","front","B06-AT-03",
                   action_index=action_index,source_event="I1:source_hit:1",
                   contact_reference="G5:I1:external_contact:1",
                   defense_reference="G5:I1:external_defense:1",
                   contact_verified=True,defense_verified=True,
                   die_face=1,critical="devastating",critical_dice=(1,1),
                   wound_location_roll=14)
        self.assertEqual(attack["wound"],"Critical")
        self.assertEqual(front.hp,6)
        self.assertEqual(front.wounds[0].requirement,30)
        b.end_current_turn()
        for i in range(5):
            b.start_next_turn(RegenerationChoice(repair=6))
            self.assertEqual(front.wounds[0].progress,6*(i+1))
            b.end_current_turn()
            if i<4:
                b.begin_next_round()
                b.start_next_turn(RegenerationChoice())
                b.end_current_turn()
        self.assertEqual(front.vigor,front.vigor_max-30)
        self.assertEqual(len(b.report()["wound_creation_events"]),1)
        self.assertEqual(b.report()["native_step2_count"],10)
        self.assertIsNone(b.report()["winner"])
        self.assertFalse(b.report()["complete_encounter_certified"])
        e.check()



    def test_11_historical_committed_action_cannot_be_spent_next_round(self):
        e,d,b=scene()
        stale=begin_attack(e,b)
        b.end_current_turn()
        b.start_next_turn(RegenerationChoice())
        b.end_current_turn()
        b.begin_next_round()
        b.start_next_turn(RegenerationChoice())
        current=len(e.ledger)
        e.declare_sequence("soldier","sentry",("B06-AT-03",),("take_hit",))
        before=(e.actors["sentry"].hp,len(e.actors["sentry"].wounds))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "genuine committed Physical Action"):
            hit(e,b,stale,source_event="stale-previous-round",
                critical="normal",critical_dice=(),die_face=3,
                wound_location_roll=None)
        self.assertEqual((e.actors["sentry"].hp,
                          len(e.actors["sentry"].wounds)),before)
        self.assertEqual(len(b.report()["verified_hits"]),0)
        r=hit(e,b,current,source_event="new-actual-hit",
              critical="normal",critical_dice=(),die_face=3,
              wound_location_roll=None)
        self.assertEqual(r["hp_loss"],6)
        self.assertEqual(len(b.report()["verified_hits"]),1)
        self.assertEqual(b.report()["verified_hits"][0]["action_index"],current)
        e.check()



    def test_12_duplicate_source_event_rejected_across_bridge_instances(self):
        e,d,first=scene()
        initial=begin_attack(e,first)
        first_hit=hit(e,first,initial,source_event="shared-external-evidence",
                      critical="normal",critical_dice=(),die_face=1,
                      wound_location_roll=None)
        self.assertEqual(first_hit["hp_loss"],4)
        first.end_current_turn()
        first.start_next_turn(RegenerationChoice())
        first.end_current_turn()
        first.begin_next_round()
        later=WoundContinuation(e)
        later.start_next_turn(RegenerationChoice())
        next_index=len(e.ledger)
        e.declare_sequence("soldier","sentry",("B06-AT-03",),("take_hit",))
        prior=(e.actors["sentry"].hp, e.actors["sentry"].vigor,
               len(e.actors["sentry"].wounds),
               sum(x["kind"]=="g4_damage_applied" for x in e.ledger))
        with self.assertRaisesRegex(ValueError,
                                    "Source event already consumed in encounter"):
            hit(e,later,next_index,source_event="shared-external-evidence",
                critical="normal",critical_dice=(),die_face=1,
                wound_location_roll=None)
        self.assertEqual(
            (e.actors["sentry"].hp, e.actors["sentry"].vigor,
             len(e.actors["sentry"].wounds),
             sum(x["kind"]=="g4_damage_applied" for x in e.ledger)),prior)
        self.assertFalse(later.report()["verified_hits"])
        self.assertEqual(sum(x["kind"]=="g45_attested_hit" and
                             x["detail"]["source_event"]=="shared-external-evidence"
                             for x in e.ledger),1)
        # Failed duplicate does not consume the new legally committed action.
        legal=hit(e,later,next_index,source_event="new-external-evidence",
                  critical="normal",critical_dice=(),die_face=1,
                  wound_location_roll=None)
        self.assertEqual(legal["hp_loss"],4)
        self.assertEqual(len(later.report()["verified_hits"]),1)
        e.check()

    def test_13_g1_cancelled_reserved_and_pivot_not_withdrawal(self):
        e,d,b=scene(soldier=False)
        movement=GridMovement(e,width=12,height=8)
        b.start_next_turn(RegenerationChoice())
        original=e.actors["sentry"].occupied
        # These G1 ledger kinds are meaningful, but do not demonstrate
        # displacement. They must not be usable to fabricate an exit.
        bad=[
            ("g1_reserved_mp_expired",{"label":"unused","returned_mp":3}),
            ("g1_step_cancelled",{"trigger":"cancelled","reason":"blocked"}),
            ("g1_segment_break",{"reason":"new_segment"}),
            ("g1_movement_step",{"old":original,"new":original,
                                  "step_kind":"pivot"}),
        ]
        for kind,facts in bad:
            index=len(e.ledger)
            e.log(kind,actor="sentry",**facts)
            with self.subTest(kind=kind):
                with self.assertRaisesRegex(UnresolvedDecision,
                                            "no completed actor-linked G1 translation"):
                    b.attest_withdrawal("sentry",
                        movement_event_index=index,
                        exit_policy_reference="G6:verified_boundary_exit",
                        independently_verified=True)
        self.assertEqual(b.report()["explicit_outcomes"],[])
        self.assertEqual(e.actors["sentry"].occupied,original)
        self.assertTrue(movement.step("sentry",(1,0)))
        idx=len(e.ledger)-1
        self.assertEqual(e.ledger[idx]["kind"],"g1_movement_step")
        valid=b.attest_withdrawal("sentry",movement_event_index=idx,
                   exit_policy_reference="G6:verified_boundary_exit",
                   independently_verified=True)
        self.assertEqual(valid["status"],"withdrawal_attested")
        self.assertEqual(b.report()["explicit_outcomes"],[valid])
        e.check()

    def test_14_allied_transit_requires_atomic_route_finish(self):
        sentry=enemy_actor("B06-EN-01","sentry","party",
                           start_state="cold_start",occupied=((1,1),))
        ally=party_actor("A",3,"ally","party",occupied=((2,1),))
        e=Encounter([sentry,ally],{"sentry":100,"ally":90},
                    seed=452,scenario="G45-G1-completed-route",
                    policy="attested_departure_not_victory")
        SpellState(e)
        DamageState(e)
        movement=GridMovement(e,width=12,height=8)
        e.begin_round()
        bridge=WoundContinuation(e)
        bridge.start_next_turn(RegenerationChoice())
        self.assertTrue(movement.move_route("sentry",((1,0),(1,0))))
        transit=[x for x in e.ledger if x["kind"]=="g1_allied_transit_step"]
        self.assertEqual(len(transit),2)
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "no completed actor-linked G1 translation"):
            bridge.attest_withdrawal("sentry",
                movement_event_index=transit[-1]["index"],
                exit_policy_reference="G6:actual_exit_policy",
                independently_verified=True)
        finished=next(x for x in e.ledger
                      if x["kind"]=="g1_allied_transit_finished")
        self.assertEqual(sentry.occupied,((3,1),))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "no completed actor-linked G1 translation"):
            bridge.attest_withdrawal("ally",
                movement_event_index=finished["index"],
                exit_policy_reference="G6:actual_exit_policy",
                independently_verified=True)
        success=bridge.attest_withdrawal("sentry",
                movement_event_index=finished["index"],
                exit_policy_reference="G6:actual_exit_policy",
                independently_verified=True)
        self.assertEqual(success["status"],"withdrawal_attested")
        self.assertEqual(success["movement_event_index"],finished["index"])
        self.assertEqual(len(bridge.report()["explicit_outcomes"]),1)
        self.assertIsNone(bridge.report()["winner"])
        e.check()

    def test_15_cached_witness_results_are_independent_deep_copies(self):
        from copy import deepcopy

        first=historical_phase3_wound_witnesses()
        baseline=deepcopy(first)
        self.assertEqual(len(first),22)
        self.assertIsInstance(first,tuple)
        self.assertIsInstance(first[0]["source_tuple"],tuple)
        self.assertFalse(first[0]["encounter_certified"])
        self.assertEqual(len(first[0]["next_required_authority"]),4)

        # A caller may freely annotate an experimental copy, including
        # nested collections, without rewriting the frozen shared evidence.
        first[0]["encounter_certified"]=True
        first[0]["witness_key"]="tampered"
        first[0]["next_required_authority"][0]="fabricated policy"
        first[0]["next_required_authority"].append("invented outcome")
        first[1]["g4_damage_replayed"]=True
        first[1]["next_required_authority"].clear()

        second=historical_phase3_wound_witnesses()
        third=historical_phase3_wound_witnesses()
        self.assertEqual(second,baseline)
        self.assertEqual(third,baseline)
        self.assertIsNot(first,second)
        self.assertIsNot(second,third)
        self.assertIsNot(first[0],second[0])
        self.assertIsNot(first[0]["next_required_authority"],
                         second[0]["next_required_authority"])
        self.assertFalse(second[0]["encounter_certified"])
        self.assertFalse(second[1]["g4_damage_replayed"])
        self.assertEqual(len({r["witness_key"] for r in second}),22)
        # Mutating the second result must not mutate the first or third.
        second[2]["next_required_authority"].pop()
        self.assertEqual(third[2],baseline[2])



    def test_16_interception_reservation_is_not_a_paid_attack(self):
        e,d,b=scene()
        b.start_next_turn(RegenerationChoice())
        idx=len(e.ledger)
        e.reserve("soldier","future-window","protect-ally",
                  action_kind="physical")
        self.assertEqual(e.ledger[idx]["detail"]["action_class"],"physical")
        self.assertTrue(any(x["kind"]=="interception_reserved"
                            for x in e.ledger[idx+1:]))
        before=(e.actors["sentry"].hp,e.actors["sentry"].vigor,
                len(e.actors["sentry"].wounds),e.actors["soldier"].ap_remaining,
                len(e.reservations))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "source-bound attack sequence declaration"):
            hit(e,b,idx,source_event="not-an-attack",
                critical="normal",critical_dice=(),die_face=3,
                wound_location_roll=None)
        self.assertEqual(
            (e.actors["sentry"].hp,e.actors["sentry"].vigor,
             len(e.actors["sentry"].wounds),e.actors["soldier"].ap_remaining,
             len(e.reservations)),before)
        self.assertEqual(len(b.report()["verified_hits"]),0)
        self.assertEqual(e.reservations[0].label,"protect-ally")
        self.assertFalse(any(x["kind"]=="g4_profile_hit" for x in e.ledger))
        e.check()

    def test_17_arbitrary_spend_label_cannot_impersonate_source_sequence(self):
        e,d,b=scene()
        b.start_next_turn(RegenerationChoice())
        idx=len(e.ledger)
        e.spend_ap("soldier","physical",label="sequence:B06-AT-03:0")
        before=(e.actors["sentry"].hp,len(e.actors["sentry"].wounds))
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "source-bound attack sequence declaration"):
            hit(e,b,idx,source_event="label-spoof",
                critical="normal",critical_dice=(),die_face=3,
                wound_location_roll=None)
        self.assertEqual((e.actors["sentry"].hp,
                          len(e.actors["sentry"].wounds)),before)
        self.assertFalse(b.report()["verified_hits"])
        e.check()

    def test_18_declaration_target_must_match_resolved_target(self):
        e,d,b=scene()
        idx=begin_attack(e,b)
        before=(e.actors["sentry"].hp,e.actors["soldier"].hp)
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "declaration does not match target/profile"):
            b.verified_profile_hit(
                "soldier","soldier","B06-AT-03",action_index=idx,
                source_event="wrong-target",
                contact_reference="G5:own-sword",defense_reference="G5:self",
                contact_verified=True,defense_verified=True,die_face=3,
                critical="normal",critical_dice=())
        self.assertEqual((e.actors["sentry"].hp,e.actors["soldier"].hp),before)
        self.assertFalse(b.report()["verified_hits"])
        good=hit(e,b,idx,source_event="correct-target",
                 critical="normal",critical_dice=(),die_face=3,
                 wound_location_roll=None)
        self.assertEqual(good["hp_loss"],6)
        e.check()

    def test_19_declaration_profile_must_match_resolved_profile(self):
        e,d,b=scene()
        idx=begin_attack(e,b)
        before=(e.actors["sentry"].hp,e.actors["sentry"].vigor)
        with self.assertRaisesRegex(UnresolvedDecision,
                                    "does not match declared target/profile"):
            b.verified_profile_hit(
                "soldier","sentry","B06-AT-01",action_index=idx,
                source_event="wrong-profile",
                contact_reference="G5:wrong-profile",
                defense_reference="G5:take-hit",
                contact_verified=True,defense_verified=True,die_face=3,
                critical="normal",critical_dice=())
        self.assertEqual((e.actors["sentry"].hp,e.actors["sentry"].vigor),
                         before)
        good=hit(e,b,idx,source_event="right-profile",
                 critical="normal",critical_dice=(),die_face=3,
                 wound_location_roll=None)
        self.assertEqual(good["hp_loss"],6)
        self.assertFalse(any(x["detail"].get("source_event")=="wrong-profile"
                             for x in e.ledger if x["kind"]=="g45_attested_hit"))
        e.check()

    def test_20_two_attacks_in_one_source_sequence_bind_separate_payments(self):
        sentry=enemy_actor("B06-EN-01","sentry","party",
                            start_state="cold_start",occupied=((3,2),))
        soldier=enemy_actor("B06-EN-02","soldier","enemy",
                             occupied=((4,2),))
        e=Encounter([sentry,soldier],{"sentry":100,"soldier":90},
                    seed=456,scenario="G45-double-sentry-sequence",
                    policy="independently_attested_G5_hits")
        SpellState(e)
        DamageState(e)
        e.begin_round()
        b=WoundContinuation(e)
        b.start_next_turn(RegenerationChoice())
        initial_ap=sentry.ap_remaining
        before=len(e.ledger)
        e.declare_sequence("sentry","soldier",
                           ("B06-AT-01","B06-AT-01"),
                           ("take_hit","take_hit"))
        actions=[x for x in e.ledger[before:]
                 if x["kind"]=="action_committed"]
        self.assertEqual(len(actions),2)
        self.assertEqual(sentry.ap_remaining,initial_ap-40)
        for i,action in enumerate(actions):
            result=b.verified_profile_hit(
                "sentry","soldier","B06-AT-01",
                action_index=action["index"],source_event=f"two-hit-{i}",
                contact_reference=f"G5:contact:{i}",
                defense_reference=f"G5:defense:{i}",
                contact_verified=True,defense_verified=True,
                die_face=1,critical="normal",critical_dice=())
            self.assertEqual(result["hp_loss"],2)
        self.assertEqual(soldier.hp,soldier.hp_max-4)
        self.assertEqual(sentry.ap_remaining,initial_ap-40)
        hits=b.report()["verified_hits"]
        self.assertEqual([h["declared_profile_index"] for h in hits],[0,1])
        self.assertEqual([h["action_index"] for h in hits],
                         [a["index"] for a in actions])
        self.assertEqual(hits[0]["sequence_declaration_index"],
                         hits[1]["sequence_declaration_index"])
        with self.assertRaisesRegex(ValueError,"already consumed"):
            b.verified_profile_hit(
                "sentry","soldier","B06-AT-01",
                action_index=actions[0]["index"],source_event="third-hit",
                contact_reference="G5:no-duplicate",
                defense_reference="G5:no-duplicate",
                contact_verified=True,defense_verified=True,
                die_face=1,critical="normal",critical_dice=())
        self.assertEqual(len(b.report()["verified_hits"]),2)
        e.check()

if __name__=="__main__":
    unittest.main()
