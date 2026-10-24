# B04/B05 — Medium Priest Life L1–3 Character Build and Consecration Verification v0

> **Scope:** one source-selected Medium Priest / Life character across L1–3,
> plus bounded genuine G0/AP/VP, G3 maintained effects and G4 regeneration/Vigor
> receipts. This is **structural and native mechanic evidence**, not an
> independent end-to-end MVP Focus certification or representative combat pack.

## Canonical rules (no new feature or technique)

- [Priest Foundation](../rules/08-archetypes/priest.md): starting +1 Pillar
  Accord, Medium base prepared capacity 2/3/3 (+1 Accord gives **3/4/4**),
  one Active Consecration at L1–3, 24-AP Reassign; L3 Reaction plus
  provisionally **2 Spent VP** Intercession; no High Open Invocation.
- [Guided Regeneration](../rules/07-veil-magic/guided-regeneration-v0.md):
  **2 Committed VP**, +1 at *existing* recipient Regeneration Step, no new
  step, normal 3-square living recipient targeting, shared no-stacking.
- [Vital Shelter](../rules/07-veil-magic/vital-shelter-v0.md):
  **2 Committed + 1 Spent VP**, initial **8 + max(0,VC)** finite direct
  Vigor-damage budget; no budget refresh on Reassign, and L3 Intercession
  consumes **one actual packet** from that *same* budget.
- Both Consecration activations require an own-turn Medium **24-AP**
  Projection Action. The fixed **2-Spent/60-second** spell modes are **not**
  Consecrations and are **not implemented by this bounded adapter**.
- The source character selects its existing [L1–5 Talents](../rules/10-advancement/talents-level-1-5-v0.md)
  and reuses the legal ordinary mundane allocation from the previously verified
  [Life Low Priest source build](b05-life-low-priest-l3-build-exaltation-verification-v0.md).
  The allocation is a *new character choice*, not a Low-Focus feature transfer.

## Exact source sheet

| Field | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| Focus/Pillar | Medium / Life | same | same |
| Nine Abilities | STR+2, AGI+3, PRE0, INT0, AWA+1, PRES−2, VIT+2, VA0, VC0 | unchanged | unchanged |
| Ability purchase | 28 | 28 original | 28 original |
| Weapon Training | One-Handed Swords +2 | same | same |
| Learned Disciplines | Veil Theory+2, Life Pillar Lore+2, Medicine+2, Acrobatics+2 | same + Survival+1 | same |
| Talents | TAL-C02 Enhanced Regeneration | unchanged | + TAL-M03 Frugal Technique |
| Prayer list | Guided Regeneration; Vital Shelter; Basic Heal | plus Woodland Rapport (at legal preparation) | same four |
| HP / Vigor | 12 / 12 | 12 / 24 | 12 / 36 |
| Max VP | 4 | 8 | 12 |
| AP / Physical / Projection | 30 / 24 / 24 | 36 / 24 / 24 | 42 / 24 / 24 |
| Regeneration throughput (without Guided) | 5 | 5 | 5 |
| Active Consecrations | 1 | 1 | 1 |
| Normal Used Tier ceiling | T1 | T1 | T2 |
| Automatic Universals | Inspection | Inspection | Inspection and Blink |

Starting mundane purchases: leather armor **25 sp**, sword **22 sp**,
medical kit **15 sp**, adventuring pack **8 sp** = **70 sp**, with **80 sp**
remaining. Sword held in one hand, other hand available for Basic Heal.
Guard Defense with sword is **17**; ordinary first Dodge Defense **14**,
initiative modifier **+4**. Max normal Guard capacity is **1** at all L1–3
Medium levels absent other modifiers. A L3 Blink is known and in principle
payable with 12 fully Available VP; not an automatic free cast.

The character retains only its permitted one-Pillar Prepared Life Prayers.
No unprepared casting, cross-Pillar magic, Chosen Rite, Exaltation or high-tier
Miracle is granted. At L3, Basic Heal and Woodland Rapport may use their
*existing* T2 profiles only when legally paid. The normal Miracle Petition
framework is available but the packet does not invent a requested technique.

## Native execution boundaries

New `scripts/b05_medium_priest_life_l1_l3_v0.py` provides immutable-choice
profile snapshots for all three levels; G0 `party_actor("M", ...)` now loads
them as an independently sourced actor. Existing R/F and A/B actor roles are
unchanged. The source-based `MediumLifeConsecrations` adapter attaches to
the existing G3 rather than owning a parallel VP economy:

1. A prepared, successfully applied maintained Consecration pays existing
   G0 Projection AP and VP transitions and creates a genuine G3 effect.
   G3 owns release/refund and the relevant existing G4 hook. No effect
   is added for illegal or pre-application interrupted casts.
2. Reassign pays actual **24 General Tempo AP**, changes *one existing* G3
   effect recipient, preserves its Committed VP and remaining Shelter budget,
   and never initiates healing/prevention or a new Regeneration Step.
3. Guided L3 Intercession is only accepted while the beneficiary has
   an actual pending **G0 Step 2**; the native G4 Regeneration Step consumes
   exactly +1 potential throughput, funded by one Reaction and 2 Spent VP.
   There is no extra step or ongoing second recipient.
4. Shelter L3 Intercession is selected for a **positive confirmed G4 direct
   Vigor packet** during `DamageState.apply_damage`. G4 must be installed;
   the source Medium Priest pays one Reaction + 2 Spent VP; the one packet
   consumes the *original* finite G3 budget. G4 applies only the residual
   packet to target's Vigor; budget exhaustion ends/refunds the G3 effect.
5. G1 live clear-grid sight/range/wall checks are enforced for other
   one-square recipients, including fresh Reassign/Intercession selection.
   This bounded procedure treats target cooperation as explicitly authored
   scenario policy; **actively contested Intrusion, three-dimensional/multi-cell
   delivery, complex response ordering and broader actor policy remain
   unresolved** rather than generating a made-up resistance result.

## Evidence and rejection gates

`python -m unittest tests.test_b05_medium_priest_life_l1_l3_v0 -v`

`python -m unittest discover -s tests -v`

Tests check: each selected build level and bought source allocation; target
range/wall/prepared/cap/AP/VP legality; fixed host ownership and release;
spent establishment no-refund; nonrefreshing reassignment; exactly one
real-target G4 regeneration bonus; Reaction/Spent VP one-event Intercession;
real G4 Vigor packet/budget depletion and committed VP return; invalid
intercession preflight; repeated ledger determinism.

**No independently source-confirmed attacker hit/GM defense/damage packet is
produced by the fixed G4 Intercession witness**: the test supplies an
explicitly confirmed typed damage packet, then tests the genuine G4/G3
consequence. That is not a representative Soldier/Sentry/Hunter encounter.
Native Medium Priest Basic Heal, all six Life prayers, contested Intrusion,
full tactical player/GM policies and complete combat/noncombat scene evidence
are still future integration work. In particular this PR does not pretend
that the R/F-only G4 Basic Heal adapter automatically handles the M source.

**Acceptance flags:** structural source build = **true**; bounded native
Consecration/Intercession mechanics = **tested v0**; independent end-to-end
Medium Priest Focus certification = **false**; all-12 Focus certification
unchanged at **0/12**; B04/B05/B07 strict MVP gates **open**.

Intercession price, spell resource opportunity cost and realistic relative
protection-versus-recovery value remain **playtest provisional**. Do not
relabel passing scripted receipts as an accepted encounter win rate.
