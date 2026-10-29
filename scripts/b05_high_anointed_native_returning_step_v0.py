"""B04/B05 High Anointed Life/Restoration: bounded native G0/G1/G4 Signature.

Authentic 20-AP G0 Projection and G4 live HP/Vigor packet. A source-locked
L1–3 High Anointed and separate finite Destiny account authorize the one
Returning Step packet. No Medium/Low Step access, guided spell, G5 attack,
contested +8 Intrusion, post-commit response or full Focus certification.
"""
from scripts.b05_anointed_authority_l1_l3_v0 import Anointed, returning_step
from scripts.b05_high_anointed_restoration_l1_l3_v0 import profile
from scripts.b06_encounter_state_v0 import UnresolvedDecision, _fingerprint
from scripts.b06_ranged_v0 import RangedCombat


class HighAnointedRestoration:
    def __init__(self, encounter, caster):
        if (encounter.g1 is None or encounter.g4 is None
                or caster not in encounter.actors
                or getattr(encounter.g4, "high_anointed", None) is not None):
            raise ValueError("One source-backed High Anointed requires native G1/G4")
        a = encounter.actors[caster]
        p = profile(a.level)
        path = "scripts/b05_high_anointed_restoration_l1_l3_v0.py"
        if (a.source.source_id != "AH" or a.source.path != path
                or a.source.status != "STRUCTURAL_B05_ONLY"
                or a.source.digest != _fingerprint(path)
                or a.focus != "High" or a.projection_ap != 20
                or a.hp_max != p["hp_max"] or a.vigor_max != p["vigor_max"]
                or a.vp_max != p["vp_max"] or a.ap_total != p["turn_ap"]
                or dict(a.source.abilities) != p["abilities"]):
            raise ValueError("Native source must be the exact High Anointed Restoration sheet")
        self.e = encounter
        self.caster = caster
        self.state = Anointed(a.level, "High", "Restoration")
        encounter.g4.high_anointed = self
        encounter.log("b05_high_anointed_source_bound", caster=caster,
                      source_digest=a.source.digest, level=a.level,
                      destiny=self.state.destiny,
                      scope="native_G0_G1_G4_unopposed_only")

    def _delivery(self, recipient, *, visible):
        """Current 2D G1 map geometry; visibility is an explicit scene fact."""
        if type(visible) is not bool or not visible:
            raise UnresolvedDecision("Current target visibility must be explicitly confirmed")
        a, b = self.e.actors[self.caster], self.e.actors[recipient]
        if len(a.occupied) != 1 or len(b.occupied) != 1:
            raise UnresolvedDecision("Multicell magical delivery not authored in this native slice")
        origin, dest = a.occupied[0], b.occupied[0]
        distance = max(abs(origin[0]-dest[0]), abs(origin[1]-dest[1]))
        limit = 4 if a.level >= 2 else 3
        if distance > limit:
            raise ValueError("High Returning Step target exceeds native Focus range")
        if distance and self.caster != recipient:
            cells, corners = RangedCombat._ray(origin, dest)
            walls = self.e.g1.walls
            if any(u in walls or v in walls for u,v in corners):
                raise UnresolvedDecision("Anointed path grazes an unadjudicated solid corner")
            if any(cell in walls for cell in cells[1:-1]):
                raise ValueError("Solid wall blocks magical delivery")
            if any(other.id not in (self.caster, recipient)
                   and any(cell in cells[1:-1] for cell in other.occupied)
                   for other in self.e.actors.values()):
                raise UnresolvedDecision("Intervening creature needs magical path adjudication")
        return distance

    def project(self, recipient, *, lesser=False, visible, unopposed,
                blocked_restoration=(), restoration_check=None):
        """One real paid own-turn Projection against the currently living target.

        Intrusion resistance is deliberately not guessed: a refused recipient
        needs native +8 contest authority, which this bounded slice lacks.
        No externally supplied 'paid action' or 'G4 packet success' flag.
        """
        e = self.e
        if (recipient not in e.actors or type(lesser) is not bool
                or type(unopposed) is not bool):
            raise ValueError("Explicit recipient/authority choice and opposition policy")
        a, b = e.actors[self.caster], e.actors[recipient]
        if (e.current != self.caster or e.pending_regeneration is not None
                or e.round < 1 or a.dead or a.hp <= 0
                or a.ap_remaining < 20):
            raise ValueError("High Anointed needs a legal ready G0 20-AP own turn")
        if b.dead or b.hp <= 0 or b.hp >= b.hp_max:
            raise ValueError("Returning Step requires living positive missing HP")
        if unopposed is not True:
            raise UnresolvedDecision("Contested +8 beneficial Intrusion not native-authorized")
        if not self.state.active_bond or self.state.level != a.level:
            raise ValueError("Anointed source bond cannot use Signature")
        if lesser and self.state.destiny < 1:
            raise ValueError("Insufficient finite source Destiny")
        if not lesser and b.vigor == 0:
            raise ValueError("Ordinary Signature requires target Vigor")
        distance = self._delivery(recipient, visible=visible)
        blocked = e.g4.live_heal_blocks(e, self.caster, recipient,
                                        blocked_restoration, restoration_check)
        if "hp" in blocked:
            raise ValueError("Current HP restoration is blocked")
        source_index = len(e.ledger)
        receipt = f"g0:{e.scenario}:r{e.round}:a{source_index}:{self.caster}"
        # Preview the SAME bounded source rule with live G0/G4 values; there
        # is no caller-supplied hit, target HP, paid AP or bogus Step receipt.
        preview = returning_step(
            self.state, receipt=receipt, target_id=recipient,
            recipient_hp=b.hp, recipient_max_hp=b.hp_max,
            recipient_vigor=b.vigor, lesser=lesser, ap_available=a.ap_remaining,
            distance=distance, path_visible=True, beneficial_intrusion_legal=True,
            intrusion_succeeded=True,
        )
        if preview.ap_spent != 20 or preview.hp_restored <= 0:
            raise AssertionError("High native source preview cannot authorize this projection")
        committed = e.spend_ap(self.caster, "projection",
                               label="anointed:high:returning_step")
        if committed != 20 or e.ledger[source_index]["kind"] != "action_committed":
            raise AssertionError("Missing exact real G0 Projection payment")
        # A G0 action may affect Movement segments. Re-read actual geometry
        # and G4 blocks before application; never trust the declaration's ray.
        current_distance = self._delivery(recipient, visible=visible)
        after_blocks = e.g4.live_heal_blocks(e, self.caster, recipient,
                                              blocked_restoration, restoration_check)
        if "hp" in after_blocks:
            raise UnresolvedDecision("Paid Signature now HP-blocked; no packet")
        final = returning_step(
            self.state, receipt=receipt, target_id=recipient,
            recipient_hp=b.hp, recipient_max_hp=b.hp_max, recipient_vigor=b.vigor,
            lesser=lesser, ap_available=20, distance=current_distance,
            path_visible=True, beneficial_intrusion_legal=True,
            intrusion_succeeded=True,
        )
        if final.hp_restored <= 0 or final.ap_spent != 20:
            raise UnresolvedDecision("Paid native Signature has no lawful surviving packet")
        if e.g4._live_high_anointed is not None:
            raise ValueError("Nested High Anointed native delivery forbidden")
        e.g4._live_high_anointed = (self.caster, recipient, source_index)
        try:
            delivered = e.g4.apply_high_anointed_returning_step(
                self.caster, recipient, action_index=source_index,
                hp_restored=final.hp_restored,
                recipient_vigor_spent=final.recipient_vigor_spent,
                lesser=lesser)
        finally:
            e.g4._live_high_anointed = None
        if delivered["hp_restored"] != final.hp_restored:
            raise AssertionError("G4 packet did not match the source Signature")
        self.state = final.actor
        e.log("b05_high_anointed_signature_resolved",
              caster=self.caster, recipient=recipient,
              action_index=source_index, source_receipt=receipt,
              lesser=lesser, destiny_remaining=self.state.destiny,
              hp_restored=delivered["hp_restored"],
              recipient_vigor_spent=delivered["recipient_vigor_spent"],
              ap_spent=committed, vp_spent=0,
              native_g0_g4=True, independent_focus_certified=False)
        e.check()
        return delivered | {"ap_spent":committed, "vp_spent":0,
                            "destiny_remaining":self.state.destiny,
                            "action_index":source_index}
