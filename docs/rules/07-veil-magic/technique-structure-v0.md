# Technique Structure v0 — Casting, Contributions, Profiles, and Reservations

> **LOCKED STRUCTURAL BASELINE (merged PR #62).** This document defines the common **authoring and execution structure** for Pillar/Aspect techniques, without granting a repertoire or executable techniques by itself. It implements the B05 design decisions tested against the **provisional Conjure Flame** example. **Individual effect numbers, unrestricted composition outside existing archetype features, full crafting and item economy remain unapproved.** Existing **High Scholar Composite Casting** is already authorized by [Scholar Foundation](../08-archetypes/scholar.md#levels-12--technical-repertoire-and-prepared-composite-formulae) and is **not deferred or superseded** here. Existing [Tier/Expression rules](technique-tiers-and-expression.md), [VP states](volition-points.md), [Turn AP](../05-combat/action-categories-and-physical-tempo.md), [Direct Veil](resonance-and-intrusion.md) and [Manifestation](manifestation-resolution.md) continue to govern their respective subsystems.

## 1. Orthogonal parts of a technique

A **technique** is a named expression of an authorized Pillar/Aspect, with a base tier and one or more **profiles**. A profile specifies a legal form, target and delivery. A **contribution** selects how much of the technique's authored effect that execution supplies. **Resource handling** states what happens to VP. **Resolution** specifies how the effect reaches a target and what happens if it does. None of these dimensions automatically determines another.

| Dimension | Question answered | Examples |
|---|---|---|
| Technique identity | What is being expressed? | Conjure Flame; Fire / **Conflagration** (canonical Aspect) |
| Profile | How and to what is it applied? | Thrown flame, one held weapon, an arrow/bolt, one creature, self, area |
| Contribution | How complete/strong is this expression? | **Primary**, **Secondary**, **Rider contribution** |
| VP handling | Where does the required VP go? | **Spent** for immediate casting; **Committed** for a Reserve |
| Activation | What action starts it? | One Focus-priced **Projection Action** by default for a single spell |
| Delivery/resolution | What determines success and consequences? | Physical projectile/weapon, **Manifestation**, **Imposition**, **Intrusion**, healing |
| Persistence/cadence | When may effects apply again? | Continuous, **Rider cadence**, Pulse, Spend; valid weapon hits |
| Damage/effect packets | What changes? | Fire-type **HP** damage, independent **Vigor** damage, healing, movement |

**Terminology collision:** **Rider contribution** (a limited selection from a technique's effect) is **not** the same concept as **Rider cadence** (a persistent effect triggered by eligible actions/events). The former describes *what* is contributed; the latter describes *when/how often* an output may trigger. Authors must identify both when relevant.

**No universal 3 × 3 matrix:** some techniques have a single profile and only Primary. Others may expose Secondary or Rider values without making them independently usable. The existence of a table cell is **not** permission to cast, combine, reserve or attach it. For High Scholar Composite Casting, both selected techniques must have an **exact matching authored profile identifier** and be compatible with the operation; profile names describing vaguely similar deliveries are not interchangeable.

## 2. Contribution definitions and eligibility

| Contribution | Meaning | Legal activation condition |
|---|---|---|
| **Primary** | The technique's full main effect in the chosen profile. | Normal accessible technique use, subject to the profile and caster's eligibility. |
| **Secondary** | The authored lesser/reduced expression. It may reflect channeling inefficiency, the price of composition, a conversion device or an environmental effect that demotes otherwise normal casting. | **High Scholar Composite Casting already authorizes a compatible known Secondary**; other composition, conversion, environment, item or technique-specific rules may also select Secondary. The table alone creates no extra action/cast. |
| **Rider contribution** | A restricted subset of the technique's properties, **not** its normal main physical/damage contribution. | An explicitly authorized item, feature, combined effect or other host grants the property. Merely knowing the technique does **not** grant free Riders. |

Secondary may be applied to a **standalone** cast forced into lesser efficiency; it does **not** necessarily require another spell. It may instead **supplement** a host expression, or serve as the **replacement** result of an item conversion. The permission determines which operation occurs and how costs are paid. **High Scholar Composite Casting is the existing, specific two-technique authorization**, subject to its level, known-technique, pairing/preparation and compatibility rules; this generic structure grants no additional combinations, attacks or stacking permission.

A Rider contribution can be supplied by an **independent magical item** (e.g. a socketed gem) without the wielder spending or committing VP. Its operating restrictions and power source belong to the **item**, not an assumed Reserve maintained by the wielder. An item's Rider can persist when an unrelated wielder-maintained Primary enchantment ends; whether multiple item properties stack remains item-specific.

Do not infer contribution strength, delivery method or Focus eligibility from the Aspect's metaphysical **External / Internal / Transform** category. See the [canonical Aspect identities](../../world/aspect-identities-and-boundaries.md).

## 3. Technique-specific profiles

A profile declares its actual **delivery or recipient**, supported contribution values, and separate restrictions. Examples:

- **Conjure Flame / Thrown flame:** a small ball of flame manifested outside the target, thrown using the native manifested-projectile attack procedure.
- **Conjure Flame / Reserved Weapon:** a temporary magical enhancement maintained on **one selected wielded weapon**.
- **Conjure Flame / Projectile:** fire effect attached to a physical arrow or bolt, with the ordinary projectile attack delivering it.
- **Life / Restoration:** [Basic Heal v0](basic-heal-v0.md) authors an exact **`Single Target`** profile (including Self), with distinct Primary/Secondary/Rider contributions and **direct HP/Vigor restoration**; it does not require invented weapon or area profiles.
- **Earth / Fortification (stone skin):** could author a *self-only* profile, if that particular technique is deliberately limited to self.

These are **examples of profile design**, not a mandatory profile list. **Conjure Flame v0** now explicitly authors `Thrown Projectile`, `Weapon Enchantment`, and `Ammunition Shot` identifiers in [its executable entry](conjure-flame-v0.md); other techniques may use different exact identifiers. A given Aspect may support different profile families. Specify which combination(s) of profile, contribution and resource handling are legal; do not assume the cross-product is available.

**Carrier ownership:** when a technique enhances an existing weapon/arrow, the ordinary physical attack uses its existing Attack/Defense rules; magic modifies consequences **on or after a qualifying successful hit** unless an explicit rule says otherwise. A created, independently flying manifested projectile uses the applicable [Manifested Projectile](manifestation-resolution.md#manifested-projectiles) procedure instead. For other phenomena, choose Direct Veil or Manifestation according to the actual effect, **not** the profile's label.

## 4. Activation and Turn AP — ordinary single spell

**Default rule:** activating a **single ordinary spell/technique** costs **one Projection Action** at the character's current Focus rate, whether the single activation resolves immediately or establishes an eligible Reserved effect. This replaces legacy “Spell Action Unit” language when importing technique content.

| Focus | Default single-spell activation |
|---|---:|
| **High** | **20 Turn AP** |
| **Medium** | **24 Turn AP** |
| **Low** | **30 Turn AP** |

The default is a **cost category**, not a bonus action or permission to act outside a turn. Specific authored techniques/features may explicitly require a **Full Action, Reaction, different action category or other legal timing**; those specific requirements override this default. For example, [Veil Inspection v0](veil-inspection-v0.md) already requires a Full Action, and [Blink v0](blink-v0.md) has its own Reactive timing and AP-debt rules. No new free Reactions or Interceptions are created.

A Thrown Flame attack roll is the **delivery of the spell paid for by that activation**, not an additional separately paid Physical Action. If a spell establishes a Reserved Weapon effect, later sword attacks are ordinary **Physical Actions**, each paid for normally, and **do not pay the spell activation AP again**. An item granting an automatic property is **not** assumed to make the wielder cast a spell; the item must author its own activation/trigger.

**Integrated-shot exception:** an authored `Ammunition Shot` profile may cost **0 additional spell AP** only **within** an otherwise legal, paid ordinary bow/crossbow shot. It still pays the normal Physical Action or Full Action **for firing** and the authored VP cost for each shot. This does not authorize a free standalone cast, free extra attack, free Reaction or skipped reload. See [Prepared and Spontaneous Ammunition v0](../05-combat/prepared-and-spontaneous-ammunition-v0.md).

The existing [Attack Sequence declaration](../05-combat/initiative-and-round-structure.md#attack-sequence), defensive choices and out-of-turn rules still apply. No profile creates a new spell-only defense or bypasses existing Turn AP.

## 5. VP handling: Cast versus Reserve

VP has **Available, Spent and Committed** states, per [Volition Points](volition-points.md). A technique/profile explicitly states its **VP price and handling**; it may offer immediate casting, reservation or an authored special case.

- **Cast / Spent VP:** Pay the stated amount at legal activation/resolution timing; these VP become **Spent** until recovered under existing VP rules. An immediate expression need not create a persistent reserve.
- **Reserve / Committed VP:** Commit the specified VP to an ongoing effect/anchor. It remains unavailable for other spending or commitment while active. **Release returns all still-Committed VP to Available VP**, not to Spent VP, at the channel's end. Releasing costs no action by default but **does not grant out-of-turn release timing** without a permission. Any distinct **Spent** activation surcharge remains Spent.
- **Independent magic item:** Do **not** assume the wielder pays or reserves VP for an item-defined property. Its charges, source, activation and persistence are expressly defined by that item when later authored.

**No universal Reserve multiplier is established here.** In the *provisional Conjure Flame example only*, immediate Cast costs **`2 × Used Tier` Spent VP**; Reserved Weapon costs **`4 × Used Tier` Committed VP**. Both formulas remain balance candidates. **Reserve** is the intended term, **not Reverse**; no reversal spell mechanic follows from these numbers.

Reserving does **not** downgrade Primary into Secondary; a full **Primary reserved weapon enchantment** is legitimate. Secondary contributions and Rider contributions do **not** implicitly require the recipient to maintain another Reserve. Similarly, a spell forced to Secondary by environmental interference can still follow the ordinary casting-resource method unless the interference specifically changes it.

## 6. Reserved Weapon baseline and channel break

A **Reserved Weapon** profile, when authorized by a technique, attaches **one wielder-maintained Primary enchantment** to **one selected weapon** and maintains a channel between caster and that weapon by **Committed VP**. The same cast does not enchant an off-hand weapon, ammunition, other weapons or future replacements without explicit permission.

1. **Establish:** Pay one Focus-priced spell activation (unless that technique overrides timing) and commit its stated VP. No per-hit activation AP is added.
2. **Persist:** While the VP commitment and channel remain valid, the Primary enchantment is active. There is **no universal duration countdown, upkeep VP payment, hit/charge limit, or once-per-turn application cap** on an eligible weapon-hit effect. Each **successful eligible weapon hit** may apply the authored effect. Ordinary physical attack AP, Attack Sequence and defense still govern every attack.
3. **Limit stacking:** The v0 default permits **only one wielder-maintained Primary Reserve enchantment per weapon at a time**. Maintaining a *second different Secondary Reserve enchantment on the same weapon* is an **advanced specialization/composition permission, not available by default**. An independent magical gem/property is **not a second wielder Reserve**; item stacking remains item-defined.
4. **Disarm or voluntary loss of weapon:** If the wielder is **successfully Disarmed of the reserved weapon** under [Disarm v0](../05-combat/disarm-v0.md), **or voluntarily drops/hands away that weapon at an ordinary legal own-turn zero-action decision point**, the channel **breaks immediately at that event**. Voluntary dropping is free, but zero-action timing **does not grant out-of-turn interrupt permission**. The reserved enchantment ends and **all its Committed VP immediately return to Available VP**, exactly as if it were voluntarily released. **Previously Spent VP or committed Turn AP do not refund.** Any unexecuted attack still uses the native interruption/legal-profile checks and does not regain spent AP. Recovering the dropped weapon does **not** restore the enchantment; a new legal activation is needed.
5. **Independent item property:** Disarm does **not inherently erase** a gem's independent magic. That property follows the item and its own rules; it is not maintained by the former wielder's VP. An independent item rider does not depend on another Primary Reserve continuing.
6. **Other channel failure:** Each profile must author any additional break conditions needed beyond normal VP release and this universal **Disarm** rule (e.g., destruction of its selected anchor, magical suppression or special transfer). **Do not invent global range/concentration/duration checks** to fill those gaps.

**Cadence versus hit limit:** an expressly authored **successful-hit Rider-cadence output** on a Reserved Weapon may trigger on **every eligible successful hit**; it is not limited by the number of hits in the Reserve. However, the [persistent-cadence safeguards](technique-tiers-and-expression.md#persistent-expression-cadence) still require damage values calibrated against the maximum applicable Tempo and prohibit an unrestricted **full-strength technique-scale** attack/heal on every ordinary action masquerading as a small Rider. No numerical safety is inferred from unlimited hits.

## 7. Damage resource, damage type, and separate properties

Every damaging expression explicitly states **which resource** each packet affects (usually **HP** or **Vigor**), its **damage type/property** if relevant, its **formula and scaling**, and its **trigger/defense**.

- **Fire** is a *physical damage type* for ordinary HP damage, like slashing, piercing, crushing, acid or electrical damage. It is **not** an extra resource bar and does not automatically imply another VP/HP/Vigor mechanic.
- **Vigor burn** is a **separate effect damaging Vigor**, not Fire-type HP damage simply because its source is Conjure Flame. **Fire-type resistance/immunity does not automatically negate or reduce Vigor burn.** Vigor-specific protection or an expressly dual-purpose defense can affect it.
- An otherwise **successful delivery** can apply a Vigor packet even when Fire-type HP damage is reduced to zero by fire resistance or a separately applicable mitigation, **unless the technique explicitly makes the Vigor packet conditional on actual HP loss**. A blocked/missed delivery does not apply either hit-triggered packet.
- When an independently manifested physical phenomenon directly damages a creature, the ordinary physical consequence affects **HP** by default. Weapon/arrow carriers retain their normal physical-hit damage and physical mitigation; magical Fire damage and Vigor damage are separately identified.
- **Do not automatically add Veil Control to a physical projectile's attack roll.** VC is an effect-scaling field, not a replacement for normal Agility/Precision/Training.

The explicitly authored [Elemental HP Damage and Resistance v0](elemental-damage-resistance-v0.md) now resolves **elemental Fire HP separately from ordinary physical Armor**: apply Fire Resistance to the Fire HP packet, and apply Armor/Penetration to the physical carrier packet only. Vigor burn remains independent. Do not duplicate normal Armor or Strong/Critical dice per packet; hybrid effects must supply any more specialized rule.

**VC guardrail:** [Standard Veil Control](technique-tiers-and-expression.md#standard-veil-control-scaling) is `max(VC,0) × Character Level`, applied under its stated **single packet** conditions. A technique may **explicitly author a different coefficient/distribution**, but neither a Primary/Secondary/Rider table nor repeated weapon hits automatically inherit a fresh full Standard VC packet per hit or effect. The Conjure Flame shorthand **`+ VC` is a provisional custom-scaling proposal**, not a generally approved replacement for the current standard.

## 8. Existing High Scholar Composite Casting and future contribution interfaces

### Existing authorization: High Scholar Composite Casting (not deferred)

[High Scholar — Projection through synthesis](../08-archetypes/scholar.md#high-scholar--projection-through-synthesis) **already authorizes Composite Casting**. It is the **specific authority** for combining **one known Primary Technique + one compatible known Secondary Technique**, subject to existing Scholar rules; this document **does not replace its feature, costs or advancement**.

1. **Eligibility and exact profile match:** Both component techniques must be **known**, have an **identical authored profile identifier supported by each component**, and be genuinely **compatible** for the intended expression. The caster freely chooses which known technique is **Primary** and which is **Secondary**, then selects their **common** supported profile; swapping roles may produce a distinct legal composite. **A `Thrown Projectile` is not an `Ammunition Shot`, even though both can fly**. At **levels 1–2**, the exact pair must be a **prepared composite formula**. From **level 3 (Formula Fluency)**, any compatible known pair may be composed without preparing that exact pairing. Knowing techniques does not guarantee that every pair is physically, magically or procedurally compatible.
2. **Host owns resolution:** The **Primary** contributes full normal strength and owns target, range, area/shape, attack/resistance procedure and fundamental delivery. The **Secondary** contributes a lesser effect **inside the Primary's delivery**, not a second independently targeted attack, area, duration or entire separate rider suite. A rock-projectile Primary with an eligible Conjure Flame Secondary is a **single composite projectile**; the rock determines the delivery.
3. **Secondary-value precedence:** When the selected Secondary technique/profile has **explicit authored composite-compatible Secondary effect values**, use those values **once** as its contributed output. **Do not halve or reduce them a second time** under Scholar's generic default. If no bespoke composite Secondary values are authored, the existing [Scholar default Secondary reduction](../08-archetypes/scholar.md#levels-12--technical-repertoire-and-prepared-composite-formulae) remains available for an otherwise compatible known technique: **approximately half its normal scalable numerical output**, plus a **diminished version of one compatible defining special property** where relevant. The generic fallback is **not** permission to improvise impossible target/delivery forms, acquire unlearned techniques or bypass a profile's express exclusion. An authored Secondary for an **item-only or environment-only** use does not become Scholar-compatible automatically; its compatibility must be specified.
4. **Full VP cost; compressed action:** Pay **full Primary VP cost + full Secondary VP cost** as required by [Scholar Composite Casting](../08-archetypes/scholar.md#levels-12--technical-repertoire-and-prepared-composite-formulae); **Secondary's lesser output is not a VP discount**. Use the **slower** component action requirement: Projection + Projection = **one Projection Action**; Projection + Full = **one Full Action**; Full + Full = **one Full Action**. A composite consumes **one combined action** under these rules, not two separate single-spell activations. When **both** compatible components have the exact integrated `Ammunition Shot` profile, the **one paid physical shot or Full-Action crossbow shot is the host action** and the spell attachment adds **0 extra AP**; **pay both full VP costs**, no additional shot or attack roll. Incompatible or mixed action categories without an authored mapping are not automatically legal. Individual component restrictions, tier ceilings, legal resources and incompatible effects still apply.
5. **Level 5 (Advanced Synthesis):** Scholar's **Numerical Emphasis** or **Property Emphasis** further determines the Secondary's *numeric-versus-property distribution*; this feature is **not removed** by an authored Secondary cell. An authored profile can supply explicit compatible level-5 emphasis outputs. Otherwise apply the existing Scholar emphasis defaults to that Secondary output: Numerical emphasizes the half-strength numerical component and strongly diminishes incidental properties; Property supplies little/no numerical output and retains one compatible defining property more substantially. **No double halving** is imposed merely because Secondary values are written out. Final numerical emphasis calibration remains provisional.
6. **Sustained/caster-maintained weapon effects:** Composite Casting is **not automatically** a second simultaneous Reserved Weapon enchantment. The [one-Primary-Reserve-per-weapon rule](#6-reserved-weapon-baseline-and-channel-break) remains in force; applying a second distinct **Secondary Reserve to the same weapon** requires the explicitly deferred advanced specialization. Other sustained combined effects must author a valid anchor, VP commitment and termination procedure rather than assuming they persist forever or refund Spent VP.

**Precedence:** The Scholar's **feature permission, preparation, cost, level gates, and emphasis** govern Composite Casting; the technique's **authored compatible Secondary values** govern its actual contributed effect in place of the generic output approximation. **Primary/Secondary/Rider contribution is a data vocabulary, not a replacement for the Scholar feature.** If an effect cannot be meaningfully specified under either its authored Secondary profile or the established Scholar fallback, it still needs technique content; do not fabricate a new damage or resistance procedure.

### Other selectors — future interfaces unless separately authored

These operations may select contribution strength, but **do not** create new permissions simply because Secondary or Rider values are recorded:

- **Other composition:** a future *non-Scholar* feature or item may define its own host, permitted contribution(s), AP/VP prices, target/defense and stacking. There is no generic composition entitlement for other Archetypes.
- **Conversion:** an item may **replace** a cast's result with the **Secondary** form of another technique (e.g. once every 24 hours convert to Conjure Flame). This is **not** inherently additive to the original effect; the item defines replacement, charges, costs and eligible profile.
- **Environmental downgrade:** a Veil anomaly may **force Secondary** for an otherwise standalone Primary use. Its rule specifies affected techniques, when selection occurs and whether resource costs change; no blanket free VP refund or tier reduction follows.
- **Rider from item:** a gem could supply Conjure Flame's **Vigor-only Rider contribution** to a sword already affected by a Primary Lightning Reserve, **without** the wielder reserving Fire VP. This is a future item property example, **not an MVP acquisition/crafting rule**.

**Deferred:** **new general/non-Scholar** composition authorizations and broader stacking algorithms, second Reserved enchantment specializations, permanent magical investments, item rarity/economy/recipe/charges, general environment downgrades and final higher-tier Composite burst calibration. **High Scholar Composite Casting itself remains current canon**; its exact repertoire/prepared-formula counts and technique-level compatibility/numbers may still need authoring.

## 9. Authoring template and acceptance gates

For each technique, fill the common identity; for **each supported profile × contribution**, fill what actually differs. Do not manufacture invalid combinations.

| Field | Required authoring content |
|---|---|
| Identity / access | Technique name; canonical Pillar/Aspect; Base Tier; source/access restrictions; eligible levels |
| Tier | Used Tier and ceiling; which variables scale; values at target test levels |
| Profile | Named recipient/delivery, legal range, components, target/anchor, supported contribution(s), conditions |
| Activation | AP category and timing; default one Focus-priced Projection Action for ordinary single spells; any exception |
| VP operation | Cost; **Spent**, **Committed**, or expressly authored hybrid; anchor, release and channel break |
| Contribution | Primary / Secondary / Rider effect packets and **source of permission** for reduced/limited versions |
| Delivery and defenses | Manifestation/Imposition/Intrusion/ordinary physical carrier, attack or contest, Guard/Dodge/cover/Intrusion as applicable |
| Outcome packets | HP vs Vigor vs healing/repair/control; type; fixed/dice formula; resistance/armor interaction; critical/defense triggers |
| Scaling | VC formula and **per-target/per-hit allocation**, tier; do not inherit standard VC repeatedly |
| Persistence | Ending conditions, sustained nature, and **Continuous / Rider cadence / Pulse / Spend** for each recurring output |
| Compatibility | [Projection], [Embodiment], Inward, Consecration, Devotional Rite, Conduit Form, Investment, Archetype/Focus permissions **only where explicitly authored** |
| Composition/item hooks | Whether the profile's Secondary is **High Scholar Composite-compatible**, item-only or environment-only; applicable authoring override to Scholar's default half-strength Secondary; separate future conversion/item Rider hooks, no implicit permissions |

**Technique authoring is incomplete** if its intended use lacks a legal target, effect, VP/AP price, applicable resolution, defensive interaction or persistence/trigger definition. An Aspect identity and this template alone never grant a character a castable technique.

## 10. Executable worked example — Conjure Flame v0

[Conjure Flame v0](conjure-flame-v0.md) is now the **first authored Fire / Conflagration technique**, with three exact profile identifiers (`Thrown Projectile`, `Weapon Enchantment`, `Ammunition Shot`), **Primary, Secondary and Rider** numerical expressions, Spent/Committed VP handling, immediate thrown resolution, unlimited eligible Reserved Weapon hits, and spontaneous or discounted 24-hour prepared physical ammunition. Its **numeric formulas are provisional v0 playtest values**, not final calibrated balance. The executable technique entry, not the old example embedded in PR #62, is the authority for the current nine contribution expressions, cost, compatibility and AP timing.

The **Rider contribution** does not itself authorize a gem or other independent item. A **Secondary** must match the Primary's **exact authored profile key** for current High Scholar Composite Casting; the `Weapon Enchantment` Secondary remains blocked from simultaneous double reservation absent a later specialization. See also the [elemental resistance](elemental-damage-resistance-v0.md) and [ammunition](../05-combat/prepared-and-spontaneous-ammunition-v0.md) rules.

## 11. Regression examples / review checklist

| Test | Expected v0 ruling |
|---|---|
| High / Medium / Low casts one ordinary spell | Costs **20 / 24 / 30 AP** respectively unless the individual profile overrides it |
| Conjure Flame Thrown Flame | One paid spell activation; independent manifested thrown projectile, native defenses; no extra physical attack AP |
| Character reserves Conjure Flame on one sword | **Primary** applies; Committed VP tied up; later successful paid sword attacks can trigger it without per-hit VP, turn or hit cap |
| Reserved sword successfully Disarmed | Effect ends immediately; **all Committed VP available again**, not Spent; already paid spell/attack AP not refunded; retrieval does not re-enchant |
| Sword also has independent Conjure Flame gem | Its **Rider contribution** needs no caster Fire reservation; remains a property of the item when the sword's unrelated Lightning Reserve ends |
| Two different caster-maintained reserves on one sword | **Not v0 legal** without later specialization granting that composition |
| Two different profile keys, e.g. `Thrown Projectile` + `Ammunition Shot` | **Not legal for Composite Casting**, even if both are ranged; the pair requires a shared exact supported profile identifier |
| Integrated spell enhancement to arrow | **0 extra Projection AP**, but the shot itself retains ordinary Physical/Full Action and pays the VP for every launched spontaneous enchantment |
| Prepared physical arrow | Discounted Spent VP at preparation, **24-hour expiry**; recovery ticks do not erase it; one major enchantment only |
| Fire resistance eliminates Fire HP component | Does **not** automatically eliminate the independent Vigor-burning packet if the delivery hit/trigger was valid |
| Cast under an environmental Secondary restriction | The spell may still stand alone; effect uses Secondary, and AP/VP change **only if the environment explicitly says so** |
| **High Scholar composite flaming rock** | Composite Casting permits the known matching **`Thrown Projectile`** Primary + Secondary in either chosen role, if the other technique is actually authored/compatible. Pay both full VP costs and one slower component action. The selected Primary owns delivery; Conjure Flame v0 supplies its **explicit authored Secondary** if chosen Secondary, without a second halving. |
| High Scholar, known compatible Secondary without bespoke output | Existing Scholar fallback applies: approximately half numerical output plus one diminished compatible defining property; do not declare Composite Casting universally deferred. |
| High Scholar, authored composite-compatible Secondary output | Use explicit Secondary numerical/property contribution once, **not** another automatic 50% reduction; full VP paid for both components and one slower action. |
| High Scholar, level 5 emphasis | Numerical or Property Emphasis still modifies the Secondary under Scholar rules; an authored compatible emphasis variant may define exact values. No silent double-halving. |
| One-Aspect healing or stone-skin technique | [Basic Heal v0](basic-heal-v0.md) authors one **`Single Target`** profile; no requirement to invent three attack deliveries. A future stone-skin technique may be Self only. |
| Basic Heal, genuinely beneficial on unconscious Dying ally | **No Intrusion contest**; instant Vigor restoration plus **HP-component → direct Repair Progress** while an active repairable wound remains; no free regeneration step |
| Basic Heal, consciously resisted by a conscious creature | **Intrusion contest with +8 barrier** and Basic Heal's authored **Intellect vs Vitality + Awareness** Ability pair; a failed contest still spends attempted spell VP |

## Status and next content work

**Structure v0 and Conjure Flame v0 are merged; Basic Heal v0 is now proposed as the second Pillar technique.** B05 still lacks a *sufficient executable Pillar technique catalogue*, starting prayers/repertoires, Gifted Conduits and Embodiments, Anointed Signatures, and the complete twelve Archetype × Focus playable builds. The eight selected [MVP Pillars](../../design/b05-eight-pillar-mvp-selection-and-coverage.md) remain Fire, Life, Earth, Liberty, Mind, Kinship, Secrets and Arts.

**Next:** review and playtest [Basic Heal v0](basic-heal-v0.md) (HP/Vigor/Repair Progress and beneficial Intrusion), then author **Mind / Psionics** (Imposition and physical force). Numerical values and item/specialized usage permissions remain **provisional**.
