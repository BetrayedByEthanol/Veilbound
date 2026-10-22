# B06 G7-G — Hunter Pursuit, Party Defeat and Lawful Disengagement v0

> **Source-native, fixed-policy implementation candidate.** This is not a
> representative Hunter difficulty model, universal AI, free ambush mechanic,
> unrestricted chase subsystem, sampled win rate or numerical challenge rating.
> Historical Phase 3 and G7-A–F evidence are unchanged.

## Scope and source authority

- Source roster: native L2/L3 A/B/R[/F] party and Hunter **B06-EN-03**, using [G6-C mixed_scene](../../scripts/b06_hunter_mixed_party_g6c_v0.py).
- G0 owns Initiative/turn resource refresh and full Round End. G1 owns Hunter rigid **head/rear**, translation, anchored 90° pivot, exact MP and response windows. A nominally adjacent target is **not** automatically in the Hunter's single head-forward Bite square.
- G5 owns **24-AP natural Bite B06-AT-04**, paid defenses, hit/critical proof and G4.5 source attribution. G4 owns HP, Vigor, wounds, Dying and actual death. G7-C owns the independent strictly authenticated all-party defeat/exit gates.
- The script chooses a **deterministic route** by asking G1 to preview candidate footprints, restoring the Hunter's original footprint before any action; each chosen move is then independently committed through **actual G1 movement/pivot**, cost checked and retained in the original G0 ledger.
- Cautious movement is explicitly chosen where responses cannot be resolved. This pays the real Cautious MP premium instead of silently deleting a possible Opportunity.
- The source Bite is **one Physical Action per Hunter turn**. G7-G chooses a fresh living target for a new genuine sequence after earlier prey die; it does **not** invent an instant free mid-sequence retarget or an extra attack.

## Witness 1 — native Hunter pursuit into positive all-party defeat

Use the actual mixed-party grid, with party members holding their chosen positions and never being moved into Bite range on the Hunter's behalf. The Hunter targets the first not-dead A/B/R[/F], using its legal head-forward Bite if in contact; otherwise it searches a legal cautious G1 translation/pivot route and physically pursues the target across as many **complete** natural rounds as required.

Attack faces are **explicit fixed-dice stress inputs**, not random samples: each hit uses source-legal natural-20 confirmation 20, two real bonus d4 faces of 4, a damage d6 of 6, and a real wound-location d20. The ordinary source Bite's **3+d6 Piercing Pen1** and armor mitigation remain unmodified; G5/G4 calculate whether a particular attack actually kills. The target may be Dying before truly dead, and any next turn's survival allocation consumes genuine Vigor. No HP, conditions, death markers or movements are inserted directly.

Only after the last native Round End can [G7-C PartyTerminal.attest_defeat](../../scripts/b06_g7c_party_terminals_v0.py) accept one lethal G4 event from a paid Hunter B06-AT-04 for **each** independent source PC. G7-G then records a narrow positive **multi-target** witness referencing that exact terminal receipt and the distinct lethal source indices.

An incomplete route, unsupported effect, insufficient movement or the declared **32-round ceiling** must not be converted into party defeat. A legal cutoff remains a cutoff. The authored party's decision to stand/hold and the deliberately extreme successful Bite faces are a **demonstration of mechanical reachability**, not a typical party wipe probability.

## Witness 2 — genuinely opposed departure from a living Hunter

Reuse G6-C's exact [G7-C preauthored border exits](b06-g7c-full-party-terminal-certification-v0.md), without substituting post hoc coordinates or teleporting members.

1. **Round 1:** The Hunter actually pays an ordinary noncritical Bite against the Vanguard. The living party uses real G1 Cautious MP to prepare but does not declare an early scene exit.
2. **Round 2:** The Hunter responds to the altered physical positions, translates through genuine G1 Cautious MP, obtains anatomical head-forward contact with the Vanguard and resolves a second independently **paid G5 Bite**. The party then completes distinct final G1 Cautious steps to its previously authored border squares, and each member calls G5 withdrawal linked to its original G4.5 movement receipt.
3. After the **second complete G0 Round End**, the unchanged G7-C attestor authenticates the original whole-party escape. G7-G independently checks the later Hunter pursuit, paid post-move Bite and every member's existing exit indices before adding its descriptive verification event.

**Boundary:** This proves an **opposed exit from this authored G7-C scene**, not that a Hunter can never track the party through the wider world. No 10-minute exploration advance, six-hour safe rest, universally available disengage action, invented protected passage or permanent cessation of pursuit is asserted. The result carries `ongoing_world_pursuit_not_adjudicated=true`.

A partial exit, end-of-round cutoff, Dying PC, Hunter death, missing Hunter pursuit, illegal post-exit movement or stale G7-C receipt does not gain a G7-G disengagement certificate.

## Executable interface and deterministic evidence

```bash
python -m scripts.b06_g7g_hunter_pursuit_terminals_v0 --mode multitarget_defeat --level 2 --party-size 3 --seed 0
python -m scripts.b06_g7g_hunter_pursuit_terminals_v0 --mode opposed_disengagement --level 3 --party-size 4 --seed 0 --include-ledger
python -m unittest discover -s tests -p 'test_b06_g7g_hunter_pursuit_terminals_v0.py' -v
python -m unittest discover -s tests -v
```

For the source-only fixed-dice demonstration, `seed` identifies the native encounter and G0/G5 event keys; its value does **not** create independently sampled policy variation. Each result retains the native `ledger_sha256`, initial/final real state, completed round/turn counts, source terminal and original Phase 3 digest.

The G7-G tests cover actual L2/L3 P3/P4 defeat/withdrawal witnesses, independent G5/G4.5/G4 fatal provenance, cautious paid G1 pursuit, 2-round exit evidence, preview nonmutation, parameter boundaries, deterministic replay and fail-closed original G7-C gates. The original Phase 3 **4,096**-trial checksum remains `c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b`.

## What is not yet accepted

G7-G does **not** complete B06 representative encounter calibration or certify an MVP encounter pack. It exercises only one scripted no-counterattack party policy for defeat and one scripted Cautious departure policy for escape. The positive wipe uses deliberately extremal fixed dice; no inference about ordinary lethality follows. Both fixtures use authored L2/L3 source party proxy sheets, not independently certified 12-Focus coverage.

**Recommended next gate: B06 G7-H** — combine new terminal witnesses with varied legal GM/player decisions, including full Priest/Scholar resource choices, non-extremal seeded attack sequences, opposed defensive alternatives and encounter completion without fixed-round censoring. Do not assign Hunter CR before complete, independently representative comparative evidence exists.
