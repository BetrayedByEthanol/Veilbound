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

### Codex P2 corrections — policy binding and snapshot provenance

G7-F now matches the executor's exact **scenario ID, policy ID,
opening and frontline** against the requested calibration policy before
counting a trial. It independently checks the G0-created scene and
seed, the forest Pounce receipt (including the distinction from an
ordinary Bite), the protection method/receipt count, and the
authoritative single-actor/whole-party exit policy. A source-valid
`warned_control` trial can no longer be mislabeled as
`warned_flame`, nor a forest ordinary Bite as a Pounce.

### Codex P2 follow-up — native policy selection in the ledger

The earlier check compared the requested cohort to mutable `scenario_id`,
`policy_id`, `opening`, `frontline` and protection summaries, none of
which were covered by `ledger_sha256`. In particular a `warned_control`
observation could be relabeled `warned_flame` without changing a single
source event, and a `protected_control` observation could be relabeled
`reactive_shield` by forging its report metadata.

**Corrected contract:** G7-F requests an explicit `calibration_policy`
from the source-native G7-A/C/D/E runner. Before any own-turn resource
allocation or attack, the runner checks that this cohort agrees with its
actual execution mode and writes exactly one `g7f_policy_selected`
native event directly into the G0 ledger, **after source G1/G2/G3/G4 setup
but before the first actor turn, paid action or tactical die roll**. The
native scene factory may already have begun Round 1 to refresh capacities
and map world-clock deadlines. Setup events therefore already occupy
ledger indices after `encounter_created`; the policy marker must occur
before first turn allocation, not at a guessed fixed index or necessarily
before Round Begin. It binds the cohort, runner, mode,
source scenario, level, party size and seed. It is included in the
existing `ledger_sha256` alongside all later source rolls, actions
and outcomes; G7-F must verify the exact event fields, timing, unique
occurrence and hash **before** admitting a report to a cohort.

The runner-specific mapping keeps these policies distinct even when
the same early-round source events happen to occur:
`warned_control` / `warned_flame` / `warned_archer_exit`,
`protected_control` / `reactive_shield` / `prepared_body`,
and `forest_ordinary` / `forest_pounce`.
Native protection receipts, when earned, additionally require the
matching method, reactive/prepared activation, source Hunter attacker,
A ward and B guardian; earlier G7-D source checks retain the paid
G0 Reaction/MP and original G5 action linkage.

Legacy direct G7-A/C/D/E calls without the optional G7-F instrument
are unchanged; the original Phase 3 audit remains frozen. The policy
ledger receipt proves **consistent native source execution relative to
the original ledger and SHA**, not an external cryptographic signature
or independent sampling of human strategy.

New regressions reject both exact Codex relabel attacks while retaining
their unchanged original hashes, as well as missing/late/duplicate
policy markers and changes to marker content or native mode even if
the caller recomputes a new hash. A native acceptance test independently
exercises policy binding across all four runner families.

The source ledger's `encounter_created.source_ids` contains exact
initial HP, role identities and source digests. G7-F now reconstructs
HP and death states using every native `g4_damage_applied`,
`regeneration_step`, and `g4_basic_heal_applied` event in order,
verifying each before/after chain and comparing the result against
the initial and final report snapshots. The descriptive HP deltas
and Hunter-dead flag come only from that reconstructed event history,
not unauthenticated mutable snapshot fields. An intact ledger hash
does **not** authorize changed HP or death snapshots.

This is source-ledger reconciliation, not a claim that a caller-
manufactured ledger hash is a cryptographic signature or that the
bounded native G0–G7 adapters are an exhaustive game engine.

Every seed remains in one of the seven explicit outcome bins, including
`legal_window_cutoff`, `unresolved_mechanical_branch`, and single-actor
exit. Its unresolved reason is now *derived from the hashed source ledger*,
not trusted from mutable exception text. The source-policy
paired observation cannot silently drop failed, censored or incomplete
seed results. No post-selection denominator or "only resolved games"
percentage is permitted.


### Codex P2 follow-up — ledger-derived censored classifications

The G7-F verifier reconstructs every non-certified outcome from the
original source ledger and G4-reconciled death state. A genuine completed
G0 Round End is required for `legal_window_cutoff`; an unmatched native
Round Begin / turn-start or live unresolved decision produces a distinct
unresolved classification. A real G5/G4.5 Archer exit cannot be demoted
to a cutoff, and `party_defeat_observed` requires the deaths of every
original PC, reconstructed from each genuine G4 transition.

A real Hunter death without a corresponding terminal remains unresolved.
Whole-party exit receipts without G7-C's unique party certificate are
also unresolved rather than treated as safe departures. When the ledger
demonstrates an incomplete turn, G7-F emits an auditable canonical reason
(e.g. `native_turn_or_round_incomplete`) instead of allowing editable
`unresolved.reason` to bias aggregated counts. Native reports that
disagree with these ledger-derived outcomes fail closed, without rewriting
the signed Phase 3 census or assigning a Hunter CR.

Five additional regressions cover silent unresolved-to-cutoff,
tampered unresolved reason, Archer-exit demotion, false whole-party death,
and a positive reconstructed observed-party-death control.

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

The 41 dedicated tests cover all 31 native policy cells, paired
histories, sample accounting, CLI/hash reproducibility, and fail-closed
source, ledger, turn, terminal, time-handoff and CR invariants. Full
repository CI must verify the unchanged Phase 3 signature, Bow and
Scholar regression suites on the exact PR head before merge.
