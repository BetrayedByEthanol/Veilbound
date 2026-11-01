# B04/B05/B06 — Alpha Cohort Source-Legal Mixed-Party Encounter Integration v0

> A **bounded, deterministic source-native L1 Soldier encounter** for the *first* proposed Alpha pilot party (Priest/Low, Scholar/High, Gifted/High, Anointed/Medium). It is **not** actual GM/player play, an interchangeable G8 four-character template, complete Focus certification, a validated Hunter CR, or a new general tactical rules engine.

## The source problem this closes

The first-cohort [pilot package](b04-b05-b06-b07-first-cohort-pilot-execution-evidence-v0.md) had a concrete L1 combat prerequisite. Existing fixed G8 A/B/R/F parties include **physical-only Low Priest proxies** and cannot be relabelled as the four selected Alpha characters. Existing one-character or partial-party Gifted, Anointed, Low Priest and Scholar source engines also cannot independently prove that their costs, response gates and states cooperate in **one native encounter**.

This integration creates **one** complete *source-selected* Low Priest A **or B** actor using `b05_low_priest_life_l1_l3_v0.py` (not the historical `b06_hunter_party_exchanges_v0.py` physical proxy). The original `LowLifeNativeRites` adapter is extended to accept either an **exact** historical physical proxy or this **separately fingerprinted** selected full sheet, preserving all legacy behavior while preventing a different source/Guard/AP/VP identity from claiming the Rite. The full-sheet actor has **no inherited G5 A/B proxy melee profile**: this scenario explicitly selects its legitimate G3 Chosen Rite rather than fabricating sword/mace native attack authority.

The Alpha encounter uses the actual G0-source G/F/AM actor adapters, the existing source-bound High Gifted Emotion/Thrown Flame, the Medium Anointed one-Vessel Investment with **one real recipient G4 Step**, Low Life Chosen Rite G3 host and original G3 High Scholar Fire. The unchanged source `B06-EN-02` Soldier retains its original L3-equivalent benchmark; **no enemy down-level** occurs.

## Authored L1 mixed-source policy and source receipts

A source-fixed 8×7 open-gate grid is used, with an actual predeclared initiative order and four author-declared party border exits. **No hidden teleport or omniscient player AI.**

| Phase | Event | Native source authority |
|---|---|---|
| Round 1 — Anointed | Medium Anointed commits **24 General AP** to invest the consenting, living Priest, choosing that single Vessel | G0 action, exact AM source actor, `MediumAnointedRestoration.invest`; no automatic VP charge |
| Round 1 — Soldier | Original Soldier paid melee hits the adjacent Priest with explicit sourced dice and real G4 damage | G1 adjacency, G5 paid sequence, G4 injury and wound rules; no fabricated confirmed-hit flag |
| Round 1 — Priest's *real* G4 Step | Medium declares the source-legal unopposed pulse **before** the genuinely next Priest Step; recipient has missing HP and remaining Vigor; restores **one HP** with its authored Vigor cost | Exact original `MediumAnointedRestoration.declare_pulse` + recipient G0/G4 Step; **no synthetic Step or independent Reaction** |
| Round 1 — Priest | Full Low Life A/B source pays **30 Projection AP** plus actual Chosen VP commitment; A chooses Guided Regeneration, B chooses Vital Shelter | `LowLifeNativeRites.cast_chosen` exact full-sheet source, G3 maintained host |
| Round 1 — Gifted | Genuine L1 Joy Emotion Window and paid Thrown Flame with explicit d20 natural 1; no fake Instability/Overwhelming reroll or enemy damage | `GiftedNative.establish`, `cast_flame`, original G2/G3/G4 gates |
| Round 1 — Scholar | Genuine source-paid High Scholar L1 Thrown Flame, explicit natural 1, same shared live encounter | `SpellState.cast_flame`, source F actor, actual AP and Spent VP |
| Round 2 | Soldier spends a real G5 natural-1 miss; each living party member performs explicitly sourced cautious G1 route steps and attests their original G5 scene-authored exit | G0/ G1/ G5 and the 4 exit policies, no phantom win, pursued or defeated enemy |

The packet records exact original native ledgers, actor source SHA256 paths, G4 damage/step, G3 hosts, actual AP/VP conservation and completed `party_scene_withdrawal` attestations. It supports two independently source-audited Low Priest starter variants (A/B). **Author policy** is intentionally favorable, staged and reproducible; it is not a CR, win-rate sample or proof a human player would select those actions. Player-selected tactics, Guard/Dodge alternatives, opponent pressure, multiple valid targets, real emotional scene context, consent and real GM timing remain outside this fixed candidate.

## Strict implementation and acceptance limits

- The full Low Priest actor is **not** a fabricated general Low Life melee adapter. An unrecognized A/B sword/mace native G5 attack still fails; a separate source attack adapter is required if the actual player chooses it. No generic G3 Life Rite beyond the one selected Chosen host.
- This v0 establishes **exactly one authored L1 mixed Alpha scene**, not native L2/L3 Alpha encounters, cross-level maintained poison rebinding or a fully integrated three-to-five-session campaign.
- The Medium Anointed supports a consenting, unopposed, positive-HP recipient under actual source range/geometry and a genuine G4 Step. The alternative refused Intrusion remains **unresolved**, not silently forced through.
- Gifted has a legal Joy window and a paid natural-1 miss. Safe/risky Amplification and Instability remain separately authored; this encounter does not invent an Overwhelming miscast.
- Time, recovery and external GM/player choice evidence have not been fabricated. The [first-cohort Alpha packet](b04-b05-b06-b07-first-cohort-pilot-execution-evidence-v0.md) remains **blank and noncertifying** until actual play. CI source reports never populate real sessions or reviewer claims.

## Verify source legality and the finite native terminal

```bash
python -m unittest discover -s tests -p 'test_b04_b05_b06_alpha_mixed_native_v0.py' -v
python -m scripts.b04_b05_b06_alpha_mixed_native_v0 --variant A > build/alpha-l1-selected-priest-a.json
python -m scripts.b04_b05_b06_alpha_mixed_native_v0 --variant B > build/alpha-l1-selected-priest-b.json
python -m unittest discover -s tests -v
```

These tests check the original G0/G1/G2/G3/G4/G5 source prices, both full Priest variants vs the old proxy identity, genuine Medium recipient Step, High Gifted/Scholar paid Flame, old Soldier benchmark, four scene exit certificates and rejection of fabricated identity/attack/terminal data. They also ensure the existing proxy-only Low Life regression remains eligible on its *original exact* source identity.

**MVP baseline remains** 12/12 structural Focuses, **0/12** independently full-play-certified Focuses, **0/6** strict acceptance gates, **0** authentic human play sessions, and original blocker definitions **3/7** closed. This work closes a *bounded L1 integration prerequisite*, not the real-person acceptance requirements.
