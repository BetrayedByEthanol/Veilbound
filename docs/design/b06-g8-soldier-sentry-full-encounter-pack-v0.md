# B06 G8 — Soldier/Sentry Full Encounter Pack v0 (bounded native terminal matrix)

> Source-native L2/L3 four-PC fixed-policy Soldier/Sentry terminal witnesses,
> NOT representative encounter difficulty, full playtest certification or CR.

## Scope and implementation

- [G8 source-native runner and replay attestor](../../scripts/b06_g8_soldier_sentry_full_pack_v0.py)
- [G8 regression tests](../../tests/test_b06_g8_soldier_sentry_full_pack_v0.py)
- [G5 Soldier/Sentry source melee](../../scripts/b06_soldier_sentry_g5_v0.py)
- [G7-H bounded Hunter matrix](b06-g7h-mixed-party-encounter-certification-v0.md)
- [Soldier source fixture](../../content/creatures/b06-ordinary-human-soldier.v0.json) and [Sentry source fixture](../../content/creatures/b06-firebound-sentry.v0.json)

The G5 adapter now has a narrowly validated **opt-in** for the original
source A/B Priest physical Sword/Mace profiles against exactly one named
genuine 1x1 Soldier or Sentry enemy. The default remains Hunter-only;
G6-B/Hunter callers, profile ownership, melee contact, AP, precommitted
defenses and G4 typed damage are unchanged. No generic player melee profile
or ranged Bow wound authority is introduced.

Every scene includes one genuine foe and A Vanguard, B Guardian, R Low Priest
Bow Vanguard and F High Scholar Fire at level 2 or 3. Initiative is
foe/A/B/R/F on an explicit 8x7 G1 grid. All actors take real G0 turns;
the authored R maintains a Chosen Self Guided Regeneration Rite during the
victory policy. A/B remain **physical-only Priest proxies**; the fixed
R policy does not claim Bow injury delivery against a non-Hunter target.

## Authored opponent and terminal matrix

| Enemy source | Party victory | Party defeat | Party withdrawal |
|---|---|---|---|
| Soldier B06-EN-02 | Paid sword opposition; A/B G5, F G3/G4 fire | Actual G1 cautious pursuit and 24-AP paid sword critical damage to every party member | Paid sword and four actual G1/G4.5/G5 border exits |
| Firebound Sentry cold | 30-AP Projection and 3 Committed VP before enhanced attacks | Source cold preparation, later real 20-AP enchanted sword damage | Cold preparation and later paid enhanced attack before exits |
| Firebound Sentry prepared | 3 VP already committed in source, real enchanted sword | Paid enchanted sword: physical HP plus direct Vigor packet | Real enchanted sword opposition before exits |

The three policies replay independently at **L2 and L3**. Explicit seeds
identify original source runs; attack faces, target priorities, response
declines and regeneration choices are *authored in advance*, not randomly
sampled. A 48-round ceiling remains **unresolved** unless the native
terminal conditions are actually met.

- **Victory:** Authentic A/B paid physical hits, R Chosen maintained Rite,
  F G2-lane-verified direct Thrown Flame with real spent VP and G4 Fire/Vigor,
  and at least one real enemy action or separately paid cold Sentry cast.
  A source G4 fatal foe transition and completed Round End are mandatory.
- **Defeat:** A/B/R/F hold voluntary actions, while the Soldier/Sentry
  follows actual paid G1 Cautious routes and uses genuinely funded attacks
  on successive live/Dying party members. Four distinct G4 fatal
  transitions and Round End are mandatory. Authored 20/20 high-critical
  faces demonstrate a **reachable extreme**, not normal challenge.
- **Withdrawal:** The foe genuinely attacks before all four PCs move
  Cautiously through source G1 to preauthored unique border cells and each
  obtains G4.5/G5 exit receipts. Cold Sentry cannot claim a Round-1
  enhanced attack after paying 30 AP for its Reserve. The foe survives.
  This proves **scene-local departure**, never global pursuit cessation.

## Verification and limits

The terminal attestor builds a fresh original source fixture and independently
replays the complete chosen policy. Only a whole-ledger and final-state
**exact equality** plus canonical SHA-256 passes. Rehashed changes to
G0 payment, G1 geometry, source digests, G3 VP reservations, G4 damage,
G4.5/G5 slot resolution, authored decisions or public terminal summaries
are rejected. This is a fixed policy consistency certificate, not
authorization to edit arbitrary player choices or a secret-key signature.

A passing three-terminal run reports
**bounded_three_terminal_matrix_certified=true**. It explicitly keeps
**complete_representative_party_pack_certified=false**,
**representative_encounter_calibration_accepted=false**,
**sampled_win_rate=null** and **hunter_cr=null**. Independent 12-Focus
certification remains 0/12 and all six strict MVP gates remain open.

Not in v0: general Soldier/Sentry AI, actual randomized player/GM policies,
real Bow HP damage against these foes, A/B Priest casting, protective
responses in this terminal matrix, mixed geometry and terrain,
long-term post-withdrawal safety, numeric difficulty and representative
human playtesting. The unchanged historical Phase 3 digest is
c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b.

## Verification commands

    python -m unittest discover -s tests -p test_b06_g8_soldier_sentry_full_pack_v0.py -v
    python -m unittest discover -s tests -v
    python -m scripts.b06_g8_soldier_sentry_full_pack_v0 --opponent soldier --level 3 --seed 0
    python -m scripts.b06_g8_soldier_sentry_full_pack_v0 --opponent sentry_cold --level 2 --seed 17
    python -m scripts.b06_g8_soldier_sentry_full_pack_v0 --opponent sentry_prepared --level 3 --seed 0
