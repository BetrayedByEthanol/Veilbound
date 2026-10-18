"""B06 footprint cross-field semantics: real positive/negative file validation.

The JSON Schema checks field shape. These tests ensure the companion semantic
validator rejects references to nonexistent anatomical cells for ALL THREE
registered B06 content formats. Every 'unittest discover' run executes these tests.
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
PHYSIOLOGY_FILE = ROOT / "content/creatures/b06-hunter-physiology.v0.json"
PHYSIOLOGY_SCHEMA = ROOT / "schemas/b06-hunter-physiology-v0.schema.json"


class B06FootprintSemanticValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        cls.soldier = json.loads(SOLDIER_FILE.read_text(encoding="utf-8"))
        cls.sentry = json.loads(SENTRY_FILE.read_text(encoding="utf-8"))
        cls.physiology = json.loads(PHYSIOLOGY_FILE.read_text(encoding="utf-8"))
        cls.physiology_schema = json.loads(PHYSIOLOGY_SCHEMA.read_text(encoding="utf-8"))
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
        self.assertTrue({INDEX_FILE, SOLDIER_FILE, SENTRY_FILE, PHYSIOLOGY_FILE}.issubset(set(paths)))
        self.assertEqual(validate_files(paths), [])

    def test_hunter_physiology_version_and_schema_are_explicit(self):
        self.assertEqual(validate_b06_document(self.physiology, "physiology"), [])
        self.assertEqual(self.physiology_schema["$schema"],
                         "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.physiology_schema["properties"]["schema_version"]["const"],
                         "b06-hunter-physiology-v0")
        self.assertEqual(self.physiology_schema["properties"]["record_status"]["const"],
                         "PHYSIOLOGY_ONLY_NOT_EXECUTABLE")
        p = self.physiology_schema["properties"]["creature_profile"]
        self.assertIn("footprint_cell_ids", p["required"])
        self.assertIn("reference_cell_id", p["required"])
        self.assertTrue(p["properties"]["footprint_cell_ids"]["uniqueItems"])
        self.assertEqual(p["properties"]["footprint_cell_ids"]["const"], ["head", "rear"])
        self.assertEqual(p["properties"]["reference_cell_id"]["const"], "head")

    def test_hunter_physiology_reference_to_missing_cell_fails(self):
        mutated = copy.deepcopy(self.physiology)
        mutated["creature_profile"]["reference_cell_id"] = "wing"
        errors = validate_b06_document(mutated, "physiology")
        self.assertTrue(any("creature_profile.reference_cell_id" in error
                            and "wing" in error for error in errors))

    def test_hunter_physiology_wrong_ids_and_duplicate_fail(self):
        for ids in (["head", "head"], ["wing", "rear"], ["head"],
                    ["head", "rear", "tail"], [], None, ["head", ""]):
            with self.subTest(ids=ids):
                mutated = copy.deepcopy(self.physiology)
                mutated["creature_profile"]["footprint_cell_ids"] = ids
                self.assertTrue(validate_b06_document(mutated, "physiology"))

    def test_hunter_physiology_missing_profile_or_fields_fail(self):
        for target in ("creature_profile", "record_status", "creature_id",
                       "full_enemy_fixture_path"):
            with self.subTest(missing=target):
                mutated = copy.deepcopy(self.physiology)
                mutated.pop(target)
                self.assertTrue(validate_b06_document(mutated, "physiology"))
        mutated = copy.deepcopy(self.physiology)
        mutated["creature_profile"].pop("reference_cell_id")
        self.assertTrue(validate_b06_document(mutated, "physiology"))

    def test_hunter_physiology_cannot_claim_executable_status(self):
        for key, value in (
            ("record_status", "EXECUTABLE_TEST_FIXTURE"),
            ("creature_id", "B06-EN-04"),
            ("full_enemy_fixture_path", "content/creatures/pretend-enemy.json"),
        ):
            with self.subTest(key=key):
                mutated = copy.deepcopy(self.physiology)
                mutated[key] = value
                self.assertTrue(validate_b06_document(mutated, "physiology"))

    def test_default_cli_discovers_physiology_and_all_b06_records(self):
        # Reproduces the exact mandatory command: python -m
        # scripts.validate_b06_footprints (no explicit filenames).
        self.assertTrue(PHYSIOLOGY_FILE.exists())
        with patch("builtins.print"):
            self.assertEqual(main([]), 0)

    def test_hunter_physiology_cli_accepts_valid_and_rejects_corrupt(self):
        with patch("builtins.print"):
            self.assertEqual(main([str(PHYSIOLOGY_FILE)]), 0)
        mutated = copy.deepcopy(self.physiology)
        mutated["creature_profile"]["reference_cell_id"] = "wing"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "b06-hunter-physiology.json"
            path.write_text(json.dumps(mutated), encoding="utf-8")
            with patch("builtins.print"):
                self.assertEqual(main([str(path)]), 1)

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
