"""Triada Mesh Setup & Installation Script.

Initializes ~/.triada runtime directories, deploys starter-vault,
and sets up initial configuration.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# Add src to path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from triada.config import TriadaConfig, get_default_triada_root


def install() -> None:
    print("=== Triada Mesh Installation ===")
    root = get_default_triada_root()
    print(f"Target TRIADA_ROOT: {root}")

    config = TriadaConfig(root_dir=root)
    config.ensure_directories()
    print("Runtime directories created:")
    print(f"  - Tasks: {config.tasks_dir}")
    print(f"  - Logs:  {config.logs_dir}")
    print(f"  - Vault: {config.vault_dir}")

    # Deploy starter vault if empty
    starter_vault = REPO_ROOT / "starter-vault"
    if starter_vault.exists():
        for item in starter_vault.iterdir():
            target = config.vault_dir / item.name
            if not target.exists():
                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
        print("Deployed starter-vault templates to vault directory.")

    # Save initial config if not existing
    cfg_file = root / "config.json"
    if not cfg_file.exists():
        config.save(cfg_file)
        print(f"Saved default configuration to {cfg_file}")

    print("\nInstallation complete! Run 'python scripts/doctor.py' to verify.")


if __name__ == "__main__":
    install()
