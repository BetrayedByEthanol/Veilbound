# B06 G6-A — Hunter Native Combat and Pursuit v0

> **Executable bounded integration, not a certified diverse-party fight or challenge rating.** This milestone extends the merged G5 Soldier/Sentry attack and defense executor to the one source-authored 1×2 Hunter. It preserves the original Phase 3 4,096 one-round stops and numerical checksum without reclassifying historical stops.

## Sources and runtime

- Source combatant and profiles: [B06-EN-03](../../content/creatures/b06-hunter-of-the-woods.v0.json) (AT-04 Bite, AT-05 Horn Bash, AT-06 Pounce Bite, AT-07 Horn Drive).
- Original authority: [Hunter Bite/Horn](../rules/05-combat/hunter-bite-venom-and-horn-v0.md), [Pounce](../rules/05-combat/hunter-pounce-and-prey-takedown-v0.md), [footprints](../rules/05-combat/multi-square-creature-footprints-v0.md), [Prone](../rules/05-combat/special-movement-terrain-and-prone.md) and [Shove/Trip](../rules/05-combat/universal-maneuvers.md).
- Bounded executor: [`HunterCombat`](../../scripts/b06_hunter_g6a_v0.py), using existing [G0](../../scripts/b06_encounter_state_v0.py), [G1](../../scripts/b06_movement_v0.py), [G5](../../scripts/b06_soldier_sentry_g5_v0.py), [G4.5](../../scripts/b06_wound_continuation_v0.py), [G4](../../scripts/b06_damage_v0.py), and [G4.4](../../scripts/b06_hunter_venom_endurance_v0.py).
- Focused regressions: [G6-A tests](../../tests/test_b06_hunter_g6a_v0.py).

## Normal Hunter Bite and Horn Bash

`HunterCombat` inherits G5's source-verified ordinary Attack Sequence, d20/critical/Guard/Dodge and G4.5 proof pipeline. Exactly one Hunter profile AT-04 or AT-05 fits the source's 42 Turn AP / Physical24 economy per turn; anatomical frontal adjacency against one one-square PC is required **before** G0 AP and defense expenditure and rechecked at resolution. Side/rear contact does not become a free bite or horn attack. The ordinary source G0 declaration remains reserved to the attached G5/G6 adapter; a direct call cannot pay untracked attacks.

- **AT-04 Bite:** one 3+d6 Piercing Pen1 hit. G4 owns effective Armor, actual residual Piercing, HP/wounds and death. When a Bite genuinely punctures and the target remains alive, G4.4 synchronously consumes the *latest* G4 hit to accept/ignore/prevent one Hunter toxin application; a natural resistance d20 must be supplied before a potentially puncturing hit rolls **only if** the one-instance toxin gate and an eligible preventive Ward do not already decide the exposure. Read-only preflight does not consume the active Moderate toxin (including a legacy TX-HM schedule) or the Ward; the actual G4.4 hit remains the sole source of ignored/prevented/accepted results. A lethal Bite that reaches the actual death threshold cannot schedule a resistance roll. An unpuncturing hit logs not-delivered without inventing a save. One real exposure schedules the printed deferred Full or Reduced milestones; neither the toxin nor the physical Bite resolves twice.
- **AT-05 Horn Bash:** one 2+d6 Crush Pen0 hit with ordinary G5 defenses/critical and G4 packets; never injects poison or Shoves automatically.
- Natural 1, Guard/Dodge misses and source-invalid contact create no G4 damage or venom. Previously paid slots remain subject to G5's canonical action/defense-index and turn-completion gates.

## Source-paid Hunter Pounce

`begin_pounce(hunter, target, route, defense=...)` uses **native G1**, not a second G0 Attack Sequence. G1 validates a front-facing run-up of at least three actual whole-footprint translations, terrain/blocked corners and 24-MP Charge allowance, commits **one Physical24** at the correct cutoff or at Bite contact, assigns **one** defender response, and records actual post-response contact. The G6 adapter then binds the exact paid G0 `action_committed`, G1 `g1_pounce_bite_committed`, G0 `defense_assigned`, and final G1 `g1_pounce_contact_result` events into an immutable-by-reference action identity recorded in the encounter ledger. A mutable returned receipt cannot substitute another paid action or defense. Pending Pounce payment blocks new own-turn movement, other AP expenditure and turn end until genuinely resolved; a canceled G1 contact is not a Bite hit.

`resolve_pounce(receipt, attack_face=..., ...)` resolves the source's single Bite d20+6 and one confirmation where applicable against the already paid defense, with the same Critical tiers and real G4 damage. A legal Bite hit passes its own G4 record synchronously through G4.4 before the post-hit provenance record. No second Bite/Guard/Response or second venom injection occurs. After **all** Bite/injection/wound effects, and only if forceful frontal contact and meaningful standing Prone susceptibility remain, an independently declared d20+4 vs d20+Strength/Agility+specific applicable penalty Balance contest determines Prone. Tie holds standing; a living Dying/incapable prey unable to resist follows the canonical Trip auto-success, with no extra balance rolls. Missed or fully blocked Bite may still produce a legal knockdown. No Grapple, Pin, displacement, free damage or size modifier is added.

For this bounded adapter, active Balance uses the explicit zero-extra-Training profile from the Hunter fixture and source actor ability. Unverified training or special environmental modifiers, alternative source-impaired contests and reactive response paths remain unresolved rather than granting hidden bonuses.

## Horn Drive, Prone and pursuit

`horn_drive(...)` pays one actual Physical24 instead of Horn Bash and applies the source's non-damaging front-contact Shove (Hunter d20+Strength4 versus player d20+Strength+2 Hold Ground and real named muscular-Strength impairment). Successful pressure must strictly exceed resistance. Target must have a clear next front square **and** the complete rigid Hunter body must legally advance; otherwise neither displacement occurs. A declared ordinary Close-Contact Opportunity is offered through G0's bounded, explicitly declined response window. No damage, venom, free bash or automatic Prone is created. Chosen/opposed reactive counterattacks require a later, independently supported attack-response executor.

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

## Validation

```sh
python -m unittest discover -s tests -p 'test_b06_hunter_g6a_v0.py' -v
python -m unittest discover -s tests -v
python -m scripts.validate_b06_footprints
python -m scripts.b06_hunter_phase3_report_v0 --json-out build/b06-phase3-census.json --markdown-out build/b06-phase3-census.md
```

Acceptance requires no failed new or historical regressions and a separate source-attested I3 result. Missing choices must remain unresolved rather than claimed as certified combat or earned death. New trial evidence may be added, but **never change** the frozen 32×128 original Phase 3 window counts or historical audit hash.
