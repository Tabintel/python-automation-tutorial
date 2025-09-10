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

import pytest
import logging
import sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


browsers = [
    {"browser_type": "chrome", "browser_name": "Chrome", "browser_version": "latest", "platform": "Windows 10", "build": "Parallel-Build", "name": "Chrome Test"},
    {"browser_type": "edge", "browser_name": "MicrosoftEdge", "browser_version": "latest", "platform": "Windows 10", "build": "Parallel-Build", "name": "MicrosoftEdge Test"},
]

if sys.platform != "win32":
    browsers.append({
        "browser_type": "safari",
        "browser_name": "pw-webkit",
        "browser_version": "latest",
        "platform": "macOS Big Sur",
        "build": "Parallel-Build",
        "name": "Safari Test"
    })


@pytest.mark.parametrize("lt_browser", browsers, indirect=True)
def test_parallel_execution(lt_browser):
    page = lt_browser.new_page()
    page.goto("https://www.lambdatest.com/selenium-playground/")
    logger.info(f"Page title: {page.title()}")
    page.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-n", "2"])