from __future__ import annotations

from cyberlab.infrastructure.docker import inspect_running
from cyberlab.store.metadata import list_labs, load_lab


def show_status(lab_id: str) -> None:
    lab = load_lab(lab_id)
    att = inspect_running(lab.attacker_name)
    tgt = inspect_running(lab.target_name)
    print(f"lab_id:     {lab.lab_id}")
    print(f"scenario:   {lab.scenario}")
    print(f"status:     {lab.status}")
    print(f"created_at: {lab.created_at}")
    print(f"expires_at: {lab.expires_at}")
    print(f"network:    {lab.network_name} {lab.subnet}")
    print(f"attacker:   {lab.attacker_name} {lab.attacker_ip} running={att}")
    print(f"target:     {lab.target_name} {lab.target_ip} running={tgt}")


def show_list() -> None:
    labs = list_labs()
    if not labs:
        print("No labs.")
        return
    print(f"{'ID':<12} {'STATUS':<12} {'SCENARIO':<16} {'EXPIRES'}")
    for lab in labs:
        print(f"{lab.lab_id:<12} {lab.status:<12} {lab.scenario:<16} {lab.expires_at or '-'}")
