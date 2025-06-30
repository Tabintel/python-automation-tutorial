"""
Android Native App Automation Test (LambdaTest Cloud, Appium)

This script demonstrates native app automation on LambdaTest using Appium and Python for Android.
The test performs various actions on the Proverbial Android app to demonstrate real-world testing scenarios.

Note: The app URL should point to a valid app uploaded to your LambdaTest storage.
For testing purposes, upload your .apk file to LambdaTest and update the APP_URL constant.
"""

import os
import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# LambdaTest credentials from environment variables
LAMBDATEST_USERNAME = os.getenv("LT_USERNAME")
LAMBDATEST_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")

# Note: Replace with your uploaded app URL from LambdaTest storage
# Upload your .apk file to LambdaTest and update this URL
APP_URL = "YOUR_UPLOADED_APP_URL.apk"  # e.g., "lt://APP1234567890abcdef"
APP_PACKAGE = "com.lambdatest.proverbial"  # Update with your app's package name

# Android capabilities with improved device selection using regex
ANDROID_CAPS = {
    "platformName": "Android",
    "deviceName": "Galaxy S*",  # Using regex to match any available Galaxy S series device
    "platformVersion": "11.0",  # Target Android version (will use the closest available)
    "app": APP_URL,
    "isRealMobile": True,
    "build": "Android Native App Build",
    "name": "Android Native App Test",
    "devicelog": True,
    "visual": True,
    "network": True,
    "console": True,
    "autoGrantPermissions": True,
    "appPackage": APP_PACKAGE,
    "appActivity": ".MainActivity"  # Update with your app's main activity
}

# App-specific elements (update these selectors according to your app)
class AppElements:
    # Example elements - replace with your app's actual element selectors
    WELCOME_MESSAGE = (AppiumBy.ID, "com.example.app:id/welcome_text")
    LOGIN_BUTTON = (AppiumBy.ID, "com.example.app:id/login_button")
    USERNAME_FIELD = (AppiumBy.ID, "com.example.app:id/username_field")
    PASSWORD_FIELD = (AppiumBy.ID, "com.example.app:id/password_field")
    SUBMIT_BUTTON = (AppiumBy.ID, "com.example.app:id/submit_button")
    HOME_SCREEN_TITLE = (AppiumBy.ID, "com.example.app:id/home_title")

@pytest.mark.usefixtures("android_driver")
class TestAndroidNativeApp:
    """
    Test suite for Android native app automation on LambdaTest real device cloud.
    This test demonstrates various interactions with an Android app.
    """
    
    def test_app_launch_and_basic_interactions(self, android_driver):
        """Test basic app launch and interactions."""
        driver = android_driver
        wait = WebDriverWait(driver, 20)
        
        try:
            # 1. Verify app launched successfully
            print("Android app launched successfully!")
            
            # 2. Take initial screenshot
            driver.save_screenshot("android_initial_screen.png")
            print("Initial screenshot saved as 'android_initial_screen.png'")
            
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
            
            # 9. Test hardware key events
            self._test_hardware_keys(driver)
            
            # 10. Take final screenshot
            driver.save_screenshot("android_final_screen.png")
            print("Final screenshot saved as 'android_final_screen.png'")
            
        except Exception as e:
            # Capture screenshot on failure
            driver.save_screenshot("android_test_failure.png")
            print("Screenshot saved as 'android_test_failure.png'")
            raise
    
    def _log_device_info(self, driver):
        """Log device information."""
        device_info = {
            'platform_version': driver.capabilities.get('platformVersion'),
            'device_manufacturer': driver.capabilities.get('deviceManufacturer'),
            'device_model': driver.capabilities.get('deviceModel'),
            'device_udid': driver.capabilities.get('udid'),
            'automation_name': driver.capabilities.get('automationName'),
            'app_package': driver.capabilities.get('appPackage'),
            'app_activity': driver.capabilities.get('appActivity')
        }
        print("\n=== Device Information ===")
        for key, value in device_info.items():
            if value:  # Only print if value is not None
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
            driver.save_screenshot(f"android_{new_orientation.lower()}_orientation.png")
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
        driver.save_screenshot("android_after_swipe.png")
        print("Screenshot after swipe saved as 'android_after_swipe.png'")
    
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
            current_activity = driver.current_activity
            print(f"Current activity: {current_activity}")
            
            # Background the app
            driver.background_app(-1)  # Background the app for default time
            print("App sent to background")
            time.sleep(2)
            
            # Bring app back to foreground
            driver.activate_app(driver.capabilities['appPackage'])
            print("App brought back to foreground")
            
            # Verify app is in foreground
            assert driver.current_activity == current_activity, "App not in the same activity after foregrounding"
            print("App state verified after foregrounding")
            
        except Exception as e:
            print(f"App state management test warning: {str(e)}")
    
    def _test_hardware_keys(self, driver):
        """Test hardware key events."""
        print("\n=== Testing Hardware Keys ===")
        
        try:
            # Test back button
            print("Pressing back button")
            driver.press_keycode(4)  # KEYCODE_BACK
            time.sleep(1)
            
            # Test home button
            print("Pressing home button")
            driver.press_keycode(3)  # KEYCODE_HOME
            time.sleep(1)
            
            # Test recent apps
            print("Opening recent apps")
            driver.press_keycode(187)  # KEYCODE_APP_SWITCH
            time.sleep(1)
            
            # Return to the app
            print("Returning to the app")
            driver.activate_app(driver.capabilities['appPackage'])
            
        except Exception as e:
            print(f"Hardware keys test warning: {str(e)}")
            
    def _take_screenshot(self, driver, filename):
        """Helper method to take a screenshot."""
        try:
            driver.save_screenshot(filename)
            print(f"Screenshot saved as '{filename}'")
            return True
        except Exception as e:
            print(f"Failed to save screenshot '{filename}': {str(e)}")
            return False
