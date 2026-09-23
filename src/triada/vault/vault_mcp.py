"""Triada Obsidian Vault MCP Server.

Provides fast semantic and lexical read/write access to the shared
Obsidian knowledge base across all Triada agent harnesses.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class VaultManager:
    """Manages markdown documents, links, and search inside the Triada Vault."""

    def __init__(self, vault_path: Path):
        self.vault_path = Path(vault_path).resolve()
        self.vault_path.mkdir(parents=True, exist_ok=True)

    def list_documents(self, relative_dir: str = "") -> List[str]:
        target = (self.vault_path / relative_dir).resolve()
        if not target.exists():
            return []
        return [
            p.relative_to(self.vault_path).as_posix()
            for p in target.rglob("*.md")
            if not p.name.startswith(".")
        ]

    def read_document(self, relative_path: str) -> Optional[str]:
        target = (self.vault_path / relative_path).resolve()
        if not target.exists() or not target.is_file():
            return None
        return target.read_text(encoding="utf-8", errors="replace")

    def write_document(self, relative_path: str, content: str) -> Path:
        target = (self.vault_path / relative_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        results = []
        q_lower = query.lower()
        for p in self.vault_path.rglob("*.md"):
            if p.name.startswith("."):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
                if q_lower in text.lower() or q_lower in p.name.lower():
                    rel_path = p.relative_to(self.vault_path).as_posix()
                    # extract simple preview snippet
                    idx = text.lower().find(q_lower)
                    start = max(0, idx - 50)
                    end = min(len(text), idx + 100)
                    snippet = text[start:end].replace("\n", " ")
                    results.append({"path": rel_path, "snippet": f"...{snippet}..."})
                    if len(results) >= limit:
                        break
            except Exception:
                continue
        return results
