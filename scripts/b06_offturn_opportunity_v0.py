"""B06 native off-turn ordinary Sword Opportunity delivery v0.

Policy author predeclares ALL eligible responder choices, roll faces, defense,
and wound dice before G0 commits capacity. A G1 departure supplies a live
spontaneous callback; only it can authorize an independently source-bound G5
hit, and G4.5 attests against G0's actual response index rather than Turn AP.
"""
from dataclasses import dataclass,replace
from scripts.b06_encounter_state_v0 import Response,UnresolvedDecision


@dataclass(frozen=True)
class OpportunityChoice:
    profile: str
    attack_face: int
    defense: str = "take_hit"
    damage_face: int | None = None
    confirmation_face: int | None = None
    critical_dice: tuple = ()
    vigor_die: int | None = None
    wound_location_roll: int | None = None


def _source(g5,attacker,profile):
    e=g5.e
    a=e.actors[attacker]
    if a.source.source_id not in ("B06-EN-02","B06-EN-01","S","T"):
        raise UnresolvedDecision("Off-turn ordinary Sword has no authored G5 source for this actor")
    if len(a.occupied)!=1 or a.hp<=0 or a.dead:
        raise UnresolvedDecision("Conscious one-square ordinary Sword responder required")
    if any(str(c).lower()=="prone" for c in a.conditions):
        raise UnresolvedDecision("Prone Opportunity requires separately attested weapon feasibility")
    if e.g2 is None or "Sword" not in e.g2.wielded.get(attacker,()):
        raise UnresolvedDecision("Live G2 wielded Sword required for off-turn Opportunity")
    if (a.source.source_id in ("B06-EN-01","B06-EN-02")
            and not any(name=="Sword" and equipped is True
                        for name,equipped in a.source.equipment)):
        raise UnresolvedDecision("Soldier/Sentry source has no originally equipped Sword")
    return g5._profile(attacker,profile)


def _validated(g5,mover,attacker,choice):
    e=g5.e
    if not isinstance(choice,OpportunityChoice):
        raise UnresolvedDecision("Author exact off-turn Opportunity choices before commitment")
    if (choice.defense not in ("take_hit","dodge","guard")
            or type(choice.attack_face) is not int
            or not 1<=choice.attack_face<=20):
        raise ValueError("G5 Opportunity requires genuine defense and d20 face")
    if (type(choice.critical_dice) not in (tuple,list)
            or any(type(x) is not int or not 1<=x<=4
                   for x in choice.critical_dice)):
        raise ValueError("Invalid committed Opportunity critical d4 faces")
    a=e.actors[mover]
    if a.hp<=0 or a.dead or len(a.occupied)!=1:
        raise UnresolvedDecision("Off-turn target must be a live one-square mover")
    if any(str(c).lower()=="prone" for c in a.conditions):
        raise UnresolvedDecision("Prone Opportunity defense needs separately authored feasibility")
    bonus=_source(g5,attacker,choice.profile)
    if choice.defense=="guard":
        if (not a.ready_guard or a.guard_remaining<1
                or not a.guard_instrument or a.guard_value is None
                or a.guard_instrument not in e.g2.wielded.get(mover,())
                or (a.source.source_id in ("S","T") and
                    not e.g1.genuine_scholar_sword_ready(mover))):
            raise ValueError("No real ready Guard for Opportunity defense")
        value=a.guard_value
    elif choice.defense=="dodge":
        toxin=e.g4.toxins.modifier(mover,"dodge")
        value=10+min(a.agility,4)+a.awareness-a.dodge_pressure+toxin
    else:
        value=None
    hit=(False if choice.attack_face==1 else
         True if choice.defense=="take_hit" or choice.attack_face==20
         else choice.attack_face+bonus>value)
    if choice.attack_face==20:
        if type(choice.confirmation_face) is not int or not 1<=choice.confirmation_face<=20:
            raise ValueError("Natural 20 requires canonical confirmation face")
    elif choice.confirmation_face is not None:
        raise ValueError("No confirmation roll without natural 20")
    critical="normal"
    if hit and choice.attack_face==20:
        if choice.defense=="take_hit":
            critical="devastating" if choice.confirmation_face==20 else "critical"
        elif choice.confirmation_face==20:
            critical="devastating"
        elif choice.confirmation_face!=1 and choice.confirmation_face+bonus>value:
            critical="critical"
        else:
            critical="strong"
    if len(choice.critical_dice)!={"normal":0,"strong":1,"critical":2,"devastating":2}[critical]:
        raise ValueError("Exact Opportunity confirmation critical dice required")
    if hit:
        if type(choice.damage_face) is not int:
            raise ValueError("G5 Opportunity damage die must be predeclared")
        e.g4.preflight_profile_hit(
            attacker,mover,choice.profile,die_face=choice.damage_face,
            critical=critical,critical_dice=tuple(choice.critical_dice),
            vigor_die=choice.vigor_die,wound_location_roll=choice.wound_location_roll)
    elif choice.damage_face is not None or choice.vigor_die is not None:
        raise ValueError("A miss cannot claim damage or extra dice")
    return bonus,value,hit,critical


def step(g5,mover,delta,*,decisions,cautious=False):
    """Move one real G1 square; source-authored Opportunity responses resolve
    during the *actual* live pre-step G0 window, before MP/position payment.

    decisions maps every newly eligible responder to an OpportunityChoice or
    explicit None (decline). Missing choices, spoofed responder IDs, unsupported
    sources and malformed dice reject before G0 spends any Response capacity.
    """
    e=g5.e
    if (e.g5 is not g5 or e.g1 is None or e.g4 is None
            or e.current!=mover or e.pending_regeneration is not None):
        raise UnresolvedDecision("Only installed G5 on current G0 mover can deliver Opportunities")
    if not isinstance(decisions,dict) or any(
            who not in e.actors or (decision is not None and
            not isinstance(decision,OpportunityChoice))
            for who,decision in decisions.items()):
        raise ValueError("Exact per-responder Opportunity decision map required")
    # The caller's mapping or mutable critical-dice list is never a
    # post-preflight authority. Freeze all of it before any G0 commitment.
    decisions={who:(replace(ch,critical_dice=tuple(ch.critical_dice))
                    if ch is not None and
                       isinstance(ch.critical_dice,(tuple,list))
                    else ch)
               for who,ch in decisions.items()}
    target=e.actors[mover]
    dest,_,_,_=e.g1.preview(mover,delta=tuple(delta),cautious=cautious)
    eligible=e.g1._threats(mover,dest,cautious)
    if set(decisions)!=set(eligible):
        raise UnresolvedDecision("Author exactly each eligible native Opportunity, including declines")
    for who in eligible:
        if decisions[who] is not None:
            _validated(g5,mover,who,decisions[who])
    # Dynamic G1 eligibility runs only AFTER source-authorized Interceptions.
    # This policy has no hidden or unsupported interception effects.
    def choices(live):
        if set(live)!=set(eligible):
            raise UnresolvedDecision("Opportunity eligibility changed before G0 commitment")
        for who in live:
            if decisions[who] is not None:
                _validated(g5,mover,who,decisions[who])
        return tuple(Response(who,"opportunity","g5:ordinary_sword_offturn")
                     for who in live if decisions[who] is not None)

    def on_response(state,trigger,response):
        # Invoked synchronously from G1's actual pre-step callback. G0 has
        # already paid Reaction/Opportunity capacity for ALL responders.
        who=response.actor_id
        if who not in decisions or decisions[who] is None:
            raise UnresolvedDecision("Unscheduled off-turn responder")
        g5.resolve_opportunity(trigger,response,decisions[who])

    return e.g1.step(mover,tuple(delta),cautious=cautious,
                     responses=choices,on_response=on_response)


def resolve(g5,trigger,response,choice):
    """Consume one real G0 response, native defense and G4 packet, once."""
    e=g5.e
    if (not e.is_live_spontaneous(trigger,response)
            or response.kind!="opportunity"
            or response.label!="g5:ordinary_sword_offturn"
            or trigger.actor_id!=trigger.target_id
            or e.current!=trigger.actor_id
            or e.pending_regeneration is not None):
        raise UnresolvedDecision("No exact live G0/G1 off-turn Opportunity callback")
    mover,who=trigger.actor_id,response.actor_id
    if who==mover or e.actors[who].team==e.actors[mover].team:
        raise UnresolvedDecision("Real enemy responder must threaten current mover")
    # The G1 callback emits a pending attack for exactly this trigger and
    # responder before granting access to this resolver.
    pending=[v for v in e.ledger if v["kind"]=="g1_movement_opportunity_pending"
             and v["detail"].get("trigger")==trigger.key
             and v["detail"].get("attacker")==who
             and v["detail"].get("mover")==mover]
    committed=[v for v in e.ledger if v["kind"]=="spontaneous_committed"
               and v["detail"].get("trigger")==trigger.key
               and v["detail"].get("actor")==who
               and v["detail"].get("response_kind")=="opportunity"
               and v["detail"].get("label")==response.label]
    if len(pending)!=1 or len(committed)!=1:
        raise UnresolvedDecision("Off-turn requires exact native G1 pending and G0 response")
    receipt=committed[0]
    if any(v["kind"] in ("g5_opportunity_resolved","g5_opportunity_cancelled")
           and v["detail"].get("response_index")==receipt["index"]
           for v in e.ledger):
        raise ValueError("One G0 response cannot deal Opportunity damage twice")
    # Earlier initiative-ordered responses can genuinely incapacitate the
    # same mover. Later G0-committed capacities stay paid, but no ghost attack.
    if e.actors[mover].dead or e.actors[mover].hp<=0:
        e.log("g5_opportunity_cancelled",attacker=who,mover=mover,
              response_index=receipt["index"],reason="target_incapacitated",
              committed_capacity_retained=True)
        return {"outcome":"cancelled","response_index":receipt["index"]}
    if (not any(e.g1.threatens(who,c) for c in e.actors[mover].occupied)
            or not e.g1.melee_contact(who,mover)):
        e.log("g5_opportunity_cancelled",attacker=who,mover=mover,
              response_index=receipt["index"],reason="live_contact_lost",
              committed_capacity_retained=True)
        return {"outcome":"cancelled","response_index":receipt["index"]}
    bonus,_,hit,critical=_validated(g5,mover,who,choice)
    value=e.defense(mover,choice.defense,
                    attack_key=f"g5:opportunity:{receipt['index']}")
    # A valid response cannot become an ordinary turn/AP action; source
    # approval, G0 capacity and the exact defense are independently logged.
    e.log("g5_opportunity_roll",response_index=receipt["index"],
          attacker=who,mover=mover,profile=choice.profile,
          defense=choice.defense,defense_value=value,
          attack_face=choice.attack_face,attack_bonus=bonus,
          attack_total=choice.attack_face+bonus,
          confirmation_face=choice.confirmation_face,
          critical=critical,hit=hit)
    result=None
    if hit:
        result=g5.bridge.verified_opportunity_hit(
            who,mover,choice.profile,
            trigger=trigger,response=response,
            response_index=receipt["index"],pending_index=pending[0]["index"],
            die_face=choice.damage_face,critical=critical,
            critical_dice=tuple(choice.critical_dice),
            vigor_die=choice.vigor_die,
            wound_location_roll=choice.wound_location_roll)
    e.log("g5_opportunity_resolved",attacker=who,mover=mover,
          response_index=receipt["index"],profile=choice.profile,
          outcome="hit" if hit else "miss",damage=result)
    e.check()
    return {"outcome":"hit" if hit else "miss",
            "response_index":receipt["index"],
            "damage":result,"defense":choice.defense}
