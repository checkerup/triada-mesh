# Connecting External Harnesses to Triada

> **Integration Guide for Claude Code, Cursor, Cline, Roo Code, Aider, OpenHands & Custom Agents**

Triada is designed from the ground up as an open, harness-agnostic orchestration ecosystem. While the canonical triad consists of **Mark (Antigravity)**, **Kat (Hermes)**, and **Nika (OpenCode)**, any AI coding agent can participate.

---

## 3 Tiers of Integration

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: Native MCP Client (Claude Code, Cursor, Cline, OpenHands)      │
│ - Connects in 5 minutes via standard JSON config.                     │
│ - Instant access to Obsidian Vault and peer cross-consultation.        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ TIER 2: Bi-Directional Adapter (src/triada/adapters/)                  │
│ - 100–150 lines of Python. Allows Triada to launch & supervise agents. │
│ - Participates fully in the automated round-robin relay cycle.         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ TIER 3: Universal File-based Git Watchdog (Aider, Shell, Python)       │
│ - No MCP required. Communicates via tasks/<id>/status.json & git diff. │
│ - Jev Watchdog arbitrates work and kicks false finishes cold.          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Tier 1: Instant MCP Connection (Claude Code, Cursor, Cline)

Any environment supporting the **Model Context Protocol (MCP)** can connect to Triada out-of-the-box.

### 1. Claude Code
Add Triada to Claude Code's MCP configuration:
```bash
claude mcp add triada-mesh python -m triada.mesh.server
```
Or in `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "triada-mesh": {
      "command": "python",
      "args": ["-m", "triada.mesh.server"],
      "env": {
        "TRIADA_ROOT": "~/.triada"
      }
    }
  }
}
```

### 2. Cursor
In your project's `.cursor/mcp.json` or global Cursor settings:
```json
{
  "mcpServers": {
    "triada-mesh": {
      "command": "python",
      "args": ["-m", "triada.mesh.server"]
    }
  }
}
```

### 3. Cline / Roo Code (VS Code Extension)
In `cline_mcp_settings.json`:
```json
{
  "mcpServers": {
    "triada-mesh": {
      "command": "python",
      "args": ["-m", "triada.mesh.server"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### What Tier 1 Gives Your Agent:
- `vault_search(query)` & `vault_read(path)`: Full read access to the shared Obsidian Vault (ADRs, design docs).
- `vault_write(path, content)`: Document decisions and architectural updates.
- `peer_consult(target_harness, prompt)`: Consult peer agents running other models (e.g. ask Mark or Kat for a second opinion).

---

## Tier 2: Bi-Directional Relay Adapter

To allow Triada's `RelayDispatcher` to automatically hand over tasks to an external harness (e.g. `Mark -> Claude Code -> Kat`):

1. Create a module in `src/triada/adapters/<harness>_adapter.py`:
```python
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

def run_session_prompt(
    prompt: str,
    workdir: Path,
    session_id: Optional[str] = None,
    timeout: int = 1800,
) -> Dict[str, Any]:
    # Example for Claude Code CLI:
    cmd = ["claude", "-p", prompt]
    proc = subprocess.run(
        cmd,
        cwd=workdir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )
    return {
        "harness": "claude_code",
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "success": proc.returncode == 0,
    }
```

2. Register the agent in `src/triada/relay/dispatcher.py`:
```python
RELAY_CYCLE = ["mark", "claude_code", "kat", "nika"]
```

---

## Tier 3: Universal File-based Git Watchdog (Aider, Scripts, Custom Agents)

For CLI tools without MCP clients (such as **Aider**):

1. **Task registration**: The task is defined in `~/.triada/tasks/<task_id>/task.json`.
2. **Execution**:
   ```bash
   aider --message "Read ~/.triada/tasks/task_001/task.json and implement the solution. Run all tests before finishing."
   ```
3. **Status Reporting**: The agent or wrapper writes `status.json`:
   ```json
   {
     "agent": "aider",
     "task_id": "task_001",
     "claims_done": true,
     "tests_run": true,
     "tests_passed": true,
     "artifacts": ["src/feature.py", "tests/test_feature.py"]
   }
   ```
4. **Watchdog Verification**:
   - `jev_pacer.py` monitors the task directory.
   - It performs an independent `git diff` against `base_sha.txt` and evaluates whether the specification was actually satisfied.
   - If Aider hallucinated completion without working tests, Jev writes `kicks/kick_001.json` with the exact defective code location.
