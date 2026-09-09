from __future__ import annotations

import time

from cyberlab.config.settings import (
    ATTACKER_IMAGE,
    DATA_DIR,
    LABS_DIR,
    MAX_ACTIVE_LABS,
    TARGET_IMAGE,
)
from cyberlab.infrastructure.docker import health_http, inspect_running
from cyberlab.infrastructure.terraform import apply, init
from cyberlab.models.lab import Lab
from cyberlab.orchestrator.duration import iso, parse_duration, utcnow
from cyberlab.scenarios.loader import load_scenario
from cyberlab.store.metadata import ips_for_subnet, list_labs, next_lab_id, next_subnet, save_lab


def create_lab(scenario: str, duration: str | None) -> Lab:
    load_scenario(scenario)
    active = [lab for lab in list_labs() if lab.status == "ACTIVE"]
    if len(active) >= MAX_ACTIVE_LABS:
        raise RuntimeError(f"MAX_ACTIVE_LABS={MAX_ACTIVE_LABS} reached")

    lab_id = next_lab_id()
    subnet = next_subnet(lab_id)
    attacker_ip, target_ip = ips_for_subnet(subnet)
    now = utcnow()
    expires = None
    if duration:
        expires = iso(now + parse_duration(duration))

    lab = Lab(
        lab_id=lab_id,
        scenario=scenario,
        status="CREATING",
        created_at=iso(now),
        expires_at=expires,
        attacker_name=f"attacker-01-{lab_id}",
        attacker_ip=attacker_ip,
        target_name=f"web-01-{lab_id}",
        target_ip=target_ip,
        network_name=f"cyberlab-{lab_id}",
        subnet=subnet,
        terraform_state_path=str(LABS_DIR / lab_id / "terraform.tfstate"),
    )
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    save_lab(lab)
    print("[+] Creating lab")
    print(f"[+] Lab ID: {lab.lab_id}")
    print("[+] Creating isolated network")
    print("[+] Starting attacker")
    print("[+] Starting target")
    _ = ATTACKER_IMAGE, TARGET_IMAGE
    init()
    apply(lab)
    print("[+] Running health checks")
    ok = False
    for _ in range(20):
        if inspect_running(lab.attacker_name) and inspect_running(lab.target_name) and health_http(lab):
            ok = True
            break
        time.sleep(2)
    if not ok:
        lab.status = "FAILED"
        save_lab(lab)
        raise RuntimeError("health checks failed; containers may still exist — cyberlab destroy " + lab.lab_id)
    lab.status = "ACTIVE"
    save_lab(lab)
    print()
    print("Lab ready.")
    print()
    print("Attacker:")
    print(f"  {lab.attacker_name}")
    print(f"  {lab.attacker_ip}")
    print()
    print("Target:")
    print(f"  {lab.target_name}")
    print(f"  {lab.target_ip}")
    print()
    print("Status:")
    print("  ACTIVE")
    if lab.expires_at:
        print(f"Expires: {lab.expires_at}")
    return lab
