# B06 G6-D — Encounter Completion and Missing Combat Integration v0

> **G6-D first executable slice:** native G2 Bow contact → G4 physical
> HP/critical/wounds, and a source-attested four-PC Hunter-death terminal.
> This is **not** full protective Reaction coverage, all projected
> projectile types, or a completed difficulty/CR certification. Do not
> treat these outstanding interfaces as if they were already executable.

## Verified native Bow damage

[Implementation](../../scripts/b06_hunter_completion_g6d_v0.py) wraps
exactly **one source-authorized R Bow shot** against the 1×2 Hunter on a
verified no-Cover/no-screen G2 firing lane. The actual G2
`bow_sequence()` owns one 20-AP Physical Action, one genuinely launched
arrow, one already-assigned personal ranged Take Hit, and the source
B05 fixed +4 accuracy. Its immutable G0/G2 ledger indices, one actual
launch, anatomical Hunter target cell, and the real G2 shot outcome
are independently matched before G4 damage. No second Attack roll or
another unearned action is created.

A ranged Take Hit is a **static Ranged Defense** (10 plus range
difficulty), not melee auto-hit. Natural 1 misses; an ordinary roll
hits only above that defense. A natural 20 has **one confirmation**
and the existing Strong/Critical/Devastating damage-d4 classification.
The sourced Bow's `2+d4 Piercing, Pen3` enters the existing G4
`DamagePacket` mitigation/wound engine exactly once, plus one or
two canonical extra critical d4 dice. The source's no-Strength
physical contribution is not re-applied. Damage and any required
Devastating/0-HP-crossing wound-location d20 are preflighted before
paying AP or ammunition; a missing die rejects atomically.

Each successful delivery is separately logged as
`g6d_bow_adjudicated` and `g4_damage_applied`, with stable real
G2 AP/launch/shot indices and source digest. This **does not** claim
an ordinary G5 melee attestation or invent a G4.5 G5 profile for the
Bow. Neither a miss nor a cover/Guard impact becomes a phantom HP
packet.

Explicitly outside this Bow subset: firing with a threatened Bow
Opportunity, committed multi-arrow sequences, active projectile
Dodge/Shield Guard, moved-after-declaration targets, Cover/Living
Screens/collateral, simultaneous Protective Intervene, non-Hunter
targets, area-bearing arrows, and exact atypical Prone/Reach cases.
All require further native adapters, not a permissive fallback.

## Mixed-party Hunter death attestation

G6-C already executes two true rounds of A/B/R/F against the Hunter.
The four-PC window ends with the Hunter **Dying**, not dead, after
actual Flame damage/wound. [`run_i3_defeat()`](../../scripts/b06_hunter_completion_g6d_v0.py)
continues the **same** native encounter through Round 3: the Hunter
passes a real Dying Regeneration Step, PCs complete real turns, R fires
one authenticated natural-20 devastating Bow shot, and G4 crosses
**the actual lethal threshold**. The remaining Scholar turn and
Round End then complete; no synthetic turn or terminal shortcut.

`attest_hunter_defeat()` requires the exact three/four-member
source-backed A/B/R[/F] roster, one genuinely dead Hunter with HP
at -Max HP, one native lethal G4 damage event linked to a real
G5 melee outcome or G6-D Bow adjudication, **no pending paid
attack slots**, and an actually finished G0 round. A Dying Hunter
or externally assigned death without a combat-provenanced lethal
packet does not qualify. The attested terminal is **Hunter defeat**,
not automatically all-party survival, successful withdrawal or
safety, nor a universal victory condition.

## Remaining G6-D work / certification limits

## Native Reactive Intervene — source-bounded Hunter Bite

[Reactive protector](../../scripts/b06_hunter_reactive_intervene_g6d_v0.py)
now implements **one** paid Hunter `B06-AT-04` Bite against the
L2/L3 A Restorative Vanguard with a neighboring B Preservation Guardian.
The ordinary G5 declaration pays its one Physical Action and locks the
ward's original Guard/Dodge/Take Hit before any d20. The separate
source-bound protected-resolution path checks that **same** G0
payment, one-slot G5 attestation, defense record, Hunter's real
head-forward contact and guardian's current adjacent physical
position. It opens the original `g5:melee:<paid-index>` native G0
spontaneous response window; the Guardian commits exactly one normal
`Reaction`, with no invented movement or extra AP. A previous
Opportunity-activated Reaction cannot be recycled.

**Shield Guard** requires the Guardian's ready actual shield and a
remaining normal Guard use. One Guard use is spent **only when** the
original Bite would hit; a miss still spends Reaction but consumes
zero Guard. For a non-natural-20 hit, the original attack total is
compared against the Guardian's actual Shield Guard value (without
stacking ward defense). A stop makes no damage or venom packet; a
failed shield lets the original ward take the genuine G4 profile hit.

**Body Take Hit** transfers only an otherwise-successful, originally
declared Bite to the Guardian, without a new accuracy roll or a
second defensive choice. Armor, genuine G4 wound/HP, and venom are
resolved on the Guardian; the ward's already-paid defense is
retained. A natural 20 performs **one** critical confirmation:
against Shield Defense for Shield Guard, or against the ward's
original defense for Body Take Hit. One custom
`g6d_protective_bite_attested` record binds the original paid action,
G0 Reaction debit, optional conditional Guard use and actual damage
recipient. The body transfer is **not mislabeled a G4.5 original-target
hit**; the G5 paid slot is closed exactly once by its normal resolved
event. All wound/venom dice are preflighted before the Reaction costs.

This v0 **only** covers a single ordinary Hunter Bite in the verified
A/B/head-forward contact scene with a direct, physically reachable
melee path. It does not generalize a magical/area/arrow protector,
multi-attack chain, alternate NPC/body geometry, or a prepared route.

**Prepared Protective Intervene remains outstanding**. Moving the
protector using reserved MP before the original attack's final line
check needs a distinct G1 Movement Interception executor, live
post-movement eligibility, and conditional Guard/Body effects.
The Reactive pathway must not be used to grant free movement, to
recycle a spent Reaction or to treat an earlier historical response
as current protection.

A bounded four-PC Hunter death terminal is a genuine outcome
witness, but **complete mixed-party encounter certification remains
false**: full Bow lanes, Prepared Intervene and broader reactive geometry, true party tactical
choice/withdrawal paths, alternative adverse conditions and
calibration still need testing. **No Hunter CR has been assigned.**
The original signed Phase 3 4096-trial audit remains untouched.

## Verification

```sh
python -m unittest discover -s tests -p 'test_b06_hunter_completion_g6d_v0.py' -v
python -m unittest discover -s tests -v
```

The repository CI additionally checks the historical Phase 3 audit
hash and frozen scenario reports.
