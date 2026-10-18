# B06 — Hunter versus Level-2/3 parties: scripted exchange calibration v0

> **FIRST OPPOSED EXCHANGE EVIDENCE — NOT A CERTIFIED FULL ENCOUNTER, CR OR DIFFICULTY RATING.** Eight reproducible open-lane exchange cases now use the [complete Hunter benchmark](../../content/creatures/b06-hunter-of-the-woods.v0.json) against 3/4 players at Level 2/3 in **warned** and **ambush approach** setups. The engine is [scripted v0](../../scripts/b06_hunter_party_exchanges_v0.py), checked by [regressions](../../tests/test_b06_hunter_party_exchanges_v0.py). They use actual opposed fixed d20 attacks, chosen Guard/Dodge, Armor/Pen, own-turn Vigor regeneration, the legal Pounce balance rider, a Standing Opportunity, and one grooved-canine toxin gate. They intentionally **stop on the Hunter's first HP≤0 crossing** without treating Dying as death or resolving later wounds, healing, retreat or a full fight. **No random-sample probabilities or statistical CR are inferred.**

## 1. Provenance and level/party matrix

The roster intentionally repeats **only the two audited Life Low Priest sheets** in [B05 Life Low Priest build verification](b05-life-low-priest-l3-build-exaltation-verification-v0.md), rather than fabricating eleven unaudited Focus builds:

| PC slot | Source sheet | Level-2 vs Level-3 physical actions | HP / Armor | Attack vs Hunter | Guard | Normal own-turn throughput |
|---|---|---|---|---|---|---|
| A1 | Restorative Vanguard | **1 vs 2** (36 vs 42 Turn AP, Physical20) | HP12 / Leather3 | Sword **d20+7**, **4+d6 Piercing Pen2** | 17, capacity 2 vs 3 | **6**, pays own Vigor |
| B1 | Preservation Guardian | **1 vs 2** | HP13 / Brigandine5 | Mace **d20+6**, **6+d6 Crush Pen3** | 18, capacity 3 vs 4 | **6**, pays own Vigor |
| A2 | Same Vanguard build replicated | 1 vs 2 | HP12 / Leather3 | As A1 | 17 | 6 |
| B2, only for four-person group | Same Guardian build replicated | 1 vs 2 | HP13 / Brigandine5 | As B1 | 18 | 6 |

Level 2 uses these sheets' **L2 progression**, including Vigor24/26 and Level-2 talents already acquired; Level 3 has Vigor36/39. **No Chosen Rite, magical Exaltation, Held Renewal, Vital Interposition, Basic Heal, spell casting or previously active effects are invoked.** VP is therefore unspent and omitted from the narrow exchange arithmetic, not assumed nonexistent. Character records are **audited proxies**, not independent L2/L3 full-build/party certifications.

All eight cells are the cross-product **L2/L3 × 3/4 PCs × warned/ambush**. The Hunter starts HP14/Vigor42, natural Armor3, Dodge14 with −2 per previous Dodge *chosen within the same round*, no eligible Guard, regeneration throughput4 paid with Vigor at its own real Step, and one paid 24-AP Bite/Pounce per turn. Hunter's head and rear form **one** HP/Vigor pool.

## 2. Exact positioning, initiative and scripted policy

These are **predeclared conditional tactical scenes**, not an authored universal surprise mechanic. The initiative dice are deliberately held identical between warned and ambush:

| Actor | Declared natural initiative | Bonus | Result |
|---|---:|---:|---:|
| Hunter | 16 | +4 | **20** |
| A1 | 12 | +4 | **16** |
| B1 | 11 | +4 | **15** |
| A2 | 9 | +4 | **13** |
| B2 (if present) | 7 | +4 | **11** |

The Hunter therefore wins **these particular initiative rolls**. There is **no automatic first turn, bonus damage or denied player response** granted by the label *ambush*. Other initiative outcomes require separate tests.

**Warned:** open, unobstructed ground; Hunter **head (3,0), rear (2,0)** facing east, with A1 at **(4,0)** immediately head-forward, B1 (4,1), A2 (5,0) and optional B2 (5,1). The Hunter can Bite A1 but **cannot declare a valid same-turn three-step straight Pounce** from immediate contact. Other members take ordinary legal movement within their 12 MP to approach the 1×2 Hunter from unoccupied side/rear-adjacent squares.

**Ambush approach:** same PC positions, with Hunter initially **head (0,0), rear (−1,0)** facing east. Its three uninterrupted cardinal eastward whole-body translations (2 MP each, 6 MP total) put its head at **(3,0)** with A1 exactly **one head-forward adjacent square** away; no turn/pivot, blocked cell, unsupported ground or prior MP spend. Hunter declares the single 24-AP Bite+balance Pounce at the legal contact point. This is a *conditional successful stealthy approach geometry*, **not** a universal rule for surprise, awareness failure or hidden attackers.

**Committed choices for this test:** A1 preassigns legal sword Guard17 to the Hunter Bite and, if standing provokes a later legal Opportunity, Guard17 again (L2 capacity2 suffices). A1 chooses **Agility+3** for Pounce Balance. Hunter uses Dodge against each later PC attack, including misses, with per-round pressure. The front is physically reachable to all PC weapons after ordinary within-budget approach; the matrix assumes each PC legally moves to distinct exposed adjacent cells without crossing or sharing the Hunter's footprint. It does **not** claim a generalized tactical pathfinder, flanking rule, forced-target AI, free movement, or large-creature bonus. Other valid defense/action decisions must be tested separately.

## 3. Fixed rolls and timing

- **R1 Hunter Bite:** warned d20 **11+6=17**, tied Guard17 stops Bite; ambush d20 **14+6=20**, Bite **3+d6(4)=7 Piercing Pen1** against Leather3 → **5 HP**; positive grooved-canine puncture permits **one DC12 Vitality roll**. A1 rolls **8+Vitality2=10**, Full delayed toxin, **no immediate penalty**.
- **R1 Pounce:** only ambush has valid geometry; Hunter **14+4=18** pressure beats A1's **12+Agility3=15** → Prone in A1's square. It does not create another Bite/defense or automatic Grapple. A1 reaches its own genuine Regeneration Step, spends **5 Vigor** to restore 5 HP, then **Stands for 4 MP**; the Hunter has an independently legal **one Standing Opportunity**, rolls **12+6=18** against A1's second Guard17, dealing another **5 HP**. This repeats a puncture but **does not stack or reset** the already active delayed toxin. Subsequent A1 melee action remains possible. This Opportunity is an explicit scenario choice, not a mandatory automatic reaction.
- **R1 PC physical-only attacks:** A1 declares natural attack rolls **6,6**; B1 **5,5**; A2 **12,12**; B2 **12,12**. Each Level-2 PC affords **one**, Level-3 **two** paid 20-AP attacks. Same actor's attacks are committed into one target's Attack Sequence before rolls. R1 damage dice on hits are all **d6=2**. Hunter Dodges with defenses **14, 12, 10, 8…**, counting *misses* as chosen Dodges.
- **R2, if Hunter still HP>0:** it restores **4 HP for 4 Vigor** at its **real own-turn Step**, then ordinarily Bites A1 at **d20 12+6=18** against renewed Guard17; Bite damage die **d6=3** means **4 HP** residual against Leather3. In warned setup this is the first eligible Full toxin application (8+2=10 fails DC12). In ambush the earlier toxin is already active, so a repeat applies **no new Vitality resistance**. A1's genuine own-turn Step spends Vigor on missing HP, then PC attacks use R2 dice A1 **13,13**, B1 **12,12**, A2 **12,12**, B2 **12,12** and damage die **d6=4**, ending when the Hunter first reaches **HP≤0**.
- No natural attack die is 1 or 20 in this deliberately **ordinary-hit-only** fixed stream. Natural-20 confirmation, Strong/Critical/Devastating damage, zero-HP wound creation/repair, incapacitated-PC targeting, conditional suppression, magic, actual stalking/retreat, recovery between scenes and delayed T+10/30/60/120-minute venom milestones are **not** exercised. Those are **remaining acceptance work**, not absent mechanics.

## 4. Reproducible observed outputs


| Scenario | Hunter HP at end R1 | First HP≤0 round | Hunter HP on stop | A1 HP / Vigor on stop | Full toxin to A1 | Prone / Standing Opportunity |
|---|---:|---:|---:|---:|---|---|
| L2, 3 PCs, warned | 9 | **2** | −4 | **12 / 20** | R2 | No / No |
| L2, 3 PCs, ambush | 9 | **2** | −4 | **9 / 13** | R1 | Yes / Yes |
| L2, 4 PCs, warned | 1 | **2** | −2 | **12 / 20** | R2 | No / No |
| L2, 4 PCs, ambush | 1 | **2** | −2 | **9 / 13** | R1 | Yes / Yes |
| L3, 3 PCs, warned | −7 | **1** | −7 | **12 / 36** | None | No / No |
| L3, 3 PCs, ambush | −7 | **1** | −7 | **7 / 31** | R1 | Yes / Yes |
| L3, 4 PCs, warned | −7 | **1** | −7 | **12 / 36** | None | No / No |
| L3, 4 PCs, ambush | −7 | **1** | −7 | **7 / 31** | R1 | Yes / Yes |

**Reading these numbers:** Hunter HP≤0 means **unconscious/Dying under the ordinary procedure**, *not* instant kill, verified party safety or captured prey. Combat continuation and wound repair were deliberately stopped at the first crossing. The timing of Full toxin is important even when the Hunter falls immediately; its **initial T+10-minute stage** could matter after this particular scene if not cured/suppressed. No instant toxic penalties apply during the 1–2 combat rounds.

Hunter retains **42 Vigor** when downed in R1 and **38** when downed after its R2 Step: 0/4 actually paid regeneration, respectively. The fact that L3 P3 and P4 match is **script saturation**: A1 and B1 together inflict the three hits needed to put the Hunter below 0; later characters never take an attack action in this sample, not evidence that a fourth character is worthless. The Level-2 fourth member contributes an R1 hit and decreases Hunter's first-round remaining HP from 9 to 1, but the scripted R2 next actor still finishes.

## 5. Calibration interpretation, not certification

**Supported by these fixed executions:** the Hunter's **HP14 / Armor3 / single paid Physical Action per turn** can be vulnerable to concentrated legal melee from a prepared group of three or four, especially the two-action L3 Priests. It also demonstrates that a legal Pounce can produce a **Prone→Standing Opportunity** and surviving puncture with genuine Vigor cost to the defender, even when the Hunter drops before deferred venom becomes active. The separate timed toxin can extend risk **after combat**.

**Not supported:** a win probability, CR, XP budget, general "easy" label, balance of elite predators across terrain, survival against mixed ranged/caster parties, automatically successful stalking, all first-initialive sequences, or reliably available forced Pounce. These eight deterministic lines **do not calibrate the species by themselves**. Two real player characters used as templates are both Low Life Priests and may be unusually resilient; duplicating them is a controlled baseline rather than a diverse adventuring party.

**Next required evidence:** (1) many *paired random seeds* with valid natural-1/20 confirmation, action choice/Guard allocation and wounds at 0 HP, (2) independently authored Level-2/3 non-Priest martial, ranged and caster sheets, (3) actual map-validated alternate terrain, blocked charge lanes, withdrawal and counterpounce timing, (4) both Chosen Rite/Exaltation alternatives and Venom Endurance with real VP/Vigor state, (5) delayed poison and overnight/6-hour recovery, (6) GM-recorded played encounters. Only then consider a creature CR and encounter difficulty threshold; the bestiary must remain **`unrated`**.

## 6. Reproduction

Run from the repository root:

```sh
python -m scripts.b06_hunter_party_exchanges_v0
python -m unittest tests.test_b06_hunter_party_exchanges_v0 -v
python -m unittest discover -s tests -v
python -m scripts.validate_b06_footprints
```

The harness prints all eight traces as JSON and has no third-party dependencies. Its **fixed dice are part of the test contract**, not measured random draws. Any revision to authored Hunter stats, priest sheets, range geometry, or this sampling policy must revise the script and expected test values together; **never silently preserve an obsolete result table**.
