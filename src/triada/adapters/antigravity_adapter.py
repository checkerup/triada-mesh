"""Antigravity Harness Adapter: manages Antigravity sessions and notifications."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


def find_agentapi_executable() -> Optional[str]:
    which = shutil.which("agentapi")
    if which:
        return which
    user_home = Path.home()
    cand = user_home / ".gemini" / "antigravity" / "bin" / "agentapi.bat"
    if cand.exists():
        return str(cand)
    return None


def run_session_prompt(
    prompt: str,
    session_id: Optional[str] = None,
    title: Optional[str] = None,
    timeout: int = 300,
) -> Dict[str, Any]:
    agentapi = find_agentapi_executable()
    if not agentapi:
        # Fallback notification mode
        return {
            "harness": "antigravity",
            "success": True,
            "mode": "queued_notification",
            "message": "Task queued for Antigravity in Triada ledger / tasks directory.",
        }

    args = [agentapi]
    if session_id:
        args.extend(["send-message", session_id, prompt])
    else:
        args.append("new-conversation")
        if title:
            args.extend(["--title", title])
        args.append(prompt)

    try:
        proc = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return {
            "harness": "antigravity",
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "success": proc.returncode == 0,
        }
    except Exception as e:
        return {
            "harness": "antigravity",
            "error": str(e),
            "success": False,
        }
