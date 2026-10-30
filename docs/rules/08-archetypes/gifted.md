# Gifted Foundation

> Canonical Gifted foundation from Core Rules Audit v34, amended by [High Gifted Amplification and Genuine Miscasts v0](../07-veil-magic/high-gifted-amplification-and-miscasts-v0.md). Structural Focus boundaries remain unchanged; other Focus/Aspect-specific expression content still requires authoring and balance verification.

## Archetype identity

A Gifted is born with permanent links between emotion and Aspect.

A Gifted is a **natural phenomenon of human Veil integration**, not a person selected, created, or deliberately shaped by a Pillar. Human emotion, Volition, and Pillar patterns arise within the same wider Veil metaphysics. Pillars are formed and sustained by recurring human Volition expressed through practice and interpreted through belief; a Gifted's innate emotional states naturally open unusually strong pathways into particular Aspect patterns. The linked Pillar does not need to choose, approve, or consciously recognize the Gifted.

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

Gifted do not use Priest-style daily preparation and do not individually learn **linked-Aspect techniques** like Scholars learn Pillar techniques individually.

**Emotion is the access mechanism for the Gifted's eight linked-Aspect catalogues and their emotion-dependent Archetype features.** To activate a **linked-Aspect technique**, the Gifted must genuinely evoke its matching emotion; no theatrical outward performance is required.

**Universal Veil procedures are a separate Pillar/Aspect-independent category.** A Gifted **automatically knows [Veil Inspection v0](../07-veil-magic/veil-inspection-v0.md) at character level 1 and [Blink v0](../07-veil-magic/blink-v0.md) at character level 3**, just like every other Archetype/Focus under [Universal Veil acquisition](../07-veil-magic/universal-veil-fundamentals.md#universal-eligibility-and-automatic-acquisition--locked). Neither procedure occupies any of the eight fixed emotion-to-Aspect links, requires evoking a matching emotion or establishing an Active Emotion, or uses a linked-Aspect technique slot. **Automatic knowledge does not grant free casting, extra VP, a VP discount, or permission to apply Gifted Amplification, Projected Surge, Conduit or Embodiment effects.** Any such interaction requires explicit authored compatibility; each unlocked Universal procedure keeps its own action, VP and effect restrictions. **Advanced Veil Analysis, Scrying and other unauthored procedures have no automatic unlock until their executable profiles and minimum levels exist.** The linked-Aspect catalogue rule does not automatically extend to Universal procedures.

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
3. the Gifted may instead leave Active Emotion unset, allowing the first **emotion-requiring linked-Aspect technique** to establish one at no extra action cost; a Universal procedure never establishes Active Emotion by default;
4. if a dominant competing emotion exists, it becomes Active by default unless the Gifted spends one **General Tempo Action (24 AP)** from the upcoming turn and succeeds on an Emotional Transition check;
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
- uses only **Potency, Reach, Extent, Persistence, Penetration, or Precision** with their exact conservative numerical effects in [High Gifted Amplification and Genuine Miscasts v0](../07-veil-magic/high-gifted-amplification-and-miscasts-v0.md);
- does not add VP cost by default;
- cannot duplicate the same option unless the technique says otherwise.

**Expression/damage-type swapping is not a generic Amplification.** An individual spell/profile must explicitly authorize every available option. Unused Steps expire with the Emotion Window.

### Natural Heightening

A naturally strong matching emotion may establish Heightened intensity without a check.

### Deepen Emotion

From Evoked:

- cost: **1 General Tempo Action (24 AP)**;
- check: `d20 + Awareness + Emotional Discipline Training + Resonance` vs **DC 12** benchmark;
- success: become Heightened for the current Emotion Window;
- failure: remain Evoked;
- failure does not cause Instability.

### Emotional Overload

A Heightened Gifted may spend **1 General Tempo Action (24 AP)** to become Overwhelming.

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
- failure by 5+: the risky second Step is lost and the spell undergoes **one genuine d20 miscast**, including possible fizzle, legal random retargeting (allies included), self-backlash, same-Aspect technique substitution, or rare beneficial accidents; the result may override or cancel the original spell.

The canonical [universal d20 table, pre-response timing, no-reroll fallbacks, costs, and same-Aspect replacement constraints](../07-veil-magic/high-gifted-amplification-and-miscasts-v0.md#universal-miscast-table-roll-d20-exactly-once-no-table-rerolls) **supersede** the old severe-only Manifestation Spill protection and former ban on retargeting an original spell. No unrelated Pillar/type conversion, free attacks or automatic hits.

## Emotional Transition

Changing emotions normally requires no roll when no dominant emotion is interfering.

When a dominant emotion persists:

| Interference | Cost / DC |
|---|---|
| Heightened dominant emotion | one **General Tempo Action (24 AP)**, DC 12 |
| Overwhelming dominant emotion | one **General Tempo Action (24 AP)**, DC 15 |
| particularly severe/direct conflict | GM may increase roughly +2–3 |

Check:

```
d20 + Awareness + Emotional Discipline Training + Resonance
```

Failure leaves the dominant link available for that turn. Ordinary physical actions and separately eligible **Universal Veil operations** remain available, subject to each operation's own requirements and action/VP costs. A Universal operation does not change the Active Emotion, restart the Emotion Window or override a dominant emotion merely by being used.

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

**L1–3 surcharge:** `ceil(positive effective technique VP cost / 4)` **additional Spent VP** per purchased Step; exact source-qualified [activation, reserve, and preflight rules](../07-veil-magic/high-gifted-amplification-and-miscasts-v0.md#projected-surge--high-gifted-l13) apply. A zero-VP technique does not qualify without explicit future authorization. The existing level-4 efficiency direction (−1 VP, minimum 1) remains provisional and is **not** added to the L1–3 implementation.

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

For the restricted L1–3 **Ward Form**, see [Medium Gifted Ward Conduit v0](../07-veil-magic/medium-gifted-ward-conduit-v0.md): the exact self-anchor, **24-AP initial placement**, Fear/Trust Grade I–III Pulse effects, Dormancy, release lockout and native-integration limits are deliberately **specific to Ward**. Other Conduit Forms are not granted by this link.

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

- cost: **1 General Tempo Action (24 AP)**;
- levels 1–3: **3 Spent VP**;
- levels 4–5: **2 Spent VP**;
- then commit/release any VP difference required by the new Grade.

Automatic emotional retuning is not Reconduction.

### Conduit count progression

| Level | Medium Gifted foundation |
|---:|---|
| 1 | **1 conduit**; Grades I–III available; Reconduction costs 1 General Tempo Action (24 AP) + 3 Spent VP |
| 2 | No additional universal conduit slot is added; expression growth is primarily technique/Form content |
| 3 | **2 conduits** |
| 4 | +1 Ability; Reconduction cost becomes 1 General Tempo Action (24 AP) + **2 Spent VP** |
| 5 | **3 conduits** |

### Conduit Pulse and cadence

A conduit may define one **Conduit Pulse per Emotion Window**.

Persistent expressions use the universal cadence framework:

- Continuous;
- Rider;
- Pulse;
- Spend.

A full technique-scale instance of damage, healing, Vigor restoration, strong control, or equivalent major output must not be an unrestricted per-action Rider.

## Low Gifted — Anchored Embodiment

**Core question:** *Which part of myself do I need to become, and can I stay there?*

Low Gifted gains value from committing to one emotion and maintaining it.

**Restricted L1–3 pilot expression authority:** [Rooted Guard / Unbound Step v0](low-gifted-anchored-expressions-l1-3-v0.md) approves the existing Fear/Fortification +1 committed defense and Disgust/Defiance −1 MP surcharge as **provisional watch values**. This does not authorize unsigned/unvalidated native response or movement receipts, other Anchor effects or full Focus certification.

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

- spend **1 General Tempo Action (24 AP)**;
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
| 3 | **Settled Emotion** — if Anchor persisted from previous turn, Deepen Emotion may be attempted with no General Tempo AP cost; successful settled Heightening persists while the same Anchor remains uninterrupted |
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

- Amplification permissions for techniques beyond the explicitly authored v0 profile;
- numeric calibration of the finalized L1–3 Projected Surge cost;
- final level-4 High Gifted surcharge reduction;
- Medium Conduit Form expressions and Grade scaling;
- Low Embodied and Deep Embodiment expressions;
- source-bound native combat integration for genuine miscast retargeting, Scatter, typed damage and response windows;
- persistent Rider/Pulse numbers against the maximum applicable Physical or Projection Tempo.
