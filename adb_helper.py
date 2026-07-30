import subprocess
from pathlib import Path
import os

ADB_EXE = Path(os.environ.get('ADB_EXE', r'C:\LocalOperatorMachine\tools\platform-tools\adb.exe'))


def adb_run(args, check=True):
    cmd = [str(ADB_EXE)] + list(args)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise RuntimeError(f"ADB command failed: {proc.stderr.strip()}")
    return proc.stdout, proc.stderr


if __name__ == '__main__':
    try:
        out, err = adb_run(['devices'], check=False)
        print(out)
    except Exception as e:
        print('[!] adb helper error:', e)
