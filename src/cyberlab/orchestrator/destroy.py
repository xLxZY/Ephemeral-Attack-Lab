from __future__ import annotations

from cyberlab.evidence.collector import collect_evidence
from cyberlab.infrastructure.terraform import destroy, init
from cyberlab.models.lab import Lab
from cyberlab.store.metadata import load_lab, save_lab


def destroy_lab(lab_id: str) -> Lab:
    lab = load_lab(lab_id)
    print("[+] Collecting evidence")
    lab.status = "COLLECTING"
    save_lab(lab)
    collect_evidence(lab)
    print("[+] Generating report")
    print("[+] Destroying attacker, target, network")
    lab.status = "DESTROYING"
    save_lab(lab)
    init()
    destroy(lab)
    lab.status = "DESTROYED"
    save_lab(lab)
    print(f"[+] Lab {lab.lab_id} DESTROYED; evidence in reports/{lab.lab_id}/")
    return lab
