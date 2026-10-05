# Universal Resonance and Direct Veil Magic

> **LOCKED rules.** This page defines the universal Resonance procedure and the native shared resolution engine for direct Veil effects: **Imposition** and **Intrusion**. The metaphysical meanings of Desire, Will, Volition, Resonance, level, Focus, and Pillar Accord are defined in [Metaphysical Foundation](metaphysical-foundation.md).

## Universal Resonance

Every character has a **Resonance** value from **-3 to +3**.

Resonance measures the internal coherence of the character's Volition: how coherently desires, emotions, beliefs, intentions, self-understanding, and actions reinforce rather than oppose one another.

It is not morality, loyalty, obedience, confidence, fanaticism, or Pillar alignment.

### Resonance scale

| Resonance | State | Meaning |
|---:|---|---|
| **+3** | **Integrated** | Major competing parts of the self have been consciously integrated; Volition is exceptionally coherent. |
| **+2** | **Strongly coherent** | Sustained internal coherence remains strong even under serious conflict. |
| **+1** | **Coherent** | Desires, self-understanding, intentions, and actions substantially reinforce one another. |
| **0** | **Ordinary / mixed** | A normal mixture of compatible and competing motives without major sustained internal fracture. |
| **-1** | **Dissonant** | Meaningful sustained contradiction or self-deception disrupts internal coherence. |
| **-2** | **Fractured** | Deep contradictions materially disrupt the character's Volition. |
| **-3** | **Self-opposed** | Profound, sustained conflict exists between desire, self-understanding, intention, and action. |

No additional universal special effect occurs merely for reaching +3 or -3. Individual rules may explicitly care about those values.

## Starting Resonance

A new player character normally begins at:

```
Resonance 0
```

Archetype does not change the universal starting value.

Priest **Pillar Accord** is a separate Priest-specific state and is not derived from starting Resonance.

## Resonance Events

Resonance is slow-moving. It does not change because of every emotional moment, difficult choice, failed ideal, or roleplaying scene.

A **Resonance Event** occurs when a meaningful internal conflict becomes consequential in play and the character's response establishes a lasting change in how that conflict is integrated or denied.

Use this procedure:

1. **Conflict appears.** Two or more important desires, beliefs, commitments, emotions, intentions, or parts of the character's self-understanding materially conflict.
2. **The conflict becomes consequential.** Temporary uncertainty, passing emotion, or a hypothetical contradiction is not enough by itself.
3. **The character responds over meaningful play.**
4. **Resolve the Resonance direction.**
   - Genuine recognition, acceptance, reconciliation, or integration of the conflict may increase Resonance by **+1**.
   - Sustained self-deception, denial, or repeatedly acting against an acknowledged self without integrating the contradiction may reduce Resonance by **-1**.
   - Consciously acknowledging that two important values conflict and choosing between them does **not** inherently reduce Resonance.
5. A single conflict normally changes Resonance by **at most one step**. An explicit rule may state otherwise.

Resonance cannot exceed +3 or fall below -3.

The same resolved contradiction cannot be repeatedly reused to gain Resonance. A later change requires a genuinely new conflict, a materially changed form of the old conflict, or a new stage in its resolution.

## What does not automatically change Resonance

The following are not automatic Resonance losses:

- fear, grief, anger, sadness, doubt, or other temporary emotion;
- changing one's mind;
- choosing one sincerely held value over another;
- failing to live up to an ideal once;
- making a painful compromise while honestly recognizing what is being sacrificed;
- actions performed under direct coercion;
- actions performed while magically controlled.

Likewise, merely announcing a new belief, sleeping, meditating, praying, or waiting does not automatically increase Resonance.

A character at low Resonance returns toward coherence by actually confronting, accepting, resolving, or integrating the contradiction that produced the dissonance, not by completing a fixed rest timer.

## Player and GM authority

The **player has primary authority** over what their character genuinely desires, believes, feels, and understands about themselves.

The **GM adjudicates** whether the established internal state, demonstrated choices, and sustained actions have become meaningfully coherent or contradictory enough to constitute a Resonance Event.

Resonance changes are open table information between the player and GM. They are not secretly imposed.

The GM cannot lower Resonance by inventing an unestablished hidden motive for the player character.

The player cannot retroactively redefine the character's inner state solely to erase an already-established contradiction or avoid its mechanical consequence.

### Optional Resonance Statements

A player may record a small number of concise **Resonance Statements** describing important things the character presently understands about themselves.

Examples:

- *I want my family safe more than I want glory.*
- *Authority must earn obedience.*
- *I will not abandon people who depend on me.*

These are descriptive reference points, not permanent commandments. They may change honestly through play and are not required to use the Resonance system.

## Universal mechanical scope

Resonance applies only where a rule explicitly calls for it.

The locked universal uses are:

- **Direct Veil Resistance** for both Imposition and Intrusion;
- existing Gifted emotional-control and Instability checks that already include Resonance;
- any future rule explicitly designated as testing the coherence or stability of Volition.

Resonance does **not** automatically modify:

- Max VP;
- normal VP recovery;
- spell or technique attack rolls;
- damage;
- healing;
- technique tier;
- ordinary nonmagical checks;
- Priest Pillar Accord;
- Anointed Mission state.

---

# Veil Integration Bonus

For direct Veil contests—both Imposition and Intrusion—character level contributes a bounded **Veil Integration Bonus**:

```
Veil Integration Bonus = floor(Level / 5)
```

| Character level | Veil Integration Bonus |
|---:|---:|
| **1-4** | +0 |
| **5-9** | +1 |
| **10-14** | +2 |
| **15-19** | +3 |
| **20** | +4 |

This represents the increasing resistance of a person whose existence is more deeply integrated with the Veil, and the increasing ability of an experienced practitioner to impose a deliberate Veil pattern.

Both sides receive the bonus, so equal-level opponents preserve the intended baseline probabilities.

A creature without a character level uses the equivalent value stated by its stat block. If no equivalent value is defined, use **+0**.

This bonus is locked for both **Imposition** and **Intrusion**.

---

# Shared direct Veil contest

**Imposition** and **Intrusion** use the same underlying direct-magic contest.

The difference is that Intrusion crosses the protected internal boundary of a living target and therefore adds the **Intrusion Barrier**. Imposition acts directly on the target from outside and does not receive that barrier.

## Direct Veil Pressure

The acting character rolls:

```
Direct Veil Pressure =
d20
+ Veil Control
+ Shaping Ability
+ Veil Integration Bonus
+ explicit technique and situational modifiers
```

The **Shaping Ability** is specified by the technique according to what the magical operation actually demands.

There is no universal mandatory mundane casting Ability.

**Veil Practice** or another Training is not automatically added to Direct Veil Pressure. A Training contributes only when an explicit technique, feature, or situational rule says that the particular learned expertise applies.

## Direct Veil Resistance

The target has a static resistance:

```
Direct Veil Resistance =
10
+ Resistance Ability A
+ Resistance Ability B
+ Veil Integration Bonus
+ Resonance
+ explicit technique and situational modifiers
```

The technique specifies the two defensive Abilities according to what part of the target is being acted upon and how the effect operates.

Examples of design direction include:

- identity, compulsion, or emotional overwrite: Awareness + Presence;
- perception, memory, or cognition: Awareness + Intellect;
- sleep or internal physiological suppression: Vitality + Awareness;
- direct bodily transformation: a Vitality-based pair appropriate to the authored operation;
- telekinetic restraint or forced movement: a physical pair appropriate to the authored force and method.

These examples do not create a universal save catalogue. Individual techniques still author their actual defensive pair.

A direct Veil effect succeeds only if **Direct Veil Pressure exceeds Direct Veil Resistance**. A tie resists the effect.

## Imposition

**Imposition** is magic that directly acts upon a target from outside without first becoming an independent manifested phenomenon.

Examples include:

- directly telekinetically restraining a creature;
- magically pushing or pulling a creature;
- directly igniting worn clothing;
- another external magical force applied directly to the target.

Imposition uses **Direct Veil Pressure** against **Direct Veil Resistance as written**.

It does **not** add the Intrusion Barrier.

At equal non-barrier modifiers, equal Veil Integration Bonus, and Resonance 0, Imposition therefore succeeds on 11-20: **50%**.

### Willing Imposition

A target that understands the actual Imposition may knowingly **waive Direct Veil Resistance** to that specific effect.

This permits effects such as willingly accepting telekinetic lifting without requiring a contest.

Consent applies only to the effect actually understood and accepted. If the caster materially changes the effect—for example, obtaining consent to lift someone and then attempting to hurl them—the target receives normal Direct Veil Resistance.

Imposition has no special "deceived acceptance" reduction. The +4 deceived state belongs specifically to the Intrusion Barrier because deception partially opens the otherwise protected internal boundary.

### Objects and attended equipment

Ordinary nonliving objects do **not** generate Direct Veil Resistance by themselves.

For an **unattended mundane object**:

- do not build a Direct Veil Resistance total;
- if the technique can target the object and the requested effect is within its authored size, mass, material, range, anchoring, and other limits, the Imposition succeeds without a resistance contest;
- physical attachment, mass, hardness, or similar object constraints are not Resonance and must be handled by the technique's authored limits or another explicit physical rule.

For an **attended object**—an object currently worn, carried, wielded, or otherwise under a creature's immediate physical control—the attending creature supplies the resistance:

- use that creature's **Direct Veil Resistance**;
- use the defensive Ability pair authored by the technique for an attended-object target;
- the object itself contributes no separate Resonance or Veil Integration Bonus unless an explicit item rule says otherwise;
- awareness of the attempt is not required for the creature's normal resistance to apply;
- the attending creature may knowingly waive resistance to the specific effect.

If an Imposition technique can target attended objects, it must define the appropriate defensive Ability pair for that use. If it does not, that technique cannot use the attended-object route.

If multiple unwilling creatures simultaneously attend the same object, use the **highest applicable Direct Veil Resistance** among them unless the technique explicitly says otherwise.

A magical, sentient, warded, or otherwise exceptional object may define its own Direct Veil Resistance or explicit modifiers. Use those authored rules instead of the mundane-object default.

Examples:

- igniting an unattended dry cloak within the technique's normal limits: no Direct Veil Resistance contest;
- directly igniting a cloak being worn by an unwilling creature: use the wearer's Direct Veil Resistance;
- telekinetically moving an unattended cup within the technique's mass limit: no Direct Veil Resistance contest;
- wrenching a sword from an unwilling wielder by direct telekinesis: use the wielder's Direct Veil Resistance, plus any explicit technique or physical constraints.

## Intrusion

**Intrusion** is magic that crosses into, originates within, overlaps, or directly alters the protected internal self of a living target.

Examples include mind control, forced sleep, direct perception or memory alteration, internal bodily transformation, and attempts to create or manifest matter inside living tissue.

A Manifestation does not bypass this rule. If the attempted manifestation originates inside or overlaps a living target, resolve it as an Intrusion.

Intrusion uses the same shared contest, but its resistance is:

```
Intrusion Resistance =
Direct Veil Resistance
+ Intrusion Barrier
```

The acting roll remains **Direct Veil Pressure**.

## Intrusion Barrier

The protected internal self supplies a large additional barrier.

| Target state toward this Intrusion | Intrusion Barrier |
|---|---:|
| **Unwilling / not knowingly consenting** | **+8** |
| **Genuinely deceived into accepting the magical contact** | **+4** |
| **Knowingly and willingly opens to the actual effect** | **Resistance may be waived entirely** |

### Full barrier

The **+8** barrier is the default.

Being surprised, distracted, restrained, asleep, unconscious, or unaware of the caster does not by itself reduce the barrier.

A target does not become easier to rewrite merely because they failed to notice the attempt.

### Deceived acceptance

Use the **+4** barrier only when the target has genuinely accepted the magical interaction but was materially deceived about what that interaction would actually do.

Example:

> A caster truthfully presents a spell as entering the target's memories to inspect a curse, but falsely conceals that the actual purpose is to alter those memories.

Merely casting secretly, distracting the target, disguising the casting, or attacking from surprise does not count as deceived acceptance.

The target still receives all other parts of Intrusion Resistance, including defensive Abilities, Veil Integration Bonus, Resonance, and applicable modifiers.

### Willingly opening resistance

A target that understands the actual effect may consciously open its internal boundary and **waive Intrusion Resistance** to that effect.

This is normally how willing internal buffs, healing, or transformations are accepted.

Waiving resistance applies only to the effect the target knowingly accepts. It does not create a general period of vulnerability to unrelated Intrusions.

If consent was obtained through a materially false description of the effect, use **Deceived Acceptance** instead.

## Natural d20 results

Direct Veil Pressure is resolved by its actual total.

A natural 20 does **not** automatically overcome Direct Veil Resistance or Intrusion Resistance.

This means sufficiently strong Intrusion Resistance can make an Intrusion impossible for an outmatched attacker until the attacker gains a real advantage through capability, deception, a technique-specific benefit, or changed circumstances.

Direct Veil Pressure is not a weapon attack merely because it uses a d20.

## Baseline probabilities

When attacker and defender have equal non-barrier modifiers, equal Veil Integration Bonus, and the target has Resonance 0:

| Effect / target state | Attacker success |
|---|---:|
| **Imposition** | **50%** |
| **Intrusion: unwilling (+8 barrier)** | **10%** |
| **Intrusion: deceived acceptance (+4 barrier)** | **30%** |
| **Knowingly willing and resistance waived** | no resistance contest |

Against an unwilling Resonance-0 target, the attacker needs approximately **+8 total advantage** in the non-barrier parts of the contest merely to reach an even 50% success chance.

Level alone cannot provide that full gap: Veil Integration Bonus ranges only from +0 to +4.

This preserves the intended rule that hostile Intrusion should usually fail against a comparable target and become reliable only when the attacker genuinely outmatches the target or meaningfully changes the circumstances.
