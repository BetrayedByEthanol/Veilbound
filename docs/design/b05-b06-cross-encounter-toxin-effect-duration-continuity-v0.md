# B05/B06 — Cross-Encounter Toxin, Maintained Effect & Duration Continuity v0

> **Live G8 source-state continuation, not a campaign save format or external GM certification.** Extends [#194](b05-b06-native-cross-encounter-party-resource-continuity-v0.md) without altering the source G0–G8 combat, toxin, Venom Endurance, VP or recovery rules. Supports original A/B/R/F party (L2–3) in a completed source-attested G8 terminal, followed by a pristine native scene.

## Mechanism

Call `handoff(previous, following, elapsed_seconds=N, travel_ref="...", carry_effects=True)`. The previous default `carry_effects=False` remains explicitly **fail closed** on active poisons, non-Recovery deadlines, and unrecognized hosts.

The shared preflight authenticates the original G8 terminal and **validates the entire destination before charging time** (#194 Codex fix). The effects continuation additionally validates that pending G4.2 milestone deadlines correspond to actual source-owned G4.3 toxin instances, Hunter stage markers or G4.4 Venom Endurance instances; toxin profiles and keys are original; per-actor modifiers agree with the native interpreter; committed VP and G3 effects remain reconciled. Other marker sources, unsupported G3 timers and mismatches are rejected. It also advances a deep, cyclic clone of the old encounter through G4.2 to check future death/unsupported-state transitions **before actual source time moves**, preventing invalid travel from charging the original clock.

Once authorized, **only G4.2** advances actual exploration seconds. Copy the actual `ClockEvent` keys, original chronological orders, pending deadline seconds and serials already handled by #194. The new adapter also copies the native interpreters tied to them: G4.3 active and historical toxin state, both short-interval and event-based long profiles; the G4 legacy TX-HM six-second phase and already-consumed packet identities; G4.4 Endurance ward/suppression IDs, fixed 60-second expiry, prepaid Spent VP, units and partial local six-second suppression phase; and authenticated Hunter exposure stages/onset/escalation/expiry marker keys where a **genuine original G4.4 Bite** supplied them. Old Bite *ledger indexes* are encounter-local and deliberately do **not** become attack authority in the new scene; persistent exposure IDs remain protected against replay. No source-independent Hunter bite or venom is manufactured for the sample party.

### Multi-encounter TX-HM provenance and pulse evidence

Legacy G4 `schedule_hemotoxin()` records `g4_toxin_scheduled` in the original encounter ledger, **not** in G4.3 `toxins.exposure_ids`. Its provenance therefore travels separately as the original recipient/source digest, scene and native schedule event index, together with the still-existing historical TX-HM record. No extra G4.3 exposure identity is manufactured and no exposure is reapplied in later encounters. After a second real Soldier combat has advanced the remaining legacy Step-3 ticks, a third live handoff can still authenticate the original TX-HM; removing its carried provenance must fail before committing route time.

The JSON evidence matrix records the **original pending arrival marker ID before advancing the G4.2 clock**, then checks that this same event was consumed by the native pulse. The next newly scheduled marker is reported separately. A false original-marker identity now fails evidence generation instead of producing a misleading successful witness.

### Maintained G3 effects

- Source R's Chosen **Self Guided Regeneration** continues as in #194: one original host, 1 Committed VP, no recast or additional regeneration Step.
- Source F's actually paid **Stone Skin** may continue: original Committed VP, original self-host, +2 eligible physical resistance, no recast. The original G3 engine still ends this host on actual unconsciousness or other source triggers.
- Unsupported G3 host kinds, unproven extra effects, external recipients and **round-limited** spells continue to fail closed. Converting an unbounded combat-round duration into real exploration seconds would invent a new rule. Combat-only Exaltations still expire on the original G4.2 initiative exit; nothing recreates them.

### Native source witnesses and negative cases

The CI evidence generator and regressions use the *original* Soldier withdrawal and cold Sentry arrival. Positive witnesses exercise a real GM-attested G4.3 TX-NP exposure, retained original next-hour pulse, HP/Vigor/VP from prior engagement and a native G4 pulse on the correct deadline. Separate tests verify actual TX-EN long exposure with native Low Priest B paid Self Venom Endurance suppression; exact remaining 60-second expiry and 6-second covered interval units; old G4 legacy TX-HM partial six-second phase; native TX-HE interception of the original six-hour Recovery checkpoint; and the real source-F Stone Skin host. Exact receipts capture both source/arrival state hashes; a mismatch is not accepted as a completed import.

Negative tests reject malformed/missing event links, non-pristine destination, mismatched source effects, unsourced G3 duration and previously used toxin exposure keys. The three-hour rejected destination test from #194 remains in scope; invalid continuation preflight also leaves source world seconds and ledgers unchanged. No effect is applied without the original native source action, cost and legal timing.

## Explicit boundaries

Not a generic cloud save/load format, cross-level award, NPC poison transplant, automatic GM-pursuit/route decision, new toxin resistance test, arbitrary spell-maintenance interpreter, or probability/balance audit. Any active unrelated poison, clock source, maintained effect or unresolved action without native reconstruction stays a blocker. Data is source-bound and can be used for internal pilot candidate design, **not** claimed human play or independent Focus certification.

**MVP acceptance remains** 12/12 structural, 0/12 independent Focus certifications, 0/6 accepted gates, 3/7 original blocker definitions closed.

## Verification

```bash
python -m scripts.b05_b06_cross_encounter_effect_continuity_v0
python -m unittest discover -s tests -p 'test_b05_b06_cross_encounter_effect_continuity_v0.py' -v
python -m unittest discover -s tests -p 'test_b05_b06_native_party_continuity_v0.py' -v
python -m unittest discover -s tests -v
```
