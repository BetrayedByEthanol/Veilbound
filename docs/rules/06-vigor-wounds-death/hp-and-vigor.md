# HP and Vigor

> Canonical extraction from Core Rules Audit v34. Values explicitly retained as calibration baselines remain identified as such.

## Physical integrity and reserve

**Max HP = 10 + Vitality**

HP represents physical integrity and does **not** scale with level.

**Max Vigor = (10 + Vitality) × Level**

Vigor represents the character's finite Veil-supported regenerative reserve. It is not a second HP shield. Level increases how much punishment a character can recover from rather than making the body itself progressively harder to injure.

Low Focus does not automatically gain additional Vigor capacity.

## Natural regeneration

Natural HP regeneration resolves once per character round after all damage taken before that regeneration step.

Unless another rule changes the conversion, restoring 1 HP consumes 1 Vigor.

Current adopted throughput baseline:

```
Regeneration throughput = max(Vitality, 0) + Focus Rate
```

- High Focus: +1
- Medium Focus: +2
- Low Focus: +3

These throughput values remain subject to encounter calibration.

Because regeneration resolves only once each round, multiple attacks can overwhelm current HP before regeneration occurs even when substantial Vigor remains.

## Anti-regeneration effects

Valid mechanics may include:

- direct Vigor damage;
- reduced regeneration throughput;
- temporary regeneration suppression;
- increased Vigor cost per HP restored;
- blocking external Vigor restoration;
- temporary maximum-Vigor reduction.

## Wound triggers

Ordinary hits do not normally create persistent wounds. A wound occurs only when:

1. a Called Shot successfully qualifies for a wound;
2. a Devastating Critical occurs; or
3. the target reaches 0 HP.

The detailed wound tables and some severity thresholds remain calibration content and should not be treated as fully finalized merely because the trigger framework is locked.
