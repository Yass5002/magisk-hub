#!/usr/bin/env python3
"""
Magisk Hub Module Validator
Validates all module JSON entries in modules/ against modules/schema.json (Draft-07).
Ensures schema adherence, JSON validity, and that the file slug matches the module id exactly.
Exits with status code 1 on any failure for CI pipeline integration.
"""

import glob
import json
import os
import sys

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("Error: 'jsonschema' package is required. Install via: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULES_DIR = os.path.join(REPO_ROOT, "modules")
SCHEMA_PATH = os.path.join(MODULES_DIR, "schema.json")


def load_schema():
    if not os.path.isfile(SCHEMA_PATH):
        print(f"Fatal: Schema file not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Fatal: Failed to parse schema.json: {e}", file=sys.stderr)
        sys.exit(2)


def validate_all_modules():
    schema = load_schema()
    validator = Draft7Validator(schema)

    # Collect all json files in modules/, excluding schema.json itself
    all_json_files = glob.glob(os.path.join(MODULES_DIR, "*.json"))
    module_files = [f for f in all_json_files if os.path.basename(f) != "schema.json"]

    if not module_files:
        print("Warning: No module files found in modules/", file=sys.stderr)
        sys.exit(1)

    errors_by_file = {}
    total_count = len(module_files)

    for file_path in sorted(module_files):
        filename = os.path.basename(file_path)
        expected_id = filename[:-5]  # strip '.json'
        file_errors = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            errors_by_file[filename] = [f"Invalid JSON syntax: {e}"]
            continue
        except Exception as e:
            errors_by_file[filename] = [f"Failed to read file: {e}"]
            continue

        # 1. Check ID to filename parity
        doc_id = data.get("id")
        if doc_id != expected_id:
            file_errors.append(
                f"Filename mismatch: file is '{filename}', but 'id' field is '{doc_id}' (expected '{expected_id}')"
            )

        # 2. Validate against JSON Schema
        schema_errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        for err in schema_errors:
            path_str = " -> ".join([str(p) for p in err.path]) if err.path else "root"
            file_errors.append(f"[{path_str}] {err.message}")

        # 3. Check local icon file existence if icon is specified
        icon_path = data.get("icon")
        if icon_path is not None:
            full_icon_path = os.path.join(REPO_ROOT, icon_path)
            if not os.path.isfile(full_icon_path):
                file_errors.append(f"Icon file not found at relative path '{icon_path}'")

        # 4. Check contentTier 1 requires markdown guide
        content_tier = data.get("contentTier")
        if content_tier == 1:
            full_md_path = os.path.join(REPO_ROOT, "content", "modules", f"{expected_id}.md")
            if not os.path.isfile(full_md_path):
                file_errors.append(f"contentTier is 1, but markdown guide is missing at 'content/modules/{expected_id}.md'")

        if file_errors:
            errors_by_file[filename] = file_errors

    # Report results
    if errors_by_file:
        print(f"\n❌ Validation failed: {len(errors_by_file)}/{total_count} files contain errors.\n", file=sys.stderr)
        for fname, errs in errors_by_file.items():
            print(f"• {fname}:", file=sys.stderr)
            for err in errs:
                print(f"    - {err}", file=sys.stderr)
        print("", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"✅ Success: All {total_count}/{total_count} modules are valid according to schema.")
        sys.exit(0)


if __name__ == "__main__":
    validate_all_modules()
