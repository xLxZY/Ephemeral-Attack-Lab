from __future__ import annotations

import json
import re
from typing import Any

from cyberlab.infrastructure.docker import cat_file, inspect_running
from cyberlab.models.lab import Lab
from cyberlab.store.metadata import events_path
from cyberlab.telemetry.elasticsearch import bulk_index
from cyberlab.telemetry.events import make_event

_FAILED = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+)"
)
_ACCEPTED = re.compile(r"Accepted password for (\S+) from (\S+)")
_NGINX = re.compile(
    r'^(\S+) .* "(\S+) ([^"]+) HTTP/[^"]+" (\d+)'
)


def _append_jsonl(lab_id: str, events: list[dict[str, Any]]) -> None:
    path = events_path(lab_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event) + "\n")


def collect(lab: Lab) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not inspect_running(lab.target_name):
        return events

    auth = cat_file(lab.target_name, "/var/log/auth.log") or cat_file(
        lab.target_name, "/var/log/secure"
    )
    for line in auth.splitlines():
        m = _FAILED.search(line)
        if m:
            events.append(
                make_event(
                    lab.lab_id,
                    "web-01",
                    "authentication_failure",
                    user=m.group(1),
                    source=m.group(2),
                    severity="medium",
                )
            )
            continue
        m = _ACCEPTED.search(line)
        if m:
            events.append(
                make_event(
                    lab.lab_id,
                    "web-01",
                    "authentication_success",
                    user=m.group(1),
                    source=m.group(2),
                    severity="info",
                )
            )

    access = cat_file(lab.target_name, "/var/log/acme-reporting/access.log")
    for line in access.splitlines():
        m = _NGINX.search(line)
        if not m:
            continue
        events.append(
            make_event(
                lab.lab_id,
                "web-01",
                "http_request",
                source=m.group(1),
                metadata={"method": m.group(2), "path": m.group(3), "status": m.group(4)},
            )
        )

    hook = cat_file(lab.target_name, "/var/log/acme-reporting/deploy-hook.log")
    for line in hook.splitlines():
        events.append(
            make_event(
                lab.lab_id,
                "web-01",
                "process_start",
                user="root",
                process="deploy-hook.sh",
                command=line.strip(),
                severity="info",
            )
        )

    backup = cat_file(lab.target_name, "/var/log/acme-reporting/backup.log")
    for line in backup.splitlines():
        if "backup wrote" in line:
            events.append(
                make_event(
                    lab.lab_id,
                    "web-01",
                    "process_start",
                    user="backup",
                    process="backup.sh",
                    command=line.strip(),
                )
            )

    _append_jsonl(lab.lab_id, events)
    bulk_index(events)
    return events


def load_jsonl(lab_id: str) -> list[dict[str, Any]]:
    path = events_path(lab_id)
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out
