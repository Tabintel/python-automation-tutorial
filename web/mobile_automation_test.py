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
    header = page.get_by_role("heading", name="Shop by Category")
    assert header.is_visible(), f"Page header not found on {device['name']}"
    
    # Check for mobile-specific elements
    menu_button = page.locator("button[data-toggle='dropdown']")
    assert menu_button.is_visible(), "Mobile menu button not visible"
    
    # Take a screenshot for verification
    screenshot_path = f"mobile_test_{device['name'].lower().replace(' ', '_')}.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")
    
    # Verify responsive behavior
    viewport_size = page.viewport_size
    if viewport_size and viewport_size["width"] < 768:  # Mobile breakpoint
        # Check if mobile menu is collapsed by default
        nav_menu = page.locator("nav.navbar-collapse")
        assert not nav_menu.is_visible(), "Mobile menu should be collapsed on small screens"
        
        # Open mobile menu and verify
        menu_button.click()
        assert nav_menu.is_visible(), "Mobile menu should be visible after clicking the menu button"
    
    # Verify touch interactions work
    search_icon = page.locator("a[title='Search']")
    search_icon.click()
    
    search_input = page.locator("input[name='search']")
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
    print(f"Successfully completed mobile test on {device['name']} with viewport {device['viewport']}")

# This test is now a pytest test and should be run using pytest
# Remove the main block since we're using pytest for test discovery
# if __name__ == "__main__":
#     mobile_automation_test()
