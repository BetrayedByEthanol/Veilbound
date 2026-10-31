# B05/B06 — Native Cross-Encounter Party Resource Continuity v0

> **Bounded two-engagement source evidence, not campaign persistence or human GM certification.** This is an *exact live-instance handoff* for a source-attested, complete G8 terminal into a fresh native G0/G1/G2/G3/G4 encounter. There is no new healing, MP, ammo refund, spell, duration, wounds, Hunter CR, encounter balance adjustment, or advancement rule.

## Problem and resolution

G8's standalone Soldier/Sentry policies intentionally build full initial party resources for each run. Passing their textual report or `_snapshot()` to a second scene **does not** carry actual VP Committed/Spent, Vigor, wounds, equipment readiness, ammunition, G3 maintained hosts or unconsumed G4.2 recovery checkpoints. Reusing the same source-level but rebuilding the default character would erase attrition and make a downstream victory unearned.

`scripts/b05_b06_native_party_continuity_v0.py` now supports a **trusted live-instance** handoff across the original four selected G8 party roles (A Low Life Vanguard, B Low Life Guardian, R Bow Priest and F High Fire Scholar) at **L2 or L3**. It checks the original completed `g8_bounded_terminal_attested`, genuine G0 Round End, no open G5 attack/response/movement reservation, actual source identity/digest and pristine new source-default placeholders **before importing resources**. Merely supplying a JSON report or fake 64-character digest cannot create the handoff; both actual native `Encounter` instances are required.

**Transactional destination preflight:** All target source identities, unmodified A/B/R/F actor fields and ammunition, G2 wielded state, empty party-owned G3 hosts and the newly constructed G4.2 Recovery clock/ID namespace are checked **before** calling the source clock's `advance_exploration`. A rejected handoff leaves the prior world seconds, pending Recovery checkpoints, source party and source event ledger unchanged; a corrected destination can retry the same authored interval without receiving a double six-hour Recovery. The regression explicitly rejects a modified 20→999-arrow destination at 10,800 seconds and then accepts a corrected three-hour transfer at exactly 10,800—not 21,600—seconds.

It copies the current exact HP, Vigor, VP Available/Committed/Spent, wounds and repair progress/source events, ammunition, conditions, earned milestones, Blink debt, current held equipment and source-supported maintained effects. Turn AP/MP, Guard/reaction and Dodge pressure are **not** imported as free bonuses; the new scene's first genuine Round Begin/own-turn Step reestablishes normal capacities. Positions are newly *authored scene entry geometry*, not copied squares or free G1 movement. A separate nonempty travel reference and exact elapsed G4.2 exploration seconds are mandatory, and departure/arrival/source fingerprints and previous/current ledger digests appear in the receipt.

The original G4.2 `ClockEvent` Recovery identities, next deadlines and per-actor serials are carried, including previously consumed checkpoints. New adversaries earn a **fresh** six-hour phase at arrival; no party recovery phase starts over. Actual elapsed time is advanced only by the original event-driven G4.2 clock before capture. This preserves scheduled recovery, VP Spent recovery and Vigor quarter-max limits, without extra checkpoints, early Regeneration Steps or free wound healing.

Supported G3 host rehydration is **intentionally narrow**: the genuine R Chosen maintained **Self Guided Regeneration**, with its actual **1 Committed VP**, unchanged effect ID and no fabricated re-cast. The follow-on renderer restores native G3 host objects before initiative and maintains the next source effect serial. It **fails closed** for other ongoing magical effects, unresolved hostile targets, poisoned actors, active G4.3/G4.4 toxin/Endurance, non-Recovery clock markers, unresolved Aim or incomplete G5 actions. Those require their own source-specific phase/continuation bridge; silently dropping them would invalidate a campaign. The original G3/G4 source modules are unchanged.

## Two real native engagements

1. **Soldier gate:** Original `B06-EN-02` opponent in **two paid rounds**. R fires one native G2 Bow arrow with declared natural-1 miss (20→19 arrows), the Soldier makes two normal G5/G4 strikes against A, and the party uses G1 cautious movement plus G5 exits to establish a source-attested **party scene withdrawal**. The Soldier survives; GM must independently assess pursuit or escape outside this map. This is not an automatically safe travel window.
2. **Cold Sentry contact:** The GM fixture declares a 300-second route. Actual G4.2 exploration time/Recovery events resolve and the *same party states* enter a new `B06-EN-01` cold Sentry encounter. The Sentry pays its Reserve; A/B use normal G5 physical strikes; F pays T1 Flame; R may cast genuine Guided only if no existing source-backed host survives. G4 death and G0 Round End, not a fabricated winner, establish the second **sentry defeat** terminal.

A further tested source handoff carries R's live maintained Guided through a third arrival without paying a second commitment, and a separately elapsed six-hour fixture verifies genuine (not reset) Recovery when previously damaged Vigor exists. Existing G8 individual policy outputs, source files, enemy/character definitions and source-digest baselines are untouched.

### Verification

```bash
python -m scripts.b05_b06_native_party_continuity_v0 --level 3 --seed 0 --travel-seconds 300
python -m unittest discover -s tests -p 'test_b05_b06_native_party_continuity_v0.py' -v
python -m unittest discover -s tests -v
```

A focused regression suite checks authentic two-terminals, injury and arrow attrition, exact source/snapshot/ledger digest, VP reservations and a third live host, six-hour clock deadlines, deep-copied prior wound metadata, and **negative** cases for bad source fingerprints, premodified new-state defaults, incomplete terminal, toxin and milestone continuations, unsupported hosts, forged travel and invalid input. Source-provenance CI emits an independently replayable JSON evidence register and runs all repository tests on the exact PR head.

## Scope and unclosed work

This **does not** reconstruct an arbitrary session from JSON, transfer G4.3/G4.4 poison/long toxin suppression, author GM-safe rest, authorize an unsupported maintained spell, prove protection from pursuers, rate the Soldier/Sentry against a continuing party, or include Gifted, Anointed, full Low Priest noncombat selections or an actual L1–3 campaign. It is a precise **B05/B06 source-bound candidate**, with explicit fail-closed outstanding cases. Broader native cross-encounter continuity must add the remaining source-specific duration and hazard interpreters before treating it as universal.

**Unchanged strict MVP status:** 12/12 structurally source-audited Focuses, 0/12 independent full Focus certificates, 0/6 accepted gates, B01–B03 only (3/7) definition-closed, no verified human pilot sessions.
