# Physical Hazards v0 — Locked Falling and Minor Displacement Boundaries; Provisional Collision Framework

> **FALLING v0 and Minor Displacement/Collision Boundary v0 — LOCKED.** Loss of support, ordinary/extended fall timing, emergency Catch Grip, Landing Control, the standard-gravity hard-surface falling-damage profile, and the non-damaging ordinary Shove/Throw collision boundary below are canonical. Falling damage numbers are **locked v0 playtest baselines**. The shared impact model for other collisions and crushing remains **PROVISIONAL**; specialized impact profiles remain **DEFERRED**. Existing locked movement, maneuvers, defense, and injury rules remain authoritative.

See [Movement Foundation](movement-foundation.md), [Traversal Foundation](traversal-foundation.md), [Special Movement, Terrain, and Prone](special-movement-terrain-and-prone.md), [Universal Maneuvers](universal-maneuvers.md), [Initiative and Round/Turn Procedure](initiative-and-round-structure.md), [Core Resolution](../01-core-resolution/core-resolution.md), [Weapons and Armor](weapons-and-armor.md), [HP and Vigor](../06-vigor-wounds-death/hp-and-vigor.md), and [Dying and Wounds](../06-vigor-wounds-death/dying-and-wounds.md).

## Scope and preserved boundaries

- **Falling** is uncontrolled motion following a loss of support, not ordinary MP movement or automatically Prone.
- Existing authored movement resolves before checking the support state it creates. In particular, resolve Shove/Throw displacement as already written, then evaluate any fall.
- **Forced movement and falling do not provoke general Movement Opportunities** merely because the creature changes position. An explicitly authored trigger still applies.
- **Shove and Throw do not inherently inflict impact damage.** Their blocked-displacement, step-by-step displacement, Control/Prone, and occupancy rules remain unchanged.
- **Catch Grip** uses the existing once-per-round Reaction; it grants no free movement, Guard, Dodge, attack, or AP. This cost and its eligibility/timing are **LOCKED** for v0.
- **Landing Control** is an eligible environmental check with the locked falling benefit below, not an extra attack defense or substitute for Catch Grip.
- Ordinary hazard injuries reduce **HP**, not Vigor directly. Standard falling uses the locked Impact Armor formula below. Existing wound triggers, Dying, and regeneration remain authoritative; this page creates no extra wound or critical trigger.
- A routine safe situation needs no roll. A physically impossible action cannot succeed merely because a die result is high.

## Universal physical-hazard sequence

1. **Resolve the initiating event.** Complete the original maneuver, displacement, movement, equipment failure, or other effect using its own declaration, contest, reaction, Interception, and Interrupt rules. Recheck legality when already required.
2. **Evaluate actual support.** Determine whether the creature retains sufficient ground, climbing Hold Support, buoyancy/propulsion, an effective tether, or some other independently valid support. Use an existing Stability or Traversal check **only when that procedure genuinely applies**; do not roll to restore a floor that is gone.
3. **Offer eligible support recovery.** If support is lost, resolve any automatic arrest by existing equipment/support. A creature with a reachable usable support and an available Reaction may declare one [Catch Grip](#catch-grip-v0--emergency-support-recovery) at the appropriate response window. Resolve existing precommitted Interceptions before spontaneous responses under the ordinary priority rules.
4. **Resolve uncontrolled motion.** If unarrested, determine the actual fall path, distance, and first contact. Ordinary encounter-scale falls resolve as part of the triggering event. The GM may designate genuinely prolonged falls as **Extended Falling**, using ordinary Initiative rather than a new clock; falling grants no free turns/actions.
5. **Resolve contact.** Assess whether [Landing Control](#landing-control--locked-v0) is physically possible. Standard hard-surface falls use the [locked falling-damage baseline](#falling-damage-v0--standard-impact); other physical impacts use any separately authored hazard profile and the [provisional shared framework](#shared-impact-event--provisional). Apply the existing HP, wound, position, and ongoing-hazard systems.
6. **Recheck the resulting state.** Supported, hanging/climbing, Prone on meaningful ground, still falling, restrained/crushed, unconscious, or another physically applicable state. No automatic chain displacement or repeat rolls without an authored cause.

### Support: unstable versus absent

| State | Resolution |
|---|---|
| Secure ordinary ground | No routine Stability roll |
| Unstable ground, balance meaningfully uncertain | Existing Shove Stability Check or appropriate Core Resolution/Traversal check |
| Climber still satisfies current **Hold Support** | Remains in Climbing State; no new Catch Grip Reaction |
| Support is absent, destroyed, or no longer reachable | Begin falling unless an independent arrest/support method is effective |
| Functional, adequately anchored safety equipment already arrests motion | Resolve that equipment; no Catch Grip Reaction merely to benefit from it |
| Swimming propulsion is disrupted | Follow swimming/buoyancy state; do **not** automatically apply the climbing fall procedure |

**No double test for the same event:** A failed Stability/Traversal check can establish lost support, but it does not grant a second free Stability test. Catch Grip is a different, explicitly eligible attempt to establish *new* support.

## Falling state and timing — LOCKED

A fall begins as soon as the creature has no sufficient support and no automatic arrest applies. Falling:

- uses **no MP** and spends **no Turn AP**;
- is **not** voluntary movement and creates no general Movement Opportunity;
- cannot be steered with ordinary ground movement, Sprint, Rapid Advance, or Charge;
- does not apply **Prone** until the creature reaches a position where Prone is meaningful;
- does not automatically cancel another effect; recheck physical legality and any explicit Interrupt.

For Shove/Throw, **finish the maneuver's already-authorized displacement before resolving falling**. A creature may catch support only if actually reachable at the final displacement position or at a later point of the actual fall. Throw never grants a retroactive catch of a passed ledge.

### Ordinary falling and Extended Falling

**Default:** Resolve an ordinary fall, including eligible response windows and landing, within the event that caused it. The creature cannot pause a short falling event to spend unused Turn AP or an ordinary Projection Action.

**Exception:** If actual distance, terrain, gravity, or an existing effect makes descent sufficiently prolonged, the GM may designate **Extended Falling** when the circumstances establish it. This is adjudication of an existing event, **not a separate timer, new action category, or new turn schedule**. State the expected falling window to players before action commitments where reasonably possible; do not retroactively shorten it to defeat a legal declared response.

While an Extended Fall genuinely persists through a creature's ordinary Initiative turn, that creature may use its **existing Turn AP**, including Focus-dependent Projection Actions, as physically possible. On its own turn a creature may likewise spend remaining AP only if it is already within a legally ongoing, extended fall. No fall grants or refreshes AP, MP, Reactions, Guard, or Interceptions, and passage of seconds does not itself trigger an extra turn.

At any point in a fall, a technique may activate **as a Reaction only if its own entry explicitly authorizes that Reaction timing and valid trigger**. A previously reserved Interception may release if its authored trigger and legality are satisfied. An ordinary Projection Action cannot become a Reaction just because the character has AP available. A zero-action cost alone does not grant interrupt timing. A Reaction-based technique competes with Catch Grip for the creature's one normally available Reaction. This adds **no new casting-speed/activation category**.

For unusual extended falls, the GM can use distance, gravity, existing motion and other known physical circumstances to adjudicate when contact actually occurs. Numerical free-fall estimates are optional adjudication aids, **not turn-generation thresholds**. Exceptional descent duration, air resistance, terminal velocity and time segmentation remain deferred.

### Deliberate leaps from height

A voluntary leap from height allows ordinary pre-departure preparation, equipment use, and a chosen physically possible departure orientation or path. It does **not** automatically reduce fall damage, grant extra AP/Reaction, or guarantee a successful landing. Perform any ordinary actions or technique activations before departure unless the fall subsequently meets the independent timing/permission rules above. A deliberate fall may qualify for Landing Control if physically possible; completely safe and routine short drops need no roll.

The mechanics of acquiring horizontal jump distance, extraordinary leaps, and in-air repositioning remain future **Jumping** work. Once airborne without support, use this Falling v0 procedure.

**Fixed-heading modes:** While unsupported, the creature cannot take further ground steps. Whether an interrupted Sprint/Rapid Advance/Charge approach can resume after regaining support continues to use that mode's existing legality, commitment, Prone, and expiration limits. Falling provides no extra MP, resets no Charge run-up, and grants no conversion to another movement mode; precise midair mode-state calibration is deferred.

## Catch Grip v0 — emergency support recovery

**LOCKED v0 cost:** one available **Reaction**, committed when Catch Grip is declared. The attempt is permitted on the creature's own turn or another creature's turn only when its physical trigger exists. It competes with Reactive Protective Intervene, activating Opportunity Response, and all other uses of the same Reaction.

### Trigger and eligibility

A Catch Grip is a deliberate emergency attempt when a creature is about to lose support or, while falling, passes an actual reachable support:

- a ledge, rope, handhold, rail, branch, or analogous usable support exists on the creature's real trajectory;
- the creature can perceive and attempt the catch in time and has a physically suitable usable hand, limb, implement, or an explicitly authored alternative;
- the support can plausibly bear the load and the approaching motion can plausibly be arrested;
- the creature has a Reaction available **before** passing the support's reachable position.

**Grid adjacency alone is insufficient** if the support cannot actually be reached. A character cannot use Catch Grip to cross a square, teleport back to a passed ledge, gain free climbing progress, or overcome an overwhelming physical impossibility.

**No Reaction is required** merely to continue holding already-satisfied Hold Support, to make an otherwise secured Traversal transition, or to benefit from an automatic appropriately anchored tether. If an existing grip remains secure, there was no need to Catch Grip.

### Timing and check

1. Finish the initiating displacement and existing response sequence as required by the specific action. Identify the first support genuinely available at the resulting position or while falling.
2. If a Catch Grip trigger is still valid, declare it **before leaving that support's reach**. Commit one Reaction.
3. Resolve one [Core Resolution](../01-core-resolution/core-resolution.md) check only if the emergency catch is genuinely uncertain. Choose one relevant Ability and any applicable Training and situational modifiers:

   `d20 + relevant Ability + applicable Training + situational modifiers`

4. **Success:** establish a secure hold and arrest the fall, entering/continuing the appropriate supported or hanging Traversal State; hand/limb occupancy and Hold Support apply immediately. Catch Grip never automatically puts the creature back onto the ledge.
5. **Failure:** the attempted support does not arrest the fall. Continue uncontrolled motion. The Reaction stays spent. Do not roll again against the **same** support during that continuous fall. A distinct later support may be considered only if physically reachable and the character independently has another legal opportunity/resource.

Use **Agility** for reaching and securely positioning a catch and **Strength** when the immediate challenge is arresting load through an already reachable grip. **Vitality** is generally relevant to *continued holding* or endurance rather than the initial catch. Do not sum all three Abilities.

A valid Catch Grip does **not** generate an ordinary Movement Opportunity merely for catching. It is not personal Dodge, Guard, Protective Intervene, or a reserved Movement Interception. A pre-existing Movement Interception may change the scene at its own original trigger, but it does not package a free Catch Grip or third-party rescue without a separately authored rule.

### Illustrative, nonbinding difficulties

These use the existing Core Resolution scale and require playtest calibration; they are **not** new universal fixed DCs.

| Physical catch | Illustrative target |
|---|---:|
| Sturdy, readily reachable handhold under pressure | 10 |
| Awkward ledge requiring accurate body placement | 12 |
| Wet or narrow handhold | 15 |
| Difficult swinging or poorly aligned support | 18 |
| Extreme but physically feasible catch | 20 |
| Unreachable, insufficiently strong, or physically impossible support | No roll; ineligible |

Equipment, injury, actual load, surface, approach speed and available limbs affect feasibility first and difficulty second. Training can also turn a potentially hazardous catch into an automatic success if circumstances warrant it.

## Landing Control — LOCKED v0

A creature approaching unavoidable contact may use a physically plausible landing technique if it has enough awareness, body control, time, and a suitable contact surface. Examples include a controlled roll, changing body orientation, or distributing contact force.

- **Cost:** No Reaction, Turn AP, or MP. Landing Control is a single eligible **environmental check**, not a free movement step, Dodge, Guard, or redirected trajectory.
- **Check:** If uncertain and consequential, make **one relevant Core Resolution check**, normally Agility + applicable Training + situational modifiers against a GM-selected difficulty from the existing core scale. **No universal fixed DC** is established.
- **Success:** Remove **one d4** from the falling-damage pool **before rolling**, to a minimum of zero dice. This does not confer arbitrary immunity to a sufficiently high fall.
- **Failure:** Roll the unmitigated falling-damage pool. No additional universal failure penalty.
- **Prone:** An uncontrolled landing ordinarily leaves the creature Prone if it arrives on a surface where Prone is meaningful, even if armor prevents HP loss. A successful Landing Control from **3 m or less** may leave the character standing if there is adequate secure footing and body position; higher falls ordinarily leave the creature Prone regardless of the successful damage mitigation. If Prone is physically meaningless (no viable supporting surface), do not apply it.
- **Routine drops:** Do not roll if a controlled drop is genuinely safe and routine. Deliberately leaping does not itself guarantee a successful control check or the one-die reduction.

Determine whether the landing is possible before rolling. Being unconscious, completely constrained, deprived of any meaningful orientation control, or meeting an unavoidable contact geometry can make Landing Control ineligible. Landing Control does not prevent the fall; Catch Grip is the distinct attempt to arrest it.

## Falling damage v0 — standard impact

**LOCKED v0 playtest baseline** for an ordinary humanoid falling from rest in Earth-like gravity onto a reasonably hard surface, with no independently effective arresting effect. It does not automatically apply to deep-water entries, falls from unusual initial velocity, abnormal gravity, sharp obstacles, collisions with other creatures, or extraordinary body scale.

1. **Measure vertical height** actually fallen before the first significant impact, in metres. A routine safe drop or a fall of **less than 1.5 m** has **no baseline falling damage**; special hazards may still have their own contact effect.
2. For a damaging fall of at least 1.5 m, set **N = ceiling(height / 1.5 m)**. Each started 1.5 m increment counts as one die. Roll **N d4** as one **Crush-type physical impact**.
3. If eligible Landing Control succeeds, subtract **1d4** from the pool (minimum zero) before rolling.
4. Apply any independently justified *surface/equipment* adjustment authored for that contact. The GM may adjudicate meaningful cushioning or impact arrest using the actual environment; **no universal surface-by-surface reduction table is locked yet**. Do not treat ordinary armor as this separate adjustment.
5. **Impact Armor** for this standard blunt fall is **floor(normal Armor / 2)**, minimum zero. Subtract it once from the total rolled damage, not from every die. There is **no additional weapon Penetration** or Strength/physical contribution:

   \`Falling HP Damage = max(0, falling dice total - floor(Armor / 2))\`

6. Apply HP loss, any ensuing Dying/wound trigger, and posture using the existing HP, Wounds, and Traversal rules. Damage reduction to zero does **not** automatically avoid Prone.

| Height | Dice before control | Average roll |
|---|---:|---:|
| Under 1.5 m, routine fall | 0 | 0 |
| 1.5 m | 1d4 | 2.5 |
| 3 m | 2d4 | 5 |
| 4.5 m | 3d4 | 7.5 |
| 6 m | 4d4 | 10 |
| 9 m | 6d4 | 15 |
| 12 m | 8d4 | 20 |
| 18 m | 12d4 | 30 |
| 24 m | 16d4 | 40 |

Examples: a 3 m fall with successful Landing Control rolls **1d4** before Armor; an uncontrolled 6 m fall in Armor 5 rolls **4d4 - 2**, minimum zero. Impact Armor for Armor 6 is 3. A failed Landing Control does not add damage dice.

This profile is independent of a creature's level: **Max HP = 10 + Vitality**. Vigor is not a damage shield. Reaching 0 HP invokes the established wound/Dying framework; death remains at **HP ≤ −Max HP**. Falling is not a weapon attack and receives no natural-20 critical/Devastating Critical by default. No new wound trigger is added for landing hard.

At very high heights or unusual physics, this standard profile is a provisional physical approximation and may require specialized hazard authoring. **There is no locked universal terminal-velocity cap, mass modifier, or deep-water profile**. Do not derive one from this height table.

## Minor Displacement and Collision Boundary v0 — LOCKED

Ordinary **Shove** and **Throw** are tactical displacement and posture-control maneuvers, not generic impact attacks. Their normal one- or two-square displacement (1.5–3 m) represents stumbling, loss of balance, tumbling, or forced repositioning **without inherent collision HP damage**. Merely contacting a wall, creature, or other obstruction does not turn that displacement into a damaging collision.

- **Shove:** Keep its one-square displacement, built-in advance, and existing terrain-dependent Stability Check. Shove does **not** automatically cause Prone or damage. Stable, secure footing requires no routine Stability Check.
- **Throw:** Keep its existing margin-dependent displacement and **Prone** outcomes. Neither a one-square nor two-square Throw gains impact damage; do not cancel an already-authored Prone tier merely because no damage occurs.
- **Blocked geometry:** A fully blocked Shove causes no displacement, built-in advance, automatic Prone, or automatic damage. A two-square Throw with a legal first square and blocked second square stops in the first square with its applicable Prone outcome and no automatic collision, crushing, or chain displacement.
- **Stumbling versus Falling:** A balance loss or tumble onto supported ground is not by itself a gravity fall of one or more 1.5 m increments; do not roll Falling v0 dice for horizontal movement, ordinary contact, or becoming Prone. **Catch Grip** is for emergency re-establishment of support during actual threatened/lost support, not a compulsory Reaction to recover from every stumble.
- **Actual loss of support:** Resolve all maneuver-authorized horizontal displacement first. If the resulting position is unsupported, apply the locked [Falling v0](#falling-state-and-timing--locked) procedure using **vertical distance actually fallen**, not horizontal squares traveled. No retroactive catch of a passed ledge.
- **Longer or more energetic displacement:** Crossing **three or more squares is not automatically damaging**, nor is two squares an immunity threshold. A separately authored high-energy effect may cause real collision damage even over a short distance, but only if its effect expressly provides a forceful-impact/hazard consequence and actual contact is possible. The required impact-damage profile is not established by ordinary Shove/Throw's square count or contest margin.

**This lock is a boundary, not a new collision damage subsystem.** It introduces no extra damage die, free attack, knockback speed, chain displacement, new Stability check, or automatic Reaction. Specialized damaging collisions, crushing, and structural impacts remain future work.

## Shared Impact Event — PROVISIONAL

An **Impact Event** is meaningful physical contact produced by relative motion. The **standard falling profile above is locked**; extending this shared framework to high-speed knockback, moving obstacles, falling objects, and separately authored collision-capable techniques remains **PROVISIONAL**.

1. **Contact:** Is there real intersection/contact and a genuinely forceful closing motion? Do not infer one solely from a blocked destination square.
2. **Magnitude:** Consider impact velocity/height and effective mass. A square count or contest margin is not automatically kinetic energy.
3. **Contact conditions:** Consider rigid/soft/sloped surface, stopping distance, body orientation/contact area, equipment, and relevant armor coverage.
4. **Mitigation:** Apply only eligible Landing Control or specifically authored equipment/surface mitigation; never stack invented hazard defenses.
5. **Consequences:** Use any authored hazard damage profile with existing HP/Armor/Dying/wound rules, and independently evaluate meaningful positional outcomes (e.g., Prone on supported ground or subsequent falling).
6. **Further events:** Additional impacts or sliding occur only where physical motion continues. No automatic victim-chain displacement, repeated collision damage, or extra attack is created.

A collision and a **sustained crush** are distinct. Crushing is ongoing compression or entrapment, not an initial collision repeated automatically; its recurring consequence uses the normal [ongoing-hazard timing](initiative-and-round-structure.md#ongoing-hazards) unless the authored hazard states otherwise.

### Hazard damage and injuries — preserved mechanics

- Use **HP** for damaging physical impacts. **Vigor is regenerative reserve**, not an additional HP shield or generic falling-damage pool.
- Standard hard-surface falling uses **floor(Armor / 2)** once, as locked above. Armor/coverage/bypass handling for **other impact types** requires separately authored hazard profiles; not every physical phenomenon is a standard blunt fall.
- Ordinary environmental impacts are not Attacks and do not roll natural-20 critical confirmations.
- Existing wound triggers remain: qualifying Called Shot, Devastating Critical, or reaching **0 HP**. This page adds no separate wound-on-fall trigger.
- Where a harmful impact creates a wound by an existing trigger, use the established **Crush** trauma family for ordinary blunt contact unless the actual impact is a separately authored piercing/cutting hazard.
- Damage dice, penetration, structural/object durability, and Armor interactions for **nonstandard impacts, crushing and collision** remain **DEFERRED**; do not silently reuse weapon profiles or treat ordinary Shove/Throw as damaging impacts.

### Nonbinding physical benchmark for later calibration

From rest in Earth-like gravity, neglecting air resistance, approximate speed before contact is `sqrt(2 × g × h)`. The following values are **reference physics only**, not damage tiers or automatic wound thresholds.

| Vertical distance | Approximate speed |
|---|---:|
| 1.5 m | 5.4 m/s |
| 3 m | 7.7 m/s |
| 6 m | 10.8 m/s |
| 12 m | 15.3 m/s |
| 24 m | 21.7 m/s |

This benchmark does not describe body orientation, soft landing surfaces, armor, magical effects, or initial vertical velocity. Injury severity cannot be read directly from this table.

## Interaction examples and regression checks

| Event | Required v0 boundary |
|---|---|
| Routine movement over normal ground | No hazard check |
| Ordinary one-square Shove on secure ground | Reposition only; no automatic Stability Check, Prone, or collision damage |
| One-/two-square Throw into an open supported position | Apply authored Throw displacement/Prone tier; no additional collision or falling damage |
| Character stumbles or lands Prone on secure ground | Resolve ordinary posture/balance consequences, not Falling v0 vertical-height damage |
| A magical force propels target rapidly into nearby stone | Potential impact only if separately authored as forceful collision; square count alone is not a damage rule |
| Shove into an unsupported square | Existing Shove contest/displacement first; then loss of support and any eligible Catch Grip |
| Two-square Throw over balcony | Existing full displacement first; no retroactive catch of a now-unreachable earlier ledge |
| Throw's second square blocked by wall/creature | Existing stop in first square and Prone result remain; **no automatic collision damage** |
| Shove completely blocked by wall | No displacement, built-in advance, automatic damage, or automatic Prone |
| Climber loses a hand but still meets Hold Support | No fall and no Reaction spent |
| Climber loses all Hold Support, ledge reachable | May spend Reaction for one eligible Catch Grip before passing the ledge |
| Climber held by viable anchored safety line | Resolve automatic line arrest; Catch Grip is not mandatory |
| Character already activated Opportunity Response | Reaction unavailable for ordinary Catch Grip that round |
| Catch succeeds while hanging outside platform | Remains supported/hanging, must meet Hold Support; no free climb/Stand |
| Controlled short drop | Routine safe drops require no roll. An eligible controlled damaging drop uses one Landing Control check, reducing the pool by 1d4 on success; no extra movement |
| Unarrested 12 m fall onto stone | Roll 8d4, minus 1d4 on successful eligible Landing Control, then subtract floor(Armor / 2) once; resolve HP, wound trigger, and Prone |
| Falling body meets another creature | Require intersecting physical paths; third-party contact and avoidance procedure deferred, no free attack/Guard |
| Heavy gate traps creature | Separate initial contact from recurring crushing and use authored ongoing-hazard cadence |
| Fall while Sprint/Charge movement is active | No midair MP steering or refreshed pool; preserve existing commitment/eligibility rules |
| Spell during 6 m unexpected fall | Only an independently legal Reaction/Interception can interrupt; unused Turn AP cannot pause the short event |
| Deliberate jump from high tower | Preparation before departure; normal actions only if fall is still ongoing during a legal turn, otherwise eligible Reaction/Interception |
| Extended fall crosses caster's turn | Caster may use existing AP with Focus costs on that turn, not a new air-casting action pool |

## Decision status and outstanding work

| Topic | Status |
|---|---|
| Locked Shove/Throw, forced-movement, Reaction/Interception, Traversal support, HP/Vigor/wounds boundaries | **LOCKED — unchanged** |
| Loss of support, falling state, timing default and Extended Falling adjudication | **LOCKED Falling v0** |
| Catch Grip: one Reaction, physical eligibility, one uncertain check, no retry on same support | **LOCKED Falling v0** |
| Already-held Hold Support and automatic tether arrest need no Catch Grip Reaction | **LOCKED Falling v0** |
| Deliberate jumps offer pre-departure preparation but no free impact reduction | **LOCKED Falling v0** |
| No new technique activation category; Reaction casting needs explicit permission | **LOCKED Falling v0 integration**, preserves magic action rules |
| Landing Control: one eligible Core Resolution check, no Reaction; -1d4 on success | **LOCKED Falling v0** |
| Uncontrolled landing Prone; successful control at ≤3 m may avoid it with secure footing | **LOCKED Falling v0** |
| Standard-gravity hard-surface impact: 1d4/started 1.5 m (from ≥1.5 m), half Armor floor | **LOCKED v0 playtest baseline; numerical rebalance by future explicit revision only** |
| Landing DC examples, specific cushions, unusual falling motion/height/physics | **GM adjudication / DEFERRED calibration** |
| Ordinary Shove/Throw minor displacement, blocked contact, and stumble-versus-fall distinction | **LOCKED Minor Displacement/Collision Boundary v0** |
| Shared Impact Event for other kinds of impacts | **PROVISIONAL** |
| Horizontal collision-capable maneuvers, victim avoidance, chain movement, structural damage, sustained crushing | **DEFERRED** |
| Detailed Jumping movement, precise long-fall timer, flight, underwater/buoyancy hazards | **DEFERRED** |

**Future calibration questions:** Validate 6 m and 12 m incapacitation/death outcomes against fixed Max HP, test whether half Armor and -1d4 Landing Control are sufficient, and author surface/collision/crushing and gravity variants without reopening locked combat foundations.

**Falling v0 and the Minor Displacement/Collision Boundary v0 are LOCKED.** Other Impact Event branches remain provisional/deferred. Future numerical changes must explicitly revise the v0 baseline rather than silently overriding it.
