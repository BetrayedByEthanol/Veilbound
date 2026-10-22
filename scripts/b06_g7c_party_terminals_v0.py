"""B06 G7-C: native whole-party terminals for authored Hunter scenes.

Independent G1/G4.5/G5 exits and verified G4/G4.5/G5 lethal Hunter
attack provenance are necessary; living/0-HP actors, an isolated
withdrawal or a three-round cutoff never certify a party defeat/escape.
"""
from collections import Counter
import json

from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_g7a_native_terminal_census_v0 import (
    ALLOWED, _regen_choice, _melee, _snapshot, _validate_native_ledger,
    roll, canonical_digest,
)
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene

EXIT_ROUTES={
    "vanguard":((-1,0),(-1,0)),
    "guardian":((0,1),(0,1),(0,1)),
    "archer":((-1,0),),
    "scholar":((-1,0),),
}
OUTCOMES=("party_withdrawal_attested","party_defeat_attested",
          "legal_window_cutoff","unresolved_mechanical_branch")
HISTORICAL_SHA="c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b"


class PartyTerminal:
    """One terminal receipt for all original A/B/R[/F] participants."""

    def __init__(self,combat):
        self.combat=combat
        self.e=combat.e
        self.party=tuple(actor for actor in self.e.order if actor!="hunter")
        if (len(self.party) not in (3,4)
                or self.e.order!=("hunter",*self.party)
                or set(self.e.actors)!={"hunter",*self.party}
                or self.e.actors["hunter"].source.source_id!="B06-EN-03"
                or {self.e.actors[p].source.source_id for p in self.party}!=
                   ({"A","B","R"} if len(self.party)==3
                    else {"A","B","R","F"})
                or self.e.g5 is not combat):
            raise UnresolvedDecision("G7-C needs the exact native G6-C Hunter pack")

    def _boundary(self):
        e=self.e
        if (e.current is not None or e.cursor!=len(e.order)
                or not any(x["kind"]=="round_end" for x in e.ledger)
                or self.combat.pending_attack_slots()):
            raise UnresolvedDecision("Full party terminal requires complete G0 round and no paid slots")
        if (e.actors["hunter"].dead or
                any(x["kind"] in (
                    "g6d_hunter_defeat_attested",
                    "g7c_party_defeat_attested",
                    "g7c_party_withdrawal_attested")
                    for x in e.ledger)):
            raise UnresolvedDecision("Conflicting or already certified encounter terminal")

    def attest_withdrawal(self):
        self._boundary()
        e=self.e
        policies=self.combat.scene_exits
        if (len(policies)!=len(self.party)
                or {x.actor_id for x in policies}!=set(self.party)):
            raise UnresolvedDecision("Every member needs an immutable authored exit")
        receipts=[]
        all_exits=[x for x in e.ledger if x["kind"]=="g5_terminal_exit"]
        all_g45=[x for x in e.ledger if x["kind"]=="g45_withdrawal_attested"]
        if len(all_exits)!=len(self.party) or len(all_g45)!=len(self.party):
            raise UnresolvedDecision("Exactly one authenticated G5/G4.5 exit per party member")
        for policy in policies:
            actor=policy.actor_id
            a=e.actors[actor]
            if a.dead or a.hp<=0 or a.occupied!=(policy.square,):
                raise UnresolvedDecision("Dying, dead or non-exited party actor cannot withdraw")
            x=[v for v in all_exits if v["detail"].get("actor")==actor]
            y=[v for v in all_g45 if v["detail"].get("actor")==actor]
            authors=[v for v in e.ledger if v["kind"]=="g5_scene_exit_authored"
                     and v["detail"].get("actor")==actor]
            if len(x)!=1 or len(y)!=1 or len(authors)!=1:
                raise UnresolvedDecision("Duplicate/missing source-authored actor exit")
            x,y,auth=x[0],y[0],authors[0]
            step=x["detail"].get("movement_index")
            if (auth["index"]>=step or
                    auth["detail"].get("policy")!=policy.policy_id
                    or auth["detail"].get("square")!=list(policy.square)
                    or x["detail"].get("policy")!=policy.policy_id
                    or x["detail"].get("at")!=list(policy.square)
                    or y["detail"].get("exit_policy_reference")!=policy.policy_id
                    or y["detail"].get("movement_event_index")!=step
                    or y["index"]>=x["index"]
                    or type(step) is not int or not 0<=step<y["index"]):
                raise UnresolvedDecision("Source policy and G1/G4.5/G5 receipt mismatch")
            move=e.ledger[step]
            if (move["kind"]!="g1_movement_step"
                    or move["detail"].get("actor")!=actor
                    or move["detail"].get("step_kind") not in ("orthogonal","diagonal")
                    or move["detail"].get("new")!=[list(policy.square)]
                    or move["detail"].get("old")==move["detail"].get("new")
                    or move["turn"]!=actor or x["round"]!=move["round"]):
                raise UnresolvedDecision("No native final paid G1 exit translation")
            if any(v["index"]>x["index"] and (
                    v["kind"]=="g4_damage_applied"
                    and v["detail"].get("recipient")==actor
                    or v["kind"]=="action_committed"
                    and v["detail"].get("actor")==actor)
                   for v in e.ledger):
                raise UnresolvedDecision("Exited actor resumed combat or was harmed")
            receipts.append({"actor":actor,"policy":policy.policy_id,
                             "movement":step,"g45":y["index"],"g5":x["index"]})
        # Authenticated exits and genuine final Round End must precede
        # the unique party-wide terminal. No inferred escape via positions.
        e.log("g7c_party_withdrawal_attested",party=self.party,
              member_exits=receipts,round=e.round,hunter_cr=None)
        return {"ending":"party_withdrawal_attested",
                "terminal_event":len(e.ledger)-1,
                "member_exits":receipts,"hunter_cr":None,
                "complete_party_pack_certified":False}

    def attest_defeat(self):
        """All truly dead PCs, each from a paid native Hunter Bite.

        The bounded G7-C exit policy does not manufacture these deaths,
        but the independent terminal API rejects fake or merely Dying
        observations until a real multi-target Hunter policy can prove them.
        """
        self._boundary()
        e=self.e
        if any(x["kind"]=="g5_terminal_exit" for x in e.ledger):
            raise UnresolvedDecision("No party wipe when any party member escaped")
        lethal_indices=[]
        for member in self.party:
            a=e.actors[member]
            if not a.dead or a.hp!=-a.hp_max:
                raise UnresolvedDecision("All PCs must be actually dead, not Dying")
            deaths=[x for x in e.ledger if x["kind"]=="g4_damage_applied"
                    and x["detail"].get("recipient")==member
                    and x["detail"].get("dead") is True]
            if len(deaths)!=1:
                raise UnresolvedDecision("Every party death needs unique source G4 evidence")
            lethal=deaths[0]
            if lethal["detail"].get("cause")!="source-profile:B06-AT-04":
                raise UnresolvedDecision("G7-C defeat requires native Hunter Bite provenance")
            bridge=[v for v in e.ledger if v["kind"]=="g45_attested_hit"
                    and v["detail"].get("attacker")=="hunter"
                    and v["detail"].get("target")==member
                    and v["detail"].get("profile")=="B06-AT-04"
                    and (v["detail"].get("actual_result") or {}).get("dead") is True
                    and v["index"]>lethal["index"]]
            resolved=[v for v in e.ledger if v["kind"]=="g5_melee_resolved"
                      and v["detail"].get("attacker")=="hunter"
                      and v["detail"].get("target")==member
                      and v["detail"].get("profile")=="B06-AT-04"
                      and (v["detail"].get("damage") or {}).get("dead") is True]
            proven=any(
                b["detail"].get("action_index")==r["detail"].get("action_index")
                and lethal["index"]<b["index"]<r["index"]
                and b["round"]==r["round"]==lethal["round"]
                and b["turn"]==r["turn"]==lethal["turn"]=="hunter"
                and any(roll_event["kind"]=="g5_melee_roll"
                        and roll_event["detail"].get("action_index")==
                            r["detail"].get("action_index")
                        and roll_event["detail"].get("hit") is True
                        and roll_event["index"]<lethal["index"]
                        and roll_event["round"]==lethal["round"]
                        for roll_event in e.ledger)
                for b in bridge for r in resolved)
            if not proven:
                raise UnresolvedDecision("Lethal Bite not bound to paid native G5 action")
            lethal_indices.append(lethal["index"])
        e.log("g7c_party_defeat_attested",party=self.party,
              lethal_damage_indices=lethal_indices,round=e.round,
              hunter_cr=None)
        return {"ending":"party_defeat_attested","terminal_event":len(e.ledger)-1,
                "lethal_damage_indices":lethal_indices,
                "hunter_cr":None,"complete_party_pack_certified":False}


def run_trial(level,size,seed,*,include_ledger=False):
    """One genuinely completed round of optional, cautious, sourced exits."""
    if (type(level) is not int or type(size) is not int
            or (level,size) not in ALLOWED
            or type(seed) is not int or seed<0
            or type(include_ledger) is not bool):
        raise ValueError("G7-C accepts four sourced scenes and nonnegative keyed seeds")
    combat=mixed_scene(level=level,size=size,seed=seed,party_exits=True)
    e=combat.e
    start=_snapshot(e)
    exited=[]
    unresolved=None
    for actor in e.order:
        try:
            combat.bridge.start_next_turn(_regen_choice(e,actor,seed,1))
            a=e.actors[actor]
            if actor=="hunter":
                victim=e.actors["vanguard"]
                if not victim.dead:
                    defense=("take_hit" if victim.hp<=0 else
                             "guard" if roll(seed,1,"hunter","bite",
                                "defense_choice",2)==2
                             and victim.guard_remaining>0 else "dodge")
                    _melee(combat,"hunter","vanguard","B06-AT-04",
                           defense,seed,1)
            elif a.hp>0 and not a.dead:
                for delta in EXIT_ROUTES[actor]:
                    # With Cautious translation, this explicit v0 policy
                    # suppresses a *genuine* opportunity at its MP cost,
                    # not by fabricating an enemy declination.
                    dest,cost,kind,allies=e.g1.preview(
                        actor,delta=delta,cautious=True)
                    if allies or e.g1._threats(actor,dest,True):
                        raise UnresolvedDecision("G7-C route not self-contained")
                    if not e.g1.step(actor,delta,cautious=True,responses=()):
                        raise UnresolvedDecision("G7-C movement cancelled")
                combat.withdraw(actor)
                exited.append(actor)
            combat.bridge.end_current_turn()
        except UnresolvedDecision as exc:
            unresolved={"actor":actor,"round":1,"reason":str(exc)}
            break
    if unresolved:
        outcome="unresolved_mechanical_branch"
        terminal=None
    elif len(exited)==size:
        try:
            terminal=PartyTerminal(combat).attest_withdrawal()
            outcome="party_withdrawal_attested"
        except UnresolvedDecision as exc:
            unresolved={"actor":"party","round":1,"reason":str(exc)}
            terminal=None
            outcome="unresolved_mechanical_branch"
    else:
        # One or more source PCs may genuinely be Dying/dead. This does
        # not license a defeat label while other PCs have exited.
        outcome="legal_window_cutoff"
        terminal=None
    if outcome!="unresolved_mechanical_branch":
        turns,ends=_validate_native_ledger(e)
        if ends!=1 or turns!=len(e.order):
            raise AssertionError("G7-C cannot certify unfinished native round")
    else:
        turns,ends=(sum(v["kind"]=="turn_end" for v in e.ledger),
                    sum(v["kind"]=="round_end" for v in e.ledger))
    if (outcome=="party_withdrawal_attested")!=any(
            v["kind"]=="g7c_party_withdrawal_attested" for v in e.ledger):
        raise AssertionError("No terminal without all independent exits")
    answer={"version":"B06-G7C-authored-whole-party-exit-v0",
            "scenario_id":ALLOWED[(level,size)],"level":level,
            "party_size":size,"seed":seed,"opening":"warned_clear",
            "frontline":"A_head_forward",
            "policy_id":"G7C:all-party-cautious-border-exits-v0",
            "outcome":outcome,"native_terminal":terminal,
            "exited":exited,"unexited":[p for p in e.order if p!="hunter"
                                      and p not in exited],
            "unresolved":unresolved,"rounds_completed":ends,
            "turns_completed":turns,"initial_state":start,
            "final_state":_snapshot(e),"ledger_sha256":canonical_digest(e.ledger),
            "complete_party_pack_certified":False,"hunter_cr":None}
    if include_ledger:
        answer["ledger"]=e.ledger
    return answer


def census(seeds=8,*,start_seed=0,include_trials=False):
    if (type(seeds) is not int or not 1<=seeds<=128
            or type(start_seed) is not int or start_seed<0
            or type(include_trials) is not bool):
        raise ValueError("1-128 G7-C paired seeds required")
    cases=[]
    for level,size in sorted(ALLOWED):
        runs=[run_trial(level,size,start_seed+n) for n in range(seeds)]
        counts=Counter(x["outcome"] for x in runs)
        if sum(counts.values())!=seeds or set(counts)-set(OUTCOMES):
            raise AssertionError("G7-C requires exact trial denominator")
        reasons=Counter(x["unresolved"]["reason"] for x in runs
                        if x["unresolved"])
        cases.append({"level":level,"party_size":size,
                      "scenario_id":ALLOWED[(level,size)],
                      "seed_start":start_seed,"seed_count":seeds,
                      "counts":{v:counts[v] for v in OUTCOMES},
                      "terminal_complete_party_exits":counts["party_withdrawal_attested"],
                      "native_party_defeats":counts["party_defeat_attested"],
                      "unresolved_reasons":dict(sorted(reasons.items())),
                      "win_rate":None,"confidence_interval":None,"hunter_cr":None,
                      "trial_digests":[{"seed":r["seed"],"outcome":r["outcome"],
                                        "ledger_sha256":r["ledger_sha256"]}
                                       for r in runs],
                      **({"trials":runs} if include_trials else {})})
    return {"version":"B06-G7C-full-party-terminals-v0",
            "evidence_grade":"authored_full_exit_terminal_pilot_not_CR",
            "policy":"G7C:all-party-cautious-border-exits-v0",
            "historical_phase3_not_recomputed":True,
            "historical_phase3_sha256":HISTORICAL_SHA,
            "complete_party_pack_certified":False,
            "hunter_cr":None,
            "remaining_gates":[
                "native_multitarget_Hunter_Bite_party_wipe_witness",
                "reactive_prepared_intervene_in_mixed_party",
                "alternate_frontline_ambush_pounce",
                "long_toxin_and_recovery",
                "representative_human_GM_policy_calibration"],
            "cases":cases}


def main(argv=None):
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seeds",type=int,default=8)
    p.add_argument("--start-seed",type=int,default=0)
    p.add_argument("--full-trials",action="store_true")
    args=p.parse_args(argv)
    r=census(args.seeds,start_seed=args.start_seed,include_trials=args.full_trials)
    print(json.dumps({"census_sha256":canonical_digest(r),**r},
                     sort_keys=True,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
