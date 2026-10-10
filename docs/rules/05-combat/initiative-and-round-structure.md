# Initiative and Round/Turn Procedure

> Canonical Veilbound combat-procedure baseline. This file locks initiative, the round/turn skeleton, turn/action declaration, Attack Sequences, Reaction timing, Interception timing, interruption behavior, Opportunity Attack capacity, core resource refresh timing, regeneration timing, and universal duration anchors. Ordinary grid movement, Reach, threatened space, Movement Opportunities, and Movement Interception are defined in [Movement Foundation](movement-foundation.md). Surprise, hazard values, special movement modes, and several combat maneuvers remain separate refinement work.

## Combat start

When structured combat begins:

1. establish which creatures are participating and what they are presently aware of;
2. determine any already-existing fiction that affects participation or awareness;
3. roll Initiative for each combatant;
4. establish Initiative order from highest to lowest;
5. begin Round 1.

This procedure does **not** yet define a universal surprise/unaware package. Awareness and surprise consequences remain part of the later battlefield-defense pass.

## Initiative

```text
Initiative =
d20
+ Agility
+ Awareness
+ explicit Initiative modifiers
```

Initiative represents both physical readiness to act and awareness of the developing situation.

Rules:

- roll Initiative once when combat begins;
- higher totals act first;
- natural 1 and natural 20 have no special Initiative effect;
- Training does not apply unless a rule explicitly grants an Initiative Training or modifier;
- tied willing allies may choose their relative order;
- other ties compare Awareness, then Agility;
- if still tied, make a simple roll-off;
- Initiative order normally remains fixed for the combat;
- completed turns are never retroactively undone or replayed by an Initiative change.

A later rule may explicitly change future Initiative order, but must say how it does so.

### Entering combat after it begins

A creature that becomes a combatant after Initiative has already been established rolls Initiative when it enters combat.

- If its Initiative position has not yet occurred in the current round, it acts at that position.
- If that position has already passed, its first turn occurs in the next round.

## Round structure

A round is one pass through the established Initiative order.

### Round Begin

At Round Begin:

1. expire effects that explicitly end at the start of the round;
2. refresh each combatant's normal Guard capacity;
3. reset each combatant's Dodge Pressure to 0;
4. refresh each combatant's one Reaction;
5. refresh other resources explicitly defined as **per round**;
6. resolve effects explicitly authored for the start of the round.

Round 1 uses the same procedure, initializing these round resources at full capacity.

Guard and Dodge are defensive responses, not Reaction expenditures.

### Turns

Combatants then take turns in Initiative order.

A creature does **not** pre-declare its entire turn. Normal actions are declared and resolved sequentially. Multi-attack use against one target is grouped into an **Attack Sequence** so the attacker must commit those attacks before seeing their results.

Out-of-turn Reactions, reserved Interceptions, defensive responses, Opportunity Attacks, and other interruptions occur when their triggers permit under the response procedure below.

### Round End

After the last combatant's turn:

1. resolve effects explicitly authored for the end of the round;
2. expire effects that explicitly end at the end of the round;
3. begin the next round.

There is no additional universal damage, regeneration, or resource-refresh event at Round End unless a specific rule says otherwise.

## Character turn procedure

A character's turn uses the following timing skeleton.

### 1. Start expiry

Expire effects that explicitly last until the start of this character's turn.

A reserved Interception or similar reserved action that uses the default reservation window also expires here if its trigger never occurred.

### 2. Regeneration Step

Resolve the character's once-per-round natural regeneration and the Dying survival/wound-repair procedure.

Natural regeneration occurs here **before** ordinary start-of-turn hazards and ongoing damage.

This preserves the rule that damage suffered after the Regeneration Step must normally remain until the character's next Regeneration Step.

See [HP and Vigor](../06-vigor-wounds-death/hp-and-vigor.md) and [Dying and Wounds](../06-vigor-wounds-death/dying-and-wounds.md).

### 3. Start-of-turn effects

Resolve effects explicitly authored for the start of this character's turn.

Unless a hazard says otherwise, an ongoing hazard already affecting the creature uses this timing.

Examples may later include fire, corrosive terrain, bleeding, poison, environmental exposure, or other persistent physical consequences. Their values and specific procedures are not defined by this file.

### 4. Establish turn resources

Determine the character's **Turn AP** allotment from level and explicit modifiers under [Turn Action Points and Tempo](action-categories-and-physical-tempo.md).

Turn AP is a **turn resource**, not a round resource. Also determine the character's derived Physical Tempo and Projection Tempo from the current Turn AP allotment and the Focus-based action costs.

A Full Action may be declared only while the character's entire Turn AP allotment remains available and consumes that entire allotment.

Also establish the creature's ordinary **12 MP Movement Allowance** under [Movement Foundation](movement-foundation.md). Movement Points are separate from Turn AP.

### 5. Start-of-turn choices

Resolve choices that occur after ordinary start-of-turn housekeeping and before normal actions.

Current examples include:

- choosing offensive or defensive dual-wield use;
- the Gifted Emotion Establishment Step.

The Gifted procedure remains exactly as defined in [Gifted Foundation](../08-archetypes/gifted.md): it occurs after ordinary start-of-turn housekeeping and before normal actions, and may spend the required **General Tempo Action AP** from the upcoming turn when its rules require it.

### 6. Normal turn

The character may spend Turn AP on Physical, Projection, or General Tempo actions; take a Full Action where legal; use techniques; make attacks; reserve eligible actions/effects for Interception; and move as permitted by the movement rules.

The character declares and resolves the next action or effect before choosing the next part of the turn. Costs or action capacity committed to a declaration are not refunded merely because the action is later interrupted, becomes impossible, or fails unless an explicit rule says otherwise.

Ordinary attacks against the same target use the Attack Sequence procedure below rather than being drip-declared one at a time.

### 7. End-of-turn effects

Resolve effects explicitly authored for the end of this character's turn.

### 8. End expiry

Expire effects that explicitly last until the end of this character's turn.

### 9. Cleanup

Unspent Turn AP and unreserved MP are lost.

MP already committed to a valid Movement Interception remains reserved only for that reservation's defined window. Other reserved actions/effects likewise continue only for their defined reservation window.

## Turn declaration and Attack Sequences

A character does **not** declare the entire turn in advance.

The default procedure is:

1. declare the next action/effect and its target or other required choices;
2. commit the required Turn AP, Full Action, Reaction, reservation, or other action capacity;
3. open any applicable response window;
4. resolve responses and nested responses;
5. re-check whether the declared action is still legal;
6. if legal, resolve it under the current circumstances;
7. then choose the next action/effect.

### Attack Sequence

When a creature makes one or more **ordinary on-turn attacks** against the same target, those attacks use one Attack Sequence. This includes attacks paid for with Physical, Projection, or General Tempo AP as applicable, plus granted ordinary attacks such as the offensive dual-wield off-hand Attack.

Before the first attack roll:

- declare every ordinary on-turn attack currently being committed to that target, including each attack's AP cost class and any attacks coming from granted bonus attacks;
- for **each committed attack**, declare the weapon/profile and all attack-specific choices that could affect its resolution, including any chosen attack mode, special option, or other required choice known at declaration time;
- commit the required Turn AP, granted attacks, and declared attack profiles/choices immediately;
- the defender assigns Take Hit, Dodge, or Guard to each incoming attack with those declared profiles/choices known before any attack roll in that sequence resolves.

A previously prepared [Aim v0](aim-v0.md#attacks-timing-and-interception) is **not itself an Attack Sequence**. When its specified ranged attack joins an ordinary sequence, commit all that target's attacks and identify the **single aimed shot** to the defender before assigning defenses or rolling; Aim cannot transfer to another target/profile/objective after observing results. Preparation consumed its own Physical Action AP earlier; the aimed attack still pays its normal separate action cost.

A [Charge v0](rapid-advance-and-charge-v0.md#attack-sequence-and-interception-timing) may start with a declared intended target, attack profile, and straight-line movement **before** the attack's AP becomes committed or defenses are assigned. Only the culminating attack has this limited deferred-commitment exception. Once the approach ends in an actual attack, finalize its legal target, commit any outstanding AP and all other ordinary attacks against that same target, and assign defenses to the **whole** Attack Sequence before the first attack roll. Charge never reopens an already-resolved sequence against that target.

A declared [Feint Combination](feint-combination-v0.md) may link two consecutive, separately paid melee attacks as part of this same sequence. Both attack profiles and the conditional **-2/+4/-2 accuracy rule** are fully committed before the defender assigns defenses; calculating the second attack's already-declared modifier from the first attack's outcome is **not** permission to change profiles, add attacks, or reopen defense choices afterward.

Then resolve the attacks in their declared order. **Each individual attack is a separate trigger occurrence.** Immediately before that attack's roll:

1. treat that attack as the current triggering action;
2. open and resolve its response window under the normal response procedure;
3. if the attack is still legal after responses, resolve its already-declared attack roll and consequences;
4. if it is Interrupted or otherwise made illegal, that attack is lost, then continue to the next committed attack unless a stronger rule cancels the remaining sequence.

After the sequence ends, the attacker may use any remaining turn resources normally.

A creature normally begins only **one Attack Sequence against a particular target during the same turn**. It cannot declare one attack, inspect the result, and then open another ordinary sequence against that same target to gain additional information. A granted ordinary bonus attack that is used against that target must therefore be included when that target's Attack Sequence is declared; if the sequence has already resolved, that bonus attack cannot later be added against the same target. It may still be used against another legal target that has not already received an Attack Sequence from this attacker that turn. An explicit follow-up rule such as a Riposte may override this restriction.

If the target becomes unavailable or illegal before all committed attacks resolve, the unresolved attacks remain committed rather than being refunded. The attacker may redirect the unresolved remainder as a new sequence against another legal target **only if that target has not already been the target of an Attack Sequence from this attacker during the same turn**, unless an explicit rule permits reopening that target. The weapon/profile and other attack-specific choices already declared for each redirected attack remain fixed unless an explicit rule permits changing them. The new defender assigns defenses to those already-declared redirected attacks before their rolls resolve, and counts as having been the target of an Attack Sequence for that turn.

A Full Action is not permission to bundle several ordinary AP-based actions into one action. It is a separate action category used only by actions/effects that are actually defined as Full Actions.

Out-of-turn attacks from a Reaction, Interception, or Opportunity normally consist of the one action/effect that authorized them and do not become an Attack Sequence unless a rule explicitly says otherwise.

## Regeneration and Dying timing

Natural HP regeneration resolves once on each character's own turn during the Regeneration Step.

```text
Regeneration throughput =
max(Vitality, 0) + Focus Rate
```

While Dying and still possessing Vigor, resolve the existing survival allocation during this same step. If no Vigor is available, the regeneration allocation cannot cancel the Dying loss or repair the wound unless another rule explicitly provides an alternative resource or conversion.

1. determine available regeneration throughput;
2. spend 1 point of throughput to cancel the default 1 HP Dying loss for this round, if possible and desired;
3. apply the default Dying loss if it was not cancelled;
4. use remaining throughput to spend Vigor and add cumulative **Repair Progress** to the active repairable wound;
5. prevent, offset, or medically control additional bleeding or similar ongoing losses where the relevant rules permit;
6. once accumulated Repair Progress reaches that wound's Repair Requirement, the wound is repaired; remaining throughput may then restore HP;
7. once HP rises above 0, the character may regain consciousness unless another effect prevents it.

A Dying or unconscious creature retains its Initiative position and turn timing even when it cannot take normal actions.

## Ongoing hazards

Default timing for a persistent hazard already affecting a creature is:

> Resolve the hazard at the start of that creature's turn, after its Regeneration Step, unless the hazard explicitly uses another timing.

A hazard may instead define a trigger such as:

- on entering the area;
- when struck or exposed;
- at the end of the creature's turn;
- at Round Begin or Round End;
- once every stated number of rounds;
- another explicitly authored event.

This is only a timing rule. Falling, collision, fire, environmental damage, hazardous terrain, and related values remain future physical-hazard work.

## Sustained and persistent effects

There is no universal rule that every Sustained effect automatically "ticks" once per round.

Use the existing Expression Cadence framework:

- **Continuous** remains true while valid;
- **Rider** triggers from its authored eligible event;
- **Pulse** uses its explicit refresh/timing unit;
- **Spend** requires its authored additional expenditure.

Committed VP remains committed across turn and round boundaries until the sustained effect ends unless the effect says otherwise.

There is no hidden universal upkeep roll or automatic per-round VP payment.

## Reactions, responses, Interception, and interruption

### Reaction

A **Reaction** is a once-per-round timing resource that allows an effect or rule explicitly usable as a Reaction to resolve when its trigger occurs.

- each combatant normally has one Reaction;
- it refreshes at Round Begin;
- spending it makes it unavailable until the next Round Begin;
- a Reaction may be used during the creature's own turn if a valid trigger occurs;
- a Reaction may respond to another Reaction, an Interception, an Opportunity Attack, or another interrupting effect if its own trigger is satisfied;
- the Reaction resource itself does nothing without a rule/effect that defines a trigger and consequence.

Guard and Dodge remain defensive responses and do **not** spend the Reaction.

### Response windows and nested responses

When an action/event creates a valid trigger, pause that action/event before it resolves.

Precommitted Interceptions have priority over spontaneous responses to the same original trigger.

For each trigger occurrence:

1. **Release matching Interceptions.** For each creature, identify at most one reserved Interception that releases from that trigger occurrence. If several of that creature's reservations have the same qualifying trigger, the earliest-declared matching reservation releases and the others remain reserved for later qualifying occurrences.
2. **Resolve released Interceptions first.** Released Interceptions resolve in Initiative order among their users. A released Movement Interception remains a live committed movement pool while waiting in this queue and remains subject to current mobility limits before its resolution begins.
3. **Resolve nested triggers immediately.** If an Interception creates a new trigger, open a nested response window before that Interception finishes. A valid Reaction, Opportunity Attack, or further Interception may respond to that new trigger under the normal rules. A Movement Interception suspended by this nested window remains live and subject to mobility changes until it resumes and fully finishes.
4. **Re-check the original event.** After all released Interceptions and their nested responses resolve, determine whether the original triggering action/event is still legal and relevant. If it has been cancelled or made impossible, it does not proceed to spontaneous responses unless a rule's trigger remains satisfied independently of the cancelled event.
5. **Collect spontaneous responses to the original event.** If the original event remains legal/relevant, eligible creatures may declare either:
   - an optional Reaction whose trigger is satisfied;
   - the first Opportunity Attack by spending the creature's available Reaction to activate Opportunity Response; or
   - a later Opportunity Attack from an already-active Opportunity Response with remaining Opportunity Capacity.
6. **Resolve spontaneous same-trigger responses.** These responses resolve in Initiative order among their users. If one response creates a new trigger, resolve that nested response window before returning to the older response.
7. **Resume the original event.** After all responses finish, re-check legality once more and resolve the original action/event if it remains legal.

Once a Reaction, Opportunity Attack, or released Interception is declared, its relevant capacity is committed. It may still resolve if the original action is later cancelled, provided the responding action/effect itself remains legal.

A creature with an active Opportunity Response does not need another Reaction to make later Opportunity Attacks; those later attacks still must be explicitly declared in Step 5 when a new qualifying Opportunity occurs.

### Interception

**Interception** is a timing mechanic, not a separate action category and not an automatic Interrupt.

On the reserving creature's turn:

1. reserve one otherwise legal action/effect, or a Movement Interception permitted by [Movement Foundation](movement-foundation.md);
2. declare a specific trigger with a meaningful possibility that it will not occur;
3. commit the required action capacity or reserved MP immediately.

Other costs such as VP are paid at the action/effect's normal resolution timing unless its own rule says otherwise.

An Interception reservation is **atomic**. [Aim v0](aim-v0.md#attacks-timing-and-interception) and the later attack are **two separate actions**: a single reservation cannot package Aim plus an Attack. A previously completed Aim can improve an otherwise legal separately reserved ranged attack if the target/profile/objective, remaining duration, and applicable difficulty source remain valid. Interception still resolves **before** its triggering event, creates no line of fire through solid cover, and grants no automatic Interrupt.

An Interception reservation is **atomic**:

- one reservation may contain one legal AP-based action/effect, committing its normal Physical, Projection, or General Tempo AP cost immediately;
- one action/effect that is inherently a **Full Action and otherwise eligible for Interception**, which requires and commits the reserving creature's entire Turn AP allotment; or
- one **Movement Interception**, committing a chosen amount of the creature's remaining MP.

A Full Action reservation cannot be used to bundle several ordinary AP-based actions into one Interception. Full Action status alone does not grant reservation eligibility; specific rules may prohibit it, as Sprint does. A Movement Interception reserves movement only and follows the route/timing rules in [Movement Foundation](movement-foundation.md).

A single trigger occurrence can release **at most one reserved Interception from the same creature**.

If the creature reserved several Interceptions with the same trigger, they apply to successive qualifying trigger occurrences rather than all firing together. If fewer trigger occurrences happen than the creature reserved for, the unused reservations are lost when their reservation window expires.

Different creatures may each have one Interception released by the same trigger occurrence. Once that trigger has occurred, those Interceptions remain triggered even if an earlier response Interrupts the original action; they still resolve if their own actions/effects remain legal.

Unless another rule gives a different reservation window, an unused Interception expires at the start of the reserving creature's next turn.

### Interception versus Interrupt

An ordinary Interception resolves **before** its triggering action but does not automatically cancel that action.

After the Interception resolves, re-check the triggering action under the new circumstances:

- if the action is still legal, it continues;
- if the Interception changed the fiction so the action is no longer legal, the action fails and its committed cost is lost;
- if the action remains legal but circumstances changed, resolve it using the new circumstances and applicable modifiers.

For example, causing an attacker to fall prone does not inherently cancel an attack. If the attack is still legal while prone, it continues under the applicable prone rules. If the fall moves the attacker out of reach or otherwise makes the attack impossible, it fails naturally.

An **Interrupt** is an explicit consequence that cancels the action currently being resolved.

- by default, Interrupt cancels only that current action and its committed cost;
- interrupting one attack in an Attack Sequence does not cancel the remaining committed attacks;
- cancelling the remaining Attack Sequence or ending the creature's turn requires explicit stronger wording;
- one current action can only be explicitly cancelled once. Additional responses that were already triggered may still resolve, but additional Interrupt components cannot make that same cancelled action lose its committed Turn AP cost more than once.

Weapons, maneuvers, techniques, or other rules may grant or improve deliberate disruption/Interrupt capability. No ordinary Interception gains automatic interruption merely because it hits, and the universal numerical modifier for a generic Disrupting Interception is not locked here.

## Opportunity framework

An **Opportunity** is an authored event that exposes a creature to an Opportunity Attack. [Movement Foundation](movement-foundation.md) defines the general voluntary-movement trigger from threatened space; specific rules may define additional Opportunities.

### Opportunity Response

```text
Opportunity Capacity = Physical Tempo
```

The first time a creature chooses to exploit an Opportunity in a round:

1. spend its available Reaction;
2. activate its **Opportunity Response** until Round End;
3. make one eligible Opportunity Attack against that triggering creature.

While Opportunity Response remains active:

- each later qualifying Opportunity creates a new chance to declare one Opportunity Attack during the spontaneous-response step of that trigger's response window;
- the creature may make that Opportunity Attack without spending another Reaction;
- it may make at most Opportunity Capacity Opportunity Attacks during that round in total;
- each distinct Opportunity trigger can produce at most **one** Opportunity Attack from that creature;
- one creature may trigger multiple distinct Opportunities during the round;
- several eligible enemies may each exploit the same Opportunity with their own Opportunity Response/capacity.

An Opportunity Attack is one attack authorized by the triggering rule, normally a melee attack unless that rule says otherwise. It does not consume Turn AP and is not a full Attack Sequence. Its round-side limit is Opportunity Capacity.

A generic Opportunity Attack does **not** automatically Interrupt the provoking action. A trigger may explicitly say that a successful Opportunity Attack Interrupts it. Firing a bow or crossbow while threatened is one existing such special case.

Spending the Reaction to activate Opportunity Response means that Reaction is no longer available for another Reaction effect during that round, even if Opportunity Capacity remains unused.

## Duration language

Use explicit timing anchors.

| Wording | Timing |
|---|---|
| **until the start of your next turn** | expires during Start Expiry |
| **until the end of your next turn** | expires during End Expiry |
| **until the start of the next round** | expires at Round Begin |
| **until the end of the round** | expires at Round End |
| **once per round** | refreshes at Round Begin unless explicitly anchored differently |
| **Emotion Window** | uses the Gifted-specific Emotion Window, not the round boundary |
| **Sustained** | persists according to its own ending conditions and does not imply an automatic tick |

New rules should avoid bare **"for 1 round"** wording when a start/end anchor would be clearer.

## Refinement boundary

This file locks the current combat clock:

```text
Combat begins
→ establish participation/awareness
→ roll Initiative
→ establish order

Round Begin
→ round expiries
→ Guard refresh
→ Dodge Pressure reset
→ Reaction/per-round refresh
→ round-start effects

Character turn
→ start expiry
→ Regeneration Step
→ start-of-turn effects
→ establish Turn AP, derived Tempo, and Movement Allowance
→ start-of-turn choices
→ normal actions/movement
→ end-of-turn effects
→ end expiry
→ cleanup

During/between turns
→ Guard / Dodge
→ Reactions and nested response windows
→ atomic reserved Interceptions
→ Opportunity Response / Opportunity Attacks
→ explicit Interrupts

Round End
→ round-end effects
→ round-end expiries
→ next round
```

The following remain deliberately unresolved or only minimally integrated here:

- specialized Charge variants beyond locked [Rapid Advance and Charge v0](rapid-advance-and-charge-v0.md), exact Climb/Swim MP costs, Catch Grip, jumping/falling, detailed water hazards, squeezing, size exceptions, flight, and other still-undefined special movement modes;
- weapon-family Reach assignments beyond the ordinary adjacent baseline;
- exact weapon/maneuver modifiers for deliberate Disrupting Interceptions;
- complete surprise/unaware rules;
- hazard values and physical-hazard procedures;
- conditions.
