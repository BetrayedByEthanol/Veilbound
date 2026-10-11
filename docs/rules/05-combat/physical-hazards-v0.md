# Physical Hazards v0 — Falling, Catch Grip, Landing, and Impact Framework

> **PROVISIONAL design for review; not a final numerical hazard lock.** This page proposes a Veilbound-native procedure for loss of support, falls, emergency Catch Grip, landings, and shared physical impacts. Existing locked movement, maneuvers, defense timing, and injury rules take precedence if any provisional wording would conflict. Numeric damage, armor/landing mitigation, collision-capable maneuvers, and environmental variants remain **DEFERRED**. Do not infer missing damage or new attack permissions from this page.

See [Movement Foundation](movement-foundation.md), [Traversal Foundation](traversal-foundation.md), [Special Movement, Terrain, and Prone](special-movement-terrain-and-prone.md), [Universal Maneuvers](universal-maneuvers.md), [Initiative and Round/Turn Procedure](initiative-and-round-structure.md), [Core Resolution](../01-core-resolution/core-resolution.md), [Weapons and Armor](weapons-and-armor.md), [HP and Vigor](../06-vigor-wounds-death/hp-and-vigor.md), and [Dying and Wounds](../06-vigor-wounds-death/dying-and-wounds.md).

## Scope and preserved boundaries

- **Falling** is uncontrolled motion following a loss of support, not ordinary MP movement or automatically Prone.
- Existing authored movement resolves before checking the support state it creates. In particular, resolve Shove/Throw displacement as already written, then evaluate any fall.
- **Forced movement and falling do not provoke general Movement Opportunities** merely because the creature changes position. An explicitly authored trigger still applies.
- **Shove and Throw do not inherently inflict impact damage.** Their blocked-displacement, step-by-step displacement, Control/Prone, and occupancy rules remain unchanged.
- **Catch Grip** uses the existing once-per-round Reaction; it grants no free movement, Guard, Dodge, attack, or AP.
- **Landing Control** is one possible environmental check, not an extra attack defense and not a substitute for Catch Grip.
- Ordinary hazard injuries reduce **HP**, not Vigor directly. Existing Armor, wound triggers, Dying, and regeneration remain authoritative; this page creates no extra wound or critical trigger.
- A routine safe situation needs no roll. A physically impossible action cannot succeed merely because a die result is high.

## Universal physical-hazard sequence

1. **Resolve the initiating event.** Complete the original maneuver, displacement, movement, equipment failure, or other effect using its own declaration, contest, reaction, Interception, and Interrupt rules. Recheck legality when already required.
2. **Evaluate actual support.** Determine whether the creature retains sufficient ground, climbing Hold Support, buoyancy/propulsion, an effective tether, or some other independently valid support. Use an existing Stability or Traversal check **only when that procedure genuinely applies**; do not roll to restore a floor that is gone.
3. **Offer eligible support recovery.** If support is lost, resolve any automatic arrest by existing equipment/support. A creature with a reachable usable support and an available Reaction may declare one [Catch Grip](#catch-grip-v0--emergency-support-recovery) at the appropriate response window. Resolve existing precommitted Interceptions before spontaneous responses under the ordinary priority rules.
4. **Resolve uncontrolled motion.** If unarrested, determine the actual fall path, distance, elapsed time when relevant, and first contact. Ordinary encounter-scale falls resolve as part of the triggering event. Long falls may require actual elapsed-time treatment, but do not grant free turns/actions.
5. **Resolve contact.** Assess whether [Landing Control](#landing-control) is physically possible, then evaluate one [Impact Event](#shared-impact-event). Apply any authored damage and consequences using the existing HP, armor, wound, position, and ongoing-hazard systems. Numerical hazard profiles are still deferred.
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

## Falling state and timing

A fall begins as soon as the creature has no sufficient support and no automatic arrest applies. A fall:

- uses **no MP** and spends **no Turn AP**;
- is **not** voluntary movement and therefore creates no general Movement Opportunity;
- cannot use ordinary ground movement or the creature's current Sprint/Rapid Advance/Charge allowance to steer in midair;
- does not apply **Prone** until the creature reaches a position where Prone is physically meaningful;
- does not inherently cancel an ongoing action by itself; recheck its actual physical legality and any explicit Interrupt, consistent with the initiative rules.

For Shove/Throw, **finish the maneuver's already-authorized displacement before resolving falling**. A creature can catch a ledge only if that support is actually reachable at the resulting position or at a subsequently reached point on its fall. The rules do not retroactively restore access to a ledge passed during a two-square Throw.

An ordinary drop may resolve without measured round-by-round descent. For prolonged falls, use the actual path/time and allow only independently legal actions or response triggers. Exact long-fall time segmentation and aerial maneuvering are deferred.

**Fixed-heading modes:** While unsupported, the creature cannot take further ground steps. Whether an interrupted Sprint/Rapid Advance/Charge approach can resume after regaining support continues to use the existing mode's Prone, interruption, legality, and expiration rules where applicable. This proposal does not create extra MP, reset a Charge run-up, or authorize a new conversion; precise midair mode-state calibration is deferred.

## Catch Grip v0 — emergency support recovery

**PROVISIONAL cost:** one available **Reaction**, committed when Catch Grip is declared. The attempt is permitted on the creature's own turn or another creature's turn only when its physical trigger exists. It competes with Reactive Protective Intervene, activating Opportunity Response, and all other uses of the same Reaction.

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

## Landing Control

**PROVISIONAL:** A creature approaching unavoidable contact may use an appropriate landing technique to improve its outcome if it has sufficient awareness, body control, time, and a suitable contact surface. Examples include distributing contact, bending/rolling, or adopting a safer orientation.

- No separate Reaction, Turn AP, or MP is charged for this **environmental control check**. It is **not** a free movement step, Dodge, Guard, or permission to redirect the fall.
- If meaningful uncertainty exists, make **one** relevant Core Resolution check (commonly Agility plus appropriate Training) for this landing event.
- On success, apply the eventual authored landing benefit, bounded by the physical magnitude and context of the impact. A success cannot erase arbitrarily high impact energy or invent safe terrain.
- On failure, use the event's unmitigated landing outcome; do not add a universal critical-failure consequence.
- Landing Control does not prevent the initial fall and does not substitute for Catch Grip. If the contact is safe and routine, no roll is needed.

**DEFERRED calibration:** exact impact-severity reduction, any permitted Prone avoidance, eligibility restrictions for armor/equipment, and performance at different heights/surfaces. No universal fixed damage reduction is introduced by this page.

## Shared Impact Event

An **Impact Event** is meaningful physical contact produced by relative motion. Falling, separately authored high-speed knockback, moving obstacles, and some later collision-capable techniques may all use one shared procedure.

1. **Contact:** Is there real intersection/contact and a genuinely forceful closing motion? Do not infer one solely from a blocked destination square.
2. **Magnitude:** Consider impact velocity/height and effective mass. A square count or contest margin is not automatically kinetic energy.
3. **Contact conditions:** Consider rigid/soft/sloped surface, stopping distance, body orientation/contact area, equipment, and relevant armor coverage.
4. **Mitigation:** Apply only eligible Landing Control or specifically authored equipment/surface mitigation; never stack invented hazard defenses.
5. **Consequences:** Use any authored hazard damage profile with existing HP/Armor/Dying/wound rules, and independently evaluate meaningful positional outcomes (e.g., Prone on supported ground or subsequent falling).
6. **Further events:** Additional impacts or sliding occur only where physical motion continues. No automatic victim-chain displacement, repeated collision damage, or extra attack is created.

A collision and a **sustained crush** are distinct. Crushing is ongoing compression or entrapment, not an initial collision repeated automatically; its recurring consequence uses the normal [ongoing-hazard timing](initiative-and-round-structure.md#ongoing-hazards) unless the authored hazard states otherwise.

### Hazard damage and injuries — preserved mechanics

- Use **HP** for damaging physical impacts. **Vigor is regenerative reserve**, not an additional HP shield or generic falling-damage pool.
- Fixed Armor reduction and any appropriate contact/coverage or armor-bypass exceptions must be defined by a later hazard profile; this page does **not** assert that every fall ignores or is fully stopped by Armor.
- Ordinary environmental impacts are not Attacks and do not roll natural-20 critical confirmations.
- Existing wound triggers remain: qualifying Called Shot, Devastating Critical, or reaching **0 HP**. This page adds no separate wound-on-fall trigger.
- Where a harmful impact creates a wound by an existing trigger, use the established **Crush** trauma family for ordinary blunt contact unless the actual impact is a separately authored piercing/cutting hazard.
- Damage dice, penetration, structural/object durability, overkill severity, and exact Armor interaction are **DEFERRED**, not left to hidden default weapon formulas.

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
| Shove into an unsupported square | Existing Shove contest/displacement first; then loss of support and any eligible Catch Grip |
| Two-square Throw over balcony | Existing full displacement first; no retroactive catch of a now-unreachable earlier ledge |
| Throw's second square blocked by wall/creature | Existing stop in first square and Prone result remain; **no automatic collision damage** |
| Shove completely blocked by wall | No displacement, built-in advance, automatic damage, or automatic Prone |
| Climber loses a hand but still meets Hold Support | No fall and no Reaction spent |
| Climber loses all Hold Support, ledge reachable | May spend Reaction for one eligible Catch Grip before passing the ledge |
| Climber held by viable anchored safety line | Resolve automatic line arrest; Catch Grip is not mandatory |
| Character already activated Opportunity Response | Reaction unavailable for ordinary Catch Grip that round |
| Catch succeeds while hanging outside platform | Remains supported/hanging, must meet Hold Support; no free climb/Stand |
| Controlled short drop | Optional Landing Control if uncertain; no additional movement |
| High-speed fall onto stone | Landing Control cannot simply erase impact; use eventual calibrated damage |
| Falling body meets another creature | Require intersecting physical paths; third-party contact and avoidance procedure deferred, no free attack/Guard |
| Heavy gate traps creature | Separate initial contact from recurring crushing and use authored ongoing-hazard cadence |
| Fall while Sprint/Charge movement is active | No midair MP steering or refreshed pool; preserve existing commitment/eligibility rules |

## Decision status and outstanding work

| Topic | Status |
|---|---|
| Locked Shove/Throw, forced-movement, Reaction/Interception, Traversal support, HP/Vigor/wounds boundaries | **LOCKED — unchanged** |
| Distinguishing unstable footing, loss of support, and uncontrolled falling | **PROVISIONAL** |
| Ordinary encounter falls resolve within triggering event; long falls respect real time | **PROVISIONAL** |
| Catch Grip as a one-Reaction emergency support recovery, physically qualified | **PROVISIONAL** |
| No Catch Grip cost for already retained/automatically secured support | **PROVISIONAL clarification**, compatible with locked Traversal |
| Landing Control uses one eligible Core Resolution check without a Reaction | **PROVISIONAL** |
| One shared Impact Event for falls and qualifying collisions | **PROVISIONAL architecture** |
| Exact Catch/landing target calibration and success benefits | **DEFERRED** |
| Falling damage/Armor/penetration, impact severity and mass/size calibration | **DEFERRED** |
| Horizontal collision-capable maneuvers, victim avoidance, chain movement, structural damage | **DEFERRED** |
| Jumping, long-fall timing, flight, underwater/buoyancy hazards and sustained crushing profiles | **DEFERRED** |

**Review questions:** (1) Does emergency Catch Grip consuming the only Reaction make Shove-off-ledge play sufficiently tactical without overpunishing the defender? (2) Should a particular equipment/Training trait later provide a non-Reaction arrest? (3) What severity/damage benchmarks preserve ordinary danger against level-independent HP while giving reasonable value to Armor and landing skill?

Do not mark Physical Hazards numerically complete or treat these design proposals as **LOCKED** until reviewed and calibrated.
