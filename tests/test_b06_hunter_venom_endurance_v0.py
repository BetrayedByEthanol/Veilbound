"""G4.4 Hunter timing and Venom Endurance bounded executable regression."""
import unittest
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, party_actor, enemy_actor, UnresolvedDecision)
from scripts.b06_damage_v0 import DamageState, DamagePacket
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


    def test_31_stale_bite_after_exploration_cannot_reanchor_or_use_late_ward(self):
        e,d,v,c=scene()
        hit_index,physical=hit(e,d)
        self.assertGreater(physical["hp_loss"],0)
        victim_hp=e.actors["victim"].hp
        # The first Bite is already five minutes old. A Ward cast NOW
        # cannot retroactively prevent exposure at its original impact.
        c.advance_exploration(300)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        ward=cast(e,v)
        whole_round(e)
        pending_before=set(c.events)
        with self.assertRaisesRegex(
                UnresolvedDecision,"latest Bite event synchronously"):
            v.apply_bite("hunter","victim",
                         profile_hit_index=hit_index,
                         exposure_key="retroactive",resistance_die=1)
        self.assertEqual(e.actors["victim"].hp,victim_hp)
        self.assertEqual(set(c.events),pending_before)
        self.assertIsNone(d.toxins.active("victim"))
        self.assertTrue(v.effects[ward]["active"])
        self.assertFalse(entries(e,"g44_hunter_accepted"))
        self.assertFalse(entries(e,"g44_ward_intercepted"))
        self.assertNotIn("retroactive",d.toxins.exposure_ids)
        # A NEW verified physical Bite may still consume that valid Ward.
        fresh,_=hit(e,d)
        prevented=v.apply_bite("hunter","victim",
                    profile_hit_index=fresh,
                    exposure_key="new-bite",resistance_die=None)
        self.assertEqual(prevented["outcome"],"prevented")
        self.assertFalse(v.effects[ward]["active"])
        self.assertIsNone(d.toxins.active("victim"))
        e.check()

    def test_32_stale_bite_after_round_boundary_rejected(self):
        e,d,v,c=scene()
        hit_index,_=hit(e,d)
        whole_round(e)
        e.begin_round()
        with self.assertRaisesRegex(
                UnresolvedDecision,"latest Bite event synchronously"):
            v.apply_bite("hunter","victim",
                         profile_hit_index=hit_index,
                         exposure_key="next-round",resistance_die=1)
        self.assertFalse(entries(e,"g44_hunter_accepted"))
        self.assertNotIn("next-round",d.toxins.exposure_ids)
        self.assertIsNone(d.toxins.active("victim"))
        self.assertEqual(len([x for x in c.events
                              if x.startswith("hunter:")]),0)
        e.check()

    def test_33_unrelated_same_instant_ledger_event_ends_bite_window(self):
        e,d,v,c=scene()
        hit_index,_=hit(e,d)
        e.log("fixture_independent_action",description="no time elapsed")
        with self.assertRaisesRegex(
                UnresolvedDecision,"latest Bite event synchronously"):
            v.apply_bite("hunter","victim",
                         profile_hit_index=hit_index,
                         exposure_key="intervening",resistance_die=1)
        self.assertNotIn(hit_index,v.hit_keys)
        self.assertIsNone(d.toxins.active("victim"))
        e.check()

    def test_34_unrelated_lethal_g4_damage_ends_ward_immediately(self):
        e,d,v,c=scene()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        initial_spent=e.actors["caster"].vp_spent
        ward=cast(e,v)
        expiry=v.effects[ward]["expiry"]
        self.assertTrue(v.effects[ward]["active"])
        victim=e.actors["victim"]
        # A physical Crush packet uses the source's normal weapon Armor
        # rule. Include that actual Armor in the independently rolled raw
        # fixture so the confirmed post-mitigation HP damage is lethal.
        d.apply_damage("victim",
             (DamagePacket("hp","Crush",victim.hp_max*2+d._armor(victim),
                           armor_rule="weapon"),),
             event_key="fixture:lethal_other_source",
             cause="independently_confirmed_unrelated_attack")
        self.assertTrue(victim.dead)
        self.assertFalse(v.effects[ward]["active"])
        self.assertTrue(c.events[expiry].canceled)
        ended=[x for x in entries(e,"g44_endurance_ended")
               if x["effect"]==ward]
        self.assertEqual(len(ended),1)
        self.assertEqual(ended[0]["reason"],"recipient_dead")
        self.assertEqual(e.actors["caster"].vp_spent,initial_spent+2)
        damage_idx=next(x["index"] for x in e.ledger
                        if x["kind"]=="g4_damage_applied"
                        and x["detail"]["event_key"]=="fixture:lethal_other_source")
        end_idx=next(x["index"] for x in e.ledger
                     if x["kind"]=="g44_endurance_ended"
                     and x["detail"]["effect"]==ward)
        self.assertLess(damage_idx,end_idx)
        # Death releases the per-caster slot before any toxin query or
        # scheduled expiry. The same caster may protect a living new target.
        whole_round(e)
        e.begin_round()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        new_ward=cast(e,v,recipient="caster")
        self.assertIsNotNone(new_ward)
        self.assertTrue(v.effects[new_ward]["active"])
        self.assertNotEqual(new_ward,ward)
        e.check()

    def test_35_natural_dying_step_death_ends_suppression_immediately(self):
        e,d,v,c=scene()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        d.toxins.apply("victim","TX-NE",
             exposure_key="already-exposed",source="fixture:verified_injection",
             route="injection",delivery_verified=True,
             residual_piercing_hp=1,resistance_die=1)
        suppression=cast(e,v,mode="suppression")
        self.assertTrue(v.effects[suppression]["active"])
        victim=e.actors["victim"]
        damage=victim.hp_max*2-1
        d.apply_damage("victim",
             (DamagePacket("hp","Crush",damage+d._armor(victim),
                           armor_rule="weapon"),),
             event_key="fixture:near_lethal",
             cause="independently_confirmed_dying_attack",
             wound_location_roll=10)
        self.assertEqual(victim.hp,-victim.hp_max+1)
        self.assertFalse(victim.dead)
        self.assertTrue(v.effects[suppression]["active"])
        e.end_turn()
        e.start_turn("victim",regen_choice=RegenerationChoice())
        self.assertTrue(victim.dead)
        self.assertFalse(v.effects[suppression]["active"])
        self.assertEqual(
            [x["reason"] for x in entries(e,"g44_endurance_ended")
             if x["effect"]==suppression],["recipient_dead"])
        self.assertTrue(c.events[v.effects[suppression]["expiry"]].canceled)
        self.assertEqual(v.for_recipient("victim"),None)
        e.check()


    def test_36_tx_en_step3_carries_five_exploration_seconds(self):
        # At Step 3 the first protected interval ends, but that Step is
        # not an extra six elapsed world seconds. Its existing 5s remainder
        # must follow the next paid interval through mode conversion.
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-EN",exposure_key="en-phase",
                       source="test:verified_ingestion",route="ingestion",
                       delivery_verified=True,resistance_die=1)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        effect=cast(e,v,mode="suppression")
        whole_round(e)  # buys next interval, phase 0 and one unit remains
        self.assertEqual((v.effects[effect]["units"],
                          v.effects[effect]["phase"]),(1,0))
        c.advance_exploration(5)
        self.assertEqual(v.effects[effect]["phase"],5)
        c.enter_initiative()
        e.begin_round()
        whole_round(e)  # genuine recipient Step 3 buys last unit
        self.assertEqual((v.effects[effect]["units"],
                          v.effects[effect]["phase"],
                          v.effects[effect]["covered"]),(0,5,True))
        self.assertEqual(d.toxins.modifier("victim","physical_exertion"),0)
        c.leave_initiative()
        self.assertTrue(v.effects[effect]["active"])
        c.advance_exploration(1)
        self.assertFalse(v.effects[effect]["active"])
        self.assertEqual(d.toxins.modifier("victim","physical_exertion"),-1)
        self.assertIsNotNone(d.toxins.active("victim"))
        self.assertEqual(len([x for x in entries(e,"g44_suppression_unit")
                              if x["effect"]==effect]),3)
        e.check()

    def test_37_hunter_step3_preserves_shorter_fractional_remainders(self):
        # Both small and large partial intervals must finish at precisely
        # (6-phase) actual exploration seconds after a real Step 3.
        for partial in (1,5):
            with self.subTest(partial=partial):
                e,d,v,c=scene()
                result,_=bite(e,d,v,key="hunter-phase")
                self.assertEqual(result["resolution"],"Full")
                c.advance_exploration(600)
                self.assertEqual(d.toxins.active("victim")["stage"],1)
                e.start_turn("caster",regen_choice=RegenerationChoice())
                effect=cast(e,v,mode="suppression")
                whole_round(e)
                self.assertEqual(v.effects[effect]["units"],1)
                c.advance_exploration(partial)
                self.assertEqual(v.effects[effect]["phase"],partial)
                c.enter_initiative()
                e.begin_round()
                whole_round(e)
                self.assertEqual((v.effects[effect]["phase"],
                                  v.effects[effect]["units"]),
                                 (partial,0))
                self.assertTrue(v.effects[effect]["covered"])
                c.leave_initiative()
                self.assertEqual(d.toxins.modifier("victim","mp"),0)
                c.advance_exploration(5-partial)
                self.assertTrue(v.effects[effect]["active"])
                self.assertEqual(v.effects[effect]["phase"],5)
                c.advance_exploration(1)
                self.assertFalse(v.effects[effect]["active"])
                self.assertEqual(d.toxins.modifier("victim","mp"),-2)
                self.assertEqual(d.toxins.active("victim")["stage"],1)
                self.assertEqual(len([x for x in entries(e,"g44_suppression_unit")
                                      if x["effect"]==effect]),3)
                e.check()

    def test_38_exploration_long_boundary_still_resets_phase(self):
        # The fractional carry rule applies to Step 3 only. A real complete
        # six-second exploration interval starts the next at phase zero.
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-EN",exposure_key="en-full-interval",
                       source="test:verified_ingestion",route="ingestion",
                       delivery_verified=True,resistance_die=1)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        effect=cast(e,v,mode="suppression")
        whole_round(e)
        self.assertEqual(v.effects[effect]["units"],1)
        c.advance_exploration(6)
        self.assertEqual((v.effects[effect]["units"],
                          v.effects[effect]["phase"],
                          v.effects[effect]["covered"]),(0,0,True))
        c.advance_exploration(5)
        self.assertTrue(v.effects[effect]["active"])
        c.advance_exploration(1)
        self.assertFalse(v.effects[effect]["active"])
        self.assertEqual(d.toxins.modifier("victim","physical_exertion"),-1)
        e.check()


    def test_39_coalesced_q0_endurance_expiry_precedes_earlier_nephro_pulse(self):
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-NP",exposure_key="pulse-at-3600",
                       source="test:verified_ingestion",route="ingestion",
                       delivery_verified=True,resistance_die=1)
        c.advance_exploration(3543)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        effect=cast(e,v,mode="suppression")
        whole_round(e)
        pulse=d.toxins.active("victim")["marker"]
        expiry=v.effects[effect]["expiry"]
        self.assertEqual(c.events[pulse].due_seconds,3600)
        self.assertEqual(c.events[expiry].due_seconds,3603)
        self.assertLess(c.events[pulse].original_order,
                        c.events[expiry].original_order)
        c.advance_exploration(55)
        vigor_before=e.actors["victim"].vigor
        self.assertEqual(c.world_seconds,3598)
        c.enter_initiative()  # both q0 at same next Round Begin
        self.assertTrue(c.events[expiry].consumed)
        self.assertTrue(c.events[pulse].consumed)
        self.assertFalse(v.effects[effect]["active"])
        self.assertEqual(e.actors["victim"].vigor,vigor_before-1)
        self.assertEqual(v.effects[effect]["units"],3)
        self.assertFalse(entries(e,"g44_toxin_packet_prevented"))
        due=[x["event_id"] for x in entries(e,"g42_milestone_due")
             if x["event_id"] in (pulse,expiry)]
        self.assertEqual(due,[expiry,pulse])
        self.assertEqual(len(entries(e,"g44_suppression_unit")),0)
        e.check()

    def test_40_coalesced_future_round_endurance_expiry_precedes_pulse(self):
        e,d,v,c=scene()
        d.toxins.apply("victim","TX-NP",exposure_key="pulse-q1",
                       source="test:verified_ingestion",route="ingestion",
                       delivery_verified=True,resistance_die=1)
        c.advance_exploration(3543)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        effect=cast(e,v,mode="suppression")
        whole_round(e)
        pulse=d.toxins.active("victim")["marker"]
        expiry=v.effects[effect]["expiry"]
        c.advance_exploration(49)   # T=3592; remaining 8 and 11 -> q=1
        c.enter_initiative()
        self.assertFalse(c.events[pulse].consumed)
        self.assertFalse(c.events[expiry].consumed)
        self.assertEqual(c.events[pulse].due_round,c.events[expiry].due_round)
        e.begin_round()
        whole_round(e)
        vigor_before=e.actors["victim"].vigor
        e.begin_round()  # both events due at Round Begin
        self.assertEqual(e.actors["victim"].vigor,vigor_before-1)
        self.assertFalse(v.effects[effect]["active"])
        self.assertFalse(entries(e,"g44_toxin_packet_prevented"))
        self.assertEqual([x["event_id"] for x in entries(e,"g42_milestone_due")
                          if x["event_id"] in (pulse,expiry)], [expiry,pulse])
        e.check()

    def test_41_legacy_hemotoxin_suppression_exact_budget_and_native_ticks(self):
        e,d,v,c=scene()
        d.schedule_hemotoxin("victim",exposure_key="legacy-full",
                             actual_exposure=True,resistance_total=9,
                             wound_location_roll=10)
        legacy=d.short_toxins[0]
        self.assertEqual(legacy["left"],5)
        self.assertIsNone(d.toxins.active("victim"))
        e.start_turn("caster",regen_choice=RegenerationChoice())
        effect=cast(e,v,mode="suppression")
        self.assertTrue(v.effects[effect]["active"])
        self.assertTrue(v.effects[effect]["bound_legacy"])
        self.assertEqual(v.effects[effect]["bound_key"],"legacy-full")
        self.assertEqual(v.effects[effect]["units"],3)
        self.assertEqual(len(d.short_toxins),1)
        whole_round(e)
        self.assertEqual((legacy["applied"],legacy["left"],
                          v.effects[effect]["units"]),(1,4,2))
        c.advance_exploration(12)
        self.assertEqual((legacy["applied"],legacy["left"],
                          v.effects[effect]["units"]),(3,2,0))
        self.assertFalse(v.effects[effect]["active"])
        self.assertEqual(e.actors["victim"].hp,e.actors["victim"].hp_max)
        c.advance_exploration(12)
        self.assertEqual((legacy["applied"],legacy["left"]),(5,0))
        self.assertEqual(e.actors["victim"].hp,e.actors["victim"].hp_max-2)
        prevented=[x for x in entries(e,"g44_toxin_packet_prevented")
                   if x["key"]=="legacy-full"]
        self.assertEqual([x["packet"] for x in prevented],[1,2,3])
        self.assertTrue(all(x["legacy"] for x in prevented))
        self.assertEqual(len(entries(e,"g4_toxin_tick")),5)
        self.assertIsNone(d.toxins.active("victim"))
        self.assertEqual(len(d.short_toxins),1)
        e.check()

    def test_42_legacy_reduced_toxin_expires_with_unused_suppression(self):
        from dataclasses import replace
        e,d,v,c=scene()
        a=e.actors["caster"]
        a.source=replace(a.source,abilities=tuple(
            (k,4 if k=="Veil Control" else n) for k,n in a.source.abilities))
        d.schedule_hemotoxin("victim",exposure_key="legacy-reduced",
                             actual_exposure=True,resistance_total=12,
                             wound_location_roll=10)
        legacy=d.short_toxins[0]
        e.start_turn("caster",regen_choice=RegenerationChoice())
        effect=cast(e,v,mode="suppression")
        self.assertEqual(v.effects[effect]["units"],5)
        whole_round(e)
        c.advance_exploration(12)
        self.assertEqual((legacy["left"],legacy["applied"]),(0,3))
        self.assertFalse(v.effects[effect]["active"])
        self.assertEqual(v.effects[effect]["units"],2)
        self.assertEqual(
            [x["reason"] for x in entries(e,"g44_endurance_ended")
             if x["effect"]==effect],["bound_toxin_ended"])
        self.assertEqual(e.actors["victim"].hp,e.actors["victim"].hp_max)
        self.assertTrue(c.events[v.effects[effect]["expiry"]].canceled)
        self.assertEqual(len(entries(e,"g44_toxin_packet_prevented")),3)
        e.check()

if __name__=="__main__":
    unittest.main()
