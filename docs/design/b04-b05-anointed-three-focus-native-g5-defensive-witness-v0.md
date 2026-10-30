# B04/B05 — Anointed Restoration Three-Focus Native G5 Defensive Witness v0

> **A bounded combat-pressure integration, NOT an independent Focus certificate.** After merged **#171** L3 source-paid Guided Authority and #168–170 native three-Focus Returning Steps, this slice puts sourced AH/AM/AL Restoration characters inside the *actual* G0/G1/G3/G4/G5 Soldier/Sentry combat timeline. Fixed one-hit and two-round policy evidence does not establish representative encounter balance, Anointed offensive melee access, full role effectiveness, a win rate or any MVP exit.

## Source-backed scope and scenario matrix

The [native witness runner](../../scripts/b05_anointed_native_defensive_encounter_v0.py) evaluates **54 deterministic policies** = **3 Focuses × 3 levels (L1–3) × 2 opponents × 3 choices**, all from existing character and creature source SHA256s.

| Axis | Authored cases |
|---|---|
| Focus and actor | **High AH**, **Medium AM**, **Low AL**, each sourced at L1/L2/L3 |
| Enemy | Actual **ordinary Soldier B06-EN-02** sword `B06-AT-03`, or prepared Firebound **Sentry B06-EN-01** `B06-AT-02` with its genuinely preexisting G3 Fire Reserve |
| Two-round policy | `baseline` (no Signature), `signature` (normal recipient-Vigor conversion), `lesser` (one finite 1-Destiny Vigor-free Signature) |
| Exact dice and response | One actual enemy G5 melee declaration, d20=12, sword d6=2, and if prepared Sentry, Vigor d6=1. Defender explicitly elects `take_hit`; no unknown defense, AI, Opportunity or protective response is invented. |
| Native resources | G0 paid enemy Physical Action and G5 attested source-hit index, G4 actual Armor/Fire/Vigor mitigation, G0 genuine recipient Step for two completed rounds, source-attested Signature AP/Vigor/Destiny receipts and unchanged bounded actor source digests |

A **High** caster acts before the enemy in Round 1 and projects the paid **20 AP** Returning Step onto the wounded living `F` ally in its Round-2 ready own turn. A **Medium** caster first pays **24 AP General** to Invest that exact ally, then after the enemy hits, may declare its **0 AP** pulse for the ally's genuine same-round own G4 Regeneration Step. A **Low** caster is the enemy's direct living melee target and acts **after** that enemy in Round 1; its optional **0 AP** self-Embodied pulse occurs at its own genuine post-hit G4 Step. This deliberately keeps Low self-only, Medium one-Vessel and High paid-Projection expression distinct.

Every policy deliberately chooses **zero discretionary ordinary HP/Repair regeneration** on the recipient's two real Steps. This isolates the genuine G5-induced HP/Vigor injury from the one source Signature packet; it is **not** an optimal recovery policy or a claim that a player should forgo natural regeneration. The enemy attacks **once** in Round 1; Round 2 supplies the delayed High healing window and checks that no extra G5 attack or Step is manufactured. No fabricated injury initial HP assignment, neutral-action ticking, out-of-combat timers, additional Guard or weapon attack by the Anointed is included.

## Native evidence and independently checkable comparisons

Each actual hit is bound to one `g5_melee_sequence_attested`, one G0 enemy Physical `action_committed`, one `g5_melee_resolved` and one G4 `g4_damage_applied`; `foe` profiles are always looked up from the authentic Soldier/Sentry source, including the Sentry's actual prepared G3 Reserved Weapon state. Wound/Dying remains with real G4; these narrow dice/policies intentionally avoid asserting a wound-repair or party-death outcome.

Baseline versus Signature comparisons preserve the **same actor positions, same attack die/damage die, same two G0 Regeneration Steps and same source profiles**. Ordinary effects must improve the beneficiary's post-hit HP by exactly **2 (High)** or **1 (Medium/Low)** while decreasing the *recipient's* remaining Vigor by the identical amount. Lesser effects improve the same HP while consuming **0 additional recipient Vigor** but **1 finite Anointed Destiny**; both leave the Anointed's available VP unchanged and provide no free ordinary technique. No HP appears before its genuine source G5 hit.

A report includes exact bounded scope, policy, source digests, complete native G0–G5 ledger, resulting HP/Vigor/VP/Destiny, G5 action/payment count, Step count, and canonical SHA256 of that ledger. `attest_policy()` recomputes the entire source scene and checks **full equality**, rather than accepting a caller-recomputed digest over forged resource outcomes.

[Focused regression tests](../../tests/test_b05_anointed_native_defensive_encounter_v0.py) cover 54 unique matrix policies, authentic source IDs and paid G5/G4 packets, AP and source-digest provenance, exact baseline/Signature/Lesser HP/Vigor/Destiny deltas at all levels and both opponents, High-vs-Medium-vs-Low delivery timing, two real regeneration Steps, forged report/ledger rejection and unsupported profile/policy denial. The tests do **not** replay unrestricted tactical choices, enemy AI or B07 GM adjudications.

## Readiness and next integration

**This is bounded defensive G5 evidence, not certified combat readiness.** The structural roster stays **12/12**; independently certified complete Focuses **0/12**; strict MVP exits **0/6**. B04–B07 remain open and the existing B06 **G0–G8** milestones are unchanged.

Unimplemented/uncertified areas remain **Anointed source-approved mundane G5 offensive profiles and attacks**, high/medium/low opportunistic attack interactions, contested beneficial **+8 Intrusion** and response-window adjudication, injury/wound/Dying healing edge cases, wider opponent and defender tactics, sustained attrition, actual role comparison, **noncombat** and exploration decisions, and independent legal L1–3 Focus progression and GM pilot approval. The existing native L3 Guided Primary + Authority path (#171) is **not** automatically invoked by this one-Signature comparison; it still needs representative combat/attrition cases before certification.
