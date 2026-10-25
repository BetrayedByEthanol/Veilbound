# B04/B05 — Medium/Low Scholar Native Physical Offense and Weapon Readiness v0

> **Scope:** existing medium S and low T **one-handed Sword Cut** ordinary physical attack, not an enchantment or a new Focus ability. This implements source-backed G0/G1/G2/G4/G4.5/G5 attack sequences and checks original Inward/Embodiment hosts without redefining them. It is **not** full encounter or Focus certification.

## 1. Exact authored characters and weapon rule

The only eligible player fixtures are the existing **Medium Scholar Earth/Life S L1–3** and **Low Scholar Prepared Embodiment T L1–3**. Both have source-authored Strength +2, Agility +3, One-Handed Swords direct Training +2, a **wielded ordinary Sword**, and leather armor. These are not A/B Priest physical proxies or independent Fighter/Spellblade role certificates.

| Weapon element | Canonical [Weapons and Armor](../rules/05-combat/weapons-and-armor.md) and [Attack Math](../rules/05-combat/weapon-attack-and-guard-math.md) |
|---|---|
| Identity | Single actual one-handed Sword, ordinary **Cut** choice, no secondary type or Power profile |
| Accuracy | d20 + STR2 + AGI3 + One-Handed Swords Training2 = **+7** |
| Raw direct HP | Sword fixed3 + d6 + floor(max(STR2,0)/2) = **4 + d6** |
| Mitigation | **Penetration 2**; enemy Armor reduced by Pen2 **once**; wound/critical through actual G4/G5 |
| Action | Medium **24 Physical AP**, Low **20 Physical AP**; no spell AP, no VP to attack |
| Source attack IDs | Medium `B05-PC-S-SWORD-CUT`, Low `B05-PC-T-SWORD-CUT` |
| Regular Physical Tempo | Medium L1/2/3 **1/1/1**, Low **1/1/2** |
| Sword Guard | **17** when actually wielded and ready, capacity Medium **1/1/1** and Low **1/1/2** |
| Cast interaction | Inward/Embodiment is still its own paid Projection action. L1–3 **Physical + Projection** cannot fit together into one turn; no magic automatically rides the Sword |

### Explicit verified readiness

The [profile authority](../../scripts/b05_scholar_native_sword_v0.py) binds the actor against the **actual selected B05 file digest, full original source/equipment/training, level, Focus, source G0 AP/resource attributes**, and a single native profile ID. A profile name alone is not authority. The live G2 ready/wielded set must contain **exactly the sourced Sword**. A nonexistent G2 adapter, an unwielded Sword, another weapon, a spoofed source digest/equipment/Training, or a mismatched ID **fails before G0 Attack Sequence AP or defender Guard/Dodge is spent**.

The same condition drives G1 **melee contact and threatened-square logic** (so an actor cannot continue threatening with a stowed weapon). It also gates the Sword's actual **G0 Guard allocation** before consuming Guard capacity, and **G5 Guard resolution** after a once-valid declaration: no ghost weapon Guard after a real loss of readiness. The system does **not** grant a free re-draw, hand switch, projectile Guard, additional reaction or alternative parrying instrument. Removing or changing an equipped Sword must be a separately legal physical equipment event; the tests simulate its result to verify fail-closed behavior, not authorize a free loss/restore timing path.

**Source provenance:** Both S/T `Source.attack_profiles` tuples now contain precisely their native named mundane Sword attack. G5 validates the same profile/ready set on both declaration and resolution; G4 computes its canonical Cut/Pen2 HP packet with the native actor's original Strength and source; G4.5 binds the exact prepaid physical action, canonical declared slot, actual target, contact and defense. The existing SourceMelee attacker/defender interfaces and Soldier/Sentry/Hunter handling are unchanged for other roles.

## 2. Genuine opposed scene

[The two-round native audit](../../scripts/b05_scholar_native_physical_offense_v0.py) runs the actual G0 cycle with Scholar S/T and **B06-EN-02 Ordinary Human Soldier**, one-square adjacent contact, real G2 readiness and G4 recovery. Each policy provides fixed legitimate choices and exact roll faces: Sword and Soldier hit d20 **12**; damage d6 **4**; Take Hit defenses; wound-location die **8** whenever a wound qualifies. Native G0 Step2 is executed for each participant, with Scholar allocating eligible HP restoration and the Soldier explicitly conserving Vigor; these are bounded policies, not optimized enemy AI.


| Policy | L1/L2 | L3 | What native mechanics it proves |
|---|---|---|---|
| `baseline` | Medium and Low | Both | One paid Sword attack each own turn, with actual G5+G4 damage and Soldier retaliation |
| `stone` | Both | Both | First-turn paid, source-authorized MS/LS Stone self-effect, second-turn Sword action, genuine G4 resistance and no extra free action |
| `guided` | Both | Both | First-turn paid MS/LS Guided, genuine G0 Step2 throughput, second-turn Sword, no additional restoration step |
| `double` | Not legal | **Low only** | Two prepaid **20-AP** Sword slots in the first L3 Low turn, resolved in exact declared order; later new turn remains independently funded |

The matrix has **19 cases** (6 baseline + 6 Stone + 6 Guided + 1 L3 Low double). Each records actual source digests, signed G0/G4/G5 ledger, HP/Vigor/VP, physical vs Projection payments, native self-host identity, real Step2 and Soldier retaliation. `attest_case` replays the entire source policy and refuses forged metrics or recomputed-digest ledgers. The matrix omits full individual ledgers for size but retains original per-cell digests. Any wounded/Dying combatant follows native G4 rather than a fabricated terminal score.

## 3. Verification and remaining limits

The [focused tests](../../tests/test_b05_scholar_native_physical_offense_v0.py) cover all six structural profiles, Cut/Armor/Pen2 damage, Medium/Low action price, L3 Low ordered doubles, L1/2 insufficient AP, lost Sword/Guard both before and **after** G0 commitment, source forgery, actual native misses, Stone/Guided costs, Step2, exact scene replay, and JSON persistence. This also requires updating the existing Scholar Flame source attestation and original test expectation: S/T now have **one separately authenticated mundane Sword profile**, not an empty physical attack roster. Their known/prepared Flame access, Focus costs and source Throwing remain unchanged.

**Open gates:** complete source-authorized attack-defense repertoire (e.g. ordinary weapon Pierce selection, Feint/Charge/Disarm in mixed policies), actual hands/item-state transitions, Opportunity/OA Sword hits, broader mobile/cover/multi-enemy tactics, full High/Mid/Low matched tactical balancing, recovery and attribute advancement, any Low weapon-focused Embodiment or conjured magic sword, and full PS-01/PS-02/PS-03/PS-08 and independent Focus certification. This PR grants **no numerical buff or nerf**, passive weapon enchantment, or shadow Guard capacity. Structural Archetype×Focus coverage remains **6/12**, complete independent Focus certification **0/12**.

## Reproduction

```bash
python -m scripts.b05_scholar_native_physical_offense_v0
python -m scripts.b05_scholar_native_physical_offense_v0 --focus Low --level 3 --policy double
python -m unittest tests.test_b05_scholar_native_physical_offense_v0 -v
python -m unittest discover -s tests -v
```

Open one PR for this source-bound feature and verify exact-head CI and Codex review. Do not merge or delete the branch automatically.
