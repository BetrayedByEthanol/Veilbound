# Talents — Level 1–5 MVP Catalogue v0

> **32 individually selectable PROVISIONAL PLAYTEST Talents.** These are *not* yet a locked balance calibration. Minimum level and numerical values may be revised after testing. Use the shared [Talent Framework](talents-framework-v0.md) for acquisition, timing, stacking, terminology and the deferred-content boundary. No magical item crafting, potion manufacture or permanent enchantment Talents are included.

## Catalogue overview

| Category | Level 1 | Level 3 | Level 5 | Total |
|---|---:|---:|---:|---:|
| Combat / physical | 6 | 5 | 3 | **14** |
| Magical tactics / spellcasting | 2 | 1 | 2 | **5** |
| Archetype-specific | 4 | 0 | 4 | **8** |
| Knowledge / exploration / practical utility | 4 | 0 | 1 | **5** |
| **Total** | **16** | **6** | **10** | **32** |

**Key:** `L` = minimum *character* level; `Once/round` refreshes at Round Begin; `Once/turn` applies to the character's own turn; `Once/6h` refreshes after each completed 6-hour period. Entries are **one-time purchases** and cannot be stacked with themselves. **A published, usable underlying spell, Signature, action or Training is required** wherever the entry specifically says so; these records do not author missing techniques.

## Combat and physical — 14

### TAL-C01 — Combat Awareness
**L 1 · Any Archetype/Focus · Passive · Mundane.** Add **+2 explicit Initiative modifier** to the existing `d20 + Agility + Awareness + modifiers` roll. No bonus to ordinary Awareness, Dodge, tracking, surprise, or other checks. Requires no AP, Reaction or VP.

### TAL-C02 — Enhanced Regeneration
**L 1 · Any · Passive · Veil-assisted.** Increase the character's **once-per-turn regeneration throughput by +1**. Apply in the existing Regeneration Step (including Dying procedure where legally usable), spending **1 Vigor for each HP restored or point of wound Repair Progress**. Does not add Max HP, Vigor, a second step, recover irreparable wounds, bypass suppression, or permit extra spontaneous healing.

### TAL-C03 — Surefooted Step
**L 1 · Any · Passive · Mundane.** **Once on the character's own turn**, one otherwise legal **Normal diagonal grid step** costs **2 MP instead of 3 MP**. Flat terrain/occupancy costs remain; this does not apply to Cautious Movement, a fixed-heading Rapid Advance/Charge/Sprint, reserved Movement Interception, or forced movement. It cannot cross blocked corners or occupied enemies.

### TAL-C04 — Mobile Sight
**L 1 · Any · Passive · Mundane · Aiming.** **Once per established Aim preparation**, the shooter may deliberately change their firing position by **one legal voluntary Normal movement step** without that step alone breaking [Aim](../05-combat/aim-v0.md#duration-consumption-and-breaking-aim), provided the original target remains meaningfully tracked and the locked attack profile/objective remain usable. Pay normal MP and any Movement Opportunities; moving farther, losing the target, changing profile/objective, being displaced, or other Aim-breaking events still break it. No extra Aim, attack, mitigation or AP is generated.

### TAL-C05 — Guard Reserve
**L 1 · Any · Passive · Mundane.** At **Round Begin**, increase the character's **normal Guard capacity by +1** beyond derived Physical Tempo. This is a Talent modifier, separate from and compatible with the **at-most-one equipment Guard-capacity bonus** allowed by defensive off-hand/shield rules. Guard legality, projectile restrictions and Guard Defense are unchanged; no additional Reaction or Guard action is granted.

### TAL-C06 — Secure Grip
**L 1 · Any · Passive · Mundane.** **Once per round**, when the character is the **holding defender** in a legitimate [Disarm Contest](../05-combat/disarm-v0.md#shared-disarm-contest) targeting one held item, add **+2** to that contest's existing **Grip Retention modifier**. Decide before either contest roll. This is not a general Attack, Guard or Strength bonus; it does not prevent loss of an item if the contest is lost or resistance is physically impossible.

### TAL-C07 — Reactive Aim
**L 3 · Any · Triggered · Mundane · Aiming.** **Trigger:** another creature the shooter can meaningfully observe/track **finishes a voluntary movement step** while a legal ranged Aim against it can be established. The shooter may **spend their one Reaction for the round** in the corresponding response window to establish **one normal Aim preparation immediately, without paying the usual Physical Action AP for that Aim**. Declare target, specific ranged attack profile, precise objective and chosen eligible difficulty source then; the shooter needs usable aiming equipment. This is **Aim**, not an attack; all existing maximum mitigation **4**, breaking, one-active-Aim and duration rules apply, including expiration at the start of the shooter's **second subsequent turn after establishment** (the next eligible own turn counts as first). Does not create a shot, reserve one, trigger an Interception or avoid line-of-fire restrictions. If trigger or legal aim disappears after Reaction commitment, Reaction stays spent. **Watch:** interrupt/response ordering when the creature's step also triggers other Opportunities.

### TAL-C08 — Cross-Weapon Fluency
**L 3 · Any · Passive · Mundane · Melee.** Extend [B04 melee-only half-transfer](../05-combat/weapon-training-and-refinements-v0.md#melee-only-half-transfer) for a receiving melee family with directly invested rank `D` below highest directly invested melee-family rank `H`:

```text
Effective Melee Training = min(H, D + floor(H / 2) + 1, level rank cap)
```

When `D = H`, use `H` normally; without a directly invested melee source there is **no transfer**. No transfer into/from **Bows or Crossbows**, chaining, use of effective ranks as sources, or satisfaction of a refinement's **direct-investment prerequisite**. E.g. `H=+5, D=0` normally yields effective `+2`; this Talent yields `+3`.

### TAL-C09 — Disengaging Strike
**L 3 · Any · Passive · Mundane · Movement.** **Once per own turn**, after actually resolving a legal ordinary **melee weapon attack** against one creature, designate that creature. Your **next single Normal movement step this turn** that would create a **Movement Opportunity from that designated creature** is treated as **Cautious solely against that creature without doubling that step's base MP cost**. Pay normal step, terrain and occupancy costs; other enemies' Movement Opportunities still apply, and this does not change an earlier segment's existing one-opportunity-per-enemy limit. No extra attack, MP, disengagement from other enemies, or immunity to action-triggered Opportunities. Does not apply to Charge, Sprint or Rapid Advance movement.

### TAL-C10 — Emergency Regeneration
**L 3 · Any · Triggered · Veil-assisted.** **Trigger:** a single attack or hazard is about to apply a **confirmed HP-damage amount** to the character. **Before subtracting that HP damage**, while the character is still **conscious with positive HP**, spend **one Reaction**, **ceil(HP restored / 2) Spent VP**, and **1 Vigor per HP restored**, then immediately restore **a chosen positive number of HP no greater than current regeneration throughput**, also limited by **existing missing HP, current Vigor, and available VP**. If throughput is 0 or no positive amount can be funded, activation is illegal. Choose the restored amount when committing; if no HP is missing, this Talent cannot activate. This is **HP restoration only**; no wound Repair Progress, Dying recovery, Vigor restoration or extra regeneration step. Ordinary suppression/repair restrictions remain. Afterwards apply the original damage and its wound trigger normally if it drops the target from positive to nonpositive HP. A failed/invalid subsequent hit does not refund a committed Reaction/VP. **Watch:** exact response placement versus criticals, simultaneous damage and defensive commitments.

### TAL-C11 — Adaptive Protector
**L 3 · Any · Passive · Mundane · Defensive timing.** When making a legal **Prepared Protective Intervene** reservation, the character may **defer only the choice between Shield Guard and Body Take Hit** until the reserved Movement Interception releases. At reservation still name the protected creature and meaningful specific trigger, reserve MP and retain all ordinary requirements. On release choose **one** protective option before the incoming roll, with appropriate legal shield/body position; if neither option is legal the reservation has no protective effect. This changes **when a choice is locked**, not the number of protected attacks, movement, available Guard capacity, Reaction, or reservation expiry. [Protective Intervene](../05-combat/protective-intervene-v0.md) controls all other resolution.

### TAL-C12 — Dual-Source Aim
**L 5 · Any · Passive · Mundane · Aiming.** When completing **one** ordinary Aim, nominate **two distinct eligible shot-difficulty sources** rather than one, for the **same target and same attack profile**. Declare both aiming objectives and sources **before committing the Aim AP**; neither can be replaced when the attack is declared or after seeing a defense. **At attack declaration**, identify the **one attack** receiving this Aim, pay its attack cost and preserve the existing Attack Sequence commitments; **do not allocate mitigation yet**. **Immediately after the defender assigns Take Hit, Dodge or legal projectile Guard, but before rolling**, allocate **at most 4 total mitigation** across the two previously named **positive difficulty sources that actually apply to the assigned defense** (never more than that source's current positive value). **For an Attack Sequence**, declare every attack and assign all defenses first, then lock the allocation for its one identified aimed attack **before the sequence's first attack roll**, even if that shot is later in the sequence. **For a standalone attack**, allocate just after its individual defense is assigned and before its roll. A source absent from the assigned defense receives **0**: for example, Range Difficulty normally does not apply to projectile Guard, while independently eligible Cover Difficulty does. **After allocation is locked**, later Interceptions, Reactions, position changes or a legal lost-Guard fallback may change which difficulty sources apply at actual resolution: apply each already allocated mitigation only up to that source's **then-applicable positive value**, and **lose any remaining share**. Do **not** reallocate it to the other named source or a third source, convert it to Attack, or retain it for another shot. There is **no reassignment after allocation**, including after prior attacks in the sequence resolve or after seeing the aimed attack's result. The combined mitigation is **4 total, not 4 per source**. The prepared Aim is still consumed by **one attack** and cannot bypass complete cover, legal Called Shot permission or screen-hit procedures. No target/profile switching or stacking Aim preparations.

### TAL-C13 — Contingent Interception
**L 5 · Any · Passive · Mundane · Prepared timing.** When reserving **one otherwise legal Interception action or Movement Interception**, the character may define **two distinct, specific, plausible, non-guaranteed triggers referring to the same named creature or fixed location**, rather than one. **Only the first occurring legal trigger releases** the single atomic reservation; the second expires with it, and no second action/MP pool is created. Both triggers must present a real possibility of **neither** occurring before default expiry (no vague “if anything happens” triggers). The initial AP/MP commitment, existing trigger priority, action legality and default expiry are unchanged. Does not bundle Aim + Attack or circumvent Rapid Advance/Charge/Sprint reservations.

### TAL-C14 — Burst Footwork
**L 5 · Any · Activated · Veil-assisted · Movement.** **Once during the character's own turn**, pay **2 Vigor** before starting a legal **Normal movement segment** and gain **2 additional MP usable on Normal movement that turn only**. These MP vanish at turn cleanup. They are **not** multiplied into Rapid Advance, Charge or Sprint allowances, cannot be newly reserved as Movement Interception, and do not fund free movement outside the character's turn. Ordinary terrain, blocked squares and Movement Opportunities apply. Cannot activate when Vigor is insufficient.

## Magical tactics / spellcasting — 5

### TAL-M01 — Deep Volition Reserve
**L 1 · Any · Passive · Veil-assisted.** Increase **Max VP by +2 flat**, not `+2 × Level`. **When this Talent is first acquired (including at character creation), place both newly granted VP in the Spent state**, not Available or Committed. They subsequently return to **Available VP** through the normal completed-6-hour **VP Recovery** procedure, calculated against the **new Max VP** with existing rounding. The VP ledger must always satisfy **Available + Committed + Spent = Max VP**. Purchasing the Talent does **not** immediately restore VP, create usable VP before recovery, add regeneration, alter Veil Affinity, or grant an extra spell. No stacking with itself.

### TAL-M02 — Volitional Calibration
**L 1 · Any · Activated · Veil-assisted · Direct magic.** **Once per round**, before rolling **Direct Veil Pressure** for an **otherwise legal, authored Imposition or Intrusion effect**, spend **1 additional VP** to gain **+2 as an explicit modifier on that single Direct Veil Pressure roll**. Pay the technique's ordinary separate cost and resolve normal target resistance. This does **not** increase Veil Control, standard damage packets, tier, effect duration, or Manifestation attacks; no roll means no use. The additional VP is Spent even if the effect fails. Requires actual access to a qualifying authored direct Veil effect.

### TAL-M03 — Frugal Technique
**L 3 · Any · Passive · Veil-assisted.** **Once on the character's own turn**, one otherwise legal **authored Veil technique** with a normal **Spent VP component of at least 2** costs **1 fewer Spent VP** for that activation (minimum 1). Declare the discount before paying. Does not lower Committed VP, Destiny, a separate Overroute/Surge/Invocation surcharge, an external item cost, or composite secondary costs separately; does not refresh output or create a zero-VP cast. A composite, when otherwise legal, counts as **one** activation with at most one such reduction from its aggregate ordinary Spent VP cost.

### TAL-M04 — Patient Projection
**L 5 · Any · Activated · Veil-assisted · Interception.** **Once per round**, while reserving an **otherwise eligible authored Projection Action technique** as one atomic [Interception](../05-combat/initiative-and-round-structure.md#interception), spend **1 extra VP immediately** (Spent). That **single reservation** expires at the **start of your second subsequent turn**, rather than the default start of your next turn. The usual AP is committed at reservation; normal technique VP is paid at its normal resolution, and unused reservations do not refund the extra VP/AP. The trigger must remain specific and non-guaranteed. This does not prepare a second spell, extend an effect's duration, or allow Full-Action effects that cannot be reserved.

### TAL-M05 — Veil Brace
**L 5 · Any · Triggered · Veil-assisted · Defensive.** When the character is a target of a **declared direct Imposition or Intrusion** and a pressure roll has **not** yet occurred, spend **one Reaction + 2 Spent VP** to add **+2 to their static Direct Veil Resistance against that one effect**. Declare before the Pressure roll; if the effect later misses/loses legality there is no refund. This does **not** protect allies, count as a Guard or Dodge, impose Intrusion Barrier on Imposition, help against physical Manifestations, create counterspells, or prevent a target from choosing to waive resistance.

## Archetype-specific — 8

### TAL-P01 — Expanded Liturgy
**L 1 · Priest only · Passive · Veil-assisted.** Gain **+1 base Prepared Prayer capacity** at the next normal preparation; choose the extra eligible **chosen-Pillar** prayer then. This adds to (but is not itself) the separate positive **Pillar Accord** capacity adjustment. It does not increase Accord, add a second Pillar, allow unprepared invocation for free, change tier, count as a Universal procedure slot, or grant a Miracle Petition. Requires an authored eligible prayer to make the slot useful.

### TAL-P02 — Disciplined Invocation
**L 5 · Priest only · Passive · Veil-assisted.** **Once per round**, when activating a **chosen-Pillar Prepared Prayer** with a normal **Spent VP cost of at least 2**, reduce that *ordinary* Spent VP component by **1** (minimum 1). Works on a legal out-of-turn activation if the prayer independently has that timing, unlike `TAL-M03`'s own-turn restriction; no new Reaction is granted. Does not change Open Invocation surcharges, Accord, Miracle Petition, Committed VP or other separately authored cost. A prayer cannot benefit from both this and `TAL-M03` on the same activation. **Watch:** comparative efficiency of Priest and shared VP discounts.

### TAL-S01 — Expanded Repertoire
**L 1 · Scholar only · Passive · Technical.** Learn **one additional individually learned Pillar/Aspect technique** within the normal tier ceiling and any other genuine learning/access prerequisites. This is **one** extra known Pillar technique, not an extra Aspect catalogue, composite formula, automatic preparation or Universal procedure. Select when Talent is acquired; if no eligible authored technique is available, save the Talent selection rather than create an imagined spell.

### TAL-S02 — Formula Precision
**L 5 · Scholar only · Passive · Technical.** Choose **one authored, individually learned Pillar technique** that has a normal **Direct Veil Pressure** or explicitly defined magical **attack roll**. **Once per own turn**, add **+1 to that one qualifying roll** when resolving the chosen technique; declare which roll before it is made if both are ever available. No +1 Veil Control, packet scaling, tier, VP reduction, extra spell, or direct benefit to a Composite Secondary that makes no independent roll. Changing the nominated technique requires an as-yet-unauthored retraining procedure.

### TAL-G01 — Emotional Poise
**L 1 · Gifted only · Passive · Emotional.** **Once per Emotion Window**, before rolling a legal **Emotional Transition check** against a genuinely **dominant competing emotion**, add **+2** to that single check. Normal General Tempo AP, eligibility, active emotion, and failure rules apply. This is not automatic Heightening, an additional emotion-to-Aspect link, an Instability bonus, or a change to **Universal Veil** access.

### TAL-G02 — Measured Deepening
**L 5 · Gifted only · Passive · Emotional.** **Once per 6-hour interval**, when an actual paid **Deepen Emotion** check fails, reroll that check immediately and keep the **second result**. It is still the **same Deepen attempt** (same spent General Tempo Action and Emotion Window); it does not permit a second Deepen attempt, force Overwhelming intensity, recover an Amplification Step, or change a linked Aspect. Cannot be used on Emotional Transition or Instability.

### TAL-A01 — Imprint Recall
**L 1 · Anointed only · Passive · Knowledge.** **Once per 6-hour interval**, when the character fails a legitimate **Intellect + relevant Pillar Lore or era/region History** check to recall, interpret or explain something about **their own bonded Pillar's pattern or Birth Imprint context**, reroll and keep the **second result**. Does not reveal absent or secret information automatically, grant an additional Aspect, change Mission, or substitute for an actual Signature/Authority effect.

### TAL-A02 — Signature Precision
**L 5 · Anointed only · Passive · Veil-assisted.** Requires an **authored, accessible Signature Expression** with a legal attack roll or Direct Veil Pressure roll. **Once per own turn**, add **+1 to one such roll** from that Signature, declared before rolling. Not +1 Veil Control, damage output, VP, Destiny, Aspect Authority, or a second Signature activation. If the Signature has no applicable roll, this Talent cannot be selected for it; an eligible player may save the selection instead. Bond Dormancy or other normal eligibility limits still apply.

## Knowledge, exploration and practical utility — 5

### TAL-U01 — Veil Insight
**L 1 · Any · Passive · Scholarly.** Prerequisite: at least **+1 directly invested** in **Veil Theory** or **Pillar Lore**. **Once per 6-hour interval**, after failing one legitimate check using either of those *actually applicable* narrow disciplines to **interpret an already observed Veil structure, enchantment or Pillar pattern**, reroll that check and keep the second result. Not free Veil Inspection, not automatic detection or an all-purpose magical Attack modifier; information must be plausibly available, and effects of irreversible failures are not reversed.

### TAL-U02 — Practical Appraisal
**L 1 · Any · Procedural · Mundane.** Prerequisite: **+1 directly invested** in Smithing, Engineering, Carpentry, Tailoring or a relevant named Trade. **Once per 6 hours**, when a **time-pressured, legitimately applicable** check with one of those disciplines to assess an ordinary item or mechanism fails, the character nevertheless learns **one concretely observable partial detail** of its construction/material state (e.g. an inferior alloy, a worn joint, a likely repair need) that such an inspection could physically reveal. The **overall task/check still fails**, and the GM need not reveal facts that would require success, a disassembly that has not occurred, or an inaccessible interior. This is a **bounded partial-information guarantee under pressure**, not automatic full identification, a general bonus, a new crafting recipe, curse/magical-signature detection, or free repair. It gives no benefit when the ordinary skill check already succeeds or when no check is needed.

### TAL-U03 — Field Diagnosis
**L 1 · Any · Passive · Mundane.** Prerequisite: **+1 directly invested Medicine**. **Once per 6-hour interval**, reroll one failed, **time-pressured Medicine check** to diagnose an observed injury or apply an ordinary independently legal first-aid procedure; keep the second result. Cannot heal HP, create Repair Progress, replace the Dying procedure, revive a dead creature, invent a treatment, or reverse irreversible harm from the failed first attempt.

### TAL-U04 — Route Familiarity
**L 1 · Any · Procedural · Mundane.** Prerequisite: **+1 directly invested Navigation or Tracking**. After at least **10 minutes studying a particular traversable route, actual maps, bearings or physical traces**, designate one specific planned route segment. **Once per 6-hour interval**, gain **+2 as an explicit situational modifier to one subsequent relevant Navigation or Tracking check** along that segment before the character next completes a 6-hour interval. This is not a general +2 Training, map creation, an assumed safe passage, or a bypass of unfamiliar routes/obstacles.

### TAL-U05 — Prepared Contingency
**L 5 · Any · Procedural · Mundane.** Prerequisite: **+2 directly invested** in one named Learned Discipline. Spend **10 minutes** preparing tools, notes or a feasible task-specific method for **one declared later task** actually using that discipline; the relevant resources must exist. **Once per 6-hour interval**, if the character subsequently fails a **time-pressured check for that declared task** while circumstances still match the plan, immediately reroll and keep the **second result**. An irreversible failure, absent information, changed task, or impossible method cannot be undone; no generic social/perception bonus, no additional equipment or crafting recipe.

## Example test characters and consistency cases

1. **Level-3 Low-Focus archer** with `TAL-C07 Reactive Aim` can use their Reaction after a tracked enemy completes a legal step to establish ordinary Aim. On their next attack they pay the attack AP normally and reduce at most one chosen applicable positive difficulty by at most 4. They cannot spend that same Reaction on Reactive Intervene or initial Opportunity Response.
2. **Level-3 mixed-weapon fighter** with `H=+2` directly invested in Swords and no Axe investment has ordinary half-transfer `+1`, improved to **+2** by `TAL-C08`; the character still lacks a directly invested Axe rank required by an Axe-only Style Refinement.
3. **Level-3 wounded caster** with HP 6/10, Vigor 5 and regeneration throughput 3 may spend Reaction, **2 Spent VP**, and **3 Vigor** to restore 3 HP before a confirmed HP-damaging hit. The incoming hit still resolves in full afterward. If already at HP 0 they cannot use `TAL-C10`.
4. **Level-5 High-Focus caster** might spend one of two early Talent choices on `TAL-M01` or an Archetype repertoire option rather than martial utility; this character still acquires projected magic through their normal Archetype, separately from Talents.
5. **Low-Focus investigator** can select `TAL-U01` and `TAL-U04` instead of combat Talents, if directly invested Training prerequisites are met. Having more Talent selections does **not** require martial advancement.
6. **Repeated casting:** `TAL-P02` and `TAL-M03` cannot stack on a single prayer. Neither makes a 1-VP technique cost zero nor lowers additional Invocation surcharges. `TAL-S02` does not change its selected technique's Standard Veil Control damage packet.

## Playtest notes / unresolved extensions

- Most physical entries are mechanically exercisable against the current action and defense framework. Some spell/Archetype entries require **future authored technique or Signature entries**; **save the selection** if no actual qualifying content exists.
- Catalogue is designed for levels **1–5 only**. Nothing here grants extra Talent selections at levels 6–20, adds advanced crafting, resolves universal helping/group checks, or creates custom magic items.
- Track eligibility by actual weapon family, available Ward/Prayer/technique, direct-investment rank and current turn/round resources. Test at all **12 Archetype/Focus combinations**, especially one-build depletion after four early Low-Focus picks.
- No numerical item crafting, enchanting or potion Talent is selectable in this MVP.
