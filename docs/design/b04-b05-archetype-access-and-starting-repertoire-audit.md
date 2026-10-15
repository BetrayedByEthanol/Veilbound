# B04/B05 — Archetype Access and Starting Repertoire Audit (15 October 2026)

> **Audit findings, not new player-facing rules.** Baseline: repository `main` **after merged PR #70**. All **eight** selected Pillars have **one** executable Tier-1 representative technique. This audit distinguishes the ability to *choose an Archetype/Focus and perform universal or mundane actions* from an **independently constructible, identity-complete character**. **No unresolved numeric count, Signature, Consecration, Devotional Rite, Conduit Form, Inward Boost, Rider, Access, or Gifted compatibility is invented or unlocked by this audit.** For canonical procedures use the linked rules, not proposed fixes below.

## Scope, evidence, verdicts

Sources: [Character Creation](../rules/02-character-creation/character-creation-foundation.md), [Priest](../rules/08-archetypes/priest.md), [Scholar](../rules/08-archetypes/scholar.md), [Gifted](../rules/08-archetypes/gifted.md), [Anointed](../rules/08-archetypes/anointed.md), [Focus](../rules/09-focus/focus.md), [Universal Veil](../rules/07-veil-magic/universal-veil-fundamentals.md), [Technique Structure](../rules/07-veil-magic/technique-structure-v0.md), [Advancement](../rules/10-advancement/progression-architecture.md), [Eight-Pillar selection and Strong-link construction](b05-eight-pillar-mvp-selection-and-coverage.md), [48 × 8 Gifted compatibility matrix](16-pillar-48-aspect-coverage-compatibility-audit.md), and [MVP blocker register](veilbound-roadmap-and-mvp-readiness.md).

**Audit question:** For **each** of the 12 Archetype × Focus combinations, can a player *now*, using only exact authored permissions, numbers, available spells, and normal L1 actions/resources: (1) make all mandatory creation/access selections; (2) execute the Focus's defining L1 magical loop; (3) fight and contribute outside combat; (4) legally reach L2 and L3 without missing compulsory selections? We distinguish:

- **BASELINE EXECUTABLE:** universal character chassis, equipment, native combat, and individual conditional techniques already have real procedures.
- **CONDITIONAL:** example could operate if an explicitly unresolved number/access selection or available technique were granted; **not a passed full-build test**.
- **BLOCKED:** the defining L1 Archetype × Focus loop cannot be performed from currently authored content/rules, irrespective of whether the character can fight mundanely.
- **PLAYABLE/PASSED:** a complete L1 build plus a verified L1→L3 progression path and defining Archetype/Focus expression. **No combination currently meets this final gate.**

**Verdict:** **0/12 independently certified identity-complete level-1 builds; 0/12 verified level-1→3 walkthroughs.** This is an **evidence/readiness count**, not a declaration that no one can run a provisional character by agreeing to house rules. **B04, B05 and B07 remain MVP blockers.** B06 encounters remain a separate open blocker.

## Shared creation chassis (all 12): substantially executable, but not complete characters

| Shared field | Current authoring status / binding consequence |
|---|---|
| Archetype and Focus | **4 × 3** choices, canonical distinct identities |
| Abilities | **9** scores start −2; spend **28 cumulative points** with normal +4 creation cap |
| Training | **2 Weapon** development points; **8 Learned Discipline** points (default 4/2/2 families or eligible specialization), starting direct-rank cap +2; **2–3 background familiarities**, not general skill bonuses |
| Resonance | Start **0** (not Priest Accord, Gifted emotional intensity, or Anointed Destiny) |
| Core HP / Vigor | At L1, **Max HP = 10 + Vitality**, **Max Vigor = 10 + Vitality** |
| VP by Focus | **High (6 + VA) × level**, **Medium (4 + VA) × level**, **Low (2 + VA) × level**, each uses the canonical `max(1, base + VA)` floor. At L1 and **VA 0**, Max VP = **6 / 4 / 2**; no free VP beyond actual Available balance |
| Turn action economy | **30 / 36 / 42 Turn AP** at L1/L2/L3; Physical Action AP High **30**, Medium **24**, Low **20**; Projection Action AP High **20**, Medium **24**, Low **30**; General Tempo Action **24 AP** |
| L1 Tempo / Guard | Physical Tempo **1**, Projection Tempo **1**, baseline Guard capacity **1** for all Focuses; at L3 High **1/2/1**, Medium **1/1/1**, Low **2/1/2** |
| Starting equipment | **150 sp** mundane purchase budget; ordinary clothing assumed. No free Archetype-specific equipment or free magical items |
| Talent selection | **One provisional L1 Talent choice**; subsequent B07 schedule High **L5**, Medium **L3 and L5**, Low **L2/L3/L5**; exact later balance provisional |
| Universals | **Basic Veil Inspection auto-known L1**; **Blink auto-known L3**; neither uses Pillar slots/links/bond, but both must be paid for normally; other Universal techniques (Veil Analysis, Scrying, Veil Arrow) are **not** executable |
| L3 Blink affordability | Base **10 VP**. At L3 and VA 0, Max VP **18/12/6** (High/Medium/Low), so Low **cannot pay** its base; Low with **VA +2** would have **12 Max VP**, and could potentially fund it if Available, subject to all other requirements |
| Still incomplete | Background/origin subsystem and full derived sheet procedures; **most importantly mandatory Archetype-specific counts, Focus technique compatibility, Signatures**, and L1→3 feature awards |

**Guardrail:** **Technique published ≠ technique automatically known/prepared/accessible.** The exception is the two explicitly level-unlocked Universals. **Focus determines action/VP efficiency, not independent Pillar permission.** Exact Profile/Secondary/Rider names, tags and host permissions matter.

## Tier-1 authored representative technique inventory (not a starter spell list)

| Pillar / Aspect | Authored technique (PR) | What a genuinely eligible L1 user could execute | Limit relevant to build construction |
|---|---|---|---|
| Fire / Conflagration | [Conjure Flame](../rules/07-veil-magic/conjure-flame-v0.md) (#63) | Thrown fire, eligible Reserved Weapon, integrated/prepared physical ammunition | One `Weapon Enchantment` Reserve costs **4 Committed VP at Tier 1**; L1 Low VA0 **Max VP 2 cannot fund that profile**, though 2-VP thrown/shot versions are affordable. **No automatically granted [Embodiment], Devotional Rite, Consecration or Conduit Form compatibility** |
| Life / Restoration | [Basic Heal](../rules/07-veil-magic/basic-heal-v0.md) (#64) | `Self` and `Single Target` healing, **2 Spent VP T1** | Beneficial Intrusion; no persistent Consecration, automatic other-Pillar access or repeatable Rider |
| Mind / Psionics | [Minor Telekinesis](../rules/07-veil-magic/minor-telekinesis-v0.md) (#65) | `Single Object` physical displacement, **2 Spent VP T1** | Not creature-targeted control, sustained Inward Boost, or damage by implication |
| Earth / Fortification | [Stone Skin](../rules/07-veil-magic/stone-skin-v0.md) (#66) | `Self` persistent resistance at **ceil(Max VP/3) Committed VP**; on-turn Projection Action or eligible Reaction | **[Projection] self-Intrusion**, not an automatically authored transferable **Consecration**, **Inward-channel/Routing** or **Devotional Rite** expression. One legal High Scholar `Self` composite with Basic Heal Secondary is specifically authored if both known |
| Liberty / Defiance | [Weaken Restraints](../rules/07-veil-magic/weaken-restraints-v0.md) (#67) | One touched nonmagical restraint weakened, **Full Action + 2 Spent VP T1** | No general traversal, extra free break attempt, Secondary or Rider |
| Kinship / Guardian | [Protective Ward](../rules/07-veil-magic/protective-ward-v0.md) (#68) | **Pre-roll Reaction + 2 Spent VP** protects another ally vs one eligible physical attack | Not self-protection, indefinite Ward Consecration or persistent equipment enchantment |
| Secrets / Hallucination | [Phantom Sound](../rules/07-veil-magic/phantom-sound-v0.md) (#69) | One **1-VP short sound**, or **1-VP integrated arrow/bolt sound** | Not Phantom Image, compelled perception, ongoing Conduit or free melee Rider; no authored Secondary |
| Arts / Inspiration | [Spark of Inspiration](../rules/07-veil-magic/spark-of-inspiration-v0.md) (#70) | One consensual **2-VP +2** to first defined creative/expressive noncombat check | Not universal Performance/Persuasion, combat buff, forced belief or Consecration/Signature |

**Coverage is eight distinct Aspects out of the selected 24 Aspects (one per selected Pillar)**, not an 8×3 tiered catalogue. Tier ceiling permits T2 at L3 but **does not grant a different or unimplemented Tier-2 technique**; some fixed-T1 spells explicitly have no Tier-2 scaling.

## Twelve Archetype × Focus verdict matrix — level 1

| Combination | What is already usable *if legitimate Aspect/technique access is provided* | Critical L1 gap and strict result |
|---|---|---|
| **High Priest** | Chosen-Pillar spell Primary; normal High Projection AP; Prepared Prayers and an Open Invocation **framework** | **CONDITIONAL/BLOCKED:** starting **Accord** and **Prepared Prayer base capacity** undefined; unprepared **Invocation Surcharge** undefined, so cannot reliably pay/open-invoke as fallback. Even a chosen Pillar only has one representative Aspect technique |
| **Medium Priest** | Normal permitted prepared prayers; **1 Active Consecration** and reassignment framework | **BLOCKED:** starting Accord/preparation count missing **and no individually authored eligible Consecration output/recipient/cadence to establish and reassign**. Merely casting Stone Skin on self is not permission to turn it into a distributable blessing |
| **Low Priest** | Ordinary allowed instant prayers, native combat; **Chosen Devotion** commitment discount framework | **BLOCKED:** starting Accord/preparation count and **eligible Devotional Rite** absent. No explicitly compatible **Chosen Devotion** for sustained self/equipment expression, even though individual spells/weapon Reserves exist |
| **High Scholar** | Individually learned cross-Pillar Primary casts; authored **Stone Skin Primary + Basic Heal `Self` Secondary** composite when **both learned and prepared as a formula**, with full VP for both | **CONDITIONAL/BLOCKED:** **L1 known-technique count and prepared composite-formula capacity/count** undefined; no certified starting list or guaranteed legal composite. High VA0 can mechanically fund the example (**2 Committed + 2 Spent = 4 VP** out of 6) **if** the two known/prepared selections are granted |
| **Medium Scholar** | Ordinary individually learned projected spells; **1 Inward Boost** active/channel and 3-VP rerouting framework | **BLOCKED:** **known-technique count** undefined and **no expressly authored Inward Boost/channel profiles with rerouting/Overrouting outputs**. A `Self` label or [Projection] tag alone is not an automatic Inward channel |
| **Low Scholar** | Mundane combat and conditional individually known/prepared spells; **1 Active Embodiment** framework | **BLOCKED:** **known + prepared counts**, explicit eligible **Embodiment configurations** and how selected existing equipment/self effects qualify are not authoritatively instantiated. Conjure Flame's `Weapon Enchantment` is an **equipment-focused candidate, not automatically a granted Low Scholar embodiment**; at L1 Low VA0 its **4 Committed VP** price also exceeds Max VP 2 |
| **High Gifted** | Eight emotion→Aspect links with conditional linked catalogue access; ordinary accessible Tier-1 [Projection] casts when matching emotion is active; **Projected Surge** framework | **CONDITIONAL/BLOCKED:** emotional links are constructible, but **technique-specific Amplification options** and **final Projected Surge surcharge** absent. Can cast an authored linked Primary; cannot certify the defining intensity/surge loop |
| **Medium Gifted** | Eight links; **1 Conduit**, Grades I–III (1/2/3 Committed VP), automatic re-expression and 3-VP Reconduction framework | **BLOCKED:** no **Aspect × Conduit Form × Grade** effects/cadence; most changed Active Emotions leave the Form without an authored output (Dormant). Grade III also consumes **3/4 available VP at L1 Medium VA0** before further actions |
| **Low Gifted** | Eight links; **Anchored Emotion** and Break Anchor (24 AP) framework; native physical actions and conditional linked casts | **BLOCKED:** the chosen Aspect's **persistent self-centered Embodied Expression** is not authored; Anchor alone supplies no defined physical benefit |
| **High Anointed** | One permanent bonded Aspect; full normal bonded-Aspect catalogue access; **0-VP Signature** and projected Authority structure | **BLOCKED:** **birth-imprint-specific High Signature [Signature][Projection] output/action/scaling** and at least one Destiny-priced eligible Authority missing. Bonded Conjure Flame, etc., is executable where chosen; it is **not** automatically a Signature |
| **Medium Anointed** | Bonded Aspect casts; **1 Vessel**, 24-AP establish/change and **0 VP** Investment framework | **BLOCKED:** **Invested Signature expression, valid target/persistence/host interactions, and Authority** absent. A chosen Vessel is not itself a magical effect, and remote range is not granted by the generic framework |
| **Low Anointed** | Bonded Aspect casts, native physical combat; always-available **0-VP Embodied Signature** framework | **BLOCKED:** **self-centered Embodied Signature output/cadence** and compatible Authority are absent; cannot assume a free per-hit magical Rider, extra Guard or movement |

**None is certified as a complete L1 build.** High Priest, High Scholar, High Gifted, and any Anointed with an authored bonded Aspect have meaningful *conditional ordinary spells*, while martial actions and Universal Inspection are shared by everyone. Those are **partial execution paths**, not proof of full Focus identity or valid mandatory starting selections. A specific Pillar/Aspect choice without an authored Tier-1 expression may have **zero accessible Pillar spells** at L1.

## Gifted compatibility: important distinction between two valid constructions

The already merged [B05 selected-roster Strong-only example](b05-eight-pillar-mvp-selection-and-coverage.md#verified-strong-only-gifted-construction-selected-c) has:

| Emotion | Strong linked Aspect | Authored Tier-1 technique? |
|---|---|---|
| Joy | Arts / Inspiration | **Yes** — Spark of Inspiration |
| Sadness | Life / Restoration | **Yes** — Basic Heal |
| Anger | Fire / Conflagration | **Yes** — Conjure Flame |
| Fear | Earth / Fortification | **Yes** — Stone Skin |
| Surprise | Secrets / Hallucination | **Yes** — Phantom Sound |
| Disgust | Liberty / Defiance | **Yes** — Weaken Restraints |
| Trust | Kinship / Guardian | **Yes** — Protective Ward |
| Anticipation | **Mind / Insight** | **No** — there is no authored Mind / Insight spell; existing Mind spell is **Psionics** |

**The eight-Strong validation passes emotion/Pillar compatibility, NOT eight-Spell access.** Do not silently replace Insight with Psionics while keeping an `S` rating: **Mind / Psionics is only P for Anger, Surprise and Trust**, with no Strong compatibility.

**Independently validated eight-authored-Aspect example** (valid under the **existing** locked 48×8 matrix, not a new rule):

| Emotion | Linked authored Aspect | Rating |
|---|---|:---:|
| Joy | **Fire / Conflagration** | **P** |
| Sadness | **Life / Restoration** | **S** |
| Anger | **Mind / Psionics** | **P** |
| Fear | **Earth / Fortification** | **S** |
| Surprise | **Secrets / Hallucination** | **S** |
| Disgust | **Liberty / Defiance** | **S** |
| Trust | **Kinship / Guardian** | **S** |
| Anticipation | **Arts / Inspiration** | **S** |

This table obeys **one link per emotion, eight distinct Pillars, eight distinct Aspects**, using **six S and two P**. For P links, the **player must supply a coherent emotional interpretation at creation**; after that, S and P have the same mechanical strength. Linking all eight does **not** mean all eight can cast in the same Emotion Window or gain a compatible Conduit/Embodied/Amplification output.

**Exhaustive assignment check restricted to these eight exactly authored Aspects:** across all one-to-one emotion assignments using S/P cells, **542** are legal; **0** are entirely Strong; maximum **6 Strong + 2 Plausible**, attained in **24** assignments. Computed from the eight relevant rows of the retained [compatibility matrix](16-pillar-48-aspect-coverage-compatibility-audit.md#exact-gifted-compatibility-matrix--all-48-aspects) by finite backtracking, not a revision of the matrix. The earlier **278 Strong-only matchings** refer to **any appropriate Aspect within each of the eight selected Pillars**, not this narrower eight-authored-technique restriction. Hence **an authored-aspect-only Gifted is possible**, but the published original Strong-only example still needs **Mind / Insight content** to exercise all eight links.

## Numerical affordability and ability-to-act checks (L1; VA 0 unless noted)

| Case | Existing formula → outcome | Verdict |
|---|---|---|
| High/Medium/Low L1 Available VP at full rest | **6/4/2**, normal Projection Action costs **20/24/30 AP** in a **30 AP** turn | One ordinary single cast can fit each Focus's L1 Turn AP, if the spell/target/access/cost is legal |
| Low L1 Conjure Flame Thrown or 1 physical arrow | **2 Spent VP**; full L1 VA0 pool | Affordable **once** on a fully Available 2-VP pool; not a no-cost baseline attack |
| Low L1 Conjure Flame Reserved Weapon | **4 Committed VP > 2 Max VP** | **Cannot establish** at VA0; no discount implicit from being Low Focus |
| Low L1 Stone Skin | **ceil(2/3)=1 Committed VP**, 1 VP still Available | Affordability is positive; **does not by itself authorize** a Devotional Rite, Inward Boost, or Anchored Embodiment |
| Medium L1 Stone Skin | **ceil(4/3)=2 Committed VP**, 2 VP remain Available | Could retain resistance and one 2-VP cast if access actually granted; not Medium Inward rerouting automatically |
| High L1 Stone Skin + Basic Heal composite | **2 Committed + 2 Spent VP = 4**, out of 6 | Mechanically affordable **if** High Scholar knows both and has a valid prepared composite formula |
| Medium Gifted Grade III Conduit | **3 Committed of Max VP 4** before other Spent VP | Numerically affordable with 1 remaining Available, **but no Conduit output yet authored** |
| Level-3 Low Universal Blink, VA0 | **6 Max VP < 10 Spent VP** base | Unaffordable despite automatic knowledge; +2 VA could make it 12 Max VP (other restrictions remain) |
| Projection advantage L3 | High **42 AP / 20 AP = 2 Projection Actions**; Low **42 / 20 = 2 Physical Actions**; Medium **42/24 = 1** of each category in isolation | Focus tempo differences are implemented; this **does not** grant two spell choices, additional technique knowledge, or free amplification |

## Finding register — missing decisions/content, with priority and acceptance tests

| ID | Blocker | Priority | Concrete close-out test |
|---|---|---|---|
| **A01** | Priest L1 Accord value, base **Prepared Prayer counts for High/Medium/Low**, negative-Accord floor and preparation timing/access wording | **MVP blocker** | Choose a Pillar, start with reproducible Accord and enumerate legal prepared prayers without GM-chosen counts; no negative capacity or hidden automatic knowledge |
| **A02** | High Priest L1 **Open Invocation VP surcharge** and affordable fallback | **MVP blocker for High identity** | Test one prepared and one unprepared Tier-1 technique: Full Action (L1–4), normal VP + authored surcharge, and clear insufficient-VP result |
| **A03** | At least one **Prepared Consecration** output with legal one-Pillar/Aspect, target, Committed VP, Continuous/Rider/Pulse, Reassign behavior | **MVP blocker for Medium Priest** | Apply at L1 to recipient A, legally reassign to B for **24 AP**, preserve same technique and actual event/duration; not repurpose a self-only spell |
| **A04** | At least one eligible **Devotional Rite / Chosen Devotion** with self/equipment target, VP commitment and low-Focus affordability | **MVP blocker for Low Priest** | Commit and maintain actual benefit at L1; apply Chosen discount **−1 Committed VP, min 1**; identify future Exaltation property without inventing it at L1 |
| **A05** | Scholar L1 **known-technique counts High/Medium/Low**, Low **prepared subset count**, High L1–2 prepared **composite-formula count/eligibility**, L2 awards | **MVP blocker** | Create cross-Pillar Scholar spell lists independently; optionally use exact `Self` Stone Skin + Basic Heal composite only when both known and properly prepared |
| **A06** | Medium Scholar **authored Inward Boosts** with precise channels, compatibility, Reserve, routing replacement and Overroute output | **MVP blocker for Medium Scholar** | At least **two** differently functional legal boosts in a test repertoire, or explicitly narrow reroute use, then test 3-VP L1 reroute and one active channel |
| **A07** | Low Scholar **which existing prepared self/equipment effects are legal Embodiments**, plus affordable pilot candidate, switching, later Intensification compatibility | **MVP blocker for Low Scholar** | Declare valid prepared active Embodiment at L1 without inferring tags, confirm eligibility/4-VP Fire weapon problem, release/switch paying normal AP/VP |
| **A08** | High Gifted actual **Tier-1 technique-specific Amplification Steps** and Projected Surge surcharge | **MVP blocker for High Gifted identity** | Heighten or Deepen one linked emotion; apply explicit allowed Amplification option and paid/limited Surge on one [Projection] technique without fictitious scaling |
| **A09** | Medium Gifted **Conduit Form × Aspect × Grade** outputs with re-expression/dormancy and cadence | **MVP blocker for Medium Gifted** | Establish Grade I/II/III Conduit, change emotion to one supported and one unsupported Aspect, verify exact effect and Dormant behavior; Reconduction costs 24 AP + 3 Spent VP |
| **A10** | Low Gifted one or more **Aspect-specific Embodied Expressions**, anchored persistence, compatible action integration | **MVP blocker for Low Gifted** | Anchor at combat start, prove one passive/physical effect at L1, Break Anchor for 24 AP, re-establish with authored new Aspect effect |
| **A11** | **Anointed Aspect/Birth-Imprint Signature packages** at L1 (High projected, Medium invested, Low embodied) including **0 VP** activation, action/target, output and cadence | **MVP blocker for all 3 Anointed Focuses** | Same bonded Aspect with meaningful Signature for each Focus; never substitute a regular 2-VP technique for the 0-VP Signature |
| **A12** | Anointed **Tier-1 Aspect Authority options, Destiny cost, legal Signature/host compatibility**, and Medium Vessel details | **MVP blocker for Anointed depth** | Spend Destiny on compatible Signature/Aspect effect; Medium moves one actual Vessel; Low has a legal non-multiplied embodied cadence |
| **A13** | **Pilot scope/access menu** (whether all eight selected Pillars and all 24 Aspects are nominally selectable despite 16 lacking a Tier-1 representative); Gifted **S/P link interpretation** | **MVP blocker to certify unrestricted choice** | Publish legal *pilot* options without rewriting 16-Pillar canon; include the eight-authored Gifted 6S/2P example and mark blank linked Aspects honestly |
| **A14** | Concrete L1 **sheet/feature allocation**, per-Archetype **L2/L3 awards and counts**, background/social adjudication and XP/milestone pilot policy | **MVP blocker B04/B07** | Twelve character records with source-backed choices, actual derived resources, and audited level-up L1→2→3 without invented capacity or signatures |
| **A15** | Empirical **resource and action balance** for low VP, medium reroute/Conduit spending, High composites, Anointed Destiny and healing | **Calibration, after minimum playable slice** | Run short mixed encounters and check ability to perform meaningful Archetype moves and ordinary attacks; adjust only in dedicated balance PR |

**Current blockers share dependencies:** A01–A12 are the **necessary content/numeric authoring**, A13 limits whether arbitrary player Pillar/Aspect choice is feasible, A14 proves integration, A15 is playtest. The audit does **not** lock the proposed numbers or mechanically classify any existing spell as a Consecration/Devotional Rite/Inward Boost/Embodiment/Signature merely because it looks useful.

## Recommended minimal closure plan — make twelve pilot builds without authoring 48 full packages

1. **Lock the pilot selection policy and shared starting quantities (A01/A02/A05/A13).** Keep canonical 16 Pillars/48 Aspects intact; specify a restricted **test-adventure legal menu**, or else accept the much larger authoring burden of unrestricted all-selected-Aspect support. Preserve Priest High > Medium > Low Prepared counts before Accord. Avoid promising Open Invocation on an unaffordable 2-VP Low character.
2. **Author one complete L1 identity-carrying package per Focus family, reused where **canonically compatible**, not by re-labeling spells**: Priest Consecration + Devotional Rite, Scholar 2 Inward-channel functions + eligible Low Embodiment, Gifted amplifications/Conduit/Embodied expressions, Anointed one bonded-Aspect **High/Medium/Low Signature + Authority** vertical slice. Each needs VP, AP, targeting, cadence, expiry, examples and refusal/exclusion rules.
3. **Verify concrete exemplar pilot choices for each Focus across all four Archetypes.** Add one Priest Pillar that supports projected, Consecration and Devotional expressions; Scholar cross-Pillar technical breadth and a meaningful High Composite; Gifted 8 links with representative emotional options and one P interpretation; Anointed a bonded Aspect with all three actual Signatures. More Tier-1/2 spell variety should respond to **specific failed character-role tests**, not arbitrary catalogue quotas.
4. **Build twelve full L1 sheets and advance them through L2/L3 (A14)**, with exact weapons/discipline points, available and committed resources, Turn AP/Guard, prep/repertoire/linked/bonded choices, archetype features, L2/3 Talent awards, VP affordability and Universal Blink. Mark any L3 **Tier-2 ceiling without authored Tier-2 effect** honestly. Record what each character can do in a combat turn and an exploration/social scene.
5. **Build the B06 enemy/encounter slice and playtest (A15).** Do not defer this indefinitely while increasing the spell catalogue; test whether ten-minute Inspiration, 1-VP Phantom Sound, 2-VP utility/healing, Low Focus VP scarcity and 0-VP Anointed Signatures are worth their action and resource costs.

### Formal acceptance gate

**Pass B04/B05 starting-access audit only when:** all **12** pilot builds independently specify mandatory choices **without GM inventions**; each has an eligible, affordable **Archetype/Focus-defining L1 loop** plus ordinary physical combat, at least one useful noncombat contribution, no unauthored Pillar spells under claimed access, and a verified progression L1→3 (B07). This is **not yet passed**. An interim *pilot roster lock* is a scoped **new decision**, not an automatic general change to all player choices.

## Unchanged and explicitly deferred

No change to Volition/Pillar metaphysics, Aspect identities, Gifted matrix S/P values, known/Prepared/linked access ownership, Intrusion versus Manifestation, Reserve semantics, Focus AP, blanket ability checks or underlying eight technique payloads. **Phantom Image**, further 16 selected-Aspect Tier-1 gaps, full repertoire breadth beyond pilot, advanced Conduits/Signatures, 36 specializations, high-level 6–20, full crafting/PWA and comprehensive bestiary stay open or deferred according to their separate priorities. **B06 small enemy pack remains required** even if B04/B05 character content is repaired.
