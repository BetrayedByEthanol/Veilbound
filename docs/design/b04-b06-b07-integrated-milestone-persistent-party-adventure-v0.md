# B04/B06/B07 — Integrated L1–3 Milestone Advancement & Persistent Party Adventure v0

**Scope:** One reproducible **author-GM fixture** demonstrating the *same* original source A/B/R/F characters at L1, L2, and L3. This is **not an externally observed GM session, a legalizing general level-up rule, a 12-Focus combat certification, or an automatic milestone.** It consumes the original [four-session pilot outline](b04-b05-b06-b07-integrated-mvp-pilot-adventure-v0.md) and two approved GM-declared group-milestone windows; the original fixed G8 engine remains expressly L2/3.

## Source-backed chronological witness

1. **L1 — spoiled shipment and gate:** build the actual G0 L1 party from original A/B/R/F source sheets, install real G1/G2/G3/G4 and use the existing #188 source training and difficulty arithmetic for three author-declared survey, ordinary diagnosis and public-record checks. All three source actors, d20 faces, elapsed G4.2 exploration costs and party ledger are retained in **one live native encounter**. There is **no illegal G8 L1 combat replay**.
2. **Gate milestone → L2:** an individually named author-GM *candidate* event with `kind=adventure_milestone`, `gm_declared=True`, `automatic=False`, the exact L1→L2 order, and the prior source-gate receipt. The audited G0 Level-2 source fields replace only Level-1 caps/identity/action profile. Existing HP, Vigor, Available VP, Committed VP, ammunition, carried wounds and exact pending G4.2 Recovery events remain. **Conservative v0 policy**: the newly awarded Max VP capacity is initially **Spent**, not Available; no free VP refill is invented. This is explicitly a scenario policy under the canonical requirement to avoid automatic refill, **not** a universal level-up rule. Normal six-hour G4.2 Recovery remains the sole subsequent source of VP reimbursement.
3. **L2 — Soldier corridor:** an explicit restricted *first entrance* into a native G8 L2 Soldier after L1 noncombat milestone, with the same actual actor source digests and original G4.2 clock, not a fraudulent prior G8 terminal. The original G0/G2/G4/G5 Soldier two-round **opposed withdrawal** is resolved; the natural-1 G2 Bow launch genuinely consumes one arrow, and source G4 harm survives. The original G8 `party_scene_withdrawal` attestation closes this encounter; no forced exit means no free party safety or Hunter CR claim.
4. **Shrine milestone → L3:** a distinct authored candidate GM declaration, applied only at a settled, source-certified G8 exit with no active poison, maintained spell or unsupported pending milestone requiring a special level-dependent interpreter. Legal L3 G0 snapshots, new source maxima and talents/technique access are independently checked by the pre-existing `audit()`. Committed/Available VP, existing HP/Vigor, wounds, the missing arrow and old Recovery deadlines are **not reset**. The scripted Soldier withdrawal alone does not prove a real GM-approved shrine achievement; that beat remains a separately declared **author fixture**, requiring actual external GM evidence for acceptance.
5. **L3 — Sentry confrontation:** the prior same physical party enters the original G8 L3 cold Sentry through the already reviewed PR #194/#195 handoff at a named, paid 300-second route. The G8 source Sentry terminal requires true native attack/spell/movement results. Original source L2 injury, Bow ammunition attrition, level awards and the pending six-hour phase are carried through the level change.

## Trust, safety and limitations

- `validate_pilot_milestones()` checks two distinct ordered GM records per character. The author fixture explicitly declares candidate milestones; **no code claims to authenticate a human GM**, infer a milestone from winning a fight, use XP, skip levels, apply Anointed Destiny refills or automatically mark the strict MVP gate complete.
- Level transitions are **transaction-preflighted**: source level, authorized profile, source equipment, exact character capacities, no living hazard/host requiring an unsupplied interpreter, no pending G5 slot, no dying participant. Award timing is only at a settled exploration boundary. No pending original Recovery clock ID/phase is rewritten.
- Source-specific new Training/Talents/techniques are represented through the corresponding authored Level-2/Level-3 source build, not by deriving custom benefit effects from a feat-name guess. A/B remain clearly labeled G0 **physical proxies**; this fixture is **not** full Low Priest focus-play certification.
- L1 narrative G0 actor state is bridged **once** to G8 after the first milestone using an explicit different first-entry contract, not the G8-to-G8 `handoff()` which correctly requires a real old G8 terminal. Future G8 encounters use the original authenticated G8-to-G8 handoff.
- Cross-level active G3 maintained spell, poison, or other scheduled G4.3/G4.4 duration migration is **not implemented by this v0 advancement bridge**. Such attempts fail closed rather than fabricate scaling or erase the state. This is narrower than same-level effects continuation in PR #195.
- The original four-session pilot has two L2 sessions but this deterministic witness contains only one representative L2 Soldier scene, an L1 native noncombat sequence, one L3 Sentry encounter and two **author-declared milestone candidates**. It does not fabricate the missing forest/shrine human sessions or true GM achievement.

## Verification

```bash
python -m scripts.b04_b06_b07_integrated_milestone_persistent_party_v0
python -m unittest discover -s tests -p 'test_b04_b06_b07_integrated_milestone_persistent_party_v0.py' -v
python -m unittest discover -s tests -v
```

**MVP status remains:** 12/12 structural pairings verified; 0/12 independent full-Focus certificates, 0/6 accepted gates, 0 authentic human pilot sessions. The earlier 3/7 closed blocker count remains unchanged.
