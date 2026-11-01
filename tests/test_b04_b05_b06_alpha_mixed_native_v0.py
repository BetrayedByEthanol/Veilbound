"""Alpha L1 mixed-party native Soldier source/actions/host/terminal regressions."""
from copy import deepcopy
import unittest

from scripts.b04_b05_b06_alpha_mixed_native_v0 import (
    run,attest,scene,PARTY,FOCUSES,EXIT_SQUARES,
)
from scripts.b05_low_life_native_rites_v0 import (
    LowLifeNativeRites,full_low_priest_actor,FULL_SOURCE,FULL_STATUS,
)
from scripts.b05_medium_anointed_native_returning_step_v0 import MediumAnointedRestoration
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


class AlphaNativeMixedL1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=run(variant="A")
        cls.b=run(variant="B")

    def test_01_both_full_selected_priest_variants_with_exact_sources(self):
        for variant,r in (("A",self.a),("B",self.b)):
            with self.subTest(variant=variant):
                self.assertEqual(r["level"],1)
                self.assertEqual(r["source_paths"]["priest"],FULL_SOURCE)
                self.assertTrue(r["actual_full_low_priest_source"])
                self.assertEqual(r["opponent_level"],3)
                self.assertEqual(r["opponent_source"],"B06-EN-02")
                self.assertEqual(set(r["party_focuses"]),set(PARTY))
                self.assertEqual(r["party_focuses"],FOCUSES)
                self.assertEqual(r["native_party_exits"],4)
                self.assertEqual(r["terminal"],"party_scene_withdrawal")
                self.assertEqual(r["rounds"],2)
                self.assertEqual(
                    {n:tuple(r["final_state"][n]["occupied"][0])
                     for n in PARTY},EXIT_SQUARES)

    def test_02_paid_four_focus_action_windows_and_original_enemy_hit(self):
        for r in (self.a,self.b):
            def events(k):
                return [x for x in r["ledger"] if x["kind"]==k]
            self.assertEqual(len(events("b05_low_rite_established")),1)
            self.assertEqual(len(events("b05_medium_anointed_investment_established")),1)
            self.assertEqual(len(events("g4_anointed_medium_returning_step_applied")),1)
            self.assertEqual(len(events("b05_gifted_emotion_established")),1)
            self.assertEqual(len(events("g3_flame_launched")),2)
            self.assertEqual(len(events("g5_melee_resolved")),2)
            self.assertEqual(len(events("g5_terminal_exit")),4)
            self.assertEqual(
                {e["detail"]["actor"]:e["detail"]["ap_spent"]
                 for e in events("action_committed")
                 if e["detail"]["actor"] in PARTY},
                {"anointed":24,"priest":30,"gifted":20,"scholar":20})
            self.assertEqual(events("b05_low_rite_established")[0]["detail"]["chosen"],True)
            self.assertEqual(events("b05_medium_anointed_investment_established")[0]["detail"]["vessel"],"priest")
            pulse=events("g4_anointed_medium_returning_step_applied")[0]
            self.assertEqual(pulse["detail"]["recipient"],"priest")
            self.assertEqual(pulse["detail"]["activation_ap"],0)
            self.assertEqual(pulse["detail"]["hp_restored"],1)
            self.assertGreater(pulse["detail"]["recipient_vigor_spent"],0)

    def test_03_source_lanes_maintained_host_and_VP_conservation(self):
        for r in (self.a,self.b):
            self.assertEqual(r["final_state"]["foe"]["dead"],False)
            for n in PARTY:
                actor=r["final_vp_totals"][n]
                self.assertEqual(actor["available"]+
                                 actor["committed"]+actor["spent"],
                                 actor["max"])
            casts=[x for x in r["ledger"] if x["kind"]=="g3_flame_launched"]
            self.assertEqual({x["detail"]["caster"] for x in casts},
                             {"gifted","scholar"})
            self.assertTrue(all(x["detail"]["outcome"]=="automatic_miss"
                                for x in casts))
            self.assertFalse(r["human_sessions"])
            self.assertFalse(r["independent_full_focus_certificates"])
            self.assertFalse(r["strict_mvp_exits_met"])

    def test_04_source_bound_replay_rejects_forged_policies(self):
        for variant,r in (("A",self.a),("B",self.b)):
            self.assertEqual(attest(r,variant=variant)["ledger_sha256"],
                             r["ledger_sha256"])
        forged=deepcopy(self.a)
        forged["terminal"]="soldier_defeat"
        with self.assertRaises(AssertionError):
            attest(forged)
        forged=deepcopy(self.a)
        forged["ledger"][0]["kind"]="fake_creation"
        forged["ledger_sha256"]=canonical_digest(forged["ledger"])
        with self.assertRaises(AssertionError):
            attest(forged)

    def test_05_no_proxy_or_skipped_full_source_identity(self):
        combat,low,joy,invest=scene(variant="A")
        self.assertEqual(combat.e.actors["priest"].source.status,FULL_STATUS)
        self.assertEqual(combat.e.actors["priest"].source.attack_profiles,())
        self.assertEqual(low.chosen_name,"Guided Regeneration")
        with self.assertRaises(ValueError):
            scene(variant="ghost")
        with self.assertRaises(ValueError):
            scene(seed=-1)
        self.assertNotEqual(self.a["source_digests"]["priest"],
                            self.a["source_digests"]["gifted"])

    def test_06_old_proxy_remains_source_separated_but_retains_native_rite(self):
        proxy=party_actor("A",1,"priest","party",occupied=((1,1),))
        full=full_low_priest_actor("A",1,"priest","party",occupied=((1,1),))
        self.assertNotEqual(full.source,proxy.source)
        self.assertNotEqual(full.source.status,proxy.source.status)
        for actor in (proxy,full):
            e=Encounter([actor],{"priest":30},seed=0)
            GridMovement(e,width=6,height=6)
            RangedCombat(e)
            SpellState(e)
            DamageState(e)
            adapter=LowLifeNativeRites(e,"priest")
            e.begin_round()
            e.start_turn("priest",regen_choice=RegenerationChoice())
            self.assertIsNotNone(adapter.cast_chosen("priest"))
            e.end_turn()
            e.check()

    def test_07_forged_full_actor_cannot_be_accepted_as_legacy_proxy(self):
        priest=full_low_priest_actor("A",1,"priest","party",occupied=((1,1),))
        e=Encounter([priest],{"priest":30},seed=0)
        GridMovement(e,width=6,height=6)
        RangedCombat(e)
        SpellState(e)
        DamageState(e)
        priest.guard_capacity+=1
        with self.assertRaises(UnresolvedDecision):
            LowLifeNativeRites(e,"priest")

    def test_08_no_unsupported_new_A_or_B_melee_authority(self):
        combat,_,_,_=scene(variant="A")
        e=combat.e
        self.assertEqual(e.actors["priest"].source.attack_profiles,())
        e.start_turn("anointed",regen_choice=RegenerationChoice())
        # An attempted free full-Priest melee declaration is NOT allowed to
        # fall back onto a legacy Hunter physical A/B proxy identity.
        with self.assertRaises((UnresolvedDecision,ValueError)):
            combat.declare("priest","foe",profiles=("B06-PC-A-SWORD",),
                           defenses=("take_hit",))


if __name__=="__main__":
    unittest.main()
