"""High Priest Life L1–3: source-bound G0/G3/G4 prepared and invocation v0.

Only Basic Heal Primary and Guided/Vital Shelter Primary are executed. The
other authored Life prayers are preparation/access identities, not phantom
spells. A prepared action costs 20 AP; an unprepared L1–3 Invocation uses a
single native Full Action and a separately paid 1 Spent VP surcharge.
"""
from hashlib import sha256
from math import ceil

from scripts.b05_high_priest_life_l1_l3_v0 import LIFE_T1, profile
from scripts.b06_encounter_state_v0 import ROOT, UnresolvedDecision
from scripts.b06_damage_v0 import DamageState
from scripts.b06_ranged_v0 import RangedCombat

SOURCE="scripts/b05_high_priest_life_l1_l3_v0.py"
EXECUTABLE=frozenset(("Basic Heal","Guided Regeneration","Vital Shelter"))


class HighLifeLiturgy:
    def __init__(self,encounter,caster,*,preparation="standard"):
        if encounter.g3 is None or encounter.g4 is None:
            raise ValueError("High Life requires actual G0, G3 and G4")
        if encounter.round or encounter.current is not None:
            raise ValueError("Choose original prayer preparation before Round Begin")
        if getattr(encounter.g3,"high_life",None) is not None:
            raise ValueError("High Life preparation adapter already installed")
        self.e=encounter
        self.g3=encounter.g3
        self.g4=encounter.g4
        self.caster=caster
        p=profile(encounter.actors[caster].level,preparation=preparation)
        a=encounter.actors[caster]
        digest=sha256((ROOT/SOURCE).read_bytes()).hexdigest()
        if (a.source.source_id!="H" or a.source.path!=SOURCE
                or a.source.digest!=digest or a.focus!="High"
                or dict(a.source.abilities)!=p["abilities"]
                or a.vp_max!=p["vp_max"] or a.projection_ap!=20
                or a.physical_ap!=30 or a.regen!=p["normal_regen_throughput"]
                or a.source.status!="STRUCTURAL_B05_ONLY"):
            raise UnresolvedDecision("Only exact sourced High Life H character allowed")
        self.prepared=set(p["prepared_prayers"])
        self.open_slot=p["open_prayer_slots"]==1
        self.open_filled=None
        self.capacity=p["prepared_capacity"]
        self.g3.high_life=self
        self.e.log("b05_high_prayers_prepared",caster=caster,
                   preparation=preparation,prepared=sorted(self.prepared),
                   open_slot=int(self.open_slot),capacity=self.capacity,
                   source_sha256=digest)

    def _priest(self,caster):
        if caster!=self.caster or caster not in self.e.actors:
            raise UnresolvedDecision("No matching prepared High Life caster")
        a=self.e.actors[caster]
        p=profile(a.level)
        if (a.source.source_id!="H" or a.source.path!=SOURCE
                or a.source.digest!=sha256((ROOT/SOURCE).read_bytes()).hexdigest()
                or dict(a.source.abilities)!=p["abilities"]
                or a.focus!="High" or a.vp_max!=p["vp_max"]
                or a.projection_ap!=20 or a.physical_ap!=30):
            raise UnresolvedDecision("High Priest source changed")
        if a.dead or a.hp<=0:
            raise ValueError("Incapacitated Priest cannot cast")
        if self.e.current!=caster or self.e.pending_regeneration is not None:
            raise ValueError("Only a ready own turn permits normal casting")
        return a

    def _target(self,caster,recipient):
        if recipient not in self.e.actors:
            raise ValueError("Unknown Life recipient")
        a,b=self.e.actors[caster],self.e.actors[recipient]
        if b.dead:
            raise ValueError("Life techniques require living recipients")
        if recipient==caster:
            return
        if self.e.g1 is None or len(a.occupied)!=1 or len(b.occupied)!=1:
            raise UnresolvedDecision("Non-self Life magic requires real one-cell G1 geometry")
        src,dst=a.occupied[0],b.occupied[0]
        if len(src)!=2 or len(dst)!=2:
            raise UnresolvedDecision("Only 2D G1 geometry verified")
        dx,dy=sorted((abs(src[0]-dst[0]),abs(src[1]-dst[1])),reverse=True)
        if dx+0.5*dy>3:
            raise ValueError("Recipient outside three-square magic range")
        cells,corners=RangedCombat._ray(src,dst)
        walls=self.e.g1.walls
        if any(cell in walls for cell in cells[1:-1]) or any(
                x in walls or y in walls for x,y in corners):
            raise ValueError("Recipient air path obstructed")

    def _access(self,kind,access):
        if kind not in EXECUTABLE:
            if kind not in LIFE_T1:
                raise UnresolvedDecision("Technique not in the chosen Life Pillar")
            raise UnresolvedDecision("Authored Life technique lacks native v0 executor")
        if access not in ("prepared","invocation","open_prayer"):
            raise ValueError("Explicit authorized technique access mode required")
        if access=="prepared":
            if kind not in self.prepared:
                raise UnresolvedDecision("Technique not currently Prepared")
        elif access=="invocation":
            if kind in self.prepared:
                raise UnresolvedDecision("Open Invocation requires UNPREPARED technique")
        else:
            if (not self.open_slot or kind in self.prepared
                    or kind==self.open_filled):
                raise UnresolvedDecision("One unspecified L3 Open Prayer slot required")
        return access=="invocation"

    def cast(self,caster,kind,recipient,*,access="prepared",
             mode="maintained",tier=1,die=None,hand_available=False,
             unopposed=True,on_committed=None,delivery_check=None,
             blocked_restoration=(),restoration_check=None):
        """Execute one exact primary; no fabricated spell or contest outcome."""
        a=self._priest(caster)
        invoked=self._access(kind,access)
        if type(tier) is not int or tier<1 or tier>(2 if a.level>=3 else 1):
            raise ValueError("Used Tier exceeds the actual level ceiling")
        if kind!="Basic Heal" and tier!=1:
            raise ValueError("Guided/Shelter have authored T1 output only")
        if unopposed is not True:
            raise UnresolvedDecision(
                "Contested Life Intrusion requires independently attested contest")
        if kind=="Basic Heal":
            if mode!="instant" or type(die) is not int or not 1<=die<=8:
                raise ValueError("Basic Heal needs instant mode and one native d8")
            if self.e.g4 is None:
                raise UnresolvedDecision("G4 required for full Basic Heal")
            if recipient not in self.e.actors:
                raise ValueError("Unknown Basic Heal recipient")
            if unopposed is not True:
                raise UnresolvedDecision("Contested Intrusion not yet attested by this adapter")
            if hand_available is not True:
                raise ValueError("Basic Heal needs a free functioning hand")
            if on_committed is not None and (delivery_check is None
                                              or restoration_check is None):
                raise UnresolvedDecision("Post-commit Basic Heal requires live checks")
            if delivery_check is not None and not callable(delivery_check):
                raise ValueError("Delivery check must be callable")
            if restoration_check is not None and not callable(restoration_check):
                raise ValueError("Restoration check must be callable")
            declared=DamageState.live_heal_blocks(
                self.e,caster,recipient,blocked_restoration,restoration_check)
            spent,committed=2*tier,0
        else:
            if mode not in ("maintained","fixed") or die is not None:
                raise ValueError("Choose exact Guided/Shelter mode, not Basic Heal dice")
            spent=(2 if mode=="fixed" else int(kind=="Vital Shelter"))
            committed=(2 if mode=="maintained" else 0)
            if self.g3.active(caster,kind) or any(
                x.kind==kind and x.recipient==recipient
                for x in self.g3.effects.values()):
                raise ValueError("Identical maintained/fixed effect already exists")
            declared=frozenset()
        if on_committed is not None and not callable(on_committed):
            raise ValueError("Committed response must be callable")
        self._target(caster,recipient)
        if kind=="Basic Heal":
            issue=self.g4._heal_delivery_issue(
                caster,recipient,hand_available=hand_available,
                in_range=True,unobstructed=True,delivery_check=delivery_check)
            if issue is not None:
                raise ValueError("Basic Heal delivery invalid: "+issue)
        surcharge=int(invoked)
        price=spent+committed+surcharge
        self.g3._funds(a,spent+surcharge,committed)
        action="full" if invoked else "projection"
        ap_required=a.ap_total if invoked else a.projection_ap
        if a.ap_remaining<ap_required or (invoked and a.ap_remaining!=a.ap_total):
            raise ValueError("High Priest has insufficient untouched action AP")
        # Open Prayer's first legally declared use fills the unique slot.
        # A later interrupted application cannot retarget it for free.
        if access=="open_prayer":
            self.prepared.add(kind)
            self.open_slot=False
            self.open_filled=kind
            self.e.log("b05_open_prayer_slot_filled",caster=caster,kind=kind,
                       prepared=sorted(self.prepared),capacity=self.capacity)
        self.e.spend_ap(caster,action,label="b05:high:"+access+":"+kind)
        if on_committed is not None:
            on_committed(self.e)
        try:
            self._target(caster,recipient)
            if kind=="Basic Heal":
                if not hand_available:
                    raise ValueError("Basic Heal lost functioning hand")
                issue=self.g4._heal_delivery_issue(
                    caster,recipient,hand_available=hand_available,
                    in_range=True,unobstructed=True,delivery_check=delivery_check)
                if issue is not None:
                    raise ValueError("Basic Heal lost live delivery: "+issue)
                blocks=DamageState.live_heal_blocks(
                    self.e,caster,recipient,blocked_restoration,restoration_check)
            else:
                if self.g3.active(caster,kind) or any(
                    x.kind==kind and x.recipient==recipient
                    for x in self.g3.effects.values()):
                    raise ValueError("Identical effect established during responses")
                blocks=declared
            if a.hp<=0 or a.vp_available<price:
                raise ValueError("Caster incapacitated or funds no longer available")
        except (ValueError,UnresolvedDecision) as error:
            self.e.log("b05_high_cast_interrupted",caster=caster,kind=kind,
                       access=access,reason=str(error),vp_spent=0)
            self.e.check()
            return None
        self.g3._pay(caster,spent+surcharge,committed,
                     label="b05:high:"+access+":"+kind)
        if kind=="Basic Heal":
            r=self.g4.resolve_heal(
                recipient,contribution="Primary",
                vigor_amount=4+ceil(die*tier/3)+self.g3.heal_vc(a),
                blocked_components=blocks,
                source="b05:high:"+access+":paid_primary")
            r.update({"spent_vp":spent+surcharge,"surcharge":surcharge,
                      "committed_vp":0,"action_ap":ap_required})
            self.e.log("b05_high_life_applied",caster=caster,kind=kind,
                       recipient=recipient,access=access,spent=spent,
                       surcharge=surcharge,committed=0,action_ap=ap_required,
                       hp_restored=r["hp_restored"],vigor_restored=r["vigor_restored"])
            return r
        host=self.g3._new_effect(
            caster,kind,recipient,committed,
            budget=(8+max(0,dict(a.source.abilities)["Veil Control"])
                    if kind=="Vital Shelter" else None),
            expiry_round=(self.e.round+10 if mode=="fixed" else None))
        self.e.log("b05_high_life_applied",caster=caster,kind=kind,
                   recipient=recipient,access=access,mode=mode,
                   spent=spent,surcharge=surcharge,
                   committed=committed,effect=host.ident,
                   budget=host.budget,action_ap=ap_required)
        self.e.check()
        return host
