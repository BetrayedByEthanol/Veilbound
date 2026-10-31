# B06 — Representative Soldier/Sentry/Hunter GM Encounter Packs v0

> **Three playable GM encounter *candidates*, with replayable source-native evidence and explicit untested assumptions.** These are **not** an empirically representative sample, complete campaign, calibrated numerical encounter difficulty/CR, independently played GM sessions or closure of B06. This PR assembles existing trusted native G0–G8 engines rather than creating a new combat or terrain subsystem. Original [encounter frequency vs intrinsic CR vs scenario difficulty](b06-encounter-frequency-challenge-and-hunter-ecology-v0.md) distinctions remain binding.

## Runbook — what the GM needs to declare

Before each scene, record **four actual party characters and source-legal L2/3 sheets**, available VP/Vigor/HP/wounds, carried equipment, spell preparations and source start-state; choose first contact, goals, sight, cover, physical obstacles, escape feasibility, hostile response policy and who decides any discretionary responses. The original native benchmark party for the executable traces is **A Vanguard, B Guardian, R Bow Priest, F Fire Scholar** (A/B are explicitly **physical-only Low Priest proxies**, not complete character certificates). The G7F forest tactical probes may also use three PCs (A/B/R). Source-neutral diplomacy or avoidance means **no mandatory combat**; the supplied policy traces begin only after a GM has chosen to enter hostility. Do not treat predeclared dice or fixed player tactics as representative player choices.

### Pack 1 — Ordinary Soldier: The Road Gate

**Entry and stakes.** One source **B06-EN-02 Ordinary Human Soldier** challenges passage toward the supply trail. Offering proof, negotiating or using the existing noncombat ledger path can resolve the meeting without an automatic hostile encounter; no generic opposed Persuasion check is introduced here. If the GM invokes actual combat, use the source G8 **8×7 open encounter lane** and its source positions. No additional gate crowds, sniper cover, reinforcements or automatic alarm/ambush are authorized by these fixed traces.

**Player choices and existing engine evidence.** Compare **one actual enemy sword + A/B paid melee and F Flame** in G8 `party_victory`; an aggressively concentrated, paid Soldier pursuit/critical policy `party_defeat`; and fully paid *opposed* border exits `opposed_withdrawal`. The defeat case intentionally uses fixed high-critical dice to establish an **extreme reachable** loss, not ordinary likelihood, and the R Priest's G3 Chosen Guided Rite is separately funded. All exits are **G1 cautious movement / genuine G4.5/G5 receipts** and allow no free MP, reaction, teleport or safe post-exit immunity.

**Terrain and counterplay menu for a human GM.** Physical gate barriers, civilians, partial cover, unequal warning, alternative routing, Soldier surrender and assistance are meaningful *suggested fiction*, but any selected one **requires source-rule geometry or a separately authored rule resolution**, not a falsified G8 receipt. The current executable evidence is expressly a **clear source lane** with one enemy. A GM should log actual block coordinates, Guard/Dodge/cover decisions, response window declarations, R ammunition, A/B physical melee and F VP.

**Aftermath prompt.** If the soldier dies, inspect actual party HP/VP/wounds; passage approval or reinforcements are GM decisions, not mechanical rewards. If all PCs die, record the actual deaths, not a TPK based on nonpositive HP alone. If they withdraw, the foe is **still alive** and scene-local exits are not immunity from a later alarm/chase. There is **no automatic six-hour rest or recovery**.

### Pack 2 — Firebound Sentry: Cold Shrine versus Prepared Shrine

**Entry and stakes.** One actual source **B06-EN-01 Firebound Sentry** guarding a shrine walkway. A wary group may observe magical preparedness and choose avoidance or parley; an undecided NPC policy stays a real GM choice. The executable lane is the same source G8 **8×7 open scene**, no automatically active shrine wards or environmental Flame hazards.

**The decisive before-contact choice is real.** Use **`sentry_shrine_cold`** only when the sentry begins from the source `cold_start`. It must pay its real **30 Projection AP and 3 Committed VP** on its first action before a later enhanced attack. Use **`sentry_shrine_prepared`** only when the prepared source start state is genuinely justified before combat; its **3 VP are already Committed**, so never grant an additional preparation AP/VP or free second Reserve. Both source starts can run the three G8 policies (`party_victory`, `party_defeat`, `opposed_withdrawal`) at L2 or L3.

**Pressure and protective alternatives.** The sentry's enhanced sword can carry real HP and direct Vigor harm; this is the distinction worth measuring against party defense, R's Chosen Rite, F fire and withdrawal. GM choices about warded architecture, open doors, anti-magic or special protection must use existing relevant canon and cannot be credited as tested by this open-lane matrix. Compare cold/prepared traces **with the same predeclared source seed** without claiming randomized control or equivalent starting state.

**Aftermath prompt.** Verify exact initial committed VP, final available/committed VP, wounds and real exits from the native receipt before any continuation. A prepared Sentry can remain a living threat after party border departure. The script provides **no victory XP, rest window, latent ward release or observed campaign reward**.

### Pack 3 — Hunter of the Woods: Warned Corridor, Forest Pounce, and Withdrawal

**Entry and stakes.** The source **B06-EN-03 Hunter** is an elite **1×2 natural predator**, not a compulsory fight on every forest contact. A GM should describe tracks, churned ground, prey remains, warning calls and changes in the corridor; letting the party **avoid** it can be a successful noncombat choice without a combat-roll encounter. If it engages, use the source positions/footprint, head-forward contact and genuine rules for Bite/Pounce, wound/Dying and Hunter venom. No invented surprise action, generic free Trip, D&D-style initiative advantage or numeric Hunter CR.

**Three source-native terminal demonstrations at L2 and L3 (P4).** G7-H already authenticates `mixed_victory_rite` (A/B source melee, R Chosen Guided Rite and real Bow, F Flame), `hunter_multitarget_defeat` (paid multi-target lethal pursuit) and `opposed_living_hunter_withdrawal` (real Round-2 chase before **four** G5 border exits with Hunter alive). These branches start from one fixed source roster but have separate authored choices/dice. The pack checks the original attestation and retains actual source HP, wounds, Vigor, VP, ammo and exit receipts; it **does not** grant post-withdrawal safety.

**Variable positioning and response tests, not terminal successes by fiat.** Run the **G7-F** L2/L3, P3/P4 comparison `forest_ordinary` versus `forest_pounce` on the genuine G7-E forest 1×2 opening geometry. At **L3 P4 only**, run the existing `warned_party_exit`, `protected_control`, `reactive_shield`, and `prepared_body` authored source tactics. The forest test can reach a legal *round cutoff* or an unresolved native branch rather than an end; keep every one of those outcomes in the actual observation denominator. Do not convert a cutoff into a win, redraw a defeated party, or omit adverse encounters. A warned/forest case's mere physical environment does not certify generic forest stealth.

**Aftermath prompt.** Real Bite contact, source toxin/wound receipts and G4 regeneration determine what needs intervention. The short G7-F forest probes provide **authenticated aggregate HP changes**, not reconstructed full character wound sheets; do not invent missing final wound/VP detail from those summaries. A surviving Hunter can track or re-engage after an opposed exit. Ask a human GM to establish a defensible safe distance, interrupted/continuing pursuit, any valid venom onset/expiry, secure first aid and whether **actual G4.2 exploration time may be advanced**. Never assert rest, six-hour VP/Vigor recovery or venom expiration merely because a trace ends.

## Source-native execution and evidence denominator

[Native GM pack runner](../../scripts/b06_representative_gm_encounter_packs_v0.py) invokes only the original [G8 Soldier/Sentry source execution and independent replay attestor](../../scripts/b06_g8_soldier_sentry_full_pack_v0.py), [G7-H Hunter terminal attestation](../../scripts/b06_g7h_mixed_encounter_certification_v0.py) and [G7-F tactical source attestation](../../scripts/b06_g7f_representative_calibration_v0.py). It **does not edit** the existing NPC source JSON, player builds, terrain rules, source registries, attack dice, Action Point costs, pursuit rules or G0–G8 machinery.

| Actual source-policy observation | L2 | L3 | Total | Evidence grade |
|---|---:|---:|---:|---|
| Soldier G8, 3 terminal policies | 3 | 3 | **6** | Source-native bounded terminal |
| Sentry cold G8, 3 terminal policies | 3 | 3 | **6** | Source-native bounded terminal |
| Sentry prepared G8, 3 terminal policies | 3 | 3 | **6** | Source-native bounded terminal |
| Hunter G7-H, 3 terminal policies | 3 | 3 | **6** | Source-native bounded terminal |
| Hunter G7-F forest ordinary/pounce, P3+P4 | 4 | 4 | **8** | Short-window tactical, censored/unresolved when no real terminal |
| Hunter G7-F warned/protection, P4 | 0 | 4 | **4** | Short-window tactical, censored/unresolved when no real terminal |
| **Total** | **16** | **20** | **36** | **Not 36 independent GM sessions** |

The runner preserves a **36-observation denominator**, source IDs, predeclared seed, original canonical ledger SHA-256, per-scenario policy and any genuine terminal/cutoff. For full native G8/G7-H traces it records actual actor final **HP, Vigor, available/committed VP, ammo, wounds, Dying/death** and exit receipts. G7-F tactical cases expose **only** their original independently attested aggregate HP changes, Pounce/protective witnesses and cutoff/terminal evidence. Do not pool those final states into invented HP measurements. There is **no empirical win rate, confidence interval, numeric encounter CR, encounter frequency roll, treatment effect, AI model or representative difficulty threshold**.

A deterministic L2 P4 G8 victory and a deliberately scripted L3 P4 Hunter lethal loss can both be true without meaning a typical group has 50% win probability. Seed labels are not an independent distribution of human choices; G8 defeat intentionally uses fixed high-critical attacks, and G7-H policies are individually selected fixed source paths.

## Commands / pilot execution

```bash
python -m scripts.b06_representative_gm_encounter_packs_v0 --gm-pack soldier_gate --level 2 --policy opposed_withdrawal
python -m scripts.b06_representative_gm_encounter_packs_v0 --gm-pack sentry_shrine_cold --level 3 --policy party_victory
python -m scripts.b06_representative_gm_encounter_packs_v0 --gm-pack sentry_shrine_prepared --level 3 --policy party_defeat
python -m scripts.b06_representative_gm_encounter_packs_v0 --gm-pack hunter_forest --level 2 --policy mixed_victory_rite
python -m scripts.b06_representative_gm_encounter_packs_v0 --gm-pack hunter_forest --level 3 --party-size 3 --policy forest_pounce
python -m scripts.b06_representative_gm_encounter_packs_v0 --gm-pack hunter_forest --level 3 --policy reactive_shield
python -m scripts.b06_representative_gm_encounter_packs_v0 > build/b06-representative-gm-encounter-packs-v0.json
python -m unittest discover -s tests -p 'test_b06_representative_gm_encounter_packs_v0.py' -v
```

For an **actual pilot**, record for each encounter: players/GM and consent, actual original source character snapshots, chosen enemy preparation, entry distance/map, initial VP/HP/Vigor/wounds, warnings, dice and declarations, legal responses, actual attack/movement/VP/HP event IDs, first outcome, the status of each party member, venom onset risk, retreat pursuit resolution, noncombat continuations, elapsed world time, treatment/recovery and independently witnessed decisions. **Source-native fixed-policy successes remain machine proofs only**, and a *representative GM pack* cannot be accepted without independent real sessions and varied tactics.

## Gates deliberately left open

**B06** is still open: Source terminal/path coverage is not independently tested representative Soldier/Sentry/Hunter difficulty, mixed-party role balance, full 3–5-session adventure pacing, multi-encounter resource continuity or calibrated Hunter challenge. Soldier/Sentry generic bow output, non-open gate geometry, dynamic terrain/cover and protection outside currently authored scenes, P3 Hunter full terminals, and post-withdrawal long-time safety are not supplied by this PR. No new B06 G9 or arbitrary universal policy engine is required. The [MVP acceptance register](b04-b07-mvp-acceptance-register-refresh-v0.md) remains at **12/12 structural Focus builds, 0/12 independently fully certified, 0/6 strict exit gates and 3/7 original closed blocker definitions**.

**Concrete next handoff:** Connect the [three-scene noncombat supply-cache segment](b05-b06-integrated-noncombat-adventure-scenes-consequences-v0.md) with these three encounter briefs and **actual GM-declared choices** into one 3–5-session pilot adventure, then run a real tabletop test and independently review C1–C7. Two **actual, distinct, GM-declared L2 and L3 group-story milestones** remain required; the combat runner cannot award them.
