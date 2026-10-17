# Content schemas

Schemas define the contracts used by Veilbound's structured content and future rules tooling.

Initial schemas are intentionally minimal. They establish identity, naming, visibility, status, tags, and the first domain-specific fields without prematurely encoding every unfinished subsystem.

As systems become canonical, extend the schemas through reviewed migrations rather than placing arbitrary one-off fields into content files.

## B06 benchmark fixtures

- [Enemy benchmark schema v0](b06-enemy-benchmark-v0.schema.json) — Draft 2020-12 structural contract for a **design/test-only** Level-1–3 opponent: exact Abilities, VP states, defenses, equipment, lawful conditional attack profiles, and explicitly sourced optional toxin delivery. **JSON-schema validity alone does not authorize a technique, monster power or combat rule.**
- First example: [B06-EN-01 Firebound Sentry](../content/creatures/b06-firebound-sentry.v0.json), with ordinary sword and legally reserved Conjure Flame modes. See [B06 design record](../docs/design/b06-enemy-benchmark-schema-and-attack-profiles-v0.md) and [stdlib regression tests](../tests/test_b06_enemy_benchmark_v0.py).
