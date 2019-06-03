import logging
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# To use the google chrome browser, a third party driver called chromedriver
# is needed. Download the correct driver for your Google Chrome browser version
# and SO at https://sites.google.com/a/chromium.org/chromedriver/downloads, and
# place it in the same folder as the python script
try:
    chromedriver = "./chromedriver"
    driver = webdriver.Chrome(chromedriver)
except Exception:
    logging.error("chromedriver file not on script folder, please download and add it here")
    sys.exit(1)

logging.info("Navigating to livelo main page")
driver.get("http:pontoslivelo.com.br")
logging.info("Done loading the livelo page")

bt_not_now = WebDriverWait(driver, 5).\
    until(expected_conditions.presence_of_element_located((By.XPATH, "//*[text()='Agora não']")))
if bt_not_now:
    logging.info("Found notifications popup on screen, clicking on 'Agora não' button...")
    bt_not_now.click()

try:
    search_bar = driver.find_element_by_css_selector("input[placeholder='O que você está procurando?']")
    logging.info("Found search bar on page, starting to type the search input...")
except Exception as e:
    assert False, "Assert Failed{}".format(e)

search_bar.send_keys("Motorola Moto G7 Plus")
search_bar.send_keys(Keys.RETURN)
logging.info("Done searching the requested item, now preparing to click on it")

product = driver.find_element_by_partial_link_text("Smartphone Motorola Moto G7 Plus")
driver.execute_script("arguments[0].scrollIntoView();", product)
product.click()
logging.info("Clicked on item, now adding it to the cart")

# Wait until the add to cart button is clickable, or until timeout
bt_add_to_cart = WebDriverWait(driver, 20).\
    until(expected_conditions.presence_of_element_located((By.NAME, "m:additemtoorder")))
# driver.execute_script("arguments[0].scrollIntoView();", bt_add_to_cart)
bt_add_to_cart.click()
logging.info("Item added to cart, now we are going to check if it was really added to the cart")

cart_icon = driver.find_element_by_id("shopping-cart-icon")
mouse_over_icon = ActionChains(driver).move_to_element(cart_icon)
mouse_over_icon.perform()

try:
    cart_count = driver.find_element_by_id("cart-item-count")
    finalize_button = driver.find_element_by_id("finalize-btn")
except NoSuchElementException:
    logging.info("Elements not located, the item was not properly added to the cart. Test status: FAIL")
else:
    logging.info("The item was succesfully added to the cart. Test status: PASS")
