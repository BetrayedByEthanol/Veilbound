"""Bounded executable L1-3 Anointed rules receipts; not native G0/G4 certification."""
from dataclasses import replace
from pathlib import Path
import unittest

from scripts.b05_anointed_authority_l1_l3_v0 import (
    Anointed, recover_destiny, mission_event, set_bond, set_embodiment, invest,
    returning_step, kindled_flame, conjure_flame_l3, guided_regeneration_l3,
)
ROOT = Path(__file__).resolve().parents[1]


class AnointedL1L3Foundation(unittest.TestCase):
    def test_01_l1_l3_and_bond_limits(self):
        for level in (1, 2, 3):
            self.assertEqual(2, Anointed(level, "High", "Restoration").destiny)
        with self.assertRaises(ValueError): Anointed(5, "High", "Restoration")
        with self.assertRaises(ValueError): Anointed(1, "High", "Fortification")
        with self.assertRaises(ValueError): Anointed(1, "Low", "Restoration", destiny=3)
        dormant = set_bond(Anointed(1,"High","Restoration"),active=False)
        with self.assertRaises(ValueError):
            returning_step(dormant, receipt="x", target_id="ally", recipient_hp=5,
                           recipient_max_hp=12, recipient_vigor=8, ap_available=20)
        self.assertEqual(2, mission_event(dormant,"event",gm_recognized=True).destiny)
        self.assertEqual(dormant,recover_destiny(dormant,720))

    def test_02_six_hour_recovery_uses_remainder_and_cap(self):
        a=Anointed(3,"Low","Conflagration",destiny=0)
        a=recover_destiny(a,359)
        self.assertEqual((0,359),(a.destiny,a.six_hour_remainder_minutes))
        a=recover_destiny(a,1)
        self.assertEqual((1,0),(a.destiny,a.six_hour_remainder_minutes))
        a=recover_destiny(a,720)
        self.assertEqual(2,a.destiny)
        self.assertEqual(2,recover_destiny(a,6*60).destiny)
        with self.assertRaises(ValueError): recover_destiny(a,-1)
        with self.assertRaises(ValueError): recover_destiny(a,1.5)

    def test_03_gm_event_unique_not_farmable(self):
        a=Anointed(1,"High","Restoration",destiny=0)
        self.assertEqual(0,mission_event(a,"cure village",gm_recognized=False).destiny)
        a=mission_event(a,"cure village",gm_recognized=True)
        self.assertEqual(1,a.destiny)
        self.assertEqual(a,mission_event(a,"cure village",gm_recognized=True))
        a=mission_event(a,"founded hospice",gm_recognized=True)
        self.assertEqual(2,a.destiny)
        self.assertEqual(2,mission_event(a,"third",gm_recognized=True).destiny)

    def test_04_high_restoration_vigor_conversion_and_authority(self):
        actor=Anointed(1,"High","Restoration")
        n=returning_step(actor,receipt="cast1",target_id="fighter",recipient_hp=5,
             recipient_max_hp=12,recipient_vigor=20,ap_available=20,distance=3)
        self.assertEqual((2,2,20,2), (n.hp_restored,n.recipient_vigor_spent,n.ap_spent,n.actor.destiny))
        a=returning_step(n.actor,receipt="cast2",target_id="fighter",recipient_hp=7,
             recipient_max_hp=12,recipient_vigor=0,lesser=True,ap_available=20,distance=3)
        self.assertEqual((2,0,1), (a.hp_restored,a.recipient_vigor_spent,a.actor.destiny))
        with self.assertRaises(ValueError):
            returning_step(a.actor,receipt="cast2",target_id="fighter",recipient_hp=9,
                recipient_max_hp=12,recipient_vigor=8,ap_available=20)
        with self.assertRaises(ValueError):
            returning_step(actor,receipt="empty",target_id="fighter",recipient_hp=5,
                recipient_max_hp=12,recipient_vigor=0,ap_available=20)
        with self.assertRaises(ValueError):
            returning_step(actor,receipt="full",target_id="fighter",recipient_hp=12,
                recipient_max_hp=12,recipient_vigor=3,lesser=True,ap_available=20)

    def test_05_restoration_intrusion_dying_range_and_l2(self):
        actor=Anointed(1,"High","Restoration")
        base=dict(target_id="fighter",recipient_hp=5,recipient_max_hp=12,recipient_vigor=8,ap_available=20)
        with self.assertRaises(ValueError): returning_step(actor,receipt="r",distance=4,**base)
        with self.assertRaises(ValueError): returning_step(actor,receipt="r",beneficial_intrusion_legal=False,**base)
        resisted=returning_step(actor,receipt="resisted",lesser=True,
                intrusion_succeeded=False,**base)
        self.assertEqual((0,0,1,20),
                         (resisted.hp_restored,resisted.recipient_vigor_spent,
                          resisted.actor.destiny,resisted.ap_spent))
        with self.assertRaises(ValueError):
            returning_step(resisted.actor,receipt="resisted",lesser=True,**base)
        with self.assertRaises(ValueError): returning_step(actor,receipt="r",recipient_living=False,**base)
        with self.assertRaises(ValueError): returning_step(actor,receipt="r",**(base|{"recipient_hp":0}))
        with self.assertRaises(ValueError): returning_step(actor,receipt="r",path_visible=False,**base)
        self.assertEqual(2,returning_step(replace(actor,level=2),receipt="l2",distance=4,**base).hp_restored)

    def test_06_medium_and_low_restoration_genuine_step(self):
        med=Anointed(1,"Medium","Restoration")
        with self.assertRaises(ValueError): invest(med,"patient",ap_available=23,legal_vessel=True,consent_or_other_delivery_valid=True)
        med,ap=invest(med,"patient",ap_available=24,legal_vessel=True,consent_or_other_delivery_valid=True)
        self.assertEqual(24,ap)
        args=dict(target_id="patient",recipient_hp=7,recipient_max_hp=12,recipient_vigor=8,
                  authenticated_regeneration_step=True,focus_turn_id="patient:R1")
        healed=returning_step(med,receipt="patient-step1",**args)
        self.assertEqual((1,1,0),(healed.hp_restored,healed.recipient_vigor_spent,healed.ap_spent))
        with self.assertRaises(ValueError): returning_step(healed.actor,receipt="other",**args)
        with self.assertRaises(ValueError): returning_step(med,receipt="bad",**(args|{"target_id":"other"}))
        low=Anointed(1,"Low","Restoration")
        dormant_low=set_bond(low,active=False)
        reawakened=set_bond(dormant_low,active=True)
        self.assertFalse(reawakened.embodied)
        self.assertTrue(set_embodiment(reawakened,manifested=True,at_own_turn_start=True).embodied)
        with self.assertRaises(ValueError):
            set_embodiment(reawakened,manifested=True,at_own_turn_start=False)
        with self.assertRaises(ValueError): returning_step(low,receipt="n",**args)
        ok=returning_step(low,receipt="self1",target_id="self",recipient_hp=7,
                recipient_max_hp=12,recipient_vigor=8,authenticated_regeneration_step=True,
                focus_turn_id="self:R1",lesser=True)
        self.assertEqual((1,0), (ok.hp_restored,ok.recipient_vigor_spent))
        with self.assertRaises(ValueError): returning_step(ok.actor,receipt="self2",target_id="self",
               recipient_hp=8,recipient_max_hp=12,recipient_vigor=8,authenticated_regeneration_step=True,
               focus_turn_id="self:R1")

    def test_07_high_fire_hit_miss_authority_and_timing(self):
        a=Anointed(2,"High","Conflagration")
        hit=kindled_flame(a,receipt="shot1",hit=True,target_vigor=9,target_hp=8,
                          ap_available=20,distance=4,lesser=True)
        self.assertEqual((1,4,20,1),(hit.fire_hp_packet,hit.vigor_damage_packet,hit.ap_spent,hit.actor.destiny))
        missed=kindled_flame(hit.actor,receipt="shot2",hit=False,target_vigor=9,target_hp=8,
                             ap_available=20,lesser=True)
        self.assertEqual((0,0,0),(missed.fire_hp_packet,missed.vigor_damage_packet,missed.actor.destiny))
        with self.assertRaises(ValueError): kindled_flame(a,receipt="bad",hit=True,target_vigor=8,
                                                          target_hp=7,ap_available=19)
        with self.assertRaises(ValueError): kindled_flame(replace(a,level=1),receipt="bad",hit=True,
                                                          target_vigor=8,target_hp=7,ap_available=20,distance=4)
        deflected=kindled_flame(a,receipt="def",hit=True,target_vigor=0,target_hp=1,
                                fire_resistance=5,ap_available=20)
        self.assertEqual((0,0,False),(deflected.fire_hp_packet,deflected.vigor_damage_packet,
                                      deflected.requires_native_dying_bridge))
        lethal=kindled_flame(a,receipt="lethal",hit=True,target_vigor=0,target_hp=1,ap_available=20)
        self.assertTrue(lethal.requires_native_dying_bridge)

    def test_08_medium_low_flame_one_per_turn_no_free_carrier(self):
        medium=Anointed(3,"Medium","Conflagration")
        medium,_=invest(medium,"w1",ap_available=42,legal_vessel=True,consent_or_other_delivery_valid=True)
        args=dict(hit=True,target_hp=12,target_vigor=36,carrier_attack_authentic=True,carrier_attack_on_own_turn=True,turn_id="own:R1",
                  invested_weapon_id="w1",active_wielded_weapon_id="w1")
        x=kindled_flame(medium,receipt="w1-hit",**args)
        self.assertEqual(1,x.vigor_damage_packet)
        with self.assertRaises(ValueError):
            kindled_flame(medium,receipt="offturn",**(args|{"carrier_attack_on_own_turn":False}))
        with self.assertRaises(ValueError): kindled_flame(x.actor,receipt="w2-hit",**args)
        with self.assertRaises(ValueError): kindled_flame(medium,receipt="w3-hit",**(args|{"carrier_attack_authentic":False}))
        low=Anointed(3,"Low","Conflagration")
        k=kindled_flame(low,receipt="swing",hit=True,target_hp=12,target_vigor=9,
                        carrier_attack_authentic=True,carrier_attack_on_own_turn=True,turn_id="own:R1",active_wielded_weapon_id="sword",lesser=True)
        self.assertEqual((4,1), (k.vigor_damage_packet,k.actor.destiny))
        with self.assertRaises(ValueError):
            kindled_flame(low,receipt="offturn",hit=True,target_hp=12,target_vigor=9,
                carrier_attack_authentic=True,carrier_attack_on_own_turn=False,
                turn_id="reaction:R1",active_wielded_weapon_id="sword")
        with self.assertRaises(ValueError): kindled_flame(k.actor,receipt="swing2",hit=True,
                  target_hp=12,target_vigor=9,carrier_attack_authentic=True,carrier_attack_on_own_turn=True,
                  turn_id="own:R1",active_wielded_weapon_id="sword")

    def test_09_l3_conjure_exact_profile_and_payment(self):
        high=Anointed(3,"High","Conflagration")
        out=conjure_flame_l3(high,receipt="paid",profile="Thrown Projectile",used_tier=2,
                            hit=True,target_vigor_after_base=6,adequate_spent_vp=True,
                            authentic_paid_attack=True)
        self.assertEqual((3,4,1),(out.additional_vigor_damage,out.spent_vp_this_attempt,out.actor.destiny))
        with self.assertRaises(ValueError): conjure_flame_l3(high,receipt="bad",profile="Ammunition Shot",
                          used_tier=2,hit=True,target_vigor_after_base=5,adequate_spent_vp=True,
                          authentic_paid_attack=True)
        with self.assertRaises(ValueError): conjure_flame_l3(high,receipt="bad",profile="Thrown Projectile",
                          used_tier=3,hit=True,target_vigor_after_base=5,adequate_spent_vp=True,
                          authentic_paid_attack=True)
        with self.assertRaises(ValueError): conjure_flame_l3(high,receipt="not-paid",profile="Thrown Projectile",
                          used_tier=2,hit=True,target_vigor_after_base=5,adequate_spent_vp=True,
                          authentic_paid_attack=False)
        # A caller-supplied "matches" flag cannot substitute for an active Vessel.
        uninvested=Anointed(3,"Medium","Conflagration")
        with self.assertRaises(ValueError):
            conjure_flame_l3(uninvested,receipt="no-invest",profile="Weapon Enchantment",
                 used_tier=1,hit=True,target_vigor_after_base=9,active_reserve=True,
                 reserved_vp=4,vessel_weapon_matches=True,weapon_wielded=True,
                 authentic_paid_attack=True)
        med=Anointed(3,"Medium","Conflagration",invested_vessel="weapon")
        w=conjure_flame_l3(med,receipt="paid-w",profile="Weapon Enchantment",used_tier=1,
                           hit=False,target_vigor_after_base=36,active_reserve=True,reserved_vp=4,
                           vessel_weapon_matches=True,weapon_wielded=True,authentic_paid_attack=True)
        self.assertEqual((0,0,4,1),(w.additional_vigor_damage,w.spent_vp_this_attempt,
                                      w.required_existing_committed_vp,w.actor.destiny))
        with self.assertRaises(ValueError): conjure_flame_l3(med,receipt="bad",profile="Weapon Enchantment",
                           used_tier=1,hit=True,target_vigor_after_base=9,active_reserve=True,reserved_vp=4,
                           vessel_weapon_matches=False,weapon_wielded=True,authentic_paid_attack=True)
        with self.assertRaises(ValueError): conjure_flame_l3(med,receipt="not-reserved",profile="Weapon Enchantment",
                           used_tier=1,hit=True,target_vigor_after_base=9,active_reserve=False,reserved_vp=0,
                           vessel_weapon_matches=True,weapon_wielded=True,authentic_paid_attack=True)

    def test_10_guided_regeneration_one_hp_only_and_refusal(self):
        high=Anointed(3,"High","Restoration")
        args=dict(receipt="step1",recipient_missing_hp_after_ordinary=2,
                  active_paid_guided_instance=True,mode="Maintained",profile="Single Target",
                  authenticated_regeneration_step=True,guided_bonus_unsuppressed=True)
        x=guided_regeneration_l3(high,**args)
        self.assertEqual((1,1),(x.additional_hp_without_vigor,x.actor.destiny))
        with self.assertRaises(ValueError): guided_regeneration_l3(x.actor,**args)
        with self.assertRaises(ValueError): guided_regeneration_l3(high,**(args|{"recipient_missing_hp_after_ordinary":0}))
        with self.assertRaises(ValueError): guided_regeneration_l3(high,**(args|{"recipient_dying":True}))
        with self.assertRaises(ValueError): guided_regeneration_l3(high,**(args|{"active_paid_guided_instance":False}))
        with self.assertRaises(ValueError): guided_regeneration_l3(high,**(args|{"guided_bonus_unsuppressed":False}))
        med=Anointed(3,"Medium","Restoration",invested_vessel="patient")
        with self.assertRaises(ValueError): guided_regeneration_l3(med,**args)
        with self.assertRaises(ValueError):
            guided_regeneration_l3(Anointed(3,"Medium","Restoration"),
                                   **(args|{"vessel_matches":True}))
        self.assertEqual(1,guided_regeneration_l3(med,
                         **(args|{"vessel_matches":True})).additional_hp_without_vigor)
        low=Anointed(3,"Low","Restoration")
        with self.assertRaises(ValueError): guided_regeneration_l3(low,**args)
        self.assertEqual(1,guided_regeneration_l3(low,**(args|{"profile":"Self","recipient_self":True})).additional_hp_without_vigor)
        with self.assertRaises(ValueError):
            guided_regeneration_l3(replace(low,embodied=False),**(args|{"profile":"Self","recipient_self":True}))

    def test_11_ledger_no_same_receipt_cross_effect_and_no_implicit_grades(self):
        a=Anointed(3,"High","Conflagration")
        first=kindled_flame(a,receipt="one",hit=True,target_hp=7,target_vigor=8,ap_available=20)
        with self.assertRaises(ValueError): conjure_flame_l3(first.actor,receipt="one",
                profile="Thrown Projectile",used_tier=1,hit=True,target_vigor_after_base=5,
                adequate_spent_vp=True,authentic_paid_attack=True)
        with self.assertRaises(TypeError): kindled_flame(a,receipt="i",hit=True,target_hp=5,
                 target_vigor=5,ap_available=20,grade="greater")

    def test_12_canonical_rule_contract_and_readiness(self):
        docs=["docs/rules/08-archetypes/anointed.md",
              "docs/rules/08-archetypes/anointed-signature-authority-l1-3-v0.md",
              "docs/rules/08-archetypes/README.md",
              "docs/rules/07-veil-magic/conjure-flame-v0.md",
              "docs/rules/07-veil-magic/guided-regeneration-v0.md",
              "docs/design/veilbound-roadmap-and-mvp-readiness.md"]
        text="\n".join((ROOT/p).read_text(encoding="utf-8") for p in docs)
        self.assertIn("anointed-signature-authority-l1-3-v0.md",
                      (ROOT/"docs/rules/08-archetypes/anointed.md").read_text(encoding="utf-8"))
        self.assertIn("Anointed Level-3 Lesser Authority compatibility",
                      (ROOT/"docs/rules/07-veil-magic/conjure-flame-v0.md").read_text(encoding="utf-8"))
        self.assertIn("Anointed Level-3 Lesser Authority compatibility",
                      (ROOT/"docs/rules/07-veil-magic/guided-regeneration-v0.md").read_text(encoding="utf-8"))
        for needle in ("Maximum Destiny = 2", "Meaningful Mission Event", "Spare the Reserve",
                       "Consuming Flame", "single", "L1–3", "1 Fire HP", "+3 Vigor",
                       "0-VP", "0/12", "9/12", "L3", "Sovereign Projection"):
            self.assertIn(needle,text)


if __name__=="__main__":
    unittest.main()
