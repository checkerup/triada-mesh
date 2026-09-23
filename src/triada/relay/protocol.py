"""Triada Machine-Readable Handover Contract Protocol."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class HandoverPackage:
    handover_id: str
    task_id: str
    from_agent: str
    to_agent: str
    iteration: int
    git_base_sha: str
    artifacts: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)
    known_risks: List[str] = field(default_factory=list)
    context_notes: str = ""
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HandoverPackage:
        return cls(**data)

    def save(self, filepath: Path) -> None:
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, filepath: Path) -> HandoverPackage:
        p = Path(filepath)
        if not p.exists():
            raise FileNotFoundError(f"Handover file not found: {filepath}")
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls.from_dict(data)
