# B04/B05 — Restricted MVP Pilot Roster and Gifted/Anointed Readiness v0

> **Historical PR #149 candidate roster, with 31 October 2026 current overlay:** All 12 Archetype × Focus structural pairings have since been merged. **#179** approved Low Gifted Rooted Guard **+1** / Unbound Step **−1 MP**, restricted authored numbers under watch and two GM-declared L2/L3 milestone awards; **#180** added bounded native Low Gifted Guard/Dodge/MP receipts; **#181** independently audited 12 pairings / 39 snapshots and **#182** fixed three source Talent ledgers. The 13 Tier-1 identities / 10 of 24 selected-Aspect count has been rechecked against individual source pages. Old "missing six Focuses" and "decision needed" tables below are **as-of-#149 history, not active work**. Current source: [roadmap](veilbound-roadmap-and-mvp-readiness.md), [acceptance register](b04-b07-mvp-acceptance-register-refresh-v0.md) and [approved watches](b04-b05-b07-mvp-pilot-approvals-and-watches-v0.md). **12/12 structural, 0/12 independently full certified, 0/6 strict exits, 3/7 blockers closed.**

> **Planning / authoring audit, not canonical game rules, new magic, new player entitlements, or an MVP certificate.** Source checkpoint: `main` after merged PR #149 (25 October 2026). All examples below require the actual source-authored Archetype, Focus, level, tag, AP, VP, target and mode permissions; a restricted **pilot fixture** is not a repeal of broader world or character-creation canon. The active [MVP readiness register](veilbound-roadmap-and-mvp-readiness.md) remains authoritative for merged progress.

## Scope and decision boundaries

- **Already decided:** the first level 1–3 tabletop pilot covers **all 12** Archetype × Focus identities, combat **and** noncombat, advancement and a 3–5-session adventure. The selected **eight-Pillar authoring roster** is Fire, Life, Earth, Liberty, Mind, Kinship, Secrets and Arts ([selection decision](b05-eight-pillar-mvp-selection-and-coverage.md)). All 16 Pillars and 48 Aspects remain canonical.
- **Pilot restriction proposed/accepted in planning:** prefer a **restricted, declared menu of source-usable options** rather than implying that all 24 Aspects from the eight Pillars already offer full playable repertoires. This limits the test-adventure content contract, **not** a general permanent ban on other valid character choices; the exact final pilot roster cannot be marked approved until each required Focus-specific expression is authored.
- **No permission by resemblance:** a technique tagged [Projection], [Embodiment], Self, Weapon Enchantment, or merely named for an Aspect is **not** automatically a Gifted Amplification, Conduit, Anchor benefit, Anointed 0-VP Signature, Destiny Authority, Scholar Inward Boost or Priest Rite. See [Gifted](../rules/08-archetypes/gifted.md), [Anointed](../rules/08-archetypes/anointed.md) and [technique structure](../rules/07-veil-magic/technique-structure-v0.md).
- **Counting:** unique individually authored base-Tier-1 technique **identities** (not cast profiles, modes, upcast Used Tiers, Focus reconfigurations, Universals, Exaltation properties or tools). A covered Aspect has ≥1 such executable technique. A covered Aspect is **not** fully built for all Archetypes/Focuses. Published effects do not automatically grant access.

## Fresh source-backed Tier-1 identity census

The 25 October 2026 census inspects the current individual files in `docs/rules/07-veil-magic/`, not the October 15 historical [starting-access audit](b04-b05-archetype-access-and-starting-repertoire-audit.md). All **13** named base-Tier-1 Pillar-technique identity files below are distinct; they cover **10 of the selected 24** Aspects, leaving **14/24 without an individually authored base-Tier-1 identity**. These are design/source profiles; numerical balance can remain provisional. Higher Used Tier in a single technique is **not** a distinct authored base-Tier-2 technique.

| Pillar / Aspect | Individually authored base-Tier-1 techniques | Count |
|---|---|---:|
| Fire / Conflagration | [Conjure Flame](../rules/07-veil-magic/conjure-flame-v0.md) | 1 |
| Life / Nature | [Gentle Growth](../rules/07-veil-magic/gentle-growth-v0.md), [Woodland Rapport](../rules/07-veil-magic/woodland-rapport-v0.md) | 2 |
| Life / Preservation | [Vital Shelter](../rules/07-veil-magic/vital-shelter-v0.md), [Venom Endurance](../rules/07-veil-magic/venom-endurance-v0.md) | 2 |
| Life / Restoration | [Basic Heal](../rules/07-veil-magic/basic-heal-v0.md), [Guided Regeneration](../rules/07-veil-magic/guided-regeneration-v0.md) | 2 |
| Earth / Fortification | [Stone Skin](../rules/07-veil-magic/stone-skin-v0.md) | 1 |
| Liberty / Defiance | [Weaken Restraints](../rules/07-veil-magic/weaken-restraints-v0.md) | 1 |
| Mind / Psionics | [Minor Telekinesis](../rules/07-veil-magic/minor-telekinesis-v0.md) | 1 |
| Kinship / Guardian | [Protective Ward](../rules/07-veil-magic/protective-ward-v0.md) | 1 |
| Secrets / Hallucination | [Phantom Sound](../rules/07-veil-magic/phantom-sound-v0.md) | 1 |
| Arts / Inspiration | [Spark of Inspiration](../rules/07-veil-magic/spark-of-inspiration-v0.md) | 1 |
| **Total** | **13 distinct technique identities / 10 distinct Aspects** | **13** |

### Selected-Aspect coverage, with blanks explicit

These Aspects are taken from the [eight-Pillar roster's canonical table](b05-eight-pillar-mvp-selection-and-coverage.md#selected-roster--canonical-domain-and-initial-mechanical-hypothesis); **covered** means individual Tier-1 technique identity exists, not Focus viability.

| Pillar | External | Internal | Transform | Covered / 3 |
|---|---|---|---|---:|
| Fire | Conflagration **covered** | Warmth **missing** | Forge **missing** | 1 |
| Life | Nature **covered** | Preservation **covered** | Restoration **covered** | 3 |
| Earth | Quake **missing** | Fortification **covered** | Bounty **missing** | 1 |
| Liberty | Exploration **missing** | Autonomy **missing** | Defiance **covered** | 1 |
| Mind | Psionics **covered** | Insight **missing** | Memory **missing** | 1 |
| Kinship | Guardian **covered** | Sacrifice **missing** | Unity **missing** | 1 |
| Secrets | Shadow **missing** | Deception **missing** | Hallucination **covered** | 1 |
| Arts | Performance **missing** | Inspiration **covered** | Creation **missing** | 1 |
| **Total** | | | | **10/24 covered; 14 missing** |

**Scope boundary:** [Universal Veil Inspection](../rules/07-veil-magic/veil-inspection-v0.md) (L1), [Blink](../rules/07-veil-magic/blink-v0.md) (L3), [Scholar Inward/Embodiment profiles](../rules/07-veil-magic/scholar-inward-embodiment-profiles-v0.md), and [Life Exaltation properties](../rules/07-veil-magic/life-exaltation-properties-v0.md) are **not additional Pillar-technique identities**. No blanket Tier-2 completeness claim is made: some existing T1-base techniques author higher Used Tier modes (for example Conjure Flame, Minor Telekinesis, Basic Heal and Woodland Rapport), while others explicitly do not. L3's ceiling is not a free spell.

## Restricted pilot candidate menu — not yet executable for all twelve

This is a **test-adventure menu of candidate build fixtures**. It is not a new universal character-creation rule. Current source-supported Priest and Scholar rows are reference builds; Gifted/Anointed rows remain **pending specific content**.

| Archetype / Focus | Pilot candidate restriction | Verified versus still blocked |
|---|---|---|
| Priest High / Medium / Low | **Life** chosen Pillar; use the existing three separate H/M/Low Life L1–3 source builds, their eligible prepared Life prayers, Consecration and Chosen Rite/Exaltation where actually qualified | **6/12 shared Priest/Scholar structural total** includes these 3; bounded native evidence, **not** independent full combat+noncombat certification |
| Scholar High | Existing **Fire** F L1–3 structural candidate with only individually learned, source-legal techniques and explicitly compatible composite profiles | Structural/native; known technique count and eligible formula remain source-bound; not general cross-Pillar grant |
| Scholar Medium | Existing **Earth/Life Inward** S candidate (Stone Skin and Guided Regeneration with **explicit** authored Inward profiles) | Structural/native; not automatic reclassification of all Self spells |
| Scholar Low | Existing **Earth/Life Embodiment** T candidate (authored Stone/Guided Self profiles), with its prepared subset and legal paid switch | Structural/native; no generic low-cost Conjure Flame Reserve at L1 VA0 |
| Gifted High / Medium / Low | Eight **distinct emotion–Aspect** links spanning **eight distinct Pillars**, using only the eight already authored Aspects in the source-verified **6 Strong / 2 Plausible** fixture below | Legal *link scaffold* and ordinary conditional technique access, but **zero** Gifted Focus pairings structurally complete until expression rules exist |
| Anointed High / Medium / Low | **Candidate for design review: Life / Restoration** bond across all three Focus test builds, with one explicitly authored Birth Imprint/Mission package and future High projected, Medium invested and Low embodied Signature/Authority expressions | Existing Basic Heal/Guided Regeneration are normal bonded techniques **only**; no 0-VP Signature or Authority is yet authored. The specific bond/Birth Imprint package requires approval before canonical effect authoring |

The narrow choice of Life/Restoration for **Anointed is a proposal**, not a resolved design decision or permission to repurpose Basic Heal as a Signature. Other source-backed Aspects could be evaluated before selecting a bonded-Aspect vertical slice. The three Anointed must each have **one Aspect bond**, not an implied second pillar. Character-sheet choice of a particular Mission/Birth Imprint requires actual authoring and approval.

### Gifted pilot candidate — eight authored Aspects, source-legal 6S/2P

From the independently checked example in the [historical compatibility/access audit](b04-b05-archetype-access-and-starting-repertoire-audit.md#gifted-compatibility-important-distinction-between-two-valid-constructions), **not** the different eight-Strong sample in the eight-Pillar selection document. S = Strong; P = Plausible and **needs a coherent emotion interpretation at creation**, without any lower post-creation mechanical effectiveness.

| Emotion | Aspect link | Rating | Authored ordinary technique |
|---|---|:---:|---|
| Joy | Fire / Conflagration | P | Conjure Flame |
| Sadness | Life / Restoration | S | Basic Heal; Guided Regeneration |
| Anger | Mind / Psionics | P | Minor Telekinesis |
| Fear | Earth / Fortification | S | Stone Skin |
| Surprise | Secrets / Hallucination | S | Phantom Sound |
| Disgust | Liberty / Defiance | S | Weaken Restraints |
| Trust | Kinship / Guardian | S | Protective Ward |
| Anticipation | Arts / Inspiration | S | Spark of Inspiration |

**Important counterexample:** the separate **all-Strong** example links Anticipation to **Mind / Insight**, which has **no authored T1 technique**. Do not claim eight executable paths from that example. The 6S/2P sample has eight authored ordinary technique identities, but each is usable **only in its matching Active Emotion window**, with actual level, VP, action, targeting and trigger legality. It does not automatically provide eight eligible Amplification options, eight Conduit outputs, or eight Embodied Expressions. The **same legal eight-link scaffold** can be used to compare three Focuses without erasing their different identities or emotion restrictions.

## Six unfinished Focus implementation contracts

| Focus | Already defined in canonical rules | Missing authored content and v0 acceptance witness |
|---|---|---|
| **High Gifted (A08)** | Emotion Window, Heightening, Deepen Emotion, one Projected Surge allowance per Window, eligible [Projection] restriction | **Proposed design slice:** author a **technique-specific** Conjure Flame `Thrown Projectile` Amplification choice with explicit output/duration and legal modifier category; settle v0 Surge VP surcharge (source says approximately 25% of ordinary technique VP, minimum 1, **provisional**). Verify naturally Heightened vs paid Deepen, surge allowance and off-turn expiration, insufficiency, Instability when applicable. L1 **24-AP Deepen + 20-AP Projection cannot occur in one 30-AP turn**; do not certify that invented combo. |
| **Medium Gifted (A09)** | Grade I/II/III Conduits reserve **1/2/3 Committed VP**, one Conduit L1 and two L3; active-emotion retuning, unsupported Form becomes Dormant; **24 AP + 3 Spent VP** Reconduction at L1–3 | **Proposed design slice:** one named Form (for example **Ward**), at least two **explicit** compatible linked-Aspect/Grade outputs with documented continuous/Pulse/Spend limits; unsupported Active Emotion yields actual Dormant state. Test Grade affordability (at VA0 L1 Max VP 4), legitimate reroute/Reconduction after commitment, collision with ordinary paid casts and exact refresh per Emotion Window; no copied Stone Skin/Protective Ward or free defense. |
| **Low Gifted (A10)** | Anchored Emotion, **24 AP** voluntary Break Anchor, automatic prior Anchor re-establishment absent disruption, L2 Instinctive and L3 Settled Emotion | **Proposed design slice:** one **self-centered**, finite-budget Earth/Fortification Anchor benefit and one differently linked source-qualified alternate Anchor expression; define activation, cadence, host and termination. Test actual persistence, lost benefit on Break/disruption, legal physical integration without free action, and no assumed permanent Stone Skin from ordinary access. |
| **High Anointed (A11/A12)** | Single permanent bond, Mission, Birth Imprint, **0 VP** High [Signature][Projection], compatible Destiny-priced Authority | **Proposed design slice:** author one named Life/Restoration projected Signature with bounded useful output, exact action/targets/scale and at least one eligible Destiny Authority. Verify 0-VP Signature distinct from paid Basic Heal and **L2 projection / L3 Authority compatibility** without free technique. |
| **Medium Anointed (A11/A12)** | One invested Vessel; establish/change normally **24 AP and 0 VP**, Release free; Source-specific persistence/range | **Proposed design slice:** same candidate bond with named Invested Signature output on a legal Vessel and compatible Authority. Test reassignment, changed target, duration and no invented remote casting or area Vessel. Hostile Investment delivery remains **out of pilot scope unless chosen**. |
| **Low Anointed (A11/A12)** | Self-centered persistent **0-VP** embodied Signature, physical integration L2, compatible Incarnate Authority L3 | **Proposed design slice:** same bond with one named self/worn-gear Signature, bounded cadence and Destiny-paid Authority; test sustained output, ordinary physical action, termination, and strict ban on free full-strength healing per swing, extra AP/Guard or a duplicate complete technique event. |

**All proposed slices are DESIGN INPUTS, not newly approved numeric profiles.** A PR may implement existing foundation infrastructure without approving these missing effects, but it may not use placeholders to certify a Focus. Each eventual effect PR must identify: exact Aspect and profile, minimum level/Tier, AP/Reaction, normal Spent/Committed VP and/or Destiny, target/range, interaction/defense, duration and cadence, legal mode/tag host, expiry, examples, negative cases and level-specific affordability. Preserve the [selected Aspect's conceptual boundaries](../world/aspect-identities-and-boundaries.md).

### Decision register

| Decision | Current state | Next authorized action |
|---|---|---|
| Eight authoring Pillars, 12 pairings, restricted **pilot** scope | Existing planning direction; no expansion of world rules | Implement and test the explicitly listed **candidate fixtures**; do not grant an unrestricted selection menu |
| Exact **Gifted** Amplification/Conduit/Embodiment effects | **NEEDS CONTENT DESIGN / APPROVAL** | Write source-constrained effect profiles as a separate PR, review the numeric budgets, then implement |
| High Gifted Projected Surge numeric surcharge | Approximate 25% / min 1 benchmark **not locked** | Propose and test an exact integer formula before declaring full High Gifted readiness |
| Anointed bond choice, Birth Imprint/Signature/Authority package | **Life / Restoration is only a candidate**; **NEEDS DESIGN / APPROVAL** | Agree on one complete bonded-Aspect slice and separate 0-VP/Destiny-priced outputs |
| Anointed Destiny capacity and recovery | Provisional canonical baseline **Max 2 + floor(L/5)**, 25% per six-hour interval (minimum 1) | Use as expressly provisional playtest assumption; change only on evidence and approval |
| Medium Anointed hostile delivery, full Aspect catalogue and high-level features | Not needed for proposed L1–3 pilot if authoring avoids them | Defer unless a chosen actual scene demands them |
| Pilot level-up awards | XP/milestone policy not canonical; mechanical Talent/AP/VP awards already sourced | Propose **milestone leveling** for the 3–5-session pilot, then record explicit awards in adventure |
| B06 G0–G8 integration and numeric encounter challenge | Original bounded v0 implementation delivered; representative evidence still missing | Do not create G9; finish representative packs after source-legal players, do not assign numeric Hunter CR prematurely |

## MVP implementation order and stop/go conditions

1. **B04/B05 content PRs:** approve and author Gifted amplification/conduit/anchor effects, then High/Medium/Low **independent** L1→L2→L3 source-state builds; a fully legal eight-link arrangement alone does not certify any Focus.
2. **B04/B05 content PRs:** approve one Anointed bonded-Aspect Birth Imprint/Signature/Authority family, implement three independent Focus source builds and resource/host refusal cases. Ordinary techniques never stand in for the Signature.
3. **B04/B07 acceptance:** independently review twelve real legal character records, each with mandatory choices, combat and noncombat proof, level-step resource arithmetic, affordable source actions and explicit negative/countercases. Preserve 6/12 structural and **0/12 independent certificates until merged evidence changes them**.
4. **Parallel short integration:** replay the newer [#148 native Sword Opportunity](b06-native-offturn-opportunity-attack-resolution-v0.md) in Scholar mobile/two-Soldier scenes; keep #147's nine historical pending probes unchanged.
5. **B06 and pilot:** deliver representative varied GM Soldier/Sentry/Hunter packs, authored exploration and social/investigation scenes, complete outcome/withdrawal/aftermath records, milestone awards and **observed human/GM** 3–5-session playtests. No numeric Hunter CR or global balance certificate until justified.

**Gate:** This document only closes the **inventory/readiness planning task**. It does **not** close B04, B05, B06 or B07; add a character pairing to structural 6/12 only after genuinely authoring and verifying it, and mark a strict MVP exit gate passed only with independently reviewed end-to-end evidence. No `docs/rules/`, `content/`, engine, paid cost, creature statistics or frozen historical report changes are authorized here.
