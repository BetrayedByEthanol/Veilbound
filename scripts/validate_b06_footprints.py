"""B06 semantic footprint checks for bestiary, enemy and physiology JSON.

JSON Schema Draft 2020-12 cannot, without nonstandard extensions, express
"reference_cell_id is one of the values in sibling array cell_ids".
The physiology-only Hunter snapshot uses footprint_cell_ids directly under
creature_profile; its own JSON Schema constrains the shape, and this validator
checks membership and the authoritative head/rear identity semantically.
Run this alongside normal JSON Schema validation, not in place of it:

    python -m scripts.validate_b06_footprints

With no arguments, validates every content/creatures/b06-*.json.
Explicit filenames are also supported for authoring and CI.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
CREATURE_DIR = ROOT / "content" / "creatures"
SUPPORTED_VERSIONS = frozenset((
    "b06-bestiary-index-v0",
    "b06-enemy-v0",
    "b06-hunter-physiology-v0",
))


def validate_footprint(footprint: Any, location: str = "footprint") -> list[str]:
    """Return human-readable semantic errors, without modifying the record."""
    if not isinstance(footprint, dict):
        return [f"{location}: footprint must be an object"]

    errors: list[str] = []
    cell_ids = footprint.get("cell_ids")
    ref = footprint.get("reference_cell_id")

    if not isinstance(cell_ids, list) or not cell_ids:
        errors.append(f"{location}.cell_ids: expected a nonempty list")
        return errors

    if any(not isinstance(value, str) or not value for value in cell_ids):
        errors.append(f"{location}.cell_ids: all IDs must be nonempty strings")
        return errors

    if len(cell_ids) != len(set(cell_ids)):
        errors.append(f"{location}.cell_ids: body-local cell IDs must be unique")

    if not isinstance(ref, str) or ref not in cell_ids:
        errors.append(
            f"{location}.reference_cell_id: {ref!r} must occur in cell_ids"
        )

    # A rectangular footprint covers exactly width × length occupied cells.
    # Nonrectangular shapes need their own geometry definitions.
    if footprint.get("shape") == "rectangular":
        width, length = footprint.get("width_cells"), footprint.get("length_cells")
        if (type(width) is int and width > 0
                and type(length) is int and length > 0
                and len(cell_ids) != width * length):
            errors.append(
                f"{location}.cell_ids: rectangular {width}x{length} footprint "
                f"needs {width * length} cells, found {len(cell_ids)}"
            )

    return errors


def validate_b06_document(document: Any, location: str = "<document>") -> list[str]:
    """Check B06 anatomical-cell semantics by explicitly registered format."""
    if not isinstance(document, dict):
        return [f"{location}: B06 document must be an object"]

    version = document.get("schema_version")
    if version not in SUPPORTED_VERSIONS:
        return [f"{location}.schema_version: unsupported B06 version {version!r}"]

    errors: list[str] = []
    if version == "b06-bestiary-index-v0":
        entries = document.get("entries")
        if not isinstance(entries, list):
            return [f"{location}.entries: expected a list"]
        for index, entry in enumerate(entries):
            where = f"{location}.entries[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{where}: entry must be an object")
                continue
            profile = entry.get("creature_profile")
            if isinstance(profile, dict) and "footprint" in profile:
                errors.extend(validate_footprint(
                    profile["footprint"], f"{where}.creature_profile.footprint"
                ))
    elif version == "b06-enemy-v0":
        profile = document.get("creature_profile")
        if isinstance(profile, dict) and "footprint" in profile:
            errors.extend(validate_footprint(
                profile["footprint"], f"{location}.creature_profile.footprint"
            ))
    elif version == "b06-hunter-physiology-v0":
        # This is a deliberately incomplete, NON-EXECUTABLE Hunter calibration
        # record. Its footprint fields are direct children of creature_profile,
        # unlike the full enemy/index formats. Never silently ignore them or
        # accept an empty record with only schema_version.
        if document.get("record_status") != "PHYSIOLOGY_ONLY_NOT_EXECUTABLE":
            errors.append(
                f"{location}.record_status: Hunter physiology must remain "
                "'PHYSIOLOGY_ONLY_NOT_EXECUTABLE'"
            )
        if document.get("full_enemy_fixture_path", object()) is not None:
            errors.append(
                f"{location}.full_enemy_fixture_path: physiology record "
                "must not claim an executable enemy fixture"
            )
        if document.get("creature_id") != "B06-EN-03":
            errors.append(
                f"{location}.creature_id: Hunter physiology must identify B06-EN-03"
            )
        profile = document.get("creature_profile")
        where = f"{location}.creature_profile"
        if not isinstance(profile, dict):
            errors.append(f"{where}: expected an object")
        else:
            errors.extend(validate_footprint(
                {
                    "cell_ids": profile.get("footprint_cell_ids"),
                    "reference_cell_id": profile.get("reference_cell_id"),
                    "shape": "rectangular",
                    "width_cells": 1,
                    "length_cells": 2,
                },
                where,
            ))
            # The referenced Hunter's anatomy is specifically head/rear.
            # A matching list/ref that silently describes a different body
            # is not a valid partial snapshot of B06-EN-03.
            if profile.get("footprint_cell_ids") != ["head", "rear"]:
                errors.append(
                    f"{where}.footprint_cell_ids: Hunter requires "
                    "ordered ['head', 'rear'] local cells"
                )
            if profile.get("reference_cell_id") != "head":
                errors.append(
                    f"{where}.reference_cell_id: Hunter reference must be 'head'"
                )
    return errors


def validate_files(paths: Sequence[Path]) -> list[str]:
    """Validate authored files from disk; useful for CI and build tooling."""
    errors: list[str] = []
    for path in paths:
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: unable to read valid JSON: {exc}")
            continue
        errors.extend(validate_b06_document(document, str(path)))
    return errors


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths", metavar="JSON_FILE", nargs="*", type=Path,
        help="B06 JSON files; defaults to content/creatures/b06-*.json"
    )
    args = parser.parse_args(argv)
    paths = args.paths or sorted(CREATURE_DIR.glob("b06-*.json"))
    if not paths:
        print("No B06 JSON files selected")
        return 1
    errors = validate_files(paths)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"B06 footprint semantic validation failed ({len(errors)} error(s))")
        return 1
    print(f"B06 footprint semantic validation passed ({len(paths)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
