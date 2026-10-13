# October 2026 Review Follow-ups

This design note records classification changes from the post-Turn-AP automated review. Canonical rule files remain the source of truth.

## Lore status

### Pillar Accord and Scholar access

**Status: READY / CANONICAL CLARIFICATION APPLIED**

Priest Accord increasing Prepared Prayer capacity is not evidence that a conscious Pillar grants permission while Scholars somehow bypass it.

- Scholars technically reproduce stable Aspect patterns.
- Priests cultivate a sustained relational coherence with one Pillar.
- Higher Accord means the Priest can stably maintain more prepared expressions of that Pillar pattern.

The canonical explanation now lives in `docs/rules/08-archetypes/priest.md`.

### Miracle Petition metaphysics

**Status: MECHANISM OPEN / TERMINOLOGY NARROWED**

The exact metaphysical mechanism of a successful Miracle Petition remains unresolved.

Until deliberately settled, use:

- **transient localized Pillar reinforcement**; or
- **localized pattern amplification**.

Do not describe an ordinary successful Petition as a **Pillar surge**. That term is reserved for the exceptional surge phenomenon associated with Anointed origin.

## Legacy migration classification

The following material is not one undifferentiated "Ready" bucket.

### Ready or close to ready

- **48 Aspect identities** — **migrated to canonical lore** in [Aspect Identities and Boundaries](../world/aspect-identities-and-boundaries.md) by an explicit B05 author decision; machine-readable `content/aspects/` migration remains separate.
- **Aspect boundary rulings** — positive/negative metaphysical domains are **canonical lore** in the same reference. Their technique-level costs, permissions and mechanics remain to be authored.
- **Cultural unity across Pillars** — ready as setting lore.
- **Setting texture, places, institutions, and cultural examples** — suitable for migration as **provisional lore**, after checking for contradictions with current Pillar metaphysics.
- **Base Archetype rarity** — already substantially canonical: Priest ~1/100, Scholar ~1/1,000, Gifted ~1/100,000, Anointed ~1/1,000,000.

### Decision / mechanics — not safe automatic migration

- **Anointed locality rationale** such as "there should be no other Anointed nearby" — requires a deliberate setting/mechanics decision; current rarity does not imply a local-exclusion rule.
- **Multi-pathing / acquiring additional Archetype paths** — mechanical progression decision. Gifted and Anointed origins are constrained, but the general multi-path procedure is not canonical.
- **Gifted complex-emotion resolution** — mechanical subsystem requiring reconciliation with the current Gifted Emotion Window, Conduit, Anchor, and Instability structure.
- **Mission granularity and numeric Destiny rewards** such as minor/major/full recovery — calibration/mechanics, not lore. Current Anointed canon already uses provisional elapsed-time Destiny recovery plus an unspecified benefit from meaningful Mission Fulfillment.

### Deliberate decisions still required

- **executable resurrection mechanics** — Life/Restoration may exceptionally restore the dead, but rarity, quest/material requirements, effect limits, costs and resolution remain to be authored;
- what ends or breaks sustained effects;
- allied-Pillar access and legacy Divine Sense concepts for Priests;
- armor limitations by Focus;
- group and ritual casting;
- the final universal maneuver list.

### Terminology cleanup

- `Liberty` vs legacy `Liberation`;
- moralized vocabulary such as `Divine`, `Holy`, `Radiant`, or `Protection from Evil/Good` where it conflicts with morally neutral Veil metaphysics;
- specialization names or descriptions that imply a human-like speaking Pillar where direct Pillar communication remains unresolved.

## Turn-AP migration cleanup

The legacy Called Shot statement that it consumes an entire "Attack action regardless of normal attack count" is superseded.

Called Shot remains an unresolved maneuver and must receive an explicit **Turn AP or Full Action cost** during the maneuver/weapon pass.

[Aim v0](../rules/05-combat/aim-v0.md) is now canonical as a **different** separately paid Physical Action: declaring a target and body-part objective does not make a Called Shot legal, grant a wound, or provide an Interrupt. Called Shot difficulty and wound qualification still need native rules. **[Unified Firing Lane v0](../rules/05-combat/unified-firing-lane-v0.md)** now authors ordinary projectile **shooting past intervening creatures and friendly-fire risk** with one highest obstruction and conditional collateral accuracy; **mere melee engagement remains no penalty**. Living Screen values and protective geometry/critical tuning are a watch, not missing foundational procedures. [Protective Intervene v0](../rules/05-combat/protective-intervene-v0.md) now independently authors **Reactive one-Reaction** and **Prepared reserved-MP** Shield Guard/Body Take Hit against one otherwise successful attack. **[Cover and Line of Fire v0](../rules/05-combat/cover-and-line-of-fire-v0.md)** now independently authors directional physical cover, +2/+4/+6/+8 difficulty, cover hits, and illegal full blockage. Aim v0 may reduce **one** selected positive Cover Difficulty by up to 4; it does not bypass solid obstacles. Cover damage/penetration and concealment remain unresolved; protective **Shield Guard and deliberate Body Take Hit for another** now use Protective Intervene v0's explicit legal timing, resource and physical positioning restrictions; normal Dodge still does not protect someone else. Incidental enemy/ally collisions now use Unified Firing Lane v0.
