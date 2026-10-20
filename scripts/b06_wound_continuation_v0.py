"""B06 G4.5: source-attested wound continuation, not a G5 encounter verdict.

This bridge *observes* native G0/G4 steps. It never invents contact,
critical confirmation, cure, withdrawal geometry or a new Regeneration Step.
"""
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
        self.source_events=set()
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

    def verified_profile_hit(self,attacker,target,profile_id,*,action_index,
                             source_event,contact_reference,defense_reference,
                             contact_verified,defense_verified,
                             die_face,critical="normal",critical_dice=(),
                             vigor_die=None,wound_location_roll=None):
        """Consume a *real* G0 Physical Action and an external G5 attestation.

        The caller, NOT G4.5, must have resolved contact, defense and critical
        tier. These refs document that independent decision, not fabricate it.
        """
        if any(type(x) is not str or not x for x in
               (source_event,contact_reference,defense_reference)):
            raise UnresolvedDecision("Stable G5 contact/defense source refs required")
        if contact_verified is not True or defense_verified is not True:
            raise UnresolvedDecision("G5 confirmed contact and defense required")
        if source_event in self.source_events:
            raise ValueError("Source event already consumed")
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
        # The AP reservation cannot be resurrected on a later Physical
        # Action in this same turn or after another independently resolved
        # profile hit. Defense/Interception logs between commitment and
        # final resolution remain permitted.
        if any(x["kind"] in ("action_committed","g4_profile_hit",
                            "turn_end","round_begin")
               for x in self.e.ledger[action_index+1:]):
            raise UnresolvedDecision("Physical hit must consume its current live action")
        # G0 supplied the AP cost; G4 supplies source JSON attack packets,
        # mitigation, exact one-event wound and native effects.
        result=self.d.apply_profile_hit(
            attacker,target,profile_id,die_face=die_face,
            confirmed_hit=True,critical=critical,
            critical_dice=critical_dice,vigor_die=vigor_die,
            wound_location_roll=wound_location_roll)
        self.source_events.add(source_event)
        self.seen_actions.add(action_index)
        self.e.log("g45_attested_hit",source_event=source_event,
                   attacker=attacker,target=target,profile=profile_id,
                   action_index=action_index,
                   contact_reference=contact_reference,
                   defense_reference=defense_reference,
                   attacker_source=self.e.actors[attacker].source.digest,
                   target_source=self.e.actors[target].source.digest,
                   critical=critical,actual_result=result,
                   target_state=_actor_state(self.e.actors[target]))
        self.e.check()
        return result

    def start_next_turn(self,choice=None):
        """Only the actual next Initiative position; no synthesized steps."""
        if self.e.cursor>=len(self.e.order):
            raise ValueError("Begin the next real round first")
        actor_id=self.e.order[self.e.cursor]
        if choice is not None and not isinstance(choice,RegenerationChoice):
            raise ValueError("Actual source RegenerationChoice required")
        before=self.snapshot()
        first=len(self.e.ledger)
        self.e.start_turn(actor_id,regen_choice=choice)
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
        return item

    def attest_withdrawal(self,actor_id,*,movement_event_index,
                          exit_policy_reference,independently_verified):
        """Record a legal exit, never infer escape from a low HP value."""
        if actor_id not in self.e.actors:
            raise ValueError("Unknown actor")
        if self.e.actors[actor_id].dead:
            raise ValueError("Dead actor cannot withdraw")
        if independently_verified is not True or not isinstance(
                exit_policy_reference,str) or not exit_policy_reference:
            raise UnresolvedDecision("G5/G6 exit policy and confirmation required")
        if type(movement_event_index) is not int or not (
                self.start<=movement_event_index<len(self.e.ledger)):
            raise UnresolvedDecision("Actual in-scene G1 movement evidence required")
        ev=self.e.ledger[movement_event_index]
        if not ev["kind"].startswith("g1_") or ev["detail"].get("actor")!=actor_id:
            raise UnresolvedDecision("Claimed withdrawal has no actor-linked G1 movement evidence")
        item={"status":"withdrawal_attested","actor":actor_id,
              "movement_event_index":movement_event_index,
              "exit_policy_reference":exit_policy_reference,
              "round":self.e.round}
        self.outcomes.append(item)
        self.e.log("g45_withdrawal_attested",**item)
        return item

    def report(self):
        """Audit evidence, not an automatically claimed winner or CR."""
        events=self.e.ledger[self.start:]
        return {"status":"bounded_continuation",
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
                "winner":None,"challenge_rating":None}


@lru_cache(maxsize=1)
def historical_phase3_wound_witnesses():
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
