"""Alpha first-cohort real-table GM handoff and NON-CERTIFYING readiness audit.

This is a source-linked operational bridge, not a gameplay resolver or an
alternative acceptance authority. It preserves the original Alpha intake,
checks its existing source/chronology/file-reference schema, and never infers
that any reported pseudonym, action or milestone was genuinely observed.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from scripts.b04_b05_b06_b07_first_cohort_pilot_v0 import (
    blank_packet, validate, PAIRINGS, COHORT_ID, CODES, SOURCE_GAPS,
)
from scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 import (
    GATES, COHORTS,
)
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

VERSION="B04-B05-B06-B07-Alpha-GM-Execution-Handoff-v0"
ROOT=Path(__file__).resolve().parents[1]
MECHANICAL_SOURCES={
    "full_selected_low_priest":"scripts/b05_low_priest_life_l1_l3_v0.py",
    "high_scholar":"scripts/b05_high_scholar_fire_l1_l3_v0.py",
    "high_gifted":"scripts/b05_high_gifted_l1_l3_v0.py",
    "medium_anointed":"scripts/b05_medium_anointed_restoration_l1_l3_v0.py",
    "alpha_L1_mixed":"scripts/b04_b05_b06_alpha_mixed_native_v0.py",
    "alpha_L1_tactical":"scripts/b04_b05_b06_alpha_l1_tactics_v0.py",
    "alpha_L1_L3_progression":"scripts/b04_b05_b06_alpha_l2_l3_progression_v0.py",
    "alpha_L2_venom_sentry":"scripts/b04_b05_b06_alpha_l2_hazard_sentry_v0.py",
    "original_noncombat":"scripts/b05_b06_integrated_noncombat_adventure_v0.py",
    "gm_three_enemy_reference":"scripts/b06_representative_gm_encounter_packs_v0.py",
    "flexible_cohort_evidence":"scripts/b04_b07_pilot_evidence_cohorts_v0.py",
    "alpha_evidence_intake":"scripts/b04_b05_b06_b07_first_cohort_pilot_v0.py",
    "independent_focus_protocol":"scripts/b04_b07_twelve_focus_certification_protocol_v0.py",
}
BEATS=("supply","gate","forest","shrine","village")
SCENES=(
    ("supply",1,"L1 exploration, spoilage and source-paid noncombat alternatives",
     "Actual cause, original held items, medical/source checks, competing crossing and elapsed G4.2 travel",
     "NONCOMBAT_GM_FACTS_AND_PLAYER_CHOICES"),
    ("gate",1,"Native L1 full-Alpha Soldier contact with Guard/Dodge, optional paid Focus actions, withdrawal or held position",
     "GM decides negotiation, geometry, enemy behavior and each declared action; unsupported responses require separate source adjudication",
     "BOUNDED_HOSTILE_OPTION_ONLY"),
    ("forest",2,"Original anatomical Hunter at L2, paid Bite and G4.4 venom, source B-only Endurance or A untreated, genuine G1/G5 exits",
     "Only after actual first group award; decide ambush, pursuit, protection, safe travel and real venom resolution",
     "HAZARD_AND_PURSUIT_CONDITIONAL"),
    ("shrine",2,"Original cold/prepared Sentry options; source enhanced sword damage and same-L2 toxin/Endurance continuity",
     "Choose authentic cold or prepared start; unresolved poison or maintained magic blocks unreviewed L2-to-L3 handoff",
     "CROSS_LEVEL_ACTIVE_EFFECT_BLOCK"),
    ("village",3,"Actual return, patient care and supply-crisis consequences; bounded L3 source actions available",
     "Only after distinct actual second group award; record multiple true outcomes and weaknesses, no mass cure or scripted victory",
     "REAL_GM_ENDING_REQUIRED"),
)
TRIAGE=(
    ("P01","REAL_PARTICIPANTS_AND_SHEETS","EXTERNAL_PREPLAY",
     "Four actual players choose original L1 Focus sheets, including Low Priest A/B. GM and independent reviewer validate purchases, known/prepared magic, equipment and source hashes.",
     "DO_NOT_START_UNTIL_RECORDED"),
    ("P02","GM_SCENE_FACTS_AND_TACTICAL_POLICY","GM_PREPLAY",
     "GM establishes village spoilage truth, terrain/entry, soldier hostility, Hunter pursuit, Sentry cold/prepared start and noncombat alternatives before checks.",
     "GM_ADJUDICATION_NEEDED"),
    ("P03","ARBITRARY_MIXED_ALPHA_COMBAT","CONDITIONAL_IMPLEMENTATION",
     "L1 Guard/Dodge and L1-L3 source actions are bounded fixtures. Any human-selected attack, support, reaction, contested Intrusion or off-turn option outside an authorized native path requires explicit source referee resolution or targeted implementation.",
     "STOP_UNSUPPORTED_PATH"),
    ("P04","L2_L3_REAL_MILESTONES","EXTERNAL_GM_EVIDENCE",
     "Two separate genuinely GM-declared group-story achievements, not automatic gate/shrine script receipts, combat victory, Anointed Destiny or elapsed time; selected destination sheets and earned/saved choices checked.",
     "NO_DEEMED_AWARD"),
    ("P05","LONG_LIVED_CROSS_LEVEL_EFFECTS","CONDITIONAL_IMPLEMENTATION",
     "Same-level venom/Endurance carry is verified, but active toxins, other maintained hosts and unsafe pursuit cannot cross a clean L2-L3 level-up in the bounded Alpha chain. Resolve under canonical rules or stop and implement that exact case.",
     "STOP_UNSUPPORTED_TRANSFER"),
    ("P06","ADVANCEMENT_RESOURCE_POLICY","GM_AND_SOURCE_REVIEW",
     "Synthetic progression stages gained Max VP as Spent for conservative testing; do not interpret fixture policy as a canonical universal level-up refresh. Review actual source/legal award and resource changes.",
     "DO_NOT_INFER_FREE_REFILL"),
    ("P07","COUNTERCASES_AND_ROLE_OBSERVATION","EXTERNAL_PLAY_EVIDENCE",
     "Record each actual L1/L2/L3 combat AND noncombat choice and rejected alternative, Focus weakness, actual GM consequences, resource/clock receipt and status.",
     "UNOBSERVED_UNTIL_PLAYED"),
    ("P08","INDEPENDENT_C1_C7_AND_SIX_GATES","EXTERNAL_REVIEW",
     "A reviewer independent from author/GM/players examines raw selected records; 84 Alpha slots cover only four of the twelve pairings. Beta/Gamma and 36 Focus-level slots still require evidence before full MVP acceptance.",
     "NO_AUTO_CERTIFICATION"),
)
CAPABILITIES=(
    ("full_selected_low_priest","BOUNDED_SOURCE_LEGAL",
     "Full Priest A/B L1-3 complete sheets; physical G8 A/B proxy attacks do not transfer to its source Rite"),
    ("alpha_L1_mixed","BOUNDED_SOURCE_LEGAL",
     "One original four-Focus Soldier source contact, explicit withdrawals, original unscaled opponent; not arbitrary action AI"),
    ("alpha_L1_tactical","BOUNDED_SOURCE_LEGAL",
     "Five authored Guard/Dodge/Take Hit and hold/withdraw policies; real player alternative still must be adjudicated"),
    ("alpha_L1_L3_progression","AUTHOR_CANDIDATE_ONLY",
     "Three clean source-native stages and two author-candidate story beats; no real GM award and no implicit VP refresh"),
    ("alpha_L2_venom_sentry","BOUNDED_SOURCE_LEGAL",
     "Original Hunter Bite/injection, prepared B-only Endurance, enhanced Sentry hit, atomic same-L2 hazard carry"),
    ("original_noncombat","AUTHOR_CANDIDATE_ONLY",
     "Paid source checks and authored consequences are illustrative GM premises, not actual social rulings"),
    ("gm_three_enemy_reference","ORIGINAL_OPPONENT_REFERENCE",
     "Soldier/Sentry/Hunter source profiles and fixed G8/G7 tests; not automatic selected Alpha tactical outcomes"),
)
# Distinct from the older frozen intake's SOURCE_GAPS field. Never mutate
# that field: it is a versioned compatibility and validator contract.
LEGACY_GAP_REASSESSMENT=(
    ("L1 general four-Focus combat","PARTIALLY_ADDRESSED",
     "Merged Alpha L1 source encounter and tactical policies now exist; general human-selected options remain conditional."),
    ("Hunter/defensive and venom coverage","PARTIALLY_ADDRESSED",
     "Anatomical Hunter and real G4.4 venom/Endurance and withdrawal tested; GM pursuit and alternate responses still need play."),
    ("Sentry coverage","PARTIALLY_ADDRESSED",
     "Cold source Reserve and HP/Fire/Vigor hit shown; other arrival states, human alternative actions and representative pressure still open."),
    ("L3 village and human choices","EXTERNAL_EVIDENCE_REQUIRED",
     "Candidate level-3 source actions exist; the actual village conclusion is a GM/player decision."),
    ("Cross-level active poison and hosts","UNSUPPORTED_UNTIL_ADJUDICATED",
     "Verified same-level toxin persistence is not a general legal L2-L3 rebind."),
)


def _sources():
    result={}
    for key,path in MECHANICAL_SOURCES.items():
        f=ROOT/path
        if not f.is_file():
            raise ValueError("Missing canonical source for Alpha handoff: "+path)
        result[key]={"path":path,"sha256":sha256(f.read_bytes()).hexdigest()}
    return result


def _stages():
    return [{"beat":beat,"target_level":level,
             "bounded_source_reference":source,
             "live_gm_player_requirement":gm,
             "guardrail":guardrail,
             "automatically_playable":False,
             "human_scene_observed":False}
            for beat,level,source,gm,guardrail in SCENES]


def _triage():
    return [{"id":ident,"dependency":topic,"owner_class":owner,
             "required_action":action,"stop_rule":stop}
            for ident,topic,owner,action,stop in TRIAGE]


def handoff(packet=None,*,evidence_root=None):
    """Current source audit plus original Alpha packet structural preflight.

    Even an apparently complete untrusted packet and matching local SHA
    cannot authenticate actual human sessions, accepted Focuses or GM awards.
    No personal references, raw evidence or submitted packet are echoed.
    """
    if evidence_root is not None and packet is None:
        raise ValueError("An evidence root needs an explicitly provided packet")
    if len(PAIRINGS)!=4 or tuple(PAIRINGS)!=tuple(COHORTS[COHORT_ID]):
        raise AssertionError("Canonical four Focus Alpha pairing order changed")
    if tuple(CODES)!=tuple("C"+str(i) for i in range(1,8)):
        raise AssertionError("Existing C1-C7 evidence source protocol changed")
    if len(GATES)!=6 or {g[0] for g in GATES}!={
            "Create","Act","Resolve","Advance","Challenge","Observe"}:
        raise AssertionError("Six fixed MVP acceptance gates changed")
    packet=deepcopy(blank_packet() if packet is None else packet)
    checked=validate(packet,evidence_root=evidence_root)
    if packet["cohort_id"]!=COHORT_ID or len(packet["review_queue"])!=84:
        raise ValueError("Original Alpha packet not selected")
    sources=_sources()
    choices=[{"character_id":c["character_id"],
              "pairing":c["pairing"],
              "level_sheet_selected":[bool(c["sheet_refs"][str(l)])
                                      for l in (1,2,3)],
              "variant_declared":bool(c["selected_variant"]),
              "review_notes_proposed":bool(c["independent_sheet_reviewer_ref"])}
             for c in packet["characters"]]
    emitted={
        "version":VERSION,
        "cohort_id":COHORT_ID,
        "status":"NONCERTIFYING_OPERATIONAL_HANDOFF",
        "source_snapshot_sha256":canonical_digest(sources),
        "source_files":sources,
        "source_intake_version":packet["version"],
        "legacy_packet_source_gaps_preserved":len(SOURCE_GAPS),
        "legacy_gap_reassessment":[{"topic":a,"state":b,"explanation":c}
                                  for a,b,c in LEGACY_GAP_REASSESSMENT],
        "native_reference_scope":[
            {"id":ref,"state":status,"scope":scope}
            for ref,status,scope in CAPABILITIES],
        "scene_handoff":_stages(),
        "prerequisite_register":_triage(),
        "selected_character_preflight":choices,
        "original_intake_shape_preflight":checked,
        "pilot_packet_unmodified_by_audit":True,
        "table_execution_decision":"CONDITIONAL_GO_ONLY_AFTER_GM_SOURCE_AND_SAFETY_REVIEW",
        "automatic_mixed_party_gameplay":"NO_GO_UNSUPPORTED_PLAYER_CHOICES",
        "independent_certification_decision":"NO_GO_UNTIL_AUTHENTIC_HUMAN_REVIEW",
        "level_up_with_live_unsupported_effects":"NO_GO_UNTIL_SOURCE_LEGAL_RESOLUTION",
        "source_legal_alternatives_require_human_choice":True,
        "original_player_pilot_sessions_verified":0,
        "external_gm_milestones_authenticated":0,
        "independent_full_focus_certificates":0,
        "strict_mvp_exits_met":0,
        "structural_focus_pairings":12,
        "original_mvp_blockers_closed":3,
        "full_twelve_focus_cohort_execution_not_complete":True,
        "independent_gate_register":[{"gate":name,"needed":needed,
                                       "status":"OPEN",
                                       "automatically_accepted":False}
                                      for name,needed in GATES],
        "privacy":"Keep populated packets and raw evidence in private access-controlled storage, not public CI artifacts.",
    }
    return emitted


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--packet",metavar="JSON")
    cli.add_argument("--evidence-root",metavar="DIR")
    cli.add_argument("--blank-packet",action="store_true")
    args=cli.parse_args()
    if args.blank_packet and (args.packet or args.evidence_root):
        cli.error("--blank-packet cannot be combined with other arguments")
    if args.evidence_root and not args.packet:
        cli.error("--evidence-root requires --packet")
    if args.blank_packet:
        value=blank_packet()
    else:
        if args.packet:
            with open(args.packet,encoding="utf-8") as f:
                packet=json.load(f)
        else:
            packet=None
        value=handoff(packet,evidence_root=args.evidence_root)
    print(json.dumps(value,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
