# B04/B05/B06/B07 — First Cohort Pilot Execution & Independent Evidence Verification v0

> **Execution kit only, not a record of real human play.** Based on the merged [acceptance readiness](b04-b06-b07-persistent-adventure-acceptance-certification-readiness-v0.md), [persistent L1–3 party](b04-b06-b07-integrated-milestone-persistent-party-adventure-v0.md), [C1–C7 certification protocol](b04-b07-independent-twelve-focus-certification-protocol-pilot-roster-v0.md), and [multi-cohort evidence protocol](b04-b07-pilot-evidence-flexibility-multi-cohort-v0.md). It supplies evidence preparation and offline checking; it cannot execute human sessions or authenticate GM/reviewer identities.

## Alpha — first four-character cohort

This is the existing **COHORT-ALPHA** allocation from readiness #197, not the historical A/B/R/F source-script party #196.

| Participant | Selected Focus | Original source / bounded native adapter | First real player decision |
|---|---|---|---|
| PC-1 | Priest/Low | Complete L1–3 Life A/B sheets in scripts/b05_low_priest_life_l1_l3_v0.py; source noncombat scripts/b04_b05_low_priest_complete_noncombat_v0.py | Choose **A or B**, then a full legal Rite/Exaltation/weapon path. G8 physical A/B proxies alone cannot certify the full Priest. |
| PC-2 | Scholar/High | scripts/b05_high_scholar_fire_l1_l3_v0.py and bounded G8 Flame/composite fixtures | Actual known/prepared formula and utility decisions, AP/VP affordability and combat alternatives |
| PC-3 | Gifted/High | scripts/b05_high_gifted_l1_l3_v0.py and scripts/b05_high_gifted_native_encounter_v0.py | Chosen Emotion/Aspect, safe vs risky Amplification, real Instability, range and outcome |
| PC-4 | Anointed/Medium | scripts/b05_medium_anointed_restoration_l1_l3_v0.py and scripts/b05_medium_anointed_native_returning_step_v0.py | One consenting Vessel, paid 24-AP Investment, true recipient G4 Step and GM Mission story alternatives |

**Go/no-go:** There is no established single source-native mixed-Alpha four-PC G8 L1 combat engine. A specialized standalone adapter is not blanket permission to resolve every mixed party action. The GM and independent referee must select and test source-legal scene compositions first, or mark the chosen combat BLOCKED. Do not downlevel a G8 enemy or reuse historical fixed party victories as real Alpha play.

**New bounded Alpha native L1 source witness:** [B04/B05/B06 Alpha Mixed-Party Encounter v0](b04-b05-b06-alpha-source-native-mixed-party-encounter-v0.md) proves exact shared G0/G3/G4/G5 co-existence of all four selected Focuses, both complete Low Priest A/B chosen Rites, one source Medium Anointed invested Step, native Gifted/Scholar Flame and four cautious exits against the original Soldier. It supplies **one author-fixed policy**, not a general source-legal player tactical menu. Any actual GM/player choices beyond that authored policy still need separate source preflight and human evidence.

**Alpha L1 tactical-choice preflight supplement:** [B04/B05/B06 Alpha L1 Tactical Choice & Defensive Response v0](b04-b05-b06-alpha-l1-tactical-defensive-response-v0.md) enumerates independently auditable Guard/Dodge/Take Hit, actual G0 AP/VP paid actions and nonterminal hold-position outcomes for the full selected Alpha L1 party. Players and the GM must still actually choose actions/defenses and report original evidence; source-fixed test branches do not constitute human C1–C7 play.

## Before real sessions

The GM and independent reviewer examine all four full original L1 sheets, source hashes, legal gear, selected/saved Talent/Training, initial HP/Vigor/VP/AP and native action eligibility. Select L2/L3 advancement choices without awarding levels in advance. A first-cohort packet leaves Low Priest A/B selection blank until the **player actually chooses**. Assign participant, GM, author and separate reviewer responsibilities outside the repository; keep personally identifying data and raw private session evidence in controlled local storage, never in these PR fixtures.

## Four-session candidate (not forced milestone schedule)

| Candidate session | Actual player/GM choices and consequences | Required collection |
|---|---|---|
| **1. L1 Supply/Gate** | Source-legal diagnosis, records, travel and alternative routes; combat only with an independently validated L1 Alpha engine | Real declarations, alternative, core rolls, GM ruling, before/after resources and elapsed G4.2 seconds. Milestone 1 **only if** GM actually declares significant group achievement. |
| **2. L2 Forest** | Hunter avoidance, real contact or withdrawal, Ward/guard/venom and pursuit if legally supported | Only after actual L1→L2 award; true L2 sheets, defense/attack costs, wound, toxin, clock and exit consequences |
| **3. L2 Shrine** | Choose cold/prepared Sentry only with legal fictional preparation, parley or alternate route | Actual action/GM decisions, source event receipts and separate group-story Milestone 2 if truly earned |
| **4. L3 Village** | Recovery, consequences, field support, genuine late-Focus combat and noncombat decisions | Level 3 legal play, review and unresolved issue reports, old VP/HP/ammo/poison clocks and outcome denominators |

The existing adventure supports 3–5 session groupings and flexible actual milestone placement. If a milestone is not awarded, characters stay their current level: record incomplete coverage, never force a fictional level change. Cross-level live maintained hosts/poisons require a source-authorized solution, not silent erasure or fixture-only VP refill policy.

## Working with the Alpha execution packet

Generate and check the unreported packet and the noncertifying readiness summary from the repository root:

    mkdir -p build
    python -m scripts.b04_b05_b06_b07_first_cohort_pilot_v0 --blank > build/first-cohort-alpha-blank.json
    python -m scripts.b04_b05_b06_b07_first_cohort_pilot_v0 > build/first-cohort-alpha-readiness.json
    python -m scripts.b04_b05_b06_b07_first_cohort_pilot_v0 --check build/first-cohort-alpha-blank.json

**When true external records exist**, work from a private copy of the packet and save actual primary materials under an access-controlled local evidence root. Run the independent offline file-integrity check:

    python -m scripts.b04_b05_b06_b07_first_cohort_pilot_v0 --check /private/pilot/alpha-intake.json --evidence-root /private/pilot/alpha-evidence

Do **not** upload any populated packet or private evidence root to public GitHub. The manifest requires exact unique opaque IDs, document kind, normalized root-relative path and lowercase 64-character SHA-256. It rejects missing/different bytes, duplicate names/paths, traversal, external symlink targets, unknown kinds and oversized files. If no --evidence-root is passed, it **cannot claim file integrity was verified**.

**Selected-sheet provenance is mandatory for reported evidence:** A Focus-level evidence row's nested sheet reference must equal the first-cohort character's explicitly selected sheet for that exact level. A GM milestone's reviewed sheet for every participating character must equal that character's selected **destination** level sheet; its preceding source level sheet must also be present. Reported rows cannot silently select a Priest/Low A/B variant, borrow another character's sheet, use an unselected manifest sheet, reuse a sheet across characters, or substitute a different level. Fully blank UNOBSERVED packets remain valid until a real character/player selection is recorded. Source/file reference matching is **not** proof of the selected sheet's contents or of independent human validation.

The original nested cohort format remains authoritative for sessions, scene level/beat/outcome, GM and player choices, source action, resource and world-clock references, separately declared milestones and their reviewed sheets. The new wrapper requires reported document references to exist in the file manifest **with the appropriate category**; a selected-source sheet and a GM adjudication are not interchangeable. Its 84 entries represent four characters × three levels × C1–C7 criteria. Each entry starts UNOBSERVED, with no invented witness. SUBMITTED requires a primary document, and later REVIEWED_NEEDS_FIX or REVIEWED_EVIDENCE_PRESENT requires named reviewer pseudonym and separate review notes. Neither means CERTIFIED.

## Independent reviewer procedure

1. **Source and identity (C1–C2):** independently retrieve actual source sheets, compare hashes and character/legal choices against source; check A/B Low Priest complete magic vs physical proxy; confirm reviewer is not the author, player or GM. Matching pseudonyms are not independent identity authentication.
2. **Combat and noncombat (C3–C4):** compare actual player action, rejected alternative, source prerequisite/roll, AP/VP/MP/Guard/Reaction, attack/response/target legality and consequence. Source-paid fixed-seed fixtures do not count as human decisions.
3. **Counterplay (C5):** capture a genuine legal failure/opportunity cost for each defining Focus mechanic at L1, L2 and L3. A negative deterministic regression may inform the reviewer but does not substitute for on-table choice.
4. **Session continuity (C6):** verify scene start/end party HP/Vigor/VP Available/Committed/Spent, wounds, arrows, recovery deadlines, spell hosts, toxin origins and elapsed travel, including attrition or safe rest actually adjudicated by GM.
5. **True group milestone (C7):** record two distinct actual GM story achievements and declarations, scene/time, each participating character's pre/post reviewed sheet, resource conservation and saved vs earned choices. Anointed Mission beats, victory and clock intervals never grant automatic level.
6. **Signoff:** independently examine original accessible raw materials and mark findings for B04/B05/B06/B07 corrections. Only an authorized actual review can decide whether C1–C7/Focus is satisfied; evaluate the six Create/Act/Resolve/Advance/Challenge/Observe gates separately after representative human data. No CLI or SHA can confer certification.

## Known technical blockers: stop rather than synthesize

- L1 four-Focus Alpha mixed combat has **no generally validated native G8 party resolver**; choose proven legal encounter or implement a tightly scoped adapter.
- L2 Hunter and Sentry opposition plus off-turn options must support the chosen actual Alpha abilities and reactions, not only an A/B/R/F original script.
- Medium Anointed one-Vessel investment must use genuine consent and recipient Step; High Gifted amplification/miscast must preserve native emotion and instability.
- Cross-level active toxins/maintained magic are not generally supported by the bounded #196 advancement bridge. Settle effects legally at milestone or implement separate explicit source rebind and regression.
- Actual human participants, GM(s), independent reviewer(s), session/clock decisions and calibration denominators have not been supplied. These are **external evidence and execution dependencies**, not bugs to “fix” with invented outcomes.

## Testing and non-certifying output

    python -m unittest discover -s tests -p 'test_b04_b05_b06_b07_first_cohort_pilot_v0.py' -v
    python -m unittest discover -s tests -v

The actual MVP status is unchanged: **12/12 structural Focus pairings, 0/12 independent full Focus certifications, 0/6 accepted gates, 0 verified human pilot sessions, 0 externally authenticated GM milestones; 3/7 original blocker definitions closed**. Passing all structural, manifest or source CI checks does not prove real play, independent review or lawful completion of the pilot.