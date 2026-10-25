"""B06 G4.5: source-attested wound continuation, not a G5 encounter verdict.

This bridge *observes* native G0/G4 steps. It never invents contact,
critical confirmation, cure, withdrawal geometry or a new Regeneration Step.
"""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision

BLOCKERS=frozenset((
    "g5_contact_or_defense","g5_critical_confirmation",
    "missing_wound_location","exceptional_injury_rule",
    "g5_retreat_geometry","g6_tactical_policy","unresolved_response",
    "other_source_decision",
))


def _actor_state(a):
    return {"id":a.id,"source_id":a.source.source_id,
            "source_digest":a.source.digest,"hp":a.hp,"hp_max":a.hp_max,
            "vigor":a.vigor,"vigor_max":a.vigor_max,
            "dead":a.dead,"dying":a.hp<=0 and not a.dead,
            "vp_available":a.vp_available,
            "vp_committed":a.vp_committed,"vp_spent":a.vp_spent,
            "wounds":[{"id":w.ident,"source_event":w.source_event,
                       "severity":w.severity,"location":w.location,
                       "trauma":w.trauma,"requirement":w.requirement,
                       "progress":w.progress,"repairable":w.repairable,
                       "completed":w.progress==w.requirement}
                      for w in a.wounds]}


class WoundContinuation:
    def __init__(self,encounter):
        if getattr(encounter,"g4",None) is None:
            raise ValueError("Attach G4 before wound continuation")
        self.e=encounter
        self.d=encounter.g4
        self.start=len(encounter.ledger)
        self.seen_actions=set()
        self.outcomes=[]
        self.start_state={k:_actor_state(v) for k,v in encounter.actors.items()}
        self.e.log("g45_continuation_opened",
                   sources={k:a.source.digest for k,a in encounter.actors.items()},
                   scene=encounter.scenario)

    def snapshot(self):
        return {"round":self.e.round,"current":self.e.current,
                "clock_mode":self.d.clock.mode,
                "world_seconds":self.d.clock.world_seconds,
                "actors":{k:_actor_state(a) for k,a in self.e.actors.items()}}

    def _bound_attack_declaration(self,attacker,target,profile_id,action_index):
        """Bind a paid G0 action to its original target/profile declaration.

        G0's declare_sequence authorizes ordinary attack reservations; a
        generic physical spend (e.g. Interception reserve) never does.
        Full sequences precommit every profile/AP before rolling, so the
        matching source action is the corresponding ordered slot rather
        than simply the most recent physical action in the ledger.
        """
        ledger=self.e.ledger
        action=ledger[action_index]
        declarations=[ev for ev in ledger[action_index+1:]
                      if ev["kind"]=="attack_sequence_committed" and
                      ev["round"]==self.e.round and ev["turn"]==attacker]
        if not declarations:
            raise UnresolvedDecision(
                "G0 source-bound attack sequence declaration required")
        declaration=declarations[0]
        details=declaration["detail"]
        profiles=details.get("profiles")
        defenses=details.get("defenses")
        if (details.get("attacker")!=attacker or
                not isinstance(profiles,list) or
                not isinstance(defenses,list) or
                len(profiles)!=len(defenses) or not profiles):
            raise UnresolvedDecision(
                "Committed attack declaration does not match target/profile")
        # The N most recent actor Physical Actions before G0's sequence
        # marker must be its N ordered, exact profile-index payments.
        # G1 bookkeeping can occur between those AP events.
        paid=[ev for ev in ledger[:declaration["index"]]
              if ev["kind"]=="action_committed" and
              ev["round"]==self.e.round and ev["turn"]==attacker and
              ev["detail"].get("actor")==attacker]
        paid=paid[-len(profiles):]
        if (len(paid)!=len(profiles) or
                any(ev["detail"].get("action_class")!="physical" or
                    ev["detail"].get("label")!=f"sequence:{p}:{i}"
                    for i,(ev,p) in enumerate(zip(paid,profiles)))):
            raise UnresolvedDecision(
                "Paid actions do not match committed attack sequence")
        positions=[i for i,ev in enumerate(paid)
                   if ev["index"]==action_index]
        if (len(positions)!=1 or profiles[positions[0]]!=profile_id):
            raise UnresolvedDecision(
                "Committed attack action does not match declared target/profile")
        # G5 is the sole explicit retarget authority for a G0-paid suffix.
        # No invented second AP payment or free target reassignment: the
        # last source-attested redirect for this exact action must match.
        redirects=[ev["detail"] for ev in ledger
                   if ev["kind"]=="g5_melee_retarget_committed"
                   and ev["detail"].get("declaration_index")==declaration["index"]
                   and action_index in ev["detail"].get("action_indices",())]
        actual_target=(redirects[-1]["target"] if redirects
                       else details.get("target"))
        if actual_target!=target:
            raise UnresolvedDecision(
                "Committed attack declaration does not match target/profile")
        if redirects:
            chosen=redirects[-1]
            i=chosen["action_indices"].index(action_index)
            if (chosen.get("attacker")!=attacker
                    or chosen.get("original_target")!=details.get("target")
                    or chosen.get("profiles",())[i]!=profile_id
                    or (attacker,target) not in self.e.seen_sequences):
                raise UnresolvedDecision("Retarget lacks legal G5 paid-suffix authority")
        # The old committed sequence cannot be revived after beginning a
        # second action/sequence, even while the attacker remains current.
        if any(ev["kind"] in ("action_committed",
                              "attack_sequence_committed",
                              "turn_end","round_begin")
               for ev in ledger[declaration["index"]+1:]):
            raise UnresolvedDecision(
                "Physical hit must consume its current live attack sequence")
        # Per-action consumption survives reopening the bridge.
        if any(ev["kind"]=="g45_attested_hit" and
               ev["detail"].get("action_index")==action_index
               for ev in ledger):
            raise ValueError("G0 attack action already consumed in encounter")
        return declaration["index"],positions[0]

    def verified_profile_hit(self,attacker,target,profile_id,*,action_index,
                             source_event,contact_reference,defense_reference,
                             contact_verified,defense_verified,
                             die_face,critical="normal",critical_dice=(),
                             vigor_die=None,wound_location_roll=None,
                             on_damage=None,medium_intercessor=None):
        """Consume a *real* G0 Physical Action and an external G5 attestation.

        The caller, NOT G4.5, must have resolved contact, defense and critical
        tier. These refs document that independent decision, not fabricate it.
        """
        if any(type(x) is not str or not x for x in
               (source_event,contact_reference,defense_reference)):
            raise UnresolvedDecision("Stable G5 contact/defense source refs required")
        if contact_verified is not True or defense_verified is not True:
            raise UnresolvedDecision("G5 confirmed contact and defense required")
        # A malformed caller hook must not leave irreversible G4 damage,
        # a spent source action or a missing G4.5 provenance record.
        # Validate before the first stateful damage operation.
        if on_damage is not None and not callable(on_damage):
            raise TypeError("G5 post-damage hook must be callable")
        # The encounter's immutable serialized ledger is the shared
        # provenance registry. Another WoundContinuation instance must
        # never allow a previously accepted external source ID again.
        if any(ev["kind"]=="g45_attested_hit" and
               ev["detail"].get("source_event")==source_event
               for ev in self.e.ledger):
            raise ValueError("Source event already consumed in encounter")
        if type(action_index) is not int or action_index<self.start or (
                action_index>=len(self.e.ledger)):
            raise UnresolvedDecision("G0 in-scene Physical Action index required")
        if action_index in self.seen_actions:
            raise ValueError("G0 Physical Action already consumed by bridge")
        action=self.e.ledger[action_index]
        facts=action["detail"]
        if (action["kind"]!="action_committed"
                or facts.get("actor")!=attacker
                or facts.get("action_class")!="physical"
                or action["round"]!=self.e.round
                or action["turn"]!=attacker
                or self.e.current!=attacker
                or self.e.pending_regeneration is not None
                or self.e.actors[attacker].hp<=0):
            raise UnresolvedDecision("Current attacker needs genuine committed Physical Action")
        declaration_index,profile_index=self._bound_attack_declaration(
            attacker,target,profile_id,action_index)
        # G0 supplied the exact sequence payment and target/profile binding;
        # G4 supplies source JSON attack packets,
        # mitigation, exact one-event wound and native effects.
        result=self.d.apply_profile_hit(
            attacker,target,profile_id,die_face=die_face,
            confirmed_hit=True,critical=critical,
            critical_dice=critical_dice,vigor_die=vigor_die,
            wound_location_roll=wound_location_roll,
            medium_intercessor=medium_intercessor)
        self.seen_actions.add(action_index)
        # A Hunter Bite's delivered toxin must consume the newest G4 hit
        # synchronously, before G4.5 appends its own provenance event.
        # Only the resolved G5 adapter supplies this optional callback.
        if on_damage is not None:
            on_damage(result)
        self.e.log("g45_attested_hit",source_event=source_event,
                   attacker=attacker,target=target,profile=profile_id,
                   action_index=action_index,
                   sequence_declaration_index=declaration_index,
                   declared_profile_index=profile_index,
                   contact_reference=contact_reference,
                   defense_reference=defense_reference,
                   attacker_source=self.e.actors[attacker].source.digest,
                   target_source=self.e.actors[target].source.digest,
                   critical=critical,actual_result=result,
                   **({"medium_intercessor":medium_intercessor}
                      if medium_intercessor is not None else {}),
                   target_state=_actor_state(self.e.actors[target]))
        self.e.check()
        return result

    def verified_opportunity_hit(self,attacker,target,profile_id,*,trigger,
                                 response,response_index,pending_index,
                                 die_face,critical="normal",critical_dice=(),
                                 vigor_die=None,wound_location_roll=None):
        """G4.5 off-turn proof: consume ONE actual G0 Opportunity commitment.

        Unlike an ordinary turn attack, no AP action/sequence is fabricated.
        The immutable response index and *live* G1 pre-step callback bind the
        defender, source, actual G4 packet and one permitted damage event.
        """
        e=self.e
        if (not e.is_live_spontaneous(trigger,response)
                or response.kind!="opportunity"
                or response.actor_id!=attacker
                or trigger.actor_id!=target
                or trigger.target_id!=target
                or type(response_index) is not int
                or type(pending_index) is not int
                or response_index<self.start
                or pending_index<=response_index
                or pending_index>=len(e.ledger)):
            raise UnresolvedDecision("G4.5 requires exact live committed G0/G1 Opportunity")
        paid=e.ledger[response_index]
        pending=e.ledger[pending_index]
        if (paid["kind"]!="spontaneous_committed"
                or paid["round"]!=e.round
                or paid["detail"].get("actor")!=attacker
                or paid["detail"].get("response_kind")!="opportunity"
                or paid["detail"].get("label")!=response.label
                or paid["detail"].get("trigger")!=trigger.key
                or pending["kind"]!="g1_movement_opportunity_pending"
                or pending["detail"].get("trigger")!=trigger.key
                or pending["detail"].get("attacker")!=attacker
                or pending["detail"].get("mover")!=target
                or e.current!=target or e.pending_regeneration is not None
                or e.actors[attacker].hp<=0
                or e.actors[attacker].dead
                or e.actors[target].dead):
            raise UnresolvedDecision("Source response and moving target no longer match")
        if any(event["kind"] in ("g45_opportunity_attested_hit",
                               "g5_opportunity_resolved","g5_opportunity_cancelled")
               and event["detail"].get("response_index")==response_index
               for event in e.ledger):
            raise ValueError("G0 Opportunity source response already consumed")
        if (e.g1 is None or
                not e.g1.melee_contact(attacker,target)):
            raise UnresolvedDecision("Opportunity requires genuine pre-step G1 contact")
        # G4 enforces original source JSON, Armor, HP/Vigor, critical/wound,
        # poison/active-effect transition and exact wound-location preflight.
        e.g4.preflight_profile_hit(
            attacker,target,profile_id,die_face=die_face,
            critical=critical,critical_dice=critical_dice,
            vigor_die=vigor_die,wound_location_roll=wound_location_roll)
        result=e.g4.apply_profile_hit(
            attacker,target,profile_id,die_face=die_face,
            confirmed_hit=True,critical=critical,
            critical_dice=critical_dice,vigor_die=vigor_die,
            wound_location_roll=wound_location_roll)
        e.log("g45_opportunity_attested_hit",
              attacker=attacker,target=target,profile=profile_id,
              response_index=response_index,pending_index=pending_index,
              trigger=trigger.key,
              source_event=f"g45:opportunity:{e.seed}:{response_index}",
              attacker_source=e.actors[attacker].source.digest,
              target_source=e.actors[target].source.digest,
              no_turn_ap_payment=True,critical=critical,
              actual_result=result,target_state=_actor_state(e.actors[target]))
        e.check()
        return result

    def start_next_turn(self,choice=None,*,on_regeneration_ready=None,
                        on_regeneration_complete=None):
        """Only the actual next Initiative position; no synthesized steps."""
        if self.e.cursor>=len(self.e.order):
            raise ValueError("Begin the next real round first")
        actor_id=self.e.order[self.e.cursor]
        if choice is not None and not isinstance(choice,RegenerationChoice):
            raise ValueError("Actual source RegenerationChoice required")
        before=self.snapshot()
        first=len(self.e.ledger)
        self.e.start_turn(actor_id,regen_choice=choice,
                          on_regeneration_ready=on_regeneration_ready,
                          on_regeneration_complete=on_regeneration_complete)
        evidence=[x for x in self.e.ledger[first:]
                  if x["kind"] in ("regeneration_step","regeneration_dead")]
        if len(evidence)!=1:
            raise AssertionError("Exactly one native Step 2 required")
        self.e.log("g45_native_turn_started",actor=actor_id,
                   step2_index=evidence[0]["index"],
                   before=before["actors"][actor_id],
                   after=_actor_state(self.e.actors[actor_id]))
        self.e.check()
        return self.snapshot()

    def end_current_turn(self):
        if self.e.current is None or self.e.pending_regeneration is not None:
            raise ValueError("Resolve actual own turn before ending")
        ident=self.e.current
        self.e.end_turn()
        self.e.log("g45_native_turn_ended",actor=ident,
                   actor_state=_actor_state(self.e.actors[ident]))
        return self.snapshot()

    def begin_next_round(self):
        self.e.begin_round()
        return self.snapshot()

    def mark_unresolved(self,category,*,source_reference,detail):
        if category not in BLOCKERS:
            raise ValueError("Only explicitly classified missing authority")
        if not isinstance(source_reference,str) or not source_reference:
            raise ValueError("Missing source reference")
        if not isinstance(detail,str) or not detail:
            raise ValueError("Explain exact remaining decision")
        item={"status":"unresolved","category":category,
              "source_reference":source_reference,"detail":detail,
              "round":self.e.round,"ledger_at":len(self.e.ledger)}
        self.outcomes.append(item)
        self.e.log("g45_unresolved_stop",**item)
        # The caller may annotate its own copy, never the retained outcome.
        return deepcopy(item)

    def attest_withdrawal(self,actor_id,*,movement_event_index,
                          exit_policy_reference,independently_verified):
        """Record a legal exit, never infer escape from a low HP value."""
        if actor_id not in self.e.actors:
            raise ValueError("Unknown actor")
        # A genuine earlier G1 step does not authorize withdrawal after
        # the actor falls unconscious before the exit is attested.
        a=self.e.actors[actor_id]
        if a.hp<=0 or a.dead:
            raise ValueError("Dying/dead actor cannot withdraw")
        if independently_verified is not True or not isinstance(
                exit_policy_reference,str) or not exit_policy_reference:
            raise UnresolvedDecision("G5/G6 exit policy and confirmation required")
        if type(movement_event_index) is not int or not (
                self.start<=movement_event_index<len(self.e.ledger)):
            raise UnresolvedDecision("Actual in-scene G1 movement evidence required")
        ev=self.e.ledger[movement_event_index]
        facts=ev["detail"]
        # G1's prefix also covers MP reservation expiry, canceled steps,
        # segment breaks, pivots and pending responses. None establishes
        # a completed positional translation for a legal withdrawal.
        completed_step=(
            ev["kind"]=="g1_movement_step" and
            facts.get("step_kind") in ("orthogonal","diagonal") and
            facts.get("old")!=facts.get("new") and
            facts.get("old") is not None and facts.get("new") is not None)
        # Allied transit commits atomically and is signaled by its
        # final route-completion event, not an intermediate ally cell.
        # Require its complete contiguous source route, not an unrelated
        # previous transit step followed by an invented finish marker.
        count=facts.get("steps")
        route=(self.e.ledger[movement_event_index-count:movement_event_index]
               if type(count) is int and count>0
               and movement_event_index-count>=self.start else ())
        completed_transit=(
            ev["kind"]=="g1_allied_transit_finished" and
            len(route)==count and
            all(step["kind"]=="g1_allied_transit_step" and
                step["detail"].get("actor")==actor_id and
                step["detail"].get("old")!=step["detail"].get("new")
                for step in route) and
            all(route[i]["detail"].get("new")==route[i+1]["detail"].get("old")
                for i in range(len(route)-1)) and
            sum(step["detail"].get("cost",0) for step in route)==facts.get("cost"))
        if (facts.get("actor")!=actor_id or
                not (completed_step or completed_transit)):
            raise UnresolvedDecision(
                "Claimed withdrawal has no completed actor-linked G1 translation")
        item={"status":"withdrawal_attested","actor":actor_id,
              "movement_event_index":movement_event_index,
              "exit_policy_reference":exit_policy_reference,
              "round":self.e.round}
        self.outcomes.append(item)
        self.e.log("g45_withdrawal_attested",**item)
        return deepcopy(item)

    def report(self):
        """Detached audit snapshot; callers cannot rewrite G0/G4/G4.5 ledger.

        Copy the *whole* report: nested wound/hit result/target-state
        dictionaries, start state and retained explicit outcomes must all
        be independent of the authoritative encounter and this bridge.
        """
        events=self.e.ledger[self.start:]
        return deepcopy({"status":"bounded_continuation",
                "scene":self.e.scenario,"policy":self.e.policy,
                "source_actor_states":self.start_state,
                "current":self.snapshot(),
                "native_step2_count":sum(x["kind"] in
                    ("regeneration_step","regeneration_dead") for x in events),
                "g4_damage_events":[x["detail"]["event_key"] for x in events
                                    if x["kind"]=="g4_damage_applied"],
                "wound_creation_events":[x["detail"] for x in events
                                         if x["kind"]=="g4_wound_created"],
                "verified_hits":[x["detail"] for x in events
                                 if x["kind"]=="g45_attested_hit"],
                "explicit_outcomes":list(self.outcomes),
                "recorded_dead":[k for k,a in self.e.actors.items() if a.dead],
                "event_index_range":[self.start,len(self.e.ledger)-1],
                "complete_encounter_certified":False,
                "winner":None,"challenge_rating":None})


@lru_cache(maxsize=1)
def _cached_historical_phase3_wound_witnesses():
    """Re-identify EXACTLY 22 frozen Phase3 first stops, never re-adjudicate.

    Source trial only publishes first-stop outcomes, not complete G5
    contact/attack defense proofs or new player choices; each witness is
    individually reproducible but BLOCKED, not misreported as repaired/dead.
    """
    from scripts.b06_hunter_tactical_diversity_v0 import CASES, SEEDS, trial
    witnesses=[]
    for level,size,roster,opening,front in CASES:
        for seed in range(SEEDS):
            record=trial(level,size,roster,opening,front,seed)
            if record["terminal"]!="wound_unresolved":
                continue
            key=(level,size,roster,opening,front,seed)
            raw=json.dumps(record,sort_keys=True,separators=(",",":"),
                           allow_nan=False).encode("utf-8")
            witnesses.append({
                "witness_key":f"P3-W-L{level}-N{size}-{roster}-{opening}-{front}-S{seed:03d}",
                "source_tuple":key,"source_trial_sha256":sha256(raw).hexdigest(),
                "source_terminal":"wound_unresolved",
                "source_hunter_hp":record["hunter_hp"],
                "source_front_hp":record["front_hp"],
                "source_contact_route":record["contact_route"],
                "classification":"unresolved_G5_critical_confirmation_and_wound_location",
                "next_required_authority":[
                    "independent verified physical hit/contact/defense source",
                    "precommitted actual wound-location d20",
                    "explicit G5/G6 continuation reactions and policy",
                    "new real turns and source-selected recovery/retreat choices"],
                "g4_damage_replayed":False,
                "historical_census_mutated":False,
                "encounter_certified":False})
    if len(witnesses)!=22:
        raise AssertionError("Frozen Phase3 has changed: expected 22 first-stop witnesses")
    return tuple(witnesses)


def historical_phase3_wound_witnesses():
    """Return independent witness records; never expose mutable cached data.

    The 4,096 original trials are computed only on the first call. Both
    record dictionaries and nested authority lists are deep-copied on
    every public read, preserving source tuples and fixed evidence.
    """
    return deepcopy(_cached_historical_phase3_wound_witnesses())
