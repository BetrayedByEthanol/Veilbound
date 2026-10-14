# Dying and Wounds

> Canonical current wound framework. **0-HP overkill severity and default Repair Requirements now have deterministic v0 playtest values**; exceptional injury outcomes and individual injury effects remain calibration items.

## When wounds occur

Ordinary hits do not normally create persistent wounds.

A wound occurs only when:

1. a **Called Shot** successfully qualifies for a wound;
2. a **Devastating Critical** occurs; or
3. the target **first drops from positive HP to 0 HP or below** through a damaging event.

The exact Called Shot action cost and procedure remain unresolved. The legacy statement that a Called Shot consumes an entire **Attack action** is superseded by the shared Turn AP architecture and must be re-authored as an explicit AP or Full Action cost during the maneuver/weapon pass. Called Shots should continue to carry substantial location difficulty.

## Random wound location

When a wound occurs and the attacker did not specify a location, roll d20:

| d20 | Location |
|---:|---|
| 1–2 | Head / neck |
| 3–8 | Chest |
| 9–12 | Abdomen |
| 13–15 | Arm |
| 16–19 | Leg |
| 20 | Hand / extremity |

Weapon trauma type determines the relevant injury family.

| Location | Cut | Pierce | Crush |
|---|---|---|---|
| Head | Severe laceration; possible neck decapitation where physically plausible | Eye/brain penetration | Skull fracture / brain trauma |
| Chest | Massive open wound | Punctured lung / heart | Broken ribs / organ trauma |
| Abdomen | Evisceration / severe bleeding | Organ perforation | Ruptured organ / internal bleeding |
| Arm | Tendon/artery severance; possible amputation | Deep puncture / nerve injury | Shattered bone |
| Leg | Artery/tendon severance; possible amputation | Deep puncture | Shattered leg |
| Hand | Severed fingers/tendons | Pierced hand | Crushed hand |

## Wound severity

Severity is determined by the event that caused the wound rather than by a second random roll. A single damaging event with more than one qualifying wound trigger produces **one wound for that event**, using the **highest applicable minimum severity**, unless a separate explicitly authored effect creates an additional wound. Its actual location and trauma family still follow the relevant attack/hazard procedure.

The canonical wound ladder is:

> **Serious → Severe → Critical → Catastrophic → Irreparable or Fatal**

**Irreparable** and **Fatal** are different terminal outcomes:

- **Irreparable:** the character may survive, but ordinary natural Vigor regeneration cannot reconstruct the lost or destroyed structure. A fully severed limb is the baseline example. Prosthetics, exceptional reconstruction, or an explicit supernatural technique may still provide another solution.
- **Fatal:** the injury destroys a vital structure so completely that the character dies rather than entering the ordinary Dying process. Decapitation is the baseline example. Once actually dead, ordinary Vigor regeneration cannot restart the body.

Event guidance:

- **Called Shot:** normally Serious if it qualifies; exceptional results may upgrade to Severe, Critical, Catastrophic, or become Irreparable where the attack physically severs or destroys a structure.
- **0 HP:** use the following **deterministic v0 playtest severity bands** for the first damaging event that takes HP from positive to 0 or below. Measure the **HP immediately after that event**, including all damage bonuses and Armor, **before** later Dying losses or regeneration. Define `O = max(0, -HP after damage)` and `M = Maximum HP`:
  - **Serious** when `0 ≤ O < ceil(M / 3)`.
  - **Severe** when `ceil(M / 3) ≤ O < ceil(2 × M / 3)`.
  - **Critical** when `ceil(2 × M / 3) ≤ O < M`.
  - At `O ≥ M` the character has reached **HP ≤ -Maximum HP** and is **dead** under the existing death threshold; do not create an additional repairable wound as an alternative to death.
  - **Examples:** Maximum HP 10: at HP **0 to -3**, Serious; **-4 to -6**, Severe; **-7 to -9**, Critical; **-10 or below**, dead. Maximum HP 12: **0 to -3**, Serious; **-4 to -7**, Severe; **-8 to -11**, Critical; **-12 or below**, dead.
  - This determines the **default severity for HP overkill**, not an automatic amputation, precise organ injury, or extraordinary trauma location. A separately qualified **Devastating Critical** sets a minimum of Critical, even if the 0-HP band would be lower. Existing physically established Irreparable/Fatal destruction remains authoritative.
- **Devastating Critical:** at least Critical; sufficiently destructive results may become Catastrophic or Irreparable, and may be Fatal when the weapon, location, and circumstances physically destroy a vital structure. A Devastating Critical that also reaches 0 HP **does not automatically create a second wound**; use the stronger applicable severity and any independently established physical consequences.

**Additional wound timing boundary:** Already being at 0 HP or below does **not** create another new *0-HP-triggered* wound on each subsequent hit or Dying tick. Further HP loss still approaches the normal death threshold; a new separately qualifying Called Shot, Devastating Critical, or explicitly authored additional injury can still create its own wound.

## Repair requirement

Wound repair cost represents bodily trauma and does not scale with level.

| Severity | Baseline repair requirement |
|---|---:|
| Serious | **10 Vigor** (default) |
| Severe | **20 Vigor** (default) |
| Critical | **30 Vigor** (default) |
| Catastrophic | 40+ Vigor |
| Irreparable | Cannot be naturally reconstructed |
| Fatal | Immediate death; no natural repair |

For an injury without a more specific authored requirement, use the **exact 10 / 20 / 30 Vigor v0 defaults** above; do not require the GM to invent a number at the 0-HP trigger. A more specific listed or authored injury requirement takes precedence. The numerical defaults remain **playtest calibration values** and do not define new ongoing penalties for unspecified injury details.

A wound's repair requirement may exceed the character's current or even maximum Vigor. Repair is **incremental and cumulative**, not a lump-sum payment.

Each point of regeneration throughput allocated to wound repair consumes **1 Vigor** and adds **1 point of Repair Progress** to that wound. Repair Progress persists between turns, encounters, rests, and Vigor Recovery intervals unless an explicit effect removes it.

When accumulated Repair Progress reaches the wound's Repair Requirement, that wound is repaired. A character may therefore naturally repair a large wound over multiple Vigor-recovery cycles even when the wound's total requirement exceeds Max Vigor.

External healing, reconstruction, or medical rules may add Repair Progress, substitute another resource, accelerate recovery, or bypass part of this procedure when they explicitly say so. [Basic Heal v0](../07-veil-magic/basic-heal-v0.md#dying-recipient-convert-the-hp-component-to-repair-progress) is one such **narrowly authored exception**: while a target is Dying, its otherwise-small HP component directly adds **+2 Primary or +1 Secondary Repair Progress** toward the current active repairable wound without spending the patient's Vigor/throughput. Surplus HP points can restore actual HP **only after completing that wound and with no other blocking unfinished active wound**. This does **not** grant instant natural regeneration or repair Irreparable wounds.

**Irreparable** wounds do not accumulate ordinary natural Repair Progress toward reconstruction; they require an explicit effect capable of reconstructing the lost structure. **Fatal** wounds use no repair track because death has already occurred.

Current example values:

| Wound | Repair requirement / class |
|---|---:|
| Deep arm wound | 10 |
| Broken arm | 15 |
| Severed tendon | 15 |
| Broken leg | 20 |
| Major artery | 20 plus ongoing bleeding |
| Destroyed eye | ~25 |
| Shattered leg | 30 |
| Punctured lung | 30 |
| Severe abdominal organ injury | 30 |
| Crushed skull | 40+ or Fatal where the brain is destroyed |
| Fully severed limb | Irreparable |
| Decapitation | Fatal |

Specific wounds may impose ongoing effects until treated or repaired, such as bleeding, reduced movement, impaired Dodge, reduced regeneration throughput, or sensory penalties.

## Dying

At **0 HP or below**, a character is normally unconscious and **Dying**.

By default, a Dying character loses **1 HP per round**. That loss is resolved during the character's Regeneration Step unless it is cancelled by regeneration throughput as described below.

```
Death threshold = HP <= -Maximum HP
```

Once actually dead, ordinary Vigor regeneration cannot restart the body.

A Dying or unconscious character retains its Initiative position and normal turn timing even when unable to take ordinary actions.

## Regeneration while Dying

While Dying and still possessing Vigor, regeneration throughput is first available for survival and wound repair rather than ordinary HP recovery.

Resolve this procedure during the character's Regeneration Step. If no Vigor is available, the regeneration allocation cannot cancel the Dying loss or repair the wound unless another rule explicitly provides an alternative resource or conversion.

1. determine available regeneration throughput;
2. spend 1 point to cancel the default -1 HP Dying loss for that round, if possible and desired;
3. apply the default Dying loss if it was not cancelled;
4. use remaining throughput to spend Vigor and add cumulative Repair Progress to the active wound;
5. prevent, offset, or medically control additional bleeding or similar ongoing losses where the relevant rules permit;
6. once accumulated Repair Progress reaches the Wound Repair Requirement, the wound is repaired; remaining throughput in that regeneration step may then restore HP;
7. once HP rises above 0, the character can regain consciousness unless another effect prevents it.

Medicine can stabilize, stop bleeding, immobilize injuries, and otherwise suppress ongoing consequences without necessarily restoring HP or completing supernatural tissue reconstruction. **Successful [Basic Heal v0](../07-veil-magic/basic-heal-v0.md) on an unconscious, genuinely beneficially treated Dying target does not require an Intrusion contest merely because the target cannot give active consent**. It supplies independent Vigor and small direct Repair Progress but does not alter the ordering of subsequent natural Dying regeneration steps.

See [Initiative and Round/Turn Procedure](../05-combat/initiative-and-round-structure.md) for the exact turn timing.
