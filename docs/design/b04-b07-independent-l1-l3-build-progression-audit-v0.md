# B04/B07 — Independent L1–3 Build and Progression Audit v0

> **Independent mechanical review, not a full playable Focus certificate.** This report audits all **12 Archetype × Focus pairings**, **13 physical/source variants** (Low Priest A and B count as one pairing) and **39 L1/L2/L3 snapshots**. It does not claim player/GM role witnesses, verified two-milestone adventures, representative encounter outcomes, or 12/12 independently certified Focuses.

## Audit method and authority

The independent [executable cross-source audit](../../scripts/b04_b07_independent_progression_audit_v0.py) imports each selected original profile(level) but **does not call the original profile's own verify() or trust its source_legal/certified booleans**. Each sheet is checked against separately coded creation and progression rules: the 28-point nine-Ability schedule, two separate Weapon Development points, eight starting Learned Discipline points plus one at L2, the no-extra-L3-training/no-before-L4-Ability gates, 150 sp starting budget with no automatic level-up loot, exact Focus-based Max VP, HP/Vigor and 30/36/42 Turn AP, physical/projection AP tempo, L1 Veil Inspection and L3 Blink (access is **not** VP affordability), L1/L2/L3 regular Tier gates, and unchanged selected skills, equipment, bonds/links as applicable. At L3, the Talent count must respect the authored [B07 early-level Focus awards](../rules/10-advancement/talents-framework-v0.md), including explicit saved-selection accounting rather than inventing a choice.

Each witness records the original source-file SHA-256 and its independent findings. The **Low Priest A/B** case uses the actual G0 physical proxy actor at each level and cross-checks the separate [authored A/B build record](b05-life-low-priest-l3-build-exaltation-verification-v0.md); this is intentionally **not claimed to be a complete generic Low Priest profile**. It does not convert a physical proxy into proof of unrestricted spellcasting, Chosen Rite legality, or full noncombat play.

The verifier separately checks *hypothetical* GM-declared L1→L2→L3 receipts: exactly two distinct, explicit story-event IDs, correct character, one level at a time, and non-automatic awards. No two events have actually occurred. This validation does not award levels, grant new Training/Talents, refill Available VP, refill Destiny, add known techniques, or infer XP. Only a real GM session/adventure record can establish the milestones happened.

## Findings requiring follow-up

| Source pairing | Level | Finding | Classification / next action |
|---|---|---|---|
| **High Priest / Life** | L3 | Sheet includes a second selected Talent, **TAL-M03 Frugal Technique**, although the adopted provisional High Focus schedule awards only the L1 selection before L5 | **Over-award / structural progression inconsistency**. Remove or separately explain the extra selection through a documented authorized rule; do not presume its effects legal |
| **Medium Gifted / Ward** | L3 | Only the L1 Talent is shown although Medium Focus earns a second selection at L3 | **Unaccounted earned selection**, not necessarily illegal. Choose a legal L3 Talent or explicitly record it as saved, with no free effect |
| **Low Scholar / Embodiment** | L2–L3 | The build shows L1 Talent and adds a Talent at L3, without accounting for the distinct L2 award | **Unaccounted earned selection**, not necessarily illegal. Identify an actual L2 choice or explicitly record the saved award. No retroactive free combat effect |

These are **source observations**, not silently corrected character choices. The executable audit produces machine-readable pairing/level issue codes. A future corrective PR should reconcile source snapshots, the rule's Talent ledger, associated independent checks, native actor-derived Talent modifiers, and any affected bounded evidence before claiming that the relevant L1→3 structural progression is fully validated. In particular, removing High Priest's unauthorized L3 Talent is more than a documentation change if prior encounters relied on its VP discount.

## Verification vs certification matrix

- **Checked now:** original source provenance and independent bounded budget/award/progression validation across the twelve pairings; three Talent-accounting discrepancies discovered and explicitly retained.
- **Not yet checked as independent full-Focus evidence:** complete L1, L2 and L3 combat **and** noncombat role alternatives, meaningfully weak options/counterplay, all required native spell/technique/pilot choices, level-transition actual resource conservation across real sessions, genuine GM-authored consequences, and independent acceptance sign-off.
- **Strict MVP exit gates:** still **0/6**. Independent full Focus certificates still **0/12**. Original B01–B07 closure remains **3/7**. Structural source pairings remain **12/12 present**, but mechanical progression corrections are open. Original B06 G0–G8 milestones remain fixed.

## Reproduce

From the repository root:

    python -m unittest -v tests.test_b04_b07_independent_progression_audit_v0
    python -m scripts.b04_b07_independent_progression_audit_v0

The JSON reporter includes the SHA-256 provenance, every structured issue, explicit noncertification and missing evidence. The test suite includes negative tampering of earned VP, training, illegal early Blink and Talent access, and illegal/missing GM milestone chronology. Passing these tests **does not imply a completed adventure or 12 Focus certificates**.
