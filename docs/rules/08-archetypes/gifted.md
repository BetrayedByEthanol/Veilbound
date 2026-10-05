# Gifted Foundation

> Canonical extraction from Core Rules Audit v34 plus the locked High/Medium foundation details from the immediately preceding Gifted design pass. Structural rules are promoted here; Aspect-specific expression content and several numeric surcharges remain calibration work.

## Archetype identity

A Gifted is born with permanent links between emotion and Aspect.

A Gifted is a **natural phenomenon of human Veil integration**, not a person selected, created, or deliberately shaped by a Pillar. Human emotion/desire and Pillar patterns arise within the same wider Veil metaphysics. A Gifted's innate emotional states naturally open unusually strong pathways into particular Aspect patterns; the linked Pillar does not need to choose, approve, or consciously recognize the Gifted.

The eight core emotions are:

- Joy
- Sadness
- Anger
- Fear
- Surprise
- Disgust
- Trust
- Anticipation

A Gifted has exactly **eight permanent emotion-to-Aspect links**, one for each emotion.

Each link:

- points to one specific Aspect;
- must use a different Aspect;
- must come from a different Pillar;
- is fixed at birth;
- grants access to that Aspect's full technique catalogue up to the universal character-level tier limit.

There is no required External/Internal/Transform distribution.

Gifted do not use Priest-style daily preparation and do not individually learn techniques like Scholars.

Emotion is the access mechanism. The emotion must be genuinely evoked, but no theatrical outward performance is required.

Any Gifted formula that references **Resonance** uses the universal internal-coherence state defined in [Metaphysical Foundation](../07-veil-magic/metaphysical-foundation.md#universal-resonance) and resolved by [Universal Resonance and Direct Veil Magic](../07-veil-magic/resonance-and-intrusion.md), not a Pillar-relationship score.

## Compatibility at creation

Emotion/Aspect compatibility uses three ratings:

- **Strong (S)** — immediately intuitive;
- **Plausible (P)** — valid when the player establishes a coherent emotional interpretation at creation;
- **No default link** — unavailable by default.

Strong and Plausible links are mechanically identical after character creation.

A Plausible link is justified when chosen; it is not re-litigated every time the Gifted uses the Aspect.

The full compatibility matrix remains canonical design content and should be migrated separately into structured content.

## Emotion Establishment Step

At the start of each Gifted turn, after ordinary start-of-turn housekeeping and before normal actions:

1. the previous **Emotion Window** ends;
2. if no dominant competing emotion interferes, the Gifted may establish any eligible linked emotion at no action cost;
3. the Gifted may instead leave Active Emotion unset, allowing the first emotion-requiring Gifted technique to establish one at no extra action cost;
4. if a dominant competing emotion exists, it becomes Active by default unless the Gifted spends 1 Attack Unit from the upcoming turn and succeeds on an Emotional Transition check;
5. Low Gifted normally re-establishes an uninterrupted Anchor;
6. Medium Gifted conduits immediately re-express when the new Active Emotion is established.

A newly established Active Emotion is normally fixed for the current Emotion Window unless an explicit feature says otherwise.

## Emotion Window

The **Emotion Window** begins at the Emotion Establishment Step and ends at the next such step.

Resources tied to emotion refresh by Emotion Window, not by attack or by other creatures' turns.

- Amplification Steps are generated once per Emotion Window.
- Deepen Emotion may be attempted at most once per Emotion Window unless explicitly expanded.
- Projected Surge allowances refresh once per Emotion Window.
- Maximum one Instability Check per Emotion Window.
- Reactions use the same remaining emotional resources.
- Changing Active Emotion inside the same window does not restart or refresh the window.

## Emotional intensity

| State | Meaning | Effect |
|---|---|---|
| **Evoked** | enough genuine emotion to open the link | normal technique use |
| **Heightened** | strong genuine emotion | 1 Amplification Step in the Emotion Window |
| **Overwhelming** | extreme genuine emotion | access to a second Amplification Step; using it risks Instability |

### Amplification Steps

Amplification:

- never raises technique tier;
- is technique-specific;
- may modify authored categories such as Potency, Reach, Extent, Persistence, Penetration, or Expression;
- does not add VP cost by default;
- cannot duplicate the same option unless the technique says otherwise.

Unused Steps expire with the Emotion Window.

### Natural Heightening

A naturally strong matching emotion may establish Heightened intensity without a check.

### Deepen Emotion

From Evoked:

- cost: **1 Attack Unit**;
- check: `d20 + Awareness + Emotional Discipline Training + Resonance` vs **DC 12** benchmark;
- success: become Heightened for the current Emotion Window;
- failure: remain Evoked;
- failure does not cause Instability.

### Emotional Overload

A Heightened Gifted may spend **1 Attack Unit** to become Overwhelming.

No second emotional check is required merely to enter Overwhelming.

The first Amplification Step remains safe. Actually using the second Step triggers Instability.

### Instability Check

```
d20 + Veil Control + Emotional Discipline Training + Resonance
vs
12 + ceil(Technique Tier / 2)
```

| Tier | DC |
|---:|---:|
| 0 | 12 |
| 1–2 | 13 |
| 3–4 | 14 |
| 5–6 | 15 |
| 7–8 | 16 |
| 9 | 17 |

Outcomes:

- success: both Steps function;
- failure by 1–4: first Step functions, second Step is lost;
- failure by 5+: first Step functions, second Step is lost, and an Aspect-appropriate **Manifestation Spill** occurs.

Instability remains an uncontrolled expression of the **same Aspect**. It does not generically invert healing into damage, swap elements, cast a different technique, or randomly retarget unrelated creatures.

Aspect-specific Instability Profiles remain future content.

## Emotional Transition

Changing emotions normally requires no roll when no dominant emotion is interfering.

When a dominant emotion persists:

| Interference | Cost / DC |
|---|---|
| Heightened dominant emotion | 1 Attack Unit, DC 12 |
| Overwhelming dominant emotion | 1 Attack Unit, DC 15 |
| particularly severe/direct conflict | GM may increase roughly +2–3 |

Check:

```
d20 + Awareness + Emotional Discipline Training + Resonance
```

Failure leaves the dominant link available for that turn. Ordinary physical actions remain available.

## High Gifted — Projection and intensity

**Core question:** *How far can I push what I feel right now?*

High Gifted expresses the current emotion-linked Aspect through outward technique use and deliberate extra amplification.

### Projected Surge

A **Projected Surge** may only be applied to a technique explicitly tagged **[Projection]**.

Projection eligibility belongs to the individual technique, not automatically to an entire Aspect category.

Projected Surge:

- buys an additional Amplification Step by paying an additional VP surcharge;
- does not increase technique tier;
- is separate from the ordinary Step generated by Heightened/Overwhelming emotion;
- refreshes by Emotion Window rather than by attack;
- may be held for a compatible Reaction during the same Emotion Window.

Levels 1–4 normally allow **one Projected Surge allowance per Emotion Window**.

The current surcharge benchmark is proportional to the technique's VP cost and remains provisional. The established design direction is approximately 25% of technique VP, minimum 1, with level-4 efficiency reducing the surcharge by 1 VP to a minimum of 1. Final numbers require calibration.

### Level 5 — Full projected expression

At level 5, one eligible `[Projection]` technique may receive **up to two Projected Surge Steps** in the same Emotion Window, paying the applicable surcharge for each.

This is increased emotional projection depth, not an extra action and not a tier increase.

### High Gifted boundary

High Gifted is **conditional intensity**.

It is distinct from:

- High Scholar synthesis;
- High Priest prepared/open one-Pillar invocation;
- High Anointed fixed one-Aspect Authority.

## Medium Gifted — Conduits and retuning

**Core question:** *What do my established conduits become under this emotion?*

Medium Gifted establishes persistent **Conduits** anchored into a defined form and locus.

Examples of Conduit Forms include:

- Contact;
- Ward;
- Motion;
- other authored forms added by Aspect content.

The Form and anchor are comparatively sticky. The **Aspect expression automatically retunes** when Active Emotion changes.

Changing Active Emotion does not itself count as Reconduction and costs no VP beyond the normal emotion rules.

If the newly Active Aspect has no authored expression for the current Conduit Form, that conduit becomes **Dormant** for that emotion rather than improvising an unsupported effect.

### Conduit Grade

Each conduit has a fixed Grade while established:

- **Grade I:** commit 1 VP;
- **Grade II:** commit 2 VP;
- **Grade III:** commit 3 VP.

All three Grades are available from level 1.

Changing emotion retains the same Grade.

Changing Grade is Reconduction.

### Reconduction

Reconduction changes a conduit's anchor, form, or Grade.

- cost: **1 Attack Unit**;
- levels 1–3: **3 Spent VP**;
- levels 4–5: **2 Spent VP**;
- then commit/release any VP difference required by the new Grade.

Automatic emotional retuning is not Reconduction.

### Conduit count progression

| Level | Medium Gifted foundation |
|---:|---|
| 1 | **1 conduit**; Grades I–III available; Reconduction costs 1 AU + 3 Spent VP |
| 2 | No additional universal conduit slot is added; expression growth is primarily technique/Form content |
| 3 | **2 conduits** |
| 4 | +1 Ability; Reconduction cost becomes 1 AU + **2 Spent VP** |
| 5 | **3 conduits** |

### Conduit Pulse and cadence

A conduit may define one **Conduit Pulse per Emotion Window**.

Persistent expressions use the universal cadence framework:

- Continuous;
- Rider;
- Pulse;
- Spend.

A full technique-scale instance of damage, healing, Vigor restoration, strong control, or equivalent major output must not be an unrestricted per-Attack-Unit Rider.

## Low Gifted — Anchored Embodiment

**Core question:** *Which part of myself do I need to become, and can I stay there?*

Low Gifted gains value from committing to one emotion and maintaining it.

### Active Emotion vs Anchored Emotion

- Active Emotion is the universal current Gifted link.
- **Anchored Emotion** is the Low Gifted's chosen persistent emotional commitment.
- At combat start, establish an Anchor.
- If uninterrupted, it automatically becomes Active again at later Emotion Establishment Steps.
- An externally dominant emotion can disrupt the Anchor without automatically replacing the player's chosen Anchor.

### Anchored Embodiment

The Anchored Emotion's linked Aspect grants an Aspect-specific **Embodied Expression**.

It is:

- self-centered;
- persistent through the emotion state;
- integrated with ordinary physical play;
- defined by Aspect content.

Outside combat, the Gifted may settle into one emotion at a time for the corresponding preparatory/noncombat expression. Benefits are not banked across multiple emotions.

### Break Anchor

To voluntarily change Anchor:

- spend **1 Attack Unit**;
- genuinely evoke another linked emotion;
- no roll if no competing dominant emotion interferes;
- new emotion becomes Active and the new Anchor;
- old Embodied Expression and persistence benefits end;
- new emotion starts at Evoked intensity unless circumstances naturally justify more.

There is no additional VP tax. The cost is tempo and lost momentum.

### Forced disruption

A dominant external emotion may disrupt the Anchor.

The player may accept the competing Active Emotion or attempt to reassert the Anchor through the normal Emotional Transition procedure.

Ordinary physical actions remain available regardless.

### Low Gifted progression

| Level | Foundation feature |
|---:|---|
| 1 | **Anchored Embodiment** |
| 2 | **Instinctive Expression** — Embodied Expression may integrate with eligible attacks, Guard, Dodge, movement, grapples/shoves, interception, touch, etc.; no free actions |
| 3 | **Settled Emotion** — if Anchor persisted from previous turn, Deepen Emotion may be attempted with no AU cost; successful settled Heightening persists while the same Anchor remains uninterrupted |
| 4 | **Emotional Center + Ability Increase** — +1 Ability; +2 on Emotional Transition checks specifically to preserve/reclaim the Anchor |
| 5 | **Deep Embodiment** — a stable Heightened Anchor gains an authored Aspect-specific Deep Embodiment rider |

Breaking or losing the Anchor ends Settled/Deep Embodiment benefits.

## Three-Focus Gifted distinction

| Focus | Gifted expression |
|---|---|
| High | **Amplify/project** the current emotion-linked Aspect |
| Medium | **Retune** established conduits as Active Emotion changes |
| Low | **Anchor and embody** one emotion, gaining value from persistence |

## Retired Gifted rules

The current foundation supersedes:

- mandatory d100 manifestation tables;
- generic random-target free spells;
- generic healing/damage inversion;
- tier increases from emotional amplification;
- legacy CHA-based emotional checks;
- Faith Rest/short-rest grounding dependencies;
- free manifestations as a normal reward for low control.

## Calibration/content still unresolved

- Aspect-specific Amplification options;
- final Projected Surge surcharge;
- final level-4 High Gifted surcharge reduction;
- Medium Conduit Form expressions and Grade scaling;
- Low Embodied and Deep Embodiment expressions;
- Aspect-specific Instability Profiles;
- persistent Rider/Pulse numbers against maximum Physical Tempo.
