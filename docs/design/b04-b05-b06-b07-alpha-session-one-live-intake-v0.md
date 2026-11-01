# B04/B05/B06/B07 — Alpha Session 1 Preflight & Live Evidence Intake v0

> **External GM/player operations, not a new gameplay engine or certification.** Extends the [Session 1 GM packet](b04-b05-b06-b07-alpha-session-one-gm-packet-v0.md) and the [canonical first-cohort Alpha intake](b04-b05-b06-b07-first-cohort-pilot-execution-evidence-v0.md). Does not change the source rules, four Focuses, 84 C1–C7 review slots, or GM Milestones. Real decisions and primary evidence must be supplied by actual humans, never fabricated by test fixtures.

## Operational go/no-go

| Stage | Required actual action | Machine preflight | What is never authenticated |
|---|---|---|---|
| **Before Session 1** | GM sets true spoilage, ring, map, keeper, Soldier motive and table safety; four players choose source-legal L1 Priest/Low **A or B**, Scholar/High, Gifted/High and Anointed/Medium, with paid actions and persistent resources; reviewer and evidence storage arranged | Reports missing preparation field names and missing selected generic PC IDs; filled references mean **REFERENCE_ONLY_POSSIBLE_INTAKE** | Identity, consent, source legality or real play |
| **During Session 1** | Run **Supply → Gate at L1**, record actual crossing, herb/ring inspection, keeper petition and optional Soldier conflict; each player chooses actions and legal alternatives; GM adjudicates facts, rolls and consequences | Original worksheet stages are **UNOBSERVED**, **SOURCE_REPORTED** or **SOURCE_BLOCKED**; unresolved tactics stay held | Automated successes or compulsory combat |
| **After actual Session 1** | Register real private evidence files and SHA-256, fill *existing* canonical Alpha packet and worksheet using the same scene IDs and original source reference IDs | Read-only crossbind invokes original canonical validator with a **required evidence-root byte check**, then matches sources and stage/scene chronology | That a hash proves an honest person acted or rolled lawfully |
| **Independent review** | A separate real reviewer checks character legality, actual player options, countercases, GM rulings, resources, original source and declarations; enters findings in original C1–C7 intake | Only structural review references are checked; all real session/certification counters remain zero | Independence, real GM milestone or any MVP exit |

**Current baseline:** an unobserved blank Alpha Session 1 worksheet is **NO GO for live intake** until actual pre-session sources, GM truth and player choices are provided. A GM may still run a lawful real tabletop session with canonical referee rulings; no universal automated four-PC encounter engine is claimed.

## Exact source-reference crosswalk

Each genuine completed worksheet scene has the original scene ID, chosen and declined legal action, GM ruling, exact source action, source before/after resources, G4.2 clock and separately recorded actual outcome.

| Session 1 worksheet field | Canonical first-cohort scene field | Mandatory evidence category |
|---|---|---|
| `scene_ref` | `scene_id` | Unique scene ID; not a file |
| `chosen_ref` | `choice_ref` | `player_choice` |
| `declined_alternative_ref` | `alternative_ref` | `player_choice` |
| `gm_consequence_ref` | `gm_consequence_ref` | `gm_adjudication` |
| `source_action_ref` | `source_action_ref` | `source_action` |
| `resource_before_ref` | `resource_before_ref` | `resource_snapshot` |
| `resource_after_ref` | `resource_after_ref` | `resource_snapshot` |
| `clock_ref` | `world_clock_ref` | `clock_trace` |
| `outcome_ref` | Separate registered outcome file | `gm_adjudication` |

Only `SOURCE_REPORTED` stages become original canonical **L1 supply/gate** scenes. The optional `gate_hostility` stage stays unobserved if the Soldier never attacks; it cannot be credited as C3 combat evidence. The original stage order cannot be changed or supplemented by an out-of-band battle.

A `SOURCE_BLOCKED` stage holds its original stop/GM ruling, source issue/countercase, before-resources and clock references, **not** a fake resolved canonical scene. A private canonical packet may record other genuinely resolved scenes alongside a blocked stage, but the result remains **HOLD_FOR_SOURCE_ADJUDICATION**. Record the exact missing source mechanic, or resolve under canonical rules with separately reviewable evidence. No scripted G5 terminal or safe rest may substitute for that missing action.

### Four original source-legal sheets and continuation

All four worksheet L1 selected sheets and explicit variants must match **the same original** canonical Alpha selected characters, source fingerprints, nested player references and actual original source-sheet evidence. A historical physical Priest A/B proxy is not a full Low Priest legal source. Each starting-resource reference must be present as an original `resource_snapshot`. The worksheet end resources must match the canonical session's end snapshot, with the actual end G4.2 clock attached as a `clock_trace`. Preserve HP, Vigor, VP Available/Committed/Spent, wounds/Dying, ammunition, effect hosts, Guard/Dodge, initiative time, recovery deadlines, actual travel and scene consequences without invented refill.

**Milestone One remains optional.** If the GM truly declares a significant group supply story beat, record a separate event ID, an original `milestone_declaration` file, a genuine story `gm_adjudication`, the **actual gate scene** it follows and four original independently reviewed L2 destination-sheet refs. The declaration *file reference* is not required to equal the independent GM event ID. The verifier only checks that the worksheet and original Alpha packet agree. It cannot give the four PCs L2, authenticate a GM, declare a safe six-hour rest, or choose the real advancement VP policy. If no group beat is declared, both sources stay unawarded and the party remains L1.

## Secure four-step workflow

1. **Prepare locally outside Git and public CI.** Generate a blank worksheet and the *existing* canonical Alpha intake. Do not fill missing sections with synthetic outcomes:

   ~~~bash
   mkdir -p /private/veilbound/alpha
   python -m scripts.b04_b05_b06_b07_alpha_session_one_v0 --blank > /private/veilbound/alpha/session-one.json
   python -m scripts.b04_b05_b06_b07_first_cohort_pilot_v0 --blank > /private/veilbound/alpha/intake.json
   python -m scripts.b04_b05_b06_b07_alpha_session_one_live_intake_v0 --preflight /private/veilbound/alpha/session-one.json
   ~~~

2. **Actual GM and players decide.** Complete source-selected L1 sheets, GM scene facts, safety and independent reviewer arrangements, and actual before resources. Run the four [Session 1 scene cards](b04-b05-b06-b07-alpha-session-one-gm-packet-v0.md) only as warranted by player choices. For actual scene attempts, record original rolls, alternative actions, source AP/VP/MP/Guard/response, combat/noncombat consequences and clock time. Re-run `--preflight` as new source choices are recorded; it is still noncertifying.

3. **Store original primary bytes privately.** For each original record, use a unique normalized root-relative path such as `records/s1-crossing-choice.md`, one matching document kind, unique `ref_id` and actual SHA-256 in canonical `evidence_files`. Example:

   ~~~bash
   sha256sum /private/veilbound/alpha/evidence/records/s1-crossing-choice.md
   ~~~

   Do not put filled packets, notes, participants, raw rolls or evidence files in CI artifacts or public PRs. The original validator already refuses path traversal, out-of-root symlinks, stale hashes and wrong categories. A SHA hash proves file-byte consistency only.

4. **Read-only local intake and real independent review.** Fill the canonical session (original GM, report author and players, selected L1 sheets and review notes, actual scene records, starting and ending resources, actual story award if any) and the Session 1 worksheet with **matching original reference IDs**. Then:

   ~~~bash
   python -m scripts.b04_b05_b06_b07_first_cohort_pilot_v0 --check /private/veilbound/alpha/intake.json --evidence-root /private/veilbound/alpha/evidence
   python -m scripts.b04_b05_b06_b07_alpha_session_one_live_intake_v0 --intake /private/veilbound/alpha/session-one.json --packet /private/veilbound/alpha/intake.json --evidence-root /private/veilbound/alpha/evidence
   ~~~

   The commands **never modify or import** the private packet. The new cross-check rejects unregistered bytes, mismatch between chosen/declined options and canonical scene fields, source substitution, wrong GM/session, changed or missing end-state, extra invented played scenes, and milestone declaration disagreements. It allows a source-blocked stage only when marked and held distinctly.

The new module's default command emits a safe blank readiness report; it does not request private files from CI. Its responses omit human pseudonyms and primary content. The independent reviewer still must inspect the **actual original** character and raw action evidence, cost/roll/clock legality, GM truth, countercases, and original C1–C7 entries, keeping unresolved slots unobserved or requiring fixes. The machine can accept schema fields labelled `REVIEWED_EVIDENCE_PRESENT` without knowing if any person actually reviewed anything.

## Regression and acceptance

Run focused tests and general tests from repository root:

~~~bash
python -m unittest discover -s tests -p 'test_b04_b05_b06_b07_alpha_session_one_live_intake_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.b04_b05_b06_b07_alpha_session_one_live_intake_v0
~~~

Focused tests deliberately create and remove *test-only* source-shaped files in a temporary directory. They cover positive structural crossbinding, immutable canonical files, absent local evidence-root, stale SHA, false local/canonical choice or alternative, missing state/clock, wrong scene/order, original Focus substitution, blocked tactics, unfounded/mismatched milestones, wrong file categories, private path escapes and no fake certification. CI uploads only the blank preflight; **never** a completed human session, client note or private file.

**MVP readiness is unchanged:** 12/12 structurally source-legal Focuses, **0/12 independently certified**, **0/6 accepted strict MVP gates**, 3/7 original blocker definitions closed, **0 externally authenticated Alpha sessions**. The intended next real progress is an actual table with externally reviewed evidence, not another deterministic replay.
