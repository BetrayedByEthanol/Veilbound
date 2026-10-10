# Turn Action Points and Tempo

> Canonical Veilbound turn-economy foundation. Initiative, declaration, Reactions, Interception, interruption timing, Attack Sequences, and Opportunity timing are defined in [Initiative and Round/Turn Procedure](initiative-and-round-structure.md). Ordinary grid movement, Reach, threatened space, and movement-based Opportunity triggers are defined in [Movement Foundation](movement-foundation.md).

## Turn Action Points

Each character receives one shared **Turn Action Point (Turn AP)** pool on their turn.

```text
Turn AP = min(120, 30 + 6 × (Level - 1))
```

Turn AP is established at the start of the character's turn and is a **turn resource**, not a round resource. Unspent Turn AP is lost during turn cleanup.

| Level | Turn AP |
|---:|---:|
| 1 | 30 |
| 2 | 36 |
| 3 | 42 |
| 4 | 48 |
| 5 | 54 |
| 6 | 60 |
| 7 | 66 |
| 8 | 72 |
| 9 | 78 |
| 10 | 84 |
| 11 | 90 |
| 12 | 96 |
| 13 | 102 |
| 14 | 108 |
| 15 | 114 |
| 16–20 | 120 |

The shared pool means physical and projected actions compete directly for the same finite turn. Focus changes **how efficiently** that pool can be expressed, not how many separate action pools the character receives.

## Focus action costs

Tempo-scale actions use one of three AP cost classes.

| Focus | Physical Action | Projection Action | General Tempo Action |
|---|---:|---:|---:|
| **High — Projection** | 30 AP | 20 AP | 24 AP |
| **Medium — Routing** | 24 AP | 24 AP | 24 AP |
| **Low — Embodiment** | 20 AP | 30 AP | 24 AP |

### Physical Action

A **Physical Action** is ordinary physical combat activity whose cadence should follow embodied physical tempo, including an ordinary weapon attack and other actions explicitly authored with the Physical Action cost. [Aim v0](aim-v0.md) is a separately paid Physical Action preparing one specified future ranged attack; it does **not** fire, grant a bonus attack, change Physical Tempo, or pay for the later attack.

### Projection Action

A **Projection Action** is an outward/projected Veil technique authored at tempo-action scale. It uses the Projection Action cost for the character's Focus.

Projection cost does not grant universal repeatability. A technique may still be once per turn, limited by Expression Cadence, or otherwise restricted by its own rule.

### General Tempo Action

A **General Tempo Action** costs **24 AP** regardless of Focus.

Use this for turn-economy actions whose timing should not inherently favor Embodiment or Projection, such as setup, reconfiguration, or similar neutral tempo costs when a rule explicitly assigns the General Tempo Action cost.

### Full Action

A **Full Action** requires the character's **entire Turn AP allotment for that turn to remain available** and consumes that entire allotment.

A Full Action therefore occupies the whole AP-based action economy at every level. It does not cost a fixed 120 AP.

A Full Action is not permission to bundle several ordinary tempo actions together. Only an action/effect explicitly authored as a Full Action uses this category.

## Derived tempo

Physical and Projection Tempo are derived values, not separate spendable pools.

```text
Physical Tempo =
floor(Turn AP / Physical Action Cost)

Projection Tempo =
floor(Turn AP / Projection Action Cost)
```

They represent the maximum number of corresponding ordinary tempo actions the character could perform in a turn **if the entire Turn AP pool were spent only on that action class**.

Mixed turns require no conversion rule: pay each action's AP cost from the same Turn AP pool.

At the mature 120-AP cadence:

| Focus | Physical Tempo | Projection Tempo |
|---|---:|---:|
| High | 4 | 6 |
| Medium | 5 | 5 |
| Low | 6 | 4 |

Examples at 120 AP:

- High Focus: Physical actions cost 30 AP; Projection actions cost 20 AP.
- Medium Focus: both cost 24 AP.
- Low Focus: Physical actions cost 20 AP; Projection actions cost 30 AP.

Unused remainder AP does not create a partial action.

## Guard and Opportunity capacity

Normal Guard capacity is locked to derived Physical Tempo:

```text
Guard Capacity = Physical Tempo
```

Equipment and explicit features may modify Guard capacity.

The general Opportunity framework likewise uses:

```text
Opportunity Capacity = Physical Tempo
```

Guard and Opportunity capacity are round-side resources/capacities. Spending Turn AP on Projection or General Tempo actions does **not** reduce already-derived Guard or Opportunity capacity for that round.

Dodge remains separate from Physical Tempo and is not usage-limited by this table.

## Granted bonus actions

A rule may grant an attack or other action without an additional AP cost.

Such a grant is not extra Turn AP and does not change Physical or Projection Tempo. It follows its own restrictions and still participates in procedures such as Attack Sequence declaration where applicable.

Permanent or repeatable free-action grants should remain rare because they bypass the shared Turn AP economy.

## Reactions and Sustained effects

Current non-AP action/timing categories remain:

- **Reaction:** uses the character's one Reaction. The Reaction refreshes at Round Begin.
- **Sustained:** remains active over time and normally uses Committed VP according to the effect's rules.

An effect may have an AP-based activation cost and then become Sustained.

Prepared effects are not a separate core action category. They are ordinary effects applied in advance with a defined duration.

Permanent or long-term binding into magic items is a separate future subsystem.

## Interception

Interception is a **timing mechanic**, not a separate action category and not an automatic Interrupt.

To intercept, reserve one otherwise valid action/effect or an explicitly permitted movement reservation and declare a specific trigger with a meaningful failure case.

A reservation is atomic:

- one legal AP-based action/effect, committing that action's normal Physical, Projection, or General Tempo AP cost immediately;
- one action/effect inherently defined as a Full Action **and otherwise eligible for Interception**, which requires and commits the entire Turn AP allotment; or
- one **Movement Interception**, committing a chosen amount of remaining MP under [Movement Foundation](movement-foundation.md).

A Full Action cannot be used to bundle several ordinary tempo actions into one Interception. Being a Full Action does not itself make an action reservable; a specific rule may prohibit Interception reservation. **Sprint is one such prohibited Full Action.** Reserved movement is movement, not a bundled AP-based action.

Only one reserved Interception from the same creature can release from one trigger occurrence. Multiple reservations with the same trigger apply in declaration order to successive qualifying occurrences.

Other costs such as VP are paid at the action/effect's normal resolution timing unless its own rule says otherwise.

See [Initiative and Round/Turn Procedure](initiative-and-round-structure.md) for response order, nested responses, interruption, and Opportunity timing.
