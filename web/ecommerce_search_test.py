    Uses Playwright to connect to LambdaTest, navigate to the e-commerce site,
    perform a product search, and click the "Add to Cart" button.
    
Code Walkthrough:
        Uses Playwright with LambdaTest to navigate to the e-commerce site,
    perform a product search, and verify search results.
    
Code Walkthrough:
    - Uses the lt_browser fixture from conftest.py for browser management
    - Locates the search box and enters a search query
    - Verifies search results and takes a screenshot
    
Execution:
    Run with: pytest web/ecommerce_search_test.py -v
    Verify test execution via console output and the LambdaTest Dashboard.
"""

import pytest
from playwright.sync_api import Page, expect

# Test data
SEARCH_TERM = "iPhone"
EXPECTED_RESULTS = ["iPhone", "Apple"]

# Using the lt_browser fixture from conftest.py which is configured
# with appropriate capabilities for this test

def test_ecommerce_search(lt_browser: Page):
    """
    Test product search functionality on the e-commerce playground.
    
    Args:
        lt_browser: Playwright Page instance provided by the lt_browser fixture
    """
    # Create a new page in the browser context
    page = lt_browser
    
    # Navigate to the e-commerce site
    page.goto("https://ecommerce-playground.lambdatest.io/")
    
    # Accept cookies if the banner is present
    try:
        accept_button = page.get_by_role("button", name="Accept")
        if accept_button.is_visible():
            accept_button.click()
    except Exception as e:
        print(f"Cookie banner not found or could not be accepted: {e}")
    
    # Find the search box and enter the search term
    search_box = page.get_by_placeholder("Search For Products")
    expect(search_box).to_be_visible()
    search_box.fill(SEARCH_TERM)
    
    # Click the search button
    search_button = page.get_by_role("button", name="Search")
    search_button.click()
    
    # Wait for search results to load and verify content
    results_header = page.get_by_role("heading", name=f"Search - {SEARCH_TERM}")
    expect(results_header).to_be_visible()
    
    # Verify search results contain expected content
    page_content = page.content().lower()
    for term in EXPECTED_RESULTS:
        assert term.lower() in page_content, f"Expected term '{term}' not found in search results"
    
    # Take a screenshot of the results
    screenshot = page.screenshot()
    with open("ecommerce_search_results.png", "wb") as f:
        f.write(screenshot)
    
    print(f"[E-Commerce] Search for '{SEARCH_TERM}' completed successfully")

# The test is now properly integrated with pytest and uses the lt_browser fixture
# No need for the main block as pytest will discover and run the test
