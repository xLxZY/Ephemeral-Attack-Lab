from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

_RE = re.compile(r"^(\d+)([smh])$")


def parse_duration(text: str) -> timedelta:
    m = _RE.match(text.strip())
    if not m:
        raise ValueError("duration must look like 30m, 2m, 1h, 45s")
    n = int(m.group(1))
    unit = m.group(2)
    if unit == "s":
        return timedelta(seconds=n)
    if unit == "m":
        return timedelta(minutes=n)
    return timedelta(hours=n)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
