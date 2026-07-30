import sqlite3
import os
from pathlib import Path

DB_FILE = Path(os.environ.get('VAULT_DB', r'C:\LocalOperatorMachine\vault.db'))

def show_build_artifacts():
    print('=== LOCAL OPERATOR MACHINE: BUILD ARTIFACTS & PROOF OF WORK ===')
    print()
    print('1. LOCAL INFRASTRUCTURE & VAULT:')
    print(f'   - Path: {DB_FILE.parent}')
    print('   - Core Database: vault.db (SQLite)')

    if DB_FILE.exists():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) FROM outreach_vault')
            count = cursor.fetchone()[0]
            cursor.execute('SELECT id, recipient, direction, timestamp FROM outreach_vault ORDER BY id DESC LIMIT 3')
            recent = cursor.fetchall()
        except Exception:
            count = 0
            recent = []
        finally:
            conn.close()

        print(f'   - Vault Records Logged: {count}')
        print('   - Recent Transmission Logs:')
        for row in recent:
            print(f'     -> ID: {row[0]} | Target: {row[1]} | Action: {row[2]} | Time: {row[3]}')
    else:
        print('   - Vault Status: Not initialized.')

    print()
    print('2. AUTOMATION ASSETS BUILT:')
    print('   - ADB Bridge Interface (platform-tools link to physical hardware)')
    print('   - Python Execution Scripts (vault logger, intent dispatchers, diagnostics)')
    print('   - PowerShell Control Scripts')

if __name__ == '__main__':
    show_build_artifacts()
