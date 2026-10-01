# Contributing to Veilbound

## Change flow

1. Work from a branch.
2. Keep design discussion separate from canonical rule/content changes.
3. When a design decision is locked, update the canonical file that owns that rule.
4. Update or add structured content when software-facing data changes.
5. Add validation/tests when a rule can be checked mechanically.
6. Open a pull request describing what changed and what remains provisional.

## Status language

Use these labels in design/audit material when useful:

- **LOCKED** — accepted as the current rule/structure.
- **PROVISIONAL** — usable current design, still expected to change through calibration/testing.
- **INHERITED** — retained from an older/external rules assumption and not yet replaced natively.
- **CONFLICTING** — two or more current sources disagree.
- **MISSING** — required rule/content does not yet exist.

Canonical rule files should prefer direct normative language over carrying audit labels inline everywhere.

## Canonical vs design material

- `docs/design/`: reasoning, audits, experiments, discarded alternatives.
- `docs/rules/`: player/GM-facing canonical rules.
- `docs/world/`: canonical world/setting reference.
- `content/`: structured canonical objects consumed by software.
- `schemas/`: contracts for those structured objects.

## Content IDs

Structured content should use stable, human-readable IDs such as:

```
pillar.order
aspect.order.stability
technique.fire.conflagration.flame-mantle
condition.dying
item.weapon.arming-sword
```

IDs should not encode mutable presentation text or version numbers.
