# Triada Perpetual Relay Protocol

The Perpetual Relay Protocol governs the autonomous, round-robin handover of engineering tasks between Triada members:

$$\text{Mark (Antigravity)} \longrightarrow \text{Kat (Hermes)} \longrightarrow \text{Nika (OpenCode)} \longrightarrow \text{Mark (Antigravity)}$$

## Machine-Readable Handover Contract

Every transition generates a standardized `handover.json` file inside the task directory:

```json
{
  "handover_id": "handover_task_001_002",
  "task_id": "task_001",
  "from_agent": "mark",
  "to_agent": "kat",
  "iteration": 2,
  "git_base_sha": "a1b2c3d4",
  "artifacts": [
    "src/triada/config.py",
    "tests/test_config.py"
  ],
  "acceptance_criteria": [
    "Unit tests must pass with exit code 0",
    "No file descriptor leaks"
  ],
  "context_notes": "Mark completed config parser and unit tests. Kat must integrate with daemon_runner."
}
```

## Double Verification Standards

A task is NEVER dispatched to the next peer unless all five conditions are satisfied:
1. `claims_done == true`
2. `tests_run == true` AND `tests_passed == true` (exit code 0)
3. Zero unresolved kicks from Jev Watchdog (all kick files are older than the latest status update)
4. Every declared artifact physically exists on disk
5. Windows File-Lock Grace Period (15–30 seconds) is executed to allow background handles to close.
