"""Checks every plugin folder under tools/ and examples/plugins/.

A plugin folder is any folder holding a plugin.json. Each must:
  - have a valid plugin.json (name required; version, description, dsc_api, entry typed right),
  - have its entry file (default __init__.py), defining register(),
  - and, under tools/, be listed in README.md's tool index.

Run from the repo root: python scripts/check_plugins.py
"""

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = {"name": str, "version": str, "description": str, "dsc_api": str, "entry": str}


def check(folder: Path, readme: str) -> list[str]:
    where = folder.relative_to(ROOT).as_posix()
    try:
        manifest = json.loads((folder / "plugin.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [f"{where}: plugin.json unreadable: {e}"]
    if not isinstance(manifest, dict):
        return [f"{where}: plugin.json must be a JSON object"]

    errors = []
    for key, value in manifest.items():
        if key not in FIELDS:
            errors.append(f"{where}: unknown plugin.json key '{key}'")
        elif not isinstance(value, FIELDS[key]):
            errors.append(f"{where}: '{key}' must be a {FIELDS[key].__name__}")
    if not manifest.get("name"):
        errors.append(f"{where}: plugin.json needs a 'name'")
    api = manifest.get("dsc_api")
    if isinstance(api, str) and not re.fullmatch(r"\d+\.\d+", api):
        errors.append(f"{where}: dsc_api must be 'MAJOR.MINOR', got '{api}'")

    entry = folder / str(manifest.get("entry", "__init__.py"))
    if not entry.is_file():
        errors.append(f"{where}: entry file {entry.name} missing")
    else:
        tree = ast.parse(entry.read_text(encoding="utf-8"), str(entry))
        if not any(isinstance(n, ast.FunctionDef) and n.name == "register" for n in tree.body):
            errors.append(f"{where}: {entry.name} defines no register()")

    if where.startswith("tools/") and f"]({where}/)" not in readme:
        errors.append(f"{where}: not listed in README.md's tool index as [..]({where}/)")
    return errors


def main() -> int:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    folders = sorted(p.parent for base in ("tools", "examples/plugins")
                     for p in (ROOT / base).rglob("plugin.json"))
    errors = [e for f in folders for e in check(f, readme)]
    for e in errors:
        print(e)
    print(f"{len(folders)} plugin(s) checked, {len(errors)} problem(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
