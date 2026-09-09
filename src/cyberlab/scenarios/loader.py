from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from cyberlab.config.settings import SCENARIOS_DIR


def load_scenario(name: str) -> dict[str, Any]:
    path = SCENARIOS_DIR / name / "scenario.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"unknown scenario: {name} ({path})")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if data.get("name") != name:
        raise ValueError(f"scenario name mismatch in {path}")
    return data
