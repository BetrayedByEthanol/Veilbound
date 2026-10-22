"""B06 G7-A native end-to-end *bounded* terminal census v0.

Real G0–G6D actors, turns, AP, physical attacks, G2 Bow, G3 Flame,
G4 damage/wounds/Dying and G5/G6 Hunter Bite. The same keyed dice across
matched L2/L3 × P3/P4 warned-clear A-front runs, with predeclared
guard/dodge and HP-regeneration policies. No invented AI, area, Pounce,
escape, unverified critical Flame damage, CR, or statistical victory.
"""
from collections import Counter
from hashlib import sha256
import json

from scripts.b06_encounter_state_v0 import RegenerationChoice, UnresolvedDecision
from scripts.b06_g7_calibration_readiness_v0 import (
    ACTORS, LEVELS, PARTY_SIZES, canonical_digest, scenario_matrix, _ledger_measures,
)
from scripts.b06_hunter_mixed_party_g6c_v0 import mixed_scene
from scripts.b06_hunter_completion_g6d_v0 import HunterCompletion

MAX_ROUNDS = 3
ALLOWED = {(row["level"],row["party_size"]):row["scenario_id"]
           for row in scenario_matrix()
           if row["status"]=="fixed_native_window"}
OUTCOMES = (
    "hunter_defeat_attested",
    "party_defeat_observed",
    "legal_window_cutoff",
    "unresolved_mechanical_branch",
)
REASON_NO_FULL_CERT = (
    "fixed_three_round_ceiling_no_general_retreat_or_party_terminal_attestation",
    "no_ambush_pounce_or_alternative_frontline_and_protection",
    "scholar_flame_nat20_requires_native_G5_delivery",
)


def roll(seed,round_no,actor,action,kind,sides,slot=0):
    """Independent keyed dN. Keys exclude level and party size for pairing.

    Branches do not consume a mutable stream: an extra wound/confirmation
    die cannot re-roll a later actor's attack or favor a terminal outcome.
    """
    if (type(seed) is not int or seed<0 or
            type(round_no) is not int or round_no<1 or
            type(sides) is not int or sides<2 or
            type(slot) is not int or slot<0 or
            not all(type(x) is str and x for x in (actor,action,kind))):
        raise ValueError("Only explicit nonnegative keyed seed/draw policy")
    key=json.dumps(["B06-G7A-v0",seed,round_no,actor,action,kind,slot],
                   separators=(",",":"),ensure_ascii=True)
    return 1+int(sha256(key.encode()).hexdigest(),16)%sides


def _snapshot(e):
    return {ident:{
        "source_id":a.source.source_id,"source_digest":a.source.digest,
        "hp":a.hp,"hp_max":a.hp_max,"vigor":a.vigor,
        "vp_available":a.vp_available,"vp_committed":a.vp_committed,
        "ammunition":a.ammunition,"occupied":list(map(list,a.occupied)),
        "wounds":[{"id":w.ident,"severity":w.severity,
                   "progress":w.progress,"requirement":w.requirement}
                  for w in a.wounds],
        "dying":a.hp<=0 and not a.dead,"dead":a.dead
    } for ident,a in e.actors.items()}


def _regen_choice(e,ident,seed,round_no):
    a=e.actors[ident]
    if a.dead:
        return RegenerationChoice()
    if a.hp<=0:
        return RegenerationChoice(cancel_dying_loss=bool(
            a.vigor>0 and a.regen>0 and
            roll(seed,round_no,ident,"turn_start","survival_choice",2)==2))
    # Do not make up targeting for multi-wound repair. Natural HP recovery
    # is always an *explicit* unenhanced chosen allocation.
    use=roll(seed,round_no,ident,"turn_start","hp_regen_choice",2)==2
    hp=min(a.regen,a.vigor,max(0,a.hp_max-a.hp)) if use else 0
    return RegenerationChoice(hp=hp)


def _critical_faces(seed,round_no,attacker,action,face,bonus,
                    defense,defense_value):
    """Predeclare G5 native critical dice against the *paid* defense."""
    if face!=20:
        return None,()
    confirm=roll(seed,round_no,attacker,action,"confirmation",20)
    if defense=="take_hit":
        tier="devastating" if confirm==20 else "critical"
    elif confirm==20:
        tier="devastating"
    elif confirm!=1 and confirm+bonus>defense_value:
        tier="critical"
    else:
        tier="strong"
    count=1 if tier=="strong" else 2
    return confirm,tuple(roll(seed,round_no,attacker,action,"critical_d4",4,j)
                         for j in range(count))


def _melee(c,attacker,target,profile,defense,seed,round_no):
    e=c.e
    action=f"melee:{profile}"
    # One actual G0 sequence commits the target's defensive resource
    # before the attack face is examined; do not reroll on Guard outcome.
    seq=c.declare(attacker,target,profiles=(profile,),defenses=(defense,))
    face=roll(seed,round_no,attacker,action,"primary_d20",20)
    assigned=e.ledger[seq["defenses"][0]]["detail"]
    actual="take_hit" if e.actors[target].hp<=0 else defense
    value=None if actual=="take_hit" else assigned["defense_value"]
    bonus=c._profile(attacker,profile)
    confirmation,critical=_critical_faces(
        seed,round_no,attacker,action,face,bonus,actual,value)
    hit=face!=1 and (actual=="take_hit" or face==20 or face+bonus>value)
    dice={"attack_face":face,"confirmation_face":confirmation,
          "critical_dice":critical if hit else (),
          "wound_location_roll":roll(seed,round_no,attacker,action,"wound_d20",20)}
    if hit:
        dice["damage_face"]=roll(seed,round_no,attacker,action,"damage_d6",6)
        if profile=="B06-AT-04":
            dice["venom_resistance_die"]=roll(
                seed,round_no,target,action,"venom_resistance_d20",20)
    result=c.resolve(seq,0,**dice)
    if result["outcome"]!=("hit" if hit else "miss"):
        raise AssertionError("G5 resolved opposite of precommitted source defense")
    return result


def _bow(c,seed,round_no):
    e=c.e
    action="bow:one"
    face=roll(seed,round_no,"archer",action,"primary_d20",20)
    kw={"primary_face":face,
        "target_cell":e.g1.body_cell("hunter","head")}
    if face==20:
        confirm=roll(seed,round_no,"archer",action,"confirmation",20)
        kw["confirmation_face"]=confirm
        # Source R Bow bonus +4, same static G2 Take Hit range defense.
        lane=e.g2.lane("archer","hunter",target_cell=kw["target_cell"])
        _,value=e.g2._defense_value(
            e.actors["hunter"],"take_hit",lane.range_difficulty,0)
        tier=("devastating" if confirm==20 else "critical"
              if confirm!=1 and confirm+4>value else "strong")
        count=1 if tier=="strong" else 2
        kw["critical_dice"]=tuple(
            roll(seed,round_no,"archer",action,"critical_d4",4,j)
            for j in range(count))
    lane=e.g2.lane("archer","hunter",target_cell=kw["target_cell"])
    _,defense=e.g2._defense_value(e.actors["hunter"],"take_hit",
                                  lane.range_difficulty,0)
    hit=face!=1 and (face==20 or face+4>defense)
    if hit:
        kw["damage_face"]=roll(seed,round_no,"archer",action,"damage_d4",4)
        kw["wound_location_roll"]=roll(
            seed,round_no,"archer",action,"wound_d20",20)
    return HunterCompletion(c).bow_hit("archer","hunter",**kw)


def _flame(c,seed,round_no,*,resolve_critical=False):
    e=c.e
    action="flame:tier1"
    face=roll(seed,round_no,"scholar",action,"primary_d20",20)
    critical={}
    if resolve_critical and face==20:
        confirmation=roll(seed,round_no,"scholar",action,"confirmation",20)
        critical={"confirmation_face":confirmation,
                  "critical_dice":tuple(
                      roll(seed,round_no,"scholar",action,"critical_d4",4,j)
                      for j in range(2))}
    result=e.g3.cast_flame(
        "scholar","hunter",tier=1,face=face,
        vigor_die=roll(seed,round_no,"scholar",action,"vigor_d8",8),
        hand_available=True,
        target_cell=e.g1.body_cell("hunter","head"),
        wound_location_roll=roll(seed,round_no,"scholar",action,"wound_d20",20),
        **critical)
    if result["outcome"]=="critical_confirmation_pending_G5":
        raise UnresolvedDecision("g3_flame_natural20_delivery_not_native_G5")
    if result["outcome"] not in ("direct_hit_resolved_G4",
                                 "automatic_miss","ordinary_miss"):
        raise UnresolvedDecision("g3_flame_unresolved_delivery:"+result["outcome"])
    return result


def _validate_native_ledger(e):
    if any(ev["index"]!=i for i,ev in enumerate(e.ledger)):
        raise AssertionError("G0 event indices cannot be rewritten")
    turns=[ev["detail"]["actor"] for ev in e.ledger
           if ev["kind"]=="turn_end"]
    if turns!=list(e.order)*(len(turns)//len(e.order))+list(e.order)[:len(turns)%len(e.order)]:
        raise AssertionError("G0 turn sequence must follow native Initiative")
    ends=sum(ev["kind"]=="round_end" for ev in e.ledger)
    if ends!=len(turns)//len(e.order):
        raise AssertionError("Only truly completed G0 rounds may be counted")
    if e.current is None and e.cursor!=len(e.order) and len(turns)!=ends*len(e.order):
        raise AssertionError("Stopped G0 turn without an unresolved decision")
    return len(turns),ends


def run_trial(level,size,seed,*,max_rounds=MAX_ROUNDS,include_ledger=False,
              policy_mode="g7a",calibration_policy=None):
    if ((level,size) not in ALLOWED or type(level) is not int
            or type(size) is not int):
        raise ValueError("Only four G7 ready warned-clear A-front cells")
    if type(seed) is not int or seed<0:
        raise ValueError("Nonnegative integer seed required")
    if type(max_rounds) is not int or not 1<=max_rounds<=MAX_ROUNDS:
        raise ValueError("1–3 round native observation ceiling only")
    if type(include_ledger) is not bool:
        raise ValueError("Explicit include_ledger Boolean required")
    if policy_mode not in ("g7a","g7b_flame","g7b_archer_exit"):
        raise ValueError("Only preauthored G7-A/B policy modes are supported")
    cohort={"g7a":"warned_control","g7b_flame":"warned_flame",
            "g7b_archer_exit":"warned_archer_exit"}[policy_mode]
    if calibration_policy is not None and calibration_policy!=cohort:
        raise ValueError("G7-F cohort does not match native G7-A/B policy")
    combat=mixed_scene(
        level=level,size=size,seed=seed,
        archer_exit=policy_mode=="g7b_archer_exit")
    e=combat.e
    if calibration_policy is not None:
        e.log("g7f_policy_selected", cohort=cohort, runner="g7a",
              mode=policy_mode, scenario=e.scenario,
              level=level, party_size=size, seed=seed)
    before=_snapshot(e)
    unresolved=None
    archer_withdrew=False
    completed=0
    planned=ALLOWED[(level,size)]
    for round_no in range(1,max_rounds+1):
        if round_no>1:
            combat.bridge.begin_next_round()
        for actor in e.order:
            try:
                combat.bridge.start_next_turn(
                    _regen_choice(e,actor,seed,round_no))
                a=e.actors[actor]
                h=e.actors["hunter"]
                if (a.dead or a.hp<=0 or archer_withdrew or
                        h.dead and actor!="hunter"):
                    pass  # real turn remains started/ended, no phantom attack
                elif actor=="hunter":
                    v=e.actors["vanguard"]
                    if not v.dead:
                        # Dying is not dead, but G0 forbids active defenses
                        # before it accepts/pays the Hunter's declaration.
                        # Select the only legal static defense *before*
                        # the native pre-roll Guard/Dodge commitment.
                        if v.hp<=0:
                            defense="take_hit"
                        else:
                            choice=roll(seed,round_no,actor,"bite","defense_choice",2)
                            defense=("guard" if choice==2 and v.guard_remaining>0
                                     else "dodge")
                        _melee(combat,"hunter","vanguard","B06-AT-04",
                               defense,seed,round_no)
                elif actor in ("vanguard","guardian"):
                    profile=("B06-PC-A-SWORD" if actor=="vanguard"
                             else "B06-PC-B-MACE")
                    # Actual Hunter Dodge or static Take Hit; no natural
                    # Guard is fabricated for its non-shield anatomy.
                    pick=roll(seed,round_no,actor,"melee","hunter_defense_choice",2)
                    defense="dodge" if pick==2 and h.hp>0 else "take_hit"
                    _melee(combat,actor,"hunter",profile,defense,seed,round_no)
                elif actor=="archer":
                    retreat=(policy_mode=="g7b_archer_exit" and
                             roll(seed,round_no,"archer","route:west_border",
                                  "retreat_choice",2)==2)
                    if retreat:
                        # The G6-C archer is one legal westward step away
                        # from a *previously authored* scene exit. Decline
                        # no true Opportunity: reject if anyone threatens
                        # the step instead of suppressing its attack.
                        dest,_,_,allies=e.g1.preview("archer",delta=(-1,0))
                        if allies or e.g1._threats("archer",dest,False):
                            raise UnresolvedDecision(
                                "G7B archer border path needs genuine Opportunity resolver")
                        if not e.g1.step("archer",(-1,0),responses=()):
                            raise UnresolvedDecision("G7B archer border step interrupted")
                        combat.withdraw("archer")
                        archer_withdrew=True
                    else:
                        _bow(combat,seed,round_no)
                elif actor=="scholar":
                    _flame(combat,seed,round_no,
                           resolve_critical=policy_mode!="g7a")
                else:
                    raise AssertionError("G7-A does not invent fifth PC")
                combat.bridge.end_current_turn()
            except UnresolvedDecision as exc:
                unresolved={"actor":actor,"round":round_no,
                            "reason":str(exc)}
                break
        if unresolved is not None:
            break
        if e.current is not None or e.cursor!=len(e.order):
            raise AssertionError("No fictitious Round End in completed G7-A round")
        completed+=1
        if (archer_withdrew or e.actors["hunter"].dead or all(
                e.actors[x].dead for x in e.order if x!="hunter")):
            break
    # No encounter success can be inferred merely from a hit, Dying,
    # missing legal continuation, or a finite observation ceiling.
    if unresolved is not None:
        status="unresolved_mechanical_branch"
        terminal=None
    elif archer_withdrew:
        # A *single* archer's genuine G1 -> G4.5 -> G5 exit, never
        # automatically a whole-party withdrawal or Hunter loss.
        exits=[v for v in e.ledger if v["kind"]=="g5_terminal_exit"
               and v["detail"].get("actor")=="archer"]
        signed=[v for v in e.ledger if v["kind"]=="g45_withdrawal_attested"
                and v["detail"].get("actor")=="archer"]
        if (len(exits)!=1 or len(signed)!=1
                or exits[0]["detail"]["movement_index"]!=
                   signed[0]["detail"]["movement_event_index"]):
            raise AssertionError("G7-B archer exit lacks same native G1 movement")
        status="archer_withdrawal_attested"
        terminal={"ending":status,"actor":"archer",
                  "g5_exit_event":exits[0]["index"],
                  "g45_withdrawal_event":signed[0]["index"],
                  "not_whole_party_withdrawal":True}
    elif e.actors["hunter"].dead:
        try:
            terminal=HunterCompletion(combat).attest_hunter_defeat(
                "hunter",party_ids=tuple(x for x in e.order if x!="hunter"))
            status="hunter_defeat_attested"
        except UnresolvedDecision as exc:
            status="unresolved_mechanical_branch"
            unresolved={"actor":"hunter","round":e.round,
                        "reason":"death_terminal_authority:"+str(exc)}
            terminal=None
    elif all(e.actors[x].dead for x in e.order if x!="hunter"):
        # No mixed-party party-wipe certification API exists; distinguish
        # native death facts from any presumed full encounter outcome.
        status="party_defeat_observed"
        terminal=None
    else:
        status="legal_window_cutoff"
        terminal=None
    turns,round_ends=_validate_native_ledger(e)
    if status!="unresolved_mechanical_branch" and (
            e.current is not None or round_ends!=completed):
        raise AssertionError("Non-unresolved outcomes require genuine full turns")
    counts=_ledger_measures(e.ledger)
    if (status=="hunter_defeat_attested")!=bool(counts["g6d_defeat_terminals"]):
        raise AssertionError("G7-A must not mint a terminal without G6-D proof")
    if counts["g2_arrows_launched"]!=counts["g6d_attested_bow"]:
        raise AssertionError("Every G7-A launched Bow shot needs exact G6-D receipt")
    native_digest=canonical_digest(e.ledger)
    summary={
        "scenario_id":planned,"level":level,"party_size":size,"seed":seed,
        "policy_id":("G7A-keyed-guard-dodge-regen-clear-A-front-v0"
                     if policy_mode=="g7a" else
                     "G7B-keyed-"+policy_mode+"-clear-A-front-v0"),
        "opening":"warned_clear","frontline":"A_head_forward",
        "outcome":status,"native_terminal":terminal,
        "unresolved":unresolved,
        "round_limit":max_rounds,"rounds_completed":round_ends,
        "turns_completed":turns,
        "initial_state":before,"final_state":_snapshot(e),
        "measures":counts,"ledger_sha256":native_digest,
        "sample_is_complete_encounter":status=="hunter_defeat_attested",
        "one_party_member_exit_only":status=="archer_withdrawal_attested",
        "complete_party_pack_certified":False,"hunter_cr":None,
    }
    if include_ledger:
        summary["ledger"]=e.ledger
    return summary


def census(seeds=8,*,start_seed=0,max_rounds=MAX_ROUNDS,
           include_trials=True):
    if (type(seeds) is not int or not 1<=seeds<=128
            or type(start_seed) is not int or start_seed<0
            or type(max_rounds) is not int or not 1<=max_rounds<=MAX_ROUNDS
            or type(include_trials) is not bool):
        raise ValueError("G7-A bounded census requires 1–128 ordered seeds")
    cases=[]
    for level in LEVELS:
        for size in PARTY_SIZES:
            trials=[run_trial(level,size,start_seed+i,
                              max_rounds=max_rounds) for i in range(seeds)]
            tally=Counter(t["outcome"] for t in trials)
            if sum(tally.values())!=seeds or set(tally)-set(OUTCOMES):
                raise AssertionError("Census must account for every selected seed")
            cases.append({
                "scenario_id":ALLOWED[(level,size)],
                "level":level,"party_size":size,
                "seed_start":start_seed,"seed_count":seeds,
                "counts":{status:tally[status] for status in OUTCOMES},
                "censored_or_unresolved":(
                    tally["legal_window_cutoff"]+tally["unresolved_mechanical_branch"]),
                "unresolved_reasons":dict(sorted(Counter(
                    t["unresolved"]["reason"] for t in trials
                    if t["unresolved"] is not None).items())),
                "complete_hunter_defeat_terminal_count":tally["hunter_defeat_attested"],
                "complete_encounter_outcome_rate":None,
                "confidence_interval":None,"hunter_cr":None,
                "trial_digests":[{"seed":t["seed"],"ledger_sha256":t["ledger_sha256"],
                                  "outcome":t["outcome"]}
                                 for t in trials],
                **({"trials":trials} if include_trials else {}),
            })
    return {"version":"B06-G7A-bounded-native-terminal-census-v0",
            "evidence_grade":"native_observation_censored_not_CR_calibration",
            "max_rounds":max_rounds,
            "pairing":"SHA256 keyed by seed/round/actor/action/die; level and party size excluded",
            "no_seed_rerolls_after_terminal":True,
            "historical_phase3_not_recomputed":True,
            "historical_phase3_sha256":
                "c02c9830d10f1bcaf7d80ccedfe81102c1d4d9b28f4f004e9f715560b184ca5b",
            "no_numeric_cr":True,
            "missing_certification_gates":list(REASON_NO_FULL_CERT),
            "cases":cases}


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds",type=int,default=8)
    parser.add_argument("--start-seed",type=int,default=0)
    parser.add_argument("--rounds",type=int,default=MAX_ROUNDS)
    parser.add_argument("--full-trials",action="store_true")
    args=parser.parse_args(argv)
    result=census(args.seeds,start_seed=args.start_seed,
                  max_rounds=args.rounds,include_trials=args.full_trials)
    print(json.dumps({"census_sha256":canonical_digest(result),**result},
                     sort_keys=True,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
