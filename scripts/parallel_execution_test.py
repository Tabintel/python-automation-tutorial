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
import pytest
from playwright.sync_api import sync_playwright

def test_parallel_execution(pytestconfig):
    browsers = [
        {"browser_type": "chrome", "capabilities": {"browserName": "Chrome", "browserVersion": "latest", "LT:Options": {"platform": "Windows 10", "build": "Parallel-Build", "name": "Chrome Test"}}},
        {"browser_type": "firefox", "capabilities": {"browserName": "Firefox", "browserVersion": "latest", "LT:Options": {"platform": "Windows 10", "build": "Parallel-Build", "name": "Firefox Test"}}},
        {"browser_type": "safari", "capabilities": {"browserName": "Safari", "browserVersion": "latest", "LT:Options": {"platform": "macOS Big Sur", "build": "Parallel-Build", "name": "Safari Test"}}}
    ]

    def run(browser_param):
        from playwright.sync_api import Error
        try:
            browser = pytestconfig._store['lt_browser'](browser_param)
            page = browser.new_page()
            page.goto("https://www.lambdatest.com/selenium-playground/")
            print(f"[{browser_param['browser_type']}] Page title: {page.title()}")
            page.close()
        except Error as e:
            print(f"Error with {browser_param['browser_type']}: {e}")

    threads = []
    for param in browsers:
        t = threading.Thread(target=run, args=(param,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    print("Parallel execution test completed.")
