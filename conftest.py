import os
import json
import pytest
from playwright.sync_api import sync_playwright

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    caps_json = json.dumps(caps)
    return f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"

@pytest.fixture(scope="function")
def lt_browser(request):
    """
    Pytest fixture for Playwright browser session on LambdaTest.
    Usage: def test_x(lt_browser):
    """
    browser_type = request.param.get("browser_type")
    capabilities = request.param.get("capabilities")
    ws_endpoint = get_ws_endpoint(capabilities)
    with sync_playwright() as p:
        if browser_type.lower() == "chrome":
            browser = p.chromium.connect(ws_endpoint)
        elif browser_type.lower() == "firefox":
            browser = p.firefox.connect(ws_endpoint)
        elif browser_type.lower() == "safari":
            browser = p.webkit.connect(ws_endpoint)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        yield browser
        browser.close()
