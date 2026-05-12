# 상태 보장

from utils.log_utils import clear_logs, get_logs
from utils.validators import check_init, check_logout, check_login
from utils.actions import click, perform_login, perform_logout
from utils.coordinates import INIT_BUTTON, LOGIN_BUTTON, LOGOUT_BUTTON, GUEST_BUTTON
from utils.lock import init_lock
from utils.log_utils import wait_for_check
import time



def ensure_init(driver):
    if getattr(driver, "_initialized", False):
        return

    device_id = driver.capabilities["udid"]

    logs = get_logs(device_id)

    if check_init(logs):
        driver._initialized = True
        return

    clear_logs(device_id)
    click(driver, INIT_BUTTON)

    if wait_for_check(driver, check_init, timeout=10):
        driver._initialized = True
        return
    
    print("Init uncertain (skip)")
    driver._initialized = True




def ensure_login(driver):
    if getattr(driver, "_logged_in", False):
        return

    device_id = driver.capabilities["udid"]

    clear_logs(device_id)
    perform_login(driver)

    if not wait_for_check(driver, check_login, timeout=15):
        raise Exception("Login failed")

    driver._logged_in = True


def ensure_logout(driver):
    if getattr(driver, "_logged_out", False):
        return

    device_id = driver.capabilities["udid"]

    clear_logs(device_id)
    perform_logout(driver)

    if not wait_for_check(driver, check_logout, timeout=10):
        raise Exception("Logout failed")

    driver._logged_out = True
    driver._logged_in = False
