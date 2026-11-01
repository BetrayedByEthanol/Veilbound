"""Alpha first-cohort source, evidence-integrity and noncertifying review tests."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.b04_b05_b06_b07_first_cohort_pilot_v0 import (
    blank_packet, validate, run, COHORT_ID, PAIRINGS,
    CAPABILITIES, DOC_KINDS, CODES,
)
from scripts.b04_b07_pilot_evidence_cohorts_v0 import preflight as cohort_preflight


def register(packet, kind, ref, root=None):
    assert kind in DOC_KINDS
    data=("test-only-unobserved-local-fixture:"+ref).encode()
    rel="records/"+ref+".txt"
    if root is not None:
        p=Path(root)/rel
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(data)
    packet["evidence_files"].append({
        "ref_id":ref,"kind":kind,"path":rel,"sha256":sha256(data).hexdigest(),
    })
    return ref


def one_synthetic_session(packet, root=None):
    """Recorded-reference-shaped test data, NEVER an actual played session."""
    cohort=packet["cohort_packet"]["cohorts"][0]
    cohort["gm_ref"]="GM-TEST-ONLY"
    cohort["report_author_ref"]="AUTHOR-TEST-ONLY"
    for i,actor in enumerate(cohort["characters"],1):
        actor["player_ref"]=f"PLAYER-TEST-{i}"
    r=lambda kind,name:register(packet,kind,name,root)
    before=r("resource_snapshot","source-start")
    after=r("resource_snapshot","source-end")
    choice=r("player_choice","choice")
    alternative=r("player_choice","alternative")
    consequence=r("gm_adjudication","gm-consequence")
    action=r("source_action","action")
    s_before=r("resource_snapshot","scene-start")
    s_after=r("resource_snapshot","scene-end")
    clock=r("clock_trace","g42-clock")
    cohort["sessions"].append({
        "session_id":"TEST-S1","played_at":"FAKE-TEST-DATE",
        "incoming_handoff_ref":"",
        "start_resource_state_ref":before,
        "end_resource_state_ref":after,
        "inter_session_transition_ref":"",
        "scenes":[{
            "scene_id":"TEST-SCENE-1",
            "beat":"supply","level":1,"outcome":"partial",
            "choice_ref":choice,"alternative_ref":alternative,
            "gm_consequence_ref":consequence,"source_action_ref":action,
            "resource_before_ref":s_before,"resource_after_ref":s_after,
            "world_clock_ref":clock,
        }],
    })
    return choice


class FirstCohortPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blank=blank_packet()

    def test_01_four_canonical_roster_and_source_sha(self):
        p=self.blank
        self.assertEqual(p["cohort_id"],COHORT_ID)
        self.assertEqual(len(p["characters"]),4)
        self.assertEqual(tuple(x["pairing"] for x in p["characters"]),PAIRINGS)
        self.assertEqual(tuple(CAPABILITIES),PAIRINGS)
        self.assertEqual((len(p["review_queue"]),len(CODES)),(84,7))
        self.assertEqual(
            {(x["character_id"],x["level"],x["criterion"])
             for x in p["review_queue"]},
            {(f"PC-{i}",l,c)
             for i in range(1,5) for l in (1,2,3) for c in CODES})
        self.assertEqual(cohort_preflight(p["cohort_packet"])["strict_mvp_exits_met"],0)

    def test_02_empty_packet_has_no_fake_play_or_accepted_reviews(self):
        receipt=validate(deepcopy(self.blank))
        self.assertEqual(receipt["candidate_sessions_reported"],0)
        self.assertEqual(receipt["candidate_milestones_reported"],0)
        self.assertEqual(receipt["candidate_review_submissions"],0)
        self.assertEqual(receipt["candidate_review_notes_present"],0)
        self.assertFalse(receipt["evidence_bytes_sha256_checked"])
        self.assertEqual(receipt["independently_certified_focuses"],0)
        self.assertEqual(receipt["strict_mvp_exits_met"],0)

    def test_03_source_scoped_plan_explicitly_blocks_missing_mixed_engine(self):
        r=run()
        self.assertEqual(r["cohort_id"],COHORT_ID)
        self.assertEqual(r["level_review_slots"],84)
        self.assertEqual([x["beats"] for x in r["recommended_schedule"]],
                         [["supply","gate"],["forest"],["shrine"],["village"]])
        self.assertTrue(any("no single native G8 L1" in x
                            for x in r["blocking_scenes"]))
        self.assertIn("physical proxies",CAPABILITIES["Priest/Low"]["constraint"])
        self.assertFalse(r["individual_C1_C7_certification"])

    def test_04_test_only_session_can_be_structurally_checked_with_real_local_bytes(self):
        with TemporaryDirectory() as root:
            p=blank_packet()
            choice=one_synthetic_session(p,root)
            result=validate(p,evidence_root=root)
            self.assertTrue(result["evidence_bytes_sha256_checked"])
            self.assertEqual(result["candidate_sessions_reported"],1)
            self.assertEqual(result["candidate_milestones_reported"],0)
            self.assertEqual(result["independently_certified_focuses"],0)
            entry=next(x for x in p["review_queue"]
                       if x["character_id"]=="PC-1"
                       and x["level"]==1 and x["criterion"]=="C4")
            entry["status"]="SUBMITTED"
            entry["evidence_refs"]=[choice]
            result=validate(p,evidence_root=root)
            self.assertEqual(result["candidate_review_submissions"],1)
            self.assertEqual(result["candidate_review_notes_present"],0)

    def test_05_submitted_notes_still_never_certify_or_authenticate_people(self):
        with TemporaryDirectory() as root:
            p=blank_packet()
            choice=one_synthetic_session(p,root)
            review=register(p,"review_notes","review-note",root)
            finding=register(p,"review_notes","review-findings",root)
            entry=next(x for x in p["review_queue"]
                       if x["character_id"]=="PC-1"
                       and x["level"]==1 and x["criterion"]=="C4")
            entry.update(status="REVIEWED_EVIDENCE_PRESENT",
                         evidence_refs=[choice],
                         reviewer_identity_ref="INDEPENDENT-REVIEWER-TEST",
                         reviewer_ref=review,finding_ref=finding)
            result=validate(p,evidence_root=root)
            self.assertEqual(result["candidate_review_notes_present"],1)
            self.assertFalse(result["external_human_identity_authenticated"])
            self.assertEqual(result["actual_gm_story_milestones_authenticated"],0)
            self.assertEqual(result["strict_mvp_exits_met"],0)
            entry["reviewer_identity_ref"]="GM-TEST-ONLY"
            with self.assertRaises(ValueError):
                validate(p,evidence_root=root)

    def test_06_mutated_evidence_is_rejected_by_local_integrity_check(self):
        with TemporaryDirectory() as root:
            p=blank_packet()
            one_synthetic_session(p,root)
            original=validate(p,evidence_root=root)
            self.assertTrue(original["evidence_bytes_sha256_checked"])
            path=Path(root)/p["evidence_files"][0]["path"]
            path.write_text("tampered",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"differ from manifest"):
                validate(p,evidence_root=root)
            # A source-only check cannot claim byte verification.
            self.assertFalse(validate(p)["evidence_bytes_sha256_checked"])

    def test_07_evidence_path_traversal_and_external_symlink_rejected(self):
        with TemporaryDirectory() as root,TemporaryDirectory() as outside:
            p=blank_packet()
            one_synthetic_session(p,root)
            altered=deepcopy(p)
            altered["evidence_files"][0]["path"]="../outside.txt"
            with self.assertRaises(ValueError):
                validate(altered,evidence_root=root)
            link=Path(root)/p["evidence_files"][0]["path"]
            link.unlink()
            outside_file=Path(outside)/"external.txt"
            outside_file.write_text("external bytes",encoding="utf-8")
            link.symlink_to(outside_file)
            with self.assertRaises(ValueError):
                validate(p,evidence_root=root)

    def test_08_unknown_manifest_kind_duplicate_refs_and_wrong_kind_fail(self):
        with TemporaryDirectory() as root:
            p=blank_packet()
            one_synthetic_session(p,root)
            for name,modify in (
                ("kind",lambda q:q["evidence_files"][0].update(kind="fictional")),
                ("duplicate",lambda q:q["evidence_files"].append(
                    deepcopy(q["evidence_files"][0]))),
                ("source_action_substitution",lambda q:q["evidence_files"][-2].update(
                    kind="selected_sheet")),
                ("bad_digest",lambda q:q["evidence_files"][0].update(
                    sha256="SHA_NOT_SHA256")),
            ):
                with self.subTest(name=name):
                    candidate=deepcopy(p)
                    modify(candidate)
                    with self.assertRaises(ValueError):
                        validate(candidate,evidence_root=root)

    def test_09_forged_cohort_or_source_or_certification_rejected(self):
        for name,change in (
            ("source_digest",lambda q:q.update(source_roster_digest="0"*64)),
            ("other_cohort",lambda q:q.update(cohort_id="COHORT-BETA")),
            ("person_name",lambda q:q["characters"][0].update(pairing="Priest/High")),
            ("false_gate",lambda q:q.update(strict_mvp_exits_met=1)),
            ("human_claim",lambda q:q.update(human_sessions_authenticated=1)),
            ("fake_source",lambda q:q["characters"][0].update(
                source_fingerprints={"a.py":"fake"})),
        ):
            with self.subTest(name=name):
                candidate=deepcopy(self.blank)
                change(candidate)
                with self.assertRaises(ValueError):
                    validate(candidate)

    def test_10_unreported_scene_cannot_be_used_for_combat_review(self):
        p=blank_packet()
        ref=register(p,"source_action","unsourced-combat")
        row=next(x for x in p["review_queue"]
                 if x["character_id"]=="PC-3"
                 and x["level"]==1 and x["criterion"]=="C3")
        row.update(status="SUBMITTED",evidence_refs=[ref])
        with self.assertRaisesRegex(ValueError,"unplayed level"):
            validate(p)

    def test_11_milestone_C7_and_higher_level_C2_not_claimable_early(self):
        p=blank_packet()
        ref=register(p,"source_action","unearned-milestone")
        for code,level in (("C7",1),("C2",2)):
            with self.subTest(code=code):
                candidate=deepcopy(p)
                row=next(x for x in candidate["review_queue"]
                         if x["character_id"]=="PC-1"
                         and x["level"]==level and x["criterion"]==code)
                row.update(status="SUBMITTED",evidence_refs=[ref])
                with self.assertRaises(ValueError):
                    validate(candidate)

    def test_12_low_priest_variant_and_selected_level_sheet_separation(self):
        with TemporaryDirectory() as root:
            p=blank_packet()
            ref=register(p,"selected_sheet","sheet-a1",root)
            note=register(p,"review_notes","sheet-review",root)
            selected=p["characters"][0]
            selected["selected_variant"]="A"
            selected["sheet_refs"]["1"]=ref
            selected["independent_sheet_reviewer_ref"]=note
            self.assertEqual(validate(p,evidence_root=root)["strict_mvp_exits_met"],0)
            selected["sheet_refs"]["2"]=ref
            with self.assertRaisesRegex(ValueError,"cannot be reused"):
                validate(p,evidence_root=root)
            selected["sheet_refs"]["2"]=""
            selected["selected_variant"]="default"
            with self.assertRaises(ValueError):
                validate(p,evidence_root=root)

    def test_13_json_contract_is_stable(self):
        self.assertEqual(json.loads(json.dumps(self.blank)),self.blank)
        self.assertEqual(json.loads(json.dumps(run())),run())


if __name__=="__main__":
    unittest.main()
