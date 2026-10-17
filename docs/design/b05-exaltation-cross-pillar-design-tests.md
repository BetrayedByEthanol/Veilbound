# B05 — Exaltation cross-Pillar design validation (non-executable)

> **DESIGN TESTS ONLY — NOT NEW PLAYER POWERS.** Stress-test the [locked universal Exaltation framework](../rules/08-archetypes/low-priest-exaltation-framework-v0.md) against two existing non-Life maintained techniques. No Earth/Fire Level-3 Exaltation is authored or granted by this page. Its draft property descriptions are illustrative authoring probes, not spells, selectable features, prices, damage packets or actual statuses.

## Earth / Fortification — Stone Skin

**Canonical test host:** [Stone Skin v0](../rules/07-veil-magic/stone-skin-v0.md) has a self-targeted maintained Primary with `ceil(Max VP/3)` Committed VP, Physical/Fire/Electrical HP resistance `R = 2 + floor(max(0, VC)/4)`, and its own authorized normal Projection Action or qualifying Reaction. Even though its expression tag is `[Projection]`, **a Low Priest who has legally Prepared and maintains this as their one active Chosen Rite** satisfies the universal Rite rule. Its aspect is **Earth / Fortification** (Internal).

| Architecture check | Result |
|---|---|
| Qualifying host | **PASS**: actual self target + active Committed-VP body reinforcement |
| Same-Aspect Level-3 identity | **PASS** for a future **Earth / Fortification** property only, never for Life / Restoration |
| Required host predicate example | Ongoing body-integrity/typed resistance; not a Regeneration Step modifier or a finite shelter pool |
| Illustrative secondary behavior | **Anchored Posture**: momentarily express fortification as physical stability against one qualifying shove/forced movement event; exact effect, timing, size limits, cost and contest interaction **NOT AUTHORED** |
| Action timing | Existing Stone Skin's **Reactive activation does not grant a free Reactive Exaltation**. A future property must explicitly provide and pay its own trigger/action (or integral event) |
| Stacking/defense | Cannot infer +Guard, additional Armor, stacked resistance sources, free Dodge, general immunity or a new displacement contest |
| Death/host loss | Stone Skin ends on unconsciousness; any pending Exaltation ends at the same time without a separate VP refund |
| Verdict | **Framework suitable**; illustrative Earth effect remains **NON-EXECUTABLE** pending full authored profile and calibration |

**Negative case:** A Stone Skin Chosen Rite cannot activate Life Held Renewal just because both are maintained and self-targeted. It has neither the matching Aspect nor the required regeneration capability. A separate Level-5 cross-Pillar permission does **not** exist: Living Liturgy stays inside the same Pillar.

## Fire / Conflagration — Conjure Flame

**Canonical test host:** [Conjure Flame v0 — Reserved Weapon](../rules/07-veil-magic/conjure-flame-v0.md#b-reserved-weapon--weapon-enchantment) enchants **one weapon the caster continues actually wielding**; its Tier-1 base reserve is **4 Committed VP**, **3** only for the specifically identified active Low Priest Chosen instance. The weapon's normally paid attacks can carry its independently authored fire/Vigor packets on hits. Its aspect is **Fire / Conflagration** (External); the *weapon-delivery profile* nevertheless qualifies as an inward/equipment Chosen Rite.

| Architecture check | Result |
|---|---|
| Qualifying host | **PASS** only for a **Prepared, active, actually wielded Reserved Weapon** with positive Committed VP and specifically Chosen instance |
| Same-Aspect Level-3 identity | **PASS** for a future **Fire / Conflagration** property only |
| Required host predicate example | Persistent weapon-carried combustion, one recorded weapon and legal successful hit events; does not qualify just because another Conjure Flame profile shares the technique name |
| Illustrative secondary behavior | **Directed Kindling**: controlled interaction with an already contacted combustible material through the enchanted weapon; source, material, physical fire, spread, fire damage, timing, and price all **NOT AUTHORED** |
| Prevent accidental escalation | No free extra attack, spontaneous Rider, guaranteed Ignite/Burning, unrestricted fire spread, additional target, per-hit full spell, or automatic area effect |
| Cost/accounting | A prospective Exaltation would use separately authored Spent VP, **not another discount** on the already-locked Chosen 3 Committed VP. A second weapon at L4 is non-Chosen, normally **4 Committed**, and cannot host Exaltation |
| Host loss | **Sheathing, stowing, dropping, disarming or otherwise ceasing to wield** ends the weapon channel at once; any pending Exaltation expires, and only the effective Committed VP returns |
| Verdict | **Framework suitable**; illustrative Fire effect remains **NON-EXECUTABLE** pending full authored profile and calibration |

**Negative cases:** A `Thrown Projectile` or `Ammunition Shot` Conjure Flame activation spends VP and is **not an ongoing Committed-VP Rite**. Holding an enchanted sword in a backpack cannot preserve the Reserve. If a Level-4 Priest maintains separate weapon A (Chosen) and weapon B (non-Chosen), only A may host an authored property; stowing A terminates its host but does not promote B.

## Why these two tests matter

These tests deliberately exercise **two different host capabilities** (body resistance vs wielder-maintained offensive carrier), **two different Aspect categories** (Internal vs External), **two different activation styles** (Stone Skin's own reactive cast vs Conjure Flame's ordinary on-turn weapon cast), and **different host termination**. Both should use the **same universal Exaltation activation/ledger framework** without sharing the same magical property.

**Validation result:** No universal-rule change or bespoke technique-specific Exaltation requirement was necessary to describe either host. **This is a structural paper audit, not end-to-end character certification or numeric combat validation.** Until actual Earth/Fire properties are independently authored, their Level-3 Low Priest builds remain **incomplete for Exaltation**.

## Life exception check: Venom Endurance

[Venom Endurance](../rules/07-veil-magic/venom-endurance-v0.md) has `Self` and `Single Target` profiles but its current modes cost **Spent VP only**. It is **not** a qualifying Chosen Devotion Rite or a separate Exaltation host at Level 3; its anti-toxin capabilities cannot be automatically borrowed by a maintained Life / Preservation Rite. A future property inspired by that technique must be **independently authored and priced**, with an actual compatible host and limited output.
