"""
Web Mobile Automation Test (LambdaTest Cloud)
This script demonstrates browser automation on real mobile devices using Playwright and LambdaTest.
"""
import pytest
from playwright.sync_api import sync_playwright

MOBILE_CAPS = {
    "browserName": "Chrome",
    "browserVersion": "latest",
    "LT:Options": {
        "platform": "Android",
        "deviceName": "Galaxy S21",
        "realMobile": True,
        "build": "Mobile Web Build",
        "name": "Web Mobile Automation Test"
    }
}

@pytest.mark.parametrize("lt_browser", [{"browser_type": "chrome", "capabilities": MOBILE_CAPS}], indirect=True)
def test_web_mobile_automation(lt_browser):
    page = lt_browser.new_page()
    page.goto("https://www.lambdatest.com/selenium-playground/")
    assert "Selenium" in page.title()
    print(f"[Mobile Web] Page title: {page.title()}")
    page.close()
