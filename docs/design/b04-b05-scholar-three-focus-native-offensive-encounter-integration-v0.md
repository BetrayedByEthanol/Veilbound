# B04/B05 — Scholar Three-Focus Native Offensive Encounter Integration v0

> **Bounded genuine G0/G1/G2/G3/G4/G5 offense and retaliation.** The three Focuses now share a **source-authorized Thrown Flame Primary** under their real AP/VP/access rules; this does not invent native Sword profiles or certify a complete combat role. The selected **Low Scholar L1 knows Conjure Flame but did not prepare it** and remains **unable to cast in this character loadout**. Do not replace that absence with a fabricated ordinary melee attack or free spell.

## Source-derived authorization and rule boundaries

The [native Flame authority](../../scripts/b05_scholar_thrown_flame_access_v0.py) binds each live actor to its actual **High F**, **Medium S** or **Low T** structural source and file digest, selected Ability array, weapon Training, gear state, turn/action costs, VP capacity, and individually learned repertoire. For Low it also requires the *actual prepared subset*. A forged digest, changed source status, non-structural proxy, added attack profile or altered equipment/training is rejected before AP/VP. When G2 is installed, the physical lane requires the original live ready/wielded state: F's carried Dagger does not become a free Guard; S/T wield one Sword and retain a different free hand. The invocation requires an explicit **available functioning hand**. There is no dynamic generic dual-wielding/hand occupancy model here, so any unevidenced occupied-hand claim is not silently accepted.

| Selected source | L1 | L2 | L3 | Projection AP | Source Throwing modifier | Primary T1 / T2 Spent VP |
|---|---|---|---|---:|---:|---|
| High F | Known, legal | Known, legal | Known, legal, Used Tier 2 | **20** | **+2 Throwing**; AGI3/PRE0 ⇒ attack **+5** | **2 / 4** |
| Medium S | Individually learned, legal outward cast | Legal | Legal, Used Tier 2 | **24** | **No learned Throwing ranks**, AGI3/PRE0 ⇒ attack **+3** | **2 / 4** |
| Low T | **Known but NOT prepared: blocked** | Prepared after legal L2 preparation window | Prepared, Used Tier 2 | **30** | **No learned Throwing ranks**, AGI3/PRE0 ⇒ attack **+3** | **2 / 4** |

The zero Throwing rank does **not** add a penalty or grant phantom +2 Training. One legal cast still has actual normal `d20 + AGI + PRE + Throwing`, *exactly one* Focus-priced Projection, and **2×Used Tier Spent VP**. No Strength, Sword Training, or Veil Control bonus changes accuracy. Existing G2 physical ray (1–3 squares, +0 range difficulty, cover, screens, Prone, defense readiness) and G3 critical confirmation/VP-before-launch logic remain authoritative. G4 consumes only the original G3 direct-hit capability, dealing **F2 HP plus separate Vigor `2+ceil(d8×T/3)+VC`** with no fictitious Armor mitigation on the elemental packet. The same genuine G5 Soldier melee retaliation and G4 HP/Vigor/wound/death path are reused. No second shot, free weapon strike, spontaneous Low preparation, or automatic attack on current equipment is granted.

**Cast interruption and timing:** preflight unprepared access, missing hand, out-of-range line, current threat, unavailable VP/AP, invalid tier or missing damage evidence *before any AP*. After AP commitment the source/prepared/wielded state and physical line are checked again; a lost line or source authority interrupts without spending unlaunched VP. Full active Opportunity/Interception and screen collisions remain unresolved in this bounded scene and are never auto-declined as a free cast. The initial High F direct attack behavior stays unchanged for previously authored Ranged and G3 tests.

## Follow-up: native ordinary Sword authorization

The later [Medium/Low Scholar Native Physical Offense and Weapon Readiness v0](b04-b05-medium-low-scholar-native-physical-offense-weapon-readiness-v0.md) explicitly adds **one source-bound ordinary Sword Cut profile** to the selected S/T sheets. References below to empty S/T native melee rosters are the **historical boundary of this earlier Thrown Flame-only PR**, not the current state. The new mundane profile grants no enchantment or extra Flame preparation.

## Bounded matched native scene

[The native encounter runner](../../scripts/b05_scholar_three_focus_native_offense_v0.py) uses one Scholar (source F/S/T) at (2,2) and the same fully equipped **B06-EN-02 Soldier** at (4,2), with clear G1/G2 lane and fixed rolled Initiative Scholar first. Three source-selected levels, all three Focuses, and three policies yield **21 cells**:

- **9 × `no_spell`**: physical baseline, no imaginary Scholar offense;
- **9 × `flame_t1`**: eight genuinely paid source-legal casts + the explicitly blocked **Low L1 unprepared** case;
- **3 × `flame_t2`**: real High/Medium/Low L3 Used Tier-2 paid casts.

Every cell runs **two complete G0 rounds**: the Scholar has one first-round opening decision (cast or decline), then the Soldier legally moves one G1 square into melee and resolves one real paid G5 sword attack on each enemy own turn when both survive. On the Scholar's second turn the soldier is already threatening the caster: **no free second projected attack is claimed**. Real native G4/Step2 handles regeneration and attrition. The Soldier chooses explicit **zero regeneration allocation** as a fixed policy, not a model of optimal AI. This is deliberately not a duel victory policy, a three-Focus DPS estimate, or a full terminal certificate.

Fixed original inputs: G3 Flame initial **d20=12**, d8 Vigor=3; G5 Soldier sword attack d20=12, damage d6=4, `take_hit` and wound-location=8. Every report retains actual G0/G2/G3/G4/G5 ledger, source fingerprints, source attack bonus, focus-specific AP and VP, Soldier hits, HP/Vigor and genuine own regeneration receipts. One exact native report can be `attest_case`-replayed; source/ledger or report forgery is rejected even with user-rehashed digests. Matrix output includes 21 compact, source-tied case hashes; no fake win rate or numerical balancing claim.

### Native evidence vs unsupported work

This PR closes the **shared source-authorized Thrown Flame Primary** coverage gap for eligible F/S/T builds and verifies identical target, initial range/face, source-accurate costs and actual retaliation. It **does not** establish a native S/T ordinary Sword melee attack: those G0 source characters currently have deliberately **empty** `source.attack_profiles`; wielding a Sword and owning Training ranks do not themselves grant a G5 player attack binding. It also does not implement F's full offensive composite timing, Low Reserved Weapon `Weapon Enchantment`, independent weapon-Embodiment permission, movement/reactions under genuine live casting pressure, Low L1 alternative prepared loadouts, mixed-party tactical policy, long attrition/rest, or full adventure certification. They require separate authoring and source-proof work.

**Recommendation:** no Scholar Focus AP/VP/Spell numerical tuning from 21 deterministic cells; before a full combat-role certification, integrate **source-grounded S/T physical Sword damage and shared active enemy defenses**, then open varied movement/cover/Reaction/tactical scenarios. Any Low L1 alternative requires an explicit separately purchased/prepared character, not retroactive modification of the approved L1 sheet. Structural pairing coverage remains 6/12; complete independent Focus certification remains 0/12.

## Reproduce

```bash
python -m scripts.b05_scholar_three_focus_native_offense_v0
python -m scripts.b05_scholar_three_focus_native_offense_v0 --focus Medium --level 2 --policy flame_t1
python -m unittest tests.test_b05_scholar_three_focus_native_offense_v0 -v
python -m unittest discover -s tests -v
```

Run Codex review and verify exact PR head against GitHub Actions. Do not merge or delete the branch automatically.
