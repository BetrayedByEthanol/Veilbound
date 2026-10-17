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

- [B06-EN-01 Firebound Sentry](creatures/b06-firebound-sentry.v0.json), merged PR #84, is an **executable enemy test fixture**, not automatically canonized bestiary lore. Its `B06-AT-01` sword and `B06-AT-02` enchanted sword still use the same locked mechanics; it now links to the shared creature taxonomy. Contract: [extended enemy benchmark v0](../schemas/b06-enemy-benchmark-v0.schema.json).
- [Initial 14-entry B06 bestiary](creatures/b06-initial-bestiary-v0.json) — **design-only concepts**, with one currently executable Sentry and thirteen **not yet executable** creatures including non-Archetype humans, natural/Veil beasts, non-playable Elves/Orcs/Goblins, Dwarf TBD, dragons, Raised/Turned undead, spirits and Pillar surge manifestations. [Bestiary index schema](../schemas/b06-bestiary-index-v0.schema.json); [design reference](../docs/design/b06-creature-types-and-initial-bestiary-v0.md).
