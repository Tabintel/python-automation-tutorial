#!/usr/bin/env python3
"""
Problem Scenario:
    Execute a LambdaTest automation test inside a Docker container using Playwright.
    
Implementation:
    Uses Playwright to connect to LambdaTest and perform a simple navigation test.
    
Code Walkthrough:
    - Constructs capabilities for Chrome on Windows 10.
    - Connects to LambdaTest and navigates to the Selenium Playground.
    
Execution:
    Build and run via Docker as per instructions in the README.
"""

import os
import json
from playwright.sync_api import sync_playwright

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    caps_json = json.dumps(caps)
    return f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"

def docker_lambda_test():
    capabilities = {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "platform": "Windows 10",
        "build": "Playwright Python Automation Build",
        "name": "Docker Integration Test",
    }
    ws_endpoint = get_ws_endpoint(capabilities)
    
    with sync_playwright() as p:
        browser = p.chromium.connect(ws_endpoint)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground")
        header = page.text_content("h1")
        print("Docker test: Header found:", header)
        browser.close()

if __name__ == "__main__":
    docker_lambda_test()
