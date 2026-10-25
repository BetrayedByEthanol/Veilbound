# B04/B05 — Scholar Three-Focus Tactical Encounter and Resource Attrition Verification v0

> **Status: bounded, deterministic native evidence; no Focus certification or balance tuning.** This work extends previously merged High F Thrown Flame and Medium S/Low T Sword Cut/Inward/Embodiment integration. It reuses original G0/G1/G2/G3/G4/G4.5/G5 mechanics and the unchanged B06-EN-02 Ordinary Human Soldier. No new spell, weapon effect, action, price, recovery tick, target defense or attack damage is introduced.

## What is compared and what is not

All selected L1–3 Scholars begin **two squares** from the same Soldier: Scholar at (2,2), Soldier at (4,2), genuine Scholar-first initiative. The same Soldier, 4 genuine G0 rounds and single predeclared attack-face/damage policy are held fixed. Sources, resource budgets, equipment, access and legal technique preparation **differ** by Focus, and the report preserves rather than erases those differences.

| Source | First-round non-maintained offense | AP and VP | Legal defensive / maintained choices |
|---|---|---|---|
| **High F** | G2/G3 T1 Thrown Flame at 2 squares; no wielded Sword/Guard | Projection 20 AP, 2 Spent VP; attack +5 | Dodge; native standalone **Stone Skin**; no separately authored Guided |
| **Medium S** | G1 one-square advance, paid G5 ordinary Sword Cut hit | Physical 24 AP; 4×Level max VP | Dodge, wielded Sword Guard17, individually learned MS Stone / Guided Inwards (24 Projection AP and genuine Committed VP) |
| **Low T** | G1 one-square advance, paid G5 ordinary Sword Cut hit | Physical 20 AP; 2×Level max VP | Dodge, wielded Sword Guard17, **prepared** LS Stone / Guided Embodiments (30 Projection AP and genuine Committed VP) |

**The selected Low L1 knows but did not prepare Thrown Flame.** A real round-two attempted cast is rejected before AP/VP, while other Focuses face the existing **threatened-casting Opportunity requirement**. The rejected attempt is retained as its own native preflight witness; G2 line previews are not interpreted as paid launches. All current L1–3 profiles remain unable to fund an ordinary Physical plus Projection Action in the same turn. A maintained effect is not a Sword enchantment, extra reaction or second native regeneration step.

## Authored four-round policies

[Executable native runner](../../scripts/b05_scholar_three_focus_tactical_attrition_v0.py) records **48 deterministic scenes**: three levels × all three Focuses × four common policies (**36**) and three levels × Medium/Low × two additional legal policies (**12**). All use **four real G0 rounds**, actual G4 damage and G4.5 bridge, original G0 Step2 once per actor per round, legal G1 one-square approach, and no fabricated extra action.

| Policy | Focus scope | Decision / actual mechanics |
|---|---|---|
| `pressure` | High, Medium, Low | Source opening Flame or ordinary Sword, original Soldier melee Take Hit retaliation, 4 native damage opportunities and real Vigor-limited HP recovery |
| `dodge` | All | Same original Soldier d20 face with **Dodge** declared before G5 roll; no extra attack or invented Dodge value |
| `cover` | All | Physical G2 directional tier-8 partial cover at (3,2); the High ranged Flame is a paid **cover impact** rather than G4 direct damage; S/T close and strike using ordinary melee, not magical projectile cover mechanics |
| `stone` | All | Spend native Projection and **Commit VP** to independent Stone Skin before contact; retain actual protective mitigation/attrition/host receipts, no free Sword effect |
| `guard` | Medium, Low only | Declare genuine Sword Guard17 against the Soldier's same attack. High has a carried Dagger and cannot use this policy |
| `guided` | Medium, Low only | Commit VP with separately paid MS/LS Guided on round one; execute source-native G0 Step2 throughput/recovery, then ordinary Sword on later legal turns |

Fixed inputs: Soldier melee **d20=8, d6=1** against source-declared Take Hit, Dodge or Sword Guard; Scholar Sword **d20=12, d6=4** (Cut, Penetration2); High T1 Flame **d20=12, d8=3**. Wound-location input **d20=8** is supplied wherever native G4 qualifies. These deterministic rolls are authored comparable decision inputs, **not random attack simulations or damage averages**. The Soldier elects **zero self-regeneration allocation**, conserving its Vigor; Scholar regenerates at the existing, source-modified throughput, limited by real missing HP and actual remaining Vigor. The Soldier's real physical attack and target are never substituted with precomputed damage.

Each selected policy uses no more than **two source-legal Sword hits** to preserve one living Soldier through the four-round attrition horizon; unused AP is recorded at genuine turn end. This is a **bounded encounter probe**, not optimized offense or a claim that a player would pass turns under every tactical circumstance. Native Step2 and source effects, not a fabricated global clock, establish timing and recovery.

## Evidence, replay, and source attestation

Each scene retains the complete native event ledger, source SHA256 of both combatants, current SHA256 of the actual build/access/combat implementation files, per-round AP/VP/state receipts, G1 movement, G2 firing lane/cover preview, G3 launch and maintained effect, G4 HP/Vigor/wound, G4.5 verified hit, G5 defense and hit/miss, native Step2 and final positions. The report separates **Paid AP**, **Spent VP**, **Committed VP**, attack launches, hits, effect creation/termination, and actual HP restored. The matrix provides compact per-scene digests without duplicating complete ledgers.

`attest_case` and `attest_matrix` replay the complete source-native policy and reject changed source, altered output claims, skipped receipts or forged ledgers even if an attacker recomputes SHA256 fields. Reports are **normalized to JSON-compatible lists/dictionaries before hashing** so persisted CLI witnesses re-attest unchanged. All source/engine checks run live, without trusting caller-edited metrics or caller-supplied attack profiles.

[18 focused regression tests](../../tests/test_b05_scholar_three_focus_tactical_attrition_v0.py) cover all 48 native case variants; four real rounds and genuine Step2 count; actual Spell VP payment and physical AP; cover impact vs direct damage; no extra Sword damage; Guard/Dodge vs the identical Soldier roll; HP/Vigor conservation; High vs S/T repertoire gates; source-bound Stone/Guided maintenance; true threatened-cast preflight; G4.5 paid hit receipts; report tamper resistance and JSON round trips.

## Limitations and next gates

The fixed Soldier rolls were deliberately chosen to keep the Scholar conscious and the Soldier alive for the four-round window, not to certify survival under an optimized or randomly sampled enemy. Different source-legal attack modes and first-turn actions remain **intentionally unmatched**; do not treat the raw outgoing-damage column as a controlled equal-repertoire balance comparison. No actual Opportunity attack execution on departure, active defended Flame into cover + interposed living bodies, ranged cover ricochet/screen damage, Low L1 alternative prepared repertoire, physical weapon replacement/Equip action, multi-target group tactics, source-backed encounter exit policy, post-fight recovery/rest, environmental hazard, long-run Monte Carlo, terminal victory/defeat, or independent PS/Four-role certificate is established.

**No AP, VP, attack, defense, damage, regeneration or level progression numbers are retuned.** These deterministic scenes are additional native evidence for subsequent multi-foe/mobile tactical policy and eventually separately authorized Focus certification. Structural Archetype×Focus coverage remains **6/12**, independent end-to-end Focus certifications remain **0/12**.

## Reproduction

```bash
python -m scripts.b05_scholar_three_focus_tactical_attrition_v0
python -m scripts.b05_scholar_three_focus_tactical_attrition_v0 --focus High --level 2 --policy cover
python -m scripts.b05_scholar_three_focus_tactical_attrition_v0 --focus Low --level 3 --policy guided
python -m unittest tests.test_b05_scholar_three_focus_tactical_attrition_v0 -v
python -m unittest discover -s tests -v
```

After successful CI, request Codex review. **Do not merge or delete the feature branch automatically.**
