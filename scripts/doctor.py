"""Triada Environment Diagnostics & Health Check."""

from __future__ import annotations

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
from triada.pacer.pacer import load_provider


def doctor() -> int:
    print("=== Triada Doctor: Diagnostics ===")
    errors = 0

    # 1. Python version
    py_ver = sys.version_info
    print(f"[OK] Python version: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    if py_ver < (3, 9):
        print("  [ERROR] Triada requires Python >= 3.9")
        errors += 1

    # 2. Configuration & directories
    config = TriadaConfig.load()
    print(f"[OK] TRIADA_ROOT: {config.root_dir}")
    print(f"[OK] Vault directory: {config.vault_dir}")

    # 3. Provider check
    try:
        provider = load_provider(config.jev_provider)
        count = provider.available_keys_count()
        print(f"[OK] Provider '{config.jev_provider}' loaded. Active keys in pool: {count}")
    except Exception as e:
        print(f"[WARN] Provider check notice: {e}")

    # 4. Harness CLI tools availability
    hermes_cli = shutil.which("hermes")
    opencode_cli = shutil.which("opencode")

    if hermes_cli:
        print(f"[OK] Hermes CLI detected: {hermes_cli}")
    else:
        print("[INFO] Hermes CLI not found in PATH (will use local fallback or direct adapter)")

    if opencode_cli:
        print(f"[OK] OpenCode CLI detected: {opencode_cli}")
    else:
        print("[INFO] OpenCode CLI not found in PATH (will use scoop/shims fallback)")

    print(f"\nDiagnostics completed. Total errors: {errors}")
    return errors


if __name__ == "__main__":
    sys.exit(doctor())
