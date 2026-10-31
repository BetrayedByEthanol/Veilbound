# B04/B05 — Focus-Specific Combat & Noncombat Evidence v0

> **Bounded automated source evidence, not independent full-Focus certification or actual human/GM play.** This evidence pack instantiates the **12 structural Archetype × Focus pairings at each L1–3 level**, reproduces two genuine G0–G5 authored combat policies per pairing/level and distinguishes real noncombat utility from unexecuted skill access. See the [PR #184 twelve-Focus certification protocol](b04-b07-independent-twelve-focus-certification-protocol-pilot-roster-v0.md) and [MVP register](b04-b07-mvp-acceptance-register-refresh-v0.md). No new gameplay rule, tier expression, G-stage, skill roll, social DC, fictional GM judgement or playtest outcome is authorized.

## What this PR actually demonstrates

| Evidence type | Source-backed v0 evidence | What remains unproved |
|---|---|---|
| **Combat** | **36 pairing × level rows, each with two distinct authentic native combat policy ledgers**: 72 bounded G0–G5 witnesses, including separate paid High Gifted Flame and Low Gifted Guard integrations | A fixed-policy outcome is not a human tactical choice, full terminal encounter, role ranking or sampled win rate |
| **General noncombat** | **24 pairing-level source checks** across eight non-Anointed/non-Low-Priest pairings: two distinct nonzero Learned Discipline ranks are read from current source sheets, with true source fingerprint | An authored skill and a proposed alternative do **not** resolve a genuine GM check, yield a social/exploration consequence or verify usable magic |
| **Anointed noncombat** | **Nine AH/AM/AL × L1–3** real source-native G4.2 exploration/partial-clock policy replays in addition to genuine training choices | The scripted `clock_partial` does **not** claim a real GM Mission verdict, observed agency, consenting roleplay, story milestone or level gain |
| **Low Priest noncombat** | **Three blocked pairing-level slots**, explicitly identifying A/B G0 *physical* proxies and authored Rite/Exaltation source record | No complete independently selected/observed Low Priest skill and social/exploration sheet; cannot infer utility from a native physical proxy |
| **Certification** | **12 structural pairings** and explicit choice/weakness evidence candidates | **0/12** independent full-Focus certificates, **0/6** strict MVP exits, **0** verified real human/GM sessions; B04/B05/B06/B07 remain open |

The code records actual native ledger SHA-256, number of events, event-kind identities, policy source module and existing source metrics. It must not fabricate an action from a summary, count raw ledgers as independent played scenes, or silently convert a damage/VP comparison into a CR. Same physical **Priest/Low A/B** variants count **once** toward 12 Focuses; the two variants differ and are **not** legal in-session reconfiguration for one actor.

## Runnable execution and review

```bash
python -m scripts.b04_b05_focus_combat_noncombat_evidence_v0 --pairing Gifted/Low --level 2
python -m scripts.b04_b05_focus_combat_noncombat_evidence_v0 --pairing Anointed/Medium --level 3
python -m scripts.b04_b05_focus_combat_noncombat_evidence_v0 > build/b04-b05-focus-evidence-v0.json
python -m unittest discover -s tests -p 'test_b04_b05_focus_combat_noncombat_evidence_v0.py' -v
```

Each row contains:

- **Selected native combat witness** and an **alternative native combat witness**, both with genuine native event ledgers attested by a recomputed digest. These are **author-selected demonstration policies**, never claims about a player's chosen action.
- **Noncombat evidence** distinguishing `SOURCE_TRAINING_ACCESS_ONLY_GM_UNRESOLVED`, `BOUNDED_NATIVE_G42_CLOCK_NOT_EXTERNAL_GM_VERDICT` and `LOW_PRIEST_A_B_PROXY_NO_COMPLETE_NONCOMBAT_SHEET`.
- **Explicit boundaries:** actual human choices **0**, external verified sessions **0**, full-Focus certificates **false** and strict MVP exit gates **0**.

The evidence pack uses [the #181/#182 independent source provenance](b04-b07-independent-l1-l3-build-progression-audit-v0.md) via the [#184 roster](../../scripts/b04_b07_twelve_focus_certification_protocol_v0.py), rather than trusting the output of source `verify()` or an invented new character. It preserves actual native G0/G1/G2/G3/G4/G5 mechanics and G4.2 source world clock. Captured ledgers are intentionally **bounded** and are not a cross-session state history.

## Twelve-Focus combat comparison ledger and actual noncombat gaps

| Pairing | Bounded native selected vs alternative | Noncombat source evidence | Missing Focus-specific positive/countercase in representative play |
|---|---|---|---|
| Priest/High | Prepared Guided vs baseline under actual Soldier G5 pressure; G0/G3/G4 payments | Real trained skill options only | Prepared vs Open Invocation and L3 Open Prayer decision under field hazard/time; one true GM consequence |
| Priest/Medium | Four-round `triage` vs `baseline` with actual Soldier and source G3/G4 | Real trained skill options only | One-host Consecration vs L3 Intercession Reaction opportunity cost; real Medicine/travel decision |
| Priest/Low | Native A/Rite vs B/Rite physical proxy alternatives (distinct build variants) | **Blocker: no independently reviewed complete skill sheet** | Complete Low Priest build, physical/Veil choice, self-host expiry and meaningful noncombat application |
| Scholar/High | Known authored Thrown Flame T1 vs `no_spell` Soldier response | Real trained skill options only | Composite preparation/casting tradeoff and actual technical investigation check |
| Scholar/Medium | Native Earth/Life Inward Stone vs baseline G5 | Real trained skill options only | #148 sequential live Opportunity replay alongside real technical/scouting decision |
| Scholar/Low | Native self Stone Embodiment vs baseline G5 | Real trained skill options only | Real six-hour preparation and exploration, hostile pressure while switching self-host |
| Gifted/High | Actual source-native Joy Thrown Flame with paid **Surge Precision** vs ordinary paid cast | Real trained skill options only | Emotion Window/Instability and unauthored off-Aspect utility rejection in genuine noncombat scene |
| Gifted/Medium | Native Fear Ward vs dormant Ward under Soldier G4/G5 | Real trained skill options only | Trust third-party protection/retune tradeoff, observable noncombat emotional utility |
| Gifted/Low | Real G0 paid Rooted Guard **18 vs 17** alters Soldier G5 **miss vs hit** | Real trained skill options only | Real G1 cautious/difficult Unbound Step −1 MP in a noncombat travel choice (native isolated movement exists #180) |
| Anointed/High | Two-round genuine weapon+Returning Step vs weapon only | Actual G4.2 exploration clock **without GM recognition** | External consent/Mission event and the true Projection vs other support choice |
| Anointed/Medium | Two-round genuine Dagger+one-Vessel Returning Step vs weapon only | Actual G4.2 exploration clock **without GM recognition** | Independent GM and consenting recipient, one-Vessel/24-AP tradeoff in a full scene |
| Anointed/Low | Two-round genuine Sword+self Returning Step vs weapon only | Actual G4.2 exploration clock **without GM recognition** | Self-hosted Signature and six-hour Destiny in real noncombat/mission choice |

**The bounded 72-witness count is not a quantity goal or MVP gate.** Source-specific unresolved branches must remain blocked rather than being replaced by made-up decisions. This is evidence toward **C1/C3/C5**; it does not provide independent **C4/C6/C7** human decisions, GM rulings or actual milestone awards.

## Regression and downstream acceptance

The regression suite replays each pairing/level source policy, checks original native `action_committed` events and distinct policy digests, authentic High Gifted paid Surge and Low Gifted paid +1 Guard defense, source-profile Training alternatives, real G4.2 Anointed clocks, and strict no-certification boundaries. An omitted or nonsensical level/policy fails closed.

**Still required for B04/B05 closure:** full independently reviewed L1–3 choices, native encounter alternatives and genuine noncombat source execution under GM adjudication; Low Priest must get a complete legal utility/source sheet, not a physical proxy. The next tasks should deliver Focus-specific **noncombat scene resolution adapters** (use an existing canonical check procedure, not invented social skills), then real mixed-party/GM encounters and witnessed player/GM choices. Any unresolved Intrusion, stealth or environmental effect becomes a concrete conditional implementation issue only when a selected scenario requires it.

**Unchanged MVP:** **12/12** structural pairings, **0/12** independent full Focus certificates, **0/6** accepted exits, **3/7** definition blockers closed; original B06 G0–G8 unchanged, Hunter CR unrated. No real 3–5-session pilot was conducted by this source-generated report.
