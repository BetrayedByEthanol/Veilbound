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

Veilbound is in its **level 1–3 tabletop MVP implementation and verification phase**. The G0–G7-F source-native combat and calibration pilot infrastructure is merged, but the **12 Archetype × Focus builds and complete representative encounters are not yet certified**. The first web application remains a deliberately limited reference shell; production character building, campaign state, multiplayer and VTT-style features are deferred.

For the **current development roadmap, completed milestones, remaining priorities and six strict MVP exit gates**, use the [active roadmap and MVP readiness register](docs/design/veilbound-roadmap-and-mvp-readiness.md). Its planning status does not override canonical rules.

See [docs/README.md](docs/README.md) for documentation conventions and [CONTRIBUTING.md](CONTRIBUTING.md) for change workflow.
