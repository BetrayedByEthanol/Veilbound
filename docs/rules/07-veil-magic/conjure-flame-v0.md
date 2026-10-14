# Conjure Flame v0 — Fire / Conflagration

> **Executable technique profile with PROVISIONAL v0 playtest damage, costs, range, and VC coefficients.** It uses the already-locked [Technique Structure](technique-structure-v0.md), [tier ceiling](technique-tiers-and-expression.md), [elemental HP/resistance](elemental-damage-resistance-v0.md), [ammunition rules](../05-combat/prepared-and-spontaneous-ammunition-v0.md) and [Manifestation Resolution](manifestation-resolution.md). **Publishing a technique does not automatically teach it to a character**: apply the relevant Archetype's known/prepared/Aspect-access rules. This document does not grant all four Archetypes the technique.

## Identity, access, and common limits

| Field | Conjure Flame v0 |
|---|---|
| Pillar / canonical Aspect | **Fire / Conflagration** (not the historical working name *Combustion*) |
| Base Tier | **1**; requires valid access to this individual Pillar technique |
| Used Tier | Chosen at declaration, **T ≥ 1**, subject to normal character-level ceiling (L1–2: T1; L3–4: T2) |
| Focus | High / Medium / Low; each pays their normal AP category for the selected profile |
| Components | **Hands or Held**: a functioning available hand for a free-thrown manifestation, or the held weapon/launcher carrying a weapon/ammunition effect; requires the ability to perform the chosen action. No free-hand requirement on top of an otherwise legal two-handed bow shot. |
| Interaction | Thrown flame = independently manifested physical projectile; weapon/ammunition = ordinary weapon/carrier with magical on-hit packets |
| Damage | Separately authored **Fire HP** and **Vigor burn** packets; Fire Resistance affects only Fire HP by default |
| Veil Control v0 | **VC = max(0, Veil Control)** in each authored formula; **custom output coefficient**, **not** Standard VC × Character Level. Applied **once on each eligible hit**, with ammunition snapshots as defined below. |
| Durations | Thrown: immediate; Reserved Weapon: while channel valid; Ammunition Shot: one fired projectile |
| Extra status | **No automatic Ignite, Burning, area damage, flame spread, damage over time, lighting radius, or free attack** |

**Damage expression key:** For all profiles below, `F n` means **n Fire-type HP damage** and `V <expression>` means a **separate Vigor-damage packet**. Roll the shown die afresh **per actual eligible hit**; `ceil(dN × T / X)` rounds that single rolled-die fraction upward. `VC` is always **max(0, the applicable caster's Veil Control)**: **Thrown Flame** uses the caster at activation; **Reserved Weapon** uses the channel-maintaining caster at each eligible hit; **spontaneous Ammunition Shot** uses the caster/shooter at launch; **prepared Ammunition Shot** uses the **preparer's VC captured at successful preparation completion**, independently of the eventual shooter. Each packet is nonnegative. **Do not multiply this VC term by level or add the full standard VC packet again.** A future balance pass may author **VC per X character levels**, independently by **profile × contribution**, but no such multiplier applies in this v0.

## Profile identifiers and contribution values

**These exact identifiers are shared profile keys for Scholar Composite Casting.** The caster chooses which of two known compatible techniques is Primary and which is Secondary; both must support the **same identifier** and an authored legal composite use. Matching a general concept such as “ranged” or “one creature” is not enough. Profile matching does not override explicit restrictions.

| Profile key | Primary (normally independently executable) | Secondary (only with authorization) | Rider contribution (only with authorization) |
|---|---|---|---|
| **`Thrown Projectile`** | `F 2; V 2 + ceil(d8×T/3) + VC` | `F 1; V 2 + ceil(d6×T/6) + VC` | `V 2 + ceil(d4×T/6) + VC` |
| **`Weapon Enchantment`** | `F 2; V 1 + ceil(d6×T/4) + VC` | `F 1; V 1 + ceil(d8×T/8) + VC` | `V 1 + ceil(d6×T/8) + VC` |
| **`Ammunition Shot`** | `F 1; V 1 + ceil(d4×T/5) + VC` | `F 1; V 1 + ceil(d4×T/10) + VC` | `V ceil(d4×T/10) + VC` |

**Contribution permissions:**

- **Primary:** the three profiles below are usable individually by a character who knows/is authorized to express this technique and can pay the stated action and VP costs.
- **Secondary / Thrown Projectile:** explicitly **High Scholar Composite-compatible** when the other **known** technique has the exact **`Thrown Projectile`** key, is itself compatible, and the Scholar satisfies its prepared-pair/Formula Fluency conditions. The Primary owns the delivery, attack, range, target, and fundamental resolution; only Conjure Flame's **Secondary** effects attach if Conjure Flame was selected as Secondary. Pay **full VP for both techniques** and the Scholar's one slower composite action. **Do not halve this authored Secondary output again**.
- **Secondary / Ammunition Shot:** explicitly **High Scholar Composite-compatible** only when the other component has exact **`Ammunition Shot`** support and the **whole composition is delivered by one ordinary legal arrow/bolt attack**. The underlying bow/crossbow action remains mandatory, including a heavy crossbow's Full Action. Any incompatible activation requirements need an **express technique-specific resolution** before that pairing is playable; an integrated 0-additional-AP attachment is never a free shot. Both components charge their **full authored VP costs**.
- **Secondary / Weapon Enchantment:** recorded as a future contribution value, **not permission** to place a second caster-maintained reservation on an already reserved weapon, nor a free High Scholar weapon-composite option. Later specialization may authorize it.
- **Rider contribution:** numerical **Vigor-only** values are recorded for future independent item properties, components, gems or explicitly authored special features. **Knowing Conjure Flame is not enough to attach its Rider to a free attack**, and no permanent gem, item slot, crafting effect or additional reservation is granted by this document.
- A future authorized **item conversion** or environmental downgrade can select Secondary under its own rules, including a standalone weakened cast; this technique grants no such item or environmental effect by itself.

**Reversing roles is legal only where both profiles and permissions exist:** Conjure Flame Primary with another spell Secondary and another spell Primary with Conjure Flame Secondary are **different composites**, and both are subject to known-technique, profile, tier, action and VP constraints. A magically created rock using **`Thrown Projectile`** can potentially combine with this technique in either role; an **`Ammunition Shot`** arrow profile is not interchangeable with **`Thrown Projectile`** merely because both travel through the air.

## A. Thrown Flame — `Thrown Projectile`

| Field | Rule |
|---|---|
| Primary activation | **One Projection Action**: High **20 AP**, Medium **24 AP**, Low **30 AP** |
| VP | **2 × T Spent VP** per throw |
| Range / target | **1–3 squares (up to 4.5 m)**; one legal physical projectile path to one target, subject to cover/defenses |
| Range Difficulty | **+0 at 1, 2, or 3 squares** in both static Ranged Defense and active ranged Dodge; a target beyond 3 squares is **out of range**, not a longer-range shot |
| Attack | **d20 + Agility + Precision + Throwing Learned Discipline + applicable shot modifiers** |
| Defense | Normal manifested-projectile **ranged** defense (static defense, Dodge, eligible projectile Guard and cover); **not** a Direct Veil Resistance attack |
| Damage on qualifying hit | Primary `F 2; V 2 + ceil(d8×T/3) + VC`; use other authored contribution only when legal |
| Miss/blocked delivery | No hit-triggered Fire HP or Vigor damage |

**Range resolution:** Thrown Flame has its **own explicit +0 Range Difficulty at every legal distance (1–3 squares)**. Do **not** import the **−2 Close** band from the separate bow/crossbow range table. Add applicable cover, position, Dodge Pressure and other normal shot/defense modifiers independently. A target beyond three squares is illegal regardless of bow/crossbow range bands.

**Throwing** is the existing **Learned Discipline**, specifically authorized as applicable here, using the same two-Ability thrown procedure as an otherwise legal thrown knife. **Small Blades Weapon Training, Veil Practice and Veil Control never add to this attack roll** unless a different explicit rule says so. The attack roll is part of the paid spell activation, **not another Physical Action**. No Strength bonus is added to these technique-authored damage packets.

This is a direct-hit HP-damaging physical Attack and uses applicable natural-20/Strong/Critical rules. Any qualified additional HP critical dice apply **once to its primary Fire HP packet** (before Fire Resistance), never again to the Vigor packet.

## B. Reserved Weapon — `Weapon Enchantment`

| Field | Rule |
|---|---|
| Primary activation | **One Projection Action**: High **20 AP**, Medium **24 AP**, Low **30 AP** |
| VP | **4 × T Committed VP**, returned when the channel ends |
| Target | **One weapon the caster currently wields**; explicitly identify it on activation |
| Duration | **While the weapon channel and VP reservation remain valid**; no hit count, expiration clock or upkeep VP |
| Attack/defense | **Ordinary weapon attack and defense**, with its normal Physical Action/AP or authored attack timing |
| Damage per eligible successful hit | Weapon's own physical packet + Primary `F 2; V 1 + ceil(d6×T/4) + VC` |
| Extra per-hit cost | **0 VP, 0 spell AP**; underlying weapon attacks still cost their usual AP |

The magical packet applies on **every qualifying successful hit** by **the selected enchanted weapon**, including an otherwise eligible hit whose ordinary physical HP damage is absorbed by Armor. A different weapon, unenchanted off-hand attack, replaced projectile or mere possession of the enchanted sword does not inherit it. The v0 **Rider cadence** is **each eligible successful weapon hit**, and the numbers remain subject to multi-attack Tempo balancing.

**Channel termination:** successful [Disarm](../05-combat/disarm-v0.md), or **voluntarily dropping/handing away the selected weapon** at a legal own-turn zero-action decision point, breaks the channel immediately and **returns all Committed VP to Available**. A chosen drop is free under normal [zero-action timing](volition-points.md#zero-action-timing), **not** a free interrupt. Recovering the weapon does not reactivate it. The weapon's independent item effects do not vanish solely because this wielder-maintained Reserve ended. One wielder-maintained Primary reserved enchantment per weapon remains the default; no secondary simultaneous Reserve is authorized.

## C. Enchanted arrow/bolt — `Ammunition Shot`

**Integrated spontaneous casting:** When the caster makes an otherwise legal **bow or crossbow shot using one physical arrow or bolt**, the caster may choose Conjure Flame's Primary Ammunition Shot as a **0-additional-AP attachment** to that shot.

- Pay the normal **Physical Action** for a bow shot or **Full Action** for the heavy crossbow shot and obey ordinary range, Accuracy/Training, Aim, cover, Opportunity, Attack Sequence and reload restrictions.
- Declare Conjure Flame, Used Tier, the actual physical projectile and VP cost **before the Attack Sequence's first roll**. Ensure sufficient Available VP for all declared magical shots; **spend 2 × T VP when that projectile launches**, before its roll. **Lock the spontaneous effect's VC to the caster/shooter's max(0, VC) at launch**, not a later attack/impact value. A launched miss still costs VP; **pre-launch interruption costs the committed attack AP but not unspent spell VP**, per [ammunition timing](../05-combat/prepared-and-spontaneous-ammunition-v0.md#integrated-on-shot-activation-0-additional-ap).
- On a successful hit, add **`F 1; V 1 + ceil(d4×T/5) + VC`** (Primary) as separate on-hit packets **alongside the normal arrow/bolt physical damage**. Physical Armor/Penetration applies to the native shot; Fire Resistance applies to the Fire HP packet, and Vigor burn is separate.
- This is **one shot** and one ordinary Attack; it creates **no second spell attack, second ammunition item, bonus shot or independent Fire critical damage dice**. Strong/Critical extra HP dice apply once to the arrow/bolt's normal primary physical HP packet.

**Prepared physical ammunition:** [Prepared Ammunition v0](../05-combat/prepared-and-spontaneous-ammunition-v0.md#prepared-physical-ammunition--provisional-playtest-procedure) also authorizes the same **Primary** effect to be applied in advance:

- **10 uninterrupted minutes** for a batch of **1–20 physical arrows/bolts**; commit to one Used Tier T for that batch.
- Spend **1 × T VP per projectile** at successful completion (a **50% VP discount** relative to spontaneous Primary, not a Secondary power downgrade). At **successful preparation completion**, record **the preparer's max(0, Veil Control)** as **stored VC** on every arrow/bolt of that batch along with its **Used Tier T**. This numeric VC snapshot and Tier are fixed for the life of each enchantment, **even if the preparer later improves/loses VC or the ammunition changes hands**. **Only the damage die is rolled on a future eligible hit**; no damage dice are rolled at preparation.
- Enchantment expires **24 hours after completion** or on firing, whichever comes first. VP recovery after preparation does **not** erase it or refund its cost. Prepared projectiles can be carried by another user; their paid-for effect does not require a reservation.
- When fired, **no additional spell AP or VP** is charged for the prepaid effect, but the ordinary bow/crossbow shot still costs its native action and one physical ammunition item. **Attack/accuracy use the actual shooter's stats; the stored spell effect uses the recorded preparer's VC, never the shooter's VC**. Do not recalculate the stored VC at firing or impact. A miss consumes the attached effect.

**One major enchantment per physical projectile.** A prepared Conjure Flame arrow cannot receive another major spontaneous/prepared enchantment under v0. More elaborate stacking is deferred. **Veil Arrow** (historical Ethereal Arrow) is a future Universal candidate, **not an automatically granted, executable ammunition source** in this PR.

## Damage mitigation and mechanical boundaries

1. **Fire HP:** `max(0, raw Fire HP − Fire Resistance)`; ordinary **Armor does not reduce this explicitly elemental packet**, and physical Penetration does not improve it.
2. **Physical weapon/arrow HP:** apply the carrier's ordinary weapon damage formula, Penetration and Armor **exactly once**.
3. **Vigor burn:** an independent Vigor-damage packet; **neither Fire Resistance nor ordinary Armor** reduces it automatically. A successful hit may burn Vigor despite **0 Fire HP** or **0 carrier HP** damage; a miss does not.
4. **Critical/wounds:** one qualifying natural-20 confirmation and one primary direct-hit HP critical dice award, as specified per profile above; same-hit packets do not create multiple duplicate wounds.
5. **No area or persistent fire:** Conjure Flame's attack does not itself create a burning zone, Ignite condition, ongoing damage, scaling illumination benefit or free terrain control. Interacting with ordinary flammable objects is subject to actual material/world conditions, not a guaranteed igniting combat rider.
6. **No negative VC bonus:** negative Veil Control yields **+0**, not negative damage, and does not replace throwing/bow weapon accuracy.
7. **No invented extra resistance roll:** valid physical Manifestation and weapon-hit consequences use their authored normal defense, not a second Direct Veil contest.

## Level 1–3 v0 calibration snapshots

For **VC +0**, the following refer to **Primary Vigor damage on a successful hit**; add **max(0, VC)** when applicable. These are damage per hit, **not hit probabilities** or total encounter outcomes.

| Level | Normal max Used Tier | Thrown `2+ceil(d8×T/3)` range / mean | Reserved `1+ceil(d6×T/4)` range / mean | Ammunition `1+ceil(d4×T/5)` range / mean |
|---:|---:|---:|---:|---:|
| **1–2** | **1** | **3–5 / 3.875** | **2–3 / 2.333** | **2 / 2.000** |
| **3** | **2** | **3–8 / 5.375** | **2–4 / 3.000** | **2–3 / 2.500** |

**Caution:** Low Focus at Level 1 with Veil Affinity +0 has Max VP 2, so can afford a Tier-1 **Thrown Flame** but cannot establish the Tier-1 **4 Committed VP** Reserved Weapon enchantment. This is a VP-capacity consequence, not a new Focus prohibition. Do not treat all profiles as affordable to all characters at every level.

### Regression examples

| Case | Expected |
|---|---|
| A level-1 Throwing +2 user throws flame | `d20+Agility+Precision+2`; **no Small Blades**, Veil Practice or VC attack bonus; 1 Focus-priced Projection Action and **2 Spent VP** |
| Thrown Flame targets at 1, 2, or 3 squares | **Range Difficulty = +0** for static Defense and active Dodge; never apply the bow/crossbow Close −2 band; 4+ squares is out of range |
| A flame projectile hits Fire-Resistant target | Fire HP minus explicit Fire Resistance; Vigor packet applies independently |
| A selected Reserved sword hits three times | The defined on-hit fire/Vigor packets apply **three** times, with no per-hit VP or magic AP |
| The wielder legally drops the reserved sword | The channel ends and its **4×T Committed VP** becomes Available; no free reaction timing |
| Spontaneous bow shot with Conjure Flame | One normal paid ranged attack; **2×T VP spent on launch** even on miss; 0 extra Projection AP |
| Heavy crossbow shot with Conjure Flame | **Full Action** still required; enchantment never waives its reload Full Action |
| Physical arrow prepared for Tier 2 | 10-minute preparation; **2 Spent VP** per arrow; effect expires in 24 hours; hit uses Tier 2 values |
| VC +3 caster prepares Tier-1 arrow; VC +0 archer fires it | On a successful hit, **Primary Ammunition Vigor = 1 + ceil(d4×1/5) + 3 = 5**, not 2; archer's normal accuracy still applies |
| VC +0 caster prepares Tier-1 arrow; VC +4 archer fires it | On a successful hit, **Primary Ammunition Vigor = 2**, not 6; the shooter does not improve the prepared effect |
| Preparer's VC changes after preparing an arrow | The arrow keeps its **recorded VC**; its damage die is still rolled on the eventual qualifying hit |
| Scholar combines two matching `Thrown Projectile` techniques | Chooses Primary/Secondary; full VP for both; one slower composite action; selected Secondary value once |
| Scholar combines `Thrown Projectile` and `Ammunition Shot` | **Invalid** — exact profile mismatch |
| Scholar combines two `Ammunition Shot` techniques | One paid physical shot if the combined rules support it; full VP for **each** component; no bonus shot or second roll |
| Scholar attempts two simultaneous reserved weapon effects | **Invalid without later specialization**, even if profile labels match |
| Fire-immune creature hit by magical sword | Fire HP = 0; ordinary weapon HP and Vigor burn still resolve normally |
| Fire-only Thrown Flame qualifies as Critical | Bonus HP dice **once on its direct-hit Fire HP packet**, before resistance; no bonus to Vigor |
| Mundane weapon/arrow physical damage is entirely stopped by Armor | Successful hit still applies independent Fire and Vigor packets |

## Deliberately deferred

- Final VC-per-X-level coefficients **by profile and contribution**, numeric VP/damage/range tuning beyond this level-1–3 playtest baseline, resistance granting/stacking mechanics, and any automatic Burning/Ignition spread techniques.
- Independent enchanted gem/Rider sources, weapon-reserve specializations, conversion-item economy, permanent investment, mixed-aspect crafting, ammo pickup/recovery beyond existing combat baseline.
- Automatic technique access/repertoire counts, cross-Archetype compatibility, Veil Arrow acquisition/execution and any separate fire-control terrain effect.

The **structural and execution procedures are authored** here; **B05 remains open overall** until a sufficient eight-Pillar playable catalogue and starting access/repertoire are completed.
