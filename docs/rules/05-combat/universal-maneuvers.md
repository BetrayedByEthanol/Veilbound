# Universal Maneuvers

> Canonical Veilbound universal physical maneuvers. This page begins with the locked **Shove v0** procedure. Other universal maneuvers remain future work unless separately promoted.

## Shove v0

**Shove** is a universal **Physical Maneuver** representing committed whole-body force used to drive an adjacent creature out of its position.

A Shove costs **one Physical Action**.

The attacker must have a plausible method for transferring whole-body force, such as:

- shield contact;
- body or shoulder contact;
- a usable free hand combined with bodily drive;
- another method explicitly capable of Shoving.

Ordinary contact with a sword, spear, axe, or similar weapon does **not** by itself provide a full-square Shove. Weapon binds, hooks, trips, and other control techniques are separate maneuvers unless an explicit rule says otherwise.

A full-square Shove represents committed bodily displacement, not merely arm pressure applied through a weapon.

## Close-contact entry

A Shove requires the attacker to enter close bodily measure rather than merely extend a weapon through ordinary fighting distance.

The small footwork needed to enter that contact is part of the maneuver rather than an ordinary grid step. It does not spend MP by itself.

If the target currently threatens the attacker, declaring the Shove creates a **Close-Contact Opportunity** for that target before the Shove contest resolves.

Resolve that Opportunity through the normal [Opportunity Response procedure](initiative-and-round-structure.md#opportunity-framework).

If the resulting Opportunity Attack **hits**, the attacker suffers:

```text
-2 to this Shove contest
```

The attack otherwise applies its normal damage and consequences.

A hit does **not** automatically Interrupt the Shove. After the response resolves, recheck the maneuver normally. If the hit or another response makes the Shove physically impossible—for example by incapacitating, displacing, or otherwise preventing the attacker from carrying out the drive—the Shove cannot continue.

An explicit future rule that establishes an already-secured close-contact position may state that no new Close-Contact Opportunity is created.

## Shove contest

After all responses to the close-contact entry have resolved, make an opposed contest.

Attacker:

```text
Shove Pressure =
d20
+ Strength
+ applicable Training
+ Shove modifiers
```

Defender:

```text
Hold Ground =
d20
+ Strength
+ applicable Training
+ 2 Hold Ground
+ Anchoring modifiers
```

The attacker must **beat** the defender's total.

A tie means the defender holds position.

### Hold Ground +2

The defender receives **+2 Hold Ground** because maintaining an already occupied position has an inherent positional advantage over entering hostile measure and generating enough force to drive that position backward.

This modifier is part of the baseline Shove procedure.

A future effect may explicitly remove, improve, or replace Hold Ground when the defender is unusually off-balance, braced, anchored, or otherwise in a special state.

### Applicable Training

There is no mandatory broad Athletics skill.

A narrow Training contributes only when that learned expertise genuinely applies to the particular method of Shoving or resisting the Shove.

## Successful Shove

On a successful Shove:

```text
Before:
[A][D][ ]

After:
[ ][A][D]
```

- the defender is forcibly displaced **one square directly away** from the attacker;
- the attacker advances into the defender's former square;
- the defender's displacement is **forced movement**;
- the defender spends no MP;
- the defender does not create a general Movement Opportunity merely because the Shove moved them;
- the attacker's built-in advance costs no MP.

The Shove's built-in advance does **not** create a Movement Opportunity from the target being Shoved. That target's Close-Contact Opportunity already represents its chance to punish the entry.

Other enemies may still gain ordinary Movement Opportunities if the attacker's built-in advance actually causes the attacker to leave squares they threaten under the normal [Movement Opportunity](movement-foundation.md#movement-opportunities) rules.

A Shove does not inherently deal damage and does not inherently make the target Prone.

## Blocked displacement

A full-square Shove requires the target to be able to enter the destination square or position.

If a solid obstruction, another creature, or another effect completely prevents the target from being displaced into that destination:

- the full-square displacement does not occur;
- the attacker does not enter the defender's square;
- no automatic damage or Prone result occurs.

Collision, crushing, chain displacement, and impact consequences remain future physical-hazard rules.

A missing floor or other unsupported destination is not automatically a blocked destination. If the Shove carries the target beyond support, resolve the resulting falling, Traversal Disruption, Catch Grip, or other hazard through the applicable rules once those procedures exist.

## Terrain and force generation

Terrain can affect the Shove contest without automatically determining whether the defender falls Prone.

Separate the following questions:

1. **Can the attacker generate and transfer enough force to displace the target?**
2. **Can the defender anchor strongly enough to resist that displacement?**
3. **If displaced, can the defender remain stable afterward?**

### Attacker footing

Circumstances that materially affect the attacker's ability to drive forward—such as poor traction, severe slope, unstable footing, or useful bracing—may apply a **Shove modifier** to Shove Pressure.

### Defender Anchoring

**Anchoring** modifies the defender's ability to resist displacement.

Anchoring may depend on:

- traction and footing;
- slope and direction of the Shove;
- bracing against a wall, railing, structure, or other support;
- physical anchoring;
- loose, slippery, unstable, or otherwise unfavorable ground;
- another circumstance directly affecting the ability to hold ground.

Anchoring modifies **Hold Ground**. It does not by itself determine whether the defender becomes Prone after being moved.

Exact numerical Anchoring modifiers are not yet calibrated.

## Stability after displacement

A successful Shove does **not** inherently knock the target Prone.

If the resulting displacement occurs across terrain or circumstances where remaining upright is meaningfully uncertain, resolve a separate **Stability Check** after the displacement.

Use:

```text
Stability =
d20
+ Agility
+ applicable Training
+ situational modifiers
```

against the difficulty created by the actual terrain or circumstance.

On ordinary secure ground, no Stability Check is required.

Failure normally causes **Prone** when loss of balance is the relevant consequence. A specific hazard may instead cause another result appropriate to the fiction, such as sliding, losing support, beginning to fall, or becoming subject to a future Catch Grip procedure.

Exact terrain difficulties and special hazard outcomes remain future calibration.

The intended distinction is:

> **Strength determines whether the creature is displaced. Agility determines whether it remains stable afterward.**

## Equipment boundary

Shields are naturally well suited to Shoving because they provide a broad protected contact surface for transferring whole-body force.

The current Shove lock does **not** grant a universal additional Shove bonus based on shield size.

A shield already matters because:

- it is a clearly valid Shove method; and
- its existing Guard benefits can protect the attacker against the Close-Contact Opportunity.

Whether particular shields, equipment traits, creature anatomy, or later features grant additional Shove modifiers remains part of equipment and maneuver calibration.

## Deliberately unresolved

Shove v0 does not define:

- exact numerical Anchoring modifiers;
- exact Stability difficulties for specific terrain;
- collision or crushing damage;
- chain displacement into another creature;
- special shield-size Shove bonuses;
- size-category modifiers or impossibility thresholds;
- weapon bind or hook procedures;
- Grapple, Trip, Disarm, Feint, Charge, or other universal maneuvers;
- Catch Grip and falling damage.

Those remain explicit later design work.
