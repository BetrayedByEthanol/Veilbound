# B04/B05 — Anointed Authority & Destiny Cross-Aspect Balance v0

> **DESIGN ONLY — NOT CANONICAL, NOT NATIVE, NOT A PLAYER PERMISSION.** This record proposes a graded Authority interface, Destiny and Meaningful Mission Event policy, and a reproducible numerical comparison of Conflagration Vigor burn versus regeneration interference. No player Signature, normal Pillar technique, native G0/G4/G5 encounter or complete Anointed character is implemented. B04/B05 still block MVP: **9/12** structural Focus pairings, **0/12** independently certified; 0/6 strict exits unchanged. B06 G0–G8 taxonomy is unchanged.

## One Signature, one graded Authority — provisional

The Anointed always retains a **0-VP Signature** while the bond is active. A single Authority expenditure enhances one otherwise lawful application. Focus defines the delivery, Aspect defines the effect. This is **not generic metamagic** and does not provide a spell catalogue or extra attacks.

| Choice | Unlock level | Destiny per eligible attempt | Character experience |
|---|---:|---:|---|
| Baseline Signature | 1 | 0 | Always useful without Destiny |
| Lesser Authority | 1 | 1 | First degree of exceptional control |
| Greater Authority | 5 | 2 | Stronger degree; Lesser remains available |
| Supreme Authority | 10 | 3 | Strongest degree; lower intensities remain |

The **1/2/3 cost and L1/L5/L10 gates are design candidates**. To avoid post-roll abuse, declare Authority before hit/resistance; spend Destiny at the actual legal application attempt even if it misses or is resisted. A declaration interrupted before the legal attempt pays no Destiny. One expenditure empowers one application only, never an unlimited persistent Vessel, all weapon strikes, additional actions, attacks, targets, casts or regeneration steps. **Level 3** already expands Focus-specific Authority eligibility to *explicitly compatible ordinary Aspect techniques* but does **not** unlock Greater intensity or automatically grant compatibility. No Conjure Flame, Basic Heal or Guided Regeneration Authority attachment is authorized by this document.

## Destiny and Meaningful Mission Event

Retain the existing **provisional** maximum Destiny formula: 2 plus floor(Level / 5), with 25% of the maximum restored after every **completed six-hour interval**, rounded half-up, minimum 1, capped at maximum. Partial intervals restore none. The proposed High L4 +1 maximum is **excluded from default calculations** and remains separately unresolved.

| Level | Destiny maximum | 6-hour recovery | Candidate strength available |
|---:|---:|---:|---|
| 1 | 2 | 1 | Lesser |
| 3 | 2 | 1 | Lesser |
| 5 | 3 | 1 | Lesser / Greater |
| 10 | 4 | 1 | Lesser / Greater / Supreme |
| 15 | 5 | 1 | Lesser / Greater / Supreme |
| 20 | 6 | 2 | Lesser / Greater / Supreme |

**Meaningful Mission Event** is not a Mission milestone or quest-progress gauge. A Mission has no completion percentage, fixed quest or endpoint. At GM discretion, one significant story event genuinely expressing, challenging or deepening that lifetime Mission can restore **+1 Destiny** (capped). A party successfully curing an afflicted village might count; routine repeated healing, ordinary attacks, repeatedly narrating the same event, or following a prescribed morality do not automatically count. A single GM-recognized event can award only once; another award needs another distinct meaningful event. This is additional to clock recovery, not a replacement. Aligned/Conflicted/Forsaken and Resonance remain independent of a GM reward choice. The isolated model's recognized unique event IDs are deterministic *witnesses*, not a new automated quest tracker.

## Fire / Conflagration: Kindled Flame proposal

One hypothetical **0 VP** Signature application produces **1 Fire HP** and **1 Vigor** damage on a valid hit, each as a distinct packet. A miss produces neither. Explicit Fire Resistance reduces Fire HP only; physical Armor does not mitigate Fire HP. The proposed Signature has no authored range, accuracy, legal Focus carrier, environmental fire behavior, permanent matter, Ignite, Burning, fire spread, extra attack or free spell permission.

**One Authority principle: stronger Vigor burn, not three separate spells.**

| Expression | Destiny | Fire HP on hit | Vigor damage on hit | Additional burn |
|---|---:|---:|---:|---:|
| Baseline | 0 | 1 | 1 | 0 |
| Lesser | 1 | 1 | 4 | **+3** |
| Greater | 2 | 1 | 7 | **+6** |
| Supreme | 3 | 1 | 10 | **+9** |

The **3/6/9** progression is experimental, not automatically granted by a universal formula, and cannot be attached to an ordinary spell without a specifically authored L3-compatible profile. No automatic Used Tier or Veil Control scaling is inferred.

### Source-constrained paid technique comparison

The existing [Conjure Flame](../rules/07-veil-magic/conjure-flame-v0.md) T1 Thrown Projectile Primary has **2 Fire HP**, plus Vigor equal to **2 + ceil(d8 × Used Tier / 3) + max(Veil Control,0)**, costs **2 × Used Tier Spent VP** and one Projection Action. The source-calculated VC0 Vigor averages on a successful hit are:

| Level | Highest eligible tier | VP per cast | Paid Vigor mean on hit | Highest candidate Authority Vigor on hit |
|---:|---:|---:|---:|---:|
| 1 | T1 | 2 | **3.875** | **4** |
| 3 | T2 | 4 | **5.375** | **4** |
| 5 | T3 | 6 | **6.500** | **7** |
| 10 | T5 | 10 | **9.875** | **10** |
| 20 | T9 | 18 | **15.500** | **10** |

Assuming **65% hit probability** only to normalize arithmetic (not a source-derived Anointed hit chance), L1 paid expectation is **2.51875 Vigor/attempt** versus Lesser Signature **2.6**. Paid magic retains higher Fire HP, its real attack/target profiles, Veil Control scaling and distinct resource cost; Destiny and VP are not interchangeable. At level 20, the paid spell's **15.5** average Vigor already exceeds Supreme's fixed **10**. **Late-level Signature relevance remains an open calibration issue**; this is not permission to invent further scaling.

## Comparison alternative — Searing Interference

**Searing Interference** is a deliberately **unapproved** alternative: the same baseline 1 Fire HP + 1 Vigor on hit, but Lesser/Greater/Supreme decrease **the target's next existing natural Regeneration Step throughput by 1/2/3**, floor zero, then expire. This neither burns additional Vigor nor changes its six-hour recovery, grants a new Regeneration Step, produces terrain damage, or automatically applies a lasting condition in canon. The pending-effect timing, stacking and resistance rules are **not authored for Conflagration**. Modeling it does not implement it.

### Actual source enemy profiles, isolated mathematical outcomes

| Existing B06 fixture | HP Max | Vigor Max | Natural regeneration | Fire resistance |
|---|---:|---:|---:|---|
| [Ordinary Human Soldier](../../content/creatures/b06-ordinary-human-soldier.v0.json) | **12** | **36** | **2** | None |
| [Firebound Sentry](../../content/creatures/b06-firebound-sentry.v0.json) | **12** | **36** | **6** | None |
| [Hunter of the Woods](../../content/creatures/b06-hunter-of-the-woods.v0.json) | **14** | **42** | **4** | None |

These are source-loaded **executable fixture statblocks**, but the model does **not** run the native encounter engine. The repeatable matrix covers **3 targets × 4 Vigor states (0, 1, 4, full) × 4 intensities × 2 models = 96** single assumed hit/next existing regeneration scenarios. Each starts at positive HP, five below maximum; it does not adjudicate actual attack skills, Dodge, Guard, cover, lethal wounds, death or CR. Whenever an attack would reach 0 HP the harness explicitly defers to the existing native Dying/wound rules.

**Example Supreme (3 Destiny):** Firebound Sentry starts at **7/12 HP, 36/36 Vigor**, throughput **6**. The assumed Fire HP 1 hit brings it to HP 6.

| After the next Regeneration Step | Direct Vigor burn | Searing Interference |
|---|---:|---:|
| Vigor immediately after hit | 26 (10 burned) | 35 (1 burned) |
| HP restored at next Step | **6** | **3** |
| HP after Step | **12** | **9** |
| Vigor after Step | **20** | **32** |

Direct burn is stronger for **lasting Vigor attrition**; interference is better for suppressing immediate repair while Vigor remains available. With **0 Vigor**, neither denies regeneration that could have happened. Interference adds condition tracking and expiration complexity, whereas direct burn reuses native Vigor packets. **Preference for initial pilot: direct burn**; it already feels Anointed through the 0-VP Signature and Destiny intensities without requiring an unrelated new power.

## High / Medium / Low three-Focus cadence (not damage parity)

[Turn Action Points and Tempo](../rules/05-combat/action-categories-and-physical-tempo.md) provide High **20 AP per Projection Action**, Medium **24 AP Physical/General**, and Low **20 AP Physical**. Proposed **opportunity envelopes only**:

- **High:** spend 20 AP for each active projected Signature application; one declared paid Authority per eligible attempt. Multiple projections fit into later-level Turn AP, subject to distinct legal attack and response resolution.
- **Medium:** spend an existing **24 AP General Action** to invest exactly one eligible weapon/tool Vessel. Then, at most **one actual paid Physical Action** (24 AP) each own turn may carry one Signature packet. Not a free action, remote hit or unlimited per-hit rider. Vessel/weapon authorization is still missing.
- **Low:** while embodied, at most **one legal paid Physical Action** (20 AP) per own turn may carry one Signature packet; not every weapon strike. Additional independent physical weapon damage is deliberately excluded because no three Anointed builds are authored.

| Level | Turn AP | High projections per own turn | Medium first/second/third own turns | Low packets per own turn |
|---:|---:|---:|---|---:|
| 1 | 30 | 1 | 0 / 1 / 1 | 1 |
| 3 | 42 | 2 | 0 / 1 / 1 | 1 |
| 5 | 54 | 2 | 1 / 1 / 1 | 1 |
| 10 | 84 | 4 | 1 / 1 / 1 | 1 |
| 20 | 120 | 6 | 1 / 1 / 1 | 1 |

At L1–3 Medium's 24-AP setup leaves insufficient AP for a 24-AP physical attack in that same turn. These envelopes **do not prove Focus DPS parity**, because Medium/Low may add the packet to a separate eligible weapon attack and High spends an action entirely on the Signature. High's potential six L20 free actions and Medium/Low's physical tempo require native testing. No extra attacks or independently legal Anointed character builds result from this study.

## Life / Restoration cross-check (no silent rewrite)

[Returning Step](b04-b05-anointed-restoration-birth-mission-signature-baseline-v0.md) remains a proposed **0-VP Vigor-to-HP conversion**: High **2 HP** per paid Projection Action; Medium **1 HP** at one invested patient's existing Step; Low **1 HP** at the embodied own Step. Candidate **Spare the Reserve** at 1 Destiny conserves the recipient's Vigor for the **existing** Focus cap. This PR **does not** replace those figures, authorize Greater/Supreme Restoration values, create free Wound Repair Progress or add Dying rescue. Restoration needs its *own* expressly authored graded intensity output and out-of-initiative cadence, not a general Conflagration-damage formula.

## Open blockers before canonical promotion

1. Existing High **Sovereign Projection** (L5) allows two compatible Authority Expressions at full cost. A one-graded-Authority model may conflict; do **not** automatically rewrite, combine, stack, double or discount it. The proposed High L4 extra Destiny point also remains unresolved.
2. **Level 3** ordinary-technique Authority compatibility still requires separate exact [Projection]/Vessel/[Embodiment] profiles and VP cost/source authorization.
3. Conflagration's range/target/accuracy/defense, all three carriers, physical action/rider timing, exact Destiny cost receipts, interruption and missed-hit proof, anti-duplication and paid techniques need actual native tests. Medium hostile Investment and Restoration noncombat cadence remain open.
4. Missing **High/Medium/Low L1–3 Anointed legal character builds**, source-native encounter integration, representative combat and noncombat evidence, and late-level calibration cannot be inferred from this design model.
5. The GM-recognized significant story event is **not a Mission completion checklist** and must not allow easy Destiny farming. Keep existing Resonance and Aligned/Conflicted/Forsaken rules untouched.

### Reproduce

From repository root run:

- python -m unittest discover -s tests -p 'test_b04_b05_anointed_authority_destiny_v0.py' -v
- python -m scripts.b04_b05_anointed_authority_destiny_v0

The second command prints a deterministic JSON report containing **96 single-hit/next-Step scenarios**, **15 three-Focus AP envelopes**, and paid Conjure Flame references. This is an **isolated comparison, not native combat certification**.
