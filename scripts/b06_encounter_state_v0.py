"""B06 G0: deterministic actor/resource state and native encounter event ledger.

This is an integration substrate, NOT an attack roller, movement solver, spell
executor, opponent AI, wound adjudicator or complete-encounter simulator.
External decisions are required for every unresolved tactical/legal choice.
No new rules are introduced. Run tests/test_b06_encounter_state_v0.py.
"""
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ENEMIES = {
    "B06-EN-01": "content/creatures/b06-firebound-sentry.v0.json",
    "B06-EN-02": "content/creatures/b06-ordinary-human-soldier.v0.json",
    "B06-EN-03": "content/creatures/b06-hunter-of-the-woods.v0.json",
}
FOCUS_COST = {"High": (30, 20), "Medium": (24, 24), "Low": (20, 30)}
VALID_DEFENSES = frozenset(("guard", "dodge", "take_hit"))


class UnresolvedDecision(ValueError):
    """Caller must provide a legal rule/policy choice, never auto-play one."""


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be integer >= {minimum}")
    return value


def _fingerprint(path):
    return sha256((ROOT / path).read_bytes()).hexdigest()


@dataclass(frozen=True)
class Source:
    path: str
    source_id: str
    digest: str
    status: str
    abilities: tuple
    training: tuple
    equipment: tuple
    attack_profiles: tuple
    start_state: str
    attack_requirements: tuple = ()  # (profile_id, required effect, forbidden effect)


@dataclass
class Wound:
    ident: str
    requirement: int
    progress: int = 0
    repairable: bool = True
    severity: str | None = None
    location: str | None = None
    trauma: str | None = None
    source_event: str | None = None

    def __post_init__(self):
        _integer(self.requirement, "wound requirement", 1)
        _integer(self.progress, "wound progress")
        if self.progress > self.requirement:
            raise ValueError("Repair exceeds requirement")


@dataclass(frozen=True)
class RegenerationChoice:
    hp: int = 0
    repair: int = 0
    cancel_dying_loss: bool = False
    wound_allocations: tuple = ()  # G4 only: non-Dying ((wound_id, amount), ...)


@dataclass
class Actor:
    id: str
    team: str
    source: Source
    level: int
    focus: str | None
    initiative_bonus: int
    awareness: int
    agility: int
    hp_max: int
    vigor_max: int
    vp_max: int
    hp: int
    vigor: int
    vp_available: int
    vp_committed: int
    vp_spent: int
    regen: int
    ap_total: int
    physical_ap: int
    projection_ap: int | None
    guard_instrument: str | None
    guard_value: int | None
    guard_capacity: int
    footprint: tuple = ("body",)
    occupied: tuple = ()
    ready_guard: bool = True
    ammunition: int = 0
    maintained: list = field(default_factory=list)
    wounds: list = field(default_factory=list)
    conditions: list = field(default_factory=list)
    milestones: list = field(default_factory=list)
    ap_remaining: int = 0
    mp_remaining: int = 0
    guard_remaining: int = 0
    dodge_pressure: int = 0
    reaction_available: bool = False
    opportunity_active: bool = False
    opportunity_used: int = 0
    blink_debt_due: int = 0
    blink_debt_next: int = 0
    dead: bool = False
    # Immutable anatomical selection once sourced (or frozen at initial setup).
    # Indexes of footprint and occupied correspond across all legal pivots.
    reference_cell_id: str | None = None

    def reference_square(self):
        """Return the fixed body-local reference cell's CURRENT world square."""
        if not self.footprint or len(self.occupied) != len(self.footprint):
            raise ValueError("Actor requires a complete fixed footprint")
        if self.reference_cell_id is None:
            # Legacy fallback is selected ONCE, never re-sorted on a pivot.
            self.reference_cell_id = self.footprint[
                self.occupied.index(min(self.occupied))]
        if self.reference_cell_id not in self.footprint:
            raise ValueError("Reference cell is not part of authored footprint")
        return self.occupied[self.footprint.index(self.reference_cell_id)]

    def validate(self):
        for name in ("hp_max", "vigor_max", "vp_max", "vigor",
                     "vp_available", "vp_committed", "vp_spent", "regen",
                     "ap_total", "physical_ap", "guard_capacity", "guard_remaining",
                     "ap_remaining", "mp_remaining", "dodge_pressure",
                     "opportunity_used", "ammunition"):
            _integer(getattr(self, name), name)
        if self.hp_max < 1 or self.physical_ap < 1:
            raise ValueError("Invalid source-derived max HP/AP cost")
        if self.vigor > self.vigor_max:
            raise ValueError("Vigor exceeds maximum")
        if self.hp > self.hp_max or self.hp < -self.hp_max:
            raise ValueError("HP exceeds bound or corpse threshold")
        if sum((self.vp_available, self.vp_committed, self.vp_spent)) != self.vp_max:
            raise ValueError("Available + Committed + Spent VP != Max VP")
        if self.guard_remaining > self.guard_capacity or self.ap_remaining > self.ap_total:
            raise ValueError("Round/turn capacity exceeded")
        if self.dead != (self.hp <= -self.hp_max):
            raise ValueError("Dead status disagrees with HP threshold")
        if not self.footprint or len(set(self.footprint)) != len(self.footprint):
            raise ValueError("Unique source footprint cell IDs required")
        if len(self.occupied) != len(self.footprint):
            raise ValueError("Explicit static footprint cells required")
        if len(set(self.occupied)) != len(self.occupied):
            raise ValueError("Actor's occupied squares overlap")
        self.reference_square()  # Validate/freeze source or one-time legacy ID.
        if self.guard_instrument is None and self.guard_value is not None:
            raise ValueError("Guard value without instrument")
        for w in self.wounds:
            if not isinstance(w, Wound):
                raise ValueError("Invalid wound object")
            w.__post_init__()


def enemy_actor(source_id, actor_id, team, *, start_state=None, occupied):
    """Load exact existing B06 JSON source start; never recompute NPC Focus."""
    path = ENEMIES[source_id]
    obj = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if obj["id"] != source_id or obj["status"] != "EXECUTABLE_TEST_FIXTURE":
        raise ValueError("Source fixture mismatch")
    states = obj["resources"]["start_states"]
    if start_state is None:
        if len(states) != 1:
            raise UnresolvedDecision("Choose explicit enemy start state")
        start_state = states[0]["id"]
    candidates = [s for s in states if s["id"] == start_state]
    if len(candidates) != 1:
        raise ValueError("Unknown enemy start state")
    init = candidates[0]
    d, r = obj["defenses"], obj["resources"]
    shape = obj.get("creature_profile", {}).get("footprint", {})
    footprint = tuple(shape.get("cell_ids", ("body",)))
    source = Source(path, source_id, _fingerprint(path), obj["status"],
                    tuple(sorted(obj["abilities"].items())), (),
                    tuple((e["name"], e["equipped"]) for e in obj["equipment"]),
                    tuple(p["id"] for p in obj["attack_profiles"]), init["id"],
                    tuple((p["id"], p.get("required_active_effect"),
                           p.get("requires_effect_inactive"))
                          for p in obj["attack_profiles"]))
    actor = Actor(actor_id, team, source, obj["benchmark_level"],
                  obj["identity"]["focus"], d["initiative_bonus"],
                  obj["abilities"]["awareness"], obj["abilities"]["agility"],
                  d["hp_max"], d["vigor_max"], r["max_vp"],
                  init["hp"], init["vigor"], init["available_vp"],
                  init["committed_vp"], init["spent_vp"],
                  r["natural_regeneration_throughput"], r["turn_ap"],
                  r["physical_action_ap"], r["projection_action_ap"],
                  d["guard_instrument"], d["guard_base"], d["guard_capacity"],
                  footprint=footprint, occupied=tuple(tuple(p) for p in occupied),
                  reference_cell_id=shape.get("reference_cell_id"),
                  ready_guard=(d["guard_instrument"] is not None),
                  maintained=list(init["active_effects"]))
    actor.validate()
    return actor


def party_actor(role, level, actor_id, team, *, occupied):
    """A/B remain physical proxies; H/M/R/F are sourced B05 sheets."""
    _integer(level, "level", 1)
    if level not in (1, 2, 3):
        raise ValueError("G0 only adapts authored L1–3")
    if role == "H":
        from scripts.b05_high_priest_life_l1_l3_v0 import profile
        p=profile(level)
        path="scripts/b05_high_priest_life_l1_l3_v0.py"
        gear=tuple((name,"worn" if name=="Leather armor" else
                    "wielded" if name=="Sword" else "carried")
                   for name in p["equipment_sp"])
        source=Source(path,"H",_fingerprint(path),"STRUCTURAL_B05_ONLY",
                      tuple(sorted(p["abilities"].items())),
                      tuple(sorted(p["weapon_training"].items())),
                      gear,(),f"L{level}-high-life-structural")
        a=p["abilities"]
        actor=Actor(actor_id,team,source,level,"High",
                    p["initiative"],a["Awareness"],a["Agility"],
                    p["hp_max"],p["vigor_max"],p["vp_max"],
                    p["hp_max"],p["vigor_max"],p["vp_max"],0,0,
                    p["normal_regen_throughput"],p["turn_ap"],
                    p["physical_action_ap"],p["projection_action_ap"],
                    "Sword",p["guard_value"],p["normal_guard_capacity"],
                    occupied=tuple(tuple(c) for c in occupied))
    elif role == "M":
        from scripts.b05_medium_priest_life_l1_l3_v0 import profile
        p = profile(level)
        path = "scripts/b05_medium_priest_life_l1_l3_v0.py"
        gear = tuple((name, "worn" if name == "Leather armor" else
                      "wielded" if name == "Sword" else "carried")
                     for name in p["equipment_sp"])
        source = Source(path, "M", _fingerprint(path), "STRUCTURAL_B05_ONLY",
                        tuple(sorted(p["abilities"].items())),
                        tuple(sorted(p["weapon_training"].items())),
                        gear, (), f"L{level}-medium-life-structural")
        a = p["abilities"]
        actor = Actor(actor_id, team, source, level, "Medium",
                      p["initiative"], a["Awareness"], a["Agility"],
                      p["hp_max"], p["vigor_max"], p["vp_max"],
                      p["hp_max"], p["vigor_max"], p["vp_max"], 0, 0,
                      p["normal_regen_throughput"], p["turn_ap"],
                      p["physical_action_ap"], p["projection_action_ap"],
                      "Sword", p["guard_value"], p["normal_guard_capacity"],
                      occupied=tuple(tuple(c) for c in occupied))
    elif role == "T":
        # Source T: prepared technical Arsenal and one *explicit*, ordinary
        # sourced Sword Cut profile; no generic weapon enchantment authority.
        from scripts.b05_low_scholar_l1_l3_v0 import profile
        p=profile(level)
        path="scripts/b05_low_scholar_l1_l3_v0.py"
        equipment=tuple(sorted((name,
            "worn" if name=="Leather armor" else
            "wielded" if name=="Sword" else "carried")
            for name in p["equipment_sp"]))
        source=Source(path,"T",_fingerprint(path),"STRUCTURAL_B05_ONLY",
                      tuple(sorted(p["abilities"].items())),
                      tuple(sorted(p["weapon_training"].items())),
                      equipment, ("B05-PC-T-SWORD-CUT",),
                      f"L{level}-low-scholar-prepared")
        a=p["abilities"]
        actor=Actor(actor_id,team,source,level,"Low",p["initiative"],
                    a["Awareness"],a["Agility"],p["hp_max"],p["vigor_max"],
                    p["vp_max"],p["hp_max"],p["vigor_max"],p["vp_max"],0,0,
                    p["normal_regen_throughput"],p["turn_ap"],
                    p["physical_action_ap"],p["projection_action_ap"],
                    "Sword",p["guard_value"],p["normal_guard_capacity"],
                    occupied=tuple(tuple(c) for c in occupied))
    elif role == "S":
        # Structural Medium Scholar, independent from M Medium Priest.
        # Only its exact mundane Sword Cut profile is authorized.
        from scripts.b05_medium_scholar_l1_l3_v0 import profile
        p=profile(level)
        path="scripts/b05_medium_scholar_l1_l3_v0.py"
        equipment=tuple(sorted((name,
            "worn" if name == "Leather armor" else
            "wielded" if name == "Sword" else "carried")
            for name in p["equipment_sp"]))
        source=Source(path,"S",_fingerprint(path),"STRUCTURAL_B05_ONLY",
                      tuple(sorted(p["abilities"].items())),
                      tuple(sorted(p["weapon_training"].items())),
                      equipment, ("B05-PC-S-SWORD-CUT",),
                      f"L{level}-medium-scholar-inward")
        a=p["abilities"]
        actor=Actor(actor_id,team,source,level,"Medium",p["initiative"],
                    a["Awareness"],a["Agility"],p["hp_max"],p["vigor_max"],
                    p["vp_max"],p["hp_max"],p["vigor_max"],p["vp_max"],0,0,
                    p["normal_regen_throughput"],p["turn_ap"],
                    p["physical_action_ap"],p["projection_action_ap"],
                    "Sword",p["guard_value"],p["normal_guard_capacity"],
                    occupied=tuple(tuple(c) for c in occupied))
    elif role in ("R", "F"):
        if role == "R":
            from scripts.b05_bow_vanguard_l1_l3_v0 import profile
            path = "scripts/b05_bow_vanguard_l1_l3_v0.py"
        else:
            from scripts.b05_high_scholar_fire_l1_l3_v0 import profile
            path = "scripts/b05_high_scholar_fire_l1_l3_v0.py"
        p = profile(level)
        is_bow = role == "R"
        focus = p["focus"]
        abilities = p["abilities"]
        guard = None  # Bow in hands, or F's dagger only carried.
        cap = p["normal_guard_capacity"] if is_bow else p["guard_capacity"]
        equipments = p["equipment_sp"] if is_bow else p["starting_equipment_sp"]
        # The R bow is wielded but never Guard-capable. F's dagger is
        # purchased/carried, NOT wielded; leather is worn in both scenes.
        equipment_state = {
            name: ("worn" if name == "Leather armor"
                   else "wielded" if is_bow and name == "Bow"
                   else "ammunition" if is_bow and name == "20 arrows"
                   else "carried")
            for name in equipments
        }
        source = Source(path, role, _fingerprint(path), "STRUCTURAL_B05_ONLY",
                        tuple(sorted(abilities.items())),
                        tuple(sorted(p["weapon_training"].items())),
                        tuple(sorted(equipment_state.items())), (),
                        f"L{level}-structural")
        actor = Actor(actor_id, team, source, level, focus, p["initiative"],
                      abilities["Awareness"], abilities["Agility"],
                      p["hp_max"], p["vigor_max"], p["vp_max"],
                      p["hp_max"], p["vigor_max"], p["vp_max"], 0, 0,
                      p["normal_regen_throughput"], p["turn_ap"],
                      p["physical_action_ap"], p["projection_action_ap"],
                      guard, None, cap,
                      occupied=tuple(tuple(c) for c in occupied),
                      ready_guard=False,
                      ammunition=(p["initial_arrows"] if is_bow else 0))
    elif role in ("A", "B"):
        from scripts.b06_hunter_party_exchanges_v0 import BUILD
        p = BUILD[role]
        path = "scripts/b06_hunter_party_exchanges_v0.py"
        hp = p["hp"]
        # A/B were verified as Life/Low Priests in the authored B05 L3
        # ledger: VA0 grants 2 VP/level. The Phase-2 BUILD is still ONLY
        # the attack/defense physical projection. Default is explicitly
        # an unbuffed full-resource scene, never automatically chosen Rite.
        ability_array = ((2, 3, 0, 0, 1, -2, 2, 0, 0) if role == "A"
                         else (2, 2, 0, 1, 0, -2, 3, 0, 0))
        keys = ("Strength", "Agility", "Precision", "Intellect", "Awareness",
                "Presence", "Vitality", "Veil Affinity", "Veil Control")
        gear = (("Leather armor", "worn"), ("Sword", "wielded"),
                ("Medical kit", "carried"), ("Adventuring pack", "carried")) if role == "A" else (
                ("Brigandine", "worn"), ("Mace", "wielded"), ("Shield", "held"),
                ("Medical kit", "carried"), ("Adventuring pack", "carried"))
        source = Source(path, role, _fingerprint(path), "B05_UNBUFFED_PHYSICAL_PROXY",
                        tuple(zip(keys, ability_array)),
                        (("Sword", 2),) if role == "A" else (("Mace", 2),),
                        gear, ("B06-PC-A-SWORD",) if role=="A" else
                        ("B06-PC-B-MACE",), f"L{level}-physical-proxy")
        ap = 30 + 6 * (level - 1)
        # B gets Combat Awareness +2 only after L2; A gets Guard Reserve
        # only after L2. The Phase 1/2 physical role constants are L2/L3.
        initiative = (p["initiative"] if role == "A" or level >= 2 else 2)
        extra_guard = (p["guard_extra"] if role == "B" or level >= 2 else 0)
        actor = Actor(actor_id, team, source, level, "Low", initiative,
                      ability_array[4], p["agi"],
                      hp, hp * level, 2 * level, hp, hp * level,
                      2 * level, 0, 0,
                      p["regen"], ap, 20, 30, "Sword" if role == "A" else "Shield",
                      p["guard"], ap // 20 + extra_guard,
                      occupied=tuple(tuple(c) for c in occupied))
    else:
        raise ValueError("G0 supports only A/B/R/F sources")
    actor.validate()
    return actor


@dataclass
class Trigger:
    key: str
    actor_id: str
    target_id: str
    legal: bool = True


@dataclass
class Reservation:
    actor_id: str
    trigger_key: str
    label: str
    order: int


@dataclass(frozen=True)
class Response:
    actor_id: str
    kind: str  # 'reaction' or 'opportunity', not a free Guard/Dodge
    label: str


class Encounter:
    def __init__(self, actors, initiative_scores, *, seed, tie_order=(),
                 scenario="G0-clear", policy="explicit", objective="unresolved"):
        self.actors = {a.id: a for a in actors}
        if not actors or len(self.actors) != len(actors):
            raise ValueError("Nonempty unique actor roster required")
        for a in actors:
            a.validate()
        cells = [p for a in actors for p in a.occupied]
        if len(set(cells)) != len(cells):
            raise ValueError("Initial footprint overlaps another actor")
        if set(initiative_scores) != set(self.actors):
            raise ValueError("Initiative scores required for all combatants")
        if any(type(x) is not int for x in initiative_scores.values()):
            raise ValueError("Initiative must be an explicit rolled integer")
        self.seed = _integer(seed, "seed")
        self.scenario, self.policy, self.objective = scenario, policy, objective
        self.round = 0
        self.cursor = 0
        self.current = None
        self.ledger = []
        self.reservations = []
        self.seen_sequences = set()
        self.regen_done = set()
        self.pending_regeneration = None
        # Only the actual currently executing spontaneous callback may
        # apply pre-roll effects. A historical ledger entry is NOT proof
        # that the response window remains open; nested windows restore it.
        self._live_spontaneous_response = None
        self.g1 = None  # Optional native physical grid; G0-only stays supported.
        self.g2 = None  # Optional G2 ranged executor; never adds phantom shots.
        self.g3 = None  # Optional source-bound spell state; G0-only is unchanged.
        self.g4 = None  # Optional injury executor; G0/G3 stand-alone paths unchanged.
        rank = {v: i for i, v in enumerate(tie_order)}
        def priority(a):
            return (-initiative_scores[a.id], -a.awareness, -a.agility,
                    rank.get(a.id, len(rank)))
        self.order = tuple(a.id for a in sorted(actors, key=priority))
        for i in range(len(self.order) - 1):
            a, b = (self.actors[x] for x in self.order[i:i + 2])
            if priority(a) == priority(b):
                raise UnresolvedDecision("Exact Initiative tie needs chosen ally order or roll-off")
        self.log("encounter_created", order=self.order, seed=self.seed,
                 scenario=self.scenario, policy=self.policy,
                 objective=self.objective, source_ids={
                     a.id: {
                         "source_id": a.source.source_id, "digest": a.source.digest,
                         "start_state": a.source.start_state, "team": a.team,
                         "level": a.level, "hp": a.hp, "vigor": a.vigor,
                         "vp": [a.vp_available, a.vp_committed, a.vp_spent],
                         "occupied": a.occupied,
                     } for a in actors})

    def log(self, kind, **details):
        # JSON-serializable, immutable-by-serialization history; no refs to actors.
        self.ledger.append({"index": len(self.ledger), "round": self.round,
                            "turn": self.current, "kind": kind,
                            "detail": json.loads(json.dumps(details, sort_keys=True))})

    def serialize(self):
        return json.dumps(self.ledger, sort_keys=True, separators=(",", ":"))

    def check(self):
        for actor in self.actors.values():
            actor.validate()

    def begin_round(self):
        if self.round and self.cursor != len(self.order):
            raise ValueError("Cannot refresh round capacities mid-round")
        # Round End is logged on last end_turn(), before any subsequent round.
        self.round += 1
        self.regen_done.clear()
        self.seen_sequences.clear()
        self.cursor = 0
        self.current = None
        for a in self.actors.values():
            a.guard_remaining = a.guard_capacity
            a.dodge_pressure = 0
            # Refresh is a once-per-round capacity, not a snapshot of HP.
            # Dying actors cannot use it now; declaration validates current
            # consciousness. If Step 2 later restores HP, capacity is intact.
            a.reaction_available = True
            a.opportunity_active = False
            a.opportunity_used = 0
        self.log("round_begin", refreshed=list(self.order))
        if self.g3 is not None:
            self.g3.on_round_begin()
        # G4.2 absolute long milestones and independently earned 6h
        # Recovery resolve only at genuine Round Begin; no ghost own turns.
        if self.g4 is not None:
            self.g4.clock.on_round_begin(self.round)
        self.check()

    def _regenerate(self, a, choice):
        if self.g4 is not None:
            return self.g4.regenerate(a, choice)
        if a.id in self.regen_done:
            raise ValueError("Regeneration Step already resolved this round")
        if a.dead:
            self.regen_done.add(a.id)
            self.log("regeneration_dead", actor=a.id)
            return
        # Guided Regeneration is only +1 throughput at the beneficiary's
        # existing genuine Regeneration Step, never a new or early step.
        throughput=(a.regen + (self.g3.regen_throughput(a.id)
                               if self.g3 is not None else 0))
        missing = a.hp < a.hp_max or any(w.repairable and w.progress < w.requirement for w in a.wounds)
        if missing and a.vigor and throughput and choice is None:
            self.log("unresolved_decision", actor=a.id, choice="regeneration_allocation")
            raise UnresolvedDecision("Explicit regeneration allocation required")
        choice = choice or RegenerationChoice()
        if not isinstance(choice, RegenerationChoice):
            raise ValueError("Invalid regeneration policy")
        for part in (choice.hp, choice.repair):
            _integer(part, "regeneration allocation")
        if type(choice.cancel_dying_loss) is not bool:
            raise ValueError("Cancel Dying loss must be bool")
        dying = a.hp <= 0
        if choice.cancel_dying_loss and not dying:
            raise ValueError("Cannot cancel Dying loss while conscious")
        survival = int(dying and choice.cancel_dying_loss)
        debit = survival + choice.hp + choice.repair
        if debit > throughput or debit > a.vigor:
            raise ValueError("Natural regeneration exceeds throughput or available Vigor")
        if not dying and choice.hp > a.hp_max - a.hp:
            raise ValueError("Cannot heal above Max HP")
        # Dying is survival -> oldest-first wound repair -> HP (only if unblocked).
        incomplete = [w for w in a.wounds if w.progress < w.requirement]
        repairable = [w for w in incomplete if w.repairable]
        # Non-Dying PCs choose *which* wound to repair; this minimal G0
        # plan lacks per-wound allocation. Never silently give them Dying's
        # oldest-first selection when multiple wounds are available.
        if not dying and choice.repair and len(repairable) > 1:
            self.log("unresolved_decision", actor=a.id,
                     choice="non_dying_wound_target_allocation")
            raise UnresolvedDecision("Select non-Dying wound allocation explicitly in G4")
        if choice.repair > sum(w.requirement - w.progress for w in repairable):
            raise ValueError("Repair allocation exceeds open repairable wounds")
        if dying and choice.hp:
            if any(not w.repairable for w in incomplete) or (
                    choice.repair < sum(w.requirement - w.progress for w in repairable)):
                raise ValueError("Dying natural HP requires all blocking wounds repaired")
            if a.hp + choice.hp > a.hp_max:
                raise ValueError("Dying restoration exceeds Max HP")
        if dying and not survival and a.hp - 1 <= -a.hp_max and (
                choice.hp or choice.repair):
            raise ValueError("Cannot regenerate after lethal Dying loss")
        self.regen_done.add(a.id)
        hp_before, vigor_before = a.hp, a.vigor
        if dying and not survival:
            a.hp -= 1
            if a.hp <= -a.hp_max:
                a.hp = -a.hp_max
                a.dead = True
        if not a.dead:
            for w in repairable:
                delta = min(choice.repair, w.requirement - w.progress)
                w.progress += delta
                choice = RegenerationChoice(choice.hp, choice.repair - delta, choice.cancel_dying_loss)
            a.hp += choice.hp
            a.vigor -= debit
        self.log("regeneration_step", actor=a.id, hp_before=hp_before, hp_after=a.hp,
                 vigor_before=vigor_before, vigor_after=a.vigor,
                 survival_cancelled=bool(survival), hp_restored=choice.hp,
                 repair_points=debit-survival-choice.hp, throughput_spent=debit)
        self.check()

    def start_turn(self, actor_id, *, regen_choice=None,
                   on_regeneration_ready=None,on_regeneration_complete=None):
        if not self.round or self.cursor >= len(self.order):
            raise ValueError("No turn is ready")
        if self.current is not None and self.pending_regeneration != actor_id:
            raise ValueError("Another turn is already open")
        if self.current is not None and self.pending_regeneration is None:
            raise ValueError("Turn resources already established")
        if actor_id != self.order[self.cursor]:
            raise ValueError("Actor is not next in Initiative order")
        a = self.actors[actor_id]
        if self.pending_regeneration is None:
            # Preflight debt before beginning Step 1; invalid debt is not
            # allowed to partially expire reservations or start a turn.
            if a.blink_debt_due > a.ap_total:
                self.log("unresolved_decision", actor=actor_id, choice="blink_debt_shortage")
                raise UnresolvedDecision("Authored exceptional Blink AP shortage")
            self.current = actor_id
            expired = [r.label for r in self.reservations if r.actor_id == actor_id]
            self.reservations = [r for r in self.reservations if r.actor_id != actor_id]
            self.log("turn_start_expiry", actor=actor_id, expired=expired)
            self.pending_regeneration = actor_id
        # Step 1 is committed and logged only once. If Step 2 needs a policy
        # choice, keep this turn suspended here and resume Step 2 later; do
        # NOT revive expired reservations or append a duplicate expiry event.
        # Optional source-authored response at the real Step-2 boundary.
        # This is not a new free regeneration step or an ordinary cast.
        if on_regeneration_ready is not None:
            if not callable(on_regeneration_ready):
                raise ValueError("Regeneration response must be callable")
            on_regeneration_ready(self, actor_id)
        low = (getattr(self.g3,"low_life",None)
               if self.g3 is not None else None)
        if low is not None:
            low.on_step_start(actor_id)
        low_scholar=(getattr(self.g3,"low_scholar",None)
                     if self.g3 is not None else None)
        if low_scholar is not None:
            low_scholar.on_step_start(actor_id)
        self._regenerate(a, regen_choice)
        if low_scholar is not None:
            low_scholar.on_step_complete(actor_id)
        # The actual completed G0 Step 2 is the only legal EX-LR-01
        # arming window. A caller's callback does not create a second Step.
        if on_regeneration_complete is not None:
            if not callable(on_regeneration_complete):
                raise ValueError("Regeneration completion policy must be callable")
            on_regeneration_complete(self, actor_id)
        if self.g3 is not None and getattr(self.g3, "medium_life", None) is not None:
            self.g3.medium_life.finish_regen(actor_id)
        self.pending_regeneration = None
        # G4 handles genuine Step 3 scheduled toxin harm after the sole
        # Step 2 regeneration, before Step 4 establishes Turn resources.
        if self.g4 is not None:
            self.g4.on_turn_start(actor_id)
        a.ap_remaining = (0 if a.hp <= 0 or a.dead
                          else a.ap_total - a.blink_debt_due)
        # Exact named ordinary-MP impairments change the newly established
        # own-turn allowance; neither virtual toxin intervals nor another
        # creature's turn can grant an extra movement refresh.
        mp_penalty=(self.g4.toxins.modifier(actor_id,"mp")
                    if self.g4 is not None else 0)
        a.mp_remaining = max(0,12+mp_penalty)
        scholar=(getattr(self.g3,"medium_scholar",None)
                 if self.g3 is not None else None)
        if scholar is not None:
            scholar.on_turn_resources(actor_id)
        a.blink_debt_due = a.blink_debt_next
        a.blink_debt_next = 0
        self.log("turn_resources", actor=actor_id, ap=a.ap_remaining,
                 mp=a.mp_remaining)
        if self.g1 is not None:
            self.g1.on_turn_start(actor_id)
        if self.g2 is not None:
            self.g2.on_turn_start(actor_id)
        self.check()

    def end_turn(self):
        if self.current is None or self.pending_regeneration is not None:
            raise ValueError("No resolved open turn")
        # G5 precommits every sequence slot. Never let a caller bypass
        # SourceMelee by ending G0 directly (or through a G4.5 bridge)
        # and thereby erase a paid but still unresolved attack. The
        # optional hook must run BEFORE round/turn/resources mutate.
        if getattr(self, "g5", None) is not None:
            self.g5.assert_turn_completion_allowed(self.current)
        a = self.actors[self.current]
        if self.g1 is not None and self.g1.pounce is not None and self.g1.pounce.hunter_id == a.id:
            raise ValueError("Resolve or explicitly abort ongoing Pounce before turn end")
        self.log("turn_end", actor=a.id, unused_ap=a.ap_remaining, unused_mp=a.mp_remaining)
        self.seen_sequences = {key for key in self.seen_sequences if key[0] != a.id}
        a.ap_remaining = 0
        a.mp_remaining = 0
        self.cursor += 1
        self.current = None
        if self.cursor == len(self.order):
            # Close the round even when the scenario never begins another.
            # No authored end-of-round effect executor exists in G0; after
            # that deferred boundary, Opportunity Response expires NOW.
            expired = [a.id for a in self.actors.values()
                       if a.opportunity_active]
            self.log("round_end", effects="authored effects deferred",
                     expired_opportunity_response=expired)
            for participant in self.actors.values():
                participant.opportunity_active = False

    def spend_ap(self, actor_id, kind, *, label):
        if self.current != actor_id or self.pending_regeneration is not None:
            raise ValueError("Only ready current actor may spend Turn AP")
        # G5 pays all ordinary Attack Sequence slots up front. A later
        # Physical/Projection/General/Full spend (including reserve()) must
        # not supersede any unresolved slot: G4.5 would reject that now-stale
        # action and the turn completion gate would leave the scene stranded.
        # During declare_sequence the G5 attestation is not created until
        # all canonical G0 payments and defenses have been committed, so
        # this hook permits those original payments but blocks later ones.
        if getattr(self, "g5", None) is not None:
            self.g5.assert_ap_commitment_allowed(actor_id)
        a = self.actors[actor_id]
        if a.dead or a.hp <= 0:
            raise ValueError("Dying/dead actors cannot take ordinary voluntary actions")
        if (self.g1 is not None and self.g1.pounce is not None
                and self.g1.pounce.hunter_id == actor_id
                and not self.g1._internal_pounce_spend):
            raise ValueError("Complete or abort active Pounce before another own action")
        costs = {"physical": a.physical_ap, "projection": a.projection_ap,
                 "general": 24, "full": a.ap_total}
        if kind not in costs or costs[kind] is None:
            raise ValueError("Action class not available to this source")
        cost = costs[kind]
        if kind == "full" and a.ap_remaining != a.ap_total:
            raise ValueError("Full Action requires entire untouched Turn AP allotment")
        if a.ap_remaining < cost:
            raise ValueError("Insufficient Turn AP")
        a.ap_remaining -= cost
        self.log("action_committed", actor=actor_id, action_class=kind, label=label,
                 ap_spent=cost, ap_remaining=a.ap_remaining)
        if self.g1 is not None:
            self.g1.on_own_action(actor_id, label=label)
        return cost

    def spend_vp(self, actor_id, points, *, mode, label):
        a = self.actors[actor_id]
        _integer(points, "VP spend", 1)
        if mode not in ("spent", "committed"):
            raise ValueError("VP mode must be explicit")
        if points > a.vp_available:
            raise ValueError("Insufficient Available VP")
        a.vp_available -= points
        if mode == "spent":
            a.vp_spent += points
        else:
            a.vp_committed += points
        self.log("vp_transition", actor=actor_id, mode=mode, points=points, label=label)
        self.check()

    def release_vp(self, actor_id, points, *, label):
        a = self.actors[actor_id]
        _integer(points, "release", 1)
        if points > a.vp_committed:
            raise ValueError("Cannot refund Spent VP")
        # G3 owns the VP committed to each *still active* effect. Refunding
        # that share through this generic G0 entry point would leave a
        # paid spell in place with no reservation, including the Sentry's
        # enhanced sword. G3._end removes the effect BEFORE refunding its
        # committed VP, so legitimate expiration, sword break, and voluntary
        # release keep their existing source-driven timing.
        if self.g3 is not None:
            owned = sum(effect.committed for effect in self.g3.effects.values()
                        if effect.caster == actor_id)
            if owned < 0 or owned > a.vp_committed:
                raise ValueError("Active G3 effect has invalid committed VP funding")
            if a.vp_committed - points < owned:
                raise ValueError("Cannot refund VP owned by active G3 effects")
        ward=(getattr(self.g4,"medium_gifted",None)
              if self.g4 is not None else None)
        if ward is not None and actor_id==ward.caster:
            # A generic G0 release cannot strand the still-established Ward.
            owned_ward=sum(c.grade for c in ward.conduits)
            g3_owned = (sum(effect.committed for effect in self.g3.effects.values()
                            if effect.caster == actor_id)
                        if self.g3 is not None else 0)
            if a.vp_committed - points < owned_ward + g3_owned:
                raise ValueError("Cannot refund VP owned by Ward/G3 effects")
        a.vp_committed -= points
        a.vp_available += points
        self.log("vp_release", actor=actor_id, points=points, label=label)
        self.check()

    def defense(self, actor_id, choice, *, attack_key, projectile=False):
        a = self.actors[actor_id]
        if choice not in VALID_DEFENSES:
            raise ValueError("Defense must be declared before attack roll")
        if a.hp <= 0 and choice != "take_hit":
            raise ValueError("Unconscious/dead actor cannot actively Guard or Dodge")
        if projectile:
            raise UnresolvedDecision("G2 must validate projectile Guard/Dodge and lane first")
        if choice == "guard":
            if (a.source.source_id in ("S","T")
                    and (self.g1 is None or
                         not self.g1.genuine_scholar_sword_ready(actor_id))):
                raise ValueError("Scholar Sword Guard requires current wielding")
            if (a.guard_remaining == 0 or a.guard_value is None
                    or not a.guard_instrument or not a.ready_guard):
                raise ValueError("Cannot Guard without ready legal instrument/capacity")
            a.guard_remaining -= 1
            value = a.guard_value
        elif choice == "dodge":
            # Neurotoxin affects Dodge only, never source Agility or Guard.
            toxin_dodge = (self.g4.toxins.modifier(actor_id,"dodge")
                           if self.g4 is not None else 0)
            value = 10 + min(a.agility, 4) + a.awareness - a.dodge_pressure + toxin_dodge
            a.dodge_pressure += 2
        else:
            value = None  # Take Hit is not an invented guaranteed-hit melee roll.
        self.log("defense_assigned", actor=actor_id, defense=choice,
                 attack_key=attack_key, defense_value=value,
                 guard_remaining=a.guard_remaining, dodge_pressure=a.dodge_pressure)
        return value

    def declare_sequence(self, attacker, target, profiles, defenses):
        if self.current != attacker or self.pending_regeneration is not None:
            raise ValueError("Only ready current actor declares ordinary sequence")
        # G5's source-bound AP slots cannot be superseded by a second
        # target's G0 sequence. Guard the native entry point as well as
        # SourceMelee.declare(), before spending AP or defender resources.
        if getattr(self,"g5",None) is not None:
            self.g5.assert_sequence_declaration_allowed(attacker)
            # Native G0 has no post-commit G5 attestation callback.
            # A direct declaration would pay AP/Guard then escape the
            # G5 pending-slot/end-turn gate. Only the G5 adapter may
            # enter this synchronous declaration window.
            if not self.g5._native_sequence_authorized:
                raise UnresolvedDecision(
                    "G5 requires SourceMelee.declare for tracked attack sequences")
        a, t = self.actors[attacker], self.actors[target]
        # A same-turn 0-HP crossing can invalidate an attacker after Turn AP
        # was established. Rejection MUST precede the sequence lock and all
        # AP/Guard/Dodge commitment, so later legal recovery can retry.
        if a.dead or a.hp <= 0:
            raise ValueError("Dying/dead attacker cannot declare ordinary attacks")
        if (attacker, target) in self.seen_sequences:
            raise ValueError("Second ordinary Attack Sequence to same target forbidden")
        if not profiles or len(profiles) != len(defenses):
            raise ValueError("Commit all declared profiles and defenses together")
        if any(p not in a.source.attack_profiles for p in profiles):
            raise UnresolvedDecision("Profile is not a supported native G0 fixture attack")
        # The profile catalogue is not itself an eligibility grant. Special
        # Pounce/Horn Drive require G1 manoeuvre/contact state, and an enhanced
        # Sentry sword profile requires its actually active Chosen Reserve.
        if a.source.source_id == "B06-EN-03" and not (
                getattr(self, "g5", None) is not None
                and self.g5._native_sequence_authorized
                and all(p in ("B06-AT-04", "B06-AT-05") for p in profiles)):
            raise UnresolvedDecision("Hunter attack needs G6 verified frontal contact and manoeuvre validation")
        for profile_id, required, inactive in a.source.attack_requirements:
            if profile_id not in profiles:
                continue
            if required is not None and required not in a.maintained:
                raise ValueError("Attack profile requires active effect: " + required)
            if inactive is not None and inactive in a.maintained:
                raise ValueError("Attack profile requires inactive effect: " + inactive)
        if a.ap_remaining < len(profiles) * a.physical_ap:
            raise ValueError("Not enough AP for full Attack Sequence")
        if any(x not in VALID_DEFENSES for x in defenses):
            raise ValueError("Invalid defense declaration")
        if t.hp <= 0 and any(d != "take_hit" for d in defenses):
            raise ValueError("Dying/dead target cannot actively defend a sequence")
        # Validate the actual Guard instrument before any Attack Sequence
        # AP is paid, the target is locked, or defenses are assigned.
        # Encounter.defense() independently checks this too, but waiting
        # until that call would strand a paid, untracked sequence.
        if defenses.count("guard") > t.guard_remaining or (
            "guard" in defenses and (
                t.guard_value is None or not t.ready_guard
                or not t.guard_instrument
                or (t.source.source_id in ("S","T") and
                    (self.g1 is None or
                     not self.g1.genuine_scholar_sword_ready(target))))):
            raise ValueError("Insufficient legal Guard assignments")
        self.seen_sequences.add((attacker, target))
        for i, p in enumerate(profiles):
            self.spend_ap(attacker, "physical", label=f"sequence:{p}:{i}")
        self.log("attack_sequence_committed", attacker=attacker, target=target,
                 profiles=list(profiles), defenses=list(defenses))
        for i, choice in enumerate(defenses):
            self.defense(target, choice, attack_key=f"{attacker}:{target}:{i}")
        self.log("unresolved_attack_roll", attacker=attacker, target=target,
                 reason="G0 commits declarations and defenses; G5 adjudicates physical hit/damage")
        self.check()

    def reserve(self, actor_id, trigger_key, label, *, action_kind="physical"):
        self.spend_ap(actor_id, action_kind, label=f"interception:{label}")
        self.reservations.append(Reservation(actor_id, trigger_key, label,
                                             len(self.reservations)))
        self.log("interception_reserved", actor=actor_id, trigger=trigger_key,
                 label=label)

    def is_live_spontaneous(self, trigger, response):
        """True only inside this exact native response's active callback."""
        current = self._live_spontaneous_response
        return (current is not None and current[0] is trigger
                and current[1] is response)

    def response_window(self, trigger, *, on_interception, spontaneous=(),
                        on_spontaneous=None, after_interceptions=None):
        """Run an original trigger and expire its unused G3 preflight on exit.

        Cleanup covers Interception cancellation, normal resolution, errors,
        and nested windows without touching claims for distinct Trigger
        objects that happen to reuse the same external text key.
        """
        try:
            return self._response_window(
                trigger,on_interception=on_interception,
                spontaneous=spontaneous,on_spontaneous=on_spontaneous,
                after_interceptions=after_interceptions)
        finally:
            if self.g3 is not None:
                self.g3.on_response_window_closed(trigger)

    def _response_window(self, trigger, *, on_interception, spontaneous=(),
                         on_spontaneous=None, after_interceptions=None):
        """Caller resolves independently authorized effects; G0 never invents Interrupt.

        Interception callback may call nested response_window() or set trigger.legal
        from a separately source-validated effect. No spontaneous response is
        collected after the first legality recheck fails.
        """
        if self.pending_regeneration is not None:
            raise UnresolvedDecision("Resolve pending Regeneration Step before responding")
        # The response window belongs to an existing round, not the gap
        # after its Round End. This also prevents a new Reaction on a closed
        # round even if the combatant had never used it.
        if self.round == 0 or self.cursor == len(self.order):
            raise ValueError("Cannot open response window outside an active round")
        matches = []
        used = set()
        for r in self.reservations:
            if r.trigger_key == trigger.key and r.actor_id not in used:
                matches.append(r)
                used.add(r.actor_id)
        self.reservations = [r for r in self.reservations if r not in matches]
        matches.sort(key=lambda r: self.order.index(r.actor_id))
        self.log("response_window_open", trigger=trigger.key)
        for r in matches:
            self.log("interception_released", actor=r.actor_id, label=r.label,
                     trigger=trigger.key)
            on_interception(self, trigger, r)
        # Validate the final geometry only after every same-trigger
        # Interception. An intermediate state may change again before
        # the original trigger's single canonical legality recheck.
        if after_interceptions is not None:
            after_interceptions(self, trigger)
        self.log("trigger_rechecked_after_interceptions", trigger=trigger.key,
                 legal=trigger.legal)
        if not trigger.legal:
            self.log("trigger_cancelled_before_spontaneous", trigger=trigger.key)
            return False
        # A callable policy is evaluated only AFTER all matching Interceptions
        # and the first original-trigger legality recheck. This permits G1 to
        # derive eligible Movement Opportunities from the resulting geometry
        # without incorrectly cancelling the *original movement step*.
        declared = spontaneous(self, trigger) if callable(spontaneous) else spontaneous
        if declared is None:
            raise UnresolvedDecision("Spontaneous policy must return explicit choices")
        if declared and on_spontaneous is None:
            raise ValueError("Spontaneous choices require effect resolution")
        # Validate whole declaration set before paying any Reaction. Multiple
        # same-window responses from one actor may need a separate authored
        # permission, which this G0 subset deliberately does not provide.
        choices = sorted(declared, key=lambda c: self.order.index(c.actor_id))
        if len({c.actor_id for c in choices}) != len(choices):
            raise UnresolvedDecision("Multiple simultaneous responses by one actor")
        for c in choices:
            a = self.actors[c.actor_id]
            # Round Begin refreshed the capacity independently of HP; only
            # a currently conscious/alive actor can actually declare a
            # spontaneous Reaction or Opportunity Attack.
            if a.dead or a.hp <= 0:
                raise ValueError("Dying/dead actor cannot declare a response")
            if c.kind not in ("reaction", "opportunity"):
                raise ValueError("Unknown response category")
            if c.kind == "reaction" and not a.reaction_available:
                raise ValueError("Reaction already used")
            if c.kind == "opportunity":
                if a.opportunity_used >= a.ap_total // a.physical_ap:
                    raise ValueError("Opportunity capacity exhausted")
                if not a.opportunity_active and not a.reaction_available:
                    raise ValueError("First Opportunity needs Reaction")
        for c in choices:
            a = self.actors[c.actor_id]
            if c.kind == "reaction":
                if not a.reaction_available:
                    raise ValueError("Reaction already used")
                a.reaction_available = False
            elif c.kind == "opportunity":
                capacity = a.ap_total // a.physical_ap
                if a.opportunity_used >= capacity:
                    raise ValueError("Opportunity capacity exhausted")
                if not a.opportunity_active:
                    if not a.reaction_available:
                        raise ValueError("First Opportunity needs Reaction")
                    a.reaction_available = False
                    a.opportunity_active = True
                a.opportunity_used += 1
            else:
                raise ValueError("Unknown response category")
            self.log("spontaneous_committed", actor=c.actor_id, response_kind=c.kind,
                     trigger=trigger.key, label=c.label)
        for c in choices:
            # G0 commits all capacities before executing initiative-ordered
            # responses. Mark ONLY this live callback as the authority for
            # G3 pre-roll effect application. The finally block prevents
            # stale authorization after returns, exceptions, or nested G0
            # response windows.
            previous = self._live_spontaneous_response
            self._live_spontaneous_response = (trigger, c)
            try:
                on_spontaneous(self, trigger, c)
            finally:
                self._live_spontaneous_response = previous
        self.log("trigger_rechecked_after_responses", trigger=trigger.key,
                 legal=trigger.legal)
        if trigger.legal:
            self.log("trigger_ready_to_resolve", trigger=trigger.key)
        else:
            self.log("trigger_cancelled_after_spontaneous", trigger=trigger.key)
        self.check()
        return trigger.legal
