# Elemental HP Damage and Resistance v0

> **Proposed executable v0 baseline; numerical resistance sources remain individually authored.** This page supplies the missing typed-damage resolution for Conjure Flame and future expressly elemental effects. It does **not** retroactively retype every physical hazard, weapon or environmental impact. See [Technique Structure v0](technique-structure-v0.md#7-damage-resource-damage-type-and-separate-properties), [Weapons and Armor](../05-combat/weapons-and-armor.md) and [Strong/Critical damage](../05-combat/defensive-responses-and-criticals.md#strong-hit-critical-hit-and-devastating-critical-damage--v0-playtest-baseline).

## Distinguish resource, type and delivery

An effect packet independently specifies:

- **Resource:** HP, Vigor, or another explicitly defined consequence.
- **Type:** Fire, Electrical, Acid, Slashing, etc., where applicable.
- **Delivery/trigger:** a successful ordinary hit, an authored environmental hazard, a direct Veil contest, or another defined event.

**Fire is a damage type, not an additional resource.** An authored **Fire HP packet** reduces HP; a separate **Vigor-burning packet** reduces Vigor. They are not one combined damage pool.

## Elemental HP resolution

When an effect explicitly labels a damage packet **elemental HP damage** (Conjure Flame's Fire HP damage is such a packet), resolve the packet as:

```
Elemental HP damage taken = max(0, raw elemental HP damage - applicable typed resistance)
```

**Fire Resistance N** reduces each eligible **Fire HP packet** by N. A source stating **Fire immunity** reduces eligible Fire HP damage to **0**, regardless of amount. If the target has no authored applicable Fire Resistance, use **0**. Do not invent resistance from the name of an Aspect, ancestry, worn equipment or a descriptive fire-resistant appearance.

An elemental HP packet of this kind is **not reduced by ordinary physical Armor or by the carrier weapon's Penetration**. A physical sword/arrow still resolves its own physical HP packet with normal Armor/Penetration; the Fire packet resolves **once** against Fire Resistance. Do **not** reduce one packet with Armor, then Fire Resistance, or subtract Armor a second time from the entire mixed-type attack. A future **explicit hybrid** effect must supply its own mitigation instructions.

Other named elemental types (such as Electrical or Acid) may reuse this structure **only when the technique/hazard authors the corresponding elemental HP packet and resistance**; this rule alone does not create spells, new elemental defenses, conditions or environmental damage.

## Separate Vigor property and hit success

- **Vigor burn is independent of Fire-type HP damage.** Fire Resistance/immunity does **not** automatically reduce the Vigor packet; an expressly authored Vigor defense or dual-purpose protection may do so.
- If the incoming **delivery is successfully blocked, misses or otherwise fails to trigger its on-hit effects**, neither hit-triggered Fire nor hit-triggered Vigor applies.
- If a delivered **hit succeeds**, the Vigor packet may still apply even if physical Armor reduces a weapon/arrow's HP damage to 0 **or** Fire Resistance negates the Fire HP packet, unless the technique specifically requires HP to be lost.
- Apply each source's applicable mitigation **once per eligible packet**, not once for every descriptive subeffect. No unbounded conversion of Fire to Vigor or vice versa is implied.

## Criticals, wounds, and no double-counting

The existing **Strong/Critical/Devastating** procedure awards any bonus dice **once to the attack's single primary direct-hit HP damage packet**. On a weapon/arrow attack with a Fire enhancement, the native **physical** packet is primary; no second bonus is added to the Fire or Vigor enhancement. On a manifested thrown flame whose only HP packet is Fire, that Fire packet is the primary direct-hit HP packet and can receive the usual bonus dice **once**, before Fire Resistance, if the attack actually qualifies under the existing natural-20 confirmation procedure. Do not award HP critical dice to Vigor packets.

HP dropping from positive to nonpositive and any qualifying Devastating wound still use the existing [single-event wound procedure](../06-vigor-wounds-death/dying-and-wounds.md#when-wounds-occur). Multiple packets from the **same hit** are one hit/event for wound resolution; calculate the resulting HP loss and apply existing rules, not one wound per packet.

## Worked mixed-type example

An enchanted sword scores a legal hit and rolls **7 Slashing HP**, carries **2 Fire HP**, and applies **3 Vigor burn**. It has **Penetration 2**. The target has **Armor 5**, **Fire Resistance 2**, and no Vigor protection.

- Slashing: Effective Armor = max(5 − 2, 0) = **3**; physical damage taken = max(7 − 3, 0) = **4 HP**.
- Fire: max(2 − 2, 0) = **0 HP**; do not subtract Armor again.
- Vigor: **3 Vigor** lost from its separate packet.

If Fire Resistance were absent, the same hit would deal **4 Slashing HP + 2 Fire HP + 3 Vigor**.

## Scope and watchlist

This v0 supplies deterministic mitigation to **explicitly tagged elemental HP packets**. It does not define how environmental burning spreads, ignite duration, fire-damage-over-time, resistances granted by specific Fire/Water/Lightning techniques, elemental resistances on NPC sheets, partial type conversion, stacking of multiple independent resistance sources, or generic elemental damage from ordinary terrain hazards. Author those separately when needed; do not silently import other games' resistance rules.
