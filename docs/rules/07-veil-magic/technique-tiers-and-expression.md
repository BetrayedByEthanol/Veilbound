# Technique Tiers and Expression Metadata

> Canonical extraction from Core Rules Audit v34.

## Universal technique tiers

Veilbound uses technique tiers **0 through 9**.

Tier 0 is available whenever the character has access to the relevant technique.

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

The standard packet is not implicitly repeated per projectile, target, Attack Unit, pulse, or repeated hit.

Area, multi-target, multi-hit, rapid-fire, persistent, healing, control, defensive, utility, and other effects must explicitly author their own Veil Control coefficient, parameter, distribution, or cadence. They do not inherit one full Standard Veil Control packet per target or hit merely by referring to Veil Control.

Negative Veil Control does not create negative bonus output.

### Physical Manifestation damage

When a valid Manifestation creates an independent physical phenomenon and that phenomenon harms a creature through the ordinary physical/world procedure, its ordinary physical damage affects **HP** unless an explicit technique or hazard rule says otherwise.

A technique may separately deal Vigor damage if authored to disrupt regenerative reserve. Vigor damage does not directly reduce HP.

## Persistent Expression Cadence

Any sustained, persistent, attached, embodied, invested, consecrated, routed or similar effect that can interact repeatedly with ordinary actions must declare an **Expression Cadence** for each output.

- **Continuous** — a static or persistent property. It does not multiply with Attack Units and normally remains active while the effect remains valid.
- **Rider** — a modest effect that may apply to each eligible action, attack, Guard, movement or other listed event. Rider values must be calibrated against the maximum Physical Tempo capable of triggering them.
- **Pulse** — a stronger finite effect with an explicit refresh unit such as once per turn, round, Emotion Window or another authored interval.
- **Spend** — a stronger repeatable output that requires an explicit additional cost each time it is used, such as VP, Vigor, Destiny or another listed resource.

A full technique-scale instance of damage, healing, Vigor restoration, strong control or comparable major output must not be an unrestricted per-Attack-Unit Rider. Use Pulse, Spend, a finite budget or another explicitly bounded cadence.

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

Archetype-specific rules may add narrower qualifiers, but should not duplicate an existing universal concept without a mechanical reason.
