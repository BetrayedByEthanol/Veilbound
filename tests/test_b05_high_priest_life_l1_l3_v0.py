"""B04/B05 High Priest L1–3 authentic G0/G3/G4 action and prayer receipts."""
import unittest

from scripts.b05_high_priest_life_l1_l3_v0 import profile,verify
from scripts.b05_high_priest_life_invocation_v0 import HighLifeLiturgy
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState,DamagePacket


def scene(level=1,*,preparation="standard",walls=()):
    high=party_actor("H",level,"priest","party",occupied=((1,2),))
    ally=party_actor("F",level,"ally","party",occupied=((3,2),))
    e=Encounter([high,ally],{"priest":30,"ally":20},seed=550,
                scenario="B05-High-Priest-Life",
                policy="source_paid_unopposed_v0",
                objective="verify_high_access_and_price_not_full_encounter")
    GridMovement(e,width=9,height=6,walls=walls)
    SpellState(e)
    DamageState(e)
    ministry=HighLifeLiturgy(e,"priest",preparation=preparation)
    e.begin_round()
    return e,ministry


def events(e,kind):
    return [v["detail"] for v in e.ledger if v["kind"]==kind]


class HighLifeV0Tests(unittest.TestCase):
    def test_01_complete_structural_profiles_and_two_initial_lists(self):
        self.assertTrue(verify()["source_legal_structural"])
        for level in (1,2,3):
            for policy in ("standard","invocation","ward_invocation"):
                with self.subTest(level=level,policy=policy):
                    p=profile(level,preparation=policy)
                    a=party_actor("H",level,"H","party",occupied=((1,1),))
                    self.assertEqual(p["prepared_capacity"],4 if level==1 else 5)
                    self.assertEqual(len(p["prepared_prayers"])+p["open_prayer_slots"],
                                     p["prepared_capacity"])
                    self.assertEqual((a.hp_max,a.vigor_max,a.vp_max),
                                     (12,12*level,6*level))
                    self.assertEqual((a.ap_total,a.physical_ap,a.projection_ap),
                                     (30+6*(level-1),30,20))
                    self.assertEqual((a.regen,a.guard_capacity,a.guard_value),
                                     (4,1,17))
                    self.assertEqual(p["silver_remaining"],80)
                    self.assertEqual((p["accord"],p["resonance"]),(1,0))
                    self.assertEqual(p["talents"], ("TAL-C02",))
                    self.assertNotIn("TAL-M03", p["talents"])
                    self.assertEqual(sum(p["learned_disciplines"].values()),
                                     8 if level==1 else 9)
                    self.assertEqual(a.source.source_id,"H")
                    self.assertEqual(a.source.status,"STRUCTURAL_B05_ONLY")
                    self.assertFalse(a.source.attack_profiles)

    def test_02_illegal_preparation_and_unowned_actor_fail(self):
        for level in (0,4,True,1.5):
            with self.assertRaises(ValueError):
                profile(level)
        with self.assertRaises(ValueError):
            profile(1,preparation="fabricated")
        e,x=scene(1)
        with self.assertRaises(UnresolvedDecision):
            x.cast("ally","Basic Heal","ally",mode="instant",die=1)
        with self.assertRaises(UnresolvedDecision):
            e.g4.cast_basic_heal("priest","ally",die=1)
        with self.assertRaises((UnresolvedDecision,ValueError)):
            e.g3.cast_guided("priest",recipient="priest")
        self.assertEqual(e.actors["priest"].vp_available,6)

    def test_03_prepared_basic_heal_native_g4_receipt(self):
        for level in (1,2,3):
            with self.subTest(level=level):
                e,x=scene(level)
                ally=e.actors["ally"]
                ally.hp-=3
                ally.vigor-=8
                e.start_turn("priest")
                r=x.cast("priest","Basic Heal","ally",
                         mode="instant",tier=1,die=3,hand_available=True)
                self.assertEqual((r["hp_restored"],r["vigor_restored"]), (2,5))
                a=e.actors["priest"]
                self.assertEqual((a.ap_remaining,a.vp_available,a.vp_spent),
                                 (a.ap_total-20,a.vp_max-2,2))
                self.assertEqual(r["surcharge"],0)
                self.assertEqual(len(events(e,"g4_basic_heal_applied")),1)
                self.assertEqual(len(events(e,"regeneration_step")),1)
                self.assertEqual(events(e,"b05_high_life_applied")[0]["access"],
                                 "prepared")
                e.check()

    def test_04_invoked_basic_heal_full_action_and_3_vp(self):
        for level in (1,2,3):
            with self.subTest(level=level):
                e,x=scene(level,preparation="invocation")
                ally=e.actors["ally"]
                ally.hp-=3
                ally.vigor-=7
                e.start_turn("priest")
                r=x.cast("priest","Basic Heal","ally",
                         access="invocation",mode="instant",die=3,
                         hand_available=True)
                a=e.actors["priest"]
                self.assertEqual((r["spent_vp"],r["surcharge"],r["action_ap"]),
                                 (3,1,a.ap_total))
                self.assertEqual((a.ap_remaining,a.vp_available,a.vp_spent),
                                 (0,a.vp_max-3,3))
                self.assertEqual(events(e,"action_committed")[-1]["action_class"],
                                 "full")
                with self.assertRaises(UnresolvedDecision):
                    x.cast("priest","Basic Heal","ally",mode="instant",
                           die=3,hand_available=True)
                self.assertEqual(len(events(e,"b05_high_life_applied")),1)
                e.check()

    def test_05_unprepared_cannot_get_prepared_price_or_fake_invocation(self):
        e,x=scene(1,preparation="invocation")
        e.start_turn("priest")
        before=e.actors["priest"].ap_remaining
        for kind,access in (("Basic Heal","prepared"),
                            ("Guided Regeneration","invocation"),
                            ("Stone Skin","invocation"),
                            ("Guided Regeneration","open_prayer")):
            with self.subTest(kind=kind,access=access):
                with self.assertRaises((ValueError,UnresolvedDecision)):
                    x.cast("priest",kind,"priest",access=access,
                           mode="instant" if kind=="Basic Heal" else "maintained",
                           die=1 if kind=="Basic Heal" else None,
                           hand_available=True)
        self.assertEqual(e.actors["priest"].ap_remaining,before)

    def test_06_invocation_requires_whole_turn_unspent(self):
        e,x=scene(3,preparation="invocation")
        e.start_turn("priest")
        e.spend_ap("priest","projection",label="prior_legal_action")
        a=e.actors["priest"]
        before=(a.ap_remaining,a.vp_available)
        with self.assertRaisesRegex(ValueError,"untouched"):
            x.cast("priest","Basic Heal","priest",access="invocation",
                   mode="instant",die=2,hand_available=True)
        self.assertEqual((a.ap_remaining,a.vp_available),before)
        self.assertFalse(events(e,"b05_high_life_applied"))

    def test_07_no_surcharge_on_prepared_guided_and_real_step_only(self):
        e,x=scene(1)
        e.start_turn("priest")
        h=x.cast("priest","Guided Regeneration","ally")
        self.assertEqual((h.kind,h.recipient,h.committed,h.expiry_round),
                         ("Guided Regeneration","ally",2,None))
        self.assertEqual((e.actors["priest"].vp_available,
                          e.actors["priest"].vp_committed,
                          e.actors["priest"].vp_spent),(4,2,0))
        self.assertEqual(e.g3.regen_throughput("ally"),1)
        self.assertEqual(len(events(e,"regeneration_step")),1)
        e.end_turn()
        ally=e.actors["ally"]
        ally.hp-=3
        e.start_turn("ally",regen_choice=RegenerationChoice(hp=3))
        self.assertEqual(ally.hp,ally.hp_max)
        self.assertEqual(ally.vigor,ally.vigor_max-3)
        self.assertEqual(len(events(e,"regeneration_step")),2)

    def test_08_invoked_maintained_surcharge_is_spent_not_reserved(self):
        e,x=scene(1,preparation="ward_invocation")
        e.start_turn("priest")
        r=x.cast("priest","Vital Shelter","priest",access="invocation")
        self.assertEqual((r.committed,r.budget),(2,8))
        a=e.actors["priest"]
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(2,2,2))
        self.assertEqual(a.ap_remaining,0)
        self.assertEqual(events(e,"b05_high_life_applied")[0]["surcharge"],1)
        self.assertEqual(events(e,"action_committed")[-1]["action_class"],"full")
        # Releasing the reserve never refunds the separately spent surcharge
        # or the ordinary Spent establishment.
        e.g3.release("priest","Vital Shelter")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(4,0,2))
        e.check()

    def test_09_shelter_finite_real_g4_damage_and_release(self):
        e,x=scene(1)
        e.start_turn("priest")
        h=x.cast("priest","Vital Shelter","ally")
        self.assertEqual((h.committed,h.budget),(2,8))
        a=e.actors["priest"]
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(3,2,1))
        result=e.g4.apply_damage(
            "ally",(DamagePacket("vigor","Direct Vigor",5),),
            event_key="confirmed-vigor-packet",cause="bounded_attested_hit")
        self.assertEqual((result["vigor_loss"],h.budget),(0,3))
        e.g3.release("priest","Vital Shelter")
        self.assertEqual((a.vp_available,a.vp_committed,a.vp_spent),(5,0,1))
        self.assertEqual(len(events(e,"g3_effect_ended")),1)
        e.check()

    def test_10_l3_open_prayer_fills_exactly_one_slot_at_normal_cost(self):
        e,x=scene(3,preparation="invocation")
        self.assertEqual((len(x.prepared),x.capacity,x.open_slot),(4,5,True))
        e.start_turn("priest")
        r=x.cast("priest","Basic Heal","priest",access="open_prayer",
                 mode="instant",die=3,hand_available=True)
        self.assertEqual((r["spent_vp"],r["action_ap"],r["surcharge"]),(2,20,0))
        self.assertEqual((len(x.prepared),x.capacity,x.open_slot),
                         (5,5,False))
        self.assertEqual(x.open_filled,"Basic Heal")
        self.assertEqual(len(events(e,"b05_open_prayer_slot_filled")),1)
        with self.assertRaises(UnresolvedDecision):
            x.cast("priest","Vital Shelter","priest",access="open_prayer")
        self.assertEqual(e.actors["priest"].ap_remaining,22)
        r2=x.cast("priest","Basic Heal","priest",access="prepared",
                  mode="instant",die=2,hand_available=True)
        self.assertEqual(r2["spent_vp"],2)
        self.assertEqual(e.actors["priest"].ap_remaining,2)
        self.assertEqual(len(events(e,"b05_open_prayer_slot_filled")),1)

    def test_18_l3_open_prayer_can_fill_maintained_shelter_without_surcharge(self):
        e,x=scene(3,preparation="ward_invocation")
        e.start_turn("priest")
        host=x.cast("priest","Vital Shelter","ally",access="open_prayer")
        self.assertEqual((host.committed,host.budget),(2,8))
        self.assertEqual((len(x.prepared),x.open_filled,x.open_slot),
                         (5,"Vital Shelter",False))
        self.assertEqual((e.actors["priest"].vp_available,
                          e.actors["priest"].vp_committed,
                          e.actors["priest"].vp_spent),(15,2,1))
        self.assertEqual(e.actors["priest"].ap_remaining,22)
        self.assertEqual(events(e,"b05_high_life_applied")[0]["surcharge"],0)

    def test_19_invoked_fixed_primary_pays_ordinary_2_plus_surcharge(self):
        e,x=scene(2,preparation="ward_invocation")
        e.start_turn("priest")
        effect=x.cast("priest","Vital Shelter","priest",
                      access="invocation",mode="fixed")
        self.assertEqual((effect.committed,effect.budget),(0,8))
        self.assertEqual((e.actors["priest"].vp_available,
                          e.actors["priest"].vp_committed,
                          e.actors["priest"].vp_spent),(9,0,3))
        self.assertEqual(e.actors["priest"].ap_remaining,0)
        self.assertEqual(events(e,"b05_high_life_applied")[0]["surcharge"],1)

    def test_11_open_prayer_slot_persists_after_post_commit_interruption(self):
        e,x=scene(3,preparation="invocation")
        e.start_turn("priest")
        live={"hand":True}
        def committed(enc):
            live["hand"]=False
        r=x.cast("priest","Basic Heal","priest",access="open_prayer",
                 mode="instant",die=1,hand_available=True,
                 delivery_check=lambda enc,caster,recipient:
                     (live["hand"],True,True),
                 restoration_check=lambda enc,caster,recipient:(),
                 on_committed=committed)
        self.assertIsNone(r)
        self.assertEqual(x.open_filled,"Basic Heal")
        self.assertFalse(x.open_slot)
        self.assertEqual((e.actors["priest"].ap_remaining,
                          e.actors["priest"].vp_available),(22,18))
        self.assertEqual(len(events(e,"b05_high_cast_interrupted")),1)
        self.assertFalse(events(e,"g4_basic_heal_applied"))
        with self.assertRaises(UnresolvedDecision):
            x.cast("priest","Basic Heal","priest",access="open_prayer",
                   mode="instant",die=1,hand_available=True)
        e.check()

    def test_12_full_action_interrupted_before_application_spends_zero_vp(self):
        e,x=scene(1,preparation="invocation")
        e.start_turn("priest")
        live={"hand":True}
        def committed(enc):
            live["hand"]=False
        r=x.cast("priest","Basic Heal","priest",access="invocation",
                 mode="instant",die=1,hand_available=True,
                 delivery_check=lambda enc,caster,recipient:
                     (live["hand"],True,True),
                 restoration_check=lambda enc,caster,recipient:(),
                 on_committed=committed)
        self.assertIsNone(r)
        self.assertEqual(e.actors["priest"].ap_remaining,0)
        self.assertEqual((e.actors["priest"].vp_available,
                          e.actors["priest"].vp_spent),(6,0))
        self.assertEqual(events(e,"action_committed")[-1]["action_class"],"full")
        self.assertEqual(events(e,"b05_high_cast_interrupted")[0]["vp_spent"],0)

    def test_13_blocked_wall_and_missing_hand_preflight_atomically(self):
        e,x=scene(1,walls=((2,2),))
        e.start_turn("priest")
        a=e.actors["priest"]
        before=(a.ap_remaining,a.vp_available)
        with self.assertRaises(ValueError):
            x.cast("priest","Guided Regeneration","ally")
        with self.assertRaises(ValueError):
            x.cast("priest","Basic Heal","priest",
                   mode="instant",die=1,hand_available=False)
        self.assertEqual((a.ap_remaining,a.vp_available),before)
        self.assertFalse(events(e,"action_committed"))

    def test_14_l3_tier2_basic_heal_legal_but_no_t2_guided_shelter(self):
        e,x=scene(3)
        recipient=e.actors["ally"]
        recipient.hp-=4
        recipient.vigor-=13
        e.start_turn("priest")
        r=x.cast("priest","Basic Heal","ally",mode="instant",
                 tier=2,die=6,hand_available=True)
        self.assertEqual((r["spent_vp"],r["vigor_restored"]),(4,8))
        with self.assertRaises(ValueError):
            x.cast("priest","Guided Regeneration","priest",tier=2)
        self.assertEqual(e.actors["priest"].vp_spent,4)

    def test_15_fixed_modes_are_timed_spent_not_maintained(self):
        e,x=scene(2)
        e.start_turn("priest")
        h=x.cast("priest","Vital Shelter","priest",mode="fixed")
        self.assertEqual((h.committed,h.budget,h.expiry_round),
                         (0,8,e.round+10))
        self.assertEqual((e.actors["priest"].vp_available,
                          e.actors["priest"].vp_committed,
                          e.actors["priest"].vp_spent),(10,0,2))
        e.g3.release("priest","Vital Shelter")
        self.assertEqual(e.actors["priest"].vp_available,10)

    def test_16_source_prayers_not_automatically_executable(self):
        e,x=scene(2)
        e.start_turn("priest")
        before=(e.actors["priest"].ap_remaining,
                e.actors["priest"].vp_available)
        with self.assertRaises(UnresolvedDecision):
            x.cast("priest","Woodland Rapport","ally")
        self.assertEqual((e.actors["priest"].ap_remaining,
                          e.actors["priest"].vp_available),before)

    def test_17_same_turn_two_prepared_projections_only_at_l3(self):
        e,x=scene(3)
        e.start_turn("priest")
        first=x.cast("priest","Basic Heal","priest",
                     mode="instant",die=1,hand_available=True)
        second=x.cast("priest","Basic Heal","priest",
                      mode="instant",die=1,hand_available=True)
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertEqual(e.actors["priest"].ap_remaining,2)
        with self.assertRaises(ValueError):
            x.cast("priest","Basic Heal","priest",
                   mode="instant",die=1,hand_available=True)
        self.assertEqual(len(events(e,"g4_basic_heal_applied")),2)


if __name__=="__main__":
    unittest.main()
