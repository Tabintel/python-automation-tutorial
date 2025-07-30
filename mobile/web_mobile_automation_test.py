"""
Web Mobile Automation Test (LambdaTest Cloud)
This script demonstrates browser automation on real mobile devices using Playwright and LambdaTest.
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MOBILE_CAPS = {"build": "Mobile Web Build", "name": "Web Mobile Automation Test"}


@pytest.mark.parametrize("android_driver", [MOBILE_CAPS], indirect=True)
def test_web_mobile_automation(android_driver):

    # get the browser button
    browser = WebDriverWait(android_driver, 20).until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.lambdatest.proverbial:id/webview")
        )
    )
    # click the browser button
    browser.click()

    # get the url text input
    url = WebDriverWait(android_driver, 20).until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.lambdatest.proverbial:id/url"))
    )
    # enter the url
    url.send_keys("https://www.lambdatest.com/selenium-playground")

    # get the find button
    find = WebDriverWait(android_driver, 20).until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.lambdatest.proverbial:id/find"))
    )
    # click the find button
    find.click()

    # switch to webview so that the content of the webpage can be fetched
    WebDriverWait(android_driver, 20).until(lambda d: len(d.contexts) > 1)
    for context in android_driver.contexts:
        if context.startswith("WEBVIEW"):
            android_driver.switch_to.context(context)
            break

    # ow assert page title
    WebDriverWait(android_driver, 20).until(lambda d: "Selenium" in d.title)
    assert "Selenium" in android_driver.title
    logging.info(f"[Mobile Web] Page title: {android_driver.title}")


if __name__ == "__main__":
    pytest.main([__file__, "-s"])