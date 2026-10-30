"""B04/B05 — source-verified Anointed Restoration ordinary physical G5 melee.

One authored AH/AM dagger or AL sword, no supernatural effect added to the
mundane weapon, and no off-turn Opportunity or Riposte authorization.
G1/G2 live wielding, G0 source AP and G4 damage always remain authoritative.
"""
from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile as high
from scripts.b05_medium_anointed_restoration_l1_l3_v0 import profile as medium
from scripts.b05_low_anointed_restoration_l1_l3_v0 import profile as low
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint

MELEE_IDS={
    "AH":"B05-PC-AH-DAGGER-PIERCE",
    "AM":"B05-PC-AM-DAGGER-PIERCE",
    "AL":"B05-PC-AL-SWORD-CUT",
}
SOURCES={
    "AH":("scripts/b05_high_anointed_restoration_l1_l3_v0.py",high,"High","Dagger","Small Blades",2,0,"d4","Pierce"),
    "AM":("scripts/b05_medium_anointed_restoration_l1_l3_v0.py",medium,"Medium","Dagger","Small Blades",2,0,"d4","Pierce"),
    "AL":("scripts/b05_low_anointed_restoration_l1_l3_v0.py",low,"Low","Sword","One-Handed Swords",3,2,"d6","Cut"),
}


def anointed_weapon_profile(actor,profile_id,*,encounter):
    """Return (canonical G4 typed packet, normal attack bonus) or fail closed.

    Source-bound training/weapon/ability and mutable G2 ready state both
    matter: source purchase, a claimed Guard, or a caller's attack bonus do
    not grant a native hit. The G0 Source attack-profile set grants only
    this one ordinary weapon identity per Focus, not magical effects.
    """
    role=actor.source.source_id
    if role not in SOURCES or profile_id!=MELEE_IDS.get(role):
        raise UnresolvedDecision("Only sourced Anointed ordinary Dagger/Sword attack")
    path,make,focus,weapon,family,base,pen,die,trauma=SOURCES[role]
    p=make(actor.level)
    source=actor.source
    gear=tuple(sorted(
        (name,"worn" if name=="Leather armor" else
         "wielded" if name==weapon else "carried")
        for name in p["equipment_sp"]
    ))
    if (source.path!=path or source.digest!=_fingerprint(path)
            or source.status!="STRUCTURAL_B05_ONLY"
            or source.start_state!=f"L{actor.level}-{focus.lower()}-anointed-restoration-structural"
            or source.attack_profiles!=(MELEE_IDS[role],)
            or source.equipment!=gear
            or dict(source.training)!=p["weapon_training"]
            or dict(source.abilities)!=p["abilities"]
            or actor.focus!=focus
            or actor.level not in (1,2,3)
            or actor.hp_max!=p["hp_max"]
            or actor.vigor_max!=p["vigor_max"]
            or actor.vp_max!=p["vp_max"]
            or actor.ap_total!=p["turn_ap"]
            or actor.physical_ap!=p["physical_action_ap"]
            or actor.projection_ap!=p["projection_action_ap"]
            or actor.regen!=p["normal_regen_throughput"]
            or actor.guard_instrument!=weapon
            or p["wielded_weapon"]!=weapon
            or p["weapon_training"]!={family:2}):
        raise UnresolvedDecision("Anointed physical attacker source mismatch")
    if (getattr(encounter,"g2",None) is None
            or getattr(encounter,"g1",None) is None
            or actor.id not in encounter.actors
            or encounter.actors[actor.id] is not actor
            or set(encounter.g2.wielded.get(actor.id,()))!={weapon}):
        raise UnresolvedDecision("Real G2 currently wielded Anointed weapon required")
    abilities=p["abilities"]
    bonus=abilities["Strength"]+abilities["Agility"]+p["weapon_training"][family]
    if bonus!=3 or abilities["Strength"]!=0:
        raise AssertionError("Authored AH/AM/AL physical source numbers drifted")
    return ({
        "id":MELEE_IDS[role],
        "range_class":"melee",
        "primary_hp_packet":{
            "fixed_base":base,"die":die,"damage_type":trauma,
            "armor_penetration":pen,"strength_contribution":"light",
        },
        "additional_packets":[],"toxin_delivery":None,
    },bonus)
