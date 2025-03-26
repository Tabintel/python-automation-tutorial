#!/usr/bin/env python3
"""
Problem Scenario:
    Automate a product search and simulate an add-to-cart action on the LambdaTest E-Commerce Playground.
    
Implementation:
    Uses Playwright to connect to LambdaTest, navigate to the e-commerce site,
    perform a product search, and click the "Add to Cart" button.
    
Code Walkthrough:
    - Constructs capabilities for Firefox on Windows 10.
    - Locates the search box (by name) and sends a search query.
    - Waits for the results and clicks the "Add to Cart" button.
    
Execution:
    Verify test execution via console output and the LambdaTest Dashboard.
"""

import os
import json
from playwright.sync_api import sync_playwright

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    caps_json = json.dumps(caps)
    ws_endpoint = f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"
    return ws_endpoint

def lambda_test_ecommerce():
    capabilities = {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "platform": "Windows 10",
        "build": "Playwright Python Automation Build",
        "name": "E-Commerce Search Test",
    }
    ws_endpoint = get_ws_endpoint(capabilities)
    
    with sync_playwright() as p:
        browser = p.firefox.connect(ws_endpoint)
        page = browser.new_page()
        page.goto("https://ecommerce-playground.lambdatest.io/")
        page.fill("[name='search']", "Laptop")
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)  # Wait for results to load
        
        # Find and click the first "Add to Cart" button
        page.click("text=Add to Cart", timeout=10000)
        print("Product search and add-to-cart executed successfully!")
        browser.close()

if __name__ == "__main__":
    lambda_test_ecommerce()
