# Prepared and Spontaneous Ammunition v0

> **Proposed executable v0 ammunition infrastructure.** Restores the three-mode design intent from the [historical Core Rules Audit v34](../../design/audits/Veilbound_Core_Rules_Audit_v34.md), but supersedes its obsolete **Full Recovery** expiration trigger with the current [six-hour VP recovery](../07-veil-magic/volition-points.md#recovery). **Only a specifically authored technique can enchant ammunition or receive a preparation discount**; this page does not grant all spells those abilities. Refer to [Conjure Flame v0](../07-veil-magic/conjure-flame-v0.md) for the first complete ammunition effect.

## Ammunition modes

| Mode | What is fired | Payment | Availability |
|---|---|---|---|
| **Mundane** | Ordinary physical arrow/bolt | No VP; expend ordinary ammunition | Existing bow/crossbow baseline |
| **Spontaneous enchanted physical** | One physical arrow/bolt with one authored effect applied during its shot | Full technique's **Spent VP per fired shot** | Only an effect with an **Ammunition Shot** integrated-casting profile |
| **Prepared enchanted physical** | One previously enchanted real arrow/bolt | **Spent VP at preparation**; no second payment for the already prepared effect when fired | Only a technique expressly allowing preparation |
| **Veil Arrow** (candidate, not executable here) | A future magically generated temporary arrow | Future authored cost/eligibility | [Universal Veil backlog](../07-veil-magic/universal-veil-fundamentals.md#status-and-work-order) |

Ordinary arrows/bolts retain the normal physical attack, range, Penetration, defenses, line of fire, ammo consumption, and bow-versus-crossbow action costs. A magic effect **does not itself create ammunition**, replace ammunition cost or circumvent reloads.

## Integrated on-shot activation (0 additional AP)

When a technique explicitly supports an **Ammunition Shot** profile with integrated activation, the caster **declares the spell, Used Tier, contribution, and exact shot** as part of the ordinary ranged Attack declaration. **No additional Projection Action/AP** is charged. The **underlying bow Physical Action or heavy-crossbow Full Action** remains mandatory; the action cannot occur at 0 AP on its own.

- **Pay/commit normal shooting AP first**, obeying Attack Sequence declarations, prior defense assignment, ranged Opportunities, Aim, cover and the full-reload rules. A zero-additional-AP magic attachment grants **no extra shot, Reaction or out-of-turn timing**.
- For a spontaneous effect, verify enough **Available VP** for each declared enchanted shot. Declare all enchanted shots and their total maximum VP demand before an Attack Sequence's first roll, so one VP cannot promise multiple shots. Each individual shot **spends its VP when the projectile is actually launched**, before its attack roll; a miss, Guard/Dodge defense, interception **after launch**, or consumed ammunition does not refund VP.
- If an action is **Interrupted or rendered illegal before projectile launch**, its committed shooting AP remains lost under normal combat rules, but **unlaunched** spontaneous-effect VP is not Spent and an unfired prepared arrow is not consumed merely for being selected. Do not reassign that declared enchantment to a different already-committed attack mid-sequence.
- Once launched, the effect travels with **that one projectile**, applies the authored on-hit packet to a target it actually hits, and ends whether it hits, is stopped by cover, misses or otherwise finishes that shot. The effect does not persist on a fired projectile for future attacks unless a technique explicitly says so.
- An ammunition enchantment's on-hit effect does not independently roll a second attack or direct Veil resistance merely because its origin was magical.

An integrated shot still counts as one **ordinary Attack** for Attack Sequence and ordinary weapon critical rules, not a separate spell attack. If a specific future technique needs a distinct spell action, it must explicitly say so and establish compatible timing.

## Prepared physical ammunition — provisional playtest procedure

An effect with an expressly authorized **Prepared Ammunition** mode may be applied to real ammunition **outside an immediate shot**:

1. During **10 uninterrupted minutes of suitable preparation**, select **1–20 individual physical arrows/bolts** (one ordinary quiver-size batch) that the preparer possesses and can work on. Choose **one authored eligible technique**, its supported **Ammunition Shot** profile and a legal **Used Tier** for the batch. **The tier and any caster-derived scaling inputs specified by that technique are locked at successful preparation completion**, not upgraded when fired. For Conjure Flame, record **the preparer's max(0, Veil Control)** and the Used Tier on **each individual arrow/bolt**. This stored value is not the eventual shooter's VC.
2. **Spend** the technique's stated **per-projectile preparation VP** for **each** arrow/bolt now; a smaller batch costs proportionally less. All VP must be Available when paid. **No VP is Committed to the ammunition**, and no VP returns automatically if unused arrows expire. A caster unable to pay for every declared arrow may instead choose a smaller batch.
3. Mark each prepared arrow/bolt and its **individual expiry exactly 24 hours after completion**. Only one **major ammunition enchantment** can occupy any one physical projectile at a time under v0; attempting to prepare a second major effect onto an already enchanted arrow is illegal until the original expires or is consumed.
4. **Firing a prepared arrow/bolt** uses only its ordinary ranged attack action and zero additional spell AP/VP for the **prepaid effect**. A valid hit receives the stored **effect formula and recorded scaling inputs**. **Roll random damage dice when the shot actually hits**, not at preparation; add the stored numeric caster coefficient rather than replacing it with the shooter's stats. The projectile consumes that enchantment when fired, even if it misses. An unfired expired projectile becomes mundane ammunition; it is not destroyed by expiration.
5. Prepared effects **persist if the quiver is dropped or the arrow changes hands**; they are attached to individual physical ammunition, **not** a wielder-maintained VP reservation. Transfer does not grant the new owner knowledge of the spell or change **the recorded preparer's scaling inputs**. Use the **actual shooter's ordinary weapon accuracy and physical-attack statistics**, but the prepared magical output remains the preparer's stored effect regardless of who fires it. A particular future technique may explicitly specify different snapshot rules before being playable.
6. **VP recovered in six-hour ticks does not dispel prepared ammunition**, accelerate expiry, return already Spent preparation VP or extend a projectile's lifetime. Repeated preparation/rest cycles cannot create **permanent** stored enchantments: every batch independently expires within 24 hours. Future economic/concurrent-stock caps may be calibrated if such daily preparation creates excessive stock.

**Preparation time (10 minutes/batch), size (up to 20), the 24-hour lifetime and technique-specific discounts are v0 playtest values**, not a claim that every character can mass-enchant arrows. Preparation is an extended noncombat procedure; **not** a Full Action that converts 20 arrows in one combat turn. Interruption before completion creates no prepared arrows; no VP is spent until preparation completes and the chosen batch is successfully bound.

## Conjure Flame ammunition pricing — v0 playtest

| Conjure Flame ammunition use | Spent VP |
|---|---|
| One **spontaneously enchanted** physical arrow/bolt at Used Tier T | **2 × T**, paid when fired |
| One **prepared** physical arrow/bolt at Used Tier T | **1 × T**, paid during preparation |
| One batch of N prepared arrows/bolts (1–20, same T) | **N × T**, paid on completion |

Prepared ammunition uses the technique's **Primary Ammunition Shot output at the locked Used Tier and recorded preparer VC**, **not Secondary** merely because it was prepared. For an immediately enchanted shot, Conjure Flame instead captures the caster/shooter's VC **at projectile launch**. In neither case is VC recalculated on impact; only the **damage die** is rolled on a successful hit. The discount is for committing preparation time and upfront Spent VP; this is **not** a permanent investment, no Reserve refund applies, and it is **not** a new VP state.

**Worked example:** Tier 1, 10 prepared arrows = **10 Spent VP** after 10 minutes, versus **20 Spent VP** across 10 spontaneous Tier-1 shots. They expire in 24 hours even if none are used. With fewer Available VP, prepare fewer arrows.

## Explicitly deferred

- **Veil Arrow** (working name for the historical *Ethereal Arrow*): proposed creation of transient magical ammunition during a shot, historical **1 VP per arrow**, possibly combined with an eligible effect for full effect VP + creation VP. **Not automatically unlocked, not yet an executable spell and not itself a physical arrow eligible for batch preparation.**
- Ammunition crafting, magical recovery of spent arrows, exceptional ammunition, permanent rune/enchanted quiver inventory, stacked major enchantments, re-enchanting fired projectiles, stacking multiple integrated spells on one shot without authorization and generalized preparation discounts for unrelated spells.
- **Composite Casting** is possible only when its Primary and Secondary share an authored exact profile and the combined shooting/cost timing is legal; [Scholar rules](../08-archetypes/scholar.md) and [Technique Structure](../07-veil-magic/technique-structure-v0.md#8-existing-high-scholar-composite-casting-and-future-contribution-interfaces) govern the full VP cost of **both** components. Integrated 0-additional-AP attachment never creates a free weapon attack.
