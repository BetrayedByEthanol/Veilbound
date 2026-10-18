# B06 — Hunter of the Woods Physiology and Defense v0

> **HUNTER-LOCAL PHYSIOLOGY LOCK CANDIDATE / CALIBRATION BASELINE.** This is **step 1** toward the complete B06-EN-03 executable enemy. It authors the Hunter's HP, natural Armor, Dodge, Vigor and regeneration from already defined Veilbound procedures, with independently stated biological ability anchors and one narrow non-Focus mapping. These **initial numbers remain provisional for opposed encounter calibration**; this document does **not** certify difficulty, promote a complete enemy fixture or change global NPC, natural-armor, size, or level rules. The 14-entry bestiary retains **B06-EN-03 CONCEPT_ONLY** and a null executable fixture path until the remaining attack/ability-resource integration is reviewed.

## 1. Anatomy and permitted source

The Hunter is one **living, corporeal, animal-like, non-Archetype** forest quadruped, bulkier than a bear, occupying a **rigid 1×2 footprint** with stable anatomical cell IDs **head** (reference cell) and **rear**. Its dense hide and dermis are the **creature-local natural Armor source**, not worn Leather, an equipment stack, a magic effect, a detachable shield or an armored horn that can Guard. Muscularity and body length **do not themselves multiply HP, Vigor, Armor, attack damage, Guard opportunities or regeneration**. A strike or area that affects both occupied cells still targets one creature, with one shared HP/Vigor state and normal packet processing; a hit on a particular body cell remains associated with that stable anatomical cell through movement.

This authoring deliberately uses the existing [HP and Vigor](../rules/06-vigor-wounds-death/hp-and-vigor.md), [defensive response and Dodge Pressure](../rules/05-combat/defensive-responses-and-criticals.md), [weapons and Armor](../rules/05-combat/weapons-and-armor.md), and [footprint](../rules/05-combat/multi-square-creature-footprints-v0.md) procedures without assuming that every animal or nonhuman must share the exact numbers below.

## 2. Numeric physiology profile

| Quantity | B06-EN-03 v0 | Derivation and status |
|---|---:|---|
| **Vitality** | **+4** | Creature-local robust-body candidate; affects HP, Vigor and base regen |
| **Agility** | **+2** | Creature-local agility input; no new size/facing defense modifier |
| **Awareness** | **+2** | Creature-local alertness input; no automatic special scent/ambush check |
| **Max HP** | **14** | **10 + Vitality4**; does **not** also scale with size or benchmark level |
| **Natural Armor** | **3** | One uniform hide/dermis Armor rating; no stacked equipment bonus or extra coverage-specific head/rear rating |
| **Dodge Agility cap** | **None** | The thick hide is not a worn armor set imposing an equipment-based positive-Agility cap |
| **Dodge Defense (first Dodge)** | **14** | **10 + Agility2 + Awareness2 − Dodge Pressure0** |
| **Dodge Pressure** | **0 / 2 / 4 / 6 ...** | First through fourth chosen Dodge: defenses **14 / 12 / 10 / 8**; reset at Round Begin |
| **Legal Guard instrument / base capacity** | **None / 1 (currently unusable)** | Provisional **42 AP / Physical24** means **Physical Tempo1** and **one base Guard capacity**, but no horn, jaw, claw or shield is an authored Guard instrument; without a legal instrument choose Dodge or Take Hit |
| **Benchmark rank** | **3-equivalent** | Explicit **B06-local Vigor comparison anchor**, not actual PC Level, numerical CR, XP value or party difficulty |
| **Max Vigor** | **42** | **(10 + Vitality4) × benchmark rank3 = 14 × 3** |
| **Non-Focus regen contribution** | **+0** | Same narrow B06 non-Focus modeling choice as the ordinary soldier, **not** a new universal animal Focus Rate |
| **Natural Regeneration throughput** | **4** | **max(Vitality4, 0) + 0 = 4** at its **one real own-turn Regeneration Step** |
| **HP/Repair Progress conversion** | **1 Vigor per 1 point** | Existing non-Dying allocation and Dying rules; no free healing outside real entitlement |
| **Vigor Recovery every completed 6 hours** | **11** | **round-half-up(0.25 × 42) = round-half-up(10.5) = 11**, capped at Max Vigor42 |
| **Personal VP / Projection** | **0 / none** | No Priest/Scholar/Gifted/Anointed spellcasting or personally invoked Veil powers from an ordinary Veil-connected animal |

**Role of the rank:** It is only a fixture-calibration input for the existing Vigor formula. Do not infer a character-level XP award, monster CR or size-driven universal Level3 animal scaling. The choice of **Vitality4, Agility2, Awareness2, natural Armor3 and rank3** is deliberately an **encounter-test hypothesis**; the derived arithmetic and defense behavior are currently executable, but actual values may be recalibrated after measured opposed fights.

**Normal attacks and physical statistics remain separate:** The already-authored [Bite, venom and Horn Bash/Drive](../rules/05-combat/hunter-bite-venom-and-horn-v0.md) and [Pounce](../rules/05-combat/hunter-pounce-and-prey-takedown-v0.md) retain provisional local **d20+6 Bite, d20+5 Horn**, **24 AP Physical**, **M12**, **42 Turn AP**, and **+4 Pounce Pressure** samples. This physiology slice does **not** automatically finalize Strength, assign weapon Training, decompose natural attack totals, award a free Horn Guard, or turn those independent local profiles into a complete schema-valid enemy.

## 3. Defense, regeneration and wound sequencing

1. **Defenses are chosen normally:** An aware, physically capable Hunter may choose Dodge (14 initially, Dodge Pressure −2 per prior chosen Dodge this round) or Take Hit. **Guard is unavailable despite the derived Physical Tempo1/base capacity1** until a separate actual Guard-capable natural instrument and its limitations are explicitly authored; the horn is **not** such an instrument. Neither armor nor footprint grants a Reaction, an extra defense assignment, a second Guard budget or extra Dodge.
2. **Natural Armor applies once to HP injury:** For an actual Piercing/Crush/Cut hit, use **effective Armor = max(3 − attack Penetration, 0)** and existing ordinary damage rules. No automatic resistance to Fire, Veil damage, direct Vigor packets, toxins or critical injury. As with other armor, damage and Penetration belong to the real packet and source, not to the number of occupied cells.
3. **Regeneration is never immediate upon taking injury:** The **one actual own-turn Regeneration Step** precedes that turn's ordinary start-of-turn hazards. With 42 Vigor and throughput4, at most **4** HP/Repair Progress points can be restored **if actually missing and legally repairable**, spending exactly the corresponding Vigor. A non-Dying NPC's controlling GM allocates the available throughput between HP and genuine Repair Progress as the same non-Dying allocation rule allows; the choice cannot invent repair progress for an unwounded creature. Wounds and any Dying restrictions take precedence over a normal non-Dying allocation.
4. **No stamina subsystem:** Pounce, Charge, running, tracking prey, retreating, resting a minute, or reaching a den do not themselves cost, regenerate or refresh Vigor. The independently authored **completed six-hour** Vigor Recovery (11, capped at 42) may occur in exploration on its existing clock; **general exploration-time natural HP regeneration is not authored** by this record.
5. **Incapacitation matters:** At HP0 or below, use existing actual Dying, wound and incapable-of-active-defense rules. High Vigor does **not** block HP injury, prevent 0-HP crossing or grant an automatic Dodge/Guard when unconscious. Natural horn mass, thick hide and the creature's 1×2 geometry do not negate wound or critical triggers.

## 4. Bounded reproducible cases

| ID | Setup | Required outcome |
|---|---|---|
| HPH-01 | Fresh Hunter VIT+4 / benchmark3 | **HP14**, **Vigor42**, **throughput4**, six-hour **Vigor Recovery11** |
| HPH-02 | Capless natural Armor3, AGI+2 / AWA+2 | First four Dodges **14,12,10,8**. No special size penalty, no per-cell extra Dodge |
| HPH-03 | Soldier sword ordinary hit, raw **4+d6** with d6=4, **Pen2** | Raw Piercing8, effective Armor **max(3−2,0)=1**, Hunter suffers **7 HP** once (HP14→7), not 7 per footprint cell |
| HPH-04 | HPH-03 followed by the Hunter's **next real own-turn Regeneration Step**, still not Dying | Restore **4 HP** (HP7→11), consume **4 Vigor** (42→38); the attack itself provided no extra regeneration |
| HPH-05 | Full health Hunter with only 1 missing HP or Vigor0 | Never restore more than missing HP or spend unavailable Vigor; no negative Vigor, free 4-point heal or virtual turn |
| HPH-06 | Six hours elapse from Vigor38, no independent other effects | Recover **11 Vigor** to the **cap42**, not 49; no corresponding free HP repair or time-reset from prior Pounce |
| HPH-07 | Natural Bite/Horn are still its only authored physical weapons | **No usable Guard** from either (one unused base capacity), no additional attack from two occupied squares and no intrinsic Venom immunity |
| HPH-08 | Hunter takes HP14→0 at a qualified first positive-to-nonpositive crossing | Existing Dying/wound rules apply; the Hunter cannot perform ordinary active Dodge or ordinary non-Dying regeneration allocation while incapacitated |

These are **arithmetic and sequencing** checks, not a stochastic fight, validated CR or finalized difficulty.

## 5. Next executable fixture gate (not part of physiology lock)

After this source is reviewed, the [B06-EN-03 full enemy record](../../schemas/b06-enemy-benchmark-v0.schema.json) still requires coherent **Strength and natural attack contribution decomposition, Initiative, Action/Reaction capacity, source-backed Bite/venom/Horn attack entries, Pounce/Drive mode authoring, concrete start states and legal tactics**, and a complete schema/ID validation pass. At that stage promote the index's **CONCEPT_ONLY** and null fixture path only when a **real executable file** exists. Preserve the one-square-PC Pounce boundary and unrated CR until encounter review. No interim text field, concept source or physiology-only test should masquerade as full B06 enemy execution.