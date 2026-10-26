# B04/B05 — High Gifted L1–3 Native Encounter Integration v0

> **Bounded native combat evidence, not independent High Gifted Focus certification.** Follows merged #151 (Amplification/Genuine Miscasts) and #152 (source-backed L1–3 structural build). Uses existing B06 **G0–G5**, not an additional G9 milestone. No new technique, naturally Overwhelming trigger, Reactive Thrown Flame, free Reaction or AP exception is introduced.

## Exact source and delivery

- `gifted_actor(level, ...)` projects the unchanged **High Gifted eight-link pilot** from `scripts/b05_high_gifted_l1_l3_v0.py` to a real G0 `Actor`, with digest-pinned source identity `G`, armor/wielded dagger, AP/VP/HP/Vigor, Guard, and L1–3 progression. The attacker source cannot be replaced by Scholar `F`.
- The `GiftedNative` adapter is installed on a genuine G3 `SpellState` alongside G1 `GridMovement`, G2 `RangedCombat` and G4 `DamageState`. It requires a ready G0 actor turn and a single **Emotion Establishment Step** each time that actor receives new turn resources.
- A real `turn_resources` ledger index identifies the **Emotion Window**. Attempts to establish twice in the same window, establish after a paid action, reuse a stale window on a later turn or cast with non-Joy Active Emotion are rejected. Natural Heightening requires an explicitly asserted fictional rationale; **Evoked** grants no safe Step.
- Only `Conjure Flame / Thrown Projectile / Primary` has the authorized High Gifted options **Potency**, **Reach** and **Precision**. The profile is explicitly tagged `[Projection]`; buying one extra Step by **Surge** spends `ceil((2×Used Tier)/4)` extra **Spent VP**, once per Emotion Window. The safe Step and Surge allowance are consumed independently, not refreshed per cast/attack.
- G2 supplies the real path, wall/corner, cover and screen geometry. **Reach** raises maximum direct delivery from 3 to 4 squares without changing minimum 1 square. No Range Band borrowed from a Bow is used.
- The original G2 shield/Guard/Dodge/Take Hit decision and pressure are committed as normal. **Precision** adds +1 to the single authored Flame attack roll. **Potency** rolls the original eligible d8 twice and uses the higher *before* the existing `2+ceil(d8×Tier/3)` Vigor packet. Fixed 2 Fire HP is unchanged.
- The cast pays **20 Turn AP**, then its base and Surge Spent VP through native G0 transitions, emits a `g3_flame_launched` source-digest/Emotion-Window/Amp receipt and immediately consumes confirmed hits through **G4.apply_flame**, including real HP/Vigor mitigation and wound preflight. Explicit natural-20 confirmation and required critical dice are mandatory for completed native resolution.
- The adapter does not accept a post-commit callback; threatened casting requiring Opportunity response, interposed living screens and unsupported live reactions remain **rejected**, not silently resolved. Existing Scholar Flame remains separately source-authorized.

## Bounded verification scenarios

`tests/test_b05_high_gifted_native_encounter_v0.py` checks:
- Source-legal **L1/L2/L3** normal direct Flame hits, paid AP/VP, source ID, G3 launch and exactly one genuine G4 damaging event each.
- Real range-four G2 lane with naturally Heightened safe Reach and paid Surge Precision, plus Evoked Surge without a Heightened Step.
- Potency's d8 selection and source damage scaling; L3's two ordinary Projection Actions sharing one Surge and one safe Step.
- G2 aware Dodge pressure, failed unqualified Dodge, source Soldier G1 contact and **G5** retaliation.
- Early no-cost refusal of wrong emotion, missing/emotionally unjustified Heightening, stale/duplicate windows, unprepared tier, illegal options or dice, missing Reach, insufficient AP/VP, tampered source and changed wielded equipment.

**Unresolved deliberately:** the currently approved L1–3 rules do not provide a lawful same-turn **Overload 24 AP + normal Flame 20 AP = 44 AP** (maximum Turn AP 42). The isolated zero-AP test fixture does not authorize Reactive Thrown Flame. Consequently this PR **does not** claim a lawful native risky Step or miscast witness, broaden to all eight technique catalogues, assert off-turn magic, or invent severe-failure delivery. Those require separately approved source mechanics.

## Acceptance accounting

This refines B04/B05 High Gifted within existing B06 G0–G5; High Gifted remains **one structural pairing plus bounded native evidence**, not an independent certified Focus. Structural **7/12**, certified **0/12**, strict MVP gates **0/6**, blocker definitions **3/7** and representative encounter packs **0** remain unchanged. The original G0–G8 taxonomy, signed historical denominators and Hunter CR status remain unchanged.

Verification commands:
```sh
python -m unittest tests.test_b05_high_gifted_native_encounter_v0 -v
python -m unittest discover -s tests -v
```
