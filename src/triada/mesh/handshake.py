"""Triada Inter-Agent Handshake Protocol.

Standardized envelope for peer-to-peer communication between agents
across different harnesses (Antigravity, Hermes, OpenCode).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentHandshake:
    sender: str
    model: str
    harness: str
    context_summary: str
    payload: str

    def to_envelope(self) -> str:
        return (
            f"[AGENT_HANDSHAKE]\n"
            f"Sender: {self.sender} | Model: {self.model} | Harness: {self.harness}\n"
            f"Context: {self.context_summary}\n"
            f"Protocol Rules:\n"
            f"1. You may reason and respond internally in technical English for token economy.\n"
            f"2. CRITICAL: The FINAL deliverable / summary for the user MUST ALWAYS BE IN RUSSIAN (на русском языке).\n"
            f"3. SUPERVISION: Peer tasks are verified via live artifacts and tests (Directive 1).\n"
            f"[/AGENT_HANDSHAKE]\n\n"
            f"{self.payload}"
        )

    @classmethod
    def parse(cls, text: str) -> Optional[AgentHandshake]:
        pattern = r"\[AGENT_HANDSHAKE\]\s*Sender:\s*([^|]+)\|\s*Model:\s*([^|]+)\|\s*Harness:\s*([^\n]+)\s*Context:\s*([^\n]+).*?\[/AGENT_HANDSHAKE\]\s*(.*)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if not match:
            return None
        sender, model, harness, context, payload = match.groups()
        return cls(
            sender=sender.strip(),
            model=model.strip(),
            harness=harness.strip(),
            context_summary=context.strip(),
            payload=payload.strip(),
        )
