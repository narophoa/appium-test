from utils.actions import click, wait, perform_login, perform_logout, perform_purchase, perform_consume
from utils.log_utils import clear_logs, get_logs, wait_for_check
from utils.validators import check_init, check_maintenance, check_login, check_logout, check_purchase, check_initstore, check_entershop, check_consume
from utils.coordinates import INIT_BUTTON, LOGIN_BUTTON, LOGOUT_BUTTON, GUEST_BUTTON, MAINTENANCE_BUTTON, INITSTORE_BUTTON, ENTERSHOP_BUTTON
from utils.state import ensure_init, ensure_login, ensure_logout
import pytest, time
from conftest import DEVICES


#4
@pytest.mark.parametrize("driver", DEVICES, indirect=True)
def test_init(driver):
    device_id = driver.capabilities["udid"]
    clear_logs(device_id)
    click(driver, INIT_BUTTON)
    # assert wait_for_check(driver, check_init)


@pytest.mark.parametrize("driver", DEVICES, indirect=True)
def test_maintenance(driver):
    device_id = driver.capabilities["udid"]

    ensure_init(driver)   # ✅ 조건부 실행
    time.sleep(1)
    clear_logs(device_id)
    click(driver, MAINTENANCE_BUTTON)

    assert wait_for_check(driver, check_maintenance)


@pytest.mark.parametrize("driver", DEVICES, indirect=True)
def test_login_guest(driver):
    ensure_init(driver)
    ensure_login(driver)

    logs = get_logs(driver.capabilities["udid"])
    assert check_login(logs)



@pytest.mark.parametrize("driver", DEVICES, indirect=True)
def test_logout(driver, loggedin_driver):
    driver = loggedin_driver

    ensure_logout(driver)

    logs = get_logs(driver.capabilities["udid"])
    assert check_logout(logs)



@pytest.mark.parametrize("driver", DEVICES, indirect=True)
def test_purchase_basic(driver, loggedin_driver):
    driver = loggedin_driver

    print("\nPurchase Basic Test")    

    clear_logs(driver.capabilities["udid"])
    click(driver, INITSTORE_BUTTON)
    assert wait_for_check(driver, check_initstore)

    clear_logs(driver.capabilities["udid"])
    click(driver, ENTERSHOP_BUTTON)
    assert wait_for_check(driver, check_entershop)

    clear_logs(driver.capabilities["udid"])
    perform_purchase(driver)
    assert wait_for_check(driver, check_purchase, timeout=30)

    clear_logs(driver.capabilities["udid"])
    perform_consume(driver)        

# #@pytest.mark.parametrize("driver", DEVICES, indirect=True)
# # def test_purchase_lifecycle(loggedin_driver):
# #     driver = loggedin_driver

# #     print("\nPurchase Lifecycle Test")
    
# #     clear_logs(driver.capabilities["udid"])
# #     click(driver, INITSTORE_BUTTON)
# #     assert wait_for_check(driver, check_initstore), "InitStore Failed"
    
# #     clear_logs(driver.capabilities["udid"])
# #     click(driver, ENTERSHOP_BUTTON)
# #     assert wait_for_check(driver, check_entershop), "EnterShop Failed"
    
# #     # 첫 구매
# #     clear_logs(driver.capabilities["udid"])  
# #     perform_purchase(driver)
# #     assert wait_for_check(driver, check_purchase, timeout=30), "First Purchase Failed"

# #     # consume 확인 / Consume은 재구매 성공 여부로 검증함
# #     clear_logs(driver.capabilities["udid"])
# #     perform_consume(driver)    

#     # 두 번째 구매
#     clear_logs(driver.capabilities["udid"])
#     perform_purchase(driver)
#     assert wait_for_check(driver, check_purchase, timeout=30), "consume Failed"