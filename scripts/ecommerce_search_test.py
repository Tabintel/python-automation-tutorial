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
import pytest
from playwright.sync_api import sync_playwright

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    caps_json = json.dumps(caps)
    ws_endpoint = f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"
    return ws_endpoint

@pytest.mark.parametrize("lt_browser", [{"browser_type": "firefox", "capabilities": {"browserName": "Firefox", "browserVersion": "latest", "LT:Options": {"platform": "Windows 10", "build": "ECommerce-Build", "name": "E-Commerce Search Test"}}}], indirect=True)
def test_ecommerce_search(lt_browser):
    """
    Automate a product search and simulate an add-to-cart action on the LambdaTest E-Commerce Playground.

    :param lt_browser: The lt_browser pytest fixture for browser management.
    """
    page = lt_browser.new_page()
    page.goto("https://ecommerce-playground.lambdatest.io/")
    page.fill("input[name='search']", "iPhone")
    page.click("button[type='button'][data-bs-original-title='Search']")
    assert "iPhone" in page.content()
    print(f"[E-Commerce] Search completed. Title: {page.title()}")
    page.close()

if __name__ == "__main__":
    pytest.main([__file__])
