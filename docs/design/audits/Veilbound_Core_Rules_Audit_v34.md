# Veilbound Core Rules Audit

## Audit definitions

- **LOCKED** — consistent across the relevant files and sufficiently defined to treat as current canon. This does not necessarily mean final balance.
- **PROVISIONAL** — a usable design exists, but it is explicitly draft/optional, incomplete, balance-dependent, or relies heavily on GM discretion.
- **INHERITED FROM 5e** — Veilbound currently assumes the D&D 5e rule rather than defining its own.
- **CONFLICTING** — two or more files, or two parts of one file, give incompatible rules.
- **MISSING** — a rule required to run the game is not actually defined in these eight files.
- **SUPERSEDED** — the audit finding accurately described the legacy source set, but a later canonical rule now replaces it.

## October 2026 supersession note

This audit records the state of the legacy source set and is no longer itself the source of truth where later canonical files exist.

In particular, the former **"desire / will over faith"** fuel wording is superseded. Current canon defines **Volition as the fundamental force that sustains Pillars; belief gives that Volition meaning and helps stabilize Pillar identity**. See `docs/world/veil-and-pillars.md` and `docs/rules/07-veil-magic/metaphysical-foundation.md`.

Several legacy conflict rows below are marked **SUPERSEDED** where native canonical rules have since resolved them. Pillar communication remains genuinely unresolved.

## Source-of-truth hierarchy

The archive timestamps and contents suggest this practical hierarchy:

| Priority | File | Audit role |
|---|---|---|
| 1 | `veilbound_mechanics.md` (Jan 7) | Latest integrated player-mechanics summary. |
| 1 | `veilbound_talents.md` (Jan 7) | Dedicated martial/Low-Focus subsystem. |
| 1 | `veilbound_gifted.md` (Jan 7) | Dedicated Gifted subsystem. |
| 1 | `veilbound_anointed.md` (Jan 7) | Dedicated Anointed subsystem. |
| 2 | `volition_system.md` (Jan 3) | Explicitly labelled **FINALIZED VP SYSTEM** and reproduced by the Jan 7 mechanics guide. |
| 2 | `veilbound_prestige_classes.md` (Jan 6) | Main source for specialization/mastery/prestige concepts, but still uses legacy `FP` terminology and contains lore/mechanical contradictions. |
| 3 | `veilbound_spells_v1.md` (Jan 6) | Explicit v1 spell matrix; file itself says balance may need adjustment. |
| 3 | `veilbound_rework.md` (Jan 3) | Strongest worldbuilding/lore source, but its mechanical sections contain older versions superseded elsewhere. |

**Practical rule:** treat `veilbound_rework.md` as the lore authority, but do not automatically treat its numerical mechanics as current.

---

## Post-audit locked decisions — Core Resolution & Durability v0

The following decisions were made after reviewing the original eight-file archive. They supersede inherited 5e assumptions in the affected areas. Exact balance values that still require playtesting are marked **PROVISIONAL** rather than silently treated as final.

### Native abilities — **LOCKED**

Veilbound replaces the D&D six-ability chassis with nine direct ability modifiers:

- **Strength** — raw muscular power.
- **Agility** — gross motor control, movement, balance and bodily coordination.
- **Precision** — fine motor control and delicate manipulation.
- **Intellect** — reasoning, memory and learned understanding.
- **Awareness** — observation, instinct and environmental notice.
- **Presence** — social force, self-expression, persuasion and command; physical attractiveness is not folded into this score and may instead be represented by traits.
- **Vitality** — physical resilience and the primary survivability ability.
- **Veil Affinity** — innate relationship with the Veil and magical potential; it is not a substitute for Vitality and does not make a magically gifted character physically durable.

Abilities use their modifier directly rather than a legacy 3–18 score plus derived modifier. The exact creation budget, minimums and maximums remain to be finalized.

### Core action procedure — **LOCKED**

Before rolling, determine whether a roll is needed at all. **Routine or trivial actions that the character can reasonably perform automatically do not require a roll.** Training may also make actions routine for that character that would be uncertain for another.

For uncertain actions:

1. **Passive:** use `10 + Ability + applicable Training + situational modifiers`. This is used for things the character does or notices naturally without deliberately spending time on the task.
2. **Active with sufficient safe time:** the player may roll normally, **Take 10**, or **Take 20** when repeated attempts are possible and failure itself carries no serious consequence. The GM determines how much fictional time Take 10 or Take 20 consumes. Take 20 represents exhaustive effort, not literal guaranteed success.
3. **Active under pressure / limited time:** roll `d20 + Ability + applicable Training + situational modifiers`. No Take 10 or Take 20.

General checks compare against `10 + Difficulty Modifier`. Difficulty is GM-set according to circumstances rather than a fixed property of an object.

| Difficulty | Modifier | Target |
|---|---:|---:|
| Easy under pressure | -3 | 7 |
| Favorable | -1 | 9 |
| Standard | +0 | 10 |
| Challenging | +2 | 12 |
| Hard | +5 | 15 |
| Exceptional | +8 | 18 |
| Extreme | +10 | 20 |

Tasks below this range are normally automatic rather than rolled. Higher targets are possible for genuinely extraordinary circumstances.

### Natural 1 / Natural 20 — **PARTLY LOCKED / PARTLY PROVISIONAL**

**LOCKED:** On an attack roll, a natural 1 is an automatic miss and carries **no inherent fumble or critical-failure effect**. Extra attacks therefore increase offensive opportunity without also making trained characters disproportionately likely to drop weapons, fall over or injure allies. Hazardous circumstances can still have their own consequences, but those are caused by the circumstance rather than by a universal fumble rule.

**PROVISIONAL:** Natural 20s should create a critical opportunity rather than an automatic lethal result. A confirmation-based critical procedure is under consideration, but its exact threshold and severity ladder remain to be finalized alongside weapon damage and wound rules.

For non-combat checks, natural-1/natural-20 handling remains subject to final review; the core no-roll / passive / Take 10 / Take 20 framework does not depend on critical check outcomes.

### Training / skills — **LOCKED**

Training represents specific learned expertise, experience or knowledge. Generic human capability remains on the base ability; Veilbound deliberately avoids broad mandatory umbrella skills such as Perception, Investigation, Athletics, Persuasion, Deception or generic Stealth.

Training scale:

| Training | Bonus |
|---|---:|
| None | +0 |
| Familiar | +1 |
| Trained | +2 |
| Expert | +3 |
| Master | +4 |

The scale is intentionally narrow so specialists are better without creating +20-versus-0 problems or mandatory party roles. A training is not permanently tied to one ability: e.g. Medicine can pair with Intellect for diagnosis and Precision for surgery; Climbing can pair with Strength or Agility depending on the obstacle.

Common training catalogue: **Climbing, Swimming, Acrobatics, Riding, Throwing, Lockwork, Sleight of Hand, Trapwork, Smithing, Carpentry, Tailoring, Engineering, Medicine, Herbalism, Alchemy, Navigation, Tracking, Hunting, Survival, Disguise, Acting, Oratory, Negotiation, Interrogation, cultural Etiquette, Command, Veil Theory, Veil Practice, Pillar Lore, regional/era History, regional Law, regional Politics, Religion & Cults, and profession-specific Trades.** Custom narrow trainings and knowledge fields are explicitly allowed.

Knowledge training may grant information automatically when the character would simply know it; not every use requires a roll.

### Player skill vs character skill — **LOCKED**

Players choose approaches and make decisions; character abilities determine what the character knows, notices, communicates and executes. A clever player may make deductions from clues already available even when playing a low-Intellect character, but information the character would need to know can still require Intellect/training. Conversely, a high-Intellect character may receive deductions or contextual clues that the player personally missed. The same principle applies socially: players need not personally deliver an eloquent speech to use a high-Presence character. Strong or weak approaches primarily alter the situation/difficulty rather than replacing the character's statistics.

### HP / Vigor durability model — **LOCKED concept, PROVISIONAL numbers**

Veilbound separates immediate physical integrity from regenerative reserve:

- **HP** represents current physical integrity. HP does not scale substantially with character level; it is primarily determined by **Vitality**. Being stabbed in the chest or struck in the head remains dangerous at high level.
- **Vigor Points** represent the body's finite Veil-assisted regenerative reserve. Ordinary damage is applied to HP, not to Vigor as a second shield.
- Missing HP naturally regenerates by consuming Vigor. **Vitality determines the regeneration rate** and is intentionally the principal survivability investment.
- Vigor itself returns much more slowly than HP; the exact recovery schedule (full rest / roughly day-scale recovery) is still **PROVISIONAL**.
- Some supernatural attacks may damage Vigor directly, suppress regeneration, reduce Vigor efficiency or otherwise attack the regenerative system rather than HP.
- **Veil Affinity remains a magical-capacity/offense-oriented ability, not a hidden survivability stat.** A Scholar can invest heavily in Veil Affinity and remain physically frail without Vitality.

Exact HP-by-Vitality values, Vigor capacity, HP-per-Vigor conversion, regeneration rates and recovery timing require weapon/damage playtesting and therefore remain **PROVISIONAL**.

### Healing economy — **LOCKED concept, PROVISIONAL costs**

Healing magic distinguishes between two fundamentally different tasks:

- **Restore Vigor:** replenish regenerative reserve; cheaper in VP because the body still performs the physical repair.
- **Restore HP directly:** repair current physical damage immediately; substantially more expensive in VP.

Higher-tier effects may restore both. Serious lasting wounds/structural injuries are a **PROVISIONAL** third layer pending final wound-trigger and treatment rules. Exact VP costs are not locked yet.

---

# 1. World, metaphysics and setting structure

| Rule / concept | Status | Audit finding |
|---|---|---|
| The Veil is a parallel non-physical realm underlying reality | **LOCKED** | Clear and consistent. All magic ultimately originates through the Veil. |
| There are no actual gods | **LOCKED / UPDATED** | Pillars remain emergent rather than creator-deities. Later canon supersedes "accumulated desire" as fuel: Volition is fundamental; belief gives meaning and stability. |
| Volition is the fundamental source of Pillar energy | **SUPERSEDED** | The legacy "will/desire" and "will over faith" wording is replaced by the canonical model: Volition sustains Pillars; desire supplies motive, belief supplies meaning, and will selects/sustains direction. |
| Power rewards internal coherence rather than morality | **LOCKED** | The Veil is morally neutral; conviction and self-consistency matter more than virtue. |
| Pillars are semi-conscious pattern-recognition structures | **LOCKED** | They recognize energy signatures, learn patterns and react instinctively, but do not possess normal human cognition. |
| Pillars cannot directly communicate like gods | **CONFLICTING** | Worldbuilding says they cannot communicate directly, while Oracle/Prophet material refers to divine visions, interpreting Pillar will and speaking for the Pillar. Clarify whether these are inference, symbolic manifestations, or literal communication. |
| Sixteen Pillars | **LOCKED** | Order, Liberty, Life, Death, Fire, Water, Earth, Skywinds, Lightning, Kinship, Strength, Fortune, Mind, Alchemy, Arts, Secrets. |
| Three aspects per Pillar | **LOCKED** | External / Internal / Transform is consistent, producing 48 aspects. |
| Exact 48 aspect names | **LOCKED** | The aspect names are consistent between the mechanics guide, worldbuilding and spell matrix. |
| Pillars can evolve or be absorbed | **LOCKED** | Worldbuilding provides a coherent abstraction/absorption model. |
| Regional Pillar strength is affected by local belief/desire | **LOCKED** as lore | This is repeatedly important to the setting. |
| Mechanical modifier for regional Pillar strength | **MISSING** | No table or procedure determines what “stronger locally” actually changes at the table. |
| Ordinary people may pragmatically engage several Pillars | **LOCKED** | Multi-Pillar everyday practice is explicitly supported. |
| Priest-dominated political systems are the default | **PROVISIONAL** | Strong worldbuilding assumption, but it reads as a broad setting model rather than a fully mapped political canon. |
| Gameplay pillars of the RPG itself | **MISSING** | The files define cosmic Pillars, but not the game’s design pillars such as combat, investigation, social play, exploration, institutional change, etc. |

---

# 2. Character framework and creation

| Rule / concept | Status | Audit finding |
|---|---|---|
| Four archetypes: Priest, Scholar, Gifted, Anointed | **LOCKED** | Their conceptual identities are strong and consistent. |
| Approximate rarity of the four paths | **LOCKED** | Priest ~1/100, Scholar ~1/1,000, Gifted ~1/100,000, Anointed ~1/1,000,000 is repeated. |
| High / Medium / Low Focus | **LOCKED** | Core martial-versus-magical axis. |
| Focus VP multipliers: 1 / 0.75 / 0.5 | **LOCKED** | Present in the finalized/integrated VP system. |
| Martial-Only Focus | **PROVISIONAL** | Appears in character creation, but disappears from the specialization/mastery architecture and “total build options.” It is not developed into a playable path. |
| Native ability chassis | **LOCKED** | Strength, Agility, Precision, Intellect, Awareness, Presence, Vitality, Veil Affinity and Veil Control replace the inherited D&D six-ability chassis. |
| Archetype casting-stat mapping | **SUPERSEDED** | Native canon no longer assigns one mandatory mundane casting stat by Archetype. Individual magical operations author the abilities they actually use. |
| Ability-score generation | **LOCKED** | All nine abilities begin at −2. Character creation uses 28 points with escalating cumulative costs: −2=0, −1=1, 0=2, +1=3, +2=5, +3=7, +4=10. Normal creation cap is +4. |
| Training / skill model | **LOCKED** | Narrow acquired trainings use +0 to +4 and pair situationally with an ability. Generic umbrella skills such as Perception, Investigation, Athletics and Persuasion are deliberately avoided. Custom narrow trainings are allowed. |
| Training bonus progression | **LOCKED** | None +0, Familiar +1, Trained +2, Expert +3, Master +4. This does not use the 5e proficiency bonus. |
| General proficiency bonus | **RETIRED FOR GENERAL CHECKS / CONFLICTING ELSEWHERE** | The native skill engine no longer needs a universal 5e proficiency bonus. Existing VP, spell DC, DP and class features that still use Prof must be redesigned or explicitly retain a separate progression statistic. |
| Starting Resonance by archetype | **LOCKED** | Priest +1, Scholar +1, Gifted 0, Anointed +2 in the integrated guide. |
| Hit points | **LOCKED concept / PROVISIONAL numbers** | HP is physical integrity, scales primarily with Vitality, and should remain approximately fixed across levels rather than increasing every level. Exact values remain to be tuned. Hit Dice are not assumed. |
| Base Armor Class calculation | **INHERITED FROM 5e** | AC is referenced but no native formula exists. |
| Saving throws / defenses | **MISSING / REQUIRES NATIVE REWRITE** | Legacy STR/DEX/CON/WIS/CHA saves no longer fit the new eight-ability chassis. A native defense/save mapping still needs definition. |
| Backgrounds/origins | **MISSING** | No background system, background features, social origin or starting contacts system. |
| Starting equipment packages | **PROVISIONAL** | Focus-level summaries exist, but the mechanics file explicitly points to missing “full equipment tables.” |
| Character creation as a complete executable procedure | **PROVISIONAL / INCOMPLETE** | Native ability allocation and advancement, training, HP/Vigor, and core equipment baselines are defined. Backgrounds, some equipment traits, and derived spell/defense formulas still need completion. |

---

# 3. Core resolution system

| Rule / concept | Status | Audit finding |
|---|---|---|
| General non-combat check formula | **LOCKED** | Active check = `d20 + Ability + applicable Training + situational modifiers` vs `10 + Difficulty Modifier`. |
| Spell attack roll | **INHERITED FROM 5e** | `d20 + proficiency + ability vs AC`. |
| Spell save DC | **INHERITED FROM 5e** | `8 + proficiency + ability`. |
| Advantage / disadvantage | **INHERITED FROM 5e** | Used repeatedly but not defined. |
| General difficulty scale | **LOCKED** | Base 10 with GM-set modifiers: -3 easy under pressure, -1 favorable, +0 standard, +2 challenging, +5 hard, +8 exceptional, +10 extreme. Trivial/routine actions normally require no roll. |
| Natural 1 / Natural 20 outcome rule | **PARTLY LOCKED / PARTLY PROVISIONAL** | **Attacks:** natural 1 is an automatic miss with no inherent fumble. Natural 20 critical handling is still provisional, with confirmation favored over automatic catastrophic injury. **Non-combat checks:** exact natural-1/20 treatment remains to be finalized; ordinary resolution does not require special critical outcomes. |
| Group checks / helping | **MISSING** | Core individual resolution is locked, but cooperative assistance/group-resolution rules still need definition. |
| Extended tasks / progress clocks | **MISSING** | No procedure. |
| When the GM should call for a roll | **LOCKED** | Do not roll for routine/trivial competence. Passive uncertainty uses 10 + modifiers; active tasks with safe time allow roll/Take 10/Take 20; pressured or consequential tasks require a roll. |
| Old freeform “Performing Miracles” procedure | **SUPERSEDED** | The canonical Priest Miracle Petition system replaces the legacy Faith Check/freeform procedure. |

---

# 3A. Durability, regeneration and healing

| Rule / concept | Status | Audit finding |
|---|---|---|
| HP meaning | **LOCKED** | HP represents current physical integrity rather than abstract level-scaled combat luck. |
| HP level scaling | **LOCKED** | HP does not meaningfully increase with level; it is primarily a function of Vitality. |
| Vitality role | **LOCKED** | Vitality is the deliberate core survivability investment: more physical resilience and faster regenerative throughput. |
| Vigor Points | **LOCKED concept** | Vigor is a finite Veil-assisted regenerative reserve, not a second HP shield. |
| Natural regeneration | **LOCKED concept / PROVISIONAL numbers** | Missing HP regenerates over time by consuming Vigor; Vitality controls rate. Exact rate and HP:Vigor conversion remain to be tested. |
| Vigor recovery | **PROVISIONAL** | Vigor replenishes far more slowly than HP regeneration, likely on full-rest/day-scale timing. Exact schedule is not locked. |
| Direct Vigor damage | **LOCKED concept** | Some supernatural attacks may damage Vigor directly or interfere with regeneration without first removing HP. |
| Veil Affinity and durability | **LOCKED** | Veil Affinity does not automatically increase physical durability. It can support magical capacity/offense while the character remains frail without Vitality. |
| Restore Vigor magic | **LOCKED concept / PROVISIONAL costs** | Replenishing Vigor is cheaper than directly repairing HP. |
| Direct HP healing magic | **LOCKED concept / PROVISIONAL costs** | Directly repairing physical damage is a stronger and substantially more VP-expensive healing effect. |
| Wounds / structural trauma | **PROVISIONAL** | A distinct lasting-injury layer is desirable for serious trauma, but triggers, ceilings, penalties and treatment are not yet finalized. |

---

# 4. Volition Points, Resonance and magic economy

| Rule / concept | Status | Audit finding |
|---|---|---|
| VP pool formula | **SUPERSEDED / LOCKED BELOW** | Legacy archetype-constant formulas are retired. Current Max VP is universal by Focus: High `max(1, 6 + Veil Affinity) × Level`, Medium `max(1, 4 + Veil Affinity) × Level`, Low `max(1, 2 + Veil Affinity) × Level`. |
| Archetype constants | **RETIRED** | Max VP no longer uses archetype-specific constants. Archetypes differentiate access, preparation, amplification, routing, reliability and special VP interactions instead. |
| Spell cost formula | **LOCKED** | `0.75 × spell level²`, rounded: 1/3/7/12/19/27/37/48/61. |
| Cantrips cost 0 VP | **LOCKED** | Present in integrated mechanics. |
| Focus determines VP pool | **LOCKED** | Focus, Veil Affinity and level determine Max VP directly: High `(6+VA)×Level`, Medium `(4+VA)×Level`, Low `(2+VA)×Level`, each with a minimum coefficient of 1. |
| VP recovery on long/short/Faith Rest | **RETIRED / SUPERSEDED** | VP now recovers by completed 6-hour elapsed-time intervals at 25% Max VP per interval. Faith Rest does not reset VP or Resonance. |
| Resonance scale −3 to +3 | **LOCKED** | Core concept and labels are stable. |
| Priest Resonance cost modifier | **RETIRED / SUPERSEDED** | Priest Resonance no longer changes general VP costs. Positive Resonance instead expands prepared access, enables Miracle Petition access, and grants a small final-effect bonus up to +3. |
| Gifted Resonance does not alter VP costs | **LOCKED** | Repeated consistently; Resonance changes control/risk instead. |
| Priest Resonance inversion-risk percentages | **RETIRED** | Percentage inversion risk and automatic universal inversion are not part of the current Priest Resonance foundation. |
| Priest Resonance change through play | **LOCKED CONCEPT / PROCEDURE PROVISIONAL** | Resonance is slow-moving and reflects sustained coherence between genuine belief, intention, action and the chosen Pillar. Exact adjudication cadence remains to be formalized. |
| Spell levels 0–9 | **INHERITED FROM 5e** | Veilbound adopts the 5e spell-tier scale. |
| Spell-level access by character level and Focus | **MISSING** | Critical gap: there is no complete table saying when High/Medium/Low Focus gains access to 1st–9th-level magic. |
| Ritual casting | **PROVISIONAL** | Integrated rule says 10 minutes and half VP, but it is unclear who can ritual-cast and how this interacts with Scholar’s supposedly unique Ritual Mastery. |
| Concentration | **INHERITED FROM 5e** | The mechanics guide explicitly says “Standard 5e rules apply.” |
| Spell attack/save targeting, ranges and durations | **INHERITED FROM 5e** | Most spell entries are names rather than complete Veilbound stat blocks. |

---

# 5. Priest

| Rule / concept | Status | Audit finding |
|---|---|---|
| Prayer/volition as casting method | **LOCKED** | Strong thematic identity. |
| One primary Pillar, access to all three aspects | **LOCKED** | Consistent. |
| No normal “spells known” limit within primary Pillar | **LOCKED** | Priests pray for any available spell from their Pillar. |
| Allied Pillar Initiate | **PROVISIONAL** | A level-3 rule and later spell gains are given, but allied-Pillar relationships and eligibility are not defined. |
| Divine Sense | **PROVISIONAL** | Functional draft exists. |
| Channel Divinity | **PROVISIONAL** | Resource exists, but only an Order example is given; complete Pillar-specific effects are absent. |
| Regional Influence | **MISSING** mechanically | Stated as a Priest feature, but there is no procedure for strengthening a Pillar over time. |
| Conviction/hypocrisy mechanically affecting power | **LOCKED** concept | Implemented mainly through Resonance, though the exact Resonance-change procedure remains provisional. |

---

# 6. Scholar

| Rule / concept | Status | Audit finding |
|---|---|---|
| Technical/ritual casting rather than prayer | **LOCKED** | Strong identity. |
| Potential access to any Pillar/aspect | **LOCKED** | Core Scholar advantage. |
| Limited learned ritual/spell selection | **LOCKED** concept | Repeated, but the actual quantity is not given. |
| Number of spells/rituals known | **MISSING** | No progression table. |
| Learning-time rules | **PROVISIONAL** | Older worldbuilding gives Resonance-dependent day ranges, but integrated mechanics do not formalize them. |
| Researching/creating new spells | **PROVISIONAL** | Feature is stated without a complete procedure, cost, difficulty or balance method. |
| Ritual Mastery | **PROVISIONAL** | Needs reconciliation with the generic ritual rule available in the mechanics guide. |

---

# 7. Gifted

| Rule / concept | Status | Audit finding |
|---|---|---|
| Emotion-linked natural magic | **LOCKED** | This is one of the strongest archetype identities. |
| Eight core emotions | **LOCKED** | Joy, sadness, anger, fear, surprise, disgust, trust, anticipation. |
| Number/permanence of emotion-aspect links | **SUPERSEDED** | Canonical Gifted rules use exactly **8 permanent emotion-to-Aspect links**, fixed at birth. |
| Natural vs invoked emotion casting | **LOCKED** concept | Both are consistently distinguished. |
| Intentional casting-check DCs | **PROVISIONAL** | A DC-by-Resonance table exists, but the exact roll formula is not cleanly stated in the integrated mechanics. |
| Accidental manifestation trigger from overwhelming emotion | **PROVISIONAL** | Detailed and usable, but heavily GM-discretionary. |
| Emotional Stability Check | **SUPERSEDED** | Replaced by the current Gifted Emotion Establishment / Deepen Emotion / Instability procedures using universal Resonance where explicitly stated. |
| d100 manifestation table | **SUPERSEDED** | The legacy d100 manifestation table is not part of the current Gifted foundation. |
| Low-Focus Gifted `+20 = safer` interaction | **SUPERSEDED** | Retired with the legacy d100 manifestation table. |
| Suppression / Redirection / Grounding | **PROVISIONAL** | Detailed subsystem, but not yet integrated into the base level progression. |
| Complex-emotion fusion | **PROVISIONAL** | Explicitly an advanced, GM-creative rule. |
| Voluntary emotional overload | **PROVISIONAL** | Playable draft, but depends on fixing the manifestation-table direction first. |

---

# 8. Anointed

| Rule / concept | Status | Audit finding |
|---|---|---|
| Born during a Pillar surge | **LOCKED** in core lore | Repeated in mechanics/worldbuilding. |
| One aspect permanently | **LOCKED** | Strong defining limitation. |
| Mission-bound identity | **LOCKED** concept | Mission is central to Anointed design. |
| Infinite 0-VP Signature Miracle | **LOCKED** concept | Core Anointed identity. |
| Destiny Point pool = Proficiency Bonus | **LOCKED** | Dedicated and integrated files agree. |
| DP recovery from mission progress | **PROVISIONAL** | Entirely milestone/GM-discretion based. |
| Signature base scaling | **PROVISIONAL** | Dedicated file gives a complete draft, but it is not demonstrated for all 48 aspects and has not been balance-validated. |
| DP enhancement list/costs | **SUPERSEDED** | Current Anointed canon uses Destiny and Aspect Authority rather than the conflicting legacy DP enhancement lists. |
| Secondary miracles cost +50% VP | **PROVISIONAL** | Defined only in the dedicated file. |
| Falling/abandoning mission | **PROVISIONAL** | “Lose all powers permanently”/must start a new path is dramatic but lacks formal triggers and recovery/exception rules. |
| Anointed can be gained later through prestige | **SUPERSEDED** | Current Anointed canon states that Anointed are born during a Pillar surge and are not later granted the Archetype by ordinary training. Separate multi-pathing rules remain future work. |

---

# 9. Spell catalogue

| Rule / concept | Status | Audit finding |
|---|---|---|
| 48 aspects × 10 spell tiers | **PROVISIONAL** | The matrix is complete structurally but is explicitly `v1` and says balance may need review. |
| Cross-Pillar spell duplication | **PROVISIONAL** | Deliberate and often thematically sensible, but needs systematic review. |
| Most named spells | **INHERITED FROM 5e** | Fireball, Haste, Wish, Counterspell, etc. require the 5e spell definitions to function. |
| Veilbound-original spell names | **MISSING** mechanically | Names such as Word of Balance, Endless Horizon, Crown of Continuance, The Living Forge, Eternal Accord, Veilbreaker's Will, Chronicle of Fortune, Veil Unwoven, Soul Crucible, Mirror of Creation, Dream of Secrets, etc. do not have full spell stat blocks here. |
| Spell availability per archetype | **PROVISIONAL** | Priest/Scholar/Gifted/Anointed access philosophies are defined, but exact acquisition limits are not. |
| Maximum spell tier per Focus and level | **MISSING** | This prevents the matrix from functioning as a complete player progression system. |

---

# 10. Combat engine

## Core defensive response model — **LOCKED**

Against an incoming attack, the defender chooses one of only **three core responses**:

1. **Take Hit** — The defender does not actively avoid or stop the attack. The attack lands unless the attacker rolls a natural 1. There is no passive Evasion score that can make an undefended target mysteriously hard to hit.
2. **Dodge** — The defender actively moves out of the attack. Dodge is not usage-limited, but each Dodge chosen during the same round adds **Dodge Pressure**, making later Dodges progressively worse. Only choosing Dodge increments this counter; taking a hit or using Guard does not. Dodge Pressure resets for the next round. Exact numerical degradation remains provisional pending combat simulation.
3. **Guard** — The defender actively stops or redirects the attack with a weapon, shield or other appropriate equipment. Guard combines the previous Parry/Block concepts into one limited defensive resource/action. Guard capacity and effectiveness can be improved by equipment, training, level and inward Veil development. Shields should make Guard easier and/or increase Guard capacity rather than creating an entirely separate defense subsystem.

**LOCKED simplifications:**

- **Riposte** is not a fourth defensive response; it can be a follow-up triggered by a successful Guard when equipment/build rules allow it.
- **Intercept** is not a separate subsystem; protecting an adjacent ally can consume/use Guard.
- Repeated incoming attacks do **not** automatically reduce defense. Only repeated chosen Dodges create Dodge Pressure.
- Low-Focus inward development can improve Guard capacity, Dodge effectiveness or similar fundamentals without adding bespoke martial techniques.
- Medium Focus may temporarily improve those same fundamentals through VP-powered inward routing.

| Rule / concept | Status | Audit finding |
|---|---|---|
| Action economy | **LOCKED FOUNDATION** | Turn AP, Focus-based Physical/Projection/General costs, Full Actions, Reactions, Interception, Opportunity Response, ordinary Movement Points, Sprint, terrain costs, movement impairments, and Prone/Crawl/Stand movement now have native Veilbound procedures. Other specialized movement/action content remains later work. |
| Attack action and weapon attacks | **PROVISIONAL / REQUIRES NATIVE MATH** | Universal physical Attack remains a core action. A two-ability attack formula is favored conceptually, but exact ability pairings, training contribution and attack-quality thresholds are not yet locked. |
| Initiative | **LOCKED NATIVE SYSTEM** | Initiative, ties, late entry, round refresh, and turn timing are defined in the canonical Initiative and Round/Turn Procedure. |
| Movement, reach and opportunity attacks | **LOCKED FOUNDATION / SOME SPECIAL MODES PENDING** | Native 12-MP grid movement, orthogonal/diagonal costs, split movement, segments, Cautious Movement, occupancy, blocked corners, adjacent Melee Reach, threatened space, Movement Opportunities, Movement Interception, Sprint, terrain surcharges, movement impairments, allied-square transit, and Prone/Crawl/Stand movement are defined. Charge, climbing, swimming, jumping/falling, squeezing, size exceptions, flight, and final weapon Reach assignments remain pending. |
| Damage / durability | **PARTLY LOCKED, PARTLY MISSING** | Damage normally reduces physical HP. Vigor is a regenerative reserve rather than temporary HP; some supernatural effects may target Vigor directly. Resistance/immunity categories still need native definitions. |
| Conditions: frightened, stunned, blinded, prone, paralyzed, charmed, etc. | **PARTLY NATIVE / MOSTLY UNRESOLVED** | Prone now has native movement consequences (Crawl/Stand/Sprint restriction), but its attack/Guard/Dodge effects and the other named conditions still require a Veilbound-native conditions appendix. |
| Exhaustion | **INHERITED FROM 5e** | Used as a capstone cost, but version/effects are not specified. |
| Critical-hit core rule | **LOCKED FRAMEWORK / DAMAGE BONUS PENDING** | Natural 1 is an automatic miss without fumble. Natural 20 creates a confirmation-based critical opportunity; a second natural 20 creates a Devastating Critical. Exact Strong Hit/Critical damage bonuses remain to be calibrated. |
| Low-Focus Extra Attack progression | **SUPERSEDED** | Replaced by canonical Physical Tempo formulas and the current Focus/level cadence. |
| Medium-Focus attack progression | **PROVISIONAL** | Baseline is 2 attacks from level 5, but specific specializations/masteries can increase it. Needs a single progression table. |
| Fighting Styles | **INHERITED FROM 5e** | Mostly direct 5e Fighting Styles with minor additions. |
| Superiority Dice / Combat Talents | **PROVISIONAL**, 5e-derived | A detailed system exists, but much is adapted directly from Battle Master mechanics and has not been integrated across all Focus paths. |
| Low-Focus critical-range improvement | **PROVISIONAL** | 19–20 at level 9 is clear in the martial file, but later masteries introduce other overlapping critical-range rules. |
| Exotic weapons | **PROVISIONAL** | The list mostly contains weapons that are ordinary 5e martial weapons; the category needs a Veilbound-specific weapon taxonomy. |
| Weapon/armor properties | **PARTLY LOCKED NATIVE SYSTEM** | Damage, Penetration, Armor reduction, Dodge Agility caps and the Two-Handed trait now have native Veilbound rules. Reach, shield numbers, dual wielding and some weapon-specific traits remain to be finalized. |
| Dropping to 0 HP / dying / death | **LOCKED FRAMEWORK** | At 0 HP the character is normally unconscious and Dying, loses 1 HP/round, and dies at −Max HP unless an applicable effect intervenes. Wound repair and Cheat Death rules are defined below. |
| Natural healing / regeneration | **LOCKED concept / PROVISIONAL numbers** | Missing HP regenerates by consuming Vigor at a Vitality-driven rate. Vigor recovers much more slowly. Exact timing, capacity and conversion require playtesting; Hit Dice are not assumed. |
| Cover, concealment, surprise, grappling, shoving | **PARTLY NATIVE / PARTLY MISSING** | Grapple, shove, feint and similar physically plausible maneuvers are intended as universal core actions rather than class techniques. Exact procedures plus cover/concealment/surprise still need definition. |
| Encounter building / enemy challenge rules | **MISSING** | No CR-equivalent, encounter budget or balancing method. |
| Creature/NPC combat stat construction | **MISSING** | No bestiary or NPC builder. |

---

# 11. Advancement, specializations and multiclassing

| Rule / concept | Status | Audit finding |
|---|---|---|
| Levels 1–20 | **INHERITED FROM 5e** scale | Veilbound builds its progression on the 20-level chassis. |
| Foundation 1–5 / Specialization 6–15 / Mastery 16–20 | **LOCKED** | Repeated consistently and gives Veilbound a strong progression identity. |
| 36 specialization names/roles | **LOCKED** as architecture | The 4 × 3 × 3 matrix is stable. |
| Specialization feature schedule 6/7/11/15 | **LOCKED** | Clearly defined. |
| Full mechanics for all 36 specializations | **MISSING** | Most are names/themes only; War Chanter and a handful of concepts are the main worked examples. |
| 12 mastery identities | **LOCKED** as architecture | 4 archetypes × 3 Focus levels. |
| Mastery mechanical implementations | **PROVISIONAL / CONFLICTING** | Many exist in `veilbound_prestige_classes.md`, but they use legacy FP terminology and conflict with martial progression and newer subsystem details. |
| 18 hybrid Prestige Classes | **PROVISIONAL** | Strong conceptual matrix, only one substantial worked progression. |
| Prestige entry: 5 levels in each of two archetypes | **PROVISIONAL** | A rule exists, but no complete multiclass system establishes how levels, VP, Focus, spell progression or innate archetypes combine. |
| Multiclassing generally | **MISSING** | Worldbuilding says multi-pathing is possible, but mechanical rules are not complete. |
| Priest+Anointed / Gifted+Anointed acquisition logic | **CONFLICTING** | Some prestige concepts contradict “Anointed are born, not made.” |
| Ability Score Improvements | **LOCKED** | At levels 4, 8, 12, 16 and 20, increase one ability of choice by +1, to a normal permanent natural cap of +5. No special negative-score catch-up bonus. |
| Feats | **MISSING** | No feat system. |
| XP or milestone advancement | **MISSING** | No rule for gaining levels. |

---

# 12. Equipment, economy and crafting

| Rule / concept | Status | Audit finding |
|---|---|---|
| Complete mundane weapon table | **PROVISIONAL BASELINE ESTABLISHED** | Core damage/Penetration profiles are now calibrated for dagger, rapier, sword, spear, axe, mace, greatsword, bow and heavy crossbow. Additional weapon families and special traits remain to be added. |
| Complete armor/shield table | **PROVISIONAL BASELINE ESTABLISHED** | Armor ratings and Dodge Agility caps are now calibrated for the core armor roster. Coverage, shield values, rune-capacity numbers and several traits remain to be finalized. |
| Adventuring equipment | **MISSING** | Packs are named but not defined. |
| Starting money | **PROVISIONAL / 5e-derived** | Uses `gp`; the setting economy/currency is not otherwise established. |
| Item prices and availability | **MISSING** | No functioning market/economy rules. |
| Magic items / relics | **MISSING** | Mentioned conceptually but no catalogue/system. |
| Crafting | **MISSING** | Forge/Alchemy aspects imply crafting, but there is no actual crafting procedure. |
| Encumbrance / carrying capacity | **MISSING** | No rule. |
| Consumables, ammunition and supplies | **MISSING** | No system. |

---

# 13. Non-combat play

| Rule / concept | Status | Audit finding |
|---|---|---|
| Basic social interaction resolution | **LOCKED at core-check level** | Ordinary social execution uses Presence plus applicable narrow training against the standard difficulty system. Player approach changes circumstances/difficulty. Extended social conflicts remain undeveloped. |
| Basic investigation resolution | **LOCKED at core-check level** | Observation defaults to Awareness; reasoning/interpretation defaults to Intellect; specialized knowledge/training applies when relevant. There is deliberately no generic Investigation or Perception skill. Extended clue/progress procedures remain undeveloped. |
| Exploration | **MISSING** | No travel, navigation, discovery, hazard or expedition procedure. |
| Basic stealth resolution | **LOCKED at core-check level** | Ordinary quiet movement uses Agility. Narrow context-specific training may apply, but there is deliberately no mandatory generic Stealth skill. Detection/opposed procedures still need formalization. |
| Downtime | **MISSING** | No framework. |
| Craft/research projects | **MISSING** | Scholar research is conceptual only. |
| Faction/influence rules | **MISSING** | Setting strongly supports them, but none exist mechanically. |
| Settlement/institutional change | **MISSING** | No rules for the political/resource consequences that the setting is well suited to model. |
| Extended social/investigation conflicts | **MISSING** | No progress tracks, clocks or opposed influence systems. |

---

# 14. GM-facing rules

| Rule / concept | Status | Audit finding |
|---|---|---|
| Gifted emotional-intensity guidance | **PROVISIONAL** | Useful and fairly detailed. |
| Anointed mission/DP milestone guidance | **PROVISIONAL** | Useful, but strongly dependent on GM discretion. |
| General difficulty-setting guidance | **LOCKED** | Difficulty is `10 + GM-set modifier` using the native difficulty ladder; circumstances and player approach modify task difficulty. |
| General adjudication/when-to-roll guidance | **LOCKED** | Routine competence is automatic; passive uncertainty uses 10 + modifiers; active safe-time actions allow roll/Take 10/Take 20; pressured/consequential actions require the d20. |
| Regional Pillar-state tracking | **MISSING** | Important world concept has no quantitative or qualitative GM system. |
| NPC creation | **MISSING** | No template. |
| Monster/bestiary creation | **MISSING** | No template. |
| Encounter design | **MISSING** | No budget or difficulty system. |
| Treasure/reward generation | **MISSING** | No procedure. |
| Campaign/faction/settlement clocks | **MISSING** | Nothing yet converts Veilbound’s institutional themes into campaign mechanics. |

---

# Audit items resolved by Core Resolution & Durability v0

The following original audit findings are no longer open design gaps:

- The inherited D&D six-ability chassis is replaced by the nine native Veilbound abilities.
- The generic 5e skill/proficiency model is replaced by narrow +0…+4 training.
- Generic Perception, Investigation, Athletics, Persuasion, Deception and Stealth skills are deliberately not part of the core model.
- General non-combat check math is now native Veilbound.
- The general difficulty ladder and GM when-to-roll procedure are defined.
- Passive checks, Take 10 and Take 20 are defined.
- Natural 1/20 behavior on ability checks is defined as worst/best plausible outcome.
- HP is no longer assumed to scale by level or use a 5e Hit-Die model.
- Vitality is the central survivability ability.
- Vigor is established as regenerative reserve, with direct Vigor attacks and separate HP/Vigor healing as valid design spaces.

These decisions do **not** yet resolve combat defenses, spell attack/save math, the remaining uses of 5e Proficiency Bonus, or exact durability numbers.

# Major conflicts that should be resolved first

1. **VP formula:** linear old formula vs finalized squared formula. Adopt the squared formula unless deliberately reopening the VP economy.
2. **Gifted constant:** old 2× vs current 4×. Current 4× is supported by the finalized and integrated files.
3. **VP recovery:** old one-hour full Faith Rest vs newer long/short/10-minute Faith Rest model.
4. **Resonance VP modifiers:** old fixed modifiers vs newer spell-level-scaled modifiers.
5. **Gifted manifestation-table direction:** high Resonance currently mathematically makes the d100 result worse despite text saying the opposite. Reverse the modifier signs or reverse the table ordering.
6. **Gifted emotion links:** eight permanent links at creation vs variable/unlockable links.
7. **Anointed DP enhancements:** integrated summary and dedicated Anointed document use different lists and costs.
8. **Low-Focus attack progression:** 3 attacks at level 11/4 at 17 in the martial file conflicts with mastery text saying 3 at 18.
9. **Anointed origin:** birth-only lore conflicts with prestige paths that can apparently become Anointed later.
10. **Direct Pillar communication:** Pillars cannot directly communicate, yet Oracle/Prophet descriptions imply visions or communicated will.
11. **Freeform miracle resolution:** old Faith Checks conflict with the newer spell-casting model unless explicitly retained as a separate improvisation rule.
12. **FP vs VP terminology:** prestige/mastery material still uses legacy `FP`; all current rules should use `VP` if FP is obsolete.

# Strong canonical candidates

These are not new design decisions; they are the versions most strongly supported by the existing files:

| Question | Strong candidate |
|---|---|
| VP pool | **SUPERSEDED:** universal Focus-based Max VP formula is locked in the post-audit rules. |
| Constants | **RETIRED:** no archetype-specific Max VP constants. |
| Focus scaling | **LOCKED:** High `max(1,6+VA)×Level`; Medium `max(1,4+VA)×Level`; Low `max(1,2+VA)×Level`. |
| Spell cost | `0.75 × spell level²`, rounded |
| Resonance | −3 to +3 universal scale |
| Priest spell-cost Resonance modifier | **RETIRED:** Priest Resonance now modifies preparation, Miracle access and small final-effect potency instead of global VP cost. |
| Gifted cost interaction | Resonance changes risk, never VP cost |
| Gifted link model | Eight permanent core-emotion/aspect links at creation |
| Low-Focus attacks | Dedicated martial progression: 2 at 5, 3 at 11, 4 at 17; rewrite later mastery text around this baseline |
| Anointed core | One aspect, mission and infinite signature are strong candidates; DP tied to legacy Proficiency Bonus now requires a native replacement. |
| Anointed enhancement rules | Use the dedicated Anointed subsystem as the baseline and remove the older summary table after review |
| Character progression | Foundation 1–5, Specialization 6–15, Mastery 16–20 |


# LOCKED — Focus as Veil Expression

Focus no longer means simply **caster / hybrid / martial**. It defines **where a character's growing relationship with the Veil is expressed**. Level represents deeper integration with the Veil; Focus determines the direction that integration takes.

| Focus | Core expression | Advancement character | Combat experience |
|---|---|---|---|
| **Low — Embodiment** | Veil power is primarily turned inward and becomes persistent bodily reinforcement. | Mostly passive/inherent developments selected while leveling. | Lower turn-by-turn complexity, more reliance on core combat actions and repeated dice resolution. |
| **Medium — Routing** | Veil power is actively redirected between the body, equipment and outward spell effects. | Temporary inward enhancements plus a limited projected spell toolkit, competing for the same VP resource. | Timing/resource-management play: decide when to enhance, reposition, defend or cast. |
| **High — Projection** | Veil power is primarily shaped outward into spells and external manifestations. | Broader and stronger projected magic, spell selection and spell modification. | Highest action-selection burden; success depends heavily on choosing the appropriate spell/effect and managing VP. |

## Low Focus — Embodiment

**LOCKED:** Low-Focus advancement should primarily modify the character **passively or persistently**, rather than adding an action bar of activated combat techniques. Typical developments may improve such things as:

- sustained Vigor and regeneration;
- reflex speed;
- physical force and movement;
- wound resistance;
- additional attacks or reactions where justified by increased speed;
- efficiency of ordinary core combat actions.

These developments do **not** create special martial techniques. If a mundane action is physically possible, it belongs to the core combat system and can be attempted by anyone under the appropriate rules. Leveling may make the character faster, stronger or harder to kill, but does not unlock arbitrary moves such as a non-magical "Whirlwind Slash" that require separate fictional justification.

Core martial verbs should remain compact and universal, such as **Attack, Feint, Riposte, Dodge/Defend, Shove, Grapple, Disarm, Trip, Aim, Charge and Intercept** (final list still to be settled in the combat chapter).

**Design target:** Low Focus should support players who enjoy substantial build tinkering between sessions but comparatively straightforward, dice-forward execution during combat.

## Medium Focus — Routing

**LOCKED:** Medium Focus actively redirects Veil power and therefore supports more temporary, activated inward effects than Low Focus. A Medium-Focus character may, for example:

- enhance a weapon;
- blink or reposition magically;
- accelerate motion temporarily to increase attacks or land a difficult hit;
- redirect Veil flow into reflexes/defense when pressured;
- use a limited outward spell;
- shift resources between offense, defense, mobility and spellcasting during the fight.

These effects should generally draw from the **same VP pool** used for outward spells. The core Medium-Focus decision is therefore not "which martial technique do I unlock?" but **where do I route my limited Veil power right now?**

Medium Focus should have:

- fewer and/or weaker projected spells than High Focus;
- more active inward effects than Low Focus;
- greater short-term flexibility than Low Focus, purchased through VP expenditure and timing decisions;
- meaningful competition between spending VP on bodily/equipment enhancement versus spending it on an external spell.

A Spellblade is the clearest example: one encounter may favor weapon enhancement + blink + accelerated motion; another may favor dropping offensive enhancement and routing VP into improved dodging/survival.

## High Focus — Projection

**LOCKED:** High Focus concentrates advancement on outward Veil manipulation. High-Focus characters should receive broader/stronger spell access and more projected options, with their main combat complexity coming from **selection** rather than numerous passive martial improvements.

High Focus therefore remains the natural home of full-caster-like builds, but the reason is now fictional and systemic: most of their Veil integration is projected outward rather than embodied inwardly.

## Cross-focus design rules

**LOCKED:**

1. **Level deepens Veil integration for everyone.** A high-level martial character is extraordinary because the Veil increasingly sustains and reinforces them, not because mundane biology scales without explanation.
2. **Focus determines expression, not permission.** Low Focus can still learn some spells; High Focus can still gain limited inward development. The difference is where most advancement naturally goes.
3. **Low Focus favors build-time complexity and play-time simplicity.** Most inward benefits are passive/persistent.
4. **Medium Focus favors timing and routing.** Its active inward effects are temporary and usually compete with spells for VP.
5. **High Focus favors projected choice.** Its complexity comes from a larger spell/effect toolkit and VP allocation.
6. **No arbitrary martial ability vocabulary.** Veil advancement may explain greater speed, strength, reflexes or durability, but it enhances universal combat actions rather than inventing unexplained special sword moves.
7. **Ordinary techniques remain ordinary.** Feints, ripostes, grapples, shoves and similar actions belong to the core combat rules; training and Veil development change effectiveness, not fundamental permission to attempt them.

## Audit consequences

This locked model changes several older audit assumptions:

- The old `High 1 / Medium .75 / Low .5` VP multipliers can no longer be treated as the complete Focus model; they are now **PROVISIONAL legacy numbers** pending native VP/Vigor advancement design.
- Low Focus should gain level-based inward Veil developments and/or passive reinforcement, not merely reduced spellcasting plus conventional martial class features.
- Medium Focus requires a native subsystem for temporary inward Veil routing and VP expenditure.
- Spell-access progression must be designed around **projection capacity**, while inward advancement must be designed around **embodiment capacity**.
- The combat chapter must define the universal mundane action vocabulary before Focus developments are written, so advancement modifies shared actions instead of duplicating them as named class techniques.

# What is actually ready to lock now

The following material is mature enough to be treated as the current Veilbound foundation without first redesigning it:

- The Veil and the absence of true gods.
- Pillars as human-created emergent forces powered by collective desire.
- Moral neutrality of the Veil and the importance of internal coherence.
- The sixteen Pillars and forty-eight aspects.
- The four path identities: Priest, Scholar, Gifted, Anointed.
- The broad rarity and social identity of those paths.
- Focus as **Veil expression**, not a simple martial/magical tradeoff: Low = embodiment, Medium = routing, High = projection.
- Resonance as a −3 to +3 universal character state.
- The quadratic spell-cost curve.
- The three-act 1–20 progression structure.
- The 36-specialization and 12-mastery architecture, though not their complete mechanics.
- The eight native abilities: Strength, Agility, Precision, Intellect, Awareness, Presence, Vitality and Veil Affinity.
- Direct ability modifiers rather than 3–18 legacy scores.
- Narrow acquired training at +0 to +4, with no generic mandatory Perception/Investigation/Athletics/Persuasion/Stealth skills.
- The core d20 check procedure, passive 10, Take 10, Take 20 and the base-10 difficulty ladder.
- The three-response defense model: Take Hit, Dodge with accumulating Dodge Pressure, or limited Guard; Parry/Block collapse into Guard, while Riposte/Intercept are Guard-linked follow-ups/uses.
- Natural 1 on attacks as an automatic miss with no inherent fumble; natural-20 critical handling remains provisional.
- HP as level-stable physical integrity primarily tied to Vitality.
- Vigor as finite regenerative reserve and the distinction between restoring HP and restoring Vigor.

# What prevents Veilbound from being a standalone RPG today

The general non-combat engine and the core **Take Hit / Dodge / Guard** defensive decision model now exist. The largest remaining standalone-RPG gaps are the exact native attack/Guard/Dodge math, turn/action economy, damage/armor calibration, 0-HP rules, and legacy formulas that still depend on 5e proficiency or ability assumptions.

To become independently playable rather than “Veilbound layered over 5e,” the rules still need:

1. Finalize starting allocation and advancement for the eight native abilities.
2. Finalize native attack, Dodge and Guard math plus saving/defense categories; passive AC/Evasion is no longer assumed.
3. Tune HP, Vigor capacity, regeneration, wound and healing numbers against actual weapon/spell damage.
4. A complete spell-access progression by level and Focus.
5. A self-contained combat chapter, including initiative, defenses, 0 HP/death, conditions and resting.
6. Resolution of the remaining VP, Gifted, Anointed and martial progression conflicts above.
7. Complete specialization/mastery mechanics.
8. A complete equipment/economy system.
9. Extended social/investigation procedures plus exploration, downtime and crafting systems.
10. NPC, creature and encounter-building rules.

## Bottom-line audit

**Veilbound now has a strong locked setting/metaphysics layer, a native general action-resolution engine, a clear durability concept, a strong magic-resource identity, and a clear class/progression skeleton.** It is no longer accurate to describe the entire connective engine as missing; the main remaining dependency on 5e is concentrated in combat, defenses, several spell/class formulas, and legacy content terminology.

**Core Resolution v0 is now substantially locked.** Ordinary actions, passive resolution, Take 10/Take 20, narrow training, the base-10 difficulty framework, and natural-1/natural-20 plausibility rules now have a native Veilbound foundation. The durability model also now has a clear conceptual split between HP, Vitality-driven regeneration and Vigor reserve.

The cleanest next design task is **combat math calibration**: finalize the two-ability attack formula, Dodge degradation, Guard capacity/check math, initiative/action economy, weapon damage versus armor, and 0-HP/death rules. Those decisions will let us numerically tune HP/Vigor and then revisit spells and class progression without relying on 5e assumptions.

---

# SUPERSEDED UPDATE: Physical Tempo Progression

## Status: SUPERSEDED BY TURN AP

The former direct Focus/level Physical Tempo table is no longer canonical. It is replaced by the shared Turn AP architecture below. Earlier audit discussion that assumes spendable Attack Units is historical unless restated by current canonical rules.

---

# LOCKED UPDATE: Turn Action Points, Physical Tempo, and Projection Tempo

## Status: LOCKED

All Focuses use one shared level-based Turn AP pool:

```text
Turn AP = min(120, 30 + 6 × (Level - 1))
```

Turn AP begins at 30 at level 1, increases by 6 per level, reaches 120 at level 16, and remains 120 through level 20.

Focus determines fixed AP efficiency:

| Focus | Physical Action | Projection Action | General Tempo Action |
|---|---:|---:|---:|
| High — Projection | 30 AP | 20 AP | 24 AP |
| Medium — Routing | 24 AP | 24 AP | 24 AP |
| Low — Embodiment | 20 AP | 30 AP | 24 AP |

Derived values are:

```text
Physical Tempo = floor(Turn AP / Physical Action Cost)
Projection Tempo = floor(Turn AP / Projection Action Cost)
Guard Capacity = Physical Tempo
Opportunity Capacity = Physical Tempo
```

Physical Tempo and Projection Tempo are throughput measures, not separate action pools. Mixed physical/projected turns simply pay each action's AP cost from the same Turn AP pool.

At the mature 120-AP cadence:

| Focus | Physical Tempo / Guard | Projection Tempo |
|---|---:|---:|
| High | 4 | 6 |
| Medium | 5 | 5 |
| Low | 6 | 4 |

A **Full Action** requires the entire current Turn AP allotment to remain available and consumes that entire allotment. It does not cost a fixed 120 AP.

A **General Tempo Action** costs 24 AP regardless of Focus and is used for neutral setup/reconfiguration actions whose timing should not inherently favor Embodiment or Projection.

Projection Tempo does not grant universal technique repeatability. Technique-specific cadence, VP costs, Pulse/Spend limits, and other restrictions continue to govern repeated magical output.

---

# LOCKED UPDATE: Guard, Dodge, Criticals, Weapons and Armor

## Defensive declaration and Guard — LOCKED

For each enemy's declared attack sequence, the defender assigns **Take Hit**, **Dodge**, or **Guard** to each incoming attack before the rolls for that enemy resolve.

- **Take Hit:** the attack lands unless the attacker rolls a natural 1.
- **Dodge:** unlimited, but repeated Dodges in the same round accumulate Dodge Pressure.
- **Guard:** limited by Physical Tempo and equipment. Guard unifies parrying and blocking into one defensive response.

Guard is binary:
- attack fails to beat Guard Defense → attack is stopped;
- attack beats Guard Defense → attack hits normally and armor handles the damage.

There is no partial/half-damage Guard state.

Ordinary dual-wielding does not stack Guard bonuses. Use the best applicable Guard setup. Defensive off-hand weapons such as parrying daggers and shields may improve Guard. Shields may improve Guard score and sufficiently substantial shields may grant **at most +1 Guard capacity per round from equipment**, regardless of shield size.

Riposte is a possible follow-up to a successful Guard where appropriate, not a separate core defense. Intercept uses Guard to protect an ally rather than creating a separate defensive subsystem.

## Dodge — LOCKED

**Dodge Defense = 10 + Agility + Awareness − Dodge Pressure**

Dodge Pressure is **−2 for each previous Dodge chosen in the same round**:
- 1st Dodge: no penalty
- 2nd Dodge: −2
- 3rd Dodge: −4
- 4th Dodge: −6
- and so on.

Only choosing Dodge increments Dodge Pressure. Taking a hit or using Guard does not. Dodge has no training bonus and no minimum floor; repeated Dodges can become extremely unreliable so characters can be overwhelmed.

Inward Veil development may later improve Dodge through passive Low-Focus reinforcement or temporary Medium-Focus VP-powered redirection without changing this baseline formula.

## Natural 1 and criticals — LOCKED

A natural 1 on an attack is an **automatic miss**. It has no inherent fumble or critical-failure effect.

A natural 20 creates a critical opportunity.

Against **Dodge or Guard**:
1. Roll a confirmation attack against the same defense assigned to that attack.
2. Failed confirmation → **Strong Hit** with a small damage bonus.
3. Successful confirmation → **Critical Hit**.
4. Confirmation is also a natural 20 → **Devastating Critical**.

Against **Take Hit**:
- the initial natural 20 is automatically a Critical Hit;
- roll once more only to determine whether a second natural 20 upgrades it to a Devastating Critical.

There is no separate Critical Defense statistic. Guard does not cancel criticals by special rule; its higher defense naturally makes confirmation harder.

## Ability scale — LOCKED

Veilbound uses direct ability modifiers rather than D&D-style 3–18 scores. **0 is the ordinary adult baseline**, and negative values are allowed.

| Modifier | Meaning |
|---:|---|
| −2 | Seriously poor / impaired |
| −1 | Below average |
| 0 | Normal adult |
| +1 | Noticeably capable |
| +2 | Very capable |
| +3 | Exceptional |
| +4 | Elite human |
| +5 | Near peak natural human |
| +6+ | Normally Veil-enhanced or otherwise extraordinary |

Natural ability should remain compressed. Veil advancement should generally improve capability through reinforcement, routing and projection rather than routinely inflating natural ability scores.

## Weapon damage model and baseline table — LOCKED CALIBRATION

Ordinary weapon damage uses:

**fixed weapon base + one damage die + applicable physical contribution**

The fixed component prevents clean hits from becoming trivial solely because of a low damage roll, while the single die preserves useful variance and keeps high-attack turns manageable.

After a hit:

**Effective Armor = max(Armor − Penetration, 0)**

**HP Damage = max(rolled weapon damage + applicable physical contribution − Effective Armor, 0)**

The following mundane profiles are the current calibrated baseline. Applicable physical contribution, exact attack-ability pairing and some weapon-specific traits are separate rules and remain to be finalized.

| Weapon | Hands | Damage | Pen | Trauma | Baseline identity |
|---|---|---:|---:|---|---|
| Dagger | 1 | 2 + d4 | 0 | Cut / Pierce | Concealable; poor against armor; strong gap/called-shot tool |
| Rapier | 1 | 2 + d6 | 2 | Pierce | Precision weapon; moderate armor interaction |
| Sword | 1 | 3 + d6 | 2 | Cut / Pierce | General-purpose one-handed baseline |
| Spear | 1 or 2* | 3 + d6 | 3 | Pierce | Reach/penetration-oriented; exact one-vs-two-handed handling pending |
| Axe | 1 | 3 + d8 | 2 | Cut | High raw Cut trauma |
| Mace | 1 | 4 + d6 | 3 | Crush | Strong anti-armor one-handed weapon |
| Greatsword | 2 | 4 + d8 | 2 | Cut | Two-handed Power profile; high raw damage rather than exceptional Penetration |
| Bow | 2 | 2 + d4 | 3 | Pierce | Sustained ranged weapon; lower raw trauma, strong penetration, primary carrier for ranged status/debuff effects |
| Heavy crossbow | 2 | 4 + d8 | 4 | Pierce | High-penetration opening/burst weapon with substantial reload cost |

\* Spears may later be split into one-handed spear and dedicated two-handed long-spear profiles when Reach is finalized.

### Two-Handed — LOCKED

**Two-Handed:** A weapon with this trait requires two available hands to **Attack or Guard** with it.

- A two-handed **melee** weapon gains **+1 Guard Defense** from leverage.
- Two-Handed grants **no additional Guard capacity**.
- There is **no universal Two-Handed damage or Penetration bonus**. Increased leverage is already represented in that weapon's listed Damage, Penetration, Reach, trauma profile or other traits.
- A character cannot simultaneously benefit from a shield, defensive off-hand weapon, second weapon or another held item while Attacking or Guarding with a Two-Handed weapon.
- A character may briefly remove one hand for ordinary manipulation, but cannot Attack or Guard with the weapon until both hands are available again.

Two-handed weapon families should specialize rather than universally dominate:

| Family | Leverage primarily becomes |
|---|---|
| Greatsword | Raw damage |
| Polehammer | Penetration / Crush |
| Long spear | Reach / Pierce |
| Greataxe | Power / Cut trauma |

This makes the choice an opportunity-cost decision. A one-handed sword may be combined with a shield, parrying off-hand or other tool; a greatsword gives those options up for stronger offense and modestly stronger Guard quality.

## Armor model and baseline table — LOCKED CALIBRATION

Armor provides **fixed damage reduction**. Weapon **Penetration** reduces effective Armor before damage is applied.

Armor remains individual equipment rather than collapsing entirely into Light/Medium/Heavy. Broad categories may still govern training and general rules.

Each armor type is described primarily by:
- **Armor** — fixed damage reduction;
- **Coverage** — how much of the body is protected, especially relevant to wounds and called shots;
- **Agility Cap** — maximum positive Agility contribution to Dodge;
- **Traits** — a small number of meaningful characteristics;
- **Rune capacity** — a later enchantment property kept separate from Armor Rating.

Avoid a universal Slash/Pierce/Crush resistance matrix unless testing later demonstrates a need for one.

| Armor | Armor | Dodge Agility cap | Rune-space direction | Baseline identity |
|---|---:|---:|---|---|
| Clothing / light robes | 0 | None | High | No meaningful mundane protection; maximum mobility and strong enchantment canvas |
| Heavy padded / battle robes | 3 | +2 | Very High | Cumbersome cloth layers; weak-to-moderate mundane protection but excellent rune space |
| Leather | 3 | +4 | Medium | Mobile light protection |
| Reinforced leather | 4 | +3 | Medium | Stronger mobile protection |
| Chain mail | 4 | +3 | Low | Flexible metal protection; awkward rune surface |
| Brigandine | 5 | +2 | Low–Medium | Standard serious frontline protection |
| Scale armor | 5 | +2 | Low–Medium | Standard serious frontline protection |
| Breastplate | 5 | +3 | Low | Strong torso protection with better mobility but less total coverage |
| Plate armor | 6 | +2 | Low | Heavy frontline/defender-grade protection |
| Full knightly harness | 7 | +1* | Very Low | Maximum mundane protection and coverage at substantial mobility cost |

\* +1 is the baseline full-harness Dodge cap; specialized fitting, Veil enhancement or later equipment traits may modify it.

**Armor 5 is the calibrated standard for serious frontline protection.** Armor 6–7 represents increasingly specialized heavy protection.

### Agility caps — LOCKED

Armor caps only the **positive Agility modifier applied to Dodge Defense**; it does not reduce the character's actual Agility score.

**Dodge Defense = 10 + min(positive Agility, Armor Agility Cap) + Awareness − Dodge Pressure**

If Agility is 0 or negative, use the actual modifier; armor never raises a poor Agility score to its cap.

The cap does not normally apply to weapon attacks or every Agility-based check. Other movement restrictions, if relevant, are handled by specific equipment traits or circumstances rather than automatically stacking broad penalties onto armor.

### Rune capacity — LOCKED DIRECTION, NUMBERS DEFERRED

Rune capacity is deliberately separate from mundane Armor Rating. Cloth and layered robes can provide much more usable inscription/weaving space than chain or rigid breastplates. This gives magically invested characters a genuine equipment tradeoff rather than forcing all high-level characters toward maximum mundane Armor.

Examples of intended choices:
- an agile Spellblade may choose light robes and rely on Dodge, Blink and temporary magical defenses;
- a Battlemage may choose heavy rune-rich robes, accepting a lower Dodge Agility cap for greater enchantment infrastructure;
- a frontline Fighter may choose Armor 5–7 and sacrifice rune capacity for reliable passive protection.

Exact rune-slot/capacity values belong to the later enchantment system and are not yet numerically locked.

## HP / Vigor / Wounds calibration — LOCKED

### HP and Vigor

**Max HP = 10 + Vitality**

HP represents physical integrity and does **not** scale with level.

**Max Vigor = (10 + Vitality) × Level**

Vigor represents the character's Veil-supported regenerative reserve. Level increases how much punishment the character can recover from rather than making the body itself harder to stab, crush, or burn.

Low Focus does **not** automatically receive additional Vigor capacity. Extra reserve is an optional inward Veil-development choice rather than a universal Focus benefit.

### Natural regeneration

Natural HP regeneration resolves **once per character round**, after all damage taken before that regeneration step. It consumes Vigor point-for-point unless another rule modifies efficiency.

**Regeneration throughput = max(Vitality, 0) + Focus Rate**

- High Focus: +1
- Medium Focus: +2
- Low Focus: +3

The exact throughput values remain subject to encounter calibration, but this formula is the adopted baseline.

Because regeneration resolves only once each round, several attacks can overwhelm current HP before the character can recover. A character may therefore need to become defensive even while retaining a large Vigor reserve.

Valid anti-regeneration mechanics include:
- direct Vigor damage;
- reduced regeneration throughput;
- temporary regeneration suppression;
- increased Vigor cost per HP restored;
- blocking external Vigor restoration;
- temporary maximum-Vigor reduction.

Death-Pillar effects, alchemical substances and specialized magical weapons are valid sources of these effects.

### Wound triggers

Ordinary hits do not normally create persistent wounds. A wound occurs only when:

1. a **Called Shot** successfully qualifies for a wound;
2. a **Devastating Critical** occurs; or
3. the target reaches **0 HP**.

A Called Shot consumes the character's entire Attack action regardless of normal attack count and carries substantial location difficulty. It is intended for specific tactical goals rather than as a default damage option.

### Random wound location

If the attacker did not specify a location, roll d20:

| d20 | Location |
|---:|---|
| 1–2 | Head / neck |
| 3–8 | Chest |
| 9–12 | Abdomen |
| 13–15 | Arm |
| 16–19 | Leg |
| 20 | Hand / extremity |

Weapon trauma type determines the applicable wound column.

| Location | Cut | Pierce | Crush |
|---|---|---|---|
| Head | Severe laceration; possible neck decapitation where physically plausible | Eye/brain penetration | Skull fracture / brain trauma |
| Chest | Massive open wound | Punctured lung / heart | Broken ribs / organ trauma |
| Abdomen | Evisceration / severe bleeding | Organ perforation | Ruptured organ / internal bleeding |
| Arm | Tendon/artery severance; possible amputation | Deep puncture / nerve injury | Shattered bone |
| Leg | Artery/tendon severance; possible amputation | Deep puncture | Shattered leg |
| Hand | Severed fingers/tendons | Pierced hand | Crushed hand |

Weapons may support more than one trauma mode where appropriate, but the physical attack mode determines which column applies.
### Wound severity

Severity is determined by the event that caused the wound rather than by a second random roll.

- **Called Shot:** normally Serious if it qualifies; exceptional results may upgrade it.
- **0 HP:** Serious or Critical depending on how far the attack carries the target below zero; exact overkill threshold remains to be calibrated.
- **Devastating Critical:** at least Critical and may be Fatal when the weapon, location and circumstances physically permit it.

### Wound Repair Requirement

Wound repair cost is based on bodily trauma and does **not** scale with level.

| Severity | Baseline repair requirement |
|---|---:|
| Serious | ~10 Vigor |
| Severe | ~20 Vigor |
| Critical | ~30 Vigor |
| Catastrophic | 40+ Vigor |
| Irreparable / immediately fatal | Cannot be naturally regenerated |

Current example values:

| Wound | Repair requirement |
|---|---:|
| Deep arm wound | 10 |
| Broken arm | 15 |
| Severed tendon | 15 |
| Broken leg | 20 |
| Major artery | 20 plus ongoing bleeding |
| Destroyed eye | ~25 |
| Shattered leg | 30 |
| Punctured lung | 30 |
| Severe abdominal organ injury | 30 |
| Crushed skull | 40+ |
| Decapitation / destroyed vital structure beyond repair | — |

Specific wounds may impose ongoing effects until treated or repaired. Examples include bleeding, reduced movement, impaired Dodge, reduced regeneration throughput, or sensory penalties.

### Dying and death

At **0 HP or below**, a character is normally unconscious and **Dying**.

By default, a Dying character loses **1 HP per round**.

**Death occurs at HP ≤ −Maximum HP.**

Once actually dead, ordinary Vigor regeneration cannot restart the body.

While Dying and still possessing Vigor, the character's regeneration throughput is first available for survival and wound repair rather than ordinary HP recovery. The player may allocate that throughput mechanically even though the character is unconscious:

- 1 point may be spent to cancel the default −1 HP Dying loss for that round;
- remaining throughput may be spent toward the active Wound Repair Requirement;
- additional bleeding or similar ongoing losses must also be prevented, offset, or medically controlled;
- once the wound is repaired, remaining throughput in that regeneration step may restore HP;
- once HP rises above 0, the character can regain consciousness unless another effect prevents it.

Medicine can stabilize, stop bleeding, immobilize injuries and otherwise suppress ongoing consequences without necessarily restoring HP or completing supernatural tissue reconstruction.

## Cheat Death / Death-Pillar survival — LOCKED FRAMEWORK

Cheat Death is a family of escalating Death-Pillar effects rather than one universal spell.

A Cheat Death effect must be activated **while the character is conscious**. Once HP has reached 0 and the character is unconscious, they cannot voluntarily activate it.

Lower forms may allow the character to remain conscious and function below 0 HP without changing the natural death threshold. Higher forms may suppress Dying effects and/or extend the temporary death threshold farther below **−Maximum HP**.

While a Cheat Death effect is active:
- the character cannot receive external HP healing;
- the character cannot receive external Vigor restoration;
- protective barriers, damage prevention, mundane stabilization and wound treatment may still function;
- the effect does not itself repair wounds.

This forces a real tactical choice between using healing now and committing to Death magic to remain active despite worsening injuries.

If a higher Cheat Death effect sustains the character **below their normal death threshold**, the character gains a persistent **Death Mark**. Death Marks survive the encounter and require meaningful healing, full recovery or an appropriate restorative ritual to remove. Repeated unresolved marks can lead toward partial undeath or instability.

Intentional **lichdom** is a deliberate high-level advancement choice for a character deeply invested in the Death Pillar. It is not an automatic consequence of accumulating marks; uncontrolled marks instead represent dangerous, imperfect dependence on Death-Pillar sustainment.

## Off-hand, dual-wield and ranged combat — LOCKED PLAYTEST BASELINE

### Defensive off-hands and shields

A defensive off-hand grants **+1 Guard capacity**. Its type determines any additional benefit.

| Setup | Extra Guard capacity | Guard Defense bonus | Special |
|---|---:|---:|---|
| Parrying dagger | +1 | +1 melee | Improved Riposte |
| Buckler | +1 | +1 | May Guard normal projectiles |
| Shield | +1 | +2 | May Guard normal projectiles |
| Large shield | +1 | +3 | May Guard normal projectiles; possible mobility/cumbersomeness drawback |
| Two-handed melee weapon | — | +1 | Offensive/reach leverage is built into weapon profile |

Shield size increases Guard Defense rather than Guard count. Ordinary weapons do not normally Guard arrows or crossbow bolts.

### Riposte

Any successful **melee Guard** creates a **Riposte Opening** against that attacker until the end of the defender's next turn. A Riposte:
- spends one of the defender's normal Attack units;
- gains **+2 to the attack roll**;
- is not a free additional attack;
- consumes the opening after one attack.

A parrying dagger improves the Riposte attack bonus to **+3** instead of +2.

### Dual wield

At the start of the wielder's turn, choose the relevant offensive or defensive use. The character does not gain both benefits in the same turn.

- **Light + Light:** either gain **+1 off-hand Attack** that turn, or **+1 Guard capacity** until the next turn.
- **Medium + Light:** either gain **+1 off-hand Attack with the light weapon at −2 to the attack roll**, or **+1 Guard capacity** until the next turn. A parrying dagger may also provide its Riposte improvement.
- **Medium + Medium:** no baseline extra Attack or Guard. The benefit is flexibility to choose which weapon profile to use for each normal attack. Dedicated dual-wield development may later unlock a heavily penalized extra off-hand attack.

### Ranged defense

Melee and projectile defense use different assumptions.

Against melee, choosing **Take Hit** means the attack lands unless the attacker rolls a natural 1.

Against a normal ranged projectile, a target that does not actively evade is **not automatically hit**. Use a static **Ranged Defense** based on:

`10 + Range Difficulty + Cover + Size/Position and other shot-condition modifiers`

An aware target may actively Dodge a ranged attack.

`Ranged Dodge = 10 + capped Agility + Awareness + Evasion Bonus + Range Difficulty − Dodge Pressure`

Awareness represents reading the shooter's posture, aim and timing rather than reacting after the projectile is already in flight.

**Evasion Bonus = Physical Tempo − 1**, giving +0/+1/+2/+3/+4/+5 at Tempo 1/2/3/4/5/6. This lets active ranged defense scale alongside trained ranged offense without adding a mandatory generic Dodge skill.

Current baseline bow/crossbow range bands are:

| Range | Squares | Approx. distance | Difficulty modifier |
|---|---:|---:|---:|
| Close | 1–6 | 1.5–9 m | −2 |
| Short | 7–12 | 10.5–18 m | +0 |
| Medium | 13–30 | 19.5–45 m | +2 |
| Long | 31–60 | 46.5–90 m | +5 |
| Extreme | 61–120 | 91.5–180 m | +8 |

These bands are calibrated against the locked baseline movement of 6 orthogonal squares (12 MP). Sprint is now locked at three times the impaired normal Movement Allowance—36 MP / 18 orthogonal squares for an unimpaired ordinary creature—so the range bands should be retested against that faster closing speed. Charge remains unresolved. Short-range Blink assumptions in the roughly 20–30 square range likewise remain technique calibration rather than movement-foundation canon. Specific ranged weapons may later gain different maximum ranges without changing the universal band modifiers.

### Archer battlefield identity

Archers are primarily **long-range debuff, status-delivery, interruption and Interception specialists**, rather than top sustained HP/Vigor killers. Their advantage is applying useful effects from distance and threatening declared actions or lanes. Melee/contact weapon enchantments may later support stronger direct Vigor burn and anti-regeneration than projectile enchantments, while projectile enchantments emphasize marks, debuffs, interruption, tracking, slowing, suppression and related control effects.

Close range is intentionally dangerous for an Archer. Bows normally cannot Guard melee attacks; a shield is generally unavailable while actively using a two-handed bow; readying another weapon costs one General Tempo Action (24 AP); and melee-focused characters or Spellblades can close or Blink into engagement. The close-range accuracy benefit does not remove this positional risk.

A bow or crossbow may be fired while the wielder is threatened in melee, but doing so provokes an opportunity attack before the ranged attack resolves. If the provoking attack hits, the ranged attack is interrupted and lost. Because an ordinary bow cannot Guard melee attacks, the Archer usually must Dodge, use an explicit magical/Veil defense, or Take Hit and accept the resulting interruption.

### Crossbows

Crossbows are **low-training, high-alpha** ranged weapons rather than scaling sustained-fire weapons. The current heavy-crossbow baseline is **4+d8 damage, Pen 4**.

**Firing a heavy crossbow is a Full Action. Reloading a heavy crossbow is also a Full Action.** Each requires the character's entire current Turn AP allotment to remain available and consumes that allotment. A high-Tempo character therefore does not gain multiple heavy-crossbow shots from higher Physical Tempo.

Dropping a held item such as a fired crossbow is normally free. Drawing/readying another weapon costs one **General Tempo Action (24 AP)**. Thus a character may use a preloaded heavy crossbow as an opening Full Action, then on a later turn drop it, spend 24 AP to draw a melee weapon, and use any remaining Turn AP normally. This preserves the prepared-volley tactic without allowing a character to fire the heavy crossbow and transition into melee offense during the same turn.

Dedicated Archers therefore outscale crossbows in sustained fire as Physical Tempo rises, while crossbows remain useful for prepared opening shots, ambushes, militia/guards and NPC volley fire.

### Ammunition and ethereal arrows

A standard quiver is treated as holding about **20 arrows**.

- Mundane physical arrows cost no VP to fire.
- An Archer-oriented character may create an **Ethereal Arrow** as part of a bow attack for **1 VP**. Ethereal arrows disappear shortly after impact or miss and cannot be recovered.
- An enchanted ethereal arrow costs **1 VP + the full VP cost of the chosen ammunition effect**.
- A physical arrow may normally hold **one major ammunition enchantment**. Poison, smoke, explosive, snare, interruption, tracking, regeneration suppression, Veil marking and similar effects are separate loadout choices rather than stackable all-purpose arrows.
- Pre-enchanting physical ammunition receives a substantial **bulk preparation discount**. Example calibration: an effect that costs 2 VP when manifested spontaneously may cost about 20 VP to prepare on a batch of 20 physical arrows, while the equivalent ethereal shot costs 3 VP each. Exact effect costs remain to be calibrated.
- Prepared ammunition enchantments are temporary. They expire at the character's **next Full Recovery or after about 24 hours, whichever occurs first**. Completing a Full Recovery dissipates all previously prepared ammunition enchantments from that character. The physical arrows remain usable as mundane ammunition. This prevents repeated prepare/recover cycles from stockpiling carts of enchanted arrows.

This creates three ammunition modes: **mundane physical arrows** are finite and free; **prepared enchanted arrows** are finite, efficient and planned; **ethereal arrows** are flexible and effectively unlimited but VP-expensive.

## Ranged sanity-test checkpoint — PASSED FOR CURRENT BASELINE

The current bow/crossbow numbers were sanity-tested against Armor 3–7, active ranged Dodge, increasing Physical Tempo and prepared crossbow volleys. The results support the intended roles:
- **Bow:** `2+d4`, Pen 3. Raw HP damage is modest against heavy armor, while high Physical Tempo creates sustained pressure and makes lightly armored/rune-focused targets vulnerable.
- **Heavy crossbow:** `4+d8`, Pen 4. Prepared volleys are intentionally dangerous, but Full-Action firing and Full-Action reloading prevent the weapon from scaling with Physical Tempo like a bow.
- **Armor interaction:** Armor 6–7 remains strongly protective against ordinary bow HP damage, keeping the Archer focused on ranged status/debuff delivery against heavily protected frontline targets.
- **Opening-volley transition:** firing a preloaded heavy crossbow as a Full Action, then discarding it and drawing a melee weapon on a later turn remains a valid tactical opener. It no longer grants same-turn melee attacks at high Physical Tempo.

## Remaining combat calibration work

The core HP/Vigor/Wound model, baseline mundane weapon damage, Penetration, Armor ratings, Dodge Agility caps, Two-Handed rule, off-hand/shield framework, dual-wield framework and ranged-defense framework are now locked for the current playtest baseline. Remaining calibration includes:
- applicable physical damage contribution by weapon;
- exact attack ability pairs and training interaction by weapon family;
- Reach, Brace and other weapon-specific traits;
- final mobility/cumbersomeness drawback for large shields if needed;
- armor Coverage and final armor trait definitions;
- exact rune-capacity values once the enchantment system is built;
- projectile-enchantment effect costs and final bulk-preparation formula;
- Strong Hit and Critical Hit damage bonuses;
- exact overkill threshold for Serious versus Critical 0-HP wounds;
- detailed ongoing effects and repair requirements for the full wound list;
- high-level direct Vigor-damage and defensive-development scaling needed to keep peer fights within intended encounter duration.

## LOCKED — Native Ability Set Update: Veil Affinity and Veil Control

The native ability set now contains nine abilities:

- Strength
- Agility
- Precision
- Intellect
- Awareness
- Presence
- Vitality
- Veil Affinity
- Veil Control

### Veil Affinity
Veil Affinity represents magical capacity: how much Veil power a character can contain and channel. It is intended to govern VP reservoir and may also govern maximum simultaneous VP commitment and/or the maximum intensity of a single effect.

### Veil Control
Veil Control represents magical execution: how precisely, efficiently, and forcefully a character shapes Veil power. It is intended to govern spell attack accuracy, effect potency, resistance difficulty, healing effectiveness, maintenance/manipulation of complex effects, and similar execution functions.

### Archetype Stat Freedom
No whole Archetype is tied to a mandatory mundane casting ability. Scholar does not universally require Intellect, Priest does not universally require Presence, etc. A low-Intellect practical Scholar or a quiet low-Presence village Priest must remain mechanically viable.

Mundane abilities may still contribute to specific magical actions when the action genuinely depends on them—for example Precision for a precision spell, Awareness for timing/target-reading, Intellect for ritual theory/design, Presence for command-like magic, or Vitality for bodily strain—but these are effect-specific rather than universal Archetype requirements.

### Focus and Veil Ability Dependence
- High Focus generally treats Veil Affinity and Veil Control as primary attributes.
- Medium Focus balances Veil Affinity/Control against physical and mundane abilities.
- Low Focus can function with more moderate Veil stats because much of its power is persistent embodiment and relies more heavily on physical abilities.

This split supersedes the earlier eight-ability version of the native ability system.


## LOCKED — Level-1 Ability Generation and Advancement

### Character Creation
All nine abilities begin at **−2**. A level-1 character receives **28 ability points** to distribute. Costs are cumulative from −2 and intentionally rise at higher positive values:

| Final score | Total cost |
|---:|---:|
| −2 | 0 |
| −1 | 1 |
| 0 | 2 |
| +1 | 3 |
| +2 | 5 |
| +3 | 7 |
| +4 | 10 |

The normal level-1 maximum is **+4**. A balanced default of two abilities at +3 and the remaining seven at 0 costs exactly 28 points. The escalating curve permits hard specialization but makes +4/+4 builds pay for that specialization with real weaknesses elsewhere.

### Ability Advancement
At levels **4, 8, 12, 16 and 20**, increase **one ability of the player's choice by +1**. This schedule is universal across Focuses and Archetypes.

There is **no special catch-up rule for negative abilities**. Raising −2 to 0 therefore requires two separate advancement milestones. This prevents character creation from rewarding extreme dump-stat arrays that can later be repaired at unusually low cost.

Normal permanent natural ability advancement is capped at **+5**. Effective capability above +5 may come from exceptional Veil enhancement, transformation, relics, temporary effects, lichdom or similarly extraordinary mechanics, but not ordinary ability advancement.

## LOCKED — Core VP Engine and Recovery

### Maximum VP
Maximum VP scales by Focus, Veil Affinity, and level:

- **High Focus:** `max(1, 6 + Veil Affinity) × Level`
- **Medium Focus:** `max(1, 4 + Veil Affinity) × Level`
- **Low Focus:** `max(1, 2 + Veil Affinity) × Level`

Focus determines how efficiently and how often a character is expected to turn VP into active effects. Veil Affinity determines the size of the character's reservoir. A large VP pool is therefore a valid build investment even on Medium- or Low-Focus characters, but action economy and available effect types limit how quickly that reserve can be converted into battlefield impact.

### VP States
VP exists in three states:

- **Available VP:** can be spent or committed normally.
- **Committed VP:** tied to an ongoing sustained effect and unavailable for other uses while that effect remains active.
- **Spent VP:** exhausted and unavailable until recovered.

Releasing a sustained/committed effect has **no action cost** unless that effect explicitly says otherwise. Its committed VP immediately returns to Available VP because it was never spent.

### Rerouting
Rerouting is effect-dependent. Inward-routing effects—such as shifting a Veil enhancement from weapon damage into reflexes or defense—may be rerouted with **no action cost** but normally require a small VP expenditure. The generic cross-system benchmark remains effect-dependent. For the **Medium Scholar**, the specific progression is now locked below: 3 VP per reroute at levels 1–2, falling to 2 VP at levels 3–5, with no action cost and no per-round frequency limit. Other classes/effects may use different routing costs.

Rerouting changes the allocation of already committed power; it is distinct from dismissing one effect and activating an unrelated new effect.

### Zero-action timing and no-refresh rule — **LOCKED**

A rule that says an effect may be **released, rerouted, reassigned, retuned, rechanneled, or otherwise changed with no action cost** removes the action cost only. It does **not** by itself grant interrupt timing.

Unless a feature explicitly provides a Reaction, trigger, or other out-of-turn timing permission, a zero-action change is made during the character's own turn at an otherwise legal decision point.

Changing the allocation, target, expression, anchor, form, or Vessel of an existing effect does **not** refresh or recreate any limited output attached to that effect. In particular, it does not refresh:

- activation effects;
- Pulse uses;
- once-per-turn or once-per-round riders;
- once-per-window resources;
- limited healing, damage, control, Vigor restoration, or similar output;
- any other authored cooldown, charge, or finite-use benefit.

A feature must explicitly say that moving or changing an effect refreshes such an output if that is intended. This rule applies across Scholar routing, Priest Consecration reassignment, Gifted retuning/reconduction, Anointed rechanneling/Investment, and future systems using equivalent zero-action movement.

### VP Recovery
VP recovery is based on **elapsed in-world time**, not on a short-rest/long-rest recharge button.

A character has a sheet value:

> **VP Recovery = 25% of Max VP, rounded to the nearest whole VP**

Minimum recovery is 1 VP if Max VP is above 0.

For every **completed 6-hour interval** of elapsed time, restore one VP Recovery amount from Spent VP, up to Max VP. Partial intervals grant no recovery.

Examples:
- Max VP 30 → VP Recovery 8.
- 2 hours elapsed → 0 VP recovered.
- 6 hours elapsed → 8 VP recovered.
- 12 hours elapsed → 16 VP recovered.
- 24 hours elapsed → recover up to the full pool.

Resting has no unique recharge property. Sleep, travel, study, waiting, downtime, or other elapsed time can all produce recovery ticks unless a specific condition prevents normal VP recovery. Rest remains useful because it is a convenient period for time passage and preparation.

Committed VP does not need recovery. Only Spent VP is restored by recovery ticks.

### VP Effect / Action Categories
Core VP effect/action categories are:

- **Attack Unit:** consumes one Attack unit.
- **Full Action:** consumes the character's entire granted Attack-unit allotment for that turn.
- **Reaction:** uses the character's one Reaction.
- **Sustained:** remains active over time and normally uses Committed VP according to the effect's rules.

An effect can have an activation category and then become Sustained—for example, an effect may require one Attack Unit to activate and then commit VP while maintained.

Prepared effects are not a separate core action category. They are ordinary effects applied in advance with a defined duration. Permanent or long-term binding into magic items remains a separate future subsystem.

### Persistent Expression Cadence — **LOCKED UNIVERSAL RULE**

Any sustained, persistent, attached, embodied, invested, consecrated, routed, or similar effect that can interact repeatedly with ordinary actions must declare an **Expression Cadence** for each of its outputs. The universal cadence vocabulary is:

- **Continuous:** a static or persistent property. It does not multiply with Attack Units and normally remains in force while the effect is valid.
- **Rider:** a modest effect that may apply to each eligible action, attack, Guard, movement, or other listed event. Rider values must be calibrated against the **maximum Physical Tempo** that can trigger them.
- **Pulse:** a stronger finite effect with an explicit refresh unit, such as once per turn, round, Emotion Window, or another authored interval. Moving or retargeting the parent effect does not refresh the Pulse.
- **Spend:** a stronger repeatable output that requires an explicit additional cost—VP, Vigor, Destiny, another resource, or another listed expenditure—each time it is used.

A full technique-scale instance of **damage, healing, Vigor restoration, strong control, or equivalent major output must not be an unrestricted per-Attack-Unit Rider**. Such output must instead use Pulse, Spend, a finite budget, or another explicitly bounded cadence.

An effect may contain more than one cadence component—for example a Continuous defense, a modest weapon Rider, and a once-per-round Pulse—but each component must state its own cadence.

This cadence framework is universal and applies to Scholar Embodiments, Priest Consecrations and Devotional Rites, Gifted Conduits and Embodiments, Anointed Signatures/Investments/Embodiments, future magical equipment, and other persistent Veil effects.

### Interception and Spells
There is no separate Interception-spell category. **Interception is a timing mechanic** that reserves an otherwise valid action or effect and declares a specific trigger with a meaningful failure case. When the trigger occurs, the reserved effect resolves using its normal Attack Unit, Full Action, or other category and its normal VP cost. If the trigger never occurs, the reserved action is lost.

### Veil Control Scaling Principle
Veil Control scaling is specified by individual effects rather than by one universal damage formula. A provisional baseline for a straightforward single-target damage spell is:

> **Bonus Vigor damage = max(Veil Control, 0) × Character Level**

Multi-hit, rapid-fire, area, healing, control, defensive, and utility effects may use different coefficients or apply Veil Control to different parameters so that the same scaling packet is not multiplied excessively by Physical Tempo or number of targets.

## LOCKED — Medium Scholar Foundation, Levels 1–5

The Medium Scholar is a **routing-and-repertoire chassis**, not a disguised Spellblade class. Its Focus identity is rapid allocation of committed Veil power; its Scholar identity is technical access to individually learned techniques drawn from Pillars and Aspects.

### Scholar Archetype Identity

- A Scholar accesses magic through learned technical methods rather than prayer, emotion-linked instinct, or a permanent Anointed bond.
- A Scholar may potentially learn techniques from **any Pillar or Aspect**, but every technique must be learned individually.
- Scholar breadth is offset by lack of innate archetype amplification: a Scholar normally uses the effect's standard Veil Control scaling rather than receiving the stronger intrinsic Aspect amplification expected from Anointed, emotion-driven amplification expected from Gifted, or Pillar/Resonance efficiency expected from Priests.
- Scholar strength therefore comes from **selection, combination, preparation, technical shaping, and cross-Pillar repertoire**, not superior raw output from any one Aspect.
- Techniques retain their actual Pillar/Aspect identity. A Scholar does not learn generic abstract buffs detached from the setting's metaphysics.

### Inward Boosts

Certain learned techniques have the **Inward** property. These route Veil power through the Scholar's own body or immediately wielded equipment. Examples include accuracy, weapon damage, Vigor burn, reflexes, movement speed, jumping, bodily reinforcement, Guard enhancement, senses, and regeneration support.

An Inward Boost:
- commits its listed VP;
- normally has no ongoing action cost once active;
- remains active until released or rerouted;
- occupies an applicable **Inward Channel**.

Representative channels include **Weapon, Motor Control, Reflex, Locomotion, Body, Senses, and Regeneration**. Channel names are functional rather than strictly anatomical.

Two limits apply simultaneously:
1. **Boost-slot limit:** the Medium Scholar may maintain only a limited number of active Inward Boosts.
2. **Channel exclusivity:** only one active Inward Boost may occupy the same channel at a time.

Thus Weapon Vigor Burn + Motor Accuracy is legal when two slots are available, but Weapon Vigor Burn + Weapon Damage is not; both compete for the Weapon channel. Likewise, Running Speed and Jumping enhancement normally compete for the Locomotion channel.

### Outward Techniques

Outward effects are not instantaneously produced by Inward Routing. Illusions, projected barriers, battlefield zones, external healing, projectiles, externally projected concealment, traps, and similar effects use their listed activation action and VP rules.

A Scholar may release committed VP from an Inward Boost with no action cost, but activating an outward effect still requires its normal Attack Unit, Full Action, Reaction, or other activation requirement. For example, an illusion that requires one Attack Unit cannot be created merely by instantaneously rerouting an Accuracy boost.

### Rerouting

Rerouting replaces one active Inward Boost with another known, compatible Inward Boost while redistributing already committed power.

- **No action cost.**
- **No per-round frequency limit.**
- Levels 1–2: **3 Spent VP per reroute**.
- Levels 3–5: **2 Spent VP per reroute**.
- Rerouting does not itself increase the total committed VP unless the destination effect requires a different commitment and the character supplies the difference normally.

A character may reroute repeatedly in an emergency and deliberately burn through a large portion of the VP pool. This is an intended Medium-Focus playstyle rather than an exploit: flexibility can substitute for endurance when the situation is urgent.

### Overrouting

**Overrouting** is a strenuous form of Inward Routing used when one capability is especially important right now. It pushes an Inward Boost beyond its ordinary output by drawing capability away from a defined competing bodily function or channel.

- The benefit and sacrifice are defined by the technique rather than chosen freely by the player as an irrelevant dump-stat penalty.
- Examples include exceptional reflexes at the cost of Strength/output; exceptional Strength at the cost of Precision/reflexes; greater Fortification at the cost of mobility; or greater Accuracy at the cost of raw offensive enhancement.
- Overrouting may temporarily push effective capability above the normal +5 natural-human ceiling; this is a Veil enhancement rather than permanent natural advancement.
- Normal Overrouting is capped at **2 steps** unless a later feature explicitly exceeds that limit.

**Overrouting has an additional VP surcharge on top of ordinary Routing:**

> **Overroute surcharge = +1 Spent VP per Overroute step**

Therefore:
- Levels 1–2: entering a one-step Overroute normally costs **4 Spent VP** total (3 routing + 1 surcharge); two steps cost **5 Spent VP** total.
- Levels 3–5: entering a one-step Overroute normally costs **3 Spent VP** total (2 routing + 1 surcharge); two steps cost **4 Spent VP** total.

The surcharge represents the immediate strain and sacrificial nature of forcing disproportionate Veil flow into one function. Maintaining an already established Overroute does not continuously spend additional VP unless the individual technique says otherwise. Dropping the Overroute back to the normal version of the same active boost has no action cost and no VP cost; pushing it into Overroute again requires paying the routing cost and surcharge again.

### Level Progression

| Level | Medium Scholar foundation |
|---:|---|
| **1** | **Veil Routing.** Maximum **1 active Inward Boost**. 3 VP reroute. Scholar begins with a small individually learned technical repertoire spanning chosen Pillars/Aspects. |
| **2** | **Technical Repertoire.** Expand the number and/or breadth of learned techniques. Access remains individually learned rather than automatically granted by Pillar. Exact techniques-known progression remains a later content/balance table. |
| **3** | **Efficient Routing + Overrouting.** Reroute cost becomes **2 VP**. Overrouting becomes part of the mature Medium Scholar loop and adds its +1 VP-per-step surcharge plus defined tradeoff. |
| **4** | **Dual Routing.** Maximum active Inward Boosts increases from **1 to 2**, while channel exclusivity still applies. Also gain the universal level-4 +1 Ability increase. |
| **5** | **Matrix Reconfiguration.** One rerouting payment may replace both currently active Inward Boosts at once, provided the new configuration is legal and known. If Overrouting is added to either destination effect, add the applicable Overroute surcharge for each Overroute step applied. |

### Playstyle Neutrality

The base Medium Scholar must support multiple viable playstyles without making any one of them mandatory. Examples include:

- **Spellblade:** weapon enhancement + accuracy, then rapid defensive rerouting under pressure.
- **Assassin:** precision/mobility, concealment, disabling or suppression techniques, then escape tools.
- **Archer:** senses/accuracy, prepared ammunition techniques, movement, marks, interruptions, and utility magic.
- **Fighter:** stable physical enhancement with selective magical support.
- **Defender:** Body/Reflex/Guard routing plus outward barriers or control.
- **Combat Caster:** defensive inward routing supporting frequent outward spell use.
- **Battlemage:** personal enhancement combined with larger Full-Action control/AoE techniques.
- **Healer/support:** self-protection and mobility for dangerous positioning combined with learned Life or other support techniques.

The unifying identity is not weapon choice or combat role. It is: **learn technical Aspect methods, commit Veil power into a constrained inward matrix, and reconfigure that matrix faster than other archetypes can change their magical posture.**

At level 6, **Field Arcanist, Veil Router, and Surge Caster** branch from this common chassis; they should modify how the same foundation is exploited rather than repair missing core functionality.


---

## Post-audit locked decisions — High Scholar Foundation v0

### Core identity — **LOCKED**

The **High Scholar** is Veilbound's broad technical caster: a competent magical toolbox / jack-of-all-trades whose strength is **breadth, cross-Pillar learning, and situational combinations**, not innate raw superiority inside any one Pillar or Aspect.

Scholar archetype rules apply:
- a Scholar may individually learn techniques from **any Pillar and any Aspect**;
- every technique must be learned rather than automatically granted by Pillar affiliation;
- ordinary learned techniques are cast at their **normal full listed effectiveness**, normal VP cost, normal action requirement, and normal Veil Control scaling;
- Scholars do **not** suffer a generalist penalty to normal spells;
- Scholars receive no innate Priest Resonance amplification, Gifted emotion amplification, or Anointed Aspect amplification merely for being Scholars;
- a Scholar may still deliberately specialize their repertoire, but that selection does not grant specialist-archetype amplification.

The High Scholar should normally be able to answer a wide range of problems when the relevant technique is known: damage, healing/stabilization, mobility, control, concealment, utility, protection, and mundane magical conveniences. Their core fantasy is **"I probably have a competent tool for this"**, not **"every spell I cast must be combined."**

### Level 1 — Technical Repertoire — **LOCKED structure / PROVISIONAL counts**

High Scholars begin with a comparatively broad learned spell/technique repertoire and may learn across unrelated Pillars and Aspects.

The exact number of techniques known at each level remains **PROVISIONAL** until the spell list and expected repertoire size are sufficiently complete to calibrate it. High Focus Scholar should nevertheless have a larger outward-technique repertoire than Medium or Low Scholar as part of its identity.

### Level 1 — Composite Casting — **LOCKED**

A High Scholar may combine **one known Primary Technique** and **one compatible known Secondary Technique** into a single composite spell.

#### Levels 1–2 — Prepared Formulae

At levels 1–2, Composite Casting requires **prepared formulae**. During suitable preparation, the Scholar designates specific known **Primary + Secondary** pairings that are available for Composite Casting. Both component techniques must be known and compatible. The exact number of prepared composite formulae remains **PROVISIONAL** pending repertoire and spell-list calibration.

All normal Composite Casting rules still apply to a prepared formula: the Primary resolves at full strength, the Secondary is diminished, both full VP costs are paid, and the slower action requirement is used.

#### Primary Technique

The Primary defines the composite spell's:
- target;
- range;
- area or shape;
- attack / resistance resolution;
- fundamental purpose and delivery chassis.

The Primary resolves at **full normal strength**, including its normal numerical output and Veil Control scaling.

#### Secondary Technique

The Secondary is incorporated into the Primary rather than becoming a second independently resolved spell.

By default the Secondary contributes:
- approximately **half of its normal numerical damage, healing, or comparable scalable output**; and
- a **diminished version of one compatible defining special property**, where applicable.

The Secondary does not normally gain:
- separate targeting;
- a second independent attack roll;
- its complete original area or targeting structure;
- its complete original duration;
- every rider or special property of the original technique.

A composite spell is therefore one spell with a dominant Primary chassis and a reduced Secondary contribution, not two fully resolved spells stapled together.

#### VP cost

> **Composite VP Cost = full Primary VP cost + full Secondary VP cost**

There is no default VP discount. Composite Casting provides **action compression, not VP efficiency**.

#### Action cost

The composite spell uses the **slower action requirement** of its two techniques:
- Attack Unit + Attack Unit → **1 Attack Unit**;
- Attack Unit + Full Action → **1 Full Action**;
- Full Action + Full Action → **1 Full Action**.

This intentionally supports two different High Scholar combat patterns:
- **Combat Caster:** frequent Attack-Unit composites can create rapid burst and rider stacking, but consume VP extremely quickly;
- **Battlemage:** expensive Full-Action composites can compress what would otherwise require two Full Actions into one turn, but still pay both techniques' VP costs.

The governing tactical question is always: **does getting the Secondary effect right now justify paying for both techniques right now?** Ordinary single-spell casting should often remain the more VP-efficient choice.

### Level 2 — Expanded Repertoire — **LOCKED structure / PROVISIONAL counts**

The High Scholar learns additional techniques and expands the toolbox rather than receiving a generic raw-potency bonus.

There is no requirement to distribute selections evenly among damage, healing, control, support, mobility, defense, or utility. Broad generalists and deliberately focused Scholar repertoires are both valid.

### Level 3 — Formula Fluency — **LOCKED**

At level 3, the requirement to prepare individual composite pairings is removed. Any compatible pair of known techniques may be synthesized **directly at casting time**, without the Scholar having designated that exact pairing during preparation.

Knowing techniques A, B, C, and D is sufficient to attempt compatible A+B, A+C, B+D, etc. combinations. This prevents the combination system from turning into a second exponentially growing spells-known list while making level 3 the point where live technical synthesis comes online.

Formula Fluency does not remove the normal composite VP cost or Secondary reduction.

### Level 4 — Expanded Repertoire + Ability Increase — **LOCKED structure / PROVISIONAL counts**

The High Scholar gains:
- the universal level-4 **+1 Ability** increase; and
- another meaningful repertoire expansion.

No Scholar-specific generic damage, healing, save-DC, or potency increase is added here. Level progression, Veil Control scaling, VP growth, and additional learned tools already improve the character.

### Level 5 — Advanced Synthesis — **LOCKED**

When Composite Casting, the High Scholar chooses how the Secondary Technique is incorporated.

#### Numerical Emphasis

The Secondary contributes approximately **half of its normal numerical output**, while any incidental special property is strongly diminished.

Use this when the added damage, healing, movement, barrier value, or other numerical contribution is the important part of the combination.

#### Property Emphasis

The Secondary contributes **little or no numerical output**, but one compatible defining non-numerical property is preserved substantially more strongly than under ordinary Composite Casting.

Examples include emphasizing knockback, regeneration suppression, concealment, restraint, interruption, terrain alteration, or another defining rider instead of Secondary damage/healing.

Advanced Synthesis improves the Scholar's ability to construct the **right answer for the situation** rather than simply increasing total spell output.

### Playstyle support — **LOCKED design requirement**

The High Scholar foundation must remain viable for multiple caster playstyles, including:
- **Combat Caster:** competent normal Attack-Unit casting with composites available for expensive burst or riders;
- **Battlemage:** large Full-Action spells with expensive composite action compression when two effects are needed immediately;
- **Controller:** broad restraint, terrain, disruption and suppression selection;
- **Support / healer:** competent ordinary healing, protection, cleansing, mobility and utility when those techniques are learned;
- **Generalist toolbox:** deliberately broad selection covering party gaps and exploration problems;
- **Focused Scholar:** a player may select many techniques serving one role, while remaining mechanically distinct from an archetype with innate Aspect specialization.

**Core design rule:** the High Scholar's ordinary magic is fully competent. Composite Casting is a situational technical advantage, not a mandatory rotation or a tax on baseline effectiveness.

---

## LOCKED — Low Scholar Foundation, Levels 1–5

The **Low Scholar** is a prepared, martial-first cross-Pillar toolbox. Its Scholar identity is individually learned technical access to techniques from many Pillars and Aspects; its Low-Focus identity is **Embodiment, preparation, commitment, and selective VP expenditure** rather than rapid mid-combat reconfiguration.

**Core play question:** *What did I prepare, what is worth activating for this encounter, and when is spending scarce VP better than relying on ordinary martial actions?*

The Low Scholar remains fully capable of fighting without magic. Attack, Guard, Dodge, Shove, Grapple, Feint, Riposte and other normal combat actions remain a valid default, and conserving VP is intentional gameplay.

### Known, Prepared, and Active

Low Scholar techniques exist in three layers:

1. **Known Techniques** — everything the Scholar has learned. Scholars may learn techniques from any Pillar or Aspect, subject to normal learning requirements.
2. **Prepared Techniques** — a limited subset configured in advance for ready adventuring/combat use. Exact prepared-technique counts remain **PROVISIONAL** until the spell list is large enough to calibrate repertoire size.
3. **Active Embodiments** — the much smaller subset of prepared inward/equipment techniques currently sustained on the Scholar or their equipment.

This preserves broad Scholar potential while making advance preparation matter.

Example prepared loadouts may include techniques such as a Fire-Pillar flaming weapon, Lightning weapon, Lightning Reflexes, Earth-Pillar Stone Skin, Strength-Pillar physical enhancement, poison resistance, Cheat Death, Wind Wall, Seismic Shock, enhanced senses, concealment, emergency healing, or other learned Aspect techniques.

### Embodiments and switching

An **Embodiment** is a prepared inward or equipment-focused technique that alters the Scholar or their immediately used equipment. Examples include:

- Flaming Weapon / Lightning Weapon
- Lightning Reflexes
- Stone Skin
- Strength enhancement
- Poison resistance
- enhanced senses
- movement enhancement
- Cheat Death

An Embodiment uses its listed activation action, commits its listed VP, and may also spend VP on activation if the technique specifies it.

The Low Scholar **does not receive Medium-style rerouting**. To change from one active Embodiment to another, the Scholar must release the existing effect and activate the replacement normally. Released Committed VP returns to Available VP, but any VP already Spent to establish or intensify the previous effect remains Spent. This makes changing plans possible but intentionally inefficient with the Low Focus's smaller VP pool.

The intended behavior is that a Low Scholar often commits to the best overall enhancement for the encounter rather than switching between Fire, Lightning, defense, movement, etc. every round. Rapid adaptation is the Medium Scholar's identity.

### Active Embodiment hard limit

The Low Scholar has a hard limit on simultaneous Active Embodiments so that a large late-game VP pool cannot simply sustain every available inward enhancement permanently.

- **Levels 1–3:** maximum **1 Active Embodiment**.
- **Levels 4–5:** maximum **2 Active Embodiments**.

Where two effects compete for the same physical/equipment channel, they remain mutually exclusive even if the Scholar has spare Embodiment slots.

### Outward techniques

Low Focus does not prohibit projection. A Low Scholar may prepare and cast outward techniques such as **Wind Wall**, **Seismic Shock**, emergency healing, battlefield obstruction, short-range projection, or similar effects.

These use their normal Attack Unit / Full Action / Reaction requirements and normal VP costs. Because the Low Scholar has the smallest Scholar VP pool, outward casting is normally a **selective reserve expenditure**, not the character's default turn loop.

### Level 1 — Prepared Arsenal

The Low Scholar gains **Prepared Arsenal**:

- access to individually learned techniques from any Pillar/Aspect;
- a limited Prepared Technique loadout selected during suitable preparation;
- maximum **1 Active Embodiment**;
- ordinary prepared outward techniques remain available at their normal action and VP costs.

Exact known/prepared technique counts remain **PROVISIONAL** pending spell-list calibration.

### Level 2 — Field Preparation

The Scholar expands both their learned repertoire and prepared loadout capacity. This level reinforces cross-Pillar preparation rather than raw magical potency.

The player may prepare a generalist kit or deliberately bias the loadout toward a specific anticipated threat, environment, or role. Poor preparation is allowed to matter; the Low Scholar is not expected to have every known solution immediately ready.

### Level 3 — Deep Embodiment

The Low Scholar gains **Deep Embodiment**.

A compatible Active Embodiment may be **Intensified** by paying additional VP specified by the technique. Intensification strengthens the technique the Scholar already chose rather than switching to another effect.

Examples include stronger Lightning Reflexes, greater Stone Skin protection, improved poison resistance, stronger Strength enhancement, deeper Cheat Death protection, or a more forceful weapon enhancement.

This is the Low Scholar's preferred way to spend more power during an encounter: **lean harder into the prepared decision** rather than constantly rerouting it.

### Level 4 — Dual Embodiment

Alongside the universal **+1 Ability** increase, the Low Scholar's Active Embodiment limit increases from **1 to 2**.

Both Embodiments must be prepared and pay their own normal commitment/activation costs. Channel conflicts still apply.

Examples include:

- weapon enhancement + Lightning Reflexes;
- Stone Skin + Strength enhancement;
- enhanced senses + bow/accuracy support;
- poison resistance + Cheat Death;
- concealment-oriented embodiment + movement enhancement.

### Level 5 — Entrenched Configuration

The Low Scholar becomes more efficient when **sticking with the configuration they chose**.

If an Active Embodiment has remained unchanged continuously since the start of the Scholar's previous turn, the next **Intensification** of that Embodiment costs **1 VP less**, minimum 1 VP unless a technique explicitly permits zero.

Changing or replacing that Embodiment breaks the entrenched state and the new effect must first remain stable for the required duration before receiving this benefit.

This rewards preparation and commitment without making all passive effects permanently cheaper and without creating Medium-style rapid switching.

### Locked Low Scholar play pattern

The intended Low Scholar loop is:

1. **Learn broadly** across Pillars/Aspects.
2. **Prepare narrowly enough that choices matter.**
3. Enter an encounter relying on ordinary martial competence.
4. Activate one or two Embodiments when their benefit justifies tying up VP.
5. Prefer **Intensifying** a good choice over swapping repeatedly.
6. Spend additional VP on outward techniques only when the situation warrants it.
7. Accept that changing from one enhancement to another mid-fight is possible but costly and not the Low Focus's identity.

The Low Scholar must support multiple martial or hybrid playstyles, including Fighter, Defender, Spellblade-like weapon enhancer, Assassin, Archer, survivalist, and utility/support builds, without turning any one of them into the class's mandatory identity.

**Core design rule:** High Scholar asks *“Which spell solves this?”* Medium Scholar asks *“Where should my power be routed right now?”* Low Scholar asks *“What did I prepare, and is spending VP on it worth more than simply fighting?”*


---

## LOCKED — Universal VP by Focus and Priest Resonance Foundation v0

### Universal Max VP — **LOCKED**

Maximum VP is determined by **Focus, Veil Affinity, and character level**, not by a Focus × Archetype matrix.

- **High Focus:** `max(1, 6 + Veil Affinity) × Level`
- **Medium Focus:** `max(1, 4 + Veil Affinity) × Level`
- **Low Focus:** `max(1, 2 + Veil Affinity) × Level`

Archetypes differentiate **how** characters access, prepare, amplify, route, stabilize, or otherwise exploit Veil power rather than receiving separate base reservoirs. Individual archetype features may interact with VP, but should not alter this universal Max VP progression unless later playtesting demonstrates a systemic need.

This creates a deliberate balance anchor: characters of the same Focus and Veil Affinity have the same fuel reservoir even when their archetypes use that reservoir very differently.

### Priest Resonance — core meaning — **LOCKED**

**Resonance** is a slow-moving measure of internal coherence between a Priest's genuine beliefs, intentions, actions, and the principles of their chosen Pillar. It is **not morality** and should normally change through sustained play rather than encounter-by-encounter optimization.

Retain the **−3 to +3** scale:

| Resonance | Priest state |
|---:|---|
| **+3** | Deeply aligned |
| **+2** | Strongly aligned |
| **+1** | Stable |
| **0** | Conflicted / uncertain |
| **−1** | Dissonant |
| **−2** | Severe conflict |
| **−3** | Fundamentally opposed / inverted relationship |

A Priest's connection becomes clearer when belief, intent and behavior remain coherent with the Pillar. Doubt by itself is not automatically dissonance; hypocrisy, self-deception, or sustained action fundamentally opposed to the Priest's actual professed relationship with the Pillar are stronger causes of decline. Exact adjudication cadence remains **PROVISIONAL** and should avoid rewarding performative micro-optimization.

### Chosen Pillar and daily prayer — **LOCKED FOUNDATION**

A Priest is tied to **one chosen Pillar** and may draw from **all three Aspects** of that Pillar. Unlike Scholars, Priests do not individually learn every technique as permanent technical knowledge.

During suitable **daily prayer/preparation**, the Priest selects a limited number of techniques from the chosen Pillar to have prepared. The Priest may change that selection during the next suitable prayer/preparation period.

Exact base prepared-technique counts remain **PROVISIONAL** pending spell/technique-list calibration.

### Resonance and prepared access — **LOCKED STRUCTURE / PROVISIONAL FLOOR**

Positive Resonance increases how much of the Pillar the Priest can hold ready:

- Resonance **+1:** base prepared capacity **+1** technique.
- Resonance **+2:** base prepared capacity **+2** techniques.
- Resonance **+3:** base prepared capacity **+3** techniques.

Negative Resonance correspondingly reduces prepared access, but an appropriate minimum prepared-capacity floor must be retained so a Priest remains playable. The exact floor and base preparation counts remain **PROVISIONAL**.

Resonance does **not** routinely raise the Priest's normal maximum spell/technique tier.

### Miracle Petition — **LOCKED FOUNDATION / PROVISIONAL FREQUENCY**

A Priest with positive Resonance may receive limited access to a technique **one tier above their normal maximum**. This is a special **Miracle Petition**, not ordinary tier progression.

Current structure:

- **Resonance +1:** the one-tier-higher Miracle is selected during prayer/preparation.
- **Resonance +2:** the Priest may choose the one-tier-higher Miracle more flexibly when it is invoked, provided it is a valid technique of the chosen Pillar.
- **Resonance +3:** improve **flexibility and/or frequency**, rather than routinely allowing a two-tier jump.

The current starting benchmark is **one Miracle Petition per 24 hours**. Exact frequency and any high-Resonance improvement remain **PROVISIONAL** pending tier and encounter calibration.

### Pillar Resonance Bonus — **LOCKED**

Positive Resonance grants a small **Pillar Resonance Bonus** equal to the Priest's positive Resonance, maximum **+3**.

This bonus is **not effective Veil Control**. It therefore does not enter formulas where Veil Control is multiplied by level or otherwise strongly scaled. Instead it applies as a small final-effect modifier where appropriate, for example:

- +1 / +2 / +3 final damage;
- +1 / +2 / +3 final healing;
- +1 / +2 / +3 barrier strength;
- +1 / +2 / +3 movement distance where an effect uses squares;
- or another technique-specific minor benefit of comparable weight.

Do **not** routinely add the Pillar Resonance Bonus to spell attack rolls or resistance/save difficulty. Those uses are substantially more powerful than the intended small potency benefit and require explicit technique-specific permission if ever used.

Negative Resonance does not automatically impose matching damage/healing penalties. Reduced preparation breadth and loss of Miracle access are already meaningful consequences; avoid double punishment.

### Legacy Priest Resonance rules — **RETIRED**

The following legacy mechanics are superseded for Priests:

- Faith Rest resetting Resonance;
- VP recovery reduction or restoration based on Resonance;
- global spell-level-based or fixed VP-cost modifiers from Resonance;
- percentage miracle-inversion tables;
- automatic universal inversion at −3;
- legacy Wisdom-save Resonance Collapse;
- treating a brief meditation/prayer as sufficient to erase genuine ideological conflict.

### Archetype contrast — **LOCKED DESIGN RULE**

- **Scholar:** permanently learns selected technical methods from potentially any Pillar/Aspect.
- **Priest:** re-prepares techniques from all three Aspects of **one chosen Pillar**, with Resonance controlling prepared breadth, a small potency benefit, and limited Miracle access.

Focus then determines how that archetype relationship is expressed in play; it does not change the universal Max VP formula.

---

## LOCKED — High Priest Foundation, Levels 1–5

### Core identity — **LOCKED**

The **High Priest** is the strongest projected/caster expression of one chosen Pillar. A High Priest has broad daily access across all three Aspects of that Pillar rather than cross-Pillar learning.

**Core play question:** *Which prayers did I prepare efficiently, and is this situation important enough to reach beyond them?*

The High Priest does **not** gain Scholar Composite Casting, Medium-style rerouting, or Low-style Embodiment emphasis.

### Priest spell-access layers — **LOCKED STRUCTURE**

High Priest access is divided into three layers:

1. **Pillar Catalogue** — potential access to techniques of the chosen Pillar, across all three Aspects, up to the Priest's normal maximum technique tier and subject to any individual prerequisites. Priests do not individually learn every technique like Scholars.
2. **Prepared Prayers** — during daily prayer/preparation, choose a limited number of techniques from the Pillar Catalogue. Prepared Prayers use their normal action cost, normal VP cost, and normal Resonance benefits. High Priest should have the largest base Prepared Prayer capacity among the three Priest Focuses. Exact base counts remain **PROVISIONAL** pending spell-list calibration.
3. **Miracle Petition** — the separate Priest-wide Resonance feature allowing limited access to a technique one tier above the Priest's normal maximum. Open Invocation never substitutes for Miracle Petition and cannot exceed the normal-tier limit.

### Level 1 — High Liturgy + Open Invocation — **LOCKED STRUCTURE / PROVISIONAL SURCHARGE**

**High Liturgy** establishes the High Priest's daily Prepared Prayer system.

**Open Invocation** allows the High Priest to invoke an unprepared technique from the chosen Pillar if:

- it is within the Priest's normal accessible tier range;
- it is not a Miracle-tier technique;
- the Priest meets all normal prerequisites.

An Open Invocation:

- pays the technique's normal VP cost;
- adds an additional **Invocation Surcharge**;
- at levels 1–4 requires at least a **Full Action**, even if the prepared version would normally require only an Attack Unit.

The exact Invocation Surcharge remains **PROVISIONAL** until spell VP costs are calibrated. It must be significant enough that good preparation is meaningfully more efficient than repeatedly improvising.

#### Focus boundary

Open Invocation is primarily for projected or immediate magic. Long-lived inward/Embodiment-style configurations should generally need to be **Prepared Prayers** rather than being casually established through spontaneous High-Focus invocation.

### Level 2 — Expanded Liturgy — **LOCKED STRUCTURE / PROVISIONAL COUNTS**

Increase Prepared Prayer capacity. This expands daily breadth within the chosen Pillar rather than granting generic potency.

### Level 3 — Open Prayer — **LOCKED**

During daily prayer, the High Priest may leave **one Prepared Prayer slot unspecified** as an **Open Prayer**.

When first used, choose any eligible technique from the chosen Pillar within the Priest's normal tier limit. That technique immediately fills the Open Prayer slot and counts as Prepared for the remainder of the current preparation cycle.

The same Open Prayer slot cannot repeatedly transform into different techniques during the day.

### Level 4 — Expanded Liturgy + Ability Increase — **LOCKED STRUCTURE / PROVISIONAL COUNTS**

The High Priest gains:

- the universal level-4 **+1 Ability** increase; and
- another meaningful increase in Prepared Prayer capacity.

Do not add a generic damage, healing, save-difficulty, or Resonance multiplier at this level.

### Level 5 — Fluent Invocation — **LOCKED**

Open Invocation no longer automatically increases the invoked technique to a Full Action.

An eligible unprepared technique uses its **normal listed action requirement** while still paying the Invocation Surcharge.

Preparation therefore remains the VP-efficient mode, while the mature High Priest gains substantially stronger spontaneous flexibility inside the chosen Pillar.

### Resonance interaction — **LOCKED**

High Priest uses the Priest-wide Resonance rules unchanged:

- positive Resonance adds **+1/+2/+3 Prepared Prayer capacity** at Resonance +1/+2/+3;
- positive Resonance grants the small **Pillar Resonance Bonus** to appropriate final effect values;
- positive Resonance governs **Miracle Petition** access.

Resonance does not become effective Veil Control.

### Intended High Priest loop — **LOCKED DESIGN RULE**

- **Prepared Prayer** — efficient expected answer.
- **Open Invocation** — unprepared normal-tier answer at a meaningful VP premium; Full Action at levels 1–4, normal listed action at level 5+.
- **Miracle Petition** — exceptional one-tier-higher access through positive Resonance.

### High Priest vs High Scholar — **LOCKED IDENTITY BOUNDARY**

- **High Scholar:** individually learns across many Pillars, builds a broad technical toolbox, uses prepared composites at levels 1–2 and on-the-fly synthesis from level 3.
- **High Priest:** remains bound to one Pillar, re-prepares techniques from all three Aspects, gains costly spontaneous access within that Pillar, and relies on Resonance and Miracle Petition rather than technical synthesis.

### Deliberately unresolved calibration points
The following remain **PROVISIONAL** and should be calibrated against the final spell/tier economy:

- exact base Prepared Prayer counts by level;
- exact Open Invocation VP surcharge.

---

## Post-audit locked decisions — Medium Priest Foundation v0

### Core identity — **LOCKED**

The **Medium Priest** is the active minister and distributor of one chosen Pillar. Its core question is: **“Who needs my Pillar’s power right now?”**

The Medium Priest is not primarily a spontaneous projector like the High Priest and is not a technical internal rerouter like the Medium Scholar. Its flexibility comes from placing and redistributing prepared blessings while still mixing ordinary combat and outward prayer casting.

### Priest access — **LOCKED STRUCTURE / PROVISIONAL COUNTS**

The Medium Priest uses the Priest-wide access structure:

- potential access to the chosen Pillar's techniques across all three Aspects through the **Pillar Catalogue**;
- a limited daily selection of **Prepared Prayers**;
- normal Priest-wide **Miracle Petition** access through positive Resonance.

Medium Priest should have fewer base Prepared Prayers than High Priest. Exact preparation counts remain **PROVISIONAL** pending spell-list and tier calibration.

Medium Priest does **not** gain High-Priest Open Invocation. Its flexibility comes from distributing prepared power, not spontaneously invoking unprepared techniques.

### Consecrations — **LOCKED**

Certain prepared Priest techniques have the **Consecration** property.

A Consecration is a sustained blessing placed on an eligible recipient or anchor defined by the individual technique. Valid targets may include:

- self;
- ally;
- weapon;
- shield;
- armor;
- another wielded or carried object;
- a small location or other anchor where the technique explicitly permits it.

Consecrations retain their actual Pillar and Aspect identity. They are not generic universal buffs.

### Level 1 — Consecrated Ministry — **LOCKED**

At levels 1–3, the Medium Priest may maintain a maximum of **1 Active Consecration**.

An Active Consecration:

- must be a Prepared Prayer;
- uses its normal activation action;
- commits its listed VP;
- remains active according to the technique;
- may be freely released, returning Committed VP according to the core VP rules.

#### Reassign Consecration

The Medium Priest may move the same Active Consecration to another valid recipient.

- Reassignment costs **1 Attack Unit**.
- The new recipient must be valid for the same technique and within its allowed reassignment range.
- The effect itself does not change; only the recipient changes.
- Reassignment does not permit an unprepared technique and does not transform one Consecration into another.

Example: **Fire Ward on self → Fire Ward on ally** is valid reassignment. **Fire Ward → Flaming Weapon** is not; the Priest must release the first effect and activate the second normally.

### Level 2 — Expanded Ministry — **LOCKED STRUCTURE / PROVISIONAL COUNTS**

Increase Prepared Prayer capacity. This broadens what the Medium Priest can potentially minister without increasing Active Consecration count or granting a generic potency increase.

### Level 3 — Intercession — **LOCKED STRUCTURE / PROVISIONAL VP COST**

When another valid recipient within the active Consecration's appropriate range is about to face an event to which that Consecration could meaningfully apply, the Medium Priest may use their **Reaction** and spend additional VP to momentarily extend that same Consecration to the recipient for the triggering resolution only.

- The original recipient retains the Consecration.
- The temporary recipient gains the relevant benefit only for the triggering resolution.
- The extension ends immediately after that resolution.
- The technique must genuinely apply to the triggering event and must permit the recipient type.

Current benchmark cost:

> **Intercession = 2 Spent VP**

This cost remains **PROVISIONAL** pending individual spell and technique calibration.

### Level 4 — Dual Ministry — **LOCKED**

The Medium Priest gains:

- the universal level-4 **+1 Ability** increase; and
- an increase from 1 to **2 Active Consecrations**.

Each Consecration:

- must be prepared;
- commits its own VP;
- follows its own target and duration rules;
- may be reassigned independently.

The two Consecrations may come from different Aspects of the same chosen Pillar.

### Level 5 — Liturgical Relay — **LOCKED**

Once per turn, the Medium Priest may **Reassign one Active Consecration without spending an action**.

This free reassignment:

- does not change the technique;
- does not reduce its VP commitment;
- does not allow an unprepared technique;
- does not duplicate the Consecration.

Additional reassignments during the same turn still cost **1 Attack Unit** each.

### Outward casting — **LOCKED**

Medium Priest may cast ordinary Prepared outward prayers using their normal action and VP costs.

The foundation does not require a buff/support playstyle. It must support multiple viable approaches including fighter/priest, defender, combat caster, healer, controller, weapon enhancer, ranged support, self-focused warrior, and related builds.

### Resonance interaction — **LOCKED**

Medium Priest uses the Priest-wide Resonance rules unchanged:

- positive Resonance adds Prepared Prayer capacity;
- positive Resonance grants the small Pillar Resonance Bonus;
- positive Resonance governs Miracle Petition access.

No separate Medium-Priest Resonance subsystem is added.

### Medium Priest vs Medium Scholar — **LOCKED IDENTITY BOUNDARY**

The two Medium-Focus foundations solve different control problems:

- **Medium Scholar:** changes **what function** inward Veil power performs through technical rerouting; uses individually learned cross-Pillar techniques and Overrouting.
- **Medium Priest:** changes **who receives** an existing prepared Consecration; uses one Pillar across all three Aspects and relies on reassignment and Intercession.

A Medium Scholar may redirect Accuracy into Reflexes or Armor. A Medium Priest may move Fire Ward from one ally to another, but Fire Ward does not become a different prayer merely because it is reassigned.

### Deliberately unresolved calibration points

The following remain **PROVISIONAL**:

- exact Medium Priest base Prepared Prayer counts by level;
- exact Intercession VP cost, with 2 Spent VP as the current benchmark;
- individual Consecration reassignment ranges and recipient restrictions where technique-specific.

---

## LOCKED — Low Priest Foundation, Levels 1–5

### Core identity — **LOCKED**

The **Low Priest** is the most persistent, self-anchored expression of one chosen Pillar. Its Priest identity is daily access to all three Aspects of that one Pillar through prayer and Resonance; its Low-Focus identity is **Devotion, martial reliance, persistent self/equipment blessings, and selective Active Prayer expenditure**.

**Core play question:** *How am I embodying my Pillar today, and when is spending scarce VP worth more than simply fighting?*

Low Priest does not gain High-Priest Open Invocation, Medium-Priest Consecration reassignment, Medium-Scholar rerouting, or Scholar Composite Casting.

### Priest access — **LOCKED**

Low Priest uses the Priest-wide foundation:

- one chosen Pillar;
- access to all three Aspects of that Pillar;
- daily Prepared Prayers selected from the Pillar Catalogue;
- Priest Resonance and its Prepared Prayer bonus;
- the Priest-wide Miracle Petition when Resonance permits it.

Low Priest should have fewer base Prepared Prayers than High Priest. Exact base counts remain **PROVISIONAL** pending spell-list calibration.

### Devotional Rites — **LOCKED**

Certain Prepared Prayers have the **Devotional Rite** property. A Devotional Rite is a sustained inward or immediately worn/wielded expression of the chosen Pillar anchored to the Priest or their own equipment.

Representative examples include:

- Fire: heat resistance, flaming weapon, burning retaliation, purification through flame;
- Strength: physical power, stability, Guard reinforcement, resistance to forced movement;
- Life: poison resistance, disease resistance, regeneration support;
- Death: Cheat Death, pain suppression, wound endurance;
- Order: discipline, steadfastness, resistance to disruption or displacement.

Devotional Rites remain actual Pillar/Aspect techniques rather than generic Low-Focus buffs.

### Level 1 — Chosen Devotion — **LOCKED**

During daily prayer/preparation, the Low Priest designates **one prepared Devotional Rite** as their **Chosen Devotion**.

The Chosen Devotion:

- must belong to the Priest's chosen Pillar;
- must target the Priest or their immediately worn/wielded equipment;
- remains a Prepared Prayer;
- commits VP normally, except its VP commitment is reduced by **1 VP, minimum 1**;
- is the primary anchor for later Low-Priest Exaltation features.

The Low Priest may still prepare and activate other valid Devotional Rites normally; only the Chosen Devotion receives the special efficiency and Exaltation benefits unless another feature says otherwise.

### Level 2 — Devotional Repertoire — **LOCKED structure / PROVISIONAL counts**

Increase Prepared Prayer capacity. This broadens the Low Priest's daily toolset rather than granting generic potency.

A practical Low-Priest loadout may include:

- one or more Devotional Rites;
- one or more Active Prayers that support the martial loop;
- emergency protection, healing, control, or utility appropriate to the chosen Pillar.

Exact Prepared Prayer progression remains **PROVISIONAL**.

### Level 3 — Exaltation — **LOCKED structure / TECHNIQUE COSTS PROVISIONAL**

The Low Priest gains **Exaltation**.

Exaltation allows the Priest to spend additional VP so the **Chosen Devotion temporarily expresses a related secondary property of the same Pillar/Aspect**. Exaltation broadens the devotion's expression rather than merely applying a generic numerical increase.

Examples include:

- Strength enhancement expressing temporary resistance to forced movement or stronger Guard;
- Flaming Weapon expressing brief fire resistance or retaliatory heat;
- Life regeneration support expressing temporary poison resistance;
- Death pain suppression expressing temporary wound suppression or deeper Cheat Death protection.

Each Devotional Rite defines the Exaltation effects compatible with it and their VP costs. A general benchmark of roughly **1–3 Spent VP** is acceptable for early calibration, but exact costs remain technique-specific and **PROVISIONAL**.

### Level 4 — Twofold Devotion — **LOCKED**

Alongside the universal **+1 Ability** increase, the Low Priest may maintain up to **2 Active Devotional Rites** at once, subject to normal compatibility/channel restrictions.

Only one Devotional Rite is the **Chosen Devotion** and receives the Chosen Devotion commitment reduction and Exaltation privileges unless a later feature explicitly expands that rule.

Examples include:

- Flaming Weapon + Heat Resistance;
- Cheat Death + Pain Suppression;
- Strength Enhancement + Stability;
- Regeneration Support + Poison Resistance.

### Level 5 — Living Liturgy — **LOCKED / REWORKED BY 12-COMBINATION AUDIT**

If the Chosen Devotion has remained active and unchanged continuously since the start of the Priest's previous turn, the Priest may use **Living Liturgy** when applying Exaltation to that Devotion.

Living Liturgy allows the Exaltation to express **one authored compatible property from another Aspect of the same chosen Pillar**, rather than being restricted to a secondary property of the Chosen Devotion's own Aspect.

- The Chosen Devotion remains the anchor; Living Liturgy does not activate a second Prepared Prayer.
- The Exaltation pays its **normal listed VP cost**; Living Liturgy does not provide a generic VP discount.
- The cross-Aspect property must be explicitly authored as compatible with that Devotional Rite.
- It does not gain a separate target, action, full technique payload, or independent duration unless the authored Exaltation explicitly says otherwise.
- Only one Living Liturgy cross-Aspect expression may be active on the Chosen Devotion at a time unless a later feature explicitly expands this.
- Changing the Chosen Devotion or allowing it to end breaks the stable state; the new Devotion must again remain unchanged through the required interval before Living Liturgy is available.

Examples of design direction:
- a **Fire / Conflagration** flaming-weapon Devotion may exalt through **Warmth** for protective heat/fire resistance or through **Forge** for exceptional weapon integrity;
- an **Earth / Fortification** Devotion may borrow an authored **Bounty** expression that helps the defended ground sustain or shelter those relying on it;
- a **Life / Preservation** Devotion may borrow an authored **Restoration** expression that supports recovery while the protective Rite remains the anchor.

Living Liturgy therefore rewards sustained devotion by letting the Priest embody **more of the whole Pillar through one stable Rite**. This differentiates it from Low Scholar Entrenched Configuration, which rewards a stable technical configuration with improved efficiency.

### Active Prayers — **LOCKED**

Low Focus does **not** mean passive-only magic. A Low Priest may prepare and use **Active Prayers**: immediate projected effects of the chosen Pillar that support, protect, create openings for, or occasionally replace part of the martial sequence.

Active Prayers use their listed Attack Unit, Full Action, Reaction, and VP costs normally.

Representative Low-Focus Active Prayers include:

- **Earth:** shift or buckle the ground beneath a target to trip or unbalance them, creating an opening for remaining melee attacks; raise a small obstruction;
- **Wind:** Reaction-based brief wind barrier against an incoming projectile; short shove or movement assist;
- **Fire:** short flame burst, ignite an object, force an enemy away;
- **Strength:** concussive shove or momentary impact effect;
- **Life:** touch healing, stabilization, poison suppression;
- **Death:** regeneration suppression, hindering a wounded target;
- **Order:** halt, stabilize, or resist displacement;
- **Water:** slick ground, brief water shield, or knockback.

The defining Low-Focus decision is often whether spending VP on an Active Prayer creates enough advantage to justify not simply using ordinary attacks, Guards, Ripostes, Shoves, or other martial actions.

### Focus identity boundaries — **LOCKED**

- **High Priest:** projection breadth inside one Pillar; prepared prayers plus costly Open Invocation.
- **Medium Priest:** distribution; move the same Consecration between valid recipients and extend it through Intercession.
- **Low Priest:** embodiment and martial support; maintain self-anchored Devotional Rites, deepen the Chosen Devotion through Exaltation, and use selective Active Prayers to create tactical openings or protection.

Low Priest vs Low Scholar:

- **Low Scholar:** broad cross-Pillar technical preparation; chooses among learned tools and may numerically Intensify a prepared Embodiment.
- **Low Priest:** one Pillar across all three Aspects; chooses a Chosen Devotion and may Exalt it into related secondary expressions of that same Pillar/Aspect.

### Deliberately unresolved calibration points

The following remain **PROVISIONAL**:

- exact Low Priest base Prepared Prayer counts by level;
- exact technique-by-technique Exaltation costs and secondary properties;
- individual Active Prayer VP costs and action categories where not already defined by the spell/technique list.

---

## LOCKED UPDATE — Priest Comparative Audit Corrections v0

### Base Prepared Prayer capacity ordering — **LOCKED**

At equal character level and before Resonance modifiers, the three Priest Focuses use the following structural ordering:

> **High Priest base Prepared Prayer capacity > Medium Priest base Prepared Prayer capacity > Low Priest base Prepared Prayer capacity**

Exact numerical progressions remain **PROVISIONAL** pending spell/technique-list calibration. Positive or negative Resonance then modifies the appropriate base capacity according to the Priest-wide Resonance rules.

### Miracle Petition — **REVISED AND LOCKED FOUNDATION**

This section **supersedes** the earlier assumption that a positive-Resonance Priest receives a guaranteed once-per-24-hours one-tier-higher Miracle Petition or that +1/+2/+3 Resonance primarily determines advance selection/flexibility/frequency.

A **Miracle Petition** is an uncertain request for exceptional intervention from the Priest's chosen Pillar. It is not a guaranteed daily resource.

#### Eligibility

- The Priest must have **positive Resonance**.
- The requested technique/effect must genuinely belong to the Priest's chosen Pillar.
- The normal benchmark remains access to a technique **one tier above the Priest's normal maximum technique tier**. A Petition does not normally jump two or more tiers unless a later explicit rule says otherwise.
- A Miracle Petition grants exceptional access to the requested effect; it does not permanently add that technique to Prepared Prayers.

#### Petition check — **LOCKED STRUCTURE / PROVISIONAL NUMBERS**

When the Priest petitions for a Miracle, make a dedicated **Miracle Petition roll**. Success chance increases with positive Resonance and decreases with outstanding **Miracle Debt**.

Current calibration benchmark:

> **d20 + (2 × Resonance) − (3 × Miracle Debt) vs 12**

This produces approximately:
- Resonance +1, no debt: 55% success;
- Resonance +2, no debt: 65% success;
- Resonance +3, no debt: 75% success;
- each outstanding Miracle Debt reduces the chance by roughly 15 percentage points.

The formula is **PROVISIONAL for numerical calibration**, but the structure is locked: higher Resonance improves the chance; accumulated Miracle Debt makes repeated miracles progressively less likely.

#### On success

- The Pillar answers the Petition and the requested one-tier-higher technique may resolve.
- Unless the individual Miracle explicitly says otherwise, it uses its **normal listed action requirement and normal VP cost**. The Petition grants access, not free VP or free action economy.
- The successful Miracle creates **+1 Miracle Debt**.
- Sustained effects continue for their normal duration; the Priest does not accumulate additional Debt merely because one successful Miracle remains active.

#### On failure

- The Pillar does not answer that Petition.
- The attempted action is consumed, but no VP is spent unless a specific effect says otherwise.
- A failed Petition does **not** create Miracle Debt because no Miracle occurred.
- The same Petition cannot simply be spammed repeatedly in the same situation. The Priest may petition again only after the circumstances materially change, a new distinct crisis arises, or the GM judges that a genuinely new Petition is being made.

### Miracle Debt — **LOCKED**

Miracle Debt represents accumulated exceptional favor already granted by the Pillar. It is not ordinary VP debt and does not reduce Max VP.

- Each successful Miracle Petition adds **1 Miracle Debt**.
- Outstanding Debt lowers the chance that later Miracle Petitions are answered.
- There is no automatic daily reset.
- Debt is primarily repaid through the same narrative process that would otherwise increase Resonance.

### Resonance Advance or Debt Repayment — **LOCKED**

Resonance increases are not generated by routine spell use or encounter-by-encounter optimization. The **GM determines when the Priest has earned a Resonance Advance**, normally because the Priest:

- has acted with sustained and unusually strong coherence with the chosen Pillar;
- performs an exceptional deed in service of the Pillar;
- resolves a major conflict in a way genuinely aligned with the Pillar's principles;
- or reaches another comparable narrative milestone.

When the Priest would gain **+1 Resonance**, the player chooses one of the following:

1. **Increase Resonance by +1**, up to the normal maximum of +3; or
2. **Repay 1 Miracle Debt** instead, leaving Resonance unchanged.

Example: a Priest at Resonance +1 with 1 Miracle Debt earns a Resonance Advance. They may become Resonance +2 and retain the Debt, or remain at +1 and reduce Miracle Debt from 1 to 0.

At Resonance +3, a further earned Resonance Advance cannot raise Resonance above +3, so it may instead repay Miracle Debt where applicable.

A Resonance loss caused by dissonance, hypocrisy, or sustained conflict with the Pillar cannot be redirected into Debt repayment. Miracle Debt does not shield the Priest from Resonance loss.

### Design intent — **LOCKED**

Miracle Petition should feel like uncertain exceptional favor rather than a scheduled resource. A highly aligned Priest is more likely to be answered, but repeated successful intervention creates an accumulating obligation and progressively weaker odds until the Priest again demonstrates meaningful service/alignment and chooses to repay that debt.

This keeps Miracles player-invoked but prevents them from becoming a predictable daily spell slot, while giving the GM a narrative lever through Resonance Advances rather than direct control over whether an individual Petition automatically succeeds.

---

## LOCKED — Universal Technique Tier Progression and Tier-9 Miracle Petition

### Universal technique tiers — **LOCKED**

Veilbound uses technique/spell tiers **0 through 9**.

Tier 0 is available whenever the character/archetype has access to the relevant technique.

Maximum normal technique tier is determined by **character level universally across Focus**:

| Character level | Maximum normal technique tier |
|---:|---:|
| 1–2 | 1 |
| 3–4 | 2 |
| 5–6 | 3 |
| 7–8 | 4 |
| 9–10 | 5 |
| 11–12 | 6 |
| 13–14 | 7 |
| 15–16 | 8 |
| 17–20 | 9 |

### Focus does not cap technique tier — **LOCKED**

High, Medium, and Low Focus all eventually gain normal access up to **Tier 9**.

Focus differentiates:
- maximum VP reservoir;
- Physical Tempo;
- action/resource emphasis;
- and the way archetype-specific mechanics express Veil power.

Focus does **not** determine a lower maximum spell/technique tier. A Low-Focus character may therefore use Tier-9 techniques, but the smaller Low-Focus VP pool makes such use a much larger relative resource commitment.

### High-tier content design — **LOCKED**

High-tier techniques are not exclusively large projected caster effects.

For every Pillar, at least one Aspect should continue to offer meaningful **inward, martial-support, defensive, mobility, embodiment, or comparable non-artillery techniques** at higher tiers where thematically appropriate. This preserves meaningful Low- and Medium-Focus development through tiers 7–9 rather than making the upper technique tiers functionally High-Focus-only content.

### Miracle Petition at maximum tier — **LOCKED**

Before normal Tier-9 access, a successful **Miracle Petition** grants exceptional access to one eligible technique **one tier above** the Priest's normal maximum, subject to the existing Miracle Petition roll and Miracle Debt rules.

Once the Priest has normal **Tier-9** access, there is no Tier 10. Instead, on a successful Miracle Petition:

- the Priest may invoke **one chosen eligible technique from their chosen Pillar, Tier 0–9**;
- that invocation costs **0 VP**;
- the technique still uses its **normal listed action requirement**;
- normal targeting, duration, attack/resistance, sustaining, and other technique rules still apply;
- the technique is not permanently added to Prepared Prayers;
- the successful Petition still adds **+1 Miracle Debt**.

This changes the meaning of the Petition at the cap:
- **before Tier 9:** the Priest asks the Pillar for access beyond their normal capability;
- **at Tier 9:** the Priest asks the Pillar to bear the VP cost of an otherwise legal invocation.

### Universal technique-expression metadata — **LOCKED FOUNDATION**

Technique entries and persistent-effect packages use a shared metadata vocabulary so archetype features can refer to the same concepts without inventing parallel tag systems. Tags and properties are **permissions/descriptors**, not automatic bonuses; a class feature must still state what it does with the tagged technique.

- **`[Projection]`** — the technique or expression is capable of outward/projected delivery and may interact with features that explicitly require Projection. The tag does not by itself increase range, area, targets, or power.
- **`[Embodiment]`** — the technique or expression is designed to be integrated into the user's body, worn/wielded equipment, or ordinary physical action where an Embodiment feature permits it. The tag does not itself grant action compression or persistence.
- **`Inward`** — the technique routes power into the user or immediately used equipment and, where relevant, occupies an authored inward channel such as Weapon, Reflex, Body, Locomotion, Senses, or Regeneration. `Inward` and `[Embodiment]` may overlap but are not synonymous.
- **`Consecration`** — a Priest-compatible sustained blessing placed on an authored recipient or anchor. Consecration status does not by itself allow reassignment; Medium Priest features provide that behavior.
- **`Devotional Rite`** — a Priest-compatible sustained inward or immediately worn/wielded expression suitable for Low-Priest Devotion/Exaltation mechanics.
- **`Conduit Form` compatibility** — states which Medium-Gifted conduit forms (for example Contact, Ward, Motion, or later authored forms) can express the technique/Aspect package. Unsupported forms remain unsupported rather than being improvised.
- **`Investment` compatibility** — states which Vessel categories a Medium Anointed may validly invest for that technique/Signature/Authority interaction. A physically present target is not automatically compatible.
- **`Cadence`** — declares each persistent output as Continuous, Rider, Pulse, Spend, or another explicitly bounded cadence consistent with the universal Persistent Expression Cadence rule.

Content templates should use these common metadata fields consistently. Archetype-specific rules may add narrower qualifiers, but should not create duplicate terms for an already defined universal concept without a mechanical reason.

---

# Gifted archetype-wide foundation — LOCKED v24

## Gifted emotion–Aspect access

- A Gifted is born with **eight permanent emotion-to-Aspect links**, one for each core emotion: **Joy, Sadness, Anger, Fear, Surprise, Disgust, Trust, Anticipation**.
- Each link is to **one specific Aspect**, not to an entire Pillar.
- The eight linked Aspects are fixed at birth.
- The Gifted has access to the **full technique catalogue** of each linked Aspect up to their normal universal technique-tier limit.
- Gifted do **not** use Priest-style daily preparation and do **not** individually learn techniques like Scholars.
- Emotion is the actual access mechanism: to use a linked Aspect, the Gifted must genuinely evoke the linked emotion, either naturally or deliberately.
- Emotional invocation does not require theatrical outward expression. Memory, focus, concentration, or another genuine internal route is sufficient if it produces the emotion.

## Scholar vs Gifted breadth calibration — **LOCKED DESIGN REQUIREMENT**

Gifted breadth and Scholar breadth are intentionally different rather than measured only by the raw number of techniques appearing on the character sheet.

- **Gifted breadth is large but fixed:** eight full Aspect catalogues are permanently determined at birth and cannot be reselected to solve later campaign needs. Only the currently Active Emotion's linked Aspect is available at a given emotional window.
- **Scholar breadth is configurable:** Scholars may deliberately learn across the full 48-Aspect space and shape their repertoire toward anticipated problems, party gaps, research discoveries, or later campaign needs.

When finalizing Scholar techniques-known/prepared counts and the full technique catalogue, calibration must test **distinct configurable problem coverage**, not merely compare raw technique totals. A broadly constructed Scholar—especially High Scholar—must retain a meaningful advantage in deliberately assembling answers across unrelated Pillars/Aspects, even if a Gifted's eight fixed catalogues contain a large absolute number of techniques.

This requirement does not mean every Scholar always has more immediately usable techniques than every Gifted. Medium/Low preparation and routing constraints still matter, and a Gifted may be exceptionally well matched to a particular campaign because of their fixed birth links. The requirement is that Scholar remains the archetype with the strongest **player-configurable breadth over time**.

## Active Emotion

- The first linked emotion channeled during a turn becomes the Gifted's **Active Emotion**.
- The Active Emotion persists until the start of the Gifted's next turn.
- While it is active, Gifted magic may only be channeled through the Aspect linked to that Active Emotion.
- Ordinary physical actions, movement, attacks, Guard, etc. remain available normally.
- The Gifted cannot switch to another emotion-linked Aspect during the same turn or during intervening reactions before the next turn.
- At the start of the next turn, the Active Emotion ends and a new one may normally be established.

## Emotional intensity

Three states are used:

| State | Meaning | Effect |
|---|---|---|
| **Evoked** | Sufficient genuine emotion to open the link | Normal technique use |
| **Heightened** | Strong genuine emotion | 1 Amplification Step per turn |
| **Overwhelming** | Extreme genuine emotion | Access to 2 Amplification Steps per turn; using the second risks Instability |

## Amplification Steps

- Amplification never raises technique tier.
- Amplification is technique-specific and functions as constrained emotional metamagic.
- Typical categories include **Potency, Reach, Extent, Persistence, Penetration**, and technique-specific **Expression/riders**.
- Each technique defines which Amplifications are legal.
- The same Amplification normally cannot be chosen twice unless the technique explicitly allows it.
- Heightened emotion provides **1 Amplification Step per turn**.
- Overwhelming emotion provides **2 Amplification Steps per turn**.
- Unused Steps expire at the start of the Gifted's next turn.
- Amplification Steps do not add VP cost by default.

## Natural Heightening

- If circumstances naturally produce a strong matching emotion, the Gifted may be Heightened without a check.
- If the strong circumstance persists, it may continue to support Heightened emotion in later rounds.

## Deepen Emotion

A Gifted with only Evoked emotion may deliberately deepen it.

- **Cost:** 1 Attack Unit.
- **Check:** `d20 + Awareness + Emotional Discipline Training + Resonance` vs **DC 12** benchmark.
- **Success:** Evoked becomes Heightened until the Active Emotion ends.
- **Failure:** remains Evoked.
- Failure does not cause Instability.
- Maximum **one Deepen Emotion attempt per turn**.

## Emotional Overload

- A Heightened Gifted may spend **1 Attack Unit** to push the current emotion to Overwhelming.
- No second emotional check is required to enter Overwhelming deliberately.
- Using only the first Amplification Step remains safe.
- Actually using the **second Amplification Step** triggers the Instability Check.
- Exceptionally intense circumstances may produce Overwhelming emotion naturally without spending an Attack Unit.

## Instability Check

- Maximum **one Instability Check per turn**.
- **Trigger:** using the second Amplification Step from an Overwhelming Active Emotion.
- **Check:** `d20 + Veil Control + Emotional Discipline Training + Resonance`.
- **DC:** `12 + ceil(Technique Tier / 2)`.

| Technique Tier | Instability DC |
|---:|---:|
| 0 | 12 |
| 1–2 | 13 |
| 3–4 | 14 |
| 5–6 | 15 |
| 7–8 | 16 |
| 9 | 17 |

### Instability outcomes

- **Success:** both Amplification Steps function normally.
- **Failure by 1–4 — Strained Channel:** technique resolves with the first Amplification Step; the second Step is lost.
- **Failure by 5+ — Manifestation Spill:** technique still resolves with the first Amplification Step; the second Step is lost and an Aspect-appropriate Instability consequence occurs.
- Instability remains an uncontrolled expression of the **same Aspect**. It does not generically invert healing into damage, swap elements, replace the technique with another spell, or randomly target unrelated creatures.
- Aspect-specific **Instability Profiles** will be designed later.
- After a Manifestation Spill, the current emotion remains emotionally dominant into the next turn, though the formal Active Emotion still ends at turn start.

## Emotional Transition

At the start of a new turn, changing emotions normally requires no roll if no powerful emotion is interfering.

If a dominant emotion persists, changing to another linked emotion requires deliberate effort:

| Interference | Cost / DC |
|---|---|
| Heightened dominant emotion | 1 Attack Unit, DC 12 |
| Overwhelming dominant emotion | 1 Attack Unit, DC 15 |
| Particularly severe/direct emotional conflict | GM may increase by roughly +2–3 |

- **Check:** `d20 + Awareness + Emotional Discipline Training + Resonance`.
- **Success:** the desired emotion may become the new Active Emotion.
- **Failure:** the desired emotion cannot be established that turn; the dominant emotional link remains available.
- Maximum **one transition attempt per turn**.
- This rule applies when circumstance or prior Instability makes an emotion genuinely dominant, not every time the player changes emotion between turns.

## Design intent

Gifted breadth is broad across the character sheet but narrow within a tactical sequence. A Gifted possesses eight full Aspect catalogues, but only one emotion-linked Aspect is available at a time. Emotional intensity powers technique-specific amplification; dangerous instability appears only when the Gifted chooses to push Overwhelming emotion into the second Amplification Step.

## Legacy status changes

The following legacy Gifted mechanics are superseded by this foundation:

- mandatory d100 manifestation tables;
- generic random-target free spells;
- generic healing-to-damage or damage-to-healing inversion;
- spell-tier increases from emotional amplification;
- legacy CHA-based emotional checks;
- legacy Faith Rest / short-rest grounding dependencies;
- free manifestations as a normal reward for low control.

The concepts of natural vs invoked emotion, emotional training, deliberate emotional overload, and rare loss of control are retained in the new native system above.

---

# Gifted Emotion × Aspect Compatibility Matrix v2 — LOCKED

## Gifted link creation

- A Gifted has exactly **eight permanent emotion-to-Aspect links**, one for each core emotion: **Joy, Sadness, Anger, Fear, Surprise, Disgust, Trust, Anticipation**.
- Each link must point to a **different Aspect**.
- Each link must also come from a **different Pillar**.
- Therefore every Gifted has exactly **eight linked Aspects drawn from exactly eight different Pillars**.
- No Pillar may appear more than once among the eight links.
- There is **no required distribution** among External, Internal, or Transform Aspects.

## Compatibility ratings

- **S — Strong:** the emotion-to-Aspect relationship is immediately intuitive and requires no special justification.
- **P — Plausible:** the relationship is valid if the player establishes a coherent emotional interpretation for why that emotion resonates with that Aspect.
- **— — No default link:** that pairing is not available by default.
- **Strong and Plausible links are mechanically identical after character creation.**
- A Plausible link requires only a short interpretation **when the link is chosen**. It is not re-argued or re-approved every time the Gifted uses that Aspect.
- The interpretation must explain **why the emotion resonates with the Aspect itself**, not merely why someone feeling that emotion would find that Aspect useful.

| Aspect | Joy | Sadness | Anger | Fear | Surprise | Disgust | Trust | Anticipation |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Order–Law | — | — | P | — | — | P | S | — |
| Order–Constancy | — | P | P | — | — | P | S | — |
| Order–Stability | — | P | — | S | — | P | S | — |
| Liberty–Defiance | P | P | S | — | — | S | — | — |
| Liberty–Autonomy | P | — | P | S | — | P | — | — |
| Liberty–Exploration | S | — | — | — | S | — | — | S |
| Life–Restoration | P | S | — | — | — | P | — | — |
| Life–Preservation | — | P | P | S | — | P | P | P |
| Life–Nature | S | — | — | — | P | — | P | P |
| Death–Plague | — | P | S | S | — | S | — | — |
| Death–Mastery | — | P | P | S | — | P | — | P |
| Death–Spirit | P | S | P | S | P | — | S | P |
| Fire–Conflagration | P | — | S | — | S | — | — | — |
| Fire–Warmth | S | P | — | — | — | S | S | — |
| Fire–Forge | P | — | — | — | — | — | — | P |
| Water–Flow | P | S | P | — | P | — | — | P |
| Water–Calm | P | P | — | — | — | S | S | — |
| Water–Medium | — | — | — | — | — | — | P | P |
| Earth–Quake | — | P | S | S | S | — | — | — |
| Earth–Fortification | — | P | P | S | — | P | S | P |
| Earth–Bounty | S | — | — | — | — | — | P | S |
| Skywinds–Gale | P | P | S | P | S | — | — | P |
| Skywinds–Swiftness | P | — | P | S | S | — | — | S |
| Skywinds–Sky | S | — | — | — | S | — | — | P |
| Lightning–Strike | P | — | S | S | S | — | — | P |
| Lightning–Reflexes | P | — | P | S | S | — | — | S |
| Lightning–Charge | P | — | P | — | P | — | — | S |
| Kinship–Guardian | P | P | S | S | — | — | S | P |
| Kinship–Sacrifice | P | S | P | P | — | — | S | P |
| Kinship–Unity | S | P | P | P | — | — | S | P |
| Strength–Power | P | — | S | P | — | — | — | — |
| Strength–Endurance | — | S | S | S | — | — | P | P |
| Strength–Training | P | P | P | — | — | — | P | S |
| Fortune–Manipulation | — | — | P | — | — | — | — | P |
| Fortune–Charm | S | — | — | — | P | — | S | P |
| Fortune–Luck | S | — | — | — | S | — | P | S |
| Mind–Psionics | — | — | P | — | P | — | P | — |
| Mind–Memory | S | S | P | P | P | P | P | — |
| Mind–Insight | — | — | — | P | S | — | — | S |
| Alchemy–Concoctions | P | — | P | — | S | S | — | P |
| Alchemy–Elixirs | P | P | — | — | P | P | P | P |
| Alchemy–Transmutation | P | — | P | — | S | P | — | P |
| Arts–Performance | S | S | S | P | S | P | P | P |
| Arts–Inspiration | S | P | P | P | S | P | P | S |
| Arts–Creation | S | P | P | P | P | P | P | P |
| Secrets–Deception | P | P | P | S | P | — | — | P |
| Secrets–Shadow | — | S | — | S | P | — | — | P |
| Secrets–Hallucination | P | P | P | S | S | P | — | P |

## Validation

- The matrix has been checked under the **eight-distinct-Pillars** constraint and supports complete legal Gifted builds without forcing invalid links.
- **Strong-only** complete builds are possible.
- Plausible links provide additional character-expression flexibility without increasing mechanical power.
- The compatibility table is a **character-creation constraint**, not an in-play approval procedure. Once a legal link is established, it remains valid for that Gifted.

---

# Gifted — Low Focus Foundation (Locked for current design pass)

## Core identity
Low Gifted embodies one emotion-linked Aspect as a persistent combat state.

Core question:
> “Which part of myself do I need to become, and can I stay there?”

Unlike High Gifted, which pushes projection, and Medium Gifted, which retunes conduits, Low Gifted gains value from committing to one emotion and maintaining it. Low Gifted can still change state when tactically necessary, but doing so costs tempo and resets accumulated emotional momentum.

## Active Emotion vs Anchored Emotion
- **Active Emotion** remains the universal Gifted rule determining which linked Aspect is currently available.
- **Anchored Emotion** is the Low Gifted-specific commitment to one Active Emotion.
- At combat start, the Low Gifted normally establishes one of their eight emotions as Anchored Emotion.
- If uninterrupted, that Anchored Emotion automatically becomes Active again at the start of subsequent turns.
- When the Anchor changes, the new emotion becomes the new Anchor immediately; there is no separate later anchoring action.

## Anchored Embodiment
- The current Anchored Emotion's linked Aspect grants an Aspect-specific **Embodied Expression**.
- Embodied Expression is self-only, persistent during the Active Emotion window, and integrates with ordinary physical play rather than requiring constant recasting.
- Exact expressions are defined per Aspect.
- Example: Anger → Fire/Conflagration can produce a flaming-weapon/offensive fire embodiment.
- Example: Trust → Earth/Fortification can produce a stone-skin/defensive embodiment.
- Example: Fear → Lightning/Reflexes can produce an evasive/reflex embodiment.
- Outside combat, a Low Gifted may deliberately settle into one emotion at a time to gain the corresponding noncombat/preparatory Embodied Expression. Changing emotion ends the previous expression; benefits are not banked.

## Voluntary tactical switch — Break Anchor
A Low Gifted may voluntarily abandon the current Anchor when circumstances demand another Aspect.

**Break Anchor:**
- spend **1 Attack Unit**;
- choose and genuinely evoke another linked emotion;
- no roll is required if no competing dominant emotion is interfering;
- the new emotion immediately becomes Active and becomes the new Anchor;
- the old Embodied Expression ends immediately;
- all persistence benefits, Settled Emotion progress, Deep Embodiment, and emotion-specific intensification tied to the old Anchor end;
- the new emotion begins at **Evoked** intensity; Heightened/Overwhelming intensity does not transfer;
- persistence-based Low Gifted benefits must be built up again from the new Anchor.

Baseline cost is **tempo + loss/reset of momentum**. There is no additional VP tax for voluntary switching.

## Forced emotional disruption
External circumstances may create a genuinely dominant competing emotion, e.g. a dragon roar causing strong Fear while the Gifted is anchored in Anger.

- The old Anchor is disrupted.
- The competing emotion becomes Active at its appropriate natural intensity when the normal Active Emotion window changes.
- The player may accept the competing emotion and use its linked Aspect, or attempt to reassert the Anchor.

**Reassert Anchor:**
- spend **1 Attack Unit**;
- make the normal Emotional Transition check:
  `d20 + Awareness + Emotional Discipline Training + Resonance`;
- Heightened dominant competing emotion: **DC 12**;
- Overwhelming dominant competing emotion: **DC 15**;
- particularly severe/direct conflict may increase roughly **+2–3**.

Success restores the desired Anchored Emotion. Failure means the competing emotion remains Active that turn. Ordinary physical actions remain available regardless.

This keeps emotional effects meaningful without removing player agency.

## Levels 1–5

### Level 1 — Anchored Embodiment
- Establish Anchored Emotion at combat start.
- Gain the linked Aspect's Embodied Expression.
- Voluntary Break Anchor costs 1 AU and resets momentum.
- Fighting a dominant competing emotion costs 1 AU + Emotional Transition check.

### Level 2 — Instinctive Expression
- Embodied Expression explicitly integrates with eligible ordinary physical actions and reactions as defined by the Aspect, including attacks, Guard, Dodge, movement, grapples/shoves, interception, touch, etc.
- It does not grant free actions.

### Level 3 — Settled Emotion
If the same Anchored Emotion remained uninterrupted from the start of the previous turn until the start of the current turn, the Low Gifted may attempt **Deepen Emotion with no Attack Unit cost**.

Use the normal Deepen Emotion check:
`d20 + Awareness + Emotional Discipline Training + Resonance vs DC 12`

- Success: Anchored Emotion becomes Heightened.
- Failure: remains Evoked; no additional penalty.

### Level 4 — Emotional Center + universal +1 Ability
- Gain the universal +1 Ability.
- Gain **+2 on Emotional Transition checks** made specifically to preserve or reclaim the Anchored Emotion.
- Reasserting against disruption still costs 1 AU.

### Level 5 — Deep Embodiment
If the current Anchored Emotion:
- has remained uninterrupted since at least the start of the previous turn; and
- is Heightened;

then its Embodied Expression gains an additional **Aspect-specific Deep Embodiment rider**.

The rider is defined per Aspect rather than as a generic numerical bonus. Breaking or losing the emotional state ends Deep Embodiment immediately.

## Amplification relationship
Low Gifted emotional intensity and Aspect-specific embodiment may later interact with Amplification, but the locked foundation centers on persistent embodiment, emotional commitment, and persistence rewards rather than free per-turn state swapping. Exact numerical effects and individual Aspect Embodied/Deep Embodiment expressions remain for later content design and calibration.

## Design distinction
- **High Gifted:** intensify/project current emotion.
- **Medium Gifted:** persistent conduits automatically retune when emotion changes.
- **Low Gifted:** choose an emotional embodiment and gain increasing value from staying in it, while retaining the option to sacrifice that momentum for a tactically necessary change.


---

# Gifted Comparative Stress Test and Archetype Audit — v27

**Status:** PASS WITH CLARIFICATIONS / CALIBRATION GATES. No structural redesign required.

## Common test Gifted
The same eight-link character is used across all three Focuses:
- Anger → Fire / Conflagration
- Fear → Lightning / Reflexes
- Trust → Earth / Fortification
- Sadness → Life / Restoration
- Joy → Liberty / Exploration
- Surprise → Mind / Insight
- Disgust → Alchemy / Concoctions
- Anticipation → Strength / Training

All eight links use different Aspects and different Pillars.

## Comparative identity result
- **High Gifted:** intensity/projection — asks “How far can I push what I feel right now?”
- **Medium Gifted:** conduction/retuning — asks “What do my established conduits become under this emotion?”
- **Low Gifted:** embodiment/commitment — asks “Which emotional state do I become, and can I hold it?”

The three Focuses remain distinct under identical emotion/Aspect access.

## Scenario stress tests

### 1. Offensive opening — Anger / Fire-Conflagration
- High: casts outward Conflagration and may purchase Projected Surge amplification.
- Medium: existing Contact conduit retunes into a fire expression on weapon/touch.
- Low: anchors Anger and fights through a persistent Conflagration Embodiment such as a flaming blade.
**Result:** PASS. Same Aspect produces three different play loops.

### 2. Ally suddenly needs healing — Sadness / Life-Restoration
- High: on the next legal emotional window, establishes Sadness and can amplify projected Restoration.
- Medium: existing compatible conduits automatically retune to Restoration; Contact can become restorative touch/conduction.
- Low: voluntarily Breaks Anchor for 1 AU, loses accumulated Anger momentum, and establishes Sadness/Restoration at Evoked intensity.
**Result:** PASS. Medium is the most dynamically adaptive; Low pays commitment cost; High pays no stance-loss cost but remains bound by the one-Active-Emotion window.

### 3. Dragon roar causes dominant Fear
- High: may accept Fear/Reflexes or spend 1 AU + Emotional Transition check to establish another desired emotion while Fear remains dominant.
- Medium: same emotional conflict rule; if Fear becomes Active, conduits retune to Lightning/Reflexes expressions.
- Low: preferred Anchor can be disrupted; may accept Fear temporarily or spend 1 AU + Transition check to reassert the Anchor. L4 Emotional Center gives +2 specifically when preserving/reclaiming the Anchor.
**Result:** PASS, but Low forced-disruption wording needs clarification: an externally imposed Active Emotion should not automatically become the new chosen Anchor unless the player deliberately adopts it.

### 4. Multiple Attack Units / high Physical Tempo
- High: PASS because emotional Amplification and Projected Surge are limited by the Active Emotion window and do not refresh per attack or on other creatures’ turns.
- Medium: CALIBRATION GATE. Persistent Contact/Ward/etc. expressions must not grant an unrestricted full-strength damage/healing payload on every Attack Unit unless explicitly balanced for Physical Tempo.
- Low: CALIBRATION GATE. Embodied weapon riders and similar effects must be Tempo-safe; avoid generic level-scaling bonus damage multiplied across every Low-Focus attack.

### 5. Defensive reaction between turns
- High: may reserve unused emotional Amplification / eligible Projected Surge for a compatible Reaction within the same Active Emotion window.
- Medium: conduits retain their current expression until the next Active Emotion is established and can support eligible reactions.
- Low: current Embodiment persists through the window and supports defined reactions/defenses.
**Result:** PASS. No focus refreshes emotional resources on another creature’s turn.

### 6. Resource pressure
- High: spends the most VP when repeatedly buying Projected Surge Steps; high ceiling, high burn.
- Medium: pays committed VP into conduits and pays expensive Reconduction when changing anchor/form; normal emotional retuning itself is free.
- Low: basic Embodiment is persistent/efficient but has the smallest Focus VP reservoir and pays tempo/momentum to change state.
**Result:** PASS. Resource identities are distinct.

### 7. Long combat / changing tactical demands
- High: normally chooses the most useful emotion each new window and pushes output.
- Medium: benefits from deliberate emotional cycling because the same conduit network becomes different tools.
- Low: benefits from staying in one Anchor; changing is possible but resets accumulated benefits.
**Result:** STRONG PASS. This is the clearest three-way Focus differentiation.

### 8. Out-of-combat utility
- All Gifted can sequentially access their eight fixed Aspect catalogues by genuinely evoking the associated emotions.
- High remains projection-oriented; Medium can use appropriate conduit structures; Low can settle into one noncombat/preparatory Embodiment at a time and cannot bank benefits from multiple emotions.
**Result:** PASS PROVISIONALLY. Eight full fixed Aspects create intentionally broad innate access; later technique/repertoire calibration must ensure this does not erase Scholar breadth in practice.

### 9. Emotional manipulation by enemies/environment
- High and Medium gain or lose tactical options depending on which emotion becomes dominant.
- Low is most vulnerable to disruption because momentum can be broken, but gains the best later resistance to reclaiming its chosen state.
**Result:** PASS. Emotional effects matter differently to all three Focuses without removing ordinary physical agency.

### 10. Cross-archetype overlap
- High Gifted vs High Scholar: intensity vs synthesis.
- High Gifted vs High Priest: fixed emotional Aspect access + amplification vs one-Pillar prepared/open prayer access + Miracle Petition.
- Medium Gifted vs Medium Scholar: sticky conduit structures that automatically retune vs cheap deliberate functional rerouting.
- Medium Gifted vs Medium Priest: retunes expression of a conduit network vs redistributes persistent blessings among recipients.
- Low Gifted vs Low Scholar: emotion-determined embodied state vs deliberately prepared/configured Embodiments.
- Low Gifted vs Low Priest: temporary emotional embodiment and persistence vs devotional self-anchored Rites/Exaltation.
**Result:** PASS. No current pair is functionally redundant.

## Resolved Gifted clarifications — v28

**Status:** RESOLVED / LOCKED FOUNDATION. Numerical values inside individual Aspect expressions still require ordinary content calibration, but the seven structural questions exposed by the v27 stress test are resolved below.

### A. Emotion Establishment Step — LOCKED
At the start of each Gifted's turn, after ordinary start-of-turn housekeeping and before normal actions, resolve an **Emotion Establishment Step**.

1. The prior turn's Emotion Window ends.
2. If no dominant competing emotion interferes, the Gifted may genuinely establish any eligible linked emotion at no action cost. That emotion becomes Active.
3. The Gifted may instead leave Active Emotion unset. If so, the first Gifted technique/effect that requires an emotion may establish one at no extra action cost, provided no dominant competing emotion interferes.
4. If a dominant competing emotion is present, it would become Active by default. Before it locks in, the Gifted may spend **1 Attack Unit from the upcoming turn** and make the normal Emotional Transition check to establish a different desired emotion. Success establishes the desired emotion; failure establishes the dominant competing emotion.
5. Low Gifted normally auto-establishes an uninterrupted Anchored Emotion. If that Anchor has been disrupted, use the Low forced-disruption rules below.
6. Medium Gifted conduits re-express immediately when the new Active Emotion is established.

A newly established Active Emotion is normally fixed for the current Emotion Window. Explicit exceptions, such as Low Gifted **Break Anchor**, say otherwise.

### B. Emotion Window terminology and refresh timing — LOCKED
Use **Emotion Window** as the Gifted resource-refresh unit. An Emotion Window begins with the Gifted's Emotion Establishment Step and ends at the next such step.

- Heightened/Overwhelming Amplification Steps are generated once per Emotion Window, not once per creature turn or per attack.
- If the Gifted begins the window Evoked and later becomes Heightened, they gain the first Step at that moment. If they later become Overwhelming, they gain only the second Step; previously spent Steps are not refilled.
- Unused Amplification Steps expire when the Emotion Window ends.
- Deepen Emotion may be attempted at most once per Emotion Window unless a feature explicitly says otherwise.- High Gifted Projected Surge allowances refresh once per Emotion Window.
- The maximum-one Instability Check limit is also per Emotion Window.
- Reactions on other creatures' turns use the same current pool and do not refresh anything.
- If an explicit feature changes Active Emotion inside the same Emotion Window, the window does not restart and its once-per-window resources do not refresh.

This preserves the tactical one-emotion identity while allowing explicitly defined exceptions without resource-reset exploits.

### C. Medium Conduit Grade and power budget — LOCKED FOUNDATION
Every Medium Gifted Conduit has a **Conduit Grade** chosen when the conduit is established. Grade is independent of the currently expressed Aspect and therefore does not change when emotion retunes the conduit.

- **Grade I:** commit 1 VP.
- **Grade II:** commit 2 VP.
- **Grade III:** commit 3 VP.
- All three Grades are available from level 1; choosing a high Grade at low level is balanced by the proportion of the Medium Gifted's VP pool that remains committed.
- Every supported Aspect/Form expression must define how Grade I–III scale. Exact numbers are content calibration, not a class-rule decision.
- Free emotional retuning always retains the same Grade. It can never turn a low-commitment conduit into a higher-grade effect.
- If the newly Active Aspect has no expression for that Conduit Form, the conduit becomes **Dormant** for that emotion rather than improvising a stronger/different effect.
- Changing a conduit Grade counts as **Reconduction**: pay the normal Reconduction action/Spent-VP cost, then commit or release the VP difference as appropriate.
- Changing only Active Emotion never counts as Reconduction.

Each conduit may also have **one Conduit Pulse per Emotion Window** if its current Aspect/Form expression defines a Pulse. The Pulse is a cadence budget for stronger effects, not an additional generic action.

### D. Tempo-safe persistent expressions — LOCKED DESIGN RULE
Every persistent Medium Conduit expression and Low Embodied Expression that can interact with ordinary actions must declare an **Expression Cadence**. Use one or more of:

- **Continuous:** a static/persistent benefit; it does not multiply with Attack Units.
- **Rider:** a modest effect that may apply to each eligible attack/action. Rider values must be calibrated assuming the maximum Physical Tempo that can use them.
- **Pulse:** a stronger effect usable once per Emotion Window (for Medium, normally using that conduit's Conduit Pulse).
- **Spend:** a repeatable stronger effect only by paying an explicit additional VP, Vigor, or other listed cost each use.

A full technique-scale damage, healing, or Vigor-restoration effect must **not** be an unrestricted per-Attack-Unit Rider. Resource restoration in particular must use Pulse, Spend, or another explicit finite budget.

Examples:
- Lightning Contact on a weapon may provide a modest Tempo-safe electrical Rider and optionally a stronger once-window Pulse.
- Restoration Contact on the same weapon may use its Pulse to restore a defined amount of Vigor when the Gifted deliberately touches/taps an ally; it does not restore a full healing payload on every weapon tap.
- Low Conflagration flaming-blade damage may be a modest Rider, while a stronger flare/burn is Pulse or Spend.
- Earth/Fortification stone-skin is naturally Continuous rather than multiplied by attacks.

### E. Low Gifted forced disruption versus chosen Anchor — LOCKED
A Low Gifted's **Anchored Emotion** is a chosen commitment and is distinct from whatever emotion is temporarily Active.

- An externally imposed/dominant emotion can prevent the Anchor from becoming Active, but it does **not** automatically become the new Anchor.
- When this happens, mark the chosen Anchor **Disrupted**. All Settled Emotion progress, sustained Heightening, and Deep Embodiment tied to that Anchor end immediately.
- The competing emotion may become Active for the current Emotion Window and may be used normally, but the chosen Anchor remains the character's Anchor unless voluntarily replaced.
- If the competing emotion is no longer dominant at a later Emotion Establishment Step, the existing Anchor may auto-establish again, but it returns at its normal intensity and must rebuild persistence.
- If the competing emotion remains dominant, the Gifted may spend 1 AU during the Emotion Establishment Step and make the normal Emotional Transition check to reclaim the Anchor.
- The Gifted may instead voluntarily adopt another emotion as the new Anchor via **Break Anchor**.
- **Break Anchor may be used at most once per Emotion Window.** It costs 1 AU, immediately changes Active Emotion and Anchor, resets all prior Anchor momentum, starts the new Anchor at Evoked intensity unless the rules explicitly establish a stronger natural intensity, and does not refresh any once-per-Emotion-Window resources.

### F. Low Gifted Settled Emotion preserves Heightened — LOCKED
At level 3, **Settled Emotion** now creates persistent Heightening rather than requiring repeated Deepen rolls.

- If the same Anchor remained uninterrupted from the start of the previous turn through the current Emotion Establishment Step, the Low Gifted may make the normal Deepen Emotion check with no AU cost.
- On success, mark the Anchor **Settled Heightened**.
- While that same Anchor remains uninterrupted and undisrupted, it automatically establishes at **Heightened** intensity in each later Emotion Window. No further Deepen checks are required.
- Because it begins those windows Heightened, it receives the normal one Heightened Amplification Step each Emotion Window.
- Deliberate Emotional Overload can still raise it to Overwhelming for the current window. Unless an external/natural condition keeps it Overwhelming, it returns to its Settled Heightened baseline next window.
- Break Anchor or forced disruption ends Settled Heightened immediately. A reclaimed/re-established Anchor starts from normal intensity unless naturally Heightened/Overwhelming and must settle again to regain this feature.

This makes Low Gifted reward emotional commitment rather than repeated identical dice checks.

### G. Explicit Projection tag for High Gifted — LOCKED
Techniques now use an explicit **[Projection]** tag when they are eligible for High Gifted **Projected Surge**.

- Projected Surge can only be applied to a technique carrying `[Projection]`.
- Projection eligibility is a property of the individual technique, not of the Aspect category and not simply of whether the target is another creature.
- An Internal or Transform Aspect may contain `[Projection]` techniques.
- An External Aspect may contain techniques that are not `[Projection]` and therefore cannot receive Projected Surge.
- Passive Medium Conduit expressions and Low Embodied Expressions are not automatically Projection-compatible; they require an explicit technique/feature rule if they are ever intended to interact with Projected Surge.

This preserves High Gifted's identity as deliberate outward projection without misclassifying whole Aspects.

## Gifted audit verdict after resolution
**PASS — FOUNDATION RESOLVED; CONTENT/NUMBER CALIBRATION REMAINS.**

The shared Gifted chassis and High/Medium/Low level-1–5 foundations are structurally coherent. Remaining Gifted work is primarily content production and balance calibration:
- write Aspect-specific Amplification options;
- write Medium Conduit Form expressions and Grade I–III scaling;
- write Low Embodied and Deep Embodiment expressions;
- calibrate High Projected Surge VP surcharge and level-4 reduction;
- test persistent Rider/Pulse numbers against Physical Tempo and VP/Vigor economies.

---

# Anointed Origin Model — LOCKED

## Surge-born origin
Anointed are born during exceptional Pillar surges. A surge does **not** require that the Pillar was previously weak, nor does a crisis by itself automatically create a surge. Crisis and recovery are one possible route; successful innovation, flourishing practice, communal achievement, or other positive developments can generate the same conditions.

The general pattern is:

**successful practice → adoption → cultural reinforcement → concentrated collective commitment/celebration → Pillar surge**

A crisis may precede the successful practice, but it is optional rather than foundational.

### What builds toward a surge
A surge becomes more likely or more intense when several conditions converge:

- **Successful practice:** people repeatedly act in ways that realize the Pillar/Aspect concept rather than merely wishing for it.
- **Adoption:** the practice spreads beyond an isolated individual and becomes shared by a community.
- **Cultural reinforcement:** the practice becomes taught, repeated, valued, ritualized, institutionalized, or otherwise embedded in communal life.
- **Conceptual focus:** the participants' desires and volition point toward substantially the same Pillar or Aspect rather than dispersing among unrelated concepts.
- **Successful results:** visible success strengthens confidence, desire, and continued determined action.
- **Synchronization:** a festival, recovery celebration, victory, unveiling, harvest, communal rite, or similar event concentrates otherwise diffuse desire and volition into a shared moment.
- **Explicit prayer or thanks:** formal Pillar recognition can make the conceptual focus especially clean, but formal religion is not mandatory for a surge.

A Priest can materially increase the likelihood of this pattern by giving diffuse wants a coherent conceptual language, encouraging repeatable practices, building institutions, and organizing collective observances. A Priest cannot simply perform a ritual and manufacture an Anointed.

## Examples

### Life / Restoration
A plague may initially weaken Life locally. People begin wanting recovery, a Life Priest or other healers organize sanitation, treatment, clean water, herbal remedies, and care for the sick, and those practices begin succeeding. The community adopts and maintains them. A later celebration of survival and renewed health may synchronize enough collective desire and volition around Life/Restoration to create a surge.

The plague itself is not the surge. The successful, culturally reinforced response to it is what can produce the surge.

### Earth / Bounty
No preceding weakness is required. A farmer discovers a highly effective method of soil fertilization. The village adopts it, improves it, and eventually enjoys an exceptional harvest. The practice becomes culturally important. During a major harvest celebration, the community collectively gives thanks for abundance and commits to maintaining the practices that produced it. The resulting concentrated desire and volition may cause an Earth/Bounty surge.

A child born during that surge could become an Earth/Bounty Anointed with a broad Mission such as **"Make the land flourish and ensure it provides abundantly."** The specific fertilizer technique helped create the surge but is not itself the lifetime Mission.

## Mission imprint
The surge imprints a broad, enduring Mission aligned with the Aspect and with the successful pattern that generated the surge. The originating event shapes the Mission but is not itself the Mission.

Examples:
- Life/Restoration surge born from successful plague recovery → **Heal sickness and restore damaged life.**
- Earth/Bounty surge born from agricultural innovation and harvest abundance → **Make the land flourish and ensure it provides abundantly.**
- Fire/Forge surge born from a culture of exceptional craftsmanship → **Create works worthy of exceptional craft.**

The Mission is intended to guide a lifetime and remain open to interpretation rather than functioning as a finite quest objective.

## Universal Anointed Aspect Intuition — LOCKED
All Anointed possess an instinctive, non-generic sensitivity to patterns genuinely belonging to their bonded Aspect. This is an archetype-wide consequence of the permanent Aspect bond and does not depend on Focus.

Examples:
- **Restoration:** injury, disease, failing recovery, or conditions obstructing healing.
- **Forge:** workmanship, material stress, heat/workability, probable points of failure in crafted objects.
- **Fortification:** structural weakness, instability, defensive integrity.
- **Conflagration:** meaningful heat/fire sources and likely flame behavior.
- **Spirit:** evidence of lingering dead, disrupted passage, or similar Spirit-domain phenomena.

Aspect Intuition is not a universal supernatural detector, Mission compass, or omniscience. It only supplies information that coherently belongs to the bonded Aspect, and normal checks still apply where uncertainty, pressure, concealment, or expertise matter.

## Reinforcement loop
Once born, an Anointed can further strengthen the same conceptual pattern simply by fulfilling the Mission well:

**Anointed advances Mission → visible success demonstrates the Aspect's value → practices, desire, institutions, and cultural commitment strengthen → future Pillar surges become easier or stronger.**

The Anointed does not need to consciously pursue Pillar growth. Their primary motivation is Mission fulfillment. Pillar reinforcement is a systemic consequence of succeeding at that Mission.

This creates the core Priest/Anointed distinction:

- **Priest:** "How do I serve my Pillar, strengthen its presence, and help it grow?"
- **Anointed:** "How do I use what I am to further my Mission?"

A Priest deliberately cultivates Pillar strength. An Anointed pursues the Mission imprinted by the surge; doing so often strengthens the Pillar as a by-product.

---

# High Anointed Foundation — LOCKED STRUCTURE / NUMBERS & CONTENT PROVISIONAL

## Core question
**How can I project the full power of my Aspect to further the Mission that created me?**

The High Anointed remains a one-Aspect specialist. Its play identity is not generic spell amplification, broad Pillar service, or technical synthesis. It projects unusually deep **Aspect Authority** in pursuit of its Mission.

The Anointed-wide conceptual structure is:
- **Mission tells the Anointed why.**
- **Bonded Aspect tells the Anointed what they uniquely command.**
- **Focus tells the Anointed how they express it.**
- **Destiny pays for exceptional moments of Aspect Authority.**

The High Anointed expresses this through projection.

## Birth Imprint — LOCKED CONCEPT
At character creation, the circumstances of the Pillar surge, the bonded Aspect, and the broad lifelong Mission establish a **Birth Imprint**.

The Birth Imprint represents the particular successful cultural/practical pattern whose surge produced the Anointed. It individualizes the Anointed inside the same Aspect without expanding Aspect breadth.

Two Anointed bonded to the same Aspect may therefore have different Birth Imprints and Signature Expressions.

Examples:
- **Earth / Bounty**, agricultural surge: fertility, cultivation, soil abundance, successful harvest practice.
- **Earth / Bounty**, resource-prosperity surge: identifying and improving access to useful earth resources.
- **Life / Restoration**, plague-recovery surge: cleansing disease and restoring health.
- **Life / Restoration**, battlefield-recovery surge: stabilizing trauma and restoring damaged bodies.

A Birth Imprint must remain broad enough to support an adventuring career. It must not be restricted to one hyper-specific historical practice, material, crop, settlement, or event.

**Birth Imprint access boundary — LOCKED:** the Birth Imprint shapes the Anointed's Signature Expression and may determine compatible or favored Authority interactions, but it does **not** remove access to the rest of the bonded Aspect's normal technique catalogue and does **not** grant access to techniques or Authorities outside that Aspect. Birth Imprint individualizes depth; it is not a hidden subclass or a second access system.

## Living Signature — LOCKED CONCEPT / NUMBERS PROVISIONAL
Every High Anointed has a **Signature Expression** shaped by the Birth Imprint.

The Signature Expression is:
- a manifestation of the bonded Aspect;
- tied to the character's Birth Imprint and Mission;
- **0 VP** at its baseline;
- always known and available while the Anointed bond is active;
- deliberately modest enough to coexist with normal techniques, weapons, and other zero-cost actions;
- explicitly tagged **[Signature]** and **[Projection]** for High Anointed use;
- scaled by its own Aspect/Birth-Imprint definition rather than by a universal legacy damage/healing dice table.

The old universal Signature scaling table is retired. A Signature is not merely the same spell with a different damage type.

## Aspect Authority — LOCKED CONCEPT
**Aspect Authority** is the defining depth mechanic of the Anointed.

Authority represents effects that are unusually absolute, deep, or privileged expressions of the bonded Aspect and are not normally available to other users of the same technique.

Authority is:
- Aspect-specific rather than generic metamagic;
- not a technique-tier increase;
- not a universal menu of damage, range, area, duration, target, or save modifiers;
- authored as compatible options for particular Signature Expressions and bonded-Aspect techniques;
- paid for with **Destiny** rather than ordinary VP unless an Authority explicitly states otherwise.

Examples of design direction:
- **Life / Restoration:** preserve a dying creature from further deterioration; restore function that ordinary Restoration cannot yet repair; cleanse unusually severe damage within appropriate tier limits.
- **Fire / Forge:** work material beyond ordinary technique limits; create exceptional bonds; shape unusually complex or resistant material.
- **Earth / Fortification:** resist displacement or collapse in ways normal protection cannot; reinforce structures under catastrophic stress.
- **Fire / Conflagration:** cause flame to retain or express properties representing exceptional authority over destructive combustion rather than simply adding generic damage.

Exact Authority catalogues remain future Aspect-specific content.

## Destiny — PROVISIONAL NUMERICAL FOUNDATION
Destiny remains the Anointed-specific secondary resource used for exceptional Aspect Authority.

Resource layers:
- **Signature Expression:** baseline 0 VP.
- **Normal bonded-Aspect techniques:** normal VP costs and normal action requirements.
- **Aspect Authority:** Destiny.

Provisional baseline Destiny capacity:
`Maximum Destiny = 2 + floor(Level / 5)`

Provisional progression:
- Levels 1–4: 2 Destiny
- Levels 5–9: 3 Destiny
- Levels 10–14: 4 Destiny
- Levels 15–19: 5 Destiny
- Level 20: 6 Destiny

Provisional baseline recovery:
- Recover 25% of Maximum Destiny per completed 6-hour elapsed interval, rounded to nearest whole, minimum 1.
- This baseline exists so the archetype cannot be starved of its defining resource by campaign structure or GM pacing.

Mission fulfillment provides an **additional** Destiny relationship rather than the sole recovery source.

**Meaningful Mission Fulfillment** may restore Destiny or grant a temporary Destiny benefit. Mission Fulfillment means a consequential success that genuinely advances the Anointed's broad Mission; it is not limited to spreading a cultural practice.

Establishing, spreading, improving, preserving, or reinforcing successful Aspect-related practices is one important form of Mission Fulfillment, especially because such practices can also reinforce the Pillar's wider cultural pattern, but direct accomplishment of the Mission can qualify as well.

Examples:
- Earth/Bounty Anointed teaches an agricultural method that is successfully adopted.
- Life/Restoration Anointed establishes practices that materially reduce disease or cures a disease whose defeat substantially advances the Mission.
- Fire/Forge Anointed develops a superior craft method that other smiths successfully adopt or completes a defining masterwork that meaningfully advances the Mission.
- Fire/Conflagration Anointed destroys a target whose destruction is a major expression of the character's broad Mission, even if no new social practice is created.
- Kinship/Guardian Anointed successfully preserves a person, community, or charge whose protection is a major expression of the Mission.

Exact mission-award procedure and reward magnitude remain calibration work; baseline Destiny recovery remains independent of Mission awards so the archetype cannot be resource-starved by campaign structure.

## Level 1 — Living Signature + Birth Imprint + Aspect Authority
At level 1, the High Anointed establishes:
- bonded Aspect;
- broad lifelong Mission;
- Birth Imprint;
- High Signature Expression;
- access to that Aspect's level-appropriate Authority options.

Normally one compatible Authority Expression may be added to a Signature manifestation by paying its listed Destiny cost.

The Anointed also has full normal access to the bonded Aspect's technique catalogue up to the universal character-level tier limit, using normal VP/action rules.

## Level 2 — Expanded Projection
The High Anointed's Signature gains an authored **Expanded Projection** expression that makes the Focus's outward identity mechanically visible before higher-level Authority comes online.

Each High Signature package defines an Aspect-appropriate projection axis, such as:
- greater **reach**;
- greater **extent or area**;
- affecting **multiple compatible subjects**;
- manifesting from a **remote point** the Anointed can validly target;
- establishing a broader **projected field or presence**;
- another outward delivery form appropriate to the Aspect.

Expanded Projection is not a generic menu chosen anew on every use. The Signature/Aspect package specifies what form of projection that Anointed can express, and may specify output reductions, targeting conditions, or other limits where necessary.

Expanded Projection does **not** increase technique tier, does not automatically increase raw potency, and does not grant free Authority. Normal action requirements and any listed VP/Destiny costs still apply.

The archetype-wide **Aspect Intuition** feature remains available to High Anointed as it is to Medium and Low Anointed.

## Level 3 — Manifest Authority
At levels 1–2, Authority primarily modifies the Signature Expression.

At level 3, the High Anointed may also invoke compatible Authority Expressions through any bonded-Aspect technique explicitly tagged **[Projection]**.

- The technique still costs normal VP.
- The Authority costs its listed Destiny separately.
- The technique must explicitly list or support the chosen Authority.
- Authority does not permit arbitrary freeform escalation beyond the authored Aspect rules.

## Level 4 — Deepened Destiny + universal +1 Ability
Gain the universal **+1 Ability** increase.

Provisional High-Focus benefit:
- Maximum Destiny increases by **+1** beyond the normal Anointed baseline.

This additional reserve is provisional and must be tested against Medium/Low Anointed before final audit lock.

## Level 5 — Sovereign Projection
Normally, one Signature or projected bonded-Aspect technique carries at most one Authority Expression.

At level 5:
- once per turn, one compatible **[Projection]** Signature or bonded-Aspect technique may carry **two compatible Authority Expressions**;
- pay the full listed Destiny cost for each Authority;
- no discount is granted;
- this does not increase technique tier;
- this does not create an additional spell or action.

Sovereign Projection represents greater depth inside the same Aspect rather than generic effect manipulation.

## Archetype/Focus distinctions
### High Anointed vs High Priest
- **High Priest:** asks how to serve the Pillar, strengthen its presence, and help it grow; accesses three Aspects of one Pillar through prayer/preparation/open invocation.
- **High Anointed:** asks how to use their one Aspect to further the Mission; Pillar reinforcement is normally a consequence of Mission success rather than the primary motive.

### High Anointed vs High Gifted
- **High Gifted:** conditional intensity; increases the expression of the currently active emotion-linked Aspect through Amplification and Projected Surge.
- **High Anointed:** fixed one-Aspect depth; uses authored Aspect Authority to do things unusually privileged or absolute within that one domain.

### High Anointed vs High Scholar
- **High Scholar:** breadth, synthesis, and technical combination across learned techniques.
- **High Anointed:** narrow permanent access and exceptional depth within one Aspect.

## Current status
**FOUNDATION PASSED THREE-FOCUS AUDIT WITH TARGETED UPDATES INTEGRATED.**

The structural High Anointed foundation is accepted. The following remain calibration/content work rather than identity redesign:
- exact Signature Expressions for all Aspects/Birth Imprints;
- exact Authority catalogues and Destiny costs;
- final Destiny pool/recovery formula;
- final decision on the High level-4 +1 Maximum Destiny benefit;
- numerical interaction with VP, Physical Tempo, healing, damage, and control;
- comparison against Medium and Low Anointed in the later Anointed audit.

---

# Medium Anointed L1–5 Foundation — LOCKED STRUCTURE / NUMBERS & CONTENT PROVISIONAL

## Core question — LOCKED

> **“Where should I channel my Aspect right now to further my Mission?”**

The Medium Anointed concentrates their permanent bonded Aspect into a specific **Vessel**: a creature, item, piece of equipment, material, bounded location, or ongoing undertaking that can meaningfully express that Aspect.

The Medium Anointed is not defined by support, defense, melee, or offense. The defining decision is **where the one permanent Aspect is concentrated**.

Examples:
- **Life / Restoration:** invest a patient, medicine, physician’s tool, wound, organ, or other valid treatment target.
- **Fire / Forge:** invest a blade being forged, furnace, hammer, armor, existing weapon, material, or other compatible crafted target.
- **Fire / Conflagration:** invest an enemy, weapon, armor, gate, fuel source, or other compatible destructive target.
- **Earth / Fortification:** invest the structure, shield, bridge, position, or person that must hold.

The Medium identity is therefore **concentrated Aspect application through a chosen target or instrument**.

## Focus distinction — LOCKED CONCEPT

- **High Anointed:** “How can I project my Aspect most powerfully in pursuit of the Mission that created me?”
- **Medium Anointed:** “Where should I channel my Aspect right now to further my Mission?”

High emphasizes projection, scale, reach, and outward manifestation.
Medium emphasizes placement, concentration, targeting, and investment.

Example, two **Life / Restoration** Anointed with the Mission *heal the sick*:
- the **High Anointed** may cure a plague spreading through an entire village;
- the **Medium Anointed** may invest Restoration into one specially prepared potion, patient, treatment, or tool to cure an illness no one else has managed to overcome.

Neither is simply the better healer. They solve different Restoration problems.

## Level 1 — Aspect Investment

A Medium Anointed may establish one **Invested Vessel** at a time.

A Vessel may be:
- self;
- a willing creature;
- an unwilling creature where the Aspect and delivery method permit;
- weapon, armor, tool, medicine, or other object;
- material;
- bounded location or structure;
- an ongoing craft, treatment, construction, ritual, or other undertaking;
- another target category explicitly supported by the bonded Aspect.

The Aspect determines compatibility. A target being physically present is not enough; the bonded Aspect must be capable of meaningfully interacting with it.

### Vessel coherence and scale — LOCKED
A Vessel must be **one coherent target or locus of practical interaction**. Valid examples include one creature, one object, one material body, one gate, one bridge, one room-sized or otherwise specifically bounded location where supported, one treatment, one craft project, or one comparable undertaking with a concrete locus.

A Vessel is **not** an arbitrary aggregation or abstract objective. A settlement, army, population, entire forest, battlefield, kingdom, war, campaign, or goal such as *win the war* cannot normally be declared as one Vessel merely because the player can describe it as a single idea. Larger or distributed targets require an explicit technique, Signature, or Authority that says they qualify.

An ongoing undertaking is valid only when it is itself a coherent work or process the Aspect can be concentrated into, such as forging one masterwork, treating one patient, constructing one bridge, or conducting one defined ritual.

This boundary preserves the Focus distinction: **High projects across scale; Medium concentrates into a chosen locus.**

### Investment persistence and remote-channel boundary — LOCKED
Investment may persist when the Vessel leaves the Anointed's immediate reach unless the relevant Aspect package says otherwise. Persistence alone, however, does **not** turn the Vessel into an unlimited remote casting anchor.

Channel Through Vessel never bypasses a technique's normal range, line-of-effect, targeting, contact, perception, or delivery requirements unless the individual Signature, technique, or Authority explicitly says that it does. An invested enemy three kingdoms away remains invested if the rules allow that persistence, but the Anointed cannot simply resolve ordinary techniques through that target from three kingdoms away.

### Establishing Investment

Provisional baseline:
- establishing or changing the Invested Vessel costs **1 Attack Unit**;
- releasing an Investment is free;
- establishing the Investment itself costs **0 VP**;
- the Medium Anointed normally has only **one primary Invested Vessel** at a time.

Hostile creatures or attended hostile objects cannot normally be Invested merely by declaration. The Anointed must satisfy an appropriate delivery condition such as a successful attack, touch, compatible technique, or other Aspect-specific method.

Exact hostile-investment resolution remains content/balance work.

## Birth Imprint and Invested Signature

The archetype-wide **Birth Imprint** remains part of the Medium Anointed.

For Medium Focus, the Birth Imprint shapes an **Invested Signature Expression**: the character’s baseline 0-VP Signature is especially expressed **through, within, or upon the Invested Vessel**.

Examples:
- plague-born **Life / Restoration** may invest a patient, medicine, or treatment tool and express disease-cleansing Restoration through it;
- **Fire / Forge** may invest a furnace, hammer, weapon, armor, or unfinished masterwork and express supernatural shaping, joining, heating, or craft through that Vessel;
- **Fire / Conflagration** may invest an enemy, weapon, gate, or fuel source and express destructive fire through that specific target.

The Signature is not simply a free spell targeted at the Vessel. The Vessel becomes the principal place through which the Anointed’s Birth Imprint manifests.

## Aspect Authority — Medium expression

The Medium Anointed receives the archetype-wide **Aspect Authority** mechanic.

At low levels, Authority is primarily expressed through the Invested Vessel.

Destiny may therefore permit exceptional Aspect-specific outcomes involving that Vessel that ordinary techniques cannot normally produce.

Examples of design direction:
- **Restoration:** empower a medicine or treatment to overcome an illness beyond ordinary healing capability within authored limits;
- **Forge:** work material, joins, or crafted structures beyond ordinary technique limits;
- **Conflagration:** force destructive combustion into a resistant but compatible target;
- **Fortification:** make one structure, position, or protected subject withstand an otherwise exceptional stress.

Authority remains Aspect-specific depth, not generic numerical metamagic.

## Level 2 — Channel Through Vessel

The Invested Vessel becomes an extension of the Anointed’s Aspect bond.

Compatible Signature Expressions and bonded-Aspect techniques may resolve:
- **on** the Vessel;
- **through** the Vessel;
- or using the Vessel as the relevant point of interaction,

when the individual Aspect and technique support that relationship.

Examples:
- a Conflagration Anointed channels a fire expression through an invested sword strike;
- a Restoration Anointed channels through invested physician’s tools or medicine;
- a Forge Anointed channels supernatural shaping through an invested hammer, furnace, workpiece, or other compatible Vessel.

Channel Through Vessel does **not** inherently grant extra actions. A technique or effect still uses its normal action cost unless an explicit rule states otherwise.

## Level 3 — Deep Channeling

At level 3, the Medium Anointed may invoke compatible **Aspect Authority** through ordinary bonded-Aspect techniques when those techniques are being applied **to, through, or by means of the Invested Vessel**.

Resource separation remains:
- normal bonded-Aspect technique = normal **VP** cost;
- Authority Expression = listed **Destiny** cost.

The technique must explicitly support the chosen Authority. Deep Channeling does not permit arbitrary freeform escalation.

This is the level at which the concentrated single-target/single-instrument concept becomes fully operational.

Example:
A Life / Restoration Anointed invests a prepared potion, channels an ordinary Restoration technique through it, and spends Destiny on an authored Restoration Authority that allows the treatment to overcome an otherwise resistant illness.

## Level 4 — Swift Rechanneling + universal +1 Ability

Gain the universal **+1 Ability** increase.

Provisional Medium-Focus benefit:

> **Once per turn, the Medium Anointed may change their Invested Vessel without spending the normal 1 Attack Unit.**

All target eligibility, contact, range, and hostile-investment requirements still apply.

This represents growing skill at placing the Aspect exactly where it is needed rather than increasing the breadth of the Aspect itself.

The once-per-turn free rechannel structure is retained after the three-focus audit. Its exact cadence remains a numerical balance point for later testing; if playtesting shows that it trivializes Vessel commitment, cadence may be reduced without changing the Medium identity.

## Level 5 — Total Investment

At level 5, concentrating the Birth-Imprint Signature and a compatible normal bonded-Aspect technique into the **same Invested Vessel** can unlock an authored **Total Investment Synergy** for that Aspect package.

The synergy is the level-5 benefit; merely allowing two compatible effects to coexist is not treated as a special permission unless another rule would actually make them exclusive.

Rules:
- the character still has only **one primary Invested Vessel**;
- the Signature and ordinary technique must both validly interact with that same Vessel;
- the normal technique still pays its normal VP, action, duration, targeting, commitment, and upkeep costs;
- only one Total Investment Synergy is active for a Vessel at a time unless an explicit later feature says otherwise;
- the synergy is authored per Aspect/Birth-Imprint package rather than chosen from a generic stacking menu;
- the synergy does not automatically create another action, another full technique-scale damage/healing instance, or additional targets unless the authored synergy explicitly permits it.

Design examples:
- **Forge:** maintaining the Invested Signature's exceptional material state while a Forge technique reshapes or reinforces the same work can unlock a deeper material/craft interaction.
- **Restoration:** the Invested Signature may continue addressing the underlying disease or failure state while the normal Restoration technique repairs immediate bodily damage, with an authored synergy when both operate on the same patient or treatment.
- **Fortification:** Signature reinforcement and a stronger Fortification technique concentrated into the same gate, bridge, shield, or defender can unlock an authored resilience interaction.
- **Conflagration:** an Invested burn plus another compatible Conflagration technique driven into the same target can unlock an authored combustion interaction.

The level-5 identity is **deeper concentration producing unique same-Vessel synergy, not wider distribution or generic effect stacking**.

## Medium Anointed progression summary

| Level | Feature |
|---:|---|
| **1** | **Aspect Investment + Invested Signature + Aspect Authority** |
| **2** | **Channel Through Vessel** |
| **3** | **Deep Channeling** — Authority through normal techniques applied to/through the Invested Vessel |
| **4** | **Swift Rechanneling + universal +1 Ability** |
| **5** | **Total Investment** — concentrating Signature and a compatible normal Aspect technique into the same Vessel unlocks an authored synergy |

## Archetype/Focus distinctions

### Medium Anointed vs Medium Gifted
- **Medium Gifted:** establishes conduits whose expression changes when the Active Emotion changes; the conduits are comparatively sticky while the Aspect expression changes.
- **Medium Anointed:** the Aspect never changes; the **Vessel changes** according to where the one permanent Aspect needs to be concentrated.

Shorthand:
- Gifted: **same conduits → changing Aspect expression**.
- Anointed: **same Aspect forever → changing Vessel**.

### Medium Anointed vs Medium Priest
- **Medium Priest:** distributes prepared Pillar blessings/consecrations among recipients or anchors according to who needs the Pillar’s aid.
- **Medium Anointed:** concentrates one permanent Aspect into the specific creature, object, location, material, or undertaking most important to the Mission.

### Medium Anointed vs Medium Scholar
- **Medium Scholar:** reroutes among different learned magical functions according to the active problem.
- **Medium Anointed:** keeps the same Aspect and changes the target/instrument through which that depth is expressed.

## Current status

**FOUNDATION PASSED THREE-FOCUS AUDIT WITH TARGETED UPDATES INTEGRATED.**

The structural Medium Anointed foundation is accepted. The following remain calibration/content work rather than identity redesign:
- exact Vessel eligibility by Aspect and technique within the locked coherence/scale rule;
- hostile-investment delivery/resolution;
- exact Invested Signature expressions for Birth Imprints;
- exact Authority catalogues and Destiny costs;
- final Destiny pool/recovery formula shared by Anointed;
- final cadence of Swift Rechanneling;
- exact Aspect-specific Total Investment Synergies and their numerical limits;
- numerical interaction with VP, Physical Tempo, healing, damage, crafting, and control;
- comparison against High and Low Anointed in the later Anointed audit.

---

# Low Anointed L1–5 Foundation — LOCKED STRUCTURE / NUMBERS & CONTENT PROVISIONAL

## Core question

> **“How do I embody my Aspect through myself and my actions to further my Mission?”**

The Low Anointed is the embodiment expression of the archetype. High projects the bonded Aspect outward; Medium concentrates it into a chosen Vessel; Low makes the Aspect a persistent part of the Anointed’s own body, equipment, and ordinary physical actions.

The Low Anointed retains the archetype-wide Anointed foundation:
- born during a Pillar surge;
- one permanent bonded Aspect;
- one broad lifelong Mission shaped by the birth surge;
- a Birth Imprint reflecting the successful practice and collective conditions that produced the surge;
- full normal catalogue of the bonded Aspect up to the universal tier cap;
- normal VP costs for normal Aspect techniques;
- a 0-VP Signature Expression;
- Aspect Authority fueled by Destiny;
- Aligned / Conflicted / Forsaken Mission states and bond Dormancy on genuine Mission abandonment.

Low Focus changes **how** that identity is expressed: the Aspect is embodied rather than primarily projected or invested into an external Vessel.

## Level 1 — Embodied Signature + Birth Imprint + Aspect Authority

The Anointed’s Birth Imprint produces an **Embodied Signature Expression**.

The Embodied Signature is:
- 0 VP;
- self-centered;
- persistent while manifested;
- shaped by the Birth Imprint;
- capable of including worn or directly carried equipment where the Aspect logically permits;
- intentionally stronger as an enduring personal expression than as a generic free spell, while remaining below unrestricted full technique-scale output.

The Anointed may suppress or resume the manifestation at the start of their turn without spending an action. Outside meaningful pressure, suppression or resumption requires no meaningful action.

Examples:
- **Fire / Conflagration — Flame Mantle:** the Anointed can wreath themselves in supernatural flame without harming themselves or ordinary worn equipment; later Aspect content may provide modest contact or weapon riders, heat/light, and deeper flame-state Authority.
- **Life / Restoration — Restorative Body:** the Anointed’s body continuously expresses Restoration, allowing substantially greater self-regeneration throughput than the ordinary natural HP regeneration rate. This normally still consumes Vigor unless an explicit effect changes the conversion.
- **Earth / Fortification:** the body becomes unusually difficult to break, move, or destabilize.
- **Skywinds / Swiftness:** movement and bodily acceleration naturally express supernatural speed.
- **Fire / Forge:** hands, tools, and actively used equipment can express supernatural craftsmanship, heat, shaping, or material integrity.

### Embodied Signature cadence rule

An Embodied Signature may define:
- **Continuous** persistent properties;
- modest **Riders** on eligible physical actions;
- limited **Pulses**;
- stronger **Spend** effects requiring explicit resource expenditure.

**Full technique-scale damage, healing, Vigor restoration, or equivalent major output cannot trigger freely on every Attack Unit.** This is especially important because Low Focus gains the highest Physical Tempo.

### Aspect Authority at level 1

Low Anointed gains access to Aspect Authority immediately. At levels 1–2, its special Low-Focus application is primarily through the Embodied Signature and the Anointed’s own embodied state.

Destiny can therefore push the embodiment into exceptional Aspect-specific expressions without becoming generic metamagic.

Examples:
- **Conflagration:** become substantially more flame-like rather than merely being surrounded by fire;
- **Restoration:** force severe bodily damage into immediate recovery;
- **Fortification:** become temporarily almost impossible to move or break.

Exact Authority effects and Destiny costs are authored per Aspect and remain content/calibration work.

## Level 2 — Living Instrument

The bonded Aspect becomes naturally integrated into the Anointed’s ordinary physical activity.

The Embodied Signature may define compatible interactions with:
- Attack;
- Guard;
- Dodge;
- movement;
- grapple;
- shove;
- interception;
- tool use;
- other mundane physical actions where the Aspect package permits.

This does not create extra actions. The Aspect is integrated into the physical action rather than replacing or duplicating it.

Examples:
- a Conflagration Anointed can fight with ordinary weapon attacks while remaining wreathed in their own flame;
- a Fortification Anointed’s Guard can naturally express supernatural solidity;
- a Swiftness Anointed’s movement can express the Aspect without repeatedly casting a separate movement technique;
- a Restoration Anointed can continue fighting while their body converts reserves into recovery at an exceptional rate.

### Equipment boundary

Worn and actively wielded equipment may count as part of the Low Anointed’s embodied expression where appropriate.

When an object is no longer worn, wielded, or directly carried, the Low-specific embodied expression normally ends.

This creates an explicit boundary with Medium Anointed:
- **Low:** a flaming sword in the Anointed’s hand is part of their embodiment;
- **Medium:** leaving the Aspect concentrated inside a sword or other object independent of the Anointed is Aspect Investment.

## Level 3 — Incarnate Authority

Aspect Authority expands beyond the basic Signature.

The Low Anointed may invoke compatible Authority through:
- the Embodied Signature;
- their own body;
- worn equipment;
- actively wielded equipment;
- compatible self-targeting or `[Embodiment]` bonded-Aspect techniques.

Normal techniques still cost normal VP. Authority still costs Destiny.

Examples:
- **Conflagration:** an Authority may temporarily shift the Anointed from merely wreathed in supernatural fire toward actually becoming a living flame-state;
- **Restoration:** Authority may close a Severe wound rapidly, maintain bodily function through otherwise incapacitating trauma, or force damaged organs toward their proper living state;
- **Fortification:** Authority may temporarily make the Anointed extraordinarily difficult to displace, breach, or structurally compromise.

The exact consequences remain Aspect-specific rather than a universal numeric enhancement menu.

## Level 4 — Seamless Invocation + universal +1 Ability

Gain the universal **+1 Ability** increase.

Provisional Low-Focus benefit:

> **Once per turn, when the Anointed spends an Attack Unit on an eligible ordinary physical action, they may activate one compatible 1-Attack-Unit `[Embodiment]` technique as part of that same Attack Unit, paying the technique’s normal VP cost.**

Restrictions:
- the technique must explicitly support `[Embodiment]`;
- it cannot generate another attack or action;
- it cannot recursively trigger itself or another action-generating feature;
- it cannot convert an unrelated outward technique into a free rider;
- Seamless Invocation may establish, alter, refresh, or intensify an Embodiment state, but it cannot deliver an additional **full technique-scale immediate instance of damage, healing, control, Vigor restoration, or equivalent major output** unless that technique explicitly authorizes Seamless use for that output.

This is action integration, not free casting and not a hidden extra Attack Unit. Persistent output continues to follow the normal Continuous / Rider / Pulse / Spend cadence rules.

Example:
A Conflagration Anointed makes a sword attack and simultaneously activates a compatible self-directed Conflagration enhancement that is designed for Embodiment, rather than spending one Attack Unit to enhance and another to attack.

The once-per-turn cadence remains numerically provisional for later balance testing, but the action-integration structure and output guardrail are locked.

## Level 5 — Living Aspect

The Embodied Signature reaches its first major maturation.

Each Low Anointed Aspect package gains an **advanced persistent manifestation** representing the Anointed becoming substantially more like the bonded Aspect while retaining their ordinary martial and physical play.

This is not a second Aspect, not a new prepared effect, and not a change of Birth Imprint. It is a deeper expression of the same permanent bond.

Examples:
- **Conflagration:** the Anointed approaches a true living incarnation of flame while continuing to fight with ordinary martial actions;
- **Restoration:** regeneration becomes extraordinary, potentially improving HP-recovery throughput, Vigor-to-recovery efficiency, limited wound repair, or resistance to bodily deterioration, with exact numbers determined later;
- **Fortification:** the Anointed increasingly resembles an immovable living bastion;
- **Swiftness:** supernatural motion becomes a persistent property of ordinary bodily movement;
- **Forge:** hands, body, and equipment operate increasingly like an extension of a supernatural forge.

The level-5 identity is **deeper embodiment**, not broader Aspect access.

## Low Anointed progression summary

| Level | Feature |
|---:|---|
| **1** | **Embodied Signature + Birth Imprint + Aspect Authority** |
| **2** | **Living Instrument** — Aspect integrates with ordinary physical action |
| **3** | **Incarnate Authority** — Authority through self, Signature, embodied equipment, and compatible techniques |
| **4** | **Seamless Invocation + universal +1 Ability** |
| **5** | **Living Aspect** — advanced persistent form of the Embodied Signature |

## Three-Focus Anointed distinction

| Focus | Core question | Primary expression |
|---|---|---|
| **High** | **How can I project my Aspect most powerfully in pursuit of the Mission that created me?** | projection, scale, outward Authority |
| **Medium** | **Where should I channel my Aspect right now to further my Mission?** | concentrated Aspect Investment into a Vessel |
| **Low** | **How do I embody my Aspect through myself and my actions to further my Mission?** | persistent embodiment and physical integration |

Illustrative Restoration split:
- **High:** cure the village-wide plague;
- **Medium:** channel Restoration into the one medicine or patient that no ordinary treatment can save;
- **Low:** become extraordinarily difficult to keep wounded because Restoration is persistently expressed through the body.

Illustrative Conflagration split:
- **High:** project overwhelming destructive fire;
- **Medium:** channel Conflagration into the exact creature, weapon, armor, gate, fuel source, or other Vessel that needs to burn;
- **Low:** become the burning thing while continuing to fight through ordinary martial actions.

## Archetype/Focus distinctions

### Low Anointed vs Low Gifted
- **Low Gifted:** maintains an emotional Anchor and gains deeper embodiment by sustaining that emotional state.
- **Low Anointed:** has no emotional access gate; the one permanent Aspect is intrinsically part of the Anointed and is expressed through body, equipment, and action.

### Low Anointed vs Low Scholar
- **Low Scholar:** deliberately prepares and maintains chosen magical Embodiments and pays switching/commitment costs when changing configuration.
- **Low Anointed:** does not choose among learned configurations; the same bonded Aspect is continuously embodied and deepens through Birth Imprint and Authority.

### Low Anointed vs Low Priest
- **Low Priest:** maintains inward Devotional Rites as a persistent expression of service to one Pillar.
- **Low Anointed:** embodies one Aspect because it is permanently part of them, in service of their Mission rather than direct Pillar devotion.

## Current status

**PROVISIONALLY LOCKED PENDING ANOINTED AUDIT.**

The structural Low Anointed foundation is accepted for the current design pass. The following remain calibration/content work rather than identity redesign:
- exact 48 Aspect/Birth-Imprint Embodied Signature packages;
- exact Continuous/Rider/Pulse/Spend cadence for each Signature;
- exact regeneration throughput and Vigor interaction for Restoration;
- exact living-flame and other altered-state rules;
- exact Incarnate Authority catalogues and Destiny costs;
- final Destiny pool/recovery formula shared by Anointed;
- final cadence and eligibility of Seamless Invocation;
- interactions with Physical Tempo, Guard, Dodge, wounds, armor, equipment, and ordinary martial actions;
- comparative balance against High/Medium Anointed and Low Priest/Scholar/Gifted in the Anointed audit.

---

# Anointed Three-Focus Audit Resolution — v33

**Verdict: PASS — FOUNDATION RESOLVED; CONTENT/NUMBER CALIBRATION REMAINS.**

The six audit updates are integrated into the canonical Anointed foundation:

1. **Aspect Intuition is universal to all Anointed**, and High level 2 is now **Expanded Projection**.
2. **Medium Vessel coherence/scale and remote-channel boundaries are locked**, preventing arbitrary aggregated Vessels and unlimited remote casting through Investment.
3. **Medium Total Investment is now an authored same-Vessel synergy**, not mere permission to stack Signature plus technique.
4. **Low Seamless Invocation has an immediate-output guardrail**, preserving action integration without becoming a hidden extra Attack Unit.
5. **Mission-based Destiny rewards now trigger from meaningful Mission Fulfillment broadly**, with cultural/practice reinforcement as one important but non-exclusive case.
6. **Birth Imprint access boundaries are explicit:** it shapes Signature/Authority identity without narrowing the bonded Aspect catalogue or granting outside-Aspect access.

Remaining Anointed work is calibration/content production rather than foundation redesign:
- final Destiny capacity and recovery values;
- final High +1 Maximum Destiny decision;
- exact Signature Expressions and Expanded Projection profiles;
- Aspect-specific Authority catalogues and Destiny costs;
- Medium Total Investment Synergies;
- Low Living Aspect expressions and regeneration/damage/control numbers;
- final Swift Rechanneling and Seamless Invocation cadence after numerical playtesting;
- full 48-Aspect content coverage across High projection, Medium investment, and Low embodiment.

---

# Veilbound 12-Combination Base Foundation Audit Resolution — v34

**Verdict: PASS — L1–5 ARCHITECTURE RESOLVED; CONTENT/NUMBER CALIBRATION REMAINS.**

The five targeted updates from the 12-combination audit are now integrated into the canonical foundation:

1. **Low Priest level 5 Living Liturgy is reworked.** Stable Chosen Devotion now enables authored cross-Aspect expression from the same Pillar at normal Exaltation cost, differentiating Priest commitment from Low Scholar's efficiency-based Entrenched Configuration.
2. **Zero-action timing/no-refresh is universal.** Free rerouting, reassignment, retuning, rechanneling, release, and similar operations do not grant interrupt timing and do not refresh activation/Pulse/once-per-window output unless explicitly stated.
3. **Continuous / Rider / Pulse / Spend is now universal persistent-effect cadence.** Full technique-scale damage, healing, Vigor restoration, strong control, or equivalent major output cannot be an unrestricted per-Attack-Unit Rider.
4. **Scholar-vs-Gifted breadth calibration is explicit.** Gifted owns large fixed breadth; Scholar must retain the strongest player-configurable cross-Pillar/Aspect problem coverage over time.
5. **Universal technique-expression metadata is established.** `[Projection]`, `[Embodiment]`, `Inward`, `Consecration`, `Devotional Rite`, Conduit Form compatibility, Investment compatibility, and Cadence now share one cross-system vocabulary.

### 12-combination status

- **High Focus:** projection identity passes across Scholar, Priest, Gifted, and Anointed.
- **Medium Focus:** routing/allocation identity passes across all four archetypes; movement of persistent power now shares timing and no-refresh rules.
- **Low Focus:** embodiment/commitment identity passes across all four archetypes; the Low Priest/Low Scholar level-5 overlap is resolved.
- **Archetype access:** Scholar configurable breadth, Priest one-Pillar prepared/aligned access, Gifted eight fixed emotion-linked Aspects, and Anointed one-Aspect Authority remain distinct.

### Remaining work before numerical playtest lock

The remaining work is primarily calibration/content rather than foundation redesign:
- Scholar known/prepared repertoire counts and Composite Casting burst testing once High Physical Tempo reaches multiple Attack Units;
- Priest Prepared Prayer counts, Open Invocation surcharge, Pillar Accord floor/procedure, Miracle frequency calibration, and authored Living Liturgy compatibility tables;
- Gifted Aspect/Form expressions, Amplification options, Projected Surge cost, and final persistent-output numbers;
- Anointed Destiny numbers, Signatures, Authority catalogues, Total Investment synergies, Living Aspect packages, and final cadence testing;
- universal persistent-effect numeric budgets against maximum Physical Tempo;
- technique content metadata cleanup across the eventual full catalogue.


---

# Post-audit locked decision — Metaphysical Foundation

The following decisions supersede older v34 assumptions where terminology or meaning conflicts.

## Desire, Will, Volition, Resonance

- **Desire** is the raw direction of wants, needs, emotions, convictions, impulses, and longings.
- **Will** selects, organizes, sustains, and acts upon desire.
- **Volition** is the usable metaphysical force produced when desire and will are directed through the Veil into coherent intention and action.
- **Resonance** remains a universal **-3 to +3** character state, but its canonical meaning is now explicitly **internal coherence**: how coherently desires, emotions, beliefs, intentions, self-understanding, and actions reinforce rather than oppose one another.
- Resonance is not morality, Pillar loyalty, obedience, confidence, or a generic spellcasting bonus.
- The universal starting Resonance value, change cadence, recovery procedure, and full numerical effects remain **UNRESOLVED** pending the dedicated Resonance mechanics pass.

This supersedes the older audit row that treated **starting Resonance as archetype-specific** (Priest +1, Scholar +1, Gifted 0, Anointed +2). Those values must not be promoted as universal starting Resonance values.

## Priest Resonance renamed Pillar Accord

The Priest-specific state formerly called **Priest Resonance** is renamed **Pillar Accord**.

Pillar Accord remains a Priest-specific **-3 to +3** state measuring coherence between the Priest's genuine relationship, intentions, actions, and the principles/pattern of the chosen Pillar.

Universal Resonance and Pillar Accord are separate and may move independently.

The rename is not intended as a balance change. Existing Priest mechanics migrate from Priest Resonance to Pillar Accord:

- Prepared Prayer capacity;
- small final-effect Accord bonus;
- Miracle Petition eligibility;
- Miracle Petition probability;
- Miracle Debt advancement/repayment;
- gains/losses caused by sustained alignment or conflict with the chosen Pillar.

Universal Resonance does not automatically stack into those Priest-specific mechanics.

## VP, level, and Focus

**VP is freely available Volition**, not total Volition or total Veil integration.

No separate numeric Total Volition pool is tracked.

**Level** canonically represents increasing depth of integration with the Veil.

**Focus** determines where that growing integration is predominantly expressed:

- High — Projection: more integration remains freely allocatable as VP;
- Medium — Routing: integration is developed into active routing/reconfiguration plus a moderate free VP reservoir;
- Low — Embodiment: more integration is already persistently expressed through body, reflexes, equipment interaction, and other embodied development, leaving less freely available as VP.

Different Focuses therefore do not imply different total metaphysical worth or total will at the same level.

## Archetype metaphysical access

- **Scholar:** accesses real Pillar/Aspect patterns through learned technical methods without requiring Pillar approval, recognition, favor, or personal bond.
- **Gifted:** is a natural phenomenon of human Veil integration rather than a person selected, created, or deliberately shaped by a Pillar. Innate emotional states naturally open fixed pathways into Aspect patterns.
- **Anointed:** Mission state remains separate from universal Resonance. A coherent rejection of the Mission may produce Forsaken/Dormant consequences without requiring low Resonance.

Existing Gifted formulas that already reference Resonance refer to the restored universal internal-coherence state.

## Magical resistance terminology

To avoid collision with the Pillar Aspect names **External / Internal / Transform**, the resistance taxonomy uses:

- **Intrusion** — magic crosses into, originates within, overlaps, or directly alters the protected internal self of a living target; strongest magical resistance.
- **Imposition** — magic acts directly on a target from outside without first becoming an independent manifested phenomenon; intended roughly even contest at equal capability.
- **Manifestation** — magic creates an independently existing external phenomenon; once validly manifested outside the protected living target, the phenomenon is resolved through ordinary applicable defenses rather than magical resistance.

A supposed Manifestation created inside or overlapping a living target is an **Intrusion**. This prevents manifestation wording from bypassing internal protection (for example, conjuring water inside lungs).

The shared **Direct Veil** numerical procedure for both Imposition and Intrusion is resolved by the post-audit decision below.


---

# Post-audit locked decision — Universal Resonance and Direct Veil Magic

This decision builds on the locked metaphysical foundation above and supersedes its unresolved placeholders for universal Resonance, Imposition, and Intrusion.

## Universal Resonance procedure

Universal Resonance remains a **-3 to +3** character state measuring internal coherence of Volition.

### Starting value

New player characters normally begin at:

```
Resonance 0
```

Archetype does not modify the universal starting value.

The old archetype-specific starting Resonance row remains superseded. Priest **Pillar Accord** is a separate subsystem and its starting value is not decided by this universal rule.

### Scale

- **+3 Integrated**
- **+2 Strongly coherent**
- **+1 Coherent**
- **0 Ordinary / mixed**
- **-1 Dissonant**
- **-2 Fractured**
- **-3 Self-opposed**

There is no additional universal special effect merely for reaching +3 or -3 unless an explicit rule says otherwise.

### Resonance Events

Resonance changes only through a meaningful **Resonance Event**:

1. an important internal conflict exists;
2. it becomes consequential in play;
3. the character's response establishes a lasting change in how that conflict is integrated or denied;
4. genuine recognition/integration may raise Resonance by +1;
5. sustained self-deception, denial, or repeatedly acting against an acknowledged self without integrating the contradiction may reduce Resonance by -1.

A single conflict normally changes Resonance by at most one step.

The same resolved contradiction cannot be repeatedly farmed for increases.

Temporary emotion, ordinary doubt, changing one's mind, one failed ideal, direct coercion, or magically controlled action do not automatically reduce Resonance.

Rest, sleep, meditation, prayer, or elapsed time do not automatically restore Resonance.

### Player/GM authority

The player has primary authority over the character's genuine desires, beliefs, feelings, and self-understanding.

The GM adjudicates whether established internal states and demonstrated actions have become coherent or contradictory enough to constitute a Resonance Event.

Resonance changes are open rather than secretly imposed.

The GM may not invent an unestablished hidden motive to reduce Resonance, and the player may not retroactively redefine an already-established motive solely to erase an established contradiction.

Optional concise **Resonance Statements** may be recorded as descriptive reference points but are not permanent commandments.

### Mechanical scope

Locked universal uses:

- **Direct Veil Resistance** for both Imposition and Intrusion;
- existing Gifted emotional-control and Instability checks that explicitly include Resonance;
- future rules that explicitly test Volition coherence/stability.

Universal Resonance does **not** modify:

- Max VP;
- normal VP recovery;
- ordinary spell/technique attack rolls;
- damage;
- healing;
- technique tier;
- ordinary nonmagical checks;
- Priest Pillar Accord;
- Anointed Mission state.

## Veil Integration Bonus

For direct Veil contests—both Imposition and Intrusion:

```
Veil Integration Bonus = floor(Level / 5)
```

Progression:

- Levels 1-4: +0
- Levels 5-9: +1
- Levels 10-14: +2
- Levels 15-19: +3
- Level 20: +4

Both acting character and target use the bonus.

A creature without a character level uses the equivalent value in its stat block; if none is defined, use +0.

This bonus is locked for both **Imposition** and **Intrusion**.

## Shared Direct Veil Pressure

```
Direct Veil Pressure =
d20
+ Veil Control
+ Shaping Ability
+ Veil Integration Bonus
+ explicit technique and situational modifiers
```

The technique authors the **Shaping Ability** according to what the magical operation actually requires.

There is no universal mandatory mundane casting Ability.

Veil Practice or another Training is not automatically added. Training contributes only when an explicit technique, feature, or situational rule says it applies.

## Shared Direct Veil Resistance

```
Direct Veil Resistance =
10
+ Resistance Ability A
+ Resistance Ability B
+ Veil Integration Bonus
+ Resonance
+ explicit technique and situational modifiers
```

The technique authors the two defensive Abilities according to what part of the target is being acted upon and how the effect operates.

A direct Veil effect succeeds only when **Direct Veil Pressure exceeds Direct Veil Resistance**. A tie resists.

There is no universal generic Will-save statistic.

## Imposition

Imposition uses **Direct Veil Pressure** against **Direct Veil Resistance as written**.

It does not add the Intrusion Barrier.

At equal non-barrier modifiers, equal Veil Integration Bonus, and Resonance 0, Imposition succeeds on 11-20: **50%**.

A target that understands the actual Imposition may knowingly waive Direct Veil Resistance to that specific effect.

Consent applies only to the effect actually understood and accepted. If the caster materially changes the effect, the target receives normal Direct Veil Resistance.

Imposition has no special deceived-acceptance reduction. The +4 deceived state belongs specifically to the Intrusion Barrier.

### Object targets

Ordinary nonliving objects do not generate Direct Veil Resistance.

- **Unattended mundane object:** if the technique permits the target and the effect is within its authored size/mass/material/range/anchoring limits, the Imposition succeeds without a Direct Veil Resistance contest.
- **Attended object:** if worn, carried, wielded, or under a creature's immediate physical control, the attending creature supplies Direct Veil Resistance using the defensive Ability pair authored for that attended-object use.
- The attending creature may knowingly waive that resistance for the specific Imposition effect it understands and accepts.
- The object itself contributes no Resonance or Veil Integration Bonus unless an explicit item rule says otherwise.
- Awareness of the attempt is not required for the attending creature's normal resistance to apply.
- Multiple unwilling attending creatures use the highest applicable Direct Veil Resistance unless the technique explicitly says otherwise.
- Exceptional magical, sentient, or warded objects may define their own Direct Veil Resistance or modifiers.

An Imposition technique that can target attended objects must author the defensive Ability pair for that route; otherwise it cannot use the attended-object route.

## Intrusion

Intrusion uses the same shared contest, but:

```
Intrusion Resistance =
Direct Veil Resistance
+ Intrusion Barrier
```

The acting roll remains **Direct Veil Pressure**.

## Intrusion Barrier

- **Unwilling / not knowingly consenting:** +8
- **Genuinely deceived into accepting the magical contact:** +4
- **Knowingly and willingly opens to the actual effect:** resistance may be waived entirely

The +8 barrier is the default.

Surprise, distraction, restraint, sleep, unconsciousness, or lack of awareness does not by itself reduce the barrier.

The +4 deceived state requires genuine acceptance of the magical interaction under a materially false understanding of what it will do. Secret casting or surprise alone is not enough.

A willing target may waive resistance only for the actual effect knowingly accepted. Consent obtained through material deception uses the +4 deceived barrier instead.

## Natural d20 results

Direct Veil Pressure resolves by actual total.

A natural 20 does **not** automatically overcome Direct Veil Resistance or Intrusion Resistance.

Direct Veil Pressure is not automatically a weapon attack merely because it uses a d20.

## Baseline calibration

At equal non-barrier modifiers, equal Veil Integration Bonus, and Resonance 0:

- Imposition -> **50%** attacker success;
- full +8 Intrusion Barrier -> **10%** attacker success;
- deceived +4 Intrusion Barrier -> **30%** attacker success;
- knowingly willing and waived -> no resistance contest.

Against an unwilling Resonance-0 target, the attacker needs approximately **+8 non-barrier advantage** merely to reach an even 50% success chance.

The maximum level-derived gap from Veil Integration Bonus alone is +4, so level by itself cannot make hostile Intrusion reliable against a comparable target.

## Remaining magical-defense work

- Manifestation delivery mapping is resolved by the post-audit decision below.
- Individual Direct Veil techniques still need authored Shaping Abilities, defensive Ability pairs, and any explicit Training interactions.
- Individual Manifestation techniques still need authored ranges, damage/effects, terrain consequences, beam parameters, and other content-specific values.


---

# Post-audit locked decision — Manifestation Resolution

This decision resolves the remaining universal mapping for **Manifestation** delivery.

## Core principle

A valid Manifestation creates an independently existing external phenomenon.

Once that phenomenon exists outside a living target, it does **not** use Direct Veil Resistance merely because magic created it.

Instead, resolve it through the ordinary physical/world procedure that matches what the phenomenon actually does.

A supposed Manifestation created inside or overlapping living tissue remains **Intrusion**.

There is no new generic spell-attack, spell-save, or area-dodge subsystem for Manifestations.

## Manifested projectiles

A manifested projectile uses the normal thrown-projectile attack architecture unless the technique explicitly uses another ordinary launcher/delivery method:

```
Manifested Projectile Attack =
d20
+ Agility
+ Precision
+ relevant Training
+ situational modifiers
```

The technique authors range, projectile properties, damage/effect, Penetration where relevant, and other constraints.

Relevant Training is the ordinary narrow throwing/weapon Training that actually applies; Veil Practice is not automatically substituted.

The thrown attack procedure does not automatically add Strength to a technique-authored damage packet. If the Manifestation creates an ordinary weapon profile, use that profile's normal Physical Contribution; otherwise use the authored technique damage/effect.

The projectile does not gain Veil Control, Resonance, or Veil Integration Bonus on its attack merely because magic created it.

Normal ranged defenses, projectile Guard where valid, cover, range, size/position, and other shot conditions apply.

If a projectile carries an area effect, resolve projectile delivery first and then resolve the area from the impact point. The area grants no second generic Dodge.

For a missed projectile-delivered area attack, determine a **Miss Impact Point**:

```
Miss Margin = max(0, Defense - Attack Total)
Scatter Distance = 1 + floor(Miss Margin / 5)
```

A natural 1 remains an automatic miss; if its total would otherwise beat the Defense, use Miss Margin 0.

Roll 1d8 for compass direction (N, NE, E, SE, S, SW, W, NW), move the impact point by Scatter Distance from the intended point, and resolve the area there.

A technique may explicitly replace this generic scatter rule with an authored miss-placement procedure. Physical obstructions still intercept normally under the applicable physical/cover rules.

A near miss may still place the original target inside the resulting area.

### Successful Guard against a projectile-delivered area

A legal projectile Guard that stops the attack does not use scatter.

By default, the projectile impacts the interposing Guard instrument at the defender's position, and the carried area resolves from that point.

The successful Guard stops the direct projectile hit but does not automatically cancel the carried explosion, burst, cloud, splash, or other area.

A shield, wall, or other barrier mitigates that resulting area only if the ordinary physical rules say it can actually interpose against the phenomenon.

A technique may explicitly override this default by stating that a Guarded projectile dissipates, fails to trigger, ricochets, or uses another authored impact rule.

## Pointed beams

A manifested beam that must be directly pointed at a target uses double Precision:

```
Beam Attack =
d20
+ Precision
+ Precision
+ explicit technique and situational modifiers
```

A Training applies only when an explicit rule or technique says a specific narrow Training applies.

Pointed beams use normal applicable ranged defenses and shot conditions.

Beam damage, dwell, penetration, rider, duration, and other effects are authored/calibrated around the double-Precision accuracy model.

## Area Manifestations

There is **no generic area-effect Dodge** that allows a character to remain in the affected space while avoiding the phenomenon.

If the area occupies the character's position when it resolves, the character suffers its authored consequences unless another rule physically prevents or mitigates them.

Relevant prevention/mitigation may include:

- already being outside the area;
- actual movement that occurs before resolution;
- a suitable barrier or cover;
- a shield/interposition rule when the shield can physically block the phenomenon;
- resistance, immunity, armor, or another consequence-specific mitigation rule.

Exact universal shield/cover handling against broad physical phenomena remains part of combat-defense work rather than a magical save.

## Persistent terrain

Manifested terrain resolves as terrain/hazard.

Entering, crossing, or remaining in the affected space applies the authored consequence at the technique/hazard's stated timing.

There is no Direct Veil Resistance or generic area Dodge merely because the terrain was created magically.

Examples include burning floor, ice, smoke, thorns, acid, or rubble.

Applicable resistance, immunity, armor, equipment, or other mitigation works normally when relevant.

## Manifested restraints

A manifested object or creature that physically grabs, binds, or restrains a target uses the ordinary grapple / grab / escape procedure.

Examples include vines, chains, or a manifested hand.

The restraint does not use Direct Veil Resistance merely because the restraining thing was created magically.

The universal grapple/grab procedure itself remains a combat-procedure dependency.

## Falling manifested objects

A manifested object that falls, collapses, or is dropped onto a target uses the ordinary falling-object / physical-hazard procedure.

The magic determines that the object exists; its subsequent collision is resolved as an equivalent ordinary falling object.

The universal falling-object/collision procedure remains a physical-hazard dependency.

## Melee and enchantments

There is no separate Manifestation melee-attack category.

A melee attack uses the normal melee rules.

A manifested or magically created weapon that is physically wielded uses the ordinary melee procedure for its weapon profile.

A magical enchantment, Embodiment, Signature, rider, or similar effect attached to a melee attack modifies what happens on or after the successful normal melee hit unless its own rule explicitly says otherwise.

## Resulting attack/defense architecture

- **Intrusion:** Direct Veil Pressure vs Direct Veil Resistance + Intrusion Barrier.
- **Imposition:** Direct Veil Pressure vs Direct Veil Resistance.
- **Manifestation projectile:** normal thrown/ranged projectile procedure.
- **Manifestation pointed beam:** double-Precision ranged attack.
- **Manifestation area/terrain:** authored physical consequence; no generic area Dodge.
- **Manifestation restraint:** normal grapple/grab procedure.
- **Manifestation falling object:** normal falling-object/hazard procedure.
- **Melee enchantment / manifested wielded weapon:** normal melee attack with authored magical consequences.

Remaining work is therefore physical combat/hazard procedure and technique content, not another universal magical-defense formula.


---

# LOCKED UPDATE: Initiative and Round/Turn Procedure

## Status: LOCKED BASELINE

The first native combat-procedure pass is now locked.

Canonical rules live in:

- `docs/rules/05-combat/initiative-and-round-structure.md`
- `docs/rules/05-combat/action-categories-and-physical-tempo.md`
- `docs/rules/06-vigor-wounds-death/hp-and-vigor.md`
- `docs/rules/06-vigor-wounds-death/dying-and-wounds.md`

This supersedes the earlier audit statement that Initiative is merely inherited/referenced but undefined.

## Initiative

```text
Initiative =
d20
+ Agility
+ Awareness
+ explicit Initiative modifiers
```

Locked baseline:

- roll once at combat start;
- higher total acts first;
- natural 1/20 have no special Initiative effect;
- no generic Training contribution;
- willing allied ties may choose order;
- otherwise ties compare Awareness, then Agility, then roll off;
- order normally remains fixed;
- completed turns are never retroactively undone;
- later entrants roll when they enter, acting this round only if their Initiative position has not already passed.

Awareness/participation is established before Initiative where fiction requires it, but a complete universal surprise/unaware procedure is still pending.

## Round Begin

Round Begin now provides the universal round-resource refresh point:

1. start-of-round expiries;
2. Guard capacity refresh;
3. Dodge Pressure resets to 0;
4. the one Reaction refreshes;
5. other explicitly per-round resources refresh;
6. authored start-of-round effects resolve.

Guard and Dodge remain defensive responses and do not consume the Reaction.

## Character turn

The locked turn skeleton is:

1. Start Expiry;
2. Regeneration Step;
3. start-of-turn effects/hazards;
4. establish Turn AP and derived Physical/Projection Tempo;
5. start-of-turn choices, including the Gifted Emotion Establishment Step;
6. normal turn;
7. end-of-turn effects;
8. End Expiry;
9. cleanup.

The procedure does **not** require declaring an entire turn in advance.

Turn AP is a turn resource. Unspent Turn AP is lost during cleanup.

## Regeneration and Dying

Natural regeneration now has an exact timing anchor: once on the character's own turn during the Regeneration Step, before ordinary start-of-turn hazards and ongoing damage.

This preserves the attrition model: damage suffered after the Regeneration Step normally remains until the next Regeneration Step.

Dying characters retain Initiative/turn timing. Regeneration-based survival/wound repair still requires available Vigor unless another rule explicitly provides an alternative resource or conversion. During their Regeneration Step:

1. determine throughput;
2. optionally spend 1 throughput to cancel the default 1 HP Dying loss;
3. apply that loss if not cancelled;
4. allocate remaining throughput to wound repair and permitted bleeding/ongoing-loss control;
5. restore HP only once wound-repair requirements permit it.

## Round End

Round End resolves authored end-of-round effects and end-of-round expiries, then the next round begins.

There is no additional universal regeneration, damage, or resource-refresh event at Round End.

## Hazards and sustained effects

Default timing for an ongoing hazard already affecting a creature is the start of that creature's turn **after** its Regeneration Step unless the hazard authors another trigger.

This is timing only; physical-hazard values/procedures remain unresolved.

Sustained/persistent effects do not gain an automatic universal round tick. Their outputs continue to use the locked Expression Cadence framework: Continuous, Rider, Pulse, Spend.

## Interception and duration baseline

Interception remains a timing mechanic rather than a new action category.

Default reservation window: until the start of the reserving character's next turn unless another rule says otherwise. If the trigger never occurs, the reservation is lost.

Explicit duration anchors are preferred:

- until start of next turn;
- until end of next turn;
- until start of next round;
- until end of round;
- once per round;
- Emotion Window;
- Sustained according to its own ending condition.

Bare `for 1 round` language should be avoided when a precise anchor is available.

## Explicit follow-up boundary

This lock deliberately does **not** close:

- detailed Reaction declaration and competing-trigger priority;
- detailed Interception declaration/priority refinement;
- broader turn-declaration rules;
- specialized movement layers beyond the Movement Foundation;
- weapon-family Reach assignments beyond the adjacent baseline;
- complete surprise/unaware rules;
- physical-hazard values/procedures;
- conditions.

Those are follow-up combat-procedure layers and should integrate with this clock rather than silently replace it.


---

# LOCKED UPDATE: Turn Declaration, Reactions, Interception, and Opportunity Responses

## Status: LOCKED STRUCTURE

The deferred timing layer following Initiative/Round Structure is now locked at the structural level.

Canonical procedure lives primarily in:

- `docs/rules/05-combat/initiative-and-round-structure.md`
- `docs/rules/05-combat/action-categories-and-physical-tempo.md`
- `docs/rules/05-combat/defensive-responses-and-criticals.md`
- `docs/rules/05-combat/off-hand-and-ranged-combat.md`

## Sequential turn declaration

A creature does **not** pre-declare its entire turn.

The default flow is:

1. declare the next action/effect;
2. commit its action capacity;
3. resolve any response window;
4. re-check legality;
5. resolve the action if still legal;
6. then choose the next action/effect.

Costs/action capacity are not refunded merely because the declared action is later interrupted, becomes impossible, or fails unless an explicit rule says otherwise.

## Attack Sequences and standalone attacks

All ordinary on-turn attacks against the same target are grouped into one **Attack Sequence**, including granted bonus attacks such as an offensive dual-wield off-hand Attack.

Before rolling:

- the attacker declares every ordinary on-turn attack committed against that target, including each attack's AP cost class and any granted bonus attacks;
- for each committed attack, the attacker declares its weapon/profile and other attack-specific choices that could affect resolution;
- the relevant Turn AP, granted attacks, and declared profiles/choices are committed;
- the defender assigns Take Hit / Dodge / Guard to each incoming attack with those declarations known.

The attacks then resolve in order. Each committed attack is its own trigger occurrence and opens its own response window immediately before its roll. If that attack survives the response window, it resolves; otherwise it is lost and the sequence proceeds to the next committed attack unless a stronger rule cancels the remaining sequence.

A creature normally opens only one ordinary Attack Sequence against the same target per turn. This prevents drip-declaring attacks one at a time to gain information after each result. A granted bonus attack used against that target must be included in that sequence; if the sequence has already resolved, the bonus attack cannot later be added against the same target, though it may be used against another eligible target.

Explicit follow-ups such as Riposte may override that restriction.

A standalone attack outside an Attack Sequence—including a Reaction, Interception, Opportunity Attack, Full Action attack, or explicit follow-up—receives its own defense declaration after it is declared and before its attack roll. It uses the same round Guard capacity and Dodge Pressure as all other attacks.

If the target becomes unavailable before all committed attacks resolve, unresolved committed attacks are not refunded. They may be redirected as a remaining sequence against another legal target only if that target has not already received an Attack Sequence from this attacker during the same turn, unless an explicit rule permits reopening that target. Their already-declared weapon/profile and attack-specific choices remain fixed unless an explicit rule permits changing them. The new target assigns defenses before those redirected rolls.

## Reactions

Reaction remains one per round and refreshes at Round Begin.

A Reaction:

- may be used during the creature's own turn when a valid trigger occurs;
- may respond to another Reaction, Interception, Opportunity Attack, or other response if its own trigger is met;
- does not by itself grant an action—an authored rule/effect must define the trigger and consequence.

Guard and Dodge remain separate defensive responses and do not spend the Reaction.

## Response windows

When an event creates a valid trigger, pause the event before resolution.

Precommitted Interceptions resolve before spontaneous responses to that same original trigger. Interceptions resolve in Initiative order, with any nested triggers they create resolved immediately.

After Interceptions finish, re-check the original event. If it remains legal/relevant, collect spontaneous Reactions plus Opportunity Attacks from either a newly activated or already-active Opportunity Response. Those responses resolve in Initiative order.

A response can create a nested response window; the nested window resolves before returning to the older response.

Once a Reaction, Opportunity Attack, or released Interception is declared, its relevant capacity remains committed even if an earlier response later cancels the original action, provided the responding action itself remains legal.

## Atomic Interception

Interception remains a timing mechanic rather than an action category.

A reservation contains exactly:

- one legal AP-based action/effect, committing its normal Physical, Projection, or General Tempo AP cost;
- one action/effect inherently defined as a Full Action, requiring and committing the entire Turn AP allotment; or
- one Movement Interception, committing a chosen amount of remaining MP.

A Full Action cannot be used to bundle multiple ordinary AP-based actions into one Interception. A Movement Interception reserves movement only and follows the canonical Movement Foundation.

One trigger occurrence can release at most **one** reserved Interception from the same creature.

Multiple reservations with the same trigger therefore cover successive qualifying trigger occurrences in declaration order. If fewer occurrences happen than were reserved for, unused reservations expire and are lost.

Different creatures may each release one reserved Interception from the same trigger occurrence.

## Interception is not automatic interruption

An ordinary Interception resolves before its triggering action but does **not** inherently cancel it.

After the Interception:

- if the action remains legal, it continues;
- if consequences make it illegal, it fails naturally;
- if circumstances changed but it remains legal, resolve it under the new circumstances.

An **Interrupt** must be an explicit consequence.

By default an Interrupt cancels only the current action and its committed cost.

For an Attack Sequence:

- interrupting one attack loses that attack;
- remaining committed attacks continue unless a stronger rule explicitly cancels the sequence;
- ending the entire turn requires explicit stronger wording.

The same current action cannot be explicitly cancelled more than once. Other already-triggered responses may still resolve, but their Interrupt components do not make that one cancelled action lose its committed Turn AP cost more than once.

Weapon traits, maneuvers, techniques, or similar content may later improve deliberate interruption. The universal numeric cost/modifier for a generic Disrupting Interception is **not** locked here.

## Opportunity Response

An Opportunity is an authored event that exposes a creature to an Opportunity Attack.

```text
Opportunity Capacity = Physical Tempo
```

The first time a creature exploits an Opportunity during a round:

1. spend its Reaction;
2. activate Opportunity Response until Round End;
3. make one eligible Opportunity Attack.

While active:

- further Opportunity Attacks do not spend another Reaction;
- total Opportunity Attacks that round cannot exceed Opportunity Capacity;
- each distinct Opportunity trigger can produce at most one Opportunity Attack from that creature;
- one creature may trigger multiple distinct Opportunities;
- multiple eligible enemies may separately exploit the same Opportunity.

A generic Opportunity Attack is one authorized attack, normally melee, and is not an Attack Sequence.

A generic Opportunity Attack does **not** automatically Interrupt its provoking action.

The existing threatened-ranged rule is a specific stronger trigger: firing a bow or crossbow while threatened creates an Opportunity before the ranged attack, and a successful resulting Opportunity Attack Interrupts that ranged attack.

## Remaining timing/combat dependencies

Still unresolved:

- Charge, climbing, swimming, jumping/falling, squeezing, size exceptions, flight, and other special movement modes;
- non-movement combat effects of Prone and whether Standing while threatened creates a specific Opportunity;
- final weapon-family Reach assignments beyond the adjacent baseline;
- exact weapon/maneuver traits or modifiers for deliberate Disrupting Interception;
- complete surprise/unaware rules;
- physical-hazard values/procedures;
- conditions;
- universal physical maneuvers.


---

# LOCKED UPDATE: Movement Foundation

## Status: LOCKED FOUNDATION

Canonical procedure lives in:

- `docs/rules/05-combat/movement-foundation.md`
- `docs/rules/05-combat/initiative-and-round-structure.md`

## Grid and Movement Points

One square represents approximately **1.5 m / 5 ft**.

```text
Movement Allowance = 12 MP per turn
Orthogonal step = 2 MP
Diagonal step = 3 MP
```

Movement is separate from Turn AP. Twelve MP permits 6 orthogonal squares, approximately 9 m / 30 ft, or 4 diagonal squares.

Movement may be freely split around actions. An action/effect begun by the **moving creature** ends that creature's current movement segment; enemy Opportunity Attacks, Reactions, and other spontaneous responses do not do so by themselves. Later movement after the mover's own intervening action/effect begins a new segment. Switching between Normal and Cautious Movement does not itself create a new segment.

## Cautious Movement

Cautious Movement doubles the base step cost before flat surcharges and prevents that step from creating the general Movement Opportunity for leaving threatened space.

Current examples:

- orthogonal Cautious step: 4 MP;
- diagonal Cautious step: 6 MP;
- orthogonal Cautious step through an ally: 6 MP;
- diagonal Cautious step through an ally: 8 MP.

## Occupancy and blocked corners

Hostile occupied squares cannot normally be entered or passed through.

Allied occupied squares may be passed through with a **+2 MP flat surcharge** applied after movement-mode multiplication, but cannot normally be used as the ending square.

Diagonal movement cannot pass through the touching corner of two orthogonally adjacent blockers when no usable physical gap exists.

## Reach and threatened space

Melee Reach is the set of squares presently targetable by an ordinary melee attack using a ready melee capability. The ordinary baseline is the 8 surrounding squares.

A creature threatens those squares while capable of the relevant melee attack. Remaining Turn AP does not determine whether Reach exists.

There is no separate universal engagement lock beyond Reach, threatened space, occupancy, and authored Opportunity triggers.

## Movement Opportunities

Entering threatened space does not provoke by default.

When a creature voluntarily attempts a **Normal** step out of a threatened square, the threatening enemy gains a Movement Opportunity **before the mover leaves the starting square**.

This applies whether the destination remains threatened or lies outside Reach.

The same enemy can gain at most one general Movement Opportunity from that mover during one movement segment. Cautious steps do not create this Opportunity.

Forced movement does not provoke by default. Teleportation/non-traversal relocation does not provoke from skipped squares, though activating a specific effect may separately be authored to create an Opportunity.

## Movement Interception

A creature may reserve any amount of remaining MP through the existing Interception framework, committing that MP immediately and declaring a specific trigger.

The exact route is chosen only when the trigger occurs. Reserved movement follows ordinary movement, occupancy, Cautious Movement, and Opportunity rules. A reserved Movement Interception cannot release during the reserving creature's own turn; it is an out-of-turn positioning reservation.

When a Movement Interception completes at least one legal movement step during another creature's movement, that active creature's movement segment ends. Releasing the reservation without moving does not break the segment. After a qualifying Movement Interception resolves, the mover re-evaluates the new state and may use remaining MP as a new movement segment.

## Still deferred

- Charge and other attack-linked movement maneuvers;
- extra movement purchased directly with Turn AP;
- climbing, swimming, jumping/falling;
- squeezing;
- size-based occupancy/reach exceptions;
- flight and other special movement modes;
- final weapon-family Reach assignments;
- detailed forced-movement procedures;
- non-movement combat effects of Prone and whether Standing while threatened creates a specific Opportunity;
- Reaction Blink AP Debt / Overdraw as technique/action-economy content.


---

# LOCKED UPDATE: Special Movement, Terrain, and Prone

## Status: LOCKED BASELINE

Canonical procedure lives in:

- `docs/rules/05-combat/special-movement-terrain-and-prone.md`
- `docs/rules/05-combat/movement-foundation.md`

## Sprint

Sprint is a **Full Action** and replaces the normal Movement Allowance for the turn.

```text
Sprint Movement Allowance =
3 × impaired normal Movement Allowance
```

An unimpaired ordinary creature therefore has **36 MP** while Sprinting.

MP already spent earlier in the turn remains spent. Sprint does not create a second movement pool.

When Sprint movement begins, choose one of the 8 grid directions as the Sprint Heading. Sprint movement continues along that heading; stopping or changing movement segments does not reset it. Sprint cannot use Cautious Movement.

If an external effect or response physically blocks further movement along the current Sprint Heading, the sprinter may pay **2 MP** for Forced Redirection and select a new heading. Voluntary turning without an external obstruction is not permitted.

Sprint otherwise follows ordinary terrain, occupancy, threatened-space, and Opportunity rules.

## Terrain

Terrain modifies **step cost**, not whole-turn Movement Allowance.

| Terrain | Step surcharge |
|---|---:|
| Normal | +0 MP |
| Difficult | +2 MP |
| Severe | +4 MP |
| Impassable | cannot normally enter |

Flat terrain and occupancy surcharges are applied after movement-mode base-cost changes.

## Movement impairments

Movement impairments reduce the creature's normal Movement Allowance.

For the ordinary 12-MP baseline:

```text
Impaired normal Movement Allowance =
12 MP - explicit impairment
```

Sprint then triples the impaired normal allowance, making the impairment proportionally meaningful at running speed. A serious effect may explicitly prohibit Sprint.

Movement Allowance cannot fall below 0 MP.

## Allied-square transit

Entering an allied occupied square requires enough MP and a legal route to enter and then leave that square as one continuous passage. The mover cannot intentionally begin the passage if it would become stranded sharing the ally's square under the known state.

The existing **+2 MP** allied-square surcharge remains flat and is applied after movement-mode changes.

## Prone, Crawl, and Stand

This lock defines only the movement consequences of Prone.

A Prone creature cannot use ordinary walking movement or Sprint. It may Crawl or Stand.

Voluntarily dropping Prone costs **0 MP / 0 Turn AP** and does not by itself end the current movement segment.

Crawl costs:

- orthogonal: **4 MP**;
- diagonal: **6 MP**.

Cautious Movement and Crawl stack additively by copies of the base step cost:

```text
Normal = 1 × base
Cautious = 2 × base
Crawl = 2 × base
Cautious Crawl = 3 × base
```

Thus Cautious Crawl costs 6 MP orthogonally or 9 MP diagonally before flat terrain/occupancy surcharges.

Standing from Prone costs **4 MP**, costs no Turn AP, and does not refresh Movement Allowance.

If a creature was knocked Prone after Sprint was activated, it cannot Sprint while Prone; after Standing it may resume any remaining Sprint movement under the existing Sprint Heading if still legal.

## Explicitly unresolved

- attack/Guard/Dodge and other combat effects of Prone;
- whether Standing while threatened creates a separate authored Opportunity;
- Charge;
- climbing, swimming, jumping/falling;
- squeezing;
- size exceptions;
- flight and other special movement modes.
