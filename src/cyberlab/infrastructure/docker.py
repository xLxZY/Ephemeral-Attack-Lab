from __future__ import annotations

import subprocess

from cyberlab.models.lab import Lab


def inspect_running(name: str) -> bool:
    proc = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", name],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0 and proc.stdout.strip() == "true"


def health_http(lab: Lab, timeout: int = 8) -> bool:
    proc = subprocess.run(
        [
            "docker",
            "exec",
            lab.attacker_name,
            "curl",
            "-sS",
            "-m",
            str(timeout),
            f"http://{lab.target_ip}/health",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0 and "ok" in proc.stdout


def cat_file(container: str, path: str) -> str:
    proc = subprocess.run(
        ["docker", "exec", container, "cat", path],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else ""


def shell_attacker(lab: Lab) -> int:
    return subprocess.call(
        ["docker", "exec", "-it", "-u", "analyst", lab.attacker_name, "bash", "-l"]
    )
