# Veilbound

Veilbound is an original tabletop role-playing game and the companion tooling used to run it.

This repository is intended to become the **single structured source of truth** for:

- the canonical rules;
- game content such as Pillars, Aspects, techniques, equipment, conditions, archetypes, and creatures;
- setting/world reference material;
- machine-readable schemas;
- the Veilbound web/PWA reference and future campaign tools;
- validation, export, and rules-engine code.

## Repository layout

```text
docs/       Human-readable rules, world material, and design records
content/    Structured canonical game content
schemas/    Schemas defining structured content contracts
apps/web/   Minimal PWA shell and future Veilbound companion UI
packages/   Shared rules/content code
tests/      Rules and content validation tests
tools/      Repository maintenance, indexing, validation, and export tools
```

## Source-of-truth rule

- `docs/design/` records design reasoning, audits, alternatives, and unresolved questions.
- `docs/rules/` contains the current canonical rules.
- `docs/world/` contains current canonical setting/lore material.
- `content/` contains canonical structured game objects intended for software consumption.
- `schemas/` defines how structured content is represented.

A design note or audit entry does **not** override canonical rules/content merely because it is newer. A rule becomes canonical only when the canonical rules/content files are updated.

## Current phase

The repository is being initialized while Veilbound's core rules are still under development. The first web application is deliberately limited to a searchable/offline-capable reference shell. Character building, campaign state, encounters, multiplayer synchronization, and VTT-style features come later.

See [docs/README.md](docs/README.md) for documentation conventions and [CONTRIBUTING.md](CONTRIBUTING.md) for change workflow.
