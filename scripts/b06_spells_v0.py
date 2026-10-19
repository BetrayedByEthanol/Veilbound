"""B06 G3: source-specific legal spell activation and VP state, not a full combat engine.

F High Scholar L1-3, R Low Life Bow Priest and Firebound Sentry are adapted
from their exact B05/EN source fixtures. A/B are physical proxies, not silently
complete Priest spellbooks. Damage packets are delivered, never applied to G4
HP/Vigor/wounds. An unresolved magical or physical choice must be supplied.
"""
from dataclasses import dataclass
from math import ceil

from scripts.b05_high_scholar_fire_l1_l3_v0 import FORMULAS, profile as scholar
from scripts.b06_encounter_state_v0 import Response, UnresolvedDecision


@dataclass
class SpellEffect:
    ident: str
    caster: str
    kind: str
    recipient: str
    committed: int
    chosen: bool = False
    anchor: str | None = None
    parent: str | None = None
    budget: int | None = None
    resistance: int = 0
    expiry_round: int | None = None


class SpellState:
    """Explicit event/state adapter for authored G3 casts and maintained hosts."""

    def __init__(self, encounter):
        if getattr(encounter, "g3", None) is not None:
            raise ValueError("G3 already attached")
        self.e = encounter
        self.effects = {}
        self.next_effect = 0
        self.reactive_stone_claimed = set()
        # G0 deliberately stores the exact original Sentry active-effect ID.
        # Reconstruct that genuine source-backed reservation without moving VP.
        for a in encounter.actors.values():
            if a.source.source_id == "B06-EN-01":
                if "B06-FIRE-RESERVE-01" in a.maintained:
                    if (a.source.start_state != "prepared_start"
                            or (a.vp_available,a.vp_committed,a.vp_spent)!=(3,3,0)):
                        raise ValueError("Sentry prepared reserve/source VP mismatch")
                    self.effects[(a.id,"B06-FIRE-RESERVE-01")] = SpellEffect(
                        "B06-FIRE-RESERVE-01",a.id,"Sentry Sword Reserve",
                        a.id,3,chosen=True,anchor="Sword")
                elif a.source.start_state != "cold_start" or a.vp_committed:
                    raise ValueError("Sentry cold source VP mismatch")
        encounter.g3=self
        encounter.log("g3_spell_state_installed",loaded=[
            {"caster":v.caster,"effect":v.ident,"committed":v.committed}
            for v in self.effects.values()])
        encounter.check()

    def _actor(self,caster):
        if caster not in self.e.actors:
            raise ValueError("Unknown caster")
        a=self.e.actors[caster]
        if a.dead or a.hp<=0:
            raise ValueError("Dying/dead caster cannot cast")
        return a

    def _own(self,caster,ap_cost):
        a=self._actor(caster)
        if self.e.current!=caster or self.e.pending_regeneration is not None:
            raise ValueError("Only ready own-turn casting is supported")
        if a.projection_ap!=ap_cost or a.ap_remaining<ap_cost:
            raise ValueError("Insufficient source-specific Projection AP")
        # G1 active Pounce/spell timing restrictions remain in spend_ap.
        return a

    def _new_effect(self,caster,kind,recipient,committed,*,chosen=False,
                    anchor=None,parent=None,budget=None,resistance=0,
                    expiry_round=None,ident=None):
        if ident is None:
            self.next_effect+=1
            ident=f"G3-{self.next_effect:04d}"
        a=self.e.actors[caster]
        if (caster,ident) in self.effects:
            raise ValueError("Effect ID already exists")
        v=SpellEffect(ident,caster,kind,recipient,committed,chosen,anchor,parent,
                      budget,resistance,expiry_round)
        self.effects[(caster,ident)]=v
        a.maintained.append(ident)
        self.e.log("g3_effect_established",caster=caster,recipient=recipient,
                   effect=ident,kind=kind,committed=committed,
                   chosen=chosen,anchor=anchor,parent=parent,
                   budget=budget,resistance=resistance,expiry_round=expiry_round)
        return v

    def active(self,caster,kind):
        return [x for x in self.effects.values()
                if x.caster==caster and x.kind==kind]

    def _funds(self,a,spent,committed):
        if a.vp_available<spent+committed:
            raise ValueError("Insufficient combined Available VP")
        if spent<0 or committed<0:
            raise ValueError("Negative VP component")

    def _pay(self,caster,spent,committed,*,label):
        a=self.e.actors[caster]
        self._funds(a,spent,committed)
        if spent:
            self.e.spend_vp(caster,spent,mode="spent",label=label)
        if committed:
            self.e.spend_vp(caster,committed,mode="committed",label=label)

    def _commit(self,caster,*,on_committed=None,label):
        self.e.spend_ap(caster,"projection",label=label)
        if on_committed is not None:
            on_committed(self.e)

    def _sentry_wielded(self,a):
        # G0 enemy source equipment stores source-equipped Boolean; G2 has a
        # mutable ready-set. Source state cannot grant extra ready actions.
        if self.e.g2 is not None:
            return "Sword" in self.e.g2.wielded[a.id]
        return any(name=="Sword" and state is True
                   for name,state in a.source.equipment)

    def cast_sentry_reserve(self,caster,*,on_committed=None):
        a=self._own(caster,30)
        if a.source.source_id!="B06-EN-01" or a.source.start_state!="cold_start":
            raise ValueError("Only cold-start Sentry may establish its Chosen Reserve")
        if self.active(caster,"Sentry Sword Reserve"):
            raise ValueError("Already active")
        if not self._sentry_wielded(a):
            raise ValueError("Source sword must actually be wielded")
        self._funds(a,0,3)
        self._commit(caster,on_committed=on_committed,label="g3:sentry:chosen_reserved_sword")
        if a.hp<=0 or not self._sentry_wielded(a) or a.vp_available<3:
            self.e.log("g3_cast_interrupted",caster=caster,kind="Sentry Sword Reserve")
            return None
        self._pay(caster,0,3,label="g3:sentry:chosen_reserved_sword")
        return self._new_effect(caster,"Sentry Sword Reserve",caster,3,
                                chosen=True,anchor="Sword",
                                ident="B06-FIRE-RESERVE-01")

    def sentry_profile(self,caster):
        a=self._actor(caster)
        if a.source.source_id!="B06-EN-01":
            raise ValueError("Not a Firebound Sentry")
        active=bool(self.active(caster,"Sentry Sword Reserve"))
        return "B06-AT-02" if active and self._sentry_wielded(a) else "B06-AT-01"

    def _formula(self,a,secondary):
        if a.source.source_id!="F":
            raise ValueError("Only F High Scholar knows these exact formulae")
        if secondary not in ("Basic Heal","Vital Shelter"):
            raise UnresolvedDecision("No authorized High Scholar Self composite")
        p=scholar(a.level)
        form=next((f for f in FORMULAS if f["primary"]=="Stone Skin"
                   and f["secondary"]==secondary and f["profile"]=="Self"),None)
        if form is None or (a.level<3 and form not in p["prepared_composite_formulas"]):
            raise ValueError("Formula not prepared or authorized at this level")
        return p

    def cast_scholar_composite(self,caster,secondary,*,heal_tier=1,heal_die=None,
                               hand_available=False,on_committed=None):
        a=self._own(caster,20)
        p=self._formula(a,secondary)
        if self.active(caster,"Stone Skin"):
            raise ValueError("Only one Stone Skin instance per caster")
        reserve=(a.vp_max+2)//3
        if secondary=="Basic Heal":
            if hand_available is not True:
                raise ValueError("Basic Heal requires functioning available hand")
            if heal_tier not in (1,2) or heal_tier>p["max_used_tier"]:
                raise ValueError("Invalid component Used Tier")
            if type(heal_die) is not int or not 1<=heal_die<=6:
                raise UnresolvedDecision("Explicit legal d6 Heal Secondary roll required")
            if a.wounds or a.hp<=0:
                raise UnresolvedDecision("Dying/wound application belongs in G4")
            spent=2*heal_tier
            committed=reserve
        else:
            if heal_tier!=1 or heal_die is not None:
                raise ValueError("Vital Shelter Secondary has no Basic Heal tier/die")
            spent=1
            committed=reserve+2
            if any(v.kind.endswith("Shelter") and v.recipient==caster
                   for v in self.effects.values()):
                raise ValueError("Recipient already has a Shelter")
        self._funds(a,spent,committed)
        self._commit(caster,on_committed=on_committed,
                     label="g3:composite:Stone Skin+"+secondary)
        if a.hp<=0 or a.vp_available<spent+committed or (
                secondary=="Basic Heal" and hand_available is not True):
            self.e.log("g3_cast_interrupted",caster=caster,kind="Composite",secondary=secondary)
            return None
        self._pay(caster,spent,committed,label="g3:composite:"+secondary)
        host=self._new_effect(caster,"Stone Skin",caster,reserve,resistance=2)
        if secondary=="Basic Heal":
            restored_hp=min(1,a.hp_max-a.hp)
            restored_vigor=min(2+ceil(heal_die*heal_tier/6),a.vigor_max-a.vigor)
            a.hp+=restored_hp
            a.vigor+=restored_vigor
            self.e.log("g3_basic_heal_secondary_once",caster=caster,host=host.ident,
                       tier=heal_tier,hp=restored_hp,vigor=restored_vigor,
                       die=heal_die,regen_debit=0)
            self.e.check()
        else:
            self._new_effect(caster,"Vital Shelter",caster,2,parent=host.ident,budget=4)
        return host

    def cast_stone(self,caster,*,tier=1,on_committed=None):
        """One independently known F Stone Skin Primary, ordinary on-turn."""
        a=self._own(caster,20)
        if a.source.source_id!="F":
            raise UnresolvedDecision("Only F has verified standalone Stone Skin access")
        if type(tier) is not int or tier<1 or tier>scholar(a.level)["max_used_tier"]:
            raise ValueError("Stone Skin Used Tier over source ceiling")
        if self.active(caster,"Stone Skin"):
            raise ValueError("One Stone Skin instance per caster")
        reserve=(a.vp_max+2)//3
        self._funds(a,0,reserve)
        self._commit(caster,on_committed=on_committed,label="g3:standalone:stone_skin")
        if a.hp<=0 or a.vp_available<reserve or self.active(caster,"Stone Skin"):
            self.e.log("g3_cast_interrupted",caster=caster,kind="Stone Skin")
            return None
        self._pay(caster,0,reserve,label="g3:stone_skin")
        return self._new_effect(caster,"Stone Skin",caster,reserve,resistance=2)

    def prepare_reactive_stone(self,caster,trigger,*,perceptible):
        """Return a genuine G0 Response choice; do not consume it yet.

        The caller must submit it through Encounter.response_window before
        a roll/hazard, with the normal post-Interception eligibility ordering.
        """
        a=self._actor(caster)
        if a.source.source_id!="F":
            raise UnresolvedDecision("Only F has verified Stone Skin knowledge")
        if not trigger.legal or trigger.target_id!=caster or perceptible is not True:
            raise ValueError("No eligible perceived incoming target/hazard")
        if not a.reaction_available or self.e.round==0:
            raise ValueError("Stone Skin Reaction not available")
        if self.active(caster,"Stone Skin"):
            raise ValueError("Cannot stack Stone Skin")
        self._funds(a,0,(a.vp_max+2)//3)
        return Response(caster,"reaction","g3:reactive_stone")

    def resolve_reactive_stone(self,caster,trigger,response):
        """Only after G0 has *actually* committed this labeled Reaction."""
        a=self._actor(caster)
        if (response!=Response(caster,"reaction","g3:reactive_stone")
                or trigger.target_id!=caster or not trigger.legal
                or a.source.source_id!="F"):
            raise ValueError("Illegal Reactive Stone Skin source/trigger")
        token=(caster,trigger.key)
        proof=any(event["kind"]=="spontaneous_committed" and
                  event["detail"].get("trigger")==trigger.key and
                  event["detail"].get("actor")==caster and
                  event["detail"].get("response_kind")=="reaction" and
                  event["detail"].get("label")=="g3:reactive_stone"
                  for event in self.e.ledger)
        if not proof or token in self.reactive_stone_claimed or a.reaction_available:
            raise ValueError("No unused G0-committed matching Reaction")
        self.reactive_stone_claimed.add(token)
        if self.active(caster,"Stone Skin") or a.vp_available<(a.vp_max+2)//3:
            self.e.log("g3_cast_interrupted",caster=caster,kind="Reactive Stone Skin",
                       trigger=trigger.key)
            return None
        reserve=(a.vp_max+2)//3
        self._pay(caster,0,reserve,label="g3:reactive_stone:"+trigger.key)
        effect=self._new_effect(caster,"Stone Skin",caster,reserve,resistance=2)
        self.e.log("g3_stone_reacted",caster=caster,trigger=trigger.key,
                   reaction_spent=True,ap_spent=0,ap_debt=0)
        return effect

    def cast_self_basic_heal(self,caster,*,tier=1,die,hand_available=False,
                             on_committed=None):
        """Independent Primary; non-Dying self only, G4 owns wound allocation."""
        a=self._own(caster,20 if self.e.actors[caster].source.source_id=="F" else 30)
        if a.source.source_id not in ("F","R"):
            raise UnresolvedDecision("Only source-backed F/R Basic Heal access")
        if type(tier) is not int or tier<1 or tier>(1 if a.level<3 else 2):
            raise ValueError("Invalid Basic Heal Used Tier")
        if type(die) is not int or not 1<=die<=8:
            raise UnresolvedDecision("Explicit actual Heal Primary d8 required")
        if hand_available is not True:
            raise ValueError("Basic Heal needs genuinely available hand")
        if a.wounds or a.hp<=0:
            raise UnresolvedDecision("Wound or Dying recipient requires G4")
        cost=2*tier
        self._funds(a,cost,0)
        self._commit(caster,on_committed=on_committed,label="g3:self_basic_heal")
        if a.hp<=0 or a.vp_available<cost:
            self.e.log("g3_cast_interrupted",caster=caster,kind="Basic Heal")
            return None
        self._pay(caster,cost,0,label="g3:self_basic_heal")
        hp=min(2,a.hp_max-a.hp)
        vigor=min(4+ceil(die*tier/3),a.vigor_max-a.vigor)
        a.hp+=hp
        a.vigor+=vigor
        self.e.log("g3_basic_heal_primary_once",caster=caster,recipient=caster,
                   tier=tier,die=die,hp=hp,vigor=vigor,
                   regen_debit=0,spent_vp=cost)
        self.e.check()
        return {"hp_restored":hp,"vigor_restored":vigor,"spent_vp":cost}

    def cast_guided(self,caster,*,mode="maintained",chosen=False,
                    recipient=None,on_committed=None):
        a=self._own(caster,30)
        if a.source.source_id!="R":
            raise UnresolvedDecision("A/B physical proxies have no G3 Prepared Prayer sheet")
        if recipient not in (None,caster):
            raise UnresolvedDecision("G3 only covers source-authored R Self Guided Regeneration")
        if mode not in ("maintained","fixed"):
            raise ValueError("Choose Guided Regeneration fixed or maintained")
        if self.active(caster,"Guided Regeneration"):
            raise ValueError("Cannot stack/replace same Guided instance")
        # Fixed Spent-only blessings are not Rites; maintained positive
        # self-reservations are, whether chosen or ordinary.
        if any(v.caster==caster and v.recipient==caster and v.committed>0
               and v.kind in ("Guided Regeneration","Vital Shelter",
                              "Stone Skin","Sentry Sword Reserve")
               for v in self.effects.values()):
            raise ValueError("One active L1-3 Devotional Rite slot")
        if chosen and mode!="maintained":
            raise ValueError("Spent-only Fixed Guided is not a Chosen Rite")
        committed=1 if chosen else 2 if mode=="maintained" else 0
        spent=2 if mode=="fixed" else 0
        self._funds(a,spent,committed)
        self._commit(caster,on_committed=on_committed,label="g3:guided:"+mode)
        if a.hp<=0 or a.vp_available<spent+committed:
            self.e.log("g3_cast_interrupted",caster=caster,kind="Guided Regeneration")
            return None
        self._pay(caster,spent,committed,label="g3:guided:"+mode)
        return self._new_effect(caster,"Guided Regeneration",caster,committed,
                                chosen=chosen,
                                expiry_round=(self.e.round+10 if mode=="fixed" else None))

    def exaltation_eligibility(self,caster,property_id):
        """Check real authored L3 Low Life host eligibility, not an activation.

        EX-LR-01's Step-end arm/payout belongs to G4's dated HP-loss ledger.
        EX-LP-01 needs a finite Chosen Vital Shelter Primary host, which the
        R starting repertoire does NOT currently have.
        """
        a=self._actor(caster)
        if a.source.source_id!="R" or a.level<3:
            return False
        chosen=[v for v in self.effects.values()
                if v.caster==caster and v.recipient==caster and v.chosen
                and v.committed>0]
        if len(chosen)!=1:
            return False
        host=chosen[0]
        if property_id=="EX-LR-01":
            return host.kind=="Guided Regeneration" and host.expiry_round is None
        if property_id=="EX-LP-01":
            return host.kind=="Vital Shelter" and (host.budget or 0)>=2
        raise ValueError("Only the two authored L3 Life properties exist")

    def regen_throughput(self,actor_id):
        # No invented instant Regeneration Step; augment one actual G0 Step.
        return int(any(x.kind=="Guided Regeneration" and x.recipient==actor_id
                       for x in self.effects.values()))

    def resistance(self,actor_id,kind,other=()):
        allowed=kind in ("Physical","Crush","Cut","Piercing","Fire","Electrical")
        values=list(other)
        if allowed:
            values += [v.resistance for v in self.effects.values()
                       if v.kind=="Stone Skin" and v.recipient==actor_id]
        return max((0,*values))

    def prevent_vigor(self,actor_id,damage):
        if type(damage) is not int or damage<0:
            raise ValueError("Explicit nonnegative direct Vigor packet required")
        shelters=[v for v in self.effects.values()
                  if v.kind=="Vital Shelter" and v.recipient==actor_id]
        if len(shelters)>1:
            raise ValueError("Shelter stacking is not legal")
        a=self.e.actors[actor_id]
        shield=shelters[0] if shelters else None
        absorbed=(min(damage,shield.budget) if shield and a.vigor>0 else 0)
        if absorbed:
            shield.budget-=absorbed
        remaining=damage-absorbed
        self.e.log("g3_shelter_packet",recipient=actor_id,original=damage,
                   prevented=absorbed,residual=remaining,
                   budget=shield.budget if shield else None,
                   note="G4 owns application of residual Vigor damage")
        if shield and shield.budget==0:
            self._end(shield,reason="budget_exhausted")
        return remaining

    def _end(self,effect,*,reason):
        # Child reservation releases independently on exhaustion; a host end
        # always releases its remaining children first.
        for sub in list(self.effects.values()):
            if sub.caster==effect.caster and sub.parent==effect.ident:
                self._end(sub,reason="parent_ended:"+reason)
        key=(effect.caster,effect.ident)
        if self.effects.pop(key,None) is None:
            return
        a=self.e.actors[effect.caster]
        if effect.ident in a.maintained:
            a.maintained.remove(effect.ident)
        if effect.committed:
            self.e.release_vp(effect.caster,effect.committed,label="g3:"+reason)
        self.e.log("g3_effect_ended",caster=effect.caster,effect=effect.ident,
                   kind=effect.kind,returned=effect.committed,reason=reason)

    def release(self,caster,kind,*,own_turn=True):
        if own_turn and (self.e.current!=caster or
                         self.e.pending_regeneration is not None):
            raise ValueError("Voluntary release only at legal own-turn decision")
        found=self.active(caster,kind)
        if len(found)!=1:
            raise ValueError("Exactly one active named effect required")
        self._end(found[0],reason="voluntary_release")
        self.e.check()

    def sword_no_longer_wielded(self,caster):
        a=self.e.actors[caster]
        if a.source.source_id!="B06-EN-01":
            raise ValueError("Only Sentry reserve anchor is handled here")
        if self._sentry_wielded(a):
            raise ValueError("Sword remains wielded; no channel break")
        for v in list(self.active(caster,"Sentry Sword Reserve")):
            self._end(v,reason="sword_no_longer_wielded")
        self.e.check()

    def sync_consciousness(self,actor_id):
        a=self.e.actors[actor_id]
        if a.hp>0 and not a.dead:
            return
        # Stone Skin must end at once; Guided maintained only ends on death,
        # as explicitly authored. G4 must invoke this at the damage event.
        for v in list(self.effects.values()):
            if v.caster==actor_id and (
                    v.kind=="Stone Skin" or a.dead):
                self._end(v,reason="caster_unconscious_or_dead")
            elif v.recipient==actor_id and a.dead:
                self._end(v,reason="recipient_dead")
        self.e.check()

    def on_round_begin(self):
        for v in list(self.effects.values()):
            if v.expiry_round is not None and self.e.round>=v.expiry_round:
                self._end(v,reason="round_begin_duration_expiry")

    def cast_flame(self,caster,target,*,tier,face,vigor_die,
                   defense="take_hit",aware=False,hand_available=False,
                   on_committed=None,exposures=(),origin=None,target_cell=None):
        """Bounded direct clear/cover-only F Thrown Flame; no G4 HP mutations.

        Mixed living-screen destination/scatter and full opportunity/Reaction
        response need the G2 general-projectile adapter, deferred to G3+G5.
        Reject them rather than pretend G2's Bow arrow is a magic projectile.
        """
        a=self._own(caster,20)
        if a.source.source_id!="F":
            raise ValueError("Only authored F has this known T1 Conjure Flame")
        if tier not in (1,2) or tier>scholar(a.level)["max_used_tier"]:
            raise ValueError("Unsupported Used Tier for F")
        if hand_available is not True:
            raise ValueError("Free Thrown Flame requires available functioning hand")
        if type(face) is not int or not 1<=face<=20:
            raise ValueError("Explicit primary d20 face required")
        if type(vigor_die) is not int or not 1<=vigor_die<=8:
            raise ValueError("Explicit hit packet d8 face required")
        if defense not in ("take_hit","dodge","guard"):
            raise ValueError("Unknown ranged projectile defense")
        if defense!="take_hit" and aware is not True:
            raise ValueError("Projectile active defense requires actual target awareness")
        if self.e.g2 is None:
            raise UnresolvedDecision("G3 physical flame requires installed G2 firing lane")
        lane=self.e.g2.preview_thrown_flame(caster,target,exposures=exposures,
                                             origin=origin,target_cell=target_cell)
        if lane.screens:
            raise UnresolvedDecision("G3 mixed Flame collision/area needs full G2 projectile delivery")
        if any(self.e.g1.threatens(enemy.id,c) for enemy in self.e.actors.values()
               if enemy.team!=a.team for c in a.occupied):
            raise UnresolvedDecision("Threatened F casting needs genuine Opportunity response")
        victim=self.e.actors[target]
        if defense=="guard" or defense=="dodge":
            self.e.g2._defense_value(victim,defense,0,lane.cover)
        price=2*tier
        self._funds(a,price,0)
        self._commit(caster,on_committed=on_committed,label="g3:thrown_flame:T"+str(tier))
        try:
            refreshed=self.e.g2.preview_thrown_flame(
                caster,target,exposures=exposures,origin=origin,target_cell=target_cell)
        except (ValueError,UnresolvedDecision):
            self.e.log("g3_cast_interrupted",caster=caster,kind="Thrown Flame",
                       cause="post_commit_physical_lane")
            return {"outcome":"interrupted_before_launch","vp_spent":0}
        if (a.hp<=0 or a.vp_available<price or
                refreshed.screens):
            self.e.log("g3_cast_interrupted",caster=caster,kind="Thrown Flame",
                       cause="caster_or_resources")
            return {"outcome":"interrupted_before_launch","vp_spent":0}
        self._pay(caster,price,0,label="g3:thrown_flame:T"+str(tier))
        b,d=self.e.g2._defense_value(victim,defense,0,refreshed.cover,commit=True)
        attack=face+5
        if face==1:
            outcome="automatic_miss"
        elif face==20:
            outcome="critical_confirmation_pending_G5"
        elif attack>d:
            outcome="direct_hit_pending_G4"
        elif refreshed.cover and attack>b and attack<=d:
            outcome="cover_impact"
        elif defense=="guard" and attack<=b:
            outcome="guard_impact"
        else:
            outcome="ordinary_miss"
        packets=( {"fire_hp":2,
                   "vigor":2+ceil(vigor_die*tier/3)}
                  if outcome=="direct_hit_pending_G4" else None)
        result={"outcome":outcome,"attack_total":attack,
                "base_defense":b,"final_defense":d,"vp_spent":price,
                "packets_pending_g4":packets}
        self.e.log("g3_flame_launched",caster=caster,target=target,
                   tier=tier,primary_face=face,die=vigor_die,**result)
        self.e.check()
        return result
