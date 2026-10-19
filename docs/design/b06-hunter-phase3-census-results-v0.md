# B06 — Hunter Phase 3 Verified One-Round Census v0

> **VERIFIED SCRIPT EXECUTION, NOT COMPLETED ENCOUNTER CERTIFICATION.** This is a snapshot of the [Phase 3 tactical and party-diversity runner](../../scripts/b06_hunter_tactical_diversity_v0.py), not a full playtest, party win probability or numerical CR. **32 source-conditioned cells × 128 SHA-256-keyed seeds = 4,096 one-round windows**; party candidates R/F are **not** independently certified L1–3 character builds. The result is produced by the [report generator](../../scripts/b06_hunter_phase3_report_v0.py) and guarded by 24 report-focused regression tests, including exact per-seed replay of every published aggregate.

## Exact execution evidence

- **PR-head-source attestation** is verified by [workflow run 39178749564](https://github.com/BetrayedByEthanol/Veilbound/actions/runs/39178749564), which explicitly checked out and matched **PR head `b607f2925258e9769f3a4ffa6fa9883b1d015553`** before executing the simulator. Earlier runs used GitHub's default synthetic merge checkout; their matching numeric results are supplementary rather than the authoritative head-attestation evidence. The Phase 3 gameplay runner remains unchanged from merged PR #94.
- **Focused tactical tests:** **14/14 passed**; **new report tests:** **24/24 passed** (including exact exposed-front VP reconciliation, Pounce/Balance terminal accounting, path/toxin exclusivity, impossible sub-three Fire Vigor burn, finite/physical mean HP, per-seed source replay, earlier source-attribution guards, and variable-seed reports); **full repository unittest discovery: 237/237 passed, zero skipped** using optional Draft 2020-12 `jsonschema`. **B06 footprint semantic validator:** all five creature fixture/index documents passed. Python 3.12 CI environment. The pinned-head run reproduced the earlier **identical terminal counts and canonical JSON SHA-256**.
- CI [`b06-phase3-census` artifact](https://github.com/BetrayedByEthanol/Veilbound/actions/runs/39178749564/artifacts/12155042424) from the PR-head-pinned execution contains the full machine-readable 32-cell JSON and generated Markdown. Canonical JSON SHA-256 (excluding its `audit_sha256` field) was independently recomputed from the prior artifact and confirmed unchanged:
  `c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`.
- No extrapolation to playtest balance, a generic Hunter rating or an actual party wipe is authorized. **Hunter remains `unrated`; B06 remains blocking; 0 certified complete B06 encounter packs; 0/12 full Focus certificates.**

## Full 4,096-window first-stop census

| First stopping event | Windows | Share |
|---|---:|---:|
| Hunter first reaches 0 HP (`hunter_first_zero`) | **2,673** | **65.3%** |
| Frontline target first reaches 0 HP (`frontline_first_zero`) | 0 | 0.0% |
| Above-zero Devastating wound unresolved (`wound_unresolved`) | 22 | 0.5% |
| Unresolved contact geometry/Opportunity (`contact_path_unresolved`) | **770** | **18.8%** |
| Completed one round, no earlier terminal (`round_one_complete`) | 631 | 15.4% |
| **Total** | **4,096** | **100%** |

Each column counts the **first stop in one specific scripted window**; categories are mutually exclusive. A Hunter at 0 HP is **Dying, not dead**. A frontline 0 does not imply party defeat. A wound boundary stops before unresolved continuation. An unresolved path means **the movement/Opportunity branch cannot be resolved from the model**, and is neither a win nor a loss. Percentages are descriptive fractions of artificial model trials, **not** estimated real-game probabilities.

## Role and action accounting

| Event | Recorded count |
|---|---:|
| Pounce declared | 714 |
| Pounce Balance resolved | 708 |
| Full / Reduced toxin applications | 443 / 584 |
| Spent VP | 2,538 |
| Arrows fired | 2,023 |
| Fire-caused direct Vigor burn | 3,283 |
| Front caster paid precontact spell launches | 229 |
| Front caster approach MP paid | 308 |
| Trials with a disrupted approach lane | 1,321 |
| Contact path unresolved stops | 770 |

**Pounce declared ≠ Balance resolved:** six one-round traces stop after an eligible Bite's terminal effect rather than resolving the post-Bite Balance. Delayed toxin stages are not advanced to T+10/30/60/120 minutes.

### Original and mixed roster totals (2,048 windows each)

| Count | Original Low Life proxy party | Mixed guardian/archer/Fire witness |
|---|---:|---:|
| Hunter first reaches 0 HP | 1,363 | 1,310 |
| Frontline reaches 0 HP first | 0 | 0 |
| Wound unresolved | 8 | 14 |
| Contact path unresolved | **531** | **239** |
| One round completes | 146 | 485 |
| Pounce declared | 312 | 402 |
| Full / Reduced toxin | 151 / 250 | 292 / 334 |
| Spent VP | 0 | 2,538 |
| Arrows fired | 0 | 2,023 |
| Direct Vigor burn | 0 | 3,283 |

These groups differ in physical/ranged/Fire damage composition, threatened-caster restrictions, initial frontal-target options and legal movement; they are **not interchangeable or causally matched win/loss experiments**. In particular, the greater number of unresolved paths for original parties is due to this runner's single staged pre-Hunter melee entry square, not evidence that a real melee party physically cannot attack.

For an additional context split, **warned** initial positions account for 0 unresolved contact paths and 1,624 Hunter-first-zero stops in 2,048 windows; **ambush** configurations account for all 770 unresolved paths and 1,049 Hunter-first-zero stops in 2,048 windows. Comparing their raw ratios as encounter difficulty would discard unresolved routes and the drastically different initial geometry.

## All 32 scenario cells — verified counts

**Every row has 128 keyed trials.** Negative mean Hunter HP represents first-hit **overkill at the stopping event**, not continued attacks below 0.

| Scenario | Hunter 0 first | Front 0 first | Wound stop | Path unresolved | Round complete | Pounce | VP | Arrows | Vigor burn | Mean Hunter HP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| L2-P3-original-warned-armored | 82 | 0 | 1 | 0 | 45 | 0 | 0 | 0 | 0 | 0.023 |
| L2-P3-original-warned-exposed | 83 | 0 | 0 | 0 | 45 | 0 | 0 | 0 | 0 | -0.109 |
| L2-P3-original-ambush-armored | 36 | 0 | 1 | 74 | 17 | 42 | 0 | 0 | 0 | 5.164 |
| L2-P3-original-ambush-exposed | 40 | 0 | 0 | 74 | 14 | 42 | 0 | 0 | 0 | 4.742 |
| L2-P3-mixed-warned-armored | 46 | 0 | 1 | 0 | 81 | 0 | 242 | 121 | 290 | 4.211 |
| L2-P3-mixed-warned-exposed | 29 | 0 | 1 | 0 | 98 | 0 | 0 | 127 | 0 | 5.703 |
| L2-P3-mixed-ambush-armored | 46 | 0 | 1 | 0 | 81 | 72 | 242 | 121 | 290 | 4.211 |
| L2-P3-mixed-ambush-exposed | 32 | 0 | 1 | 46 | 49 | 48 | 92 | 104 | 98 | 5.594 |
| L2-P4-original-warned-armored | 117 | 0 | 1 | 0 | 10 | 0 | 0 | 0 | 0 | -3.383 |
| L2-P4-original-warned-exposed | 118 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | -3.516 |
| L2-P4-original-ambush-armored | 41 | 0 | 1 | 83 | 3 | 36 | 0 | 0 | 0 | 4.734 |
| L2-P4-original-ambush-exposed | 41 | 0 | 0 | 85 | 2 | 36 | 0 | 0 | 0 | 4.594 |
| L2-P4-mixed-warned-armored | 86 | 0 | 1 | 0 | 41 | 0 | 212 | 104 | 265 | -0.047 |
| L2-P4-mixed-warned-exposed | 73 | 0 | 0 | 0 | 55 | 0 | 0 | 111 | 0 | 1.281 |
| L2-P4-mixed-ambush-armored | 52 | 0 | 1 | 54 | 21 | 47 | 186 | 91 | 235 | 3.531 |
| L2-P4-mixed-ambush-exposed | 38 | 0 | 0 | 74 | 16 | 38 | 62 | 80 | 68 | 5.117 |
| L3-P3-original-warned-armored | 127 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | -3.875 |
| L3-P3-original-warned-exposed | 128 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -4.008 |
| L3-P3-original-ambush-armored | 75 | 0 | 1 | 52 | 0 | 42 | 0 | 0 | 0 | 0.656 |
| L3-P3-original-ambush-exposed | 77 | 0 | 0 | 51 | 0 | 42 | 0 | 0 | 0 | 0.445 |
| L3-P3-mixed-warned-armored | 119 | 0 | 1 | 0 | 8 | 0 | 354 | 165 | 480 | -3.188 |
| L3-P3-mixed-warned-exposed | 108 | 0 | 1 | 0 | 19 | 0 | 0 | 180 | 0 | -2.828 |
| L3-P3-mixed-ambush-armored | 119 | 0 | 1 | 0 | 8 | 68 | 354 | 165 | 480 | -3.188 |
| L3-P3-mixed-ambush-exposed | 108 | 0 | 2 | 12 | 6 | 47 | 182 | 154 | 222 | -2.266 |
| L3-P4-original-warned-armored | 127 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | -4.102 |
| L3-P4-original-warned-exposed | 128 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -4.234 |
| L3-P4-original-ambush-armored | 70 | 0 | 1 | 57 | 0 | 36 | 0 | 0 | 0 | 1.117 |
| L3-P4-original-ambush-exposed | 73 | 0 | 0 | 55 | 0 | 36 | 0 | 0 | 0 | 0.656 |
| L3-P4-mixed-warned-armored | 126 | 0 | 1 | 0 | 1 | 0 | 254 | 128 | 364 | -3.266 |
| L3-P4-mixed-warned-exposed | 127 | 0 | 0 | 0 | 1 | 0 | 0 | 139 | 0 | -4.055 |
| L3-P4-mixed-ambush-armored | 107 | 0 | 1 | 20 | 0 | 45 | 236 | 118 | 340 | -1.711 |
| L3-P4-mixed-ambush-exposed | 94 | 0 | 1 | 33 | 0 | 37 | 122 | 115 | 151 | -0.953 |

## Scope discipline and next gates

- The generator replays each keyed source trial independently of the aggregated `census()` output and requires an exact match of every recorded count, terminal category and three-decimal mean HP before signing; JSON serializes with `allow_nan=False`, and the mean must be finite and within the runner's physical first-stop HP bounds.
- Verify the exact artifact/run provenance on future changes: **numbers correspond to the PR-head-attested execution stated above**, not an automatically refreshed dataset. The CI checkout asserts source HEAD equals the event PR-head SHA (or the dispatched ref SHA), while the report's seed-range provenance is generated from the requested seed count.
- Resolve obstructed `contact_path_unresolved` cases with actual 1×2 occupancy, legal Cautious/Normal paths, Movement Opportunities and correct defensive responses; do not redistribute these 770 stops between player/Hunter outcomes.
- Finish independent L1→3 Bow and High Scholar sheets; authorize the real full technique sets before claiming valid mixed-Focus playtesting.
- Continue into **multi-round** Soldier/Sentry/Hunter encounters with authentic Rites/Exaltations, wound repair, Dying, delayed toxin, retreat and GM decision-making.
- Only after full representative comparisons should party survival or creature CR become a calibration candidate.
