# B06 G4 — Damage, Wounds, Dying and Recovery Integration v0

> Bounded source-backed integration candidate. This is neither a new combat ruleset nor a complete G5–G7 encounter certificate. Canonical sources govern: HP and Vigor; Dying and Wounds; Weapons and Armor; Elemental Damage and Resistance; Basic Heal; Mundane Toxins; Volition Points.

## Reusable native state and authored transitions

- Executor: scripts/b06_damage_v0.py, DamageState(encounter). G0 without G4 retains its existing documented behavior. The event ledger records actual HP, Vigor, wound, repair and maintained-effect transitions.
- Damage: only independently confirmed hits/packets; no newly invented attack resolution. Ordinary physical weapon HP packets use effective Armor after source Penetration, then one applicable highest typed resistance. Explicit Fire HP bypasses physical Armor. Direct Vigor packets are separate and use remaining current Vigor before finite G3 Vital Shelter prevention. Multiple components share one event-wide wound trigger. Distinct event keys cannot be replayed.
- Source adapters: Soldier/Sentry/Hunter fixture damage profiles with explicit legal damage die and verified critical d4 faces; Sentry's actually active Sword Reserve controls ordinary versus enhanced profile. G3 Thrown Flame is accepted only from its genuine pending direct-hit ledger entry. Hunter Bite yields puncture eligibility only after mitigation, not an automatic accepted venom exposure.
- Wounds: actual location d20 is an explicitly required input whenever an event can create a wound. The first positive-to-nonpositive HP crossing, or a separately confirmed Devastating Critical, creates at most one default Serious/Severe/Critical wound at 10/20/30 cumulative Repair Requirement. Death at HP <= -MaxHP does not manufacture a repairable alternative. Identity, trauma, source event, location and severity remain recorded.
- Regeneration: use only G0's existing own-turn Step 2, including G3 Guided Regeneration +1 throughput. Non-Dying players explicitly allocate HP versus individual wounds, debiting one Vigor per actual point. Dying applies survival-cost choice, default HP loss if not cancelled, oldest-first cumulative Repair Progress, and HP only when no incomplete or irreparable blockers remain. HP threshold death ends maintained effects; unconsciousness ends Stone Skin and dependent Shelter, but not otherwise valid Guided Regeneration.
- Basic Heal: genuine paid G3 F/R Primary works on self and independently verified in-range/unobstructed Single Target beneficiaries when genuinely beneficial and unopposed. Ordinary direct HP and Vigor never debit recipient regeneration. A Dying recipient directs 2 Primary or 1 Secondary HP-equivalent points toward one selected unfinished wound (fallback oldest), with no spill; only legally usable surplus heals HP. G3 Self Primary and authorized Composite Secondary use the same non-Dying wound-aware resolver if G4 is attached. Unavailable resisted Intrusion is rejected rather than guessed.
- Clock bridge: a narrowly supported TX-HM Full five or Reduced three future one-HP ticks executes at genuine target Step 3 or completed six-second exploration intervals. Exploration never grants virtual regeneration, wound repair or Dying losses. Completed six-hour elapsed intervals apply source-derived 25%-half-up Vigor Recovery and VP Recovery from Spent only, preserving Committed VP.

## Deferred and unresolved G4 dependencies

This adapter does not establish physical contact, hit/critical qualification, Called Shot action costs, exceptional Catastrophic/Irreparable/Fatal physical outcomes, ongoing bleeding/Medicine treatment, full toxin-family nonstacking/ward or Hunter venom 10/30/60/120-minute milestone continuity. TX-HM accepts independently verified exposure and resistance; it does not invent an injection or cure. Wider initiative/exploration clock conversion, elapsed recovery phase existing before scene creation, and full contested healing require explicit sourced policies.

The historical 22 Phase 3 wound stops are not replayed as though G5/G6 decisions were available. The original 4,096 Hunter observations and checksum remain unchanged. No Soldier/Sentry/Hunter encounter is certified; the 0/12 Focus certificates and unrated Hunter CR remain unchanged. G4 is a bounded executable candidate, not a claim that every G4 gate acceptance criterion is complete.

## Verification

Focused suite: python -m unittest discover -s tests -p 'test_b06_damage_v0.py' -v

Full suite: python -m unittest discover -s tests -v

Both are included in the updated exact-PR-head GitHub Actions verification workflow. Follow-on work should finish unresolved damage and toxin clocks under G4, then implement G5 Soldier/Sentry, G6 Hunter, and G7 calibration without silently changing canonical rules.
