# Basic Heal v0 — Life / Restoration

> **Executable Life / Restoration technique with PROVISIONAL numerical playtest values.** This is an instant, low-cost **Vigor replenishment** spell with minor HP restoration and a small emergency contribution to wound repair while Dying. It does **not** increase natural regeneration throughput, create a new Regeneration Step, treat a wound directly outside the specified Dying conversion, stabilize automatically, or resurrect the dead. Use [Technique Structure v0](technique-structure-v0.md), [HP and Vigor](../06-vigor-wounds-death/hp-and-vigor.md), [Dying and Wounds](../06-vigor-wounds-death/dying-and-wounds.md), and [Intrusion](resonance-and-intrusion.md#intrusion). A published technique is **not automatically known**: each character still needs their Archetype's actual Life/Restoration acquisition/access permission.

## Identity and executable profile

| Field | Rule |
|---|---|
| Name / source | **Basic Heal — Life / Restoration**; canonical Aspect is **Restoration (Transform)**, but Aspect metaphysical class does not replace the magic interaction type |
| Base Tier / access | **Tier 1**, requires legitimate knowledge/access through individual Archetype rules |
| Used Tier | Choose **T ≥ 1** at declaration, no greater than universal tier ceiling (levels 1–2: T1; level 3: up to T2) |
| Profile identifiers | **`Single Target`** and **`Self`** are distinct exact profile keys, each with the same authored Primary/Secondary/Rider values and AP/VP. `Single Target` allows one eligible recipient (including the caster); `Self` can affect **the caster only** at 0 squares. |
| Components | **Hands:** at least one functioning available hand; no weapon/implement requirement |
| Range / target | **0–3 squares** (Self = 0), one living creature at another square within **3 squares / 4.5 m**, visible to the caster with **an unobstructed magical delivery path through the air**; physical walls and wholly obstructed paths block casting |
| Expression / interaction | **[Projection]** single-target direct restorative **Intrusion** into living biological function; it is **not Manifestation** or physical projectile delivery |
| Primary activation | **One Projection Action**, paid High **20 AP**, Medium **24 AP**, Low **30 AP** |
| Primary VP | **2 × T Spent VP** for the attempted spell |
| Duration / cadence | **Instant**, one effect per completed cast; no ongoing Pulse, Rider cadence, upkeep, held Reserve or free triggered repeats |
| Target defense | **Beneficial/unopposed** (including unconscious **without an active prior refusal**): no Intrusion contest. **Consciously resisted or subject to a still-effective prior refusal:** canonical **+8 Intrusion Barrier**, including during unconsciousness. |
| VC effect coefficient | **VC = max(0, Veil Control)** of this spell's caster at effect resolution, once per cast, **not** standard VC × Level |
| HP and Vigor limits | Apply only actual missing HP/Vigor: neither may exceed the target's current normal **Max HP/Max Vigor** |

This technique's [Projection] tag allows specifically authorized Projection interactions; its **Intrusion** classification comes from **directly restoring internal bodily state**, not from the name, range, or Aspect category. Unconsciousness is **not** a targeting prohibition for a genuinely beneficial Basic Heal. A caster cannot use this technique to heal a **dead** creature, and it does not alter a creature's maximum resource capacity.

## Authored contributions — `Single Target` and `Self`

**Both exact keys** share the contribution table and costs below. The `Self` profile permits compatible self-only Primary/Secondary compositions and potential future **expressly authorized** Rider use; it does **not** independently grant a free Rider trigger or second spell. A composite must select **one shared exact key** supported by both techniques. A `Self` composite can target only its caster; `Single Target` cannot be substituted for a self-only component.

| Contribution | HP component | Vigor restoration | Eligibility |
|---|---:|---|---|
| **Primary** | **2 HP** | **`4 + ceil(d8 × T / 3) + VC`** | Ordinary independent casting; **2 × T Spent VP** and one Projection Action |
| **Secondary** | **1 HP** | **`2 + ceil(d6 × T / 6) + VC`** | Eligible as a compatible High Scholar Composite Casting **Secondary** with exact matching **`Single Target` or `Self`** profile, after full technique and effect compatibility checks; other selection requires separate authorization |
| **Rider contribution** | **0 HP** | **`2 + ceil(d4 × T / 6) + VC`** | **Data for later expressly authorized item/feature/technique**; does **not** grant a free per-action regenerative Rider, free item enchantment or repeating Vigor restoration |

`T` is the Basic Heal component's **own Used Tier**; `ceil` acts on the specified rolled die multiplied by T and divided by the indicated constant. Roll the die **only when an otherwise legal spell applies successfully**. **VC = max(0, the Basic Heal caster's raw Veil Control)** at this attempt's resolution; a negative raw VC produces 0 in the output, **but still contributes its actual negative modifier** to a contested Direct Veil Pressure roll. **No additional standard VC packet** is automatically granted.

Primary and Secondary are **different authored effect strengths**, not a VP discount. A High Scholar using Composite Casting pays the **full VP cost of this technique (2×T)** plus the other component's full VP cost, with one slower legal composite action; when this explicitly authored Secondary applies, **do not halve its listed restoration again**. The **Primary** technique owns the delivered target/resolution; exact `Single Target` or `Self` match is necessary but not by itself sufficient for combining incompatible effects or target definitions. Do not convert an unwanted harmful composite into “beneficial” merely by adding this healing component: assess the **actual complete effect** under universal Intrusion rules. This technique does not itself grant multicasting or item Rider permissions.

## Application order, resistance, and expenditure

1. **Declare** Basic Heal, legal recipient, one exact **`Single Target` or `Self`** profile, contribution authorization and Used Tier. With `Self`, the caster is the sole legal recipient. Confirm a functioning hand, range, visibility, path, permitted biological target, sufficient Turn AP and Available VP. For self-healing no separate line of sight to one's own body is required.
2. **Commit** the Focus-priced Projection Action AP on declaration using normal turn/responses. If the action is Interrupted or becomes illegal before a valid magical application can be attempted, the already committed AP remains lost; **no VP is spent for an application that never occurs**. This does not grant interruption protection or a free out-of-turn casting window.
3. **At valid effect resolution**, spend **2×T VP** for an independently cast Primary (or the full authored costs of every component for a legal composite), **even if a legitimate resistance contest subsequently defeats it**, then resolve that contest if needed:
   - **Actually beneficial and unopposed**, including an unaware, incapacitated or unconscious recipient **without an applicable still-effective prior refusal**: **no Intrusion contest**.
   - **Conscious deliberate resistance or an applicable still-effective prior express refusal**, even while unconscious: normal **Direct Veil Pressure vs Direct Veil Resistance +8**. Use **Intellect** as this technique's **Shaping Ability** and **Vitality + Awareness** as its authored **defensive Abilities**. These Ability assignments are a **v0 calibration baseline**, not a universal healing-ability rule.
   - **Any effect that has become harmful or deceptively mixed through a composition or feature:** apply [universal harmful/deceived Intrusion](resonance-and-intrusion.md#intrusion-barrier) and the same authored Ability assignments for Basic Heal where its contribution requires a contest. **No second saving throw** is added for the healing packet of a composite that already has one legally authored Primary contest.
   - **Direct Veil Pressure = `d20 + raw Veil Control + Intellect + Veil Integration Bonus + explicit modifiers`.** Target base resistance = **`10 + Vitality + Awareness + target Veil Integration Bonus + Resonance + explicit modifiers`**, then add the applicable barrier. **Tie resists.** A natural 20 does not auto-succeed.
4. On **successful, permitted** application, roll the authored Vigor restoration and allocate the HP component using the Dying rule below. Apply relevant caps. The Vigor component restores reserve **directly**; it does not purchase extra HP/regeneration/Repair Progress at the moment of casting.

A conscious creature may decline a supposedly helpful effect and resist it. A still-effective express refusal remains operative through unconsciousness for its stated scope and uses the **+8** barrier; a refusal limited to an earlier completed cast does not persist. A corpse is not a legal recipient. A **genuinely beneficial and unopposed** spell does not require prior signed/express consent when its recipient is unconscious. A specific ward, curse, applicable healing immunity or external-healing block still operates independently of whether an Intrusion contest was waived. A caster's claim that an objectively hostile modification is beneficial does not bypass the barrier.

## Normal recipient: minor HP and large Vigor replenishment

If the recipient is **not Dying** at the instant the valid effect applies:

- Restore the authored **HP component directly**, up to missing HP. This is a small instant restorative effect, **not** natural Regeneration Step throughput and **does not spend the recipient's Vigor**.
- Restore the authored **Vigor component directly**, up to missing Vigor, **without making an extra Vigor-to-HP conversion**.
- **Do not** add Wound Repair Progress, even if this non-Dying recipient has an unfinished repairable wound. Such recovery remains under the normal Regeneration Step or a later specially authored wound-treatment technique.
- If no resources are missing, the spent VP is **not refunded** and no resource is raised above maximum.

## Dying recipient: convert the HP component to Repair Progress

If the recipient **is Dying (HP ≤ 0)** when Basic Heal resolves, use this procedure before ordinary HP restoration. The [Dying recovery-blocking wound rule](../06-vigor-wounds-death/dying-and-wounds.md#regeneration-while-dying) applies: **all wounds with unfinished Repair Requirements** are recovery-blocking during the current Dying episode, whether acquired before it or while Dying. A still-present **Irreparable** injury also blocks Basic Heal from bypassing it with direct HP healing. A Fatal injury is death and cannot be healed by this technique.

1. **Select one wound at declaration.** The caster selects **one identified unfinished repairable wound** for this cast's Repair Progress. If no legal wound is identified or selected, use the **oldest unfinished repairable wound**, with recording order breaking ties. This fallback does not reveal hidden injury information or grant wound detection.
2. **Convert the HP component one-for-one** into direct Repair Progress on the **one selected wound**: **Primary +2**, **Secondary +1**, **Rider +0**. This does not consume the patient's Vigor or natural regeneration throughput and is not an extra Regeneration Step.
3. **Cap at wound completion.** Unused HP-component points **cannot spill into another wound**. If **any** wound remains unfinished or an unreconstructed blocking injury remains, **all leftover points are lost**: none restore HP. Only if the selected wound just completed **and no other blocking wound remains** may the unused HP-component points restore actual HP (up to Max HP). Completing a wound alone never raises HP or automatically restores consciousness.
4. **No repairable wound:** If there are **no incomplete recovery-blocking wounds**, restore the HP component normally even if HP is still 0 or negative. If a blocking Irreparable injury remains, Basic Heal cannot repair it or use its HP component to bypass it.
5. **Vigor restoration is independent.** Restore the rolled Vigor packet up to Max Vigor unless a distinct protection blocks external Vigor restoration. It does not immediately cancel Dying HP loss, provide throughput, repair another wound or trigger extra regeneration. The next normal Regeneration Step follows the existing survival-first order.

**Worked multi-wound example:** At **HP 0**, wound A has **9/10** progress and B has **3/20**. Primary Basic Heal selects A; **+1 progress** finishes A. Since B remains unfinished, the unused **1 HP-equivalent point is lost** and HP stays **0**. If A were the **only** wound, the remaining point would restore **+1 HP**, allowing recovery to positive HP. If the caster does not specify a wound, the oldest unfinished repairable wound receives the cast's progress.

**No double-counting:** Basic Heal's +2/+1 direct progress replaces its own HP component while repair is required, not HP and Repair Progress together. Irreparable wounds receive no ordinary progress; a dead creature is not a valid recipient.

### Suppression and persistent damage

- **Ordinary natural regeneration suppression** changes the Regeneration Step/throughput according to its own rules; it does **not** automatically block instant Basic Heal HP restoration, the technique's **direct external Repair Progress**, or Vigor replenishment.
- An effect explicitly preventing **external Vigor restoration** stops the **Vigor packet**; one explicitly preventing **direct HP healing**, **external wound repair** or **all healing** stops the relevant Basic Heal component(s). Apply each narrowly authored prohibition as written; **do not** infer that blocking one resource blocks all others.
- Basic Heal does **not** remove bleeding, poison, regeneration suppression, blocked healing, repair-rate penalties or an ongoing wound condition; repairing a wound through completed Repair Progress follows the ordinary wound procedure and its authored consequences.

## Level 1–3 numerical/playtest checks

All quantities below are **per successful cast** and **before target missing-resource caps**; `VC` below is the caster's **nonnegative output VC**. No passive or repeated Rider effect is included.

| Used Tier | Contribution | VC +0 Vigor (min–max; mean) | VC +2 Vigor (min–max; mean) | HP / Dying Repair Progress |
|---:|---|---|---|---|
| 1 | Primary | **5–7; 5.875** | **7–9; 7.875** | **2 HP / +2 Repair** |
| 1 | Secondary | **3; 3.000** | **5; 5.000** | **1 HP / +1 Repair** |
| 1 | Rider | **3; 3.000** | **5; 5.000** | **0 / +0 Repair** |
| 2 | Primary | **5–10; 7.375** | **7–12; 9.375** | **2 HP / +2 Repair** |
| 2 | Secondary | **3–4; 3.500** | **5–6; 5.500** | **1 HP / +1 Repair** |
| 2 | Rider | **3–4; 3.250** | **5–6; 5.250** | **0 / +0 Repair** |

With recipient **Vitality +1**, max HP = 11 and max Vigor = **11/22/33 at levels 1/2/3**. A Tier-1 Primary with VC +2 restores **7.875 average Vigor** to a sufficiently depleted target, corresponding to **71.6% / 35.8% / 23.9%** of those maximum pools. At level 3, Tier-2 Primary costs **4 VP** (double Tier-1's 2 VP) but averages only **9.375 Vigor** versus Tier-1 **7.875**; **higher-tier efficiency is a watch**, not permission to alter the given formulas silently.

At **Veil Affinity +0**, full VP pool and no other spending, the maximum number of **Tier-1 casts per full VP pool** at levels 1/2/3 is High **3/6/9**, Medium **2/4/6**, Low **1/2/3**. Available projection casts per turn for these levels are High **1/1/2**, Medium **1/1/1**, Low **1/1/1**. At level 3, Higher Tier 2 costs **4 VP** and max VP-pool casts are High **4**, Medium **3**, Low **1**. These are separate VP/AP ceilings, not promised successful resistant-target hits.

## Regression / safety of resolution boundaries

| Situation | Expected v0 result |
|---|---|
| Conscious willing ally accepts healing | No Direct Veil contest, spend **2×T VP**, apply capped HP + Vigor |
| Unconscious genuinely beneficial target at −3 HP, 0 Vigor, Serious wound 0/10; T1, VC +2 | No Intrusion contest; **2/10 Repair**, **7–9 Vigor**, **HP remains −3**; no extra regen tick |
| Same target deliberately resists while conscious | Roll **d20 + raw VC + Intellect + Veil Integration** against **10 + Vitality + Awareness + target Integration + Resonance +8**; tie resists; pay VP even on failure |
| Equal non-barrier stats, harmful/unwilling or beneficial/resisted | +8 Intrusion Barrier, **10%** success in standard unmodified comparison; no automatic natural-20 success |
| Actual hostile effect deceptively accepted as benign | +4 barrier, base resistance still applies; mislabeling or concealment by itself never grants free healing-style bypass |
| Target with a ward specifically blocking external restoration | Ward applies independently even when beneficial Intrusion has no contest |
| Dying target HP 0, wound at 9/10, Primary | +1 Repair finishes wound and remaining +1 restores **HP 1**; recovery only if no other block |
| Dying target HP −3, wound 9/10, Primary | +1 Repair and +1 HP yields **HP −2**, still Dying; Vigor restores separately |
| Dying target with 0 Vigor receives VC +2 T1 Primary | Restore 7–9 Vigor, but **no instant regeneration**; natural Dying survival/repair next normal Step |
| Dying target with Irreparable active wound | No ordinary Repair Progress and no wound-bypassing HP recovery; separately eligible Vigor still restores |
| Non-Dying wounded target | Up to **2 HP + rolled Vigor**; **0** direct wound progress |
| An ally at full Max HP and Max Vigor | Spell cannot exceed caps; valid cast still spends VP |
| One legal High Scholar **`Single Target`** composite | One Primary and authored Secondary **once**, both full VP costs and one slower action; neither extra target nor doubled healing proc |
| Mismatched profile or unapproved Rider application | No composite/standalone Rider use merely because a table cell exists |

## Deferred / calibration watch

- **Tier scaling**: at level 3, one Tier-2 cast has weak Vigor/VP efficiency against two Tier-1 casts, while High Focus can cast two Tier-1 spells in a turn. Retain as a v0 tuning watch, not a framework change.
- **Casting Abilities** Intellect / Vitality + Awareness are **v0 technique-specific values** subject to playtesting. No global “healing attack Ability” or +Training was created.
- **Vigor/VP sustain**: repeated heal casts, max-Vigor caps, six-hour VP/Vigor recovery and rising multi-action Tempo may influence attrition; re-evaluate before higher tiers.
- **Later restorative techniques** may specialize in larger instant HP restoration, direct +20-style wound repair, increased natural Vigor-to-HP throughput, larger Vigor burst/action efficiency, reconstruction or a specially authored emergency Reaction. **Basic Heal grants none of these automatically.**
- No self-cast-by-unconscious creature, automatic prepared prayer, Gifted Conduit, Priest Devotional Rite, Consecration, Anointed Signature or generic magic item Rider is granted by this document. It does **not** close the overall **B05** repertoire/content blocker.
