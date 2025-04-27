"""
iOS Native App Automation Test (LambdaTest Cloud, Appium)
This script demonstrates native app automation on LambdaTest using Appium and Python for iOS.
iOS app: https://prod-mobile-artefacts.lambdatest.com/assets/docs/proverbial_ios.ipa
"""
import os
import pytest
from appium import webdriver

LAMBDATEST_USERNAME = os.getenv("LT_USERNAME")
LAMBDATEST_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")

IOS_CAPS = {
    "platformName": "iOS",
    "deviceName": "iPhone 12",
    "platformVersion": "14",
    "app": "https://prod-mobile-artefacts.lambdatest.com/assets/docs/proverbial_ios.ipa",
    "isRealMobile": True,
    "build": "Native App Build",
    "name": "iOS Native App Test"
}

@pytest.mark.skipif(not LAMBDATEST_USERNAME or not LAMBDATEST_ACCESS_KEY, reason="LambdaTest credentials not set")
def test_ios_native_app():
    desired_caps = IOS_CAPS.copy()
    driver = webdriver.Remote(
        command_executor=f"https://{LAMBDATEST_USERNAME}:{LAMBDATEST_ACCESS_KEY}@mobile-hub.lambdatest.com/wd/hub",
        desired_capabilities=desired_caps
    )
    try:
        print("iOS app launched!")
        # You can add more app interactions as needed
    finally:
        driver.quit()
