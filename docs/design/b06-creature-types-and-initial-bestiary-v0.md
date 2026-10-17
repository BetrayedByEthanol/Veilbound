# B06 — Creature Types, Revised Benchmark Schema, and Initial Bestiary v0

> **DESIGN-SCOPE taxonomy and initial content index, not canonical species rules or a certified bestiary.** The user-provided Veilbound species/monster concepts are recorded here as proposed setting constraints; canonical [Volition and Pillar metaphysics](../world/veil-and-pillars.md), [48 Aspect domains](../world/aspect-identities-and-boundaries.md), [Anointed surges](../rules/08-archetypes/anointed.md), [Mundane Toxins](../rules/05-combat/mundane-toxins-v0.md), and existing combat procedures remain authoritative. Neither a creature category nor a Pillar tag grants a spell, immunity, movement mode, action, toxin exposure or natural attack without separately authored rules. No playable nonhuman species are included in the **MVP**.

## 1. Creature ontology: independent dimensions, not mutually exclusive classes

| Dimension | Purpose | Examples / important limits |
|---|---|---|
| **Family** | What sort of combatant/presence? | Ordinary humanoid, Archetype humanoid, natural beast, Veil-touched beast, dragon, raised undead, turned undead, surge manifestation, spirit, unresolved species |
| **Species or kind** | Physical/ecological identity | Human, Elf, Orc, Goblin, Dwarf, Hunter of the Woods; no fixed personality, culture, occupation or player Archetype inferred from species |
| **Body state** | What material form is present? | Living body, **corporeal raised**, **corporeal turned**, Veil-formed, nonphysical spirit, unknown |
| **Cognition** | Ability to deliberate, not combat difficulty | Sapient, animal-like, **non-sentient pattern**, undetermined; dragon mostly animal-like, manifestation non-sentient |
| **Veil relationship** | Origin or mode of supernatural capacity | Ordinary connection/no independent invocation, learned/bonded Archetype, **outward dominant**, **inward dominant**, innate Pillar affinity, Veil-touched, reanimation, transformation, surge-formed, posthumous spirit |
| **Physical presence** | Whether ordinary physical attack interaction is even applicable | Corporeal, conditionally manifested, nonphysical/no ordinary interaction, undetermined |
| **Capability source** | Exact origin of each attack/effect | Ordinary wielded weapon, biological bite/claw/horn, actual authored item effect, learned Veil technique, innate creature effect, physical undead animation, Veil manifestation |
| **Implementation status** | Explicit playability gate | Existing executable combat fixture, conceptual NPC/creature, deferred future type |

**No default "monster Focus":** A normal human soldier, natural wolf-like beast, dragon or raised skeleton is not automatically Low/Medium/High Focus and need not receive Priest/Scholar/Gifted/Anointed known-technique counts, VP or Talent progression. The [revised benchmark schema](../../schemas/b06-enemy-benchmark-v0.schema.json) keeps `progression` **required only for player-rules-derived opponents**. Every future executable stat block still needs actual legal **AP, movement, defenses, resources and effect sources**; the absence of player Focus never grants free attacks or magic. A future non-Archetype creature's `max_vp: 0` states it has no personal spell-VP budget in that fixture; it is not a universal metaphysical claim that no innate expression could ever exist.

### Species direction and human cultural range

- **MVP player species:** human only. Many different human cultures and individual backgrounds can create broad character variation without obligatory fantasy-species player rules. Other sapient species exist as world inhabitants and NPCs; no individual is required to behave like a species stereotype.
- **Ordinary humans:** a Veil relationship and Vigor, but **no personally accessible Veil invocation** without one of the valid exceptional access mechanisms. Conventional equipment and externally sourced, individually authored magical items are separate.
- **Elves:** an extreme outward-dominant Veil relationship, with very weak inward reinforcement and extremely low Vigor/physical durability. **Do not simply assign a player High Focus or its AP/VP formulas.** Social displacement/isolated populations are a setting direction, not universal elf psychology.
- **Orcs and Goblins:** inward-dominant Veil integration, high Vigor and actual regeneration, **no independent outward Projection/spellcasting**. Some larger forms, especially Orcs, may have leathery skin. Vigor maxima, regeneration throughput and natural Armor are **independent values** requiring authored numeric rules; don't presume armor stacking or uniform social identities.
- **Dwarves:** explicitly **TBD**. No imported crafting, mountain, size, psychological or magical stereotypes.

### Creature-specific distinctions

- **Dragons:** flying biological creatures with natural attacks and breath attacks, mostly animal-like cognition (approximately canine or modestly higher), usually a strong instinctive affinity for a Pillar. **Not ordinary spellcasters.** Their instinctive pattern expression **does not automatically contribute sapient volition** or create a personal Anointed Mission. Breath geometry and flying combat remain beyond the initial B06-A.
- **Hunter of the Woods:** larger/bulkier than a bear with a wolf-like head, horn and venomous bite. Bite, horn and possible body strike are **three potential profiles, not three granted attacks per turn**. Its venom must be assigned one explicitly authored biological source and eligible [TX catalogue](../rules/05-combat/mundane-toxins-v0.md) effect; a positive **post-mitigation puncture** or independently established breached route must survive before injection exposure. The horn **does not inherit** bite venom.
- **Veil-touched Dire Giant Spider:** aggressive enormous spider, with the details of its Veil alteration **undetermined**. Veil-touched is an origin, **not a free magic attack, poison, web binding or spell repertoire**.
- **Raised versus Turned undead:** **Raised** = previously existing corporeal physical remains animated (skeletons, zombies, ghouls). **Turned** = an existing being changed into an undead state (vampires, liches). No default package of poison immunity, zero Vigor, infinite regeneration, inability to wound, unique weakness, all-spells-access, mindlessness or single command structure. Their physical recovery/HP/Vigor/Dying and identity retention need creature-specific rules. These do **not** become independent spirits.
- **Independent spirits:** real posthumous presences under **Death / Spirit**, nonphysical and fleeting, with no ordinary physical interaction; separate from the physical undead and ordinary combatant pool. Summoning/communication requires individually authored capabilities, not a free melee ghost.
- **Veil Manifestations:** non-sentient formations from an exceptional Pillar-related Veil event, potentially a surge like the event associated with an Anointed's origin but **not born individuals with a permanent Mission, Destiny or 0-VP Signature**. They may be fleeting, anchored or persistent **only when authored**. Their conduct reflects the source Pillar/Aspect and event imprint without personal will, human moral alignment, angel/devil/demon metaphysics, or personified Pillar commands. Formation is **not guaranteed by a surge**. The community's sapient choices can sustain the originating Pillar; a non-sentient manifestation does not itself create fresh sustaining Volition. Physical presence, dissipation, resource/cadence and combat targeting require later definition.

## 2. Initial bestiary register

The [machine-readable 14-entry seed](../../content/creatures/b06-initial-bestiary-v0.json) is validated against the [standalone bestiary-index JSON Schema](../../schemas/b06-bestiary-index-v0.schema.json). **Only B06-EN-01 already has a complete separately authored attack-capable fixture.** All listed non-Sentry abilities are **capability *candidates*** and do not count as usable attacks until individual source and numeric rules are published.

| ID | Creature | MVP window | First useful role / status |
|---|---|---|---|
| **EN-01** | **Firebound Sentry** | B06-A | **Already executable** in [original PR #84 fixture](../../content/creatures/b06-firebound-sentry.v0.json): sword and maintained Conjure Flame; linked to this taxonomy |
| **EN-02** | Ordinary Human Soldier | B06-A | First non-Archetype **mundane weapon**/Armor/Guard comparison; NPC AP and derived numbers require an independently authored baseline |
| **EN-03** | Hunter of the Woods | B06-A | First **natural bite/horn** and real biological toxin-delivery source; large creature combat math pending |
| **EN-04** | Veil-touched Dire Giant Spider | B06-A | Aggressive **Veil-altered beast**; precise alteration and any venom/web effect pending |
| **EN-05** | Goblin | B06 later | Inward-only high-Vigor/regen physiology, non-playable MVP |
| **EN-06** | Orc | B06 later | Larger inward-only physiology, possible leathery skin; independent Armor interaction required |
| **EN-07** | Elf | B06 later | Outward-dominant/low-Vigor asymmetry; exact casting access and durability unresolved |
| **EN-08** | Dwarf | Post-MVP | **TBD**, avoid inventing biological/cultural roles |
| **EN-09** | Dragon | Post-MVP | Animal-like Pillar affinity, flight/breath; **not a spellcaster** |
| **EN-10** | Raised Skeleton | B06 later | First **corporeal reanimation** and injury/repair tests |
| **EN-11** | Turned Vampire | Post-MVP | Transformation, retained identity, independently authored power package |
| **EN-12** | Turned Lich | Post-MVP | Transformed individual; previously learned magic only if explicitly established |
| **EN-13** | Pillar Surge Manifestation | Post-MVP | **Non-sentient** pattern-formed entity, source/anchor/dispersal, optional physical form |
| **EN-14** | Independent Posthumous Spirit | Post-MVP | Nonphysical fleeting presence, not currently an ordinary combat target |

B06-A should initially build/verify the **ordinary soldier** and **Hunter** after reviewing this schema update. EN-04 can follow once its unique innate alteration is selected. This does **not** mean all four initial rows are complete or balanced.

## 3. Schema changes and backward compatibility

- Keep existing `schema_version: "b06-enemy-v0"`, ID format, **B06-AT-01/02**, numeric packets, original Sentry's AP/VP math, and legacy enemy fixture contracts valid. No universal rules or combat numbers changed.
- `creature_profile` adds independent `family`, `species_or_kind`, `body_state`, `cognition`, `veil_relationship[]`, `physical_presence`, `mvp_player_option`, possible `pillar_affinities[]`, physiology and behavior notes. The Sentry now has `bestiary_ref: "B06-EN-01"` and exact linked profile metadata.
- `identity.type` now distinguishes a legitimate player-rules-derived opponent, non-Archetype ordinary humanoid, generic creature, raised/turned undead, manifestation or nonphysical spirit. For **any non-player-derived executable creature**, `creature_profile` is mandatory. For player-derived opponents, `progression` remains mandatory; for ordinary humans and monsters it is optional.
- Attack records may separately tag `source_class`, `resolution_kind`, `source_authority_ref` and `target_geometry`; these classify **only an already legal authored attack**, never create its accuracy, action, breath AoE, natural weapon damage or supernatural source. Toxin records now require an explicit `source_ref` pointing to an independently authored real delivery mechanism in addition to a catalogue profile and declared route. **A string-shaped reference is not proof that the cited source exists**; validate provenance during Codex Review or source-link tests.
- **No false completeness:** the concept index uses **separate typed entries** with required `planned_capabilities[].state` and `missing_authority[]` fields. Nothing in the index can be passed to an encounter resolver as an executable stat block. The index schema uses a self-contained copy of the shared concept definitions and [regression tests](../../tests/test_b06_creature_types_v0.py) check those definitions remain in sync with the benchmark schema.
- Future migrations can expand natural-weapon/area/non-damaging ability resolution or individual creature resource models **without making them automatically legal now**. In particular the existing B06 executable `attack_roll` and `primary_hp_packet` remain mandatory and numeric; non-weapon innate abilities require later authored source and resolution procedures before they can be encoded as executable profiles.

## 4. Acceptance gates and explicit non-goals

| Slice | Required proof | Current |
|---|---|---|
| Creature taxonomy | Independently record species, physiology, cognition, Veil origin, physical presence and player-access scope | **Authored design v0** |
| Executable Firebound Sentry migration | Same weapons, source/typed packets, AP/VP/defense values; linked to initial index | **Metadata-only extension; regression required** |
| Human soldier | No Archetype, no personal learned spells; exact lawful physical action/defense statistics and perhaps separately paid item effects | **CONCEPT; not yet executable** |
| Hunter of the Woods | Body-scale rule or local documented constraint, bite/horn/other AP, real source-linked venom profile, post-armor piercing injection gate and limits | **CONCEPT; not yet executable** |
| Veil-touched spider | Exact actual alteration rather than automatic "spider magic" | **CONCEPT; not yet executable** |
| Undead, dragons, manifestations and spirits | Creature-specific metaphysics plus physical target and resource constraints | **Deferred; no innate immunity package** |
| B06-A completed encounter pack | Fully opposed combat traces against both [Low Life Priest builds](b05-life-low-priest-l3-build-exaltation-verification-v0.md), natural responses, actual end-to-end damage/VP/Vigor/provenance | **OPEN; 0/12 Focus certification unchanged** |

**Next implementation PR after review:** develop EN-02 Ordinary Human Soldier with a **source-backed non-Archetype NPC action/tempo budget**, and EN-03 Hunter with independently authored natural attack and toxin material delivery. Build one actual opposed attack sequence against each verified Life Low Priest. Do not silently infer an NPC Focus, venom coating, full dragon flight or undead poison immunity.
