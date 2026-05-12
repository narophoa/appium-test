
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time, subprocess

from utils.state import ensure_init, ensure_login, ensure_logout


# -----------------------------
# Appium server auto start
# -----------------------------

appium_processes = []


def kill_existing_appium():
    print("Killing existing Appium servers...")
    subprocess.call(
        'wmic process where "commandline like \'%appium%\'" call terminate',
        shell=True
    )


def start_appium_servers(devices):
    print("Starting Appium servers...")

    for device in devices:
        port = device["port"]

        p = subprocess.Popen(
            f"appium -p {port}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        appium_processes.append(p)
        print(f"Appium started on port {port}")

    time.sleep(5 + len(devices) * 2)


def stop_appium_servers():
    print("Stopping Appium servers...")
    for p in appium_processes:
        p.terminate()


# -----------------------------
# Device detect
# -----------------------------

def get_connected_devices():
    result = subprocess.check_output("adb devices", shell=True).decode()
    lines = result.strip().split("\n")[1:]

    devices = []
    base_port = 4723

    for i, line in enumerate(lines):
        parts = line.split()
        if len(parts) == 2 and parts[1] == "device":
            device_id = parts[0]
            devices.append({
                "deviceName": device_id,
                "port": base_port + i * 2
            })

    return devices


DEVICES = get_connected_devices()

if not DEVICES:
    raise Exception("No connected devices found")


# -----------------------------
# pytest hooks
# -----------------------------

def pytest_sessionstart(session):
    kill_existing_appium()
    start_appium_servers(DEVICES)
    time.sleep(10)

def pytest_sessionfinish(session, exitstatus):
    stop_appium_servers()


# -----------------------------
# driver (REUSE 핵심)
# -----------------------------

@pytest.fixture(scope="function")
def driver(request):
    device = request.param

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = device["deviceName"]
    options.udid = device["deviceName"]
    options.app_package = "com.webzen.mocaa.nativesample"
    options.app_activity = "com.epicgames.unreal.GameActivity"
    options.no_reset = True

    driver = webdriver.Remote(
        f"http://localhost:{device['port']}",
        options=options
    )

    print(f"[Driver Created] {device['deviceName']}")

    time.sleep(5)   # ❗ 추가 (중요)
    driver.implicitly_wait(5)


    yield driver

    driver.quit()
    print(f"[Driver Quit] {device['deviceName']}")


@pytest.fixture
def loggedin_driver(driver):
    ensure_init(driver)
    ensure_login(driver)
    return driver
