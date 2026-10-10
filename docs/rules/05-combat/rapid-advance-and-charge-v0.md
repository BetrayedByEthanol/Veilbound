# Rapid Advance and Charge v0

> **LOCKED native movement and universal combat foundation; numeric calibration remains playtest-sensitive.** Rapid Advance offers faster **straight-line** movement without an AP cost. Charge extends the straight-line allowance further and may end in **one paid ordinary melee attack**. Neither mode grants a universal Attack/damage bonus, reduces Dodge Defense, or increases Dodge Pressure. See [Movement Foundation](movement-foundation.md), [Special Movement, Terrain, and Prone](special-movement-terrain-and-prone.md), [Turn Action Points and Tempo](action-categories-and-physical-tempo.md), and [Attack Sequence](initiative-and-round-structure.md#attack-sequence).

## Shared movement model

Let **M** be the creature's **currently impaired normal Movement Allowance** (usually 12 MP) after applicable modifiers and with a minimum of 0 MP.

| Mode | Current-turn movement allowance | Turn AP requirement | Heading | Attack |
|---|---:|---|---|---|
| Normal movement | **M** | None | Freely change direction | Ordinary attacks paid separately |
| **Rapid Advance** | **floor(3 x M / 2)** | **0 AP** | One fixed heading | Ordinary attacks paid separately |
| **Charge** | **2 x M** | **one Physical Action**, committed as described below | One fixed heading | One paid melee attack at the end |
| Sprint | **3 x M** | Full Action | Sprint Heading, subject to its existing Forced Redirection rule | No attack from Sprint |

These are **alternative total current-turn MP allowances**, **not additive pools**. MP already spent is never erased, duplicated, or refunded by changing circumstances. A step costs ordinary **2 MP orthogonally / 3 MP diagonally** plus applicable terrain and occupancy surcharges. A movement-allowance impairment updates the allowance for the current mode; MP spent earlier remains spent. **Distance** for Charge's minimum is measured by completed grid steps, **not** MP cost, so expensive terrain never counts as extra distance.

Rapid Advance or Charge may be initiated only **on the creature's own turn**, **before any MP has been spent or committed to Movement Interception during that turn**, and only while the creature can actually use the relevant walking/running locomotion. The creature chooses one of the **8 grid headings** at initiation. Its movement in that mode, including after an action or a Movement Interception that ends its current movement segment, must remain **along the original heading**. Neither mode permits Cautious Movement, voluntary heading changes, or Sprint's exceptional 2-MP Forced Redirection.

Rapid Advance and Charge obey the existing rules for terrain, step costs, occupancy (including allied transit), blocked corners, threatened spaces, Movement Opportunities, and physical locomotion limits. Merely **entering** threatened space does not provoke; a Normal step **leaving** threatened space can provoke. These modes grant no exception from an authored Opportunity or a creature's otherwise legal Interception.

**No defensive penalty:** Rapid Advance and Charge leave Guard, Dodge, Reaction, Opportunity Capacity, and Dodge Pressure unchanged except for ordinary consequences of separately occurring attacks or effects. There is **no Charge Exposure modifier** in v0.

To keep the extra allowance tied to the creature's own committed heading and turn, **MP cannot be newly reserved for Movement Interception after Rapid Advance or Charge starts**. A creature cannot switch between Rapid Advance, Charge, and Sprint in the same turn; **the only conversion permitted is an aborted Charge becoming Rapid Advance**, preserving its original heading and MP already spent. These modes are not themselves eligible as out-of-turn movement or attack Interception reservations.

## Rapid Advance (0 AP)

Declare Rapid Advance before any MP is spent/reserved this turn. Choose the heading and replace the normal current-turn movement allowance with **floor(3 x M / 2)** (18 MP for an unimpaired ordinary creature).

- Its straight-line movement may be **split around ordinary actions**, but neither an intervening action nor a movement-segment interruption resets the fixed heading.
- The creature may stop, attack, use a technique, or perform another otherwise legal action with its normal AP costs. **Rapid Advance does not grant an attack** or modify attack rolls or damage.
- A completed or abandoned Rapid Advance does not restore free-direction Normal movement later that turn; any further voluntary movement must follow the original heading within the same total Rapid Advance allowance.
- If an effect changes M, recalculate **floor(3 x M / 2)** immediately; if previously spent MP already meets/exceeds the reduced allowance, no further Rapid Advance steps can be completed. Never undo earlier legal steps.
- Ordinary Movement Interception and Opportunity rules apply to movement across this mode's steps, but the Rapid Advance heading remains fixed after an Interception changes the battlefield.

Rapid Advance consumes **no Turn AP**, including when it ends early because the creature voluntarily stops or an obstacle makes further straight-line movement impossible. Becoming Prone suspends Rapid Advance, subject to the [Prone suspension and Standing procedure](#prone-during-rapid-advance-or-charge).

### Rapid Advance with Drive / Drag

The existing [Drive / Drag v0](universal-maneuvers.md#drive--drag-v0) remains a legal **separate Physical Action** for a Controller while Rapid Advance is active, provided its Grapple, contest, locomotion, and pair-movement prerequisites are met. Drive / Drag's default freedom to change direction applies **only when no stricter active movement mode governs the Controller**:

- **Rapid Advance's fixed heading takes precedence.** Every Drive / Drag step moving the shared Grapple square counts as the Controller's **voluntary movement** and must follow the heading already chosen for Rapid Advance. Starting or ending the Drive / Drag Movement Segment, a failed contest, or a Movement Interception does **not** clear or change the heading.
- The Controller spends MP from its existing **Rapid Advance total current-turn allowance** (`floor(3 × M / 2)`), not a new or second pool. MP spent earlier that turn remains spent. The Controlled creature spends no MP, as normal.
- **Drive / Drag's slow pair-movement step costs are unchanged**: on ordinary ground, **4 MP orthogonally or 6 MP diagonally**, plus applicable flat surcharges. Rapid Advance increases the total allowance but does not discount Drive / Drag step costs or grant a free Grapple Contest.
- The Controller must pay the normal **one Physical Action** for Drive / Drag, resolve its one Grapple Contest, obey its single-segment limit and third-party Movement Opportunities, and pay another action/contest for another Drive / Drag segment. If the contested action fails, its AP is spent normally; the Rapid Advance allowance and heading remain unchanged.
- Prone suspends the Rapid Advance allowance under its usual rule: it cannot fund Crawling or Prone Drive / Drag; only the 4-MP Stand exception applies until Standing.

**Example:** A Controller activates Rapid Advance with 18 MP and an eastward heading, then wins Drive / Drag. With 0 MP previously spent and clear ordinary terrain, it can drive the pair **four orthogonal squares east** for 16 MP, leaving 2 MP. It cannot turn north, change heading after the contest, or move four squares and then claim a fresh movement pool.

**Charge is not a Drive / Drag action.** Charge's fast approach cannot move an intact shared Grapple pair by itself, nor can the Controller insert Drive / Drag during that approach; doing so would be an intervening Physical Action prohibited by Charge. An **AP-free aborted Charge converted to Rapid Advance** may subsequently use Drive / Drag, retaining the original heading, MP spent, and all normal Drive / Drag costs.

## Charge: committed approach plus one melee attack

A Charge is an **attack-linked movement maneuver**, not a free attack added to Rapid Advance or Sprint. It costs **one normal Focus-priced Physical Action** for its culminating melee attack and provides a current-turn allowance of **2 x M** (24 MP unimpaired). Its attack causes **normal weapon damage** on a hit and gets **no universal Charge accuracy or damage bonus**.

**Before moving**, declare:

1. **Charge intent**, an **initial intended target**, the **melee attack profile**, and one fixed heading. There must be a presently plausible straight-line approach on which that profile can reach the intended target after enough movement. Charge does not grant extra melee Reach.
2. Reserve in the sense of **keeping available**, but **do not yet spend**, enough current unspent Turn AP to pay **one Physical Action** when commitment occurs; those AP cannot be spent on another action during the ongoing Charge approach.
3. Begin the Charge movement segment. **At least 3 actual grid steps** must be completed along the Charge heading before any culminating Charge attack can begin, whether those steps are orthogonal or diagonal. A movement impairment, obstacle, or failed reach check never waives the minimum.

Charge movement and the culminating attack must occur **in order**, with no separate action deliberately inserted by the charging creature between starting its approach and beginning its Charge attack. **Drive / Drag cannot occur during Charge's movement approach** and Charge does not authorize carrying a shared Grapple pair without the separately paid Drive / Drag maneuver. **Standing to recover from Prone under the explicit suspension procedure is permitted and does not by itself count as an intervening action that cancels the approach; it still resets the Charge's three-step run-up.** Existing Movement Opportunities, enemy Interceptions, and nested responses continue to resolve at their normal step/attack timing. If a Movement Interception ends a movement segment, Charge can resume **only in the original heading** and only if it remains physically legal. A forced displacement does not count toward the Charge's three voluntary steps.

### Exactly when AP becomes committed

Use the currently effective **Rapid Advance allowance** as the cutoff for the AP-free portion of a Charge approach.

- **During a legal straight-line approach within the Rapid Advance allowance**, Charge is **tentative**: the intended Physical Action AP cost remains available but **unspent**. The creature may voluntarily abandon Charge, or it may be blocked or stopped before a legal attack becomes possible. In either case **only the actual MP spent is consumed**; no Physical Action AP is spent.
- **Before undertaking a step that would exceed the Rapid Advance allowance**, the creature must still be eligible to pay one Physical Action. If that step is completed legally, **commit the Physical Action AP immediately upon completion of the threshold-crossing step**. If a response prevents the step, no AP is charged merely because the step was attempted. The attack is prepaid at this point and is **not charged a second time** when it begins.
- **If a legal Charge attack begins before the Rapid Advance allowance is exceeded**, commit the Physical Action AP immediately **before opening the attack's response window**.
- Once AP is committed by either method, it remains spent if the attack is Interrupted, the target becomes unreachable, or movement is subsequently obstructed, under the normal committed-action rule.
- If an impairment later lowers the Rapid Advance cutoff below MP **already completed**, do not charge AP retroactively. Before performing **any further Charge step** beyond that newly reduced cutoff, commit the Physical Action upon a legally completed step if not already committed. A movement impairment also reduces the **2 x M Charge allowance**, and already-completed steps remain spent even if they now exceed that allowance.
- **Standing is not a Charge movement step.** Its 4-MP cost can cross the Rapid Advance allowance while a Charge is suspended without itself committing Attack AP. The AP threshold is charged only upon completion of a qualifying **Charge movement step**, or when its culminating attack begins.

**Aborting before AP commitment:** Convert the tentative approach into **Rapid Advance**. Keep the same heading and actual MP spent, obey the current Rapid Advance allowance, and permit later legal actions with the character's unspent Turn AP. If the Rapid Advance allowance has not yet been exhausted, any further voluntary movement this turn must follow the **same heading**. If the creature was knocked Prone, the converted Rapid Advance allowance stays **suspended** until Standing; the creature cannot Crawl from it. If the 4-MP Stand cost alone pushed MP already spent beyond the Rapid Advance allowance, that expenditure remains spent with **no retroactive Charge AP cost**, but no further Rapid Advance steps are possible. The character cannot start a second Charge or Sprint that turn. Even an allied creature stepping into the path does not automatically block passage when normal allied-square transit remains legal; the charging creature may instead **choose** to stop.

**Aborting after AP commitment:** The attack's Physical Action cost remains spent. If no Charge attack can be made, the Charge ends, **unused Charge MP is lost**, and there is no ordinary or Rapid Advance movement conversion. Any remaining Turn AP may be used normally.

### Prone during Rapid Advance or Charge

If a creature becomes **Prone after activating Rapid Advance or during the movement approach of Charge**, apply this procedure immediately, whether the fall was voluntary or caused by an enemy response:

1. **Suspend, do not automatically cancel, the active mode.** End the active movement segment, retain the original fixed heading, and keep all MP already spent. The remaining current-turn Rapid Advance or Charge allowance is **suspended**, not restored to normal movement or converted into a new pool. Recalculate it normally if an impairment changes M.
2. **While Prone, neither mode can move.** Suspended MP cannot fund Crawl, Cautious Crawl, ordinary movement, further Rapid Advance or Charge steps, or any other MP expenditure **except the normal 4-MP Stand action**. Stand commits 4 MP from the suspended mode allowance before its existing Standing Opportunity and other responses; an Interrupted or impossible Stand loses those 4 MP normally. If fewer than 4 MP remain, that pool cannot fund Standing.
3. **After a successful Stand**, lift the suspension if the movement mode is still legal. The creature may continue voluntary movement **only along its original heading**, within the recalculated total allowance, starting a **new movement segment**. The Stand MP remains spent and reduces the same remaining allowance. Neither heading nor MP refreshes.
4. **Rapid Advance** resumes normally at 0 AP. **Charge approach** resumes with its existing **AP status unchanged**: AP that was previously committed is never refunded; a tentative Charge remains tentative until a completed step crosses the Rapid Advance cutoff or a legal Charge attack begins. **The three-step Charge minimum resets to zero on becoming Prone**—only new, voluntary steps **after Standing** count toward the culminating attack. Pre-fall steps remain spent MP but do not count toward this new run-up.
5. **The charger may choose to abort** while suspended or after Standing under the existing [AP commitment and abort rules](#exactly-when-ap-becomes-committed). Before AP commitment, convert to suspended/active Rapid Advance as appropriate, keeping heading and MP already spent; after AP commitment, ending Charge loses unused Charge MP and retains the AP expense. If no Stand is completed before turn cleanup, the suspended mode expires, unused MP is lost, and previously committed AP remains spent.

**A fall during the Charge attack's own response window is different.** The Charge approach has already ended and the Physical Action AP has been committed. Resolve the attack under the existing [Interception/Interrupt and Prone attack legality](initiative-and-round-structure.md#interception-versus-interrupt) rules: becoming Prone does **not** automatically Interrupt an otherwise still-legal attack, but an attack that becomes impossible is lost with AP spent. No suspended Charge movement or renewed three-step run-up is created after the Charge attack began.

The dedicated [Prone movement and Standing rules](special-movement-terrain-and-prone.md#prone-movement-state) control Standing Opportunities, interruptions, and posture legality; this section only defines what happens to the new movement modes and Charge's unfinished approach.

### Valid end and retargeting

After **at least 3 completed voluntary steps**, the charging creature may end the approach and attempt one attack if an enemy is **currently within the declared melee profile's actual Reach** and the attack is otherwise legal. It may choose the **initial target** or **one different legal enemy** in Reach, including an enemy who legally moved into or obstructed the path. It may **not** change the declared heading, weapon/profile, or required melee method, and it cannot retroactively claim a path that was never taken.

Retargeting occurs **before any defender assigns a defense and before the culminating attack's roll**. The new target must be eligible for an ordinary Attack Sequence from this attacker that turn: Charge does **not** bypass the **one ordinary Attack Sequence per target per turn** limit. If the original target remains eligible, the attacker may still choose a different legal target in Reach when finishing the charge; the final target is selected only once, before the Attack Sequence begins.

If the route is blocked or movement is interrupted but the 3-step minimum has been satisfied and a **legal target is already in Reach**, the attacker may end the movement and resolve the Charge attack against that target. If no legal target is reachable, the Charge is aborted under the AP-commitment rules above. A creature never gains an automatic Shove, collision, forced displacement, or Prone result from a Charge.

### Attack Sequence and Interception timing

Charge has a narrow **deferred-attack-commitment exception** to the usual declare-and-pay-before-response sequence, solely during its initial **movement approach**. The **intended target and attack profile are declared before any Charge movement**; the attack's **final target** and AP payment are fixed by the rules above. The attack itself is **not rolled**, and the defender does **not** assign Guard/Dodge/Take Hit, until the approach ends and a legal attack is actually initiated.

At that moment, before the first attack roll, declare and pay for **all ordinary attacks** that will be part of the final target's Attack Sequence this turn, including the Charge attack (already paid if the extended-movement threshold was crossed) and any ordinary later attacks or granted attacks against that target. The defender assigns defenses to **every committed attack before any roll**, using the normal Attack Sequence procedure. The attacker cannot add more attacks to that target's sequence after seeing attack or defense results. Previously committed attack profiles and other declared attack choices remain fixed.

The Charge attack is **one ordinary paid melee attack**, not a free extra attack or a Full Action. It gets its **own normal attack response/Interception window**. If the attack is **Interrupted**, handle its loss and any remaining committed attacks exactly as for ordinary attacks; it is not refunded. Movement interruption alone is **not** an attack Interrupt and does not by itself cancel a legal Charge. Completing the attack ends the Charge movement mode and **discards unused Charge MP**; remaining Turn AP may be spent on other legal actions. No additional walking movement is available that turn from the former Charge allowance.

## Examples

| Situation | Outcome |
|---|---|
| Fighter begins Charge and voluntarily stops after 2 orthogonal steps (4 MP) when an ally moves ahead | No 3-step minimum, no attack, **4 MP spent**, **0 AP spent**; converts to Rapid Advance with the same heading |
| Fighter has spent 14 MP and a legal allied transit or enemy Interception blocks further Charge movement | If no legal target is in Reach, stop/abort to Rapid Advance; **14 MP spent**, **0 AP**; if the 3-step minimum and Reach are met, may instead pay one Physical Action and attack |
| Fighter has spent 18 MP and attempts a blocked step costing 2 MP | If the step does not complete, **no AP** is committed solely for that attempt; the fighter may abort to Rapid Advance (18 MP already spent) |
| Fighter legally completes a 2-MP step taking total spent MP from 18 to 20 | **One Physical Action AP is committed**, even if an obstacle subsequently prevents the planned attack |
| Defender Interception moves another enemy into Reach after Charge's third step | The attacker may select the new enemy before defenders are assigned, using the **unchanged attack profile** and the ordinary Attack Sequence limit |
| Charge attack is Interrupted after legal attack declaration | The paid Physical Action stays spent; resolve remaining precommitted attacks under ordinary Attack Sequence rules |
| Rapid Advance user is knocked Prone with at least 4 MP left | Rapid MP is suspended; 4 MP may pay Stand but **not Crawl**; after Standing resume same heading with remaining MP, no AP cost |
| Charge is interrupted by Prone before its attack begins | Charge MP is suspended, original heading retained; after Standing **three new steps** are required before attacking; existing AP commitment stays as it was |
| Tentative Charge has spent 16 MP, then spends 4 MP to Stand | Total spend reaches **20 MP** but **no Charge AP is due merely from Standing**. Aborting converts to Rapid Advance with 0 MP available; a subsequent completed Charge step requires AP if it exceeds the Rapid cutoff |
| Charge attacker becomes Prone during attack's response window | Apply normal attack legality/Interrupt, not movement suspension; AP already committed |
| Rapid Advance Controller uses Drive / Drag east on clear ground | Same 18-MP total allowance, east-only heading, one separate paid Physical Action and normal contest; four orthogonal pair steps cost 16 MP, leaving 2 MP |
| Controller wants to turn while driving during Rapid Advance | No: Drive / Drag's ordinary turning freedom does not override the active Rapid Advance heading |
| Controller aborts tentative Charge to Rapid Advance, then uses Drive / Drag | Permitted if the Grapple is legal; same original heading, already-spent MP and ordinary paid Drive / Drag contest |

## Deferred and calibration watch

**LOCKED v0:** Rapid Advance 1.5 x M (floor), straight heading and no AP; Charge 2 x M with one attack costing a Focus-priced Physical Action; 3-step minimum; no prior MP spending/reservations; no voluntary turn or Cautious steps; no universal accuracy/damage bonus; **no Charge/Rapid Dodge penalty**; ordinary Movement Opportunities/Interceptions; retargeting in actual Reach; tentative AP-free abort within Rapid allowance and paid commitment on the first completed step beyond it or when the Charge attack begins. **Prone suspends both modes; Stand may use 4 suspended MP, Crawl cannot; after Stand, heading persists and an unfinished Charge must complete a fresh three-step approach with its existing AP status.**

**Playtest-sensitive:** Exact 1.5 x / 2 x multipliers, 3-step minimum, opportunity exposure at extended distance, and whether the Charge movement incentive is too generous for its AP cost. The v0 ability to attack after a short Charge (when at least 3 steps were completed) deliberately permits a normal melee attack with no bonus; Rapid Advance may be equally good or better at such short ranges.

**Deferred:** Mounted charges, momentum-dependent impact/trauma bonuses, shield rush and collision damage, Brace-versus-Charge weapon reactions, size/mass limits, unusually mobile anatomy, and any separately authored charge-specific combat techniques.
