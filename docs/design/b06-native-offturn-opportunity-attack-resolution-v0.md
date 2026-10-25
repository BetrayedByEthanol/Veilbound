# B06 — Native Off-Turn Opportunity Attack Resolution v0

> **Status: bounded native combat executor, not unrestricted universal Reaction or Focus certification.** Connect the existing genuine **G0 Opportunity commitment**, **G1 pre-step movement window**, **G5 source-verified melee roll**, **G4 typed damage / wounds**, and **G4.5 off-turn provenance**. Do not backdate or invent an ordinary Turn AP expenditure for a spontaneous attack.

## Scope and authority

[Native Opportunity resolver](../../scripts/b06_offturn_opportunity_v0.py) is installed through the existing [SourceMelee G5 adapter](../../scripts/b06_soldier_sentry_g5_v0.py), not through an independent side channel. The caller supplies **all choices before movement** using `SourceMelee.opportunity_step(mover, delta, decisions={responder: OpportunityChoice(...) or None})`. Every currently eligible source is accounted for; `None` means an explicit decline, not a phantom attack. The engine computes eligible responders using G1's real threatened **departure** squares, G2 live weapon readiness and existing per-segment Opportunity history. G1 validates the move's footprint, blockers, MP and optional cautious travel exactly as before.

Allowed attack sources for this first bounded G5 delivery: one-square, conscious **B06-EN-02 Soldier Sword (B06-AT-03)**, **B06-EN-01 Sentry Sword (live source-selected B06-AT-01/02, including separately verified Chosen Reserve requirements)**, and real **Medium/Low Scholar ordinary Sword Cut (S/T source-attested)**. The selected **High Scholar F's carried Dagger**, arbitrary A/B party proxy against non-Hunter targets, Hunter Bite/Horn, generic weapon changes, invented spell Opportunity casting, unarmed and Prone weapon feasibility are **not** granted by this adapter. The resolver refuses unsupported sources, wrong/absent ready Sword, spoofed profile, illegal defense, missing wound die, wrong critical dice and incomplete decisions **before G0 response commitment**.

### Genuine one-shot sequence

1. **Preflight:** G5 checks the entire current G1 eligibility set and every selected attack's source profile, actual G2 wielded Sword, legal target, defense (Take Hit, real Sword Guard or Dodge) and authored d20/d6/critical/vigor/wound dice. No AP, Reaction, Guard or movement MP is paid during preflight.
2. **G1 departure:** The source's current G0 turn calls native `g1.step` with a dynamic policy. Eligibility is rechecked after Interceptions; the exact selected `Response(..., "opportunity", ...)` is delivered to native G0, which consumes first Reaction and per-round Opportunity capacity **once per responder** and logs `spontaneous_committed` in initiative order.
3. **Off-turn G5 callback:** Only `Encounter.is_live_spontaneous(trigger, response)` inside G1's actual pre-step response window may roll. G5 authenticates the G1 pending attack and same-trigger G0 `spontaneous_committed` ledger index, recomputes live contact, source and chosen defense, commits the actual defender's Guard or Dodge pressure, and logs the roll, full critical tier, actual hit/miss and response consumption. This **does not** deduct an extra physical AP from the attacker.
4. **G4.5 proof / G4 packet:** A hit passes the exact source action **response index**, G1 pending index and live callback into [WoundContinuation.verified_opportunity_hit](../../scripts/b06_wound_continuation_v0.py). G4 independently preflights and applies original source-typed armor/HP/Vigor effects and wound logic. G4.5 logs `g45_opportunity_attested_hit` before G5 logs `g5_opportunity_resolved`. Both check the response-index ledger for duplicate consumption; a miss records no G4 HP packet.
5. **Movement afterward:** The original G1 movement is rechecked normally. **A living mover continues and pays its actual MP** after the response. If off-turn G4 damage makes the mover Dying/dead, the step fails before payment and leaves its original occupied square. If an earlier Opportunity incapacitated the mover, later **already committed** responses are explicitly cancelled with capacities retained—never converted into attacks against a corpse. G1 marks sources provoked for the same movement segment even when the original movement is interrupted; G0's Reaction/Opportunity refresh remains strictly at the next real Round Begin.

This adapter does **not** allow a caller to attach independently authenticated hit results to an arbitrary old `spontaneous_committed`, alter a response index, choose a different target after the fact, or replay a consumed G0 response into another G4 packet. Original own-turn `G5.declare/resolve` and their separate G0 Physical AP/sequence requirements remain unchanged. Existing G1 callers without the explicit new G5 helper retain their historical **pending/unresolved** semantics: this PR does not implicitly roll dice for them.

## Deterministic native evidence

[Native two-Soldier integration witnesses](../../scripts/b06_offturn_opportunity_witness_v0.py) cover **nine cases** (High F, Medium S and Low T at L1–3), with original character sheets, real first G0 regeneration step, Scholar at (2,2), Soldier alpha at (3,2) and beta at (3,3). The Scholar moves normally to (2,3); both Soldiers genuinely respond: alpha spends Opportunity on a natural-1 miss, beta pays Opportunity and lands one real source G4 Cut hit. The Scholar survives and completes its actual G1 move; no enemy Turn AP was fabricated. Remaining genuine G0 turns close the same round. Original source digests, implementation SHA256, full native ledger, exact G4.5 response receipt, movement MP and actor HP are signed and source-replay attested.

[23 focused regression tests](../../tests/test_b06_offturn_opportunity_v0.py) additionally exercise: two initiative-ordered responders, successful and missed source attacks, Guard and escalating Dodge pressure (including rejection of High's carried, unwielded Dagger Guard), S/T source weapon readiness and rejection of lost Sword, invalid profile/dice preflights with zero capacity leaks, natural-20 devastating wound crossing, defender incapacitation canceling movement and a second committed Opportunity, explicit declines and doubled cautious movement MP, per-segment anti-double-dip, outside-callback replay rejection, cold Sentry normal Sword authority and rejected unauthorized enhanced reserve profile, and JSON evidence tampering.

## Deliberate boundaries and next work

Do **not** confuse one Opportunity hit with unrestricted off-turn G5 attack sequences. **Not implemented here:** exceptional Hunter anatomical Bite/Horn/Pounce triggers and Venom, A/B Hunter-limited physical proxy attacks on arbitrary new targets, Prone special-feasibility adjudication, independent ranged Opportunity magic, interposed Living Screen damage, Interception/Reactive Stone sequencing after a source-specific response, cross-target paired Opportunity choice optimization, every equipment transition and enemy AI, or generic off-turn G5 multi-action combinations. A response without this native helper retains G1's historical pending attack record. The B04/B05 **nine historical unresolved probes** remain valid snapshots of pre-bridge behavior; these new B06 witnesses are independent **completed** evidence, not silent edits of prior claims.

No numerical tuning, new attack profile, extra MP, replenished reaction, extra regeneration or full Focus certification is authorized. Independent Scholar Focus certification remains a separate milestone.

## Reproduce

```bash
python -m unittest tests.test_b06_offturn_opportunity_v0 -v
python -m scripts.b06_offturn_opportunity_witness_v0
python -m unittest discover -s tests -v
```

Require green B05/B06 exact PR-head Actions and Codex review before merge. **Never merge or delete a branch without explicit operator authorization.**
