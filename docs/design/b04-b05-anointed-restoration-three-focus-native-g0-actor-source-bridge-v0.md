# B04/B05 — Anointed Restoration Three-Focus Native G0 Actor Source Bridge v0

> **Source-backed native actor provisioning only.** Merged #166 completed **12/12 structural L1–3 pairing sheets**; this bridge makes High/Medium/Low Anointed source identities usable in existing G0 encounter state, NOT new native Signature/Authority, completed G4 wound resolution, combat role certification, native G5 attacks or representative encounter victory. Keep **0/12 independent Focus certificates** and **0/6 strict MVP exit gates**.

## Original source identities

The [High](b04-b05-high-anointed-restoration-l1-l3-character-build-verification-v0.md) (#164), [Medium](b04-b05-medium-anointed-restoration-l1-l3-character-build-verification-v0.md) (#165), and [Low](b04-b05-low-anointed-restoration-l1-l3-character-build-verification-v0.md) (#166) source-verified **Life / Restoration** Anointed builds share one birth-surge Mission and one legal permanent bond. [Anointed authority and Destiny](../rules/08-archetypes/anointed-signature-authority-l1-3-v0.md) stays a separate **isolated** referee until its AP/VP/Vigor/recipient-Step/Intrusion and real action receipt validations can be integrated.

The [native G0 actor adapter](../../scripts/b05_anointed_native_g0_actor_v0.py) introduces three explicit, noncolliding role IDs:

| Source ID | Focus | HP L1/L2/L3 | Vigor | VP | Physical / Projection AP | Regen throughput | Guard capacity |
|---|---|---|---|---|---|---|---|
| `AH` | High | 12/12/12 | 12/24/36 | 6/12/18 | 30 / 20 | 3/3/3 | 1/1/1 |
| `AM` | Medium | 12/12/12 | 12/24/36 | 4/8/12 | 24 / 24 | 4/4/4 | 1/1/1 |
| `AL` | Low | 12/12/12 | 12/24/36 | 2/4/6 | 20 / 30 | 5/6/6 | 1/1/3 |

All have Turn AP **30/36/42**, initial full legal resource ledgers, individually source-hashed authored `.py` sheet identities, starting armor, wielded Dagger or Sword as actually sourced, trained weapon Guard **13**, and no invented native melee attack profile. The Low L2 TAL-C02 increases the *one existing Step's regeneration throughput*, and L3 TAL-C05 increases normal Guard capacity, *not Opportunity or Reaction*. Their actual **G0 native Regeneration Step** may spend existing self Vigor on chosen HP/repair allocation, but does **not** trigger an implicit Returning Step Signature.

This adapter is deliberately outside the mature B06 G0/G4/G5 modules' gameplay semantics; `party_actor("AH"|"AM"|"AL", level, ...)` dispatches source-backed G0 character creation, preserving historical role IDs A/B/R/F/H/M/S/T. `Source.status = STRUCTURAL_B05_ONLY` and empty `attack_profiles` explicitly prevent attaching unapproved combat mechanics. A starting Sword or Dagger does not automatically authorize a source G5 melee attack or Conflagration packet.

## Acceptance scope

[Regression tests](../../tests/test_b05_anointed_native_g0_actor_v0.py) audit all **nine** Focus × level source profiles and SHA-256 links; genuine G0 Round Begin/own-turn Step-2 HP+Vigor accounting, ordinary Physical AP and G0 VP conservation; L3 Low Guard Reserve and two separately paid Physical Actions; the absence of Destiny/Vessel/Signature fields in native Actor; invalid levels/footprints and untouched original source dispatch. No mock Step flag is treated as an authentic spell receipt.

**Next:** integrate one explicit High Anointed Returning Step legal Projection and its recipient Vigor-to-HP packet against G0/G4 state, then bound Medium/Low Step authorization and exact L3 Guided Authority. Keep action legality, beneficial refusal/Intrusion, actual current delivery geometry and packet ledger authority unified. Do not infer a complete all-three-Focus playable build, noncombat identity, GM adventure, extra B06 milestone or **0/6** exit gate closure from this provisioning bridge.
