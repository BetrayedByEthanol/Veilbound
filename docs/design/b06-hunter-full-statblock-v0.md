# B06 — Hunter of the Woods Complete Combat Stat Block v0

> **EXECUTABLE TEST FIXTURE — PROVISIONAL / UNRATED.** [B06-EN-03 full enemy JSON](../../content/creatures/b06-hunter-of-the-woods.v0.json) combines the existing independently authored natural attack, slow venom, footprint, Pounce and physiology rules. It is an **actual schema-bound enemy benchmark** for deterministic source/legality checks, **not** a verified Challenge Rating, playtested fight or generalized nonhuman progression system. The [physiology-only snapshot](../../content/creatures/b06-hunter-physiology.v0.json) remains separately marked **PHYSIOLOGY_ONLY_NOT_EXECUTABLE**; its null `full_enemy_fixture_path` means *that snapshot cannot masquerade as the full enemy*, not that the separately linked full enemy JSON does not exist.

## 1. Final v0 numerical inputs

| Attribute | Hunter B06 v0 | Source / boundary |
|---|---:|---|
| Strength | **+4** | Large predatory musculature, same **+4** already used for Pounce Pressure and Horn Drive; not an added size bonus |
| Agility | **+2** | Merged physiology; mobile four-footed body |
| Precision | **+1** | Creature-local measured cranial horn placement; *not* a global monster or Horn accuracy rule |
| Intelligence | **−2** | Non-sapient animal cognition anchor; does not force behavior or guaranteed lack of learning |
| Awareness | **+2** | Merged physiology; no free scent stealth/tracking bonus |
| Presence | **−1** | Social/motivational test input; horn threats do not automatically cause fear |
| Vitality | **+4** | Merged physiology: HP14, throughput4 |
| Veil Affinity / Control | **0 / 0** | Explicit inert ability values for the 9-field schema; **no independent Veil invocation or personal VP** |

The non-physiology values are **Hunter-local candidate stats**, not legal level-3 human point-buy, proof that animal intelligence is universally −2, or a proposed new ability scale. The Hunter has no Archetype, Focus, named Pillar, learned natural-weapon Training or inherited Talents.

| Combat value | Current B06 v0 | Derivation |
|---|---:|---|
| Benchmark rank | **3-equivalent** | Comparison anchor for Vigor/Turn AP, **not actual level, CR or XP** |
| HP / Vigor | **14 / 42** | `10+Vitality4`; `14×rank3` |
| Natural Armor | **3** | Fixed uniform hide/dermis across one shared creature, no worn Dodge cap or per-cell pool |
| First Dodge / Dodge series | **14; then 12, 10, 8…** | `10 + Agility2 + Awareness2 − Dodge Pressure`; reset pressure at Round Begin |
| Initiative | **d20+4** | `Agility2 + Awareness2`, no innate surprise or hunting bonus |
| Turn AP / Physical Action | **42 / 24** | `30 + 6×(3−1)`; **creature-local non-Focus Physical24** retained |
| Physical Tempo / Opportunity | **1 / 1** | `floor(42/24)=1`; independent normal Opportunity round capacity |
| Guard capacity / usable Guard | **1 / none** | Base tempo capacity exists, but **no legal natural Guard instrument**, so cannot choose Guard |
| Reaction | **1 per round** | Standard Reaction resource; no automatic reaction-only counterattack |
| Normal movement | **12 MP** | Whole 1×2 body translation/pivot, ordinary 2/3 MP costs plus terrain |
| Pounce extended M / cutoff | **24 / 18 MP** | `2M` and `floor(3M/2)` without prior MP spending/reservation |
| Natural regeneration | **4 per actual own-turn Step** | `max(VIT4,0)+local non-Focus0`, 1 Vigor per restored HP/Repair Progress |
| Vigor Recovery | **11 every completed 6h** | 25%×42=10.5, round half up; cap42 |
| Personal VP / Projection | **0 / none** | Non-Archetype animal has no self-invoked Veil modes |

**Footprint:** one straight contiguous **1×2** rigid body with permanent local cells `head` (reference) and `rear`, irrespective of pivots. The entire body must fit and pay translated terrain costs; head/rear never supply independent HP, armor, attack opportunities, extra Reactions or separate initiative.

## 2. Source-derived natural attacks and resolution data

The existing [Hunter Bite, pursuit toxin and Horn Bash/Drive v0](../rules/05-combat/hunter-bite-venom-and-horn-v0.md) and [Hunter Pounce v0](../rules/05-combat/hunter-pounce-and-prey-takedown-v0.md) already define the attack/contest procedure. The present fixture **decomposes the existing fixed totals** without buffing them. Because these are **source-authored natural weapon damage packages**, `strength_contribution="none"` in the schema means *the complete physical contribution is already included in the printed local base*, not that the Hunter is weak. **Do not add STR+4 again to damage**.

| Mode | One committed action | Derived accuracy / pressure | Packet and consequences |
|---|---|---|---|
| **B06-AT-04 — normal Bite** | 24 AP; facing head-forward adjacent one-square PC | `d20+STR4+AGI2+natural Training0=d20+6` | **3+d6 Piercing Pen1**; real surviving puncture gates **one** slow venom exposure |
| **B06-AT-05 — Horn Bash** | 24 AP; frontal adjacent one-square PC | `d20+STR4+Precision1+Training0=d20+5` | **2+d6 Crush Pen0**; no free Shove, toxin, fear, additional attack or natural Guard |
| **B06-AT-06 — Pounce** | 24 AP **total** as a scoped Charge/Bite action with precommitted head-forward route | **one** Bite `d20+6`, then conditionally **independent pressure `d20+STR4+specific Training0=d20+4`** | One Bite **3+d6 Piercing Pen1** and possible venom, *then* one free eligible Balance contest; strict Pressure win→**Prone in place**, otherwise remains standing; no second attack |
| **B06-AT-07 — Horn Drive** | 24 AP **instead of** Horn Bash; canonical Shove Close-Contact Opportunity applies | **no attack roll**, `d20+STR4=d20+4` Shove vs defender `d20+Strength+specific Training+2 Hold Ground+Anchoring` | **No damage packet**; strict contest win plus legal destination displaces one-square PC straight forward 1 square and advances **whole rigid 1×2** Hunter 1 square; otherwise no move |

**Why these Ability pairings?** Natural weapons have **no published universal weapon attack Ability pairing**. This fixture authors **Hunter-only** Bite as Strength+Agility (closing, jaw placement) and Horn Bash as Strength+Precision (pointing and driving a single frontal horn). These are decomposition choices for *already-existing* +6 and +5 totals; they are not retroactive generic sword/mace/Bite/Horn rules. Narrow natural weapon Training is **0**, and situational bonuses are **0**, until real effects (e.g., Shove's Close-Contact Opportunity −2) actually apply.

The schema's optional `linked_contest` contains the Pounce **force check after its one Bite attack**, or Horn Drive's **ordinary Shove contest with no attack roll/HP packet**, including authoritative resolution links and zero *additional* AP cost. **Both Hunter-local contest kinds bind the baseline pressure to `attacker_modifier=4 + training_modifier=0 + other_modifier=0 = total_pressure_bonus=4` at the schema level.** The printed `total_pressure_bonus` is the authored *baseline*, not the dynamic post-response roll result: independently legal situation modifiers (such as the −2 canonical Close-Contact Opportunity penalty on Horn Drive) still apply when their trigger occurs. JSON Schema Draft 2020-12 does not provide generic cross-field addition; a different future creature or variable contest contribution needs separately authored validation rather than arbitrary integers. Its **kind-discriminated Draft 2020-12 conditions** also bind Pounce to the named grooved-canine natural Bite source, Strength+Agility attack roll, real Piercing packet and canine toxin origin; Horn Drive is bound to the named frontal-horn/shoulder source with no attack roll, damage packet or toxin. The source descriptors are exact **B06-v0 contracts**, not a universal natural-weapon template; a future redesign must update fixture, authority and schema together. **The overall 24 AP cost is still paid once**. Normal Bite/Horn Bash have no linked contest. An attack mode isn't a separate simultaneous strike or another action in the same Attack Sequence simply because it has its own fixture record.

## 3. Time-order / eligibility boundaries

**Pounce:** declare linked Bite+force before movement; head already facing cardinal heading, begin with no MP used/reserved, translate at least three real legal whole-body squares and satisfy the strict front-adjacent one-square standing-PC condition. Extended Pounce budget replaces ordinary MP (`24`, not +24). Pay 24 AP at Charge commitment/cutoff or before attack. Defenses/Interceptions/Reactions occur during the **one Bite** response window. After damage/real HP prevention, evaluate puncture and at most one toxin resistance **before** the independent balance rider. If target moved or action interrupted, neither roll happens. If Bite misses/Guard stops it but frontal force contact remains, the rider can still roll. If Bite incapacitated an otherwise-standing target, use Trip's *unable-to-contest* result only when still physically legal; no second balance roll or extra Bite.

**Venom:** the source is **B06-SRC-HUNTER-GROOVED-CANINES** with paired venomous saliva grooves, not Horn, Fire or impact. Only actual positive remaining Piercing HP after armor and any event-wide prevention (or independently established breached route) permits one new toxin application. An already active equal/lower-grade instance rejects re-exposure without another resistance roll. An eligible new instance gets one **DC12 Vitality** check: **Full** after failure or **Reduced** after success (tie with DC succeeds). **No immediate poison penalty.** Full has T+10m slow stage, T+30m deeper nonstacking replacement stage, T+120m expiry; Reduced has only T+10m stage and T+60m expiry. Apply Venom Endurance and other actually-authored prevention/suppression on their own timing; no free antidote or instant kill.

**Horn Drive:** choosing the alternative prevents Horn Bash damage that action. The target can make a normal **Close-Contact Opportunity** when eligible; if it hits, Shove takes −2 Pressure, and later invalidating incapacitation may end Drive. Defender has +2 Hold Ground. On strict win, force displacement only with a clear target destination and a **legal whole-footprint advance**; do not move either participant when physically blocked. No automatic Prone, Crush packet, Grapple or poison.

**Other reactions:** the Hunter has one Reaction like any creature, not a species special. A legal frontal normal Bite or Horn Bash may be an ordinary Opportunity Attack (round capacity1). Horn Drive is **not an Opportunity Attack substitution**. No preemptive Bite, counterpounce or free horn parry.

## 4. Repeatable sanity cases

| ID | Fixture-driven event | Deterministic result |
|---|---|---|
| HFS-01 | Stats STR4/AGI2/PRECI1/AWA2 | Bite+6, Horn+5, Pounce+4, Drive+4, Initiative+4 |
| HFS-02 | 42 Turn AP, Physical24 | One paid Physical Action; 18 AP remain; no second 24-AP action; Tempo1 and one Opportunity budget |
| HFS-03 | First→fourth Dodge in same round | 14, 12, 10, 8; no Guard despite latent capacity1 |
| HFS-04 | Bite d6=4 versus Armor5 | `3+4−max(5−1,0)=3` Piercing HP and one puncture-eligible toxin application if not prevented |
| HFS-05 | Bite d6=1 versus Armor5 | `3+1−4=0`: no injection, no resistance; successful force-only Pounce may still knock down |
| HFS-06 | Horn Bash d6=4 versus Armor5 | `2+4−5=1` Crush HP; no shove or injection |
| HFS-07 | Pounce balance Hunter d20=9 / defender d20=12+Strength3 | Hunter13, defender15: remains standing despite independently successful Bite |
| HFS-08 | Drive attacker d20=13, defender d20=8+STR2+Hold Ground2 | Hunter17, defender12: target displaced forward1 and Hunter whole body advances only with full legal clear path |
| HFS-09 | Soldier raw sword `4+d6` with d6=4, Pen2 hits Hunter Armor3 | Hunter takes 7 HP once (14→7); next actual own-turn Step can repair 4 HP for 4 Vigor |
| HFS-10 | Hunter Turn 12 MP, legal unobstructed Pounce no impairment | 2M=24; threshold18; ≥3 completed translated steps, head-forward; no extra pivot |
| HFS-11 | Venom accepted at T0, failed DC12; later re-Bite while instance active | Do not re-roll DC or refresh onset; stage T+10, replacement T+30, expiry T+120 |
| HFS-12 | No enemy Guard instrument, full HP, 42 Vigor | Natural Guard illegal; no free HP regen, no more than 42 Vigor after 11-point six-hour Recovery |

## 5. Validation, promotion and unresolved gates

This version **promotes only** the Hunter's [14-entry design-index](../../content/creatures/b06-initial-bestiary-v0.json) metadata from `CONCEPT_ONLY` to `EXECUTABLE_FIXTURE_EXISTS`, with a real [`b06-enemy-v0` test fixture](../../content/creatures/b06-hunter-of-the-woods.v0.json). It adds no new natural weapon power or size/mass bonus. The detached physiology-only record remains a validated schema-backed partial calibration source and **is not itself** an executable enemy.

Use both **Draft 2020-12 JSON Schema** and the required **semantic footprint validator**, plus the new fixture regression checks. A schema-valid record alone cannot prove that combat balance is satisfactory.

**Still open:** zero accepted **B06-1/B06-2/B06-3 real opposed full encounter packs**, no repeated-seed outcome statistics, no observed Challenge Rating/XP/TP equivalence, no size/mass treatment for larger prey or mass-based damage, no numerical scent/perception abilities, no tested player options for disengagement/venom therapy, no automatic hostility. Planned forest encounters remain **untested** regardless of the elite-ambush ecological role.

This is an encounter-test-ready **combatant fixture**, not a completed MVP Challenge/Observe acceptance gate.