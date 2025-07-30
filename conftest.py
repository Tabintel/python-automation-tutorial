import os
import json
import pytest
from typing import Dict, Any
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
from playwright.sync_api import sync_playwright, Browser, Page
from dotenv import load_dotenv


load_dotenv()

# LambdaTest credentials
LT_USERNAME = os.getenv("LT_USERNAME")
LT_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")


# Common test configurations
class TestConfig:
    # Web test configurations
    WEB_TEST_TIMEOUT = 60000  # 30 seconds
    SCREENSHOT_ON_FAILURE = True

    # Mobile test configurations
    ANDROID_APP_URL = os.getenv("ANDROID_APP_URL", "YOUR_ANDROID_APP_URL")
    IOS_APP_URL = os.getenv("IOS_APP_URL", "YOUR_IOS_APP_URL")


# Helper functions
def get_ws_endpoint(
    browser_name: str,
    browser_version: str,
    platform: str,
    build: str | None = None,
    name: str | None = None,
) -> str:
    """Generate WebSocket endpoint for LambdaTest."""
    if not LT_USERNAME or not LT_ACCESS_KEY:
        raise ValueError(
            "LambdaTest credentials not set. Please set LT_USERNAME and LT_ACCESS_KEY environment variables."
        )

    # Merge common capabilities with test-specific capabilities
    capabilities = {
        "browserName": browser_name,
        "browserVersion": browser_version,
        "LT:Options": {
            "platform": platform,
            "build": build or "Playwright Python Build",
            "name": name or "Playwright Python Test",
            "user": LT_USERNAME,
            "accessKey": LT_ACCESS_KEY,
            "network": True,
            "video": True,
            "console": True,
            "tunnel": False,
            "geoLocation": "",
        },
    }
    caps_json = json.dumps(capabilities)

    return f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}"


def get_android_capabilities(build: str, name: str) -> Dict[str, Any]:
    """Get Android capabilities for Appium tests."""
    return {
        "LT:Options": {
            "platformName": "android",
            "deviceName": "Galaxy S21 5G",
            "platformVersion": "12",
            "build": build,
            "name": name,
            "isRealMobile": True,
            "username": LT_USERNAME,
            "accessKey": LT_ACCESS_KEY,
            "app": TestConfig.ANDROID_APP_URL,
            "autoGrantPermissions": True,
            "appPackage": "com.lambdatest.proverbial",
            "appActivity": ".MainActivity",
        }
    }


def get_ios_capabilities(build: str, name: str) -> Dict[str, Any]:
    """Get iOS capabilities for Appium tests."""
    return {
        "LT:Options": {
            "platformName": "ios",
            "deviceName": "iPhone 12",
            "platformVersion": "15",
            "build": build,
            "name": name,
            "isRealMobile": True,
            "username": LT_USERNAME,
            "accessKey": LT_ACCESS_KEY,
            "app": TestConfig.IOS_APP_URL,
            "autoGrantPermissions": True,
            "bundleId": "com.lambdatest.proverbial",
            "automationName": "XCUITest",
        }
    }


# Web Test Fixtures
@pytest.fixture(scope="function")
def lt_browser(request) -> Browser:
    """
    Pytest fixture for Playwright browser session on LambdaTest.

    Usage in tests:
    @pytest.mark.parametrize('lt_browser', [{
        'browser_type': 'chrome',
        'capabilities': {
            'browserName': 'Chrome',
            'browserVersion': 'latest',
            'LT:Options': {
                'platform': 'Windows 10',
                'build': 'Web Test Build',
                'name': 'Web Test'
            }
        }
    }], indirect=True)
    def test_example(lt_browser):
        page = lt_browser.new_page()
        # Test code here
    """
    browser_type = request.param.get("browser_type")
    browser_name = request.param.get("browser_name")
    browser_version = request.param.get("browser_version")
    platform = request.param.get("platform")
    build = request.param.get("build")
    name = request.param.get("name")

    if name is None:
        test_name = request.node.name.replace("_", " ").title()
        name = f"{test_name} - {browser_type.capitalize()}"

    ws_endpoint = get_ws_endpoint(browser_name, browser_version, platform, build, name)

    with sync_playwright() as p:
        # Map browser type to Playwright browser
        browser_map = {
            "chrome": p.chromium,
            "firefox": p.firefox,
            "safari": p.webkit,
            "edge": p.chromium,  # Edge is Chromium-based
        }

        browser_launcher = browser_map.get(browser_type.lower())
        if not browser_launcher:
            raise ValueError(f"Unsupported browser type: {browser_type}")

        browser = browser_launcher.connect(ws_endpoint)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture(scope="function")
def lt_page(lt_browser: Browser) -> Page:
    """
    Pytest fixture that provides a new browser page.
    Automatically takes a screenshot on test failure.
    """
    page = lt_browser.new_page()
    yield page

    # Take screenshot on test failure
    if (
        hasattr(pytest, "test_failed")
        and pytest.test_failed
        and TestConfig.SCREENSHOT_ON_FAILURE
    ):
        screenshot = page.screenshot()
        with open("test_failure.png", "wb") as f:
            f.write(screenshot)

    page.close()


# Mobile Test Fixtures
@pytest.fixture(scope="function")
def android_driver(request):
    """
    Pytest fixture for Android Appium driver on LambdaTest.
    """
    if not LT_USERNAME or not LT_ACCESS_KEY:
        pytest.fail(
            "LambdaTest credentials not set. Set LT_USERNAME and LT_ACCESS_KEY environment variables."
        )

    build = request.param.get("build")
    name = request.param.get("name")

    capabilities = get_android_capabilities(build, name)

    try:
        driver = webdriver.Remote(
            command_executor=f"https://{LT_USERNAME}:{LT_ACCESS_KEY}@mobile-hub.lambdatest.com/wd/hub",
            options=AppiumOptions().load_capabilities(capabilities),
        )
        yield driver
    except Exception as e:
        print(f"Error initializing Android driver: {e}")
        raise
    finally:
        if "driver" in locals():
            driver.quit()


@pytest.fixture(scope="function")
def ios_driver(request):
    """
    Pytest fixture for iOS Appium driver on LambdaTest.
    """
    if not LT_USERNAME or not LT_ACCESS_KEY:
        pytest.fail(
            "LambdaTest credentials not set. Set LT_USERNAME and LT_ACCESS_KEY environment variables."
        )

    build = request.param.get("build")
    name = request.param.get("name")

    capabilities = get_ios_capabilities(build, name)

    try:
        driver = webdriver.Remote(
            command_executor=f"https://{LT_USERNAME}:{LT_ACCESS_KEY}@mobile-hub.lambdatest.com/wd/hub",
            options=AppiumOptions().load_capabilities(capabilities),
        )
        yield driver
    except Exception as e:
        print(f"Error initializing iOS driver: {e}")
        raise
    finally:
        if "driver" in locals():
            driver.quit()


# Hooks
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Track test status for screenshots on failure."""
    outcome = yield
    rep = outcome.get_result()

    # Set test_failed attribute if the test failed
    setattr(pytest, "test_failed", rep.failed)