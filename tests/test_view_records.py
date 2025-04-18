import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Add this import
import os  # For handling environment variables

class TestViewTransactionRecords:
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

    def test_viewTransactionRecords(self):
        print("🔎 Opening login page...")
        # Ensure that you update the URL to use the Docker container's service name or IP
        self.driver.get("http://web:8000/login/")  # Assuming 'web' is the Docker service name

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys(os.getenv("TEST_USERNAME", "nived"))

        print("🧪 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(os.getenv("TEST_PASSWORD", "qwerty"))

        print("🚀 Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-dark")
        login_button.click()

        print("⏳ Waiting for 'View Records' link to appear...")
        view_records_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "View Records")))
        print("✅ 'View Records' link is visible. Clicking it...")
        view_records_link.click()

        print("⏳ Waiting for transaction records page to load...")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Transaction Records')]"))
            )
            print("✅ Transaction records page loaded successfully.")
        except Exception as e:
            print("❌ Failed to load transaction records page.")
            raise e

        # Assert URL contains 'records' or similar
        current_url = self.driver.current_url.lower()
        print(f"🌐 Redirected to: {current_url}")
        assert "records" in current_url, \
            f"❌ Did not redirect to transaction records page. URL: {current_url}"