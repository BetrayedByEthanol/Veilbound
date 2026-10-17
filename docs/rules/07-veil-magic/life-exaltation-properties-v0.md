# Life Exaltation Properties v0 — Low Priest Level 3

> **EXECUTABLE v0, numerical values PROVISIONAL.** Implements the [universal Exaltation framework](../08-archetypes/low-priest-exaltation-framework-v0.md). Each property requires the **one specifically identified active Chosen Rite instance**. Neither is an independently cast spell, generic Secondary contribution, or additional Prepared Prayer. No Level-5 cross-Aspect compatibility is authored yet.

## EX-LR-01 — Held Renewal

| Field | Rule |
|---|---|
| Identity | **Life / Restoration**, Level-3 Low Priest Exaltation |
| Pattern | Defer use of otherwise-unused throughput **from an already real Regeneration Step** |
| Host | **Self-targeted maintained Chosen Guided Regeneration** actually supplying its Regeneration modifier |
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
