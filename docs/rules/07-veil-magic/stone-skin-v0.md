# Stone Skin v0 — Earth / Fortification

> **Executable v0 defensive technique; numerical resistance and VP economy remain provisional for level 1–3 playtesting.** **Earth / Fortification** is the canonical **Internal** Aspect. Stone Skin reinforces the caster's own physical integrity through **beneficial self-targeted Intrusion**, with persistent **typed HP damage resistance**, **not Armor**, extra Guard/Dodge, temporary HP or generic Direct Veil Resistance. Neither knowing Earth/Fortification nor publication here automatically teaches this technique: apply actual Archetype technique-access rules.

References: [Aspect identity](../../world/aspect-identities-and-boundaries.md), [Technique Structure](technique-structure-v0.md), [Technique Tiers and Cadence](technique-tiers-and-expression.md), [VP states](volition-points.md), [Elemental HP resistance](elemental-damage-resistance-v0.md), [Armor](../05-combat/weapons-and-armor.md), [Defense and Criticals](../05-combat/defensive-responses-and-criticals.md), [Reaction timing](../05-combat/initiative-and-round-structure.md), and [Beneficial Intrusion](resonance-and-intrusion.md#intrusion-barrier).

## Identity and executable profile

| Property | Stone Skin v0 |
|---|---|
| Pillar / canonical Aspect | **Earth / Fortification**, **Internal** |
| Base Tier / access | **Tier 1**; individual technique access required |
| Used Tier | **T ≥ 1** within [the ordinary universal tier ceiling](technique-tiers-and-expression.md#universal-technique-tiers) at the character's level (e.g. **L1–2 max T1, L3–4 max T2, L5–6 max T3, L7–8 max T4, L17–20 max T9**); **no additional Tier-based enhancement** to this v0 technique |
| Exact profile identifier | **`Self`** only; the caster is the sole recipient |
| Components | **None**; caster must nevertheless be conscious, capable of the chosen activation, and legally able to use the relevant action/Reaction |
| Expression / interaction | **[Projection]**, beneficial, willing **self-Intrusion** reinforcing one's own body; **no normal Direct Veil contest**. The `[Projection]` tag does not prevent automatic Low Priest **Devotional Rite** eligibility for this self-targeted maintained Committed-VP profile |
| Target / range / sight | **Self, 0 squares**. No independent line of sight/path or external targeting is required |
| Normal activation | **One Projection Action on own turn**, High **20 AP** / Medium **24 AP** / Low **30 AP** |
| Reactive activation | **One Reaction** on a qualifying [trigger](#reactive-activation--no-ap-debt); **0 immediate Turn AP**, **no subsequent AP debt** |
| VP price / handling | Base **`ceil(Max VP / 3)` Committed VP**; for a Low Priest's actual **Chosen Devotion Rite**, reduce by **1 Committed VP, minimum 1**. Pay from Available at activation; **no Spent VP** for standalone Stone Skin |
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
| Scholar Composite authorization | **Stone Skin Primary + compatible `Self` Secondary** in a **normal on-turn composite Projection Action**. Explicit partners: [Basic Heal v0](basic-heal-v0.md)'s `Self` Secondary once on successful activation, or [Vital Shelter v0](vital-shelter-v0.md#high-scholar--explicit-composite-casting-compatibility)'s **maintained, subordinate `Self` Secondary finite Vigor budget**. Pay all component VP prices; **never** attach either through Reactive Stone Skin |
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

1. **Resolve the damage source's own procedure first.** For an attack, determine its hit/miss, Take Hit / Dodge / Guard, cover and any Strong / Critical / Devastating Critical bonus dice before mitigating the resulting HP packets. For a hazard, determine the **hazard's own authored damage generation and mitigation requirements** (e.g. Landing Control and specialized Impact Armor for a standard fall); **apply its Armor mitigation once in Steps 2–3**, not separately here and then again later. A missed/fully blocked attack does not create its normal hit-triggered damage packets.
2. **Physical HP packets:** Apply **only the Armor/mitigation formula specifically authorized by their source**, then subtract the **one highest eligible physical HP resistance** (including Stone Skin if highest) from the resulting nonnegative packet and floor final HP damage at 0. For an **ordinary weapon attack**, use its usual **Effective Armor = max(Armor − Penetration, 0)**, applied once, followed by resistance; Penetration reduces effective **weapon Armor**, **not Stone Skin**. This weapon equation is **not** a universal Armor formula for every physical hit.
3. **Physical hazards retain their specialized mitigation.** For a standard [hard-surface fall](../05-combat/physical-hazards-v0.md#falling-damage-v0--standard-impact), resolve any Landing Control dice reduction and applicable surface/equipment adjustments, then use the locked **Impact Armor = floor(normal Armor / 2)** **once** against the one **Crush-type physical HP packet**. **Only after that** subtract the highest applicable Crush/Physical HP resistance (Stone Skin qualifies) once. **Do not substitute full normal Armor**, introduce ordinary weapon Penetration, or apply Armor twice. For other hazards with authored Armor/bypass procedures, use those specific procedures before eligible typed resistance. Hazards with no authored damage or typing do not gain one here.
4. For an **independent Fire or Electrical HP packet**, apply its **highest applicable typed resistance once**, floor at 0. Do **not** apply ordinary weapon Armor to an elemental-only packet or subtract Stone Skin twice because the same hit also had a physical carrier packet.
5. Preserve independent **Vigor packets** unchanged by Stone Skin even if the corresponding Fire or physical HP packet becomes 0. Determine 0-HP and Devastating Critical wounds under the normal wound rules; Stone Skin is not a blanket prevention of an independent Devastating Critical wound trigger. Apply the hazard's separately authored post-contact posture/Prone, fall state and wound consequences **even when eligible resistance reduces falling HP damage to zero**. Do not invent Electrical or physical types for effects lacking them.

**Examples:**

| Situation | Result |
|---|---|
| Ordinary weapon attack: 10 Physical HP, Armor 5, Penetration 3, Stone Skin R2 | Weapon Effective Armor 2, then R2 → **6 HP taken** |
| Ordinary weapon attack: 10 Physical HP, Armor 5, Penetration 0, Stone Skin R2 | Weapon Effective Armor 5, then R2 → **3 HP taken** |
| Standard fall: 10 Crush HP rolled, normal Armor 5, Stone Skin R2, no other adjustment | Locked falling Impact Armor **floor(5/2)=2**, then R2 → **6 HP taken**; **not** 3 HP from ordinary weapon Armor |
| Same standard fall, normal Armor 5, no eligible physical resistance | Impact Armor **2** → **8 HP taken**, unchanged locked Falling baseline |
| Same standard fall, native Physical/Crush R4 and Stone Skin R2 | Impact Armor **2**, then **max(4,2)=4** resistance → **4 HP taken**; not cumulative R6 |
| Small standard fall whose resulting Crush HP packet is reduced to 0 by Stone Skin | **0 HP taken**, but the locked falling **Prone/landing consequences still apply** |
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

1. **Declare:** Choose normal or reactive activation; confirm technique access, `Self` Primary, legal timing, caster consciousness and ability to activate, no already-active Stone Skin, and **available resources**. For a **Low Priest with this Prepared** it automatically qualifies as one Devotional Rite under [Priest](../08-archetypes/priest.md#devotional-rites): first check the **shared Active Rite cap** at declaration (L1–3 one; L4+ two), **including Reaction activation**, and later recheck at application. No cast may bypass the cap by calling this a non-Rite. Determine the **effective Committed VP cost**: base `ceil(current Max VP / 3)`; reduce by **1, minimum 1**, only if Stone Skin was designated **Chosen Devotion** during preparation, this **specific new Stone Skin instance** was declared **Chosen**, and **no other active Rite instance is Chosen**. A Prepared Stone Skin cast that is non-Chosen (including while a different Chosen Rite is active at L4+) pays its full base Reserve. Lock the effective Reserve before responses; ordinary **Spent VP** discounts cannot lower it. **Available VP must cover the entire locked effective Reserve** at declaration or the attempt is **illegal**: no AP/Reaction is committed and no response trigger is created. This Rite eligibility grants no Reaction to a different technique, no Exaltation property, and no extra Active Rite.
2. **Commit activation capacity:** Pay the Focus-priced **Projection Action AP** *or* the single **Reaction**. The cost selected is now committed and is not refunded merely because an Interception, suppression or other legal response interrupts the attempted cast. **No AP or AP Debt** is ever charged for the reactive method; normal on-turn casting does not consume a Reaction.
3. **Resolve after responses:** Confirm the caster is still conscious, self-targeting and otherwise permitted to activate, **recheck Low Priest Active Rite cap if applicable**, and **recheck Available VP ≥ the locked effective Reserve**. If the action is interrupted, activation becomes illegal, or the Reserve is no longer affordable, **no Stone Skin effect is created and no VP are committed**; the already spent AP/Reaction remains lost. Do not reduce the Tier/cost retroactively or silently convert a failed reaction to the other activation method. A valid beneficial self-Intrusion ordinarily involves **no Direct Veil contest**, but an actual authored ward, suppression or specific self-Intrusion prohibition still applies.
4. **Successful activation:** Move the locked Reserve amount **Available → Committed VP**; snapshot `R` using the caster's VC at this instant. The Continuous protection starts **now**, before a triggering attack/hazard damages the caster if the Reaction's timing was legal. There is no recurring VP payment or AP cost while maintaining it.
5. **Maintenance/end:** The caster can sustain Stone Skin across rounds while **conscious and the VP remain Committed**. **Unconsciousness terminates it immediately** (including unconsciousness caused by a subsequent injury); death or an explicitly applicable suppression/channel-ending condition also ends it. It may also be **voluntarily released at a legal own-turn decision point with no action cost**, not in a new free interrupt window. On end, its still-Committed VP **return to Available VP immediately**; nothing spent on a separate Secondary is refunded. Regaining consciousness does not restore the ended instance; reactivation needs a new legal cast. The active Reserve's snapshot VP amount does not fluctuate every round with later changes to Max VP.

**Standing in the same damaging hazard:** An active Stone Skin works on every eligible packet for as long as maintained, with no repeated Reaction; a caster activating reactively needs **a new legitimate impending hazard event**. There is no unlimited Reaction each time the caster notices an ongoing condition, and no retroactive protection against earlier damage.

## High Scholar Composite — Stone Skin Primary + compatible `Self` Secondary

### A. Stone Skin Primary + Basic Heal Secondary

**Authorized on-turn Basic Heal combination:** A **High Scholar** who knows both techniques, meets the existing **prepared pair at levels 1–2 / Formula Fluency at level 3+** restrictions, and legally selects the identical exact **`Self`** profile may use Stone Skin as **Primary** with [Basic Heal v0](basic-heal-v0.md) as **Secondary**. **The composite must satisfy both components' requirements**, including Basic Heal's **one functioning available hand** even though standalone Stone Skin has no material/hand components. This particular pair is authored compatible **only when declared as a normal on-turn Projection Action**. It does **not** grant reactive composite casting, an extra reaction-based heal or a Stone Skin Secondary in reverse order.

- **For this Basic Heal composite only**, the entire composition consumes **one Projection Action**, High **20 AP** (the current High Scholar Focus), not two actions. No additional AP debt or trigger response arises from Basic Heal.
- **For this Basic Heal composite only**, pay **both full component prices**: Stone Skin **`ceil(Max VP / 3)` Committed VP**, and Basic Heal **`2 × T_heal` Spent VP**, where **`T_heal` is Basic Heal's independently selected legal Used Tier** under [the universal normal tier ceiling](technique-tiers-and-expression.md#universal-technique-tiers): **L1–2 max T1, L3–4 max T2, L5–6 max T3, L7–8 max T4, and L17–20 max T9** (intervening levels use the canonical table). **No additional Tier-2 or composite-only cap applies**; Tier and access remain checked at declaration. **Stone Skin's own reserve and Tier are unchanged by this choice.** Use only discounts specifically applicable to the one composite activation. Before declaration and again at legal resolution, require **Available VP ≥ the entire effective combined requirement**; no partially funded combination or post-declaration downgrading.
- On a successful authorized self-application, **commit the Stone Skin reserve** and **spend Basic Heal's full VP cost once**; resolve Basic Heal's **authored `Self` Secondary exactly once** at the time of casting: **1 HP** plus **`2 + ceil(d6 × T_heal / 6) + max(0, VC)` Vigor**, subject to Basic Heal's own missing-resource caps and wound-repair conversion. This is **not** recurring restoration and is **not** further halved.
- Stone Skin remains **Primary Continuous resistance**, with its own normal end/VP return. The **Spent healing VP never return** merely because Stone Skin later ends. The primary self-only target and normal resistance/eligibility govern; neither technique grants a second target, a separately created body, or a second action. If the caster becomes ineligible before application, no Partial Stone Skin/Basic Heal activation is silently substituted.

**Example:** Level-1 High Scholar with Veil Affinity +0 has **Max VP 6**. Stone Skin's Reserve is **2**, Basic Heal Tier 1 costs **2 Spent VP**, so composite declaration requires at least **4 Available VP**. With 6 Available, after successful activation: **2 Committed**, **2 Spent**, **2 Available**. When Stone Skin later ends, the 2 Committed VP return; **4 Available / 2 Spent** remain.

### B. Stone Skin Primary + Vital Shelter Secondary

**Authorized on-turn Vital Shelter combination:** An eligible High Scholar may alternatively use **Stone Skin `Self` Primary + [Vital Shelter maintained `Self` Secondary](vital-shelter-v0.md#high-scholar--explicit-composite-casting-compatibility)** in that one normal Projection Action. Vital Shelter contributes only its finite Secondary **`4 + floor(max(0, VC)/2)` Vigor-prevention budget**, not the full Primary budget. Pay **Stone Skin's own `ceil(Max VP/3)` Committed VP plus Vital Shelter's full 2 Committed + 1 Spent VP**; both require their own genuine technique knowledge and applicable composite formula. **Stone Skin's termination, including unconsciousness, also terminates its attached Shelter Secondary.** If the Shelter budget empties first, only that Secondary ends; Stone Skin persists. Nothing authorizes Reactive Composite Casting, an independently detached Shelter, or a second Stone Skin Secondary.

**This Vital Shelter composite is separate from the Basic Heal composite in section A.** It has **no Basic Heal cost, no Basic Heal healing packet and no free-hand requirement inherited from Basic Heal**. Its complete combined base price is **`ceil(Max VP/3) + 2` Committed VP + `1` Spent VP** (one normal on-turn **High 20-AP Projection Action**); all of those VP must be Available at declaration/application. On a legal attempted activation the **1 ordinary Spent VP** is paid even if the whole composition is resisted; Stone Skin and Shelter Committed VP are established **only on successful application**. It contributes Stone Skin Primary HP resistance plus Vital Shelter Secondary finite Vigor prevention once, not Basic Heal's `2 × T_heal` or `2 + ceil(d6 × T_heal/6)` output.

**Example:** An L1 High Scholar with Veil Affinity +0 has Max VP **6**. The combined normal price is **2 Stone Skin Committed + 2 Shelter Committed + 1 Shelter Spent = 5 Available VP**. After successful activation from 6 Available, the character has **1 Available / 4 Committed / 1 Spent**, **Stone Skin R2** and **Shelter S4** at VC0. The Basic Heal cost, output and mandatory free hand from section A do not apply.

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
| L1 VA0 Low Priest, Prepared Stone Skin designated Chosen; no other Rite | Base ceil(2/3)=**1 Committed**, Chosen −1 minimum 1 => **1 Committed**. Normal on-turn and authored Reactive methods obey same effective cost and one-Rite cap |
| L3 VA0 Low Priest, Prepared Stone Skin designated Chosen with vacant Chosen slot | Max VP **6**, base ceil(6/3)=**2 Committed**; when this successful instance is explicitly marked Chosen it reduces to **1 Committed**. Another already-active Chosen Rite prevents discount, not ordinary casting if capacity allows |
| L3 Low Priest has another qualifying Active Rite and reacts using Stone Skin | **Illegal** to declare despite available Reaction/VP: one Active Rite cap is full; no Reaction or VP charged |
| L1 Low Priest with unprepared Stone Skin | **Not a Rite** and no normal prepared access; no Chosen discount; a new reaction is not granted merely by the universal Rite rule |
| VC −1, +0, +2, +4, +8 | R **2, 2, 2, 3, 4**, snapshotted on successful activation |
| Fire from wildfire and Fire from Conjure Flame, same Fire HP packet value | **Same Stone Skin resistance**; magical/mundane provenance irrelevant |
| Incoming ordinary weapon Physical 10, Armor 5, Penetration 3, Stone Skin R2 | Weapon Effective Armor **2**, final **6 HP** |
| Standard hard-surface fall rolls **10 Crush HP**, Armor **5**, Stone Skin R2 | **Impact Armor = floor(5/2) = 2** first; then R2 → **6 HP lost**, not 3 |
| Same standard fall with Armor 5, no resistance | **8 HP** (locked Impact Armor formula unchanged) |
| Same fall with additional independent Physical R4 and Stone Skin R2 | Impact Armor **2**, then highest resistance **4** → **4 HP**; do not sum R |
| Falling HP damage reduced to zero by Stone Skin | **Prone/landing state is still determined** by Falling v0, not automatically negated |
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
| L3 High Scholar: Stone Skin Primary + Basic Heal `Self` Secondary at legal `T_heal=2` | **One 20-AP Projection Action**; commit Stone Skin's unchanged Reserve + spend **4 VP** for Tier-2 Heal; Healing Secondary **`2 + ceil(d6×2/6)+VC` Vigor + 1 HP** once, not 2 VP at T2 |
| L5 High Scholar: Stone Skin Primary + Basic Heal `Self` Secondary, `T_heal=3`, VA0, VC0 | Tier 3 is legal at L5: Max VP **30**, Stone Skin reserves **10 Committed**, Basic Heal spends **6 VP**, one High **20-AP Projection Action**; secondary restores **3–5 Vigor + 1 HP** once, not capped at T2 |
| L7 High Scholar: Stone Skin Primary + Basic Heal `Self` Secondary, `T_heal=4`, VA0, VC0 | Tier 4 is legal at L7: Max VP **42**, Stone Skin reserves **14 Committed**, Basic Heal spends **8 VP**; secondary restores **3–6 Vigor + 1 HP** once; Stone Skin's own HP resistance unchanged |
| L17 High Scholar: Stone Skin Primary + Basic Heal `Self` Secondary, `T_heal=9`, VA0, VC0 | Tier 9 is legal at L17: Max VP **102**, Stone Skin reserves **34 Committed**, Basic Heal spends **18 VP**; secondary restores **4–11 Vigor + 1 HP** once; no tier-upscaled Stone Skin resistance |
| L5 High Scholar tries Stone Skin + Basic Heal with `T_heal=4` | Illegal level-ceiling violation; L5 maximum is **T3**, and the composite cannot override it |
| L1 High Scholar: Stone Skin Primary + Vital Shelter maintained `Self` Secondary, VC0 | **One 20-AP Projection Action**; **4 Committed + 1 Spent VP**, Stone Skin **R2 HP resistance** and Shelter **S4 Vigor prevention**; no Basic Heal cost, healing, or hand component |
| Stone Skin + Vital Shelter composite interrupted before magical application | **One Projection Action lost**, no VP Spent/Committed; no partial Stone Skin or Secondary Shelter |
| Vital Shelter Secondary on Stone Skin host ends or depletes | Host termination ends both protections, returning their still-Committed VP; Secondary depletion first ends **only Shelter** and returns its 2 Committed VP; never creates/replenishes a new Shelter |
| Legal High Scholar `Self` composite, Stone Skin Primary + Basic Heal Secondary, both T1 | Requires **one functioning available hand** for Basic Heal; one High **20-AP** Projection Action; Reserve **ceil(Max VP/3)** plus Spend **2 VP**, heal once |
| Level-1 High Scholar Max VP 6 composite, starts 6 Available | At activation **2 Committed / 2 Spent / 2 Available**, heal once |
| Same composite maintains Stone Skin several rounds | Basic Heal's Secondary **never repeats**; ending Stone Skin returns only Committed VP |
| Stone Skin technique known but no Archetype authorization to use it | No cast; document does not grant automatic repertoire |

## Explicit Medium and Low Scholar compatibility (alternative Tier-1 modes)

The [Scholar-specific profile addendum](scholar-inward-embodiment-profiles-v0.md) expressly authors `MS-STONE-BODY-T1` (**Medium** Self Inward Body, **24 AP + 1 Committed VP**, HP R1 of original eligible Physical/Fire/Electrical types) and `LS-STONE-BODY-T1` (**Low** prepared Self Embodiment, **30 AP + ceil(Max VP/3) Committed VP**, original snapshotted Stone Skin R). Low L3 can Intensify the active host for **1 Spent VP**, receiving **+1 R until next own turn**, not a reactive extra spell.

Neither is automatic from the ordinary `Self` [Projection] tag; neither alters original Stone Skin's native reactive cast, High Scholar composite or named-effect nonstacking. Their early [profile/AP/VP model](../../design/b05-scholar-inward-embodiment-profiles-v0.md) does not yet constitute G3/G4 native Medium/Low Scholar combat certification.

## Status

**v0 design lock:** separate **normal Projection Action** and **standalone Reaction** activation methods, with **no reactive AP debt**; one-third-Max-VP Committed Reserve, maintained until unconsciousness/release; type-based Physical/Fire/Electrical **HP resistance** independent of damage source; **highest applicable resistance once per HP packet**, while worn Armor remains separate; `Self` Primary, no Stone Skin Secondary/Rider, and on-turn High Scholar Stone Skin Primary + `Self` Basic Heal Secondary resolved once. Numerical balance, damage-type coverage and higher-tier utility remain **provisional**. B05 remains open pending enough Pillar/Aspect and Archetype repertoire to play all twelve MVP builds.
