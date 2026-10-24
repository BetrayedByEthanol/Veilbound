# B04/B05 — Three-Focus Priest Life Extended Attrition and Tactical Balance v0

**Scope:** evidence-first, source-native High/Medium/Low Priest **four/eight-round requested attrition horizons** with real G0 time, G1 MP and contact, G3 effects, G4 HP/Vigor and regeneration, G4.5 authoritative paid-hit provenance, and G5 declared melee plus ordinary Guard/Dodge. This is a **bounded comparative audit, not final three-Focus balance certification**, a calibrated win-rate sample, or permission to modify AP/VP/damage numbers.

## Native population and fixed policy strata

The roster is unchanged from the merged two-round comparison: separate **H** High Priest, **M** Medium Priest, **A** Low Priest Chosen Guided, and **B** Low Priest Chosen Shelter build; each is compared against its *own* role/level/opponent/pressure/tactic/horizon baseline. The enemy is always a genuine **Soldier B06-EN-02** or **prepared Sentry B06-EN-01**. Every encounter uses their original source armor, HP/Vigor, speed, guard instruments, action prices and finite effects; no cross-Focus equalized numerical surrogate is introduced.

- Priest starts at (2,2), native foe at (3,2); initiative Priest 30 then foe 20; visible adjacent contact, no fabricated opportunity attacks.
- The original Soldier sword B06-AT-03 / prepared Sentry B06-AT-02 is native G5 declared, AP paid and resolved against one explicitly assigned defense each live foe turn. Attack d20 **12**. **Light** damage d6 **1** and **heavy** d6 **4** are two fixed authored dice scenarios, *not distributions*. Sentry reserved sword applies source Direct Vigor with d6 **4**; wound location d20 **8** is supplied precommitted only when a genuine hit may require it.
- Horizons are **4** and **8** requested rounds. An incapacitated Priest ends the scenario at the *actual completed-round boundary*: no phantom future turns, attacks, MP or survival Steps. Report **rounds actually completed**, paid attack attempts, hit/miss outcomes and damage separately. A Guard/Dodge **miss** spends native attack AP and assigned defense resources; it creates no hit packet or imaginary G4 damage. This is a deliberate distinction from the prior v0's forced two Take Hits.
- **Three explicit tactical choices:** Take Hit in place; Guard with original ready instrument/capacity; or **Dodge plus one real G1 cautious lateral step every even-numbered still-conscious Priest turn**, alternating (2,2) and (2,3) while retaining actual contact. The step pays MP, declines eligible Opportunities without spoofing another actor's attack, and does not pretend to confer an unmodeled cover or flanking modifier.
- One authentic Step 2 per actual Priest/foe turn; Priest allocates the maximum *currently legal* HP restoration with available Vigor/throughput and explicit Dying-survival cancellation if needed. No virtual regeneration before damage, replenished VP, six-hour recovery or wound repair shortcut.

## Real Life access

| Role | Baseline and supported policy | AP/VP sources |
|---|---|---|
| H — High | baseline, maintained prepared Guided, maintained prepared Shelter, paid Basic Heal Primary on eligible even turns | 20 AP per prepared Projection; normal 2 Committed Guided / 2 Committed + 1 Spent Shelter; 2 Spent VP per real Basic Heal |
| M — Medium | baseline, maintained Consecration Guided/Shelter, eligible paid Basic Heal Primary on even turns | 24 AP per Consecration; 2 Committed Guided / 2 Committed + 1 Spent Shelter; actual existing G4 paid Medium Basic Heal |
| A — Low Guided | baseline, Chosen Guided, L3 Chosen plus actual Held Renewal opportunities after genuine later Step 2 | 30 AP Projection, 1 Committed host; L3 may Spend 1 VP per actually armed Held Renewal if unused Step throughput and host remain |
| B — Low Shelter | baseline, Chosen Shelter, L3 Chosen plus genuine Vital Interposition opportunities | 30 AP Projection, 1 Committed + 1 Spent host; L3 may Spend 1 more VP on a legal own-turn arm with live B8; host can expire and refund Committed VP |

No magical action is required when the active caster is incapacitated or has insufficient funds; no pseudo-AP or discount is created. L3 Exaltation is never available at L1–2. High Invocation/Open Prayer and Medium external Intercession were verified independently in earlier milestones, but **cannot be inserted as equal-priced self-defense options**. Low Chosen Rites remain self-only, not transferable onto the Scholar ally. These limitations are deliberately preserved.

## Evidence, attestation and interpretation

The matrix comprises **912 exact source-native cases**, crossing H/M/A/B, L1–3, Soldier/Sentry, 4/8 requested rounds, light/heavy damage, Take Hit/Guard/cautious Dodge, and each level-legal original Focus policy. Each result retains original source digests, a replay-authenticated full ledger SHA-256, the number of *actually completed* rounds and live paid attacks, native hit/miss/packet counts, final HP/Vigor and VP partitions, genuine Regen and external-heal receipts, finite effects/refunds, Dying/wounds/death, paid Projection AP, and actual lateral MP spent.

Each cell is paired with exactly the *same role/level/opponent/horizon/pressure/tactic* no-magic baseline. Baseline deltas report HP, Vigor, wound, prevented Direct Vigor, Low Vital HP prevention, Spent/Committed VP and paid AP, as well as **actual round-completion difference**. When one policy exits early and the other continues, that difference remains explicit; results must not be normalized by guessed future hits or counted as a measured win rate.

### Candidate balance interpretation (not tuning decisions)

- High's lower prepared AP and broader practical heal access create potential action flexibility, conditional on real VP and ability to use the Projection window. Not a measured Focus advantage unless repeated in more varied threats.
- Medium's 24-AP Consecration vs High's 20 and Low's 30 is measurable; the unique Intercession Reaction path needs a future, *external-recipient*, source-legal matched scenario rather than an invented self-Reaction shortcut.
- Low Chosen spends less Committed VP but reserves a higher AP action and gains its L3 self-Exaltation niche. B's finite Shelter may exhaust, returning Committed (never Spent) VP. A's Held Renewal must consume genuinely unused throughput from the actual later Step 2, not a synthetic regeneration packet.
- Guard/Dodge can prevent an incoming hit altogether, changing the marginal value of healing and mitigation. Movement in this bounded clear map is a real resource expense and eligibility test, *not* an assumed defensive bonus. The heavy and light d6 witnesses deliberately expose this dependency without sampling enemy accuracy.
- A participant's early incapacitation is observable source survival evidence, but no GM victory condition, opponent adaptation or statistically meaningful win-rate is defined.

**Out of scope and left for later separate approval:** numerical Focus rebalancing, multi-enemy target selection, Hunter pounce/venom, genuine contested magic, generic source H/M/A/B offensive attacks, low external support, probabilistic rolls, enemy AI and cross-Focus economic utility weights. `three_focus_balance_certified=false`; `numerical_tuning_approved=false` on all reports.

## Reproduce

```bash
python -m unittest tests.test_b05_three_focus_life_extended_attrition_v0 -v
python -m unittest discover -s tests -v
python -m scripts.b05_three_focus_life_extended_attrition_v0 --seed 0
python -m scripts.b05_three_focus_life_extended_attrition_v0 --role B --level 3 --opponent sentry_prepared --policy exaltation --horizon 8 --pressure heavy --tactic take_hit
```

The next evidence gate, **after review**, is a source-legal multi-recipient/intercession stress study and varied tactical dynamics; changing numbers remains a separate explicit balance decision.
