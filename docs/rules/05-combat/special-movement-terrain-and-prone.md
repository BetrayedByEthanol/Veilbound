# Special Movement, Terrain, and Prone

> Canonical extension to [Movement Foundation](movement-foundation.md). This page locks Sprint, terrain step costs, movement-allowance impairments, allied-square transit requirements, and the movement consequences of Prone. Charge, climbing, swimming, jumping/falling, squeezing, size exceptions, flight, and the non-movement combat effects of Prone remain later work.

## Calculation order

Movement uses two separate layers:

1. **Movement allowance** determines how many Movement Points (MP) the creature has available.
2. **Step cost** determines how much of that allowance a particular step spends.

For movement allowance:

```text
base normal Movement Allowance
→ apply movement-allowance impairments
→ apply the chosen movement mode's allowance rule
```

For an individual step:

```text
base step cost
→ apply slow movement-mode cost changes
→ add flat terrain and occupancy surcharges
```

Flat terrain and occupancy surcharges are not multiplied by Cautious Movement, Crawl, or another slow movement mode unless a rule explicitly says otherwise.

## Sprint

**Sprint is a Full Action.**

Sprint is **not eligible to be reserved as an Interception**. It must be declared and resolved during the creature's own turn.

The creature must meet the normal Full Action requirement: its entire Turn AP allotment for the turn must still be available, and declaring Sprint consumes that entire allotment.

For an unimpaired ordinary creature:

```text
Sprint Movement Allowance = 36 MP
```

More generally:

```text
Sprint Movement Allowance =
3 × impaired normal Movement Allowance
```

Sprint replaces the creature's normal Movement Allowance for that turn; it does not add a second pool. MP already spent earlier in the turn remains spent and counts against the Sprint allowance.

MP already committed to a Movement Interception before Sprint is declared also counts against the Sprint allowance and remains reserved under its original reservation. **Sprint MP cannot be newly reserved for a Movement Interception after Sprint is declared.**

A pre-existing Movement Interception reservation does not become Sprint movement when it later releases. It follows the ordinary reserved-movement rules and is not constrained by Sprint Heading. Because the reserved MP already counted against the Sprint allowance, this does not create additional movement beyond the Sprint total.

A Sprint that has resolved is not refunded or undone merely because a later Movement Interception or other response changes the battlefield.

### Sprint Heading

When the creature begins Sprint movement, choose one of the **8 grid directions** as its **Sprint Heading**.

While Sprinting:

- Sprint movement must continue along the current Sprint Heading;
- stopping does not reset the Sprint Heading;
- ending or restarting a movement segment does not by itself reset the Sprint Heading;
- the creature cannot voluntarily change Sprint Heading;
- Sprint movement cannot use Cautious Movement.

Sprint otherwise uses the ordinary movement rules, including base orthogonal/diagonal step costs, terrain surcharges, occupancy, blocked corners, threatened space, and Movement Opportunities.

Entering threatened space does not provoke by default. Leaving a threatened square during Sprint is Normal movement and therefore creates the ordinary Movement Opportunity where applicable.

### Forced Redirection

An external change may make continued movement along the current Sprint Heading physically impossible.

Examples include:

- a Movement Interception occupying or blocking the route;
- a newly created obstacle;
- an external displacement that leaves the current heading blocked.

If an external effect or response makes further movement along the current Sprint Heading illegal or physically blocked, the sprinter may pay **2 MP** to make a **Forced Redirection** and choose a new Sprint Heading.

Forced Redirection:

- is permitted only because of the external obstruction;
- does not refund any MP already spent;
- does not restore Turn AP;
- does not itself create a new movement allowance;
- is not available merely because the sprinter would prefer a different route.

If no legal continuation or Forced Redirection is available, the creature may stop; unused MP is lost normally at cleanup.

## Terrain

Terrain changes the cost of crossing affected squares rather than reducing the creature's whole Movement Allowance.

| Terrain | Flat step surcharge |
|---|---:|
| Normal | +0 MP |
| Difficult | **+2 MP** |
| Severe | **+4 MP** |
| Impassable | cannot normally enter |

The surcharge is added to the step that enters the affected terrain.

Examples:

| Step | Cost |
|---|---:|
| orthogonal through Difficult terrain | 4 MP |
| diagonal through Difficult terrain | 5 MP |
| orthogonal through Severe terrain | 6 MP |
| diagonal through Severe terrain | 7 MP |
| Cautious orthogonal through Difficult terrain | 6 MP |
| Cautious diagonal through Difficult terrain | 8 MP |

A specific terrain feature may define a different surcharge or additional requirement.

## Allied-square transit

The existing +2 MP allied-square surcharge remains a flat occupancy surcharge.

A creature may enter an allied occupied square only when it has enough MP to **enter that square and leave it into a legal square as one continuous passage**.

The creature may not intentionally enter an allied square if the known remaining MP and route cannot complete that passage.

Example in Difficult terrain:

- orthogonal step into the ally's square: `2 base + 2 Difficult + 2 ally = 6 MP`;
- orthogonal step out into another Difficult square: `2 base + 2 Difficult = 4 MP`;
- total MP required before beginning the passage: **10 MP**.

This prevents movement costs from leaving two creatures stranded in the same square.

If an external response changes the battlefield after the passage has legally begun, resolve the changed state under the normal movement/interruption rules rather than retroactively making the original entry illegal.

## Movement impairments

A movement impairment reduces the creature's **normal Movement Allowance** rather than increasing the price of every square.

For an ordinary creature:

```text
Impaired normal Movement Allowance =
12 MP - explicit impairment
```

An effect that impairs movement states its MP reduction.

Sprint is calculated from the impaired normal allowance:

```text
Sprint MP =
3 × impaired normal Movement Allowance
```

This makes an impairment proportionally meaningful at both walking and Sprint speeds.

An especially serious impairment may explicitly state that the creature **cannot Sprint**, regardless of remaining MP.

Movement Allowance cannot fall below 0 MP.

### Impairments and reserved movement

A Movement Interception reservation does **not** preserve movement capacity against a later impairment.

At all times:

```text
total unreleased MP reserved for Movement Interceptions
≤ current impaired normal Movement Allowance
```

Use the creature's **normal impaired allowance** for this cap even if Sprint has replaced its current-turn allowance. Sprint MP itself cannot be newly reserved.

Whenever an impairment lowers the normal Movement Allowance below the creature's current total of unreleased reserved MP:

1. immediately reduce reserved MP until the total fits the new allowance;
2. reduce the **newest-declared Movement Interception reservation first**, then continue backward through earlier reservations if necessary;
3. MP removed from a reservation is lost and does not return to ordinary movement;
4. a reservation reduced to 0 MP expires immediately.

Example: a creature has reserved 12 MP and is then reduced to a 6-MP normal Movement Allowance. Its reservation is immediately reduced to **6 MP**. If its allowance falls to 0 MP, the reservation expires.

If the impairment later ends or weakens, trimmed reservation MP is **not restored**.

## Prone movement state

This section defines only the **movement consequences** of being Prone. Attack, Guard, Dodge, targeting, and any other combat consequences of Prone remain part of the later conditions/combat-position pass.

A Prone creature:

- remains in its current square;
- cannot use ordinary walking movement while Prone;
- cannot Sprint while Prone;
- may normally move by **Crawling**;
- may spend MP to **Stand**.

**Sprint exception:** if Sprint has already replaced the creature's Movement Allowance for the current turn and the creature becomes Prone, that remaining Sprint allowance is suspended while Prone. It cannot be spent on Crawl or Cautious Crawl. The creature may spend **4 MP from that remaining Sprint allowance only to Stand**. If it cannot pay the 4 MP Stand cost, it cannot voluntarily move using that Sprint allowance while Prone.

### Dropping Prone

A creature may voluntarily drop Prone for **0 MP** and **0 Turn AP**.

Dropping Prone is a movement-state change, not an AP-based action, and does not by itself end the current movement segment.

An external effect may also make a creature Prone under its own procedure.

### Crawl

Crawl is a slow movement mode.

| Step | Crawl cost |
|---|---:|
| orthogonal | 4 MP |
| diagonal | 6 MP |

Crawling is voluntary movement and follows ordinary threatened-space rules.

A normal Crawl step out of a threatened square can therefore create a Movement Opportunity.

### Cautious Crawl

Cautious Movement and Crawl stack **additively by copies of the base step cost**, rather than multiplying each other.

For the currently defined slow movement modes:

```text
Normal step = 1 × base step cost
Cautious step = 2 × base step cost
Crawl step = 2 × base step cost
Cautious Crawl = 3 × base step cost
```

Therefore:

| Step | Cautious Crawl |
|---|---:|
| orthogonal | 6 MP |
| diagonal | 9 MP |

Flat terrain and occupancy surcharges are added afterward.

Example:

```text
Diagonal Cautious Crawl through Difficult terrain
= (3 MP × 3) + 2 MP
= 11 MP
```

A Cautious Crawl step receives the normal benefit of Cautious Movement and does not create the general Movement Opportunity merely for leaving a threatened square.

### Standing

Standing from Prone costs **4 MP**.

Standing:

- costs no Turn AP;
- does not restore or reset Movement Allowance;
- does not refund MP already spent during the turn;
- **ends the creature's current movement segment when Standing begins**;
- ends the Prone movement state once completed.

Any movement after Standing is completed begins a **new movement segment**.

If a creature was knocked Prone after activating Sprint, its remaining Sprint allowance is suspended except for paying the 4 MP Stand cost. If it Stands and still has Sprint MP remaining, it may resume Sprint as a new movement segment under the existing Sprint Heading unless another rule or the battlefield state prevents it.

Whether **Standing while threatened** creates its own authored Opportunity is deliberately **not locked here**. The current general Movement Opportunity rule only triggers when voluntarily leaving a threatened square; the full Prone condition pass will determine whether Standing adds a separate trigger.

## Deferred special movement

Still unresolved:

- Charge and other attack-linked movement maneuvers;
- climbing;
- swimming;
- jumping and falling;
- squeezing;
- size-based occupancy and Reach exceptions;
- flight and other special movement modes;
- detailed forced-movement procedures;
- movement checks for exceptional terrain;
- non-movement combat effects of Prone;
- whether Standing while threatened creates a specific Opportunity.
