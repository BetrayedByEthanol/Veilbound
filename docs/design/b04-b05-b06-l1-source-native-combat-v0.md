# B04/B05/B06 — Level 1 Source-Native Combat Coverage v0

> **An L1 hostile-combat GM reference with real G0–G5 actions, exact source fingerprints, and bounded native terminals.** Not proof of fair L1 encounter difficulty, a full twelve-Focus character certificate, independently witnessed gameplay, or a numerical challenge rating. The original B06 G0–G8 engine and all NPC/PC source definitions are unchanged.

## Why this slice is necessary

The [merged #190 pilot adventure](b04-b05-b06-b07-integrated-mvp-pilot-adventure-v0.md) locates a possible Soldier road-gate conflict in its level-one chapter, but the [G8 Soldier/Sentry GM pack](b06-representative-soldier-sentry-hunter-gm-encounter-packs-v0.md) **intentionally accepts only L2/L3 benchmark A/B/R/F parties**. Its L2 actors, HP/VP snapshots and fixed histories may **not** be silently presented as L1 play. Earlier [individual L1 Scholar physical](../../scripts/b05_scholar_native_physical_offense_v0.py) and [L1 Scholar Flame](../../scripts/b05_scholar_three_focus_native_offense_v0.py) demonstrations were real but bounded two-round witnesses, not complete group conflict outcomes.

This integration builds **three authentic L1 source characters** against the **unchanged** source Ordinary Human Soldier, `B06-EN-02`, whose authored benchmark is **level 3 equivalent**. This is a potentially difficult/imbalanced opponent, **not** a secretly created L1 Soldier. The encounter represents one *legal exposure*, not a recommendation that a typical L1 party should fight it.

## Source party and legal actions

| Actor | Source | Position | Actual delivery |
|---|---|---|---|
| High Fire Scholar `F` | L1 selected High Scholar source sheet; source-held equipment/VP | (1,0) | One G0/G3 paid T1 Conjure Flame through G4, no free ranged Bow |
| Medium Earth/Life Scholar `S` | L1 selected Medium Inward Scholar source sheet | (2,2) | G2-wielded ordinary Sword Cut, actual G1 contact, G0 paid G5/G4 hit |
| Low Earth/Life Scholar `T` | L1 selected Low Embodiment Scholar source sheet | (3,3) | Its own G2-wielded ordinary Sword Cut; no fabricated L1 prepared Flame |
| Ordinary Human Soldier | Original `B06-EN-02`, **L3-equivalent** start | (3,2) | Original G5 Sword `B06-AT-03`, full source HP/Vigor, normal reaction windows |

The lane is an 8×7 open grid. Original G1 movement, G0 turn/Regeneration Step, G2 source equipment, G3 spell, G4 damage/wounds/Dying and G5 attack/exit paths are used directly. The fixture declares deterministic dice and declines optional responses; no universal sword authorization, enemy re-leveling, scripted direct HP mutation, automatic healing or fictional MP/VP payment is added.

## Two discrete source terminal branches

**Favorable offense**: Soldier pays for a genuine natural-1 miss each active turn; the actual L1 High Scholar makes one Tier-1 cast and the two selected source Scholars make genuine paid sword attacks. Enemy death must be an actual G4 HP crossing recorded in a completed G0 round. The GM must **not** interpret the deliberately favorable Soldier policy as typical difficulty, or force the players to attack rather than try other options.

**Opposed withdrawal**: Soldier instead makes a real paid sword attack; the three L1 characters use individually authored cautious G1 routes to three real border squares and G5 terminal exit declarations. A scene-local withdrawal leaves the Soldier alive and does **not** guarantee no pursuit, free rest, an alarm-free village, or recovery. This branch requires genuine source geometry and legal current-character movement.

Each native report includes original source IDs/digests, L1 actor levels, the Soldier's unmodified source benchmark, G0/G1/G3/G4/G5 event evidence, complete `_snapshot` HP/Vigor/wounds/ammo/position/exit status, separate Spent VP totals, bounded terminal outcome and a ledger SHA-256. `attest_policy` independently replays the declared policy and rejects tampering, including a recomputed attacker/source status field. Unresolved round ceilings remain censored rather than renamed wins. Other actual encounters, tactics, protections, injuries, terrain, characters and alternative NPC decisions must be separately resolved.

## Running the source reference

```bash
python -m scripts.b04_b05_b06_l1_source_native_combat_v0 --policy favorable_offense
python -m scripts.b04_b05_b06_l1_source_native_combat_v0 --policy opposed_withdrawal
python -m scripts.b04_b05_b06_l1_source_native_combat_v0 > build/b04-b05-b06-l1-source-native-combat-v0.json
python -m unittest discover -s tests -p 'test_b04_b05_b06_l1_source_native_combat_v0.py' -v
```

The independent-audit CI workflow runs focused source tests, generates an authenticated deterministic matrix, and runs the repository-wide unit tests at the exact PR head.

## Acceptance boundary and follow-on

This closes **the specific lack of any L1 hostile group-combat source-native reference** in the integrated gate adventure. It does **not** prove any of the other nine Focuses, certify even the three participating Scholar Focuses, complete a Low Priest magical sheet, provide a general L1 enemy suite, validate representative four-player L1 encounters, or close B04/B05/B06/any MVP gate.

For actual L1 tabletop play, the GM still needs a complete original sheet for each participant, a source-grounded threat/start/map, real choices/opposition, legal outcome/aftermath and independently reviewed [multi-cohort pilot evidence](b04-b07-pilot-evidence-flexibility-multi-cohort-v0.md). If the original Soldier's L3-equivalent danger is unsuitable for the party, use the authored avoidance/withdrawal route or separately source-authored appropriate opposition; **do not down-level the existing JSON**.

Strict unchanged status: **12/12 structural builds, 0/12 independently fully certified, 0/6 exit gates, B01–B03 only (3/7) definition-closed, G0–G8 delivered in bounded scope, Hunter CR unrated**.
