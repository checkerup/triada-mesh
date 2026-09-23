"""Contracts and schemas for Jev Pacer Watchdog."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TaskStatus:
    agent: str
    task_id: str
    iteration: int = 1
    claims_done: bool = False
    tests_run: bool = False
    tests_passed: bool = False
    waiting_on_external: bool = False
    external_blocker: Optional[str] = None
    last_output_tail: str = ""
    updated_at: float = 0.0
    artifacts: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TaskStatus:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class KickPayload:
    kick_id: int
    task_id: str
    stalled_location: str
    confidence: float
    message: str
    issued_at: str
    details: Dict[str, Any] = field(default_factory=dict)
