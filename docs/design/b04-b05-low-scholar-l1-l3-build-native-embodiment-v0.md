# B04/B05 — Low Scholar L1–3 Character Build and Native Embodiment Verification v0

> **Source-grounded candidate sixth structural Archetype × Focus pairing.** Native G0/G1/G3/G4/G5 *bounded* Earth/Life Embodiment and Soldier evidence; **not** independent three-to-five-session combat/noncombat certification, PS-03 Spellblade completion, encounter balance, or a new general enchantment.

## Authored source sheet (T)

[Low Scholar structural source](../../scripts/b05_low_scholar_l1_l3_v0.py) establishes a **different G0 source ID `T`** from Medium Scholar `S`, Priest `M`, High Scholar `F`. The character is a lawful chosen Earth/Life/Fire technical melee generalist; it **does not** acquire a native attacking weapon technique merely because a Sword is wielded.

| Field | L1 | L2 | L3 |
|---|---:|---:|---:|
| Ability modifiers | **Strength +2, Agility +3, Precision 0, Intellect 0, Awareness +1, Presence −2, Vitality +2, Veil Affinity 0, Veil Control 0**; exact **28-point** starting purchase | unchanged | unchanged |
| HP / Vigor / VP maximum | **12 / 12 / 2** | **12 / 24 / 4** | **12 / 36 / 6** |
| Turn AP / Physical AP / Projection AP | **30 / 20 / 30** | **36 / 20 / 30** | **42 / 20 / 30** |
| Physical tempo / real Sword Guards | **1 / 1** | **1 / 1** | **2 / 2** |
| Ordinary regeneration / MP | **5 / 12** | **5 / 12** | **5 / 12** |
| Individually known Pillar techniques | **Stone Skin, Guided Regeneration, Conjure Flame** (3/3) | Add **Basic Heal** (4/4) | Same **4/4** |
| Actually prepared subset | **Stone Skin, Guided Regeneration** (2/2) | **Stone Skin, Guided Regeneration, Conjure Flame** (3/3) | Same **3/3** |
| Embodiment active limit | **1** | **1** | **1** |
| Native Embodiment VP reserve | Stone **1**, Guided **2** | Stone **2**, Guided **2** | Stone **2**, Guided **2** |
| Intensification | Not yet legal | Not yet legal | **1 Spent VP** on one live eligible host; authored timed property |
| Known Universal Veil | Veil Inspection | Veil Inspection | Veil Inspection and Blink |
| Initiative / Dodge | **+4 / 14** | **+4 / 14** | **+6 / 14** from L3 Combat Awareness |

**Training:** One-Handed Swords +2 (2 Weapon points), Veil Theory +2 and Earth Pillar Lore +2 (Scholarly 4), Medicine +2 (Professional 2), Acrobatics +2 (Physical 2): normal independent 8 Learned points in **4/2/2** families. L2 Navigation +1; no L3 extra points. **Talents:** L1 TAL-U01 Veil Insight (Veil Theory prerequisite satisfied), L3 TAL-C01 Combat Awareness (Initiative only). **Gear:** Leather armor 25 sp worn, Sword 22 sp wielded, Adventuring pack 8 sp, General artisan toolkit 12 sp carried: 67/150 sp spent, 83 sp remaining, no phantom shield/armor stacking.

**Preparation timeline:** L1 two prepared choices use the free initial selection. This source's L2 and L3 `prepared_techniques` are snapshots **after** an eligible **10-minute preparation no more than once per completed six-hour interval**; leveling itself never instantly fills the extra prepared slot, and the source adapter does not purport to perform that time passage. **Basic Heal is known but not prepared**, thus it cannot be used as a Low Prepared Arsenal action through this fixture. Other outward techniques keep their normal payment and permission and are not automatically an Embodiment. Both self Embodiments require their actual known **and prepared** technique.

## Native implementation

[Source T Embodiment adapter](../../scripts/b05_low_scholar_native_embodiment_v0.py) binds complete immutable live G0 source identity/digest, gear, abilities, training, AP/VP/regen/Guard and original Prepared Arsenal. It requires existing G1, G3 and G4. Source-legal G3 hosts own both finite reservation and effect identity; no mutable report/state is trusted for authorization.

**Activation and switching.** `LS-STONE-BODY-T1` pays one real **30-AP Projection** and commits **ceil(MaxVP/3)** (**1/2/2 VP**); the native Stone host snapshots `R=2+floor(max(0,source VC)/4)` (**R2 at VC0**) for its established Physical/Fire/Electrical HP mitigation. `LS-GUIDED-REGEN-T1` pays one real **30-AP Projection** and **2 Committed VP** for +1 on subsequent real G0 own Step2. Low may maintain **only one**. Changing requires legal **zero-AP release** (return remaining Committed, never prior Spent) **followed by a new, independently paid 30-AP Projection**. The v0 offers **no Medium-style reroute**, no automatic reactive Embodiment and no illicit Chosen Devotion/Consecration discount. L1 VA0 Guided therefore reserves its **entire 2 VP**.

**Cross-caster same-recipient exclusivity.** Before AP payment, and again after committed AP but before VP/effect establishment, the native adapter checks existing Stone/Guided hosts by both **caster and recipient**, not merely `SpellState.active(caster,kind)`. A Medium Priest already blessing T with Guided makes a redundant Low Guided activation illegal **without a resource debit**. A Priest blessing someone else does not block the Low Self profile. The ordinary Priest source rules remain unchanged.

**L3 Deep Embodiment.** Only while a valid, prepared, actually maintained T host exists, on a **ready own-turn decision** pay **1 Spent VP**. Stone Skin immediately gets **+1 native G3 resistance on the existing host**, expiring at the **start of the next own turn** (native G0 Step 1→2 transition); the host and its original reserved VP persist. Guided receives **+1 further throughput on exactly the next completed genuine own G0/G4 Regeneration Step 2**; it does not preheal HP, add a new Step, bypass Vigor, or amend elapsed-time recovery. The implementation arms the native Step window on G0's original `start_turn` path and consumes pending intensity **only after G4's actual recorded `regeneration_step` receipt**. An unresolved allocation that has not completed the Step may not consume it. Repeated pre-expiry intensification or lack of VP is rejected. Release, death or other genuine G3 host termination discards pending intensity without refund.

**Source-native battle and proof:** [14-cell fixed Soldier runner](../../scripts/b05_low_scholar_native_encounter_v0.py) reuses genuine `B06-EN-02` G5 Sword and G4 typed HP/Armor/Stone resistance, one initiative-driven G0 Step2 per actor/round and G1 contact. Three levels × four policies (baseline, Stone, Guided, paid second-turn release+switch) plus two L3 Intensification variants. Fixes explicit attack/damage die faces and `take_hit` defense; no hypothetical combat success rates, target choice, general enemy AI or source-unspecified attack. Native receipts demonstrate only actual restored HP/Vigor, spent AP/VP and Stone protection. A Guided intensity may confer **unused throughput** when damage/deficit is insufficient; this does not count as bonus HP. Each report carries the real source digests and complete event ledger, with strict **full native replay** for attestation rather than accepting user-rehashed receipts.

[Regression tests](../../tests/test_b05_low_scholar_native_embodiment_v0.py) cover L1–3 legal identity, genuine G0/VP payments and prepared subsets, fresh-action switching, native G4 HP change, L3 next-own-turn Stone expiration and true-Step-only Guided consumption, invalid/unauthorized/out-of-turn calls, cross-caster recipient collision, source digest tampering, death/release, report forgery and 14 source-replayed policies. This implements **two explicitly authored Self profiles only**. It does **not** add a Low weapon enchantment/Spellblade effect, make unprepared outward casting legal, or invent L3 Tier-2 variants.

## Acceptance and remaining gaps

This is a **sixth candidate structural pairing** (Priest H/M/Low Life; Scholar H Fire/M Earth-Life/Low Earth-Life) after review and merge, while **0/12 full independent Focus role/noncombat/adventure certificates** remain. Full Low Scholar native outgoing Sword/Flame and equipment-bound **PS-03** effects, additional physical roles, individualized scenes and actual ten-minute/6-hour preparation passage are future tasks; not silently certified by the Step/defense matrix. Other Archetypes and Focus pricing are unchanged, no global balancing authorized, B04/B05/B06/B07 blockers and strict MVP exit gates remain open.

## Reproduce

```bash
python -m scripts.b05_low_scholar_l1_l3_v0
python -m unittest tests.test_b05_low_scholar_native_embodiment_v0 -v
python -m scripts.b05_low_scholar_native_encounter_v0
python -m scripts.b05_low_scholar_native_encounter_v0 --level 3 --policy guided_intensify
python -m unittest discover -s tests -v
```

Submit Codex review; publish only after source-native evidence and exact-head Actions. Do not merge or clean branches automatically.
