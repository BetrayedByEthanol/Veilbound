# B06 — Hunter Tactical and Party Diversity v0 (Phase 3)

> **REVIEW CANDIDATE — CONDITIONAL ONE-ROUND MODEL. NOT A CERTIFIED PARTY BUILD, FULL ENCOUNTER, WIN RATE OR CHALLENGE RATING.** The [seeded Phase 3 runner](../../scripts/b06_hunter_tactical_diversity_v0.py) and [tests](../../tests/test_b06_hunter_tactical_diversity_v0.py) extend the [Phase 2 Hunter windows](b06-hunter-repeated-encounter-calibration-v0.md) beyond an exclusively melee Low Priest group. They distinguish attacker roles and which frontline target the Hunter is actually positioned to reach.

## 1. Provenance and source-bound profiles

The original A/B roles bind to the audited [Life Low Priest Level 1–3 sheets](b05-life-low-priest-l3-build-exaltation-verification-v0.md); they are not new character options. The alternative R/F encounter roles are **provisional numeric witnesses** rather than independently certified complete Level-2/3 character sheets.

| Role | Source/status | Ordinary attack | Resource / defensive boundary |
|---|---|---|---|
| A — sword Vanguard | Audited Low Life Priest A | Sword d20+7; 4+d6 Piercing Pen2 | HP12, leather Armor3, sword Guard17, Low Physical20, L2 1 / L3 2 attacks |
| B — armored Guardian | Audited Low Life Priest B | Mace d20+6; 6+d6 Crush Pen3 | HP13, brigandine Armor5, shield Guard18, Low Physical20, L2 1 / L3 2 attacks |
| R — bow Vanguard variant | A's same 28-point abilities, Low-Focus Tempo, Talents and regeneration, but **Bow Training+2 instead of Sword+2**, not a newly certified progression | Bow d20+4 (STR2 + Precision0 + Bow2); **2+d4 Piercing Pen3**, no STR damage bonus | HP12/Armor3; no legal Guard with bow; one arrow per paid 20-AP shot. Leather25 + Bow26 + 20 arrows5 + dagger4 + pack8 = **68 sp** of ordinary 150-sp budget |
| F — Fire thrower | **Provisional High Scholar** with A's 28-point abilities, Throwing Learned Discipline+2 and one individually known authored Fire / Conflagration **Conjure Flame** Primary | Thrown Flame d20+5 (AGI3 + Precision0 + Throwing2), Tier1; on successful hit **Fire2 HP** plus **Vigor 2+ceil(d8/3)** | HP12/Leather3, no wielded Guard; High Projection20, **2 Spent VP per launched spell** (even a miss), Max VP6×Level at VA0 (L2 12, L3 18), own-turn natural throughput VIT2+High1=3. Leather25 + dagger4 + pack8 = **37 sp** |

**Incomplete build gate:** F's remaining distinct known spell repertoire, other Learned Discipline points, Talent awards, and full L1→3 sheet have *not* been individually established in this slice. F demonstrates one named legal technique/profile; it is not a certified High Scholar. R is a reallocated equipment/weapon-training variant of A, not a distinct Archetype/Focus certification. Neither is counted toward the MVP's required twelve independently proven combinations. The Fire technique does not automatically teach itself to anyone: its use here is a declared *provisional Scholar known-technique choice*. No unauthorized Composite, higher-tier, extra attack, or free VP is granted.

The **original** 3/4-member party is A1, B1, A2[, B2]; the **mixed** party is B1, R1, F1[, A1]. Both use actual Level-2/3 Turn AP (36/42) with no bonus turns. All participants start with full appropriate HP, Vigor and VP and real held equipment, not free mid-fight item swaps.

## 2. Pre-staged Hunter tactics and geometry contract

The matrix is **L2/L3 × 3/4 members × original/mixed × warned/ambush × armored/exposed lead = 32 conditions**. Each condition has **128 matched SHA-256-keyed seeds**, giving **4,096 configured one-round trials**. This is a staged, conditional set of opening encounters, not a pathfinder or a generic initiative/surprise AI.

The Hunter's **armored** front contact is B1. Its **exposed** contact is A1 in the original party or F1 in the mixed party. These are **independently positioned starting states**, not free in-round target switching, impossible 1×2 rotation, teleports or retroactive weapon targets.

In **warned**, the Hunter is already head-forward adjacent to the chosen standing one-square lead; it can pay for an ordinary Bite, **not** an instant Pounce without its three-step approach. In **ambush**, the Hunter begins with a clear cardinal three-square whole-body straight lane to that chosen lead and Pounce is legal only if the Hunter wins Initiative *before every PC*. An earlier PC's ordinary approach breaks that specific starting-run-up assumption. Ambush **does not provide surprise attack bonuses, denied defenses or automatic first turns**.

Other party roles require separately pre-established **nonoverlapping legal attack lanes at action time**: A/B can walk to melee without crossing threatened-exit squares; R has an unobstructed bow lane **7–12 squares away** (Short Range Difficulty +0) with no ally or enemy Living Screen; F has a clear **1–3-square Thrown Flame** lane (+0 on its own authored technique), without cover, intervening creatures or a forbidden inside-target Manifestation. Real maps **must confirm these assumptions** before a played encounter; the runner does not prove every simultaneous placement or moving shot is legal.

**Conservative exposed F:** When Hunter's staged front contact is F, the runner does **not** authorize a free threatened close-range projectile or free withdrawal. It records F's skipped cast instead of fabricating its movement/Opportunity chain. This is a **test restriction**, not a universal rule prohibiting magic while threatened. Backline defensive repositioning remains unmodeled.

## 3. Actual first-round procedures modeled

- Initiative is independent **d20+4** per participant, ties by Awareness, Agility, then a keyed roll. Hunter has AWA2/AGI2; A/R/F use AWA1/AGI3; B uses AWA0/AGI2.
- Hunter pays for **one** normal Bite or **one** eligible 24-AP Pounce, with its natural Bite+6 / 3+d6 Piercing Pen1, post-mitigation puncture-only DC12 toxin, and an independent d20+4 Pounce Balance when Bite damage has not already triggered the run's stopping boundary. A tied Balance fails to knock Prone.
- A/B select actually wielded **Guard17/18**; F has no Guard instrument. Hunter always selects Dodge. First Hunter ranged and melee Dodge both begin at **14**: Hunter Agility2+Awareness2, and Physical Tempo1 grants ranged Evasion bonus0. Every further chosen Dodge reduces its Defense by 2 **including misses**. No free Guard, armor-stacking, cover, size or flank modifiers.
- A prone lead commits **4 MP** to Stand and remains Prone throughout the Hunter's first eligible Standing Opportunity, granting Hunter **+2 melee attack**; Standing completes only if responses leave it legal. If the Opportunity produces terminal wound damage, no subsequent toxin/Stand completion is generated.
- Natural 1 misses; natural 20 gets the authored **single confirmation**. Strong +1d4, Critical/Devastating +2d4 apply **once to the primary hit HP packet before Armor or typed resistance**. R's Bow rolls d4 damage, not d6; Strength never adds to Bow damage. Flame has **Fire2 primary HP** with no invented physical Armor mitigation, plus independent **Vigor burn** on a hit even where Fire HP is zero. No critical Vigor multiplier.
- An unthreatened F uses **one Projection20 + 2 Spent VP** per thrown flame, *even on a miss*. R uses a paid Physical20 and **one physical arrow** per actual shot. At L2, the 36-AP pool buys one such action; at L3, the 42-AP pool buys two. No extra automatic composite or reload benefit.
- The Hunter's genuine own-turn Step2 restores **up to 4 missing HP for matching Vigor**, even when higher-Initiative PCs hit it before that Step. The lead's own-turn Step also spends recipient Vigor when repairing missing HP. No Round-Begin restoration or extra Step is invented.
- Entire HP and Vigor packets of **one legal hit** resolve before its terminal check. The bounded trial then ends on **Hunter's first HP≤0**, **lead's first HP≤0**, or **a Devastating unresolved wound**; it does not process subsequent toxin/Pounce/other actions. Otherwise it stops after **one round**. A fallen Hunter is Dying, not automatically dead; a fallen lead is not a wiped party.

## 4. Outputs, limitations and acceptance

From repository root, the following script reports the terminal-category counts, Pounce declarations/actual Balance resolutions, Full/Reduced accepted toxin instances, Spent VP, arrows fired, Vigor burn and mean Hunter HP for every one of the 32 case records:

    python -m scripts.b06_hunter_tactical_diversity_v0

**No numerical 32-cell census is asserted yet**: the new 4,096-trial matrix is *configured*, but the actual GitHub checkout and its runner need Codex/CI verification before any figures are published as results. Six standard-library tests check sourced stats and damage, natural-20 Fire/Bow packet separation, terminal-Bite precedence, seed replay, 32-cell conservation and bounded AP/ammunition/VP. Their presence does not by itself establish a passing CI run.

**Not simulated:** true map collision/cover and mixed Living Screen, multiple turns, actual Guard/Intervene of other PCs, accurate threatened-caster Withdrawal, adaptive Hunter redirection, actual Dying/wound repair, post-combat venom T+10/30/60/120, real Priest Rite/Exaltation or non-Conjure Scholar spells, VP six-hour Recovery, and player GM negotiation/flight. **No Hunter numeric CR or party victory probability is justified, and B06 remains an MVP blocker.**

**Next acceptance steps:** Run the 32 cells and audit every line against real deployment geometry; author complete independently legal R/F advancement sheets in B05/B07; add actual terrain/LOS/opportunity/retreat and genuine multi-round wound resolution; test active spells and varied Hunter target switching. Do not enlarge statistical sample size as a substitute for those legal/tactical gaps.

### Required checkout validation

    python -m scripts.b06_hunter_tactical_diversity_v0
    python -m unittest discover -s tests -p 'test_b06_hunter_tactical_diversity_v0.py' -v
    python -m unittest discover -s tests -v
    python -m scripts.validate_b06_footprints
