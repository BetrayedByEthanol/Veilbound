"""B04/B05 Medium Scholar real G0/G1/G3/G4 and Soldier G5 verification."""
from copy import deepcopy
from dataclasses import replace
import unittest

from scripts.b05_medium_scholar_l1_l3_v0 import (
    profile,verify,KNOWN_L1,KNOWN_L2,PROFILE_IDS,
)
from scripts.b05_medium_scholar_native_inward_v0 import MediumScholarInward
from scripts.b05_medium_priest_consecrations_v0 import MediumLifeConsecrations
from scripts.b05_medium_scholar_native_encounter_v0 import (
    run_policy,attest_policy,run_matrix,
)
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, party_actor, enemy_actor, UnresolvedDecision,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def scene(level=3):
    s=party_actor("S",level,"scholar","party",occupied=((2,2),))
    f=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    e=Encounter([s,f],{"scholar":40,"foe":30},seed=0,
                scenario="MediumScholarManualNativeChecks")
    GridMovement(e,width=8,height=8,scene_id="scholar-manual-map")
    SpellState(e)
    DamageState(e)
    adapter=MediumScholarInward(e,"scholar")
    e.begin_round()
    e.start_turn("scholar",regen_choice=RegenerationChoice())
    return e,adapter


def events(r,kind):
    return [x for x in r["ledger"] if x["kind"]==kind]


def priest_guided_scene(*, level=2, recipient="scholar"):
    """Pay a real M Consecration before S's actual native G0 turn."""
    priest=party_actor("M",level,"priest","party",occupied=((1,2),))
    scholar=party_actor("S",level,"scholar","party",occupied=((2,2),))
    e=Encounter([priest,scholar],{"priest":40,"scholar":30},seed=0,
                scenario="B05-Medium-Scholar-recipient-exclusivity",
                policy="real_preexisting_medium_priest_consecration")
    GridMovement(e,width=7,height=7,scene_id="priest-scholar-guided")
    SpellState(e)
    DamageState(e)
    consecrations=MediumLifeConsecrations(e)
    inward=MediumScholarInward(e,"scholar")
    e.begin_round()
    e.start_turn("priest",regen_choice=RegenerationChoice())
    priest_host=consecrations.cast("priest","Guided Regeneration",recipient)
    if priest_host is None:
        raise AssertionError("Expected a legally paid native Priest effect")
    e.end_turn()
    e.start_turn("scholar",regen_choice=RegenerationChoice())
    return e,consecrations,inward,priest_host


class MediumScholarNativeTests(unittest.TestCase):
    def test_01_build_all_levels_and_native_source_immutability(self):
        self.assertTrue(verify()["structural_build_source_verified"])
        prev=None
        for lv in (1,2,3):
            p=profile(lv)
            a=party_actor("S",lv,"scholar","party",occupied=((2,2),))
            self.assertEqual(a.source.source_id,"S")
            self.assertEqual(a.source.status,"STRUCTURAL_B05_ONLY")
            self.assertEqual(dict(a.source.abilities),p["abilities"])
            self.assertEqual(a.source.attack_profiles,
                             ("B05-PC-S-SWORD-CUT",))
            self.assertTrue(p["native_physical_attack_verified"])
            self.assertEqual((a.hp_max,a.vigor_max,a.vp_max),
                             (12,12*lv,4*lv))
            self.assertEqual((a.ap_total,a.physical_ap,a.projection_ap),
                             (30+6*(lv-1),24,24))
            self.assertEqual(a.guard_value,17)
            self.assertEqual(p["silver_remaining_sp"],83)
            self.assertEqual(sum(p["equipment_sp"].values()),67)
            self.assertEqual(len(p["known_pillar_techniques"]),4 if lv==1 else 5)
            self.assertEqual(p["normal_regen_throughput"],3)
            self.assertEqual(p["movement_points"],12)
            self.assertEqual(p["initiative"],4 if lv<3 else 6)
            self.assertEqual(p["talents"],(
                ("TAL-U01 Veil Insight",) if lv<3 else
                ("TAL-U01 Veil Insight","TAL-C01 Combat Awareness")))
            self.assertEqual(p["weapon_development_points"],2)
            self.assertEqual(p["abilities"]["Veil Affinity"],0)
            self.assertTrue(set(PROFILE_IDS).issubset(p["known_inward_profiles"]))
            if prev:
                self.assertTrue(set(prev["known_pillar_techniques"]).issubset(
                    set(p["known_pillar_techniques"])))
            prev=p
        self.assertEqual(KNOWN_L1[0],"Stone Skin")
        self.assertEqual(KNOWN_L2,"Minor Telekinesis")

    def test_02_g0_ap_vp_and_live_stone_only(self):
        e,ms=scene(1)
        effect=ms.activate("MS-STONE-BODY-T1")
        s=e.actors["scholar"]
        self.assertEqual(effect.kind,"Stone Skin")
        self.assertEqual(effect.resistance,1)
        self.assertEqual((s.ap_remaining,s.vp_available,s.vp_committed,s.vp_spent),
                         (6,3,1,0))
        self.assertEqual(e.g3.resistance("scholar","Physical"),1)
        self.assertEqual(e.g3.resistance("scholar","Fire"),1)
        self.assertEqual(e.g3.resistance("scholar","Poison"),0)
        self.assertEqual(e.g3.resistance("foe","Fire"),0)
        self.assertEqual(e.g3.regen_throughput("scholar"),0)
        self.assertEqual(s.mp_remaining,12)
        self.assertEqual(len(e.g3.active("scholar","Stone Skin")),1)
        self.assertTrue(any(x["kind"]=="action_committed" and
            x["detail"]["ap_spent"]==24 for x in e.ledger))
        e.check()

    def test_03_g0_guided_requires_real_own_step_not_instant_hp(self):
        e,ms=scene(1)
        s=e.actors["scholar"]
        ms.activate("MS-GUIDED-REGEN-T1")
        self.assertEqual(s.hp,s.hp_max)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertEqual(len([x for x in e.ledger
                             if x["kind"]=="regeneration_step" and
                             x["detail"]["actor"]=="scholar"]),1)
        self.assertEqual(s.vp_committed,1)

    def test_04_real_soldier_damage_resistance_and_step_delta(self):
        cases={x:run_policy(level=1,policy=x) for x in
               ("baseline","stone","guided","reroute")}
        for name,r in cases.items():
            self.assertEqual(r["metrics"]["attack_hits"],3)
            self.assertEqual(r["metrics"]["damage_receipts"],3)
            self.assertEqual(r["metrics"]["regeneration_steps"],3)
            self.assertEqual(r["source_ids"]["scholar"],"S")
            self.assertEqual(r["source_ids"]["foe"],"B06-EN-02")
            self.assertEqual(r["ledger_sha256"],canonical_digest(r["ledger"]))
        self.assertGreater(cases["stone"]["metrics"]["scholar_hp"],
                           cases["baseline"]["metrics"]["scholar_hp"])
        self.assertGreater(cases["guided"]["metrics"]["native_hp_restored"],
                           cases["baseline"]["metrics"]["native_hp_restored"])
        self.assertEqual(cases["reroute"]["metrics"]["vp"],(0,1,3))
        self.assertEqual(cases["reroute"]["metrics"]["reroutes"],1)
        self.assertEqual(cases["reroute"]["metrics"]["active_effect"],
                         "MS-GUIDED-REGEN-T1")

    def test_05_paid_reroute_atomic_and_zero_action(self):
        e,ms=scene(2)
        ms.activate("MS-STONE-BODY-T1")
        a=e.actors["scholar"]
        ap=a.ap_remaining
        ms.reroute("MS-GUIDED-REGEN-T1")
        self.assertEqual(a.ap_remaining,ap)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(4,1,3))
        self.assertEqual(ms._current_ident(),"MS-GUIDED-REGEN-T1")
        self.assertEqual(e.g3.resistance("scholar","Physical"),0)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        before=(a.vp_available,a.vp_committed,a.vp_spent,a.mp_remaining)
        with self.assertRaises(ValueError):
            ms.reroute("MS-GUIDED-REGEN-T1")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent,a.mp_remaining),before)

    def test_06_l1_second_reroute_insufficient_does_not_release_host(self):
        e,ms=scene(1)
        ms.activate("MS-STONE-BODY-T1")
        ms.reroute("MS-GUIDED-REGEN-T1")
        a=e.actors["scholar"]
        prior=(ms.effect_id,list(a.maintained),
               a.vp_available,a.vp_committed,a.vp_spent)
        with self.assertRaises(ValueError):
            ms.reroute("MS-STONE-BODY-T1")
        self.assertEqual((ms.effect_id,list(a.maintained),
                          a.vp_available,a.vp_committed,a.vp_spent),prior)
        e.check()

    def test_07_overroute_mp_12_10_8_and_g1_real_steps(self):
        e,ms=scene(3)
        ms.activate("MS-STONE-BODY-T1")
        a=e.actors["scholar"]
        self.assertEqual(a.mp_remaining,12)
        ms.overroute(1)
        self.assertEqual((a.mp_remaining,ms.steps),(10,1))
        self.assertEqual(e.g3.resistance("scholar","Physical"),2)
        ms.overroute(2)
        self.assertEqual((a.mp_remaining,ms.steps),(8,2))
        self.assertEqual(e.g3.resistance("scholar","Fire"),3)
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(9,1,2))
        for step in ((-1,0),(0,-1),(-1,0),(0,-1)):
            self.assertTrue(e.g1.step("scholar",step))
        self.assertEqual(a.mp_remaining,0)
        with self.assertRaises(ValueError):
            e.g1.step("scholar",(1,0))
        ms.overroute(0)
        self.assertEqual(a.mp_remaining,4)  # release only withheld MP, not moved MP
        self.assertEqual(e.g3.resistance("scholar","Fire"),1)
        self.assertEqual(a.vp_spent,2)
        e.check()

    def test_08_no_backdated_mp_for_late_overroute(self):
        e,ms=scene(3)
        ms.activate("MS-STONE-BODY-T1")
        for step in ((-1,0),(-1,0),(0,-1),(0,-1),(1,0)):
            self.assertTrue(e.g1.step("scholar",step))
        a=e.actors["scholar"]
        self.assertEqual(a.mp_remaining,2)
        before=(a.mp_remaining,a.vp_available,a.vp_committed,a.vp_spent,
                ms.steps,ms.effect_id)
        with self.assertRaises(ValueError):
            ms.overroute(2)
        self.assertEqual((a.mp_remaining,a.vp_available,a.vp_committed,
                          a.vp_spent,ms.steps,ms.effect_id),before)
        self.assertEqual(e.g3.resistance("scholar","Physical"),1)

    def test_09_next_turn_native_mp_reapplies_sustained_penalty(self):
        e,ms=scene(3)
        ms.activate("MS-STONE-BODY-T1")
        ms.overroute(2)
        self.assertEqual(e.actors["scholar"].mp_remaining,8)
        e.end_turn()
        e.start_turn("foe",regen_choice=RegenerationChoice())
        e.end_turn()
        e.begin_round()
        e.start_turn("scholar",regen_choice=RegenerationChoice())
        self.assertEqual(e.actors["scholar"].mp_remaining,8)
        self.assertEqual(ms.steps,2)
        self.assertEqual(len([v for v in e.ledger
                              if v["kind"]=="b05_medium_scholar_turn_mp"]),2)

    def test_10_legal_l3_overroute_into_guided_real_step(self):
        result=run_policy(level=3,policy="overroute_guided")
        self.assertEqual(result["metrics"]["overroutes"],1)
        self.assertEqual(result["metrics"]["active_steps"],2)
        self.assertEqual(result["metrics"]["vp"],(9,1,2))
        # G0 end-turn cleanup correctly discards unused MP: assert the
        # native MP *during* each turn, never claim 8 MP survived cleanup.
        self.assertEqual(result["metrics"]["last_mp"],0)
        turns=[x["detail"]["mp"] for x in events(result,"turn_resources")
               if x["detail"]["actor"]=="scholar"]
        self.assertEqual(turns,[12,8,8])
        applied=[x["detail"]["mp_remaining"] for x in
                 events(result,"b05_medium_scholar_mp_reconciled")]
        self.assertIn(8,applied)
        guided=run_policy(level=3,policy="guided")
        self.assertGreater(result["metrics"]["native_hp_restored"],
                           guided["metrics"]["native_hp_restored"])

    def test_11_reactive_cast_and_low_profiles_not_authorized(self):
        e,ms=scene(1)
        prior=len(e.ledger)
        for bad in ("LS-STONE-BODY-T1","MS-UNKNOWN","Stone Skin"):
            with self.assertRaises((ValueError,UnresolvedDecision)):
                ms.activate(bad)
        self.assertEqual(len(e.ledger),prior)
        ms.activate("MS-STONE-BODY-T1")
        with self.assertRaises(ValueError):
            ms.activate("MS-GUIDED-REGEN-T1")
        e.check()

    def test_12_no_out_of_turn_free_reroute_or_overroute(self):
        e,ms=scene(3)
        ms.activate("MS-STONE-BODY-T1")
        e.end_turn()
        before=(ms.effect_id, e.actors["scholar"].vp_available,
                e.actors["scholar"].vp_spent)
        with self.assertRaises(ValueError):
            ms.reroute("MS-GUIDED-REGEN-T1")
        with self.assertRaises(ValueError):
            ms.overroute(2)
        self.assertEqual((ms.effect_id,e.actors["scholar"].vp_available,
                          e.actors["scholar"].vp_spent),before)

    def test_13_release_refunds_committed_only_and_clears_host(self):
        e,ms=scene(3)
        ms.activate("MS-STONE-BODY-T1")
        ms.overroute(2)
        ms.release()
        a=e.actors["scholar"]
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(10,0,2))
        self.assertIsNone(ms.effect_id)
        self.assertEqual(e.g3.resistance("scholar","Physical"),0)
        self.assertEqual(a.mp_remaining,12)
        self.assertFalse(e.g3.active("scholar","Stone Skin"))
        e.check()

    def test_14_medium_priest_cannot_inherit_scholar_inward(self):
        a=party_actor("M",1,"priest","party",occupied=((2,2),))
        e=Encounter([a],{"priest":30},seed=0)
        GridMovement(e,width=6,height=6)
        SpellState(e)
        DamageState(e)
        with self.assertRaises(UnresolvedDecision):
            MediumScholarInward(e,"priest")
        self.assertIsNone(e.g3.medium_scholar)

    def test_15_report_replay_rejects_rehashed_forgery(self):
        args={"level":2,"policy":"reroute","seed":0}
        r=run_policy(**args)
        self.assertEqual(attest_policy(r,**args),r)
        bad=deepcopy(r)
        bad["metrics"]["paid_projection_ap"]+=24
        bad["ledger_sha256"]=canonical_digest(bad["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(bad,**args)
        bad=deepcopy(r)
        bad["ledger"][0]["kind"]="forged"
        bad["ledger_sha256"]=canonical_digest(bad["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(bad,**args)

    def test_16_matrix_count_and_limit_flags(self):
        m=run_matrix()
        self.assertEqual(m["case_count"],14)
        self.assertEqual(m["audit_sha256"],canonical_digest(
            {k:v for k,v in m.items() if k!="audit_sha256"}))
        self.assertFalse(m["full_focus_certified"])
        self.assertFalse(m["numerical_tuning_authorized"])
        self.assertEqual({x["level"] for x in m["cases"]},{1,2,3})
        self.assertEqual(len({(x["level"],x["policy"]) for x in m["cases"]}),14)

    def test_17_invalid_policy_or_level_never_starts_source_scene(self):
        for lv,policy in ((1,"overroute_body"),(2,"overroute_guided"),
                          (3,"unknown"),(True,"stone"),(4,"guided")):
            with self.assertRaises(ValueError):
                run_policy(level=lv,policy=policy)
        with self.assertRaises(ValueError):
            profile(False)

    def test_18_no_double_inward_and_no_fake_external_beneficiary(self):
        e,ms=scene(2)
        ms.activate("MS-GUIDED-REGEN-T1")
        self.assertEqual(e.g3.regen_throughput("foe"),0)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertEqual(len(e.g3.active("scholar","Guided Regeneration")),1)
        with self.assertRaises(ValueError):
            ms.activate("MS-STONE-BODY-T1")
        self.assertFalse(e.g3.active("foe","Guided Regeneration"))
        e.check()
        source=e.actors["scholar"].source
        before=(e.actors["scholar"].vp_available,
                e.actors["scholar"].vp_committed,
                e.actors["scholar"].vp_spent)
        for forged in (
            replace(source,digest="0"*64),
            replace(source,equipment=tuple(
                (name,"carried" if name=="Leather armor" else state)
                for name,state in source.equipment)),
        ):
            e.actors["scholar"].source=forged
            with self.assertRaises(UnresolvedDecision):
                ms.reroute("MS-STONE-BODY-T1")
            self.assertEqual(before,(
                e.actors["scholar"].vp_available,
                e.actors["scholar"].vp_committed,
                e.actors["scholar"].vp_spent))
        e.actors["scholar"].source=source
        e.check()


    def test_19_priest_guided_on_scholar_blocks_activation_before_payment(self):
        e,priest,ms,priest_host=priest_guided_scene(level=1)
        actor=e.actors["scholar"]
        self.assertEqual(priest_host.recipient,"scholar")
        self.assertEqual(priest_host.caster,"priest")
        # This is the precise regression: active(caster,kind) is empty,
        # although the recipient already has the same native blessing.
        self.assertEqual(e.g3.active("scholar","Guided Regeneration"),[])
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        before=(actor.ap_remaining,actor.vp_available,actor.vp_committed,
                actor.vp_spent,actor.mp_remaining,len(e.ledger),
                tuple(e.g3.effects))
        with self.assertRaises(ValueError):
            ms.activate("MS-GUIDED-REGEN-T1")
        self.assertEqual(before,(
            actor.ap_remaining,actor.vp_available,actor.vp_committed,
            actor.vp_spent,actor.mp_remaining,len(e.ledger),
            tuple(e.g3.effects)))
        self.assertIsNone(ms.effect_id)
        self.assertEqual(e.g3.effects[("priest",priest_host.ident)],priest_host)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        # Unrelated Stone Inward remains a valid paid option.
        stone=ms.activate("MS-STONE-BODY-T1")
        self.assertEqual(stone.kind,"Stone Skin")
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        e.check()

    def test_20_priest_guided_blocks_reroute_without_releasing_stone(self):
        e,priest,ms,priest_host=priest_guided_scene(level=2)
        scholar=e.actors["scholar"]
        stone=ms.activate("MS-STONE-BODY-T1")
        self.assertEqual(e.g3.resistance("scholar","Physical"),1)
        before=(ms.effect_id,ms.steps,
                scholar.ap_remaining,scholar.vp_available,
                scholar.vp_committed,scholar.vp_spent,scholar.mp_remaining,
                len(e.ledger),tuple(e.g3.effects))
        with self.assertRaises(ValueError):
            ms.reroute("MS-GUIDED-REGEN-T1")
        self.assertEqual(before,(
            ms.effect_id,ms.steps,
            scholar.ap_remaining,scholar.vp_available,
            scholar.vp_committed,scholar.vp_spent,scholar.mp_remaining,
            len(e.ledger),tuple(e.g3.effects)))
        self.assertIs(e.g3.effects[("scholar",stone.ident)],stone)
        self.assertIs(e.g3.effects[("priest",priest_host.ident)],priest_host)
        self.assertEqual(e.g3.resistance("scholar","Physical"),1)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        e.check()

        # Once the original Priest legitimately releases the benefit,
        # the exact same Scholar reroute is legal on the next own turn.
        e.end_turn()
        e.begin_round()
        e.start_turn("priest",regen_choice=RegenerationChoice())
        e.g3.release("priest","Guided Regeneration")
        e.end_turn()
        e.start_turn("scholar",regen_choice=RegenerationChoice())
        guided=ms.reroute("MS-GUIDED-REGEN-T1")
        self.assertEqual(guided.recipient,"scholar")
        self.assertEqual(guided.caster,"scholar")
        self.assertEqual((scholar.vp_available,scholar.vp_committed,
                          scholar.vp_spent),(4,1,3))
        self.assertEqual(e.g3.resistance("scholar","Physical"),0)
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertEqual(len([x for x in e.g3.effects.values()
                              if x.kind=="Guided Regeneration" and
                              x.recipient=="scholar"]),1)
        e.check()

    def test_21_same_named_effect_on_other_recipient_is_legal(self):
        e,priest,ms,priest_host=priest_guided_scene(
            level=1,recipient="priest")
        self.assertEqual(priest_host.recipient,"priest")
        scholar=e.actors["scholar"]
        guided=ms.activate("MS-GUIDED-REGEN-T1")
        self.assertIsNotNone(guided)
        self.assertEqual(guided.recipient,"scholar")
        self.assertEqual((scholar.ap_remaining,scholar.vp_available,
                          scholar.vp_committed,scholar.vp_spent),(6,3,1,0))
        self.assertEqual(e.g3.regen_throughput("scholar"),1)
        self.assertEqual(e.g3.regen_throughput("priest"),1)
        self.assertEqual(len([x for x in e.g3.effects.values()
                              if x.kind=="Guided Regeneration"]),2)
        e.check()


if __name__=="__main__":
    unittest.main()
