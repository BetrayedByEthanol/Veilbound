"""B04/B05 Medium Priest Life: source sheet and bounded native G0/G3/G4 receipts."""
import unittest

from scripts.b05_medium_priest_life_l1_l3_v0 import profile, verify
from scripts.b05_medium_priest_consecrations_v0 import MediumLifeConsecrations
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState, DamagePacket


def scene(level=3, *, walls=()):
    m = party_actor("M",level,"medium","party",occupied=((1,2),))
    f = party_actor("F",level,"ally","party",occupied=((3,2),))
    e = Encounter([m,f], {"medium":30,"ally":20},
                  seed=530, scenario="B05-Medium-Life",
                  policy="authored_unopposed_cooperative",
                  objective="source_bound_focus_receipts")
    GridMovement(e,width=10,height=7,walls=walls)
    SpellState(e)
    DamageState(e)
    c = MediumLifeConsecrations(e)
    e.begin_round()
    return e,c


def events(e, kind):
    return [v["detail"] for v in e.ledger if v["kind"]==kind]


class MediumLifeTest(unittest.TestCase):
    def test_structural_l1_l3_full_source_and_budget(self):
        self.assertTrue(verify()["source_legal_structural"])
        for lv in (1,2,3):
            with self.subTest(level=lv):
                p=profile(lv)
                a=party_actor("M",lv,"medium","party",occupied=((1,1),))
                self.assertEqual((p["hp_max"],p["vigor_max"],p["vp_max"]),
                                 (12,12*lv,4*lv))
                self.assertEqual((p["turn_ap"],p["physical_action_ap"],
                                  p["projection_action_ap"]), (30+6*(lv-1),24,24))
                self.assertEqual(p["prepared_capacity"],3 if lv==1 else 4)
                self.assertEqual((p["accord"],p["silver_remaining"]),(1,80))
                self.assertEqual(sum(p["equipment_sp"].values()),70)
                self.assertEqual(sum(p["learned_disciplines"].values()),
                                 8 if lv==1 else 9)
                self.assertEqual((a.regen,a.guard_value,a.guard_capacity),(5,17,1))
                self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),
                                 (4*lv,0,0))
                self.assertEqual(len(p["talents"]),1 if lv<3 else 2)
                self.assertEqual(p["universals"][-1],
                                 "Blink" if lv==3 else "Veil Inspection")

    def test_invalid_levels_and_source_policy_rejected(self):
        for lv in (0,4,True,1.5):
            with self.assertRaises(ValueError):
                profile(lv)
        e,c=scene(3)
        with self.assertRaises(UnresolvedDecision):
            c.cast("ally","Guided Regeneration","medium")
        with self.assertRaises(UnresolvedDecision):
            c.cast("medium","Basic Heal","ally")

    def test_l1_guided_ap_and_vp_and_no_free_step(self):
        e,c=scene(1)
        e.start_turn("medium")
        host=c.cast("medium","Guided Regeneration","ally")
        self.assertEqual((host.recipient,host.committed,host.budget),("ally",2,None))
        a=e.actors["medium"]
        self.assertEqual((a.ap_remaining,a.vp_available,a.vp_committed,a.vp_spent),
                         (6,2,2,0))
        self.assertEqual(e.g3.regen_throughput("ally"),1)
        self.assertEqual(e.actors["ally"].hp,e.actors["ally"].hp_max)
        with self.assertRaises(ValueError):
            c.cast("medium","Vital Shelter","medium")
        with self.assertRaises(ValueError):
            c.reassign("medium","ally")
        e.g3.release("medium","Guided Regeneration")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(4,0,0))
        self.assertEqual(e.g3.regen_throughput("ally"),0)
        e.check()

    def test_l1_shelter_budget_and_maintained_spent_release(self):
        e,c=scene(1)
        e.start_turn("medium")
        h=c.cast("medium","Vital Shelter","medium")
        self.assertEqual(h.budget,8)
        a=e.actors["medium"]
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(1,2,1))
        e.g3.release("medium","Vital Shelter")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,0,1))
        with self.assertRaises(ValueError):
            c.cast("medium","Vital Shelter","medium") # only 6 AP left
        e.check()

    def test_reassign_same_effect_no_refresh_or_extra_vp(self):
        e,c=scene(2)
        e.start_turn("medium")
        h=c.cast("medium","Vital Shelter","medium")
        # Native G4 direct Vigor packet consumes this exact G3 host budget.
        result=e.g4.apply_damage("medium",(DamagePacket("vigor","Direct Vigor",5),),
                                 event_key="confirmed-vigor-1",
                                 cause="bounded_attested_packet_fixture")
        self.assertEqual(result["vigor_loss"],0)
        self.assertEqual(h.budget,3)
        a=e.actors["medium"]
        before=(a.vp_available,a.vp_committed,a.vp_spent)
        self.assertEqual(a.ap_remaining,12)
        with self.assertRaises(ValueError):
            c.reassign("medium","ally") # cannot reassign in the same 36-AP turn
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),before)
        e.end_turn()
        e.start_turn("ally")
        e.end_turn()
        e.begin_round()
        e.start_turn("medium")
        self.assertTrue(c.reassign("medium","ally"))
        self.assertEqual((h.recipient,h.budget,h.committed),("ally",3,2))
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),before)
        self.assertEqual(a.ap_remaining,12)
        self.assertEqual(len(events(e,"g3_effect_established")),1)
        self.assertEqual(len(events(e,"b05_consecration_reassigned")),1)
        e.check()

    def test_blocked_and_out_of_range_targets_preflight_without_ap(self):
        e,c=scene(3,walls=((2,2),))
        e.start_turn("medium")
        before=(e.actors["medium"].ap_remaining,e.actors["medium"].vp_available)
        with self.assertRaises(ValueError):
            c.cast("medium","Guided Regeneration","ally")
        self.assertEqual((e.actors["medium"].ap_remaining,
                          e.actors["medium"].vp_available),before)
        self.assertFalse(e.g3.effects)

    def test_l3_guided_intercession_exact_real_step(self):
        e,c=scene(3)
        e.start_turn("medium")
        host=c.cast("medium","Guided Regeneration","medium")
        e.end_turn()
        f=e.actors["ally"]
        f.hp=f.hp_max-4
        f.vigor=f.vigor_max
        before=e.actors["medium"].vp_available
        def response(enc,who):
            self.assertEqual((enc.pending_regeneration,enc.current),("ally","ally"))
            c.intercede_regeneration("medium",who)
        e.start_turn("ally",regen_choice=RegenerationChoice(hp=4),
                     on_regeneration_ready=response)
        self.assertEqual((f.hp,f.vigor),(f.hp_max,f.vigor_max-4))
        self.assertEqual(e.g3.regen_throughput("ally"),0)
        self.assertEqual(host.recipient,"medium")
        self.assertEqual(e.actors["medium"].vp_available,before-2)
        self.assertFalse(e.actors["medium"].reaction_available)
        self.assertEqual(len(events(e,"b05_guided_intercession_finished")),1)
        with self.assertRaises(ValueError):
            c.intercede_regeneration("medium","ally")
        e.check()

    def test_l3_vital_intercession_native_g4_packet_and_exhaustion(self):
        e,c=scene(3)
        e.start_turn("medium")
        h=c.cast("medium","Vital Shelter","medium")
        e.g4.apply_damage("medium",(DamagePacket("vigor","Direct Vigor",3),),
                          event_key="packet-initial",cause="bounded_attested_packet_fixture")
        self.assertEqual(h.budget,5)
        before=e.actors["ally"].vigor
        result=e.g4.apply_damage(
            "ally",(DamagePacket("vigor","Direct Vigor",7),),
            event_key="packet-ally",cause="bounded_attested_packet_fixture",
            medium_intercessor="medium")
        self.assertEqual(result["vigor_loss"],2)
        self.assertEqual(e.actors["ally"].vigor,before-2)
        self.assertFalse(e.g3.active("medium","Vital Shelter"))
        self.assertEqual((e.actors["medium"].vp_available,
                          e.actors["medium"].vp_committed,
                          e.actors["medium"].vp_spent),(9,0,3))
        self.assertEqual(events(e,"b05_vital_intercession_packet")[0]["prevented"],5)
        self.assertFalse(e.actors["medium"].reaction_available)
        e.check()

    def test_intercession_fail_closed_pre_damage_no_consumption(self):
        e,c=scene(3)
        e.start_turn("medium")
        c.cast("medium","Guided Regeneration","medium")
        a=e.actors["medium"]
        state=(a.vp_available,a.vp_spent,a.reaction_available,
               len(e.g4.used_events))
        with self.assertRaises(ValueError):
            e.g4.apply_damage(
                "ally",(DamagePacket("vigor","Direct Vigor",2),),
                event_key="unauthorized-medium",cause="bounded_fixture",
                medium_intercessor="medium")
        self.assertEqual((a.vp_available,a.vp_spent,a.reaction_available,
                          len(e.g4.used_events)),state)
        with self.assertRaises(ValueError):
            e.g4.apply_damage("ally",(DamagePacket("hp","Fire",2),),
                              event_key="no-vigor",cause="bounded_fixture",
                              medium_intercessor="medium")
        self.assertEqual(a.vp_spent,0)

    def test_deterministic_ledger_and_unsupported_options(self):
        def witness():
            e,c=scene(3)
            e.start_turn("medium")
            c.cast("medium","Guided Regeneration","ally")
            e.end_turn()
            a=e.actors["ally"];a.hp-=2
            e.start_turn("ally",regen_choice=RegenerationChoice(hp=2))
            e.end_turn()
            e.check()
            return e.serialize()
        self.assertEqual(witness(),witness())
        e,c=scene(1)
        e.start_turn("medium")
        with self.assertRaises(UnresolvedDecision):
            c.cast("medium","Venom Endurance","medium")
        self.assertEqual(e.actors["medium"].ap_remaining,30)


if __name__ == "__main__":
    unittest.main()
