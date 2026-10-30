# B04/B05 — Anointed Human Field-Pilot Evidence Intake v0

> **Practical evidence collection, not certified play or a new game rule.** This handoff follows merged **#177**: all three Life / Restoration Anointed Focuses have L1–3 structural characters, bounded native G0/G4/G5 combat actions (#168–176), and a source-bound G4.2 exploration/GM Mission accounting interface (#177). None of those deterministic witnesses establishes an **independent** character certificate, a real human decision, an authenticated GM judgement, balanced encounter difficulty, or one of the six strict MVP exits.

## What the pilot must actually observe

A **three-to-five-session** restricted pilot should follow a real player character through legal level progression and meaningful player-selected alternatives, not just replay the fixed d20 policies from #172–177. The encounter and noncombat protocol must preserve the **High / Medium / Low** Anointed differences:

| Focus | Combat alternatives requiring observation | Noncombat alternatives requiring observation |
|---|---|---|
| High Restoration (AH) | Actual G0 **30 AP Dagger** offense versus **20 AP paid Returning Step Projection** at a legal later turn, with possible normal/Lesser Vigor/finite-Destiny cost | Beneficial projection to a real consenting recipient, visibility/range and an actual GM-recognized Mission beat or explicit absence of one |
| Medium Restoration (AM) | Actual **24 AP one-Vessel General Investment**, recipient's real G4 Step pulse versus paid **24 AP Dagger** own-turn action, without pretending 48 AP fits L1 | Chosen willing Vessel, consent changes, distinction between an externally determined significant event and automatic free Destiny |
| Low Restoration (AL) | One authentic **20 AP Sword** source hit versus embodied self Returning Step **only on own G4 Step**; no 0-AP remote healing entitlement | Own Embodiment and active/dormant bond choices, independent real six-hour exploration clock, no manufactured new G0 Step |

These are **example decision questions, not mandatory scripts**. A human can choose other source-authorized actions. Player/GM uncertainty should be recorded, including declined attacks, no eligible wound, blocked Restoration, and unresolved contested beneficial **+8 Intrusion** rather than improvising an unauthorized automatic success. Outcomes, resource expenditure, source receipts and the alternatives actually considered must remain distinct.

A reported mission story beat (for example, curing a village) is **not** automatically GM-recognized, and the continuing Mission does **not** end with any one milestone. No player receives a free source ability merely from participating in the pilot.

## Nine structural slots and four evidence domains

The [source-bound evidence intake CLI](../../scripts/b05_anointed_pilot_evidence_intake_v0.py) enumerates **nine** candidate **Anointed Focus × level slots**: AH/AM/AL × L1, L2, L3, using actual current source actors and file fingerprints. This is a **subset** of the existing **12/12** Archetype × Focus structural roster, not an alternative 9/12 roster or an assertion that each slot is a separately certified pairing.

For each real session, capture an explicit session identifier/date/order, the exact character source role and SHA, a scenario identifier, a GM observation reference, and recorded **human** player decisions with separate **chosen action, meaningful alternative considered, observed consequence and source/event reference**. Each decision is tagged to one of four domains:

- **combat:** actual opponent, target, AP/Guard/response choice, source-paid native event, injury/withdrawal consequence;
- **exploration:** physical travel/problem choice, real G4.2 time and environmental consequences; no synthetic combat clock;
- **mission:** external GM recognition or refusal and a distinct significant-event ID, with active bond and finite Destiny consequence;
- **advancement:** independent L1→L2→L3 options, purchase/training/repertoire decision and resulting resource budget.

A single session need not cover all domains; the **aggregate** reports only what a submitter *claims* to have recorded. Repeated sessions across real 3–5-session play should be separated. The validator does **not** assert that every referenced native trace exists, was legitimately resolved, was observed by a human, or belongs to a real authenticated GM. A hash of self-provided data is an integrity label, **not independent evidence**.

## Workflow

From the repository root:

```bash
python -m scripts.b05_anointed_pilot_evidence_intake_v0 --slots
python -m scripts.b05_anointed_pilot_evidence_intake_v0 --template --focus High --level 1 > pilot-blank.json
# Only after actual human play: fill all external references and decisions.
python -m scripts.b05_anointed_pilot_evidence_intake_v0 --check pilot-filled.json
# Optional: a JSON array of independently supplied, filled session records.
python -m scripts.b05_anointed_pilot_evidence_intake_v0 --aggregate real-session-forms.json
```

Blank forms have **no fabricated observations** and fail filled-submission validation by design. A structurally valid form is still **unverified**. It can demonstrate current source-role identity, explicit candidate decisions and unique per-session IDs; it cannot confirm the GM's identity, source-ledger authenticity, consent, contested Intrusion outcome, genuinely independently reviewed progression, or real player agency. All **nine** slots remain `SOURCE_STRUCTURAL_ONLY`, and the aggregate always reports **zero externally verified sessions, zero independently certified Focuses and zero closed MVP exits** until a separate, authorized verification process is established. A fully populated candidate never automatically graduates to certification.

## Acceptance boundary and next work

The [ten regression methods](../../tests/test_b05_anointed_pilot_evidence_intake_v0.py) confirm the nine exact AH/AM/AL L1–3 source hashes, reject spoofed roles/hashes and self-declared certification flags, require attributable session/decision fields and different alternatives, preserve nonempty external-reporter references, and refuse duplicate session identities. Even nine apparently complete candidate forms do not close a gate.

**Unresolved external requirements** remain: an independent reviewer for every legal character and level transition; genuine human and GM decisions with verifiable provenance; multi-encounter tactical/defensive and contested-consent decisions; diverse **combat and noncombat** objectives; representative challenge calibration; and GM-recognized Mission events without auto-inference.

Therefore this **is not certified** Anointed field play, individual Focus feasibility or B07 representative observation. The project remains **12/12 structural Focus pairings, 0/12 independently certified, 0/6 strict MVP exits**. B04–B07 stay open; original B06 G0–G8 is unchanged. The next step after intake is real external 3–5-session play, independent evidence review and adjudication of unresolved choices, **not** adding more nominally representative scripted case counts.
