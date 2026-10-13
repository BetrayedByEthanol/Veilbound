# Veil Inspection v0 — Held-Item Examination

> **LOCKED B05 basic Inspection design; numerical +2 and 2 VP remain playtest calibration values.** This is the first executable **Universal Veil Inspection** operation. It reads **observable magical patterns on one item held by the caster**, independently of Pillar/Aspect access. It does **not** replace the separately deferred **Veil Analysis** procedure for subtle, dormant or concealed effects. See [Universal Veil Fundamentals](universal-veil-fundamentals.md), [Core Resolution](../01-core-resolution/core-resolution.md) and [Volition Points](volition-points.md). **Universal procedure acquisition and technique-tier mapping remain deferred**: being eligible to learn Universal magic is not automatic knowledge of every operation.

## Profile

| Property | Veil Inspection v0 |
|---|---|
| Family | Universal Veil — Inspection |
| Operation | Basic held-item examination, **not** Veil Analysis |
| Action | **One Full Action** on the caster's own turn; **not** a Reaction or freely reservable Interception |
| VP cost | **Base 2 Spent VP**, paid only when the examination completes; use independently applicable VP-cost reductions |
| Range / eligible subject | **Touch — one item physically held in the caster's hand throughout the Full Action** |
| Gloves | Ordinary gloves are allowed; a bare skin-to-item interface is not required |
| Baseline check | **None** to perceive actually observable magical patterns or discernible Pillar/Aspect signatures |
| Optional interpretation | **+2 situational modifier to one relevant Veil Theory check performed as part of this completed examination** |
| Result | Observation and limited interpretation only; no spell activation, dispelling, control, automatic ability disclosure, ward bypass or material alteration |
| Duration | Examination resolves once; acquired information persists normally as knowledge, not as a sustained magical sensor |
| Required Training | **None** for basic observation; relevant actual Veil Theory expertise applies only to its corresponding interpretation check |

A **Full Action** consumes the caster's full remaining Turn AP allotment under [Turn AP and Tempo](../05-combat/action-categories-and-physical-tempo.md). It is not a promise of an uninterrupted full combat round and does not by itself spend the character's Reaction or all ordinary MP. The caster **must hold and continue examining the same item throughout**, so they cannot switch subjects mid-action or claim an examination of an item they are no longer holding.

## Held-item boundary

- Inspect **exactly one physically grasped item** per completed operation, such as a sword, ring, book, amulet or portable instrument. Simply seeing it, knowing its location, holding a container with inaccessible contents, or being in the same room does not suffice.
- A **worn item** is eligible only if the caster genuinely **takes that item in hand** during the examination; wearing equipment without grasping it is not the authored held-item procedure.
- A permanently installed structure, room, building, large device that cannot meaningfully be **held**, loose environmental effect, or another creature is **not** an eligible subject of Basic Inspection. A future more advanced or different Universal procedure may examine those without granting that capability here.
- **Ordinary gloves** do not block this contact. If a separate rule expressly interferes with magic conducted through gloves, apply that separately; no generic bare-skin requirement is invented.
- An item held by an **unwilling creature** or otherwise protected as an attended item cannot be magically probed without any separately required possession, consent, protection or contest. Merely touching a victim's equipment or briefly grabbing a weapon does not bypass [Universal Veil protections](universal-veil-fundamentals.md#universal-spell--ritual-authoring-boundary) or authorize involuntary disarming, dismantling or reading a protected living subject.
- A single complicated artifact remains one item if physically coherent; one examination does not automatically grant access to every sealed internal component, unrelated contents or independently concealed secondary enchantment.

## Basic information depth — automatic when observable

On **completion**, reveal what the accessible item's magic **actually presents as an observable Veil pattern**, without requiring a detection roll. The examination can return:

1. **Presence:** whether at least one **observable magical pattern** exists on/in the accessible item.
2. **Pillar identity:** the recognizable **Pillar signature(s)** represented by those observable patterns, when a signature is actually discernible.
3. **Aspect identity:** the recognizable **Aspect signature(s)** associated with those patterns, when actually discernible. Identifying a Pillar does not guarantee that its precise Aspect is readable.
4. **Multiplicity:** if multiple **observable, distinguishable** signatures coexist, report those observations rather than pretending the item has only one Pillar or Aspect.

An effect may instead be **Universal**, unattributed, unfamiliar, obscured, damaged or otherwise unreadable. In that case report the **actual observation and uncertainty**, not a guessed Pillar/Aspect. **Pillar/Aspect signatures describe the item's magical pattern**, never its bearer's beliefs, allegiance, morality or intent.

**No-observation result:** if nothing magical is observable to Basic Inspection, the report is **“No observable magical pattern detected.”** It is **not** a guarantee that the item is nonmagical. A dormant, concealed, suppressed, subtly embedded or protected effect can remain undiscovered; Inspection does not make every latent pattern visible merely by naming the item.

**No automatic function identification:** observing, for example, a recognizable Aspect pattern on a blade does **not** automatically reveal its activation words, damage values, duration, precise enchantment function, curse, power source, hidden mechanism, construction formula, or every possible effect. The reader gets the magical **identity that is observable**, not a complete ability card. Obvious context remains useful as ordinary information but does not override concealment.

## Veil Theory — one bounded +2 interpretation check

After the basic observation, the caster may attempt **one legitimate, relevant theoretical interpretation check** as part of that **same completed Full Action**, provided the available evidence makes a meaningful question answerable. Usually:

```text
d20 + Intellect + actually applicable Veil Theory Training
    + 2 Inspection situational modifier + other legal modifiers
vs
10 + task Difficulty Modifier
```

- The **+2** applies **once** to that **specific** Veil Theory check about **patterns actually observed on that item during this examination**, not to the automatic baseline detection. It is a **situational modifier, not +2 Training**, +2 Veil Control, a Pillar Lore replacement, or an improvement to Direct Veil Pressure.
- If no theoretical check is relevant or no interpretable magical evidence exists, there is **no bonus to carry forward** or grant to another subject; the player still receives the automatic baseline observation.
- The caster **does not need directly invested Veil Theory** to use Basic Inspection. A Veil Theory check, if allowed with untrained rank **+0**, can still receive the +2 when the theoretical question is genuinely relevant. Ordinary training restrictions and GM difficulty selection apply as usual.
- The +2 is attached to the same check if an independently permitted **reroll** applies, such as [TAL-U01 — Veil Insight](../10-advancement/talents-level-1-5-v0.md#tal-u01--veil-insight); it does not authorize extra checks, extra rerolls, or an additional Full Action worth of information.
- Repeatedly casting Inspection on an **unchanged** item with **no new evidence or changed circumstances** reveals the same baseline information and does **not** automatically grant unlimited fresh rolls at an interpretation question already attempted. Follow [Core Resolution](../01-core-resolution/core-resolution.md) for when repeat attempts, safe-time work, Take 10 or Take 20 are appropriate. A failed interpretation roll does **not** erase the separately granted basic observation.
- This check is **not** a hidden-enchantment detection contest; a high result cannot reveal evidence excluded from the basic readout. Detection of a concealed underlying effect belongs to **Veil Analysis**.

## VP and resolution timing

Basic Inspection is an **authored Universal Veil procedure**, so an independently applicable Talent modifier can change its **base 2 Spent VP** cost. In particular, [TAL-M03 — Frugal Technique](../10-advancement/talents-level-1-5-v0.md#tal-m03--frugal-technique) can reduce one eligible own-turn Inspection from **2 to 1 Spent VP**, if its **once-per-own-turn** use is unspent. Restrictions on other modifiers and minimum costs continue to apply; no Pillar-specific preparation is fabricated.

1. **Declare one eligible held item**, the intention to use Basic Inspection, and any **eligible VP-cost modifiers**. Calculate and lock the **effective Spent VP cost** and confirm that at least that much **Available VP** exists **before committing** the Full Action AP. A character with only 1 Available VP may legally use an eligible unused Frugal Technique to cast Inspection for **1 VP**; without a discount, they cannot declare it.
2. **Commit the Full Action AP**, which requires the caster's full normal Turn AP allotment still be unspent. If a once-per-turn Talent cost discount was chosen, its use is committed **at declaration**, even if the Inspection ultimately fails.
3. Resolve any authorized **Interceptions, interruptions or other response windows**. When the operation would complete, recheck **continuous legal hand-held access to the item** and that the locked effective VP cost can still be paid. If the action is cancelled, contact lost, the subject becomes ineligible, or available VP falls below the effective cost, the attempt **fails**, yielding **no Inspection information and spending 0 VP**; the previously committed Full Action AP is **not refunded**.
4. **On a legally completed examination, spend the locked effective VP cost**, **even if no observable magical pattern exists**. Resolve its guaranteed observable report and at most one eligible **Veil Theory interpretation check** with +2 during that Full Action. An interpretation failure does not refund VP or the action and never revokes the automatic observation.

Inspection doesn't establish a sustained magical effect, add a recurring per-round detect-magic aura, or generate a new free opportunity to inspect another item as movement continues.

## Veil Analysis — separate, **not yet executable**

**Veil Analysis** is a **distinct, more demanding Universal examination procedure**, not an optional extra roll automatically bundled into the 2-VP Basic Inspection. Its role is to investigate:

- dormant, faint, subtle, suppressed, deliberately disguised or actively **concealed** effects that Basic Inspection might miss;
- the **functions and operating principles** of a detected but incompletely understood enchantment;
- complex, damaged, multiple, unfamiliar or contested patterns and potentially **hidden curses**.

Analysis should eventually distinguish **detecting that a hidden pattern exists** from **reconstructing how it works**; sufficiently skilled investigators may be able to do both **if its authored checks and protections permit**. Its **action/time, VP, tier/learning requirements, equipment, difficulty, concealment/resistance procedure, information bands, false/partial results and failure costs are DEFERRED**. This page gives **no automatic concealed-magic detection**, no numerical concealment threshold, and no permission to bypass item/creature protections.

## Regression cases

| Case | Basic Inspection v0 result |
|---|---|
| Held sword has a clearly observable Pillar/Aspect pattern | Full Action + effective VP; reveal observable magical presence and discernible Pillar/Aspect; no automatic enchantment stats |
| Held ring has two openly distinguishable signatures | Identify both as appropriate; not a generic “one signature only” rule |
| Held object has only dormant or concealed magic that is not observable | “No observable magical pattern detected”; **not** certified nonmagical |
| Item has readable Pillar pattern but no discernible Aspect | Report Pillar, acknowledge Aspect unresolved; do not guess |
| Item contains a generic Universal pattern | Report it as such if observable, without inventing a Pillar |
| Held item is mundane | Completed Inspection spends effective VP and returns “No observable magical pattern detected” |
| Item is visible on a table, not in the caster's hand | Ineligible; cannot begin a legal Inspection |
| Item is held through ordinary gloves | Eligible; bare skin unnecessary |
| Caster has 2 Available VP, no modifier | May complete basic Inspection for **2 Spent VP** |
| Caster has 1 Available VP and unused TAL-M03 during their own turn | Can declare discounted Inspection for **1 Spent VP** |
| Item is taken away by an Interception before the examination completes | Full Action remains spent; **0 VP**, no Inspection information |
| Item's visible pattern raises a legitimate theoretical question | **+2 to one relevant Veil Theory check**, as part of this completed Full Action |
| Caster repeats Inspection with no new evidence after an interpretation failure | Same basic observation; no automatic bonus reroll or fresh interpretation roll |
| Artifact has a deliberately concealed secondary effect | Basic Inspection does not force disclosure; Veil Analysis remains separately unauthored |

## Status

**LOCKED B05 basic Inspection design:** one physically held item; ordinary gloves allowed; **Full Action**, **base 2 VP**, only paid on completion (effective cost honors legal Talent discounts); basic observation of magical presence and discernible **Pillar/Aspect signatures** without a roll; bounded **+2 to one relevant Veil Theory interpretation check in the same Full Action**; **no** automatic concealed effects, curse functionality or all-item identification; Veil Analysis separate and deferred.

**STILL DEFERRED:** formal Universal procedure acquisition/tier; Veil Analysis profile including concealment mechanics; examining larger structures, non-held objects, remote magic and beings; magical item/enchantment system and creation/economy. These are not silently granted by Basic Inspection.
