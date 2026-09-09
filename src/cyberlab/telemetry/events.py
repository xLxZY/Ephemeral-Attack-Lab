from __future__ import annotations

from typing import Any

from cyberlab.orchestrator.duration import iso, utcnow


def make_event(
    lab_id: str,
    host: str,
    event_type: str,
    **extra: Any,
) -> dict[str, Any]:
    event: dict[str, Any] = {
        "lab_id": lab_id,
        "timestamp": extra.pop("timestamp", iso(utcnow())),
        "host": host,
        "event_type": event_type,
    }
    event.update({k: v for k, v in extra.items() if v is not None})
    return event
