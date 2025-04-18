import pytest
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserLoginErrorMessagewithIncorrectCredentials:
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

    def test_userLoginErrorMessagewithIncorrectCredentials(self):
        self.driver.get("http://localhost:8000/login/")  # URL for your Django app
        time.sleep(0.5)

        self.driver.find_element(By.NAME, "username").send_keys("nived")
        time.sleep(0.5)

        self.driver.find_element(By.NAME, "password").send_keys("123456")  # Incorrect password
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".btn-dark").click()
        time.sleep(2)

        # Wait for the error message to appear
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))  # Update class if different
            )
            assert "invalid" in error_element.text.lower(), \
                "❌ Error message does not contain 'invalid'. Found: " + error_element.text
            print("✅ Error message displayed correctly:", error_element.text)
        except Exception as e:
            print("❌ Error message not found or did not match expectation.")
            raise e
