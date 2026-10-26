"""Proposal-only Ward Conduit accounting: NOT a native Medium Gifted certificate."""
import unittest

from scripts.b05_medium_gifted_conduit_design_v0 import (
    MediumGiftedWardDesign, EXPRESSION, PILOT_LINKS,
)


def model(level=1, emotion="Fear"):
    m = MediumGiftedWardDesign(level)
    m.begin_turn(emotion)
    return m


class MediumGiftedWardDesignTests(unittest.TestCase):
    def test_exact_fixed_resources_and_slot_progression(self):
        for level, vp, ap, slots in ((1, 4, 30, 1), (2, 8, 36, 1),
                                     (3, 12, 42, 2)):
            with self.subTest(level=level):
                m = model(level)
                self.assertEqual((m.max_vp, m.turn_ap, m.slot_cap),
                                 (vp, ap, slots))
                self.assertEqual((m.available, m.committed, m.spent),
                                 (vp, 0, 0))
                m.check()

    def test_pilot_links_are_distinct_and_two_aspect_profiles_exact(self):
        self.assertEqual(set(EXPRESSION), {"Fear", "Trust"})
        for emotion, (pillar, aspect, _, _) in EXPRESSION.items():
            self.assertEqual(PILOT_LINKS[emotion][:2], (pillar, aspect))
        self.assertEqual(8, len({x[0] for x in PILOT_LINKS.values()}))

    def test_three_grades_commit_exact_vp_without_spending(self):
        for grade in (1, 2, 3):
            with self.subTest(grade=grade):
                m = model()
                c = m.establish(grade=grade)
                self.assertEqual((c.grade, c.status, m.available,
                                  m.committed, m.spent, m.ap),
                                 (grade, "Active", 4-grade, grade, 0, 6))
                with self.assertRaises(ValueError):
                    m.establish(grade=1)
                m.check()

    def test_grade_three_blocks_other_full_price_l1_activation(self):
        m = model()
        m.establish(grade=3)
        m.end_turn()
        m.begin_turn("Joy")
        self.assertEqual(m.conduits[0].status, "Dormant")
        before = (m.ap, m.available, m.committed, m.spent)
        with self.assertRaises(ValueError):
            m.spend_other_action(spent_vp=2)
        self.assertEqual((m.ap, m.available, m.committed, m.spent), before)
        self.assertEqual(m.conduits[0].status, "Dormant")
        m.check()

    def test_grade_one_l1_allows_one_other_two_vp_action(self):
        m = model()
        m.establish(grade=1)
        m.end_turn()
        m.begin_turn("Joy")
        m.spend_other_action(spent_vp=2)
        self.assertEqual((m.ap, m.available, m.committed, m.spent),
                         (6, 1, 1, 2))
        m.check()

    def test_fear_self_physical_hp_pulse_no_free_defense_or_resistance(self):
        m = model()
        m.establish(grade=2)
        self.assertEqual(m.pulse("first", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=5), 2)
        self.assertEqual(m.pulse("second", recipient="caster", resource="hp",
                                 damage_type="Cut", post_mitigation=5), 0)
        self.assertEqual((m.available, m.committed, m.spent), (2, 2, 0))
        self.assertEqual(m.ap, 6)
        m.check()

    def test_fear_does_not_inherit_stone_skin_fire_or_vigor_protection(self):
        m = model()
        m.establish(grade=2)
        self.assertEqual(m.pulse("fire", recipient="caster", resource="hp",
                                 damage_type="Fire", post_mitigation=5), 0)
        self.assertEqual(m.pulse("vigor", recipient="caster", resource="vigor",
                                 damage_type="Direct Vigor", post_mitigation=3), 0)
        self.assertEqual(m.pulse("physical", recipient="caster", resource="hp",
                                 damage_type="Crush", post_mitigation=5), 2)
        m.check()

    def test_trust_protects_adjacent_other_ally_vigor_once_only(self):
        m = model(emotion="Trust")
        m.establish(grade=3)
        for key, recipient, resource, adjacent in (
            ("self", "caster", "vigor", True),
            ("far", "other_ally", "vigor", False),
            ("hp", "other_ally", "hp", True),
        ):
            self.assertEqual(m.pulse(key, recipient=recipient, resource=resource,
                                     damage_type="Other", post_mitigation=8,
                                     adjacent=adjacent), 0)
        self.assertEqual(m.pulse("eligible", recipient="other_ally",
                                 resource="vigor", damage_type="Direct Vigor",
                                 post_mitigation=8, adjacent=True), 3)
        self.assertEqual(m.pulse("after", recipient="other_ally",
                                 resource="vigor", damage_type="Direct Vigor",
                                 post_mitigation=8, adjacent=True), 0)
        m.check()

    def test_unsupported_emotion_dormancy_retains_commitment(self):
        m = model(emotion="Joy")
        c = m.establish(grade=2)
        self.assertEqual(c.status, "Dormant")
        self.assertEqual(m.pulse("joy", recipient="caster", resource="hp",
                                 damage_type="Physical", post_mitigation=4), 0)
        m.end_turn()
        m.begin_turn("Fear")
        self.assertEqual((c.status, c.grade, c.anchor, m.committed),
                         ("Active", 2, "self", 2))
        m.check()

    def test_retuning_is_not_reconduction_and_window_refresh_only_once(self):
        m = model()
        c = m.establish(grade=2)
        self.assertEqual(m.pulse("fear", recipient="caster", resource="hp",
                                 damage_type="Cut", post_mitigation=6), 2)
        m.end_turn()
        m.begin_turn("Trust")
        self.assertEqual((c.status, c.grade, m.ap, m.committed, m.spent),
                         ("Active", 2, 30, 2, 0))
        self.assertEqual(m.pulse("trust", recipient="other_ally", resource="vigor",
                                 damage_type="Direct Vigor", post_mitigation=6,
                                 adjacent=True), 2)
        m.end_turn()
        m.begin_turn("Fear")
        self.assertEqual(m.pulse("fear-again", recipient="caster", resource="hp",
                                 damage_type="Physical", post_mitigation=3), 2)
        m.check()

    def test_unset_first_link_retunes_without_minting_new_window(self):
        m = model(emotion=None)
        c = m.establish(grade=1)
        self.assertEqual(c.status, "Dormant")
        window = m.window
        m.first_link("Trust")
        self.assertEqual(m.window, window)
        self.assertEqual(c.status, "Active")
        self.assertEqual(m.pulse("first", recipient="other_ally", resource="vigor",
                                 damage_type="Direct Vigor", post_mitigation=3,
                                 adjacent=True), 1)
        with self.assertRaises(ValueError):
            m.first_link("Fear")
        self.assertEqual(m.pulse("second", recipient="other_ally", resource="vigor",
                                 damage_type="Direct Vigor", post_mitigation=3,
                                 adjacent=True), 0)

    def test_l2_reconduction_pays_full_spent_and_grade_delta_atomically(self):
        m = model(level=2)
        c = m.establish(grade=1)
        m.end_turn()
        m.begin_turn("Fear")
        m.reconduct_grade(c.serial, 2)
        self.assertEqual((m.available, m.committed, m.spent, m.ap, c.grade),
                         (3, 2, 3, 12, 2))
        m.check()

    def test_reconduction_without_funds_fails_without_changes(self):
        m = model()
        c = m.establish(grade=2)
        m.end_turn()
        m.begin_turn("Fear")
        before = (m.available, m.committed, m.spent, m.ap, c.grade)
        with self.assertRaises(ValueError):
            m.reconduct_grade(c.serial, 1)
        self.assertEqual((m.available, m.committed, m.spent, m.ap, c.grade), before)
        m.check()

    def test_reconduction_does_not_refresh_same_window_pulse(self):
        m = model(level=2)
        c = m.establish(grade=1)
        m.end_turn()
        m.begin_turn("Fear")
        self.assertEqual(m.pulse("first", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=7), 1)
        m.reconduct_grade(c.serial, 2)
        self.assertEqual(m.pulse("second", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=7), 0)
        m.check()

    def test_level_three_two_conduits_cannot_stack_same_damage_event(self):
        m = model(level=3)
        c1 = m.establish(grade=3)
        m.end_turn()
        m.begin_turn("Fear")
        c2 = m.establish(grade=3)
        self.assertEqual((m.available, m.committed, m.spent), (6, 6, 0))
        self.assertEqual(m.pulse("hit1", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=9), 3)
        self.assertEqual(m.pulse("hit2", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=9), 3)
        self.assertEqual(c1.pulse_window, c2.pulse_window)
        with self.assertRaises(ValueError):
            m.pulse("hit1", recipient="caster", resource="hp",
                    damage_type="Piercing", post_mitigation=9)
        self.assertEqual(m.pulse("hit3", recipient="caster", resource="hp",
                                 damage_type="Piercing", post_mitigation=9), 0)
        m.check()

    def test_zero_packet_does_not_consume_pulse(self):
        m = model()
        m.establish(grade=1)
        self.assertEqual(m.pulse("zero", recipient="caster", resource="hp",
                                 damage_type="Cut", post_mitigation=0), 0)
        self.assertEqual(m.pulse("later", recipient="caster", resource="hp",
                                 damage_type="Cut", post_mitigation=4), 1)

    def test_no_unsourced_form_anchor_or_grade_or_extra_slot(self):
        m = model()
        for kw in ({"form": "Motion", "grade": 1},
                   {"anchor": "other_ally", "grade": 1},
                   {"grade": 0}, {"grade": 4}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):
                    m.establish(**kw)
        self.assertEqual((m.ap, m.available, m.committed), (30, 4, 0))

    def test_no_same_turn_double_establishment_or_free_24_ap_reconfiguration(self):
        m = model(level=3)
        m.establish(grade=1)
        with self.assertRaises(ValueError):
            m.establish(grade=1)
        m.end_turn()
        m.begin_turn("Fear")
        m.establish(grade=1)
        with self.assertRaises(ValueError):
            m.reconduct_grade(1, 2)
        m.check()


if __name__ == "__main__":
    unittest.main()
