"""G6-D source-bound Bow hit/wound proofs and mixed-party Hunter terminal."""
import unittest

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
from scripts.b06_hunter_completion_g6d_v0 import HunterCompletion, run_i3_defeat


def events(e,kind):
    return [v for v in e.ledger if v["kind"]==kind]


def shooting_scene(*,size=3,level=3):
    combat=mixed_scene(size=size,level=level,seed=641)
    e=combat.e
    for ident in ("hunter","vanguard","guardian"):
        combat.bridge.start_next_turn(RegenerationChoice())
        assert e.current==ident
        combat.bridge.end_current_turn()
    combat.bridge.start_next_turn(RegenerationChoice())
    assert e.current=="archer"
    return combat,HunterCompletion(combat)


class G6DTests(unittest.TestCase):
    def test_01_source_bow_hit_spends_only_g2_action_and_one_arrow(self):
        combat,completion=shooting_scene()
        e=combat.e
        archer=e.actors["archer"]
        hp=e.actors["hunter"].hp
        ap=archer.ap_remaining
        shot=completion.bow_hit("archer","hunter",primary_face=12,
                                damage_face=3,target_cell=(3,2))
        self.assertEqual(shot["outcome"],"hit")
        self.assertEqual(shot["critical"],"normal")
        self.assertEqual(shot["damage"]["hp_loss"],5)
        self.assertEqual(e.actors["hunter"].hp,hp-5)
        self.assertEqual(archer.ap_remaining,ap-20)
        self.assertEqual(archer.ammunition,19)
        self.assertEqual(len(events(e,"g2_bow_shot_resolved")),1)
        self.assertEqual(len(events(e,"g6d_bow_adjudicated")),1)
        self.assertEqual(len(events(e,"g4_damage_applied")),1)
        self.assertEqual(events(e,"g6d_bow_adjudicated")[0]["detail"]["action_index"],
                         shot["action_index"])
        self.assertFalse(events(e,"g45_attested_hit"))
        e.check()

    def test_02_natural_one_consumes_arrow_and_ap_no_damage(self):
        combat,completion=shooting_scene()
        e=combat.e
        result=completion.bow_hit("archer","hunter",primary_face=1,
                                  target_cell=(3,2))
        self.assertEqual(result["outcome"],"miss")
        self.assertIsNone(result["damage"])
        self.assertEqual(e.actors["hunter"].hp,14)
        self.assertEqual(e.actors["archer"].ammunition,19)
        self.assertEqual(len(events(e,"g4_damage_applied")),0)
        e.check()

    def test_03_ranged_static_take_hit_is_not_automatic_melee_hit(self):
        combat,completion=shooting_scene()
        e=combat.e
        result=completion.bow_hit("archer","hunter",primary_face=2,
                                  target_cell=(3,2))
        self.assertEqual(result["outcome"],"miss")
        self.assertEqual(result["damage"],None)
        self.assertEqual(e.actors["hunter"].hp,14)
        e.check()

    def test_04_natural_twenty_strong_critical_and_devastating(self):
        for confirm,critical,critical_dice,loss in (
                (1,"strong",(2,),2+4+2),
                (10,"critical",(1,2),2+4+3),
                (20,"devastating",(1,2),2+4+3)):
            with self.subTest(confirmation=confirm):
                combat,completion=shooting_scene()
                e=combat.e
                result=completion.bow_hit(
                    "archer","hunter",primary_face=20,
                    confirmation_face=confirm,critical_dice=critical_dice,
                    damage_face=4,target_cell=(3,2),
                    wound_location_roll=8 if critical=="devastating" else None)
                self.assertEqual(result["critical"],critical)
                self.assertEqual(result["damage"]["hp_loss"],loss)
                self.assertEqual(e.actors["hunter"].hp,14-loss)
                self.assertEqual(len(events(e,"g4_damage_applied")),1)
                e.check()

    def test_05_preflight_missing_wound_die_charges_no_resources(self):
        combat,completion=shooting_scene()
        e=combat.e
        e.actors["hunter"].hp=4
        before=(len(e.ledger),e.actors["archer"].ap_remaining,
                e.actors["archer"].ammunition)
        with self.assertRaisesRegex(UnresolvedDecision,"wound"):
            completion.bow_hit("archer","hunter",primary_face=12,
                               damage_face=3,target_cell=(3,2))
        self.assertEqual((len(e.ledger),e.actors["archer"].ap_remaining,
                          e.actors["archer"].ammunition),before)
        self.assertFalse(events(e,"g2_bow_launched"))
        e.check()

    def test_06_illegal_bow_dice_or_active_defense_preflight_atomically(self):
        choices=(
            {"primary_face":20,"confirmation_face":10,"critical_dice":(),
             "damage_face":4,"target_cell":(3,2)},
            {"primary_face":5,"damage_face":5,"target_cell":(3,2)},
            {"primary_face":12,"damage_face":3,"target_cell":(4,3)},
            {"primary_face":12,"damage_face":3,"target_cell":(3,2),
             "defense":"dodge"},
            {"primary_face":1,"damage_face":2,"target_cell":(3,2)},
        )
        for kwargs in choices:
            with self.subTest(kwargs=kwargs):
                combat,completion=shooting_scene()
                e=combat.e
                before=(len(e.ledger),e.actors["archer"].ap_remaining,
                        e.actors["archer"].ammunition)
                with self.assertRaises((ValueError,UnresolvedDecision)):
                    completion.bow_hit("archer","hunter",**kwargs)
                self.assertEqual((len(e.ledger),e.actors["archer"].ap_remaining,
                                  e.actors["archer"].ammunition),before)

    def test_07_native_same_target_sequence_lock_prevents_second_shot(self):
        combat,completion=shooting_scene()
        e=combat.e
        completion.bow_hit("archer","hunter",primary_face=1,
                           target_cell=(3,2))
        prior=len(e.ledger)
        with self.assertRaisesRegex(ValueError,"same-target"):
            completion.bow_hit("archer","hunter",primary_face=1,
                               target_cell=(3,2))
        self.assertEqual(len(e.ledger),prior)
        e.check()

    def test_08_cannot_attest_dying_hunter_as_dead(self):
        combat,completion=shooting_scene()
        e=combat.e
        e.actors["hunter"].hp=0
        before=len(e.ledger)
        with self.assertRaisesRegex(UnresolvedDecision,"actually dead"):
            completion.attest_hunter_defeat(
                "hunter",party_ids=("vanguard","guardian","archer"))
        self.assertEqual(len(e.ledger),before)

    def test_09_four_party_native_bow_lethal_in_third_real_round(self):
        report=run_i3_defeat(level=3,seed=643)
        self.assertEqual(report["terminal"]["ending"],"hunter_defeat_attested")
        self.assertEqual(report["rounds"],3)
        self.assertEqual(report["hunter_hp"],-14)
        self.assertTrue(report["hunter_dead"])
        self.assertEqual(report["finishing_shot"]["critical"],"devastating")
        self.assertTrue(report["finishing_shot"]["damage"]["dead"])
        self.assertEqual(report["finishing_shot"]["damage"]["hp_loss"],12)
        self.assertEqual(report["finishing_shot"]["ammo_remaining"],17)
        self.assertEqual(len([v for v in report["ledger"]
                              if v["kind"]=="round_end"]),3)
        self.assertEqual(len([v for v in report["ledger"]
                              if v["kind"]=="g6d_hunter_defeat_attested"]),1)
        self.assertFalse(report["complete_party_pack_certified"])
        self.assertIsNone(report["hunter_cr"])

    def test_10_four_party_l2_terminal_same_native_boundaries(self):
        report=run_i3_defeat(level=2,seed=642)
        self.assertEqual(report["terminal"]["ending"],"hunter_defeat_attested")
        self.assertEqual(report["rounds"],3)
        self.assertTrue(report["hunter_dead"])
        self.assertFalse(report["complete_party_pack_certified"])
        self.assertEqual(len([v for v in report["ledger"]
                              if v["kind"]=="g6d_bow_adjudicated"]),1)

    def test_11_terminal_report_is_deterministic(self):
        a=run_i3_defeat(seed=652)
        b=run_i3_defeat(seed=652)
        self.assertEqual(a,b)
        a["ledger"].clear()
        self.assertNotEqual(a,b)

    def test_12_terminal_is_once_only_and_rejects_false_party_roster(self):
        report=run_i3_defeat(seed=644)
        proof=[ev for ev in report["ledger"]
               if ev["kind"]=="g6d_hunter_defeat_attested"]
        self.assertEqual(len(proof),1)
        self.assertEqual(proof[0]["detail"]["party"],
                         ["vanguard","guardian","archer","scholar"])
        self.assertEqual(proof[0]["detail"]["outcome"],
                         "hunter_dead_after_actual_native_combat")


if __name__=="__main__":
    unittest.main()
