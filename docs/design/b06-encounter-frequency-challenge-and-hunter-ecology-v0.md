# B06 — Encounter Frequency, Creature Challenge and Encounter Difficulty v0

> **LOCK CANDIDATE — definitions and assessment procedure, not a numerical CR/XP budget.** The distinction between **encounter frequency**, **creature challenge rating**, **encounter size and composition**, **encounter difficulty**, and **encounter role** can be adopted now. **Numeric challenge values, party threat budgets, probability rolls, and difficulty cutoffs remain UNCALIBRATED** until opposed B06 encounters and exploratory/social scenes are actually run. The [14-entry bestiary](../../content/creatures/b06-initial-bestiary-v0.json) is a status/index, not a complete stat block or fixed encounter generator.

## 1. Five independent quantities

| Concept | Question answered | What it must NOT imply |
|---|---|---|
| **Encounter frequency / encounter rate** | How often does this creature or situation arise **in a specified place, season, time, route and activity**, and how likely is contact? | Not combat difficulty, not population density by default, not a mandatory random-encounter roll, not aggression or a forced fight |
| **Creature challenge rating (CR)** | What is the creature's **intrinsic combat challenge under an explicitly stated standard reference setup**, estimated from tested offensive, defensive, mobility, control and recovery capabilities? | Not merely its benchmark/build level, story importance, rarity, ecological rank or an automatically valid scalar for every party |
| **Creature encounter role** | What is it designed to do? **ordinary humanoid**, **specialist**, **elite predator**, **boss**, or **noncombat agent** are examples of qualitative roles | Role alone does not add HP, additional attacks, immune traits, Reactions, GM difficulty bonuses or numerical CR |
| **Encounter size / composition** | **How many player characters at what levels, how many opponents and of which types**, and what other participants/objectives are present? | Not a synonym for map footprint (1×2 squares), challenge rating or encounter frequency; 2 enemies versus 4 PCs can be unlike 1 enemy versus 2 PCs despite similar totals |
| **Encounter difficulty** | How dangerous or costly is the **specific scenario for this particular party** (including starting resources, terrain, warning, initiative, alternate solutions, retreat, allies and reinforcements)? | Not a fixed creature stat or proof that all contact turns into combat |

**Terminology:** Use **Encounter Frequency** for the ecological/social likelihood dimension, to avoid confusing it with **Encounter Difficulty** or the creature's **Challenge Rating**. Call `benchmark_level` a stat calibration input, never `CR`. A multi-square **footprint** is also distinct from the **number of opponents** in an encounter.

## 2. Frequency is contextual, and contact does not mean combat

A frequency assessment names a region/context, season/time, prey or patrol conditions, and **why** contact might occur. A standard soldier might be **regularly present at a staffed town gate**, encountered on an open road as a patrol, or absent deep in wilderness. Those are different contexts for the **same stat block**.

A Hunter is an **apex ambush predator of forested territory**. Evidence such as dens, excavated earth, displaced roots, gouged trees, tracks, scavenged remains or a startled herd can create **indirect encounters** before anyone sees it. It may avoid an alert group rather than fight. Rutting season, territorial defense, hunger, prey availability, den proximity and existing injury can change behavior; no global numerical spawn probability is justified yet.

Record **contact/observation**, **possible interaction**, and **hostile engagement** separately. A patrol at a gate commonly produces an interaction, not a melee encounter; a Hunter might stalk, threaten, withdraw or fight. **No default automatic aggression roll.**

## 3. A rating must be earned by controlled encounter evidence

Until an actual calibration suite exists:

- Creature `challenge_rating` is **`unrated`** (no numeric CR or challenge points). The role label may still be `standard` or `elite`.
- A scenario may carry an **untested intended difficulty** label (e.g. **routine/standard/dangerous/severe**) to select what to playtest, never to claim verified balance.
- Record the assumed **PC count**, **each PC level/build**, **enemy count/type**, equipment/resources/VP/Vigor, visibility/cover, forest density, first detection, initiative, starting distance, alternate objectives and retreat feasibility.
- Measure actual hit/defense and action sequences, whether a character becomes Dying, damage and Vigor/VP spent, wound/poison effects, victory/escape/surrender, durations and between-encounter recovery. Repeat variants against different Focus builds and initial conditions.
- A larger group does not automatically equal its members' sum: concentrated offense, guard exhaustion, multiattacks, healing, positioning, terrain and enemy target selection can be strongly **nonlinear**. No universally valid exchange formula between creature count, party size and party level is locked.
- Only after representative tested outcomes should a **numerical creature CR scale**, **encounter difficulty thresholds** or **party threat-point budget** be proposed for locking. Any early "4 TP Soldier / 12 TP Hunter" ideas are explicitly **historical illustration, not accepted canon**.

A scenario with a dangerous combatant may still be an **easy social interaction**. Difficulty of negotiation, evasion, tracking or concealment must not be auto-derived from combat CR.

## 4. Initial B06 example matrix — all intended matchups UNTESTED

| Creature / scene | Party | Enemies | Intended role/difficulty | Context and unvalidated assumptions |
|---|---|---:|---|---|
| **Ordinary Human Soldier** | 1 × L3 | 1 | Standard combat baseline | No magical VP or Focus for soldier; open/neutral terrain and full resources |
| **Ordinary Human Soldiers** | 4 × L1 | 2 | Standard **candidate**, may differ materially from solo test | Group tactics, separate Guards/turns and PC low-level fragility must be tested |
| **Ordinary Human Soldier at gate** | Any suitable party | 1+, plus civilians/guards | **Social/exploration interaction** by default | Gate checks, patrol, escort, road interaction; reinforcements/context can increase stakes without buffing soldier stats |
| **Hunter of the Woods, warned party** | 3–4 × L2–3 | 1 | **Dangerous elite test** | Forest travel, credible detection/warning, escape options; actual Pounce/venom rules still unauthored |
| **Hunter, successful forest ambush** | 3–4 × L2–3 | 1 | **Severe risk test**, not guaranteed death | May open with Pounce/bite; test Awareness, initial separation, response opportunities, target concentration and withdrawal |
| **Hunter's den or tracks** | Any appropriate party | 0 or 1 present | Exploration / avoid / investigate / negotiate route | Territorial evidence and den-hazard setting, no mandatory combat or repeated roll-until-hostility |

**Creature role and scenario danger differ:** the Soldier is an **ordinary humanoid and flexible social NPC**. The Hunter is an **elite ambush predator**. Neither has an evidenced numeric CR yet. The Hunter's projected lethal bite and forest tactics cannot simply be assigned a 12-point budget without reproducing outcomes against both Life Low Priest builds and other party mixes.

## 5. Hunter ecology — content identity lock, mechanics explicitly deferred

The Hunter is a **living natural beast**, larger/bulkier than a bear, with a wolf-like head, a prominent horn, powerful forelegs/hindlegs and a **venomous puncturing bite**, normally inhabiting wooded territories. Its proposed ordinary footprint is **1×2 squares**, governed by [Multi-Square Creature Footprints v0](../rules/05-combat/multi-square-creature-footprints-v0.md).

**Primary hunt:** stalk → explosive Pounce combining locomotion and an actual bite opportunity → if the prey is brought down, finish the hunt; **if takedown fails but the bite genuinely punctures**, envenomation can still occur. Bite success must be **mechanically independent from takedown success** at the relevant authored resolution points. It can withdraw, avoid injury, conserve energy, follow tracks/scent, and attack again when prey is vulnerable. It can take down deer/elk and, with an appropriate tactic, much larger moose. None of these ecological claims author a free attack or automatic Prone, Grapple, bleed, tracking lock-on or unavoidable kill.

**Horn's nonlethal primary functions:** rutting/competition during mating seasons, intimidation and warding off other predators, and loosening earth/roots/weak material when excavating or enlarging dens. It may inflict real injury or help drive away an attacker when necessary. **Do not treat the horn as intrinsically optimized for repeated armor-piercing kills.**

**Slow pursuit venom:** the biological bite is a real potential **injection source** when the independently authored bite actually produces a surviving Piercing HP puncture after armor and prevention (or another explicit legitimate breach). A target resisting its toxin does **not** automatically negate all effects unless the actual profile says so. The existing [mundane toxin framework](../rules/05-combat/mundane-toxins-v0.md) applies its **one-instance**, exposure/resistance, and exploration clock boundaries. The current **TX-HM** catalogue is a useful **short 5/3-tick demonstration**, but it is **not already a long-term pursuit venom**. A new **slow-acting fictional Hunter venom** needs a distinct profile with actual effects, onset, resistance, duration, exploration timing and recovery rules; **none are presently executable**. No automatic sickness, speed reduction or guaranteed collapse is assigned yet.

**Vigor versus stamina:** The creature **may** use normal passive Vigor and wound repair like ordinary fauna, but a universal animal-Vigor entitlement and the Hunter's HP/Vigor/regen numbers are **OPEN**. Physical exertion, recovery from a Pounce, and walking after a sprint do **not** automatically spend or restore Vigor: Vigor is a regenerative reserve, **not a generalized stamina bar**. It has no independent personal Veil invocation or assumed VP pool. No conventional weapon/shield Guard is the **intended defense style**; final Natural Armor, Dodge, HP and counteractions await playtest.

**Pounce v0 now has a [scoped creature-specific review candidate](../rules/05-combat/hunter-pounce-and-prey-takedown-v0.md):** one provisional 24-AP Charge-style Bite plus an independently resolved free Trip-like balance contest against an **ordinary standing one-square PC in the Hunter's head-forward contact square**, with both parts able to fail independently. This **explicit** ability does not amend universal Charge (still one ordinary paid attack, no free Trip), establish multi-square Grapple, make Horn attacks, or give the Hunter executable Bite/venom/physiology. Non-PC size/mass, larger prey, final attack source/accuracy/damage and full encounter calibration remain unauthored. **Hunter remains CONCEPT_ONLY**.

## 6. MVP status and criteria

**Foundation decisions to review/lock now:** separate ecological frequency vs intrinsic CR vs party/composition vs scenario difficulty; standard/elite roles without invented difficulty points; per-context contact/social/hostility distinctions; the Hunter's ecological behavior and non-lethal horn priority; and 1×2 footprint handling with terrain averaging and pivots.

**Still pending:** Codex review of the Hunter's newly authored **one-square-PC Pounce candidate**, larger-body Grapple/takedown, slow venom, final natural Bite stats/Vigor, actual source/resolution, calibrated challenge rating, encounter frequency probabilities, numerical party budgets, and **full opposed encounter traces**. B06 stays open. No Archetype×Focus certification is claimed.
