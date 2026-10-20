"""G4.4 Hunter timing and Venom Endurance bounded executable regression."""
import unittest
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, party_actor, enemy_actor, UnresolvedDecision)
from scripts.b06_damage_v0 import DamageState
from scripts.b06_hunter_venom_endurance_v0 import HUNTER


def scene(*,target_role="F",with_caster=True):
    victim=party_actor(target_role,3,"victim","party",occupied=((3,1),))
    hunter=enemy_actor("B06-EN-03","hunter","enemy",
                       occupied=((6,1),(5,1)))
    roster=[victim,hunter]
    scores={"victim":80,"hunter":70}
    if with_caster:
        priest=party_actor("A",3,"caster","party",occupied=((1,1),))
        roster.insert(0,priest);scores["caster"]=100
    e=Encounter(roster,scores,seed=444,scenario="G4.4",
                policy="source_attested")
    d=DamageState(e)
    e.begin_round()
    return e,d,d.venom,d.clock


def hit(e,d,*,profile="B06-AT-04",die=3,target="victim"):
    out=d.apply_profile_hit("hunter",target,profile,
                            die_face=die,confirmed_hit=True,
                            wound_location_roll=8)
    assert e.ledger[-1]["kind"]=="g4_profile_hit"
    return e.ledger[-1]["index"],out


def bite(e,d,v,*,key="bite",face=1,profile="B06-AT-04",die=3):
    index,damage=hit(e,d,profile=profile,die=die)
    effect=v.apply_bite("hunter","victim",profile_hit_index=index,
                        exposure_key=key,resistance_die=face)
    return effect,damage


def cast(e,v,*,mode="ward",recipient="victim",price=2,**kwargs):
    return v.cast_endurance("caster",recipient,profile="Single Target",
                             mode=mode,source_authorized=True,
                             source_reference="test:independently_attested_Life_Prayer",
                             ordinary_cost=price,**kwargs)


def whole_round(e):
    if e.current is not None:e.end_turn()
    for who in e.order[e.cursor:]:
        e.start_turn(who,regen_choice=RegenerationChoice())
        e.end_turn()


def entries(e,kind):
    return [x["detail"] for x in e.ledger if x["kind"]==kind]


class G44Regressions(unittest.TestCase):
    def test_01_hunter_full_stages_no_direct_damage_or_saves(self):
        e,d,v,c=scene()
        result,damage=bite(e,d,v,face=1)
        self.assertEqual(result["outcome"],"accepted")
        self.assertTrue(damage["injection_eligible"])
        t=d.toxins.active("victim")
        self.assertEqual(t["profile"],HUNTER)
        self.assertEqual(t["stage"],0)
        self.assertEqual(d.toxins.modifier("victim","mp"),0)
        remaining=e.actors["victim"].hp
        c.advance_exploration(599)
        self.assertEqual(t["stage"],0)
        c.advance_exploration(1)
        self.assertEqual((t["stage"],d.toxins.modifier("victim","mp"),
                          d.toxins.modifier("victim","muscular_strength")),(1,-2,-1))
        c.advance_exploration(1200)
        self.assertEqual((t["stage"],d.toxins.modifier("victim","mp"),
                          d.toxins.modifier("victim","muscular_strength")),(2,-4,-2))
        c.advance_exploration(5400)
        self.assertIsNone(d.toxins.active("victim"))
        self.assertEqual(d.toxins.modifier("victim","mp"),0)
        self.assertEqual(e.actors["victim"].hp,remaining)
        self.assertEqual(len(entries(e,"g44_hunter_milestone")),3)
        self.assertEqual(len(entries(e,"g44_hunter_accepted")),1)
        e.check()

    def test_02_reduced_tie_no_escalation_and_60min_expiry(self):
        e,d,v,c=scene()
        raw=dict(e.actors["victim"].source.abilities)["Vitality"]
        rolled=12-raw
        self.assertTrue(1<=rolled<=20)
        o,_=bite(e,d,v,face=rolled)
        self.assertEqual(o["resolution"],"Reduced")
        self.assertEqual(len(d.toxins.active("victim")["markers"]),2)
        c.advance_exploration(600)
        self.assertEqual(d.toxins.modifier("victim","mp"),-2)
        c.advance_exploration(3000)
        self.assertIsNone(d.toxins.active("victim"))
        self.assertEqual([x["stage"] for x in entries(e,"g44_hunter_milestone")],[1,1])
        e.check()

    def test_03_bite_armor_gate_nonpiercing_and_horn_never_envenom(self):
        e,d,v,c=scene(target_role="B")
        i,damage=hit(e,d,die=1)
        self.assertFalse(damage["injection_eligible"])
        o=v.apply_bite("hunter","victim",profile_hit_index=i,
                       exposure_key="stopped",resistance_die=None)
        self.assertEqual(o["outcome"],"not_delivered")
        self.assertIsNone(d.toxins.active("victim"))
        i,_=hit(e,d,profile="B06-AT-05",die=1)
        with self.assertRaises(UnresolvedDecision):
            v.apply_bite("hunter","victim",profile_hit_index=i,
                         exposure_key="horn",resistance_die=11)
        self.assertIsNone(d.toxins.active("victim"))
        e.check()

    def test_04_pounce_bite_one_entry_and_no_immediate_stage(self):
        e,d,v,c=scene()
        o,_=bite(e,d,v,key="pounce",profile="B06-AT-06")
        self.assertEqual(o["outcome"],"accepted")
        self.assertEqual(d.toxins.active("victim")["stage"],0)
        self.assertEqual(d.toxins.modifier("victim","muscular_strength"),0)
        self.assertEqual(len(entries(e,"g44_hunter_accepted")),1)
        e.check()

    def test_05_same_grade_repeat_does_not_reset_milestones_or_save(self):
        e,d,v,c=scene()
        bite(e,d,v,key="first")
        c.advance_exploration(900)
        t=d.toxins.active("victim")
        first_markers=tuple(t["markers"])
        other,damage=bite(e,d,v,key="second",face=20)
        self.assertEqual(other["outcome"],"ignored")
        self.assertEqual(d.toxins.active("victim")["markers"],list(first_markers))
        self.assertEqual(d.toxins.active("victim")["result"],"Full")
        self.assertTrue(damage["hp_loss"]>0)
        c.advance_exploration(900)
        self.assertEqual(d.toxins.active("victim")["stage"],2)
        e.check()

    def test_06_initiative_exposure_exact_round_labels_and_exit(self):
        e,d,v,c=scene()
        c.enter_initiative()
        bite(e,d,v)
        t=d.toxins.active("victim")
        self.assertEqual([c.events[x].due_round for x in t["markers"]],
                         [101,301,1201])
        whole_round(e)
        c.leave_initiative()
        self.assertEqual([c.events[x].due_seconds for x in t["markers"]],
                         [588,1788,7188])
        c.advance_exploration(588)
        self.assertEqual(t["stage"],1)
        c.advance_exploration(1200)
        self.assertEqual(t["stage"],2)
        e.check()

    def test_07_exploration_to_initiative_each_milestone_independent(self):
        e,d,v,c=scene()
        bite(e,d,v)
        c.advance_exploration(598)
        c.enter_initiative()
        t=d.toxins.active("victim")
        self.assertEqual(c.events[t["markers"][0]].due_round,1)
        self.assertEqual(t["stage"],1)  # q0 resolves before actions
        self.assertEqual(c.events[t["markers"][1]].due_round,201)
        self.assertEqual(c.events[t["markers"][2]].due_round,1101)
        e.check()

    def test_08_ward_stops_valid_bite_before_resistance_not_physical_hp(self):
        e,d,v,c=scene()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v)
        self.assertIsNotNone(eid)
        whole_round(e)
        result,damage=bite(e,d,v,face=None)
        self.assertEqual(result["outcome"],"prevented")
        self.assertTrue(damage["hp_loss"]>0)
        self.assertIsNone(d.toxins.active("victim"))
        self.assertFalse(v.effects[eid]["active"])
        self.assertEqual(len(entries(e,"g44_ward_intercepted")),1)
        e.check()

    def test_09_ward_does_not_spend_on_blocked_bite_or_same_grade(self):
        e,d,v,c=scene(target_role="B")
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v)
        whole_round(e)
        index,_=hit(e,d,die=1)
        r=v.apply_bite("hunter","victim",profile_hit_index=index,
                       exposure_key="no-puncture")
        self.assertEqual(r["outcome"],"not_delivered")
        self.assertTrue(v.effects[eid]["active"])
        # Independently present a Minor and then a different Minor;
        # catalog nonstacking precedes any Ward attempt.
        o=d.toxins.apply("victim","TX-MY",exposure_key="minor",
                          source="test:minor",route="injection",
                          delivery_verified=True,residual_piercing_hp=1,
                          resistance_die=1)
        self.assertEqual(o["outcome"],"prevented")
        self.assertFalse(v.effects[eid]["active"])
        e.check()

    def test_10_suppression_before_hunter_onset_zero_units_then_first(self):
        e,d,v,c=scene()
        bite(e,d,v)
        c.advance_exploration(599)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v,mode="suppression")
        self.assertEqual(v.effects[eid]["units"],3)
        self.assertFalse(v.effects[eid]["covered"])
        whole_round(e)
        c.advance_exploration(1)
        self.assertEqual(d.toxins.active("victim")["stage"],1)
        self.assertEqual(v.effects[eid]["units"],2)
        self.assertEqual(d.toxins.modifier("victim","mp"),0)
        c.advance_exploration(6)
        self.assertEqual(v.effects[eid]["units"],1)
        c.advance_exploration(12)
        self.assertFalse(v.effects[eid]["active"])
        self.assertEqual(d.toxins.modifier("victim","mp"),-2)
        e.check()

    def test_11_suppression_stage2_does_not_consume_extra_unit(self):
        e,d,v,c=scene()
        bite(e,d,v)
        c.advance_exploration(1799)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v,mode="suppression")
        self.assertEqual(v.effects[eid]["units"],2)
        whole_round(e)
        c.advance_exploration(1)
        self.assertEqual(d.toxins.active("victim")["stage"],2)
        # The real victim Step 3 in whole_round() already purchased the
        # second interval. Escalation itself buys no further unit.
        self.assertEqual(v.effects[eid]["units"],1)
        self.assertEqual(d.toxins.modifier("victim","mp"),0)
        c.advance_exploration(17)
        self.assertFalse(v.effects[eid]["active"])
        self.assertEqual(d.toxins.modifier("victim","mp"),-4)
        e.check()

    def test_12_fixed_ward_expires_at_one_minute_without_refund(self):
        e,d,v,c=scene()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        start=e.actors["caster"].vp_spent
        eid=cast(e,v)
        whole_round(e)
        c.advance_exploration(60)
        self.assertFalse(v.effects[eid]["active"])
        self.assertEqual(e.actors["caster"].vp_spent-start,2)
        e.check()

    def test_13_expiry_at_round_r_plus_10_prior_to_same_boundary(self):
        e,d,v,c=scene()
        c.enter_initiative()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v)
        self.assertEqual(c.events[v.effects[eid]["expiry"]].due_round,11)
        self.assertEqual(c.events[v.effects[eid]["expiry"]].phase,"before_toxin")
        whole_round(e)
        for _ in range(10):
            e.begin_round()
            whole_round(e)
        self.assertFalse(v.effects[eid]["active"])
        e.check()

    def test_14_suppression_blocks_nephro_packet_before_vigor_shield(self):
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-NP",exposure_key="kidney",
                       source="test:valid-ingestion",route="ingestion",
                       delivery_verified=True,resistance_die=1)
        c.advance_exploration(3570)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v,mode="suppression")
        whole_round(e)
        before=e.actors["victim"].vigor
        c.advance_exploration(30)
        self.assertEqual(e.actors["victim"].vigor,before)
        self.assertEqual(v.effects[eid]["units"],2)
        self.assertEqual(d.toxins.active("victim")["remaining"],3)
        e.check()

    def test_15_suppression_stops_three_future_hemotoxin_packets(self):
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-HM",exposure_key="hem",
                      source="test:verified-puncture",route="injection",
                      delivery_verified=True,residual_piercing_hp=1,
                      resistance_die=1,wound_location_rolls=(1,2,3,4,5))
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v,mode="suppression")
        whole_round(e)  # victim's genuine Step 3 consumes packet one
        c.advance_exploration(24)
        self.assertEqual(e.actors["victim"].hp,e.actors["victim"].hp_max-2)
        self.assertFalse(v.effects[eid]["active"])
        self.assertIsNone(d.toxins.active("victim"))
        self.assertEqual(len(entries(e,"g44_toxin_packet_prevented")),3)
        e.check()

    def test_16_fixed_spell_no_useful_toxin_still_spends_vp(self):
        e,d,v,c=scene()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        before=e.actors["caster"].vp_available
        eid=cast(e,v,mode="suppression")
        self.assertFalse(v.effects[eid]["active"])
        self.assertEqual(e.actors["caster"].vp_available,before-2)
        e.check()

    def test_17_contested_tie_resists_but_pays_valid_cast(self):
        e,d,v,c=scene()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v,unopposed=False,intrusion_totals=(15,15))
        self.assertIsNone(eid)
        self.assertEqual(e.actors["caster"].vp_spent,2)
        self.assertFalse(v.effects)
        e.check()

    def test_18_interrupted_cast_spends_ap_not_vp(self):
        e,d,v,c=scene()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        a=e.actors["caster"]
        before=(a.ap_remaining,a.vp_spent)
        # Post-commit recipient moves outside range.
        def move(enc):
            enc.actors["victim"].occupied=((12,1),)
        eid=cast(e,v,on_committed=move)
        self.assertIsNone(eid)
        self.assertEqual(a.ap_remaining,before[0]-30)
        self.assertEqual(a.vp_spent,before[1])
        e.check()

    def test_19_suppression_depleted_does_not_stop_original_stages(self):
        e,d,v,c=scene()
        bite(e,d,v)
        c.advance_exploration(900)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v,mode="suppression")
        whole_round(e)
        c.advance_exploration(18)
        self.assertFalse(v.effects[eid]["active"])
        self.assertEqual(d.toxins.modifier("victim","muscular_strength"),-1)
        self.assertEqual(d.toxins.active("victim")["stage"],1)
        e.check()

    def test_20_no_free_activation_or_foreign_source(self):
        e,d,v,c=scene()
        with self.assertRaises((ValueError,UnresolvedDecision)):
            v.cast_endurance("caster","victim",profile="Single Target",mode="ward",
                             source_authorized=False,source_reference="none")
        e.start_turn("caster",regen_choice=RegenerationChoice())
        with self.assertRaises((ValueError,UnresolvedDecision)):
            cast(e,v,price=1)
        self.assertEqual(e.actors["caster"].vp_spent,0)
        e.check()


    def test_21_rejected_hunter_key_is_reserved_across_all_toxin_paths(self):
        e,d,v,c=scene(target_role="B")
        index,damage=hit(e,d,die=1)
        self.assertFalse(damage["injection_eligible"])
        result=v.apply_bite("hunter","victim",profile_hit_index=index,
                            exposure_key="rejected-hunter")
        self.assertEqual(result["outcome"],"not_delivered")
        with self.assertRaisesRegex(ValueError,"Toxin exposure key already processed"):
            d.toxins.apply("victim","TX-MY",exposure_key="rejected-hunter",
                           source="test:independently_attested",
                           route="injection",delivery_verified=True,
                           residual_piercing_hp=1,resistance_die=1)
        self.assertIsNone(d.toxins.active("victim"))
        e.check()

    def test_22_missing_sourced_raw_vc_rejected_before_cast_resources(self):
        from dataclasses import replace
        e,d,v,c=scene()
        a=e.actors["caster"]
        a.source=replace(a.source,abilities=tuple((k,n) for k,n
                        in a.source.abilities if k!="Veil Control"))
        e.start_turn("caster",regen_choice=RegenerationChoice())
        before=(a.ap_remaining,a.vp_spent,len(v.effects))
        with self.assertRaisesRegex(UnresolvedDecision,"raw Veil Control"):
            cast(e,v,mode="suppression")
        self.assertEqual((a.ap_remaining,a.vp_spent,len(v.effects)),before)
        e.check()

    def test_23_hepato_suppression_preserves_genuine_recovery_and_vp(self):
        e,d,v,c=scene()
        target=e.actors["victim"]
        target.vigor-=10
        target.vp_spent=4
        target.vp_available-=4
        c.advance_exploration(21570)
        d.toxins.apply("victim","TX-HE",exposure_key="liver",
                        source="test:verified_ingestion",route="ingestion",
                        delivery_verified=True,resistance_die=1)
        original=c.events["recovery:victim:1"]
        self.assertFalse(original.consumed)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        effect=cast(e,v,mode="suppression")
        whole_round(e)
        c.advance_exploration(30)
        self.assertTrue(original.consumed)
        self.assertIsNone(d.toxins.active("victim"))
        self.assertFalse(v.effects[effect]["active"])
        recovered=entries(e,"g4_six_hour_recovery")
        actual=next(x for x in recovered if x["actor"]=="victim")
        self.assertEqual(actual["toxin_recovery_reduction"],0)
        self.assertEqual(actual["vigor"],max(1,(target.vigor_max+2)//4))
        self.assertGreater(actual["spent_vp_recovered"],0)
        self.assertEqual(len(entries(e,"g43_hepatotoxin_recovery")),1)
        e.check()

    def test_24_same_grade_ignored_before_ward_consumption(self):
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-MY",exposure_key="old-minor",
                        source="test:verified_injection",route="injection",
                        delivery_verified=True,residual_piercing_hp=1,
                        resistance_die=1)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v)
        whole_round(e)
        result=d.toxins.apply("victim","TX-DE",exposure_key="same-minor",
                              source="test:verified_contact",route="contact",
                              delivery_verified=True,resistance_die=None)
        self.assertEqual(result["outcome"],"ignored")
        self.assertTrue(v.effects[eid]["active"])
        self.assertEqual(d.toxins.active("victim")["key"],"old-minor")
        self.assertFalse(entries(e,"g44_ward_intercepted"))
        e.check()

    def test_25_continuous_neuro_protects_whole_local_intervals(self):
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-NE",exposure_key="nerve",
                        source="test:verified_injection",route="injection",
                        delivery_verified=True,residual_piercing_hp=1,
                        resistance_die=1)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v,mode="suppression")
        self.assertEqual(v.effects[eid]["units"],2)
        self.assertEqual(d.toxins.modifier("victim","dodge"),0)
        whole_round(e)
        # Actual Step 3 completed the initial toxin-local interval.
        self.assertEqual(v.effects[eid]["units"],1)
        c.advance_exploration(12)
        self.assertFalse(v.effects[eid]["active"])
        self.assertEqual(d.toxins.modifier("victim","dodge"),-2)
        self.assertIsNotNone(d.toxins.active("victim"))
        self.assertEqual(d.toxins.active("victim")["left"],2)
        e.check()

    def test_26_fixed_expiry_precedes_same_second_nephro_pulse(self):
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-NP",exposure_key="timed-nephro",
                        source="test:verified_ingestion",route="ingestion",
                        delivery_verified=True,resistance_die=1)
        c.advance_exploration(3540)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        eid=cast(e,v,mode="suppression")
        whole_round(e)
        vigor=e.actors["victim"].vigor
        c.advance_exploration(60)
        self.assertFalse(v.effects[eid]["active"])
        self.assertEqual(e.actors["victim"].vigor,vigor-1)
        self.assertEqual(len(entries(e,"g44_toxin_packet_prevented")),0)
        self.assertEqual(d.toxins.active("victim")["remaining"],3)
        e.check()


    def test_27_range_accepts_hunter_head_when_rear_sorts_lower(self):
        e,d,v,c=scene()
        hunter=e.actors["hunter"]
        self.assertEqual(hunter.footprint,("head","rear"))
        self.assertEqual(hunter.reference_cell_id,"head")
        # The rear is lexicographically closer to origin, but one square
        # FARTHER from the caster. The authored head is at exact range 3.
        hunter.occupied=((4,1),(3,1))
        e.actors["caster"].occupied=((7,1),)
        e.actors["victim"].occupied=((11,1),)
        self.assertEqual(hunter.reference_square(),(4,1))
        self.assertEqual(min(hunter.occupied),(3,1))
        e.start_turn("caster",regen_choice=RegenerationChoice())
        effect=cast(e,v,recipient="hunter")
        self.assertIsNotNone(effect)
        self.assertTrue(v.effects[effect]["active"])
        self.assertEqual(v.effects[effect]["recipient"],"hunter")
        e.check()

    def test_28_range_rejects_hunter_head_when_rear_would_be_in_range(self):
        e,d,v,c=scene()
        hunter=e.actors["hunter"]
        e.actors["victim"].occupied=((11,1),)
        # The rear at x=4 is in range 3, but the source reference head
        # at x=5 is 4 squares away and cannot be chosen by re-sorting.
        hunter.occupied=((5,1),(4,1))
        self.assertEqual(hunter.reference_square(),(5,1))
        self.assertEqual(min(hunter.occupied),(4,1))
        e.start_turn("caster",regen_choice=RegenerationChoice())
        a=e.actors["caster"]
        ap,spent,available=a.ap_remaining,a.vp_spent,a.vp_available
        with self.assertRaisesRegex(ValueError,
                                    "Invalid declaration-time Venom Endurance delivery"):
            cast(e,v,recipient="hunter")
        self.assertEqual((a.ap_remaining,a.vp_spent,a.vp_available),
                         (ap,spent,available))
        self.assertFalse(v.effects)
        e.check()

    def test_29_post_commit_pivot_rechecks_head_not_rear(self):
        e,d,v,c=scene()
        hunter=e.actors["hunter"]
        e.actors["victim"].occupied=((11,1),)
        hunter.occupied=((4,1),(5,1))
        self.assertEqual(hunter.reference_square(),(4,1))
        e.start_turn("caster",regen_choice=RegenerationChoice())
        a=e.actors["caster"]
        ap,spent,available=a.ap_remaining,a.vp_spent,a.vp_available
        def pivot(enc):
            # Source IDs do not change during a legal 180-degree pivot.
            enc.actors["hunter"].occupied=((5,1),(4,1))
        result=cast(e,v,recipient="hunter",on_committed=pivot)
        self.assertIsNone(result)
        self.assertEqual(hunter.reference_square(),(5,1))
        self.assertEqual(hunter.reference_cell_id,"head")
        self.assertEqual((a.ap_remaining,a.vp_spent,a.vp_available),
                         (ap-30,spent,available))
        self.assertFalse(v.effects)
        self.assertEqual(entries(e,"g44_endurance_interrupted")[-1]["vp_spent"],0)
        e.check()

    def test_30_legacy_fallback_cell_chosen_once_not_after_pivot(self):
        actor=party_actor("F",3,"legacy","party",occupied=((6,1),))
        # An explicitly modeled legacy two-cell actor with no stored
        # authored reference selects a deterministic original ID ONCE.
        actor.footprint=("front","tail")
        actor.occupied=((6,1),(5,1))
        actor.reference_cell_id=None
        actor.validate()
        self.assertEqual(actor.reference_cell_id,"tail")
        self.assertEqual(actor.reference_square(),(5,1))
        actor.occupied=((4,1),(5,1))
        self.assertEqual(actor.reference_square(),(5,1))
        actor.validate()
        self.assertEqual(actor.reference_cell_id,"tail")
        actor.reference_cell_id="unknown"
        with self.assertRaisesRegex(ValueError,"Reference cell"):
            actor.validate()

if __name__=="__main__":
    unittest.main()
