"""B06 G2: bounded source-backed direct projectile firing lane and bow executor.

Geometry: a finite G1 tile-center direct line, an explicit directional cover
surface, and explicit exposure for every actor centered on that line.
An ambiguous corner/body silhouette must be authored, not silently inferred.
This is NOT damage, attack-crit confirmation, VP casting, complete combat or AI.
"""
from dataclasses import dataclass, field
from fractions import Fraction

from scripts.b06_encounter_state_v0 import Response, Trigger, UnresolvedDecision

TIERS = frozenset((0, 2, 4, 6, 8))
BOW_BANDS = ((6, -2), (12, 0), (30, 2), (60, 5), (120, 8))


@dataclass(frozen=True)
class CoverSurface:
    cell: tuple
    difficulty: int
    # Direction of ray travel into the cover cell; orientation is mandatory.
    facing: tuple


@dataclass(frozen=True)
class ShotChoice:
    defense: str = "take_hit"
    primary_face: int = 10
    # Exposure is (actor_id, L), with L source-authored from the actual
    # silhouette and firing opening; never inferred from melee engagement.
    exposures: tuple = ()
    # Conditional declared personal defenses for exposed creatures.
    collateral: tuple = ()
    secondary_face: int | None = None
    aim_source: str | None = None
    trigger_key: str | None = None
    opportunities: tuple = ()
    interceptor_routes: dict = field(default_factory=dict)
    on_opportunity: object = None


@dataclass
class AimRecord:
    target: str
    profile: str
    source: str
    position: tuple
    own_turn_number: int


@dataclass(frozen=True)
class Lane:
    origin: tuple
    destination: tuple
    cells: tuple
    distance: int
    range_difficulty: int
    cover: int
    screens: tuple
    effective_obstruction: int
    blocked: bool = False


class RangedCombat:
    """Attach once to a G0 encounter with an already-installed G1 grid.

    Only source-backed R ('Bow' wielded) firing and physical F lane preview
    are currently executable. No general attack/hit damage executor exists.
    """

    def __init__(self, encounter, *, cover=(), scene_id="G2-authored-lane"):
        if encounter.g1 is None or getattr(encounter, "g2", None) is not None:
            raise ValueError("G2 requires one attached native G1 grid")
        self.e, self.g = encounter, encounter.g1
        self.scene_id = scene_id
        self.cover = {}
        for surface in cover:
            if not isinstance(surface, CoverSurface):
                raise ValueError("Explicit CoverSurface required")
            if (not self.g.inside(surface.cell)
                    or surface.cell in self.g.walls
                    or surface.cell in self.cover
                    or surface.difficulty not in TIERS - {0}
                    or surface.facing not in ((1, 0), (-1, 0), (0, 1),
                                              (0, -1), (1, 1), (1, -1),
                                              (-1, 1), (-1, -1))):
                raise ValueError("Invalid distinct directional partial cover source")
            self.cover[surface.cell] = surface
        self.aims = {}
        self.own_turn_number = {a: 0 for a in encounter.actors}
        self.wielded = {}
        for a in encounter.actors.values():
            items = {name: state for name, state in a.source.equipment}
            self.wielded[a.id] = {n for n, st in items.items()
                                  if st is True or st == "wielded"}
        encounter.g2 = self
        encounter.log("g2_lane_installed", scene=scene_id,
                      cover=[{"cell":s.cell, "difficulty":s.difficulty,
                              "facing":s.facing} for s in self.cover.values()])

    def on_turn_start(self, actor_id):
        self.own_turn_number[actor_id] += 1
        current = self.aims.get(actor_id)
        if current and self.own_turn_number[actor_id] >= current.own_turn_number + 2:
            self.aims.pop(actor_id)
            self.e.log("g2_aim_expired", actor=actor_id, reason="second_subsequent_turn")

    def on_position_change(self, actor_id):
        if actor_id in self.aims:
            self.aims.pop(actor_id)
            self.e.log("g2_aim_broken", actor=actor_id, reason="firing_position_changed")

    def ready_weapon(self, actor_id, weapon):
        a = self.e.actors[actor_id]
        available = dict(a.source.equipment)
        if weapon not in available or weapon in ("Leather armor", "20 arrows"):
            raise ValueError("Item is not available to ready as a weapon")
        if weapon not in ("Bow", "Dagger"):
            raise UnresolvedDecision("Weapon ready-state adapter limited to R Bow/Dagger")
        if a.source.source_id != "R":
            raise UnresolvedDecision("G2 weapon swap only uses audited R build")
        if weapon in self.wielded[actor_id]:
            raise ValueError("Weapon is already wielded")
        self.e.spend_ap(actor_id, "general", label="g2:ready:"+weapon)
        self.wielded[actor_id].discard("Bow")
        self.wielded[actor_id].discard("Dagger")
        self.wielded[actor_id].add(weapon)
        self.on_position_change(actor_id)  # cannot retain an aim with former gear
        self.e.log("g2_weapon_readied", actor=actor_id, weapon=weapon,
                   ap_remaining=a.ap_remaining)
        self.e.check()

    @staticmethod
    def _ray(a, b):
        """Exact tile-center ray; corner crossings do not fabricate a side lane."""
        x, y = a
        dx, dy = b[0]-x, b[1]-y
        if not (dx or dy):
            raise ValueError("Direct ranged lane must have nonzero distance")
        sx = (dx > 0) - (dx < 0)
        sy = (dy > 0) - (dy < 0)
        tx = Fraction(1, 2*abs(dx)) if dx else None
        ty = Fraction(1, 2*abs(dy)) if dy else None
        delta_x = Fraction(1, abs(dx)) if dx else None
        delta_y = Fraction(1, abs(dy)) if dy else None
        route, corner_sides = [(x, y)], []
        while (x, y) != b:
            if tx is None or (ty is not None and ty < tx):
                y += sy
                ty += delta_y
            elif ty is None or tx < ty:
                x += sx
                tx += delta_x
            else:
                # Ray passes an exact grid corner: two side tiles are not
                # directly traversed. Adjacent fully-solid wall corners
                # require external GM opening adjudication.
                corner_sides.append(((x+sx, y), (x, y+sy)))
                x += sx
                y += sy
                tx += delta_x
                ty += delta_y
            route.append((x, y))
        return tuple(route), tuple(corner_sides)

    def lane(self, shooter_id, target_id, *, exposures=(), origin=None,
             target_cell=None, range_kind="bow"):
        if shooter_id not in self.e.actors or target_id not in self.e.actors:
            raise ValueError("Unknown G2 shooter or target")
        shooter, target = self.e.actors[shooter_id], self.e.actors[target_id]
        if shooter.dead or shooter.hp <= 0 or target.dead:
            raise ValueError("Incapacitated shooter or dead target")
        if origin is None:
            if len(shooter.occupied) != 1:
                raise UnresolvedDecision("Explicit projectile origin for multicell shooter required")
            origin = shooter.occupied[0]
        if origin not in shooter.occupied:
            raise ValueError("Source origin must belong to shooter footprint")
        if target_cell is None:
            if len(target.occupied) != 1:
                raise UnresolvedDecision("Explicit target anatomy cell required for multicell target")
            target_cell = target.occupied[0]
        if target_cell not in target.occupied:
            raise ValueError("Target cell must belong to intended target")
        cells, corners = self._ray(origin, target_cell)
        # A physically solid corner at an exact tile-boundary intersection
        # needs a specific GM firing opening; neither auto-block nor phase.
        if any(u in self.g.walls or v in self.g.walls for u, v in corners):
            raise UnresolvedDecision("Direct projectile grazes an unadjudicated wall corner")
        if any(c in self.g.walls for c in cells[1:-1]):
            raise ValueError("No physically usable direct firing path through solid wall")
        if target_cell in self.g.walls:
            raise ValueError("Target cell blocked by solid wall")
        # All exposures must correspond to an actual intervening creature
        # intersecting this centerline, and each such actor requires an
        # authored tier. The G1 body may occupy 2 cells but is ONE screen.
        overlapping = {a.id for a in self.e.actors.values()
                       if a.id not in (shooter_id, target_id)
                       and any(p in cells[1:-1] for p in a.occupied)}
        source_exposures = dict(exposures)
        if (len(source_exposures) != len(tuple(exposures))
                or set(source_exposures) != overlapping
                or any(v not in TIERS - {0} for v in source_exposures.values())):
            raise UnresolvedDecision("Specify each physically interposed Living Screen and its authored exposure")
        # Directional partial cover is authored from this origin. Where two
        # cover objects overlap, a single effective opening must be supplied;
        # do not silently max or sum distinct physical barriers.
        surfaces = [self.cover[c] for c in cells[1:-1] if c in self.cover]
        if len(surfaces) > 1:
            raise UnresolvedDecision("Several physical cover pieces need one authored effective opening")
        heading = ((target_cell[0] > origin[0])-(target_cell[0] < origin[0]),
                   (target_cell[1] > origin[1])-(target_cell[1] < origin[1]))
        if surfaces and surfaces[0].facing != heading:
            raise UnresolvedDecision("Directional cover opening not authorized from this origin")
        c = surfaces[0].difficulty if surfaces else 0
        # In this 2-D centerline subset, a creature whose entire footprint
        # appears behind the intended point does not count as a screen.
        positions = {cell:i for i, cell in enumerate(cells)}
        screens = tuple(sorted(((k, v, min(positions[q] for q in self.e.actors[k].occupied
                                          if q in positions))
                                for k, v in source_exposures.items()),
                               key=lambda x:x[2]))
        squares = max(abs(target_cell[0]-origin[0]),abs(target_cell[1]-origin[1]))
        if range_kind == "bow":
            band = next((m for limit,m in BOW_BANDS if squares <= limit), None)
            if band is None:
                raise ValueError("Beyond 120-square bow range")
        elif range_kind == "flame":
            if squares < 1 or squares > 3:
                raise ValueError("Thrown Flame range is exactly 1–3 squares")
            band = 0  # Conjure Flame explicit +0, not Bow Close -2.
        else:
            raise UnresolvedDecision("Only bow and F physical flame previews are G2")
        return Lane(origin,target_cell,cells,squares,band,c,screens,
                    max((c, *(v for _,v,_ in screens)), default=0))

    def preview_thrown_flame(self, shooter_id, target_id, *, exposures=(),
                             origin=None, target_cell=None):
        """Physical lane only; no G3 spell access, AP, VP, roll or Fire hit."""
        a = self.e.actors[shooter_id]
        if a.source.source_id != "F":
            raise ValueError("Only authored F High Scholar may preview Flame")
        lane = self.lane(shooter_id,target_id,exposures=exposures,origin=origin,
                         target_cell=target_cell,range_kind="flame")
        self.e.log("g2_flame_lane_preview", shooter=shooter_id,target=target_id,
                   squares=lane.distance, range_difficulty=0,
                   obstruction=lane.effective_obstruction,
                   outcome="physical_only_G3_cast_not_committed")
        return lane

    def _bow_ready(self, shooter_id):
        a = self.e.actors[shooter_id]
        if a.source.source_id != "R" or "Bow" not in self.wielded[shooter_id]:
            raise ValueError("Source-authored wielded Bow required; carried dagger not a bow")
        if a.ammunition < 1:
            raise ValueError("No physical arrow to fire")
        return a

    def aim(self, shooter_id, target_id, source, *, profile="bow"):
        a=self._bow_ready(shooter_id)
        lane=self.lane(shooter_id,target_id,range_kind="bow")
        if source not in ("range", "cover") and not source.startswith("screen:"):
            raise ValueError("Aim names one exact shot-difficulty source")
        if source.startswith("screen:"):
            raise UnresolvedDecision("Living-screen Aim requires a specified authored exposed lane")
        if not a.ap_remaining >= a.physical_ap:
            raise ValueError("Insufficient AP to Aim")
        self.e.spend_ap(shooter_id,"physical",label="g2:aim:"+source)
        self.aims[shooter_id]=AimRecord(target_id,profile,source,a.occupied,
                                       self.own_turn_number[shooter_id])
        self.e.log("g2_aim_prepared",shooter=shooter_id,target=target_id,
                   profile=profile,source=source)
        return self.aims[shooter_id]

    def _aim_reduce(self, shooter_id,target_id,source,range_difficulty,cover,screens):
        aim=self.aims.get(shooter_id)
        mitigation=0
        if aim and aim.target==target_id and aim.profile=="bow" and aim.position==self.e.actors[shooter_id].occupied:
            # The chosen objective cannot be silently changed at release.
            if source is not None and source != aim.source:
                raise ValueError("Cannot reassign retained Aim to a different source")
            if aim.source == "range":
                mitigation=min(4,max(0,range_difficulty))
                range_difficulty -= mitigation
            elif aim.source == "cover":
                mitigation=min(4,cover)
                cover -= mitigation
            else:
                selected=aim.source.removeprefix("screen:")
                if selected not in screens:
                    mitigation=0
                else:
                    mitigation=min(4,screens[selected])
                    screens[selected]-=mitigation
        elif source is not None:
            raise ValueError("No matching active Aim")
        return range_difficulty,cover,screens,mitigation

    @staticmethod
    def _defense_value(actor,choice,range_diff,obstruction,*,commit=False):
        if choice not in ("take_hit","dodge","guard"):
            raise ValueError("Invalid projectile defense")
        if actor.hp <= 0 or actor.dead:
            if choice != "take_hit":
                raise ValueError("Incapacitated target cannot actively defend")
        if choice == "guard":
            instr=(actor.guard_instrument or "").lower()
            if ("shield" not in instr and "buckler" not in instr
                    or not actor.ready_guard or actor.guard_remaining<1
                    or actor.guard_value is None):
                raise ValueError("Only ready projectile-capable shield Guard allowed")
            value=actor.guard_value+obstruction
            base=actor.guard_value
            if commit:
                actor.guard_remaining-=1
        elif choice=="dodge":
            if any(str(x).lower()=="prone" for x in actor.conditions):
                raise UnresolvedDecision("Prone Dodge requires explicit physical capability")
            evasion=actor.ap_total//actor.physical_ap - 1
            value=10+min(actor.agility,4)+actor.awareness+evasion+range_diff+obstruction-actor.dodge_pressure
            base=value-obstruction
            if commit:
                actor.dodge_pressure+=2
        else:
            value=10+range_diff+obstruction
            base=value-obstruction
        return base,value

    @staticmethod
    def _faces(b, d, bonus):
        return tuple(n for n in range(2,20) if n+bonus<=d)

    @staticmethod
    def _allocate(b, d, bonus, cover, screens, shooter_team, actors):
        available=[n for n in range(2,20) if n+bonus<=d]
        faces={}
        for face in reversed(available[-cover:] if cover else []):
            faces[face]=("cover",None)
        remain=[n for n in available if n not in faces]
        allies=sorted((item for item in screens if actors[item[0]].team==shooter_team),
                      key=lambda x:x[2])
        enemies=sorted((item for item in screens if actors[item[0]].team!=shooter_team),
                       key=lambda x:x[2])
        for actor_id,tier,_ in allies:
            for face in remain[:tier]:
                faces[face]=("creature",actor_id)
            remain=[n for n in remain if n not in faces]
        for actor_id,tier,_ in enemies:
            for face in reversed(remain[-tier:] if tier else []):
                faces[face]=("creature",actor_id)
            remain=[n for n in remain if n not in faces]
        return faces

    def _intercept(self,tr,record,paths):
        # Exactly the same G1 saved-MP resource/collision executor as the
        # native movement step, but the projectile's original geometry is
        # validated after the precommitted movement.
        entry=self.g.motion.pop(record.label,None)
        if entry is None:
            raise UnresolvedDecision("Non-MP shot Interception requires G3/G4 resolver")
        for delta in paths.get(record.label,()):
            try:
                self.g._movement(entry.actor_id,delta=tuple(delta),reserved=entry,
                                 trigger_key=f"{tr.key}:intercept:{entry.steps}")
            except (ValueError,UnresolvedDecision) as error:
                self.e.log("g2_interception_route_rejected",actor=entry.actor_id,
                           label=entry.label,reason=str(error),spent_mp=entry.spent_mp)
                break
        self.e.log("g2_interception_resolved",actor=entry.actor_id,
                   label=record.label,steps=entry.steps,
                   consumed_mp=entry.spent_mp,committed_mp=entry.reserved_mp)

    def _shot(self,shooter_id,target_id,shot,seq_no):
        e=self.e
        shooter=e.actors[shooter_id]
        # Defensive choices were validated with the batch before AP payment.
        key=shot.trigger_key or f"g2:bow:{shooter_id}:{target_id}:{seq_no}:{len(e.ledger)}"
        def dynamic_opportunities(state,tr):
            # Specific bow-while-threatened Opportunity, not a normal
            # Movement Opportunity. No hit is inferred from geometry.
            current=tuple(oid for oid in e.order if oid!=shooter_id
                          and e.actors[oid].team!=shooter.team and
                          any(self.g.threatens(oid,c) for c in shooter.occupied))
            declared=tuple(shot.opportunities)
            if any(not isinstance(c,Response) or c.kind!="opportunity" or
                   c.actor_id not in current for c in declared):
                # Stale post-Interception offers are dropped; invalid caller
                # types/duplicate choices were preflighted at batch start.
                return tuple(c for c in declared if isinstance(c,Response) and
                             c.kind=="opportunity" and c.actor_id in current)
            return declared
        def on_opp(state,tr,response):
            e.log("g2_threatened_bow_opportunity",attacker=response.actor_id,
                  shooter=shooter_id,trigger=tr.key)
            result=shot.on_opportunity(response)  # independent G5 outcome
            if type(result) is not bool:
                raise UnresolvedDecision("Opportunity hit/miss must be explicit")
            if result:
                tr.legal=False
                e.log("g2_bow_interrupted",shooter=shooter_id,source=response.actor_id,
                      reason="source_authored_opportunity_hit")
        def on_interception(state,tr,res):
            self._intercept(tr,res,shot.interceptor_routes)
            try:
                self.lane(shooter_id,target_id,exposures=shot.exposures)
            except (ValueError,UnresolvedDecision):
                tr.legal=False
        trig=Trigger(key,shooter_id,target_id)
        try:
            proceeds=e.response_window(trig,on_interception=on_interception,
                        spontaneous=dynamic_opportunities,on_spontaneous=on_opp)
        except Exception as err:
            e.log("g2_bow_unresolved",shooter=shooter_id,target=target_id,
                  reason=f"{type(err).__name__}: {err}",ap_paid=True,launched=False)
            raise
        if not proceeds:
            e.log("g2_bow_no_launch",shooter=shooter_id,target=target_id,
                  trigger=key,reason="interrupted_or_obstructed",ammunition_spent=0)
            return {"outcome":"interrupted_before_launch"}
        try:
            lane=self.lane(shooter_id,target_id,exposures=shot.exposures)
        except (ValueError,UnresolvedDecision) as err:
            e.log("g2_bow_no_launch",shooter=shooter_id,target=target_id,
                  trigger=key,reason=str(err),ammunition_spent=0)
            return {"outcome":"illegal_after_commit"}
        if shooter.ammunition<1:
            raise UnresolvedDecision("Committed bow sequence lacks remaining physical arrows")
        if shot.aim_source is not None and (shooter_id not in self.aims or
                                            self.aims[shooter_id].source!=shot.aim_source):
            raise ValueError("Shot's retained Aim was lost")
        screen_tiers={sid:l for sid,l,_ in lane.screens}
        used_aim=bool(self.aims.get(shooter_id) and
                      self.aims[shooter_id].target==target_id)
        range_mod,cover,screens,mitigation=self._aim_reduce(
            shooter_id,target_id,shot.aim_source,lane.range_difficulty,
            lane.cover,screen_tiers)
        if used_aim:
            self.aims.pop(shooter_id)
            e.log("g2_aim_consumed",shooter=shooter_id,target=target_id,
                  mitigation=mitigation)
        # Assign declared personal defense before rolling, after Interception.
        target=e.actors[target_id]
        b,d=self._defense_value(target,shot.defense,range_mod,
                                 max((cover,*screens.values()),default=0),
                                 commit=True)
        e.log("g2_projectile_defense_assigned",actor=target_id,choice=shot.defense,
              base=b,final=d,guard_remaining=target.guard_remaining,
              dodge_pressure=target.dodge_pressure)
        shooter.ammunition-=1  # only now has the arrow physically launched
        e.log("g2_bow_launched",shooter=shooter_id,target=target_id,
              ammo_remaining=shooter.ammunition,attack_bonus=4,
              aim_mitigation=mitigation,range_difficulty=range_mod,
              cover=cover,screens=screens,effective_obstruction=d-b)
        base=b
        bonus=4 # exact B05 R bow_attack_bonus at all L1-L3
        face=shot.primary_face
        total=face+bonus
        faces=(self._allocate(b,d,bonus,cover,lane.screens,target.team if False else shooter.team,e.actors)
               if lane.screens else {})
        # Aim at a screen must narrow that specific source's collateral band.
        if lane.screens:
            modified=tuple((sid,screens[sid],pos) for sid,_,pos in lane.screens
                           if screens[sid]>0)
            faces=self._allocate(b,d,bonus,cover,modified,shooter.team,e.actors)
        e.log("g2_miss_faces_preallocated",shooter=shooter_id,target=target_id,
              faces={str(k):v for k,v in sorted(faces.items())},
              primary_face=face,base_defense=b,final_defense=d)
        if face==1:
            outcome="automatic_miss"
            struck=None
        elif face==20:
            outcome="critical_confirmation_pending_G5"
            struck=target_id
        elif total>d:
            outcome="intended_hit_pending_G5"
            struck=target_id
        else:
            if lane.screens:
                category, incidental=faces.get(face,("miss",None))
                if category=="cover":
                    outcome="cover_impact"
                    struck=None
                elif category=="creature":
                    candidate=e.actors[incidental]
                    declaration=dict(shot.collateral)[incidental]
                    squares=max(abs(candidate.occupied[0][0]-lane.origin[0]),
                                abs(candidate.occupied[0][1]-lane.origin[1]))
                    secondary_band=next((m for limit,m in BOW_BANDS
                                         if squares<=limit),None)
                    cb,cd=self._defense_value(candidate,declaration,secondary_band,
                                               0,commit=True)
                    if shot.secondary_face is None:
                        raise UnresolvedDecision("Selected collateral face requires conditional d20")
                    sec=shot.secondary_face
                    if sec!=1 and sec+bonus>cd:
                        outcome="collateral_hit_pending_G5"
                        struck=incidental
                    elif declaration=="guard" and sec!=1:
                        outcome="collateral_guard_impact"
                        struck=None
                    else:
                        outcome="collateral_miss"
                        struck=None
                    e.log("g2_conditional_secondary",projectile="same_bow_arrow",
                          target=incidental,defense=declaration,defense_value=cd,
                          secondary_face=sec,secondary_total=sec+bonus,
                          outcome=outcome,extra_ap=0,extra_ammo=0)
                elif shot.defense=="guard" and total<=b:
                    outcome="intended_guard_impact"
                    struck=None
                else:
                    outcome="ordinary_miss"
                    struck=None
            elif cover and total>b and total<=d:
                outcome="cover_impact"
                struck=None
            elif shot.defense=="guard" and total<=b:
                outcome="intended_guard_impact"
                struck=None
            else:
                outcome="ordinary_miss"
                struck=None
        if outcome in ("ordinary_miss","automatic_miss","collateral_miss"):
            # G3 Manifestation may use this original primary total for area
            # scatter; G2 NEVER launches the F spell or invents an area.
            scatter_margin=max(0,base-total)
        else:
            scatter_margin=None
        result={"outcome":outcome,"target":struck,"primary_face":face,
                "attack_total":total,"base_defense":b,"final_defense":d,
                "scatter_margin":scatter_margin,"ammunition_spent":1}
        e.log("g2_bow_shot_resolved",shooter=shooter_id,intended=target_id,**result,
              note="attack_delivery_only_HP_wounds_critical_G5_deferred")
        e.check()
        return result

    def bow_sequence(self,shooter_id,target_id,shots):
        """Commit one on-turn Attack Sequence to one target before first roll.

        All shots and each defender's intended/collateral policy are fixed
        before the first roll. Each fired shot consumes one physical arrow.
        Interrupted shot costs AP, not arrow; later shots remain committed.
        """
        e=self.e
        a=self._bow_ready(shooter_id)
        if e.current!=shooter_id or e.pending_regeneration:
            raise ValueError("Bow shooting requires ready current turn")
        if (shooter_id,target_id) in e.seen_sequences:
            raise ValueError("No second Attack Sequence against same target this turn")
        shots=tuple(shots)
        if not shots or any(not isinstance(sh,ShotChoice) for sh in shots):
            raise ValueError("Nonempty explicitly committed ShotChoice sequence required")
        if len(shots)>a.ammunition or a.ap_remaining<len(shots)*a.physical_ap:
            raise ValueError("Not enough AP or physical arrows for declared sequence")
        if sum(s.aim_source is not None for s in shots)>1:
            raise ValueError("One retained Aim can apply to one attack only")
        for idx,sh in enumerate(shots):
            if type(sh.primary_face) is not int or not 1<=sh.primary_face<=20:
                raise ValueError("Exactly one lawful primary d20 face per shot")
            if sh.secondary_face is not None and (type(sh.secondary_face) is not int or
                                                   not 1<=sh.secondary_face<=20):
                raise ValueError("Conditional d20 face must be 1–20")
            lane=self.lane(shooter_id,target_id,exposures=sh.exposures)
            if sh.defense not in ("take_hit","guard","dodge"):
                raise ValueError("Invalid intended defense")
            if sh.defense=="guard":
                self._defense_value(e.actors[target_id],"guard",0,0)
            if sh.defense=="dodge" and e.actors[target_id].hp<=0:
                raise ValueError("Dying target cannot Dodge")
            if set(dict(sh.collateral))!=set(sid for sid,_,_ in lane.screens):
                raise UnresolvedDecision("Every eligible incidental creature needs predeclared personal defense")
            for incidental,choice in sh.collateral:
                if choice not in ("take_hit","dodge","guard"):
                    raise ValueError("Invalid conditional defense")
                self._defense_value(e.actors[incidental],choice,0,0)
            if sh.opportunities and sh.on_opportunity is None:
                raise UnresolvedDecision("Threatened bow Opportunity requires explicit attack outcome policy")
            if any(not isinstance(x,Response) or x.kind!="opportunity"
                   for x in sh.opportunities):
                raise ValueError("Only explicitly selected Opportunity responses")
            if len({x.actor_id for x in sh.opportunities})!=len(sh.opportunities):
                raise ValueError("Duplicate Opportunity source")
            if sh.aim_source is not None:
                record=self.aims.get(shooter_id)
                if not record or record.target!=target_id or record.profile!="bow" or record.source!=sh.aim_source:
                    raise ValueError("Shot has no matching retained Aim")
        # G0's own-action hook breaks G1 segment, as canon requires.
        e.seen_sequences.add((shooter_id,target_id))
        for i in range(len(shots)):
            e.spend_ap(shooter_id,"physical",label=f"g2:bow:{target_id}:{i}")
        e.log("g2_bow_sequence_committed",shooter=shooter_id,target=target_id,
              profiles=["Bow"]*len(shots),defenses=[s.defense for s in shots],
              ammunition_selected=len(shots),note="only launched arrows are expended")
        return tuple(self._shot(shooter_id,target_id,shot,i) for i,shot in enumerate(shots))
