# Disarm v0

> **LOCKED native foundation; numerical calibration remains playtest-sensitive.** Disarm is one universal Physical Maneuver that forces release of a specific **held item**. Ordinary Disarm and Grapple Disarm share one contest. See [Universal Maneuvers](universal-maneuvers.md) for Close-Contact Opportunities and Grapple Control; [Turn Action Points and Tempo](action-categories-and-physical-tempo.md) for action costs; and [Defensive Responses and Criticals](defensive-responses-and-criticals.md) for lost-Guard fallbacks.

## Declaration and eligible contact

**Disarm costs one Physical Action**, using the actor's normal Focus-based Physical Action cost. Before opening responses, identify **one held item**, its holder, and the actual contact method. A two-handed item remains one item; one success must plausibly overcome *all* grips maintaining it.

An **eligible Disarm contact method** is a physical action able to apply leverage, torque, or controlled force to make the holder release the item. It must satisfy **all four** requirements:

1. **Releasable target.** The item is gripped or wielded and can physically leave that grip. An object merely worn, sheathed, packed away, firmly strapped on without a releasable grip, built into the creature, or otherwise anchored is not ordinarily Disarmable.
2. **Reachable control point.** The actor can actually contact the item, its gripping hand/wrist, or another mechanically relevant control point with the method's present reach and positioning. Disarm grants no extra melee Reach.
3. **Grip-breaking mechanism.** The method can wrench, twist, trap, lever, or otherwise defeat possession of the **whole item**. Merely striking its surface is insufficient.
4. **Available control.** The actor has sufficient usable limbs, implement geometry, leverage, and body position. A limb already needed for an incompatible Pin/Grapple hold is not also available for the Disarm.

Eligible method families:

| Contact family | Eligibility | Baseline positioning |
|---|---|---|
| **Direct hand/body control** | A free hand or suitable body contact can grip or lever the weapon hand, wrist, hilt, or comparable control point. Universally available when physically plausible; no mandatory Training. | Normally requires entering close bodily measure. |
| **Weapon-assisted capture or leverage** | The implement has an **actually suitable hooking, trapping, catching, or levering feature**, an explicitly authored Disarm-capable technique, or another *already-established* source of comparable leverage. | Uses only its genuinely usable method Reach; no free bodily entry. |
| **Established Grapple control** | An existing Controller has a **usable contact method** against the Controlled creature's item. Control is positional permission, not automatically a secured weapon hand. | Already shares the Grapple square; see Grapple Disarm. |

Examples: gripping a swordsman's wrist with a free hand **qualifies** if close contact is possible; an appropriate hooked polearm catching a weapon shaft **qualifies** if its geometry really provides leverage; a Controller manipulating a reachable weapon wrist **qualifies** if the requisite limb is free. An ordinary sword hit against a blade, a mace blow against fingers, a normal Guard/parry, or claiming any weapon strike is a "bind" **does not by itself qualify**. Damaging a hand belongs to an actual weapon attack or Called Shot, not this non-damaging contest.

A weapon profile alone neither grants Disarm eligibility nor a modifier. A real hook/trap geometry can authorize a one-action attempt without establishing a **persistent weapon-bind state**; weapon-specific traits and authored Disarm techniques may later formalize access. The GM adjudicates real geometry, not a blanket permission granted by narration. A method that cannot overcome both grips on a two-handed weapon cannot release that weapon.

Recheck item, grip, reach, and contact prerequisites **after responses** and before the contest resolves. An impossible interaction never becomes possible because of a high roll.

## Ordinary Disarm and Close-Contact Opportunity

Use **ordinary Disarm** against a creature **other than the actor's own Grapple partner**, including a named, physically accessible item of a participant in someone else's Grapple.

If the chosen method must **enter close bodily measure** and the target threatens the attacker, it creates the normal **Close-Contact Opportunity** before the Disarm Contest:

- the target receives an eligible Opportunity under [Opportunity Response](initiative-and-round-structure.md#opportunity-framework);
- a hitting Opportunity Attack applies **-2 to the ensuing Disarm Contest**, in addition to damage and its normal consequences;
- a hit does not automatically Interrupt Disarm, though injury, displacement, or another effect may make it physically impossible.

A qualifying weapon-assisted method operating entirely within its **already usable contact distance** creates **no additional Close-Contact Opportunity** merely from attempting Disarm. Such contact spends no MP and does not create shared-square Grappling State. The absence of an Opportunity is a positional advantage, **not** an automatic bonus to the contest.

Against a target engaged in a different Grapple, designate exactly one holder/item. This is not an outside **Committed Strike** and cannot transfer to the other grappler.

## Shared Disarm Contest

Both ordinary and Grapple Disarm resolve as the same opposed contest.

Attacker:

~~~text
Disarm Pressure =
d20
+ Strength or Agility
+ applicable Training
+ Disarm modifiers
~~~

Defender:

~~~text
Grip Resistance =
d20
+ Strength or Agility
+ applicable Training
+ 6 Grip Retention
+ Grip modifiers
~~~

**Strength** applies to forceful leverage, wrenching, and resisting a pull. **Agility** applies to timing, technical leverage, grip repositioning, and controlled twisting. Each participant uses the **single Ability that plausibly fits the actual method**. Narrow relevant Training applies when that learned skill materially helps. Neither participant substitutes the two-Ability weapon Attack or Guard formula.

The **+6 Grip Retention** is the baseline advantage of securing an item already held. It applies **once per item**, not per hand, and does not stack with Shove's Hold Ground, Guard Defense, or an invented two-handed bonus. Holding with two hands matters to **physical eligibility**, but does not automatically add another numeric retention bonus.

At equal Ability, Training, and other modifiers, a valid attempt succeeds **22.75%** of the time. This is a game-balance target, not a real-world disarm frequency. Bonuses from specific authored equipment/techniques may modify Disarm Pressure or Grip Resistance; **there is no generic +2 from having a weapon hook, proximity, Grapple Control, or Pin**. Future weapon-bind and secured-limb techniques may grant a **single, non-stacking positional advantage**, with exact values defined in those later rules rather than inferred here.

| Contest result | Consequence |
|---|---|
| Disarmer beats Grip Resistance | Holder releases the named item |
| Exact tie | Holder retains the item |
| Holder beats Disarm Pressure | Holder retains the item |

Failure or tie does not automatically reverse a Grapple, disarm the actor, damage either creature, or confer another condition.

A holder that is genuinely unable to make any plausible active grip resistance does not roll. The Disarm succeeds automatically if the actor can *actually* complete the release. **Prone, Controlled, and Pinned do not alone prove inability to resist.** Inability to resist never bypasses an impossible contact or release mechanism. The Attack roll's natural-1/20 and critical procedures do not apply.

## Attempt frequency

Each creature may **declare at most one Disarm against the same specific item during any one turn**, including eligible out-of-turn actions resolving in that turn. A failed or interrupted declared attempt counts. Another creature may attempt a Disarm independently if it has a valid action and method; allied cooperation is not an automatic bonus. A different item may be targeted separately.

This prevents one high-Tempo creature from repeatedly fishing for a successful item release before its Attack Sequence without granting the target blanket immunity from coordinated opponents.

## Grapple Disarm

Against the **other participant of the same Grappling State**, use **Grapple Disarm**:

- only the **Controller** may declare it. A Neutral participant must Gain Control and a Controlled participant must Reverse Control first;
- it costs **one Physical Action**, names a specific item held by the Controlled creature, and uses the **same Disarm Contest**, including +6 Grip Retention;
- no new Close-Contact Opportunity occurs **between the Grapple partners**, because they already share close bodily measure;
- Grapple Control **grants permission**, not an automatic numeric bonus, weapon-hand restraint, free limb, or assured release;
- the Controller must have an eligible free-hand, suitable implement, or other physically valid contact method, accounting for limbs already committed to Grapple/Pin;
- after success, tie, or failure, the existing Grappling State, Controller/Controlled position, and independently maintained Pin remain unchanged.

A Pin matters only through the body parts it actually restrains. A Controller cannot claim a limb is required to maintain Pin and simultaneously use that same limb for an incompatible Disarm. Persistent **secured weapon-hand or limb control** is separate future rules content, not a free consequence of Grapple.

The Controlled or Neutral participant cannot evade these restrictions by calling its attempt an ordinary Disarm against its current Grapple partner. Ordinary Disarm against someone **outside** the current Grapple remains physically possible only if the actor truly has the free limbs/reach required.

## Item release, defensive consequences, and battlefield control

On success:

- the named item drops **at its holder's current position** (the shared square if Grappling);
- the disarmer does **not** automatically catch, seize, wield, throw, or relocate it;
- neither creature is inherently displaced, made Prone, damaged, or placed in another condition;
- the drop itself creates **no Movement Opportunity**;
- item-dependent Attack profiles, Guard instruments, and other benefits become unavailable until a legal alternative is established; previously committed AP and defense capacity are not refunded.

**Being Disarmed does not consume or disable the victim's Reaction, Opportunity Capacity, or active Opportunity Response.** It may instead make a particular Opportunity Attack **illegal**, if the victim no longer has any usable melee weapon, natural attack, or other explicit melee capability. Re-evaluate the victim's **Melee Reach/threatened squares** from the attacks still legal in the new equipment/body state. A retained shield or other legal Guard instrument remains usable. The disarmed creature still occupies space and can impede passage under normal occupancy rules.

When a Guard was already assigned in an Attack Sequence and its required instrument disappears before that attack's resolution, use the [lost-Guard fallback](defensive-responses-and-criticals.md#guard-instrument-lost-after-defense-assignment). Disarm does **not** automatically turn every committed Guard into an unopposed hit.

An item landing over an unsupported surface or in a hazard follows actual environment/hazard rules when those exist. No automatic collision/falling-item damage arises from Disarm.

## Recovering a dropped item

A creature with a usable hand can retrieve and ready **one reachable dropped item** when the item is genuinely accessible; normal physical restrictions from Grapple, Pin, occupancy, support, posture, or barriers still apply. The item must no longer be held by another creature.

| Recovery | Cost | Exposure |
|---|---|---|
| **Quick Recovery** | **One Physical Action** (normal Focus-based Physical AP cost) | Creates a **Recovery Opportunity** for each eligible enemy currently threatening the recoverer's square |
| **Guarded Recovery** | **One Full Action** | Creates **no Recovery Opportunity from the retrieval itself** |

**Quick Recovery:** Declare the specific item, commit the Physical Action cost, and open the response window **before the item is picked up**. Each eligible threatening enemy may make at most one Opportunity Attack from this Recovery Opportunity, subject to their existing Reaction/Opportunity Response and round Opportunity Capacity. Each enemy is assessed independently; this is one authored action-trigger Opportunity, not a Movement Opportunity.

The item is **not yet ready** when those Opportunity Attacks resolve, so it cannot be used to Guard them. A generic hitting Opportunity Attack does **not automatically Interrupt recovery**; resolve its ordinary consequences, then recheck whether the item is still reachable and recovery physically possible. Successful recovery picks up and readies the item as part of the same Physical Action, without a second draw cost. If recovery becomes impossible, the action is lost under ordinary committed-action timing.

**Guarded Recovery:** A Full Action requires the creature's entire original Turn AP allotment to remain available and consumes it all. It represents a deliberately protected retrieval. It avoids only the **Recovery Opportunity** generated by retrieving the item, not independent movement, Standing, spell, or other authored Opportunities, and is not a blanket immunity to attacks.

Both methods remain subject to actual limb/posture restrictions. **There is no universal free Reaction to catch or retrieve a disarmed item.** Specialized reactions/techniques may define such an option later. Drawing a stored replacement item still uses its separately authored General Tempo Action cost (24 AP); it is not the same action as retrieving an item from the ground.

## Action and defense timing

Disarm is a **non-damaging maneuver contest**, **not** an ordinary weapon Attack or a member of an Attack Sequence. Its defender rolls Grip Resistance rather than selecting Take Hit, Dodge, or Guard for the Disarm Contest; no Guard capacity is spent and no Dodge Pressure incurred by that contest alone. Disarm creates no automatic Riposte Opening.

A Disarm cannot be inserted into the middle of an already committed Attack Sequence to change its attack profiles or the defender's earlier defense assignments. Ordinary attacks against that target still obey the [one Attack Sequence per target per turn](initiative-and-round-structure.md#attack-sequence) rule.

A legal Disarm resolving during an Interception or other valid response window can change whether a later action still has the item necessary to resolve. Recheck legality through the normal response procedure. **Disarm is not an automatic Interrupt** and never retroactively refunds or uncommits unrelated actions.

## Deliberately deferred

This v0 does not define persistent limb/weapon control, formal weapon-bind states, catch-and-seize in the same action, remote theft, forceful strap removal, special shield/two-hand retention values, creature size/anatomy exceptions, a universal unarmed Guard profile, or specific equipment-based Disarm bonuses. Weapon-control and Limb Control systems may authorize additional methods or bonuses later; they must explicitly state what they change.
