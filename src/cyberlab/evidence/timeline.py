from __future__ import annotations

from typing import Any

from cyberlab.models.lab import Lab


def build_timeline(lab: Lab, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "timestamp": lab.created_at,
            "event_type": "lab_created",
            "host": "control",
            "summary": f"Lab {lab.lab_id} created scenario={lab.scenario}",
        }
    ]
    for event in events:
        rows.append(
            {
                "timestamp": event.get("timestamp"),
                "event_type": event.get("event_type"),
                "host": event.get("host"),
                "summary": event.get("command")
                or event.get("user")
                or event.get("event_type"),
            }
        )
    if lab.status == "DESTROYED":
        rows.append(
            {
                "timestamp": events[-1]["timestamp"] if events else lab.created_at,
                "event_type": "lab_destroyed",
                "host": "control",
                "summary": f"Lab {lab.lab_id} destroyed; evidence preserved",
            }
        )
    rows.sort(key=lambda r: r.get("timestamp") or "")
    return rows
