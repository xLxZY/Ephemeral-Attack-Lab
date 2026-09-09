from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Lab:
    lab_id: str
    scenario: str
    status: str
    created_at: str
    expires_at: str | None
    attacker_name: str
    attacker_ip: str
    target_name: str
    target_ip: str
    network_name: str
    subnet: str
    terraform_state_path: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Lab":
        return cls(**data)
