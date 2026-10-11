# Protective Intervene v0 — Reactive and Prepared Protection

> **LOCKED native protective-response foundation / interaction calibration watch.** A character can protect another creature from **one declared incoming attack** through **Shield Guard** or **Body Take Hit**, using either a **spontaneous Reaction** from a legally reachable position or a **precommitted Movement Interception** that reaches a protective position. The protective action is declared **before the attack roll**; it does not grant an additional Attack, Dodge, Guard use, movement step, or automatic Interrupt. See [Initiative and Round/Turn Procedure](initiative-and-round-structure.md), [Movement Foundation](movement-foundation.md), [Defensive Responses and Criticals](defensive-responses-and-criticals.md), and [Unified Firing Lane v0](unified-firing-lane-v0.md).

## Purpose, trigger, and physical eligibility

**Protective Intervene** is the name of the **protection** rule, not a replacement for Veilbound's existing **Interception** timing mechanic.

An eligible protector may commit to defending **one named other creature** against **one specific incoming attack** that has been **declared but not yet rolled**. A character must reasonably perceive the threat (sight, warning, or another actual source of awareness), be capable of using the chosen shield or bodily position, and possess the requisite Reaction **or** valid prior movement reservation. Mere adjacency, an abstract Reach score, friendship, or being in melee does not guarantee that an attack path can be reached.

The protector must be able to place **a usable shield or their body across that particular attack's actual approach path**, with believable facing/angle, size, reachable exposure, and positioning. A shield behind the intended target, a solid barrier separating the protector from the trajectory, an unusable shield arm, or an unreachable attack path defeats eligibility. For ordinary grid play, **adjacent or already along the lane** is the default scale; a nonadjacent protector needs an independently legal prior repositioning, not an extended invisible reach. No protector may end movement in an allied-occupied square contrary to [Movement Foundation](movement-foundation.md#occupied-squares).

For a declared multiattack **Attack Sequence**, one Protective Intervene affects **one specified individual attack**, not the entire sequence. It must be committed **before the roll of that attack**, with normal target/weapon/profile declarations and preassigned defenses retained. Each individual attack is its own trigger occurrence; no choosing which one to protect after seeing an attack result. **At most one protector** can apply Protective Intervene to a given attack. Normal physical cover and incidental Living Screen protections remain separate.

**Eligibility boundary:** The baseline covers attacks with a physically interceptable strike, weapon, or projectile. It does not redirect Direct Veil Intrusion, an already-resolved area effect, environmental hazard without an individually interceptable attack, a path the protector cannot physically reach, or a phenomenon a shield/body cannot intercept. Whether a particular Manifestation has a physically interceptable projectile is determined by its authored delivery, not merely its magical origin.

## Two activation routes: Reactive or Prepared

| | **Reactive Intervene** | **Prepared Intervene** |
|---|---|---|
| Preparation | None | Reserve **Movement Interception** with named ward and meaningful trigger on own turn |
| At triggering attack | Spend **one Reaction** before roll | Release already committed reserved MP; do **not** spend Reaction |
| Position | Must already be able to reach the attack path; **zero free MP** | Must complete **at least one legal movement step** and reach the attack path |
| Protection choice | Declare Shield Guard or Body Take Hit before roll | Choose Shield Guard or Body Take Hit **when reserving** |
| Normal defense expense | Shield spends one normal Guard use **only if used**; Body accepts the actual hit | Same; no extra Guard capacity and no new Take Hit pool |
| Opportunity Response | Cannot newly activate after this Reaction has been spent | Reaction stays available, subject to other independent uses |
| If attack misses | Reaction stays spent; no incoming hit to transfer | MP reservation is already released/consumed; no incoming hit to transfer |

### Reactive Intervene — spontaneous Reaction

When a specific attack against another creature is declared, the protector can spend their **available Reaction** in the attack's **spontaneous response window**, before that attack's roll, **only if** they already have the physically necessary protective position and method. Declare the intended ward, specific incoming attack, and **Shield Guard** or **Body Take Hit** immediately. The Reaction is **committed and spent even if the attack later misses, fails, is cancelled, or strikes cover**. There is **no free step, square, repositioning, or new protective Guard capacity**.

Reactive Intervene competes with [Opportunity Response](initiative-and-round-structure.md#opportunity-response) for the **same once-per-round Reaction**. An already spent Reaction cannot be spent again on Reactive Intervene; conversely a Reactive Intervene Reaction cannot subsequently activate Opportunity Response that round. Defensive Guard/Dodge selected **for oneself** do not otherwise spend a Reaction and are not prohibited by this competition.

### Prepared Intervene — reserved Movement Interception

On the protector's own turn, use the existing [Movement Interception](movement-foundation.md#movement-interception) reservation:

1. Name **one creature to protect**, choose **Shield Guard** or **Body Take Hit**, and declare a **specific meaningful, non-guaranteed trigger**, for example *the first qualifying ranged attack declared against the mage before my next turn*.
2. Reserve a legal positive number of remaining **MP** immediately. The commitment follows the existing Movement Interception expiry, mobility/terrain, occupied-square, Cautious Movement, Opportunity, and turn restrictions. No Turn AP is bundled; **no Reaction** is spent.
3. When the trigger occurs, the reserved Movement Interception releases **before spontaneous Reactions**, following the usual initiative/nested-response order. Move along a legal route and complete **at least one actual movement step** into a position from which the selected protective method **can reach the specific incoming attack path**. A reservation that releases but cannot complete a legal protective step has **no protective effect**; the committed MP is not refunded.
4. When the attack later reaches its ordinary pre-roll resolution, apply the already-declared **conditional Shield Guard or Body Take Hit** only if the original intended creature would otherwise be struck. The underlying attack can have been cancelled, changed, or rendered illegal; recheck it under the actual state before rolling and do not redirect a cancelled/missed attack.

**Atomic-reservation exception, explicitly limited:** Existing Interception reservations remain **one Movement Interception**, **not** a bundle of movement plus a Physical Action or second Interception. This maneuver grants one **conditional protective defensive response** to that successfully released movement; it costs no separate Turn AP, creates no extra action/Reaction, and **cannot be combined with another reserved action in the same reservation**. If the movement does not complete **at least one legal step into a genuinely protective position**, the conditional response cannot apply. Multiple attacks cannot release the same reservation twice; an unused reservation expires under the normal default window.

Prepared Intervene preserves the protector's Reaction, so they may separately use an independently legal Reaction or later activate Opportunity Response. **This is the tactical reward for precommitting MP and a particular protection objective**, not permission to take an extra Attack or to protect every attack in a sequence. If an Opportunity Attack or mobility effect prevents the reserved movement from establishing the protective position, no protective response follows.

### Declaration and response sequence

For the particular incoming attack:

1. The attacker commits the attack/profile normally; the intended defender has already assigned **Take Hit, Dodge, or Guard** according to Attack Sequence rules.
2. Release applicable **precommitted Interceptions**, including Prepared Intervene movement, **before spontaneous responses**. Resolve any nested responses and recheck physical line/attack legality.
3. Eligible protectors may commit **Reactive Intervene**, if no protector has already been selected for that attack. Prepared Intervene that reached its protective position is the selected protector and has precedence over later spontaneous offers; **do not stack protectors**.
4. Before rolling, re-evaluate actual **Cover, Living Screens, defense, and attack legality** after movement. Roll and resolve the attack **against its original declared defender** using their **already-assigned defense**. If it would **not** hit, the protective response does not catch it. A miss still resolves its normal Cover/Living Screen/Guard impact or area scatter, without being attracted to the protector.
5. If the original attack **would hit**, resolve exactly **one** predeclared Shield Guard or Body Take Hit below. No new Attack Sequence, attack roll to redirect, defense reassignment for the ward, or damage to **both** creatures follows from a single ordinary direct hit.

If prepared movement makes the attack's actual direct path **completely blocked**, apply the existing illegality/cancellation rules and committed attack-cost consequences; do not automatically turn an illegal attack against the ward into a free hit on the protector. Moving into the line may itself make the protector an ordinary **Living Screen**, with the canonical allocation for misses; that **does not grant another screen modifier just for using Intervene**, and an incidental collision is not automatically the promised protective body hit.

## Shield Guard — attempt to stop the hit

- Requires a **ready, physically operable shield** that can Guard this incoming attack; shields may Guard normal projectiles under [Off-Hand and Ranged Combat](off-hand-and-ranged-combat.md#defensive-off-hands-and-shields). Ordinary weapons do **not** become projectile-capable and Guard eligibility is not broadened by this maneuver.
- Once the predeclared attack **would hit the ward**, commit **one use of the protector's existing Guard capacity** and compare the **original attack total** to the protector's ordinary legal **Shield Guard Defense**. A normally resolved original attack total that **does not beat** Shield Guard Defense is stopped by the shield; otherwise it strikes the **original intended target**. Do not substitute the ward's Defense for the shield's, take the higher of them as a new stacked Defense, or grant an extra +Cover from the **same** held shield. Independent real barriers remain governed by their physical placement.
- Shield Guard success contacts the **shield**, not the ward or protector's body. A projectile carrying an impact-triggered burst, cloud, or explosion resolves its actual area from the shield/Guard impact location; it is **not erased** by the successful Guard. Attack effects that can damage the shield use only separately authored equipment/object rules, not invented shield HP.
- The normal attack's **natural-20 special procedure has priority** over ordinary numerical Guard stopping: a natural 20 that would strike the ward cannot be reclassified as an ordinary numerically blocked shield hit merely because the shield's Guard Defense exceeds its attack total. Against Shield Intervene, use the existing **natural-20-versus-Guard confirmation procedure once**, with the protector's Guard Defense as confirmation Defense, and apply its resulting Strong/Critical/Devastating severity to the **ward** if the protective Guard could not stop that special hit. The protector does not generate a second separate critical opportunity. This interaction remains playtest-sensitive.
- **Shield or shield-arm loss after declaration:** An intervening Disarm, Secure Limb, or other response may make the shield unusable **before the original attack roll**. The protector may use a different already-ready, physically usable **shield** that can reach the same attack path, retaining the predeclared Shield Guard method; they may **not** switch to protective Dodge, Body Take Hit, or another action after seeing the disruption. If no eligible shield remains, **the protective Shield Guard cannot occur** and the original attack resolves against the ward under its normal already-assigned defense. The Reactive Intervene **Reaction** or Prepared Intervene **reserved MP** remains spent/committed as usual. **No Guard capacity is spent merely because the shield was lost or the protective response was declared:** it is charged **only after an otherwise-successful hit on the ward is established and a legal Shield Guard actually proceeds**. If the attack subsequently misses, hits cover, or is cancelled before that point, Guard expenditure is **zero**. This differs from loss of an **ordinary, already-committed personal Guard** under [Guard instrument loss](defensive-responses-and-criticals.md#guard-instrument-lost-after-defense-assignment). Once the protective Guard use **has actually been committed** against an otherwise-successful hit, later instrument loss cannot refund that spent use.

**Conditional resource timing:** The **Reaction/reserved MP** is committed at declaration/reservation; **Guard capacity is not**. A protective Shield Guard consumes **one Guard use only when an otherwise-successful attack against the ward reaches an actually legal shield-Guard attempt**. A pre-roll shield loss with no eligible replacement, or a primary miss, cover impact, or cancelled attack, **does not spend any Guard capacity**, even though the Reaction/reserved MP remains spent. If a Guard use has **already** been committed against an established incoming hit, subsequent loss does not refund it. Do not import the ordinary already-spent-Guard fallback's resource rule into a **never-activated conditional** Protective Intervene.

## Body Take Hit — accept the otherwise successful attack

- When the attack would actually hit the ward and the protector has a plausible reachable bodily path, they **receive that one direct hit instead of the ward**. This is **deliberate transfer of a confirmed hit**, not a second attack made against the protector's passive Ranged Defense. There is **no second accuracy test, personal Dodge, defensive Guard, conditional miss, or free extra Reaction**. The protector's **Armor, damage mitigation, HP/Vigor, wounds, and other applicable on-hit effects** then apply normally to the new recipient.
- If the original attack is a natural-20 Strong Hit, Critical Hit, or Devastating Critical under its pre-existing resolution, **transfer the already determined attack severity** to the protector. Do not add a new confirmation roll against the protector's Defense or downgrade the attack merely because they have better passive evasion. Other hit effects keep their independently authored eligibility requirements; a rider that requires a particular target or body part does not automatically transfer.
- If the original attack **misses**, Body Take Hit does **not** attract it. Likewise, a legal cover hit, an ordinary Living Screen incidental collision, a successful intended-target Guard, or a cancelled/illegal attack is **not** a hit transferred by Body Take Hit.
- Body Take Hit needs **no Guard capacity**. The cost is the declared Reactive Intervene Reaction **or** prepared MP commitment plus the full consequences of the received hit.

## Interactions and examples

| Case | Resolution |
|---|---|
| Knight adjacent to mage can physically reach the incoming arrow; no reservation; available Reaction | Reactive Shield Guard or Body Take Hit, declared before roll; Reaction committed whether or not mage is hit |
| Knight two squares away with no prior movement reservation | **Cannot** spontaneously cross that distance; no free move |
| Knight reserved MP to step into line, then archer attacks mage | Resolve one normal Movement Interception step/route before spontaneous responses; if position is legal, one predeclared protective response can apply to an otherwise successful attack |
| Knight's prepared movement draws a Movement Opportunity | Resolve it normally; if knight is stopped before reaching a protective position, protection fails |
| Mage chooses Dodge, arrow misses mage | Knight neither Guard-intercepts nor Body-Takes the miss; the committed Reaction/MP is still spent |
| Archer fires three committed attacks at mage | A given Protective Intervene applies to **one named attack**; it is not an all-sequence defense or third-party Dodge |
| Two guards volunteer to protect mage's one incoming attack | First valid prepared protector has priority; otherwise choose **one** eligible reactive protector in initiative order; no layered shield checks |
| Projectile primary die strikes wall's Cover face | Wall is impact point; no redirected hit to the knight |
| Projectile primary die selects knight's ordinary Living Screen face | Use canonical **conditional secondary collateral roll** versus knight's own predeclared defense; do **not** also perform Body Take Hit |
| Shield stops an area-bearing arrow | Shield is real impact point; carried area can still affect nearby characters according to actual radius and barriers |
| Nested Disarm disables protector's only shield **before** the attack roll; attack later misses, hits cover, or is cancelled | **Reaction/reserved MP remains committed; Guard capacity stays unchanged**. There was no legal protective Guard attempt. |
| Nested Disarm disables protector's only shield before the attack roll; attack later hits ward | **Reaction/reserved MP remains committed; Guard capacity stays unchanged**; with no usable replacement shield, no protective Guard takes place and the ward receives the hit. |
| A legal protective Shield Guard was activated against an otherwise-successful hit, then loses its instrument | Previously **committed Guard use remains spent**; no retroactive refund, protective Dodge, or switch to Body Take Hit. |
| Guard-capable buckler but no full shield? | **Provisional eligibility:** buckler is a shield-family Guard instrument, so it may Shield Intervene if its size/position can realistically span the ward's attack path; no automatic success from mere equipment |
| Attacker rolls natural 1 | Automatic miss; protection cannot turn it into a hit |

## Lock boundary and playtest watch

**LOCKED v0:** Spontaneous **Reaction** option, **precommitted MP** option, one named ward and triggering attack, Shield Guard versus deliberate Body Take Hit, **no protective Dodge**, no free movement or Guard capacity, no stacked Living Screen, pre-roll choice, and no transfer of actual misses. Prepared protection is one **atomic Movement Interception with an explicitly granted conditional protective response**, not two actions. A Reactive Intervene Reaction competes with Opportunity Response; a properly reserved Prepared Intervene **preserves** the Reaction.

**Calibration / later authoring:** reachable cross-square shield geometry, grapple/pin/size edge cases, natural-20 confirmation versus protective Guard, multi-protector priority and high-Tempo Guard economy, exact equipment damage, non-projectile magical attacks, large-body shields, and a future **Prepared Protective Stance** that protects more than one attack. Protective Intervene does **not** grant that Stance or create an unauthored area-Guard/penetration system.
