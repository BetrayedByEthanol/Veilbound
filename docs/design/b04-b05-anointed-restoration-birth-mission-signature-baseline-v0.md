# B04/B05 — Anointed Life/Restoration Birth, Mission and Signature Baseline v0

> **Design proposal and isolated numerical pilot contract — NOT an executable rule or player entitlement.** The Anointed foundation in [anointed.md](../rules/08-archetypes/anointed.md) is authoritative. This record proposes one common Life / Restoration birth-and-bond package and **one** restorative Signature principle with three Focus expressions. The Focus trigger, healing caps and Destiny price below require review, native binding and encounter/attrition calibration before promotion into `docs/rules/`. This PR creates **zero** completed Anointed L1–3 sheets and **zero** independent Focus certifications; MVP counts stay **9/12 structural, 0/12 independently certified, 0/6 strict gates**.

## Why this narrow slice

The original Anointed design sought a familiar, repeatedly useful Signature (comparable in *role*, not rules, to a character-defining repeatable magical attack), modified exceptionally through Destiny. Later Focus design demands distinct gameplay: **High acts through Projection; Medium invests one Vessel; Low embodies the Aspect**. It does **not** require three unrelated spells, a Signature spell list, mandatory Birth-Imprint variants, or an additional Signature resource.

**Authoring rule proposed for the pilot:** The bonded Aspect determines the common Signature operation; Focus determines the action pattern and eligible recipient; Destiny grants a bounded exception. Ordinary bonded techniques remain separate and spend VP normally. A modest baseline **0-VP Signature** must remain useful without requiring Destiny expenditure. It is not a free Tier-1 Basic Heal.

## Surge-born origin — extraordinary joy without prophecy

**Pilot surge: The Returning Steps.** Across a network of settlements, healers, patients, craftspeople and families spent generations establishing reproducible restorative treatment and rehabilitation practices. Their success spread, improving the prospects of people who had long been unable to regain ordinary bodily function. At an extraordinary public celebration of the widespread success—patients taking long-awaited steps among their families, communities embracing and passing on the practices—collective adoption, gratitude, commitment and synchronized **Volition** cohered around the **Life / Restoration** pattern in an exceptional Pillar surge. The Anointed was born during that surge; the child did not cause it and was not issued a command.

This is an illustrative *positively extraordinary* origin, not a requirement that surges are celebrations or even joyful. The **successful, culturally reinforced practice and exceptional collective Volition** make this a surge candidate, not happiness by itself. Tragedy, crisis, prior Pillar weakness, named bloodline, chosen parents, or a deity assigning a task are **not required**. The general surge pattern already exists in the Anointed foundation. This origin claims no new geographic radius or guaranteed number of Anointed per surge.

**One permanent bond:** Life / Restoration (Transform). The bond grants normal access to authored Restoration techniques at their real cost/level restrictions, not free access to other Life Aspects.

**Birth Imprint — The Returning Step.** A personal imprint of regained bodily function through patient, shared and sustained treatment. It colors the appearance and interpretation of the one common Signature; this pilot does **not** add a second technique selection, unique mechanically distinct Imprint subclass, or exclusion from ordinary Restoration techniques.

**Lifelong Mission:** *Make recovery possible where injury or illness has taken that possibility away.*

The Mission guides enduring activity without naming a quest completion or prescribing morality, profession, patient priority, or a single interpretation. Aligned/Conflicted/Forsaken and genuine reawakening retain their existing canonical definitions. The Mission is **not** a Pillar-issued order; sincere, enduring rejection—not an isolated difficult choice—causes Forsaken Dormancy. Mission state remains distinct from Resonance. A different Anointed may interpret the same surge differently; personal uniqueness need not multiply mechanics.

## Single common Signature: Returning Step

**Signature operation:** Turn a small amount of a living recipient's **existing Vigor** into immediate **HP** restoration, preserving the canonical **1 Vigor per 1 HP** conversion. This is a separate small restorative application, **not** an extra natural Regeneration Step or a throughput increase. The name and effect are one Signature, not three spells. Baseline **0 Spent VP / 0 Committed VP**.

**Candidate v0 resolution, not approved numbers:**

1. Require an active Anointed bond, a legal recipient and applicable Focus trigger. The recipient must be **alive, at positive HP**, and missing HP; a Dying recipient, dead creature or no missing HP provides no legal application. Ordinary refusals and **beneficial bodily Intrusion** rules still apply to an external recipient (including the +8 barrier for an effective refusal). The proposal does not authorize hostile Invested Vessels.
2. The Focus supplies an upper HP cap `K`: High **2 HP** for one paid Projection Action; Medium **1 HP** per eligible Invested Vessel's existing Regeneration Step; Low **1 HP** per own existing Regeneration Step while embodied. These different delivery budgets are **calibration candidates**, not new universal Focus bonuses.
3. Baseline actual HP restored is `H = min(K, MaxHP - HP, AvailableVigor)`. Subtract exactly `H` Vigor from **that recipient** and restore exactly `H` HP. No negative balances and no overhealing. The caster pays no Signature VP. If insufficient Vigor exists, do **not** conjure the missing HP.
4. The Signature grants **zero** direct Vigor, Wound Repair Progress, additional regeneration throughput, Dying-loss cancellation, stabilization, removal of conditions, maximum-HP increase or resurrection. A living non-Dying recipient with a separate unfinished wound may receive ordinary HP only; no hidden wound repair is created. Existing restrictions on HP restoration, magical suppression and bodily Intrusion remain applicable.
5. At most one completed pulse per eligible event/recipient. It does not stack with itself at a single trigger, generate extra actions or weapon attacks, and does not borrow Guided Regeneration's authored spell profile. Genuine resolution must use existing event/order authorities when implemented.

### Focus expression — *same conversion, different play pattern*

| Focus | L1 Signature use (v0 candidate) | Existing action economy and cadence | Distinctiveness |
|---|---|---|---|
| **High — Project** | Actively deliver up to **2 HP** to one eligible living recipient within **0–3 squares**, visible with a legal unobstructed magical path; beneficial bodily Intrusion and refusal apply. | **One Projection Action, 20 AP** per attempt; **0 VP**. Every completed cast is one pulse; no free Rider, spell copy, remote casting or bonus action. | A meaningful deliberate healing action that competes for AP. |
| **Medium — Invest** | Invest exactly **one consenting living creature** as Vessel (self allowed); after valid setup, restore up to **1 HP** to that Vessel once at the start of its existing Regeneration Step, immediately before normal regeneration. | Establish/change one Vessel: **one General Tempo Action, 24 AP, 0 VP**; release free. No extra regeneration step or activation AP per eligible vessel step. Require Vessel currently visible **within 0–3 squares with a legal magical path at each pulse**; Investment can remain but produces no remote pulse when those conditions fail. | Front-loaded commitment to one patient, not an always-on party-wide aura or remote casting. |
| **Low — Embody** | While the self-centered embodied Signature is manifested, restore up to **1 HP** to self once at the start of the Anointed's own existing Regeneration Step, immediately before normal regeneration. | **0 VP**; no new action and no separate Step. May suppress/resume at start of own turn under the foundation rule. No passive ally output, repeated weapon-hit heal, or extra Guard. | Persistent personal recovery, not another active Projection spell. |

Only **one** pulse of this Signature per such Focus-defined event; simultaneous duplicate triggering cannot accumulate more HP. Medium and Low restoration consumes the recipient's Vigor and occurs *before* normal Regeneration Step allocation, so ordinary regeneration may then spend further Vigor and throughput as usual. If both are available, they restore separately and never spend the same Vigor twice. A self-affected Medium Vessel is still one Vessel, not an additional target or second Signature.

**Outside initiative:** Do not invent a new elapsed-seconds-to-Regeneration-Step schedule. A High Anointed may repeatedly take ordinary legal Projection Actions where actions can be performed; each application still consumes **recipient Vigor**. Medium/Low event-driven pulses require a separately source-reconciled noncombat cadence before an executable rule can claim continuous healing between encounters. They cannot gain unlimited Vigor, repair wounds, or generate permanent accumulating benefit by repeatedly declaring harmless actions.

### L2–3 interface, deliberately not three extra spells

- **High L2 Expanded Projection:** **candidate** +1 square of *Signature-only* maximum reach (3 → 4), subject to visibility/path; no extra healing, targets or tier. Must be measured against other available support.
- **Medium L2 Channel Through Vessel:** the foundation permits compatible effects through Vessel, but **this draft grants no additional remote cast or normal-technique delivery**. Source-authored interactions remain a separate design/implementation step.
- **Low L2 Living Instrument:** **candidate** move the once-per-own-turn self pulse from the usual start-of-turn Regeneration Step to the completion of one actually legal paid Physical Action **during that turn**. It is a **timing substitution**, never a second pulse, extra action, free Guard/Dodge, weapon attack or automatic per-hit Rider. If no such action is completed, the normal regeneration-step timing applies; the choice must be locked before the first candidate trigger of that turn.
- **All L3 Authority-to-technique interactions:** the canonical Focus unlocks are retained, but the below Signature-specific Authority is **not automatically compatible** with Basic Heal, Guided Regeneration or any other ordinary technique. Individual L3 technique compatibility remains to be authored, with distinct VP and Destiny payment.

The purpose of these candidates is to expose the key action/trigger differences for review before assigning a complete level-by-level character build. No level-4–20 scaling table, signature-selection menu, or 48-Aspect coverage is introduced. HP is level-independent in the current rules; late-level relevance should first be evaluated as **percentage of Max HP and opportunity cost**, not by presuming automatic raw HP inflation.

## One Destiny Authority: Spare the Reserve (candidate)

**One exceptional modification of this same Signature**, not a separate spell or a metamagic catalogue. At a legal Signature pulse, spend **1 Destiny** (separate from normal VP) to restore up to the Focus's usual HP cap **without consuming the recipient's Vigor**. The available Destiny must cover the cost at the actual Authority activation. Restore `H = min(K, MaxHP - HP)`; recipient Vigor is unchanged. This is the only new effect; no additional target, action, pulse, wound repair, Dying exception, longer reach, Vigor creation, or stacking.

The Authority must be declared before resolution and cannot be used without a legal Signature target/trigger. It should not spend Destiny merely to heal a full-HP recipient. The currently proposed Destiny pool `2 + floor(Level / 5)` and interval recovery remain **provisional** under the foundation. One-pulse exception is finite because Destiny is finite; its numerical economy needs full day-scale calibration, particularly at high levels.

Ordinary **Basic Heal** remains a separate authored **2 × Used Tier VP** technique that restores modest HP **and restores Vigor**. **Guided Regeneration** remains a separate paid technique increasing throughput at the existing Step. Neither becomes free, and no paid VP technique is automatically an Anointed Signature or Authority host.

## Deterministic examples and refusal probes

All examples are candidate calculations, not existing native engine receipts.

| Scenario | Result |
|---|---|
| Fighter 12 HP maximum, currently 5 HP; 20 Vigor; High delivers normal 2-HP pulse | Fighter becomes **7 HP, 18 Vigor**; at next own Step, throughput **3** may independently restore **3 HP** at **3 Vigor**, ending **10 HP, 15 Vigor** (assuming no other changes). |
| Same before pulse, but High pays 1 Destiny for Spare the Reserve | Fighter becomes **7 HP, 20 Vigor**; subsequent Step restores 3 HP consuming 3 Vigor, ending **10 HP, 17 Vigor**. |
| Fighter 5/12 HP, only 1 Vigor, High normal 2-HP pulse | Exactly **1 HP** restored, **1 Vigor** spent; ends 6 HP, 0 Vigor. |
| Fighter 5/12 HP, 0 Vigor, High normal pulse | **0 HP** restored; no fabricated reserve, regardless of 2-HP ceiling. |
| Fighter 5/12 HP, 0 Vigor, High Authority paid | Can restore up to 2 HP if Destiny is available; **0** Vigor remains; no ongoing free restoration. |
| Recipient at 11/12 HP, 5 Vigor, High normal pulse | Exactly **1 HP** restored and **1 Vigor** consumed; no overheal or needless second Vigor spend. |
| Recipient 0 HP with an unfinished Serious wound | Baseline and Authority pulses **ineligible**; no HP, Repair Progress, stabilizing or Dying bypass. Basic Heal has its own existing bounded Dying procedure. |
| Medium invested patient leaves valid 0–3 square visibility/path | Investment is not an unrestricted remote-healing channel; no pulse until in range/path again. |
| Low L2 physical-action trigger after already gaining own start-of-turn pulse | **Rejected**: timing swap is once per own turn; no second pulse or automatic weapon-hit healing. |
| Non-Dying wounded patient | Direct HP may be restored subject to all limits, but **no Repair Progress**. |
| Full HP, any Focus | No restorative application and no legal paid Authority enhancement. |
| Forsaken bond | No Signature, Investment-based Anointed pulse or Destiny Authority. |
| External target refuses | Apply ordinary beneficial-bodily-Intrusion resistance and +8 barrier; do not label involuntary alteration beneficial to bypass it. |

## Acceptance gate and deliberately open decisions

1. **Authoritative story requirements:** extraordinary *joyful* celebration is valid because collective, successful and culturally reinforced Restoration practice culminated in exceptional Volition; tragedy and divine tasking are not prerequisites. One Imprint and broad non-prescriptive Mission must remain separate from Focus and Resonance.
2. **Gameplay distinction:** one Signature converter, High active AP; Medium one Invested patient and Step pulse; Low self embodiment and Step pulse; no three unrelated techniques, no selectable Imprint spell tree.
3. **Exact 0-VP safety:** all normal pulses conserve total `HP + Vigor` on the recipient until cap; no free stockpiled Vigor/HP, no free wound progress, no extra Step and no out-of-combat elapsed-time loophole. **Spare the Reserve** is a Destiny-limited intentional exception to that conservation.
4. **Real comparison required:** measure High healing/AP, Medium setup/availability, Low actual physical contribution and L2 trigger benefit against Basic Heal, Guided Regeneration, natural throughput, enemy damage, attrition and refusal conditions. Confirm medium/low event-based signatures are meaningful when outside initiative. Compare L1, L3, midgame and late levels before claiming long-term scaling.
5. **Not included:** canonical rule promotion, full Destiny validation, L3 paid-technique Authority compatibility, native turn/consent/overlap receipts, Medium hostile investment, complete L1–3 Anointed character sheets, independent Focus certification, out-of-initiative recovery clock and 48-Aspect production catalogue.
6. **Stop/go:** no player-facing numeric entitlement or roadmap completion count until separately reviewed effect promotion and genuine source-bound native and character-build verification.

### Source anchors

- [Anointed Foundation](../rules/08-archetypes/anointed.md) — surge, Mission states, Birth Imprint, Focus cadence, Signature 0 VP and provisional Destiny.
- [HP and Vigor](../rules/06-vigor-wounds-death/hp-and-vigor.md) and [Dying and Wounds](../rules/06-vigor-wounds-death/dying-and-wounds.md) — 1:1 natural conversion, throughput, wound repair and Dying gates.
- [Initiative and Round/Turn](../rules/05-combat/initiative-and-round-structure.md) — existing Regeneration Step and turn action costs.
- [Direct Veil Intrusion](../rules/07-veil-magic/resonance-and-intrusion.md) — bodily alteration, refusal and consent.
- [Basic Heal](../rules/07-veil-magic/basic-heal-v0.md) and [Guided Regeneration](../rules/07-veil-magic/guided-regeneration-v0.md) — independent paid Restoration techniques.
- [Aspect identities and boundaries](../world/aspect-identities-and-boundaries.md) — Restoration does not acquire Preservation, Nature, unrestricted resurrection, or additional techniques.
