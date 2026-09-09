from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from cyberlab.config.settings import ELASTICSEARCH_URL

INDEX = "cyberlab-events"


def available() -> bool:
    try:
        with urllib.request.urlopen(ELASTICSEARCH_URL, timeout=3) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False


def bulk_index(events: list[dict[str, Any]]) -> None:
    if not events:
        return
    lines: list[str] = []
    for event in events:
        lines.append(json.dumps({"index": {"_index": INDEX}}))
        lines.append(json.dumps(event))
    body = ("\n".join(lines) + "\n").encode("utf-8")
    req = urllib.request.Request(
        f"{ELASTICSEARCH_URL}/_bulk",
        data=body,
        headers={"Content-Type": "application/x-ndjson"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp.read()
    except urllib.error.URLError:
        return


def search_lab(lab_id: str, size: int = 5000) -> list[dict[str, Any]]:
    payload = json.dumps(
        {
            "size": size,
            "query": {"term": {"lab_id.keyword": lab_id}},
            "sort": [{"timestamp": {"order": "asc", "unmapped_type": "date"}}],
        }
    ).encode("utf-8")
    # keyword subfield may not exist if ES dynamically mapped timestamp only.
    payload_alt = json.dumps(
        {
            "size": size,
            "query": {"term": {"lab_id": lab_id}},
            "sort": [{"timestamp": {"order": "asc", "unmapped_type": "date"}}],
        }
    ).encode("utf-8")
    for data in (payload, payload_alt):
        req = urllib.request.Request(
            f"{ELASTICSEARCH_URL}/{INDEX}/_search",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            hits = body.get("hits", {}).get("hits", [])
            return [h.get("_source", {}) for h in hits]
        except urllib.error.HTTPError:
            continue
        except urllib.error.URLError:
            return []
    return []
