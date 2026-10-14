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
| VP cost | **2 Spent VP** on an otherwise valid magical application, subject only to an eligible explicit discount; no Committed VP |
| Duration | **1 minute / 60 seconds of elapsed in-world time** following successful activation; temporary weakening, **no channel upkeep or reapplication pulse** |
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

**Pressure must exceed Resistance; a tie resists.** Apply the universal attended-object Imposition procedure, including conscious waiver and any independently authored object protection. **No Intrusion Barrier** is added; this is an Imposition on an object, not hostile Intrusion into a creature. An otherwise valid resisted application still **spends the 2 VP**. The spell does **not** additionally challenge the captive's body or grant another Strength contest at activation.

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

1. **Declare** an eligible restraint and `Touched Object` **Primary**, confirming contact, a legally available Full Action, character/Archetype access, and **at least 2 Available VP** (after only a genuinely applicable modifier). Confirm the target is not a magical restraint.
2. **Commit the Full Action** (the caster's entire Turn AP for this turn), then follow normal response and interruption ordering. Contact and eligibility must remain valid at application; the Full Action is not made interrupt-proof and does not automatically allow casting out of turn.
3. **At valid resolution** spend **2 VP** and resolve **one** applicable attended-object Direct Veil contest (if any). A resisted attempt still spends the VP; a declared action interrupted or made invalid **before** valid magical application costs the committed Full Action but **does not spend VP**.
4. **On success**, snapshot the caster's raw signed VC and the corresponding material reduction. The chosen restraint is **temporarily weakened for one minute**, starting at resolution. Re-evaluate the *ordinary* base break DC from real circumstances when a legal break attempt occurs; apply the **snapshotted material threshold** and `min`, not newly gained VC. No ongoing VP/Reaction/AP and no automatic recurring checks.
5. **Expiration / break:** After one minute, any **intact** restraint returns to its normal physical strength/break DC. A restraint physically broken during the window **stays broken**; the technique itself does not cause that physical break or leave permanent damage. The spell is a temporary property change, not a maintained Reserve, and **does not end early from caster unconsciousness** after successful activation. A fresh legal cast may start a new one-minute effect but multiple overlapping Weaken Restraints effects on the **same assembly do not stack**, add DC reductions, or make the timer indefinite. Use the **best (lowest) active adjusted DC**, subject to its own remaining expiry, if independent valid instances temporarily overlap; other restraints are independent.
6. **No mass release:** Each Full Action selects **one** restraint assembly and costs 2 Spent VP. Multiple casts are possible only with their actual actions/VP and separate timers. There is no general area-of-effect or one-action weakening of a prisonful of restraints.

**Duration handling:** The one minute is **60 seconds of actual elapsed in-world time**. It does not grant free actions during that period or a new round-speed conversion; use established scene/round time adjudication. The effect is established on completion (not delayed until a future physical break) and expires when that time elapses.

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
| Caster at 2 VP completes valid unopposed cast | **0 Available, 2 Spent**; effect lasts one minute |
| Valid contested cast fails | **2 VP Spent**, no weakened restraint |
| Cast interrupted before magical application | Full Action lost, **no VP spent** |
| More than one separate restraint | Only the selected **one assembly** affected |
| Caster knocked unconscious after successful activation | One-minute effect remains until expiry, unless separately suppressed |
| One minute elapses with restraint intact | Base physical break DC applies again; spent VP not refunded |
| A weakened restraint physically breaks before expiry | Remains broken after expiry; spell did not itself deal damage |
| High Scholar attempts to take Weaken Restraints as a Secondary | **No authored Secondary**, so cannot select it as a normally legal compositional Secondary |
| Gifted strong exemplar Disgust → Defiance | Matching emotion link supplies **Aspect access**, but still pays **Full Action and 2 VP**; no universal automatic spell acquisition |

## Design status

**v0 design locked:** Liberty / Defiance Tier-1 **`Touched Object` Primary**; touch **without free hand**, nonmagical restraint only, **Full Action**, **2 Spent VP**, **one-minute temporary reduction** using material **12/10/8 − signed VC** with **`min(original DC, …)`** so it cannot worsen breakability; attended-object Imposition resistance using Strength + Vitality and highest applicable non-waived defense; actual physical breaking remains separate. **No Secondary/Rider and no Tier multiplier**. Numbers, one-minute throughput and suitability for Low-Focus escape play are **provisional pending playtest**. B05's full eight-Pillar repertoire remains incomplete.
