# Protective Ward v0 — Kinship / Guardian

> **Executable Tier-1 B05 technique; approved design direction, provisional level 1–3 playtest range, price and defensive effectiveness.** Protective Ward manifests a **brief magical shield beside one ally** to intercept **one specifically declared incoming physically interceptable attack**. It grants a **separately paid Reaction defense** at range, not free Guard/Dodge capacity, an attack redirect to the caster, an additional target defense assignment, or blanket prevention of harm. The canonical **Kinship / Guardian** Aspect is **External**; it protects others rather than assuming their wounds (the latter belongs to **Kinship / Sacrifice**). Technique publication does **not** grant automatic access to every Priest, Scholar, Gifted or Anointed.

See [Aspect boundaries](../../world/aspect-identities-and-boundaries.md#kinship), [Technique Structure](technique-structure-v0.md), [Technique Tiers](technique-tiers-and-expression.md), [Initiative response windows](../05-combat/initiative-and-round-structure.md#response-windows-and-nested-responses), [Protective Intervene](../05-combat/protective-intervene-v0.md), [Guard Defense](../05-combat/weapon-attack-and-guard-math.md#guard-defense), [Shield equipment](../05-combat/off-hand-and-ranged-combat.md#defensive-off-hands-and-shields), [Critical confirmation](../05-combat/defensive-responses-and-criticals.md#natural-20-and-confirmation), [Manifestation](manifestation-resolution.md), and [VP rules](volition-points.md).

## Identity and profile

| Field | Protective Ward v0 |
|---|---|
| Pillar / Aspect | **Kinship / Guardian**, canonical **External** |
| Base Tier / access | **Tier 1**, requires normal individual technique and Aspect/Archetype access; choosing Kinship or linking Trust to Guardian does not automatically teach it |
| Used Tier | **T ≥ 1** within normal tier ceiling; **no additional Tier-based scaling** in v0 |
| Exact profile | **`Other Ally — Single Incoming Attack`**, **one other allied creature**, **one specific declared incoming attack** |
| Expression | **[Projection]**, outward **brief defensive Manifestation** beside the warded ally; not Intrusion on the ally, a hostile magic contest against the attacker, or an independently targetable summoned creature |
| Contributions | **Primary only**; no Secondary or Rider contribution, no automatically authorized Reactive High Scholar Composite |
| Activation | **One spontaneous Reaction**, during the original attack's **pre-roll response window** after applicable precommitted Interceptions and nested responses; **0 Turn AP, 0 later AP Debt** |
| Cost | **Base 2 Spent VP** for a valid magical application; any expressly eligible ordinary Spent VP discount is **locked at legal declaration**, rechecked at application, then spent at the locked amount |
| Guard resource | **0 Guard uses**; **no free Shield Guard capacity** or substitution for the ward's already assigned personal defense |
| Range | **6 square-equivalents (nominally 9 m) maximum**, direct caster-to-ally separation calculated with this technique's **explicit 3D grid metric** below; **no adjacency requirement, path-distance substitution or teleportation/repositioning** |
| Sight/path | Caster must **directly perceive the protected ally**, perceive the **specific incoming threat**, and have **one unobstructed straight magical line** through open space to the ally at declaration and valid application |
| Components | **None**: no hand, held shield, weapon, somatic/verbal component, or physical shield position needed; must be conscious, perceiving the threat and able to take a legal Reaction |
| Duration / cadence | **Instant; one conditional ward check** against the named attack after valid magical activation; disappears when that attack resolves/cancels. **No ongoing Reserve, Continuous output, additional Pulse or repeat-use trigger** |
| Ward Defense | **Caster's standard-shield Guard Defense:** `10 + caster Strength + caster Agility + eligible shield-associated weapon Training + 2 + expressly applicable general Guard modifiers`; see rules below |
| Criticals | **A legal natural 20 bypasses ordinary ward stopping**. Use exactly **one** normal natural-20 confirmation against **Ward Defense**, producing **Strong / Critical / Devastating** severity on the **original ally**, never an extra ward or ally confirmation |
| Damage / other effects | **None** dealt by the technique; no healing, resistance, extra Armor, cover, movement, interruption of a whole Attack Sequence, redirect of damage to caster, or protection of unrelated attacks |

## Target acquisition, range, and eligible threats

### Protective Ward 3D range metric — local to this technique

Use the 1.5 m grid along three orthogonal coordinate axes **x, y, z**. For the caster-to-ally displacement, count absolute offsets in squares `dx = |x_ally − x_caster|`, `dy = |y_ally − y_caster|`, and `dz = |z_ally − z_caster|`. Sort them as `a ≥ b ≥ c` and calculate:

```text
Protective Ward direct 3D range (square-equivalents)
  = (a - b) × 1 + (b - c) × 1.5 + c × 2
  = a + 0.5 × b + 0.5 × c
```

This **explicitly adopts the same grid arithmetic** as [Minor Telekinesis's local 3D metric](minor-telekinesis-v0.md#three-dimensional-distance-metric--targeting-and-movement), **but defines it independently for Protective Ward**; neither spell establishes a universal distance rule for other techniques or creature flight. One-axis separation counts **1 per square**, two-axis diagonal **1.5**, three-axis diagonal **2**. **Retain half-square values**; do not round down, replace this with Euclidean distance, count only the longest axis or use walked/curved path MP. The resulting number must be **≤6** (nominally 9 m at six orthogonal square-equivalents) and **the unobstructed straight targeting line is a separate requirement**. Measure direct caster-to-ally displacement once; walls may block a numerically in-range ally. Recalculate range on valid application after intervening movement, as for other targeting requirements.

For ordinary **one-square creatures**, use the centre of their occupied grid square at their current elevation. For a creature occupying **multiple squares**, use its **single predesignated map-reference square**, selected when it is initially positioned (and changed only with its actual position), **not whichever part is nearest the caster**. To make an existing multi-square creature executable without an already recorded reference square, choose its **lowest-x occupied square; among ties lowest-y; among ties lowest-z**, before any Ward declaration. The same reference square governs this Ward's range check throughout the attempt, subject to actual relocation; **do not retarget a closer part of its body after seeing a range outcome**. This reference square is purely Protective Ward bookkeeping and does not redefine occupied area, ordinary Attack reach or targeting for other rules.

| Caster-to-ally 3D offset `(dx, dy, dz)` | Range | Eligible numerically (≤6)? |
|---|---:|---|
| `(6, 0, 0)` | 6 | **Yes** |
| `(7, 0, 0)` | 7 | **No** |
| `(4, 4, 0)` | 6 | **Yes** |
| `(5, 5, 0)` | 7.5 | **No** |
| `(4, 2, 0)` | 5 | **Yes** |
| `(0, 0, 6)` | 6 | **Yes** |
| `(4, 0, 4)` | 6 | **Yes** |
| `(3, 3, 3)` | 6 | **Yes** |
| `(4, 4, 4)` | 8 | **No** |
| `(4, 2, 2)` | 6 | **Yes** |

**Ally and range:** Choose one **other** friendly creature as the original, declared target of the triggering attack. The caster cannot use this profile on themself or on an arbitrary structure. The ally may be incapacitated or unaware of the incoming attack; the **caster** must perceive both the ally and the threat before the attack roll. **No ally consent/Direct Veil Resistance contest is needed**: the effect creates an external barrier in the attack path, rather than intruding on the ally's body or mind. Ally status does not grant sight, clairvoyance or immunity to other targeting restrictions.

**Targeting line:** At declaration and again when the magical ward would apply, the caster must have **direct perception of the actual ally**, **direct 3D distance ≤6 square-equivalents under the Protective Ward metric above**, measured between caster's occupied-square centre and the ally's occupied-square centre (or fixed multi-square reference square), and a **single straight unobstructed line through open air** from their position to some exposed part of the ally. Walls, closed doors and **solid transparent glass** block the line even where sight would otherwise be possible. Open gaps, windows and grilles are legal only when an actual unobstructed line passes through. **No curved line around corners**, distant ally sensed solely via a magical bond, or automatic target lock from a warning about the ally. This is a technique-specific targeting requirement, not a new universal line-of-effect rule.

**Threat awareness:** The caster must perceive an identifiable incoming attack before its roll, whether by observing the attacker, perceiving the weapon/projectile or receiving a timely independently credible warning. A hidden attack not perceived until after resolution cannot trigger a retroactive Ward. Knowing an ally is *generally* in danger is insufficient. The caster need not physically stand in, reach or move into the incoming attack's lane: the ward is manifested at the ally's **occupied space at the approach of that attack**, with no free movement and no requirement that the caster share the attack's physical path. This describes where the magical shield intercepts; it does **not** let the caster select an adjacent square or area impact origin.

**Eligible attacks:** One **individually declared physical strike, projectile, pointed beam or independently manifested physical attack** whose authored delivery can plausibly contact a shield-like magical barrier at the ally. Mundane and magical origin alone does not decide eligibility; the attack's physical/delivery nature does. **Melee, arrows/bolts and physical Manifestation projectiles** may qualify when their particular direct hit would be interceptable. A pointed beam can qualify only if the underlying attack actually uses the physical attack/beam-defense architecture and can meet an intervening protective surface. A magical ward cannot automatically intercept **Direct Veil Intrusion/Imposition on a person, an already-resolved hit, ambient damage, an attack lacking a physically interceptable impact, environmental hazards, or a free-form area without a separately incoming interceptable carrier**. A carried area attack may have an interceptable projectile, but intercepting that projectile **does not erase the area**.

**One attack:** Select **one** particular attack within a declared multiattack Attack Sequence. No effect on the remaining attacks, no delayed pre-declaration of a different attack, no blanket protection until next turn. The ward is **not a physical cover object or Living Screen** and does not create Cover Difficulty, line-of-fire blocking, collision faces, shield HP or a new target for ordinary attacks before its conditional block is evaluated.

## Magical Shield Guard Defense — locked v0 expression

Use the caster's **Shield Guard Ability pair Strength + Agility** and a **standard shield's +2 Guard Defense bonus**, without requiring the caster to physically hold, wear or operate a shield:

```text
Protective Ward Defense = 10 + caster Strength + caster Agility
                            + eligible shield-style effective Weapon Training
                            + 2 (virtual standard-shield Guard bonus)
                            + other expressly applicable general Guard modifiers
```

**Training:** Follow the existing **shield** Training selection, **not** the ally's own Training, the caster's best arbitrary weapon Training or a new Shield Training skill. If the caster **currently wields a legal one-handed melee weapon** that could contribute its effective Weapon Training to shield Guard, count that effective Training **once**; otherwise **+0**. This adapts the shield's ordinary 'one-handed melee weapon in the other hand' rule to the virtual shield, which has **no physical hand**. The spell does not conjure a trained weapon, make an otherwise illegal weapon legal, or enable unrelated two-handed weapon/bow Training as shield Training.

**Bonuses and constraints:** The **+2 virtual shield bonus replaces**, rather than stacks with, a buckler (+1), equipped shield (+2), large shield (+3), physical defensive off-hand bonus, two-handed leverage, or other equipment-specific shield bonus. Other **general Guard Defense modifiers** applying to the caster's **shield-style Guard** can apply to this virtual shield **only if their authored conditions are genuinely satisfied without a physical shield and their own rule does not exclude magical wards**. A modifier requiring a held shield, specific equipment, shield arm, bodily interception, weapon leverage, personal impact position or extra Guard capacity does **not** qualify merely because the virtual barrier resembles a shield. A bonus explicitly authored to affect **magical Ward Defense** also applies according to its own rule; do not import unrelated equipment reach, ordinary shield positioning, Guard capacity or riposte modifiers. **No Veil Control, Intellect, Resonance, Tier or caster Level term** is silently added to this formula. The ally's own Armor, Guard/Dodge, Cover and existing defenses remain independent and are not copied into Ward Defense.

The **caster** supplies Ward Defense, even when the ally has much higher Guard/Dodge. Compute it **at valid ward application** and retain it for this one attack including any critical confirmation; no recalculation from the ally's state. Against a non-natural-20 otherwise-successful attack compare **the original attack total** to Ward Defense: **attack total ≤ Ward Defense → intercepted**; **attack total > Ward Defense → the original ally is hit**. No second attack roll, no magical contest against the attacker and no extra VP payment or Guard use at this check.

## Exact Reaction, VP, and attack order

1. **Original declaration:** The attacker commits the particular attack and original target and appropriate profile; the ally assigns the usual **Take Hit, Dodge or Guard** according to [Attack Sequence](../05-combat/initiative-and-round-structure.md#attack-sequence). An ally's Guard resource and Dodge Pressure remain governed by that assignment; the Guardian cannot change that defense after seeing an attack roll.
2. **Earlier responses:** Resolve all matching **precommitted Interceptions and nested responses first**, then recheck that the original attack remains legal/relevant. If it has been cancelled, made impossible, or no longer targets the ally before the spontaneous-response step, **no Protective Ward Reaction/VP may be declared for that original attack**. An independently triggered new attack gets its own proper response window.
3. **Declare Ward:** At the **spontaneous pre-roll Reaction window**, choose one eligible original incoming attack and ally. Verify range, direct sight/line, threat awareness, Reaction availability, access and physically interceptable delivery. Calculate **base 2 Spent VP**, then apply any **independently eligible cost reduction**, e.g. [TAL-M03 Frugal Technique](../10-advancement/talents-level-1-5-v0.md#tal-m03--frugal-technique) **only on the Guardian's own turn**, if unused; **lock the effective cost** (minimum 1) and require **Available VP ≥ locked effective cost**. A failed legality/affordability check **cannot legally declare the Reaction** and consumes **no Reaction, VP or Talent use**. A **legal discounted declaration immediately consumes TAL-M03's once-per-own-turn use** before responses, even if the attempt ultimately fails.
4. **Commit Reaction:** Spend **one Reaction**, with **no Turn AP or future AP Debt**. This competes with the same Reaction used for Reactive Protective Intervene, Reactive Stone Skin, Reactive Blink, or activating Opportunity Response. There is **no Interception reservation mode for this technique**, no free movement, and no separate Guard use. Resolve contemporaneous valid spontaneous responses in the canonical initiative order with all nested response windows; the ward does not leapfrog a precommitted Interception.
5. **Magical application:** After intervening responses, recheck the chosen ally, original unresolved attack, its interceptability, caster consciousness, range, direct sight/path and **Available VP ≥ locked effective cost**. If the attempt became invalid or underfunded **before valid magical application**, it fails with **Reaction spent, no ward and 0 technique VP spent**; any TAL-M03 use selected at legal declaration **remains consumed**. If valid, spend **exactly the locked effective ordinary Spent VP amount** (**normally 2**, **1** for eligible Frugal Technique); the spell succeeds in placing its one conditional barrier automatically, with **no additional activation roll or willing-ally Intrusion contest**. Once magically applied, VP are **not refunded** because a later response cancels/misses the attack.
6. **Resolve the original attack:** Apply the original target's committed defense, actual attack/cover/Living Screen rules and critical procedure with **one** initial attack roll. Ordinary original miss, cover impact, incidental Living Screen impact, natural 1 or now-illegal attack → the ward makes **no extra Guard comparison** and protects nobody else; **the Reaction and VP spent on a valid magical application remain spent**. If an ordinary (non-natural-20) attack would directly hit the ally, compare that **same attack total once** to Ward Defense. A ward block means the attack physically contacts the ward **in the original ally's occupied space**, using the fixed impact anchor defined below; an unsuccessful ward check leaves the original hit on the ally with their normal Armor/resistances/wounds and relevant on-hit effects. **Do not roll or select the ward as an additional creature target.**
7. **Natural 20 — fails to stop:** A legal initial **natural 20** is an otherwise-successful attack regardless of Ward Defense; the ward **cannot stop it**, even if its static Defense would exceed the original total. Resolve **one** existing natural-20 confirmation against **Ward Defense instead of the ally's originally assigned Dodge/Guard/Take Hit confirmation**: failed confirmation → **Strong Hit** on ally; successful → **Critical Hit** on ally; confirmation natural 20 → **Devastating Critical** on ally. No confirmation against the ally *and* the ward, no second initial roll, no second hit, and no cancellation of the original natural-20 attack. Preserve the original attack's actual damage and other on-hit consequences, subject to the resulting severity and ordinary mitigation.
8. **End:** The ward vanishes after that attack's resolution or cancellation. It does not persist to another attack in the sequence, create a Shield Guard use or Riposte Opening, alter the caster's Guard capacity or Dodge Pressure, transfer the hit to the caster, or provide cover after the triggering attack.

**Protective Intervene priority/nonstacking:** A given attack may have **at most one protective interception**. An already successfully established **Prepared Protective Intervene** has priority. Otherwise use canonical **initiative-ordered spontaneous responses** to determine the first **validly committed** Protective Intervene or Protective Ward; once one is selected for that attack, the other cannot be added as another layer or declared after viewing the roll. A caster cannot use both their own Reaction techniques on the same trigger. A protector with no legal ward/Intervene cannot occupy the slot merely by proposing an illegal declaration. Normal personal Guard/Dodge and physical cover remain unaffected, and the original target receives **no extra defense reassignment**.

**Projectile area and beams — fixed impact anchor:** When Protective Ward successfully blocks an otherwise-hitting projectile, **the impact point is the original protected ally's occupied square**, exactly as the default for [successful projectile Guard](manifestation-resolution.md#successful-guard-against-an-area-projectile). **For a standard one-square ally, use that one square at its elevation**, not any adjacent/front/back square or arbitrary barrier edge. **For a multi-square ally, use the original attack's specifically declared target square within its occupied space; this must be recorded with the attack declaration, before Protective Ward is considered or the attack rolled.** If the original attack specified only the creature, the GM fixes an occupied target square **before the spontaneous Ward declaration** using the same **predesignated map-reference square** (or lowest-x/y/z fallback) as the range metric above. **Do not select or relocate the impact point after seeing the attack total, ward result, or which area coverage would be advantageous.** The ally's actual occupied-square location after all legal earlier movement/Interceptions controls; if the chosen impact square is no longer occupied or targetable, the attack's existing legality/targeting rules apply before any ward comparison, without a free new area anchor. The ward's appearance on the approach side is narrative only and does not change this fixed grid impact origin. No new scatter roll or radius shift occurs on a successful ward block.

Its carried explosion/cloud/area resolves from **this fixed occupied-space point**, and may still affect the ally (or Guardian if inside the area) under the independently authored area rules; Protective Ward provides **no immunity to the carried area**. A successfully blocked pointed beam contacts the ward for that direct hit, but **does not create a generic beam reflection, wall, area shield, or permanent obstruction**. No unapproved projectile damage to, destruction of or extra HP for the virtual shield is inferred. An ordinary non-hit that struck physical cover or a Living Screen stays with that original impact; the magical ward neither moves nor steals it.

## v0 regression and playtest matrix

| Scenario | Required result |
|---|---|
| Level-1 Guardian with technique access, High/Medium/Low Focus | **1 Reaction + base 2 Spent VP**, 0 Turn AP/next-turn debt, **no Guard capacity**; Low Focus with Veil Affinity +0 (Max VP 2) can pay once from full Available |
| Allied creature **6 3D square-equivalents** away in straight open line, attack noticed | Eligible without caster adjacency, movement, hand or physical shield; virtual barrier in ally's occupied space |
| Ally beyond **6 direct 3D square-equivalents** / behind solid glass or wall / around corner | Cannot legally declare this profile despite awareness; **no Reaction or VP spent** |
| Horizontal diagonal offset `(5,5,0)` with clear direct line | **7.5 square-equivalents**, **out of range**; no longest-axis-only or Euclidean replacement |
| Horizontal diagonal offset `(4,4,0)` with clear line | **6 square-equivalents**, numerically in range |
| Vertical-only offset `(0,0,6)` with clear line | **6 square-equivalents**, numerically in range |
| Vertical-horizontal offset `(4,0,4)` with clear line | **6 square-equivalents**, numerically in range |
| Three-axis offset `(4,2,2)` with clear line | **6 square-equivalents**, numerically in range; half-square arithmetic not rounded |
| Three-axis offset `(4,4,4)` with clear line | **8 square-equivalents**, out of range |
| Multiple occupied squares, nearest edge inside six but predesignated reference cell outside six | **Out of range**; no choosing favorable squares after range check |
| Caster sees ally but does not perceive ambush until after hit | No Reactive Ward and no retroactive rewind |
| Other creature friendly but outside caster's perceptual line | No remote bond/scrying bypass or auto warning |
| Attack declared and then cancelled by a prior Interception | No spontaneous Ward declaration on that original cancelled attack; **0 Reaction and 0 VP** |
| Caster's original legal Reaction Ward is interrupted or made invalid before application | **Reaction lost, 0 technique VP spent**, no barrier/extra defense; TAL-M03 if chosen stays used |
| Successful 2-VP magical application followed by a normal original miss | **2 Spent VP and Reaction** remain spent, no Guard check or free transfer to Guardian |
| Caster has unused own-turn TAL-M03 and 1 Available VP | Legal discounted declaration, **1-VP effective cost locked**, TAL-M03 use consumed at declaration; pay 1 at valid magical application |
| Caster has spent TAL-M03 and only 1 Available VP | Illegal cast; no Reaction/VP/Talent use |
| Own-turn discounted Reaction is disrupted before magical application | **0 technique VP spent**, Reaction lost; **TAL-M03 stays consumed** for that own turn |
| Attack total 16 would hit ally, Ward Defense 17, not natural 20 | Single original attack roll; **ward intercepts** because 16 ≤17; **no Guard use** |
| Attack total 18 would hit ally, Ward Defense 17, not natural 20 | **Ally takes original hit**; 18 >17; caster is not struck |
| Attack total 16 misses ally at original Defense 19, Ward Defense 12 | **Original miss remains miss**, no shield comparison, despite low Ward Defense |
| Caster Strength +2, Agility +1, one-handed weapon Training +2 | Ward Defense **17** = 10+2+1+2+2 |
| Caster Strength +2, Agility +1, no eligible one-handed weapon Training | Ward Defense **15** = 10+2+1+0+2 (no other qualifying Guard modifiers) |
| General +1 Guard Defense feature legally applies to caster's shield-style Guard without a held shield | Ward Defense increases by **+1**; an equipment-only Guard bonus requiring physical gear does **not** transfer |
| Caster also carries an actual large shield (+3) | Virtual shield still has **+2**, not +2+3; no extra Guard capacity |
| Caster has bow or two-handed melee weapon only | No legal shield-style off-hand weapon Training; Ward Defense uses **+0 Training**; casting itself still legal |
| Ally has its own high Shield Guard Defense or Dodge bonus | Remains its ordinary original defense only; neither ally's bonus copied into Ward Defense nor another Guard/Dodge selected |
| Normal initial natural 20, failed confirmation versus Ward Defense | Ward **cannot block**, original ally suffers **Strong Hit**, not a miss or separate second hit |
| Normal initial natural 20, confirmed | Ward **cannot block**, original ally suffers **Critical Hit** |
| Initial natural 20 + confirmation natural 20 | Ward **cannot block**, original ally suffers **Devastating Critical Hit** under ordinary wound/damage rules |
| Ally had Take Hit preassigned, attacker rolls natural 20 | **One** confirmation versus Ward Defense replaces usual Take Hit auto-Critical procedure for this protected natural-20 attack; failure still **Strong Hit** and ward fails |
| Precommitted Prepared Protective Intervene is already valid | It owns the one-protector slot; **no additional Protective Ward**, even from another caster |
| One attacker declares 3 attacks at an ally | One protective Reaction/Ward can apply to **one selected attack only**; no blanket 3-hit interception |
| Attack is direct mental Intrusion or pure non-physical status | **Not physically interceptable**, cannot trigger Ward |
| Physical Manifestation projectile would hit ally | Potentially eligible; resolve original projectile attack then conditional Ward as for mundane projectile |
| Magical area expands around ally without one interceptable carrier | Cannot Ward the whole area; no global magical resistance |
| Explosion-bearing arrow intercepted by the Ward; ally occupies one square | Projectile impacts **that ally-occupied square**, not a chosen adjacent square; explosion resolves there and **can still affect ally** |
| Large ally occupies multiple squares and attack declared a specific target square | When blocked, **use that predeclared occupied target square** as area origin; no caster/GM post-roll shift |
| Large ally has no attack target square declared | **Before Ward declaration**, fix impact target to its **predesignated reference square** (or lowest-x/y/z fallback); area uses that exact square if intercepted |
| Projectile hits cover, Living Screen, or misses before a conditional Ward block | Its original collision/scatter rule determines impact, **not** Ward's occupied-space anchor |
| Ally relocates before magical Ward application | Recheck 3D range, direct line and original attack legality; cannot use a stale position or freely choose a new impact anchor |
| Ordinary shot hits physical Cover or a Living Screen rather than ally | Protective Ward does **not** steal that shot or redirect it to caster |
| Protecting an ally does not add Guard capacity | No shield +1 capacity, no free Dodge, Riposte, additional Cover or incidental Living Screen |
| Gifted sample **Trust → Kinship / Guardian** | Grants an eligible **Aspect link**, **not** automatic technique knowledge or a free slot; independent eligible access still necessary |
| Sacrifice-style damage transference to caster | **Not** a Guardian Protective Ward permission; reserve for future Kinship / Sacrifice authoring |

## Design status and deferred boundaries

**Locked as a provisional v0 playtest profile:** Tier 1 Kinship / Guardian **`Other Ally — Single Incoming Attack` Primary**; one threatened **other ally** within **6 direct 3D square-equivalents (nominally 9 m)**, measured by this technique's explicit sorted-axis **a + 0.5b + 0.5c** metric; live sight of ally, threat awareness, straight unobstructed magical line, **one spontaneous pre-roll Reaction**, **base 2 Spent VP at valid application**, **0 Guard capacity/Turn AP/AP debt**, one virtual **standard-shield** comparison using **caster Strength + Agility + legal effective shield-associated Training + 2 + individually eligible general Guard modifiers**, conditional on the original attack otherwise hitting. **Natural-20 attack always bypasses ward stopping**, with **one confirmation against Ward Defense** setting the original ally's Strong/Critical/Devastating severity. **No extra physical movement, full-Sequence blocking, independent Dodge, self ward, Direct Veil Intrusion interception, unbounded areas, damage transfer to caster, Secondary or Rider**. Range/price/effectiveness and edge-case balancing await L1–3 playtests; this technique does not itself solve Archetype initial acquisition or the full eight-Pillar catalogue.
