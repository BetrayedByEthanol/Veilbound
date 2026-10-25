# B04/B05 — Scholar Three-Focus Comparative Balance and Native Encounter Audit v0

> **Decision: keep existing provisional numbers unchanged.** High / Medium / Low Scholar L1–3 differ in real AP/VP, equipment and access; the data support a **bounded shared defense comparison**, not a ranked full combat-role or matched-offense win rate. No extra technique, generalized Inward/Embodiment, unauthorized native outgoing attack or Spellblade weapon enchantment is introduced.

## 1. Source and evidence boundaries

The [executable audit](../../scripts/b05_scholar_three_focus_comparative_native_audit_v0.py) reads the actual canonical [Scholar rules](../rules/08-archetypes/scholar.md), [exact Earth/Life focus profiles](../rules/07-veil-magic/scholar-inward-embodiment-profiles-v0.md), [Turn AP](../rules/05-combat/action-categories-and-physical-tempo.md), and [VP rules](../rules/07-veil-magic/volition-points.md), plus the **existing** character and encounter source. It signs byte-level SHA-256 hashes of **15** specific rules/build/native runtime files before running. Certain Focus/price declaration snippets must remain unique; even a same-length change to sourced bytes changes the resulting audit digest. The complete audit is normalized to **JSON-compatible containers before its digest is calculated**, including the original Medium/Low `vp` tuples, so the exact CLI-generated JSON can be loaded again and attested unchanged. Its `attest_audit` independently rebuilds and checks the complete source-bound result (and `attest_matched` replays one exact native scene), rejecting report edits even if the user recomputes the reported ledger digest.

There are **three deliberately distinct evidence layers**:

1. **Nine actual selected structural characters**: source `F` High Scholar Fire, `S` Medium Scholar Earth/Life, `T` Low Scholar Earth/Life. These use **identical nine starting Ability modifiers** (STR2 AGI3 PRE0 INT0 AWA1 PRES−2 VIT2 VA0 VC0) and HP12, Vigor12×Level, but *different* individual learning, Training disciplines, talents, equipment, and Focus AP/VP. Their selected builds are not fictional statistically matched alternative characters.
2. **18 genuinely matched three-Focus Soldier scenes**: each level (L1–3) × three sources × `baseline` or `stone`. Each uses **exactly** B06-EN-02 Soldier, G0 Initiative Scholar before foe, G1 fixed adjacent contact, genuine G3 Stone host (when selected), G4 typed resistance/Armor/Regeneration, G4.5 bridge and G5 sword receipt, fixed attack d20=12, damage d6=5, wound location=8, `take_hit`, 3 full rounds. The Scholar never attacks. The policy is deliberately a **source-native damage/defense comparison**, not a victory scene. Each level's High source uses `SpellState.cast_stone`, Medium the authored MS R1 mode, Low the prepared LS original R2 mode.
3. **28 original Medium/Low tactical self-buff scenes, kept separate**: the prior medium pack uses Soldier d6=**5** and Low pack d6=**6**. Each has 14 separately source-native cases: baseline, Stone, Guided, paid reroute/release+recast, and two L3 temporary amplifications. Source receipts are replayed with the original policy runners; **they must never be pooled with the 18 matched scenes** to rank relative damage/survivability. High has **no matching native Guided or Low/Medium switching profile** and is deliberately absent from these cases.

Existing B06 [High Scholar Fire source](b05-high-scholar-fire-l1-l3-build-verification-v0.md) provides a separate native F Thrown Flame lane in earlier tests, and the High role appears in bounded Hunter policies, but **a complete matched three-Focus outgoing damage/healing/skill encounter does not yet exist**. This audit does not reinterpret unmatched High Flame offense as proof of superiority over currently unsupported native Medium/Low player Sword or Flame attacks.

## 2. Same-stat Focus and source progression

| Measure (actual selected characters) | High F L1 / L2 / L3 | Medium S L1 / L2 / L3 | Low T L1 / L2 / L3 |
|---|---|---|---|
| Max VP at VA0 | **6 / 12 / 18** | **4 / 8 / 12** | **2 / 4 / 6** |
| After a **completed six-hour VP recovery** (half-up 25%, not free on round/turn begin) | **2 / 3 / 5** | **1 / 2 / 3** | **1 / 1 / 2** |
| Turn AP | 30 / 36 / 42 | 30 / 36 / 42 | 30 / 36 / 42 |
| Physical / Projection price | **30 / 20 AP** | **24 / 24 AP** | **20 / 30 AP** |
| Physical Tempo | **1 / 1 / 1** | **1 / 1 / 1** | **1 / 1 / 2** |
| Projection Tempo | **1 / 1 / 2** | **1 / 1 / 1** | **1 / 1 / 1** |
| Natural source-sheet regen at VIT2 | **3 / 3 / 3** | **3 / 3 / 3** | **5 / 5 / 5** |
| Known individual Pillar techniques | **5 / 6 / 6** | **4 / 5 / 5** | **3 / 4 / 4** |
| Prepared selection | High L1 **1** composite formula / L2 **2** / L3 **Formula Fluency** (no prepared-formula requirement) | No general prepared technique subset | Low **2 / 3 / 3** prepared subset of actually known spells |
| Normal source Guard **capacity** | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 2 |
| **Actual equipment Guard usable in the scene** | **None** — F's Dagger is carried, not wielded | Sword **Guard17** | Sword **Guard17** |
| Max HP / Max Vigor | 12 / 12,24,36 | 12 / 12,24,36 | 12 / 12,24,36 |
| Base ordinary movement | 12 MP per turn | 12 MP per turn; L3 MS Overroute imposes 10/8 MP | 12 MP per turn |

The extra Low regeneration is the **canonical Focus rate**, not an automatically bestowed regeneration spell. High/Medium/Low cannot fit a Physical plus Projection action in the same normal 42-AP-or-less turn (respectively **50, 48, 50 AP**). High can project twice at L3 if **both individually legal 20-AP activations** and their VP conditions hold; Low can take two 20-AP physical actions if actually authorized. The audit does **not** award free extra hits or spells solely because the tempo arithmetic permits them.

The High source F knows Conjure Flame and self/composite casting, Low T has a prepared technical subset that **excludes** known Basic Heal at L2/3, and Medium S knows its own authored Inward configurations. There is **no universal Stone equivalence**: each Focus applies its actual, *different* technique/profile price.

## 3. True matched native Stone Skin cost and effect

| Source | Paid activation | Native G3 resistance at actual VC0 | Committed VP L1/L2/L3 | Special constraint |
|---|---|---:|---|---|
| High F, standalone Self | **20 AP** | **R2** | **2/4/6** | Genuine F normal G3 Stone activation; no free dagger Guard |
| Medium S, Body Inward | **24 AP** | **R1** | **1/1/1** | Learned MS mode, may reroute for separate **3/3/2 Spent VP** only under its original legal rules |
| Low T, prepared Self Embodiment | **30 AP** | **R2** | **1/2/2** | Prepared Arsenal; switching requires release **then another paid 30-AP Projection** |

Each choice mitigates only eligible **HP packet types**; it does not automatically prevent Vigor, bypass Armor, authorize Reactive casting, generate a second instance, or confer a Guard. The audit computes **actual signed native HP/Vigor/Step results**, paid Projection actions and VP breakdown after three fixed Soldier strikes; it never fabricates percentage damage reduction or hypothetical resistance ticks. **An original paid Stone host is not guaranteed to remain active until encounter end:** when a Scholar becomes unconscious or dead, G4/G3 can legally end Stone and return its Committed VP. The comparative report authenticates the *original* G3 establishment's actual R and Committed payment **separately from** the terminal host state, end reason, VP refund and final HP. Baseline casts no Stone. A correct audit records whether the source actor **survived or became Dying/dead** under the fixed input, not a guaranteed survival outcome, win rate or generally superior CR.

### Additional tactical policies, not three-way matches

The **28** older native Medium/Low replays attest existing legally paid choices:

- Medium: one MS R1 or Guided +1 on real Step2; paid no-AP reroute of an existing host, L3 up to two Overroute steps costing VP and sacrificing real MP. Initial VP and reroute fees constrain mode changes.
- Low: one *prepared* R2 Stone or real Step2 Guided +1; release plus fresh paid Projection, L3 **+1 R until next own turn** or **+1 on one actual native Step2** for **1 Spent VP**, no double consumption or free HP.

The original Medium/Low demonstrations used different fixed damage faces, so their raw end HP or native restoration must not be compared as equal encounter intensity. Extra Guided throughput is not equivalent to healed HP when Vigor or deficit limits apply. High's normal/composite offensive opportunities are a separate evidence tier, not invented M/L spell engines.

## 4. Assessment and next verification gates

**Current balance verdict: provisional — do not tune Focus rates or spell costs from this sample.**

The matched defensive probe exposes a concrete action/VP/resistance trade-off: High spends a faster action but more ongoing VP, Medium reserves only 1 VP with weaker R and paid tactical rerouting, Low retains R2 with a slow new cast and (at L3) an independently paid transient benefit. Differences in actual source weapon readiness, repertoire, positioning, and how much natural recovery each Focus receives **prevent an unconditional rank ordering**. There are no player attacks in the matched cohort, no random sample, no repeated independent policies across all three Focuses and no statistical win rate.

The following remain **open**, not implicitly certified by this PR: (1) shared three-Focus native **outgoing** attacks, legal equipment/hand profiles and source-policy offense; (2) matched active defense/Guard versus Dodge, Opportunity pressure, position/cover and more enemies; (3) fair tactical decision and mixed-party benchmarks instead of deterministic Take Hit; (4) multi-recipient support and actual bounded six-hour Rest/VP renewal windows; (5) native technical exploration/noncombat scenes, Low preparation timing passage, and high composite precision; (6) independent PS-01–PS-08 role/adventure certification and all MVP exit gates. The 6 structural candidates remain **not** 6 completed adventure-ready Focus certificates, and no numeric calibration or CR policy is authorized.

**Prioritization:** next build a *shared author-approved outgoing offense surface* for S/T and comparable F, then expand common encounter choices and resource attrition before changing core numbers. Weapon-focused Low Scholar and PS-03 must receive **separate explicit** authoring, never derived from a generic Self spell.

## 5. Reproduce

```bash
python -m scripts.b05_scholar_three_focus_comparative_native_audit_v0 --focus High --level 2 --policy stone
python -m scripts.b05_scholar_three_focus_comparative_native_audit_v0
python -m unittest tests.test_b05_scholar_three_focus_comparative_native_audit_v0 -v
python -m unittest discover -s tests -v
```

This is a **comparative source-data and bounded native G0–G5 audit**, not a three-way win-rate or numerical buff/nerf PR. Code review and exact-head Actions are required before merge; branch cleanup must be user-authorized.
