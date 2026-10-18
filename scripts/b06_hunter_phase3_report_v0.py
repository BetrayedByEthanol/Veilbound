"""Validate and publish B06 Phase 3's deterministic *bounded* one-round census.

This report has no wins, deaths, CR estimates or geometric pathfinding.
Execute at repository root:
  python -m scripts.b06_hunter_phase3_report_v0 --json-out ... --markdown-out ...
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from scripts.b06_hunter_tactical_diversity_v0 import CASES, SEEDS, census, trial

TERMINAL_STATES = frozenset((
    "round_one_complete", "hunter_first_zero", "frontline_first_zero",
    "wound_unresolved", "contact_path_unresolved",
))
TERMINAL_ORDER = (
    "hunter_first_zero", "frontline_first_zero", "wound_unresolved",
    "contact_path_unresolved", "round_one_complete",
)
METRICS = (
    "pounce_declared", "balance_resolved", "full_toxin", "reduced_toxin",
    "vp_spent", "arrows_fired", "vigor_burn",
    "front_caster_precontact_casts", "front_caster_approach_mp",
    "lane_disrupted_trials", "contact_path_unresolved",
)


def build_report(seeds=SEEDS):
    """Run real Phase 3 code and verify every published aggregate."""
    if not isinstance(seeds, int) or seeds <= 0:
        raise ValueError("seeds must be a positive integer")
    rows = census(seeds=seeds)
    if len(CASES) != 32 or len(rows) != len(CASES):
        raise AssertionError("Changed Phase 3 case shape")
    expected_keys = [f"L{level}-P{size}-{roster}-{opening}-{front}"
                     for level, size, roster, opening, front in CASES]
    if [r["scenario"] for r in rows] != expected_keys:
        raise AssertionError("Case order mismatch")

    for row in rows:
        terminal = row["terminal"]
        if (row["trials"] != seeds or set(terminal) - TERMINAL_STATES or
                any(not isinstance(v, int) or v < 0 for v in terminal.values()) or
                sum(terminal.values()) != seeds):
            raise AssertionError(f"Terminal conservation: {row['scenario']}")
        if any(not isinstance(row[k], int) or row[k] < 0 for k in METRICS):
            raise AssertionError(f"Invalid counter: {row['scenario']}")
        # These are summed *per-trial booleans*, not event multiplicities.
        # Each can occur at most once within one source trial.
        boolean_counts = ("pounce_declared", "balance_resolved",
                          "lane_disrupted_trials")
        if any(row[k] > row["trials"] for k in boolean_counts):
            raise AssertionError(
                f"Per-trial Boolean count exceeds trial count: {row['scenario']}")
        if row["contact_path_unresolved"] != terminal.get("contact_path_unresolved", 0):
            raise AssertionError(f"Bad unresolved count: {row['scenario']}")
        if row["balance_resolved"] > row["pounce_declared"] or (
            row["full_toxin"] + row["reduced_toxin"] > seeds
        ):
            raise AssertionError(f"Impossible Pounce/toxin count: {row['scenario']}")
        # Pounce is declared only with a clear lane, and every unresolved
        # contact path requires a previously disrupted lane. These are
        # mutually exclusive first-window state flags per source trial.
        if (row["pounce_declared"] + row["lane_disrupted_trials"] >
                row["trials"] or
                row["contact_path_unresolved"] > row["lane_disrupted_trials"]):
            raise AssertionError(
                f"Inconsistent Pounce/lane/path attribution: {row['scenario']}")
        if row["vp_spent"] % 2 or row["front_caster_approach_mp"] % 2:
            raise AssertionError(f"Invalid VP/movement increment: {row['scenario']}")
        level, size, roster, opening, front = CASES[expected_keys.index(row["scenario"])]
        # Warned starts in frontal contact; no precontact corridor move
        # occurs, so neither Pounce, lane disruption nor unresolved paths
        # are possible in a warned source trial.
        if opening == "warned" and any(
                row[k] for k in ("pounce_declared", "lane_disrupted_trials",
                                 "contact_path_unresolved")):
            raise AssertionError(
                f"Warned opening has ambush-only counters: {row['scenario']}")
        # A/B-only original parties have neither a Bow shooter nor a Fire
        # caster. The census must never attribute Flame-caused Vigor burn,
        # Flame VP, or the front caster's range-entry MP/casts to them.
        caster_only = ("vp_spent", "vigor_burn",
                       "front_caster_precontact_casts",
                       "front_caster_approach_mp")
        if roster == "original" and (
                row["arrows_fired"] or any(row[k] for k in caster_only)):
            raise AssertionError(
                f"Original roster received mixed resources: {row['scenario']}")
        # Front F needs to step into the 1-3-square cast lane *only* in
        # mixed/ambush/exposed scenarios, and casts made before Hunter
        # contact can only belong to that same setup. Backline F can still
        # cast in other mixed setups; only these front-specific fields
        # must remain zero there.
        front_flame_setup = (roster == "mixed" and opening == "ambush"
                             and front == "exposed")
        if not front_flame_setup and (
                row["front_caster_precontact_casts"] or
                row["front_caster_approach_mp"]):
            raise AssertionError(
                f"Impossible front-caster attribution: {row['scenario']}")
        # In mixed/warned/exposed, F is the unique caster and the lead:
        # warned contact already threatens F, so the source trial skips
        # its action before any VP is spent or direct Fire Vigor is dealt.
        # No backline F exists to account for those totals instead.
        if (roster == "mixed" and opening == "warned" and
                front == "exposed" and
                (row["vp_spent"] or row["vigor_burn"])):
            raise AssertionError(
                f"Threatened front Flame spent resources: {row['scenario']}")
        max_actions = (30 + 6 * (level - 1)) // 20
        if row["front_caster_precontact_casts"] > (
                row["front_caster_approach_mp"] // 2 * max_actions):
            raise AssertionError(
                f"Precontact caster lacked paid range-entry movement: {row['scenario']}")
        # Every 2-MP front-F approach in the bounded runner is followed
        # by at least one affordable Flame launch, counted even on a miss.
        if (row["front_caster_precontact_casts"] <
                row["front_caster_approach_mp"] // 2):
            raise AssertionError(
                f"Front caster moved without launching Flame: {row['scenario']}")
        # Every Flame launch costs 2 VP and may burn at most 5 Vigor
        # (2 + ceil(d8/3)). Its critical HP packet does not multiply burn.
        if row["vigor_burn"] > (row["vp_spent"] // 2) * 5:
            raise AssertionError(
                f"Vigor burn exceeds paid Flame launches: {row['scenario']}")
        if (row["vp_spent"] > seeds * max_actions * 2 or
                row["arrows_fired"] > seeds * max_actions):
            raise AssertionError(f"Impossible VP/ammunition bound: {row['scenario']}")
        if row["front_caster_precontact_casts"] * 2 > row["vp_spent"]:
            raise AssertionError(f"Unpaid front spell: {row['scenario']}")
        if row["front_caster_approach_mp"] > 2 * seeds:
            raise AssertionError(f"Impossible front F movement: {row['scenario']}")

    totals = {
        "trials": sum(r["trials"] for r in rows),
        "terminal": {s: sum(r["terminal"].get(s, 0) for r in rows)
                     for s in TERMINAL_ORDER},
        **{k: sum(r[k] for r in rows) for k in METRICS},
    }
    if totals["trials"] != len(CASES) * seeds:
        raise AssertionError("Census size mismatch")
    if sum(totals["terminal"].values()) != totals["trials"]:
        raise AssertionError("Total terminal conservation")

    group_totals = {}
    for ix, name in ((2, "roster"), (3, "opening"), (4, "front")):
        by = {}
        for r, case in zip(rows, CASES):
            key = case[ix]
            if key not in by:
                by[key] = {"trials": 0, "terminal": Counter(),
                           **{k: 0 for k in METRICS}}
            dst = by[key]
            dst["trials"] += seeds
            dst["terminal"].update(r["terminal"])
            for k in METRICS:
                dst[k] += r[k]
        group_totals[name] = {
            key: {**group, "terminal": {s: group["terminal"].get(s, 0)
                                        for s in TERMINAL_ORDER}}
            for key, group in by.items()
        }
        if sum(v["trials"] for v in group_totals[name].values()) != totals["trials"]:
            raise AssertionError("Grouped census conservation")

    data = {
        "model": "B06 Hunter Phase 3 bounded one-round v0",
        "seed_count_per_cell": seeds,
        "scenario_count": len(CASES),
        "source_runner": "scripts/b06_hunter_tactical_diversity_v0.py",
        "terminal_meaning": "first stopping event, NEVER party victory/death/CR",
        "totals": totals, "by": group_totals, "cases": rows,
    }
    serialized = json.dumps(data, sort_keys=True, separators=(",", ":"),
                            ensure_ascii=True).encode("utf-8")
    data["audit_sha256"] = sha256(serialized).hexdigest()
    return data


def render_markdown(report):
    """Reproducible Markdown output, deliberately without inferred win rates."""
    lines = [
        "# B06 Phase 3 — deterministic one-round census",
        "",
        f"**{report['scenario_count']} conditions × "
        f"{report['seed_count_per_cell']} keyed seeds = "
        f"{report['totals']['trials']} sampled windows.**",
        "",
        "These are *first stops within one round*, not party victory, death, "
        "CR, full encounter outcomes or observed playtest results. In particular "
        "`contact_path_unresolved` is an **unresolved geometry/Opportunity** "
        "case and must not be put in a victory denominator.",
        "",
        f"Audit SHA-256: `{report['audit_sha256']}` "
        "(canonical JSON excluding this hash).",
        "",
        "## Terminal and resource totals",
        "",
        "| First stop | Windows |",
        "|---|---:|",
    ]
    for stop in TERMINAL_ORDER:
        lines.append(f"| `{stop}` | {report['totals']['terminal'][stop]} |")
    lines += [
        "",
        "| Counted event | Total |",
        "|---|---:|",
    ]
    for key in METRICS:
        lines.append(f"| `{key}` | {report['totals'][key]} |")
    lines += ["", "## Party roster comparison — conditional one-round totals", "",
              "| Roster | Windows | Hunter-first 0 HP | Front-first 0 HP | "
              "Unresolved path | Pounce declarations | Spent VP | Arrows |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for name, group in report["by"]["roster"].items():
        t = group["terminal"]
        lines.append(
            f"| {name} | {group['trials']} | {t['hunter_first_zero']} | "
            f"{t['frontline_first_zero']} | {t['contact_path_unresolved']} | "
            f"{group['pounce_declared']} | {group['vp_spent']} | "
            f"{group['arrows_fired']} |"
        )
    lines += [
        "",
        "The rosters have different combat roles, starting arrangements and "
        "legal-action restrictions. Their counts are **not causally matched "
        "win probabilities**. Hunter first reaching 0 HP only marks Dying; "
        "a single frontline down is not party defeat.",
        "",
        "## All scenario cells",
        "",
        "| Scenario | Hunter-first 0 | Front-first 0 | Wound stop | "
        "Unresolved path | Round complete | Pounce | VP | Arrows | "
        "Vigor burn | Mean Hunter HP at stop |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["cases"]:
        t = row["terminal"]
        lines.append(
            f"| {row['scenario']} | {t.get('hunter_first_zero',0)} | "
            f"{t.get('frontline_first_zero',0)} | "
            f"{t.get('wound_unresolved',0)} | "
            f"{t.get('contact_path_unresolved',0)} | "
            f"{t.get('round_one_complete',0)} | {row['pounce_declared']} | "
            f"{row['vp_spent']} | {row['arrows_fired']} | {row['vigor_burn']} | "
            f"{row['mean_hunter_hp']:.3f} |"
        )
    lines += [
        "",
        "## Verification and limits",
        "",
        f"- Source: merged Phase 3 runner, 32 cells, seeds " 
        f"`0..{report['seed_count_per_cell'] - 1}` per cell.",
        "- Internally checked: count conservation, known terminal types, ",
        "  bounds on ammo/VP/movement, toxin and Pounce resolution, ",
        "  original-roster resource isolation and group totals.",
        "- Not resolved: full map/LOS geometry, conditional movement/Opportunities,",
        "  full character sheets for R/F, full Dying/wounds, multiple rounds,",
        "  long-term toxin, retreat and adaptive target choice.",
        "- The saved numeric output is **only as verified as the reported",
        "  execution environment and source commit**; do not replace source",
        "  acceptance with a manually copied or unreviewed result.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json-out", type=Path)
    p.add_argument("--markdown-out", type=Path)
    p.add_argument("--seeds", type=int, default=SEEDS)
    args = p.parse_args(argv)
    result = build_report(seeds=args.seeds)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(render_markdown(result), encoding="utf-8")
    print(json.dumps({
        "cases": result["scenario_count"],
        "trials": result["totals"]["trials"],
        "terminals": result["totals"]["terminal"],
        "rosters": result["by"]["roster"],
        "audit_sha256": result["audit_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
