# B04/B06/B07 — Persistent Party Adventure Acceptance & Independent Certification Readiness v0

> **Execution runbook and source-linked gap register, not a completed certification.** Uses the merged L1→L3 [persistent party fixture](b04-b06-b07-integrated-milestone-persistent-party-adventure-v0.md), the [independent twelve-Focus protocol](b04-b07-independent-twelve-focus-certification-protocol-pilot-roster-v0.md), the [flexible cohort intake](b04-b07-pilot-evidence-flexibility-multi-cohort-v0.md), the [3–5-session candidate adventure](b04-b05-b06-b07-integrated-mvp-pilot-adventure-v0.md) and the [six-gate acceptance register](b04-b07-mvp-acceptance-register-refresh-v0.md). **No player, GM, reviewer, session, milestone, difficulty rating or acceptance claim is fabricated.**

**First-cohort execution handoff:** [Alpha Pilot Execution & Independent Evidence Verification v0](b04-b05-b06-b07-first-cohort-pilot-execution-evidence-v0.md) moves the Alpha planning cohort into a *blank, structured execution packet*: participant/source manifest, actual scene and GM milestone intake, 84 C1–C7 review tasks and optional local evidence-file hash comparison. Requires real players/GM/independent reviewer and actual source-legal Alpha scenes; no CI output is presented as actual play.

## Verified starting point — different evidence is not interchangeable

| Evidence | What is already source-backed | What is still missing |
|---|---|---|
| **12 Focus structures** | 12 audited Archetype×Focus source pairings, 13 structural variants and 39 structural level snapshots; source SHA-256s returned from the actual independent audit | A separately reviewed **complete** sheet/choice ledger and play legality for each pairing at L1, L2 and L3; 12/12 **full** certificates not achieved |
| **Native L1 adventure** | #196 G0/G4.2 four-character party; source ordinary diagnosis (A) and survey/records (F), 3 author-declared d20 checks and genuine elapsed world time | Source-paid real player/GM decisions for all four roles and **all 12 Focuses**; representative L1 combat, independent opponent/alternative choices, observed consequences |
| **Native L2** | G8 original Soldier opposed withdrawal; actor injuries, source Bow arrow (20→19), four physical actor sources | Player-chosen opposing policies; Full Low Priest A/B magical choices (G0 A/B here are **physical proxies**); Focus-specific alternatives; Hunter corridor and actual shrine GM progress |
| **Native L3** | G8 cold Sentry victory from the **same** continued original party; HP/Vigor/VP, ammunition, prior clock phases and level candidate record retained | Varied Sentry/Hunter/Soldier outcomes, negative counterplay, real GM rulings, independent Focus-specific reviews |
| **Two author-fixture milestones** | Distinct source-checked gate L1→L2 and shrine L2→L3 records; level sheet profiles and no-fabricated-refill continuity | **Actual** GM story achievement and declaration, exact scene/time, separate L2/L3 reviewed sheets and participant attribution. A Soldier withdrawal alone **does not establish** the shrine milestone |
| **Persistent G4.2/G4.3/G4.4** | Original same-level G8 handoffs can carry source-authenticated toxins, Endurance, Stone Skin/Guided, recovery and provenance (#194–195) | Cross-level **active** poison/maintained spell translation is deliberately unsupported by #196 and must be avoided during the level-up window or separately authored and tested |
| **Human certification** | Blank candidate/participant packet schemas and a structural preflight only | Verified 3–5-session human play, independent reviewer decisions, actual challenge/denominator calibration and explicitly authorized gate sign-off |

**Current immutable baseline for readiness:** **12/12 structural**, **0/12 independently full-Focus certified**, **0/6 MVP exit gates**, **0 verified human pilot sessions**, **0 externally verified GM milestone awards**; B01–B03 of seven original blockers closed (**3/7**). Automated checks may validate references and source invariants, but cannot award external-play credit.

## Machine-readable C1–C7 matrix

The new `scripts/b04_b06_b07_persistent_adventure_acceptance_readiness_v0.py` derives the **current actual source digests** and Focus-defined positive/negative identity prompts from the existing audited roster and `FOCUS_TASKS`. It runs the **merged native #196** source chain to ensure the source witness still passes, then produces 36 Focus×level records; each has seven explicitly unmet independent checks (**252 outstanding C1–C7 review tasks**, *not* 252 distinct new mechanics). A bounded scripted scene is tagged as **machine-only** and remains incomplete for **every** human C3/C4/C6/C7 criterion. There is no implemented function that flips a criterion, Focus or MVP gate to accepted.

```bash
# Rerun native chain and emit all 12 pairings x 3 levels x C1-C7 gaps.
python -m scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 > build/persistent-adventure-readiness.json

# Generate source-linked blank, still-UNOBSERVED cohort forms for three tables.
python -m scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 --cohort-templates > build/blank-pilot-cohorts.json

# One full-fidelity existing certification-intake blank plus Focus-specific task cards.
python -m scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 --field-sheet 'Gifted/High' > build/gifted-high-fieldwork.json

# Validate ONE edited cohort with the pre-existing flexible intake; this checks
# reference shape and scene/milestone order ONLY, not actual authenticity.
python -m scripts.b04_b07_pilot_evidence_cohorts_v0 --check actual-cohort.json
```

**Keep all person-identifying information and confidential GM observations in controlled private pilot records.** Repository fixtures and blank packets must not be populated with invented referee names or personal data. If packets reference private records, preserve source/event hashes and authorized access so a separate reviewer can retrieve the raw evidence.

## Practical 3–5-session GM/player procedure

The existing **four-session schedule** is a concrete candidate, not a requirement that actual awards happen at the named beats. The flexible multi-cohort intake is authoritative for recorded real events; its level chronology is based on **actual scene-linked GM declarations**, not fixed session-number triggers.

| Session/target level | GM preparation and real choice | Required raw evidence and stop/go |
|---|---|---|
| **1: L1 — Supply and Gate** | Give players source-legal competing approach/diagnosis/record routes; require an actual risk, alternative and outcome. At most use the standalone verified L1 combat scope of #191, not a down-leveled G8 Soldier/Sentry. GM may decide significant group-story Milestone 1 **only after an observed achievement**. | Source-signed selected sheets (C1); individual AP/VP/time/roll and real GM adjudications (C4); other considered route; scene start/end resources, wounds and clocks. If no genuine event, **do not advance to L2**. |
| **2: L2 — Hunter Forest** | Give warned escape, cautious movement, avoidance and genuine Hunter opposition choices. Select native G7F/G7H or a separately validated source/legal encounter for that Focus/cohort; do not assume Hunter CR. Include toxin onset, pressure, protection, pursuit and possible failure-forward. | Player-selected combat option + alternative and countercase (C3/C5); a true exposure/venom/recovery trace; GM records whether safety/rest is actually available. Denied, fled, or unresolved outcomes are acceptable data. |
| **3: L2 — Shrine/Sentry** | Offer observation/parley/alternate access and cold vs prepared Sentry only when source/fiction authorizes that initial state. Distinguish withdrawal from victory. Milestone 2 only when an actual later **group-story** event merits L3. | Source legal G8 L2 or separately validated scene, genuine VP/response/wounds and event hashes; reviewed before/after sheets (C2/C7). A GM may defer second award; do not silently turn a win into a level. |
| **4: L3 — Village/aftermath** | Test L3 defining Focus identity through both hostile and field/support decisions. Follow the real recovery/six-hour clock, actual rest safety, toxins, old wounds, limited VP and depleted ammunition; do not grant automatic cure. | End-to-end source continuity and milestone identities, GM consequence/alternative/countercase, actual late-Level-3 combat/noncombat behavior, reviewer notes and all observed balance denominators. |

For **three sessions**, combine supply+gate and forest+shrine; for **five**, split supply and gate. Do not claim a session level until the actual declaration makes it legal; the cohort intake permits multiple levels in one session only after a valid in-session milestone. All five adventure beats **supply → gate → forest → shrine → village** retain their authored order even when players choose partial success, bypass or retreat.

### Suggested staffing and 12-Focus coverage

The machine generator emits **three suggested four-player cohorts**, not 12 simultaneous PCs, with separate, real source-selected characters, GM decisions and independent reviewers:

| Cohort | Four independently tracked Focuses | Native availability caution |
|---|---|---|
| **Alpha** | Priest/Low; Scholar/High; Gifted/High; Anointed/Medium | #196 supports bounded A/B physical Low Priest and High Scholar Fire fixtures only; Gifted/Anointed require separate native or externally verified source-legal adjudication; a full Priest/Low is **not** its physical A/B proxy |
| **Beta** | Priest/High; Scholar/Medium; Gifted/Low; Anointed/High | Requires source-authenticated combat, utility and resource choices for each Focus and source-balanced opponents |
| **Gamma** | Priest/Medium; Scholar/Low; Gifted/Medium; Anointed/Low | Requires source-authenticated shared protection, Embodiment/ward and true Step/Consent opportunities |

In **every** cohort at **each** of L1, L2, L3, collect C1–C6 per pairing plus the two distinct group-story GM awards (C7) for its individual players. One cohort can legitimately fail or delay its milestone: record it and either arrange another qualifying session inside the pilot scope or flag incomplete coverage. Multiple cohorts may repeat a pairing, but do not count duplicate participants as additional certificates.

### Required on-table capture and independent review

For every played scene, obtain the **actual player's declaration**, at least one material alternative considered, the exact starting state (HP/Vigor/VP Available/Committed/Spent, wounds, ammo, maintained effects, toxin clock), the source action/legal prerequisites, any relevant target geometry and roll, the GM's contested or consenting ruling, the final native event and world-clock state, and the consequence for the next session. A native negative test may support C5 but **cannot substitute for** the observed C3/C4 choice.

At each actual milestone, record **unique event ID, GM declaration, the completed group-story achievement, after-scene anchor, affected characters, before/after sheet hashes, and earned/selected/saved Talent/Training and resource deltas**. For L2 and L3, check both increase eligibility and the source's affordability. #196's **new VP capacity begins Spent** is a conservative *fixture policy*, not a universal rule silently imposed on human tables; if the live GM chooses a different interpretation, record a rules decision/dependency and test that separately.

The independent reviewer must inspect accessible original primary records separately from their author/implementer, compare source digests, verify player/GM choice and legal mechanics, and distinguish **verified human observation** from replay-only test artifacts. Avoid publishing personal identities, GM confidential notes or private links in the repository. Follow the existing [C1–C7 source protocol](b04-b07-independent-twelve-focus-certification-protocol-pilot-roster-v0.md) and [multi-cohort exact schema](b04-b07-pilot-evidence-flexibility-multi-cohort-v0.md). Completed syntactic packets are **still candidate/unverified** until independently reviewed outside the CLI.

## Blocker triage — decision vs implementation vs evidence

| Priority | Concrete gap | Primary owner | Next action / validation | Type |
|---|---|---|---|---|
| **P0** | No verifiable player, independent GM or independent reviewer assignments; 0 external play | B04/B07 | Recruit/co-ordinate three real 3–5-session tables or equivalent lawful rotating cohorts; record roles and secure raw evidence access | **External execution arrangement**, not missing game rule |
| **P0** | 36 Focus-level C1–C7 cells have no independent acceptance | B04/B05/B07 | Independently compare 12 full selected character lines and legal alternatives; use generated individual Focus field sheets | **External review/evidence** |
| **P0** | Two milestones are author-fixture only | B07 | GM adjudicates two distinct genuine group-story moments; verify both against actual scenes and sheet transitions | **External play and review** |
| **P0** | Mixed native L1 encounter and Focus-specific L1 decisions are not generally supported by #196 G8 | B04/B05/B06 | Choose a separately sourced legal L1 combat policy for each cohort; don't transplant L2 G8 or treat #191 as all 12 playable Focuses | **Conditional scene implementation** |
| **P1** | Full Priest/Low Rite/Exaltation not established by A/B proxy chain; other Focuses absent from #196 | B04/B05/B06 | Execute and test defining combat and field expressions for the *actual chosen* line at each level; create only missing bound adapters identified by concrete pilot actions | **Implementation when selected scenes require it** |
| **P1** | Advancement with live poison/maintained hosts is deliberately fail-closed | B04/B06/B07 | Plan an actual legal clean milestone boundary or implement and test source-authorized cross-level effect/recovery rebind; never erase effects | **Conditional implementation** |
| **P1** | Representative Soldier/Sentry/Hunter opposition, retreat, aftermath and damage coverage still incomplete | B06 | Run authentic real GM variants and compare opposed outcomes; record wounds/dying/attrition, time, pursuit and choice of prepared Sentry | **GM scene implementation and evidence** |
| **P1** | Balance watches (Gifted, Rooted Guard, Unbound Step, Anointed, critical/wounds), representative CR not determined | B04–B07 | Collect player role effectiveness and encounter completion/failure denominators, then separately decide adjustments | **Evidence then possible rules decision** |
| **P2** | Advanced optional Intrusion, unrepresented Aspects or Tier-2/3 miracles | B05 | Only implement if an actual selected Focus identity/scene is blocked and the canonical source permits the effect | **Conditional, not blanket MVP blocker** |

The legacy B06 G0–G8 stages are **not** reopened or expanded. P0/P1 mean collection or a narrowly identified missing scene/adapter, not automatic authority to alter the rules.

## Exit checklist and responsibility

**GM:** complete 3–5 sessions for the tracked cohort with actual meaningful alternative outcomes, adjudicate separate group-story milestone events without automatic levels, track resources and clocks through each transition, record opponent policies and real denominators.

**Players:** verify selected source sheet and starter choices, declare actual actions and alternatives in combat/noncombat, report where a Focus cannot meaningfully function, keep the observed negative options distinct from forced scripted outcomes.

**Independent reviewer:** examine raw logs, not just completed form strings; attest C1–C7 at each level, report concrete missing legality or source gaps back to B04/B05/B06/B07, and separately judge representativeness and balance. Do not double count Low Priest A/B or repeated cohort coverage.

**Acceptance owner:** consider the **six unchanged Create/Act/Resolve/Advance/Challenge/Observe gates separately** only after independently verified full Focus evidence and representative actual play. This artifact's machine output keeps **all six OPEN**, **0/12 independently certified**, and **0/6 accepted** regardless of whether the author-fixture chain and all regressions pass.

## Regression and evidence commands

```bash
python -m unittest discover -s tests -p 'test_b04_b06_b07_persistent_adventure_acceptance_readiness_v0.py' -v
python -m scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 > build/persistent-adventure-readiness.json
python -m scripts.b04_b06_b07_persistent_adventure_acceptance_readiness_v0 --cohort-templates > build/blank-pilot-cohorts.json
python -m json.tool build/persistent-adventure-readiness.json > /dev/null
python -m json.tool build/blank-pilot-cohorts.json > /dev/null
```

These are **planning/evidence** artifacts. Completed automated tests alone must **not** mutate the acceptance register's actual gate status.
