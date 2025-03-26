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
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_ws_endpoint(caps: dict) -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    
    if not username or not access_key:
        raise EnvironmentError("LT_USERNAME and LT_ACCESS_KEY environment variables must be set")
    
    caps_json = json.dumps(caps)
    # LambdaTest Playwright endpoint format
    ws_endpoint = f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"
    return ws_endpoint

def lambda_test_form_submission():
    try:
        capabilities = {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "platform": "Windows 10",
            "build": "Playwright Python Automation Build",
            "name": "Playground Form Test",
        }
        ws_endpoint = get_ws_endpoint(capabilities)
        
        with sync_playwright() as p:
            logger.info("Connecting to LambdaTest Cloud")
            # Connect using Chrome (you can also use p.chromium)
            browser = p.chromium.connect(ws_endpoint)
            page = browser.new_page()
            
            logger.info("Navigating to LambdaTest Selenium Playground")
            page.goto("https://www.lambdatest.com/selenium-playground")
            
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
                page.evaluate("_ => {}", "lambdatest_action: setTestStatus", {"status": "passed", "remark": "Form submission successful"})
            else:
                logger.error("Form submission verification failed")
                page.evaluate("_ => {}", "lambdatest_action: setTestStatus", {"status": "failed", "remark": "Form submission failed"})
            
            browser.close()
            logger.info("Test completed successfully")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    lambda_test_form_submission()
