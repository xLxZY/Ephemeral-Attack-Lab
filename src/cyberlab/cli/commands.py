from __future__ import annotations

import json

import typer

from cyberlab.config.settings import LAB_DEFAULT_DURATION
from cyberlab.evidence.collector import collect_evidence
from cyberlab.infrastructure.docker import shell_attacker
from cyberlab.orchestrator.create import create_lab
from cyberlab.orchestrator.destroy import destroy_lab
from cyberlab.orchestrator.reap import reap
from cyberlab.orchestrator.status import show_list, show_status
from cyberlab.store.metadata import load_lab
from cyberlab.telemetry.collector import collect

app = typer.Typer(no_args_is_help=True, help="Ephemeral Attack Lab")
shell_app = typer.Typer(no_args_is_help=True, help="Open a shell in a lab role")
app.add_typer(shell_app, name="shell")


@app.command("create")
def create_cmd(
    scenario: str = typer.Option(..., "--scenario", help="Scenario id"),
    duration: str | None = typer.Option(None, "--duration", help="e.g. 30m, 2m, 1h"),
) -> None:
    create_lab(scenario, duration if duration is not None else LAB_DEFAULT_DURATION)


@app.command("list")
def list_cmd() -> None:
    show_list()


@app.command("status")
def status_cmd(lab_id: str) -> None:
    show_status(lab_id)


@app.command("info")
def info_cmd(lab_id: str) -> None:
    lab = load_lab(lab_id)
    print(json.dumps(lab.to_dict(), indent=2))


@shell_app.command("attacker")
def shell_attacker_cmd(lab_id: str) -> None:
    lab = load_lab(lab_id)
    if lab.status != "ACTIVE":
        raise typer.Exit(code=1)
    raise typer.Exit(code=shell_attacker(lab))


@app.command("destroy")
def destroy_cmd(lab_id: str) -> None:
    destroy_lab(lab_id)


@app.command("report")
def report_cmd(lab_id: str) -> None:
    lab = load_lab(lab_id)
    path = collect_evidence(lab)
    print(f"[+] Report written to {path}")


@app.command("collect")
def collect_events_cmd(lab_id: str) -> None:
    lab = load_lab(lab_id)
    events = collect(lab)
    print(f"[+] Collected {len(events)} events for {lab_id}")


@app.command("reap")
def reap_cmd() -> None:
    reap()


if __name__ == "__main__":
    app()
