# B04/B05 — Anointed Three-Focus Source-Native Mundane G5 Offense v0

> **One real ordinary weapon Attack Sequence per Focus and source L1–3 character, not a new spell/Signature or independent Focus certificate.** Earlier #172–174 witness scenarios tested defensive Soldier/Sentry damage and healing without attempting any player weapon attacks. The three structural Anointed sheets already have a selected ordinary, wielded weapon and its training. This slice explicitly binds that existing equipment/Training and canonical physical packets to the **real G0/G1/G2/G4/G4.5/G5** source-paid Attack Sequence and verifies one-hit offense alongside authentic enemy retaliation.

## Source-approved mundane weapon profiles

| Focus | G0 source role/profile | Authoritative source equipment/Training | G5 attack bonus | Exact canonical ordinary damage |
|---|---|---|---:|---|
| High Restoration | `AH` / `B05-PC-AH-DAGGER-PIERCE` | Wielded **Dagger**; Small Blades 2 | **+3** (Strength 0 + Agility 1 + Training 2) | **2+d4 Pierce, Penetration 0**, Light physical contribution +0 |
| Medium Restoration | `AM` / `B05-PC-AM-DAGGER-PIERCE` | Wielded **Dagger**; Small Blades 2 | **+3** | **2+d4 Pierce, Penetration 0**, Light +0 |
| Low Restoration | `AL` / `B05-PC-AL-SWORD-CUT` | Wielded **Sword**; One-Handed Swords 2 | **+3** | **3+d6 Cut, Penetration 2**, Light +0 |

[Native weapon referee](../../scripts/b05_anointed_native_melee_v0.py) checks each actual sheet's path/SHA256, source status, exact L1–3 start state, Ability/Training/gear selection, current HP/Vigor/AP/Focus/Guard/resource formula and a **genuinely wielded G2 weapon** in the actual G1 encounter. A purchased item, a stale Guard, spoofed source hash or fabricated alternate spell profile cannot authorize a hit. G0 exposes **only one sourced mundane profile per Anointed Focus**. Neither a free weapon enchantment, a new Aspect power, extra AP, changed Destiny nor new wound mechanics is granted.

**Native G1 contact** must have true G2 weapon readiness before G5 declarations. Both G0 Guard commitment and G5 Guard rechecks require current wielding, so the source sheet's Guard number by itself is insufficient. G5 uses the actual **d4 for High/Medium Dagger** and the existing **d6 for Low Sword/Soldier/Sentry**; its pre-roll validation and G4 typed damage use the identical source packet. G4.5 binds the G0 paid Physical Action to its exact source profile and target; G4 resolves the ordinary Armor/Penetration, confirmation and Wound rules without introducing a second damage or spell effect.

## Bounded L1–3 encounter evidence

The [native source-offense runner](../../scripts/b05_anointed_native_g5_offense_v0.py) provides **36 fixed cases = 3 Focuses × L1/L2/L3 × 2 existing opponents (ordinary Soldier B06-EN-02 / prepared Firebound Sentry B06-EN-01) × 2 policies (`hold` / `strike`)**. On a genuine Round-1 turn with a real G2 ready weapon, `strike` declares and resolves **one G0-paid G5 Physical Attack** with source d20=12 and selected d4/d6 face=4; `hold` conserves AP. Both cases receive **one authentic G5 Soldier/Sentry reply** with sword d6=2 and prepared Sentry source Vigor damage when relevant. Every defender selects `take_hit` as an explicit policy (no hidden Guard/Dodge). All ordinary weapon contact, damage and spent AP are real; no winner/terminal certificate or sampled win rate is claimed.

Against the same initialized opponent and fixed dice, the **Dagger** changes Soldier HP by **1** and prepared Sentry HP by **3**, whereas the **Sword** changes them by **4** and **6**, respectively. This follows canonical Armor mitigation and physical Penetration. Ordinary attacks do not drain source VP, trigger the Returning Step, create an extra G4 Regeneration Step or spend Destiny. This is not an optimization study, an Anointed melee-specialist class grant, automatic Opportunity, Riposte, magical attack, hostile Intrusion, or representative AI play.

The [eleven native regression methods](../../tests/test_b05_anointed_native_g5_offense_v0.py) cover all 36 cases, the exact d4/d6/Penetration delta and same-exposure `hold` control, true G0 Paid Action → G5 source profile → G4.5 consumed hit → G4 damage, source fingerprint, actual G1/G2 wielded contact, invalid/missing G2 readiness, invalid dagger d6 face with retry before roll/damage, spoofed source/profile denial, deterministic full-ledger replay and recomputed-hash forgery rejection. The older native actor, High/Medium/Low Signature and #172 defensive-witness tests are updated **only** to recognize the one ordinary source profile; none of their previously bounded Signature/Authority behavior is changed.

## Remaining B04/B05 and MVP readiness

The selected Anointed **Life/Restoration** pairings are now structurally sourced with genuine mundane G5 offensive access; that is **not certified** combat versatility or finished Archetype × Focus viability. This first slice is one source attack per turn, fixed contact, no cover/terrain, no pressure tactics, no opportunity/interception, no unopposed healing cast or contested beneficial Intrusion in these offensive scenes, and no active magical defensive responses. The term **unopposed** in prior healing encounters refers exclusively to consenting beneficial restoration, not to the `take_hit` physical defense here. Noncombat Mission identity and actual six-hour Destiny or GM significant-event awards still require integrated testing; so do multiple opponents, adaptive tactics and full L1–3 progression/role comparisons.

**MVP counts stay unchanged:** **12/12** structural Focus builds, **0/12** independently certified complete Focuses, **0/6** strict MVP exits; B04–B07 remain open and the original bounded B06 **G0–G8** milestones remain fixed.
