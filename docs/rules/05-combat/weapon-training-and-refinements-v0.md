# Weapon Training and Style Refinements v0

> **B04 design baseline:** Weapon Training is separate from Learned Disciplines. **LOCKED design choices:** weapon-family categories, melee-only half-transfer, no standalone Shield Training, category-specific refinements, and one point per directly purchased +1 rank. **PROVISIONAL v0 numerical calibration:** starting budget, +5 ceiling, level gates and development schedule. Refinement **effects** are not yet authored; do not grant imagined bonuses.

## Weapon families

A weapon uses one **Weapon Training family**, not a separate Training for every named weapon. The current mundane catalogue maps as follows:

| Weapon Training family | Current weapons |
|---|---|
| Small Blades | Dagger; parrying dagger |
| One-Handed Swords | Sword; rapier |
| Two-Handed Swords | Greatsword |
| Polearms | Spear, whether used in one or two hands |
| Axes | Axe |
| Blunt Weapons | Mace |
| Bows | Bow |
| Crossbows | Heavy crossbow |

New weapon variants should be assigned to a family when authored; that assignment does not silently define Reach, dual-wield handling class, new firing modes or other weapon statistics. **Throwing** remains the separately defined narrow Learned Discipline where an existing rule calls for it. A weapon's ordinary melee Training does not automatically grant a bonus to throwing it or authorize a thrown profile; the exact Training mapping for future thrown-weapon profiles remains to be authored.

## Investment and effective ranks

- A new character has **2 Weapon Development Points** and can invest each as +1 directly in a weapon family; normal creation maximum **+2** in one family.
- Each later directly invested +1 costs **one Weapon Development Point**; there are no escalating purchase costs.
- **Normal Weapon Training ceiling: +5 (provisional v0)**, distinct from the original +4 general Training scale. Rank names: Untrained +0, Familiar +1, Trained +2, Expert +3, Master +4, Grandmaster +5.
- Level gates are provisional v0: **+2 at creation; +3 from level 4; +4 from level 8; +5 from level 12**. These gates limit purchase/effective rank; they do not automatically grant the rank.
- **Focus and Archetype do not change** a character's Weapon Training ceiling, rate of improvement, or permission to master a weapon. Physical Tempo and Veil expression remain separate.

### Melee-only half-transfer

Familiarity with one **melee** family transfers some learned combat fundamentals to **other melee families**.

Let `H` be the character's highest **directly invested** melee-family rank and `D` the directly invested rank in the other melee family. If `D = H`, use `H`. Otherwise:

```
Effective Melee Training = min(H, D + floor(H / 2), current level rank cap)
```

- Transfer is **only between melee families**: Small Blades, One-Handed Swords, Two-Handed Swords, Polearms, Axes and Blunt Weapons.
- Bows and Crossbows are trained **independently**: no half-transfer into, out of, or between these ranged families.
- A character with no directly invested melee training has **no transferred bonus**.
- The source rank is **directly invested only**; never use an effective/transferred rank to start another transfer, stack multiple sources, or grant reciprocal extra ranks.
- Training transferred into a melee family improves the same legal Attack and instrument-based Guard checks as Training directly invested in that family, **but does not satisfy a refinement's directly invested prerequisite**.

| Highest invested melee rank | Other melee family invested +0 | Invested +1 | Invested +2 | Invested +3 |
|---:|---:|---:|---:|---:|
| +2 | +1 | +2 | +2 | — |
| +3 | +1 | +2 | +3 | +3 |
| +4 | +2 | +3 | +4 | +4 |
| +5 | +2 | +3 | +4 | +5 |

The table shows effective ranks assuming another melee family has the stated highest direct investment; equal-highest families simply use their directly invested rank. There is no additional transfer to the highest itself.

**Example:** One-Handed Swords directly +5 grants uninvested Axes effective +2; investing +1 Axes produces effective +3, +2 produces +4, and +3 produces effective +5. A character who invests exclusively in Bow +5 gains **no** melee half-transfer.

## Attack, Guard, and shield handling

For each legal weapon Attack or weapon Guard, insert **one effective Weapon Training value** for the actual weapon family into the existing two-Ability formula in [Weapon Attack and Guard Math](weapon-attack-and-guard-math.md). The weapon's normal Ability pairings, Attack Sequence, physical damage and Guard eligibility are unchanged.

**Shields and bucklers do not have a separate Training category or point tax.** When Guarding with a held shield or buckler, use the effective Weapon Training of **one currently wielded, legal one-handed melee weapon in the other hand**, if any. Its Training applies to the shield Guard formula; retain the shield's existing Guard Defense bonus, +1 Guard capacity and projectile eligibility. If there is no such wielded weapon, use **+0 Weapon Training** for shield Guard. Do not add both a shield and sword Training, use a stowed weapon's rank, or borrow a two-handed weapon's Training while holding a shield. Weapon Guard still uses the weapon's own category Training and normal projectile restrictions.

Parrying daggers are **Small Blades** and **inherit the ordinary dagger's complete weapon profile**, including Agility + Precision Attack/Guard pairings, 2 + d4 damage, Penetration 0, Light Physical Contribution, Cut/Pierce trauma and base weapon Guard bonus +0. Their already-authored defensive off-hand Guard/Riposte equipment benefits apply **only when used as that off-hand**; they are not shields, and their bonuses do not stack as a second Training. See [Weapons and Armor](weapons-and-armor.md#mundane-weapon-baseline), [Weapon Attack and Guard Math](weapon-attack-and-guard-math.md) and [Off-Hand and Ranged Combat](off-hand-and-ranged-combat.md#defensive-off-hands-and-shields).

## Category-specific Weapon Style Refinements

A **Weapon Style Refinement** is tied to **exactly one nominated weapon family** when purchased; its benefit never automatically transfers to another family. It requires the stated **directly invested** rank in its nominated family (not a rank gained through melee half-transfer).

Weapon Development Points may purchase either:

1. +1 directly invested Weapon Training in one family, subject to cap; or
2. one **separately authored** refinement for a specified family, paying its authored cost (default **1 point** when not otherwise specified).

A refinement should improve a defined application of existing maneuvers/defensive rules—e.g. Riposte, Disarm, Feint, Guard or Intervene—without becoming an unconditional Attack or Guard bonus. **No individual refinement benefits, numerical modifiers, prerequisites, duplicate/refund rules or catalogs are authored by this page.** Such purchases are unavailable until a concrete refinement is published; they are not free-floating points to invent bonuses. This remains a **B07 advancement/content dependency**, not a reason to force a dedicated player to train unrelated weapons.

## Provisional v0 Weapon Development schedule

| Level | Development points awarded | Highest purchasable rank |
|---|---:|---:|
| 1 | 2 at creation | +2 |
| 4 | +1 | +3 |
| 8 | +1 | +4 |
| 12 | +1 | +5 |
| 16 | +1 | +5 |
| 20 | +1 | +5 |

No additional points at other levels under this **provisional** schedule. Unspent points may be retained until an eligible rank or authored refinement is available. This allows a dedicated character to stay with one family rather than being compelled to diversify; full refinement catalogs and high-level rewards remain open design work.

## Calibration and deferred work

- Simulate Attack and Guard success rates with the +5 ceiling, melee transfer, shield equipment bonuses, Focus Physical Tempo and Dodge before treating rank/point schedules as final.
- Author actual category-specific refinements before using them in play.
- Author thrown-weapon training assignments, special nonhumanoid weapons and future weapon-family splits separately.
