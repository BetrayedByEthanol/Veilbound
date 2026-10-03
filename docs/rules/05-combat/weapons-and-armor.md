# Weapons and Armor

> Canonical current playtest baseline. Weapon attack pairings and Physical Contribution are defined in [Weapon Attack, Guard, and Physical Contribution](weapon-attack-and-guard-math.md). Reach/Brace, final armor Coverage, and rune-capacity numbers remain unresolved.

## Weapon damage

Ordinary weapon damage uses:

```
fixed weapon base + one damage die + applicable physical contribution
```

After a hit:

```
Effective Armor = max(Armor - Penetration, 0)
```

```
HP Damage = max(rolled weapon damage + applicable physical contribution - Effective Armor, 0)
```

Physical Contribution is weapon-specific:

- **None:** `0`
- **Light:** `floor(max(Strength, 0) / 2)`
- **Full:** `Strength`

See [Weapon Attack, Guard, and Physical Contribution](weapon-attack-and-guard-math.md) for the current assignment by weapon.

## Mundane weapon baseline

| Weapon | Hands | Damage | Pen | Physical contribution | Trauma | Baseline identity |
|---|---|---:|---:|---|---|---|
| Dagger | 1 | 2 + d4 | 0 | Light | Cut / Pierce | Concealable; poor against armor; strong gap/called-shot tool |
| Rapier | 1 | 2 + d6 | 2 | Light | Pierce | Precision weapon; moderate armor interaction |
| Sword | 1 | 3 + d6 | 2 | Light | Cut / Pierce | General-purpose one-handed baseline |
| Spear | 1 or 2* | 3 + d6 | 3 | Full | Pierce | Reach/penetration-oriented |
| Axe | 1 | 3 + d8 | 2 | Full | Cut | High raw Cut trauma |
| Mace | 1 | 4 + d6 | 3 | Full | Crush | Strong anti-armor one-handed weapon |
| Greatsword | 2 | 4 + d8 | 2 | Full | Cut | Two-handed Power profile; high raw damage rather than exceptional Penetration |
| Bow | 2 | 2 + d4 | 3 | None | Pierce | Sustained ranged weapon; lower raw trauma, strong penetration |
| Heavy crossbow | 2 | 4 + d8 | 4 | None | Pierce | High-penetration opening/burst weapon with substantial reload cost |

\* The spear profile may later be split when Reach is finalized.

## Two-Handed

A weapon with **Two-Handed** requires two available hands to Attack or Guard with it **when that weapon is otherwise capable of Guarding the incoming attack**. The trait does not itself grant Guard capability.

**Ordinary bows and heavy crossbows cannot Guard.** A character threatened while holding one must use another legal defense, such as Dodge, an explicit magical/Veil defense, or Take Hit, unless a specific feature says otherwise.

- A two-handed **melee** weapon gains **+1 Guard Defense** from leverage.
- Two-Handed grants no additional Guard capacity.
- There is no universal Two-Handed damage or Penetration bonus.
- A character cannot simultaneously benefit from a shield, defensive off-hand weapon, second weapon, or another held item while Attacking or Guarding with a Two-Handed weapon.
- A character may briefly remove one hand for ordinary manipulation, but cannot Attack or Guard with the weapon until both hands are available again.

Two-handed weapon families should specialize rather than receiving the same generic bonus:

| Family | Leverage primarily becomes |
|---|---|
| Greatsword | Raw damage |
| Polehammer | Penetration / Crush |
| Long spear | Reach / Pierce |
| Greataxe | Power / Cut trauma |

## Armor

Armor provides **fixed damage reduction**.

Weapon Penetration reduces effective Armor before damage is applied.

Each armor type is primarily described by:

- **Armor** — fixed damage reduction;
- **Coverage** — body protection relevant to wounds/called shots;
- **Agility Cap** — maximum positive Agility contribution to Dodge;
- **Traits** — a small number of meaningful characteristics;
- **Rune capacity** — a later enchantment property kept separate from Armor Rating.

| Armor | Armor | Dodge Agility cap | Rune-space direction | Baseline identity |
|---|---:|---:|---|---|
| Clothing / light robes | 0 | None | High | No meaningful mundane protection; maximum mobility and strong enchantment canvas |
| Heavy padded / battle robes | 3 | +2 | Very High | Cumbersome cloth layers; weak-to-moderate protection, excellent rune space |
| Leather | 3 | +4 | Medium | Mobile light protection |
| Reinforced leather | 4 | +3 | Medium | Stronger mobile protection |
| Chain mail | 4 | +3 | Low | Flexible metal protection; awkward rune surface |
| Brigandine | 5 | +2 | Low-Medium | Standard serious frontline protection |
| Scale armor | 5 | +2 | Low-Medium | Standard serious frontline protection |
| Breastplate | 5 | +3 | Low | Strong torso protection with better mobility but less total coverage |
| Plate armor | 6 | +2 | Low | Heavy frontline/defender-grade protection |
| Full knightly harness | 7 | +1* | Very Low | Maximum mundane protection and coverage at substantial mobility cost |

\* +1 is the current baseline Dodge cap for a full harness.

**Armor 5** is the calibrated baseline for serious frontline protection. Armor 6–7 represents increasingly specialized heavy protection.

## Dodge Agility caps

Armor caps only the **positive Agility modifier applied to Dodge Defense**.

It does not reduce the actual Agility ability.

When Agility is positive:

```
Dodge Defense =
10 + min(Agility, Armor Agility Cap) + Awareness - Dodge Pressure
```

If Agility is 0 or negative, use the actual modifier. Armor never raises a poor Agility value to the cap.

The cap does not normally apply to weapon attacks or every Agility-based check.

## Rune capacity

Rune capacity is separate from mundane Armor Rating.

The intended tradeoff is that cloth/layered equipment can provide much more usable inscription or weaving space than chain or rigid plate, while heavier mundane armor gives stronger passive physical protection.

Exact rune-slot/capacity values are deferred to the enchantment system.
