# Triada Mesh

> **Autonomous Multi-Agent Relay, Watchdog Arbiter & Cross-Harness Knowledge Mesh**  
> *Connecting Google Antigravity, Hermes Agent, and OpenCode into an unstoppable, self-verifying engineering triad.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Multi-Harness](https://img.shields.io/badge/Harness-Antigravity%20%7C%20Hermes%20%7C%20OpenCode-blueviolet)](docs/architecture.md)

[**Русская версия (README.ru.md)**](README.ru.md) | [**中文版 (README.zh.md)**](README.zh.md)

---

## What is Triada?

Triada is an open-source decentralized agent orchestration engine built around a simple principle: **no single AI model or harness should work in isolation**.

By uniting three premier agent environments with diverse cognitive models, Triada eliminates single-model blind spots, halts collective hallucinations, and ensures continuous, evidence-based engineering execution.

```
                      ┌──────────────────────────────────────┐
                      │        Obsidian Knowledge Mesh       │
                      │        (Vault MCP Server)            │
                      └──────────────────┬───────────────────┘
                                         │ Shared Context & ADRs
                                         ▼
┌──────────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│  Mark (Antigravity)  │◄─────►│    Kat (Hermes)      │◄─────►│    Nika (OpenCode)   │
│  - Architecture      │       │  - Server Daemons    │       │  - Diff Surgery      │
│  - Task Specs        │       │  - Integration Tests │       │  - Code Optimization │
│  - Imagen Assets     │       │  - Linux SSH Bridge  │       │  - Edge-Case Tests   │
│  - Top Reasoning     │       │  - Server Reasoning  │       │  - High-Speed Code   │
└──────────┬───────────┘       └──────────┬───────────┘       └──────────┬───────────┘
           │                              │                              │
           └──────────────────────────────┼──────────────────────────────┘
                                          │
                                          ▼
                      ┌──────────────────────────────────────┐
                      │    Jev Pacer & Relay Dispatcher      │
                      │  - Watchdog (Anti-False Finish)      │
                      │  - Automated Relay Handover          │
                      │  - Double Verification Gate          │
                      └──────────────────────────────────────┘
```

---

## Core Pillars

### 1. Multi-Harness Cognitive Tiering
Rather than restricting all agents to a single model family, Triada enforces model diversity:
- **Mark (Antigravity)**: Reasoning & Architecture flagship (Gemini 2.5 Pro / Claude 3.7 Sonnet).
- **Kat (Hermes)**: Persistent Server Daemons & Autonomous Execution (Moonshot Kimi K3 / DeepSeek R1).
- **Nika (OpenCode)**: High-speed Diff Surgery & Code Optimization (GLM-5.2 / Qwen Coder).

### 2. Jev Pacer Watchdog (Anti-False Finish)
Large language models tend to suffer from "False Finish" — claiming tasks are complete when code is untested or broken. Jev Pacer is an independent watchdog daemon backed by TypeSafe Jev System One probability scoring. It continuously cross-checks git diffs and test exit codes against the original task specification. If an agent tries to exit prematurely, Jev issues a targeted corrective **kick**.

### 3. Autonomous Relay Dispatcher
The Relay Dispatcher executes a round-robin relay across the Triada (`Mark -> Kat -> Nika -> Mark`). It implements **Double Verification** (requiring passed tests, non-empty artifacts, and resolved kicks) and an automated **Windows file-lock grace period** (15–30s) to prevent lock collisions.

### 4. Obsidian Knowledge Mesh (Vault MCP)
A shared Obsidian Vault gives all agents a persistent, human-readable second brain for Architecture Decision Records (ADRs), peer supervision logs, and cross-session memory.

---

## Quickstart

### Prerequisites
- Python 3.9+
- Git

### Installation
```bash
git clone https://github.com/checkerup/triada-mesh.git
cd triada-mesh
python scripts/install.py
```

### Run Diagnostics
```bash
python scripts/doctor.py
```

### Configure Credentials
Copy `.env.example` to `.env` and provide your Jev API key:
```bash
cp .env.example .env
# Edit .env to set TRIADA_JEV_API_KEY
```

### Run the Test Suite
```bash
python tests/run_tests.py
```

---

## Pluggable KeyPool Architecture

Triada cleanly separates core orchestration from credential sources:
- **Built-in (`env`)**: Reads keys directly from `TRIADA_JEV_API_KEY` (supports multiple comma-separated keys with automatic rotation).
- **Custom / Private Farms**: You can plug in any private credential farm or dynamic key-generation service by implementing the abstract `KeyPoolProvider` interface. The public repository remains completely free of proprietary harvesting code. See [src/triada/providers/README.md](src/triada/providers/README.md).

---

## Autonomous Triada Council Skill (`triada-council`)

Triada Mesh includes a pre-configured, cross-harness skill in [`skills/triada-council/`](skills/triada-council/):
- **Natural Language Auto-Dispatch**: Triggers automatically on `консилиум триады`, `триада реши`, `запусти консилиум`, or `/triada-council`.
- **Session Archaeological Ingestion**: Pass any past session ID (e.g. `20260923_023804_05b757`), and the system will automatically parse past chat history directly from SQLite/transcripts, isolate unsolved dilemmas, and convene the council.
- **Cognitive Triad & Jev Arbitration**:
  - **Mark (Antigravity)**: Strategic synthesis & architectural roadmaps.
  - **Kat (Hermes)**: Empirical verification, server daemons, live testing.
  - **Nika (OpenCode)**: Diff surgery, risk audit, logical critique.
  - **Jev (TypeSafe System One)**: Independent judge and arbiter verifying deliverables against specifications.
- **Anti-Substitution Lock**: Strictly forbids agents from replacing the external 3-agent council with internal local subagents, guaranteeing true cognitive diversity.

---

## Supporting External Harnesses (Claude Code, Cursor, Cline, Aider)

Triada is completely harness-agnostic. Any AI coding tool can connect through 3 flexible tiers:

1. **Tier 1 (Instant MCP)**: **Claude Code, Cursor, Cline, Roo Code, OpenHands** connect in 5 minutes via standard JSON config (`python -m triada.mesh.server`), gaining immediate read/write access to the Obsidian Vault and peer cross-consultation.
2. **Tier 2 (Relay Adapter)**: Full bi-directional participation in the autonomous round-robin relay cycle (`Mark -> Claude Code -> Kat`) via modular adapters in `src/triada/adapters/`.
3. **Tier 3 (Git Watchdog)**: Non-MCP tools like **Aider** or custom Python scripts interact through `tasks/<id>/status.json` and git diffs under Jev Pacer supervision.

📖 **Full Step-by-Step Guide & Configs**: [docs/external-harnesses.md](docs/external-harnesses.md)

---

## License

MIT License. See [LICENSE](LICENSE) for details.

