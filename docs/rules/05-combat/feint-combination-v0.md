# Feint Combination v0

> **LOCKED native foundation; numeric modifiers remain playtest-calibratable.** Feint is a two-strike, credible melee combination that trades the chance of landing **both** attacks for a better chance of landing **at least one** against an actively defending opponent. It uses the existing [Attack Sequence](initiative-and-round-structure.md#attack-sequence), [Physical Action costs](action-categories-and-physical-tempo.md#focus-action-costs), and [Guard/Dodge/Take Hit](defensive-responses-and-criticals.md#declaring-defense) procedures; it does **not** introduce a secret declaration, independent deception contest, extra Reaction, or universal defense-resource drain.

## Definition and action cost

A **Feint Combination** links **two consecutive ordinary melee attacks** against **the same target** inside the attacker's ordinary on-turn Attack Sequence:

1. **Feint opener:** a genuine, fully damaging melee attack whose deliberate deceptive timing and direction impose **-2 on its Attack roll**.
2. **Committed follow-up:** a second genuine, fully damaging melee attack, resolved with a conditional accuracy modifier determined **only by what actually happened to the opener**.

Both attacks consume their **normal Physical Action AP cost**, separately: total **2 x Physical Action cost** for the pair (High Focus 60 AP, Medium Focus 48 AP, Low Focus 40 AP). Neither attack is free, and the Feint Combination grants no extra attack or action. The attacker must have enough **currently unspent Turn AP for both** when declaring the sequence; unused AP from other turns cannot be saved or pooled.

The attacks must be individually legal melee strikes delivered with usable weapon(s), limbs or an otherwise legal melee attack method. The two weapon/profiles may differ if the creature can actually use each in the declared order, but the attacker cannot bypass equipment changes, reload, grip, reach, or other ordinary prerequisites. No special Training proficiency is required **in addition** to the legal ordinary attacks: the two-action tempo is the actual universal access gate.

An Attack Sequence may include other ordinary attacks before or after the pair. Different **non-overlapping** pairs may be declared in one sequence when the actor can pay for them; one attack cannot be simultaneously a follow-up and the opener of another combination. This v0 imposes **no arbitrary once-per-turn limit**. Granted no-AP attacks (such as an extra off-hand attack) and out-of-turn Reaction/Opportunity/Interception attacks cannot fill either slot unless an explicit later technique authorizes it.

## Low-level access: deliberate training-and-tempo gate

The Feint Combination is **not available at low level when the character lacks the Turn AP to commit two Physical Actions**. This is intentional for v0.

In the fiction, the character **has not yet developed the trained timing, follow-through, and combat tempo needed to execute this skilled two-strike deception**. This explanation does not create an additional Training rank, feat, class, or equipment prerequisite. Gaining enough Turn AP is the mechanical representation of growing competence, regardless of Focus.

Using the current [Turn AP progression](action-categories-and-physical-tempo.md#turn-action-points):

| Focus | One Physical Action | Total Feint AP | First level with enough Turn AP |
|---|---:|---:|---:|
| Low — Embodiment | 20 AP | **40 AP** | **Level 3** (42 Turn AP) |
| Medium — Routing | 24 AP | **48 AP** | **Level 4** (48 Turn AP) |
| High — Projection | 30 AP | **60 AP** | **Level 6** (60 Turn AP) |

A creature below its applicable threshold cannot declare a Feint Combination, even if an unrelated effect grants an attack without AP cost; a later **explicitly authored exception** may say otherwise. Levels above the threshold still require enough unspent AP **at declaration time**.

## Declare openly before defenses

Before the Attack Sequence starts resolving, the attacker:

1. Declares **all ordinary attacks** committed against the defender under the normal Attack Sequence procedure.
2. Identifies every Feint Combination's **two consecutive paid melee attacks**, including which is the **opener** and which is the **follow-up**.
3. Declares the target, each weapon/profile, other attack-specific choices, and commits **all** associated AP.
4. Lets the defender assign **Take Hit, Dodge, or Guard separately for every attack** before the first roll of the sequence.

**The Feint designation is public.** The defender can choose the most appropriate defense with knowledge of the declared combination. The player does not secretly mark an attack as a Feint, nor may the attacker retroactively choose the Feint after learning a defense or seeing a roll.

The opener is a **real, damaging attack**, not a harmless fake: choosing Take Hit against it exposes the target to normal melee Take Hit rules (normally an automatic hit except a natural 1). There is no option to “ignore the feint” without accepting that real threat.

## Resolve the opener and follow-up

Resolve the opener as a normal melee attack with **-2 on its Attack roll** and **normal weapon damage and Penetration on a hit**. It receives its normal individual response window and ordinary natural-1, natural-20, and critical procedures.

When its linked follow-up later resolves, determine the **one** conditional modifier using this table:

| Resolved opener outcome | Follow-up's Attack modifier |
|---|---:|
| Defender **successfully Guards** the opener (stops the attack) | **+4** |
| Defender **successfully Dodges** the opener (avoids the attack) | **+4** |
| Opener hits, including a hit against Guard/Dodge or a chosen Take Hit | **-2** |
| Opener is a natural 1, is Interrupted, becomes illegal, or otherwise fails to create a qualifying successful Guard/Dodge | **-2** |

The **+4 Opening** exists only on the **single linked follow-up** against **the creature that actually defended the opener**. A defense choice alone is insufficient: the defense must **succeed** against a resolved, otherwise legal opener. The opening is an immediate result of the actual Guard/Dodge, not a general condition, token, stacking bonus, future-turn effect, or separate attack. A natural-1 opener never earns the +4 even if Guard or Dodge had been assigned.

If the defender chose Guard or Dodge but the opener hits, the attacker receives **-2**, not +4. If the defender chooses Take Hit, the opener still deals its normal damage when it hits, and its follow-up is **-2**.

The follow-up resolves with its **own attack roll, defense, response window, normal damage, and critical rules**. It receives **+4 or -2**, never both. This Feint modifier changes accuracy only; **both strikes always retain their normal weapon damage**. The conditional modifier is determined when the follow-up resolves; it does not reopen its already-declared weapon/profile or the defender's already-assigned defense.

If the opener is cancelled, the follow-up is **not automatically cancelled**. It still costs the AP already committed, resolves at **-2** if it remains legal, and follows the ordinary Attack Sequence and [Interception-versus-Interrupt](initiative-and-round-structure.md#interception-versus-interrupt) rules. If the original target becomes illegal and the general Attack Sequence redirection rule permits the follow-up against another target, its conditional **+4 never transfers** to a different target: it resolves at **-2**, with its committed weapon/profile unchanged.

## Defense resources and tactical niche

Defenses use the **existing** round-side system:

- Choosing **Guard** spends ordinary Guard capacity as usual, regardless of whether it successfully stops the opener. A successfully Guarded opener can grant the follow-up +4; **no second Guard use** is imposed by Feint.
- Choosing **Dodge** adds ordinary Dodge Pressure as usual. A successfully Dodged opener can grant the follow-up +4; Feint **does not add extra Dodge Pressure**.
- Choosing **Take Hit** against the opener preserves Guard/Dodge resources but risks its normal full-damage hit. Feint **does not** force a Guard or Dodge choice.
- Any later attack's defense choice and legality remain governed by already-assigned Attack Sequence defenses and applicable mid-sequence legality/fallback rules.

Feint is especially useful when landing **at least one** melee hit against a highly active Guard/Dodge defender matters more than maximizing the chance of landing **both** strikes. The **-2 on the opener and -2 on the follow-up after an actual hit** are deliberate costs: two ordinary attacks retain the stronger chance to connect twice. Enemies able to absorb the opener with Take Hit, ordinary attacks against poorly defended targets, and situations where the combination cannot reach the same target may favor ordinary attacks instead.

**No other creature may exploit the +4:** it belongs only to the paid, linked follow-up, not to allied attacks, a different Attack Sequence, a Riposte, or an unrelated melee strike.

## Illustrative sequence

At 120 Turn AP, a Low-Focus attacker can commit three ordinary sword attacks against one defender for 60 AP. The attacker declares **attacks 1 and 2 as the Feint Combination**, with attack 3 ordinary; all three profiles, choices and AP are committed, then the defender assigns defenses to all three.

- **Attack 1** (opener) rolls its normal sword attack at **-2**. The defender's assigned Guard stops it.
- **Attack 2** (linked follow-up) rolls its committed sword attack at **+4** against its separately assigned defense. Whether it hits or misses, it consumes the same normal 20-AP Physical Action cost.
- **Attack 3** is unaffected. The Feint opening cannot be transferred to it even if attack 2 was interrupted or missed.

If instead attack 1 hits, attack 2 rolls at **-2**. The first hit's damage is fully normal, and attack 3 remains unaffected.

## Deliberate v0 calibration boundaries

**LOCKED v0:** two consecutive paid genuine melee attacks in one ordinary Attack Sequence; open declaration before defenses; two Physical Action AP costs; **-2 opener / +4 after a successful Guard or Dodge / -2 otherwise**; normal damage; no forced defense expenditure, hidden bookkeeping, separate Feint contest, automatic ally benefit, overlapping pair, or arbitrary per-turn limit; access naturally gated by current Turn AP.

**Playtest watch:** the exact -2/+4/-2 numerical values, high-Guard versus high-Dodge outcomes, natural-20 interactions, the defender's Take Hit choice under heavy armor, and whether a successfully Guarded/Dodged opener should someday need a minimum threat/margin to earn the +4. That last margin rule is **not** part of v0.

**Deferred:** harmless standalone false attacks, out-of-turn deception, ranged or projected Feints, special equipment/Training variations, extraordinary combo exceptions, and ally-wide deception openings.
