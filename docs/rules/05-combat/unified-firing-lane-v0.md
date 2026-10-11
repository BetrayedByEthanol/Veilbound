# Unified Firing Lane v0 — Shooting Past Creatures

> **LOCKED procedural baseline / numerical calibration watch.** A legal ranged shot through a physically occupied firing lane uses **one highest applicable obstruction difficulty**, a **single primary attack roll with an allocated miss spectrum**, and **one conditional secondary accuracy roll** only when the selected miss threatens an unintended creature. Engagement in melee by itself is **not** Cover or an extra targeting modifier. The provisional Living Screen tiers and collateral probabilities require playtesting. Use [Cover and Line of Fire v0](cover-and-line-of-fire-v0.md), [Aim v0](aim-v0.md), [Defensive Responses](defensive-responses-and-criticals.md), and [Initiative and Round/Turn](initiative-and-round-structure.md).

## Scope and physical legality

- Apply this procedure to **direct ranged projectiles**, including projectile-delivered magical areas, when **one or more distinct creatures physically obstruct** the legal shot to a specified intended target. Being merely engaged in melee, adjacent to a target, or allied/hostile creates **no Living Screen** without actual interference in the firing lane.
- Consider the attack origin, current silhouettes/positions, height, intended firing opening, **distance order** of intervening creatures, and relevant physical cover. A creature may be an ally, enemy, or neither. **Allegiance never alters geometry or the difficulty of that creature's obstruction**; it determines where its possible collateral outcome is placed on the spectrum.
- A fully impenetrable physical obstruction that leaves **no usable direct path** makes an ordinary direct attack **illegal**, regardless of the numerical modifier, Aim, or natural 20. A completely physically blocked path cannot become legal merely because the numerical face allocation omits a screen. Existing attack-commitment and timing rules determine what happens if a legal shot becomes illegal before resolution.
- If **no intervening creature** obstructs, use **Cover and Line of Fire v0 unchanged**, including its one-roll cover-hit window. The mixed-obstruction face allocation below supersedes that window **only for a legal shot with at least one effective Living Screen**; this is not a retroactive revision of cover-only shots.
- A projectile normally strikes **at most one creature directly**. Penetration, ricochet, multi-hit traits, special trajectories, and post-impact areas require their own authored rules.

## Effective obstruction difficulty — take the highest, do not sum

Determine each independently applicable **Living Screen source `L_i`** from how much that specific creature obstructs the intended firing corridor. Use the established exposure-style steps provisionally:

| Living Screen exposure | Provisional source difficulty `L_i` |
|---|---:|
| No meaningful overlap with firing corridor | +0 (not a screen) |
| Light obstruction | +2 |
| Half-like obstruction | +4 |
| Major obstruction | +6 |
| Narrow available opening around the creature | +8 |
| No physically usable direct path | Illegal direct shot, not +8 |

Determine the **single effective physical Cover source `C`** for the intended firing corridor under Cover v0; ordinary stone/wood/terrain Cover retains its own +0/+2/+4/+6/+8 ladder. Where several pieces of solid cover overlap, use Cover v0's single effective opening, **not their sum**. Independent Range Difficulty, valid Size/Position conditions, and Dodge Pressure remain in their existing calculations; avoid counting the same exposed-profile restriction again under a different name.

For this shot, after any valid, **single-source Aim mitigation**, calculate:

```text
P = max(C, L_1, L_2, ... L_n)
B = selected intended-target Defense excluding only this shot's P
D = B + P
```

**P is one external obstruction modifier**, never `C + sum(L_i)`. Add it once to the selected static Ranged Defense or active Ranged Dodge. For an independently legal projectile Guard, apply the obstruction as one external condition to Guard Defense as Cover v0 permits, but **do not insert Range Difficulty** into Guard unless another rule independently authorizes it. No new Guard capacity, automatic Dodge, Reaction, or Guard eligibility is created.

Each **residual** source still matters for **miss-face allocation**, even if a different source establishes the maximum `P`. For example, `C = 4` and an enemy `L = 6` gives **+6** to the intended target's Defense, while the barrier still reserves **four upper miss faces**. This is one trajectory-allocation procedure, **not ten Defense points**.

## Before rolling: declare and allocate

1. **Commit shot and responses.** Declare the intended target, attack profile, applicable Aim/otherwise legal Called Shot choices, and the actual lane. The intended defender chooses its existing legal Take Hit, Dodge, or Guard response **before the primary die** according to [Defense assignment](defensive-responses-and-criticals.md#declaring-defense). Identify possible collateral creatures and allow each **aware** creature to **predeclare a conditional personal defense** (Take Hit/static Ranged Defense, legal Dodge, or legal projectile Guard) **before the dice**, not after observing an outcome. Unaware creatures cannot spontaneously select active defense based on an unseen shot; apply their ordinary legal passive defense.
2. **Calculate `B`, the residual `C` and each `L_i`, `P`, and `D`.** Determine the **available failed natural-d20 faces**: the natural rolls **2 through 19** for which this primary Attack total would **not beat `D`** under the chosen response. Natural **1** remains an automatic miss with **no incidental collision**; natural **20** remains under the existing critical/confirmation rules and is never assigned as a stray face. If another existing special roll rule applies, resolve it before allocating a miss.
3. **Cover at the top:** starting with the **highest available failed face**, reserve as many faces as the **residual Cover Difficulty `C`**, up to the number actually available. They represent impact with the physically blocking cover, even if a Living Screen supplies a **higher** `P`.
4. **Allies at the bottom:** starting with the **lowest remaining face** (at least natural **2**), assign each physically eligible allied Living Screen up to its residual `L_i` faces, ordered **nearest ally to the archer first**.
5. **Enemies at the upper end:** starting with the **highest remaining face below the cover band**, assign each physically eligible enemy Living Screen up to its residual `L_i` faces, ordered **nearest enemy to the archer first**. Their bands grow **downward**, while allied bands grow **upward**. For neutral creatures, the GM declares which collateral-risk side they occupy **before** the roll based on the shooter's perceived stakes; their physical `L_i` is unchanged.
6. **Do not overlap or invent faces.** Each face has **at most one** destination. A later creature gets only the still-unclaimed faces, possibly **fewer than `L_i` or zero**. Unallocated failed faces remain ordinary misses. If the low and high allocation fronts meet, previously allocated faces stay assigned; the algorithm's cover → allied screens → enemy screens precedence determines the remaining space. A zero-face creature cannot be accidentally struck by this shot's standard procedure, even though the physically blocked-path gate still applies.

Allocate the faces **once before rolling**, using the actual current lane. Do not move faces after seeing a roll, reinterpret an ally as an enemy, or take another full attack against each screen. For a longer sequence, recompute only when the actual geometry, response, selected target, or applicable modifiers change.

## Resolve the primary and conditional secondary roll

1. Roll **one primary d20** and calculate the attack's normal **Attack total `A`** against intended-target `D`. Respect existing natural-1 and natural-20 precedence. If this is a legal **hit on the intended target**, resolve that one hit normally; **do not** apply any stray-face allocation.
2. On an ordinary primary miss, consult that natural face's **preallocated destination**:
   - **Cover face:** the projectile **strikes the actual barrier surface**; apply the authored Cover v0 impact/area priority, **not** ordinary miss scatter.
   - **Creature face:** the projectile **threatens that single creature**. Make **one conditional secondary d20 accuracy check** against the creature's **own selected legal ranged Defense**. The secondary check uses the weapon's normal, relevant Attack contributions and the **actual distance and conditions to that unintended creature**, not the intended target's Living Screen/Cover bonus, target-specific Aim, or target-specific Called Shot improvement. The collateral creature can use its predeclared personal Dodge or projectile-capable Guard where legal. An awareness warning does not grant a free Dodge or free movement.
   - **Unallocated face:** ordinary miss **unless the intended defender's legal, committed projectile Guard stops the projectile under its ordinary pre-obstruction instrument defense**; in that case it impacts the Guard instrument instead of scattering. Otherwise handle ordinary projectile-area Miss Impact Point scatter when applicable. An automatic natural 1 remains an automatic miss, not a mandatory Guard-instrument impact.
3. If the **secondary check beats the collateral creature's Defense**, it is the projectile's **one direct creature hit**; apply normal damage/riders that actually transfer from the projectile. If the secondary accuracy **fails against a legal projectile Guard**, that Guard instead **intercepts at its actual instrument** (including any carried surface-triggered area). On a failed check against passive Defense or Dodge, the projectile **misses that creature and intended target**, with ordinary miss-area scatter as applicable; **never** chain additional collision checks down the lane. A failed secondary check **does not substitute its own attack total** for the already-rolled primary shot when determining miss scatter.
4. The secondary d20 is a **conditional accuracy check for the same projectile**, **not** a second Attack action, Attack Sequence, projectile, AP/VP payment, ammunition use, or independent critical opportunity. For this baseline, its **natural 1 fails** and **its numerical total must beat the accidental target's Defense**; a secondary natural 20 does not separately create a critical/automatic-hit event. The natural-20/Strong Hit treatment of accidental hits is a **later calibration point**. The primary natural-20 rules remain unchanged.
5. **Resources and timing:** Collateral defenses are declared conditionally **before the primary attack roll**; a collateral creature spends Guard capacity or incurs its next Dodge Pressure **only if its face is actually selected and it resolves that defense**. The intended target spends its committed normal defense resources under existing rules. Losing an already committed instrument follows the existing defense-fallback rule; no one gets a late decision after seeing either die.
6. On an **ordinary miss** that strikes neither barrier, **either Guard instrument**, nor creature, a projectile-delivered area follows the [Manifestation miss scatter](../07-veil-magic/manifestation-resolution.md#projectile-delivered-areas). **Always use the original primary Attack total `A_primary`** (the roll against the intended target) for `Miss Margin = max(0, B - A_primary)`, where **`Scatter Defense = B` excludes only the effective unified obstruction `P`**, not other valid modifiers. This is **also true when a creature face selected a secondary accuracy check that failed** against static Defense or Dodge: **do not use `A_secondary`**, which tests only incidental collision. Roll the usual scatter direction/distance from the **original intended impact point**. An area carried by a projectile that strikes a creature/cover/shield originates at that **real impact point** under its effect's normal rules. Ordinary missing projectiles do not gain invented random creature hits.

**Physical order still controls real reachability:** a selected obstruction must actually be accessible to that trajectory. Shield, barrier, and creature results are not licenses to phase a projectile through a fully blocking nearer obstacle. A legally intervening protective shield/Take Hit action, if separately authorized, resolves in its proper response timing and can alter the effective lane before the attack. This baseline does not create a new free protective action.

## Personal avoidance, warnings, and deliberate protective Intervene

- **Personal defense:** an aware incidental target may **Dodge to protect itself**, or use an eligible shield/other projectile-capable **Guard**, with all existing defense legality and costs. Lack of awareness means no newly granted active defense; facing away is evidence about awareness, not a universal automatic penalty. An archer may give a timely audible warning before responses; it can alert allies **and enemies**, but is not automatic communication, MP, Dodge, or a new Reaction.
- **Ducking behind cover:** only a **legal** positioning/posture/movement response that **actually changes the exposed silhouette before resolution** changes `C`, eligibility, or the lane. Ordinary Dodge does not silently grant an extra square of movement or an automatic upgrade to full cover; a physically completed move into complete cover can invalidate the direct shot.
- **Protective Intervene for another:** a deliberately guarding creature may protect another by an **otherwise legal shield Guard/Intercept** or **deliberately Take Hit**, with physical placement and proper response timing. **Dodge never redirects another creature's attack to protect someone else.** This distinction does **not** grant a free new Take Hit Interception trigger, action cost, or extra Guard use; those exact protective-intervention authorizations remain a separate maneuver/timing pass.
- **Other self-defense does not protect a third party automatically.** A creature's ordinary Dodge may make its own position safer or change actual exposure; it does not act as an attack redirection on behalf of the backliner.

## Aim, Called Shots, and other precision

- A prepared [Aim v0](aim-v0.md) may choose **one** actual positive source: **a specified Living Screen `L_i`**, **physical Cover `C`**, or independently applicable Range Difficulty. Apply its usual mitigation `min(4, source)` to **that source only**, recalculate `P` and the preassigned bands, and never invent a general +4 Attack or automatic safe-shot guarantee.
- Aiming at an **ally's** screen can remove/reduce that ally's low-end collateral faces, **even when a different screen or cover remains the maximum `P`**. Aiming at Cover removes/reduces the upper cover band. Aiming at Range changes the ordinary relevant Defense component in `B` and may change which natural faces miss, but leaves unrelated screen widths untouched.
- **Called Shot** location difficulty, AP/Full Action cost, wounds, and interruption effects remain **unauthored**. Any later *independently legal* Called Shot keeps its own costs and location legality; neither a named body part nor Aim permits targeting through fully blocked geometry or erases unselected collateral sources.
- **Careful Shot** as a separate immediate Attack penalty/safety tradeoff has **no locked numerical implementation** yet. Do not silently assign a -4 Attack, collateral immunity, or extra defense roll. Aim is the current authored precision preparation.

## Worked firing lane: ally → enemy → Half Cover → mage

An archer (`Attack = d20 + 6`) shoots past a friendly swordsman (`L_ally = 2`), then an enemy knight (`L_enemy = 6`), toward a mage whose base selected Defense is `B = 16` behind **Half Cover** (`C = 4`).

```text
P = max(2, 6, 4) = 6    (NOT +12)
D = B + P = 22
Hit mage numerically on natural 17–19; natural 20 uses its existing special rule.
Failed allocatable natural faces: 2–16
```

| Natural primary face | Outcome |
|---|---|
| **1** | Automatic miss; no incidental collision |
| **2–3** | Allied swordsman **potentially** struck; check secondary accuracy against ally's actual Defense |
| **4–6** | Ordinary miss |
| **7–12** | Enemy knight **potentially** struck; check secondary accuracy against knight's actual Defense; on failed secondary accuracy without Guard, scatter uses the **primary** Attack total |
| **13–16** | Projectile contacts **Half Cover**, even though `P = 6` comes from the knight |
| **17–19** | Direct hit on intended mage, absent other rules |
| **20** | Existing natural-20/critical handling |

With a secondary `d20 + 6` and static Ranged Defense **12** for the ally, primary faces 2–3 cause **10% exposure** times a **70% secondary numerical hit chance** = **7% overall incidental ally-hit chance**. With knight Defense **14**, faces 7–12 give 30% exposure times 60% = **18% accidental enemy-hit chance**. These are playtest examples, not fixed balance targets. Their own legal Dodge/Guard, armor and actual geometry still matter.

**Different geometry:** an ally standing *beside*, not **in**, the shot does not become a screen. If the mage fully ducks behind solid cover through an already legal response **before** firing, recheck line-of-fire legality rather than assigning cover faces for an impossible target. If cover contributes +4 and a living screen contributes +6, the target gets **+6**, while the **top four** available miss faces are still **cover hits**.

## Boundaries and calibration watch

**LOCKED procedural structure:** actual-lane legal target gate; melee engagement alone not a penalty; highest effective obstruction `P` only; single highest physical Cover source plus one source per genuinely intervening creature; allied low/natural-2-up and enemy high/below-cover/down allocation (nearest first within side); no overlapping or invented faces; primary Attack determines intended hit or collateral destination; a secondary roll only for the **one** selected incidental creature; individual defenses matter; shield Guard/body Take Hit—but not Dodge—as prospective **protective** Intervene methods; Aim only one selected source; cover-only procedure unchanged.

**PROVISIONAL/calibration:** numerical +2/+4/+6/+8 Living Screen exposure values, how crowded geometries receive each exposure tier, face widths/probabilities at accuracy extremes, allocation ordering when many mixed-allegiance screens compete, secondary-check natural-20/critical treatment, warnings and awareness edge cases, conditional defense resource timing, an explicit protective **Take Hit** authorization/cost, special projectile profiles, cover-seeking posture responses, and any future Careful Shot penalty. No extra Called Shot, cover penetration, or concealment rule is smuggled in here.
