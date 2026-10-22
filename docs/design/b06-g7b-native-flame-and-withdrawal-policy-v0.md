# B06 G7-B — Native Flame Critical and Bounded Withdrawal Policy v0

> **Implementation and censored-policy evidence; not a universal tactical
> engine, complete party-escape terminal, sampled win probability, CR,
> or certified B06 pack.** This milestone adds an explicitly confirmed
> direct-hit Scholar Flame and one independently authored R Archer
> withdrawal option to G7-A's four warned-clear A-head-forward encounters.
> It deliberately does **not** enable ambush, alternative head-front
> targets or unverified protective Intervene in the multi-round runner.

## Native G3→G4 Flame critical completion

[Defensive Responses and Criticals](../rules/05-combat/defensive-responses-and-criticals.md#natural-20-and-confirmation)
and [Conjure Flame](../rules/07-veil-magic/conjure-flame-v0.md#a-thrown-flame--thrown-projectile)
already explicitly say a **direct-hit Thrown Flame** uses the ordinary
natural-20 confirmation procedure, assigning **+1d4 Fire HP** for Strong
or **+2d4 Fire HP** for Critical/Devastating before Fire Resistance.
The independent Vigor packet does **not** receive additional critical
dice. This PR implements that *existing* rule in a native, bounded
G3/G4 execution path:

- G3 accepts **optional explicit** `confirmation_face` and exact
  `critical_dice` on a natural-20 Thrown Flame. When present,
  confirmation and Fire HP dice are validated **before** AP, Spent VP
  or defender-resource payment.
- The current single committed ranged defense is used for confirmation:
  an ordinary Take Hit gives Critical unless confirmation also rolls
  natural 20 (Devastating); eligible aware Dodge/Guard can produce Strong
  after failed confirmation. No second attack or second Projection AP.
- If a live `on_committed` response changes the intended defender's
  Dodge Pressure or any other ranged-defense input, **G3 re-evaluates
  the critical tier against the recomputed live G2 defense** before
  Spent VP or defensive capacity is paid. If the tier no longer
  matches the previously declared critical dice count, G3 logs
  `post_commit_critical_tier_changed` and interrupts before launch:
  original Projection AP stays spent, Spent VP remains zero, and no
  Fire/Vigor packet or defensive commitment is fabricated or rerolled.
  Responses that change the defense but **not** the tier can proceed.
- G4 preflights the correct Fire HP **including** bonus dice and
  independently requires the wound-location d20 on a 0-HP crossing or
  Devastating wound. G3 then commits one real launch with the exact
  critical tier and d4 provenance. G4 consumes that *same launch* once,
  for one Fire HP and one separate Vigor packet, and applies an
  actual Devastating wound when qualified.
- Existing callers that **omit** a natural-20 confirmation retain the
  previous `critical_confirmation_pending_G5` result, with real AP/VP
  spent and no fabricated damage. Old G7-A results/census continue to
  use this legacy behavior; the new G7-B policy opts into predeclared
  confirmation and source-derived G4 damage.
- The Hunter G6-D lethal-terminal validator now independently supports
  genuine G3→G4 **source F** fatal Fire packets, matching the exact
  launch-keyed G4 event/turn and excluding pending, missed, other-caster
  or spoofed lethal claims. A Hunter merely **Dying** is still not a
  verified Hunter kill.

The new path is a **direct** single-target physical projectile under
the already supported G2 lane and legal defender. This does **not**
settle living screens, area/scatter, cover collision, Reactive Stone
response to a transferred hit, or multi-target effects.

## One deliberately authored exit: R Archer, not full party withdrawal

G7-B extends the existing [G6-C source scene](b06-g6c-mixed-party-hunter-encounter-v0.md)
**only when explicitly requested at scene creation** with a
G5 `SceneExit` for the sourced R Archer at map border **(0,4)**.
R starts at **(1,4)**; on its own turn the policy preselects either
one ordinary real Bow shot or a **one-cell westward G1 step** and
attempted G4.5/G5 scene-authenticated withdrawal. The step is
refused before execution if it needs an unimplemented Opportunity or
passes through an ally. No free teleport or cancellation of costs.

A legal exit requires the immutable scene / grid / objective / actor
/ border policy, genuine paid G1 completed step, living/standing R,
no pending ordinary attack slots, and identical G4.5 / G5 movement
event indices. If R withdraws, any later actors in that real round
complete their legal G0 turns **without new offensive actions**,
then this encounter observation stops after actual Round End.

The outcome **`archer_withdrawal_attested`** is *one party member's*
proven exit. Other party members remain in the encounter; it is
**not a full-party retreat, defeat, mutual withdrawal or combat victory**.
No generalized “the whole party can now escape” rule is introduced.
The original G6-C scene and fixed witness remain unchanged when
`archer_exit=False`.

## Native scenario / policy matrix

[`scripts/b06_g7b_tactical_terminal_census_v0.py`](../../scripts/b06_g7b_tactical_terminal_census_v0.py)
uses two explicitly selected policies in each of the original
**four** L2/L3 × P3/P4 warned-clear A-frontline cells:

| Policy | Native behavior | Still unavailable |
|---|---|---|
| `g7b_flame` | Real keyed Flame natural-20 confirmation, exactly sourced Fire HP/Vigor, unchanged A/B/R physical offense | Party-wide retreat, alternate targets and unverified protections |
| `g7b_archer_exit` | Same Flame policy; R independently prechooses source-declared **Bow vs one-step exit** | Withdrawal of A/B/F or of the whole party, post-exit group play |

This means **eight bounded *policy cohorts***, not eight newly certified
difficulty scenario geometries. Each uses independent SHA-256-keyed
draws (unchanged from G7-A), naturally preserves paired rolls across
L2/L3 and P3/P4, and records a complete native G0 event log digest.
For each cohort `census(seeds=128)` accounts for every one of the
128 inputs under five mutually exclusive outcome classes:

| Category | Meaning |
|---|---|
| `hunter_defeat_attested` | Lethal G4 event linked to paid G5 melee, paid G2 Bow, or authenticated direct G3 Flame, after a genuine completed Round End |
| `party_defeat_observed` | All source PC actors actually dead; no generic party terminal certificate inferred |
| `archer_withdrawal_attested` | **One** sourced R Archer genuinely reaches and leaves via the predetermined border |
| `legal_window_cutoff` | Three-round cap, no attested terminal; **not** a draw |
| `unresolved_mechanical_branch` | Unsupported source branch with full actor/round reason; **not** an outcome silently treated as death or withdrawal |

The census explicitly reports `actual_party_withdrawals: 0`,
`sampled_win_rate: null`, `ci95: null`, `hunter_cr: null`,
and `complete_party_packs_certified: 0`. Its
`incomplete_or_single_exit` includes all censored windows,
unresolved mechanical branches **and** partial Archer withdrawals.
It never removes them from a denominator to manufacture win rates.

**No new probability estimate** is justified by this tactical-policy
pilot. Actor positioning, number of scripted decisions, enemy choice,
retreat incentives and reaction integrations are not a representative
population of human-GM combat choices.

## Unchanged boundaries and next gates

**Phase 3** remains **32 × 128 = 4,096 first-stop windows**, with
the original canonical digest
`c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`.
G7-A's original `run_trial(...,policy_mode="g7a")` and original
census **retain** their prior policy and unresolved natural-20 Flame
handling. G7-B reports are a distinct version/namespace; they are
not an overwrite of historical or G7-A evidence.

The remaining core G7 gaps are **full-party withdrawal or source-attested
party defeat**, source-backed integrated Reactive/Prepared Intervene,
alternate Hunter head-forward contact and real forest ambush/Pounce,
wider legal spell/reaction tactics, long toxin/exploration clock
continuation and six-hour recovery, and actual human/GM-play evidence.
**Do not assign Hunter CR or encounter difficulty cutoffs** before
representative full encounter comparison is available.

## Verification

```sh
python -m scripts.b06_g7b_tactical_terminal_census_v0 --seeds 8
python -m scripts.b06_g7b_tactical_terminal_census_v0 --seeds 128
python -m unittest discover -s tests -p 'test_b06_g7b_tactical_terminal_census_v0.py' -v
python -m unittest discover -s tests -v
```

The G7-B regression suite covers actual Fire HP/Vigor packet parity,
Critical/Strong/Devastating confirmation, early failure on missing
critical/wound dice, legacy natural-20 G7-A compatibility, source-tied
one-step Archer exit (and invalid exit claims), eight policy cohorts,
replay fingerprints, and full 128-seed accounting. These are native
executable checks, **not tabletop CR validation**.
