"""B06-EN-03 Hunter natural Bite/Horn and delayed pursuit venom contracts.

These are deterministic *local profile* regressions, not a finalized enemy
encounter or an independent JSON Schema validation engine.
"""
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/rules/05-combat/hunter-bite-venom-and-horn-v0.md"
POUNCE = ROOT / "docs/rules/05-combat/hunter-pounce-and-prey-takedown-v0.md"
TX = ROOT / "docs/rules/05-combat/mundane-toxins-v0.md"
SHOVE = ROOT / "docs/rules/05-combat/universal-maneuvers.md"
INDEX = ROOT / "content/creatures/b06-initial-bestiary-v0.json"


def residual_pierce(d6, armor, *, penetration=1, prevention=0):
    """One normal source-authored Bite packet, with prevention AFTER armor."""
    rolled = 3 + d6
    effective_armor = max(armor - penetration, 0)
    residual = max(rolled - effective_armor, 0)
    return max(0, residual - prevention)


def venom_result(vitality_die, vitality=2, dc=12):
    """One noncritical mundane toxin natural resistance comparison."""
    return "Reduced" if vitality_die + vitality >= dc else "Full"


def stage_after_seconds(outcome, elapsed):
    """Single fixed milestone schedule from exposure, no stacking/damage."""
    if outcome == "Full":
        if elapsed >= 7200:
            return (0, 0, False)
        if elapsed >= 1800:
            return (-4, -2, True)
        if elapsed >= 600:
            return (-2, -1, True)
        return (0, 0, True)
    if outcome == "Reduced":
        if elapsed >= 3600:
            return (0, 0, False)
        if elapsed >= 600:
            return (-2, -1, True)
        return (0, 0, True)
    raise ValueError("Only one Full or Reduced outcome may be recorded")


def remaining_rounds_to_event(seconds):
    return seconds // 6


def remaining_seconds_after_round_exit(next_event_round, current_round):
    return 6 * max(0, next_event_round - current_round - 1)


def horn_drive(rear, head, target, *, obstacle=False):
    """A frontal 1×2 Shove win with the full footprint moving atomically."""
    dr = (head[0] - rear[0], head[1] - rear[1])
    if sum(abs(x) for x in dr) != 1:
        raise ValueError("Straight, cardinal 1×2 only")
    if target != (head[0] + dr[0], head[1] + dr[1]):
        raise ValueError("Target must be in head-forward adjacent cell")
    destination = (target[0] + dr[0], target[1] + dr[1])
    if obstacle:
        return rear, head, target
    return head, target, destination


class HunterBiteHornV0Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = SOURCE.read_text(encoding="utf-8")
        cls.pounce = POUNCE.read_text(encoding="utf-8")
        cls.tx = TX.read_text(encoding="utf-8")
        cls.shove = SHOVE.read_text(encoding="utf-8")
        cls.index = json.loads(INDEX.read_text(encoding="utf-8"))
        cls.hunter = next(x for x in cls.index["entries"] if x["id"] == "B06-EN-03")

    def test_authored_source_references_are_unique_and_found(self):
        self.assertIn("B06-SRC-HUNTER-GROOVED-CANINES", self.rules)
        self.assertIn("B06-SRC-HUNTER-FRONTAL-HORN", self.rules)
        self.assertIn("B06-TX-HUNTER-SLOW-MY", self.rules)
        self.assertIn("docs/rules/05-combat/hunter-bite-venom-and-horn-v0.md",
                      self.hunter["rules_basis"])

    def test_bite_uses_previous_pounce_packet_without_double_strength(self):
        self.assertIn("d20 + 6", self.rules)
        self.assertIn("3 + d6 Piercing, Pen 1", self.rules)
        self.assertIn("same natural Bite d20+6 and 3+d6 Pen1", self.rules)
        self.assertIn("do not add unestablished Strength", self.rules)
        self.assertIn("one paid Bite attack", self.pounce)

    def test_bite_damage_against_leather_brigandine_harness(self):
        self.assertEqual(residual_pierce(4, 3), 5)
        self.assertEqual(residual_pierce(4, 5), 3)
        self.assertEqual(residual_pierce(4, 7), 1)
        self.assertEqual(residual_pierce(1, 5), 0)

    def test_injection_requires_surviving_piercing_and_actual_source(self):
        self.assertEqual(residual_pierce(4, 5, prevention=3), 0)
        self.assertEqual(residual_pierce(4, 5, prevention=2), 1)
        self.assertIn("positive surviving Piercing HP packet", self.rules)
        self.assertIn("Other typed HP", self.rules)
        self.assertIn("no injection", self.rules)
        self.assertIn("a real puncture", self.tx)

    def test_bite_uses_one_action_not_one_per_cuspid(self):
        self.assertIn("24 Turn AP", self.rules)
        self.assertIn("one Bite attack", self.rules)
        self.assertIn("not two grooved-canine attacks", self.rules)
        self.assertIn("No extra free off-hand", self.rules)

    def test_venom_is_delivered_from_canines_not_horn_or_contact(self):
        self.assertIn("modified salivary gland", self.rules)
        self.assertIn("injection only", self.rules)
        self.assertIn("not horn or unarmed contact", self.rules)
        self.assertIn("No new Bite attack", self.rules)

    def test_full_and_reduced_do_not_automatically_negate_on_save(self):
        self.assertEqual(venom_result(10, 2), "Reduced")
        self.assertEqual(venom_result(9, 2), "Full")
        self.assertEqual(venom_result(1, 2), "Full")
        self.assertIn("Moderate; Vitality DC 12", self.rules)
        self.assertIn("one", self.rules)

    def test_full_slow_venom_stages_and_exact_expiry(self):
        self.assertEqual(stage_after_seconds("Full", 0), (0, 0, True))
        self.assertEqual(stage_after_seconds("Full", 599), (0, 0, True))
        self.assertEqual(stage_after_seconds("Full", 600), (-2, -1, True))
        self.assertEqual(stage_after_seconds("Full", 1799), (-2, -1, True))
        self.assertEqual(stage_after_seconds("Full", 1800), (-4, -2, True))
        self.assertEqual(stage_after_seconds("Full", 7199), (-4, -2, True))
        self.assertEqual(stage_after_seconds("Full", 7200), (0, 0, False))

    def test_reduced_slow_venom_never_escalates(self):
        self.assertEqual(stage_after_seconds("Reduced", 0), (0, 0, True))
        self.assertEqual(stage_after_seconds("Reduced", 600), (-2, -1, True))
        self.assertEqual(stage_after_seconds("Reduced", 1800), (-2, -1, True))
        self.assertEqual(stage_after_seconds("Reduced", 3599), (-2, -1, True))
        self.assertEqual(stage_after_seconds("Reduced", 3600), (0, 0, False))

    def test_venom_penalties_do_not_stack_or_target_weapon_attack(self):
        self.assertEqual(stage_after_seconds("Full", 1800), (-4, -2, True))
        self.assertIn("replaces stage 1", self.rules)
        self.assertIn("does **not** lower **Strength** itself", self.rules)
        self.assertIn("ordinary weapon Attack rolls", self.rules)
        self.assertIn("not −3 cumulatively", self.rules)

    def test_source_is_not_short_thornblood_catalogue(self):
        self.assertIn("not a copy of short", self.rules)
        self.assertIn("TX-HM", self.rules)
        self.assertIn("next **5** start-of-turn toxin ticks", self.tx)

    def test_no_immediate_effect_on_pounce_balance(self):
        self.assertEqual(stage_after_seconds("Full", 0), (0, 0, True))
        self.assertIn("No poison penalty applies immediately", self.pounce)
        self.assertIn("cannot rewrite the Balance roll of that same Pounce", self.rules)

    def test_one_instance_active_even_before_onset(self):
        self.assertTrue(stage_after_seconds("Full", 300)[2])
        self.assertIn("one active ordinary toxin instance", self.rules)
        self.assertIn("no new Vitality roll", self.rules)
        self.assertIn("T+30m/T+120m schedule remains unchanged", self.rules)

    def test_long_milestones_new_initiative_conversion(self):
        self.assertEqual([x//6 for x in (600,1800,3600,7200)],
                         [100,300,600,1200])
        self.assertIn("Round Begin R+100", self.rules)
        self.assertIn("R+300", self.rules)
        self.assertIn("R+1200", self.rules)
        self.assertIn("R+600", self.rules)

    def test_long_milestone_exploration_entry_conservative(self):
        self.assertEqual(remaining_rounds_to_event(1), 0)
        self.assertEqual(remaining_rounds_to_event(37), 6)
        self.assertEqual(remaining_rounds_to_event(600), 100)
        self.assertIn("q=floor(s/6)", self.rules)

    def test_long_milestone_combat_exit_conservative(self):
        self.assertEqual(remaining_seconds_after_round_exit(106, 104), 6)
        self.assertEqual(remaining_seconds_after_round_exit(100, 100), 0)
        self.assertIn("6×max(0,E−C−1)", self.rules)

    def test_toxin_has_no_hp_damage_vigor_recovery_or_stamina_subsystem(self):
        self.assertIn("0 direct HP, 0 direct Vigor damage", self.rules)
        self.assertIn("No six-second short toxin ticks", self.rules)
        self.assertIn("no invented new recovery checkpoints", self.rules)

    def test_horn_bash_is_defensive_crush_not_armor_piercing(self):
        self.assertIn("d20 + 5", self.rules)
        self.assertIn("2 + d6 Crush, Pen 0", self.rules)
        self.assertIn("not venomous", self.rules)
        self.assertIn("not automatically trigger Shove", self.rules)
        self.assertIn("frontal-cranial horn", self.rules)

    def test_horn_drive_is_separate_paid_shove_not_bash_rider(self):
        self.assertIn("**instead of** Horn Bash/Bite", self.rules)
        self.assertIn("No Crush damage", self.rules)
        self.assertIn("+2 Hold Ground", self.rules)
        self.assertIn("Close-Contact Opportunity", self.rules)
        self.assertIn("24 Turn AP", self.rules)

    def test_horn_drive_full_footprint_follows_canonical_shove_advance(self):
        self.assertEqual(horn_drive((0,0),(1,0),(2,0)),
                         ((1,0),(2,0),(3,0)))
        self.assertIn("old rear → old head square", self.rules)
        self.assertIn("head → vacated former PC square", self.rules)
        self.assertIn("one canonical Shove entry", self.rules)

    def test_horn_drive_blocked_target_prevents_both_movements(self):
        self.assertEqual(horn_drive((0,0),(1,0),(2,0),obstacle=True),
                         ((0,0),(1,0),(2,0)))
        self.assertIn("no one moves", self.rules)
        self.assertIn("blocked Shove rule", self.rules)

    def test_horn_drive_cannot_push_side_target_without_paid_pivot(self):
        with self.assertRaises(ValueError):
            horn_drive((0,0),(1,0),(1,1))
        self.assertIn("no sideways choice", self.rules)

    def test_horn_repeated_force_has_no_free_pounce_grapple_or_guard(self):
        self.assertIn("Horn Bash is not a Guard", self.rules)
        self.assertIn("free fear effect", self.rules)
        self.assertIn("not a free Bash rider", self.rules)

    def test_hunter_stays_concept_only_and_both_sources_are_still_uncalibrated(self):
        self.assertEqual(self.hunter["entry_status"], "CONCEPT_ONLY")
        self.assertIsNone(self.hunter["fixture_path"])
        self.assertEqual(self.hunter["encounter_guidance"]["challenge_rating"]["status"],"unrated")
        for cid in ("B06-CAP-HUNTER-BITE","B06-CAP-HUNTER-HORN"):
            cap=next(x for x in self.hunter["planned_capabilities"] if x["id"]==cid)
            self.assertEqual(cap["state"],"requires_authored_attack_or_effect")
            self.assertTrue(cap["missing_authority"])

    def test_venom_endurance_is_existing_protection_not_free_cure(self):
        self.assertIn("Venom Endurance", self.rules)
        self.assertIn("not** independently purge", self.rules)
        self.assertIn("one-instance", self.tx.lower())


if __name__ == "__main__":
    unittest.main()
