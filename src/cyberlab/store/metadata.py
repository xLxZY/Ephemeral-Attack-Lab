from __future__ import annotations

import json
import re
from pathlib import Path

from cyberlab.config.settings import LABS_DIR
from cyberlab.models.lab import Lab

_ID_RE = re.compile(r"^lab-(\d{3})$")


def lab_dir(lab_id: str) -> Path:
    return LABS_DIR / lab_id


def metadata_path(lab_id: str) -> Path:
    return lab_dir(lab_id) / "metadata.json"


def events_path(lab_id: str) -> Path:
    return lab_dir(lab_id) / "events.jsonl"


def save_lab(lab: Lab) -> None:
    path = metadata_path(lab.lab_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lab.to_dict(), indent=2) + "\n", encoding="utf-8")


def load_lab(lab_id: str) -> Lab:
    path = metadata_path(lab_id)
    if not path.is_file():
        raise FileNotFoundError(f"unknown lab: {lab_id}")
    return Lab.from_dict(json.loads(path.read_text(encoding="utf-8")))


def list_labs() -> list[Lab]:
    if not LABS_DIR.is_dir():
        return []
    labs: list[Lab] = []
    for child in sorted(LABS_DIR.iterdir()):
        meta = child / "metadata.json"
        if meta.is_file():
            labs.append(Lab.from_dict(json.loads(meta.read_text(encoding="utf-8"))))
    return labs


def next_lab_id() -> str:
    n = 0
    for lab in list_labs():
        m = _ID_RE.match(lab.lab_id)
        if m:
            n = max(n, int(m.group(1)))
    return f"lab-{n + 1:03d}"


def next_subnet(lab_id: str) -> str:
    m = _ID_RE.match(lab_id)
    idx = int(m.group(1)) - 1 if m else 0
    if idx < 0 or idx > 255:
        raise ValueError("lab index out of subnet range")
    return f"172.20.{idx}.0/24"


def ips_for_subnet(subnet: str) -> tuple[str, str]:
    prefix = subnet.rsplit(".", 1)[0]
    # 172.20.N.0/24 -> prefix 172.20.N
    base = ".".join(subnet.split(".")[:3])
    return f"{base}.2", f"{base}.3"
