"""B04/B05 Low Anointed native G0/G4 self-Embodiment Step acceptance."""
from pathlib import Path
from hashlib import sha256
import unittest

from scripts.b05_low_anointed_native_returning_step_v0 import LowAnointedRestoration
from scripts.b05_medium_anointed_native_returning_step_v0 import MediumAnointedRestoration
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState

ROOT=Path(__file__).resolve().parents[1]


def scene(level=1, *, hp=5, vigor=7, with_medium=False):
    low=party_actor("AL",level,"low","party",occupied=((2,2),))
    low.hp=hp
    low.vigor=vigor
    actors=[low]
    scores={"low":20}
    if with_medium:
        medium=party_actor("AM",level,"medium","party",occupied=((1,2),))
        actors.insert(0,medium)
        scores["medium"]=30
    e=Encounter(actors,scores,seed=0,scenario="B04-B05-Low-Anointed-native",
                objective="own_existing_G4_step_not_full_Focus_certification")
    GridMovement(e,width=7,height=7,scene_id="b05-low-native")
    SpellState(e)
    DamageState(e)
    low_adapter=LowAnointedRestoration(e,"low")
    medium_adapter=MediumAnointedRestoration(e,"medium") if with_medium else None
    e.begin_round()
    return e,low_adapter,medium_adapter


def events(e,kind):
    return [x for x in e.ledger if x["kind"]==kind]


class LowAnointedNativeTests(unittest.TestCase):
    def test_01_all_three_levels_one_real_step_and_1_to_1_self_vigor(self):
        for level in (1,2,3):
            with self.subTest(level=level):
                e,low,_=scene(level)
                low.declare_pulse()
                e.start_turn("low",regen_choice=RegenerationChoice(hp=1))
                a=e.actors["low"]
                self.assertEqual((7,5),(a.hp,a.vigor))
                self.assertEqual(1,len(events(e,"g4_anointed_low_returning_step_applied")))
                self.assertEqual(1,len(events(e,"regeneration_step")))
                pulse=events(e,"g4_anointed_low_returning_step_applied")[0]
                step=events(e,"regeneration_step")[0]
                self.assertLess(pulse["index"],step["index"])
                self.assertEqual((1,1,0,0,0),
                    (pulse["detail"]["hp_restored"],
                     pulse["detail"]["recipient_vigor_spent"],
                     pulse["detail"]["activation_ap"],pulse["detail"]["vp_spent"],
                     pulse["detail"]["destiny_cost"]))
                self.assertEqual((1,1),(step["detail"]["hp_restored"],
                                        step["detail"]["throughput_spent"]))
                self.assertEqual(2,low.state.destiny)
                self.assertIsNone(low.pending)
                self.assertEqual("low",pulse["detail"]["recipient"])
                self.assertEqual(sha256((ROOT/a.source.path).read_bytes()).hexdigest(),
                                 pulse["detail"]["source_digest"])
                self.assertEqual((a.vp_max,0,0),
                    (a.vp_available,a.vp_committed,a.vp_spent))
                self.assertEqual(30+6*(level-1),a.ap_remaining)
                self.assertEqual(5+int(level>=2),a.regen)
                self.assertEqual(3 if level==3 else 1,a.guard_capacity)
                e.check()

    def test_02_lesser_at_zero_vigor_spends_destiny_without_new_step(self):
        e,low,_=scene(3,hp=5,vigor=0)
        with self.assertRaises(ValueError):
            low.declare_pulse()
        low.declare_pulse(lesser=True)
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual((6,0,1),(e.actors["low"].hp,
                                   e.actors["low"].vigor,low.state.destiny))
        self.assertEqual(1,len(events(e,"regeneration_step")))
        self.assertEqual(0,events(e,"regeneration_step")[0]["detail"]["throughput_spent"])
        self.assertEqual(1,events(e,"g4_anointed_low_returning_step_applied")[0]["detail"]["destiny_cost"])
        with self.assertRaises(ValueError):
            e.g4.regenerate(e.actors["low"],RegenerationChoice())
        self.assertEqual(1,low.state.destiny)

    def test_03_unlawful_normal_allocation_is_atomic_and_retryable(self):
        e,low,_=scene(2,hp=11,vigor=4)
        low.declare_pulse(lesser=True)
        old=(e.actors["low"].hp,e.actors["low"].vigor,low.state.destiny)
        with self.assertRaises(ValueError):
            e.start_turn("low",regen_choice=RegenerationChoice(hp=1))
        self.assertEqual(old,(e.actors["low"].hp,
                              e.actors["low"].vigor,low.state.destiny))
        self.assertNotIn("low",e.regen_done)
        self.assertIsNotNone(low.pending)
        self.assertFalse(events(e,"g4_anointed_low_returning_step_applied"))
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual((12,4,1),(e.actors["low"].hp,
                                   e.actors["low"].vigor,low.state.destiny))
        self.assertEqual(1,len(events(e,"g4_anointed_low_returning_step_applied")))
        e.check()

    def test_04_only_genuine_next_self_step_may_deliver_pulse(self):
        e,low,_=scene(2,hp=4,vigor=8)
        low.declare_pulse()
        with self.assertRaises(ValueError):
            low.declare_pulse()
        with self.assertRaises(ValueError):
            low._preview_step(e.actors["low"])
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual(5,e.actors["low"].hp)
        with self.assertRaises(ValueError):
            low.declare_pulse()
        e.end_turn()
        e.begin_round()
        low.declare_pulse()
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual((6,6),(e.actors["low"].hp,e.actors["low"].vigor))
        self.assertEqual(2,len(events(e,"g4_anointed_low_returning_step_applied")))
        self.assertEqual(2,len(events(e,"regeneration_step")))

    def test_05_suppression_and_resume_only_during_true_turn_start_callback(self):
        e,low,_=scene(2,hp=5,vigor=7)
        with self.assertRaises(ValueError):
            low.toggle_embodiment(manifested=False)
        def suppress(encounter,recipient):
            self.assertEqual("low",recipient)
            self.assertFalse(low.toggle_embodiment(manifested=False))
            with self.assertRaises(ValueError):
                low.toggle_embodiment(manifested=True)
            with self.assertRaises(ValueError):
                low.declare_pulse()
        e.start_turn("low",regen_choice=RegenerationChoice(),
                     on_regeneration_ready=suppress)
        self.assertEqual((5,7),(e.actors["low"].hp,e.actors["low"].vigor))
        with self.assertRaises(ValueError):
            low.toggle_embodiment(manifested=True)
        e.end_turn()
        e.begin_round()
        with self.assertRaises(ValueError):
            low.declare_pulse()
        def resume(encounter,recipient):
            self.assertTrue(low.toggle_embodiment(manifested=True))
            low.declare_pulse()
        e.start_turn("low",regen_choice=RegenerationChoice(),
                     on_regeneration_ready=resume)
        self.assertEqual((6,6),(e.actors["low"].hp,e.actors["low"].vigor))
        self.assertEqual(1,len(events(e,"g4_anointed_low_returning_step_applied")))
        self.assertEqual(2,len(events(e,"b05_low_anointed_embodiment_set")))
        e.check()

    def test_06_reject_ineligible_self_dying_full_and_current_hp_block(self):
        for hp,vigor,lesser in ((12,7,False),(0,7,True),(5,0,False)):
            with self.subTest(hp=hp,vigor=vigor):
                e,low,_=scene(1,hp=hp,vigor=vigor)
                with self.assertRaises(ValueError):
                    low.declare_pulse(lesser=lesser)
                self.assertFalse(events(e,"g4_anointed_low_returning_step_applied"))
        e,low,_=scene(2)
        current={"blocked":False}
        def blocks(encounter,caster,recipient):
            return ("hp",) if current["blocked"] else ()
        low.declare_pulse(restoration_check=blocks)
        current["blocked"]=True
        before=(e.actors["low"].hp,e.actors["low"].vigor,low.state.destiny)
        with self.assertRaises(ValueError):
            e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual(before,(e.actors["low"].hp,e.actors["low"].vigor,low.state.destiny))
        low.cancel_pulse()
        e.start_turn("low",regen_choice=RegenerationChoice(hp=1))
        self.assertEqual((6,6,2),(e.actors["low"].hp,
                                  e.actors["low"].vigor,low.state.destiny))

    def test_07_callback_cannot_spoof_g4_authority_or_toggle_after_failure(self):
        e,low,_=scene(2,hp=11,vigor=5)
        low.declare_pulse(lesser=True)
        def try_direct(encounter,recipient):
            actor=encounter.actors[recipient]
            preview=low._preview_step(actor)
            self.assertIsNotNone(preview)
            with self.assertRaises(ValueError):
                low._apply_step(actor,preview)
            self.assertEqual(2,low.state.destiny)
            self.assertIsNone(encounter.g4._live_low_anointed)
        with self.assertRaises(ValueError):
            e.start_turn("low",regen_choice=RegenerationChoice(hp=1),
                         on_regeneration_ready=try_direct)
        with self.assertRaises(ValueError):
            low.toggle_embodiment(manifested=False)
        self.assertEqual((11,5,2),(e.actors["low"].hp,
                                   e.actors["low"].vigor,low.state.destiny))
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual((12,5,1),(e.actors["low"].hp,
                                   e.actors["low"].vigor,low.state.destiny))
        self.assertIsNone(e.g4._live_low_anointed)

    def test_08_suspended_step_can_cancel_without_destiny_or_ap_spend(self):
        e,low,_=scene(1,hp=11,vigor=3)
        low.declare_pulse(lesser=True)
        with self.assertRaises(ValueError):
            e.start_turn("low",regen_choice=RegenerationChoice(hp=1))
        low.cancel_pulse()
        self.assertEqual((11,3,2),(e.actors["low"].hp,
                                   e.actors["low"].vigor,low.state.destiny))
        self.assertEqual(1,len(events(e,"b05_low_anointed_pulse_cancelled")))
        e.start_turn("low",regen_choice=RegenerationChoice(hp=1))
        self.assertEqual((12,2,2),(e.actors["low"].hp,
                                   e.actors["low"].vigor,low.state.destiny))
        self.assertFalse(events(e,"g4_anointed_low_returning_step_applied"))
        with self.assertRaises(ValueError):
            low.cancel_pulse()

    def test_09_dead_at_actual_step_expires_queued_pulse_without_payment(self):
        e,low,_=scene(1,hp=5,vigor=7)
        low.declare_pulse(lesser=True)
        a=e.actors["low"]
        a.hp=-a.hp_max
        a.dead=True
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertIsNone(low.pending)
        self.assertEqual(2,low.state.destiny)
        self.assertEqual(1,len(events(e,"regeneration_dead")))
        self.assertEqual(1,len(events(e,"b05_low_anointed_pulse_expired_on_death")))
        self.assertFalse(events(e,"g4_anointed_low_returning_step_applied"))
        e.check()

    def test_10_second_medium_patient_pulse_on_same_step_fails_closed(self):
        e,low,medium=scene(2,with_medium=True,hp=5,vigor=7)
        e.start_turn("medium",regen_choice=RegenerationChoice())
        medium.invest("low",consenting=True)
        e.end_turn()
        medium.declare_pulse("low",visible=True,unopposed=True)
        low.declare_pulse()
        before=(e.actors["low"].hp,e.actors["low"].vigor,
                low.state.destiny,medium.state.destiny)
        with self.assertRaises(UnresolvedDecision):
            e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual(before,(e.actors["low"].hp,e.actors["low"].vigor,
                                 low.state.destiny,medium.state.destiny))
        self.assertFalse(events(e,"g4_anointed_low_returning_step_applied"))
        self.assertFalse(events(e,"g4_anointed_medium_returning_step_applied"))
        medium.cancel_pulse()
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual((6,6),(e.actors["low"].hp,e.actors["low"].vigor))
        self.assertEqual(1,len(events(e,"g4_anointed_low_returning_step_applied")))

    def test_11_low_l3_guard_talent_two_physical_actions_not_extra_pulse(self):
        e,low,_=scene(3,hp=4,vigor=8)
        self.assertEqual(3,e.actors["low"].guard_remaining)
        low.declare_pulse()
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual(1,len(events(e,"g4_anointed_low_returning_step_applied")))
        self.assertEqual(20,e.spend_ap("low","physical",label="paid sword one"))
        self.assertEqual(20,e.spend_ap("low","physical",label="paid sword two"))
        self.assertEqual(2,e.actors["low"].ap_remaining)
        with self.assertRaises(ValueError):
            e.spend_ap("low","projection",label="does not fit")
        with self.assertRaises(ValueError):
            low.declare_pulse()
        self.assertEqual(1,len(events(e,"g4_anointed_low_returning_step_applied")))
        self.assertEqual((e.actors["low"].vp_max,0,0),
                         (e.actors["low"].vp_available,
                          e.actors["low"].vp_committed,e.actors["low"].vp_spent))
        e.end_turn()

    def test_13_missing_allocation_retry_cannot_resume_suppressed_embodiment(self):
        # Codex P2: the original Step 1 was already entered without a
        # callback; Step-2's missing allocation MUST NOT create a new
        # Embodiment window just because a later retry supplies a callback.
        e,low,_=scene(2,hp=5,vigor=7)
        def suppress(encounter,recipient):
            self.assertFalse(low.toggle_embodiment(manifested=False))
        e.start_turn("low",regen_choice=RegenerationChoice(),
                     on_regeneration_ready=suppress)
        self.assertFalse(low.state.embodied)
        e.end_turn()
        e.begin_round()
        original_expiries=len(events(e,"turn_start_expiry"))
        with self.assertRaises(UnresolvedDecision):
            e.start_turn("low")  # Missing natural regeneration allocation.
        self.assertEqual("low",e.pending_regeneration)
        self.assertEqual("low",e.current)
        self.assertIsNone(e._live_regeneration_ready_callback)
        callback_retried=[]
        def forbidden_late_resume(encounter,recipient):
            callback_retried.append(recipient)
            self.assertIsNone(encounter._live_regeneration_ready_callback)
            with self.assertRaises(ValueError):
                low.toggle_embodiment(manifested=True)
            with self.assertRaises(ValueError):
                low.declare_pulse()
        e.start_turn("low",regen_choice=RegenerationChoice(hp=1),
                     on_regeneration_ready=forbidden_late_resume)
        self.assertEqual(["low"],callback_retried)
        self.assertFalse(low.state.embodied)
        self.assertEqual((6,6,2),(e.actors["low"].hp,
                                   e.actors["low"].vigor,low.state.destiny))
        self.assertEqual(original_expiries+1,len(events(e,"turn_start_expiry")))
        self.assertFalse(events(e,"g4_anointed_low_returning_step_applied"))
        self.assertEqual(1,len(events(e,"b05_low_anointed_embodiment_set")))
        self.assertIsNone(e._live_regeneration_ready_callback)
        e.check()

    def test_14_invalid_allocation_retry_cannot_toggle_again_but_next_turn_can(self):
        # A legitimate first-entry toggle (even when Step 2 later fails)
        # consumes its original timing window. The retry callback may make
        # normal policy choices but must not gain another toggle capability.
        e,low,_=scene(2,hp=11,vigor=7)
        def first_entry(encounter,recipient):
            self.assertEqual(recipient,encounter._live_regeneration_ready_callback)
            self.assertFalse(low.toggle_embodiment(manifested=False))
        with self.assertRaises(ValueError):
            e.start_turn("low",regen_choice=RegenerationChoice(hp=2),
                         on_regeneration_ready=first_entry)
        self.assertFalse(low.state.embodied)
        self.assertEqual("low",e.pending_regeneration)
        self.assertIsNone(e._live_regeneration_ready_callback)
        retried=[]
        def late(encounter,recipient):
            retried.append(recipient)
            self.assertIsNone(encounter._live_regeneration_ready_callback)
            with self.assertRaises(ValueError):
                low.toggle_embodiment(manifested=True)
            with self.assertRaises(ValueError):
                low.declare_pulse()
        e.start_turn("low",regen_choice=RegenerationChoice(hp=1),
                     on_regeneration_ready=late)
        self.assertEqual(["low"],retried)
        self.assertFalse(low.state.embodied)
        self.assertEqual((12,6,2),(e.actors["low"].hp,
                                    e.actors["low"].vigor,low.state.destiny))
        self.assertEqual(1,len(events(e,"b05_low_anointed_embodiment_set")))
        self.assertFalse(events(e,"g4_anointed_low_returning_step_applied"))
        e.end_turn()
        e.begin_round()
        def next_real_turn(encounter,recipient):
            self.assertEqual(recipient,encounter._live_regeneration_ready_callback)
            self.assertTrue(low.toggle_embodiment(manifested=True))
        e.start_turn("low",regen_choice=RegenerationChoice(),
                     on_regeneration_ready=next_real_turn)
        self.assertTrue(low.state.embodied)
        self.assertEqual(2,len(events(e,"b05_low_anointed_embodiment_set")))
        self.assertIsNone(e._live_regeneration_ready_callback)
        e.check()

    def test_12_source_binding_and_no_unsupported_focus_certificate(self):
        for role in ("AH","AM"):
            wrong=party_actor(role,1,"a","party",occupied=((0,0),))
            e=Encounter([wrong],{"a":10},seed=0)
            SpellState(e)
            DamageState(e)
            with self.assertRaises(ValueError):
                LowAnointedRestoration(e,"a")
        e,low,_=scene(3)
        self.assertEqual("STRUCTURAL_B05_ONLY",e.actors["low"].source.status)
        self.assertEqual((),e.actors["low"].source.attack_profiles)
        self.assertFalse(hasattr(e.actors["low"],"destiny"))
        self.assertFalse(events(e,"g5_melee_resolved"))
        doc=(ROOT/"docs/design/b04-b05-low-anointed-restoration-native-embodied-step-v0.md").read_text()
        for phrase in ("12/12","0/12","0/6","G0","G4","Guided Regeneration",
                       "Embodiment","1 Destiny","Regeneration Step"):
            self.assertIn(phrase,doc)


if __name__=="__main__":
    unittest.main()
