# Life Exaltation Properties v0 — Low Priest Level 3

> **EXECUTABLE v0, numerical values PROVISIONAL.** Implements the [universal Exaltation framework](../08-archetypes/low-priest-exaltation-framework-v0.md). Each property requires the **one specifically identified active Chosen Rite instance**. Neither is an independently cast spell, generic Secondary contribution, or additional Prepared Prayer. No Level-5 cross-Aspect compatibility is authored yet.

## EX-LR-01 — Held Renewal

| Field | Rule |
|---|---|
| Identity | **Life / Restoration**, Level-3 Low Priest Exaltation |
| Pattern | Defer use of otherwise-unused throughput **from an already real Regeneration Step** |
| Host | Any **self-targeted maintained Chosen Life/Restoration Rite** actively giving its owner an authored positive modifier to their genuine Regeneration Step throughput. **Guided Regeneration** currently qualifies |
| Activation | **End of Priest's genuine own-turn Regeneration Step while in initiative**, while **conscious and at positive HP**, after all normal allocation and before start-of-turn hazards; **0 additional AP, no Reaction** |
| Price | **1 Spent VP** at activation, no separate reservation and no refund |
| Capacity | Hold **1 or 2 genuinely unused throughput points**, never more than unused actual throughput from that Step |
| Trigger | **First subsequent actual HP-loss event** on the Priest, resolved after damage, wound and Dying/death checks |
| Payout | Only if still **conscious and above 0 HP**: automatically restore `min(held points, actual missing HP, Current Vigor)` HP, consuming **1 Vigor per HP** |
| Expiry | At first real HP-loss event (whether healing succeeded or not), start of Priest's next own-turn Regeneration Step, initiative exit, or end of the exact Chosen Rite |
| Boundary | No new Step, no extra recipient, no Repair Progress at payout, no new Vigor, no resurrection, and no prevention of a first lethal HP crossing |

**Resolution.** Complete the legitimate Step's standard regeneration and wound-repair allocation, paying Vigor normally. Only **actual remaining positive throughput that would be lost at the end of that same Step** is eligible to be held. The player chooses 1 or 2 such points and pays 1 Spent VP immediately. **No Vigor is consumed for merely holding unused throughput**; it is paid only if HP is actually restored later. All other unused throughput expires as usual. A Priest cannot arm twice from one Step or while another property remains pending.

After the **first later event causing actual HP loss**, complete all normal damage, wounds and 0-HP/Dying/death determinations first. If still living, conscious and at positive HP, heal up to the held amount and current missing HP, paying 1 Vigor per HP; consume the held expression even if only part can be applied. If the first hit takes HP to 0 or below, **no healing occurs**, and the property expires. Full regeneration suppression in force at the payout also prevents the healing and consumes the held expression. Fully stopped damage, Vigor-only damage and voluntary resource spending are **not** HP-loss triggers.

**Clock boundary.** Arming requires an **actual initiative own-turn Regeneration Step**. There is no extrapolated out-of-initiative Step from toxin clocks or elapsed seconds. Leaving initiative expires the pending property; the next real own-turn Step also ends it before new allocation. This is **deferred expenditure of that original Step's throughput**, not a second Regeneration Step.

**Talent distinction.** [TAL-C10 Emergency Regeneration](../10-advancement/talents-level-1-5-v0.md#tal-c10--emergency-regeneration) is a **pre-damage Reaction**, restores missing HP immediately with its own VP price and current throughput and can change whether the attack causes a 0-HP crossing. Held Renewal is armed beforehand from *unused* throughput, pays its own VP in advance, triggers *after* actual damage, **cannot avert lethal crossing**, and uses no Reaction.

### EX-LR-01 regression

| Case | Expected |
|---|---|
| L3 Low VA0 Vitality0, self Chosen Guided Regeneration | Max VP **6**; Rite **1 Committed** and **5 Available** before property; actual throughput **Low 3 + Guided 1 = 4** |
| At HP10/10, no wounds, with 4 unused throughput, hold 2 | Pay **1 Spent** leaving **4 Available**; mark 2 unused points held; Vigor unchanged until payout |
| Later 3 HP actual damage, remain above 0 with Vigor≥2 | Resolve 10→7 HP and wounds first, then restore **2 HP for 2 Vigor** to HP9; one Step total |
| First damaging event takes HP3→0 or below | No HP recovery; normal Dying and wound procedure proceeds; pending points expire |
| Earlier hit fully absorbed by Armor, or Vigor-only packet | Held points remain pending; no false HP trigger |
| All throughput spent in the original Step | No legal activation, no VP spent |
| Host ends, initiative ends, or Priest reaches next true Step | Pending held points expire; no carryover, new Step, Vigor or Spent VP refund |

## EX-LP-01 — Vital Interposition

| Field | Rule |
|---|---|
| Identity | **Life / Preservation**, Level-3 Low Priest Exaltation |
| Pattern | Temporarily **convert some of a finite protective budget** to a new, bounded form of bodily protection |
| Host | Any **self-targeted maintained Chosen Life/Preservation Rite** with an **actual finite numeric budget preventing incoming direct Vigor-damage packets**. Must have **at least 2 unspent budget points at Exaltation activation**; after arming it may stay pending while the valid host has **1 point remaining**, but can prevent 0 HP at payout. **Vital Shelter Primary** currently qualifies |
| Activation | One legal **own-turn decision point in initiative**, while conscious and at positive HP; expressly **0 additional AP, no Reaction** |
| Price | **1 Spent VP** at Exaltation activation, independent of the **actual host's existing locked Committed VP and any already Spent establishment cost**. Vital Shelter as Chosen currently uses 1 Committed + 1 Spent to establish the host; other compatible hosts use their own prices |
| Trigger | First subsequent **single incoming hit/hazard event with positive aggregate HP damage** after each separate HP packet receives its ordinary mitigation; all HP packets belonging to that one event are **one** Exaltation trigger |
| Output | **Once per qualifying event**, before HP loss: prevent up to **2 HP** from the **sum of that event's individually mitigated HP packets**, spending **2 actual remaining host prevention-budget points per 1 HP prevented**: `prevented HP = min(2, sum(nonnegative post-mitigation HP packets in event), floor(actual host remaining budget / 2))` |
| Duration | Until the start of the Priest's **next own turn**, first qualifying HP-damaging event, initiative exit, end of the exact Chosen host, or depletion of its actual finite budget |
| Frequency | **At most once per Priest own turn**; no stacking, free reroute or renewal of remaining budget |

**Activation.** Require an actually eligible **Chosen self-maintained finite Vigor-prevention budget** active **on the Priest** (currently Vital Shelter Primary), at least 2 remaining budget, one free pending Exaltation slot, a legal own-turn decision point and 1 Available VP. Pay that VP as **Spent on activation**, regardless of whether any HP harm subsequently arrives. This permission to arm the property for 0 additional AP **is specific to this entry**: no ordinary spell activation, off-turn ability or Reaction is created.

**Conversion — one hit/event, not one typed packet.** Resolve the entire incoming hit/hazard's legitimate delivery and defenses, then independently apply the existing Armor/penetration and each packet's highest applicable typed resistance. **Gather every nonnegative post-mitigation HP packet belonging to that same originating hit/event** (for example, physical HP and Fire HP on a Conjure Flame-enchanted sword hit) and sum them into one **event HP total**. The first event with **event HP total > 0** triggers Vital Interposition **once**, with no player selection, no preference for a primary/physical/elemental packet, and no implied global packet order. Before subtracting HP, prevent `min(2, event HP total, floor(actual remaining host Vigor-prevention budget / 2))` HP from **that event total**, and spend **2 actual host budget points per 1 HP prevented**. Subtract the reduced **event HP total** from HP once for this property's accounting; individual packets retain their original types and ordinary independent mitigation, and this rule does not change their authored delivery or other non-HP effects. Assess one-event 0-HP/wound/death consequences against the **final HP loss after prevention**; separately qualifying Devastating Critical wounds remain applicable. The pending property is consumed by the one triggering event, not one selected packet, regardless of how many HP packets it contained. For this property **no packet is declared to have 'won'**: it prevents event-total HP rather than inventing a physical-versus-Fire ordering. If another explicit rule needs a particular packet's actual surviving type-specific HP amount, that interaction requires its own ordering/provenance rule; Vital Interposition itself grants no arbitrary assignment.

For a single **mixed physical/elemental HP and direct Vigor-damage event**, first finish **all individual HP packet mitigation**, then apply the Exaltation **once to the sum of that event's positive remaining HP packets**, consuming the requisite **actual host finite budget before applying HP**; process that event's independent direct Vigor packet(s) afterward using **only the host budget remaining** under its ordinary prevention procedure. This **HP-before-Vigor budget priority applies only within the same event**; prior separately resolved Vigor-damage events already consumed their budget normally. If fewer than 2 host points remain at the later qualifying HP event, the armed property is consumed with no HP prevented. Pure Vigor-only events still consume budget according to the host and **do not trigger** this property. An event whose HP packets are all mitigated to zero, voluntary resource expenditures and ordinary Dying-round HP loss do not trigger it. This protection is a **one-event finite-budget diversion**, not a new general HP-resistance rating, nor a general change to elemental/physical packet mitigation.

**Termination and per-instance VP ledger.** Depleting the **actual qualifying Chosen host's finite Vigor-prevention budget to 0** always ends any **pending Vital Interposition**. It ends **the host itself** immediately **only if that host's own authored rules end it at depletion**; otherwise the host remains maintained under its own rules and **no host Committed VP is returned merely because this property's required budget is exhausted**. On host end, return **only the actual effective VP still Committed by that specific host instance** according to its original reservation ledger, **not Vital Shelter's example 1 VP by default**. The host's **own Spent VP establishment costs, if any, remain Spent in their actual original amounts**, and the Exaltation's separate **1 Spent VP never returns**. This property does not change a host's initial Committed VP, create a reservation, supply an establishment cost, or refund/convert Spent VP. A host's own depletion, legal Rite release, initiative exit or property expiry does not recharge the finite budget; non-Chosen copies never inherit the property. **Current Vital Shelter example only:** its Chosen instance refunds **1 Committed VP** on real termination, while its original **1 Spent** establishment cost stays Spent.

**Identity boundary.** This expresses **Preservation** by redirecting an existing finite self-protective reservoir to prevent a little direct HP injury. It is not automatic Stone Skin-style resistance, retrospective healing, regeneration, Venom Endurance's toxin prevention/suppression, or protection for other recipients.

### EX-LP-01 regression

| Case | Expected |
|---|---|
| L3 Low VA0, VC0, Chosen Vital Shelter | Max VP **6**; host costs **1 Committed + 1 Spent** leaving **4 Available**, with actual **B8** |
| Arm Vital Interposition on own turn | Pay **1 more Spent**, leave **3 Available**; original **B8** unchanged at arming |
| B8, next hit/event totals HP5 after ordinary packet mitigation | Prevent **2 HP** from the event total, consume **4 of B8**, apply **3 HP**, leaving **B4** |
| B8, mixed event HP5 + Vigor3, current Vigor positive | HP prevention consumes **4** budget first; normal host then prevents Vigor3 using **3** more; **B1** remains |
| B8, Conjure Flame-style single hit: physical HP1 + Fire HP2 after separate mitigation | Both HP packets belong to **one** hit. Aggregate HP **3**, prevent **2 HP total** for **4 budget**, apply **1 HP**; B **8→4**. **Neither packet is player-selected** and the effect never fires twice |
| B8, same mixed-type hit plus independent Vigor3, Current Vigor at least 3 | Prevent **2 of combined 3 HP** (B **8→4**); original host then prevents **3 Vigor** (B **4→1**). One event trigger; normal packet-specific Armor and Fire Resistance already applied |
| B4, mixed hit with physical HP1 + Fire HP2 + direct Vigor3; host is Vital Shelter | Prevent **2 HP** from event HP3; **B4→0**, so Vital Shelter ends immediately and returns its actual Chosen **1 Committed**. The later Vigor3 packet receives **no Vital Shelter prevention**, because the host has ended. Total actual HP loss **1**, Vigor damage **3** if Current Vigor permits |
| B3, next single-hit event total HP5 | Prevent **1 HP** for **2 budget**, apply **4 HP**, leave **B1** |
| B1 from earlier Vigor prevention, first HP packet arrives | Spend **0** budget preventing **0 HP**; pending property expires, no bonus capacity |
| Incoming Vigor only, or HP fully stopped by Armor | Ordinary shelter handles Vigor; pending HP property stays armed while host remains |
| Another HP hit after the first qualifying HP packet | No further HP diversion until another legal own-turn Exaltation activation |
| Actual host budget exhausted or host released, or Priest exits initiative | Pending property expires; refund only that **actual host instance's** remaining Committed VP if its own termination rule ends it. Original host Spent establishment VP and **1 Spent Exaltation** remain Spent; no second Rite or independent protection |
| **Hypothetical alternate qualifying Preservation host (accounting fixture only)**: at L3 Low VA0 Max VP6, effective **3 Committed +2 Spent** host with finite B2, then arm EX-LP-01 | Host established: **1 Available +3 Committed +2 Spent**. Exaltation spends the remaining **1 VP**, so **0 Available +3 Committed +3 Spent**. This is a host-ledger test, **not an authored new spell** |
| Same hypothetical host: HP event total2 uses both budget points and the host's own authored rule ends it at B0 | Prevent **1 HP**, consume B2. **Exactly 3 Committed VP** return to Available (**3 Available /0 Committed /3 Spent**); host's original **2 Spent** and Exaltation **1 Spent** do not refund. Never substitute Vital Shelter's example **1 Committed/1 Spent** |
| Alternative qualifying host whose own rules retain the host after budget reaches B0 | Pending Vital Interposition expires for lack of an available protection budget, **but the host's actual Committed VP stays Committed** until its own channel legally ends; no refund merely from property expiry |

## Scope and Level-5 boundary

These are **two executable Level-3 Life properties** with **provisional 1-Spent VP prices and 2-point limits**. Compatibility is **capability-based, not keyed to these two technique names**: future same-Aspect self-maintained Chosen Rites qualify automatically if their actually authored effects supply the exact throughput-modifier or finite Vigor-prevention-budget host predicate. The two named techniques are the current executable examples. No automatically cast Venom Endurance or other technique is granted.

At Level 3 they cannot cross Aspects. At Level 5, Living Liturgy still needs an **explicitly authorized cross-Aspect host match and all normal stability rules**; none is granted merely because the property shares the Life Pillar. Held Renewal does not work on Vital Shelter (no Regen modifier), and Vital Interposition does not work on Guided Regeneration (no finite shelter budget). The [Earth and Fire probes](../../design/b05-exaltation-cross-pillar-design-tests.md) are NON-EXECUTABLE.
