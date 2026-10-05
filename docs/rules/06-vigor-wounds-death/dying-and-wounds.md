# Dying and Wounds

> Canonical current framework extracted from Core Rules Audit v34. Some wound severity thresholds and individual injury effects remain calibration items.

## When wounds occur

Ordinary hits do not normally create persistent wounds.

A wound occurs only when:

1. a **Called Shot** successfully qualifies for a wound;
2. a **Devastating Critical** occurs; or
3. the target reaches **0 HP**.

A Called Shot consumes the character's entire Attack action regardless of normal attack count and carries substantial location difficulty. The exact called-shot procedure is not yet fully specified in the audit.

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

Severity is determined by the event that caused the wound rather than by a second random roll.

- **Called Shot:** normally Serious if it qualifies; exceptional results may upgrade it.
- **0 HP:** Serious or Critical depending on how far the attack carries the target below zero. The exact overkill threshold remains unresolved.
- **Devastating Critical:** at least Critical and may be Fatal when the weapon, location and circumstances physically permit it.

## Repair requirement

Wound repair cost represents bodily trauma and does not scale with level.

| Severity | Baseline repair requirement |
|---|---:|
| Serious | ~10 Vigor |
| Severe | ~20 Vigor |
| Critical | ~30 Vigor |
| Catastrophic | 40+ Vigor |
| Irreparable / immediately fatal | Cannot be naturally regenerated |

Current example values:

| Wound | Repair requirement |
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
| Crushed skull | 40+ |
| Decapitation / destroyed vital structure beyond repair | — |

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
4. use remaining throughput toward the active Wound Repair Requirement;
5. prevent, offset, or medically control additional bleeding or similar ongoing losses where the relevant rules permit;
6. once the wound is repaired, remaining throughput in that regeneration step may restore HP;
7. once HP rises above 0, the character can regain consciousness unless another effect prevents it.

Medicine can stabilize, stop bleeding, immobilize injuries, and otherwise suppress ongoing consequences without necessarily restoring HP or completing supernatural tissue reconstruction.

See [Initiative and Round/Turn Procedure](../05-combat/initiative-and-round-structure.md) for the exact turn timing.
