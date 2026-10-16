# Guided Regeneration v0 — Life / Restoration

> **Executable Tier-1 design with PROVISIONAL VP and one-minute duration calibration.** Guided Regeneration increases **existing natural regeneration throughput by exactly +1** during the beneficiary's normal Regeneration Step. It never creates a new step, restores Vigor, changes the 1 Vigor per HP/Repair Progress conversion, or bypasses Dying/wound restrictions. The caster chooses **either** a fixed-duration **Spent VP** mode or a continuously maintained **Committed VP** mode at activation. Only the maintained mode is eligible for Priest Consecration/Devotional Rite. This entry is not automatic technique acquisition. See [Life Aspect boundary](../../world/aspect-identities-and-boundaries.md#life), [HP and Vigor](../06-vigor-wounds-death/hp-and-vigor.md), [Dying and Wounds](../06-vigor-wounds-death/dying-and-wounds.md), [turn procedure](../05-combat/initiative-and-round-structure.md), [Technique Structure](technique-structure-v0.md), [Direct Veil Intrusion](resonance-and-intrusion.md#intrusion) and [Priest](../08-archetypes/priest.md).

## Identity and profile matrix

| Property | Guided Regeneration v0 |
|---|---|
| Pillar / Aspect | **Life / Restoration**, canonical Transform Aspect |
| Base Tier / current executable Used Tier | **Tier 1 only**. Higher Used-Tier effects are **not authored**; L3 Tier-2 ceiling or a Miracle Petition does not invent an upcast. |
| Access | Chosen-Pillar **Prepared Prayer** for Priest; individually known for Scholar; Gifted/Anointed require their ordinary real Aspect access. No automatic acquisition from this document. |
| Exact recipient profiles | `Single Target`: one eligible **living creature** (including caster); `Self`: **caster only**, 0 range. These are exact identifiers, not implicit composite permissions. |
| Contribution | **Primary only**; no Secondary or Rider contribution, no independent repeating Rider |
| Interaction | **Beneficial bodily Intrusion**. `Single Target` is [Projection]; `Self` is explicitly **Inward, [Embodiment], Regeneration channel** and may be used as a Devotional Rite in maintained mode. |
| Ordinary activation | **One Projection Action** on caster's own turn: High **20 AP**, Medium **24 AP**, Low **30 AP**, for **either** mode |
| Fixed-duration mode | **2 Spent VP**, one minute maximum; **no Committed VP** |
| Maintained mode | **2 Committed VP**; persists while its reservation and conditions remain valid; **no Spent VP** |
| Benefit | **+1 throughput** at beneficiary's **existing once-per-own-turn Regeneration Step** only, subject to its usual restrictions and available Vigor |
| Duration/cadence | **Continuous modifier**, never a regeneration event; see exact expiry below |
| VC / Tier / Accord effect scaling | **No numerical scaling** in v0. Neither positive Veil Control nor Pillar Accord multiplies recurring throughput or changes conversion. |
| Stacking / instance cap | **No stacking** between applications or modes. **One active Guided Regeneration instance per caster**; one recipient receives at most **+1** total from Guided Regeneration even from different casters. |
| Additional capabilities | **None**: no extra Vigor/HP, immediate repair, free healing, additional step, temporary HP, regeneration efficiency, automatic stabilization or resurrection |

### Range and recipient acquisition

For the `Single Target` profile, maximum **3 direct 3D square-equivalents** (nominally 4.5 m along one axis) from caster to recipient. For this technique alone, take absolute grid offsets `dx,dy,dz`; sort to `a >= b >= c` and calculate **`a + 0.5*b + 0.5*c`**. Retain fractions: `(2,2,0)` is 3 and eligible; `(3,1,0)` is 3.5 and ineligible. Use square centres for one-square creatures; for a larger footprint use the fixed map-reference occupied square already recorded for each participant, or the lowest-x then lowest-y then lowest-z occupied square if absent. Do not choose the nearest occupied cell after seeing a result. This is **not a new global targeting metric**.

A non-self recipient must be **directly visible** and reachable through **one unobstructed straight magical delivery line through open air** at declaration and application. A solid wall, closed door or solid glass blocks the line, even if visible through glass. An open passage may qualify. `Self` needs neither outward sight nor an outward path. The effect **follows its living recipient** once established; range/sight are **not** continuously checked. Reassignment and Intercession have their own fresh eligibility checks.

A genuinely beneficial recipient who does not oppose the effect has no Intrusion contest, including an **unconscious** recipient without a still-effective prior refusal. A consciously resisting recipient or one with an applicable surviving refusal uses the ordinary **+8 Intrusion Barrier**. When contested, this technique uses **Intellect** for caster Shaping and **Vitality + Awareness** for target defense, with the shared Direct Veil Pressure/Resistance, Resonance and integration rules. Tie resists. These Ability assignments are **v0 calibration**, not a new universal healing save.

## Two exclusive payment and duration modes

The caster chooses one mode at declaration. Modes change **resource handling and duration**, **not throughput magnitude**. A maintained effect cannot be converted to fixed duration, or vice versa, without ending it and making a fresh paid activation.

### A. Fixed-duration cast — 2 Spent VP

- The **base** fixed-mode price is **2 Spent VP**. Apply only an otherwise eligible **ordinary Spent-VP discount** at declaration (e.g. [TAL-M03 — Frugal Technique](../10-advancement/talents-level-1-5-v0.md#tal-m03--frugal-technique), minimum 1 VP), and **lock the effective price before responses**. Check that Available VP covers this **locked** cost at declaration and again at application. Move **exactly the locked effective price** from Available to Spent on every legally attempted magical application, including a contested application that is resisted. If interruption/target loss prevents any magical application, pay no VP but committed AP remain lost. A legally declared TAL-M03 use is consumed immediately on declaration even if a later interruption prevents spending VP; it is not restored on a failed or resisted attempt.
- The successful effect lasts **up to 60 elapsed seconds outside initiative**, or expires **at Round Begin R+10** if activated during combat round R (before anyone takes a turn in that new round). Earlier removal, target death, or magical dispelling can end it.
- **Exploration → initiative (technique-local conservative conversion):** With **s whole elapsed-time seconds remaining**, set **q = floor(s / 6)** and discard the remainder (any fractional second is also rounded down). If **q = 0**, expire immediately at transition; otherwise, if the first initiative round is **R**, expire **Round Begin R+q**. Example: **37 seconds** remaining → **q=6**, expires **Round Begin R+6**, not R+7.
- **Initiative → exploration (technique-local conservative conversion):** If initiative ends during round **C** with a scheduled expiry at **Round Begin E**, count **n = max(0, E−C)** future Round Begin boundaries, including the expiry boundary. The current partial round earns no remaining-time credit. Set the exact out-of-combat countdown to **s = 6 × max(0, n−1) whole seconds**. If **s = 0**, expire immediately. Example: **E=C+4** → **n=4** → **18 seconds**, not an uncertain 24. An instance already expired at Round Begin E cannot be converted.
- **Repeated transitions:** Apply those floor conversions to **remaining** time only; never restart a full minute or ten-round window, bank a discarded remainder, or gain extra duration by crossing the boundary again. These conservative conversions may **shorten** the effect, but never intentionally extend it. The factor of six is **local to this technique**, not a global initiative-round duration. While staying in one timing mode, the original **60 seconds** or **R+10** expiry remains exact in that mode.
- Once successfully applied, the effect is **independent of a caster-held VP channel**: the caster moving away, becoming unconscious or dying does not itself remove it; recipient death still ends the effect. Releasing/dismissing the fixed-duration effect **never refunds Spent VP**.
- **Not** an Active Consecration or a Devotional Rite. Cannot be Reassigned as one; does not receive the Chosen Devotion commitment reduction or Exaltation.
- Its fixed duration is **not a new regeneration cadence**. Ten rounds do not necessarily give ten useful Regeneration Steps: the recipient must have an actual step while the effect is live.

### B. Maintained reserve — 2 Committed VP

- On **successful application only**, move **2 Available VP -> Committed VP**. Unsuccessful resisted or interrupted activations never establish a reservation; their paid AP still remain spent.
- Remains active **without a time cap** while the originating caster maintains that commitment and the recipient remains living. There is **no upkeep AP/VP**, finite Pulse or per-turn recast.
- The caster's **unconsciousness alone does not end** the maintained pattern: its +1 may still assist the recipient's normal Dying Regeneration Step. The caster's **death**, intentional own-turn release, loss of the underlying maintained effect through applicable suppression, or recipient death ends it. On end, still-Committed VP returns to Available VP under the ordinary reservation rules; no retroactive recovery/VP refund arises for completed steps.
- Only this mode is expressly **Consecration-compatible** when used by a Medium Priest or **Devotional Rite-compatible** when a Low Priest prepares the `Self` profile. No generic Scholar Inward Boost/reroute, Low Scholar Active Embodiment, Gifted Conduit, or Anointed Signature permission is created just from those tags.
- **Chosen Devotion:** if an eligible Low Priest selects `Self` Guided Regeneration as the prepared Chosen Devotion, the existing **-1 Committed VP, minimum 1** reduces **2 -> 1 Committed VP** on the maintained activation. The fixed-duration 2 **Spent** VP mode receives no such reduction. A Low Priest with Veil Affinity +0 has Max VP 2 at L1, so can reserve 1 and retain 1 Available. Exaltation requires **later authored compatible properties**; none is granted here.

Both modes can be voluntarily dismissed at a normal **own-turn zero-action decision point**, but not as a new reaction/interrupt. One caster must end any previous Guided Regeneration instance **before** establishing a replacement in either mode; an old fixed-duration cast may be dismissed with no VP refund. Another caster's active instance on the same recipient does **not** raise the throughput bonus beyond +1, and maintaining the redundant cast grants no further healing. No replacement, dismissal, reassignment, recast or change in beneficiary creates a second regeneration step or refreshes any already-resolved output.

## Regeneration resolution

At the **recipient's normal Regeneration Step** (before start-of-turn hazards), if the effect is active and the step is allowed, calculate:

```text
Baseline throughput = max(recipient Vitality, 0) + recipient Focus Rate
Otherwise applicable throughput = baseline + other eligible throughput modifiers
Guided throughput = otherwise applicable throughput + 1 (if not already benefiting from Guided Regeneration)
```

High / Medium / Low recipient Focus Rates remain **1 / 2 / 3**. **Recipient** statistics, not caster statistics, control throughput. **Preserve all otherwise applicable bonuses and reductions**, including the separate **+1 from [TAL-C02 — Enhanced Regeneration](../10-advancement/talents-level-1-5-v0.md#tal-c02--enhanced-regeneration)**. For example, **Vitality +1, High Focus** supplies baseline **2**; TAL-C02 makes it **3**, and Guided Regeneration makes it **4**. The restriction applies **only to additional Guided Regeneration copies**, not independent throughput modifiers. Each modifier and any suppression still obeys its own specific rules; this formula does not override regeneration suppression or create a new global modifier priority.

- Each point actually used still consumes **1 recipient Vigor** for **1 HP restored** or **1 Repair Progress** under the existing rule. The extra point itself restores nothing and adds no Vigor.
- A **non-Dying** recipient may split eligible throughput between HP and repairable wounds by the existing player-controlled allocation. Unused throughput is lost at that step, not stored.
- A **Dying** recipient must first use the existing **survival-first** procedure (including the possible 1-point cancellation of the default Dying HP loss), then oldest unfinished repairable wound first, then HP only when all recovery-blocking wounds are complete. Guided Regeneration does **not** heal Irreparable/Fatal wounds or bypass another unfinished wound.
- If the recipient has **0 Vigor**, no usable throughput is created. If regeneration is fully suppressed, +1 **does not bypass** suppression. Apply specific partial throughput reductions normally; the +1 is part of the available throughput, not an independent uncancellable step.
- **No immediate/extra Regeneration Step** occurs on activation, reassignment, Intercession, start/end of a cast, entering/leaving initiative or voluntary release. Outside initiative there is no invented round-by-round or minute-by-minute HP/Repair Progress recovery; use only other **already authorized** regeneration/recovery procedures.
- Does not accelerate elapsed-time **6-hour Vigor Recovery**, alter Maximum HP/Maximum Vigor, mitigate damage, prevent Vigor burn, or interact with poison without separately authored rules.

The +1 is a **Continuous throughput modifier**, not a free repeated healing Rider and not a separately paid healing packet. This v0 provides **no Secondary or Rider contribution** and authors no High Scholar Composite pairing merely because the `Self`/`Single Target` keys happen to match another technique.

## Medium Priest — maintained Consecration only

An eligible Medium Priest with **Guided Regeneration prepared** may activate the maintained `Single Target` (or `Self`) profile as **one Active Consecration** using the normal Projection Action and **2 Committed VP**. Level 1–3 Priests can normally maintain **at most one Active Consecration** across all techniques.

**Reassign Consecration:** During the caster's own turn, pay one **24-AP General Tempo Action** and choose another legal living recipient within this technique's **3-square local range, sight and unobstructed path**. On a valid, accepted transfer, move the **existing maintained instance** to that recipient with its same VP commitment, duration and Continuous cadence. The prior recipient loses +1 immediately; the new recipient receives +1 only at their **next otherwise legal Regeneration Step**. There is no additional activation cost, new healing packet or regenerated resource.

If the new recipient has a relevant Intrusion refusal, resolve the technique's ordinary Intrusion contest for the new direct beneficiary. If target eligibility fails or resistance holds, the **24 AP is still lost**, and the existing Consecration remains on the original recipient. No VP are newly Spent or Committed for that failed transfer. You cannot reassign a fixed-duration cast.

**Level-3 Intercession-compatible trigger (provisional 2 Spent VP):** When **another** valid recipient is about to resolve their normal Regeneration Step, the Priest can spend **one Reaction + the existing 2 Spent VP benchmark** to apply the +1 to **that one imminent Step**, provided the Consecration is already active and this technique's range/sight/path and recipient Intrusion requirements hold at the trigger. The original beneficiary retains the normal effect; the Intercession beneficiary does not become a second ongoing recipient. No step is moved forward or repeated, and no additional +1 stacks if that recipient already has Guided Regeneration. The expenditure does not refresh prior throughput; if no regeneration can occur, no healing is generated. Normal Reaction/VP affordability and interruption/resistance procedures remain applicable. This does not grant an out-of-turn projection cast.

## Activation and termination procedure

1. **Declare:** Confirm the technique is legitimately known or prepared; choose one exact recipient profile **and one exclusive payment mode**; validate the recipient, range/sight/path, AP, mode-specific VP, instance cap, and legal action timing. For fixed mode, apply only specifically eligible **ordinary Spent-VP** discounts and **lock the effective price** (normally 2, or 1 with an eligible one-VP discount) before responses. For maintained mode, the normal commitment is 2, except the actual Low Priest Chosen Devotion discount to 1. Insufficient Available VP for the **locked price** makes the declaration illegal without opening a response window. An eligible **TAL-M03** use is consumed on legal declaration, even if application later fails.
2. **Commit AP and resolve responses:** Pay one Focus-priced Projection Action (High **20**, Medium **24**, Low **30**), then process ordinary Interceptions/Reactions, interruption and recipient changes. This action does **not** grant a free self-recovery Step or a Reactive cast.
3. **Recheck:** At actual application after responses, recheck eligibility, caster capability, the recipient still living, range/path (unless `Self`), **Available VP against the previously locked effective price** and non-stacking/instance rules. If the spell was interrupted or the application became illegal before it could be attempted, no VP become Spent/Committed and paid AP remain lost (any legally selected TAL-M03 use remains consumed).
4. **Beneficial Intrusion:** An unopposed genuinely beneficial application succeeds without a contest, including an unconscious beneficiary without applicable prior refusal. If the beneficiary actively resists or has a surviving refusal, use the authored Direct Veil contest (+8 barrier). For **fixed-duration mode**, spend **exactly its previously locked effective Spent-VP price** (normally 2; **1 if legally discounted**) upon a legal magical application **whether unopposed or resisted**. For **maintained mode**, establish only its locked VP commitment on success; a resisted application creates no ongoing commitment. Both consume their already-paid AP.
5. **Establish:** If successful, either (A) register the fixed-duration expiry and no VP channel, or (B) lock the effective maintained VP commitment and its caster/recipient endpoints. The +1 applies solely to future normal recipient Regeneration Steps until the instance actually ends. Subsequent legal release, death, suppression, replacement and duration expiry follow the selected mode above.

## Worked examples and regression cases

| Case | Expected result |
|---|---|
| VA +0 L1 High / Medium / Low normal fixed cast | **20 / 24 / 30 AP**, **2 Spent VP** in all cases; expiry after one minute; no refundable commitment |
| VA +0 L1 High / Medium / Low ordinary maintained cast | **20 / 24 / 30 AP**, **2 Committed VP**, not Spent; one continuous instance, ordinary release refunds the still-committed 2 |
| VA +0 L1 Low Priest selects maintained `Self` as Chosen Devotion | **1 Committed VP**, not 1 Spent; other **1 Available VP** remains. Fixed mode stays **2 Spent** |
| Recipient Vitality +1: High / Medium / Low baseline throughput, no other modifiers | **2 / 3 / 4**; active Guided Regeneration yields **3 / 4 / 5** |
| Recipient Vitality +1, High Focus and TAL-C02 Enhanced Regeneration | Baseline **2** + TAL-C02 **1** + Guided Regeneration **1** = **4** throughput; two Guided copies still give only **4** |
| Recipient missing HP 5; Vigor 1; throughput otherwise 2 | Can spend **at most 1 Vigor** to restore **at most 1 HP**; +1 creates no free energy |
| Non-Dying recipient has both HP loss and unfinished repairable wound | Player may allocate the additional throughput to **HP or Repair Progress**, spending Vigor at ordinary 1:1 |
| Dying recipient with two unfinished wounds | Use survival cancellation and **oldest unfinished repairable wound first**; no HP before all blockers are cleared |
| Dying recipient has Irreparable injury | +1 may support eligible survival/other repairable wounds where possible; cannot reconstruct/bypass Irreparable recovery block |
| Recipient at 0 Vigor or fully suppressed | **0** extra HP/repair; no independent tick or free conversion |
| Spell cast after recipient's Regeneration Step this turn | **No retroactive +1**; earliest benefit next normal Step |
| Fixed spell activated in round R | Expires **Round Begin R+10** at latest; cannot supply throughput in round R+10 |
| Fixed spell cast out of initiative, then initiative begins | **37 whole seconds** remaining → **floor(37/6)=6**; if first round R, expiry **Round Begin R+6**; 1 second discarded |
| Fixed spell leaves initiative mid-round C with expiry Round Begin E=C+4 | Count **n=4** future boundaries, then **6×(4−1)=18 whole seconds** remaining in exploration; no credit for partial round C |
| Fixed spell leaves initiative with only E=C+1 remaining | **n=1**, conversion gives **0 seconds**, expires at transition |
| Fixed spell enters initiative with only 5 seconds left | **floor(5/6)=0**, expires immediately, not one extra round |
| Fixed spell exits and re-enters initiative | Each transition floors **remaining** time; never extends/restarts original duration |
| Maintained caster knocked unconscious | Committed VP remain and benefit may assist Dying; no free reactivation |
| Maintained caster dies | Maintained pattern ends, reservation releases; no resurrection |
| Fixed-mode caster dies | Fixed spell remains for its unexpired term while recipient lives, absent dispelling |
| Target walks behind wall after application | Ongoing benefit remains; fresh Reassign/Intercession still needs target eligibility |
| Two different casters bless one recipient | **Total bonus +1, never +2**; no VP refund from redundant effect |
| Same caster wants to switch Spent to Committed mode | Must end old instance at legal own-turn decision point, pay new action and VP; spent cost never refunded |
| Level-1 Medium Priest reassigns maintained Consecration | **24 AP**, legal new recipient, existing 2 VP reserve; no extra step or copied effect |
| Failed reassignment/resisted new recipient | 24 AP lost, original Consecration stays; no extra VP charge |
| L3 Medium Priest uses Intercession for other's imminent normal Step | **1 Reaction + 2 Spent VP**, temporary +1 for that Step only; no second Step or extra ongoing target |
| Intercession beneficiary already has Guided Regeneration | No additive throughput; spent VP/Reaction do not grant second effect |
| Candidate tries to upcast at level 3 | **No enhanced T2 profile authorized** by v0; T2 ceiling alone does not scale throughput |
| Positive Priest Accord or high Veil Control | Still **exactly +1**; no per-round multiplicative bonus |
| TAL-M03 discounts an eligible fixed cast; target resists | Lock **1 Spent VP** at legal declaration, consume the TAL-M03 use then, and spend **exactly 1 VP** upon valid resisted Intrusion; 20/24/30 activation AP is still lost |
| TAL-M03 declared on fixed cast; interruption prevents application | Talent use consumed on legal declaration; **0 Spent VP** if no application can occur; paid AP lost |
| Talent discounts 1 ordinary Spent VP | Only an expressly applicable Spent discount can affect fixed mode's **locked effective price**; it cannot reduce 2-VP maintained commitment or Chosen Devotion's separate math |
| Technique is merely known by a Scholar | No automatic Medium Scholar reroute, Low Scholar Active Embodiment, or composite pairing solely from matching labels |
| Outside initiative for 6 hours | **No invented Regeneration Steps**; existing Vigor Recovery timing remains unchanged |

## Open calibration and explicit deferrals

- **2 Spent VP / one minute versus 2 Committed VP / continuous**: verify role distinction, long-term maintenance, resource scarcity and L1–3 encounter utility with actual combats.
- **+1 per actual Regeneration Step**: confirm useful for Low Devotion without making larger immediate heals or protection redundant; measure net **Vigor spent**, not just theoretical additional throughput.
- **Level-3 Intercession 2 Spent VP** may be too costly for +1 throughput; retain current Priest benchmark and test before changing universal Intercession pricing.
- A distinct **Tier-2/3 profile/upcast**, any compound/restoration specialization, **Low Priest Exaltation property**, Scholar Routing/Embodiment compatibility, other Archetype-specific expression and extended out-of-combat healing rules remain **unauthored**.
- **No changes** to Prepared Prayer counts, starting Accord, general VP Recovery, regeneration priorities, Direct Veil procedure, or global time/targeting rules.
