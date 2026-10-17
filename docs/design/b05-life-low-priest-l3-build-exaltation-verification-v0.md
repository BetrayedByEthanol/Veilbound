# B05 — Level-3 Life Low Priest Builds and Exaltation Verification v0

> **Verification record, 17 October 2026 — two structurally legal Life Low Priest builds, deterministic procedure/ledger tests, NOT end-to-end encounter certification.** Based on merged [PR #80 Devotional Rites](../rules/08-archetypes/priest.md#devotional-rites) and [PR #81 Exaltation](../rules/08-archetypes/low-priest-exaltation-framework-v0.md). All scenario attacks below are **explicit after-mitigation fixtures**, not enemy statistics, attack-roll simulations, automatically occurring threats or measured combat probabilities. **0/12 full archetype/Focus L1–3 certification cases remain independently signed off.** Numerical balance remains provisional.

## 1. Canonical inputs and test boundaries

- **Low Priest / Life:** three Aspects accessible, one chosen-Pillar list; at starting Accord **+1 Stable**, 2 actual Prepared Prayer slots at **L1**, **3 at L2 and L3** (base 1/2/2 plus Accord). One chosen Prepared technique is designated at each legal prayer preparation; precisely **one actual self-maintained Committed-VP Rite** can be active at L1–3, and only the **specifically Chosen instance** may anchor Exaltation. Initial preparations free, later changes need **10 uninterrupted minutes at most once per six elapsed hours**.
- **Level resources:** Low VP = `max(1, 2 + Veil Affinity) × Level`; HP = `10 + Vitality`; Vigor = `(10 + Vitality) × Level`. At L3 Turn AP **42**, Physical Action **20**, Projection Action **30**, General Tempo **24**, physical tempo/ordinary Guard capacity **2**, projection tempo **1**, **12 movement points**. A cast (30) plus an ordinary attack (20) is **illegal in the same ordinary turn**; two physical attacks (40) are legal. A **0-additional-AP expressly authored Exaltation** is not a free spell or a new regeneration turn.
- **Regeneration:** the actual once-per-own-turn Step 2 precedes start hazards, Turn AP establishment and the normal action. Low throughput = `max(Vitality, 0) + 3` plus separately authored modifiers, requiring **1 recipient Vigor per HP or Repair Progress**. Full or extra throughput does not create another Step. Non-Dying may allocate to HP or repairable wounds; Dying uses survival/oldest-blocking-wound order.
- **Level-3 Low Talent selections:** one at L1, one at L2, one at L3, with individual minimum-level gates. Level-2 Learned Discipline progression adds **one point**, not more Weapon Training; no normal Ability advance before L4.
- **Tier and Universal:** at L3 regular normal Used Tier up to **2** when authored for that technique. Universal Inspection L1 and Blink L3 are automatically known but use their full **authored VP/action** prices. Blink's **10 Spent VP** base is **unaffordable at these VA0 L3 Max VP6 snapshots**, even when a valid destination exists. Do not count an unusable unlock as successful Blink.
- **Equipment:** ordinary L1 **150 sp** purchase limit is carried into these unchanged L3 test sheets (no assumed loot). Full, natural VP/Vigor at first setup are **after appropriate elapsed recovery or otherwise legal full-resource initial state**, *not* free restoration granted by leveling.

## 2. Complete mechanical build fixtures

Each nine-Ability allocation spends exactly **28 starting points** (0/1/2/3/5/7/10 total cost for -2/-1/0/+1/+2/+3/+4). Background familiarities are narrative only, not +Training or free contacts.

| Field | A — Restorative Vanguard | B — Preservation Guardian |
|---|---|---|
| Archetype / Focus / Pillar | Priest / Low Embodiment / **Life** | Priest / Low Embodiment / **Life** |
| Ability scores `STR, AGI, PRE, INT, AWA, PRES, VIT, VA, VC` | **+2,+3,0,0,+1,-2,+2,0,0**; cost `5+7+2+2+3+0+5+2+2 = 28` | **+2,+2,0,+1,0,-2,+3,0,0**; cost `5+5+2+3+2+0+7+2+2 = 28` |
| Level-1 Weapon Development | **Sword +2**; spent both points | **Mace +2**; spent both points |
| Level-1 Learned Disciplines (8 points) | Scholarly: **Veil Theory +2, Life Pillar Lore +2** (4); professional **Medicine +2** (2); field **Acrobatics +2** (2) | Professional: **Medicine +2, Herbalism +2** (4); field **Survival +2** (2); scholarly **Life Pillar Lore +2** (2) |
| Level-2 discipline point | **Survival +1** (9 invested total, cap +2) | **Veil Theory +1** (9 invested total, cap +2) |
| Talents by actual award | L1 **TAL-C02 Enhanced Regeneration**, L2 **TAL-C05 Guard Reserve**, L3 **TAL-C10 Emergency Regeneration** | L1 **TAL-C05 Guard Reserve**, L2 **TAL-C01 Combat Awareness**, L3 **TAL-C09 Disengaging Strike** |
| Level-1 Prepared / Chosen | **Guided Regeneration** (Chosen), **Basic Heal** | **Vital Shelter** (Chosen), **Basic Heal** |
| Level-2 additional Prepared | **Woodland Rapport** (Nature), filled at a legal next preparation | **Venom Endurance** (Preservation), filled at a legal next preparation |
| Level-3 Prepared | Same three, no unexplained new slot | Same three, no unexplained new slot |
| Other access | Auto **Inspection** at L1, **Blink** at L3 (presently unaffordable) | Same |
| Purchased L1 gear and retained coins | **Leather 25, sword 22, medical kit 15, adventuring pack 8 =70 sp; 80 sp retained**. Wield sword in one hand, **keep the other hand free** | **Brigandine 95, mace 16, shield 16, medical kit 15, pack 8 =150 sp; 0 retained**. With mace + shield wielded, **no free hand for Basic Heal** |
| Background familiarities (non-numeric) | Home community; prior rural medical practice | Town watch; temple infirmary |

### Derived ledger / martial comparison

| Value | A L1 → L2 → L3 | B L1 → L2 → L3 |
|---|---|---|
| Max HP | **12 → 12 → 12** | **13 → 13 → 13** |
| Max Vigor | **12 → 24 → 36** | **13 → 26 → 39** |
| Max VP (VA0) | **2 → 4 → 6** | **2 → 4 → 6** |
| Turn AP | **30 → 36 → 42** | **30 → 36 → 42** |
| Low Physical / Projection tempo at L3 | **2 / 1** | **2 / 1** |
| Normal own-turn Regeneration throughput at L3 *without Chosen host* | **2 Vitality +3 Focus +1 TAL-C02 = 6** | **3 Vitality +3 Focus = 6** |
| With actively maintained Chosen host | **7** (Guided's +1) | **6** (Vital Shelter never increases regeneration) |
| VP after first successful L3 Chosen maintenance (starting 6 Available) | **5 Available /1 Committed /0 Spent**; Guided cast cost 30 AP | **4 Available /1 Committed /1 Spent**, Shelter budget B=**8** at VC0; cast cost 30 AP |
| VP after first legal Exaltation arm | **4 Available /1 Committed /1 Spent**; must first reach a **later genuine Step 2** with unused throughput | **3 Available /1 Committed /2 Spent**; may arm **on same own turn after casting** with at least budget 2 |
| L3 ordinary sword/mace Attack | **d20+7** (STR2+AGI3+Sword2) | **d20+6** (STR2+AGI2+Mace2) |
| First ordinary Dodge Defense | **14** (AGI3+Awareness1; leather cap4) | **12** (AGI2+Awareness0; brigandine cap2) |
| Guard Defense in specified wielded setup | **17**, sword +2 Training | **18**, shield with mace +2 Training and shield +2 |
| Guard capacity at L3 | **3** (physical tempo2 + TAL-C05 1) | **4** (tempo2 + shield1 + TAL-C05 1) |
| Initiative baseline at L3 | **d20+4** (AGI3+Awareness1) | **d20+4** (AGI2+Awareness0+TAL-C01 2) |
| Vigor / VP completed-six-hour recovery at L3 | **9 Vigor /2 VP** (Max 36/6; half-up) | **10 Vigor /2 VP** (Max39/6; half-up) |

**Hands/access boundary:** Guided Regeneration, Vital Shelter and Venom Endurance explicitly require **no hand components**. **Basic Heal requires one functioning available hand**, so A can cast it while wielding only the sword and preserving the other hand. B **cannot legally cast Basic Heal while both shield and mace occupy their hands**, despite having the technique Prepared, enough VP and 30 AP. B can independently choose a **legal one-free-hand loadout/state** before casting; this audit **does not invent a free mid-turn item swap or an unlisted equipment-action cost**. When B stops wielding the mace, the shield no longer borrows mace Training for its Guard; follow its own +0-Training fallback and equipment capacity rules.

## 3. Timed A fixture — Guided Regeneration + Held Renewal

All actions assume unopposed self-beneficial magic and no interruption, and all named damage is **actual after mitigation**. Start L3 **HP12/12, Vigor36/36, VP A6/C0/S0**, initial max-resource snapshot.

| Step/event | HP | Vigor | VP A/C/S | Check |
|---|---:|---:|---|---|
| Round 1 Step 2, not yet buffed | 12 | 36 | 6/0/0 | Natural throughput6 from VIT2+Low3+C02 1; no recovery needed |
| R1 normal turn: cast **Chosen Guided Regeneration** for 30/42 AP | 12 | 36 | **5/1/0** | Positive maintained self-targeted Rite, no base Spent; **12 AP remain**, not enough for 20-AP weapon Attack |
| R1 after caster's turn: stipulated enemy hit deals **2 HP** | 10 | 36 | 5/1/0 | No Held Renewal is pending; cannot arm after hit/out of turn |
| R2 real Step 2 | 12 | **34** | 5/1/0 | Throughput **7**; heal missing2 for **2 Vigor**; exactly **5 eligible throughput unused** |
| **At end of R2 Step 2**, arm Held Renewal with **2** of 5 unused points | 12 | 34 | **4/1/1** | **1 VP Spent**, 0 extra AP/Reaction; next genuine own Step/initiative exit/host termination expires it |
| Later R2: actual **4 HP** hit | 8 → **10** | **32** | 4/1/1 | Resolve hit to HP8, then automatic Held payout heals2 for **2 Vigor**; no second Step; pending used |
| A separate subsequent R2 confirmed **11 HP** hit, while at HP10 and with Reaction unused | **10→12→1** | **30** | **3/1/2** | **TAL-C10** spends one Reaction, **ceil(2/2)=1 Spent VP**, **2 Vigor** to heal 2 *before* the hit. Without C10: 10−11=−1 (Dying/0-HP wound). With C10: 12−11=1, survives. No free second Held payout |
| R3 genuine Step 2 | **8** | **23** | 3/1/2 | Throughput7 repairs 7 missing HP for 7 Vigor; **0 unused throughput**, so **Held Renewal activation illegal** this Step, even though VP remain |
| R4 Step 2, no intervening injury | **12** | **19** | 3/1/2 | Restore missing4 (4 Vigor), leaving3 genuine unused throughput; Held may again legally arm for **1 Spent** if desired |

**Separate lethal-boundary fixture (reset):** If HP12, Held2 pending, incoming event deals **13 actual HP** after mitigation, resolve HP12→−1 and the first 0-HP wound/Dying procedure before Held payout. Held expires **without any healing**, even with Vigor available. TAL-C10 also cannot preheal when HP was full before that hit. Held Renewal is **not a death-save loophole**. At HP≤−Max HP, death rather than recovery still applies.

**Timing verdict:** A's Guided host activates on R1 normal action **after** Step2, so the first possible Held arm is **R2 Step2**, not R1. Later severe attrition consumes all throughput, making Held Renewal unavailable precisely when the Priest needs large amounts of normal healing. Talent C10 is distinctly **pre-hit Reaction healing**, competes for Spent VP and can avert a lethal crossing when HP is already missing. None of these produces an extra regeneration interval or post-Dying reversal.

## 4. Timed B fixture — Vital Shelter + Vital Interposition

Start L3 **HP13/13, Vigor39/39, VP A6/C0/S0**, VC0, legitimate self-beneficial Chosen maintenance.

| Step/event | HP | Vigor | VP A/C/S | Shelter budget | Check |
|---|---:|---:|---|---:|---|
| R1 Step 2 | 13 | 39 | 6/0/0 | — | Ordinary Low throughput6, no prior regeneration |
| R1 turn: cast Chosen maintained Vital Shelter for 30/42 AP | 13 | 39 | **4/1/1** | **8** | 1 Committed discount +1 **Spent** establishment; 12 AP left, no physical Attack |
| **Same R1 own-turn** after cast: arm EX-LP-01 | 13 | 39 | **3/1/2** | **8** | 1 extra Spent; specific **0-additional-AP own-turn activation** allowed, no new Reaction/action |
| Enemy's later **one venom-coated enchanted piercing hit**: post-native mitigation **1 Piercing HP +2 Fire HP +3 direct Vigor** | **12** | **39** | 3/1/2 | **1** | Aggregate HP3; prevent **2 HP** using budget4, assigning 1 Piercing then 1 Fire: residual **0 Piercing +1 Fire**. No injection from weapon puncture unless independent breach. Ordinary Shelter then absorbs Vigor3 using next budget3; **8→4→1** |
| R2 Step 2 | **13** | **38** | 3/1/2 | 1 | Heal missing1 normally for 1 Vigor; budget **does not refresh** |
| R2 attempt to arm another Vital Interposition | 13 | 38 | 3/1/2 | 1 | **Illegal**: host has fewer than 2 budget points; no Spent VP even though 3 Available |
| Later R2 direct Vigor-damage packet **2**, with Current Vigor positive | 13 | **37** | **4/0/2** | **0 / host ended** | Host absorbs the last **1**, remaining **1 Vigor damage** applies. Original Chosen **1 Committed refunds** to Available, but host establishment and Exaltation Spent VP stay Spent |
| R3 legal fresh Chosen Shelter cast, then fresh EX-LP arm | 13 | 37 | **1/1/4** | **8 new** | New 30 AP cast: from 4/0/2 pay 1 Spent +1 Committed →2/1/3; new 0-AP arm costs 1 more Spent →1/1/4. A new action+real Spent cost, **not** free reservoir refresh |

**Same-hit depletion/provenance alternatives (independent fixture):** On a new full B8 host, physical **Piercing3 + Fire2 + Vigor3** after native mitigation: prevent 2 **Piercing** leaving **Piercing1 + Fire2**; positive puncture may deliver eligible mundane injection toxin through the ordinary source/ward/resistance gate; spend B4 first then absorb the Vigor3 (B1). With only **B4** before the mixed hit, HP prevention consumes it all; the host ends **before** same-hit Vigor3, so those Vigor points are no longer sheltered. Ordinary physical Armor and Fire Resistance are **not** applied twice. A merely remaining Fire HP packet is not a puncture.

**No automatic anti-toxin entitlement:** Vital Interposition protects HP by diverting a real finite host budget; it is **not** Venom Endurance. If injection remains physically valid via positive piercing damage or another established breach, ordinary toxin delivery, nonstack gate, an independently paid applicable ward and natural resistance still apply.

## 5. Additional procedure and resource acceptance cases

| ID | Setup / attempt | Required result |
|---|---|---|
| L3-01 | A has Chosen Guided active, tries to maintain Vital Shelter as second self Rite | **Illegal at L3** before action/VP, even if Available ≥3; releasing the old Rite at legal own-turn point first frees slot but does not make the new technique Chosen |
| L3-02 | B has Chosen Shelter, uses unprepared Guided Regeneration | **Illegal as ordinary Low Priest unprepared Prayer**; neither Open Invocation nor Medium Consecration permitted |
| L3-03 | A maintained Guided on **ally**, or Fixed/Spent mode on self | These are **not Chosen Rites**, no Exaltation, regardless of technique preparation |
| L3-04 | A/B try the *other Aspect's* property | **Illegal** at L3; Living Liturgy is L5+ and requires an authored cross-Aspect compatible host. Guided has no finite shelter budget; Shelter has no Regeneration modifier |
| L3-05 | A release Chosen Guided before the pending Held triggers, or B loses Shelter while Interposition armed | Pending property **expires**. Only actual host Committed VP refund; property Spent VP never refunds and no effect transfers to another Rite |
| L3-06 | A attempts to arm Held at **0 Vigor**, during full regeneration suppression, or with 0 unused throughput | **Illegal/no new held points** (no eligible throughput); no automatic HP recovery/another Step |
| L3-07 | B attempts Interposition before Shelter established, with budget1 at arm, or on ally-targeted non-Rite Shelter | **Illegal**; no reserved generic protection or zero-cost cast |
| L3-08 | B has B1 *after* legally arming when budget≥2 and receives first positive HP event | Armed effect triggers **once**, prevents **0 HP** (insufficient remaining budget) and expires; no created budget |
| L3-09 | B uses shield+mace and declares Basic Heal Self | **Illegal until a functioning hand is available**; the normal no-components rule of Shelter does not carry over to Basic Heal |
| L3-10 | A with Chosen maintenance and at least 2 Available, free hand, 30 AP tries Basic Heal T1 | **Legal** ordinary Prepared Prayer: **2 Spent**, Primary restores **2 HP + 5–7 Vigor** before missing-resource caps; not a Rite or Exaltation |
| L3-11 | B after first cast+arm (Available3) tries Basic Heal at T2 (**4 Spent**) or a 2nd Projection on the cast turn | T2 unaffordable at that resource snapshot; **two Projection Actions cost 60 >42**. T1 may be affordable on a later turn **only when a free hand is truly available** |
| L3-12 | A has chosen maintained Guided active and 4 Available; uses prepared Woodland Rapport **T2** with eligible peaceful 125-kg animal | **4 Spent VP +30 AP** is potentially legal at L3 (actual target/mass/path/animal state required). No extra Rite; no additional attack that turn |
| L3-13 | A/B L3 VA0 attempts normal Blink | **Known** (Universal unlock), but **10 Spent > MaxVP6**, so not currently affordable; no activation/AP/VP paid |
| L3-14 | Priest maintains Chosen Rite while unconscious | Guided/Shelter may persist on caster unconsciousness under their own rules, but **cannot newly activate Exaltation** while unconscious; an already pending property follows its own conditional termination/payout. Held cannot heal if unconscious or HP≤0; Shelter's host may still intercept qualifying Vigor even without new actions |
| L3-15 | A/B have positive Accord +1, query whether it adds to both Exaltation numbers | **No unlisted +1** to 2 held throughput or 2 prevented HP; these properties do not author Accord numerical scaling |
| L3-16 | Two fully prevented HP packets, or one Vigor-only event while B armed | **No HP trigger**; ordinary host budget may still be consumed by Vigor harm; typed damage source/packet identities remain recorded |
| L3-17 | Priests exit initiative with a pending Held / Interposition | Pending property **expires at the authored transition** and does not generate out-of-combat extra turns; its Spent VP remains Spent |
| L3-18 | One attack has Piercing1 + Fire2 after mitigation and B8; compare with Piercing3 + Fire2 | **Primary-first attribution** leaves **Piercing0 Fire1** (not injected) versus **Piercing1 Fire2** (puncture can expose); one event-wide prevention, not two |

## 6. Verification outcome and remaining work

| Gate | Result |
|---|---|
| Complete nine-Abilities, starting allocations, L2 discipline point, talents by level, legal Life preparation | **PASS — two authored L3 build fixtures**; no fictional equipment/Talent/spell grant |
| HP/Vigor/VP progression and initial VP states | **PASS** as conditional full-resource snapshots; **level-up immediate VP-state assignment remains an independent procedure not asserted here** |
| L3 Low Turn AP and ordinary two-attacks-vs-one-cast timing | **PASS**; 42 AP, 20 Physical, 30 Projection |
| One active Chosen Rite, correct VP commitment/Spent separation and upkeep | **PASS** |
| Held Renewal Step-only activation, genuine throughput, Vigor expenditure, nonlethal boundary, TAL-C10 distinction | **PASS procedural fixtures**; first host-cast turn cannot arm |
| Vital Interposition same-turn arming, 2:1 budget conversion, typed injection, mixed Vigor priority, host release/refund | **PASS procedural fixtures** |
| Basic Heal free-hand restriction, ordinary spells, finite budgets, tier price and Blink affordability | **PASS as legal/illegal checks**; rapid equipment-changing action permissions remain outside this slice |
| Numerical balance and subjective choice quality across real combats | **NOT VERIFIED**; only illustrative scripted inputs, not distributional encounter analysis |
| B05 full 1→3 Focus certification, equipment switching, monster opposition, social/exploration scene pack and enemy-stat pacing | **NOT CERTIFIED**; B06 encounter pack and independent build audit still needed |

**Design observations (not canon changes):**
1. **Asymmetric first-use window:** at initiative start Guided must wait until the following own-turn Step 2 to arm Held; Shelter can arm Interposition on the same own turn as its paid Chosen cast. This is a real first-round exposure difference.
2. **Held Renewal is throughput-dependent and fails when fully occupied.** A L3 throughput7 character can hold2 only if **≤5 throughput** was actually used at the Step; severe injury/wounds or 0 Vigor can remove its activation. It adds delayed **up to 2 HP for 1 Spent + up to 2 Vigor**, and only after a *nonlethal* hit. It does not replace the pre-hit lifesaving role of TAL-C10 or general wound repair.
3. **Vital Interposition converts, never adds, protection:** each **2 HP prevented consumes 4 points of the host's original B8**—budget that could otherwise prevent 4 direct Vigor damage. A fresh B8 host can fund **at most two full-strength 2-HP diversions** if no competing Vigor packets, and each costs its own 1 Spent activation at separate legal own-turn opportunities. Its first-hit protection can prevent crossing 0 HP; but host establishment also costs 1 Spent and B can be depleted before use.
4. **Low AP identity is preserved:** both have 2 possible weapon attacks on a purely physical L3 turn, versus 1 paid Projection Action; routine Rite maintenance is action-free. No free turn or repeated spell is created by either Exaltation.
5. **Real competitive costs:** both VP Max6; B spends **2 Spent +1 Committed** to enter its fully armed protective state, leaving3 Available, versus A **1 Spent +1 Committed** only after a later Step, leaving4. The point-in-time comparison is **not a balance verdict**: A additionally supplies passive throughput +1 and may consume Vigor when its held payout succeeds; B has a finite 8-point reservoir and better armor/Guard but fewer post-arm VP and hand constraints.

**Recommendation:** Treat the L3 Low Life **mechanical feasibility/ledger gate as verified in v0 fixtures**, but do **not** increase the global **0/12 independently certified full builds** or change numerical VP, throughput, finite budget, AP or poison rules on the basis of selected scenarios. Next run opposing actual L1–3 stat blocks with a short mixed HP/direct-Vigor/toxin/attrition sequence, and test alternative talent/gear choices plus the B04 equipment-switch policy. Record outcome distributions and actual player action choices before cost tuning.
