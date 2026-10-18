# B06 — Ordinary Human (Non-Archetype) Template and Soldier Fixture v0

> **PROVISIONAL B06 NPC COMBAT BASELINE — FOR REVIEW; NOT A NEW PLAYER ARCHETYPE OR UNIVERSAL RULE.** This document introduces one reusable `ordinary human, no Veil invocation` benchmark template and [B06-EN-02 equipped soldier](../../content/creatures/b06-ordinary-human-soldier.v0.json), using canonical **physical attack, armor, shield, HP/Vigor, initiative, Turn AP and movement** mechanics. It makes only two explicit, **B06-local** design choices for non-Archetype action/regeneration costs. No existing combat rules are silently modified; these two values remain candidate NPC defaults pending review. The optional `Level 3` rating is **encounter-calibration equivalence**, not a statement that ordinary people possess a player Focus, Archetype or full level progression.

## 1. Why this template exists

**Most humans are ordinary Veil-connected people, not Priests, Scholars, Gifted or Anointed.** Ordinary humans still have body/Ability scores, HP, Vigor, Training, movement, reactions, equipment and physical combat. They **cannot independently invoke Veil techniques**, even if their recorded Veil Affinity/Control modifiers are nonnegative. No VP is tracked as personally Available, Committed or Spent. A future **actually authored** magical item may have its own independent active effect and authorization; possessing gear never grants a personal spellcasting repertoire.

The template is **not** an enforceable cultural identity, personality or universal human combat specialist: farmer, traveler, veteran, smith, aristocrat, scout and ordinary soldier can have different statistics, learned skills, gear and choices. Most ordinary humans need no attack profile at all unless an encounter requires one.

### Universal physical inputs versus two NPC-specific defaults

| Field | Template choice | Rules basis / status |
|---|---|---|
| **Level-equivalent** | Set benchmark rank `L` when testing versus L1–3 characters | Not an NPC character level, XP progression, Challenge Rating or access to level-gated player perks |
| **Abilities** | Supply the actual physical Ability modifiers and ordinary ability checks | Reuse the nine-Ability value convention; no universal player 28-point-buy obligation on NPCs |
| **HP** | `10 + Vitality` | [HP and Vigor](../rules/06-vigor-wounds-death/hp-and-vigor.md); same mortal physical baseline |
| **Vigor** | `(10 + Vitality) × L` | Existing resource formula at the **selected benchmark-equivalent rank**; calibrate against actual encounters |
| **Turn AP** | `min(120, 30 + 6 × (L−1))` | Existing [Turn AP](../rules/05-combat/action-categories-and-physical-tempo.md); does not imply a Focus |
| **Physical Action** | **24 AP** | **NEW PROVISIONAL B06 NON-ARCHETYPE DEFAULT:** reuse the existing *neutral* 24-AP magnitude as a standard mundane action price. This is **not** a claim the canonical General Tempo Action is itself a Physical Action or that High/Medium/Low applies. Review before broader NPC adoption |
| **General Tempo** | 24 AP | Existing universally neutral action class for actions **explicitly** authored to use it; no free actions |
| **Projection Action** | **Not available** (`null` in fixture) | No independently invoked Veil techniques/Universal Inspection/Blink/Focus identity; **VP=0** (not merely an unaffordable 20/24/30 AP spell) |
| **Physical Tempo / normal Guard / Opportunity** | `floor(Turn AP / 24)` | Apply existing derived Tempo and related Guard/Opportunity framework **to the explicitly proposed non-Archetype physical cost** |
| **Natural regeneration throughput** | **`max(Vitality,0) + 0`** | **NEW PROVISIONAL B06 NON-ARCHETYPE DEFAULT:** use the canonical `max(VIT,0)` component and **zero added Focus rate**. This is **not** the High Focus +1 rate. Restore/rebuild only by paying 1 Vigor per point at the real own-turn Regeneration Step |
| **Reactions and movement** | 1 Reaction/round, 12 MP, normal Guard/Dodge/Take Hit and movement/Opportunity | Existing physical systems; no auto-riposte, bonus attack, immunity or talent |
| **Magic item** | Optional only after independently authored item and source/cost rule | An item can provide an effect without turning its wielder into a personal VP-using Veil caster; no magic item in B06-EN-02 |

The template is intentionally **neutral** between the three Focus cadences: granting every ordinary human Low Focus's 20-AP physical speed and +3 regeneration would make non-Archetype soldiers into mechanically superior embodiments by default; granting them High Focus's 30 AP and +1 regen would instead import a Focus they do not have. **24 AP + 0 Focus-rate** is a clear, independently revisable B06 proposal, not an established population-wide metaphysical claim.

## 2. Equipped example — B06-EN-02 Ordinary Human Soldier (L3-equivalent)

| Statistic | Value and derivation |
|---|---|
| **Identity** | Living human, sapient, **no Archetype, Focus, Pillar devotion or invokable techniques** |
| **Abilities** | STR +2, AGI +2, Precision 0, Intellect 0, Awareness +1, Presence 0, Vitality +2, Veil Affinity 0, Veil Control 0. Nine scores happen to cost **28** under character point-buy but the NPC template does not require all humans to obey it |
| **HP / Vigor** | **12 HP / 36 Vigor** from Vitality +2 and benchmark rank 3 |
| **VP and spell actions** | **0 Max VP; 0 Available/Committed/Spent**, Projection Action **unavailable**; no Prepared Veil techniques, Talent spell, Rite, Universal Veil or magical item |
| **Turn AP / action** | **42 AP**, proposed **24 AP per Physical Action**, hence **1 sword attack maximum** in an otherwise purely physical L3-equivalent turn (42−24=18; not enough for another) |
| **Regeneration** | **Throughput 2**, once each true Regeneration Step, paying **1 Vigor per HP or repair progress** and respecting Dying/wound allocation |
| **Equipment** | Brigandine **Armor 5** (95 sp), sword (22 sp), shield (16 sp), pack (8 sp); total **141 sp** from existing mundane item prices |
| **Attack** | **`d20 +6`** from STR2 + AGI2 + One-Handed Swords Training2 |
| **Sword damage** | **`4+d6` raw Piercing HP, Penetration 2**; subtract actual target Armor after Penetration exactly once |
| **Sword Guard** | **16** = 10+STR2+AGI2+Training2; weapon alone normally cannot Guard ordinary arrows |
| **Shield Guard** | **18** = Sword Guard 16 + shield bonus2; the legal held shield may Guard normal projectiles |
| **Guard capacity** | **2 per round** = base Physical Tempo1 + shield1, refreshed at Round Begin |
| **Dodge** | **13** = 10 + min(AGI2, Brigandine cap2) + Awareness1; subtract previous Dodges' nonnegative pressure 2 each |
| **Initiative / Movement / Reaction** | **d20+3**, **12 MP**, **1 Reaction** |

**Only one executable attack profile is defined:** `B06-AT-03` ordinary one-handed sword thrust. The soldier cannot attach a toxin or Conjure Flame, swing with a shield for a bonus attack, use an unspecified special maneuver/weapon refinement, or fire a crossbow without actually holding one and authoring that profile. Its shield grants defensive **capacity and Defense**, not extra offense.

### Damage sanity example against the two audited Life Low Priests

Roll `d6=4`, ordinary non-critical successful sword attack, and apply target Armor:

| Target | Raw Piercing | Effective Armor | Final HP damage |
|---|---:|---:|---:|
| Restorative Vanguard — Leather Armor3 | `3+4+1=8` | `max(3−2,0)=1` | **7 Piercing HP** |
| Preservation Guardian — Brigandine Armor5 | `8` | `max(5−2,0)=3` | **5 Piercing HP** |

These are **post-hit damage arithmetic checks only**: they do **not** bypass actual Attack versus Guard/Dodge/Take Hit, confirmed criticals, Vital Shelter/Interposition, natural Regeneration, reaction opportunities, Dying or other event timing. Defenders must legally establish their Rites/effects and respond at the actual windows; the sheet alone gives no passive shield from magic.

## 3. Reusable ordinary-human modifications

A GM can reuse this NPC template with a different ordinary human occupation: change specific Abilities, trained weapon families, physical armor, equipment, chosen nonmagical tactics and corresponding derived numbers. A civilian may have no weapon Training or armor. A scout might use bow and Dodge but cannot weapon-Guard with a bow. A heavily armored veteran might have different Guard and Vigor, but **no implicit Extra Attack** from the label Veteran.

Any combat *variation* becomes executable only when every derived field, chosen legal equipment, attack cost, Attack/Defense/Armor, effective Training and stat-block source is recomputed. The 150-sp shopping list is a **comparability reference**, not a rule that every NPC owns only 150 sp of gear.

**Outside this narrow B06 candidate:** no claim that every human has 36 Vigor, that ordinary society is split into physical Focuses, or that human cultures have identical combat statistics. The benchmark L3-equivalent pool is a *test calibration choice*, not the universal value for farmers, children, injured people or experienced veterans.

## 4. B06 completion boundaries and next steps

- [x] Add schema-valid [B06-EN-02 standalone fixture](../../content/creatures/b06-ordinary-human-soldier.v0.json), `source_class: mundane_weapon`, actual weapon Attack/Shield Guard, 0 VP and non-projector resources.
- [x] Update the [14-entry initial bestiary](../../content/creatures/b06-initial-bestiary-v0.json) to mark **two** executable test fixtures (Sentry and Soldier), there are **12 still-non-executable entries**; no other design concept is promoted.
- [ ] Codex-review the **24-AP neutral Physical Action and +0 non-Focus regeneration rate** as the intentionally proposed narrow B06 NPC defaults; do not treat them as preexisting canonical Focus values.
- [ ] Complete the first genuinely opposed Level-3 Life Low Priest encounters with source-grounded initiative, defense assignment, Attack rolls, physical damage, actual Regeneration and Vigor ledgers.
- [ ] Develop **B06-EN-03 Hunter of the Woods** using independently authored natural weapons, large-body effects and real TX biological delivery; never automatically copy the human soldier's action or repair defaults onto a beast.

**B06 remains OPEN** and **0/12 Archetype×Focus MVP builds** are independently certified. This document is a [design record](README.md), not a replacement for canonical player rules.
