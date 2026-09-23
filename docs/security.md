# Security Architecture & Zero Secret Exposure (Directive 9)

Triada enforces a strict Zero Secret Exposure policy across all repositories and agent workflows.

## Security Guarantees
1. **Isolated Key Providers**: Private API token harvesting, dynamic credential farms, and auto-registration scripts are strictly banned from the main repository. They are maintained in separate, private repositories and plugged into Triada via the abstract `KeyPoolProvider` interface.
2. **Git Hygiene**:
   - SQLite databases (`*.db`, `*.sqlite`, `state.db`, `opencode.db`), session cookies, and runtime logs are strictly ignored by `.gitignore`.
   - All credentials and sensitive tokens must be specified via environment variables (`.env`) and never committed.
   - Every release is verified using pre-push secret scanners (Gitleaks / TruffleHog).
3. **Decoupled Vault Templates**:
   - `starter-vault` contains only empty markdown schemas and protocols.
   - User notes, financial accounts, private research, and operational data are strictly excluded via an explicit file whitelist.
