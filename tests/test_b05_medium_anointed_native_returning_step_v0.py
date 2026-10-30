"""Authentic G0-paid Medium Investment and G4-before-natural-regen Step pulse."""
from pathlib import Path
from hashlib import sha256
import unittest

from scripts.b05_medium_anointed_native_returning_step_v0 import (
    MediumAnointedRestoration,
)
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState

ROOT=Path(__file__).resolve().parents[1]


def scene(level=1,*,medium_at=(1,1),patient_at=(3,1),
          walls=(),hp=7,vigor=7,third_at=None):
    m=party_actor("AM",level,"medium","party",occupied=(medium_at,))
    patient=party_actor("AH",level,"patient","party",occupied=(patient_at,))
    patient.hp=hp
    patient.vigor=vigor
    actors=[m,patient]
    scores={"medium":30,"patient":20}
    if third_at is not None:
        third=party_actor("AL",level,"other","party",occupied=(third_at,))
        actors.append(third)
        scores["other"]=10
    e=Encounter(actors,scores,seed=0,scenario="B04-B05-Medium-Anointed-native",
                objective="one_real_G0_invested_patient_step_not_victory")
    GridMovement(e,width=8,height=7,walls=walls,scene_id="B05-medium-native")
    SpellState(e)
    DamageState(e)
    med=MediumAnointedRestoration(e,"medium")
    e.begin_round()
    e.start_turn("medium",regen_choice=RegenerationChoice())
    return e,med


def events(e,kind):
    return [v for v in e.ledger if v["kind"]==kind]


def to_patient_step(e,med,*,lesser=False,choice=RegenerationChoice(),
                    visible=True,unopposed=True,blocked_restoration=()):
    med.invest("patient",consenting=True)
    e.end_turn()
    med.declare_pulse("patient",lesser=lesser,visible=visible,
                      unopposed=unopposed,blocked_restoration=blocked_restoration)
    e.start_turn("patient",regen_choice=choice)


class MediumAnointedNativeTests(unittest.TestCase):
    def test_01_nine_real_levels_paid_invest_and_one_native_pulse(self):
        for lv in (1,2,3):
            with self.subTest(level=lv):
                e,med=scene(lv,hp=7,vigor=7)
                to_patient_step(e,med,choice=RegenerationChoice(hp=1))
                p=e.actors["patient"]
                self.assertEqual((9,5),(p.hp,p.vigor))
                self.assertEqual(1,len(events(e,"g4_anointed_medium_returning_step_applied")))
                patient_steps=[x for x in events(e,"regeneration_step")
                               if x["detail"]["actor"]=="patient"]
                self.assertEqual(1,len(patient_steps))
                pulse=events(e,"g4_anointed_medium_returning_step_applied")[0]
                step=patient_steps[0]
                self.assertLess(pulse["index"],step["index"])
                self.assertEqual((1,1,0,0),(pulse["detail"]["hp_restored"],
                                 pulse["detail"]["recipient_vigor_spent"],
                                 pulse["detail"]["activation_ap"],
                                 pulse["detail"]["vp_spent"]))
                self.assertEqual((1,1),(step["detail"]["hp_restored"],
                                       step["detail"]["throughput_spent"]))
                i=pulse["detail"]["investment_action_index"]
                self.assertEqual(("action_committed","general",24),
                    (e.ledger[i]["kind"],e.ledger[i]["detail"]["action_class"],
                     e.ledger[i]["detail"]["ap_spent"]))
                self.assertEqual(sha256((ROOT/e.actors["medium"].source.path).read_bytes()).hexdigest(),
                                 pulse["detail"]["source_digest"])
                self.assertEqual(2,med.state.destiny)
                self.assertIsNone(med.pending)
                self.assertEqual(("B05-PC-AM-DAGGER-PIERCE",),e.actors["medium"].source.attack_profiles)
                e.check()

    def test_02_lesser_one_destiny_at_zero_vigor_and_no_double_step(self):
        e,med=scene(3,hp=6,vigor=0)
        to_patient_step(e,med,lesser=True)
        self.assertEqual((7,0),(e.actors["patient"].hp,e.actors["patient"].vigor))
        self.assertEqual(1,med.state.destiny)
        steps=[x for x in events(e,"regeneration_step")
               if x["detail"]["actor"]=="patient"]
        self.assertEqual(1,len(steps))
        self.assertEqual(0,steps[0]["detail"]["throughput_spent"])
        self.assertEqual(1,len(events(e,"g4_anointed_medium_returning_step_applied")))
        self.assertIsNone(med.pending)
        with self.assertRaises(ValueError):
            med.declare_pulse("patient",lesser=True,visible=True,unopposed=True)
        with self.assertRaises(ValueError):
            e.g4.regenerate(e.actors["patient"],RegenerationChoice())
        self.assertEqual(1,med.state.destiny)

    def test_03_invalid_natural_allocation_preserves_pulse_and_destiny(self):
        e,med=scene(2,hp=11,vigor=3)
        med.invest("patient",consenting=True)
        e.end_turn()
        med.declare_pulse("patient",lesser=True,visible=True,unopposed=True)
        old=(e.actors["patient"].hp,e.actors["patient"].vigor,med.state.destiny)
        with self.assertRaises(ValueError):
            e.start_turn("patient",regen_choice=RegenerationChoice(hp=1))
        self.assertEqual(old,(e.actors["patient"].hp,
                              e.actors["patient"].vigor,med.state.destiny))
        self.assertFalse(events(e,"g4_anointed_medium_returning_step_applied"))
        self.assertNotIn("patient",e.regen_done)
        self.assertIsNotNone(med.pending)
        e.start_turn("patient",regen_choice=RegenerationChoice())
        self.assertEqual((12,3,1),(e.actors["patient"].hp,
                                   e.actors["patient"].vigor,med.state.destiny))
        self.assertEqual(1,len(events(e,"g4_anointed_medium_returning_step_applied")))

    def test_04_invest_requires_real_general_action_consent_and_living_patient(self):
        for case in ("refused","dying","missing","insufficient_ap"):
            with self.subTest(case=case):
                e,med=scene()
                if case=="dying":
                    e.actors["patient"].hp=0
                if case=="insufficient_ap":
                    e.actors["medium"].ap_remaining=23
                before=len(events(e,"action_committed"))
                with self.assertRaises((ValueError,UnresolvedDecision)):
                    med.invest("missing" if case=="missing" else "patient",
                               consenting=(case!="refused"))
                self.assertEqual(before,len(events(e,"action_committed")))
                self.assertIsNone(med.state.invested_vessel)
        e,med=scene(3)
        out=med.invest("patient",consenting=True)
        self.assertEqual((24,0),(out["ap_spent"],out["vp_spent"]))
        self.assertEqual(18,e.actors["medium"].ap_remaining)
        self.assertEqual("patient",med.state.invested_vessel)
        self.assertEqual((e.actors["medium"].vp_max,0,0),
                         (e.actors["medium"].vp_available,
                          e.actors["medium"].vp_committed,e.actors["medium"].vp_spent))
        with self.assertRaises(ValueError):
            med.invest("patient",consenting=True)
        e.check()

    def test_05_range_wall_corner_screen_and_intrusion_rejected_before_pulse(self):
        for case in ("range","wall","corner","screen","invisible","refused","blocked"):
            with self.subTest(case=case):
                patient_at=((5,1) if case=="range" else
                            (3,3) if case=="corner" else (3,1))
                walls=(((2,1),) if case in ("wall","corner") else ())
                e,med=scene(3,patient_at=patient_at,walls=walls,
                            third_at=(2,1) if case=="screen" else None)
                med.invest("patient",consenting=True)
                e.end_turn()
                args={"visible":case!="invisible","unopposed":case!="refused"}
                if case=="blocked":args["blocked_restoration"]=("hp",)
                with self.assertRaises((ValueError,UnresolvedDecision)):
                    med.declare_pulse("patient",**args)
                self.assertIsNone(med.pending)
                self.assertEqual(2,med.state.destiny)
                self.assertFalse(events(e,"g4_anointed_medium_returning_step_applied"))

    def test_06_no_forged_step_no_wrong_vessel_and_no_second_queued_pulse(self):
        e,med=scene(2)
        med.invest("patient",consenting=True)
        with self.assertRaises(ValueError):
            med.declare_pulse("patient",visible=True,unopposed=True)
        e.end_turn()
        with self.assertRaises(ValueError):
            med.declare_pulse("medium",visible=True,unopposed=True)
        med.declare_pulse("patient",visible=True,unopposed=True)
        with self.assertRaises(ValueError):
            med.declare_pulse("patient",visible=True,unopposed=True)
        with self.assertRaises(ValueError):
            med._preview_step(e.actors["patient"])
        self.assertFalse(events(e,"g4_anointed_medium_returning_step_applied"))
        e.start_turn("patient",regen_choice=RegenerationChoice())
        self.assertEqual(1,len(events(e,"g4_anointed_medium_returning_step_applied")))
        self.assertIsNone(med.pending)
        self.assertEqual(2,med.state.destiny)

    def test_07_g4_preflight_rechecks_changed_source_at_real_step(self):
        for case in ("moved","hp_block","no_vigor","full_hp"):
            with self.subTest(case=case):
                e,med=scene(1)
                med.invest("patient",consenting=True)
                e.end_turn()
                live={"blocked":False}
                def current_blocks(encounter,caster,recipient):
                    return ("hp",) if live["blocked"] else ()
                med.declare_pulse("patient",visible=True,unopposed=True,
                    restoration_check=(current_blocks if case=="hp_block" else None))
                patient=e.actors["patient"]
                if case=="moved":patient.occupied=((6,1),)
                elif case=="no_vigor":patient.vigor=0
                elif case=="full_hp":patient.hp=patient.hp_max
                else:
                    # An initially legal pulse cannot bypass a NEW live G4
                    # HP block established before the recipient's true Step.
                    live["blocked"]=True
                old=(patient.hp,patient.vigor,med.state.destiny)
                with self.assertRaises((ValueError,UnresolvedDecision)):
                    e.start_turn("patient",regen_choice=RegenerationChoice())
                self.assertEqual(old,(patient.hp,patient.vigor,med.state.destiny))
                self.assertFalse(events(e,"g4_anointed_medium_returning_step_applied"))
                self.assertIsNotNone(med.pending)

    def test_08_suspended_step_can_cancel_without_ap_destiny_or_healing(self):
        e,med=scene(2,hp=11,vigor=3)
        med.invest("patient",consenting=True)
        e.end_turn()
        med.declare_pulse("patient",lesser=True,visible=True,unopposed=True)
        with self.assertRaises(ValueError):
            e.start_turn("patient",regen_choice=RegenerationChoice(hp=2))
        self.assertIsNotNone(med.pending)
        med.cancel_pulse()
        self.assertIsNone(med.pending)
        self.assertEqual((11,3,2),(e.actors["patient"].hp,
                                   e.actors["patient"].vigor,med.state.destiny))
        self.assertEqual(1,len(events(e,"b05_medium_anointed_pulse_cancelled")))
        self.assertEqual(0,len(events(e,"g4_anointed_medium_returning_step_applied")))
        e.start_turn("patient",regen_choice=RegenerationChoice(hp=1))
        self.assertEqual((12,2,2),(e.actors["patient"].hp,
                                   e.actors["patient"].vigor,med.state.destiny))
        self.assertEqual(1,len([v for v in events(e,"regeneration_step")
                                if v["detail"]["actor"]=="patient"]))
        with self.assertRaises(ValueError):
            med.cancel_pulse()

    def test_09_direct_step_hook_cannot_spoof_g4_commit_authority(self):
        e,med=scene(2,hp=7,vigor=7)
        med.invest("patient",consenting=True)
        e.end_turn()
        med.declare_pulse("patient",visible=True,unopposed=True)
        def attempted_bypass(encounter,recipient_id):
            actor=encounter.actors[recipient_id]
            preview=med._preview_step(actor)
            self.assertIsNotNone(preview)
            before=(actor.hp,actor.vigor,med.state.destiny)
            with self.assertRaises(ValueError):
                med._apply_step(actor,preview)
            self.assertEqual(before,(actor.hp,actor.vigor,med.state.destiny))
            self.assertIsNone(encounter.g4._live_medium_anointed)
        e.start_turn("patient",regen_choice=RegenerationChoice(hp=1),
                     on_regeneration_ready=attempted_bypass)
        self.assertEqual((9,5),(e.actors["patient"].hp,
                                e.actors["patient"].vigor))
        self.assertEqual(1,len(events(e,"g4_anointed_medium_returning_step_applied")))
        self.assertIsNone(e.g4._live_medium_anointed)

    def test_10_dead_vessel_step_expires_queue_without_healing(self):
        e,med=scene(1)
        med.invest("patient",consenting=True)
        e.end_turn()
        med.declare_pulse("patient",lesser=True,visible=True,unopposed=True)
        patient=e.actors["patient"]
        patient.hp=-patient.hp_max
        patient.dead=True
        e.start_turn("patient",regen_choice=RegenerationChoice())
        self.assertIsNone(med.pending)
        self.assertEqual(2,med.state.destiny)
        self.assertEqual(1,len(events(e,"regeneration_dead")))
        self.assertEqual(1,len(events(e,"b05_medium_anointed_pulse_expired_on_death")))
        self.assertFalse(events(e,"g4_anointed_medium_returning_step_applied"))
        e.check()

    def test_11_no_native_guided_authority_g5_combat_or_independent_cert(self):
        e,med=scene(3)
        to_patient_step(e,med)
        self.assertFalse(any(x["kind"] in (
            "g5_melee_resolved","g4_basic_heal_applied",
            "g3_effect_established") for x in e.ledger))
        self.assertFalse(hasattr(e.actors["medium"],"destiny"))
        self.assertEqual(1,len(events(e,"g4_anointed_medium_returning_step_applied")))
        doc=(ROOT/"docs/design/b04-b05-medium-anointed-restoration-native-investment-step-v0.md").read_text()
        for phrase in ("24 AP","0 VP","0/12","0/6","+8 Intrusion","G0","G4","Guided Regeneration"):
            self.assertIn(phrase,doc)


if __name__=="__main__":
    unittest.main()
