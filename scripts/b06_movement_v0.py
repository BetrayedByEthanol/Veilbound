"""B06 G1: bounded native grid/footprint movement and physical contact.

Consumes G0 Encounter; never computes combat damage, Balance rolls, spell
casting, projectile flight or AI routes. Route/response choices remain explicit.
The 4,096 signed Hunter Phase-3 first stops are never modified or replayed.
"""
from dataclasses import dataclass
from math import ceil

from scripts.b06_encounter_state_v0 import (
    Reservation, Response, Trigger, UnresolvedDecision,
)

TERRAIN = {"normal": 0, "difficult": 2, "severe": 4}
HEADINGS = ((1, 0), (-1, 0), (0, 1), (0, -1))
AROUND = tuple((x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)
               if x or y)


@dataclass
class MotionReservation:
    actor_id: str
    trigger_key: str
    label: str
    reserved_mp: int
    spent_mp: int = 0
    steps: int = 0


@dataclass
class PounceRun:
    hunter_id: str
    target_id: str
    heading: tuple
    steps: int = 0
    committed: bool = False
    spent_mp: int = 0


class GridMovement:
    """Finite authored 2-D map, native G0 actor positions and shared event log.

    Direct step/pivot is allowed only on the mover's own established turn.
    MP Interception routes run out of turn against a precommitted MP pool.
    Normal movement and pivot spend MP on success, never on illegal attempts.
    """

    def __init__(self, encounter, *, width, height, walls=(), terrain=None,
                 scene_id="G1-authored-grid"):
        if encounter.g1 is not None:
            raise ValueError("G1 grid is already installed")
        if type(width) is not int or type(height) is not int or min(width, height) < 1:
            raise ValueError("Finite positive grid dimensions required")
        self.e = encounter
        self.width, self.height = width, height
        self.walls = frozenset(tuple(p) for p in walls)
        self.terrain = {tuple(k): v for k, v in (terrain or {}).items()}
        self.scene_id = scene_id
        for c in self.walls:
            if not self.inside(c):
                raise ValueError("Wall outside authored grid")
        for c, kind in self.terrain.items():
            if not self.inside(c) or c in self.walls or kind not in TERRAIN:
                raise ValueError("Invalid authored terrain cell")
        for actor in encounter.actors.values():
            if not self.valid_footprint(actor, actor.occupied):
                raise ValueError("Invalid initial G1 actor placement")
        self.segment = {a: 0 for a in encounter.actors}
        self.provoked = {a: set() for a in encounter.actors}
        self.motion = {}
        self.next_reservation = 0
        self.pounce = None
        encounter.g1 = self
        encounter.log("g1_map_installed", scene=scene_id, width=width, height=height,
                      walls=sorted(self.walls),
                      terrain=sorted((c, v) for c, v in self.terrain.items()),
                      body_cells={a.id: dict(zip(a.footprint, a.occupied))
                                  for a in encounter.actors.values()})

    def inside(self, c):
        return (len(c) == 2 and all(type(n) is int for n in c)
                and 0 <= c[0] < self.width and 0 <= c[1] < self.height)

    def valid_footprint(self, actor, dest, *, ally_transit=False):
        if len(dest) != len(actor.footprint) or len(set(dest)) != len(dest):
            return False
        for c in dest:
            if not self.inside(c) or c in self.walls:
                return False
            for other in self.e.actors.values():
                if other.id == actor.id or c not in other.occupied:
                    continue
                if other.team != actor.team or not ally_transit:
                    return False
        return True

    def body_cell(self, actor_id, label):
        a = self.e.actors[actor_id]
        if label not in a.footprint:
            raise ValueError("Unknown stable anatomical cell label")
        return a.occupied[a.footprint.index(label)]

    def occupants(self, at):
        return tuple(a.id for a in self.e.actors.values() if at in a.occupied)

    def front(self, actor_id):
        a = self.e.actors[actor_id]
        if a.footprint != ("head", "rear"):
            raise ValueError("Frontal contact requires authored head/rear Hunter")
        head, rear = a.occupied
        heading = (head[0] - rear[0], head[1] - rear[1])
        if heading not in HEADINGS:
            raise ValueError("Hunter body must be rigid adjacent and cardinal")
        return (head[0] + heading[0], head[1] + heading[1])

    def reach(self, actor_id):
        a = self.e.actors[actor_id]
        # Ordinary adjacent reach of *each* cell; no bonus for body length.
        return { (c[0]+d[0], c[1]+d[1])
                 for c in a.occupied for d in AROUND
                 if (c[0]+d[0], c[1]+d[1]) not in a.occupied }

    def threatens(self, actor_id, at):
        a = self.e.actors[actor_id]
        if a.dead or a.hp <= 0:
            return False
        gear = dict(a.source.equipment)
        melee = (a.source.source_id == "B06-EN-03"
                 or any(state == "wielded" and any(
                     term in name.lower()
                     for term in ("sword", "mace", "dagger", "axe", "spear", "club"))
                     for name, state in gear.items()))
        if not melee:
            return False
        return at in self.reach(actor_id)

    def melee_contact(self, attacker_id, target_id, *, hunter_front=False):
        a, t = self.e.actors[attacker_id], self.e.actors[target_id]
        if a.dead or a.hp <= 0 or t.dead:
            return False
        if hunter_front:
            return (a.source.source_id == "B06-EN-03"
                    and len(t.occupied) == 1
                    and self.front(attacker_id) == t.occupied[0])
        return bool(self.reach(attacker_id).intersection(t.occupied))

    def preview(self, actor_id, *, delta=None, pivot=None, clockwise=None,
                cautious=False, reserved=False, ally_transit=False):
        a = self.e.actors[actor_id]
        old = a.occupied
        if delta is not None and pivot is not None:
            raise ValueError("Choose translation or pivot")
        if delta is not None:
            if tuple(delta) not in AROUND:
                raise ValueError("One 8-neighbor step required")
            dx, dy = delta
            dest = tuple((x+dx, y+dy) for x, y in old)
            # Diagonal blocked corners for EACH virtual footprint cell. A
            # former square of the same body is not an obstacle to itself.
            if dx and dy:
                for x, y in old:
                    blockers = ((x+dx, y), (x, y+dy))
                    if all(self._solid(c, actor_id) for c in blockers):
                        raise ValueError("Blocked diagonal corner / body sweep")
            kind = "diagonal" if dx and dy else "orthogonal"
            base = (3 if kind == "diagonal" else 2) * (2 if cautious else 1)
            cell_costs = [base + TERRAIN.get(self.terrain.get(c, "normal"), 0)
                          for c in dest]
            cost = (sum(cell_costs) + len(cell_costs) - 1) // len(cell_costs)
        elif pivot is not None:
            if len(a.occupied) != 2 or a.footprint != ("head", "rear"):
                raise UnresolvedDecision("Only straight 1x2 Hunter 90-degree pivot authored")
            if pivot not in a.footprint or type(clockwise) is not bool:
                raise ValueError("Choose anchored anatomical cell and direction")
            index = a.footprint.index(pivot)
            moving = 1-index
            ax, ay = old[index]
            x, y = old[moving]
            dx, dy = x-ax, y-ay
            if (dx, dy) not in HEADINGS:
                raise ValueError("Hunter rigid cardinal orientation required")
            rotated = (dy, -dx) if clockwise else (-dy, dx)
            final = (ax+rotated[0], ay+rotated[1])
            # The swept outside corner must clear even when diagonal blocked-
            # corner's second orthogonal side is the creature's own anchor.
            outside = (x+rotated[0], y+rotated[1])
            if self._solid(outside, actor_id):
                raise ValueError("Pivot swept corner obstructed")
            dest = list(old)
            dest[moving] = final
            dest = tuple(dest)
            cost = (6 if cautious else 3) + TERRAIN.get(
                self.terrain.get(final, "normal"), 0)
            kind = "pivot"
        else:
            raise ValueError("One translation or pivot required")
        if not self.valid_footprint(a, dest, ally_transit=ally_transit):
            raise ValueError("Destination blocked, outside map, or occupied")
        entered = set(dest) - set(old)
        allies = {c for c in entered
                  if any(self.e.actors[oid].team == a.team
                         for oid in self.occupants(c) if oid != actor_id)}
        cost += 2*len(allies)
        # A single step cannot end on an ally: require authored continuous
        # transit route and validate its final clear destination as one unit.
        if allies and not ally_transit:
            raise UnresolvedDecision("Allied transit requires declared continuous route")
        return dest, cost, kind, allies

    def _solid(self, c, actor_id):
        return (not self.inside(c) or c in self.walls
                or any(x.id != actor_id and c in x.occupied
                       for x in self.e.actors.values()))

    def on_turn_start(self, actor_id):
        # G0 already expired reservations at this boundary. No refund: MP
        # was removed at commit. Discard G1 bookkeeping for those labels.
        expired = [key for key, r in self.motion.items() if r.actor_id == actor_id]
        for key in expired:
            r = self.motion.pop(key)
            self.e.log("g1_reserved_mp_expired", actor=actor_id, label=key,
                       unused_mp=r.reserved_mp-r.spent_mp)
        self.provoked[actor_id].clear()
        self.segment[actor_id] += 1

    def on_own_action(self, actor_id, *, label):
        # Pounce's AP commitment at its own legal threshold is part of one
        # fixed-heading approach, not an intervening action/segment break.
        if self.pounce and self.pounce.hunter_id == actor_id and label.startswith("g1:pounce:"):
            return
        self.break_segment(actor_id, reason="own_action")

    def break_segment(self, actor_id, *, reason):
        self.segment[actor_id] += 1
        self.provoked[actor_id].clear()
        self.e.log("g1_segment_break", actor=actor_id, reason=reason,
                   new_segment=self.segment[actor_id])

    def _threats(self, mover_id, dest, cautious):
        if cautious:
            return ()
        mover = self.e.actors[mover_id]
        left = set(mover.occupied) - set(dest)
        if not left:
            return ()
        return tuple(oid for oid in self.e.order
                     if oid != mover_id and self.e.actors[oid].team != mover.team
                     and oid not in self.provoked[mover_id]
                     and any(self.threatens(oid, c) for c in left))

    def _budget(self, actor_id, reserved):
        return reserved.reserved_mp-reserved.spent_mp if reserved else self.e.actors[actor_id].mp_remaining

    def _commit_mp(self, actor_id, cost, reserved):
        if reserved:
            reserved.spent_mp += cost
            reserved.steps += 1
        else:
            self.e.actors[actor_id].mp_remaining -= cost

    def _movement(self, actor_id, *, delta=None, pivot=None, clockwise=None,
                  cautious=False, reserved=None, trigger_key=None,
                  responses=(), interceptor_routes=None, on_response=None):
        a = self.e.actors[actor_id]
        if a.hp <= 0 or a.dead:
            raise ValueError("Incapacitated creature cannot voluntarily move")
        if reserved is None and (self.e.current != actor_id or self.e.pending_regeneration):
            raise ValueError("Normal movement requires ready current actor turn")
        if reserved is not None and self.e.current == actor_id:
            raise ValueError("Movement Interception cannot release on own turn")
        if self.pounce and self.pounce.hunter_id == actor_id:
            if pivot is not None or cautious or reserved is not None or delta != self.pounce.heading:
                raise ValueError("Pounce is fixed-head-forward straight translation")
        dest, cost, kind, allies = self.preview(
            actor_id, delta=delta, pivot=pivot, clockwise=clockwise,
            cautious=cautious)
        if self._budget(actor_id, reserved) < cost:
            raise ValueError("Insufficient movement MP")
        initial = a.occupied
        threats = self._threats(actor_id, dest, cautious)
        wanted = tuple(responses)
        if any(not isinstance(c, Response) or c.kind != "opportunity"
               or c.actor_id not in threats for c in wanted):
            raise ValueError("Explicit Opportunity choice not eligible from departure")
        if len({c.actor_id for c in wanted}) != len(wanted):
            raise ValueError("One Movement Opportunity per enemy per segment")
        key = trigger_key or f"g1:{actor_id}:step:{len(self.e.ledger)}"
        trigger = Trigger(key, actor_id, actor_id)
        interception_paths = interceptor_routes or {}

        def apply_interception(e, tr, reservation):
            entry = self.motion.pop(reservation.label, None)
            if entry is None:
                raise UnresolvedDecision("Non-movement Interception requires authored action resolver")
            route = interception_paths.get(reservation.label, ())
            steps_before = entry.steps
            for step in route:
                self._movement(entry.actor_id, delta=tuple(step), reserved=entry,
                               trigger_key=f"{key}:intercept:{entry.steps}",
                               interceptor_routes=interception_paths)
            e.log("g1_movement_interception_resolved", actor=entry.actor_id,
                  label=entry.label, committed_mp=entry.reserved_mp,
                  consumed_mp=entry.spent_mp, completed_steps=entry.steps)
            if entry.steps > steps_before and self.e.current is not None:
                self.break_segment(self.e.current, reason="movement_interception")
            # Original declaration must be rechecked against changed map;
            # if geometry invalidated it, precommitted costs are not refunded.
            try:
                self.preview(actor_id, delta=delta, pivot=pivot,
                             clockwise=clockwise, cautious=cautious)
            except (ValueError, UnresolvedDecision):
                tr.legal = False

        def apply_response(e, tr, response):
            e.log("g1_movement_opportunity_pending", attacker=response.actor_id,
                  mover=actor_id, trigger=tr.key, outcome="G5_attack_unresolved")
            if on_response:
                on_response(e, tr, response)

        # Give the native response framework the pre-step event: Interceptions,
        # first legality recheck, legal spontaneous Opportunity, second recheck.
        can_proceed = self.e.response_window(
            trigger, on_interception=apply_interception,
            spontaneous=wanted, on_spontaneous=apply_response if wanted else None)
        if not can_proceed:
            self.e.log("g1_step_cancelled", actor=actor_id, trigger=key,
                       reason="response_or_geometry_changed", mp_charged=0)
            return False
        # A response may cause a no-longer-passable destination or capacity
        # decrease. Revalidate before atomic state change.
        latest, new_cost, _, _ = self.preview(
            actor_id, delta=delta, pivot=pivot, clockwise=clockwise,
            cautious=cautious)
        if a.occupied != initial or latest != dest or new_cost != cost:
            self.e.log("g1_step_cancelled", actor=actor_id, trigger=key,
                       reason="original_position_or_cost_changed", mp_charged=0)
            return False
        if self._budget(actor_id, reserved) < cost or a.hp <= 0 or a.dead:
            self.e.log("g1_step_cancelled", actor=actor_id, trigger=key,
                       reason="response_removed_mobility", mp_charged=0)
            return False
        if self.pounce and self.pounce.hunter_id == actor_id:
            run = self.pounce
            if not run.committed and run.spent_mp + cost > 18:
                self.e.spend_ap(actor_id, "physical", label="g1:pounce:cutoff")
                run.committed = True
        self._commit_mp(actor_id, cost, reserved)
        a.occupied = latest
        self.provoked[actor_id].update(threats)
        if self.pounce and self.pounce.hunter_id == actor_id:
            self.pounce.steps += 1
            self.pounce.spent_mp += cost
        self.e.log("g1_movement_step", actor=actor_id,
                   old=initial, new=latest, kind=kind,
                   direction=delta, pivot_anchor=pivot, clockwise=clockwise,
                   cautious=cautious, cost=cost, mp_remaining=self._budget(actor_id, reserved),
                   opportunity_sources=threats, segment=self.segment[actor_id],
                   reserved=bool(reserved))
        self.e.check()
        return True

    def step(self, actor_id, delta, **kwargs):
        return self._movement(actor_id, delta=tuple(delta), **kwargs)

    def pivot(self, actor_id, anchor, *, clockwise, **kwargs):
        return self._movement(actor_id, pivot=anchor, clockwise=clockwise, **kwargs)

    def move_route(self, actor_id, deltas, *, cautious=False):
        """Atomic no-response continuous allied transit; otherwise ordinary steps.

        A route crossing an ally is prevalidated in full and committed only
        if it has no third-party response windows or contingent mid-route
        choices. Those require a later dedicated G1 policy rather than
        ending illegally on an ally after a cancelled final step.
        """
        moves = tuple(tuple(d) for d in deltas)
        a = self.e.actors[actor_id]
        if not moves:
            raise ValueError("Nonempty declared route required")
        if self.pounce and self.pounce.hunter_id == actor_id:
            return all(self.step(actor_id, d) for d in moves)
        old = a.occupied
        total = 0
        transient = False
        simulated = []
        try:
            for i, direction in enumerate(moves):
                new, cost, kind, ally = self.preview(
                    actor_id, delta=direction, cautious=cautious, ally_transit=True)
                if ally:
                    transient = True
                    if i == len(moves)-1:
                        raise ValueError("Cannot end movement on ally")
                if transient and (self._threats(actor_id, new, cautious)
                                  or self.e.reservations):
                    raise UnresolvedDecision("Allied transit with responses needs explicit route adjudication")
                simulated.append((old, new, cost, kind, ally))
                total += cost
                a.occupied = new
                old = new
        finally:
            a.occupied = simulated[0][0] if simulated else old
        if not transient:
            return all(self.step(actor_id, d, cautious=cautious) for d in moves)
        if self.e.current != actor_id or self.e.pending_regeneration:
            raise ValueError("Allied transit requires active turn")
        if total > a.mp_remaining:
            raise ValueError("Insufficient MP for continuous allied transit")
        for before, after, cost, kind, ally in simulated:
            self.e.log("g1_allied_transit_step", actor=actor_id,
                       old=before, new=after, cost=cost,
                       entered_allies=sorted(ally), mode="cautious" if cautious else "normal")
        a.occupied = simulated[-1][1]
        a.mp_remaining -= total
        self.e.log("g1_allied_transit_finished", actor=actor_id,
                   steps=len(simulated), cost=total, remaining_mp=a.mp_remaining)
        self.e.check()
        return True

    def reserve_movement(self, actor_id, trigger_key, mp, *, label):
        if self.e.current != actor_id or self.e.pending_regeneration:
            raise ValueError("Reserve MP on ready own turn only")
        if self.pounce is not None and self.pounce.hunter_id == actor_id:
            raise ValueError("Pounce prohibits new Movement Interception reservations")
        a = self.e.actors[actor_id]
        if type(mp) is not int or mp < 1 or mp > a.mp_remaining:
            raise ValueError("Positive available MP required")
        if not trigger_key or not label:
            raise ValueError("Meaningful named external trigger required")
        self.next_reservation += 1
        key = f"G1-MP:{self.next_reservation}:{label}"
        a.mp_remaining -= mp
        r = MotionReservation(actor_id, trigger_key, key, mp)
        self.motion[key] = r
        self.e.reservations.append(Reservation(actor_id, trigger_key, key,
                                               len(self.e.reservations)))
        self.e.log("g1_movement_mp_reserved", actor=actor_id, trigger=trigger_key,
                   label=key, mp=mp, unreserved_mp=a.mp_remaining)
        return key

    def start_pounce(self, hunter_id, target_id):
        a = self.e.actors[hunter_id]
        if self.pounce is not None:
            raise ValueError("Pounce already active")
        if (a.source.source_id != "B06-EN-03" or
                self.e.current != hunter_id or self.e.pending_regeneration):
            raise ValueError("Pounce requires Hunter on own ready turn")
        if a.mp_remaining != 12 or any(r.actor_id == hunter_id for r in self.motion.values()):
            raise ValueError("Pounce must begin before movement or MP reservation")
        if a.ap_remaining < a.physical_ap:
            raise ValueError("Pounce needs one available Physical Action")
        head, rear = a.occupied
        heading = (head[0]-rear[0], head[1]-rear[1])
        if heading not in HEADINGS:
            raise ValueError("Pounce needs cardinal head-forward body")
        if (target_id not in self.e.actors or
                len(self.e.actors[target_id].occupied) != 1 or
                self.e.actors[target_id].team == a.team):
            raise ValueError("Pounce target must be one-square opposing creature")
        a.mp_remaining = 24
        self.pounce = PounceRun(hunter_id, target_id, heading)
        self.e.log("g1_pounce_declared", hunter=hunter_id, target=target_id,
                   heading=heading, max_mp=24, cutoff_mp=18)
        return heading

    def pounce_contact(self, *, defense="take_hit", interceptor_routes=None,
                       responses=(), on_response=None, trigger_key=None):
        run = self.pounce
        if run is None:
            raise ValueError("No Pounce approach")
        a = self.e.actors[run.hunter_id]
        t = self.e.actors[run.target_id]
        if run.steps < 3 or not self.melee_contact(a.id, t.id, hunter_front=True):
            raise ValueError("Pounce needs three translated steps and frontal contact")
        if a.hp <= 0 or a.dead or t.dead:
            raise ValueError("Pounce participants no longer eligible")
        if (a.id, t.id) in self.e.seen_sequences:
            raise ValueError("Second attack on same target prohibited")
        if defense not in ("take_hit", "dodge", "guard"):
            raise ValueError("Invalid Bite defense")
        if t.hp <= 0 and defense != "take_hit":
            raise ValueError("Dying target cannot actively defend")
        if defense == "guard" and (
                not t.ready_guard or t.guard_instrument is None
                or t.guard_value is None or t.guard_remaining == 0):
            raise ValueError("Illegal Bite Guard")
        if not run.committed:
            self.e.spend_ap(a.id, "physical", label="g1:pounce:bite")
            run.committed = True
        self.e.seen_sequences.add((a.id, t.id))
        self.e.log("g1_pounce_bite_committed", hunter=a.id, target=t.id,
                   profile="B06-AT-06", ap_spent=24,
                   translated_steps=run.steps, cost_mp=run.spent_mp)
        self.e.defense(t.id, defense, attack_key=f"G1-pounce:{a.id}:{t.id}")
        trig = Trigger(trigger_key or f"g1:pounce:bite:{len(self.e.ledger)}", a.id, t.id)
        initial_target = t.occupied
        def intercept(e, tr, r):
            entry = self.motion.pop(r.label, None)
            if entry is None:
                raise UnresolvedDecision("Pounce attack-action Interception needs G3 resolver")
            for delta in (interceptor_routes or {}).get(r.label, ()):
                self._movement(entry.actor_id, delta=tuple(delta), reserved=entry,
                               trigger_key=f"{tr.key}:intercept:{entry.steps}")
            e.log("g1_movement_interception_resolved", actor=entry.actor_id,
                  label=entry.label, committed_mp=entry.reserved_mp,
                  consumed_mp=entry.spent_mp, completed_steps=entry.steps)
            if not self.melee_contact(a.id, t.id, hunter_front=True):
                tr.legal = False
        def react(e, tr, c):
            e.log("g1_pounce_reaction_pending", actor=c.actor_id, trigger=tr.key,
                  outcome="G3/G5_action_unresolved")
            if on_response:
                on_response(e, tr, c)
        ok = self.e.response_window(
            trig, on_interception=intercept,
            spontaneous=tuple(responses), on_spontaneous=react if responses else None)
        valid = bool(ok and t.occupied == initial_target and
                     self.melee_contact(a.id, t.id, hunter_front=True)
                     and a.hp > 0 and not a.dead)
        self.e.log("g1_pounce_contact_result", hunter=a.id, target=t.id,
                   legal_after_responses=valid,
                   bite="one_paid_Bite_pending_G5" if valid else "cancelled",
                   balance=("conditional_after_Bite_resolution_G5"
                            if valid else "not_applicable"))
        # No roll, damage, poison, condition or forced Prone before G4/G5.
        a.mp_remaining = 0
        self.pounce = None
        self.e.check()
        return valid

    def pounce_abort(self):
        run = self.pounce
        if run is None:
            raise ValueError("No active Pounce")
        a = self.e.actors[run.hunter_id]
        # Below cutoff Charge converts to fixed-heading Rapid Advance; no
        # extra AP. G1 deliberately does not auto-extend or execute a route.
        self.e.log("g1_pounce_aborted", hunter=a.id, translated_steps=run.steps,
                   cost_mp=run.spent_mp, ap_committed=run.committed,
                   reason="explicit_policy_abort")
        if run.committed:
            a.mp_remaining = 0
        else:
            a.mp_remaining = max(0, 18-run.spent_mp)
        self.pounce = None
