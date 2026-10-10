# Cover and Line of Fire v0

> **LOCKED native battlefield-defense foundation; the +2 / +4 / +6 / +8 ladder is playtest-sensitive.** Physical cover creates an **external difficulty for a legal ranged shot**, not a separate defender roll or an increase to Guard/Dodge capacity. One attack roll resolves both accuracy and whether an otherwise accurate projectile strikes cover. See [Ranged Defense](off-hand-and-ranged-combat.md), [Defensive Responses](defensive-responses-and-criticals.md), [Aim](aim-v0.md), and [Manifestation Resolution](../07-veil-magic/manifestation-resolution.md).

## Line of fire first: can the attack reach the target?

Before committing a ranged attack, establish its **actual origin**, its intended **target/point**, and whether at least one **physically usable direct path** passes through an exposed portion of the target from that origin.

1. **Clear line of fire:** No relevant solid obstruction between the attack origin and the intended target. Cover Difficulty = 0.
2. **Partially obstructed, but physically possible line of fire:** An exposed target portion or a usable opening exists. The attack is legal; use the applicable [Cover Difficulty tier](#cover-difficulty-tiers).
3. **Completely blocked:** Solid, impenetrable-for-this-attack cover blocks every usable direct path to the intended target. **No direct attack against the creature is legal**, regardless of Attack total, natural 20, Aim, or proposed Called Shot. The attacker can instead target the **barrier itself**, a different exposed point, or use a **separately authored** attack that physically penetrates or bypasses the obstruction.

Evaluate **actual firing direction, elevation, position, attack profile, posture, and available openings**. Cover is **directional**: protection from one firing position may not protect against an attacker at a different angle. A waist-high wall, parapet, and firing slit are not magically symmetric; an attacker behind an obstacle can shoot out only along a **physically usable firing route**. A target must be meaningfully exposed to that specific line of fire. Do not model precise projectile trajectories or calculate pixel-level exposure for ordinary play.

Choose cover relative to the **actual attack origin** and the defender's actual position/posture when that attack resolves. If a valid Interception or other response changes the geometry, recheck cover and legality at the normal response timing **without reopening already committed attack profiles or defense choices**. Cover is an external shot condition, not a new defense option.

## Cover Difficulty tiers

| Cover condition | Typical exposed portion (guideline, not percentage math) | Cover Difficulty |
|---|---|---:|
| **None** | No relevant solid obstruction | **+0** |
| **Light** | Much of the target visible; small obstacle, edge, or low barrier | **+2** |
| **Half** | Roughly half the target protected by the obstacle | **+4** |
| **Major** | Most of the target protected; substantial visible part remains | **+6** |
| **Narrow opening** | Very small but physically usable gap or exposed point | **+8** |
| **Full solid cover** | No physically usable direct line of fire | **Shot illegal** |

The percentages/exposure descriptions are **GM adjudication guides**, not random chance. **Do not roll to see whether cover catches the shot**: the existing Attack roll already determines that. Do not require a **Called Shot** merely because only a limited target area is exposed. An ordinary successful attack against a partly exposed creature resolves ordinary hit consequences; it does not automatically obtain a particular location wound, targeted injury, or Interrupt.

If several physical obstructions lie along the route, assess **one effective Cover Difficulty from the actual remaining opening**; do **not** sum +2 +4 +6 from separate obstacles. If their combined geometry leaves **no usable path**, the target has **full solid cover**. Distinct penalties from range, independently applicable size/position, and separately authored shot conditions remain separate, but **do not count the same reduced visible profile twice** (for example, a Prone profile bonus that is already fully represented by the selected cover exposure tier).

Cover cannot grant protection against an attack that originates on the same **unblocked side** of the barrier; evaluate actual geometry, not only grid adjacency or a static "in cover" label.

## Apply cover to the selected ranged defense

Cover adds **one external shot-condition modifier** to the defender's existing resolution. It is not Guard equipment, extra Guard capacity, a free Dodge, an additional Reaction, or a second die roll.

For a normal projectile when the defender chooses **Take Hit**, or cannot make an active response, use **static Ranged Defense**:

```text
Static Ranged Defense =
10 + Range Difficulty + Cover Difficulty
+ applicable Size/Position and other shot-condition modifiers
```

For an aware defender who chooses **active Ranged Dodge**, use the current Dodge formula **plus the same applicable Cover Difficulty**:

```text
Ranged Dodge =
10 + capped Agility + Awareness + Evasion Bonus
+ Range Difficulty + Cover Difficulty - Dodge Pressure
+ other modifiers explicitly applicable to active Ranged Dodge
```

The current [Prone Position Defense](special-movement-terrain-and-prone.md#ranged-attacks-against-a-prone-target) remains applicable where independent and physically meaningful; do **not** duplicate one and the same physical reduction in target exposure with both that modifier and the chosen Cover tier. Cover does **not** change Dodge Pressure or inherent Agility/Awareness/Evasion.

**Legal projectile Guard:** When the defender may actually Guard this projectile with a qualifying instrument, **add applicable Cover Difficulty once as an external ranged shot condition to its otherwise normal Guard Defense**. Neither the barrier nor cover automatically grants Guard eligibility, Guard capacity, an instrument, or a separate chance to stop the shot. Keep the Guard instrument's ordinary bonus/capacity exactly as authored. If the "cover" is merely the **same held shield/instrument** chosen for Guard, **do not also count it as environmental Cover**; it contributes through its own Guard stats instead. A separately positioned wall may supply genuine external cover while a buckler remains a distinct Guard instrument. Do not introduce Range Difficulty into Guard unless a rule explicitly makes it apply to that Guard calculation.

**One response per attack** still applies. A chosen Dodge/Guard spends the normal defensive resources and is not reselected after the attack roll. See [Defense assignment](defensive-responses-and-criticals.md#declaring-defense).

## Cover-hit window: one roll decides impact location

After the defender's applicable static Ranged Defense, active Ranged Dodge, or legal projectile Guard is selected and all ordinary responses finish, determine:

- **Base Defense (B):** the otherwise applicable defense against **this actual attack**, with every applicable modifier **except the effective Cover Difficulty**.
- **Effective Cover (C):** the positive Cover Difficulty **remaining after any valid [Aim](aim-v0.md) mitigation** against Cover, with minimum 0.
- **Final Defense (D):** `B + C`.
- **Attack Total (A):** the one normal attack roll and applicable attack modifiers.

Resolve the **same one roll**:

| Result | Consequence |
|---|---|
| Direct attack is physically **illegal** | Cannot target the creature, regardless of roll; choose another legal target or attack the barrier |
| Natural **1** | Automatic miss under existing rules; no automatic cover strike solely from the natural 1 |
| `A > D` | **Target is hit**, subject to existing critical-confirmation and other valid attack rules |
| `B < A <= D` and `C > 0` | **Cover catches the attack**; projectile contacts the actual intervening obstacle before reaching the target |
| `A <= B` | Attack fails for a reason **other than this cover band**; resolve the usual ordinary miss, Dodge, or successful instrument-Guard outcome, as applicable |

The **cover-hit band** is the difference between defeating the base defense and defeating that base defense plus cover. Do **not** make a second attack, roll cover percent, roll disadvantage, or reroll an active Dodge. If the chosen defense is Guard and `A <= B`, that remains an ordinary **successful instrument Guard**, not a cover strike; use the existing Guard impact rules where relevant.

An Aim that mitigates **Cover** changes `C` for this shot and therefore narrows the cover-hit band. Aim against a **different source**, such as Range Difficulty, changes the source in `B` but **does not reduce C**. This applies to whichever defense actually resolves the shot, without changing the existing Aim declaration or granting a universal accuracy bonus.

**Natural 20 / confirmation:** Existing critical rules still determine the attack/confirmation result for a **legal shot**. Cover remains part of the applicable defense in any required confirmation. Natural 20 never authorizes a physically impossible line of fire. Do not introduce new cover-specific critical effects or automatic cover-penetration here.

### What happens to a projectile stopped by cover?

A projectile that lands in the cover-hit band **strikes the exposed, physically blocking part of the cover** rather than the creature. Place the impact at the **first actual blocking surface along that attempted route**, on its incoming/attacker-facing side unless a more precise battlefield depiction specifies the impact point.

- It does **not** deal its ordinary on-hit damage/status/wound/Interrupt to the intended creature.
- The cover/object may sustain damage or be penetrated **only if** a separately authored object durability, attack penetration, or destruction rule supports that interaction. Cover v0 grants **no universal cover HP, penetration-through-cover formula, or incidental destruction**.
- An effect that explicitly triggers **on striking a surface**, including projectile-delivered bursts, detonations, clouds or splashes, can still occur **from the cover impact point** under its actual effect rules. Cover does not automatically shield a creature from an ensuing area effect; evaluate the barrier's real ability to block that phenomenon and its geometry.
- If the projectile has no applicable on-surface consequence, it simply fails to reach the target. A mundane arrow hitting stone does not become a free attack against something behind the stone.

**Projectile-delivered Manifestation/area priority:** A physically blocked cover-hit projectile **impacts the cover instead of using ordinary random miss scatter**. The [Manifestation Miss Impact Point rule](../07-veil-magic/manifestation-resolution.md#projectile-delivered-areas) applies to **ordinary misses**, not cover hits. On a legal success, use the intended point normally. On a legal successful projectile Guard, use the Guard instrument impact rule normally. Never make a second generalized cover impact roll.

For **non-projectile pointed rays/beams** or unusual ranged phenomena, the same line-of-fire and Cover Difficulty model may affect an applicable **aimed attack roll**, but a "cover hit" represents contact with the **barrier** only where that phenomenon actually collides or is obstructed. The attack's authored physical propagation controls whether the beam terminates, scorches, reflects, or passes through. A barrier cannot be treated as a universal defense against unrelated area effects, non-ballistic hazards, or **Direct Veil Intrusion** merely because Cover exists.

## Aim and precision: not mandatory Called Shots

[Aim v0](aim-v0.md) can declare **the chosen Cover Difficulty source** and mitigate **up to 4** of its positive value for **one** subsequent eligible shot. Do not combine Aim against Range and Cover for the same shot; they remain distinct selectable sources. For example:

| Actual cover | Ordinary Cover Difficulty | Aim directed specifically at Cover |
|---|---:|---:|
| Light | +2 | +0 |
| Half | +4 | +0 |
| Major | +6 | +2 |
| Narrow opening | +8 | +4 |
| Full solid cover | Shot illegal | Still illegal |

Aim does not grant hidden-target detection, let a weapon fire through solid walls, or authorize Called Shot effects. To deliberately damage a particular body location with authored special wound/disable effects requires a separately legal **Called Shot** once that maneuver is defined. If the desired body part is completely blocked from the chosen attack origin, the Called Shot is impossible regardless of Aim.

## Examples

| Situation | Result |
|---|---|
| Target has **B = 14**, **Half Cover +4**, no Aim | D = 18; A <= 14 ordinary miss/defense, A 15–18 **strikes cover**, A >=19 hits target, absent a special natural-roll rule |
| Same target; Aim declared specifically against Half Cover | C becomes 0; D = 14; A >=15 hits target, subject to normal roll rules |
| Archer at Long range (+5), target behind Half Cover (+4), Aim declared **against Range** | Range source becomes +1, but Cover remains +4 and cover-hit band remains 4 points wide |
| Shooter has a clear flank around a wall | Cover = +0 from that firing direction even if the target would have Cover from another direction |
| Only target's upper body visible above stone parapet | Ordinary attack legal with the applicable cover tier; a successful hit is not automatically a Called Shot to the head |
| Solid wall completely blocks target | Cannot target creature with a direct ordinary arrow; can attack wall or use an explicitly authored penetrating/bypassing attack |
| Projectile-delivered burst falls within cover-hit band | Impact/detonation at the actual barrier surface; do **not** use random miss scatter |
| Archer selects a shield-based legal projectile Guard while behind an independent wall | Separate wall contributes Cover once, independent shield handles Guard normally; no double count for the same held shield |
| Interception moves target behind a wall before attack resolution | Recheck legality and cover at actual attack timing; any impossible direct shot fails under existing committed-action rules |

## Deferred boundaries

- **Shooting into melee, intervening creatures, and friendly fire:** do not equate an interposing ally/enemy with a wall or automatically assign a generic penalty merely for an engaged target. Actual rules for creature interception and stray-hit outcomes require a separate v0.
- **Concealment, invisibility, smoke, darkness, and unseen targets:** sight and target acquisition are not ordinary physical cover. A target behind smoke may be hard to find without any solid obstruction. This subsystem must be authored separately.
- **Ballistic arc, projectile penetration, ricochet, and barrier durability/destruction:** physical special-case behavior requires authored weapon/object traits rather than generic cover-hit damage or second cover rolls.
- **Physical defense against area effects:** walls and barriers block an area only where a particular phenomenon and actual geometry allow it. No universal area-save or "Cover cancels area" rule is added.
- **Called Shot, weapon profiles, precision techniques:** no invented Called Shot AP cost, location difficulty, wounds, or on-hit Interrupt is introduced here.
- **Playtesting:** verify Cover Difficulty +2/+4/+6/+8, interaction with active high-Tempo Dodge, Aim's four-point cap, and whether the cover-hit window is too punishing for high-value on-hit ammunition.

**LOCKED v0:** Physical line-of-fire gate; directional Cover +2/+4/+6/+8; **one Attack roll**; Cover Difficulty contributes to static Ranged Defense, active Ranged Dodge, and legal projectile Guard (not extra capacity); no second percentage cover roll, disadvantage, or mandatory Called Shot; cover-hit band `B < A <= B+C` after eligible Aim; real cover impact supersedes normal projectile-area scatter; solid blockage prohibits direct targeting. Numerical ladder is playtest-sensitive.
