# Ephemeral Attack Lab

Python- and Terraform-driven platform that creates a short-lived isolated Docker lab: security workstation `attacker-01` and company server `web-01`. Telemetry goes to Elasticsearch, Grafana visualizes it, evidence is written to disk, then the lab is destroyed.

## Problem

Manual cyber labs waste time on machines, users, networks, logs, and cleanup. This automates create → observe → collect → destroy → report.

## Core idea

Infrastructure that is created to be attacked inside an isolated lab, observed, investigated, and safely destroyed. Evidence survives.

## Architecture

CLI → orchestrator → Terraform → Docker network → attacker-01 + web-01 → events → Elasticsearch → Grafana → evidence pack → destroy.

## Stack

Docker, Python (Typer), Terraform, Elasticsearch, Grafana.

## Quick start (VM)

See `docs/deployment.md`. Short path:

```bash
make build-target
make build-attacker
make platform-up
python3 -m venv .venv && source .venv/bin/activate && pip install -e .
cyberlab create --scenario ssh-privesc
cyberlab shell attacker lab-001
cyberlab collect lab-001
cyberlab report lab-001
cyberlab destroy lab-001
## Security warning

Run only in a dedicated VM. Do not publish lab ports to your LAN. Do not point attacker tools at any host except the lab target IP. Lab passwords are fake and lab-scoped. Attacker and target must not receive the Docker socket, host mounts, host network, or privileged mode.

## Limitations

Single-host Docker. One scenario. Elasticsearch security disabled for the private VM. Not a SOC/SIEM product.

## Future work

Additional scenarios only after this loop is stable: web compromise, backup misconfiguration, internal pivot.
