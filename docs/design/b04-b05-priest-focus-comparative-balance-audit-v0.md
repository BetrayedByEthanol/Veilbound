# B04/B05 — Priest Focus Comparative Balance Audit v0 (L1–3)

> **Decision:** retain the current provisional High / Medium / Low Priest numbers; **no Focus is proven over- or underpowered** by the available evidence. A reproducible comparison of rules is possible, but a matched three-Focus opposed encounter and cost-equivalence calibration are **not yet possible**. No canonical mechanic, spell effect, VP cost, or gate is changed in this audit.

## 1. Evidence tiers and comparison method

1. **Canonical Focus rules (source-defined):** [Priest Foundation](../rules/08-archetypes/priest.md), [Turn AP and Tempo](../rules/05-combat/action-categories-and-physical-tempo.md), [Volition Points](../rules/07-veil-magic/volition-points.md), [HP/Vigor Regeneration](../rules/06-vigor-wounds-death/hp-and-vigor.md), [Basic Heal](../rules/07-veil-magic/basic-heal-v0.md). These establish all-Focus capacities/costs but do not provide three finished sample characters.
2. **Selected character witnesses (not identical talent policy):** [Low Life A/B L3 build and Exaltation](b05-life-low-priest-l3-build-exaltation-verification-v0.md) documents two legal Low Priest choices, real chosen Rite/Exaltation procedures and hand/equipment limitations. G0's `A` is only a **physical proxy** for A's build, not a complete Low Priest spell/Exaltation runtime. [Medium Life L1–3 build](b04-b05-medium-priest-life-l1-l3-build-consecration-verification-v0.md) supplies one source-selected M with TAL-C02 (L1) and TAL-M03 (L3); Basic Heal and Consecrations have actual runtime adapters. **There is not yet a correspondingly audited High Priest Life L1–3 character sheet or native encounter pilot.**
3. **Native opposing encounter evidence (Medium only):** [PR #129's two-round integration](b04-b05-medium-priest-life-l1-l3-encounter-integration-balance-verification-v0.md) supplies **27** legal Level/foe/policy cells against authentic Soldier and *prepared* Firebound Sentry. Actual G0/G1/G3/G4/G4.5/G5 payments/packets are executable. The policy/face/defense choices are deliberately fixed; neither Low nor High was run through the same native opposed support policy. Do **not** compare a fully executed M against hypothetical Low/High damage, win rates or invented cast throughput.

`scripts/b05_priest_focus_comparative_balance_audit_v0.py` first checks **actual numeric payment declarations** (including Open Invocation +1 Spent and Full Action, Basic Heal 2×T Spent, Guided 2 Committed, Vital Shelter 2 Committed +1 Spent / B8, Low Chosen −1 Committed, Medium Intercession 2 Spent, and TAL-M03's limit) before any witness is accepted, then checks its normalized M numbers against the actual selected M profile and Low against G0's A physical proxy. It imports the merged native M matrix rather than re-simulating hits or fabricating Low/High encounters. All returned full reports include **SHA-256 hashes of the exact UTF-8 bytes** of their canonical rules, build evidence, and encounter-source scripts; the stored character count is diagnostic only. The audit digest includes those per-file hashes. A same-length source edit therefore changes the signed result, and a conflicting modeled numeric declaration **fails closed** rather than issuing a new report with an obsolete cost. `attest()` independently rebuilds from current source files and rejects stale original reports and rehashed edits.

**Normalization:** **VA 0**, **VIT +2**, **HP 12**, **Life Pillar**, **starting Accord +1**, no TAL-P01, no free VP, no bonus encounter resource. These are *identical reference inputs*, **not** new High Priest or alternate Low Priest character creation choices. In particular the underlying Focus-rate Regeneration below is **before** any selected TAL-C02; Low A and M actually select C02 for **+1 additional throughput**. Never attribute that +1 to every Priest of their Focus. Equipment, armor, weapon talents, guards beyond ordinary physical tempo, hand freedom, and spell availability are not held equal across their actual character sheets.

## 2. Strict equal-stat Focus progression

| Measure | High L1 / L2 / L3 | Medium L1 / L2 / L3 | Low L1 / L2 / L3 |
|---|---|---|---|
| Max VP (VA0) | **6 / 12 / 18** | **4 / 8 / 12** | **2 / 4 / 6** |
| VP restored per *completed* six hours (half-up 25% Max) | **2 / 3 / 5** | **1 / 2 / 3** | **1 / 1 / 2** |
| Shared Turn AP | **30 / 36 / 42** | **30 / 36 / 42** | **30 / 36 / 42** |
| Cost Physical / Projection | **30 / 20 AP** | **24 / 24 AP** | **20 / 30 AP** |
| Max derived Physical Tempo | **1 / 1 / 1** | **1 / 1 / 1** | **1 / 1 / 2** |
| Max derived Projection Tempo | **1 / 1 / 2** | **1 / 1 / 1** | **1 / 1 / 1** |
| General Tempo | **24 AP** | **24 AP** | **24 AP** |
| Base native regeneration with VIT+2, *before Talents or Guided* | **3** | **4** | **5** |
| Prepared Prayer capacity with Accord+1 | **4 / 5 / 5** | **3 / 4 / 4** | **2 / 3 / 3** |
| Normal max Guard uses at equal no-feature equipment | **1 / 1 / 1** | **1 / 1 / 1** | **1 / 1 / 2** |

**No L1–3 Focus can fit a Physical Action and Projection Action in the same normal Turn AP** (High 30+20=50, Medium 24+24=48, Low 20+30=50, each exceeding the Level-3 maximum 42). L3 High can project twice (40/42) where Medium projects once (24/42) and Low can take two ordinary Physical Actions (40/42). This is *opportunity cost*, not evidence that either Focus gains free damage or a second spell under technique-specific cadence limits. All three have one standard Reaction each round unless other rules explicitly adjust it. Guard capacity does not deplete merely because a priest projected in their turn.

**Prepared slots are capacities, not six free Life techniques.** The Priest can fill only distinct eligible authored chosen-Pillar techniques at the permitted tier, in a legal preparation window. Accord decline suspends excess entries immediately; TAL-P01 optionally adds +1 base capacity **only when legitimately selected**. Inspection/Blink do not fill these slots, and Blink may be known but unaffordable (Low A at L3 has only VP6 against Blink's 10 Spent).

## 3. Comparable Life technique payment and role differences

The following compares **actual canonical costs under conditional legal access**, not universally prepared or independently certified spell effects.

| Action or state | High Priest | Medium Priest | Low Priest |
|---|---|---|---|
| Ordinary prepared T1 Basic Heal | **20 AP + 2 Spent VP** | **24 AP + 2 Spent VP** | **30 AP + 2 Spent VP** |
| Maintained Guided on self, undiscounted | 20 AP + **2 Committed VP** | 24 AP + **2 Committed VP** | 30 AP + **2 Committed VP** |
| Maintained Guided **chosen** self Rite | Not a High Priest feature | Not a Medium Priest feature | 30 AP + **1 Committed VP**, one active Chosen instance |
| Maintained Vital Shelter | 20 AP + **2 Committed + 1 Spent** | 24 AP + **2 Committed + 1 Spent** | 30 AP + **2 Committed + 1 Spent**; if Chosen Self Rite: **1 Committed + 1 Spent** |
| Unprepared authored normal-tier Life Basic Heal | **Full Action + 3 Spent VP** (2 normal +1 separate surcharge) | No Open Invocation | No Open Invocation |
| L3 distinguishing feature | **Open Prayer:** one of existing five prepared slots is unspecified until first legal use, no surcharge on that filling | **Intercession:** one Reaction + **2 Spent VP**, existing host only, one valid event/recipient, no refresh | **Exaltation:** only a named compatible active Chosen Rite, property-specific timing and Spent price (first Life options: **1 Spent VP** each) |

High's **+1 Open Invocation surcharge**, Medium's **2 Spent Intercession**, and the authored Low property prices are all provisional. Open Invocation requires a truly eligible unprepared normal-tier spell and 1–4-level **Full Action**; it cannot be treated as a free fifth or sixth Prepared Prayer, tier unlock, alternative Miracle Petition, or a new spell. A Low **ally-targeted** maintained Guided is **not** a self/equipped-item Rite and cannot claim a chosen discount or Chosen Exaltation; Medium Reassign moves the one existing budget/host, spending a **24-AP General Action**, rather than creating output. All three still retain ordinary authored prepared magic in addition to their respective feature.

**Resource snapshots, normalized L3 full VP:** High 18 Available after a normal Guided reserve -> **16 Available / 2 Committed**; Medium 12 -> **10 / 2**; Low 6 chosen self Guided -> **5 / 1** (ordinary non-Chosen would be **4 / 2**). Reserving is not Spent VP; future use of these Available VP requires its own valid action/technique. Low TAL-C02 and Medium TAL-C02 each add +1 selected Regeneration throughput to their equal-stat base (result **6 Low** and **5 Medium**); High has *no selected High build* to which we may assign an equivalent Talent. At L3 the selected Medium TAL-M03 **can** discount a single otherwise legal technique's ordinary Spent VP component ≥2 by 1, once on its own turn, but the PR #129 Basic Heal/Intercession fixed-policy evidence **does not exercise** that optional discount, and it never reduces a separate Invocation surcharge, Committed VP, or makes one Intercession automatic.

## 4. What the actual Medium encounter tests establish

The reproducible L3 paired comparison in the same two real G5-attacked Soldier/Sentry setup finds:

- **Direct Guided on ally vs self Guided + L3 Intercession:** the same ally HP/Vigor outcome for this selected two-round policy; Intercession uses **2 Reactions and 4 more Spent VP** while keeping the host's 2 Committed VP. This is a timed delivery alternative, not extra throughput granted for free.
- **Direct Shelter on ally vs self Shelter + L3 Intercession, prepared Sentry only:** same ally HP/Vigor under the selected Vigor packets, again **2 Reactions and 4 more Spent VP**, consuming the same original finite B8 host budget. The Soldier produces no native direct Vigor packet and cannot authorize this Shelter Intercession path.
- **Basic Heal:** Medium's valid Single Target T1 receipt spends 24 AP and 2 VP to restore bounded HP and Vigor (no extra Regeneration Step); its value depends on missing HP/Vigor, hand availability, Intrusion permission, timing, and other simultaneous opportunities.
- **Low A/B fixtures:** TAL-C10, EX-LR-01 Held Renewal, and EX-LP-01 Vital Interposition establish meaningful alternatives (pre-hit talent healing, later-Step held recovery, finite HP prevention), but **their older after-mitigation fixture comparisons are not identical native G5 attacks against the same foe**. They cannot be translated into a win-rate, damage-prevention superiority, or a 2-VP Intercession cost verdict.
- **High Priest:** The larger VP, projected tempo, preparedness and Full-Action Open Invocation cost are **rules projections** until High Life gets a legal fully sourced L1–3 character and source-native opponent pilots.

### Explicit numerical watches, no retuning yet

| Watch | Evidence and risk | Required before changing values |
|---|---|---|
| **High access vs Medium redistribution** | High opens more prepared expressions and has L3 two Projection actions; Medium trades breadth for 24-AP Reassign and event-based Intercession | Same eligible authored Life repertoire and native coordinated encounters, declared strategies and pressure variation |
| **Intercession 2 VP + Reaction** | In the v0 two-round paired policy, pays 4 more VP for the same target outcome; price may punish mobility but may be necessary flexibility cost | Move targets, alternative pressures, multiple incoming legal packets, exhausted B8, reactions contested by defense, VP recovery across fights |
| **Low Chosen and Exaltation** | A Low with chosen self-Guided commits1 instead of2; two authored Life Exaltations add distinct output for Spent prices; strong body tempo but scarce VP | Authenticated Low full spell/Exaltation rotation against same foes, wound/toxin mix, loadout hand limits, actual threat-facing roles |
| **Accord / preparation** | 4/3/2 effective at L1, 5/4/3 at L2–3; High slots may exceed actual authored repertoire diversity | Real repertoire overlap, 10-minute prep policy, Accord variation (−3..+3), broader Aspect catalogue |
| **Recovery and attrition** | High VP6/12/18 vs Medium4/8/12 vs Low2/4/6, six-hour recovery 25% half-up | More than two rounds and multiple real world-time encounters; no invented encounter reset or VP refresh |
| **Miracle Petition** | Shared conditional permission, provisional d20 +2×Accord −3×Debt vs12, success has Debt | Explicit rare-attempt policy and authored outcomes; not a repeatable known spell or free VP |

## 5. Decision, acceptance and follow-on PRs

**Keep the current L1–3 numbers unchanged.** The arithmetic and existing Medium paired evidence establish real tactical/resource differences, not a statistical or qualitative global balance ranking. **0/12 independent full archetype/Focus MVP certifications remain** and the previously locked B04/B05/B07 strict gates are unchanged.

Recommended continuation, in dependency order: (1) High Priest Life L1–3 legal build, prepared and Open Invocation execution with source G0/G3/G4 receipts; (2) Low Priest Life A/B native G5/G4 spell/Chosen Rite/Exaltation encounter integration with meaningful enemy pressure and hand/equipment legality; (3) a shared matched L1–3 three-Focus tactical matrix on the same opposing source encounters, actual party choices and six-hour attrition, with no guessed win probabilities; (4) only then adjudicate costs for High Open Invocation, Medium Intercession and Low Exaltation.

### Commands

`python -m scripts.b05_priest_focus_comparative_balance_audit_v0 --seed 0`

`python -m unittest tests.test_b05_priest_focus_comparative_balance_audit_v0 -v`

`python -m unittest discover -s tests -v`

Audit output contains **9** normalized Focus/level progressions, actual selected Low/M source witnesses, **27** real native Medium policy summaries and **3** L3 paired direct/Intercession contrasts. Changed or missing **modeled numeric cost declarations** cause the audit to fail before reporting any witness. Both a price change (same-length +1→+2) and a non-price same-length source edit are covered by dedicated regressions; every source file has a SHA-256 content fingerprint rather than a character-count substitute. Arbitrary edited or self-rehashed output, or a report from a different source revision, does not pass independent replay. No High character/encounter, Low complete spell encounter, objective balance score, sampled win rate or CI sign-off is invented.
