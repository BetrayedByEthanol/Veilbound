# B04/B05 — Medium Scholar L1–3 Character Build and Native Inward Verification v0

> **Bounded native structural verification and genuine Soldier self-defense/Step tests, not an independent full Focus or MVP adventure certificate.** Canonical sources are [Scholar](../rules/08-archetypes/scholar.md), [MS Inward profiles](../rules/07-veil-magic/scholar-inward-embodiment-profiles-v0.md), [Stone Skin](../rules/07-veil-magic/stone-skin-v0.md), [Guided Regeneration](../rules/07-veil-magic/guided-regeneration-v0.md), [12-MP movement](../rules/05-combat/movement-foundation.md), and B04 character creation.

## Source sheet — S Medium Scholar (Earth/Life technical vanguard)

[Audited source sheet](../../scripts/b05_medium_scholar_l1_l3_v0.py) is one **explicitly selected legal build**, not a new Archetype or automatic known-technique list. The native G0 source ID **S** distinguishes it from M Medium **Priest** and F High Scholar.

| Field | Authored choice/evidence |
|---|---|
| Abilities L1–3 | Strength +2; Agility +3; Precision +0; Intellect +0; Awareness +1; Presence −2; Vitality +2; Veil Affinity +0; Veil Control +0 — **28 creation points** |
| Weapon Training | One-Handed Swords +2; **2 weapon development points** |
| Learned disciplines at L1 | Veil Theory +2 and Pillar Lore (Earth) +2 (Scholarly 4); Medicine +2 (Professional 2); Acrobatics +2 (Physical 2), **8 total** |
| L2 discipline award | Navigation +1, rank ceiling respected; no new L3 development point |
| Talents | L1 **TAL-U01 Veil Insight**, Veil Theory +2 prerequisite met; L3 **TAL-C01 Combat Awareness** (+2 Initiative only); no implied magical bonuses |
| Gear | Worn Leather Armor **25 sp**; wielded Sword **22 sp**; Standard adventuring pack **8 sp**; General artisan toolkit **12 sp**. Total **67 sp**, **83 sp** of starting 150 sp unspent; cosmetic clothing free. One actual Sword Guard, no phantom shield |
| Known at L1 | Stone Skin (Earth/Fortification); Guided Regeneration (Life/Restoration); Conjure Flame (Fire/Conflagration); Basic Heal (Life/Restoration); **4/4 individually learned** |
| Known at L2/L3 | Add Minor Telekinesis (Mind/Psionics) at L2; **5/5** at L2/L3. No new L3 learned technique or generic prepared subset |
| Inward modes | Exactly **MS-STONE-BODY-T1** and **MS-GUIDED-REGEN-T1**; one active; no ordinary Self automatic reroute, no Priest Consecration |
| Universals | Veil Inspection L1; Blink L3 **automatically known**, no Scholar slot. At L3 VA0 max VP12 can potentially pay base Blink10 if Available, without pretending the current native encounter implements its use |
| Physical/Projected AP | **24 / 24** AP per action; Turn AP **30 / 36 / 42**, physical/projected tempo **1/1/1** and sword Guard capacity **1/1/1** |
| Resources | Max HP **12**, Max Vigor **12/24/36**, Max VP **4/8/12**, normal native regen throughput **3**, Movement **12 MP** |
| Defense | Sword Guard **17** if actually wielded; Dodge **14**; Initiative **+4/+4/+6**, including L3 Combat Awareness |
| Authority | G0 source ID **S**, SHA of exact build script, original ability/training/equipment snapshots, native VP/AP/Step2 state; **no new native player physical attack profile** is fabricated |

## Native G0/G1/G3/G4 execution

[Medium Scholar native adapter](../../scripts/b05_medium_scholar_native_inward_v0.py) requires one source S, correct ability/source-derived AP and VP and actual installed G1/G3/G4. It never operates on the M Priest or F Scholar actor. [G0 source](../../scripts/b06_encounter_state_v0.py) installs the actor through the same traceable source construction as existing party actors.

1. **Activate Stone Inward**: at a **ready own turn** spend one real **24-AP Projection Action** and **1 Committed VP**, establish **Stone Skin** Self in actual G3 effect registry with **R1** against its eligible Physical/Fire/Electrical HP types. Existing G4 typed HP mitigation reads that resistance; Vigor, other damage types and Armor remain unaffected.
2. **Activate Guided Inward**: same AP/VP payment; genuine G3 **Guided Regeneration** Self host. Its **+1** is included in **the caster's next actual G0/G4 Step 2** throughput only; it is not immediate HP, a second Step or an allied buff. Vigor spent for actual HP restored remains native.
3. **Reroute** only with a live source host, a **different individually learned compatible MS profile**, an open ready own turn, and the entire **3-Spent VP (L1–2) / 2-Spent VP (L3)** fee **plus 1 new Committed VP** independently affordable after the original refund. Old G3 host ends through authoritative release and returns only its **Committed 1**, not earlier Spent VP; the replacement is a new genuine effect with zero extra AP. Same-host refresh and external targets are rejected.
4. **L3 Overroute** on a live host: maximum two steps; **+1 Spent VP per increase** (L3 reroute-into-overroute pays the normal additional 2 Spent reroute fee too). R1→R2→R3 Stone or +1→+2→+3 genuine Guided throughput, in exchange for exactly **−2 ordinary MP per step** from the canonical 12 MP allowance.
5. **G1 movement enforcement**: native G0 sets 12 MP (modified by legitimate impairments), and the adapter reconciles an already-active Overroute at that one real turn resource refresh. Increasing steps later checks **actual remaining native MP before spending VP**, reducing it by 2 per added step; if prior movement consumes too much MP, the overroute **fails before payment/effect mutation**. Dropping to normal only restores previously withheld, unspent MP **during that same own turn**; no old G1 movement receipt is reversed. Movement remains subject to original walls, occupancy, hazards, Cautious costs and triggered Opportunities.
6. **Termination** uses genuine G3 end and VP refund. Stone ends on unconsciousness; Guided only with its original applicable death/release rules. Before either activation or rerouting, compare existing named G3 effects by **recipient as well as caster**: if a Medium Priest (or other original caster) already maintains Guided Regeneration on S, S may not establish another Guided instance and **must not lose AP, VP or its old Inward host** for that invalid declaration. The same recipient exclusivity applies to Stone Skin. The post-commit recheck likewise prevents a newly introduced duplicate. An existing effect on a **different** recipient does not prohibit S's own legal Inward. Existing Priest/High Scholar/Priest Life systems are not remapped.

### L1 VP budget and L3 MP proof

At L1 and VA0, S has **4 VP**: activating Stone costs **1 Committed** then rerouting to Guided costs **3 Spent**, leaving **0 Available / 1 Committed / 3 Spent**, with only 24 AP paid for the initial activation. The next eligible Guided throughput occurs **at the actual next Step 2**, not at the reroute.

At L3, a Stone R1 initial host and two paid Overroute steps use **1 Committed / 2 Spent** from 12 VP. Native G1 movement reduces from **12→8 MP**, allowing up to **four** ordinary orthogonal squares, not two. If an actor has already spent 10 MP, a new two-step Overroute is rejected before the 2-VP payment. Dropping the mode doesn't refund spent VP or walked squares.

## Bounded source-native combat and certification limits

[3-round native Soldier matrix](../../scripts/b05_medium_scholar_native_encounter_v0.py) uses original G5 B06-AT-03 attack declarations against source S, actual G0 Take Hit, fixed 12 d20 / 5 d6 face, native G4 typed HP packet/Armor/resistance handling, one authentic G0 Step2 per round, and the existing G1 map. At each level it tests baseline, Stone, Guided and paid reroute; L3 adds two Overroute effects. This yields **14 deterministic cells**, **not** empirical win rates or CR. Original source ID/digests, all event receipts, HP/Vigor, AP and VP conservation and full ledger digest are retained; reported individual cases can only pass through a **full native replay**, not by rehashing altered user data.

[Regression tests](../../tests/test_b05_medium_scholar_native_inward_v0.py) (including native Medium Priest→Scholar Guided collision in **both** activation and reroute, post-rejection resource/state preservation, and legitimate different-recipient benefits) cover independently sourced legal L1→3 sheets and progression, actual G5+G4 HP resistance, Step-only paid healing, end-of-turn and out-of-turn restrictions, named-effect exclusivity, real native MP conservation, source isolation from Medium Priest, full source replay and invalid decisions. All preexisting B06 profiles and deterministic witness snapshots are preserved.

**Explicitly not certified:** general Scholar ordinary spell use beyond the two authored MS Inward profiles; native S outgoing Sword or Conjure Flame attacks; full player defense policy variation; representative tactical/GM target choices; multiple-foe encounters; native post-combat 6-hour Recovery; noncombat scenario proficiency; independent PS-01 Fighter, PS-02 Defender, PS-03 Spellblade or PS-08 Support role certificates; full Focus balance and numerical tuning. A structurally legal three-level build plus narrowly source-native effects is **not** a complete 3–5-session Focus or MVP certificate.

**Readiness disposition:** this provides the *candidate fifth* structural Archetype × Focus pairing (Scholar Medium) on merge, but keeps **0/12 full end-to-end certificates**, B04/B05/B06/B07 and all six strict MVP exit gates **open**. Subsequent work: Low Scholar L1–3 Native Embodiment source build, broader Scholar medium/low outgoing offense/equipment and noncombat, then independent role/adventure calibration.

### Reproduce

```bash
python -m scripts.b05_medium_scholar_l1_l3_v0
python -m unittest tests.test_b05_medium_scholar_native_inward_v0 -v
python -m unittest discover -s tests -v
python -m scripts.b05_medium_scholar_native_encounter_v0 --level 3 --policy overroute_body
python -m scripts.b05_medium_scholar_native_encounter_v0
```

Code review and **exact-PR-head** CI are required. No ability, technique price, recovery schedule, NPC source or Priest mechanic is rebalanced by this slice.
