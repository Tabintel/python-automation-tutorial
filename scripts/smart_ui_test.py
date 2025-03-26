#!/usr/bin/env python3
"""
Problem Scenario:
    Validate UI element details by capturing its location and size for smart UI validation.
    
Implementation:
    Uses Playwright to connect to LambdaTest,
    navigates to the Selenium Playground,
    locates a header element, and prints its bounding box.
    
Code Walkthrough:
    - Constructs capabilities for Firefox.
    - Retrieves element position and dimensions.
    - Demonstrates SmartUI validation concepts.
    
Execution:
    Check console output for element details.
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
    return f"wss://cdp.lambdatest.com/playwright?capabilities={caps_json}&user={username}&key={access_key}"

def smart_ui_test():
    try:
        capabilities = {
            "browserName": "Firefox",
            "browserVersion": "latest",
            "platform": "Windows 10",
            "build": "Playwright Python Automation Build",
            "name": "Smart UI Test",
            "smartUI.project": "Python Automation Demo",  # SmartUI project name
            "smartUI.baseline": True,  # Mark this as baseline for future comparisons
        }
        ws_endpoint = get_ws_endpoint(capabilities)
        
        with sync_playwright() as p:
            logger.info("Connecting to LambdaTest Cloud")
            browser = p.firefox.connect(ws_endpoint)
            page = browser.new_page()
            
            # Navigate to the Selenium Playground
            logger.info("Navigating to LambdaTest Selenium Playground")
            page.goto("https://www.lambdatest.com/selenium-playground")
            
            # Find the header element
            element = page.query_selector("h1")
            if not element:
                raise Exception("Header element not found")
            
            # Get element's bounding box
            box = element.bounding_box()
            logger.info("Smart UI Test - Element Details:")
            logger.info(f"Location: X={box['x']}, Y={box['y']}")
            logger.info(f"Size: Width={box['width']}, Height={box['height']}")
            
            # Take a screenshot for SmartUI comparison
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = "screenshots/smart_ui_test.png"
            page.screenshot(path=screenshot_path)
            logger.info(f"Screenshot saved to {screenshot_path}")
            
            # Simulate SmartUI validation by checking element dimensions
            # In a real scenario, LambdaTest's SmartUI would compare this with baseline
            if box['width'] > 0 and box['height'] > 0:
                logger.info("Element validation passed")
                # Mark test as passed in LambdaTest
                page.evaluate("_ => {}", "lambdatest_action: setTestStatus", {"status": "passed", "remark": "SmartUI validation successful"})
            else:
                logger.error("Element validation failed - invalid dimensions")
                page.evaluate("_ => {}", "lambdatest_action: setTestStatus", {"status": "failed", "remark": "SmartUI validation failed"})
            
            browser.close()
            logger.info("Test completed successfully")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    smart_ui_test()
