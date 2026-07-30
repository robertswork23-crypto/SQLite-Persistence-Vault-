import subprocess
import os
from pathlib import Path

REPO_DIR = Path(os.environ.get('REPO_DIR', r'C:\LocalOperatorMachine'))
REMOTE_URL = os.environ.get('REMOTE_URL', 'https://github.com/robertswork23-crypto/SQLite-Persistence-Vault-.git')


def run(cmd, **kwargs):
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    return result


def ensure_remote():
    cwd = os.getcwd()
    try:
        os.chdir(REPO_DIR)
        remotes = run(['git', 'remote'])
        if 'origin' not in remotes.stdout.splitlines():
            print("[*] No 'origin' remote found. Adding it now.")
            add = run(['git', 'remote', 'add', 'origin', REMOTE_URL])
            if add.returncode != 0:
                print("[!] Failed to add remote:", add.stderr.strip())
                return False
        else:
            print("[*] 'origin' remote already configured.")
        return True
    finally:
        os.chdir(cwd)


def push():
    if not ensure_remote():
        return
    print("[*] Staging files...")
    cwd = os.getcwd()
    try:
        os.chdir(REPO_DIR)
        run(['git', 'add', '.'])
        commit = run(['git', 'commit', '-m', 'Update: Local Operator Machine functional builds and logs'])
        if commit.returncode != 0 and 'nothing to commit' in (commit.stderr + commit.stdout).lower():
            print("[*] No changes to commit.")
        else:
            print("[+] Commit result:", (commit.stdout or commit.stderr).strip())
        confirm = os.environ.get('AUTO_PUSH', 'no').lower()
        if confirm == 'yes':
            push_result = run(['git', 'push', '-u', 'origin', 'main'])
            if push_result.returncode == 0:
                print("[+] Successfully pushed.")
            else:
                print("[!] Push failed:", push_result.stderr.strip())
        else:
            print("[*] AUTO_PUSH not enabled. Set AUTO_PUSH=yes environment variable to push automatically.")
    finally:
        os.chdir(cwd)


if __name__ == '__main__':
    push()
