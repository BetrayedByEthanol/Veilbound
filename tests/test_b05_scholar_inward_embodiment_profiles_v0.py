"""B05 Scholar configuration profile model regressions (not G0 build certificates)."""
import unittest

from scripts.b05_scholar_inward_embodiment_profiles_v0 import (
    PROFILES, MEDIUM, LOW, TECHNIQUE_NAMES, KNOWN_CAP, PREPARED_CAP,
    ScholarConfigurationLedger, committed_cost,
)

BOTH = ("Stone Skin", "Guided Regeneration")


def medium(level=1, va=0, known=BOTH):
    return ScholarConfigurationLedger(
        focus="Medium", level=level, veil_affinity=va, known=known)


def low(level=1, va=0, known=BOTH, prepared=BOTH):
    return ScholarConfigurationLedger(
        focus="Low", level=level, veil_affinity=va,
        known=known, prepared=prepared)


class ScholarInwardEmbodimentProfilesTests(unittest.TestCase):
    def test_01_distinct_profiles_and_explicit_compatibility(self):
        self.assertEqual(set(PROFILES), set(MEDIUM + LOW))
        self.assertEqual(TECHNIQUE_NAMES, set(BOTH))
        self.assertEqual({PROFILES[x].mode for x in MEDIUM}, {"Inward"})
        self.assertEqual({PROFILES[x].mode for x in LOW}, {"Embodiment"})
        self.assertEqual({PROFILES[x].channel for x in MEDIUM}, {"Body", "Regeneration"})
        self.assertEqual({PROFILES[x].channel for x in LOW}, {"Body", "Regeneration"})
        self.assertEqual(KNOWN_CAP["Medium"], (4, 5, 5))
        self.assertEqual(KNOWN_CAP["Low"], (3, 4, 4))
        self.assertEqual(PREPARED_CAP, (2, 3, 3))

    def test_02_level_one_m_inward_base_and_reroute_exact_vp(self):
        m = medium()
        self.assertEqual(m.max_vp, 4)
        m.begin_turn()
        m.activate(MEDIUM[0])
        self.assertEqual(m.snapshot()["ap_remaining"], 6)
        self.assertEqual((m.vp_available, m.vp_committed, m.vp_spent), (3, 1, 0))
        m.reroute(MEDIUM[1])
        self.assertEqual((m.vp_available, m.vp_committed, m.vp_spent), (0, 1, 3))
        self.assertEqual(m.snapshot()["ap_remaining"], 6)
        self.assertEqual(m.model_effect()["regen_bonus"], 1)
        m.release()
        self.assertEqual((m.vp_available, m.vp_committed, m.vp_spent), (1, 0, 3))
        with self.assertRaises(ValueError):
            m.activate(MEDIUM[0])  # insufficient 24 AP, no free new spell

    def test_03_medium_reroute_has_no_free_refund_or_invalid_same_refresh(self):
        m = medium(level=2)
        m.begin_turn()
        m.activate(MEDIUM[0])
        before = m.snapshot()
        with self.assertRaises(ValueError):
            m.reroute(MEDIUM[0])
        self.assertEqual(m.snapshot(), before)
        m.reroute(MEDIUM[1])
        self.assertEqual((m.vp_available, m.vp_committed, m.vp_spent), (4, 1, 3))
        m.reroute(MEDIUM[0])
        self.assertEqual((m.vp_available, m.vp_committed, m.vp_spent), (1, 1, 6))
        self.assertEqual(m.snapshot()["ap_remaining"], 12)

    def test_04_medium_reroute_preflight_is_atomic_on_insufficient_vp(self):
        m = medium()
        m.begin_turn()
        m.activate(MEDIUM[0])
        m.reroute(MEDIUM[1])
        before = m.snapshot()
        with self.assertRaises(ValueError):
            m.reroute(MEDIUM[0])
        self.assertEqual(m.snapshot(), before)

    def test_05_medium_l3_overroute_tradeoff_and_payment(self):
        m = medium(level=3)
        m.begin_turn()
        m.activate(MEDIUM[0])
        m.overroute(2)
        self.assertEqual(m.model_effect(), {
            "resistance": 3, "regen_bonus": 0, "movement_cap": 2})
        self.assertEqual(m.vp_spent, 2)
        before = m.snapshot()
        m.overroute(2)
        self.assertEqual(m.snapshot(), before)
        m.overroute(0)
        self.assertEqual(m.model_effect()["resistance"], 1)
        self.assertEqual(m.vp_spent, 2)  # no refund of earlier Spent VP
        m.overroute(1)
        self.assertEqual(m.vp_spent, 3)
        m.reroute(MEDIUM[1], overroute_steps=2)
        self.assertEqual(m.vp_spent, 7)  # L3 2 reroute +2 overroute
        self.assertEqual(m.model_effect(), {
            "resistance": 0, "regen_bonus": 3, "movement_cap": 2})
        self.assertEqual(m.vp_committed, 1)

    def test_06_no_l1_overrouting_and_no_direct_cast_bypass(self):
        m = medium()
        m.begin_turn()
        m.activate(MEDIUM[0])
        with self.assertRaises(ValueError):
            m.overroute(1)
        with self.assertRaises(ValueError):
            m.reroute(MEDIUM[1], overroute_steps=1)
        with self.assertRaises(ValueError):
            m.activate(MEDIUM[1])

    def test_07_low_stone_source_reserve_not_discounted(self):
        for lv in (1, 2, 3):
            a = low(level=lv)
            a.begin_turn()
            a.activate(LOW[0])
            self.assertEqual(a.vp_committed, committed_cost(PROFILES[LOW[0]], a.max_vp))
            self.assertEqual(a.vp_committed, (a.max_vp + 2)//3)
            self.assertEqual(a.model_effect(veil_control=0)["resistance"], 2)
            self.assertEqual(a.ap_remaining, 30 + 6*(lv-1)-30)
            a.check()

    def test_08_low_guided_requires_two_committed_and_real_step_for_hp(self):
        a = low()
        a.begin_turn()
        a.activate(LOW[1])
        self.assertEqual((a.vp_available, a.vp_committed, a.vp_spent), (0, 2, 0))
        self.assertEqual(a.model_effect()["regen_bonus"], 1)
        self.assertFalse(a.consume_next_guided_step_marker())
        with self.assertRaises(ValueError):
            a.intensify()
        a.end_turn()

    def test_09_low_cannot_instantly_switch_or_reroute(self):
        a = low(level=2)
        a.begin_turn()
        a.activate(LOW[0])
        before = a.snapshot()
        with self.assertRaises(ValueError):
            a.activate(LOW[1])
        with self.assertRaises(ValueError):
            a.reroute(LOW[1])
        self.assertEqual(a.snapshot(), before)
        a.release()
        with self.assertRaises(ValueError):
            a.activate(LOW[1])  # own-turn has only 36 AP, spent 30
        a.end_turn()
        a.begin_turn()
        a.activate(LOW[1])
        self.assertEqual(a.vp_spent, 0)
        self.assertEqual(a.vp_committed, 2)

    def test_10_low_l3_stone_intensification_expiry_and_debit(self):
        a = low(level=3)
        a.begin_turn()
        a.activate(LOW[0])
        a.intensify()
        self.assertEqual(a.model_effect(veil_control=0)["resistance"], 3)
        self.assertEqual(a.vp_spent, 1)
        with self.assertRaises(ValueError):
            a.intensify()
        a.end_turn()
        a.begin_turn()
        self.assertEqual(a.model_effect(veil_control=0)["resistance"], 2)
        self.assertEqual(a.vp_spent, 1)
        self.assertFalse(a.snapshot()["intensified"])

    def test_11_low_l3_guided_next_step_marker_only(self):
        a = low(level=3)
        a.begin_turn()
        a.activate(LOW[1])
        a.intensify()
        self.assertEqual(a.model_effect()["regen_bonus"], 2)
        a.end_turn()
        self.assertEqual(a.model_effect()["regen_bonus"], 2)
        self.assertTrue(a.consume_next_guided_step_marker())
        self.assertEqual(a.model_effect()["regen_bonus"], 1)
        self.assertFalse(a.consume_next_guided_step_marker())
        self.assertEqual(a.vp_spent, 1)

    def test_12_low_l1_prepared_subset_is_real_limit(self):
        a = low(prepared=("Stone Skin",))
        a.begin_turn()
        with self.assertRaises(ValueError):
            a.activate(LOW[1])
        a.activate(LOW[0])
        self.assertEqual(a.vp_committed, 1)
        for wrong in ({"focus":"Low","level":1,"veil_affinity":0,
                       "known":BOTH,"prepared":("Stone Skin", "Stone Skin")},
                      {"focus":"Low","level":1,"veil_affinity":0,
                       "known":("Stone Skin",),"prepared":BOTH}):
            with self.assertRaises(ValueError):
                ScholarConfigurationLedger(**wrong)

    def test_13_reject_cross_focus_and_unknown_spell_creation(self):
        m = medium()
        m.begin_turn()
        with self.assertRaises(ValueError):
            m.activate(LOW[0])
        with self.assertRaises(ValueError):
            m.activate("STONE-SKIN-ORDINARY-SELF")
        for known in (("Stone Skin", "Stone Skin"), ("Unknown Spell",)):
            with self.assertRaises(ValueError):
                medium(known=known)
        a = low()
        a.begin_turn()
        with self.assertRaises(ValueError):
            a.activate(MEDIUM[0])

    def test_14_reject_wrong_levels_affinity_and_overflows(self):
        for focus in ("Medium", "Low"):
            for lv in (0, True, 4):
                with self.assertRaises(ValueError):
                    ScholarConfigurationLedger(focus=focus, level=lv,
                                               veil_affinity=0, known=BOTH)
        for bad in (-3, 5, True):
            with self.assertRaises(ValueError):
                medium(va=bad)
        with self.assertRaises(ValueError):
            low(prepared=BOTH + ("Stone Skin",))
        with self.assertRaises(ValueError):
            ScholarConfigurationLedger(focus="High", level=1,
                                       veil_affinity=0, known=BOTH)

    def test_15_no_hidden_actions_between_turns(self):
        a = low()
        with self.assertRaises(ValueError):
            a.activate(LOW[0])
        a.begin_turn()
        with self.assertRaises(ValueError):
            a.begin_turn()
        a.activate(LOW[0])
        a.end_turn()
        before = a.snapshot()
        for operation in (lambda: a.release(), lambda: a.activate(LOW[1])):
            with self.assertRaises(ValueError):
                operation()
        self.assertEqual(a.snapshot(), before)

    def test_16_vp_preserved_across_l1_l2_l3(self):
        for focus in ("Medium", "Low"):
            for lv in (1,2,3):
                a = (medium(level=lv) if focus=="Medium" else low(level=lv))
                a.begin_turn()
                a.activate((MEDIUM if focus=="Medium" else LOW)[0])
                a.check()
                a.release()
                self.assertEqual(a.vp_available, a.max_vp)
                self.assertEqual(a.vp_committed, 0)
                self.assertEqual(a.vp_spent, 0)

    def test_17_pure_model_no_combat_certificate(self):
        a = medium(level=3)
        self.assertFalse(hasattr(a, "attack"))
        self.assertFalse(hasattr(a, "damage"))
        self.assertFalse(hasattr(a, "apply_hp"))
        self.assertFalse(hasattr(a, "certify_build"))


if __name__ == "__main__":
    unittest.main()
