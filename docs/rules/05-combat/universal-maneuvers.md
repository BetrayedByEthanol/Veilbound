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

### Shove against a Grapple partner

A creature may attempt to Shove the other participant in its current Grappling State if the current hold and available body position make that Shove physically possible.

Because the two creatures are already in secured bodily contact, this Shove does **not** create a new Close-Contact Opportunity between those two participants.

Resolve the Shove contest normally.

If the Shove produces the normal one-square displacement:

- the Grappling State ends immediately when that displacement breaks the existing hold;
- any Pin or Control dependent on that Grappling State ends with it;
- the Shove attacker **does not** take the normal built-in advance into the defender's former square.

The attacker remains in its own square. This makes the maneuver a break-contact Shove rather than movement of the Grappling pair.

If the Shove fails, or if the displacement is completely prevented by the blocked-displacement rules, the Grappling State is not ended merely by the attempt.

Shove cannot therefore be used to move both participants together while preserving Grappling State. Moving an intact Grappling pair remains reserved for the future **Drive / Drag** procedure.

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
- Trip, Disarm, Feint, Charge, or other universal maneuvers beyond the locked Grapple v0 foundation;
- Catch Grip and falling damage.

Those remain explicit later design work.


# Grapple v0

**Grapple** is a persistent close-contact physical state between two creatures. It represents an established bodily clinch, hold, or wrestling engagement rather than a one-sided condition simply applied to one target.

A Grappling State has one of two control positions:

- **Neutral** — both creatures are engaged, but neither currently has superior control;
- **Controlled** — one creature is the **Controller** and the other is the **Controlled** creature.

Control describes positional advantage **inside the grapple**. It does not make the Controller safe from other enemies and does not make the Controlled creature helpless.

## Initiating a Grapple

Initiating a Grapple costs **one Physical Action** and requires:

- an adjacent target;
- a physically plausible way to establish bodily contact;
- enough usable limbs, body position, or anatomy to maintain that contact;
- **neither the initiator nor the target is already participating in another Grappling State**.

Ordinary weapon reach alone is not enough. A Grapple represents entering bodily contact rather than merely extending a weapon through fighting measure.

A creature already in a Grappling State cannot start a second ordinary Grapple and cannot be selected as the target of a second ordinary Grapple. The existing Grappling State must first end. When a third creature is trying to free or replace a Controller in an existing controlled grapple, use **Grapple Intervention** instead. Neutral multi-creature dogpiles and other overlapping Grappling States remain outside Grapple v0.

### Close-contact entry

If the target currently threatens the initiator, declaring the Grapple creates the same **Close-Contact Opportunity** used by Shove before the Grapple Contest resolves.

Resolve that Opportunity normally.

If the resulting Opportunity Attack **hits**, the initiator suffers:

```text
-2 to this Grapple Contest
```

The attack otherwise applies its normal damage and consequences.

A hit does not automatically Interrupt the Grapple attempt. After the response resolves, recheck whether establishing the Grapple remains physically possible.

Once two creatures are already in the same Grappling State, actions that merely contest or exploit that existing grapple do **not** create another Close-Contact Opportunity between those two creatures merely for remaining in bodily contact.

## Grapple Contest

When a Grapple rule calls for a **Grapple Contest**, each participant rolls:

```text
Grapple Contest =
d20
+ Strength or Agility
+ applicable Training
+ situational modifiers
```

Each participant uses **Strength** or **Agility** according to the actual method being used in that contest:

- **Strength** for overpowering, driving, wrenching, or forcefully maintaining control;
- **Agility** for leverage, body positioning, slipping a hold, turning an entry, or technical positional control.

A participant may not choose an Ability that the described method cannot plausibly use.

A narrow relevant Training applies normally. Veilbound does not create a mandatory broad Athletics skill for Grappling.

### Unable to contest

A Grapple Contest represents **active physical opposition**. A creature that is unconscious or otherwise physically incapable of making any plausible active Grapple response does **not** roll a Grapple Contest.

When a Grapple Contest is required:

- if exactly one participant is capable of actively contesting, that participant **wins the Grapple Contest automatically**;
- if neither participant is capable of actively contesting, no opposed Grapple Contest can be resolved and an action that requires winning that contest cannot establish a new result;
- an explicit effect may state that a creature remains capable of contesting despite otherwise restricted actions.

This rule does not make an impossible physical interaction possible. The acting creature must still satisfy the maneuver's normal contact, anatomy, position, and capability requirements.

For Grapple initiation, an incapable target therefore cannot roll high enough to become Controller: if the initiator remains capable of completing the Grapple after all responses, the initiator wins the initiation contest automatically.

### Initiation result

Compare the two Grapple Contest totals:

- **initiator wins** → both creatures enter Grappling State; the initiator is Controller and the defender is Controlled;
- **defender wins** → both creatures enter Grappling State; the defender is Controller and the initiator is Controlled;
- **exact tie** → both creatures enter Grappling State in **Neutral** control.

There is no generic "close enough" tie band. Only an actual tied total produces Neutral through this rule.

This means entering a Grapple is a commitment: an opponent who wins the entry contest may immediately turn that contact into their own controlling position.

## Position on the grid

Entering Grappling State does not merge the creatures into one occupied square.

Both creatures remain in their actual grid positions unless another rule moves them.

While Grappling:

- neither creature may use ordinary voluntary movement simply to increase distance from the other while the Grappling State persists;
- a Controlled creature cannot simply walk out of the grapple;
- the Controller cannot ordinary-move away while simultaneously claiming to maintain the grapple;
- moving the grapple as a pair requires a future **Drive / Drag** procedure rather than ordinary movement.

The Grappling State requires continued plausible bodily contact between its participants.

If an effect, forced movement, teleportation, fall, displacement, or other event places the participants so that the physical contact required to maintain the grapple no longer exists, the **Grappling State ends immediately**.

This automatic end does not require an Escape action or contest. Any Pin or other control dependent on that Grappling State ends with it.

Voluntary release, Escape, or another explicit effect may also end the state.

## Control and available actions

Control grants permission to attempt stronger grapple actions. It does **not** automatically apply every possible wrestling consequence.

A Controller does not automatically:

- knock the target Prone;
- Pin the target;
- drag the target;
- disarm the target;
- prevent all attacks or magic;
- make attacks against the target automatically hit.

Those outcomes require their own actions or explicit effects.

### Maintaining physical control

Hands, arms, legs, or other body parts actually committed to maintaining a hold or Pin are not simultaneously available for incompatible actions.

A creature may still attack, Guard, manipulate an item, cast, or perform another action while Grappling when the required body parts and position remain physically available.

This applies to both Controller and Controlled creature.

A Grappling State requires the creature actually responsible for maintaining the hold to remain physically capable of doing so.

### Controlled Grapple maintenance

In a Controller/Controlled Grapple, the **Controller** is the creature actively maintaining Control.

If the **Controlled creature** becomes unconscious or otherwise unable to actively contest or maintain contact, the Grappling State does **not** end merely for that reason. The Controller may continue holding the creature as long as the Controller remains capable of maintaining the required physical contact.

An existing Pin may likewise continue against an incapacitated Controlled creature if the Controller still satisfies that Pin's physical requirements.

If the **Controller** becomes unconscious or otherwise incapable of actively maintaining the hold:

- any Pin maintained by that Controller ends immediately;
- that Controller loses Control;
- if the other participant is capable of maintaining contact and chooses to do so, that participant becomes the new **Controller** immediately;
- otherwise, the Grappling State ends immediately.

Changing Controller through this incapacity transition does not cost a Physical Action because the former Controller is no longer capable of opposing the hold.

### Neutral Grapple maintenance

In a Neutral Grapple, neither creature has established superior control, but both are still participating in the clinch.

If one Neutral participant becomes unconscious or otherwise incapable of actively maintaining or contesting the contact:

- if the other participant is capable of maintaining contact and chooses to do so, the capable participant becomes **Controller** immediately;
- otherwise, the Grappling State ends immediately.

If neither Neutral participant can maintain contact, the Grappling State ends immediately.

Becoming unable to contest a particular Grapple Contest does not by itself end an existing Grappling State. The state ends only when no capable creature is maintaining the required bodily contact, or when another Grapple rule explicitly ends it.

## Gain or Reverse Control

A creature in a **Neutral** Grapple may spend one Physical Action to try to **Gain Control**.

Make a Grapple Contest:

- acting creature wins → acting creature becomes Controller;
- other creature wins → other creature becomes Controller;
- tie → Grapple remains Neutral.

A **Controlled** creature may spend one Physical Action to try to **Reverse Control**.

Make a Grapple Contest:

- Controlled creature wins → any Pin maintained by the former Controller ends immediately, then Control reverses;
- Controller wins → current Control remains; an existing Pin remains only if its physical requirements are still being maintained;
- tie → any existing Pin ends immediately and Control breaks down to **Neutral**.

The Grappling State itself continues through Gain Control or Reverse Control unless another rule ends it.

## Escape

A Controlled or Neutral participant may spend one Physical Action to try to **Escape** the Grapple entirely.

Make a Grapple Contest between the escaping creature and the other participant.

- escaping creature wins → the Grappling State ends;
- other creature wins → the current control position remains unchanged;
- tie → the current control position remains unchanged.

Escape means the creature is trying to disengage rather than take the upper hand.

If both participants voluntarily cease maintaining contact, the Grappling State ends without a contest.

A Controller may also voluntarily release the Controlled creature on its own turn without spending a Physical Action unless another effect explicitly prevents release.

## Pin

A **Pin** is a stronger position established from existing Control. It remains part of the same Grappling State rather than creating a separate grapple.

Only the Controller may attempt to establish a Pin.

Attempting a Pin costs **one Physical Action** and requires a plausible way to convert the current controlling position into a more restrictive hold.

Make a Grapple Contest:

- Controller wins → the Controlled creature becomes **Pinned** under that Controller;
- tie or Controlled creature wins → the Pin is not established and the existing Control position remains unchanged.

A Pin does not include a free attack.

### Pin dependency

A Pin exists only while the **same Controller** continues to control the same creature and continues to satisfy the physical requirements of that Pin.

The Pin ends immediately if:

- Control reverses;
- Control becomes Neutral;
- the Grappling State ends;
- Grapple Intervention releases the Pinned creature or replaces the Controller;
- the Controller voluntarily releases the hold; or
- the Controller can no longer maintain the body position or committed limbs required by that Pin.

Ending a Pin does not by itself end the underlying Grappling State unless the event that ended the Pin also ends that state.

A Pinned creature:

- remains Controlled;
- cannot use ordinary voluntary movement to separate from the Controller;
- cannot use a body part that is actually trapped or committed by the Pin for an incompatible action;
- cannot normally Dodge an attack from the Controller when the Pin physically prevents the repositioning that Dodge would require;
- may still Guard, attack, use magic, or perform another action when the Pin leaves the required body parts and position physically available.

The Controller may make later attacks from the Pin using body parts or weapons that remain free. For example, a Controller maintaining a plausible Pin with body weight and one arm may be able to punch with the other arm.

The Controller cannot simultaneously claim that a hand or limb is required to maintain the Pin and use that same hand or limb for an incompatible attack or item action.

Pin does **not** mean unconscious, paralyzed, helpless, or automatically hit.

The exact catalogue of Pin configurations and any future Pin-specific bonuses to Escape, Reverse Control, or Intervention remain later calibration.

## Vulnerability to outside melee attacks

Grappling makes **both** participants more vulnerable to outside melee threats. Having Control helps inside the grapple; it does not provide general protection from a third combatant.

Against a melee attack made by a creature **outside** the Grappling State:

- ordinary Dodge is normally unavailable to either grappler because the close-contact state prevents the free repositioning assumed by ordinary Dodge;
- an explicit effect or position may permit Dodge if it genuinely provides enough movement;
- Guard remains available only with a legal Guard instrument and body parts not committed to maintaining the grapple or Pin;
- Take Hit remains available normally.

### Controlled Strike into a grapple

An outside melee attacker may make a **Controlled Strike** against one participant.

Resolve the attack normally against the chosen target.

A Controlled Strike gains no special attack bonus from the Grapple and cannot transfer to the other participant merely because it misses.

### Committed Strike into a grapple

An outside melee attacker may instead exploit the target's restricted movement with a **Committed Strike**.

The attack gains:

```text
+2 to the melee attack roll
```

Because the strike may transfer, **both grapplers assign their defense before the attack roll**:

- the declared target assigns Take Hit, Dodge, or Guard under the normal defense rules;
- the other grappler simultaneously assigns the defense they will use if the strike transfers to them;
- each assignment must be legal in the current Grappling State;
- Guard capacity, Dodge Pressure, and other defense resources are committed exactly as they are for any other assigned defense; there is no free late defense after seeing the attack roll.

If the attack fails to hit the chosen target because that target successfully uses a legal Dodge or another positional defense that causes the strike to pass through the entangled space, resolve the transfer against the defense already assigned by the other grappler.

- if the other grappler assigned **Take Hit**, the transferred melee attack hits them automatically under the normal Take Hit rule; a natural 1 cannot reach this step because natural 1 does not transfer;
- if the other grappler assigned a defense with a Defense total, compare the **same attack total** against that already-assigned defense;
- if the same attack total beats that defense, the other grappler is hit instead;
- if it does not, the attack misses both;
- a successful Guard against the original attack physically stops or redirects the strike and therefore prevents transfer;
- a natural 1 remains an automatic miss and does **not** transfer to the other grappler.

This transfer rule applies only to the authored Committed Strike into a Grapple. It is not a universal friendly-fire rule.

## Attacks between the grapplers

A participant attacking the other creature in the same Grappling State does not use the outside Committed Strike transfer rule.

The attack is legal only if the current body position and available limbs make that attack physically possible.

Close weapons, fists, knees, headbutts, daggers, or similar methods may be usable where long weapons or large swings are not. Exact weapon-by-weapon Grapple restrictions remain part of the later weapon/maneuver pass.

## Third-party Grapple Intervention

A third creature may spend one Physical Action to **Intervene** against a Controller that is Grappling an ally or another creature.

The intervener must:

- not already be participating in another Grappling State;
- be adjacent to the Controller; and
- be able to establish plausible close bodily contact.

If the Controller currently threatens the intervener, entering that contact creates the normal **Close-Contact Opportunity** before the Intervention contest. A hit applies the same **-2** modifier to the intervener's ensuing Grapple Contest.

Before rolling, the intervener chooses one objective.

### Peel Off

**Peel Off** attempts only to break the Controller's hold on the original Controlled creature.

Make a Grapple Contest between the intervener and the Controller.

- intervener wins → the original Grappling State ends; the original Controlled creature is free; the intervener and former Controller do not automatically enter Grappling State;
- Controller wins → the original Grappling State and Control remain unchanged;
- tie → the original Controlled creature is released, and the intervener and former Controller enter a new **Neutral Grappling State** with each other.

### Take Over

**Take Over** attempts to free the original Controlled creature **and** establish Control over the former Controller.

The intervener suffers:

```text
-2 to this Intervention Grapple Contest
```

Make a Grapple Contest between the intervener and the Controller.

- intervener wins → the original Controlled creature is released; the intervener and former Controller enter Grappling State with the intervener as Controller;
- Controller wins → the original Grappling State and Control remain unchanged;
- tie → the original Controlled creature is released; the intervener and former Controller enter a new **Neutral Grappling State**.

Take Over is harder than Peel Off because it asks the intervener not only to break the existing control relationship but to convert that intervention into a controlling position of their own.

## Multi-participant boundary

Grapple v0 does not model arbitrary chains of simultaneous control such as one creature controlling a second creature that simultaneously controls a third.

Ordinary Grapple initiation therefore requires both participants to be free of any existing Grappling State. Use **Grapple Intervention** when an eligible third creature is trying to break or replace an existing control relationship.

Dedicated rules for cooperative dogpiles, multiple creatures restraining one target, unusual multi-limbed creatures, and other true multi-participant Grapples remain future work.

## Deliberately unresolved Grapple layers

Grapple v0 does not yet define:

- Drive / Drag movement of a Grappling pair;
- Throw / Takedown procedures;
- Grapple-specific Disarm procedures;
- detailed limb-control or weapon-control actions;
- a catalogue of Pin configurations;
- Pin-specific numerical bonuses to Escape, Reverse Control, or Intervention;
- size-category modifiers and impossibility thresholds;
- cooperative multi-creature Grapples and dogpiles;
- weapon-by-weapon restrictions while Grappling;
- ranged attacks into a Grapple;
- creature anatomy exceptions beyond ordinary humanoid assumptions.

Those remain explicit later maneuver, equipment, creature, and calibration work.
