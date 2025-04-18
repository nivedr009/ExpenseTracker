import pytest
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserLoginwithCorrectCredentials:
    def setup_method(self, method):
        # Set up Chrome options to run in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (necessary for Docker)
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome Docker's limited memory
        chrome_options.add_argument("--remote-debugging-port=9222")  # Optional for debugging

        # Set the executable path of ChromeDriver inside the Docker container
        service = ChromeService(executable_path="/usr/local/bin/chromedriver")  # Path in Docker container
        self.driver = Chrome(service=service, options=chrome_options)  # Pass Chrome options
        self.driver.maximize_window()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_userLoginwithCorrectCredentials(self):
        self.driver.get("http://localhost:8000/login/")  # URL for your Django app
        time.sleep(0.5)

        self.driver.find_element(By.NAME, "username").send_keys("nived")
        time.sleep(0.5)

        self.driver.find_element(By.NAME, "password").send_keys("qwerty")
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".btn-dark").click()
        time.sleep(2)

        # Wait for a dashboard element to confirm successful login
        try:
            dashboard_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]"))
            )
            print("✅ Successfully logged in. Dashboard is visible.")
        except Exception as e:
            print("❌ Login might have failed. Dashboard element not found.")
            raise e

        # Assert that the URL indicates dashboard or home
        assert "dashboard" in self.driver.current_url.lower() or "home" in self.driver.current_url.lower(), \
            "❌ Login did not redirect to dashboard/home. Current URL: " + self.driver.current_url
