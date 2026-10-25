"""B04/B05 bounded source-native Medium/Low Scholar Sword Cut v0.

Attack stats come ONLY from the authored L1–3 selected Scholar source and
canonical one-handed Sword. G2's current wielding is mandatory: the
structural purchase or Guard number alone does not authorize a hit.
No secondary Fire, Embodiment weapon transformation or free Riposte.
"""
from scripts.b05_medium_scholar_l1_l3_v0 import profile as medium
from scripts.b05_low_scholar_l1_l3_v0 import profile as low
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint

SWORD_IDS={"S":"B05-PC-S-SWORD-CUT","T":"B05-PC-T-SWORD-CUT"}
SOURCES={
    "S":("scripts/b05_medium_scholar_l1_l3_v0.py",medium,
         "Medium","medium-scholar-inward"),
    "T":("scripts/b05_low_scholar_l1_l3_v0.py",low,
         "Low","low-scholar-prepared"),
}
SWORD_ITEM={"fixed_base":3,"die":"d6","damage_type":"Cut",
            "armor_penetration":2,"strength_contribution":"light"}


def scholar_sword_profile(actor, profile_id, *, encounter):
    """Return (packet source, attack bonus), fail closed before G0 payment.

    G2 owns the mutable equipped/ready set. Source equipment/Training cannot
    be replaced by a fabricated caller profile. Repeated calls on declare
    and resolve revalidate current live readiness.
    """
    role=actor.source.source_id
    if role not in SOURCES or profile_id!=SWORD_IDS.get(role):
        raise UnresolvedDecision("Only individually sourced S/T ordinary Sword Cut")
    path,make,focus,start=SOURCES[role]
    p=make(actor.level)
    source=actor.source
    gear=tuple(sorted((name,
        "worn" if name=="Leather armor" else
        "wielded" if name=="Sword" else "carried")
        for name in p["equipment_sp"]))
    if (source.path!=path or source.digest!=_fingerprint(path)
            or source.status!="STRUCTURAL_B05_ONLY"
            or source.start_state!=f"L{actor.level}-{start}"
            or source.attack_profiles!=(SWORD_IDS[role],)
            or source.equipment!=gear
            or dict(source.abilities)!=p["abilities"]
            or dict(source.training)!=p["weapon_training"]
            or actor.focus!=focus
            or actor.hp_max!=p["hp_max"]
            or actor.vigor_max!=p["vigor_max"]
            or actor.vp_max!=p["vp_max"]
            or actor.ap_total!=p["turn_ap"]
            or actor.physical_ap!=p["physical_action_ap"]
            or actor.projection_ap!=p["projection_action_ap"]
            or actor.regen!=p["normal_regen_throughput"]
            or actor.guard_instrument!="Sword"
            or actor.guard_value!=p["guard_value"]):
        raise UnresolvedDecision("Selected S/T Sword attack source mismatch")
    if (getattr(encounter,"g2",None) is None
            or getattr(encounter,"g1",None) is None
            or actor.id not in encounter.actors
            or encounter.actors[actor.id] is not actor
            or set(encounter.g2.wielded.get(actor.id,()))!={"Sword"}):
        raise UnresolvedDecision("Actual G2 Sword wielding required before melee")
    # Only a mundane Sword, one learned training family, one Cut attack.
    if (p["wielded_weapon"]!="Sword"
            or p["weapon_training"]!={"One-Handed Swords":2}):
        raise UnresolvedDecision("Source has no verified one-handed Sword")
    abilities=p["abilities"]
    bonus=(abilities["Strength"]+abilities["Agility"]
           +p["weapon_training"]["One-Handed Swords"])
    if bonus!=7:
        raise AssertionError("Unexpected Scholar authored Sword bonus drift")
    return ({
        "id":SWORD_IDS[role],"range_class":"melee",
        "primary_hp_packet":dict(SWORD_ITEM),
        "additional_packets":[],"toxin_delivery":None,
    },bonus)
