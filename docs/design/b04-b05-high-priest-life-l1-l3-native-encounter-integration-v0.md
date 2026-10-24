# B04/B05 — High Priest Life L1–3 Native Encounter Integration v0

**Scope:** source-backed, two-round native G0/G1/G3/G4/G4.5/G5 integration of the existing [High Priest Life L1–3 build, Open Invocation and Open Prayer](b04-b05-high-priest-life-l1-l3-build-open-invocation-verification-v0.md). **No independent Focus certificate, enemy AI, CR claim, win-rate or three-Focus balance sign-off.**

## Bound characters, scene and source policy

H is exactly the existing High Life Priest build: original nine-Ability, TAL-C02, leather and sword, free healing hand, Max VP **6/12/18**, Turn AP **30/36/42**, Projection AP **20**, and native unbuffed regeneration throughput **4**. It has no independently sourced G5 weapon attack profile; this matrix measures High Life **support**, never fabricates player martial damage or extra actions.

H at (1,2) supports the same original **F High Scholar Fire**, HP12, at (2,2) used by Medium comparative encounters. A genuine source Soldier (B06-EN-02) or **prepared** Firebound Sentry (B06-EN-01) attacks from (3,2) in actual G1 contact. Initiative H 30, foe 24, ally 18. Across two complete rounds, foe declares and pays one native G5 sword attack per round, the defender explicitly selects Take Hit, G4.5 certifies each paid action, G4 applies source HP/Direct-Vigor packets, and G0 resolves exactly one Step 2 per actor per round.

**Fixed declared dice:** melee d20 12; source sword d6 1; prepared Sentry enchanted Vigor d6 4; High Basic Heal d8 3; a wound-location d20 value of 8 is precommitted only where required. Optional responses are declined; no inventing GM choices afterward. F voluntarily allocates at most 1 real throughput/Vigor to HP in its first genuine Step 2, retaining a deficit for R2 healing; R2 spends up to its genuine current throughput and Vigor. This is a **fixed player policy** shared across all comparison cells, not optimal play. Original High, foe and F source state/hits remain identical between policies.

## Exactly authored preparation and access policies

All chosen preparation lists are selected **before Round Begin**, not freely reshuffled mid-encounter.

| Policy | Initial preparation | High's legal Primary | Native payment |
|---|---|---|---|
| baseline | standard | No spell | 0 |
| prepared_guided | standard | R1 Guided Regeneration maintained on F | 20 AP, 2 Committed VP |
| prepared_shelter | standard | R1 Vital Shelter maintained on F with B8 | 20 AP, 2 Committed +1 Spent VP |
| prepared_heal | standard | R2 Basic Heal on F, functioning free hand | 20 AP, 2 Spent VP |
| invoked_heal | invocation (Heal unprepared) | R2 Open Invocation Basic Heal | Entire Full Action AP, 3 Spent VP |
| invoked_shelter | ward_invocation (Shelter unprepared) | R1 Open Invocation maintained Vital Shelter | Entire Full Action AP, 2 Committed +2 Spent VP |
| open_heal (L3 only) | invocation, unspecified slot | R2 Open Prayer fills with Basic Heal | 20 AP, 2 Spent VP; no surcharge |
| open_shelter (L3 only) | ward_invocation, unspecified slot | R1 Open Prayer fills with Vital Shelter | 20 AP, 2 Committed +1 Spent VP |
| dual_prepared (L3 only) | standard | R1 Guided + Shelter, both maintained on F | Two real Projection Actions, 40 of 42 AP; 4 Committed +1 Spent VP |

For each opponent L1–2 have 6 policies and L3 has 9; across both opponents this is **42 deterministic native cells**, not statistical trials. TAL-M03 Frugal Technique is **not auto-applied**, and the High Priest never gains a phantom full martial attack.

Guided gives +1 throughput on F's **existing real Step 2**, with 1 Vigor per recovered HP. Shelter consumes actual remaining B8 against *real* Sentry Direct Vigor packets, not Soldier HP and not a fabricated substitute packet. Basic Heal is the actual delivered G4 Primary; its HP/Vigor restoration is separate from natural Step 2, with AP/VP paid from the High Priest. Invocation pays its +1 Spent surcharge separately from normal spell cost; Open Prayer fills one previously unspecified slot without such a surcharge. No L3 second Projection Action is counted at L1–2.

## Evidence and certification boundaries

The runner records source IDs and digests, policy and preparation, each native G5 hit, G4 packet, ordinary Regeneration Step, HP/Vigor/VP/AP ledger receipt, effect/budget and Open Prayer fill, plus the canonical full-ledger SHA-256. Its source replay attestation regenerates the entire result instead of trusting a caller's mutated/rehashed report. Illegal level/policy combinations and unsupported source techniques fail closed. The 15 dedicated tests cover 42 cells, AP and VP accounting, full Invocation, Open Prayer, L3 double Projection, source-native combat chronology and anti-tampering.

**Still excluded:** High Priest generic G5 offensive profile; contested Intrusion; GM-opponent AI; protective stance or healing to dead actors; prolonged attrition, Hunter pounce/toxin, sampled win rate, balance-tuning decisions, encounter victory or independent three-Focus certification.

## Verification

- python -m unittest tests.test_b05_high_life_native_encounter_v0 -v
- python -m unittest discover -s tests -v
- python -m scripts.b05_high_life_native_encounter_v0 --seed 0

**Next gate:** matched three-Focus Priest Life comparative native encounter balance, not authorized from these fixed traces alone.
