import logging
import os.path
import pytest
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# To use the google chrome browser, a third party driver called chromedriver
# is needed. Download the correct driver for your Google Chrome browser version
# and SO at https://sites.google.com/a/chromium.org/chromedriver/downloads, and
# place it in the same folder as the python script
@pytest.fixture()
def browser():
    """
    Function to configure the Browser to be utilized, which is Google Chrome on thi case
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    try:
        chromedriver = "./chromedriver"
        browser = webdriver.Chrome(chromedriver)
    except Exception as e:
        logging.error("chromedriver file not on script folder, please download and add it here {}".format(e))
        sys.exit(1)

    logging.info("Maximizing browser window")
    browser.maximize_window()

    logging.info("Navigating to livelo main page")
    browser.get("http:pontoslivelo.com.br")
    logging.info("Done loading the livelo page")

    return browser


@pytest.fixture()
def without_popup(browser):
    """
    Function to close the notifications popup that appear after opening the page
    """
    bt_not_now = WebDriverWait(browser, 5).\
        until(expected_conditions.presence_of_element_located((By.XPATH, "//*[text()='Agora não']")))
    if bt_not_now:
        logging.info("Found notifications popup on screen, clicking on 'Agora não' button...")
        bt_not_now.click()


@pytest.fixture()
def browser_teardown(browser):
    """
    Function to execute the test teardown, which closes the browser after finishing the test
    """
    yield
    logging.info("Finalizing test, closing the browser")
    browser.close()
    browser.quit()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            driver = item.funcargs['browser']
            save_path = "./screenshots/"
            file_name = os.path.join(save_path, report.nodeid.replace("::", "_")+".png")
            _capture_screenshot(file_name, driver)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name, driver):
    logging.warning("Test failed, Capturing the screenshot")
    driver.get_screenshot_as_file(name)
