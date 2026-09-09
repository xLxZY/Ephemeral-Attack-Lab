from __future__ import annotations

from typing import Any

from cyberlab.models.lab import Lab


def render_markdown(lab: Lab, timeline: list[dict[str, Any]], events: list[dict[str, Any]]) -> str:
    auth_fail = sum(1 for e in events if e.get("event_type") == "authentication_failure")
    auth_ok = sum(1 for e in events if e.get("event_type") == "authentication_success")
    proc = sum(1 for e in events if e.get("event_type") == "process_start")
    http = sum(1 for e in events if e.get("event_type") == "http_request")
    lines = [
        "# EPHEMERAL ATTACK LAB REPORT",
        "",
        f"Lab ID: {lab.lab_id}",
        f"Scenario: {lab.scenario}",
        f"Target: web-01 ({lab.target_ip})",
        f"Attacker: attacker-01 ({lab.attacker_ip})",
        f"Status: {lab.status}",
        f"Created: {lab.created_at}",
        f"Expires: {lab.expires_at or 'n/a'}",
        "",
        "## Summary",
        "",
        "Controlled laboratory exercise on an isolated Docker network. "
        f"Collected {len(events)} events "
        f"(auth_fail={auth_fail}, auth_ok={auth_ok}, process={proc}, http={http}).",
        "",
        "## Timeline",
        "",
    ]
    for row in timeline:
        lines.append(
            f"- {row.get('timestamp')}  {row.get('event_type')}  "
            f"{row.get('host')}  {row.get('summary')}"
        )
    lines.append("")
    return "\n".join(lines)
