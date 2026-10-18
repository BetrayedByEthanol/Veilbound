# Content schemas

Schemas define the contracts used by Veilbound's structured content and future rules tooling.

Initial schemas are intentionally minimal. They establish identity, naming, visibility, status, tags, and the first domain-specific fields without prematurely encoding every unfinished subsystem.

As systems become canonical, extend the schemas through reviewed migrations rather than placing arbitrary one-off fields into content files.

## B06 benchmark fixtures

- [Enemy / creature benchmark schema v0](b06-enemy-benchmark-v0.schema.json) — **extended after merged PR #84** to cover ordinary non-Archetype humans, beasts, Veil-touched creatures, dragons, Raised/Turned undead and Veil Manifestations. Player-derived enemies still require their own progression; non-Archetype creatures need separately authored action and attack sources. Existing Firebound attack numbers remain unchanged. **JSON-schema validity alone does not authorize a technique or monster ability.**
- [Initial bestiary index schema v0](b06-bestiary-index-v0.schema.json) — standalone machine-checkable contract for **14 creature entries**, distinct from executable encounter/stat-block records. Current review adds optional explicit **rigid footprint** and **encounter guidance** (contextual frequency, unrated CR, qualitative role, party-size-and-level matchup tests), without inventing a numerical balance scale. Its shared taxonomy definitions are kept identical to those of the enemy schema by [regression tests](../tests/test_b06_creature_types_v0.py).
- First example: [B06-EN-01 Firebound Sentry](../content/creatures/b06-firebound-sentry.v0.json), with ordinary sword and legally reserved Conjure Flame modes. See [B06 design record](../docs/design/b06-enemy-benchmark-schema-and-attack-profiles-v0.md) and [stdlib regression tests](../tests/test_b06_enemy_benchmark_v0.py).
- Second example (B06-local candidate): [B06-EN-02 Ordinary Human Soldier](../content/creatures/b06-ordinary-human-soldier.v0.json), **no Archetype or personal VP**, a sword/shield/brigandine loadout and an explicitly provisional **24-AP non-Focus Physical Action / Vitality-only regeneration** template. See the [design rationale](../docs/design/b06-ordinary-human-soldier-template-v0.md) and [regression tests](../tests/test_b06_ordinary_human_soldier_v0.py).
