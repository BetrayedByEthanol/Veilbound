# B04/B05 — Priest Implementation Checklist (Level 1–3)

> **Status checkpoint: 16 October 2026, after merged PRs #72 and #73.** This is a **design/acceptance checklist, not additional player-facing rules**. Checkmarks distinguish a **canonical, executable v0 rule** from a **verified playable build**; a rule being authored does not mean its resource numbers are playtest-approved. Canonical authority: [Priest Foundation](../rules/08-archetypes/priest.md), [starting repertoire v0](b04-b05-priest-scholar-starting-repertoires-v0.md), [HP/Vigor](../rules/06-vigor-wounds-death/hp-and-vigor.md), [Technique Structure](../rules/07-veil-magic/technique-structure-v0.md), and [Guided Regeneration v0](../rules/07-veil-magic/guided-regeneration-v0.md). Parent [MVP Roadmap](veilbound-roadmap-and-mvp-readiness.md) tracks B01–B07 across the complete game.

## Status legend and current verdict

- **AUTHORED v0**: Canonical procedure or profile exists and can be executed if the character has legal access and resources. Its numeric balance may remain **PROVISIONAL**.
- **PARTIAL**: A defining Focus mechanic has at least one eligible execution path, but lacks enough alternative choices, level-3 expression, or practical validation.
- **MISSING**: Required technique/property/test has not been authored; a framework or candidate name does not supply it.
- **VERIFIED**: A complete legal character sheet and relevant L1→L3 action/resource test have actually been demonstrated. **None of the three Priest Focuses currently meets this test.**

**Priest state: framework and starting counts AUTHORED v0; High can use prepared and Open Invocation rules; Medium has one maintained Life Consecration; Low has one maintained Life Devotional Rite; no certified L1→L3 Priest Focus build.** Keep B04/B05/B07 open until those builds and meaningful alternatives are demonstrated.

## P0 — Shared Priest core (merged canon)

| Check | Implementation item | Status / evidence |
|---|---|---|
| [x] | One chosen Pillar; eligible prayers from all three of its canonical Aspects | AUTHORED — [Priest Foundation](../rules/08-archetypes/priest.md#archetype-identity) |
| [x] | Initial Pillar Accord **+1**, independent Resonance **0** | AUTHORED v0 — [PR #72 repertoire baseline](b04-b05-priest-scholar-starting-repertoires-v0.md) |
| [x] | Base Prepared Prayer capacity at L1/L2/L3: **High 3/4/4, Medium 2/3/3, Low 1/2/2** | AUTHORED v0 — [Priest](../rules/08-archetypes/priest.md#archetype-identity) |
| [x] | Effective capacity = **max(1, base + signed Accord + explicit base-capacity modifiers)**; ordinary +1 Accord yields **High 4/5/5, Medium 3/4/4, Low 2/3/3** | AUTHORED v0 — [Priest](../rules/08-archetypes/priest.md#prepared-access) |
| [x] | Initial preparation at creation; subsequent **10 uninterrupted minutes**, at most **once per six elapsed in-world hours**; capacity changes suspend/fill correctly | AUTHORED v0 — [Priest](../rules/08-archetypes/priest.md#prepared-access) |
| [x] | VP scaling by Focus, correct Spent/Committed states, and ordinary Projection AP (High 20 / Medium 24 / Low 30) | AUTHORED — [VP](../rules/07-veil-magic/volition-points.md), [Technique Structure](../rules/07-veil-magic/technique-structure-v0.md) |
| [x] | Accord effect bonus only where technique supports it; avoid +Accord repeated per-turn Guided throughput | AUTHORED boundary — [Priest](../rules/08-archetypes/priest.md#pillar-accord-bonus), [Guided Regeneration](../rules/07-veil-magic/guided-regeneration-v0.md) |
| [x] | Miracle Petition eligibility, **d20 + 2×Accord − 3×Debt vs 12**, Debt on success, Accord Advance choice to deepen or repay | AUTHORED v0 — [Priest](../rules/08-archetypes/priest.md#miracle-petition); numeric/cadence calibration pending |
| [ ] | Test Accord +3 catalogue saturation, negative-Accord floor, real preparation tradeoffs, and infrequent Accord Advance vs persistent Debt | NOT VERIFIED — needs multiple eligible techniques and L1–3 scenarios |
| [ ] | Confirm Miracle Petition's interaction with **higher Used Tier of an existing technique** versus a distinct higher-base-tier technique; test actual VP/action eligibility | NOT VERIFIED — do not infer extra upcasts from tier access |
| [ ] | Finish one fully legal L1→L3 Priest character sheet per Focus, including VP/AP, preparation, L3 features, Gifted/Anointed-independent sources, and common Universals | NOT VERIFIED — B04/B05/B07 acceptance |

## P1 — High Priest: preparation and Open Invocation

| Check | Implementation item | Status / evidence |
|---|---|---|
| [x] | Prepared Prayers use normal eligible technique VP/action; High has highest base preparation capacity | AUTHORED v0 |
| [x] | Open Invocation of **unprepared, chosen-Pillar, normal-tier** technique; ordinary price **plus separate +1 Spent VP**, never discounted | AUTHORED v0 — [Priest](../rules/08-archetypes/priest.md#level-1--high-liturgy--open-invocation) |
| [x] | At L1–4 Open Invocation requires **Full Action consuming entire available Turn AP**; at L5+ ordinary technique action; illegal/interrupted attempts respect VP timing | AUTHORED v0; [Guided Regeneration](../rules/07-veil-magic/guided-regeneration-v0.md) has regression cases for fixed/maintained modes |
| [x] | L3 Open Prayer reserves one **existing** prepared slot and fills it once; **not** a free extra slot, no Invocation surcharge | AUTHORED — [Priest](../rules/08-archetypes/priest.md#level-3--open-prayer) |
| [ ] | Compare at least **two useful L1 preparations** against mixed exploration/attrition/combat; ensure omitting an option matters | NOT VERIFIED — Life currently has only two authored T1 techniques |
| [ ] | Test Prepared vs Open Invocation vs Open Prayer at L1 and L3, including low VP, interruption, costs, and all-Turn-AP Full Action restriction | NOT VERIFIED end-to-end; individual procedure regression examples exist |
| [ ] | Test positive Accord expanding preparation without eliminating selection pressure; test +1 surcharge as real but not prohibitive emergency flexibility | NOT VERIFIED — balance calibration |

## P2 — Medium Priest: Consecration and Intercession

| Check | Implementation item | Status / evidence |
|---|---|---|
| [x] | Max **one Active Consecration at L1–3**, must be Prepared, paid and maintained | AUTHORED — [Priest](../rules/08-archetypes/priest.md#level-1--consecrated-ministry) |
| [x] | Reassign **same** maintained blessing for **24 AP General Tempo Action**, subject to target constraints and no refresh | AUTHORED — [Priest](../rules/08-archetypes/priest.md#level-1--consecrated-ministry) |
| [x] | **Guided Regeneration maintained** `Single Target` or `Self` is an eligible Consecration: **2 Committed VP**, +1 throughput in existing steps | AUTHORED in merged PR #73; **fixed 2 Spent/one-minute mode is not Consecration** |
| [x] | L3 Intercession framework: **Reaction + 2 Spent VP** (provisional); Guided Regeneration trigger extends +1 to another eligible recipient's **one imminent Regeneration Step** | AUTHORED v0, not a second step/continuous second recipient |
| [ ] | Author **another functionally different transferable sustained blessing**, candidate **Vital Shelter** (finite cumulative **Vigor**-damage budget, no refresh on reassignment), not another copy of Guided Regeneration | MISSING; candidate is **not canon** |
| [ ] | Compare protection vs recovery as **two distinct preparation/Consecration selections**; check transferring one effect does not change its identity | NOT VERIFIED |
| [ ] | Run L3 Intercession affordability and timing with an active Consecration and another recipient; assess whether **2 Spent VP for +1 throughput** is worthwhile | NOT VERIFIED; cost is provisional |
| [ ] | Confirm at least one full L1→L3 Medium Priest combat+exploration loop without assuming a second simultaneous Consecration before L4 | NOT VERIFIED |

## P3 — Low Priest: Devotion, Exaltation and Active Prayers

| Check | Implementation item | Status / evidence |
|---|---|---|
| [x] | One prepared **Chosen Devotion** at L1; self/equipment anchored; **−1 Committed VP, minimum 1** | AUTHORED — [Priest](../rules/08-archetypes/priest.md#level-1--chosen-devotion) |
| [x] | **Guided Regeneration maintained `Self`** is a valid Rite; normal **2 Committed → 1 Committed VP** when Chosen, +1 regeneration throughput | AUTHORED in merged PR #73; the **Spent** one-minute version is **not** a Rite |
| [x] | Low retains ordinary Active Prayer casting when prepared and affordable; Rite commitment competes with scarce VP | AUTHORED — [Priest](../rules/08-archetypes/priest.md#active-prayers) |
| [x] | L3 **Exaltation** structure requires a related **authored secondary property** and additional VP | AUTHORED framework — no compatible Guided Regeneration Exaltation property yet |
| [ ] | Author **at least one alternative affordable self/equipment Devotional Rite** to test meaningful L1 selection; a self-compatible Preservation expression is a **candidate**, not automatic | MISSING |
| [ ] | Author Guided Regeneration's **specific L3 Exaltation property**, distinct from a mere throughput number bonus; price for Low-Focus VP pool | MISSING |
| [ ] | Test maintain/release/recast, Dying/unconsciousness, available VP for Basic Heal, and L3 Exaltation while Rite active | NOT VERIFIED end-to-end; Guided Regeneration includes individual regression examples |
| [ ] | Demonstrate viable L1→L3 Low Priest preparations with at least **two different Rite decisions**, rather than making the only eligible Rite mandatory | NOT VERIFIED |

## P4 — Life pilot repertoire and Miracle content

The working **Life pilot is a design target**, not a quota that creates spells, and none of the unauthored candidates below is automatically available in play.

| Tier / Aspect | Candidate technique | Current state |
|---|---|---|
| T1 Restoration | **Basic Heal** — instant HP/Vigor restoration | **AUTHORED**, merged PR #64 |
| T1 Restoration | **Guided Regeneration** — +1 throughput; fixed 2 Spent / 1 minute **or** maintained 2 Committed | **AUTHORED**, merged PR #73 |
| T1 Preservation | **Vital Shelter** — finite Vigor-damage protection; budget needs comparison against repeated Conjure Flame and Basic Heal | **MISSING**, next profile |
| T1 Preservation | **Venom Endurance** — limited poison protection; numeric effects depend on poison procedures | **MISSING** |
| T1 Nature | **Gentle Growth** — modest growth of existing vegetation | **MISSING** |
| T1 Nature | **Woodland Rapport** — improve the disposition of a small ordinarily neutral animal, not compel obedience | **MISSING** |
| T2 Restoration | **Mend Trauma** — direct bounded Repair Progress without reconstructing irreparable wounds | **MISSING** |
| T2 Preservation | **Shared Sanctuary** — shared finite protection budget | **MISSING** |
| T2 Nature | **Instinctive Communion** — bounded animal communication beyond improving disposition | **MISSING** |
| T3 Nature (candidate) | **Entangling Growth** — distinct battlefield-control Miracle candidate, with vegetation/defense boundaries | **MISSING** |

**Current pilot authoring: T1 = 2 of 6 design candidates; T2 = 0 of 3; T3 = 0 of 1.** Two authored Life techniques are from the **same Aspect (Restoration)**. Coverage of Life / Preservation and Life / Nature is **0 techniques each**. **Animal Companion** is a separately deferred future idea, **not** Tier-1 Woodland Rapport or a hidden MVP prerequisite.

**Miracles:** The Tier-1 catalogue alone does not demonstrate an authored **distinct Tier-2 Life Miracle** for levels 1–2, or a **distinct Tier-3 Life Miracle** for level 3. Higher-Used-Tier interpretations of existing spells require explicit legality and affordability checks; never call a named future technique executable.

## P5 — Priest verification scenarios / gates

| Scenario | What to observe | Status |
|---|---|---|
| **L1 High**, initial Accord +1, 4 prepared capacity, 6 Max VP at VA 0 | Different useful preparations; prepared Basic Heal vs unprepared Full Action +1 Spent invocation; +1 throughput mode choice | **NOT VERIFIED** as a full build |
| **L1 Medium**, initial Accord +1, 3 prepared capacity, 4 Max VP at VA 0 | One active maintained Consecration, 24 AP transfer, other prepared prayer; compare two blessing identities once Vital Shelter exists | **PARTIAL PROFILE**, not full build |
| **L1 Low**, initial Accord +1, 2 prepared capacity, 2 Max VP at VA 0 | Chosen `Self` Guided Regeneration 1 Committed leaving 1 Available; cannot cast 2-Spent Basic Heal without releasing Rite or obtaining VP | **PARTIAL PROFILE**, not full build |
| **L3 High** | L3 Open Prayer vs normal preparation and Open Invocation Full Action, legitimate T2 accesses, Miracle check | **NOT VERIFIED** |
| **L3 Medium** | Consecration Intercession cost/range/trigger, normal target regeneration, no duplicated pulse/refill | **PARTIAL PROFILE**, not full build |
| **L3 Low** | An actually authored Exaltation while Chosen Devotion active, action/VP vs martial Tempo and regeneration | **MISSING secondary property** |
| **Accord sweep** | Positive +1/+2/+3 capacity, negative floor, infrequent Advance vs Debt, anti-saturation | **NOT VERIFIED** |
| **Four scene mix** | Short combat, multi-round attrition, poison/biological hazard, woodland social/exploration | **NOT VERIFIED** |

**Graduation criteria:** For each Focus demonstrate **(1) at least two meaningfully different playable preparations, (2) affordable legal L1 uses with VA 0 as a benchmark, (3) working L3 defining ability, (4) preparation/Accord/Invocation/Miracle decisions under mixed scenes, (5) L1→L3 verified sheet/progression**. Before that, classify that Focus as **PARTIAL**, not verified. Then reuse the same tests for Fire, Earth, Mind, Liberty, Kinship, Secrets and Arts without imposing identical spells/roles on each Pillar.

## Immediate order of work

1. **Vital Shelter v0**: author finite Vigor protective budget, mixed HP/Vigor interaction, duration or maintained mode, Medium Consecration, no-refresh, costing against Conjure Flame and Basic Heal. Consider a separately legal affordable `Self` Rite profile only if it meaningfully supports Low's choices.
2. **Complete Tier-1 Life breadth** (Preservation and Nature), and **explicit Low Rite alternative plus L3 Guided Regeneration Exaltation**.
3. **Author representative T2 Life options** for Miracle Petition, then a distinctive T3 candidate or legally authored higher-Used-Tier output, and verify real affordability.
4. **Run High / Medium / Low Priest L1→L3 builds and mixed-scenario tests**; tune the already-authored PR #72 counts, Accord and Open Invocation surcharge using evidence.
5. **Expand the other seven MVP Pillars** using the mechanical-coverage, Focus compatibility and Miracle eligibility tests; B04/B05/B07 certification remains separate from publication of individual spells.
