# B06 G6-A — Hunter Native Combat and Pursuit v0

> **Executable bounded integration, not a certified diverse-party fight or challenge rating.** This milestone extends the merged G5 Soldier/Sentry attack and defense executor to the one source-authored 1×2 Hunter. It preserves the original Phase 3 4,096 one-round stops and numerical checksum without reclassifying historical stops.

## Sources and runtime

- Source combatant and profiles: [B06-EN-03](../../content/creatures/b06-hunter-of-the-woods.v0.json) (AT-04 Bite, AT-05 Horn Bash, AT-06 Pounce Bite, AT-07 Horn Drive).
- Original authority: [Hunter Bite/Horn](../rules/05-combat/hunter-bite-venom-and-horn-v0.md), [Pounce](../rules/05-combat/hunter-pounce-and-prey-takedown-v0.md), [footprints](../rules/05-combat/multi-square-creature-footprints-v0.md), [Prone](../rules/05-combat/special-movement-terrain-and-prone.md) and [Shove/Trip](../rules/05-combat/universal-maneuvers.md).
- Bounded executor: [`HunterCombat`](../../scripts/b06_hunter_g6a_v0.py), using existing [G0](../../scripts/b06_encounter_state_v0.py), [G1](../../scripts/b06_movement_v0.py), [G5](../../scripts/b06_soldier_sentry_g5_v0.py), [G4.5](../../scripts/b06_wound_continuation_v0.py), [G4](../../scripts/b06_damage_v0.py), and [G4.4](../../scripts/b06_hunter_venom_endurance_v0.py).
- Focused regressions: [G6-A tests](../../tests/test_b06_hunter_g6a_v0.py).

## Normal Hunter Bite and Horn Bash

`HunterCombat` inherits G5's source-verified ordinary Attack Sequence, d20/critical/Guard/Dodge and G4.5 proof pipeline. Exactly one Hunter profile AT-04 or AT-05 fits the source's 42 Turn AP / Physical24 economy per turn; anatomical frontal adjacency against one one-square PC is required **before** G0 AP and defense expenditure and rechecked at resolution. Side/rear contact does not become a free bite or horn attack. The shared G1 `threatens()` predicate also restricts **Hunter Movement and Standing Opportunities to the single immediately head-forward square** rather than the generic union of adjacency around both body cells. Leaving rear or side proximity therefore neither offers nor consumes a Hunter natural-attack Opportunity; turning/pivoting changes that one forward square naturally. The ordinary source G0 declaration remains reserved to the attached G5/G6 adapter; a direct call cannot pay untracked attacks.

- **AT-04 Bite:** one 3+d6 Piercing Pen1 hit. G4 owns effective Armor, actual residual Piercing, HP/wounds and death. When a Bite genuinely punctures and the target remains alive, G4.4 synchronously consumes the *latest* G4 hit to accept/ignore/prevent one Hunter toxin application; a natural resistance d20 must be supplied before a potentially puncturing hit rolls **only if** the one-instance toxin gate and an eligible preventive Ward do not already decide the exposure. Read-only preflight does not consume the active Moderate toxin (including a legacy TX-HM schedule) or the Ward; the actual G4.4 hit remains the sole source of ignored/prevented/accepted results. A lethal Bite that reaches the actual death threshold cannot schedule a resistance roll. An unpuncturing hit logs not-delivered without inventing a save. One real exposure schedules the printed deferred Full or Reduced milestones; neither the toxin nor the physical Bite resolves twice.
- **AT-05 Horn Bash:** one 2+d6 Crush Pen0 hit with ordinary G5 defenses/critical and G4 packets; never injects poison or Shoves automatically.
- Natural 1, Guard/Dodge misses and source-invalid contact create no G4 damage or venom. Previously paid slots remain subject to G5's canonical action/defense-index and turn-completion gates.

## Source-paid Hunter Pounce

`begin_pounce(hunter, target, route, defense=...)` uses **native G1**, not a second G0 Attack Sequence. G1 validates a front-facing run-up of at least three actual whole-footprint translations, terrain/blocked corners and 24-MP Charge allowance, commits **one Physical24** at the correct cutoff or at Bite contact, assigns **one** defender response, and records actual post-response contact. The G6 adapter then binds the exact paid G0 `action_committed`, G1 `g1_pounce_bite_committed`, G0 `defense_assigned`, and final G1 `g1_pounce_contact_result` events into an immutable-by-reference action identity recorded in the encounter ledger. A mutable returned receipt cannot substitute another paid action or defense. Pending Pounce payment blocks new own-turn movement, other AP expenditure and turn end until genuinely resolved; a canceled G1 contact is not a Bite hit.

`resolve_pounce(receipt, attack_face=..., ...)` resolves the source's single Bite d20+6 and one confirmation where applicable against the already paid defense, with the same Critical tiers and real G4 damage. A legal Bite hit passes its own G4 record synchronously through G4.4 before the post-hit provenance record. No second Bite/Guard/Response or second venom injection occurs. A Guard committed at contact is rechecked before the Pounce Bite roll: if a still-conscious defender loses the ready Guard or its instrument, leave the paid Pounce unresolved pending independently authorized defensive fallback, matching ordinary G5. If the defender becomes Dying, the already-paid Guard/Dodge falls back to Take Hit, as in G5. After **all** Bite/injection/wound effects, and only if forceful frontal contact and meaningful standing Prone susceptibility remain, an independently declared d20+4 vs d20+Strength/Agility+specific applicable penalty Balance contest determines Prone. Tie holds standing; a living Dying/incapable prey unable to resist follows the canonical Trip auto-success, with no extra balance rolls. Missed or fully blocked Bite may still produce a legal knockdown. **Post-Bite G4 predicted HP** determines whether contest dice and defender ability must be supplied *before* the G6 Bite roll log: a surviving, standing, positive-HP prey still requires both genuine Balance d20s; a resulting Dying prey falls Prone automatically without a Balance roll or ability choice; a dead prey receives no Balance resolution. This avoids fabricated unused dice while preserving precommitment for all actual contests. No Grapple, Pin, displacement, free damage or size modifier is added.

For this bounded adapter, active Balance uses the explicit zero-extra-Training profile from the Hunter fixture and source actor ability. Unverified training or special environmental modifiers, alternative source-impaired contests and reactive response paths remain unresolved rather than granting hidden bonuses.

## Horn Drive, Prone and pursuit

`horn_drive(...)` pays one actual Physical24 instead of Horn Bash and applies the source's non-damaging front-contact Shove (Hunter d20+Strength4 versus player d20+Strength+2 Hold Ground and real named muscular-Strength impairment). Successful pressure must strictly exceed resistance. Target must have a clear next front square **and** the complete rigid Hunter body must legally advance; otherwise neither displacement occurs. A declared ordinary Close-Contact Opportunity is offered through G0's bounded, explicitly declined response window. No damage, venom, free bash or automatic Prone is created. If the rigid Hunter advance would abandon a cell under an opposing **third party's** melee threat, the G6-A bounded executor rejects the contested Shove *before* spending Physical AP, consuming responses or changing positions. An authored G1-style third-party Movement Opportunity handler is required to advance in that geometry. A resisted Shove or blocked destination has no advancing body and therefore does not fabricate such an Opportunity. Chosen/opposed reactive counterattacks require a later, independently supported attack-response executor.

G1 now supports a bounded one-square `crawl_step`: normal Crawl is 2× step base, Cautious Crawl 3×, with ordinary destination terrain and response handling. `stand` spends 4 actual MP, breaks the movement segment and opens a G0 Standing Opportunity before clearing Prone. Existing G1 spatial and voluntary-movement checks remain authoritative. The bounded policy explicitly declines optional Opportunity attacks; if a PC actually chooses to take one, G6-B must supply a legal attack executor. Neither Crawl nor Stand mints extra MP/AP or defeats an occupied-square rule. **Prone during Pounce or aborted-Pounce Rapid Advance suspends that fast-movement pool**: while either mode is active, Crawl/Cautious Crawl is illegal, even with the source heading. Only Standing may use 4 MP from the suspended pool. On successful Standing during Pounce, reset the translated run-up count to zero and retain all prior AP payment and actual movement expenditure (including the 4 Stand MP toward future Charge cutoff); three **new** translated steps are required before Bite contact. An unsuccessful/interrupted Stand does not clear Prone or reset the run-up.

## Verified I3 witness and restrictions

`run_i3(seed=...)` provides one narrow, repeatable **two-round Hunter-versus-L3-A** authored open-corridor case. In round one, one G0-paid Hunter Bite naturally misses a committed Guard. The real party turn and Round End occur. In round two, one newly paid Bite punctures the same defender, G4 applies genuine damage, G4.4 schedules deferred accepted venom and the player spends recipient Vigor to regenerate at the next actual Step 2. The player then pays two actual G1 westward translations and reaches a scene-authored border exit; G4.5/G5 independently attest its living withdrawal with a real movement receipt. The scene report records native round, sources, attacks, toxins and exit. It is **not** a victory probability, full party-pack certificate or Hunter CR; the Hunter remains alive when the target withdraws.

The following remain **outside G6-A**: generic Hunter AI or target-switching policy, fully adjudicated actively chosen Movement/Standing/Close-Contact Opportunities, reactive Protective Intervene/Blink, nontrivial prepared Interceptions, arbitrary terrain hazards, large-prey Pounce, multi-square Grapple, unsupported caster spell choices, full 3–4-PC I3 combat, original historical Phase 3 trial reclassification, and end-to-end difficulty calibration.

## Codex review regressions

- Second puncturing normal Bite against a still-active source-accepted Moderate Hunter toxin: **physical damage applies, no second resistance d20, old milestones unchanged**.
- Pounce Bite against verified legacy Moderate TX-HM: **ignore re-exposure before resistance, preserve the existing short schedule**.
- Active preventive Venom Endurance Ward: **consume the Ward on the genuine delivered Bite, no unused resistance d20**.
- Active Hunter Pounce or converted aborted-Pounce Rapid Advance with Prone: **Crawl rejected before MP/position/event mutation**, while funded Stand completes.
- Pounce after Standing: **old three steps invalidated**, current MP/AP preserved, and a genuine new three-step approach still enables exactly one paid Bite.

## Additional Codex review regressions

- A living 1×2 Hunter has exactly one sourced frontal natural-attack threat, not a generic rear/side-body adjacency threat. Moving away from rear- or side-adjacent squares does not offer, debit or record its Opportunity; leaving the genuine head-forward square still does.
- A legal Pounce Bite that pushes a surviving prey to Dying may resolve its automatic knockdown **without any unused Balance d20s or ability declaration**; a lethal Bite leaves no post-damage Balance roll or Prone event.
- A living positive-HP prey after a missed or surviving Bite still needs both genuine Balance d20s **before** emitting the Pounce Bite roll log; an incomplete declaration leaves the already paid Pounce slot pending and does not mutate HP.

## Additional Codex review regressions

- Horn Drive with third-party armed PC threatening the Hunter's departing rear cell: independently verify the G1 threat and reject before AP, response, geometry or ledger mutation.
- Resisted Horn Drive and blocked destination in the same three-actor arrangement: retain their normal paid non-movement outcomes without inventing Movement Opportunities.
- Pounce Guard lost after commitment: verify both `ready_guard=False` and `guard_instrument=None` independently block the roll while preserving the paid pending attack; restoring a legal Guard permits the one genuine resolution.

## Codex review — exposure-key and full-footprint Standing safeguards

- Both native normal Bite (AT-04) and paid Pounce Bite (AT-06) preflight their deterministic `g6:bite:{seed}:{action_index}` / `g6:pounce:{seed}:{action_index}` toxin exposure IDs **before** the irreversible G4 hit, G5/G6 attack roll ledger, or G4.5 action consumption. G4.4 uses the **same shared read-only key validator** synchronously at toxin delivery. Real toxin identifiers from either unified exposures, legacy TX-HM or previous Hunter Bite delivery cannot alias a newly delivered Bite. A rejected alias preserves HP, Vigor, the pending action receipt and the existing exposure; retry cannot duplicate the damage. Lethal physical hits with no live venom delivery remain legal without consuming an unneeded exposure identity.
- A Standing creature is threatened if **any occupied footprint square** is within an opposing source's actual G1 threatened reach. The Standing Opportunity log contains each threatening actor once in sorted stable order, even if that actor reaches multiple cells. In particular, a Prone 1×2 Hunter Standing while only its rear is threatened records the source; this does not grant rear-facing Hunter *attacks*, whose head-only threat policy is unchanged.
- Regression coverage uses a legitimate preexisting legacy TX-HM exposure deliberately carrying each generated key and asserts that a failed normal/Pounce resolution is side-effect-free and repeatably rejected before any damage, plus rear-only, both-cell and distinct front/rear Standing threats.

## Codex review — muscle penalties and post-damage hook preflight

- Both Strength-based Hunter contest totals use the source's base pressure **plus the Hunter's own current** `muscular_strength` toxin modifier: Pounce Balance uses d20 + 4 + modifier; Horn Drive uses d20 + sourced Strength + modifier. The target's independently applicable modifier is unchanged. Equal totals remain a defender hold, never a Hunter win.
- G4.5 rejects a supplied non-callable `on_damage` hook **before** `apply_profile_hit()` or `seen_actions` mutation. An invalid hook cannot create an orphaned wound or use the real source action; after rejection, the same valid paid action can resolve once with a genuine callable hook. Valid post-damage callbacks still run synchronously after the G4 hit, before the G4.5 attestation.
- Regression witnesses: poison the Hunter with a *real* accepted TX-MY (-1 `muscular_strength`) between Pounce contact and Balance or before Horn Drive, and verify both clean wins become tied holds; reject malformed damage callbacks without touching HP, Vigor, injuries, source action identity or the ledger, then retry successfully.

## Validation

```sh
python -m unittest discover -s tests -p 'test_b06_hunter_g6a_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.validate_b06_footprints
python -m scripts.b06_hunter_phase3_report_v0 --json-out build/b06-phase3-census.json --markdown-out build/b06-phase3-census.md
```

Acceptance requires no failed new or historical regressions and a separate source-attested I3 result. Missing choices must remain unresolved rather than claimed as certified combat or earned death. New trial evidence may be added, but **never change** the frozen 32×128 original Phase 3 window counts or historical audit hash.
