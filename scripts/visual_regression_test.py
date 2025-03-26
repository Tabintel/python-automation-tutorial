#!/usr/bin/env python3
"""
Problem Scenario:
    Capture a screenshot of a webpage for visual regression testing.
    
Implementation:
    Uses Playwright to navigate to a URL and capture a screenshot,
    which is saved locally for comparison.
    
Code Walkthrough:
    - Connects to LambdaTest Cloud with Chrome.
    - Navigates to https://www.lambdatest.com.
    - Saves the screenshot to the 'screenshots' folder.
    
Execution:
    Check the 'screenshots/visual_regression.png' file for the captured screenshot.
"""

import os
import json
from playwright.sync_api import sync_playwright

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    caps_json = json.dumps(caps)
    return f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"

def visual_regression_test():
    capabilities = {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "platform": "Windows 10",
        "build": "Playwright Python Automation Build",
        "name": "Visual Regression Test",
    }
    ws_endpoint = get_ws_endpoint(capabilities)
    
    with sync_playwright() as p:
        browser = p.chromium.connect(ws_endpoint)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com")
        screenshot_path = "screenshots/visual_regression.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        browser.close()

if __name__ == "__main__":
    visual_regression_test()
