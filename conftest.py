
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
# ✅ driver cache (핵심 추가)
# -----------------------------
DRIVERS = {}


def create_driver(device):
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

    time.sleep(5)
    driver.implicitly_wait(5)

    return driver


# -----------------------------
# ✅ driver fixture (속도 개선)
# -----------------------------
@pytest.fixture(scope="function")
def driver(request):
    device = request.param
    device_id = device["deviceName"]

    # ✅ 이미 있으면 재사용
    if device_id not in DRIVERS:
        DRIVERS[device_id] = create_driver(device)

    driver = DRIVERS[device_id]

    # ✅ 상태 초기화
    ensure_init(driver)

    yield driver


# -----------------------------
# login fixture
# -----------------------------
@pytest.fixture
def loggedin_driver(driver):
    ensure_login(driver)
    return driver


# -----------------------------
# 종료 처리 (중요)
# -----------------------------
def pytest_sessionfinish(session, exitstatus):
    print("Driver cleanup...")

    for d in DRIVERS.values():
        try:
            d.quit()
        except:
            pass

    stop_appium_servers()
