# Multi-Square Creature Footprints v0

> **LOCK CANDIDATE — shared movement/occupancy foundation, scoped rather than a new size-based combat package.** This extends [Movement Foundation](movement-foundation.md) and [Special Movement, Terrain and Prone](special-movement-terrain-and-prone.md) to physically contiguous multi-square creatures. **The deterministic translation-cost, 1×2 pivot and whole-footprint validity procedures are candidates for locking after review.** No automatic size bonuses, longer melee Reach, charge damage, mass-based contest modifiers, custom Pounce, natural weapon or blanket squeezing exceptions follow from occupying multiple squares.

## 1. Footprint and orientation

- A creature's **footprint** is a named, fixed set of **N contiguous 1.5 m grid squares**, all occupied by the **same single creature**. Its position consists of **permanent body-local cell IDs and 1-based indices**, exactly one stable map-reference **cell ID**, relative offsets and a current orientation. Each cell retains its identity when the offsets reorient with the creature; its current **world grid coordinate changes**, but its ID/index does **not**. A selected attack/area-effect cell follows that cell, not the same world coordinate or a new coordinate sort.
- Each cell prevents illegal hostile overlap. **A creature does not collide with its own prior footprint** when some squares overlap between successive positions. Intermediate and final positions still must be physically legal.
- An attack targeting one eligible occupied square still targets the **creature once**, not N independent enemies or N separate HP pools. One effect does not multiply merely because its area overlaps more than one square of the same creature. A separately authored location, coverage or multi-target rule can specify otherwise.
- The creature's ordinary adjacent melee Reach is the **union of adjacency around currently occupied squares** where its anatomy allows the authored attack; a longer body does **not** grant an extra distance from any occupied square. Physical bite/horn direction and turn-related attacks require separate source-specific rules; this foundation does **not** introduce universal facing bonuses or flanking.
- A creature's physical body and footprint are linked. No portion can pass through impassable/fully blocked space just because other portions have firm footing. No free compression or squeezing.

### Stable footprint indices and map-reference cell

1. When the creature's footprint is **first instantiated**, assign each anatomical/body-local cell a **unique immutable ID** and **permanent 1-based ordinal index**, and choose exactly **one fixed reference cell ID**. For the Hunter's straight 1×2 body, **index 1 = `head`, index 2 = `rear`, reference = `head`**. In structured records these are `footprint.cell_ids` (index order) and `footprint.reference_cell_id`. For a larger or irregular footprint, enumerate its authored body-local offsets exactly once and keep the order; the list must have one entry per actual cell.
2. Build the current map mapping `cell_id → world(x,y,z)` from **that same body-local ID and orientation** after each legal translation, pivot or relocation (including Blink if otherwise legal). A pivot **moves a cell's coordinate**, not its anatomical label. Never reconstruct, renumber, relabel or reorder the stored cell IDs from their **current** x/y/z values.
3. When an effect precommits to an occupied grid square, resolve the **one body-local cell ID/index** occupying that square at the proper declaration point and store it with that effect. At later resolution, use the **same ID/index** to retrieve its **then-current coordinate**. A changed orientation, reference coordinate or world-coordinate ordering never changes the committed anatomical cell, grants a new choice or rewrites the original attack's legality.
4. For a legacy multi-square actor **without a recorded reference cell or labels**, the preexisting **lowest-x, then lowest-y, then lowest-z** rule can be used **once at initial setup** to choose a reference and assign deterministic initial body-local indices. **Persist** those chosen identities before any such attack/Ward declaration; on every subsequent pivot/move, carry the existing IDs forward instead of sorting again. For new structured footprints, use the explicitly authored IDs; no free choice of a later favorable reference cell.
5. If the originally chosen anatomical cell **ceases to exist** after an expressly authored footprint change, a dependent effect may use its source rule's fallback (for [Protective Ward](../07-veil-magic/protective-ward-v0.md), **the surviving fixed reference cell ID**, otherwise the **lowest remaining permanent cell index**) **only if the original attack and effect remain legal**. Loss of that cell is not a reason to assign a new attack profile or target after a roll. Ordinary movement/pivoting does not remove cells.

**Pivot regression (two cells):** Initially `rear=(0,0)`, `head=(1,0)`; an attack specifically selects **head = index 1**. Pivot 90° about the rear to `head=(0,-1)`, `rear=(0,0)`. The occupied-world-coordinate sort switches order across the pivot (originally rear first, afterward head first), but the stored **head/index 1** still maps to **(0,-1)**, never rear at (0,0). The same identity must be preserved through another pivot, translation, or Blink that keeps the footprint.

## 2. Whole-footprint translation

For a voluntary one-square orthogonal or diagonal **translation** of a rigid footprint:

1. Preserve the current orientation and move **every** offset by the same one-square vector.
2. Validate **all** destination squares and the full body passage. Each constituent virtual cell's diagonal passage must pass the ordinary blocked-corner rule, including obstructed swept space; a footprint cannot pass through a forbidden gap by checking only its reference square. If any required cell is impassable or the rigid body cannot fit, **the entire step is illegal**, regardless of the cost of other cells.
3. For each footprint cell `i`, calculate the ordinary **virtual step cost `c_i`**, using the same movement mode and step direction: **orthogonal 2 MP / diagonal 3 MP**, doubled **base** when Cautious, then that cell's *destination* terrain surcharge (+0 Normal, +2 Difficult, +4 Severe). Count all `N` cells, including a rear cell that moves into a square previously occupied by this creature. Evaluate terrain at the destination of **each indexed cell**; do not charge only the lead edge.
4. The creature pays **`ceil((c_1 + ... + c_N) / N)` MP** for the translation. This models redistributed quadruped traction/load instead of granting the entire body the best of its front/rear footing. **Round once after averaging**, not per individual component.
5. Normal **allied occupied-square transit surcharges** remain separately **+2 MP per distinct newly entered allied-occupied square**, added after terrain averaging, and the creature must be able to finish that continuous transit with a clear whole footprint. An ally surcharge does not become cheaper merely because the creature is long. A square the mover itself previously occupied is not an ally surcharge or collision. Normal hostile non-overlap remains strict.
6. Declare the full footprint translation as **one movement step** for cost, movement-segment and Opportunity purposes, not one successive step per constituent cell. A single hazard triggers at most once for a given creature from a given whole-footprint step unless its independently authored trigger says otherwise. The move happens atomically after ordinary response windows; no intermediate halfway body state.

The base and destination terrain costs use exactly the existing MP numbers. Averaging does **not** let passability, legal threats, collision, effects or physical obstacles be averaged.

### Representative 1×2 ordinary steps

| Front terrain | Rear terrain | Orthogonal `ceil((front+rear)/2)` | Diagonal |
|---|---|---:|---:|
| Normal | Normal | `ceil((2+2)/2)=2` MP | `ceil((3+3)/2)=3` MP |
| Difficult | Normal | `ceil((4+2)/2)=3` MP | `ceil((5+3)/2)=4` MP |
| Difficult | Difficult | `4` MP | `5` MP |
| Severe | Normal | `ceil((6+2)/2)=4` MP | `ceil((7+3)/2)=5` MP |
| Severe | Difficult | `ceil((6+4)/2)=5` MP | `ceil((7+5)/2)=6` MP |
| Severe | Severe | `6` MP | `7` MP |
| Impassable | Normal | **Illegal** | **Illegal** |

**Example:** Hunter front square moves into Difficult terrain (4 MP) while its rear cell moves through Normal (2 MP): one orthogonal step costs **3 MP**. In reverse terrain the cost is also 3. For a Cautious orthogonal step, double each *base* 2→4 before adding terrain; with front Difficult (6) and rear Normal (4), cost **5 MP**, not 6. No Cautious Movement Opportunity from this Cautious step.

## 3. Turning: first executable shape is a straight 1×2

A straight 1×2 footprint has **one front/head and one rear cell** (the distinction is anatomical metadata, not universal target Armor, bonus damage or combat facing):

- A voluntary **90° pivot** keeps exactly one designated occupied cell **stationary** (front or rear, chosen when the pivot is declared), while the other occupies the perpendicular adjacent destination. The moving cell traverses a **diagonal grid displacement** around that pivot: charge **3 MP** for an ordinary pivot (**6 MP Cautious**) **plus the destination cell's flat terrain surcharge**. The anchored cell does not enter new terrain and its terrain is not charged for a stationary pivot. Add any ordinary newly entered allied transit surcharge separately.
- Both final occupied cells and the **swept diagonal corner** must be clear. Apply the existing diagonal blocked-corner and rigid-body passage restrictions to the moving cell and the full body. An impassable destination or obstructed rotation is illegal, not converted into a free turn.
- A **180° reversal** takes **two** separately paid and validated 90° pivots. The body cannot swap head and tail labels for free; changing the creature's traveling direction does not automatically reverse its anatomy.
- A successfully completed 90° pivot changes one occupied square and counts as **one legal movement step** for movement segments and ordinary Movement Interception; an attempted/blocked pivot does not count. Normal versus Cautious movement governs the existing Movement Opportunity trigger (see below). A pivot cannot satisfy **Charge's minimum three straight-line translated approach steps** or count as distance moved for run-up or Sprint.
- **Normal movement** permits pivots; **Rapid Advance, Charge and Sprint forbid voluntary pivot/turning** while their authored fixed-heading restriction applies. Their movement allowances, AP timing, Prone suspension, Opportunity/Interception, Charge retargeting and no-bonus/no-free-knockdown rules remain unchanged.

For other rigid footprints (**1×3, 2×2, 2×3, irregular shapes**), translation, occupancy, targeting and threatened-space handling above apply, but **voluntary rotation/pivot cost and swept-turn geometry require a separately authored geometry rule**. No implicit instant/free rotation is granted.

## 4. Threatened space, interaction and special movement

- A creature is in an enemy's threatened space if **any** of its footprint squares is threatened by that enemy. If a Normal translation/pivot moves any occupied square **out of a square that enemy threatens**, the normal leaving-threatened-space rule can apply **before** the whole movement step resolves. This includes movement from threatened to threatened space. A threatening enemy still receives **at most one general Movement Opportunity from the creature per movement segment**, not one per foot/head/rear cell. **Cautious** whole-footprint steps do not trigger that general departure Opportunity.
- Movement, interception, cover, AoE and obstruction must assess the **whole legal footprint**. A multi-square body does not gain multiple Reactions, Turns, Opportunities, attack targets or Regeneration Steps from its extra occupied squares.
- **Rapid Advance, Charge and Sprint** use their existing total allowance and AP rules; each translated footprint step simply consumes the applicable whole-footprint MP. Fixed heading remains mandatory. No free Pounce, collision/knockdown, Shove, Trip, Grapple, capture or additional damage comes from this chapter.
- **Forced movement:** a source must physically fit and place the whole body into legal squares; this document provides no independent contest, mass exception, collision damage, partial squashing or new effect when an attempted forced displacement cannot fit. Use the independently authored source effect and the existing collision/fall boundary.
- **Grapple compatibility is explicitly OPEN:** the current [Grapple v0](universal-maneuvers.md) assumes the participants share a single **Grapple square**. This document does **not** rewrite that state to silently collapse a 1×2 creature into one square. A multi-square grapple/takedown, Pin, dragging a multi-square participant, and Pounce-linked takedown require a separate topology/contest specification; until authored, **do not resolve them using the single-square Grapple shortcut**. Existing Trip/Shove may only be attempted where current method and size/mass plausibility are already independently legal.
- Existing [Protective Ward](../07-veil-magic/protective-ward-v0.md) and other source-defined multi-square targeted effects retain their **precommitted body-local footprint cell ID/index** after translation, pivot or legal Blink; they map that same anatomical cell to its **new** world coordinate only at resolution. **Do not re-sort final occupied coordinates** to interpret a stored index. This rule supplies no ability to change the target cell after seeing a die result.

## 5. Examples and exclusions

| Situation | Correct result |
|---|---|
| Normal head Difficult, rear Normal | 3 MP orthogonal |
| Same terrain, Cautious orthogonal | 5 MP (base doubled before terrain, then averaged) |
| Both Severely Difficult | 6 MP orthogonal |
| One end is impassable | No movement |
| A long creature translates one square while its rear overlaps its own old front square | Legal if path clear; still includes both indexed destination terrain costs |
| A 90° pivot with Normal terrain destination | 3 MP, moving end traverses a diagonal; anchored end stationary |
| A pivot's destination is Difficult | 5 MP (3 + 2) |
| Hunter tries to pivot inside fixed-heading Charge | Illegal; no free heading reset |
| A 1×2 creature exits two squares threatened by the same enemy in one segment | At most one general Movement Opportunity for that enemy |
| A creature overlaps two cells of one AoE | One target/normal effect instance unless the effect independently says otherwise |
| A 1×2 body tries to use shared single-square Grapple to hold a 1-square enemy | **Not authorized by footprint rules**; needs a separate large-body grapple method |

**Remaining design/calibration:** Pounce/takedown delivery, applicable mass/size contests, multi-square Grapple/Drive/Drag, complex footprint pivots, precise collision/squeezing, size-specific natural armor/reach and unusual terrain traversal. Do not fill these automatically via an enemy's footprint tag.
