# B06 G7 — Encounter Calibration Readiness and Scenario Matrix v0

> **Calibration design and executable-evidence audit; NOT calibrated
> encounter difficulty, a creature CR, a party-win probability, or complete
> B06 encounter-pack certification.** The G7 entry gate may begin because
> G6-C/G6-D now demonstrate genuine multi-round source-backed combat and
> one bounded Hunter death terminal. Source-supported **fixed dice** are
> evidence that the engine can perform an action, not stochastic playtests.

## Decision

**GO** for authored scenario planning, evidence collection and *pilot
infrastructure*. **NO-GO** for a pooled Hunter difficulty estimate,
numeric CR, unqualified survival rate, or G7 difficulty threshold.

Evidence comes from three distinct sources:

| Evidence | Scope genuinely supported | Not supported |
|---|---|---|
| [Frozen Phase 3 report](b06-hunter-phase3-census-results-v0.md) | **32 conditioned cells × 128 seeds = 4,096 one-round first-stop windows**, canonical SHA-256 `c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b` | Complete parties, first-0-HP-as-kill, unresolved 770 paths redistributed into defeats; independent L1–3 mixed build certification in the old simulator |
| [Native G6-C](b06-g6c-mixed-party-hunter-encounter-v0.md) | L2/L3 **three/four source-backed PCs**, two full real Initiative rounds; actual A/B melee, R natural-1 launched misses, optional F Fire and Hunter Bite/venom/regeneration | Variable dice policies, alternate frontliners and setups, terminal survival/defeat rate |
| [Native G6-D](b06-g6d-hunter-completion-bow-damage-v0.md) | Source R Bow-to-G4, real 4-PC third-round Bow Hunter death terminal and independently tested bounded Reactive/Prepared Intervene | General Arrow Cover/collateral, universal protective geometry, live multi-action AI or randomized death frequency |

**One scripted Hunter defeat is proof of reachability, not a sample of the
probability of defeating the Hunter.** Likewise, the actual G6-C 4-PC
Dying event is not Hunter death, and a live two-round cutoff is not a
completed escape, surrender or party defeat. Each instrumented
continuation must keep the event ledger and its exact original
source/cost indices.

## Versioned, machine-readable scenario manifest

[`scripts/b06_g7_calibration_readiness_v0.py`](../../scripts/b06_g7_calibration_readiness_v0.py)
enumerates all **48** cells of the strictly scoped first G7 matrix:

| Dimension | Values | Authority and reason |
|---|---|---|
| Character level | **L2, L3** | Full G6-C and G6-D native proxy-sheet levels |
| PC count | **3, 4** | 3: A/B/R; 4: A/B/R/F |
| Enemy count/type | **one 1×2 B06-EN-03 Hunter** | Source fixture, HP14, Armor3 and its native physiology |
| Start | **warned_clear**, **forest_ambush** | Warned clear has authored map/contact; forest ambush needs genuine reach/terrain/Pounce alternatives |
| Head-forward target | **A_head_forward**, **B_head_forward** | G6-C authors A in front, B adjacent beside; changing front is not renaming an actor |
| Policy | **decline_all**, **reactive_shield**, **prepared_body** | Declined options are G6-C fixed script; G6-D protects only source Hunter Bite in bounded A/B geometry |

<text>This matrix is a trial *plan*. No invented Cover, surprise modifier,
initiative manipulation, shield AP, MP step, Critical, poison tick or
extra attack is assigned to the blocked cells.</text>

### Status partition (48 / 48 accounted for)

| Status | Cells | Exact scope |
|---|---:|---|
| `fixed_native_window` | **4** | L2/L3 × 3/4 PCs, warned clear, A head-forward, declined optional responses. Native two-round G6-C witnesses exist |
| `component_verified_only` | **2** | **L3, four PCs, warned-clear, A head-forward:** Reactive Shield or Prepared Body are independently exercised by the source G6-D protection regression fixtures. They are **not composed into a G6-C mixed-party encounter** |
| `blocked_not_executable` | **42** | All forest ambush or B head-forward variants **plus six warned-clear A-front protective variants** at L2/P3, L2/P4, or L3/P3 that have **no tested G6-D protective witness for that exact level/party size** |

In other words: **4 fixed-choice encounter windows witnessed, 2 configurations
with separately verified response components, 42 currently blocked**.
These are not 48 combat outcomes, and none is a stochastic calibration
sample. A component-only status does not imply the entire encounter
can run under that policy. The only qualifying protection evidence is
[`tests/test_b06_hunter_reactive_intervene_g6d_v0.py`](../../tests/test_b06_hunter_reactive_intervene_g6d_v0.py),
whose native `witness()` and `prepared_witness()` construct
`mixed_scene(size=4, level=3)`. **No G7 protection variant is
executed by the G7 readiness runner**: the matrix cites those prior
regression tests, while the six G7 source replays cover only G6-C
declined-defense windows and G6-D Bow finishing terminals. All
six untested level/party-size protection combinations carry the
`G6D_protection_component_not_verified_at_level_party_size` gate.
The `component_evidence_ref` field records the exact regression
source on the two verified-component rows; `component_evidence_replayed`
is `false` for every matrix row.

All rows have a stable, unique `scenario_id`, explicit build-source
IDs, the missing-authority gate list, `calibration_samples: 0`,
`success_rate: null`, `ci95: null`, `terminal_count: null` and
`creature_cr: null`. Do not treat null as 0% success.

### Native regression witnesses linked to the matrix

The report can replay six **actual** native fixture executions:

- Four G6-C L2/L3 × P3/P4 **two-round** fixed-choice windows. Each
  must have the correct source fingerprints, full turn order and
  two actual Round End events, with two genuinely launched arrows
  and zero G6-D terminal events.
- Two separate G6-D L2/L3 **four-PC third-round defeat overlays**.
  Each has one valid source Bow-to-G4 adjudication, one attested
  Hunter-death terminal and three true Round Ends. These overlays
  reference the existing matching warned-clear P4 matrix cell; they
  are **not new, independent sample cells** or random results.

For each witness the audit records **source IDs and hashes, event counts
from the native ledger, actual rounds, Hunter HP/Dying/dead state,
fixed seed and ending**. The runner validates turn order, actual
Round Ends and source provenance instead of trusting a handwritten
assertion of victory. A CLI `readiness_sha256` fingerprints the
canonical manifest and observations; it is intentionally **distinct**
from the immutable Phase 3 historical audit SHA.

Re-running those six witnesses with different labels/seeds does not
create six additional independent tactical trials: the attack faces
and responses remain chosen by code.

## Required readiness gates before any calibrated outcome census

1. **Real mutually exclusive terminal states.** Separate
   `hunter_dead`, `party_defeated`, `party_withdrew`,
   `other_explicit_resolution`, `legal_window_cutoff` and
   `unresolved_mechanical_branch`. Dying is its own nonterminal
   state, not a kill; poison suppression, wounds, later death and
   recovery must stay on the real clock and damage engine. Do not
   reclassify missing contact, unavailable defender or stuck route
   as defeat.
2. **Complete source-backed party tactics.** Mix independent native
   A/B/R[/F] builds, including physical versus projected AP, legal
   start-of-turn VP/Vigor, regeneration, spent ammunition, Guard/Dodge
   pressure, reactions, withdrawal, retreat and target choice. G6-D
   reactive/prepared protections must be part of the **same native
   encounter**, not stitched on after seeing whether the Bite hit.
3. **Comparable genuine geometry.** Both A and B head-forward cases
   need independently legal 1×2 contact and head/rear mapping.
   Warned and ambush starts require genuine grid/visibility/initiative
   observations; real Pounce route, Cautious movement and nested
   Opportunity/Interception decisions must be resolved or recorded
   unresolved, never inferred from the old statistical approximation.
4. **Ranged coverage and rules-authority boundaries.** The G6-D Bow
   hit adapter remains clear-lane/Take Hit source-bounded; complex
   Cover, living screens, collateral, Guard/Dodge, multi-arrow
   sequences and changed targets require their own evidence. The
   experimental conditions must either use supported mechanics or
   explicitly block unsupported choices, not silently force misses.
5. **Sample design and paired comparisons.** Author an independent
   deterministic keyed random-draw policy for hit, confirmation,
   damage, resistance, movement choices and tactical decisions.
   Lock seeds, scenario configuration, first detection, HP/VP/Vigor,
   arrows/gear, ability use, threat intent, stop criteria and fixed
   step budget **before outcomes are seen**. Pair the same keyed
   source draws across meaningful policy variants and disclose
   nonidentical opponent/party composition as confounded.
6. **Uncertainty and reporting.** Start with a candidate **128-seed
   pilot per genuinely runnable cell** (planning target, *not yet
   samples*). Report every trial denominator and the unresolved
   count and reason. Do not calculate wins/defeats only over the
   resolved subset. The pure `wilson_95()` helper is available for
   future unconditionally complete, independent binary outcomes;
   it is **never used on the current fixed-face fixtures**.
   Confidence bounds require a valid independent trial design;
   paired comparisons need paired analysis, not two unpaired
   intervals asserted as a causal effect.

### Acceptance test for advancing from G7 readiness to G7 calibration

A proposed first batch must carry: named `scenario_id`; real sourced
builds and initiative/footprint snapshot; meaningful varied tactics
and documented deterministic draw policy; complete ledger-backed
terminal provenance; all starting and ending HP/Vigor/VP/MP/AP,
ammo, wounds, injuries and toxin state; causal source links for
protection and ranged hit transfers; and an explicit **legal /
unresolved / observed terminal** classification for *every* seed.
Before a numeric creature rating, repeat with alternate fronts,
ambush/warned, 3/4 PCs, L2/L3 and independently justified difficulty
benchmarks against other creatures or opponents. A scalar Hunter CR
is not automatically identifiable from one selected party.

## Usage and verification

```sh
# 48 cells + six actual G6-C/G6-D witness replays (JSON to stdout)
python -m scripts.b06_g7_calibration_readiness_v0 > /tmp/b06-g7-readiness.json

# Fast 48-cell scope and readiness gates without native re-execution
python -m scripts.b06_g7_calibration_readiness_v0 --manifest-only

# 24 G7 source/coverage/CI/interval/fail-closed tests
python -m unittest discover -s tests -p 'test_b06_g7_calibration_readiness_v0.py' -v
python -m unittest discover -s tests -v
```

**Historical invariant:** Do not edit
`scripts/b06_hunter_tactical_diversity_v0.py`,
`scripts/b06_hunter_phase3_report_v0.py`, or the old signed
Phase 3 JSON/hash when adding new native G7 evidence. Keep historical
first-stop counts in their own metric namespace. The original 770
unresolved Phase 3 contact cases do not magically become legal
full-encounter results after G6 implementation.

## Next implementation priority

I recommend **G7-A — Native End-to-End Policy and Terminal Census
Infrastructure v0**, initially limited to warned-clear A-front
L2/L3 P3/P4 cases. Do not begin by turning the 48 planned matrix rows
into 48 synthetic completions. Then expand real geometry/frontline
support and source-backed protective/Bow response policies before
any CR proposal. This readiness deliverable changes **no
gameplay rules, monster statistics, prices or historical census**.
