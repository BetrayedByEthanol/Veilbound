# B06 G7-F — Representative Encounter Calibration v0 (source-native pilot)

> **A reproducible *candidate* calibration dataset, not representative
> human/GM play and not a numerical Hunter challenge rating.** The name
> describes the target acceptance gate, not a certification already earned.
> This PR adds genuinely executed, explicitly sampled source-native policy
> observations. No new surprise bonus, Hunter retreat, player Rite,
> post-fight safety or fabricated whole-party defeat is authorized.

## What is executable

`python -m scripts.b06_g7f_representative_calibration_v0 --seeds 4`

The G7-F runner executes **31 separately identified policy cohorts**, with
**1–128 independent, SHA256-keyed seeds per cohort**. The same seed is
precommitted across eligible related policies; no stream-dependent rerolls
or reassignment of policies after observing their outcomes. Every case uses
existing G0–G7-E native scene executors, returns its complete original G0
ledger to G7-F for independent verification, and is assigned **one
non-overlapping source-policy-seed identity**.

For each L2/L3 × three-/four-PC A/B/R[/F] party:

| Policy | Existing native authority | Limits |
|---|---|---|
| `warned_control` | G7-A source-paid A/B melee, R Bow, optional F Flame and Hunter Bite | Three-round ceiling; G7-A unresolved Flame critical remains unresolved |
| `warned_flame` | G7-B confirmed direct Thrown Flame critical | Three-round ceiling, no generalized projectile policy |
| `warned_archer_exit` | G7-B individually attested R exit | One member's exit is never a party escape |
| `warned_party_exit` | G7-C separately authored A/B/R[/F] Cautious routes + terminal gate | One-round fixed start; positive whole-party withdrawal where earned |
| `b_front` | G7-D actual B head-forward/Hunter targeting, A at side | Two-round ceiling; no reversed A-protects-B magic |
| `forest_ordinary` | G7-E genuine three-step Hunter approach and paid normal Bite | Two-round ceiling, forest geometry **without** surprise bonus |
| `forest_pounce` | G7-E rigid 1×2 three-step 24 AP Pounce, real Bite, independent Balance | Two-round ceiling; no invented Grab or free Stand |

**L3/four-PC only:** `protected_control`, `reactive_shield` and
`prepared_body` invoke G7-D's original A-front integration, with genuine
Reaction/Guard vs previously committed MP movement. These add **three
cohorts**, for **31 total** (4 × 7 + 3).

## Strong provenance and terminal criteria

The adapter refuses result mutation or inflation: exact source A/B/R/F and
Hunter identities and stable fingerprints; native G0 index, chronological
turn order and real Round End; rehashed original G0 ledger; originating
policy, seed, native outcome and resource snapshots; no invented
`complete_party_pack_certified` or numeric CR. Its separate, compact trial
row records authentic Hunter/party HP change, Pounce, protected Bite,
party-exit events, completed turns/rounds, event hash and unresolved reason.
A terminal may be counted as **native certified** only when the source
G6-D Hunter-death, G7-C whole-party exit, or G7-C full-party defeat event
exists once with an original native terminal receipt at a completed Round
End. `party_defeat_observed` is **not** certified full-party defeat;
Dying/0 HP is **not** death. Native Cautious withdrawal is distinct from
G7-E's **zero-second** exploration-clock handoff; forest observation
ending with a live Hunter cannot be turned into a safe rest or escape.

Every seed remains in one of the seven explicit outcome bins, including
`legal_window_cutoff`, `unresolved_mechanical_branch`, and single-actor
exit. An unresolved branch records its native reason. The source-policy
paired observation cannot silently drop failed, censored or incomplete
seed results. No post-selection denominator or "only resolved games"
percentage is permitted.

## Paired, but noncausal tactical comparisons

There are **10** predeclared comparisons (4 forest approach-vs-Pounce,
4 warned control-vs-archer-exit, and 2 L3/P4 protection contrasts). The
report keeps both original ledger digests, separate full outcome labels,
paired source seed, and **descriptive** Hunter/party HP-change deltas.
It distinguishes both-sides-terminal from censored pairs, rather than
pretending that a finite two-/three-round HP difference is encounter
success, confidence interval, survival probability or a causal effect.

**Important comparability limit:** Pairing source seeds does not imply
identical random faces for actions with different source keys, or
identical choices after their trajectories diverge. G7-E's own paired
`opening_bite` control is the directly shared source-face comparison;
other pairings are policy-declared observational contrasts only.

The pilot can execute **31 × 128 = 3,968 native observations** and
**10 × 128 = 1,280 paired observations** with full denominators, but
these numbers are *simulation repetitions under hardcoded policy
families*, **not independent representative human encounters**.
The older signed Phase 3 **4,096 first-stop windows** remain separate,
unchanged, SHA256:
`c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`.

## Acceptance boundary and next concrete gates

**G7-F establishes repeatable native observation and comparative sampling
infrastructure; representative encounter calibration is *not yet
accepted*.** Reports therefore retain `sampled_win_rate=null`,
`confidence_interval=null`, `creature_challenge_rating=null`,
`complete_party_packs_certified=0` and
`representative_encounter_calibration_accepted=false`.

Required before issuing a representative success probability or Hunter
rating: (1) positive multi-target source-backed Hunter party wipe, (2)
a fictionally lawful disengagement when Hunter survives before long
exploration, (3) representative separately observed player and GM
policies with independent sampling/weights, (4) broader legitimate
Cover, reactive defense, Priest Rite, heal/ward and ranged choices,
(5) completed outcomes rather than fixed-round censoring and (6)
comparative baselines against other enemy difficulty. The next
implementation should target **native Hunter pursuit/retarget into an
actual full-party adverse terminal and legal opposed withdrawal**, not
another standalone audit.

## Verification

```sh
python -m unittest discover -s tests -p 'test_b06_g7f_representative_calibration_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.b06_g7f_representative_calibration_v0 --seeds 4
python -m scripts.b06_g7f_representative_calibration_v0 --seeds 128
```

The 24 dedicated tests cover all 31 native policy cells, paired
histories, sample accounting, CLI/hash reproducibility, and fail-closed
source, ledger, turn, terminal, time-handoff and CR invariants. Full
repository CI must verify the unchanged Phase 3 signature, Bow and
Scholar regression suites on the exact PR head before merge.
