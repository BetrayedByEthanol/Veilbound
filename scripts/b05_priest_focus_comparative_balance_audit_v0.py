"""B04/B05 L1-3 Priest Focus comparison: sourced arithmetic + bounded M receipts.

This is an audit, not three opposed character pilots. High Priest has a
canonical rules profile but no source-built High Priest Life encounter actor;
Low A is a physical G0 proxy plus separate documented Rite/Exaltation tests.
Never convert modeled access/capacity into certified effectiveness.
"""
import argparse
from hashlib import sha256
from copy import deepcopy
import json

from scripts.b05_medium_priest_life_l1_l3_v0 import profile as medium_profile
from scripts.b06_encounter_state_v0 import ROOT, party_actor
from scripts.b05_medium_life_encounter_balance_v0 import run_matrix
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

LEVELS = (1, 2, 3)
FOCUSES = ("High", "Medium", "Low")
RATES = {
    "High": {"vp": 6, "physical": 30, "projection": 20, "regen": 1,
             "prepared": (3, 4, 4)},
    "Medium": {"vp": 4, "physical": 24, "projection": 24, "regen": 2,
               "prepared": (2, 3, 3)},
    "Low": {"vp": 2, "physical": 20, "projection": 30, "regen": 3,
            "prepared": (1, 2, 2)},
}
REFERENCE = {"veil_affinity": 0, "vitality": 2, "accord": 1,
             "hp_max": 12, "pillar": "Life"}
SOURCE_PATHS = (
    "docs/rules/08-archetypes/priest.md",
    "docs/rules/07-veil-magic/volition-points.md",
    "docs/rules/05-combat/action-categories-and-physical-tempo.md",
    "docs/rules/06-vigor-wounds-death/hp-and-vigor.md",
    "docs/rules/07-veil-magic/basic-heal-v0.md",
    "docs/rules/07-veil-magic/guided-regeneration-v0.md",
    "docs/rules/07-veil-magic/vital-shelter-v0.md",
    "docs/rules/10-advancement/talents-level-1-5-v0.md",
    "docs/design/b05-life-low-priest-l3-build-exaltation-verification-v0.md",
    "docs/design/b04-b05-medium-priest-life-l1-l3-encounter-integration-balance-verification-v0.md",
    "scripts/b05_medium_priest_life_l1_l3_v0.py",
    "scripts/b05_medium_life_encounter_balance_v0.py",
    "scripts/b06_encounter_state_v0.py",
    "scripts/b06_hunter_party_exchanges_v0.py",
)
# Match the actual price-bearing DECLARATIONS, not just feature labels or
# incidental examples elsewhere in the same document. A same-length price
# replacement must fail closed before modeled witnesses can be attested.
REQUIRED_RULES = {
    SOURCE_PATHS[0]: (
        "High **4/5/5**, Medium **3/4/4**, Low **2/3/3**",
        "- pays the **full normal technique VP** plus **1 additional Spent VP Invocation Surcharge**,",
        "- **levels 1–4: one Full Action**,",
        "**level 5+:** the technique's normal action while still paying +1 Spent VP;",
        "This **+1 surcharge is a provisional L1–3 playtest value**.",
        "Intercession = 2 Spent VP",
        "- costs one **General Tempo Action (24 AP)**;",
        "**2 Committed + 1 Spent VP**",
        "**−1 Committed VP, minimum 1**",
        "**2→1 Committed VP**",
    ),
    SOURCE_PATHS[1]: (
        "High Focus:** `max(1, 6 + Veil Affinity) × Level`",
        "Medium Focus:** `max(1, 4 + Veil Affinity) × Level`",
        "Low Focus:** `max(1, 2 + Veil Affinity) × Level`",
        "VP Recovery = 25% of Max VP",
    ),
    SOURCE_PATHS[2]: (
        "30 + 6 × (Level - 1)",
        "| **High — Projection** | 30 AP | 20 AP | 24 AP |",
        "| **Medium — Routing** | 24 AP | 24 AP | 24 AP |",
        "| **Low — Embodiment** | 20 AP | 30 AP | 24 AP |",
    ),
    SOURCE_PATHS[3]: (
        "Regeneration throughput = max(Vitality, 0) + Focus Rate",
        "High Focus: +1", "Medium Focus: +2", "Low Focus: +3",
    ),
    SOURCE_PATHS[4]: (
        "| Primary activation | **One Projection Action**, paid High **20 AP**, Medium **24 AP**, Low **30 AP** |",
        "| Primary VP | **2 × T Spent VP** for the attempted spell |",
    ),
    SOURCE_PATHS[5]: (
        "| Ordinary activation | **One Projection Action** on caster's own turn: High **20 AP**, Medium **24 AP**, Low **30 AP**",
        "| Maintained mode | **2 Committed VP**;",
        "| Benefit | **+1 throughput** at beneficiary's **existing once-per-own-turn Regeneration Step**",
        "with a **separate +1 Spent VP surcharge**.",
    ),
    SOURCE_PATHS[6]: (
        "| Ordinary activation | **One own-turn Focus-priced Projection Action**, High **20**, Medium **24**, Low **30 Turn AP**;",
        "| Maintained mode — Primary | **2 Committed VP + 1 ordinary Spent VP**;",
        "| Primary initial prevention budget | **B = 8 + max(0, caster Veil Control)**;",
    ),
    SOURCE_PATHS[7]: (
        "### TAL-M03 — Frugal Technique",
        "with a normal **Spent VP component of at least 2** costs **1 fewer Spent VP**",
    ),
}


def verify_basis():
    """Pin price-bearing declarations AND hash actual source bytes for replay.

    The source hash is part of the signed report itself: editing a source
    without changing character count still changes audit_sha256 and makes an
    earlier attestation fail. Price changes must additionally fail closed
    instead of simply reissuing the stale numerical payment witness.
    """
    evidence={}
    for path in SOURCE_PATHS:
        raw=(ROOT / path).read_bytes()
        contents=raw.decode("utf-8")
        for needle in REQUIRED_RULES.get(path, ()):
            if contents.count(needle)!=1:
                raise AssertionError(
                    f"Rule changed or duplicate declaration; review audit: {path}: {needle}")
        evidence[path]={
            "present":True,
            "chars":len(contents),
            "sha256":sha256(raw).hexdigest(),
        }
    return evidence


def _half_up_quarter(value):
    # VP Recovery uses exact positive 25% and half-up, not Python bankers rounding.
    return max(1,(value+2)//4)


def row(focus, level, *, accord=1, talent_bonus=0):
    """Normalize to VA0/VIT2 so Focus, not unrelated stat buys, varies."""
    if focus not in FOCUSES or type(level) is not int or level not in LEVELS:
        raise ValueError("Only canonical Priest Focuses at levels 1-3")
    if type(accord) is not int or not -3<=accord<=3:
        raise ValueError("Pillar Accord must be an integer from -3 to +3")
    if type(talent_bonus) is not int or talent_bonus not in (0,1):
        raise ValueError("Only no extra capacity or TAL-P01 +1 is modeled")
    r=RATES[focus]
    ap=30+6*(level-1)
    vp=max(1,r["vp"]+REFERENCE["veil_affinity"])*level
    base=r["prepared"][level-1]
    effective=max(1,base+accord+talent_bonus)
    return {
        "focus":focus, "level":level, "accord":accord,
        "vp_max":vp, "six_hour_vp_recovery":_half_up_quarter(vp),
        "hp_max":REFERENCE["hp_max"],
        "vigor_max":REFERENCE["hp_max"]*level,
        "base_regen":max(0,REFERENCE["vitality"])+r["regen"],
        "turn_ap":ap, "physical_ap":r["physical"],
        "projection_ap":r["projection"], "general_ap":24,
        "physical_tempo":ap//r["physical"],
        "projection_tempo":ap//r["projection"],
        "normal_guard_capacity":ap//r["physical"],
        "mixed_physical_projection_in_one_turn":
            r["physical"]+r["projection"]<=ap,
        "base_prepared_capacity":base,
        "effective_prepared_capacity":effective,
        "normal_basic_heal_t1_cost_spent_vp":2,
        "max_unsubsidized_t1_basic_heal_by_vp":vp//2,
        "normal_guided_maintained_committed":2,
        "normal_shelter_committed":2,
        "normal_shelter_establishment_spent":1,
        "normal_shelter_initial_budget":8,  # reference VC0; source spell
        "independent_full_focus_certified":False,
        "source_basis":"canonical_focus_rules_normalized_va0_vit2",
    }


def _crosscheck_real_characters(rows):
    medium={}
    low={}
    for level in LEVELS:
        native=medium_profile(level)
        m=rows["Medium"][level-1]
        must={
            "hp_max":m["hp_max"],"vigor_max":m["vigor_max"],
            "vp_max":m["vp_max"],"turn_ap":m["turn_ap"],
            "physical_action_ap":m["physical_ap"],
            "projection_action_ap":m["projection_ap"],
            "prepared_capacity":m["effective_prepared_capacity"],
            "active_consecration_cap":1,
        }
        for key,value in must.items():
            if native[key]!=value:
                raise AssertionError(f"M L{level} source mismatch at {key}")
        if native["normal_regen_throughput"] != m["base_regen"]+1:
            raise AssertionError("M TAL-C02 is selected, not a Focus bonus")
        if "Basic Heal" not in native["prepared_prayers"]:
            raise AssertionError("M selected Life repertoire drifted")
        medium[level]={
            "source":"scripts/b05_medium_priest_life_l1_l3_v0.py",
            "selected_talent_regen_bonus":1,
            "total_regen":native["normal_regen_throughput"],
            "selected_prepared":list(native["prepared_prayers"]),
            "selected_talents":list(native["talents"]),
        }
        a=party_actor("A",level,f"low-{level}","party",occupied=((1,1),))
        l=rows["Low"][level-1]
        for key,expected in (("hp_max",l["hp_max"]),
                             ("vigor_max",l["vigor_max"]),
                             ("vp_max",l["vp_max"]),
                             ("ap_total",l["turn_ap"]),
                             ("physical_ap",l["physical_ap"]),
                             ("projection_ap",l["projection_ap"])):
            if getattr(a,key)!=expected:
                raise AssertionError(f"Low A physical proxy differs at {key}")
        if a.regen!=l["base_regen"]+1:
            raise AssertionError("Low A TAL-C02 is a selected extra throughput")
        low[level]={
            "source":a.source.path, "source_digest":a.source.digest,
            "source_status":a.source.status,
            "selected_talent_regen_bonus":1,
            "total_regen":a.regen,
            "chosen_guided_commitment":1,  # authored -1, minimum 1
            "one_active_rite_cap":1,
            "full_priest_spell_runtime_certified":False,
        }
    return {"Medium":medium,"Low":low}


def _prayer_cost_witnesses(rows):
    """Payment and timing examples, not arbitrary outcomes or hit chances."""
    out=[]
    for focus in FOCUSES:
        for level in LEVELS:
            r=rows[focus][level-1]
            # One T1 projected Basic Heal from genuinely prepared Life access;
            # no assumption of a suitable target, working hand or free action.
            out.append({
                "focus":focus,"level":level,
                "prepared_basic_heal": {
                    "projection_ap":r["projection_ap"],
                    "spent_vp":2,
                    "available_after_from_full":r["vp_max"]-2,
                    "affordable_from_full":r["vp_max"]>=2,
                    "separate_physical_action_same_turn":
                        r["mixed_physical_projection_in_one_turn"],
                },
                "maintained_guided_on_self": {
                    "projection_ap":r["projection_ap"],
                    "committed_vp":1 if focus=="Low" else 2,
                    "chosen_rite_only":focus=="Low",
                    "affordable_from_full":r["vp_max"] >=
                        (1 if focus=="Low" else 2),
                    "selected_legal_access_not_assumed":True,
                },
                "unprepared_life_basic_heal_open_invocation":
                    ({"full_action_ap":r["turn_ap"],
                      "normal_spent_vp":2,"surcharge_spent_vp":1,
                      "total_spent_vp":3,
                      "affordable_from_full":r["vp_max"]>=3,
                      "may_invoke_only_if_authored_eligible_unprepared":True}
                     if focus=="High" else None),
            })
    return out


def _encounter_evidence(seed):
    """Consume the already tested M-only 27-cell native G5/G4.5/G4 matrix."""
    native=run_matrix(seed=seed)
    if native["policy_count"]!=27 or len(native["trials"])!=27:
        raise AssertionError("Native Medium encounter matrix unexpectedly changed")
    cells={(x["level"],x["opponent"],x["policy"]):x
           for x in native["trials"]}
    if len(cells)!=27:
        raise AssertionError("Duplicate policy cell")
    pairs=[]
    for opponent in ("soldier","sentry_prepared"):
        direct=("guided","shelter")
        for strategy in direct:
            source=cells[3,opponent,strategy]
            if strategy=="shelter" and opponent=="soldier":
                continue
            ext=strategy+"_intercession"
            indirect=cells[3,opponent,ext]
            a,b=source["metrics"],indirect["metrics"]
            if (a["ally_hp"],a["ally_vigor"]) != (b["ally_hp"],b["ally_vigor"]):
                raise AssertionError("Intercession must not be mislabeled equivalent")
            if (b["intercession_reactions"]!=2 or
                    b["priest_vp"][2]-a["priest_vp"][2]!=4 or
                    b["priest_vp"][1]!=a["priest_vp"][1]):
                raise AssertionError("Paired 2-Reaction/4-Spent benchmark changed")
            pairs.append({
                "opponent":opponent,"effect":strategy,
                "same_ally_hp_vigor_for_fixed_policy":True,
                "extra_spent_vp":4,"extra_reactions":2,
                "ledger_sha256_direct":source["ledger_sha256"],
                "ledger_sha256_interceded":indirect["ledger_sha256"],
                "provisional_cost_accepted":False,
            })
    return {
        "source":"scripts/b05_medium_life_encounter_balance_v0.py",
        "policy_count":native["policy_count"],
        "native_policy_cells":deepcopy(native["trials"]),
        "l3_direct_vs_intercession_pairs":pairs,
        "native_medium_only":True,
        "low_and_high_opposed_cohorts":None,
        "sampled_win_rate":None,"confidence_interval":None,
        "balance_price_approved":False,
    }


def audit(*,seed=0):
    if type(seed) is not int or seed<0:
        raise ValueError("Source seed must be a nonnegative integer")
    basis=verify_basis()
    rows={f:[row(f,level) for level in LEVELS] for f in FOCUSES}
    sources=_crosscheck_real_characters(rows)
    witness=_prayer_cost_witnesses(rows)
    evidence=_encounter_evidence(seed)
    report={
        "version":"B04-B05-Priest-Focus-Comparative-Balance-Audit-v0",
        "seed":seed, "reference":dict(REFERENCE),
        "source_files":basis,
        "focus_progression":rows,
        "selected_source_witnesses":sources,
        "priced_actions":witness,
        "native_medium_encounter":evidence,
        "high_priest_life_complete_character":None,
        "high_priest_life_native_encounter":None,
        "low_priest_life_full_spell_encounter":None,
        "mvp_focus_certifications_added":0,
        "open_numerical_decisions":[
            "High Open Invocation +1 Spent VP surcharge",
            "High/Medium/Low starting capacity balance at Accord +1",
            "Medium L3 Intercession 2 Spent VP plus Reaction",
            "Low Chosen Rite/Exaltation relative support cost",
            "Miracle Petition probability and six-hour recovery pacing",
        ],
        "comparison_is_measured_three_focus_balance":False,
        "certify_representative_priest_encounter":False,
        "sampled_win_rate":None,
    }
    report["audit_sha256"]=canonical_digest(report)
    return report


def attest(report,*,seed=0):
    if not isinstance(report,dict):
        raise AssertionError("Comparison audit must be a complete dict")
    digest=report.get("audit_sha256")
    if canonical_digest({k:v for k,v in report.items()
                         if k!="audit_sha256"})!=digest or report!=audit(seed=seed):
        raise AssertionError("Comparison audit failed independent source replay")
    return deepcopy(report)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args()
    print(json.dumps(audit(seed=args.seed),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
