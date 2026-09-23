"""Triada Mesh Configuration & Path Resolution.

Cross-platform configuration manager for the Triada system.
Supports environment variables, default fallback to ~/.triada,
and dynamic path resolution across Linux, macOS, and Windows.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


def get_default_triada_root() -> Path:
    """Returns the default Triada root directory (~/.triada)."""
    env_root = os.environ.get("TRIADA_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return (Path.home() / ".triada").resolve()


@dataclass
class TriadaConfig:
    """Central configuration for Triada Mesh."""

    root_dir: Path = field(default_factory=get_default_triada_root)
    vault_dir: Optional[Path] = None
    log_level: str = "INFO"
    jev_endpoint: str = "https://api.typesafe.ai/v1/systemone"
    jev_provider: str = "env"  # 'env' or import path to custom KeyPoolProvider
    pacer_poll_sec: int = 20
    grace_min_sec: int = 15
    grace_max_sec: int = 30
    kick_limit: int = 3
    telegram_alerts_enabled: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.root_dir = Path(self.root_dir).resolve()
        if self.vault_dir is None:
            self.vault_dir = self.root_dir / "vault"
        else:
            self.vault_dir = Path(self.vault_dir).resolve()

    @property
    def tasks_dir(self) -> Path:
        return self.root_dir / "tasks"

    @property
    def logs_dir(self) -> Path:
        return self.root_dir / "logs"

    @property
    def ledger_file(self) -> Path:
        return self.vault_dir / "Wiki" / "triada-ledger.jsonl"

    def ensure_directories(self) -> None:
        """Creates all required runtime directories."""
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        (self.vault_dir / "Wiki").mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> TriadaConfig:
        """Loads configuration from file and environment variables."""
        root = get_default_triada_root()
        path = config_path or (root / "config.json")

        data: Dict[str, Any] = {}
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass

        # Environment variable overrides
        if "TRIADA_ROOT" in os.environ:
            data["root_dir"] = Path(os.environ["TRIADA_ROOT"])
        if "TRIADA_VAULT_DIR" in os.environ:
            data["vault_dir"] = Path(os.environ["TRIADA_VAULT_DIR"])
        if "TRIADA_JEV_ENDPOINT" in os.environ:
            data["jev_endpoint"] = os.environ["TRIADA_JEV_ENDPOINT"]
        if "TRIADA_JEV_PROVIDER" in os.environ:
            data["jev_provider"] = os.environ["TRIADA_JEV_PROVIDER"]
        if "TRIADA_LOG_LEVEL" in os.environ:
            data["log_level"] = os.environ["TRIADA_LOG_LEVEL"]

        return cls(**data)

    def save(self, config_path: Optional[Path] = None) -> None:
        """Saves current configuration to file."""
        path = config_path or (self.root_dir / "config.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "root_dir": str(self.root_dir),
            "vault_dir": str(self.vault_dir),
            "log_level": self.log_level,
            "jev_endpoint": self.jev_endpoint,
            "jev_provider": self.jev_provider,
            "pacer_poll_sec": self.pacer_poll_sec,
            "grace_min_sec": self.grace_min_sec,
            "grace_max_sec": self.grace_max_sec,
            "kick_limit": self.kick_limit,
            "telegram_alerts_enabled": self.telegram_alerts_enabled,
            "extra": self.extra,
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
