"""B04/B05 authentic Anointed normal G5 Dagger/Sword offense and negative gates."""
from copy import deepcopy
from dataclasses import replace
import unittest

from scripts.b05_anointed_native_melee_v0 import (
    MELEE_IDS,anointed_weapon_profile,
)
from scripts.b05_anointed_native_g5_offense_v0 import (
    FOCUSES,LEVELS,OPPONENTS,POLICIES,run_matrix,run_policy,attest_policy,
)
from scripts.b06_encounter_state_v0 import (
    Encounter,RegenerationChoice,UnresolvedDecision,party_actor,enemy_actor,
)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_ranged_v0 import RangedCombat
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest


def rows(report,kind):
    return [v for v in report["ledger"] if v["kind"]==kind]


def scene(role="AL",level=3,*,g2=True):
    hero=party_actor(role,level,"anointed","party",occupied=((2,2),))
    foe=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    e=Encounter([hero,foe],{"anointed":40,"foe":30},seed=0,
                scenario="B05-Anointed-Physical-Negative-Gates",
                objective="source_legal_melee_no_free_magical_packet")
    GridMovement(e,width=7,height=6,scene_id="anointed-g5-test")
    if g2:
        RangedCombat(e,scene_id="anointed-g2-test")
    SpellState(e)
    DamageState(e)
    combat=SourceMelee(e)
    e.begin_round()
    combat.bridge.start_next_turn(RegenerationChoice())
    return combat


class AnointedNativeMeleeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports=run_matrix(seed=0)
        cls.lookup={(r["focus"],r["level"],r["opponent"],r["policy"]):r
                    for r in cls.reports}

    def test_01_exact_thirty_six_real_source_policy_cases(self):
        self.assertEqual(36,len(self.reports))
        self.assertEqual(36,len(self.lookup))
        self.assertEqual(36,len(FOCUSES)*len(LEVELS)*len(OPPONENTS)*len(POLICIES))
        for r in self.reports:
            self.assertFalse(r["independent_focus_certified"])
            self.assertFalse(r["representative_play_certified"])
            self.assertIsNone(r["sampled_win_rate"])
            self.assertFalse(r["metrics"]["native_signature_or_authority_spent"])

    def test_02_three_real_sourced_melee_profiles_and_correct_dice(self):
        for r in self.reports:
            with self.subTest(r=(r["focus"],r["level"],r["opponent"],r["policy"])):
                role=FOCUSES[r["focus"]]
                m=r["metrics"]
                self.assertEqual(MELEE_IDS[role],m["player_attack_profile"])
                self.assertEqual(3,m["player_attack_bonus"])
                self.assertEqual("d6" if role=="AL" else "d4",
                                 m["player_weapon_damage_die"])
                self.assertTrue(m["source_weapon_still_wielded"])
                self.assertEqual(role,r["source_ids"]["anointed"])
                self.assertEqual({"soldier":"B06-EN-02",
                                  "sentry_prepared":"B06-EN-01"}[r["opponent"]],
                                 r["source_ids"]["foe"])
                self.assertEqual(1,m["enemy_g5_hits"])
                self.assertEqual(1,m["enemy_g4_damage_events"])
                self.assertEqual(1,m["recipient_regeneration_steps"])

    def test_03_one_paid_g0_physical_sequence_binds_exact_g5_g4(self):
        for r in self.reports:
            m=r["metrics"]
            count=int(r["policy"]=="strike")
            self.assertEqual((count,count,count),
                             (m["player_g0_paid_physical_actions"],
                              m["player_g5_hits"],m["player_g4_damage_events"]))
            seq=[x for x in rows(r,"g5_melee_sequence_attested")
                 if x["detail"]["attacker"]=="anointed"]
            self.assertEqual(count,len(seq))
            if count:
                paid=[x for x in rows(r,"action_committed")
                      if x["detail"]["actor"]=="anointed"]
                roll=[x for x in rows(r,"g5_melee_roll")
                      if x["detail"]["attacker"]=="anointed"]
                hits=[x for x in rows(r,"g5_melee_resolved")
                      if x["detail"]["attacker"]=="anointed"]
                g45=[x for x in rows(r,"g45_attested_hit")
                      if x["detail"]["attacker"]=="anointed"]
                self.assertEqual((1,1,1,1),(len(paid),len(roll),len(hits),len(g45)))
                self.assertEqual([paid[0]["index"]],seq[0]["detail"]["action_indices"])
                self.assertEqual(paid[0]["index"],g45[0]["detail"]["action_index"])
                self.assertEqual(roll[0]["detail"]["profile"],m["player_attack_profile"])
                self.assertEqual(r["source_digests"]["anointed"],
                                 seq[0]["detail"]["source_digest"])
                self.assertEqual(r["source_digests"]["anointed"],
                                 g45[0]["detail"]["attacker_source"])
                self.assertEqual({"High":30,"Medium":24,"Low":20}[r["focus"]],
                                 paid[0]["detail"]["ap_spent"])

    def test_04_ordinary_damage_matches_sword_penetration_and_dagger_armor(self):
        for focus in FOCUSES:
            for lv in LEVELS:
                for opponent in OPPONENTS:
                    base=self.lookup[focus,lv,opponent,"hold"]["metrics"]
                    strike=self.lookup[focus,lv,opponent,"strike"]["metrics"]
                    expected=(
                        4 if opponent=="soldier" else 6
                    ) if focus=="Low" else (
                        1 if opponent=="soldier" else 3)
                    with self.subTest(focus=focus,lv=lv,foe=opponent):
                        self.assertEqual(base["enemy_hp"]-expected,strike["enemy_hp"])
                        self.assertEqual(base["enemy_vigor"],strike["enemy_vigor"])
                        self.assertEqual(base["anointed_hp"],strike["anointed_hp"])
                        self.assertEqual(base["anointed_vigor"],strike["anointed_vigor"])
                        self.assertEqual(1,strike["player_g5_hits"])
                        self.assertEqual(0,base["player_g5_hits"])

    def test_05_no_g2_does_not_grant_g1_threat_or_g5_attack(self):
        for role in MELEE_IDS:
            combat=scene(role,g2=False)
            e=combat.e
            a=e.actors["anointed"]
            self.assertEqual((MELEE_IDS[role],),a.source.attack_profiles)
            self.assertFalse(e.g1.melee_contact("anointed","foe"))
            before=(a.ap_remaining,len(e.ledger))
            with self.assertRaises(UnresolvedDecision):
                combat.declare("anointed","foe",profiles=(MELEE_IDS[role],),
                               defenses=("take_hit",))
            self.assertEqual(before,(a.ap_remaining,len(e.ledger)))
            self.assertFalse(any(x["kind"]=="action_committed" for x in e.ledger))

    def test_06_lost_g2_wielding_rejects_before_any_attack_payment(self):
        for role in MELEE_IDS:
            combat=scene(role)
            e=combat.e
            a=e.actors["anointed"]
            e.g2.wielded[a.id].clear()
            self.assertFalse(e.g1.melee_contact("anointed","foe"))
            before=(a.ap_remaining,len(e.ledger))
            with self.assertRaises(UnresolvedDecision):
                combat.declare("anointed","foe",profiles=(MELEE_IDS[role],),
                               defenses=("take_hit",))
            self.assertEqual(before,(a.ap_remaining,len(e.ledger)))

    def test_07_forged_sha_or_wrong_profile_cannot_claim_g5_damage(self):
        for role in MELEE_IDS:
            combat=scene(role)
            e=combat.e
            a=e.actors["anointed"]
            original=a.source
            wrong="B05-PC-AL-SWORD-CUT" if role!="AL" else "B05-PC-AH-DAGGER-PIERCE"
            with self.assertRaises(UnresolvedDecision):
                combat.declare("anointed","foe",profiles=(wrong,),
                               defenses=("take_hit",))
            a.source=replace(original,digest="0"*64)
            with self.assertRaises(UnresolvedDecision):
                anointed_weapon_profile(a,MELEE_IDS[role],encounter=e)
            a.source=original
            self.assertTrue(e.g1.melee_contact("anointed","foe"))
            self.assertFalse(any(x["kind"]=="action_committed" for x in e.ledger))

    def test_08_dagger_rejects_d6_face_after_g0_payment_without_false_hit(self):
        for role in ("AH","AM"):
            combat=scene(role)
            e=combat.e
            seq=combat.declare("anointed","foe",profiles=(MELEE_IDS[role],),
                               defenses=("take_hit",))
            before=e.actors["foe"].hp
            with self.assertRaises(ValueError):
                combat.resolve(seq,0,attack_face=12,damage_face=5)
            self.assertEqual(before,e.actors["foe"].hp)
            self.assertFalse(any(x["kind"]=="g4_damage_applied" for x in e.ledger))
            self.assertFalse(any(x["kind"]=="g5_melee_roll" for x in e.ledger))
            legal=combat.resolve(seq,0,attack_face=12,damage_face=4)
            self.assertEqual("hit",legal["outcome"])
            self.assertEqual(1,len([x for x in e.ledger
                                    if x["kind"]=="g5_melee_resolved"]))
            with self.assertRaises(ValueError):
                combat.resolve(seq,0,attack_face=12,damage_face=4)

    def test_09_exact_report_replay_rejects_forged_and_rehashed_receipts(self):
        for focus in FOCUSES:
            r=self.lookup[focus,3,"sentry_prepared","strike"]
            self.assertEqual(r,attest_policy(r,focus=focus,level=3,
                                             opponent="sentry_prepared",policy="strike"))
        r=deepcopy(self.lookup["Medium",2,"soldier","strike"])
        r["metrics"]["enemy_hp"]+=1
        with self.assertRaises(AssertionError):
            attest_policy(r,focus="Medium",level=2,opponent="soldier")
        r=deepcopy(self.lookup["Low",3,"soldier","strike"])
        x=next(e for e in rows(r,"g5_melee_roll")
               if e["detail"]["attacker"]=="anointed")
        x["detail"]["attack_bonus"]+=2
        r["ledger_sha256"]=canonical_digest(r["ledger"])
        with self.assertRaises(AssertionError):
            attest_policy(r,focus="Low",level=3,opponent="soldier")

    def test_10_invalid_source_policy_or_level_rejected(self):
        for args in (
            {"focus":"Wrong","level":1,"opponent":"soldier","policy":"strike"},
            {"focus":"High","level":4,"opponent":"soldier","policy":"strike"},
            {"focus":"Low","level":2,"opponent":"hunter","policy":"strike"},
            {"focus":"Medium","level":3,"opponent":"soldier","policy":"magic"},
            {"focus":"High","level":3,"opponent":"soldier","policy":"strike","seed":-1},
        ):
            with self.subTest(args=args),self.assertRaises(ValueError):
                run_policy(**args)

    def test_11_documented_bounded_scope_and_mvp_counts(self):
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        doc=(root/"docs/design/b04-b05-anointed-mundane-native-g5-offense-v0.md").read_text().lower()
        for phrase in ("36","12/12","0/12","0/6","g0","g1","g2","g4","g5",
                       "dagger","sword","soldier","sentry","d4","d6","not certified",
                       "source","unopposed","noncombat"):
            self.assertIn(phrase,doc)


if __name__=="__main__":
    unittest.main()
