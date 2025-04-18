import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

class TestUserRegistration:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)

    def teardown_method(self, method):
        self.driver.quit()

    def test_userRegistration(self):
        print("⏳ Opening login page...")
        self.driver.get("http://web:8000/login/")

        print("📝 Clicking 'Register here' link...")
        register_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Register here")))
        register_link.click()

        print("🖋️ Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("nived")  # Hardcoded username

        print("🖋️ Entering email...")
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys("nived@example.com")  # Use a dummy email

        print("🖋️ Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("qwerty")  # Hardcoded password

        print("🖱️ Clicking register button...")
        register_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-dark")
        register_button.click()

        print("⚠️ Waiting for error message (username already exists)...")
        try:
            # Increased wait time to 20 seconds
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            assert "Username already exists" in error_message.text, "❌ 'Username already exists' message not found."
            print("✅ 'Username already exists' message displayed.")
        except Exception as e:
            print("❌ Error message for existing username not displayed.")
            self.driver.save_screenshot("error_screenshot.png")  # Take a screenshot on failure
            raise e
