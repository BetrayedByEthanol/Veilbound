# B04/B05 — Medium Gifted L1–3 Native Encounter and Tactical Balance Verification v0

> **Bounded native multi-round comparison, not a certified Focus, encounter challenge rating, representative player population, or authorization to tune the Ward.** Builds on merged [#155 structural Ward](b04-b05-medium-gifted-l1-l3-character-build-verification-v0.md) and [#156 exact G0/G1/G4/G5 Ward damage integration](b04-b05-medium-gifted-native-ward-encounter-integration-v0.md). No new Conduit Form, attack source, rule, or B06 milestone is created.

## Explicit scene and policies

`run_matrix(seed=0)` generates **21 reproducible source-native encounter witnesses** (3 actual Medium Gifted levels × (4 Soldier + 3 prepared-Sentry policies)). The full real G0/G1/G2/G3/G4/G4.5/G5 ledger, source digests, policy inputs, actor states, accounting metrics and cryptographic report digests are retained for each witness. Source replay, not merely self-consistent recalculated hashes, is the acceptance gate.

- **Soldier** (4 complete rounds per case, position `gifted=(2,2)`, `foe=(3,2)`): same actual sword profile `B06-AT-03`, declared attack d20 **4** and damage d6 **1**. Compare **Fear** (active Grade II Holdfast each real Emotion Window), **Dormant** (Joy-anchored Conduit with the same paid VP), **Dodge** (Fear Conduit, but each real G0 Dodge makes the authored sword miss; no free Pulse), and **Retune** (Fear only in round 1; Joy thereafter, while commitment stays). The caster pays **24 General AP and 2 Committed VP** once at the start, never magically refreshing a persistent Grade or setting a fresh Conduit free at later rounds. Actual Step-2 self HP restoration spends available Vigor within throughput.
- **Prepared Sentry** (2 complete rounds per case, `gifted=(2,2)`, `ally=(3,2)`, `foe=(4,2)`): real `B06-AT-02` reserved sword, d20 **4**, physical d6 **1**, Vigor d6 **4**, and native G4/4.5 receipts. The R ally starts and remains the source-authored attack recipient; the Gifted caster is **not** automatically an enemy target. Compare **Trust** (Grade II Shared Reserve blocks up to 2 actual Direct Vigor per round while the ally is orthogonally adjacent), **Dormant** (Joy-anchored Conduit), and **Diagonal** (Trust remains active, but a **real G1 paid movement step** moves the caster to `(2,1)` before round-2 damage, making the ally diagonal and therefore ineligible). Each actor takes a real initiative turn and regeneration step. The foe does not switch attack recipients by fiat.

All source enemy attack rolls/damage faces, target choices, defense choices and non-offensive player behavior are **deliberately fixed author policy**. No PC attack is fabricated for the Medium Gifted, whose ordinary physical offense has not yet been accepted by the dedicated G5 native weapon adapter. The comparison answers whether an established Ward meaningfully changes real received packets, VP allocation, survival/recovery and ally adjacency, **not** whether Medium Gifted wins a fair fight, is globally stronger or weaker than Priest/Scholar, or offers representative difficulty.

## Acceptance and counters

1. Every source damage event must correspond to a genuine G5 hit and G4.5 attested action. A miss has no G4 packet or free Ward Pulse. The G5/AP source attacker and the defending ally maintain their own native costs/defenses; no manual HP adjustment or aggregate damage shortcut is used.
2. One Grade II Conduit costs exactly **24 General AP + 2 Committed VP**, never Spent VP. It cannot grant a Pulse while Dormant; Fear only blocks one eligible HP packet per Emotion Window, Trust only blocks one eligible adjacent allied Direct Vigor packet. An unused Ward Pulse cannot be manufactured by a missed attack. Four new Emotion Windows on four rounds are distinct and sourced from actual `turn_resources`.
3. Sequential source damage, Regen Step-2 HP restoration and Vigor expenditure are reported separately. The same authored Soldier/Sentry dice permit **policy comparisons**, not derived win probabilities. Native saved receipts and source fingerprints are reconciled with `canonical_digest` and re-execution; changed ledger/metrics reject even if a caller recomputes a digest.
4. No additional archetype × Focus pairing, Tier-1 catalogue entry, G9 category or MVP exit-gate success follows. Structural pairings remain **8/12**, independently fully certified Focuses **0/12**, original blocker closures **3/7**, and strict MVP exits **0/6**.

## Bounded exclusions and follow-up

This pack contains no authored Medium Gifted universal/offensive casting route, no general-G5 dagger adapter, no multi-actor attack-order permutations beyond the fixed source sequence, no multiple Grade/simultaneous finite-prevention priority comparison, and no representative long-running terminal encounter. It retains provisional Ward mitigation values without recommending numerical buffs or nerfs. A focused next review should assess the source legal **Medium Gifted offensive/noncombat repertoire** and independently test role tradeoffs against other archetypes before any overall Focus certification or tuning decision.

Run:

```bash
python -m unittest tests.test_b05_medium_gifted_tactical_balance_v0 -v
python -m scripts.b05_medium_gifted_tactical_balance_v0 --summary
python -m unittest discover -s tests -v
```
