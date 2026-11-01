# B04/B05/B06 — Alpha Cohort L1 Tactical Choice & Defensive Response Integration v0

> **Bounded native tactical evidence**, not a general encounter AI, player/GM play record, balance calibration, independent certification or new rule. Extends the merged [Alpha four-Focus L1 native Soldier encounter](b04-b05-b06-alpha-source-native-mixed-party-encounter-v0.md), preserving its source actors, unchanged original Soldier, G0–G5 authority and four authored withdrawal exits.

## Source-backed decisions and native outcomes

The `b04_b05_b06_alpha_l1_tactics_v0.py` module creates exactly one original L1 mixed Alpha encounter per declared policy, with complete explicit decisions for all four members and a pre-roll Soldier attack. The original #199 scenario and tests are unchanged. Choices are **validated before scene construction**: no omitted or arbitrary options, no attack confirmation from unimplemented natural 20, and no caller-declared hit or invented response capability.

| Choice | Supported authored options | Source authority and limitation |
|---|---|---|
| Low Priest response to Soldier | **Take Hit / Guard / Dodge** | Original G0 defense assigned **before** actual G5 melee roll. Guard requires real instrument/remaining capacity and costs one Guard; Dodge increments native Dodge Pressure by 2; Take Hit consumes neither. Neither becomes a free reaction/AP credit. |
| Soldier d20 | Explicit 1–19 | Actual G5 compares source melee bonus against the **assigned** Guard/Dodge defense value and pays real G4 dice **only on a hit**. Natural 20/confirmation intentionally fails closed in this bounded policy. |
| Medium Anointed | **Invest Priest / Hold** | Real source 24-AP General Investment, consent assumed only in the explicitly authored policy. A pulse is declared only on the Priest's genuine next G4 Step after an actual Soldier injury and with remaining Vigor; no phantom healing for a missed attack or an uninvested target. |
| Low Priest | **Chosen Rite / Hold** | A and B use their complete selected L1 Life sources, exact Chosen host, 30 Projection AP and original Committed/Spent VP. Held turn grants no magic. |
| High Gifted | **Joy Flame / Hold** | Native Emotion Establishment followed by legal source-paid L1 Thrown Flame (fixed natural-1 demonstration). No fictional Overwhelming, Instability or free surge. |
| High Scholar | **Flame / Hold** | Native source-paid L1 Thrown Flame (fixed natural-1 demonstration), or forgo attack. Both use the original F source and G3/VP accounting. |
| Round-two stance | **Cautious Withdraw / Hold Position** | Original G1 actual paid movement and G5 scene-authored exits for all four, **or** a genuinely complete round with zero exits and an **ongoing unresolved engagement**; no invented defeat, victory or fake terminal certificate. |

This is a narrow **predeclared tactical source bridge**, not live free-form combat or automated adjudication of unknown alternative GM choices. Actual contested consent, alternate targets, nontrivial Interception/Opportunity, prone capability, risk amplification, critical confirmations, counterfire and full pursuit remain outside this module and must retain the existing native explicit gates.

## Five source-tested branches

| Policy | Defense / first Soldier die | Party option variation | Result |
|---|---|---|---|
| `protected_guard` | Guard, d20=2 | All four choose their existing paid support/Flame actions | Real Guard debit; no Priest injury; **no** Medium pulse; party withdrawal |
| `evasive_dodge` | Dodge, d20=2 | Scholar holds, other three choose native actions | Real Dodge Pressure +2; no injury, no pulse; withdrawal |
| `wounded_no_investment` | Take Hit, d20=12 | Anointed and Gifted hold; Priest Rite + Scholar Flame | Source G4 injury, no Investment/pulse, withdrawal with retained HP attrition |
| `wounded_with_step` | Take Hit, d20=12 | Original four paid source expressions | Native recipient pulse with HP and Vigor delta; withdrawal |
| `defend_position` | Take Hit, d20=12 | Priest and Scholar hold; other two act | Two rounds completed, no exit certificate, **ongoing engagement not a terminal** |

Each policy is run for both **A and B** complete, selected Low Priest source sheets. The mixed-party actors remain **Priest/Low, Scholar/High, Gifted/High and Anointed/Medium**. Soldier source `B06-EN-02` remains the original L3-equivalent benchmark at L1; **difficulty is not normalized**. No physical-only A/B proxy attack profiles are granted.

The policy output preserves the original native actor/source SHA-256 fingerprints, the actual defense assignment (Guard remaining and Dodge Pressure), native G5 roll and damage receipts, G3 source actions, available/committed/spent VP, G4 HP/Vigor changes, original G1 movement and terminal exits, and a source-bound SHA256 ledger. A caller changing the policy, defender response, AP costs, outcome, ledger or terminal fails the exact source replay attestation, including after a new ledger digest is calculated.

## Run and verify

```bash
python -m unittest discover -s tests -p 'test_b04_b05_b06_alpha_l1_tactics_v0.py' -v
python -m scripts.b04_b05_b06_alpha_l1_tactics_v0 --policy protected_guard --variant A
python -m scripts.b04_b05_b06_alpha_l1_tactics_v0 --policy evasive_dodge --variant B
python -m scripts.b04_b05_b06_alpha_l1_tactics_v0 --policy wounded_with_step --variant A
python -m scripts.b04_b05_b06_alpha_l1_tactics_v0 --policy defend_position --variant B
python -m unittest discover -s tests -v
```

All focused tests must reject unsupported declaration fields, natural-20 unsupported confirmation, fake outcomes, borrowed melee authority, illegal Guard/Prone Dodge prior to paying G0 attack AP, and simulated terminal certificates for held-position rounds.

## Human pilot and MVP acceptance boundary

The first-cohort [evidence intake](b04-b05-b06-b07-first-cohort-pilot-execution-evidence-v0.md) remains UNOBSERVED. Machine-fixed dice and author policy outcomes are **not player choices or independent GM verdicts** and must not populate the human C1–C7 review slots. Real participant alternatives require their own initial source sheet, declared dice/defenses, GM clock context and independently reviewable original receipts. This PR improves the **L1 choice/defense execution surface only**. L2–L3 native mixed Alpha encounters and authentic pilot sessions remain separate work.

MVP status remains **12/12 structural** Focuses, **0/12** independently full-play-certified, **0/6** strict accepted gates and **0** authenticated real human sessions; no additional B06 G-stage or empirical Soldier/Hunter balance claim.
