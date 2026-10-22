# B06 G7-E — Forest Approach, Pounce and Extended Recovery v0

> **Bounded executable integration, not universal surprise or a Hunter CR.** G7-E
> adds a source-authored forest run-up, compares one genuine Hunter Pounce
> with a genuine ordinary approach + Bite on paired source dice, executes
> real A/B/R[/F] Initiative turns, then transitions *only after a finished
> round* to the existing persistent world clock for venom and earned
> six-hour recovery. Ending this **observation window** is not a fictionally
> certified end to the encounter, withdrawal, complete party pack or death.

## Forest geometry and the surprise boundary

The canonical [Initiative rules](../rules/05-combat/initiative-and-round-structure.md)
state explicitly that there is **no universal surprise/unaware action
package**. G7-E therefore calls its opening
`forest_ambush_geometry_only`: the Hunter is positioned for an
authored physical approach, but every actor retains its genuine Initiative,
defense, awareness and ordinary Turn AP. There is no phantom surprise
round, bonus Bite, flat-footed defense, unseen-target advantage,
stealth contest, environmental Cover modifier or free Interception.

Four actual mixed-party scenes (L2/L3 × 3/4 PCs) share fixed source
characters, existing Initiative scores and a bounded grid. Initial
indexed Hunter body is **head (2,2), rear (1,2)**, facing east,
with **source-A vanguard (6,2)**, **source-B guardian (5,3)**,
**source-R archer (2,4)** and optional **source-F scholar (3,0)**.
The 1×2 Hunter must translate exactly **three whole-body legal east
steps** to **head (5,2), rear (4,2)**, paying **6 normal MP**.
Only then is A at the Hunter's genuine head-forward **(6,2)**
contact square. The other PCs retain native equipment, statuses and
G2 projectile/Flame lanes, rather than fictional replacement builds.

## Two paired source-native approach policies

All eight cohorts are the four L2/L3 × P3/P4 scenes paired across:

| Policy | Native resolution |
|---|---|
| `ordinary_approach` | Three real 1×2 whole-footprint G1 movement steps at normal MP, followed by **one** native paid G5 **B06-AT-04 Hunter Bite**, with its ordinary original Dodge/Guard, G4 injury and source-eligible G4.4 venom. No linked free balance contest. |
| `pounce` | **G6-A `begin_pounce`** commits the authored three-step G1 movement plus original **24-AP** source Pounce, one G0 defender assignment and one G6 source receipt. **G6-A `resolve_pounce`** resolves the independently authenticated **B06-AT-06 Bite**, its G4 damage and G4.4 single poison exposure, then **exactly one** linked opposed Strength balance attempt for an able defender (or source-authorized unable-to-contest Prone). No second Bite or invented Grapple. |

The original attack face, natural-20 confirmation face, critical d4
faces, damage d6, wound d20, and venom resistance d20 all derive from
the same SHA256 keyed **`opening_bite`** stream for each policy/seed.
Thus differences in positional and linked Pounce force are not
artifacts of re-rolling an ordinary Bite. Pounce's separate balance
d20s and declared Strength method are paid only when the defender
can actually contest. A missed Bite **can still legitimately knock
down** an able prey if the independent native force roll wins.

Native A/B melee, R Bow and F Flame are attempted on their genuine
G0 turns only when source position and state permit. Prone A is
**not** silently stood up for free; it sits out unsupported subsequent
weapon actions until a separate legal Standing policy is applied.
Hunter may make a later normal Bite if it retains actual head-forward
contact and is alive. Maximum **two genuine whole Initiative rounds**.
All cutoffs and unresolved mechanics are explicitly classified;
observed death/Prone is not a fabricated terminal.

## Venom chronology and recovery

The existing [G4.2 world clock](b06-g42-persistent-world-encounter-clock-v0.md)
and [G4.4 Hunter venom](b06-g44-hunter-venom-endurance-v0.md)
are reused without reimplementing source poison stages.

1. Enter Initiative through `e.g4.clock.enter_initiative()` before
   Round-1 turns. Pounce Bite may create one native accepted
   `g44_hunter_accepted` with **no immediate toxin penalty**; its
   source timeline owns the next onset, escalation and expiry.
2. Resolve G4.5's real combat Regeneration Step and G4 Step 3 on each
   actual own turn, including wound repair/Dying consequences, rather
   than advancing poison with fabricated initiative turns.
3. **Only at completed Round End**, with no open attack slots or
   suspended Pounce, allow `clock.leave_initiative()`. This means the
   bounded combat-observation policy has stopped; **it does not**
   certify Hunter withdrawal or a safe return to camp while the
   Hunter might still be alive.
4. Advance **actual exploration seconds** through
   `g4.advance_exploration(seconds)` (0–21,600 source seconds).
   G4.4 alone interprets the Hunter's **10-minute onset**, optional
   **30-minute escalation** and sourced expiry; G4.2 alone awards
   already scheduled **six-hour** Vigor/Spent-VP checkpoints, and
   dead actors cannot regain resources.
5. The precise deadline after a genuine combat round obeys the
   clock's **conservative initiative-to-exploration conversion**; it
   need not occur at exactly `world_seconds=21600`. No extra
   benefit is assigned solely because a report requests six hours.

`clock_handoff` records source ledger indices of true Hunter
milestones and six-hour recovery receipts. It exposes
`not_a_combat_terminal: true` to make the scenario's unresolved
fictional disengagement explicit. No hidden Free Recovery, retroactive
wound repair, poison stage reset, fabricated exploration encounter
or automatic escape occurs.

## Eight bounded source cohorts and acceptance

[`scripts/b06_g7e_ambush_pounce_recovery_v0.py`](../../scripts/b06_g7e_ambush_pounce_recovery_v0.py)
supports 1–128 independent paired seeds per each of eight cells,
`round_limit=1/2` and `exploration_seconds=0..21600`.
At 128 seeds, the eight-cell ledger census accounts for **1,024
individual observations**, not a Hunter difficulty probability.
Outcomes remain:

- `hunter_defeat_attested` — genuine G6-D independently proven
  final Hunter death (only where supported by exact native sources).
- `party_defeat_observed` — actual dead PCs, but **no** G7-C certified
  whole-party death without each source-linked terminal proof.
- `legal_window_cutoff` — ongoing live scenario at policy ceiling,
  not survival, victory, successful escape or completed combat.
- `unresolved_mechanical_branch` — actual unavailable mechanics,
  character, round and source reason retained with a native ledger.

Original G7 readiness 48-cell manifest is left untouched; a
forest geometry/Pounce implementation **does not make its universal
ambush and representative-play claims valid**. Pounce numbers remain
source-authored but provisional for balance. Historical **4,096
one-round Phase 3 first stops** and SHA-256
`c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`
are not rerolled or recomputed.

Run:

```sh
python -m unittest discover -s tests -p 'test_b06_g7e_ambush_pounce_recovery_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.b06_g7e_ambush_pounce_recovery_v0 --seeds 128 --exploration-seconds 7200
python -m scripts.b06_g7e_ambush_pounce_recovery_v0 --seeds 8 --exploration-seconds 21600
```

Remaining mandatory gates for G7-F: **authored surprise/awareness
consequences**, fictionally and mechanically lawful disengagement
before extended exploration if Hunter survives, native positive
multi-target whole-party-defeat witness, broader player protection
and ranged/offensive tactics, and representative human/GM tactical
sample acceptance. **Hunter CR stays unrated; no general B06
complete encounter pack or MVP end-to-end Focus build is certified.**
