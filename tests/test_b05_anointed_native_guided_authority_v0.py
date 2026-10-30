"""B04/B05 — native L3 High/Medium/Low Guided Regeneration Authority."""
from pathlib import Path
from hashlib import sha256
import unittest

from scripts.b05_anointed_native_guided_authority_v0 import AnointedGuidedAuthority
from scripts.b05_high_anointed_native_returning_step_v0 import HighAnointedRestoration
from scripts.b05_medium_anointed_native_returning_step_v0 import MediumAnointedRestoration
from scripts.b05_low_anointed_native_returning_step_v0 import LowAnointedRestoration
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState

ROOT=Path(__file__).resolve().parents[1]


def scene(role="AH",*,level=3,hp=6,vigor=6,patient_at=(3,1)):
    caster=party_actor(role,level,"caster","party",occupied=((1,1),))
    if role=="AL":
        caster.hp, caster.vigor=hp,vigor
        actors=[caster]
    else:
        patient=party_actor("AH",level,"patient","party",occupied=(patient_at,))
        patient.hp,patient.vigor=hp,vigor
        actors=[caster,patient]
    e=Encounter(actors,{x.id:30 if x.id=="caster" else 20 for x in actors},
                seed=1,scenario="B05-L3-Guided-Source-Native",
                objective="paid_technique_true_step_not_Focus_certification")
    GridMovement(e,width=8,height=6,scene_id="anointed-guided-native")
    SpellState(e)
    DamageState(e)
    classes={"AH":HighAnointedRestoration,
             "AM":MediumAnointedRestoration,
             "AL":LowAnointedRestoration}
    native=classes[role](e,"caster")
    guide=AnointedGuidedAuthority(e,"caster") if level==3 else None
    e.begin_round()
    return e,native,guide,"caster" if role=="AL" else "patient"


def entries(e,kind):
    return [x for x in e.ledger if x["kind"]==kind]


def funded(e,native,guide,recipient,*,mode="maintained"):
    # Real G0 action order; Medium must invest the Vessel in an earlier
    # turn because its L3 42 AP cannot pay 24+24 in the same turn.
    e.start_turn("caster",regen_choice=RegenerationChoice())
    if guide.focus=="Medium":
        native.invest(recipient,consenting=True)
        e.end_turn()
        e.start_turn(recipient,regen_choice=RegenerationChoice())
        e.end_turn()
        e.begin_round()
        e.start_turn("caster",regen_choice=RegenerationChoice())
    host=guide.cast(recipient,mode=mode,visible=True,unopposed=True)
    e.end_turn()
    if guide.focus=="Low":
        e.begin_round()
    return host


def apply(e,guide,recipient,*,choice=RegenerationChoice()):
    guide.declare_waiver(recipient,visible=True,unopposed=True)
    e.start_turn(recipient,regen_choice=choice)


class AnointedGuidedNativeTests(unittest.TestCase):
    def test_01_three_l3_focus_paid_maintained_host_and_free_increment(self):
        for role in ("AH","AM","AL"):
            with self.subTest(role=role):
                e,native,guide,patient=scene(role,hp=6,vigor=5)
                h=funded(e,native,guide,patient)
                self.assertEqual(2,h.committed)
                caster=e.actors["caster"]
                self.assertEqual((caster.vp_max-2,2,0),
                                 (caster.vp_available,caster.vp_committed,caster.vp_spent))
                apply(e,guide,patient,choice=RegenerationChoice(hp=1))
                recipient=e.actors[patient]
                self.assertEqual((8,4),(recipient.hp,recipient.vigor))
                self.assertEqual(1,native.state.destiny)
                paid=entries(e,"b05_anointed_guided_host_established")[0]["detail"]
                self.assertEqual(sha256((ROOT/caster.source.path).read_bytes()).hexdigest(),
                                 paid["source_digest"])
                self.assertEqual(caster.projection_ap,paid["ap_spent"])
                self.assertEqual(2,paid["vp_committed"])
                event=entries(e,"g4_anointed_guided_waiver_applied")[0]
                reg=[v for v in entries(e,"regeneration_step") if v["detail"]["actor"]==patient][-1]
                self.assertLess(reg["index"],event["index"])
                self.assertEqual((1,0,1),(event["detail"]["hp_restored"],
                                         event["detail"]["recipient_vigor_spent"],
                                         event["detail"]["destiny_cost"]))
                self.assertEqual(0,event["detail"]["activation_ap"])
                self.assertIsNone(guide.pending)
                e.check()

    def test_02_zero_vigor_free_increment_without_any_new_step(self):
        for role in ("AH","AM","AL"):
            with self.subTest(role=role):
                e,native,guide,recipient=scene(role,hp=7,vigor=0)
                funded(e,native,guide,recipient)
                apply(e,guide,recipient)
                a=e.actors[recipient]
                self.assertEqual((8,0),(a.hp,a.vigor))
                self.assertEqual(1,native.state.destiny)
                self.assertEqual(1,len(entries(e,"g4_anointed_guided_waiver_applied")))
                with self.assertRaises(ValueError):
                    e.g4.regenerate(a,RegenerationChoice())

    def test_03_fixed_host_is_spent_vp_and_not_a_destiny_discount(self):
        e,native,guide,recipient=scene("AH",hp=5,vigor=4)
        h=funded(e,native,guide,recipient,mode="fixed")
        self.assertEqual(0,h.committed)
        caster=e.actors["caster"]
        self.assertEqual((caster.vp_max-2,0,2),
                         (caster.vp_available,caster.vp_committed,caster.vp_spent))
        apply(e,guide,recipient)
        self.assertEqual((6,4),(e.actors[recipient].hp,e.actors[recipient].vigor))
        self.assertEqual(1,native.state.destiny)
        host=entries(e,"b05_anointed_guided_host_established")[0]["detail"]
        self.assertEqual((2,0),(host["vp_spent"],host["vp_committed"]))

    def test_04_ordinary_paid_guided_without_authority_spends_real_vigor(self):
        e,native,guide,recipient=scene("AH",hp=5,vigor=4)
        funded(e,native,guide,recipient)
        e.start_turn(recipient,regen_choice=RegenerationChoice(hp=4))
        self.assertEqual((9,0),(e.actors[recipient].hp,e.actors[recipient].vigor))
        self.assertEqual(2,native.state.destiny)
        self.assertEqual([],entries(e,"g4_anointed_guided_waiver_applied"))
        self.assertEqual(1,len([x for x in entries(e,"regeneration_step")
                                if x["detail"]["actor"]==recipient]))

    def test_05_invalid_normal_choice_does_not_spend_destiny_or_partially_heal(self):
        e,native,guide,recipient=scene("AH",hp=11,vigor=4)
        funded(e,native,guide,recipient)
        guide.declare_waiver(recipient,visible=True,unopposed=True)
        before=(e.actors[recipient].hp,e.actors[recipient].vigor,native.state.destiny)
        with self.assertRaises(ValueError):
            e.start_turn(recipient,regen_choice=RegenerationChoice(hp=1))
        self.assertEqual(before,(e.actors[recipient].hp,
                                 e.actors[recipient].vigor,native.state.destiny))
        self.assertIsNotNone(guide.pending)
        self.assertFalse(entries(e,"g4_anointed_guided_waiver_applied"))
        e.start_turn(recipient,regen_choice=RegenerationChoice())
        self.assertEqual((12,4,1),(e.actors[recipient].hp,
                                   e.actors[recipient].vigor,native.state.destiny))
        self.assertEqual(1,len(entries(e,"g4_anointed_guided_waiver_applied")))

    def test_06_direct_payout_from_step_callback_cannot_impersonate_g4(self):
        e,native,guide,recipient=scene("AH",hp=6,vigor=5)
        funded(e,native,guide,recipient)
        guide.declare_waiver(recipient,visible=True,unopposed=True)
        def fraudulent(encounter,actor_id):
            a=encounter.actors[actor_id]
            out=guide._preview_payout(a,missing_after_ordinary=3)
            with self.assertRaises(ValueError):
                guide._apply_step(a,out)
            self.assertEqual((6,5,2),(a.hp,a.vigor,native.state.destiny))
        e.start_turn(recipient,regen_choice=RegenerationChoice(),
                     on_regeneration_ready=fraudulent)
        self.assertEqual((7,5,1),(e.actors[recipient].hp,
                                  e.actors[recipient].vigor,native.state.destiny))

    def test_07_host_release_blocks_waiver_and_no_forged_source(self):
        e,native,guide,recipient=scene("AH")
        funded(e,native,guide,recipient)
        # Recipient turn is ready; maintained host can only be released on
        # caster's own ready turn, not through a caller's synthetic snapshot.
        e.start_turn(recipient,regen_choice=RegenerationChoice())
        e.end_turn()
        e.begin_round()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        e.g3.release("caster","Guided Regeneration")
        e.end_turn()
        with self.assertRaises(ValueError):
            guide.declare_waiver(recipient,visible=True,unopposed=True)
        self.assertEqual(2,native.state.destiny)
        self.assertEqual((e.actors["caster"].vp_max-0,0,0),
                         (e.actors["caster"].vp_available,
                          e.actors["caster"].vp_committed,e.actors["caster"].vp_spent))

    def test_08_cannot_apply_both_low_signature_and_guided_waiver_same_step(self):
        e,low,guide,recipient=scene("AL",hp=5,vigor=5)
        funded(e,low,guide,recipient)
        low.declare_pulse()
        guide.declare_waiver(recipient,visible=True,unopposed=True)
        before=(e.actors[recipient].hp,e.actors[recipient].vigor,low.state.destiny)
        with self.assertRaises(UnresolvedDecision):
            e.start_turn(recipient,regen_choice=RegenerationChoice())
        self.assertEqual(before,(e.actors[recipient].hp,
                                 e.actors[recipient].vigor,low.state.destiny))
        self.assertFalse(entries(e,"g4_anointed_guided_waiver_applied"))
        low.cancel_pulse()
        e.start_turn(recipient,regen_choice=RegenerationChoice())
        self.assertEqual((6,5,1),(e.actors[recipient].hp,
                                  e.actors[recipient].vigor,low.state.destiny))

    def test_09_reject_unsourced_l2_wrong_medium_vessel_and_refusal(self):
        e,native,unused,recipient=scene("AH",level=2)
        with self.assertRaises(ValueError):
            AnointedGuidedAuthority(e,"caster")
        e,native,guide,recipient=scene("AM",hp=6,vigor=4)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        with self.assertRaises(ValueError):
            guide.cast(recipient,mode="maintained",visible=True,unopposed=True)
        native.invest(recipient,consenting=True)
        with self.assertRaises(ValueError):
            guide.cast(recipient,mode="maintained",visible=True,unopposed=True)
        e.end_turn()
        e.start_turn(recipient,regen_choice=RegenerationChoice())
        e.end_turn()
        e.begin_round()
        e.start_turn("caster",regen_choice=RegenerationChoice())
        with self.assertRaises(UnresolvedDecision):
            guide.cast(recipient,mode="maintained",visible=True,unopposed=False)
        with self.assertRaises(ValueError):
            guide.cast("unknown",mode="maintained",visible=True,unopposed=True)
        self.assertEqual(42,e.actors["caster"].ap_remaining)
        self.assertEqual(2,native.state.destiny)

    def test_10_positive_non_dying_unsuppressed_guided_only(self):
        e,native,guide,recipient=scene("AH",hp=0,vigor=6)
        e.start_turn("caster",regen_choice=RegenerationChoice())
        with self.assertRaises(ValueError):
            guide.cast(recipient,mode="maintained",visible=True,unopposed=True)
        e,native,guide,recipient=scene("AH",hp=11,vigor=4)
        funded(e,native,guide,recipient)
        guide.declare_waiver(recipient,visible=True,unopposed=True)
        recipient_actor=e.actors[recipient]
        # If the native HP deficit disappears before Step, do not debit.
        recipient_actor.hp=recipient_actor.hp_max
        with self.assertRaises(ValueError):
            e.start_turn(recipient,regen_choice=RegenerationChoice())
        self.assertEqual(2,native.state.destiny)
        self.assertFalse(entries(e,"g4_anointed_guided_waiver_applied"))
        guide.cancel_waiver()
        e.start_turn(recipient,regen_choice=RegenerationChoice())

    def test_11_guided_weighted_diagonals_reject_paid_cast_without_ap_vp_loss(self):
        # Authoritative Guided 3D-equivalent distance is a + b/2 + c/2,
        # not Chebyshev. Both (3,1,0)=3.5 and (3,3,0)=4.5 are illegal.
        for role in ("AH","AM"):
            for target in ((4,2),(4,4)):
                with self.subTest(role=role,target=target):
                    e,native,guide,recipient=scene(role,patient_at=target)
                    e.start_turn("caster",regen_choice=RegenerationChoice())
                    if role=="AM":
                        native.invest(recipient,consenting=True)
                        e.end_turn()
                        e.start_turn(recipient,regen_choice=RegenerationChoice())
                        e.end_turn()
                        e.begin_round()
                        e.start_turn("caster",regen_choice=RegenerationChoice())
                    actor=e.actors["caster"]
                    before=(actor.ap_remaining,actor.vp_available,
                            actor.vp_spent,actor.vp_committed,native.state.destiny)
                    with self.assertRaises(ValueError):
                        guide.cast(recipient,mode="maintained",
                                   visible=True,unopposed=True)
                    self.assertEqual(before,
                                     (actor.ap_remaining,actor.vp_available,
                                      actor.vp_spent,actor.vp_committed,
                                      native.state.destiny))
                    self.assertFalse(entries(e,"b05_anointed_guided_host_established"))
                    self.assertFalse(e.g3.active("caster","Guided Regeneration"))
                    self.assertIsNone(guide.host)
                    e.check()

    def test_12_guided_weighted_boundary_admits_axis_three_and_diagonal_two_two(self):
        # Exactly 3 square-equivalents is legal: (3,0)=3 and (2,2)=3.
        for role in ("AH","AM"):
            for target in ((4,1),(3,3)):
                with self.subTest(role=role,target=target):
                    e,native,guide,recipient=scene(role,patient_at=target)
                    host=funded(e,native,guide,recipient)
                    self.assertEqual(3.0,guide._delivery(recipient,visible=True))
                    self.assertEqual(recipient,host.recipient)
                    self.assertEqual(1,len(entries(e,"b05_anointed_guided_host_established")))
                    self.assertEqual(2,host.committed)
                    e.check()

    def test_13_guided_authority_declaration_rechecks_weighted_range_without_destiny(self):
        # Establish valid paid Guided at (2,0), then move outside authored
        # range: declaration must not resurrect Chebyshev and spend Destiny.
        for role in ("AH","AM"):
            for target in ((4,2),(4,4)):
                with self.subTest(role=role,target=target):
                    e,native,guide,recipient=scene(role,patient_at=(3,1))
                    funded(e,native,guide,recipient)
                    e.actors[recipient].occupied=(target,)
                    before=(native.state.destiny,e.actors[recipient].hp,
                            e.actors[recipient].vigor)
                    with self.assertRaises(ValueError):
                        guide.declare_waiver(recipient,visible=True,unopposed=True)
                    self.assertEqual(before,(native.state.destiny,
                                             e.actors[recipient].hp,
                                             e.actors[recipient].vigor))
                    self.assertIsNone(guide.pending)
                    self.assertFalse(entries(e,"b05_anointed_guided_waiver_declared"))
                    self.assertFalse(entries(e,"g4_anointed_guided_waiver_applied"))
                    e.check()

    def test_14_no_extra_focus_certification_or_technique_discount(self):
        e,native,guide,recipient=scene("AH")
        funded(e,native,guide,recipient)
        self.assertEqual("STRUCTURAL_B05_ONLY",e.actors["caster"].source.status)
        self.assertFalse(hasattr(e.actors["caster"],"destiny"))
        self.assertFalse(entries(e,"g5_melee_resolved"))
        self.assertFalse(entries(e,"g4_anointed_guided_waiver_applied"))
        doc=(ROOT/"docs/design/b04-b05-anointed-l3-guided-regeneration-native-authority-v0.md").read_text()
        for phrase in ("12/12","0/12","0/6","G0","G3","G4",
                       "L3","2 VP","20/24/30","1 Destiny"):
            self.assertIn(phrase,doc)


if __name__=="__main__":
    unittest.main()
