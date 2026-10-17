# B06 Enemy Benchmark Schema and First Attack Profiles v0

> **EXECUTABLE BENCHMARK FIXTURE / DESIGN-SCOPE CONTENT — NOT NEW UNIVERSAL COMBAT RULES.** This creates one machine-readable [enemy schema](../../schemas/b06-enemy-benchmark-v0.schema.json) and a [Level-3 Firebound Sentry fixture](../../content/creatures/b06-firebound-sentry.v0.json) using only the current sword, Low Priest, Conjure Flame, and defense rules. It does **not** complete the B06 opponent/scene pack, invent monster poison delivery, or certify any of the 12 Archetype × Focus identities. [Roadmap B06 acceptance gates](veilbound-roadmap-and-mvp-readiness.md#b06-next-acceptance-slice--comparative-level-3-life-low-priest-encounters) remain open.

## 1. Data contract

The [JSON Schema](../../schemas/b06-enemy-benchmark-v0.schema.json) declares a reusable `B06-EN-xx` test-opponent record: source references; archetype/Focus if derived from a character; all nine Abilities; Training, Talents and Prepared techniques; HP/Vigor/Armor/Guard/Dodge; Initiative, Turn AP, movement, real VP ledger, start states and maintained effects; an array of typed attack profiles; bounded tactics; and audit caveats.

Each attack profile contains:

| Field | Purpose / legality |
|---|---|
| `id`, `name`, `weapon_or_source` | Stable attack ID and exact weapon/creature-authored delivery source; a monster's name alone cannot grant a weapon or sting |
| `action_class`, `ap` | Actual paid action, with native Full Action/Reaction authority separately required; never infer free attacks from a magical packet |
| `attack_roll` | The **two explicit Abilities, one effective Training source and other modifiers**, plus checked final attack bonus. A natural-20 confirmation is **not a separate attack** |
| `primary_hp_packet` | Original typed physical/elemental direct-hit HP packet, with die/base, physical contribution and physical Penetration/Armor or typed resistance |
| `additional_packets` | Independently typed Fire HP / direct Vigor payloads; retain source and type through defenses and finite event-wide prevention |
| `required_active_effect` and `requires_effect_inactive` | Mutually exclusive legal equipment-state profiles. A Reserved Weapon's extra packets apply automatically on every qualifying successful hit |
| `toxin_delivery` | **Optional explicit source record.** Must identify a real authored attack/creature/hazard source, catalogue toxin and route; an unassigned toxin catalogue name cannot create injection |
| `critical_notes`, `legality_refs` | Which primary packet receives the **one** Strong/Critical HP-dice addition, natural-20/confirmation procedure and exact canonical reference |

The schema verifies **data shape, not rules legality by itself**: JSON Schema cannot establish that a Priest legally prepared a Fire technique, that the armor and damage calculations are correct, or that a monster has a real venom source. The fixture's `validation.formula_checks`, worked numbers, and a future independent rules validator must check that.

### Explicit scope and source hierarchy

- A `content/creatures/` file marked `EXECUTABLE_TEST_FIXTURE` is an **encounter-development exemplar**, not general permission for every NPC to buy magic or poison.
- Canonical action, damage, HP/Vigor, defense, Tier, Rite and toxin rules in `docs/rules/` take precedence over the fixture.
- Do not treat `benchmark_level: 3` as a monster challenge rating, threat value, XP award or automatic encounter difficulty. The entry happens to use a real **Level-3 Priest/Low character-equivalent chassis**, not an invented monster scaling equation.
- Start modes are *separate initial conditions*, not simultaneous alternative reservoirs. Record which one was used and whether actual elapsed preparation/action/recovery permits the pre-armed state.
- The enemy's tactical policy is an explicit **test choice**, not an AI rule granting extra actions. If a scenario suppresses use of an otherwise known Talent for comparison, record it as **policy**, not a missing Talent.

## 2. First benchmark opponent: B06-EN-01 Firebound Sentry

One legally constructed **Level-3 Fire Low Priest** has **Chosen Conjure Flame** prepared. It is based on the legal physical build template of [PR #82](b05-life-low-priest-l3-build-exaltation-verification-v0.md), replacing Life access with Fire and limiting its current legal spell menu to authored Fire/Conflagration content. At L3 the Fire-specific Exaltation **is NOT authored**; the Level-3 feature cannot generate a custom Fire benefit.

| Derived quantity | Value | Authority / calculation |
|---|---|---|
| STR / AGI / PRE / AWA / VIT / VA / VC | **+2 / +3 / 0 / +1 / +2 / 0 / 0** | All nine Abilities in machine fixture; complete allocation costs 28 points |
| HP / Vigor / VP at L3 | **12 / 36 / 6** | HP `10+VIT`; Vigor `(10+VIT)×3`; Low VP `(2+VA)×3` |
| Turn AP / Physical / Projection | **42 / 20 / 30** | Low Focus L3 |
| Sword Attack / Guard | **d20+7 / Guard 17** | STR2 + AGI3 + Sword Training2; Guard =10 +same |
| Dodge / Initiative | **14 / d20+4** | Leather Dodge-cap4, AGI3+AWA1 |
| Leather Armor / Sword Pen | **Armor 3 / Pen 2** | Sword uses **3+d6 + Light(STR2)=4+d6** raw Piercing HP, before target Armor |
| Guard capacity / genuine regeneration | **3 / 6 throughput per actual Step** | Low L3 Physical Tempo2 + TAL-C05 1; VIT2 + Low3 + TAL-C02 1 |
| Gear purchase | **70 sp** | Leather25 + Sword22 + medical kit15 + pack8 |
| Chosen Fire Reserved Weapon, Tier 1 | **3 Committed VP** | Baseline4 −1 Chosen, one particular wielded sword; no extra per-hit VP |

The enemy's **L3 TAL-C10 Emergency Regeneration** is a real available Talent, but the simple benchmark policy may explicitly disable its choice to measure unassisted weapon output; a separate scenario must test its actual Reaction/VP/Vigor consequences before considering this opponent's full survival.

### Profile B06-AT-01 — Ordinary sword thrust

- **Legal only when the sword is wielded and the Conjure Flame Reserve is not active.**
- **One Physical Action = 20 AP.** The Priest can pay for at most **two** in a 42-AP turn, declared together against the same target as one Attack Sequence.
- Attack **`d20+7`**; on an ordinary hit, deal **`4+d6` raw Piercing HP**, Penetration **2**, then **`max(0, raw − max(target Armor−2,0))`**.
- Natural-20 confirmation adds **Strong +1d4 / Critical +2d4 / Devastating +2d4 + wound trigger** once to the primary sword HP packet **before Armor**. There is no automatic separate Fire, direct Vigor, poison, or free additional swing.

### Profile B06-AT-02 — Conjure Flame T1 Reserved Weapon sword thrust

- Legal **only while the exact selected sword remains actually wielded and its Chosen `B06-FIRE-RESERVE-01` effect is active**. It **replaces B06-AT-01** in that state; the attacker cannot choose to omit the mandatory Fire/Vigor on-hit packets.
- The **same one Physical Action (20 AP)** and **same `d20+7` weapon attack roll** deliver **three distinct packets on success**:

| Packet | Raw output | Defense / mitigation |
|---|---|---|
| Primary **Piercing HP** | **`4+d6`**, Pen 2 | Existing weapon hit and physical Armor once; receives any qualified Critical bonus dice |
| Secondary **Fire HP** | **2** | Explicit **Fire Resistance** only by default; **not** another physical Armor subtraction |
| Secondary **direct Vigor** | **`1+ceil(d6/4)`** at T1 VC0 = **2–3 Vigor** | Not automatically reduced by Armor or Fire Resistance; valid separately authored Vigor protection may intercept |

No Burning, Ignite, area effect, additional weapon attack, bonus Reaction or stand-alone Rider is granted. A blocked/missed **physical weapon hit** causes **none** of these additional packets. If the physical HP is stopped by Armor but the **weapon attack actually hits**, Fire HP and direct Vigor still apply.

**Cold start:** Begin with **6 Available / 0 Committed / 0 Spent**. One **30-AP** Projection Action establishes Tier-1 Chosen Reserved Weapon with **3 Committed**, leaving **3 Available** and **12 Turn AP**; an ordinary 20-AP sword swing **cannot fit that turn**. First enchanted sword attack is possible on a later legal physical action, not as a bonus to the cast.

**Prepared start:** The exact sword was already legally enchanted before combat, continuously wielded, with **3 Available / 3 Committed / 0 Spent** at initiative start. A sword attack can occur on the first turn without re-paying setup AP, only because the state was actually established earlier. Disarm, sheathing, stow or a legal drop **immediately end** this channel; refund exactly **3 Committed**, never an imagined base 4. The spell cannot spontaneously revive on re-wield.

## 3. Attack math sanity fixtures (ordinary hits, not observed outcomes)

Assume the defender elects/legally resolves a response and the sentry's attack **actually hits**; roll an ordinary `d6 = 4`, with no critical. The numbers below validate *post-hit damage arithmetic only*, not hit probability or entire damage order.

| Defender | Raw sword HP | Effective Armor | Final physical HP | Additional HP/Vigor while Fire-armed |
|---|---:|---:|---:|---|
| **Restorative Vanguard**, Leather Armor3 | `4+4=8` | `max(3−2,0)=1` | **7 Piercing HP** | **+2 Fire HP**, **+2 or +3 direct Vigor** |
| **Preservation Guardian**, Brigandine Armor5 | `4+4=8` | `max(5−2,0)=3` | **5 Piercing HP** | **+2 Fire HP**, **+2 or +3 direct Vigor** |

Vital Interposition is applied **only after the target's legal actual Rite and Exaltation activation**, once to the triggering event's *individually mitigated* HP packets and attributed **primary direct-hit Piercing first**. Its actual original Vital Shelter budget is then used for the remaining independent Vigor packets. Held Renewal, if genuinely armed at its actual prior Regeneration Step, attempts healing **after** fully resolving the damage and cannot reverse a Dying crossing. Do not automatically grant either Exaltation because the defender's build has it on its sheet.

## 4. What is still required before the full B06-A encounter pack

1. **Opponent review:** Codex-verify the exact Fire Low Priest's access, L3 talent allocation, preparation, effective Chosen reservation, wound/critical timing and numeric Defense. A schema-valid fixture is not an independently certified Fire Priest Focus.
2. **Real opposed encounters:** Provide map/starting positions, initiative rolls, attack sequences, defender defense assignments, actual attack/confirmation/damage dice, and turn-by-turn HP/Vigor/VP and effect-state logs. No encounter has been rolled or simulated merely by authoring these profiles.
3. **Separate toxin-bearing source:** [Mundane Toxins v0](../rules/05-combat/mundane-toxins-v0.md) offers valid profiles such as TX-HM Thornblood venom but **does not authorize weapon coating, a natural stinger or injection by itself**. A later independently authored monster/hazard/ability must supply genuine injection delivery and an explicit catalogue link; then use the schema's optional `toxin_delivery` field. **Never add free poison** to B06-AT-01/02.
4. **B06 comparison and coverage:** Test both previously audited Low Priest Life defenders under identical legal cold/prepared starting conditions; then add physical-only and toxin counterparts plus exploration/social content, and eventually High/Medium Priest and other Archetypes. No change to the parent roadmap's 0/12 certified-build status.

## 5. Next verification actions

- Parse both JSON files and validate the enemy record against [schema v0](../../schemas/b06-enemy-benchmark-v0.schema.json).
- Check VP invariants (`Available + Committed + Spent = Max VP`), fixed Ability budget, sword Attack/Guard, critical/Armor math and conditional magical packet presence.
- Validate that no attack carries a `toxin_delivery` object without its actual separately authored delivery source.
- Next PR: create the three encounter records and event-log contract, resolve at least one **fully opposed** combat trace against each Life Low Priest build, and only then run any larger balance simulation.

**State:** B06 **enemy schema + initial physical/magical attack profiles authored for review**; no complete encounter, no sourced toxin weapon, no Focus certification and no numerical balance change.
