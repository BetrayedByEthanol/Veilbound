"""B06 G7-C: native complete-party exit and fail-closed defeat witnesses."""
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from scripts.b06_encounter_state_v0 import RegenerationChoice,UnresolvedDecision
from scripts.b06_damage_v0 import DamagePacket
from scripts.b06_g7a_native_terminal_census_v0 import (
    _regen_choice,_melee,canonical_digest,
)
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
from scripts.b06_g7c_party_terminals_v0 import (
    PartyTerminal, EXIT_ROUTES, run_trial, census, OUTCOMES, HISTORICAL_SHA, main
)


def fully_exited_scene(*,size=4,level=3):
    c=mixed_scene(size=size,level=level,seed=23001,party_exits=True)
    e=c.e
    for actor in e.order:
        c.bridge.start_next_turn(RegenerationChoice())
        if actor!="hunter":
            for delta in EXIT_ROUTES[actor]:
                assert e.g1.step(actor,delta,cautious=True,responses=())
            c.withdraw(actor)
        c.bridge.end_current_turn()
    return c


class G7CTests(unittest.TestCase):
    def test_01_certifies_all_three_and_four_real_native_actor_exits(self):
        for size in (3,4):
            for level in (2,3):
                with self.subTest(size=size,level=level):
                    c=fully_exited_scene(size=size,level=level)
                    p=PartyTerminal(c).attest_withdrawal()
                    self.assertEqual(p["ending"],"party_withdrawal_attested")
                    self.assertEqual(len(p["member_exits"]),size)
                    self.assertEqual({v["actor"] for v in p["member_exits"]},
                                     set(c.e.order)-{"hunter"})
                    self.assertEqual(sum(x["kind"]=="g7c_party_withdrawal_attested"
                                         for x in c.e.ledger),1)
                    for proof in p["member_exits"]:
                        step=c.e.ledger[proof["movement"]]
                        g45=c.e.ledger[proof["g45"]]
                        g5=c.e.ledger[proof["g5"]]
                        self.assertEqual(step["kind"],"g1_movement_step")
                        self.assertEqual(g45["kind"],"g45_withdrawal_attested")
                        self.assertEqual(g5["kind"],"g5_terminal_exit")
                        self.assertEqual(step["detail"]["actor"],proof["actor"])
                        self.assertEqual(g45["detail"]["movement_event_index"],
                                         proof["movement"])
                        self.assertEqual(g5["detail"]["movement_index"],
                                         proof["movement"])
                    self.assertIsNone(p["hunter_cr"])
                    self.assertFalse(p["complete_party_pack_certified"])

    def test_02_seeds_complete_one_real_round_or_keep_incompleteness(self):
        for size,level,seed in ((3,2,0),(4,3,1),(3,3,30),(4,2,30)):
            with self.subTest(size=size,level=level,seed=seed):
                a=run_trial(level,size,seed,include_ledger=True)
                self.assertIn(a["outcome"],OUTCOMES)
                self.assertEqual(a["ledger_sha256"],canonical_digest(a["ledger"]))
                self.assertEqual(len(a["exited"])+len(a["unexited"]),size)
                self.assertEqual(a["rounds_completed"],1)
                self.assertEqual(a["turns_completed"],size+1)
                self.assertIsNone(a["hunter_cr"])
                self.assertFalse(a["complete_party_pack_certified"])

    def test_03_without_authored_exits_cannot_certify(self):
        c=mixed_scene(size=3,level=2,seed=0)
        for actor in c.e.order:
            c.bridge.start_next_turn(RegenerationChoice())
            c.bridge.end_current_turn()
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_withdrawal()

    def test_04_partial_exit_is_not_a_whole_party_terminal(self):
        c=mixed_scene(size=3,level=2,seed=3,party_exits=True)
        e=c.e
        c.bridge.start_next_turn(RegenerationChoice())
        c.bridge.end_current_turn()
        for actor in ("vanguard","guardian","archer"):
            c.bridge.start_next_turn(RegenerationChoice())
            if actor!="guardian":
                for delta in EXIT_ROUTES[actor]:
                    e.g1.step(actor,delta,cautious=True)
                c.withdraw(actor)
            c.bridge.end_current_turn()
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_withdrawal()
        self.assertFalse(any(x["kind"]=="g7c_party_withdrawal_attested"
                             for x in e.ledger))

    def test_05_no_terminal_during_open_turn_or_unfinished_round(self):
        c=mixed_scene(size=3,level=2,seed=4,party_exits=True)
        c.bridge.start_next_turn(RegenerationChoice())
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_withdrawal()
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_defeat()

    def test_06_no_duplicate_terminal_or_cross_type_attestation(self):
        c=fully_exited_scene()
        PartyTerminal(c).attest_withdrawal()
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_withdrawal()
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_defeat()

    def test_07_no_whole_party_terminal_for_observed_dying(self):
        c=mixed_scene(size=3,level=3,seed=5,party_exits=True)
        e=c.e
        for actor in e.order:
            c.bridge.start_next_turn(RegenerationChoice())
            c.bridge.end_current_turn()
        e.actors["vanguard"].hp=0
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_defeat()
        self.assertFalse(any(x["kind"]=="g7c_party_defeat_attested"
                             for x in e.ledger))

    def test_08_spoofed_mass_deaths_cannot_certify_party_defeat(self):
        c=mixed_scene(size=3,level=3,seed=6,party_exits=True)
        e=c.e
        for actor in e.order:
            c.bridge.start_next_turn(RegenerationChoice())
            c.bridge.end_current_turn()
        for actor in ("vanguard","guardian","archer"):
            a=e.actors[actor]
            e.g4.apply_damage(
                actor,(DamagePacket("hp","Fire",2*a.hp_max),),
                event_key=f"external:fake:{actor}",cause="source-profile:B06-AT-04",
                wound_location_roll=8)
            self.assertTrue(a.dead)
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_defeat()
        self.assertFalse(any(x["kind"]=="g7c_party_defeat_attested"
                             for x in e.ledger))

    def test_09_wrong_scene_exit_cannot_be_supplied_at_withdrawal(self):
        c=mixed_scene(size=3,level=2,seed=7,party_exits=True)
        with self.assertRaises(UnresolvedDecision):
            c.withdraw("hunter")
        self.assertEqual(len(c.scene_exits),3)
        self.assertIsNone(c.scene_exit)

    def test_10_duplicate_or_conflicting_scene_exits_rejected(self):
        from scripts.b06_soldier_sentry_g5_v0 import SourceMelee, SceneExit
        # The adapter's guard is strict even before any native action.
        c=mixed_scene(size=3,level=3,seed=8)
        base=c.scene_exit
        self.assertIsNone(base)
        old=c.scene_exits
        self.assertEqual(old,())
        with self.assertRaises(ValueError):
            SourceMelee(c.e,scene_exits=[1])
        # Same engine cannot attach a second G5 (required invariant).
        exit=SceneExit(c.e.scenario,c.e.g1.scene_id,c.e.objective,
                       "archer",(0,4),"policy")
        with self.assertRaises(ValueError):
            SourceMelee(c.e,scene_exit=exit,scene_exits=(exit,))

    def test_11_tampered_or_missing_member_receipts_fail_closed(self):
        for kind in ("policy","movement_index","at"):
            with self.subTest(kind=kind):
                c=fully_exited_scene(size=3)
                event=next(v for v in c.e.ledger
                           if v["kind"]=="g5_terminal_exit")
                event["detail"][kind]=("forged" if kind=="policy" else
                                       -1 if kind=="movement_index" else [1,1])
                with self.assertRaises(UnresolvedDecision):
                    PartyTerminal(c).attest_withdrawal()

    def test_12_damage_after_exit_prevents_party_terminal(self):
        c=fully_exited_scene(size=3)
        e=c.e
        e.g4.apply_damage("archer",(DamagePacket("hp","Fire",1),),
                          event_key="test:post_exit",cause="test:fixture")
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_withdrawal()

    def test_13_no_full_party_exit_from_stale_positions_or_missing_step(self):
        c=fully_exited_scene(size=3)
        e=c.e
        step=next(v for v in e.ledger if v["kind"]=="g1_movement_step"
                  and v["detail"]["actor"]=="archer")
        step["detail"]["new"]=[[1,4]]
        with self.assertRaises(UnresolvedDecision):
            PartyTerminal(c).attest_withdrawal()

    def test_14_128_seeds_all_four_cases_accounted_and_no_CR(self):
        report=census(128)
        self.assertEqual(len(report["cases"]),4)
        for cell in report["cases"]:
            with self.subTest(level=cell["level"],size=cell["party_size"]):
                self.assertEqual(cell["seed_count"],128)
                self.assertEqual(sum(cell["counts"].values()),128)
                self.assertEqual(len(cell["trial_digests"]),128)
                self.assertEqual([r["seed"] for r in cell["trial_digests"]],
                                 list(range(128)))
                self.assertIsNone(cell["win_rate"])
                self.assertIsNone(cell["hunter_cr"])
        self.assertEqual(report["historical_phase3_sha256"],HISTORICAL_SHA)
        self.assertIsNone(report["hunter_cr"])

    def test_15_reproducibility_and_census_bounds(self):
        self.assertEqual(census(3,start_seed=30),census(3,start_seed=30))
        for args in ({"seeds":0},{"seeds":True},{"seeds":129},
                     {"start_seed":-1},{"include_trials":0}):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    census(**args)
        for values in ((1,3,0),(2,2,0),(2,3,-1)):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    run_trial(*values)

    def test_16_cli_digest_and_original_g7b_policy_untouched(self):
        from scripts.b06_g7b_tactical_terminal_census_v0 import native_case
        previous=native_case(2,3,0,policy="g7b_archer_exit")
        self.assertNotEqual(previous["outcome"],"party_withdrawal_attested")
        output=StringIO()
        with redirect_stdout(output):
            main(["--seeds","1"])
        obj=json.loads(output.getvalue())
        digest=obj.pop("census_sha256")
        self.assertEqual(digest,canonical_digest(obj))
        self.assertEqual(len(obj["cases"]),4)


    def test_17_post_exit_move_away_then_back_is_not_an_exit(self):
        # Codex P2: a previous G5 exit cannot be resurrected by ending at
        # the same border coordinate after fresh, real G1 movements.
        for size in (3,4):
            with self.subTest(party_size=size):
                c=mixed_scene(size=size,level=3,seed=23001,
                              party_exits=True)
                e=c.e
                for actor in e.order:
                    c.bridge.start_next_turn(RegenerationChoice())
                    if actor!="hunter":
                        for delta in EXIT_ROUTES[actor]:
                            self.assertTrue(e.g1.step(
                                actor,delta,cautious=True,responses=()))
                        c.withdraw(actor)
                        if actor=="vanguard":
                            # A spent 8 MP to reach its authored border;
                            # the remaining 4 MP suffice to step away and
                            # back on the SAME own turn, after G5 exit.
                            self.assertTrue(e.g1.step(
                                actor,(1,0),responses=()))
                            self.assertTrue(e.g1.step(
                                actor,(-1,0),responses=()))
                    c.bridge.end_current_turn()
                self.assertEqual(e.actors["vanguard"].occupied,((0,2),))
                self.assertEqual(sum(x["kind"]=="round_end"
                                     for x in e.ledger),1)
                self.assertEqual(sum(x["kind"]=="g5_terminal_exit"
                                     for x in e.ledger),size)
                steps=[x for x in e.ledger if
                       x["kind"]=="g1_movement_step"
                       and x["detail"]["actor"]=="vanguard"]
                exit_event=next(x for x in e.ledger if
                                x["kind"]=="g5_terminal_exit"
                                and x["detail"]["actor"]=="vanguard")
                self.assertEqual(len([x for x in steps if
                                      x["index"]>exit_event["index"]]),2)
                with self.assertRaisesRegex(
                        UnresolvedDecision,"Exited actor resumed"):
                    PartyTerminal(c).attest_withdrawal()
                self.assertFalse(any(
                    x["kind"]=="g7c_party_withdrawal_attested"
                    for x in e.ledger))

    def test_18_later_completed_round_invalidates_old_exit_without_movement(self):
        # A subsequent normal G0 start is enough to invalidate an
        # individually attested exit, even if the actor never moves
        # again and ends at the original authored square.
        for size in (3,4):
            with self.subTest(party_size=size):
                c=fully_exited_scene(size=size,level=3)
                e=c.e
                original_positions={p:e.actors[p].occupied
                                    for p in e.order if p!="hunter"}
                c.bridge.begin_next_round()
                for actor in e.order:
                    c.bridge.start_next_turn(RegenerationChoice())
                    c.bridge.end_current_turn()
                self.assertEqual(
                    {p:e.actors[p].occupied for p in original_positions},
                    original_positions)
                self.assertEqual(sum(x["kind"]=="round_end"
                                     for x in e.ledger),2)
                self.assertEqual(sum(
                    x["kind"]=="turn_start_expiry"
                    for x in e.ledger if x["detail"].get("actor")=="vanguard"),
                    2)
                with self.assertRaisesRegex(
                        UnresolvedDecision,"Exited actor resumed"):
                    PartyTerminal(c).attest_withdrawal()
                self.assertFalse(any(
                    x["kind"]=="g7c_party_withdrawal_attested"
                    for x in e.ledger))

    def test_19_invalid_legacy_single_scene_exit_is_value_error(self):
        # Codex P2: reject non-SceneExit *before* building the authored
        # actor-id set; the legacy public argument must not AttributeError.
        from scripts.b06_soldier_sentry_g5_v0 import SourceMelee
        from scripts.b06_hunter_g6a_v0 import HunterCombat
        for value in (0,False,"bad",{"actor_id":"archer"},
                      object(),("not","a","scene","exit")):
            for adapter in (SourceMelee,HunterCombat):
                with self.subTest(value_type=type(value).__name__,
                                  adapter=adapter.__name__):
                    c=mixed_scene(size=3,level=2,seed=113)
                    e=c.e
                    before=len(e.ledger)
                    with self.assertRaises(ValueError) as raised:
                        adapter(e,scene_exit=value)
                    self.assertNotIsInstance(raised.exception,AttributeError)
                    self.assertEqual(len(e.ledger),before)
                    self.assertIs(e.g5,c)
                    e.check()


if __name__=="__main__":
    unittest.main()
