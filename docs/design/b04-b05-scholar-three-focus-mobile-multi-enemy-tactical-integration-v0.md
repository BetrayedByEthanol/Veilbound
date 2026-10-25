# B04/B05 — Scholar Three-Focus Mobile and Multi-Enemy Tactical Integration v0

> **Bounded source-native integration, not independent Focus certification.** Implemented through the original G0/G1/G2/G3/G4/G4.5/G5 execution and unchanged selected High F, Medium S and Low T Scholar character sheets. Two real **B06-EN-02 Soldiers** are separate actors, each with its own initiative, position, movement budget, G5 action, source digest and G4 HP. No new spell, speed, damage, action cost, combat role or encounter difficulty is created.

## Native encounter matrix

[The executable native runner](../../scripts/b05_scholar_three_focus_mobile_multi_enemy_v0.py) and [18 focused regression tests](../../tests/test_b05_scholar_three_focus_mobile_multi_enemy_v0.py) define **36 L1–3 three-Focus cases**:

| Policy | Count | Authored source boundary |
|---|---:|---|
| `pursuit` | 9 | Three completed rounds with two separately moving and paid attacking Soldiers; Scholar's legal Flame or ordinary Sword attacks, real target choice and G0 Step2 |
| `cover_shift` | 9 | Identical characters, opposing choices and true map positions with a fixed directional tier-8 cover surface at (2,3). High's second Flame genuinely strikes the cover while its other two have clear lanes after movement; Medium/Low ordinary melee remains unchanged |
| `stone_weave` | 9 | Original individually paid High/Medium/Low Stone Skin on round one, followed by two later source-legal physical Sword (S/T) or projected Flame (F) actions on genuine turns and two-enemy retaliation |
| `opportunity_probe` | 9 | Genuine two-Soldier G1 departure and **two G0-committed Opportunity responses**. The source engine reports each G5 attack **unresolved**; case stops with a recorded G4.5 blocker instead of falsely asserting damage or complete rounds |

**27 cases have fully completed, three-round G0 turns**, with three independently paid turn actions for each Soldier. The **nine additional Opportunity cases are intentionally incomplete** because current G1 records `g1_movement_opportunity_pending` while ordinary native G5 requires the attacker to own the current turn. G0 Opportunity commitment does *not* give that pending attack a valid off-turn G5 attack roll or G4 HP packet. No fabricated "hit" is added. Completing off-turn Opportunity delivery is a separate combat-engine integration prerequisite for full certification.

### Geometry and opposed tactics

The completed policies begin with Scholar at (2,2), Soldier alpha at (4,2) and Soldier beta at (4,4), all one-square native bodies. Scholar wins explicit initiative; alpha and beta have different later initiative scores. In each completed scene:

- **High F** casts one real T1 Thrown Flame at alpha from its original two-square opening. The Soldiers then advance separately to threaten its square. High uses **native cautious paid MP** to reposition on rounds two and three, first to (1,3), then to (0,3), recovering a legal physical G2 firing lane to beta. The tier-8 cover at (2,3) intercepts the second shot in `cover_shift`, but the third lane no longer crosses that cover. **All VP and Projection AP are paid;** a G2 preview alone never deals Fire damage.
- **Medium S and Low T** advance by one legal G1 square to (3,2), attack alpha with the real sourced **Sword Cut** profile, then select beta and alpha on later turns. When Stone is cast first, alpha **must pay a genuine first-round G1 approach from (4,2) to (3,2)** before it can attack the unmoved Scholar; the Scholars then switch to source-paid Sword attacks on later turns, targeting alpha then beta. Their G5 actions retain their real Focus AP prices, Strength/Agility/Training, actual one-handed Sword, Penetration 2, and canonical G4 damage.
- **Both enemy Soldiers** independently follow physical one-square/diagonal G1 movement into melee contact. Each pays its own G0/G5 Sword slot on each native turn (six enemy attacks per completed scene). Explicit enemy face policy is alpha (1,12,1) and beta (12,1,12), with damage d6=1 for non-natural-1 hits. These are **chosen deterministic inputs**, not randomized difficulty calibration or authored intelligence. Native G4/Step2 resolves attrition and natural recovery. Cautious movement explicitly declines eligible Opportunity responses in completed scenes: no incomplete attack is disguised as a completed encounter.

### Actual Opportunity-response boundary

For each Focus/level, the separate `opportunity_probe` begins with Scholar at (2,2), alpha at (3,2) and beta at (3,3). On the Scholar's real G0 turn, it attempts **ordinary (non-cautious) movement** to (2,3). G1 computes both eligible departures and calls its **post-Interception dynamic selection**. The policy commits both source Soldier `Response(..., "opportunity", ...)` entries in initiative order; it genuinely spends both first Reaction/Opportunity capacities and logs both pending off-turn G5 deliveries. The Scholar's native movement/MP still occurs. The case then records an explicit `unresolved_response` blocker with the exact missing G5 authority.

This probes response *eligibility, window timing, budget, provenance and pending delivery*. **It cannot certify Opportunity damage, HP loss, wound continuation, two complete enemy attack turns, or a terminal outcome**. No hidden `decline_all`, invisible attack resolution, free Reaction refresh or synthetic off-turn sequence is silently added.

## Evidence and replay controls

Each full case retains complete G0–G5 native ledger, movement/MP receipts, independently logged Soldier attacks, attack misses and real G4 hit packets, source-selected ordered targets, actual G2 lane preview, source-paid Stone or Flame AP/VP, genuine per-turn regeneration, current combatant positions and HP/Vigor, and the original source SHA256 for the actual build and executor files. The probes separately retain both `spontaneous_committed`, both `g1_movement_opportunity_pending` and exactly one `g45_unresolved_stop` classification.

`attest_case` and `attest_matrix` replay the complete original native policy and reject modified saved reports even if all unkeyed digests are recomputed. The JSON is normalized before signing, and the compact matrix carries source-basis and exact per-case digests without duplicating all 36 full ledgers.

## Explicitly unresolved

This PR does **not** authorize G5 off-turn Opportunity hit resolution, Interception/OA damage against a moving Scholar, spontaneous Guard/Dodge defenses against such attacks, multiple enemy types, live living-screen collision damage, arbitrary ranged cover geometry, random encounter balance, weapon swaps, low-L1 unprepared outward casting, new Inward/Embodiment effects, independent Focus/adventure certificates, mixed-party roles, or numerical tuning. It is a deliberately small real **multi-actor mobile foundation**. Full tactical certification requires source-authorized off-turn attack delivery and broader policy evidence, not one of these deterministic winning/movement scripts.

## Reproduce

```bash
python -m scripts.b05_scholar_three_focus_mobile_multi_enemy_v0
python -m scripts.b05_scholar_three_focus_mobile_multi_enemy_v0 --focus High --level 2 --policy cover_shift
python -m scripts.b05_scholar_three_focus_mobile_multi_enemy_v0 --focus Low --level 1 --policy opportunity_probe
python -m unittest tests.test_b05_scholar_three_focus_mobile_multi_enemy_v0 -v
python -m unittest discover -s tests -v
```

Codex review and exact PR-head CI required. **Do not automatically merge or delete the branch.**
