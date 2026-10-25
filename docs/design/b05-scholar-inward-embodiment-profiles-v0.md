# B05 — Scholar Inward Boost and Embodiment Profiles v0

> **Scope:** explicit Tier-1 profile authoring and executable cost/legality **model** for future Medium and Low Scholar character builds. Not an automatically certified source-native G0/G3/G4 spell encounter; not an L1–3 full character build or global balance test.

## Why this slice is needed

The [Scholar Foundation](../rules/08-archetypes/scholar.md) already locks Medium **Veil Routing** and Low **Prepared Arsenal** identities, known caps **4/5/5** Medium and **3/4/4** Low, Low prepared cap **2/3/3**, Medium reroute costs **3 Spent VP L1–2 / 2 Spent VP L3**, and Low L3 technique-specific Intensification. But existing **Self Projection** spell profiles were explicitly *not* automatically Inward or Embodiment compatible. This slice authors **four exact** compatible alternatives/permissions without applying a Focus bonus to every spell or inventing another technique identity.

Canonical proposed values and timing: [Scholar Inward / Embodiment Profiles v0](../rules/07-veil-magic/scholar-inward-embodiment-profiles-v0.md). Regression/contract model: [Script](../../scripts/b05_scholar_inward_embodiment_profiles_v0.py) and [Tests](../../tests/test_b05_scholar_inward_embodiment_profiles_v0.py).

## Authored alternatives and early resource cases

| Level and Focus, VA 0 | Exact profile choice | Required own-turn AP / VP | Locked intent / limitation |
|---|---|---|---|
| L1 Medium (Max VP 4) | MS-STONE-BODY-T1, Stone Skin Inward Body | **24 AP +1 Committed**; R1 typed HP resistance | Cheaper/weaker than ordinary Stone Skin; not Armor or an outward/ally spell |
| L1 Medium | MS-GUIDED-REGEN-T1, Guided Regeneration Inward Regeneration | **24 AP +1 Committed**; real Self Step +1 throughput | Can reroute Body→Regeneration **+3 Spent**, leaving 0 Available VP. No free HP/Step or changed recipient |
| L1 Low (Max VP 2) | LS-STONE-BODY-T1, Stone Skin Embodiment | **30 AP +1 Committed**; original normal Stone Skin R2 at VC0 | No Priest Chosen discount or inherited reactive Embodiment |
| L1 Low | LS-GUIDED-REGEN-T1, Guided Embodiment | **30 AP +2 Committed**, consuming all Max VP | +1 only at natural Self Step. To switch, release and **pay another Projection**; no Medium reroute |
| L3 Medium (Max VP 12) | Active Inward, Overroute | **+1 Spent per step**, at most 2, with **−2 MP available per step** (**12 / 10 / 8 MP** for zero/one/two steps) | At L3 reroute cost is **2 Spent**; step increases resistance or natural regen +1 but sacrifices real locomotion |
| L3 Low (Max VP 6) | Active Stone/Guided Embodiment, Intensify | **1 Spent** per active unconsumed intensification | Stone R+1 until next own turn; Guided +1 at next genuine own Step; no instant heal, new cast or out-of-turn trigger |

This deliberately preserves a meaningful distinction between **Medium swapping functions through one already paid commitment** and **Low committing to a planned configuration with a costly release/recast**. Medium never gains extra recipients, Low never gains free reaction timing or an enchanted weapon simply because it is equipment-focused.

## Definition gate and evidence matrix

| Gate | Current evidence | B04/B05 acceptance status |
|---|---|---|
| Explicit eligible techniques | Stone Skin / Guided Regeneration named; individual Scholar learning required | **Authored**: 4 profile identifiers, modes, tier, channels and cost |
| Known/prepared limits | Medium ordinary known, Low known+prepared verified against allowed list and cap | **Model checked**; no source character/repertoire signer |
| VP and AP conservation | Available/Committed/Spent ledger + source baseline VA0 formula, 24/30 AP | **Model checked**; not native G0 event attestation |
| Medium one active + reroute | No same-profile refresh, no unsupported other Inward, full cost before release | **Model checked**; no real G3 application/MP enforcement yet |
| Medium L3 Overroute | +1 per paid step; −2 MP per step preview from **12 MP** (10/8 MP when boosted), 2 maximum | **Authored/model checked only**; G1 movement source continuity not yet established |
| Low switch and L3 Intensify | Release refunds only Committed; new activation pays AP; timed benefits | **Authored/model checked only**; no authentic G4 packet or G0 Step binding yet |
| Medium/Low L1→3 builds | Nine Abilities, Training, Talents, equipment, complete technique picks | **BLOCKED**, next B04/B05 build packages |
| PS-03/PS-01/PS-02 combat role outcomes | Source-authored physical attack, real affected enemy or protected ally | **NOT CLAIMED**; build + encounter adapters needed |

### Potential balance concerns to test later

- Medium **1-Committed** Guided throughput vs ordinary **2-Committed** Guided is intentionally an Inward-focus-specific price. Test whether frequent rerouting becomes worth its 3/2 Spent VP fee instead of simply maintaining one effect.
- Medium Stone R1 vs Low full Stone R2 must be compared on actual typed HP packets, Vigor costs, enemy targeting and weapon access—not assumed equivalent buffs.
- Medium Overroute movement sacrifice is **2 MP per step from 12 MP** (not two squares); it must be enforced by **native G1 remaining MP/elapsed-movement proofs**, or the stronger output cannot be certified.
- Low L1 Guided costs all VP, leaving no reserve for emergency casting; Stone can leave 1 Available. Low L3 pending intensification must be consumed by genuine time/Step events and must not conjure a third Projection action.
- The ordinary spell's reactive/maintained rules, damage resistance stacking and native G0 response timing remain authoritative. No Focus-wide numeric tuning or ranking is authorized.

## Next coherent tasks

1. **B04/B05 — Medium Scholar L1–3 Character Build and Native Inward Verification v0:** independently legal nine-Ability/gear/Training/Talent sheet, individually learned known spells, actual G0 actor and G3/G4/G1 effect application, VP and action accounting. Fail closed on unverified Overroute G1 MP reconciliation.
2. **B04/B05 — Low Scholar L1–3 Character Build and Native Embodiment Verification v0:** independent source sheet, prepared known subset/limited VP, actual G0 paid release-and-recast, real Stone resistance and Guided Step-only intensification. A Spellblade weapon synergy needs **its own** explicitly authored compatible equipment technique; these self-buffs do not certify PS-03.
3. **B06/B05 comparative role scenarios** only after both builds are truly native. Measure actual HP/Vigor, movement/response opportunity cost, sustained output and role failure countercases with full ledgers. Preserve no-result/censored evidence and do not replace scripted examples with alleged win rates.

**Disposition:** four explicit executable **profile/cost-contract definitions**, no complete Medium/Low Scholar character or encounter certificate, no change to B01–B07 or the six MVP gates, no numerical balance signoff and no merged status asserted by this document alone.
