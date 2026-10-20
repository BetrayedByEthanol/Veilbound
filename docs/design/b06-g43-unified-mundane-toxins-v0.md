# B06 G4.3 — Unified Mundane Toxin Application/Effects v0

> **Executable bounded mundane-toxin integration, not a new toxin-rules amendment or full G4 certification.** Canonical authority is [Mundane Toxins v0](../rules/05-combat/mundane-toxins-v0.md), [Regeneration / Dying](../rules/06-vigor-wounds-death/hp-and-vigor.md), [the native initiative sequence](../rules/05-combat/initiative-and-round-structure.md) and [G4.2 world/encounter clock](b06-g42-persistent-world-encounter-clock-v0.md). Hunter's named pursuit venom, Venom Endurance, magical Death/Plague, treatment and full attack qualifications remain separate G4.4/G5+ work.

## Implemented source contract

[`MundaneToxins`](../../scripts/b06_mundane_toxins_v0.py) installs with the existing G4 `DamageState` and uses its **one shared G4.2 world clock**. It has one live mundane instance per recipient across *all eleven* canonical `TX-*` examples; finite source-identified exposure keys are never reusable. The old G4 bounded `schedule_hemotoxin` entry point remains available for earlier G4 tests but **cannot coexist on one recipient** with an active unified G4.3 instance.

### Delivery, nonstacking, ward, resistance

`toxin_state.apply(recipient, profile, exposure_key, source, route, delivery_verified, residual_piercing_hp, breach_verified, resistance_die, resistance_modifier, preventive_ward, wound_location_roll)` requires **source-attested material and allowed route**. Injection additionally requires **positive surviving Piercing HP after all mitigation** or a separately verified body breach. Contact requires actual susceptible exposed skin; inhalation must have viable inhaled material; ingestion actual consumed material. Those physical proofs are **caller-provided** (G5 owns hit/packet qualification); the engine never manufactures a hit, ingestion, inhalation, or contact.

Exactly one active **printed** Minor/Moderate profile: equal/lower grade is ignored **before** invoking a ward or requiring a resistance roll. A higher-grade eligible exposure can be independently prevented by an actually authorized `preventive_ward(encounter,recipient,profile,grade)` callback before the natural check; successful prevention does not overwrite the prior instance. That callback supplies **no ward by itself** and must come from an independently legally funded, timed, applicable effect. Otherwise the caller supplies one actual `d20` and any explicit sourced modifier: `d20+raw recipient Vitality+modifier >= DC10/12` selects the **literal** catalogue's Reduced profile; failure Full. The **raw Vitality lookup accepts the canonical capitalized player-sheet `Vitality` and lowercase JSON-enemy `vitality` source keys**; it never treats a missing ability as 0. No natural 1/20 automatic immunity, second save or invented default skill bonus. A valid higher printed grade replaces the previous future schedule **only after its new exposure is fully legal**. Previous actual losses never revert. Exposure identities are global to **both** the legacy G4 TX-HM scheduler and the unified executor, **even after a legacy toxin has completely expired**.

For recurring HP-damage profiles **TX-HM/TX-NC**, the source must precommit a `wound_location_rolls` sequence containing **one independent, actual d20 for every future damaging HP packet** (Full/Reduced 5/3 for TX-HM, 3/2 for TX-NC; TX-NC's first two toxin-local intervals are delay-only). The engine associates one value with the corresponding stable packet event ID; when two distinct packets each cross a repaired recipient from HP>0 to HP<=0, **each creates its wound using that packet's different precommitted roll**, never replaying the exposure's original one. A lone `wound_location_roll` is accepted only for immediate **TX-CY**. An absent, incomplete or invalid per-packet sequence is **unresolved before toxin acceptance**, preventing an asynchronous clock from advancing into a second wound without a new roll. Unused precommitted dice are not separate damage, a wound trigger, or an entitlement to roll again.

### Eleven profiles and timing

| Profile | Authored consequence implemented |
|---|---|
| **TX-HM** | Full **5** / Reduced **3** actual 1-HP short ticks; one per **genuine target Step 3** or completed **6s exploration interval**. |
| **TX-NE** | **−2 Dodge Defense** for **5/3** short intervals; native G0 melee and G2 ranged Dodge read only this modifier. Agility/Guard/Dodge Pressure unaffected. |
| **TX-CY** | **4/2 immediate HP** on actually valid skin-contact delivery, then **3** toxin-local intervals of active residual nonstack marker. |
| **TX-NC** | Exactly **two short onset-delay intervals**, then **3/2** 1-HP short packets. No irreparable injury or extra necrosis. |
| **TX-MY** | **−2 normal MP allowance**, **−1 eligible muscular Strength exertion** for **6/3** intervals; source Strength not changed. |
| **TX-CA** | **−1 throughput** on any real eligible Step 2 during **4/2** toxin-local intervals; no fictional Step 2 in exploration, never reduces 6h Recovery. |
| **TX-HE** | **−2/−1** from **one independently pending real Vigor Recovery checkpoint** within **6h**, or expire; full VP Recovery untouched. If milestone and checkpoint coincide, the Recovery-first phase is used; no newly manufactured checkpoint. |
| **TX-NP** | **1 direct Vigor damage** at each **4/2** actual hourly milestone via G4 packets, respecting separately authored G3 Vigor prevention, with **no HP conversion**. |
| **TX-PN** | **−2 ordinary MP**, **−1 actual breathing/endurance tasks** for **5/3** short intervals; no automatic suffocation. |
| **TX-EN** | **−1 eligible physical-exertion checks** for **3/2 elapsed hours**, one long expiry. No hourly damage. |
| **TX-DE** | **−1 Precision on checks genuinely using the contacted area** for **6/3** intervals, not blanket Precision/weapon attacks. |

Named modifiers are available through `toxins.modifier(recipient,use)`: `dodge`, `mp`, `muscular_strength`, `regen_throughput`, `breathing_endurance`, `physical_exertion` and `contact_precision`. G0/G2 automatically apply the executable Dodge penalty, G0 establishes the next real turn's reduced MP allowance and G4 applies TX-CA at real Step 2. Other adjudicated skill/task consumers must query the **specific** named modifier on a genuine eligible check; the engine does not re-author skills or change source attributes. A mid-turn active MP impairment can restrict current remaining MP, but expiry never refunds previously used MP.

### Temporal integration

G4.2 progresses the current unified short instance alongside legacy TX-HM, preserving exactly `0..5` leftover seconds when entering/leaving initiative. A real affected-creature Step 2→3 pair advances one interval, with TX-CA applying at Step 2 and other interval consequences at Step 3. Pure exploration progression applies short packets chronologically with **no free regeneration, AP/MP/Guard or Dying losses**. TX-NP's next pulse, TX-EN expiry and TX-HE maximum expiry are registered as **source-owned, cancelable G4.2 milestones**; q=floor(s/6) entry and `6*max(0,E-C-1)` exit apply independently to these and Recovery. Consumed marker IDs and recovery checkpoints cannot replay on mode changes. Original expiry vs Recovery deadline order is preserved when conversions coalesce; true-tie TX-HE Recovery precedes its maximum expiry.

### Deliberate boundaries

- A successful exposure requires **independently sourced real delivery**; this integration does not prove that the weapon/contact route was actually resolved by the attack/defense executor. Ward callback authorization remains external until G4.4's executable Venom Endurance linkage.
- **Hunter B06-TX-HUNTER-SLOW-MY**, Bite residual-Piercing gate integration, staged pursuit penalties and finite preventive/suppression-unit spending remain G4.4, not a twelfth generic catalogue entry.
- No additional toxin families, optional higher grades, antidotes, unauthorized medical cure or irreparable injury. `stop_authorized` is an explicit externally authorized end-state integration port, not an unconditional cure mechanic.
- Noncombat physical checks must use the exact named modifier; current bounded G0/G2 native handling proves Dodge, MP and Step2 parity but is not a claim that all future G5/G6 contest actions have already been integrated.
- This integration adds no complete Soldier/Sentry/Hunter encounter, historical 22 wound-stop replay, 12 Focus certificates or numeric Hunter CR.

## Tests

[`test_b06_mundane_toxins_v0.py`](../../tests/test_b06_mundane_toxins_v0.py) covers profile inventory, actual physical exposure gates, **all three lowercase JSON-enemy Vitality sources**, one-instance grade precedence, **non-reusable expired legacy exposure keys**, ward-before-resistance ordering, natural tie and full/reduced outcomes, **distinct packet-indexed wound-location d20 rolls across repeated repaired 0-HP crossings**, each profile's exact packets/penalties/expiry, TX-HE existing checkpoint semantics, native Step 2/3, exploration partial phase, conservative clock mode conversions, old TX-HM interoperability and no virtual Dying or regeneration. Existing G0–G4.2 tests and **unchanged historical 4,096 Hunter Phase 3 one-round corpus** provide compatibility checks.

```bash
python -m unittest discover -s tests -p 'test_b06_mundane_toxins_v0.py' -v
python -m unittest discover -s tests -v
```

**Next: G4.4 Hunter venom & Venom Endurance; then G4.5 wound continuation alongside G5 scene integration.**
