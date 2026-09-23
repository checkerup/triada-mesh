"""OpenCode Harness Adapter: reads opencode.db and executes via opencode CLI.

CRITICAL REQUIREMENT: Always executes with an explicit --dir parameter
to prevent directory indexing hangs on Windows.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


def find_opencode_executable() -> str:
    which = shutil.which("opencode")
    if which:
        return which
    user_home = Path.home()
    scoop_shim = user_home / "scoop" / "shims" / "opencode.exe"
    if scoop_shim.exists():
        return str(scoop_shim)
    return "opencode"


def get_opencode_db_path() -> Path:
    return Path.home() / ".local" / "share" / "opencode" / "opencode.db"


def run_session_prompt(
    prompt: str,
    workdir: Path,
    session_id: Optional[str] = None,
    model: Optional[str] = None,
    timeout: int = 1800,
) -> Dict[str, Any]:
    cmd_exe = find_opencode_executable()
    workdir_path = Path(workdir).resolve()
    if not workdir_path.exists():
        return {
            "harness": "opencode",
            "error": f"Work directory {workdir_path} does not exist",
            "success": False,
        }

    args = [cmd_exe, "run", "--auto", "--dir", str(workdir_path)]
    if session_id:
        args.extend(["--session", session_id])
    if model:
        args.extend(["-m", model])
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
            "harness": "opencode",
            "workdir": str(workdir_path),
            "session_id": session_id,
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "success": proc.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {
            "harness": "opencode",
            "error": f"OpenCode timed out after {timeout} seconds",
            "success": False,
        }
    except Exception as e:
        return {
            "harness": "opencode",
            "error": str(e),
            "success": False,
        }
