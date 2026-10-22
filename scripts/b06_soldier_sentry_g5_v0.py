"""B06 G5 v0: source-bound Soldier/Sentry melee and narrow terminal scenes.

No generic AI, unsupported Opportunity effects, protective intervention,
Hunter contact, victory-from-zero-HP or implicit dice. G0/G1/G3/G4/G4.5
remain authoritative for their separate costs and state transitions.
"""
from copy import deepcopy
from dataclasses import dataclass
import json

from scripts.b06_encounter_state_v0 import (
    Encounter, RegenerationChoice, Trigger, UnresolvedDecision,
    ROOT, enemy_actor, party_actor)
from scripts.b06_movement_v0 import GridMovement
from scripts.b06_spells_v0 import SpellState
from scripts.b06_damage_v0 import DamageState
from scripts.b06_wound_continuation_v0 import WoundContinuation


def _face(value,sides,label):
    if type(value) is not int or not 1<=value<=sides:
        raise UnresolvedDecision(f"Explicit {label} d{sides} face required")
    return value


@dataclass(frozen=True)
class SceneExit:
    """Independent, immutable scene declaration, not a withdrawal claim.

    A scene author must bind an actor to a map-border exit and exact exit
    policy before opening the G5 adapter; callers cannot choose new exits
    or policies at withdrawal time.
    """
    encounter_scene: str
    grid_scene: str
    objective: str
    actor_id: str
    square: tuple
    policy_id: str


class SourceMelee:
    """Resolve ordinary 1x1 Soldier/Sentry sword sequences in genuine G0 time.

    This adapter makes hit and defense adjudication real instead of taking
    G4.5's external confirmed-hit flag on faith. Every provided die face is
    a declared, reproducible policy/input and retained in the event ledger.
    G5 does not choose a player defense, roll, or tactical response itself.
    """
    def __init__(self,encounter,*,scene_exit=None,scene_exits=()):
        if (type(scene_exits) is not tuple
                or (scene_exit is not None and scene_exits)
                or any(not isinstance(v,SceneExit) for v in scene_exits)):
            raise ValueError("Select one single exit or a preauthored tuple")
        authored=(scene_exit,) if scene_exit is not None else scene_exits
        if len({v.actor_id for v in authored})!=len(authored):
            raise ValueError("One independently authored G5 exit per actor")
        if any(getattr(encounter,x,None) is None for x in ("g1","g3","g4")):
            raise ValueError("Install native G1, G3 and G4 before G5")
        for exit in authored:
            g=encounter.g1
            square=exit.square
            if (exit.encounter_scene!=encounter.scenario
                    or exit.grid_scene!=g.scene_id
                    or exit.objective!=encounter.objective
                    or exit.actor_id not in encounter.actors
                    or not isinstance(square,tuple) or len(square)!=2
                    or any(type(v) is not int for v in square)
                    or not g.inside(square)
                    or not (square[0] in (0,g.width-1)
                            or square[1] in (0,g.height-1))
                    or not isinstance(exit.policy_id,str)
                    or not exit.policy_id):
                raise ValueError("Scene exit must match source scene, border and objective")
            if len(encounter.actors[exit.actor_id].occupied)!=1:
                raise ValueError("G5 scene exit requires a one-square actor")
        if getattr(encounter,"g5",None) is not None:
            raise ValueError("G5 melee already attached to encounter")
        # Native G0 supports declarations independently of this adapter.
        # An earlier attack_sequence_committed has already spent AP and
        # assigned defenses, but has no G5-attested action slots. Importing
        # it would require reconstructing previously resolved choices and
        # legal effects; accepting it would let native end_turn silently
        # discard the paid attack. Attach G5 *before* the first sequence.
        # Reject prior-round records as well: we cannot certify their
        # completion merely from a turn boundary.
        if any(ev["kind"]=="attack_sequence_committed"
               for ev in encounter.ledger):
            raise UnresolvedDecision(
                "Attach G5 before any untracked native Attack Sequence")
        self.e=encounter
        self.scene_exit=scene_exit
        # Both single and multiple exit arrangements are fixed at attach
        # time; withdrawals cannot supply or replace their own policies.
        self.scene_exits=tuple(authored)
        # Authorize only this adapter's synchronous native G0 declaration.
        # Standalone Encounter.declare_sequence cannot strand paid slots.
        self._native_sequence_authorized=False
        self.bridge=WoundContinuation(encounter)
        encounter.g5=self
        for exit in authored:
            encounter.log("g5_scene_exit_authored",
                          encounter_scene=exit.encounter_scene,
                          grid_scene=exit.grid_scene,
                          objective=exit.objective,
                          actor=exit.actor_id,
                          square=exit.square,policy=exit.policy_id)

    def pending_attack_slots(self,actor_id=None):
        """Read the authoritative encounter ledger, never caller receipts.

        A paid slot is unresolved until its exact G5 action index has a
        later native outcome (resolved or explicitly trigger-cancelled).
        Look across ALL prior turns/rounds for terminal validation:
        silently missing an enemy attack cannot be cured by Round Begin.
        """
        pending=[]
        ledger=self.e.ledger
        for committed in ledger:
            if committed["kind"]!="g5_melee_sequence_attested":
                continue
            d=committed["detail"]
            if actor_id is not None and d.get("attacker")!=actor_id:
                continue
            for slot,index in enumerate(d["action_indices"]):
                if not any(outcome["index"]>committed["index"]
                           and outcome["kind"] in (
                               "g5_melee_resolved","g5_melee_cancelled")
                           and outcome["detail"].get("action_index")==index
                           for outcome in ledger):
                    pending.append({"attacker":d["attacker"],
                                    "declaration_index":d["declaration_index"],
                                    "slot":slot,"action_index":index})
        return tuple(pending)

    def assert_sequence_declaration_allowed(self,actor_id):
        """One pending G5 Attack Sequence per actor, regardless of target.

        G0 normally locks one ordinary sequence only *per target*. G5 must
        close all pre-paid slots before declaring another target's sequence,
        or a later action invalidates G4.5's old live-action binding.
        """
        if self.pending_attack_slots(actor_id):
            raise UnresolvedDecision(
                "Complete pending G5 Attack Sequence before declaring another")

    def assert_ap_commitment_allowed(self,actor_id):
        """G0 spend_ap gate for ALL new own-turn costs, including reserve().

        Native declare_sequence() pays every initial profile before its G5
        sequence attestation exists. Once attested, no other on-turn AP spend
        may invalidate an unresolved action; completion restores normal
        spending for any remaining AP in that turn.
        """
        if self.pending_attack_slots(actor_id):
            raise UnresolvedDecision(
                "Complete pending G5 Attack Sequence before committing Turn AP")

    def assert_turn_completion_allowed(self,actor_id):
        """G0 calls before END TURN consumes resources or advances cursor."""
        # Defensive backstop if a source-owned death was applied outside a
        # usual G4 hit callback; healthy unresolved slots still block.
        self.cancel_incapacitated_attacker(actor_id)
        if self.pending_attack_slots(actor_id):
            raise UnresolvedDecision(
                "Resolve or explicitly cancel every committed G5 attack slot "
                "before ending the attacker turn")

    def assert_movement_allowed(self,actor_id):
        """No ordinary G1 movement while this actor's paid G5 sequence is open.

        Authoritative G5 ledger markers track the *entire* precommitted
        sequence. Only a future separately adjudicated attack-response
        path may authorize movement inside its own live window; this v0
        has no such response policy.
        """
        if self.e.current!=actor_id:
            return
        for ev in reversed(self.e.ledger):
            if (ev["kind"]!="g5_melee_sequence_attested"
                    or ev["round"]!=self.e.round
                    or ev["turn"]!=actor_id
                    or ev["detail"].get("attacker")!=actor_id):
                continue
            actions=ev["detail"]["action_indices"]
            for index in actions:
                if not any(x["kind"] in ("g5_melee_resolved","g5_melee_cancelled")
                           and x["detail"].get("action_index")==index
                           for x in self.e.ledger[ev["index"]+1:]):
                    raise UnresolvedDecision(
                        "Complete committed G5 Attack Sequence before movement")
            return

    def _contact(self,attacker,target):
        a=self.e.actors[attacker]
        return self.e.g1.melee_contact(
            attacker,target,hunter_front=(a.source.source_id=="B06-EN-03"))

    def _profile(self,attacker,profile_id):
        a=self.e.actors[attacker]
        if a.source.source_id in ("A","B"):
            from scripts.b06_player_offense_g6b_v0 import party_weapon_profile
            profile,bonus=party_weapon_profile(a,profile_id)
            return bonus
        if a.source.source_id not in ("B06-EN-01","B06-EN-02","B06-EN-03"):
            raise UnresolvedDecision("G5/G6 only resolves sourced enemy or A/B melee")
        if (a.source.source_id=="B06-EN-03"
                and profile_id not in ("B06-AT-04","B06-AT-05")):
            raise UnresolvedDecision("G6 Pounce and Horn Drive need their own commitment path")
        if profile_id not in a.source.attack_profiles:
            raise ValueError("Attack profile does not belong to attacker")
        obj=json.loads((ROOT/a.source.path).read_text(encoding="utf-8"))
        matches=[p for p in obj["attack_profiles"] if p["id"]==profile_id]
        if len(matches)!=1 or matches[0]["range_class"]!="melee":
            raise UnresolvedDecision("Missing source ordinary-melee attack profile")
        if a.source.source_id=="B06-EN-01" and (
                self.e.g3.sentry_profile(attacker)!=profile_id):
            raise ValueError("Sentry profile must match actually wielded Reserve")
        bonus=matches[0]["attack_roll"]["total_bonus"]
        if type(bonus) is not int:
            raise UnresolvedDecision("Sourced attack bonus required")
        return bonus

    def declare(self,attacker,target,*,profiles,defenses,
                prone_dodge_feasible=None,prone_guard_feasible=None,
                prone_attack_feasible=None):
        e=self.e
        # Reject before ANY declaration cost, chosen defense or roll. A
        # second target cannot invalidate a still-open earlier sequence.
        self.assert_sequence_declaration_allowed(attacker)
        if target not in e.actors or attacker not in e.actors or attacker==target:
            raise ValueError("Distinct existing attacker and target required")
        a,t=e.actors[attacker],e.actors[target]
        if a.team==t.team:
            raise ValueError("Cannot declare enemy sword against ally")
        if a.source.source_id in ("A","B") and t.source.source_id!="B06-EN-03":
            raise UnresolvedDecision("Bounded G6-B player melee only targets the Hunter")
        target_supported=(len(t.occupied)==1 or
                          (t.source.source_id=="B06-EN-03"
                           and t.footprint==("head","rear")
                           and len(t.occupied)==2))
        attacker_supported=(len(a.occupied)==1 or
                           (a.source.source_id=="B06-EN-03"
                            and a.footprint==("head","rear")
                            and len(a.occupied)==2))
        if not target_supported or not attacker_supported:
            raise UnresolvedDecision("G5/G6B requires sourced one-square or Hunter body contact")
        if not self._contact(attacker,target):
            raise UnresolvedDecision("G1 current actual melee contact required")
        profiles=tuple(profiles)
        defenses=tuple(defenses)
        if not profiles or len(profiles)!=len(defenses):
            raise ValueError("Complete physical sequence and defenses required")
        # The Prone -2 accuracy penalty does not make an otherwise unusable
        # sword attack legal. The actual required weapon/limb mechanics
        # must be affirmatively attested BEFORE any native sequence AP or
        # defender Guard/Dodge is committed. Merely holding a sword does
        # not establish that its attack can be made from this posture.
        if (any(str(c).lower()=="prone" for c in a.conditions) and
                prone_attack_feasible is not True):
            raise UnresolvedDecision(
                "Prone sword attack requires explicit physical feasibility before commitment")
        # A Prone creature may Dodge only when actual repositioning is
        # physically possible. G0 does not know the map/posture feasibility
        # and would otherwise debit Dodge Pressure on an illegal choice.
        # Never infer feasibility from the condition "Prone" alone.
        if ("dodge" in defenses and
                any(str(c).lower()=="prone" for c in t.conditions) and
                prone_dodge_feasible is not True):
            raise UnresolvedDecision(
                "Prone Dodge requires explicit physical capability before commitment")
        if ("guard" in defenses and
                any(str(c).lower()=="prone" for c in t.conditions) and
                prone_guard_feasible is not True):
            raise UnresolvedDecision(
                "Prone Guard requires explicit instrument feasibility before commitment")
        # G0 assigns Guard after charging all sequence AP. A formerly ready
        # defender may have lost its actual instrument independently; that
        # must reject here, before any action, sequence lock or Guard is
        # committed. G0 repeats this preflight for callers without G5.
        if "guard" in defenses and (
                not t.guard_instrument or not t.ready_guard
                or t.guard_value is None):
            raise ValueError("Cannot Guard without ready legal instrument/capacity")
        bonuses=[self._profile(attacker,p) for p in profiles]
        before=len(e.ledger)
        self._native_sequence_authorized=True
        try:
            e.declare_sequence(attacker,target,profiles,defenses)
        finally:
            self._native_sequence_authorized=False
        changes=e.ledger[before:]
        paid=[x for x in changes if x["kind"]=="action_committed"]
        declared=[x for x in changes if x["kind"]=="attack_sequence_committed"]
        assigned=[x for x in changes if x["kind"]=="defense_assigned"]
        if len(paid)!=len(profiles) or len(assigned)!=len(profiles) or len(declared)!=1:
            raise AssertionError("Native G0 sequence ledger incomplete")
        e.log("g5_melee_sequence_attested",attacker=attacker,target=target,
              source_digest=a.source.digest,profiles=profiles,
              action_indices=[x["index"] for x in paid],
              defense_indices=[x["index"] for x in assigned],
              declaration_index=declared[0]["index"],
              prone_dodge_feasible=prone_dodge_feasible is True,
              prone_guard_feasible=prone_guard_feasible is True,
              prone_attack_feasible=prone_attack_feasible is True,
              source_bonuses=bonuses)
        return {"attacker":attacker,"target":target,
                "profiles":profiles,"actions":tuple(x["index"] for x in paid),
                "defenses":tuple(x["index"] for x in assigned),
                "declaration":declared[0]["index"]}

    def cancel_incapacitated_attacker(self,actor_id,*,damage_event_key=None):
        """Close committed G0-paid attacks lost to actual G4 incapacitation.

        The G4 damage hook calls this immediately after logging the native
        damage event. Unlike a response-window failure, an attacker now at
        HP <= 0 can never deliver its pending ordinary sword strikes.
        Neither AP nor assigned Guard/Dodge resources are refunded.
        Repeated calls are idempotent because the ledger owns pending slots.
        """
        a=self.e.actors[actor_id]
        if a.hp>0 and not a.dead:
            return ()
        cancelled=[]
        for pending in self.pending_attack_slots(actor_id):
            declaration=self.e.ledger[pending["declaration_index"]]
            target=declaration["detail"]["target"]
            self.e.log("g5_melee_cancelled",
                       action_index=pending["action_index"],
                       declaration_index=pending["declaration_index"],
                       slot=pending["slot"],attacker=actor_id,target=target,
                       reason="attacker_dead_before_resolution" if a.dead
                              else "attacker_dying_before_resolution",
                       damage_event_key=damage_event_key,
                       attacker_hp=a.hp,attacker_dead=a.dead,
                       ap_refunded=0,defense_commitments_refunded=False)
            cancelled.append(pending["action_index"])
        return tuple(cancelled)

    def _current_target_for_slot(self,declaration,action_index,original_target):
        """The last genuine paid-suffix retarget controls this exact action."""
        bindings=[ev for ev in self.e.ledger
                  if ev["kind"]=="g5_melee_retarget_committed"
                  and ev["detail"].get("declaration_index")==declaration
                  and action_index in ev["detail"].get("action_indices",())]
        if not bindings:
            return original_target,None
        chosen=bindings[-1]["detail"]
        return chosen["target"],chosen

    def _pending_suffix(self,sequence):
        """Only the still-unresolved ordered suffix can be redirected."""
        declaration=sequence["declaration"]
        native=self.e.ledger[declaration]
        if (native["kind"]!="attack_sequence_committed"
                or native["detail"].get("attacker")!=sequence["attacker"]
                or native["detail"].get("target")!=sequence["target"]
                or native["detail"].get("profiles")!=list(sequence["profiles"])):
            raise UnresolvedDecision("G0 committed sequence no longer matches original declaration")
        actions=tuple(sequence["actions"])
        pending=self.pending_attack_slots(sequence["attacker"])
        suffix=[p for p in pending if p["declaration_index"]==declaration]
        if not suffix:
            raise ValueError("No remaining paid G5 attack slots")
        if [p["action_index"] for p in suffix]!=list(actions[suffix[0]["slot"]:]):
            raise UnresolvedDecision("Retarget/decline requires an intact pending suffix")
        return suffix

    def _supported_suffix_target(self,attacker,target_id):
        """G5/G6-B source-authorized target footprint for a paid suffix.

        A/B proxy attacks have *only* the sourced Hunter as a legal target,
        including after any redirection; generic Soldier/Sentry attacks
        retain their one-square target support. The Hunter's anatomical
        two-square body is never itself a reason to abandon paid attacks.
        """
        actor=self.e.actors[attacker]
        target=self.e.actors[target_id]
        if len(actor.occupied)!=1:
            return False
        if target.source.source_id=="B06-EN-03":
            return (target.footprint==("head","rear")
                    and len(target.occupied)==2)
        return (actor.source.source_id not in ("A","B")
                and len(target.occupied)==1)

    def _paid_target_unavailable(self,attacker,target_id):
        """Only genuine source targeting illegality unlocks a paid suffix.

        A non-dead creature with HP <= 0 is still an attackable Dying
        target. Its precommitted active Guard/Dodge falls back to Take Hit
        during resolve(); unconsciousness alone never grants a redirect
        or refund of the already paid attacks.
        """
        actor=self.e.actors[attacker]
        target=self.e.actors[target_id]
        return (target.dead or target.team==actor.team
                or not self._supported_suffix_target(attacker,target_id)
                or not self._contact(attacker,target_id))

    def retarget_remaining(self,sequence,new_target,*,defenses,
                           prone_dodge_feasible=None,prone_guard_feasible=None):
        """Redirect already-funded suffix; only NEW defender resources are paid.

        Original profiles and payment IDs never change; only a previously
        unattacked eligible target receives newly selected pre-roll defenses.
        """
        e=self.e
        attacker=sequence["attacker"]
        suffix=self._pending_suffix(sequence)
        if e.current!=attacker or e.pending_regeneration is not None or (
                e.actors[attacker].hp<=0):
            raise UnresolvedDecision("Retarget requires a live current attacker")
        original=sequence["target"]
        prior_target,_=self._current_target_for_slot(
            sequence["declaration"],suffix[0]["action_index"],original)
        if not self._paid_target_unavailable(attacker,prior_target):
            raise UnresolvedDecision("Original target remains legal for paid follow-ups")
        if new_target not in e.actors or new_target==attacker or (
                e.actors[new_target].team==e.actors[attacker].team):
            raise ValueError("New target must be a distinct opposing creature")
        target=e.actors[new_target]
        # The G6-B A/B player attack cannot escape its Hunter-only target
        # scope through a previously funded G5 suffix. Check source AND
        # anatomical shape before committing newly assigned defenses.
        # A living Dying creature remains an eligible attack target.
        if not self._supported_suffix_target(attacker,new_target):
            raise UnresolvedDecision(
                "Paid suffix requires source-authorized target footprint "
                "(A/B only against Hunter)")
        if target.dead or not self._contact(attacker,new_target):
            # Keep the previously verified one-square G5 diagnostic while
            # recognizing the Hunter's independently supported 1x2 body.
            label=("1x1" if len(target.occupied)==1 else "Hunter")
            raise UnresolvedDecision(
                f"Redirect target needs genuine live {label} G1 contact")
        if (attacker,new_target) in e.seen_sequences:
            raise UnresolvedDecision("Retarget cannot reopen a previously attacked target")
        defenses=tuple(defenses)
        if len(defenses)!=len(suffix) or any(x not in
                ("take_hit","guard","dodge") for x in defenses):
            raise ValueError("One valid newly assigned defense per funded remaining profile")
        # Recheck Dying at the NEW target before calling G0 defense().
        # Mixed/active response declarations may not spend a Guard or
        # advance Dodge Pressure on someone unable to defend actively.
        if target.hp<=0 and any(choice!="take_hit" for choice in defenses):
            raise ValueError("Dying redirect target requires Take Hit for every paid follow-up")
        if (defenses.count("guard")>target.guard_remaining
                or ("guard" in defenses and
                    (not target.ready_guard or not target.guard_instrument or
                     target.guard_value is None))):
            raise ValueError("Retarget defender has insufficient legal Guard")
        if ("dodge" in defenses and
                any(str(x).lower()=="prone" for x in target.conditions)
                and prone_dodge_feasible is not True):
            raise UnresolvedDecision("Retarget Prone Dodge requires physical feasibility")
        if ("guard" in defenses and
                any(str(x).lower()=="prone" for x in target.conditions)
                and prone_guard_feasible is not True):
            raise UnresolvedDecision("Retarget Prone Guard requires instrument feasibility")
        # Validate all fixed original profiles before paying ANY newly chosen
        # defense; the redirect cannot change weapon/effect eligibility.
        for entry in suffix:
            self._profile(attacker,sequence["profiles"][entry["slot"]])
        start=len(e.ledger)
        for entry,choice in zip(suffix,defenses):
            e.defense(new_target,choice,
                      attack_key=f"{attacker}:{new_target}:redirect:{sequence['declaration']}:{entry['slot']}")
        assigned=[ev["index"] for ev in e.ledger[start:]
                  if ev["kind"]=="defense_assigned"]
        if len(assigned)!=len(suffix):
            raise AssertionError("G0 redirected defense allocation incomplete")
        e.seen_sequences.add((attacker,new_target))
        e.log("g5_melee_retarget_committed",
              attacker=attacker,original_target=original,
              from_target=prior_target,target=new_target,
              declaration_index=sequence["declaration"],
              start_slot=suffix[0]["slot"],
              profiles=[sequence["profiles"][x["slot"]] for x in suffix],
              action_indices=[x["action_index"] for x in suffix],
              defense_indices=assigned,defenses=defenses,
              prone_dodge_feasible=prone_dodge_feasible is True,
              prone_guard_feasible=prone_guard_feasible is True,
              ap_spent=0,old_defense_commitments_refunded=False)
        e.check()
        return {"target":new_target,"action_indices":tuple(x["action_index"] for x in suffix),
                "defense_indices":tuple(assigned)}

    def decline_remaining(self,sequence,*,reason="target_unavailable"):
        """Explicitly abandon the still-paid suffix; never auto-cancel on kill."""
        suffix=self._pending_suffix(sequence)
        e=self.e
        attacker=sequence["attacker"]
        if e.current!=attacker or e.pending_regeneration is not None or (
                e.actors[attacker].hp<=0):
            raise UnresolvedDecision("Decline must be made by live current attacker")
        prior,_=self._current_target_for_slot(
            sequence["declaration"],suffix[0]["action_index"],sequence["target"])
        if reason!="target_unavailable" or not self._paid_target_unavailable(
                attacker,prior):
            raise UnresolvedDecision("Explicit decline requires an unavailable target")
        for entry in suffix:
            e.log("g5_melee_cancelled",attacker=attacker,target=prior,
                  action_index=entry["action_index"],
                  declaration_index=sequence["declaration"],
                  slot=entry["slot"],reason="explicit_decline_target_unavailable",
                  ap_refunded=0,defense_commitments_refunded=False)
        e.check()
        return tuple(x["action_index"] for x in suffix)

    def resolve(self,sequence,slot,*,attack_face,damage_face=None,
                confirmation_face=None,critical_dice=(),vigor_die=None,
                wound_location_roll=None,spontaneous_policy="decline_all",
                venom_resistance_die=None,venom_resistance_modifier=0):
        e=self.e
        attacker,target=sequence["attacker"],sequence["target"]
        if type(slot) is not int or slot not in range(len(sequence["profiles"])):
            raise ValueError("Source attack slot required")
        if spontaneous_policy!="decline_all":
            raise UnresolvedDecision("Nontrivial Reaction/Interception requires separate G5 authority")
        if venom_resistance_die is not None:
            _face(venom_resistance_die,20,"Hunter venom resistance")
        if type(venom_resistance_modifier) is not int:
            raise ValueError("Venom resistance modifier must be integer")
        action_index=sequence["actions"][slot]
        defense_index=sequence["defenses"][slot]
        declaration=sequence["declaration"]
        if any(type(i) is not int or i<0 or i>=len(e.ledger)
               for i in (action_index,defense_index,declaration)):
            raise ValueError("No valid native G0 source indices")
        if e.current!=attacker or e.pending_regeneration is not None:
            raise ValueError("Only current live attack sequence can resolve")
        # A prior genuine damage event may have removed the attacker after
        # payment. Cancel these *specific* paid slots before the G1 contact
        # gate (which would otherwise report a permanent unresolved attack).
        if e.actors[attacker].hp<=0 or e.actors[attacker].dead:
            self.cancel_incapacitated_attacker(attacker)
            raise UnresolvedDecision(
                "Attacker incapacitated; remaining G5 sequence slots cancelled")
        native=e.ledger[declaration]
        if native["round"]!=e.round or native["turn"]!=attacker:
            raise UnresolvedDecision(
                "G5 attack action/declaration must belong to current round and turn")
        # Reconstruct EVERY payment from the canonical G0 declaration,
        # including earlier slots. The public sequence result is a mutable
        # convenience receipt, never an authority for attack ordering.
        # A prior-round resolved action ID must not masquerade as this
        # round's already-resolved slot and unlock a later Dodge12 attack.
        native_profiles=native["detail"].get("profiles")
        if (native["kind"]!="attack_sequence_committed"
                or native["detail"].get("attacker")!=attacker
                or native["detail"].get("target")!=target
                or not isinstance(native_profiles,list) or not native_profiles
                or native_profiles!=list(sequence["profiles"])):
            raise UnresolvedDecision("G0 pre-roll declaration or defense mismatched")
        payments=[ev for ev in e.ledger[:declaration]
                  if ev["kind"]=="action_committed"
                  and ev["round"]==native["round"]
                  and ev["turn"]==attacker
                  and ev["detail"].get("actor")==attacker]
        payments=payments[-len(native_profiles):]
        if (len(payments)!=len(native_profiles) or
                any(ev["detail"].get("action_class")!="physical" or
                    ev["detail"].get("label")!=f"sequence:{profile}:{i}"
                    for i,(ev,profile) in enumerate(
                        zip(payments,native_profiles)))):
            raise UnresolvedDecision("G0 native attack sequence payments mismatched")
        native_actions=tuple(ev["index"] for ev in payments)
        if (len(sequence["actions"])!=len(native_actions)
                or any(type(idx) is not int for idx in sequence["actions"])
                or tuple(sequence["actions"])!=native_actions):
            raise UnresolvedDecision(
                "G5 action index does not match declared attack slot")
        action_index=native_actions[slot]
        if any(x["kind"]=="g5_melee_resolved" and
               x["detail"].get("action_index")==action_index for x in e.ledger):
            raise ValueError("G5 action already resolved")
        if any(x["kind"]=="g5_melee_cancelled" and
               x["detail"].get("action_index")==action_index for x in e.ledger):
            raise ValueError("G5 action already cancelled")
        # Both source indices AND earlier outcomes come from the native
        # declaration. A caller cannot substitute an older resolved index.
        for prior in native_actions[:slot]:
            if not any(x["kind"] in ("g5_melee_resolved","g5_melee_cancelled")
                       and x["detail"].get("action_index")==prior
                       for x in e.ledger):
                raise UnresolvedDecision(
                    "Resolve or lose earlier declared attack slots first")
        # Any completed G1 movement by the attacker since the native
        # declaration would be an illegal interleaving of turn resources,
        # even if the new position stays adjacent. This additionally
        # protects against direct G1 entry points bypassing our proactive
        # movement guard. No response-authorized movement exists in G5 v0.
        if any(x["kind"] in ("g1_movement_step",
                             "g1_allied_transit_step",
                             "g1_allied_transit_finished")
               and x["detail"].get("actor")==attacker
               for x in e.ledger[declaration+1:]):
            raise UnresolvedDecision(
                "Committed G5 Attack Sequence cannot interleave movement")
        # The original G0 target/profile receipt remains unchanged; a
        # separately committed G5 redirection may redirect this paid suffix.
        target,rebound=self._current_target_for_slot(
            declaration,action_index,target)
        if not self._contact(attacker,target):
            raise UnresolvedDecision("Actual G1 contact lost before attack roll")
        p=native_profiles[slot]
        action=e.ledger[action_index]
        # Every outcome, INCLUDING natural-1 misses, must consume an action
        # committed for this exact live turn. Without this preflight a stale
        # sequence could log a new-round miss without having paid new AP.
        if (action["kind"]!="action_committed"
                or action["round"]!=e.round or action["turn"]!=attacker
                or action["detail"].get("actor")!=attacker
                or action["detail"].get("action_class")!="physical"
                or native["round"]!=e.round or native["turn"]!=attacker):
            raise UnresolvedDecision(
                "G5 attack action/declaration must belong to current round and turn")
        # An explicitly reserved G0 Interception is a more specific
        # unresolved blocker than a later unrelated Physical Action spend.
        # Check it before evaluating the sequence's live-action window,
        # without consuming the reservation or opening its response window.
        trigger_key=f"g5:melee:{action_index}"
        if any(r.trigger_key==trigger_key for r in e.reservations):
            raise UnresolvedDecision("Reserved Interception needs explicit G5 resolution")
        # Reuse G4.5's canonical paid sequence binding for BOTH hit and miss.
        # Its returned position prevents relabeling one paid slot as another
        # even when a multi-attack sequence repeats the same profile.
        bound_declaration,bound_slot=self.bridge._bound_attack_declaration(
            attacker,target,p,action_index)
        if bound_declaration!=declaration or bound_slot!=slot:
            raise UnresolvedDecision(
                "G5 action index does not match declared attack slot")
        if (native["kind"]!="attack_sequence_committed"
                or native["detail"].get("attacker")!=attacker
                or native["detail"].get("target")!=sequence["target"]
                or native["detail"].get("profiles")!=list(sequence["profiles"])
                or len(sequence["defenses"])!=len(sequence["profiles"])):
            raise UnresolvedDecision("G0 pre-roll declaration or defense mismatched")
        # G0 emits one defense_assigned per committed profile, immediately
        # after attack_sequence_committed and in profile order. Rebind every
        # supplied event index to this exact declaration AND canonical slot.
        # Merely comparing labels is not enough: consecutive Dodge values
        # differ because Dodge Pressure is paid at declaration.
        assigned=[]
        for i,declared_defense in enumerate(native["detail"].get("defenses",())):
            canonical_index=declaration+1+i
            if (canonical_index>=len(e.ledger)
                    or type(sequence["defenses"][i]) is not int
                    or sequence["defenses"][i]!=canonical_index):
                raise UnresolvedDecision(
                    "G0 assigned defense event does not match declared slot")
            ev=e.ledger[canonical_index]
            if (ev["kind"]!="defense_assigned"
                    or ev["round"]!=e.round or ev["turn"]!=attacker
                    or ev["detail"].get("actor")!=sequence["target"]
                    or ev["detail"].get("attack_key")!=
                    f"{attacker}:{sequence['target']}:{i}"
                    or ev["detail"].get("defense")!=declared_defense):
                raise UnresolvedDecision(
                    "G0 assigned defense event does not match declared slot")
            assigned.append(ev)
        if (len(assigned)!=len(sequence["profiles"])
                or native["detail"]["defenses"]!=[
                    event["detail"]["defense"] for event in assigned]):
            raise UnresolvedDecision("G0 pre-roll declaration or defense mismatched")
        d=assigned[slot]
        if rebound is not None:
            positions=[i for i,index in enumerate(rebound["action_indices"])
                       if index==action_index]
            if len(positions)!=1:
                raise UnresolvedDecision("Retargeted attack slot not found")
            position=positions[0]
            defense_index=rebound["defense_indices"][position]
            if type(defense_index) is not int or not 0<=defense_index<len(e.ledger):
                raise UnresolvedDecision("Retargeted defender has no source defense")
            d=e.ledger[defense_index]
            if (d["kind"]!="defense_assigned" or d["round"]!=e.round
                    or d["detail"].get("actor")!=target
                    or d["detail"].get("defense")!=rebound["defenses"][position]
                    or d["detail"].get("attack_key")!=
                    f"{attacker}:{target}:redirect:{declaration}:{slot}"):
                raise UnresolvedDecision("Retargeted defense does not match paid slot")
        elif d["index"]!=defense_index:
            raise UnresolvedDecision(
                "G0 assigned defense event does not match declared slot")
        if (d["detail"]["defense"]=="dodge"
                and any(str(c).lower()=="prone"
                        for c in e.actors[target].conditions)):
            attested=next((ev for ev in e.ledger[declaration+1:]
                           if ev["kind"]=="g5_melee_sequence_attested"
                           and ev["detail"].get("declaration_index")==declaration),
                          None)
            if (rebound is not None and
                    rebound.get("prone_dodge_feasible") is not True):
                raise UnresolvedDecision(
                    "Retarget Prone Dodge needs precommitted physical feasibility")
            if (rebound is None and
                    (attested is None or
                     attested["detail"].get("prone_dodge_feasible") is not True)):
                raise UnresolvedDecision(
                    "Prone Dodge requires explicit physical capability before resolution")
        if (d["detail"]["defense"]=="guard"
                and e.actors[target].hp>0 and not e.actors[target].dead
                and any(str(c).lower()=="prone"
                        for c in e.actors[target].conditions)):
            attested=next((ev for ev in e.ledger[declaration+1:]
                           if ev["kind"]=="g5_melee_sequence_attested"
                           and ev["detail"].get("declaration_index")==declaration),
                          None)
            if (rebound is not None and
                    rebound.get("prone_guard_feasible") is not True):
                raise UnresolvedDecision(
                    "Retarget Prone Guard needs precommitted instrument feasibility")
            if (rebound is None and
                    (attested is None or
                     attested["detail"].get("prone_guard_feasible") is not True)):
                raise UnresolvedDecision(
                    "Prone Guard requires explicit instrument feasibility before resolution")
        # The attacker may have become Prone after paying for the
        # sequence. Never turn an unattested sword action into a legal
        # hit simply by applying its -2 modifier. Retain the already
        # committed slot until a separately supported resolution exists.
        if any(str(c).lower()=="prone" for c in e.actors[attacker].conditions):
            attested=next((ev for ev in e.ledger[declaration+1:]
                           if ev["kind"]=="g5_melee_sequence_attested"
                           and ev["detail"].get("declaration_index")==declaration),
                          None)
            if (attested is None or
                    attested["detail"].get("prone_attack_feasible") is not True):
                raise UnresolvedDecision(
                    "Prone sword attack requires explicit physical feasibility before resolution")
        source_bonus=self._profile(attacker,p)
        # Live Prone positioning changes melee accuracy, NOT source training.
        # Two Prone creatures do not each receive a reciprocal +2.
        attacking_prone=any(str(c).lower()=="prone"
                            for c in e.actors[attacker].conditions)
        target_prone=any(str(c).lower()=="prone"
                         for c in e.actors[target].conditions)
        prone_modifier=(-2 if attacking_prone else 2 if target_prone else 0)
        bonus=source_bonus+prone_modifier
        declared_defense=d["detail"]["defense"]
        defense=declared_defense
        value=d["detail"]["defense_value"]
        if e.actors[target].dead:
            raise UnresolvedDecision("Target already dead, no further live attack")
        # Defense was genuinely committed pre-roll, but a subsequently
        # Dying creature cannot actively Guard or Dodge a later attack.
        # Keep the already spent Guard/Dodge pressure; use Take Hit instead.
        dying_fallback=(e.actors[target].hp<=0
                        and declared_defense in ("guard","dodge"))
        if dying_fallback:
            defense="take_hit"
            value=None
        elif (defense=="guard" and (
                not e.actors[target].ready_guard or
                not e.actors[target].guard_instrument)):
            raise UnresolvedDecision("Changed Guard requires native defensive fallback")
        attack_face=_face(attack_face,20,"initial melee attack")
        if attack_face==20:
            confirmation_face=_face(confirmation_face,20,"critical confirmation")
        elif confirmation_face is not None:
            raise ValueError("No confirmation roll without natural 20")
        if type(critical_dice) not in (tuple,list):
            raise ValueError("Explicit canonical critical dice required")
        total=attack_face+bonus
        hit=False if attack_face==1 else (
            True if defense=="take_hit" or attack_face==20 else total>value)
        critical="normal"
        if hit and attack_face==20:
            if defense=="take_hit":
                critical="devastating" if confirmation_face==20 else "critical"
            elif confirmation_face==20:
                critical="devastating"
            elif confirmation_face!=1 and confirmation_face+bonus>value:
                # Canonical natural 1 is an automatic miss for the
                # confirmation attack, regardless of high source bonus or
                # reduced Dodge Defense from accumulated Dodge Pressure.
                critical="critical"
            else:
                critical="strong"
        expected={"normal":0,"strong":1,"critical":2,"devastating":2}[critical]
        if (len(critical_dice)!=expected or any(
                type(x) is not int or not 1<=x<=4 for x in critical_dice)):
            raise ValueError("Exact critical d4 faces required")
        venom_exposure_key=None
        if hit:
            _face(damage_face,6,"source melee damage")
            # G4 owns the exact profile's typed packets, source Vigor die,
            # resistance/Armor calculation and wound-location requirement.
            # Run that preflight BEFORE response windows or roll logs, so
            # invalid missing dice cannot lead to contradictory retries.
            predicted=e.g4.preflight_profile_hit(
                attacker,target,p,die_face=damage_face,
                critical=critical,critical_dice=tuple(critical_dice),
                vigor_die=vigor_die,wound_location_roll=wound_location_roll)
            if p=="B06-AT-04":
                venom_exposure_key=f"g6:bite:{e.seed}:{action_index}"
                if predicted["hp_after"]>-e.actors[target].hp_max:
                    e.g4.venom.validate_exposure_key(venom_exposure_key)
                _,_,packets=e.g4._profile_hit_packets(
                    attacker,target,p,die_face=damage_face,
                    critical=critical,critical_dice=tuple(critical_dice))
                if (e.g4._mitigate_hp(e.actors[target],packets[0])>0
                        and predicted["hp_after"]>-e.actors[target].hp_max
                        and e.g4.venom.bite_resistance_required(target)
                        and venom_resistance_die is None):
                    raise UnresolvedDecision(
                        "Potential puncturing Hunter Bite requires precommitted venom d20")
        elif damage_face is not None:
            raise ValueError("Damage dice cannot be used for a miss")
        if dying_fallback:
            e.log("g5_defense_unavailable_fallback",attacker=attacker,
                  target=target,action_index=action_index,
                  declared=declared_defense,resolved="take_hit",
                  reason="target_dying_after_prior_sequence_slot",
                  guard_and_dodge_commitments_retained=True)
        # The native G0 response executor opens, rechecks, closes and logs
        # the trigger. This bounded policy explicitly DECLINES all eligible
        # spontaneous responses, but never silently consumes a reserved
        # Interception, whose effect executor is not part of G5 v0.
        trigger=Trigger(trigger_key,attacker,target)
        def recheck(e,tr):
            tr.legal=(e.current==attacker
                      and not e.actors[attacker].dead
                      and e.actors[attacker].hp>0
                      and not e.actors[target].dead
                      and self._contact(attacker,target))
        valid=e.response_window(trigger,on_interception=lambda *args: None,
                                spontaneous=(),after_interceptions=recheck)
        if not valid:
            e.log("g5_melee_cancelled",action_index=action_index,
                  trigger=trigger_key)
            raise UnresolvedDecision("Attack trigger canceled before roll")
        e.log("g5_melee_roll",action_index=action_index,
              declaration_index=declaration,slot=slot,
              attacker=attacker,target=target,profile=p,
              defense=defense,declared_defense=declared_defense,
              defense_value=value,attack_face=attack_face,
              source_attack_bonus=source_bonus,prone_modifier=prone_modifier,
              attack_bonus=bonus,attack_total=total,
              confirmation_face=confirmation_face,critical=critical,
              hit=hit,spontaneous_policy=spontaneous_policy)
        result=None
        if hit:
            def after_damage(damage):
                if p=="B06-AT-04" and not e.actors[target].dead:
                    damage["venom"]=e.g4.venom.apply_bite(
                        attacker,target,profile_hit_index=len(e.ledger)-1,
                        exposure_key=venom_exposure_key,
                        resistance_die=venom_resistance_die,
                        resistance_modifier=venom_resistance_modifier)
            result=self.bridge.verified_profile_hit(
                attacker,target,p,action_index=action_index,
                source_event=f"g5:source:{e.seed}:{action_index}",
                contact_reference=trigger_key,
                defense_reference=f"g0:defense:{defense_index}",
                contact_verified=True,defense_verified=True,
                die_face=damage_face,critical=critical,
                critical_dice=tuple(critical_dice),vigor_die=vigor_die,
                wound_location_roll=wound_location_roll,
                on_damage=after_damage if p=="B06-AT-04" else None)
        e.log("g5_melee_resolved",action_index=action_index,
              attacker=attacker,target=target,profile=p,
              outcome="hit" if hit else "miss",
              damage=result,critical=critical)
        # Even a fatal first hit retains any remaining paid slots.
        # The caller must redirect them to a new legal target, or explicitly
        # decline when the original target is no longer available.
        e.check()
        return {"outcome":"hit" if hit else "miss","critical":critical,
                "defense":defense,"defense_value":value,
                "declared_defense":declared_defense,
                "prone_modifier":prone_modifier,
                "attack_total":total,"damage":deepcopy(result),
                "action_index":action_index}

    def withdraw(self,actor_id):
        """Only a prior scene-authored border exit can end this encounter.

        No caller-selected exit_square or policy_id is accepted at withdrawal
        time. Independent authority derives from the immutable scene setup,
        combined with a native, completed G1 movement step at that square.
        """
        # Terminal evidence must not hide ANY unpaid-for-but-unresolved
        # source attack, even if a caller somehow bypassed the G0 end-turn
        # hook, or another actor/round subsequently took a turn.
        if self.pending_attack_slots():
            raise UnresolvedDecision(
                "Cannot attest G5 terminal withdrawal with unresolved "
                "committed attack slots")
        policy=next((x for x in self.scene_exits if x.actor_id==actor_id),None)
        if policy is None:
            raise UnresolvedDecision("Actor does not match a scene-authored exit policy")
        if (self.e.scenario!=policy.encounter_scene or
                self.e.objective!=policy.objective or
                self.e.g1.scene_id!=policy.grid_scene):
            raise UnresolvedDecision("Scene-authored exit context has changed")
        a=self.e.actors[actor_id]
        # A completed move is not an automatic escape: subsequent harm can
        # leave the actor unconscious at the same authored border square.
        # Eligibility is checked at the actual terminal attestation time.
        if a.hp<=0 or a.dead:
            raise ValueError("Dying/dead actor cannot withdraw")
        if len(a.occupied)!=1 or a.occupied[0]!=policy.square:
            raise UnresolvedDecision("Actor has not reached scene-authored exit square")
        if any(x["kind"]=="g5_terminal_exit" and
               x["detail"].get("actor")==actor_id
               for x in self.e.ledger):
            raise ValueError("Scene exit already attested")
        # A completed normal translation or *finished* atomic allied
        # transit may arrive at the authored border. Intermediate transit
        # steps are never terminal evidence, even if they visit that square.
        arrivals=[x for x in self.e.ledger[self.bridge.start:]
                  if x["detail"].get("actor")==actor_id and
                  (x["kind"]=="g1_allied_transit_finished" or
                   (x["kind"]=="g1_movement_step" and
                    x["detail"].get("step_kind") in
                        ("orthogonal","diagonal")))]
        if not arrivals:
            raise UnresolvedDecision(
                "Actual completed G1 movement to scene-authored exit required")
        last=arrivals[-1]
        if last["kind"]=="g1_movement_step":
            final=last["detail"].get("new")
        else:
            # G1's route-finish record contains count/cost, not coordinates.
            # Its immediate preceding source step supplies the final
            # position; G4.5 independently verifies the entire contiguous
            # paid route before accepting this finish event.
            previous=(self.e.ledger[last["index"]-1]
                      if last["index"]>self.bridge.start else None)
            final=(previous["detail"].get("new")
                   if previous is not None and
                   previous["kind"]=="g1_allied_transit_step" and
                   previous["detail"].get("actor")==actor_id else None)
        if (not isinstance(final,(tuple,list)) or len(final)!=1 or
                tuple(final[0])!=policy.square):
            raise UnresolvedDecision(
                "Actual final G1 movement to scene-authored exit required")
        evidence=self.bridge.attest_withdrawal(
            actor_id,movement_event_index=last["index"],
            exit_policy_reference=policy.policy_id,
            independently_verified=True)
        self.e.log("g5_terminal_exit",actor=actor_id,
                   at=policy.square,policy=policy.policy_id,
                   movement_index=last["index"])
        return evidence

    def report(self):
        evidence=self.bridge.report()
        pending=self.pending_attack_slots()
        return {"scene":self.e.scenario,"seed":self.e.seed,
                "objective":self.e.objective,
                "source_provenance":evidence["source_actor_states"],
                "ending":(
                    "unresolved" if pending
                    else "withdrawal_attested" if any(
                        x["kind"]=="g5_terminal_exit"
                        for x in self.e.ledger[self.bridge.start:])
                    else "death_attested" if any(a.dead for a in self.e.actors.values())
                    else "unresolved"),
                "outcomes":deepcopy(evidence["explicit_outcomes"]),
                "unresolved_attack_slots":deepcopy(pending),
                "attacks":deepcopy([x["detail"] for x in self.e.ledger
                    if x["kind"]=="g5_melee_resolved"]),
                "wounds":deepcopy(evidence["wound_creation_events"]),
                "current":evidence["current"],
                "complete_party_pack_certified":False,
                "hunter_cr":None}


def fixed_scene(pack,*,sentry_state=None,seed=501):
    """A single source-derived L3 Priest A witness opposing one benchmark foe."""
    if pack not in ("I1","I2"):
        raise ValueError("Only I1 Soldier or I2 Sentry defined")
    if pack=="I1":
        opponent=enemy_actor("B06-EN-02","foe","enemy",occupied=((3,2),))
    else:
        opponent=enemy_actor("B06-EN-01","foe","enemy",
                             start_state=sentry_state or "cold_start",
                             occupied=((3,2),))
    front=party_actor("A",3,"front","party",occupied=((2,2),))
    e=Encounter([opponent,front],{"foe":30,"front":20},seed=seed,
                scenario=f"B06-{pack}:"+(
                    opponent.source.start_state or "ordinary_start"),
                objective="front_reaches_verified_exit",
                policy="fixed_dice_declared_guard_or_take_hit_decline_responses")
    GridMovement(e,width=8,height=5,scene_id="G5-open-corridor")
    SpellState(e)
    DamageState(e)
    e.begin_round()
    # Only the I1/I2 author selects the exit policy. Caller attempts to
    # withdraw from arbitrary interior cells cannot rewrite this contract.
    scene_exit=SceneExit(e.scenario,e.g1.scene_id,e.objective,
                         "front",(0,2),"G5:open-corridor:exit-front")
    return SourceMelee(e,scene_exit=scene_exit)


def _retreat_on_turn(scene):
    e=scene.e
    scene.bridge.start_next_turn(RegenerationChoice())
    if e.current!="front":
        raise AssertionError("Exit turn expected front")
    # This is an explicit G5 scenario policy, not inferred AI:
    # all eligible Movement Opportunities are declined.
    for _ in range(2):
        if not e.g1.step("front",(-1,0),responses=lambda eligible: ()):
            raise UnresolvedDecision("Declared exit step was canceled")
    scene.withdraw("front")
    scene.bridge.end_current_turn()


def run_i1(*,seed=501):
    """I1 opponent Soldier Guard counterplay + actual Priest exit terminal."""
    scene=fixed_scene("I1",seed=seed)
    e=scene.e
    scene.bridge.start_next_turn(RegenerationChoice())
    sequence=scene.declare("foe","front",profiles=("B06-AT-03",),
                           defenses=("guard",))
    outcome=scene.resolve(sequence,0,attack_face=1)
    scene.bridge.end_current_turn()
    _retreat_on_turn(scene)
    report=scene.report()
    if report["ending"]!="withdrawal_attested":
        raise AssertionError("I1 scripted exit requires genuine terminal movement")
    report["i1_first_attack"]=outcome
    return report


def run_i2(*,state,seed=502):
    """I2 cold pays Projection then later enchants, prepared starts enchanted."""
    if state not in ("cold_start","prepared_start"):
        raise ValueError("Specify one of both source Sentry starts")
    scene=fixed_scene("I2",sentry_state=state,seed=seed)
    e=scene.e
    scene.bridge.start_next_turn(RegenerationChoice())
    if state=="cold_start":
        if e.g3.cast_sentry_reserve("foe") is None:
            raise UnresolvedDecision("Sentry cast failed")
        if e.actors["foe"].ap_remaining>=e.actors["foe"].physical_ap:
            raise AssertionError("Cold sentry cannot attack after Projection30")
        scene.bridge.end_current_turn()
        scene.bridge.start_next_turn(RegenerationChoice())
        scene.bridge.end_current_turn()
        scene.bridge.begin_next_round()
        scene.bridge.start_next_turn(RegenerationChoice())
    seq=scene.declare("foe","front",profiles=("B06-AT-02",),
                      defenses=("take_hit",))
    outcome=scene.resolve(seq,0,attack_face=11,damage_face=4,
                          vigor_die=4)
    scene.bridge.end_current_turn()
    _retreat_on_turn(scene)
    report=scene.report()
    if report["ending"]!="withdrawal_attested":
        raise AssertionError("I2 scripted exit requires genuine terminal movement")
    report["i2_first_hit"]=outcome
    report["start_state"]=state
    return report
