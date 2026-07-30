# Local Operator Machine: SQLite Persistence Vault & Automation Suite

## Overview
This project contains tools and scripts used to manage a local SQLite "vault" database and helper scripts that interact with an Android device via ADB. It is intended for authorized testing and verification only.

IMPORTANT: Do not use these tools to send messages to real recipients without explicit, documented consent. By default scripts are configured with placeholders and dry-run safeguards.

---

## Quick setup
1. Install Python 3.8+ on your machine.
2. If you plan to run ADB-based scripts, install platform-tools and set the `ADB_EXE` environment variable, e.g.:

   - Windows (Powershell):
     $env:ADB_EXE = 'C:\LocalOperatorMachine\tools\platform-tools\adb.exe'

3. Optionally set these environment variables to customize behavior:

   - VAULT_DB: path to the SQLite DB (default: C:\LocalOperatorMachine\vault.db)
   - ADB_EXE: path to adb executable
   - REPO_DIR: path to your local repo directory (used by push_safe.py)
   - REMOTE_URL: remote Git URL if you want to configure a remote
   - AUTO_PUSH: set to `yes` to allow push_safe.py to push automatically (use with caution)
   - TEST_NUMBER / TARGET_NUMBER: set to a test phone number for dry-run testing (do not use real numbers)
   - DRY_RUN: set to `true` (default) to prevent scripts from actually invoking ADB send operations

4. Initialize the database schema:

    python db_init.py

5. Run checks and dry-run tests before enabling AUTO_PUSH or disabling DRY_RUN.

---

## Files added/updated in this commit
- db_init.py: Initializes the SQLite schema safely if not present.
- push_safe.py: Safer git push helper that does not remove remotes and requires AUTO_PUSH=yes to push.
- adb_helper.py: Small wrapper for invoking adb with error handling.
- .gitignore: Ignores local DB and platform tools, editor files.
- Updated build_summary.py, sms_diagnostic.py, test_confirm.py to use environment variables and dry-run defaults.

---

## Safety & Legal Notes
Automated messaging to real recipients can be illegal or violate terms of service. Use only for authorized testing on devices you own or manage. Replace placeholder numbers with test numbers and keep `DRY_RUN=true` until you have explicit authorization.

If you want this repository made public, please confirm via the GitHub web UI or instruct me to change repository visibility (this operation requires an explicit API call and appropriate permissions).
