# B04/B05 — Formal Priest Life Focus Balance Assessment v0

**Assessment disposition:** **RETAIN EXISTING NUMBERS; BOUNDED MECHANICAL EVIDENCE ACCEPTED; GLOBAL BALANCE NOT YET CERTIFIED.** This is a formal *review of the available evidence*, not a claim that three Priest Life Focuses are equally powerful, not a probability study, and not authorization to alter the rulebook.

**Scope:** human L1–3 Priest Life High (H), Medium (M), Low Restorative Vanguard A (A, Guided Chosen) and Low Preservation Vanguard B (B, Shelter Chosen), with the actual current source builds, spell permissions, AP/VP budgets, G0/G1/G3/G4/G4.5/G5 native receipts, and the target policies already merged into main. A/B are different source builds: they are **not interchangeable replicas of a single Low Priest statistic line**.

## Executive finding / decision

1. **No demonstrated rules contradiction or numerical adjustment requiring immediate change in the bounded evidence.** The three preceding, fully tested source-native suites verify that their authored actions actually pay for their outcomes, with original source geometry, resource partitions, damage packets, active effects, Reaction windows and natural Step-2 regeneration. This is **mechanical confidence**, not an empirical proof of balanced utility.
2. **Distinct Focus identities exist in the supported L1–3 repertoire:** High has cheaper 20-AP prepared Projections and can place *different* maintained effects on two allies at L3; Medium has a single 24-AP Consecration host with a paid 24-AP reassignment and two source-legal L3 Intercession modes (each 2 Spent VP and one Reaction, subject to packet/Step restrictions); Low A has self-only Chosen Guided plus source-valid paid Basic Heal when hand/funds permit; Low B has self-only Chosen Shelter and finite-budget L3 Vital Interposition, but its occupied mace/shield currently forbids a free-hand external Basic Heal action.
3. **Do not declare a strongest or weakest Focus.** These differences include distinct source equipment, maximum HP/Vigor, pool sizes, targets, preparation constraints and opportunities; comparing raw terminal HP across H, M, A and B would conflate magic with build defenses. Self-defense and external ally support are different experimental strata.
4. **MVP decision:** keep the current L1–3 Focus rules **unchanged for controlled playtesting**, with the per-Focus legal access and source-resource caps verified as implemented. Reserve final balance sign-off and proposed numerical changes for later, targeted authorizations. The technical v0 assessment is complete; **global balance certification remains false**.

## Evidence inventory, provenance and comparability

| Evidence stratum | Source | Primary scenarios | What it actually measures | Constraint |
|---|---|---:|---|---|
| Two-round matched self-defense | `scripts/b05_three_focus_life_comparison_v0.py` | **64** | True paid Soldier/Sentry attacks, real natural HP/Vigor, finite self-Shelter, Low L3 Exaltation and original AP/VP | Compare each role only to the **same role, level and opponent** with no magic |
| Extended attrition & tactical selection | `scripts/b05_three_focus_life_extended_attrition_v0.py` | **912** | 4/8 requested rounds, early stops, Guard, Dodge, real G1 cautious movement, fixed light/heavy damage, source-paid Healing | Realized rounds can differ; report those differences **separately** from like-exposure terminal HP/Vigor |
| Multi-recipient support & Intercession | `scripts/b05_priest_life_multi_recipient_stress_v0.py` | **408** | Distinct F Scholar and R Bow Vanguard recipients, changing foe targets, paid M reassignment, L3 Guided/Vital Intercession, High distinct two-target maintenance, Low A legal external Heal | A dead scheduled target is **not silently retargeted**. If paid enemy attack counts differ, terminal HP/Vigor is **not like-exposure evidence** |
| Older H/M ally support, contextual only | Embedded in the first suite | **36** | Historical two-round High/Medium support to Scholar F | Previous F regeneration policies differ; **not** a third Low recipient comparison; excluded from primary count |
| **Primary total** | Three first-party source-native matrix runners | **1,384** | Exact deterministic scenario witnesses | **Not** 1,384 random independent trials or statistical win-rate samples |

Executable authority: `scripts/b05_priest_life_formal_balance_assessment_v0.py` calls all three source-native matrix runners with one explicit seed, checks original canonical audit hashes and exact cardinalities, validates per-role/per-level and foe source digests across strata, and requires each row's **own same-source no-magic baseline**. Output contains all three parent audit SHA-256 values, group-level witness counts and observed HP/Vigor outcomes, AP/VP payment occurrence, actual Healing/Reassignment/Intercession receipts, early-stop or dead-target attack-exposure mismatches, a separately labeled 36-case contextual stratum, unresolved gates and a canonical assessment SHA-256. `attest_assessment(...,seed=...)` independently re-runs the source scenes before accepting even a rehashed caller-supplied summary.

### How to interpret the generated observation table

The JSON `cohort_observations` groups by **stratum + exact Focus role + exact authored policy**, then reports counts of cells with higher/lower terminal HP or Vigor relative to that cell's own no-magic baseline. Counts have **no probability interpretation** and are **not comparable across cohorts with different coverage or action prices**. The accompanying `same_exposure_cells` and `changed_exposure_cells` fields are essential: early terminal comparison against different realized round counts or absent scheduled G5 attacks is excluded from reported HP/Vigor benefit frequencies. Such altered survival/attack exposure remains separately visible and cannot be erased or scored as a free health improvement.

Native damage and restoration naturally depend on VP, finite Shelter budget, recipient HP deficit, real regeneration throughput, line of effect, initiative and explicit Reaction availability. An unchanged HP result can mean an effect had no eligible opportunity to help, **not** that the spell is ineffective. Conversely, the number of snapshots where a fixed policy helps is **not** a general-play reliability rate. Aggregate "party HP" counts in a *single multi-recipient cell* describe resource units, not a utility function or weighted win criterion.

## Verified seed-0 results snapshot (bounded, not a ranking)

The CI-backed source-native assessment with **seed 0** produced assessment digest `672703891adb31865a64947469c8653826ab0708a645b08974c679913a899cd5` before this documentation-only addition. These counts are illustrative fixed-policy observations from `B05_FORMAL_SOURCE_COUNTS` in the 1,294-test B05 verification; they are **not rates, posterior probabilities or head-to-head Focus scores**.

| Native cohort (separate source stratum) | Witnesses | Same realized exposure | Higher terminal HP than own baseline | Higher terminal Vigor than own baseline | Additional native evidence |
|---|---:|---:|---:|---:|---|
| H High, extended paid Heal cycle | 72 | 42 | 30 | 42 | No healing after an imagined early stop; HP/Vigor improvement frequencies only count like-exposure cells |
| B Low, extended L3 Exaltation | 24 | 21 | 6 | 14 | Three scenarios had a different realized round count and are excluded from endpoint-benefit tallies |
| H High, L3 external dual prepared wards | 8 | 8 | 6 | 3 | Genuine two-target maintained effects; no Basic Heal receipt in this policy |
| M Medium, L3 Guided Intercession | 8 | 8 | 6 | 0 | **4** genuine other-beneficiary G0 Step-2 Intercession receipts |
| M Medium, L3 Shelter Intercession | 8 | 8 | 0 | 4 | **4** genuine native Sentry G5/G4 Direct Vigor Intercession receipts |
| A Low, external Basic Heal triage | 24 | 24 | 9 | 24 | **47** real paid external Heal receipts across 24 independent scenes |
| B Low, self Chosen Shelter in multi-target scene | 24 | 24 | 0 | 6 | **0** external Basic Heal receipts; original mace-and-shield access restriction preserved |
| B Low, two-round self L3 Exaltation | 2 | 2 | 0 | 2 | Only two deterministic self-defense witnesses; not a general survival rate |

**Reading the table:** Each row uses its **own H, M, A or B no-magic source baseline** at the same authored conditions. “Higher terminal HP/Vigor” counts *scene endpoints*, not gained point totals, and it does not equate one HP with one Vigor or one saved party member with another. In multi-target scenes, the HP/Vigor comparison combines the existing three party recipients **within each same-source scenario only**; it is never a cross-Focus utility weighting. Cohorts with different source AP/VP prices, targeting access, enemy policy, pressure or realized exposure are **not commensurate**. The H Heal cohort has 30 different-exposure scenarios; these are not interpreted as a bonus from missing attacks. Re-run the assessment after source changes; this snapshot is diagnostic evidence, not an immutable balancing target.

## Focus-by-Focus formal assessment

| Focus | Proven native mechanical niche (L1–3) | Countervailing cost or restriction | Balance disposition |
|---|---|---|---|
| **H — High Life** | 20 AP prepared Prayer; high preparation flexibility; maintained Guided or Shelter on an ally, paid Basic Heal, L3 two distinct prepared maintained effects on separate allies | Finite VP; preparation/Invocation gating; two concurrent effects consume their actual separate AP and Committed/Spent VP; no invented free offensive turn | **Retain.** Test different preparation plans and real action economy under multiple competing uses before declaring superior |
| **M — Medium Life** | Single maintained host (Guided/Shelter), 24-AP reassignment F→R while preserving budget/reservation; L3 Guided Intercession at a real other-recipient Step-2 and Vital Intercession for native other-recipient Direct Vigor packet | 24 AP host/reassignment; 2 Spent VP and one real Reaction per Intercession; cannot bless same recipient twice, cannot react to Soldier HP-only damage, cannot exceed finite host budget | **Retain.** Reaction opportunity cost and tactical initiative changes are the outstanding performance questions |
| **A — Low Guided** | Lower **1 Committed VP** Chosen self-Rite; L3 Held Renewal only from actually unused true throughput; independently source-legal **30-AP/2-Spent VP Basic Heal** to F/R where a functional hand/range exists | Chosen cannot target F/R; Level 1's small VP pool cannot reserve Chosen and pay a 2-Spent Heal together; no extra regeneration Steps | **Retain.** Test whether self-maintenance/ally triage is viable under frequent shared VP pressure |
| **B — Low Shelter** | Lower **1 Committed + 1 Spent VP** self-Chosen Shelter with finite B8; L3 Vital Interposition pays 1 more Spent VP to prevent genuine *own* HP loss; committed-only refund upon legitimate host expiry | 30-AP Chosen; **both hands occupied by verified mace and shield**, so external Basic Heal cannot be authorized by a fake `hand_available=True`; self-only host and finite budget | **Retain with explicit support limitation.** An action-priced, source-legal equipment-transition experiment is a *design prerequisite* before claiming B has equivalent external healing |

The table states **access/cost identities and tested receipts**, not a numerical rank or "optimal" build. Low Priest A and B's different equipment and physical defenses must never be hidden in cross-Focus output.

## Risk / unresolved-evidence register

| ID | Priority | Missing evidence | Required next check |
|---|---|---|---|
| G1 | High | Fixed d20/d6, single source foe, limited horizons; no probability distribution | Bounded variable attack/damage confirmations, additional genuine enemy types and wound-creation stress |
| G2 | High | Focuses do not share comparable external targeting/host count/equipment | Measure **legal party objectives** and budget rather than pretend to grant all Focuses the same spell |
| G3 | High | Fixed Initiative, deterministic targeting, no adaptive AI/contested spell choices | Alternative initiative and target selection with source-authenticated G0/G5 outcomes |
| G4 | Medium | Medium Intercession's lost alternative Reaction is not valued | Multi-eligible native Reaction windows and equivalent opportunity costs |
| G5 | Medium | Low B's dual-held equipment prevents external Basic Heal now | Independently author/verify the equipment switch, if desired, before a balance comparison |
| G6 | Medium | No long adventuring-day/wound and VP-recovery distribution | Cross-encounter attrition and actual recovery timeline, not extrapolated four-round costs |

A test gap is **not** a defect finding. None of G1–G6 alone authorizes increasing/decreasing a spell's VP cost, regenerating extra HP, changing action economy or overriding the source equipment contract. A numerical tuning PR would need a named benefit/drawback hypothesis, a new source-backed matched stress test, a before/after replay, and explicit project approval.

## Decision gate and recommended next milestone

**Approve:** bounded L1–3 Priest Life mechanical/comparative evidence for use as the next controlled-playtest baseline.

**Defer:** final global Priest Life balance sign-off, generic Focus rankings, unverified Low B free-hand transition, any AP/VP/regeneration/Shelter rewrite. The assessment deliberately returns `global_balance_certified=false`, `numerical_tuning_authorized=false` and `focus_ranking=null`.

**Next:** **B04/B05 — Priest Life Focus Decision-Gate Playtests v0** focused on G1–G4 (additional genuine enemy/initiative/target policies and Medium Reaction conflicts), with G5 addressed as a separate equipment-rule decision if necessary. Only propose actual numerical tuning if those new legal cases reveal a reproducible role-locally adverse tradeoff.

## Reproduction

```bash
python -m unittest tests.test_b05_priest_life_formal_balance_assessment_v0 -v
python -m unittest discover -s tests -v
python -m scripts.b05_priest_life_formal_balance_assessment_v0 --seed 0 > priest_life_focus_balance_assessment_v0.json
```

The generated JSON is an assessment built from **live source files on that repository commit**; a source change requires re-running it, not copying numeric counts from an earlier review. All tests and scripts must retain historical B06 Phase 3 audit stability. No automatic branch merge, rules tuning or certification is part of this milestone.
