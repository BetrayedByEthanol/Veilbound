# B04/B05 — Anointed Natural Regeneration and G5 Attrition v0

> **Bounded source-backed recovery-policy comparison, not certified combat readiness.** Extend merged **#172** genuine Soldier/Sentry G5 injury with real, player-selected **ordinary G4 HP allocation** at each of two existing recipient Regeneration Steps. Compare the same attack exposure against no Signature, a normal Returning Step, and finite Lesser Authority. No extra Step or new offensive G5 profile is invented.

## Scope and authored choices

[Native policy runner](../../scripts/b05_anointed_native_natural_recovery_v0.py) uses the exact same sourced encounter, positions, deterministic d20/d6 attack faces, living recipients, G0 AP/VP and real G5/G4 hit resolution as merged [three-Focus defensive witness](b04-b05-anointed-three-focus-native-g5-defensive-witness-v0.md). The comparison is **54 fixed policies = 3 Anointed Focuses × L1/L2/L3 × Soldier/prepared Sentry × 3 recovery selections**.

The recipient makes two **explicit ordinary `RegenerationChoice(hp=1)`** decisions, once after the genuine Round-1 enemy hit and again at the genuine Round-2 Regeneration Step. These separately restore 2 HP for **2 recipient Vigor**, with **0 wound Repair Progress** and no other spontaneous healing. This is a selected comparison policy, **not** an automatic optimization, a full-throughput choice, or a rule that natural regeneration must always allocate HP. G4 retains all source constraints: living vs Dying, available Vigor, missing HP, current throughput and wound legality.

The three authored policy names are:

| Policy | Ordinary HP / recipient Vigor | Additional Returning Step |
|---|---|---|
| `natural_only` | 2 / 2 across two real Steps | None; full finite Destiny unchanged |
| `natural_plus_signature` | 2 / 2 | One independently legal High 20-AP Projection (+2 HP, 2 recipient Vigor), Medium previously paid 24-AP Investment (+1 HP, 1 recipient Vigor at patient Step), or Low Embodied (+1 self HP, 1 self Vigor at own Step) |
| `natural_plus_lesser` | 2 / 2 | Same HP cap, **0 extra recipient Vigor**, and **1 spent finite Destiny**, at the same legal native High/Medium/Low source window |

All legal beneficial target delivery in this bounded scene is **explicitly unopposed** (`unopposed=True` on High/Medium native restoration), and Medium's Invested recipient consent is explicit. Low is self-only. It does **not** certify changing consent, refused Restoration, or any **contested +8 Intrusion Barrier** adjudication. A GM must separately adjudicate those cases.

The **High** Anointed acts before the Round-1 enemy, so after the real Round-1 patient Step with 1 ordinary HP restored, High pays a Round-2 20-AP Projection before the patient's second natural Step. The **Medium** Anointed pays 24 AP to invest the patient at its genuine first turn, then the recipient's Round-1 Step preflights the 1 ordinary HP allocation **against the projected after-Signature HP and Vigor**. The **Low** Anointed receives the actual Round-1 G5 hit, and its own Step likewise resolves Signature first and normal 1 HP/1 Vigor second. Neither Medium nor Low receives an extra Regeneration Step from the Signature.

## Acceptance evidence and conservation checks

The [nine focused regression methods](../../tests/test_b05_anointed_native_natural_recovery_v0.py) evaluate all **54 native encounters**, compare each one to the exact zero-natural-recovery baseline from #172, and check that:
- The natural-only result has **+2 HP / −2 recipient Vigor** relative to the original same-exposure baseline, with unchanged two-Destiny reserve.
- A normal Signature then adds exactly **+2 High / +1 Medium or Low HP** and spends the corresponding **2 / 1 recipient Vigor** independently of the two ordinary HP regeneration debits.
- A Lesser Signature adds the same HP, spends **0 additional Vigor** but **1 finite Destiny**. It never waives the two separately allocated ordinary G4 regeneration costs.
- Each native receipt proves precisely one enemy G0-paid G5 hit and G4 damage, **two genuine dated patient G4 Steps**, source actor/creature digests, one legal Focus-specific Signature at its actual action/Step boundary, and one explicit policy selection.
- Every reported ledger is source-replayable and full-result attested. Modifying ordinary regeneration debit or policy allocation and recomputing the report SHA256 cannot manufacture valid evidence.

This is **not** prolonged multi-opponent attrition, encounter AI, defensive Guard/Dodge tactics, Wound/Dying recovery, an Anointed G5 offensive sword attack, L3 paid Guided Regeneration Authority in combat, measured role effectiveness or representative GM play. High/Medium/Low L3 Guided remains separately implemented in #171, but is **not triggered** here; combining a same-Step Guided Authority with Returning Step still requires an explicit authored order. No synthetic noncombat Regeneration Step cadence or free Destiny recharge is asserted.

## Readiness remains open

The roster remains **12/12 structural Focus builds**, **0/12 independently certified complete Focuses**, and **0/6 strict MVP exits**. B04–B07 are open, and existing B06 **G0–G8** milestone boundaries remain fixed. **This witness is not certified** for full Archetype × Focus combat readiness or B07 representative player choices. Next gaps include native ordinary Anointed melee/offense from approved source profiles, actual G5 enemy tactics and protections, pressured L3 Guided, GM-authored noncombat identity, contested beneficial Intrusion and independent progression/attrition certificates.
