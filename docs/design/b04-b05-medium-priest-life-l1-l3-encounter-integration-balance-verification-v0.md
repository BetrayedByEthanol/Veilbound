# B04/B05 — Medium Priest Life L1–3 Encounter Integration and Balance Verification v0

**Status:** executable **two-round fixed-policy comparison**, NOT an independent full encounter, sampled balance measurement, player/GM AI, or Medium Focus certification. Canonical techniques, Focus numbers, and enemy-source rules are unchanged.

## Authoritative inputs

- [Medium Priest Life L1–3 Character Build and Consecration Verification v0](b04-b05-medium-priest-life-l1-l3-build-consecration-verification-v0.md): one independently sourced medium character (the `M` G0 role), 24-AP Projection/General cost, 4/8/12 VP, Guided 2 Committed VP, Shelter 2 Committed +1 Spent VP with a finite initial budget of 8, L3 Intercession one Reaction and **provisional** 2 Spent VP.
- [Priest](../rules/08-archetypes/priest.md), [Guided Regeneration](../rules/07-veil-magic/guided-regeneration-v0.md), [Vital Shelter](../rules/07-veil-magic/vital-shelter-v0.md), and [Basic Heal](../rules/07-veil-magic/basic-heal-v0.md).
- Exact existing enemy fixtures `content/creatures/b06-ordinary-human-soldier.v0.json` and `content/creatures/b06-firebound-sentry.v0.json`. The Sentry starts in its **already paid** `prepared_start` state with a Chosen Conjure Flame Reserved Sword; this is NOT a free Round-1 enchantment.
- Actual G0 initiative/turn AP and Regeneration Steps; G1 contact; G3 maintained effects, VP and Basic Heal hand authority; G4 native HP/Vigor, Shelter and healing; G4.5 real committed attack binding; G5 native strike, defense and roll.

## Fixed scene and policy specification

One `M` Priest at grid (1,2), one `F` High Scholar ally at (2,2), one one-square source Soldier or Sentry at (3,2), no walls, 8×7 map. Initiative scores are **scenario-assigned explicit** (30, 24, 18) for Priest, foe, ally; these scores are not passive class bonuses. Two actual completed rounds, one opponent physical sword attack in each enemy turn, each attack declared separately through native G5 with one `take_hit` defense. Attack die = **12**, sword damage d6 = **1**, enchanted Sentry additional Vigor d6 = **4**. No critical, no invented Wound; fixed policy declines optional responses. Defenders do not attack the enemy. The foe is not magically forced to miss, and no HP/Vigor is set to scripted end-state values.

Every actor has a genuine Step 2 on their own turn. The ally allocates as much of its missing conscious HP as actually allowed by Current Vigor, source Regeneration throughput and a legal Guided bonus; no extra step is invented. The Priest chooses one action only when the named strategy calls for it. The two-round stop is **not** a victory, defeat, withdrawal, or a combat terminal certificate. At L1–2 the L3-equivalent foes are deliberately **not** described as level-matched challenge ratings.

| Strategy | Priest Round 1 | Priest Round 2 | Target and effect |
|---|---|---|---|
| `no_magic` | no magic | no magic | control, ordinary native ally Regeneration only |
| `guided` | pay maintained Guided for ally | no action | +1 on ally's two genuine Step 2 receipts |
| `shelter` | pay maintained Shelter for ally | no action | one unchanged B8 protects genuine direct Vigor packets, never HP |
| `basic_heal` | no magic | source-paid T1 Basic Heal for ally, actual d8=3 | 24 AP, 2 Spent VP, 2 HP and 5 Vigor (up to target's missing resources), functioning free hand |
| `guided_intercession` | maintain Guided on Priest themself | L3 only, maintain same instance | only as ally enters genuine Step 2; two paid Reaction+2 VP Intercessions |
| `shelter_intercession` | maintain Shelter on Priest themself | L3 only | Sentry only; spend Reaction+2 VP against each independently delivered Sentry G4 Vigor packet |

For the last two, Intercession **does not transfer a persistent effect** or open a second Consecration slot. G5 carries the Sentry's declared `medium_intercessor` through **one paid physical attack → G4.5 bound action → source JSON hit packets → G4 pre-damage Intercession**. The target's HP packet still resolves, and the original finite budget is not refreshed. A Soldier strike has no Vigor packet and must **reject** Shelter Intercession rather than fabricate damage.

**Costs are the currently authored provisional terms, not proposed tuning:** Guided (2 Committed), Shelter (2 Committed+1 Spent), Basic Heal T1 (2 Spent), L3 Intercession (2 Spent + one refreshed Reaction each round). TAL-M03 Frugal Technique has **not** been activated as an unverified automatic discount; no discount is silently credited in these witnesses.

## Data/evidence and interpretation

Execute the complete matrix:

`python -m scripts.b05_medium_life_encounter_balance_v0`

Execute and inspect one full, native event-ledger witness:

`python -m scripts.b05_medium_life_encounter_balance_v0 --opponent sentry_prepared --level 3 --policy shelter_intercession --seed 0`

Run the focused regressions:

`python -m unittest tests.test_b05_medium_life_encounter_balance_v0 -v`

`python -m unittest discover -s tests -v`

The reported 27 selected pairs (L1/L2: 4 policies × 2 foes; L3: 5 vs Soldier, 6 vs Sentry) contain: source digests, exact G5 paid hits, G4.5 bound-hit events, G4 damage/regeneration/heal receipts, G3 establishment and VP transition, total priest AP paid, HP and Vigor remaining, finite budget prevention, paid Reaction counts, and a canonical ledger digest. `attest_policy()` reconstructs one witness from authentic fixtures and **replays** native execution; it rejects a forged metrics dict or even a tampered-and-rehashed ledger.

The controlled comparisons answer **what these specific legal payments achieve under this fixed damage and timing policy**, not what players would usually choose. For the **Sentry**, Guided improves HP throughput at the ally's normal Step 2 but consumes the recipient's Vigor 1:1; Shelter instead conserves Vigor from the separate enchantment packet and leaves HP loss unaffected. Basic Heal spends two VP and a separate Round-2 action to restore HP/Vigor; its ability to cover both resources should be compared against the persistent reservations' ongoing opportunity cost. At L3, a Consecration redirected transiently through Intercession achieves the same recipient-specific packet/Step effect as a directly hosted one in this bounded two-round scene **but additionally spends 4 VP and two distinct round Reactions**. This is direct evidence of a real opportunity-cost premium under the provisional **2 VP per Intercession**; **it does not establish the fair/balanced price**.

Further cases needed before accepting Medium Priest balance: representative independent GM/player policies and lawful opponent retaliation choices (including full possible two-hit Sentry sequences, Guard/Dodge, movement and cover), real High/Medium/Low Priest parties, Hunter venom and Pounce, fatigue/recovery across scenes, varied VP reserves and depleted Shelter budgets, genuine Basic Heal contested Intrusion and blocked delivery, L3 Frugal Technique use, larger samples and uncertainty bounds. The selected F ally is a genuine B05 High Scholar source sheet but does **not** perform a complete independent High Scholar spell rotation in this comparison. No independent Focus certificate is produced.

**Acceptance matrix**

| Gate | Conclusion |
|---|---|
| Medium Priest structural L1–3 source | Implemented in earlier PR #128 |
| Source-native opponent pressure + Consecration + Basic Heal | In scope, tested by this v0 |
| Source-native L3 Intercession during opponent paid strike / actual Step 2 | In scope, tested by this v0 |
| Resource receipts / forced legal policy comparison | Bounded, reproducible; no inferred probabilities |
| Pricing decision: Intercession 2 VP fair? | **Provisional; not accepted** |
| Fully opposed, representative encounter and independent Focus certification | **Not claimed; open** |
| Historical Phase 3 audit / original Soldier/Sentry/Hunter packages | Must remain unchanged |

This record makes no claim to a sampled win rate, confidence interval, CR, or completed independent Medium Priest Focus certification.
