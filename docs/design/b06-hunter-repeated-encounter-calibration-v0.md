# B06 — Hunter Repeated Combat Windows v0 (Phase 2)

> **REPRODUCIBLE SIMULATION EVIDENCE — NOT A PLAYTEST OR CHALLENGE RATING.** Extends [Phase 1's eight fixed-dice party exchanges](b06-hunter-party-encounter-exchange-calibration-v0.md) with **512 paired deterministic seeds** across **Level 2/3 × 3/4 PCs × warned/ambush × Guard/Dodge**: **16 cells and 8,192 bounded trials**. The [runner](../../scripts/b06_hunter_repeated_exchanges_v0.py) and [regressions](../../tests/test_b06_hunter_repeated_exchanges_v0.py) use authored Hunter and Low Life Priest attack/defense data. These are **simulated outcomes under selected tactics**, not observations of human players or unconditional win probabilities.

## Controlled party and combat contract

- The group still alternates repeated, structurally audited **A — Restorative Vanguard** and **B — Preservation Guardian** [Life Low Priest L1→3 sheets](b05-life-low-priest-l3-build-exaltation-verification-v0.md), using the sheets' actual L2/L3 stat progression. A1 is the **only Hunter target** in this deliberately focused comparison; all three/four PCs use their legal **one or two paid physical attacks** and focus the Hunter. No fake martial/caster sheets are introduced.
- Hunter retains **HP14, natural Armor3, Dodge14 with escalating −2 for each chosen Dodge, Vigor42, own-turn regeneration up to 4 for equal Vigor, Bite d20+6 / 3+d6 Piercing Pen1, linked Pounce Strength+4** and **no natural Guard instrument**. PC A1 chooses **sword Guard17** as long as capacity is available, or under the independent **Dodge** policy chooses actual **first Dodge14 then −2 per further Dodge in the same round**.
- Warned starts **head-adjacent** and permits normal Bite, not a fictional free three-step Pounce. Ambush starts with the legal **straight cardinal three-step head-forward Charge lane** from Phase 1; **only when Hunter acts before all PCs in round 1** does that specific movement still permit a paid Pounce. An earlier PC's declared within-12-MP approach disrupts this prepared run-up, and the Hunter may use an ordinary paid Bite from reachable front contact instead. Ambush **never** grants free surprise damage, a suppressed response or initiative advantage.
- Every actor rolls an independent **d20+4 Initiative**; ties apply **Awareness then Agility**, and remaining ties use a seeded roll-off. Hunter and both Priest sheets share initiative +4 (Hunter AWA2/AGI2, A AWA1/AGI3, B AWA0/AGI2). Initiative order and attack/defense rolls are **paired across warned/ambush and Guard/Dodge by keyed SHA-256 seed streams**, so one policy does not silently cause all subsequent unrelated dice to reroll.
- Rounds start with refreshed Guard/Dodge pressure, Opportunity and Reaction availability. Own-turn Step 2 regenerates actually missing HP using recipient Vigor, including when the Hunter was injured by earlier-initiative PCs. The Hunter **chooses one Bite/Pounce each eligible own turn**, and otherwise exploits its one physically legal **Standing Opportunity** when A1 begins to rise; the **+2 melee attack against a still-Prone defender** is applied before Standing completes, with A1's 4 MP committed. PC attacks are predeclared as a per-target Attack Sequence; the Hunter chooses Dodge on each hit attempt and therefore accrues Dodge Pressure **even when the attack misses**.
- Natural **1 always misses**. Natural **20** follows the authoritative single confirmation: versus active Guard/Dodge, failed confirmation **Strong +1d4**, successful **Critical +2d4**, natural20 confirmation **Devastating +2d4**; versus Take Hit, initial 20 is Critical, confirming 20 upgrades to Devastating. Extra dice apply **once** to the direct HP packet **before** physical Armor/Penetration. Pounce Balance is independent of Bite hit and its tie does not knock Prone. Only **real surviving grooved-canine Piercing HP** initiates one **DC12 Vitality** resistance: Full on fail, Reduced on success, **no immediate penalty and no restacking**.
- **Stopping boundary:** a trial ends when **Hunter first reaches HP≤0**, when **A1 first reaches HP≤0**, on a **Devastating Critical with an unresolved wound** even if target HP stays positive, or after at most **three rounds** without crossing. First 0 HP is **Dying**, not an automatic kill, and triggers a wound the runner intentionally does not continue resolving. Likewise, an above-zero Devastating wound may alter future actions, so the runner reports **devastating_wound_unresolved** instead of pretending it has no effect. This explicitly avoids fabricating wound location, treatment, NPC surrender, retreat, AI tactics or a party-wide defeat when only A1 is down.

## Reproduced 512-seed results

All counts are **out of 512 fixed seeds per cell**. *Hunter first 0* is a **stopping event**, not a party victory; *A1 first 0* does not mean all PCs are defeated. Devastating unresolved and three-round window end are **competing, separately reported outcomes**. Avoid normalizing by “completed wins” or assigning a CR.

| Party | Opening | A1 defense | Hunter first 0 | A1 first 0 | Devastating unresolved | Window end | Pounce uses | Full / Reduced venom |
|---|---|---|---:|---:|---:|---:|---:|---:|
| L2, 3 | Warned | Guard | 503 | 1 | 4 | 4 | 0 | 76 / 103 |
| L2, 3 | Warned | Dodge | 503 | 1 | 4 | 4 | 0 | 95 / 143 |
| L2, 3 | Ambush | Guard | 499 | 5 | 4 | 4 | 145 | 89 / 109 |
| L2, 3 | Ambush | Dodge | 498 | 6 | 4 | 4 | 145 | 106 / 149 |
| L2, 4 | Warned | Guard | 509 | 0 | 3 | 0 | 0 | 55 / 75 |
| L2, 4 | Warned | Dodge | 509 | 0 | 3 | 0 | 0 | 73 / 112 |
| L2, 4 | Ambush | Guard | 507 | 2 | 3 | 0 | 119 | 64 / 79 |
| L2, 4 | Ambush | Dodge | 506 | 3 | 3 | 0 | 119 | 82 / 116 |
| L3, 3 | Warned | Guard | 508 | 1 | 3 | 0 | 0 | 41 / 64 |
| L3, 3 | Warned | Dodge | 508 | 1 | 3 | 0 | 0 | 57 / 93 |
| L3, 3 | Ambush | Guard | 507 | 2 | 3 | 0 | 145 | 51 / 67 |
| L3, 3 | Ambush | Dodge | 507 | 2 | 3 | 0 | 145 | 65 / 97 |
| L3, 4 | Warned | Guard | 509 | 0 | 3 | 0 | 0 | 31 / 49 |
| L3, 4 | Warned | Dodge | 509 | 0 | 3 | 0 | 0 | 46 / 73 |
| L3, 4 | Ambush | Guard | 508 | 1 | 3 | 0 | 119 | 36 / 51 |
| L3, 4 | Ambush | Dodge | 508 | 1 | 3 | 0 | 119 | 51 / 75 |

The Hunter is the **first creature to reach nonpositive HP** in roughly **97–99%** of these *highly constrained focus-fire trials*. This **confirms a vulnerability of this playstyle/fixture**, not a general 97–99% party win chance: no one attempted to retreat, cast, defend an ally, exploit alternative terrain, draw ranged fire, change target, or play through injuries. The **3→4 party change** and L2→L3 improvement are therefore **policy-conditional**. The Guard-versus-Dodge difference is clearer in **accepted venom applications** than in first-down counts; its delayed stages can matter later even when the Hunter is downed before 10 minutes.

A Pounce attempt occurs in **145/512 seeds with a 3-PC ambush setup** and **119/512 with 4 PCs**, where the Hunter wins actual Initiative outright; it isn't guaranteed just because the scene is labeled an ambush. Knockdown and Standing Opportunity require subsequent legal trigger and response. The source's **Full/Reduced** venom remains pending when encounters stop; its T+10/T+30/T+60/T+120-minute effects were **not** simulated in the short combat window.

## Limitations / next acceptance gates

**No CR, XP, threat point or finished encounter difficulty is assigned.** The seed census is small, its inputs are artificial uniform dice, and all tactics are deterministic assumptions. Critical wound types are not adjudicated; **all 0-HP and Devastating outcomes terminate** before healing/repair/retreat, and **no full Dying continuation is claimed**. The benchmark parties reuse just **one Archetype/Focus**, include **no active Life Rites/Exaltations, spells, VP expenditures, Venom Endurance, movement tactics beyond conditional open-lane reach, opportunity suppression, target switching or player decision trees**.

Next step: (1) genuine Dying/wound continuation and GM-verified encounter traces; (2) non-Priest L2/3 ranged and caster builds, including legal full VP/action sets; (3) blocked paths, varied terrain/line of fire, intervention and retreat/withdrawal behavior; (4) alternate PC decisions and Hunter prey selection; (5) post-fight delayed toxin and six-hour recovery; (6) additional independent seed batches only **after** these decision/model deficiencies are addressed. **B06 remains blocking/unrated and 0 full encounter packs certified.**

## Verification

From the repository root:

```sh
python -m scripts.b06_hunter_repeated_exchanges_v0 > /tmp/b06-hunter-phase2.json
python -m unittest discover -s tests -p 'test_b06_hunter_repeated_exchanges_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.validate_b06_footprints
```

The **new focused tests were run and passed** against an isolated local harness and a minimal mirror of the merged Hunter's pinned stats (**5 methods**, 512-seed matrix), not against a connected repository checkout. The full repo test suite and footprint validation have **not** run in that isolated environment and require CI/Codex verification. Count pins are reproducibility tests, **not** an endorsement of simulation assumptions.
