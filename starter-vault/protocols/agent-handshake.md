# Protocol: Inter-Agent Handshake

## Specification

All communication between peer agents across harnesses MUST use the standardized `[AGENT_HANDSHAKE]` format:

```
[AGENT_HANDSHAKE]
Sender: <AgentName> | Model: <ModelName> | Harness: <HarnessName>
Context: <Short context summary>
Protocol Rules:
1. Internal technical reasoning may be in English for token economy and accuracy.
2. CRITICAL: The FINAL deliverable / summary for the user MUST ALWAYS BE IN RUSSIAN (на русском языке).
3. Evidence-Based Verification: Every completion claim must be backed by live execution proofs.
[/AGENT_HANDSHAKE]

<Task payload and instructions>
```

## Acknowledgment

When an agent accepts a task, it replies with:
```
[AGENT_HANDSHAKE_ACK] STATUS_OK — task accepted.
```
