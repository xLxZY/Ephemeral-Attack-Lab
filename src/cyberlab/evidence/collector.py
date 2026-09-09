from __future__ import annotations

import json
from pathlib import Path

from cyberlab.config.settings import REPORTS_DIR
from cyberlab.evidence.report import render_markdown
from cyberlab.evidence.timeline import build_timeline
from cyberlab.models.lab import Lab
from cyberlab.telemetry.collector import collect, load_jsonl
from cyberlab.telemetry.elasticsearch import available, search_lab


def collect_evidence(lab: Lab) -> Path:
    live = []
    try:
        live = collect(lab)
    except Exception:
        live = []
    es_events = search_lab(lab.lab_id) if available() else []
    file_events = load_jsonl(lab.lab_id)
    events = es_events or file_events or live
    events = sorted(events, key=lambda e: e.get("timestamp") or "")
    timeline = build_timeline(lab, events)
    out = REPORTS_DIR / lab.lab_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "metadata.json").write_text(json.dumps(lab.to_dict(), indent=2) + "\n", encoding="utf-8")
    (out / "events.json").write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
    (out / "timeline.json").write_text(json.dumps(timeline, indent=2) + "\n", encoding="utf-8")
    (out / "report.md").write_text(render_markdown(lab, timeline, events), encoding="utf-8")
    return out
