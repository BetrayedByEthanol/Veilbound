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

Ordinary bows and heavy crossbows are not Guard-capable weapons. A future destructive emergency-block rule may allow an unsuitable held object to be sacrificed, but that is not part of their normal weapon profiles.

## Riposte

A successful **melee Guard** creates a **Riposte Opening** against that attacker until the end of the defender's next turn.

A Riposte:

- costs the defender one **Physical Action** worth of Turn AP;
- gains **+2 to the attack roll**;
- is not a free additional attack;
- consumes the opening after one attack;
- is an explicit follow-up that may target the same attacker even if that attacker already received an Attack Sequence from the riposting character during the same turn.

A parrying dagger improves the Riposte attack bonus to **+3** instead of +2.

## Dual wield

The **Light** and **Medium** labels in this section are weapon-handling classes for dual wield. They are **not** the same thing as the current **Light Physical Contribution** damage category. Final weapon-class assignments remain unresolved until the weapon-family/handedness pass is completed.

At the start of the wielder's turn, choose the offensive or defensive use. The character does not gain both in the same turn.

- **Light + Light:** either gain **+1 off-hand Attack** that turn, or use the defensive off-hand framework for **+1 Guard capacity** until the start of the wielder's next turn.
- **Medium + Light:** either gain **+1 off-hand Attack with the light weapon at -2 to the attack roll**, or use the defensive off-hand framework for **+1 Guard capacity** until the start of the wielder's next turn. A parrying dagger may also provide its Riposte improvement.
- **Medium + Medium:** no baseline extra Attack or Guard. The benefit is flexibility to choose which weapon profile to use for each normal attack.

The defensive dual-wield option is the same **defensive off-hand/shield Guard-capacity framework** used above; it does not stack into a second +1 Guard-capacity bonus from the same framework. If the bonus remains active through Round Begin, the refreshed Guard capacity includes that +1 until it expires at the start of the wielder's next turn.

A granted off-hand Attack is an **ordinary on-turn attack** for Attack Sequence declaration. If used against a target, it must be declared as part of that target's Attack Sequence rather than added after that sequence resolves. It costs **no additional Turn AP** and does not increase Physical Tempo.

Dedicated dual-wield development may later expand these options.

## Magical Manifestations using ranged defense

A valid Manifestation that becomes an independent projectile or pointed beam uses the ordinary ranged-defense procedures on this page rather than Direct Veil Resistance.

- manifested projectiles use the normal thrown-projectile attack architecture;
- pointed beams use the locked double-Precision beam attack;
- area Manifestations do **not** gain a generic ranged Dodge merely because they are magical.

See [Manifestation Resolution](../07-veil-magic/manifestation-resolution.md) for the full mapping.

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

Explicit **Size/Position** modifiers that say they apply to active ranged defense are added to Ranged Dodge after this formula. In particular, the locked [Prone ranged-profile rule](special-movement-terrain-and-prone.md#ranged-attacks-against-a-prone-target) can grant +2 Position Defense to both static Ranged Defense and active Ranged Dodge.

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

A bow or crossbow may be fired while the wielder is threatened in melee, but doing so creates an **Opportunity** before the ranged attack resolves.

An eligible enemy may exploit that Opportunity through the universal **Opportunity Response** procedure in [Initiative and Round/Turn Procedure](initiative-and-round-structure.md#opportunity-framework).

This trigger has a specific stronger consequence: if the resulting Opportunity Attack hits, the provoking ranged attack is **Interrupted and lost**.

That hit-to-Interrupt clause belongs to this trigger specifically. A generic Opportunity Attack does not automatically Interrupt its provoking action.

## Heavy crossbow timing

Firing a heavy crossbow is a **Full Action**.

Reloading a heavy crossbow is also a **Full Action**.

Each is a **Full Action** and therefore requires the character's entire Turn AP allotment to remain available and consumes that entire allotment.

Dropping a held item such as a fired crossbow is normally free.

Drawing or readying another weapon costs one **General Tempo Action (24 AP)**.
