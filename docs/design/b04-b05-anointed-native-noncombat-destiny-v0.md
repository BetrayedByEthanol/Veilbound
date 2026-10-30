# B04/B05 — Native Anointed Noncombat Destiny and Mission Story Beats v0

> **Bounded genuine WorldClock + GM-adjudication integration, not certified noncombat Focus play.** Merged #176 put ordinary G5 offense and Returning Step in one authentic two-round encounter; #171–175 established source-backed Signature/Authority with finite shared Destiny. This slice connects those existing **L1–3 High/Medium/Low Restoration** source states to the existing G4.2 **WorldClock** exploration chronology, while leaving actual GM recognition of significant Mission events strictly external. No quest is automatically “complete,” and fulfilling a story beat never ends the Anointed's continuing Mission.

## Authoritative sources and boundary

The [noncombat native bridge](../../scripts/b05_anointed_native_destiny_exploration_v0.py) attaches to an existing High/Medium/Low Anointed native state and **the encounter's already-constructed G4.2 WorldClock**. It does not advance physical time itself, create a G0 turn, duplicate a G4 Regeneration Step, or mint Destiny from a combat-round label. It verifies the AH/AM/AL exact source sheet path, SHA256, Focus, level and current Restoration bond before binding. One bridge per encounter owns the source Destiny accounting.

**Six-hour recovery:** `sync_world_time()` reads only actual `clock.world_seconds` already advanced by `clock.advance_exploration(seconds)` at a valid complete-round exploration boundary. The source `recover_destiny(..., elapsed_minutes)` retains partial minutes toward a **completed 360-minute active-bond interval** and caps the shared Destiny pool at **2**. The bridge additionally tracks subminute seconds rather than fabricating minute credits. **Dormant bond time earns no Destiny**, but already-earned active progress is retained. The same actual clock still separately owns standard G4.2 six-hour **Vigor/Spent VP** Recovery; those recovery receipts neither grant nor imply a second Destiny reward.

**Significant Mission story beat:** `record_mission_event(event_id, gm_recognized=True)` delegates to the existing `mission_event` rule, credits up to **+1 Destiny** within the existing cap and consumes the event ID exactly once, even if at cap. An absent/false GM verdict never generates an award, and identical GM-recognized event IDs cannot be farmed. The source verdict is an **explicit external GM adjudication**, not a system-authenticated GM identity, automatically recognized quest completion, mandatory birth tragedy, morality score, rigid list of mission milestones, or final victory over a never-ending Mission. The illustrative story beat `gm:restoration:healed_village` means a **GM may recognize curing a village as a meaningful event**; the mere label never establishes that it occurred.

**GM bond verdict:** An explicitly acknowledged external `active=False/True` verdict delegates to the canonical `set_bond` source rule and blocks recovery during dormancy. It does not automatically judge behavior, reactivate Low Embodiment, restore Investment, award a story event or grant new Authority. Elapsed real active-world time is reconciled **before** either GM award or bond-state change, so award order cannot retroactively rewrite the preceding six-hour clock.

## Native 72-case proof

[Source-native test runner](../../scripts/b05_anointed_native_noncombat_destiny_v0.py) uses **72 deterministic policies = three Focuses × L1/2/3 × ordinary Soldier or prepared Sentry × four noncombat policies**. Every case starts with one genuinely paid **Lesser Returning Step** after an actual Soldier/Sentry G5 hit and finishes **two G0 rounds** with the real recipient G4 Step and **Destiny 2→1**. It then leaves actual G4.2 initiative at a completed round boundary; the only subsequent clock is real exploration, never a ghost Regeneration Step.

| Policy | Authored outcome |
|---|---|
| `clock_partial` | **359 minutes** of actual exploration yield 0 Destiny (remainder 359); the next **60 seconds** complete six hours and restore **+1**, capping the pool at 2. |
| `gm_recognized` | One **external GM-recognized** significant story beat awards +1, replay of the same event is refused, and an additional actual six hours add **0** because the pool is full. |
| `gm_unrecognized` | GM recognition is absent: no event award; subsequent real six-hour recovery, not a quest label, earns the one Destiny. |
| `dormant_pause` | Explicit GM verdict puts the bond dormant; the next real six hours earn **0** Destiny. After separate reactivation and another active six hours, exactly **+1** is restored. Low's unmanifested Embodiment remains off after reactivation. |

The [ten focused tests](../../tests/test_b05_anointed_native_noncombat_destiny_v0.py) verify all 72 source-backed outcomes; genuine G0/G4/G5 Lesser payment and one source enemy hit; real G4.2 enter/leave initiative markers and world recovery; no extra Regeneration Steps; partial-clock precision and capped awards; distinct Mission versus time receipts; external-GM refusal, unique-ID replay denial, dormant-bond interruption and Low Embodiment; source digests and exact deterministic ledger replays that reject even rehashed forged receipts.

The native witnesses deliberately use the existing **unopposed** beneficial Restoration path and fixed enemy `take_hit` policy. They do not resolve contested +8 Intrusion, a full player-directed journey, calendar travel logistics, social influence, actual GM identity authentication, party-wide Missions, variable moral judgements, noncombat encounter skill checks, or an externally certified GM play session. The G4.2 combat Round Begin surrogate is **not assumed to be physical six-hour elapsed time** for Destiny, and no free regeneration is invented.

## Readiness, limits, and next gate

This extends actual L1–3 Anointed *noncombat* accounting but **is not certified** independent Focus-role versatility or B07 Mission roleplay. The MVP census is still **12/12 structural**, **0/12 independently certified complete Focuses**, **0/6 strict MVP exits**; B04–B07 remain open and B06 **G0–G8** remains fixed. The next meaningful gate is a genuinely varied combat/noncombat pilot with GM recognition/consent and audited player decision policies, not additional synthetic Focus certificates. No new Destiny rule, GM milestone catalogue, or requirement for an emotionally tragic origin is added.
