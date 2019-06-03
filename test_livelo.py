import logging
import pytest
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


ELEMENT_SEARCH_BAR = "search"
ELEMENT_PRODUCT_DESCRIPTION = "proddesc"
ELEMENT_ADD_TO_CART = "btn-add-to-cart"
ELEMENT_CART_ICON = "shopping-cart-icon"
ELEMENT_CART_COUNTER = "cart-item-count"
ELEMENT_FINALIZE_BUTTON = "finalize-btn"


@pytest.mark.parametrize("search_text, product_name",
                         [("Smartphone Motorola Moto G7", "Smartphone Motorola Moto G7 Play"),
                          ("Smartphone Motorola Moto G7", "Smartphone Motorola Moto G7 Poswer")])
def test_add_item_to_cart(browser, without_popup, browser_teardown, search_text, product_name):
    """
    Main function of the test
    """
    def is_element_present(type, value):
        try:
            browser.find_element(by=type, value=value)
        except NoSuchElementException:
            return False
        return True

    # Look for the Search bar
    assert is_element_present(By.ID, "search"), "The search bar is not present on the screen"
    search_bar = browser.find_element(By.ID, ELEMENT_SEARCH_BAR)
    # search_bar.send_keys("Smartphone Motorola Moto G7")
    search_bar.send_keys(search_text)
    search_bar.send_keys(Keys.RETURN)
    logging.info("Looking for the product on the search results")

    WebDriverWait(browser, 5).\
        until(expected_conditions.presence_of_element_located((By.CLASS_NAME, ELEMENT_PRODUCT_DESCRIPTION)))

    # Search all the products listed after the search
    products = browser.find_elements(By.CLASS_NAME, ELEMENT_PRODUCT_DESCRIPTION)
    for product in products:
        if product_name in product.text:
            logging.info("Found the desired product, clicking on it ")
            product.click()
            break

    page_title = browser.title
    assert product_name in page_title, "Product not found"

    # Wait until the add to cart button is clickable, or until timeout
    bt_add_to_cart = WebDriverWait(browser, 20).\
        until(expected_conditions.presence_of_element_located((By.ID, ELEMENT_ADD_TO_CART)))
    bt_add_to_cart.click()
    logging.info("Item added to cart, now we are going to check if it was really added to the cart")

    # Search the sopping cart icon
    cart_icon = browser.find_element(By.ID, ELEMENT_CART_ICON)
    mouse_over_icon = ActionChains(browser).move_to_element(cart_icon)
    mouse_over_icon.perform()

    # Verify if the cart really contains a item
    assert is_element_present(By.ID, ELEMENT_CART_COUNTER), "The cart item counter is not present on the page"
    assert is_element_present(By.ID, ELEMENT_FINALIZE_BUTTON), "The finalize purchase button is not present on the page"

    time.sleep(5)
