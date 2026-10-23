# B06 G7-H — Complete Mixed-Party Encounter Certification v0 (bounded terminal matrix)

> **Bounded terminal-path certificate, not representative encounter calibration.**
> Source-native Level-2/3 four-PC (A/B/R/F) Hunter scenes can now reach
> independently authenticated Hunter death, full-party death and genuine
> opposed party withdrawal. The game rules, Hunter CR, original G7-F
> sampling, and historical Phase 3 results remain unchanged. The milestone
> name denotes the *target* of eventual complete encounter certification;
> this first executable acceptance slice is explicitly narrower.

## Why G7-H is needed

G7-G proved a source-paid Hunter multi-target wipe and opposed living-Hunter
exit. G6-D separately proved a Hunter loss to the mixed A/B/R/F party.
Those earlier one-off scripts did not together constitute a reviewed,
single-source **three-terminal pack** with a shared roster, consistent
policy provenance, genuinely different participant roles and a strict
cross-branch acceptance boundary.

The new [G7-H terminal pack runner](../../scripts/b06_g7h_mixed_encounter_certification_v0.py)
replays **three independent native encounters** for each L2 or L3
four-person source scene. Each branch begins with the same G6-C authored
initial team positions, sources and initiative order. They are distinct
fixed tactical policies, **not** counterfactual branches copied from one
game state, unbiased seed samples, empirical player strategy, or a CR
estimation dataset.

| Native policy | Real source action and terminal | What it proves |
|---|---|---|
| `mixed_victory_rite` | G0-paid Hunter Bites, A/B paid melee, R Low Priest actual **Chosen, Maintained Self Guided Regeneration Rite** (1 committed VP) replacing its otherwise missed Round-1 shot, two F High Scholar genuine G3→G4 Thrown Flame hits; R independently committed Bow lethal hit in Round 3; G6-D Hunter death terminal after genuine Round End | Four mixed source identities participate, authentic Priest Rite/VP and Fire/Bow/HP, genuine Hunter defeat |
| `hunter_multitarget_defeat` | G7-G rigid Hunter G1 head-forward cautious pursuit, one paid natural Bite per turn, G4 wounds/Dying and actual lethal Bite per player; native G7-C all-dead terminal | A *positive reachable* multi-target adverse terminal rather than an inferred 0-HP wipe |
| `opposed_living_hunter_withdrawal` | G7-G Round-1 contact, Round-2 paid Hunter chase/pursuit Bite, each party member's independently authored G1→G4.5→G5 border exit, then G7-C whole-party receipt | Genuine opposed **scene-local** party departure with Hunter still alive |

The first branch reuses the original [G6-D source victory](../../scripts/b06_hunter_completion_g6d_v0.py)
with an **opt-in** G7-H R Rite replacement on Round 1. All previous
default G6-D callers and test fixtures remain unchanged; the R Rite
does not create additional turns, free MP/AP/VP, new Prayer access for
A/B, new healing or an extra shot. The other two branches reuse the
existing [G7-G source-native implementation](../../scripts/b06_g7g_hunter_pursuit_terminals_v0.py)
without modifying the established terminal or actor contracts.

## Certification algorithm and fail-closed limits

`run_pack(level, seed)` certifies **only** the source-bound terminal
matrix when all three branches pass independently:

1. The exact original G0 scene, order **Hunter/A/B/R/F**, actor source
   identities, source digests, L2/L3 level, seed and scenario must match.
2. The native policy marker (`g7h_pack_policy_selected` for victory,
   `g7g_policy_selected` for defeat/withdrawal) must appear **exactly
   once before the first actual turn or paid action**. Relabeling a
   mutable report's outcome or policy cannot substitute for the marker.
3. The original native G0 event indices, SHA-256 digest, every source
   HP/death transition, the final snapshots, full Initiative chronology
   and completed Round Ends must reconcile. No late open turn, paid
   action or unresolved G5 sequence can be declared a completed branch.
4. Each branch must contain exactly **one** canonical G6-D or G7-C
   terminal of its authored kind. Its returned terminal reference must
   point to the original event—not a new G7-H or fabricated ending.
5. G7-H independently checks decisive native evidence: R actual Chosen
   Rite and Bow, F two real Fire packet deliveries, A/B melee and Hunter
   Bite for victory. **Each lethal Hunter Bite** must retain one uncancelled
   paid G0 Physical Action, its original G5 declaration, a hit-producing G5
   roll, the synchronous G4 damage transition, a matching G4.5 attested hit,
   and a final G5 `melee_resolved` result bound to the **same source action,
   victim and round**. G4 cause text and the terminal's lethal indices alone
   cannot certify a death.
6. For opposed withdrawal, **both** native Hunter Bites must resolve in
   Round 1 and after Round-2 pursuit respectively. The signed pursuit event
   must reference actual paid G1 steps; all four exits must independently
   bind the **previously authored actor/policy/border square** to the final
   same-turn G1 cautious translation, the original matching G4.5 withdrawal
   attestation, and the G5 exit, in strict event order. The final G7-C
   `member_exits` list and G7-G verification indices must match those
   independently reconstructed receipts. No post-exit actor movement,
   damage or new turn is accepted.

**Exact authored A/B defender and miss policy (Codex follow-up).**
For the G6-D victory witness, Hunter must **Dodge** both paid Vanguard
sword sequences (original source Dodge 14 at each Round Begin, followed by
2 Dodge Pressure), then **Take Hit** against both Guardian mace sequences
while preserving that same pressure and source Guard remainder. The
original G0 declaration, actual defense assignment, defense value,
resource receipt, paid action, attested G5 sequence and final roll must
agree with the **independently authored G6-C policy**, not just with each
other. Guardian's Round-1 natural-1 **miss** still requires its paid
20-AP action, both **legal** G0 response-window rechecks, genuine ready
receipt, original G5 roll and uncancelled `g5_melee_resolved` miss; replacing
it with cancellation or an illegal recheck cannot certify. This is
checked for **all four** A/B actions across the two source rounds.
For every terminal branch, `encounter_created.detail.policy` and
`objective` must also equal the independently reconstructed **original
G6-C scene**, even after a digest is recomputed; the later G7-H/G7-G
marker cannot amend the genesis policy.

Additional P1 authentication (this review round): A/B source melee
must reconcile each paid 20-AP action against Step-4 original Turn AP
and remaining AP; G7-G withdrawal must retain actual Hunter head-forward
contact at the **replayed**, not just receipt-claimed, Round-2 pursuit
footprint and at paid Bite rolls; every native regeneration Step must
stay within independently sourced HP maximum, Regen throughput, Vigor
availability, Dying and Step 2 timing. This bounded scenario does not
authorize spontaneous external heals or unspecified voluntary wound
repair. The G6-D victory terminal must match the **entire** authentic
source receipt, including original party roster, source digest, native
HP and round, cause and outcome—not merely its lethal event index.

A mislabeled, incomplete, role-substituted, stale, unsigned or
nonterminal result fails closed.

### G7-C signed terminal and closing geometry (Codex P1/P2)

For **both** G7-C terminal paths, the independent verifier requires the
**exact complete native signed event schema**: original party roster,
four authentic `lethal_damage_indices` or `member_exits` in their
canonical field, source-completed `round`, and `hunter_cr: null`.
The terminal event itself must be at that completed G0 round, outside
the actor's turn and after the final `round_end`; the separate returned
terminal receipt must also have the exact source field set, not merely
a matching event index. An extra, removed or substituted signed field
cannot become authoritative by recomputing SHA-256.

For **withdrawal**, G1 replays all authored cautious movements from
the original source grid and actor footprints. The result is compared
with `final_state[actor].occupied` for **each of the five original
actors**, not just with the signed border-square exits. Forged in-grid
positions, out-of-grid positions, altered Hunter footprint, omitted or
extra occupied cells fail even when the original ledger and digest are
otherwise genuine. The G7-G scene-exit limit is unchanged.

### Final source-payment and roll audit (Codex P1)

The G7-H attestor independently rederives the Bow shot's natural-1 rule,
source +4, effective ranged defense, natural-20 confirmation tier and
permitted original G2 outcome. Both the G2 shot and G6-D adjudication
must match that computation, not merely each other's mutable labels.
The Hunter's paid Bite chain must similarly reproduce its **+6 source
bonus**, original native Take Hit defense, +6 attack total, natural-1
auto-miss, natural-20 confirmation tier and its 24-AP source payment
before a successful G5/G4.5/G4 chain is counted.

Each **Chosen R Guided Regeneration** instance and each of the **two
F Thrown Flame** launches requires one *same-actor, same-round/turn,
strictly ordered* matching G0 Projection AP payment **and** a distinct
G0 \`vp_transition\` of the source-correct kind and exact quantity:
R commits **1 VP** (30 AP); F spends **2 VP** (20 AP) per T1 launch.
The verifier also reconciles total G0 source VP transitions/release
against real final actor VP availability and commitment. Relabeling
payment events and recomputing the ledger digest cannot preserve
certification. These checks do not change any G0–G7-G source mechanics
or the terminal certification boundary.
 Ordinary nonterminal scenes must retain
their unresolved/censored classification elsewhere; G7-H cannot call
an unfinished run a victory or resample until a favored outcome appears.

**Positive acceptance field:**
`bounded_terminal_matrix_certified=true` means **three authentic
terminal types for one explicitly supported L2/L3 × P4 source scene,
under three fixed authored policies**. It is *not* equivalent to
`complete_party_pack_certified`, which remains `false`.
`full_representative_encounter_pack_certified=false`,
`representative_encounter_calibration_accepted=false`,
`sampled_win_rate=null`, `confidence_interval=null`,
`human_GM_policy_weights=null` and `hunter_cr=null`.

The G7-G defeat script uses intentionally extremal confirmed critical
faces and a mostly passive party. The withdrawal script uses a source-
authored Cautious border path, not a universal safe retreat. The victory
uses fixed source dice and lacks independently confirmed mid-combat
protective intervention/healing. Fixed encounter seeds identify G0
events; **replaying multiple seeds is not a representative probability
experiment**.

### Codex P1 provenance hardening — lethal Bow and G1 withdrawal continuity

The G7-H independent attestor now verifies the victory terminal's
`lethal_damage_index` points to the **single genuinely lethal Hunter
`g4_damage_applied` event**, not an earlier nonlethal hit. Its native
`cause` and unique `event_key` must reconstruct the exact
**G0-paid Physical Action → G2 Bow declaration → launch → shot resolve →
G4 lethal damage → G6-D Bow adjudication → signed G6-D terminal**
for the same real Archer turn. The terminal's own `source_event_cause`,
the Bow damage summary and HP-loss transition must agree. A forged
terminal pointer or substituted Bow action/shot fails even when the
attacker recomputes the public ledger SHA-256.

Withdrawal proofs additionally replay **every** G1 movement step—Hunter
translations/pivots and each PC's intermediate and final steps—against
a freshly authored G6-C map and initial source actor footprints. Each
recorded old coordinate must equal the preceding genuine position;
direction, step kind, cardinal Hunter anatomy/pivot, target footprint,
map bounds, collisions, Cautious cost and remaining own-turn MP must
agree with G1's original `preview()` contract. Unsupported alternate
movement modes fail closed. The final G7-C exit still requires its
separate movement/G4.5/G5 signed receipt. Neither a changed
`old=[[100,100]]` coordinate nor a teleport-like translation can
obtain a certificate simply by recalculating a digest.

These checks validate ledger **consistency**, not the security of a
public unkeyed digest against a fully fabricated, internally coherent
history; trusted execution remains essential for final certification.

## Codex P1/P2 correction — independently derived dice, source payments and chronology

The G7-H *fixed-dice* witness now checks the original authored inputs
against every claimed decisive native G4 packet, not just against editable
G6-D/G5/G3 summaries or the ledger hash:

- **R Bow lethal:** the actual G0 Physical action must debit **20 AP** and
  its `ap_remaining` must follow the previous source `turn_resources`
  and any earlier paid actions. The sourced G6-D finisher is natural
  20, confirmation 20, two critical d4s `(4,4)`, damage d4 `4`.
  Its exact **14 Piercing HP** packet, bypassed Armor-3 via Bow
  Penetration-3, G4 floor-clipped HP loss and returned G6-D damage
  receipt must all agree. Ordinary or natural-1 Bow hits cannot claim
  the devastating packet even if G2 and G6-D summaries are edited
  together. This is explicitly **not** a general Bow roll generator.
- **Hunter Bite (all three policies):** victory's genuinely successful
  Round-2 Bite now passes the exact same original G0→G5 declaration,
  24 AP cost and remainder, defense, native d20, G4 source-profile
  packet, G4.5 and G5 completion chain as defeat/withdrawal. The original
  G6-C victory script uses `10` / d6 `1`; G7-G defeat uses natural
  `20` / confirmation `20` / d4 `(4,4)` / d6 `6`;
  opposed withdrawal uses face `12` / d6 `1`.
  Accordingly the source B06-AT-04 **3+d6 Piercing Pen-1** raw packet
  is exactly 4, 17 or 4 before verified source armor mitigation,
  respectively. Editing an attack to an ordinary hit while preserving
  the devastating fatal packet cannot certify.
- **F Thrown Flame:** each already AP/VP-attested G3 launch binds to
  **exactly one synchronous G4** event with original `g3:thrown_flame`
  cause, caster turn, source event key, original **Fire HP** and
  **Direct Vigor** raw/mitigated packets from the launch's
  verified d20, d8, critical dice and Used Tier. Both HP and Vigor
  transitions are checked. Clearing the packet list or relabeling a
  cause fails closed even if HP summaries are left intact.
- **G0 receipt chronology:** all `round_begin`, `turn_start_expiry`,
  `turn_end` and `round_end` events are replayed in source
  Initiative order with their original round and turn fields. A
  rehashed `round_end.round=999`, wrong actor, repeated round or
  post-Round-End open turn cannot be certified.

These are source-model *witness attestation* rules. They do not extend
the combat engine's universal ability/damage tables or change the
historical Phase 3 digest. Requiring authored dice for this cohort is
intentional; generalized unscripted player/GM roll distributions and
independently representative encounter samples remain future gates.

### Codex P1 correction — source-backed Spell AP, digests, and A/B typed damage

G7-H no longer treats declared Spell AP as sufficient payment: each
**Chosen Guided Regeneration Rite** and each separately launched **Scholar
Thrown Flame** traverses the same native `_paid_action_ap` reconciliation
used for the finishing Bow shot. The verifier requires one own-turn
`turn_resources` receipt, checks source-authored starting Turn AP against
an independently instantiated G6-C sheet, consumes earlier paid actions
in order, and requires the exact recorded `ap_remaining` after each
Projection Action. Zero-AP / inflated-AP receipts, negative funded balances
and forged remainders are rejected even when the ledger is rehashed.

Actor identity now binds **all five original G0 source digests** (Hunter,
A, B, R, F) and the entire authored genesis source roster against fresh
`mixed_scene` fixture construction. Agreement among editable genesis,
snapshots, G5 action labels and G4.5 `attacker_source` /
`target_source` strings cannot impersonate a real fixture.

A/B actual hit validation now calls the source G4
`_profile_hit_packets` and `_mitigate_hp` on independently recreated
actors and the fixed G6-C `POLICY` attack/damage dice. It verifies the
complete **Cut/Crush** HP packet structure, source die + Strength,
penetration against Hunter Armor 3, effective HP mitigation, source
`g4_damage_applied` event and actual clipped HP transition. The native
G4.5 and G5 cached results must agree with the independently derived
`hp_packets` and loss. Changing `raw` and `mitigated` to an impossible
value while preserving the four-point HP delta cannot certify.

Dedicated adversarial tests cover both separate Flame turns, the Rite,
each of five fixture digests and both A/B profiles (including tampering
with armor, damage type, extra packets, and cached summaries). This is
**audited source provenance for the fixed bounded pack**; it does not
expand coverage to arbitrary dice, new profiles or representative CR.

## Player/GM tactics and MVP boundary

- **Playable source role diversity demonstrated:** A/B martial proxy
  actions, R Low Priest Chosen Self Rite and sourced Bow, F High Scholar
  actual Thrown Flame, Hunter sourced Bite. The R Rite uses its real
  maintained VP reservation, not invented Priest preparation or A/B
  casting access.
- **Outstanding combat integration:** A/B are still **physical-only
  proxies**. General Priest Heal/Rite/Exaltation, dynamic full response
  windows (Prepared Body/Reactive Shield) *within these terminal paths*,
  mixed attacker pressure, varied terrain, active GM/player policy and
  complete long-clock safe aftermath are **not certified** by this pack.
  Existing G7-D protective and G7-E forest/Pounce observers remain
  independent, not silently pooled.
- **Outstanding party configurations:** The matrix runs for **four**
  original A/B/R/F members at L2 or L3. Three-PC victory/defeat/exit
  variants have separate G7-G evidence, but no approved three-terminal
  G7-H source pack. Alternative frontlines and broader Focus coverage
  remain separate gates.
- **Scene-local exit:** G7-C proves a legal **authored border exit** after
  actual opposition; it does not establish that the surviving Hunter
  cannot pursue or track the party after leaving the scene.

### Codex P1 follow-up — Bow arrow conservation and fixed Flame face identity

The **victory certificate is a fixed G6-C/G6-D policy witness**. A
syntactically consistent, rehashed native ledger is *not* enough when it
substitutes different source-dice choices or consumes no physical arrow.

- **R Bow physical inventory:** derive the starting R ammunition from the
  actual B05 Bow Vanguard L2/L3 sheet (not from the mutable report), and
  require the pre-action R snapshot to equal that quantity. The original
  R **Round 1 Chosen Rite** spends no arrow; **Round 2** makes the original
  G6-C natural-1 missed Bow shot; **Round 3** launches the 20/20 lethal
  G6-D finishing Bow. Both authentic rounds must have exactly one ordered
  **paid Physical Action → G2 one-arrow declaration (`ammunition_selected=1`)
  → G2 launch (previous balance minus one) → G2 resolution
  (`ammunition_spent=1`)**, and the final R snapshot must equal the
  independently reconstructed **starting inventory minus two**. Zero-arrow
  finishing shots are rejected even when the declaration, launch, resolution,
  final snapshot and SHA digest have all been edited consistently.
- **F source-dice identity:** each of the separately AP/VP-paid Round-1
  and Round-2 Thrown Flame launches must carry its *own* independently
  authored G6-C Scholar **(primary d20, vigor d8) = (12, 3)**, keyed to the
  native round. The existing defense math and exact synchronous G4 Fire/
  Vigor packet validations also apply. A legal alternate d20 hit (e.g.,
  10+5) or d8 with identical resulting damage (e.g., 2 instead of 3)
  cannot be relabeled as this fixed witness simply by rehashing the ledger.

Adversarial tests cover Codex's coordinated zero-arrow forgery, missing or
misordered source stages, incorrect opening/closing stock, either Round-2/3
ammunition debit, and independently substituted Scholar d20 and d8 faces
in either Round 1 or Round 2. Both actual L2 and L3 source traces must
continue to certify with no rule modifications.

### Codex follow-up — defense declarations, terminal ordering and wipe receipts

The completed source-chain audit now rejects three additional classes of
post-hoc ledger forgery, **even when the attacker recomputes the canonical
ledger SHA-256**:

1. **Every certified Hunter Bite** must match its original G0
   `attack_sequence_committed.defenses[position]`, the matching
   `defense_assigned` receipt, and the exact
   `hunter:<original-target>:<position>` attack key. Binding the roll and
   source-paid action alone is insufficient; a re-labeled Guard is not the
   originally declared Take Hit choice.
2. **Victory terminal ordering** requires the genuine
   `g6d_hunter_defeat_attested` event *after* the last completed native
   `round_end`, just as the G7-C defeat/withdrawal terminals do. A terminal
   inserted after the final turn but before its Round End is premature.
3. **Defeat verification receipt** is compared as an exact original-schema
   object against native proof: full original party list, unique G4 fatal
   Bite indices in source-party order, native terminal pointer, all distinct
   Hunter targets reconstructed from the actual chronological target
   selections and prior deaths, and the still-living Hunter. The chosen
   target must match each real pursuit event and first still-living source
   party member; changing both a target and a summary cannot invent a
   different target history.

Adversarial tests mutate individual Bite declaration defense slots and
attack keys **across all three terminal policies**, move the G6-D terminal
before its last Round End, corrupt each of the four G7-G defeat verification
fields, and forge target-selection and verification records together. These
are strictly authentication improvements; no combat rule, dice or policy
selection changes, and no new representative sample is claimed.

### Codex follow-up — Hunter miss AP and complete actor snapshots

- **P1: the missed Round-1 Hunter Bite is paid.** G7-H audits *both* original
  victory-mode Hunter G0 physical actions against native current-turn resource
  grants, 24-AP debit, 18-AP remainder, distinct source declarations,
  defense-assignment receipts, and exactly one G5 roll/resolution each.
  The authored first-round **natural 1** is a paid **miss**, not a
  paid hit: it cannot carry G4 damage or a G4.5 hit. The already established
  second-round hit remains independently verified through its G4/G4.5
  outcome. Rehashing a trace with `ap_spent=0` and `ap_remaining=42`
  on the Round-1 miss must fail.
- **P2: authenticate every exposed actor snapshot field.** At encounter
  creation G7-H compares the *entire* initial serialized roster against a
  fresh exact G6-C source fixture, including maximum HP, source identity,
  initial wounds, geometry and status. At close, the verifier enforces the
  exact serialized field schema, derives `dying` from final HP/death,
  preserves fixture `source_id`/`source_digest`/`hp_max`, replays all
  actual G1 footprints in every policy, and reconstructs the complete
  wound inventory from the unique synchronous G4 wound-creation receipts.
  Wound identity, severity, repair requirement and initial progress
  are checked, while the existing HP/Vigor, VP, ammunition and
  regeneration audits still independently verify their balances.
  No unmodeled wound repair, external heal or post-fight status is accepted.

Additional regressions explicitly forge the missed Bite's AP debit,
remaining budget, and resolution; delete a source lethal wound, alter
its fields, falsify `dying`, `hp_max` or `source_id`, add unexplained
snapshot fields, or tamper with initial source data. All such trials must
fail closed even with a recomputed ledger digest.

### Codex P2 follow-up — source-derived wounds and complete exit receipt

A wound's own `g4_wound_created` attributes are **not** independent
authority. The G7-H closing-state verifier now derives whether a wound
must exist, its Serious/Severe/Critical band and repair requirement from
the independently authenticated source attack/critical and original
G4 before/after HP (including the lethal `-HP max` floor). The exact
location comes from the preauthored G7-G Bite or G6-C Flame wound d20,
mapped through native G4 `LOCATIONS`; the trauma follows the validated
typed source HP packet (Piercing or Fire), not an editable wound field.
All newly minted G4 wound IDs must follow the global original
`G4-W####` allocation sequence, with exactly one valid created/damage
pair. Changing even a *valid* wound band, or jointly rewriting the G4
event, G4.5/G5 result and closing snapshot, cannot downgrade a
Devastating Hunter Bite wound.

The final G7-G opposed-disengagement verification event is also checked
by **exact whole-object equality** against native proofs: the G7-C
terminal index, real Round-2 G1 pursuit index, both real paid Hunter Bite
resolution indices, four independently authenticated G5 border exits,
living Hunter closing HP/death, the authored scene-only boundary
`authored_G7C_scene_exits_only`, and the explicitly unresolved
post-scene-world-pursuit flag. Unrecognized or missing receipt keys fail
closed. Neither correction broadens the witness into a general healing,
restoration, safety, or encounter-difficulty claim.

## Codex P1 — Legal Bow and G1 movement response-window provenance

G7-H treats `trigger_rechecked_after_responses.legal=false` as a
**cancellation**, even when a later G2 launch/G4 death or G1 move/G5
exit event remains in a tampered ledger with a recomputed SHA-256.
Those later receipts do **not** override the native G0 trigger state.

- **Lethal R Bow:** reconstruct the exact source G6-D one-shot trigger
  from the native seed, combat round, archer and Hunter. Require one
  `response_window_open`, true
  `trigger_rechecked_after_interceptions`, true
  `trigger_rechecked_after_responses` and
  `trigger_ready_to_resolve`, all once, in that order, on the Archer's
  actual turn **after** the real G2 Bow declaration and **before** the
  real G2 launch. Reject cancelled, duplicate, foreign-trigger,
  intercepted or spontaneous response receipts in this authored
  no-response witness.
- **Every G7-G Cautious G1 step**, not just final border exits: the
  actual `g1_movement_step` must immediately follow its own G0
  `trigger_ready_to_resolve`. Verify that window's original opening
  has the authentic `g1:<actor>:step:<opening-index>` key; both
  legal rechecks are true; open → rechecks → ready have no missing,
  extra, duplicated or cancelled stage. A movement cannot borrow
  another turn's or another step's valid ready receipt. The existing
  independently rebuilt G1 geometry/MP replay and G4.5/G5 border
  receipt checks still apply.

Adversarial tests cover false rechecks on the finishing Bow and **all
four** closing party border moves (with their ledger hashes recomputed);
wrong/duplicated ready receipts, invalid trigger bindings and authentic
L2/L3 seed-0/seed-17 positive traces. These are provenance checks on
the already-supported G0/G1/G2 rules, **not new Opportunity,
Interception, Ranged or scene-exit mechanics**.

## G7-H response-window, Turn AP and Hunter venom reconciliation

Accepted Hunter Bites now have an **action-keyed native response-window
witness**, not merely a paid G5 roll and G4/G4.5 outcome. For every Hunter
hit, and the original victory Round-1 miss, the exact trigger
`g5:melee:<paid-action-index>` must have one original `response_window_open`,
a **true** `trigger_rechecked_after_interceptions`, a **true**
`trigger_rechecked_after_responses`, and
`trigger_ready_to_resolve`, all in order on the same original Hunter
turn **after** source G5 sequence attestation and **before** its roll.
A cancelled, fabricated, duplicated, or substituted response stage is
not a legally resolved Bite. The three authored witnesses all decline
spontaneous responses; they cannot silently contain an additional
Interception or Reaction while claiming this fixed policy.

The audit also independently replays **every actor's Turn AP** across
each native Initiative turn. G0 `turn_resources.ap` must equal the
original L2/L3 source allowance for a conscious actor (zero if Dying or
dead), each `action_committed` consumes the correct source Physical,
Projection, General, or Full AP amount, every interim `ap_remaining`
must equal the paid balance, and `turn_end.unused_ap` must equal the
actual remaining amount. A Hunter with 42 AP after one paid 24-AP Bite
must record **18 AP**, never a mutable alternative such as 999.

Finally, each G4 Hunter `g4_profile_hit.injection_eligible` is derived
from its actual source Piercing packet after mitigation and must be
identical to the G4.5/G5 `actual_result.injection_eligible`. A living
target's recorded G4.4 venom result must have exactly one matching,
synchronous `accepted`, `ignored`, `prevented`, or
`not_delivered` native venom receipt with the same original exposure
key and, where present, original G4 profile hit index. A dead recipient
cannot receive postmortem venom. Ledger digest recomputation cannot
override these relationships.

The additional adversarial regressions mutate legal rechecks,
`trigger_ready_to_resolve`, Hunter/party AP budgets, Hunter
injection eligibility and venom event classification while keeping
the trial's recomputed ledger hash valid. Unmodified L2/L3 seeded
native witnesses continue to be required to pass. No new combat rules,
archetype capabilities, immunity, encounter probabilities or challenge
ratings are inferred.

## Execution and regression checks

```bash
python -m scripts.b06_g7h_mixed_encounter_certification_v0 --level 2 --seed 17
python -m scripts.b06_g7h_mixed_encounter_certification_v0 --level 3 --seed 17 --include-trials
python -m unittest discover -s tests -p test_b06_g7h_mixed_encounter_certification_v0.py -v
python -m unittest discover -s tests -v
```

The [G7-H regression tests](../../tests/test_b06_g7h_mixed_encounter_certification_v0.py)
verify all three genuine completed branches for both L2/L3, per-source
combat roles, chosen Rite/VP, authentic G1/G4/G5/G6 receipts, deterministic
native replay, tamper rejection for policies/outcomes/hashes/HP snapshots
and completed-round gating. The older G6-D default is unchanged.

**Historical Phase 3 4,096-window SHA-256 stays**
`c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`.
This candidate changes no historical evidence, source abilities or
numerical Hunter CR.

## Next acceptance gates

The next implementation should integrate **actual defensive intervention
and Priest/Scholar healing or wards into terminal-capable encounters**;
broaden legitimate P3/P4 player/GM choices and alternative frontlines;
complete legitimate non-extremal encounter continuations, recovery and
opposed departure; then independently collect representative play policies,
whole-outcome denominators and Soldier/Sentry comparison baselines.

Until those are demonstrated, the original MVP ledger remains at
**0/12 independently certified Focus combinations**, **0 complete
representative opposed party encounter packs** and Hunter **unrated**.

## G7-H source-turn MP and Hunter venom hardening (Codex P2)

The terminal audit must **not** treat a rehashed event ledger as the
authority for resource entitlements or delayed venom outcomes.

- **Turn MP:** G0 Step 4 awards each character **12 ordinary MP**
  plus any genuine active source toxin modifier, whether or not the actor
  moves. The G7-H G1 replay derives that allowance from a newly loaded
  G6-C scene, never `turn_resources.detail.mp`. Its remaining-MP
  check still independently accounts for each source-previewed Cautious
  step and `turn_end.unused_mp`. No currently accepted G7-H terminal
  reaches the first 600-second Hunter venom onset, and the fixed
  policies provide no MP-granting ability. A fabricated zero-MP idle
  turn plus matching zero `unused_mp` is rejected, even after a valid
  rehash. This source formula must be extended if future policies
  legitimately run through a toxin onset/other MP modifiers.
- **Hunter Bite G4.4:** Every nonfatal G5/G4.5 Bite resolves a single
  eligible source puncture or a non-puncture, and the original fixed
  policy supplies its *resistance d20*: natural **1** for the G6-C
  victory's Round-2 Hunter, natural **20** for G7-G defeat and
  withdrawal. Recompute the resistance total as this die **plus the
  independently loaded victim's Vitality** (authored modifier zero).
  Compare the actual `Full` (total below DC 12) or `Reduced`
  (total at least 12) result against the original G4.4 event and its
  G4.5/G5 mirrors; a rehash cannot change `Full/3` to
  `Reduced/999`.
- **Source deadlines:** For an accepted Hunter Moderate toxin,
  require exactly the native `g42_milestone_scheduled` identities,
  chronological scheduling order, original target, source, phase
  `before_recovery`, and delays: `Full` at 600/1800/7200 s
  (onset/escalation/expiry), `Reduced` at 600/3600 s
  (onset/expiry). Importantly the current G6-C authored fixtures
  begin ordinary G0 Initiative rounds **without calling the separate
  WorldClock.enter_initiative() handoff**. The native scheduling basis
  remains exploration at world second zero, so these source receipts
  carry `due_seconds` of 600/1800/7200 or 600/3600 and
  `due_round=null`—they do **not** yet use the canonical six-second
  Round-Begin surrogate. G7-H derives this mode from a newly loaded
  G6-C reference and rejects fabricated clock handoffs or advances.
  The original accepted G4.4 `marker_ids` must exactly list those
  markers. The fixed scenes end before due markers; any fabricated
  early milestone or unexpected protective Ward cannot silently
  redefine a supported trial.
- **Nonstacking:** Once an original accepted Moderate Hunter toxin is
  still active, later equal-grade puncturing Bites against that actor
  must have the native **ignored** outcome, not a new resistance
  result or an invented second timer. A non-puncturing hit cannot
  manufacture scheduled venom at all. Lethal HP damage cannot
  inject postmortem toxin.

Dedicated tampering regressions cover idle-turn MP receipt/Turn End
rewrites, coordinated G4.4/G4.5/G5 resistance-result substitutions,
missing/mis-timed source venom markers, and positive L2/L3 source
terminal runs. These checks harden the **bounded source-witness**
certificate only; no numerical Hunter CR or representative encounter
sampling is inferred.


## Codex P1 — A/B hit windows and complete Chosen Rite provenance

The source victory policy now refuses a Vanguard or Guardian *hit*
unless the paid G5 source action has its **own original G0 response
window**, keyed by `g5:melee:<action_index>` and bound to the specific
native turn, attack-sequence attestation and roll. Exactly four
contiguous events must occur after sequence attestation and before the
hit-producing roll:

1. `response_window_open`
2. `trigger_rechecked_after_interceptions` with `legal=true`
3. `trigger_rechecked_after_responses` with `legal=true`
4. `trigger_ready_to_resolve` immediately before `g5_melee_roll`

This is the **native G5 decline-all** policy: it neither claims to
resolve a reserved Interception nor accepts invented intervening
spontaneous responses. A canceled trigger, false legality recheck,
foreign/duplicated ready or borrowed action trigger cannot authorize
an unchanged G4 damage packet and G4.5 hit receipt, even after the
ledger digest has been recomputed. Hunter Bites, Bow and G1 steps
retain their separate previously implemented response-window proofs.

The actual R `cast_guided(mode="maintained", chosen=True,
recipient="archer")` calls `G3._new_effect` once on this source
scene, creating `G3-0001` in Round 1. In addition to G0's
30-AP Projected Action and 1-point `committed` VP debit, G7-H now
requires **exactly one** full establishment receipt, with no omitted
or added fields: `caster=recipient="archer"`,
`effect="G3-0001"`, `effect_kind="Guided Regeneration"`,
`committed=1`, `chosen=true`, `anchor=null`,
`parent=null`, `budget=null`, `resistance=0` and
`expiry_round=null`. Any fixed-duration expiry, fabricated effect
ID, unattested anchor, parent, budget, resistance or extra effect is
incompatible with that authorized maintained Chosen Rite.

Dedicated source-ledger tampering regressions change each A/B
hit's G0 legality rechecks and ready/origin binding, and every
individually editable Rite establishment field. Positive L2/L3,
seeds 0 and 17 remain bounded source-witness acceptance only,
not broad response selection, a full Priest spellbook or Hunter CR.

## Codex P1/P2 — Native Bow lane and G4.5 bridge snapshots

The G6-D victory's Round-2 missed Bow and Round-3 lethal Bow are
revalidated against a freshly constructed G6-C source scene. That
policy authorizes **no repositioning**. For each launch, the verifier
reconstructs the source Archer-to-Hunter **head-cell** G2 lane and
compares its actual range band, absence of cover/living screens, zero
Aim mitigation and resulting effective obstruction with the precise
`g2_bow_launched` receipt. It also binds the immediately preceding
`g2_projectile_defense_rechecked` and following
`g2_miss_faces_preallocated` and `g2_bow_shot_resolved` defenses to
the reconstructed G2 `take_hit` value. A forged range difficulty
(such as 999), coordinated defense adjustment or substituted screen
fails even if the ledger digest is recomputed.

G7-H now reconstructs **every** native `g45_attested_hit`
`target_state` **at the precise hit event**, rather than trusting
the editable G4.5 result or final-state summary. The source actor's
identity, digest, maximum resources and starting state come from a
fresh G6-C fixture; chronological source G4 damage, Step-2 recovery,
VP commitments/releases and G4 wound creation determine the complete
post-hit state including HP, Vigor, VP, Dying/dead status and the
original wound identities, trauma and progress. The verifier also
checks the original paid action, G5 sequence/defense reference and
G4.5 attacker/target source digests. Existing separate G4 packet,
wound-severity, VP and natural regeneration verifiers still validate
these inputs independently, preventing a forged earlier ledger event
from becoming its own authority.

New regression cases edit individual Bow geometry/defense receipts,
Hunter Bite and A/B G4.5 snapshot fields and bridge provenance and
recompute the original ledger hash; positive L2/L3 source traces
remain accepted. The source rules, historical census and Hunter CR
are unchanged.

## Codex P2 — Fixed G7-G Actions, Bite wound parity and signed pursuit routes

Three further tampering cases are now rejected independently of an edited
ledger SHA-256:

1. **An affordable AP debit is not an authorized policy action.** The G7-G
   defeat and withdrawal policies let the original players **hold** their
   discretionary Actions (while G1 movement and lawful border exit remain
   legitimate). The only G0 `action_committed` allowed in either policy
   is one 24-AP `physical` `sequence:B06-AT-04:0` from the Hunter in a
   given round. Each such payment must have exactly one native uncancelled
   G5 Bite hit resolution and its own valid G4/G4.5 chain. An apparently
   affordable `general`, `projection`, `full` or additional physical
   Action by any original character is not certified merely because its
   Turn-End unused AP was also rewritten.
2. **One source packet, one wound severity.** Every native Hunter Bite's
   `g45_attested_hit.detail.actual_result.wound` and its identical G5
   `damage.wound` must equal the wound severity recorded by the actual
   synchronous `g4_damage_applied.detail.wound` packet. A nonlethal
   Devastating Bite that created a Critical wound cannot instead report
   `null` on the G4.5/G5 result, even with correct HP/Vigor arithmetic.
3. **Pursuit declarations and completion receipts derive from G1.**
   At each G7-G Hunter target-selection event, independently reconstruct
   the source shortest legal Cautious route using the G7-G native planner
   on the freshly replayed source grid. Require the selection's initial
   Hunter footprint and *entire* planned route to match that source
   computation. Every actual Hunter G1 step/pivot must consume the
   declared route's next movement with its real cost. At the subsequent
   pursuit completion, compare the earlier starting footprint, ordered
   actual G1 movement indices, final footprint, source-authenticated
   remaining MP and real Hunter head contact. An incomplete prefix is
   allowed only when the next declared step truly exceeds remaining
   source MP. No forged empty movement list, arbitrary MP, substituted
   route or contradictory footprint can supply a signed pursuit.

The new negative tests target both fixed G7-G policy modes, jointly
tampered G4.5/G5 wound summaries and multiple coordinated pursuit
receipt forgeries. Legitimate L2/L3 source traces must still certify.
The exact scope remains a **bounded authored terminal matrix**;
there is no representative player/GM policy sampling or numeric CR.
