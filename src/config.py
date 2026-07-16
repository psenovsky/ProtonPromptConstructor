from __future__ import annotations

import json
from pathlib import Path


DEFAULTS_FILE = Path(__file__).resolve().parent.parent / "defaults.json"


def save_defaults(state: dict, path: Path = DEFAULTS_FILE) -> None:
    path.write_text(json.dumps(state, indent=2) + "\n")


def load_defaults(path: Path = DEFAULTS_FILE) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
