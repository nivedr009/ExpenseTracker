import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Add this import
import os  # For handling environment variables

class TestUserRegistration:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Use webdriver-manager to automatically download and set up ChromeDriver
        service = Service(ChromeDriverManager().install())  # Use ChromeDriverManager to handle ChromeDriver installation
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)

    def teardown_method(self, method):
        self.driver.quit()

    def test_userRegistration(self):
        print("🔎 Opening login page...")
        self.driver.get("http://web:8000/login/")

        print("🚀 Clicking 'Register here' link...")
        register_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Register here")))
        register_link.click()

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys(os.getenv("TEST_NEW_USERNAME", "newuser"))

        print("🧪 Entering email...")
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys(os.getenv("TEST_NEW_EMAIL", "newuser@gmail.com"))

        print("🧪 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(os.getenv("TEST_NEW_PASSWORD", "qwerty"))

        print("🚀 Clicking register button...")
        register_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-dark")
        register_button.click()

        print("⏳ Waiting for dashboard to load (after registration)...")
        try:
            dashboard_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]"))
            )
            print("✅ Successfully redirected to dashboard.")
        except Exception as e:
            print("❌ Dashboard not loaded. Registration might have failed.")
            raise e

        # ✅ Assert dashboard is shown, not based on URL
        assert dashboard_element is not None, "❌ Dashboard element not found after registration."
        print("✅ Registration test passed.")

