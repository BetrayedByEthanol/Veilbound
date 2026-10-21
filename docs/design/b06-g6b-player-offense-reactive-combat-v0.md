# B06 G6-B — Player Offense and Reactive Combat Integration v0

> **Bounded, executable extension; not full-party certification.** G6-B adds
> the two existing audited Low Life Priest physical proxies (A and B) as
> real native player melee attackers against the Hunter, plus one genuine
> paid-response player Opportunity Attack when the Hunter moves out of reach.
> It does not invent additional character sheets, spell choices, monster AI,
> reactive protective movement or a final Hunter difficulty rating.

## Source and scope

- [A/B authored physical fixture](../../scripts/b06_hunter_party_exchanges_v0.py),
  with the existing [B05 Life Priest verification](b05-life-low-priest-l3-build-exaltation-verification-v0.md).
- [Weapon attacks, Guard, and physical contribution](../rules/05-combat/weapon-attack-and-guard-math.md),
  [weapons and armor](../rules/05-combat/weapons-and-armor.md),
  [G0 round/Reaction](../rules/05-combat/initiative-and-round-structure.md),
  [G1 opportunity timing](../rules/05-combat/movement-foundation.md).
- [G5 paid melee](../../scripts/b06_soldier_sentry_g5_v0.py),
  [G4 typed packets and wounds](../../scripts/b06_damage_v0.py),
  [G4.5 proof](../../scripts/b06_wound_continuation_v0.py),
  [G6-A Hunter](../../scripts/b06_hunter_g6a_v0.py).
- Executable [G6-B player adapter](../../scripts/b06_player_offense_g6b_v0.py),
  with [focused regression tests](../../tests/test_b06_player_offense_g6b_v0.py).

## Genuine on-turn A/B versus Hunter

`party_actor("A"/"B", L1–3, ...)` now carries one source-attested
`Source.attack_profiles` identity per proxy. This is **not** a general
new repertoire or permission to choose unsupported weapons:

| Existing proxy | Paid G0 profile | Attested attack bonus | Native G4 base | Pen | Damage mode |
|---|---|---:|---|---:|---|
| A — Restorative Vanguard | `B06-PC-A-SWORD` | Strength2 + Agility3 + Sword Training2 = **+7** | 3 + d6 + floor(Strength/2) = **4 + d6** | 2 | Cut |
| B — Preservation Guardian | `B06-PC-B-MACE` | Strength2 + Agility2 + Mace Training2 = **+6** | 4 + d6 + Strength = **6 + d6** | 3 | Crush |

Only actual `wielded` source gear is legal. Sword Cut is the bounded
selected damage mode (not an unvalidated retroactive Cut/Pierce switch).
`PlayerHunterCombat.declare()/resolve()` uses existing G5 and G0; all
same-target attacks are precommitted in an Attack Sequence and each
defense assignment (Hunter Dodge/Take Hit, no fictional natural Guard)
is paid before the first strike. G4 handles effective Hunter Armor3,
critical d4, HP, wound locations, Dying, and source provenance; G4.5
logs the actual paid G0 action. No separate side ledger or instant-kill
claim is accepted. Player targets other than the source Hunter remain
outside this executor.

## One genuine PC Opportunity during Hunter movement

`PlayerHunterCombat.step_with_opportunity(hunter, delta, pc, ...)` offers
exactly one selected A/B Sword/Mace **Opportunity** on one actual
`G1.step` and only when the source's genuine departure-cell threat
predicate is satisfied. It does not permit an attack on an unprovoking
pivot or a generic back-cell Hunter Opportunity. Inputs (including
damage/critical/wound dice and Hunter defense choice) are checked
**before** G0 can consume a Reaction; post-commit
`e.is_live_spontaneous(trigger,response)` and the source
`spontaneous_committed` event bind the callback to the real response.

- G0 charges one once-per-round **Reaction** to activate Opportunity
  Response unless previously activated. Its native Physical Tempo limit
  caps the total Opportunities; G6-B spends **zero Turn AP**, not an
  invented second Physical Action.
- The intended moving Hunter chooses its real Take Hit or Dodge before
  rolling. There is **no natural Hunter Guard**. Natural 1 misses, natural
  20 confirms once, and ties to Dodge miss.
- One actually successful attack causes real G4 weapon damage and wound
  evidence *before* G1 finishes the original step. A Dying/dead Hunter
  loses the step; its attempted departure does not teleport or spend
  ordinary MP.
- Responses cannot be double-consumed outside the live G0 callback.
  Caller-supplied payloads do not stand in for a historical Reaction,
  attack sequence or cached hit.
- No Movement Interception or nested chosen Opportunity routes are
  accepted by the bounded helper; unsupported choices raise
  `UnresolvedDecision`, not a guessed outcome.

## Explicit G6-B limitations and next slices

The milestone is a **player-offense and reactive-Opportunity foundation**,
not all possible defensive reactions. Still unresolved: full
`Reactive Intervene` and `Prepared Intervene` with Body Take Hit versus
Shield Guard, chosen active counterattacks during G6-A Pounce/Standing,
G2 Bow projectile **damage and critical/wound post-resolution**, PC
cast-offense under G3, arbitrary target redirection, feats/maneuvers,
and mixed-party 3–4-PC complete I3 packs. The existing G2 Bow
delivery-only result is **not** silently promoted to an HP hit.

The original Phase 3 4,096 frozen one-round census and hash remain
untouched; new player-side evidence must be kept distinct from signed
legacy stops. A/B source sheets retain their physical-proxy status;
no Archetype×Focus or Hunter CR is certified by these tests.

## Validation

```sh
python -m unittest discover -s tests -p 'test_b06_player_offense_g6b_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.validate_b06_footprints
python -m scripts.b06_hunter_phase3_report_v0 --json-out build/b06-phase3-census.json --markdown-out build/b06-phase3-census.md
```
