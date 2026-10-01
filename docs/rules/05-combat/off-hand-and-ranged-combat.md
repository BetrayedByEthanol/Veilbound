# Off-Hand and Ranged Combat

> Canonical current playtest baseline extracted from Core Rules Audit v34.

## Defensive off-hands and shields

A defensive off-hand grants **+1 Guard capacity**. Its type determines any additional benefit.

| Setup | Extra Guard capacity | Guard Defense bonus | Special |
|---|---:|---:|---|
| Parrying dagger | +1 | +1 melee | Improved Riposte |
| Buckler | +1 | +1 | May Guard normal projectiles |
| Shield | +1 | +2 | May Guard normal projectiles |
| Large shield | +1 | +3 | May Guard normal projectiles; mobility/cumbersomeness drawback still to be finalized |
| Two-handed melee weapon | — | +1 | Leverage already reflected in weapon profile |

Shield size increases Guard Defense rather than Guard count.

Ordinary weapons do not normally Guard arrows or crossbow bolts.

## Riposte

A successful **melee Guard** creates a **Riposte Opening** against that attacker until the end of the defender's next turn.

A Riposte:

- spends one of the defender's normal Attack units;
- gains **+2 to the attack roll**;
- is not a free additional attack;
- consumes the opening after one attack.

A parrying dagger improves the Riposte attack bonus to **+3** instead of +2.

## Dual wield

At the start of the wielder's turn, choose the offensive or defensive use. The character does not gain both in the same turn.

- **Light + Light:** either gain **+1 off-hand Attack** that turn, or **+1 Guard capacity** until the next turn.
- **Medium + Light:** either gain **+1 off-hand Attack with the light weapon at -2 to the attack roll**, or **+1 Guard capacity** until the next turn. A parrying dagger may also provide its Riposte improvement.
- **Medium + Medium:** no baseline extra Attack or Guard. The benefit is flexibility to choose which weapon profile to use for each normal attack.

Dedicated dual-wield development may later expand these options.

## Static ranged defense

Unlike melee Take Hit, a normal ranged projectile does not automatically hit a target that simply does not actively evade.

Use:

```
Ranged Defense =
10 + Range Difficulty + Cover + Size/Position and other shot-condition modifiers
```

## Active ranged Dodge

An aware target may actively Dodge a ranged attack.

```
Ranged Dodge =
10 + capped Agility + Awareness + Evasion Bonus + Range Difficulty - Dodge Pressure
```

Awareness represents reading the shooter's posture, aim, and timing rather than reacting only after the projectile is already in flight.

```
Evasion Bonus = Physical Tempo - 1
```

This gives +0 / +1 / +2 / +3 / +4 / +5 at Tempo 1 / 2 / 3 / 4 / 5 / 6.

## Bow and crossbow range bands

| Range | Squares | Approx. distance | Difficulty modifier |
|---|---:|---:|---:|
| Close | 1–6 | 1.5–9 m | -2 |
| Short | 7–12 | 10.5–18 m | +0 |
| Medium | 13–30 | 19.5–45 m | +2 |
| Long | 31–60 | 46.5–90 m | +5 |
| Extreme | 61–120 | 91.5–180 m | +8 |

These are the current bow/crossbow baseline bands. Specific ranged weapons may later use different maximum ranges without changing the universal band modifiers.

## Ranged weapons while threatened

A bow or crossbow may be fired while the wielder is threatened in melee, but doing so provokes an opportunity attack **before** the ranged attack resolves.

If the provoking attack hits, the ranged attack is interrupted and lost.

The audit still lacks a complete general opportunity-attack procedure, so only this specific locked interaction is canonical here.

## Heavy crossbow timing

Firing a heavy crossbow is a **Full Action**.

Reloading a heavy crossbow is also a **Full Action**.

Each consumes the character's entire granted Attack-unit allotment for that turn regardless of Physical Tempo.

Dropping a held item such as a fired crossbow is normally free.

Drawing or readying another weapon costs **one Attack Unit**.
