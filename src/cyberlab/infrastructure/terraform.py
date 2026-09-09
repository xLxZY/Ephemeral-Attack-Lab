from __future__ import annotations

import subprocess
from pathlib import Path

from cyberlab.config.settings import TERRAFORM_DIR
from cyberlab.models.lab import Lab


class TerraformError(RuntimeError):
    pass


def _run(args: list[str], state: Path) -> str:
    cmd = ["terraform", *args, f"-state={state}"]
    proc = subprocess.run(
        cmd,
        cwd=TERRAFORM_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise TerraformError(proc.stderr or proc.stdout)
    return proc.stdout


def init() -> None:
    lock = TERRAFORM_DIR / ".terraform"
    cmd = ["terraform", "init", "-input=false"]
    proc = subprocess.run(cmd, cwd=TERRAFORM_DIR, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise TerraformError(proc.stderr or proc.stdout)
    _ = lock


def apply(lab: Lab) -> str:
    state = Path(lab.terraform_state_path)
    state.parent.mkdir(parents=True, exist_ok=True)
    vars_ = [
        f"-var=lab_id={lab.lab_id}",
        f"-var=scenario={lab.scenario}",
        f"-var=network_subnet={lab.subnet}",
        f"-var=attacker_ip={lab.attacker_ip}",
        f"-var=target_ip={lab.target_ip}",
    ]
    return _run(["apply", "-auto-approve", "-input=false", *vars_], state)


def destroy(lab: Lab) -> str:
    state = Path(lab.terraform_state_path)
    vars_ = [
        f"-var=lab_id={lab.lab_id}",
        f"-var=scenario={lab.scenario}",
        f"-var=network_subnet={lab.subnet}",
        f"-var=attacker_ip={lab.attacker_ip}",
        f"-var=target_ip={lab.target_ip}",
    ]
    return _run(["destroy", "-auto-approve", "-input=false", *vars_], state)
