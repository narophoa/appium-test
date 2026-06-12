#클릭, Wait
import time
from utils.coordinates import INIT_BUTTON, LOGIN_BUTTON, LOGOUT_BUTTON, GUEST_BUTTON, INITSTORE_BUTTON, ENTERSHOP_BUTTON, PURCHASE_BUTTON, PURCHASE_PRODUCT_BUTTON, RECEIVE_ITEMS_BUTTON

def click(driver, pos):
    driver.execute_script("mobile: clickGesture", {
        "x": pos[0],
        "y": pos[1]
    })

def perform_login(driver):
    click(driver, LOGIN_BUTTON)
    time.sleep(2)

    click(driver, GUEST_BUTTON)
    time.sleep(2)

def perform_logout(driver):
    click(driver, LOGOUT_BUTTON)
    time.sleep(2)

def wait(seconds):
    time.sleep(seconds)


def perform_purchase(driver):
    click(driver, INITSTORE_BUTTON)
    time.sleep(2)

    click(driver, ENTERSHOP_BUTTON)
    time.sleep(2)

    click(driver, PURCHASE_BUTTON)
    time.sleep(2)

    click(driver, PURCHASE_PRODUCT_BUTTON)
    time.sleep(1)


def perform_consume(driver):   
    click(driver, RECEIVE_ITEMS_BUTTON)
    time.sleep(3)


#
