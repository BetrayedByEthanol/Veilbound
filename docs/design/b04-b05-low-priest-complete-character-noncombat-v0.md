# B04/B05 — Low Priest L1–3 Complete Character & Noncombat Verification v0

> **Two authentic source-selected Life/Low Priest variants (A/B), six independently audited L1–3 full sheets, ordinary source-trained checks and eight paid utility-action receipts.** This is **not** full Focus certification or human/GM gameplay. The source-native A/B combat actors remain the previously verified physical G0 projections; no existing G0–G8 rules, enemy statistics, Chosen Rite engine, numerical balance or player-option permissions change.

## Missing link resolved

The [17 October original A/B build record](b05-life-low-priest-l3-build-exaltation-verification-v0.md) specified nine Abilities, two trained weapon points, eight learned discipline points, an additional L2 discipline point, every Talent selection, 150-sp purchases, valid Life preparations, Chosen Devotion, one active Rite, L3 Exaltation, hand constraints and HP/Vigor/VP/AP across levels. However, `party_actor("A"/"B")` exposed **only the physical G0 source**, and the later [#186 noncombat scene resolver](b04-b05-source-legal-noncombat-scene-resolution-v0.md) therefore assigned **zero learned training** to both Low Priest alternatives. Those missing technical source fields—not an absent canonical Low Priest subsystem—are filled here.

## Complete selected L1–3 profiles

`scripts/b05_low_priest_life_l1_l3_v0.py::profile(role,level)` owns the two explicit build selections. It does not derive purchased skill or spell access from an A/B physical-only G0 actor, nor invent a shared character that combines both paths.

| Actual selected choice | A — Restorative Vanguard | B — Preservation Guardian |
|---|---|---|
| L1 Learned Disciplines | Veil Theory +2, Life Pillar Lore +2, Medicine +2, Acrobatics +2 | Medicine +2, Herbalism +2, Survival +2, Life Pillar Lore +2 |
| L2 additional discipline | Survival +1 | Veil Theory +1 |
| Weapon Training | One-Handed Swords +2 | Blunt Weapons +2 |
| L1→L2→L3 Talents | C02 → C05 → C10 | C05 → C01 → C09 |
| L1 Prepared | Guided Regeneration (Chosen), Basic Heal | Vital Shelter (Chosen), Basic Heal |
| L2/L3 Prepared | Add Woodland Rapport | Add Venom Endurance |
| L1 gear (sp) | Leather 25, Sword 22, Medical kit 15, Pack 8; **80 left** | Brigandine 95, Mace 16, Shield 16, Medical kit 15, Pack 8; **0 left** |
| Starting hands | Sword wielded, **one free** | Mace + shield equipped, **no free hand** |
| Max HP | 12 | 13 |
| Max Vigor L1/L2/L3 | 12 / 24 / 36 | 13 / 26 / 39 |
| Max VP L1/L2/L3 | 2 / 4 / 6 | 2 / 4 / 6 |
| L3 available Exaltation | Held Renewal on an actual Chosen self-Guided host | Vital Interposition on an actual Chosen self-Shelter host |

Each level has 30/36/42 Turn AP, Low Physical Action 20 AP, Projection Action 30 AP, canonical Universal Veil Inspection at L1 and Blink *known* at L3 but unaffordable at 10 Spent against max 6 VP. Ordinary starting loadout does **not** permit B to use Basic Heal with mace and shield both occupying their hands; this adds no invented free item swap. Chosen is one specifically activated, maintained self-Rite and cannot transfer to the other Prayer. Normal Rites still pay ordinary costs. No automatically granted preparation change, six-hour recovery or free level-up refill is presumed.

## Independent structural and G0 provenance

The existing `b04_b07_independent_progression_audit_v0.py` now independently runs the **canonical cross-source sheet checks** on each selected A/B L1/L2/L3 snapshot. Additional independent expected A/B selection tables check exactly purchased Learned Disciplines, weapon family, preparation/Chosen identity, starter equipment, actual occupied hands, one Rite, L3-only Exaltation and direct reconciliations against the **unchanged live physical G0** actor: source Abilities/level, HP/Vigor/VP, AP, regeneration, Guard and Initiative. This is not merely `profile().verify()` asserting its own fields.

The independent roster still counts **12 Archetype × Focus pairings, 13 structural variants and 39 level snapshots**. Low Priest remains *one* Focus pairing with A and B selected variants. It retains the original physical source and design-record digests, and adds a separate full-sheet SHA-256. All subsequent user-external certification packets must carry the new complete source fingerprint; historical source run receipts stay unchanged. No independent human attestation is fabricated.

## Source-backed noncombat evidence

- Ordinary checks: both A and B gain real **Medicine +2** on applicable medical diagnosis; only A gains **Acrobatics +2** when balancing. Both still use their actual Presence on an untrained public-record petition. The G4.2 world clock and preauthored GM consequences are inherited from #186; these are deterministic author scenarios, not externally judged skills.
- Native Universal **Veil Inspection**: actual G0 **Full Action**, **2 Spent VP**, held observable Life/Restoration-pattern fixture, six separate A/B × L1/L2/L3 receipts. It reveals no unobserved cure or hidden enchantment.
- Selected A **Woodland Rapport**, L2–3 only: actual 30-AP Projection and 2 Spent VP against a bounded nonhostile, visible animal no heavier than 25 kg, for two additional native receipts. GM animal response remains explicitly unresolved; no forced animal obedience, speech, or free recovery is introduced.
- B's authored **Venom Endurance** remains Prepared at L2–3, but this PR **does not invent an independent toxin target, reaction, extra duration or protection outcome**. Its exact defensive/other availability is subject to the original technique's mechanics and actual table setup. Likewise L3 Exaltation uses the previously merged G0/G3/G4 native Rite adapter, not a new noncombat spell engine.

The new `b04_b05_low_priest_complete_noncombat_v0.py` produces **six level/variant records, 18 original ordinary core-check scenes and eight paid native utility actions**. It refuses A L1 Rapport, all B Rapport, illegal animal targets, unearned options and foreign variants. Existing #185 proxy-only combat/noncombat evidence remains a *historical bounded report*, not retroactively reclassified as observed full sheets; updated #186/#188 live scene outputs explicitly report full selected-sheet training while still retaining their unchanged physical G0 provenance.

## Run

```bash
python -m scripts.b05_low_priest_life_l1_l3_v0
python -m scripts.b04_b05_low_priest_complete_noncombat_v0
python -m unittest discover -s tests -p 'test_b04_b05_low_priest_complete_noncombat_v0.py' -v
python -m unittest discover -s tests -p 'test_b04_b05_noncombat_scene_resolution_v0.py' -v
python -m unittest discover -s tests -v
```

The B04/B07 exact-PR-head independent audit workflow executes these tests alongside the historical progression/protocol and noncombat suites, exports a new **separate** Low Priest JSON register and retains existing bounded evidence artifacts.

## Unclosed acceptance

The new data supplies complete *selected source records*, actual native cost/Training receipts and negative alternatives, **not an independently certified Low Priest Focus**. Still missing: real player decisions through L1–3, representative GM-run combat **and** noncombat choices at each level, source-backed toxin/downtime/Chosen release/recast across genuine connected encounters, independent external reviewer approval, and actual group milestones. **12/12 structural, 0/12 independently full-certified, 0/6 MVP exit gates, 3/7 original blockers definition-closed**, unchanged.
