# Life Exaltation Properties v0 — Low Priest Level 3

> **EXECUTABLE v0, numerical values PROVISIONAL.** Implements the [universal Exaltation framework](../08-archetypes/low-priest-exaltation-framework-v0.md). Each property requires the **one specifically identified active Chosen Rite instance**. Neither is an independently cast spell, generic Secondary contribution, or additional Prepared Prayer. No Level-5 cross-Aspect compatibility is authored yet.

## EX-LR-01 — Held Renewal

| Field | Rule |
|---|---|
| Identity | **Life / Restoration**, Level-3 Low Priest Exaltation |
| Pattern | Defer use of otherwise-unused throughput **from an already real Regeneration Step** |
| Host | Any **self-targeted maintained Chosen Life/Restoration Rite** actively giving its owner an authored positive modifier to their genuine Regeneration Step throughput. **Guided Regeneration** currently qualifies |
| Activation | **End of Priest's genuine own-turn Regeneration Step while in initiative**, after all normal allocation and before start-of-turn hazards; **0 additional AP, no Reaction** |
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
| Host | Any **self-targeted maintained Chosen Life/Preservation Rite** with an **actual finite numeric budget preventing incoming direct Vigor-damage packets** and at least **2 unspent points**. **Vital Shelter Primary** currently qualifies |
| Activation | One legal **own-turn decision point in initiative**, while conscious and at positive HP; expressly **0 additional AP, no Reaction** |
| Price | **1 Spent VP** immediately, beyond the Chosen host's **1 Committed +1 Spent** establishment price |
| Trigger | First subsequent **incoming HP-damage packet** that would actually lower the Priest's HP after ordinary defense/armor/resistance |
| Output | Before HP subtraction, prevent up to **2 HP**, spending **2 Shelter budget points per 1 HP prevented**: `prevented HP = min(2, eligible HP damage, floor(current Shelter budget / 2))` |
| Duration | Until the start of the Priest's **next own turn**, first qualifying HP packet, initiative exit, end of the exact Chosen Shelter, or depletion of its finite budget |
| Frequency | **At most once per Priest own turn**; no stacking, free reroute or renewal of remaining budget |

**Activation.** Require an actually eligible **Chosen self-maintained finite Vigor-prevention budget** active **on the Priest** (currently Vital Shelter Primary), at least 2 remaining budget, one free pending Exaltation slot, a legal own-turn decision point and 1 Available VP. Pay that VP as **Spent on activation**, regardless of whether any HP harm subsequently arrives. This permission to arm the property for 0 additional AP **is specific to this entry**: no ordinary spell activation, off-turn ability or Reaction is created.

**Conversion.** An incoming hit/hazard first resolves its normal delivery, defenses, Armor and any applicable existing resistance. If it would deal **positive actual HP damage**, use up to **2** of that HP packet's points and consume **2 real, already remaining Vital Shelter budget points for each HP prevented**. Do this **before subtracting HP and assessing the resulting 0-HP threshold**. A Devastating Critical or independently authored wound trigger still applies even when HP injury is partly prevented. One arm protects **one actual HP packet only**; no other HP packets gain protection until a separately legal new activation.

For a mixed HP/Vigor event, after native defensive/mitigation checks, **apply the Exaltation's HP-budget diversion first**, then process that event's independent direct Vigor packet under normal Vital Shelter prevention using **only the remaining original budget**. If earlier Vigor packets consumed enough budget that fewer than 2 remain, the next HP packet consumes the armed Exaltation **without preventing HP**. Pure Vigor packets still use normal Vital Shelter rules and **do not trigger** the Exaltation. Fully mitigated HP packets, voluntary expenditures and ordinary Dying-round HP decay do not trigger it. No extra HP resistance rating is created.

**Termination.** Reaching original Shelter budget **0** ends the host immediately under its own rules, refunds only its actual **1 Committed VP** if Chosen, and ends pending Exaltation. The original Shelter **1 Spent establishment VP** and the Exaltation **1 Spent VP** never return. Ordinary budget depletion, Rite release, initiative exit or expiry do not recharge anything, and non-Chosen copies do not inherit the property.

**Identity boundary.** This expresses **Preservation** by redirecting an existing finite self-protective reservoir to prevent a little direct HP injury. It is not automatic Stone Skin-style resistance, retrospective healing, regeneration, Venom Endurance's toxin prevention/suppression, or protection for other recipients.

### EX-LP-01 regression

| Case | Expected |
|---|---|
| L3 Low VA0, VC0, Chosen Vital Shelter | Max VP **6**; host costs **1 Committed + 1 Spent** leaving **4 Available**, with actual **B8** |
| Arm Vital Interposition on own turn | Pay **1 more Spent**, leave **3 Available**; original **B8** unchanged at arming |
| B8, next after-mitigation packet HP5 | Prevent **2 HP**, consume **4 of B8**, apply **3 HP**, leaving **B4** |
| B8, mixed event HP5 + Vigor3, current Vigor positive | HP prevention consumes B4; original shelter then prevents Vigor3 consuming B3; **B1** remains |
| B3, next HP5 | Prevent **1 HP** for **2 budget**, apply 4 HP, leave **B1** |
| B1 from earlier Vigor prevention, first HP packet arrives | Spend **0** budget preventing **0 HP**; pending property expires, no bonus capacity |
| Incoming Vigor only, or HP fully stopped by Armor | Ordinary shelter handles Vigor; pending HP property stays armed while host remains |
| Another HP hit after the first qualifying HP packet | No further HP diversion until another legal own-turn Exaltation activation |
| Shelter depleted or released, or Priest exits initiative | Pending property expires, no Spent VP refund; no second Rite or independent protection |

## Scope and Level-5 boundary

These are **two executable Level-3 Life properties** with **provisional 1-Spent VP prices and 2-point limits**. Their required host capabilities are narrow; other future Life Rites may qualify only if a property explicitly names or accurately covers their authored capability. No automatically cast Venom Endurance or other technique is granted.

At Level 3 they cannot cross Aspects. At Level 5, Living Liturgy still needs an **explicitly authorized cross-Aspect host match and all normal stability rules**; none is granted merely because the property shares the Life Pillar. Held Renewal does not work on Vital Shelter (no Regen modifier), and Vital Interposition does not work on Guided Regeneration (no finite shelter budget). The [Earth and Fire probes](../../design/b05-exaltation-cross-pillar-design-tests.md) are NON-EXECUTABLE.
