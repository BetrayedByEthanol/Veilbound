"""B04/B05 source-bound Anointed human-pilot evidence intake, not certification."""
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.b05_anointed_pilot_evidence_intake_v0 import (
    VERSION,FOCUSES,LEVELS,DOMAINS,UNRESOLVED,
    pilot_slots,blank_template,validate_intake,aggregate_intakes,
    source_actor,canonical_digest,
)


def packet(focus="High",level=1,*,session="pilot-session-01",domains=()):
    value=blank_template(focus=focus,level=level)
    value.update({
        "session_id":session,"session_date":"2026-10-30",
        "scenario_id":"gm:pilot:restoration-field",
        "session_sequence":1,
        "gm_observation_reference":"external:gm-field-notes-001",
        "independent_review_reference":"",
    })
    value["player_decisions"]=[{
        "domain":domain,"decision_id":f"human-candidate-{i}",
        "chosen_action":f"Player reported choosing {domain} action {i}",
        "alternative_considered":f"Player reported considering other {domain} action {i}",
        "observed_consequence":f"GM reported consequence for {domain} choice {i}",
        "source_event_reference":f"unverified:table-log:entry-{i}",
    } for i,domain in enumerate(domains)]
    return value


class AnointedPilotFieldEvidenceTests(unittest.TestCase):
    def test_01_nine_authentic_anointed_slots_are_not_nine_certificates(self):
        slots=pilot_slots()
        self.assertEqual(9,len(slots))
        self.assertEqual({(f,lv) for f in FOCUSES for lv in LEVELS},
                         {(v["focus"],v["level"]) for v in slots})
        for slot in slots:
            actor=source_actor(slot["focus"],slot["level"])
            self.assertEqual(slot["source_role"],actor.source.source_id)
            self.assertEqual(slot["source_digest"],actor.source.digest)
            self.assertEqual("SOURCE_STRUCTURAL_ONLY",slot["status"])
            self.assertIs(slot["human_play_certified"],False)
            self.assertIs(slot["independent_focus_certified"],False)

    def test_02_blank_template_contains_no_invented_session_or_gm_verdict(self):
        for focus in FOCUSES:
            form=blank_template(focus=focus,level=2)
            self.assertEqual(VERSION,form["version"])
            self.assertEqual([],form["player_decisions"])
            self.assertEqual("",form["session_id"])
            self.assertEqual("",form["gm_observation_reference"])
            self.assertIsNone(form["session_sequence"])
            with self.assertRaises(ValueError):
                validate_intake(form)

    def test_03_valid_structural_intake_does_not_prove_actual_play(self):
        for focus in FOCUSES:
            for level in LEVELS:
                candidate=packet(focus,level,domains=DOMAINS)
                report=validate_intake(candidate)
                self.assertTrue(report["structural_intake_valid"])
                self.assertEqual(4,report["reported_choices"])
                self.assertEqual(list(sorted(DOMAINS)),report["reported_domains"])
                self.assertEqual(canonical_digest(candidate),
                                 report["intake_sha256"])
                for key in ("actual_human_play_verified",
                            "gm_identity_authenticated",
                            "native_receipts_verified",
                            "independent_focus_certified",
                            "mvp_exit_certified"):
                    self.assertIs(report[key],False)
                self.assertEqual(list(UNRESOLVED),report["unresolved"])

    def test_04_source_hash_and_actor_role_spoofing_are_refused(self):
        for focus in FOCUSES:
            p=packet(focus,3)
            for field,replacement in (
                ("source_digest","0"*64),
                ("source_role","F"),
                ("source_role","AL" if focus!="Low" else "AH"),
                ("focus","Gifted"),
                ("level",4),
                ("level",True),
            ):
                bad=deepcopy(p)
                bad[field]=replacement
                with self.subTest(focus=focus,field=field,value=replacement):
                    with self.assertRaises(ValueError):
                        validate_intake(bad)

    def test_05_disallow_self_declared_certification_fields(self):
        p=packet(domains=DOMAINS)
        for field in ("independent_focus_certified",
                      "gm_authenticated",
                      "mvp_exit_certified",
                      "native_receipts_verified"):
            forged=deepcopy(p)
            forged[field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_intake(forged)
        p["version"]="unsupported-old-v0"
        with self.assertRaises(ValueError):
            validate_intake(p)

    def test_06_required_external_session_identity_and_legal_date(self):
        p=packet()
        for field,replacement in (
            ("session_id",""),
            ("session_date","sometime"),
            ("session_date","2026-02-30"),
            ("session_sequence",0),
            ("session_sequence",True),
            ("gm_observation_reference",""),
            ("evidence_kind","self-certified"),
            ("scenario_id"," "),
        ):
            bad=deepcopy(p);bad[field]=replacement
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_intake(bad)

    def test_07_player_choices_require_distinct_options_and_observation(self):
        p=packet(domains=("combat","exploration"))
        bad=deepcopy(p)
        bad["player_decisions"][0]["alternative_considered"]=bad[
            "player_decisions"][0]["chosen_action"]
        with self.assertRaises(ValueError):
            validate_intake(bad)
        bad=deepcopy(p)
        bad["player_decisions"][0]["observed_consequence"]=""
        with self.assertRaises(ValueError):
            validate_intake(bad)
        bad=deepcopy(p)
        bad["player_decisions"][0]["domain"]="unsupported-winrate"
        with self.assertRaises(ValueError):
            validate_intake(bad)
        bad=deepcopy(p)
        bad["player_decisions"][0]["pretend_legal_native_step"]=True
        with self.assertRaises(ValueError):
            validate_intake(bad)
        bad=deepcopy(p)
        bad["player_decisions"][1]["decision_id"]=bad[
            "player_decisions"][0]["decision_id"]
        with self.assertRaises(ValueError):
            validate_intake(bad)
        self.assertEqual(2,validate_intake(p)["reported_choices"])

    def test_08_aggregation_preserves_all_nine_gaps_even_when_forms_full(self):
        forms=[packet(f,lv,session=f"pilot-{f}-{lv}",domains=DOMAINS)
               for f in FOCUSES for lv in LEVELS]
        result=aggregate_intakes(forms)
        self.assertEqual(9,len(result["slots"]))
        self.assertEqual(9,result["submitted_sessions"])
        self.assertEqual(9,result["reported_complete_domain_sets"])
        for slot in result["slots"]:
            self.assertEqual(1,slot["reported_sessions"])
            self.assertEqual(list(sorted(DOMAINS)),slot["reported_domains"])
            self.assertIs(slot["independent_focus_certified"],False)
        self.assertEqual((0,0,0),(result["independently_certified_focuses"],
                                  result["strict_mvp_exits"],
                                  result["externally_verified_sessions"]))

    def test_09_empty_and_repeated_sessions_never_close_a_gate(self):
        empty=aggregate_intakes([])
        self.assertEqual(0,empty["submitted_sessions"])
        self.assertEqual(9,len(empty["slots"]))
        self.assertEqual(0,empty["reported_complete_domain_sets"])
        self.assertTrue(all(s["reported_sessions"]==0 for s in empty["slots"]))
        p=packet()
        with self.assertRaises(ValueError):
            aggregate_intakes([p,deepcopy(p)])
        with self.assertRaises(ValueError):
            aggregate_intakes({"sessions":[p]})

    def test_10_source_docs_keep_gm_and_independent_certification_open(self):
        root=Path(__file__).resolve().parents[1]
        doc=(root/"docs/design/b04-b05-anointed-field-pilot-evidence-v0.md").read_text().lower()
        roadmap=(root/"docs/design/veilbound-roadmap-and-mvp-readiness.md").read_text()
        index=(root/"docs/design/README.md").read_text()
        for term in ("nine", "12/12", "0/12", "0/6", "three-to-five",
                     "independent", "unverified", "source", "combat",
                     "exploration", "mission", "advancement", "consent",
                     "intrusion", "human", "gm", "not certified"):
            self.assertIn(term,doc)
        self.assertIn("b04-b05-anointed-field-pilot-evidence-v0.md",index)
        self.assertEqual(6,sum(l.startswith("| [ ] **") for l in roadmap.splitlines()))
        self.assertIn("**12/12**",roadmap)
        self.assertIn("**0/12**",roadmap)
        self.assertIn("**0/6**",roadmap)


if __name__=="__main__":
    unittest.main()
