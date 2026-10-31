"""B05/B06: preserve native G4.2/G4.3/G4.4 hazard identities between scenes.

Called only from the source-attested G8 live-instance handoff. All state comes
from native G4, never caller-provided JSON or a fabricated exposure.
"""
from copy import deepcopy
from dataclasses import asdict
from scripts.b06_encounter_state_v0 import UnresolvedDecision
from scripts.b06_mundane_toxins_v0 import PROFILES
from scripts.b06_hunter_venom_endurance_v0 import HUNTER

PARTY = ("vanguard", "guardian", "archer", "scholar")
CLOCK_TAGS = ("mundane:", "hunter:", "endurance:")


def effect_state(e):
    """Stable receipts including active and historical unique hazard keys."""
    d = e.g4
    return {
        "short_toxins": deepcopy([t for t in d.short_toxins
                                  if t["recipient"] in PARTY]),
        "unified_instances": deepcopy({
            k:v for k,v in d.toxins.instances.items() if k in PARTY}),
        "exposure_ids": sorted(d.toxins.exposure_ids),
        "hunter_keys": sorted(d.venom.hunter_keys),
        "endurance_effects": deepcopy({
            k:v for k,v in d.venom.effects.items()
            if v["caster"] in PARTY or v["recipient"] in PARTY}),
        "endurance_serial": d.venom.next_effect,
        "damage_toxin_events": sorted(k for k in d.used_events
                                      if k.startswith("toxin:")),
        "modifiers": {n:deepcopy(getattr(e.actors[n],"toxin_modifiers",{}))
                      for n in PARTY},
        "clock_events": {
            k:asdict(ev) for k,ev in d.clock.events.items()
            if ev.actor_id in PARTY},
        "recovery_serial": {
            n:d.clock.recovery_serial[n] for n in PARTY},
        "world_seconds": d.clock.world_seconds,
    }


def _active_marker(e, actor, ident, source):
    ev=e.g4.clock.events.get(ident)
    if (ev is None or ev.actor_id!=actor or ev.source != source
            or ev.kind!="milestone" or ev.consumed or ev.canceled
            or ev.due_seconds is None or ev.due_round is not None):
        raise UnresolvedDecision("Active toxin/Endurance marker lost its G4.2 deadline")


def validate_source(e):
    """Read-only validation for party hazards before committing any travel."""
    d=e.g4
    for n in PARTY:
        a=e.actors[n]
        if a.dead or a.hp<=0:
            raise UnresolvedDecision("Ongoing hazard needs a live party recipient")
        legacy=[t for t in d.short_toxins if t["recipient"]==n and t["left"]>0]
        if len(legacy)>1:
            raise UnresolvedDecision("More than one legacy toxin on one recipient")
        for t in legacy:
            if (t["key"] not in d.toxins.exposure_ids
                    and not any(ev["kind"]=="g4_toxin_scheduled"
                                and ev["detail"].get("key")==t["key"]
                                for ev in e.ledger)):
                raise UnresolvedDecision("Legacy toxin has no native source")
            if (type(t["phase"]) is not int or not 0<=t["phase"]<6
                    or type(t["applied"]) is not int or t["applied"]<0):
                raise UnresolvedDecision("Invalid legacy toxin interval")
        toxin=d.toxins.active(n)
        if toxin:
            if legacy or toxin["key"] not in d.toxins.exposure_ids:
                raise UnresolvedDecision("Inconsistent unified toxin identity/one-instance slot")
            profile=toxin["profile"]
            if profile not in PROFILES and profile!=HUNTER:
                raise UnresolvedDecision("Unrecognized toxin profile cannot be migrated")
            if profile==HUNTER:
                if (toxin["clock"]!="hunter" or toxin.get("stage") not in (0,1,2)
                        or toxin["key"] not in d.venom.hunter_keys):
                    raise UnresolvedDecision("Unproven Hunter stage/exposure")
                for ident in toxin["markers"]:
                    ev=d.clock.events.get(ident)
                    if ev is None or ev.actor_id!=n or ev.source!=toxin["source_tag"]:
                        raise UnresolvedDecision("Hunter onset/escalation/expiry source mismatch")
            else:
                if (toxin["clock"] not in ("short","long")
                        or toxin["grade"]!=PROFILES[profile][0]):
                    raise UnresolvedDecision("Corrupt mundane toxin profile")
                if toxin["clock"]=="short" and not (
                        type(toxin["phase"]) is int and 0<=toxin["phase"]<6):
                    raise UnresolvedDecision("Corrupt short-toxin local interval")
                marker=toxin.get("marker")
                if marker:
                    _active_marker(e,n,marker,toxin["source_tag"])
                elif profile in ("TX-NP","TX-EN","TX-HE"):
                    # TX-HE may end via the native Recovery before its expiry.
                    raise UnresolvedDecision("Scheduled long toxin missing pending event")
                if profile=="TX-HE":
                    if not toxin.get("recovery_id"):
                        raise UnresolvedDecision("Hepatotoxin missing original recovery identity")
        # Recorded modifier must match the CURRENT native source interpreter;
        # do not normalize a tampered value during import.
        expected={}
        if toxin:
            if profile==HUNTER:
                expected=d.venom.hunter_penalties(toxin)
            else:
                from scripts.b06_mundane_toxins_v0 import PENALTIES
                expected=dict(PENALTIES.get(profile,{}))
            if d.venom.covering(toxin):
                expected={}
        if getattr(a,"toxin_modifiers",{})!=expected:
            raise UnresolvedDecision("Native toxin penalties disagree with actor")
    for ident,v in d.venom.effects.items():
        if not v["active"]:
            continue
        if (v["id"]!=ident or v["caster"] not in PARTY
                or v["recipient"] not in PARTY or
                v["mode"] not in ("ward","suppression")
                or v["cost"] not in (1,2,3)
                or type(v["units"]) is not int or not 0<=v["units"]<=5
                or type(v["phase"]) is not int or not 0<=v["phase"]<6):
            raise UnresolvedDecision("Cannot carry nonparty or invalid Endurance")
        _active_marker(e,v["recipient"],v["expiry"],v["source"])
        if v["bound_key"]:
            t=d.toxins.active(v["recipient"])
            legacy=next((t for t in d.short_toxins
                         if t["recipient"]==v["recipient"] and t["left"]>0),None)
            actual=legacy if v["bound_legacy"] else t
            if actual is None or actual["key"]!=v["bound_key"]:
                raise UnresolvedDecision("Endurance suppression target was lost")
    for ev in d.clock._pending():
        if ev.actor_id in PARTY and ev.kind=="milestone":
            if not ev.source.startswith(CLOCK_TAGS):
                raise UnresolvedDecision("Unsupported live non-toxin milestone")
            if ev.source.startswith("endurance:") and not any(
                    v["active"] and v["expiry"]==ev.ident
                    and v["source"]==ev.source
                    for v in d.venom.effects.values()):
                raise UnresolvedDecision("Unowned Endurance expiry marker")
            if ev.source.startswith("hunter:") and not any(
                    t["active"] and t["profile"]==HUNTER
                    and ev.ident in t["markers"] and t["source_tag"]==ev.source
                    for t in d.toxins.instances.values()):
                raise UnresolvedDecision("Unowned Hunter venom marker")
            if ev.source.startswith("mundane:") and not any(
                    t["active"] and t["source_tag"]==ev.source
                    and t.get("marker")==ev.ident
                    for t in d.toxins.instances.values()):
                raise UnresolvedDecision("Unowned mundane toxin marker")


def restore(previous, following):
    """Copy source-owned G4 ledgers after prior clock was settled & transferred.

    The existing G4.2 handoff copies chronological event IDs, deadlines and
    serials. This copies the interpreters *linked* to those events. Bite hit
    indexes are encounter-local and are NOT inherited as live hit authority.
    """
    p,f=previous.g4,following.g4
    f.short_toxins=deepcopy([v for v in p.short_toxins
                            if v["recipient"] in PARTY])
    f.toxins.instances=deepcopy({k:v for k,v in p.toxins.instances.items()
                                if k in PARTY})
    f.toxins.exposure_ids=set(p.toxins.exposure_ids)
    f.venom.effects=deepcopy({
        k:v for k,v in p.venom.effects.items()
        if v["caster"] in PARTY or v["recipient"] in PARTY})
    f.venom.next_effect=p.venom.next_effect
    f.venom.hunter_keys=set(p.venom.hunter_keys)
    f.venom.hit_keys=set()  # Earlier encounter-local Bite indices lack authority here.
    f.used_events.update(k for k in p.used_events if k.startswith("toxin:"))
    for n in PARTY:
        # State is first checked as a *source* value; no free ability/MP/AP.
        f.toxins._synchronize(n)
    if effect_state(previous)!=effect_state(following):
        raise AssertionError("Native toxin/Endurance continuation identity changed")


def matrix():
    """One actually source-paid G4.3 exposure through live G8-to-G8 handoff."""
    from scripts.b05_b06_native_party_continuity_v0 import (
        _first_withdrawal, _new_scene, handoff,
    )
    from scripts.b06_g7a_native_terminal_census_v0 import canonical_digest
    source=_first_withdrawal(3,0)
    dose=source.g4.toxins.apply(
        "guardian","TX-NP",exposure_key="source:gate:np",
        source="GM:documented-contaminated-water",route="ingestion",
        delivery_verified=True,resistance_die=1)
    if dose["outcome"]!="accepted":
        raise AssertionError("Native mundane toxin was not actually accepted")
    prior=effect_state(source)
    dest,_=_new_scene("sentry_cold",3,0,prepared_only=True)
    receipt=handoff(source,dest,elapsed_seconds=100,
                    travel_ref="GM:gate-to-sentry:100s",
                    carry_effects=True)
    arrival=effect_state(dest)
    if canonical_digest(arrival)!=receipt["native_effect_continuation_sha256"]:
        raise AssertionError("G4 toxin/clock receipt changed on arrival")
    t=dest.g4.toxins.active("guardian")
    marker=dest.g4.clock.events[t["marker"]]
    seconds=marker.due_seconds-dest.g4.clock.world_seconds
    before=dest.actors["guardian"].vigor
    dest.g4.clock.advance_exploration(seconds)
    if dest.actors["guardian"].vigor!=before-1:
        raise AssertionError("Native scheduled toxin pulse did not deliver")
    return {
        "version":"B05-B06-Effect-Duration-Continuation-v0",
        "scope":"actual_G8_live_instance_no_human_play",
        "native_exposure":dose,"handoff":receipt,
        "source_effect_sha256":canonical_digest(prior),
        "arrival_effect_sha256":canonical_digest(arrival),
        "remaining_seconds_until_native_pulse":seconds,
        "next_native_toxin_event":t["marker"],
        "vigor_before_pulse":before,
        "vigor_after_pulse":dest.actors["guardian"].vigor,
        "same_authenticated_marker":t["marker"] in arrival["clock_events"],
        "independent_focus_certificates":0,"human_pilot_sessions":0,
        "mvp_exit_gates":0,
    }


def main():
    import json
    print(json.dumps(matrix(),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
