import subprocess
import os
import sqlite3
from datetime import datetime

ADB_EXE = os.environ.get('ADB_EXE', r'C:\LocalOperatorMachine\tools\platform-tools\adb.exe')
DB_FILE = os.environ.get('VAULT_DB', r'C:\LocalOperatorMachine\vault.db')
TEST_NUMBER = os.environ.get('TEST_NUMBER', 'REPLACE_WITH_TEST_NUMBER')
TEST_MESSAGE = os.environ.get('TEST_MESSAGE', 'Local Operator Machine: Live message dispatch confirmation test.')
DRY_RUN = os.environ.get('DRY_RUN', 'true').lower() in ('1', 'true', 'yes')

try:
    import db_init
except Exception:
    db_init = None


def send_and_verify():
    print('=== LIVE MESSAGE DISPATCH & VERIFICATION ===')

    # Initialize DB schema if available
    if db_init is not None:
        try:
            db_init.init_db()
        except Exception as e:
            print('[!] Failed to initialize DB schema:', e)

    # 1. Trigger intent
    if DRY_RUN:
        print('[*] DRY_RUN enabled — not sending an actual message. Intended target:', TEST_NUMBER)
    else:
        cmd = [
            ADB_EXE, 'shell', 'am', 'start', '-a', 'android.intent.action.SENDTO',
            '-d', f'smsto:{TEST_NUMBER}',
            '--es', 'sms_body', TEST_MESSAGE,
            '--ez', 'exit_on_sent', 'true'
        ]
        subprocess.run(cmd, capture_output=True)
        subprocess.run([ADB_EXE, 'shell', 'input', 'keyevent', '66'], capture_output=True)

    # 2. Log transmission
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS outreach_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT NOT NULL,
            direction TEXT,
            message TEXT,
            tone TEXT,
            thought TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO outreach_vault (recipient, direction, message, tone, thought, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (TEST_NUMBER, 'LIVE_CONFIRMATION_DISPATCH', TEST_MESSAGE, 'Verification Test', 'Live confirmation test sent to target device (dry-run may be enabled).', str(datetime.now())))
    conn.commit()
    conn.close()

    print('[√] Message intent fired (or skipped in dry-run) and logged to vault.')

if __name__ == '__main__':
    send_and_verify()
