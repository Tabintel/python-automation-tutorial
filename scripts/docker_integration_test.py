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
import pytest

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    caps_json = json.dumps(caps)
    return f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"

# Refactor to use lt_browser fixture
@pytest.mark.parametrize("lt_browser", [{"browser_type": "chromium", "capabilities": {"browserName": "Chrome", "browserVersion": "latest", "LT:Options": {"platform": "Windows 10", "build": "Docker-Build", "name": "Docker Integration Test"}}}], indirect=True)
def test_docker_integration(lt_browser):
    """
    Run Playwright tests inside a Docker container on LambdaTest.
    """
    page = lt_browser.new_page()
    page.goto("https://www.lambdatest.com/selenium-playground/")
    assert "Selenium" in page.title()
    print(f"[Docker Integration] Test completed. Title: {page.title()}")
    page.close()

if __name__ == "__main__":
    pytest.main([__file__])
