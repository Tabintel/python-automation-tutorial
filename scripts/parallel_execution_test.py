#!/usr/bin/env python3
"""
Problem Scenario:
    Run parallel tests across Chrome, Safari, and Firefox using Playwright on LambdaTest.
    
Implementation:
    Uses Python threading to run tests concurrently with different browser capabilities.
    
Code Walkthrough:
    - Defines a test function that navigates to the Selenium Playground.
    - Launches parallel threads for each browser configuration.
    
Execution:
    Check console output and LambdaTest Dashboard for parallel test results.
"""

import os
import json
import threading
from playwright.sync_api import sync_playwright

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    caps_json = json.dumps(caps)
    return f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"

def run_test(browser_type: str, capabilities: dict, test_name: str):
    ws_endpoint = get_ws_endpoint(capabilities)
    with sync_playwright() as p:
        if browser_type.lower() == "chrome":
            browser = p.chromium.connect(ws_endpoint)
        elif browser_type.lower() == "firefox":
            browser = p.firefox.connect(ws_endpoint)
        elif browser_type.lower() == "safari":
            # For Safari, you might use WebKit as a proxy.
            browser = p.webkit.connect(ws_endpoint)
        else:
            print(f"Unsupported browser: {browser_type}")
            return
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground")
        header = page.text_content("h1")
        print(f"{test_name} on {browser_type}: Found header: {header}")
        browser.close()

if __name__ == "__main__":
    tests = [
        ("Chrome", {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "platform": "Windows 10",
            "build": "Playwright Python Automation Build",
            "name": "Parallel Test - Chrome",
        }),
        ("Safari", {
            "browserName": "Safari",
            "browserVersion": "latest",
            "platform": "macOS Monterey",
            "build": "Playwright Python Automation Build",
            "name": "Parallel Test - Safari",
        }),
        ("Firefox", {
            "browserName": "Firefox",
            "browserVersion": "latest",
            "platform": "Windows 10",
            "build": "Playwright Python Automation Build",
            "name": "Parallel Test - Firefox",
        }),
    ]

    threads = []
    for browser_type, caps in tests:
        t = threading.Thread(target=run_test, args=(browser_type, caps, f"Test on {browser_type}"))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print("Parallel execution test completed.")
