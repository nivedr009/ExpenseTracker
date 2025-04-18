import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserLoginwithCorrectCredentials:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Using default path since chromedriver is already in /usr/local/bin
        service = ChromeService()
        self.driver = Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()

    def test_userLoginwithCorrectCredentials(self):
        print("🔎 Opening login page...")
        self.driver.get("http://localhost:8000/login/")

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("nived")

        print("🧪 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("qwerty")

        print("🚀 Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-dark")
        login_button.click()

        print("⏳ Waiting for Dashboard to appear...")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]"))
            )
            print("✅ Successfully logged in. Dashboard is visible.")
        except Exception as e:
            print("❌ Login might have failed. Dashboard element not found.")
            raise e

        # Assert URL contains dashboard or home
        current_url = self.driver.current_url.lower()
        print(f"🌐 Redirected to: {current_url}")
        assert "dashboard" in current_url or "home" in current_url, \
            f"❌ Login did not redirect to dashboard/home. URL: {current_url}"
