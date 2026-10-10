# Movement Foundation

> Canonical Veilbound grid-movement baseline. This page defines ordinary Movement Points, split movement, movement segments, diagonal cost, cautious movement, occupancy, blocked corners, melee reach, threatened space, movement-based Opportunities, forced movement, teleportation, and reserved Movement Interception. [Rapid Advance and Charge v0](rapid-advance-and-charge-v0.md) author fixed-heading faster approaches; Sprint, terrain costs, movement impairments, and Prone/Crawl/Stand movement are defined in [Special Movement, Terrain, and Prone](special-movement-terrain-and-prone.md). Climbing and swimming capability/state/segment rules are defined in [Traversal Foundation](traversal-foundation.md).

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

A **movement segment** is one continuous period of movement between actions/effects begun by the moving creature.

- when the **moving creature** begins one of its own actions or effects, its current movement segment ends;
- after that action/effect resolves, later movement by that creature begins a new segment;
- an enemy's Opportunity Attack, Reaction, or other spontaneous response does **not** by itself end the mover's segment;
- switching between Normal and Cautious Movement does **not** by itself end the segment;
- a **Movement Interception** that completes at least one legal step during an active creature's movement ends that creature's current movement segment as described under Movement Interception below.

A creature using ordinary movement may change direction, change between Normal and Cautious Movement, or stop moving without creating a new segment merely by changing movement mode. A new segment begins when movement resumes after one of the mover's own intervening actions/effects or after a qualifying Movement Interception has broken the segment. **Rapid Advance, Charge, and Sprint** override the ordinary permission to change heading: their authored heading persists across breaks in movement segments.

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

The [Grappling State](universal-maneuvers.md#shared-grapple-square) is one such explicit exception: its two participants occupy one shared Grapple square until that state ends or an effect separates them.

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

Entering an allied occupied square is a transit: the mover must have enough MP and a legal route to enter and then leave that square as one continuous passage. See [Special Movement, Terrain, and Prone](special-movement-terrain-and-prone.md#allied-square-transit).

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

Movement may be reserved through the existing **Interception** framework. Sprint-specific limits on reserving MP are defined in [Special Movement, Terrain, and Prone](special-movement-terrain-and-prone.md#sprint); [Rapid Advance and Charge](rapid-advance-and-charge-v0.md#shared-movement-model) also prohibit new MP reservations after their activation. Their extra allowance does not become out-of-turn Interception movement.

On the reserving creature's turn:

1. choose a specific trigger with a meaningful possibility of not occurring;
2. reserve any amount of the creature's **remaining MP**;
3. commit that reserved MP immediately.

The reserved MP is no longer available for ordinary movement during that turn. Reserved MP is still subject to later reductions in the creature's normal Movement Allowance; see [Impairments, spent MP, and Movement Interceptions](special-movement-terrain-and-prone.md#impairments-spent-mp-and-movement-interceptions).

A reserved **Movement Interception cannot release during the reserving creature's own turn**. It is an out-of-turn positioning reservation, not a way for the active mover to react to Opportunities or other responses generated by its own movement.

The exact future route does **not** need to be declared when the reservation is made. If the trigger occurs on another creature's turn or otherwise while the reserver is not taking its own turn, the creature chooses a legal route under the battlefield state that exists when the Interception resolves and may spend up to the reserved MP. A Movement Interception remains subject to later mobility impairments throughout its full lifecycle, including while unreleased, released-but-queued, currently resolving, or suspended by a nested response. If multiple Movement Interceptions were reserved from the same turn's Movement Allowance, MP spent by a completed one remains charged against that reservation cohort while any sibling pool from the cohort remains live. See [Impairments, spent MP, and Movement Interceptions](special-movement-terrain-and-prone.md#impairments-spent-mp-and-movement-interceptions).

Reserved movement follows all ordinary movement rules, including:

- orthogonal/diagonal costs;
- Cautious Movement;
- occupancy and blocked-corner rules;
- threatened space and Movement Opportunities.

Unless another rule provides a different reservation window, unused reserved MP expires at the start of the reserving creature's next turn.

### Effect on an active mover

When a Movement Interception resolves during another creature's active movement, it ends that active creature's current movement segment **only if the interceptor completes at least one legal movement step**.

Merely releasing the reservation, spending 0 MP, or having too little reserved MP to complete any legal step does not break the active mover's segment. A released reservation remains committed/used under the normal Interception rules even if no movement occurs.

After a Movement Interception that completed at least one legal step, and any nested responses resolve:

1. re-evaluate the battlefield state;
2. re-check whether the active creature's intended next step remains legal;
3. the active creature may choose what to do next;
4. any remaining MP remains available unless the Interception itself removed or restricted it.

If the active creature resumes movement, that movement begins a **new movement segment**.

The active creature is not forced to continue along a route chosen before the Interception changed the battlefield.

## Deferred movement layers

The following are intentionally not defined by Movement Foundation:

- specialized charge variants beyond locked [Charge v0](rapid-advance-and-charge-v0.md), and other attack-linked movement maneuvers;
- extra movement purchased directly through Turn AP;
- exact Climb/Swim MP costs and speed calibration;
- Catch Grip, falling, and detailed water-hazard procedures;
- jumping and falling;
- squeezing;
- size-based occupancy/reach exceptions;
- flight and other special movement modes;
- generic movement checks outside authored traversal/hazard procedures;
- detailed forced-movement resolution;
- movement-specific conditions beyond the locked Prone movement consequences;
- weapon-family Reach assignments beyond the ordinary adjacent baseline.
