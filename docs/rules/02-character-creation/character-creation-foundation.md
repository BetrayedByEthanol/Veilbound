# Character Creation Foundation

> Canonical extraction from Core Rules Audit v34. Veilbound does **not yet have a complete executable character-creation procedure**. This page records the portions that are currently defined and makes the remaining gaps explicit instead of filling them with 5e defaults.

## Current character framework

A player character is currently defined by these major mechanical layers:

1. **Archetype** — Priest, Scholar, Gifted, or Anointed.
2. **Focus** — High, Medium, or Low.
3. **Nine Abilities** — Strength, Agility, Precision, Intellect, Awareness, Presence, Vitality, Veil Affinity, Veil Control.
4. **Trainings** — narrow learned expertise using the +0 to +4 training scale.
5. **Archetype-specific access choices** — such as a Priest's chosen Pillar, a Scholar's learned techniques, a Gifted's emotion-to-Aspect links, or an Anointed's bonded Aspect/Mission/Birth Imprint.
6. **Derived resources and combat values** — HP, Vigor, VP, Physical Tempo, and other values whose rules are already defined.
7. **Equipment** — currently only partially defined.
8. **Background/origin/social starting position** — currently missing as a complete subsystem.

## Step 1 — Choose Archetype

Choose one of the four base Archetypes:

- [Priest](../08-archetypes/priest.md)
- [Scholar](../08-archetypes/scholar.md)
- [Gifted](../08-archetypes/gifted.md)
- [Anointed](../08-archetypes/anointed.md)

Archetype defines the character's **relationship to and access route into the Veil**.

## Step 2 — Choose Focus

Choose:

- **High — Projection**
- **Medium — Routing**
- **Low — Embodiment**

See [Focus: Veil Expression](../09-focus/focus.md).

Focus does not replace Archetype. The two choices combine to produce one of twelve base foundations.

## Step 3 — Allocate Abilities

Use the level-1 generation rules from [Abilities and Training](abilities-and-training.md).

All nine abilities begin at **-2**.

Spend **28 ability points** using the cumulative costs:

| Final score | Cost |
|---:|---:|
| -2 | 0 |
| -1 | 1 |
| 0 | 2 |
| +1 | 3 |
| +2 | 5 |
| +3 | 7 |
| +4 | 10 |

The normal creation cap is **+4**.

## Step 4 — Choose Trainings

The training engine is defined, but the audit does **not** yet define a final number of starting Training selections/points.

Until that allocation rule exists, a complete rules-legal level-1 character cannot be finalized solely from the canonical rules.

Do not import 5e proficiency counts or background proficiencies to fill this gap.

## Step 5 — Make Archetype-specific choices

### Priest

Choose one Pillar. Priest access is constrained to that Pillar's three Aspects and its Prepared Prayer structure.

Exact starting Prepared Prayer counts remain provisional.

### Scholar

Choose individually learned techniques from allowed Pillars/Aspects.

Exact starting repertoire counts remain provisional.

### Gifted

Create exactly eight permanent emotion-to-Aspect links:

- one for each core emotion;
- each link uses a different Aspect;
- each link comes from a different Pillar.

The full compatibility matrix remains to be migrated into structured content.

### Anointed

Define:

- one bonded Pillar/Aspect;
- a broad lifelong Mission;
- a Birth Imprint shaped by the surge that created the bond.

Exact Signature/Authority packages remain Aspect-specific content work.

## Step 6 — Calculate derived durability/resources

Use the currently promoted native formulas.

### HP

```
Maximum HP = 10 + Vitality
```

### Vigor

```
Maximum Vigor = (10 + Vitality) × Level
```

At level 1, this is equal to Maximum HP.

### VP

Use Focus:

- High: `max(1, 6 + Veil Affinity) × Level`
- Medium: `max(1, 4 + Veil Affinity) × Level`
- Low: `max(1, 2 + Veil Affinity) × Level`

See [Volition Points](../07-veil-magic/volition-points.md).

### Physical Tempo

At levels 1–3 all Focuses begin at:

- **1 Attack**
- **1 Guard**

See [Action Categories and Physical Tempo](../05-combat/action-categories-and-physical-tempo.md).

## Step 7 — Equipment

Core weapon and armor baselines exist, but the complete equipment system does not.

Currently unresolved:

- final starting packages;
- full adventuring gear;
- currency/economy;
- prices and availability;
- ammunition/supply procedure;
- encumbrance/carrying capacity;
- complete rune/magic-item system.

Do not treat a 5e equipment package or gold table as canonical Veilbound equipment.

## Character-creation systems still missing

The audit explicitly leaves these areas incomplete:

- background/origin mechanics;
- social origin and starting contacts;
- starting Training allocation;
- complete starting equipment packages;
- complete native defense/save mapping, including non-spell hazards and spell defenses;
- some spell-derived formulas;
- final repertoire/preparation counts for several Archetypes;
- a final shared procedure for every remaining derived sheet value.

This means the **character framework is substantially defined**, but character creation is not yet a closed end-to-end rules procedure.
