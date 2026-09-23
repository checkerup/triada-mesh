"""Abstract interfaces for KeyPool and Jev Arbiter Providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class KeyPoolProvider(ABC):
    """Abstract base provider for obtaining and managing API keys for Jev Arbiter."""

    @abstractmethod
    def get_key(self) -> str:
        """Returns an active, unexhausted API key."""
        pass

    @abstractmethod
    def report_exhausted(self, key: str) -> None:
        """Reports an API key as exhausted (401/402/429) to trigger rotation/cooling."""
        pass

    @abstractmethod
    def available_keys_count(self) -> int:
        """Returns the number of currently available keys in the pool."""
        pass

    def refresh_pool(self) -> None:
        """Optional hook to trigger proactive pool replenishment."""
        pass
