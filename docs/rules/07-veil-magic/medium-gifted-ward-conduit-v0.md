# Medium Gifted Ward Conduit v0 — Restricted L1–3 Expression

> **Provisional executable L1–3 Ward Focus expression, merged in PR #155 from the earlier [Medium Gifted Conduit Expression Design v0](../../design/b04-b05-medium-gifted-l1-l3-conduit-expression-design-v0.md).** This [bounded native encounter integration](../../design/b04-b05-medium-gifted-native-ward-encounter-integration-v0.md) sources real G4 damage and G5 hit/miss events, without adding another Tier-1 technique, extra link, free Reaction or approved global finite-budget priority. Grade values and setup costs remain playtest provisional.

Rules basis: [Gifted foundation](../08-archetypes/gifted.md#medium-gifted--conduits-and-retuning), [VP states](volition-points.md), [Turn AP](../05-combat/action-categories-and-physical-tempo.md), [persistent expression cadence](technique-tiers-and-expression.md#persistent-expression-cadence), and [damage](../06-vigor-wounds-death/hp-and-vigor.md). All individually cast ordinary techniques (including [Stone Skin](stone-skin-v0.md) and [Protective Ward](protective-ward-v0.md)) retain their own prices, delivery and eligibility independently of the Conduit.

## Identity, establishment, and duration

| Field | L1–3 Ward Conduit v0 |
|---|---|
| Who can use it | **Medium Gifted** with an eligible current emotion-to-Aspect link; a Conduit is a Focus expression, not a learned, prepared or freely cast technique |
| Form and host | **Ward**, **self-anchored** to the caster's living body/position; no item, remote ward, moving independent ward or other host |
| Slot limit | **1** at L1–2; **2** at L3; Dormant Conduits still occupy slots |
| Grade and Committed VP | Grade **I/II/III = 1/2/3 Committed VP** per Conduit; chosen during paid initial establishment; no automatic regrading with emotion or level |
| Initial placement | **24 AP**, one own-turn General Tempo Action, and the chosen Grade's Committed VP; conscious caster, free slot, sufficient Available VP and valid self-anchor required; never automatic or free at level-up |
| Duration | **Continuous** while caster remains conscious, self-host exists and this instance's VP remain Committed. Voluntary release or unconsciousness ends it; release returns only that instance's Committed VP to Available, never previously Spent VP |
| Access after placement | Immediately retunes on **real Active Emotion** establishment/change: Fear–Earth/Fortification → Holdfast; Trust–Kinship/Guardian → Shared Reserve; **all other emotions or unset → Dormant**, keeping Grade, slot and Committed VP |
| Cadence | **one Pulse per Conduit per Emotion Window**, on its first eligible nonzero original post-mitigation damage packet; cannot bank Pulses or refresh by attack, turn-ending, emotion switching, Reconduction or same-window re-establishment |
| Scaling | No Used Tier, level or standard VC × level scaling. One Pulse prevents **min(Grade, remaining eligible damage)**; Grade I/II/III = **1/2/3** maximum |
| Exclusions | No Stone Skin resistance, Protective Ward shield roll, free Guard/Dodge or Reaction, attack negation, redirect, HP/Vigor healing, passive unlimited prevention, cross-Aspect expression, new Tier-1 spell or Universal Veil compatibility |

A Conduit may be placed in Dormant state if the current emotion lacks its Form's authored expression, but placing it still pays 24 AP and Grade VP. A change to Active Emotion does not change Grade, anchor, VP balance, or the existing Emotion Window. The first legal linked technique may establish a previously unset emotion according to the base Gifted foundation; its normal AP/VP price and legal target are **not waived**. Only one Active Emotion exists at once, so Fear and Trust effects cannot both operate during the same incoming event. Universal Veil Inspection/Blink never establish an emotion by themselves.

## Exact emotion-linked Ward expressions

| Active link | Output, packet and recipient | Limits |
|---|---|---|
| **Fear → Earth / Fortification** | **Holdfast**: Pulse up to **1/2/3** prevention of the caster's **first eligible direct Physical-type HP damage packet** with positive remaining damage after that packet's legal Armor and **single highest** applicable resistance. Physical includes eligible Cut, Piercing and Crush. | Self only. Not Fire/Electrical/elemental HP, Vigor, indirect condition, extra resistance, or a persistent Stone Skin effect. |
| **Trust → Kinship / Guardian** | **Shared Reserve**: Pulse up to **1/2/3** prevention of **one original direct Vigor-damage packet** to **one other allied creature orthogonally adjacent to the caster** (one grid side, not diagonal) at the event. | Requires real ally, adjacency, open unobstructed relation; not self/enemies/far ally, HP, toxin-tick/milestone/resource exhaustion absent an expressly *direct damage* source, or a free Protective Ward Reaction. |

For Trust, measure adjacency from actual established occupied cells at the relevant damage event. No free movement, teleportation, reach through a solid wall, bending path or closer cell selected by an existing separately defined multi-square-creature reference rule. Native multi-square, 3D, ally identity and obstruction timing must be proven by a later G1/G4 integration; the isolated pilot only supports single-square orthogonally adjacent creatures on one plane and rejects undecidable geometry. This limitation does not grant fictional immunity to damage or free extra opportunity windows.

## Prevention ordering and distinct event identity

1. Resolve the original attack, active defense, cover, valid pre-roll Reactions and damage source through their own rules. On an HP packet, apply its ordinary Armor/hazard mitigation and the **one highest eligible resistance** before Holdfast. On Direct Vigor, apply source-authored modifications and any independently required pre-damage protective responses before Shared Reserve. Do not treat a Ward as Armor/resistance or move it into the original hit/miss check.
2. Before the eligible **remaining** damage is actually taken, a ready Conduit on that recipient may Pulse up to min(Grade, remaining). If another finite prevention budget is simultaneously eligible but its ordering relative to this Pulse has no authored rule, the combination is **not yet certified for native play**; do not resolve by double-applying either budget. The bounded G4 adapter rejects overlapping finite-prevention budgets; future source rules must author the order before that combination is supported.
3. Evaluate eligible Conduits by their stable establishment order **oldest first**. One original damaging event may use **at most one** Ward Conduit Pulse total, even if L3 has two established Conduits; a second later eligible event may consume the other. An already-seen event cannot be replayed with a new packet identity just to harvest another Pulse. Non-eligible or zero post-mitigation packets never consume Pulse. Never reduce below zero damage or retroactively undo a committed wound.
4. The Pulse is automatic on the first eligible packet; it is **not** a per-attack choice, action, Reaction, Guard use, reroll, Direct Veil contest, extra response window or magical casting event. If the actor is incapacitated and the Conduit terminates **before** the event, it cannot Pulse.

The isolated `MediumGiftedWardDesign` engine models these budgets using caller-supplied event identities and already-mitigated amounts. It is **not** proof of a source-bound G0/G1/G3/G4/G5 prevention event. This PR's bounded G4/G5 bridge supplies native typed Soldier/Sentry packets, G4.5-attested G0-paid ordinary attacks **and independently attested G0/G1 off-turn Opportunity responses**, response-ordered hit/miss, wound-preflight parity and receipt binding; overlapping finite protection remains a downstream blocker.

## Reconduction, voluntary release, and refresh

- Reconduction changes an established Conduit's Grade, Form or anchor only when an **actually authored replacement Form/anchor exists**. At L1–3 it costs **24 AP and 3 Spent VP**, followed by the increase/decrease of Grade VP commitment. The Ward has only a **self** anchor and **Ward** Form in v0; only Grade changes are executable.
- **Preflight first:** Available VP must pay the 3-Spent surcharge **plus** any *positive* commitment delta, without counting future refunded commitment from lowering a Grade. Pay the action, Spent VP, then adjust the Grade commitment atomically. A change does **not** refresh a used Pulse or Emotion Window. Invalid or unaffordable requests spend **nothing**.
- Free voluntary release ends the specific Conduit, returns its own committed Grade VP and forfeits its unspent Pulse. **To prevent an immediate no-surcharge release/re-create Grade swap, a released Ward's self-anchor cannot accept a newly placed Ward until the next Emotion Window.** All other existing own Wards remain unaffected, and the next-window placement must pay its entire 24 AP and Grade VP again. This waiting restriction does not imply that a released Ward automatically returns next window; it must be established anew.
- Under the base Gifted emotion rules, each new Emotion Window can refresh the available Pulse eligibility for **still-existing** Conduits, not create new slots or recover Spent VP. Normal six-hour VP Recovery restores Spent VP by its own rule, not committed VP while a Conduit remains active. Unconsciousness ends Conduit maintenance, returning its Committed VP; it does not grant free post-unconsciousness setup.

## Level 1–3 source arithmetic and hard boundaries

At **Veil Affinity 0**, Medium Max VP is **4 / 8 / 12** for levels 1/2/3; Turn AP **30 / 36 / 42**. Medium Physical and Projection actions are **24 AP**. All three Grades are affordable at L1, but **Grade III commits 3 of 4 VP**, leaving only 1 Available; a normal 2-Spent-VP T1 technique is unavailable until sufficient VP is freed/recovered, and it is never an extra free Conduit Pulse. Two new Conduits at L3 require **48 AP**, which does not fit into a **42-AP** turn. A paid 24-AP Deepen plus a normal 24-AP T1 Projection also fails at all L1–3.

A Grade I → II Reconduction at L2 from `Available 7 / Committed 1 / Spent 0` results after payment in `Available 3 / Committed 2 / Spent 3`; at L1 it fails when only 3 Available remains because it needs 4 before commitment adjustment. One Grade II + one Grade II at L3 leave 8 Available out of 12 VP, so the independently priced 10-VP Blink is **not currently affordable** without a lawful release or other resource change. Universal acquisition at L3 never creates free VP or a third Conduit slot.

**Status:** This is a narrowly scoped L1–3 pilot Form/profile. Grade mitigation values, self-anchor and short ally range are provisional pending encounter/role balance. Neither the **full three-Form Conduit catalogue** nor independent Medium Gifted combat/noncombat Focus certification is implied. No B06 G9 milestone exists.
