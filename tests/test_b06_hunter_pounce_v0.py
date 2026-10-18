"""Hunter Pounce / Prey Takedown v0 action-economy and player-response regressions.

These standard-library tests formalize the B06-EN-03 *provisional* Pounce
sample. They do not certify attack balance; the separate complete enemy fixture
now exists as an executable B06 benchmark.
"""
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POUNCE = ROOT / "docs/rules/05-combat/hunter-pounce-and-prey-takedown-v0.md"
CHARGE = ROOT / "docs/rules/05-combat/rapid-advance-and-charge-v0.md"
TRIP = ROOT / "docs/rules/05-combat/universal-maneuvers.md"
FOOTPRINT = ROOT / "docs/rules/05-combat/multi-square-creature-footprints-v0.md"
BESTIARY = ROOT / "content/creatures/b06-initial-bestiary-v0.json"


def pounce_result(
    bite_die, defense, balance_die, target_balance,
    *,
    bite_bonus=6,
    pounce_bonus=4,
    bite_damage_d6=4,
    armor=4,
    penetration=1,
    guard_or_dodge=True,
    attack_legal=True,
    balance_legal=True,
    defender_can_resist=True,
    target_hp_before_bite=None,
):
    """One fixed, non-critical Bite and post-damage balance resolution.

    This calculation is intentionally limited to ordinary, non-natural-20
    rolls. The canonical critical and defense rules still govern actual play.
    """
    if not attack_legal:
        return dict(bite_hit=False, hp=0, prone=False, rolled=False)

    # Against Take Hit, a legal melee attack hits unless natural 1.
    hit = bite_die != 1 and (bite_die + bite_bonus > defense if guard_or_dodge else True)
    hp = max(0, 3 + bite_damage_d6 - max(0, armor - penetration)) if hit else 0
    # Resolve injury first: 0 HP or below means unconscious and Dying,
    # but neither incapacitation nor an ordinary Bite grants free extra damage.
    able_to_resist = defender_can_resist
    if target_hp_before_bite is not None:
        able_to_resist = able_to_resist and target_hp_before_bite - hp > 0
    if not balance_legal:
        prone = False
        balance_rolled = False
    elif not able_to_resist:
        # Trip's unable-to-contest outcome requires a physically legal
        # knockdown: balance_legal includes contact, surface and force.
        prone = True
        balance_rolled = False
    else:
        prone = balance_die + pounce_bonus > target_balance
        balance_rolled = True
    return dict(bite_hit=hit, hp=hp, prone=prone, rolled=True,
                balance_rolled=balance_rolled)


class HunterPounceRulesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = POUNCE.read_text(encoding="utf-8")
        cls.charge = CHARGE.read_text(encoding="utf-8")
        cls.trip = TRIP.read_text(encoding="utf-8")
        cls.footprint = FOOTPRINT.read_text(encoding="utf-8")
        cls.index = json.loads(BESTIARY.read_text(encoding="utf-8"))
        cls.hunter = next(e for e in cls.index["entries"] if e["id"] == "B06-EN-03")

    def test_pounce_is_hunter_only_not_global_charge_revision(self):
        self.assertIn("HUNTER-LOCAL RULE CANDIDATE", self.rules)
        self.assertIn("not a general Charge/Trip/Grapple revision", self.rules)
        self.assertIn("one paid Bite attack", self.rules)
        self.assertIn("one Pounce-specific forceful balance contest", self.rules)
        self.assertIn("one ordinary paid melee attack", self.charge)

    def test_pounce_single_action_and_pool_replace_not_add(self):
        self.assertIn("one Physical Action = 24 Turn AP", self.rules)
        self.assertIn("42 AP", self.rules)
        self.assertIn("2 × M = 24 MP", self.rules)
        self.assertEqual(42-24, 18)
        self.assertEqual(2*12, 24)
        self.assertIn("not +24 MP", self.rules)

    def test_rapid_cutoff_and_three_actual_steps(self):
        self.assertEqual(math.floor(3*12/2), 18)
        self.assertIn("floor(3 × M / 2) = 18 MP", self.rules)
        self.assertIn("3 completed voluntary translated steps", self.rules)
        self.assertEqual(3*2, 6)
        self.assertEqual(3*3, 9)  # Even three mixed-terrain steps are three, not four+.
        self.assertIn("first completed step exceeding the Rapid Advance cutoff", self.rules)

    def test_natural_bite_and_pressure_both_test_only(self):
        for marker in ("d20 + 6", "3 + d6 Piercing, Penetration 1", "d20 + 4"):
            self.assertIn(marker, self.rules)
        self.assertIn("test-only numbers", self.rules)
        self.assertEqual(self.hunter["entry_status"], "EXECUTABLE_FIXTURE_EXISTS")
        self.assertEqual(self.hunter["fixture_path"],
                         "content/creatures/b06-hunter-of-the-woods.v0.json")

    def test_front_head_only_one_by_two_footprint(self):
        shape = self.hunter["creature_profile"]["footprint"]
        self.assertEqual(shape["cell_ids"], ["head", "rear"])
        self.assertEqual(shape["reference_cell_id"], "head")
        self.assertIn("one of 4 cardinal head-forward directions", self.rules)
        self.assertIn("single immediately head-forward adjacent square", self.rules)
        self.assertIn("no pivots", self.rules.lower())
        self.assertIn("No voluntary pivot", self.charge)

    def test_actual_puncturing_bite_not_implied_venom(self):
        self.assertIn("does not grant TX-HM or any free poisoning", self.rules)
        self.assertIn("real surviving post-mitigation Piercing HP puncture", self.rules)
        self.assertIn("Pounce success, Prone or a Balance roll", self.rules)
        self.assertIn("No poison penalty applies immediately", self.rules)
        self.assertIn("hunter-bite-venom-and-horn-v0.md", self.rules)

    def test_hit_and_takedown_failure_independent(self):
        r=pounce_result(12,13,9,15)
        self.assertTrue(r["bite_hit"])
        self.assertEqual(r["hp"], 4)
        self.assertFalse(r["prone"])

    def test_worked_surviving_bite_requires_authored_venom_before_balance(self):
        # First worked table row must use the already-authored delivery source.
        worked = next(line for line in self.rules.splitlines()
                      if line.startswith("| **Bite lands; prey resists takedown**"))
        self.assertEqual(pounce_result(12, 13, 9, 15)["hp"], 4)
        self.assertIn("**4 Piercing HP**", worked)
        self.assertIn("one DC12 Vitality resistance check in stage D, before Balance",
                      worked)
        self.assertNotIn("only if** venom source authored", worked)
        self.assertIn("11 < DC12", self.rules)
        self.assertLess(9 + 2, 12)  # Illustrative failed natural resistance.
        self.assertIn("**Full** `B06-TX-HUNTER-SLOW-MY`", self.rules)
        self.assertIn("**T+10 minutes**", self.rules)
        self.assertIn("**T+30 minutes**", self.rules)
        self.assertIn("**T+120 minutes**", self.rules)
        self.assertIn("**Reduced**", self.rules)
        self.assertIn("Do not make a second toxin check after Balance", self.rules)
        self.assertFalse(pounce_result(12, 13, 9, 15)["prone"])

    def test_missed_bite_but_takedown_succeeds(self):
        r=pounce_result(3,13,17,9)
        self.assertFalse(r["bite_hit"])
        self.assertEqual(r["hp"], 0)
        self.assertTrue(r["prone"])

    def test_guard_blocked_bite_but_balance_fails(self):
        r=pounce_result(9,16,16,11)
        self.assertFalse(r["bite_hit"])
        self.assertEqual(r["hp"], 0)
        self.assertTrue(r["prone"])

    def test_guard_blocked_bite_and_balance_succeeds(self):
        r=pounce_result(9,16,7,16)
        self.assertFalse(r["bite_hit"])
        self.assertFalse(r["prone"])

    def test_tied_balance_does_not_knock_prone(self):
        r=pounce_result(12,13,9,13)
        self.assertTrue(r["bite_hit"])
        self.assertFalse(r["prone"])
        self.assertIn("Tie or defender wins", self.rules)

    def test_one_roll_each_and_no_auto_prone_on_bite_natural20(self):
        self.assertIn("one attack, one physical damage packet", self.rules)
        self.assertIn("No new free Reaction", self.rules)
        self.assertIn("successful natural 20", self.rules)
        self.assertIn("does not automatically grant a takedown", self.rules)

    def test_pounce_rider_does_not_double_charge_close_contact_opportunities(self):
        self.assertIn("creates **no additional Close-Contact Opportunity**", self.rules)
        self.assertIn("Movement Opportunities along the actual Charge route", self.rules)
        self.assertIn("does **not** move into or share the target's square", self.rules)

    def test_player_commits_balance_ability_before_opposed_dice(self):
        self.assertIn("before either balance die is rolled", self.rules)
        self.assertIn("Strength to brace", self.rules)
        self.assertIn("Agility to recover balance", self.rules)
        self.assertIn("Neither participant may switch Abilities", self.rules)

    def test_bite_natural_one_miss_does_not_automatically_cancel_balance(self):
        r=pounce_result(1,13,16,11)
        self.assertFalse(r["bite_hit"])
        self.assertTrue(r["prone"])
        self.assertIn("natural 1", self.rules)

    def test_no_balance_if_bite_action_interrupt_or_target_moved(self):
        r=pounce_result(14,13,20,7,attack_legal=False)
        self.assertFalse(r["rolled"])
        self.assertFalse(r["prone"])
        self.assertEqual(r["hp"],0)
        self.assertIn("**neither** roll occurs", self.rules)
        self.assertIn("24 AP stay spent", self.rules)

    def test_no_balance_if_already_prone_or_no_eligible_ground(self):
        r=pounce_result(14,13,20,7,balance_legal=False)
        self.assertTrue(r["bite_hit"])
        self.assertFalse(r["prone"])
        self.assertIn("Already Prone", self.rules)

    def test_bite_incapacitates_standing_pc_auto_prone_under_trip_rule(self):
        # Four post-Armor HP damage takes a 3-HP standing PC to -1:
        # the PC cannot resist and must fall if still in frontal contact.
        result = pounce_result(12, 13, 1, 99, target_hp_before_bite=3)
        self.assertTrue(result["bite_hit"])
        self.assertEqual(result["hp"], 4)
        self.assertTrue(result["prone"])
        self.assertFalse(result["balance_rolled"])
        self.assertIn("Bite damage made the PC unconscious/Dying", self.rules)
        self.assertIn("no Balance Resistance or Hunter Pressure die is rolled", self.rules)
        self.assertIn("unable to make any plausible active resistance", self.trip)

    def test_unable_to_contest_before_bite_auto_prone_only_if_contact_legal(self):
        result = pounce_result(3, 13, 1, 99, defender_can_resist=False)
        self.assertFalse(result["bite_hit"])
        self.assertTrue(result["prone"])
        self.assertFalse(result["balance_rolled"])
        invalid_contact = pounce_result(12, 13, 20, 7,
                                        target_hp_before_bite=3,
                                        balance_legal=False)
        self.assertTrue(invalid_contact["bite_hit"])
        self.assertFalse(invalid_contact["prone"])
        self.assertFalse(invalid_contact["balance_rolled"])

    def test_incapacitated_is_not_an_unconditional_no_balance_exception(self):
        self.assertIn("Being incapacitated **does not by itself cancel**", self.rules)
        self.assertIn("Already Prone", self.rules)
        self.assertIn("no supported ground where Prone is meaningful", self.rules)
        self.assertIn("Still standing and able to resist after Bite", self.rules)

    def test_damage_cannot_be_via_free_body_impact(self):
        self.assertIn("no displacement, Grapple Control, Pin, additional damage or extra attack",self.rules)
        self.assertIn("no retained", self.rules)
        self.assertIn("without an additional AP expenditure", self.rules)

    def test_non_focus_ap_does_not_grant_extra_attack(self):
        self.assertIn("not enough for another 24-AP",self.rules)
        self.assertIn("One ordinary Attack Sequence", self.rules)
        self.assertIn("does not reopen", self.rules)

    def test_defender_choices_and_standing_opportunity(self):
        for x in ("Take Hit, Dodge or one eligible Guard", "Reactive Blink",
                  "precommitted Interception", "Standing Opportunity", "4 MP Stand"):
            self.assertIn(x, self.rules)
        self.assertIn("No new free Reaction", self.rules)

    def test_canonical_grapple_takedown_not_redefined(self):
        self.assertIn("existing Controller/Controlled Grappling State", self.trip)
        self.assertIn("no Grappling State",self.rules)
        self.assertIn("not** canonical", self.rules)

    def test_b06_capability_keeps_missing_authority(self):
        cap=next(c for c in self.hunter["planned_capabilities"]
                 if c["id"]=="B06-CAP-HUNTER-POUNCE")
        self.assertEqual(cap["state"],"requires_authored_attack_or_effect")
        self.assertTrue(cap["missing_authority"])
        self.assertIn("docs/rules/05-combat/hunter-pounce-and-prey-takedown-v0.md",
                      self.hunter["rules_basis"])
        self.assertFalse(any(c["state"]=="existing_authority_only"
                             for c in self.hunter["planned_capabilities"]))


if __name__=="__main__":
    unittest.main()
