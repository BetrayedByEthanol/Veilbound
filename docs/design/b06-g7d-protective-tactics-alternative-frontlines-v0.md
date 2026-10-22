# B06 G7-D — Protective Tactics and Alternative Frontlines v0

> **Executable two-round source policies, not a general tactical engine,
> complete encounter calibration, or a Hunter CR.** G7-D integrates
> existing *native G6-D* Protective Intervene into G7-A's genuine multi-round
> mixed-party sequence and separately verifies a B-head-forward source
> position. It does not rewrite the frozen 48-cell G7 readiness plan.

## Rules and source boundaries

G7-D reuses [Protective Intervene v0](../rules/05-combat/protective-intervene-v0.md)
without inventing a second shield/body resolution. The existing
[`ReactiveHunterProtection`](../../scripts/b06_hunter_reactive_intervene_g6d_v0.py)
is a **single original paid Hunter Bite** executor, limited to
the source **A ward / B Guardian protector** and the actual one-square
Hunter head-forward target. It authenticates the G5 one-slot declaration,
original precommitted ward defense, actual G0 spontaneous Reaction or
reserved G1 MP release, the protective Shield Guard or Body Take Hit,
original-source critical severity, one G4 damage/venom recipient, and
final paid G5 resolution. G7-D calls it inside a real G0 Initiative
round sequence; it does **not** turn a G6-D isolated component into a
phantom free effect.

The independent B-head-forward variant is a *different preauthored
starting scene*, not a post-launch target rewrite: source B
(`guardian`) starts at Hunter head-forward **(2,2)**, source A
(`vanguard`) starts at side **(3,3)**. Hunter remains a true rigid
head/rear 1×2 at (3,2)/(4,2), and G1 authenticates the head-forward
Bite into B plus real side-source A→Hunter sword contact. Bow R and
Scholar F keep their sourced original positions, with previewed
real clear lanes; G0/G5 rolls and G4 damage are not exchanged between
character sources. Existing A-front G6-C, G7-A/B/C default scenes and
their reported observations keep their original scenario IDs and
positions.

## Seven bounded scenario-policy cohorts

| Native cohort | Level/party | Real source policy |
|---|---|---|
| A front, control | L3/P4 | Real Hunter Bite vs A, ordinary assigned Guard/Dodge, A/B melee and R/F damage |
| A front, Reactive Shield | L3/P4 | B Guardian protects A with a **real G0 Reaction**, conditional **one Guard use**, no free movement; genuine G6-D one-Bite executor |
| A front, Prepared Body | L3/P4 | Hunter's Round-1 ordinary Bite; B Guardian spends native own-turn G1 MP to step from (3,3)→(4,3), **precommits** a named conditional protective Bite return (4,3)→(3,3), then on Hunter's next qualifying Bite one genuine **G0 MP Interception** transfers any real hit to B; **Reaction stays available** |
| B front, ordinary Bite | L2/P3, L2/P4, L3/P3, L3/P4 | Source Hunter targets shield-bearing B at actual (2,2) head-forward square; A acts from the real adjacent side, no invented A-protects-B maneuver |

Reactive and Prepared **do not** invent protection for L2/P3,
L2/P4 or L3/P3, which had not previously been source-component
verified. The code intentionally refuses `reactive_shield` and
`prepared_body` there. Nor does the existing G6-D A-ward/B-protector
adapter authorize a mechanically reversed B-ward/A-protector response;
that is a future separately supported protection gate.

Only **warned_clear** geometry and at most **two genuine native rounds**
are supported. The Prepared variant reserves the exact named
`g6d:prepared:hunter:vanguard:next_bite` trigger on B's first
own turn. G0's next-turn expiry remains authoritative; G7-D never
spends or releases old MP automatically. If the Hunter/ward/protector
becomes unable to make/receive an attack, the simulation follows
the corresponding source-bounded no-attack/ordinary response path,
not a fabricated successful protection.

SHA-256 keyed rolls share primary Hunter Bite, wound, venom and
normal party-attack keys across the A-front control/protected cohorts,
without consuming a mutable random stream. Each actual G6-D
protected Bite must match a separately recorded `g5_melee_resolved`,
and its `g6d_protective_bite_attested` receipt must reference the
real G0 `spontaneous_committed` or `interception_released`
event. Prepared protection also requires the genuine completed
saved-MP G1 return step to the original protective lane.

## Measurement and certification limit

[`scripts/b06_g7d_protection_frontlines_v0.py`](../../scripts/b06_g7d_protection_frontlines_v0.py)
offers `run_trial(level,size,seed,policy=...)` for its **seven exact**
source cells, and `census(seeds=8)` to `census(seeds=128)`.
It records true ledger digest, start/end source HP/Vigor, source
turns, actual protective receipt counts, native damage/wounds,
genuine Hunter-death terminal where independently attested, and
exclusive *observed* statuses:

- `hunter_defeat_attested` — a real source-verified lethal Hunter hit,
  genuinely completed before terminal attestation.
- `party_defeat_observed` — all original PCs actually dead; **not a
  minted G7-C full-party defeat token**.
- `legal_window_cutoff` — still within live bounded combat after two
  rounds; not a draw or survival probability.
- `unresolved_mechanical_branch` — unavailable source or genuine
  mechanical choice, retained with actor, round and reason.

The data explicitly sets `complete_party_packs_certified: 0`,
`sampled_win_rate: null`, `ci95: null`, `hunter_cr: null`.
Even though paired seeds can expose changes in actual Guard/Reaction
spending and HP/Vigor trajectories, **the pilot policies and two-round
ceiling are not representative player tactics**. These bounded
counts must **not** be promoted into a Hunter CR or encounter win rate.
The original G7-C source-attested full-party exit remains separately
available; G7-D has no authored retreat exits.

Historical Phase 3's **4,096 first-stop** observations and original
SHA-256 `c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`
are unchanged. G7-A/B/C reporting and previous component tests remain
independent. The original 48-cell matrix is still a **readiness plan**,
not automatically marked complete because of G7-D pilot rows.

## Verification and next gates

```sh
python -m unittest discover -s tests -p 'test_b06_g7d_protection_frontlines_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.b06_g7d_protection_frontlines_v0 --seeds 128
```

Tests cover the seven scene-policy cells, true B-front head contact,
native target and MP/Reaction/protective Guard/Body provenance, one
preauthored Interception and genuine saved-MP movement, source-invalid
role reversal, exclusion of unsupported L2/P3/P4 protection, legacy
G7-A/B/C stability, 7×128=**896** denominator preservation,
deterministic SHA-256 and continued absence of CR certification.

Remaining prerequisites: genuine B-ward protective source/path
qualification if desired; multiround Hunter target redirection with
positive G7-C all-party death evidence; forest ambush and natural 1×2
Pounce, more tactics and long poison/recovery execution; finally
representative GM/player data for actual encounter balance.
