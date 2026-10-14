# Technique Tiers and Expression Metadata

> Canonical extraction from Core Rules Audit v34. For the subsequent **single-spell activation default, Primary/Secondary/Rider contributions, technique-specific profiles and Reserve rules**, see [Technique Structure v0](technique-structure-v0.md). This page remains authoritative for tier ceilings, numeric Veil Control constraints, expression tags and cadence.

## Universal technique tiers

Veilbound uses technique tiers **0 through 9**.

Tier 0 is available whenever the character has access to the relevant technique.

**Universal Veil Fundamentals** are a **Pillar/Aspect-independent magical category**, not an extra Pillar or Aspect. See [Universal Veil Fundamentals](universal-veil-fundamentals.md) and [Veil Translocation](veil-translocation-foundation.md). The universal tier ceiling below applies to authored **tiered** Universal procedures as well as Pillar techniques; a tier ceiling **alone** does not make an unauthored or ungated Universal technique available. Under [automatic Universal Veil acquisition](universal-veil-fundamentals.md#universal-eligibility-and-automatic-acquisition--locked), an **executable Universal procedure with an explicit minimum character level unlocks at that level**, with no technique-slot cost. **Basic Inspection (level 1) and Blink (level 3) have explicit level gates but no assigned numeric tier**; their access is not suspended pending later tier metadata. An actual assigned tier still enforces this ceiling for any future authored tiered Universal procedure.

Maximum normal technique tier is universal across Focus:

| Character level | Maximum normal technique tier |
|---:|---:|
| 1–2 | 1 |
| 3–4 | 2 |
| 5–6 | 3 |
| 7–8 | 4 |
| 9–10 | 5 |
| 11–12 | 6 |
| 13–14 | 7 |
| 15–16 | 8 |
| 17–20 | 9 |

High, Medium and Low Focus all eventually gain normal access through Tier 9. Focus changes how power is expressed and resourced; it does not impose a lower maximum technique tier.

## Veil Control scaling and damage targets

Every damaging, healing, restorative, barrier, or otherwise numerically scaling technique must state how **Veil Control** affects that technique. There is no implicit rule that every magical effect uses the same coefficient or that every magical damage packet attacks the same resource.

A technique that deals damage must identify whether each authored damage packet affects:

- **HP** — physical integrity;
- **Vigor** — regenerative reserve;
- both through separately stated packets; or
- another explicitly defined resource or wound procedure.

Do not infer a damage target merely from a technique being magical, from its Pillar, or from whether its delivery is Intrusion, Imposition, or Manifestation.

### Standard Veil Control scaling

When a technique explicitly says it uses **standard Veil Control scaling**, use:

```
Standard Veil Control packet =
max(Veil Control, 0) × Character Level
```

For a straightforward **single-target damaging technique**, add the Standard Veil Control packet once to that technique's authored **Vigor-damage packet against that target**, unless the technique explicitly defines another use for the packet.

The standard packet is not implicitly repeated per projectile, target, AP-based action, pulse, or repeated hit.

Area, multi-target, multi-hit, rapid-fire, persistent, healing, control, defensive, utility, and other effects must explicitly author their own Veil Control coefficient, parameter, distribution, or cadence. They do not inherit one full Standard Veil Control packet per target or hit merely by referring to Veil Control.

Negative Veil Control does not create negative bonus output.

### Physical Manifestation damage

When a valid Manifestation creates an independent physical phenomenon and that phenomenon harms a creature through the ordinary physical/world procedure, its ordinary physical damage affects **HP** unless an explicit technique or hazard rule says otherwise.

A technique may separately deal Vigor damage if authored to disrupt regenerative reserve. Vigor damage does not directly reduce HP.

**Standard Veil Control scaling does not automatically add damage to an HP-damage packet.** A technique that is intended to scale HP damage with Veil Control must explicitly author and calibrate that scaling rather than inheriting the Standard Vigor-damage packet.

## Persistent Expression Cadence

Any sustained, persistent, attached, embodied, invested, consecrated, routed or similar effect that can interact repeatedly with ordinary actions must declare an **Expression Cadence** for each output.

- **Continuous** — a static or persistent property. It does not multiply merely because a character can spend more Turn AP and normally remains active while the effect remains valid.
- **Rider** — a modest effect that may apply to each eligible action, attack, Guard, movement or other listed event. Rider values must be calibrated against the maximum eligible Physical or Projection Tempo capable of triggering them. **This is Rider cadence, not the distinct Rider contribution value** of [Technique Structure v0](technique-structure-v0.md#2-contribution-definitions-and-eligibility). An authored Reserved Weapon effect may trigger on each eligible successful hit without a hit count limit, but that does not waive Rider-cadence power constraints.
- **Pulse** — a stronger finite effect with an explicit refresh unit such as once per turn, round, Emotion Window or another authored interval.
- **Spend** — a stronger repeatable output that requires an explicit additional cost each time it is used, such as VP, Vigor, Destiny or another listed resource.

A full technique-scale instance of damage, healing, Vigor restoration, strong control or comparable major output must not be an unrestricted per-action Rider merely because the user can afford several AP-based actions. Use Pulse, Spend, a finite budget or another explicitly bounded cadence.

A single effect may contain multiple cadence components, but each component must state its own cadence.

## Universal technique-expression metadata

Technique entries and persistent-effect packages use a shared metadata vocabulary.

These are descriptors and permissions, not automatic bonuses.

- **[Projection]** — capable of outward/projected delivery and may interact with features that explicitly require Projection.
- **[Embodiment]** — designed to integrate into the user's body, worn/wielded equipment or ordinary physical action where a feature permits it.
- **Inward** — routes power into the user or immediately used equipment and may occupy an authored inward channel such as Weapon, Reflex, Body, Locomotion, Senses or Regeneration.
- **Consecration** — a Priest-compatible sustained blessing placed on an authored recipient or anchor.
- **Devotional Rite** — a Priest-compatible sustained inward or immediately worn/wielded expression suitable for Devotion/Exaltation mechanics.
- **Conduit Form compatibility** — defines which Medium-Gifted conduit forms may express the technique or Aspect package.
- **Investment compatibility** — defines which Vessel categories a Medium Anointed may validly invest for that interaction.
- **Cadence** — declares each persistent output as Continuous, Rider, Pulse, Spend or another explicitly bounded cadence.
- **Action cost** — when activated during ordinary turn economy, states whether the technique uses a Physical Action cost, Projection Action cost, General Tempo Action cost, Full Action, Reaction, or another explicitly authored timing/cost. **Ordinary single-spell activation defaults to one Focus-priced Projection Action (High 20 / Medium 24 / Low 30 AP)** under [Technique Structure v0](technique-structure-v0.md#4-activation-and-turn-ap--ordinary-single-spell), including activation of an authored Reserve; the individual technique may explicitly override this default. Using that AP category does **not** automatically confer the **[Projection]** expression tag.

Archetype-specific rules may add narrower qualifiers, but should not duplicate an existing universal concept without a mechanical reason. **Universal Veil** classification does not by itself authorize a Priest-specific Consecration, Scholar Composite formula, Gifted Conduit or Anointed Authority. Each such interaction requires its own explicit compatibility. Author an individual Universal operation's action, effective cost, minimum character level, effect and (if tiered) tier in its own profile. **Blink v0 and Veil Inspection v0 have authored action, cost, effect and automatic acquisition levels**; other operations, including advanced Analysis and Scrying, remain deferred.
