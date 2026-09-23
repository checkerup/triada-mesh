# Protocol: Peer Supervision & Evidence-Based Verification

## Core Principle (Directive 1)
No reports without proofs. Every claim of "finished", "fixed", or "working" must be substantiated with live terminal outputs, exit codes, and non-empty files.

## Handover Verification Rules

Before a task is passed to the next Triada member:
1. `claims_done == true`
2. `tests_run == true` and `tests_passed == true` (exit code 0)
3. Zero unresolved kicks from Jev Watchdog
4. All artifacts physically exist on disk
5. A 15–30 second Windows file lock grace period must be observed by Relay Dispatcher before starting the next peer process.
