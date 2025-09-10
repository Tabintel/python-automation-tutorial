#!/usr/bin/env python3
"""
Problem Scenario:
    Run a mobile automation test on LambdaTest Real Device Cloud using Playwright.
    
Implementation:
    Uses mobile-specific capabilities (e.g., Android device) to connect to LambdaTest.
    
Important Note:
    This script demonstrates mobile web testing using Playwright with mobile device emulation.
    For real device testing, consider using Appium with LambdaTest's real device cloud.
    Playwright's mobile testing is limited to emulation and does not support real device testing.
    
Code Walkthrough:
    - Uses mobile emulation capabilities for an Android device with Chrome.
    - Navigates to the Selenium Playground.
    - Captures a header text.
    
Execution:
    Verify output on the console and via LambdaTest Dashboard.
"""

import pytest
from playwright.sync_api import expect
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Note: Playwright does not support real device automation directly.
# This test demonstrates mobile emulation in the browser.
# For real device testing, use Appium with LambdaTest's real device cloud.

# Test configuration for different mobile devices
MOBILE_DEVICES = [
    {
        "name": "iPhone 12 Pro",
        "viewport": {"width": 390, "height": 844},
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    },
    {
        "name": "Pixel 5",
        "viewport": {"width": 393, "height": 851},
        "user_agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
    },
    {
        "name": "Galaxy S20",
        "viewport": {"width": 412, "height": 915},
        "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36"
    }
]

@pytest.mark.parametrize("lt_browser", [{"browser_type": "chrome", "browser_name": "Chrome", "browser_version": "latest", "platform": "Windows 10", "build": "Mobile Automation Build", "name": "E-commerce Search Test"}], indirect=True)
@pytest.mark.parametrize('device', MOBILE_DEVICES, ids=[d["name"] for d in MOBILE_DEVICES])
def test_mobile_emulation(lt_page, device):
    """
    Test mobile emulation using Playwright on LambdaTest.
    Tests multiple mobile device profiles with different viewports and user agents.
    """
    page = lt_page
    
    # Set the viewport and user agent for the device
    page.set_viewport_size(device["viewport"])
    page.set_extra_http_headers({"user-agent": device["user_agent"]})
    
    # Navigate to a mobile-friendly website
    page.goto("https://ecommerce-playground.lambdatest.io/")
    
    # Wait for the page to load
    page.wait_for_load_state("networkidle")
    
    # Verify the page loaded correctly
    # header = page.get_by_role("heading", name="Shop by Category") # the "Shop by Category header is showing on desktop mode, not mobile"
    header = page.get_by_role("button", name="All Categories")
    assert header.is_visible(), f"Page header not found on {device['name']}"
    
    # Check for mobile-specific elements
    menu_button = page.get_by_role("button", name="Shop by Category")
    assert menu_button.is_visible(), "Mobile menu button not visible"
    
    # Take a screenshot for verification
    screenshot_path = f"mobile_test_{device['name'].lower().replace(' ', '_')}.png"
    page.screenshot(path=screenshot_path)
    logging.info(f"Screenshot saved: {screenshot_path}")
    
    # Verify responsive behavior
    viewport_size = page.viewport_size
    if viewport_size and viewport_size["width"] < 768:  # Mobile breakpoint
        # Check if mobile menu is collapsed by default
        # Locate drawer by its heading
        drawer = page.locator("div.mz-pure-drawer:has(h5:has-text('Top categories'))")

        # Validate that it's now active (has 'active' in class)
        assert not drawer.evaluate("el => el.classList.contains('active')"), "Drawer is active before clicking menu"

        # Click the hamburger menu button
        menu_button.click()

        # Wait until the menu becomes visible (class 'show' is added)
        page.wait_for_timeout(1000)  # Small wait for animation

        # Locate drawer by its heading
        drawer = page.locator("div.mz-pure-drawer:has(h5:has-text('Top categories'))")

        # Validate that it's now active (has 'active' in class)
        assert drawer.evaluate("el => el.classList.contains('active')"), "Drawer is not active after clicking menu"

        # click the menu button again to close the nav bar
        close_button = page.get_by_role("heading", name="Top categories close").get_by_label("close")
        close_button.click()

        # Wait until the menu becomes hidden (class 'show' is removed)
        page.wait_for_timeout(1000)  # Small wait for animation


    
    # Verify touch interactions work
    search_icon = page.get_by_title("Search")
    search_icon.click()

    page.wait_for_timeout(1000)
    
    search_input = page.get_by_placeholder("Keywords")
    assert search_input.is_visible(), "Search input should be visible after clicking search icon"
    
    # Test form input
    test_search = "iPhone"
    search_input.fill(test_search)
    search_input.press("Enter")
    
    # Verify search results
    results_header = page.get_by_role("heading", level=1)
    expect(results_header).to_contain_text(test_search)
    
    # Verify product grid is responsive
    products = page.locator(".product-layout")
    product_count = products.count()
    assert product_count > 0, "No products found in search results"
    
    # Log test completion
    logging.info(f"Successfully completed mobile test on {device['name']} with viewport {device['viewport']}")


if __name__ == "__main__":
    pytest.main([__file__])