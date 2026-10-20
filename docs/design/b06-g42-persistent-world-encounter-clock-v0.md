# B06 G4.2 — Persistent World/Encounter Clock v0

> **Bounded chronological infrastructure, not G4 toxin resolution, global physical combat-time law, or encounter certification.** Implements the clock slice defined in [G4 remaining-dependencies audit](b06-g4-remaining-dependencies-and-completion-audit-v0.md). Canonical timing authority: [Initiative and Round/Turn Procedure](../rules/05-combat/initiative-and-round-structure.md), [Mundane Toxins](../rules/05-combat/mundane-toxins-v0.md#3-ticks-timekeeping-and-healing), [HP and Vigor](../rules/06-vigor-wounds-death/hp-and-vigor.md#vigor-recovery), [Volition Points](../rules/07-veil-magic/volition-points.md#recovery), and [Hunter's long-milestone mapping](../rules/05-combat/hunter-bite-venom-and-horn-v0.md#long-clock-and-exploration--initiative-transitions).

## Scope and contract

The optional [G4 `WorldClock`](../../scripts/b06_world_clock_v0.py) is installed with [`DamageState`](../../scripts/b06_damage_v0.py) and observes [G0 genuine Round Begin](../../scripts/b06_encounter_state_v0.py); it never invokes `start_turn`, `Regeneration Step`, HP healing, Dying survival, AP/MP, Guard, Reaction or a fabricated Step 3. Existing encounters without explicit mode changes remain compatible with the original bounded G4 `advance_exploration` API.

| Surface | G4.2 executable contract |
|---|---|
| **Exploration** | One actual monotonically increasing `world_seconds` counter. `advance_exploration(Δt)` consumes events in source-time order, breaking at **each real milestone, short toxin interval and independent Recovery checkpoint** rather than paying all toxin packets first and Recovery last. Zero elapsed seconds never manufactures recovery. |
| **Recovery entitlement** | A separate pending **6-hour checkpoint per actor**, existing even without toxin exposure, with stable `recovery:<actor>:<number>` IDs, recorded consumed markers and source digest. Each awards source-derived **25% half-up** Vigor (capped by Max) and Spent VP only, preserving Committed VP. At full resources it still consumes the checkpoint with zero restoration. Exactly one next checkpoint follows each consumed live-actor checkpoint; neither mode switch nor poison application resets the cadence. |
| **Pre-scene phase** | `DamageState(encounter, recovery_phase_seconds={actor_id:seconds_until_next})` accepts independently attested per-recipient remaining **1…21,600 seconds**. Omitted actors default to 21,600 from the bounded scene start; this is a model default, **not** a claim that arbitrary in-world characters began their cadence just now. Explicit partial phases prevent a newly inserted encounter from resetting genuine preexisting Recovery. |
| **External milestone** | `clock.schedule_milestone(actor_id,event_id,source,delay_seconds,phase)` creates a uniquely keyed, source-bound **marker only**. It logs `g42_milestone_due` once and retains consumed/canceled identity; it does **not** apply Hunter weakness, toxin damage, cure, Venom Endurance, or a generic effect. `cancel_milestone` requires the same source. Effect dispatch remains G4.3–G4.4 work. |
| **Initiative entry** | `clock.enter_initiative()` at a legal round boundary maps **each** exploration remaining time `s` independently to `R+floor(s/6)`. `q=0` resolves at the entry transition **before any actions**, not at a virtual turn. Saved preconversion deadline orders coalesced milestones (e.g. 37s, 39s, 41s all at R+6). |
| **Initiative Round Begin** | G0 `begin_round()` invokes `clock.on_round_begin` once, *after* the native resource refresh/G3 Round Begin processing. Only due registered long milestone markers or genuine Recovery checkpoints execute. No global six-second physical duration is claimed for a combat round. A **new milestone authored during initiative** requires a positive whole-six-second **source-specific surrogate** duration, preventing arbitrary subround rounding guesses. |
| **Initiative exit** | `clock.leave_initiative()` at a legal round boundary maps each pending Round Begin E from exit round C to **`6×max(0,E−C−1)` exploration seconds**. A zero conversion fires at transition. Previously consumed event identities remain consumed; independent pending Recovery survives all mode changes. |
| **Short toxin phase** | Existing TX-HM Full five / Reduced three packets continue through *real target Step 3* or **six actual exploration seconds per local interval**. Fractional `phase` is preserved through initiative entry and exit. A genuine turn contributes **one** local toxin interval without crediting elapsed world seconds; exploration contributes actual seconds with **no virtual Step 2**. |
| **Stable same-boundary order** | Sort by mapped due boundary, **original independent source-time order**, declared tie phase (`before_recovery`, actual `recovery`, `after_recovery`) and registration serial. The phase field names explicit marker-vs-Recovery order at genuine ties. Do not use these generic markers to invent toxin effect semantics: G4.3 must separately account for actual canonical TX-HE Recovery-before-expiry precedence and other effect-specific rules. |

### Event provenance and limitations

Every queued event records stable ID, recipient, actor source ID and digest, source, phase, original order, local due representation, and consumed/canceled status. The ledger also records recovered Vigor/Spent VP, real transition labels and actual marker resolutions. **`world_seconds` counts exploration elapsed seconds only**; initiative uses conservative Round Begin labels and makes no assertion of physical seconds. At mode changes, the due representation is converted conservatively and can shorten the remaining delay. Repeated transitions never legitimately duplicate events or grow a toxin deadline.

No automatic external-world persistence across different `Encounter` instances exists yet: a later encounter must import its honestly sourced remaining Recovery phase rather than silently infer it from another scene's stopped timeline. The G4.2 event ledger can be exported by a subsequent integration slice; reconstructing arbitrary independently sourced active toxin instances is **not implemented**. A long-time operation crossing a meaningful damage/choice milestone must stop for GM input in the eventual action/condition interpreter; marker-only G4.2 does **not** claim to auto-play those decisions.

### Deterministic checks

[`test_b06_world_clock_v0.py`](../../tests/test_b06_world_clock_v0.py) proves G4.2 chronology: exact 6h−1 / +1, independent phases, marker/recovery interleaving, five 5-second exploration advances with zero-time mode switches, 5s exploration → genuine Step2/Step3 → 1s exploration, q=0 and q=6 mapping, coalesced preconversion order, E−C−1 exit, preexisting Recovery consumed once across multiple modes, new initiative-surrogate validation, cancellation and source identity, illegal transitions, full-pool checkpoint, and absence of virtual HP regeneration/Dying.

Run:

```sh
python -m unittest discover -s tests -p 'test_b06_world_clock_v0.py' -v
python -m unittest discover -s tests -v
```

Existing G4 regression tests remain the authority for already implemented direct HP/Vigor, wound location, Basic Heal, native toxin Step 3 and six-hour recovery. The historical 4,096 Phase 3 one-round census remains unchanged.

## Next G4 slice

**G4.3 — Unified Mundane Toxin Application/Effects v0**: wire genuine delivery → printed-grade nonstack → eligible preventive Ward → single natural save → one accepted instance; bind canonical short and long toxin consequences to the G4.2 source-owned milestone/real-turn clocks. **G4.4 Hunter Venom/Venom Endurance** then implements exact T+10/30/60/120 milestone changes with suppression and injection gates. Neither is silently included in this infrastructural PR.
