# B06 G7-C — Full-Party Terminal Certification v0

> **Bounded native source evidence.** Establishes a genuine all-party
> withdrawal certificate and a fail-closed all-dead Hunter-Bite
> certification gate for the original L2/L3 × 3/4-player mixed-party
> Hunter fixture. It does **not** claim that the one-round withdrawal
> policy samples representative play, verifies generalized party defeat,
> constitutes a complete encounter difficulty sample, or assigns CR.

## Native scene-authored full-party exit

G5's pre-existing single-actor `SceneExit` authority was extended with
an optional **tuple** of independently authored `SceneExit` records.
The previous single-exit constructor and G7-B archer exit remain
unchanged. Scene authoring still strictly validates scenario, grid,
objective, actor, border square and source policy before any attacks;
no new exit can be chosen while withdrawing, and duplicate actor exits
or simultaneous single/multiple modes are rejected. The legacy
`scene_exit` constructor argument is still strictly type-checked
**before** any exit-member dereference, so malformed values reject with
`ValueError` rather than an accidental `AttributeError`. All G5 exits retain
their own authentic G1 movement + G4.5 signed exit + G5 terminal
receipt.

The new **G7-C-specific** mixed scene requests `party_exits=True` and
authenticates these routes and squares:

| PC source | Start | Exact authored border exit | Genuine one-round movement |
|---|---|---|---|
| A Vanguard | (2,2) | (0,2) | west, west |
| B Guardian | (3,3) | (3,6) | south, south, south |
| R Archer | (1,4) | (0,4) | west |
| F Scholar (4-PC) | (1,0) | (0,0) | west |

Every step consumes **ordinary source MP**. Cautious movement is an
explicit, legal policy, chosen to avoid unresolved Opportunity attacks,
with its real increased cost: A 8 MP, B 12 MP, R 4 MP, F 4 MP. No actor
teleports to the exit or receives an invented free response. The Hunter
acts first and uses G7-A's native keyed Bite/defense policy; a damaged
or Dying Vanguard cannot withdraw just because the other party
members reached their borders.

One-party terminal attestor `PartyTerminal.attest_withdrawal()` checks:
- **An entire completed native Initiative round**, no suspended current
  turn, and no unresolved previously paid G5 Attack Sequence slots.
- The original and exact sourced **A/B/R[/F] party** and living Hunter;
  no existing Hunter-victory or incompatible/duplicate party certificate.
- Exactly one **previously authored** policy, G1 final paid step,
  G4.5 signed event and G5 signed exit per present party member,
  with matching actor, border square, movement/event index, policy and
  correct chronological ordering.
- Each PC remains above 0 HP and is at their individual authored exit.
  No qualifying PC is subsequently harmed or takes another paid action
  after their source-signed withdrawal. **Any later actor-linked G1 event
  (including a move away followed by a return) or subsequent G0 own-turn
  start/resources also invalidate that actor's exit receipt**, even when
  a later Round End leaves the PC at the exact original border square.
  The immediate `turn_end` closing the legitimate exit turn is allowed;
  a newly begun turn is not.

Only then is the **unique** native ledger event
`g7c_party_withdrawal_attested` issued with all member evidence indices.
A single R exit in G7-B or a missing/blocked/dying PC is *never*
promoted to a whole-party escape.

## Native party-defeat evidence and precedence

`PartyTerminal.attest_defeat()` is an independent **fail-closed gate**:
all original PCs must have actually reached their source-specific
**dead** HP threshold, not merely 0 HP or the Dying state, after a
full Round End. No party member may have an attested exit; the Hunter
must remain alive; no conflicting terminal may already exist.

Each death additionally requires genuine G4 lethal damage from the
Hunter's Bite profile `B06-AT-04` bound to **that same target** by
a paid real G5 `g5_melee_roll` hit, G4.5 source-authenticated
`g45_attested_hit`, and G5 `g5_melee_resolved` with matching
native action index, round, Hunter turn, and ordering. Manually
changing an actor's HP, appending unverified G4 packets, or reaching
Dying cannot mint a party-wipe token.

**The fixed G7-C one-round escape fixture does not produce a genuine
all-dead Hunter-Bite playthrough**: that requires multi-round
Hunter retargeting and independently authorized movement/contact.
Consequently its census does **not** report attested party-defeat
observations; the rejection side of the certificate is tested here,
and its first positive Hunter multi-target witness remains a gate.
This preserves the difference between *a source-backed attestation
contract* and *an evidenced playable multi-target policy*.

Terminal precedence is fail-closed: incomplete/unsupported mechanics
are never treated as a terminal; the completed-round boundary and
outstanding attack slots are checked first; existing Hunter defeat
and full-party attestation cannot be overwritten by a conflicting
withdrawal/defeat certificate. A partial retreat alongside a dead/
Dying PC is an **incomplete observation**, not a party escape or wipe.

## Four native bounded cohort cells

[`scripts/b06_g7c_party_terminals_v0.py`](../../scripts/b06_g7c_party_terminals_v0.py)
runs a source-authorized **single round** of Hunter Bite followed
by eligible PCs pursuing their independent routes. Four cells:
L2/P3, L2/P4, L3/P3, L3/P4; a fixed keyed seed specifies Hunter
attack, defense, critical, damage and actor regeneration choices.

Each requested seed is retained under one of
`party_withdrawal_attested`, `party_defeat_attested`,
`legal_window_cutoff`, or `unresolved_mechanical_branch`.
Every completed withdrawal is a **scene-specific full-party terminal**,
not a general combat victory. Partial exits, Hunter-induced deaths
and Dying without every member leaving are censored. The
`party_defeat_attested` column remains zero until the native positive
multi-target Hunter witness is added.

Census supports 1–128 paired deterministic seeds per cell, with
every seed represented by a hashed native source ledger and explicit
category counts. It preserves the original Phase 3 4,096-window audit
SHA `c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`.
G7-A and G7-B scripts, original G6-C fixed scene, and historical
terminal definitions remain separately available.

**No Hunter CR, representative withdrawal frequency, calibrated
survival rate or certified complete scenario pack** is inferred.

## Tests and remaining work

```sh
python -m unittest discover -s tests -p 'test_b06_g7c_party_terminals_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.b06_g7c_party_terminals_v0 --seeds 128
```

The initial G7-C regressions check four independent 3/4-PC
L2/L3 complete exit certificates, real Step/receipt lineage,
partial/unfinished/duplicate/contradictory terminal rejection,
Dying versus dead distinction, forged generic G4 lethal records,
late harm after actor exit, wrongly authored exits and modified
movement receipts, 128-seed complete denominator, prior G7-B
policy preservation and deterministic digest.

**Next:** positive multi-target native Hunter Bite party-wipe
witness; more than one round of genuine party-alternative decisions;
Integrated Reactive/Prepared Intervene; alternate frontlines and
forest ambush/Pounce; toxin/recovery continuity; representative
human/GM policy calibration.
