"""Default Environment-based KeyPoolProvider for Triada."""

from __future__ import annotations

import os
from typing import List, Set

from .base import KeyPoolProvider


class EnvKeyPoolProvider(KeyPoolProvider):
    """Provides API keys loaded from the environment variable TRIADA_JEV_API_KEY.

    Multiple keys can be supplied as a comma-separated list.
    """

    def __init__(self, env_var: str = "TRIADA_JEV_API_KEY"):
        self.env_var = env_var
        raw = os.environ.get(env_var, "").strip()
        self._keys: List[str] = [k.strip() for k in raw.split(",") if k.strip()]
        self._exhausted: Set[str] = set()
        self._index: int = 0

    def get_key(self) -> str:
        active = [k for k in self._keys if k not in self._exhausted]
        if not active:
            if not self._keys:
                raise RuntimeError(
                    f"No API keys configured. Please set the {self.env_var} environment variable."
                )
            # If all were marked exhausted, reset cooling and retry
            self._exhausted.clear()
            active = list(self._keys)

        key = active[self._index % len(active)]
        self._index += 1
        return key

    def report_exhausted(self, key: str) -> None:
        self._exhausted.add(key)

    def available_keys_count(self) -> int:
        return len([k for k in self._keys if k not in self._exhausted])
