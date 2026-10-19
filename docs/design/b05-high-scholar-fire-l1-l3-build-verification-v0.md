# B05/B07 — High Scholar Fire Level 1–3 Character Build and Verification v0

> **STRUCTURAL BUILD CANDIDATE, executable source-bound ledger.** This is the first explicitly assembled **Scholar / High Focus** character for the [Hunter Phase 3 F combat witness](b06-hunter-tactical-and-party-diversity-v0.md). The term *Fire Thrower* describes its primary offensive attack; **Scholars are cross-Pillar technical casters, not automatically Fire-only Priests**. This record neither expands the spell catalogue nor certifies a full High Scholar combat/exploration loop, 1 of the 12 required Archetype×Focus identities, a completed B06 encounter or a Hunter CR. B06 F combat statistics and the 4,096-window Phase 3 trial algorithm **remain unchanged**.

## 1. Identity, ability array, Training and Talent

The actual rules are [Scholar](../rules/08-archetypes/scholar.md), [character creation](../rules/02-character-creation/character-creation-foundation.md), [abilities and Training](../rules/02-character-creation/abilities-and-training.md), [Focus action costs](../rules/09-focus/focus.md), and [B07 Talents](../rules/10-advancement/talents-level-1-5-v0.md). This build makes **choices within the current provisional rules**, not new mechanical entitlements.

| Field | Selected High Scholar v0 | Legality |
|---|---|---|
| Archetype / Focus | **Scholar / High (Projection)** | Individual learned techniques; no Priest Pillar Accord or Chosen Devotion |
| Nine abilities | **STR+2, AGI+3, PRE0, INT0, AWA+1, PRES−2, VIT+2, VA0, VC0** | **28** creation points: 5+7+2+2+3+0+5+2+2 |
| Starting Weapon Training | **Small Blades +2** | 2 separately purchased Weapon Development ranks; **not** added to Thrown Flame |
| Starting Learned Disciplines | Veil Theory **+2**, **Pillar Lore (Fire) +2**, Throwing **+2**, Medicine **+2** | 8 points, cap +2; default **4 Scholarly / 2 Physical and Fieldcraft / 2 flexible Professional and Technical** |
| Level 2 Learned Discipline | **Alchemy +1** | Exactly one new level-2 point; no additional rank at level 3 |
| Level 1 Talent | **TAL-U01 — Veil Insight** | Eligible from directly invested Veil Theory +2; one failed, applicable observed Veil-structure/lore interpretation reroll per six hours; not a general casting/Attack or initiative bonus |
| Talent additions L2–3 | **None** | High Focus receives only one selection during levels 1–3; do **not** import Low Focus additional Talents |
| Universal Resonance | **0** | Does not imply Pillar Accord; Pillar identity belongs to each individual learned technique |
| Background familiarities | Arcane study community; local practical herbal and medical work | Descriptive context only, no Training modifier or guaranteed social advantage |
| Abilities advancement L2–3 | **None** | Next normal +1 Ability at level 4 |

The **Small Blades +2** purchase gives a possible normal **dagger Attack d20+5**, **3+d4 Cut/Pierce Pen0** and **Guard15 only if the dagger is actually wielded and its Guard is otherwise legal**. Its existence does not alter F's Stage-3 setup: F **carries** its dagger but has **no Guard instrument in hand** while throwing Flame; `ROLE["F"]["guard"] = None`, `guard_extra=0`. Ordinary equipment readying and required casting hands remain subject to their authored action/timing restrictions. It would be incorrect to give F Guard15 in the previously published one-round census.

## 2. Equipment and money — frozen F loadout

| Starting purchase | Price |
|---|---:|
| Legal starter Leather armor (Armor3) | 25 sp |
| Dagger (carried, not wielded in Phase 3 F snapshot) | 4 sp |
| Standard adventuring pack | 8 sp |
| **Total** | **37 sp** |
| **Unspent starting budget** | **113 sp** |

There is **no staff, bow, wand, free kit, magical implement, crossbow ammunition or heavy/battle robe** in the original F profile. Ordinary clothing/robe appearance is assumed worn for free at Armor0, **not** bought as the starter-prohibited heavy padded/battle robes. No unlisted weapon acquisition or item discount is implied. High Focus/Scholar has **no extra equipment purchasing privilege**.

## 3. Individually known Pillar repertoire

The [Scholar starting repertoire v0](b04-b05-priest-scholar-starting-repertoires-v0.md) and [canonical Scholar page](../rules/08-archetypes/scholar.md) give **5 known individual Pillar techniques at L1, +1 at L2, no additional learned technique at L3**. Universal Veil Inspection and Blink are separate and consume no known slots. A spell with many profiles still occupies **only one** known slot.

| Acquisition | Known technique | Pillar / Aspect | Primary role |
|---|---|---|---|
| L1 (1) | [Conjure Flame](../rules/07-veil-magic/conjure-flame-v0.md) | Fire / Conflagration | **F's Tier-1 `Thrown Projectile`**: d20+5, Fire2 HP plus separate Vigor burn; also known eligible weapon/ammunition profiles but **not automatically used** |
| L1 (2) | [Stone Skin](../rules/07-veil-magic/stone-skin-v0.md) | Earth / Fortification | Maintained **`Self`** typed HP resistance; normal or authorized reactive activation |
| L1 (3) | [Basic Heal](../rules/07-veil-magic/basic-heal-v0.md) | Life / Restoration | **`Self` / `Single Target`** restorative Primary and authorized `Self` composite Secondary; **one functioning available hand** |
| L1 (4) | [Minor Telekinesis](../rules/07-veil-magic/minor-telekinesis-v0.md) | Mind / Psionics | **`Single Object`** inanimate-object manipulation, not free weapon collision damage or creature control |
| L1 (5) | [Phantom Sound](../rules/07-veil-magic/phantom-sound-v0.md) | Secrets / Hallucination | Short sound/distraction signal; **does not** confer mind control or High Scholar Secondary permissions |
| L2 (6) | [Vital Shelter](../rules/07-veil-magic/vital-shelter-v0.md) | Life / Preservation | Finite Vigor-damage prevention via legal target profile and paid mode; can be one authorized `Self` composite Secondary |

All five starting choices are authored **Tier-1** techniques, and the level-2 addition is also authored. **A Tier-2 ceiling at L3 means a known technique may use only its expressly authored Tier-2 profile**: for example, L3 can use Conjure Flame Thrown T2 and Basic Heal T2; it does not automatically learn a seventh technique or amplify Phantom Sound, Stone Skin or Vital Shelter without explicit scaling. No entire Fire Aspect/Pillar catalogue is granted.

### Prepared Composite Formulae (exact and ordered)

Normal known **Primary** techniques are available as individual spells without requiring preparation. Only an explicitly authorized *Composite* needs High's L1–2 formula list; high preparation uses **10 uninterrupted minutes of technical study**, at most once per six elapsed hours, except the freely chosen initial L1 set. Level-up new capacity is filled at the **next legal preparation**, not instant spontaneous study.

| Level | Prepared composite capacity | Actual chosen list / rule |
|---|---:|---|
| **L1** | 1 | **Stone Skin Primary + Basic Heal Secondary**, exact shared `Self` profile, **normal on-turn Projection**, self recipient only |
| **L2** | 2 | Retain previous formula, then add **Stone Skin Primary + Vital Shelter maintained Secondary**, exact shared `Self` profile at next legal technical preparation |
| **L3** | No preparation required | **Formula Fluency**: no advance pair selection; *any otherwise authorized known pair* may be selected on its own legal cast, with normal full component prices |

The **L1 Stone Skin + Basic Heal** authorization comes directly from Stone Skin's High Scholar section and Basic Heal's compatible `Self` Secondary. At VA0/VC0 and T1, it uses **one High 20-AP Projection Action**; **Stone Skin commits 2/4/6 VP** at L1/L2/L3 as `ceil(MaxVP/3)`, and **Basic Heal spends 2 VP**. Total up-front Available VP required **4/6/8**. At full L1 VP6: **Available2, Committed2, Spent2** after a successful activation, and Basic Heal Secondary produces only **1 HP + 3 Vigor** restoration *up to missing amounts*, **once**. The composite is not a reusable heal pulse.

The **L2 Stone Skin + Vital Shelter** authorization is also explicitly authored under Stone Skin and Vital Shelter. It uses one normal High 20-AP Projection Action; at VA0/VC0, Stone Skin commits **4 VP** and the maintained subordinate `Self` Vital Shelter commits **2 VP** and spends **1 VP**, so starting from L2 full MaxVP12 the successful cast leaves **Available5, Committed6, Spent1**. Its **S4** finite Vigor protection is subordinate to the maintained Stone Skin host; it is not the full independently maintained Shelter B8 and cannot transfer to another target. A simultaneous second standalone Stone Skin or unauthorized additional maintained instances remain illegal. At L3 the T1 example requires **9 VP** before casting (6+2 committed, 1 spent).

**Important negative gate:** Conjure Flame's `Thrown Projectile` Secondary requires a separately known genuinely compatible **`Thrown Projectile`** Primary. **None of the five other selected known techniques provides that lawful pairing here**. Therefore **there is no prepared Flame composite, no Fire+Stone Skin shortcut, and no automatically available magic-arrow composite**. Neither an identical-looking generic spell delivery nor a Rider cell grants composite authorization.

## 4. Derived levels 1–3 ledger

| Value | L1 | L2 | L3 |
|---|---:|---:|---:|
| Max HP (10+VIT2) | **12** | 12 | 12 |
| Max Vigor = HP×level | **12** | 24 | 36 |
| Max VP = (6+VA0)×level | **6** | 12 | 18 |
| Turn AP | 30 | 36 | 42 |
| Physical / Projection / General Tempo action cost | 30 / 20 / 24 | 30 / 20 / 24 | 30 / 20 / 24 |
| Physical / Projection Tempo | **1 / 1** | **1 / 1** | **1 / 2** |
| Normal Guard capacity (equipment not wielded) | 1 | 1 | 1 |
| First Dodge / Initiative modifier | **14 / +4** | 14 / +4 | 14 / +4 |
| Natural once-per-turn Regen throughput | **3** | 3 | 3 |
| Known Pillar techniques | **5** | 6 | 6 |
| Actual prepared formulae | **1** | 2 | Not required |
| Max ordinarily permitted Used Tier | **1** | 1 | 2 |
| Ordinary 20-AP Thrown Flame T1 launches per full pure-projection turn | **1** | 1 | 2 |
| Automatically known Universal procedures | Inspection | Inspection | Inspection, Blink |

A **Thrown Flame** declaration pays one **20-AP Projection Action**; each **T1 launched** spell costs **2 Spent VP** (misses included) and is **d20+AGI3+PRE0+Throwing2 = d20+5**, at exactly **1–3 squares**. A successful T1 hit causes **Fire2 HP plus separate Vigor `2+ceil(d8/3)` = 3–5** at VC0; Fire Resistance does not automatically protect against the Vigor packet. Do not add the Scholar's Veil Theory, Small Blades, Veil Practice, VC or level to the attack roll. L3 may cast two such separate 20-AP T1 Flames from 42 AP and sufficient VP; it does **not** receive a free attack. A T2 Flame costs **4 Spent** per launch and can be used at L3 where legal, at the technique's independently authored T2 Vigor values.

A physical dagger attack costs **30 AP** for High Focus. Even at L3, **30+20=50 >42**, so it cannot combine a normal dagger attack and Thrown Flame in one turn. The dagger is not wielded in the original F starting situation. Basic Heal requires an available hand, and Thrown Flame's free manifestation also requires one functioning available hand; no free item swap or no-hands casting is implied. Stone Skin's lawful **Reaction activation** is not a free out-of-turn Composite Casting, and its maintained VP reservations reduce Available VP for later spells.

The Scholar automatically knows **Blink at level 3** without consuming a known slot. VA0 **MaxVP18**, so its ordinary **10-Spent-VP** cost can be affordable from sufficient Available VP (unlike the Bow Vanguard's Low VP6); actual Reaction/AP/movement restrictions still apply. Veil Inspection at L1 is likewise known and **not** included among the five learned Pillar spells.

## 5. Acceptance and non-acceptance

Run from repository root:

```sh
python -m scripts.b05_high_scholar_fire_l1_l3_v0
python -m unittest discover -s tests -p 'test_b05_high_scholar_fire_l1_l3_v0.py' -v
python -m unittest discover -s tests -v
```

The [fixture](../../scripts/b05_high_scholar_fire_l1_l3_v0.py) derives numeric L1–3 resource/Focus values, uses exact known spell names, records formula order and costs, and checks its F role against the unchanged [Hunter Phase 3 runner](../../scripts/b06_hunter_tactical_diversity_v0.py). The [tests](../../tests/test_b05_high_scholar_fire_l1_l3_v0.py) assert ability/discipline/weapon budgets, equipment accounting, exact-formula authorization, VP affordability, level progression and source-role invariants.

**Verified within this PR only after CI runs:** structural character source-and-ledger consistency. **Not verified or claimed:** complete positional/Opportunity legality in Phase 3, full multi-round combat, accurate modeled spell selection AI, full known magic effects in a live encounter, enough dedicated Fire techniques for a mature Fire-specialist repertoire, complete noncombat acceptance, Hunter CR, or **any of the twelve independently certified Archetype×Focus MVP identities**. The normal 4,096 Phase 3 windows were bounded one-round probes and **must retain their previous numeric results/digest**. Next is genuine High Scholar multi-spell/caster combat and exploration verification, followed by full three-enemy encounter completion with R/F.
