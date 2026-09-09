from __future__ import annotations

from datetime import datetime, timezone

from cyberlab.orchestrator.destroy import destroy_lab
from cyberlab.store.metadata import list_labs


def reap() -> None:
    now = datetime.now(timezone.utc)
    for lab in list_labs():
        if lab.status != "ACTIVE" or not lab.expires_at:
            continue
        exp = datetime.strptime(lab.expires_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if exp <= now:
            print(f"[+] Reaping expired lab {lab.lab_id}")
            destroy_lab(lab.lab_id)
