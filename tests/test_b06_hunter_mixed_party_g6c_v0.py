"""B06 G6-C: 3/4-character L2/3 real-time Hunter mixed-party witnesses."""
import unittest
from unittest.mock import patch

from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_hunter_g6a_v0 import run_i3
from scripts.b06_hunter_mixed_party_g6c_v0 import (
    HUNTER_HEAD, LOCATIONS, POLICY, ROSTER, mixed_scene, run_i3_mixed,
)


def event_kinds(report,kind):
    return [x for x in report["ledger"] if x["kind"]==kind]


class G6CMixedParty(unittest.TestCase):
    def _verify(self,size,level):
        report=run_i3_mixed(size=size,level=level,seed=630+size*10+level)
        roster=("hunter",*ROSTER[:size])
        self.assertEqual(tuple(report["initiative"]),roster)
        self.assertEqual(tuple(report["turns"]),roster*2)
        self.assertEqual(report["rounds"],2)
        self.assertEqual(report["round_ends"],2)
        self.assertEqual(report["window_status"],"two_real_rounds_observed")
        self.assertEqual(report["ending"],"not_attested_full_encounter")
        self.assertFalse(report["complete_party_pack_certified"])
        self.assertIsNone(report["hunter_cr"])
        self.assertEqual(len(report["roster"]),size+1)
        self.assertEqual(report["arrow_launches"],2)
        self.assertEqual(len(event_kinds(report,"g2_bow_shot_resolved")),2)
        self.assertTrue(all(x["detail"]["outcome"]=="automatic_miss"
                            for x in event_kinds(report,"g2_bow_shot_resolved")))
        self.assertEqual(len(event_kinds(report,"g5_melee_sequence_attested")),6)
        self.assertEqual(len(event_kinds(report,"g5_melee_resolved")),6)
        self.assertEqual(len(event_kinds(report,"g6b_opportunity_resolved")),0)
        self.assertEqual(len(event_kinds(report,"g45_attested_hit")),
                         report["g45_melee_attestations"])
        self.assertEqual(len(event_kinds(report,"g4_damage_applied")),
                         report["actual_g4_damage_events"])
        self.assertEqual(report["original_report"]["current"]["round"],2)
        self.assertEqual(report["original_report"]["ending"],"unresolved")
        self.assertFalse(report["original_report"]["complete_party_pack_certified"])
        self.assertEqual(len(event_kinds(report,"regeneration_step")),2*(size+1))
        self.assertFalse(report["original_report"]["unresolved_attack_slots"])
        self.assertTrue(all(x["detail"]["ap_remaining"]>=0
                            for x in event_kinds(report,"action_committed")))
        self.assertEqual(report["attack_observations"][0]["round"],1)
        self.assertEqual(report["attack_observations"][1]["round"],2)
        self.assertIn("G2 landed-bow-hit-to-G4 physical damage and critical proof",
                      report["missing_mechanics"])
        self.assertEqual(len(event_kinds(report,"g5_terminal_exit")),0)
        return report

    def test_01_three_pc_l2_all_native_turns(self):
        self._verify(3,2)

    def test_02_three_pc_l3_all_native_turns(self):
        self._verify(3,3)

    def test_03_four_pc_l2_all_native_turns(self):
        self._verify(4,2)

    def test_04_four_pc_l3_all_native_turns(self):
        self._verify(4,3)

    def test_05_three_party_hunter_remains_conscious_no_false_death(self):
        report=self._verify(3,3)
        self.assertEqual(report["hunter_hp"],3)
        self.assertFalse(report["hunter_dead"])
        self.assertFalse(report["hunter_dying"])
        self.assertEqual(report["scholar_flame_hits"],0)
        self.assertNotIn("scholar",report["initiative"])
        self.assertFalse(event_kinds(report,"g3_flame_launched"))
        self.assertEqual(len(event_kinds(report,"g44_hunter_accepted")),1)
        self.assertEqual(len(event_kinds(report,"g4_wound_created")),0)

    def test_06_four_party_flame_creates_genuine_hunter_wound_not_victory(self):
        report=self._verify(4,3)
        self.assertEqual(report["hunter_hp"],-1)
        self.assertTrue(report["hunter_dying"])
        self.assertFalse(report["hunter_dead"])
        self.assertEqual(report["scholar_flame_hits"],2)
        self.assertEqual(len(event_kinds(report,"g4_wound_created")),1)
        wound=event_kinds(report,"g4_wound_created")[0]["detail"]
        self.assertEqual(wound["recipient"],"hunter")
        self.assertEqual(wound["location"],"Chest")
        self.assertEqual(len(event_kinds(report,"g4_basic_heal_applied")),0)
        self.assertEqual(report["g45_melee_attestations"],4)
        self.assertGreaterEqual(report["actual_g4_damage_events"],5)
        self.assertEqual(report["ending"],"not_attested_full_encounter")

    def test_07_bow_debits_real_ammo_without_phantom_damage(self):
        report=self._verify(4,2)
        launched=event_kinds(report,"g2_bow_launched")
        self.assertEqual([x["detail"]["ammo_remaining"] for x in launched],[19,18])
        self.assertEqual(len(event_kinds(report,"g2_bow_sequence_committed")),2)
        self.assertFalse(any(x["detail"].get("profile")=="Bow"
                             for x in event_kinds(report,"g4_profile_hit")))
        self.assertFalse(any(x["detail"].get("source_event","").startswith("G2:")
                             for x in event_kinds(report,"g45_attested_hit")))

    def test_08_hunter_turn_source_bite_damage_venom_regen(self):
        report=self._verify(3,3)
        bites=[x for x in event_kinds(report,"g5_melee_resolved")
               if x["detail"]["attacker"]=="hunter"]
        self.assertEqual([x["detail"]["outcome"] for x in bites],["miss","hit"])
        self.assertEqual([x["detail"]["profile"] for x in bites],
                         ["B06-AT-04"]*2)
        self.assertEqual(len(event_kinds(report,"g44_hunter_accepted")),1)
        self.assertEqual(len(event_kinds(report,"g4_profile_hit")),4)
        self.assertEqual([o["round"] for o in event_kinds(report,"round_end")],[1,2])
        hunter_regens=[e for e in event_kinds(report,"regeneration_step")
                       if e["detail"]["actor"]=="hunter"]
        self.assertEqual(len(hunter_regens),2)
        self.assertEqual(hunter_regens[1]["detail"]["hp_restored"],4)

    def test_09_source_roster_bound_to_concrete_authored_builds(self):
        combat=mixed_scene(size=4,level=3)
        e=combat.e
        self.assertEqual(tuple(e.actors),("hunter",*ROSTER))
        self.assertEqual(e.order,("hunter",*ROSTER))
        self.assertEqual(e.actors["hunter"].footprint,("head","rear"))
        self.assertEqual(e.g1.front("hunter"),LOCATIONS["vanguard"])
        self.assertEqual(e.actors["hunter"].occupied,(HUNTER_HEAD,(4,2)))
        self.assertEqual(e.actors["vanguard"].source.source_id,"A")
        self.assertEqual(e.actors["guardian"].source.source_id,"B")
        self.assertEqual(e.actors["archer"].source.source_id,"R")
        self.assertEqual(e.actors["scholar"].source.source_id,"F")
        self.assertFalse(e.g1.threatens("hunter",LOCATIONS["guardian"]))
        self.assertTrue(e.g1.melee_contact("guardian","hunter"))
        e.check()

    def test_10_invalid_rosters_are_rejected_without_partial_scenes(self):
        for size,level,seed in ((2,3,630),(5,3,630),(True,3,630),
                                (3,1,630),(3,4,630),(3,True,630),
                                (3,3,-1),(3,3,False)):
            with self.subTest(size=size,level=level,seed=seed):
                with self.assertRaises(ValueError):
                    mixed_scene(size=size,level=level,seed=seed)

    def test_11_explicit_projectile_hit_fails_closed_not_faked_damage(self):
        # G2 cannot yet resolve a bow hit into G4. The G6-C witness must
        # fail rather than quietly declare a successful encounter.
        with patch.dict(POLICY[1],{"archer":20}):
            with self.assertRaisesRegex(AssertionError,"legitimate missed"):
                run_i3_mixed(size=3,level=3)
        self.assertEqual(POLICY[1]["archer"],1)

    def test_12_melee_guard_dodge_are_charged_at_real_declaration(self):
        report=self._verify(4,3)
        defenses=event_kinds(report,"defense_assigned")
        self.assertGreaterEqual(len(defenses),6)
        self.assertEqual(defenses[0]["detail"]["actor"],"vanguard")
        self.assertEqual(defenses[0]["detail"]["defense"],"guard")
        # One real Hunter Dodge assigned against the Vanguard per round.
        hunter_dodges=[x for x in defenses if x["detail"]["actor"]=="hunter"
                        and x["detail"]["defense"]=="dodge"]
        self.assertEqual(len(hunter_dodges),2)
        self.assertEqual([x["detail"]["defense_value"] for x in hunter_dodges],
                         [14,14])
        self.assertEqual(len(event_kinds(report,"g5_melee_cancelled")),0)

    def test_13_report_copy_cannot_mutate_independent_next_run(self):
        first=run_i3_mixed(size=3,level=2,seed=631)
        twin=run_i3_mixed(size=3,level=2,seed=631)
        self.assertEqual(first,twin)
        first["attack_observations"][0]["results"]["hunter"]["outcome"]="invented"
        first["ledger"].clear()
        self.assertNotEqual(first,twin)
        self.assertEqual(twin,run_i3_mixed(size=3,level=2,seed=631))

    def test_14_legacy_g6a_single_actor_i3_still_independent(self):
        # G6-C must not replace or broaden G6-A's locked 1v1 witness.
        prior=run_i3(seed=791)
        self.assertEqual(prior["ending"],"withdrawal_attested")
        self.assertFalse(prior["complete_party_pack_certified"])
        self.assertEqual(prior["current"]["round"],2)
        self.assertEqual(prior,run_i3(seed=791))


if __name__=="__main__":
    unittest.main()
