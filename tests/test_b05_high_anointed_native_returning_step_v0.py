"""Native High Anointed Returning Step: G0 paid source / G1 path / G4 Vigor ledger."""
from pathlib import Path
from hashlib import sha256
import unittest

from scripts.b05_high_anointed_native_returning_step_v0 import HighAnointedRestoration
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState

ROOT = Path(__file__).resolve().parents[1]


def native_scene(level=1, *, high_at=(1,1), recipient_at=(3,1),
                 walls=(), recipient_hp=6, recipient_vigor=7):
    high = party_actor("AH",level,"high","party",occupied=(high_at,))
    patient = party_actor("AM",level,"patient","party",occupied=(recipient_at,))
    patient.hp = recipient_hp
    patient.vigor = recipient_vigor
    e = Encounter([high,patient],{"high":30,"patient":20},
                  seed=0,scenario="B04-B05-High-Anointed-Returning-Step-native",
                  objective="source_paid_native_g4_healing_not_victory")
    GridMovement(e,width=9,height=7,walls=walls,scene_id="b05-high-restoration")
    SpellState(e)
    DamageState(e)
    adapter = HighAnointedRestoration(e,"high")
    e.begin_round()
    e.start_turn("high",regen_choice=RegenerationChoice())
    return e,adapter


def entries(e,kind):
    return [v for v in e.ledger if v["kind"]==kind]


class NativeHighAnointedRestorationTests(unittest.TestCase):
    def test_01_real_g0_g4_baseline_pays_only_recipient_vigor(self):
        for lv in (1,2,3):
            with self.subTest(level=lv):
                e,a=native_scene(lv)
                hp_before=e.actors["patient"].hp
                vigor_before=e.actors["patient"].vigor
                out=a.project("patient",visible=True,unopposed=True)
                self.assertEqual((2,2,20,0,2),
                    (out["hp_restored"],out["recipient_vigor_spent"],
                     out["ap_spent"],out["vp_spent"],out["destiny_remaining"]))
                self.assertEqual((hp_before+2,vigor_before-2),
                                 (e.actors["patient"].hp,e.actors["patient"].vigor))
                self.assertEqual(e.actors["high"].ap_total-20,e.actors["high"].ap_remaining)
                self.assertEqual((e.actors["high"].vp_max,0,0),
                    (e.actors["high"].vp_available,e.actors["high"].vp_committed,
                     e.actors["high"].vp_spent))
                self.assertEqual(1,len(entries(e,"g4_anointed_returning_step_applied")))
                self.assertEqual(1,len(entries(e,"b05_high_anointed_signature_resolved")))
                event=entries(e,"g4_anointed_returning_step_applied")[0]["detail"]
                source_action=e.ledger[event["action_index"]]
                self.assertEqual(("action_committed","projection",20),
                    (source_action["kind"],source_action["detail"]["action_class"],
                     source_action["detail"]["ap_spent"]))
                self.assertEqual(sha256((ROOT/e.actors["high"].source.path).read_bytes()).hexdigest(),
                                 event["source_digest"])
                self.assertEqual((0,2),(event["vp_spent"],event["recipient_vigor_spent"]))
                e.check()

    def test_02_finite_lesser_destiny_at_zero_vigor_and_no_free_vp(self):
        e,a=native_scene(3,recipient_hp=2,recipient_vigor=0)
        for remaining in (1,0):
            out=a.project("patient",lesser=True,visible=True,unopposed=True)
            self.assertEqual((2,0,remaining),
                (out["hp_restored"],out["recipient_vigor_spent"],
                 out["destiny_remaining"]))
            self.assertEqual(0,e.actors["patient"].vigor)
        self.assertEqual(2,e.actors["high"].ap_remaining)
        before=(e.actors["high"].ap_remaining,len(e.ledger))
        with self.assertRaises(ValueError):
            a.project("patient",lesser=True,visible=True,unopposed=True)
        self.assertEqual(before,(e.actors["high"].ap_remaining,len(e.ledger)))
        self.assertEqual(2,len(entries(e,"g4_anointed_returning_step_applied")))
        self.assertEqual(0,a.state.destiny)
        self.assertEqual((e.actors["high"].vp_max,0,0),
            (e.actors["high"].vp_available,e.actors["high"].vp_committed,
             e.actors["high"].vp_spent))

    def test_03_missing_hp_dying_full_hp_and_zero_vigor_fail_before_ap(self):
        for hp,vigor,lesser in ((12,7,False),(0,7,True),(6,0,False)):
            with self.subTest(hp=hp,vigor=vigor,lesser=lesser):
                e,a=native_scene(1,recipient_hp=hp,recipient_vigor=vigor)
                before=e.actors["high"].ap_remaining
                with self.assertRaises(ValueError):
                    a.project("patient",visible=True,unopposed=True,lesser=lesser)
                self.assertEqual(before,e.actors["high"].ap_remaining)
                self.assertEqual([],entries(e,"g4_anointed_returning_step_applied"))

    def test_04_high_l1_range_limit_l2_expansion_wall_and_corner(self):
        for level,good in ((1,False),(2,True),(3,True)):
            e,a=native_scene(level,recipient_at=(5,1))
            ap=e.actors["high"].ap_remaining
            if good:
                self.assertEqual(2,a.project("patient",visible=True,unopposed=True)["hp_restored"])
            else:
                with self.assertRaises(ValueError):
                    a.project("patient",visible=True,unopposed=True)
                self.assertEqual(ap,e.actors["high"].ap_remaining)
        for walls,at,exc in (
            (((2,1),),(3,1),ValueError),
            (((2,1),),(3,3),UnresolvedDecision),
        ):
            e,a=native_scene(2,recipient_at=at,walls=walls)
            with self.assertRaises(exc):
                a.project("patient",visible=True,unopposed=True)
            self.assertEqual(36,e.actors["high"].ap_remaining)

    def test_05_unopposed_intrusion_and_current_g4_blocks_are_required(self):
        for kwargs, error in (
            ({"visible":False,"unopposed":True},UnresolvedDecision),
            ({"visible":True,"unopposed":False},UnresolvedDecision),
            ({"visible":True,"unopposed":True,"blocked_restoration":("hp",)},ValueError),
            ({"visible":True,"unopposed":True,
              "restoration_check":lambda e,c,r: ("hp",)},ValueError),
        ):
            e,a=native_scene()
            with self.subTest(kwargs=tuple(kwargs)),self.assertRaises(error):
                a.project("patient",**kwargs)
            self.assertEqual(30,e.actors["high"].ap_remaining)
            self.assertFalse(entries(e,"g4_anointed_returning_step_applied"))
        # Blocking external Vigor *restoration* alone does not prohibit the
        # recipient's own Vigor expenditure to restore HP.
        e,a=native_scene()
        out=a.project("patient",visible=True,unopposed=True,
                      blocked_restoration=("vigor",))
        self.assertEqual((2,2),(out["hp_restored"],out["recipient_vigor_spent"]))

    def test_06_native_source_binding_cannot_be_forged_by_other_focus(self):
        for role in ("AM","AL"):
            actor=party_actor(role,1,"caster","party",occupied=((1,1),))
            e=Encounter([actor],{"caster":30},seed=0)
            GridMovement(e,width=6,height=6)
            SpellState(e)
            DamageState(e)
            with self.assertRaises(ValueError):
                HighAnointedRestoration(e,"caster")
        e,a=native_scene()
        with self.assertRaises(ValueError):
            HighAnointedRestoration(e,"high")
        self.assertEqual(2,a.state.destiny)

    def test_07_g4_direct_delivery_requires_live_bound_paid_action(self):
        e,a=native_scene()
        before=len(e.ledger)
        self.assertEqual(20,e.spend_ap("high","projection",
                                      label="anointed:high:returning_step"))
        with self.assertRaises(ValueError):
            e.g4.apply_high_anointed_returning_step(
                "high","patient",action_index=before,
                hp_restored=2,recipient_vigor_spent=2,lesser=False)
        self.assertEqual((6,7),(e.actors["patient"].hp,e.actors["patient"].vigor))
        self.assertFalse(entries(e,"g4_anointed_returning_step_applied"))
        # A legitimate new paid action remains available only while AP lasts.
        with self.assertRaises(ValueError):
            a.project("patient",visible=True,unopposed=True)

    def test_08_no_native_g5_miracles_or_independent_focus_certificate(self):
        e,a=native_scene(3)
        out=a.project("patient",visible=True,unopposed=True)
        self.assertEqual(20,out["ap_spent"])
        self.assertFalse(any(v["kind"] in (
            "g5_melee_resolved","g3_effect_established",
            "g4_basic_heal_applied") for v in e.ledger))
        self.assertEqual((),e.actors["high"].source.attack_profiles)
        self.assertEqual("STRUCTURAL_B05_ONLY",e.actors["high"].source.status)
        doc=(ROOT/"docs/design/b04-b05-high-anointed-restoration-native-returning-step-v0.md").read_text()
        for phrase in ("0/12","0/6","20 AP","G0","G4","+8 Intrusion","G5"):
            self.assertIn(phrase,doc)


if __name__ == "__main__":
    unittest.main()
