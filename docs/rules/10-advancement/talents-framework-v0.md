# Talents — B07 MVP Framework v0

> **B07 structural design baseline; numerical progression and individual effects PROVISIONAL PLAYTEST CONTENT.** Talents are optional selections that customize a character's methods, costs, timing and capabilities across mundane and Veil-assisted play. The first 32 defined examples are in [Level 1–5 Talent Catalogue v0](talents-level-1-5-v0.md). Nothing on these pages automatically turns an unauthored Veil technique, crafting recipe, equipment property or social subsystem into a usable effect.

## Purpose and identity

A **Talent** is one player-selected character development, distinct from:
- **Archetype Features:** automatic identity/progression features of Priest, Scholar, Gifted or Anointed;
- **Pillar/Aspect Techniques:** authored expressions with their own magical access, tier and cost;
- **Universal Veil Procedures:** Pillar-independent Inspection/Translocation with separately authored access and cost;
- **Weapon Style Refinements:** one nominated weapon family, bought with Weapon Development Points;
- **Discipline Refinements:** a specific Learned Discipline, bought with Discipline Development Points.

Talents may be **mundane**, **Veil-assisted**, or **mixed**; **passive**, **activated**, **triggered**, or **procedural**. An Archetype Talent is a *general Talent with an Archetype prerequisite*, **not** an extra automatic class feature. Multiple tags can describe the same Talent; category labels do not impose Focus restrictions.

**Design priority:** meaningful trade-offs, alternative ways to use already-legal actions, improved reliability of bounded tasks, or a genuinely specialized capability. Plain static bonuses are permitted but should be exceptional and limited. A Talent may modify the **mechanics** of an action but does not retroactively declare ordinary physically plausible activities to be Talent-exclusive. If the activity itself is possible under core rules, anyone can attempt it; Talents improve an explicitly specified interaction.

## Acquisition — Focus-biased, separate from Training

**LOCKED direction:** Low Focus gains more Talent selections than Medium, and Medium more than High. The Talents come from **one shared catalogue** unless explicit individual prerequisites apply. Low Focus may select magical/knowledge Talents and High Focus may select physical/professional Talents; Focus is not an implicit category ban.

**PROVISIONAL B07 level 1–5 schedule** (one selection at each indicated level):

| Level | High Focus | Medium Focus | Low Focus |
|---:|:---:|:---:|:---:|
| 1 | +1 | +1 | +1 |
| 2 | — | — | +1 |
| 3 | — | +1 | +1 |
| 4 | — | — | — |
| 5 | +1 | +1 | +1 |
| **Total through 5** | **2** | **3** | **4** |

The previously discussed **5 / 8 / 11 total choices by level 20** (High / Medium / Low) is a **design target, not an adopted level-6–20 award schedule**. Later distribution must be checked against Specialization (6–15), Mastery (16–20), actual authored magic, and total build-choice pressure.

- Talent selections are **not purchased** with Weapon Development or Learned Discipline points, VP, Destiny, or Ability increases. Existing starting Weapon/Discipline budgets and their gates remain unchanged.
- One selection buys **one** listed Talent. A Talent cannot be chosen twice unless its own entry explicitly allows repetition and states what changes.
- The character must meet the entry's **minimum character level and other prerequisites when choosing it**; there is no universal Archetype or Focus prerequisite.
- Selections can be **saved** until a later level or until an authored prerequisite becomes available. Saved selections may be spent later, but the character then uses the current prerequisites and available catalogue. Selections cannot be borrowed in advance.
- The exact **retraining/respec procedure is deferred**; do not assume free swaps between fights, preparation cycles, or level-ups.
- Talents have no automatic VP cost merely because they are Veil-assisted. They have the **explicit** cost given in their entry.

## Entry contract

Each selectable entry in the v0 catalogue states:

| Field | Requirement |
|---|---|
| ID and name | Stable `TAL-...` identifier and readable name |
| Source | Combat/physical, spellcasting, Archetype or utility; often with extra purpose tags |
| Minimum level | Character level at selection; other prerequisites listed separately |
| Mode and nature | Passive / activated / triggered / procedural and mundane / Veil-assisted / mixed |
| Trigger and cost | Exact timing; AP/Reaction/MP/VP/Vigor (if applicable), or none |
| Effect | Named underlying rule being changed, effect amount, eligibility and how it resolves |
| Limits | Refresh interval, targets, non-stacking, forbidden interactions, failure or loss |

Level gates and individual numerical parameters in the B07 catalogue remain **provisional**, even when a complete v0 effect is presented for tabletop testing.

## Mechanical integration and guardrails

### Actions, Reactions and Interceptions

Follow [Turn AP and Tempo](../05-combat/action-categories-and-physical-tempo.md) and [Initiative and Round Structure](../05-combat/initiative-and-round-structure.md) unless an entry expressly replaces a *named part* of an action's cost or timing.

- **One Reaction per round** remains the default shared resource. A Talent usable as a Reaction does **not** create a second Reaction; it competes with Opportunity Response, Reactive Intervene, and other Reaction effects.
- A Talent changing **Aim** still uses [Aim v0](../05-combat/aim-v0.md): specified target, delivery profile and difficulty source; actual Aim mitigation at most 4; one active Aim; carry and breaking conditions except specifically overwritten.
- Prepared **Interception** remains one atomic reserved legal action or MP commitment with a meaningful, non-guaranteed trigger. Talents may expressly change *which trigger or expiry applies* but not bundle otherwise-separate Aim and Attack into one action or ignore one-attack-sequence-per-target.
- An effect reducing an AP cost must say *which* action it reprices and whether the reduction is one use or persistent. Nothing silently increases Turn AP, Physical/Projection Tempo, Guard capacity, or out-of-turn permissions.

### VP, Veil effects and Archetypes

- Keep **Available / Committed / Spent VP** distinct. A discount applies only to its stated component and may not lower a Spent VP cost below its listed minimum; switching/rerouting never refreshes spent limited effects.
- A bonus to a technique's **roll** is **not** +1 Veil Control and does **not** increase the [level-multiplied Standard Veil Control packet](../07-veil-magic/technique-tiers-and-expression.md#standard-veil-control-scaling).
- Talents cannot exceed normal technique-tier ceilings, grant another Pillar/Aspect link or bonded Aspect, transform a Universal Veil procedure into a Pillar technique, or automatically override an Archetype's preparation, Accord, emotional, Composite or Destiny boundaries.
- **Known/prepared technique Talents need actual authored, eligible techniques.** They do not populate the missing Pillar catalogue; a player may save the selection rather than buy an unusable entry.

### Weapon Training and Learned Disciplines

- [B04 melee-only half-transfer](../05-combat/weapon-training-and-refinements-v0.md#melee-only-half-transfer) and direct-investment prerequisites remain authoritative; a Talent modifying transfer must state its calculation and cannot silently include Bow/Crossbow.
- Talents do **not** add a general +1 Training, create broad all-purpose Perception/Persuasion/Investigation skill bonuses or stack a second Training on a single check.
- A bounded reroll/diagnostic change is not an unlimited retry, a guarantee of information absent from the scene, or an invitation to ignore [Take 10 / Take 20](../01-core-resolution/core-resolution.md). No reroll reverses an irreversible action or gains knowledge the character could not plausibly access.
- A Talent that merely improves one nominated *weapon-family maneuver* normally belongs to **Weapon Style Refinements**. A Talent whose sole benefit is upgrading a nominated *professional skill* may instead become a Discipline Refinement when those catalogues are authored. V0 examples deliberately test **cross-system actions, timing, resilience, or narrowly authored utility** without consuming those refinement budgets.

### Limits and stacking

- A **once-per-round** Talent refreshes at Round Begin; a **once-per-turn** Talent applies once to the owner's turn; a **once-per-6-hour** Talent refreshes after a completed 6-hour interval. Explicitly authored other windows take precedence.
- One named Talent can be applied at most once to the same check, attack, Aim preparation, defensive response, or regeneration step unless the entry says otherwise. Two Talents do not each grant a second full effect merely by referring to the same triggering event: apply distinct legal modifications at their explicitly defined times. No infinite VP refunds, stacked free attacks, per-target full scaling packets, or re-trigger-on-reroll loops.
- Expenditure occurs when the Talent says it does. A spent Reaction or VP is not refunded when the triggering event subsequently becomes invalid unless expressly stated.
- **Unavailable content remains unavailable:** an entry requiring a spell, Active Signature, rite or specific enhancement can be selected only if the character can actually access a valid authored example.

## MVP and deferred scope

**MVP included:** ordinary combat, repositioning, defense, Aim, limited regeneration tradeoffs, specific Veil technique enhancements, Archetype repertoire/preparation, knowledge checks, navigation, and mundane field utility.

**OUT of MVP / NOT SELECTABLE in v0:** magical item creation; gem sockets; permanent enchantments; magical potion manufacture; magic-item economic bonuses; unauthored crafting projects. Their meaningful Talent effects require **magical equipment, material accessibility, item powers and crafting economics first**, and should enter at later progression only after those systems are supported. Ordinary Smithing, Medicine, Alchemy and field repairs remain available through existing Learned Disciplines; Talents are not required to do ordinary professional tasks.

**B07 playtest watchlist:** low-level choices per build and Focus; guard and movement efficiency versus Physical Tempo; Reactive Aim timing versus Interception; VP discounts and healing cadence; bounded rerolls under pressure; single-technique specialization versus high-level Veil Control scaling; Archetype known/prepared counts. These numbers can change after tests; none replaces locked core rules by implication.
