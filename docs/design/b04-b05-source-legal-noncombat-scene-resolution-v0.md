# B04/B05 — Source-Legal Noncombat Scene Resolution v0

> **Bounded scripted author-fixture resolution, not human/GM play or Focus certification.** Built on canonical [Core Resolution](../rules/01-core-resolution/core-resolution.md), [Non-Combat Play](../rules/04-non-combat/non-combat-play.md), [Abilities and Training](../rules/02-character-creation/abilities-and-training.md), [GM Adjudication](../rules/14-gm-rules/adjudication.md) and actual G4.2 [WorldClock](../../scripts/b06_world_clock_v0.py). No mechanical rule was added. The user's previously approved restricted L1–3 pilot and two actual GM-declared advancement events remain unchanged.

## Evidence and exact boundaries

| Source-backed delivery | Count and boundary |
|---|---|
| Original structural pairings and levels | **12 Focus pairings × L1–3 = 36 pairing-level slots**; Low Priest A/B are variants of one pairing |
| Explicitly authored core-check scenes | **216 pressure-check forks** = 12 × 3 × **3 domains** × **2 meaningfully different approaches**, each with a native G4.2 exploration-time event receipt and source SHA |
| Exploration | Slippery footbridge **Agility + narrowly relevant Acrobatics** versus route survey **Awareness + Navigation where actually trained** |
| Investigation | Identifying spoiled medicinal herbs **Intellect + Medicine where genuinely trained** versus noticing visible stains **Awareness**, no invented Investigation bonus |
| Social | Request public store log **Presence**, zero universal Persuasion/Negotiation bonus; alternatively cite a factual local precedent **Intellect + regional/era History only if actually learned**, against the *authored neutral storekeeper's stated premise* |
| Low Priest | **18 strictly ability-only pressure forks** using A source G0 physical proxy at L1–3, no invented Learned Discipline or independent full sheet; selecting B is a separately sourced physical *variant*, not an in-character switch |
| Additional canonical modes | Narrow **passive noticing** and **unhurried safe investigation** (safe d20 / Take 10 / Take 20) with explicitly different fictional risk/time, not permission to Take 20 under pressure |
| Acceptance | **0 external player choices, 0 actual GM decisions, 0/12 independent full Focus certificates, 0/6 MVP exit gates** |

Every row resolves a real **canonical** check (when pressure applies: `d20 + actual source Ability + narrowly relevant purchased Training + declared situational modifier` versus `10 + difficulty modifier`). Fixed author-fixture examples choose their own plausible circumstances from the canonical DC ladder: Challenging `12`, Hard `15` or Standard `10`, with a deliberately fixed `d20=12`. This is **not a universal DC for a footbridge, storekeeper or herb sample**. The G4.2 WorldClock advances the explicitly authored **90–240 seconds** for that option; an alternative lives in a **separate fork**, not additional paid actions on one character or a shared quest clock. Fixed text states a plausible immediate success/failure result **only for the mocked GM stance** and changes when the check crosses its threshold.

**No fictitious external GM:** These authored static scene circumstances, die faces, NPC premise and narrative consequences are fixtures for verifying the mechanics. A real GM must determine whether a roll is even necessary, set the actual contextual difficulty and consequences, decide whether the requested social outcome is plausible for that NPC, and witness the player's intended approach. No real NPC disposition is mutated in this code, nor does a fixed fictional result authenticate a social skill contest. It does not resolve opposed social or stealth checks, helping/group actions, extended influence, a generic expedition or investigation progress clock, or unauthored Veil effects. The **noncombat natural-1/20 special effects remain unresolved in canon**, so the code uses numerical totals even on those die faces.

## Safe-time and passive boundary

All **216 matrix forks are pressured actions**. The resolver additionally supports only:

- **Passive incidental noticing**: ordinary Awareness survey of an existing route or staining, `10 + Ability + relevant Training`, no deliberate time or dice.
- **Safe active action**: repeated observation of visible staining in an **unhurried, nonconsequential laboratory**. It permits a normal d20, Take 10 or Take 20; the mock GM defines a 90-second normal effort or a distinct 900-second exhaustive effort. Take 20 is **not guaranteed success**, because the actual check total must still meet the target.
- **Rejections**: a pressured bridge, timed technical diagnosis, or NPC's requested cooperation cannot be relabeled as a safe retry or passive persuasion. No automatic automatic success, guaranteed clue or coerced NPC compliance.

The convenience `--mode` cannot add a nonexistent mechanic. Scene costs are modeled as time on G4.2, **never** AP/VP spent, extra Talent/Discipline access, recovery, GM milestone advancement or time-free extra turns. The G4.2 fixture stays short of any six-hour recovery checkpoint.

## Source, provenance and execution

Each run constructs a **real G0 sourced party actor**, matches its source path/SHA to the already merged [#181–#184 independent roster](../../scripts/b04_b07_twelve_focus_certification_protocol_v0.py), and for eleven pairings derives **actual Abilities and Learned Disciplines** from their authored L1/2/3 `profile()`. The Low Priest A/B G0 proxies provide independently attested **physical Abilities only**; inventing Medicine, Etiquette or a complete Low Priest sheet is prohibited. The same source pairing can legitimately yield different success odds for different approaches without an invented universal Training.

```bash
python -m scripts.b04_b05_noncombat_scene_resolution_v0 --pairing 'Scholar/Medium' --level 2 --domain investigation --policy diagnose
python -m scripts.b04_b05_noncombat_scene_resolution_v0 --pairing 'Gifted/Low' --level 2 --domain exploration --policy survey
python -m scripts.b04_b05_noncombat_scene_resolution_v0 --pairing 'Anointed/Medium' --level 3 --domain social --policy petition
python -m scripts.b04_b05_noncombat_scene_resolution_v0 --pairing 'Priest/Low' --level 2 --domain investigation --policy diagnose --low-variant B
python -m scripts.b04_b05_noncombat_scene_resolution_v0 > build/b04-b05-noncombat-scene-resolution-v0.json
python -m unittest discover -s tests -p 'test_b04_b05_noncombat_scene_resolution_v0.py' -v
```

The output includes the exact source SHA, chosen **trained or untrained** scope, original Ability modifier, canonical target/total, result, the fixture's elapsed world seconds, and SHA-256 of actual source-native G4.2 ledger events. It returns `AUTHORED_GM_FIXTURE_NOT_HUMAN_ADJUDICATION` and **false** full-Focus certification on every row. The full matrix is deliberately **not** a universal PC skill menu: some characters have rank zero in the relevant option; such checks use only their Ability. Source Training is not inherently tied to any fixed Ability, and generic social, perception, investigation, stealth and survival bonuses are never invented.

## Remaining real work

- **C4 noncombat human decision evidence** still requires GM-authenticated choice, alternatives, contextual difficulty, actual repercussions and source-legal utility in the chosen 3–5-session adventure. This PR adds a complete ordinary *core-check* demonstration, not a generic scene/encounter engine or real verified observation.
- **Low Priest C1/C4** still needs a separately reviewed, full source-legal Learned Discipline/utility record; A/B G0 proxies are not full characters.
- **B05 authored noncombat magic** needs explicit per-technique native effects/AP/VP and GM interactions when the selected pilot scene uses them; a mundane diagnosis may not infer spell access. **Scholar live #148 Opportunity** and representative B06 Soldier/Sentry/Hunter encounters remain separate work.
- Real participant/GM session coverage, resource continuity, two distinct **actually GM-declared** level awards, challenge calibration and independent C1–C7 review still determine strict MVP readiness: **12/12 structural, 0/12 independently fully certified, 0/6 exits, B01–B03 closed (3/7)**.

No original G0–G8 bounded milestone or Hunter challenge rating is changed by these scenes.
