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

import pytest
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Refactor to use lt_browser fixture
@pytest.mark.parametrize("lt_browser", [{"browser_type": "chrome", "browser_name": "Chrome", "browser_version": "latest", "platform": "Windows 10", "build": "Docker-Build", "name": "Docker Integration Test"}], indirect=True)
def test_docker_integration(lt_browser):
    """
    Run Playwright tests inside a Docker container on LambdaTest.
    """
    page = lt_browser.new_page()
    page.goto("https://www.lambdatest.com/selenium-playground/")
    assert "Selenium" in page.title()
    logging.info(f"[Docker Integration] Test completed. Title: {page.title()}")
    page.close()

if __name__ == "__main__":
    pytest.main([__file__])
