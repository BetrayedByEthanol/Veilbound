"""B06 G6-D v0: source-bound Bow-to-G4 and mixed-party terminal authority.

A deliberately bounded, clear-lane one-arrow adapter. G2 still owns every
real projectile launch, its committed physical AP, defense and ammunition.
Only an independently verified hit may reach G4 (including natural-20
confirmation) and an independently sourced wound location. No invented
G5 melee action, extra hit roll, or Bow VP packet is created.
"""
from copy import deepcopy

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_damage_v0 import DamagePacket
from scripts.b06_ranged_v0 import ShotChoice
from scripts.b05_bow_vanguard_l1_l3_v0 import profile as bow_sheet


class HunterCompletion:
    def __init__(self,combat):
        e=combat.e
        if e.g1 is None or e.g2 is None or e.g3 is None or e.g4 is None or e.g5 is not combat:
            raise UnresolvedDecision("G6-D requires same native G0/G1/G2/G3/G4/G5 combat")
        self.combat=combat
        self.e=e

    def bow_hit(self,shooter,target,*,primary_face,damage_face=None,
                confirmation_face=None,critical_dice=(),wound_location_roll=None,
                defense="take_hit",target_cell=None):
        """Pay one native G2 physical shot, then attest one physical G4 hit.

        This executor accepts a deliberately clear path with one source
        R Bow shooter, one sourced two-cell Hunter recipient and a static
        Take Hit ranged defense. It rejects cover/screen, active defenses,
        unknown interception, prone/critical ambiguity *before* AP is paid.
        This is not a general projectile/critical/collateral resolver.
        """
        e=self.e
        if shooter not in e.actors or target not in e.actors:
            raise ValueError("Existing shooter and target required")
        a,t=e.actors[shooter],e.actors[target]
        if (a.source.source_id!="R" or
                a.source.path!="scripts/b05_bow_vanguard_l1_l3_v0.py"
                or t.source.source_id!="B06-EN-03" or
                t.footprint!=("head","rear") or len(t.occupied)!=2
                or a.team==t.team):
            raise UnresolvedDecision("G6-D permits only verified R Bow versus Hunter")
        if (e.current!=shooter or e.pending_regeneration is not None
                or a.hp<=0 or a.dead or t.dead):
            raise ValueError("Only live current R turn against nondead Hunter")
        if any(str(x).lower()=="prone" for x in t.conditions):
            raise UnresolvedDecision("Prone projectile profile needs separate G2 policy")
        if defense!="take_hit":
            raise UnresolvedDecision("G6-D excludes active projectile defenses")
        if (target_cell is None or target_cell not in t.occupied):
            raise UnresolvedDecision("Explicit actual Hunter anatomical cell required")
        if any(e.g1.threatens(enemy.id,c) for enemy in e.actors.values()
               if enemy.team!=a.team for c in a.occupied):
            raise UnresolvedDecision("Threatened Bow requires native Opportunity resolver")
        sheet=bow_sheet(a.level)
        if (sheet["bow_attack_bonus"]!=4 or sheet["bow_damage"]!="2+d4 Piercing"
                or sheet["bow_penetration"]!=3 or
                dict(a.source.equipment).get("Bow")!="wielded"
                or "Bow" not in e.g2.wielded[shooter]):
            raise UnresolvedDecision("Current equipped Bow disagrees with sourced attack")
        if type(primary_face) is not int or not 1<=primary_face<=20:
            raise ValueError("Bow primary d20 face must be 1–20")
        if a.ap_remaining<a.physical_ap or a.ammunition<1:
            raise ValueError("Insufficient sourced arrow or Physical AP")
        if (shooter,target) in e.seen_sequences:
            raise ValueError("Second same-target ordinary Bow sequence not allowed")
        # G2 otherwise derives its response key inside _shot AFTER spending
        # physical AP. Explicitly bind the one-shot key now and refuse a
        # live Interception before any source cost or G2 mutation.
        shot_trigger=(f"g6d:bow:{e.seed}:{e.round}:"
                      f"{shooter}:{target}:one_shot")
        if any(r.trigger_key==shot_trigger for r in e.reservations):
            raise UnresolvedDecision(
                "G6-D Bow matching Interception requires an authenticated route executor")
        lane=e.g2.lane(shooter,target,target_cell=target_cell)
        if lane.screens or lane.cover or lane.blocked:
            raise UnresolvedDecision("G6-D Bow requires clear lane without Living Screens/Cover")
        # G2 Take Hit is a static *ranged* defense: NOT melee auto-hit.
        base,defense_value=e.g2._defense_value(t,"take_hit",lane.range_difficulty,0)
        total=primary_face+sheet["bow_attack_bonus"]
        hit=primary_face!=1 and (primary_face==20 or total>defense_value)
        if primary_face==20:
            if type(confirmation_face) is not int or not 1<=confirmation_face<=20:
                raise ValueError("Natural-20 Bow requires one confirmation d20")
            critical=("devastating" if confirmation_face==20 else "critical"
                      if confirmation_face+4>defense_value and confirmation_face!=1
                      else "strong")
        else:
            if confirmation_face is not None:
                raise ValueError("No Bow confirmation without natural 20")
            critical="normal"
        expected={"normal":0,"strong":1,"critical":2,"devastating":2}[critical]
        if (type(critical_dice) not in (tuple,list)
                or len(critical_dice)!=(expected if hit else 0)
                or any(type(v) is not int or not 1<=v<=4 for v in critical_dice)):
            raise ValueError("Source critical damage requires exact d4 faces")
        if hit:
            if type(damage_face) is not int or not 1<=damage_face<=4:
                raise ValueError("Verified Bow hit requires one damage d4")
            packet=DamagePacket("hp","Piercing",
                                2+damage_face+sum(critical_dice),3,"weapon")
            # Preflight the G4 wound crossing before G2 spends Physical AP
            # or an arrow. G4 will use precisely this packet and same
            # recipient state; no callback may mutate it in this bounded
            # no-Interception/no-Opportunity clear-lane wrapper.
            loss=e.g4._mitigate_hp(t,packet)
            after=max(-t.hp_max,t.hp-loss)
            wound_needed=(t.hp>0 and after<=0 or
                          critical=="devastating") and after>-t.hp_max
            if wound_needed and (
                    type(wound_location_roll) is not int or
                    not 1<=wound_location_roll<=20):
                raise UnresolvedDecision("G6-D Bow wound requires predeclared location d20")
        else:
            if damage_face is not None or critical_dice or wound_location_roll is not None:
                raise ValueError("Miss cannot mint damage or a wound roll")
            packet=None
        start=len(e.ledger)
        result=e.g2.bow_sequence(shooter,target,(
            ShotChoice(defense="take_hit",primary_face=primary_face,
                       target_cell=target_cell,trigger_key=shot_trigger),
        ))
        # All source events MUST come from this ONE real G2 sequence.
        added=e.ledger[start:]
        commitments=[v for v in added if v["kind"]=="action_committed"
                     and v["detail"].get("actor")==shooter]
        declared=[v for v in added if v["kind"]=="g2_bow_sequence_committed"]
        windows=[v for v in added if v["kind"]=="response_window_open"]
        intercepted=[v for v in added if v["kind"]=="interception_released"]
        launched=[v for v in added if v["kind"]=="g2_bow_launched"]
        resolved=[v for v in added if v["kind"]=="g2_bow_shot_resolved"]
        if (len(commitments)!=1 or len(declared)!=1
                or len(windows)!=1 or intercepted
                or windows[0]["detail"].get("trigger")!=shot_trigger
                or len(launched)!=1 or len(resolved)!=1 or len(result)!=1
                or commitments[0]["detail"].get("label")!=f"g2:bow:{target}:0"
                or declared[0]["detail"].get("shooter")!=shooter
                or declared[0]["detail"].get("target")!=target
                or launched[0]["detail"].get("shooter")!=shooter
                or resolved[0]["detail"].get("shooter")!=shooter
                or resolved[0]["detail"].get("intended")!=target
                or resolved[0]["detail"].get("primary_face")!=primary_face
                # G2's authoritative ledger adds delivery identity and a
                # descriptive note; its returned result contains just the
                # shot outcome, which must otherwise match *exactly*.
                or result[0]!={k:v for k,v in resolved[0]["detail"].items()
                               if k not in ("note","shooter","intended")}):
            raise UnresolvedDecision("Missing exact source G2 paid launched shot provenance")
        expected_outcome=("critical_confirmation_pending_G5" if primary_face==20
                          else "intended_hit_pending_G5" if hit else
                          result[0]["outcome"])
        if (result[0]["outcome"]!=expected_outcome
                or result[0]["target"]!=(target if hit else None)):
            raise UnresolvedDecision("G2 actual shot contradicts precommitted hit policy")
        damage=None
        if hit:
            key=f"g6d:bow:{e.seed}:{commitments[0]['index']}:{resolved[0]['index']}"
            damage=e.g4.apply_damage(
                target,(packet,),event_key=key,
                cause=f"g6d:source_bow:{shooter}:{resolved[0]['index']}",
                devastating=critical=="devastating",
                wound_location_roll=wound_location_roll,
                wound_trauma="Piercing")
        e.log("g6d_bow_adjudicated",shooter=shooter,target=target,
              shot_index=resolved[0]["index"],
              action_index=commitments[0]["index"],
              launch_index=launched[0]["index"],
              original_outcome=result[0]["outcome"],
              outcome="hit" if hit else "miss",
              attack_face=primary_face,attack_total=total,
              defense_value=defense_value,confirmation_face=confirmation_face,
              critical=critical,damage=deepcopy(damage),
              source_digest=a.source.digest,
              chosen_target_part=t.footprint[t.occupied.index(target_cell)])
        e.check()
        return {"outcome":"hit" if hit else "miss","critical":critical,
                "damage":deepcopy(damage),"action_index":commitments[0]["index"],
                "shot_index":resolved[0]["index"],"ammo_remaining":a.ammunition}

    def attest_hunter_defeat(self,hunter,*,party_ids):
        """Verify an actual, final G4 source death, not a 0-HP crossing.

        The token is unavailable while an ordinary attack remains paid and
        pending, and one source-verified lethal packet must exist in ledger.
        This is a *defeat* terminal, not a party-escape or CR declaration.
        """
        e=self.e
        if hunter not in e.actors:
            raise ValueError("Unknown encounter target")
        h=e.actors[hunter]
        if h.source.source_id!="B06-EN-03" or h.team!="enemy" or not h.dead:
            raise UnresolvedDecision("Terminal requires actually dead source Hunter")
        if h.hp!=-h.hp_max:
            raise UnresolvedDecision("Terminal Hunter must have reached lethal HP threshold")
        party=tuple(party_ids)
        if (len(party) not in (3,4) or len(set(party))!=len(party)
                or set(e.actors)!={hunter,*party}
                or any(e.actors[p].team!="party" for p in party)):
            raise UnresolvedDecision("Terminal requires exact sourced mixed-party roster")
        sources={e.actors[p].source.source_id for p in party}
        if sources!=({"A","B","R"} if len(party)==3 else {"A","B","R","F"}):
            raise UnresolvedDecision("G6-D requires independently sourced mixed roster")
        if self.combat.pending_attack_slots():
            raise UnresolvedDecision("No terminal while paid melee actions unresolved")
        if (e.current is not None or e.cursor!=len(e.order)
                or e.round<1):
            raise UnresolvedDecision("Complete current real G0 round before terminal attestation")
        damage_events=[ev for ev in e.ledger if ev["kind"]=="g4_damage_applied"
                       and ev["detail"].get("recipient")==hunter
                       and ev["detail"].get("dead") is True]
        if len(damage_events)!=1:
            raise UnresolvedDecision("Exactly one native lethal G4 event required")
        lethal=damage_events[0]
        cause=lethal["detail"].get("cause","")
        valid_bow=bool(cause.startswith("g6d:source_bow:") and any(
            v["kind"]=="g6d_bow_adjudicated" and
            v["detail"].get("target")==hunter and
            v["detail"].get("damage",{}).get("dead") is True
            for v in e.ledger))
        valid_melee=bool(cause.startswith("source-profile:") and any(
            v["kind"]=="g5_melee_resolved" and
            v["detail"].get("target")==hunter and
            v["detail"].get("damage",{}).get("dead") is True
            for v in e.ledger))
        if not (valid_bow or valid_melee):
            raise UnresolvedDecision("Lethal event lacks paid source-attested combat")
        if any(v["kind"]=="g6d_hunter_defeat_attested" for v in e.ledger):
            raise ValueError("Hunter defeat terminal already attested")
        e.log("g6d_hunter_defeat_attested",hunter=hunter,
              party=party,lethal_damage_index=lethal["index"],
              hp=h.hp,source_digest=h.source.digest,
              source_event_cause=cause,round=e.round,
              outcome="hunter_dead_after_actual_native_combat",
              hunter_cr=None)
        return {"ending":"hunter_defeat_attested",
                "terminal_event":len(e.ledger)-1,
                "round":e.round,"hunter_cr":None,"complete_party_pack_certified":False}


def run_i3_defeat(*,level=3,seed=640):
    """Real 4-PC I3 window: two established rounds + one paid Bow lethal shot.

    The third round is completed with genuine turns. Death is not inferred
    from the second round's Dying wound; it occurs only from the sourced R
    natural-20, two source critical d4s and a real G4 lethal packet.
    """
    if type(level) is not int or level not in (2,3):
        raise ValueError("Only authored L2/L3 mixed party")
    from scripts.b06_hunter_mixed_party_g6c_v0 import (
        mixed_scene,_hunter_turn,_priest_turn,_archer_turn,_scholar_turn,
    )
    combat=mixed_scene(size=4,level=level,seed=seed)
    e=combat.e
    for round_no in (1,2):
        if round_no==2:
            combat.bridge.begin_next_round()
        _hunter_turn(combat,round_no)
        _priest_turn(combat,"vanguard",round_no)
        _priest_turn(combat,"guardian",round_no)
        _archer_turn(combat,round_no)
        _scholar_turn(combat,round_no)
    if e.actors["hunter"].hp>=1 or e.actors["hunter"].dead:
        raise AssertionError("Hunter must have genuine G4 Dying wound, not death")
    combat.bridge.begin_next_round()
    for ident in ("hunter","vanguard","guardian"):
        combat.bridge.start_next_turn(RegenerationChoice())
        combat.bridge.end_current_turn()
    combat.bridge.start_next_turn(RegenerationChoice())
    completion=HunterCompletion(combat)
    finishing=completion.bow_hit("archer","hunter",primary_face=20,
                                confirmation_face=20,critical_dice=(4,4),
                                damage_face=4,target_cell=e.g1.body_cell("hunter","head"))
    combat.bridge.end_current_turn()
    combat.bridge.start_next_turn(RegenerationChoice())
    combat.bridge.end_current_turn()
    terminal=completion.attest_hunter_defeat(
        "hunter",party_ids=("vanguard","guardian","archer","scholar"))
    report=combat.report()
    return {"terminal":terminal,"finishing_shot":finishing,
            "source_report":report,"ledger":deepcopy(e.ledger),
            "hunter_hp":e.actors["hunter"].hp,
            "hunter_dead":e.actors["hunter"].dead,
            "rounds":e.round,"roster":list(e.order),
            "complete_party_pack_certified":False,
            "hunter_cr":None}
