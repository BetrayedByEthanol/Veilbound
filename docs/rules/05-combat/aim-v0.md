# Aim v0

> **LOCKED native universal precision-setup maneuver; the +4 maximum is a playtest calibration value.** Aim is an extra Physical Action spent preparing **one specified ranged attack**, not an attack itself and not an Interception or Interrupt. It reduces one declared source of **applicable shot difficulty** for that attack, rather than giving a universal Attack bonus. [Turn AP and Physical Actions](action-categories-and-physical-tempo.md), [Ranged Defense](off-hand-and-ranged-combat.md), and [Interception / Attack Sequences](initiative-and-round-structure.md) remain authoritative for those systems.

## Purpose and cost

Ordinary ranged attacks already include choosing a target, orienting the weapon, judging distance, and firing. **Aim** represents **additional** deliberate preparation for a difficult shot.

**Aim costs one Focus-priced Physical Action** from the shared Turn AP pool:

| Focus | Aim | Aim + an ordinary paid Physical Action attack |
|---|---:|---:|
| Low | 20 AP | 40 AP |
| Medium | 24 AP | 48 AP |
| High | 30 AP | 60 AP |

The second column is the **Aim action alone**; the combined totals assume the subsequent attack itself costs one normal Physical Action. A projected technique pays its **own separately authored action cost**, not an assumed Physical Action cost. Aim **does not make the subsequent attack free**, generate extra attacks, or modify Physical Tempo.

The character may Aim even if insufficient Turn AP remains to fire during that same turn, provided the Aim action itself is legal and affordable. The prepared Aim may carry into a later turn subject to its expiration and break conditions.

## Binding declaration

When declaring Aim, and **before committing its AP**, the character chooses:

1. **One designated, currently observable target**, which may be a creature or a precise physical point/object that a legal ranged attack could target.
2. **One specific ranged attack profile**: weapon or physical delivery method and the ammunition, projectile, or effect-bearing variant to be used. If a projectile carries an explicitly authored on-hit effect, identify its chosen delivery profile here.
3. **One precise aiming objective and one associated difficulty source**, for example *offset this target's range difficulty*, *thread a visible gap in partial cover*, *hit a particular exposed body location using a legal Called Shot*, or *place a shot through an opening between combatants*. The objective is **not** a floating accuracy bonus that can be reassigned later.

The shooter must be able to meaningfully observe/track that target, have physically usable aiming equipment or a valid aimed delivery method, and be capable of preparing the stated profile. Aim does not create a legal shot through an entirely opaque or physically blocking obstacle.

The same chosen target, attack profile, and objective must remain in force when the aimed attack is declared. **Changing any of them loses the Aim**, without refunding the preparation AP. Target movement or a change in range does not by itself invalidate the declaration if the same target remains meaningfully tracked and the profile/objective remain usable; evaluate the actual difficulty at release.

A named aim objective does **not** grant an unauthorized Called Shot, movement-triggered shot, special spell delivery, status effect, or new attack mode.

## Benefit: mitigate a particular shot difficulty, up to 4

For **one subsequent otherwise legal ranged attack** using the exact declaration, reduce **one selected, positive, applicable shot-difficulty modifier** by:

```text
Aim mitigation = min(4, max(0, selected applicable shot-difficulty modifier))
```

The affected difficulty is reduced by that mitigation **to no lower than 0**. Aim does not add an unconditional +4 to the attack roll and cannot turn a favorable negative modifier into an additional bonus.

Eligible difficulty is a **shot-condition modifier that actually applies to the chosen attack and relevant defense calculation**. Current examples include positive Range Difficulty and the **numeric Cover Difficulty now authored by [Cover and Line of Fire v0](cover-and-line-of-fire-v0.md#cover-difficulty-tiers)**. Future authored examples may include intervening combatants, small exposed targets, or **legal** Called Shot location difficulty. If the applicable rule lacks a numeric targeting penalty or if the penalty does not apply to a particular defense, **Aim has nothing to mitigate in that calculation**. Do not invent a cover, melee, or Called Shot modifier merely to use Aim.

- If a difficulty source contributes to both static Ranged Defense and active Ranged Dodge (such as **Range Difficulty**), apply the mitigation to that source in **whichever defense actually resolves** the shot; do not apply the same mitigation twice.
- If the source contributes only to static defense, reduce it only there. Cover Difficulty is present in active Ranged Dodge **only because the independently authored [Cover and Line of Fire v0](cover-and-line-of-fire-v0.md#apply-cover-to-the-selected-ranged-defense) adds it**. Aim still cannot insert an unauthored modifier into a defense.
- If there is no positive modifier from the selected source when the shot resolves, Aim gives **0 benefit**; it does not transfer to another source or become an attack bonus.
- Aim does not reduce Armor, Penetration requirements, a defender's **Agility, Awareness, Evasion Bonus, or Dodge Pressure**, weapon handling/action costs, or independent attack/resistance tests.
- Aim cannot turn an **illegal or physically blocked line of fire** into a legal shot. It does not erase an interposing body, solid wall, barrier protection, or the eventual consequences of a missed shot.

**Examples with existing bow range bands:** Aimed **Medium** range changes its +2 source to +0; **Long** changes +5 to +1; **Extreme** changes +8 to +4. A point-blank/Close range modifier of -2 remains -2: Aim does not change it. **Cover Difficulty is now canonical at +2/+4/+6/+8** where a partial-cover geometry applies; illustrative +6 Called Shot or shooting-into-melee penalties remain **noncanonical** until separately authored.

The aim benefit is capped at **4 for the selected source**, even if the character has taken several Aim actions.

## Duration, consumption, and breaking Aim

Aim takes effect only **after its Physical Action resolves successfully**. An explicit Interrupt or loss of prerequisites during the Aim action prevents the preparation from becoming active; its already-committed AP stays spent under normal rules.

Once established, Aim lasts until **the earliest** of:

- the first attack using its declared target/profile/objective **begins**, whether it hits, misses, is Interrupted, or becomes illegal after commitment;
- the shooter changes the declared target, attack profile, or objective; deliberately changes its firing position; loses control/use of the necessary weapon or delivery method; or can no longer meaningfully track the designated target;
- a Dodge, displacement, posture/position change, or other event **actually disrupts** the prepared firing position or the ability to maintain the specified shot;
- the **start of the shooter's second subsequent turn** after the turn in which Aim completed.

Thus Aim established on turn 1 remains eligible during turn 1, the intervening turns of other combatants, and turn 2; it **expires at the start of that shooter's turn 3**. There is no unlimited carried bonus from repeatedly postponing the shot.

Target movement **without losing track** does not by itself break Aim. A momentary change in range recalculates its chosen difficulty source; target movement behind complete cover may prevent a legal shot until the obstruction clears, but the shooter may retain preparation only while it can **meaningfully track** the same target. Being attacked or merely suffering damage is **not automatically** an Aim-breaking Interrupt; apply only actual effects that invalidate preparation. An attack that begins consumes Aim before its own response window even if that response subsequently Interrupts the shot.

A character may hold **at most one active Aim preparation**. Starting another Aim replaces the previous one when the new Aim completes; Aim's benefit cannot stack with itself. The character cannot accumulate bonuses by repeating Aim actions.

## Attacks, timing, and Interception

An Aim action is **not an attack**, does not deal damage, and does **not** itself create an Attack Sequence. It does not automatically open a shot or grant Interception/Interrupt timing.

**Ordinary on-turn shot:** When later declaring the actual aimed attack, pay its separate action cost normally. If it targets a creature that receives an [Attack Sequence](initiative-and-round-structure.md#attack-sequence) from the shooter that turn, commit **all ordinary attacks in that target's sequence** before its first roll, and tell the defender which **single attack** has the already-locked Aim benefit. The defender assigns defenses with the profiles and shot modifiers known; no other attack in the sequence inherits Aim and no modifier is transferred after seeing an outcome. Ordinary one-sequence-per-target rules still apply.

**Prepared Interception shot:** Aim can be established **before separately reserving one legal ranged attack as an Interception**. The reservation commits its **own AP or Full Action** and has its own specific trigger, expiry, and normal [Interception timing](initiative-and-round-structure.md#interception). **An atomic Interception cannot package Aim + Attack together.** If the attack releases while Aim is still valid, it may use Aim; if the trigger never occurs or Aim has expired/broken, the reserved attack's normal commitments/expiry still apply and there is no retroactive refund. Interception takes place **before** the declared triggering event, so a target emerging from solid cover is not automatically exposed when the earlier Interception would resolve. Recheck attack legality and line of fire normally.

**Heavy crossbow:** A heavy-crossbow shot remains a **Full Action**, and reloading remains another Full Action. Aim does not reduce either cost or allow Aim and heavy-crossbow firing in the same turn under ordinary rules. A retained Aim from a prior turn may apply when a later legal Full-Action crossbow shot resolves. Full-Action Interception is allowed only when its action is **otherwise eligible** under the existing reservation rule; Aim does not grant eligibility.

**Magical delivery:** Aim may mitigate an applicable physical/ranged shot difficulty for an **otherwise legal manifested projectile, pointed beam, or effect-bearing ammunition attack** that actually uses a ranged attack roll, provided its authored casting/delivery method can support maintaining the declared aimed profile. The projectile/technique keeps its normal attack formula, separate action/VP costs, and all effect magnitude/duration/resistance rules. Aim provides **no universal Veil Control, Resonance, Veil Integration, VP, damage, penetration, or rider bonus**. It does not apply to Direct Intrusion, a non-aimed area effect, or any effect without an eligible aimed ranged attack roll.

**On-hit disruption:** Aim only improves delivery of a **separately authored** mark, suppression, poison, disruption, or other on-hit effect; it **never** makes a successful attack Interrupt by itself. An attacker seeking to act before an opponent's action completes still needs **Interception or another explicitly authorized response**.

## Deferred integrations (do not silently import legacy rules)

- **Cover and line of fire:** [Cover and Line of Fire v0](cover-and-line-of-fire-v0.md) now defines numeric physical partial-cover tiers, directions/openings, and the one-roll cover-hit window. Aim can mitigate only a **declared, actually applicable** positive Cover Difficulty and never bypasses solid obstruction. More detailed cover destruction/penetration remains deferred.
- **Shooting into melee:** distinguish an engaged target with a genuinely clear shot from intervening allies/enemies, define authored targeting modifiers, and establish any friendly-fire/stray-hit and obstruction procedure. Being in melee does **not** itself gain a new universal penalty from Aim.
- **Called Shots:** author the native Turn AP-compatible Called Shot action, location difficulty, wound qualification and effect/Interrupt interactions. Legacy references to an entire "Attack action" are **not** automatically valid under Turn AP. Aim for a specific body part is only a preparation, not permission to inflict a wound or Interrupt.
- **Special precision techniques:** multiple-target aim, sniper traits, aim from moving platforms, special cover penetration, guided shots, and unusually stable magical targeting need independent explicit rules.
- **Calibration:** verify the **maximum mitigation 4**, single-use cadence, and cost of a Focus-priced Physical Action against two separate attacks, enchanted arrows with on-hit control effects, and low-level AP budgets.

## Examples

| Preparation and later attack | Outcome |
|---|---|
| Archer Aims at a tracked guard with the objective "compensate for Long range"; later fires that bow profile at Long range | Reduce the +5 range source by 4, leaving +1; consume Aim on attack declaration |
| The same guard closes to Medium range, remaining tracked | Reduce the then-applicable +2 source to 0, **not** +4 Attack |
| Target is at Close range (-2) despite long-range objective | No positive range difficulty to mitigate; Aim does not become a generic +4 |
| Archer Aims at one guard's exposed hand, then chooses a different guard or the head | Original Aim invalid; no transfer; any Called Shot additionally requires its own legal rules |
| Archer Aims with an enchanted suppression arrow and hits | Increase only hit likelihood where the chosen difficulty applies; effect resolves according to its own authored trigger, without amplified suppression |
| Archer Aims, then reserves a bow attack if the guard begins a spell | Separate atomic attack Interception; apply Aim if still valid; a hit only Interrupts when some **separate** effect explicitly provides Interrupt |
| Archer Aims from turn 1 but takes no shot before turn 3 starts | Aim expires at the start of the shooter's turn 3 |
| Archer moves to another shooting position or is knocked out of position | Prepared Aim is lost without refund |
