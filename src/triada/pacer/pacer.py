"""Jev Pacer & Iteration Watchdog.

Evaluates agent iteration evidence (git diff, status.json, test execution)
against the task specification using TypeSafe System One Jev arbiter.
Intercepts False Finish and Stalls by issuing targeted kicks.
"""

from __future__ import annotations

import importlib
import json
import logging
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from triada.config import TriadaConfig
from triada.pacer.contracts import KickPayload, TaskStatus
from triada.providers.base import KeyPoolProvider
from triada.providers.env_provider import EnvKeyPoolProvider

log = logging.getLogger("triada.pacer")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_provider(provider_spec: str) -> KeyPoolProvider:
    """Loads KeyPoolProvider by name ('env') or import path 'pkg.module:Class'."""
    if provider_spec == "env":
        return EnvKeyPoolProvider()

    if ":" in provider_spec:
        mod_name, class_name = provider_spec.split(":", 1)
        mod = importlib.import_module(mod_name)
        cls = getattr(mod, class_name)
        return cls()

    return EnvKeyPoolProvider()


class JevPacer:
    """Watchdog daemon evaluating tasks and issuing kicks on false finish or stalls."""

    def __init__(self, config: TriadaConfig, provider: Optional[KeyPoolProvider] = None):
        self.config = config
        self.provider = provider or load_provider(config.jev_provider)

    def evaluate_task(self, task_dir: Path) -> Optional[KickPayload]:
        task_id = task_dir.name
        status_file = task_dir / "status.json"
        if not status_file.exists():
            return None

        try:
            status_data = json.loads(status_file.read_text(encoding="utf-8"))
            status = TaskStatus.from_dict(status_data)
        except Exception:
            return None

        # Do not kick if not claiming done
        if not status.claims_done:
            return None

        # False finish detection: claiming done without running or passing tests
        if not status.tests_run or not status.tests_passed:
            return self.issue_kick(
                task_dir,
                stalled_location="untested_code",
                confidence=0.96,
                message="Code or state was changed but verification tests were not run or did not pass.",
            )

        return None

    def issue_kick(
        self,
        task_dir: Path,
        stalled_location: str,
        confidence: float,
        message: str,
    ) -> KickPayload:
        kicks_dir = task_dir / "kicks"
        kicks_dir.mkdir(parents=True, exist_ok=True)
        existing = list(kicks_dir.glob("kick_*.json"))
        kick_id = len(existing) + 1

        payload = KickPayload(
            kick_id=kick_id,
            task_id=task_dir.name,
            stalled_location=stalled_location,
            confidence=confidence,
            message=message,
            issued_at=now_iso(),
        )

        kick_file = kicks_dir / f"kick_{kick_id:03d}.json"
        kick_file.write_text(
            json.dumps(
                {
                    "kick_id": payload.kick_id,
                    "task_id": payload.task_id,
                    "stalled_location": payload.stalled_location,
                    "confidence": payload.confidence,
                    "message": payload.message,
                    "issued_at": payload.issued_at,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        log.warning(f"[{task_dir.name}] KICK #{kick_id} -> {stalled_location} (conf={confidence})")
        self.append_ledger({
            "event": "kick",
            "task_id": task_dir.name,
            "kick_id": kick_id,
            "stalled_location": stalled_location,
            "confidence": confidence,
        })
        return payload

    def append_ledger(self, record: Dict[str, Any]) -> None:
        ledger = self.config.ledger_file
        ledger.parent.mkdir(parents=True, exist_ok=True)
        payload = {"ts": now_iso(), "source": "jev_pacer", **record}
        with open(ledger, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
