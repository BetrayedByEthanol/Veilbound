# B06 G6-C — Mixed-Party Hunter Encounter Integration v0

> **Executable two-round integration witnesses, not encounter certification.**
> This milestone advances I3 from a one-versus-one Hunter exchange to
> full real Initiative passes with three and four distinct, source-backed
> L2/L3 player characters. It does **not** automatically award victory,
> claim a resolved Hunter challenge rating, or resolve currently
> unsupported landed Bow arrows / Protective Intervene.

## Source and readiness boundary

The existing G0–G6B code supports a bounded mixed party without replacing
the original encounter rules or inventing additional combat mechanics.

| Element | Actual source | G6-C action |
|---|---|---|
| Hunter (B06-EN-03) | [Hunter creature fixture](../../content/creatures/b06-hunter-of-the-woods.v0.json) / [G6-A](../../scripts/b06_hunter_g6a_v0.py) | Native Bite miss followed by real puncturing Bite and venom; next-round Regeneration Step |
| A — Restorative Vanguard | [Low Priest A physical proxy](../../scripts/b06_hunter_party_exchanges_v0.py) / [G6-B](../../scripts/b06_player_offense_g6b_v0.py) | Sword +7; separately paid G0 turns, G5 attack rolls and G4+G4.5 hit evidence; own next-turn recovery |
| B — Preservation Guardian | Same A/B physical source and G6-B | Mace +6; native Attack Sequence, wound/Armor system |
| R — Bow Vanguard | [B05 L1–3 sheet](../../scripts/b05_bow_vanguard_l1_l3_v0.py) / [G2](../../scripts/b06_ranged_v0.py) | One **actual launched, explicitly missed arrow per round**, consuming sourced ammunition and Turn AP |
| F — Fire Scholar (four-PC only) | [B05 L1–3 Fire](../../scripts/b05_high_scholar_fire_l1_l3_v0.py) / [G3](../../scripts/b06_spells_v0.py) | Two valid Tier-1 **Thrown Flame direct hits** from clear 2-square line, paid with real projection AP and Spent VP; G4 Fire HP/Vigor/wound resolution |

The Hunter's head starts at **(3,2)** and rear at **(4,2)**, facing west.
Priest A stands in the **sole head-forward threatened square (2,2)**;
Priest B stands to the side at (3,3), able to attack but **not
automatically eligible to redirect the Hunter's Bite**. R at (1,4)
fires diagonally to the explicit Hunter **head cell** without a screen.
In four-PC packs F at (1,0) casts along a different clear diagonal.
No creature is placed on a physically overlapping footprint.

The explicit authored Initiative scores are Hunter 30, A 24, B 20,
R 16, F 12. These are scenario roll *outcomes*, not permanent source
bonuses, surprise or generic monster AI. All turns in the active party's
Initiative order resolve and end; the real G0 Round End occurs before
the next Round Begin.

## Executable I3-G6C fixture matrix

[Executor](../../scripts/b06_hunter_mixed_party_g6c_v0.py):
`mixed_scene(size=3|4, level=2|3, seed=...)` and
`run_i3_mixed(size=3|4, level=2|3, seed=...)`.

| Fixture | True party roster | Observed window | Planned native outcomes |
|---|---|---|---|
| Three-PC L2 | A, B, R | Two complete rounds | Hunter still conscious |
| Three-PC L3 | A, B, R | Two complete rounds | Hunter still conscious |
| Four-PC L2 | A, B, R, F | Two complete rounds | Hunter crosses to Dying under real G4 Fire wound |
| Four-PC L3 | A, B, R, F | Two complete rounds | Hunter crosses to Dying under real G4 Fire wound |

**Round 1:** Hunter declares one Bite versus A's independently committed
Guard; the source natural 1 misses without fabricated damage. A lands
one 4-HP-after-Armor Sword wound-free hit, B pays a genuine action but
misses naturally, R launches one actual natural-1 arrow, and in four-PC
cases F casts one paid Tier-1 direct Thrown Flame. The last F attack
takes 2 HP and its independently sourced direct Vigor packet.

**Round 2:** Hunter performs one genuine natural regeneration (4 HP,
4 Vigor where funded) and delivers a Bite to A's preselected Take Hit.
The piercing hit also uses one actual TX-NE venom resistance die,
one-instance gate and independent delayed toxin clock. A allocates
2 HP at its own subsequent Regeneration Step, not at the bite boundary.
A and B pay fresh physical attacks against the Hunter; R fires one
more genuinely missed arrow. Four-PC F casts a second valid Flame,
which crosses the Hunter to Dying and consumes an **independently
declared wound-location d20**. A 0-HP crossing is **not death** and
does not itself prove a Hunter kill or a safe full-party victory.

All attack damage/cost/defense receipts derive from the native ledger:
G0 payments, G5 profiles and outcomes, G4 typed damage, G4.4 venom,
G4.5 melee hit provenance, G2 launched ammunition, G3 projection
and VP transitions. A G2 projectile result with a pending hit is
rejected by this executor rather than silently converted to damage.
No extra automatic opportunity attacks are assumed merely because
another ally could threaten movement.

## Readiness gaps and certification boundary

These **are four genuine mixed-party integration windows**, not four
fully certified encounters with scripted terminal outcomes.
In particular, all the following remain separate work:

1. **Ranged Bow hit-to-G4 bridge:** G2 supplies explicit geometry,
   defender resources, actual launches and hit-or-miss delivery. It
   still labels positive Bow contact / natural-20 confirmation as
   `*_pending_G5`. A landed arrow's physical damage, severity and
   wound provenance are **not** attested by the current G6-C path.
2. **Protective and active reactions:** full Reactive/Prepared Intervene
   (Guard versus Body Take Hit, actual nested windows) and chosen
   counterattacks remain distinct from G6-B's narrowly supported
   **movement Opportunity** executor. Nearby allies are not
   automatically protecting each other.
3. **Full encounter terminal/CR:** actual all-party withdrawal,
   confirmed kill, or other independently authorized win/loss
   requires its own source-attested terminal route. The two-round
   observations end as `not_attested_full_encounter`, with
   `complete_party_pack_certified=false` and `hunter_cr=null`.
4. **Ambush, mixed cover/screen, additional monster actions and
   wider action-choice matrices** are not inferred from these
   clear-lane, fixed-choice evidence fixtures.

This stage does not change the historical frozen **4096-trial**
Phase 3 audit, its original hash, or the previous I3 solo withdrawal
witness. A/B remain explicitly **physical proxies**, not fully
certified Priest repertoires. The G6-C report returns the native
ledger, true roster/source hashes, per-turn results, real Round Ends,
remaining restrictions and original G4.5/G5 reports.

## Verification

```sh
python -m unittest discover -s tests -p 'test_b06_hunter_mixed_party_g6c_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.validate_b06_footprints
```

The full existing GitHub Actions pipeline also runs the frozen Hunter
Phase 3 census and its independent audit hash comparison.
