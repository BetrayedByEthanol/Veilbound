# Limb / Weapon-Hand Control v0

> **LOCKED native foundation.** **Secure Limb** is a targeted, persistent rider on an existing **Controller/Controlled Grappling State**, not a separate Grapple, a universal condition, or a weapon bind at ordinary melee distance. It restricts one specifically controlled grasping limb while the hold is maintained. See [Universal Maneuvers — Grapple v0](universal-maneuvers.md#grapple-v0), [Pin](universal-maneuvers.md#pin), and [Disarm v0](disarm-v0.md).

## Secure Limb: declaration and eligibility

A creature may attempt **Secure Limb** only if it is the **Controller** in an existing Grappling State. The action costs **one Physical Action** at the Controller's normal Focus-based Physical Action cost.

Before rolling, identify **one specific upper limb or analogous grasping appendage** of the Controlled creature, and describe how the Controller can isolate and maintain control of it. The chosen limb must be physically reachable in the current shared Grapple square; the Controller must have usable hands, limbs, body leverage, or suitable anatomy and position to maintain both the existing Grapple Control and the additional hold.

**Control grants permission, not automatic limb access.** It does not free a limb committed to maintaining a different hold or make an inaccessible arm reachable. Secure Limb does not require the target to be holding a weapon: an empty hand may also be secured.

This v0 concerns **upper limbs and grasping appendages**. Dedicated leg control, wing/flight restraint, unusual creature anatomy, weapon binds from fighting distance, and joint injury are later subsystems.

Already-established Grapple contact means declaring Secure Limb creates **no new Close-Contact Opportunity between these two grapplers**. Opportunities from other independently authored events remain applicable.

## Establishing the Secured Limb

Make the ordinary [Grapple Contest](universal-maneuvers.md#grapple-contest), with each participant using **d20 + plausible Strength or Agility + applicable narrow Training + situational modifiers**. Secure Limb grants no automatic numerical modifier to this establishing contest.

| Grapple Contest outcome | Result |
|---|---|
| Controller wins | The declared limb becomes **Secured** under the same Controller |
| Exact tie | No new limb is secured; the existing Controller/Controlled position remains |
| Controlled creature wins | No new limb is secured; the existing Controller/Controlled position remains |

The failure/tie outcomes do not inherently end an existing Pin, reverse Control, break Grappling State, or grant a counterattack.

Apply the Grapple Contest's normal **unable-to-contest** rule when a participant cannot make any plausible active response. Incapacity does not bypass physical reach, required free limbs, or an impossible hold.

A Controller may declare **at most one Secure Limb attempt against that Grapple partner per turn**, even with enough Turn AP for additional Physical Actions. This is an attempt limit, not immunity against distinct lawful actions or an automatic penalty against the Controller.

## Secured Limb: effects

While the rider persists, the **named limb cannot perform an action incompatible with its actual restraint**. Determine legality from that limb's role in the action, rather than applying an all-purpose penalty to the creature.

- A weapon held solely by the Secured Limb cannot be used to **Attack, Guard, or make an Opportunity Attack** while that attack or defense requires motion of that limb; the weapon is **still held**, not automatically dropped.
- A **two-handed weapon** requiring both hands to Attack or Guard becomes unusable for those actions when one of its necessary arms is Secured, unless an explicit separately legal weapon mode applies.
- Another free arm, weapon, shield, foot, head, or natural weapon may still be used where its action and current Grapple positioning are physically legal.
- A technique, spell, or item manipulation requiring the Secured Limb cannot use that limb, but **Veil magic does not automatically fail** if it can legally operate without the limb.
- Reaction, Opportunity Capacity, an active Opportunity Response, Turn AP, and Guard capacity are **not themselves removed**. Recalculate the actions, legal Guard instruments, actual Reach, and threatened squares the creature still has available.
- Dodge is **not automatically penalized** by this rider. It remains legal only if the actual Grapple position, restraint and necessary body motion permit the intended Dodge under existing rules.
- The Secured Limb cannot simply be used for ordinary equipment manipulation or another incompatible maneuver, but it **can participate in a declared attempt to free itself**, using whatever active bodily resistance is physically possible.

**Secured Limb is not Pin, Prone, paralysis, helplessness, or a guaranteed hit.** The Controlled creature remains capable of taking legal actions with its remaining available body parts. Restricting a weapon-bearing arm can weaken the creature's protection of allies, but does not automatically switch off all melee threats.

When a previously assigned Guard becomes illegal because its necessary limb is newly Secured, use the existing [lost-Guard fallback](defensive-responses-and-criticals.md#guard-instrument-lost-after-defense-assignment): another legal Guard instrument where available, then Dodge where legal, otherwise Take Hit. A Secured Limb can make a Guard impossible **without removing the physical weapon**.

## Disarm synergy: Secured Weapon-Hand advantage

A Controller with **a formally Secured limb that actually holds or controls the target item** receives a **+4 positional bonus to Disarm Pressure** when making a legal [Grapple Disarm](disarm-v0.md#grapple-disarm) against that item.

- The bonus is earned by **first winning Secure Limb**, not merely by being a Controller, being adjacent, holding a weapon, or maintaining Pin.
- The Disarm still costs its own **Physical Action**, satisfies all [eligible contact](disarm-v0.md#declaration-and-eligible-contact) requirements, and uses the normal opposed Disarm Contest with the defender's **+6 Grip Retention**.
- The Controller must still possess enough available body parts and leverage to perform the actual item-release method while maintaining both Grapple and Secured Limb. A hand committed to holding the limb cannot simultaneously perform an incompatible independent action.
- This +4 is a **single positional bonus**: it does **not stack** with another positional/binding advantage granted by equipment or a later technique. Use only the largest applicable positional advantage. Legitimate non-positional Training and situational modifiers remain governed by their own rules.
- The +4 applies only to **the item actually implicated by the Secured grasping limb**, not to another weapon or item on the creature.

At equal underlying Disarm contest modifiers, the +4 increases the chance of success against the normal +6 Grip Retention from **22.75% to 38.25%**. It does not guarantee release or authorize taking possession of the item after it is dropped.

Securing an unarmed limb never supplies a general +4 Disarm bonus against some other held item.

## Break Limb Control

A Controlled creature may spend **one Physical Action** to attempt **Break Limb Control** rather than Reverse Control or Escape. This attempt is always allowed **if a plausible bodily resistance method exists**, even when the Secured Limb cannot perform an ordinary attack or item manipulation.

Make a normal **Grapple Contest**, with the Controlled creature receiving **+2 specifically to this Break Limb Control contest**. This bonus is not a universal bonus to Reverse Control, Escape, or resisting the original Secure Limb.

| Break Limb Control contest | Result |
|---|---|
| Controlled creature wins | The named Secured Limb rider ends |
| Exact tie | The named Secured Limb rider ends |
| Controller wins | The named Secured Limb rider remains |

**Break Limb Control does not itself change the Grappling State or its Controller/Controlled position.** An independently maintained Pin also remains in force; a limb freed from the *Secured Limb rider* may still be restricted by that Pin's actual physical configuration.

With equal baseline contest modifiers before the +2, the Controlled creature succeeds or ties **61.75%** of the time.

The Controlled creature may instead attempt ordinary [Reverse Control](universal-maneuvers.md#gain-or-reverse-control) or [Escape](universal-maneuvers.md#escape), paying their normal costs and satisfying their separate prerequisites. A successful Reverse Control or Escape can end the Secured Limb because it ends the necessary Controller relationship or Grappling State. Break Limb Control is the **focused, more accessible way to recover the limb** while leaving the Grapple itself intact.

## Persistence, replacement, and interaction with Pin

There is **no recurring Turn AP cost** to maintain one Secured Limb. It persists only while the **same Controller** maintains Grapple Control and a physically valid hold on the chosen limb.

A Controller can maintain at most **one formally Secured Limb per Grapple partner** under this v0. To change the target limb, the Controller must **release the old Secured Limb rider when declaring a new Secure Limb attempt**, pay another Physical Action, and win the new contest. Failure does not restore the released rider. Releasing the rider alone does not end the underlying Grapple.

The Secured Limb rider immediately ends if:

- Grappling State ends or the original Controller no longer has Control, including Neutralization, reversal, incapacitation transitions, or a successful separation;
- the Controller voluntarily releases that limb or can no longer maintain the necessary physical position, contact, or committed body parts;
- the Controlled creature wins or ties Break Limb Control; or
- another authored effect or physical displacement makes the specific hold impossible.

A Pin and Secured Limb may coexist **only where the Controller can actually maintain both**. Pin's own trapped-body-part restrictions remain effective independently and are neither created nor strengthened merely by assigning the Secured Limb label. A Pin **does not automatically provide the +4 Secured Weapon-Hand Disarm bonus**: that precision advantage requires a successful Secure Limb action and continuing contact on the relevant grasping limb.

If establishing or maintaining Pin requires the limbs previously used for Secure Limb, the Secured Limb ends; likewise, a later action cannot borrow a hand already committed to maintaining either hold.

Neither state gains a second automatic numerical modifier to Disarm, Escape, Reverse Control, or other attacks merely because both labels coexist.

## Explicit boundaries

Secure Limb v0 provides **one rider**, not tiers of Contested Limb, partial weapon-use penalties, progressive grip tracking, additional per-round resistance rolls, permanent injuries, or a general condition applying outside Grapple. Persistent **weapon-to-weapon binds at fighting distance** and any special weapon-assisted trapping actions belong to a later technique system, not this Grapple rider.

Creature-specific anatomy, simultaneous multi-limb restraint, leg control, joint damage, partial/one-handed variants of normally two-handed weapons, and cooperative dogpiles remain separate rules work.
