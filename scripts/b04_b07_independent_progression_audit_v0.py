"""Independent B04/B07 L1–3 structural and progression audit, NOT Focus play certification.

Checks selected published sheets against *separate* creation, award and
resource invariants. Never invokes a source module's self-verify() helper,
counts authored tactical fixtures as independent tests, invents Talent
choices, or grants an adventure milestone automatically.
"""
from copy import deepcopy
from hashlib import sha256
from importlib import import_module
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LEVELS = (1, 2, 3)
ABILITY_COST = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 5, 3: 7, 4: 10}
ABILITIES = ("Strength", "Agility", "Precision", "Intellect", "Awareness",
             "Presence", "Vitality", "Veil Affinity", "Veil Control")
TALENT_AWARDS = {"High": (1,), "Medium": (1, 3), "Low": (1, 2, 3)}
VP_PER_LEVEL = {"High": 6, "Medium": 4, "Low": 2}
# Canonical action-categories-and-physical-tempo.md: one shared Turn AP
# pool, with Focus-specific prices. Never derive prices from audited sheets.
FOCUS_ACTION_COSTS = {
    "High": (30, 20, 24),
    "Medium": (24, 24, 24),
    "Low": (20, 30, 24),
}
# scholar.md, L1–3 individual repertoire and preparation limits. None
# denotes L3 Formula Fluency (no required prepared-formula list).
SCHOLAR_KNOWN = {
    "High": (5, 6, 6), "Medium": (4, 5, 5), "Low": (3, 4, 4),
}
SCHOLAR_FORMULAS = (1, 2, None)
SCHOLAR_LOW_PREPARED = (2, 3, 3)
# priest.md: base *before* Accord and explicitly acquired TAL-P01.
PRIEST_BASE_PREPARED = {
    "High": (3, 4, 4), "Medium": (2, 3, 3), "Low": (1, 2, 2),
}
SOURCE_MODULES = {
    "Priest/High": "b05_high_priest_life_l1_l3_v0",
    "Priest/Medium": "b05_medium_priest_life_l1_l3_v0",
    "Scholar/High": "b05_high_scholar_fire_l1_l3_v0",
    "Scholar/Medium": "b05_medium_scholar_l1_l3_v0",
    "Scholar/Low": "b05_low_scholar_l1_l3_v0",
    "Gifted/High": "b05_high_gifted_l1_l3_v0",
    "Gifted/Medium": "b05_medium_gifted_l1_l3_v0",
    "Gifted/Low": "b05_low_gifted_l1_l3_v0",
    "Anointed/High": "b05_high_anointed_restoration_l1_l3_v0",
    "Anointed/Medium": "b05_medium_anointed_restoration_l1_l3_v0",
    "Anointed/Low": "b05_low_anointed_restoration_l1_l3_v0",
}
# Low Priest has two authored A/B choices rather than a unified profile().
# Those source G0 characters are *physical proxies*, not full build sheets.
LOW_PRIEST = {
    "A": {"abilities": (2, 3, 0, 0, 1, -2, 2, 0, 0),
          "weapon": "Sword", "hp": 12,
          "talents": ("TAL-C02", "TAL-C05", "TAL-C10")},
    "B": {"abilities": (2, 2, 0, 1, 0, -2, 3, 0, 0),
          "weapon": "Mace", "hp": 13,
          "talents": ("TAL-C05", "TAL-C01", "TAL-C09")},
}
CATALOGUE = "docs/rules/10-advancement/talents-level-1-5-v0.md"
LOW_RECORD = "docs/design/b05-life-low-priest-l3-build-exaltation-verification-v0.md"


def _sha(path):
    return sha256((ROOT / path).read_bytes()).hexdigest()


def _issue(issues, code, *, level, detail):
    issues.append({"code": code, "level": level, "detail": detail})


def talent_minimums():
    """Read actual authored Talent IDs and minimum levels, not source claims."""
    text = (ROOT / CATALOGUE).read_text(encoding="utf-8")
    found = re.findall(r"^### (TAL-[A-Z]\d{2})[^\n]*\n\*\*L (\d+)\b",
                       text, flags=re.MULTILINE)
    if len(found) != 32 or len({name for name, _ in found}) != 32:
        raise ValueError("B07 catalogue identity/gate shape changed; re-audit")
    return {name: int(lvl) for name, lvl in found}


def _sheet_issues(pairing, level, sheet, first, prior, gates):
    """Independent policy checks; does not call profile.verify()."""
    issues = []
    archetype, focus = pairing.split("/")
    def check(ok, code, message):
        if not ok:
            _issue(issues, code, level=level, detail=message)
    check(sheet.get("archetype") == archetype and sheet.get("focus") == focus
          and sheet.get("level") == level, "identity", "Wrong build identity/level")
    abilities = sheet.get("abilities", {})
    check(set(abilities) == set(ABILITIES), "abilities", "Nine named abilities required")
    ability_valid = (set(abilities) == set(ABILITIES)
                     and all(type(n) is int and n in ABILITY_COST
                             for n in abilities.values()))
    if ability_valid:
        points = sum(ABILITY_COST[n] for n in abilities.values())
        check(points == 28, "ability_budget", "L1 creation must spend 28 points")
        if "ability_points" in sheet:
            check(sheet["ability_points"] == points, "ability_total", "Reported ability budget differs")
        if prior:
            check(abilities == prior["abilities"], "early_ability_increase",
                  "No Ability increase at L2/L3")
    else:
        check(False, "ability_budget", "Unknown ability allocation/cost")

    learned = sheet.get("learned_disciplines", {})
    check(isinstance(learned, dict) and
          all(type(n) is int and 0 <= n <= 2 for n in learned.values()),
          "learned_ranks", "L1–3 direct-invested discipline rank maximum +2")
    if isinstance(learned, dict):
        check(sum(learned.values()) == 8 + int(level >= 2),
              "learned_budget", "Eight at creation; one point at L2, none at L3")
        if "learned_points" in sheet:
            check(sheet["learned_points"] == sum(learned.values()),
                  "learned_total", "Reported learned points differ")
        if prior:
            delta = {key: learned.get(key, 0)-prior["learned_disciplines"].get(key, 0)
                     for key in set(learned) | set(prior["learned_disciplines"])}
            check(all(x >= 0 for x in delta.values())
                  and sum(delta.values()) == int(level == 2),
                  "learned_progression", "Only one eligible L2 point; no free L3 change")
    weapon = sheet.get("weapon_training", {})
    check(isinstance(weapon, dict) and
          sum(weapon.values()) == 2 and all(type(v) is int and 0 <= v <= 2
                                            for v in weapon.values()),
          "weapon_budget", "Two independent direct Weapon Development points")
    if isinstance(weapon, dict):
        if "weapon_development_points" in sheet:
            check(sheet["weapon_development_points"] == 2,
                  "weapon_total", "Incorrect source Weapon Development account")
        if prior:
            check(weapon == prior["weapon_training"], "early_weapon_increase",
                  "No Weapon Development award before L4")

    gear = (sheet.get("equipment_sp") or sheet.get("starting_equipment_sp"))
    if not isinstance(gear, dict):
        check(False, "equipment", "No sourced starting equipment ledger")
    else:
        price = sum(gear.values())
        remainder = next((sheet[k] for k in ("silver_remaining", "silver_remaining_sp",
                                            "starting_silver_left") if k in sheet), None)
        check(all(type(v) is int and v >= 0 for v in gear.values())
              and price <= 150 and remainder == 150-price, "equipment_budget",
              "Starting purchases and retained silver must reconcile to 150 sp")
        if prior:
            old = prior.get("equipment_sp") or prior.get("starting_equipment_sp")
            check(gear == old, "free_level_equipment",
                  "No free gear award at pilot milestones")

    vit = abilities.get("Vitality")
    aff = abilities.get("Veil Affinity")
    if type(vit) is int and type(aff) is int:
        hp = 10 + vit
        check(sheet.get("hp_max") == hp
              and sheet.get("vigor_max") == hp * level,
              "hp_vigor", "HP constant at L1–3; Max Vigor scales by level")
        # Explicit Deep Volition Reserve would modify this; none of the
        # selected 12 source builds acquires that Talent in this pilot.
        check(sheet.get("vp_max") == max(1, VP_PER_LEVEL[focus] + aff) * level,
              "vp_formula", "Max VP depends on Focus, Veil Affinity and level")
    check(sheet.get("turn_ap") == 30 + 6 * (level-1),
          "turn_ap", "L1/L2/L3 ordinary Turn AP must be 30/36/42")
    physical_ap, projection_ap, general_ap = FOCUS_ACTION_COSTS[focus]
    check((sheet.get("physical_action_ap"), sheet.get("projection_action_ap"))
          == (physical_ap, projection_ap), "focus_action_cost",
          "Focus Physical/Projection AP must match canonical 30/20, 24/24, 20/30")
    if "general_action_ap" in sheet:
        check(sheet["general_action_ap"] == general_ap,
              "general_action_cost", "General Tempo Action costs 24 AP at all Focuses")
    # Tempo is evaluated against the independent canonical price, even if
    # a forged source changes BOTH its price and its matching derived tempo.
    if sheet.get("physical_tempo") is not None:
        check(sheet["physical_tempo"] ==
              (30 + 6*(level-1)) // physical_ap,
              "physical_tempo", "Physical Tempo from canonical Focus AP")
    if sheet.get("projection_tempo") is not None:
        check(sheet["projection_tempo"] ==
              (30 + 6*(level-1)) // projection_ap,
              "projection_tempo", "Projection Tempo from canonical Focus AP")

    universals = (sheet.get("universals") if "universals" in sheet
                  else sheet.get("universal"))
    check(universals is not None and
          set(universals) == ({"Veil Inspection", "Blink"} if level == 3
                              else {"Veil Inspection"})
          and len(universals) == (2 if level == 3 else 1),
          "universal_award", "Inspection L1, Blink L3; no fabricated access")
    tier = sheet.get("tier_ceiling", sheet.get("max_used_tier"))
    check(tier == (2 if level == 3 else 1),
          "tier_ceiling", "No Tier-2 ordinary technique before L3")
    if "movement_points" in sheet:
        check(sheet["movement_points"] == 12, "movement", "Ordinary MP 12")

    talents = sheet.get("talents", [])
    ids = [re.match(r"^(TAL-[A-Z]\d{2})\b", str(t)) for t in talents]
    selected = [v.group(1) for v in ids if v]
    check(len(selected) == len(talents) and len(set(selected)) == len(selected),
          "talent_identity", "Selected Talent IDs must be unique catalogue entries")
    check(all(t in gates and gates[t] <= level for t in selected),
          "talent_gate", "Selected Talent must exist and meet its minimum level")
    awarded = sum(n <= level for n in TALENT_AWARDS[focus])
    check(len(selected) <= awarded, "talent_overaward",
          "More selected Talents than Focus's earned awards")
    # An unspent earned selection is LEGAL in B07, but these source sheets
    # do not explicitly account for an actual saved/available award.
    if len(selected) < awarded:
        saved = sheet.get("saved_talent_selections")
        check(saved == awarded-len(selected), "talent_unaccounted",
              "No explicit saved-selection ledger for earned unused Talent")
    if prior:
        old = [re.match(r"^(TAL-[A-Z]\d{2})\b", str(t)).group(1)
               for t in prior.get("talents", [])]
        check(set(old) <= set(selected), "talent_retraining",
              "No free Talent replacement/retraining at L2–3")
    # Only an eligible, nonduplicated selection within the earned Focus
    # awards can modify a native repertoire limit. Missing/saved choices
    # and invented extra Talents do not enlarge it.
    valid_selection = (len(selected) == len(talents)
                       and len(set(selected)) == len(selected)
                       and len(selected) <= awarded
                       and all(t in gates and gates[t] <= level for t in selected))
    if archetype == "Scholar":
        known = sheet.get("known_pillar_techniques", ())
        expanded = int(valid_selection and "TAL-S01" in selected)
        known_cap = SCHOLAR_KNOWN[focus][level-1] + expanded
        check(sheet.get("known_capacity") == known_cap
              and len(known) <= known_cap and len(set(known)) == len(known),
              "scholar_known_capacity",
              "Independent known count; only earned TAL-S01 adds one")
        if prior:
            check(set(prior["known_pillar_techniques"]) <= set(known),
                  "scholar_level_access", "No forgotten known technique on level award")
        if focus == "High":
            formulas = sheet.get("prepared_composite_formulas", ())
            formula_cap = SCHOLAR_FORMULAS[level-1]
            if formula_cap is None:
                # Formula Fluency removes the preparation requirement at L3.
                # No invented numeric prepared-formula allowance exists.
                check(sheet.get("formula_fluency") is True
                      and sheet.get("prepared_formula_capacity") in (None, 0),
                      "scholar_formula_capacity",
                      "L3 Formula Fluency has no required prepared-formula slots")
            else:
                check(sheet.get("prepared_formula_capacity") == formula_cap
                      and len(formulas) <= formula_cap,
                      "scholar_formula_capacity",
                      "High formula cap is 1 at L1 and 2 at L2; no Talent adds slots")
            check(len({json.dumps(f, sort_keys=True) for f in formulas})
                  == len(formulas) and
                  all(f.get("primary") in known and f.get("secondary") in known
                      for f in formulas),
                  "scholar_formula_legality",
                  "Formulas must be unique and use genuinely known components")
        elif focus == "Medium":
            check(sheet.get("prepared_technique_subset") is None
                  and sheet.get("prepared_capacity") is None,
                  "scholar_medium_preparation",
                  "Medium Scholar has no general prepared-technique limit")
        else:
            prepared = sheet.get("prepared_techniques", ())
            prepared_cap = SCHOLAR_LOW_PREPARED[level-1]
            check(sheet.get("prepared_capacity") == prepared_cap
                  and len(prepared) <= prepared_cap
                  and len(set(prepared)) == len(prepared)
                  and set(prepared) <= set(known),
                  "scholar_preparation_capacity",
                  "Low prepared cap is 2/3/3; subset of known; no Talent adds slots")
    if archetype == "Priest":
        prayer = sheet.get("prepared_prayers", ())
        accord = sheet.get("accord")
        # These published L1–3 pilot snapshots start at Accord +1 and do
        # not attest a later GM or Petition change. A source-only larger
        # Accord is not independent permission for extra slots.
        check(type(accord) is int and accord == first.get("accord") == 1,
              "priest_accord_provenance",
              "Starting Accord +1 carried without an authenticated change")
        effective = max(1, PRIEST_BASE_PREPARED[focus][level-1]
                        + (accord if type(accord) is int else 0)
                        + int(valid_selection and "TAL-P01" in selected))
        check(sheet.get("prepared_capacity") == effective,
              "priest_capacity",
              "Independent base + actual Accord + earned TAL-P01 capacity")
        open_slots = sheet.get("open_prayer_slots", 0)
        check(type(open_slots) is int and 0 <= open_slots
              <= int(focus == "High" and level == 3)
              and len(prayer)+open_slots <= effective
              and len(set(prayer)) == len(prayer),
              "priest_preparation",
              "Chosen-Pillar prayers, optional High L3 Open slot, within real cap")
    if archetype == "Gifted":
        links = sheet.get("emotion_aspect_links", {})
        check(len(links) == 8 and
              set(links) == set(sheet.get("authored_linked_techniques", {})),
              "gifted_links", "Eight authored Emotion/Aspect links")
        if prior:
            check(links == prior["emotion_aspect_links"], "gifted_link_mutation",
                  "No free re-binding of eight linked Aspects at level award")
    if archetype == "Anointed":
        check(sheet.get("bond_active") is True and
              sheet.get("signature") == "Returning Step"
              and sheet.get("max_destiny") == 2
              and sheet.get("destiny_initial_at_creation_only") == 2,
              "anointed_bond", "One Restoration bond, fixed Signature and Destiny cap")
        if prior:
            check(sheet.get("bond") == prior.get("bond")
                  and sheet.get("mission") == prior.get("mission"),
                  "anointed_bond_mutation", "Level award does not replace bond/mission")
    return issues


def _low_priest_issues(role, level, actor, gates):
    """Cross-check actual A/B G0 proxy against the separately authored build record."""
    spec = LOW_PRIEST[role]
    issues = []
    def check(condition, code, detail):
        if not condition:
            _issue(issues, code, level=level, detail=detail)
    values = dict(zip(ABILITIES, spec["abilities"]))
    check(sum(ABILITY_COST[n] for n in values.values()) == 28,
          "ability_budget", "Documented A/B creation allocation")
    check(actor.source.source_id == role
          and actor.source.path == "scripts/b06_hunter_party_exchanges_v0.py"
          and actor.source.digest == _sha(actor.source.path),
          "low_source", "Exact actual G0 A/B physical proxy identity")
    check((actor.level, actor.focus, actor.hp_max, actor.vigor_max, actor.vp_max)
          == (level, "Low", spec["hp"], spec["hp"]*level, 2*level),
          "low_resources", "Documented A/B HP, Vigor and Focus VP")
    check((actor.ap_total, actor.physical_ap, actor.projection_ap)
          == (30+6*(level-1), 20, 30), "low_ap", "Actual A/B AP tempo")
    chosen = spec["talents"][:level]
    check(len(chosen) == level and all(gates[name] <= n
                                     for n, name in enumerate(chosen, 1)),
          "low_talents", "Documented A/B selected three Talent award levels")
    check(dict(actor.source.equipment).get(spec["weapon"]) == "wielded",
          "low_weapon", "Documented A/B physical weapon sourced in G0")
    return issues


def audit():
    """Independent static progression receipts; certificate count intentionally zero."""
    gates = talent_minimums()
    pairings = {}
    for pairing, module_name in SOURCE_MODULES.items():
        path = "scripts/" + module_name + ".py"
        make = import_module("scripts." + module_name).profile
        sheets = [make(n) for n in LEVELS]
        faults = []
        for i, sheet in enumerate(sheets):
            faults.extend(_sheet_issues(pairing, LEVELS[i], sheet, sheets[0],
                                        sheets[i-1] if i else None, gates))
        pairings[pairing] = {
            "variants": 1, "levels_checked": 3, "source": path,
            "source_sha256": _sha(path), "issues": faults,
            "full_focus_certified": False}
    from scripts.b06_encounter_state_v0 import party_actor
    low_results = []
    for role in ("A", "B"):
        actor_issues = []
        for level in LEVELS:
            actor = party_actor(role, level, "audit-"+role, "party",
                                occupied=((1,1),))
            actor_issues.extend(_low_priest_issues(role, level, actor, gates))
        low_results.append({"variant": role, "issues": actor_issues})
    pairings["Priest/Low"] = {
        "variants": 2, "levels_checked": 3,
        "source": "scripts/b06_hunter_party_exchanges_v0.py",
        "source_sha256": _sha("scripts/b06_hunter_party_exchanges_v0.py"),
        "build_record": LOW_RECORD, "build_record_sha256": _sha(LOW_RECORD),
        "issues": [dict(issue, variant=entry["variant"])
                   for entry in low_results for issue in entry["issues"]],
        "full_focus_certified": False,
        "boundary": "G0 physical A/B proxy plus documented build; not full sheet"}
    issues = [dict(x, pairing=pairing)
              for pairing, record in sorted(pairings.items())
              for x in record["issues"]]
    return {
        "scope": "independent L1-3 structural/progression audit only",
        "pairings_checked": len(pairings), "variants_checked": 13,
        "level_snapshots_checked": 39,
        "structural_source_pairings": 12,
        "independently_certified_full_focuses": 0,
        "strict_mvp_exits_met": 0,
        "issues": issues, "pairings": dict(sorted(pairings.items())),
        "outstanding": ["unresolved talent award accounting",
                        "independent combat AND noncombat role witnesses",
                        "representative encounter and real player/GM decisions",
                        "real two-event GM milestone adventure evidence"]}


def validate_pilot_milestones(actor_id, records):
    """Validate a proposed GM award chronology, never apply levels/resources."""
    if type(actor_id) is not str or not actor_id:
        raise ValueError("Explicit pilot character required")
    if not isinstance(records, (list, tuple)) or len(records) != 2:
        raise ValueError("Exactly two separate pilot level-award events required")
    seen = set()
    current = 1
    for entry in records:
        if not isinstance(entry, dict):
            raise ValueError("Each event needs an explicit GM record")
        event = entry.get("event_id")
        if (type(event) is not str or not event.strip() or event in seen
                or entry.get("character_id") != actor_id
                or entry.get("gm_declared") is not True
                or entry.get("kind") != "adventure_milestone"
                or entry.get("from_level") != current
                or entry.get("to_level") != current + 1
                or entry.get("automatic") is not False
                or "xp" in entry or "destiny_refill" in entry
                or "vp_refill" in entry):
            raise ValueError("Invalid or duplicate GM-declared advancement milestone")
        seen.add(event)
        current += 1
    return {"actor": actor_id, "level": 3, "unique_milestones": 2,
            "awards_applied": False, "resources_refreshed": False}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
