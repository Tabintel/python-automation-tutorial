#!/usr/bin/env python3
"""
Local Form Submission Test

This test demonstrates running a basic form submission test locally using Chrome.
It performs the following actions:
- Launches a local Chrome browser
- Navigates to the LambdaTest Selenium Playground
- Fills out and submits a form
- Verifies the form submission
"""

import os
import logging
import pytest
from playwright.sync_api import sync_playwright, expect

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_local_form_submission():
    """
    Test form submission on the LambdaTest Selenium Playground using local Chrome.
    """
    with sync_playwright() as p:
        # Launch Chrome browser
        logger.info("Launching Chrome browser")
        browser = p.chromium.launch(headless=False)  # Set headless=True for CI/CD
        
        # Create a new browser context and page
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Navigate to the test page
            logger.info("Navigating to LambdaTest Selenium Playground")
            page.goto("https://www.lambdatest.com/selenium-playground/")
            
            # Navigate to Simple Form Demo
            logger.info("Navigating to Simple Form Demo")
            page.click("text=Simple Form Demo")
            
            # Fill out the form
            logger.info("Filling out the form")
            test_message = "Local Chrome Test"
            page.fill("#user-message", test_message)
            page.click("#showInput")
            
            # Verify the output
            output_text = page.text_content("#message")
            logger.info(f"Output message: {output_text}")
            
            # Assert the test passed
            assert test_message in output_text, f"Expected '{test_message}' in output, got '{output_text}'"
            logger.info("Test passed: Form submission successful")
            
            # Take a screenshot for verification
            screenshot_path = "local_form_submission.png"
            page.screenshot(path=screenshot_path)
            logger.info(f"Screenshot saved to {screenshot_path}")
            
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise
            
        finally:
            # Close the browser
            logger.info("Closing browser")
            browser.close()

if __name__ == "__main__":
    test_local_form_submission()
