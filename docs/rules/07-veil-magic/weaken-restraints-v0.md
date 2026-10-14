# Weaken Restraints v0 — Liberty / Defiance

> **Executable level 1–3 B05 technique; cost and DCs are locked as provisional v0 playtest values.** This touch-only **escape / exploration** technique weakens **one mundane physical restraint** rather than granting automatic escape. The canonical **Liberty / Defiance** Aspect is **Transform**; that metaphysical class does not itself select the technique's **direct Imposition** delivery. **Actual technique access still follows each Archetype.** The verified Strong Gifted configuration links **Disgust → Liberty / Defiance**, but that example does not grant every Gifted this particular link.

See [Aspect identities](../../world/aspect-identities-and-boundaries.md), [Technique Structure](technique-structure-v0.md), [Direct Veil Imposition](resonance-and-intrusion.md#imposition), [Core Resolution](../01-core-resolution/core-resolution.md), [Full Actions](../05-combat/action-categories-and-physical-tempo.md#full-action), [Initiative and Round](../05-combat/initiative-and-round-structure.md), and [Volition Points](volition-points.md).

## Identity and profile

| Field | Weaken Restraints v0 |
|---|---|
| Pillar / Aspect | **Liberty / Defiance**, canonical **Transform** |
| Base Tier | **1**; requires normal technique access |
| Used Tier | **T ≥ 1**, within universal ceiling; **no Tier-based numerical scaling** for v0 |
| Focus | **High / Medium / Low**; identical spell cost and **Full Action** requirement |
| Exact profile | **`Touched Object`** — **one** coherent nonmagical physical restraint |
| Components | **None**: **no free hand, gesture, implement or verbal component**; caster must remain conscious and capable of a legal Full Action |
| Physical contact | **Required at declaration and through valid activation**; contact by the caster's **bound body** is sufficient; no line-of-sight or free-hand requirement |
| Target / range | **Touch** one mundane restraint; not a creature, general loose material, a lock or a magical binding |
| Expression / interaction | **[Projection], direct Imposition** modifying the restraint's physical breakability; **not** Intrusion into the captive or Manifestation |
| Activation | **One Full Action on the caster's own turn**, requiring and consuming the entire Turn AP allotment; **not** a Reaction, free Interception or attack |
| VP cost | **Base 2 Spent VP**; at declaration compute and **lock the effective ordinary Spent VP cost** after any expressly eligible discount (e.g. **TAL-M03 — Frugal Technique** reduces it to **1 VP** on a qualifying own-turn cast). Pay that locked cost at valid application; no Committed VP |
| Duration | **1 minute (60 seconds) outside initiative**; in structured combat, **expires at Round Begin of the tenth subsequent round** after successful casting (casting round = R; expire at Round Begin R+10). **Technique-specific combat anchor only**, not a universal round-length conversion; no upkeep |
| Primary | Lowers the **DC of an otherwise legal physical Strength check to break the restraint**, using the material table and formula below |
| Contributions | **Primary only**; no Secondary, Rider contribution, or standalone High Scholar composite authorization |
| Damage / other effects | **None**; no HP/Vigor damage, free escape, unlocking, Disarm, release, extra action, object destruction or involuntary movement |

**Full Action remains Full Action at all Focus levels.** It is **not** High 20 / Medium 24 / Low 30 AP: those are ordinary **Projection Action** costs, which this technique expressly replaces. A caster restrained by their hands may still use the technique if they can touch the restraint with some part of their body and are otherwise capable of taking a Full Action. A specific independent condition that prevents actions or magic still prevents the cast.

## Eligible restraint and object-attendance boundary

A **restraint** here is a physical binding or fastening that actually prevents or restricts a creature's bodily freedom (or is a prepared component of that binding assembly), such as shackles/handcuffs, chain bindings, rope ties, cloth strips used as bonds, or ordinary binding vines/webs. Select **one functionally coherent restraint assembly**. A single pair of connected handcuffs may be one assembly; multiple unrelated chains, separately tied captives or independent anchors are **not** automatically one target. This definition does **not** convert an ordinary climbing rope, general textile, armor, weapon, door, lock, structural beam or other mundane object into an eligible restraint merely because breaking it would be convenient.

The selected restraint must be **nonmagical**: actively magical/enchanted shackles, magically sustained webs and magical bindings are ineligible. Its wearer being magical or its owner being a mage does **not** alone make an otherwise mundane restraint magical. The technique does not dispel effects, remove magical properties, defeat wards or open locks; a separately effective magical protection or immunity still applies under its own rule.

**Attended-object Imposition:** Like worn jewelry or a held weapon, a restraint is **attended** when actually worn, held, carried, gripped or under a creature's **immediate physical control**. The currently bound wearer can knowingly **waive their own Direct Veil Resistance**, including the self-bound caster. A captor **does not gain an attending-object defense merely from ownership, having tied the knots earlier or standing nearby**; they must currently qualify as physically attending the restraint. If an unwilling captor is actually holding one end of the target rope, or multiple creatures attend the same selected restraint, resolve **one Direct Veil contest using the highest applicable non-waived attending creature's resistance**, not a roll per creature. An unwilling bound wearer can decline to waive resistance even when the caster considers freeing them beneficial. An ordinary **unattended mundane restraint** generates **no inherent Direct Veil Resistance**.

This technique authors the necessary **attended-object defensive pair: Strength + Vitality**. When a contest is required, use:

```text
Direct Veil Pressure = d20 + raw signed caster VC + Intellect
                         + caster Veil Integration Bonus
                         + explicitly applicable modifiers

Direct Veil Resistance = 10 + attending creature Strength + Vitality
                           + attending creature Veil Integration Bonus
                           + Resonance + explicit modifiers
```

**Pressure must exceed Resistance; a tie resists.** Apply the universal attended-object Imposition procedure, including conscious waiver and any independently authored object protection. **No Intrusion Barrier** is added; this is an Imposition on an object, not hostile Intrusion into a creature. An otherwise valid resisted application still **spends the locked effective ordinary Spent VP cost** (base 2, or 1 with an applicable discount such as TAL-M03). The spell does **not** additionally challenge the captive's body or grant another Strength contest at activation.

## Break DC and material categories

First obtain the **original, currently applicable ordinary physical Strength-check DC** for actually attempting to break this restraint using the character's proposed method under [Core Resolution](../01-core-resolution/core-resolution.md). That DC is established from the **circumstances**, not a fixed universal object statistic. A physical break must remain feasible; this spell does not supply missing leverage, working limbs, tools or access to the restraint.

On successful magic, lower its break DC temporarily:

```text
Adjusted Break DC = min(Original Break DC, Material Base DC - caster raw signed VC)
```

| Physical restraint | Material Base DC | After magic |
|---|---:|---|
| Chain, shackles, metal bindings | **12** | `min(original DC, 12 − VC)` |
| Rope, cloth, fabric and similar fibers | **10** | `min(original DC, 10 − VC)` |
| Nonmagical vines, webs and similar organic entanglement | **8** | `min(original DC, 8 − VC)` |

**Never make it harder:** the `min` prevents an increased DC even when raw VC is negative, or when the original binding was already easily breakable. **Use raw signed VC** for this authored DC expression (as well as for any Direct Veil Pressure). **Do not substitute the standard VC × Level packet**, add Tier, or roll an extra magical Strength check. At high VC, a resulting very low DC follows the normal **routine/trivial check** convention if a physical break is truly possible; this is **not automatic freedom without a break action**. For composite/materially mixed restraints, use the **material of the binding's actual operative load-bearing component**. If several independent components must be broken, one spell does not weaken all of them; any separate restraint remains unaffected.

Examples assuming the original break DC and a viable Strength attempt:

| Restraint | Original DC | Caster VC | Adjusted DC |
|---|---:|---:|---:|
| Heavy metal shackles | 18 | +2 | **10** |
| Ordinary rope ties | 14 | +2 | **8** |
| Nonmagical web binding | 12 | +2 | **6** |
| Already-fragile cloth | 7 | +2 | **7** — never worsened |
| Heavy metal chain | 18 | −3 | **15** — no worse than 18 |
| Metal shackles | 18 | +12 | **0** — trivial only if physically breakable |

This spell does not itself roll Strength. **A later break attempt** is an ordinary legal physical action/check using:

```text
d20 + Strength + actually applicable Training/situational modifiers
  ≥ Adjusted Break DC
```

Use the ordinary action or time needed by the physical break attempt; **the Full Action used to cast is not also a free break attempt**. If the physical break is impossible from the creature's current position, a lowered DC does not magically give them the required leverage or ability to attempt it. Under pressure use an active roll; outside pressure, apply ordinary safe-time/Take 10/Take 20 and no-roll rules when their prerequisites actually hold.

## Timing, duration, and application

1. **Declare and lock the effective VP price:** Select an eligible restraint and `Touched Object` **Primary**; confirm contact, legal Full Action, Archetype access and a nonmagical target. Start from **base 2 Spent VP** and apply only reductions actually eligible at declaration, such as [TAL-M03 — Frugal Technique](../10-advancement/talents-level-1-5-v0.md#tal-m03--frugal-technique) on a qualifying character's **own turn**: 2 → **1 Spent VP** (minimum 1). **Lock that effective cost for this activation**; do not recompute it mid-response, apply unearned reductions, or allow the ordinary Spent component to reach zero. Require **Available VP ≥ locked effective cost at declaration**, before Full Action/AP commitment or any response window. An underfunded attempt is **illegal**, commits no Full Action/VP and creates no new response.
2. **Commit the Full Action** (the caster's entire Turn AP for this turn), then follow normal response and interruption ordering. Contact and eligibility must remain valid at application; the Full Action is not made interrupt-proof and does not automatically allow casting out of turn. The **locked effective Spent VP cost** cannot be reduced or silently raised by changing circumstances during the response window.
3. **Recheck at application:** After all applicable responses and legality checks, require **Available VP ≥ the same locked effective cost** again, because an intervening legal Reaction or other response can spend/commit VP. If now underfunded, or contact/target/action legality is lost before application, the attempt **fails without a magical application or resistance contest**; the already committed Full Action remains lost and **no technique VP are spent**. If still legal and affordable, move **exactly the locked effective amount** from Available → **Spent VP**, **before** resolving the **single applicable attended-object Direct Veil contest**. A valid cast **resisted by that contest still pays that exact amount**, never a hard-coded 2. A separate optional surcharge, such as [TAL-M02 — Volitional Calibration](../10-advancement/talents-level-1-5-v0.md#tal-m02--volitional-calibration) when its own conditions apply, remains separately payable by its own rule and is **not discounted or included** in the locked ordinary technique cost.
4. **On success**, snapshot the caster's raw signed VC and corresponding material reduction. The chosen restraint is temporarily weakened starting **at successful application**. **Outside initiative**, duration is **60 seconds of elapsed in-world time**. **During initiative**, record casting round **R**; it lasts for the rest of R and rounds **R+1 through R+9**, and expires **at Round Begin of R+10, before that round's refresh/start effects**, whether or not the original caster still has a turn. Re-evaluate the *ordinary* break DC from real circumstances when a legal break attempt occurs; apply the **snapshotted material threshold** and `min`, not newly gained VC. No ongoing VP/Reaction/AP and no recurring checks.
5. **Expiration / break:** At the applicable **60-second or explicit Round Begin** expiry, any **intact** restraint returns to its normal physical strength/break DC. A restraint physically broken during the window **stays broken**; the technique itself does not cause that physical break or leave permanent damage. The spell is a temporary property change, not a maintained Reserve, and **does not end early from caster unconsciousness** after successful activation. A fresh legal cast may start a new one-minute effect but multiple overlapping Weaken Restraints effects on the **same assembly do not stack**, add DC reductions, or make the timer indefinite. Use the **best (lowest) active adjusted DC**, subject to its own remaining expiry, if independent valid instances temporarily overlap; other restraints are independent.
6. **No mass release:** Each Full Action selects **one** restraint assembly and has **base 2 Spent VP**, reduced only by an eligible discount to the activation's locked effective cost. Multiple casts are possible only with their actual actions/VP and separate timers. There is no general area-of-effect or one-action weakening of a prisonful of restraints.

**Duration handling — two explicit timekeeping modes, local to this technique:** In exploration/non-initiative play, count **60 elapsed in-world seconds** from successful resolution. While initiative is running, use **ten Round Begin boundaries following the casting round**; record round R on application, and **expire at Round Begin R+10** (not Round End R+9, the caster's tenth turn, or a real-world stopwatch). This is a **specific v0 combat surrogate for the one-minute duration**, **not** an authoritative 6-second round or a general conversion rule for other spells. The effect remains active against eligible break attempts until its expiry boundary, even if the caster is unconscious, dead, no longer taking turns, or absent from initiative.

**Scene/initiative transitions — deterministic conservative rounding, local to Weaken Restraints:** The ordinary duration remains **60 elapsed in-world seconds outside combat**, and a fresh successful cast **during combat** still expires at **Round Begin R+10**. The existing initiative rules do **not** assign an exact duration in seconds to a partially completed combat round. Therefore an exact real-second translation at an arbitrary mid-round transition is **not available** without changing the global combat clock. This technique expressly uses a **round-down / no-extension policy** at each transition instead of silently treating fractional time as a full round:

- **Exploration → initiative:** If `s` **whole seconds remain** when initiative starts, compute **`q = floor(s / 6)` whole combat-round intervals** and a discarded remainder **`r = s mod 6`**, where **`0 ≤ r < 6`**. If `q = 0`, the effect **expires immediately at the transition**, before any combat action. Otherwise, if the first active initiative round is **R**, record the expiry as **Round Begin R+q**. The **`r` leftover seconds are deliberately lost, not rounded up or banked for an extra round**. Example: **37 seconds** remaining → **6** complete round intervals + **1 discarded second**, **expiry at Round Begin R+6**; **not seven rounds/42 seconds**.
- **Initiative → exploration:** If initiative stops during round **C**, and the active effect's scheduled expiry is **Round Begin E**, count the **future Round Begin boundaries** including its expiry: **`n = max(0, E − C)`**. The current, potentially incomplete round **C receives no extra remaining-time credit**. Set the exact noncombat countdown to **`s = 6 × max(0, n − 1)` seconds**; if `s = 0`, it expires immediately as initiative ends. Example: four future boundaries (round C+1 through C+4, expiry at C+4) → **18 seconds exactly**, **not an unspecified "up to 24 seconds"**. The leading current partial round is deliberately discarded, rather than granting six unearned seconds.
- **Round-boundary / repeated transition policy:** At the instant Round Begin **E** is reached, the instance expires before round refresh/start effects; do not convert an already expired effect. When initiative begins again, apply the **same floor** policy to the then-current noncombat seconds. Each transition operates on the **remaining** duration, **never resets** to 60 seconds or ten rounds. If the campaign records whole seconds only, floor any fractional out-of-combat remainder at transition rather than rounding up.

**Acknowledged tradeoff:** These conversions are **conservative approximations** and can **shorten** a remaining effect by up to **five whole seconds on entry**, and by **up to one current round's six-second budget on exit**. Repeated crossings may shorten it further. They **never intentionally extend** the effect; the price is that "one minute" is exact **within continuous noncombat play** and ten Round Begin boundaries are exact **within continuous initiative**, but a switch of timekeeping may end it **slightly early**. The six-second accounting unit is **solely for this one effect's transitions** and creates **no global seconds-per-round rule**. Track each active restraint instance and its expiry separately.

## v0 regression matrix

| Test | Required result |
|---|---|
| High, Medium or Low Focus caster | **Full Action**, all currently available Turn AP; **2 Spent VP**; no per-Focus Projection Action substitute |
| Level 1 with Veil Affinity +0 | Max VP High **6**, Medium **4**, Low **2**; **all can pay 2 VP** from full Available pool |
| Character has hands tied behind back and wrists contact mundane cuffs | Valid **without a free hand** if conscious and otherwise capable of a legal Full Action |
| Character immobilized so cannot take actions | **Not a valid cast**, even if touching the restraint |
| Mundane restraint physically touched but completely out of sight | **Eligible**; touch rather than sight is required |
| Ordinary climbing rope / door / lock | **Not eligible** merely because breaking would be useful |
| Actually magical shackle or magically sustained web | **Ineligible**; no dispelling or ward bypass |
| Self-bound wearer willingly waives magical defense | No attended-object Direct Veil contest from their own waived defense |
| Unwilling bound wearer | Normal attended-object Direct Veil contest with **Strength + Vitality** |
| Unwilling captor physically holding rope while wearer waives | Captor supplies **attended** defense, using highest non-waived resistance |
| Captor who tied restraint earlier but is now merely watching | **No extra attending defense** solely for ownership or earlier tying |
| Two unwilling creatures holding same restraint | **One** highest Direct Veil Resistance contest; no per-holder magical rolls |
| Unattended mundane restraint | **No Direct Veil Resistance** by default |
| Magic succeeds on tied/worn restraint | Temporary **break DC** reduction; no free untying, automatic break or additional escape check |
| Heavy metal original DC18, VC+2 | Adjusted DC **10** |
| Rope original DC14, VC+2 | Adjusted DC **8** |
| Web original DC12, VC+2 | Adjusted DC **6** |
| Already loose cloth original DC7, VC+2 | Remains **DC7**; spell cannot worsen it |
| Signed VC −3 on metal original DC18 | **DC15** rather than DC18 or a worse result |
| Cast on restraint with an existing effect | No additive weakening or unbounded stacking |
| Character cannot physically produce a break attempt | Lowered DC does **not** itself enable a physically impossible break |
| Caster at 2 VP completes valid unopposed cast without a discount | **0 Available, 2 Spent**; outside initiative lasts **60 seconds**, or in combat through Round Begin **R+10** |
| Level-3 caster with **TAL-M03**, base 2 VP, exactly **1 Available VP** at declaration | Legal on own turn; **lock cost 1**; valid application spends **1 VP**, not 2 |
| TAL-M03 declared, 1 VP at declaration and still 1 at application; attended target resists | Valid Imposition contest fails; **1 VP Spent**, not 2; Full Action spent |
| TAL-M03 not eligible or already used; caster has only 1 Available VP | **Illegal declaration**; no Full Action, VP expenditure or response window |
| Cost **1** locked legally; a response spends caster's last Available VP before application | **Application cancelled**: Full Action lost, **0 technique VP Spent**, no Imposition contest or weakening; do not charge 2 |
| Cost **2** locked with ≥2 VP on declaration; an intervening response leaves only 1 Available VP | **Application cancelled**: Full Action lost, **0 technique VP Spent**; no automatic discount or downgrading to 1 |
| TAL-M03 discounted cost locked at 1; caster's Available VP rises to 2 before application | Pay **1 VP** as locked, not original base 2 |
| Valid contested cast fails **without discount** | **2 VP Spent**, no weakened restraint |
| Cast interrupted before magical application | Full Action lost, **no VP spent** |
| More than one separate restraint | Only the selected **one assembly** affected |
| Caster knocked unconscious after successful activation | One-minute effect remains until expiry, unless separately suppressed |
| Outside initiative, 60 elapsed seconds with restraint intact | Base physical break DC returns; **Spent VP not refunded** |
| Cast during combat in round **R**, no interruptions to initiative | Maintained through remaining R and rounds **R+1…R+9**; **expires at Round Begin R+10** before new round refresh/actions |
| Caster incapacitated or removed from initiative after casting in R | Expiry still at **Round Begin R+10**, not indefinitely delayed until their next turn |
| Spell cast out of combat with **37 seconds remaining** when initiative starts in round **R** | **floor(37/6) = 6**, discard **1 second**; expires at **Round Begin R+6**, not R+7; conservative shortening is explicit |
| Spell cast in combat, **4 future Round Begin boundaries** remain and combat ends in current round **C** | Exit conversion: **6 × (4 − 1) = 18 seconds exactly** outside initiative; discard potential remainder of C, not an unspecified 24-second allowance |
| Enter initiative with **5 seconds remaining** | **floor(5/6) = 0**; effect expires immediately rather than extending into a six-second interval |
| Enter initiative with exactly **6 seconds remaining**, new round R | One whole interval; expires at **Round Begin R+1** |
| End initiative with only **one** future Round Begin boundary to expiry | **6 × (1 − 1) = 0 seconds**; expires immediately, no fractional mid-round bonus |
| Go back to exploration and later re-enter initiative | Count down the actual remaining **seconds**, floor them on re-entry; **never refresh** the 60-second timer |
| Spell's break DC would be automatically easy but no physical break is feasible | No automatic freedom, still requires **legal separate physical attempt** |
| A weakened restraint physically breaks before expiry | Remains broken after expiry; spell did not itself deal damage |
| High Scholar attempts to take Weaken Restraints as a Secondary | **No authored Secondary**, so cannot select it as a normally legal compositional Secondary |
| Gifted strong exemplar Disgust → Defiance | Matching emotion link supplies **Aspect access**, but still pays **Full Action and 2 VP**; no universal automatic spell acquisition |

## Design status

**v0 design locked:** Liberty / Defiance Tier-1 **`Touched Object` Primary**; touch **without free hand**, nonmagical restraint only, **Full Action**, **base 2 Spent VP** (lock an eligible discount at declaration, verify affordability again at application, spend exactly locked cost), **one-minute temporary reduction** (60 seconds outside initiative; expire at **Round Begin R+10** for a combat cast) using material **12/10/8 − signed VC** with **`min(original DC, …)`** so it cannot worsen breakability; attended-object Imposition resistance using Strength + Vitality and highest applicable non-waived defense; actual physical breaking remains separate. **No Secondary/Rider and no Tier multiplier**. Numbers, one-minute throughput and suitability for Low-Focus escape play are **provisional pending playtest**. B05's full eight-Pillar repertoire remains incomplete.
