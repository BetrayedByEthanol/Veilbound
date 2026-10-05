# Initiative and Round/Turn Procedure

> Canonical Veilbound combat-procedure baseline. This file locks initiative, the round/turn skeleton, core resource refresh timing, regeneration timing, and universal duration anchors. Detailed reaction/interception priority, full declaration procedure, movement/reach, opportunity attacks, surprise, and hazard values remain separate refinement work.

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

Out-of-turn responses, reserved effects, defensive responses, and other interruptions may occur when their triggers permit. Their detailed declaration and priority procedure remains separate refinement work.

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

Determine the character's Attack-unit allotment for this turn from Physical Tempo and explicit modifiers.

Attack Units are **turn resources**, not round resources.

A Full Action continues to consume the character's entire granted Attack-unit allotment for that turn.

Movement allowance will also be established here once the movement subsystem is locked.

### 5. Start-of-turn choices

Resolve choices that occur after ordinary start-of-turn housekeeping and before normal actions.

Current examples include:

- choosing offensive or defensive dual-wield use;
- the Gifted Emotion Establishment Step.

The Gifted procedure remains exactly as defined in [Gifted Foundation](../08-archetypes/gifted.md): it occurs after ordinary start-of-turn housekeeping and before normal actions, and may spend an Attack Unit from the upcoming turn when its rules require it.

### 6. Normal turn

The character may spend Attack Units, take a Full Action where legal, use techniques, make attacks, reserve eligible actions/effects for Interception, and move as permitted by the movement rules.

This file does **not** require a character to pre-declare an entire turn.

The exact rules for splitting movement, action declaration, trigger priority, and other sequencing choices remain future refinement.

### 7. End-of-turn effects

Resolve effects explicitly authored for the end of this character's turn.

### 8. End expiry

Expire effects that explicitly last until the end of this character's turn.

### 9. Cleanup

Unspent Attack Units are lost.

Reserved actions/effects that remain valid continue only for their defined reservation window.

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
4. use remaining throughput toward the active Wound Repair Requirement;
5. prevent, offset, or medically control additional bleeding or similar ongoing losses where the relevant rules permit;
6. once the wound is repaired, remaining throughput may restore HP;
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

## Reactions, Guard, Dodge, and Interception

The current baseline distinctions are:

- **Reaction:** one Reaction per combatant, refreshed at Round Begin;
- **Guard:** uses Guard capacity and does not consume the Reaction;
- **Dodge:** does not consume the Reaction and instead accumulates Dodge Pressure;
- **Interception:** remains a timing mechanic that reserves an otherwise valid action/effect and names a trigger.

Unless a rule gives a different reservation window, a reserved Interception remains available until the start of the reserving character's next turn. If the trigger never occurs, the reserved action/effect is lost.

When an out-of-turn response resolves, resolve that response before resuming the triggering event if the triggering event is still legal.

This is the current baseline only. Detailed trigger declaration, competing-response priority, simultaneous reactions, opportunity-attack integration, and broader interruption procedure remain explicit follow-up work.

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
→ establish Attack Units
→ start-of-turn choices
→ normal actions/movement
→ end-of-turn effects
→ end expiry
→ cleanup

During/between turns
→ Guard / Dodge
→ Reactions
→ reserved Interceptions
→ future opportunity attacks and other interruptions

Round End
→ round-end effects
→ round-end expiries
→ next round
```

The following remain deliberately unresolved or only minimally integrated here:

- detailed Reaction declaration and competing-trigger priority;
- detailed Interception declaration/priority refinements;
- general turn-declaration rules beyond the timing skeleton;
- movement allowance, splitting movement, reach, and engagement;
- opportunity attacks;
- complete surprise/unaware rules;
- hazard values and physical-hazard procedures;
- conditions.
