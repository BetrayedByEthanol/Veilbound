# Movement Foundation

> Canonical Veilbound grid-movement baseline. This page defines ordinary Movement Points, split movement, movement segments, diagonal cost, cautious movement, occupancy, blocked corners, melee reach, threatened space, movement-based Opportunities, forced movement, teleportation, and reserved Movement Interception. Sprint/Charge, difficult terrain, prone/crawling, climbing, swimming, jumping, squeezing, size exceptions, and special movement modes remain later work.

## Grid scale and Movement Points

One combat-grid square represents approximately **1.5 m / 5 ft**.

A creature with the ordinary baseline receives:

```text
Movement Allowance = 12 Movement Points (MP) per turn
```

Ordinary step costs are:

| Step | MP cost |
|---|---:|
| one orthogonal square | 2 MP |
| one diagonal square | 3 MP |

This is equivalent to up to **6 orthogonal squares**, approximately **9 m / 30 ft**, or **4 diagonal squares** when the entire allowance is spent on one direction of movement.

Movement Points are separate from Turn AP. Ordinary movement does not spend Turn AP.

Unused ordinary MP is lost at turn cleanup unless it was explicitly committed to a valid Movement Interception.

## Split movement

Movement may be freely split around actions and effects during the creature's turn.

For example, a creature may:

1. move;
2. make an Attack Sequence against one target;
3. move again;
4. make an Attack Sequence against another target;
5. spend its remaining MP afterward.

The creature does not predeclare its entire route.

## Movement segments

A **movement segment** is one continuous period of movement between actions/effects.

- beginning an action or effect ends the current movement segment;
- after that action/effect resolves, later movement begins a new segment;
- switching between Normal and Cautious Movement does **not** by itself end the segment;
- an Interception that resolves during an active creature's movement ends that creature's current movement segment as described under Movement Interception below.

A creature may change direction, change between Normal and Cautious Movement, or stop moving without creating a new segment merely by changing movement mode. A new segment begins when movement resumes after an intervening action/effect or after an Interception has broken the segment.

## Cautious Movement

A creature may move carefully to avoid exposing itself while leaving threatened space.

For a Cautious step:

1. take the normal base step cost;
2. double that base cost;
3. then add any flat occupancy or terrain surcharge.

Current Cautious costs before other surcharges are:

| Step | Normal | Cautious |
|---|---:|---:|
| orthogonal | 2 MP | 4 MP |
| diagonal | 3 MP | 6 MP |

A Cautious step does **not** create a Movement Opportunity merely for leaving a threatened square.

Changing from Cautious Movement to Normal Movement, or vice versa, does not create a new movement segment. If a creature later makes a normal provoking step during the same segment, that step may still create the segment's one Movement Opportunity from each relevant threatening enemy.

## Occupied squares

### Hostile creatures

A creature cannot voluntarily enter or pass through a square occupied by a hostile creature unless an explicit rule permits it.

### Allied creatures

A creature may pass through an allied creature's square by paying a **+2 MP flat surcharge** for the step that enters that occupied square.

The allied surcharge is added **after** any movement-mode multiplication.

Examples:

| Step through ally | Cost |
|---|---:|
| orthogonal, Normal | 4 MP |
| diagonal, Normal | 5 MP |
| orthogonal, Cautious | 6 MP |
| diagonal, Cautious | 8 MP |

A creature cannot normally end its movement in a square occupied by an ally.

Specific rules may later override these occupancy limits for size differences, phasing, tumbling, forced movement, or similar cases.

## Blocked corners

A diagonal step is legal only when the creature can physically pass through the corner.

A creature cannot move diagonally between two orthogonally adjacent blocking obstacles, occupied squares, or equivalent solid obstructions when those blockers leave no usable gap for the creature to pass through.

The grid does not allow a creature to squeeze through the touching corner of two blocked squares merely because the diagonal destination itself is open.

More detailed squeezing and size rules remain future work.

## Melee Reach

**Melee Reach** is the set of squares a creature can currently target with an ordinary melee attack using a ready melee weapon, natural weapon, or other explicit melee capability.

The ordinary adjacent-reach baseline includes the **8 surrounding squares**. A weapon, creature, technique, or other explicit rule may extend or alter that reach.

Melee Reach is based on current position, geometry, equipment, and capability. It does **not** disappear merely because the creature has no Turn AP remaining.

## Threatened space

A creature **threatens** every square within its current Melee Reach while it remains capable of making the relevant melee attack.

Being threatened does not by itself impose a generic accuracy, defense, movement, or action penalty. Threat matters when a rule says that movement or another action creates an **Opportunity**.

There is no separate universal engagement lock beyond Reach, threatened space, occupancy, and authored Opportunity triggers.

## Movement Opportunities

Entering a threatened square does **not** create a Movement Opportunity by default.

When a creature voluntarily attempts to leave a square threatened by an enemy using a **Normal** step, that enemy gains a **Movement Opportunity before the creature leaves the starting square**.

This includes both:

- moving from one threatened square to another threatened square; and
- moving from a threatened square to a square outside that enemy's Reach.

The triggering creature is still in the starting square when the Opportunity resolves.

A Cautious step does not create this Movement Opportunity.

### One per enemy per movement segment

The same threatening creature can gain at most **one Movement Opportunity from a particular mover during one movement segment**, regardless of how many provoking squares that mover crosses during that uninterrupted segment.

If an action/effect or Interception ends the segment and the creature later resumes movement, the resumed movement is a new segment and can create another Movement Opportunity.

This segment limit applies to the general movement trigger. Other distinct authored Opportunities may still occur normally.

### Opportunity Response

Movement Opportunities use the existing [Opportunity Response](initiative-and-round-structure.md#opportunity-framework) procedure.

The first Opportunity a creature chooses to exploit during a round spends its Reaction and activates Opportunity Response. Later distinct Opportunities may be exploited without another Reaction while Opportunity Response remains active, up to the creature's Opportunity Capacity.

A generic Opportunity Attack does not automatically Interrupt movement. If the attack or another response creates a consequence that makes the intended movement illegal or impossible, re-evaluate the movement under the changed state.

## Other actions while threatened

Movement is not the only possible source of Opportunities.

An action or effect performed while threatened creates an Opportunity only when a rule explicitly says so.

The existing bow/crossbow rule is one such specific trigger: firing one while threatened creates an Opportunity before the ranged attack, and a successful resulting Opportunity Attack Interrupts that ranged attack.

Do not infer that every non-melee action provokes merely because it is performed while threatened.

## Forced movement

Forced or involuntary movement does **not** create a Movement Opportunity from the general movement trigger by default.

Examples include being shoved, dragged, knocked back, or displaced by an external effect.

A specific rule may explicitly make forced movement provoke.

## Teleportation and non-traversal movement

Teleportation, Blink, phasing, or another effect that relocates a creature without traversing the intervening squares does not create Movement Opportunities merely from the skipped threatened squares.

The activation of such an effect may still create an Opportunity if that effect or another rule explicitly says so.

Reaction-based Blink, next-turn AP Debt, and any desperation Overdraw rule are technique/action-economy content rather than part of this baseline movement lock.

## Movement Interception

Movement may be reserved through the existing **Interception** framework.

On the reserving creature's turn:

1. choose a specific trigger with a meaningful possibility of not occurring;
2. reserve any amount of the creature's **remaining MP**;
3. commit that reserved MP immediately.

The reserved MP is no longer available for ordinary movement during that turn.

The exact future route does **not** need to be declared when the reservation is made. If the trigger occurs, the creature chooses a legal route under the battlefield state that exists when the Interception resolves and may spend up to the reserved MP.

Reserved movement follows all ordinary movement rules, including:

- orthogonal/diagonal costs;
- Cautious Movement;
- occupancy and blocked-corner rules;
- threatened space and Movement Opportunities.

Unless another rule provides a different reservation window, unused reserved MP expires at the start of the reserving creature's next turn.

### Effect on an active mover

When a Movement Interception resolves during another creature's active movement, that active creature's current movement segment ends.

After the Interception and any nested responses resolve:

1. re-evaluate the battlefield state;
2. re-check whether the active creature's intended next step remains legal;
3. the active creature may choose what to do next;
4. any remaining MP remains available unless the Interception itself removed or restricted it.

If the active creature resumes movement, that movement begins a **new movement segment**.

The active creature is not forced to continue along a route chosen before the Interception changed the battlefield.

## Deferred movement layers

The following are intentionally not defined by Movement Foundation:

- Sprint and Charge;
- extra movement purchased through Turn AP;
- difficult terrain;
- prone and crawling;
- climbing;
- swimming;
- jumping and falling;
- squeezing;
- size-based occupancy/reach exceptions;
- flight and other special movement modes;
- generic movement checks;
- detailed forced-movement resolution;
- movement-specific conditions;
- weapon-family Reach assignments beyond the ordinary adjacent baseline.
