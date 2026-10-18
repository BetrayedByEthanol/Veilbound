"""B06 footprint cross-field semantics: real positive/negative file validation.

The JSON Schema checks field shape. These tests ensure the companion semantic
validator rejects references to nonexistent anatomical cells for BOTH accepted
B06 content formats. Every 'unittest discover' run executes these tests.
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate_b06_footprints import (
    validate_footprint,
    validate_b06_document,
    validate_files,
    main,
)


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "content/creatures/b06-initial-bestiary-v0.json"
SOLDIER_FILE = ROOT / "content/creatures/b06-ordinary-human-soldier.v0.json"
SENTRY_FILE = ROOT / "content/creatures/b06-firebound-sentry.v0.json"


class B06FootprintSemanticValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        cls.soldier = json.loads(SOLDIER_FILE.read_text(encoding="utf-8"))
        cls.sentry = json.loads(SENTRY_FILE.read_text(encoding="utf-8"))
        cls.hunter = next(e for e in cls.index["entries"] if e["id"] == "B06-EN-03")
        cls.footprint = cls.hunter["creature_profile"]["footprint"]

    def test_authored_hunter_is_semantically_valid(self):
        self.assertEqual(validate_footprint(self.footprint), [])
        self.assertEqual(validate_b06_document(self.index), [])

    def test_all_current_and_future_named_b06_files_pass_semantic_validation(self):
        # Discover all B06 files, not merely a hard-coded list of today's fixtures.
        # This makes `python -m unittest discover -s tests` catch future invalid
        # bestiary entries and new executable enemy files alike.
        paths = sorted((ROOT / "content/creatures").glob("b06-*.json"))
        self.assertTrue({INDEX_FILE, SOLDIER_FILE, SENTRY_FILE}.issubset(set(paths)))
        self.assertEqual(validate_files(paths), [])

    def test_typo_wing_reference_is_rejected_in_index(self):
        mutated = copy.deepcopy(self.index)
        hunter = next(e for e in mutated["entries"] if e["id"] == "B06-EN-03")
        fp = hunter["creature_profile"]["footprint"]
        fp["reference_cell_id"] = "wing"
        errors = validate_b06_document(mutated, "bestiary")
        self.assertEqual(len(errors), 1)
        self.assertIn("reference_cell_id", errors[0])
        self.assertIn("'wing' must occur in cell_ids", errors[0])
        self.assertIn("entries[2]", errors[0])

    def test_typo_wing_reference_is_rejected_in_enemy_fixture(self):
        mutated = copy.deepcopy(self.soldier)
        mutated["creature_profile"]["footprint"] = copy.deepcopy(self.footprint)
        mutated["creature_profile"]["footprint"]["reference_cell_id"] = "wing"
        errors = validate_b06_document(mutated, "soldier")
        self.assertEqual(len(errors), 1)
        self.assertIn("soldier.creature_profile.footprint.reference_cell_id", errors[0])
        self.assertIn("'wing'", errors[0])

    def test_valid_new_multi_square_enemy_fixture_passes(self):
        fixture = copy.deepcopy(self.soldier)
        fixture["creature_profile"]["footprint"] = copy.deepcopy(self.footprint)
        self.assertEqual(validate_b06_document(fixture, "new-enemy"), [])

    def test_no_footprint_is_still_legal(self):
        self.assertEqual(validate_b06_document(self.soldier), [])
        self.assertEqual(validate_b06_document(self.sentry), [])

    def test_missing_reference_fails(self):
        fp = copy.deepcopy(self.footprint)
        del fp["reference_cell_id"]
        self.assertIn("must occur in cell_ids",
                      " ".join(validate_footprint(fp)))

    def test_duplicate_cell_ids_fail(self):
        fp = copy.deepcopy(self.footprint)
        fp["cell_ids"] = ["head", "head"]
        fp["reference_cell_id"] = "head"
        self.assertTrue(any("must be unique" in error
                            for error in validate_footprint(fp)))

    def test_rectangular_count_mismatch_fails(self):
        fp = copy.deepcopy(self.footprint)
        fp["cell_ids"] = ["head", "rear", "tail"]
        fp["reference_cell_id"] = "head"
        self.assertTrue(any("needs 2 cells, found 3" in error
                            for error in validate_footprint(fp)))

    def test_empty_or_invalid_ids_fail_cleanly(self):
        for values in ([], None, ["head", ""]):
            with self.subTest(values=values):
                fp = copy.deepcopy(self.footprint)
                fp["cell_ids"] = values
                self.assertTrue(validate_footprint(fp))

    def test_cli_returns_failure_on_invalid_json_fixture(self):
        mutated = copy.deepcopy(self.soldier)
        mutated["creature_profile"]["footprint"] = copy.deepcopy(self.footprint)
        mutated["creature_profile"]["footprint"]["reference_cell_id"] = "wing"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "b06-bad-enemy.json"
            path.write_text(json.dumps(mutated), encoding="utf-8")
            with patch("builtins.print"):
                self.assertEqual(main([str(path)]), 1)

    def test_cli_accepts_valid_b06_fixture(self):
        with patch("builtins.print"):
            self.assertEqual(main([str(INDEX_FILE), str(SOLDIER_FILE)]), 0)

    def test_unsupported_version_cannot_silently_pass(self):
        self.assertTrue(validate_b06_document(
            {"schema_version": "b06-unrecognized-v9"}))


if __name__ == "__main__":
    unittest.main()
