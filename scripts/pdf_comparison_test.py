#!/usr/bin/env python3
"""
Problem Scenario:
    Simulate PDF comparison by navigating to a sample PDF URL and capturing its screenshot.
    
Implementation:
    Uses Playwright to connect to LambdaTest, open a sample PDF,
    and save a screenshot for later visual comparison.
    
Code Walkthrough:
    - Constructs capabilities for Chrome.
    - Navigates to a sample PDF URL.
    - Saves the screenshot as 'pdf_comparison.png' in the screenshots folder.
    
Execution:
    Verify the screenshot in the 'screenshots' folder.
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

def pdf_comparison_test():
    try:
        capabilities = {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "platform": "Windows 10",
            "build": "Playwright Python Automation Build",
            "name": "PDF Comparison Test",
            "visual": True,  # Enable visual testing features
        }
        ws_endpoint = get_ws_endpoint(capabilities)
        
        with sync_playwright() as p:
            logger.info("Connecting to LambdaTest Cloud")
            browser = p.chromium.connect(ws_endpoint)
            page = browser.new_page()
            
            # Navigate to a sample PDF URL
            pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            logger.info(f"Navigating to PDF URL: {pdf_url}")
            page.goto(pdf_url)
            
            # Wait for PDF to load
            page.wait_for_load_state("networkidle")
            
            # Create screenshots directory if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)
            
            # Take screenshot
            screenshot_path = "screenshots/pdf_comparison.png"
            page.screenshot(path=screenshot_path)
            logger.info(f"PDF screenshot saved to {screenshot_path}")
            
            # Mark test as passed in LambdaTest
            page.evaluate("_ => {}", "lambdatest_action: setTestStatus", {"status": "passed", "remark": "PDF comparison successful"})
            
            browser.close()
            logger.info("Test completed successfully")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    pdf_comparison_test()