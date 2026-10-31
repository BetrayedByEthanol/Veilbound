# B04/B07 — Pilot Evidence Intake Flexibility & Multi-Cohort Attribution v0

> Candidate-only pilot evidence intake following merged PR #190. This is not a new rules engine, a real human session, a GM award, independent Focus certification or an MVP gate closure.

## Purpose and preserved source contract

The original [PR #190 integrated adventure](b04-b05-b06-b07-integrated-mvp-pilot-adventure-v0.md) keeps its fixed 3/4/5-session candidate planner and immutable versioned intake. That *example plan* anticipates a group-story milestone after the gate and another after the shrine. Real GMs may award one or both at another significant moment, defer them or never award them. Its single-campaign evidence cannot safely attribute many rotating parties to the same 36 Focus × level review targets.

This new, separately versioned intake reuses the twelve-pairing roster and its exact original source fingerprints without modifying PR #190's planner, canonical rules, mechanical effects, character files or historic bounded audits.

## Multi-cohort evidence contract

- A packet has a canonical source roster digest, one or more uniquely identified **cohorts**, and reserved, permanently zero independent-certification fields. Each cohort contains 1–5 source-identified characters, each with a cohort-local character ID, pairing, original source fingerprints and player reference. The same Focus pairing may appear in separate cohorts without multiplying its distinct Focus-level coverage.
- Within a cohort, each reported session owns its GM and report-author context, a globally unique session ID, played-at reference, original beginning/ending resource snapshot references, and one or more scenes. A session may hold scenes at different levels *only after* a genuinely GM-declared in-session milestone. All scene IDs, session IDs and milestone event IDs must be globally unique across cohorts.
- Scenes are source-declared actions at an actual level, with original five-beat order preserved: supply → gate → forest → shrine → village. Scenes may repeat within the same beat and can be grouped differently across actual sessions; the script does not create new GM outcomes, enemies, magic or legal AP/VP actions.
- A cohort can report **zero, one or two distinct** group-story milestone events. Each event references the exact actual scene after which the GM declared it, its significant story achievement, and a *separate reviewed L2/L3 sheet for each participating character*. The second must occur after the first at a later scene. The next scene must have the newly granted level. Award placement is **not** restricted to the proposed gate or shrine windows, and neither the first nor the second award is automatic.
- A session handoff binds the preceding end-state reference exactly. If the next session starts with a changed resource state, an additional inter-session transition reference must account for the actual source-legal clock, safety, healing, wounds, Vigor, VP, ammunition and pursuit. This is only an assertion until external source/GM review.
- A Focus-level evidence record belongs to one actual cohort character and one actual L1/L2/L3. Combat, noncombat and weakness scene IDs must exist **inside that cohort at exactly that level**. Independently reviewed sheet, player alternative and countercase evidence are mandatory strings for a *candidate* row, never proof that the choices really happened or were legal.
- The preflight counts unique candidate Focus × level rows across cohorts, while retaining the exact contributing cohort/character references. It does not overcount repeated Focus pairings and it cannot authenticate identities, decisions, source legality, reviewers, genuine milestone awards or completed game sessions.

## Usage

Generate one blank cohort with 1–5 distinct roster pairings:

```bash
python -m scripts.b04_b07_pilot_evidence_cohorts_v0 --blank-cohort C1 --pairing Priest/High --pairing Scholar/Low > pilot-cohorts.json
python -m scripts.b04_b07_pilot_evidence_cohorts_v0 --check pilot-cohorts.json
python -m unittest discover -s tests -p 'test_b04_b07_pilot_evidence_cohorts_v0.py' -v
```

To include another real party, generate a second blank candidate and append only its cohort object to the first packet's cohorts list. Preserve the unchanged version and roster digest. Fill GM, player, source, session, scene, actual milestone and reviewer references only after those events are observed. The validator accepts a partial campaign without milestone awards; such a packet is *not* a completed 3–5-session pilot.

An illustrative allowed chronology: after the supply scene, the GM recognizes the group's evidence as a meaningful story milestone, so the next gate scene is L2; after a later forest scene, another genuine distinct event permits L3 in the following shrine scene. Another cohort may remain L1 through the gate and reach L2 later. Neither schedule is assumed or certified by this tool.

## Test and acceptance boundary

The regressions reject wrong levels before or after milestone events; nonsequential, duplicate or foreign awards; missing participant sheets; ID collisions across cohorts; character source tampering; foreign or wrong-level evidence; false certificate flags; and handoffs that silently alter resources. Positive synthetic examples are explicitly labeled *not human play*. The GitHub Actions exact-head audit runs the new focused tests, blank cohort validation and the existing repository suite.

**Unchanged strict status:** 12/12 structural builds, 0/12 independently full-certified pairings, 0/6 MVP gates, 3/7 original blockers closed, and G0–G8 delivered only in their bounded implementation scope. Next playability gaps include L1 hostile combat, complete Low Priest noncombat source sheets, true multi-encounter party state and independently observed and reviewed pilot sessions.
