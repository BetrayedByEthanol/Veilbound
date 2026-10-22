# B06 G7-A — Native End-to-End Policy and Terminal Census Infrastructure v0

> **Pilot infrastructure and censored combat evidence. NOT a measured win
> probability, universal encounter AI, complete B06 party certificate or
> numerical Hunter Challenge Rating.** This executor actually plays three
> source-backed G0 rounds or stops at a source-detected mechanical
> boundary. It does not manufacture victory from HP zero, two-round
> survivors or an unsupported Flame critical.

## Scope and source authority

[`scripts/b06_g7a_native_terminal_census_v0.py`](../../scripts/b06_g7a_native_terminal_census_v0.py)
runs the **four** previously classified `fixed_native_window`
[G7 readiness cells](b06-g7-encounter-calibration-readiness-scenario-matrix-v0.md):

| Cell family | Actor sources | Native opening | Duration |
|---|---|---|---|
| L2-P3, L3-P3 | A Low Life Sword, B Low Life Guardian, R Low Life Bow | G6-C warned clear, A in Hunter's genuine head-forward contact | Up to 3 true rounds |
| L2-P4, L3-P4 | Same three plus F High Scholar Fire | Identical native contact and lane | Up to 3 true rounds |

Each encounter creates real G0 actors and source digest snapshots, G1
1×2 Hunter anatomy, G2 clear Bow, G3 real Tier-1 Flame, G4 physical
HP/wounds/Dying and delayed Hunter venom, G5 precommitted
physical Attack Sequences, and G6-D Bow-to-G4 and Hunter death
attestation. **Only one source-derived action per eligible active actor
per turn is currently selected by this trial policy**. A Dying/dead
actor receives its actual G0 Regeneration Step and completed turn,
not a fabricated attack or phantom reanimation.

The Hunter targets **A Vanguard** with one paid source Bite when still
conscious and A is not dead. A and B each choose one true sword/mace
attack on the Hunter while able. R launches one G2 Bow shot
using the authenticated G6-D hit/miss/damage/critical pipeline.
F may cast one real G3 Conjure Flame against the Hunter's head
cell. No money, Armor, stats, AP or spell grants have been changed.

### Keyed decision and dice policy

- SHA-256 keys contain **policy version + seed + real round + actor +
  action + die purpose + die index**. Exact same actor/action/round
  draw is paired across L2/L3 and P3/P4: the key intentionally
  excludes party size and level. A branch that needs another critical
  or wound die does not shift any later result.
- Before an attack is rolled, the policy commits **Guard versus Dodge**
  for A when legally available; the Hunter defends sword/mace using
  **Dodge versus Take Hit** and pays any real Dodge Pressure; an
  incapacitated Hunter only receives Take Hit. Natural HP recovery
  is independently chosen each turn and charged through native
  Vigor/throughput. Dying survival cancellation likewise requires
  actual throughput and Vigor. All options are modest, preauthored
  *trial policies*, not learned optimal player or animal tactics.
- Every ordinary physical attack has its one natural attack d20,
  optional natural-20 confirmation, exactly sourced critical d4 dice,
  source damage d6, toxin resistance d20 if puncture may occur,
  and predeclared wound-location d20. R Bow uses its **d4** and
  G2 static **Ranged** Take Hit. No extra roll or reroll is granted
  on a disappointing result.
- **G3 F Flame natural 20 is not generalized into free damage.** The
  original G3 executor marks it `critical_confirmation_pending_G5`.
  G7-A records the authentic paid source event and classifies the
  trial as `unresolved_mechanical_branch`, never a fake G4
  hit, victory or ordinary miss.

### Event-derived state and four non-interchangeable outcomes

| Outcome label | Native evidence / interpretation |
|---|---|
| `hunter_defeat_attested` | **Actual source G4 lethal packet** with source-authenticated G5 melee or G6-D Bow plus **completed genuine G0 Round End** and G6-D once-only Hunter terminal |
| `party_defeat_observed` | All participating PC source actors actually dead after real G0 turns; **observational only**, not a general encounter/escape/party-certificate API |
| `legal_window_cutoff` | Three genuine rounds finished, no full terminal; Hunter may be Dying and source resources consumed, **not** a win/draw |
| `unresolved_mechanical_branch` | Source executor reports an unsupported legal choice or critical/transfer, or a death without G6-D terminal authority; recorded with actor, round and exact reason |

The censused terminal classes are **not binary survival probabilities**.
The last two are explicit censored/unknown outcomes. Do not calculate
a Hunter defeat rate over the *resolved* subset while excluding
unresolved or fixed cutoffs.

Every seed's report contains source fingerprints, initial/final HP,
Vigor, VP, ammunition, wounds, death/Dying state, real G0 turn and
Round-End counts, G5 melee and G2/Bow/Flame/G4 event counts,
native once-only terminal details if present, and a SHA-256 of the
**entire actual G0 ledger**. The `include_ledger=True` API returns
that full ledger to independently inspect causality. CLI
`--full-trials` includes full per-seed summaries; default CLI
outputs counts, per-seed ledger fingerprints and unresolved reasons
without overloading reports with full event logs.

### Deterministic pilot and coverage accounting

`census(seeds=8,start_seed=0,max_rounds=3)` executes the **same seed
range across all four** scenarios. The bounded test harness allows
**1–128** explicitly requested seeds per cell and rejects zero,
booleans, invalid round budgets and unsupported party configurations.
A planned full 128-seed pilot across four cells would represent
**512 native, at-most-three-round observations**, *not*
512 completed encounters. The outcome counts sum to the exact
requested per-cell denominator, and every explicit unresolved reason
has its own tally. No result is silently dropped, re-rolled or
moved into the Hunter-death class.

Even a finished trial's status is not an approved mixed-role
difficulty estimate. **Numeric creature CR, CI95, win/defeat
probabilities and party-pack certification remain `null`/false**.
The current finite, simplified combat policy is not representative
of retreat, spell repertoire use, environmental variety, preparation,
Pounce, long-term toxin and postcombat recovery.

## Hard exclusions / next gate

These are deliberately **not** part of the four accepted scenarios:

1. Warned versus **forest ambush** and **B Guardian head-forward**.
   Both need genuine newly authored geometry, true Hunter Pounce
   and target-defense legality.
2. Integrated Reactive Shield / Prepared Body. These independently
   verified G6-D *components* are not generalized to any trial
   result here. The other 44 of G7's 48 readiness rows stay at
   their actual prior authority level.
3. Natural-20 **Scholar Flame** final damage/critical confirmation,
   Cover/living screens and non-Bow ranged protection, multi-arrow
   sequences, alternative melee targets with verified positioning,
   lawful retreat and party-defeat scene exits.
4. Full Dying wound repair selection, optional Priest Rite /
   Exaltation, High Scholar maintained effects/Basic Heal, post-escape
   T+10/30/60/120-minute delayed toxin and six-hour recovery,
   party decision quality and open-ended route/GM choices.

An unsupported path must be **reported**, not filled by a new
mechanical rule, silent favorable die or optimistic victory.
The frozen [Phase 3 first-stop census](b06-hunter-phase3-census-results-v0.md)
is still a separate **4,096-window** historical experiment with
unchanged canonical SHA-256
`c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`.
G7-A does not reopen its 770 unresolved contact stops or 22
wound stops and never replaces its one-round results.

## Verification and CLI

```sh
python -m scripts.b06_g7a_native_terminal_census_v0 --seeds 8
python -m scripts.b06_g7a_native_terminal_census_v0 --seeds 4 --full-trials
python -m unittest discover -s tests -p 'test_b06_g7a_native_terminal_census_v0.py' -v
python -m unittest discover -s tests -v
```

The native tests check ledger/round truth, stable paired draws, all
four source rosters, full four-category denominator accounting,
bounded seeds/rounds, no fabricated CR/win probability, original
ammo debit and G6-D death provenance. They do **not** certify all
threat policies, narrative outcomes or real tabletop balance.

## Proposed next implementation

**G7-B — Complete source-authorized terminal alternatives and
tactical policy coverage v0**, prioritized as follows:
finalize and source-bind G3 natural-20 Flame; independent party
withdrawal/escape or defensible party-wipe terminal; connect
actual G6-D protection into the mixed-party encounter loop;
expand real Hunter Pounce/ambush and alternative front positions;
then run the preregistered 128-seed pilot with recorded censored
denominators. Only after representative genuinely completed
comparisons should we consider numerical Hunter difficulty/CR.
