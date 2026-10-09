# Traversal Foundation

> Canonical Veilbound foundation for climbing and swimming as traversal rather than ordinary ground movement. This page defines capability adjudication, Traversal State and Traversal Segments, climbing support requirements, combat action legality, defensive movement, Opportunities, and disruption. Exact Climb/Swim MP costs, fixed capability thresholds, Catch Grip calibration, falling damage, drowning/breathing, currents/waves, armor-specific traversal effects, and detailed underwater weapon rules remain later work.

## Ground movement remains the baseline

Ordinary ground movement remains the simple default defined in [Movement Foundation](movement-foundation.md).

Outside combat, ordinary ground travel does **not** require a check merely to walk or travel over normal traversable ground. Distance, terrain, weather, load, and hazards may change travel time or create specific hazards, but Veilbound does not require generic ground-movement checks for routine travel.

Climbing and swimming are different. They are **Traversal** activities whose feasibility, risk, effort, and combat movement may depend on the character, route, method, equipment, and environment.

## Traversal resolution order

Resolve a traversal in this order:

1. **Capability — can the character do it by this method?**
2. **Risk — if it is possible, is success meaningfully uncertain?**
3. **Effort — does sustained exertion matter?**
4. **Combat movement — if combat timing matters, how much progress can the creature make with its available MP?**

Combat MP never makes an otherwise impossible traversal possible. Establish valid traversal first; MP measures progress through an already-valid traversal.

## Capability: possible before rolled

There is no universal Climb Capability or Swim Capability score.

The GM judges the actual route, method, creature, Training, equipment, injuries, load, and environment and places the attempt in one of three categories:

| Result | Meaning |
|---|---|
| **Automatic** | The character can perform the traversal and there is no meaningful uncertainty requiring a roll. |
| **Hazardous** | The traversal is physically possible, but failure is meaningfully possible and consequential. |
| **Impossible by current method** | The character cannot perform the traversal as attempted without changing the method, equipment, route, assistance, or circumstances. |

A die roll does not turn a physically impossible attempt into a possible one.

Changing the method may change the category. A rope, ladder, flotation aid, climbing equipment, assistance, magic, a lighter load, or a different route may turn an impossible attempt into a hazardous or automatic one.

Training may make a task automatic for one creature that is hazardous for another, or make a route possible that an untrained creature could not use safely. No fixed universal Training threshold is imposed by this foundation.

## Traversal checks

When a traversal is **Hazardous**, use the ordinary [Core Resolution](../01-core-resolution/core-resolution.md) procedure:

```text
d20 + relevant Ability + applicable Training + situational modifiers
```

against the GM-set difficulty for the actual circumstances.

Choose **one** relevant Ability for the immediate challenge. Do not add Strength, Agility, and Vitality together merely because several could matter to the overall activity.

Climbing Training applies when learned climbing technique materially helps the attempted climb. Swimming Training applies when learned swimming technique materially helps the attempted swim.

### Climbing Ability guidance

| Ability | Use when the immediate challenge is mainly… | Examples |
|---|---|---|
| **Strength** | producing or sustaining force | hauling up a rope, pulling over an overhang, climbing under heavy load, maintaining a demanding grip |
| **Agility** | body positioning, balance, or precise movement | technical footholds, awkward transitions, narrow ledges, moving efficiently between holds |
| **Vitality** | sustaining exertion | prolonged ascent, hanging for an extended period, repeated strenuous climbing without sufficient rest |

### Swimming Ability guidance

| Ability | Use when the immediate challenge is mainly… | Examples |
|---|---|---|
| **Strength** | producing propulsion against resistance | fighting a current, towing someone, moving while heavily burdened, powering through rough water |
| **Agility** | maneuvering and body control | diving through an opening, navigating rocks, changing direction in turbulent water, avoiding obstacles |
| **Vitality** | sustaining exertion | long-distance swimming, prolonged treading water, remaining effective through extended rough-water effort |

These tables are guidance, not fixed Ability assignments. The fiction determines what the immediate challenge is testing.

## Risk and effort are separate

A traversal can be physically demanding without being immediately hazardous.

Examples:

- climbing a secured rope in calm conditions may be tiring but not uncertain enough to roll for every few metres;
- crossing calm water may be automatic for a capable swimmer even though a long crossing eventually tests endurance;
- a wet narrow ledge may require little raw Strength but still be hazardous because slipping matters.

Do not call for repeated checks merely because traversal is strenuous.

When prolonged effort itself becomes uncertain, the GM may call for an appropriate check—often Vitality plus relevant Training—at a meaningful point. Exact endurance intervals, fatigue accumulation, and exhaustion consequences remain future work.

## Traversal State

A creature enters a **Traversal State** when it begins relying on a climbing route, swimming medium, or other authored traversal method rather than ordinary supported ground movement.

Entering or leaving Traversal State is not inherently a Turn AP action. The actual movement, equipment handling, checks, or other actions required by the fiction still use their normal procedures.

Traversal State persists while the creature remains dependent on that traversal's support or propulsion requirements.

Stopping movement or beginning another action does **not** by itself end Traversal State.

Examples:

- a creature may stop climbing, remain hanging on the cliff, attack if physically able, and still be in Climbing State;
- a creature may stop making swimming progress but remain in Swimming State while treading or otherwise maintaining itself in the water.

A creature leaves Traversal State when it reaches a stable state that no longer depends on that traversal method, or when an effect changes the creature into another movement/traversal state.

## Traversal Segments

A **Traversal Segment** is one continuous period of making progress through a traversal.

A Traversal Segment is a specialized movement segment and uses the same general timing principles as [Movement Segments](movement-foundation.md#movement-segments).

A Traversal Segment ends when:

- the traversing creature begins one of its own actions or effects;
- the creature leaves its current Traversal State;
- the creature changes to a materially different traversal route or traversal mode;
- a Traversal Disruption breaks the creature's progress;
- another rule explicitly ends the segment.

An enemy Opportunity Attack, Reaction, or other spontaneous response does **not** by itself end the Traversal Segment unless its result actually disrupts the traversal.

Stopping progress without another intervening event does not by itself create a new segment.

If the creature later resumes traversal after its segment has ended, it begins a new Traversal Segment.

### Transition between ground movement and traversal

Beginning traversal ends the current ordinary ground-movement segment and begins a Traversal Segment.

Leaving traversal for ordinary ground movement ends the Traversal Segment. If the creature continues moving on the ground, that movement begins a new ordinary movement segment.

The ordinary one-Movement-Opportunity-per-enemy-per-segment limit treats each Traversal Segment as a movement segment.

## Climbing support requirements

A climbable route may require different amounts of hand support to **hold position** and to **make progress**.

Use:

| Support | Requirement |
|---|---|
| **Support 0** | no usable hand is required |
| **Support 1** | at least one usable hand is required |
| **Support 2** | two usable hands are required |

A route may therefore have both:

- **Hold Support** — hands required merely to remain securely in place;
- **Progress Support** — hands required to make climbing progress.

Progress Support may be higher than Hold Support.

Examples may include a route where two hands are needed to climb but only one is needed to stop and hang safely. Exact support values belong to the route and circumstances rather than to one universal climbing table.

A hand committed to satisfying Hold Support or Progress Support is not simultaneously available to wield, use, manipulate, or otherwise operate an item.

If the creature stops making progress, use the route's Hold Support requirement. To resume climbing progress, it must again satisfy Progress Support.

Equipment or techniques may explicitly alter support requirements.

## Swimming propulsion requirements

Swimming uses propulsion rather than the climbing Support scale.

The GM considers which limbs and movements are available, what the creature is carrying, its Swimming Training, its physical condition, equipment, and the water conditions when deciding whether controlled swimming remains Automatic, Hazardous, or Impossible by the current method.

Holding an item does not universally forbid swimming, but an occupied or impaired limb may reduce available propulsion enough to change the traversal assessment.

This foundation does not impose a universal numerical penalty for swimming with an occupied hand, shield, weapon, injured limb, or armor. Those consequences follow from the actual propulsion requirement and later equipment rules.

## Actions while traversing

An action is legal while traversing only if the creature can continue satisfying the traversal's current **support or propulsion requirements** while performing that action.

For climbing:

- if the creature is holding position, use **Hold Support**;
- if an action is performed while also making climbing progress, use **Progress Support**;
- hands committed to support are unavailable for weapon, shield, item, or other hand-dependent use.

For swimming, the creature must retain enough usable propulsion/control for the action and current water conditions.

There is no universal attack penalty merely for being in a Traversal State.

Weapon or action restrictions that arise from the environment itself—such as detailed underwater weapon behavior—remain separate rules.

## Guard, Dodge, and defensive movement

Traversal does not apply a universal penalty to Guard or Dodge.

A defensive response is legal only when the creature can physically perform it while continuing to satisfy the relevant traversal requirements.

Examples:

- a climber cannot Guard with a weapon held in a hand currently required for support;
- a climber cannot Dodge by moving into unsupported empty space;
- a swimmer may use defensive movement only through positions and movement the creature can physically reach while swimming.

If a defense requires repositioning, that repositioning must be legal in the current Traversal State.

Exact defense interactions for particular weapons, shields, underwater combat, and future traversal techniques remain separate rules.

## Threatened space and Opportunities

Climbing and swimming do **not** inherently create an Opportunity merely because the creature is traversing.

Ordinary Reach and threatened-space rules continue to apply to the creature's actual position.

When a creature voluntarily leaves a threatened position through traversal, the ordinary Movement Opportunity rule applies before departure unless the movement qualifies as Cautious or another explicit rule prevents the Opportunity.

Entering threatened space does not provoke by default.

A traversal route or circumstance that permits deliberate controlled movement may permit **Cautious traversal**. Cautious traversal receives the ordinary protection from the general Movement Opportunity. Exact Climb/Swim MP costs, including the cost of Cautious traversal, remain unresolved until traversal speeds are calibrated.

### Diving and vertical movement

Changing depth or vertical position does not erase an Opportunity that already exists at the starting position.

If a swimmer at the surface begins a dive from a position threatened by an enemy whose Reach covers that starting position, leaving that threatened position can create the ordinary Movement Opportunity **before** the swimmer moves beyond that Reach.

Once the creature occupies a position outside that enemy's actual Reach, that enemy no longer threatens it merely because it is swimming or climbing.

## Traversal Disruption

A **Traversal Disruption** occurs when an event materially prevents the creature from maintaining the support or controlled propulsion required by its current traversal.

An attack does **not** automatically cause Traversal Disruption merely because it hits.

Authored or fictional causes can include:

- losing required support;
- forced displacement that removes the creature from its support or viable traversal path;
- destruction or loss of the rope, hold, platform, flotation, or other relevant support;
- an explicit effect that disrupts grip, balance, or controlled traversal;
- another change that makes the current traversal requirements impossible to satisfy.

### Climbing Disruption

If a climbing creature still satisfies **Hold Support** after the disrupting event, it remains in Climbing State.

If it no longer satisfies Hold Support or is displaced away from usable support, it begins to fall **unless another valid support is immediately established**.

A reachable ledge, rope, hold, piece of equipment, or other support may make such re-establishment possible. The eventual **Catch Grip** procedure, including any dedicated timing, modifiers, and calibration, remains unresolved.

Falling distance, falling damage, collisions, and related hazards remain part of the future falling rules.

### Swimming Disruption

Swimming Disruption does not use the climbing fall rule.

If the creature can no longer maintain controlled swimming, the water and buoyancy state determine what happens next. Calm-water drift, current displacement, sinking/rising, breath, drowning, waves, and other water-hazard consequences remain future work.

## Deferred traversal layers

This foundation deliberately does **not** define:

- exact Climb MP costs or Climb speed;
- exact Swim MP costs or Swim speed;
- fixed Strength/Agility/Vitality thresholds for routes;
- fixed Training thresholds for routes;
- character-creation rules determining starting Climbing/Swimming competence;
- a universal Catch Grip procedure;
- falling distance/damage and collision rules;
- drowning, breath-holding, buoyancy, currents, waves, and other water hazards;
- armor-specific climbing/swimming effects;
- detailed underwater weapon behavior;
- universal fatigue/exhaustion intervals for sustained traversal;
- jumping, squeezing, flight, or other future traversal/movement modes.
