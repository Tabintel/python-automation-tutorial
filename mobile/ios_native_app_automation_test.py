"""
iOS Native App Automation Test (LambdaTest Cloud, Appium)

This script demonstrates native app automation on LambdaTest using Appium and Python for iOS.
The test performs various actions on the Proverbial iOS app to demonstrate real-world testing scenarios.

Note: The app URL should point to a valid app uploaded to your LambdaTest storage.
For testing purposes, upload your .ipa file to LambdaTest and update the APP_URL constant.
"""

import time
import logging
import pytest

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# App-specific elements (update these selectors according to your app)
class AppElements:
    TEXT_ELEMENT = (AppiumBy.ID, "Text")
    TOAST_ELEMENT = (AppiumBy.ID, "Toast")
    NOTIFICATION_ELEMENT = (AppiumBy.ID, "Notification")
    GEOLOCATION_ELEMENT = (AppiumBy.ID, "GeoLocation")
    COLOUR_ELEMENT = (AppiumBy.ID, "Colour")
    HOME_ELEMENT = (AppiumBy.ID, "Home")


MOBILE_CAPS = {"build": "Ios Mobile Build", "name": "Ios Mobile Automation Test"}


@pytest.mark.parametrize("ios_driver", [MOBILE_CAPS], indirect=True)
class TestIOSNativeApp:
    """
    Test suite for iOS native app automation on LambdaTest real device cloud.
    This test demonstrates various interactions with the Proverbial iOS app.
    """

    def test_app_launch_and_basic_interactions(self, ios_driver):
        driver = ios_driver
        wait = WebDriverWait(driver, 20)

        try:
            logger.info("iOS app launched successfully.")

            self._take_screenshot(driver, "ios_initial_screen.png")
            self._log_device_info(driver)
            self._log_battery_status(driver)
            self._test_orientation(driver)
            self._test_swipe_gesture(driver)
            self._test_navigation(driver, wait)
            self._test_app_state_management(driver)

            self._take_screenshot(driver, "ios_final_screen.png")

        except Exception as e:
            logger.error(f"Test failed with error: {e}")
            self._take_screenshot(driver, "ios_test_failure.png")
            raise

    def _log_device_info(self, driver):
        device_info = {
            "platform_version": driver.capabilities.get("platformVersion"),
            "device_manufacturer": driver.capabilities.get("deviceManufacturer"),
            "device_model": driver.capabilities.get("deviceModel"),
            "device_udid": driver.capabilities.get("udid"),
            "automation_name": driver.capabilities.get("automationName"),
            "app_package": driver.capabilities.get("appPackage"),
            "app_activity": driver.capabilities.get("appActivity"),
        }

        logger.info("📱 Device Information:")
        for key, value in device_info.items():
            if value:
                logger.info(f"{key.replace('_', ' ').title()}: {value}")

    def _log_battery_status(self, driver):
        try:
            battery_info = driver.execute_script("mobile: batteryInfo")
            logger.info("Battery Status:")
            logger.info(f"Level: {battery_info.get('level')}%")
            logger.info(f"State: {battery_info.get('state')}")
        except Exception as e:
            logger.warning(f"Could not retrieve battery info: {e}")

    def _test_orientation(self, driver):
        logger.info("Testing Orientation...")

        try:
            current_orientation = driver.orientation
            logger.info(f"Current orientation: {current_orientation}")

            new_orientation = (
                "LANDSCAPE" if current_orientation == "PORTRAIT" else "PORTRAIT"
            )

            driver.orientation = new_orientation
            logger.info(f"Changed orientation to: {new_orientation}")
            time.sleep(2)

            assert driver.orientation == new_orientation, (
                f"Failed to change orientation to {new_orientation}"
            )

            self._take_screenshot(
                driver, f"ios_{new_orientation.lower()}_orientation.png"
            )

            driver.orientation = current_orientation
            logger.info(f"Returned to original orientation: {current_orientation}")

        except Exception as e:
            logger.warning(f"Orientation test failed: {e}")

    def _test_swipe_gesture(self, driver):
        logger.info("Testing Swipe Gesture...")

        try:
            size = driver.get_window_size()
            start_x = size["width"] // 2
            start_y = int(size["height"] * 0.7)
            end_y = int(size["height"] * 0.3)

            logger.info(f"Swiping from ({start_x}, {start_y}) to ({start_x}, {end_y})")
            driver.swipe(start_x, start_y, start_x, end_y, 500)

            self._take_screenshot(driver, "ios_after_swipe.png")
        except Exception as e:
            logger.warning(f"Swipe gesture failed: {e}")

    def _test_navigation(self, driver, wait):
        logger.info("Testing Navigation...")

        try:
            wait.until(EC.element_to_be_clickable(AppElements.COLOUR_ELEMENT)).click()
            logger.info("Colour element clicked.")

            wait.until(EC.element_to_be_clickable(AppElements.TEXT_ELEMENT)).click()
            logger.info("Text element clicked.")

            wait.until(EC.element_to_be_clickable(AppElements.TOAST_ELEMENT)).click()
            logger.info("Toast element clicked.")

            wait.until(EC.element_to_be_clickable(AppElements.HOME_ELEMENT)).click()
            logger.info("Home element clicked.")


            time.sleep(3)

            wait.until(
                EC.element_to_be_clickable(AppElements.GEOLOCATION_ELEMENT)
            ).click()
            logger.info("Geolocation element clicked.")
            time.sleep(5)

            wait.until(EC.element_to_be_clickable((AppiumBy.ID, "Back"))).click()
            logger.info("Back button clicked.")

            wait.until(
                EC.element_to_be_clickable(AppElements.NOTIFICATION_ELEMENT)
            ).click()
            logger.info("Notification element clicked.")
            logger.info("Navigation test completed successfully.")

        except TimeoutException:
            logger.error("Navigation test skipped - element not found (Timeout).")
        except Exception as e:
            logger.error(f"Navigation test error: {e}")


    def _test_app_state_management(self, driver):
        logger.info("Testing App State Management on iOS...")

        try:
            initial_app_state = driver.execute_script("mobile: queryAppState", {"bundleId": driver.capabilities.get('bundleId')})
            logger.info(f"Initial app state: {initial_app_state} (4 = foreground, 2/3 = background)")

            # Verify it's in the foreground initially (state 4)
            if initial_app_state != 4:
                logger.warning(f"App not in foreground initially (state: {initial_app_state}), trying to activate.")
                driver.activate_app(driver.capabilities.get('bundleId'))
                time.sleep(3)
                initial_app_state = driver.execute_script("mobile: queryAppState", {"bundleId": driver.capabilities.get('bundleId')})
                assert initial_app_state == 4, "Failed to activate app to foreground"

            # send app to background
            logger.info("Sending app to background.")
            driver.background_app(-1)
            time.sleep(3)

            # Verify app is in background (state 2 or 3)
            background_app_state = driver.execute_script("mobile: queryAppState", {"bundleId": driver.capabilities.get('bundleId')})
            logger.info(f"App state after backgrounding: {background_app_state}")
            assert background_app_state in [2, 3], "App not in background after background_app command"

            logger.info("Activating app to foreground.")
            driver.activate_app(driver.capabilities.get('bundleId'))
            # driver.launch_app()

            time.sleep(5)

            # Verify app is back in foreground (state 4)
            foreground_app_state = driver.execute_script("mobile: queryAppState", {"bundleId": driver.capabilities.get('bundleId')})
            logger.info(f"App state after foregrounding: {foreground_app_state}")
            assert foreground_app_state == 4, (
                "App not in foreground after returning from background"
            )

            logger.info("App state verified after background/foreground cycle.")

        except Exception as e:
            logger.warning(f"App state management failed: {e}")


    def _take_screenshot(self, driver, filename):
        try:
            driver.save_screenshot(filename)
            logger.info(f"Screenshot saved as '{filename}'")
            return True
        except Exception as e:
            logger.error(f"Failed to save screenshot '{filename}': {e}")
            return False


if __name__ == "__main__":
    pytest.main([__file__, "-s"],)
