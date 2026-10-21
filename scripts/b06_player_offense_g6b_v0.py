"""B06 G6-B v0: audited player melee into Hunter and genuine G1 Opportunity hits.

A/B Low Life Priest sheets are L1–3 PHYSICAL PROXIES. This file adds only
their source-equipment Sword/Mace strikes; it does not certify archetype
repertoires, Bow projectile wounds, Protective Intervene, or full party packs.
Ordinary own-turn attacks run through G5; out-of-turn attacks run in the
actual G0 spontaneous Opportunity callback before G1's movement step.
"""
from copy import deepcopy

from scripts.b06_encounter_state_v0 import (
    Response, UnresolvedDecision,
)
from scripts.b06_hunter_g6a_v0 import HunterCombat
from scripts.b06_soldier_sentry_g5_v0 import _face
from scripts.b06_hunter_party_exchanges_v0 import BUILD


PARTY_MELEE = {
    "A": ("B06-PC-A-SWORD", "Sword", 3, 2, "light", "Cut"),
    "B": ("B06-PC-B-MACE", "Mace", 4, 3, "full", "Crush"),
}


def party_weapon_profile(actor, profile_id):
    """One source-derived physical proxy, no caller-authored combat numbers.

    Verify source binding, current wielded equipment, Training and the
    published A/B fixture attack/damage baselines before returning packets.
    The Sword's ordinary Cut mode is explicitly selected for this v0.
    """
    role=actor.source.source_id
    if role not in PARTY_MELEE:
        raise UnresolvedDecision("Only audited A/B proxy melee is authorized")
    ident,weapon,base,penetration,contribution,trauma=PARTY_MELEE[role]
    if (profile_id!=ident or actor.source.attack_profiles!=(ident,)
            or actor.source.path!="scripts/b06_hunter_party_exchanges_v0.py"
            or actor.source.status!="B05_UNBUFFED_PHYSICAL_PROXY"):
        raise UnresolvedDecision("Unrecognized or unsourced A/B weapon profile")
    equipment=dict(actor.source.equipment)
    if equipment.get(weapon)!="wielded":
        raise UnresolvedDecision("Source attack weapon is not wielded")
    abilities=dict(actor.source.abilities)
    training=dict(actor.source.training)
    strength,agility=abilities.get("Strength"),abilities.get("Agility")
    weapon_training=training.get(weapon)
    if any(type(x) is not int for x in (strength,agility,weapon_training)):
        raise UnresolvedDecision("Source lacks locked weapon ability/Training")
    attack_bonus=strength+agility+weapon_training
    physical=(strength if contribution=="full" else max(strength,0)//2)
    audited=BUILD[role]
    if (attack_bonus!=audited["attack"] or base+physical!=audited["weapon_base"]
            or penetration!=audited["penetration"]):
        raise UnresolvedDecision("A/B proxy diverges from verified physical baseline")
    return ({
        "id":ident,"range_class":"melee",
        "primary_hp_packet":{"fixed_base":base,"die":"d6",
                             "damage_type":trauma,
                             "armor_penetration":penetration,
                             "strength_contribution":contribution},
        "additional_packets":[],"toxin_delivery":None,
    },attack_bonus)


class PlayerHunterCombat(HunterCombat):
    """Attach G5+G6A once, then execute G6B bounded PC physical actions.

    Use declare()/resolve() for A/B own-turn Sword/Mace against the Hunter.
    step_with_opportunity() is the only G6B live out-of-turn damage path:
    the native G1 Opportunity first spends G0 Reaction/capacity and then
    delivers one real paid-response packet before the mover's step.
    """

    def _profile(self, attacker, profile_id):
        actor=self.e.actors[attacker]
        if actor.source.source_id in PARTY_MELEE:
            return party_weapon_profile(actor,profile_id)[1]
        return super()._profile(attacker,profile_id)

    def declare(self, attacker, target, *, profiles, defenses, **kwargs):
        actor=self.e.actors[attacker]
        if actor.source.source_id in PARTY_MELEE:
            if self.e.actors[target].source.source_id!="B06-EN-03":
                raise UnresolvedDecision("G6-B player weapon attacks only target Hunter")
            if any(profile != PARTY_MELEE[actor.source.source_id][0]
                   for profile in profiles):
                raise UnresolvedDecision("Player sequence requires its wielded source profile")
        return super().declare(attacker,target,profiles=profiles,
                               defenses=defenses,**kwargs)

    def step_with_opportunity(self,hunter_id,delta,attacker_id,*,
                              defense="take_hit",attack_face,
                              damage_face=None,confirmation_face=None,
                              critical_dice=(),wound_location_roll=None,
                              cautious=False,trigger_key=None):
        """One predeclared PC Opportunity on one REAL Hunter movement step.

        No synthetic attack AP, Reaction, contact or forced hit. Reject
        unsupported Interceptions and wrong initial geometry atomically.
        Defensive choice and d20s are known before G1 may commit response
        capacity; actual defense is assigned inside the native callback.
        """
        e=self.e
        if hunter_id not in e.actors or attacker_id not in e.actors:
            raise ValueError("Known Hunter mover and PC responder required")
        mover,attacker=e.actors[hunter_id],e.actors[attacker_id]
        if (mover.source.source_id!="B06-EN-03"
                or attacker.source.source_id not in PARTY_MELEE
                or mover.team==attacker.team):
            raise UnresolvedDecision("G6-B Opportunity requires opposing Hunter and A/B")
        if (e.current!=hunter_id or e.pending_regeneration is not None
                or mover.hp<=0 or mover.dead
                or attacker.hp<=0 or attacker.dead):
            raise ValueError("Ready living Hunter movement and PC responder required")
        if e.g1.pounce is not None or hunter_id in e.g1.rapid_heading:
            raise UnresolvedDecision("G6-B has no Pounce/Rapid Opportunity policy")
        if any(str(x).lower()=="prone" for x in mover.conditions):
            raise UnresolvedDecision("Prone Hunter Crawl Opportunity needs separate policy")
        if defense not in ("take_hit","dodge"):
            raise UnresolvedDecision("Hunter has no source Guard instrument")
        if (not attacker.reaction_available and not attacker.opportunity_active
                or attacker.opportunity_used>=attacker.ap_total//attacker.physical_ap):
            raise ValueError("PC lacks native Opportunity activation/capacity")
        delta=tuple(delta)
        destination,_,_,_=e.g1.preview(hunter_id,delta=delta,cautious=cautious)
        if attacker_id not in e.g1._threats(hunter_id,destination,cautious):
            raise UnresolvedDecision("No new genuine PC threat at Hunter departure")
        if not self._contact(attacker_id,hunter_id):
            raise UnresolvedDecision("PC cannot deliver current melee Opportunity")
        profile=PARTY_MELEE[attacker.source.source_id][0]
        bonus=self._profile(attacker_id,profile)
        face=_face(attack_face,20,"G6-B Opportunity attack")
        target_prone=any(str(x).lower()=="prone" for x in mover.conditions)
        attacker_prone=any(str(x).lower()=="prone" for x in attacker.conditions)
        if attacker_prone:
            raise UnresolvedDecision("Prone PC Opportunity needs verified attack feasibility")
        bonus+=2 if target_prone else 0
        if defense=="dodge":
            value=(10+min(mover.agility,4)+mover.awareness-mover.dodge_pressure
                   +e.g4.toxins.modifier(hunter_id,"dodge"))
        else:
            value=None
        total=face+bonus
        hit=face!=1 and (defense=="take_hit" or face==20 or total>value)
        if face==20:
            confirmation_face=_face(confirmation_face,20,"Opportunity confirmation")
        elif confirmation_face is not None:
            raise ValueError("No confirmation without natural 20")
        critical="normal"
        if hit and face==20:
            if confirmation_face==20:
                critical="devastating"
            elif (defense=="take_hit" or
                  (confirmation_face!=1 and confirmation_face+bonus>value)):
                critical="critical"
            else:
                critical="strong"
        expected={"normal":0,"strong":1,"critical":2,"devastating":2}[critical]
        if (type(critical_dice) not in (tuple,list)
                or len(critical_dice)!=expected
                or any(type(x) is not int or not 1<=x<=4 for x in critical_dice)):
            raise ValueError("Exact canonical Opportunity critical d4 dice required")
        if hit:
            _face(damage_face,6,"Opportunity weapon damage")
            e.g4.preflight_profile_hit(
                attacker_id,hunter_id,profile,die_face=damage_face,
                critical=critical,critical_dice=tuple(critical_dice),
                wound_location_roll=wound_location_roll)
        elif damage_face is not None:
            raise ValueError("Missed Opportunity cannot consume damage die")
        if not isinstance(cautious,bool):
            raise ValueError("Explicit Cautious choice must be boolean")
        key=(trigger_key if trigger_key is not None
             else f"g6b:move:{hunter_id}:{attacker_id}:{len(e.ledger)}")
        if type(key) is not str or not key:
            raise ValueError("Stable movement trigger key required")
        if any(r.trigger_key==key for r in e.reservations):
            raise UnresolvedDecision("Prepared Interception requires separate G6-B executor")
        response=Response(attacker_id,"opportunity",
                          f"g6b:weapon:{profile}:{key}")
        resolved=[]

        def on_response(encounter,trigger,selected):
            if (selected != response or
                    not encounter.is_live_spontaneous(trigger,selected)
                    or trigger.key!=key
                    or encounter.current!=hunter_id
                    or not self._contact(attacker_id,hunter_id)):
                raise UnresolvedDecision("No live native PC Opportunity authority")
            # The G0 callback is reached only AFTER the spontaneous
            # commitment debits Reaction (first use) and Opportunity count.
            committed=next((x for x in reversed(encounter.ledger)
                            if x["kind"]=="spontaneous_committed"
                            and x["detail"].get("actor")==attacker_id
                            and x["detail"].get("trigger")==key
                            and x["detail"].get("response_kind")=="opportunity"),None)
            if committed is None:
                raise UnresolvedDecision("Missing committed native G0 response")
            # Recheck the predeclared actual defense, not a substituted
            # caller-provided result or a retroactive better Dodge value.
            checked=encounter.defense(
                hunter_id,defense,
                attack_key=f"g6b:opportunity:{committed['index']}")
            if checked!=value:
                raise UnresolvedDecision("Hunter defense changed after Opportunity preflight")
            encounter.log("g6b_opportunity_roll",
                          response_index=committed["index"],attacker=attacker_id,
                          mover=hunter_id,profile=profile,
                          attack_face=face,bonus=bonus,attack_total=total,
                          defense=defense,defense_value=value,
                          confirmation_face=confirmation_face,
                          critical=critical,hit=hit)
            damage=None
            if hit:
                damage=encounter.g4.apply_profile_hit(
                    attacker_id,hunter_id,profile,die_face=damage_face,
                    confirmed_hit=True,critical=critical,
                    critical_dice=tuple(critical_dice),
                    wound_location_roll=wound_location_roll)
            encounter.log("g6b_opportunity_resolved",
                          response_index=committed["index"],
                          attacker=attacker_id,target=hunter_id,
                          profile=profile,outcome="hit" if hit else "miss",
                          damage=deepcopy(damage),critical=critical,
                          defense=defense,
                          ap_spent=0,source_attacker=attacker.source.digest)
            resolved.append({"outcome":"hit" if hit else "miss",
                             "critical":critical,"damage":deepcopy(damage),
                             "response_index":committed["index"]})
            if mover.hp<=0 or mover.dead:
                trigger.legal=False

        moved=e.g1.step(hunter_id,delta,cautious=cautious,
                        trigger_key=key,responses=(response,),
                        on_response=on_response)
        if len(resolved)!=1:
            raise UnresolvedDecision("PC Opportunity had no single native response resolution")
        e.check()
        return {"movement_completed":bool(moved),"opportunity":resolved[0],
                "hunter_position":mover.occupied}
