"""B04/B05 Low Scholar real G0/G1/G3/G4/G5 Embodiment regressions."""
from copy import deepcopy
from dataclasses import replace
import unittest

from scripts.b05_low_scholar_l1_l3_v0 import (
    profile,verify,KNOWN_L1,KNOWN_L2,PREPARED_L1,PREPARED_L2,
)
from scripts.b05_low_scholar_native_embodiment_v0 import LowScholarEmbodiment
from scripts.b05_low_scholar_native_encounter_v0 import (
    run_policy,run_matrix,attest_policy,
)
from scripts.b05_medium_priest_consecrations_v0 import MediumLifeConsecrations
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,party_actor,enemy_actor,UnresolvedDecision,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


STONE="LS-STONE-BODY-T1"
GUIDED="LS-GUIDED-REGEN-T1"


def scene(level=3):
    t=party_actor("T",level,"scholar","party",occupied=((2,2),))
    f=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    e=Encounter([t,f],{"scholar":40,"foe":30},
                seed=0,scenario="LowScholarNativeManualChecks")
    GridMovement(e,width=8,height=8)
    SpellState(e)
    DamageState(e)
    ls=LowScholarEmbodiment(e,"scholar")
    e.begin_round()
    e.start_turn("scholar",regen_choice=RegenerationChoice())
    return e,ls


def next_scholar_turn(e,choice=None):
    e.end_turn()
    e.start_turn("foe",regen_choice=RegenerationChoice())
    e.end_turn()
    e.begin_round()
    e.start_turn("scholar",regen_choice=choice or RegenerationChoice())


class LowScholarNativeTests(unittest.TestCase):
    def test_01_source_sheet_all_three_levels(self):
        self.assertTrue(verify()["structural_low_scholar_source_verified"])
        self.assertEqual(KNOWN_L1,(
            "Stone Skin","Guided Regeneration","Conjure Flame"))
        self.assertEqual(KNOWN_L2,"Basic Heal")
        self.assertEqual(PREPARED_L1,("Stone Skin","Guided Regeneration"))
        self.assertEqual(PREPARED_L2,PREPARED_L1+("Conjure Flame",))
        for level in (1,2,3):
            with self.subTest(level=level):
                p=profile(level)
                a=party_actor("T",level,"scholar","party",occupied=((2,2),))
                self.assertEqual((p["hp_max"],p["vigor_max"],p["vp_max"]),
                                 (12,12*level,2*level))
                self.assertEqual((a.ap_total,a.physical_ap,a.projection_ap),
                                 (30+6*(level-1),20,30))
                self.assertEqual(a.focus,"Low")
                self.assertEqual(a.source.source_id,"T")
                self.assertEqual(a.source.attack_profiles,
                                 ("B05-PC-T-SWORD-CUT",))
                self.assertTrue(p["native_physical_attack_verified"])
                self.assertEqual((a.regen,a.guard_value,a.guard_capacity),
                                 (5,17,1 if level<3 else 2))
                self.assertEqual(p["movement_points"],12)
                self.assertEqual(p["silver_remaining_sp"],83)
                self.assertEqual(p["stone_committed_vp"],1 if level==1 else 2)
                self.assertEqual(p["guided_committed_vp"],2)
                self.assertEqual(len(p["known_pillar_techniques"]),
                                 3 if level==1 else 4)
                self.assertEqual(len(p["prepared_techniques"]),
                                 2 if level==1 else 3)
                self.assertTrue(set(p["prepared_techniques"]).issubset(
                    p["known_pillar_techniques"]))
                self.assertNotIn("Basic Heal",p["prepared_techniques"])
                self.assertFalse(p["native_weapon_embodiment_authored"])

    def test_02_low_l1_stone_cost_original_resistance(self):
        e,ls=scene(1)
        a=e.actors["scholar"]
        effect=ls.activate(STONE)
        self.assertEqual(effect.resistance,2)
        self.assertEqual((effect.committed,e.g3.resistance("scholar","Physical")),(1,2))
        self.assertEqual((a.ap_remaining,a.vp_available,a.vp_committed,a.vp_spent),
                         (0,1,1,0))
        self.assertEqual(e.g3.resistance("scholar","Fire"),2)
        self.assertEqual(e.g3.resistance("scholar","Poison"),0)
        self.assertEqual(e.g3.regen_throughput("scholar"),0)
        self.assertEqual(e.g3.resistance("foe","Physical"),0)
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="action_committed" and
                              v["detail"]["actor"]=="scholar" and
                              v["detail"]["ap_spent"]==30]),1)
        e.check()

    def test_03_low_l1_guided_uses_all_vp_no_instant_step(self):
        e,ls=scene(1)
        a=e.actors["scholar"]
        steps_before=len([v for v in e.ledger
            if v["kind"]=="regeneration_step" and v["detail"]["actor"]=="scholar"])
        ls.activate(GUIDED)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(0,2,0))
        self.assertEqual(a.ap_remaining,0)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertEqual(a.hp,a.hp_max)
        self.assertEqual(len([v for v in e.ledger
            if v["kind"]=="regeneration_step" and v["detail"]["actor"]=="scholar"]),
            steps_before)
        with self.assertRaises(ValueError):
            ls.intensify()

    def test_04_low_release_then_new_projection_not_free_switch(self):
        e,ls=scene(2)
        a=e.actors["scholar"]
        ls.activate(STONE)
        self.assertEqual(a.ap_remaining,6)
        with self.assertRaises(ValueError):
            ls.activate(GUIDED)
        before=(a.vp_available,a.vp_committed,a.vp_spent,ls.effect_id)
        with self.assertRaises(AttributeError):
            ls.reroute(GUIDED)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent,ls.effect_id),
                         before)
        ls.release()
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(4,0,0))
        with self.assertRaises(ValueError):
            ls.activate(GUIDED)  # 6 AP cannot buy 30 AP
        self.assertIsNone(ls.effect_id)
        next_scholar_turn(e)
        ls.activate(GUIDED)
        self.assertEqual((a.ap_remaining,a.vp_available,a.vp_committed,a.vp_spent),
                         (6,2,2,0))
        self.assertEqual(e.g3.resistance("scholar","Physical"),0)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)

    def test_05_l3_stone_intensify_and_next_own_turn_expiry(self):
        e,ls=scene(3)
        a=e.actors["scholar"]
        effect=ls.activate(STONE)
        ls.intensify()
        self.assertEqual(effect.resistance,3)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,2,1))
        with self.assertRaises(ValueError):
            ls.intensify()
        with self.assertRaises(ValueError):
            ls.activate(GUIDED)
        next_scholar_turn(e)
        self.assertIs(e.g3.effects[("scholar",effect.ident)],effect)
        self.assertEqual(effect.resistance,2)
        self.assertFalse(ls.intensified)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,2,1))
        self.assertEqual(len([v for v in e.ledger
            if v["kind"]=="b05_low_scholar_stone_intensity_expired"]),1)

    def test_06_l3_guided_intensity_only_at_real_step(self):
        e,ls=scene(3)
        a=e.actors["scholar"]
        effect=ls.activate(GUIDED)
        ls.intensify()
        self.assertTrue(ls.intensified)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertEqual(a.hp,a.hp_max)
        self.assertFalse(any(v["kind"]=="b05_low_scholar_guided_intensity_consumed"
                             for v in e.ledger))
        with self.assertRaises(ValueError):
            ls.intensify()
        next_scholar_turn(e)
        self.assertFalse(ls.intensified)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertEqual(len([v for v in e.ledger
            if v["kind"]=="b05_low_scholar_guided_intensity_consumed"]),1)
        self.assertEqual(a.vp_spent,1)
        self.assertEqual(effect.committed,2)
        receipt=[v for v in e.ledger if v["kind"]=="regeneration_step"
                 and v["detail"]["actor"]=="scholar"][-1]
        consumed=[v for v in e.ledger if
                  v["kind"]=="b05_low_scholar_guided_intensity_consumed"][-1]
        self.assertEqual(consumed["detail"]["step2_index"],receipt["index"])

    def test_07_source_native_soldier_cases_and_real_effect_delta(self):
        examples={p:run_policy(level=2,policy=p) for p in
                  ("baseline","stone","guided","switch")}
        for policy,r in examples.items():
            with self.subTest(policy=policy):
                self.assertEqual(r["source_ids"]["scholar"],"T")
                self.assertEqual(r["source_ids"]["foe"],"B06-EN-02")
                self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))
                self.assertEqual(r["metrics"]["actual_self_steps"],3)
                self.assertEqual(r["metrics"]["confirmed_attacks"],3)
                self.assertEqual(r["metrics"]["damage_receipts"],3)
                self.assertEqual(r["metrics"]["last_mp"],0)
        self.assertGreater(examples["stone"]["metrics"]["hp"],
                           examples["baseline"]["metrics"]["hp"])
        self.assertGreater(examples["guided"]["metrics"]["hp_restored"],
                           examples["baseline"]["metrics"]["hp_restored"])
        self.assertEqual(examples["switch"]["metrics"]["activations"],2)
        self.assertEqual(examples["switch"]["metrics"]["releases"],1)
        self.assertEqual(examples["switch"]["metrics"]["paid_projection_ap"],60)

    def test_08_native_l3_intensification_damage_step_and_expiry(self):
        baseline=run_policy(level=3,policy="stone")
        boosted=run_policy(level=3,policy="stone_intensify")
        self.assertEqual(boosted["metrics"]["stone_intensity_expirations"],1)
        self.assertEqual(boosted["metrics"]["intensifications"],1)
        self.assertEqual(boosted["metrics"]["vp"],(3,2,1))
        self.assertGreaterEqual(boosted["metrics"]["hp"],baseline["metrics"]["hp"])
        g=run_policy(level=3,policy="guided_intensify")
        self.assertEqual(g["metrics"]["guided_intensity_consumptions"],1)
        self.assertEqual(g["metrics"]["intensifications"],1)
        self.assertEqual(g["metrics"]["vp"],(3,2,1))
        self.assertFalse(g["metrics"]["intensified"])
        self.assertEqual(g["metrics"]["actual_self_steps"],3)
        self.assertEqual(g["metrics"]["last_mp"],0)

    def test_09_reject_no_out_of_turn_or_invalid_focus(self):
        e,ls=scene(3)
        before=len(e.ledger)
        for bad in ("MS-STONE-BODY-T1","LS-UNKNOWN","Stone Skin"):
            with self.assertRaises(UnresolvedDecision):
                ls.activate(bad)
        self.assertEqual(len(e.ledger),before)
        ls.activate(STONE)
        e.end_turn()
        prior=e.actors["scholar"].vp_spent
        with self.assertRaises(ValueError):
            ls.intensify()
        with self.assertRaises(ValueError):
            ls.release()
        self.assertEqual(e.actors["scholar"].vp_spent,prior)

    def test_10_real_medium_priest_guided_blocks_duplicate_low_activation(self):
        priest=party_actor("M",1,"priest","party",occupied=((1,2),))
        scholar=party_actor("T",1,"scholar","party",occupied=((2,2),))
        e=Encounter([priest,scholar],{"priest":40,"scholar":30},seed=7)
        GridMovement(e,width=7,height=7)
        SpellState(e)
        DamageState(e)
        consecration=MediumLifeConsecrations(e)
        ls=LowScholarEmbodiment(e,"scholar")
        e.begin_round()
        e.start_turn("priest",regen_choice=RegenerationChoice())
        hosted=consecration.cast("priest","Guided Regeneration","scholar")
        e.end_turn()
        e.start_turn("scholar",regen_choice=RegenerationChoice())
        a=e.actors["scholar"]
        before=(a.ap_remaining,a.vp_available,a.vp_committed,
                a.vp_spent,len(e.ledger),tuple(e.g3.effects))
        with self.assertRaises(ValueError):
            ls.activate(GUIDED)
        self.assertEqual((a.ap_remaining,a.vp_available,a.vp_committed,
                          a.vp_spent,len(e.ledger),tuple(e.g3.effects)),before)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertIs(e.g3.effects[("priest",hosted.ident)],hosted)
        ls.activate(STONE)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        e.check()

    def test_11_unprepared_and_non_t_source_rejected(self):
        e,ls=scene(2)
        with self.assertRaises(UnresolvedDecision):
            ls.activate("Conjure Flame")
        with self.assertRaises(UnresolvedDecision):
            ls.activate("Basic Heal")
        source=e.actors["scholar"].source
        before=(e.actors["scholar"].ap_remaining,
                e.actors["scholar"].vp_available,len(e.ledger))
        for fake in (replace(source,digest="0"*64),
                     replace(source,source_id="M"),
                     replace(source,equipment=(("Leather armor","carried"),))):
            e.actors["scholar"].source=fake
            with self.assertRaises(UnresolvedDecision):
                ls.activate(STONE)
            self.assertEqual(before,(
                e.actors["scholar"].ap_remaining,
                e.actors["scholar"].vp_available,len(e.ledger)))
        e.actors["scholar"].source=source
        e.check()

    def test_12_ending_stone_on_unconsciousness_refunds_vp(self):
        e,ls=scene(2)
        a=e.actors["scholar"]
        effect=ls.activate(STONE)
        a.hp=0
        e.g3.sync_consciousness("scholar")
        self.assertIsNone(ls.effect_id)
        self.assertNotIn(("scholar",effect.ident),e.g3.effects)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(4,0,0))
        self.assertEqual(e.g3.resistance("scholar","Physical"),0)
        e.check()

    def test_13_ending_guided_before_step_discards_pending_without_refund(self):
        e,ls=scene(3)
        a=e.actors["scholar"]
        ls.activate(GUIDED)
        ls.intensify()
        ls.release()
        self.assertIsNone(ls.effect_id)
        self.assertFalse(ls.intensified)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(5,0,1))
        self.assertEqual(e.g3.regen_throughput("scholar"),0)
        next_scholar_turn(e)
        self.assertFalse(any(v["kind"]=="b05_low_scholar_guided_intensity_consumed"
                             for v in e.ledger))

    def test_14_g0_step_hooks_cannot_be_forged_outside_step(self):
        e,ls=scene(3)
        ls.activate(GUIDED)
        ls.intensify()
        before=(e.actors["scholar"].vp_spent,ls.intensified,len(e.ledger))
        with self.assertRaises(UnresolvedDecision):
            ls.on_step_start("scholar")
        with self.assertRaises(AssertionError):
            ls.on_step_complete("scholar")
        self.assertEqual((e.actors["scholar"].vp_spent,ls.intensified,len(e.ledger)),
                         before)

    def test_15_matrix_count_and_limits(self):
        r=run_matrix()
        self.assertEqual(r["case_count"],14)
        self.assertEqual(len({(x["level"],x["policy"]) for x in r["cases"]}),14)
        self.assertEqual(r["audit_sha256"],canonical_digest({
            k:v for k,v in r.items() if k!="audit_sha256"}))
        self.assertFalse(r["full_focus_certified"])
        self.assertFalse(r["numerical_tuning_authorized"])

    def test_16_report_tampering_rejected_even_after_digest_rewrite(self):
        p={"level":2,"policy":"switch","seed":0}
        r=run_policy(**p)
        self.assertEqual(attest_policy(r,**p),r)
        forged=deepcopy(r)
        forged["metrics"]["paid_projection_ap"]=0
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(forged,**p)
        forged=deepcopy(r)
        forged["ledger"][0]["kind"]="replaced"
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(forged,**p)

    def test_17_invalid_early_intensify_and_unknown_scene_policy(self):
        for lv in (1,2):
            e,ls=scene(lv)
            ls.activate(STONE)
            with self.assertRaises(ValueError):
                ls.intensify()
        for lv,policy in ((1,"stone_intensify"),(2,"guided_intensify"),
                          (4,"stone"),(True,"stone"),(3,"fake")):
            with self.assertRaises(ValueError):
                run_policy(level=lv,policy=policy)

    def test_18_other_recipient_guided_still_allows_own_embodiment(self):
        priest=party_actor("M",1,"priest","party",occupied=((1,2),))
        scholar=party_actor("T",1,"scholar","party",occupied=((2,2),))
        e=Encounter([priest,scholar],{"priest":40,"scholar":30},seed=8)
        GridMovement(e,width=7,height=7)
        SpellState(e)
        DamageState(e)
        c=MediumLifeConsecrations(e)
        ls=LowScholarEmbodiment(e,"scholar")
        e.begin_round()
        e.start_turn("priest",regen_choice=RegenerationChoice())
        c.cast("priest","Guided Regeneration","priest")
        e.end_turn()
        e.start_turn("scholar",regen_choice=RegenerationChoice())
        own=ls.activate(GUIDED)
        self.assertEqual(own.recipient,"scholar")
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertEqual(e.g3.regen_throughput("priest"),1)
        self.assertEqual(len([x for x in e.g3.effects.values()
            if x.kind=="Guided Regeneration"]),2)
        e.check()


    def test_19_native_dying_death_mid_step_preserves_receipt_and_ends_turn(self):
        # The low-Scholar host is terminated by native G4 while Step2 is
        # already in progress. G0 still must authenticate that exact Step.
        for level in (1, 2, 3):
            with self.subTest(level=level):
                e,ls=scene(level)
                a=e.actors["scholar"]
                host=ls.activate(GUIDED)
                if level==3:
                    ls.intensify()
                before_spent=a.vp_spent
                e.end_turn()
                e.start_turn("foe",regen_choice=RegenerationChoice())
                e.end_turn()

                # Source-valid fixture immediately before the native Dying
                # loss: -11 of 12 HP and no Vigor to cancel it.
                a.hp=-11
                a.vigor=0
                e.check()
                e.begin_round()
                first=len(e.ledger)
                e.start_turn("scholar",regen_choice=RegenerationChoice())

                self.assertTrue(a.dead)
                self.assertEqual(a.hp,-12)
                self.assertEqual(a.vigor,0)
                self.assertIsNone(e.pending_regeneration)
                self.assertEqual(e.current,"scholar")
                self.assertIn("scholar",e.regen_done)
                self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),
                                 (2*level-before_spent,0,before_spent))
                self.assertEqual(a.ap_remaining,0)
                self.assertIsNone(ls.effect_id)
                self.assertFalse(ls.intensified)
                self.assertFalse(ls._step_live)
                self.assertIsNone(ls._step_open_at)
                self.assertNotIn(("scholar",host.ident),e.g3.effects)

                progressed=e.ledger[first:]
                ended=[v for v in progressed if
                       v["kind"]=="g3_effect_ended" and
                       v["detail"]["effect"]==host.ident]
                step=[v for v in progressed if
                      v["kind"]=="regeneration_step" and
                      v["detail"]["actor"]=="scholar"]
                self.assertEqual(len(ended),1)
                self.assertEqual(len(step),1)
                self.assertLess(ended[0]["index"],step[0]["index"])
                self.assertEqual((step[0]["detail"]["hp_before"],
                                  step[0]["detail"]["hp_after"]),(-11,-12))
                self.assertTrue(step[0]["detail"]["dead"])
                self.assertFalse(any(v["kind"]==
                    "b05_low_scholar_guided_intensity_consumed"
                    for v in progressed))
                self.assertFalse(any(v["kind"]=="regeneration_dead"
                                     for v in progressed))
                e.check()
                # Re-entering Step2 or replaying the same source turn is
                # illegal; a genuine end_turn must nevertheless succeed.
                with self.assertRaises(ValueError):
                    e.start_turn("scholar",regen_choice=RegenerationChoice())
                e.end_turn()
                e.start_turn("foe",regen_choice=RegenerationChoice())
                e.end_turn()
                e.check()

    def test_20_nonfatal_dying_step_consumes_guided_without_fake_hp(self):
        # A living but unconscious caster can maintain Guided. The native
        # Step still consumes one Intensification even with zero Vigor,
        # but must not invent HP recovery or terminate the live host.
        e,ls=scene(3)
        a=e.actors["scholar"]
        host=ls.activate(GUIDED)
        ls.intensify()
        e.end_turn()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        e.end_turn()
        a.hp=0
        a.vigor=0
        e.check()
        e.begin_round()
        first=len(e.ledger)
        e.start_turn("scholar",regen_choice=RegenerationChoice())
        self.assertEqual((a.hp,a.vigor),(-1,0))
        self.assertFalse(a.dead)
        self.assertIsNone(e.pending_regeneration)
        self.assertEqual(ls.effect_id,host.ident)
        self.assertFalse(ls.intensified)
        self.assertFalse(ls._step_live)
        self.assertIsNone(ls._step_open_at)
        self.assertIs(e.g3.effects[("scholar",host.ident)],host)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,2,1))
        trace=e.ledger[first:]
        steps=[v for v in trace if v["kind"]=="regeneration_step"
               and v["detail"]["actor"]=="scholar"]
        consumed=[v for v in trace if
                  v["kind"]=="b05_low_scholar_guided_intensity_consumed"]
        self.assertEqual((len(steps),len(consumed)),(1,1))
        self.assertEqual(steps[0]["detail"]["hp_restored"],0)
        self.assertEqual(consumed[0]["detail"]["step2_index"],steps[0]["index"])
        self.assertFalse(any(v["kind"]=="g3_effect_ended" for v in trace))
        e.check()
        e.end_turn()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        e.end_turn()
        e.check()


if __name__=="__main__":
    unittest.main()
