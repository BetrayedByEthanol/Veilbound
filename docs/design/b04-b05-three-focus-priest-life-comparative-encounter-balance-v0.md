# B04/B05 — Three-Focus Priest Life Comparative Encounter Balance v0

**Status:** candidate evidence audit / matched bounded native encounters, **not** a final balance sign-off. This milestone compares actual G0/G1/G3/G4/G4.5/G5 source-bound outcomes under an explicitly uniform adversary policy, normalizes *only* against each build's authentic no-magic baseline, and maintains the distinction between self-Rite protection and support of an unrelated ally.

## Scope and two comparison strata

**Primary matched self-defense stratum:** H (High Priest), M (Medium Priest), A (Low Priest Chosen Guided Regeneration), and B (Low Priest Chosen Vital Shelter) each occupy precisely (2,2); exactly one genuine Soldier B06-EN-02 or prepared Sentry B06-EN-01 occupies (3,2), with source-paid G5 normal swords, native G4 HP/Direct Vigor and two rounds. G0 initiative priority Priest 30 / foe 20, explicit Take Hit with optional spontaneous responses declined, attack d20 **12**, sword d6 **1**, Sentry bonus Vigor d6 **4**, precommitted wound location d20 **8**. Both rounds the native Step 2 allocates available throughput and Vigor to missing HP, never creating an extra regeneration action. A/B original physical equipment, Armor, maximum HP, Vigor and VP remain authentic and **are not silently standardized**.

H and M choose baseline, Guided or Shelter self-beneficial maintained Primary; A can choose baseline, Chosen Guided and (only at L3) Chosen Guided plus actual Held Renewal opportunity; B chooses baseline, Chosen Shelter and (only at L3) Chosen Shelter plus Vital Interposition. The actual original action and funding gates apply: High prepared **20 AP**, **2 Committed** (plus 1 Spent for Shelter); Medium prepared **24 AP**, same committed/spent; Low Chosen **30 AP**, **1 Committed** (plus 1 Spent for Shelter). Actual optional Low L3 Exaltation requires another **1 Spent VP** and the original host and timing; A Held may arm only after unused true Step-2 throughput, while B Vital arms in its own turn. No unsupported Low Priest external-target magic or extra full turn is inserted.

Self-defense comparisons consist of **64 native cells** (H 18, M 18, A 14, B 14) across all L1–3 and Soldier/prepared-Sentry conditions. Of these, the L3-only Exaltation cells are an **extra Low capability branch**, not a same-priced tier shared by H/M.

**Secondary historical ally-support stratum:** the *already merged* High Priest and Medium Priest runners independently attacked the same genuine F Scholar Fire ally, and their actual replay reports remain available for trend/context: **36 source-native cells**, 6 levels × opponent combinations with baseline, Guided and Shelter choices for H and M. These have shared source F and enemy identities but **their earlier authored F Step-2 policies differ**, so they are context and not another mathematically matched experiment. **Low A/B do not have source-authored proxy permissions to cast the same techniques on F**, so no equal-target Low ally sample or inferred three-Focus healing comparison is claimed.

## Auditable metrics

Every self scene records: original source digests; starting HP/Vigor and source Armor; VP max, available/committed/spent; final HP/Vigor, wounds, Dying and death; exactly 2 source G5 resolved hits, 2 G4 damage applications and 2 genuine Priest Step 2 receipts; post-mitigation HP damage; native direct Vigor prevention/applied; genuine natural HP restored and paid Vigor; Low Vital HP prevented and Held HP paid; AP paid for real actions; effects established; pending Exaltation; canonical full-ledger SHA-256. Every source witness is re-executed to verify it rather than trusting even a caller-rehashed JSON report.

A distinct **same-source baseline delta** accompanies each scene, using **the same role + level + opponent** with the same dice and choices but no magic. Delta covers final HP, final Vigor, wounds, Direct Vigor prevented, Low Vital HP prevented, Spent VP, Committed VP and AP. This is evidence of *that exact option under that fixed source scenario*, not a model-normalized statistic or a generic ratio of magic power per VP. Across A/B/H/M, differences in build Armor, natural throughput, initial Vigor and HP remain visible. No relative win rate or cross-Focus winner is manufactured.

## Interpretation boundary / candidate balance questions

1. **Action access and opportunity cost:** High uses 20 AP for a prepared Prayer, Medium 24, Low 30 for its Chosen Rite; that measured AP saving cannot alone establish superiority since VP pools, optional free hand, maintained caps and support targeting differ.
2. **Actual restoration:** Guided provides +1 throughput at an *existing* real regeneration Step; it is limited by eligible HP deficit and Vigor. A low value of extra healed HP in a two-round scene may mean no unused damage, not an underpowered spell. Held Renewal additionally requires authentic available throughput and subsequent HP loss.
3. **Prevention:** B8 Shelter prevents genuine Direct Vigor from prepared Sentry, not the Soldier's HP-only sword profile. Low L3 Vital Interposition can additionally divert real HP before wound crossing; two units of Shelter budget per HP prevented must be counted as opportunity cost. Zero prevention in Soldier scenes is a known scenario coverage limitation.
4. **Relative finite resources:** All costs retain Spent vs Committed distinction. Current-encounter remaining VP is not a measured six-hour consumption rate; ending/releasing the host or another combat changes it. High Open Invocation, L3 Open Prayer and High double-Projection were *already verified* in PR #133, but are not same-cost counterparts to Low Chosen/Exaltation and hence do not get invented equal matching slots here.
5. **Survival:** Wounds, Dying and death are recorded from native G4, not translated into a victory policy. Two fixed hits with predetermined damage and no foe AI cannot support a probability, threat-rating recommendation or final per-Focus numerical rebalancing.

**No numbers are changed by this milestone.** Candidate questions for a later targeted tuning study are whether (a) High 20 AP flexibility yields meaningful extra value under >2-turn action opportunity, (b) Medium Intercession's Reaction/Vigor opportunity cost can offset its supported ally breadth, and (c) Low Chosen's lower VP pool but lower Committed price and L3 self Exaltation yields a meaningful self-survival niche. Answer those with source-backed broader policy conditions before changing AP, VP, thresholds, dice or damage.

## Reproduction

```bash
python -m unittest tests.test_b05_three_focus_life_comparison_v0 -v
python -m unittest discover -s tests -v
python -m scripts.b05_three_focus_life_comparison_v0 --seed 0
python -m scripts.b05_three_focus_life_comparison_v0 --role B --level 3 --opponent sentry_prepared --policy exaltation
```

**Next research step:** multi-round attrition, matched ally support with legal Low support repertoire (not fabricated self-Rite reassignment), varied damage dice/critical and opportunity/reaction policies, and only then a separately authorized three-Focus tuning recommendation. **`three_focus_balance_certified=false`** intentionally remains true of this v0 evidence audit.
