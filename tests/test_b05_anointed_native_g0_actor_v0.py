"""Source-bound Anointed AH/AM/AL G0 actor bridge and real regeneration."""
from pathlib import Path
from hashlib import sha256
import unittest

from scripts.b05_anointed_native_g0_actor_v0 import ROLES, anointed_party_actor
from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, UnresolvedDecision, party_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat

ROOT = Path(__file__).resolve().parents[1]
FOCUS_DATA = {
    "AH": ("High", (6,12,18), (30,20), (3,3,3), (1,1,1), "Dagger"),
    "AM": ("Medium", (4,8,12), (24,24), (4,4,4), (1,1,1), "Dagger"),
    "AL": ("Low", (2,4,6), (20,30), (5,6,6), (1,1,3), "Sword"),
}


class AnointedG0ActorBridge(unittest.TestCase):
    def test_01_full_nine_source_profile_and_gear_matrix(self):
        self.assertEqual(set(ROLES), set(FOCUS_DATA))
        for role,(focus,vps,cost,regen,guards,weapon) in FOCUS_DATA.items():
            for lv in (1,2,3):
                with self.subTest(role=role,level=lv):
                    a=party_actor(role,lv,"anointed","party",occupied=((1,1),))
                    self.assertEqual((focus,lv),(a.focus,a.level))
                    self.assertEqual((12,12*lv,vps[lv-1]),
                                     (a.hp_max,a.vigor_max,a.vp_max))
                    self.assertEqual((30+6*(lv-1),*cost),
                                     (a.ap_total,a.physical_ap,a.projection_ap))
                    self.assertEqual((regen[lv-1],guards[lv-1]),
                                     (a.regen,a.guard_capacity))
                    self.assertEqual(13,a.guard_value)
                    self.assertEqual(weapon,a.guard_instrument)
                    self.assertEqual((a.vp_max,0,0),
                                     (a.vp_available,a.vp_committed,a.vp_spent))
                    self.assertEqual("STRUCTURAL_B05_ONLY",a.source.status)
                    self.assertEqual(role,a.source.source_id)
                    self.assertEqual(({"AH":"B05-PC-AH-DAGGER-PIERCE","AM":"B05-PC-AM-DAGGER-PIERCE","AL":"B05-PC-AL-SWORD-CUT"}[role],),a.source.attack_profiles)
                    self.assertEqual(sha256((ROOT/a.source.path).read_bytes()).hexdigest(),
                                     a.source.digest)
                    self.assertIn((weapon,"wielded"),a.source.equipment)
                    self.assertIn(("Leather armor","worn"),a.source.equipment)
                    self.assertEqual(("body",),a.footprint)
                    a.validate()

    def test_02_g0_real_regeneration_step_ap_and_vp_conservation(self):
        for role in FOCUS_DATA:
            for lv in (1,2,3):
                with self.subTest(role=role,level=lv):
                    actor=party_actor(role,lv,"hero","party",occupied=((1,1),))
                    actor.hp=9
                    e=Encounter([actor],{"hero":20},seed=0,
                        scenario="B04-B05-Anointed-G0-actor-state",
                        objective="real_native_step_not_signature_or_authority")
                    e.begin_round()
                    e.start_turn("hero",regen_choice=RegenerationChoice(hp=2))
                    self.assertEqual((11,actor.vigor_max-2),
                                     (actor.hp,actor.vigor))
                    step=[x for x in e.ledger if x["kind"]=="regeneration_step"]
                    self.assertEqual(1,len(step))
                    self.assertEqual((2,2),(step[0]["detail"]["hp_restored"],
                                             step[0]["detail"]["throughput_spent"]))
                    self.assertEqual(actor.ap_total,actor.ap_remaining)
                    self.assertEqual(12,actor.mp_remaining)
                    self.assertEqual(actor.guard_capacity,actor.guard_remaining)
                    e.spend_ap("hero","physical",label="ordinary physical action")
                    self.assertEqual(actor.ap_total-actor.physical_ap,actor.ap_remaining)
                    e.spend_vp("hero",1,mode="spent",label="ordinary VP ledger probe")
                    self.assertEqual((actor.vp_max-1,0,1),
                                     (actor.vp_available,actor.vp_committed,actor.vp_spent))
                    e.end_turn()
                    self.assertEqual(1,len([x for x in e.ledger
                                             if x["kind"]=="round_end"]))
                    self.assertFalse(any(x["kind"].startswith("anointed_signature")
                                         for x in e.ledger))
                    e.check()

    def test_03_low_l3_real_guard_reserve_and_two_physical_costs(self):
        a=party_actor("AL",3,"low","party",occupied=((1,1),))
        e=Encounter([a],{"low":20},seed=1)
        # A paid Guard needs live G1/G2 wielding, not just source equipment.
        GridMovement(e,width=6,height=6,scene_id="b05-anointed-g0-guard")
        RangedCombat(e,scene_id="b05-anointed-g2-guard")
        self.assertTrue(e.g1.genuine_anointed_weapon_ready("low"))
        e.begin_round()
        self.assertEqual(3,a.guard_remaining)
        self.assertEqual([13,13,13],[e.defense("low","guard",attack_key=f"h{n}")
                                     for n in (1,2,3)])
        with self.assertRaises(ValueError):
            e.defense("low","guard",attack_key="fourth")
        e.start_turn("low",regen_choice=RegenerationChoice())
        self.assertEqual(20,e.spend_ap("low","physical",label="first paid physical"))
        self.assertEqual(20,e.spend_ap("low","physical",label="second paid physical"))
        self.assertEqual(2,a.ap_remaining)
        with self.assertRaises(ValueError):
            e.spend_ap("low","physical",label="unsupported third")
        with self.assertRaises(ValueError):
            e.spend_ap("low","projection",label="unsupported extra projection")
        e.end_turn()
        e.check()

    def test_04_no_unsourced_aspect_signature_or_destiny_state(self):
        for role in FOCUS_DATA:
            a=party_actor(role,3,"hero","party",occupied=((0,0),))
            self.assertFalse(hasattr(a,"destiny"))
            self.assertFalse(hasattr(a,"invested_vessel"))
            self.assertFalse(hasattr(a,"anointed_signature"))
            self.assertEqual(({"AH":"B05-PC-AH-DAGGER-PIERCE","AM":"B05-PC-AM-DAGGER-PIERCE","AL":"B05-PC-AL-SWORD-CUT"}[role],),a.source.attack_profiles)
            self.assertEqual("STRUCTURAL_B05_ONLY",a.source.status)
            self.assertNotIn(("Conjure Flame","carried"),a.source.equipment)

    def test_05_invalid_role_level_source_or_occupancy_fails_closed(self):
        for role,lv in (("AH",0),("AM",4),("AL",True),("AR",3)):
            with self.subTest(role=role,level=lv),self.assertRaises(ValueError):
                anointed_party_actor(role,lv,"x","party",occupied=((1,1),))
        for actor_id,team in (("","party"),("x","")):
            with self.assertRaises(ValueError):
                anointed_party_actor("AH",1,actor_id,team,occupied=((1,1),))
        with self.assertRaises(ValueError):
            anointed_party_actor("AH",1,"x","party",occupied=())
        with self.assertRaises(ValueError):
            anointed_party_actor("AH",1,"x","party",occupied=((1,1),(2,1)))

    def test_06_original_g0_party_source_dispatch_unchanged(self):
        for role in ("A","B","R","F","H","M","S","T"):
            a=party_actor(role,1,"existing","party",occupied=((0,0),))
            self.assertNotIn(a.source.source_id,("AH","AM","AL"))
            a.validate()


if __name__=="__main__":
    unittest.main()
