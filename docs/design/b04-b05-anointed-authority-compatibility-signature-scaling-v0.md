# B04/B05 — Anointed Authority Compatibility and Signature Scaling v0

> **DESIGN ONLY — NOT CANONICAL, NOT NATIVE.** This bounded successor to [Authority & Destiny Cross-Aspect Balance v0](b04-b05-anointed-authority-destiny-cross-aspect-balance-v0.md) and [Returning Step v0](b04-b05-anointed-restoration-birth-mission-signature-baseline-v0.md) supplies **candidate** grade non-stacking, exact level-3 ordinary-technique Authority pairings, and six-level Conflagration scaling comparisons. It does **not** change [Anointed Foundation](../rules/08-archetypes/anointed.md), authorize a player-facing Signature or Authority-enhanced spell, add an Anointed character build, certify encounter outcomes, or change **9/12** structural, **0/12** independently certified, **0/6** MVP exits or the original B06 G0–G8 milestones.

## Decision 1 — Authority grades and High Sovereign Projection

The merged [Authority/Destiny proposal](b04-b05-anointed-authority-destiny-cross-aspect-balance-v0.md) proposes one Aspect-defined Authority with **Lesser (L1, 1 Destiny), Greater (L5, 2 Destiny), Supreme (L10, 3 Destiny)**. Its actual effects remain Aspect-authored, not generic metamagic or automatic Used-Tier advancement. An Anointed always retains the **0-VP Signature** while the bond remains active; no Destiny is needed to remain effective.

**Non-stacking candidate:** one application may carry **exactly one intensity of the same Authority**. Do not combine Lesser + Greater, repeat Lesser, carry both Greater + Supreme, double one intensity, or split one expenditure into additional attacks/recipients. Otherwise a level-5 Lesser + Greater combination could reproduce +9 Conflagration Vigor before Supreme unlocks at level 10. This prohibition applies to **High, Medium and Low**.

**High L5 Sovereign Projection — reconcile explicitly, do not silently overwrite canon:** The existing foundation still permits *two compatible Authority Expressions* in one compatible projected use, at full cost. Our design has **only one proposed graded Authority per pilot Aspect**. Different grades of that *same* Authority do not count as two distinct compatible expressions; therefore **Sovereign Projection currently supplies no second empowered application for these pilots**. Two genuinely **different**, separately authored compatible Authorities could eventually satisfy its existing text if the design later retains more than one; this PR neither grants them nor removes the feature. A possible future L5 replacement emphasizing expanded outward delivery requires separately authored recipient/range/area semantics and a decision PR. Do not invent extra targets, potency, free Destiny, or a new projection rule just to fill the L5 slot. **This preserves the canonical text while recording the incompatibility as an explicit review gate.**

**Payment candidate:** declare the one grade before attack/response; check source-legal AP, VP/reserve, bond/target and Destiny. Commit Destiny at the actual eligible application attempt, even on a miss or resistance, but not on a pre-application interruption. One paid attack or eligible Regeneration Step uses a unique receipt; replaying the same receipt cannot spend/apply another enhanced packet. All numerical illustrations below use **Lesser only at level 3**, not prematurely available Greater/Supreme.

## Decision 2 — Exact level-3 ordinary-technique compatibility candidates

The canonical [Anointed foundation](../rules/08-archetypes/anointed.md) grants High L3 **Manifest Authority** through compatible **[Projection]** techniques, Medium L3 **Deep Channeling** through compatible **Invested Vessels**, and Low L3 **Incarnate Authority** through embodied/self/equipment applications. That framework alone does **not** grant Authority to a technique. Both the technique's **exact profile** and **the chosen Authority output** must explicitly permit it. Anointed still needs ordinary legal bonded-Aspect access, sufficient VP, actions, range, sight/path, recipient consent/Intrusion, equipment state, and other normal permissions.

### Conflagration — one selected paid Conjure Flame attack

**Candidate compatibility (not yet a technique rule):**

| Focus at L3 | Exact ordinary source profile | Additional required delivery | Proposed *Lesser* Authority only |
|---|---|---|---|
| **High** | [Conjure Flame](../rules/07-veil-magic/conjure-flame-v0.md) **Thrown Projectile / Primary** | One real **[Projection]** projectile with ordinary range/Throwing/cover/Guard/Dodge | +3 Vigor on the single qualifying projectile hit |
| **Medium** | **Weapon Enchantment / Primary** | One currently wielded weapon that is also the single valid Invested Vessel; established **4 × T Committed VP** reservation | +3 Vigor on **one declared paid weapon attack**, not every Reserved Weapon hit |
| **Low** | **Weapon Enchantment / Primary** | One actively wielded weapon and valid active **4 × T Committed VP** reservation, embodied through one legal paid physical attack | +3 Vigor on **one declared paid weapon attack**, not every hit or every action |

**Source-bound payments:** High Thrown Projectile uses **one 20-AP Projection Action + 2 × T Spent VP**, and its Vigor packet is `2 + ceil(d8 × T / 3) + max(VC,0)`; Medium/Low must have already established a legal Reserved Weapon via the ordinary **24/30-AP Projection Action and 4 × T Committed VP**, and continue to wield it. Each Reserved hit uses its ordinary paid Physical Action, with base Vigor packet `1 + ceil(d6 × T / 4) + max(VC,0)`; the existing reservation does **not** add per-hit VP cost. The candidate **1 Destiny** adds exactly **+3 Vigor to one existing hit packet**; do **not** create an extra Kindled Flame, second Fire HP packet or independent damage roll. Conjure Flame *Ammunition Shot*, Secondary, Rider and other modes remain **unapproved** for Anointed Authority. This model does not change High Gifted's separately authored [Projection] metadata or grant Anointed access from that Gifted-only entry.

**Numerical L3 High example (T2, VC0):** expected Vigor per hit is **5.375** normally, **8.375** with 1 Destiny; Fire HP remains **2**; VP cost remains **4**. A miss or successful defensive response still pays the legal attempted action/VP and Destiny under their respective timings, with **zero** added hit-triggered damage. An interrupted non-application should not consume unspent Destiny. A weapon drop, broken reserve, mismatched Vessel or recycled event receipt cannot deliver another enhancement.

### Restoration — one Guided Regeneration Step, not Basic Heal

**Candidate compatibility (not yet a technique rule):**

| Focus at L3 | Exact source profile | Required interaction | Proposed *Lesser* Authority only |
|---|---|---|---|
| **High** | [Guided Regeneration](../rules/07-veil-magic/guided-regeneration-v0.md) **Single Target** | Legal projected living recipient, actual active fixed or maintained effect | One **incremental +1 HP** of the technique's next eligible Regeneration Step costs **0 recipient Vigor** |
| **Medium** | **Single Target** | One living Invested Vessel is the actual eligible target, obeying normal delivery/range/path | Same one incremental +1 HP, no remote or extra target |
| **Low** | **Self / [Embodiment] / Regeneration channel** | Actual self-only maintained or fixed Guided, ordinary cast completed | Same one incremental +1 HP during own valid Step |

[Guided Regeneration v0](../rules/07-veil-magic/guided-regeneration-v0.md) already offers exactly **+1 throughput**, not another Step. Its legal modes remain **2 Spent VP** fixed or **2 Committed VP** maintained; normal casting remains Focus-priced **20/24/30-AP Projection Action**. It cannot be silently cast as a free weapon rider, does not receive extra duration, and is still Tier 1 even at level 3. **Basic Heal** has no eligible waiver of recipient Vigor consumption: it restores Vigor rather than consuming recipient Vigor, and **has no proposed Authority compatibility**.

**Precise one-Step waiver candidate, not native:** Apply to one **already-existing** beneficiary Regeneration Step of a valid active Guided instance. This model considers a **living, non-Dying recipient with positive HP and no competing wound allocation**; calculate ordinary natural HP recovery from current throughput and recipient Vigor first, then if HP is still missing, allow **up to one additional +1 HP provided by Guided** without deducting Vigor for that **one** extra HP. Charge **1 Destiny** once at that legal step; subsequent eligible steps revert to normal 1 Vigor per HP unless separately enhanced. This is a specific exception to Guided's current Vigor requirement, **not an executable permission** until promoted. If recipient has 0 Vigor, the one Destiny-funded extra HP can still apply under this candidate, but there is no free natural regeneration, no other extra HP, no free wound repair, no Dying stabilization or cancellation, and no off-initiative fabricated Regeneration Step. No Destiny spend if full HP or no incremental HP can be applied. Exact sequencing with wound repair, paid interruption, refusal, and simultaneous effects needs native authoring before use.

**Example:** Recipient at 7/12 HP with throughput **2** and Vigor **3**; ordinary Regeneration Step restores 2 HP costing 2 Vigor; candidate Guided + Lesser Authority restores **1 extra HP without Vigor**, ending **10 HP and 1 Vigor**, spending 1 Destiny. Without Authority, the extra +1 Guided restoration would consume the third Vigor, ending 10 HP and 0 Vigor. One Destiny therefore saves **1 Vigor** when the incremental HP would otherwise be funded. This small benefit is **a balance concern** and may not justify implementing L3 Restoration Authority unchanged; retain the comparison as a negative decision witness, not an implicit approval.

## Decision 3 — Conflagration Signature scaling through L20

The [merged experimental Kindled Flame](b04-b05-anointed-authority-destiny-cross-aspect-balance-v0.md) has **1 Fire HP + 1 Vigor** on a qualifying hit for 0 VP; proposed graded Authority adds **+3/+6/+9 Vigor** at **1/2/3 Destiny**, unlocked at L1/L5/L10. Its actual attack/target/carrier rules are **not yet authored**, so this is per-eligible-application arithmetic, not a player-facing spell.

**Scaling candidate for the baseline Signature's own Vigor packet:**

`Signature Vigor = 1 + floor(Level / 5)`

**Authority bonus remains +3/+6/+9**, rather than scaling again with level. Fire HP remains **1**. This formula is **Conflagration-specific**, not the Standard Veil Control packet nor a universal Anointed/Aspect damage table. It adds **no implicit VC**; otherwise one high-level free Signature could dominate paid techniques and multiply with High's Projection Tempo. Compare exact existing paid [Conjure Flame](../rules/07-veil-magic/conjure-flame-v0.md), **T = min(9, floor((Level+1)/2))**, VC0, at the highest legal used tier:

| Level | Max tier / paid VP | Paid Thrown mean Vigor on hit | Signature fixed 0-Destiny | Signature scaled 0-Destiny | Strongest available grade | Scaled empowered Vigor on hit |
|---:|---|---:|---:|---:|---|---:|
| **1** | T1 / 2 VP | **3.875** | 1 | **1** | Lesser (1 Destiny) | **4** |
| **3** | T2 / 4 VP | **5.375** | 1 | **1** | Lesser (1 Destiny) | **4** |
| **5** | T3 / 6 VP | **6.500** | 1 | **2** | Greater (2 Destiny) | **8** |
| **10** | T5 / 10 VP | **9.875** | 1 | **3** | Supreme (3 Destiny) | **12** |
| **15** | T8 / 16 VP | **14.375** | 1 | **4** | Supreme (3 Destiny) | **13** |
| **20** | T9 / 18 VP | **15.500** | 1 | **5** | Supreme (3 Destiny) | **14** |

The L15 paid average **14.375** is from enumeration of all eight d8 faces at T8, not a rounded projection. Paid Conjure Flame still delivers **2 Fire HP**, its own VC coefficient, and real alternative profiles at full VP cost. The Signature remains 0 VP, Focus-specific, and Destiny-empowerable, with no paid technique profile inherited. These values offer a consistent baseline into L20 but **do not establish potency parity, CR, or long-term tuning**.

### Three Focus output and action economy (opportunity envelope only)

The [action economy](../rules/05-combat/action-categories-and-physical-tempo.md) gives Turn AP 30 at L1 up to 120 at L16+, High Projection 20 AP, Medium Physical/General 24 AP, Low Physical 20 AP. [PR #161's isolated envelope](b04-b05-anointed-authority-destiny-cross-aspect-balance-v0.md) constrains the proposed Medium/Low Signature packet to **one successful eligible paid Physical Action per own turn** following Medium's 24-AP Vessel setup. High may spend a separate 20-AP Projection Action on each eligible Signature attempt. This is **not** a native Anointed legal build or full encounter policy.

| Level | High possible independent projections / own turn | Medium projected packet opportunities R1/R2/R3 | Low packet opportunities / own turn | High baseline full-hit Vigor budget at max Turn AP* |
|---:|---:|---|---:|---:|
| 1 | 1 | 0 / 1 / 1 | 1 | 1 |
| 3 | 2 | 0 / 1 / 1 | 1 | 2 |
| 5 | 2 | 1 / 1 / 1 | 1 | 4 |
| 10 | 4 | 1 / 1 / 1 | 1 | 12 |
| 15 | 5 | 1 / 1 / 1 | 1 | 20 |
| 20 | 6 | 1 / 1 / 1 | 1 | 30 |

*Assumes **every** potential High Signature attempt legally hits, no other AP spending, no cover/Dodge/Guard/interception, all targets have sufficient Vigor and no resistances. The medium/low carrier's **ordinary weapon damage is omitted** and their packet does not multiply across high physical tempo. This is a theoretical **uncapped ceiling**, not realistic encounter output. For finite targets apply `min(actual current Vigor, Vigor packet)` separately to each hit. At L20, High's six 0-VP projected attempts could burn **30 Vigor in one full-hit turn**; this is a prominent **scaling risk** and requires actual multi-hit response/movement/cover/opportunity and source-legal character tests, particularly relative to a 0-VP signature's long-term value. Scaling may ultimately need cadence or formula adjustment, not blind adoption.

Under a purely illustrative **65% independent hit chance**, the L20 High unopposed expectation for six baseline projections is **19.5 Vigor** before defender resource caps; medium/low produce **3.25 expected Vigor** from their single candidate packet, **plus their separate, unmodeled weapon attacks**. These rates are not sourced encounter hit chances.

### Cross-Aspect sanity check

Restoration's [Returning Step baseline](b04-b05-anointed-restoration-birth-mission-signature-baseline-v0.md) does not scale raw HP automatically because HP remains level-independent. High baseline **2 HP**, Medium/Low **1 HP** from existing recipient Vigor remain candidates; the level-3 Guided waiver is **a separate ordinary-technique compatibility proposal**, not a replacement for the existing **Spare the Reserve** Signature Authority. Do not add 2 HP to Basic Heal, make Guided Regeneration free, create out-of-combat Regen Steps, or allow restoration from negative HP outside the authored Dying procedure. Later Greater/Supreme Restoration intensity outputs and the High L5 feature still require an explicit choice, not extrapolation of Conflagration numbers.

## Approval boundary and next steps

1. **Design approval required:** single-grade no-stacking rule versus canonical High L5 two-expression text; whether Sovereign Projection needs a future rewrite; separately whether Conflagration's baseline should scale 1 per five levels.
2. **Source profile authority required:** add explicit **Anointed** tags/compatibility to chosen exact Conjure Flame and Guided Regeneration profiles; keep every other technique/profile ineligible, including Conjure Flame ammunition/Secondary/Rider and **Basic Heal**. Verify real L3 normal VP/AP/casting/attachment/target and Destiny receipts.
3. **Native proof required:** commit-time costs on misses/interruption, replay/duplicate prevention, one attached hit per paid Destiny (Medium/Low), prior Vessel setup and maintained weapon reservation, legal Guided Step and zero-Vigor exception, HP/Dying/wound/Intrusion safeguards, and source G0/G1/G3/G4/G5 outcomes.
4. **Scaling proof required:** actual enemy hit probabilities/mitigation and Vigor caps over multiple rounds/encounters, comparative AP allocation and opportunity/Guard responses, genuine High Projection/Low physical roles, and attrition/rest cadence at L1/L3 and beyond.
5. **MVP accounting unchanged:** no new Anointed structural pairings or independent focus certifications, no new Tier-1 technique or Aspect census increment, no B06 phase expansion, no Blocker closure. The model is **not native** and is not a representative playtest.

### Reproduction

From repo root:

- `python -m unittest discover -s tests -p 'test_b04_b05_anointed_authority_compatibility_scaling_v0.py' -v`
- `python -m scripts.b04_b05_anointed_authority_compatibility_scaling_v0`

The new module imports the merged [PR #161 comparison model](../../scripts/b04_b05_anointed_authority_destiny_v0.py) for source-grounded Destiny/paid Conjure Flame and three-Focus AP opportunity envelopes. Every output is **DESIGN ONLY**, not a canonical mechanic or actual encounter.
