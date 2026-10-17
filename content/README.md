# Structured game content

This directory will contain canonical machine-readable game objects.

Planned collections:

- `pillars/`
- `aspects/`
- `techniques/`
- `equipment/`
- `conditions/`
- `archetypes/`
- `specializations/`
- `backgrounds/`
- `origins/`
- `creatures/`
- `tables/`

Content should validate against schemas in `/schemas` and use stable IDs.

The repository currently defines only the initial schema contracts; large-scale content migration should happen after those contracts are reviewed.

### B06 provisional benchmark content

- [B06-EN-01 Firebound Sentry](creatures/b06-firebound-sentry.v0.json) is a **reviewable enemy test fixture**, not an automatically canonized bestiary creature. Its mutually exclusive `B06-AT-01` normal sword and `B06-AT-02` already-enchanted Conjure Flame sword profiles use existing rules; neither grants a toxin weapon or additional attack. Contract: [enemy benchmark v0](../schemas/b06-enemy-benchmark-v0.schema.json).
