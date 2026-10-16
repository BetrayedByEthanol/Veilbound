# B04/B05 — Priest Implementation Checklist (Level 1–3)

> **Status checkpoint: 16 October 2026, after merged PR #77 (Woodland Rapport). Mundane Toxins v0 is proposed **only on the current unmerged PR branch**.** This is a **design/acceptance checklist**, not additional player-facing rules authority. Checkmarks distinguish authored v0 from complete tested Priest Focus builds; costs and toxin parameters remain provisional. Canonical authority: [Priest](../rules/08-archetypes/priest.md), [starting repertoire](b04-b05-priest-scholar-starting-repertoires-v0.md), [Technique Structure](../rules/07-veil-magic/technique-structure-v0.md), [Vital Shelter](../rules/07-veil-magic/vital-shelter-v0.md), [Gentle Growth](../rules/07-veil-magic/gentle-growth-v0.md), [Woodland Rapport](../rules/07-veil-magic/woodland-rapport-v0.md) and [Life boundaries](../world/aspect-identities-and-boundaries.md#life). Parent [roadmap](veilbound-roadmap-and-mvp-readiness.md) tracks B01–B07.

## Status legend and current verdict

- **AUTHORED v0**: Canonical procedure or profile exists and can be executed if the character has legal access and resources. Its numeric balance may remain **PROVISIONAL**.
- **PARTIAL**: A defining Focus mechanic has at least one eligible execution path, but lacks enough alternative choices, level-3 expression, or practical validation.
- **MISSING**: Required technique/property/test has not been authored; a framework or candidate name does not supply it.
- **VERIFIED**: A complete legal character sheet and relevant L1→L3 action/resource test have actually been demonstrated. **None of the three Priest Focuses currently meets this test.**

**Priest state:** Priest starting counts/preparation AUTHORED v0; **two distinct canonical Medium Life Consecrations** (Guided Regeneration, Vital Shelter), **two distinct canonical Low Life `Self` Rite alternatives** (one Active Rite at L1–3), and merged **Gentle Growth / Woodland Rapport** ordinary Life/Nature prayers. **Mundane Toxins v0 is branch-only hazard groundwork**, not a Life technique, extra Priest Rite/Consecration, antidote, poison immunity or Venom Endurance. **No Priest Focus has a certified L1→L3 build**; B04/B05/B07 stay open.

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
| [ ] | Compare at least **two useful L1 preparations** against mixed exploration/attrition/combat; ensure omitting an option matters | **NOT VERIFIED** — five merged Life Tier-1 techniques after PR #77; breadth alone does not verify preparation tradeoffs |
| [ ] | Test Prepared vs Open Invocation vs Open Prayer at L1 and L3, including low VP, interruption, costs, and all-Turn-AP Full Action restriction | NOT VERIFIED end-to-end; individual procedure regression examples exist |
| [ ] | Test positive Accord expanding preparation without eliminating selection pressure; test +1 surcharge as real but not prohibitive emergency flexibility | NOT VERIFIED — balance calibration |

## P2 — Medium Priest: Consecration and Intercession

| Check | Implementation item | Status / evidence |
|---|---|---|
| [x] | Max **one Active Consecration at L1–3**, must be Prepared, paid and maintained | AUTHORED — [Priest](../rules/08-archetypes/priest.md#level-1--consecrated-ministry) |
| [x] | Reassign **same** maintained blessing for **24 AP General Tempo Action**, subject to target constraints and no refresh | AUTHORED — [Priest](../rules/08-archetypes/priest.md#level-1--consecrated-ministry) |
| [x] | **Guided Regeneration maintained** `Single Target` or `Self` is an eligible Consecration: **2 Committed VP**, +1 throughput in existing steps | AUTHORED in merged PR #73; **fixed 2 Spent/one-minute mode is not Consecration** |
| [x] | L3 Intercession framework: **Reaction + 2 Spent VP** (provisional); Guided Regeneration trigger extends +1 to another eligible recipient's **one imminent Regeneration Step** | AUTHORED v0, not a second step/continuous second recipient |
| [x] | **[Vital Shelter v0](../rules/07-veil-magic/vital-shelter-v0.md)** supplies a second functionally different transferable maintained blessing (finite cumulative Vigor-damage prevention; no refresh on Reassign/Intercession) | **AUTHORED in merged PR #75**; VS-01/02 resource, recast and composite balance watches still open |
| [ ] | Compare protection vs recovery as **two distinct preparation/Consecration selections**; check transferring one effect does not change its identity | NOT VERIFIED |
| [ ] | Run L3 Intercession affordability and timing with an active Consecration and another recipient; assess whether **2 Spent VP for +1 throughput** is worthwhile | NOT VERIFIED; cost is provisional |
| [ ] | Confirm at least one full L1→L3 Medium Priest combat+exploration loop without assuming a second simultaneous Consecration before L4 | NOT VERIFIED |

## P3 — Low Priest: Devotion, Exaltation and Active Prayers

| Check | Implementation item | Status / evidence |
|---|---|---|
| [x] | One prepared **Chosen Devotion** at L1; self/equipment anchored; **−1 Committed VP, minimum 1** | AUTHORED — [Priest](../rules/08-archetypes/priest.md#level-1--chosen-devotion) |
| [x] | **Devotional Rite capacity:** **1 Active Rite at L1–3** across Chosen and non-Chosen; **2 Active Rites only at L4+** through Twofold Devotion. Level-2 extra preparation and VP affordability **do not raise** active capacity | AUTHORED shared Priest rule, clarified in **merged PR #75**; second Rite declaration fails before AP/VP commitment when the cap is full |
| [x] | **Guided Regeneration maintained `Self`** is a valid Rite; normal **2 Committed → 1 Committed VP** when Chosen, +1 regeneration throughput | AUTHORED in merged PR #73; the **Spent** one-minute version is **not** a Rite |
| [x] | Low retains ordinary Active Prayer casting when prepared and affordable; Rite commitment competes with scarce VP | AUTHORED — [Priest](../rules/08-archetypes/priest.md#active-prayers) |
| [x] | L3 **Exaltation** structure requires a related **authored secondary property** and additional VP | AUTHORED framework — no compatible Guided Regeneration Exaltation property yet |
| [x] | **[Vital Shelter](../rules/07-veil-magic/vital-shelter-v0.md#low-priest--maintained-self-devotional-rite)** provides an alternative affordable `Self` Rite, Chosen cost **1 Committed + 1 Spent VP** | **AUTHORED in merged PR #75**; Low VA0 L1 ends with **0 Available**. Non-Chosen Shelter costs **2 Committed + 1 Spent**; can replace but **not overlap** another Rite before L4. Meaningful gameplay choice still UNVERIFIED |
| [ ] | Author Guided Regeneration's **specific L3 Exaltation property**, distinct from a mere throughput number bonus; price for Low-Focus VP pool | MISSING |
| [ ] | Test maintain/release/recast, Dying/unconsciousness, available VP for Basic Heal, and L3 Exaltation while Rite active | NOT VERIFIED end-to-end; Guided Regeneration includes individual regression examples |
| [ ] | Demonstrate viable L1→L3 Low Priest preparations with at least **two different Rite decisions**, rather than making the only eligible Rite mandatory | NOT VERIFIED |

## P4 — Life pilot repertoire and Miracle content

The working **Life pilot is a design target**, not a quota that creates spells, and none of the unauthored candidates below is automatically available in play.

| Tier / Aspect | Candidate technique | Current state |
|---|---|---|
| T1 Restoration | **Basic Heal** — instant HP/Vigor restoration | **AUTHORED**, merged PR #64 |
| T1 Restoration | **Guided Regeneration** — +1 throughput; fixed 2 Spent / 1 minute **or** maintained 2 Committed | **AUTHORED**, merged PR #73 |
| T1 Preservation | **[Vital Shelter v0](../rules/07-veil-magic/vital-shelter-v0.md)** — finite Vigor-damage protection, maintained recast watch **VS-01**, High Scholar Secondary with Basic Heal/Stone Skin **VS-02** | **AUTHORED, merged PR #75**, numbers/balance provisional; Conflagration remains a specialist Vigor-burn stress test |
| T1 Preservation | **Venom Endurance** — proposed bounded magical prevention/negation of eligible mundane toxin applications/ticks; must not duplicate Basic Heal's HP/Vigor repair or Vital Shelter's direct-Vigor-only budget | **MISSING technique**. **[Mundane Toxins v0](../rules/05-combat/mundane-toxins-v0.md) is branch-only** source material for 11 Minor/Moderate hazard profiles, Vitality resistance (reduced on success), one-instance nonstacking and short/long duration handling. **No protection spell authored** |
| T1 Nature | **[Gentle Growth v0](../rules/07-veil-magic/gentle-growth-v0.md)** — `Rooted Plant` Primary, 1 Spent VP, 60 sec; one 0.5 m flexible shoot, three mature buds, or one 5 cm seedling; ordinary permanent biological result | **AUTHORED, merged PR #76**; GG-01–04 utility/ecology watches remain provisional; not a Consecration/Rite/Secondary/Rider |
| T1 Nature | **[Woodland Rapport v0](../rules/07-veil-magic/woodland-rapport-v0.md)** — `Single Animal` Primary, Used T1–3: eligible mass **25/125/625 kg inclusive**, ordinary **2/4/6 Spent VP**; external non-compulsory cues 10–30 min by VC, **+2 once** initial peaceful approach | **AUTHORED, merged PR #77**; numerical WR-01–06 watches remain open; no animal commands/companion, Consecration, Rite, Secondary/Rider or separate named Miracle tier |
| T2 Restoration | **Mend Trauma** — direct bounded Repair Progress without reconstructing irreparable wounds | **MISSING** |
| T2 Preservation | **Shared Sanctuary** — shared finite protection budget | **MISSING** |
| T2 Nature | **Instinctive Communion** — bounded animal communication beyond improving disposition | **MISSING** |
| T3 Nature (candidate) | **Entangling Growth** — distinct battlefield-control Miracle candidate, with vegetation/defense boundaries | **MISSING** |

**Current merged Life pilot: T1 = 5/6 candidate Life techniques** (Restoration 2, Preservation 1, Nature 2), covering **3/3 Life Aspects**, after merged PR #77. **Venom Endurance alone remains MISSING** from the six planned Tier-1 candidates; **this toxin hazard PR does not raise the technique count**. **T2 = 0/3 distinct named candidates and T3 = 0/1**; Woodland Rapport's authored higher **Used Tiers 2/3** do not create distinct named Miracle techniques. Animal Companion and magical Death/Plague toxins remain deferred. No L1→L3 Priest build certified.

**Miracles:** Woodland Rapport's normal **Tier-2 option unlocks at L3**, while its normal **Tier-3 option unlocks at L5**; a potential Tier-3 request at L3 must use **separate canonical Miracle Petition procedures** and is **not** automatic ordinary-tier access. These modes **do not** fulfill the target for **distinct Tier-2/Tier-3 Life Miracle techniques**; preserve those acceptance gates and verify actual VP/Petition feasibility.

## P5 — Priest verification scenarios / gates

| Scenario | What to observe | Status |
|---|---|---|
| **L1 High**, initial Accord +1, 4 prepared capacity, 6 Max VP at VA 0 | Prepared Life Restoration/Preservation/Nature options including **merged** Gentle Growth and Woodland Rapport (T1 **2 Spent +20 AP**, or **3 Spent + Full Action** if unprepared under eligible Open Invocation); test against mundane toxin encounter **without an authored Venom Endurance** | **NOT VERIFIED** as a complete build; Nature breadth merged |
| **L1 Medium**, initial Accord +1, 3 prepared capacity, 4 Max VP at VA 0 | **Merged** Guided Regeneration (2 Committed) vs **merged** Vital Shelter (2 Committed +1 Spent, leaving 1 Available); 24-AP transfer never refreshes finite buffer; merged Gentle Growth is an ordinary Nature prayer, **not Consecration** | **TWO CANONICAL OPTIONS**, comparative balance/build tests NOT VERIFIED |
| **L1 Low**, initial Accord +1, 2 prepared capacity, 2 Max VP at VA 0 | Chosen `Self` Guided Regeneration **1 Committed +1 Available** vs Chosen Vital Shelter **1 Committed +1 Spent**; merged Gentle Growth **1 Spent** and merged Woodland Rapport T1 **2 Spent** are separately prepared ordinary prayers, not active Rites. They remain subject to actually Available VP | **TWO CANONICAL RITE ALTERNATIVES; Nature utility AUTHORED**, Focus verification missing |
| **L2–3 Low**, VA0 (Max VP **4/6**), two prepared Rite choices | Attempt **non-Chosen maintained Vital Shelter** while Chosen Guided Regeneration occupies 1 Active Rite; check capacity **before** AP/VP even when the 3-VP cost is affordable. Legal after own-turn release/recast, but no Chosen discount for Shelter unless it was designated during preparation | **SHARED ONE-RITE CAP AUTHORED**, end-to-end tests pending; Level-4 Twofold unlocks two Active Rites |
| **L3 High** | Open Prayer vs Prepared/Open Invocation; merged normal Tier-2 Woodland Rapport (125 kg, **4 Spent** before discounts); test separate Miracle Petition permission and resource affordability. Mundane toxin resistance requires its own Vitality check | **Woodland Rapport T2 AUTHORED**, L3 full build NOT VERIFIED |
| **L3 Medium** | Consecration Intercession cost/range/trigger, normal target regeneration, no duplicated pulse/refill | **PARTIAL PROFILE**, not full build |
| **L3 Low** | An actually authored Exaltation while Chosen Devotion active, action/VP vs martial Tempo and regeneration | **MISSING secondary property** |
| **Accord sweep** | Positive +1/+2/+3 capacity, negative floor, infrequent Advance vs Debt, anti-saturation | **NOT VERIFIED** |
| **Four scene mix** | Combat attrition, a **[mundane toxin](../rules/05-combat/mundane-toxins-v0.md) hazard** with repeat-exposure and Vitality resistance (branch-only), poison-induced HP versus direct Vigor packets, an ordinary animal encounter (T1 wary fox / L3 T2 wolf), and plant-growth exploration; no fictional Venom Endurance cast until authored | **NOT VERIFIED**; provisional toxin TX-01–19 tests and WR-01–06 remain open |

**Graduation criteria:** For each Focus demonstrate **(1) at least two meaningfully different playable preparations, (2) affordable legal L1 uses with VA 0 as a benchmark, (3) working L3 defining ability, (4) preparation/Accord/Invocation/Miracle decisions under mixed scenes, (5) L1→L3 verified sheet/progression**. Before that, classify that Focus as **PARTIAL**, not verified. Then reuse the same tests for Fire, Earth, Mind, Liberty, Kinship, Secrets and Arts without imposing identical spells/roles on each Pillar.

## Immediate order of work

1. **Review/merge [Mundane Toxins v0](../rules/05-combat/mundane-toxins-v0.md)** (current PR only): exposure gating; reduced nonzero result on natural Vitality success; **11 distinct hazard profiles**, one active toxin per recipient and **TX-01–19** watches; short chronological tick batching and long hourly/6-hour events. No Veil poison, recipe, source organism or player-facing Venom Endurance spell yet. Retain merged Woodland Rapport PR #77 and WR-01–06 watches.
2. **Author Venom Endurance v0 (Life/Preservation)** independently, calibrated for **real prospective toxin negation** with finite coverage/timing, not merely the same resource effects as Basic Heal/Vital Shelter. Then a distinct **Guided Regeneration L3 Low Priest Exaltation**; retain Vital Shelter VS-01/02/03 and full damage/VP affordability comparison.
3. **Author representative T2 Life options** for Miracle Petition, then a distinctive T3 candidate or legally authored higher-Used-Tier output, and verify real affordability.
4. **Run High / Medium / Low Priest L1→L3 builds and mixed-scenario tests**; tune the already-authored PR #72 counts, Accord and Open Invocation surcharge using evidence.
5. **Expand the other seven MVP Pillars** using the mechanical-coverage, Focus compatibility and Miracle eligibility tests; B04/B05/B07 certification remains separate from publication of individual spells.
