"""Exact source authorization for L1–3 Scholar Thrown Flame.

This helper returns *only* the individually authored Primary Thrown
Projectile access. It never grants S/T native Sword offense, a new
Embodiment/Composite, or an unprepared Low outward technique.
"""
from scripts.b05_high_scholar_fire_l1_l3_v0 import profile as high_profile
from scripts.b05_medium_scholar_l1_l3_v0 import profile as medium_profile
from scripts.b05_low_scholar_l1_l3_v0 import profile as low_profile
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint

SOURCES={
    "F":("High","scripts/b05_high_scholar_fire_l1_l3_v0.py",high_profile),
    "S":("Medium","scripts/b05_medium_scholar_l1_l3_v0.py",medium_profile),
    "T":("Low","scripts/b05_low_scholar_l1_l3_v0.py",low_profile),
}


def flame_access(actor, *, wielded=None):
    """Fail closed on every selected character/repertoire/hand-bound source."""
    identity=SOURCES.get(actor.source.source_id)
    if identity is None or type(actor.level) is not int or actor.level not in (1,2,3):
        raise UnresolvedDecision("Only authored High/Medium/Low Scholar L1–3")
    focus,path,make=identity
    p=make(actor.level)
    a=actor.source
    gear=p["starting_equipment_sp"] if focus=="High" else p["equipment_sp"]
    expected_gear=tuple(sorted((name,
        "worn" if name=="Leather armor" else
        "wielded" if focus!="High" and name=="Sword" else "carried")
        for name in gear))
    expected_start=(f"L{actor.level}-structural" if focus=="High" else
                    f"L{actor.level}-medium-scholar-inward" if focus=="Medium"
                    else f"L{actor.level}-low-scholar-prepared")
    if (actor.focus!=focus or a.path!=path or a.digest!=_fingerprint(path)
            or a.status!="STRUCTURAL_B05_ONLY"
            or a.start_state!=expected_start
            or a.attack_profiles!=(
                (("B05-PC-S-SWORD-CUT",) if focus=="Medium"
                 else ("B05-PC-T-SWORD-CUT",) if focus=="Low"
                 else ())
            or a.equipment!=expected_gear
            or dict(a.abilities)!=p["abilities"]
            or dict(a.training)!=p["weapon_training"]
            or actor.hp_max!=p["hp_max"] or actor.vigor_max!=p["vigor_max"]
            or actor.vp_max!=p["vp_max"] or actor.ap_total!=p["turn_ap"]
            or actor.physical_ap!=p["physical_action_ap"]
            or actor.projection_ap!=p["projection_action_ap"]
            or actor.regen!=p["normal_regen_throughput"]):
        raise UnresolvedDecision("Scholar Thrown Flame source sheet mismatch")
    if ("Conjure Flame" not in p["known_pillar_techniques"]
            or (focus=="Low"
                and "Conjure Flame" not in p["prepared_techniques"])):
        raise UnresolvedDecision("Low Prepared Arsenal does not authorize this Flame")
    if wielded is not None:
        required=(set() if focus=="High" else {"Sword"})
        if set(wielded)!=required:
            raise UnresolvedDecision(
                "Authored one-handed Sword or High carried-Dagger hand state changed")
    abilities=p["abilities"]
    throwing=p["learned_disciplines"].get("Throwing",0)
    if type(throwing) is not int or throwing<0:
        raise UnresolvedDecision("Invalid sourced Throwing learned rank")
    bonus=abilities["Agility"]+abilities["Precision"]+throwing
    return {"focus":focus,"role":a.source_id,"level":actor.level,
            "action_ap":p["projection_action_ap"],
            "max_tier":p["max_used_tier"],"attack_bonus":bonus,
            "throwing":throwing,"source_digest":a.digest,
            "prepared":focus!="Low" or
                       "Conjure Flame" in p["prepared_techniques"]}
