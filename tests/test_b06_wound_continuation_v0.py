"""G4.5: bounded real-turn injury continuation + frozen wound-witness register."""
import unittest

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, Wound,
    enemy_actor, party_actor)
from scripts.b06_damage_v0 import DamageState, DamagePacket
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


def begin_attack(e,bridge):
    bridge.start_next_turn(RegenerationChoice())
    idx=len(e.ledger)
    e.spend_ap("soldier","physical",label="G5:attested_sword_thrust")
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
        e.spend_ap("soldier","physical",label="G5:verified_sword")
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
        e.spend_ap("soldier","physical",label="G5:fresh_action")
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


if __name__=="__main__":
    unittest.main()
