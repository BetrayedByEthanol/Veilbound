# Stone Skin v0 — Earth / Fortification

> **Executable v0 defensive technique; numerical resistance and VP economy remain provisional for level 1–3 playtesting.** **Earth / Fortification** is the canonical **Internal** Aspect. Stone Skin reinforces the caster's own physical integrity through **beneficial self-targeted Intrusion**, with persistent **typed HP damage resistance**, **not Armor**, extra Guard/Dodge, temporary HP or generic Direct Veil Resistance. Neither knowing Earth/Fortification nor publication here automatically teaches this technique: apply actual Archetype technique-access rules.

References: [Aspect identity](../../world/aspect-identities-and-boundaries.md), [Technique Structure](technique-structure-v0.md), [Technique Tiers and Cadence](technique-tiers-and-expression.md), [VP states](volition-points.md), [Elemental HP resistance](elemental-damage-resistance-v0.md), [Armor](../05-combat/weapons-and-armor.md), [Defense and Criticals](../05-combat/defensive-responses-and-criticals.md), [Reaction timing](../05-combat/initiative-and-round-structure.md), and [Beneficial Intrusion](resonance-and-intrusion.md#intrusion-barrier).

## Identity and executable profile

| Property | Stone Skin v0 |
|---|---|
| Pillar / canonical Aspect | **Earth / Fortification**, **Internal** |
| Base Tier / access | **Tier 1**; individual technique access required |
| Used Tier | **T ≥ 1** within ordinary level ceiling (L1–2: T1; L3: up to T2); **no additional Tier-based enhancement** to this v0 technique |
| Exact profile identifier | **`Self`** only; the caster is the sole recipient |
| Components | **None**; caster must nevertheless be conscious, capable of the chosen activation, and legally able to use the relevant action/Reaction |
| Expression / interaction | **[Projection]**, beneficial, willing **self-Intrusion** reinforcing one's own body; **no normal Direct Veil contest** |
| Target / range / sight | **Self, 0 squares**. No independent line of sight/path or external targeting is required |
| Normal activation | **One Projection Action on own turn**, High **20 AP** / Medium **24 AP** / Low **30 AP** |
| Reactive activation | **One Reaction** on a qualifying [trigger](#reactive-activation--no-ap-debt); **0 immediate Turn AP**, **no subsequent AP debt** |
| VP price / handling | **`ceil(Max VP / 3)` Committed VP**; payable from Available VP at activation; **no Spent VP** for standalone Stone Skin |
| Duration / cadence | **Maintained / Continuous** while its VP remain Committed and caster remains conscious; no turn counter, pulse, upkeep roll, per-hit expenditure, or periodic VP payment |
| Effective HP resistance | **`R = 2 + floor(max(0, VC) / 4)`**, snapshotted on successful activation |
| Eligible HP damage types | **Physical** (e.g. cut/slash, pierce, crush/blunt), **Fire**, **Electrical**; exact physical/elemental type catalogue remains provisional |
| Source of damage | **Irrelevant**: mundane or magical cause does not alter a packet's authored damage type; both qualify identically |
| Ineligible harm | **Vigor damage**, unlisted HP damage types (e.g. Acid/Poison), non-HP effects, magic contests and wounds unaffected except through actual reduction of eligible HP damage |
| Armor / Guard / Dodge | Worn **Armor remains separate and combines** with the one applicable resistance; no Penetration reduction to Stone Skin, no extra Guard/Dodge or Agility/Movement restrictions |
| Resistance source stacking | Among **all sources of resistance applicable to the same HP packet**, apply **the highest one once**, **not their sum**; physical Armor is not a resistance source |
| Stacking with itself | **One active instance per caster**; additional Stone Skin casts do not compound, reroll or stack the protection |
| End condition | **Immediate termination on unconsciousness**, voluntary legal release, or other expressly applicable effect/channel termination; committed VP return to Available |
| Stone Skin contribution | **Primary only**; **no Stone Skin Secondary or Rider** |
| Scholar Composite authorization | **Stone Skin Primary + compatible `Self` Secondary** in a **normal on-turn composite Projection Action**, including [Basic Heal v0](basic-heal-v0.md)'s authored `Self` Secondary **applied once on successful activation**; full component VP prices |
| Explicit exclusions | No automatic Reactive Composite Casting, no reactive healing, no armor-rating increase, no general magical immunity, no multiple-target variant, no free out-of-turn spell |

## Resistance value and damage resolution

Compute and snapshot on successful activation:

```text
R = 2 + floor(max(0, caster's Veil Control) / 4)
```

**`VC` is the actual caster's Veil Control at activation, with negative values treated as 0 for this output.** There is **no standard VC × Level packet**, no Tier multiplier and no post-activation recalculation each round or when temporary VC modifiers change. Recasting as a new instance after the old one ends snapshots again.

| VC at activation | Stone Skin R |
|---:|---:|
| −2 / 0 / +2 / +3 | **2** |
| +4 / +7 | **3** |
| +8 / +11 | **4** |
| +12 | **5** |

Stone Skin applies to **HP damage packets**, never to Vigor. An eligible packet remains eligible whether caused by a mundane weapon, magically created physical projectile, ordinary blaze, Conjure Flame Fire HP packet, or authored Electrical HP technique/hazard. Merely being *magical* does not cause a Fire or physical packet to bypass its type. Conversely, an **Intrusion effect that changes HP or Vigor without an authored eligible damage type** does **not** acquire Physical/Fire/Electrical type automatically and is not reduced merely for being described as harmful.

**Source stacking: maximum only.** For each incoming typed HP packet, identify the resistance values from **all currently applicable sources**. Use the **single highest applicable resistance value**, not a sum or one subtraction per source. A separate source may protect another packet/type, but two protections qualifying for the **same packet** never double-dip merely by using different labels. Immunity or an explicitly specialized defense continues to follow its own authored rules; the highest-only rule does not downgrade immunity. This highest-only rule is also recorded in the shared [Elemental HP Damage and Resistance](elemental-damage-resistance-v0.md) baseline. **Physical Armor is its own subsystem, not another resistance value.**

**Application order:**

1. Resolve normal attack, any declared Take Hit / Dodge / Guard, cover and Strong / Critical / Devastating Critical determination **before** damage mitigation. An attack that misses or is fully blocked does not trigger on-hit damage packets.
2. For a successful **physical HP packet**, include ordinary weapon/attack and any eligible Strong/Critical bonus dice **once** in that packet; then compute **Effective Armor = max(Armor − Penetration, 0)** and subtract it once. **Then** subtract the highest applicable physical HP resistance (including Stone Skin if it is the highest), floor resulting HP damage at 0. Penetration does **not** reduce Stone Skin's R.
3. For an **independent Fire or Electrical HP packet**, apply its **highest applicable typed resistance once**, floor at 0. Do **not** apply ordinary Armor to an elemental-only packet or subtract Stone Skin again because the same hit also had a physical carrier packet.
4. Preserve independent **Vigor packets** unchanged by Stone Skin even if the corresponding Fire or physical HP packet becomes 0. Determine 0-HP and Devastating Critical wounds under the normal wound rules; Stone Skin is not a blanket prevention of an independent Devastating Critical wound trigger.
5. Other damaging conditions, terrain/hazard rules, special armor bypass and protections keep their own authored restrictions. Do not invent Electrical or physical types for effects lacking them.

**Examples:**

| Situation | Result |
|---|---|
| Ordinary 10 Physical HP, Armor 5, Penetration 3, Stone Skin R2 | Effective Armor 2, then R2 → **6 HP taken** |
| Mundane Fire 6 HP, Stone Skin R2 | **4 Fire HP taken** |
| Conjure Flame Fire 6 HP, Stone Skin R2 | **4 Fire HP taken**; exact same result as mundane Fire |
| Native Fire Resistance 3 plus Stone Skin Fire R2 versus Fire 6 HP | **max(3,2) = 3 resistance**, so **3 Fire HP taken**; not Resistance 5 |
| Native Physical Resistance 4 plus Stone Skin R2 versus 10 Physical HP after effective Armor 2 | Use **R4 once**, so **4 HP taken**, not R6 |
| Same attack has 7 Physical HP + 2 Fire HP + 3 Vigor; effective Armor 3; Stone Skin R2 | Physical HP **2**, Fire HP **0**, Vigor **3** (unaffected) |
| Acid HP 6 or separate Vigor 4; Stone Skin R2 | Stone Skin reduces **neither** |
| Piercing magical projectile vs physically identical mundane projectile | Same Physical resistance applies; no magical-source exception |
| Physical Penetration 6 versus Armor 5, Stone Skin R2, raw Physical HP 10 | Armor becomes 0; Stone Skin remains R2; **8 HP taken** |
| Strong/Critical attack | Bonus HP dice enter the eligible main packet before mitigation; Stone Skin **does not negate** qualifying Devastating Critical wound trigger by name alone |

## Two alternative activation methods — locked

An eligible caster chooses **one** activation method per attempt, never both. Stone Skin does not require or inherit Reactive Blink's next-turn AP Debt.

### A. Normal Projection Action

On the caster's own turn, pay **one Projection Action**: High **20**, Medium **24**, Low **30** Turn AP. The caster may activate proactively, without waiting for a threat. On successful activation reserve the VP and establish **Continuous** protection immediately. The cast does **not** also consume the caster's Reaction.

### B. Reactive activation — no AP debt

**Authorized trigger:** The conscious caster is the declared target of an **incoming attack**, or is about to be affected by a **perceptible imminent damaging hazard**. The caster must be capable of perceiving the threatening event and have an **unused Reaction**. There is no general out-of-turn trigger for mere suspicion or an already completed attack or hazard. This Reactive permission applies **only to standalone Stone Skin Primary**, not to combined healing or another composite.

**Response window:** Against an attack, declare Stone Skin **after the incoming attack has been committed/declared and before its attack roll resolves**; against a qualifying hazard, declare **before that hazard's damage is determined/resolved**. **Do not** wait to see the attack roll, hit/miss, damage dice, HP loss or a wound result. If no perception of the triggering danger was possible before its damage resolved, no retroactive Reaction is allowed. Stone Skin cannot undo already dealt damage.

Follow the canonical [response timing](../05-combat/initiative-and-round-structure.md#response-windows-and-nested-responses): resolve **precommitted Interceptions** and their nested effects first; re-check that the original threat still exists; then, at the normal spontaneous-response step, spend **one Reaction** to attempt Stone Skin. If an earlier Interception cancels the event, no Stone Skin Reaction may be declared on that cancelled original trigger. A genuinely new independent nested hazard/attack may generate its own legal response window. Stone Skin is **not** a Guard/Dodge/Take Hit choice or an additional defense assignment.

If the Reaction cast is valid and resolves before the triggering hit/hazard damage, **Stone Skin protects against that damage and remains maintained thereafter**, without further Reactions for subsequent eligible packets. The caster still has their ordinary Guard/Dodge/Take Hit options where the attack and defense rules allow them.

**Reactive costs: one Reaction, no Projection AP and no AP Debt.** The one-third-Max-VP Reserve is its substantial sustained resource commitment. Reactive Stone Skin and Reactive Blink compete for the same single Reaction, but **do not share Blink's debt rule**. The effect cannot trigger a free healing Secondary or any extra magic on that Reaction.

### Funding, resolution, and termination

1. **Declare:** Choose normal or reactive activation; confirm technique access, `Self` Primary, legal timing, caster consciousness and ability to activate, no already-active Stone Skin, and **available resources**. Determine the **effective Committed VP cost**: `ceil(current Max VP / 3)`, applying only a specifically eligible cost modifier (ordinary **Spent VP** discounts do not automatically apply to a **Committed VP** cost). **Available VP must cover the entire locked Reserve** at declaration or the attempt is **illegal**: no AP/Reaction is committed and no response trigger is created.
2. **Commit activation capacity:** Pay the Focus-priced **Projection Action AP** *or* the single **Reaction**. The cost selected is now committed and is not refunded merely because an Interception, suppression or other legal response interrupts the attempted cast. **No AP or AP Debt** is ever charged for the reactive method; normal on-turn casting does not consume a Reaction.
3. **Resolve after responses:** Confirm the caster is still conscious, self-targeting and otherwise permitted to activate, and **recheck Available VP ≥ the locked effective Reserve**. If the action is interrupted, activation becomes illegal, or the Reserve is no longer affordable, **no Stone Skin effect is created and no VP are committed**; the already spent AP/Reaction remains lost. Do not reduce the Tier/cost retroactively or silently convert a failed reaction to the other activation method. A valid beneficial self-Intrusion ordinarily involves **no Direct Veil contest**, but an actual authored ward, suppression or specific self-Intrusion prohibition still applies.
4. **Successful activation:** Move the locked Reserve amount **Available → Committed VP**; snapshot `R` using the caster's VC at this instant. The Continuous protection starts **now**, before a triggering attack/hazard damages the caster if the Reaction's timing was legal. There is no recurring VP payment or AP cost while maintaining it.
5. **Maintenance/end:** The caster can sustain Stone Skin across rounds while **conscious and the VP remain Committed**. **Unconsciousness terminates it immediately** (including unconsciousness caused by a subsequent injury); death or an explicitly applicable suppression/channel-ending condition also ends it. It may also be **voluntarily released at a legal own-turn decision point with no action cost**, not in a new free interrupt window. On end, its still-Committed VP **return to Available VP immediately**; nothing spent on a separate Secondary is refunded. Regaining consciousness does not restore the ended instance; reactivation needs a new legal cast. The active Reserve's snapshot VP amount does not fluctuate every round with later changes to Max VP.

**Standing in the same damaging hazard:** An active Stone Skin works on every eligible packet for as long as maintained, with no repeated Reaction; a caster activating reactively needs **a new legitimate impending hazard event**. There is no unlimited Reaction each time the caster notices an ongoing condition, and no retroactive protection against earlier damage.

## High Scholar Composite — Stone Skin Primary + Basic Heal Secondary

**Authorized on-turn combination:** A **High Scholar** who knows both techniques, meets the existing **prepared pair at levels 1–2 / Formula Fluency at level 3+** restrictions, and legally selects the identical exact **`Self`** profile may use Stone Skin as **Primary** with [Basic Heal v0](basic-heal-v0.md) as **Secondary**. **The composite must satisfy both components' requirements**, including Basic Heal's **one functioning available hand** even though standalone Stone Skin has no material/hand components. This particular pair is authored compatible **only when declared as a normal on-turn Projection Action**. It does **not** grant reactive composite casting, an extra reaction-based heal or a Stone Skin Secondary in reverse order.

- The entire composition consumes **one Projection Action**, High **20 AP** (the current High Scholar Focus), not two actions. No additional AP debt or trigger response arises from Basic Heal.
- Pay **both full component prices**: Stone Skin **`ceil(Max VP / 3)` Committed VP**, and Basic Heal **`2 × T_heal` Spent VP**, with only discounts specifically applicable to their respective components. Before declaration and again at legal resolution, require **Available VP ≥ the entire effective combined requirement**; no partially funded combination or post-declaration downgrading.
- On a successful authorized self-application, **commit the Stone Skin reserve** and **spend Basic Heal's full VP cost once**; resolve Basic Heal's **authored `Self` Secondary exactly once** at the time of casting: **1 HP** plus **`2 + ceil(d6 × T_heal / 6) + max(0, VC)` Vigor**, subject to Basic Heal's own missing-resource caps and wound-repair conversion. This is **not** recurring restoration and is **not** further halved.
- Stone Skin remains **Primary Continuous resistance**, with its own normal end/VP return. The **Spent healing VP never return** merely because Stone Skin later ends. The primary self-only target and normal resistance/eligibility govern; neither technique grants a second target, a separately created body, or a second action. If the caster becomes ineligible before application, no Partial Stone Skin/Basic Heal activation is silently substituted.

**Example:** Level-1 High Scholar with Veil Affinity +0 has **Max VP 6**. Stone Skin's Reserve is **2**, Basic Heal Tier 1 costs **2 Spent VP**, so composite declaration requires at least **4 Available VP**. With 6 Available, after successful activation: **2 Committed**, **2 Spent**, **2 Available**. When Stone Skin later ends, the 2 Committed VP return; **4 Available / 2 Spent** remain.

## Regression matrix

| Scenario | Expected result |
|---|---|
| High/Medium/Low Focus declares Stone Skin normally with enough AP/VP | **20/24/30 AP**, no Reaction; reserve **ceil(Max VP/3)** on success |
| Incoming declared attack, caster has Reaction and sufficient Available VP | Reactive cast may resolve **before attack roll** using **1 Reaction, 0 AP, 0 AP debt**, with normal response priority |
| Threat cancels in an earlier precommitted Interception | No Reactive Stone Skin declaration for cancelled original trigger; no Reaction/VP spent |
| Attack has already rolled/damaged caster before reaction choice | **No retroactive activation**; too late |
| Perceptible imminent damaging environmental hazard | One Reaction can activate **before** damage event; no instant repeat once hazard damage is known |
| Caster lacks Reaction before eligible trigger | Cannot activate reactively; may still cast normally on own turn with AP |
| Normal caster has AP but insufficient Available VP for Reserve | **Cannot declare**, no AP or response bait |
| Reactive caster has Reaction but insufficient Available VP for Reserve | **Cannot declare**, Reaction preserved |
| VP becomes insufficient after legal reactive declaration, before application | Cast fails, **Reaction spent**, **0 VP Committed**, no resistance |
| Level 1 High / Medium / Low Focus, Veil Affinity +0 | Max VP **6/4/2**, Reserve **2/2/1** |
| Level 3 High / Medium / Low Focus, Veil Affinity +0 | Max VP **18/12/6**, Reserve **6/4/2** |
| VC −1, +0, +2, +4, +8 | R **2, 2, 2, 3, 4**, snapshotted on successful activation |
| Fire from wildfire and Fire from Conjure Flame, same Fire HP packet value | **Same Stone Skin resistance**; magical/mundane provenance irrelevant |
| Incoming Physical 10, Armor 5, Penetration 3, Stone Skin R2 | Effective Armor **2**, final **6 HP** |
| Native Fire Resistance 3 and Stone Skin Fire R2 | Effective resistance **3**, not 5 |
| Native physical resistance R4, Stone Skin R2, Armor 5 vs Penetration 3 and Physical HP 10 | Effective Armor **2**, resistance **4**, final **4 HP** |
| Physical 7 HP, Fire 2 HP, Vigor 3, effective Armor 3, Stone Skin R2 | **2 Physical HP**, **0 Fire HP**, **3 Vigor** |
| Physical damage from magical conjuration versus same mundane physical attack | Same Physical R; no global magic-source exception |
| Acid HP, poison HP or direct Vigor | Not reduced unless separately protected |
| A Critical attack with extra physical HP dice | Damage dice before Armor then highest Physical R; Stone Skin does not erase Critical/Devastating classification |
| Already maintained Stone Skin and a subsequent attack | Protection applies automatically; **no further AP/Reaction/VP** |
| Same caster attempts second simultaneous Stone Skin | **Cannot stack/refresh** the active instance |
| Caster falls unconscious | Stone Skin terminates immediately; Committed VP return |
| Caster voluntarily releases on own turn | Ends at legal own-turn decision point, 0 action cost; VP return |
| Reactive Stone Skin tries to add Basic Heal Secondary | **Illegal**; reactive mode does **not** authorize Composite or healing |
| Legal High Scholar `Self` composite, Stone Skin Primary + Basic Heal Secondary, both T1 | Requires **one functioning available hand** for Basic Heal; one High **20-AP** Projection Action; Reserve **ceil(Max VP/3)** plus Spend **2 VP**, heal once |
| Level-1 High Scholar Max VP 6 composite, starts 6 Available | At activation **2 Committed / 2 Spent / 2 Available**, heal once |
| Same composite maintains Stone Skin several rounds | Basic Heal's Secondary **never repeats**; ending Stone Skin returns only Committed VP |
| Stone Skin technique known but no Archetype authorization to use it | No cast; document does not grant automatic repertoire |

## Status

**v0 design lock:** separate **normal Projection Action** and **standalone Reaction** activation methods, with **no reactive AP debt**; one-third-Max-VP Committed Reserve, maintained until unconsciousness/release; type-based Physical/Fire/Electrical **HP resistance** independent of damage source; **highest applicable resistance once per HP packet**, while worn Armor remains separate; `Self` Primary, no Stone Skin Secondary/Rider, and on-turn High Scholar Stone Skin Primary + `Self` Basic Heal Secondary resolved once. Numerical balance, damage-type coverage and higher-tier utility remain **provisional**. B05 remains open pending enough Pillar/Aspect and Archetype repertoire to play all twelve MVP builds.
