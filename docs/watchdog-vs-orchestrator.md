# Watchdog vs. Orchestrator: Decoupling Safety from Execution

In conventional multi-agent frameworks, task evaluation and process execution are bundled into a single monolithic loop. This causes catastrophic failure modes:
1. **Single Point of Failure**: If an agent process hangs or encounters a network error, the evaluator crashes with it.
2. **False Finish Hallucinations**: An LLM agent claiming "All tests passed, project finished" fools simple orchestrators that lack cold, external verification.
3. **Deadlocks**: Spawning background processes while holding file descriptors creates irreversible locks (especially on Windows).

## Triada's Decoupled Architecture

```
┌─────────────────────────────────┐
│     RelayDispatcher.py          │  ← Orchestrator:
│     (Process Spawning & Relay)  │    Spawns agents, enforces grace periods,
└────────────────┬────────────────┘    records handovers.
                 │
                 ▼
┌─────────────────────────────────┐
│        tasks/<id>/status.json   │  ← File-based decoupled interface
│        tasks/<id>/handover.json │
└────────────────▲────────────────┘
                 │
┌────────────────┴────────────────┐
│        jev_pacer.py             │  ← Watchdog (Observer):
│        (Cold Arbiter)           │    NEVER spawns agents. Only evaluates evidence
└─────────────────────────────────┘    vs. spec, issues kicks, and triggers kill-switch.
```

- **Jev Pacer (Watchdog)** is completely read-only with respect to processes. It queries TypeSafe Jev System One to evaluate `is_tz_satisfied` and `should_kick`. If an agent claims completion without passing tests, it immediately writes `kick_NNN.json`.
- **Relay Dispatcher** is completely read-only with respect to scoring. It simply checks if Jev has issued any unresolved kicks, verifies that tests exited with code 0, and handles agent invocation.

If Jev Pacer is terminated, the Relay Dispatcher still safely runs green tasks. If the Relay Dispatcher is terminated, Jev Pacer continues kicking incomplete work.
