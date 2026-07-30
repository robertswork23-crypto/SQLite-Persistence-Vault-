import subprocess
import os

ADB_EXE = os.environ.get('ADB_EXE', r'C:\LocalOperatorMachine\tools\platform-tools\adb.exe')
TARGET_NUMBER = os.environ.get('TARGET_NUMBER', 'REPLACE_WITH_TEST_NUMBER')
DRY_RUN = os.environ.get('DRY_RUN', 'true').lower() in ('1', 'true', 'yes')

def diagnose_sms_dispatch():
    print('=== SMS INTENT DIAGNOSTIC ===')

    # Check if adb is connected
    if DRY_RUN:
        print('[*] DRY_RUN enabled — skipping real ADB calls. Devices check would run here.')
    else:
        devices = subprocess.run([ADB_EXE, 'devices'], capture_output=True, text=True)
        print(devices.stdout)

        # Try an explicit action view intent instead of sendto
        print(f'[*] Forcing SMS compose window for: {TARGET_NUMBER}')
        cmd = [
            ADB_EXE, 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW',
            '-d', f'sms:{TARGET_NUMBER}',
            '--es', 'sms_body', 'Local Operator Machine: Direct hardware link confirmation.'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f'[+] Intent broadcast result: {result.stdout.strip() or "Broadcast sent to device screen."}')

if __name__ == '__main__':
    diagnose_sms_dispatch()
