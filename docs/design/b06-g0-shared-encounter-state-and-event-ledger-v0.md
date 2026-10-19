# B06 G0 — Shared Encounter State and Native Turn/Event Ledger v0

> **Implementation contract and test evidence, not combat rules or a completed encounter.** This incremental adapter consumes existing canonical initiative/AP, defense, regeneration and creature/character source data. It does **not** certify a numerical CR, the Phase 3 first-stop cohort, any complete B06-I1/I2/I3 encounter, or any Archetype × Focus end-to-end identity.

## G0 implementation

Source: [`scripts/b06_encounter_state_v0.py`](../../scripts/b06_encounter_state_v0.py).
Tests: [`tests/test_b06_encounter_state_v0.py`](../../tests/test_b06_encounter_state_v0.py).

**Typed source provenance and initial resources**

- Every actor retains a frozen `Source` record: repository-relative source path, SHA-256 of its exact source bytes, source ID, scope/status, immutable Ability/Training/equipment/attack-profile tuples, and explicitly selected start state.
- **B06-EN-01** Sentry: exact `cold_start` versus `prepared_start`; does not silently assign 3 Committed VP or activate the Reserve for a cold state.
- **B06-EN-02** Soldier: local non-Archetype `42 AP/Physical24`, 0 VP, Shield Guard18/capacity2, Vigor36 and regeneration2. These **do not** define a generic NPC progression rule.
- **B06-EN-03** Hunter: one shared HP14/Vigor42, latent but unusable Guard capacity1 without instrument, and rigid ordered `("head","rear")` occupied cells. G0 **requires explicit positions**; it has no movement/pivot/path search and grants no anatomical extra hitboxes.
- **A/B**: source-linked **physical-only role projections** from the Phase 1/2 Hunter code and two structurally reviewed B05 Life/Low Priest sheets; their unbuffed `2 × level` VA0 VP reserve is **not** a new spell executor or a claim that their normal Priest states always start without Rites. Actual prepared-prayer and hands/state decisions still require G3.
- **R/F**: instantiate from their independently audited L1–3 Python ledgers. An R wielding a bow and an F with a *carried but not wielded* dagger have **no currently valid Guard instrument**, regardless of their physical-tempo Guard capacity. R starts with the authored 20 arrows, not infinite ammunition. These are structurally verified, **not** new Focus certificates.

**Runtime and timing**

- One actor instance owns persistent HP/Vigor, Available/Committed/Spent VP, Wound Repair Progress, chosen effects, conditions, timed milestones, ammunition, posture/footprint records and round/turn counters.
- Caller supplies actual Initiative totals and explicit tie-order policy when needed. A stable actor ID is **not** a fictional tie-break/AI choice.
- At **Round Begin**, refresh Guard capacity, zero nonnegative Dodge Pressure, refresh the Reaction and reset Opportunity usage. Guard/Dodge are not Reactions. Turn AP and 12 MP arrive on **the actor's own turn**, after its unique Regeneration Step, and unused ordinary AP/MP are lost at cleanup. Subsequent rounds are separately refreshed.
- The `RegenerationChoice` is explicit and paid through the shared Vigor pool: natural restored HP, wound Repair Progress and cancelling a Dying −1 HP loss each consume **1 throughput and 1 recipient Vigor per point**. Survival cancellation leaves HP and Repair Progress unchanged; with zero Vigor the Dying loss proceeds. Dying natural wound repair is oldest-incomplete-first; no direct natural HP before all blocking wounds are repaired. This G0 slice does **not** execute Basic Heal or other externally authored healing (G3–G4); those effects must *not* be forced through this natural-regeneration debit method.
- `spend_ap`, `spend_vp` and `release_vp` reject resource overdraw, refunds of Spent VP, and unsupported action classes. A Full Action is legal only with the entire Turn AP allotment available. Blink debt is represented but its geometric response/AP-exception handling awaits G3.
- `declare_sequence` commits **all listed ordinary physical source attack profiles** and AP before defender's pre-roll Guard/Dodge/Take-Hit assignments. Guard requires a currently ready Guard-capable instrument, Dodge subtracts pressure **once**, each chosen Dodge then adds 2 pressure, and Take Hit does not claim an automatic hit. G0 logs `unresolved_attack_roll` instead of fabricating one; ranged lane/profile, magical Composite, complex Pounce and damage/wounds stay in G1–G5.

**Response priority and audit log**

- An Interception reservation commits its ordinary AP at reservation, with one earliest matching reservation released **per creature** on a trigger occurrence. Released Interceptions resolve in **Initiative** order; nested response windows are permitted and resolved within their caller.
- **Critically**, the original trigger is rechecked **after precommitted Interceptions** and nested windows, **before** spontaneous Reactions/Opportunities. If invalid, the original response never declares/pays Reactive Blink. If still valid, selected spontaneous responses commit capacity and resolve in Initiative order; the trigger then receives a **second legality recheck**. G0 does **not** grant an inherent Interrupt to an ordinary Interception: the supplied source-validated effect must actually change legality.
- A monotonic append-only event ledger records turn/round, actors, declarations/commitments, response order, source identity/hash, defense allocation, costs, unresolved decisions, and first/second rechecks. `serialize()` uses canonical sorted JSON for deterministic trace comparisons; seed is supplied but **G0 does not roll from it**.

## Source ownership and explicit stop boundaries

| Gate | G0 can assert | Not claimed |
|---|---|---|
| G0 source/clock | B06 enemy cold/prepared and local non-Focus states, A/B/R/F structural/proxy lineage, Round Begin and AP/MP accounting | GM policy, full player equipment handling, initiative roll execution |
| G0 defense/order | Physical-profile declaration, same-target sequence lock, pre-roll Guard/Dodge/Take Hit, Interception-before-Reaction, no Reaction on cancelled trigger | Projectile-specific legal Guard and cover (G2); actual hit, miss, defense invalidation and damage/wounds (G4–G5) |
| G0 resource conservation | No negative budgets, VP partition, one genuine own-turn natural regen, three natural Vigor debit cases | Actual caster VP techniques and Basic Heal (G3–G4), Dying continuation with full injuries/hazards (G4) |
| G1 onward | Explicit initial coordinates and ordered Hunter body cells, retained timed-effects field | Movement/LOS/traversal (G1–G2), spells (G3), toxin clocks (G4), full fights (G5–G6), CR (G7) |

**Provenance discipline:** Do **not** assign the original signed Hunter Phase 3's 770 `contact_path_unresolved` runs to new paths or outcomes. The old 4,096-trial census, first-stop counts and Hunter `unrated` remain unchanged. No executed attack-roll damage from this G0 ledger may be represented as a full encounter result.

## Verification

```bash
python -m unittest discover -s tests -p 'test_b06_encounter_state_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.validate_b06_footprints
python -m scripts.b06_hunter_phase3_report_v0 --json-out build/b06-phase3-census.json --markdown-out build/b06-phase3-census.md
```

CI is configured to rerun the exact-PR-head B06 Phase 3 verification and full repository unittest suite whenever the G0 module or this design contract changes. Completion of **G0** means *reusable, traceable substrate and regression gates*; G1 is still required before any geometrically honest multi-actor contact.
