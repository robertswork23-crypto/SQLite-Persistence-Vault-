import sqlite3
import os
from pathlib import Path

DB_FILE = Path(os.environ.get('VAULT_DB', r'C:\LocalOperatorMachine\vault.db'))

SCHEMA = """
CREATE TABLE IF NOT EXISTS outreach_vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient TEXT NOT NULL,
    direction TEXT,
    message TEXT,
    tone TEXT,
    thought TEXT,
    timestamp TEXT
);
"""

def init_db():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.cursor()
        cursor.executescript(SCHEMA)
        conn.commit()
        print(f"[+] Database initialized at: {DB_FILE}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
