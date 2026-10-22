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
   Bite for victory; genuine unique G4 fatal Hunter Bite receipts for
   every player in defeat; and four distinct source exits plus actual
   Hunter pursued G1 steps for withdrawal.

A mislabeled, incomplete, role-substituted, stale, unsigned or
nonterminal result fails closed. Ordinary nonterminal scenes must retain
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
