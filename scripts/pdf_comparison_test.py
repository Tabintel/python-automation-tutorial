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
import pytest
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

@pytest.mark.parametrize("lt_browser", [{"browser_type": "chromium", "capabilities": {"browserName": "Chrome", "browserVersion": "latest", "LT:Options": {"platform": "Windows 10", "build": "PDF-Build", "name": "PDF Comparison Test"}}}], indirect=True)
def test_pdf_comparison(lt_browser):
    """
    Simulates PDF comparison by navigating to a sample PDF URL and capturing its screenshot on LambdaTest.
    """
    page = lt_browser.new_page()
    pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    page.goto(pdf_url)
    page.screenshot(path="screenshots/pdf_screenshot.png")
    logger.info(f"[PDF Comparison] Screenshot saved for PDF at {pdf_url}")
    page.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--disable-pytest-warnings"])