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

A mislabeled, incomplete, role-substituted, stale, unsigned or
nonterminal result fails closed.

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
