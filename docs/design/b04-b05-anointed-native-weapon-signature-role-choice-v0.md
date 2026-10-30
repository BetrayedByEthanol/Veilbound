# B04/B05 — Anointed Native Weapon and Returning Step Role Choice v0

> **Bounded integrated G5 combat choice, not certified Focus or full representative play.** Merged #175 granted source-authenticated mundane Dagger/Sword access to the three L1–3 Restoration Anointed Focuses. Earlier #172–174 separately proved Returning Step and L3 Guided under true Soldier/Sentry damage. This slice combines **one real Anointed G0-paid G5 weapon attack**, **one real enemy G5/G4 injury**, and **one optional native G4 Returning Step** in a *single two-round scene*, accounting for each Focus's actual AP and Step opportunities.

## Exact source-backed 54-case policy set

[Native two-round role-choice runner](../../scripts/b05_anointed_native_g5_weapon_signature_choice_v0.py) produces **54 deterministic cases = three Restoration Focuses × L1/L2/L3 × authentic Soldier or prepared Firebound Sentry × three authored choices**. All use one actual player weapon hit (AH/AM **Dagger 2+d4 Piercing, Penetration 0**; AL **Sword 3+d6 Cut, Penetration 2**), one enemy source-paid physical hit, fixed d20=12, player damage face=4, enemy sword d6=2, Sentry Vigor die=1, genuine G1/G2 live wielded melee contact, G4 physical Armor/damage, G4.5 consumed G0 action, and exactly **two genuine recipient G0 Regeneration Steps**. Nothing grants a second weapon attack or invents extra regeneration.

| Policy | Enemy/weapon exposure | Optional native Returning Step |
|---|---|---|
| `weapon_only` | One paid Anointed ordinary G5 weapon hit and one identical enemy G5 injury | None; 2 Destiny remain |
| `weapon_signature` | Same two native hits and source dice | Exactly one Focus-specific HP packet; **High +2 HP / −2 recipient Vigor**, **Medium/Low +1 HP / −1 recipient Vigor**, no Destiny |
| `weapon_lesser` | Same two native hits and source dice | Same capped HP restoration, **0 additional recipient Vigor**, and **1 finite shared Destiny** |

The recipients explicitly decline discretionary natural HP/Repair regeneration (`RegenerationChoice()`) on each real Step, separating the sole source Signature healing from normal Vigor allocation. This is an authored comparison choice, **not** a recommendation to avoid ordinary regeneration or claim that players have no other legal options. Benefits are **unopposed** and consenting, with High/Medium explicitly declaring current visibility; **contested +8 Intrusion** and changing consent remain unresolved. All optional attack defenses are explicitly `take_hit`, not fabricated Guard/Dodge or unseen AI decisions.

## Focus-specific G0/AP opportunities are not interchangeable

- **High Restoration:** acts before Round-1 enemy strike and spends one genuine **30 AP Physical** action on its Dagger; the living allied patient is struck by the Soldier/Sentry afterward. On High's separate **Round-2** own turn, it spends a genuine **20 AP Projection** to apply Returning Step to that wounded living patient. The two payments never occupy the same turn; its Round-2 Projection follows, not precedes, the actual G5 wound.
- **Medium Restoration:** at its Round-1 own turn pays **24 AP General** to Invest one explicitly consenting ally, which precludes a second 24-AP physical attack in the same L1 30-AP turn. The source enemy hits that ally; Medium declares a **0 AP** pulse for the *ally's real Round-1 Regeneration Step*. The ordinary Dagger attack is therefore delayed until Medium's genuine **Round-2** turn and paid as **24 AP Physical** then. The no-Signature comparison instead attacks in Round 1. Both apply the same wound and end with exactly one weapon attack; this is a bounded action-timing comparison, not simultaneous healing/striking.
- **Low Restoration:** the enemy hits Low first in Round 1. Low can elect its already-embodied **0 AP self** Returning Step on its imminent native G4 Step, then spends **20 AP Physical** for its ordinary Sword attack **after** that Step on the same real turn. Low neither projects to an ally nor gains an extra G4 Step or attack from healing.

Every scene uses exact source actor and creature SHA256, fixed positions permitting legal adjacent G1/G2 contact, one source physical G5 player action, one source enemy paid G5 action, Focus-native healing event and remaining VP/Destiny. The [nine focused regression tests](../../tests/test_b05_anointed_native_g5_weapon_signature_choice_v0.py) compare all **54** same-exposure cases, cross-check each Focus's exact event order/AP and legal recipient, preserve the one ordinary damage contribution, separate Signature recipient-Vigor from finite Destiny, refuse forged source ledgers even when rehashed, and deny unsupported policy/level combinations. `attest_policy()` replays the entire native G0–G5 scene and checks the whole report, not a caller-maintained hash.

## Boundaries and next proof

This is one pre-authored attack, one paid reply, and one optional unopposed Signature in two rounds; **not certified** tactical balance, defense reactions, multi-target objectives, a win rate, adaptive AI, complete Focus role readiness, larger encounters, Wounds/Dying pressure, contested beneficial Intrusion or Mission/Destiny **noncombat** consequences. It does not exercise L3 Guided alongside the Signature; doing so needs a separately authenticated order and shared-pool treatment. It grants no general new weapon profile, spell or free AP.

**MVP readiness unchanged:** **12/12** structural pairings, **0/12** independent full Focus certificates, **0/6** strict MVP exit gates, B04–B07 open and original B06 **G0–G8** unchanged. The next certification work must demonstrate representative character progression and genuinely differentiated combat/noncombat decisions, not simply count these fixed encounters as complete Focus roles.
