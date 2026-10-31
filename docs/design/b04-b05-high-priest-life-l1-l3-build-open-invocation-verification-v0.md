# B04/B05 — High Priest Life L1–3 Character Build and Open Invocation Verification v0

> **Current-source B04/B07 correction (31 October 2026):** The L3
> `TAL-M03 Frugal Technique` selection described in the historical
> character paragraph below was **not earned by High Focus**. The
> corrected source selects **TAL-C02 only at L1–3**; no TAL-M03 discount
> is available to this High Priest. The existing bounded native
> policies did not use that optional discount. No HP/VP/AP or native
> outcome is retroactively changed by this ledger erratum.

**Scope:** executable **structural build + G0/G3/G4 Life primary casting**, distinct High Priest prepared/Open Invocation/Open Prayer access receipts. This is not a High Priest's independently certified full character/encounter or a three-Focus matched balance run. All prices remain provisional and unchanged.

## Sourced character

One **High Priest / Life**, same valid mundane 28-point starting Ability allocation as the earlier Life Medium Vanguard: STR+2, AGI+3, Precision 0, Intellect 0, Awareness+1, Presence−2, Vitality+2, Veil Affinity0, Veil Control0. At L1 invest sword category +2 and eight Learned Discipline points (Veil Theory+2, Life Pillar Lore+2, Medicine+2, Acrobatics+2), L2 adds Survival+1. Start with Leather 25sp, Sword 22sp, Medical kit 15sp, Pack 8sp = **70sp paid / 80sp left**; one-handed Sword leaves one hand free for Basic Heal when actually free. Talents **TAL-C02 Enhanced Regeneration at L1** and **TAL-M03 Frugal Technique at L3**; TAL-M03 is an available optional once-own-turn discount, **not activated automatically** in the v0 scenarios. +1 Pillar Accord, Resonance0, Miracle Debt0. L3 unlocks universal Blink but **10 Spent VP remains a separately payable requirement**, not a free invocation.

| Stat | L1 | L2 | L3 |
|---|---:|---:|---:|
| Max HP | 12 | 12 | 12 |
| Max Vigor | 12 | 24 | 36 |
| Max VP (VA0 High) | 6 | 12 | 18 |
| Turn AP | 30 | 36 | 42 |
| Physical / Projection Action AP | 30 / 20 | 30 / 20 | 30 / 20 |
| Max Physical / Projection Tempo | 1 / 1 | 1 / 1 | 1 / 2 |
| Ordinary Guard capacity | 1 | 1 | 1 |
| Actual selected natural regen throughput | 4 | 4 | 4 |
| Prepared capacity incl. starting Accord +1 | 4 | 5 | 5 |
| Open Prayer unspecified reservation | 0 | 0 | At most 1 of the five |

High Focus's **base** regeneration is VIT2 +1 = 3; actual selected TAL-C02 separately adds +1. The normal one-step Vigor debit is unchanged. Ability and gear are a deliberate selected build, not automatic bonuses for the entire Priest Focus.

## Legal initial preparation variants

The character-creation selection is fixed **before G0 Round Begin**. This is not a free mid-scene prayer reshuffle and does not implement the full 10-minute / six-elapsed-hour repreparation clock. Each list contains only **distinct existing, actually authored Life techniques** from its Restoration / Preservation / Nature Aspects. None adds a known spell or permits a second Pillar.

| Preparation | L1, four prepared | L2, five prepared | L3, four prepared + one unspecified slot |
|---|---|---|---|
| `standard` | Basic Heal, Guided Regeneration, Vital Shelter, Woodland Rapport | Same + Venom Endurance | Basic Heal, Guided Regeneration, Vital Shelter, Woodland Rapport; one unspecified |
| `invocation` | Guided Regeneration, Vital Shelter, Woodland Rapport, Venom Endurance | Same + Gentle Growth | Guided Regeneration, Vital Shelter, Woodland Rapport, Venom Endurance; one unspecified |
| `ward_invocation` | Basic Heal, Guided Regeneration, Woodland Rapport, Venom Endurance | Same + Gentle Growth | Basic Heal, Guided Regeneration, Woodland Rapport, Venom Endurance; one unspecified |

A slot in this list is only **prepared access**. This v0 executor handles **Basic Heal Primary**, **Guided Regeneration** fixed/maintained Primary and **Vital Shelter** fixed/maintained Primary. Other named authored Life techniques remain preparation identities; a request to execute their missing native adapters fails closed. No free Venom Endurance toxin guard, Woodland Rapport animal interaction or Gentle Growth effect is modeled. No composite, extra technique, Tier-2 Guided/Shelter, Miracle Petition or uncontested opposing Intrusion is invented.

## Action, pricing and source-authorized application

`party_actor("H", level, ...)` creates the exact High Life G0 actor by profile and digest; `HighLifeLiturgy` chooses the initial legal preparation and attaches to actual G3/G4 *before* Round Begin. All paid actions use **G0 spend_ap**; maintained and fixed hosts use **G3 named source effects**; actual Basic Heal HP/Vigor/Repair uses **G4 resolve_heal**. Guided changes only the actual target's **once-per-own-turn Step 2**. Shelter creates a single **B=8+max(0, VC)** finite native G3/G4 Vigor prevention pool. No scripted opponent packet or synthetic extra Step is included.

| Legal action | G0 action | Normal VP payment | Extra VP |
|---|---|---|---|
| **Prepared Basic Heal T1** | 20 AP Projection | 2 Spent | None |
| **Prepared Basic Heal T2, L3 only** | 20 AP Projection | 4 Spent | None |
| **Prepared Guided maintained** | 20 AP Projection | 2 Committed | None |
| **Prepared Shelter maintained** | 20 AP Projection | 2 Committed +1 Spent | None |
| **Unprepared, eligible T1 Basic Heal Open Invocation** | **Entire still-untouched Turn AP**: L1 30, L2 36, L3 42 | 2 Spent | **+1 separate Spent** (3 total) |
| **Unprepared maintained Shelter Open Invocation** | Entire still-untouched Turn AP | 2 Committed +1 Spent | **+1 separate Spent** (4 Available required) |
| **Unprepared fixed Shelter Open Invocation** | Entire still-untouched Turn AP | 2 Spent, B8 / one-minute maximum | **+1 separate Spent** (3 total) |
| **L3 Open Prayer first selection Basic Heal or Shelter** | **20 AP Projection**, not Full Action | Technique's normal VP | **No Invocation surcharge** |

Open Invocation is restricted to an eligible **unprepared** normal-tier chosen-Pillar spell (which can require a free hand, valid target, real G1 range/path, and G4 effects). High Priest does **not** grant a simultaneous physical weapon attack when declaring a Full Action. It is illegal if any of the turn's AP was spent already, even if enough raw AP appears available. The **+1 surcharge is Spent**, never Committed, returned on release, TAL-M03-discounted, or an extra invocation capacity. Post-commit lost target, hand, source or funding **forfeits the already-paid AP** but no technique or surcharge VP is paid before a valid magical application. Valid application spends the full normal Spent component plus surcharge. Contested/previously refused bodily Intrusion is explicitly **unresolved** without an independent resistance/ward check; unopposed casting only is executed here.

**L3 Open Prayer:** precisely one **existing capacity slot** is unspecified at legal character preparation. Its first later **legal declaration**, after targeting/AP/VP preflight, binds exactly one eligible authored Life technique permanently to that slot until a future independently authorized preparation; the same paid normal cast then uses Projection AP and the ordinary VP **without Open Invocation surcharge**. A declaration interrupted by later committed responses **still binds that original slot choice**; AP remains paid and 0 application VP is charged. No second Open Prayer slot, retroactive target change, unprepared casting discount for another technique, or instant re-preparation.

## Verification and limits

Run:

`python -m unittest tests.test_b05_high_priest_life_l1_l3_v0 -v`

`python -m unittest discover -s tests -v`

`python -m scripts.b05_high_priest_life_l1_l3_v0`

Tests verify genuine source digest, L1–3 allocation/resources, 3 original legal preparation variants, prepared Basic Heal G4 receipts and two L3 Projection actions, both Open Invocation payment classes, Full Action preconditions and interruption, native Guided Step 2, finite Shelter G4 prevention, L3 Open Prayer (Basic Heal and Shelter), fixed-vs-maintained contracts, wrong source, wrong access, illegal tier, blocked paths, no free hand, no invented Life actions and source ledger/VP conservation.

**Not certified:** authentic opposed High Life G5 encounters; independent full L1–3 Focus certification; contested healing resolution; preparation changes after 10 minutes/six world-hours or Accord changes during the scene; High optional TAL-M03 selected discount in normal/invoked turn; Universal Blink affordability, Miracle Petition, Open Prayer after new Accord-driven suspension; full Life catalogue casting, all injury/toxin contingencies or representative three-Focus balance. The L3 normal two-Projection tempo does not itself guarantee two useful spells. This PR changes no authored VP/AP prices or Focus distinction, and adds no B04/B05/B07 certification.

## Acceptance gate

1. G0 authentic High-Life source and real VP/AP/Regeneration figures at all levels.
2. G3/G4 source-paid normal Prepared Life effect paths, with actual receipt and bounded mode.
3. L1–3 exact Full Action + separate surcharge on unprepared normal-tier Invocation; rejects false prepared discounts.
4. L3 first-legal-use binding of **one** Open Prayer slot, correct normal cost, persisted after post-commit interruption.
5. Historical B06 scenario ledgers, hashes, and older Focus fixtures unchanged by ordinary-path additions.
