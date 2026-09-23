# Triada Mesh — Skills Catalog

This directory contains reusable Agent Skills that can be loaded into any Triada-compatible harness (Google Antigravity, Hermes Agent, OpenCode, Claude Code, Cursor, Windsurf).

## Available Skills

### 🏛️ `triada-council`
Universal autonomous council uniting **Mark (Antigravity)**, **Kat (Hermes)**, and **Nika (OpenCode)** under independent arbitration by **Jev (TypeSafe System One)**.
- **Triggers**: `консилиум триады`, `триада реши`, `триада консилиум`, `запусти консилиум`, `/triada-council`.
- **Modes**: Both coding tasks (test-driven diffs) and non-coding tasks (research, security audits, financial analysis, resource triage).

## Installation

### For Google Antigravity
Symlink or copy `skills/triada-council/` into your global or workspace skills folder:
```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.gemini\config\skills\triada-council" -Target "c:\ai_workflow\triada_mesh\skills\triada-council"
```

### For Hermes Agent
Symlink or copy into Hermes profile skills directory:
```powershell
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\hermes\skills\triada-council" -Target "c:\ai_workflow\triada_mesh\skills\triada-council"
```

### For OpenCode / Claude Code / Cursor
Reference `skills/triada-council/SKILL.md` directly in `AGENTS.md` or `.cursorrules` / `CLAUDE.md`.
