#로그 처리


import subprocess, time

def clear_logs(device_id):
    subprocess.call(f"adb -s {device_id} logcat -c", shell=True)

def get_logs(device_id):
    return subprocess.check_output(
        f"adb -s {device_id} logcat -d",
        encoding="utf-8",
        errors="ignore",
        shell=True
    )

def clean_logs(logs):
    return logs.replace(" ", "").replace("\n", "")

def wait_for_check(driver, check_func, timeout=5):
    device_id = driver.capabilities["udid"]

    for _ in range(timeout):
        logs = get_logs(device_id)
        if check_func(logs):
            return True
        time.sleep(1)
    return False



