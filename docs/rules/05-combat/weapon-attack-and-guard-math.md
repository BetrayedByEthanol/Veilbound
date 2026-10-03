# Weapon Attack, Guard, and Physical Contribution

> **LOCKED current baseline.** This page promotes the native two-Ability weapon attack model and the current Guard/physical-contribution decisions. Balance values may still be revisited through playtesting, but these rules replace the audit's unresolved placeholder for ordinary weapon attack pairings and base Guard Defense.

## Weapon attack roll

When an ordinary weapon attack requires an attack roll, use:

```
Weapon Attack =
d20
+ Attack Ability A
+ Attack Ability B
+ relevant Training
+ situational modifiers
```

One d20 resolves the attack. The two Abilities represent different physical demands of delivering the weapon accurately; they are not separate rolls.

Training improves attack quality. Physical Tempo determines attack quantity.

## Current weapon attack pairings

| Weapon | Attack Ability A | Attack Ability B |
|---|---|---|
| Dagger | Agility | Precision |
| Rapier | Agility | Precision |
| Sword | Strength | Agility |
| Spear | Agility | Precision |
| Axe | Strength | Agility |
| Mace | Strength | Agility |
| Greatsword | Strength | Agility |
| Bow | Strength | Precision |
| Heavy crossbow | Agility | Precision |

The generic **Sword** remains one current baseline family. It may later split into shorter/longer sword profiles if Reach, hand-and-a-half use, or a larger weapon catalogue makes that distinction mechanically useful.

### Bow accuracy and Strength

Strength contributes to a bow's attack pairing because drawing and controlling the bow are part of delivering the shot accurately.

For a given bow profile, however, excess Strength does **not** add direct damage or Penetration. The bow's construction/draw profile supplies that part of the weapon's baseline statistics.

Future bow families may use different Strength requirements to represent heavier draw weights. No such requirement table is locked yet.

## Universal thrown attack override

Unless a weapon explicitly states another thrown pairing, an otherwise legal thrown weapon attack uses:

```
Thrown Weapon Attack =
d20
+ Agility
+ Precision
+ relevant Training
+ situational modifiers
```

This changes only the attack Ability pairing.

It does **not** grant a thrown mode, range, or special property to a weapon that cannot otherwise be thrown.

The weapon keeps its normal physical-contribution class unless a specific thrown profile says otherwise.

## Guard Defense

When a character uses a legal weapon, shield, or other Guard-capable instrument:

```
Guard Defense =
10
+ Guard Ability A
+ Guard Ability B
+ relevant Training
+ Guard modifiers
```

An attack must **beat** Guard Defense to hit.

Guard remains limited by Guard capacity from Physical Tempo and equipment.

## Current Guard pairings

| Guard instrument | Guard Ability A | Guard Ability B | Base weapon Guard bonus |
|---|---|---|---:|
| Dagger | Agility | Precision | +0 |
| Rapier | Agility | Precision | +0 |
| Sword | Strength | Agility | +0 |
| Spear | Strength | Agility | +0 |
| Axe | Strength | Agility | +0 |
| Mace | Strength | Agility | +0 |
| Greatsword | Strength | Agility | +0 |
| Buckler / shield | Strength | Agility | +0 before shield equipment bonus |
| Bow | — | — | Cannot Guard |
| Heavy crossbow | — | — | Cannot Guard |

The current default weapon-specific Guard bonus is **+0**.

Future weapon traits may distinguish weapons that are particularly good or poor at parrying—for example, a sword or rapier may eventually gain a Guard advantage over an axe—but that differentiation is not part of the current baseline.

Existing equipment/trait modifiers remain separate:

- two-handed **melee** weapon: +1 Guard Defense from leverage;
- parrying dagger used as the defensive off-hand: +1 melee Guard Defense;
- buckler/shield/large-shield bonuses use their existing equipment values.

### Bows and crossbows

Ordinary bows and heavy crossbows cannot Guard.

A future general rule may allow a character to interpose an unsuitable held object as a destructive emergency block, potentially damaging or destroying that object. Such a desperation rule is **not** currently part of the normal Bow or Heavy Crossbow profile.

## Physical contribution to weapon damage

Accuracy and impact are separate questions.

The attack roll determines whether the weapon is delivered effectively.

After a hit, the weapon's **Physical Contribution** class determines how much the wielder's Strength changes the damage.

Three classes are used:

```
None  = 0

Light = floor(max(Strength, 0) / 2)

Full  = Strength
```

Light contribution never becomes negative.

Full contribution uses the actual Strength modifier, including negative Strength.

## Current contribution classes

| Weapon | Physical Contribution |
|---|---|
| Dagger | Light |
| Rapier | Light |
| Sword | Light |
| Spear | Full |
| Axe | Full |
| Mace | Full |
| Greatsword | Full |
| Bow | None |
| Heavy crossbow | None |

The generic Sword uses **Light** contribution for the current baseline.

A weak character choosing a Full-contribution weapon receives the normal consequence of that choice: negative Strength reduces the weapon's damage contribution.

### Crossbow

A heavy crossbow receives **no physical contribution**.

Its mechanical advantage, stored energy, base damage, and high Penetration are already represented by the weapon profile. The wielder's Strength does not increase the energy of an already prepared shot.

### Bow

A bow also receives **no direct physical contribution** for a normal shot from the same bow profile.

Strength can make that bow easier to draw and control and may later determine access to heavier-draw bow profiles, but excess Strength does not add damage or Penetration to every shot from the same bow.

## Damage procedure

For an ordinary weapon hit:

```
Rolled Weapon Damage =
fixed weapon base
+ one damage die
+ Physical Contribution
```

Then:

```
Effective Armor = max(Armor - Penetration, 0)
```

```
HP Damage = max(Rolled Weapon Damage - Effective Armor, 0)
```

Physical Contribution modifies damage, not Penetration, unless a specific weapon or feature explicitly says otherwise.

## Deliberately still unresolved

This page does not resolve:

- spell attack and spell-defense/save formulas;
- Strong Hit / Critical Hit bonus damage;
- Reach and Brace;
- complete thrown-weapon ranges/profiles;
- weapon-specific Guard traits beyond the existing current equipment modifiers;
- the exact Training taxonomy for individual weapon families;
- a destructive emergency-block rule for normally non-Guard equipment.
