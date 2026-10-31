"""B04/B05 source-legal noncombat core-check scene executor v0.

Runs the *canonical* ordinary noncombat core-check procedures against actual
L1-3 example character Abilities/learned Training. Authored fixed GM-stance
fixtures are demonstrations, NOT observations of an actual GM or human player.
No opposed social, Stealth contest, unapproved skill, progress clock, magical
access, automatic mission verdict, advancement, or Focus certification.
"""
import argparse
from functools import lru_cache
from importlib import import_module
import json

from scripts.b04_b07_independent_progression_audit_v0 import LOW_PRIEST
from scripts.b04_b07_twelve_focus_certification_protocol_v0 import roster
from scripts.b06_encounter_state_v0 import Encounter, party_actor, _fingerprint
from scripts.b06_damage_v0 import DamageState
from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest

LEVELS = (1, 2, 3)
ROLES = {
    "Priest/High": "H", "Priest/Medium": "M", "Priest/Low": "A",
    "Scholar/High": "F", "Scholar/Medium": "S", "Scholar/Low": "T",
    "Gifted/High": "G", "Gifted/Medium": "MG", "Gifted/Low": "GL",
    "Anointed/High": "AH", "Anointed/Medium": "AM", "Anointed/Low": "AL",
}
DOMAIN_POLICIES = {
    "exploration": ("balance", "survey"),
    "investigation": ("diagnose", "observe"),
    "social": ("petition", "document"),
}
# Authored GM *fixture* conditions, not universal skill/scene cost rules.
# The alternative genuinely changes the approach and which Ability/Training
# could apply to an otherwise narrow, achievable situation.
SCENES = {
    "exploration": {
        "balance": dict(ability="Agility", training="Acrobatics",
                        target_modifier=5, time_seconds=90,
                        premise="Cross a slippery narrow footbridge by balancing",
                        success="Crossing accomplished before the patrol",
                        failure="Crossing not completed before the patrol"),
        "survey": dict(ability="Awareness", training="Navigation",
                       target_modifier=2, time_seconds=180,
                       premise="Identify the safer marked line across the ford",
                       success="Usable route identified before the patrol",
                       failure="No safe line identified before the patrol"),
    },
    "investigation": {
        "diagnose": dict(ability="Intellect", training="Medicine",
                         target_modifier=2, time_seconds=240,
                         premise="Diagnose the signs of an ordinary spoiled herb batch",
                         success="Source of contamination identified",
                         failure="Source of contamination remains uncertain"),
        "observe": dict(ability="Awareness", training=None,
                        target_modifier=0, time_seconds=90,
                        premise="Search for visible staining on the stored herbs",
                        success="Visible stains noticed",
                        failure="Stains not noticed in the allotted search"),
    },
    "social": {
        "petition": dict(ability="Presence", training=None,
                         target_modifier=2, time_seconds=60,
                         premise="Ask a neutral storekeeper to show the public supply log",
                         success="Storekeeper agrees to show the public log",
                         failure="Storekeeper declines this request"),
        "document": dict(ability="Intellect", training="regional/era History",
                         target_modifier=2, time_seconds=120,
                         premise="Cite a known local public-record precedent to the storekeeper",
                         success="Storekeeper accepts the precedent and shows the public log",
                         failure="Precedent not established; log remains unavailable"),
    },
}
# Canonical Core Resolution ladder, not a new DC scale.
DIFFICULTY = {-3: 7, -1: 9, 0: 10, 2: 12, 5: 15, 8: 18, 10: 20}
ALLOWED_MODES = ("pressure", "passive", "safe_roll", "take10", "take20")
# These are SPECIFIC alternative fictional premises: no arbitrary safe
# retries at a pressured ford, contested NPC request, or pressured diagnosis.
SAFE_EFFORT = frozenset({("investigation", "observe")})
PASSIVE_NOTICE = frozenset({
    ("investigation", "observe"), ("exploration", "survey"),
})
# GM-authored safe investigation timing, not a universal Take20 multiplier.
SAFE_OBSERVE_SECONDS = {"safe_roll": 90, "take10": 90, "take20": 900}
SOURCE_ONLY = "AUTHORED_GM_FIXTURE_NOT_HUMAN_ADJUDICATION"
NO_CERTIFICATION = {
    "human_player_choices": 0,
    "externally_verified_gm_scenes": 0,
    "independently_certified_focuses": 0,
    "strict_mvp_exits_met": 0,
}


@lru_cache(maxsize=1)
def _sources():
    return {row["pairing"]: row for row in roster()}


def _character(pairing, level, *, low_variant):
    if type(pairing) is not str or pairing not in ROLES:
        raise ValueError("Unknown independent twelve-Focus pairing")
    if type(level) is not int or level not in LEVELS:
        raise ValueError("Only authored L1–3 levels")
    if pairing != "Priest/Low" and low_variant is not None:
        raise ValueError("Only Low Priest has physical A/B variant selection")
    if pairing == "Priest/Low":
        if low_variant not in ("A", "B"):
            raise ValueError("Low Priest must identify A or B physical variant")
        role = low_variant
    else:
        role = ROLES[pairing]
    actor = party_actor(role, level, "pilot", "party", occupied=((1, 1),))
    provenance = _sources()[pairing]
    if provenance["source_issues"]:
        raise ValueError("Source has unresolved structural audit issues")
    source_path = actor.source.path
    fingerprint = provenance["source_fingerprints"].get(source_path)
    if (fingerprint is None or actor.source.digest != fingerprint
            or _fingerprint(source_path) != fingerprint):
        raise ValueError("Native actor mismatches independently audited source")
    if pairing == "Priest/Low":
        # G0 physical A/B is NOT a full Low Priest character sheet. The
        # ability values are source-attested, but Learned Disciplines are not.
        source_abilities = dict(actor.source.abilities)
        expected = LOW_PRIEST[low_variant]["abilities"]
        keys = ("Strength", "Agility", "Precision", "Intellect",
                "Awareness", "Presence", "Vitality", "Veil Affinity",
                "Veil Control")
        if tuple(source_abilities[k] for k in keys) != expected:
            raise ValueError("Low Priest physical proxy abilities changed")
        return actor, source_abilities, {}, "LOW_PRIEST_G0_ABILITIES_ONLY"
    module = import_module("scripts." + source_path.split("/")[-1][:-3])
    p = module.profile(level)
    abilities, disciplines = p["abilities"], p["learned_disciplines"]
    if (dict(actor.source.abilities) != abilities
            or type(disciplines) is not dict):
        raise ValueError("Full pilot profile conflicts with sourced native actor")
    return actor, abilities, disciplines, "AUTHORED_COMPLETE_SOURCE_PROFILE"


def resolve_scene(pairing, level, domain, policy, *, face=12, mode="pressure",
                  low_variant=None, situational_modifier=0):
    """One independent preauthored fork; no synthetic GM/player endorsement.

    Time and plausible success/failure consequences are *explicit fixture
    premises*, not universal penalties or automatic Veil effects.
    """
    if type(domain) is not str or domain not in SCENES:
        raise ValueError("Only authored exploration/investigation/social fixtures")
    if type(policy) is not str or policy not in SCENES[domain]:
        raise ValueError("Only explicitly authored alternative approaches")
    if type(mode) is not str or mode not in ALLOWED_MODES:
        raise ValueError("Unsupported canonical core check mode")
    if type(situational_modifier) is not int or not -10 <= situational_modifier <= 10:
        raise ValueError("Explicit bounded fixture modifier required")
    if mode in ("pressure", "safe_roll"):
        if type(face) is not int or not 1 <= face <= 20:
            raise ValueError("Only an actual d20 result 1–20 is permitted")
    elif face is not None:
        raise ValueError("Passive/Take 10/Take 20 have no d20 face")
    actor, abilities, learned, source_status = _character(
        pairing, level, low_variant=low_variant)
    spec = SCENES[domain][policy]
    training_name = spec["training"]
    if training_name is not None and training_name in learned:
        rank = learned[training_name]
        if type(rank) is not int or not 0 <= rank <= 2:
            raise ValueError("Source Training rank outside L1–3 cap")
    else:
        rank = 0
    ability = abilities[spec["ability"]]
    if type(ability) is not int or not -2 <= ability <= 5:
        raise ValueError("Unrecognized source Ability modifier")
    # Do not mutate the same pressured encounter into a risk-free Take20.
    # The one explicitly safe sample is an unhurried, repeatable laboratory
    # observation without a serious failure consequence. Passive modes are
    # ordinary incidental noticing, not deliberate NPC persuasion.
    if mode in ("safe_roll", "take10", "take20") and (domain, policy) not in SAFE_EFFORT:
        raise ValueError("Safe effort requires the separately authored low-risk premise")
    if mode == "passive" and (domain, policy) not in PASSIVE_NOTICE:
        raise ValueError("Passive detection requires an authored natural-noticing premise")
    if mode == "pressure" or mode == "safe_roll":
        base = face
    else:
        base = 10 if mode in ("passive", "take10") else 20
    target = DIFFICULTY[spec["target_modifier"]]
    total = base + ability + rank + situational_modifier
    passed = total >= target
    # No universal noncombat natural-1 miss or natural-20 success.
    cost_seconds = (0 if mode == "passive" else
                    SAFE_OBSERVE_SECONDS[mode] if mode in SAFE_OBSERVE_SECONDS
                    else spec["time_seconds"])
    premise = (("Unhurried repeatable laboratory observation, no serious failure risk"
                if mode in SAFE_OBSERVE_SECONDS else
                "Notice an existing detail while passing, no deliberate search")
               if mode != "pressure" else spec["premise"])
    consequence = (("Found visible stains" if passed else
                     "No stains found during this chosen safe effort")
                   if mode in SAFE_OBSERVE_SECONDS else
                   ("Existing detail noticed" if passed else "Existing detail unnoticed")
                   if mode == "passive" else
                   spec["success"] if passed else spec["failure"])
    encounter = Encounter(
        [actor], {"pilot": 40}, seed=0,
        scenario="B04-B05-Canonical-Noncombat-Fixture-v0",
        policy=f"{domain}:{policy}:{mode}",
        objective="bounded_noncombat_check_not_human_GM_certification",
    )
    g4 = DamageState(encounter)
    if cost_seconds:
        g4.advance_exploration(cost_seconds)
    if encounter.g4.clock.world_seconds != cost_seconds:
        raise AssertionError("Source G4.2 exploration time was not committed")
    encounter.log(
        "b04_b05_noncombat_core_check_fixture",
        actor="pilot", actor_source=actor.source.path,
        source_sha256=actor.source.digest,
        pairing=pairing, level=level, variant=low_variant,
        domain=domain, policy=policy, mode=mode,
        ability=spec["ability"], ability_modifier=ability,
        training=training_name if rank else None, trained_rank=rank,
        situational_modifier=situational_modifier, face=face,
        base=base, total=total, target=target,
        success=passed, fixture_time_seconds=cost_seconds,
        outcome=consequence,
        gm_verdict="FIXED_AUTHOR_SCENARIO_NOT_AN_EXTERNAL_GM",
        strict_mvp_exits_met=0, independent_focus_certified=False,
    )
    encounter.check()
    return {
        "pairing": pairing, "level": level, "low_variant": low_variant,
        "domain": domain, "policy": policy, "mode": mode,
        "premise": premise,
        "ability": spec["ability"], "ability_modifier": ability,
        "training": training_name if rank else None, "trained_rank": rank,
        "situational_modifier": situational_modifier,
        "d20_face": face, "check_base": base, "total": total,
        "difficulty_modifier": spec["target_modifier"], "target": target,
        "success": passed, "consequence": consequence,
        "elapsed_seconds": encounter.g4.clock.world_seconds,
        "native_g42_event_count": len(encounter.ledger),
        "native_ledger_sha256": canonical_digest(encounter.ledger),
        "source_path": actor.source.path, "source_sha256": actor.source.digest,
        "source_scope": source_status, "status": SOURCE_ONLY,
        "human_choice_observed": False, "external_gm_adjudicated": False,
        "independent_focus_certified": False, "strict_mvp_exits_met": 0,
    }


def matrix():
    rows = []
    for pairing in sorted(ROLES):
        for level in LEVELS:
            for domain, policies in DOMAIN_POLICIES.items():
                for policy in policies:
                    rows.append(resolve_scene(
                        pairing, level, domain, policy,
                        low_variant="A" if pairing == "Priest/Low" else None,
                    ))
    if len(rows) != 216:
        raise AssertionError("Expected 12 x 3 x 3 x 2 bounded core-check forks")
    return {
        "focus_pairings": 12, "pairing_level_slots": 36,
        "domains": list(DOMAIN_POLICIES),
        "mechanically_resolved_fixed_fixtures": len(rows),
        "low_priest_ability_only_fixtures": sum(
            r["pairing"] == "Priest/Low" for r in rows),
        "full_low_priest_noncombat_certificates": 0,
        **NO_CERTIFICATION, "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairing", choices=sorted(ROLES))
    parser.add_argument("--level", type=int)
    parser.add_argument("--domain", choices=sorted(SCENES))
    parser.add_argument("--policy", type=str)
    parser.add_argument("--low-variant", choices=("A", "B"))
    parser.add_argument("--mode", choices=ALLOWED_MODES, default="pressure")
    parser.add_argument("--face", type=int, default=None)
    args = parser.parse_args()
    subset = [args.pairing, args.level, args.domain, args.policy]
    if any(x is not None for x in subset):
        if not all(x is not None for x in subset):
            parser.error("pairing, level, domain and policy are all required")
        value = resolve_scene(
            args.pairing, args.level, args.domain, args.policy,
            low_variant=args.low_variant, mode=args.mode,
            face=(12 if args.face is None and args.mode in ("pressure", "safe_roll")
                  else args.face),
        )
    else:
        if args.face is not None or args.low_variant is not None or args.mode != "pressure":
            parser.error("single-scene options require all four selector fields")
        value = matrix()
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
