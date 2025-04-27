#!/usr/bin/env python3
"""
Problem Scenario:
    Run a mobile automation test on LambdaTest Real Device Cloud using Playwright.
    
Implementation:
    Uses mobile-specific capabilities (e.g., Android device) to connect to LambdaTest.
    
Code Walkthrough:
    - Constructs capabilities for an Android device (Google Pixel 3) with Chrome.
    - Navigates to the Selenium Playground.
    - Captures a header text.
    
Execution:
    Verify output on the console and via LambdaTest Dashboard.
"""

# This script has moved to mobile/web_mobile_automation_test.py and is now covered there.
# For native app automation, see mobile/native_app_automation_test.py and mobile/ios_native_app_automation_test.py

import os
import json
from playwright.sync_api import sync_playwright

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    caps_json = json.dumps(caps)
    return f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"

def mobile_automation_test():
    capabilities = {
        "platformName": "Android",
        "deviceName": "Google Pixel 3",
        "browserName": "Chrome",
        "build": "Playwright Python Automation Build",
        "name": "Mobile Automation Test",
    }
    ws_endpoint = get_ws_endpoint(capabilities)
    
    with sync_playwright() as p:
        browser = p.chromium.connect(ws_endpoint)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground")
        header = page.text_content("h1")
        print("Mobile test: Header found:", header)
        browser.close()

if __name__ == "__main__":
    mobile_automation_test()
