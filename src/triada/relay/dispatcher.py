"""Triada Autonomous Relay Dispatcher.

Orchestrates handovers across the Triada cycle (mark -> kat -> nika -> mark).
Enforces Double Verification and Windows file lock grace periods.
"""

from __future__ import annotations

import json
import logging
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from triada.adapters import antigravity_adapter, hermes_adapter, opencode_adapter
from triada.config import TriadaConfig
from triada.relay.protocol import HandoverPackage

log = logging.getLogger("triada.relay.dispatcher")

RELAY_CYCLE = ["mark", "kat", "nika"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class RelayDispatcher:
    """Evaluates task completion conditions and triggers the next peer agent in the Triada cycle."""

    def __init__(self, config: TriadaConfig):
        self.config = config

    def next_agent_in_cycle(self, current_agent: str) -> str:
        cur = current_agent.lower().strip()
        if cur not in RELAY_CYCLE:
            raise ValueError(f"Unknown agent: '{current_agent}'. Expected one of {RELAY_CYCLE}")
        idx = RELAY_CYCLE.index(cur)
        return RELAY_CYCLE[(idx + 1) % len(RELAY_CYCLE)]

    def check_active_kicks(self, task_dir: Path, status_mtime: float) -> List[Dict[str, Any]]:
        """A kick is active if its file modification time is newer than the last status.json update."""
        kicks_dir = task_dir / "kicks"
        if not kicks_dir.exists():
            return []
        active = []
        for kf in kicks_dir.glob("kick_*.json"):
            if kf.stat().st_mtime >= status_mtime - 1.0:
                try:
                    data = json.loads(kf.read_text(encoding="utf-8"))
                    active.append({
                        "file": kf.name,
                        "stalled_location": data.get("stalled_location", "unknown"),
                    })
                except Exception:
                    active.append({"file": kf.name, "stalled_location": "unparsed"})
        return active

    def check_artifacts_present(self, workdir: Path, artifacts: List[str]) -> Tuple[bool, List[str]]:
        missing = []
        for art in artifacts:
            p = Path(art)
            if not p.is_absolute():
                p = workdir / art
            if not p.exists():
                missing.append(art)
        return len(missing) == 0, missing

    def validate_for_handover(self, task_dir: Path) -> Tuple[bool, List[str], Dict[str, Any]]:
        status_file = task_dir / "status.json"
        if not status_file.exists():
            return False, ["status.json missing"], {}

        status_mtime = status_file.stat().st_mtime
        try:
            status = json.loads(status_file.read_text(encoding="utf-8"))
        except Exception as e:
            return False, [f"status.json unreadable: {e}"], {}

        reasons = []
        if not status.get("claims_done", False):
            reasons.append("claims_done is not True")
        if not status.get("tests_run", False):
            reasons.append("tests_run is not True")
        if not status.get("tests_passed", False):
            reasons.append("tests_passed is not True")

        # Check kicks
        active_kicks = self.check_active_kicks(task_dir, status_mtime)
        if active_kicks:
            reasons.append(f"active unresolved kicks: {active_kicks}")

        # Check workdir & artifacts
        workdir_file = task_dir / "workdir.txt"
        workdir = task_dir
        if workdir_file.exists():
            try:
                workdir = Path(workdir_file.read_text(encoding="utf-8").strip())
            except Exception:
                pass

        artifacts = status.get("artifacts", [])
        task_json = task_dir / "task.json"
        if task_json.exists():
            try:
                tdata = json.loads(task_json.read_text(encoding="utf-8"))
                artifacts.extend(tdata.get("artifacts", []))
            except Exception:
                pass

        ok, missing = self.check_artifacts_present(workdir, list(set(artifacts)))
        if not ok:
            reasons.append(f"missing physical artifacts: {missing}")

        return len(reasons) == 0, reasons, status

    def append_ledger(self, event_data: Dict[str, Any]) -> None:
        ledger = self.config.ledger_file
        ledger.parent.mkdir(parents=True, exist_ok=True)
        record = {"ts": now_iso(), "source": "relay_dispatcher", **event_data}
        with open(ledger, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def process_task(self, task_dir: Path, dry_run: bool = False) -> Dict[str, Any]:
        task_id = task_dir.name
        can_handover, reasons, status = self.validate_for_handover(task_dir)

        if not can_handover:
            log.info(f"[{task_id}] Handover blocked: {reasons}")
            self.append_ledger({
                "event": "handover_blocked",
                "task_id": task_id,
                "agent": status.get("agent", "unknown"),
                "reasons": reasons,
            })
            return {"status": "blocked", "reasons": reasons}

        from_agent = status.get("agent", "mark").lower()
        next_agent = self.next_agent_in_cycle(from_agent)
        iteration = status.get("iteration", 1) + 1

        workdir = task_dir
        workdir_file = task_dir / "workdir.txt"
        if workdir_file.exists():
            workdir = Path(workdir_file.read_text(encoding="utf-8").strip())

        base_sha = ""
        base_file = task_dir / "base_sha.txt"
        if base_file.exists():
            base_sha = base_file.read_text(encoding="utf-8").strip()

        handover = HandoverPackage(
            handover_id=f"handover_{task_id}_{iteration:03d}",
            task_id=task_id,
            from_agent=from_agent,
            to_agent=next_agent,
            iteration=iteration,
            git_base_sha=base_sha,
            artifacts=status.get("artifacts", []),
            acceptance_criteria=[
                "Verification tests must be implemented and passing (exit code 0)",
                "No regressions against base_sha",
            ],
            context_notes=status.get("last_output_tail", ""),
        )

        handover_file = task_dir / "handover.json"
        handover.save(handover_file)
        log.info(f"[{task_id}] Handover saved: {from_agent} -> {next_agent} (iter {iteration})")

        # Grace period for Windows file locks
        if not dry_run:
            grace = random.uniform(self.config.grace_min_sec, self.config.grace_max_sec)
            log.info(f"[{task_id}] Grace period: sleeping {grace:.1f}s for lock release...")
            time.sleep(grace)

        # Dispatch next agent
        dispatch_result = self.dispatch_agent(next_agent, task_id, workdir, handover_file, dry_run)

        self.append_ledger({
            "event": "handover_dispatched",
            "task_id": task_id,
            "from_agent": from_agent,
            "to_agent": next_agent,
            "iteration": iteration,
            "dry_run": dry_run,
            "dispatch": dispatch_result,
        })

        return {
            "status": "dispatched",
            "from_agent": from_agent,
            "to_agent": next_agent,
            "iteration": iteration,
            "dispatch": dispatch_result,
        }

    def dispatch_agent(
        self,
        agent: str,
        task_id: str,
        workdir: Path,
        handover_file: Path,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        prompt = (
            f"[AGENT_HANDSHAKE] Relay handover for task {task_id}: "
            f"read {handover_file.as_posix()} and execute iteration."
        )

        if dry_run:
            return {"agent": agent, "dry_run": True, "prompt": prompt}

        if agent == "kat":
            return hermes_adapter.run_session_prompt(prompt, profile="kat")
        elif agent == "nika":
            return opencode_adapter.run_session_prompt(prompt, workdir=workdir)
        elif agent == "mark":
            return antigravity_adapter.run_session_prompt(prompt, title=f"Relay: {task_id}")
        else:
            raise ValueError(f"Unknown target agent: {agent}")
