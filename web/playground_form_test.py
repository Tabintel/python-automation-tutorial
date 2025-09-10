#!/usr/bin/env python3
"""
Problem Scenario:
    Automate a form submission on the LambdaTest Selenium Playground.
    
Implementation:
    Uses Playwright's synchronous API to connect to LambdaTest's cloud,
    navigates to the playground, fills out an input field, and submits the form.
    
Code Walkthrough:
    - Constructs capabilities for Chrome on Windows 10.
    - Connects via WebSocket to LambdaTest.
    - Locates the input element (by CSS selector) and types text.
    - Clicks the submit button.
    
Execution:
    View console output and screenshots (captured via LambdaTest Dashboard).
"""

import os
import json
import logging
import pytest
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

    page = lt_browser.new_page()
    logger.info("Navigating to LambdaTest Selenium Playground")
    page.goto("https://www.lambdatest.com/selenium-playground/")
    
    # Navigate to Simple Form Demo
    logger.info("Navigating to Simple Form Demo")
    page.click("text=Simple Form Demo")
    
    # Wait for the input field and interact with it
    logger.info("Filling out the form")
    page.fill("#user-message", "LambdaTest Automation")
    page.click("#showInput")
    
    # Verify the output
    output_text = page.text_content("#message")
    logger.info(f"Output message: {output_text}")
    
    if "LambdaTest Automation" in output_text:
        logger.info("Form submission verification successful")
        # Mark test as passed in LambdaTest
        page.evaluate("""() => {
            window.lambdatest_action = {
                action: 'setTestStatus',
                arguments: {
                    status: 'passed',
                    remark: 'Form submission successful'
                }
            }
        }""")

    else:
        logger.error("Form submission verification failed")
        page.evaluate("""() => {
            window.lambdatest_action = {
                action: 'setTestStatus',
                arguments: {
                    status: 'failed',
                    remark: 'Form submission failed'
                }
            }
        }""")

    
    page.close()
    logger.info("Test completed successfully")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])