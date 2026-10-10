# Manifestation Resolution

> **LOCKED resolution principle.** A valid Manifestation creates an independently existing external phenomenon. Once that phenomenon exists outside a living target, it is resolved through the ordinary physical/world procedure appropriate to what the phenomenon actually does. It does **not** use Direct Veil Resistance merely because magic created it.

See [Metaphysical Foundation](metaphysical-foundation.md) for the Intrusion / Imposition / Manifestation distinction and [Universal Resonance and Direct Veil Magic](resonance-and-intrusion.md) for Direct Veil Resistance.

## Core rule

A Manifestation does not receive a generic spell attack, spell save, or area-dodge subsystem.

Instead:

1. determine what independent phenomenon now exists;
2. identify the ordinary physical delivery or hazard procedure that matches it;
3. use that procedure;
4. apply the Manifestation's authored damage, penetration, condition, terrain, duration, resistance, or other consequences.

If the attempted effect originates **inside or overlapping a living target**, it is not a valid Manifestation against that target. Resolve it as **Intrusion**.

## Manifested projectiles

A manifested projectile uses the normal thrown-projectile attack architecture unless the technique explicitly defines another ordinary launcher or delivery method.

Use the universal thrown attack override:

```
Manifested Projectile Attack =
d20
+ Agility
+ Precision
+ relevant Training
+ situational modifiers
```

The technique must still define its legal range, projectile properties, damage/effect, Penetration where relevant, and any other authored constraints.

The **relevant Training** is the ordinary narrow throwing/weapon Training that actually applies to the projectile. **Veil Practice is not automatically substituted** merely because magic created it.

Reusing the thrown attack procedure does not automatically add Strength to a technique-authored damage packet. If the Manifestation creates an ordinary weapon profile, use that profile's normal Physical Contribution; otherwise use the technique's authored damage/effect.

A Manifestation does not gain **Veil Control**, **Resonance**, or **Veil Integration Bonus** on the projectile attack merely because magic created the projectile.

The normal ranged-defense rules apply to the launched projectile:

- static Ranged Defense where appropriate;
- active ranged Dodge where appropriate;
- normal projectile Guard where the defender has equipment capable of Guarding that projectile;
- cover, range, size/position, and other ordinary shot-condition modifiers.

If a Manifestation creates a projectile but a different physical launcher is actually used, resolve the attack with that launcher's normal rules instead.

### Projectile-delivered areas

If a projectile carries an area effect, resolve the projectile's delivery first and then resolve the area from the resulting impact point. **[Cover and Line of Fire v0](../05-combat/cover-and-line-of-fire-v0.md#cover-hit-window-one-roll-decides-impact-location) takes precedence over normal random miss scatter** when a legal ranged attack falls into the cover-hit window: the projectile strikes the **real interposing cover surface**, and any surface-triggered burst/cloud/explosion originates from that impact point. Resolve the area against the actual barrier and intervening geometry; a cover impact does not cancel the carried area by default. Full solid blockage makes an ordinary direct targeted shot against the concealed creature **illegal**, not a scatter shot through a wall.

On a successful attack, the intended target point is the impact point.

On an **ordinary miss not already stopped by Cover or a successful physical Guard**, determine a **Miss Impact Point** rather than discarding the projectile:

1. Determine **Scatter Defense** from the defense that actually resolved the shot:
   - **No applicable Cover Difficulty:** use that actual defense unchanged.
   - **Partial cover, and the attack is an ordinary miss** (`A <= B`, or an automatic natural-1 miss regardless of its numerical total, under [Cover and Line of Fire v0](../05-combat/cover-and-line-of-fire-v0.md#cover-hit-window-one-roll-decides-impact-location)): use **Base Defense `B`**, the actual selected defense **excluding effective Cover Difficulty `C`**, rather than final Cover-adjusted Defense `D = B + C`.
   - **Cover-hit band** (`B < A <= D`), physically illegal direct shot, or successful projectile Guard: this ordinary-miss scatter procedure **does not apply**. Resolve the actual cover/Guard impact or illegality first.
2. Calculate the **Miss Margin**:
   ```text
   Miss Margin = max(0, Scatter Defense - Attack Total)
   ```
   Keep all other modifiers that actually contributed to Base Defense, including any separately declared **Aim against Range**; remove **only effective Cover Difficulty** when this is an ordinary miss. A natural 1 is still an automatic miss. If its Attack Total would otherwise beat **Scatter Defense**, use Miss Margin 0.
3. Calculate scatter distance:
   ```
   Scatter Distance = 1 + floor(Miss Margin / 5)
   ```
4. Roll **1d8** for direction from the intended impact point:
   - 1 — north
   - 2 — northeast
   - 3 — east
   - 4 — southeast
   - 5 — south
   - 6 — southwest
   - 7 — west
   - 8 — northwest
5. Move the impact point that many squares in the rolled direction. That square is the **Miss Impact Point**.
6. Resolve the projectile's area from that point.

**Cover scatter example:** With `B = 10`, `C = 8`, and `A = 5`, the shot is an **ordinary miss** (`A <= B`), not a cover impact. Use `Scatter Defense = B = 10`: **Miss Margin = 5** and **Scatter Distance = 2 squares**. Using final `D = 18` here would incorrectly inflate Miss Margin to 13 and scatter to 3 squares.

Scatter Defense derives from the **actual defense selected for the shot**—static Ranged Defense or active Ranged Dodge where applicable—but excludes the effective **Cover Difficulty** for ordinary misses. A cover hit, a successful projectile Guard, or a physically illegal direct shot does **not** use this scatter procedure.

### Successful Guard against an area projectile

If a legal projectile Guard stops a projectile-delivered area attack, the projectile does **not** scatter.

By default, the projectile impacts the **interposing Guard instrument at the defender's position**. Use the defender's occupied space as the impact point unless the battlefield representation tracks a more precise barrier boundary.

Resolve the carried area from that impact point.

A successful Guard therefore stops the projectile from striking the defender directly, but it does **not** automatically cancel an explosion, burst, cloud, splash, or other area carried by that projectile.

A shield, wall, or other barrier may separately block or mitigate the resulting area only when the ordinary physical rules say that barrier can actually interpose against that phenomenon.

A technique may explicitly state that being Guarded causes the projectile to dissipate, fail to trigger, ricochet, or use another authored impact rule. That specific rule overrides this default.

A technique may explicitly replace this scatter rule with a different authored miss-placement procedure when its projectile behaves differently.

Physical interception by a wall, shield, cover, or other solid obstruction remains governed by [Cover and Line of Fire v0](../05-combat/cover-and-line-of-fire-v0.md). Scatter does not allow a projectile to pass through an obstruction it could not physically cross. **Cover hits and legal instrument-Guard impacts are not ordinary misses for purposes of this random scatter procedure.**

The area does **not** grant a second generic Dodge after the projectile has established where the effect occurs. A near miss can therefore still catch the original target if the resulting area reaches that target's space.

## Pointed beams

A manifested beam that must be continuously or directly pointed at a target uses **Precision twice** as its attack Ability contribution.

```
Beam Attack =
d20
+ Precision
+ Precision
+ explicit technique and situational modifiers
```

A Training is added only if the technique or another explicit rule says a specific narrow Training applies. There is no automatic Veil Practice bonus.

A pointed beam is a ranged attack and uses the normal applicable ranged defenses and shot conditions.

Beam techniques must be calibrated around this specialized accuracy model. Their authored damage, duration, dwell, penetration, rider, or other effects account for the fact that the attack uses double Precision.

## Area manifestations

There is **no generic area-effect Dodge** that allows a character to remain inside the affected space while avoiding the phenomenon.

If a Manifestation occupies the character's position when it resolves, the character suffers the phenomenon's authored consequences unless another rule actually prevents or mitigates them.

Examples include:

- a wall of fire occupying the character's space;
- an expanding cloud;
- a burst of heat;
- a field of shards;
- an area of corrosive material.

Avoiding an area requires something that changes the fiction rather than an abstract save, such as:

- already being outside the affected area;
- actual movement granted before the area resolves;
- a suitable physical barrier or cover;
- an applicable shield/interposition rule;
- immunity, resistance, armor, or another mitigation rule that applies to the consequence.

A shield or barrier may protect against an area Manifestation only when it can physically interpose against the relevant phenomenon. The final universal shield/cover handling for such cases belongs to the combat-defense rules; this page does not invent a separate magical Guard procedure.

## Persistent terrain and hazards

Manifested terrain is resolved as terrain or a hazard.

A creature entering, crossing, or remaining in the affected space suffers the authored consequence at the timing stated by the technique or the ordinary hazard rule.

There is no generic Direct Veil Resistance or area Dodge merely because the terrain was created magically.

Examples:

- burning floor deals its authored fire damage while occupied;
- ice changes footing or movement according to the applicable terrain rule;
- smoke obstructs or harms according to its authored hazard;
- thorns, acid, rubble, or similar created terrain use their physical consequences.

Applicable resistance, immunity, armor, equipment, or other mitigation works normally if the consequence says it applies.

## Manifested restraints

A Manifestation that physically grabs, binds, or restrains a target uses the ordinary physical procedure appropriate to **what was manifested**.

The restraint does not use Direct Veil Resistance merely because the restraining thing was created by magic.

### Manifested creatures or creature-like agents

A manifested **creature** or independently acting creature-like agent may use the locked [Grapple v0](../05-combat/universal-maneuvers.md#grapple-v0) foundation only when its authored profile supplies everything Grapple v0 requires, including:

- usable Strength and/or Agility values for Grapple Contests;
- any applicable Training or explicit contest modifiers;
- the anatomy/reach needed to establish and maintain physical contact;
- an action/timing model capable of initiating, maintaining, releasing, and exploiting a Grappling State.

An animated manifested hand, vine-creature, chain-creature, or similar agent therefore uses Grapple v0 only if the technique actually gives it such a creature-like Grapple profile.

If such an agent actually becomes **Controller** in a legal Grappling State, the locked [Secure Limb v0](../05-combat/limb-control-v0.md) rider applies normally **when its authored creature-like profile also provides the action, physically usable controlling limbs/anatomy, reach, and maintained contact required by that maneuver**. Resolve its Secure Limb and Break Limb Control through the ordinary Grapple Contest and the same AP/timing framework. This does **not** give an inert manifested object Grappling State, assume missing anatomy or action economy for a Manifestation, or bypass the existing [Grapple v0](../05-combat/universal-maneuvers.md#grapple-v0) prerequisites.

### Manifested objects

An inert or non-creature manifested object—such as ordinary conjured chains, binding vines, bands, or a fixed restraint—does **not** automatically enter Grappling State and does not roll a Grapple Contest merely because it restrains physically.

Its technique must instead author the physical restraint procedure it needs, such as:

- how the restraint is initially applied;
- what physical values or fixed resistance the object provides;
- what action/check allows a creature to break, slip, cut, or otherwise escape it;
- how damage, destruction, release, duration, or loss of anchoring ends the restraint.

Those authored rules remain physical restraint mechanics, not Direct Veil Resistance.

Until a universal object-restraint controller model is separately locked, do not treat an inert manifested object as a creature for Grapple v0.

## Falling manifested objects

A manifested object that falls, collapses, or is dropped onto a target uses the ordinary **falling-object / physical hazard** procedure.

Magic determines that the object exists. Once it is falling as an independent object, its collision is resolved exactly as an equivalent ordinary falling object would be.

The final falling-object procedure remains part of the physical-hazard rules.

## Melee and enchanted attacks

There is no separate **Manifestation melee attack** category.

If a character is making a melee attack, use the normal melee rules.

A manifested or magically created weapon that is physically wielded uses the ordinary melee attack procedure appropriate to its weapon profile.

A magical enchantment, Embodiment, Signature, rider, or other effect attached to a melee weapon or physical strike modifies what happens **on or after a successful normal melee hit** unless its own rule explicitly says otherwise.

Magic does not replace the normal melee attack roll merely because the weapon or rider is supernatural.

## Classification examples

| Effect | Classification | Resolution |
|---|---|---|
| Telekinetically hold a creature with direct Veil force | Imposition | Direct Veil Pressure vs Direct Veil Resistance |
| Create an animated hand/creature that physically grabs a creature | Manifestation | Grapple v0 if its authored creature-like profile supplies the required contest/action values |
| Create and throw an ice spike | Manifestation | normal thrown-projectile rules |
| Point a cutting beam at a creature | Manifestation | double-Precision beam attack vs normal ranged defense |
| Create a wall of fire through occupied spaces | Manifestation | no generic area Dodge; occupants suffer/mitigate authored consequence |
| Create burning ground | Manifestation | persistent terrain/hazard consequence while occupied |
| Conjure a stone overhead and let it fall | Manifestation | normal falling-object/hazard procedure |
| Enchant a sword with fire | melee attack with magical rider | normal melee attack; fire effect resolves on/after hit |
| Create fire inside a creature's lungs | Intrusion | Direct Veil Resistance + Intrusion Barrier |

## What remains outside this lock

This page locks the **mapping principle and delivery families**, not every physical subsystem they invoke.

Still to be completed in the combat/hazard rules:

- advanced Grapple/control extensions beyond locked Grapple v0 and [Secure Limb v0](../05-combat/limb-control-v0.md), including cooperative multi-creature restraint, multi-limb and leg control, unusual-anatomy exceptions, and persistent weapon-to-weapon binds outside Grapple;
- a universal physical restraint model for inert manifested objects such as chains, vines, bands, cages, or other non-creature restraints;
- final shield and cover handling against broad physical phenomena;
- general movement/reaction timing that may allow actual movement before an area resolves;
- falling-object and collision damage;
- complete condition handling;
- technique-by-technique projectile ranges, beam effects, terrain consequences, and other authored content.

Those missing procedures do not create a separate magical-defense layer. When completed, Manifestations use them directly.
