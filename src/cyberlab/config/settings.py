from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(REPO_ROOT / ".env")


def _expand(path: str) -> Path:
    return Path(os.path.expanduser(path)).resolve()


MAX_ACTIVE_LABS = int(os.getenv("MAX_ACTIVE_LABS", "3"))
LAB_DEFAULT_DURATION = os.getenv("LAB_DEFAULT_DURATION", "30m")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://127.0.0.1:9201").rstrip("/")
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://127.0.0.1:3000").rstrip("/")
DOCKER_NETWORK_RANGE = os.getenv("DOCKER_NETWORK_RANGE", "172.20.0.0/16")
DATA_DIR = _expand(os.getenv("CYBERLAB_DATA_DIR", "~/.cyberlab"))
REPORTS_DIR = Path(os.getenv("CYBERLAB_REPORTS_DIR", str(REPO_ROOT / "reports")))
if not REPORTS_DIR.is_absolute():
    REPORTS_DIR = (REPO_ROOT / REPORTS_DIR).resolve()

TERRAFORM_DIR = REPO_ROOT / "infrastructure" / "terraform"
SCENARIOS_DIR = REPO_ROOT / "scenarios"
LABS_DIR = DATA_DIR / "labs"

ATTACKER_IMAGE = "cyberlab-attacker:dev"
TARGET_IMAGE = "cyberlab-web-01:dev"
