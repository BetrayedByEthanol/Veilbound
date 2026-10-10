# Defensive Responses and Criticals

> Canonical current defensive-response and critical-confirmation rules. Base Guard Defense and weapon Guard pairings are defined in [Weapon Attack, Guard, and Physical Contribution](weapon-attack-and-guard-math.md).

## Declaring defense

For each enemy's declared **Attack Sequence**, the defender assigns one of three responses to each incoming attack **before that sequence's rolls resolve**. The sequence includes all ordinary on-turn attacks committed to that target, including granted bonus attacks such as an offensive dual-wield off-hand Attack. Before defenses are assigned, the attacker must commit the attacks **and the weapon/profile plus other attack-specific choices for each attack**; see [Initiative and Round/Turn Procedure](initiative-and-round-structure.md#attack-sequence):

1. **Take Hit**
2. **Dodge**
3. **Guard**

For a **standalone attack** that occurs outside an Attack Sequence—such as an attack made by a Reaction, Interception, Opportunity Attack, Full Action, or explicit follow-up—the defender assigns **Take Hit, Dodge, or Guard after that attack is declared and before its attack roll resolves**.

Standalone attacks use the **same round defense resources** as attacks inside Attack Sequences. Guard spends normal Guard capacity, and choosing Dodge uses the defender's current Dodge Pressure and increments it normally. There is no separate out-of-turn defense pool.

Repeated incoming attacks do not automatically reduce defense. Only repeated chosen Dodges create Dodge Pressure.

## Take Hit

Against melee, Take Hit means the attack lands unless the attacker rolls a natural 1.

Ranged attacks use the separate ranged-defense rules because an undefended projectile is not automatically assumed to strike its target.

## Dodge

```
Dodge Defense = 10 + Agility + Awareness - Dodge Pressure
```

Dodge Pressure is **-2 for each previous Dodge chosen in the same round**:

| Dodge this round | Dodge Pressure |
|---:|---:|
| 1st | 0 |
| 2nd | -2 |
| 3rd | -4 |
| 4th | -6 |
| Each later Dodge | another -2 |

Only choosing Dodge increments Dodge Pressure. Taking Hit or using Guard does not.

Dodge Pressure resets to 0 at **Round Begin** under [Initiative and Round/Turn Procedure](initiative-and-round-structure.md).

Dodge has no Training bonus and no minimum floor.

When armor limits Agility for Dodge, use the armor-cap rules in [weapons-and-armor.md](weapons-and-armor.md).

Being **Prone** does not inherently remove Dodge or apply a second blanket Dodge penalty. A Prone Dodge is legal only when the required rolling, twisting, or other repositioning is physically possible; see [Special Movement, Terrain, and Prone](special-movement-terrain-and-prone.md#dodge-while-prone).

## Guard

Guard unifies parrying and blocking into one defensive response.

Base Guard capacity equals the character's derived **Physical Tempo** and may be modified by equipment. Normal Guard capacity refreshes at **Round Begin** under [Initiative and Round/Turn Procedure](initiative-and-round-structure.md).

Base Guard Defense is:

```text
10 + Guard Ability A + Guard Ability B + relevant Training + Guard modifiers
```

Use the Guard pairings in [Weapon Attack, Guard, and Physical Contribution](weapon-attack-and-guard-math.md).

Guard is binary:

- attack fails to beat Guard Defense → the attack is stopped;
- attack beats Guard Defense → the attack hits normally and armor handles the damage.

There is no partial or half-damage Guard state.

For a projectile-delivered area effect, "stopped" means the Guard instrument physically intercepts the projectile. The projectile therefore impacts at the defender's position by default and any carried area resolves from that impact point. Guarding the projectile does not automatically cancel the carried area. See [Manifestation Resolution](../07-veil-magic/manifestation-resolution.md#successful-guard-against-an-area-projectile).

Ordinary dual wielding does not stack Guard Defense bonuses. Use the best applicable Guard setup.

Being **Prone** does not inherently remove Guard or reduce Guard Defense. The chosen Guard instrument must still be physically usable from the current posture; see [Special Movement, Terrain, and Prone](special-movement-terrain-and-prone.md#guard-while-prone).

Defensive off-hand weapons and shields may improve Guard. Equipment can grant **at most +1 additional Guard capacity per round** from the defensive off-hand/shield framework.

Riposte is a possible follow-up to a successful Guard where the relevant setup permits it. It is not a fourth defensive response.

Intercept uses Guard to protect another character rather than creating a separate defensive subsystem.

## Guard instrument lost after defense assignment

A defender can lose its declared Guard instrument between assigning defenses and resolving an attack, for example through a legal [Disarm](disarm-v0.md) Interception. Handle this at **the attack's normal response/resolution time**; do not reopen the Attack Sequence or let the defender reassign already committed defenses after seeing attack results.

- If a **different Guard-capable instrument** is still ready, physically usable, and legal against that attack, the committed **Guard** may use that instrument. The defense remains Guard; use its current legal Guard Defense.
- If **no legal Guard instrument** remains, the already-assigned Guard falls back to **Dodge**, provided the defender is physically capable of Dodging at that moment. Determine Dodge Defense and advance Dodge Pressure exactly as for a Dodge actually chosen then.
- If neither Guard nor Dodge is legal, the fallback is **Take Hit**, using the normal melee or ranged Take Hit procedure as appropriate.
- Guard capacity previously committed to the assigned Guard **remains spent** even when the instrument is lost. It is not spent again on a replacement legal Guard. The switch to Dodge does not commit another Guard use, but it does incur the ordinary Dodge Pressure. No earlier defense in the Attack Sequence is rerolled or reassigned.

These fallbacks apply only when the assigned defense has become **physically illegal** before its attack resolves; a defender cannot switch merely because a Guard roll would be unfavorable. They also apply to an assigned Guard against a standalone attack if its instrument becomes illegal during nested responses.

Losing the Guard instrument does **not** itself spend the Reaction or erase Opportunity Capacity; the defender's ability to make a particular Opportunity Attack depends separately on having a legal melee method and current Reach.

## Natural 1

A natural 1 on an attack is an **automatic miss**.

It has no inherent fumble or universal critical-failure effect.

## Natural 20 and confirmation

A natural 20 creates a critical opportunity.

### Against Dodge or Guard

1. Roll a confirmation attack against the same defense assigned to that attack.
2. Failed confirmation → **Strong Hit**.
3. Successful confirmation → **Critical Hit**.
4. Confirmation is also a natural 20 → **Devastating Critical**.

### Against Take Hit

- The initial natural 20 is automatically a **Critical Hit**.
- Roll once more only to determine whether another natural 20 upgrades it to a **Devastating Critical**.

There is no separate Critical Defense statistic.

Guard does not cancel criticals by special rule; a stronger defense simply makes confirmation harder.

The exact extra damage granted by Strong Hit and Critical Hit remains a calibration item and is not defined here.
