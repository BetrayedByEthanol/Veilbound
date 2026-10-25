# B04/B05 — Priest Life Role Decision-Gate Playtests v0

> **Bounded source-native encounter stress, not observed human playtests, full combat-role certification, or permission to retune rules.** The [eight-playstyle framework](b04-b05-eight-combat-playstyles-evaluation-framework-v0.md) supplies PS-01 Fighter, PS-02 Defender and PS-08 Healer / Support objectives. Original [Priest formal balance assessment](b04-b05-formal-priest-life-focus-balance-assessment-v0.md) remains a separate historical 1,384-case audit; this document does **not** revise its original signed reports or counts.

## Implementation

- [Source-native executable runner](../../scripts/b05_priest_life_role_decision_gate_v0.py) reuses existing authored H/M/A/B Priest Life profiles and adapters, F High Scholar Fire and R Bow Vanguard allies, authentic Soldier or **prepared** Firebound Sentry, and the original G0/G1/G3/G4/G4.5/G5 attack, defense, Step-2, maintained-effect and healing paths.
- [Focused regression and adversarial tests](../../tests/test_b05_priest_life_role_decision_gate_v0.py) ensure both L1–3 legality and full source replay, no invented miss damage, truthful scene decisions and exact baseline comparisons.
- Original four-recipient adjacent G1 map: Priest (2,1), F (2,2), R (3,3), foe (3,2). **One** genuine source-paid sword attack per real foe turn, **four** rounds, natural Step-2 per actor, no synthetic NPC retarget if scheduled target dies. Nobody acquires any new action, separate Injury packet, outside-Pillar spell, free hand, added Recharge or extra Response.
- Two genuinely constructed initiative orders (**Priest first** vs **foe first**); four independent authored pressure profiles crossing attack face **8/12/16**, damage face **1/4**, Take Hit versus paid **Dodge** defense, and **alternating vs rotating** four-round foe target choices. The script passes damage/vigor/wound dice only after native G0 defense assignment identifies an actual G5 hit. G5 misses are paid but **never** deliver fictitious G4 packets.
- The new report binds level, role, opponent, variant and named Focus policy into the ledger and authenticates **every** original event and final resource state against a fresh independent replay. No caller-shape-derived fabricated policy, impossible VP, altered dice or recomputed fake public digest can produce an attested report.

### Authored decision policies

| Build | Tested legal choices | Role-specific positive opportunity | Unfavorable case or constraint |
|---|---|---|---|
| **H High** | baseline, prepared Guided on F, Basic Heal triage, L3 Guided(F)+Shelter(R) | PS-08 paid sustained/two-recipient support and recovery from real damage | Foe takes initiative, targets change; multiple prepared effects consume real AP, Committed/Spent VP |
| **M Medium** | baseline, prepared Guided on F, paid Basic Heal triage, L3 Guided Intercession to R, L3 Shelter Intercession to R from one self host | PS-08 actual other-beneficiary Step-2 or positive Sentry Direct-Vigor packet, with 2 Spent VP and one real Reaction each | One host L1–3; explicit coverage where Dodge/missed attack or no eligible recipient prevents Intercession; choice of paying versus preserving Reaction |
| **A Low Guided** | baseline, self Chosen Guided, hand-legal external Basic Heal, L2–3 Chosen plus external Heal | Source-funded self-sustain/limited party triage, candidate PS-01 | L1 cannot commit self Rite **and** spend 2 VP for external Heal simultaneously; no demonstrated generic Fighter offense |
| **B Low Shelter** | baseline, self Chosen Shelter, L3 Vital Interposition | Actual source finite self-prevention and own-turn pressure, candidate PS-02 | Mace+shield means **no** legal free-hand external Heal, no external Chosen target, and self-prevention is **not** automatically ally-protection proof |

The M policy names **do not** imply two simultaneous competing native Reaction windows. A genuine second eligible Reaction opportunity with a paid alternative defense/intervention remains **open**; Dodge assigned as the target's ordinary defense does not by itself consume the Priest's magical Reaction. The new matrix distinguishes **paid Intercession** from **unpaid due to missed/invalid trigger**. Do not claim resolved alternative-Reaction utility until an authored source-native competing Response is available.

## Comparison discipline and decision

For each exact **role × level × opponent × variant**, execute a **no-magic baseline** with the same original actor, dice, geometry, attack target schedule, initiative order, damage pressure and defense choice. Compare paid costs and resource balances for every policy. Only report HP/Vigor endpoint differences as **like-exposure** if both original and modified cases have equal number of native paid attacks, real hits and unavailability/dead-target skips. Differing realized enemy exposure is an **outcome**, not a free measured health benefit. Compare the three distinct recipients independently; do not collapse prevented Vigor, healed HP and a physical attack into one fictional utility point.

The source runner emits:
- native four-source digests, complete encounter ledger hash, original event counts, attack hit/miss and unavailable-target counts;
- per-recipient HP, Vigor, wounds, death, natural actual HP regeneration; genuinely established self/ally effects, Basic Heal receipts, Guided/Vital Intercession and Reaction expenditure;
- original available/committed/spent VP, paid Priest AP and separately labeled same-source/matched-exposure endpoint deltas;
- case and full-matrix SHA-256, **replay** attestation rejecting rehashed forgeries, falsifiable completion flags.

**Decision:** retain all existing Priest AP/VP, Life technique costs, Rite restrictions, action economy and wound rules for controlled tabletop playtests. These new scripted cases support role **mechanical opportunity/countercase testing**, not overall mathematical equality, observed win rates or a selected strongest Focus. No automatic tuning is authorized.

### Explicit open gaps after v0

- **PS-01 Fighter:** source-bound Low Priest outgoing offense, actual risky maneuvers and true pressure on an enemy, not only survival while taking enemy attacks.
- **PS-02 Defender:** actual prevented **ally** enemy action/damage through meaningful original positioning/Intervene/guard; Low self-protection is not an ally-protection certificate.
- **PS-08 Support:** full distinct-target party objective under truly adaptive target changes, blocked magic lanes, wounds, actual long-time recovery and unexpected player decisions.
- **Medium Reaction conflict:** **two truly legal simultaneous/competing native Reaction opportunities** with an alternative cost. Only single eligible Intercession and its missing-trigger branch are attested here.
- Randomized/variable natural roll *distributions* and independent sampled GM/player policies; scripted d20 faces are deterministic, **not** probability observations.
- Complete opposed victory/defeat/withdrawal, post-exit safety, social/exploration and independently certified all-Focus L1–3 build progression.

A smaller gain at L1 is not inherently a balance defect or reason to compensate Low with unauthored free control. Allow specialization, different VP rhythms and level drift, but demand a usable action at every represented level. The proposed 15–20% investigation band from the playstyle framework is **not applied** to incommensurable deterministic HP/Vigor totals.

**Certification flags remain false:** PS-01 complete Fighter, PS-02 full ally Defender, PS-08 full Healer / Support, global Focus balance, numeric tuning. All six strict MVP exit gates remain unchecked and B04/B05/B06/B07 remain blocking. No generated win-rate or CR.

## Reproduction

```bash
python -m unittest tests.test_b05_priest_life_role_decision_gate_v0 -v
python -m unittest discover -s tests -v
python -m scripts.b05_priest_life_role_decision_gate_v0 --role M --level 3 --opponent sentry_prepared --variant surprise_heavy --policy shelter_intercession --seed 0
python -m scripts.b05_priest_life_role_decision_gate_v0 --role A --level 2 --opponent soldier --variant cautious_dodge --policy chosen_and_heal --seed 0
python -m scripts.b05_priest_life_role_decision_gate_v0 --seed 0
```

Output is source-specific to the audited commit and must be regenerated after source changes. Passing GitHub Actions verifies implementation integrity, **not** human playtest balance or final MVP role certification.
