# Special Movement, Terrain, and Prone

> Canonical extension to [Movement Foundation](movement-foundation.md). This page locks Sprint, terrain step costs, movement-allowance impairments, allied-square transit requirements, and the movement and combat consequences of Prone. Climbing and swimming foundations are defined separately in [Traversal Foundation](traversal-foundation.md). [Rapid Advance and Charge v0](rapid-advance-and-charge-v0.md) are now locked as straight-heading walking modes; traversal speed calibration, jumping/falling, squeezing, size exceptions, flight, and weapon-specific Prone handling beyond the baseline remain later work.

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

## Rapid Advance and Charge

[Rapid Advance and Charge v0](rapid-advance-and-charge-v0.md) lock two additional fixed-heading walking/running modes:

- **Rapid Advance:** no AP, `floor(3 × impaired normal Movement Allowance / 2)`, usually **18 MP**.
- **Charge:** one Physical Action for its culminating melee attack, `2 × impaired normal Movement Allowance`, usually **24 MP**, minimum 3 completed steps, with conditional AP commitment on attack or use beyond the Rapid allowance.
- Both require starting before any MP is spent/reserved; use a fixed heading, ordinary terrain and Opportunity rules, and **no Dodge penalty**. See the dedicated rule for attack, abort, retargeting and Interception timing.

## Sprint

**Sprint is a Full Action.**

Sprint is **not eligible to be reserved as an Interception**. It must be declared and resolved during the creature's own turn. It cannot begin in a turn where Rapid Advance or Charge was already initiated, including an aborted Charge; Rapid Advance and Charge likewise cannot begin after Sprint.

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

If an external response changes the battlefield after the passage has legally begun, do not retroactively make the original entry illegal. Resolve the response normally.

If the mover can no longer complete a legal exit from the allied square because it is Prone, lacks sufficient usable MP, has every exit blocked, or is otherwise unable to leave, use **Interrupted Allied Transit**:

1. keep every consequence of the interruption;
2. return the mover to the last legal square it occupied immediately before entering the ally's square;
3. refund **no MP** spent to enter the allied square;
4. this fallback repositioning is not voluntary movement and does not create a Movement Opportunity.

If that previous square is itself no longer legal or occupiable, place the mover in the nearest legal square adjacent to the ally's square, minimizing distance from the previous square. If several such squares are equally near, the mover chooses among them. This fallback placement likewise costs no MP and does not provoke.

Only if no legal adjacent square exists may the mover temporarily co-occupy the allied square. That exceptional co-occupancy lasts only until the first legal opportunity for either creature to leave the square; neither creature may voluntarily choose to remain co-occupied when a legal separation is available.

## Movement impairments

A movement impairment reduces the creature's **normal Movement Allowance** rather than increasing the price of every square.

For an ordinary creature:

```text
Impaired normal Movement Allowance =
12 MP - explicit impairment
```

An effect that impairs movement states its MP reduction.

Rapid Advance, Charge, and Sprint are calculated from the impaired normal allowance:

```text
Rapid Advance MP = floor(3 × impaired normal Movement Allowance / 2)
Charge MP        = 2 × impaired normal Movement Allowance
Sprint MP        = 3 × impaired normal Movement Allowance
```

This makes an impairment proportionally meaningful at both walking and Sprint speeds.

An especially serious impairment may explicitly state that the creature **cannot Sprint**, regardless of remaining MP.

### Becoming unable to Sprint after Sprint is active

If a creature becomes **unable to Sprint** after Sprint has already replaced its Movement Allowance for the turn:

1. Sprint remains activated, but its remaining Sprint MP becomes **suspended**;
2. the creature cannot convert that suspended pool back into ordinary movement;
3. the creature cannot spend suspended Sprint MP while the prohibition lasts unless an explicit rule permits a specific expenditure;
4. the current Sprint movement segment ends when the prohibition takes effect;
5. the Sprint Heading is retained.

If the prohibition ends before turn cleanup, the creature may resume Sprint as a **new movement segment** using the same Sprint Heading and whatever Sprint MP remains. Any numeric movement impairment that also changed during the prohibition recalculates the Sprint allowance normally and may reduce what remains available.

If the prohibition is still active at turn cleanup, all unused suspended Sprint MP is lost normally.

**Prone** uses this same suspension rule. Its Standing rule is an explicit exception that allows **4 suspended Sprint MP** to be spent to Stand.

Movement Allowance cannot fall below 0 MP.

### Impairments, spent MP, and Movement Interceptions

A movement impairment applies to movement capacity that has already been partly spent, reserved, released, queued, or temporarily suspended by nested responses. None of those states preserves the old allowance.

A **Movement Interception reservation cohort** consists of all Movement Interception reservations made from the same turn's Movement Allowance.

A **live Movement Interception pool** is any MP commitment from a cohort that has not fully finished its Interception lifecycle. It includes:

- an unreleased Movement Interception reservation;
- a released Interception waiting in the Initiative-order resolution queue;
- a released Interception currently resolving;
- a released Interception whose resolution is temporarily suspended while a nested response resolves.

A particular pool stops being live when its resolution fully finishes or the reservation/pool expires or is reduced to 0 MP.

However, MP actually spent by a completed Movement Interception remains **retained cohort spend** while any other pool from the same reservation cohort remains live. Retained cohort spend stops being tracked only when that cohort has no live Movement Interception pools remaining.

When an impairment changes during the creature's own turn:

1. recalculate its current normal Movement Allowance;
2. if Rapid Advance, Charge, or Sprint is active, also recalculate that mode's allowance using its defined multiplier (with floor for Rapid Advance);
3. MP already spent during that turn remains spent and counts against the recalculated current-turn allowance;
4. unreleased Movement Interception reservations also count against that recalculated allowance.

During the creature's own turn:

```text
MP already spent this turn
+ total unreleased reserved MP
≤ recalculated current-turn Movement Allowance
```

If the left side exceeds the recalculated allowance, reduce unreleased reservations until the total fits. Reduce the **newest-declared Movement Interception reservation first**, then continue backward through earlier reservations if necessary. MP already spent is never retroactively undone.

Separately, Movement Interception commitments are continuously bounded by the creature's current impaired normal Movement Allowance.

At all times:

```text
retained completed Interception spend
+ MP already spent by live released Movement Interceptions
+ unspent MP remaining across all live Movement Interception pools
≤ current impaired normal Movement Allowance
```

For this formula:

- **retained completed Interception spend** is MP actually spent by completed Interceptions whose reservation cohort still has at least one live pool;
- **already spent by live released Interceptions** includes MP spent by a released Interception that has begun resolving but has not yet fully finished, even if its resolution is currently suspended by a nested response;
- **unspent MP** includes unreleased reservations, released-but-queued pools, the remaining MP of currently resolving Interceptions, and the remaining MP of suspended Interceptions;
- completed spend from a cohort is discarded from this accounting only when the final live pool from that cohort finishes or expires;
- use the creature's **normal impaired allowance** for this cap even if Sprint has replaced its current-turn allowance;
- Sprint MP itself cannot be newly reserved.

### Impairment while Movement Interceptions are live

Whenever an impairment lowers the cap, immediately recalculate all live Movement Interception pools before the affected creature takes any further Movement Interception step or a queued Movement Interception begins resolving.

If the cap is exceeded, reduce unspent live MP in this order:

1. **unreleased reservations**, newest-declared first;
2. **released but not yet begun** Interceptions, starting with the one latest in the pending resolution order and working backward;
3. remaining MP in **already-started** Interceptions, starting with the most recently begun Interception and working backward through any suspended older Interceptions.

MP already spent by an already-started Interception is never rolled back.

If retained completed Interception spend plus MP already spent by live released Interceptions equals or exceeds the new impaired normal Movement Allowance, all of that creature's live Movement Interceptions lose their remaining MP. A currently resolving Interception ends immediately after the effect that caused the impairment finishes resolving; queued Interceptions reduced to 0 never begin movement.

Any MP removed by these rules is lost. A reservation or released pool reduced to 0 MP expires/finishes as appropriate. Later recovery or removal of the impairment does **not** restore trimmed MP.

Examples:

- A creature moves 6 MP, reserves its remaining 6 MP, then suffers an impairment that reduces its normal allowance to 6 MP. Since `6 spent + 6 reserved > 6`, the reservation is reduced to **0 MP** and expires.
- A creature releases a 12-MP Movement Interception and spends 2 MP. An impairment then reduces its normal Movement Allowance to 6 MP and it has no other live pools. The released Interception is immediately reduced to **4 MP remaining**, for a maximum of 6 MP spent by that Interception in total.
- Two of a creature's Movement Interceptions are live: one has released and is queued with 6 MP, while another 4 MP remains unreleased. If an impairment reduces the normal allowance to 6 MP, trim the unreleased 4 MP first; the queued 6-MP pool remains. If the allowance instead falls to 2 MP, the unreleased pool is lost and the queued pool is then reduced to **2 MP** before it begins.
- A released Interception has spent 2 MP and is suspended by a nested response with 6 MP remaining. If that nested response reduces the creature's normal allowance to 4 MP and no other live pools exist, the suspended Interception is reduced to **2 MP remaining** before it resumes.
- A creature reserves two 6-MP Movement Interceptions from the same turn. The first later resolves and spends all 6 MP while the second remains reserved. That completed 6 MP remains retained cohort spend. If an impairment then reduces the creature's normal allowance to 6 MP, the remaining 6-MP reservation is reduced to **0 MP** and expires.

After the creature's own turn ends, ordinary MP spent during that completed turn no longer counts against a surviving reservation. MP spent by a live released Movement Interception continues to count while that pool is live. MP spent by a **completed** Movement Interception continues to count as retained cohort spend only while another pool from the same reservation cohort remains live. Once the cohort has no live pools remaining, its completed spend no longer affects future movement accounting.
## Prone movement state

This section defines the baseline **movement and combat consequences** of being Prone.

Prone is a positional state, not helplessness. A Prone creature may still attack, Guard, Dodge, use magic, manipulate equipment, and perform other actions when its actual body position, free limbs, equipment, and the action's physical requirements permit them.

A Prone creature:

- remains in its current square;
- cannot use ordinary walking movement while Prone;
- cannot Sprint, Rapid Advance, or Charge while Prone;
- may normally move by **Crawling**;
- may spend MP to **Stand**.

**Sprint exception:** Prone applies the general [becoming unable to Sprint after Sprint is active](#becoming-unable-to-sprint-after-sprint-is-active) rule. The suspended Sprint pool cannot fund Crawl or Cautious Crawl. Prone explicitly allows **4 MP from that suspended Sprint pool only to Stand**. If the creature cannot pay the 4 MP Stand cost, it cannot voluntarily move using that suspended Sprint allowance while Prone.

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

### Attacking while Prone

A Prone creature may attack when the chosen attack is physically usable from its current posture.

For **melee attacks** made while Prone:

```text
Prone melee attack modifier = -2
```

This represents reduced leverage, reach management, footwork, and ability to drive through the strike.

Prone does **not** apply a universal modifier to every ranged attack. Instead, the ranged weapon or attack method must actually be usable from the posture.

- an ordinary bow cannot normally make its standard shot while Prone unless an explicit technique, position, or weapon rule permits it;
- an already-loaded crossbow or another ranged weapon that can genuinely be aimed and fired from the posture may attack normally;
- exact weapon-by-weapon restrictions for spears, halberds, other long weapons, unusual bows, reload procedures, and specialized firing postures remain part of the weapon pass.

A weapon being merely held is not enough. If its required swing, draw, bracing, line of fire, or body mechanics cannot be performed from Prone, that attack profile is unavailable.

### Melee attacks against a Prone target

A non-Prone attacker making a melee attack against a Prone target gains:

```text
+2 to the melee attack roll
```

This represents superior angle, reach control, and access against a target that cannot use ordinary standing footwork.

A Prone attacker does **not** gain this +2 merely because its target is also Prone. The attacker's own Prone melee penalty still applies normally.

Being Prone does **not** inherently increase:

- damage;
- Penetration;
- critical tier;
- wound severity;
- Called Shot effect.

If a specific exposed body part or vital is being deliberately targeted, use the applicable Called Shot or later targeting procedure rather than treating Prone as an automatic damage multiplier.

### Guard while Prone

Prone does not inherently remove Guard and does not apply a universal Guard Defense penalty.

A Prone creature may Guard only when it can physically orient and operate the chosen Guard instrument from its actual posture.

Examples include raising a usable shield, turning a blade into the attack, or parrying with a sufficiently free weapon. A weapon trapped beneath the creature, a limb committed to another hold, or an instrument that cannot be brought into the attack line cannot provide that Guard.

All ordinary Guard capacity, weapon capability, body-part commitment, and other Guard rules still apply.

### Dodge while Prone

Prone does not inherently remove Dodge and does not apply a universal Dodge Defense penalty.

A Prone Dodge represents physically plausible repositioning within the creature's posture, such as:

- rolling;
- twisting the torso;
- pulling a limb clear;
- flattening or shifting the body;
- another movement that does not require ordinary standing footwork.

If the current position, Pin, restraint, terrain, confinement, or another effect prevents the required repositioning, Dodge is unavailable under the normal physical-feasibility rule.

The melee attacker's +2 against a Prone target already represents the standing positional advantage; do not also apply a generic Prone Dodge penalty for the same disadvantage.

### Ranged attacks against a Prone target

Prone can reduce a creature's presented target profile against sufficiently distant, roughly horizontal ranged attacks.

For a targeted ranged attack made from **3 or more squares away**, a Prone target gains:

```text
+2 Position Defense
```

when the Prone posture materially presents a smaller target profile to that attack.

This modifier:

- applies to both static **Ranged Defense** and active **Ranged Dodge**;
- stacks with the attack's normal Range Difficulty;
- does not apply at **1 or 2 squares**;
- does not apply when elevation, firing angle, target posture, or another circumstance substantially negates the reduced profile;
- does not protect against an area effect merely because the creature is Prone.

The GM does not grant an additional bonus merely because the range is very long; long-range difficulty is already represented by the ordinary Range Difficulty modifier.

### Standing

Standing from Prone costs **4 MP**.

Standing:

- costs no Turn AP;
- does not restore or reset Movement Allowance;
- does not refund MP already spent during the turn;
- **ends the creature's current movement segment when Standing begins**;
- ends the Prone movement state once completed.

The 4 MP Stand cost is committed when Standing begins. If Standing is later Interrupted or made impossible, that MP is not refunded.

Any movement after Standing is completed begins a **new movement segment**.

If a creature was knocked Prone after activating Sprint, its remaining Sprint allowance is suspended under the general cannot-Sprint rule except for paying the 4 MP Stand cost. If it Stands and still has Sprint MP remaining, the Prone prohibition ends and it may resume Sprint as a new movement segment under the existing Sprint Heading unless another rule or the battlefield state prevents it.

### Standing Opportunity

Beginning to Stand while threatened creates one authored **Standing Opportunity** before the Prone state ends.

- each enemy that currently threatens the Prone creature may exploit that Opportunity through the normal [Opportunity Response procedure](initiative-and-round-structure.md#opportunity-framework);
- the creature is still **Prone** while those Opportunity Attacks resolve, so all applicable Prone attack and defense modifiers still apply;
- a generic Opportunity Attack does **not** automatically Interrupt Standing merely because it hits;
- after all responses resolve, recheck whether Standing remains physically possible;
- if Standing remains legal, it completes normally;
- if a response incapacitates, restrains, displaces, or otherwise leaves the creature unable to complete the Stand, the creature does not Stand and the committed 4 MP remains spent.

Standing Opportunity is separate from the general Movement Opportunity for leaving a threatened square. A later movement step after Standing belongs to the new movement segment and can create its own ordinary Movement Opportunity normally.

A more specific rule may further constrain Standing when posture, restraint, Pin, terrain, or another authored effect makes the motion physically unavailable.

## Deferred special movement

Still unresolved:

- specialized mounted/momentum variants beyond locked [Charge v0](rapid-advance-and-charge-v0.md), and other attack-linked movement maneuvers;
- exact Climb/Swim MP costs and traversal speed calibration;
- Catch Grip, falling, and detailed water hazards;
- jumping and falling;
- squeezing;
- size-based occupancy and Reach exceptions;
- flight and other special movement modes;
- detailed forced-movement procedures;
- movement checks for exceptional terrain;
- weapon-specific Prone restrictions beyond the locked baseline, including detailed long-weapon handling and specialized ranged firing/reload postures.
