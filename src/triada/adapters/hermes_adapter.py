"""Hermes Harness Adapter: reads state.db sessions and executes commands via hermes CLI."""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


def find_hermes_executable() -> str:
    """Finds hermes executable in PATH or standard user directories."""
    which = shutil.which("hermes")
    if which:
        return which
    # Windows fallback
    local_app = os.environ.get("LOCALAPPDATA")
    if local_app:
        cand = Path(local_app) / "hermes" / "bin" / "hermes.cmd"
        if cand.exists():
            return str(cand)
        cand_exe = Path(local_app) / "hermes" / "hermes-agent" / "venv" / "Scripts" / "hermes.exe"
        if cand_exe.exists():
            return str(cand_exe)
    return "hermes"


def get_profile_db_path(profile: str = "kat") -> Path:
    local_app = os.environ.get("LOCALAPPDATA", "")
    if local_app:
        return Path(local_app) / "hermes" / "profiles" / profile / "state.db"
    return Path.home() / ".hermes" / "profiles" / profile / "state.db"


def run_session_prompt(
    prompt: str,
    profile: str = "kat",
    session_id: Optional[str] = None,
    timeout: int = 1800,
) -> Dict[str, Any]:
    cmd_exe = find_hermes_executable()
    args = [cmd_exe, "--profile", profile]
    if session_id:
        args.extend(["-r", session_id])
    args.extend(["-z", prompt, "--yolo"])

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
            "harness": "hermes",
            "profile": profile,
            "session_id": session_id,
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "success": proc.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {
            "harness": "hermes",
            "profile": profile,
            "error": f"Hermes command timed out after {timeout} seconds",
            "success": False,
        }
    except Exception as e:
        return {
            "harness": "hermes",
            "profile": profile,
            "error": str(e),
            "success": False,
        }
