# B04/B05/B06/B07 — Alpha Cohort Pilot Readiness & GM Execution Handoff v0

> **Operational go/no-go and external tabletop handoff, not a claimed playtest.** Source-checked against the merged Alpha L1–L3 native chain, L1 tactical branches, original Hunter venom and Sentry damage, and the already-versioned first-cohort evidence validator. This does not change canonical combat, level-up rules, the original Alpha packet schema, B06 G0–G8 milestones, independent certificate counts or MVP acceptance.

## Current decision: conditional controlled-tabletop GO, not automated-pilot GO

| Intended use | Decision | Required boundary |
|---|---|---|
| **GM-led actual Alpha sessions** | **CONDITIONAL GO** after pre-session preparation | A GM and players use independently reviewed full legal source sheets, set the real scene facts, choose actions, adjudicate *unsupported* branches from canonical rules or explicitly stop and request source implementation, record all costs and consequences, and have independent reviewer/evidence arrangements in place. No test runner is the table's GM. |
| **Automated arbitrary four-PC L1–L3 campaign** | **NO GO** | Current Alpha code only executes authored source-bounded options and explicit histories. It does not auto-resolve arbitrary responses, tactical choices, attacks, hazards, terrain or social fiction. |
| **Automatic L2→L3 level gain with live venom/maintained effects** | **NO GO** | Same-level active Hunter G4.4/Endurance handoff is implemented. Cross-level active toxin/G3 effect migration is not. Settle the effect **legally before a milestone**, or stop and implement a validated same-source level-transition path; never wipe or free-restore state. |
| **Independent Focus certification or six-gate MVP signoff** | **NO GO until genuine play and external review** | The 12 structural pairings and all 36 pairing-level C1–C7 obligations require actual independent evidence across Alpha/Beta/Gamma. Alpha's 84 worksheet slots cover four pairings × L1–L3, not a substitute for the other eight Focuses. |

**Baseline (no fabricated progress):** 12/12 structural pairings, **0/12 independently full-play-certified**, **0/6 strict accepted MVP gates**, **0 externally authenticated Alpha sessions** and **0 actual GM-declared story milestone events**; B01–B03 definition-closed, B04–B07 open. Source-fixture checks can pass without changing any of these numbers.

The original [first-cohort execution packet](b04-b05-b06-b07-first-cohort-pilot-execution-evidence-v0.md) contains a **frozen historical** \`scenario_gaps\` field and a structural validator that requires its original contents. That text originally said no mixed L1 Alpha encounter existed; **it must not be quietly altered** to update the historical record. The present audit instead reassesses its scope:

| Original gap | What merged native work actually supports | What remains for a human-selected scene |
|---|---|---|
| L1 Alpha four-person combat | [Real source L1 Soldier and Priest A/B support](b04-b05-b06-alpha-source-native-mixed-party-encounter-v0.md); [Guard/Dodge/Take Hit and optional actions](b04-b05-b06-alpha-l1-tactical-defensive-response-v0.md) | Arbitrary actions, off-turn opportunities, custom map, non-scripted opponent policies; the GM must source-adjudicate or block |
| L2 Hunter | [Actual source 1×2 Bite, G4.4 venom/Endurance](b04-b05-b06-alpha-hunter-venom-sentry-effects-v0.md) and [clean L2 Hunter stage](b04-b05-b06-alpha-l2-l3-mixed-advancement-v0.md) | Player-defined cover, Pounce/response choices, pursuit, safe long recovery and real alternative encounter outcomes |
| L2 Sentry | Cold source Reserve and one real HP/Fire/Vigor hit, and a bounded enhanced attack/retreat; original GM pack has cold/prepared reference | Confirm which original enemy state fiction permits, actual L2 defender reactions, terrain and unchosen ending |
| L3 village | Legal selected L3 source profiles and author-candidate progression | Genuine diagnosis, healing/supply resolution, noncombat agency, late-Focus counterexamples and truthful aftermath |
| Cross-level live effects | Original G4.2 clock and same-level toxin histories survive native handoff with atomic preflight | Active venom, maintained host, unknown effects or unsafe pursuit **cannot** be silently imported across a level-up |
| Real human play and calibration | Blank Alpha 84-slot intake, real-file SHA validation and four-session candidate | Actual named-by-pseudonym participants, GM and independent reviewer, raw decisions, full resource and time receipts, repeated opponent alternatives and verified denominators |

## Preparation before Session 1 (stop/go card)

Check each box **from real source records**, not by copying CI fixture outcomes:

- [ ] **GM and players assigned.** Four source characters are Priest/Low, Scholar/High, Gifted/High and Anointed/Medium. Use distinct local pseudonymous IDs. The GM, report author and independent reviewer have separately agreed their actual roles; do not assert that a validator authenticated anyone.
- [ ] **Full selected L1 sheets are reviewed.** Priest/Low player explicitly chooses *A or B*, with real prepared spells, hands, Exaltation, weapons and costs (not just the G8 physical proxy). Other characters have actual selected spell formulas, Gifted linked Emotion/Aspect and Anointed bond/Signature/Vessel. Save signed-off source path and SHA-256.
- [ ] **Start ledger recorded.** Actual HP/Vigor, available/committed/spent VP, AP/physical/magical tempo, guard/dodge state, weapons/ammunition, prepared techniques, saved Talents/Training, wounds/conditions and G4.2 current/recovery clocks. Do not claim an initial free refill later in the campaign.
- [ ] **The GM establishes scenario truth.** Spoilage cause and discoverable clues, public log ownership, gate motives, alternative crossings/negotiation, Hunter warning/pursuit and Sentry cold/prepared state are specified *before* testing. No scripted success, assumed miraculous cure or invented Universal social bonus.
- [ ] **Five-beat episode path and 3–5 session plan selected.** Use [integrated adventure](b04-b05-b06-b07-integrated-mvp-pilot-adventure-v0.md): **supply → gate → forest → shrine → village**. Suggested four-session grouping is S1 supply/gate L1, S2 forest L2, S3 shrine L2 and S4 village L3. This is **not** a forced leveling schedule.
- [ ] **Source boundary rules are explicit.** When a chosen combat/magic/noncombat action, target or response is outside the audited native policy, the referee must decide using canonical \`docs/rules/\` and preserve a new original source-legal receipt, or halt that encounter and open a specific implementation issue. Never relabel fixed G8 A/B/R/F output as the real Alpha party.
- [ ] **Safety and session logistics agreed.** Actual dates/availability, consent and table safety arrangements, permitted recording methods, secure evidence storage, GM/referee resolution of disputes, and a plan for a withdrawn Hunter's pursuit or unsafe travel.
- [ ] **Private evidence root ready.** Do not put filled intake files, raw rolls/session notes with personal information, or source-linked private files in public pull requests or CI artifact uploads.

If a required pre-session condition fails, **do not claim the pilot is ready to run the affected source scene**. Absence of a universal automated encounter engine does not forbid real tabletop adjudication, but using an **unsupported automated action** must stop rather than pretending a result is legal.

## Five-beat execution and source/GM boundaries

| Beat (target level only) | Source reference / legal choices | Capture at the table | Stop or fallback |
|---|---|---|---|
| **Supply (L1)** | Original noncombat crossing, diagnosis, Universal Veil Inspection only under real hand/item and known-access conditions | Player selects check or Veil action vs alternative; actual GM difficulty, successes, resource costs, missed knowledge, travel seconds | If unknown cure/cause, reveal only supported information; another source-legal lead or genuine uncertainty |
| **Gate (L1)** | Soldier social/log options; L1 actual Alpha Soldier and bounded Guard/Dodge, paid Rite, Conjure Flame, Emotion and Anointed Investment | GM motive and soldier initial state, full positions, each actor's real chosen AP/MP/VP/Guard/roll, changes, withdrawal/pursuit; adverse alternative | No fabricated win or downleveled Soldier; any unsupported response requires separate source adjudication |
| **Forest (L2 after **actual** award one)** | Anatomical Hunter contact/avoidance, genuine Bite, Ward or A/B source-eligible Venom Endurance, retreat | Source Bite penetration and d20, poison grade/resistance, unique exposure key and G4.2 deadlines, real pursuit/safe travel, what choices were declined | No automatic rest from scene exit; prevent unearned poison cure or mismatched character source |
| **Shrine (L2)** | Cold/prepared original Sentry and real paid Reserve/physical+Fire+Vigor packets, parley/alternate entrance | Enemy preparation truth, physical/Fire resistance, real protection and Dodge/Guard, party attrition, source time, noncombat route | **Before level-up**, resolve active toxin/host under canonical rules or separately implement legal cross-level continuation |
| **Village (L3 after **actual** award two)** | Original L3 selected Focus source and supply consequence alternatives, potentially source-legal adversaries | GM adjudication of cure vs supply replacement, genuine support choices, continued Anointed Mission beats, unresolved adverse effects, countercase/weakness for each role | No automatic village cure, universal L3 spell access or scripted perfect ending |

The preferred **first table run** is to let actual players choose and record truthfully, not insist that the native fixed-scene outcome occur. If an encounter is blocked because a participant picks an unimplemented but plausible rule branch, **log the exact source and user-chosen trigger** (C3/C5), postpone that specific action or resolve from canonical tabletop rules with external review. Do not turn the blocked case into a fake negative test or a forced success.

## Milestone One and Two: audit separately, never automatically

For *each* actual group-level award, collect the **GM's own declared significant group-story event, scene/time, participant list, pre-award L1/L2 selected sheets, destination L2/L3 selected sheets, source purchase/grant/saved Talent/Training ledgers, and exact HP/Vigor/VP/wounds/clock changes**. The example gate and shrine windows are **only candidate** events. Actual rewards can be earlier/later or never occur. Anointed Mission beats do not automatically grant group character level. The synthetic L1–L3 progression tests conservatively stage increased Max VP as Spent; this is **not canonical permission** to impose that policy on real players. The GM/reviewer must consult the actual advancement/resource rule source.

When the group does not earn a milestone, keep its actual level. Record that the planned C2/C7 and higher-level C3/C4 evidence remains missing rather than inventing L2/L3 events or teleporting to the next prewritten encounter. If an active toxin/maintained effect persists across the proposed level-up boundary, **stop the unsupported transition** or wait for legitimate native resolution. A real timing decision, pursuit, or unsafe downtime must be recorded separately.

## Raw evidence capture per real scene

Each **real** scene needs an original reference (private files, not hashes alone) for: scene/session ID, GM and participating player pseudonyms, source sheet revision, source situation and locations, choice and unchosen legal alternative, initiative/AP/VP/MP and response declaration, actual dice and source difficulty, real G4 HP/Vigor/wound/Endurance or G4.2 elapsed time receipts, GM consequence, resource snapshot before/after and source-linked countercase. Compare next-scene begin against prior-scene end; every difference requires a real interscene transition or lawful recovery reference.

For each of the four Alpha pairing-levels across L1/L2/L3, collect C1–C7 as defined by the [independent protocol](b04-b07-independent-twelve-focus-certification-protocol-pilot-roster-v0.md): C1 exact legal sheet; C2 actual progression; C3 human combat choice/alternative; C4 human noncombat choice/alternative; C5 genuine weakness/countercase; C6 independent reviewer and primary record; C7 two genuinely GM-declared group awards where applicable. The **84-slot queue** comes from 4 × 3 × 7. It is **not 84 certifications**. The independent reviewer must separately check original source legality and reject unsupported costs; a value marked \`REVIEWED_EVIDENCE_PRESENT\` in JSON still **cannot** prove an independent person reviewed it.

Keep the privately completed [existing packet](b04-b05-b06-b07-first-cohort-pilot-execution-evidence-v0.md) as the canonical **Alpha evidence intake**. The handoff script reads and validates it without changing the packet, accepting only the existing allowed source variant/sheet selections and primary-file hash references. The report intentionally echoes only non-identifying counts and flags.

## Go/no-go, triage and ownership

The machine-generated report has **eight individually classified prerequisite entries**: P01 participants/sheets (**external**), P02 fictional premises (**GM**), P03 unsupported Alpha mixed options (**conditional implementation/referee**), P04 true story milestones (**external GM**), P05 cross-level live effects (**conditional implementation**), P06 canonical advancement VP/resource refresh (**GM/source review**), P07 true positive/negative play at all levels (**external**), P08 independent C1–C7 and Create/Act/Resolve/Advance/Challenge/Observe gate signoffs (**external review**). A *design decision* is only needed if the actual chosen pilot requires new authority; do not reopen previously approved Milestones, provisional Low Gifted Rooted Guard +1/Unbound Step −1 MP or existing Gifted number watches without observed evidence.

**Coverage is not acceptance:** Alpha can gather four of the twelve pairing-level lines per level (12 Alpha Focus-level cases, 84 criterion slots), but the other eight pairings remain allocated to [Beta and Gamma](b04-b06-b07-persistent-adventure-acceptance-certification-readiness-v0.md). Do not pronounce the Create gate complete after only one cohort; no numerical Hunter CR, balanced win rate, authentic session count or six-gate signoff comes from deterministic scenario fixture output.

## Execute with existing source validation (offline, no personal data in Git)

Generate a safe blank Alpha packet and a **machine-readable source handoff**:

\`\`\`bash
mkdir -p build
python -m scripts.b04_b05_b06_b07_alpha_pilot_handoff_v0 --blank-packet > build/alpha-blank-private-template.json
python -m scripts.b04_b05_b06_b07_alpha_pilot_handoff_v0 > build/alpha-gm-readiness-public-v0.json
python -m scripts.b04_b05_b06_b07_alpha_pilot_handoff_v0 --packet build/alpha-blank-private-template.json
\`\`\`

When **real** private evidence exists, use the *original* validator and handoff from an access-controlled local path (never check completed packets into the repository):

\`\`\`bash
python -m scripts.b04_b05_b06_b07_first_cohort_pilot_v0 --check /private/veilbound/alpha-intake.json --evidence-root /private/veilbound/alpha-evidence
python -m scripts.b04_b05_b06_b07_alpha_pilot_handoff_v0 --packet /private/veilbound/alpha-intake.json --evidence-root /private/veilbound/alpha-evidence
\`\`\`

Both commands verify **schema and optional local bytes only**, not original human authenticity, legal dice/choices or GM/reviewer independence. The unchanged packet keeps the original SHA-256 source roster, selected sheet, milestone, 84-slot and cross-character reference restrictions.

\`\`\`bash
python -m unittest discover -s tests -p 'test_b04_b05_b06_b07_alpha_pilot_handoff_v0.py' -v
python -m unittest discover -s tests -v
\`\`\`

**The next genuinely new artifact is an actual GM/player session record**, followed by independent review and a concrete source-fix PR **only if** a real choice requires missing implementation. No automatic blocker/gate closure is proposed by this handoff.
