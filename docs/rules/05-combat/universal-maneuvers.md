# Universal Maneuvers

> Canonical Veilbound universal physical maneuvers. This page contains the locked **Shove v0**, **Grapple v0**, **Trip/Takedown v0**, and **Drive/Drag v0** foundations. Other universal maneuvers remain future work unless separately promoted.

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

Because Grappling participants already share secured bodily contact and occupy the same Grapple square, this Shove does **not** create a new Close-Contact Opportunity between those two participants.

Before making the Shove contest, the attacker chooses **one of the 8 adjacent grid directions** from the shared Grapple square as the Shove direction.

That declared direction fixes the defender's destination if the Shove succeeds. It is also the destination used to determine whether blocked-displacement rules prevent the Shove. The attacker cannot wait to see the contest result before choosing the direction.

Resolve the Shove contest normally.

If the Shove produces the normal one-square displacement:

- the defender is displaced one square from the shared Grapple square in the declared Shove direction;
- the attacker remains in the shared Grapple square, which becomes the attacker's ordinary occupied square;
- the Grappling State ends immediately;
- any Pin or Control dependent on that Grappling State ends with it;
- the attacker does **not** take the normal built-in advance.

If the Shove fails, or if the displacement is completely prevented by the blocked-displacement rules, the Grappling State remains in the shared square.

Shove cannot be used to move both participants together while preserving Grappling State. Moving an intact Grappling pair uses **Drive / Drag** instead.

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
- Disarm, Feint, Charge, or other universal maneuvers beyond the locked Grapple v0 and Trip/Takedown v0 foundations;
- Catch Grip and falling damage.

Those remain explicit later design work.


# Trip v0

**Trip** is a universal **Physical Maneuver** used to make a standing creature lose its footing and become Prone without first establishing Grapple Control.

A Trip costs **one Physical Action**.

The attacker must have a plausible method that can actually attack the target's balance, such as:

- a foot sweep or leg reap;
- a body or shoulder action directed at the target's base;
- a shield, staff, hook, haft, or other suitable contact method;
- another method explicitly capable of Tripping.

Ordinary contact with a sword edge, spear point, axe head, or similar weapon does **not** automatically provide a Trip merely because that weapon can make an ordinary attack.

The target must be within the usable reach of the actual Trip method. A body or foot Trip normally requires close bodily measure; a suitable hooked or extended implement may work from its authored melee reach.

A creature already Prone cannot be made meaningfully more Prone by Trip.

## Close-contact Trip entry

If the chosen Trip method requires entering close bodily measure rather than operating from an already-usable weapon/contact distance, use the same **Close-Contact Opportunity** framework as Shove and Grapple.

If the target currently threatens the attacker, resolve that Opportunity before the Trip contest.

If the resulting Opportunity Attack **hits**, the attacker suffers:

```text
-2 to this Trip contest
```

The hit otherwise applies its normal damage and consequences and does not automatically Interrupt Trip. Recheck whether the Trip remains physically possible after the response.

A Trip method that operates entirely from an already-established usable melee distance does not create this additional Close-Contact Opportunity merely for making the Trip.

## Trip contest

Attacker:

```text
Trip Pressure =
d20
+ Strength or Agility
+ applicable Training
+ Trip modifiers
```

Defender:

```text
Balance Resistance =
d20
+ Strength or Agility
+ applicable Training
+ Balance modifiers
```

Each participant uses the Ability that matches the actual method:

- attacker **Strength** for forceful reaps, wrenching the base, or powering through stance;
- attacker **Agility** for timing, placement, sweeps, hooks, or technical balance attacks;
- defender **Strength** for bracing, planting, or physically resisting the off-balance force;
- defender **Agility** for stepping clear, recovering balance, or redirecting the attempt.

A participant may not choose an Ability that the described method cannot plausibly use.

A narrow relevant Training applies only when it genuinely helps the particular Trip or resistance method.

The attacker must **beat** Balance Resistance.

- attacker wins → target becomes **Prone**;
- tie → target remains standing;
- defender wins → target remains standing.

A failed Trip does not automatically Trip the attacker or otherwise reverse the maneuver.

## Unable to contest Trip

Trip resistance represents active balance, bracing, or recovery.

If the defender is unable to make any plausible active resistance:

- the defender does not roll Balance Resistance;
- the Trip succeeds automatically if the attacker still has a physically valid Trip method and the target can meaningfully become Prone.

If the target is already unsupported, falling, or otherwise in a state where Prone is not the meaningful physical result, use the applicable movement/hazard procedure instead rather than forcing the Prone state.

## Trip result

A successful Trip:

- makes the target **Prone** in its current square or position;
- does not inherently move the target to another square;
- does not inherently deal damage;
- does not establish Grappling State;
- does not give the attacker Control.

Use the existing [Prone movement rules](special-movement-terrain-and-prone.md#prone-movement-state) immediately after the result.

The non-movement attack, Guard, Dodge, targeting, and other combat consequences of Prone remain part of the later Prone-condition pass.

## Trip while already Grappling

Trip v0 is not used as a shortcut around the Grapple control structure.

A creature does not use ordinary Trip against the other participant in its current Grappling State. A Controller who wants to take the Controlled creature to the ground uses **Takedown** instead.

Controlled and Neutral participants must first change or end the Grappling State through its existing procedures before using ordinary Trip against that same creature.

## Trip calibration boundary

Trip v0 does not yet define:

- weapon-specific Trip bonuses or penalties;
- size-category modifiers or impossibility thresholds;
- special interactions with unusual anatomy;
- terrain-specific Balance modifiers;
- Prone's non-movement combat effects.

Those remain later equipment, creature, terrain, and condition calibration.

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

- **initiator wins** → Grappling State begins; both creatures occupy the defender's square; the initiator is Controller and the defender is Controlled;
- **exact tie** → Grappling State begins; both creatures occupy the defender's square in **Neutral** control;
- **defender wins** → the defender chooses **Repel** or **Counter-Control**.

**Repel** means the defender defeats the close-contact entry without accepting the clinch:

- no Grappling State begins;
- both creatures remain in their original squares;
- neither creature gains Control;
- Repel is not a Shove and causes no additional displacement or damage.

**Counter-Control** means the defender turns the committed entry into a controlling hold:

- Grappling State begins;
- both creatures occupy the defender's square;
- the defender becomes Controller and the initiator becomes Controlled.

There is no generic "close enough" tie band. Only an actual tied total produces Neutral through this rule.

The close-contact footwork of a successful initiation, Neutral result, or Counter-Control is part of the Grapple action and spends no MP.

### Grapple-entry Opportunities

When an initiation result would establish Grappling State, the initiator has not yet left its original square.

Before moving the initiator into the defender's square:

- each **third-party enemy** that threatens the initiator's current square gains one Opportunity from that Grapple-entry movement;
- resolve those Opportunities through the normal Opportunity Response procedure before the initiator changes squares;
- the Grapple target does **not** gain a second Opportunity from this entry movement, because its authored **Close-Contact Opportunity** already represents its chance to punish the entry;
- Repel creates no Grapple-entry movement and therefore no Grapple-entry Opportunity;
- if a response makes the Grapple establishment illegal or impossible, recheck the result normally before moving the initiator.

This authored entry Opportunity exists even though the footwork spends no MP and is part of the Grapple action rather than an ordinary Normal step.

### Shared Grapple square

While Grappling, both participants occupy the **same grid square**.

This is an explicit exception to the normal rule against hostile creatures sharing a square. It represents the participants abandoning ordinary fighting distance and becoming physically entangled.

While the Grappling State persists:

- both creatures are still separate creatures and separate legal targets;
- both use the shared square as their position for Reach, threatened space, targeting, terrain, area effects, and other square-based rules;
- **each participant is explicitly within the other's Melee Reach while the Grappling State persists**;
- if a participant remains capable of making a relevant melee attack, it **threatens the other participant despite sharing the same square**;
- an effect that includes the shared square can affect both creatures normally;
- neither participant may use ordinary voluntary movement to leave the shared square while preserving the Grappling State;
- a third creature cannot voluntarily enter the shared Grapple square unless an explicit rule such as Grapple Intervention permits it;
- moving the intact shared Grapple square uses **Drive / Drag** rather than ordinary movement.

The Grappling State requires continued plausible bodily contact between its participants.

If forced movement, teleportation, falling, displacement, or another effect actually places the participants in different positions so that the required physical contact no longer exists, the **Grappling State ends immediately**. Any dependent Pin or Control ends with it.

### Separation requirement

Because Grappling State is what permits two hostile creatures to share one square, a **voluntary** end to the Grapple must also produce legal separate positions.

When a rule says one participant leaves or separates:

- the participant named as leaving moves into an adjacent legal free square;
- the other participant remains in the former shared Grapple square;
- if there is no legal adjacent free square for the leaving participant, that voluntary separation cannot be completed.

A rule such as Shove, forced movement, teleportation, Dump, or Grapple Intervention may provide its own separation placement instead.

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

If the **Controlled creature** becomes unconscious or otherwise unable to actively contest or maintain contact, the Grappling State does **not** end merely for that reason. The Controller may continue holding the creature in the shared square as long as the Controller remains capable of maintaining the required physical contact.

An existing Pin may likewise continue against an incapacitated Controlled creature if the Controller still satisfies that Pin's physical requirements.

If the **Controller** becomes unconscious or otherwise incapable of actively maintaining the hold:

- any Pin maintained by that Controller ends immediately;
- that Controller loses Control;
- if the other participant is capable of maintaining contact and chooses to do so, that participant becomes the new **Controller** immediately;
- otherwise, if the other participant can legally separate into an adjacent free square and chooses to do so, that participant separates immediately and the Grappling State ends;
- if the other participant does **not** take Control and does **not** complete a legal immediate separation, the Grappling State becomes **Neutral**.

The Neutral fallback applies whether separation was impossible or merely declined. It preserves a defined control position for the shared-square state until a later legal separation, Gain Control, or other Grapple procedure changes it.

Changing Controller or taking the immediate separation through this incapacity transition does not cost a Physical Action because the former Controller is no longer capable of opposing it.

### Neutral Grapple maintenance

In a Neutral Grapple, neither creature has established superior control, but both remain physically entangled in the shared square.

If one Neutral participant becomes unconscious or otherwise incapable of actively maintaining or contesting the contact:

- if the other participant is capable of maintaining contact and chooses to do so, the capable participant becomes **Controller** immediately;
- otherwise, if the capable participant can legally separate into an adjacent free square, that participant may separate immediately and the Grappling State ends;
- if no legal separation square exists, the Grappling State remains **Neutral** because the creatures cannot yet occupy legal separate positions.

If neither Neutral participant can actively maintain contact, the state remains Neutral only as the shared-square occupancy state until an external effect, recovery, or other legal separation resolves their positions.

Becoming unable to contest a particular Grapple Contest does not by itself end an existing Grappling State.

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

Escape can be declared only if at least one adjacent legal free square is available for the escaping creature to separate into. Recheck that requirement when the Escape resolves.

Make a Grapple Contest between the escaping creature and the other participant.

- escaping creature wins → choose an adjacent legal free square; the escaping creature moves there and the Grappling State ends;
- other creature wins → the current control position remains unchanged;
- tie → the current control position remains unchanged.

The successful Escape separation is part of the Physical Action:

- it costs no additional MP;
- it is not a Normal movement step and does not create the general Movement Opportunity;
- the other Grapple participant remains in the former shared square.

If no legal separation square remains when a successful Escape would resolve, the Grappling State cannot end through that Escape.

Escape means the creature is trying to disengage rather than take the upper hand. **Reverse Control** is the separate choice to stay in the shared square and fight for dominance.

### Voluntary Controller release

A Controller may voluntarily release the Controlled creature on its own turn without spending a Physical Action, but ending the shared-square Grapple requires the Controller to separate.

To do so, the Controller must immediately make one legal ordinary movement step from the shared Grapple square into an adjacent free square:

- pay that step's normal MP cost;
- resolve terrain and movement restrictions normally;
- resolve ordinary Movement Opportunities from other threatening enemies normally;
- the former Controlled creature remains in the old shared square.

If the Controller has no legal adjacent separation square or cannot pay for the required step, it cannot voluntarily end the Grapple through this release procedure.

If both participants agree to separate, either participant may be designated as the leaving creature and use this same ordinary separation step.

## Drive / Drag v0

**Drive / Drag** is the Controller-only Grapple action used to move an intact Grappling pair while preserving the shared-square state.

The terms **Drive** and **Drag** describe the fiction of pushing, pulling, steering, or hauling the opponent. They use the same v0 procedure.

Drive / Drag costs **one Physical Action** and may be attempted only when:

- the acting creature is the current Controller;
- both participants remain in the same Grappling State;
- the Controller has a physically plausible way to move the pair;
- the intended movement uses ordinary supported-ground movement or Crawl; climbing, swimming, and other Traversal-State pair movement remain later work.

Drive / Drag v0 is an on-turn action and is not eligible to be reserved as an Interception unless a later rule explicitly permits it.

### Drive / Drag contest

Make one normal Grapple Contest.

- **Controller wins** → begin one **Drive / Drag Movement Segment**;
- **tie** → no pair movement occurs and existing Control remains;
- **Controlled creature wins** → no pair movement occurs, any Pin dependent on the former Control ends, and Control degrades to **Neutral**.

If the Controlled creature cannot actively contest, use the normal Unable to Contest rule; a capable Controller wins automatically.

Only **one Grapple Contest** is made for the Drive / Drag action. Do not roll once per square.

### Drive / Drag Movement Segment

A successful Drive / Drag action creates exactly **one movement segment** for the shared Grapple square.

During that segment:

- the Controller spends its own MP;
- the Controlled creature spends no MP;
- both participants move together and continue occupying the same shared Grapple square after every successful step;
- direction may change normally; Drive / Drag has no Sprint-style heading restriction;
- the Controller may continue taking legal steps until the segment ends.

The segment ends when:

- the Controller begins another action or effect;
- the Controller voluntarily ends Drive / Drag;
- a Movement Interception completes a legal step and breaks the segment under the normal rules;
- the Controller runs out of usable MP;
- no legal Drive / Drag step remains;
- the Grappling State ends;
- the acting creature loses Control;
- another explicit effect ends the segment.

Once the segment ends, resuming pair movement requires another Physical Action and another Drive / Drag contest.

### Drive / Drag step cost

Drive / Drag is a slow pair-movement mode.

For each step:

```text
Drive / Drag step cost
= 2 × Controller's applicable locomotion step cost
+ flat terrain/occupancy surcharges
```

Use the Controller's locomotion cost **before flat surcharges**.

Examples on ordinary ground:

| Controller state | Orthogonal | Diagonal |
|---|---:|---:|
| standing / ordinary movement | 4 MP | 6 MP |
| Prone and Crawling | 8 MP | 12 MP |

The Controlled creature's own Movement Allowance is not spent.

Drive / Drag v0 cannot be combined with Cautious Movement. A later rule may explicitly author Cautious pair movement.

### Legal pair movement

The destination square must be physically capable of containing both Grapple participants.

A Drive / Drag step cannot enter:

- a square occupied by another creature unless an explicit rule permits that occupancy;
- impassable geometry that either body cannot physically traverse;
- another position where the pair cannot plausibly maintain the Grappling State.

Terrain and area effects in the destination square apply to both creatures normally.

Drive / Drag itself does not create collision, crushing, chain-displacement, or Throw damage.

### Opportunities during Drive / Drag

For Movement Opportunity purposes, the **Controller** is the voluntary mover and the Controlled creature is being moved as part of the Grapple.

When the shared Grapple square leaves a square threatened by a **third-party enemy** during Drive / Drag:

- that third-party enemy gains **one** Movement Opportunity for that Drive / Drag movement segment, subject to the normal one-per-enemy-per-segment limit;
- the Controlled creature does **not** gain a Movement Opportunity against its Controller merely because the shared Grapple square moves;
- the pair does **not** generate two Opportunities merely because two creatures occupy the shared square;
- when the third-party enemy exploits that Opportunity, **either Grapple participant may be chosen as the attack target** if that participant is otherwise a legal target for the attack;
- movement of the Controlled creature does not create a second general Movement Opportunity because it is not the voluntary mover.

The Grapple Contest used to resist Drive / Drag is the Controlled creature's authored opposition to that pair movement; Drive / Drag does not also grant that creature a general Movement Opportunity against the Controller.

If an Opportunity response breaks the Grappling State, removes the Controller's Control, incapacitates the Controller, or otherwise makes pair movement illegal, the Drive / Drag Movement Segment ends immediately.

## Takedown

**Takedown** is the Grapple escalation used by a Controller to force the Controlled creature Prone.

Only the **Controller** may attempt a Takedown.

Attempting a Takedown costs **one Physical Action** and requires:

- an existing Controller/Controlled Grappling State;
- a Controlled creature that is not already Prone;
- **Prone must be a meaningful physical result for the Controlled creature in its current position**;
- a plausible way to convert the current hold into a takedown;
- at least one currently legal successful result: **Dump** or **Follow Down**.

Do not make the Grapple Contest unless at least one successful result is legal when the Takedown is declared. Recheck immediately before the contest if an intervening effect changed positioning or terrain.

For this availability check:

- **Dump** is legal only if an adjacent legal free square exists for the Controlled creature;
- **Follow Down** is legal only if Prone is also a meaningful physical result for the Controller in the resulting position.

If exactly one result is legal, a successful Takedown must use that result. If both are legal, the Controller chooses between them after winning the contest.

A creature that is climbing, swimming, falling, suspended, unsupported, or otherwise in a position where the ground-based Prone state is not physically meaningful cannot be subjected to Takedown v0 merely because it is not already Prone.

If the intended maneuver is instead to tear a creature away from climbing support, disrupt swimming propulsion, force it from a ledge, or create another traversal/hazard consequence, resolve that through the applicable Traversal Disruption, forced-movement, or later hazard/maneuver procedure rather than substituting Takedown.

Because the participants are already in secured bodily contact, Takedown does **not** create another Close-Contact Opportunity between them.

Make the normal **Grapple Contest**.

- **Controller wins** → Takedown succeeds;
- **tie** → Takedown fails and the existing Control position remains unchanged;
- **Controlled creature wins** → Takedown fails, any Pin that depended on the former Control ends, and Control degrades to **Neutral**.

This follows the positional progression:

```text
win  -> gain the intended positional advantage
tie  -> preserve the current position
lose -> lose the current controlling advantage
```

### Successful Takedown

When the Controller wins, choose one of the following results.

#### Dump

The Controller puts the target down and releases the hold.

Dump may be chosen only if there is an adjacent legal free square for the Controlled creature.

- the Controller remains in the shared Grapple square;
- the Controller chooses an adjacent legal free square for the Controlled creature;
- the Controlled creature is placed there **Prone**;
- that separation costs no MP and does not create the general Movement Opportunity;
- the Grappling State ends;
- any Pin or Control dependent on that Grappling State ends;
- the Controller does **not** become Prone merely because of the Takedown.

The one-square separation is part of resolving Dump, not a general Throw or collision effect.

#### Follow Down

The Controller follows the target to the ground to preserve the grapple.

Follow Down may be chosen only if **Prone is also a meaningful physical result for the Controller** in the resulting position. If the Controller cannot meaningfully become Prone there, the Controller may choose Dump instead but cannot use Follow Down.

- the Controlled creature becomes **Prone**;
- the Controller also becomes **Prone** as part of resolving the Takedown;
- both remain in the same shared Grapple square;
- the Grappling State continues;
- the same creature remains Controller.

Follow Down represents accepting the positional cost of going to the ground in order to preserve Control.

### Standing after Follow Down

The preserved Control created by Follow Down is explicitly dependent on the Controller remaining down with the Prone target.

A Follow Down Controller may Stand while the Controlled creature remains Prone only as part of a **voluntary release and separation**.

To do so:

1. there must be an adjacent legal free square for the Controller;
2. the Controller must be able to pay the normal **4 MP Stand cost** plus the normal MP cost of one legal separation step into that square;
3. the Grappling State remains in force while the Controller Stands, so the shared-square occupancy remains legal;
4. when Standing completes, any dependent Pin ends and Control becomes **Neutral**; the Grappling State itself remains as the temporary shared-square occupancy state;
5. the Controller then immediately attempts the paid separation step into the chosen square;
6. that separation step follows ordinary Movement Opportunity rules;
7. the Grappling State ends only when the Controller actually completes the separation step and leaves the shared square.

If an Opportunity or other interruption prevents the separation step from completing:

- the Controller remains in the shared square;
- the Grappling State remains **Neutral**;
- the former Follow Down Control and any dependent Pin do not return automatically;
- a later legal separation, Gain Control, Reverse Control, or other Grapple procedure resolves the resulting position normally.

If the Controller cannot legally begin the full Stand-and-separate procedure, it cannot use Standing to obtain a standing position while preserving or silently ending Follow Down Control.

Under Takedown v0, a Controller therefore cannot both become standing **and** preserve Grapple Control over a creature that remains Prone. The transient Neutral shared-square state exists only to keep occupancy legal until separation succeeds or another Grapple result replaces it. A later technique or explicit feature may author a standing-control result or a separate contest that permits it.

### Takedown and existing Pin

A Takedown changes body position substantially. An existing Pin persists only if its already-defined physical requirements remain genuinely satisfied through the resulting position.

If the required limbs, leverage, or body position cease to be valid, the Pin ends under the normal Pin-dependency rule even though the Grappling State may continue through Follow Down.

### Takedown result boundary

Takedown does not inherently:

- deal damage;
- create displacement beyond the one-square separation required by **Dump**;
- create a free strike;
- establish a new Pin.

Damage from a throw, collision, edge, falling surface, or similar hazard requires the later Throw/collision/hazard procedures.

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

A third creature may spend one Physical Action to **Intervene** against a Controller that is Grappling an ally or another creature in a shared Grapple square.

The intervener must:

- not already be participating in another Grappling State;
- be adjacent to the shared Grapple square; and
- be able to establish plausible close bodily contact.

If the Controller currently threatens the intervener, entering that contact creates the normal **Close-Contact Opportunity** before the Intervention contest. A hit applies the same **-2** modifier to the intervener's ensuing Grapple Contest.

Before rolling, the intervener chooses one objective.

### Peel Off

**Peel Off** attempts only to break the Controller's hold on the original Controlled creature.

Peel Off can be declared only if the former Controller would have at least one adjacent legal free square into which it can be separated on a successful result.

Make a Grapple Contest between the intervener and the Controller.

- **intervener wins** → the original Controlled creature remains in the former shared square; the intervener chooses an adjacent legal free square and separates the former Controller into it; the original Grappling State ends; the intervener does not automatically enter Grappling State;
- **Controller wins** → the original Grappling State and Control remain unchanged;
- **tie** → Control breaks but the original Controlled creature is not released; the original Grapple becomes **Neutral** in the same shared square.

The successful Peel Off separation costs no MP and does not create the general Movement Opportunity.

### Take Over

**Take Over** attempts to free the original Controlled creature **and** replace it in the shared Grapple square as the former Controller's new opponent.

Take Over can be declared only if the original Controlled creature will have at least one legal adjacent free square after the intervener enters the shared square. The intervener's vacated starting square may satisfy this requirement if it is legal for the released creature.

The intervener suffers:

```text
-2 to this Intervention Grapple Contest
```

Make a Grapple Contest between the intervener and the Controller.

- **intervener wins** → the intervener chooses an adjacent legal free square for the original Controlled creature; that creature separates into the chosen square; the intervener enters the shared Grapple square; the original Grappling State ends; a new Grappling State begins between intervener and former Controller with the intervener as Controller;
- **Controller wins** → the original Grappling State and Control remain unchanged;
- **tie** → the intervener chooses an adjacent legal free square for the original Controlled creature; that creature separates into the chosen square; the intervener enters the shared Grapple square; the original Grappling State ends; the intervener and former Controller enter a new **Neutral Grappling State**.

The intervener chooses the released creature's destination on both a successful and tied Take Over. The replacement movement is part of the Intervention action, costs no MP, and does not create the general Movement Opportunity.

Take Over is harder than Peel Off because it asks the intervener not only to break the existing control relationship but to convert that intervention into a controlling position of their own.

## Multi-participant boundary

Grapple v0 does not model arbitrary chains of simultaneous control such as one creature controlling a second creature that simultaneously controls a third.

Ordinary Grapple initiation therefore requires both participants to be free of any existing Grappling State. Use **Grapple Intervention** when an eligible third creature is trying to break or replace an existing control relationship.

Dedicated rules for cooperative dogpiles, multiple creatures restraining one target, unusual multi-limbed creatures, and other true multi-participant Grapples remain future work.

## Deliberately unresolved Grapple layers

Grapple v0 does not yet define:

- Throw procedures beyond the locked Takedown v0;
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
