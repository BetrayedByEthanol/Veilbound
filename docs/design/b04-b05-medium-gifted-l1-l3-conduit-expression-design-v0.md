# B04/B05 — Medium Gifted L1–3 Conduit Expression Design v0

> **DESIGN CANDIDATE — requires rule/content approval. NOT a new executable canonical technique, Focus pairing, native encounter, or MVP certification.** This record separates locked Medium Gifted foundation from one expressly proposed **Ward Form** package. The isolated budget/pulse witness in `scripts/b05_medium_gifted_conduit_design_v0.py` is **not** a source-backed B06 damage/response executor; its event quantities are supplied by the caller. The repository's canonical `docs/rules/` and unchanged MVP accounting outrank this proposal.

## 1. Source boundaries and restricted pilot

- [Gifted Foundation](../rules/08-archetypes/gifted.md#medium-gifted--conduits-and-retuning) already fixes **one** Conduit L1–2, **two** L3, Grades **I/II/III** reserving **1/2/3 Committed VP**, and automatic re-expression when Active Emotion changes. Unsupported Form × current linked Aspect becomes **Dormant**, not an invented effect. Automatic retuning is neither a cast nor Reconduction.
- Existing L1–3 **Reconduction** costs **24 Turn AP (one General Tempo Action) + 3 Spent VP**, followed by positive/negative Committed VP Grade difference; a changed Grade does not create an additional Conduit or a new Emotion Window. Anchor/Form/Grade are sticky until Reconduction.
- [Veil VP](../rules/07-veil-magic/volition-points.md) gives Medium **Max VP = max(1, 4 + Veil Affinity) × Level** and three disjoint VP states. [Turn AP](../rules/05-combat/action-categories-and-physical-tempo.md) gives **30/36/42 AP** L1–3, and **24 AP** for Medium Physical, Projection and General Tempo actions.
- Restricted **8-emotion / 8-Pillar / 6-Strong + 2-Plausible pilot links** are reused from [the accepted readiness candidate](b04-b05-mvp-pilot-roster-gifted-anointed-readiness-v0.md#gifted-pilot-candidate--eight-authored-aspects-source-legal-6s2p), not copied as mandatory links for every Medium Gifted. Fear → **Earth / Fortification (Internal)** and Trust → **Kinship / Guardian (External)** are authored connections. This design grants neither Stone Skin nor Protective Ward for free. Ordinary existing techniques still require their exact linked Aspect, action, price, targets, mode and responses; Universals remain independent.
- No High Gifted **Surge** or Low Gifted **Anchor** is inherited. This proposal is **not** an eighth structural L1–3 character build: no fresh Medium Talent, Training/weapon choice, complete starting sheet, noncombat certificate or B06 native actor has been authored here.

## 2. Proposed Ward Form — exact identity and placement

| Field | **Candidate `MG-WARD-01` — self-anchored Ward Conduit** |
|---|---|
| Origin / acquisition | **Medium Gifted Focus-only Conduit expression proposal**; not an individual base-Tier-1 technique identity or a normal spell profile |
| Form and fixed anchor | **Ward**; `self` (the Gifted's own living position/body). Its Form and anchor do **not** move to another host when emotion changes. No weapon, held item, remote ward, stationary field or independent follower is granted |
| Conduit slots | One at L1–2; two at L3, counting Dormant Conduits equally; each established instance holds its own Grade/VP |
| Grades | Grade I = **1 Committed VP**, II = **2**, III = **3**; all three available from L1; Grade persists unchanged when emotion retunes |
| Initial establishment action **(PROPOSED, not canonical yet)** | **One General Tempo Action: 24 AP**, plus Grade's Committed VP, on a conscious own turn. There is no 0-AP initial placement or automatic free persistence just for choosing Medium Focus |
| Established duration **(PROPOSED)** | Maintained while anchor exists and caster is conscious and keeps the Grade VP Committed. End on genuine loss of host/consciousness, voluntary release or an applicable channel break; Committed VP returns to Available but already Spent VP is not refunded |
| Target geometry **(PROPOSED)** | Anchor remains caster even when external Trust pulse helps **one other allied creature** at **one orthogonal map square (not a diagonal)** at the event; no wall-penetrating magical reach or extra body square may be assumed. Native G1 must validate distance, source identity, intervening solid blockage and actual ally relation |
| Emotions with authored output | **Fear/Earth/Fortification → Holdfast**; **Trust/Kinship/Guardian → Shared Reserve**. All **other six pilot emotions (or unset emotion) → Dormant**, with Committed VP still held |
| Trigger and cadence **(PROPOSED)** | **Pulse: automatic on the first actually eligible post-mitigation damage packet per Conduit per Emotion Window**. A fully prevented/zero packet does not consume Pulse. The same damaging event may consume **at most one** Conduit Pulse; evaluate older Conduit before newer. Unused Pulse expires with its Emotion Window; no banking |
| Grade magnitude **(PROPOSED)** | Grade **1/2/3** prevents up to **1/2/3** of *one* qualifying damage packet after its ordinary defenses, armor and source resistances. It cannot create HP, Vigor, a second pool, temporary HP or negative damage |
| Delivery and action **(PROPOSED)** | Persistent finite prevention, not an attack, cast, extra Reaction, off-turn AP spend, interception, Guard/Dodge assignment or another hit/critical roll. It does not block or retarget a successful attack and cannot grant free Shield Guard or spell defense |
| Stacking **(PROPOSED)** | Only one Ward Conduit Pulse per original damaging event even with two L3 instances. Existing physical armor/one-highest applicable resistance must resolve exactly once before the Pulse. No duplicate Conduit mitigation of the same packet. Interactions with other *finite prevention budgets* must be ordered in a later native G4 adapter before this is certified |
| Explicit exclusions | No Ward Form outputs for Joy, Sadness, Anger, Surprise, Disgust or Anticipation; no Contact/Motion Form; no Tier/Used-Tier scaling; no independently cast spell, damage attack, crit, heal, regeneration, poison immunity, reaction, or cross-Aspect effect |

### Candidate expressions (NOT yet approved numerical game effects)

| Active Emotion / exact link | Name / cadence | Eligible output | Ineligible output |
|---|---|---|---|
| **Fear → Earth / Fortification** | **Holdfast**; **Pulse 1 per Conduit per Emotion Window** | Prevent `min(Grade, remaining damage)` from the **caster's first direct Physical-type HP packet** after the source's own Armor and highest eligible resistance. Physical includes Cut, Piercing and Crush; this is a **one-hit finite absorption**, not Stone Skin's sustained HP resistance | **Fire**, Electrical or other elemental HP; **Vigor damage**, any ally, wounds/condition damage not resolved through an eligible Physical HP packet, extra Guard/Dodge, persistent Stone Skin |
| **Trust → Kinship / Guardian** | **Shared Reserve**; **Pulse 1 per Conduit per Emotion Window** | Prevent `min(Grade, remaining damage)` from the **first actual direct Vigor-damage packet** to **one other allied creature** in the stated orthogonal adjacent zone at the moment of the event. If no qualifying ally/event, no Pulse | **Self**, enemies, nonadjacent allies, HP harm, toxic/milestone Vigor loss without the explicit `Direct Vigor` damage type, Reactive Protective Ward, ward shield/attack defense and extra Reaction |

These are two **separately proposed Conduit expressions**, not permission to attach a free Stone Skin Primary/Secondary, Protective Ward Reaction or Vital Shelter maintenance. They use one anchored Form but differ in Aspect, eligible recipient and resource. One Active Emotion at a time means there is **never simultaneous Fear and Trust output**, even with two Conduits. An out-of-Aspect ordinary spell cannot be cast merely because an older Conduit still exists.

## 3. Window lifecycle and action budget

1. The actual [Emotion Establishment Step](../rules/08-archetypes/gifted.md#emotion-establishment-step) begins **one** new Window. Conduit Grades, anchors, counts and Committed VP survive. Retune **immediately** to the matching authored expression or **Dormant** without AP/VP change, and refresh the *one* bounded Pulse eligibility by Window, not by target/attack/round or a manual cast.
2. The Gifted can choose **unset** Active Emotion at Step 5. A first otherwise-lawful linked-Aspect technique later establishes that linked emotion at no extra AP **in the same Window**; only then do eligible Conduits retune. A Universal operation never establishes Active Emotion by default. Changing emotion mid-Window by an actual authorized transition similarly retunes without creating another Pulse.
3. Establishment of a **new** Ward (candidate: 24 AP and 1/2/3 Committed VP) is a separately paid own-turn action. It is *not* a Reconduction and cannot reuse a deleted source key or make a dormant expression active without a suitable emotion.
4. Reconduction is **24 AP + 3 Spent VP**, **then** any Grade commitment increase/decrease. Preflight `Available VP ≥ 3 + max(new_grade − old_grade, 0)` *before* any AP/VP mutation; do **not** use the future downgrade refund to fund the 3 Spent VP. A change of Grade in the current Window retains that Conduit's already-consumed Pulse; otherwise, a Grade toggle could repeatedly mint mitigation.
5. No free release–recreate loop may simulate an instant zero-surcharge Reconduction: voluntary release terminates its specific Conduit; a new instance requires the separately paid establishment action and complete revalidation. **Review gate:** decide whether same-turn release/re-establish is allowable or needs a minimum lockout before canonicalizing this candidate.
6. At L3, **two** Conduits may be established across **two paid 24-AP actions/turns**: 42 AP cannot pay 48 AP in one Turn. A single damage event invokes **at most one** eligible Conduit Pulse; two Conduits may protect **two separate** events in the same Window if both still have a Pulse. Do not multiply a full defensive technique by Medium Tempo.

### VA 0 resource arithmetic (locked baseline; candidate placement costs)

| Level | Max VP | Slots | If all slots Grade I | If all slots Grade III | Turn AP / one initial 24-AP placement |
|---:|---:|---:|---|---|---|
| **L1** | **4** | **1** | `Available 3 / Committed 1` | `Available 1 / Committed 3` | 30 AP → 6 left |
| **L2** | **8** | **1** | `Available 7 / Committed 1` | `Available 5 / Committed 3` | 36 AP → 12 left |
| **L3** | **12** | **2** | `Available 10 / Committed 2` | `Available 6 / Committed 6` | 42 AP → 18 left |

**At L1 Grade III** (3 Committed / 1 Available) cannot afford an unrelated normal **2-Spent-VP** technique even when the matching Active Emotion and 24 AP would otherwise permit it. **Grade I** leaves 3 Available and can fund one such actual source-eligible technique on a later turn (assuming unchanged VP). Unspent Conduit commitments are not free recovered VP at a six-hour recovery interval; the 6-hour recovery rule restores **Spent**, not **Committed**, VP.

**L2 worked Grade I → II Reconduction:** start with Max 8 / Available 7 / Committed 1 / Spent 0; on a later turn pay **24 AP + 3 Spent VP + 1 additional Committed VP**, leaving **Available 3 / Committed 2 / Spent 3**. The same attempt at L1, where Available = 3 and cost = 4, must fail *before* any AP/VP debit. Conversely L1 Grade II → I fails at Available 2: the **1 future released VP** cannot pay the required initial 3 Spent VP. Genuine later VP recovery/release may alter affordability, but is not supplied by this isolated witness.

## 4. Worked proposed event traces and countercases

| Scenario | Expected bounded outcome |
|---|---|
| L1 Fear/Grade II, caster takes 5 Physical HP after Armor/resistance | **2 HP prevented** on first event, 3 applied by a future native executor; a second eligible event in this Window receives 0 Ward prevention |
| L1 Fear, 5 Fire HP or 4 Direct Vigor to caster | **0 prevented**; unlike Stone Skin, Fear Ward does not protect Fire HP; unlike generic Vital Shelter, it does not protect Vigor |
| New Window, Trust/Grade II, adjacent *other* ally takes 6 **Direct Vigor** | **2 prevented**, then Pulse consumed; caster/not-adjacent/HP/toxin source cannot trigger this profile |
| New Window Joy with the same Grade II | **Dormant** with **2 VP still Committed**; a genuine Joy-linked Conjure Flame remains separately priced and source-bound |
| Begin with unset emotion, first legal Trust-linked Aspect technique later establishes Trust | Conduit **automatically retunes** within the **existing** Window; no Pulse duplication or additional AP/VP from retuning |
| L3 two Grade III Wards and first eligible 9-HP event | **3 prevented, not 6** on that event; a *different* subsequent event may use the other remaining Conduit's Pulse |
| L2 Grade I has already pulsed, then pays legal Grade II Reconduction | It remains **used for this Window**; no second mitigated event until next genuine Window |
| Bad form/anchor/Grade, >slot cap, invalid eligible recipient/event, resource shortage | Reject or Dormant **before** mutation, with no fabricated defense/VP refund/damage |

## 5. Explicit implementation / approval gates

This PR provides a **candidate** `MediumGiftedWardDesign` isolated budget/event model with focused regression tests. The model deliberately **does not install G0–G5**, read world geometry, adjudicate direct/typed G4 packets, observe actual enemy turns, open a real Reaction window, invent a Focus character sheet, or output a win rate. Its `pulse()` receives a caller-supplied post-mitigation amount and an already-attested `adjacent` flag, and thus **cannot certify** actual damage prevention; real host/geometry/authentication/mitigation gates remain required.

Before promotion from design to canonical rules, review these **new choices** (not locked by Gifted Foundation): **(a)** Ward self-anchor and proposed 24-AP initial establishment; **(b)** Fear self Physical HP / Trust other-ally direct-Vigor Grade 1/2/3 prevention profiles; **(c)** no duplicate mitigation per event, eligibility/line and post-Armor/resistance precedence; **(d)** maintenance/unconsciousness/release timing and release/recreate anti-circumvention; **(e)** interactions with Stone Skin, protective Reaction and other finite prevention; **(f)** world/exploration cadence and multi-creature topology; **(g)** two-Focus level/encounter comparative balance with legal action and VP costs. No unseen choice is silently blessed as approved canon.

A subsequent **Medium Gifted L1–3 character build/verification PR** must independently author sourced 28-point Abilities, legal 4/2/2 Learned Discipline families, weapon/Talent/gear, all eight emotion links at creation, VP/AP/level advancements and actual source-authorized combat/noncombat access. A separate **native Conduit integration** must use real G0 Step-5 emotions and G1 geometry, G3 commitment/release, G4 packet preflight and protected delivery, then legal G5 interaction/attrition under explicit policy. Only then can a complete independent Focus certification be evaluated.

**MVP ledger stays:** **12/12** architectures; **7/12** structural pairings; **0/12** independently certified; **0/6** strict exit gates; **3/7** blocker definitions closed; **0** representative encounter packs; B06 G0–G8 taxonomy unchanged. Existing **13 Tier-1 technique identities / 10 of 24 covered Aspects / 14 absent** remain unchanged; the Ward proposal is not a new Pillar technique identity.

## Reproduction

```sh
python -m unittest tests.test_b05_medium_gifted_conduit_design_v0 -v
python -m unittest discover -s tests -v
```