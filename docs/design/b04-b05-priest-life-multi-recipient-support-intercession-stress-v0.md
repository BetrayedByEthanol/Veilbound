# B04/B05 — Priest Life Multi-Recipient Support and Intercession Stress v0

**Scope:** deterministic, source-native **four-character, four-round** Life support encounters using real H/M/A/B Priest builds, independently vulnerable F High Scholar and R Bow Vanguard allies, and one original Soldier or prepared Sentry. This is an *evidence gate*, not Focus ranking, win-rate sampling, or permission to tune numerical rules. No engine rule or original Phase 3 census changes.

## Authored scene and target pressure

- Priest (H, M, Low A or Low B) at **(2,1)**, F at **(2,2)**, R at **(3,3)**, and native Soldier **B06-EN-02** or prepared Firebound Sentry **B06-EN-01** at **(3,2)**. The foe is in verified G1 melee contact with **all three** independent party recipients, including the Priest; all actual Life targets must be in an unobstructed three-square magic range.
- Deterministic initiative **priest 40 > foe 30 > F 20 > R 10**. Two explicit enemy target policies: **alternating** F,R,F,R and **rotating** F,R,Priest,F. Source G5 native paid single-sword profile **B06-AT-03** / **B06-AT-02**, attack d20 **12**, Take Hit, declared pre-roll damage d6 **1** or **4** and Sentry Fire/Vigor die **4**. Genuine G4 applies source armor, typed packets and wounds; native G0 runs one actual Step 2 for each actor per round. A previously dead scheduled target is reported unavailable, **not silently retargeted** for optimal results.
- Each real Step 2 allocates up to currently available HP deficit, Vigor and ordinary/Guided throughput, including Dying-survival cancellation if supported. There is no extra regen packet, free direct HP restoration, off-turn Priest action or automatic restoration of Spent VP.
- There are **408 source-replay-checked cells** from L1/2/3, two enemies, two target patterns, two die-face pressures and each level-legal Focus policy. Source VP pools, original equipment and single-hand access, Priest AP cost, G4 actual damage and all G3 effect budgets remain untouched. No probabilities or outcome weights.

## Authored Life choices

| Role | Implemented policies | Source constraint / tactical meaning |
|---|---|---|
| **H High** | no magic; prepared Guided on F; prepared Shelter on F; dynamic Basic Heal triage; L3 dual prepared Guided on F + Shelter on R | 20 AP/Projection; L3 can fund two 20-AP casts in one 42-AP turn. Guided/Shelter are distinct maintained casts (not an invented stacked identical spell). Each actual Basic Heal costs 2 Spent VP and one legal Projection, with verified free hand, range and delivery |
| **M Medium** | no magic; Guided on F; Guided reassignment F→R; L3 Guided Intercession on R; Shelter on F; Shelter reassignment F→R; L3 Vital Intercession on R; dynamic paid Basic Heal triage | Exactly one original Consecration host; reassignment on R2 is a native 24-AP General Action, preserves existing host/budget/Committed VP. L3 Intercession costs **2 Spent VP and one true Reaction** after the eligible *other* recipient's Step-2 or Sentry's actually applying Direct Vigor packet. Consecration target and Reaction beneficiary cannot be the same |
| **A Low Guided** | no magic; self Chosen Guided; actual A Basic Heal external triage; L2–3 self Chosen plus paid external Basic Heal when independently affordable | Chosen Rite is **self-only**, 30 AP and 1 Committed VP. Actual free-hand A Basic Heal via the existing source-authorized G4 entry point costs 30 AP/2 Spent VP; at L1 2 Max VP cannot simultaneously reserve a chosen host and fund a 2-Spent Heal |
| **B Low Shelter** | no magic; self Chosen Shelter; L3 optional Vital Interposition on Priest's genuine subsequent HP loss | B's verified **mace and shield occupy both hands**; no authorized free-hand transition, so external Basic Heal is **not executed** and fabricated external Chosen Shelter is forbidden. L3 Exaltation is legal only with live self-host, remaining B8 and 1 Spent VP per eligible arming; it never protects F/R |

Dynamic triage after round 1 uses **only previously injured living F/R recipients**, prioritizing greatest current missing HP and then missing Vigor with stable F-before-R tie-break. Each real cast requires the appropriate available VP and actual G1 clear-line recipient. Thus H/M/A may heal after source harm; no synthetic packet is inserted before foes act. An eligible turn lacking funds skips casting without inventing an AP charge or VP. Preparations (High standard, Medium source default) are fixed before Round Begin.

Medium Guided Intercession is eligible only at R's Round-2 **real pending Step 2** with more missing HP than base throughput can heal, an unused Reaction, a different existing recipient, and two Available VP. Only when that bonus can actually be used is one native callback allowed to arm and pay it. Medium Vital Intercession is offered only to R on Round 2 of a prepared Sentry encounter with a matching live Shelter host, positive native Direct Vigor and Current Vigor, nonhost recipient, unspent Reaction and two Available VP. G5→G4 executes its original packet authority and finite budget; no direct invocation of a phantom prevention value.

## Measured evidence and controls

All cells retain the source-bound roster/digests; exact G5 target and action receipts; four rounds of G0 Step 2 per original living actor; genuine G4 damage and healing with HP/Vigor conservation; target-by-target final HP/Vigor/wounds/death; finite Direct Vigor prevention, active/expired effects and Committed VP refunds; native AP/VP payments; Medium paid reassignment/Intercession receipts; Low-only self Chosen and optional Exaltation receipts; **canonical SHA-256 of the full ledger**. The replay attestor reconstructs the source scenario rather than trusting the supplied JSON or a recomputed forged hash.

Each case also includes a **same role / level / enemy / target pattern / damage dice** no-magic baseline delta for F, R and Priest HP/Vigor, prevention, Spent/Committed VP and Priest AP. The Low B lack of external support is a **verified access constraint**, not automatically a balance failure. High/Medium ally effects and Low A single-target Basic Heal are different assets and should not be conflated into a universal per-VP effectiveness ranking.

### Questions left open

1. Is High's ability to maintain distinct two-target prepared prayers at L3 strategically valuable compared with Medium's one movable host and reactive off-host aid under more varied initiative timing?
2. Does Medium's 2-Spent Reaction-backed Intercession produce enough marginal protection relative to its host's finite budget and possible reassignment cost in longer or multi-threat encounters?
3. Is the Low A external Basic Heal sufficient party contribution while it also funds its chosen self-Rite, and how much does B's two-occupied-hands limitation affect its party-support niche?
4. How would meaningful enemy AI, movement, multi-foe contact, contested spell resistance, disabling wounds and wider damage-roll samples change these fixed-policy outcomes?

**No numerical Focus changes, statistical win rate, optimization, final balance certificate or universal Focus ranking are generated.** Follow with an explicit formal Priest Life Focus Balance Assessment that names uncertainty and any *proposed*, separately approved tuning decisions.

## Reproduce

```bash
python -m unittest tests.test_b05_priest_life_multi_recipient_stress_v0 -v
python -m unittest discover -s tests -v
python -m scripts.b05_priest_life_multi_recipient_stress_v0 --seed 0
python -m scripts.b05_priest_life_multi_recipient_stress_v0 --role M --level 3 --opponent sentry_prepared --pattern alternating --pressure heavy --policy shelter_intercession
```
