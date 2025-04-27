"""
Native App Automation Test (LambdaTest Cloud, Appium)
This script demonstrates native app automation on LambdaTest using Appium and Python.
Android app: https://prod-mobile-artefacts.lambdatest.com/assets/docs/proverbial_android.apk
iOS app: https://prod-mobile-artefacts.lambdatest.com/assets/docs/proverbial_ios.ipa
"""
import os
import pytest
from appium import webdriver

LAMBDATEST_USERNAME = os.getenv("LT_USERNAME")
LAMBDATEST_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")

ANDROID_CAPS = {
    "platformName": "Android",
    "deviceName": "Galaxy S21",
    "platformVersion": "11.0",
    "app": "https://prod-mobile-artefacts.lambdatest.com/assets/docs/proverbial_android.apk",
    "isRealMobile": True,
    "build": "Native App Build",
    "name": "Android Native App Test"
}

@pytest.mark.skipif(not LAMBDATEST_USERNAME or not LAMBDATEST_ACCESS_KEY, reason="LambdaTest credentials not set")
def test_android_native_app():
    desired_caps = ANDROID_CAPS.copy()
    driver = webdriver.Remote(
        command_executor=f"https://{LAMBDATEST_USERNAME}:{LAMBDATEST_ACCESS_KEY}@mobile-hub.lambdatest.com/wd/hub",
        desired_capabilities=desired_caps
    )
    try:
        assert driver.is_app_installed("com.lambdatest.proverbial")
        print("Android app launched and installed!")
        # You can add more app interactions as needed
    finally:
        driver.quit()
