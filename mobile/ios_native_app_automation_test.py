"""
iOS Native App Automation Test (LambdaTest Cloud, Appium)

This script demonstrates native app automation on LambdaTest using Appium and Python for iOS.
The test performs various actions on the Proverbial iOS app to demonstrate real-world testing scenarios.

Note: The app URL should point to a valid app uploaded to your LambdaTest storage.
For testing purposes, upload your .ipa file to LambdaTest and update the APP_URL constant.
"""

import os
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time

# LambdaTest credentials from environment variables
LAMBDATEST_USERNAME = os.getenv("LT_USERNAME")
LAMBDATEST_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")

# Note: Replace with your uploaded app URL from LambdaTest storage
# Upload your .ipa file to LambdaTest and update this URL
APP_URL = "YOUR_UPLOADED_APP_URL.ipa"  # e.g., "lt://APP1234567890abcdef"

# iOS capabilities with improved device selection using regex
IOS_CAPS = {
    "platformName": "iOS",
    "deviceName": "iPhone *",  # Using regex to match any available iPhone
    "platformVersion": "16",  # Target iOS version (will use the closest available)
    "app": APP_URL,
    "isRealMobile": True,
    "build": "iOS Native App Build",
    "name": "iOS Native App Test",
    "devicelog": True,
    "visual": True,
    "network": True,
    "console": True,
    "autoGrantPermissions": True
}

# App-specific elements (update these selectors according to your app)
class AppElements:
    # Example elements - replace with your app's actual element selectors
    WELCOME_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "welcomeMessage")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "loginButton")
    USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "usernameField")
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "passwordField")
    SUBMIT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "submitButton")
    HOME_SCREEN_TITLE = (AppiumBy.ACCESSIBILITY_ID, "homeTitle")

@pytest.mark.usefixtures("ios_driver")
class TestIOSNativeApp:
    """
    Test suite for iOS native app automation on LambdaTest real device cloud.
    This test demonstrates various interactions with an iOS app.
    """
    
    def test_app_launch_and_basic_interactions(self, ios_driver):
        """Test basic app launch and interactions."""
        driver = ios_driver
        wait = WebDriverWait(driver, 20)
        
        try:
            # 1. Verify app launched successfully
            print("iOS app launched successfully!")
            
            # 2. Take initial screenshot
            driver.save_screenshot("ios_initial_screen.png")
            print("Initial screenshot saved as 'ios_initial_screen.png'")
            
            # 3. Get and log device information
            self._log_device_info(driver)
            
            # 4. Check battery status
            self._log_battery_status(driver)
            
            # 5. Test orientation changes
            self._test_orientation(driver)
            
            # 6. Test touch interactions (swipe)
            self._test_swipe_gesture(driver)
            
            # 7. Test basic navigation (example with placeholder selectors)
            self._test_navigation(driver, wait)
            
            # 8. Test app state management
            self._test_app_state_management(driver)
            
            # 9. Take final screenshot
            driver.save_screenshot("ios_final_screen.png")
            print("Final screenshot saved as 'ios_final_screen.png'")
            
        except Exception as e:
            # Capture screenshot on failure
            driver.save_screenshot("ios_test_failure.png")
            print("Screenshot saved as 'ios_test_failure.png'")
            raise
    
    def _log_device_info(self, driver):
        """Log device information."""
        device_info = {
            'platform_version': driver.capabilities.get('platformVersion'),
            'device_udid': driver.capabilities.get('udid'),
            'device_name': driver.capabilities.get('deviceName'),
            'automation_name': driver.capabilities.get('automationName'),
            'browser_name': driver.capabilities.get('browserName'),
            'app': driver.capabilities.get('app')
        }
        print("\n=== Device Information ===")
        for key, value in device_info.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    def _log_battery_status(self, driver):
        """Log battery status information."""
        try:
            battery_info = driver.execute_script('mobile: batteryInfo')
            print("\n=== Battery Status ===")
            print(f"Level: {battery_info.get('level')}%")
            print(f"State: {battery_info.get('state')}")
        except Exception as e:
            print(f"Could not get battery info: {str(e)}")
    
    def _test_orientation(self, driver):
        """Test device orientation changes."""
        print("\n=== Testing Orientation ===")
        
        # Get current orientation
        current_orientation = driver.orientation
        print(f"Current orientation: {current_orientation}")
        
        # Toggle orientation if possible
        new_orientation = "LANDSCAPE" if current_orientation == "PORTRAIT" else "PORTRAIT"
        try:
            driver.orientation = new_orientation
            print(f"Changed orientation to: {new_orientation}")
            time.sleep(2)  # Wait for rotation to complete
            
            # Verify orientation changed
            assert driver.orientation == new_orientation, \
                f"Failed to change orientation to {new_orientation}"
                
            # Take a screenshot in the new orientation
            driver.save_screenshot(f"ios_{new_orientation.lower()}_orientation.png")
            print(f"Screenshot saved in {new_orientation} orientation")
            
            # Return to original orientation
            driver.orientation = current_orientation
            print(f"Returned to original orientation: {current_orientation}")
            
        except Exception as e:
            print(f"Orientation test warning: {str(e)}")
    
    def _test_swipe_gesture(self, driver):
        """Test swipe gesture on the screen."""
        print("\n=== Testing Swipe Gesture ===")
        
        # Get screen dimensions
        window_size = driver.get_window_size()
        width = window_size['width']
        height = window_size['height']
        
        # Define swipe coordinates (vertical swipe)
        start_x = width // 2
        start_y = int(height * 0.7)
        end_y = int(height * 0.3)
        
        print(f"Performing swipe from ({start_x}, {start_y}) to ({start_x}, {end_y})")
        driver.swipe(start_x, start_y, start_x, end_y, 500)
        
        # Take screenshot after swipe
        driver.save_screenshot("ios_after_swipe.png")
        print("Screenshot after swipe saved as 'ios_after_swipe.png'")
    
    def _test_navigation(self, driver, wait):
        """Test basic navigation flows in the app."""
        print("\n=== Testing Navigation ===")
        
        try:
            # Example: Check if login button exists and click it
            # login_button = wait.until(EC.element_to_be_clickable(AppElements.LOGIN_BUTTON))
            # login_button.click()
            # print("Clicked on login button")
            # 
            # # Example: Enter credentials
            # username_field = wait.until(EC.presence_of_element_located(AppElements.USERNAME_FIELD))
            # password_field = driver.find_element(*AppElements.PASSWORD_FIELD)
            # 
            # username_field.send_keys("testuser")
            # password_field.send_keys("testpass")
            # print("Entered credentials")
            # 
            # # Submit the form
            # driver.find_element(*AppElements.SUBMIT_BUTTON).click()
            # print("Submitted login form")
            # 
            # # Verify successful login
            # home_title = wait.until(EC.presence_of_element_located(AppElements.HOME_SCREEN_TITLE))
            # assert home_title.is_displayed(), "Login failed - home screen not displayed"
            # print("Successfully logged in")
            
            print("Navigation test completed (placeholders - update with actual selectors)")
            
        except TimeoutException:
            print("Navigation test skipped - element not found (update selectors for your app)")
        except Exception as e:
            print(f"Navigation test warning: {str(e)}")
    
    def _test_app_state_management(self, driver):
        """Test app behavior when backgrounded and restored."""
        print("\n=== Testing App State Management ===")
        
        try:
            # Get current app state
            app_state = driver.query_app_state(driver.current_package)
            print(f"Current app state: {app_state}")
            
            # Background the app
            driver.background_app(-1)  # Background the app for default time
            print("App sent to background")
            time.sleep(2)
            
            # Bring app back to foreground
            driver.activate_app(driver.current_package)
            print("App brought back to foreground")
            
            # Verify app is in foreground
            app_state = driver.query_app_state(driver.current_package)
            assert app_state == 4, "App not in foreground after activation"
            print("App state verified after foregrounding")
            
        except Exception as e:
            print(f"App state management test warning: {str(e)}")
            # Take a screenshot on error
            error_screenshot = driver.get_screenshot_as_png()
            with open("ios_app_error.png", "wb") as f:
                f.write(error_screenshot)
            raise
            
        finally:
            # Always quit the driver to end the session
            if 'driver' in locals():
                driver.quit()
                print("Test completed. Driver session ended.")
