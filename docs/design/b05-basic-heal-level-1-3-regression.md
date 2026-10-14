# B05 — Basic Heal v0, level 1–3 regression checkpoint

> **Design/playtest verification, not independent rules authority.** Canon: [Basic Heal v0](../rules/07-veil-magic/basic-heal-v0.md), [Intrusion resistance](../rules/07-veil-magic/resonance-and-intrusion.md#intrusion-barrier), [HP/Vigor](../rules/06-vigor-wounds-death/hp-and-vigor.md), [Dying](../rules/06-vigor-wounds-death/dying-and-wounds.md). Current formulas and cost values are **v0 provisional**. These deterministic cases were computed by enumerating every integer die result; they are **not combat-simulation outcomes** or success probabilities including enemy tactics.

## Restoration packet verification (before target caps)

Primary: `HP 2; Vigor 4 + ceil(d8×T/3) + max(0,VC)`. Secondary: `HP 1; Vigor 2 + ceil(d6×T/6) + max(0,VC)`. Rider: `HP 0; Vigor 2 + ceil(d4×T/6) + max(0,VC)`, usable only with distinct explicit authorization.

| Tier | Contribution | Mean Vigor at VC +0 | Mean at +2 | Mean at +4 | Range at VC +0 |
|---:|---|---:|---:|---:|---|
| 1 | Primary | **5.875** | **7.875** | **9.875** | 5–7 |
| 1 | Secondary | 3.000 | 5.000 | 7.000 | 3 |
| 1 | Rider | 3.000 | 5.000 | 7.000 | 3 |
| 2 | Primary | **7.375** | **9.375** | **11.375** | 5–10 |
| 2 | Secondary | 3.500 | 5.500 | 7.500 | 3–4 |
| 2 | Rider | 3.250 | 5.250 | 7.250 | 3–4 |

**Not all announced healing will fit**: max HP = `10+Vitality`, max Vigor = `(10+Vitality)×Level`; missing resources cap restoration. With recipient Vitality +1, max Vigor at levels 1/2/3 is **11/22/33**. T1 Primary VC +2 restores on average **7.875** Vigor to a sufficiently depleted target: **71.6% / 35.8% / 23.9%** of those maximum pools. This is a percentage of the **Vigor pool**, not a fraction of HP or instant extra regeneration.

## Turn AP and VP affordability (Veil Affinity +0)

| Level | Focus | Turn AP | Projection AP | Max Projection casts/turn | Max VP | Tier-1 casts/pool | Tier-2 casts/pool |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | High | 30 | 20 | 1 | 6 | 3 | — |
| 1 | Medium | 30 | 24 | 1 | 4 | 2 | — |
| 1 | Low | 30 | 30 | 1 | 2 | 1 | — |
| 2 | High | 36 | 20 | 1 | 12 | 6 | — |
| 2 | Medium | 36 | 24 | 1 | 8 | 4 | — |
| 2 | Low | 36 | 30 | 1 | 4 | 2 | — |
| 3 | High | 42 | 20 | 2 | 18 | 9 | 4 |
| 3 | Medium | 42 | 24 | 1 | 12 | 6 | 3 |
| 3 | Low | 42 | 30 | 1 | 6 | 3 | 1 |

`Tier-1 casts/pool` and `Tier-2 casts/pool` are calculated from a **full pool with no other expenditure/recovery**, not all in a single turn. A Tier-2 cast costs 4 VP, while Tier 1 costs 2 VP. Level 3 High Focus with 40 AP can choose **two** Tier-1 casts (average **15.750 Vigor and 4 HP** before caps for 4 VP) instead of **one** Tier-2 cast (average **9.375 Vigor and 2 HP** before caps for 4 VP). **Flag as a scaling watch, not a proposal to rewrite user-approved formulas in this PR.**

## Dying and reserve test

Set target level 1, Vitality +1, **Low Focus** (natural throughput `1+3=4`), **HP −3**, **Vigor 0**, **Serious wound at Repair Progress 0/10**. A successful T1 Basic Heal from caster VC +2 provides **7–9 Vigor**, direct **2/10 Repair Progress**, and **no HP**. For a fixed die outcome giving exactly **8 Vigor**:

| Event | HP | Vigor | Repair Progress | Outcome |
|---|---:|---:|---:|---|
| Immediately after Heal | −3 | 8 | 2/10 | No bonus regeneration step |
| Next normal Regeneration Step | −3 | 4 | 5/10 | Spend 1 Vigor cancelling Dying loss, 3 repairing |
| Second normal Regeneration Step | −3 | 0 | 8/10 | Same survival-first order |
| Third normal Regeneration Step | −4 | 0 | 8/10 | Without Vigor, Dying loses 1 HP |
| Fourth normal Regeneration Step | −5 | 0 | 8/10 | Continues Dying |

A second spell or other support may still be necessary. A spell on **9/10 wound progress at HP 0** contributes +1 Repair Progress, then spends remaining +1 HP to bring HP to **+1** if no other block exists. With HP −3, the same event brings HP only to −2; the target stays Dying.

**No repair bypass:** an Irreparable active wound gets no ordinary direct Repair Progress and blocks use of Basic Heal HP to bypass the wound. Vigor restoration remains eligible unless an effect blocks external Vigor restoration.

## Intrusion matrix and resisted cast check

| Actual situation | Contest and expected outcome |
|---|---|
| Conscious beneficiary, does not resist | **No Direct Veil contest**; valid restorative effect succeeds |
| Unconscious beneficiary / Dying ally | **No Direct Veil contest**; prior express consent not required for genuinely beneficial healing |
| Conscious target expressly refuses genuine healing | **+8** barrier and shared Direct Veil contest |
| Harmful Intrusion against unconscious target | **+8** barrier; unconsciousness never waives intrinsic harmful protection |
| Harmful Intrusion falsely passed off as benign, accepted in actual deception | **+4** barrier, not complete waiver |
| Target knowingly accepts actual effect including its risks | Contest waived for that specific understood effect |
| Caster calls hidden harmful control “healing” | Harmful/deception rules, **not** unopposed-benefit shortcut |
| Existing ward blocks external restoration | Honor ward independent of contest; no unauthorized bypass |

At equal non-barrier modifiers, equal integration, Resonance 0, the **+8** contested effect succeeds on two d20 faces (**10%**); the **+4** deceived effect succeeds on six (**30%**). For an example healer **VC +2, Intellect +2** against a level-1/2/3 target **Vitality +1, Awareness +1, Resonance 0**, pressure `d20+4`, contested defense `10+1+1+8=20`: the caster needs **17–20 = 20%**, and **spends the 2 VP even when resisted**. For beneficial/unopposed healing the success chance is **100% conditioned on a legal cast and no distinct protection**; this is not an automatic resurrection or immunity bypass.

## Acceptance checks and scope

- [x] Same `Single Target` identifier for Primary/Secondary, no invented area or weapon profile.
- [x] Dying HP component becomes +2/+1 direct repair; Rider contributes **0** repair without an independently authorized effect.
- [x] Only **once** do ordinary HP/Vigor caps and the target's chosen legal defenses apply.
- [x] No additional Regeneration Step, advance VP recovery, cross-Archetype automatic knowledge, double-halving Secondary, or per-hit/per-action full Rider healing.
- [x] New Intrusion protection does **not** allow harmful magic against an unaware/unconscious victim without +8, except expressly knowing waiver or the narrowly defined genuine deception case.
- [x] Resisted cast uses **raw Veil Control in Pressure**, **nonnegative VC** only for numeric restoration scaling.
- [x] Tier-2 VP efficiency and unusually strong level-1 Vigor replenishment remain **provisional balance watch**, not blocking ambiguity in the authored procedures.

**Next B05 work:** review PR, sample encounters, establish actual Archetype repertoires/access, then a non-damage Mind / Psionics Imposition technique.
