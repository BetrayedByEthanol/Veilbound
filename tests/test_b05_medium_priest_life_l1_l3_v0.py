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

    def test_l3_intercession_absorbs_full_packet_before_current_vigor_cap(self):
        # Codex P2: 10 eligible Vigor against 2 Current Vigor and B8.
        # Do not clamp the packet to 2 before the defensive Reaction.
        e,c=scene(3)
        e.start_turn("medium")
        host=c.cast("medium","Vital Shelter","medium")
        target=e.actors["ally"]
        target.vigor=2
        result=e.g4.apply_damage(
            "ally",(DamagePacket("vigor","Direct Vigor",10),),
            event_key="intercede-10-vs-2",cause="confirmed_full_vigor_packet",
            medium_intercessor="medium")
        self.assertEqual(result["vigor_loss"],2)
        self.assertEqual(target.vigor,0)
        self.assertEqual(host.budget,0)
        self.assertFalse(e.g3.active("medium","Vital Shelter"))
        receipt=events(e,"b05_vital_intercession_packet")
        self.assertEqual(len(receipt),1)
        self.assertEqual((receipt[0]["original"],receipt[0]["prevented"],
                          receipt[0]["residual"],receipt[0]["budget"]),
                         (10,8,2,0))
        delivered=events(e,"g4_damage_applied")
        self.assertEqual(len(delivered),1)
        self.assertEqual(delivered[0]["vigor_details"],[
            {"raw":10,"available":2,"prevented":8,"applied":2}])
        priest=e.actors["medium"]
        self.assertEqual((priest.vp_available,priest.vp_committed,
                          priest.vp_spent,priest.reaction_available),
                         (9,0,3,False))
        self.assertIn("intercede-10-vs-2",e.g4.used_events)
        e.check()

    def test_ordinary_shelter_full_packet_and_zero_vigor_guard(self):
        # The same finite-budget rule applies to ordinary G3 Shelter, with
        # no Intercession Reaction/VP price.
        e,c=scene(3)
        e.start_turn("medium")
        host=c.cast("medium","Vital Shelter","ally")
        target=e.actors["ally"]
        target.vigor=2
        result=e.g4.apply_damage(
            "ally",(DamagePacket("vigor","Direct Vigor",10),),
            event_key="ordinary-10-vs-2",cause="confirmed_full_vigor_packet")
        self.assertEqual((result["vigor_loss"],target.vigor,host.budget),(2,0,0))
        self.assertEqual(events(e,"g4_damage_applied")[0]["vigor_details"],[
            {"raw":10,"available":2,"prevented":8,"applied":2}])
        priest=e.actors["medium"]
        self.assertEqual((priest.vp_available,priest.vp_committed,
                          priest.vp_spent,priest.reaction_available),
                         (11,0,1,True))
        self.assertFalse(e.g3.active("medium","Vital Shelter"))
        # With Current Vigor already zero, another shelter does not lose
        # prevention budget to a packet that cannot reduce Current Vigor.
        e2,c2=scene(3)
        e2.start_turn("medium")
        h2=c2.cast("medium","Vital Shelter","ally")
        ally2=e2.actors["ally"]
        ally2.vigor=0
        result2=e2.g4.apply_damage(
            "ally",(DamagePacket("vigor","Direct Vigor",10),),
            event_key="ordinary-at-zero",cause="confirmed_full_vigor_packet")
        self.assertEqual(result2["vigor_loss"],0)
        self.assertEqual(h2.budget,8)
        self.assertEqual(events(e2,"g4_damage_applied")[0]["vigor_details"],[
            {"raw":10,"available":0,"prevented":0,"applied":0}])
        e.check()
        e2.check()

    def test_self_intercession_mixed_dying_and_oversized_vigor_packet(self):
        # Keep the prior Codex P2 ordering guarantee while exercising the
        # full-packet cap: a Priest at 2 Vigor goes Dying on the HP part.
        e,c=scene(3)
        e.start_turn("medium")
        host=c.cast("medium","Vital Shelter","ally")
        priest=e.actors["medium"]
        priest.vigor=2
        result=e.g4.apply_damage(
            "medium",(DamagePacket("hp","Fire",12),
                      DamagePacket("vigor","Direct Vigor",10)),
            event_key="mixed-dying-oversized",cause="confirmed_mixed_packet",
            wound_location_roll=4,medium_intercessor="medium")
        self.assertEqual((result["hp_loss"],result["vigor_loss"]),(12,2))
        self.assertEqual((priest.hp,priest.vigor,priest.dead), (0,0,False))
        self.assertEqual((priest.vp_available,priest.vp_committed,
                          priest.vp_spent,priest.reaction_available),
                         (9,0,3,False))
        self.assertEqual(host.budget,0)
        self.assertFalse(e.g3.active("medium","Vital Shelter"))
        self.assertEqual(events(e,"b05_vital_intercession_packet")[0]["prevented"],8)
        self.assertEqual(events(e,"g4_damage_applied")[0]["vigor_details"],[
            {"raw":10,"available":2,"prevented":8,"applied":2}])
        self.assertEqual(len(priest.wounds),1)
        self.assertEqual(priest.wounds[0].source_event,"mixed-dying-oversized")
        self.assertEqual(len(events(e,"g4_damage_applied")),1)
        self.assertIn("mixed-dying-oversized",e.g4.used_events)
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

    def test_direct_intercede_vigor_cannot_forge_g4_packet(self):
        # Codex P2: do not trust that callers reached this through G3.
        e,c=scene(3)
        e.start_turn("medium")
        host=c.cast("medium","Vital Shelter","medium")
        a=e.actors["medium"]
        state=(a.vp_available,a.vp_committed,a.vp_spent,
               a.reaction_available,host.budget,len(e.ledger))
        for amount in (5,1):
            with self.subTest(amount=amount):
                with self.assertRaisesRegex(ValueError,"matching live G4"):
                    c.intercede_vigor("medium","ally",amount)
                self.assertEqual(
                    (a.vp_available,a.vp_committed,a.vp_spent,
                     a.reaction_available,host.budget,len(e.ledger)),state)
        with self.assertRaisesRegex(ValueError,"applying native G4"):
            e.g3.prevent_vigor("ally",5,medium_intercessor="medium")
        self.assertEqual(
            (a.vp_available,a.vp_committed,a.vp_spent,
             a.reaction_available,host.budget,len(e.ledger)),state)
        self.assertFalse(events(e,"b05_intercession_paid"))
        self.assertFalse(events(e,"b05_vital_intercession_packet"))
        e.check()

    def test_self_intercession_mixed_incapacitating_hit_is_atomic(self):
        # Codex P2: pay/resolve the already confirmed defensive Reaction
        # before the same event reduces the Medium caster to Dying.
        e,c=scene(3)
        e.start_turn("medium")
        host=c.cast("medium","Vital Shelter","ally")
        priest=e.actors["medium"]
        self.assertEqual((priest.hp,priest.vigor,host.budget),(12,36,8))
        result=e.g4.apply_damage(
            "medium",(DamagePacket("hp","Fire",12),
                      DamagePacket("vigor","Direct Vigor",5)),
            event_key="mixed-self-dying",cause="bounded_confirmed_mixed_packet",
            wound_location_roll=4,medium_intercessor="medium")
        self.assertEqual((result["hp_loss"],result["vigor_loss"]),(12,0))
        self.assertEqual((priest.hp,priest.vigor,priest.dead,
                          priest.ap_remaining),(0,36,False,0))
        self.assertEqual((priest.vp_available,priest.vp_committed,
                          priest.vp_spent,priest.reaction_available),
                         (7,2,3,False))
        self.assertEqual((host.recipient,host.budget),("ally",3))
        self.assertIn("mixed-self-dying",e.g4.used_events)
        self.assertEqual(len(priest.wounds),1)
        self.assertEqual(priest.wounds[0].source_event,"mixed-self-dying")
        self.assertEqual(len(events(e,"b05_intercession_paid")),1)
        self.assertEqual(len(events(e,"b05_vital_intercession_packet")),1)
        self.assertEqual(
            events(e,"b05_vital_intercession_packet")[0]["prevented"],5)
        self.assertEqual(len(events(e,"g4_damage_applied")),1)
        # The entire original source event is consumed: a retry cannot
        # apply its Vigor portion or grant another defensive Reaction.
        with self.assertRaisesRegex(ValueError,"already consumed"):
            e.g4.apply_damage(
                "medium",(DamagePacket("hp","Fire",12),
                          DamagePacket("vigor","Direct Vigor",5)),
                event_key="mixed-self-dying",cause="bounded_confirmed_mixed_packet",
                wound_location_roll=4,medium_intercessor="medium")
        with self.assertRaisesRegex(ValueError,"matching live G4"):
            c.intercede_vigor("medium","ally",5)
        e.check()

    def test_mixed_wound_preflight_rejects_before_reaction_and_damage(self):
        e,c=scene(3)
        e.start_turn("medium")
        host=c.cast("medium","Vital Shelter","ally")
        a=e.actors["medium"]
        previous=(a.hp,a.vigor,a.ap_remaining,a.vp_available,a.vp_spent,
                  a.reaction_available,host.budget,len(a.wounds),len(e.ledger))
        with self.assertRaisesRegex(UnresolvedDecision,"wound-location"):
            e.g4.apply_damage(
                "medium",(DamagePacket("hp","Fire",12),
                          DamagePacket("vigor","Direct Vigor",5)),
                event_key="needs-wound-location",cause="bounded_confirmed_mixed_packet",
                medium_intercessor="medium")
        self.assertEqual(
            (a.hp,a.vigor,a.ap_remaining,a.vp_available,a.vp_spent,
             a.reaction_available,host.budget,len(a.wounds),len(e.ledger)),
            previous)
        self.assertNotIn("needs-wound-location",e.g4.used_events)
        e.check()

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
