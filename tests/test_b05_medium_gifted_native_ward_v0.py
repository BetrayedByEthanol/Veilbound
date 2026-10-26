"""Real G0/G1/G4/G5 Ward application, not the isolated design model."""
import unittest
from copy import deepcopy

from scripts.b05_medium_gifted_native_ward_v0 import (
    gifted_actor, MediumGiftedWardNative,
)
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, enemy_actor, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState, DamagePacket
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee


def scene(level=1, *, enemy="B06-EN-02", ally=False):
    gifted=gifted_actor(level,"gifted","party",occupied=((3,2),))
    friend=party_actor("R",1,"friend","party",occupied=((3,3),)) if ally else None
    location=((4,3),) if ally else ((4,2),)
    foe=enemy_actor(enemy,"foe","enemy",occupied=location,
                    **({"start_state":"prepared_start"} if enemy=="B06-EN-01" else {}))
    actors=[gifted]+([friend] if ally else [])+[foe]
    initiative={"gifted":50,"friend":40,"foe":20}
    e=Encounter(actors,{a.id:initiative[a.id] for a in actors},seed=2005,
                scenario="B04-B05-Medium-Ward-native",policy="source-dice",
                objective="bounded_native_ward")
    GridMovement(e,width=10,height=7,scene_id="medium-ward-grid")
    SpellState(e)
    DamageState(e)
    melee=SourceMelee(e)
    ward=MediumGiftedWardNative(e,"gifted")
    e.begin_round()
    e.start_turn("gifted")
    return e,ward,melee


def event(e,kind):
    return [x["detail"] for x in e.ledger if x["kind"]==kind]


def advance_to_foe(e):
    e.end_turn()
    if "friend" in e.actors:
        e.start_turn("friend")
        e.end_turn()
    e.start_turn("foe")


def hit(melee,*,target="gifted",profile="B06-AT-03",face=15,damage=5,vigor=None,defense="take_hit"):
    seq=melee.declare("foe",target,profiles=(profile,),defenses=(defense,))
    kw={"attack_face":face}
    if face != 1:
        kw["damage_face"]=damage
    if vigor is not None and face != 1:
        kw["vigor_die"]=vigor
    return melee.resolve(seq,0,**kw)


class MediumGiftedNativeWardTests(unittest.TestCase):
    def test_01_native_level_sheet_and_reserved_vp(self):
        for level in (1,2,3):
            e,w,_=scene(level)
            a=e.actors["gifted"]
            self.assertEqual((a.focus,a.vp_max,a.ap_total,a.guard_capacity),
                             ("Medium",4*level,30+6*(level-1),1))
            w.establish_emotion("Fear")
            serial=w.place(2)
            self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),
                             (4*level-2,2,0))
            self.assertEqual(a.ap_remaining,a.ap_total-24)
            self.assertEqual(w.conduits[0].serial,serial)
            self.assertEqual(w.conduits[0].status,"Active")
            e.check()

    def test_02_g5_soldier_hit_g4_holdfast_prevents_once(self):
        e,w,melee=scene()
        w.establish_emotion("Fear")
        w.place(2)
        advance_to_foe(e)
        before=e.actors["gifted"].hp
        outcome=hit(melee)
        self.assertEqual(outcome["outcome"],"hit")
        pulses=event(e,"b05_medium_ward_pulse")
        self.assertEqual(len(pulses),1)
        self.assertEqual((pulses[0]["emotion"],pulses[0]["prevented"]),("Fear",2))
        damage=event(e,"g4_damage_applied")[-1]
        self.assertEqual(damage["medium_gifted_ward"]["conduit_serial"],1)
        self.assertEqual(before-e.actors["gifted"].hp,damage["packets"][0]["mitigated"])
        self.assertEqual(damage["packets"][0]["raw"]-3-2,
                         damage["packets"][0]["mitigated"])
        leftover=w.preview("gifted",(DamagePacket("hp","Cut",5,armor_rule="weapon"),),(2,))
        self.assertEqual(leftover["prevention"],0)
        e.check()

    def test_03_g5_miss_does_not_spend_ward_pulse(self):
        e,w,melee=scene()
        w.establish_emotion("Fear")
        w.place(3)
        advance_to_foe(e)
        result=hit(melee,face=1)
        self.assertEqual(result["outcome"],"miss")
        self.assertFalse(event(e,"b05_medium_ward_pulse"))
        self.assertNotEqual(w.conduits[0].pulse_window,w.window)

    def test_04_g5_sentry_direct_vigor_trust_adjacent_other_ally(self):
        e,w,melee=scene(2,enemy="B06-EN-01",ally=True)
        w.establish_emotion("Trust")
        w.place(2)
        advance_to_foe(e)
        initial=e.actors["friend"].vigor
        result=hit(melee,target="friend",profile="B06-AT-02",vigor=4)
        self.assertEqual(result["outcome"],"hit")
        pulse=event(e,"b05_medium_ward_pulse")[-1]
        self.assertEqual((pulse["recipient"],pulse["prevented"],pulse["emotion"]),
                         ("friend",2,"Trust"))
        detail=event(e,"g4_damage_applied")[-1]
        self.assertEqual(detail["vigor_details"][0]["applied"],
                         detail["packets"][1]["mitigated"])
        self.assertEqual(initial-e.actors["friend"].vigor,
                         detail["vigor_details"][0]["applied"])
        self.assertEqual(detail["medium_gifted_ward"]["prevented"],2)
        e.check()

    def test_05_wrong_active_emotion_dormant_does_not_consume(self):
        e,w,melee=scene()
        w.establish_emotion("Joy")
        w.place(2)
        self.assertEqual(w.conduits[0].status,"Dormant")
        advance_to_foe(e)
        hit(melee)
        self.assertFalse(event(e,"b05_medium_ward_pulse"))
        self.assertEqual(e.actors["gifted"].vp_committed,2)

    def test_06_grade_three_starves_other_spend_and_direct_refund_denied(self):
        e,w,_=scene()
        w.establish_emotion("Fear")
        w.place(3)
        a=e.actors["gifted"]
        with self.assertRaises(ValueError):
            e.spend_vp("gifted",2,mode="spent",label="illegitimate")
        with self.assertRaises(ValueError):
            e.release_vp("gifted",3,label="unauthorized")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(1,3,0))

    def test_07_grade_change_does_not_create_extra_pulse(self):
        e,w,_=scene(3)
        w.establish_emotion("Fear")
        serial=w.place(1)
        # Native G4 confirmed packet demonstrates a consumed Pulse, followed
        # by next-window Reconduction. No extra Pulse from regrade alone.
        first=w.preview("gifted",(DamagePacket("hp","Cut",5,armor_rule="weapon"),),(2,))
        self.assertEqual(first["prevention"],1)
        e.end_turn()
        e.start_turn("foe")
        e.end_turn()
        e.begin_round()
        e.start_turn("gifted")
        w.establish_emotion("Fear")
        w.reconduct(serial,2)
        self.assertEqual(w.conduits[0].grade,2)
        self.assertEqual((e.actors["gifted"].vp_committed,
                          e.actors["gifted"].vp_spent),(2,3))

    def test_08_release_is_free_with_low_ap_and_locks_same_window(self):
        e,w,_=scene()
        w.establish_emotion("Fear")
        serial=w.place(2)
        self.assertLess(e.actors["gifted"].ap_remaining,24)
        w.release(serial)
        self.assertEqual((e.actors["gifted"].vp_available,
                          e.actors["gifted"].vp_committed),(4,0))
        with self.assertRaises(ValueError):
            w.place(1)

    def test_09_l3_placement_two_conduits_needs_two_turns(self):
        e,w,_=scene(3)
        w.establish_emotion("Fear")
        w.place(2)
        with self.assertRaises(ValueError):
            w.place(2)
        self.assertEqual(len(w.conduits),1)
        e.end_turn()
        e.start_turn("foe")
        e.end_turn()
        e.begin_round()
        e.start_turn("gifted")
        w.establish_emotion("Fear")
        w.place(2)
        self.assertEqual((len(w.conduits),e.actors["gifted"].vp_committed),(2,4))
        p=w.preview("gifted",(DamagePacket("hp","Cut",6,armor_rule="weapon"),),(3,))
        self.assertEqual((p["serial"],p["prevention"]),(1,2))

    def test_10_nonmatching_damage_type_and_zero_packets(self):
        e,w,_=scene()
        w.establish_emotion("Fear")
        w.place(2)
        cases=((DamagePacket("hp","Fire",5),5),
               (DamagePacket("vigor","Direct Vigor",4),4),
               (DamagePacket("hp","Cut",2,armor_rule="weapon"),0))
        for pkt,amount in cases:
            p=w.preview("gifted",(pkt,),(amount,))
            self.assertEqual(p["prevention"],0)
        self.assertNotEqual(w.conduits[0].pulse_window,w.window)

    def test_11_unset_emotion_does_not_create_free_pulse(self):
        e,w,_=scene()
        w.establish_emotion(None)
        w.place(2)
        self.assertEqual(w.conduits[0].status,"Dormant")
        self.assertEqual(w.preview("gifted",(DamagePacket("hp","Cut",5,
                          armor_rule="weapon"),),(2,))["prevention"],0)

    def test_12_no_client_supplied_packet_commit_authority(self):
        e,w,_=scene()
        w.establish_emotion("Fear")
        w.place(2)
        pkt=DamagePacket("hp","Cut",5,armor_rule="weapon")
        proposal=w.preview("gifted",(pkt,),(2,))
        with self.assertRaises(UnresolvedDecision):
            w.commit("gifted",(pkt,),proposal,event_key="fake",cause="caller:harm")
        self.assertNotEqual(w.conduits[0].pulse_window,w.window)
        self.assertFalse(event(e,"b05_medium_ward_pulse"))

    def test_13_failed_late_step5_does_not_reopen_window(self):
        e,w,_=scene()
        e.spend_ap("gifted","physical",label="early_action")
        with self.assertRaises(ValueError):
            w.establish_emotion("Fear")
        self.assertIsNone(w.window)

    def test_14_source_tampering_cannot_place_ward(self):
        e,w,_=scene()
        w.establish_emotion("Fear")
        a=e.actors["gifted"]
        a.source=deepcopy(a.source)
        # Source itself is immutable; a changed provenance must be rejected.
        from scripts.b06_encounter_state_v0 import Source
        a.source=Source("wrong",a.source.source_id,a.source.digest,
                        a.source.status,a.source.abilities,a.source.training,
                        a.source.equipment,a.source.attack_profiles,a.source.start_state)
        with self.assertRaises(UnresolvedDecision):
            w.place(1)


if __name__ == "__main__":
    unittest.main()
