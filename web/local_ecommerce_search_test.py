#!/usr/bin/env python3
"""
Local E-commerce Search Test

This test demonstrates product search functionality on an e-commerce site using Playwright
running locally (no LambdaTest). It performs the following actions:
- Launches Chrome locally
- Navigates to the e-commerce playground
- Accepts cookies if present
- Performs a product search
- Verifies search results
- Takes a screenshot of the results

Execution:
    Run with: python local_ecommerce_search_test.py
    Verify test execution via console output and generated screenshot.
"""
import logging
from playwright.sync_api import sync_playwright, expect

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test data
SEARCH_TERM = "iPhone"
EXPECTED_RESULTS = ["iPhone", "Apple"]

def test_local_ecommerce_search():
    """
    Test product search functionality locally in Chrome.
    """
    with sync_playwright() as p:
        # Launch Chrome (local, visible)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Navigate to the e-commerce site
            page.goto("https://ecommerce-playground.lambdatest.io/")

            # Accept cookies if present
            try:
                accept_button = page.get_by_role("button", name="Accept")
                if accept_button.is_visible():
                    accept_button.click()
            except Exception as e:
                logging.warning(f"Cookie banner not found or could not be accepted: {e}")

            # Search for product
            search_box = page.get_by_role("textbox", name="Search For Products")
            expect(search_box).to_be_visible()
            search_box.fill(SEARCH_TERM)

            search_button = page.get_by_role("button", name="Search")
            search_button.click()

            # Verify results header
            results_header = page.get_by_role("heading", name=f"Search - {SEARCH_TERM}")
            expect(results_header).to_be_visible()

            # Verify expected terms in page
            page_content = page.content().lower()
            for term in EXPECTED_RESULTS:
                assert term.lower() in page_content, f"Expected '{term}' not found in results"

            # Take screenshot
            screenshot = page.screenshot()
            with open("local_ecommerce_search_results.png", "wb") as f:
                f.write(screenshot)

            logging.info(f"[Local E-Commerce] Search for '{SEARCH_TERM}' completed successfully")

        finally:
            browser.close()

if __name__ == "__main__":
    test_local_ecommerce_search()
