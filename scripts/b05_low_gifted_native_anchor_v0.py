"""B05 restricted Low Gifted L1–3 native Anchor/Emotion binding v0.

Only two approved provisional pilot expressions: Rooted Guard +1 and
Unbound Step -1 MP surcharge. No new off-turn action, spell, G0 Step,
generalized Gifted source ability or independent Focus certification.
"""
from copy import deepcopy
from scripts.b05_low_gifted_anchor_design_v0 import LowGiftedAnchorDesign
from scripts.b05_low_gifted_l1_l3_v0 import profile
from scripts.b06_encounter_state_v0 import Actor,Source,_fingerprint,UnresolvedDecision

SOURCE_PATH="scripts/b05_low_gifted_l1_l3_v0.py"
SOURCE_ROLE="GL"


def low_gifted_party_actor(level,actor_id,team,*,occupied):
    p=profile(level)
    a=p["abilities"]
    gear=tuple(sorted((name,"worn" if name=="Leather armor"
                       else "wielded" if name=="Sword" else "carried")
                      for name in p["equipment_sp"]))
    source=Source(SOURCE_PATH,SOURCE_ROLE,_fingerprint(SOURCE_PATH),
                  "STRUCTURAL_B05_ONLY",tuple(sorted(a.items())),
                  tuple(sorted(p["weapon_training"].items())),
                  gear,(),f"L{level}-low-gifted-pilot")
    actor=Actor(actor_id,team,source,level,"Low",p["initiative"],
                a["Awareness"],a["Agility"],
                p["hp_max"],p["vigor_max"],p["vp_max"],
                p["hp_max"],p["vigor_max"],p["vp_max"],0,0,
                p["normal_regen_throughput"],p["turn_ap"],
                p["physical_action_ap"],p["projection_action_ap"],
                "Sword",p["sword_guard_defense"],p["guard_capacity"],
                occupied=tuple(tuple(c) for c in occupied))
    actor.validate()
    return actor


def actual_sword_ready(e,actor_id):
    """Real current G1/G2 equipment + exact native structural source."""
    if (e.g1 is None or e.g2 is None or actor_id not in e.actors):
        return False
    a=e.actors[actor_id]
    if (a.source.source_id!=SOURCE_ROLE
            or a.source.path!=SOURCE_PATH
            or a.source.digest!=_fingerprint(SOURCE_PATH)
            or a.source.status!="STRUCTURAL_B05_ONLY"
            or len(a.occupied)!=1 or a.guard_instrument!="Sword"
            or not a.ready_guard or "Sword" not in e.g2.wielded.get(actor_id,set())
            or dict(a.source.equipment).get("Sword")!="wielded"):
        return False
    return True


class LowGiftedNativeAnchor:
    """Source-bound live pilot Anchor. Caller arms; G0/G1 pays/consumes."""

    def __init__(self,encounter,actor_id,*,anchor,dominant=None):
        if (getattr(encounter,"low_gifted_anchor",None) is not None
                or encounter.round!=0 or encounter.current is not None
                or encounter.g1 is None or encounter.g2 is None
                or actor_id not in encounter.actors
                or not actual_sword_ready(encounter,actor_id)):
            raise UnresolvedDecision("Attach exact ready Low Gifted before first G0 round")
        a=encounter.actors[actor_id]
        self.e,self.actor_id=encounter,actor_id
        self.model=LowGiftedAnchorDesign(a.level,veil_affinity=
            dict(a.source.abilities)["Veil Affinity"])
        self.model.begin_window(dominant=dominant)
        self.model.establish_anchor(anchor)
        # Isolated preview transitions never debit G0 AP or authenticate G1/G5.
        # This private snapshot changes only on genuine source-native events.
        self._native_model=deepcopy(self.model)
        self.own_steps=0
        self.defense_choice=None
        self.step_choice=None
        encounter.low_gifted_anchor=self
        encounter.log("b05_low_gifted_anchor_established",actor=actor_id,
                      level=a.level,anchor=anchor,active=self.model.active,
                      dominant=dominant,window=self.model.window,
                      source_digest=a.source.digest,
                      pilot_provisional=True,independent_focus_certified=False)

    def _source(self):
        a=self.e.actors[self.actor_id]
        if (a.source.source_id!=SOURCE_ROLE or a.source.path!=SOURCE_PATH
                or a.source.digest!=_fingerprint(SOURCE_PATH)
                or a.source.status!="STRUCTURAL_B05_ONLY"
                or len(a.occupied)!=1):
            raise UnresolvedDecision("Low Gifted source identity changed")
        return a

    def _preview_authenticated(self):
        """Reject preview-only Break, Reassert, disruption and Pulse edits."""
        return vars(self.model)==vars(self._native_model)

    def on_own_step_completed(self):
        """One new Emotion Window per genuine completed own G0 Step."""
        self._source()
        e=self.e
        steps=[ev for ev in e.ledger if ev["kind"]=="regeneration_step"
               and ev["detail"]["actor"]==self.actor_id]
        if (e.current!=self.actor_id or
                e.pending_regeneration!=self.actor_id or
                len(steps)!=self.own_steps+1
                or steps[-1]["round"]!=e.round):
            raise UnresolvedDecision("No new real Low Gifted G0 Step to establish")
        # Combat-start window 1 is separate from the first own-turn
        # Emotion Establishment Step. Refresh on EVERY genuine own Step,
        # including the first, without replaying a suspended Step.
        self.own_steps+=1
        # Advance ONLY genuine native state; preview calls cannot promote
        # unpaid emotional transitions at the next authentic G0 Step.
        self._native_model.begin_window()
        if self.own_steps==1:
            # Combat-start is not an earlier own turn. Opening the first
            # own-turn window never grants L3 Settled free-AP Deepen.
            self._native_model.persisted_from_previous=False
        self.model=deepcopy(self._native_model)
        self.e.log("b05_low_gifted_emotion_window",actor=self.actor_id,
                   window=self.model.window,anchor=self.model.anchor,
                   active=self.model.active,source_digest=self._source().source.digest)
        self.defense_choice=None
        self.step_choice=None

    def _ready(self,emotion):
        # The preview model is intentionally public and mutable. Native
        # authority is the actual count of G0 Steps and source ledger
        # effects, NEVER a caller-forced model window or cleared Pulse.
        native_steps=sum(1 for event in self.e.ledger
                         if event["kind"]=="regeneration_step"
                         and event["detail"]["actor"]==self.actor_id)
        if (self.own_steps!=native_steps
                or self.model.window!=native_steps+1
                or not self._preview_authenticated()
                or not self._native_model._ready(emotion)):
            return False
        for event in self.e.ledger:
            detail=event["detail"]
            if (event["kind"]=="defense_assigned"
                    and detail.get("actor")==self.actor_id
                    and detail.get("anchor_bonus")==1
                    and detail.get("anchor_window")==self.model.window):
                return False
            if (event["kind"]=="b05_low_gifted_unbound_step_applied"
                    and detail.get("actor")==self.actor_id
                    and detail.get("window")==self.model.window):
                return False
        return True

    def choose_defense(self,attack_key,kind):
        """Player precommits one incoming source attack's Guard/Dodge rider."""
        self._source()
        if kind not in ("guard","dodge") or not isinstance(attack_key,str) or not attack_key:
            raise ValueError("Exact pre-roll Guard/Dodge and attack key required")
        if self.e.round<1 or self.e.current in (None,self.actor_id):
            raise UnresolvedDecision("Select a real enemy-turn incoming defense")
        if not self._ready("Fear") or kind=="dodge" and self.model.level<2:
            raise ValueError("Fear Anchor not eligible for this defense")
        if self.defense_choice is not None:
            raise ValueError("One pending selected defense at a time")
        self.defense_choice=(self.e.round,self.e.current,attack_key,kind)
        return self.defense_choice

    def defense_bonus(self,choice,attack_key):
        if (self.defense_choice != (self.e.round,self.e.current,attack_key,choice)
                or not self._ready("Fear")):
            return 0
        self._source()
        return 1 if choice=="guard" or (choice=="dodge" and self.model.level>=2) else 0

    def commit_defense(self,choice,attack_key,defense_index):
        if (self.defense_choice !=
                (self.e.round,self.e.current,attack_key,choice)
                or not self._preview_authenticated()
                or not self._native_model._ready("Fear")):
            raise AssertionError("Source defense cannot commit unselected Anchor")
        proof=self.e.ledger[defense_index]
        if (proof["kind"]!="defense_assigned"
                or proof["detail"]["actor"]!=self.actor_id
                or proof["detail"]["attack_key"]!=attack_key
                or proof["detail"]["defense"]!=choice
                or proof["detail"]["anchor_bonus"]!=1):
            raise AssertionError("Only real paid G0 defense grants Anchor bonus")
        got=self.model.guarded_defense(kind=choice,paid=True,self_target=True,
                                      source_legal=True,physical=True)
        if not got.applicable or got.bonus!=1:
            raise AssertionError("Model and source G0 defense diverged")
        self._native_model=deepcopy(self.model)
        self.defense_choice=None

    def choose_step(self,delta,*,cautious=False):
        self._source()
        if (self.e.current!=self.actor_id
                or self.e.pending_regeneration is not None
                or type(cautious) is not bool or type(delta) not in (tuple,list)
                or len(delta)!=2 or any(type(v) is not int for v in delta)
                or tuple(delta) not in
                ((1,0),(-1,0),(0,1),(0,-1),
                 (1,1),(1,-1),(-1,1),(-1,-1))):
            raise ValueError("Actual own-turn one-square movement choice required")
        if not self._ready("Disgust"):
            raise ValueError("Disgust Anchor not eligible")
        if cautious and self.model.level<2:
            raise ValueError("Cautious widening only from Level 2")
        if self.step_choice is not None:
            raise ValueError("One pending selected step at a time")
        self.step_choice=(self.e.round,self.actor_id,tuple(delta),cautious)
        return self.step_choice

    def preview_discount(self,actor_id,*,delta,cautious,crawl,reserved,
                         destination,full_cost):
        """Exact G1 preview and current source; pure, no model Pulse debit."""
        if (actor_id!=self.actor_id or
                self.step_choice!=(self.e.round,actor_id,tuple(delta or ()),cautious)
                or not self._ready("Disgust")):
            return 0
        self._source()
        if (reserved is not None or crawl or len(destination)!=1
                or type(full_cost) is not int):
            return 0
        # G1 previews 2 MP cardinal, 3 MP diagonal; cautious doubles
        # base costs. Only one currently selected actual surcharge qualifies.
        dx,dy=delta
        base=3 if dx and dy else 2
        if full_cost<=base:
            return 0
        if not cautious and self.e.g1.terrain.get(destination[0],"normal")=="normal":
            return 0
        return 1

    def finish_uncredited_step(self,actor_id,*,delta,cautious,movement_index):
        """A paid step without eligible surcharge cannot bank its old intent."""
        if self.step_choice==(self.e.round,actor_id,tuple(delta),cautious):
            event=self.e.ledger[movement_index]
            if (event["kind"]!="g1_movement_step"
                    or event["detail"]["actor"]!=actor_id
                    or "anchor_mp_saved" in event["detail"]):
                raise AssertionError("Only genuine unreduced G1 step can retire intent")
            self.step_choice=None

    def commit_step(self,actor_id,*,delta,cautious,source_cost,paid_cost,
                    movement_index):
        if (self.step_choice!=(self.e.round,actor_id,tuple(delta),cautious)
                or source_cost-paid_cost!=1 or not self._preview_authenticated()
                or not self._native_model._ready("Disgust")):
            raise AssertionError("Only exact selected paid G1 step qualifies")
        event=self.e.ledger[movement_index]
        if (event["kind"]!="g1_movement_step"
                or event["detail"]["actor"]!=actor_id
                or event["detail"]["cost"]!=paid_cost
                or event["detail"]["source_cost"]!=source_cost):
            raise AssertionError("Real G1 movement receipt required")
        dx,dy=delta
        base=3 if dx and dy else 2
        result=self.model.movement_step(
            kind="cautious" if cautious else "normal_difficult",
            paid=True,source_legal=True,base_mp=base,
            surcharge_mp=source_cost-base)
        if not result.applicable or result.mp_reduction!=1 or result.remaining_mp_cost!=paid_cost:
            raise AssertionError("Native paid MP and Anchor preview diverged")
        self._native_model=deepcopy(self.model)
        self.step_choice=None
        self.e.log("b05_low_gifted_unbound_step_applied",
                   actor=actor_id,window=self.model.window,
                   source_digest=self._source().source.digest,
                   g1_movement_index=movement_index,source_mp=source_cost,
                   spent_mp=paid_cost,mp_saved=1,base_mp=base,
                   step_kind="cautious" if cautious else "normal_difficult")
