"""Regression checks for Adventure 01's player props and narrative custody."""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1] / "adventures" / "the-withering-road"
GM = ROOT / "gm-manuscript.md"
PROPS = ROOT / "player-handouts.md"

EXPECTED = {
    "P-1", "P-2",
    "M-1", "M-2", "M-3",
    "D-1", "D-2", "D-3", "D-4", "D-5",
    "C-1", "C-2", "C-3", "C-4",
    "F-1", "F-2", "F-3",
}


def handout_section(source: str, identifier: str) -> str:
    match = re.search(
        rf"^## Handout {re.escape(identifier)}\b[^\n]*\n"
        rf"(.*?)(?=^## Handout |\Z)",
        source,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"Missing player prop {identifier}")
    return match.group(1)


class Adventure01HandoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gm = GM.read_text(encoding="utf-8")
        cls.props = PROPS.read_text(encoding="utf-8")

    def test_all_referenced_identifiers_are_supplied(self):
        ids = re.findall(r"^## Handout ([PMDCF]-\d+)\b", self.props, re.MULTILINE)
        self.assertEqual(set(ids), EXPECTED)
        self.assertEqual(len(ids), len(set(ids)), "Duplicate handout labels")
        refs = set(re.findall(r"\b[PMDCF]-\d+\b", self.gm))
        self.assertFalse(refs - set(ids), f"Unprovided GM references: {refs - set(ids)}")
        self.assertTrue({"D-1", "D-2", "C-1", "F-1"} <= refs)

    def test_depot_manifest_puzzle_has_real_distinct_documents(self):
        outbound = handout_section(self.props, "D-1")
        incoming = handout_section(self.props, "D-2")
        transfer = handout_section(self.props, "D-3")
        outbound_ids = set(re.findall(r"17-\d{2}", outbound))
        incoming_ids = set(re.findall(r"17-\d{2}", incoming))
        self.assertEqual(outbound_ids, {f"17-{n:02}" for n in range(1, 7)})
        self.assertEqual(incoming_ids, {"17-01", "17-02", "17-04", "17-06"})
        self.assertEqual(outbound_ids - incoming_ids, {"17-03", "17-05"})
        self.assertIn("17-03", transfer)
        self.assertIn("17-05", transfer)
        self.assertNotIn("GM solution", incoming)

    def test_essential_dispatch_and_blank_release_form(self):
        dispatch = handout_section(self.props, "C-1")
        receipt = handout_section(self.props, "F-1")
        self.assertIn("Old Kiln Rest", dispatch)
        self.assertIn("R.C.", dispatch)
        self.assertIn("Ember Watch", dispatch)
        self.assertIn("Parcels actually handed over: ____________________", receipt)
        self.assertIn("Steward's confirmation: __________________________", receipt)
        self.assertIn("not an issued authorization", receipt)

    def test_courier_ring_location_is_consistent(self):
        note = handout_section(self.props, "C-4")
        self.assertIn("**kept your ring with me**", note)
        self.assertIn("ring remains with Talla at Ember Watch", self.gm)
        self.assertNotIn("ring can later be found in the depot/cache material", self.gm)
        self.assertNotIn("I left the old ring with the cache pouch", self.props)
        self.assertNotIn("inside the cache pouch near the ring", self.props)
        self.assertIn("The ring itself is **not** with the note", note)

    def test_secret_room_and_optional_boss_not_essential(self):
        self.assertIn("**not in the Heartweb Chamber**", self.gm)
        self.assertIn("ordinary records vault", self.gm.lower())
        self.assertIn("D-5", self.props)
        self.assertIn("F-1", self.props)


if __name__ == "__main__":
    unittest.main()
